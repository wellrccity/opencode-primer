---
name: systematic-debugging
description: Use when an error or unexpected behavior appears; reproduce it, isolate the cause, and validate that the fix does not regress.
---

# Systematic debugging

## One experiment at a time
1. **Reproduce**: keep the command, the input, and the full error. For a temporary repro in PowerShell use `$env:TEMP\opencode\repro.*`; in a POSIX shell use `${TMPDIR:-/tmp}/opencode/`.
2. **Locate**: search the message or stack and read the few relevant files. Form one hypothesis at a time.
3. **Isolate**: confirm the hypothesis with a test, a log, or a minimal call.
4. **Fix**: change one cause at a time; do not mix in refactors.
5. **Regress**: rerun the reproduction and the relevant tests.

## Rules
- Each attempt records the hypothesis, the command, and the observed result.
- Do not make three random changes to "see if it passes".
- Adapt commands to the shell. In PowerShell use `Select-String` and `Get-Content -Tail`; in POSIX use `grep` and `tail`.
- Do not paste secrets or full logs into the chat.

## Output
- Cause: one sentence with file and line when confirmed.
- Fix and verification command with the real result.
- If not confirmed: state explicitly what is still missing.
