#!/usr/bin/env python3
"""Analyze Claude Code conversation history to build a communication profile.

Primary data source: ~/.claude/history.jsonl (user input history)
Supplemental source: ~/.claude/projects/*/*.jsonl (for interrupt counts, where available)

Usage:
    python3 analyze_conversations.py --all
    python3 analyze_conversations.py --all --exclude company-simulator
    python3 analyze_conversations.py --project awx-tui --project handbook
    python3 analyze_conversations.py --all --compare previous-profile.json -o profile.json
"""

import argparse
import json
import re
import string
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


SYSTEM_PREFIXES = [
    "<system-reminder>",
    "<command-name>",
    "<local-command",
    "This session is being continued",
    "Base directory for this skill:",
]

CLI_SLASH_COMMANDS = {
    "/exit", "/resume", "/cost", "/compact", "/context", "/status",
    "/model", "/rename", "/quit", "/info", "/usage", "/config",
    "/plugin", "/permissions", "/plan", "/terminal-setup", "/help",
    "/clear", "/doctor", "/fast", "/slow", "/review", "/init",
    "/simplify", "/memory", "/mcp", "/login", "/logout", "/vim",
}

PASTE_MARKER_RE = re.compile(r"\[Pasted text #\d+ \+\d+ lines?\]")

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "can", "could", "may", "might", "must", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "about",
    "between", "through", "after", "before", "above", "below", "up",
    "down", "out", "off", "over", "under", "again", "further", "then",
    "once", "that", "this", "these", "those", "it", "its", "he", "she",
    "they", "we", "you", "me", "him", "her", "us", "them", "my", "your",
    "his", "our", "their", "what", "which", "who", "whom", "when",
    "where", "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "not", "only", "same", "so",
    "than", "too", "very", "just", "but", "and", "or", "if", "because",
    "until", "while", "although", "though", "even", "also", "still",
    "already", "yet", "here", "there", "now", "i", "am", "s", "t", "re",
    "ve", "ll", "d", "m", "don", "doesn", "didn", "won", "wouldn",
    "shouldn", "couldn", "isn", "aren", "wasn", "weren", "hasn", "haven",
    "hadn",
}


