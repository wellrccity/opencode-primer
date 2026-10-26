# Configuration

OpenCode reads its global configuration from the config directory, by default `$HOME/.config/opencode` (Windows: `%USERPROFILE%\.config\opencode`), or from `$OPENCODE_CONFIG_DIR` when set.

## Files

| File | Installed as | Purpose |
| --- | --- | --- |
| `config/opencode.json` | `opencode.json` | Core settings for OpenCode 2.x. |
| `config/cli.json` | `cli.json` | CLI preferences and keybind-level defaults. |
| `config/AGENTS.md` | `AGENTS.md` | Global agent instructions. |
| `config/opencode.example.json` | not installed | Optional template for providers and MCP servers. |

`config/opencode.json` deliberately holds no providers, models, MCP servers, plugin paths, or credentials. Add those in your own copy so upgrades stay simple.

## Core settings

| Key | Value | Effect |
| --- | --- | --- |
| `$schema` | schema reference | Editor validation for the config file. |
| `formatter` | `true` | Enable the built-in formatter. |
| `tool_output` | `800` / `20000` | Truncate tool output: small preview, larger stored limit. |
| `compaction` | `auto` | Compact long sessions automatically. |
| `compaction.keep` | `8000` | Recent tokens kept verbatim. |
| `compaction.buffer` | `12000` | Headroom reserved before compaction triggers. |
| `watcher.ignore` | list | Skip `node_modules`, `.git`, `logs`, `*.log`, `dist`, `build`, `__pycache__`, `.venv`. |
| `permissions` | ordered array | Allow, ask, and deny rules for tools. |

## Permissions

`permissions` is an ordered list where the last matching rule wins: the final rule that matches a tool call decides the outcome. The shipped array starts with broad allows and ends with specific denies, so the narrow deny entries override the earlier allows. Read it top to bottom before installing: it is the authoritative statement of what the agents may do on your machine.

When you add rules, append specific denies after the broad allows, and prefer denying a destructive command over relying on instructions. The `reviewer` and `planner` agents additionally deny `edit` and `write` in their own frontmatter.

## Environment placeholders

Never write a literal credential into a config file. Use placeholders and set the variable in the shell that launches OpenCode:

```json
{
  "provider": {
    "local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local",
      "options": {
        "baseURL": "{env:LOCAL_BASE_URL}",
        "apiKey": "{env:LOCAL_API_KEY}"
      },
      "models": {
        "local-model": { "name": "Local model" }
      }
    },
    "cloud": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Cloud",
      "options": {
        "baseURL": "{env:CLOUD_BASE_URL}",
        "apiKey": "{env:CLOUD_API_KEY}"
      },
      "models": {
        "cloud-model": { "name": "Cloud model" }
      }
    }
  }
}
```

The snippet shows the shape used by `config/opencode.example.json`; provider IDs and model names there are examples. Set the variables before starting OpenCode:

```powershell
$env:LOCAL_BASE_URL = "http://127.0.0.1:1234/v1"
$env:LOCAL_API_KEY = "local"
```

```bash
export LOCAL_BASE_URL="http://127.0.0.1:1234/v1"
export LOCAL_API_KEY="local"
```

An unset variable leaves the provider unusable rather than exposing a default key, which is the intended failure mode.

## MCP servers

The example file declares `chrome` and `screen` under the MCP server map, both with `"disabled": true` and placeholder commands. Enable one only after its command exists locally, and keep credentials in environment variables. Leave them disabled on shared machines.

## Plugins

Plugins are discovered from the `plugins/` directory inside the config directory, so a folder install is enough:

```text
<config directory>/plugins/meta-goal/index.js
<config directory>/plugins/meta-goal/package.json
```

`plugins/meta-goal` provides the turn-budget goal loop behind `/meta`, `/meta-status`, and `/meta-clear`. It needs no registration entry and no network access; state is stored locally by the plugin.

## Agents and commands

`agents/*.md` and `commands/*.md` are read from the config directory after install. Agent frontmatter requires `description`; `mode` defaults to primary and `steps` is optional. Command frontmatter requires `description`. Editing those files takes effect after a restart. Free-tier and paid model IDs pinned in `agents/*.md` depend on the account; if a pinned model is not available in your account, change the `model` field.

## What not to commit

Keep provider keys, personal endpoints, machine-specific paths, and session state out of the repository. `config/opencode.example.json` is the only file that should describe providers, and it must use `{env:...}` placeholders throughout.
