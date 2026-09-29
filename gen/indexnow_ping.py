# -*- coding: utf-8 -*-
"""Ping IndexNow (Bing, and any other participating engine) with changed URLs.

One shared key file lives at the site root (see KEY_FILE below) and is
served as a public static asset; IndexNow verifies submissions against it.
Never regenerate the key or the key file without updating both together.

Usage:
    python3 gen/indexnow_ping.py <url> [url ...]
    python3 gen/indexnow_ping.py --sitemap   # submit every URL in sitemap.xml

URLs may be given as full https://1960smusic.net/... links or as bare
site-relative paths (e.g. /blog/genres/folk-rock/).

Run this after pushing to main, for whatever pages actually changed in
that push (new article, tracker-driven listing rebuild, etc.). This is
Phase 1 task 10 in docs/phase1-foundations.md.
"""
import json
import re
import sys
import urllib.request

HOST = "1960smusic.net"
BASE = f"https://{HOST}"
KEY = "2fa326ab1a737bf065e8eea8dd3c1fb4"
KEY_LOCATION = f"{BASE}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"


def normalize(url):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return BASE + (url if url.startswith("/") else "/" + url)


def urls_from_sitemap():
    text = open("sitemap.xml", encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", text)


def ping(urls):
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        print(f"IndexNow: HTTP {resp.status} for {len(urls)} URL(s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "--sitemap":
        submit = urls_from_sitemap()
    else:
        submit = [normalize(u) for u in sys.argv[1:]]
    ping(submit)
