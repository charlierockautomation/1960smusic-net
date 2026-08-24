# CLAUDE.md
# Read this file at the start of EVERY session. This is the current rule only —
# full detail lives in /docs/. Pull a doc in with @ only when the task actually
# needs it; none of /docs/ auto-loads.

## What this is

Static site for **1960smusic.net** — genre guides, artist profiles, song
stories, interactive tools. Deployed via Cloudflare Workers (static assets),
git-connected through Workers Builds (see `wrangler.toml`). Production branch
is `main`; every push to `main` deploys automatically at 100% traffic, no
dashboard promotion needed. Plain HTML/CSS, no framework, no bundler, no JS
build step.

Phase 0 (data spine + policy pages) is done. `/tools/*` has four live
client-side tools. `/blog/*` is a live, data-driven content system.

## Commands

```bash
# Regenerate data/*.json from the gen/ source-of-truth Python modules
cd gen && python3 generate.py

# QA pass on cached YouTube ids (flags non-official-looking channels)
cd gen && python3 augment.py

# Local preview (plain static site, no build)
python3 -m http.server 8000
```

No test suite, linter, or JS build in this repo.

## Data Rules

- Never hand-edit `/data/*.json` — it's generated from `gen/*_data.py` and
  overwritten on the next `generate.py` run. Edit the source `_data.py` file,
  then regenerate.
- `song.artist_id` does not always resolve in `artists.json` — look it up
  defensively, or just use `song.artist_name` for display. Don't assume every
  song has a matching bio.
