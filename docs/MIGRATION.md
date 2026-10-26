# Migration

This repository replaces the earlier Portuguese-named configuration. The behavior is preserved; names, descriptions, and prompts are English.

## Renamed skill IDs

| Legacy directory | New directory |
| --- | --- |
| `anti-slop-docs` | `anti-slop-docs` |
| `brainstorm-grill` | `brainstorm-grill` |
| `browser-control` | `browser-control` |
| `cria-skill` | `create-skill` |
| `debug-sistematico` | `systematic-debugging` |
| `entenda-codigo` | `understand-code` |
| `fluxo-profissional` | `professional-workflow` |
| `foco-execucao` | `execution-focus` |
| `git-seguro` | `git-safe` |
| `handoff-sessao` | `session-handoff` |
| `meta-goal` | `meta-goal` |
| `modo-caveman` | `caveman-mode` |
| `plano-tdd` | `tdd-plan` |
| `revisao-codigo` | `code-review` |
| `verificacao-obrigatoria` | `mandatory-verification` |
| `web-pesquisa` | `web-research` |

Remove the old directories after installing; a leftover legacy directory is not read by the new references and causes duplicate or stale triggers.

## What else changed

- Skill frontmatter is `name: <id>` plus an English description that starts with "Use when".
- Command templates from the old inline config now live in `commands/` as English prompts: `team-build`, `verify`, `review`, `plan`, `grill`, `tdd`, `handoff`, `map`.
- `reviewer` and `planner` are markdown agents in `agents/`, both denying `edit` and `write`; `reviewer` permits only `git status` and `git diff` in shell.
- The meta-goal plugin parses `stop after` and `turns` in English; `--judge` and `--max-turns` are unchanged.
- Temporary paths are cross-platform: `$env:TEMP\opencode\` on Windows and `${TMPDIR:-/tmp}/opencode/` elsewhere.
- Code maps are written to `.code-map.md`, not the old `.mapa.md`.
- Core config moved to `config/opencode.json` with the v2 schema and no provider block.

## Rotate exposed credentials

If the old configuration was shared, copied into a chat, or committed, assume every credential in it is disclosed.

1. List every provider, MCP server, and integration the old config referenced.
2. Revoke each key, token, and session at the provider.
3. Issue replacements and store them as environment variables, not in files.
4. Reference them as `{env:VARIABLE}` in the new config.
5. Search history and working trees for leftovers before pushing: key prefixes, bearer tokens, private hostnames.
6. Rewrite history only after rotation is complete; the rotation is what actually limits exposure.

## Remove absolute paths

The old config pointed at one specific Windows profile. Replace every absolute path with a portable form.

- Search for drive-letter paths and for the Windows user profile prefix. Any hit is a migration defect.
- Use `$HOME` or `$env:USERPROFILE` in scripts, and `$env:TEMP\opencode\` for temporary work.
- Use `$OPENCODE_CONFIG_DIR` when a fixed config location is required.
- Use relative paths inside the repository and document the base directory.
- Drop machine-specific MCP commands; keep placeholders in `config/opencode.example.json` instead.

`python scripts/verify.py` rejects absolute user paths, so a clean run is the acceptance check.

## Migration checklist

- [ ] New skills installed under `skills/`; legacy directories removed.
- [ ] `opencode.json` installed from `config/opencode.json`; providers merged from your own copy.
- [ ] All credentials rotated and replaced with environment placeholders.
- [ ] Absolute paths replaced; verification passes.
- [ ] OpenCode restarted and commands, agents, and skills visible.
- [ ] Old backups and exported configs deleted or stored outside the repository.
