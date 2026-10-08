# Phase 2 — Decade Spine (Oct 12 - Nov 8, 2026)

Active work queue for Phase 2 of the Sep 2026 strategy
(`docs/strategy-review-2026-09.md`). Phase 1 (`docs/phase1-foundations.md`)
closed out 2026-09-29: all 10 tasks live. **Phase 2 tasks run BEFORE new
`docs/content-build.md` rows**, same precedence rule as Phase 1. The On
This Day daily minimum continues in parallel on its own track.

Rules that still apply: CLAUDE.md in full (No Hallucination, YouTube
Embed Rule, no subagents, multiple tasks per session allowed if each is
closed out cleanly before the next starts, Charlie approves before any
push to `main`, 195-line file ceiling, competitor research before
writing per `docs/writing-standard.md`). Work the first task whose
status is `not started`.

Status values: `not started` · `in progress` · `blocked (reason)` · `live`

## Open blocker: keyword volumes unverified

Strategy review flagged year-page keyword volumes (1960-1969) as
**not yet verified**. Attempted verification 2026-09-29 via the
DataForSEO MCP tools (`dataforseo_labs_google_keyword_overview`,
`kw_data_google_ads_search_volume`): both returned HTTP 402 (no credits
on the connected account). Task 1 below proceeds on the existing
WordStream-verified clusters only (see `strategy-review-2026-09.md`
baseline data); per-year search volume is not part of any page's
published claims, so this blocks planning confidence, not the no-
hallucination rule. Re-attempt verification once DataForSEO access is
restored, and note the result here either way.

## Tasks

