#!/usr/bin/env python3
"""Entry point for the news-image-20261124 make.fun bounty.

Copies the pre-drawn front-page image (entry.png, next to this file)
to the output directory, byte for byte. Standard library only, no
network. Deterministic: both runs write identical bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    src_size = os.path.getsize(SOURCE)
    dst_size = os.path.getsize(dest)
    if dst_size != src_size:
        print(
            "error: copied size %d does not match source size %d"
            % (dst_size, src_size),
            file=sys.stderr,
        )
        return 1
    print("wrote %s (%d bytes)" % (dest, dst_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
