#!/usr/bin/env python3
import json
import sys
import os

# Read JSON from stdin
data = json.load(sys.stdin)

# Extract values
model = data['model']['display_name']
session_id = data.get('session_id', 'unknown')
ctx_pct = data.get('context_window', {}).get('used_percentage', 0) or 0
ctx_pct = int(ctx_pct)
current_dir = os.path.basename(data['workspace']['current_dir'])
current_user = os.getlogin()

total_input_tokens=0
total_output_tokens=0
transcript_lines = 0

# Check for git branch
git_branch = ""
if os.path.exists('.git'):
    try:
        with open('.git/HEAD', 'r') as f:
            ref = f.read().strip()
            if ref.startswith('ref: refs/heads/'):
                git_branch = f"{ref.replace('ref: refs/heads/', '')}"
                if git_branch == "main" or git_branch == "devel":
                    git_branch = f"| 🌿 \033[1;31m{git_branch}\033[0m"
                else:
                    git_branch = f"| ⚗️ \033[1;94m{git_branch}\033[0m"
    except:
        pass

transcript_path=data['transcript_path']

try:
    with open(f'{transcript_path}', 'r') as f:
        for line in f:
            transcript_lines = transcript_lines + 1
            transcript_line = json.loads(line)
            if 'message' in transcript_line and 'usage' in transcript_line['message']:
                if 'input_tokens' in transcript_line['message']['usage']:
                    total_input_tokens += transcript_line['message']['usage']['input_tokens']
                if 'output_tokens' in transcript_line['message']['usage']:
                    total_output_tokens += transcript_line['message']['usage']['output_tokens']
except Exception as e: 
    #print(f'ERROR: {e}')
    total_input_tokens = 0
    total_output_tokens = 0
    pass

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BRIGHT_BLUE = "\033[94m"
BOLD_BRIGHT_RED = "\033[1;91m"

# Context % heat ramp
if ctx_pct >= 90:
    CTX_COLOR = BOLD_BRIGHT_RED
elif ctx_pct >= 76:
    CTX_COLOR = RED
elif ctx_pct >= 51:
    CTX_COLOR = YELLOW
elif ctx_pct >= 26:
    CTX_COLOR = GREEN
elif ctx_pct >= 11:
    CTX_COLOR = CYAN
else:
    CTX_COLOR = BRIGHT_BLUE

# Context bar graph
BAR_WIDTH = 10
filled = round(ctx_pct / 100 * BAR_WIDTH)
empty = BAR_WIDTH - filled
ctx_bar = "█" * filled + "░" * empty

print(f"[{CTX_COLOR}{ctx_bar} {ctx_pct}%{RESET}] | 📁 {BOLD}{current_user}@{current_dir}{RESET} {git_branch} ## [🤖 \033[1;36m{model}{RESET}{DIM}@{RESET}{CYAN}{session_id}{RESET}] {DIM}TL:{transcript_lines} // I:{total_input_tokens} // O:{total_output_tokens} // T:{total_input_tokens+total_output_tokens}{RESET}")
