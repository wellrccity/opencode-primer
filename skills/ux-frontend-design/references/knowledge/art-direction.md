# Art direction: choosing a visual idea

Load when: a project has no visual direction, or the result looks generic and
must be made specific to a brand and audience.

## Principles

- Art direction is a decision, not a decoration pass. Name the idea in one
  sentence before touching code.
- Fit beats novelty. A direction that fits the audience and the product beats a
  fashionable one that fights both.
- Copying a competitor's surface copies their positioning at second hand.
  Analyze structure and intent, then build a distinct surface.
- One deliberate idea is stronger than five. Everything else supports it.
- The same template applied to every project is the definition of generic.
  Direction must change when the brief changes.

## Decision rules

How to pick references:

1. Collect 5-8 references across three buckets: same category, adjacent
   category, and out-of-category craft (print, signage, editorial, packaging).
2. For each, write what it does structurally: hierarchy, grid, type behavior,
   color weight, density, motion.
3. Write what it would cost to reproduce and whether that cost buys the brand
   anything.
4. Write at least three anti-references: what this project must not look like.
5. Extract, do not trace. Never ship a layout that is recognizable as one
   specific source.

Style families and fit:

| Family | Fits when | Fails when |
| --- | --- | --- |
| Minimal | Clarity is the product; content is strong; decisions are few | Trust needs density, or the brand has no distinctive assets |
| Editorial | Long-form, point of view, publishing, culture | Task-driven operator tools needing scan speed |
| Brutalist | Deliberate contrast, youth, art, developer tools | Regulated, trust-first, or accessibility-sensitive contexts |
| Corporate | Enterprise buyers, procurement, risk reduction | Early-stage products needing personality |
| Playful | Consumer, low risk, onboarding, education | Finance, health, legal, or grief-adjacent contexts |
| Luxury | Scarcity, craft, high price, restraint | High-frequency utility, price-led positioning |
| Utilitarian | Operations, dashboards, repeat use, speed | Brand-led acquisition pages |
| Data-dense | Analysts, monitoring, expert tooling | First-time consumer tasks |

Direction axes, choose one position per axis:

- Density: airy to dense.
- Contrast: low and soft to hard and graphic.
- Type voice: neutral to expressive.
- Color: monochrome plus accent to full spectrum.
- Imagery: photographic to illustrated to typographic-only.
- Motion: near-static to kinetic.
- Surface: flat to textured to dimensional.

Brand fit test, five questions:

1. If the logo were removed, would a user still guess the category correctly?
2. Does the direction survive being described in one sentence?
3. Can the same idea style a form, a table, and an empty state?
4. Does it hold on a 320 px screen and in dark mode?
5. Would the target audience recognize themselves, or the designer?

## Implementation patterns

Direction brief template:

```text
Audience: <who, in what context, on which device>
Job to be done: <one sentence>
Adjectives (three): <e.g. precise, calm, technical>
References: <3 links or screens> - what to take from each
Anti-references: <3 links or screens> - what to avoid and why>
Type: <display family and role, text family and role>
Color story: <dominant, secondary, accent, semantics>
Imagery: <photography, illustration, product shot, none>
Iconography: <one family, stroke weight, filled or outline>
Texture and surface: <none, paper, grid, noise - and where>
Motion identity: <what moves, duration family, what never moves>
Density: <airy or dense, per surface>
The one idea: <one sentence a reviewer can verify>
```

Type pairing:

- Pair by role, not by fashion: display for voice, text for reading, mono for
  data and code.
- Contrast pairing works when the two families differ in structure, not just in
  weight.
- Two families plus one mono is the practical maximum. Label fonts need a
  working weight, not a third family.

Color story:

- Pick a dominant field, one accent for action, and a semantic set. Derive
  surfaces and borders from the dominant field so the UI stays coherent.
- Test the palette on a dense table and on a marketing hero. A palette that
  only works on one is incomplete.

Motion identity:

- Define what the product never animates (data values, legal text, prices).
- Keep one duration family and one easing family. Identity comes from
  consistency, not from variety.

Anti-generic review, run before build:

- Remove one of the three feature cards; if the layout collapses, it was a
  template, not a design.
- Replace the hero with a typographic statement; if the page loses nothing, the
  imagery was decoration.
- Check that at least one element could only belong to this product.

## Brand fidelity

When the brief names an existing brand, differentiation happens inside its
recognizable system, not against it.

1. List three cues a customer would recognize without the logo: color, type
   shape, corner radius, icon style, tone, or motion.
2. Preserve at least two of the three in the first screen.
3. Choose one differentiator that does not contradict the brand promise.
4. Run the no-logo test: hide the logo and ask whether the screen still reads
   as the same category and still carries at least two of the cues.
5. Record the cues and the differentiator in the direction brief.

If the brand has no usable visual assets, list the category conventions and the
brand promise, then choose cues from those and record the assumption.

## Anti-patterns

- Reference copied pixel for pixel, including the competitor's weak spots.
- Three adjectives that apply to any product ("modern, clean, friendly").
- Direction described only as a mood board with no type or spacing decisions.
- Gradient hero with no hierarchy role.
- Mixed icon families or emoji used as professional icons.
- Stock photography of people pointing at screens.
- Generic 3D blobs or abstract glass shapes standing in for a brand idea.
- Expressive display type used for dense UI labels.
- Motion on every element, so nothing reads as important.
- Same dark-plus-neon template applied to a clinic and to a game studio.
- A direction that is distinctive but belongs to a different brand category.

## Verification

- Write the one-sentence idea and test it against three screens: does it
  survive in each?
- Screenshot desktop and 320 px, light and dark, and confirm the direction still
  reads.
- Count distinct type sizes, colors, radii, and shadow levels used. Anything
  outside the brief is either documented or removed.
- Run the anti-generic review above and record the result.
- Hide the logo and confirm at least two brand cues survive.
- Check that every font in use is licensed and actually loaded, not guessed.

## Related

- `ui-design.md` for turning the direction into tokens and components.
- `marketing-cro.md` when the direction serves a conversion page.
- `../../MODERN_UX_PLAYBOOK.md` for contemporary pattern expectations.
- `../../checklists/visual-review.md` for the screenshot evidence pass.
