# Responsive layout

Load when: a layout must hold from a 320px phone to a wide desktop, including zoom, long content, and translation.

## Principles

- Mobile-first. Write base styles for the narrow viewport, then add capability with `min-width` media queries. Max-width cascades grow fragile as widths multiply.
- Breakpoints are content-driven. Add one when the content breaks: text wraps badly, a row becomes unreadable, a target drops below the minimum. Device names are not a design reason.
- Reflow, not shrink. A layout that only reads at 1440px is not responsive, it is a desktop screenshot.
- Page-level horizontal scroll is a defect at every width. Contained scroll (tables, code, carousels) is a deliberate choice and needs a visible affordance.
- Pointer type is an input, not a device class. Laptops have touch screens; tablets have mice. Size targets for touch, keep hover optional.
- One spacing and type scale feeds all widths. Fluid values come from tokens, not scattered `clamp()` calls.

## Decision rules

| Situation | Rule |
| --- | --- |
| Choosing a breakpoint | Insert it where the layout visibly fails, then round to the nearest token width |
| Two layouts are possible | Prefer the one that keeps reading order and DOM order identical |
| Content is long or translated | Test with 1.3x text expansion before accepting the layout |
| Table has more than 6 columns | Choose priority columns or a card list per product, never both silently |
| Navigation exceeds 5 items on mobile | Use a labelled disclosure, not an unlabelled icon |
| Modal is taller than the viewport | Convert to a sheet with internal scroll and a fixed action bar |
| Chart labels collide | Drop series or move detail to tap, never shrink labels below 12px |
| Fixed footer or bar exists | Reserve space with padding plus `env(safe-area-inset-bottom)` |
| Any element above the primary action | Cap its height or move it below the action so the action stays fully visible in the first viewport at 390x844 |
| Primary action below the fold | Reduce the media, move the action into a sticky bar, or reorder the DOM |

### Layout transformations

| Component | Narrow | Wide | Constraint |
| --- | --- | --- | --- |
| Global nav | Disclosure menu or bottom bar | Horizontal bar with visible active state | Never hover-only; state survives navigation |
| Sidebar | Off-canvas sheet, closed by default | Persistent column | Location stays visible after closing |
| Data table | Priority columns plus row detail | Full table, sticky header | One strategy per product, documented |
| Filters | Sheet with apply and reset | Inline toolbar | Selections survive closing the sheet |
| Form | Single column, full width | Single column, 480-640px cap | Two columns only for genuinely paired fields |
| Modal | Full-height sheet | Centered dialog with max width | Focus trap and Escape work in both |
| Wizard | "Step 2 of 5" text | Step rail | Progress readable without color |
| Hero | Stacked, copy first | Side by side | Primary action above the fold in both |
| Footer | Accordion columns | Multi-column grid | Links reachable without JavaScript |
| KPI grid | One column, 2 minimum | 3 to 4 per row | Numbers never truncate mid-value |

## Implementation patterns

Fluid grid without media queries:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: var(--space-4);
}
```

Container query so a component adapts to its slot, not the viewport:

```css
.card-slot { container-type: inline-size; }
@container (min-width: 30rem) {
  .card { grid-template-columns: 8rem 1fr; }
}
```

- Relative units: `rem` for type and spacing, `%` and `fr` for layout, `ch` for measure. Keep line length at 45-75 characters.
- `clamp()` for one-dimensional fluid values only: `font-size: clamp(1.5rem, 1rem + 2vw, 2.5rem)`. Test at both ends.
- `aspect-ratio` reserves media space and prevents shift: `aspect-ratio: 16 / 9`.
- Viewport units: prefer `svh` and `dvh`; bare `100vh` overflows behind mobile browser chrome.
- Safe areas: `padding-block-end: max(var(--space-4), env(safe-area-inset-bottom))`.
- Images: `srcset` plus `sizes` matching the real rendered width, with `width` and `height` attributes set.
- Touch targets: 24x24 CSS px is the WCAG 2.2 AA floor (2.5.8), 44x44 is recommended and matches 2.5.5 AAA. Spacing can satisfy the floor only when a 24px circle does not overlap another target.
- Virtual keyboard: keep the focused field visible, avoid fixed footers over inputs, use `scroll-margin-block` on form fields.
- Test widths: 320, 375, 768, 1024, 1440 CSS px. Add 200 percent zoom, which must reflow without page-level horizontal scroll.

## Anti-patterns

- Breakpoints copied from a device list with no content reason.
- `overflow-x: hidden` on `body` used to hide a real overflow defect.
- Fixed pixel widths on containers, cards, or inputs.
- Two DOM orders for the same content, one per breakpoint, causing tab-order mismatch.
- Hiding navigation, filters, or primary actions on mobile with no visible entry point.
- Shrinking type below 16px to fit a layout instead of reflowing it.
- Sticky headers that consume more than 15 percent of a small viewport.
- Hover-only menus, tooltips, or row actions on touch devices.

## Verification

1. Load each width in the browser at 320, 375, 768, 1024, 1440 and record a screenshot per width.
2. Confirm `document.documentElement.scrollWidth` does not exceed the viewport width at each width.
3. Zoom to 200 percent at 1280px and confirm text resizes without loss (1.4.4). Then reflow to 320 CSS px (400 percent at 1280) and confirm no page-level horizontal scroll (1.4.10).
4. Tab through the page at 375px and confirm every target is reachable and at least 24x24 CSS px.
5. Open the virtual keyboard on each form field and confirm the field and its error text stay visible.
6. Switch to landscape and confirm safe-area padding keeps fixed bars off the notch and home indicator.
7. Repeat one long page with 1.3x text expansion and confirm no clipping or overlap.
8. At 390x844, confirm the primary action or entry point is fully visible without scrolling; record its top offset and the viewport height.

## Related

- `../checklists/responsive.md` for the pass/fail sweep.
- `accessibility.md` for reflow, target size, and zoom criteria.
- `ui-design.md` for the spacing and type scale used by fluid values.
- `performance.md` for image sizing and layout shift.
- `../patterns/mobile-pwa.md` for touch ergonomics and offline behavior.