def load_history(history_path, project_filter=None, exclude_filters=None):
    """Load and filter messages from history.jsonl."""
    messages = []

    with open(history_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            display = entry.get("display", "")
            project = entry.get("project", "")
            ts_ms = entry.get("timestamp", 0)
            session_id = entry.get("sessionId")

            if not display or not display.strip():
                continue

            if project_filter:
                if not any(pf in project for pf in project_filter):
                    continue

            if exclude_filters:
                if any(ef in project for ef in exclude_filters):
                    continue

            if any(display.startswith(prefix) for prefix in SYSTEM_PREFIXES):
                continue

            if display.startswith("/") and not display.startswith("/home"):
                first_token = display.split()[0].lower() if display.split() else ""
                if first_token in CLI_SLASH_COMMANDS:
                    continue

            ts_dt = None
            if ts_ms:
                try:
                    ts_dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
                except (ValueError, OSError):
                    pass

            cleaned = PASTE_MARKER_RE.sub("", display).strip()
            has_paste = bool(entry.get("pastedContents"))

            messages.append({
                "text": cleaned if cleaned else "",
                "raw_display": display,
                "length": len(cleaned) if cleaned else 0,
                "timestamp": ts_dt,
                "project": project,
                "session_id": session_id,
                "has_paste": has_paste,
            })

    return messages


def extract_project_name(project_path):
    """Extract a readable short name from a full project path."""
    p = Path(project_path)
    return p.name if p.name else str(p)


def detect_sessions(messages):
    """Group messages into sessions using sessionId or time gaps."""
    session_map = {}
    session_counter = defaultdict(int)

    by_project = defaultdict(list)
    for i, msg in enumerate(messages):
        by_project[msg["project"]].append((i, msg))

    for project, proj_msgs in by_project.items():
        proj_msgs.sort(key=lambda x: x[1]["timestamp"] or datetime.min.replace(tzinfo=timezone.utc))
        current_session = None
        prev_ts = None

        for idx, msg in proj_msgs:
            if msg["session_id"]:
                current_session = msg["session_id"]
            else:
                gap = float("inf")
                if prev_ts and msg["timestamp"]:
                    gap = (msg["timestamp"] - prev_ts).total_seconds()
                if gap > 1800 or current_session is None:
                    short = extract_project_name(project)
                    session_counter[short] += 1
                    current_session = f"inferred-{short}-{session_counter[short]}"

            session_map[idx] = current_session
            if msg["timestamp"]:
                prev_ts = msg["timestamp"]

    unique_sessions = set(session_map.values())
    sessions_per_project = defaultdict(set)
    for idx, sid in session_map.items():
        sessions_per_project[messages[idx]["project"]].add(sid)

    return {
        "total_sessions": len(unique_sessions),
        "sessions_per_project": {k: len(v) for k, v in sessions_per_project.items()},
        "session_map": session_map,
        "session_first_indices": _find_session_firsts(session_map),
    }


def _find_session_firsts(session_map):
    """Find the first message index for each session."""
    firsts = {}
    for idx, sid in sorted(session_map.items()):
        if sid not in firsts:
            firsts[sid] = idx
    return set(firsts.values())


def count_interrupts_from_project_jsonl():
    """Count [Request interrupted by user] from project JSONL files (supplemental)."""
    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.exists():
        return 0, {}

    total = 0
    per_project = Counter()

    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith("."):
            continue
        for jsonl_file in project_dir.glob("*.jsonl"):
            try:
                with open(jsonl_file) as f:
                    for line in f:
                        if "Request interrupted" in line:
                            try:
                                entry = json.loads(line)
                                etype = entry.get("type", entry.get("role", ""))
                                if etype == "user":
                                    content = ""
                                    msg = entry.get("message", entry.get("content", ""))
                                    if isinstance(msg, str):
                                        content = msg
                                    elif isinstance(msg, dict):
                                        content = str(msg.get("content", ""))
                                    if "[Request interrupted" in content:
                                        total += 1
                                        per_project[project_dir.name] += 1
                            except json.JSONDecodeError:
                                continue
            except (PermissionError, OSError):
                continue

    return total, dict(per_project)


def tokenize(text):
    """Tokenize text into lowercase words, stripping punctuation."""
    text = text.lower()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"/[\w/.-]+", "", text)
    words = text.split()
    result = []
    for w in words:
        w = w.strip(string.punctuation + "\u2018\u2019\u201c\u201d")
        if w and len(w) > 1 and not w.isdigit():
            result.append(w)
    return result


def discover_phrases(messages):
    """Discover frequent words and phrases from message text."""
    word_counter = Counter()
    bigram_counter = Counter()
    trigram_counter = Counter()
    ending_counter = Counter()
    opening_word_counter = Counter()
    opening_bigram_counter = Counter()
    opening_trigram_counter = Counter()

    for msg in messages:
        if not msg["text"] or msg["has_paste"] and not msg["text"].strip():
            continue

        words = tokenize(msg["text"])
        if not words:
            continue

        for w in words:
            if w not in STOP_WORDS:
                word_counter[w] += 1

        for i in range(len(words) - 1):
            bg = f"{words[i]} {words[i+1]}"
            if not (words[i] in STOP_WORDS and words[i+1] in STOP_WORDS):
                bigram_counter[bg] += 1

        for i in range(len(words) - 2):
            tg = f"{words[i]} {words[i+1]} {words[i+2]}"
            if not all(w in STOP_WORDS for w in [words[i], words[i+1], words[i+2]]):
                trigram_counter[tg] += 1

        last_word = msg["text"].rstrip().split()[-1].lower() if msg["text"].strip() else None
        if last_word:
            ending_counter[last_word] += 1

        raw_words = msg["text"].lower().split()
        if raw_words:
            opening_word_counter[raw_words[0]] += 1
        if len(raw_words) >= 2:
            opening_bigram_counter[f"{raw_words[0]} {raw_words[1]}"] += 1
        if len(raw_words) >= 3:
            opening_trigram_counter[f"{raw_words[0]} {raw_words[1]} {raw_words[2]}"] += 1

    return {
        "top_words": [[w, c] for w, c in word_counter.most_common(30)],
        "top_bigrams": [[p, c] for p, c in bigram_counter.most_common(30) if c >= 3],
        "top_trigrams": [[p, c] for p, c in trigram_counter.most_common(20) if c >= 3],
        "ending_patterns": [[w, c] for w, c in ending_counter.most_common(20)],
        "opening_words": [[w, c] for w, c in opening_word_counter.most_common(15)],
        "opening_bigrams": [[p, c] for p, c in opening_bigram_counter.most_common(15)],
        "opening_trigrams": [[p, c] for p, c in opening_trigram_counter.most_common(15)],
    }


