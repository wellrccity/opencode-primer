from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, List, Optional

from common import (
    MissingEnvError,
    get_env,
    http_post_json,
    http_post_multipart,
    load_environment,
    resolve_model,
)

# Redefine dataclasses locally to avoid accidental import oddities.


@dataclass
class GenerationRequest:
    prompt: str
    negative_prompt: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    steps: Optional[int] = None
    seed: Optional[int] = None
    output: Optional[Path] = None
    background_mode: str = "none"
    model: Optional[str] = None


@dataclass
class GenerationResult:
    path: Path
    model: str
    provider: str
    bytes: int
    mime: str


BACKGROUND_MODIFIERS = {
    "white": "isolated on a pure solid white background (#FFFFFF), studio lighting, high contrast, clean sharp silhouette, no shadows, no gradients, no background clutter",
    "green": "isolated on a pure solid green background (#00FF00), studio lighting, high contrast, clean sharp silhouette, no shadows, no gradients, chroma key ready",
}


def _detect_mime(data: bytes) -> str:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8"):
        return "image/jpeg"
    if data.startswith(b"GIF8"):
        return "image/gif"
    if data.startswith(b"RIFF") and len(data) >= 12 and data[8:12] == b"WEBP":
        return "image/webp"
    return "image/png"


def _unwrap_image(raw: bytes) -> bytes:
    """Return raw image bytes from either a binary or a JSON base64 response."""
    stripped = raw.lstrip()
    if not stripped.startswith(b"{"):
        return raw
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return raw
    result = payload.get("result") if isinstance(payload, dict) else None
    encoded = None
    if isinstance(result, dict):
        encoded = result.get("image") or result.get("b64_json")
    if encoded is None and isinstance(payload, dict):
        encoded = payload.get("image") or payload.get("b64_json")
    if isinstance(encoded, str) and encoded:
        try:
            return base64.b64decode(encoded)
        except (ValueError, TypeError):
            return raw
    return raw


def _write_output(output: Path, data: bytes) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)


def cloudflare_generate(
    prompt: str,
    model: str,
    width: int,
    height: int,
    steps: Optional[int],
    seed: Optional[int],
    output: Path,
    negative_prompt: Optional[str] = None,
) -> GenerationResult:
    load_environment()
    account_id = get_env("CLOUDFLARE_ACCOUNT_ID", required=True)
    token = get_env("CLOUDFLARE_API_TOKEN", required=True)
    url = "https://api.cloudflare.com/client/v4/accounts/%s/ai/run/%s" % (
        account_id,
        model,
    )
    headers = {"Authorization": "Bearer %s" % token}

    is_flux2 = "flux-2" in model
    is_schnell = "flux-1-schnell" in model

    fields: dict[str, str] = {
        "prompt": prompt,
        "width": str(width),
        "height": str(height),
    }
    if negative_prompt and not is_schnell:
        fields["negative_prompt"] = negative_prompt
    if steps is not None and not is_schnell:
        fields["num_steps"] = str(steps)
    if seed is not None:
        fields["seed"] = str(seed)

    if is_flux2:
        raw = http_post_multipart(url, headers, fields)
    else:
        payload: dict[str, Any] = {"prompt": prompt, "width": width, "height": height}
        if negative_prompt and not is_schnell:
            payload["negative_prompt"] = negative_prompt
        if steps is not None and not is_schnell:
            payload["num_steps"] = steps
        if seed is not None:
            payload["seed"] = seed
        raw = http_post_json(url, headers, payload)

    data = _unwrap_image(raw)
    _write_output(Path(output), data)
    return GenerationResult(
        path=Path(output),
        model=model,
        provider="cloudflare",
        bytes=len(data),
        mime=_detect_mime(data),
    )


def local_generate(
    prompt: str,
    model: str,
    width: int,
    height: int,
    output: Path,
) -> GenerationResult:
    """OpenAI-compatible local image server that returns file, url, or b64."""
    load_environment()
    base_url = str(get_env("LOCAL_IMAGE_BASE_URL", "http://127.0.0.1:8790/v1")).rstrip(
        "/"
    )
    url = base_url + "/images/generations"
    payload = {
        "prompt": prompt,
        "model": model,
        "size": "%dx%d" % (width, height),
    }
    raw = http_post_json(url, None, payload, timeout=600)
    response = json.loads(raw.decode("utf-8"))
    items = response.get("data") or []
    if not items:
        raise RuntimeError("Local image server returned no data")
    item = items[0]

    image_data = None
    file_path = item.get("file")
    if file_path:
        candidate = Path(str(file_path))
        if candidate.is_file():
            image_data = candidate.read_bytes()
    if image_data is None and item.get("b64_json"):
        image_data = base64.b64decode(item["b64_json"])
    if image_data is None and item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as stream:
            image_data = stream.read()
    if image_data is None:
        raise RuntimeError("Local image server response had no file, url, or b64_json")

    _write_output(Path(output), image_data)
    return GenerationResult(
        path=Path(output),
        model=str(item.get("model", model)),
        provider="local",
        bytes=len(image_data),
        mime=_detect_mime(image_data),
    )


