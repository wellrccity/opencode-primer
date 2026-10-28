from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ModelSpec:
    id: str
    provider: str
    remote_model: str
    display_name: str = "Unknown"
    default_size: tuple[int, int] = (1024, 1024)
    supports_negative_prompt: bool = True
    cost_tier: str = "unknown"
    transport: str = "json"
    response: str = "binary"
    quality_rank: int = 0


REGISTRY: Dict[str, Dict[str, Any]] = {
    "cf:black-forest-labs/flux-2-dev": {
        "provider": "cloudflare",
        "remote_model": "@cf/black-forest-labs/flux-2-dev",
        "display_name": "FLUX.2 Dev",
        "default_size": (1024, 1024),
        "supports_negative_prompt": True,
        "cost_tier": "free",
        "transport": "multipart",
        "response": "json-base64",
        "quality_rank": 5,
    },
    "cf:black-forest-labs/flux-2-klein-9b": {
        "provider": "cloudflare",
        "remote_model": "@cf/black-forest-labs/flux-2-klein-9b",
        "display_name": "FLUX.2 Klein 9B",
        "default_size": (1024, 1024),
        "supports_negative_prompt": True,
        "cost_tier": "free",
        "transport": "multipart",
        "response": "json-base64",
        "quality_rank": 4,
    },
    "cf:black-forest-labs/flux-2-klein-4b": {
        "provider": "cloudflare",
        "remote_model": "@cf/black-forest-labs/flux-2-klein-4b",
        "display_name": "FLUX.2 Klein 4B",
        "default_size": (1024, 1024),
        "supports_negative_prompt": True,
        "cost_tier": "free",
        "transport": "multipart",
        "response": "json-base64",
        "quality_rank": 3,
    },
    "cf:leonardo/phoenix-1.0": {
        "provider": "cloudflare",
        "remote_model": "@cf/leonardo/phoenix-1.0",
        "display_name": "Leonardo Phoenix 1.0",
        "default_size": (1024, 1024),
        "supports_negative_prompt": True,
        "cost_tier": "free",
        "quality_rank": 4,
    },
    "local:gpt-image-2.5-sunburst": {
        "provider": "local",
        "remote_model": "gpt-image-2.5-sunburst",
        "display_name": "Local gpt-image-2.5-sunburst",
        "default_size": (1024, 1024),
        "supports_negative_prompt": False,
        "cost_tier": "local",
        "quality_rank": 5,
    },
    "cf:stabilityai/stable-diffusion-xl-base-1.0": {
        "provider": "cloudflare",
        "remote_model": "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        "display_name": "Stable Diffusion XL Base 1.0",
        "default_size": (1024, 1024),
        "supports_negative_prompt": True,
        "cost_tier": "free",
        "quality_rank": 3,
    },
    "cf:black-forest-labs/flux-1-schnell": {
        "provider": "cloudflare",
        "remote_model": "@cf/black-forest-labs/flux-1-schnell",
        "display_name": "Black Forest Labs FLUX.1 Schnell",
        "default_size": (1024, 1024),
        "supports_negative_prompt": False,
        "cost_tier": "free",
        "quality_rank": 3,
    },
    "cf:bytedance/stable-diffusion-xl-lightning": {
        "provider": "cloudflare",
        "remote_model": "@cf/bytedance/stable-diffusion-xl-lightning",
        "display_name": "ByteDance SDXL Lightning",
        "default_size": (1024, 1024),
        "supports_negative_prompt": True,
        "cost_tier": "free",
        "quality_rank": 1,
    },
    "cf:lykon/dreamshaper-8-lcm": {
        "provider": "cloudflare",
        "remote_model": "@cf/lykon/dreamshaper-8-lcm",
        "display_name": "DreamShaper 8 LCM",
        "default_size": (1024, 1024),
        "supports_negative_prompt": False,
        "cost_tier": "free",
        "quality_rank": 2,
    },
    "openai:dall-e-3": {
        "provider": "openai",
        "remote_model": "dall-e-3",
        "display_name": "OpenAI DALL-E 3",
        "default_size": (1024, 1024),
        "supports_negative_prompt": False,
        "cost_tier": "paid",
    },
    "openai:gpt-image-1": {
        "provider": "openai",
        "remote_model": "gpt-image-1",
        "display_name": "OpenAI GPT Image 1",
        "default_size": (1024, 1024),
        "supports_negative_prompt": True,
        "cost_tier": "paid",
    },
    "custom": {
        "provider": "custom",
        "remote_model": "custom",
        "display_name": "Custom endpoint",
        "default_size": (1024, 1024),
        "supports_negative_prompt": True,
        "cost_tier": "unknown",
    },
}


