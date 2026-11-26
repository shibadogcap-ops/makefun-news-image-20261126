"""Schematic world map for band B8 (map band, y 784-884).

NOT a geographic rendering: continent blocks are simple rectangles
relative to the map-field origin. Field is 528x82 px, top-left at
(x, y) passed to draw_map.

Python stdlib only. Deterministic: no randomness, no clocks.
"""

import draw

# Continent blocks as (x, y, w, h) rects RELATIVE to the map field
# origin (field 528x82). Multi-part continents are lists of rects;
# the first rect is the pin anchor for that continent.
CONTINENTS = {
    "N AMERICA": [(8, 6, 118, 32), (26, 38, 58, 12)],
    "S AMERICA": [(102, 46, 42, 28)],
    "EUROPE": [(236, 4, 62, 22)],
    "AFRICA": [(244, 30, 70, 38)],
    "ASIA": [(308, 2, 148, 34), (398, 36, 48, 14)],
    "OCEANIA": [(450, 56, 54, 16)],
}

PIN_RADIUS = 9


class _PinCanvas:
    """Canvas adapter for draw.pin: Canvas.circle(fill=True) in draw.py
    crashes on negative sqrt; this supplies an equivalent filled disc
    and delegates everything else to the real canvas."""

    def __init__(self, cv):
        self._cv = cv

    def __getattr__(self, name):
        return getattr(self._cv, name)

    def circle(self, cx, cy, r, color, fill=True):
        if not fill:
            return self._cv.circle(cx, cy, r, color, fill=False)
        rr = float(r) * r
        y_min = int(max(0, cy - r))
        y_max = int(min(self._cv.h - 1, cy + r + 1))
        for yy in range(y_min, y_max + 1):
            dy = yy - cy
            rem = rr - dy * dy
            if rem < 0:
                continue
            span = rem ** 0.5
            x_min = int(max(0, cx - span))
            x_max = int(min(self._cv.w - 1, cx + span))
            for xx in range(x_min, x_max + 1):
                self._cv.set_pixel(xx, yy, color)

# Region labels (story["region"]) -> map block key. "ASIA-PACIFIC" and
# "MIDDLE EAST" have no separate blocks; both pin to "ASIA".
REGION_TO_BLOCK = {
    "N AMERICA": "N AMERICA",
    "S AMERICA": "S AMERICA",
    "EUROPE": "EUROPE",
    "AFRICA": "AFRICA",
    "ASIA-PACIFIC": "ASIA",
    "MIDDLE EAST": "ASIA",
    "OCEANIA": "OCEANIA",
}


def _pin_center(block, dx, dy):
    """Clamp a pin centre so the r=9 disc stays inside its block rect."""
    bx, by, bw, bh = block
    lo_x = PIN_RADIUS if bw >= 2 * PIN_RADIUS else bw / 2.0
    hi_x = bw - PIN_RADIUS if bw >= 2 * PIN_RADIUS else bw / 2.0
    lo_y = PIN_RADIUS if bh >= 2 * PIN_RADIUS else bh / 2.0
    hi_y = bh - PIN_RADIUS if bh >= 2 * PIN_RADIUS else bh / 2.0
    cx = min(max(dx, lo_x), hi_x)
    cy = min(max(dy, lo_y), hi_y)
    return cx, cy


def draw_map(cv, x, y, pins):
    """Draw the schematic map into the field whose top-left is (x, y).

    Field is 528x82. Each continent block is LIGHT-filled with a 1 px
    INK frame. pins is a list of (block_key, dx, dy, n) where dx, dy
    is the pin-centre offset in px from that block's top-left corner
    and n is the story number; the pin is an ACCENT filled circle
    radius 9 with n in PAPER at scale 1, centred.
    """
    for rects in CONTINENTS.values():
        for rx, ry, rw, rh in rects:
            cv.rect(x + rx, y + ry, rw, rh, draw.LIGHT)
            cv.frame(x + rx, y + ry, rw, rh, draw.INK, 1)
    for block_key, dx, dy, n in pins:
        rects = CONTINENTS.get(block_key)
        if not rects:
            continue
        cx, cy = _pin_center(rects[0], dx, dy)
        draw.pin(_PinCanvas(cv), x + rects[0][0] + cx, y + rects[0][1] + cy, str(n))


def region_counts(stories):
    """Count stories per region key.

    stories: list of dicts each with a "region" key (continent keys:
    "N AMERICA", "S AMERICA", "EUROPE", "AFRICA", "ASIA-PACIFIC",
    "MIDDLE EAST", "OCEANIA"). Returns a list of (region, count)
    tuples sorted by count descending; ties keep first-seen order.
    """
    counts = {}
    for s in stories:
        region = s.get("region")
        if region is None:
            continue
        counts[region] = counts.get(region, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])


def format_region_lines(counts, max_chars=35, max_lines=5):
    """Format (region, count) tuples into wrapped scale-2 lines.

    Items are "REGION N" joined by " · " (middle dot); every line
    except the last ends with a trailing " ·". At most max_lines
    lines; overflow items are merged into the final line.
    """
    items = ["%s %d" % (region, count) for region, count in counts]
    if not items:
        return []
    lines = []
    cur = items[0]
    for item in items[1:]:
        candidate = cur + " · " + item
        if len(candidate) <= max_chars:
            cur = candidate
        else:
            lines.append(cur + " ·")
            cur = item
    lines.append(cur)
    while len(lines) > max_lines:
        merged = lines[max_lines - 1] + " · " + lines[max_lines].rstrip(" ·")
        lines[max_lines - 1:max_lines + 1] = [merged]
    return lines
