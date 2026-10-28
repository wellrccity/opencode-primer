---
name: ux-frontend-design
description: Use when designing, building, reviewing, or improving web interfaces: user flows, visual direction, responsive layout, accessibility, conversion, frontend engineering, performance, SEO, security, and visual QA.
---

# UX Frontend Design

This skill is a product-quality system for web interfaces, not a component generator. It turns product intent into flows, states, tokens, and verified code. The entry point orchestrates decisions; deep knowledge lives in modules loaded only when a task needs them. No interface is "done" until it has been built, tested, and inspected in a browser.

## Activation

Use when the task involves:
- Designing or building screens, flows, components, layouts, or design tokens.
- Reviewing or auditing an existing interface for usability, accessibility, or visual quality.
- Improving conversion, hierarchy, copy, or perceived speed on a commercial page.
- Frontend work with performance, SEO, or security implications.

Do not activate for:
- Backend-only work: APIs, migrations, jobs, data pipelines without a UI.
- CLI tools, scripts, or infrastructure with no web interface.
- Pure library or algorithm work that renders nothing.

## Operating principles

1. **Evidence over taste.** A claim about quality needs a build, a test, a screenshot, or a measurement.
2. **Critique before code.** Name the goal, hierarchy, and states before writing markup.
3. **Reuse project decisions.** Extend existing tokens and components before inventing new ones.
4. **Real verification.** Browser, keyboard, zoom, and console passes are part of the work, not optional.
5. **Anti-generic by default.** Every interface needs one deliberate idea tied to brand and audience.
6. **Ethical conversion.** Persuasion must survive the question "would the user thank us for this?".

## Depth modes

| Mode | When | Phases required | Output |
| --- | --- | --- | --- |
| Audit | Read-only diagnosis of an existing interface | 0, 1, 5 | Findings with severity and evidence |
| Review | Read-only check of a diff, screen, or flow | 0, 1, 5 | Findings plus proposed fixes |
| Improve | Targeted change inside an existing system | 0, 1, 3, 4, 5 | Smallest coherent diff plus evidence |
| Build | New page, flow, or product surface | 0 to 5 | Shipped interface plus evidence |
| Single screen | One static or mostly static screen, prototype, or isolated page | 0, 1, 2, 4, 5 | Smallest coherent diff plus minimum gate evidence |

Audit and Review never modify files. Single screen still runs the minimum gate in
`references/checklists/release.md`; phase 2 is a short state list, not a full IA
map.

## Workflow

### Phase 0 - Recover project context

Inspect the stack, tokens, components, conventions, existing copy, and implemented states. Output: a short context note listing what already exists and what must be reused.

Gate: you can name the styling mechanism, the token source, and two existing components you will reuse.

### Phase 1 - Understand the product

Establish goal, audience, job to be done, constraints, and the single success metric. Output: a one-paragraph brief.

Gate: the brief states one primary action and one measurable outcome.

### Phase 2 - Define the experience

Map flows, information architecture, hierarchy, required states, and error prevention. Output: a flow and state list covering loading, empty, error, partial, and success.

Gate: every screen in the flow has all five states named.

### Phase 3 - Define the visual direction

Collect references and anti-references, then commit to one visual idea: type, color, spacing, radius, motion, density. Output: token decisions recorded as names and values.

Gate: every decision maps to a token or an existing project value, with no ad hoc values left.

### Phase 4 - Implement

Write semantics, components, states, responsive behavior, accessibility, security, and performance in one pass. Output: the smallest coherent diff.

Gate: the diff builds, uses project tokens, and covers the states from phase 2.

### Phase 5 - Validate

Run the minimum gate in `references/checklists/release.md` first. Then run build, tests, screenshots at the named widths, network inspection, and a performance check when the change warrants the full matrix. Output: evidence, quoted or attached.

Gate: the applicable completion levels in the verification protocol are all true, or the gap is reported as missing. Audit and Review state which levels the existing interface meets and which it does not.

## Non-negotiable floors

These apply in every mode, including Audit.

- Semantic HTML with landmarks, and buttons for actions, links for navigation.
- Full keyboard operability with a logical tab order and no traps.
- Visible focus on every interactive element; never remove an outline without a replacement.
- Text contrast of at least 4.5:1; large text at least 3:1; UI boundaries at least 3:1.
- Target size of at least 24x24 CSS px (WCAG 2.2 AA 2.5.8), except where the criterion's spacing, inline, or essential exceptions apply; 44x44 is the recommendation.
- No horizontal overflow at 320 CSS px width.
- At 390x844, the primary action or entry point is fully visible without scrolling; nothing above it may consume the first viewport.
- All five UI states for every touched surface: loading, empty, error, partial, success.
- Motion respects `prefers-reduced-motion`.
- No secrets, tokens, or personal data in client code, URLs, logs, or screenshots.
- Authorization is enforced server-side; hidden UI is not a permission check.
- No fake urgency, fake scarcity, fabricated proof, or invented counters.

