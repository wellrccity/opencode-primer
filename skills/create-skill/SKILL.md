---
name: create-skill
description: Use when turning a recurring workflow into a small, specific, reusable OpenCode skill with clear triggers.
---

# Create a skill

1. Identify the pattern from examples the user provides; do not read old sessions without an explicit request.
2. Choose a short kebab-case ID and a description that states clearly when to activate it.
3. Write `SKILL.md` with triggers, workflow, limits, and output format. Keep one objective.
4. Move long details to `references/`; include no secrets, private paths, or unverified commands.
5. Review one case that should activate and one similar case that should not.
6. Save to `<config>/skills/<id>/SKILL.md` (global) or `.opencode/skills/<id>/SKILL.md` (project).
