#!/usr/bin/env python3
"""Deliver the finished front page for news-image-20261121.

The page is rendered once, while the entry is built, by draw.py, and the
rendered file sits beside this script as entry.png. This script only moves
that file to the place the grader reads, with nothing but the standard
library involved, so the image the judge grades is byte for byte the image
that was checked during the build.
"""

import os
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent / "entry.png"
FALLBACK_DIR = Path("/output")


def destination() -> Path:
    """Pick the output location the harness expects."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return Path(override) / PAGE.name
    if FALLBACK_DIR.is_dir():
        return FALLBACK_DIR / PAGE.name
    return PAGE


def main() -> int:
    target = destination()
    if target.resolve() != PAGE.resolve():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(PAGE.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
