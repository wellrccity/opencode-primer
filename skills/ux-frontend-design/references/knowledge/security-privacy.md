# Security and Privacy

Load when: handling authentication, sessions, user input, personal data, third-party scripts, uploads, or anything rendered into HTML.

## Principles

- The browser is hostile territory. Any code, token, or decision shipped to the client can be read and changed by the user.
- Authorization is a server decision. Hiding a button is a UX improvement, never a security control.
- Every string from a user, a URL, an API, or a database is untrusted until it is validated or encoded for its sink.
- Escape by context: HTML text, HTML attribute, URL, CSS, JavaScript, and SQL each need different treatment.
- Collect the minimum personal data that the task requires, keep it for a stated period, and say why.
- Secrets belong in server-side configuration referenced with `{env:VAR}` placeholders, never in client bundles, logs, or source control.
- Security failures are quiet by default: do not confirm whether an account exists, and log the event without logging the secret.
- Privacy is a product requirement with legal weight under LGPD and GDPR, not a footer link.

## Decision rules

### Where to put the session token

| Storage | XSS exposure | CSRF exposure | Verdict |
| --- | --- | --- | --- |
| `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict` cookie | Not readable by script | Mitigated by `SameSite` plus a server check for state-changing requests | Default choice |
| `HttpOnly` cookie with `SameSite=None; Secure` | Not readable by script | Requires anti-CSRF tokens or origin checks | Only for cross-site embeds that need it |
| `localStorage` or `sessionStorage` | Fully readable by any injected script | Not sent automatically | Avoid for credentials |
| In-memory variable | Lost on reload, readable by injected script | Not sent automatically | Acceptable only with a refresh strategy that is itself safe |

- Keep access tokens short-lived and refresh them server-side when the architecture allows.
- Set `Secure`, `HttpOnly`, and an explicit `SameSite` value. Default to `Lax`; use `Strict` for admin surfaces when it does not break inbound links.
- Use the `__Host-` prefix for cookies that should be bound to one origin.

### Choosing an injection defense

| Sink | Correct defense |
| --- | --- |
| Element text | Assign `textContent`; never `innerHTML` for plain data |
| Framework template | Interpolation; trust the framework's escaping and avoid its raw-HTML escape hatch |
| HTML that must contain markup | Sanitize with a maintained library and an explicit allowlist |
| URL parameter | Validate the scheme against an allowlist; block `javascript:` and `data:` |
| Redirect target | Compare against a server-side allowlist of paths or hosts |
| SQL or query language | Parameterized statements; never string concatenation |
| Shell or template command | Avoid it; if unavoidable, pass arguments as an array, not a string |

- Content Security Policy is the backstop, not the fix: `default-src 'self'`, no `unsafe-inline` for scripts, explicit `script-src`, `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'self'`.
- Report-only first when a policy might break a flow, then enforce and remove violations.

### Session and permission checks

- Regenerate the session identifier on login and on privilege change.
- Expire idle sessions, expire absolute sessions, and make logout invalidate the session server-side, not just clear the cookie.
- Re-check authorization on every request for the resource, not just on page load.
- Permission-aware UI reads the same policy the server enforces; it must degrade to a clear denial state, never to a silent empty screen.

## Implementation patterns

### Forms and uploads

- Validate on the server; client validation is for feedback only.
- Reject unexpected fields, cap payload size, and enforce an allowlist of file types by content, not by extension.
- Never reflect submitted values into an error page without encoding.
- Rate-limit login, reset, and any endpoint that sends a message or costs money.

### CSRF

- For cookie-based sessions, require a per-session token or a strict `Origin`/`Sec-Fetch-Site` check on state-changing requests.
- Make state changes use non-idempotent methods (`POST`, `PUT`, `DELETE`); never let a `GET` mutate data.

### Open redirects and links

- Resolve `next`, `returnTo`, and `redirect` parameters against an allowlist; ignore anything else.
- Set `rel="noopener noreferrer"` on external links opened in a new tab.

### Data in transit and at rest

- HTTPS everywhere, HSTS with a considered `max-age`, and no mixed content.
- Do not put personal data, tokens, or reset codes in URLs: they land in logs, history, and referrer headers.
- Redact personal data in analytics, error reports, screenshots, and session replays; disable replay on payment and credential screens.

### Privacy and consent

- Purpose limitation: collect a field only for a stated use, and do not reuse it silently.
- Consent must be informed, specific, and as easy to refuse as to accept; no pre-checked boxes, no consent walls for non-essential cookies.
- Provide access, correction, export, and deletion paths for data subject requests, and honor the statutory deadlines that apply.
- Document subprocessors and third-party scripts that receive personal data; each needs a legal basis.
- Retention: define a period per data category and delete automatically.

### Dependencies

- Pin versions, review lockfile changes, and run an audit in CI.
- Treat a transitive dependency as code you ship: it can read the DOM, cookies, and storage.
- Remove unused packages; an unmaintained package is a standing vulnerability.

## Anti-patterns

- `innerHTML` with API data, and then a home-grown regex sanitizer.
- Tokens in `localStorage` justified by "it is simpler".
- Authorization checked only by hiding the route in the client router.
- Secrets in client bundles, source maps, or build-time constants.
- Session cookies without `HttpOnly` or `Secure`.
- Detailed login errors that reveal whether an email is registered.
- User data written to console logs, analytics events, or error messages.
- A consent banner that blocks nothing until the user clicks accept, or one that loads trackers before consent.
- Open redirect via an unvalidated `next` parameter.
- Wildcard CORS with credentials enabled.

## Verification

1. Search the client bundle for secrets, tokens, and API keys; record what the scan covered.
2. Submit marker payloads in every input, URL parameter, and stored field; confirm they render as text, not as markup or script.
3. Inspect session cookies in the browser: `HttpOnly`, `Secure`, `SameSite`, expiry, and scope.
4. Attempt a protected request with a lower-privilege session and confirm the server rejects it.
5. Test a state-changing request without the CSRF token or with a foreign `Origin`.
6. Check response headers: CSP, HSTS, `X-Content-Type-Options`, referrer policy, and frame ancestors.
7. Review logs and error output for personal data, tokens, and stack traces exposed to the client.
8. Walk the consent and deletion paths; confirm refusals are honored and data subject requests have a documented route.

## Related

- `../../SKILL.md` for the security floor that applies in every mode.
- `frontend-engineering.md` for auth-aware UI, error boundaries, and state handling.
- `../patterns/auth.md` for sign-in, reset, MFA, and session expiry flows.
- `../patterns/forms.md` for validation, error messaging, and autofill safety.
