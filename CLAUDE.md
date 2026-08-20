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

---
Reference docs (loaded only when the task needs them):
@docs/architecture.md · @docs/content-build.md · @docs/writing-standard.md · @link-map.md
