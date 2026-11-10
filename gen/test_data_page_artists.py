# -*- coding: utf-8 -*-
"""Checks /data/1960s-musicians-by-song-count/ against data/radio-eligible-*.json:
table rows (rank, act, count, main genre, years), ties, bio links, totals,
and that all 10 year pages, 8 genre hubs and the Radio Dial are linked.
Usage: python3 gen/test_data_page_artists.py"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_data_page_artists as b

page = open(os.path.join(b.OUT_DIR, "index.html"), encoding="utf-8").read()
rows, songs = b.load()
count, top, cutoff, info = b.stats(songs)
bio = b.bios()
errs = []

if len(songs) != len({s["youtube_id"] for s in songs}):
    errs.append("duplicate youtube ids in unique set")
order = sorted(count.values(), reverse=True)
if cutoff != order[b.TOP_N - 1] or any(count[a] < cutoff for a in top) or \
        len(top) != sum(1 for n in count.values() if n >= cutoff):
    errs.append("top-N-with-ties selection wrong")

tbody = re.search(r"<tbody>(.*?)</tbody>", page, re.S).group(1)
trs = re.findall(r"<tr>(.*?)</tr>", tbody, re.S)
if len(trs) != len(top):
    errs.append(f"table has {len(trs)} rows, want {len(top)}")
for tr, a in zip(trs, top):
    d = info[a]
    act_cell = re.search(r"<th[^>]*>(.*?)</th>", tr, re.S).group(1)
    tds = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td>(.*?)</td>", tr, re.S)]
    name = re.sub(r"<[^>]+>", "", act_cell).replace("&amp;", "&")
    if name != a:
        errs.append(f"row order: {name!r} != {a!r}")
    rank = 1 + sum(1 for x in top if count[x] > d["n"])
    yrs = str(d["first"]) if d["first"] == d["last"] else f"{d['first']} to {d['last']}"
    want = [str(rank), str(d["n"]), b.SHORT[d["genre"]].replace("&", "&amp;"), yrs]
    if tds != want:
        errs.append(f"{a}: {tds} != {want}")
    u = bio.get(b.radio.norm(a))
    if u and f'href="{u}"' not in act_cell:
        errs.append(f"{a}: bio link {u} missing")
    if not u and "<a " in act_cell:
        errs.append(f"{a}: links but has no live bio")
    # main genre really is the plurality station
    if d["genres"][d["genre"]] != max(d["genres"].values()):
        errs.append(f"{a}: main genre not plurality")

for need in (f"with {info[top[0]]['n']} of its {len(songs)} songs", f"The Radio Dial lists {len(rows)} songs",
             f"{len(count)} different acts", "our dataset", "Wild Thing", 'href="/tools/radio/"'):
    if need not in page:
        errs.append(f"missing {need!r}")
for y in b.YEARS:
    if f'href="/1960s/{y}/"' not in page:
        errs.append(f"missing link /1960s/{y}/")
for g, _ in b.GENRES:
    if f'href="/blog/genres/{g}/"' not in page:
        errs.append(f"missing hub link {g}")
print("FAIL" if errs else "PASS", *errs, sep="\n  " if errs else " ")
sys.exit(1 if errs else 0)
