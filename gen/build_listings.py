#!/usr/bin/env python3
"""Render static <a class="genre-card"> markup into blog listing pages.

Reads data/posts.json and writes crawlable HTML between
<!-- cards:start --> / <!-- cards:end --> markers in:
  blog/index.html (5 sections, one per type, capped at BLOG_INDEX_LIMIT)
  blog/{genres,artists,songs,trending,on-this-day}/index.html (one
  section each, full list for that type)

Mirrors blog/shared.js exactly: same postCardHtml() markup, same
escapeHtml() escaping, same sort (on-this-day by seq desc, else by date
desc). Run after data/posts.json changes, before generate_sitemap.py.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_JSON = ROOT / "data" / "posts.json"
BLOG_INDEX_LIMIT = 6

TYPE_LABELS = {
    "genre-hub": "Genre Hub",
    "artist-bio": "Artist Bio",
    "song-story": "Song Story",
    "trending": "Trending",
    "on-this-day": "On This Day",
}

TYPE_ORDER = ["genre-hub", "artist-bio", "song-story", "trending", "on-this-day"]

ARCHIVE_FILES = {
    "genre-hub": ROOT / "blog" / "genres" / "index.html",
    "artist-bio": ROOT / "blog" / "artists" / "index.html",
    "song-story": ROOT / "blog" / "songs" / "index.html",
    "trending": ROOT / "blog" / "trending" / "index.html",
    "on-this-day": ROOT / "blog" / "on-this-day" / "index.html",
}

BLOG_INDEX_FILE = ROOT / "blog" / "index.html"

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def escape_html(s):
    return (
        str(s if s is not None else "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def format_date(iso):
    y, m, d = iso.split("-")
    return "%s %d, %s" % (_MONTHS[int(m) - 1], int(d), y)


def by_date_desc(post):
    return post["date"]


def by_otd_desc(post):
    return post.get("seq", -1)


def sort_posts(posts, post_type):
    if post_type == "on-this-day":
        return sorted(posts, key=by_otd_desc, reverse=True)
    return sorted(posts, key=by_date_desc, reverse=True)


def post_card_html(post):
    label = TYPE_LABELS.get(post["type"], post["type"])
    return (
        '<a class="genre-card" href="' + escape_html(post["slug"]) + '">'
        + '<span class="freq">' + escape_html(label) + " &middot; " + escape_html(format_date(post["date"])) + "</span>"
        + "<h3>" + escape_html(post["title"]) + "</h3>"
        + '<p class="sound">' + escape_html(post["description"]) + "</p>"
        + "</a>"
    )


def inject(html, suffix, cards_html):
    start = "<!-- cards:start%s -->" % suffix
    end = "<!-- cards:end%s -->" % suffix
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = start + "\n" + cards_html + "\n" + end
    new_html, count = pattern.subn(replacement, html)
    if count != 1:
        raise SystemExit("expected exactly one %s ... %s marker pair, found %d" % (start, end, count))
    return new_html


def main():
    data = json.loads(POSTS_JSON.read_text())
    posts = data["posts"]
    by_type = {t: sort_posts([p for p in posts if p["type"] == t], t) for t in TYPE_ORDER}

    for post_type, path in ARCHIVE_FILES.items():
        cards = "".join(post_card_html(p) for p in by_type[post_type])
        html = path.read_text()
        html = inject(html, "", cards)
        path.write_text(html)
        print("%s: %d cards" % (path.relative_to(ROOT), len(by_type[post_type])))

    html = BLOG_INDEX_FILE.read_text()
    for post_type in TYPE_ORDER:
        cards = "".join(post_card_html(p) for p in by_type[post_type][:BLOG_INDEX_LIMIT])
        html = inject(html, ":" + post_type, cards)
    BLOG_INDEX_FILE.write_text(html)
    print("%s: updated" % BLOG_INDEX_FILE.relative_to(ROOT))


if __name__ == "__main__":
    main()
