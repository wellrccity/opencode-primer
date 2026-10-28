# Marketing and conversion (CRO)

Load when: a page or flow has a commercial goal: landing page, pricing,
signup, trial, checkout, or a campaign surface.

## Principles

- Copy sells the outcome, then the mechanism, then the proof. Feature lists are
  the mechanism, not the pitch.
- One page, one primary action. Competing calls to action split intent.
- Friction is anything between intent and completion: extra fields, unclear
  price, slow load, unexplained steps.
- Proof must be real. A testimonial without a source is a liability, not an
  asset.
- Conversion is not a license to deceive. Dark patterns convert once and cost
  the brand permanently.
- Measure the funnel, not the page. A high click rate with high drop-off is not
  success.

## Decision rules

Message hierarchy:

| Level | Content | Placement |
| --- | --- | --- |
| 1 | Value proposition: outcome for a named audience | Hero headline |
| 2 | Clarifier: how it works in one line | Subheadline |
| 3 | Primary action | Hero, repeated at decision points |
| 4 | Proof: real evidence | Near the first action ask |
| 5 | Objections: price, risk, effort, switching | Before the final action |
| 6 | Detail: specs, integrations, policy | Below the fold, linked |

Copy rules:

- Lead with the benefit, support with the mechanism. "Close the month in a day"
  beats "automated ledger reconciliation" only when it is true.
- Specificity over adjectives. A named outcome beats "powerful" or "seamless".
- Match the audience's words; internal jargon reduces trust.
- Every heading must be understandable without the section body.
- State the price or the pricing model before the form, not after.
- Buttons name the action and the result: "Create account", not "Submit".

CTA hierarchy:

- One primary CTA per viewport region, consistent label throughout the page.
- Secondary CTA is a lower-commitment alternative, visually subordinate.
- Repeat the primary action after each objection block, not after every section.

Friction reduction, in order of return:

1. Remove fields that are not used before first value.
2. Explain cost and next step before asking for commitment.
3. Allow guest or low-friction start when the business allows it.
4. Preserve entered data on validation failure.
5. Fix load and interaction performance on the critical path.

## Implementation patterns

Landing page skeleton:

```text
Hero: outcome headline, one-line clarifier, primary CTA, one proof cue
Problem: the current cost of not solving it, in the user's words
How it works: three steps, each a verb
Benefits: outcome per benefit, backed by mechanism
Proof: real customer evidence, logos only with permission
Objections: price, effort, risk, migration, support
Final CTA: restate the outcome, single action, low-friction wording
Footer: policy, contact, legal, accessibility, privacy
```

Pricing page:

- Show units and billing period explicitly; state what happens at renewal.
- Mark the recommended plan by fit, not by pressure.
- Compare plans on the dimension that decides the purchase.
- Keep the comparison table readable at 320 px: transform, do not shrink text.
- Link to the full policy instead of hiding fees in fine print.

Forms as conversion surfaces:

- Ask for the minimum needed to deliver the first value.
- Inline validation on blur, not on every keystroke.
- Label every field; placeholders are not labels.
- Show the cost of the next step before the button.

A/B testing:

- One variable per test. Two changes make the result uninterpretable.
- Decide the primary metric and guardrail metrics before launch: conversion
  rate plus refund rate, support contacts, or latency.
- Do not call a result early. A test needs enough exposure to distinguish the
  effect from noise; state the planned sample or duration in advance.
- Never ship a variant that fails accessibility, performance, or ethics checks,
  even if it wins on clicks.
- Record the outcome, including inconclusive results.

Measurement:

| Metric | Definition | Watch for |
| --- | --- | --- |
| Conversion rate | Completed actions divided by eligible sessions | Bots, duplicate submissions |
| Drop-off | Exits per step divided by entries to that step | Attribution between steps |
| Activation | First real value moment reached | Definition drift across teams |
| Retention | Return within a defined window | Window chosen after the fact |

## Anti-patterns

- Fabricated testimonials, invented customer counts, or fake logos.
- Countdown timers that reset on reload.
- "Only 2 left" when inventory is not tracked.
- Confirmshaming: "No thanks, I prefer losing money".
- Pre-checked add-ons, insurance, or marketing consent.
- Hidden fees revealed at the last step.
- Fake scarcity in pricing tiers.
- Exit-intent modal that blocks the back button.
- Auto-playing video with sound on a commercial page.
- Long form before any value has been shown.

## Verification

- Read the page as a first-time visitor: can you state the offer, the price, and
  the next step within one screen?
- Click every CTA and confirm it leads to the promised destination.
- Submit the form with invalid data and confirm nothing is lost.
- Count required fields and justify each against first value.
- Confirm all proof is sourced and permissioned; remove what is not.
- Check the funnel events fire once per action in the network panel.
- Confirm no urgency, scarcity, or discount claim is unsupported by data.

## Related

- `ux.md` for flow structure and error prevention in the funnel.
- `cognitive-psychology.md` for default effects and choice counting.
- `../../patterns/landing-page.md` for the full page contract.
- `../../patterns/forms.md` for field-level conversion details.
