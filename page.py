"""Page layout for news-image-20261118 v4.

One 1024x1024 cream broadsheet: masthead, region count bar, three rows
of illustrated panels (3 lead + 4 + 6), a dotted world map with 13
numbered pins, a day-in-numbers strip, 29 one-line briefs, a date-check
band naming the five excluded 17-November items, and a sources footer.

Variants (candidates for the gate's pairwise judging):
  A — lead Gulf, APEC, Kerch (cream broadsheet)
  B — lead APEC, Gulf, Kerch (APEC first)
  C — lead Kerch, Gulf, APEC; war-first tabloid order
  D — same order as A, dark theme
"""

from art import ARTS
from draw import Canvas, fit_text, text_width, wrap_text
from stories import (BRIEFS, DATE_LINE, EXCLUDED, FOOTER, MASTHEAD,
                     NUMBERS, PANELS, REGION_COUNTS, REGION_ORDER,
                     TAGLINE, check_counts, on_land)

W, H = 1024, 1024
MARGIN = 24
CONTENT = W - 2 * MARGIN  # 976

THEMES = {
    "cream": dict(paper=(247, 241, 222), ink=(28, 28, 28),
                  deck=(70, 66, 58), rule=(28, 28, 28),
                  panel=(252, 248, 235), border=(150, 140, 120),
                  accent=(178, 34, 34), faint=(120, 112, 96),
                  mapdot=(90, 100, 110), band=(238, 230, 205)),
    "dark": dict(paper=(26, 30, 44), ink=(236, 234, 224),
                 deck=(205, 202, 190), rule=(236, 234, 224),
                 panel=(34, 40, 58), border=(110, 115, 135),
                 accent=(232, 120, 90), faint=(160, 158, 145),
                 mapdot=(150, 160, 175), band=(40, 46, 66)),
}

VARIANTS = {
    "A": dict(theme="cream",
              lead=["gulf", "apec", "kerch"],
              rowb=["cop31", "voyager", "anthropic", "gaza"],
              rowc=["quad", "markets", "measles", "ebola", "jeffries",
                    "royals"]),
    "B": dict(theme="cream",
              lead=["apec", "gulf", "kerch"],
              rowb=["cop31", "voyager", "anthropic", "gaza"],
              rowc=["quad", "markets", "measles", "ebola", "jeffries",
                    "royals"]),
    "C": dict(theme="cream",
              lead=["kerch", "gulf", "apec"],
              rowb=["gaza", "cop31", "voyager", "anthropic"],
              rowc=["quad", "markets", "measles", "ebola", "jeffries",
                    "royals"]),
    "D": dict(theme="dark",
              lead=["gulf", "apec", "kerch"],
              rowb=["cop31", "voyager", "anthropic", "gaza"],
              rowc=["quad", "markets", "measles", "ebola", "jeffries",
                    "royals"]),
}

PANEL_BY_ID = {p["id"]: p for p in PANELS}


def _truncate(font, text, max_width):
    """Shorten text with an ellipsis until it fits max_width."""
    if text_width(font, text) <= max_width:
        return text
    while text and text_width(font, text + "...") > max_width:
        text = text[:-1].rstrip()
    return text + "..."


def _panel(cv, t, p, x, y, w, h, size):
    """Draw one panel. size: 'lead' | 'mid' | 'small'."""
    cv.rect(x, y, w, h, t["panel"])
    cv.rect(x, y, w, 1, t["border"])
    cv.rect(x, y + h - 1, w, 1, t["border"])
    cv.rect(x, y, 1, h, t["border"])
    cv.rect(x + w - 1, y, 1, h, t["border"])
    pad = 8
    ix, iw = x + pad, w - 2 * pad
    if size == "lead":
        kfont, hfont, dfont = "sans-bold-11", "serif-bold-22", "sans-11"
        art_h, head_lines, deck_lines = 72, 2, 2
        kicker_y, art_y = y + 15, y + 18
        head_y = y + 112
        lead, dlead = 25, 13
    elif size == "mid":
        kfont, hfont, dfont = "sans-bold-11", "serif-bold-17", "sans-10"
        art_h, head_lines, deck_lines = 52, 2, 2
        kicker_y, art_y = y + 14, y + 17
        head_y = y + 84
        lead, dlead = 20, 12
    else:
        kfont, hfont, dfont = "sans-bold-11", "sans-bold-13", "sans-10"
        art_h, head_lines, deck_lines = 36, 2, 2
        kicker_y, art_y = y + 13, y + 15
        head_y = y + 64
        lead, dlead = 16, 12
    cv.text(kfont, ix, kicker_y, p["kicker"], t["accent"])
    ARTS[p["art"]](cv, ix, art_y, iw, art_h)
    deck = p["deck"] if size != "small" else p["deck_short"]
    hlines = fit_text(hfont, p["headline"], iw, head_lines)
    cv.text_lines(hfont, ix, head_y, hlines, t["ink"], leading=lead)
    # Deck starts below the headline's actual line count, never on top of it.
    deck_y = head_y + len(hlines) * lead + 5
    dlines = fit_text(dfont, deck, iw, deck_lines)
    cv.text_lines(dfont, ix, deck_y, dlines, t["deck"], leading=dlead)


