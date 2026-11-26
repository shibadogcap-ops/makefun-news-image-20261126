"""Story data for the 26 November 2026 news-image edition.

Thin day: only 10 stories were verifiable as genuinely dated
26 November 2026 (US Thanksgiving). Every candidate verified as a
23-25 November event is excluded and recorded in EXCLUSIONS for the
date-check strip. 3 leads + 7 cards + 0 also-on = 10 stories.

All strings are ALL CAPS, stored pre-wrapped to the line budgets in
DESIGN-SPEC section 7, and use only drawable characters.
"""

STORIES = [
    # ---- Lead A (n=1) ----
    {
        "n": 1,
        "region": "MIDDLE EAST",
        "field": "CONFLICT",
        "headline": ["MISSILES", "OVER RIYADH"],
        "body": [
            "SAUDI DEFENCES DOWN TWO",
            "HOUTHI MISSILES OVER RIYADH",
            "ON A THIRD NIGHT OF ALERTS",
        ],
        "outlet": "TIMES NOW + ANADOLU",
        "status": "CONFIRMED",
        "hour_utc": 0,
        "pin": "ASIA",
        "number_story": False,
    },
    # ---- Lead B (n=2) ----
    {
        "n": 2,
        "region": "ASIA-PACIFIC",
        "field": "POLITICS",
        "headline": ["KIM NUKE CALL"],
        "body": [
            "KIM CALLS TO DIVERSIFY",
            "TACTICAL NUCLEAR ARMS",
        ],
        "outlet": "KCNA + REUTERS",
        "status": "CONFIRMED",
        "hour_utc": 1,
        "pin": "ASIA",
        "number_story": False,
    },
    # ---- Lead C (n=3) ----
    {
        "n": 3,
        "region": "N AMERICA",
        "field": "CLIMATE",
        "headline": ["STORM HITS EAST"],
        "body": [
            "70 MPH GUSTS AND FLOODS",
            "BATTER THE EAST COAST",
        ],
        "outlet": "NWS + WEATHER.COM",
        "status": "CONFIRMED",
        "hour_utc": 17,
        "pin": "N AMERICA",
        "number_story": True,
    },
    # ---- Cards (n=4..10) ----
    {
        "n": 4,
        "region": "ASIA-PACIFIC",
        "field": "CULTURE",
        "headline": ["TAI PO", "REMEMBERS"],
        "summary": "168 DEAD A YEAR",
        "outlet": "SCMP + REUTERS",
        "status": "CONFIRMED",
        "hour_utc": None,
        "pin": "ASIA",
        "number_story": True,
    },
    {
        "n": 5,
        "region": "N AMERICA",
        "field": "CLIMATE",
        "headline": ["KING TIDES", "HIT COAST"],
        "summary": "TIDES 2.4 FT UP",
        "outlet": "NWS + USA TODAY",
        "status": "CONFIRMED",
        "hour_utc": 19,
        "pin": "N AMERICA",
        "number_story": True,
    },
    {
        "n": 6,
        "region": "N AMERICA",
        "field": "SOCIETY",
        "headline": ["AIRPORT", "CHAOS"],
        "summary": "HOLIDAY CROWDS",
        "outlet": "AP + NWS",
        "status": "CONFIRMED",
        "hour_utc": None,
        "pin": "N AMERICA",
        "number_story": False,
    },
    {
        "n": 7,
        "region": "EUROPE",
        "field": "POLITICS",
        "headline": ["UK-EU BILL"],
        "summary": ["DEAL BEFORE MPS", "TODAY"],
        "outlet": "AFP + MANILA TIMES",
        "status": "CONFIRMED",
        "hour_utc": None,
        "pin": "EUROPE",
        "number_story": False,
    },
    {
        "n": 8,
        "region": "ASIA-PACIFIC",
        "field": "ECONOMY",
        "headline": ["STOCKS UP", "IN ASIA"],
        "summary": "NIKKEI +1.95%",
        "outlet": "CNBC TV18 + BLOOMBERG",
        "status": "CONFIRMED",
        "hour_utc": 6,
        "pin": "ASIA",
        "number_story": True,
    },
    {
        "n": 9,
        "region": "ASIA-PACIFIC",
        "field": "CULTURE",
        "headline": ["INDIA DAY"],
        "summary": ["CONSTITUTION", "ADOPTED IN 1949"],
        "outlet": "SELFSTUDYS",
        "status": "REPORTED",
        "hour_utc": None,
        "pin": "ASIA",
        "number_story": False,
    },
    {
        "n": 10,
        "region": "ASIA-PACIFIC",
        "field": "ECONOMY",
        "headline": ["MIZUHO", "AVENDUS"],
        "summary": "510M DEAL DONE",
        "outlet": "BLOOMBERG + ET",
        "status": "CONFIRMED",
        "hour_utc": None,
        "pin": "ASIA",
        "number_story": True,
    },
]