## Skip rules

Choose the smallest sufficient depth, never the smallest sufficient quality.

- A CSS-only change skips marketing and information architecture work, but never skips visual, responsive, and accessibility checks.
- A copy change skips layout and motion review, but still checks contrast and meaning.
- A new commercial page (landing, pricing, checkout) needs the full path: brief, flow, direction, implementation, validation.
- A bug fix inside an existing pattern reuses the pattern module and skips direction work.

## Decision router

Load the entry point first, then only the modules this table selects.

| Task | Module |
| --- | --- |
| Any UI task, start here | `references/knowledge/ux.md` |
| New flows, IA, or step reduction | `references/knowledge/ux.md` |
| Typography, color, spacing, tokens | `references/knowledge/ui-design.md` |
| Visual direction and style choice | `references/knowledge/art-direction.md` |
| Landing page or pricing page | `references/patterns/landing-page.md`, `references/knowledge/marketing-cro.md` |
| Conversion copy and funnel work | `references/knowledge/marketing-cro.md` |
| Forms | `references/patterns/forms.md` |
| Authentication screens | `references/patterns/auth.md` |
| Tables and dense data lists | `references/patterns/tables.md` |
| Dashboards and SaaS product UI | `references/patterns/dashboard-saas.md` |
| Admin and back-office tools | `references/patterns/admin-app.md` |
| E-commerce and checkout | `references/patterns/ecommerce-checkout.md` |
| Consumer app home, ride-hailing, or delivery | `references/patterns/consumer-home.md`, `references/patterns/mobile-pwa.md` |
| Finance, payments, money display | `references/patterns/finance.md` |
| Institutional or corporate site | `references/patterns/institutional-site.md` |
| Mobile web and PWA | `references/patterns/mobile-pwa.md`, `references/knowledge/responsive.md` |
| Navigation and menus | `references/patterns/navigation.md` |
| Accessibility audit | `references/knowledge/accessibility.md`, `references/checklists/accessibility.md` |
| Performance work | `references/knowledge/performance.md` |
| SEO | `references/knowledge/seo.md` |
| Security and privacy | `references/knowledge/security-privacy.md` |
| Frontend architecture and state | `references/knowledge/frontend-engineering.md` |
| Visual QA before release | `references/checklists/visual-review.md`, `references/checklists/release.md` |
| Pre-code critique | `references/checklists/interface-critique.md` |
| Responsive verification | `references/checklists/responsive.md` |
| Psychology deep dive | `references/knowledge/cognitive-psychology.md`, `references/UX_LAWS_REFERENCE.md` |
| Perceived speed, motion, and keyboard deep dive | `references/MODERN_UX_PLAYBOOK.md` |
| Before claiming done | `references/checklists/release.md` (minimum gate) |

## Project memory

- Inspect before designing: tokens, components, typography, spacing, radii, motion, tone, and dark mode support.
- Extend tokens instead of hardcoding values; if a value is missing, add it at the right layer.
- If no system exists, define a minimal token set inside the project's existing styling mechanism.
- Record reused versus added decisions in the plan or the PR summary.
- Never redesign unrelated screens; scope changes to the surface under work.

## Anti-generic rules

Banned unless a documented reason exists:
- Cards for everything, nested cards, and card grids used as a default layout.
- Decorative gradients with no hierarchy role, and shadow stacking.
- Arbitrary radii, emoji as professional icons, and mixed icon families.
- Hero plus three feature cards with no brand idea; center-everything layouts.
- Equal visual weight everywhere, so nothing reads as primary.
- Stock-photo cliches, generic 3D blobs, and shipped lorem ipsum.
- Animation on everything, and hover-only affordances.
- Fake urgency, fake scarcity, fake testimonials, fake counters.

Required: one deliberate visual idea tied to brand and audience, stated in one sentence before implementation.

## Verification protocol

1. Detect the stack from manifests and lockfiles.
2. Run the existing lint, typecheck, test, and build scripts; quote the results.
   For a standalone HTML file with no build, validate the document, confirm zero
   external requests, and run the minimum gate. Do not invent build or test
   commands.
