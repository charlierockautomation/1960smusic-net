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
| 3 | Year page: 1961 | not started |
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

## Task detail

### 1. Year page template + schema design
Design the shared shell for `/1960s/<year>/` before building any single
year, so all 10 stay structurally identical (matches how
`article-template.html` works for the other content types):
- Answer-first intro: year + defining fact + a number, in the first 60
  words (GEO rule 1 in the strategy review).
- Sections: US #1 hits that year (table: title, artist, chart, peak,
  weeks), key albums released, notable events (link out to the
  matching `/blog/on-this-day/<month>-<day>/` page wherever one
  exists), genre shifts that year, "Play <year>" radio filter link
  (`/tools/radio/?year=<year>`, check whether `radio-app.js` supports a
  year filter yet or whether that needs its own small task first).
- Schema: Article + ItemList (the year's #1s) + BreadcrumbList, author
  Person + datePublished/dateModified per the Phase 1 task 5/7 pattern.
- Internal links: up to the homepage and to `/best-60s-songs/` and
  `/blog/genres/60s-rock/` once those exist; across to every OTD page
  already live for that year (query `data/*.json` / OTD tracker for
  matches) and any genre hub whose era overlaps.
- Word count / density rules: use the base Structure section of
  `writing-standard.md` (no type-specific range is defined yet for
  "year page" in `check_article.py`; add one, sized after seeing how
  long a real year page runs, then keep every year page in that range).
- Facts only from `data/songs.json`/`data/artists.json` plus verified
  web search (Billboard/Official Charts year-end lists), same
  no-hallucination bar as every other page type.

Done: shell built at `docs/year-page-template.html`, same
placeholder/comment convention as `article-template.html`. Sections in
fixed order: lead, image, TOC, US #1 Hits table, Key Albums, Notable
Events, Genre Shifts, Play-on-radio CTA, FAQ, closing links. Schema:
Article (author Person, datePublished/dateModified) + ItemList (#1
hits) + BreadcrumbList (2-level, Home > Year, no mid-tier hub exists
yet) + FAQPage. `gen/check_article.py` now detects `/1960s/` paths as
type `year page`; no word-count range added yet, sizing deferred to
the first real page (task 2) per the note above.
Checked `radio-app.js` 2026-09-29: it only read a `?station=` query
param, no year filtering. Built the filter same session
(`tools/radio/radio-year.js`, wired into `tools/radio/index.html`):
on `?year=<1960-1969>` it narrows each enabled station's song pool to
that year in place (overwrites `radio-app.js`'s shared `cache`, so
Play/Skip/Select all stay within-year for free), using the `year`
field already present on every `data/radio-eligible-*.json` entry. A
genre with zero songs for that year is left unfiltered rather than
made unplayable (verified against real data: e.g. 1963 has matches in
7 of 8 genres, psychedelic-rock correctly has none since that hub
doesn't start until 1965). Logic and data shape verified via a Node
script; full browser playback not spot-checked this session.
Up-links to `/best-60s-songs/` and `/blog/genres/60s-rock/` are noted
in the template as omit-until-live (tasks 12/13), not linked yet.

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
right after the lead (before the image) on every year page, one
YouTube embed per genre-shift anchor song, so readers can play the
songs being discussed without leaving the page. YouTube API quota was
exhausted for the day (another project), so this reuses ids already
verified in `gen/yt_status_cache.json` from the site's existing
catalog rather than checking new ones; template instruction 8 now
says never to call `yt_video_status.py` for a new id on a year page.
Retrofitted onto `/1960s/1960/` (3 embeds) and `/1960s/1961/` (3
embeds); both still PASS at 1395 and 1242 words. `docs/year-page-template.html`
updated so every later year page (tasks 4-11) builds this in from the
start.

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

## Gate 2 (target Nov 8)
All 10 year pages and the Best 60s Songs list are live and linked from
every existing On This Day page whose date falls in that year. Then
Phase 3 (`docs/strategy-review-2026-09.md` roadmap: queue rotation,
monthly data page, weekly Trending, weekly refresh) begins.