# Numbers band: 5 big-number callouts, each tied to a number_story.
NUMBERS = [
    {"value": "168", "label": "TAI PO FIRE DEAD", "story_n": 4},
    {"value": "70 MPH", "label": "STORM GUSTS", "story_n": 3},
    {"value": "58,125", "label": "NIKKEI CLOSE", "story_n": 8},
    {"value": "510M", "label": "MIZUHO DEAL", "story_n": 10},
    {"value": "2.4 FT", "label": "KING TIDE SURGE", "story_n": 5},
]

# Candidates excluded from this edition's date scope (23-25 Nov),
# recorded for the date-check strip.
EXCLUSIONS = [
    "TARIFFS 25 NOV",
    "COLOMBIA 25 NOV",
    "ABREGO 25 NOV",
    "AUSTRALIA PACT 25 NOV",
]

# Pre-composed date-check strip lines (two lines, each <=78 chars).
DATE_CHECK_LINES = [
    "DATE CHECK - NOT IN: TARIFFS 25 NOV, COLOMBIA 25 NOV, ABREGO 25 NOV",
    "AUSTRALIA PACT 25 NOV - EVERYTHING ELSE HAPPENED ON 26 NOVEMBER 2026.",
]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

PIN_KEYS = {"ASIA", "N AMERICA", "EUROPE", "AFRICA", "S AMERICA",
            "SE-ASIA", "OCEANIA"}
STATUSES = {"CONFIRMED", "REPORTED", "DEVELOPING"}
DRAWABLE_CHARS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    " # % & + , - . / : ·"
)
REQUIRED_KEYS = {"n", "region", "field", "headline", "outlet", "status",
                 "hour_utc", "pin", "number_story"}


def _is_drawable(text):
    return all(c in DRAWABLE_CHARS for c in text)


def _check_drawable(text, where):
    if not _is_drawable(text):
        bad = sorted({c for c in text if c not in DRAWABLE_CHARS})
        raise AssertionError(
            f"{where}: non-drawable characters {bad} in {text!r}")


def _check_allcaps(text, where):
    for ch in text:
        if ch.islower():
            raise AssertionError(f"{where}: lowercase character {ch!r} in {text!r}")


def _check_lines(lines, where, max_len, exact=None):
    if not isinstance(lines, list) or not lines:
        raise AssertionError(f"{where}: expected a non-empty list of lines")
    if exact is not None and len(lines) != exact:
        raise AssertionError(
            f"{where}: expected exactly {exact} lines, got {len(lines)}")
    for i, line in enumerate(lines):
        if not isinstance(line, str) or not line:
            raise AssertionError(f"{where}[{i}]: line must be a non-empty string")
        if len(line) > max_len:
            raise AssertionError(
                f"{where}[{i}]: {len(line)} chars exceeds budget {max_len}: {line!r}")
        _check_allcaps(line, f"{where}[{i}]")
        _check_drawable(line, f"{where}[{i}]")