def _row(cv, t, ids, y, h, size):
    n = len(ids)
    gap = 8
    w = (CONTENT - gap * (n - 1)) // n
    for i, pid in enumerate(ids):
        _panel(cv, t, PANEL_BY_ID[pid], MARGIN + i * (w + gap), y, w, h, size)


def _map_band(cv, t, y, h, panels_in_order):
    """Dotted world map (left) + numbered legend (right)."""
    title_y = y + 13
    cv.text("sans-bold-11", MARGIN, title_y, "WHERE IT HAPPENED",
            t["accent"])
    map_x, map_y = MARGIN, y + 18
    map_w, map_h = 620, h - 22
    # dotted land
    step_lon, step_lat = 4.0, 4.0
    lon = -180.0
    while lon < 180:
        lat = -56.0
        while lat <= 84:
            if on_land(lon, lat):
                px = map_x + int((lon + 180) / 360 * map_w)
                py = map_y + int((84 - lat) / 140 * map_h)
                cv.circle(px, py, 2, t["mapdot"])
            lat += step_lat
        lon += step_lon
    # pins, numbered in display order; de-collide radially with leaders
    placed = []
    offsets = [(0, 0), (18, -14), (-18, -14), (18, 14), (-18, 14),
               (0, -20), (0, 20), (26, 0), (-26, 0), (26, -16), (-26, -16)]
    for num, pid in enumerate(panels_in_order, 1):
        p = PANEL_BY_ID[pid]
        pin = p["pin"]
        if pin is None:
            # Voyager: a star at the top-right corner of the map
            sx, sy = map_x + map_w - 12, map_y + 10
            cv.circle(sx, sy, 7, t["accent"])
            cv.text("sans-bold-11", sx, sy + 4, str(num), (255, 255, 255),
                    align="center")
            placed.append((sx, sy))
            continue
        px = map_x + int((pin[0] + 180) / 360 * map_w)
        py = map_y + int((84 - pin[1]) / 140 * map_h)
        dx, dy = px, py
        for ox, oy in offsets:
            cand = (px + ox, py + oy)
            if all(abs(cand[0] - qx) >= 17 or abs(cand[1] - qy) >= 17
                   for qx, qy in placed):
                dx, dy = cand
                break
        if (dx, dy) != (px, py):
            cv.line(px, py, dx, dy, t["accent"])
        cv.circle(dx, dy, 7, t["accent"])
        cv.text("sans-bold-11", dx, dy + 4, str(num), (255, 255, 255),
                align="center")
        placed.append((dx, dy))
    # legend: two columns
    lx = MARGIN + 636
    col_w = 168
    legend = [
        ("1", "Kuwait · Gulf drones"), ("2", "Shenzhen · APEC"),
        ("3", "Kerch · bridge hit"), ("4", "Antalya · COP31"),
        ("5", "Deep space · Voyager 1"), ("6", "San Francisco · IPO"),
        ("7", "Gaza · Yellow Line"), ("8", "Manila · Quad"),
        ("9", "New York · markets"), ("10", "DR Congo · Ebola"),
        ("11", "Washington · Jeffries"), ("12", "USA · measles"),
        ("13", "Mumbai · royals"),
    ]
    # renumber legend to match this variant's display order
    order = panels_in_order
    names = {"gulf": "Kuwait · Gulf drones", "apec": "Shenzhen · APEC",
             "kerch": "Kerch · bridge hit", "cop31": "Antalya · COP31",
             "voyager": "Deep space · Voyager 1",
             "anthropic": "San Francisco · IPO", "gaza": "Gaza · Yellow Line",
             "quad": "Manila · Quad", "markets": "New York · markets",
             "measles": "USA · measles", "ebola": "DR Congo · Ebola",
             "jeffries": "Washington · Jeffries", "royals": "Mumbai · royals"}
    legend = [(str(i + 1), names[pid]) for i, pid in enumerate(order)]
    for i, (num, label) in enumerate(legend):
        col = i // 7
        row = i % 7
        lx_i = lx + col * col_w
        ly = map_y + 4 + row * 15
        cv.text("sans-bold-11", lx_i, ly, num + ".", t["accent"])
        cv.text("sans-10", lx_i + 16, ly,
                _truncate("sans-10", label, col_w - 18), t["ink"])


