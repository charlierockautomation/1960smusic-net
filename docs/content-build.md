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
3. For a song or artist, add its verified entry to `gen/key_facts_data.py`
   BEFORE writing (check_article.py fails without it). Run
   `python3 gen/check_article.py <path>` before committing. If it fails,
   fix the article and rerun. Do not commit on a FAIL, and do not ask
   Charlie to fix formatting or structure.
4. Pre-push gate: add the `data/posts.json` entry, then run
   `python3 gen/publish_prep.py` (listings, sitemap, llms.txt, site check,
   `validate_jsonld.py --all`). Any failure blocks the push. Build locally,
   run a local server, and get Charlie's explicit go-ahead before pushing
   to `main` (see `wrangler.toml` / Cloudflare Workers Builds).
5. Post-push, same session: `python3 gen/verify_live.py --last-commit`
   (200 + in live sitemap.xml and llms.txt), then update this file (status
   → `live`) and `link-map.md` (status → `live`, live URL, inbound/outbound
   links). Only then move to the next `not started` row.

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

Row 62 ("I Walk the Line") was dropped, not reframed: Charlie's decision
2026-09-29. It's a 1956 song and this site is strictly 1960-1969. The
number is retired, not reused; row 63 onward keeps its existing number.

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

Live rows (1-70) are in [`docs/content-build-archive.md`](content-build-archive.md).

