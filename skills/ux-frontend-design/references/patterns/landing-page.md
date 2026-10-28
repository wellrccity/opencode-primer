# Landing Page

Use when: building or reviewing a marketing page whose job is to move a
specific audience to one measurable action.

## Layout and hierarchy

Above-the-fold order, top to bottom:

1. Value proposition: what it is, who it is for, why it beats the alternative.
   One headline, one supporting line. No slogan without a concrete claim.
2. Primary call to action (CTA), visible without scrolling at 375px height 640
   and at 1440px.
3. Secondary CTA, lower emphasis: "see pricing", "watch demo". Never two
   equal-weight buttons.
4. Proof placed near the claim it supports, not parked in a logo wall at the
   bottom.

Sections after the fold, in the order a skeptical reader asks questions:

| Section | Job | Content rule |
| --- | --- | --- |
| Problem | Name the pain in the reader's words | Two or three sentences |
| Benefits | Outcome per benefit | Benefit headline, feature detail under it |
| How it works | Reduce perceived effort | Three steps maximum |
| Proof | Remove doubt | Named source, real number or real quote only |
| Objections | Pre-empt the top three refusals | Price, switching cost, trust |
| Pricing teaser | Anchor and qualify | Real starting price or a range |
| FAQ | Answer the residual blocker | 5 to 8 questions, no filler |
| Final CTA | Repeat the single action | Same label as the primary CTA |
| Footer | Legal, contact, navigation | No new persuasion |

Mobile order: headline, CTA, proof line, then sections in the same order.
Collapse the benefit grid to a single column; do not reorder benefits.

## Required states

- Default, hover, focus, active, disabled for every CTA.
- Loading state on form submit with the button label preserved and a spinner
  plus text, so the label does not vanish.
- Success state with the next step named.
- Error state for each form field and one summary above the form.
- Empty and failure state for any embedded widget: video, calendar, chat.
- Long-copy state: the headline at 200 percent text zoom must not clip or
  overlap the CTA.

## Interaction rules

- One primary action per page. Every other link is visually subordinate.
- Sticky header only when it is short and does not cover anchor targets;
  offset anchor scroll by the header height.
- Anchor links use real `id` targets and keep the URL shareable.
- Forms ask for the minimum: name plus one contact field unless qualification
  is the point of the offer.
- FAQ uses native `details`/`summary` or a button with `aria-expanded`.
- No auto-playing media with sound. Autoplay video is muted, pausable, and not
  the LCP element unless it is a poster image.
- Exit intent modals and chat bubbles must not cover the primary CTA on mobile.

## Data and edge cases

- Pricing: show currency, billing period, and what is excluded. Handle missing
  price for the visitor's region with a clear fallback, not a blank block.
- Testimonials: real person, role, company, and permission on file. If the
  quote is edited, say "edited for length".
- Counters and usage numbers come from a data source with a date; otherwise
  omit them.
- Localization: layouts tolerate strings 30 percent longer than English.
- No JavaScript: headline, CTA, and proof remain readable; the form may fail
  gracefully with a server fallback.
- Slow network: the page is readable before fonts and analytics load.

## Accessibility

- One `h1`; section headings descend without skipping levels.
- CTA is a link when it navigates, a button when it submits.
- Contrast: 4.5:1 for body text, 3:1 for large text and UI borders (WCAG 2.2
  1.4.3, 1.4.11).
- Focus visible on every interactive element and not obscured by a sticky
  header (2.4.11).
- Decorative images use empty `alt`; informative images describe the content,
  not the file.
- Video has captions; motion respects `prefers-reduced-motion`.
- Target size at least 24x24 CSS px (2.5.8); 44x44 recommended for mobile CTAs.

## Performance

- LCP image is a compressed modern format with explicit width and height,
  `fetchpriority="high"`, and not lazy loaded.
- Everything below the fold is lazy loaded; third-party scripts are deferred
  and audited.
- Target: LCP 2.5 s or less and CLS 0.1 or less at the 75th percentile
  (Core Web Vitals). Label any tighter internal budget as a project decision.
- Fonts: subset, `font-display: swap`, preload the one weight used in the hero.
- SEO: descriptive `title` and meta description, canonical URL, one `h1`,
  semantic sections, and Open Graph tags. Marketing copy in the HTML, not
  injected by script.

## Anti-patterns

- Hero plus three feature cards with no brand idea and no proof.
- Fabricated urgency ("only 2 seats left") or invented customer counts.
- Confirmshaming decline links and pre-checked consent.
- Carousel as the hero: content is missed and it fights LCP.
- Vague CTA labels: "Learn more", "Get started" with no object.
- Fake dashboards or stock photos standing in for the product.
- Hidden fees revealed at checkout.
- Section count used as a proxy for persuasiveness.

## Checklist

- [ ] Value proposition states audience, outcome, and differentiator in the
      first viewport at 375x640.
- [ ] Exactly one primary CTA per page; label is verb plus object.
- [ ] Primary CTA reachable with Tab within the first 10 focus stops.
- [ ] Every claim has a source, a measurement, or is removed.
- [ ] Top three objections each answered in a named section.
- [ ] FAQ answers are in the DOM, not fetched on open.
- [ ] 320px width: no horizontal scroll, no clipped headline, CTA full width.
- [ ] 200 percent zoom: no text overlap and no content lost.
- [ ] Keyboard-only pass completes the form and reaches confirmation.
- [ ] LCP element identified in devtools and measured; value recorded.
- [ ] Console has no errors and no failed requests on load.
- [ ] `title`, meta description, canonical, and `h1` present and unique.
