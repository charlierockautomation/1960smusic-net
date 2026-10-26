# Phase 3 Data Page Spec (DRAFT, awaiting Charlie's sign-off)

Spec for the `data-page` type (`/data/<topic-slug>/`, one a month). Wiring is
built; no data page is. Nothing here is built until Charlie signs off.

## Wiring status (built 2026-10-26, uncommitted)

- `gen/check_article.py`: `detect_type` returns "data page" for
  `/data/<slug>/index.html`; word range 600-1200. All shared gates still
  apply: FAQ 4-6, TOC, image + alt, byline, title <= 60, Article JSON-LD
  with image, og:image, sentence length, keyword density and placement.
- `gen/check_seo.py`: a data page must link >= 1 `/1960s/<year>/` page and
  >= 1 genre hub, and must contain the phrase "our dataset".
- `gen/generate_sitemap.py`: `data/` stays skipped for JSON, but
  `/data/` and `/data/<slug>/` are discovered (they would otherwise have been
  silently dropped). `/data/` index is a DRAFT page, so it is not yet listed.
- `check_article.py --site`: a `/data/<slug>/` page must be in `posts.json`.
- `posts.json` type `data-page` (label "Data"); `llms.txt` gets a "Data"
  section from those entries; `/data/` index itself is not in `llms.txt`.
- `/data/index.html` placed as DRAFT (remove the comment with page one).
  `link-map.md` row added, status `placed`.
- Not wired, by choice: `CLAUDE.md` is at 195 lines, so the new type's rules
  live here and in `phase3-spread.md`. A "Data Pages" pointer needs one line
  moved out first. Ask before touching.

## Source lists checked

| Source | Rows | Per genre | Per year |
|---|---|---|---|
| `data/songs.json` | 192 | 12-46 | 5 (1960) to 35 (1967) |
| `data/radio-eligible-*.json` (8 files) | 434 (433 unique ids) | 50-60 | 9 (1960) to 85 (1967) |

Radio-eligible per genre: british-invasion 60, motown-soul 59, pop-brill-building
56, folk-rock 55, country-60s 52, garage-surf-rock 51, jazz-easy-listening 51,
psychedelic-rock 50. Per year: 1960 9, 1961 15, 1962 23, 1963 43, 1964 58,
1965 70, 1966 83, 1967 85, 1968 37, 1969 11.
Fields: `title`, `artist`, `year`, `genre`, `youtube_id`, `verified_date`
(plus `year_alt*` on 1 row). 189 of the 434 also appear in `songs.json`;
208 distinct artists. Hand-maintained, quarterly-verified (see
`docs/architecture.md`), so the file is stable enough to cite as a dataset.

Every genre clears the 50 bar, so the radio list qualifies. It does not fix
the year skew: 13 of 80 year x genre cells are zero, psychedelic rock has no
rows before 1966 and 32 in 1967, 1960 and 1969 are thin. The skew comes from
what we verified as embeddable, not from the decade. The page must say so.

## Proposed page 1

- Slug: `/data/radio-dial-songs-by-year-and-genre/`.
- Focus keyword (to verify with competitor research): "1960s songs by year".
- H1/angle: what the Radio Dial's verified playlist holds, 1960-1969, by
  year and genre. Framed as "our dataset" and "the Radio Dial's verified
  list", never "the 1960s had".
- Fields used: `year`, `genre` only (primary genre, stated on the page; the
  radio files give each row one genre). `artist`/`title` only for named
  examples in prose, checked against the file.
- Open item: "Wild Thing" (The Troggs, 1966) sits in both british-invasion
  and garage-surf-rock, so counting rows gives 434 and unique songs gives 433.
  Needs a rule. Proposed: count rows as listed per station, state the 434 vs
  433 difference in a note.
- Body: lead with the totals; one 10 x 8 count table (rows link
  `/1960s/<year>/`, column heads link the 8 genre hubs, all 10 years and 8 hubs
  linked); a method section (source, primary genre only, verification, what is
  not counted); "What the numbers show" (peak year, genre leaders, zero cells,
  each tied to the skew caveat); links to `/tools/radio/`, `/best-60s-songs/`.
  FAQ 4-6, TOC, byline, one self-hosted chart image (SVG/PNG, real alt) for
  `og:image`.
- Every figure is generated, not typed: `gen/build_data_page_radio.py`
  writes the table and chart from the JSON files, with a test like
  `gen/test_best_60s_songs.py` that fails if a number in the page differs
  from the data. Prose figures read from the same script.
- No chart positions, sales, rankings or claims about "the decade".
- Updated date rule: bumps only on a re-count after the radio files change.

## Monthly cadence ideas (subject to the same two rules: fields that exist, "our dataset")

Nov: page 1 above. Dec onward, candidates: most-featured artists in the radio
list; songs per year by `mood_tags` / `difficulty` / `tiktok_viral` from
`songs.json` (field coverage must be counted first); year-over-year genre
share. Each gets its own spec line before building.

## Decisions needed from Charlie

1. Approve radio-eligible as the source for page 1 (50+ per genre met, year skew
   stays and is disclosed).
2. Wild Thing counting rule (row count 434, or unique 433).
3. Slug and focus keyword OK, or run the keyword check first.
4. Okay to free one line in CLAUDE.md for a "Data Pages" pointer.
