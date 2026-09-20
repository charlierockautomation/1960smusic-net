# -*- coding: utf-8 -*-
"""Generates docs/daily-thumbnail-review.html: a local-only grid of every
kept Daily Guessing Game pool thumbnail (title, id, accepted year(s)) for
Charlie to eyeball for on-screen artwork/text that reveals the year. Not
part of the automated gate (no OCR available) and not deployed -- listed in
.assetsignore.

Run after gen/daily_pool_check.py so it reflects the current excluded set.

Usage: python3 gen/daily_thumbnail_review.py
"""
import json, os, glob, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "docs", "daily-thumbnail-review.html")


def load_pool():
    out = []
    for path in glob.glob(os.path.join(DATA, "radio-eligible-*.json")):
        out.extend(json.load(open(path)))
    return out


def accepted_years(song):
    years = [song.get("year")]
    if song.get("year_alt") is not None:
        years.append(song["year_alt"])
    return [y for y in years if y is not None]


def card(song):
    vid = song["youtube_id"]
    years = "/".join(str(y) for y in accepted_years(song))
    return (
        '<div class="card">'
        '<img loading="lazy" src="https://img.youtube.com/vi/%s/hqdefault.jpg" alt="">'
        '<p class="t">%s</p>'
        '<p class="a">%s &middot; %s</p>'
        '<p class="id">%s</p>'
        "</div>"
    ) % (vid, html.escape(song["title"]), html.escape(song["artist"]), years, vid)


def main():
    excluded_path = os.path.join(DATA, "daily-excluded-ids.json")
    excluded = json.load(open(excluded_path)) if os.path.exists(excluded_path) else {}
    pool = [s for s in load_pool() if s["youtube_id"] not in excluded]

    cards = "\n".join(card(s) for s in pool)
    page = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Daily thumbnail review (local only, not deployed)</title>
<style>
body{font-family:sans-serif;background:#222;color:#eee;margin:0;padding:20px;}
h1{font-size:1.1rem;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;}
.card{background:#333;border-radius:8px;padding:8px;font-size:.8rem;}
.card img{width:100%%;border-radius:4px;display:block;}
.t{font-weight:700;margin:6px 0 2px;}
.a{color:#bbb;margin:0 0 2px;}
.id{color:#888;font-family:monospace;margin:0;}
</style></head><body>
<h1>%d thumbnails to eyeball for on-screen year text/artwork. Not deployed.</h1>
<div class="grid">
%s
</div>
</body></html>
""" % (len(pool), cards)
    open(OUT, "w", encoding="utf-8").write(page)
    print("Wrote %d cards to %s" % (len(pool), OUT))


if __name__ == "__main__":
    main()
