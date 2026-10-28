# Prompt Engineering Cookbook for Web and Brand Assets

This reference provides structured prompt patterns for generating web and visual identity assets.

## Global Design Principles

1. State the subject and its purpose first.
2. Specify intentional negative space for typography, headings, or UI buttons.
3. Define studio lighting, flat vector, or 3D render style explicitly.
4. Constrain colors to brand palette keywords.
5. Use negative prompts to exclude unwanted text, watermarks, clutter, and extra artifacts.

## Asset Templates

### 1. Hero Banners (16:9)
- Goal: High-impact banner for landing page headers.
- Dimensions: 1344x768 or 1024x576.
- Prompt:
  ```text
  Wide cinematic hero banner for [brand or product], [central subject], professional studio lighting, clean minimal composition, generous negative space on the left for headline copy, modern corporate palette [color1, color2], sharp focus, 8k resolution, no text, no watermark.
  ```
- Negative Prompt:
  ```text
  text, typography, watermarks, cluttered background, blurry, distorted, crowded composition.
  ```

### 2. Logos and Brand Symbols (1:1)
- Goal: Clean vector mark or emblem.
- Dimensions: 1024x1024.
- Prompt:
  ```text
  Minimalist vector logo for [brand name], [symbol concept], flat 2d graphic, geometric, centered, high contrast, clean bold silhouette, isolated on a pure white background (#FFFFFF), no shadows, no gradients, sharp edges.
  ```
- Negative Prompt:
  ```text
  realistic photo, 3d render, shadows, gradients, bevel, text, lettering, watermark.
  ```

### 3. UI Icons and Spot Illustrations (1:1)
- Goal: Cohesive icons for feature cards and navigation.
- Dimensions: 512x512 or 1024x1024.
- Prompt:
  ```text
  Modern UI icon representing [concept], flat line art with subtle color accents, centered, crisp geometric lines, solid white background (#FFFFFF), high contrast, zero shadows, clean cutout ready.
  ```

### 4. Avatars and Portraits (1:1)
- Goal: Professional profile pictures and customer persona avatars.
- Dimensions: 1024x1024.
- Prompt:
  ```text
  Professional portrait headshot of [demographic or role], friendly confident expression, front facing, studio portrait lighting, isolated on a solid green background (#00FF00), high contrast, clean outline, chroma key ready.
  ```

## Background-Removable Prompt Recipes

Rule: the background must be a saturated key color that appears nowhere in the
subject. State the exclusion explicitly, including clothing, props, and
reflections. Magenta is the default because it is rare in real subjects.

1. Always specify the key color and its hex code.
2. Add: `The color <name> must not appear anywhere in the subject, the clothing, the props, or the reflections.`
3. Add: `Full subject visible with margin, even studio lighting, high contrast between subject and background, crisp clean silhouette, no cast shadow, no floor, no gradient, no texture, no background objects.`
4. These lines are appended automatically by `make_image.py --transparent`.
5. Negative prompt: `drop shadow, ambient occlusion, gradient background, textured background, props, blurry edges, cropped subject, watermark, text`.
6. For icons and logos, also require saturated mid-tone or dark fills; a white
   subject vanishes on a white page after the cutout.

Templates:

```text
magenta: <subject>. Isolated on a completely flat, pure solid magenta background (#FF00FF). The color magenta must not appear anywhere in the subject.
green:   <subject>. Isolated on a completely flat, pure solid green background (#00FF00). The color green must not appear anywhere in the subject.
cyan:    <subject>. Isolated on a completely flat, pure solid cyan background (#00FFFF). The color cyan must not appear anywhere in the subject.
```

Do not rely on `background: transparent` request parameters. The local server
accepts the flag and returns an opaque RGB image, so transparency is always a
post-processing step.
