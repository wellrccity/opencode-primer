# Consumer App Home (map-first)

Use when: building or reviewing the first screen of a ride-hailing, delivery,
or courier app, where the map is context for a search-led task.

## Layout and hierarchy

- Primary entry is the destination or search field: first in reading order and
  first in the DOM.
- Saved places and recents sit directly under the field and fill it in one tap;
  they support the field, never replace it.
- The map is context, not the hero. It shows the area and pins while task
  controls keep the higher visual weight.
- Cap map height so that at 390x844 the search field, or the primary action of
  the current state, is visible without scrolling.
- A bottom sheet carries the next step: options, quote, confirmation, trip
  state. Two detents, peek and expanded, are enough.
- Keep one primary action per state in a fixed slot so its position stays
  stable within that state; re-check the position when the sheet detent
  changes.

## Required states

- Idle: field, saved places, recents, area availability.
- Suggestions: typed query with a loading row and a preview of the highlight.
- No results: restate the query, offer map pin drop, keep typing possible.
- Quote loading: skeleton keeps option rows and the price column width.
- Quote ready: at least two options with price, ETA, and vehicle type.
- Partial or degraded: quote or trip data is stale or one region failed; mark
  freshness and keep the rest usable.
- No service or no drivers: state the limit, offer the next area, and show only
  a measured wait or a timestamped range; never invent driver counts.
- Confirming: request sent, cancel allowed until assignment, elapsed time
  visible.
- Assigned, arriving, in trip: driver or courier card with name, rating,
  vehicle and plate or order id, ETA, contact, share, safety.
- Completed: receipt, total, tip, rating, and the trip in history.
- Cancelled: reason recorded, any fee stated before confirmation, rebook path.
- Offline: last screen kept, actions disabled, queued work explained.
- Location denied: manual entry as the fallback, with permission instructions.
- Payment failed: the request is kept, a backup method offered, the trip not
  lost.

## Interaction rules

- Ride or delivery option always takes an explicit selection; no silent
  auto-select and no pre-highlighted upgrade.
- A single available option may be preselected only when the screen says so.
- Cancel confirms, states any fee before it applies, and keeps the trip
  recoverable.
- Live regions announce assignment, arrival, and status changes politely.
- The sheet supports drag and keyboard: Escape collapses, arrow keys move
  detents, and a labelled handle button repeats the drag action.
- Sheet state lives in the URL or history so back closes the sheet instead of
  leaving the app.
- Contact, share ETA, and safety are one tap from the active trip card, which
  restates destination, price, and payment method before confirming.

## Data and edge cases

- Ambiguous address: disambiguated options with city or postcode, never a
  silent pick.
- Stale ETA: mark the timestamp and refresh; an old ETA is never shown as live.
- Surge: state the multiplier before option selection, not at confirmation.
- Unavailable option: keep the row visible and disabled with the reason.
- Payment failure or network loss: preserve the draft request and retry
  idempotently.
- Permission denied: manual entry plus a settings link, without re-prompting on
  every visit.

## Accessibility

- The address list is the map alternative: text-first, searchable, no drag.
- Focus order follows the task: field, saved places, suggestions, options,
  primary action.
- Targets at least 24x24 CSS px (2.5.8); 44x44 for contact, share, safety,
  cancel.
- Status changes carry text and icon, never color or pin movement alone
  (1.4.1), and focus is never hidden under the sheet (2.4.11).
- Reduced motion removes pin drop and sheet spring; state changes stay instant
  and announced.
- Zoom 200 percent keeps field, options, and price readable without sideways
  scroll (1.4.10).

## Performance

- The map loads lazily or after first paint; tiles never block the search field.
- A static placeholder holds the map slot so nothing shifts when tiles arrive.
- Suggestions are debounced and abortable; a stale response never replaces a
  newer one.
- The quote request starts after explicit selection, with a skeleton that
  reserves its height; ETA updates patch the status line and card only.
- Measure LCP at 390x844 with throttling before and after the change.

## Anti-patterns

- Map filling the first viewport and pushing search below the fold.
- Fabricated nearby drivers or supply counts used as urgency.
- Fees revealed only at confirmation, or a price without currency.
- Cancel buried, small, or replaced by a support contact.
- Auto-selected premium ride or delivery option.
- Promo, onboarding, or login wall before the search field.
- Re-centring the map and stealing focus while the user types an address.

## Checklist

- [ ] Search field or primary action visible at 390x844 without scrolling.
- [ ] No horizontal overflow at 320 CSS px.
- [ ] Suggestions, no results, quote loading, and quote ready reachable by
      forcing the state.
- [ ] No service, location denied, offline, and payment failed each show a
      recovery action.
- [ ] Confirming, assigned, arriving, in trip, completed, and cancelled each
      have a reachable state and a next action.
- [ ] Option selection is explicit; no premium default.
- [ ] Surge is stated before selection; stale ETA carries a timestamp;
      ambiguous addresses are disambiguated.
- [ ] Cancel shows confirmation and any fee before it takes effect.
- [ ] Active trip card exposes contact, share, and safety in one tap.
- [ ] Loading reserves space and CLS stays under the project threshold.
- [ ] Keyboard-only run completes search through cancellation; Escape closes the
      sheet.
- [ ] The address list completes the same task with the map hidden.

## Related

- `../knowledge/ux.md` for task flow and state coverage.
- `../knowledge/responsive.md` for the first-viewport rules.
- `../knowledge/marketing-cro.md` for ethical promo placement.
- `mobile-pwa.md` for install, offline, and safe-area behavior.
- `../checklists/visual-review.md` for the capture matrix.
