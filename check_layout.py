"""Layout self-check for news-image-20261118 v4 (local dev tool).

Verifies, from the real font metrics, that no headline, deck, brief,
date-check line or footer is silently truncated by a line budget:
every wrapped text must fit its allotted lines, and every brief must
fit its column width. Exits non-zero on any violation.

Usage: python3 check_layout.py
"""

import sys

from draw import fit_text, text_width, wrap_text
from page import CONTENT, VARIANTS
from stories import (BRIEFS, EXCLUDED, FOOTER, PANELS, check_counts)

PANEL_BY_ID = {p["id"]: p for p in PANELS}
FAILURES = []


def check(cond, msg):
    if not cond:
        FAILURES.append(msg)
        print("FAIL:", msg)


def main():
    check_counts()
    # panel text budgets per row size: (headline font, width, lines,
    # deck font, width, lines)
    budgets = {
        "lead": ("serif-bold-22", 304, 2, "sans-11", 304, 2),
        "mid": ("serif-bold-17", 222, 2, "sans-10", 222, 2),
        "small": ("sans-bold-13", 140, 2, "sans-10", 140, 2),
    }
    for variant, spec in VARIANTS.items():
        for size, ids in (("lead", spec["lead"]), ("mid", spec["rowb"]),
                          ("small", spec["rowc"])):
            hf, hw, hl, df, dw, dl = budgets[size]
            for pid in ids:
                p = PANEL_BY_ID[pid]
                hlines = wrap_text(hf, p["headline"], hw)
                check(len(hlines) <= hl,
                      "%s %s headline needs %d lines: %r"
                      % (variant, pid, len(hlines), p["headline"]))
                deck = p["deck"] if size != "small" else p["deck_short"]
                dlines = wrap_text(df, deck, dw)
                check(len(dlines) <= dl,
                      "%s %s deck needs %d lines: %r"
                      % (variant, pid, len(dlines), deck))
    # briefs: one line each, must fit the column
    col_w = (CONTENT - 24) // 3
    for region, lead, text in BRIEFS:
        w = (text_width("sans-bold-11", lead + ": ")
             + text_width("sans-10", text))
        check(w <= col_w, "brief overflows: %s: %s (%d > %d)"
              % (lead, text, w, col_w))
    # date-check band: at most 2 lines
    check(len(wrap_text("sans-10", EXCLUDED, CONTENT - 16)) <= 2,
          "date-check band needs more than 2 lines")
    # footer: one line
    check(text_width("sans-10", FOOTER) <= CONTENT,
          "footer too wide: %d" % text_width("sans-10", FOOTER))
    if FAILURES:
        print("%d layout failure(s)" % len(FAILURES))
        sys.exit(1)
    print("layout check OK: 13 panels x 4 variants, 29 briefs, band, footer")


if __name__ == "__main__":
    main()
