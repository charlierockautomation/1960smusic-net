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
| 4 | Year page: 1962 | not started |
| 5 | Year page: 1963 | not started |
| 6 | Year page: 1964 | not started |
| 7 | Year page: 1965 | not started |
| 8 | Year page: 1966 | not started |
| 9 | Year page: 1967 | not started |
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
type.

Done: `/1960s/1960/` live 2026-09-29, 1349 words, check_article.py PASS
(this run set the "year page" word-count range to 1100-1700). All 19
Billboard Hot 100 number ones of 1960 verified against two independent
sources, one discrepancy resolved (Are You Lonesome Tonight, 6 weeks
total, Nov 28 1960 to Jan 9 1961). Featured image is a real 1964
Wikimedia Commons photo of Chubby Checker (public domain, correctly
dated in the caption, not claimed as a 1960 photo). Links up to 3 live
genre hubs (garage-surf-rock, country-60s, pop-brill-building) via
songs already in the dataset, and to the one live OTD page for 1960
with a direct music tie (`/blog/on-this-day/october-1/`, Joan Baez's
debut album). Not a `posts.json`/`build_listings.py` entry, that
pipeline is blog-only; added directly to `gen/generate_sitemap.py`'s
`STATIC_PAGES` instead, and to `link-map.md`.

Charlie's call 2026-09-29: added a "Listen to `<year>` Music" section
right after the lead (before the image) on every year page, so readers
can play the songs being discussed without leaving the page. Took
three tries to get right; the working version and the reasons the
first two failed are now the standing spec in
`docs/year-page-template.html`'s "Playlist player" section. Summary:

1. First attempt stacked 3 full-size static iframes (one per
   genre-shift anchor song, reusing already-cached ids since the
   YouTube API quota looked exhausted that day). Charlie rejected it as
   thin and slow, and asked for one reusable playlist player instead,
   modeled on musicofthe80s.com's sticky player and a 70s-site table
   pattern, expanded to 20-30 songs per year with fresh chart-backed
   sourcing.
2. Second attempt built that player (`/assets/js/playlist-player*.js`,
   `/assets/css/playlist-player.css`, ported from
   musicofthe80s.com's cassette-player.tsx/player-context.tsx) but
   shipped broken: the tracklist `<tr>` rows used a plain `data-year`
   attribute, which collided with `site.js`'s site-wide
   `[data-year]` footer-copyright selector and wiped every row's
   content to the current year on load.
3. Third attempt fixed the collision (everything renamed to namespaced
   `data-pp-*` attributes) and expanded to the real target: all 25
   songs from Billboard's Year-End Hot 100 top 25 of 1960, 4 ids
   already cached, 21 more found via `generate.py`'s existing no-API
   scraper and verified in one batched `videos.list` call (quota was
   not actually exhausted, 1 call used). Also wrote
   `gen/test_playlist_player.py` (Playwright) after a second real bug
   turned up on inspection, not just the reported one: the Play
   All/Shuffle/search controls had the right CSS classes but were
   missing the `data-pp-playall`/`data-pp-shuffle`/`data-pp-search`
   marker attributes `playlist-table.js` actually queries for, so they
   silently did nothing. The test now catches exactly that class of
   bug before a page ships.

Live on `/1960s/1960/` 2026-09-29, 1700 words, PASS. Tasks 4-11 build
the playlist player from the start per the template.

`/1960s/1961/` rebuilt 2026-09-29 to match: was still the old 3-embed
version from attempt 1 (shipped before the redesign request). Replaced
with the full 25-song playlist player, Billboard Year-End Hot 100 top
25 of 1961 (cross-verified against a second source), all 25 YouTube
ids resolved via `generate.py`'s no-API scraper and verified embeddable
plus not made-for-kids in one batched `yt_video_status.py` call. One id
(Will You Love Me Tomorrow) is hosted by a non-obviously-official
channel, same acceptable-if-compliant call as the `yt`-flagged rows in
`content-build.md`. `gen/check_article.py` PASS at 1594 words; Playwright
self-test (`gen/test_playlist_player_1961.py`, copied per-year per the
template's testing note) PASS. This rebuild is also what surfaced task
16 below: the page existed with no working path back to it from the
homepage or any index.

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

Done: static hub at `/1960s/` (year-guide cards for 1960/1961, "Coming
Soon" cards, no link, for 1962-1969; a second grid linking every live
genre hub). Not an article type, doesn't run `check_article.py` (same
as `/blog/genres/` and `/blog/on-this-day/`). Added to
`gen/generate_sitemap.py` STATIC_PAGES and `link-map.md`. Both `/1960s/1960/`
and `/1960s/1961/` breadcrumbs (nav + schema) now route through it.
Added a small static "1960s music, year by year" section to the
homepage linking to the hub and both live years, ahead of task 15's
full rebuild, so the pages aren't orphaned until then.

## Tracker discipline for every new year page

Every year page pushed to `main`, task 16 hub included, updates all of
the following in the same push, not a follow-up session: `sitemap.xml`
(via `gen/generate_sitemap.py`, after adding the path to
`STATIC_PAGES`), `link-map.md` (new row, live URL, up/across links),
and the `/1960s/` hub (its year-guide grid: move the card from "Coming
Soon" to a live link). This rule exists because task 3 shipped without
any of the three the first time.

## Gate 2 (target Nov 8)
All 10 year pages and the Best 60s Songs list are live and linked from
every existing On This Day page whose date falls in that year. Then
Phase 3 (`docs/strategy-review-2026-09.md` roadmap: queue rotation,
monthly data page, weekly Trending, weekly refresh) begins.