def _clean_env_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        value = value[1:-1]
    return value


SKILL_ROOT = Path(__file__).resolve().parent.parent.parent

DEFAULT_MODEL = "cf:leonardo/phoenix-1.0"
DEFAULT_CUTOUT_COLOR = "magenta"


class MissingEnvError(RuntimeError):
    """Raised when a required environment variable is absent."""


def env_search_paths() -> List[Path]:
    paths: List[Path] = [Path.cwd() / ".env"]
    if os.environ.get("IMAGE_GEN_ENV_FILE"):
        paths.insert(0, Path(os.environ["IMAGE_GEN_ENV_FILE"]))
    paths.extend(
        [
            SKILL_ROOT / ".env",
            SKILL_ROOT.parent / ".env",
            SKILL_ROOT.parent.parent / ".env",
            Path.home() / ".config" / "opencode" / ".env",
        ]
    )
    seen = set()
    unique = []
    for path in paths:
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


def load_environment(env_file: Optional[str] = None) -> None:
    candidates = [Path(env_file)] if env_file else env_search_paths()
    for candidate in candidates:
        if not candidate.is_file():
            continue
        try:
            lines = candidate.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            os.environ[key] = _clean_env_value(value)


def get_env(
    name: str, default: Optional[str] = None, required: bool = False
) -> Optional[str]:
    value = os.environ.get(name)
    if value is None or value == "":
        if required:
            searched = ", ".join(str(path) for path in env_search_paths())
            hint = (
                " Get Cloudflare values from the Workers AI dashboard."
                if name.startswith("CLOUDFLARE_")
                else ""
            )
            raise MissingEnvError(
                "Missing required environment variable: %s\n"
                "Set it in the shell or add it to one of these files: %s\n"
                "Do not search the filesystem for it.%s" % (name, searched, hint)
            )
        return default
    return value


def resolve_model(model_id: Optional[str] = None) -> ModelSpec:
    load_environment()
    if model_id is None:
        selected = get_env("IMAGE_GEN_MODEL", DEFAULT_MODEL)
    else:
        selected = model_id
    selected = str(selected).strip()
    provider_override = os.environ.get("IMAGE_GEN_PROVIDER")

    if selected.startswith("local:"):
        spec = ModelSpec(
            id=selected,
            provider="local",
            remote_model=selected.split(":", 1)[1],
            display_name=selected,
            default_size=(1024, 1024),
            supports_negative_prompt=False,
            cost_tier="local",
            quality_rank=5,
        )
    elif selected.startswith("@cf/"):
        spec = ModelSpec(
            id=selected,
            provider="cloudflare",
            remote_model=selected,
            display_name=selected,
            default_size=(1024, 1024),
            supports_negative_prompt=True,
            cost_tier="free",
        )
    elif selected in REGISTRY:
        entry = REGISTRY[selected]
        spec = ModelSpec(
            id=selected,
            provider=entry["provider"],
            remote_model=entry["remote_model"],
            display_name=entry["display_name"],
            default_size=tuple(entry["default_size"]),
            supports_negative_prompt=entry["supports_negative_prompt"],
            cost_tier=entry["cost_tier"],
        )
    else:
        spec = ModelSpec(
            id=selected,
            provider="custom",
            remote_model=selected,
            display_name=selected,
            default_size=(1024, 1024),
            supports_negative_prompt=True,
            cost_tier="unknown",
        )

    if provider_override:
        spec.provider = provider_override.strip()
    return spec


def http_post_multipart(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    fields: Optional[Dict[str, str]] = None,
    timeout: int = 600,
) -> bytes:
    """POST a form-data body. Required by the FLUX.2 Workers AI models."""
    import uuid

    boundary = "----cf" + uuid.uuid4().hex
    chunks = []
    for key, value in (fields or {}).items():
        chunks.append(
            (
                '--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n'
                % (boundary, key, value)
            ).encode("utf-8")
        )
    chunks.append(("--%s--\r\n" % boundary).encode("utf-8"))
    body = b"".join(chunks)

    headers = dict(headers or {})
    headers["Content-Type"] = "multipart/form-data; boundary=%s" % boundary
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def http_post_json(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    payload: Any = None,
    timeout: int = 120,
) -> bytes:
    headers = dict(headers or {})
    if payload is not None and not any(
        key.lower() == "content-type" for key in headers
    ):
        headers["Content-Type"] = "application/json"

    if payload is None:
        data = b""
    elif isinstance(payload, (dict, list, tuple)):
        data = json.dumps(payload).encode("utf-8")
    elif isinstance(payload, str):
        data = payload.encode("utf-8")
    elif isinstance(payload, (bytes, bytearray)):
        data = bytes(payload)
    else:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()
