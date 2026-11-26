"""Canvas + PNG writer for the news-image broadsheet renderer.

Python stdlib only (zlib, struct). 1024x1024 RGB buffer on PAPER.
Deterministic: fixed zlib level, no metadata chunks beyond
IHDR/IDAT/IEND.
"""

import struct
import zlib

INK = (24, 24, 28)
PAPER = (246, 242, 233)
ACCENT = (164, 32, 40)
GREY = (110, 108, 100)
LIGHT = (226, 220, 205)
BLUE = (36, 64, 120)
GOLD = (176, 132, 40)
GREEN = (44, 96, 60)
SKY = (168, 196, 224)

W = 1024
H = 1024


def _png_chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(
        ">I", zlib.crc32(tag + data) & 0xFFFFFFFF
    )


class Canvas:
    def __init__(self, w=W, h=H):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        for i in range(0, len(self.px), 3):
            self.px[i:i + 3] = PAPER

    def set_pixel(self, x, y, color):
        x = int(x)
        y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        x0 = max(0, int(x))
        y0 = max(0, int(y))
        x1 = min(self.w, int(x) + int(w))
        y1 = min(self.h, int(y) + int(h))
        r, g, b = color
        for yy in range(y0, y1):
            row = (yy * self.w) * 3
            for xx in range(x0, x1):
                i = row + xx * 3
                self.px[i] = r
                self.px[i + 1] = g
                self.px[i + 2] = b

    def frame(self, x, y, w, h, color, thickness=1):
        for t in range(thickness):
            self.rect(x + t, y + t, w - 2 * t, thickness, color)
            self.rect(x + t, y + h - t - thickness, w - 2 * t, thickness, color)
            self.rect(x + t, y + t, thickness, h - 2 * t, color)
            self.rect(x + w - t - thickness, y + t, thickness, h - 2 * t, color)

    def line(self, x0, y0, x1, y1, color, thickness=1):
        x0 = int(round(x0))
        y0 = int(round(y0))
        x1 = int(round(x1))
        y1 = int(round(y1))
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        half = thickness // 2
        while True:
            for oy in range(-half, thickness - half):
                for ox in range(-half, thickness - half):
                    self.set_pixel(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, fill=True):
        cx = float(cx)
        cy = float(cy)
        r = float(r)
        if fill:
            rr = r * r
            y_min = int(max(0, cy - r))
            y_max = int(min(self.h - 1, cy + r + 1))
            for y in range(y_min, y_max + 1):
                dy = y - cy
                span = max(0.0, rr - dy * dy) ** 0.5
                x_min = int(max(0, cx - span))
                x_max = int(min(self.w - 1, cx + span))
                for x in range(x_min, x_max + 1):
                    self.set_pixel(x, y, color)
        else:
            # midpoint circle, one pixel outline
            x = r
            y = 0
            err = 1 - int(r)
            while x >= y:
                for px, py in (
                    (cx + x, cy + y), (cx + y, cy + x),
                    (cx - y, cy + x), (cx - x, cy + y),
                    (cx - x, cy - y), (cx - y, cy - x),
                    (cx + y, cy - x), (cx + x, cy - y),
                ):
                    self.set_pixel(px, py, color)
                y += 1
                if err < 0:
                    err += 2 * y + 1
                else:
                    x -= 1
                    err += 2 * (y - x) + 1

    def triangle(self, points, color):
        (x1, y1), (x2, y2), (x3, y3) = points
        min_x = int(min(x1, x2, x3))
        max_x = int(max(x1, x2, x3)) + 1
        min_y = int(min(y1, y2, y3))
        max_y = int(max(y1, y2, y3)) + 1
        d = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if d == 0:
            return
        for y in range(max(0, min_y), min(self.h, max_y)):
            for x in range(max(0, min_x), min(self.w, max_x)):
                w0 = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / d
                w1 = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / d
                w2 = 1 - w0 - w1
                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    self.set_pixel(x, y, color)

    def save_png(self, path):
        def chunk(tag, data):
            return _png_chunk(tag, data)

        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)  # filter type None
            raw += self.px[y * stride:(y + 1) * stride]
        compressed = zlib.compress(bytes(raw), 6)
        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        png = (
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", compressed)
            + chunk(b"IEND", b"")
        )
        with open(path, "wb") as f:
            f.write(png)


def chip(cv, x, y, n):
    """26x16 ACCENT rect at (x,y), story number n in PAPER, scale 2, centred."""
    import font
    cv.rect(x, y, 26, 16, ACCENT)
    font.draw_text_center(cv, str(n), x + 13, y + 8, PAPER, 2)


def pin(cv, cx, cy, n):
    """ACCENT filled circle radius 9 (map pin) with number n, PAPER, scale 1."""
    import font
    cv.circle(cx, cy, 9, ACCENT, fill=True)
    font.draw_text_center(cv, str(n), cx, cy, PAPER, 1)


def band(cv, y, h):
    """Full-width INK rect from x=28 to x=996 at y with height h."""
    cv.rect(28, y, 968, h, INK)
