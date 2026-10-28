# Forms

Use when: building or reviewing any data-entry surface - one field, a settings
panel, a multi-step wizard, or an application form.

## Layout and hierarchy

- One column by default. Two columns only for short related pairs (city and
  postal code, card expiry and security code) and only above 768px.
- Group by user intent, not by database schema. Every group has a heading and
  2 to 6 fields; a group of 9 is two groups.
- Order: identity, contact, context, preferences, consent. Ask for nothing the
  system can derive, look up, or defer.
- Label above the field and always visible. A placeholder is an example of the
  expected format, never a label.
- Help text sits under the label or under the field and is bound with
  `aria-describedby`. Two lines maximum.
- Required convention: if most fields are required, mark the optional ones with
  the word "optional"; if most are optional, mark required fields with
  "(required)". A bare asterisk without a legend fails.
- Field width signals expected length: a 4-digit field must not span the page.
- Group single-value choices in `fieldset` plus `legend`.
- Keep submit in the reading order after the last field. Full width on mobile;
  on desktop the primary action aligns with the field column and the secondary
  action sits left of it.
- Multi-step: show "Step 2 of 5" plus the step name. A bar without a label does
  not say what remains.

| Data | Control | Rule |
| --- | --- | --- |
| Long text | `textarea` | Auto-grow to a max height, then scroll |
| Email | `type="email"` | `inputmode="email"`, `autocomplete="email"` |
| Phone | `type="tel"` | Accept spaces and dashes |
| Number | Text plus `inputmode="numeric"` | Use text when leading zeros matter |
| Date | `type="date"` or three selects | Never free-text date in a known locale |
| Choice of 2 to 4 | Visible radios | A select hides options behind a click |
| Single toggle | Checkbox or switch | A switch applies immediately |

## Required states

Per field: empty, focus, filled, disabled, read-only, invalid, validating, and
valid only when confirmation is useful (username availability, password
strength). Form level: pristine, dirty, submitting, succeeded, failed with
retry, and saved draft. Partial: some fields are read-only or prefilled from a
partial profile, or server validation is unavailable; label what is missing and
keep the rest usable.

- Submitting: the label becomes progress text ("Creating account..."), a second
  click is refused, and the rest of the form stays readable.
- Failure: an error summary appears at the top, focus moves there, and every
  entered value survives.
- Success: name the next step ("Check your inbox at <address>") instead of only
  "Success".

## Interaction rules

- Validate format on blur; validate completeness on submit. After a field has
  failed once, revalidate on change so the error clears while typing.
- Error text states what is wrong, why, and how to fix it: "Date must be after
  today, 12 Mar 2026" beats "Invalid date".
- On a failed submit, the summary container uses `role="alert"`, lists links to
  each field, and inline errors stay next to their field.
- Prefer native constraint types and `autocomplete` tokens over script:
  `given-name`, `family-name`, `email`, `tel`, `street-address`, `postal-code`,
  `cc-number`, `one-time-code`, `current-password`, `new-password`.
- Enter submits. In a textarea, Enter adds a line and Ctrl+Enter submits.
- Back and forward must not lose data. Persist a draft server-side behind an
  explicit "Save and exit", or locally with a visible "Draft saved" note.
- Reset is not a normal action. If it exists, label the scope ("Clear all
  fields"), confirm when it destroys work, and offer undo.
- Verify one submission path end to end: double click, slow network, and retry
  after failure must create one record, not two.

## Data and edge cases

- Names: one free "Full name" field, or first and last with no required middle,
  no title validation, no letter-count limits.
- International input: accept Unicode, no forced transliteration, support
  right-to-left text, and do not assume a postal code format.
- Normalize on submit, not while typing: trim outer whitespace, collapse
  repeated spaces, strip spaces and dashes from card numbers.
- Session expiry during a long form: keep entries, reauthenticate in place, and
  resubmit on return.
- Network failure on submit: keep values, show a retry, never silently reload.
- File upload: state type, size, and count limits before selection, show
  per-file progress, and allow removal before submit.
- Optional personal questions include "prefer not to say" and never block
  submission.

## Accessibility

- Every control has a programmatic label; placeholder-only labeling fails
  WCAG 2.2 3.3.2.
- Invalid fields set `aria-invalid="true"` and point at their message with
  `aria-describedby`; the message is text, not a color change (1.4.1).
- The error summary is announced and its links move focus to the field (3.3.1).
- Keyboard order follows visual order; no tab traps and no positive tabindex.
- Error text meets 4.5:1 contrast (1.4.3) and stays legible at 200 percent zoom.
- Targets at least 24x24 CSS px (2.5.8); 44x44 recommended for radios and
  checkboxes on touch.
- Async validation announces results in a polite live region.
- Time limits are adjustable or extendable (2.2.1), and no field requires
  recalling a value from a previous screen (3.3.7).

## Performance

- Validate locally. If a remote check is unavoidable, debounce input (300 to
  500 ms is a recommendation, not a standard) and cancel stale requests.
- Do not block first render on a schema library for a form under 10 fields.
- Reserve space for error text or place it under the field so the submit button
  does not jump; inserted errors are a common source of layout shift.
- Avoid autofocus on touch devices; it opens the keyboard and hides context.
- Submit once, keep the response small, and acknowledge the click immediately;
  show progress only when submission exceeds about 1 s.

## Anti-patterns

- Placeholder used as the label, so the label disappears on typing.
- Asterisk-only required markers with no legend.
- Errors that appear while the user types the first character.
- Clearing the form or ending the session when validation fails.
- A disabled submit button with no stated reason.
- A reset button beside submit, or "Cancel" styled as the primary action.
- Password fields that block paste or block password managers.
- Captcha shown before any suspicious behavior, with no audio or text fallback.
- Required fields revealed only after the user has committed time.

## Checklist

- [ ] Every field has a visible label associated in markup; none rely on a
      placeholder.
- [ ] Required convention is stated once in text and matches the markup.
- [ ] Tab reaches every control in visual order, then submit.
- [ ] Submitting all-empty: summary announces, links to fields, focus visible.
- [ ] Submitting one wrong format: message names the fix and the value survives.
- [ ] Double click on submit creates exactly one record.
- [ ] Throttled network shows progress and a retry path.
- [ ] Back, refresh, and expired session do not lose entered data.
- [ ] 320px width: single column, no horizontal scroll, submit reachable.
- [ ] 200 percent zoom: no clipping and every label stays tied to its field.
- [ ] Screen reader announces label, required state, help text, and error.
- [ ] `autocomplete` tokens verified against real autofill output.
- [ ] No sensitive value appears in the URL, in logs, or in analytics.
