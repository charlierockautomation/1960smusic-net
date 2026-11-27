# Content Build Queue

Single source of truth for what gets written next on 1960smusic.net. Read
this file at the start of every content session before touching anything
else.

## How this works

Work the first `not started` row only; never start a row while an earlier
one is `in progress` or `drafted`. Build, gate, push and post-push steps are
CLAUDE.md "Content Pipeline" steps 1-6 (shell: `docs/article-template.html`;
facts from `data/*.json` first, web search only for verified gaps). After
going live: status here → `live`, then `link-map.md`, then the next row.

Status values: `not started` · `in progress` (page being written) ·
`drafted` (written, not yet passing check_article.py or not yet reviewed
locally) · `live` (pushed to main and confirmed responding 200).

`_yt_flagged` = the YouTube ID came back flagged in `gen/yt_cache.json`
(non-obviously-official source or unconfirmed embeddability). Spot-check
before embedding; swap for a verified ID if the flagged one doesn't hold up.

## Rotation and pagination

Rows 36+ round-robin across the 8 genres in `data/genres.json`:
british-invasion → psychedelic-rock → garage-surf-rock → folk-rock →
motown-soul → country-60s → pop-brill-building → jazz-easy-listening, one
full artist cluster (bio row first, then its song-story rows) per genre per
pass; a genre drops out once its clusters are spent. Never stack many rows of
one genre. Why: spreads internal-link equity (each story links its bio and
hub, each bio its hub) evenly for SEO and AI citations.

Do not reorder rows already in the queue; new rows append in rotation order
only (rotation applies to future rows, not ones already locked in). Row 62
("I Walk the Line", 1956) was dropped by Charlie 2026-09-29; the number is
retired, not reused.

Each session loads only the rows in this file. The rest of the rotation
lives, in order, in:

- [`docs/content-build-queued.md`](content-build-queued.md) — rows 139-165
- [`docs/content-build-queued-2.md`](content-build-queued-2.md) — rows 166-251

When every row in the Queue table below is `live`, move those rows into
[`docs/content-build-archive.md`](content-build-archive.md) and pull the
next contiguous block up from `content-build-queued.md` (then from
`-queued-2.md`), keeping every file at or under 195 lines.

Reserved marquee bios with empty `notable_song_ids` (Country Joe and the
Fish, The 13th Floor Elevators, Love, Joan Baez, Burt Bacharach) are not
in the rotation; their pages land in a later phase per
`docs/architecture.md`.

## Queue

Live rows (1-119) are in [`docs/content-build-archive.md`](content-build-archive.md).

| # | Title | Slug | Type | Genre | Status | Focus Keyword | YouTube ID | Flag |
|---|-------|------|------|-------|--------|----------------|------------|------|
| 120 | Pink Floyd bio | /blog/artists/pink-floyd/ | artist-bio | psychedelic-rock | live | Pink Floyd | H3DGpINHX5Q |  |
| 121 | Arnold Layne | /blog/songs/arnold-layne-pink-floyd/ | song-story | psychedelic-rock | live | Arnold Layne by Pink Floyd | H3DGpINHX5Q |  |
| 122 | Astronomy Domine | /blog/songs/astronomy-domine-pink-floyd/ | song-story | psychedelic-rock | live | Astronomy Domine by Pink Floyd | 8UbNbor3OqQ |  |
| 123 | The Ventures bio | /blog/artists/the-ventures/ | artist-bio | garage-surf-rock | not started | The Ventures | hIuIIqbyEIU | yt |
| 124 | Walk Don't Run | /blog/songs/walk-dont-run-ventures/ | song-story | garage-surf-rock | not started | Walk Don't Run | hIuIIqbyEIU | yt |
| 125 | Peter, Paul and Mary bio | /blog/artists/peter-paul-and-mary/ | artist-bio | folk-rock | not started | Peter, Paul and Mary | XxWTDcP9Y5E | yt |
| 126 | If I Had a Hammer | /blog/songs/if-i-had-a-hammer-peter-paul-and-mary/ | song-story | folk-rock | not started | If I Had a Hammer | XxWTDcP9Y5E | yt |
| 127 | Puff, the Magic Dragon | /blog/songs/puff-the-magic-dragon-peter-paul-and-mary/ | song-story | folk-rock | not started | Puff, the Magic Dragon | z15pxWUXvLY | yt |
| 128 | Leaving on a Jet Plane | /blog/songs/leaving-on-a-jet-plane-peter-paul-and-mary/ | song-story | folk-rock | not started | Leaving on a Jet Plane | F2m--R3J6f4 |  |
| 129 | Freight Train | /blog/songs/freight-train-peter-paul-and-mary/ | song-story | folk-rock | not started | Freight Train by Peter, Paul and Mary | BZrb-ao5v3M |  |
| 130 | The Four Tops bio | /blog/artists/the-four-tops/ | artist-bio | motown-soul | not started | The Four Tops | 2EaflX0MWRo | yt |
| 131 | Reach Out I'll Be There | /blog/songs/reach-out-ill-be-there-four-tops/ | song-story | motown-soul | not started | Reach Out I'll Be There | 2EaflX0MWRo | yt |
| 132 | I Can't Help Myself (Sugar Pie Honey Bunch) | /blog/songs/i-cant-help-myself-sugar-pie-honey-bunch-four-tops/ | song-story | motown-soul | not started | I Can't Help Myself (Sugar Pie Honey Bunch) | s3bksUSPB4c | yt |
| 133 | Merle Haggard bio | /blog/artists/merle-haggard/ | artist-bio | country-60s | not started | Merle Haggard | 3dM03dG3zv4 |  |
| 134 | Okie from Muskogee | /blog/songs/okie-from-muskogee-merle-haggard/ | song-story | country-60s | not started | Okie from Muskogee | 3dM03dG3zv4 |  |
| 135 | Mama Tried | /blog/songs/mama-tried-merle-haggard/ | song-story | country-60s | not started | Mama Tried by Merle Haggard | loT_pYzi3Vw |  |
| 136 | The Crystals bio | /blog/artists/the-crystals/ | artist-bio | pop-brill-building | not started | The Crystals | S-OTd7DXjlo |  |
| 137 | Da Doo Ron Ron | /blog/songs/da-doo-ron-ron-crystals/ | song-story | pop-brill-building | not started | Da Doo Ron Ron | S-OTd7DXjlo |  |
| 138 | Then He Kissed Me | /blog/songs/then-he-kissed-me-crystals/ | song-story | pop-brill-building | not started | Then He Kissed Me | MSkum4B162M | yt |

Artist-bio YouTube IDs are the artist's first `notable_song_ids` entry in
`data/artists.json` (same convention used for The Beatles bio, which
embeds "She Loves You"). Song-story YouTube IDs come straight from the
matching record in `data/songs.json`.

## Trending branch check

A Monday Trending routine run that succeeds but pushes no `trending/YYYY-MM-DD`
branch means "no verifiable peg this week", not a failure. Only a failed run
needs a look.

## Weekly refresh log

One refresh a week (Phase 3). Completed entries and the table format live in
`docs/content-build-archive.md` ("Weekly refresh log"); add new rows there.

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
