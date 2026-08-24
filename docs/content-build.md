# Content Build Queue

Single source of truth for what gets written next on 1960smusic.net. Read
this file at the start of every content session before touching anything
else.

## How this works

1. Find the first row below with status `not started`. That is the only
   article to work on. Never start a new row while any earlier row is
   `in progress` or `drafted` — finish and confirm one live before starting
   the next.
2. Build the page using [`/docs/article-template.html`](article-template.html)
   as the shell. Pull facts from `data/songs.json` and `data/artists.json`
   first; use web search only to fill verified gaps (release dates,
   chart facts, direct quotes with a real source). Never invent history,
   quotes, or trivia, matching the standing site rule in `README.md`.
3. Run `python3 gen/check_article.py <path>` before committing. If it
   fails, fix the article and rerun. Do not commit on a FAIL, and do not
   ask Charlie to fix formatting or structure, since the template and
   check_article.py already define both.
4. Build locally, run a local server, and get Charlie's explicit
   go-ahead before pushing to `main`. Pushing to `main` is what makes a
   page live (see `wrangler.toml` / Cloudflare Workers Builds). Do not
   push without that go-ahead.
5. Once live, in the same session, update all three of:
   - this file (status → `live`)
   - `data/posts.json` (new entry)
   - `link-map.md` (status → `live`, live URL, inbound/outbound links)

   Only then move to the next `not started` row.

Status values: `not started` · `in progress` (page being written) ·
`drafted` (page written, not yet passing check_article.py or not yet
reviewed locally) · `live` (pushed to main and confirmed responding 200
at its live URL).

`_yt_flagged` = the YouTube ID came back flagged in `gen/yt_cache.json`
(non-obviously-official source or unconfirmed embeddability). Spot-check
before embedding; swap for a verified ID if the flagged one doesn't hold up.

## Queue

Live rows (1-12) moved to [`docs/content-build-archive.md`](content-build-archive.md).

