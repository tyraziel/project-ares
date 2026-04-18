#!/usr/bin/env python3
"""Inspect and compare Claude Code data sources for the analyze-me skill.

Reports on what data is available, its date ranges, and how history.jsonl
compares to project JSONL files. Useful for diagnosing gaps or validating
that the analysis script is seeing everything.

Usage:
    python3 inspect_data_sources.py
    python3 inspect_data_sources.py --verbose
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


def inspect_history(verbose=False):
    """Analyze ~/.claude/history.jsonl structure and coverage."""
    history_path = Path.home() / ".claude" / "history.jsonl"
    if not history_path.exists():
        print("ERROR: ~/.claude/history.jsonl not found")
        return

    entries = []
    key_sets = set()
    projects = Counter()
    project_dates = {}
    has_session_id = 0
    no_session_id = 0
    has_pasted = 0
    empty_display = 0

    with open(history_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            entries.append(d)
            key_sets.add(tuple(sorted(d.keys())))

            display = d.get("display", "")
            project = d.get("project", "unknown")
            ts_ms = d.get("timestamp", 0)

            if not display.strip():
                empty_display += 1

            if d.get("sessionId"):
                has_session_id += 1
            else:
                no_session_id += 1

            if d.get("pastedContents"):
                has_pasted += 1

            short = Path(project).name if project else "unknown"
            projects[short] += 1

            if ts_ms:
                dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
                if short not in project_dates:
                    project_dates[short] = [dt, dt]
                else:
                    project_dates[short][0] = min(project_dates[short][0], dt)
                    project_dates[short][1] = max(project_dates[short][1], dt)

    print("=" * 60)
    print("HISTORY.JSONL ANALYSIS")
    print("=" * 60)
    print(f"  Total entries: {len(entries)}")
    print(f"  Empty display: {empty_display}")
    print(f"  With sessionId: {has_session_id}")
    print(f"  Without sessionId: {no_session_id}")
    print(f"  With pastedContents: {has_pasted}")
    print(f"  Unique key schemas: {len(key_sets)}")
    for ks in key_sets:
        print(f"    {ks}")

    if entries:
        first_ts = entries[0].get("timestamp", 0)
        last_ts = entries[-1].get("timestamp", 0)
        print(f"\n  Date range:")
        print(f"    First: {datetime.fromtimestamp(first_ts / 1000, tz=timezone.utc)}")
        print(f"    Last:  {datetime.fromtimestamp(last_ts / 1000, tz=timezone.utc)}")

    print(f"\n  Unique projects: {len(projects)}")
    print(f"\n  Projects by message count:")
    for proj, count in projects.most_common():
        dates = project_dates.get(proj, [None, None])
        date_str = ""
        if dates[0] and dates[1]:
            date_str = f" | {dates[0].strftime('%Y-%m-%d')} to {dates[1].strftime('%Y-%m-%d')}"
        print(f"    {count:>5} msgs | {proj}{date_str}")

    display_lengths = [len(e.get("display", "")) for e in entries]
    if display_lengths:
        print(f"\n  Display text lengths:")
        print(f"    Min: {min(display_lengths)}")
        print(f"    Max: {max(display_lengths)}")
        print(f"    Mean: {sum(display_lengths) // len(display_lengths)}")
        print(f"    Median: {sorted(display_lengths)[len(display_lengths) // 2]}")

    if verbose:
        print(f"\n  Sample entries (first, middle, last):")
        for idx in [0, len(entries) // 2, -1]:
            e = entries[idx]
            print(f"\n    [{idx}]:")
            print(f"      display: {e.get('display', '')[:120]}")
            print(f"      project: {e.get('project', '?')}")
            print(f"      sessionId: {e.get('sessionId', 'NONE')}")
            ts = e.get("timestamp", 0)
            print(f"      timestamp: {datetime.fromtimestamp(ts / 1000, tz=timezone.utc)}")


def inspect_project_jsonl(verbose=False):
    """Analyze ~/.claude/projects/ JSONL files."""
    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.exists():
        print("\nERROR: ~/.claude/projects/ not found")
        return

    print("\n" + "=" * 60)
    print("PROJECT JSONL FILES ANALYSIS")
    print("=" * 60)

    total_root = 0
    total_subagent = 0
    project_stats = {}

    for project_dir in sorted(projects_dir.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("."):
            continue

        root_files = list(project_dir.glob("*.jsonl"))
        subagent_files = list(project_dir.rglob("subagents/**/*.jsonl"))

        root_count = len(root_files)
        sub_count = len(subagent_files)
        total_root += root_count
        total_subagent += sub_count

        user_msgs = 0
        assistant_msgs = 0
        interrupts = 0
        earliest = None
        latest = None

        for jf in root_files:
            try:
                with open(jf) as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            etype = entry.get("type", entry.get("role", ""))
                            ts = entry.get("timestamp", "")

                            if ts and isinstance(ts, str):
                                try:
                                    dt = datetime.fromisoformat(ts)
                                    if earliest is None or dt < earliest:
                                        earliest = dt
                                    if latest is None or dt > latest:
                                        latest = dt
                                except ValueError:
                                    pass

                            if etype == "user":
                                user_msgs += 1
                                msg = entry.get("message", entry.get("content", ""))
                                content = msg if isinstance(msg, str) else str(msg.get("content", "")) if isinstance(msg, dict) else ""
                                if "[Request interrupted" in content:
                                    interrupts += 1
                            elif etype == "assistant":
                                assistant_msgs += 1
                        except json.JSONDecodeError:
                            continue
            except (PermissionError, OSError):
                continue

        project_stats[project_dir.name] = {
            "root_files": root_count,
            "subagent_files": sub_count,
            "user_messages": user_msgs,
            "assistant_messages": assistant_msgs,
            "interrupts": interrupts,
            "earliest": earliest,
            "latest": latest,
        }

    print(f"  Total root-level JSONL: {total_root}")
    print(f"  Total subagent JSONL: {total_subagent}")
    print(f"  Total projects with data: {len(project_stats)}")

    print(f"\n  Per-project breakdown:")
    for name, stats in sorted(project_stats.items(), key=lambda x: -x[1]["user_messages"]):
        date_str = ""
        if stats["earliest"] and stats["latest"]:
            date_str = f" | {stats['earliest'].strftime('%Y-%m-%d')} to {stats['latest'].strftime('%Y-%m-%d')}"
        int_str = f" | {stats['interrupts']} interrupts" if stats["interrupts"] else ""
        print(
            f"    {stats['user_messages']:>5} user / {stats['assistant_messages']:>5} asst "
            f"| {stats['root_files']} files{date_str}{int_str} | {name}"
        )


def compare_sources():
    """Compare history.jsonl coverage vs project JSONL coverage."""
    print("\n" + "=" * 60)
    print("COVERAGE COMPARISON")
    print("=" * 60)

    history_path = Path.home() / ".claude" / "history.jsonl"
    projects_dir = Path.home() / ".claude" / "projects"

    hist_projects = Counter()
    if history_path.exists():
        with open(history_path) as f:
            for line in f:
                try:
                    d = json.loads(line)
                    p = d.get("project", "")
                    hist_projects[Path(p).name] += 1
                except (json.JSONDecodeError, TypeError):
                    continue

    jsonl_projects = Counter()
    if projects_dir.exists():
        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue
            for jf in project_dir.glob("*.jsonl"):
                try:
                    with open(jf) as f:
                        for line in f:
                            try:
                                entry = json.loads(line)
                                if entry.get("type") == "user" or entry.get("role") == "user":
                                    short = project_dir.name
                                    for prefix in ["-home-", "apotozni-sbx-"]:
                                        idx = short.find(prefix)
                                        if idx >= 0:
                                            short = short[idx + len(prefix):]
                                    jsonl_projects[short] += 1
                            except json.JSONDecodeError:
                                continue
                except (PermissionError, OSError):
                    continue

    all_projects = sorted(set(list(hist_projects.keys()) + list(jsonl_projects.keys())))

    print(f"  {'Project':<40} {'history.jsonl':>15} {'project JSONL':>15} {'Delta':>10}")
    print(f"  {'-' * 40} {'-' * 15} {'-' * 15} {'-' * 10}")
    for proj in all_projects:
        h = hist_projects.get(proj, 0)
        j = jsonl_projects.get(proj, 0)
        delta = h - j
        delta_str = f"+{delta}" if delta > 0 else str(delta) if delta < 0 else "="
        print(f"  {proj:<40} {h:>15} {j:>15} {delta_str:>10}")

    print(f"\n  {'TOTAL':<40} {sum(hist_projects.values()):>15} {sum(jsonl_projects.values()):>15}")


def main():
    parser = argparse.ArgumentParser(description="Inspect Claude Code data sources")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show sample entries")
    args = parser.parse_args()

    inspect_history(verbose=args.verbose)
    inspect_project_jsonl(verbose=args.verbose)
    compare_sources()


if __name__ == "__main__":
    main()
