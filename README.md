# 1960smusic.net

A static website celebrating the music of the 1960s — genre guides, artist
profiles, song stories and interactive tools. Built to be hosted on
**Cloudflare Pages** (GitHub-connected, static deploy — same pattern as
musicofthe70s.net).

## Status: Phase 0 — Foundation

This phase delivers the data spine and the structural/policy pages only.
**No tool pages or blog content are built yet, and nothing links to those
sections** — empty, unlinked shells only exist as folders for later phases.

### What's live in this phase
- `index.html` — Home
- `about.html`, `contact.html`, `privacy-policy.html`, `terms-of-use.html`
- `styles.css` — shared stylesheet
- `data/genres.json`, `data/artists.json`, `data/songs.json` — the master dataset

### Repository layout
```
/                     Home + policy pages, styles.css, _headers, _redirects
/data/                genres.json, artists.json, songs.json
/blog/                genres/ artists/ songs/ trending/ on-this-day/   (empty scaffold)
/tools/               radio/ daily/ sample-detective/ real-or-revival/
                      quiz/ trivia/ crossword/ playlist-builder/       (empty scaffold)
/gen/                 dataset generator scripts (build-time only, not deployed content)
```

## The dataset

Every tool and page on the site reads from the same three JSON files in
`/data/`:

| File | Records | Notes |
|------|---------|-------|
| `genres.json` | 8 | id, name, slug, description, defining_sound, years_active, key_artist_ids |
| `artists.json` | 70 | id, name, genre_ids, active_years, origin, bio_short, notable_song_ids, article_slug |
| `songs.json` | 180 | full schema incl. artist_name, youtube_id, mood_tags, trivia_facts, difficulty, etc. |

### Artist roster vs. song performers
`artists.json` is the **70-artist bio roster** — the acts that get full artist
profiles / hub pages. The 180 songs are performed by a wider set of acts
(including one-hit-wonders and secondary performers such as ? and the
Mysterians, The Surfaris, Iron Butterfly, The Archies). So that every song can
always be displayed without depending on a bio record existing, each song
carries an additive `artist_name` field alongside `artist_id`. A song whose
`artist_id` is not in the 70-artist roster is expected and fully supported —
its `artist_name` provides the display value, and a bio can be promoted into
the roster later. Five roster artists are reserved marquee bios whose signature
songs land in a later content phase, so their `notable_song_ids` is currently
empty (valid per schema).

### YouTube IDs
Song `youtube_id` values were resolved by searching YouTube and verifying each
candidate via YouTube's oEmbed endpoint (which confirms the video is live and
embeddable). Two internal QA fields accompany each song:

- `_youtube_flagged` (bool) — `true` when the automatically chosen video could
  not be confidently matched to the intended title + artist and should be
  spot-checked.
- `_youtube_flag_reason` (string|null) — why it was flagged.

These two underscore-prefixed fields are **not** part of the master spec
schema; they exist only for this phase's human review and can be stripped later.

## Regenerating the data
```bash
cd gen
python3 generate.py        # rebuilds ../data/*.json (re-fetches uncached YouTube IDs)
```
Resolved YouTube IDs are cached in `gen/yt_cache.json` so re-runs are fast.

## Local preview
It's a plain static site — open `index.html` directly, or serve the root:
```bash
python3 -m http.server 8000
```

## Deployment (Cloudflare Pages)
Connect this repository to Cloudflare Pages with **no build command** and the
repository root as the output directory. `_headers` sets baseline security
headers; `_redirects` is intentionally empty for now.