| # | Task | Status |
|---|---|---|
| 1 | Year page template + schema design | live |
| 2 | Year page: 1960 | live |
| 3 | Year page: 1961 | live |
| 4 | Year page: 1962 | live |
| 5 | Year page: 1963 | live |
| 6 | Year page: 1964 | live |
| 7 | Year page: 1965 | live |
| 8 | Year page: 1966 | live |
| 9 | Year page: 1967 | live |
| 10 | Year page: 1968 | not started |
| 11 | Year page: 1969 | not started |
| 12 | Best 60s Songs list page (/best-60s-songs/) | not started |
| 13 | 60s Rock umbrella hub (/blog/genres/60s-rock/) | not started |
| 14 | Tool intro copy (7 tools, 200-400 words each, crawlable) | not started |
| 15 | Homepage rebuild (full pillar copy, not just Phase 1's static links) | not started |
| 16 | `/1960s/` hub page (year index + genre hub links) | live |

## Task detail

### 1. Year page template + schema design
Done: shell built at `docs/year-page-template.html`. Full spec (sections,
schema, radio-year filter build) moved to
[`docs/phase2-decade-spine-archive.md`](phase2-decade-spine-archive.md)
to keep this file under the line ceiling. One update since archiving:
the BreadcrumbList was originally 2-level (Home > Year, "no mid-tier
hub exists yet"); task 16 added that hub, so it's 3-level now (Home >
1960s > Year) on every year page, template included.

### 2-11. Year pages 1960-1969
Build one at a time, in year order, using the task-1 template. Each is
its own row so a partial build never blocks the next; check_article.py
gate + Charlie's go-ahead before push, same as every other content
type. 1960-1964 build notes (playlist player's 3 iterations, the
`data-year` collision bug, sourcing approach) moved to
[`docs/phase2-decade-spine-archive.md`](phase2-decade-spine-archive.md)
to keep this file under the line ceiling.

`/1960s/1965/` live 2026-10-08, 1689 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1965 (tracklist; cross-verified
against billboardtop100of.com) plus the chronological number-ones
list (27 titles, dates/weeks cross-checked against de.wikipedia; no
total stated since en/de disagree 26 vs 27). Wooly Bully is year-end
No. 1 but peaked No. 2, used as the lead hook. All 25 YouTube ids
resolved (3 cached, 22 via scraper, This Diamond Ring on a retry) and
verified embeddable, not made-for-kids, in one batched call. Links all
7 eligible hubs. Featured image is a real CC BY 4.0 photo of the Rolling
Stones in Finland, June 25 1965 (Finnish Heritage Agency, via Wikimedia
Commons). Notable Events links OTD Sep 4, Sep 12, Oct 9. Playwright
self-test (`gen/test_playlist_player_1965.py`) PASS.

`/1960s/1966/` live 2026-10-08, 1694 words, check_article.py PASS.
Billboard year-end top 25 of 1966 uses Billboard's REVISED ranking
(Green Berets No. 1; billboardtop100of.com full list, Billboard's
revision confirmed by AOL and Wikipedia's Green Berets article). The
original Dec 24 1966 printed list (Wikipedia) ranks California
Dreamin' first and Green Berets tenth; the page says so in an h3.
Billboard's own page returned HTTP 402. Chronological number-ones list
(27 titles, weeks cross-checked against rogerogreen.com). All 25
YouTube ids resolved (6 cached, 19 via scraper) and verified
embeddable, not made-for-kids, in one batched call; several carry the
usual acceptable-if-compliant `yt` flag. Links 7 hubs (no country-60s,
no verified 1966 tie). Featured image: CBS publicity photo of the
Supremes on Ed Sullivan, 1966, public domain via Wikimedia Commons.
Notable Events links OTD Sep 3, 12, 21, 24, Oct 15 (Sep 10 in albums
bullet text only, no link). Playwright self-test PASS.

`/1960s/1967/` live 2026-10-08, 1554 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1967 (Wikipedia, cross-checked
against billboardtop100of.com; To Sir With Love No. 1) plus the
chronological number-ones list (19 songs; weeks derived from the
Wikipedia issue-date ranges, no independent second source found).
Peaks for non-number-ones from Wikipedia's top-ten list, Come Back
When You Grow Up confirmed No. 3 by search. All 25 YouTube ids
verified embeddable, not made-for-kids, in one batched call; two
scraper picks were live versions (Ode to Billie Joe, I Think We're
Alone Now) and were swapped for studio Topic uploads. Flagged `yt`:
I'm a Believer, Happy Together, Groovin', Incense and Peppermints.
Links 6 hubs (no country-60s, no folk-rock: no verified tie). Featured
image: public-domain Aretha Franklin photo from a July 15 1967
Atlantic trade ad in Billboard, via Wikimedia Commons. Velvet
Underground and Forever Changes dates left at month level (sources
disagree / single source). Notable Events links OTD Sep 17, 18, 23,
Oct 14. Playwright self-test (`gen/test_playlist_player_1967.py`) PASS.

### 12. Best 60s Songs list page
`/best-60s-songs/`: 100 songs pulled from `data/songs.json` (extend the
dataset first if it doesn't yet cover 100), each with year, genre,
one-line why-it-matters, embedded player, link to its song story where
one exists. Targets "60s songs" / "60s music hits" clusters.

### 13. 60s Rock umbrella hub
`/blog/genres/60s-rock/`: links down to British Invasion, Garage &
Surf, Psychedelic Rock hubs. Add to CLAUDE.md's Genre Hub Linking list
the same commit it goes live, per that section's existing rule.

### 14. Tool intro copy
200-400 words of crawlable text on each of the 7 tool pages (radio,
daily, trivia, quiz, playlist-builder, random-song,
60s-music-crossword), targeting tool-specific queries ("60s music
trivia", "60s radio"). Not a redesign, just adds real body copy above
or beside the existing interactive markup.

### 15. Homepage rebuild
Full pillar copy rewrite (Phase 1 task 2 only added static crawlable
links/tools/latest-blog block, explicitly deferred the copy rewrite to
here). Scope this once tasks 1-13 are live, since the rebuilt homepage
should link to the year spine and the new hubs/list page.

### 16. `/1960s/` hub page
Not in the original task 1-15 scoping; gap found 2026-09-29 while
rebuilding `/1960s/1961/`: neither live year page was linked from the
homepage, blog, or any index, and `/1960s/` itself 404'd. Homepage
links were correctly deferred to task 15, but no task ever covered a
plain index of the year pages themselves.

Done: static hub at `/1960s/` (year-guide cards for live years, "Coming
Soon" cards, no link, for years not yet built; a second grid linking
every live genre hub). Not an article type, doesn't run
`check_article.py` (same as `/blog/genres/` and `/blog/on-this-day/`).
Added to `gen/generate_sitemap.py` STATIC_PAGES and `link-map.md`.
Every live year page's breadcrumb (nav + schema) routes through it.
Added a small static "1960s music, year by year" section to the
homepage linking to the hub and live years, ahead of task 15's full
rebuild, so the pages aren't orphaned until then. Tracker discipline
below covers moving each new year's card off "Coming Soon" as it
ships (1962's card moved 2026-09-30).

## Tracker discipline for every new year page

Every year page pushed to `main`, task 16 hub included, updates all of
the following in the same push, not a follow-up session: `sitemap.xml`
(via `gen/generate_sitemap.py`, after adding the path to
`STATIC_PAGES`), `link-map.md` (new row, live URL, up/across links),
the `/1960s/` hub (its year-guide grid: move the card from "Coming
Soon" to a live link), and the homepage's "1960s music, year by year"
grid in `index.html` (add the new year's card; missed for 1964 on the
first push, fixed the same day). This rule exists because task 3 shipped without
any of the first three the first time.

## Gate 2 (target Nov 8)
All 10 year pages and the Best 60s Songs list are live and linked from
every existing On This Day page whose date falls in that year. Then
Phase 3 (`docs/strategy-review-2026-09.md` roadmap: queue rotation,
monthly data page, weekly Trending, weekly refresh) begins.
