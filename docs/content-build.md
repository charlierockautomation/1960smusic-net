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

## Rotation and pagination

Rows 36+ are a genre round-robin covering every artist bio and song story
buildable from the current `data/artists.json` + `data/songs.json` that is
not already live or queued. The cycle runs british-invasion →
psychedelic-rock → garage-surf-rock → folk-rock → motown-soul →
country-60s → pop-brill-building → jazz-easy-listening, placing one full
artist cluster (its bio row first, then that artist's song-story rows) per
genre per pass, then repeating. A genre drops out once its clusters are
spent. This spreads internal-link equity across all eight genres instead
of building one genre out completely: every new song story links up to its
artist bio and genre hub, every new bio links up to its hub, so the
focus-keyword text links compound evenly for SEO and AI answer citations.

Do not reorder rows already in this active table. New rows append in
rotation order only.

Each session loads only the rows in this file. The rest of the rotation
lives, in order, in:

- [`docs/content-build-queued.md`](content-build-queued.md) — rows 71-165
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

Live rows (1-26) are in [`docs/content-build-archive.md`](content-build-archive.md).

| # | Title | Slug | Type | Genre | Status | Focus Keyword | YouTube ID | Flag |
|---|-------|------|------|-------|--------|----------------|------------|------|
| 27 | The Dave Clark Five bio | /blog/artists/the-dave-clark-five/ | artist-bio | british-invasion | live | The Dave Clark 5 | mgwkpOzZXWg | |
| 28 | Glad All Over | /blog/songs/glad-all-over-dave-clark-five/ | song-story | british-invasion | live | Glad All Over | mgwkpOzZXWg | |
| 29 | Bits and Pieces | /blog/songs/bits-and-pieces-dave-clark-five/ | song-story | british-invasion | live | Bits and Pieces | SzTQduUZFY8 | |
| 30 | Because | /blog/songs/because-dave-clark-five/ | song-story | british-invasion | live | because the dave clark five | nuKdJmOZLN4 | |
| 31 | Herman's Hermits bio | /blog/artists/hermanns-hermits/ | artist-bio | british-invasion | not started | Herman's Hermits | IOfs8U_3NQk | yt |
| 32 | Mrs. Brown You've Got a Lovely Daughter | /blog/songs/mrs-brown-youve-got-a-lovely-daughter-hermanns-hermits/ | song-story | british-invasion | not started | Mrs. Brown You've Got a Lovely Daughter | IOfs8U_3NQk | yt |
| 33 | I'm Henry the VIII, I Am | /blog/songs/im-henry-the-viii-i-am-hermanns-hermits/ | song-story | british-invasion | not started | I'm Henry the VIII, I Am | FFNoDsOmluA | yt |
| 34 | The Searchers bio | /blog/artists/the-searchers/ | artist-bio | british-invasion | not started | The Searchers | ugDXpdjmpgw | yt |
| 35 | Needles and Pins | /blog/songs/needles-and-pins-searchers/ | song-story | british-invasion | not started | Needles and Pins | ugDXpdjmpgw | yt |
| 36 | Do Wah Diddy Diddy | /blog/songs/do-wah-diddy-diddy-manfred-mann/ | song-story | british-invasion | not started | Do Wah Diddy Diddy | 1UingsUi0mI |  |
| 37 | The Doors bio | /blog/artists/the-doors/ | artist-bio | psychedelic-rock | not started | The Doors | qoX6AKuYWL8 |  |
| 38 | Light My Fire | /blog/songs/light-my-fire-doors/ | song-story | psychedelic-rock | not started | Light My Fire | qoX6AKuYWL8 |  |
| 39 | The End | /blog/songs/the-end-doors/ | song-story | psychedelic-rock | not started | The End by The Doors | 9pRGoSbYHQE |  |
| 40 | Strange Days | /blog/songs/strange-days-doors/ | song-story | psychedelic-rock | not started | Strange Days by The Doors | tHOK87ozcho |  |
| 41 | The Crystal Ship | /blog/songs/the-crystal-ship-doors/ | song-story | psychedelic-rock | not started | The Crystal Ship | rbulIrN4scs |  |
| 42 | The Beach Boys bio | /blog/artists/the-beach-boys/ | artist-bio | garage-surf-rock | not started | The Beach Boys | enlOHxQ0tb4 |  |
| 43 | Surfin' USA | /blog/songs/surfin-usa-beach-boys/ | song-story | garage-surf-rock | not started | Surfin' USA by The Beach Boys | enlOHxQ0tb4 |  |
| 44 | Good Vibrations | /blog/songs/good-vibrations-beach-boys/ | song-story | garage-surf-rock | not started | Good Vibrations by The Beach Boys | apBWI6xrbLY |  |
| 45 | Fun, Fun, Fun | /blog/songs/fun-fun-fun-beach-boys/ | song-story | garage-surf-rock | not started | Fun, Fun, Fun | VF_o-N0fhZ0 |  |
| 46 | California Girls | /blog/songs/california-girls-beach-boys/ | song-story | garage-surf-rock | not started | California Girls by The Beach Boys | DR2lvcdKSdU |  |
| 47 | Surfin' Safari | /blog/songs/surfin-safari-beach-boys/ | song-story | garage-surf-rock | not started | Surfin' Safari by The Beach Boys | IMChBJZUDK8 | yt |
| 48 | Bob Dylan bio | /blog/artists/bob-dylan/ | artist-bio | folk-rock | not started | Bob Dylan | IwOfCgkyEj0 |  |
| 49 | Like a Rolling Stone | /blog/songs/like-a-rolling-stone-bob-dylan/ | song-story | folk-rock | not started | Like a Rolling Stone | IwOfCgkyEj0 |  |
| 50 | Blowin' in the Wind | /blog/songs/blowin-in-the-wind-bob-dylan/ | song-story | folk-rock | not started | Blowin' in the Wind | MMFj8uDubsE |  |
| 51 | Positively 4th Street | /blog/songs/positively-4th-street-bob-dylan/ | song-story | folk-rock | not started | Positively 4th Street | aehwEu8SBSo |  |
| 52 | Subterranean Homesick Blues | /blog/songs/subterranean-homesick-blues-bob-dylan/ | song-story | folk-rock | not started | Subterranean Homesick Blues | MGxjIBEZvx0 |  |
| 53 | The Times They Are a-Changin' | /blog/songs/the-times-they-are-a-changin-bob-dylan/ | song-story | folk-rock | not started | The Times They Are a-Changin' | 90WD_ats6eE |  |
| 54 | The Supremes bio | /blog/artists/the-supremes/ | artist-bio | motown-soul | not started | The Supremes | une981B7Q4Y |  |
| 55 | Stop! In the Name of Love | /blog/songs/stop-in-the-name-of-love-supremes/ | song-story | motown-soul | not started | Stop! In the Name of Love | une981B7Q4Y |  |
| 56 | Baby Love | /blog/songs/baby-love-supremes/ | song-story | motown-soul | not started | Baby Love by The Supremes | D6QF4sB40gU |  |
| 57 | Where Did Our Love Go | /blog/songs/where-did-our-love-go-supremes/ | song-story | motown-soul | not started | Where Did Our Love Go | Jt_31gR18NA |  |
| 58 | You Keep Me Hangin' On | /blog/songs/you-keep-me-hangin-on-supremes/ | song-story | motown-soul | not started | You Keep Me Hangin' On | pi00f6oiMu4 |  |
| 59 | Come See About Me | /blog/songs/come-see-about-me-supremes/ | song-story | motown-soul | not started | Come See About Me | NkH_dm9NkxQ |  |
| 60 | Johnny Cash bio | /blog/artists/johnny-cash/ | artist-bio | country-60s | not started | Johnny Cash | 1WaV2x8GXj0 |  |
| 61 | Ring of Fire | /blog/songs/ring-of-fire-johnny-cash/ | song-story | country-60s | not started | Ring of Fire | 1WaV2x8GXj0 |  |
| 62 | I Walk the Line | /blog/songs/i-walk-the-line-johnny-cash/ | song-story | country-60s | not started | I Walk the Line | J-6fW66IUY4 |  |
| 63 | The Monkees bio | /blog/artists/the-monkees/ | artist-bio | pop-brill-building | not started | The Monkees | 5tpxXDILZHs | yt |
| 64 | I'm a Believer | /blog/songs/im-a-believer-monkees/ | song-story | pop-brill-building | not started | I'm a Believer | 5tpxXDILZHs | yt |
| 65 | Last Train to Clarksville | /blog/songs/last-train-to-clarksville-monkees/ | song-story | pop-brill-building | not started | Last Train to Clarksville | zSzsyqzQNeQ | yt |
| 66 | Daydream Believer | /blog/songs/daydream-believer-monkees/ | song-story | pop-brill-building | not started | Daydream Believer by The Monkees | xvqeSJlgaNk |  |
| 67 | Frank Sinatra bio | /blog/artists/frank-sinatra/ | artist-bio | jazz-easy-listening | not started | Frank Sinatra | JYuyWrkwpok |  |
| 68 | Fly Me to the Moon | /blog/songs/fly-me-to-the-moon-frank-sinatra/ | song-story | jazz-easy-listening | not started | Fly Me to the Moon | JYuyWrkwpok |  |
| 69 | Strangers in the Night | /blog/songs/strangers-in-the-night-frank-sinatra/ | song-story | jazz-easy-listening | not started | Strangers in the Night | Sek1vLw3s20 |  |
| 70 | My Way | /blog/songs/my-way-frank-sinatra/ | song-story | jazz-easy-listening | not started | My Way by Frank Sinatra | qQzdAsjWGPg |  |

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
