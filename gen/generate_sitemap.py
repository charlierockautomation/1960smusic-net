# -*- coding: utf-8 -*-
"""Generate /sitemap.xml for 1960smusic.net.

Every live page is discovered from disk: any `index.html` under the site
root (plus `index.html` itself), minus gen/docs/worker/assets and any page
marked noindex or carrying a `<!-- DRAFT -->` comment. Drafts that are not
yet approved for push must be marked DRAFT or kept out of the tree, because
this script cannot tell an unpushed page from a live one.

URLs are the canonical form every page's own <link rel="canonical"> uses:
extensionless with a trailing slash. A page whose canonical tag disagrees
with its path is reported and the canonical value wins.

lastmod is the page's real last-modified date:
  1. Article JSON-LD `dateModified` when the page has one (content date).
  2. else the date of the last git commit touching the file (today if the
     file has uncommitted changes).
  3. else the file's mtime.

Run via gen/publish_prep.py (CLAUDE.md pipeline step 6), after
build_listings.py. Usage: python3 gen/generate_sitemap.py
"""
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = "https://1960smusic.net"
TODAY = date.today().isoformat()

SKIP_DIRS = {"gen", "docs", "worker", "assets", ".git", ".serena", "node_modules", "data"}

# (path prefix or exact path) -> (changefreq, priority); first match wins.
RULES = [
    ("/", ("weekly", "1.0")),
    ("/blog/", ("weekly", "0.9")),
    ("/1960s/", ("weekly", "0.7")),
    ("/best-60s-songs/", ("monthly", "0.8")),
    ("/blog/genres/", ("weekly", "0.7")),
    ("/blog/artists/", ("weekly", "0.7")),
    ("/blog/songs/", ("weekly", "0.7")),
    ("/blog/trending/", ("weekly", "0.6")),
    ("/blog/on-this-day/", ("weekly", "0.6")),
    ("/about/", ("monthly", "0.5")),
    ("/contact/", ("monthly", "0.3")),
    ("/privacy-policy/", ("yearly", "0.2")),
    ("/terms-of-use/", ("yearly", "0.2")),
    ("/tools/", ("monthly", "0.6")),
]
EXACT = {"/", "/blog/", "/1960s/", "/best-60s-songs/", "/blog/genres/",
         "/blog/artists/", "/blog/songs/", "/blog/trending/",
         "/blog/on-this-day/", "/about/", "/contact/", "/privacy-policy/",
         "/terms-of-use/"}


def freq_pri(loc):
    if loc in EXACT:
        for key, val in RULES:
            if key == loc:
                return val
    if re.match(r"^/1960s/\d{4}/$", loc):
        return ("monthly", "0.7")
    if loc.startswith("/blog/"):
        return ("monthly", "0.8")  # individual posts
    if loc.startswith("/tools/"):
        return ("monthly", "0.6")
    if loc.startswith("/about/"):
        return ("monthly", "0.5")
    return ("monthly", "0.5")


def git_date(rel):
    try:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", rel],
                               cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if dirty:
            return TODAY
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                             cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return out or None
    except OSError:
        return None


def lastmod_for(rel, text):
    m = re.search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})"', text)
    if m:
        return m.group(1)
    g = git_date(rel)
    if g:
        return g
    return datetime.fromtimestamp(os.path.getmtime(os.path.join(ROOT, rel))).date().isoformat()


def discover():
    """Yield (rel_file, path, text) for every indexable index.html."""
    for dirpath, dirs, files in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        top = rel_dir.split(os.sep)[0]
        if top in SKIP_DIRS:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if not (rel_dir == "." and d in SKIP_DIRS)]
        if "index.html" not in files:
            continue
        rel = os.path.normpath(os.path.join(rel_dir, "index.html"))
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            text = f.read()
        path = "/" if rel == "index.html" else "/" + rel[: -len("index.html")]
        yield rel, path, text


def build_urls():
    urls = {}
    for rel, path, text in discover():
        head = text[:6000]
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', head, re.I) or "<!-- DRAFT" in text:
            continue
        m = re.search(r'<link rel="canonical" href="https://1960smusic\.net([^"]*)"', head)
        loc = m.group(1) if m else path
        if m and loc != path:
            print(f"  NOTE: {rel} canonical {loc} differs from path {path}; using canonical", file=sys.stderr)
        freq, pri = freq_pri(loc)
        urls[loc] = (lastmod_for(rel, text), freq, pri)
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
    out_path = os.path.join(ROOT, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render(urls))
    print(f"Wrote {out_path} with {len(urls)} URLs.")


if __name__ == "__main__":
    main()
