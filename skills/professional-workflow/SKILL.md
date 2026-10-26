---
name: professional-workflow
description: Use when doing a code task; understand the change, plan micro-steps, make the smallest diff, and verify by running commands.
---

# Professional workflow

## Workflow
1. **Understand**: use `glob`, `grep`, and `read` on the relevant files. Note current and expected behavior.
2. **Plan**: for a multi-step change, list 3 to 7 verifiable steps.
3. **Implement**: read before editing; make the smallest useful diff.
4. **Verify**: load the `mandatory-verification` skill and run real commands.
5. **Review**: inspect the diff and the tests; use the `code-review` skill when risk or a relevant diff exists.
6. **Summary**: Changed / Verified / Missing / Next step.

## Rules
- Do not invent URLs or APIs; confirm them in an official source or in the repository.
- After editing, reread the section and check the diff.
- If two attempts fail, reduce the scope and explain the blocker before trying something else.
