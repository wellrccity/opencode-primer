# Security

## Secrets

This repository contains configuration only. It must never contain credentials, API keys, tokens, session cookies, or private hostnames.

- Provider credentials are referenced as `{env:VARIABLE}` placeholders and resolved at runtime.
- Local overrides live outside the repository, in the config directory.
- Example files use placeholder values only, with disabled MCP servers.
- Logs and backups are ignored by git; never add them with `git add -f`.

If a credential ever lands in a commit, treat it as disclosed: revoke it at the provider, issue a new one, and only then rewrite history. Rotating the secret matters more than hiding the commit.

## Reporting a vulnerability

Report privately through the repository's security advisory feature on the hosting platform. Do not open a public issue for a suspected vulnerability.

Include the affected file, the impact, and the shortest reproduction you have. The maintainer acknowledges a report, confirms or rejects it, and coordinates disclosure. Please allow time for a fix before publishing details.

## Scope

In scope: the installers, the verification script, the plugin, and the shipped configuration defaults, including permission rules that may be too permissive.

Out of scope: vulnerabilities in OpenCode itself, in model providers, or in third-party MCP servers. Report those upstream.

## Hardening notes

- Review the `permissions` array in `config/opencode.json` before installing; it is the authoritative rule list for the agents.
- Keep MCP servers disabled until you have installed and trust them.
- Installers never delete files; they skip existing ones unless you pass the force flag, which backs up the target directory first.
