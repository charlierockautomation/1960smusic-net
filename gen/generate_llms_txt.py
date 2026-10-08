# -*- coding: utf-8 -*-
"""Generate /llms.txt for 1960smusic.net.

Source of truth for "is this live" is data/posts.json: an entry only
exists there once a page is confirmed live (see CLAUDE.md content
pipeline step 6). This mirrors gen/generate_sitemap.py's approach --
read posts.json + tools.json, don't scan disk (a raw scan would catch
drafts/placeholders that aren't actually published).

Also lists the static guide pages (/1960s/ hub + the ten year pages,
/best-60s-songs/, the author page), read straight from each page's own
<title> and meta description so the entries never drift from the page.

Run via gen/publish_prep.py (CLAUDE.md pipeline step 6), after posts.json
changes, alongside generate_sitemap.py. Workers Builds runs no pre-deploy
script, so "automatic" means: one command in the publish step, enforced by
gen/check_article.py (a live page missing from llms.txt FAILs).

Usage: python3 gen/generate_llms_txt.py
"""
import html
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = "https://1960smusic.net"
TITLE = "1960s Music"
TAGLINE = (
    "Tune in to 1960s music: eight genre stations from British Invasion "
    "to Motown, hundreds of essential songs, and free interactive tools "
    "you can play now."
)
CAP = 200

SECTIONS = [
    ("Tools", None),
    ("Year Guides", "year-guide"),
    ("Best 60s Songs", "best-songs"),
    ("About the Author", "author"),
    ("Genre Hubs", "genre-hub"),
    ("Artists", "artist-bio"),
    ("Songs", "song-story"),
    ("On This Day", "on-this-day"),
    ("Trending", "trending"),
]


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


def live_tools():
    tools = load("tools.json")["tools"]
    return [t for t in tools if t.get("status") == "live"]


def page_entry(path):
    """{'title','slug','description'} read from a static page's own head."""
    rel = path.strip("/")
    with open(os.path.join(ROOT, rel, "index.html"), encoding="utf-8") as f:
        head = f.read()[:8000]
    title = html.unescape(re.search(r"<title>(.*?)</title>", head, re.S).group(1))
    title = re.sub(r"\s*\|\s*1960smusic\.net$", "", title).strip()
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', head).group(1))
    return {"title": title, "slug": path, "description": desc}


def static_pages(kind):
    if kind == "year-guide":
        paths = ["/1960s/"] + [f"/1960s/{y}/" for y in range(1960, 1970)]
    elif kind == "best-songs":
        paths = ["/best-60s-songs/"]
    else:
        paths = ["/about/charlie/"]
    return [page_entry(p) for p in paths if os.path.exists(os.path.join(ROOT, p.strip("/"), "index.html"))]


def posts_by_type(post_type):
    if post_type in ("year-guide", "best-songs", "author"):
        return static_pages(post_type)
    posts = load("posts.json")["posts"]
    matched = [p for p in posts if p["type"] == post_type]
    # newest first
    matched.sort(key=lambda p: p.get("date", ""), reverse=True)
    return matched


def cap_sections(sections):
    """Cap total entries at CAP, trimming oldest-first within whichever
    section is currently largest, repeating until under cap."""
    total = sum(len(entries) for _, entries in sections)
    while total > CAP:
        biggest_idx = max(
            range(len(sections)), key=lambda i: len(sections[i][1])
        )
        name, entries = sections[biggest_idx]
        entries.pop()  # entries are newest-first, so pop() drops oldest
        sections[biggest_idx] = (name, entries)
        total -= 1
    return sections


def render(sections, tool_entries):
    lines = [f"# {TITLE}", "", TAGLINE, "", f"Sitemap: {BASE}/sitemap.xml", ""]

    for name, entries in sections:
        if not entries:
            continue
        lines.append(f"## {name}")
        if name == "Tools":
            for t in entries:
                lines.append(f"- [{t['name']}]({BASE}{t['href']}): {t['blurb']}")
        else:
            for p in entries:
                lines.append(f"- [{p['title']}]({BASE}{p['slug']}): {p['description']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    sections = []
    for name, post_type in SECTIONS:
        if post_type is None:
            sections.append((name, live_tools()))
        else:
            sections.append((name, posts_by_type(post_type)))

    sections = cap_sections(sections)

    text = render(sections, None)
    out_path = os.path.join(ROOT, "llms.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    counts = ", ".join(f"{name}={len(entries)}" for name, entries in sections)
    print(f"Wrote {out_path} ({counts})")


if __name__ == "__main__":
    main()
