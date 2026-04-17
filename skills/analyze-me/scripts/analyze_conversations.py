#!/usr/bin/env python3
"""Analyze Claude Code conversation history to build a communication profile.

Usage:
    # Analyze all projects
    python3 analyze_conversations.py --all

    # Analyze specific project(s)
    python3 analyze_conversations.py --project ~/.claude/projects/-home-user-myproject/

    # Output to file (default: stdout)
    python3 analyze_conversations.py --all -o profile.json

    # Compare against a previous profile
    python3 analyze_conversations.py --all --compare previous-profile.json -o profile.json
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


def find_claude_dir():
    """Find the ~/.claude directory."""
    claude_dir = Path.home() / ".claude"
    if not claude_dir.exists():
        sys.exit("Error: ~/.claude directory not found. Is Claude Code installed?")
    return claude_dir


def find_all_projects(claude_dir):
    """Find all project directories under ~/.claude/projects/."""
    projects_dir = claude_dir / "projects"
    if not projects_dir.exists():
        return []
    return sorted([
        p for p in projects_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    ])


def find_conversation_files(project_dir):
    """Find all JSONL conversation files in a project directory (excluding subagents)."""
    return sorted([
        f for f in project_dir.glob("*.jsonl")
        if f.is_file()
    ])


def parse_messages(filepath):
    """Parse a JSONL conversation file, yielding structured messages."""
    messages = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type", entry.get("role", ""))
            if entry_type not in ("user", "assistant"):
                continue

            timestamp = entry.get("timestamp", "")
            ts_dt = None
            if timestamp:
                try:
                    ts_dt = datetime.fromisoformat(timestamp)
                except (ValueError, TypeError):
                    pass

            message = entry.get("message", entry.get("content", {}))
            if isinstance(message, str):
                content = message
            elif isinstance(message, dict):
                content = message.get("content", "")
            else:
                content = ""

            text_parts = []
            raw_size = len(line.encode("utf-8"))

            if isinstance(content, str):
                if content.strip():
                    text_parts.append(content.strip())
            elif isinstance(content, list):
                for item in content:
                    if not isinstance(item, dict):
                        continue
                    if item.get("type") == "text":
                        text = item.get("text", "").strip()
                        if text:
                            text_parts.append(text)

            full_text = "\n\n".join(text_parts)

            messages.append({
                "role": entry_type,
                "text": full_text,
                "raw_size": raw_size,
                "timestamp": ts_dt,
            })

    return messages


def is_system_content(text):
    """Check if text is system-injected content rather than user-typed."""
    indicators = [
        "<system-reminder>", "<command-name>", "<local-command",
        "## Chat History", "## Channel Membership", "## New Activity",
        "You may also cross-post", "If you have something valuable",
        "Do NOT prefix your response",
    ]
    return any(ind in text for ind in indicators)


def extract_user_text(text):
    """Extract actual user-typed content, stripping system injections."""
    if is_system_content(text):
        # Try to extract just the user portion before system content
        if "<system-reminder>" in text:
            parts = text.split("<system-reminder>")
            user_part = parts[0].strip()
            if user_part:
                return user_part
        return ""
    return text


def analyze_project(project_dir):
    """Analyze all conversations in a project directory."""
    project_name = project_dir.name
    conv_files = find_conversation_files(project_dir)

    if not conv_files:
        return None

    all_user_messages = []
    all_assistant_messages = []
    session_count = len(conv_files)
    total_raw_user = 0
    total_raw_assistant = 0
    timestamps = []

    for conv_file in conv_files:
        messages = parse_messages(conv_file)
        for msg in messages:
            if msg["role"] in ("user", "human"):
                total_raw_user += msg["raw_size"]
                user_text = extract_user_text(msg["text"])
                if user_text and len(user_text) < 5000:
                    all_user_messages.append({
                        "text": user_text,
                        "length": len(user_text),
                        "timestamp": msg["timestamp"],
                    })
                    if msg["timestamp"]:
                        timestamps.append(msg["timestamp"])
            elif msg["role"] == "assistant":
                total_raw_assistant += msg["raw_size"]
                if msg["text"]:
                    all_assistant_messages.append({
                        "text": msg["text"],
                        "length": len(msg["text"]),
                    })

    if not all_user_messages:
        return None

    return {
        "project_name": project_name,
        "session_count": session_count,
        "user_message_count": len(all_user_messages),
        "assistant_message_count": len(all_assistant_messages),
        "total_raw_user_bytes": total_raw_user,
        "total_raw_assistant_bytes": total_raw_assistant,
        "user_messages": all_user_messages,
        "timestamps": timestamps,
    }


def analyze_verbal_patterns(messages):
    """Analyze verbal tics, catchphrases, and language patterns."""
    texts = [m["text"].lower() for m in messages]
    all_text = " ".join(texts)

    patterns = {
        "ellipsis_usage": sum(1 for t in texts if "..." in t),
        "starts_with_ok": sum(1 for t in texts if t.startswith("ok ")),
        "starts_with_yes": sum(1 for t in texts if t.startswith("yes")),
        "starts_with_hey": sum(1 for t in texts if t.startswith("hey")),
        "starts_lowercase": sum(1 for m in messages if m["text"] and m["text"][0].islower()),
        "contains_lol": sum(1 for t in texts if "lol" in t),
        "contains_bruh": sum(1 for t in texts if "bruh" in t),
        "contains_right_question": sum(1 for t in texts if t.rstrip().endswith("right?")),
        "contains_make_it_so": sum(1 for t in texts if "make it so" in t),
        "contains_mood_misalign": sum(1 for t in texts if "mood" in t and ("misalign" in t or "aligned" in t)),
        "contains_sad_womps": sum(1 for t in texts if "sad womp" in t),
        "contains_whatevs": sum(1 for t in texts if "whatevs" in t),
        "contains_obvs": sum(1 for t in texts if "obvs" in t),
        "contains_carry_on": sum(1 for t in texts if "carry on" in t),
        "contains_thoughts": sum(1 for t in texts if t.rstrip().endswith("thoughts?")),
        "contains_emoji_shortcode": sum(1 for t in texts if re.search(r":[a-z_-]+:", t)),
        "contains_emoticon": sum(1 for t in texts if re.search(r"[:;][PpDd/\\)(]", t)),
        "uses_we": sum(1 for t in texts if re.search(r"\bwe\b", t)),
        "uses_interrupts": sum(1 for t in texts if "request interrupted" in t.lower()),
    }

    # Find potential catchphrases (2-4 word phrases that appear 3+ times)
    word_pairs = Counter()
    for t in texts:
        words = t.split()
        for i in range(len(words) - 1):
            pair = f"{words[i]} {words[i+1]}"
            if len(pair) > 5:
                word_pairs[pair] += 1

    patterns["common_phrases"] = {k: v for k, v in word_pairs.most_common(30) if v >= 3}
    patterns["total_messages"] = len(messages)

    return patterns


def analyze_message_lengths(messages):
    """Analyze message length distribution."""
    lengths = [m["length"] for m in messages]
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


def analyze_time_patterns(timestamps):
    """Analyze time-of-day and day-of-week patterns."""
    if not timestamps:
        return {}

    hours = Counter()
    days = Counter()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for ts in timestamps:
        if ts:
            hours[ts.hour] += 1
            days[day_names[ts.weekday()]] += 1

    # Find peak hours (top 5)
    peak_hours = hours.most_common(5)

    return {
        "hour_distribution": dict(sorted(hours.items())),
        "day_distribution": dict(days),
        "peak_hours_utc": peak_hours,
        "total_timestamps": len(timestamps),
    }


def analyze_greeting_patterns(messages):
    """Analyze how the user opens conversations."""
    greetings = []
    for m in messages:
        text = m["text"].strip().lower()
        if any(text.startswith(g) for g in ["hey ", "hi ", "hello ", "sup", "howdy"]):
            greetings.append(m["text"][:200])
    return greetings[:20]


def analyze_approval_disapproval(messages):
    """Find examples of approval and disapproval language."""
    approval_patterns = [
        "perfect", "brilliant", "nice", "well done", "make it so",
        "yes", "yeah", "go for it", "looks good", "i like",
        "nailed it", "exactly", "that's great",
    ]
    disapproval_patterns = [
        "still isn't", "still doesn't", "still not", "still nothing",
        "doesn't work", "isn't working", "not working",
        "don't like", "shouldn't", "why would", "why are you",
        "bruh", "ugh", "no ", "nope",
    ]

    approvals = []
    disapprovals = []

    for m in messages:
        text = m["text"].lower().strip()
        for pat in approval_patterns:
            if pat in text and len(m["text"]) < 300:
                approvals.append(m["text"][:200])
                break
        for pat in disapproval_patterns:
            if pat in text and len(m["text"]) < 300:
                disapprovals.append(m["text"][:200])
                break

    return {
        "approvals": approvals[:15],
        "disapprovals": disapprovals[:15],
    }


def analyze_instruction_style(messages):
    """Analyze how the user gives instructions."""
    questions_as_instructions = []
    direct_commands = []
    thinking_out_loud = []

    for m in messages:
        text = m["text"].strip()
        lower = text.lower()

        if len(text) > 500:
            continue

        # Questions that are really instructions
        if re.search(r"(shouldn't we|why can't we|what if we|what about|can we|should we)", lower):
            questions_as_instructions.append(text[:200])
        # Thinking out loud (ellipsis-heavy)
        elif text.count("...") >= 2 or text.count("....") >= 1:
            thinking_out_loud.append(text[:200])
        # Short direct commands
        elif len(text) < 80 and not text.endswith("?"):
            direct_commands.append(text[:200])

    return {
        "questions_as_instructions": questions_as_instructions[:10],
        "direct_commands": direct_commands[:15],
        "thinking_out_loud": thinking_out_loud[:10],
    }


def build_profile(project_analyses):
    """Build a complete profile from all project analyses."""
    all_user_messages = []
    all_timestamps = []
    project_summaries = []

    for analysis in project_analyses:
        if not analysis:
            continue
        all_user_messages.extend(analysis["user_messages"])
        all_timestamps.extend(analysis["timestamps"])

        short_name = analysis["project_name"]
        # Strip common prefix
        for prefix in ["-home-", "apotozni-sbx-"]:
            idx = short_name.find(prefix)
            if idx >= 0:
                short_name = short_name[idx + len(prefix):]

        project_summaries.append({
            "name": short_name,
            "sessions": analysis["session_count"],
            "user_messages": analysis["user_message_count"],
            "assistant_messages": analysis["assistant_message_count"],
            "raw_user_bytes": analysis["total_raw_user_bytes"],
            "raw_assistant_bytes": analysis["total_raw_assistant_bytes"],
        })

    profile = {
        "generated_at": datetime.now().isoformat(),
        "total_projects": len(project_summaries),
        "total_user_messages": len(all_user_messages),
        "total_timestamps": len(all_timestamps),
        "projects": sorted(project_summaries, key=lambda x: x["user_messages"], reverse=True),
        "verbal_patterns": analyze_verbal_patterns(all_user_messages),
        "message_lengths": analyze_message_lengths(all_user_messages),
        "time_patterns": analyze_time_patterns(all_timestamps),
        "greeting_patterns": analyze_greeting_patterns(all_user_messages),
        "approval_disapproval": analyze_approval_disapproval(all_user_messages),
        "instruction_style": analyze_instruction_style(all_user_messages),
        "sample_messages": {
            "shortest": sorted(all_user_messages, key=lambda x: x["length"])[:10],
            "longest": sorted(all_user_messages, key=lambda x: x["length"], reverse=True)[:10],
        },
    }

    # Clean timestamps from sample messages (not JSON serializable)
    for category in ["shortest", "longest"]:
        for msg in profile["sample_messages"][category]:
            if msg.get("timestamp"):
                msg["timestamp"] = msg["timestamp"].isoformat()
            else:
                msg["timestamp"] = None

    # Clean timestamps from greeting patterns and other places
    for msg in all_user_messages:
        if isinstance(msg.get("timestamp"), datetime):
            msg["timestamp"] = msg["timestamp"].isoformat()

    # Clean time_patterns timestamps
    for ts_list_key in ["timestamps"]:
        if ts_list_key in profile:
            profile[ts_list_key] = [
                t.isoformat() if isinstance(t, datetime) else t
                for t in profile[ts_list_key]
            ]

    # Remove raw message list from output (too large)
    del profile["total_timestamps"]
    if "timestamps" in profile:
        del profile["timestamps"]

    return profile


def compare_profiles(current, previous):
    """Compare current profile against a previous one and return differences."""
    diffs = {}

    # Message count changes
    prev_total = previous.get("total_user_messages", 0)
    curr_total = current.get("total_user_messages", 0)
    diffs["message_count_change"] = curr_total - prev_total

    # Project changes
    prev_projects = {p["name"] for p in previous.get("projects", [])}
    curr_projects = {p["name"] for p in current.get("projects", [])}
    diffs["new_projects"] = list(curr_projects - prev_projects)
    diffs["removed_projects"] = list(prev_projects - curr_projects)

    # Verbal pattern changes
    prev_verbal = previous.get("verbal_patterns", {})
    curr_verbal = current.get("verbal_patterns", {})
    verbal_changes = {}
    for key in set(list(prev_verbal.keys()) + list(curr_verbal.keys())):
        if key in ("common_phrases", "total_messages"):
            continue
        prev_val = prev_verbal.get(key, 0)
        curr_val = curr_verbal.get(key, 0)
        if prev_val != curr_val:
            prev_total_msgs = prev_verbal.get("total_messages", 1)
            curr_total_msgs = curr_verbal.get("total_messages", 1)
            prev_pct = (prev_val / prev_total_msgs * 100) if prev_total_msgs else 0
            curr_pct = (curr_val / curr_total_msgs * 100) if curr_total_msgs else 0
            if abs(curr_pct - prev_pct) > 1:  # Only report >1% changes
                verbal_changes[key] = {
                    "previous": f"{prev_val} ({prev_pct:.1f}%)",
                    "current": f"{curr_val} ({curr_pct:.1f}%)",
                    "direction": "up" if curr_pct > prev_pct else "down",
                }
    diffs["verbal_pattern_changes"] = verbal_changes

    # Message length changes
    prev_lengths = previous.get("message_lengths", {})
    curr_lengths = current.get("message_lengths", {})
    if prev_lengths and curr_lengths:
        diffs["message_length_changes"] = {
            "mean": {"previous": prev_lengths.get("mean"), "current": curr_lengths.get("mean")},
            "median": {"previous": prev_lengths.get("median"), "current": curr_lengths.get("median")},
        }

    # Time pattern changes
    prev_time = previous.get("time_patterns", {})
    curr_time = current.get("time_patterns", {})
    if prev_time and curr_time:
        diffs["time_pattern_changes"] = {
            "previous_peak_hours": prev_time.get("peak_hours_utc"),
            "current_peak_hours": curr_time.get("peak_hours_utc"),
        }

    return diffs


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Claude Code conversation history to build a communication profile"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Analyze all projects in ~/.claude/projects/",
    )
    group.add_argument(
        "--project",
        action="append",
        help="Specific project directory to analyze (can be repeated)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path for the profile JSON. Defaults to stdout.",
    )
    parser.add_argument(
        "--compare",
        help="Path to a previous profile JSON to compare against.",
    )
    args = parser.parse_args()

    claude_dir = find_claude_dir()

    # Determine which projects to analyze
    if args.all:
        project_dirs = find_all_projects(claude_dir)
    else:
        project_dirs = [Path(p) for p in args.project]

    if not project_dirs:
        sys.exit("Error: No projects found to analyze.")

    print(f"Analyzing {len(project_dirs)} project(s)...", file=sys.stderr)

    # Analyze each project
    analyses = []
    for project_dir in project_dirs:
        print(f"  {project_dir.name}...", file=sys.stderr)
        analysis = analyze_project(project_dir)
        if analysis:
            analyses.append(analysis)

    if not analyses:
        sys.exit("Error: No conversation data found in any project.")

    print(f"Found data in {len(analyses)} project(s).", file=sys.stderr)

    # Build profile
    profile = build_profile(analyses)

    # Compare if requested
    if args.compare:
        compare_path = Path(args.compare)
        if not compare_path.exists():
            print(f"Warning: Previous profile not found at {compare_path}, skipping comparison.", file=sys.stderr)
        else:
            with open(compare_path) as f:
                previous = json.load(f)
            profile["comparison"] = compare_profiles(profile, previous)
            print("Comparison with previous profile included.", file=sys.stderr)

    # Output
    output_json = json.dumps(profile, indent=2, default=str)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output_json)
        print(f"Profile written to {output_path}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
