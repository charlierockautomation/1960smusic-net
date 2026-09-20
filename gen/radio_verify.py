# -*- coding: utf-8 -*-
"""YouTube compliance checks, all sharing gen/yt_video_status.py's API call.

Three modes:
  python3 gen/radio_verify.py [--limit N]
      Quarterly: re-check radio-eligible-<genre>.json ids. Flags no-longer-
      embeddable/public ids to radio-dial-flagged.md (manual backfill, never
      auto-removed). Made-for-kids ids ARE auto-removed from the radio pool
      (Charlie's call: no ad-tracking-toggle handling built for radio) and
      reported in the same file.

  python3 gen/radio_verify.py --songs
      Check every youtube_id in gen/yt_cache.json (the songs.json source
      cache), writing embeddable/made_for_kids/checked_at onto each cache
      entry. Run gen/generate.py afterward to surface those fields onto
      data/songs.json records.

One-time backfill against songs.json + live pages lives in
gen/yt_backfill.py (report-only, separate from this file to keep both
under the house line-count ceiling); it reuses the same fetch_status call.

Needs YOUTUBE_API_KEY in the environment (Google Cloud Console free tier).
Never hardcode the key; it must never appear in committed files or
client-side code.
"""
import json, os, sys, argparse, datetime

from yt_video_status import fetch_status, record, load_cache as load_status_cache, \
    save_cache as save_status_cache, QUOTA_COST_PER_CALL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
YT_CACHE = os.path.join(os.path.dirname(__file__), "yt_cache.json")
FLAGGED_MD = os.path.join(ROOT, "radio-dial-flagged.md")
GENRES = ["british-invasion", "motown-soul", "folk-rock", "garage-surf-rock",
          "psychedelic-rock", "country-60s", "pop-brill-building", "jazz-easy-listening"]


def api_key_or_exit():
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit("Set YOUTUBE_API_KEY env var first (Google Cloud Console, free tier).")
    return key


def load_radio_files():
    return {g: json.load(open(os.path.join(DATA, "radio-eligible-%s.json" % g))) for g in GENRES}


def save_radio_file(g, entries):
    path = os.path.join(DATA, "radio-eligible-%s.json" % g)
    lines = ["["]
    for i, rec in enumerate(entries):
        lines.append("  " + json.dumps(rec, ensure_ascii=False) + ("," if i < len(entries) - 1 else ""))
    lines.append("]")
    open(path, "w").write("\n".join(lines) + "\n")


def write_flagged_md(today, flagged, excluded):
    lines = ["# Radio Dial -- Flagged IDs\n",
             "Quarterly `gen/radio_verify.py` run on %s.\n" % today]
    lines.append("## No longer embeddable/public (not auto-removed)\n")
    if flagged:
        lines += ["| Genre | Title | Artist | YouTube ID | Was verified |", "|---|---|---|---|---|"]
        lines += ["| %s | %s | %s | %s | %s |" % (
            g, r["title"], r["artist"], r["youtube_id"], r.get("verified_date") or "never") for g, r in flagged]
    else:
        lines.append("None flagged as of %s." % today)
    lines.append("\n## Made-for-kids (auto-removed from radio pool)\n")
    if excluded:
        lines += ["| Genre | Title | Artist | YouTube ID |", "|---|---|---|---|"]
        lines += ["| %s | %s | %s | %s |" % (g, r["title"], r["artist"], r["youtube_id"]) for g, r in excluded]
    else:
        lines.append("None excluded as of %s." % today)
    open(FLAGGED_MD, "w").write("\n".join(lines) + "\n")


def run_radio(limit):
    api_key = api_key_or_exit()
    files = load_radio_files()
    all_entries = [(g, rec) for g, entries in files.items() for rec in entries]
    all_entries.sort(key=lambda x: x[1].get("verified_date") or "0000-00-00")
    if limit:
        all_entries = all_entries[:limit]

    ids = list({rec["youtube_id"] for _, rec in all_entries})
    print("Checking %d unique video ids (%d entries)..." % (len(ids), len(all_entries)))
    status, calls = fetch_status(ids, api_key)
    save_status_cache(record(load_status_cache(), status))

    today = datetime.date.today().isoformat()
    flagged, excluded = [], []
    for g, rec in all_entries:
        st = status.get(rec["youtube_id"])
        if st and st["made_for_kids"]:
            excluded.append((g, rec))
            continue
        if st and st["embeddable"] and st["privacy_status"] == "public":
            rec["verified_date"] = today
        else:
            flagged.append((g, rec))

    for g, entries in files.items():
        kept = [rec for rec in entries if (g, rec) not in excluded]
        save_radio_file(g, kept)

    write_flagged_md(today, flagged, excluded)
    print("Passed: %d, flagged: %d, made-for-kids excluded: %d" %
          (len(all_entries) - len(flagged) - len(excluded), len(flagged), len(excluded)))
    print("%d API call(s), %d quota unit(s)." % (calls, calls * QUOTA_COST_PER_CALL))
    print("Report:", FLAGGED_MD)


def run_songs():
    api_key = api_key_or_exit()
    cache = json.load(open(YT_CACHE))
    ids = [c["youtube_id"] for c in cache.values() if c.get("youtube_id")]
    print("Checking %d song ids..." % len(set(ids)))
    status, calls = fetch_status(ids, api_key)
    save_status_cache(record(load_status_cache(), status))

    today = datetime.date.today().isoformat()
    kids_hits = []
    for key, c in cache.items():
        st = status.get(c.get("youtube_id"))
        if not st:
            continue
        c["embeddable"] = st["embeddable"]
        c["made_for_kids"] = st["made_for_kids"]
        c["checked_at"] = today
        if st["made_for_kids"]:
            kids_hits.append((key, c["youtube_id"]))
    json.dump(cache, open(YT_CACHE, "w"), indent=1)

    print("%d API call(s), %d quota unit(s)." % (calls, calls * QUOTA_COST_PER_CALL))
    if kids_hits:
        print("MADE-FOR-KIDS hits (song cache, not auto-removed, needs your review):")
        for key, vid in kids_hits:
            print("  %s -> %s" % (key, vid))
    else:
        print("No made-for-kids hits.")
    print("Run gen/generate.py to surface these fields onto data/songs.json.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--songs", action="store_true")
    args = ap.parse_args()
    if args.songs:
        run_songs()
    else:
        run_radio(args.limit)


if __name__ == "__main__":
    main()
