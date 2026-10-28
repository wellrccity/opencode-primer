# UI design: type, color, space, systems

Load when: choosing type, color, spacing, grid, elevation, or extending the
project's component system.

## Principles

- Design decisions become tokens, tokens become components, components become
  screens. Skipping a layer produces one-off values that cannot be maintained.
- Every value must be repeatable. If a spacing value appears once, it is either
  deliberate or an accident; know which.
- Contrast, target size, and focus visibility are floors, not style choices.
- Hierarchy comes from a small number of levers used consistently: size,
  weight, color, space. Adding more levers weakens all of them.
- Optical alignment beats numeric alignment. Text and icons rarely look
  centered when measured.
- Dark mode is a second palette, not an inverted one.

## Decision rules

Typography:

| Decision | Rule |
| --- | --- |
| Measure | 45-75 characters per line for body text |
| Line height | Body 1.4-1.6; headings 1.1-1.3; relax as measure widens |
| Body size | 16 CSS px minimum for primary reading text |
| Scale | One modular scale, 5-7 steps, not ad-hoc sizes per screen |
| Weight | Two weights for most products; three maximum |
| Fluid type | `clamp()` between a readable minimum and a capped maximum |
| Alignment | Left-aligned body text; avoid justified text on the web |
| Numerals | Tabular figures inside tables and aligned sums |

Color:

- Define roles, not colors: surface, surface-muted, border, text, text-muted,
  primary, primary-hover, danger, warning, success, info.
- Text contrast 4.5:1 minimum, 3:1 for large text; non-text UI boundaries and
  focus indicators 3:1.
- Never use color alone to carry meaning. Pair with text, icon, or shape.
- Semantic color stays semantic. Do not use the danger red as decoration.
- Harmony: one dominant neutral family plus one accent plus semantic colors.
  Two competing accents fight for attention on every screen.
- Dark mode: raise surfaces instead of lowering them, reduce saturation of
  bright accents, avoid pure black and pure white text pairs.

Spacing:

- Use a 4 or 8 based scale. Half steps allowed for icon nudges only.
- Proximity encodes grouping. Space between groups must be clearly larger than
  space inside a group; if in doubt, double the outer gap.
- Density modes: comfortable for reading surfaces, compact for data tables and
  operator tools. Density changes spacing, not type size below legibility.

## Implementation patterns

Grid and composition:

- Content column with a max width, plus a consistent outer gutter.
- Align to a shared left edge; a single stray alignment reads as a bug.
- Proportion: do not split a screen into equal halves when one side is the
  task and the other is context. Give weight to the task.
- Composition: one dominant element per viewport region. If two elements
  compete, demote one by size, weight, or color.
- Optical adjustments are legitimate: icon padding, optical centering, cap
  height alignment, and negative tracking on large display type.

Design system layers:

1. Tokens: raw and semantic values (color, space, radius, type, motion).
2. Primitives: unstyled or lightly styled building blocks (stack, field, box).
3. Components: composed, named by role, not by look.
4. Variants: intent (primary, secondary, ghost, danger) and size.
5. States: default, hover, focus-visible, active, disabled, loading, error,
   selected, read-only.
6. Documentation: when to use, when not to, and one live example per variant.

Elevation:

- Use elevation to express layering that matters: modal above page, popover
  above content, sticky header above scrolling content.
- Prefer border plus surface shift over shadow for static grouping.
- One shadow token per level. Stacking two shadows to fake depth reads as noise.

Action hierarchy:

- One primary action per decision region, not per screen. A long form may have
  one primary action per section and one global submit.
- Secondary actions visually recede but stay discoverable.
- Tertiary and destructive actions move to the overflow only when genuinely
  rare; never hide the only escape route.

Consistency rules:

- Same component, same behavior, same label for the same job.
- Radius, border width, and icon stroke come from tokens; mixed values read as
  sloppiness before the user can name why.
- Motion duration and easing come from a small set, reused everywhere.

## Anti-patterns

- Body text below 16 CSS px on a primary reading surface.
- Full-width paragraphs on a 1440 px screen with a 130-character measure.
- Gray-on-gray placeholder used as a label.
- Accent color applied to every interactive element, removing the hierarchy.
- Cards inside cards inside cards.
- Arbitrary radii per component (6, 10, 13, 18 px in one view).
- Shadows on flat lists used as separators.
- Two primaries side by side in the same region.
- Dark mode implemented by CSS invert.
- Icon-only buttons with no accessible name and no tooltip on desktop.
- Spacing chosen by eye per screen instead of from the scale.

## Verification

- Measure body text at the built page: computed font-size and line height, and
  characters per line at 1440 px.
- Run a contrast check on every text/background pair, including muted text and
  disabled-looking-but-readable labels.
- Confirm each interactive element has visible focus and a 3:1 focus indicator.
- Screenshot the same component in all states and compare spacing between them.
- Toggle dark mode and check contrast again; do not assume the light values
  carry over.
- Inspect computed styles for values outside the token set and list them.

## Related

- `art-direction.md` for choosing the visual idea before tokens.
- `accessibility.md` for criterion-level contrast, target, and focus rules.
- `responsive.md` for fluid type scales and breakpoint behavior.
- `../../checklists/visual-review.md` for the screenshot pass.
