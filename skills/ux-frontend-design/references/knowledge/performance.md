# Performance

Load when: a page feels slow, a build grows, a Core Web Vitals metric is out of range, or you are about to add images, fonts, scripts, or a third-party tag.

## Principles

- Performance is a user-visible property: it decides whether the first screen appears, whether taps respond, and whether layout jumps under the thumb.
- Measure before optimizing, and measure the same page the same way after. An unmeasured change is a guess.
- Field data describes real users on real networks; lab data describes a repeatable scenario. Use field data to choose the problem, lab data to isolate the cause.
- The fastest request is the one never made. Remove, defer, or replace before you compress.
- Budget the cost at design time. A hero video or a chat widget is a performance decision, not a styling detail.
- Optimize the critical path first: the LCP element, the fonts it needs, and the CSS that positions it.
- Regressions are cheap to prevent and expensive to find. Wire a check into the build.
- Report numbers with the page, device class, network profile, and date. A number without context is marketing.

## Decision rules

### Core Web Vitals thresholds

Assessment at the 75th percentile of page loads, split by mobile and desktop.

| Metric | Good | Needs improvement | Poor |
| --- | --- | --- | --- |
| LCP (Largest Contentful Paint) | 2.5 s or less | above 2.5 s to 4.0 s | above 4.0 s |
| INP (Interaction to Next Paint) | 200 ms or less | above 200 ms to 500 ms | above 500 ms |
| CLS (Cumulative Layout Shift) | 0.1 or less | above 0.1 to 0.25 | above 0.25 |

- LCP is usually the hero image, the headline block, or a poster frame. Find the element in the field data before touching anything else.
- INP is dominated by long tasks on the main thread: hydration, large list rendering, heavy event handlers, synchronous storage reads.
- CLS comes from media without dimensions, late-injected banners, web fonts swapping metrics, and content inserted above existing content.

### Budgets

Set budgets per route, not per site, and label them as project recommendations until measured.

| Asset | Starting budget (recommendation, tune per project) |
| --- | --- |
| Initial JS on a content route | keep small, review every dependency over a few tens of KB gzipped |
| Initial CSS | one render-blocking stylesheet; split the rest |
| Web fonts | two families maximum, subset, preloaded only when used above the fold |
| LCP image | sized to its rendered box, modern format, priority hint |
| Third-party scripts | each one needs an owner and a measured benefit |

### Rendering strategy

| Strategy | Use when | Cost |
| --- | --- | --- |
| Static generation | Content changes per deploy, same HTML for everyone | Rebuild on change |
| Server rendering | Personalized or frequently changing HTML, SEO matters | Server latency, hydration cost |
| Client rendering | Authenticated app shell behind a login | Empty first paint, crawl risk, slower LCP |
| Streaming SSR | Long pages where the shell can paint early | Complexity in error handling |

## Implementation patterns

### Images

- Serve AVIF or WebP with a fallback; keep the source at the largest rendered size, not the camera original.
- Always set `width` and `height` or `aspect-ratio` so the box is reserved before the bytes arrive.
- Use `srcset` and `sizes` so a phone does not download a desktop hero.
- `loading="lazy"` below the fold only. The LCP image must not be lazy; it gets `fetchpriority="high"` and no lazy hint.
- Decode off the main thread with `decoding="async"` on non-critical images; keep the LCP image eager.

### Fonts

- Subset to the scripts and weights actually used; drop unused weights.
- `font-display: swap` for body text; `optional` or preload for display type that must not shift.
- Preload only the font files used above the fold, and match metrics with `size-adjust` or a fallback stack to reduce CLS.
- Self-host where policy allows; a third-party font host adds a connection and a privacy question.

### JavaScript and CSS

- Split by route and load on interaction. A modal, chart library, or editor rarely belongs in the initial bundle.
- Keep the shell interactive fast: hydrate only the parts that need state, or render them on the server.
- Tree shaking only works with statically analyzable imports; avoid barrel files that pull whole packages.
- Remove dead CSS at build time; ship critical CSS inline only when it measurably helps.
- Move work off the main thread (web workers) for parsing, filtering, and heavy formatting.

### Third parties

- Load tags after interaction or after the main content is usable; never let an analytics tag block rendering.
- Give every tag an owner, a purpose, and a removal date. Audit quarterly.
- Prefer server-side or edge collection when the vendor supports it.

### Caching and delivery

- Hashed filenames with long-lived immutable caching for assets; short cache for HTML.
- Compress text with Brotli or gzip; do not compress already-compressed images.
- Use a CDN for static assets and set `preconnect` only for origins actually used early.
- Warm the connection for API origins used during first paint, and avoid redirect chains before the document loads.

## Anti-patterns

- Optimizing a lab score while field LCP stays above 4 s.
- A hero carousel or autoplaying video as the LCP element.
- Importing an entire icon set or UI kit for a handful of components.
- Rendering a long list without pagination or virtualization, then blaming the framework.
- Layout shift patched with a fixed height guessed in CSS instead of reserving the real aspect ratio.
- Analytics, chat, and A/B tools loaded synchronously in the head with no owner.
- Claiming "fast" from a single desktop run on a fast connection.
- Caching HTML for a year and shipping a stale release.

## Verification

1. Record baseline field data for the route: LCP, INP, CLS at the 75th percentile, mobile and desktop, with the date.
2. Reproduce in the lab with a throttled profile and note the device and network settings used.
3. Identify the LCP element in the browser performance panel; confirm it is not lazy, not blocked, and correctly sized.
4. Check CLS in the same run; confirm every image, embed, and ad slot reserves space.
5. Trace one slow interaction: find the long task, name the function, and measure again after the fix.
6. Inspect the network panel: total transferred bytes, render-blocking requests, and third-party origins.
7. Compare before and after with the same page, profile, and build. Report both numbers or report nothing.
8. Add or update a build-time budget check so the regression cannot return silently.

## Related

- `frontend-engineering.md` for state, hydration, and bundle structure decisions.
- `responsive.md` for image sizing, `srcset`, and layout behavior across widths.
- `../../SKILL.md` for the verification protocol and the four completion levels.
- `../patterns/landing-page.md` and `../patterns/ecommerce-checkout.md` for routes where LCP and INP dominate conversion.
