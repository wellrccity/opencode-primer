# Dashboard (SaaS)

Use when: building or reviewing an authenticated product surface whose job is
to answer recurring questions and drive a decision, not to display data.

## Layout and hierarchy

Rule: every widget answers a named question and points to an action. Write the
question in the widget subtitle or the design note; if no question exists,
remove the widget.

| Zone | Contents | Constraint |
| --- | --- | --- |
| Global navigation | Workspace switcher, product areas, account | One row, stable across routes |
| Local navigation | Sections inside the current area | Max one level of nesting |
| Header | Page title, date range, primary action | Primary action singular |
| KPI row | 3 to 5 headline metrics | Same unit and period across cards |
| Body | Charts, tables, activity | Ordered by decision value |
| Detail panel | Drill-down for a selected item | Does not replace the list |

Density: default to compact. Use a comfortable variant only for onboarding
screens. Fixed heights for charts prevent layout shift when data arrives.

## Required states

- Loading: skeleton that matches the final layout; no full-page spinner.
- Empty (no data yet): explains how data arrives and the first action.
- Empty (filtered to zero): states the active filters and offers reset.
- Partial: some widgets failed; the failed widget shows a retry, the rest
  still render.
- Error: message plus retry; the error does not clear other panels.
- Stale: last updated timestamp visible when data is cached or delayed.
- Permission-limited: hidden or disabled with a reason, never a silent blank.
- Long values: a 60-character metric label and a 1,000,000.00 number both fit
  without clipping at 1024px.

## Interaction rules

- Filters live in the URL so a view is shareable and back/forward works.
- Changing a filter updates only the dependent widgets; unrelated widgets do
  not flicker.
- Date range control states the timezone and whether the range is inclusive.
- Saved views store filters, sort, columns, and density; default view is
  explicit, not "last used" unless the user chose that.
- Chart hover shows values; keyboard focus reaches the same values (see
  Accessibility).
- Export offers CSV and the current filter set; the file name includes the
  range.
- Real-time updates never reorder a list under the pointer. Buffer new rows
  behind a "N new items" control.
- Onboarding is a checklist with real completion state, dismissible, and not
  a blocking tour on first load.

## Data and edge cases

- Every metric shows unit, period, and comparison baseline ("vs previous 7
  days"), or the comparison is omitted.
- Percentages over 100, negative values, nulls, and single-point series have
  defined rendering: `-` for missing, never a fake zero.
- Time zones: display in the user's zone, label it, and keep the stored value
  in UTC.
- Currency and number formatting use the user's locale, not string
  concatenation.
- Permissions: the UI reflects role, but the API enforces it. A hidden widget
  is not a security control.
- Large result sets paginate or virtualize; counts show total when known and
  "500+" when capped.

## Accessibility

- Each chart has a text summary and a data table alternative, or the table is
  the chart.
- Chart colors are distinguishable by more than hue; series carry direct
  labels or a legend with patterns (WCAG 2.2 1.4.1).
- Data tables use `th` with `scope`, a caption, and sortable headers exposing
  `aria-sort`.
- Loading regions use `aria-busy`; async updates announce via a polite live
  region, not on every tick.
- Keyboard: filters, tabs, chart drill-down, and table sort all reachable;
  focus visible and never trapped in a popover.
- Contrast 4.5:1 for text, 3:1 for chart lines and card borders against the
  surface (1.4.11).

## Performance

- Initial data request returns only the visible viewport's aggregates; detail
  loads on demand.
- No layout shift from charts or images; reserve dimensions.
- Virtualize lists past roughly 100 rows and measure rather than guess.
- Polling intervals are documented; prefer push when the backend supports it.
- Target: INP 200 ms or less at the 75th percentile (Core Web Vitals). Filter
  changes must feel immediate with an optimistic or cached render.

## Anti-patterns

- Dashboard theater: gauges, sparklines, and counters with no decision behind
  them.
- Twelve KPI cards where four would answer the question.
- Dual-axis charts and truncated axes that exaggerate change.
- Pie charts with more than four slices.
- Auto-refresh that resets scroll position or selection.
- Modal dialogs for information that belongs inline.
- Filters that apply only after a separate "Apply" click without a reason.
- Red/green as the only signal for up or down.

## Checklist

- [ ] Each widget has a written question and an action; none is decorative.
- [ ] KPI count is 5 or fewer on the default view.
- [ ] All eight states implemented: loading, empty, filtered-empty, partial,
      error, stale, permission-limited, long values.
- [ ] Filter state survives reload and browser back.
- [ ] Empty state names the first action and links to it.
- [ ] Every chart has a table or text alternative reachable by keyboard.
- [ ] Table headers expose sort state and sort works from the keyboard.
- [ ] 1024px width: no horizontal page scroll; table scrolls in its own
      container.
- [ ] Role-restricted widget verified with a lower-privilege account; API
      returns 403 independently of the UI.
- [ ] Screenshot at 1440px and 1024px reviewed for alignment and clipping.
- [ ] Filter-to-render time measured in the performance panel and recorded.
- [ ] Console and network clean after a filter change and a real-time update.
