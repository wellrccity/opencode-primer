# SEO

Load when: a page must be found in search, a route is invisible to crawlers, or metadata, URLs, redirects, and structured data are being designed or audited.

## Principles

- Search engines index documents, not screenshots. If the content and links are not in the HTML a crawler receives, they do not exist for indexing.
- One URL, one canonical document. Duplicates split signals and confuse analytics.
- Titles and headings describe the page for a human first; the crawler reads the same text.
- Semantic HTML is the cheapest SEO win: real headings, real lists, real links with real `href` values.
- Content usefulness beats metadata tricks. There is no verified shortcut that replaces answering the search intent.
- Accuracy is mandatory for structured data. Markup that claims ratings, prices, or availability that the page does not show is a defect.
- Server-rendered or statically generated HTML is the safest crawlable baseline; client rendering adds a second dependency.
- Measure with real crawl and search console data when available; do not invent ranking rules or traffic numbers.

## Decision rules

### Page-level metadata

| Element | Rule | Notes |
| --- | --- | --- |
| `<title>` | Unique per page, specific, front-loaded with the primary topic | Length is a display convention, not a ranking factor; keep the meaningful words first |
| Meta description | Unique, factual summary of the page | Not a ranking factor; it influences the snippet |
| `<h1>` | One per page, matching the page topic | Not a magic keyword slot |
| Canonical | Absolute URL of the preferred version | Self-referencing on normal pages |
| `robots` meta | Only when a page must not be indexed | Prefer `X-Robots-Tag` for non-HTML files |
| Open Graph and social tags | Accurate title, description, image | Social previews, not ranking |

### URL design

- Lowercase, hyphen-separated, stable, human-readable paths. No session IDs, no tracking parameters in canonical URLs.
- One path per resource. Changing a path requires a permanent redirect from the old one.
- Query parameters belong to filtering and pagination; declare how they are handled.
- Keep the hierarchy shallow enough to read: `/section/topic/item` is usually enough.

### Status codes and redirects

| Code | Meaning | Use |
| --- | --- | --- |
| 200 | OK | The live page |
| 301, 308 | Permanent redirect | Moved content; pass the signal to the new URL |
| 302, 307 | Temporary redirect | Short-lived moves, A/B tests, maintenance |
| 304 | Not modified | Conditional requests |
| 404 | Not found | Missing resource; return a helpful page with navigation |
| 410 | Gone | Deliberately removed content |
| 5xx | Server error | Never use for missing content |

- Redirect chains longer than one hop waste crawl budget and latency; collapse them.
- Redirect to the closest equivalent URL, not always the home page.
- Do not redirect every unknown URL to the home page; that hides broken links.

### Indexability

- `robots.txt` controls crawling, not indexing. Use `noindex` for removal.
- Keep staging, admin, search results, and internal filters out of the index.
- A sitemap lists canonical, indexable URLs only, and is referenced from `robots.txt`.
- `hreflang` pairs must be reciprocal and point to real, canonical variants.

## Implementation patterns

### Semantic structure

- Use `header`, `nav`, `main`, `article`, `section` with a heading, `footer`, and `aside` only when the content is genuinely complementary.
- Heading levels follow document structure; do not pick `h3` for its font size, and never skip a level to style it.
- Anchor text describes the destination: "view the pricing table", not "click here".
- Internal links connect related pages; a page reachable only from the sitemap is effectively orphaned.

### Rendering and crawlability

- Server-render or pre-render routes that must rank, including the main content and internal links.
- Do not gate primary content behind interaction, tabs rendered on click, or infinite scroll with no paginated equivalent.
- Lazy loading images is fine; lazy loading the body text is not.
- Ensure `robots.txt` does not block the JS and CSS bundles the page needs to render.

### Structured data

- Add JSON-LD only for facts visible on the page: organization, product, article, breadcrumb, FAQ that is actually present.
- Validate with a schema validator and recheck after content changes.
- One accurate type beats several speculative ones. Missing markup is not a defect; false markup is.

### Content and intent

- Match the page to the query intent: informational, navigational, commercial, or transactional. A product page that only explains a concept does not satisfy a buying query.
- Write a unique first paragraph that states what the page answers.
- Avoid near-duplicate pages for every city, variant, or filter; consolidate or differentiate.
- Update or remove stale pages instead of leaving them indexed.

## Anti-patterns

- Text baked into images, canvas, or video with no HTML equivalent.
- Keyword stuffing in titles, alt text, or hidden blocks.
- A single-page app with an empty HTML shell and client-only routing for public content.
- The same title and description on every route.
- Canonical tags pointing to a different page for convenience.
- `noindex` and a sitemap entry for the same URL.
- Fake review, rating, price, or availability markup.
- Redirecting removed content to the home page in bulk.
- Blocking CSS or JS in `robots.txt` and then expecting correct rendering.

## Verification

1. Fetch the raw HTML with scripts disabled and confirm the primary content, headings, and internal links are present.
2. List every route in the build and check for a unique title, meta description, and one `h1`.
3. Confirm canonical URLs are absolute, self-referencing on standard pages, and consistent with the sitemap.
4. Check status codes for every entry in the sitemap and for known old URLs; record each redirect hop.
5. Validate structured data and compare each claim against visible page content.
6. Run a crawl of the built site when a crawler is available; review orphan pages, duplicate titles, and broken links.
7. Review search console coverage and query data when access exists; record the date of the data.
8. Recheck after deploy: crawlability of new routes, canonical tags, and sitemap freshness.

## Related

- `accessibility.md` for semantics that serve both assistive technology and crawlers.
- `performance.md` for rendering strategy and crawl budget spent on slow responses.
- `../patterns/landing-page.md` for commercial page structure and metadata.
- `../patterns/institutional-site.md` for content architecture across many routes.
