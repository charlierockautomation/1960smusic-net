# -*- coding: utf-8 -*-
"""SEO-standard checks split out of check_article.py (2026-10-08 audit):
share image (og:image + Article JSON-LD image), Key Facts data prerequisite,
and the /1960s/<year>/ link rules for On This Day, trending and genre hubs.
(Song/artist year links live in check_article.check_key_facts.)
"""
import html as htmllib
import json
import os
import re
import sys

SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = "https://1960smusic.net"


def _article(text):
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S | re.I):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        if isinstance(data, dict) and data.get("@type") == "Article":
            return data
    return None


def _on_disk(url):
    path = url[len(BASE):] if url.startswith(BASE) else None
    return path is not None and os.path.exists(os.path.join(SITE_ROOT, path.lstrip("/")))


def check_share_image(text, errors):
    """og:image and the Article JSON-LD image must both exist, be absolute
    site URLs, and point at a file that exists on disk."""
    m = re.search(r'<meta property="og:image" content="([^"]*)"', text)
    if not m or not m.group(1):
        errors.append("no og:image meta tag")
    elif not m.group(1).startswith(BASE + "/"):
        errors.append(f"og:image is not an absolute {BASE} URL: {m.group(1)}")
    elif not _on_disk(m.group(1)):
        errors.append(f"og:image file not found on disk: {m.group(1)}")
    art = _article(text)
    img = (art or {}).get("image")
    if isinstance(img, list):
        img = img[0] if img else None
    if isinstance(img, dict):
        img = img.get("url")
    if not img:
        errors.append("Article JSON-LD has no image")
    elif not str(img).startswith(BASE + "/"):
        errors.append(f"Article JSON-LD image is not an absolute {BASE} URL: {img}")
    elif not _on_disk(str(img)):
        errors.append(f"Article JSON-LD image file not found on disk: {img}")


def check_key_facts_data(path, text, page_type, errors):
    """Song/artist pages need a verified gen/key_facts_data.py entry, and the
    rendered box must match it (run gen/build_key_facts.py --write)."""
    if page_type not in ("song story", "artist bio"):
        return
    from key_facts_data import ARTISTS, SONGS
    slug = os.path.basename(os.path.dirname(os.path.abspath(path)))
    entry = (SONGS if page_type == "song story" else ARTISTS).get(slug)
    if not entry:
        errors.append(f"no gen/key_facts_data.py entry for '{slug}': add verified facts there first, then run gen/build_key_facts.py --write")
        return
    m = re.search(r'<aside class="key-facts"[^>]*>(.*?)</aside>', text, flags=re.S)
    if not m:
        return  # check_key_facts already reports the missing box
    box = {htmllib.unescape(a).strip(): htmllib.unescape(re.sub(r"<[^>]+>", "", b)).strip()
           for a, b in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", m.group(1), flags=re.S)}
    for label, value in entry["rows"]:
        if box.get(label) != value:
            errors.append(f'Key Facts "{label}" does not match gen/key_facts_data.py: run gen/build_key_facts.py --write')


def check_year_links(text, page_type, path, errors):
    years = set(re.findall(r'href="/1960s/(\d{4})/"', text))
    if page_type == "trending" and not years:
        errors.append("trending post must link at least one relevant /1960s/<year>/ page")
    elif page_type == "genre hub":
        from genre_peak_years import PEAK_YEARS
        slug = os.path.basename(os.path.dirname(os.path.abspath(path)))
        want = PEAK_YEARS.get(slug)
        if not want:
            errors.append(f"genre hub '{slug}' has no entry in gen/genre_peak_years.py")
        else:
            for y in want:
                if str(y) not in years:
                    errors.append(f"genre hub must link its key year page /1960s/{y}/")
    elif page_type == "on this day":
        for y, body in re.findall(r'<section id="y(\d{4})">(.*?)</section>', text, flags=re.S):
            if f'href="/1960s/{y}/"' not in body:
                errors.append(f"On This Day {y} section must link /1960s/{y}/")
