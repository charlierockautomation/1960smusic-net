# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static site for **1960smusic.net** — genre guides, artist profiles, song stories, interactive tools. Deployed via **Cloudflare Workers (static assets)**, git-connected through Workers Builds (see `wrangler.toml`). Production branch is `main`; every push to `main` deploys automatically at 100% traffic, no dashboard promotion needed. Plain HTML/CSS, no framework, no bundler, no JS build step.

Phase 0 (data spine + policy pages) is done. `/tools/*` has four live client-side tools. `/blog/*` is a live, data-driven content system: see **Content pipeline** below before writing or placing any article.

## Commands

```bash
# Regenerate data/*.json from the gen/ source-of-truth Python modules
cd gen && python3 generate.py

# QA pass on cached YouTube ids (flags non-official-looking channels)
cd gen && python3 augment.py

# Local preview (plain static site, no build)
python3 -m http.server 8000
```

There is no test suite, linter, or JS build in this repo.

## Architecture

### Data flow: gen/ → data/*.json → static pages

The three JSON files in `/data/` (`genres.json`, `artists.json`, `songs.json`) are the single dataset every page and tool reads from. They are **generated artifacts**, not hand-edited:

- `gen/genres_data.py`, `gen/artists_data.py`, `gen/songs_data.py` hold the raw Python literals (source of truth for content).
- `gen/generate.py` imports those three, resolves each song's `youtube_id` by scraping YouTube search results and verifying via the oEmbed endpoint (confirms the video is live/embeddable), then writes the three JSON files to `/data/`. Resolved ids are cached in `gen/yt_cache.json` so re-runs only fetch new/uncached songs.
- `gen/augment.py` runs a second QA pass over `yt_cache.json`: fetches oEmbed author/title for each cached video and flags it when the channel doesn't look obviously official (not VEVO/`- Topic`/"official"/artist-name match). This sets `flagged`/`reason` in the cache, which `generate.py` surfaces on each song record as `_youtube_flagged` / `_youtube_flag_reason`.

**To change content** (add/edit an artist, song, or genre), edit the corresponding `gen/*_data.py` file, then re-run `generate.py` — do not hand-edit the JSON in `/data/` directly, it will be overwritten on the next generate.

The `_youtube_flagged` / `_youtube_flag_reason` fields on song records are QA-only scaffolding for this phase (not part of the long-term schema) and can be stripped later once every flagged song has been manually verified.

### Dataset relationship: artists vs. song performers

`artists.json` is a curated 70-artist bio roster (acts that get full profile/hub pages). `songs.json`'s 180 songs are performed by a wider set of acts, including one-hit-wonders not in the roster. Every song therefore carries its own `artist_name` (redundant with, but independent of, `artist_id`) so it can always render without a matching bio record existing. Don't assume `song.artist_id` resolves in `artists.json` — look it up defensively, or just use `artist_name` for display.

Five roster artists are reserved marquee bios with empty `notable_song_ids` (their signature songs land in a later phase) — this is valid, not a data bug.

### Page conventions (see index.html / about.html)

- Every page: `<link rel="stylesheet" href="/styles.css">`, `<link rel="canonical" href="https://1960smusic.net/...">`, standard `site-header` with `brand` + `site-nav` (`aria-current="page"` on the active link).
- Root-relative links (`/about.html`, not `about.html`).
- `_headers` sets baseline security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy) applied to `/*`; `_redirects` is intentionally empty in this phase.

## Content pipeline

Article production (genre hubs, artist bios, song stories) runs off a fixed
queue, not ad hoc requests. This is how Claude Code operates it:

1. **Read `/docs/content-build.md` first**, before writing anything. It is
   the single source of truth for what gets built next and in what order.
   Work the first `not started` row only. Never start a new row while an
   earlier one is still `in progress` or `drafted` — get one page fully
   live, tracked, and confirmed before starting the next.
2. **Research the competition before writing a word.** See
   `docs/writing-standard.md` → "Content completeness". Find the top 3
   currently-ranking pages for the focus keyword, read all 3, note every
   true fact and subtopic they cover. This is mandatory pre-writing
   research, not an optional polish pass done after a draft exists. The
   target for every article is to beat all 3 of those pages: more
   complete, more accurate, better written.
3. **Build with `/docs/article-template.html`** as the shell. Pull facts
   from `data/songs.json` and `data/artists.json` first, then fold in
   everything found in step 2, using web search to verify and fill
   further gaps (dates, chart facts, sourced quotes). Never invent
   history, quotes, or trivia — this is a standing site rule, not new
   for the pipeline.
4. **`gen/check_article.py` is the formatting/structure gate.** Run it on
   the built page; if it fails, fix the article and rerun until it PASSes.
   Never bring a formatting or structure question to Charlie — the
   template, `docs/writing-standard.md`, and check_article.py already
   define all of it. Do not commit on a FAIL.
5. **Two required human checkpoints, no others:** Charlie gives the
   go-ahead to start a session, and Charlie gives explicit approval
   before any page is pushed to `main` (which is what makes it live, see
   above). Build, validate, and present the page (e.g. via a local
   server) for that approval — don't push unprompted, and don't wait on
   Charlie for anything else in between.
6. **Once live and confirmed** (page responds 200 at its live URL), in
   the same session update all four, in order: `docs/content-build.md`
   (status → `live`), `data/posts.json` (add the entry — this is what
   makes it show up on `/blog/` and its category archive automatically,
   see `blog/shared.js`), `link-map.md` (status → `live`, live URL,
   inbound/outbound links), then regenerate `sitemap.xml` by running
   `python3 gen/generate_sitemap.py` (reads `data/posts.json` and
   `data/tools.json`; do this after `posts.json` is updated, not
   before) and commit/push the new `sitemap.xml` alongside the tracker
   updates. Only then move to the next queue row.
