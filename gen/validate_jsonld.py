# -*- coding: utf-8 -*-
"""Local JSON-LD validator (no network): parses every ld+json block on a page
and checks the properties Google's rich-result docs require/recommend for the
types this site uses, plus cross-checks against the visible page.

Usage: python3 gen/validate_jsonld.py <index.html> [...]
       python3 gen/validate_jsonld.py --all      (every index.html on the site)
Exit 1 if any ERROR. WARN = recommended property missing / soft mismatch.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATE = re.compile(r"^\d{4}(-\d{2}-\d{2})?$")
URL = re.compile(r"^https://1960smusic\.net/")


def blocks(text):
    out = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S | re.I):
        out.append(raw)
    return out


def need(node, keys, where, errs):
    for k in keys:
        v = node.get(k)
        if v in (None, "", [], {}):
            errs.append(f"{where}: missing required {k}")


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def validate(path):
    errs, warns = [], []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rel = os.path.relpath(os.path.abspath(path), ROOT).replace(os.sep, "/")
    url = "/" if rel == "index.html" else "/" + rel[: -len("index.html")]
    nodes = []
    for i, raw in enumerate(blocks(text)):
        try:
            d = json.loads(raw)
        except ValueError as e:
            errs.append(f"block {i + 1} is not valid JSON: {e}")
            continue
        if isinstance(d, dict) and "@graph" in d:
            for g in d["@graph"]:
                g.setdefault("@context", d.get("@context"))
                nodes.append(g)
        else:
            nodes.append(d)
    types = []
    for n in nodes:
        if not isinstance(n, dict):
            errs.append("top-level JSON-LD node is not an object")
            continue
        if n.get("@context") != "https://schema.org":
            errs.append(f"{n.get('@type')}: @context is not https://schema.org")
        t = n.get("@type")
        types.append(t)
        w = str(t)
        if t == "Article":
            need(n, ["headline", "image", "author", "datePublished", "dateModified", "publisher", "mainEntityOfPage"], w, errs)
            if len(n.get("headline", "")) > 110:
                warns.append("Article headline over 110 chars (Google truncates)")
            for k in ("datePublished", "dateModified"):
                if n.get(k) and not DATE.match(n[k]):
                    errs.append(f"Article {k} {n[k]!r} is not ISO 8601")
            if n.get("dateModified", "") < n.get("datePublished", ""):
                errs.append("Article dateModified earlier than datePublished")
            a = n.get("author") or {}
            if a.get("@type") not in ("Person", "Organization") or not a.get("name"):
                errs.append("Article author needs @type Person/Organization and name")
            elif not a.get("url"):
                warns.append("Article author has no url")
            pub = n.get("publisher") or {}
            if not pub.get("name") or not (pub.get("logo") or {}).get("url"):
                errs.append("Article publisher needs name and logo.url")
            if n.get("image") and not str(n["image"]).startswith("https://"):
                errs.append("Article image is not an absolute https URL")
            mep = (n.get("mainEntityOfPage") or {}).get("@id", "")
            if mep != "https://1960smusic.net" + url:
                errs.append(f"Article mainEntityOfPage {mep} != page URL {url}")
            mod = re.search(r'Updated\s*<time datetime="([^"]+)"', text)
            if mod and mod.group(1) != n.get("dateModified"):
                errs.append("visible Updated date != dateModified")
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.S)
            if h1 and plain(h1.group(1)) != plain(n.get("headline", "")):
                warns.append(f"headline {n.get('headline')!r} differs from visible H1 {plain(h1.group(1))!r}")
        elif t == "FAQPage":
            qs = n.get("mainEntity") or []
            if not qs:
                errs.append("FAQPage has no mainEntity questions")
            visible = plain(text)
            for q in qs:
                if q.get("@type") != "Question" or not q.get("name"):
                    errs.append("FAQ item is not a Question with a name")
                    continue
                ans = (q.get("acceptedAnswer") or {})
                if ans.get("@type") != "Answer" or not ans.get("text"):
                    errs.append(f"FAQ {q.get('name')!r} has no acceptedAnswer.text")
                if plain(q["name"]) not in visible:
                    errs.append(f"FAQ question not visible on page: {q['name']!r}")
        elif t == "BreadcrumbList":
            items = n.get("itemListElement") or []
            if len(items) < 2:
                errs.append("BreadcrumbList needs 2+ items")
            for i, it in enumerate(items, 1):
                if it.get("position") != i:
                    errs.append(f"Breadcrumb position {it.get('position')} should be {i}")
                if not it.get("name"):
                    errs.append(f"Breadcrumb {i} has no name")
                if not URL.match(str(it.get("item", ""))):
                    errs.append(f"Breadcrumb {i} item is not an absolute site URL")
            if items and items[-1].get("item") != "https://1960smusic.net" + url:
                errs.append(f"last breadcrumb {items[-1].get('item')} != page URL {url}")
        elif t == "MusicRecording":
            need(n, ["name", "byArtist"], w, errs)
            if n.get("datePublished") and not DATE.match(n["datePublished"]):
                errs.append("MusicRecording datePublished not ISO")
        elif t == "MusicGroup":
            need(n, ["name"], w, errs)
        elif t == "ProfilePage":
            me = n.get("mainEntity") or {}
            if me.get("@type") != "Person" or not me.get("name"):
                errs.append("ProfilePage.mainEntity must be a Person with a name")
        elif t in ("WebSite", "Organization", "WebPage", "CollectionPage", "ItemList", "WebApplication", "VideoObject", "Person", "ProfilePage", "AboutPage"):
            need(n, ["name"] if t not in ("ItemList",) else ["itemListElement"], w, errs)
            if t == "VideoObject":
                need(n, ["name", "description", "thumbnailUrl", "uploadDate"], w, errs)
        else:
            warns.append(f"unchecked @type {t!r}")
        for k, v in n.items():
            if k in ("url", "@id") and isinstance(v, str) and v.startswith("http") and not URL.match(v):
                warns.append(f"{t} {k} points off-site: {v}")
    # @id references used by Article.about must resolve
    ids = {n.get("@id") for n in nodes if isinstance(n, dict) and n.get("@id")}
    for n in nodes:
        if isinstance(n, dict) and n.get("@type") == "Article" and isinstance(n.get("about"), dict):
            ref = n["about"].get("@id")
            if ref and ref not in ids and not n["about"].get("name"):
                errs.append(f"Article.about @id {ref} has no matching block")
    if not nodes:
        warns.append("no JSON-LD on page")
    return types, errs, warns


def main(paths, quiet=False):
    bad = False
    for p in paths:
        types, errs, warns = validate(p)
        if quiet and not errs and not warns:
            continue
        print(f"{p}\n  types: {', '.join(str(t) for t in types)}")
        for e in errs:
            print(f"  ERROR: {e}")
        for w in warns:
            print(f"  WARN:  {w}")
        if not errs:
            print("  OK" + (" (with warnings)" if warns else ""))
        bad |= bool(errs)
    if quiet:
        print(f"validate_jsonld: {len(paths)} pages checked, " + ("ERRORS found" if bad else "no errors"))
    return 1 if bad else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    quiet = args == ["--all"]
    if quiet:
        args = sorted(
            os.path.join(d, "index.html")
            for d, _, fs in os.walk(ROOT)
            if "index.html" in fs
            and os.path.relpath(d, ROOT).split(os.sep)[0] not in {"gen", "docs", "worker", "assets", "data", "node_modules"}
            and not os.path.relpath(d, ROOT).startswith(".")
        )
    sys.exit(main(args, quiet=quiet))
