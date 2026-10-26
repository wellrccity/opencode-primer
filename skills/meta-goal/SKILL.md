---
name: meta-goal
description: Use when a long task has a measurable done condition and a turn limit; the plugin judges every turn.
---

# Meta goal

## Start
- Use `/meta <measurable condition>` and include verifiable proof and limits.
- Default limit: 12 turns; maximum: 15. Example: `/meta all tests pass and lint passes; stop after 8 turns`.
- To choose the judge manually: `/meta --judge provider/model <condition>`. The default judge is `opencode/glm-5.3-flash-free`.

## Loop
1. Take one micro-step.
2. Run the proof command and show the real output.
3. The plugin sends a recent slice of the conversation to the judge model, which may only declare `MET`, `NOT_YET`, or `IMPOSSIBLE` with evidence.
4. `NOT_YET` starts another turn automatically; `MET`, `IMPOSSIBLE`, three evaluations without progress, or the turn limit end the loop.

## Commands
- `/meta-status`: condition, judge, turns, and last verdict.
- `/meta-clear`: stop and clear this session's goal.
- If the default judge is unavailable, pick a model with `/models` and restart with `/meta --judge provider/model ...`.

Do not use vague goals. Do not declare completion without proof. The recent transcript is sent to the judge provider; do not put secrets in the task.
