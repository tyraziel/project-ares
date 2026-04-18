---
name: analyze-me
description: Analyze Claude Code conversation history to build a communication profile of the user. Identifies tone, verbal patterns, instruction style, time-of-day habits, project breakdown, and how the user's approach has evolved over time.
allowed-tools: Bash, Read, Write, Glob, Grep, Agent, AskUserQuestion
argument-hint: "[--all | --project <path>] [--exclude <path>] [--compare <previous-profile.json>] [-o <output.json>]"
---

# Analyze Me

Build a communication profile of the user by analyzing their Claude Code conversation history across projects.

## What This Skill Does

1. Reads user input history from `~/.claude/history.jsonl` (the complete record of all user messages since Claude Code was installed)
2. Filters out system-injected content, slash commands, and context-continuation summaries
3. Dynamically discovers verbal patterns, catchphrases, and language fingerprints via n-gram analysis
4. Analyzes message lengths, time-of-day habits, instruction style, greeting patterns, and approval/disapproval language
5. Supplements with interrupt counts from project JSONL files (where available)
6. Generates a structured JSON profile with raw statistics
7. Optionally compares against a previous profile to detect changes
8. Claude then synthesizes the raw data into a narrative profile document

## Data Sources

### Primary: `~/.claude/history.jsonl`
Every message the user typed into Claude Code, ever. Each line contains:
- `display` — the user's input text
- `pastedContents` — any pasted content (not expanded into analysis to avoid noise)
- `timestamp` — millisecond epoch timestamp
- `project` — full path to the project directory
- `sessionId` — UUID of the session (newer entries only)

### Supplemental: `~/.claude/projects/*/*.jsonl`
Full conversation files (both user and assistant messages, tool calls, etc.) but only retain recent data — older conversations are purged/rotated. Used for:
- Interrupt counts (`[Request interrupted by user]` markers)
- Not used for primary analysis since coverage is incomplete

### Diagnostic: `scripts/inspect_data_sources.py`
A utility script that reports on available data, date ranges, and compares history.jsonl coverage against project JSONL files. Run this to diagnose gaps or validate data availability:
```bash
python3 <skill-dir>/scripts/inspect_data_sources.py
python3 <skill-dir>/scripts/inspect_data_sources.py --verbose
```

## Instructions

### Step 1: Determine scope

Check if the user provided arguments: $ARGUMENTS

- `--all` → analyze all messages in `~/.claude/history.jsonl`
- `--project <substring>` → filter to projects matching this substring (can be repeated)
- `--exclude <substring>` → exclude projects matching this substring (can be repeated)
- If no arguments, ask the user what they'd like to analyze
- Check for previous profiles in the working directory and offer `--compare`

### Step 2: Run the analysis script

The script is located at `scripts/analyze_conversations.py` relative to this skill's directory.

```bash
# Analyze all projects
python3 <skill-dir>/scripts/analyze_conversations.py --all -o <output-path>.json

# Exclude noisy projects (e.g., multi-agent simulators with bot logs)
python3 <skill-dir>/scripts/analyze_conversations.py --all --exclude company-simulator -o <output-path>.json

# Analyze specific project(s) by substring match
python3 <skill-dir>/scripts/analyze_conversations.py --project awx-tui --project handbook -o <output-path>.json

# Compare against a previous profile
python3 <skill-dir>/scripts/analyze_conversations.py --all --compare <previous-profile.json> -o <output-path>.json
```

The default output path should be `analyze-me-profile-<date>.json` in the current working directory.

The script uses only Python standard library modules (no external dependencies).

### Step 3: Read and synthesize the profile

After the script runs, read the generated JSON profile. Synthesize the raw data into a **narrative analysis** covering:

#### Core Profile
- **Greeting style** — how do they open conversations? Use both `greeting_messages` and `session_openers` data.
- **Verbal fingerprint** — use the dynamically discovered n-grams (top_words, top_bigrams, top_trigrams, opening patterns, ending patterns) to identify distinctive language. Quote specific examples from the data.
- **Thinking style** — we/I ratio, ellipsis usage, questions-as-instructions. Do they think out loud?
- **Message length patterns** — distribution analysis, when do they expand vs stay terse?
- **Instruction style** — direct commands vs Socratic steering vs thinking-out-loud. Use examples from the instruction_style data.
- **Approval/disapproval** — how do they express satisfaction or dissatisfaction? Quote examples.
- **Leadership style** — do they lead, collaborate, or defer? Use we/I ratio, interrupt frequency, instruction style as evidence.
- **Time-of-day patterns** — provide a FULL 24-hour breakdown table, not just peak hours. Convert UTC to the user's local timezone if known. Include day-of-week and monthly trends.
- **Emotional patterns** — humor, frustration, excitement, anxiety. How do they process each?
- **Project breakdown** — what do they work on? Include date ranges and the narrative arc of how their focus has shifted over time.

#### If comparing against a previous profile
- What shifted in tone, verbal patterns, or instruction style?
- Are they more or less open/collaborative/directive?
- Any new phrases or abandoned ones? (use `new_phrases` and `dropped_phrases` from comparison)
- Has their relationship with Claude changed?

### Step 4: Present results and save

1. Present the narrative analysis to the user
2. Ask if they'd like to save the narrative as a markdown profile alongside the JSON data
3. If yes, write it to `analyze-me-narrative-<date>.md` in the current working directory
4. Remind them that the JSON profile at `analyze-me-profile-<date>.json` can be used for future `--compare` runs

