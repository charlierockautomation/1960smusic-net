# -*- coding: utf-8 -*-
"""One-off Playwright check for the /1960s/1960/ playlist player.
Run: python3 gen/test_playlist_player.py

Note: YT.Player replaces its target element with the actual <iframe>
(same behavior already documented in tools/radio/radio-player.js), so
"is a video loaded" is checked via PlaylistPlayer.getState() (our own
JS state, exposed as a page global) plus confirming the real YouTube
network request for that video id fired, not by reading iframe.src
(which stays a static base embed URL; the video swap happens over
postMessage, invisible to the DOM).
"""
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

PORT = 8199
URL = f"http://localhost:{PORT}/1960s/1960/"


def main():
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    errors = []
    console_errors = []
    yt_requests = set()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append(str(e)))
            page.on("request", lambda r: yt_requests.add(r.url) if "docid=" in r.url else None)
            page.goto(URL, wait_until="networkidle")

            def current_id():
                return page.evaluate("PlaylistPlayer.getState().song && PlaylistPlayer.getState().song.youtube_id")

            def any_request_for(vid):
                return any(f"docid={vid}" in u for u in yt_requests)

            rows = page.query_selector_all("tr[data-pp-yt]")
            if len(rows) != 25:
                errors.append(f"expected 25 rows, found {len(rows)}")
            titles = [r.get_attribute("data-pp-title") for r in rows]
            if any(not t or t.strip() in ("", "2026") for t in titles):
                errors.append(f"bad/blank titles in rows: {titles}")
            if "Theme from A Summer Place" not in titles or "Walk Don't Run" not in titles:
                errors.append("expected titles missing from table")

            page.click('tr[data-pp-yt="WvjuQaEBUoo"]')
            page.wait_for_timeout(4000)
            if current_id() != "WvjuQaEBUoo":
                errors.append(f"row click: expected WvjuQaEBUoo, got {current_id()}")
            if not any_request_for("WvjuQaEBUoo"):
                errors.append("row click: no real YouTube request seen for WvjuQaEBUoo")

            page.click("#pp-btn-next")
            page.wait_for_timeout(2500)
            if current_id() != "NtHZP3U3nE8":
                errors.append(f"next: expected NtHZP3U3nE8 (row 4), got {current_id()}")

            page.click("#pp-btn-prev")
            page.wait_for_timeout(2500)
            if current_id() != "WvjuQaEBUoo":
                errors.append(f"prev: expected WvjuQaEBUoo (row 3), got {current_id()}")

            page.click('[data-pp-playall][data-pp-table="pp-table-1960"]')
            page.wait_for_timeout(2500)
            if current_id() != "tSsiS-v6_6M":
                errors.append(f"play all: expected tSsiS-v6_6M (row 1), got {current_id()}")
            counter = page.text_content("#pp-bar-counter")
            if "1 / 25" not in (counter or ""):
                errors.append(f"play all: counter should read 1 / 25, got {counter!r}")

            all_ids = set(r.get_attribute("data-pp-yt") for r in rows)
            page.click('[data-pp-shuffle][data-pp-table="pp-table-1960"]')
            page.wait_for_timeout(2500)
            if current_id() not in all_ids:
                errors.append(f"shuffle: playing id {current_id()} not in table's id set")

            search = page.query_selector('[data-pp-search][data-pp-table="pp-table-1960"]')
            search.fill("twist")
            page.wait_for_timeout(300)
            visible = [r for r in rows if "pp-hidden" not in (r.get_attribute("class") or "")]
            visible_titles = [r.get_attribute("data-pp-title") for r in visible]
            if visible_titles != ["The Twist"]:
                errors.append(f"search 'twist': expected only The Twist visible, got {visible_titles}")
            search.fill("")

            page.wait_for_timeout(500)
            page.screenshot(path="/tmp/pp-1960-test.png", full_page=False)
            browser.close()
    finally:
        server.terminate()
        server.wait()

    if console_errors:
        errors.append(f"console errors during test: {console_errors}")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("PASS: all playlist player checks passed. Screenshot: /tmp/pp-1960-test.png")


if __name__ == "__main__":
    main()
