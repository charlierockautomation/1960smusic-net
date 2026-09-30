# -*- coding: utf-8 -*-
"""Playwright check for the pp-table-scroll fix (inner-scrolling tracklist,
sticky header, fade cue, active-row auto-scroll via scrollTop, player-bar
body padding). Covers /1960s/1961/ at desktop and mobile widths; also
smoke-checks /1960s/1960/ carries the same markup since both share the
one playlist-player.css/js engine.
Run: python3 gen/test_playlist_scroll.py
"""
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

PORT = 8197
BASE = f"http://localhost:{PORT}"


def main():
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()

            # --- 1960: same markup present (shared engine smoke check) ---
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto(f"{BASE}/1960s/1960/", wait_until="networkidle")
            box = page.query_selector(".pp-table-scroll")
            if not box:
                errors.append("1960: .pp-table-scroll wrapper missing")
            elif not page.query_selector(".pp-table-scroll .pp-table-fade"):
                errors.append("1960: .pp-table-fade missing")
            page.close()

            # --- 1961: full behavior check, desktop ---
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto(f"{BASE}/1960s/1961/", wait_until="networkidle")

            box = page.query_selector(".pp-table-scroll")
            if not box:
                errors.append("1961: .pp-table-scroll wrapper missing")

            box_h = page.evaluate("document.querySelector('.pp-table-scroll').clientHeight")
            scroll_h = page.evaluate("document.querySelector('.pp-table-scroll').scrollHeight")
            if not (400 <= box_h <= 520):
                errors.append(f"desktop: box clientHeight {box_h}, expected ~480px")
            if scroll_h <= box_h:
                errors.append(f"desktop: scrollHeight {scroll_h} not taller than box {box_h}, list isn't clamped")

            sticky_pos = page.evaluate(
                "getComputedStyle(document.querySelector('.pp-table-scroll thead th')).position"
            )
            if sticky_pos != "sticky":
                errors.append(f"desktop: thead th position is {sticky_pos!r}, expected sticky")

            # Page scroll: wheel over the header (outside the box) moves the page.
            page.mouse.move(640, 60)
            before_page_scroll = page.evaluate("window.scrollY")
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(200)
            after_page_scroll = page.evaluate("window.scrollY")
            if after_page_scroll <= before_page_scroll:
                errors.append(f"page did not scroll on wheel over header: {before_page_scroll} -> {after_page_scroll}")

            # Scroll the box into view, then wheel over it: box scrolls, not the page.
            box.scroll_into_view_if_needed()
            box_rect = box.bounding_box()
            page.mouse.move(box_rect["x"] + box_rect["width"] / 2, box_rect["y"] + box_rect["height"] / 2)
            page_scroll_before = page.evaluate("window.scrollY")
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(200)
            box_scroll_top = page.evaluate("document.querySelector('.pp-table-scroll').scrollTop")
            page_scroll_after = page.evaluate("window.scrollY")
            if box_scroll_top <= 0:
                errors.append("wheel over box did not move box.scrollTop")
            if page_scroll_after != page_scroll_before:
                errors.append(f"page scrolled while wheeling over box: {page_scroll_before} -> {page_scroll_after}")

            # Click a row far down the list, confirm auto-scroll (scrollTop moves)
            # without the page itself jumping (scrollIntoView would move the page).
            page.evaluate("document.querySelector('.pp-table-scroll').scrollTop = 0")
            page_scroll_before_click = page.evaluate("window.scrollY")
            page.click('tr[data-pp-yt="z5H6iwQGWl4"]')  # row 25, The Boll Weevil Song
            page.wait_for_timeout(500)
            scroll_after_click = page.evaluate("document.querySelector('.pp-table-scroll').scrollTop")
            page_scroll_after_click = page.evaluate("window.scrollY")
            if scroll_after_click <= 0:
                errors.append("clicking a far-down row did not auto-scroll the box")
            if page_scroll_after_click != page_scroll_before_click:
                errors.append("clicking a far-down row moved the page (scrollIntoView side effect suspected)")

            # Row is now visible inside the box's viewport.
            row_visible = page.evaluate("""
                (function(){
                  var box = document.querySelector('.pp-table-scroll');
                  var tr = document.querySelector('tr[data-pp-yt="z5H6iwQGWl4"]');
                  var cTop = box.scrollTop, cBottom = cTop + box.clientHeight;
                  return tr.offsetTop >= cTop && (tr.offsetTop + tr.offsetHeight) <= cBottom;
                })()
            """)
            if not row_visible:
                errors.append("active row not fully within scroll box viewport after auto-scroll")

            # Player bar visible -> body has matching bottom padding.
            page.wait_for_timeout(1500)
            bar_h = page.evaluate("document.querySelector('.pp-bar').offsetHeight")
            body_pad = page.evaluate("parseInt(getComputedStyle(document.body).paddingBottom)")
            if body_pad != bar_h:
                errors.append(f"body padding-bottom {body_pad} != bar height {bar_h}")

            # Play All lands back on row 1, which should be back in view (scrollTop ~0).
            page.click('[data-pp-playall][data-pp-table="pp-table-1961"]')
            page.wait_for_timeout(2500)
            scroll_after_playall = page.evaluate("document.querySelector('.pp-table-scroll').scrollTop")
            if scroll_after_playall > 5:
                errors.append(f"Play All: row 1 active but box.scrollTop is {scroll_after_playall}, expected ~0")

            # Search still filters rows inside the box.
            search = page.query_selector('[data-pp-search][data-pp-table="pp-table-1961"]')
            search.fill("boll")
            page.wait_for_timeout(300)
            visible_rows = page.query_selector_all('tr[data-pp-yt]:not(.pp-hidden)')
            visible_titles = [r.get_attribute('data-pp-title') for r in visible_rows]
            if visible_titles != ["The Boll Weevil Song"]:
                errors.append(f"search inside scroll box: expected only Boll Weevil visible, got {visible_titles}")
            search.fill("")

            page.screenshot(path="/tmp/pp-scroll-desktop.png", full_page=False)
            page.close()

            # --- 1961: mobile width (375px) ---
            page = browser.new_page(viewport={"width": 375, "height": 800})
            page.goto(f"{BASE}/1960s/1961/", wait_until="networkidle")
            box_h_m = page.evaluate("document.querySelector('.pp-table-scroll').clientHeight")
            viewport_h = page.evaluate("window.innerHeight")
            expected_60vh = viewport_h * 0.6
            if not (expected_60vh * 0.85 <= box_h_m <= expected_60vh * 1.15):
                errors.append(f"mobile: box clientHeight {box_h_m}, expected ~60vh ({expected_60vh:.0f})")
            page.click('tr[data-pp-yt="z5H6iwQGWl4"]')
            page.wait_for_timeout(500)
            mobile_scroll_top = page.evaluate("document.querySelector('.pp-table-scroll').scrollTop")
            if mobile_scroll_top <= 0:
                errors.append("mobile: clicking a far-down row did not auto-scroll the box")
            page.screenshot(path="/tmp/pp-scroll-mobile.png", full_page=False)
            page.close()

            browser.close()
    finally:
        server.terminate()
        server.wait()

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("PASS: scroll-box, sticky header, fade, auto-scroll, body padding, search all verified.")
    print("Screenshots: /tmp/pp-scroll-desktop.png, /tmp/pp-scroll-mobile.png")


if __name__ == "__main__":
    main()
