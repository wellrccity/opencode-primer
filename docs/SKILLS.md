# Skills

18 skills, one directory each: `skills/<id>/SKILL.md`. The description in the frontmatter is what triggers a skill, so the "Use when" column is the short form of it.

| ID | Purpose | Use when |
| --- | --- | --- |
| `anti-slop-docs` | Strip cliches from README, commits, changelog, and docs. | Writing or rewriting user-facing prose. |
| `brainstorm-grill` | Interrogate goal, scope, and acceptance criteria into a short spec. | A feature is ambiguous or oversized before implementation. |
| `browser-control` | Drive real Chrome: navigate, inspect DOM, fill forms, screenshot, read console and network. | Any browser automation or web testing task. |
| `caveman-mode` | Cut narration and token use while keeping facts and risks. | The user says "caveman mode"; exits on "normal mode". |
| `code-review` | Read-only diff review with `[BLOCKER]`, `[WARNING]`, `[SUGGESTION]`. | Before merging or integrating a change. |
| `create-skill` | Turn a recurring workflow into a small, reusable skill. | The same procedure has been repeated a few times. |
| `execution-focus` | Return to short, concrete steps. | Scope is large, attention drifts, or the task stalls. |
| `git-safe` | Inspect the diff and protect existing work before git actions. | Before commit, branch, rebase, or push. |
| `image-generation` | Generate website assets, brand visuals, icons, and hero banners with configurable image models, background removal, and vision curation. | Generating web assets, brand visuals, icons, or banners. |
| `mandatory-verification` | Run the most relevant check and report real output as Changed / Verified / Missing / Next step. | After any edit. |
| `meta-goal` | Bound a long task by a measurable done condition and a turn budget, judged each turn. | A task needs a hard stop condition. See `/meta`. |
| `professional-workflow` | Understand, plan micro-steps, smallest diff, verify by running. | Any non-trivial code task. |
| `session-handoff` | Record state, files touched, and the literal next step. | Pausing, switching model, or running low on context. |
| `systematic-debugging` | Reproduce, isolate the cause, fix, and add a regression test. | An error or unexpected behavior appears. |
| `tdd-plan` | Small red-green-refactor tasks with a check per step. | A change can be expressed as verifiable increments. |
| `understand-code` | Build a lean map of an unfamiliar codebase without reading everything. | Entering a new repository or module. |
| `ux-frontend-design` | Product-quality frontend system: UX flows, UI and art direction, responsive layout, accessibility, CRO, engineering, performance, SEO, security, and visual QA. | Designing, building, reviewing, or auditing any web interface. |
| `web-research` | Search briefly, confirm against the primary source, summarize. | Current docs, changelogs, or external facts are needed. |

## Workflow chain

The skills compose in one order for feature work:

```text
brainstorm-grill -> tdd-plan -> mandatory-verification -> code-review -> session-handoff
```

1. `brainstorm-grill` fixes the goal and acceptance criteria.
2. `tdd-plan` turns them into small verifiable steps.
3. `mandatory-verification` runs the checks after each step.
4. `code-review` inspects the finished diff read-only.
5. `session-handoff` records state if the work pauses.

Supporting skills slot in as needed: `understand-code` before planning in an unknown repository, `systematic-debugging` when a check fails, `git-safe` before any commit, `execution-focus` when the plan drifts, `meta-goal` for a long bounded effort, `caveman-mode` for terse output.

## Frontmatter contract

```markdown
---
name: skill-id
description: Use when ...
---
```

- `name` equals the directory and matches `^[a-z0-9]+(-[a-z0-9]+)*$`.
- `description` starts with "Use when" and is 20-400 characters.
- The directory contains `SKILL.md` plus an optional `references/` subdirectory for long-form material.

`python scripts/verify.py` enforces all three.
