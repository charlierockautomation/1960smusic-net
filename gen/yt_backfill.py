# -*- coding: utf-8 -*-
"""One-time YouTube compliance backfill: every id in gen/yt_cache.json plus
every youtube.com/embed/<id> already live in blog/ pages. Reuses the same
gen/yt_video_status.fetch_status call as gen/radio_verify.py.

Report-only. Never edits a live page or a data file; writes
youtube-compliance-backfill.md for Charlie to review before anything
downstream changes.

Usage: YOUTUBE_API_KEY=xxx python3 gen/yt_backfill.py
"""
import json, os, sys, re, glob, datetime

from yt_video_status import fetch_status, record, load_cache as load_status_cache, \
    save_cache as save_status_cache, QUOTA_COST_PER_CALL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
YT_CACHE = os.path.join(os.path.dirname(__file__), "yt_cache.json")
BACKFILL_MD = os.path.join(ROOT, "youtube-compliance-backfill.md")


def scan_live_page_ids():
    ids = set()
    for path in glob.glob(os.path.join(ROOT, "blog", "**", "index.html"), recursive=True):
        text = open(path, encoding="utf-8").read()
        for m in re.finditer(r"youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{11})", text):
            ids.add((m.group(1), os.path.relpath(path, ROOT)))
    return ids


def table(rows, empty):
    if not rows:
        return [empty]
    return ["| YouTube ID | Found in |", "|---|---|"] + ["| %s | %s |" % r for r in rows]


def main():
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        sys.exit("Set YOUTUBE_API_KEY env var first.")

    cache = json.load(open(YT_CACHE))
    song_ids = {c["youtube_id"] for c in cache.values() if c.get("youtube_id")}
    page_hits = scan_live_page_ids()
    page_ids = {vid for vid, _ in page_hits}
    all_ids = song_ids | page_ids
    print("Checking %d unique ids (%d from songs cache, %d from live pages)..." %
          (len(all_ids), len(song_ids), len(page_ids)))
    status, calls = fetch_status(list(all_ids), api_key)
    save_status_cache(record(load_status_cache(), status))

    today = datetime.date.today().isoformat()
    kids_hits, not_embeddable, not_found = [], [], []
    for vid in sorted(all_ids):
        st = status.get(vid)
        where = ", ".join(sorted(p for v, p in page_hits if v == vid)) or "songs cache only"
        if not st:
            not_found.append((vid, where))
        elif st["made_for_kids"]:
            kids_hits.append((vid, where))
        elif not st["embeddable"]:
            not_embeddable.append((vid, where))

    lines = ["# YouTube Compliance Backfill -- %s\n" % today,
             "One-time check of every id in gen/yt_cache.json plus every live page\n"
             "embed. Report-only: no live page or data file changed by this run.\n",
             "%d ids checked, %d API call(s), %d quota unit(s).\n" %
             (len(all_ids), calls, calls * QUOTA_COST_PER_CALL),
             "## Made-for-kids (needs your decision before anything changes)\n"]
    lines += table(kids_hits, "None.\n")
    lines.append("\n## Not embeddable\n")
    lines += table(not_embeddable, "None.\n")
    lines.append("\n## Not found (deleted/private/bad id)\n")
    lines += table(not_found, "None.\n")
    open(BACKFILL_MD, "w").write("\n".join(lines) + "\n")

    print("%d API call(s), %d quota unit(s)." % (calls, calls * QUOTA_COST_PER_CALL))
    print("Made-for-kids hits: %d, not embeddable: %d, not found: %d" %
          (len(kids_hits), len(not_embeddable), len(not_found)))
    print("Report:", BACKFILL_MD)


if __name__ == "__main__":
    main()
