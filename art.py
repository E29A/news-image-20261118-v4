"""Illustrated panels for news-image-20261118 v4.

Every art function takes (cv, x, y, w, h) and sizes every element from
w and h, so the same art fits a tall lead box and a short row box without
overflowing. No text inside the art: headlines and decks are drawn by
page.py. All drawing uses the pure-stdlib Canvas from draw.py.
"""

INK = (30, 30, 30)
WHITE = (255, 255, 255)
SKY = (168, 205, 225)
DUSK = (232, 164, 110)
SEA = (38, 68, 96)
SAND = (226, 205, 160)
RED = (178, 34, 34)
ORANGE = (224, 110, 30)
GOLD = (212, 160, 40)
GREEN = (46, 125, 60)
DARKGREEN = (28, 84, 44)
BLUE = (36, 80, 160)
GREY = (120, 120, 118)
LIGHTGREY = (205, 205, 200)


def _sky(cv, x, y, w, h, top, bottom):
    """Vertical two-tone sky: top colour fading to bottom colour in bands."""
    bands = 6
    for i in range(bands):
        t = i / (bands - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        cv.rect(x, y + i * h // bands, w, h // bands + 1, c)


def _drone(cv, cx, cy, s, color):
    """Tiny quadcopter silhouette, size s."""
    cv.rect(cx - s, cy - s // 3, s * 2, s * 2 // 3, color)
    cv.line(cx - s - s // 2, cy - s // 2, cx - s, cy - s // 4, color)
    cv.line(cx + s, cy - s // 4, cx + s + s // 2, cy - s // 2, color)
    cv.line(cx - s - s // 2, cy + s // 2, cx - s, cy + s // 4, color)
    cv.line(cx + s, cy + s // 4, cx + s + s // 2, cy + s // 2, color)
    cv.circle(cx, cy + s // 2, max(1, s // 4), color)


def _burst(cv, cx, cy, r, color):
    """Explosion star: 8 spikes around a filled disc."""
    cv.circle(cx, cy, r // 2, color)
    import math
    for i in range(8):
        a = math.pi * i / 4
        cv.thick_line(cx, cy,
                      int(cx + r * math.cos(a)), int(cy + r * math.sin(a)),
                      color, 2)


def _flagpole(cv, x, y, h, color):
    cv.vline(x, y, h, color)
    cv.circle(x, y, 2, color)


def art_gulf(cv, x, y, w, h):
    _sky(cv, x, y, w, h, DUSK, (240, 200, 150))
    sea_y = y + int(h * 0.62)
    cv.rect(x, sea_y, w, y + h - sea_y, SEA)
    cv.hline(x, sea_y, w, (255, 255, 255))
    # ship silhouette
    sx, sy = x + w // 8, sea_y + (y + h - sea_y) // 2
    cv.rect(sx, sy, w // 3, h // 10, INK)
    cv.rect(sx + w // 12, sy - h // 12, w // 9, h // 12, INK)
    cv.rect(sx + w // 5, sy - h // 12, w // 12, h // 12, (90, 40, 40))
    # burst on the water + drones in the sky
    bx, by = x + int(w * 0.72), sea_y + (y + h - sea_y) // 2
    _burst(cv, bx, by, max(6, h // 8), ORANGE)
    _burst(cv, bx, by, max(3, h // 16), (255, 220, 120))
    _drone(cv, x + int(w * 0.30), y + h // 5, max(3, h // 22), INK)
    _drone(cv, x + int(w * 0.52), y + h // 8, max(3, h // 26), INK)
    _drone(cv, x + int(w * 0.82), y + h // 4, max(3, h // 24), INK)


def art_apec(cv, x, y, w, h):
    _sky(cv, x, y, w, h, (190, 215, 235), (240, 235, 220))
    # Shenzhen towers
    base = y + h
    towers = [(0.04, 0.55), (0.16, 0.75), (0.30, 0.62), (0.44, 0.88),
              (0.58, 0.70), (0.72, 0.80), (0.86, 0.58)]
    for fx, fh in towers:
        tw = max(4, w // 16)
        tx = x + int(fx * w)
        th = int(fh * h * 0.55)
        cv.rect(tx, base - th, tw, th, (70, 85, 105))
        for wy in range(base - th + 4, base - 4, 7):
            cv.rect(tx + 1, wy, tw - 2, 1, (200, 215, 225))
    # three flags on one table line
    table_y = base - int(h * 0.10)
    cv.rect(x, table_y, w, 2, INK)
    fw, fh = w // 6, int(h * 0.24)
    # China: red field, yellow stars
    fx = x + w // 12
    fy = table_y - fh
    cv.rect(fx, fy, fw, fh, RED)
    cv.circle(fx + fw // 4, fy + fh // 3, max(2, fh // 8), GOLD)
    cv.circle(fx + int(fw * 0.6), fy + fh // 4, 1, GOLD)
    cv.circle(fx + int(fw * 0.65), fy + int(fh * 0.55), 1, GOLD)
    _flagpole(cv, fx, fy, fh + int(h * 0.10), INK)
    # Russia: white / blue / red bands
    fx = x + w // 2 - fw // 2
    cv.rect(fx, fy, fw, fh // 3, WHITE)
    cv.rect(fx, fy + fh // 3, fw, fh // 3, BLUE)
    cv.rect(fx, fy + 2 * fh // 3, fw, fh // 3, RED)
    cv.rect(fx, fy, fw, 1, INK)
    _flagpole(cv, fx, fy, fh + int(h * 0.10), INK)
    # USA: stripes + blue canton
    fx = x + w - w // 12 - fw
    for i in range(7):
        cv.rect(fx, fy + i * fh // 7, fw, fh // 7,
                RED if i % 2 == 0 else WHITE)
    cv.rect(fx, fy, fw // 2, fh * 4 // 7, BLUE)
    cv.circle(fx + fw // 4, fy + fh // 4, 1, WHITE)
    _flagpole(cv, fx, fy, fh + int(h * 0.10), INK)


def art_kerch(cv, x, y, w, h):
    _sky(cv, x, y, w, h, SKY, (225, 235, 240))
    water_y = y + int(h * 0.66)
    cv.rect(x, water_y, w, y + h - water_y, (70, 120, 160))
    deck_y = y + int(h * 0.52)
    # bridge deck: left span level, right span tilted down into the gap
    cv.rect(x + 2, deck_y, w // 2 - w // 12, max(3, h // 18), GREY)
    cv.polygon([(x + w // 2 - w // 12, deck_y),
                (x + w // 2 + w // 10, deck_y + h // 8),
                (x + w - 2, deck_y + h // 8),
                (x + w - 2, deck_y + h // 8 + max(3, h // 18)),
                (x + w // 2 + w // 10, deck_y + h // 8 + max(3, h // 18)),
                (x + w // 2 - w // 12, deck_y + max(3, h // 18))], GREY)
    # arch under the left span
    cv.ellipse(x + w // 4, deck_y + h // 6, w // 5, h // 8, LIGHTGREY)
    # support pillars
    cv.rect(x + w // 8, deck_y, 3, water_y - deck_y, GREY)
    cv.rect(x + w // 3, deck_y, 3, water_y - deck_y, GREY)
    # smoke over the gap
    gx = x + w // 2
    cv.circle(gx, deck_y - h // 10, max(4, h // 12), (90, 90, 90))
    cv.circle(gx + w // 14, deck_y - h // 6, max(3, h // 16), (120, 120, 120))
    cv.circle(gx - w // 16, deck_y - h // 7, max(3, h // 18), (110, 110, 110))
    _drone(cv, x + int(w * 0.78), y + h // 6, max(3, h // 24), INK)
    _drone(cv, x + int(w * 0.20), y + h // 8, max(3, h // 28), INK)


def art_cop31(cv, x, y, w, h):
    _sky(cv, x, y, w, h, (150, 195, 225), (235, 240, 235))
    # sun
    cv.circle(x + int(w * 0.14), y + int(h * 0.20), max(5, h // 9), GOLD)
    # globe
    gx, gy, gr = x + int(w * 0.52), y + int(h * 0.42), max(8, h // 4)
    cv.circle(gx, gy, gr, BLUE)
    cv.ellipse(gx - gr // 2, gy - gr // 3, gr // 3, gr // 4, GREEN)
    cv.ellipse(gx + gr // 6, gy + gr // 6, gr // 4, gr // 5, GREEN)
    cv.ellipse(gx - gr // 5, gy + gr // 3, gr // 5, gr // 6, DARKGREEN)
    cv.circle(gx, gy, gr, BLUE, fill=False)
    # tree
    tx = x + int(w * 0.80)
    cv.rect(tx - 2, y + int(h * 0.55), 4, int(h * 0.28), (110, 70, 30))
    cv.circle(tx, y + int(h * 0.48), max(5, h // 9), GREEN)
    cv.circle(tx - h // 12, y + int(h * 0.56), max(4, h // 12), DARKGREEN)
    cv.circle(tx + h // 12, y + int(h * 0.56), max(4, h // 12), GREEN)
    # wind turbine
    wx = x + int(w * 0.28)
    cv.vline(wx, y + int(h * 0.45), int(h * 0.38), INK)
    hub_y = y + int(h * 0.45)
    cv.circle(wx, hub_y, 2, INK)
    import math
    for k in range(3):
        a = math.pi * (0.5 + 2 * k / 3)
        cv.line(wx, hub_y, int(wx + h // 5 * math.cos(a)),
                int(hub_y + h // 5 * math.sin(a)), INK)
    # waves at the bottom
    wy = y + int(h * 0.86)
    for i in range(4):
        cv.line(x + i * w // 4, wy + (i % 2) * 2,
                x + (i + 1) * w // 4, wy + ((i + 1) % 2) * 2, BLUE)


def art_voyager(cv, x, y, w, h):
    cv.rect(x, y, w, h, (8, 10, 24))
    # fixed star field (deterministic positions)
    stars = [(0.08, 0.15), (0.22, 0.08), (0.35, 0.22), (0.48, 0.10),
             (0.62, 0.18), (0.75, 0.08), (0.88, 0.20), (0.15, 0.38),
             (0.55, 0.35), (0.82, 0.42), (0.30, 0.55), (0.68, 0.55),
             (0.92, 0.60), (0.10, 0.70), (0.40, 0.75), (0.85, 0.78)]
    for fx, fy in stars:
        cv.px(x + int(fx * w), y + int(fy * h), WHITE)
        if int(fx * 100) % 3 == 0:
            cv.px(x + int(fx * w) + 1, y + int(fy * h), WHITE)
    # signal arcs from Earth (bottom left) to the probe
    ex, ey = x + int(w * 0.12), y + int(h * 0.88)
    cv.circle(ex, ey, max(4, h // 10), (90, 140, 200), fill=False)
    cv.circle(ex, ey, max(8, h // 6), (70, 110, 170), fill=False)
    # probe: gold dish + body + boom
    px, py = x + int(w * 0.66), y + int(h * 0.38)
    cv.ellipse(px, py, max(6, w // 9), max(4, h // 10), (220, 180, 80))
    cv.ellipse(px, py, max(3, w // 18), max(2, h // 20), (160, 120, 40))
    cv.rect(px - w // 14, py + h // 12, w // 7, max(4, h // 12), (200, 200, 200))
    cv.thick_line(px + w // 14, py + h // 8, px + w // 4, py - h // 6,
                  (200, 200, 200), 2)
    cv.circle(px + w // 4, py - h // 6, 2, GOLD)


def art_anthropic(cv, x, y, w, h):
    cv.rect(x, y, w, h, WHITE)
    base = y + int(h * 0.84)
    # axes
    cv.hline(x + w // 10, base, w - w // 5, INK)
    cv.vline(x + w // 10, y + h // 8, base - (y + h // 8), INK)
    # bars: small, medium, huge
    bw = w // 6
    bars = [(0.18, 0.18, GREY), (0.42, 0.38, GREY), (0.66, 0.72, ORANGE)]
    for fx, fh, col in bars:
        bh = int(fh * h * 0.85)
        cv.rect(x + int(fx * w), base - bh, bw, bh, col)
    # arrow up over the bars
    cv.thick_line(x + int(w * 0.16), base - int(h * 0.12),
                  x + int(w * 0.86), y + int(h * 0.10), RED, 2)
    ax, ay = x + int(w * 0.86), y + int(h * 0.10)
    cv.line(ax, ay, ax - 8, ay + 2, RED)
    cv.line(ax, ay, ax - 2, ay + 8, RED)


def art_gaza(cv, x, y, w, h):
    _sky(cv, x, y, w, h, (235, 220, 180), SAND)
    ground = y + int(h * 0.68)
    cv.rect(x, ground, w, y + h - ground, (200, 175, 130))
    # tents
    for i, fx in enumerate([0.08, 0.30, 0.52]):
        tx = x + int(fx * w)
        tw = w // 6
        th = int(h * 0.22)
        cv.polygon([(tx, ground), (tx + tw // 2, ground - th),
                    (tx + tw, ground)], WHITE if i % 2 == 0 else (235, 230, 215))
        cv.line(tx + tw // 2, ground - th, tx + tw // 2, ground, GREY)
    # the Yellow Line
    ly = ground - int(h * 0.10)
    cv.rect(x, ly, w, max(2, h // 24), (230, 200, 40))
    # tank silhouette
    tx = x + int(w * 0.74)
    cv.rect(tx, ground - int(h * 0.14), w // 5, int(h * 0.14), (70, 75, 70))
    cv.rect(tx + w // 20, ground - int(h * 0.22), w // 10, int(h * 0.08),
            (70, 75, 70))
    cv.line(tx + w // 10, ground - int(h * 0.20), tx + w // 4,
            ground - int(h * 0.24), (70, 75, 70))
    # smoke
    cv.circle(x + int(w * 0.62), y + int(h * 0.30), max(4, h // 12),
              (120, 120, 120))
    cv.circle(x + int(w * 0.68), y + int(h * 0.22), max(3, h // 16),
              (140, 140, 140))


def art_quad(cv, x, y, w, h):
    _sky(cv, x, y, w, h, (185, 210, 235), (240, 238, 228))
    table_y = y + int(h * 0.62)
    cv.rect(x, table_y, w, 2, INK)
    fw, fh = w // 6, int(h * 0.26)
    fy = table_y - fh
    # USA
    fx = x + w // 14
    for i in range(7):
        cv.rect(fx, fy + i * fh // 7, fw, fh // 7,
                RED if i % 2 == 0 else WHITE)
    cv.rect(fx, fy, fw // 2, fh * 4 // 7, BLUE)
    _flagpole(cv, fx, fy, fh + int(h * 0.08), INK)
    # India: saffron / white / green + wheel
    fx = x + int(w * 0.30)
    cv.rect(fx, fy, fw, fh // 3, (255, 153, 51))
    cv.rect(fx, fy + fh // 3, fw, fh // 3, WHITE)
    cv.rect(fx, fy + 2 * fh // 3, fw, fh // 3, (19, 136, 8))
    cv.circle(fx + fw // 2, fy + fh // 2, max(2, fh // 8), BLUE, fill=False)
    _flagpole(cv, fx, fy, fh + int(h * 0.08), INK)
    # Australia: blue + stars
    fx = x + int(w * 0.54)
    cv.rect(fx, fy, fw, fh, (0, 40, 120))
    cv.circle(fx + fw // 4, fy + fh // 4, 1, WHITE)
    cv.circle(fx + int(fw * 0.7), fy + fh // 3, 1, WHITE)
    cv.circle(fx + int(fw * 0.6), fy + int(fh * 0.7), 1, WHITE)
    _flagpole(cv, fx, fy, fh + int(h * 0.08), INK)
    # Japan: white + red disc
    fx = x + int(w * 0.78)
    cv.rect(fx, fy, fw, fh, WHITE)
    cv.circle(fx + fw // 2, fy + fh // 2, max(2, fh // 5), RED)
    _flagpole(cv, fx, fy, fh + int(h * 0.08), INK)
    # four linked dots below: the network
    ny = y + int(h * 0.82)
    for i in range(4):
        dx = x + int(w * (0.18 + 0.21 * i))
        cv.circle(dx, ny, max(3, h // 20), BLUE)
        if i:
            cv.line(x + int(w * (0.18 + 0.21 * (i - 1))), ny, dx, ny, BLUE)


def art_markets(cv, x, y, w, h):
    cv.rect(x, y, w, h, WHITE)
    base = y + int(h * 0.86)
    cv.hline(x + w // 10, base, w - w // 5, INK)
    # grid
    for i in range(1, 4):
        gy = y + i * h // 5
        cv.hline(x + w // 10, gy, w - w // 5, LIGHTGREY)
    # candles: falling red, one green bounce
    candles = [(0.16, 0.30, 0.42, RED), (0.32, 0.42, 0.52, RED),
               (0.48, 0.52, 0.62, RED), (0.64, 0.62, 0.58, GREEN),
               (0.80, 0.58, 0.68, RED)]
    for fx, top_f, bot_f, col in candles:
        cx = x + int(fx * w)
        cw = max(4, w // 18)
        top = y + int(top_f * h)
        bot = y + int(bot_f * h)
        cv.vline(cx + cw // 2, top - h // 14, (bot - top) + h // 7, col)
        cv.rect(cx, top, cw, max(3, bot - top), col)
    # red arrow down
    cv.thick_line(x + int(w * 0.12), y + int(h * 0.18),
                  x + int(w * 0.88), y + int(h * 0.62), RED, 2)
    ax, ay = x + int(w * 0.88), y + int(h * 0.62)
    cv.line(ax, ay, ax - 8, ay - 2, RED)
    cv.line(ax, ay, ax - 2, ay - 8, RED)


def art_measles(cv, x, y, w, h):
    cv.rect(x, y, w, h, (250, 244, 232))
    # virus cluster: spiked red discs
    import math
    spots = [(0.24, 0.34, 0.16), (0.62, 0.28, 0.20), (0.42, 0.62, 0.18),
             (0.78, 0.62, 0.13), (0.15, 0.72, 0.10)]
    for fx, fy, fr in spots:
        cx, cy = x + int(fx * w), y + int(fy * h)
        r = max(5, int(fr * h))
        for k in range(8):
            a = math.pi * k / 4
            cv.line(cx, cy, int(cx + (r + 4) * math.cos(a)),
                    int(cy + (r + 4) * math.sin(a)), RED)
        cv.circle(cx, cy, r, RED)
        cv.circle(cx - r // 3, cy - r // 3, max(1, r // 4), (255, 120, 120))
    # small dots spreading
    for fx, fy in [(0.85, 0.30), (0.90, 0.45), (0.08, 0.45), (0.55, 0.85)]:
        cv.circle(x + int(fx * w), y + int(fy * h), 2, RED)


def art_ebola(cv, x, y, w, h):
    cv.rect(x, y, w, h, (238, 240, 232))
    # stylised Africa blob
    cx, cy = x + w // 2, y + h // 2
    blob = [(cx - w // 5, cy - h // 3), (cx + w // 6, cy - h // 3),
            (cx + w // 4, cy - h // 6), (cx + w // 5, cy + h // 6),
            (cx + w // 10, cy + h // 3), (cx - w // 12, cy + h // 4),
            (cx - w // 4, cy + h // 8), (cx - w // 4, cy - h // 6)]
    cv.polygon(blob, DARKGREEN)
    # red crosses on the outbreak zone
    for fx, fy in [(0.52, 0.42), (0.60, 0.55), (0.44, 0.58)]:
        px, py = x + int(fx * w), y + int(fy * h)
        s = max(3, h // 16)
        cv.rect(px - s, py - s // 3, s * 2, s * 2 // 3, RED)
        cv.rect(px - s // 3, py - s, s * 2 // 3, s * 2, RED)
    for fx, fy in [(0.30, 0.30), (0.72, 0.30), (0.80, 0.70), (0.25, 0.75)]:
        cv.circle(x + int(fx * w), y + int(fy * h), 2, RED)


def art_jeffries(cv, x, y, w, h):
    _sky(cv, x, y, w, h, (120, 150, 195), (215, 225, 235))
    base = y + int(h * 0.88)
    cx = x + w // 2
    # dome
    cv.ellipse(cx, base - int(h * 0.30), w // 4, int(h * 0.30), WHITE)
    cv.rect(cx - w // 4, base - int(h * 0.30), w // 2, int(h * 0.30), WHITE)
    cv.rect(cx - 2, base - int(h * 0.62), 4, int(h * 0.08), INK)
    cv.rect(cx - w // 20, base - int(h * 0.70), w // 10, int(h * 0.10), RED)
    # columns
    for i in range(-2, 3):
        col_x = cx + i * w // 7 - 2
        cv.rect(col_x, base - int(h * 0.28), 4, int(h * 0.28), (200, 205, 210))
    cv.rect(x + w // 8, base - int(h * 0.30), w * 3 // 4, 3, INK)
    cv.rect(x, base, w, y + h - base, (90, 105, 120))


def art_royals(cv, x, y, w, h):
    _sky(cv, x, y, w, h, (240, 190, 120), (250, 225, 180))
    base = y + int(h * 0.90)
    # Gateway of India arch: two pillars + round arch
    ax0, ax1 = x + w // 5, x + w * 4 // 5
    cv.rect(ax0, y + int(h * 0.42), w // 10, base - (y + int(h * 0.42)),
            (150, 110, 70))
    cv.rect(ax1 - w // 10, y + int(h * 0.42), w // 10,
            base - (y + int(h * 0.42)), (150, 110, 70))
    cv.ellipse(x + w // 2, y + int(h * 0.42), w * 3 // 10, int(h * 0.30),
               (150, 110, 70))
    cv.ellipse(x + w // 2, y + int(h * 0.52), w // 5, int(h * 0.18),
               (250, 225, 180))
    cv.rect(ax0, base - 3, ax1 - ax0, 3, (120, 85, 50))
    # crown above the arch
    cx, cy = x + w // 2, y + int(h * 0.20)
    s = max(5, h // 10)
    cv.polygon([(cx - s, cy + s // 2), (cx - s, cy - s // 2),
                (cx - s // 2, cy), (cx, cy - s),
                (cx + s // 2, cy), (cx + s, cy - s // 2),
                (cx + s, cy + s // 2)], GOLD)
    cv.circle(cx, cy - s, 2, RED)
    cv.circle(cx - s // 2, cy - s // 2, 1, BLUE)
    cv.circle(cx + s // 2, cy - s // 2, 1, BLUE)


ARTS = {
    "gulf": art_gulf, "apec": art_apec, "kerch": art_kerch,
    "cop31": art_cop31, "voyager": art_voyager, "anthropic": art_anthropic,
    "gaza": art_gaza, "quad": art_quad, "markets": art_markets,
    "measles": art_measles, "ebola": art_ebola, "jeffries": art_jeffries,
    "royals": art_royals,
}