| # | Title | Slug | Type | Genre | Status | Focus Keyword | YouTube ID | Flag |
|---|-------|------|------|-------|--------|----------------|------------|------|
| 71 | A World Without Love | /blog/songs/a-world-without-love-peter-and-gordon/ | song-story | british-invasion | live | A World Without Love | ke4hgo43JGc | swapped from Tdx6lLvvRyg (non-official) |
| 72 | The Jimi Hendrix Experience bio | /blog/artists/the-jimi-hendrix-experience/ | artist-bio | psychedelic-rock | live | The Jimi Hendrix Experience | WGoDaYjdfSg |  |
| 73 | Purple Haze | /blog/songs/purple-haze-jimi-hendrix-experience/ | song-story | psychedelic-rock | live | Purple Haze by The Jimi Hendrix Experience | WGoDaYjdfSg |  |
| 74 | Hey Joe | /blog/songs/hey-joe-jimi-hendrix-experience/ | song-story | psychedelic-rock | live | Hey Joe by The Jimi Hendrix Experience | rXwMrBb2x1Q |  |
| 75 | The Sonics bio | /blog/artists/the-sonics/ | artist-bio | garage-surf-rock | live | The Sonics | HGBsxpnRhMk |  |
| 76 | The Witch | /blog/songs/the-witch-sonics/ | song-story | garage-surf-rock | live | The Witch by The Sonics | HGBsxpnRhMk |  |
| 77 | Have Love, Will Travel | /blog/songs/have-love-will-travel-sonics/ | song-story | garage-surf-rock | not started | Have Love, Will Travel | SV9N7TbIzcE |  |
| 78 | Simon & Garfunkel bio | /blog/artists/simon-and-garfunkel/ | artist-bio | folk-rock | not started | Simon & Garfunkel | 4fWyzwo1xg0 |  |
| 79 | The Sound of Silence | /blog/songs/the-sound-of-silence-simon-and-garfunkel/ | song-story | folk-rock | not started | The Sound of Silence | 4fWyzwo1xg0 |  |
| 80 | The Boxer | /blog/songs/the-boxer-simon-and-garfunkel/ | song-story | folk-rock | not started | The Boxer by Simon & Garfunkel | l3LFML_pxlY |  |
| 81 | Scarborough Fair/Canticle | /blog/songs/scarborough-fair-canticle-simon-and-garfunkel/ | song-story | folk-rock | not started | Scarborough Fair/Canticle by Simon & Garfunkel | -Jj4s9I-53g |  |
| 82 | The Temptations bio | /blog/artists/the-temptations/ | artist-bio | motown-soul | not started | The Temptations | y3KJ7d2qBoA |  |
| 83 | My Girl | /blog/songs/my-girl-temptations/ | song-story | motown-soul | not started | My Girl by The Temptations | y3KJ7d2qBoA |  |
| 84 | Get Ready | /blog/songs/get-ready-temptations/ | song-story | motown-soul | not started | Get Ready by The Temptations | mhsYOzdJjI0 |  |
| 85 | Patsy Cline bio | /blog/artists/patsy-cline/ | artist-bio | country-60s | not started | Patsy Cline | YWKeuYcDAoo |  |
| 86 | Crazy | /blog/songs/crazy-patsy-cline/ | song-story | country-60s | not started | Crazy by Patsy Cline | YWKeuYcDAoo |  |
| 87 | I Fall to Pieces | /blog/songs/i-fall-to-pieces-patsy-cline/ | song-story | country-60s | not started | I Fall to Pieces | gEcZ8BlsJhI |  |
| 88 | The Four Seasons bio | /blog/artists/the-four-seasons/ | artist-bio | pop-brill-building | not started | The Four Seasons | GzoIvwNqKpw | yt |
| 89 | Walk Like a Man | /blog/songs/walk-like-a-man-four-seasons/ | song-story | pop-brill-building | not started | Walk Like a Man | GzoIvwNqKpw | yt |
| 90 | Big Girls Don't Cry | /blog/songs/big-girls-dont-cry-four-seasons/ | song-story | pop-brill-building | not started | Big Girls Don't Cry | zRZpaxBMJRU | yt |
| 91 | Sherry | /blog/songs/sherry-four-seasons/ | song-story | pop-brill-building | not started | Sherry by The Four Seasons | jMcWldfg28s | yt |
| 92 | Herb Alpert & The Tijuana Brass bio | /blog/artists/herb-alpert-and-the-tijuana-brass/ | artist-bio | jazz-easy-listening | not started | Herb Alpert & The Tijuana Brass | NC38-qqiVgg | yt |
| 93 | A Taste of Honey | /blog/songs/a-taste-of-honey-herb-alpert-and-the-tijuana-brass/ | song-story | jazz-easy-listening | not started | A Taste of Honey | NC38-qqiVgg | yt |
| 94 | Spanish Flea | /blog/songs/spanish-flea-herb-alpert-and-the-tijuana-brass/ | song-story | jazz-easy-listening | not started | Spanish Flea by Herb Alpert & The Tijuana Brass | aBE9EQ7gXKI |  |
| 95 | This Guy's in Love with You | /blog/songs/this-guys-in-love-with-you-herb-alpert-and-the-tijuana-brass/ | song-story | jazz-easy-listening | not started | This Guy's in Love with You | o8ByJ1C0iR4 |  |
| 96 | Sha La La La Lee | /blog/songs/sha-la-la-la-lee-small-faces/ | song-story | british-invasion | not started | Sha La La La Lee | JsuKmqQyYR4 | yt |
| 97 | Jefferson Airplane bio | /blog/artists/jefferson-airplane/ | artist-bio | psychedelic-rock | not started | Jefferson Airplane | pnJM_jC7j_4 |  |
| 98 | White Rabbit | /blog/songs/white-rabbit-jefferson-airplane/ | song-story | psychedelic-rock | not started | White Rabbit by Jefferson Airplane | pnJM_jC7j_4 |  |
| 99 | Somebody to Love | /blog/songs/somebody-to-love-jefferson-airplane/ | song-story | psychedelic-rock | not started | Somebody to Love | a-C9pUGszsw |  |
| 100 | Wooden Ships | /blog/songs/wooden-ships-jefferson-airplane/ | song-story | psychedelic-rock | not started | Wooden Ships by Jefferson Airplane | ROBaoiJK0wc |  |
| 101 | Dick Dale bio | /blog/artists/dick-dale/ | artist-bio | garage-surf-rock | not started | Dick Dale | MXB6T55oytE |  |
| 102 | Miserlou | /blog/songs/miserlou-dick-dale/ | song-story | garage-surf-rock | not started | Miserlou by Dick Dale and His Del-Tones | MXB6T55oytE |  |
| 103 | The Byrds bio | /blog/artists/the-byrds/ | artist-bio | folk-rock | not started | The Byrds | NxyOhFBoxSY |  |
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
