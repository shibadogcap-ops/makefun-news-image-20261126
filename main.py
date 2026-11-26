"""News-image edition renderer: 26 November 2026, "THE THURSDAY LEDGER".

Bands drawn by draw_top(cv):
  B1 Masthead (y 20-102)      - title + stats strip
  B2 Dateline + timeline     - y 108-172
  B3 Lead A, story 1         - y 180-384
  B4 Leads B/C, stories 2-3  - y 392-496
  B5 Numbers band            - y 504-556

Bands drawn by draw_bottom(cv):
  B6 Cards grid              - y 564-732 (stories 4-13)
  B7 Date-check strip        - y 740-776
  B8 Map band                - y 784-884
  B9 Also-on list            - y 892-988 (stories 14-26)
  B10 Footer                 - y 994-1008

main() builds the full 1024x1024 canvas and writes entry.png to
MAKEFUN_OUTPUT_DIR (falling back to ".").
"""

import os
import sys

# ---------------------------------------------------------------------------
# sys.path bootstrap: the grader runs `python3 -P -s` from a foreign cwd, so
# the script's own directory is not on sys.path. Insert it explicitly, with
# MAKEFUN_BOT_DIR as fallback.
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else ""
if not _HERE:
    _HERE = os.environ.get("MAKEFUN_BOT_DIR", "")
if _HERE and _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import draw
import font
import map
import stories

# Content column and constants
CX0 = 28
CX1 = 996
COL_W = CX1 - CX0  # 968

PX_PER_HOUR = 37.3
AXIS_X0 = 64
AXIS_Y = 148
AXIS_X1 = 960


def _story(n):
    for s in stories.STORIES:
        if s["n"] == n:
            return s
    raise KeyError(n)


