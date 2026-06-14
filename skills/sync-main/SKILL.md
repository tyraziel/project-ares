---
name: sync-main
description: Fetch origin/main and rebase the current feature branch onto it, then push.
---

# Sync Main Skill

## Steps

1. Fetch main from origin:
```bash
git fetch origin main
```

2. Rebase current branch onto it:
```bash
git rebase origin/main
```

If there are conflicts, stop and report them — do not auto-resolve.

3. Report `git log --oneline origin/main..HEAD` so the user can confirm what commits are ahead of main.

## Rules

- NEVER use `--force`
- NEVER execute `git add`
- NEVER execute `git commit`
- NEVER execute `git push`
- NEVER auto-resolve rebase conflicts — stop and report to the user
- NEVER push to main directly