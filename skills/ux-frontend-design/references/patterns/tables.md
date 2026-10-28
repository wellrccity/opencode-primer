# Tables

Use when: building or reviewing any tabular data surface - a report, a record
list, an admin grid, or an export view.

## Layout and hierarchy

- Every column answers a question the reader asks; if nobody sorts, filters, or
  acts on it, drop it or move it into a detail view.
- Order: identifier, decision-driving values, status, timestamps, actions last.
  Keep the identifier visible when scrolling horizontally.
- Text left, numbers and currency right, dates left in one stable format,
  booleans as words rather than icon alone; align each header with its values,
  since a centered header over right-aligned numbers reads as another column.
- Formatting is explicit: one locale, one decimal rule, sign for negatives, and
  tabular figures so digits do not shift between rows.
- Title, active filter summary, and result count sit above the grid; pagination
  sits below it. Density is a user setting, not a way to squeeze in columns.

## Required states

- Loading: skeleton rows matching column widths, not a collapsing spinner.
- Empty with no data: say what the table holds and offer the creating action.
  Empty after filtering: name the filters, offer "Clear filters", keep the
  controls visible.
- Error: message in the table body plus retry; never replace good data with
  zeros.
- Partial: failed rows are marked per row, not as a whole-table failure.
- Row states: default, hover, focused, selected, editing, invalid - each
  distinct and never by color alone.

## Interaction rules

- Sorting is explicit: clickable header, `aria-sort`, visible direction, and a
  stable tiebreaker so equal values do not reshuffle.
- Filters persist in the URL, state their scope, and show the count before and
  after filtering.
- Paginate record sets users scan and revisit. Treat 100 or more rendered rows
  as a signal to measure row height and scroll cost, not an automatic trigger
  to virtualize. Pair virtualization with search because find-in-page breaks.
- Selection: the header checkbox selects the current page and says so; the bulk
  bar shows the count and destructive actions confirm and name the target
  ("Archive 12 records"), with undo preferred over a dialog.
- Inline edit opens from an explicit control, not one click on the cell; Save
  and Cancel are reachable and Escape cancels.
- Sticky headers stay opaque and never cover the focused cell (WCAG 2.2
  2.4.11).
- Rows link or expose one primary action; a whole-row click target that also
  holds buttons steals clicks.

## Data and edge cases

- Long text truncates with a title or an expandable row; numbers never truncate
  silently.
- Null renders as a deliberate placeholder, distinct from zero and from an
  empty string.
- Dates declare time zone; totals and exports declare scope (page or filtered
  set), and exports state the applied sort.
- Concurrent updates show a stale marker and a refresh, and never overwrite a
  row the user is editing. Optimistic edits keep the old value until the server
  confirms, then roll back visibly on failure.

## Accessibility

- Use a real `table` with `caption`, `th`, and `scope` for tabular data (WCAG
  1.3.1); grid layouts lose header association.
- The scroll container is focusable with `tabindex="0"` and an accessible name
  so keyboard users can scroll it (2.1.1).
- Sortable headers are buttons inside the `th` and expose `aria-sort`.
- Selection checkboxes have names including the row identifier; build a
  roving-tabindex grid only when cells are interactive, else keep native table
  navigation.
- Focus stays visible on rows and header buttons (2.4.7); targets are at least
  24x24 CSS px (2.5.8), 44x44 recommended on touch.
- Result count and sort changes are announced in a polite live region.

## Performance

- Render the first page server-side and hydrate filters and sorting only.
- Measure before virtualizing: a plain table of a few hundred rows is often
  faster than a virtualization layer.
- Keep row components cheap - no per-row date libraries, observers, or inline
  closures - and debounce filter input, cancel stale requests, ignore
  out-of-order responses.
- Reserve column widths and row height so loading and error states do not shift
  layout (CLS 0.1 or less).

## Anti-patterns

- A table used for page layout, or divs used for tabular data.
- Center-aligned numbers or mixed decimal formats in one column.
- Zebra striping plus hover plus selection with no focus state.
- Pagination that resets filters, sort, or scroll position.
- A header checkbox that silently selects rows on every page.
- Inline edit that saves on blur with no cancel path.
- Horizontal scroll in a container keyboard users cannot reach.
- Totals from the visible page labeled as the full set.

## Checklist

- [ ] Every column has a header and a stated purpose; unused ones removed.
- [ ] Numeric columns right-aligned, one locale, stable figure width.
- [ ] Sorting sets `aria-sort`, shows direction, and survives reload via URL.
- [ ] Filters show the active set, the result count, and a clear action.
- [ ] Empty, filtered-empty, loading, error, and partial states exist.
- [ ] Keyboard: container scrolls, headers activate, cells edit, Escape cancels.
- [ ] Focus stays visible under a sticky header at 200 percent zoom.
- [ ] Bulk selection states its scope and confirms destructive actions.
- [ ] 320px width: rows become labeled blocks with no lost values.
- [ ] Screen reader announces table name, headers, sort, and row count.
- [ ] Export scope, sort, and time zone match what the user sees.
