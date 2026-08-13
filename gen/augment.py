# -*- coding: utf-8 -*-
"""QA pass: for each resolved YouTube id, fetch oEmbed to capture the actual
video title + channel, then apply a source-confidence flag. A song is flagged
for human spot-check when the hosting channel is not an obviously official
source (VEVO / '- Topic' / 'Official' / contains an artist-name token)."""
import json, re, time, os, urllib.parse, urllib.request
from songs_data import SONGS

CACHE = os.path.join(os.path.dirname(__file__), "yt_cache.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
STOP = {"the","and","his","her","band","experience","tijuana","brass","featuring",
        "feat","with","of","pharaohs","miracles","vandellas","seasons","tops",
        "supremes","del-tones","shondells","gordon","dean","sham","mysterians"}

def norm(s):
    s = (s or "").lower().replace("&","and")
    s = re.sub(r"[^a-z0-9 ]+"," ",s)
    return re.sub(r"\s+"," ",s).strip()

def http_get(url,t=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=t) as r:
        return r.read().decode("utf-8","ignore")

def oembed(vid):
    url=("https://www.youtube.com/oembed?url="+
         urllib.parse.quote("https://www.youtube.com/watch?v="+vid)+"&format=json")
    try:
        return json.loads(http_get(url))
    except Exception:
        return None

cache=json.load(open(CACHE))
name_by_key={f"{s[1]}|||{s[0]}":(s[0],s[1]) for s in SONGS}

flagged=0
for i,(key,rec) in enumerate(cache.items()):
    vid=rec.get("youtube_id")
    title,artist=name_by_key.get(key,("",""))[0],name_by_key.get(key,("",""))[1]
    if not vid:
        rec["flagged"]=True
        rec["reason"]=rec.get("reason") or "No video id resolved."
        flagged+=1; continue
    if "author" not in rec:
        d=oembed(vid); time.sleep(0.12)
        rec["video_title"]=(d or {}).get("title")
        rec["author"]=(d or {}).get("author_name")
        rec["live_ok"]=bool(d)
    author=rec.get("author") or ""
    vtitle=rec.get("video_title") or ""
    an=norm(author)
    atoks=[w for w in norm(artist).split() if len(w)>2 and w not in STOP]
    official = (author.endswith("VEVO") or author.endswith("- Topic") or "topic" in an
                or "official" in an or any(t in an for t in atoks))
    if not rec.get("live_ok",True):
        rec["flagged"]=True
        rec["reason"]=("oEmbed could not confirm the video is live/embeddable; "
                       "best-effort ID \u2014 verify manually.")
        flagged+=1
    elif not official:
        rec["flagged"]=True
        rec["reason"]=(f"Auto-selected upload is live and title-matched, but the hosting "
                       f"channel ('{author}') is not an obviously official source "
                       f"(VEVO/Topic/artist channel) \u2014 verify it is an acceptable copy.")
        flagged+=1
    else:
        rec["flagged"]=False
        rec["reason"]=None
    json.dump(cache,open(CACHE,"w"),indent=1)

print("augment done. flagged:",flagged,"/",len(cache))