def analyze_verbal_patterns(messages):
    """Analyze verbal patterns — general detectors + dynamic phrase discovery."""
    texts = [m["text"].lower() for m in messages if m["text"]]
    raw_texts = [m["text"] for m in messages if m["text"]]

    # --- Opener patterns ---
    openers = {
        "starts_with_hey": sum(1 for t in texts if t.startswith("hey")),
        "starts_with_ok": sum(1 for t in texts if t.startswith("ok ")),
        "starts_with_yes": sum(1 for t in texts if t.startswith("yes")),
        "starts_with_no": sum(1 for t in texts if re.match(r"^no[\s,.]", t) or t == "no"),
        "starts_with_so": sum(1 for t in texts if t.startswith("so ")),
        "starts_with_well": sum(1 for t in texts if t.startswith("well")),
        "starts_with_lets": sum(1 for t in texts if t.startswith("let's") or t.startswith("lets")),
        "starts_with_can_you": sum(1 for t in texts if t.startswith("can you")),
        "starts_with_i_think": sum(1 for t in texts if t.startswith("i think")),
    }

    # --- Punctuation intensity ---
    punctuation = {
        "ends_with_question": sum(1 for t in texts if t.rstrip().endswith("?")),
        "contains_exclamation": sum(1 for t in texts if "!" in t),
        "multi_exclamation": sum(1 for t in texts if "!!" in t),
        "multi_question": sum(1 for t in texts if "??" in t),
        "all_caps_words": sum(
            len(re.findall(r"\b[A-Z]{2,}\b", rt))
            for rt in raw_texts
            if re.search(r"\b[A-Z]{2,}\b", rt)
        ),
        "msgs_with_all_caps": sum(
            1 for rt in raw_texts
            if re.search(r"\b[A-Z]{3,}\b", rt)
            and not re.match(r"^[A-Z\s\-]+$", rt.strip())
        ),
    }

    # --- Pronoun / collaboration ---
    pronouns = {
        "uses_we": sum(1 for t in texts if re.search(r"\bwe\b", t)),
        "uses_I": sum(1 for rt in raw_texts if re.search(r"\bI\b", rt)),
    }
    we_count = pronouns["uses_we"]
    i_count = pronouns["uses_I"]
    pronouns["we_vs_I_ratio"] = round(we_count / i_count, 2) if i_count > 0 else None

    # --- Typing style fingerprints ---
    style = {
        "ellipsis_usage": sum(1 for t in texts if "..." in t),
        "starts_lowercase": sum(1 for rt in raw_texts if rt[0].islower()),
        "emoticon_usage": sum(1 for t in texts if re.search(r"[:;][PpDd/\\)(]", t)),
        "emoji_shortcode_usage": sum(1 for t in texts if re.search(r":[a-z_]+:", t)),
        "dash_connectors": sum(1 for rt in raw_texts if " -- " in rt or " - " in rt),
        "parenthetical_asides": sum(1 for rt in raw_texts if re.search(r"\([^)]{3,}\)", rt)),
    }

    # --- Humor / affect ---
    affect = {
        "contains_lol": sum(1 for t in texts if re.search(r"\blol\b", t)),
        "contains_haha": sum(1 for t in texts if re.search(r"\bhaha", t)),
    }

    # --- Confidence / hedging ---
    hedging = {
        "hedging_language": sum(
            1 for t in texts
            if re.search(r"\b(maybe|probably|i guess|idk|not sure|i suppose|might be)\b", t)
        ),
        "assertive_language": sum(
            1 for t in texts
            if re.search(r"\b(definitely|absolutely|obviously|clearly|exactly|certainly)\b", t)
        ),
    }
    hedge_count = hedging["hedging_language"]
    assert_count = hedging["assertive_language"]
    hedging["hedge_vs_assert_ratio"] = round(hedge_count / assert_count, 2) if assert_count > 0 else None

    # --- Self-correction ---
    self_correction = {
        "self_correction": sum(
            1 for t in texts
            if re.search(r"\b(actually|wait|scratch that|never mind|nevermind|well actually|nah)\b", t)
        ),
    }

    # --- Message complexity ---
    sentence_counts = []
    for t in texts:
        sents = len(re.findall(r"[.!?]+", t)) or 1
        sentence_counts.append(sents)
    complexity = {
        "avg_sentences_per_message": round(sum(sentence_counts) / len(sentence_counts), 1) if sentence_counts else 0,
    }

    # --- Totals ---
    totals = {
        "total_messages": len(messages),
        "non_empty_messages": len(texts),
    }

    general = {
        **openers,
        **punctuation,
        **pronouns,
        **style,
        **affect,
        **hedging,
        **self_correction,
        **complexity,
        **totals,
    }

    phrases = discover_phrases(messages)

    return {
        "general": general,
        **phrases,
    }


