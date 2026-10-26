# Install

Two scripts install the same files: `scripts/install.ps1` for PowerShell and `scripts/install.sh` for bash 4+.

## Target directory

| Platform | Default target |
| --- | --- |
| Windows | `%USERPROFILE%\.config\opencode` |
| Linux, macOS | `$HOME/.config/opencode` |
| Any, with override | `$OPENCODE_CONFIG_DIR` |

The environment variable wins when it is set and non-empty. Set it for a sandbox or a portable install:

```powershell
$env:OPENCODE_CONFIG_DIR = "C:\tools\opencode-config"
.\scripts\install.ps1
```

```bash
export OPENCODE_CONFIG_DIR="$HOME/opencode-config"
bash scripts/install.sh
```

Quote paths that contain spaces.

## File mapping

| From the repository | To the target directory |
| --- | --- |
| `config/opencode.json` | `opencode.json` |
| `config/cli.json` | `cli.json` |
| `config/AGENTS.md` | `AGENTS.md` |
| `agents/*` | `agents/` |
| `commands/*` | `commands/` |
| `skills/*` | `skills/` |
| `plugins/meta-goal` | `plugins/meta-goal` |

`config/opencode.example.json` is a template; the installer does not copy it. Copy it yourself and rename it if you want the sample providers and MCP entries.

Directories are created as needed. Files that already exist are skipped unless the force flag is used, and unrelated files in the target are never deleted.

## Options

| PowerShell | bash | Effect |
| --- | --- | --- |
| `-DryRun` | `--dry-run` | Print planned actions, write nothing. |
| `-Force` | `--force` | Back up the whole target, then overwrite. |
| `-Help` | `--help` | Print usage. |

Example runs:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Force
```

```bash
bash scripts/install.sh --dry-run
bash scripts/install.sh
bash scripts/install.sh --force
```

## Backup behavior

With the force flag and an existing target, the script copies the entire target to a sibling directory named `<target>-backup-<yyyyMMdd-HHmmss>` before writing. Nothing is pruned or merged destructively. If the backup fails, the install aborts with exit code 1.

Without the force flag there is no backup, because existing files are skipped.

## After installing

1. Restart OpenCode, or start it if it was not running; config is read at startup.
2. Confirm the commands appear in the command list and the skills are listed.
3. Optionally copy `config/opencode.example.json` to the target as `opencode.json` only after merging your providers into it, since it replaces the core file.

## Optional MCP servers

The example config declares two servers, both `"disabled": true`:

| Server | Needs |
| --- | --- |
| `chrome` | The browser bridge extension and a matching local server command. |
| `screen` | A desktop automation server on the same machine. |

Enable a server only after its command is installed and you have reviewed the permissions it implies. Leave them disabled on shared or remote machines. Replace placeholder commands and hosts with your own values; do not commit them.

## Uninstall

Delete the files you installed, or restore the timestamped backup directory. OpenCode state, session history, and authentication live elsewhere and are not touched by these scripts.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| PowerShell refuses to run the script | Use `-ExecutionPolicy Bypass` for the single invocation, as shown above. |
| Nothing was written | You ran a dry run, or every file already existed and was skipped. |
| Files landed in the wrong place | Unset `OPENCODE_CONFIG_DIR` or point it at the intended directory. |
| Skill not detected | The directory name is the skill ID, not the frontmatter `name`; the `description` frontmatter is what drives discovery. Both must be present and unique. |
