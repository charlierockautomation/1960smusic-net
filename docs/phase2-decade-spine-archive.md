# Phase 2 — Decade Spine: Archive

Detail write-ups rotated out of `docs/phase2-decade-spine.md` to keep it
under the 195-line ceiling (CLAUDE.md File Size Ceiling rule). Task
statuses live in the active file's table; this file only holds the
build notes for tasks whose detail no longer needs to stay in working
memory.

## Task 1 detail: Year page template + schema design

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

Note: the BreadcrumbList this task shipped was 2-level (Home > Year,
"no mid-tier hub exists yet"). Task 16 (`/1960s/` hub) later added that
mid-tier: every year page's breadcrumb is now 3-level (Home > 1960s >
Year), see `docs/phase2-decade-spine.md` task 16 for when/why.

## Task 2-11 detail: 1960 and 1961 build notes

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

## Year page build notes: 1962, 1963 (moved from active file 2026-10-08)

`/1960s/1962/` live 2026-09-30, 1677 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1962 (tracklist) plus the full
chronological 21-single number-ones list, both cross-verified against
a second source. All 25 YouTube ids resolved via `generate.py`'s
no-API scraper and verified embeddable, not made-for-kids, in one
batched `yt_video_status.py` call; several (The Stripper, Mashed
Potato Time, and others hosted by non-VEVO/Topic channels) carry the
same acceptable-if-compliant flag as existing `yt`-flagged rows in
`content-build.md`. British Invasion hub not linked: `data/genres.json`
has it starting 1963, so 1962 draws only on the other 5 eligible hubs
(pop-brill-building, motown-soul, country-60s, jazz-easy-listening,
garage-surf-rock). Featured image is a real 1969 Wikimedia Commons
photo of Ray Charles (public domain, correctly dated, not claimed as
1962), chosen because he anchors both the number-ones table and the
Key Albums section (Modern Sounds in Country and Western Music).
Notable Events links two live OTD pages with direct 1962 music ties
(`/blog/on-this-day/september-15/`, Four Seasons' Sherry; `/blog/
on-this-day/october-1/`, Beach Boys' Surfin' Safari debut album).
Playwright self-test (`gen/test_playlist_player_1962.py`) PASS.

`/1960s/1963/` live 2026-10-03, 1696 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1963 (tracklist) plus the full
chronological 21-single number-ones list, both cross-verified against
a second source. All 25 YouTube ids resolved (7 already cached, 18 via
`generate.py`'s no-API scraper) and verified embeddable, not
made-for-kids, in one batched `yt_video_status.py` call; several carry
the same acceptable-if-compliant `yt` flag used elsewhere on the site.
First year page to link the British Invasion hub (`data/genres.json`
starts it at 1963); also links garage-surf-rock, pop-brill-building,
motown-soul, jazz-easy-listening and country-60s. Featured image reuses
the existing verified 1963 Dezo Hoffmann Beatles publicity photo
(public domain, already live on two other pages) rather than sourcing
a new one. Notable Events links two live OTD pages with direct 1963
music ties (`/blog/on-this-day/september-12/`, She Loves You hits UK
No. 1; `/blog/on-this-day/september-21/`, Blue Velvet hits US No. 1).
Playwright self-test (`gen/test_playlist_player_1963.py`) PASS.
