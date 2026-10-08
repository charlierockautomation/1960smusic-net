# -*- coding: utf-8 -*-
"""Post-push check (CLAUDE.md pipeline step 6): confirm each new URL is live.

For every URL: HTTP 200 on production, listed in the LIVE sitemap.xml, and
(for /blog/ posts, which llms.txt covers) listed in the LIVE llms.txt.
Exit 1 on any miss. Run after Cloudflare's build finishes (retry in a minute
if a URL 404s right after the push).

Usage: python3 gen/verify_live.py /blog/songs/foo-bar/ [...]
       python3 gen/verify_live.py --last-commit   (index.html pages changed in HEAD)
"""
import re
import subprocess
import sys
import urllib.request

BASE = "https://1960smusic.net"


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "1960smusic-verify-live"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except OSError as e:
        return 0, str(e)


def last_commit_urls():
    out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", "HEAD~1", "HEAD"],
                         capture_output=True, text=True).stdout.split()
    return ["/" + f[: -len("index.html")] for f in out if f.endswith("/index.html") and not f.startswith(("gen/", "docs/"))]


def main(argv):
    urls = last_commit_urls() if argv == ["--last-commit"] else argv
    if not urls:
        print("usage: verify_live.py <path> [...] | --last-commit")
        return 2
    _, sitemap = fetch("/sitemap.xml")
    _, llms = fetch("/llms.txt")
    bad = False
    for u in urls:
        status, _ = fetch(u)
        in_sitemap = f"<loc>{BASE}{u}</loc>" in sitemap
        needs_llms = bool(re.match(r"^/blog/(artists|songs|genres|trending|on-this-day)/[^/]+/$", u))
        in_llms = f"({BASE}{u})" in llms if needs_llms else None
        ok = status == 200 and in_sitemap and in_llms is not False
        bad |= not ok
        llms_txt = "n/a" if in_llms is None else ("yes" if in_llms else "NO")
        print(f"{'OK  ' if ok else 'FAIL'} {u}  http={status} sitemap={'yes' if in_sitemap else 'NO'} llms={llms_txt}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
