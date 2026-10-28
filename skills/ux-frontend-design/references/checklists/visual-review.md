# Visual review checklist

When to use: after the interface renders, before merge, on every screen the diff touches.
Severity: Blocker, Warning, Suggestion.

Blocker stops merge. Warning needs a decision recorded in the pull request.
Suggestion is polish that can follow. Evidence is a file name, a measured
number, or a console line - never an adjective.

| Check | Severity | Evidence |
| --- | --- | --- |
| Screenshots captured at 320, 375, 768, 1024, and 1440 CSS px | Blocker | Five image files named by width in the review folder |
| Light mode captured for every touched screen | Blocker | One image per screen, same scroll position as the reference |
| Dark mode captured when the project ships dark mode | Warning | Paired images per screen, light next to dark |
| Default, hover, focus, and active captured for interactive controls | Blocker | State grid per control, one row per state |
| Disabled state distinct yet still legible | Warning | Disabled control screenshot plus measured contrast of its label |
| Loading state reserves the final layout space | Blocker | Skeleton screenshot and the measured delta of layout shift |
| Empty state names the cause and the next action | Blocker | Screenshot plus the exact empty-state copy |
| Error state names the field, the cause, and the fix | Blocker | Screenshot plus the error string and its element |
| Partial state shown for slow or failed secondary data | Blocker | Screenshot with one region degraded, others intact |
| No clipped text or cut controls at any captured width | Blocker | Per-width screenshot with the last character of each label visible |
| Page-level horizontal overflow at 320 | Blocker | Probe output: scrollWidth equals clientWidth |
| Primary action or entry point fully visible at 390x844 without scrolling | Blocker | Screenshot with the action above the fold and its measured top offset |
| No overlapping elements, including sticky bars, toasts, and dialogs | Blocker | Screenshot of the collision plus the offending z-index values |
| Shared left edges and baselines hold across the screen | Warning | Screenshot with alignment guides or measured offsets in px |
| Spacing matches the project scale, with no one-off values | Warning | List of spacing values used by the diff against the token scale |
| No orphan heading at the end of a scroll region | Suggestion | Screenshot of the heading with its following content below the fold |
| Text wraps without mid-word break or stray hyphen | Warning | Screenshot at the narrowest width where the line breaks |
| Images keep aspect ratio, with no distortion or upscaling blur | Blocker | Rendered width and height compared with the intrinsic size |
| Layering of dialog, dropdown, tooltip, and toast is predictable | Blocker | Screenshot of the stack plus the z-index map |
| Console has no new errors and no new warnings | Blocker | Console export filtered to the page session |
| Network panel shows no failed request and no 4xx or 5xx from the page | Blocker | Network export with status column visible |
| Focus ring is visible on every focusable element on both backgrounds | Blocker | Screenshot of each focus stop, or a keyboard pass recording |
| One primary action per decision region; hierarchy survives grayscale | Warning | Grayscale screenshot with the intended primary marked |
| Body line length stays between 45 and 75 characters | Suggestion | Measured character count on the widest body paragraph |
| Contrast measured over images and gradients, not only solid fills | Blocker | Measured ratio at the worst pixel behind the text |
| One icon family, no emoji used as a professional icon | Warning | Icon inventory with source library per icon |
| Shadow, radius, and border values come from tokens | Warning | Grep result for raw values in the changed files |
| Before and after screenshots exist for every changed view | Blocker | Paired images per view at one shared width |
| Diff is visually scoped; unrelated screens unchanged | Warning | Screenshot diff count limited to the touched views |
| Screenshots taken at device pixel ratio 1 and 2 to catch hairlines | Suggestion | Two captures of the same border-heavy component |
| Real content rendered, no shipped placeholder text | Blocker | Screenshot plus the string inventory of placeholder markers |
| Primary call to action label not truncated | Warning | Full label visible at 320 px, measured label width |

## How to run

1. Confirm the dev server or preview build is the code under review, then open
   the changed routes in a fresh profile with cache disabled.
2. Set the device toolbar to each width in the table: 320, 375, 768, 1024,
   1440. Capture the full page, not only the viewport, and name files
   `screen-width-theme-state.png`.
3. Toggle light and dark mode using the project mechanism, not a forced browser
   flag, and capture the pairs.
4. Walk every state in the table with the pointer and again with the keyboard.
   For loading, throttle the network to a slow profile so the state is visible.
5. Read the console and the network panel, filter to the page session, and
   export both.
6. Compare before and after captures at one shared width. Mark each difference
   as intended or defect.
7. Write each Blocker as one line: `[Blocker] screen/width - defect - fix`.

## Executable probes

Run in the page console at 320 px:

```js
const de = document.documentElement;
const bad = [...document.querySelectorAll("body *")]
  .filter(el => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && (r.right > de.clientWidth + 1 || r.left < -1);
  })
  .map(el => el.tagName + "." + String(el.className).slice(0, 40));

({ scrollWidth: de.scrollWidth, clientWidth: de.clientWidth, bad });
```

Run at 390x844. Replace the selector with the primary action or entry point:

```js
const cta = document.querySelector("[data-primary-action]");
const r = cta?.getBoundingClientRect();
({ visible: !!r && r.top >= 0 && r.bottom <= innerHeight, top: r?.top, vh: innerHeight });
```

If the project does not use `data-primary-action`, use the visible primary CTA.

## Pass criteria

- Zero Blocker rows open.
- 320 px probe reports `scrollWidth` equal to `clientWidth` with an empty `bad` list.
- At 390x844, the primary action or entry point is fully visible without scrolling.
- Every Warning has a recorded decision: fix now, accept with a reason, or
  defer with a date and an owner.
- The five widths, both themes, and the full state set have captures stored
  where the reviewer can open them.
- Console and network exports show no new errors, warnings, or failed requests.
- Focus ring is visible on every stop in the keyboard recording.
- No unrelated screen appears in the before and after diff.

## Related

- `interface-critique.md` for the same judgement before code exists.
- `responsive.md` for width behavior, reflow, and target size.
- `accessibility.md` for keyboard, contrast, and screen-reader evidence.
