# Navigation

Use when: designing or reviewing site or app navigation - global menus, local
sidebars, tabs, breadcrumbs, mobile drawers, search, or command palettes.

## Layout and hierarchy

- Model destinations before styling them: group by user task, name groups in
  the user's words, keep depth shallow enough that labels need no explanation.
- Global navigation carries top-level destinations; local navigation carries
  peers inside the current section. Mixing both in one bar makes each ambiguous.
- Keep global navigation in the same position on every page, local navigation
  inside the content region it scopes. Breadcrumbs show hierarchy, not history,
  and end with the current page as plain text.
- Tabs are peer views of one object. Use links with tab styling when each view
  deserves a URL; a real tablist only for local panels without URLs.
- Sidebars hold many peers, filters, or saved views. Collapse persists as a user
  choice, and a collapsed sidebar is never the only path to a destination.
- Mobile: a bottom bar for primary destinations (a recommendation, not a rule),
  a drawer for the rest, and search in the header.
- The current item is unique, visible without hover, and marked with
  `aria-current="page"` (or `"true"` for a view toggle).
- URL is state: tabs, filters, search, and open records belong in the URL so
  back, forward, refresh, and shared links restore the same view.
- Overflow goes into a labeled "More" menu with hidden destinations still
  reachable, and the skip link is the first focusable element, targeting main.

## Required states

- Per item: default, hover, focus, active, current, disabled or locked. Locked
  items stay visible with a reason when the path matters.
- Expanded and collapsed for menus, drawers, and disclosure groups, with the
  trigger exposing `aria-expanded`.
- Mobile drawer: closed, open, and closing, with background scroll locked and
  focus contained while open.
- Search: idle, typing, results, no results with a recovery hint, and error.
- Unauthorized items are hidden rather than failing on click, and the
  navigation height is reserved so a mounted menu does not shift the page.

## Interaction rules

- Tab order follows visual order and the first Tab reaches the skip link;
  Escape closes menus and drawers and returns focus to the trigger.
- Arrow keys move inside menus and tablists, Tab moves out, and no focus trap
  exists in a non-modal menu (WCAG 2.1.2).
- Triggers are buttons with `aria-expanded` and `aria-controls`. Submenus open
  on click or focus, never on hover alone, which fails touch and keyboard users.
- A command palette is an accelerator, not the only route: every action it
  exposes is also reachable through visible UI.
- Search states its scope ("Search orders") and shows recent or suggested
  queries instead of an empty box.
- Deep links to missing or protected records redirect while keeping the intended
  destination, or answer with a clear 404 and a way back.

## Data and edge cases

- Long labels wrap to two lines before truncating, and truncation keeps the full
  text in a title or accessible name. Allow 30 percent label growth for
  localization, test the longest locale, and mirror the layout for RTL.
- Permission changes mid-session remove destinations without breaking the
  current page: explain it and offer a safe landing route.
- Renamed routes keep redirects so old deep links still resolve.
- Too many destinations is a grouping problem, not a reason to shrink type or
  targets. A group with one child is flattened, not rendered as a menu.

## Accessibility

- Wrap each navigation region in `nav` with a distinct `aria-label` when more
  than one exists (WCAG 1.3.1, 2.4.1).
- Render menus as lists; the current page uses `aria-current`, not color alone
  (1.4.1).
- Focus stays visible (2.4.7), is never hidden behind a sticky header or drawer
  edge (2.4.11), and toggling a drawer announces the change.
- Targets are at least 24x24 CSS px (2.5.8); 44x44 recommended on mobile bars.
- Icon-only triggers carry an accessible name; decorative icons are hidden.
- At 320px width and 200 percent zoom the navigation reflows with no horizontal
  scroll (1.4.10).

## Performance

- Ship navigation markup in the initial HTML so links work before hydration and
  layout does not shift. Prefetch on intent (hover, focus, viewport), not every
  route.
- Let CSS handle overflow and transforms for drawers, with no layout-thrashing
  measurement on open.
- Interaction response stays within the INP threshold of 200 ms at the 75th
  percentile; defer non-critical work until after the menu opens.
- Prefer native `details`, `dialog`, and `popover` over a component library for
  one dropdown.

## Anti-patterns

- Hover-only dropdowns, or mega menus that close on the diagonal path.
- Breadcrumbs built from browser history.
- Tabs implemented as buttons, breaking back, refresh, and deep links.
- A hamburger that hides all navigation at desktop widths.
- Two current items at once, or current state shown only on hover.
- Search that quietly covers one entity type while looking universal.
- A command palette as the only way to reach a feature.
- Navigation order that changes between pages, or locked items with no
  explanation of how to unlock them.

## Checklist

- [ ] Every destination is reachable in three interactions or fewer.
- [ ] Global and local navigation are visually and semantically distinct.
- [ ] Exactly one item is current per region and marked with `aria-current`.
- [ ] Back, forward, refresh, and a pasted URL restore the same view.
- [ ] Keyboard: skip link first, Escape closes, focus returns to the trigger.
- [ ] Menus open on click or focus and work with no hover.
- [ ] Mobile drawer locks background scroll and contains focus while open.
- [ ] 320px width and 200 percent zoom: no horizontal scroll, no lost items.
- [ ] The longest locale label fits without clipping or shrinking targets.
- [ ] Unauthorized destinations are hidden or explained, never failing on click.
- [ ] Screen reader announces landmarks, the current item, and expansion state.
