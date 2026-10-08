# -*- coding: utf-8 -*-
"""One-off Playwright check for the /1960s/1968/ playlist player.
Run: python3 gen/test_playlist_player_1968.py
Copied from test_playlist_player_1967.py per docs/year-page-template.html's
"Testing" note: new PORT, new expected ids/positions, not made parametric.
"""
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

PORT = 8203
URL = f"http://localhost:{PORT}/1960s/1968/"


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
            if "Hey Jude" not in titles or "Judy in Disguise (With Glasses)" not in titles:
                errors.append("expected titles missing from table")

            page.click('tr[data-pp-yt="A_MjCqQoLLA"]')
            page.wait_for_timeout(9000)
            if current_id() != "A_MjCqQoLLA":
                errors.append(f"row click: expected A_MjCqQoLLA, got {current_id()}")
            if not any_request_for("A_MjCqQoLLA"):
                errors.append("row click: no real YouTube request seen for A_MjCqQoLLA")

            page.click("#pp-btn-next")
            page.wait_for_timeout(2500)
            if current_id() != "Y_tPE3o5NWk":
                errors.append(f"next: expected Y_tPE3o5NWk (row 2), got {current_id()}")

            page.click("#pp-btn-prev")
            page.wait_for_timeout(2500)
            if current_id() != "A_MjCqQoLLA":
                errors.append(f"prev: expected A_MjCqQoLLA (row 1), got {current_id()}")

            page.click('[data-pp-playall][data-pp-table="pp-table-1968"]')
            page.wait_for_timeout(2500)
            if current_id() != "A_MjCqQoLLA":
                errors.append(f"play all: expected A_MjCqQoLLA (row 1), got {current_id()}")
            counter = page.text_content("#pp-bar-counter")
            if "1 / 25" not in (counter or ""):
                errors.append(f"play all: counter should read 1 / 25, got {counter!r}")

            all_ids = set(r.get_attribute("data-pp-yt") for r in rows)
            page.click('[data-pp-shuffle][data-pp-table="pp-table-1968"]')
            page.wait_for_timeout(2500)
            if current_id() not in all_ids:
                errors.append(f"shuffle: playing id {current_id()} not in table's id set")

            search = page.query_selector('[data-pp-search][data-pp-table="pp-table-1968"]')
            search.fill("dock")
            page.wait_for_timeout(300)
            visible = [r for r in rows if "pp-hidden" not in (r.get_attribute("class") or "")]
            visible_titles = [r.get_attribute("data-pp-title") for r in visible]
            if visible_titles != ["(Sittin' On) The Dock of the Bay"]:
                errors.append(f"search 'dock': expected only Dock of the Bay visible, got {visible_titles}")
            search.fill("")

            page.wait_for_timeout(500)
            page.screenshot(path="/tmp/claude-1000/-home-natcharresources-1960smusic-net/b8e68fb6-8e8d-4958-8ab8-7004cb937201/scratchpad/pp-1968-test.png", full_page=False)
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
    print("PASS: all playlist player checks passed. Screenshot: /tmp/claude-1000/-home-natcharresources-1960smusic-net/b8e68fb6-8e8d-4958-8ab8-7004cb937201/scratchpad/pp-1968-test.png")


if __name__ == "__main__":
    main()
