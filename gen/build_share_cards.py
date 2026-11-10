# -*- coding: utf-8 -*-
"""Branded 1200x630 share cards (og:image / Article image), self-hosted.

Two uses (Task 5, 2026-11-10):
  - On This Day fallback (rule b in docs/on-this-day-page-template.html):
    a date card for an OTD page that has no self-hosted photo or cover of
    its own. Written to blog/on-this-day/<slug>/og-card.png.
  - Tool pages: tools/<slug>/og-card.png, one per tool in TOOLS below.

Same palette and type as assets/og-home.png. Cards are committed PNGs; the
fonts only need to exist on the machine that runs this script.

Usage: python3 gen/build_share_cards.py otd <slug> [<slug> ...]
       python3 gen/build_share_cards.py tools
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BG, GOLD, CREAM = (61, 43, 31), (184, 137, 74), (239, 227, 207)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
W, H = 1200, 630

TOOLS = {
    "radio": ("Radio Dial", "Eight 1960s genre stations, one dial"),
    "daily": ("Daily Guessing Game", "Watch the video, guess the year"),
    "trivia": ("1960s Music Trivia", "Ten questions from the decade's hits"),
    "quiz": ("What's Your 60s Sound?", "A personality quiz: find your 1960s genre"),
    "playlist-builder": ("Party Playlist Builder", "Pick a vibe, play a 1960s set"),
    "random-song": ("Random 60s Song Generator", "Spin up a track from any of eight genres"),
    "60s-music-crossword": ("60s Music Crossword", "Solve clues from the decade's music"),
}


def _fit(draw, text, path, start, max_w):
    size = start
    while size > 30:
        font = ImageFont.truetype(path, size)
        if draw.textlength(text, font=font) <= max_w:
            return font
        size -= 4
    return ImageFont.truetype(path, size)


def card(kicker, title, sub, out):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([30, 30, W - 31, H - 31], outline=GOLD, width=5)
    d.rectangle([44, 44, W - 45, H - 45], outline=GOLD, width=1)
    k = ImageFont.truetype(SERIF, 38)
    d.text((W / 2, 150), kicker, font=k, fill=GOLD, anchor="mm")
    t = _fit(d, title, SERIF_BOLD, 120, W - 160)
    d.text((W / 2, 275), title, font=t, fill=CREAM, anchor="mm")
    d.line([300, 365, W - 300, 365], fill=GOLD, width=3)
    s = _fit(d, sub, SERIF, 40, W - 160)
    d.text((W / 2, 430), sub, font=s, fill=CREAM, anchor="mm")
    b = ImageFont.truetype(SERIF_BOLD, 34)
    d.text((W / 2, 530), "1960smusic.net", font=b, fill=GOLD, anchor="mm")
    im.save(out, optimize=True)
    return out


def otd(slug):
    month, day = slug.rsplit("-", 1)
    title = f"{month.capitalize()} {int(day)}"
    out = os.path.join(ROOT, "blog", "on-this-day", slug, "og-card.png")
    return card("On This Day in 1960s Music", title, "Releases, sessions, No. 1s and milestones, 1960-1969", out)


def tools():
    outs = []
    for slug, (name, sub) in TOOLS.items():
        outs.append(card("Free 1960s Music Tool", name, sub, os.path.join(ROOT, "tools", slug, "og-card.png")))
    return outs


if __name__ == "__main__":
    if sys.argv[1:2] == ["tools"]:
        for o in tools():
            print("wrote", os.path.relpath(o, ROOT))
    elif sys.argv[1:2] == ["otd"]:
        for s in sys.argv[2:]:
            print("wrote", os.path.relpath(otd(s), ROOT))
    else:
        print(__doc__)
        sys.exit(2)
