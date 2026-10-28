# E-commerce Checkout

Use when: designing product discovery, product detail, cart, checkout, payment,
or order confirmation for a storefront.

## Layout and hierarchy

- Discovery: filter control, result count, sort, then the grid. Filters collapse
  into a sheet below 768px and never push results off screen.
- Product card: image, name, price, availability, one differentiator. No badges
  unless they carry real information (sale, low stock, new).
- Product detail: gallery first, buy box second. The buy box holds name, price,
  variant picker, quantity, add-to-cart, and a delivery estimate.
- At 375px the buy box must be reachable before any cross-sell block.
- Cart: thumbnail, name, variant, quantity stepper, unit price, line total,
  remove. Totals repeat at the bottom, never only at the top.
- Checkout is a linear sequence: contact, address, shipping, payment, review.
  Show the step count ("Step 2 of 4") and allow returning to completed steps.
- Order summary: sticky column on desktop, collapsible panel on mobile. Keep it
  open on the review step and closed on payment.
- Trust signals belong next to the pay action: return policy, delivery window,
  support channel, payment provider mark. No decorative seals.

| Step | Fields | Gate to continue |
| --- | --- | --- |
| Contact | email, phone optional | valid email format |
| Address | country, postal code, street, number, city | address accepted by validator |
| Shipping | method, delivery estimate | method selected |
| Payment | card or wallet, billing address | tokenized, no raw card data in app state |
| Review | read-only summary, edit links, place order | totals unchanged or re-confirmed |

## Required states

- Cart empty, cart with one item, cart with quantity at stock limit.
- Variant unavailable after selection; variant partially unavailable.
- Price changed since the item was added; discount expired.
- Shipping unavailable for the postal code; delivery date slipped.
- Payment processing, payment declined, payment requires a second factor.
- Network failure during submit, duplicate submit prevented, order placed.
- Session expired mid-checkout, with the cart preserved.

Every state needs a recovery action. A dead end is a defect.

## Interaction rules

- Quantity changes update line totals and the summary in place, without a page
  reload and without losing focus.
- Removing the last item replaces the cart with an empty state that links back
  to the catalog.
- Guest checkout is the default path. Account creation is offered after the
  order, never as a gate.
- Wallet buttons (Apple Pay, Google Pay, PayPal) render above the card form and
  use the platform sheet, not a custom modal.
- Validation runs on blur and on submit; never on every keystroke of a card
  number before the field is complete.
- One primary action per step. Secondary actions are text links.
- Back navigation preserves every entered value.
- Promo code input stays collapsed until requested; an invalid code explains
  why without clearing the cart.
- Submit is disabled only while a request is in flight, and the label changes
  to a progress wording instead of a spinner-only button.

## Data and edge cases

- Re-check stock and price server-side at order creation; show the diff and ask
  for confirmation when they changed.
- Send an idempotency key with the order request so a retry cannot double-charge.
- Address autocomplete fills structured fields, not one free-text blob.
- Taxes and shipping are computed from the final address, and the review step
  shows the same numbers the payment step charged.
- Currency and date formats follow the locale; the currency code is visible
  when the store sells in more than one.
- Card data never enters app state, logs, analytics, or error reports; the
  provider's tokenized field owns it.
- Order confirmation carries the order number, items, totals, delivery estimate,
  and a support path, and it survives a refresh.

## Accessibility

- Variant groups use fieldset and legend, or a radiogroup with a group label.
- Prices are announced with currency, for example "39.90 US dollars".
- Stock and error states use text plus icon, never color alone.
- Inline errors link to inputs with aria-describedby; the error summary links to
  the first invalid field.
- Cart count updates go through a polite live region.
- The step indicator is an ordered list; the current step uses aria-current.
- On step change, move focus to the step heading and announce the new step.
- The quantity stepper is a group of buttons with accessible names, not an
  unlabeled number input with spinner arrows.
- All controls meet the 24x24 CSS px floor; steppers and remove buttons reach
  44x44 where space allows.

## Performance

- The product image is the LCP element: correct dimensions, modern format,
  priority hint, no lazy loading above the fold.
- No third-party marketing script loads on the payment step.
- Analytics and personalization load after interaction or on idle.
- The order summary reserves its height so totals do not shift the layout.
- Variant selection stays under the INP budget; do not re-render the gallery on
  every option change.
- Measure LCP, INP, and CLS on the product detail and checkout routes before and
  after changes.

## Anti-patterns

- Account required before payment.
- Costs revealed only at the last step (shipping, tax, service fee).
- Countdown timers or fabricated stock counters.
- Pre-checked upsells, insurance, or newsletter opt-in.
- Disabled add-to-cart with no explanation of the missing variant.
- Multi-page wizard for four address fields.
- Custom card inputs that break autofill and password managers.
- Cross-sell blocks between the cart and the pay action.

## Checklist

- [ ] Buy box is reachable before any cross-sell at 375px.
- [ ] Guest checkout completes without creating an account.
- [ ] Total shown at review equals the amount charged, verified in a test order.
- [ ] Out-of-stock, price-change, and expired-session states each have a recovery
      action, verified by forcing the state.
- [ ] Duplicate submit is blocked and a retry reuses the idempotency key.
- [ ] Card data is absent from app state, logs, and network payloads outside the
      provider iframe.
- [ ] Step indicator exposes aria-current and focus moves to the step heading.
- [ ] Error summary and inline errors are linked to their inputs.
- [ ] Cart count changes are announced by a live region.
- [ ] Checkout route loads no marketing scripts, confirmed in the network panel.
- [ ] LCP, INP, and CLS measured on product detail and checkout.
- [ ] Keyboard-only run places an order end to end.

## Related

- `forms.md` for field structure and validation timing.
- `../knowledge/security-privacy.md` for token handling and card data scope.
- `../knowledge/marketing-cro.md` for ethical conversion rules.
