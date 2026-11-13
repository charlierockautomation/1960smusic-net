#!/usr/bin/env python3
"""Build dist/: the ONLY folder Cloudflare deploys.

Copies tracked (git ls-files) public web files into dist/. Anything that is
not a web file type, or that lives in a PRIVATE_DIRS folder, is never copied,
so working files (.md notes, scripts, skills, docs, config) never reach the
live site. Fails the build if a private file would slip through.

New private/working files: never put them in dist/, and never give them a
web file type inside a public folder. Run locally with:
    python3 scripts/build_dist.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

PRIVATE_DIRS = {"docs", "gen", "worker", "scripts"}
PUBLIC_EXTS = {
    ".html", ".css", ".js", ".json", ".xml", ".txt", ".webmanifest",
    ".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".mp3", ".mp4",
}
PUBLIC_ROOT_FILES = {"_headers", "_redirects"}  # Cloudflare config files
# Belt and braces: these must never ship, whatever the rules above say.
FORBIDDEN_SUFFIXES = (".md", ".py", ".toml", ".docx", ".pdf", ".gz", ".env", ".sh")


def tracked_files():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, check=True).stdout
    return [f for f in out.decode().split("\0") if f]


def is_public(rel: str) -> bool:
    parts = rel.split("/")
    if parts[0] in PRIVATE_DIRS or parts[0] == "dist":
        return False
    if any(p.startswith(".") for p in parts):  # .gitignore, .claude/, .gitkeep...
        return False
    if len(parts) == 1 and rel in PUBLIC_ROOT_FILES:
        return True
    return Path(rel).suffix.lower() in PUBLIC_EXTS


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    copied = 0
    for rel in tracked_files():
        src = ROOT / rel
        if not src.is_file() or not is_public(rel):
            continue
        if rel.lower().endswith(FORBIDDEN_SUFFIXES):
            sys.exit(f"refusing to deploy private file: {rel}")
        dst = DIST / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
    if not (DIST / "index.html").exists():
        sys.exit("dist/index.html missing; build aborted")
    print(f"dist/: {copied} public files")


if __name__ == "__main__":
    main()