def analyze_message_lengths(messages):
    """Analyze message length distribution."""
    lengths = [m["length"] for m in messages if m["length"] > 0]
    if not lengths:
        return {}

    sorted_lengths = sorted(lengths)
    total = len(sorted_lengths)

    return {
        "min": sorted_lengths[0],
        "max": sorted_lengths[-1],
        "mean": sum(sorted_lengths) // total,
        "median": sorted_lengths[total // 2],
        "under_50": sum(1 for l in sorted_lengths if l < 50),
        "50_to_150": sum(1 for l in sorted_lengths if 50 <= l < 150),
        "150_to_500": sum(1 for l in sorted_lengths if 150 <= l < 500),
        "over_500": sum(1 for l in sorted_lengths if l >= 500),
        "total": total,
    }


def analyze_time_patterns(messages):
    """Analyze time-of-day and day-of-week patterns."""
    timestamps = [m["timestamp"] for m in messages if m["timestamp"]]
    if not timestamps:
        return {}

    hours = Counter()
    days = Counter()
    months = Counter()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for ts in timestamps:
        hours[ts.hour] += 1
        days[day_names[ts.weekday()]] += 1
        months[ts.strftime("%Y-%m")] += 1

    return {
        "hour_distribution": dict(sorted(hours.items())),
        "day_distribution": dict(days),
        "month_distribution": dict(sorted(months.items())),
        "peak_hours_utc": hours.most_common(5),
        "total_timestamps": len(timestamps),
    }


def analyze_greeting_patterns(messages, session_first_indices=None):
    """Analyze how the user opens conversations."""
    greetings = []
    session_openers = []

    for i, m in enumerate(messages):
        text = m["text"].strip()
        lower = text.lower()
        if any(lower.startswith(g) for g in ["hey ", "hi ", "hello ", "sup", "howdy", "yo "]):
            greetings.append(text[:200])

        if session_first_indices and i in session_first_indices:
            session_openers.append(text[:200])

    return {
        "greeting_messages": greetings[:30],
        "session_openers": session_openers[:30],
    }


def analyze_approval_disapproval(messages):
    """Find examples of approval and disapproval language."""
    approval_patterns = [
        "perfect", "brilliant", "nice", "well done", "make it so",
        "yes", "yeah", "go for it", "looks good", "i like",
        "nailed it", "exactly", "that's great", "love it",
        "awesome", "good call", "that works",
    ]
    disapproval_patterns = [
        "still isn't", "still doesn't", "still not", "still nothing",
        "doesn't work", "isn't working", "not working",
        "don't like", "shouldn't", "why would", "why are you",
        "bruh", "ugh", "no ", "nope", "wrong", "that's not",
    ]

    approvals = []
    disapprovals = []

    for m in messages:
        text = m["text"]
        if not text:
            continue
        lower = text.lower().strip()
        if len(text) > 300:
            continue
        for pat in approval_patterns:
            if pat in lower:
                approvals.append(text[:200])
                break
        for pat in disapproval_patterns:
            if pat in lower:
                disapprovals.append(text[:200])
                break

    return {
        "approvals": approvals[:20],
        "disapprovals": disapprovals[:20],
    }


def analyze_instruction_style(messages):
    """Analyze how the user gives instructions."""
    questions_as_instructions = []
    direct_commands = []
    thinking_out_loud = []

    for m in messages:
        text = m["text"].strip()
        if not text or len(text) > 500:
            continue
        lower = text.lower()

        if re.search(r"(shouldn't we|why can't we|what if we|what about|can we|should we|how about)", lower):
            questions_as_instructions.append(text[:200])
        elif text.count("...") >= 2 or text.count("....") >= 1:
            thinking_out_loud.append(text[:200])
        elif len(text) < 80 and not text.endswith("?"):
            direct_commands.append(text[:200])

    return {
        "questions_as_instructions": questions_as_instructions[:15],
        "direct_commands": direct_commands[:20],
        "thinking_out_loud": thinking_out_loud[:15],
    }


def build_profile(messages, session_info, include_interrupts=True):
    """Build a complete profile from the message list."""
    by_project = defaultdict(list)
    for msg in messages:
        by_project[msg["project"]].append(msg)

    project_summaries = []
    for project_path, proj_msgs in by_project.items():
        timestamps = [m["timestamp"] for m in proj_msgs if m["timestamp"]]
        project_summaries.append({
            "name": extract_project_name(project_path),
            "full_path": project_path,
            "user_messages": len(proj_msgs),
            "sessions": session_info["sessions_per_project"].get(project_path, 0),
            "date_range": {
                "first": min(timestamps).isoformat() if timestamps else None,
                "last": max(timestamps).isoformat() if timestamps else None,
            },
        })

    project_summaries.sort(key=lambda x: x["user_messages"], reverse=True)

    all_timestamps = [m["timestamp"] for m in messages if m["timestamp"]]
    date_range = {
        "first": min(all_timestamps).isoformat() if all_timestamps else None,
        "last": max(all_timestamps).isoformat() if all_timestamps else None,
    }

    profile = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_source": "~/.claude/history.jsonl",
        "date_range": date_range,
        "total_projects": len(project_summaries),
        "total_sessions": session_info["total_sessions"],
        "total_user_messages": len(messages),
        "projects": project_summaries,
        "verbal_patterns": analyze_verbal_patterns(messages),
        "message_lengths": analyze_message_lengths(messages),
        "time_patterns": analyze_time_patterns(messages),
        "greeting_patterns": analyze_greeting_patterns(
            messages,
            session_first_indices=session_info.get("session_first_indices"),
        ),
        "approval_disapproval": analyze_approval_disapproval(messages),
        "instruction_style": analyze_instruction_style(messages),
        "sample_messages": _build_sample_messages(messages),
    }

    if include_interrupts:
        interrupt_total, interrupt_per_project = count_interrupts_from_project_jsonl()
        profile["interrupts"] = {
            "total": interrupt_total,
            "per_project": interrupt_per_project,
            "note": "Counted from project JSONL files (recent data only, not full history)",
        }

    return profile


