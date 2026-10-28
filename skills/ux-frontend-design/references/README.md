# UX Frontend Design references

Reference set for the `ux-frontend-design` skill. The entry point is
[../SKILL.md](../SKILL.md); it is the only file loaded by default. Modules here
are deep dives, loaded on demand by the router in the entry point.

Loading discipline: read the entry point first, then only the modules the
decision router selects for the current task. Do not preload the whole tree.

## Tree

| Folder | Files | Purpose |
| --- | --- | --- |
| `..` | `SKILL.md` | Entry point: principles, modes, workflow, floors, router, done criteria. |
| `.` | `README.md` | This index: loading rules, depth choice, gates, portability. |
| `.` | `UX_LAWS_REFERENCE.md` | Legacy deep dive: named UX laws with implementation examples. |
| `.` | `MODERN_UX_PLAYBOOK.md` | Legacy deep dive: tactical patterns for speed, forms, motion, keyboard. |
| `knowledge/` | 11 files | Principles and decision rules per discipline: UX, UI, art direction, CRO, psychology, responsive, accessibility, engineering, performance, SEO, security. |
| `patterns/` | 12 files | Screen-level contracts: layout, states, interaction, data, accessibility, anti-patterns, checklist. |
| `checklists/` | 5 files | Severity-rated verification tables for critique, visual, responsive, accessibility, and release. |

## Choosing depth

Depth modes are defined in [../SKILL.md](../SKILL.md) under `Depth modes`.

- Audit or Review: load a checklist plus the knowledge module for the topic.
- Improve: load the owning pattern module and the knowledge module it names.
- Build: start with `knowledge/ux.md` and `knowledge/art-direction.md`, then the
  pattern module for the surface, then the release checklist.

Workflow phases and their gates are in `Workflow` in the entry point. Skip rules
live under `Skip rules`; they reduce scope, never verification.

## Project memory

Before writing any module-guided code, inspect the project for tokens,
components, typography, spacing, radii, motion, tone, and dark mode. Extend
existing tokens instead of adding parallel values.

Record the decision set in the plan or PR summary:
- Reused: tokens, components, and patterns taken as-is.
- Extended: new tokens or variants and why the existing set was insufficient.
- Added: new components, with the pattern module that justified them.

## Quality gates

The floors in `Non-negotiable floors` apply to every mode. The full gate is
`Definition of done` plus `Verification protocol` in the entry point.

| Level | Evidence required |
| --- | --- |
| Code written | Diff reviewed, tokens reused, states named. |
| Build passes | Build command and output quoted. |
| Tests pass | Test command and result quoted. |
| Interface validated | Browser pass at 320, 375, 768, 1024, 1440 CSS px, keyboard, zoom, console, network. |

`checklists/release.md` is the gate for the final level. Do not report a level
you did not observe.

## Portability

Copy the whole skill directory, including `references/`, as one unit. Modules
cross-link with relative paths and are not designed to be split, renamed, or
merged into a single prompt. Each module stays useful when loaded alone, but the
router and the gates assume the full tree.