def _numbers(cv, t, y, h):
    n = len(NUMBERS)
    w = CONTENT // n
    for i, (num, label) in enumerate(NUMBERS):
        cx = MARGIN + i * w + w // 2
        cv.text("serif-bold-22", cx, y + 22, num, t["accent"], align="center")
        cv.text("sans-10", cx, y + 35, label, t["deck"], align="center")
        if i:
            cv.vline(MARGIN + i * w, y + 4, h - 8, t["border"])


def _briefs(cv, t, y, h):
    header_y = y + 12
    cv.text("sans-bold-11", MARGIN, header_y, "IN BRIEF", t["accent"])
    cv.hline(MARGIN, y + 17, CONTENT, t["border"])
    cols = 3
    gap = 12
    col_w = (CONTENT - gap * (cols - 1)) // cols
    rows = 10
    leading = 16
    first_base = y + 34
    for i, (region, lead, text) in enumerate(BRIEFS):
        col = i // rows
        row = i % rows
        bx = MARGIN + col * (col_w + gap)
        by = first_base + row * leading
        line = lead + ": " + text
        cv.text("sans-bold-11", bx, by, lead + ":", t["accent"])
        lw = text_width("sans-bold-11", lead + ": ")
        cv.text("sans-10", bx + lw, by,
                _truncate("sans-10", text, col_w - lw), t["ink"])


def render(variant="A"):
    """Render one variant and return the Canvas."""
    check_counts()
    spec = VARIANTS[variant]
    t = THEMES[spec["theme"]]
    cv = Canvas(W, H, t["paper"])
    order = spec["lead"] + spec["rowb"] + spec["rowc"]
    assert len(order) == 13 and len(set(order)) == 13

    # masthead
    cv.text("serif-bold-40", W // 2, 52, MASTHEAD, t["ink"], align="center")
    cv.text("sans-bold-13", W // 2, 76, DATE_LINE, t["accent"],
            align="center")
    cv.hline(MARGIN, 84, CONTENT, t["rule"])
    cv.hline(MARGIN, 87, CONTENT, t["rule"])

    # count bar
    parts = ["%s %d" % (r, REGION_COUNTS[r]) for r in REGION_ORDER]
    bar = "  ·  ".join(parts)
    cv.text("sans-bold-11", W // 2, 106, bar, t["ink"], align="center")
    cv.text("sans-10", W // 2, 106, "", t["ink"], align="center")

    # panel rows
    _row(cv, t, spec["lead"], 112, 188, "lead")
    _row(cv, t, spec["rowb"], 306, 146, "mid")
    _row(cv, t, spec["rowc"], 458, 118, "small")

    # map, numbers, briefs
    _map_band(cv, t, 582, 132, order)
    cv.hline(MARGIN, 720, CONTENT, t["border"])
    _numbers(cv, t, 722, 36)
    cv.hline(MARGIN, 760, CONTENT, t["border"])
    _briefs(cv, t, 762, 186)

    # date-check band
    band_y = 952
    cv.rect(MARGIN, band_y, CONTENT, 28, t["band"])
    cv.rect(MARGIN, band_y, CONTENT, 1, t["border"])
    cv.rect(MARGIN, band_y + 27, CONTENT, 1, t["border"])
    lines = wrap_text("sans-10", EXCLUDED, CONTENT - 16)
    yy = band_y + 11
    for ln in lines[:2]:
        cv.text("sans-10", W // 2, yy, ln, t["ink"], align="center")
        yy += 12

    # footer
    cv.text("sans-10", W // 2, 996, FOOTER, t["faint"], align="center")
    cv.text("sans-10", W // 2, 996, "", t["faint"], align="center")
    _ = TAGLINE
    return cv