def validate():
    # --- story count / roles ---
    if len(STORIES) != 10:
        raise AssertionError(f"STORIES must contain exactly 10 stories, got {len(STORIES)}")

    leads = [s for s in STORIES if s["n"] <= 3]
    cards = [s for s in STORIES if 4 <= s["n"] <= 10]
    if len(leads) != 3 or len(cards) != 7:
        raise AssertionError(
            f"expected 3 leads (n 1-3) and 7 cards (n 4-10), "
            f"got {len(leads)} leads and {len(cards)} cards")

    # --- story numbers in drawn order, no gaps/dupes ---
    ns = [s["n"] for s in STORIES]
    if ns != list(range(1, 11)):
        raise AssertionError(f"story numbers must be 1..10 in drawn order, got {ns}")

    by_n = {s["n"]: s for s in STORIES}

    for s in STORIES:
        where = f"story {s.get('n')}"
        missing = REQUIRED_KEYS - s.keys()
        if missing:
            raise AssertionError(f"{where}: missing keys {sorted(missing)}")

        # headline budgets: lead A 2 lines x <=12, lead B/C 1 line x <=15,
        # card Variant A 2 lines x <=10, card Variant B 1 line x <=10
        h = s["headline"]
        if s["n"] == 1:
            _check_lines(h, f"{where} headline", 12, exact=2)
        elif s["n"] in (2, 3):
            _check_lines(h, f"{where} headline", 15, exact=1)
        elif s["n"] in (4, 5, 6, 8, 10):  # card Variant A
            _check_lines(h, f"{where} headline", 10, exact=2)
        else:  # card Variant B
            _check_lines(h, f"{where} headline", 10, exact=1)

        if s["n"] == 1:
            if "body" not in s:
                raise AssertionError(f"{where}: lead A must have body")
            _check_lines(s["body"], f"{where} body", 33, exact=3)
        elif s["n"] in (2, 3):
            if "body" not in s:
                raise AssertionError(f"{where}: lead must have body")
            _check_lines(s["body"], f"{where} body", 26, exact=2)
        else:
            if "summary" not in s:
                raise AssertionError(f"{where}: card must have summary")
            summ = s["summary"]
            # Variant A: 1 line <=15; Variant B: 2 lines x <=15
            if s["n"] in (4, 5, 6, 8, 10):
                if not isinstance(summ, str):
                    raise AssertionError(f"{where}: card Variant A summary must be a string")
                _check_lines([summ], f"{where} summary", 15, exact=1)
            else:
                _check_lines(summ, f"{where} summary", 15, exact=2)

        # scalar fields
        if not s["outlet"] or not isinstance(s["outlet"], str):
            raise AssertionError(f"{where}: outlet must be a non-empty string")
        _check_allcaps(s["outlet"], f"{where} outlet")
        _check_drawable(s["outlet"], f"{where} outlet")
        if s["status"] not in STATUSES:
            raise AssertionError(
                f"{where}: status must be one of {sorted(STATUSES)}, got {s['status']!r}")
        hu = s["hour_utc"]
        if hu is not None and (not isinstance(hu, int) or isinstance(hu, bool)
                               or not 0 <= hu <= 23):
            raise AssertionError(f"{where}: hour_utc must be int 0-23 or None, got {hu!r}")
        if s["pin"] is not None and s["pin"] not in PIN_KEYS:
            raise AssertionError(f"{where}: pin must be a map block key or None, got {s['pin']!r}")
        if not isinstance(s["number_story"], bool):
            raise AssertionError(f"{where}: number_story must be a bool")
        if not isinstance(s["region"], str) or not s["region"]:
            raise AssertionError(f"{where}: region must be a non-empty string")
        if not isinstance(s["field"], str) or not s["field"]:
            raise AssertionError(f"{where}: field must be a non-empty string")

    # --- also-on must be absent (0 also-on stories) ---
    for s in STORIES:
        if s["n"] > 10 or s.get("kind") == "also_on":
            raise AssertionError(f"story {s['n']}: no also-on stories allowed")

    # --- NUMBERS ---
    if len(NUMBERS) != 5:
        raise AssertionError(f"NUMBERS must contain exactly 5 entries, got {len(NUMBERS)}")
    for i, num in enumerate(NUMBERS):
        w = f"NUMBERS[{i}]"
        if set(num.keys()) != {"value", "label", "story_n"}:
            raise AssertionError(f"{w}: keys must be exactly value/label/story_n")
        if len(num["value"]) > 8:
            raise AssertionError(f"{w}: value exceeds 8 chars: {num['value']!r}")
        if len(num["label"]) > 16:
            raise AssertionError(f"{w}: label exceeds 16 chars: {num['label']!r}")
        _check_allcaps(num["label"], f"{w} label")
        _check_drawable(num["value"], f"{w} value")
        _check_drawable(num["label"], f"{w} label")
        sn = num["story_n"]
        if sn not in by_n:
            raise AssertionError(f"{w}: story_n {sn} does not refer to a story")
        if not by_n[sn]["number_story"]:
            raise AssertionError(
                f"{w}: story_n {sn} refers to a story with number_story False")

    # --- DATE_CHECK_LINES ---
    if len(DATE_CHECK_LINES) != 2:
        raise AssertionError("DATE_CHECK_LINES must contain exactly 2 lines")
    for i, line in enumerate(DATE_CHECK_LINES):
        w = f"DATE_CHECK_LINES[{i}]"
        if len(line) > 78:
            raise AssertionError(f"{w}: {len(line)} chars exceeds 78")
        _check_allcaps(line, w)
        _check_drawable(line, w)


if __name__ == "__main__":
    validate()
    print("validate OK")
