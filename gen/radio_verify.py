# -*- coding: utf-8 -*-
"""Quarterly maintenance: re-check every radio-eligible song's YouTube id
against the Data API v3 videos.list endpoint. Flags ids that no longer
return embeddable:true + privacyStatus:public to radio-dial-flagged.md
for manual backfill -- never auto-removes anything from the data files.

Run manually (not on page load, not in generate.py):
    YOUTUBE_API_KEY=xxx python3 gen/radio_verify.py [--limit N]

--limit caps how many of the oldest-verified_date entries get rechecked
in one run (useful for spreading a big backlog across API-key quota)."""
import json, os, sys, urllib.request, urllib.parse, datetime, argparse

DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
FLAGGED_MD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "radio-dial-flagged.md"))
GENRES = ["british-invasion", "motown-soul", "folk-rock", "garage-surf-rock",
          "psychedelic-rock", "country-60s", "pop-brill-building", "jazz-easy-listening"]

def load_all():
    files = {}
    for g in GENRES:
        path = os.path.join(DATA, "radio-eligible-%s.json" % g)
        files[g] = json.load(open(path))
    return files

def save(g, entries):
    path = os.path.join(DATA, "radio-eligible-%s.json" % g)
    lines = ["["]
    for i, rec in enumerate(entries):
        comma = "," if i < len(entries) - 1 else ""
        lines.append("  " + json.dumps(rec, ensure_ascii=False) + comma)
    lines.append("]")
    open(path, "w").write("\n".join(lines) + "\n")

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def check_ids(ids, api_key):
    status = {}
    for batch in chunks(ids, 50):
        url = ("https://www.googleapis.com/youtube/v3/videos?part=status&id=" +
               urllib.parse.quote(",".join(batch)) + "&key=" + api_key)
        with urllib.request.urlopen(url, timeout=20) as r:
            resp = json.loads(r.read().decode())
        for item in resp.get("items", []):
            st = item.get("status", {})
            status[item["id"]] = (st.get("embeddable") is True and st.get("privacyStatus") == "public")
    return status

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        sys.exit("Set YOUTUBE_API_KEY env var first (Google Cloud Console, free tier).")

    files = load_all()
    all_entries = []
    for g, entries in files.items():
        for rec in entries:
            all_entries.append((g, rec))
    all_entries.sort(key=lambda x: x[1].get("verified_date") or "0000-00-00")
    if args.limit:
        all_entries = all_entries[:args.limit]

    ids = list({rec["youtube_id"] for _, rec in all_entries})
    print("Checking %d unique video ids (%d entries)..." % (len(ids), len(all_entries)))
    status = check_ids(ids, api_key)

    today = datetime.date.today().isoformat()
    flagged = []
    for g, rec in all_entries:
        ok = status.get(rec["youtube_id"], False)
        if ok:
            rec["verified_date"] = today
        else:
            flagged.append((g, rec))

    for g in GENRES:
        save(g, files[g])

    lines = ["# Radio Dial -- Flagged IDs\n",
              "Quarterly `gen/radio_verify.py` run on %s. Entries below no longer\n"
              "returned `embeddable:true` + `privacyStatus:public`. Not auto-removed --\n"
              "backfill a working id in the matching `data/radio-eligible-<genre>.json`\n"
              "entry by hand, or drop the entry if no replacement exists.\n" % today]
    if flagged:
        lines.append("| Genre | Title | Artist | YouTube ID | Was verified |")
        lines.append("|---|---|---|---|---|")
        for g, rec in flagged:
            lines.append("| %s | %s | %s | %s | %s |" % (
                g, rec["title"], rec["artist"], rec["youtube_id"], rec.get("verified_date") or "never"))
    else:
        lines.append("None flagged as of %s.\n" % today)
    open(FLAGGED_MD, "w").write("\n".join(lines) + "\n")

    print("Passed: %d, flagged: %d" % (len(all_entries) - len(flagged), len(flagged)))
    print("Flagged list written to", FLAGGED_MD)

if __name__ == "__main__":
    main()
