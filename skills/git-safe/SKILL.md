---
name: git-safe
description: Use when preparing commits, branches, or pushes; preserve existing work and review the diff before acting.
---

# Git safe

## Before commit
- Run `git status --short` and `git diff --stat` separately.
- Read the relevant diff; check untracked and staged files.
- Look for credentials locally when appropriate; do not print secret values in the conversation.

## Standards
- One intention per commit; short descriptive message (`feat:`, `fix:`, `test:`, `docs:`, `chore:`).
- Do not create a branch, commit, or push unless that is in the requested scope.
- If the diff is large, propose a split before reorganizing.

## Required confirmation
Do not run without explicit confirmation: `git push --force`, `git reset --hard`, `git clean -fd`, or destructive recursive removal.

## Recovery
Before any recovery action, inspect `git status`, `git reflog -n 10`, and `git stash list`. Never discard pre-existing changes.
