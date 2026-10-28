# Accessibility

Load when: building or auditing any interface that people must operate with a keyboard, a screen reader, zoom, or a touch target smaller than a fingertip.

## Principles

- Accessibility is a correctness property of the markup, not a feature added after styling. Fix the element before writing an ARIA attribute.
- WCAG 2.2 AA is the working floor. Every criterion below is testable; treat an untested criterion as unverified, not as passed.
- Native semantics first: `button`, `a`, `input`, `label`, `fieldset`, `table`, `h1`-`h6`, `nav`, `main`, `dialog`. Reach for ARIA only when no native element carries the behavior.
- No ARIA is better than bad ARIA. A wrong role is worse than no role, because it overrides the real one.
- Focus is a visible, ordered, recoverable position. A keyboard user must always know where they are and how they got there.
- Contrast, target size, and reflow are measurable. Measure them instead of judging them by eye.
- Motion, time limits, and automatic changes need an explicit off switch or a pause.
- Assistive technology announces what the DOM says, not what the screen shows. Anything conveyed by position, color, or icon alone is missing.

## Decision rules

### WCAG 2.2 AA working set

| Criterion | Requirement in practice |
| --- | --- |
| 1.3.1 Info and Relationships | Structure is expressed in markup: lists, tables with headers, fieldsets, labels, heading levels |
| 1.4.3 Contrast (Minimum) | Body text 4.5:1, large text (24 px or 18 pt, or 18.66 px or 14 pt bold) 3:1 |
| 1.4.4 Resize Text | Text scales to 200 percent without loss of content or function |
| 1.4.10 Reflow | No two-dimensional scrolling at 320 CSS px width, except for content that genuinely needs a grid |
| 1.4.11 Non-text Contrast | UI component boundaries, icons, focus rings, and chart lines reach 3:1 |
| 1.4.12 Text Spacing | No clipping when line height is 1.5, paragraph spacing 2x font size, letter spacing 0.12em, word spacing 0.16em |
| 2.1.1 Keyboard | Every action is reachable and operable with a keyboard alone |
| 2.1.2 No Keyboard Trap | Focus can leave any component with the standard keys; Escape closes overlays |
| 2.2.2 Pause, Stop, Hide | Carousels, auto-refresh, and moving decoration can be paused or stopped |
| 2.4.3 Focus Order | Tab order follows a meaningful sequence, not the visual z-index accident |
| 2.4.7 Focus Visible | A visible focus indicator exists for every focusable element |
| 2.4.11 Focus Not Obscured (Minimum) | Sticky headers, footers, and cookie bars never fully cover the focused element |
| 2.5.7 Dragging Movements | Any drag interaction has a single-pointer alternative, such as tap plus arrows |
| 2.5.8 Target Size (Minimum) | Pointer targets are at least 24x24 CSS px, or adequately spaced |
| 3.2.6 Consistent Help | Help, contact, and support links keep the same location across pages when present |
| 3.3.7 Redundant Entry | Information already entered is auto-filled or selectable, never re-typed |
| 3.3.8 Accessible Authentication (Minimum) | No cognitive test for login; paste is allowed in password fields |

Target size: 24x24 CSS px is the AA floor (2.5.8). 44x44 CSS px is the recommended size and is the AAA level (2.5.5). Use 44x44 as the default for touch surfaces. Where 24x24 is not possible, the criterion's spacing, inline, user-agent, or essential exceptions apply; document which one.

### Choosing the fix

| Symptom | Fix |
| --- | --- |
| Click handler on a `div` | Replace with `button type="button"`; keep the click handler |
| Icon-only control with no name | Add a visible label, or `aria-label` plus `title` when space truly forbids text |
| Custom dropdown | Use a native `select` first; if impossible, implement the combobox pattern with full key handling |
| Toggle built from checkbox plus label | Keep the checkbox, style the label; do not remove the input |
| Modal built from a positioned div | Use `dialog` with `showModal()` or implement focus trap, Escape, and restore |
| Error text only in red | Add an icon, a text message, and `aria-describedby` |
| Two-column layout at 320px | Collapse to one column; do not shrink the text |
| Infinite marquee | Ship static, or add a pause control and honor `prefers-reduced-motion` |
| Placeholder used as label | Add a real `<label>`; placeholders are not labels |

