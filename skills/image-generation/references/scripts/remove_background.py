from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageFilter


def detect_key_color(
    image: Image.Image, sample_border: int = 8
) -> tuple[int, int, int]:
    img = image.convert("RGB")
    width, height = img.size
    samples: list[tuple[int, int, int]] = []

    top = min(sample_border, height)
    for y in range(top):
        for x in range(width):
            samples.append(img.getpixel((x, y)))

    bottom_start = max(0, height - sample_border)
    for y in range(bottom_start, height):
        for x in range(width):
            samples.append(img.getpixel((x, y)))

    left = min(sample_border, width)
    for x in range(left):
        for y in range(height):
            samples.append(img.getpixel((x, y)))

    right_start = max(0, width - sample_border)
    for x in range(right_start, width):
        for y in range(height):
            samples.append(img.getpixel((x, y)))

    if not samples:
        return (255, 255, 255)

    reds = sorted(pixel[0] for pixel in samples)
    greens = sorted(pixel[1] for pixel in samples)
    blues = sorted(pixel[2] for pixel in samples)
    count = len(reds)
    middle = count // 2
    return (reds[middle], greens[middle], blues[middle])


def _dominance_hit(r: int, g: int, b: int, key_color: tuple[int, int, int]) -> bool:
    """Hue-based test for saturated key colors.

    Euclidean distance alone leaves key-tinted pixels behind when the subject
    blends into the background (hair over a chroma plate). A saturated key has
    a distinct channel signature, so test that signature directly.
    """
    kr, kg, kb = key_color
    saturation = max(kr, kg, kb) - min(kr, kg, kb)
    if saturation < 100:
        return False
    if kr > 150 and kb > 150 and kg < 100:
        return r > 90 and b > 90 and g < int(min(r, b) * 0.75)
    if kg > 150 and kr < 100 and kb < 100:
        return g > 120 and g > int(r * 1.4) and g > int(b * 1.4)
    if kg > 150 and kb > 150 and kr < 100:
        return g > 120 and b > 120 and r < int(min(g, b) * 0.7)
    return False


def apply_chroma_mask(
    image: Image.Image,
    key_color: tuple[int, int, int],
    tolerance: int = 32,
    feather: int = 2,
    erode: int = 1,
    despill: bool = True,
) -> Image.Image:
    img = image.convert("RGBA")
    kr, kg, kb = key_color
    pixels = img.load()
    width, height = img.size
    feather_value = float(feather) if feather else 1.0
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            dist = math.sqrt((r - kr) ** 2 + (g - kg) ** 2 + (b - kb) ** 2)
            if dist <= tolerance or _dominance_hit(r, g, b, key_color):
                new_a = 0
            elif dist < tolerance + feather:
                factor = (dist - tolerance) / feather_value
                new_a = int(a * factor)
            else:
                new_a = a
            if despill and 0 < new_a < 255:
                covered = new_a / 255.0
                r = int(min(255, max(0, (r - kr * (1.0 - covered)) / covered)))
                g = int(min(255, max(0, (g - kg * (1.0 - covered)) / covered)))
                b = int(min(255, max(0, (b - kb * (1.0 - covered)) / covered)))
            pixels[x, y] = (r, g, b, new_a)

    if erode and erode > 0:
        alpha = img.getchannel("A")
        alpha = alpha.filter(ImageFilter.MinFilter(erode * 2 + 1))
        img.putalpha(alpha)
    return img


def remove_background(
    input_path,
    output_path,
    mode: str = "auto",
    key_color: tuple[int, int, int] = (255, 255, 255),
    tolerance: int = 32,
    feather: int = 2,
    erode: int = 1,
):
    img = Image.open(input_path)
    img.load()

    if mode == "white":
        key_color = (255, 255, 255)
    elif mode == "green":
        key_color = (0, 255, 0)
    elif mode == "auto":
        key_color = detect_key_color(img)
    elif mode == "chroma":
        pass

    result = apply_chroma_mask(img, key_color, tolerance, feather, erode)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output)
    return result


def _self_test() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "_selftest_input.png"
    output_path = base_dir / "_selftest_output.png"

    img = Image.new("RGB", (64, 64), (255, 255, 255))
    pixels = img.load()
    cx, cy, radius = 32, 32, 12
    for y in range(64):
        for x in range(64):
            if (x - cx) ** 2 + (y - cy) ** 2 <= radius * radius:
                pixels[x, y] = (255, 0, 0)

    img.save(input_path)
    try:
        remove_background(input_path, output_path, mode="auto", tolerance=32, feather=2)
        result = Image.open(output_path)
        result.load()
        for point in ((0, 0), (63, 0), (0, 63), (63, 63)):
            assert result.getpixel(point)[3] == 0, "corner alpha not 0: %s" % str(point)
        assert result.getpixel((32, 32))[3] > 0, "center alpha not > 0"
    finally:
        for path in (input_path, output_path):
            try:
                path.unlink()
            except FileNotFoundError:
                pass


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Remove a flat background color.")
    parser.add_argument("input", nargs="?")
    parser.add_argument("--output")
    parser.add_argument(
        "--mode", choices=["auto", "white", "green", "chroma"], default="auto"
    )
    parser.add_argument("--key")
    parser.add_argument("--tolerance", type=int, default=32)
    parser.add_argument("--feather", type=int, default=2)
    parser.add_argument(
        "--erode",
        type=int,
        default=1,
        help="Shrink the subject mask by N pixels to remove color fringe. Default 1.",
    )
    parser.add_argument("--self-test", action="store_true", dest="self_test")
    return parser


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)

    if args.self_test:
        _self_test()
        print("self-test OK")
        return 0

    if not args.input or not args.output:
        raise SystemExit("INPUT and --output are required")

    key_color = (255, 255, 255)
    if args.key:
        parts = [part.strip() for part in args.key.split(",")]
        key_color = (int(parts[0]), int(parts[1]), int(parts[2]))

    remove_background(
        args.input,
        args.output,
        mode=args.mode,
        key_color=key_color,
        tolerance=args.tolerance,
        feather=args.feather,
        erode=args.erode,
    )
    print("saved %s" % args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