| # | Title | Slug | Type | Genre | Status | Focus Keyword | YouTube ID | Flag |
|---|-------|------|------|-------|--------|----------------|------------|------|
| 13 | Waterloo Sunset | /blog/songs/waterloo-sunset-kinks/ | song-story | british-invasion | live | Waterloo Sunset | N_MqfF0WBsU | |
| 14 | Psychedelic Rock hub | /blog/genres/psychedelic-rock/ | genre-hub | psychedelic-rock | live | Psychedelic Rock | qoX6AKuYWL8 | |
| 15 | Garage & Surf Rock hub | /blog/genres/garage-surf-rock/ | genre-hub | garage-surf-rock | live | Garage Rock | enlOHxQ0tb4 | |
| 16 | Country (Nashville Sound & Bakersfield) hub | /blog/genres/country-60s/ | genre-hub | country-60s | live | 1960s Country Music | 1WaV2x8GXj0 | |
| 17 | Pop & Brill Building hub | /blog/genres/pop-brill-building/ | genre-hub | pop-brill-building | live | Brill Building Pop | 4PQAqprjOuA | |
| 18 | Jazz & Easy Listening hub | /blog/genres/jazz-easy-listening/ | genre-hub | jazz-easy-listening | not started | Easy Listening 1960s | JYuyWrkwpok | |
| 19 | The Who bio | /blog/artists/the-who/ | artist-bio | british-invasion | not started | The Who | qN5zw04WxCc | yt |
| 20 | My Generation | /blog/songs/my-generation-who/ | song-story | british-invasion | not started | My Generation | qN5zw04WxCc | yt |
| 21 | The Animals bio | /blog/artists/the-animals/ | artist-bio | british-invasion | not started | The Animals | N4bFqW_eu2I | yt |
| 22 | House of the Rising Sun | /blog/songs/house-of-the-rising-sun-animals/ | song-story | british-invasion | not started | House of the Rising Sun | N4bFqW_eu2I | yt |
| 23 | The Yardbirds bio | /blog/artists/the-yardbirds/ | artist-bio | british-invasion | not started | The Yardbirds | yKI7c9x2lbM | |
| 24 | For Your Love | /blog/songs/for-your-love-yardbirds/ | song-story | british-invasion | not started | For Your Love | yKI7c9x2lbM | |
| 25 | Heart Full of Soul | /blog/songs/heart-full-of-soul-yardbirds/ | song-story | british-invasion | not started | Heart Full of Soul | pM1qZBFiOLU | yt |
| 26 | Over Under Sideways Down | /blog/songs/over-under-sideways-down-yardbirds/ | song-story | british-invasion | not started | Over Under Sideways Down | OUIbVrev-yk | |
| 27 | The Dave Clark Five bio | /blog/artists/the-dave-clark-five/ | artist-bio | british-invasion | not started | The Dave Clark Five | NHtNFaa2ne0 | yt |
| 28 | Glad All Over | /blog/songs/glad-all-over-dave-clark-five/ | song-story | british-invasion | not started | Glad All Over | NHtNFaa2ne0 | yt |
| 29 | Bits and Pieces | /blog/songs/bits-and-pieces-dave-clark-five/ | song-story | british-invasion | not started | Bits and Pieces | SzTQduUZFY8 | |
| 30 | Because | /blog/songs/because-dave-clark-five/ | song-story | british-invasion | not started | Because (The Dave Clark Five) | QpKWpUJybng | yt |
| 31 | Herman's Hermits bio | /blog/artists/hermanns-hermits/ | artist-bio | british-invasion | not started | Herman's Hermits | IOfs8U_3NQk | yt |
| 32 | Mrs. Brown You've Got a Lovely Daughter | /blog/songs/mrs-brown-youve-got-a-lovely-daughter-hermanns-hermits/ | song-story | british-invasion | not started | Mrs. Brown You've Got a Lovely Daughter | IOfs8U_3NQk | yt |
| 33 | I'm Henry the VIII, I Am | /blog/songs/im-henry-the-viii-i-am-hermanns-hermits/ | song-story | british-invasion | not started | I'm Henry the VIII, I Am | FFNoDsOmluA | yt |
| 34 | The Searchers bio | /blog/artists/the-searchers/ | artist-bio | british-invasion | not started | The Searchers | ugDXpdjmpgw | yt |
| 35 | Needles and Pins | /blog/songs/needles-and-pins-searchers/ | song-story | british-invasion | not started | Needles and Pins | ugDXpdjmpgw | yt |

Artist-bio YouTube IDs are the artist's first `notable_song_ids` entry in
`data/artists.json` (same convention used for The Beatles bio, which
embeds "She Loves You"). Song-story YouTube IDs come straight from the
matching record in `data/songs.json`.

## Future keywords (not queued, do not add to the rotation above)

Charlie-supplied keywords for articles that don't have a queue row yet.
These sit here until Charlie says to add them to the numbered rotation.
Adding a keyword here never changes queue order on its own.

| Keyword | Suggested article | Note |
|---|---|---|
| Sympathy for the Devil | Rolling Stones song story (not yet queued; queue currently has "(I Can't Get No) Satisfaction" as row 7) | 40,500 volume, low competition |
| 60s rock bands | Hub or list article | |
| British rock bands 1960s | Hub or list article | |
| 1960s music artists | Artist category hub | |
| Merseybeat | Sub-genre article | |
| Mod music 1960s | Sub-genre article | |
| British blues rock 1960s | Sub-genre article | |
| Lola by The Kinks | Kinks song story (not yet queued) | 27,100 volume, low competition |
| The Kinks Are the Village Green Preservation Society | Kinks album feature (not yet queued; no album-review type in the pipeline yet) | ~1,000-1,300 volume across variants, low competition |
| The Kinks Don't Forget to Dance | Kinks song story (not yet queued) | 480 volume, low competition |
| Kinda Kinks | Kinks album feature (not yet queued; no album-review type in the pipeline yet) | 480 volume, low competition |
| The Kinks Greatest Hits | Kinks compilation feature (not yet queued) | 2,900 volume, low competition |
