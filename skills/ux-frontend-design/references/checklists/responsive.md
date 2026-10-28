# Responsive checklist

When to use: when a layout must hold from 320 px to wide desktop and across input modes.
Severity: Blocker, Warning, Suggestion.

Blocker stops merge. Warning needs a recorded decision. Suggestion can follow.
Evidence is a measured width, a screenshot, or a captured viewport report.

| Check | Severity | Evidence |
| --- | --- | --- |
| No horizontal scroll at 320 CSS px | Blocker | `document.documentElement.scrollWidth <= clientWidth` measured at 320 |
| Primary action or entry point fully visible at 390x844 without scrolling | Blocker | Screenshot with the action above the fold and its measured top offset |
| Reflow at 400 percent zoom without two-dimensional scrolling (1.4.10) | Blocker | Screenshot at 1280 wide with 400 percent zoom, one scroll axis only |
| Text resize to 200 percent keeps all content and function (1.4.4) | Blocker | Screenshot at 200 percent text-only zoom, no clipped or lost element |
| Text spacing overrides do not break layout (1.4.12) | Warning | Screenshot with line height 1.5, paragraph spacing 2em, letter 0.12em, word 0.16em |
| Viewport meta omits `user-scalable=no` and `maximum-scale` | Blocker | Meta tag line from the document head |
| Breakpoints are content-driven, not device names | Warning | Comment per breakpoint naming the content pressure that forces it |
| Navigation transformation defined at every breakpoint | Blocker | Per-width screenshot of the header: inline, condensed, disclosure, or drawer |
| Table strategy chosen per width: scroll, stack, or detail row | Blocker | Screenshot of the table at 320 and 768 plus the chosen strategy in code |
| Forms use a single column with labels above inputs on narrow widths | Warning | Screenshot of a completed form at 320 and at 768 |
| A modal taller than the viewport becomes a sheet with internal scroll and a fixed action bar | Blocker | Screenshot of the open overlay at 375 and at 768 |
| Sticky headers, footers, and toolbars never cover focused content (2.4.11) | Blocker | Keyboard pass screenshot of the last field with the sticky bar visible |
| Safe areas respected on notched devices via `env(safe-area-inset-*)` | Warning | Computed padding on the fixed bar in a notched emulation |
| Virtual keyboard does not cover the focused input | Blocker | Mobile emulation screenshot with the keyboard open and the caret visible |
| Orientation change keeps state, scroll position, and open overlay | Warning | Portrait to landscape recording of the same screen |
| Touch targets measure at least 24x24 CSS px (2.5.8) | Blocker | Bounding box measurements of each interactive element |
| Primary mobile actions reach 44x44 CSS px (recommended, 2.5.5 is AAA) | Suggestion | Bounding box measurements for primary controls only |
| Adjacent targets are separated enough to avoid mis-taps | Warning | Measured gap in px between each neighboring target pair |
| No hover-only affordance without a touch equivalent | Blocker | Interaction inventory listing the trigger for each hidden action |
| Nested scroll regions do not trap scroll on touch | Warning | Recording of a swipe inside each inner scroll area |
| Long translations with 30 percent text growth still fit | Warning | Screenshot with the longest translated string substituted |
| Large text setting of the operating system does not clip labels | Warning | Screenshot at 200 percent system font scale |
| Images use `srcset` and `sizes` and never upscale past intrinsic width | Warning | Image element markup plus the largest rendered width |
| Charts re-layout and axis labels stay readable at 320 px | Blocker | Screenshot of each chart at 320 and 1440 |
| No fixed height clips content when text grows | Blocker | Grep of fixed heights on text containers in the diff |
| Container queries or media queries used consistently for one component | Suggestion | Component stylesheet showing one mechanism per component |
| Reduced motion honored for scroll, parallax, and transitions | Blocker | Screenshot or recording with `prefers-reduced-motion: reduce` forced |
| Scrolling works with keyboard, wheel, and touch at every width | Warning | Short recording per input mode |
| Print or export layout does not cut primary content | Suggestion | Print preview PDF of one representative page |

## How to run

1. Start the preview build and open each changed route at 320, 375, 390, 768,
   1024, and 1440 CSS px.
2. In the console on each width run
   `({w: document.documentElement.clientWidth, s: document.documentElement.scrollWidth})`
   and record the pair. `s` greater than `w` is a Blocker.
3. Repeat with 400 percent zoom at a 1280 px viewport, then with text-only zoom
   at 200 percent.
4. Walk the page with `Tab` only. Capture the focus ring on the first and last
   field with any sticky bar in view.
5. In device emulation open the virtual keyboard on a text input at 375 px and
   capture the caret and the submit control together.
6. Measure each target with
   `el.getBoundingClientRect()` and record width and height in CSS px.
7. Substitute the longest translated string per label and capture the screen.

## Pass criteria

- No width in the set produces horizontal overflow.
- At 390x844, the primary action or entry point is fully visible without scrolling.
- Zoom and text-spacing passes lose no content and keep every control usable.
- Every target clears 24x24 CSS px; primary mobile actions reach the
  recommended 44x44 CSS px or the deviation is recorded.
- Navigation, tables, forms, and overlays each have a stated narrow-width
  strategy visible in a screenshot.
- Focused content is never hidden behind a sticky region.
- Measurements and screenshots are stored with the review.

## Related

- `../knowledge/responsive.md` for breakpoint, grid, and container query rules.
- `visual-review.md` for the full screenshot and state pass.
- `accessibility.md` for reflow, target size, and focus criteria.