- Full data flow (gen/ → data/*.json → pages), the artists-vs-song-performers
  relationship, and page-template conventions: @docs/architecture.md

## No Hallucination Rule — ABSOLUTE

Never invent dates, chart positions, quotes, tour details, member tenures, or
awards. Unconfirmed = omit or flag as unconfirmed, never guess.

## Content Pipeline

Article production (genre hubs, artist bios, song stories) runs off a fixed
queue, not ad hoc requests.

1. **Read `/docs/content-build.md` first**, before writing anything — it is
   the single source of truth for what gets built next. Work the first
   `not started` row only. Never start a new row while an earlier one is
   still `in progress` or `drafted`.
2. **Research the competition before writing a word.** See
   `docs/writing-standard.md` → "Content completeness". Find the top 3
   currently-ranking pages for the focus keyword, read all 3, note every true
   fact and subtopic they cover. This is mandatory pre-writing research, not
   an optional polish pass.
3. **Build with `/docs/article-template.html`** as the shell. Facts from
   `data/songs.json` / `data/artists.json` first, then competitor research,
   then web search to verify and fill remaining gaps. Never invent history,
   quotes, or trivia.
4. **`gen/check_article.py` is the formatting/structure gate.** Run it on
   the built page; fix and rerun until it PASSes. Never bring a formatting or
   structure question to Charlie — the template, `docs/writing-standard.md`,
   and check_article.py already define all of it. Do not commit on a FAIL.
5. **Two required human checkpoints, no others:** Charlie gives the go-ahead
   to start a session, and Charlie gives explicit approval before any page is
   pushed to `main`. Build, validate, and present the page (e.g. local
   server) for that approval — don't push unprompted, don't wait on Charlie
   for anything else in between.
6. **Once live and confirmed** (page responds 200 at its live URL), in the
   same session update all four, in order: `docs/content-build.md` (status →
   `live`), `data/posts.json` (new entry — this is what makes it show up on
   `/blog/` and its category archive, see `blog/shared.js`), `link-map.md`
   (status → `live`, live URL, inbound/outbound links), then regenerate
   `sitemap.xml` (`python3 gen/generate_sitemap.py`, after `posts.json` is
   updated, not before) and commit/push the new `sitemap.xml` alongside the
   tracker updates. Only then move to the next queue row.

## Content Quality & Site-Strengthening Standard

Every new page must clear `gen/check_article.py` (formatting/structure) and
`docs/writing-standard.md` (competitive research, density, prose rules) in
full, no exceptions and no partial passes committed. Beyond that bar, prefer
work that strengthens the existing site over net-new isolated pages: add
internal links where a genuine connection exists (see Genre Hub Linking
below), keep trackers (`link-map.md`, `docs/content-build.md`,
`data/posts.json`) accurate the same session a page goes live, and don't
leave a page orphaned (unlinked from any hub or bio) once something it
should link to exists.

## Genre Hub Linking

A genre hub is "eligible" for linking once it is live. Eligible hubs
currently: **British Invasion** (`/blog/genres/british-invasion/`),
**Motown, Soul & R&B** (`/blog/genres/motown-soul/`), **Folk Rock**
(`/blog/genres/folk-rock/`), **Psychedelic Rock**
(`/blog/genres/psychedelic-rock/`), **Garage & Surf Rock**
(`/blog/genres/garage-surf-rock/`), **Country (Nashville Sound &
Bakersfield)** (`/blog/genres/country-60s/`), **Pop & Brill Building**
(`/blog/genres/pop-brill-building/`).

- Any artist bio or song story whose genre matches a live hub links up to
  that hub (see existing convention in `link-map.md`).
- The moment a new hub goes live, add it to this list in the same commit —
  don't batch several hubs and update the list once at the end.
- Once a hub is added here it's eligible for linking from all live content
  in that genre, not just pages written after the hub shipped — if an
  already-live article's genre matches a newly-added hub and doesn't yet
  link to it, that's a gap worth closing, not something grandfathered in.

## Content Rotation

New rows added to `docs/content-build.md` should round-robin across the 8
genres in `data/genres.json` rather than stacking many rows of one genre
back to back, so no single genre gets fully built out while others sit
untouched. This governs how *future* rows get queued, it does not mandate
reordering rows already locked into the active queue.

## File Size Ceiling

Tracker/doc files in `docs/` stay under 199 lines. When a file crosses
that line, split it into an active file (what's in progress/next) and an
archive or overflow file (done, or paginated-out future rows), the way
`docs/content-build.md` / `docs/content-build-archive.md` and
`docs/on-this-day-build.md` / `docs/on-this-day-build-queued.md` already
do. Update the file's own header to say what got split out and where.

## On This Day Pace

Minimum one On This Day date page live per day once the series is in
active production. `docs/on-this-day-build.md` is the active queue for
this series (see its own header for the current workflow).

## Trending Posts

`/blog/trending/` covers 1960s songs/artists resurging in modern
culture (TikTok, streaming, sync placements). Same content pipeline
as every other type above, plus:

- Word count target: 400-700 words. Trending-specific structure and
  the mandatory "why it's trending now" module are in
  `docs/writing-standard.md`.
- Live TikTok embed (blockquote + `tiktok.com/embed.js`) required,
  placed where it's contextually relevant. Confirm it actually
  renders before marking the page done, don't assume the markup is
  enough. This repo's dev sandbox cannot always reach TikTok's video
  CDN, so a local check can show a correctly-built but blank embed;
  spot-check the live URL after deploy the same way On This Day
  YouTube ids get spot-checked.
- Feature image is a real photo, never AI-generated, even when the
  viral source clip itself uses an AI-generated image. Prefer a
  freely-licensed photo of the artist (Wikimedia Commons first). If
  none exists, fall back to editorial-context single/album cover art,
  then non-person period-appropriate stock imagery, in that order.
  Note which tier was used when reporting the page as done.
- No rotation queue yet, unlike `docs/content-build.md`. Charlie
  requests each Trending post individually until one exists.

## No Subagents, Site-Wide

Never use the Agent/Task tool (subagents, forks, delegation) for any
work on this site. Direct single-session work only, including all
research (use WebSearch/WebFetch inline), for every content type and
every task, not only the series where this was first decided.

---
Reference docs (loaded only when the task needs them):
@docs/architecture.md · @docs/content-build.md · @docs/writing-standard.md · @link-map.md
