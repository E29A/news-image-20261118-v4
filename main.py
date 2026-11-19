"""Entry point for news-image-20261118 v4 (make.fun).

Pure standard library: draws the 18 November 2026 front page and writes
it to /output/entry.png (the sandbox path) or to a path given on the
command line. Deterministic: two runs write byte-identical files.

Usage:
    python3 main.py                 # variant A -> /output/entry.png
    python3 main.py out.png B       # variant B -> out.png
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from page import render


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    variant = sys.argv[2] if len(sys.argv) > 2 else "A"
    cv = render(variant)
    data = cv.png_bytes()
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print("variant=%s size=%d sha256=%s path=%s"
          % (variant, len(data), hashlib.sha256(data).hexdigest(), out))


if __name__ == "__main__":
    main()
