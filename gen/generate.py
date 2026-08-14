# -*- coding: utf-8 -*-
"""Generate genres.json, artists.json, songs.json for 1960smusic.net.
Fetches REAL, currently-live, embeddable YouTube IDs via YouTube search +
oEmbed verification. Flags any ID that cannot be confidently matched."""
import json, re, time, os, sys, urllib.parse, urllib.request

from artists_data import ARTISTS
from genres_data import GENRES
from songs_data import SONGS

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
CACHE = os.path.join(os.path.dirname(__file__), "yt_cache.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

STOP = {"the", "and", "his", "her", "band", "experience", "tijuana", "brass",
        "orchestra", "featuring", "feat", "with", "of", "pharaohs", "miracles",
        "vandellas", "seasons", "tops", "supremes", "del-tones", "shondells"}

# article_slug overrides: set once a bio/song-story page has been placed
# (may still be status "placed" rather than "live" -- see link-map.md)
ARTIST_ARTICLE_SLUGS = {
    "the-beatles": "/blog/artists/the-beatles/",
}
SONG_ARTICLE_SLUGS = {}

def slug(s):
    s = s.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[''\u2019]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")

def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", " ", s)          # drop parentheticals
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")

def yt_search_ids(query, n=6):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    try:
        html = http_get(url)
    except Exception as e:
        return []
    seen, out = set(), []
    for m in re.finditer(r'"videoId":"([a-zA-Z0-9_-]{11})"', html):
        vid = m.group(1)
        if vid not in seen:
            seen.add(vid); out.append(vid)
        if len(out) >= n:
            break
    return out

def oembed(vid):
    url = ("https://www.youtube.com/oembed?url=" +
           urllib.parse.quote("https://www.youtube.com/watch?v=" + vid) +
           "&format=json")
    try:
        data = json.loads(http_get(url, timeout=15))
        return data
    except Exception:
        return None

def title_match(song_title, embed_title):
    et = norm(embed_title)
    words = [w for w in norm(song_title).split() if len(w) > 2]
    if not words:
        words = norm(song_title).split()
    if norm(song_title) and norm(song_title) in et:
        return True
    hits = sum(1 for w in words if w in et)
    return hits >= max(1, (len(words) + 1) // 2)

def artist_match(artist_name, embed_title, author):
    hay = norm(embed_title) + " " + norm(author or "")
    words = [w for w in norm(artist_name).split() if len(w) > 2 and w not in STOP]
    if not words:
        return True
    return any(w in hay for w in words)

def resolve_youtube(title, artist_name):
    """Return (video_id, flagged, reason)."""
    query = f"{artist_name} {title} official"
    ids = yt_search_ids(query)
    if not ids:
        # retry simpler query
        ids = yt_search_ids(f"{artist_name} {title}")
    if not ids:
        return (None, True, "YouTube search returned no results from sandbox \u2014 needs manual lookup.")
    first = ids[0]
    for vid in ids[:5]:
        data = oembed(vid)
        time.sleep(0.15)
        if not data:
            continue
        et = data.get("title", "")
        au = data.get("author_name", "")
        if title_match(title, et) and artist_match(artist_name, et, au):
            return (vid, False, None)
    # No confident match among candidates; verify the first is at least live.
    d0 = oembed(first)
    if d0:
        return (first, True,
                "Top YouTube result is live/embeddable but its title/author did not "
                f"confidently match '{artist_name} \u2013 {title}'; verify it is the correct recording.")
    return (first, True, "Could not verify the video via oEmbed; ID is a best-effort estimate.")

def load_cache():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    return {}

def main():
    cache = load_cache()
    # ---- resolve YouTube ids (with cache) ----
    total = len(SONGS)
    for i, s in enumerate(SONGS):
        title, artist_name = s[0], s[1]
        key = f"{artist_name}|||{title}"
        if key in cache:
            continue
        vid, flagged, reason = resolve_youtube(title, artist_name)
        cache[key] = {"youtube_id": vid, "flagged": flagged, "reason": reason}
        json.dump(cache, open(CACHE, "w"), indent=1)
        print(f"[{i+1}/{total}] {artist_name} - {title} -> {vid} flagged={flagged}", flush=True)
        time.sleep(0.25)

    # ---- build song ids ----
    song_ids = {}
    used = set()
    for s in SONGS:
        title, artist_id = s[0], s[2]
        base = slug(title) + "-" + re.sub(r"^the-", "", artist_id)
        sid = base
        k = 2
        while sid in used:
            sid = f"{base}-{k}"; k += 1
        used.add(sid)
        song_ids[id(s)] = sid

    # ---- songs.json ----
    songs_json = []
    by_artist = {}
    for s in SONGS:
        (title, artist_name, artist_id, year, genre_id, difficulty, clip,
         moods, trivia, secondary) = s
        sid = song_ids[id(s)]
        c = cache[f"{artist_name}|||{title}"]
        rec = {
            "id": sid,
            "title": title,
            "artist_id": artist_id,
            "artist_name": artist_name,
            "year": year,
            "genre_id": genre_id,
            "secondary_genre_ids": secondary,
            "youtube_id": c["youtube_id"],
            "_youtube_flagged": bool(c["flagged"]),
            "_youtube_flag_reason": c["reason"],
            "youtube_clip_start_seconds": clip,
            "spotify_id": None,
            "mood_tags": moods,
            "tiktok_viral": {"is_viral": False, "note": None, "year_of_virality": None},
            "sampled_by": [],
            "trivia_facts": trivia,
            "crossword_eligible": bool(re.match(r"^[A-Za-z0-9' .!?()&,/-]+$", title)),
            "difficulty": difficulty,
            "article_slug": SONG_ARTICLE_SLUGS.get(sid),
        }
        songs_json.append(rec)
        by_artist.setdefault(artist_id, []).append((sid, difficulty, year))

    # ---- artists.json ----
    artists_json = []
    artist_ids = set(a[0] for a in ARTISTS)
    for (aid, name, genre_ids, active, origin, bio) in ARTISTS:
        notable = [sid for (sid, _d, _y) in by_artist.get(aid, [])][:5]
        artists_json.append({
            "id": aid,
            "name": name,
            "genre_ids": genre_ids,
            "active_years": active,
            "origin": origin,
            "bio_short": bio,
            "notable_song_ids": notable,
            "article_slug": ARTIST_ARTICLE_SLUGS.get(aid),
        })

    # ---- genres.json ----
    # key_artist_ids: roster artists whose primary genre_ids include this genre
    artists_by_genre = {}
    for (aid, name, genre_ids, *_ ) in ARTISTS:
        for g in genre_ids:
            artists_by_genre.setdefault(g, []).append(aid)
    genres_json = []
    for (gid, gname, desc, sound, years) in GENRES:
        ka = artists_by_genre.get(gid, [])[:8]
        genres_json.append({
            "id": gid,
            "name": gname,
            "slug": gid,
            "description": desc,
            "defining_sound": sound,
            "years_active": years,
            "key_artist_ids": ka,
        })

    os.makedirs(OUT, exist_ok=True)
    json.dump(genres_json, open(os.path.join(OUT, "genres.json"), "w"), indent=2, ensure_ascii=False)
    json.dump(artists_json, open(os.path.join(OUT, "artists.json"), "w"), indent=2, ensure_ascii=False)
    json.dump(songs_json, open(os.path.join(OUT, "songs.json"), "w"), indent=2, ensure_ascii=False)

    # sanity: song artist_id referential note
    missing_ref = sorted(set(s["artist_id"] for s in songs_json) - artist_ids)
    print("\nDONE.")
    print("songs:", len(songs_json), "artists:", len(artists_json), "genres:", len(genres_json))
    print("flagged youtube:", sum(1 for s in songs_json if s["_youtube_flagged"]))
    print("non-roster artist_ids used by songs (expected, not in 70-roster):", len(missing_ref))

if __name__ == "__main__":
    main()
