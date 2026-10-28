# Repository guide

Portable OpenCode 2.x configuration kit. User-facing documentation is in
[README.md](README.md); install details are in [docs/INSTALL.md](docs/INSTALL.md).

## First-run setup

When an agent opens a session in this repository, it should first ask the user:

"Would you like me to install this OpenCode configuration kit now? Safe mode
skips existing files; use -Force/--force later to overwrite with a backup."

- If the user accepts, detect the OS and run the matching installer:
  - Windows: `powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1`
  - Linux or macOS: `bash scripts/install.sh`
  - Prefer a dry run first when the target already contains files.
- Never install without explicit consent.
- After installation, run `python scripts/verify.py`, then tell the user to
  restart OpenCode.
- If the user declines, continue without installing and do not repeat the
  offer in the same session.

## Rules

- English only. ASCII only: no accents, smart quotes, or em dashes.
- Never commit secrets, API keys, passwords, tokens, or private paths.
  Credentials in config use `{env:VARIABLE}` or `{file:path}` placeholders.
- A skill ID is its directory name, in lowercase kebab-case
  (`^[a-z0-9]+(-[a-z0-9]+)*$`). Frontmatter `name` matches the ID.
- Keep installers safe by default: skip existing files unless forced, back up
  before overwrite, never delete unrelated files.
- Do not change behavior and documentation in separate commits without noting
  the compatibility impact.

## Layout

```text
config/      opencode.json, provider template, CLI preferences, global AGENTS.md
agents/      reviewer, planner, team-worker, team-worker-free, team-reviewer, team-worker-paid
commands/    maestro, team-build, verify, review, plan, grill, tdd, handoff, map
skills/      18 self-contained skills, one SKILL.md per directory, optional references/
plugins/     meta-goal turn-budget plugin
scripts/     install.ps1, install.sh, verify.py
docs/        install, configuration, skills, migration
```

## Changing a skill

1. Edit `skills/<id>/SKILL.md`; keep `name` equal to `<id>` and a description
   that starts with "Use when".
2. Keep the directory limited to `SKILL.md` unless the skill genuinely needs
   supporting files.
3. Update the table in `docs/SKILLS.md` if the trigger or purpose changes.
4. Run `python scripts/verify.py`.

## Verification

```bash
python scripts/verify.py
```

The script is the release gate: layout, JSON, frontmatter, ASCII, Portuguese
leftovers, secrets, machine-specific paths, documentation cross-references,
installer contract, and plugin syntax. It must exit 0 before a commit.

Additional checks when touching installers:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -DryRun
```

```bash
bash -n scripts/install.sh
bash scripts/install.sh --dry-run
```

## Commits

Use one intent per commit and a short imperative subject, optionally with
`feat:`, `fix:`, `docs:`, `test:`, or `chore:`. Do not commit generated caches,
backups, `.env` files, or installed copies.
