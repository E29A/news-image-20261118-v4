"""Pure-standard-library drawing engine for news-image-20261118 v4.

No third-party imports: the make.fun sandbox runs main.py with the
standard library only, so this module draws into an RGB bytearray and
encodes the PNG by hand (zlib + struct + binascii).

Text comes from fontdata.py, rasterised locally by gen_fonts.py from the
system DejaVu fonts. Glyphs are 2-bit grayscale bitmaps; drawing blends
them over the background (alpha = level / 3).
"""

import binascii
import math
import struct
import zlib

import fontdata

# ---------------------------------------------------------------- fonts ---

_FONTS = {}  # key -> {char: (advance, w, h, top, bytes)}


def _load_font(key):
    if key in _FONTS:
        return _FONTS[key]
    raw = fontdata.FONTS[key]
    table = {}
    for item in raw.split(";"):
        if not item:
            continue
        code, rest = item.split(":", 1)
        adv, w, h, top, hx = rest.split(",", 4)
        table[chr(int(code))] = (
            int(adv), int(w), int(h), int(top),
            bytes.fromhex(hx) if hx else b"",
        )
    _FONTS[key] = table
    return table


def text_width(font, text):
    """Advance width of `text` in font `font` (e.g. 'serif-bold-22')."""
    table = _load_font(font)
    total = 0
    for ch in text:
        g = table.get(ch) or table["?"]
        total += g[0]
    return total


def wrap_text(font, text, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(font, trial) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(font, text, max_width, max_lines=None):
    """Wrap, then drop whole trailing words until it fits max_lines."""
    lines = wrap_text(font, text, max_width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
    return lines


# --------------------------------------------------------------- canvas ---

class Canvas:
    def __init__(self, width, height, bg):
        self.w = width
        self.h = height
        self.buf = bytearray(bg) * (width * height)

    # -- pixels ------------------------------------------------------
    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = self._idx(x, y)
            self.buf[i:i + 3] = bytes(color)

    def blend_px(self, x, y, color, alpha):
        """alpha 0.0..1.0 blend of color over the current pixel."""
        if 0 <= x < self.w and 0 <= y < self.h and alpha > 0:
            i = self._idx(x, y)
            b = self.buf
            b[i] = int(b[i] + (color[0] - b[i]) * alpha)
            b[i + 1] = int(b[i + 1] + (color[1] - b[i + 1]) * alpha)
            b[i + 2] = int(b[i + 2] + (color[2] - b[i + 2]) * alpha)

    # -- shapes ------------------------------------------------------
    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            i = self._idx(x0, yy)
            row = bytes(color) * (x1 - x0)
            self.buf[i:i + (x1 - x0) * 3] = row

    def hline(self, x, y, w, color):
        self.rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.rect(x, y, 1, h, color)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.px(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def thick_line(self, x0, y0, x1, y1, color, t=2):
        for ox in range(-(t // 2), t // 2 + 1):
            for oy in range(-(t // 2), t // 2 + 1):
                self.line(x0 + ox, y0 + oy, x1 + ox, y1 + oy, color)

    def circle(self, cx, cy, r, color, fill=True):
        if r <= 0:
            return
        if fill:
            for yy in range(cy - r, cy + r + 1):
                dx = int((r * r - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) <= r else 0
                self.rect(cx - dx, yy, dx * 2 + 1, 1, color)
        else:
            steps = max(24, int(6.28 * r))
            prev = None
            for i in range(steps + 1):
                a = 2 * math.pi * i / steps
                p = (int(cx + r * math.cos(a)), int(cy + r * math.sin(a)))
                if prev is not None:
                    self.line(prev[0], prev[1], p[0], p[1], color)
                prev = p

    def ellipse(self, cx, cy, rx, ry, color, fill=True):
        if rx <= 0 or ry <= 0:
            return
        if fill:
            for yy in range(cy - ry, cy + ry + 1):
                t = (yy - cy) / ry
                dx = int(rx * (max(0.0, 1 - t * t)) ** 0.5)
                self.rect(cx - dx, yy, dx * 2 + 1, 1, color)
        else:
            steps = max(32, int(6.28 * max(rx, ry)))
            prev = None
            for i in range(steps + 1):
                a = 2 * math.pi * i / steps
                p = (int(cx + rx * math.cos(a)), int(cy + ry * math.sin(a)))
                if prev is not None:
                    self.line(prev[0], prev[1], p[0], p[1], color)
                prev = p

    def polygon(self, points, color):
        """Scanline fill of a simple polygon (even-odd)."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    t = (y - y0) / (y1 - y0)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                xa, xb = int(xs[j]), int(xs[j + 1])
                if xb > xa:
                    self.rect(xa, y, xb - xa, 1, color)

    def polyline(self, points, color):
        for a, b in zip(points, points[1:]):
            self.line(a[0], a[1], b[0], b[1], color)

    # -- text --------------------------------------------------------
    def text(self, font, x, y, s, color, align="left"):
        """Draw text with its baseline at y. align: left/center/right."""
        table = _load_font(font)
        if align != "left":
            w = text_width(font, s)
            if align == "center":
                x -= w // 2
            else:
                x -= w
        cx = x
        for ch in s:
            g = table.get(ch) or table["?"]
            adv, w, h, top, data = g
            if w and h:
                # glyph top row sits `top` px above the baseline.
                gy0 = y - top
                bitpos = 0
                total_px = w * h
                for k in range(total_px):
                    q = (data[k // 4] >> (6 - 2 * (k % 4))) & 3
                    if q:
                        px = cx + (k % w)
                        py = gy0 + (k // w)
                        self.blend_px(px, py, color, q / 3.0)
            cx += adv
        return cx

    def text_lines(self, font, x, y, lines, color, leading=None, align="left"):
        """Draw lines with baselines stepping by `leading` (default size+3)."""
        size = int(font.rsplit("-", 1)[1])
        step = leading if leading is not None else size + 3
        for ln in lines:
            self.text(font, x, y, ln, color, align=align)
            y += step
        return y

    # -- output ------------------------------------------------------
    def png_bytes(self):
        raw = bytearray()
        stride = self.w * 3
        for yy in range(self.h):
            raw.append(0)  # filter: none
            raw += self.buf[yy * stride:(yy + 1) * stride]
        comp = zlib.compress(bytes(raw), 9)
        def chunk(tag, data):
            out = struct.pack(">I", len(data)) + tag + data
            out += struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF)
            return out

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", comp) + chunk(b"IEND", b""))
