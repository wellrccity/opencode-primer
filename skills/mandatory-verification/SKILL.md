---
name: mandatory-verification
description: Use after editing - run the most relevant check and report real output; never claim success by inspection.
---

# Mandatory verification

## Checklist
- [ ] If this is a Git repository, run `git status --short` and `git diff --stat`.
- [ ] Run the relevant test/lint/build the project already provides.
- [ ] Python: use the project interpreter (`py -m py_compile file.py` or `python -m py_compile file.py`).
- [ ] JavaScript: `node --check file.js`; TypeScript: use the existing script/tsconfig.
- [ ] Reread the edited section and confirm the diff.

## Windows/output
- On PowerShell, cap logs with `Select-Object -First 100` or `Get-Content -Tail 80`; on POSIX use the available equivalent.
- If a command does not exist, say so; do not pretend it ran.
- If there are no tests, create a small reproduction in `$env:TEMP\opencode\` (PowerShell) or `${TMPDIR:-/tmp}/opencode/` (POSIX) and do not commit it.

## Report
Command run plus observed result. If you did not verify, say why and which command is missing.

End with: Changed / Verified / Missing / Next step.
