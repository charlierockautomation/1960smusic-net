# -*- coding: utf-8 -*-
"""Render the Key Facts box (gen/key_facts_data.py) into song and artist pages.

Placement: straight after the intro `<p class="lead">`, before the featured
image, between `<!-- key-facts:start -->` / `<!-- key-facts:end -->`
markers so re-runs replace the box in place. Also adds the required links:
the matching /1960s/<year>/ page, and /best-60s-songs/ when the song is on
that list (read from best-60s-songs/index.html).

Usage: python3 gen/build_key_facts.py [--write]   (dry run without --write)
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from key_facts_data import ARTISTS, SONGS  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
START, END = "<!-- key-facts:start -->", "<!-- key-facts:end -->"


def esc(s):
    return html.escape(s, quote=False)


def on_best_list():
    with open(os.path.join(ROOT, "best-60s-songs", "index.html"), encoding="utf-8") as f:
        return set(re.findall(r'href="/blog/songs/([^"/]+)/"', f.read()))


def box(rows, extra):
    out = [START, '<aside class="key-facts" aria-label="Key facts">',
           '  <p class="key-facts-title">Key Facts</p>', "  <dl>"]
    for label, value in rows:
        out.append(f"    <dt>{esc(label)}</dt><dd>{esc(value)}</dd>")
    for label, value_html in extra:
        out.append(f"    <dt>{esc(label)}</dt><dd>{value_html}</dd>")
    out += ["  </dl>", "</aside>", END]
    return "\n      ".join(out)


def apply(path, new_box):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if START in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: new_box, text, flags=re.S)
    else:
        m = re.search(r'(<p class="lead">.*?</p>)\s*\n(\s*)(<figure class="featured-image">)', text, re.S)
        if not m:
            raise SystemExit(f"no lead + featured-image anchor in {path}")
        text = text[: m.end(1)] + "\n\n      " + new_box + "\n\n" + m.group(2) + m.group(3) + text[m.end(3):]
    return text


def main(write):
    best = on_best_list()
    jobs = []
    for slug, d in SONGS.items():
        extra = [("Year guide", f'<a href="/1960s/{d["year"]}/">{d["year"]} music year guide</a>')]
        if slug in best:
            extra.append(("Playlist", '<a href="/best-60s-songs/">Best 60s Songs</a>, 100 playable hits'))
        jobs.append((f"blog/songs/{slug}/index.html", box(d["rows"], extra)))
    for slug, d in ARTISTS.items():
        links = ", ".join(f'<a href="/1960s/{y}/">{y}</a>' for y in d["years"])
        jobs.append((f"blog/artists/{slug}/index.html", box(d["rows"], [("Key years", links)])))
    for rel, b in jobs:
        p = os.path.join(ROOT, rel)
        new = apply(p, b)
        if write:
            with open(p, "w", encoding="utf-8") as f:
                f.write(new)
    print(f"{'wrote' if write else 'checked'} {len(jobs)} pages")


if __name__ == "__main__":
    main("--write" in sys.argv)
