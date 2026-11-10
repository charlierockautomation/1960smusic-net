# -*- coding: utf-8 -*-
"""Radio Dial song counts, generated from data/radio-eligible-*.json.

  unique = distinct youtube_id across all eight station files
  rows   = total entries (a song on two stations counts twice)

Write mode fills every <span data-radio-count="unique|rows">N</span> marker
on the site with the current number. Check mode (run by publish_prep.py)
fails if any marker, or any stated count in a known Radio Dial phrase
(data pages, cards, meta and JSON-LD text, posts.json, llms.txt),
disagrees with the data.
The data pages themselves are rebuilt by gen/build_data_page_radio.py and
gen/build_data_page_artists.py.

Usage: python3 gen/radio_counts.py            (write markers, then check)
       python3 gen/radio_counts.py --check    (check only)
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MARKER = re.compile(r'(<span data-radio-count="(unique|rows)">)(\d+)(</span>)')
# (regex, which count each group must equal); text is checked with tags stripped
PHRASES = [
    (re.compile(r"(\d+) songs on (?:our|the) (?:1960smusic\.net )?Radio Dial"), ("unique",)),
    (re.compile(r"among (\d+) on (?:our|the) Radio Dial"), ("unique",)),
    (re.compile(r"(\d+) Radio Dial songs"), ("rows",)),
    (re.compile(r"Radio Dial lists (\d+) songs across eight stations, and (\d+)"), ("rows", "unique")),
    (re.compile(r"with \d+ of its (\d+) songs"), ("unique",)),
    (re.compile(r"(\d+) different acts across (\d+) songs"), (None, "unique")),
    (re.compile(r"(?:hold|holds) (?:more than )?(\d+) (?:unique songs|tracks)"), ("unique",)),
]


def counts():
    rows, ids = 0, set()
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "radio-eligible-*.json"))):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        songs = data if isinstance(data, list) else data.get("songs", [])
        rows += len(songs)
        ids.update(s["youtube_id"] for s in songs)
    return {"unique": len(ids), "rows": rows}


def pages():
    skip = {"gen", "docs", "worker", "assets", "node_modules"}
    for d, _, fs in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        if rel.split(os.sep)[0] in skip or rel.startswith("."):
            continue
        if "index.html" in fs:
            yield os.path.join(d, "index.html")


def write(c):
    changed = []
    for p in pages():
        with open(p, encoding="utf-8") as f:
            text = f.read()
        new = MARKER.sub(lambda m: m.group(1) + str(c[m.group(2)]) + m.group(4), text)
        if new != text:
            with open(p, "w", encoding="utf-8") as f:
                f.write(new)
            changed.append(os.path.relpath(p, ROOT))
    return changed


EXTRA_FILES = ["llms.txt", os.path.join("data", "posts.json")]


def check(c):
    errs = []
    for p in list(pages()) + [os.path.join(ROOT, x) for x in EXTRA_FILES]:
        with open(p, encoding="utf-8") as f:
            text = f.read()
        rel = os.path.relpath(p, ROOT)
        for m in MARKER.finditer(text):
            if int(m.group(3)) != c[m.group(2)]:
                errs.append(f"{rel}: marker {m.group(2)}={m.group(3)}, data says {c[m.group(2)]}")
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text))
        for rx, kinds in PHRASES:
            for m in rx.finditer(plain):
                for kind, val in zip(kinds, m.groups()):
                    if kind and int(val) != c[kind]:
                        errs.append(f"{rel}: \"{m.group(0)}\" states {val}, data says {kind}={c[kind]}")
    return errs


def main(argv):
    c = counts()
    if "--check" not in argv:
        for rel in write(c):
            print(f"updated radio count markers in {rel}")
    errs = check(c)
    for e in errs:
        print(f"  FAIL: {e}")
    print(f"radio counts: unique={c['unique']} rows={c['rows']}, " + ("FAIL (rebuild data pages / fix copy)" if errs else "all stated counts match"))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
