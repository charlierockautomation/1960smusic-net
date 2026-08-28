# -*- coding: utf-8 -*-
"""Generate /llms.txt for 1960smusic.net.

Source of truth for "is this live" is data/posts.json: an entry only
exists there once a page is confirmed live (see CLAUDE.md content
pipeline step 6). This mirrors gen/generate_sitemap.py's approach --
read posts.json + tools.json, don't scan disk (a raw scan would catch
drafts/placeholders that aren't actually published).

Run this any time data/posts.json or data/tools.json changes, same
cadence as generate_sitemap.py. Not currently wired into an automated
build step (no .github/workflows/ in this repo, and Workers Builds runs
no pre-deploy script) -- this is a manual regeneration step, same as
sitemap.xml.

Usage: python3 gen/generate_llms_txt.py
"""
import json
import os

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


def posts_by_type(post_type):
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
