# Accessibility checklist

When to use: before merge for any interactive change, and for a WCAG 2.2 AA audit.
Severity: Blocker, Warning, Suggestion.

Blocker stops merge. Warning needs a recorded decision. Suggestion can follow.
Evidence is a documented pass, a measured value, or a tool report - not a claim.
Criterion numbers are WCAG 2.2; check the official document when wording matters.

| Check | Severity | Evidence |
| --- | --- | --- |
| Structure exposed by native semantics (1.3.1) | Blocker | Accessibility tree export of the page with regions and lists intact |
| One `h1`, no skipped heading levels (1.3.1, 2.4.6) | Blocker | Heading outline export in document order |
| Landmarks present: banner, navigation, main, contentinfo (1.3.1) | Blocker | Landmark list from the accessibility tree |
| Page has a unique descriptive title (2.4.2) | Warning | Title string per route, compared across routes |
| Page language declared (3.1.1) | Warning | `lang` attribute on the root element |
| Text contrast at least 4.5:1 for body, 3:1 for large text (1.4.3) | Blocker | Measured ratio per text style, including text over images |
| Non-text contrast at least 3:1 for controls and state cues (1.4.11) | Blocker | Measured ratio for border, icon, focus ring, and checked state |
| Color is never the only carrier of meaning (1.4.1) | Blocker | Screenshot in grayscale of the state that relies on color |
| Every function reachable by keyboard (2.1.1) | Blocker | Keyboard pass log listing each control and the reach key |
| No keyboard trap anywhere, including overlays (2.1.2) | Blocker | Recording of `Tab` and `Shift+Tab` cycling out of every overlay |
| Focus order follows the visual and reading order (2.4.3) | Blocker | Ordered focus stop list compared with the visual order |
| Focus indicator visible on every stop (2.4.7) | Blocker | Screenshot per stop, ring contrast measured against the background |
| Focused element never fully hidden by sticky content (2.4.11) | Blocker | Screenshot of the last field with sticky header or footer in view |
| Accessible name on every control (4.1.2, 1.1.1) | Blocker | Name, role, value export for each control |
| Icon-only buttons carry a programmatic name | Blocker | Accessibility tree entry for each icon button |
| Name, role, and value are correct for custom widgets (4.1.2) | Warning | Snapshot of the custom widget in the accessibility tree |
| ARIA used only where native semantics fail | Warning | List of ARIA attributes with the native element considered first |
| Status messages announced without stealing focus (4.1.3) | Warning | Live region markup plus a screen-reader capture of the toast |
| Hover or focus content dismissible and persistent (1.4.13) | Warning | Recording of the tooltip closing with `Escape` and hoverable |
| Dragging has a single-pointer alternative (2.5.7) | Blocker | Recording of the non-drag path for each draggable feature |
| Targets at least 24x24 CSS px, or spaced exception applies (2.5.8) | Blocker | Measured bounding boxes of adjacent targets |
| Primary targets 44x44 CSS px recommended (2.5.5 is AAA) | Suggestion | Measurements for primary actions only |
| Labels or instructions present before input (3.3.2) | Blocker | Field inventory with label, hint, and required marker |
| Errors identified in text and linked to the field (3.3.1) | Blocker | Screenshot of the error summary and its anchor target |
| Error messages suggest a correction (3.3.3) | Warning | Error string per validation rule |
| Required fields marked in text, not only by color or asterisk | Warning | Label markup for each required field |
| Previously entered data not requested twice (3.3.7) | Warning | Flow walkthrough showing prefilled values |
| Authentication allows paste and password managers (3.3.8) | Blocker | Attribute dump of the credential inputs, no paste blocker |
| Login has no cognitive function test (3.3.8) | Blocker | Screenshot of the challenge and the alternative offered |
| Animation can be paused, stopped, or hidden (2.2.2) | Warning | Control screenshot for any auto-playing motion over five seconds |
| Reduced motion respected for parallax and large transitions | Blocker | Recording with `prefers-reduced-motion: reduce` forced |
| No content flashes more than three times per second (2.3.1) | Blocker | Frame capture of the fastest animation |
| Text resizes to 200 percent without loss (1.4.4) | Blocker | Screenshot at 200 percent text-only zoom |
| Content reflows at 320 px without two-dimensional scroll (1.4.10) | Blocker | Screenshot at 320 px with measured scroll width |
| Text spacing overrides do not clip content (1.4.12) | Warning | Screenshot with the standard spacing override values |
| Help offered in the same relative position across pages (3.2.6) | Suggestion | Screenshot comparison of the help entry point |
| Images of text avoided where real text is possible (1.4.5) | Warning | Markup list of text rendered as an image |
| Automated scan run and every finding triaged | Blocker | Scan report with the count of unresolved findings and reasons |
| Screen-reader spot check on the primary flow | Blocker | Recording or transcript of one task completed with a screen reader |

## How to run

1. Run an automated scan such as axe or Lighthouse accessibility on each changed
   route. Record the report. The tool catches a minority of issues; keep going.
2. Do a keyboard-only pass: `Tab`, `Shift+Tab`, `Enter`, `Space`, arrow keys,
   `Escape`. Log every stop and note the order and the visible indicator.
3. Zoom the browser to 200 percent and then to 400 percent at a 1280 px
   viewport. Confirm no content is lost and only one scroll axis appears.
4. Measure contrast on real rendered text, including text over images, with a
   picker on the two worst pixels behind each string.
5. Inspect the accessibility tree for names, roles, landmarks, and heading
   order. Compare it with the visible UI.
6. Complete the primary flow once with a screen reader, on the platform the
   audience uses most.
7. Map every open item to its criterion number and severity, then re-run the
   table after the fix.

## Pass criteria

- Zero Blocker rows open.
- Every Warning has a recorded decision with an owner.
- A scan report exists and its findings are triaged, not ignored.
- Keyboard and screen-reader passes cover the primary flow end to end.
- Contrast, target size, and zoom values are recorded as measured numbers.

## Related

- `../knowledge/accessibility.md` for the criteria set and remediation patterns.
- `responsive.md` for reflow, zoom, and target measurement methods.
- `release.md` for where this evidence is recorded before shipping.
