---
name: session-handoff
description: Use when pausing, switching models, or reducing context - preserve state and one clear next step.
---

# Session handoff

Write `HANDOFF.md` in the project (or `$env:TEMP\opencode\handoff.md` on PowerShell, `${TMPDIR:-/tmp}/opencode/handoff.md` on POSIX) with:

```md
# Handoff - <task>
Goal: <done when...>
State: <what works / what fails, with observed output>
Decisions: <decisions and reason>
Files: <path + summary>
Next: <one literal, small action>
Verification: <command run and result>
```

## Rules
- Do not copy whole files or credentials; point to paths and lines.
- When resuming, read the handoff and confirm the real state of the project before continuing.
- Hand off early when context is getting confusing; do not assume a context percentage.