def _draw_stats_strip(cv):
    """B1 stats strip: INK rect with reversed PAPER text."""
    n_stories = len(stories.STORIES)
    n_regions = len({s["region"] for s in stories.STORIES})
    n_fields = len({s["field"] for s in stories.STORIES})
    text = (
        f"{n_stories} STORIES · {n_regions} CONTINENTS · "
        f"{n_fields} FIELDS · EVERY STORY DATED + SOURCED"
    )
    draw.band(cv, 76, 26)
    font.draw_text_center(cv, text, CX0 + COL_W // 2, 82, draw.PAPER, 2)


def _draw_masthead(cv):
    """B1: title + stats strip."""
    font.draw_text_center(cv, "THE THURSDAY LEDGER", CX0 + COL_W // 2, 22,
                          draw.INK, 7)
    _draw_stats_strip(cv)


def _draw_dateline(cv):
    """B2 dateline row + rule."""
    mid = CX0 + COL_W // 2  # 512
    font.draw_text(cv, "NO. 26", CX0, 108, draw.GREY, 2)
    font.draw_text_center(cv, "THURSDAY, 26 NOVEMBER 2026", mid, 108,
                          draw.INK, 2)
    font.draw_text_right(cv, "ALL TIMES UTC", CX1, 108, draw.GREY, 2)
    draw.band(cv, 128, 2)


def _draw_timeline(cv):
    """B2: UTC axis, ticks, hour labels, story pins."""
    cv.line(AXIS_X0, AXIS_Y, AXIS_X1, AXIS_Y, draw.INK, 1)

    # Ticks every 2 h: 4 px vertical marks centred on the axis.
    for h in range(0, 25, 2):
        x = AXIS_X0 + h * PX_PER_HOUR
        cv.line(x, AXIS_Y - 2, x, AXIS_Y + 2, draw.INK, 1)

    # Hour labels at 00/06/12/18/24 below the axis.
    for h in (0, 6, 12, 18, 24):
        x = AXIS_X0 + h * PX_PER_HOUR
        font.draw_text_center(cv, f"{h:02d}", x, 158, draw.GREY, 2)

    # Pins for stories with a verified UTC hour.
    for s in stories.STORIES:
        hour = s.get("hour_utc")
        if hour is None:
            continue
        x = AXIS_X0 + hour * PX_PER_HOUR
        cv.circle(x, AXIS_Y, 8, draw.ACCENT, fill=True)
        font.draw_text_center(cv, str(s["n"]), x, AXIS_Y, draw.PAPER, 1)


def _draw_lead_a_art(cv):
    """B3 art panel scene: night sky, missile trails, interception burst,
    Riyadh skyline with the Kingdom Centre tower. x 652-996, y 180-384.

    Panel frame + LIGHT caption strip occupy the outer 16 px at the bottom;
    the scene fills the interior.
    """
    px, py, pw, ph = 652, 180, 344, 204
    cv.frame(px, py, pw, ph, draw.INK, 1)

    # Night sky (interior, above the caption strip).
    cv.rect(px + 1, py + 1, pw - 2, ph - 17, draw.BLUE)

    # Stars: fixed small PAPER/GREY pixels.
    stars = [
        (672, 200, draw.PAPER), (700, 212, draw.GREY), (740, 196, draw.PAPER),
        (790, 205, draw.PAPER), (840, 196, draw.GREY), (880, 210, draw.PAPER),
        (920, 200, draw.PAPER), (950, 215, draw.GREY), (665, 240, draw.PAPER),
        (905, 245, draw.PAPER), (760, 235, draw.GREY), (985, 235, draw.PAPER),
    ]
    for sx, sy, col in stars:
        cv.rect(sx, sy, 2, 2, col)

    # Interception burst above the skyline, centre ~(812, 252).
    bx, by = 812, 252
    cv.circle(bx, by, 12, draw.ACCENT, fill=True)
    cv.circle(bx, by, 5, draw.PAPER, fill=True)
    for dx, dy in ((-22, 0), (22, 0), (0, -22), (0, 22),
                   (-15, -15), (15, 15), (-15, 15), (15, -15)):
        cv.line(bx + dx // 2, by + dy // 2, bx + dx, by + dy,
                draw.GOLD, 1)

    # Two inbound missile trails converging on the burst (GOLD).
    cv.line(700, 330, bx - 8, by + 8, draw.GOLD, 2)
    cv.line(906, 322, bx + 8, by + 6, draw.GOLD, 2)
    # Missile heads just short of the burst.
    cv.circle(716, 318, 3, draw.PAPER, fill=True)
    cv.circle(890, 310, 3, draw.PAPER, fill=True)

    # Riyadh skyline silhouette along the bottom (INK on BLUE).
    # (x, y_top, w) blocks; every building rises from the scene floor y = 366.
    buildings = [
        (660, 348, 18), (684, 354, 14), (704, 340, 16),
        (726, 350, 12), (744, 336, 14),
        # Kingdom Centre: tall tower, recognisable profile.
        (870, 312, 30),
        (916, 348, 16), (938, 354, 12), (956, 342, 20),
        (982, 352, 12),
    ]
    for x0, y0, w0 in buildings:
        cv.rect(x0, y0, w0, 366 - y0, draw.INK)
    # Taper the Kingdom Centre: overlay two INK triangles for the
    # characteristic sloped shoulders and a small GOLD antenna tip.
    cv.triangle([(870, 312), (900, 312), (885, 282)], draw.INK)
    cv.triangle([(900, 312), (930, 312), (915, 282)], draw.INK)
    cv.rect(884, 276, 2, 8, draw.GOLD)
    # Parabolic arch hint: small BLUE notch at the tower base.
    cv.circle(900, 360, 4, draw.BLUE, fill=True)

    # Caption strip: LIGHT fill in the bottom 16 px, INK scale-2 text.
    cv.rect(px + 1, py + ph - 16, pw - 2, 15, draw.LIGHT)
    font.draw_text_center(cv, "RIYADH - THIRD NIGHT", px + pw // 2,
                          py + ph - 15, draw.INK, 2)


def _draw_lead_a(cv):
    """B3: kicker + tag row, headline, rule, body (left column x28-636)."""
    s = _story(1)
    right = CX0 + 608  # 636

    # Kicker row y 180: region / field ACCENT left; tag right-aligned
    # (second outlet dropped - does not fit beside the kicker in 608 px).
    kicker = f"{s['region']} / {s['field']}"
    font.draw_text(cv, kicker, CX0, 180, draw.ACCENT, 2)
    first_outlet = s["outlet"].split(" + ")[0]
    tag = f"{first_outlet} · {s['status']}"
    font.draw_text_right(cv, tag, right, 180, draw.GREY, 2)

    # Headline y 196, scale 7, 2 lines, leading 57.
    for i, line in enumerate(s["headline"]):
        font.draw_text(cv, line, CX0, 196 + i * 57, draw.INK, 7)

    # ACCENT rule y 304.
    cv.rect(CX0, 304, 608, 3, draw.ACCENT)

    # Body y 310, scale 3, 3 lines, leading 26 (ends y 383).
    for i, line in enumerate(s["body"]):
        font.draw_text(cv, line, CX0, 310 + i * 26, draw.INK, 3)

    _draw_lead_a_art(cv)


def _draw_lead_bc(cv, n, x0):
    """B4 column for lead story n (2 or 3). Column x0..x0+471."""
    s = _story(n)
    right = x0 + 472

    # Header row y 392: chip + kicker ACCENT + tag right-aligned (GREY).
    draw.chip(cv, x0, 392, n)
    kicker = f"{s['region']} / {s['field']}"
    # Kicker starts 4 px after the 26 px chip; story 2's row is the tight
    # one (26 + 4 + 274 + 2 + 166 = 472 px exactly) but does not overlap.
    font.draw_text(cv, kicker, x0 + 30, 396, draw.ACCENT, 2)
    font.draw_text_right(cv, s["outlet"], right, 396, draw.GREY, 2)

    # Headline y 412, scale 5, 1 line.
    font.draw_text(cv, s["headline"][0], x0, 412, draw.INK, 5)

    # Body y 449, scale 3, 2 lines, leading 26 (ends y 496).
    for i, line in enumerate(s["body"]):
        font.draw_text(cv, line, x0, 449 + i * 26, draw.INK, 3)


def _draw_leads_bc(cv):
    """B4: two columns x28-500 / x524-996, hairline at x512."""
    cv.rect(512, 392, 1, 104, draw.INK)
    _draw_lead_bc(cv, 2, 28)
    _draw_lead_bc(cv, 3, 524)


def _draw_numbers(cv):
    """B5: INK band, five cells, PAPER hairlines, values + labels."""
    draw.band(cv, 504, 52)
    cell_w = 193
    for i, num in enumerate(stories.NUMBERS):
        x0 = CX0 + i * cell_w
        cx = x0 + cell_w // 2
        # Hairline divider to the right of each cell except the last.
        if i < len(stories.NUMBERS) - 1:
            cv.rect(x0 + cell_w, 504, 1, 52, draw.PAPER)
        font.draw_text_center(cv, num["value"], cx, 508, draw.PAPER, 4)
        font.draw_text_center(cv, num["label"], cx, 540, draw.PAPER, 2)


def draw_top(cv):
    """Draw bands B1-B5 (top half of the edition) onto cv."""
    _draw_masthead(cv)
    _draw_dateline(cv)
    _draw_timeline(cv)
    _draw_lead_a(cv)
    _draw_leads_bc(cv)
    _draw_numbers(cv)


# ---------------------------------------------------------------------------
# Bottom half: B6 cards, B7 date-check, B8 map band, B9 also-on, B10 footer
# ---------------------------------------------------------------------------

CARD_W = 186
CARD_H = 80
CARD_XS = [28, 223, 418, 613, 808]
CARD_YS = [564, 652]

# Pin offsets (dx, dy from the continent block's top-left) per story,
# chosen so adjacent pin centres stay >= 20 px apart.
PIN_OFFSETS = {
    # ASIA block (148x34): stories 1, 4, 5, 9, 10, 12, 13.
    1: (18, 11), 4: (38, 23), 5: (58, 11), 9: (78, 23), 10: (98, 11),
    12: (118, 23), 13: (136, 11),
    # N AMERICA block (118x32): stories 2, 3, 6, 7. dy 21 (not 23) keeps
    # the r=9 disc's bottom row off the block's bottom INK frame row.
    2: (18, 11), 3: (48, 21), 6: (78, 11), 7: (104, 21),
    # EUROPE (62x22): story 8. AFRICA (70x38): story 11.
    8: (31, 11), 11: (35, 19),
}


def _card_tag(s):
    """Card header tag: full outlet if <= 13 chars, else first outlet."""
    outlet = s["outlet"]
    if len(outlet) <= 13:
        return outlet
    return outlet.split(" + ")[0]


def _draw_card(cv, s, x, y):
    """One B6 card (186x80, LIGHT fill, no frame) at top-left (x, y)."""
    cv.rect(x, y, CARD_W, CARD_H, draw.LIGHT)
    draw.chip(cv, x, y, s["n"])
    font.draw_text_right(cv, _card_tag(s), x + CARD_W, y + 4,
                         draw.GREY, 2)

    if isinstance(s["summary"], str):
        # Variant A (headline-led): 2 headline lines, 1 summary line.
        for i, line in enumerate(s["headline"]):
            font.draw_text(cv, line, x, y + 20 + i * 23, draw.INK, 3)
        font.draw_text(cv, s["summary"], x, y + 66, draw.INK, 2)
    else:
        # Variant B (summary-led): 1 headline line, 2 summary lines.
        font.draw_text(cv, s["headline"][0], x, y + 20, draw.INK, 3)
        for i, line in enumerate(s["summary"]):
            font.draw_text(cv, line, x, y + 44 + i * 18, draw.INK, 2)


def _draw_cards(cv):
    """B6: stories 4-13 in a 5x2 grid; empty cells stay bare PAPER."""
    cards = [s for s in stories.STORIES if 4 <= s["n"] <= 13]
    for i, s in enumerate(cards):
        x = CARD_XS[i % 5]
        y = CARD_YS[i // 5]
        _draw_card(cv, s, x, y)


def _draw_date_check(cv):
    """B7: outlined box with the two DATE_CHECK_LINES, scale 2, x 40."""
    cv.frame(CX0, 740, COL_W, 36, draw.INK, 1)
    for i, line in enumerate(stories.DATE_CHECK_LINES):
        font.draw_text(cv, line, 40, 744 + i * 16, draw.INK, 2)


def _map_pins():
    """One (block_key, dx, dy, n) per lead/card story."""
    pins = []
    for s in stories.STORIES:
        if s["n"] > 13:
            continue
        block = map.REGION_TO_BLOCK[s["region"]]
        dx, dy = PIN_OFFSETS[s["n"]]
        pins.append((block, dx, dy, s["n"]))
    return pins


def _draw_map_band(cv):
    """B8: titles, schematic map + pins, region counts right column."""
    font.draw_text(cv, "WHERE IT HAPPENED", CX0, 784, draw.INK, 2)
    font.draw_text(cv, "BY REGION", 572, 784, draw.INK, 2)

    map.draw_map(cv, 28, 802, _map_pins())

    counts = map.region_counts(stories.STORIES)
    lines = map.format_region_lines(counts, max_chars=35, max_lines=5)
    for i, line in enumerate(lines):
        font.draw_text(cv, line, 572, 802 + i * 18, draw.INK, 2)


ALSO_COL_XS = [28, 268, 508, 748]
ALSO_ROW_Y0 = 910
ALSO_ROW_STEP = 16


def _draw_also_on(cv):
    """B9: title row + also-on stories n>13, 4 cols x 5 rows filled
    column by column; item = ACCENT number + INK headline, scale 2."""
    font.draw_text(cv, "ALSO ON THURSDAY", CX0, 892, draw.INK, 2)
    also = [s for s in stories.STORIES if s["n"] > 13]
    font.draw_text_right(cv, f"{len(also)} MORE STORIES", CX1, 892,
                         draw.GREY, 2)
    for i, s in enumerate(also):
        col, row = divmod(i, 5)
        if col >= len(ALSO_COL_XS):
            break
        x = ALSO_COL_XS[col]
        y = ALSO_ROW_Y0 + row * ALSO_ROW_STEP
        num = str(s["n"])
        font.draw_text(cv, num, x, y, draw.ACCENT, 2)
        hx = x + font.text_width(num, 2) + 6
        font.draw_text(cv, s["headline"], hx, y, draw.INK, 2)


def _distinct_outlets():
    """Count distinct outlets across all stories (split on ' + ')."""
    seen = []
    for s in stories.STORIES:
        for outlet in s["outlet"].split(" + "):
            if outlet not in seen:
                seen.append(outlet)
    return len(seen)


def _draw_footer(cv):
    """B10: hairline rule + centred colophon, GREY scale 2."""
    cv.rect(CX0, 992, COL_W, 1, draw.INK)
    n_sources = _distinct_outlets()
    colophon = (
        f"COMPILED FROM {n_sources} SOURCES · "
        "ALL DATED 26 NOVEMBER 2026 · THE THURSDAY LEDGER"
    )
    font.draw_text_center(cv, colophon, CX0 + COL_W // 2, 994,
                          draw.GREY, 2)


def draw_bottom(cv):
    """Draw bands B6-B10 (bottom half of the edition) onto cv."""
    _draw_cards(cv)
    _draw_date_check(cv)
    _draw_map_band(cv)
    _draw_also_on(cv)
    _draw_footer(cv)


def main():
    cv = draw.Canvas(1024, 1024)
    cv.frame(10, 10, 1004, 1004, draw.INK, 3)
    draw_top(cv)
    draw_bottom(cv)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    cv.save_png(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
