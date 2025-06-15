"""Extract frames from sprite sheets.

This helper script slices sprite sheets into individual frames of 256×256 pixels
arranged in 6 columns by 4 rows. The extracted frames are saved to a destination
folder.

Usage examples::

    python extract_frames.py Imagesidescroller/Chatanimation.png output/chat --prefix chat
    python extract_frames.py Imagesidescroller/Chienanimation.png output/dog --prefix chien

Dependencies: Pillow
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Tuple

from PIL import Image


def extract_frames(
    image_path: Path,
    output_dir: Path,
    frame_size: Tuple[int, int] = (256, 256),
    cols: int = 6,
    rows: int = 4,
    prefix: str = "frame",
) -> None:
    """Split *image_path* into frames and store them in *output_dir*.

    Parameters
    ----------
    image_path:
        Path to the sprite sheet image.
    output_dir:
        Directory where extracted frames will be written.
    frame_size:
        Width and height of each frame in pixels.
    cols, rows:
        Number of columns and rows in the sprite sheet.
    prefix:
        Prefix for generated frame filenames.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(image_path) as image:
        frame_width, frame_height = frame_size
        frame_num = 0
        for row in range(rows):
            for col in range(cols):
                left = col * frame_width
                upper = row * frame_height
                right = left + frame_width
                lower = upper + frame_height
                frame = image.crop((left, upper, right, lower))
                frame.save(output_dir / f"{prefix}_{frame_num:02d}.png")
                frame_num += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Slice sprite sheets")
    parser.add_argument("image", type=Path, help="path to sprite sheet")
    parser.add_argument("output", type=Path, help="directory to save frames")
    parser.add_argument(
        "--prefix", default="frame", help="prefix for output image names"
    )
    args = parser.parse_args()

    extract_frames(args.image, args.output, prefix=args.prefix)


if __name__ == "__main__":  # pragma: no cover - simple CLI
    main()
