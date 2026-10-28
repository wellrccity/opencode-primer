---
name: image-generation
description: Use when generating website assets, brand visuals, icons, and hero banners with configurable image models, background removal, and vision curation.
---

# Image generation

Generate website and brand assets with configurable image models, remove flat
backgrounds to transparent PNGs, and curate results with a vision model when the
generator has no vision capability.

## Overview

Purpose: site building, brand identity, and UI assets. One script does the whole
pipeline:

```
python .../references/scripts/make_image.py "PROMPT" -o PATH
```

Add `--transparent` for a cutout PNG with alpha. Credentials, provider, model,
and size presets are resolved automatically from the environment.

The skill also covers the three underlying flows separately:

1. Generate an image with a configured provider.
2. Remove a flat background (white, green, chroma, or auto) to a transparent PNG.
3. Curate the result with a multimodal LLM that scores prompt fidelity and
   visual quality.

Assets covered: hero banners, logos and symbols, UI icons, team avatars and
portraits, textures and backgrounds, and cutout-ready subjects.

## Model configuration

Providers are selected through environment variables.

Default model: `cf:leonardo/phoenix-1.0` (Leonardo Phoenix, photorealistic, best
free Cloudflare option). Local API: `local:gpt-image-2.5-sunburst`.

Supported models, ranked by measured output quality:

| Alias | Provider | Notes |
| --- | --- | --- |
| `local:gpt-image-2.5-sunburst` | local | Best realism and prompt adherence. Requires the local server. |
| `cf:black-forest-labs/flux-2-dev` | cloudflare | Excellent realism, slowest (~14 s). Multipart API. |
| `cf:black-forest-labs/flux-2-klein-9b` | cloudflare | Excellent realism, fast (~3 s). Multipart API. |
| `cf:leonardo/phoenix-1.0` | cloudflare | Very good realistic portraits, fast. Default. |
| `cf:stabilityai/stable-diffusion-xl-base-1.0` | cloudflare | Acceptable, glossy. Supports negative prompt. |
| `cf:black-forest-labs/flux-1-schnell` | cloudflare | Acceptable, no negative prompt. |
| `cf:lykon/dreamshaper-8-lcm` | cloudflare | Poor color handling, avoid. |
| `cf:bytedance/stable-diffusion-xl-lightning` | cloudflare | Cartoonish and plastic. Avoid for realism. |
| `openai:dall-e-3`, `openai:gpt-image-1` | openai | Paid. |

Configuration variables:

- `IMAGE_GEN_MODEL` - selected model alias or provider model id.
- `IMAGE_GEN_PROVIDER` - override provider (`local`, `cloudflare`, `openai`, `custom`).
- Local server:
  - `LOCAL_IMAGE_BASE_URL` (default `http://127.0.0.1:8790/v1`)
  - `LOCAL_IMAGE_MODEL` (default `gpt-image-2.5-sunburst`)
- Cloudflare:
  - `CLOUDFLARE_ACCOUNT_ID`
  - `CLOUDFLARE_API_TOKEN`
- OpenAI:
  - `OPENAI_API_TOKEN`
  - `OPENAI_BASE_URL` (default `https://api.openai.com/v1`)
- Custom:
  - `CUSTOM_IMAGE_ENDPOINT`
  - `CUSTOM_IMAGE_API_TOKEN`

Resolution rules:

- `local:<model>` routes to the local OpenAI-compatible server.
- `@cf/...` routes to Cloudflare; `cf:<model>` resolves through the registry.
- `IMAGE_GEN_PROVIDER` overrides the inferred provider.
- Unknown values pass through to the `custom` provider.

The local server returns `data[0].file` (absolute path), `url`, or `b64_json`.
All three are handled. It deletes the source file after responding, so the
script copies bytes immediately.

Known limits of the local server: `background: "transparent"` is accepted but
ignored (output is RGB with a white plate), and `size` is not honored (output
is about 1254x1254). Treat transparency as a post-processing step.

Values may be placed in a `.env` file in the working directory or next to the
scripts. Existing process environment always wins.

## Background removal flow

Cutouts are produced in two steps: generate over a flat key color, then remove
that color. `--transparent` does both in one command.

Key color rule: the background color must be a saturated hue that does not exist
anywhere in the subject. The prompt states that explicitly, including clothing,
props, and reflections. Default key: magenta `#FF00FF`, which almost never
appears in photos, logos, or clothing, unlike white.

| Key | When to use |
| --- | --- |
| `magenta` (`#FF00FF`) | Default. Best for portraits, products, logos, icons. |
| `green` (`#00FF00`) | Subjects containing magenta, pink, or purple. |
| `cyan` (`#00FFFF`) | Subjects containing magenta and green. |
| `white` (`#FFFFFF`) | Legacy. Only for subjects with no white and no pale tones. |