## Implementation patterns

### Landmarks and headings

- One `main` per page. `header`, `nav`, `main`, `aside`, `footer` at top level; skip the landmark if it would be empty.
- One `h1` describing the page job. Headings descend without skipping levels: `h1` then `h2`, never `h1` then `h3` for style.
- Every `nav` gets a distinguishable accessible name when more than one exists: `aria-label="Primary"`, `aria-label="Breadcrumb"`.
- The first focusable element is a skip link targeting `main`, visible on focus.

```html
<a class="skip" href="#main">Skip to content</a>
<header>...</header>
<main id="main" tabindex="-1">...</main>
```

### Keyboard and focus

- Focus order follows DOM order. Do not use positive `tabindex`.
- Focus indicator: at least a 2px outline with 3:1 contrast against both the component and the background, plus an offset so it is not clipped by `overflow: hidden`.
- Never write `outline: none` without an equally visible replacement.
- Overlays: move focus in on open, trap it while open, restore it to the trigger on close.
- Composite widgets follow their pattern: arrows inside the widget, Tab to leave it.

### Names, roles, values

- Every control exposes a name, a role, and a current value or state. A checkbox exposes checked; a tab exposes selected; a disclosure exposes expanded.
- Decorative images use empty `alt=""`. Meaningful images describe purpose, not appearance.
- Live regions announce asynchronous changes: `aria-live="polite"` for status, `assertive` only for errors that block the task.
- Do not announce the same event twice from two regions.

### Forms and errors

- Every field has a visible `<label for>`. Required state is text plus `required`, not an asterisk alone.
- Hint text is linked with `aria-describedby`; it must not be the only description of the field.
- Validate on blur and on submit, not on every keystroke. Announce errors in a summary linked to each field, and keep user input after failure.
- Error text says what is wrong and how to fix it, in the field's own words.

### Zoom, reflow, motion

- Test at 200 percent browser zoom and at 320 CSS px viewport width. Text must reflow, not scroll sideways.
- Use `rem` for type and spacing so zoom works. Fixed `px` type fights 1.4.4.
- Respect `prefers-reduced-motion: reduce`: remove parallax, large transforms, and autoplay; keep instant state changes.

## Anti-patterns

- ARIA role bolted onto a non-semantic element while the native element was available.
- `tabindex="0"` on a `div` acting as a button, with no Enter or Space handling.
- Focus hidden behind a sticky header, toast, or cookie banner.
- Focus ring removed for aesthetics, leaving hover-only affordance.
- Color as the only signal for state, required fields, validation, or chart series.
- Custom select, date picker, or file input with no keyboard path and no announced value.
- Automated scan reported as "accessibility passed" with no keyboard or zoom pass.
- Lorem ipsum, empty links, or `href="#"` shipped in a release.
- Icon buttons whose only name is a tooltip that appears on hover.

## Verification

1. Run an automated scan (axe, Lighthouse accessibility, or equivalent) and record the specific rules that fired. Fix real violations; triage the rest with a reason.
2. Keyboard pass: Tab from the top, confirm skip link, visible focus in order, no trap, Escape closes overlays, focus returns to the trigger.
3. Zoom pass at 200 percent, then a 320 CSS px viewport: no horizontal page scroll, no clipped text, controls still reachable.
4. Contrast pass on text, borders, focus rings, and disabled states with a color picker: 4.5:1 and 3:1.
5. Target audit: list every interactive element and its computed size; flag anything under 24x24 CSS px without sufficient spacing.
6. Screen-reader spot check on one critical flow: landmarks, heading outline, form labels, error announcement, and status update.
7. Reduced-motion check with the OS setting on: no autoplay, no parallax, no large transitions.
8. Record evidence per criterion: command output, screenshot, or a one-line note of what was observed.

## Related

- `../checklists/accessibility.md` for the criterion-by-criterion audit table.
- `responsive.md` for reflow, breakpoints, and touch ergonomics.
- `ui-design.md` for contrast and type scale decisions at the design layer.
- `security-privacy.md` for auth flows that must also satisfy 3.3.8.
