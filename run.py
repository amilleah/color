#!/usr/bin/env python3
"""
extract palettes from every photo in a folder.

writes `<name>.palette.png` next to each image and a `palettes.json` index.

usage:
    python run.py PATH/TO/PHOTOS
"""
import argparse
import json
from pathlib import Path

from images import extract_palette, render_swatch

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path, help="folder containing photos")
    ap.add_argument("--colors", type=int, default=5, help="palette size (default: 5)")
    args = ap.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"not a directory: {args.folder}")

    photos = sorted(p for p in args.folder.iterdir()
                    if p.suffix.lower() in IMAGE_EXTS
                    and not p.stem.endswith(".palette"))
    if not photos:
        raise SystemExit("no images found")

    index = {}
    for i, path in enumerate(photos, 1):
        centers_lab, rgbs, weights = extract_palette(path, args.colors)
        sidecar = path.with_name(f"{path.stem}.palette.png")
        render_swatch(rgbs, weights, sidecar)
        index[path.name] = {
            "colors_lab": centers_lab,
            "weights": [round(w, 4) for w in weights],
        }
        print(f"  {i}/{len(photos)}  {path.name}")

    (args.folder / "palettes.json").write_text(json.dumps(index, indent=2))
    print(f"Done → {args.folder / 'palettes.json'}")


if __name__ == "__main__":
    main()