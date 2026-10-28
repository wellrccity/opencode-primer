# Interface critique checklist

When to use: before UI code exists, to judge a flow, screen, or prototype on paper.
Severity: Blocker, Warning, Suggestion.

Blocker stops the work until fixed. Warning needs a decision before merge.
Suggestion is polish that can ship later. Every row needs an artifact, not an opinion.

| Check | Severity | Evidence |
| --- | --- | --- |
| Goal stated in one sentence | Blocker | Brief line naming the single job the screen does |
| Audience and context named | Warning | Brief line naming who, where, and on which device |
| Success metric chosen | Warning | Metric name plus its data source, written in the brief |
| Primary action per decision region | Blocker | Wireframe marks exactly one primary action per region |
| Hierarchy matches user priority | Warning | Ranked list of the top three elements compared with the brief |
| Flow length justified | Warning | Step count from entry to outcome, each step with a purpose |
| Decision count measured | Warning | Count of simultaneous choices per screen; above five needs a reason |
| Recovery path for every terminal state | Blocker | Each error and empty state names one exit action |
| Five states planned per surface | Blocker | State inventory listing loading, empty, error, partial, success |
| Error prevention before messages | Warning | Inputs list with constraints, defaults, and confirmations |
| Destructive actions guarded | Blocker | Confirmation or undo named for each destructive control |
| Project memory reused | Blocker | Tokens, components, and tone listed as reused or added |
| Consistency with existing screens | Warning | Diff of patterns against two reference screens |
| Visual direction is one deliberate idea | Warning | Direction brief: audience, three adjectives, references, anti-references |
| Generic-UI risks named | Warning | Screens checked against the anti-generic ban list, exceptions justified |
| Content is real or owned | Blocker | Placeholder strings carry an owner and a due date |
| Accessibility risks identified | Blocker | Risk list with WCAG 2.2 AA criterion numbers |
| Performance risks identified | Warning | Named risks: LCP element, added scripts, added fonts, added images |
| Mobile order defined | Warning | Stacked element order documented for 320 and 375 px |
| Copy reviewed for honesty | Warning | Headline, CTA, and error text read against the no-fake-proof rule |
| Navigation model and URL state | Warning | Screen map with the URL of each view and back behavior |
| Permissions covered | Blocker | Matrix of role against visible action |
| Privacy surfaces planned | Warning | Consent, data retention, and analytics fields listed |
| Localization and text expansion | Suggestion | Longest label per string, measured in characters |
| Instrumentation planned | Suggestion | Event list with trigger and property names |

## How to run

1. Read the brief. If none exists, write one paragraph first: goal, audience,
   job to be done, constraint, success metric.
2. List every screen and state in scope. Mark each as new, changed, or reused.
3. Walk the flow as a first-time user from entry point to outcome. Count steps
   and decisions out loud, then compare with the brief.
4. Fill the table. Write the artifact name in the Evidence column, not a feeling.
5. Turn each Blocker into a proposed fix with an owner and an estimate.
6. Re-run the table after the fix and keep the earlier column for comparison.

## Findings format

- One finding per line: `[Blocker] location - defect - proposed fix`.
- Order by severity, then by position in the flow.
- No finding without a location and a fix. "Feels off" is not a finding.
- Group by theme only after the severity list is complete.

## Pass criteria

- Zero Blockers open.
- Every Warning carries a decision: fix now, accept with a reason, or defer with a date.
- Each touched surface has a state inventory with all five states.
- Project memory lists reused and added tokens, components, and copy.
- The findings list fits one screen per flow; longer means the scope is too broad.

## Related

- `../knowledge/ux.md` for flows, heuristics, and error prevention.
- `../knowledge/art-direction.md` for the direction brief.
- `visual-review.md` for the same review once the interface renders.