def openai_generate(
    prompt: str, model: str, width: int, height: int, output: Path
) -> GenerationResult:
    load_environment()
    base_url = str(get_env("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
    token = get_env("OPENAI_API_TOKEN", required=True)
    url = base_url + "/images/generations"
    headers = {"Authorization": "Bearer %s" % token}
    payload = {
        "model": model,
        "prompt": prompt,
        "size": "%dx%d" % (width, height),
        "response_format": "b64_json",
    }
    raw = http_post_json(url, headers, payload)
    response = json.loads(raw.decode("utf-8"))
    item = (response.get("data") or [{}])[0]
    if "b64_json" in item and item["b64_json"]:
        image_data = base64.b64decode(item["b64_json"])
    elif "url" in item and item["url"]:
        with urllib.request.urlopen(item["url"], timeout=120) as response_stream:
            image_data = response_stream.read()
    else:
        raise RuntimeError("OpenAI response did not contain image data")
    _write_output(Path(output), image_data)
    return GenerationResult(
        path=Path(output),
        model=model,
        provider="openai",
        bytes=len(image_data),
        mime=_detect_mime(image_data),
    )


def custom_generate(
    prompt: str,
    endpoint: str,
    token: Optional[str],
    width: int,
    height: int,
    output: Path,
) -> GenerationResult:
    load_environment()
    if not endpoint:
        endpoint = str(get_env("CUSTOM_IMAGE_ENDPOINT", required=True))
    if token is None:
        token = get_env("CUSTOM_IMAGE_API_TOKEN")
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = "Bearer %s" % token
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "size": "%dx%d" % (width, height),
    }
    raw = http_post_json(endpoint, headers, payload)
    image_data = _decode_custom_response(raw)
    _write_output(Path(output), image_data)
    return GenerationResult(
        path=Path(output),
        model="custom",
        provider="custom",
        bytes=len(image_data),
        mime=_detect_mime(image_data),
    )


def _decode_custom_response(raw: bytes) -> bytes:
    if raw.startswith((b"\x89PNG\r\n\x1a\n", b"\xff\xd8", b"GIF8", b"RIFF")):
        return raw
    try:
        response = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return raw
    if isinstance(response, dict):
        for key in ("b64_json", "base64", "image", "image_base64"):
            value = response.get(key)
            if isinstance(value, str) and value:
                try:
                    return base64.b64decode(value, validate=False)
                except Exception:
                    pass
        data = response.get("data")
        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                for key in ("b64_json", "base64", "image", "image_base64"):
                    value = first.get(key)
                    if isinstance(value, str) and value:
                        try:
                            return base64.b64decode(value, validate=False)
                        except Exception:
                            pass
                if "url" in first and first["url"]:
                    with urllib.request.urlopen(first["url"], timeout=120) as stream:
                        return stream.read()
        if "url" in response and response["url"]:
            with urllib.request.urlopen(response["url"], timeout=120) as stream:
                return stream.read()
    return raw


def generate(request: GenerationRequest) -> GenerationResult:
    load_environment()
    spec = resolve_model(request.model)
    prompt = request.prompt
    if request.background_mode in BACKGROUND_MODIFIERS:
        prompt = prompt + ", " + BACKGROUND_MODIFIERS[request.background_mode]
    negative = request.negative_prompt
    if negative and not spec.supports_negative_prompt:
        negative = None

    width = request.width if request.width else spec.default_size[0]
    height = request.height if request.height else spec.default_size[1]

    if spec.provider == "cloudflare":
        return cloudflare_generate(
            prompt,
            spec.remote_model,
            width,
            height,
            request.steps,
            request.seed,
            request.output,
            negative,
        )
    if spec.provider == "local":
        return local_generate(prompt, spec.remote_model, width, height, request.output)
    if spec.provider == "openai":
        return openai_generate(prompt, spec.remote_model, width, height, request.output)
    if spec.provider == "custom":
        endpoint = get_env("CUSTOM_IMAGE_ENDPOINT", required=True)
        token = get_env("CUSTOM_IMAGE_API_TOKEN")
        return custom_generate(prompt, endpoint, token, width, height, request.output)
    raise ValueError("Unsupported image provider: %s" % spec.provider)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate an image with a configured provider."
    )
    parser.add_argument("--prompt")
    parser.add_argument("--negative")
    parser.add_argument("--model")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--steps", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument(
        "--background", choices=["none", "white", "green"], default="none"
    )
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    load_environment()
    if args.dry_run:
        spec = resolve_model(args.model)
        print(
            json.dumps(
                {
                    "model": spec.id,
                    "provider": spec.provider,
                    "remote_model": spec.remote_model,
                    "default_size": list(spec.default_size),
                },
                indent=2,
            )
        )
        return 0

    if not args.prompt:
        raise SystemExit("--prompt is required")
    if not args.output:
        raise SystemExit("--output is required")

    request = GenerationRequest(
        prompt=args.prompt,
        negative_prompt=args.negative,
        width=args.width,
        height=args.height,
        steps=args.steps,
        seed=args.seed,
        output=Path(args.output),
        background_mode=args.background,
        model=args.model,
    )
    result = generate(request)
    print(
        json.dumps(
            {
                "path": str(result.path),
                "model": result.model,
                "provider": result.provider,
                "bytes": result.bytes,
                "mime": result.mime,
            },
            indent=2,
        )
    )
    return 0


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
    except ValueError as exc:
        sys.stderr.write("ERROR\n%s\n" % exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(safe_main())
