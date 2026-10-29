#!/usr/bin/env python3
"""Render /tools/ (tools/index.html) from data/tools.json.

Writes a card per live tool between <!-- cards:start --> / <!-- cards:end -->
and the CollectionPage + ItemList + BreadcrumbList JSON-LD between
<!-- ld:start --> / <!-- ld:end -->, so the ItemList always equals the cards
linked on the page. Run by publish_prep.py before the sitemap step.
"""
import json
import re
from pathlib import Path

from build_listings import escape_html, inject, inject_ld

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "tools" / "index.html"
SITE = "https://1960smusic.net"
NAME = "Free 1960s Music Tools"
DESC = "Free 1960s music tools: a radio dial, daily guessing game, trivia, crossword, personality quiz, playlist builder and random song generator."


def main():
    tools = [t for t in json.loads((ROOT / "data" / "tools.json").read_text())["tools"] if t.get("status") == "live"]
    cards = "".join(
        '<a class="genre-card" href="%s"><span class="freq">Tool</span><h3>%s</h3><p class="sound">%s</p></a>'
        % (escape_html(t["href"]), escape_html(t["name"]), escape_html(t["blurb"]))
        for t in tools
    )
    url = SITE + "/tools/"
    blocks = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": NAME, "description": DESC, "url": url},
        {"@context": "https://schema.org", "@type": "ItemList", "name": NAME,
         "itemListElement": [{"@type": "ListItem", "position": i, "name": t["name"], "url": SITE + t["href"]}
                             for i, t in enumerate(tools, 1)]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                             {"@type": "ListItem", "position": 2, "name": "Tools", "item": url}]},
    ]
    ld = "\n".join('<script type="application/ld+json">\n%s\n</script>' % json.dumps(b, indent=2, ensure_ascii=False) for b in blocks)
    html = PAGE.read_text()
    html = inject(html, "", cards)
    html = inject_ld(html, ld)
    PAGE.write_text(html)
    print("tools/index.html: %d cards" % len(tools))


if __name__ == "__main__":
    main()
