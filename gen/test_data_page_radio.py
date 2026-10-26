# -*- coding: utf-8 -*-
"""Checks /data/1960s-music-genres-by-year/ against data/radio-eligible-*.json:
table counts and shares, totals, headline unique count, psychedelic figures,
and that all 10 year pages and 8 genre hubs are linked.
Usage: python3 gen/test_data_page_radio.py"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_data_page_radio as b

page = open(os.path.join(b.OUT_DIR, "index.html"), encoding="utf-8").read()
cell, ytot, gtot, unique = b.stats(b.load())
total = sum(ytot.values())
errs = []
tbody = re.search(r"<tbody>(.*?)</tbody>", page, re.S).group(1)
rows = {}
for tr in re.findall(r"<tr>(.*?)</tr>", tbody, re.S):
    label = re.sub(r"<[^>]+>", "", re.search(r"<th[^>]*>(.*?)</th>", tr, re.S).group(1))
    rows[label] = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td>(.*?)</td>", tr, re.S)]
for y in b.YEARS:
    cells = rows[str(y)]
    for i, (g, _) in enumerate(b.GENRES):
        n = cell[(y, g)]
        want = f"{n} ({b.pct(n, ytot[y])})" if n else "0"
        if cells[i] != want:
            errs.append(f"{y} {g}: page {cells[i]!r} != {want!r}")
    if cells[-1] != str(ytot[y]):
        errs.append(f"{y} total {cells[-1]} != {ytot[y]}")
allrow = rows["All years"]
for i, (g, _) in enumerate(b.GENRES):
    if allrow[i] != f"{gtot[g]} ({b.pct(gtot[g], total)})":
        errs.append(f"all-years {g}: {allrow[i]}")
if allrow[-1] != str(total):
    errs.append("grand total mismatch")
if f"{unique} songs on the 1960smusic.net" not in page:
    errs.append("headline unique count missing or wrong")
if f"The Radio Dial lists {total} songs" not in page:
    errs.append("method row count wrong")
for y in b.YEARS:
    if f'href="/1960s/{y}/"' not in page:
        errs.append(f"missing link /1960s/{y}/")
for g, _ in b.GENRES:
    if f'href="/blog/genres/{g}/"' not in page:
        errs.append(f"missing hub link {g}")
for need in ("/tools/radio/", "our dataset", "primary genre", "Wild Thing"):
    if need not in page:
        errs.append(f"missing {need!r}")
if any(ytot[y] < 20 for y in b.YEARS) and "small sample" not in page:
    errs.append("year under 20 songs but no small-sample note")
print("FAIL" if errs else "PASS", *errs, sep="\n  " if errs else " ")
sys.exit(1 if errs else 0)
