# -*- coding: utf-8 -*-
"""Playwright check for /best-60s-songs/: row count, row click, Play All,
Shuffle, search, year + genre filters, Play All limited to visible rows.
Run: python3 gen/test_best_60s_songs.py
"""
import sys, time, subprocess
from playwright.sync_api import sync_playwright

PORT = 8205
URL = f"http://localhost:{PORT}/best-60s-songs/"
T = '[data-pp-table="pp-table-best"]'


def main():
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    errors, console_errors, reqs = [], [], set()
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page(viewport={"width": 1280, "height": 900})
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append(str(e)))
            page.on("request", lambda r: reqs.add(r.url) if "docid=" in r.url else None)
            page.goto(URL, wait_until="networkidle")
            cur = lambda: page.evaluate("PlaylistPlayer.getState().song && PlaylistPlayer.getState().song.youtube_id")
            rows = page.query_selector_all("tr[data-pp-yt]")
            if len(rows) != 100:
                errors.append(f"expected 100 rows, got {len(rows)}")
            if any(not (r.get_attribute("data-pp-title") or "").strip() for r in rows):
                errors.append("blank title in a row")
            first = rows[0].get_attribute("data-pp-yt")
            page.click(f'tr[data-pp-yt="{first}"] .pp-play-cell')
            page.wait_for_timeout(8000)
            if cur() != first:
                errors.append(f"row click: expected {first}, got {cur()}")
            if not any(f"docid={first}" in u for u in reqs):
                errors.append("row click: no YouTube request for first row")
            page.click("#pp-btn-next"); page.wait_for_timeout(2500)
            if cur() != rows[1].get_attribute("data-pp-yt"):
                errors.append("next did not reach row 2")

            def visible():
                return [r.get_attribute("data-pp-title") for r in rows
                        if "pp-hidden" not in (r.get_attribute("class") or "")]
            # search
            page.fill(f'[data-pp-search]{T}', "wipe out"); page.wait_for_timeout(300)
            if visible() != ["Wipe Out"]:
                errors.append(f"search: {visible()}")
            page.fill(f'[data-pp-search]{T}', "")
            # year filter
            page.select_option(f'[data-pp-filter="year"]{T}', "1969"); page.wait_for_timeout(300)
            v = visible()
            if len(v) != 5 or "Sugar, Sugar" not in v:
                errors.append(f"year 1969: {v}")
            status = page.text_content("[data-pp-filter-status]")
            if "Showing 5 of 100" not in status:
                errors.append(f"status text: {status!r}")
            ids69 = {r.get_attribute("data-pp-yt") for r in rows if "pp-hidden" not in (r.get_attribute("class") or "")}
            page.click(f'[data-pp-playall]{T}'); page.wait_for_timeout(2500)
            if cur() not in ids69:
                errors.append(f"Play All with 1969 filter played {cur()} outside filter")
            if "1 / 5" not in (page.text_content("#pp-bar-counter") or ""):
                errors.append(f"counter: {page.text_content('#pp-bar-counter')!r}")
            # genre + year combined
            page.select_option(f'[data-pp-filter="genre"]{T}', "folk-rock"); page.wait_for_timeout(300)
            v = visible()
            if sorted(v) != ["The Boxer"]:
                errors.append(f"1969+folk-rock: {v}")
            page.click(f'[data-pp-shuffle]{T}'); page.wait_for_timeout(2500)
            ids = {r.get_attribute("data-pp-yt") for r in rows if "pp-hidden" not in (r.get_attribute("class") or "")}
            if cur() not in ids:
                errors.append("shuffle played outside filter")
            # reset
            page.select_option(f'[data-pp-filter="year"]{T}', ""); page.select_option(f'[data-pp-filter="genre"]{T}', "")
            page.wait_for_timeout(300)
            if len(visible()) != 100:
                errors.append("reset did not restore 100 rows")
            page.screenshot(path="/tmp/claude-1000/-home-natcharresources-1960smusic-net/d49eabdb-8ead-4242-95ae-43f61a573016/scratchpad/best60.png")
            page.set_viewport_size({"width": 400, "height": 800})
            if page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"):
                errors.append("horizontal page scroll at 400px")
            b.close()
    finally:
        server.terminate(); server.wait()
    if console_errors:
        errors.append(f"console errors: {console_errors}")
    print("FAIL" if errors else "PASS")
    for e in errors:
        print(" -", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
