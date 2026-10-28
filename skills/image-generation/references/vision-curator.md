# Vision Curator and Consultant Guide

This reference describes how to evaluate and curate generated visual assets using vision-capable models such as `opencode-go/deepseek-v4.1-flash`.

## Purpose

Text-to-image models lack self-evaluation capabilities. When generating assets for websites, the vision curator acts as an automated design reviewer to:
1. Verify prompt alignment (did the model generate what was requested).
2. Assess background purity (can the background be cleanly removed).
3. Check composition, anatomy, and artifact anomalies.
4. Assign a quantifiable quality score (1-10) with actionable revision notes.

## CLI Usage

```bash
python skills/image-generation/references/scripts/curate_image.py --image output.png --prompt "modern minimalist tech logo" [OPTIONS]
```

### Options

| Flag | Description |
| --- | --- |
| `--image PATH` | Path to the generated image file. |
| `--prompt TEXT` | Original prompt used during generation. |
| `--criteria TEXT` | Additional evaluation criteria (for example: minimalist, no text). |
| `--model ID` | Curator model override (default: `opencode-go/deepseek-v4.1-flash`). |
| `--output PATH` | Path to save JSON evaluation report. |

## Evaluation Rubric

- Prompt Match (1-10): Adherence to user prompt and constraints.
- Visual Quality (1-10): Sharpness, absence of blur, compression artifacts, or unwanted distortions.
- Cutout Readiness (1-10): Contrast between subject and background, absence of cast shadows.
- Verdict:
  - `accept`: Score 8 or higher, asset is production-ready.
  - `revise`: Score 5-7, minor adjustments to prompt or tolerance needed.
  - `reject`: Score under 5, severe prompt failure or visual defect.