### Step 5: Ask about character sheet

After presenting the profile, ask:

> "Want me to generate an NRSP-format character sheet from this profile?"

If yes, generate both a `.CS.md` (public character sheet) and `.NPC.md` (GM notes) based on the analysis.

#### NRSP Format Reference

NRSP (Narrative RPG Save Point Format) is a markdown-based system for capturing tabletop RPG narrative state. The full spec and README are bundled with this skill at `nrsp-spec/` relative to this skill's directory. The upstream repo is at: https://github.com/tyraziel/narrative-rpg-save-point-format/

**Bundled spec files:**
- `nrsp-spec/README.md` — Overview, philosophy, and file type reference
- `nrsp-spec/001_...NRSP.md` — Save Point format (narrative arc state)
- `nrsp-spec/002_...SLD.md` — Session Log Document format
- `nrsp-spec/003_...CS.md` — **Character Sheet format** (primary reference for this skill)
- `nrsp-spec/004_...LS.md` — Location Sheet format
- `nrsp-spec/005_...NPC.md` — **NPC Sheet format** (primary reference for this skill)
- `nrsp-spec/006_...LGM.md` — Game Master Location format

**Read the CS and NPC specs before generating character sheets.** The key points:

- **`.CS.md`** — Public/observable details. Required YAML: `Name`. Suggested sections: Backstory, Information, Motivations, Current State, Relationships, Stats, Inventory/Equipment, Combat Details.
- **`.NPC.md`** — GM-only extended context. Required YAML: `Name`. Suggested sections: Secret Motives, Secret Inventory, Secret Relationships. Should not duplicate the public CS unless clarity requires it.

Both files use flexible formatting (prose, bullets, tables). Translate the user's real-world traits, patterns, and behaviors into RPG-flavored descriptions. The character sheet should feel like a playable NPC — stats, abilities, weaknesses — grounded in the actual data from the analysis.

## Script Architecture

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/analyze_conversations.py` | Main analysis script — reads history.jsonl, builds profile JSON |
| `scripts/inspect_data_sources.py` | Diagnostic utility — reports on available data, date ranges, coverage gaps |

### analyze_conversations.py — Key Functions

**Data Loading:**
- **`load_history()`** — reads `~/.claude/history.jsonl`, applies project/exclude filters, strips system content and slash commands, handles paste markers
- **`extract_project_name()`** — extracts readable short name from full project path
- **`detect_sessions()`** — groups messages into sessions using `sessionId` (newer entries) or time-gap heuristic (>30 min gap = new session for older entries)
- **`count_interrupts_from_project_jsonl()`** — supplemental scan of project JSONL files for `[Request interrupted by user]` markers

**Analysis:**
- **`tokenize()`** — shared tokenizer: lowercase, strip URLs/paths/punctuation, filter single chars and numbers
- **`discover_phrases()`** — dynamic n-gram analysis: top words (minus stop words), bigrams, trigrams, ending patterns, opening words/bigrams/trigrams
- **`analyze_verbal_patterns()`** — general detectors (ellipsis, emoticons, we/I ratio, opener patterns) plus dynamic phrase discovery
- **`analyze_message_lengths()`** — min/max/mean/median and distribution buckets
- **`analyze_time_patterns()`** — hour-of-day, day-of-week, and month-by-month distributions
- **`analyze_greeting_patterns()`** — greeting messages plus session-first-message openers
- **`analyze_approval_disapproval()`** — categorizes messages as approval or disapproval with examples
- **`analyze_instruction_style()`** — classifies as Socratic questions, direct commands, or thinking-out-loud

**Profile Building:**
- **`build_profile()`** — aggregates all analyses, adds project summaries with date ranges, includes interrupt data
- **`compare_profiles()`** — diffs two profiles: message counts, new/dropped projects, verbal pattern changes, new/dropped phrases, time pattern shifts

### history.jsonl Format

Each line is a JSON object representing one user input:

| Field | Type | Description |
|-------|------|-------------|
| `display` | string | The user's input text |
| `pastedContents` | object | Clipboard content pasted in (keys are paste IDs) |
| `timestamp` | number | Millisecond epoch timestamp |
| `project` | string | Full path to the project directory |
| `sessionId` | string? | Session UUID (only present in newer entries) |

### Message Filtering

The script filters out:
- Empty or whitespace-only `display` values
- System-injected content (`<system-reminder>`, `<command-name>`, `<local-command`)
- Context continuation summaries (`"This session is being continued..."`)
- Skill SKILL.md injections (`"Base directory for this skill:"`)
- CLI slash commands (`/exit`, `/compact`, `/model`, etc.) — but NOT paths starting with `/home/`
- `[Pasted text #N +M lines]` markers are stripped from display text before analysis

### Extending the Analysis

To add new general pattern detectors:
1. Add a counter in the `general` dict within `analyze_verbal_patterns()`
2. The SKILL.md instructions will automatically pick it up in synthesis

To add new analysis dimensions:
1. Add a new `analyze_*()` function
2. Call it from `build_profile()`
3. Add synthesis instructions to the "Core Profile" section above

To add new phrase discovery:
1. Add a new counter in `discover_phrases()`
2. Return it in the phrases dict
3. It will automatically appear in the profile JSON
