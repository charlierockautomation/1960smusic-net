# -*- coding: utf-8 -*-
"""One-off Playwright check for the /1960s/1967/ playlist player.
Run: python3 gen/test_playlist_player_1967.py
Copied from test_playlist_player_1966.py per docs/year-page-template.html's
"Testing" note: new PORT, new expected ids/positions, not made parametric.
"""
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

PORT = 8202
URL = f"http://localhost:{PORT}/1960s/1967/"


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
            if "To Sir With Love" not in titles or "It Must Be Him" not in titles:
                errors.append("expected titles missing from table")

            page.click('tr[data-pp-yt="0_UpW8V6B3c"]')
            page.wait_for_timeout(9000)
            if current_id() != "0_UpW8V6B3c":
                errors.append(f"row click: expected 0_UpW8V6B3c, got {current_id()}")
            if not any_request_for("0_UpW8V6B3c"):
                errors.append("row click: no real YouTube request seen for 0_UpW8V6B3c")

            page.click("#pp-btn-next")
            page.wait_for_timeout(2500)
            if current_id() != "HIWY8UyW9bw":
                errors.append(f"next: expected HIWY8UyW9bw (row 2), got {current_id()}")

            page.click("#pp-btn-prev")
            page.wait_for_timeout(2500)
            if current_id() != "0_UpW8V6B3c":
                errors.append(f"prev: expected 0_UpW8V6B3c (row 1), got {current_id()}")

            page.click('[data-pp-playall][data-pp-table="pp-table-1967"]')
            page.wait_for_timeout(2500)
            if current_id() != "0_UpW8V6B3c":
                errors.append(f"play all: expected 0_UpW8V6B3c (row 1), got {current_id()}")
            counter = page.text_content("#pp-bar-counter")
            if "1 / 25" not in (counter or ""):
                errors.append(f"play all: counter should read 1 / 25, got {counter!r}")

            all_ids = set(r.get_attribute("data-pp-yt") for r in rows)
            page.click('[data-pp-shuffle][data-pp-table="pp-table-1967"]')
            page.wait_for_timeout(2500)
            if current_id() not in all_ids:
                errors.append(f"shuffle: playing id {current_id()} not in table's id set")

            search = page.query_selector('[data-pp-search][data-pp-table="pp-table-1967"]')
            search.fill("windy")
            page.wait_for_timeout(300)
            visible = [r for r in rows if "pp-hidden" not in (r.get_attribute("class") or "")]
            visible_titles = [r.get_attribute("data-pp-title") for r in visible]
            if visible_titles != ["Windy"]:
                errors.append(f"search 'cherish': expected only Windy visible, got {visible_titles}")
            search.fill("")

            page.wait_for_timeout(500)
            page.screenshot(path="/tmp/claude-1000/-home-natcharresources-1960smusic-net/e9f3a3cb-b46e-41fa-8dd4-e004d5a1f6a3/scratchpad/pp-1967-test.png", full_page=False)
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
    print("PASS: all playlist player checks passed. Screenshot: /tmp/claude-1000/-home-natcharresources-1960smusic-net/e9f3a3cb-b46e-41fa-8dd4-e004d5a1f6a3/scratchpad/pp-1967-test.png")


if __name__ == "__main__":
    main()
