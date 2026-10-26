# Phase 3 Data Page Spec (page 1 approved; keyword awaiting Charlie's OK)

Spec for the `data-page` type (`/data/<topic-slug>/`, one a month). Wiring is
built and committed (20e36a0). Source list expanded (50f4c29). Page 1 is NOT
built: the build waits for Charlie's OK on the focus keyword.

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

## Page 1 (approved by Charlie 2026-10-26)

- URL: `/data/radio-dial-songs-by-year-and-genre/` as approved. See keyword
  note: the writing standard wants the focus keyword in the slug.
- Framing: what is on the Radio Dial, from our dataset, not the whole decade.
  Primary internal link goes to `/tools/radio/`.
- Headline number: 556 unique songs (557 rows). One-line note that Wild
  Thing is counted in both British Invasion and Garage & Surf Rock as listed
  on the dial. The script recounts both numbers at build time.
- Table: 10 years x 8 genres, raw counts with the genre's percentage share of
  that year next to each count. Primary genre only, stated on the page.
  Year rows link `/1960s/<year>/`; genre columns link the 8 hubs.
- Analysis leads with psychedelic rock (nothing before 1966, then 1967), then
  genre leaders, zero cells, thin years (every year here is >= 43). Any year
  under 20 songs is called out as a small sample (none today).
- Generated, not typed: `gen/build_data_page_radio.py` writes table, chart and
  prose figures from the JSON files; a test fails if page numbers drift.
- Required by the gates: FAQ 4-6, TOC, byline, self-hosted chart image with
  real alt, Article JSON-LD with image, og:image, 600-1200 words, no chart
  positions or "the 1960s had" claims.

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

Recommendation: "1960s music genres". Real demand (720 US), KD 0, weak
non-specialist competition, and a count-by-genre page matches the intent.
Reject "1960s songs": 20x the volume but a list/playlist intent we already
serve, so a data page would cannibalize `/best-60s-songs/`. The by-year/
by-genre long tails have no measurable volume; use them as secondary terms.
Open: with this keyword the slug should contain it, e.g.
`/data/1960s-music-genres-by-year/` (replaces the approved slug if OK'd).

## Later pages (same two rules: fields that exist, "our dataset")

Dec onward, candidates: artists most often on the dial; songs by `mood_tags`,
`difficulty` or `tiktok_viral` from `songs.json` (count field coverage first);
year-over-year genre share. Each gets its own spec line before building.

## Decisions needed from Charlie

1. OK the focus keyword "1960s music genres" (or pick another).
2. Slug: keep `/data/radio-dial-songs-by-year-and-genre/` (needs a documented
   exception to the keyword-in-slug rule) or switch to
   `/data/1960s-music-genres-by-year/`.
