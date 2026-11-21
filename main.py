#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261121 bounty.

The front page itself is drawn at build time by draw.py (Python + Pillow)
and committed to this repository as entry.png. This program ships that
image: it copies entry.png to the output path, standard library only, so
the bytes the judge sees are always exactly the verified front page and
every run produces byte-identical output.

Output path, mirroring the kit starter's contract:
  $MAKEFUN_OUTPUT_DIR/entry.png   when the variable is set
  /output/entry.png               when /output exists
  entry.png beside this script    otherwise
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.png")
    if os.path.isdir("/output"):
        return os.path.join("/output", "entry.png")
    return os.path.join(HERE, "entry.png")


def main():
    dest = output_path()
    if os.path.abspath(dest) != os.path.abspath(SOURCE):
        parent = os.path.dirname(dest)
        if parent:
            os.makedirs(parent, exist_ok=True)
        shutil.copyfile(SOURCE, dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
