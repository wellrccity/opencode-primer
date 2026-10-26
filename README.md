# opencode-primer

Portable OpenCode 2.x configuration kit: core config, agents, commands, 16 skills, and the meta-goal plugin. Installs on Windows, Linux, and macOS.

## What's inside

| Path | Contents |
| --- | --- |
| `config/` | Core `opencode.json`, an optional provider template, CLI preferences, and the global `AGENTS.md`. |
| `agents/` | Six agent definitions: `reviewer`, `planner`, and four `team-*` agents. |
| `commands/` | Eight command templates, including `team-build`, `verify`, `review`, `plan`, `grill`, `tdd`, `handoff`, `map`. |
| `skills/` | 16 skills, one directory each, each with a single `SKILL.md`. |
| `plugins/meta-goal/` | Turn-budget plugin with an automatic judge. |
| `scripts/` | `install.ps1`, `install.sh`, and `verify.py`. |
| `docs/` | Install, configuration, skills, and migration notes. |

## Requirements

- OpenCode 2.x.
- Windows PowerShell 5.1+ (or PowerShell 7+) or bash 4+ on Linux and macOS.
- Python 3.9+ for the verification script.
- Git, for cloning the repository.
- Node.js, optional; used for `node --check` when present.

## Quick start

Both installers copy files into `$env:OPENCODE_CONFIG_DIR` when it is set, otherwise into `$HOME/.config/opencode`. Existing files are skipped by default. Pass `-Force` / `--force` to overwrite after the whole target directory is backed up.

**PowerShell** (Windows):

```powershell
git clone https://github.com/wellrccity/opencode-primer.git
cd opencode-primer
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

**bash** (Linux, macOS, WSL):

```bash
git clone https://github.com/wellrccity/opencode-primer.git
cd opencode-primer
bash scripts/install.sh --dry-run
bash scripts/install.sh
```

**Manual copy** - create the target directory and copy each item, keeping the mapping:

| Source | Destination under the config directory |
| --- | --- |
| `config/opencode.json` | `opencode.json` |
| `config/cli.json` | `cli.json` |
| `config/AGENTS.md` | `AGENTS.md` |
| `agents/*` | `agents/` |
| `commands/*` | `commands/` |
| `skills/*` | `skills/` |
| `plugins/meta-goal` | `plugins/meta-goal` |

Merging is safe: no installer deletes unrelated files. Restart OpenCode after installing. Details in [docs/INSTALL.md](docs/INSTALL.md).

## Repository layout

```text
AGENTS.md  README.md  LICENSE  CONTRIBUTING.md  SECURITY.md
.gitignore  .editorconfig  .gitattributes
.github/workflows/verify.yml
config/opencode.json  config/opencode.example.json  config/cli.json  config/AGENTS.md
agents/reviewer.md  agents/planner.md  agents/team-worker.md
agents/team-worker-free.md  agents/team-reviewer.md  agents/team-worker-paid.md
commands/team-build.md  commands/verify.md  commands/review.md  commands/plan.md
commands/grill.md  commands/tdd.md  commands/handoff.md  commands/map.md
skills/<id>/SKILL.md
plugins/meta-goal/index.js  plugins/meta-goal/package.json
scripts/install.ps1  scripts/install.sh  scripts/verify.py
docs/INSTALL.md  docs/CONFIGURATION.md  docs/SKILLS.md  docs/MIGRATION.md
```

## Skills

| Skill | Purpose |
| --- | --- |
| `anti-slop-docs` | Write docs, commits, and changelogs without AI filler. |
| `brainstorm-grill` | Close a short spec before implementing an ambiguous feature. |
| `browser-control` | Drive a real Chrome tab through the browser bridge tools. |
| `caveman-mode` | Cut narration and token use on request. |
| `code-review` | Read-only diff review with severity labels. |
| `create-skill` | Turn a recurring workflow into a small skill. |
| `execution-focus` | Regain traction when scope is large or a task stalls. |
| `git-safe` | Inspect and protect work before commit, branch, or push. |
| `mandatory-verification` | Run real verification after an edit and report output. |
| `meta-goal` | Bound a long task by a measurable done condition and a turn budget. |
| `professional-workflow` | Understand, plan micro-steps, smallest diff, verify. |
| `session-handoff` | Preserve state when pausing or switching models. |
| `systematic-debugging` | Reproduce, isolate, fix, and confirm a regression test. |
| `tdd-plan` | Small red-green-refactor tasks for verifiable changes. |
| `understand-code` | Map an unfamiliar codebase without burning context. |
| `web-research` | Check current external docs against primary sources. |

Full table with triggers: [docs/SKILLS.md](docs/SKILLS.md).

## Agents

| Agent | Mode | Role |
| --- | --- | --- |
| `reviewer` | subagent | Read-only review; denies edit and write, allows only `git status` and `git diff`. |
| `planner` | subagent | Produces 3-7 verifiable micro-steps without editing files. |
| `team-worker` | subagent | Implements one precise task; inherits the orchestrator model. |
| `team-worker-free` | subagent | Same role, pinned to a free model. |
| `team-reviewer` | subagent | Reviews recent changes, read-only, pinned to a free model. |
| `team-worker-paid` | subagent | Paid-model worker; disabled by default. |

Free-tier and paid model IDs pinned in `agents/*.md` depend on the account; if a pinned model is unavailable, change the `model` field.

## Commands

| Command | Purpose |
| --- | --- |
| `/team-build` | Orchestrate workers across a multi-part build. |
| `/verify` | Run the relevant checks and report the result. |
| `/review` | Review a diff or the working tree with the `reviewer` agent. |
| `/plan` | Produce micro-steps with the `planner` agent. |
| `/grill` | Interrogate a proposal before implementation. |
| `/tdd` | Plan red-green-refactor tasks. |
| `/handoff` | Write a handoff note with state and next step. |
| `/map` | Produce a lean map of a codebase. |

Commands accept `$ARGUMENTS` where the template uses it.

## Configuration

`config/opencode.json` holds core settings only: `$schema`, formatter, tool output limits, compaction, watcher ignores, and an ordered `permissions` array with conservative denies. It contains no providers, MCP servers, plugin paths, or secrets.

`config/opencode.example.json` is an optional template with two OpenAI-compatible providers and two MCP servers, `chrome` and `screen`, both disabled. Credentials and endpoints use `{env:VARIABLE}` placeholders, never literals.

Plugins load from the `plugins/` directory of the config directory, so `plugins/meta-goal` works after install. See [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Verification

```bash
python scripts/verify.py
```

The script is standard-library only, makes no network calls, and checks paths, JSON, skill frontmatter, command and agent frontmatter, ASCII text, secrets, and absolute user paths. It exits 0 only when every check passes. CI runs the same command on Ubuntu and Windows.

## License

MIT, copyright 2026 Well. See [LICENSE](LICENSE).
