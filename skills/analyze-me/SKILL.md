---
name: analyze-me
description: Analyze Claude Code conversation history to build a communication profile of the user. Identifies tone, verbal patterns, instruction style, time-of-day habits, project breakdown, and how the user's approach has evolved over time.
allowed-tools: Bash, Read, Write, Glob, Grep, Agent, AskUserQuestion
argument-hint: "[--all | --project <path>] [--compare <previous-profile.json>] [-o <output.json>]"
---

# Analyze Me

Build a communication profile of the user by analyzing their Claude Code conversation history across projects.

## What This Skill Does

1. Parses all JSONL conversation files in `~/.claude/projects/`
2. Extracts user messages, filtering out system-injected content
3. Analyzes verbal patterns, message lengths, time-of-day habits, instruction style, greeting patterns, and approval/disapproval language
4. Generates a structured JSON profile with raw statistics
5. Optionally compares against a previous profile to detect changes
6. Claude then synthesizes the raw data into a narrative profile document

## Instructions

### Step 1: Determine scope

Check if the user provided arguments: $ARGUMENTS

- `--all` → analyze every project in `~/.claude/projects/`
- `--project <path>` → analyze specific project(s) only (can be repeated)
- If no arguments, ask the user what they'd like to analyze

### Step 2: Run the analysis script

The script is located at `scripts/analyze_conversations.py` relative to this skill's directory.

```bash
# Analyze all projects
python3 <skill-dir>/scripts/analyze_conversations.py --all -o <output-path>.json

# Analyze specific project(s)
python3 <skill-dir>/scripts/analyze_conversations.py --project <path1> --project <path2> -o <output-path>.json

# Compare against a previous profile
python3 <skill-dir>/scripts/analyze_conversations.py --all --compare <previous-profile.json> -o <output-path>.json
```

The default output path should be `analyze-me-profile-<date>.json` in the current working directory.

The script uses only Python standard library modules (no external dependencies).

### Step 3: Read and synthesize the profile

After the script runs, read the generated JSON profile. Synthesize the raw data into a **narrative analysis** covering:

#### Core Profile
- **Greeting style** — how do they open conversations?
- **Verbal fingerprint** — catchphrases, verbal tics, distinctive language patterns. Quote specific examples.
- **Thinking style** — do they think out loud? Use questions as directions? Use "we" vs "you"?
- **Message length patterns** — terse vs verbose? Bimodal? When do they expand?
- **Instruction style** — do they give detailed specs, ask Socratic questions, or fire terse directives?
- **Approval/disapproval** — how do they express satisfaction or dissatisfaction?
- **Leadership style** — do they lead, collaborate, or defer? How do they handle Claude's autonomy?
- **Time-of-day patterns** — when do they work? Any night owl / early bird patterns? Weekend activity?
- **Emotional patterns** — humor, frustration, excitement, anxiety? How do they process each?
- **Project breakdown** — what do they work on? Where do they spend the most time?

#### If comparing against a previous profile
- What shifted in tone, verbal patterns, or instruction style?
- Are they more or less open/collaborative/directive?
- Any new catchphrases or abandoned ones?
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

The analysis script (`scripts/analyze_conversations.py`) is structured as follows:

### Key functions

- **`find_all_projects()`** — discovers all project directories under `~/.claude/projects/`
- **`find_conversation_files()`** — finds JSONL files in a project dir (excludes subagent logs)
- **`parse_messages()`** — reads JSONL line by line, handles both `type` field format and `role` field format
- **`extract_user_text()`** — strips system-injected content (system reminders, chat history context, command outputs) to isolate actual user-typed text
- **`analyze_verbal_patterns()`** — counts occurrences of known catchphrases, ellipsis usage, greeting styles, emoticons, etc.
- **`analyze_message_lengths()`** — computes min/max/mean/median and distribution buckets
- **`analyze_time_patterns()`** — extracts hour-of-day and day-of-week distributions from timestamps
- **`analyze_greeting_patterns()`** — finds conversation openers
- **`analyze_approval_disapproval()`** — categorizes messages as approval or disapproval with examples
- **`analyze_instruction_style()`** — classifies messages as Socratic questions, direct commands, or thinking-out-loud
- **`build_profile()`** — aggregates all analyses into a single JSON profile
- **`compare_profiles()`** — diffs two profiles, reporting changes in verbal patterns, message lengths, time patterns, and project activity

### JSONL format notes

Conversation files use two different schemas depending on age:

| Format | Identifying field | User messages | Content location |
|--------|------------------|---------------|-----------------|
| Newer | `type: "user"` | `type == "user"` | `message.content` (string or list of blocks) |
| Older | `role: "user"` | `role == "user"` | `content` (string or list of blocks) |

The script handles both formats transparently.

### Extending the analysis

To add new verbal pattern detection:
1. Add a counter in `analyze_verbal_patterns()`
2. The SKILL.md instructions will automatically pick it up in synthesis

To add new analysis dimensions:
1. Add a new `analyze_*()` function
2. Call it from `build_profile()`
3. Add synthesis instructions to the SKILL.md "Core Profile" section
