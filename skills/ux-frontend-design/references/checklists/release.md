# Release checklist

When to use: before merge and before deploy of any change that touches the interface.
Severity: Blocker, Warning, Suggestion.

Blocker stops the release. Warning needs a recorded decision. Suggestion can
follow the release. No row is closed by opinion; each closes with evidence.

## Completion levels

Four levels, in order. A release claim names the highest level reached.

| Level | Meaning | Proof |
| --- | --- | --- |
| 1 Code written | The diff compiles in the editor and covers the intended surfaces | Diff plus the touched file list |
| 2 Build passes | The production build completes without new warnings | Build command and full output |
| 3 Tests pass | Existing and new tests run green | Test command and summary line |
| 4 Interface validated | The rendered interface was exercised in a browser | Screenshots, keyboard pass, console and network exports |

## Minimum gate

Run this before claiming any level above code written. It takes about two
minutes and covers the failures that one-width screenshots miss.

| Check | Pass condition | Evidence |
| --- | --- | --- |
| 320 px overflow | `document.documentElement.scrollWidth` equals `clientWidth`; no element extends past the viewport | Probe output with the offending element list |
| First viewport at 390x844 | The primary action or entry point is fully visible without scrolling | Screenshot with the action above the fold |
| Keyboard path | Primary path completes with Tab, Enter, and Escape; focus is visible at every stop | Focus-stop list or recording |
| Console | Zero errors and no new warnings | Console export |
| External requests | Zero for a standalone file; only expected origins otherwise | Network export |
| Light and dark | Both checked when the project ships both | Paired captures |

For a standalone HTML file with no build, mark the build, lint, and test rows
as not applicable and use this gate as the release evidence.

## Full gate

| Check | Severity | Evidence |
| --- | --- | --- |
| Stack detected from manifests, not assumed | Blocker | Manifest and lockfile names plus the chosen command per stage |
| Lint command from the project scripts run and green | Blocker | Command and final output line |
| Typecheck or compile step run and green | Blocker | Command and final output line |
| Test suite run and green, including new behavior | Blocker | Command, pass and fail counts |
| Production build run and green with no new warnings | Blocker | Build command and bundle sizes before and after |
| Standalone HTML: document parses, no external requests, no console errors | Blocker | Browser load plus network and console exports |
| Console clean on every changed route | Blocker | Console export filtered to the session |
| Network clean: no failed request, no unexpected 4xx or 5xx | Blocker | Network export with status codes |
| Screenshots reviewed at 320, 375, 768, 1024, 1440 CSS px | Blocker | Five captures per changed view, named by width |
| Light and dark mode checked when the project ships both | Warning | Paired captures per view |
| State coverage confirmed for touched surfaces | Blocker | State inventory: default, hover, focus, active, disabled, loading, empty, error, partial, success |
| Accessibility checklist complete for the change | Blocker | Filled `accessibility.md` table with zero open Blockers |
| Responsive checklist complete for the change | Blocker | Filled `responsive.md` table with zero open Blockers |
| Keyboard-only pass done on the primary flow | Blocker | Focus stop log and a capture of each visible indicator |
| Performance measured before and after | Warning | LCP, INP, CLS values with the tool and percentile named |
| Core Web Vitals within threshold or deviation recorded | Warning | LCP at or under 2.5 s, INP at or under 200 ms, CLS at or under 0.1 at the 75th percentile |
| No secret, token, or key in client code, bundle, or logs | Blocker | Grep result for secret patterns plus a bundle scan |
| Authorization enforced on the server, not only in the UI | Blocker | Route or handler code showing the permission check |
| Inputs validated and output escaped at the boundary | Blocker | Validation and escaping call sites for each new input |
| Cookies and session settings reviewed for the change | Warning | Attribute dump: httpOnly, secure, sameSite, expiry |
| No sensitive data in URLs, analytics, or error messages | Blocker | Request log and event payload sample |
| Copy reviewed for accuracy, tone, and honesty | Blocker | Final strings with the claim each one makes |
| No fake urgency, fake scarcity, or fabricated proof | Blocker | Copy inventory checked against the ethics rules |
| Placeholder text and dead links removed | Blocker | Search result for placeholder markers and empty href values |
| Error, empty, and offline states reachable and correct | Blocker | Capture of each state plus the trigger that produced it |
| Feature flag or kill switch identified when one exists | Warning | Flag name and the off-state screenshot |
| Rollback note written: revert commit or disable flag | Blocker | Rollback line in the pull request with the exact command |
| Evidence list attached to the pull request | Blocker | Section listing each command, capture, and measurement |
| No unrelated change in the diff | Warning | Diff stat limited to the intended files |
| Release claim matches the level reached | Blocker | One sentence naming the level and the evidence behind it |

## How to run

1. Read the manifests and the script block. Write down the lint, typecheck,
   test, and build commands actually defined by the project.
2. Run them in that order and paste the final output line of each into the pull
   request. Stop at the first failure; fix, then restart the sequence.
3. Open every changed route in a production build and export the console and
   the network panel.
4. Run `visual-review.md`, `responsive.md`, and `accessibility.md`. Link each
   filled table in the evidence section.
5. Measure performance with the same tool and conditions as the baseline, and
   record both numbers.
6. Walk the copy and the security rows against the diff, not against memory.
7. Write the rollback line before merging, not after a failure.

## Pass criteria

- Every Blocker row is closed with a linked artifact.
- Every Warning has an owner, a decision, and a date.
- The evidence section contains commands with real output and captures with
  real dimensions, not descriptions of them.
- The completion level named in the summary matches the checks that actually
  ran; level 4 requires a browser pass.
- Rollback is one command or one flag, verified by reading it.

## Related

- `visual-review.md` for screenshot and state evidence.
- `responsive.md` and `accessibility.md` for the gates this file references.
- `../knowledge/performance.md` for measurement method and thresholds.
