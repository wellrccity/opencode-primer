# Cognitive psychology for interfaces

Load when: a screen feels heavy, choices overload the user, or a review needs a
principled reason instead of taste.

## Principles

- Working memory is small and temporary. Design so users recognize instead of
  remembering.
- Load is either intrinsic (the task is genuinely hard) or extraneous (the
  interface made it harder). Remove extraneous load first.
- Attention is single-channel. Two simultaneous demands produce one delayed
  answer, not two good ones.
- People build a mental model from prior tools. Deviate only when the deviation
  pays for the relearning.
- These principles justify simplifying a task. They never justify an arbitrary
  visual decision on their own.

## Correction to record: Miller

George A. Miller's 1956 paper proposed that working memory has a limited
channel capacity, commonly summarized as 7 plus or minus 2 chunks.

Record it correctly:

- 7 plus or minus 2 is a rough historical ceiling, not a target.
- Miller's number concerned immediate recall of chunks, and the paper is
  explicit that the boundary is fuzzy and manipulable by chunking.
- Modern working-memory estimates are closer to about 4 chunks in typical
  conditions.
- Treat capacity as a reason to chunk, prioritize, and sequence. Do not use it
  as a quota ("navigation may have 7 items", "a form may have 7 fields").

Practical translation:

| Do | Do not |
| --- | --- |
| Group related controls and name the groups | Count items and stop at a magic number |
| Sequence decisions across steps | Hide necessary information to reduce a count |
| Make the current stage obvious | Assume users track more than a few items |

## Decision rules

| Law or effect | Practical rule | Frontend check |
| --- | --- | --- |
| Cognitive load | Move must-remember data into the visible UI | Is any prior value only in the user's head? |
| Recognition over recall | Show options as a list, not as a command to type | Are recent and saved choices visible? |
| Hick-Hyman | Fewer and better grouped options shorten choice time | Count top-level options on the screen |
| Fitts | Make primary targets large and close to the pointer path | Measure target size and distance |
| Serial position | Put the most important items first and last in a sequence | Check the middle of long lists |
| Mental models | Follow the convention the audience already uses | Compare against the closest familiar tool |
| Affordances | Interactive elements must look interactive | Do cards, rows, and icons have clear affordance? |
| Feedback | Every action produces an observable result | Click each control and watch the response |
| Chunking | Group digits, codes, and settings | Are long strings formatted as typed? |
| Progressive disclosure | Show the decision, hide the detail behind one step | Is the hidden content optional? |

Hick-Hyman caution: it describes decision time as a function of options, not a
rule that every menu must be short. Grouping and defaulting matter more than
raw counts.

Fitts caution: bigger is not always better. Distance matters as much as size;
placing a destructive action far from the primary flow is intentional design.

## Implementation patterns

Error prevention over error recovery:

- Constrain input at the source: masks, pickers, ranges, disabled invalid dates.
- Confirm only irreversible actions; offer undo for reversible ones.
- Never require the user to translate a value the system already knows.

Feedback loop, minimal version:

- Immediate local acknowledgment within the same frame as the input.
- Progress label for work longer than about a second.
- Settled state that matches the server truth.
- Explicit failure with a retry path that keeps the input.

Progressive disclosure pattern:

```html
<details>
  <summary>Advanced options</summary>
  <!-- optional settings only; nothing required for the main decision -->
</details>
```

The native element gives keyboard support, state exposure, and text search for
free. Use it before building a custom disclosure widget.

Memory demands audit:

- List every value the user must carry between screens: email, plan, address,
  code, reference number.
- Any value the system owns must be shown, not remembered.
- Any value the user must transcribe must be copyable.

## Anti-patterns

- Using "7 plus or minus 2" to cap navigation, form fields, or menu items.
- Justifying a cluttered screen as "chunked" without visible grouping.
- Hiding required information behind hover.
- Icons with no label where the icon meaning is not universal.
- Reset buttons next to submit in a long form.
- Destructive action adjacent to the primary action with identical styling.
- Confirmation dialogs for every trivial action, training users to dismiss them.
- Placeholder-only labels, forcing recall after typing.
- Showing a raw timestamp or code that the user must convert mentally.
- Citing psychology to defend a preference that the evidence does not support.

## Verification

- Count the decisions on the primary screen. For each, write whether it is
  necessary and whether it belongs there.
- Measure the distance from the last input to the primary target in CSS px.
- List every memory demand and confirm the value is displayed somewhere.
- Trigger a failure and confirm the recovery path preserves the input.
- Test with a first-time user script: can they state the next action without
  reading help text?
- Check the disclosure widget with keyboard only: open, read, close, keep focus.

## Related

- `ux.md` for flow-level structure and state coverage.
- `ui-design.md` for target sizing, contrast, and hierarchy levers.
- `marketing-cro.md` for ethical use of defaults and social proof.
- `../../UX_LAWS_REFERENCE.md` for the full law catalog with examples.
