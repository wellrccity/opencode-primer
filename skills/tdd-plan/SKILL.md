---
name: tdd-plan
description: Use when implementing verifiable changes - small tasks in a red-green-refactor cycle.
---

# TDD plan

1. Break the work into 3-7 small tasks, each with a file and a definition of done.
2. **Red**: write and run the smallest test that shows the failure.
3. **Green**: make the smallest change that passes that test.
4. **Refactor**: only after green; run the tests again.
5. Update the checklist and stop if a dependency or decision is unclear.

## Rules
- Aim for 2-5 minutes per step; split it if it takes longer.
- One main focus per step; do not force "one file only" when the test needs integration.
- Use the runner the project already configures; do not invent dependencies.
- For a temporary repro, use `$env:TEMP\opencode\` on PowerShell or `${TMPDIR:-/tmp}/opencode/` on POSIX; do not commit it.

## Output
Show the checklist and real commands; report how many tests passed and which remain.