Removal is chroma based: Euclidean distance to the key plus a hue-dominance test
for saturated keys, edge despill, alpha feathering, and 1 px mask erosion to kill
fringe. For `icon` and `logo` presets the prompt also forbids white or near-white
subjects, so the cutout stays visible on a white page.

Tuning, when a halo survives:

- `--tolerance` (default 60): raise to 100-140 for hair edges on magenta.
- `--feather` (default 4): raise to 10-14 for soft hair transitions.
- `--erode` (default 1): raise to 2 when a colored rim remains.

CLI: `python skills/image-generation/references/scripts/remove_background.py`.

## Vision curator flow

When the image generator has no vision capability, evaluate the output with a
multimodal LLM. Default curator: `opencode-go/deepseek-v4.1-flash`.

Variables:

- `OPENCODE_API_TOKEN` (required for the curator)
- `OPENCODE_BASE_URL` (default `https://api.opencode.ai/v1`)
- `OPENCODE_MODEL` (default `opencode-go/deepseek-v4.1-flash`)

The curator returns a JSON report with `score` (1-10), `verdict`
(`accept`, `revise`, `reject`), `issues`, and `suggestions`. If the model
rejects image input, a local fallback evaluates metadata, dimensions, file
size, and prompt only, and marks the result as fallback.

CLI: `python skills/image-generation/references/scripts/curate_image.py`.

## Paths and credentials

Resolve the script directory once and reuse it. Never search, copy, or edit the
OpenCode config directory, and never invent alternative paths.

- Repository checkout: `skills/image-generation/references/scripts/`
- Global install: `~/.config/opencode/skills/image-generation/references/scripts/`

Credentials are read in this order, first match wins:

1. Process environment.
2. `IMAGE_GEN_ENV_FILE`, when set.
3. `./.env` in the current working directory.
4. `.env` next to the skill directory, then up to two parent levels.
5. `~/.config/opencode/.env`.

Missing credentials fail fast with exit code 2 and a message listing the
searched paths. Treat that as a configuration problem: report it and stop. Do
not modify unrelated files, do not retry with invented paths, and do not read
the whole config tree.

## Quick start: one command

`make_image.py` loads credentials, picks the provider and model, applies the
background prompt when needed, and writes the file. The only required inputs
are the prompt and the output path.

```
python skills/image-generation/references/scripts/make_image.py "PROMPT" -o PATH
```

Transparent PNG in one step (generates on white, then removes the background):

```
python skills/image-generation/references/scripts/make_image.py "PROMPT" -o PATH.png --transparent
```

Called from the global install, use the absolute path once:

```
python "%USERPROFILE%\.config\opencode\skills\image-generation\references\scripts\make_image.py" "PROMPT" -o PATH
```

Useful flags:

| Flag | Meaning |
| --- | --- |
| `-p, --preset` | `hero`, `banner`, `logo`, `icon`, `avatar`, `texture`, `portrait`, `landscape`, `square`. |
| `-m, --model` | Override the configured model. |
| `-t, --transparent` | One-shot cutout: key-color background prompt plus removal to PNG. |
| `--cutout-color` | `magenta` (default), `green`, `cyan`, `white`. Pick one absent from the subject. |
| `--tolerance`, `--feather`, `--erode` | Cutout tuning; see the removal flow above. |
| `--background` | `none`, `white`, `green` when you want the flat plate kept. |
| `--curate` | Run the vision curator after generation. |
| `--dry-run` | Print the resolved plan and credential status, call nothing. |

The script prints a compact JSON report with `path`, `model`, `provider`,
`bytes`, and, for cutouts, `removed_pixels` and `total_pixels`.

## CLI reference (granular scripts)

Generate an image:

```
python skills/image-generation/references/scripts/generate_image.py \
  --prompt "..." [--negative "..."] [--model ID] \
  [--width N] [--height N] [--steps N] [--seed N] \
  [--background none|white|green] --output PATH
```

Dry run (prints resolved model without generating):

```
python skills/image-generation/references/scripts/generate_image.py --dry-run
```

Remove a background:

```
python skills/image-generation/references/scripts/remove_background.py \
  INPUT --output OUTPUT [--mode auto|white|green|chroma] \
  [--key R,G,B] [--tolerance N] [--feather N]
```

Self-test the remover:

```
python skills/image-generation/references/scripts/remove_background.py --self-test
```

Curate an image:

```
python skills/image-generation/references/scripts/curate_image.py \
  --image PATH --prompt "..." [--criteria TEXT ...] [--output PATH]
```

## Recommended pipeline

1. Choose a prompt recipe from `references/prompt-cookbook.md`.
2. Generate with the matching `--background` and size.
3. Remove the background (if the recipe uses white or green).
4. Curate with the original prompt and brand criteria.
5. Accept, revise, or reject based on the verdict; iterate if needed.

## References

- `references/prompt-cookbook.md` - prompt recipes for websites and brand identity.
- `references/background-removal.md` - removal algorithms, modes, and tuning.
- `references/vision-curator.md` - vision curation and evaluation rubric.