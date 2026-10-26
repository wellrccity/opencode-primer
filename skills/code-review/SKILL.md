---
name: code-review
description: Use when reviewing a diff before merging - find defects, security risks, regressions, and missing tests without editing.
---

# Code review (read-only)

## Process
1. Check the state and size of the diff; read the relevant context in the files.
2. Check logic, boundaries, error handling, security, and compatibility with existing APIs.
3. Confirm the tests cover the new behavior and the edge cases.
4. Do not edit files or turn style suggestions into blockers.

## Output
- At most 10 findings, ordered: `[BLOCKER]`, `[WARNING]`, `[SUGGESTION]`.
- Format: `path:line - confirmed problem - impact - suggested fix`.
- Separate facts from hypotheses. If something was not read or tested, say so.
- If there are no findings, state the scope reviewed and the limits of the review.
