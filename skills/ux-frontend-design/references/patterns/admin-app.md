# Admin App

Use when: building or reviewing an internal back-office tool where trained
staff repeat high-volume operations and mistakes are expensive.

## Layout and hierarchy

- Shell order: collapsible side navigation, top bar with global search or
  command palette, content region, optional right detail panel. Keep the shell
  stable so muscle memory survives navigation.
- List-first screens: the table or queue is the page. Filters sit directly
  above it, counts next to the filter that produced them.
- Detail as a panel or separate route, not a modal, once the form has more
  than about five fields.
- One primary action per screen. Destructive actions are separated spatially
  from the safe path and never the default focus target.
- Density: compact rows by default for scanning tasks; offer an explicit
  density toggle instead of guessing. Row height around 32-36 CSS px is a
  recommendation, not a rule.
- Persistent context in the header: environment badge (staging versus
  production), current tenant or account, and the signed-in role.

## Required states

- Default, hover, focus-visible, selected, and disabled for every row action.
- Loading: skeleton rows that match final row height; no layout jump.
- Empty: distinguish "no records yet" from "no results for these filters",
  and offer the matching next action (create versus clear filters).
- Error: inline message with the failing request id and a retry control.
- Partial: rows the current role cannot read render as restricted, not blank.
- Pending: optimistic updates show a pending marker on the affected row until
  the server confirms or rejects.
- Conflict: a second editor changed the record; show both versions.
- Session expiry: preserve the unsaved draft and resume after re-auth.

## Interaction rules

- Keyboard: `Ctrl`/`Cmd+K` opens the command palette; `?` lists shortcuts;
  `/` focuses search; `Esc` closes the topmost layer only.
- Command palette actions and navigation, not only static links. Each entry
  states scope ("Archive 3 orders").
- Every shortcut has a visible equivalent. No feature is shortcut-only.
- Inline edit: click or `Enter` enters edit, `Enter` commits, `Esc` cancels
  and restores the previous value; show the saved value on failure.
- Bulk edit: selection toolbar states the count and the scope. When filters
  are active, offer "select all N matching" as a separate explicit choice.
- Undo window for soft deletes and bulk edits, roughly 5-10 seconds
  (recommendation). Undo is a toast with the action name and an undo button.
- Confirmation thresholds:

  | Operation | Treatment |
  | --- | --- |
  | Reversible single row | Execute, offer undo |
  | Reversible bulk | Confirm with count, offer undo |
  | Irreversible single | Confirm with the record name typed or checked |
  | Irreversible bulk or financial | Review step, scope count, explicit confirm |

- Never stack a confirmation dialog inside another dialog.
- Audit trail: every write records actor, timestamp, before and after values,
  and request id. Surface it on the record, not only in a separate report.

## Data and edge cases

- Deep-link filters, sort, page, and selection scope into the URL so a view
  can be shared and restored.
- Saved filters are user-owned, named, and deletable; show which one is
  active.
- Pagination with a stable sort key. Cursor pagination when the dataset
  changes during review; offsets drift.
- Concurrent edits: send the record version or updated-at value and reject
  stale writes with a diff, not a silent overwrite.
- Masks and permissions: hide a field only as UX; the server still enforces
  read access.
- Role change mid-session: refresh capabilities and drop actions that are no
  longer allowed.
- Long values: IDs, emails, and file names wrap or truncate with a copy
  control, never widen the layout.
- Export runs the same query as the view and records its parameters.

## Accessibility

- Tables use real `th` elements with `scope`; sortable headers expose
  `aria-sort` and are buttons inside the header cell.
- Row selection uses a checkbox with an accessible name that includes the
  record identifier.
- Focus moves into an opened panel and returns to the trigger on close.
- No keyboard trap in dialogs, palettes, or nested panels; `Esc` always
  closes the topmost layer.
- Shortcuts do not fire while focus is in a text field, and single-key
  shortcuts can be disabled (WCAG 2.2 2.1.4).
- Icon-only buttons carry an accessible name and a tooltip; the tooltip is
  not the only label.
- Target size at least 24x24 CSS px (2.5.8); 44x44 recommended for touch
  terminals.
- Status changes are announced through a live region; errors are not
  color-only.

## Performance

- Virtualize or paginate once a table renders beyond roughly 200 rows
  (recommendation); measure before choosing.
- Inline edit patches one row in local state instead of refetching the list.
- Keep row keys stable across sorts and filters so focus and selection hold.
- Debounce search input (300 ms is a common recommendation) and cancel
  in-flight requests on change.
- Do not mount hidden panels, palettes, or chart libraries until opened.
- Budget the heavy admin dependencies (rich text, date pickers, charts) and
  load them per route.

## Anti-patterns

- Multi-field records edited in a modal.
- Confirmation dialogs on every action, which trains reflexive clicking.
- Icon-only toolbars with unlabeled glyphs from mixed icon families.
- Hover-only row actions, unreachable by keyboard or touch.
- Silent destructive actions with no undo and no audit entry.
- Bulk actions that apply to the whole dataset while the label says the page.
- Nested cards and card-wrapped tables that reduce information density.
- Dropdowns used for fewer than about five options that could be radio
  buttons or segmented controls.
- Disabled buttons with no explanation of the missing prerequisite.
- Toasts that report success without the resulting record state.

## Checklist

- [ ] Primary action per screen identified; destructive actions separated.
- [ ] `Ctrl`/`Cmd+K` palette opens, lists actions, and closes with `Esc`.
- [ ] Shortcut list reachable from the UI, and every shortcut has a visible
      equivalent control.
- [ ] Inline edit commits with `Enter`, cancels with `Esc`, restores on error.
- [ ] Bulk scope label states the count and whether it covers all matches.
- [ ] Bulk and irreversible operations match the confirmation table.
- [ ] Undo available for soft deletes and reversible bulk edits.
- [ ] Audit entry shows actor, timestamp, before and after values.
- [ ] Empty state distinguishes no data from no matches, each with an action.
- [ ] Filters, sort, page, and saved view survive reload via the URL.
- [ ] Keyboard-only pass completes one create, one edit, one delete.
- [ ] Opened panel traps nothing; focus returns to the trigger on close.
- [ ] Table renders 500 rows without freezing interaction on the target
      device; measurement recorded.
- [ ] Console and network show no errors after the keyboard pass.