def _build_sample_messages(messages):
    """Build sample message lists for the profile."""
    non_empty = [m for m in messages if m["length"] > 0]
    shortest = sorted(non_empty, key=lambda x: x["length"])[:10]
    longest = sorted(non_empty, key=lambda x: x["length"], reverse=True)[:10]

    def serialize(msg):
        return {
            "text": msg["text"][:500],
            "length": msg["length"],
            "timestamp": msg["timestamp"].isoformat() if msg["timestamp"] else None,
            "project": extract_project_name(msg["project"]),
        }

    return {
        "shortest": [serialize(m) for m in shortest],
        "longest": [serialize(m) for m in longest],
    }


def compare_profiles(current, previous):
    """Compare current profile against a previous one."""
    diffs = {}

    prev_total = previous.get("total_user_messages", 0)
    curr_total = current.get("total_user_messages", 0)
    diffs["message_count_change"] = curr_total - prev_total

    prev_projects = {p["name"] for p in previous.get("projects", [])}
    curr_projects = {p["name"] for p in current.get("projects", [])}
    diffs["new_projects"] = sorted(curr_projects - prev_projects)
    diffs["removed_projects"] = sorted(prev_projects - curr_projects)

    prev_verbal = previous.get("verbal_patterns", {}).get("general", previous.get("verbal_patterns", {}))
    curr_verbal = current.get("verbal_patterns", {}).get("general", {})
    verbal_changes = {}
    for key in set(list(prev_verbal.keys()) + list(curr_verbal.keys())):
        if key in ("total_messages", "non_empty_messages", "we_vs_I_ratio"):
            continue
        prev_val = prev_verbal.get(key, 0)
        curr_val = curr_verbal.get(key, 0)
        if not isinstance(prev_val, (int, float)) or not isinstance(curr_val, (int, float)):
            continue
        if prev_val != curr_val:
            prev_total_msgs = prev_verbal.get("total_messages", 1)
            curr_total_msgs = curr_verbal.get("total_messages", 1)
            prev_pct = (prev_val / prev_total_msgs * 100) if prev_total_msgs else 0
            curr_pct = (curr_val / curr_total_msgs * 100) if curr_total_msgs else 0
            if abs(curr_pct - prev_pct) > 1:
                verbal_changes[key] = {
                    "previous": f"{prev_val} ({prev_pct:.1f}%)",
                    "current": f"{curr_val} ({curr_pct:.1f}%)",
                    "direction": "up" if curr_pct > prev_pct else "down",
                }
    diffs["verbal_pattern_changes"] = verbal_changes

    prev_phrases = {p[0] for p in previous.get("verbal_patterns", {}).get("top_bigrams", [])}
    curr_phrases = {p[0] for p in current.get("verbal_patterns", {}).get("top_bigrams", [])}
    diffs["new_phrases"] = sorted(curr_phrases - prev_phrases)
    diffs["dropped_phrases"] = sorted(prev_phrases - curr_phrases)

    prev_lengths = previous.get("message_lengths", {})
    curr_lengths = current.get("message_lengths", {})
    if prev_lengths and curr_lengths:
        diffs["message_length_changes"] = {
            "mean": {"previous": prev_lengths.get("mean"), "current": curr_lengths.get("mean")},
            "median": {"previous": prev_lengths.get("median"), "current": curr_lengths.get("median")},
        }

    prev_time = previous.get("time_patterns", {})
    curr_time = current.get("time_patterns", {})
    if prev_time and curr_time:
        diffs["time_pattern_changes"] = {
            "previous_peak_hours": prev_time.get("peak_hours_utc"),
            "current_peak_hours": curr_time.get("peak_hours_utc"),
        }

    diffs["date_range"] = {
        "previous": previous.get("date_range"),
        "current": current.get("date_range"),
    }

    return diffs


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Claude Code conversation history to build a communication profile"
    )
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true", help="Analyze all projects")
    scope.add_argument(
        "--project", action="append",
        help="Filter to projects matching this substring (can be repeated)",
    )
    parser.add_argument(
        "--exclude", action="append",
        help="Exclude projects matching this substring (can be repeated)",
    )
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    parser.add_argument("--compare", help="Path to a previous profile JSON to compare against")

    args = parser.parse_args()

    history_path = Path.home() / ".claude" / "history.jsonl"
    if not history_path.exists():
        sys.exit("Error: ~/.claude/history.jsonl not found. Is Claude Code installed?")

    project_filter = args.project if not args.all else None
    exclude_filters = args.exclude

    print(f"Loading history from {history_path}...", file=sys.stderr)
    messages = load_history(history_path, project_filter, exclude_filters)

    if not messages:
        sys.exit("Error: No messages found matching the given filters.")

    projects_found = len(set(m["project"] for m in messages))
    print(f"Found {len(messages)} messages across {projects_found} project(s).", file=sys.stderr)

    if exclude_filters:
        print(f"Excluding: {', '.join(exclude_filters)}", file=sys.stderr)

    print("Detecting sessions...", file=sys.stderr)
    session_info = detect_sessions(messages)
    print(f"Found {session_info['total_sessions']} session(s).", file=sys.stderr)

    print("Building profile...", file=sys.stderr)
    profile = build_profile(messages, session_info)

    if args.compare:
        compare_path = Path(args.compare)
        if not compare_path.exists():
            print(f"Warning: Previous profile not found at {compare_path}, skipping comparison.", file=sys.stderr)
        else:
            with open(compare_path) as f:
                previous = json.load(f)
            profile["comparison"] = compare_profiles(profile, previous)
            print("Comparison with previous profile included.", file=sys.stderr)

    output_json = json.dumps(profile, indent=2, default=str)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output_json)
        print(f"Profile written to {output_path}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
