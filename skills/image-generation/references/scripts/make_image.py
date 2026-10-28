"""One-shot image generation entrypoint.

Handles credentials, provider selection, background prompting, optional
background removal, and optional vision curation in a single command.

Usage:
    python make_image.py "prompt" -o output.png
    python make_image.py "prompt" -o logo.png --preset logo --transparent
    python make_image.py "prompt" -o hero.jpg --preset hero
    python make_image.py "prompt" -o check.png --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from common import (
    DEFAULT_CUTOUT_COLOR,
    MissingEnvError,
    SKILL_ROOT,
    env_search_paths,
    get_env,
    load_environment,
    resolve_model,
)

PRESETS: Dict[str, Tuple[int, int]] = {
    "hero": (1344, 768),
    "banner": (1536, 864),
    "logo": (1024, 1024),
    "icon": (512, 512),
    "avatar": (1024, 1024),
    "texture": (1024, 1024),
    "square": (1024, 1024),
    "portrait": (864, 1152),
    "landscape": (1152, 864),
}

CUTOUT_COLORS: Dict[str, Tuple[int, int, int]] = {
    "magenta": (255, 0, 255),
    "green": (0, 255, 0),
    "cyan": (0, 255, 255),
    "white": (255, 255, 255),
}

CUTOUT_COLOR_NAMES = {
    "magenta": ("magenta", "#FF00FF"),
    "green": ("green", "#00FF00"),
    "cyan": ("cyan", "#00FFFF"),
    "white": ("white", "#FFFFFF"),
}

CUTOUT_NEGATIVE = (
    "drop shadow, ambient occlusion, gradient background, textured background, "
    "props, blurry edges, cropped subject, watermark, text"
)

PROVIDER_REQUIREMENTS = {
    "cloudflare": ("CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"),
    "openai": ("OPENAI_API_TOKEN",),
    "local": (),
    "custom": ("CUSTOM_IMAGE_ENDPOINT",),
}


def cutout_prompt(prompt: str, color: str, avoid_white: bool = False) -> str:
    """Add a solid, collision-free background clause for later removal."""
    name, hex_code = CUTOUT_COLOR_NAMES[color]
    base = (
        "%s. Isolated on a completely flat, pure solid %s background (%s). "
        "The color %s must not appear anywhere in the subject, the clothing, "
        "the props, or the reflections. Full subject visible with margin, "
        "even studio lighting, high contrast between subject and background, "
        "crisp clean silhouette, no cast shadow, no floor, no gradient, "
        "no texture, no background objects." % (prompt, name, hex_code, name)
    )
    if avoid_white:
        base += (
            " The subject must stay visible on a white page: use saturated "
            "mid-tone or dark colors, never white or near-white fills."
        )
    return base


def _preflight(provider: str) -> Dict[str, str]:
    """Validate credentials for the resolved provider and return config."""
    required = PROVIDER_REQUIREMENTS.get(provider, ())
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        searched = ", ".join(str(path) for path in env_search_paths())
        raise MissingEnvError(
            "Missing credentials for provider '%s': %s\n"
            "Add them to one of these files: %s\n"
            "Do not search the filesystem for them."
            % (provider, ", ".join(missing), searched)
        )
    return {name: str(os.environ.get(name, "")) for name in required}


def _detect_provider() -> str:
    """Pick the provider from explicit config, then available credentials."""
    explicit = os.environ.get("IMAGE_GEN_PROVIDER")
    if explicit:
        return explicit.strip().lower()
    model = os.environ.get("IMAGE_GEN_MODEL", "")
    if model.startswith("local:"):
        return "local"
    if model.startswith("@cf/") or model.startswith("cf:"):
        return "cloudflare"
    if model.startswith("openai:"):
        return "openai"
    if os.environ.get("LOCAL_IMAGE_BASE_URL"):
        return "local"
    if os.environ.get("CLOUDFLARE_ACCOUNT_ID") and os.environ.get(
        "CLOUDFLARE_API_TOKEN"
    ):
        return "cloudflare"
    if os.environ.get("OPENAI_API_TOKEN"):
        return "openai"
    if os.environ.get("CUSTOM_IMAGE_ENDPOINT"):
        return "custom"
    return ""


def _default_model(provider: str) -> Optional[str]:
    if provider == "cloudflare":
        return "cf:leonardo/phoenix-1.0"
    if provider == "local":
        return "local:" + str(
            os.environ.get("LOCAL_IMAGE_MODEL", "gpt-image-2.5-sunburst")
        )
    if provider == "openai":
        return "openai:gpt-image-1"
    if provider == "custom":
        return "custom"
    return None


def _size_for(args: argparse.Namespace) -> Tuple[int, int]:
    if args.width and args.height:
        return int(args.width), int(args.height)
    if args.size:
        parts = args.size.lower().replace("x", " ").replace("*", " ").split()
        if len(parts) == 2 and all(part.isdigit() for part in parts):
            return int(parts[0]), int(parts[1])
        raise ValueError("--size must look like 1024x1024")
    return PRESETS.get(args.preset, PRESETS["square"])


def _ensure_png(path: Path) -> Path:
    if path.suffix.lower() == ".png":
        return path
    return path.with_suffix(".png")


def run(args: argparse.Namespace) -> int:
    load_environment(args.env_file)

    provider = _detect_provider()
    model = args.model or os.environ.get("IMAGE_GEN_MODEL") or _default_model(provider)

    if not provider and not args.model and not os.environ.get("IMAGE_GEN_MODEL"):
        raise MissingEnvError(
            "No image provider configured.\n"
            "Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN in: %s\n"
            "Do not search the filesystem for them."
            % ", ".join(str(path) for path in env_search_paths())
        )

    spec = resolve_model(model)
    width, height = _size_for(args)
    output = Path(args.output).expanduser()
    cutout = bool(args.transparent)

    prompt = args.prompt.strip()
    if not prompt:
        raise ValueError("A prompt is required.")
    cutout_color = args.cutout_color if args.cutout_color in CUTOUT_COLORS else None
    if cutout_color is None and args.cutout_color:
        raise ValueError(
            "--cutout-color must be one of: %s" % ", ".join(sorted(CUTOUT_COLORS))
        )
    if cutout:
        background = "none"
        prompt = cutout_prompt(
            prompt,
            cutout_color or "magenta",
            avoid_white=args.preset in ("icon", "logo"),
        )
    else:
        background = args.background
        if background == "green":
            prompt = (
                prompt + ", isolated on a pure solid green background (#00FF00), "
                "chroma key ready, no shadows, no gradients"
            )

    negative = args.negative or (CUTOUT_NEGATIVE if cutout else None)

    plan: Dict[str, Any] = {
        "model": spec.id,
        "provider": spec.provider,
        "remote_model": spec.remote_model,
        "width": width,
        "height": height,
        "background": background,
        "transparent": cutout,
        "cutout_color": (cutout_color or "magenta") if cutout else None,
        "output": str(output),
    }

    if args.dry_run:
        plan["credentials"] = _credentials_status(spec.provider)
        print(json.dumps(plan, indent=2))
        return 0

    _preflight(spec.provider)

    from generate_image import GenerationRequest, generate

    result = generate(
        GenerationRequest(
            prompt=prompt,
            negative_prompt=negative,
            width=width,
            height=height,
            steps=args.steps,
            seed=args.seed,
            output=output,
            background_mode=background if not cutout else "none",
            model=spec.id,
        )
    )

    report: Dict[str, Any] = {
        "path": str(result.path),
        "model": result.model,
        "provider": result.provider,
        "bytes": result.bytes,
        "mime": result.mime,
        "preset": args.preset,
    }

    if cutout:
        from remove_background import remove_background

        key_color = CUTOUT_COLORS[cutout_color or "magenta"]
        cut_path = _ensure_png(output)
        cut_image = remove_background(
            result.path,
            cut_path,
            mode="chroma",
            key_color=key_color,
            tolerance=args.tolerance,
            feather=args.feather,
            erode=args.erode,
        )
        alpha = cut_image.getchannel("A")
        total = cut_image.size[0] * cut_image.size[1]
        removed = alpha.histogram()[0] if hasattr(alpha, "histogram") else 0
        report["path"] = str(cut_path)
        report["bytes"] = cut_path.stat().st_size
        report["mime"] = "image/png"
        report["transparent"] = True
        report["key_color"] = "rgb%s" % (key_color,)
        report["removed_pixels"] = removed
        report["total_pixels"] = total
        if cut_path != Path(result.path):
            try:
                Path(result.path).unlink()
            except OSError:
                pass

    if args.curate:
        from curate_image import evaluate

        evaluation = evaluate(
            image_path=report["path"],
            prompt=args.prompt,
            criteria=args.criteria or None,
            output=args.curate_output,
        )
        report["curator"] = {
            "score": evaluation.score,
            "verdict": evaluation.verdict,
            "issues": evaluation.issues,
            "suggestions": evaluation.suggestions,
            "fallback": evaluation.fallback,
        }

    print(json.dumps(report, indent=2))
    return 0


def _credentials_status(provider: str) -> Dict[str, str]:
    status = {}
    for name in PROVIDER_REQUIREMENTS.get(provider, ()):
        status[name] = "set" if os.environ.get(name) else "missing"
    return status


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate an image in one command. Credentials are loaded automatically."
    )
    parser.add_argument("prompt", help="What to generate.")
    parser.add_argument("-o", "--output", required=False, help="Output image path.")
    parser.add_argument("-m", "--model", help="Model alias or provider model id.")
    parser.add_argument(
        "-p",
        "--preset",
        default="square",
        choices=sorted(PRESETS),
        help="Size preset. Default: square (1024x1024).",
    )
    parser.add_argument("--size", help="Explicit size, for example 1024x1024.")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--negative", help="Extra negative prompt terms.")
    parser.add_argument("--steps", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument(
        "--background",
        default="none",
        choices=["none", "white", "green"],
        help="Force a flat background for later removal.",
    )
    parser.add_argument(
        "-t",
        "--transparent",
        action="store_true",
        help="Generate on a flat key color, then remove the background to a PNG with alpha.",
    )
    parser.add_argument(
        "--cutout-color",
        default=DEFAULT_CUTOUT_COLOR,
        choices=sorted(CUTOUT_COLORS),
        help="Key color used for the cutout background. Default: magenta.",
    )
    parser.add_argument("--tolerance", type=int, default=60)
    parser.add_argument("--feather", type=int, default=4)
    parser.add_argument(
        "--erode",
        type=int,
        default=1,
        help="Shrink the subject mask by N pixels to remove key-color fringe.",
    )
    parser.add_argument(
        "--curate", action="store_true", help="Run the vision curator afterwards."
    )
    parser.add_argument("--criteria", nargs="*", help="Curator criteria.")
    parser.add_argument("--curate-output", help="Where to write the curator JSON.")
    parser.add_argument("--env-file", help="Explicit .env file to load.")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if not args.output and not args.dry_run:
        parser.error("-o/--output is required")
    return run(args)


def safe_main(argv: Optional[List[str]] = None) -> int:
    try:
        return main(argv)
    except MissingEnvError as exc:
        sys.stderr.write("CONFIG ERROR\n%s\n" % exc)
        return 2
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", "replace")[:400]
        except Exception:
            pass
        sys.stderr.write("PROVIDER ERROR %s %s\n%s\n" % (exc.code, exc.reason, body))
        return 3
    except urllib.error.URLError as exc:
        sys.stderr.write("NETWORK ERROR\n%s\n" % exc.reason)
        return 3
    except (ValueError, RuntimeError) as exc:
        sys.stderr.write("ERROR\n%s\n" % exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(safe_main())
