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

- [`docs/content-build-queued.md`](content-build-queued.md) — rows 120-165
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

Live rows (1-102) are in [`docs/content-build-archive.md`](content-build-archive.md).

| # | Title | Slug | Type | Genre | Status | Focus Keyword | YouTube ID | Flag |
|---|-------|------|------|-------|--------|----------------|------------|------|
| 103 | The Byrds bio | /blog/artists/the-byrds/ | artist-bio | folk-rock | live | The Byrds | NxyOhFBoxSY |  |
| 104 | Mr. Tambourine Man | /blog/songs/mr-tambourine-man-byrds/ | song-story | folk-rock | not started | Mr. Tambourine Man | Swqw5a8I4b4 |  |
| 105 | Turn! Turn! Turn! | /blog/songs/turn-turn-turn-byrds/ | song-story | folk-rock | not started | Turn! Turn! Turn! | xVOJla2vYx8 |  |
| 106 | Marvin Gaye bio | /blog/artists/marvin-gaye/ | artist-bio | motown-soul | not started | Marvin Gaye | 5ZnrZnFSlWU |  |
| 107 | I Heard It Through the Grapevine | /blog/songs/i-heard-it-through-the-grapevine-marvin-gaye/ | song-story | motown-soul | not started | I Heard It Through the Grapevine | 5ZnrZnFSlWU |  |
| 108 | Ain't No Mountain High Enough | /blog/songs/aint-no-mountain-high-enough-marvin-gaye/ | song-story | motown-soul | not started | Ain't No Mountain High Enough | IC5PL0XImjw | yt |
| 109 | How Sweet It Is (To Be Loved by You) | /blog/songs/how-sweet-it-is-to-be-loved-by-you-marvin-gaye/ | song-story | motown-soul | not started | How Sweet It Is (To Be Loved by You) | OhbQVA7hPuQ |  |
| 110 | Buck Owens bio | /blog/artists/buck-owens/ | artist-bio | country-60s | not started | Buck Owens | __SMDtF_DsY |  |
| 111 | Act Naturally | /blog/songs/act-naturally-buck-owens/ | song-story | country-60s | not started | Act Naturally by Buck Owens | __SMDtF_DsY |  |
| 112 | Together Again | /blog/songs/together-again-buck-owens/ | song-story | country-60s | not started | Together Again by Buck Owens | h6-wKFK4sQM |  |
| 113 | Buckaroo | /blog/songs/buckaroo-buck-owens/ | song-story | country-60s | not started | Buckaroo by Buck Owens | -2VLIO14dns | yt |
| 114 | The Ronettes bio | /blog/artists/the-ronettes/ | artist-bio | pop-brill-building | not started | The Ronettes | jSPpbOGnFgk |  |
| 115 | Be My Baby | /blog/songs/be-my-baby-ronettes/ | song-story | pop-brill-building | not started | Be My Baby | jSPpbOGnFgk |  |
| 116 | Dionne Warwick bio | /blog/artists/dionne-warwick/ | artist-bio | jazz-easy-listening | not started | Dionne Warwick | vsGsCvJWEo8 |  |
| 117 | Walk On By | /blog/songs/walk-on-by-dionne-warwick/ | song-story | jazz-easy-listening | not started | Walk On By | vsGsCvJWEo8 |  |
| 118 | Do You Know the Way to San Jose | /blog/songs/do-you-know-the-way-to-san-jose-dionne-warwick/ | song-story | jazz-easy-listening | not started | Do You Know the Way to San Jose | FZLa-1q-lkw |  |
| 119 | Alfie | /blog/songs/alfie-dionne-warwick/ | song-story | jazz-easy-listening | not started | Alfie by Dionne Warwick | YL06i9aiM4o | yt |

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
