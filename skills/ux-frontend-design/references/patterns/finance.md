# Finance

Use when: building or reviewing money-facing interfaces such as balances,
invoices, transfers, payments, payouts, or reconciliation screens.

## Layout and hierarchy

- Order the page by the question the user is answering: current position,
  what changed, what needs action, then history.
- Amount is the visual anchor of a transaction row. Currency, sign, and
  counterparty sit adjacent, never on a separate screen.
- Account level above transaction level: totals at the top, ledger entries
  below, and every total links to the entries that compose it.
- Tables right-align numeric columns with tabular figures and a fixed decimal
  count per currency.
- A single primary action per region: "Transfer", "Pay", "Reconcile". Never
  place "Transfer" and "Export" at equal weight.
- Keep the review step visually distinct from the entry step so the user
  notices the change in mode.

## Required states

- Default, hover, focus-visible, disabled with a stated reason, and loading
  for every money action.
- Loading: skeleton keeps the amount column width; no layout shift on values.
- Empty: no transactions yet versus no results for the filter, with the
  correct next action.
- Stale: balance older than the refresh interval is marked with its
  timestamp, not presented as live.
- Pending versus settled is a visible status, not an implied one.
- Failed, reversed, refunded, partially paid, and disputed each have their own
  label and their own next action.
- Currency unavailable for the user's region: show the supported currency and
  the reason, not a zero.
- Insufficient funds, limit exceeded, and expired verification are inline
  errors next to the field that caused them.

## Interaction rules

- Represent money as integer minor units or a decimal type. Never use binary
  floating point for values, sums, or fees.
- Round once, at the defined step, and state the rule (for example
  half-up at the currency's minor unit). Display rounding never feeds back
  into recomputation.
- Format with the platform locale and currency APIs, using an explicit locale
  and currency code. Do not hand-build symbols or separators.
- Negative values keep a minus sign and also a non-color cue: direction word,
  arrow glyph, or accounting parentheses when the locale uses them.
- Symbols and codes: show the ISO code when more than one currency appears on
  screen, or when the symbol is ambiguous.
- Dates: absolute date plus timezone for anything that affects settlement.
  Never render an ambiguous numeric date without a month name or ISO order.
- Irreversible operations require a review step that restates amount,
  currency, source, destination, fee, and total received, then explicit
  confirmation. Typing the amount is acceptable for high-value transfers.
- Send an idempotency key with each payment or transfer request so a retry
  cannot duplicate the operation.
- Receipt after execution: reference id, timestamp, status, and a copy action.
- Destructive or reversing operations offer undo only when the provider
  genuinely supports reversal; otherwise say it cannot be undone.

## Data and edge cases

- Rounding differences appear in a named line (fee, tax, exchange spread),
  never absorbed silently into the displayed total.
- Reconciliation view: two sides, a difference column, and filters for
  matched, unmatched, and disputed. Differences are explained or flagged.
- Traceability: every balance and every status change links to its source
  entry and request id, visible or copyable.
- Export: CSV and PDF carry the same precision, the query parameters, the
  generation timestamp, and the timezone.
- Permissions: role gates actions in the UI; the server enforces the same
  rules. Never rely on a hidden button.
- Masking: show only the last four digits of an account or card. No full PAN,
  no CVV, no security answer anywhere in the client.
- Sensitive values stay out of URLs, analytics events, error messages, and
  screenshots used in reviews.
- Localization: pluralization and currency formatting come from the locale;
  layouts tolerate 30 percent longer strings.
- Timezone boundary: a transaction dated at 23:50 in one timezone must show
  the same instant everywhere, with the zone stated.

## Accessibility

- Amounts expose the sign and direction to assistive technology, not only the
  visual color: "minus 42.10 EUR, debit".
- Color is never the only carrier of gain, loss, status, or error (WCAG 2.2
  1.4.1). Pair it with text, icon, or label.
- Contrast 4.5:1 for amounts and labels, 3:1 for borders and status dots
  (1.4.3, 1.4.11).
- Tables use `th` with `scope`; the caption states the currency and period.
- Totals are not announced as a raw concatenation: group labels and values in
  one readable sentence for screen readers.
- Focus is visible on every control and not obscured by sticky totals
  (2.4.11).
- Target size at least 24x24 CSS px (2.5.8); 44x44 recommended for confirm and
  cancel in payment flows.
- Zoom 200 percent: the review step keeps amount, fee, and total visible
  together so the user can compare before confirming (1.4.10).

## Performance

- Fetch the balance summary and the transaction page in parallel; render the
  summary first with a timestamp.
- Do not recompute totals from the current page only. The server total is the
  source of truth.
- Charts and statement exports load on demand, not with the landing view.
- Realtime updates patch the affected row and the total, not the whole table.
- Polling intervals are a project decision; label stale data with the last
  update time instead of implying live values.
- Keep currency and date formatters created once, not per row render.

## Anti-patterns

- Comparing displayed rounded values and reporting a mismatch as a bug without
  checking the stored precision.
- Sign shown by color alone, or red and green as the only difference.
- Amounts rendered without currency when multiple currencies are on screen.
- Confirmation dialogs that restate nothing and only ask "Are you sure?".
- A retry button on a payment request without an idempotency key.
- Prefilled amounts the user did not choose, or a preselected "pay full
  balance" for a partial-payment flow.
- Full card or account numbers in the DOM, logs, or analytics payloads.
- Hiding a forbidden action instead of disabling it with a reason, which
  leaves the user guessing.
- Statement totals that ignore fees or include them twice.
- Fake "live" balances with no timestamp.

## Checklist

- [ ] Money stored and computed as integer minor units or decimal, not float.
- [ ] Rounding rule stated once and applied at a single point in the flow.
- [ ] Every amount shows currency code, sign, and locale-correct separators.
- [ ] Negative values carry a non-color cue readable by a screen reader.
- [ ] Dates affecting settlement show absolute date, time, and timezone.
- [ ] Review step restates amount, currency, source, destination, fee, total.
- [ ] Payment request sends an idempotency key; a double submit creates one
      operation.
- [ ] Receipt shows reference id, timestamp, status, and copy action.
- [ ] Reconciliation view has a difference column and a matched/unmatched
      filter.
- [ ] Export matches displayed precision and records its query parameters.
- [ ] Account and card values masked to the last four digits in UI and logs.
- [ ] Server rejects an unauthorized action even when the button is hidden.
- [ ] Keyboard-only pass completes a transfer through the review step.
- [ ] 200 percent zoom keeps amount, fee, and total comparable on one view.
