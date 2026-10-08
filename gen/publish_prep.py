# -*- coding: utf-8 -*-
"""One command for the "once live" generated files (CLAUDE.md step 6).

Runs, in order: build_listings.py (static blog cards from posts.json),
generate_sitemap.py (every live page, real lastmod), generate_llms_txt.py,
then `check_article.py --site` to confirm sitemap.xml and llms.txt agree
with the pages on disk, then `validate_jsonld.py` on every page (any ERROR
blocks; WARNs print but pass). Commit the regenerated files with the tracker
updates, then ping IndexNow.

Usage: python3 gen/publish_prep.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ["build_listings.py"],
    ["generate_sitemap.py"],
    ["generate_llms_txt.py"],
    ["check_article.py", "--site"],
    ["validate_jsonld.py", "--all"],
]


def main():
    for step in STEPS:
        print(f"$ python3 gen/{' '.join(step)}")
        rc = subprocess.call([sys.executable, os.path.join(HERE, step[0])] + step[1:])
        if rc:
            print(f"FAILED: {step[0]} exited {rc}")
            return rc
    print("publish_prep OK: commit sitemap.xml, llms.txt, blog listings with the trackers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
