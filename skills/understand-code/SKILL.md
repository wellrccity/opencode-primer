---
name: understand-code
description: Use when entering an unknown codebase; build a compact map of the structure and flow without wasting context.
---

# Understand code

## Initial map
1. Look at the top-level structure and read README, AGENTS.md, and relevant manifests.
2. Find the entry points (main, index, routes, CLI) and follow the flow to the main data and services.
3. Write `.code-map.md` only when it helps to resume or guide a change.
4. Record: entry, main flow, state and data, tests, and known risks.
5. End with five bullets: where to change X, where to test Y, and what was not verified.

## Context economy
- Start with at most five relevant files; expand only when needed.
- Prefer precise searches over recursive reading.
- Ignore dependencies and artifacts (`node_modules`, `.git`, `logs`, `dist`, `build`, `.venv`).
- Do not assume file names or entry commands are the same across projects.
