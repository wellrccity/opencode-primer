# Auth

Use when: building or reviewing sign in, sign up, password reset, passkey,
multi-factor, or session-expiry surfaces.

## Layout and hierarchy

- One task per screen; never pair sign in and sign up at equal visual weight.
- Focused layout: brand mark, one heading, one panel, no global navigation.
- A 360 to 440 CSS px panel width is a recommendation, not a standard.
- Order methods by friction: passkey or SSO, then password, then magic link.
- Primary action follows the last field; secondary actions are links below it.
- Sign up names its consequence first: "We will email a confirmation link".
- Reset is two screens: request, then confirmation repeating the address.
- Multi-factor: one code field, labelled resend with countdown, alternate link.
- Session expiry opens an inline re-auth panel and keeps unsaved work.

| Method | Control | Requirement |
| --- | --- | --- |
| Password | `type="password"` | `current-password` or `new-password` token |
| Passkey | Button calling WebAuthn | Conditional UI plus a password fallback |
| SSO | One link or button per provider | Provider name, not a logo only |
| One-time code | Single text input | `autocomplete="one-time-code"`, numeric mode |
| Magic link | Email field only | Copy names the sender and the expiry |

## Required states

Form: idle, submitting, invalid, rate-limited, service unavailable, succeeded.
Field: empty, focus, filled, autofilled, invalid.

- Submitting: label becomes activity text and a second activation is refused.
- Rate-limited: state the wait in words and the reset moment when known.
- Service unavailable is distinct from invalid credentials and offers retry.
- Session: active, expiring, expired, signed out elsewhere, account disabled.
- Success names the destination instead of showing a bare spinner.

## Interaction rules

- Validate format on blur, credentials on submit; never score a typed password.
- Keep the email after failure; clear only the password and keep focus inside.
- Show/hide control with a state-changing accessible name; default hidden.
- Set `autocomplete` explicitly; missing tokens break password managers.
- Allow paste and password-manager fill, or document the policy exception.
- Redirect only to same-origin allowlisted relative paths; reject absolute URLs.
- Silent refresh first, then the expiry panel; never discard the draft.
- Sign out invalidates server-side, clears caches, drops sensitive route state.
- Protected routes and hidden nav are UX only; the server authorizes requests.

## Data and edge cases

- One generic error covers unknown address and wrong password, timing included.
- Sign up with an existing address returns the same copy and sends a notice.
- Reset and magic-link tokens are single use, short lived, absent from logs.
- Passkeys register after a password sign in and keep a recovery path.
- Multi-factor recovery offers codes plus support, not a single phone number.
- Trim email, lowercase the domain, never alter the local part.
- Terms start unchecked, marketing consent separate, submit works without it.

## Accessibility

- Visible labels; the error summary takes focus and links to the failing field.
- Announce asynchronous errors in a live region without moving focus.
- Prefer one code input; six boxes break paste and screen-reader entry.
- No code time limit without extension (WCAG 2.2.1); Caps Lock is only a hint.
- Targets 24x24 CSS px (2.5.8), 44x44 recommended; text contrast at least 4.5:1.
- Works at 200 percent zoom and 320px width with no horizontal scroll.

## Performance

- Keep auth routes free of marketing bundles, chat widgets, and tag managers.
- Code-split the route, preconnect to the auth endpoint, defer analytics.
- Reserve space for error text so a failed submit does not shift the form.
- Show progress after 400 ms (a recommendation) and cancel stale checks.

## Anti-patterns

- Different messages for unknown address and wrong password.
- Disabled submit with no reason, or a form that rejects autofill.
- Password rules revealed only after submit, and rules that forbid paste.
- Social login as the only path with no accessible alternative.
- Spinners with no error branch, retry, or exit.
- Session expiry that discards the draft without warning.
- Client-side guards presented as authorization.

## Checklist

- [ ] Every field has a visible label, correct `autocomplete`, keyboard access.
- [ ] Wrong credentials and unknown address return identical copy and status.
- [ ] A reset request for an unknown address matches the real-account response.
- [ ] Rate limiting states the wait in text and is enforced server-side.
- [ ] Password toggle is keyboard reachable, named, and never submits.
- [ ] Post-login redirect returns to the triggering route; off-origin `next` fails.
- [ ] Expired session keeps the draft and does not redirect mid-edit.
- [ ] Sign out invalidates server-side; back navigation restores nothing.
- [ ] A direct protected request fails authorization regardless of UI state.
- [ ] One-time code accepts paste and autofill and can be reissued.
- [ ] Terms consent starts unchecked and marketing consent is separate.
- [ ] At 320px and 200 percent zoom: no horizontal scroll, submit reachable.
- [ ] Screen reader announces label, error, and the form-level summary.
- [ ] No console errors, and no third-party call carries credentials or tokens.
