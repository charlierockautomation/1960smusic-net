#!/usr/bin/env python3
"""Render static <a class="genre-card"> markup into blog listing pages.

Reads data/posts.json and writes crawlable HTML between
<!-- cards:start --> / <!-- cards:end --> markers in:
  blog/index.html (5 sections, one per type, capped at BLOG_INDEX_LIMIT)
  blog/{genres,artists,songs,trending,on-this-day}/index.html (one
  section each, full list for that type)

Also regenerates the CollectionPage/ItemList/BreadcrumbList JSON-LD between
<!-- ld:start --> / <!-- ld:end --> in each listing's head.

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
    "data-page": "Data",
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
ROOT_INDEX_FILE = ROOT / "index.html"
LATEST_OTD_COUNT = 1
LATEST_OTHER_COUNT = 3

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


SITE = "https://1960smusic.net"

# page path -> (name, description) for the CollectionPage block
LISTING_META = {
    "blog": ("Blog: Genre Guides and Stories", "Guides and stories on the music of the 1960s: genre hubs, artists, and the songs that shaped the decade."),
    "blog/genres": ("Genre Hubs", "Every genre hub on 1960smusic.net."),
    "blog/artists": ("Artist Bios", "Every artist profile on 1960smusic.net."),
    "blog/songs": ("Song Stories", "Every song story on 1960smusic.net: the history and context behind the records that defined the 1960s."),
    "blog/on-this-day": ("On This Day", "1960s music milestones, one page per calendar date."),
    "blog/trending": ("Trending", "1960s songs and artists resurging in modern culture."),
}


def listing_ld(rel, posts):
    """CollectionPage + ItemList + BreadcrumbList for a listing page. The
    ItemList is exactly the cards rendered on the page, in page order."""
    name, desc = LISTING_META[rel]
    url = "%s/%s/" % (SITE, rel)
    blocks = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": name, "description": desc, "url": url},
        {"@context": "https://schema.org", "@type": "ItemList", "name": name,
         "itemListElement": [{"@type": "ListItem", "position": i, "name": p["title"], "url": SITE + p["slug"]}
                             for i, p in enumerate(posts, 1)]},
    ]
    crumbs = [("Home", SITE + "/")]
    if rel != "blog":
        crumbs.append(("Blog", SITE + "/blog/"))
    crumbs.append((name if rel != "blog" else "Blog", url))
    blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                   "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": u}
                                       for i, (n, u) in enumerate(crumbs, 1)]})
    return "\n".join('<script type="application/ld+json">\n%s\n</script>' % json.dumps(b, indent=2, ensure_ascii=False).replace("</", "<\\/") for b in blocks)


def inject_ld(html, ld):
    pattern = re.compile(r"<!-- ld:start -->.*?<!-- ld:end -->", re.DOTALL)
    new_html, count = pattern.subn(lambda m: "<!-- ld:start -->\n" + ld + "\n<!-- ld:end -->", html)
    if count != 1:
        raise SystemExit("expected exactly one ld:start/ld:end marker pair, found %d" % count)
    return new_html


def main():
    data = json.loads(POSTS_JSON.read_text())
    posts = data["posts"]
    by_type = {t: sort_posts([p for p in posts if p["type"] == t], t) for t in TYPE_ORDER}

    for post_type, path in ARCHIVE_FILES.items():
        cards = "".join(post_card_html(p) for p in by_type[post_type])
        html = path.read_text()
        html = inject(html, "", cards)
        html = inject_ld(html, listing_ld(str(path.parent.relative_to(ROOT)), by_type[post_type]))
        path.write_text(html)
        print("%s: %d cards" % (path.relative_to(ROOT), len(by_type[post_type])))

    html = BLOG_INDEX_FILE.read_text()
    for post_type in TYPE_ORDER:
        cards = "".join(post_card_html(p) for p in by_type[post_type][:BLOG_INDEX_LIMIT])
        html = inject(html, ":" + post_type, cards)
    shown = [p for pt in TYPE_ORDER for p in by_type[pt][:BLOG_INDEX_LIMIT]]
    html = inject_ld(html, listing_ld("blog", shown))
    BLOG_INDEX_FILE.write_text(html)
    print("%s: updated" % BLOG_INDEX_FILE.relative_to(ROOT))

    latest_otd = by_type["on-this-day"][:LATEST_OTD_COUNT]
    other_posts = sort_posts([p for p in posts if p["type"] != "on-this-day"], "")
    latest_other = other_posts[:LATEST_OTHER_COUNT]
    latest_cards = "".join(post_card_html(p) for p in latest_otd + latest_other)
    html = ROOT_INDEX_FILE.read_text()
    html = inject(html, ":latest", latest_cards)
    ROOT_INDEX_FILE.write_text(html)
    print("%s: updated" % ROOT_INDEX_FILE.relative_to(ROOT))


if __name__ == "__main__":
    main()
