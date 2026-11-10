# -*- coding: utf-8 -*-
"""Schema built from gen/key_facts_data.py (Task 5, 2026-11-10).

Run from gen/build_key_facts.py, so one command renders the Key Facts box and
the JSON-LD that mirrors it:
  - song stories: the MusicRecording block gets byArtist with the artist
    page's #subject @id (when a bio exists), recordingOf a MusicComposition
    whose composer (and lyricist, where the box splits music and lyrics) are
    the "Written by" names, producer from "Produced by", and inAlbum from
    SONG_ALBUMS where that album is verified.
  - artist bios: the MusicGroup/Person #subject node gets sameAs from SAME_AS.
Only names that appear in the box text are used (credit_names() checks it).
"""
import json
import os
import re

from key_facts_data import ARTISTS, CREDIT_OVERRIDES, SAME_AS, SONG_ALBUMS, SONGS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = "https://1960smusic.net"
LD = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)


def split_names(value):
    """Person names from a box value: drop parentheticals, anything after ';',
    "credited as ..." aliases and "Credited to ...:" preambles, then split."""
    v = value.split(";")[0]
    paren = re.search(r"\(([^)]*,[^)]*)\)", v)
    if paren and re.match(r"^[A-Z][\w-]+-[A-Z]", v):  # "Holland-Dozier-Holland (Brian Holland, ...)"
        v = paren.group(1)
    v = re.sub(r"\([^)]*\)", "", v)
    v = re.sub(r"^Credited to (?:[^:]*:)?\s*", "", v, flags=re.I)
    v = re.sub(r",\s*credited as .*$", "", v)
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+", v)
    return [p.strip() for p in parts if p.strip()]


def credit_names(slug):
    rows = dict(SONGS[slug]["rows"])
    o = CREDIT_OVERRIDES.get(slug, {})
    writers = o.get("writers") or split_names(rows["Written by"])
    lyricists = o.get("lyricists", [])
    producers = o.get("producers") or split_names(rows["Produced by"])
    for n in writers + lyricists:
        if n not in rows["Written by"]:
            raise SystemExit(f"{slug}: writer {n!r} not in Key Facts 'Written by'")
    for n in producers:
        if n not in rows["Produced by"]:
            raise SystemExit(f"{slug}: producer {n!r} not in Key Facts 'Produced by'")
    return writers, lyricists, producers


_BIOS = None


def artist_ref(name):
    """Node for a credited act: link to its bio's #subject when one exists."""
    global _BIOS
    if _BIOS is None:
        _BIOS = {}
        for slug in ARTISTS:
            with open(os.path.join(ROOT, "blog", "artists", slug, "index.html"), encoding="utf-8") as f:
                node = subject_node(f.read())
            if node:
                _BIOS[node.get("name")] = {"@type": node["@type"], "@id": node["@id"], "name": node.get("name")}
    return _BIOS.get(name)


def person(name):
    return artist_ref(name) or {"@type": "Person", "name": name}


def blocks(text):
    out = []
    for m in LD.finditer(text):
        try:
            out.append((m, json.loads(m.group(1))))
        except ValueError:
            pass
    return out


def subject_node(text):
    for _, d in blocks(text):
        if isinstance(d, dict) and str(d.get("@id", "")).endswith("#subject"):
            return d
    return None


def replace_block(text, m, data):
    return text[: m.start(1)] + json.dumps(data, ensure_ascii=False) + text[m.end(1):]


def song_artist_page(text):
    """Bio URL from the breadcrumb (Home > Artist > Song) if that bio exists."""
    for _, d in blocks(text):
        if d.get("@type") == "BreadcrumbList":
            for it in d.get("itemListElement", []):
                u = str(it.get("item", ""))
                m = re.match(re.escape(BASE) + r"/blog/artists/([^/]+)/$", u)
                if m and os.path.exists(os.path.join(ROOT, "blog", "artists", m.group(1), "index.html")):
                    return u
    return None


def enrich_song(slug, text):
    for m, d in blocks(text):
        if d.get("@type") != "MusicRecording":
            continue
        writers, lyricists, producers = credit_names(slug)
        bio = song_artist_page(text)
        by = d.get("byArtist") or {}
        if bio:
            by = {"@type": by.get("@type", "MusicGroup"), "@id": bio + "#subject", "name": by.get("name")}
        new = {k: d[k] for k in ("@context", "@type", "@id", "name", "url") if k in d}
        new["byArtist"] = by
        comp = {"@type": "MusicComposition", "name": d["name"], "composer": [person(n) for n in writers]}
        if lyricists:
            comp["lyricist"] = [person(n) for n in lyricists]
        new["recordingOf"] = comp
        new["producer"] = [person(n) for n in producers]
        album = SONG_ALBUMS.get(slug)
        if album:
            new["inAlbum"] = {"@type": "MusicAlbum", "name": album}
        if "datePublished" in d:
            new["datePublished"] = d["datePublished"]
        return replace_block(text, m, new)
    raise SystemExit(f"{slug}: no MusicRecording block")


def enrich_artist(slug, text):
    for m, d in blocks(text):
        if str(d.get("@id", "")).endswith("#subject") and d.get("@type") in ("MusicGroup", "Person"):
            urls = SAME_AS.get(slug)
            if not urls:
                return text
            if d.get("sameAs") == urls:
                return text
            d = dict(d)
            d["sameAs"] = urls
            return text[: m.start(1)] + json.dumps(d, indent=2, ensure_ascii=False) + text[m.end(1):]
    raise SystemExit(f"{slug}: no MusicGroup/Person #subject block")