3. Validate in a browser at 320, 375, 768, 1024, and 1440 CSS px.
4. Pass keyboard only: tab order, focus visibility, escape from overlays.
5. Check 200 percent zoom and reduced motion; check dark mode when present.
6. Inspect console and network for errors and failed requests.

Report four distinct levels: code written, build passes, tests pass, interface validated. Never collapse them into one claim.

## Definition of done

- [ ] One primary action per decision region, with visible hierarchy.
- [ ] All five states implemented for touched surfaces.
- [ ] Empty state explains the value and offers the first action.
- [ ] Error state names the cause and the recovery path.
- [ ] No horizontal overflow at 320 CSS px.
- [ ] At 390x844, the primary action or entry point is visible without scrolling.
- [ ] Minimum gate run and recorded: overflow, first viewport, keyboard, console.
- [ ] Keyboard pass completed with visible focus throughout.
- [ ] Contrast and target size meet the floors above.
- [ ] Zoom at 200 percent and reflow at 320 CSS px (400 percent at 1280) keep content usable.
- [ ] Reduced motion and dark mode verified when present.
- [ ] Console and network clean on the changed flow.
- [ ] No secrets, tokens, or personal data exposed client-side.
- [ ] Copy reviewed for accuracy and honest claims.
- [ ] Build and tests pass, with commands and output recorded.
- [ ] Screenshots at the five widths reviewed against the previous state.

## Output contract

Report exactly six fields, no essays:
- **Decisions** - the direction and trade-offs chosen.
- **Changed** - files and behaviors touched.
- **Verified** - commands, widths, and checks run, with results.
- **Status** - Draft, Validated, or Release-ready. Validated requires the minimum gate; Release-ready requires the full gate and the four completion levels.
- **Missing or risks** - known gaps, unverified items, follow-ups.
- **Next step** - one concrete action.

## Reference index

Knowledge:
- `references/knowledge/ux.md` - flows, IA, heuristics, error prevention, empty states.
- `references/knowledge/ui-design.md` - type, color, spacing, grid, tokens, elevation.
- `references/knowledge/art-direction.md` - references, style families, direction brief.
- `references/knowledge/marketing-cro.md` - value proposition, CTA hierarchy, testing, ethics.
- `references/knowledge/cognitive-psychology.md` - load, memory, choice, affordances.
- `references/knowledge/responsive.md` - fluid layout, breakpoints, overflow, transformations.
- `references/knowledge/accessibility.md` - WCAG 2.2 AA working set and testing.
- `references/knowledge/frontend-engineering.md` - composition, state, states, typing, tests.
- `references/knowledge/performance.md` - Core Web Vitals, images, fonts, bundles, caching.
- `references/knowledge/seo.md` - semantics, metadata, crawlability, structured data.
- `references/knowledge/security-privacy.md` - XSS, tokens, sessions, consent, data exposure.

Patterns:
- `references/patterns/landing-page.md` - hero, proof, pricing teaser, final CTA.
- `references/patterns/dashboard-saas.md` - density, filters, KPIs, saved views.
- `references/patterns/admin-app.md` - shortcuts, bulk edit, destructive actions, audit.
- `references/patterns/ecommerce-checkout.md` - product, cart, payment, confirmation.
- `references/patterns/consumer-home.md` - map-first home for ride-hailing and delivery.
- `references/patterns/institutional-site.md` - content architecture, trust, CMS limits.
- `references/patterns/forms.md` - labels, validation, errors, multi-step, autofill.
- `references/patterns/tables.md` - columns, sorting, pagination, responsive tables.
- `references/patterns/navigation.md` - global and local nav, search, URL as state.
- `references/patterns/auth.md` - sign in, reset, MFA, session expiry, safe errors.
- `references/patterns/mobile-pwa.md` - touch, safe areas, offline, install, budgets.
- `references/patterns/finance.md` - precision, formatting, confirmations, audit trail.

Checklists:
- `references/checklists/interface-critique.md` - pre-code review with severity.
- `references/checklists/visual-review.md` - screenshot inspection across states and modes.
- `references/checklists/responsive.md` - widths, reflow, zoom, virtual keyboard.
- `references/checklists/accessibility.md` - WCAG mapping plus manual passes.
- `references/checklists/release.md` - four-level completion gate.

Legacy deep dives:
- `references/UX_LAWS_REFERENCE.md` - long-form laws with implementation examples.
- `references/MODERN_UX_PLAYBOOK.md` - tactical playbook for speed, forms, motion.
