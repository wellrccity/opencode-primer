# Contributing

## Ground rules

- English only, ASCII only. No accents, smart quotes, or em dashes.
- No secrets, keys, tokens, or personal absolute paths in any commit.
- Every skill ID is lowercase kebab-case and matches its directory name.
- Keep install assets working on Windows PowerShell and POSIX shell.

## Repository map

| Area | Owner paths |
| --- | --- |
| Config, agents, commands | `config/`, `agents/`, `commands/` |
| Skills | `skills/<id>/SKILL.md` |
| Plugin | `plugins/meta-goal/` |
| Installers, hygiene | `scripts/`, `.gitignore`, `.editorconfig`, `.gitattributes` |
| Docs, CI | `README.md`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/`, `.github/` |

Change only the paths for the task you are doing, and leave unrelated files alone.

## Authoring a skill

1. Create `skills/<id>/SKILL.md`; the directory contains that file and nothing else.
2. Frontmatter:

```markdown
---
name: <id>
description: Use when ...
---
```

3. `name` equals the directory and matches `^[a-z0-9]+(-[a-z0-9]+)*$`.
4. `description` starts with "Use when", stays between 20 and 400 characters, and states the trigger, not the procedure.
5. Keep the body short: ordered steps, concrete commands, and a stop condition. No filler.
6. Use cross-platform temporary paths: `$env:TEMP\opencode\` and `${TMPDIR:-/tmp}/opencode/`.
7. Reference other skills by their English ID.

## Authoring a command

Each `commands/*.md` needs frontmatter with `description`, then a short English prompt body. Use `$ARGUMENTS` when the command takes input. Set `agent: reviewer` for `/review` and `agent: planner` for `/plan`.

## Authoring an agent

Each `agents/*.md` needs frontmatter with `description`, `mode`, and `steps`. Read-only agents deny `edit` and `write`; `reviewer` permits only `git status` and `git diff` in shell. Keep `disabled: true` on paid or optional agents.

## Authoring docs

`README.md` keeps the section set defined in `AGENTS.md`. Long procedures belong in `docs/`. Do not duplicate the skill table between `README.md` and `docs/SKILLS.md` beyond one-line summaries.

## Verification

```bash
python scripts/verify.py
```

Run it before every commit and paste the real output. It checks required paths, JSON parsing, skill and agent frontmatter, ASCII text, secrets, and absolute user paths. It exits non-zero if any check fails and prints one `PASS`/`FAIL` line per check.

Additional local checks:

```bash
node --check plugins/meta-goal/index.js
bash -n scripts/install.sh
```

## Pull requests

- One topic per pull request, with the verification output in the description.
- State what changed, what you ran, and what remains unverified.
- Do not reformat unrelated files.
