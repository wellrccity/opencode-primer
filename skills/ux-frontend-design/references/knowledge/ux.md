# UX: structure, flows, and usability

Load when: shaping a flow, information architecture, states, or reviewing task
success before visual work starts.

## Principles

- A flow exists to complete a job, not to display every field the database
  allows. Every step must earn its place.
- Hierarchy is a promise about importance. If three elements shout equally,
  the user decides by trial and error.
- Error prevention beats error messaging. A blocked mistake costs seconds; a
  corrected mistake costs minutes plus trust.
- Feedback must answer three questions at once: did my action register, what is
  happening now, and what can I do next.
- Empty screens are teaching surfaces, not accidents. Treat them as designed
  states with a next action.
- Task success and time-on-task are the outcomes. Screen count, clicks, and
  visual polish are proxies that can mislead.

## Decision rules

| Situation | Rule |
| --- | --- |
| Optional field in a core flow | Remove it, or defer it after the primary action |
| Step only collects data used later | Move it out of the critical path |
| Two decisions on one screen | Split only if they need different context; otherwise keep and group |
| Destructive action | Require confirmation proportional to impact, or offer undo |
| Long form | Group in labeled sections; multi-step only when sections are independent |
| Unavoidable delay | Show progress state, then the completed state, then the next action |
| Unknown or missing data | Show explicit "not available" rather than a blank cell |

Information architecture rules:

- Group by user mental model, not by internal team ownership.
- Depth over breadth only when the parent label is unambiguous. Two levels of
  clear navigation beat one level of vague labels.
- Every screen answers: where am I, what can I do, how do I get back.
- A label must be predictive. If it needs a tooltip to be understood, replace
  the label.

Flow review method:

1. List entry points: direct URL, search, email link, in-app link, back button,
   deep link from notification. Any entry can be the first screen.
2. Mark decision points: every place the user must choose. Count them.
3. Mark exits: cancellation, browser back, navigation away, session expiry.
   Each exit must be safe and recoverable.
4. Mark recovery paths: validation failure, network failure, permission denied,
   timeout, partial save.
5. Walk the flow with the fewest possible steps and write the count. Then walk
   it as a first-time user with no context.

## Implementation patterns

Nielsen's 10 heuristics, with a concrete frontend check each:

| Heuristic | Frontend example |
| --- | --- |
| Visibility of system status | Submit button enters a busy state and stays disabled until the request settles |
| Match with the real world | "Arrives Tue, 3 Mar" instead of an internal shipping code |
| User control and freedom | Cancel, close, and undo on every modal and destructive action |
| Consistency and standards | The same "Save" label and position across settings screens |
| Error prevention | Disable submit until required fields are valid; format inputs as typed |
| Recognition over recall | Show the chosen plan and price at the payment step |
| Flexibility and efficiency | Keyboard shortcuts and saved filters alongside the default UI |
| Aesthetic and minimalist design | Remove decoration that does not carry hierarchy or meaning |
| Help users recover from errors | Error text names the field, the problem, and the fix |
| Help and documentation | Inline help at the decision point, not only in a docs site |

Feedback timing (recommendations, not measured standards):

- Under about 100 ms: no indicator needed; the state change is the feedback.
- About 100 ms to 1 s: immediate local state change, no spinner.
- About 1 s to 10 s: visible progress with a label, keep the layout stable.
- Longer: persistent progress, explain what is happening, allow leaving the
  screen if the work continues in the background.

Placement rules:

- Field errors next to the field, plus a summary at the top for long forms.
- Global status near the region it affects, not in a corner far from the cause.
- Never rely on toast alone for a failure that needs a decision. Toasts expire.

Empty states, four variants:

- First use: explain the value and offer the primary creation action.
- No results: restate the filter, offer to clear it, suggest a broader query.
- Error: state what failed, offer retry, keep user input.
- Permission: state the missing access and who can grant it.

Partial or degraded state: some data loaded, stale cache, offline, or a section
failed. Say what is missing, mark freshness, keep the working regions usable,
and offer a per-section retry. Do not blank the whole screen because one region
failed.

Progressive disclosure:

- Show the decision, hide the detail. Advanced options behind one disclosure.
- Never hide information required to make the visible decision safely.
- Disclosure state must be reachable by keyboard and reflect state in its name.

## Anti-patterns

- Multi-step wizard for three fields.
- Required field collected twice in the same flow.
- Validation only on submit when the rule is knowable while typing.
- Success toast while the record still shows the old value.
- Empty state that only says "No data".
- Disabled button with no explanation of why it is disabled.
- Destructive action styled like a neutral one.
- Back button that loses entered data without warning.
- Flow that depends on a hover-only affordance on touch devices.
- Cognitive load hidden behind "it is only one more field".

## Verification

- Walk the happy path at 320 px and at 1440 px with the keyboard only.
- Count steps and decisions in the built flow; compare with the brief.
- Trigger each state deliberately: loading, empty, partial, error, permission
  denied, network offline. Capture a screenshot of each.
- Submit invalid input and confirm the error names field, problem, and fix.
- Confirm every exit is safe: back, cancel, refresh mid-flow, expired session.
- Report task success as a manual walkthrough result, not an assumed metric.

## Related

- `../../checklists/interface-critique.md` for pre-code flow critique.
- `cognitive-psychology.md` for decision counting and memory demands.
- `marketing-cro.md` when the flow carries a commercial goal.
- `../../patterns/forms.md` for field-level structure and validation timing.
