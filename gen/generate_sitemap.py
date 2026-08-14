# -*- coding: utf-8 -*-
"""Generate /sitemap.xml for 1960smusic.net.

Combines a fixed list of static pages with every live tool (from
data/tools.json) and every published article (from data/posts.json).

Run this any time data/posts.json changes -- adding a new article's
entry there and forgetting to regenerate the sitemap means the new page
won't be discovered from the sitemap until the next run. This is step 4
of "once live" in CLAUDE.md's content pipeline section (content-build.md,
posts.json, link-map.md, sitemap.xml).

Usage: python3 gen/generate_sitemap.py
"""
import json
import os
from datetime import date, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = "https://1960smusic.net"
TODAY = date.today().isoformat()

# path -> (changefreq, priority). Trailing slash matches the site's own
# link convention (see CLAUDE.md: root-relative links).
STATIC_PAGES = {
    "/": ("weekly", "1.0"),
    "/about.html": ("monthly", "0.5"),
    "/contact.html": ("monthly", "0.3"),
    "/privacy-policy.html": ("yearly", "0.2"),
    "/terms-of-use.html": ("yearly", "0.2"),
    "/blog/": ("weekly", "0.9"),
    "/blog/genres/": ("weekly", "0.7"),
    "/blog/artists/": ("weekly", "0.7"),
    "/blog/songs/": ("weekly", "0.7"),
    "/blog/trending/": ("weekly", "0.6"),
    "/blog/on-this-day/": ("weekly", "0.6"),
}


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


def build_urls():
    urls = {}  # loc -> (lastmod, changefreq, priority)

    for path, (freq, pri) in STATIC_PAGES.items():
        urls[path] = (TODAY, freq, pri)

    tools = load("tools.json")["tools"]
    for t in tools:
        if t.get("status") == "live":
            urls[t["href"]] = (TODAY, "monthly", "0.6")

    posts = load("posts.json")["posts"]
    archive_by_type = {}
    for p in posts:
        lastmod = p.get("date") or TODAY
        urls[p["slug"]] = (lastmod, "monthly", "0.8")
        arch = {
            "genre-hub": "/blog/genres/",
            "artist-bio": "/blog/artists/",
            "song-story": "/blog/songs/",
            "trending": "/blog/trending/",
            "on-this-day": "/blog/on-this-day/",
        }.get(p["type"])
        if arch:
            prev = archive_by_type.get(arch)
            if not prev or lastmod > prev:
                archive_by_type[arch] = lastmod

    # bump archive-page lastmod to the newest post in that category
    for arch_path, lastmod in archive_by_type.items():
        old = urls.get(arch_path)
        if old:
            urls[arch_path] = (max(lastmod, old[0]), old[1], old[2])

    return urls


def render(urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc in sorted(urls):
        lastmod, freq, pri = urls[loc]
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE}{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    urls = build_urls()
    xml = render(urls)
    out_path = os.path.join(ROOT, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Wrote {out_path} with {len(urls)} URLs.")


if __name__ == "__main__":
    main()
