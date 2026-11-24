#!/usr/bin/env python3
"""Copy the pre-rendered front page into the output directory.

The server runs only this file (Python 3, standard library only).
It copies entry.png, which sits next to this file in the repository,
to <output>/entry.png, where <output> is $MAKEFUN_OUTPUT_DIR
(default /output). No rendering, no network, no clock, no randomness:
the same bytes are written on every run.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
