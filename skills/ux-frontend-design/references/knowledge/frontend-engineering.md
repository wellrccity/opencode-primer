# Frontend engineering

Load when: implementing or refactoring interface code that must stay correct as states, permissions, and data sources multiply.

## Principles

- Separate presentation, logic, and data access. A component that fetches, transforms, and also renders is three responsibilities with one test surface.
- State lives where it is owned. Lift it only when two siblings genuinely share it; derive it when it can be computed.
- Model states explicitly. Loading, success, empty, error, and network failure are five different screens, not one screen with a spinner.
- Types are documentation that the compiler enforces. Strict mode, no `any` at boundaries, parse untrusted data at the edge.
- Composition over configuration. Children and slots beat a growing list of boolean props.
- Smallest coherent diff. Refactor only what the change requires, and keep unrelated behavior byte-identical.
- Tests exist to catch regressions you would otherwise ship. Test behavior and contracts, not implementation details.
- Dependencies are liabilities with an update schedule. Every package needs a reason, a size, and a maintenance signal.

## Decision rules

| Question | Rule |
| --- | --- |
| Local or global state? | Local first; global only for cross-route concerns such as session, theme, or feature flags |
| Server data in a global store? | No. Use the fetch layer or cache that owns it, so stale data has one source of truth |
| Value can be computed? | Derive it during render instead of storing and syncing a second copy |
| Form state library needed? | Only when there are dependent fields, multi-step state, or array fields; otherwise local state is enough |
| Two similar components? | Wait for the third case before abstracting; duplication is cheaper than a wrong abstraction |
| Fetch inside a component? | No. Call a typed client from a hook or loader; keep the component pure |
| Optimistic update? | Only when the server can reject and the UI can roll back visibly |
| Error boundary placement? | Per route or widget boundary, with a retry that does not reload the whole app |
| New dependency? | Check the last release, open vulnerabilities, bundle cost, and whether 30 lines of local code suffice |

### State taxonomy

| Type | Owner | Example | Failure mode if misplaced |
| --- | --- | --- | --- |
| UI state | Component | open, hovered, selected tab | Flicker or lost state on remount |
| Form state | Form component or form library | field values, touched, errors | Validation drift between fields |
| Server state | Data layer with cache | list of orders, user profile | Two copies disagree after refresh |
| URL state | Router | filters, page, sort, active id | Broken deep link, unshareable view |
| Session state | App shell or auth provider | user, role, expiry | Permission flash or stale identity |

## Implementation patterns

### Composition and props

```tsx
type PanelProps = {
  title: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
};

export function Panel({ title, children, actions }: PanelProps) {
  return (
    <section aria-labelledby="panel-title">
      <header>
        <h2 id="panel-title">{title}</h2>
        {actions}
      </header>
      {children}
    </section>
  );
}
```

- Props are explicit and narrow. Pass `children` instead of a `renderBody` callback until real flexibility is needed.
- Never spread unknown props onto a DOM node; it leaks `onClick` handlers and invalid attributes.
- Keep controlled and uncontrolled behavior separate: a component should not silently own a value it also accepts from props.

### Data access and contracts

- One typed client per API surface. Parse responses with a schema validator and fail loudly at the boundary.
- Normalize errors into a small union: `network`, `auth`, `validation`, `server`, `unknown`. The UI branches on the union, not on status text.
- Requests are cancellable; ignore responses after unmount or after a newer request supersedes them.
- Never trust the client for authorization. The UI hides unavailable actions; the server rejects them.

```ts
type ApiResult<T> =
  | { status: "ok"; data: T }
  | { status: "error"; kind: "auth" | "validation" | "server" | "network"; message: string };
```

### Required states per data surface

| State | Must show | Must not do |
| --- | --- | --- |
| Loading | Skeleton matching final layout, or a labelled progress region | Shift layout when data arrives |
| Empty | What this area is for, why it is empty, one next action | Show a blank panel or a zero-filled chart |
| Partial | What loaded, what failed, retry for the failed part | Discard the successful data |
| Error | Plain-language cause, retry, support path | Print a stack trace or raw payload |
| Network failure | Offline notice, preserved form input, retry when back | Drop the user's work |
| Success | The result, and the next action | Fire a toast whose only evidence is the toast |

### Forms and validation

- Validate on blur and on submit. Re-validate on change only after the first error for that field.
- Share one schema between client and server when the stack allows it; duplicate rules are a bug factory.
- Submit state is explicit: `idle`, `submitting`, `success`, `error`. Disable the submit button during submit and announce the result.

### Tests

| Level | Scope | What it proves |
| --- | --- | --- |
| Unit | Pure functions, formatters, reducers | Logic correctness and edge cases |
| Integration | Component with mocked network | Renders each state, handles error and retry |
| Flow | Real router and handlers | A user completes the task end to end |
| Contract | Schema against recorded payloads | API drift is caught before release |

## Anti-patterns

- `useEffect` used to derive state that could be computed during render.
- Fetching in `useEffect` with no cancellation, leaking state after unmount.
- A single `isLoading` boolean covering six distinct flows.
- `any` at an API boundary, followed by optional chaining everywhere downstream.
- Prop drilling through five layers instead of one context or one composed child.
- Boolean prop explosion: `isCompact`, `isBordered`, `isPrimary`, `isInline`.
- Optimistic UI with no rollback, so a rejected write looks successful forever.
- Catching errors to show a generic toast and losing the actionable detail.
- Client-side permission checks treated as enforcement.
- Wrapper components that re-export a library component with no added behavior.

## Verification

1. Run the existing scripts in order: lint, typecheck, unit tests, build. Record the actual command and exit code.
2. Force each data state in the browser or via mock: loading, empty, partial, error, network failure, success. Screenshot each.
3. Walk one flow with the network throttled to offline mid-request; confirm input survives and retry works.
4. Search the diff for `any`, non-null assertions, and `console.` before merging.
5. Confirm every new dependency appears in the lockfile and has no known high-severity advisory in the project's audit command.
6. Check that the diff touches only files required by the change; report any incidental edit.

## Related

- `performance.md` for bundle budgets, splitting, and rendering strategy.
- `security-privacy.md` for XSS, token storage, and permission enforcement.
- `../patterns/forms.md` for form structure and error patterns.
- `../patterns/tables.md` for data-dense surfaces.
