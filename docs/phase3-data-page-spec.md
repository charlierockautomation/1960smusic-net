# Phase 3 Data Page Spec (page 1 built, awaiting push approval)

Spec for the `data-page` type (`/data/<topic-slug>/`, one a month). Wiring is
built and committed (20e36a0). Source list expanded (50f4c29). Page 1 built locally, not pushed.

## Wiring (built, committed 20e36a0)

- `gen/check_article.py`: `detect_type` returns "data page" for
  `/data/<slug>/index.html`; word range 600-1200. Shared gates apply: FAQ 4-6,
  TOC, image + alt, byline, title <= 60, Article JSON-LD + image, og:image,
  sentence length, keyword density/placement.
- `gen/check_seo.py`: data page links >= 1 `/1960s/<year>/` page and >= 1 genre
  hub, and contains the phrase "our dataset".
- `gen/generate_sitemap.py`: `/data/` and `/data/<slug>/` are discovered
  (the JSON dirs under `data/` stay skipped). `/data/` index is a DRAFT page
  until page 1 ships. `posts.json` type `data-page` (label "Data") feeds
  listings and a "Data" section in `llms.txt`; `--site` requires the entry.
- `CLAUDE.md` carries a one-line Data Pages pointer to this file (196 lines).

## Source list: radio-eligible, expanded 2026-10-26 (50f4c29)

Added 123 songs for 1960, 1961, 1962, 1968, 1969 (list and method:
`gen/radio_expansion_2026-10-26.json`). Sourcing: Wikipedia Billboard Year-End
Hot 100 lists plus the year-page playlists; release year = the single year in
the song's Wikipedia infobox, equal to the stored `year` (multi-year, missing
or wrong-version infoboxes dropped, so some year-end hits released the year
before were left out); ids public, embeddable, not made-for-kids, no duplicate
ids; `daily_pool_check.py` re-run (25 of the new ids excluded from the Daily
game only, because the video title shows the year).

Now 557 rows, 556 unique ids (Wild Thing is in two genre files).
Per year: 1960 43, 1961 44, 1962 44, 1963 43, 1964 58, 1965 70, 1966 83,
1967 85, 1968 43, 1969 44. No year is under 20, so no "small sample" callout
is needed today; the page script still adds one automatically if a year
ever falls under 20. Per genre: pop-brill-building 108, motown-soul 97,
british-invasion 64, jazz-easy-listening 63, country-60s 61, folk-rock 58,
garage-surf-rock 53, psychedelic-rock 53. Fields: `title`, `artist`, `year`,
`genre`, `youtube_id`, `verified_date`. 11 of 80 year x genre cells are zero.
Psychedelic rock: 1966 7, 1967 32, 1968 11, 1969 3, nothing earlier; 1967
holds 32 of its 53 songs (60%).

## Page 1: BUILT 2026-10-26, awaiting Charlie's approval to push

URL `/data/1960s-music-genres-by-year/` (slug switched to carry the approved
focus keyword "1960s music genres"; the title and intro still say Radio Dial).
Built by `gen/build_data_page_radio.py` from the radio-eligible JSON; checked
by `gen/test_data_page_radio.py` (table cells, shares, totals, links) and
`gen/check_article.py` (PASS, 954 words). Self-hosted chart PNG is the
`og:image`.

- Structure: H1, lead (556 unique songs, "our dataset", Radio Dial link),
  chart, TOC, psychedelic rock lead insight (no songs 1960 to 1965, 7 in 1966,
  32 of its 53 in 1967, 38% of that year, 3 by 1969), the 10 x 8 table (count
  plus share of year, year rows link `/1960s/<year>/`, genre columns link the
  hubs), "What Each Genre Means" (8 H3s, each hub-linked: one paraphrased
  sentence from `genres.json` plus one dataset sentence), "How We Counted"
  (primary genre only, Wild Thing counted in both stations, 557 rows / 556
  unique), 4-question FAQ, closing with the keyword.
- Small-sample rule: the script adds a note automatically for any year under
  20 songs. None today (minimum 43).
- Wiring touched while building: `validate_jsonld.py --all` skipped all of
  `data/`, now covers `/data/` pages; `/data/` index live (DRAFT removed) with
  the page's card; `/1960s/` hub has a Data card; `posts.json` entry added.

## Focus keyword research (DataForSEO, run 2026-10-26)

Volume = Google Ads monthly average; KD = DataForSEO keyword difficulty.
Google folds "60s music genres" and "music genres of the 1960s" into the same
cluster as "1960s music genres" (identical numbers).

| Candidate | US vol | CA vol | KD US / CA |
|---|---|---|---|
| 1960s music genres | 720 (480-1,300 over 12 mo) | 90 | 0 / 0 |
| 1960s songs | 14,800 | 1,300 | 8 / 8 |
| 1960s songs by year | no data | no data | no data |
| 1960s music by genre | no data | no data | no data |
| 60s music by year | no data | no data | no data |
| 60s songs by genre | no data | no data | no data |
| 1960s music statistics | no data | no data | no data |

Top results, "1960s music genres" (US): Wikipedia "1960s in music", a Reddit
thread, Full Sail LibGuide, Rock Music Timeline, jeffs60s.com, Study.com, an
IMDb list; AI Overview and YouTube video block above them. No data-led page.
Top results, "1960s songs" (US): Spotify/Apple playlists, SiriusXM list,
YouTube videos, Wikipedia year-end list, Pitchfork, Gold Standard Song List.
Playlist and list intent, and `/best-60s-songs/` already targets it.

Decision (Charlie, 2026-10-26): focus keyword "1960s music genres"; slug
`/data/1960s-music-genres-by-year/`. "1960s songs" rejected: list intent,
already served by `/best-60s-songs/`.

## Later pages (same two rules: fields that exist, "our dataset")

Dec onward, candidates: artists most often on the dial; songs by `mood_tags`,
`difficulty` or `tiktok_viral` from `songs.json` (count field coverage first);
year-over-year genre share. Each gets its own spec line before building.

## Open

1. Charlie's approval to push page 1 (nothing pushed yet).
2. After push: `verify_live.py`, `indexnow_ping.py`, `link-map.md` rows to live.
