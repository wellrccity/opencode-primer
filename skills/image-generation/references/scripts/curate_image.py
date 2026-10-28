from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

from common import get_env, http_post_json, load_environment


def encode_image(path) -> str:
    data = pathlib.Path(path).read_bytes()
    return base64.b64encode(data).decode("ascii")


def _detect_mime(path) -> str:
    p = pathlib.Path(path)
    suffix = p.suffix.lower()
    mapping = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    if suffix in mapping:
        return mapping[suffix]
    try:
        data = p.read_bytes()[:16]
    except OSError:
        return "image/png"
    if data.startswith(b"\x89PNG"):
        return "image/png"
    if data.startswith(b"\xff\xd8"):
        return "image/jpeg"
    if data.startswith(b"GIF8"):
        return "image/gif"
    if data.startswith(b"RIFF"):
        return "image/webp"
    return "image/png"


def build_payload(
    image_b64: str,
    mime: str,
    prompt: str,
    criteria: list[str],
    model: str,
) -> dict:
    criteria = criteria or []
    system_message = (
        "You are an expert visual design curator. Evaluate if the generated "
        "image matches the prompt and visual criteria. Output strict JSON with: "
        "{score: 1-10, verdict: 'accept'|'revise'|'reject', issues: [...], "
        "suggestions: [...]}."
    )
    user_text = "Prompt: %s" % prompt
    if criteria:
        user_text += "\nCriteria:\n" + "\n".join("- " + item for item in criteria)
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:%s;base64,%s" % (mime, image_b64)},
                    },
                ],
            },
        ],
        "temperature": 0.2,
    }


def _parse_json_content(content: str) -> dict:
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


def _local_fallback(image_path, prompt, criteria, error) -> dict:
    criteria = criteria or []
    path = pathlib.Path(image_path)
    size_bytes = 0
    try:
        size_bytes = path.stat().st_size
    except OSError:
        size_bytes = 0

    width = 0
    height = 0
    mode = "unknown"
    try:
        from PIL import Image

        with Image.open(path) as im:
            width, height = im.size
            mode = im.mode
    except Exception:
        pass

    issues = []
    suggestions = []
    score = 7

    if width < 512 or height < 512:
        score -= 2
        issues.append("Low resolution (%dx%d)." % (width, height))
        suggestions.append("Generate at a higher resolution.")

    if height > 0:
        aspect = width / float(height)
        if aspect < 0.5 or aspect > 2.0:
            score -= 1
            issues.append("Extreme aspect ratio (%.2f)." % aspect)
            suggestions.append("Use a more balanced aspect ratio.")

    if size_bytes < 10000:
        score -= 1
        issues.append("Very small file size (%d bytes)." % size_bytes)
        suggestions.append("Ensure the image is not truncated or empty.")

    try:
        from PIL import Image

        with Image.open(path) as im:
            rgb = im.convert("RGB")
            corners = [
                rgb.getpixel((0, 0)),
                rgb.getpixel((rgb.width - 1, 0)),
                rgb.getpixel((0, rgb.height - 1)),
                rgb.getpixel((rgb.width - 1, rgb.height - 1)),
            ]
            spread = max(
                max(c[0] for c in corners) - min(c[0] for c in corners),
                max(c[1] for c in corners) - min(c[1] for c in corners),
                max(c[2] for c in corners) - min(c[2] for c in corners),
            )
            if spread > 40:
                score -= 1
                issues.append("Background not uniformly isolated.")
                suggestions.append("Use a solid, uniform background color.")
    except Exception:
        pass

    if not issues:
        issues.append("API unavailable; local heuristic only.")
    if not suggestions:
        suggestions.append("Retry with a vision model when available.")

    score = max(1, min(10, score))
    if score >= 8:
        verdict = "accept"
    elif score >= 5:
        verdict = "revise"
    else:
        verdict = "reject"

    return {
        "score": score,
        "verdict": verdict,
        "issues": issues,
        "suggestions": suggestions,
        "fallback": True,
        "error": error,
        "image": {
            "width": width,
            "height": height,
            "bytes": size_bytes,
            "mode": mode,
        },
        "prompt": prompt,
        "criteria": criteria,
    }


def evaluate(image_path, prompt, criteria=None, output=None, model=None):
    load_environment()
    criteria = criteria or []

    image_b64 = encode_image(image_path)
    mime = _detect_mime(image_path)

    base_url = str(get_env("OPENCODE_BASE_URL", "https://api.opencode.ai/v1")).rstrip(
        "/"
    )
    token = get_env("OPENCODE_API_TOKEN")
    selected_model = model if model else get_env("OPENCODE_MODEL", "gpt-4o")

    report = None
    try:
        if not token:
            raise RuntimeError("Missing OPENCODE_API_TOKEN")
        payload = build_payload(image_b64, mime, prompt, criteria, selected_model)
        url = base_url + "/chat/completions"
        headers = {"Authorization": "Bearer %s" % token}
        raw = http_post_json(url, headers, payload, timeout=120)
        data = json.loads(raw.decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        report = _parse_json_content(content)
        if not isinstance(report, dict):
            raise RuntimeError("Vision response was not a JSON object")
        report.setdefault("score", 5)
        report.setdefault("verdict", "revise")
        report.setdefault("issues", [])
        report.setdefault("suggestions", [])
    except Exception as exc:
        report = _local_fallback(image_path, prompt, criteria, str(exc))

    if output:
        out_path = pathlib.Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8"
        )

    print(json.dumps(report, indent=2, ensure_ascii=True))
    return report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Curate a generated image.")
    parser.add_argument("--image", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--criteria", nargs="*", default=[])
    parser.add_argument("--output")
    parser.add_argument("--model")
    return parser


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    load_environment()
    evaluate(
        args.image,
        args.prompt,
        criteria=args.criteria,
        output=args.output,
        model=args.model,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
