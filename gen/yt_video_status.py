# -*- coding: utf-8 -*-
"""Shared YouTube Data API v3 status checker (embeddable + made-for-kids).

Single source of the actual API call so gen/radio_verify.py never duplicates
it. Maintains gen/yt_status_cache.json: a flat {video_id: {embeddable,
made_for_kids, privacy_status, checked_at}} record covering every id ever
checked by any part of the pipeline (radio-eligible, songs.json, or a
one-off page embed). check_article.py reads this file to enforce that no
new YouTube id ships without a status on record.

videos.list with part=status costs 1 quota unit per call regardless of how
many ids are batched (up to 50), per Google's quota documentation
(developers.google.com/youtube/v3/determine_quota_cost).
"""
import json, os, sys, urllib.request, urllib.parse, datetime

QUOTA_COST_PER_CALL = 1
BATCH_SIZE = 50
CACHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "yt_status_cache.json"))


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def fetch_status(ids, api_key):
    """Return (status_by_id, calls_made). status_by_id[id] = {embeddable,
    made_for_kids, privacy_status} or is absent if YouTube returned no item
    for that id (deleted/private video)."""
    ids = list(dict.fromkeys(ids))  # de-dupe, keep order
    out = {}
    calls = 0
    for batch in chunks(ids, BATCH_SIZE):
        url = ("https://www.googleapis.com/youtube/v3/videos?part=status&id=" +
               urllib.parse.quote(",".join(batch)) + "&key=" + api_key)
        with urllib.request.urlopen(url, timeout=20) as r:
            resp = json.loads(r.read().decode())
        calls += 1
        for item in resp.get("items", []):
            st = item.get("status", {})
            out[item["id"]] = {
                "embeddable": st.get("embeddable") is True,
                "made_for_kids": st.get("madeForKids") is True,
                "privacy_status": st.get("privacyStatus"),
            }
    return out, calls


def load_cache():
    if os.path.exists(CACHE_PATH):
        return json.load(open(CACHE_PATH))
    return {}


def save_cache(cache):
    json.dump(cache, open(CACHE_PATH, "w"), indent=1, sort_keys=True)


def record(cache, status_by_id):
    """Merge fresh status results into the flat cache with today's date."""
    today = datetime.date.today().isoformat()
    for vid, st in status_by_id.items():
        cache[vid] = dict(st, checked_at=today)
    return cache


def check_and_record(ids, api_key):
    status, calls = fetch_status(ids, api_key)
    cache = record(load_cache(), status)
    save_cache(cache)
    return status, calls


if __name__ == "__main__":
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        sys.exit("Set YOUTUBE_API_KEY env var first.")
    if len(sys.argv) < 2:
        sys.exit("usage: python3 gen/yt_video_status.py id1,id2,...")
    ids = [i for i in sys.argv[1].split(",") if i]
    status, calls = check_and_record(ids, api_key)
    for vid in ids:
        st = status.get(vid)
        if not st:
            print(f"{vid}: NOT FOUND (deleted/private, or bad id)")
        else:
            print(f"{vid}: embeddable={st['embeddable']} made_for_kids={st['made_for_kids']} "
                  f"privacy={st['privacy_status']}")
    print(f"\n{calls} API call(s), {calls * QUOTA_COST_PER_CALL} quota unit(s).")
