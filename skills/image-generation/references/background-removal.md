# Background Removal Guide

This reference explains the background removal pipeline for website and brand assets.

## Pipeline Architecture

The `remove_background.py` utility uses Python PIL to perform fast, local color-key and chroma masking without heavy external dependencies.

```text
Input Image (JPG or PNG)
       |
       v
Detect Key Color (white, green, chroma, auto)
       |
       v
Compute Euclidean Color Distance per Pixel
       |
       v
Apply Alpha Mask with Edge Feathering
       |
       v
Export Transparent RGBA PNG
```

## CLI Usage

```bash
python skills/image-generation/references/scripts/remove_background.py input.png --output output.png [OPTIONS]
```

### Options

| Flag | Description | Default |
| --- | --- | --- |
| `--mode` | Key detection mode: `auto`, `white`, `green`, `chroma` | `auto` |
| `--key` | Target RGB color tuple `R,G,B` when using `chroma` mode | `255,255,255` |
| `--tolerance` | Color distance threshold (0-255) for full transparency | `32` |
| `--feather` | Pixel transition zone width for soft anti-aliased edge | `2` |
| `--erode` | Shrink the subject mask by N pixels to remove key fringe | `1` |
| `--self-test` | Run built-in unit self test and exit | `False` |

## Best Practices

- Magenta (`--mode chroma --key 255,0,255`): default for portraits, products, logos, and icons. Rarely present in real subjects.
- Green (`--mode green`): use when the subject contains magenta, pink, or purple.
- Cyan (`--mode chroma --key 0,255,255`): use when the subject contains magenta and green.
- White (`--mode white`): legacy. Only for subjects with no white and no pale tones.
- Auto Detect (`--mode auto`): samples the 8-pixel perimeter border to detect a flat dominant background.
- Despill: edge pixels are decontaminated from the key color before saving, which removes colored halos on hair and thin details.
- Erosion: `--erode 1` (default) shrinks the mask by one pixel to kill the residual rim. Use 2 when a visible outline survives.
- Feathering: `--feather 4` is a good default. Use 10-14 for soft hair transitions.
