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

**Current priority (Sep 29, 2026):** Phase 1 closed, all 10 tasks live.
`docs/phase2-decade-spine.md` before new queue rows; On This Day daily
minimum continues. Why: `docs/strategy-review-2026-09.md`.

## Commands

Regenerate data: `cd gen && python3 generate.py`. YouTube QA: `cd gen &&
python3 augment.py`. Preview: `python3 -m http.server 8000`. No test suite,
linter, or JS build.

## Data Rules

- Never hand-edit `/data/*.json` — it's generated from `gen/*_data.py` and
  overwritten on the next `generate.py` run. Edit the source `_data.py` file,
  then regenerate.
- `song.artist_id` does not always resolve in `artists.json` — look it up
  defensively, or just use `song.artist_name` for display. Don't assume every
  song has a matching bio.
- Full data flow (gen/ → data/*.json → pages), the artists-vs-song-performers
  relationship, and page-template conventions: @docs/architecture.md

## YouTube Embed Rule — ABSOLUTE

Every embed must be visible, unobscured, and at/above YouTube's minimum
size (200x200px, 480x270 for 16:9); never a hidden/background player.
`check_article.py` checks that song/artist pages carry an embed; the
visibility and size rules above are a manual check for every type.

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
3. **Key Facts data first (song/artist).** Before writing, add the page's
   entry to `gen/key_facts_data.py` with verified facts only (omit anything
   unconfirmed). `check_article.py` FAILs a song/artist page with no entry or
   a box that doesn't match it. Then build with `/docs/article-template.html`
   as the shell: facts from `data/songs.json` / `data/artists.json`, then
   competitor research, then web search to verify gaps. Never invent history,
   quotes, or trivia. Run `gen/build_key_facts.py --write` for the box.
4. **`gen/check_article.py` is the formatting/structure gate.** It FAILs a
   page missing any of: title ≤60 chars; visible "Updated" = JSON-LD
   dateModified; `og:image` and JSON-LD `image` (absolute, file exists); Key
   Facts box (song/artist); a `/1960s/<year>/` link (song: its release year;
   artist: key years; trending: at least one; genre hub: every year in
   `gen/genre_peak_years.py`; On This Day: one in each year section);
   `/best-60s-songs/` if the song is listed; canonical `/about/`-style legal
   links. Run it on the built page; fix and rerun until it PASSes. Never bring
   a formatting or structure question to Charlie. Do not commit on a FAIL.
5. **Pre-push gate, in this order, any failure blocks the push:**
   (a) `python3 gen/check_article.py <new page>`; (b) add the `data/posts.json`
   entry; (c) `python3 gen/publish_prep.py` (listings, `sitemap.xml`,
   `llms.txt`, `check_article.py --site`, then `validate_jsonld.py --all`).
   A page not meant to be indexed yet carries `<!-- DRAFT -->` or `noindex`.
   Then the **two required human checkpoints, no others:** Charlie's go-ahead
   to start a session, and Charlie's explicit approval before any push to
   `main`. Present the page (local server) for it. Don't push unprompted.
6. **Post-push, same session:** (a) `python3 gen/verify_live.py --last-commit`
   (or pass the URLs): each must be HTTP 200 and in the live `sitemap.xml` and
   `llms.txt`; retry after a minute if the deploy is still building; report
   the output. (b) `python3 gen/indexnow_ping.py <new-page-url>`. (c) Update,
   in order: `docs/content-build.md` (status → `live`), `link-map.md` (status,
   live URL, inbound/outbound links); commit/push those. Only then move to the
   next queue row.

## Updated Dates

Visible "Updated" and JSON-LD `dateModified` change only for substantive
content edits (facts, prose, new sections). Link, image, markup, or SEO-plumbing
changes never bump them.

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
(`/blog/genres/pop-brill-building/`), **Jazz & Easy Listening**
(`/blog/genres/jazz-easy-listening/`), **60s Rock umbrella**
(`/blog/genres/60s-rock/`, links down to the rock hubs above; cross-link
it from British Invasion, Garage & Surf, Folk Rock, and Psychedelic).

- Any artist bio or song story whose genre matches a live hub links up to
  that hub (see existing convention in `link-map.md`).
- The moment a new hub goes live, add it to this list in the same commit —
  don't batch several hubs and update the list once at the end.
- Once a hub is added here it's eligible for linking from all live content
  in that genre, not just pages written after the hub shipped — if an
  already-live article's genre matches a newly-added hub and doesn't yet
  link to it, that's a gap worth closing, not something grandfathered in.

## Content Rotation

New `docs/content-build.md` rows round-robin across the 8 genres in
`data/genres.json`; never stack many rows of one genre. Applies to future
rows only, not rows already locked into the active queue.

## File Size Ceiling

Every tracker/doc file in `docs/` (and CLAUDE.md) stays at or under **195
lines** (hard ceiling 199). When a file would cross 195, rotate content out:
keep an active file and push done rows to an archive or a numbered overflow
chain (`-queued.md`, `-queued-2.md`, ...), as `docs/content-build.md` and
`docs/on-this-day-build.md` already do. Each paginating file names its
successor in its header; update every affected header when content moves.

## On This Day Pace

Minimum one On This Day date page live per day once the series is in
active production. `docs/on-this-day-build.md` is the active queue for
this series (see its own header for the current workflow).

## Trending Posts

`/blog/trending/` (1960s songs/artists resurging in modern culture): same
pipeline as above, plus a live TikTok embed, a real-photo feature image
(never AI-generated), 400-700 words, and at least one `/1960s/<year>/`
link. Full rules: @docs/trending-posts.md. Charlie requests each post
individually; there is no rotation queue.

## No Subagents, Site-Wide

Never use the Agent/Task tool (subagents, forks, delegation) for any
work on this site. Direct single-session work only, including all
research (use WebSearch/WebFetch inline), for every content type and
every task, not only the series where this was first decided.

## Session Discipline

Multiple tasks per session are fine when they can be done cleanly, one at
a time, each fully closed out (built, checked, approved, pushed, tracker
updated) before the next one starts. Don't hold a queue open waiting for
Charlie's pick when the tracker already states order; work the next
unblocked row and continue until the queue runs out, a task needs
Charlie's decision, or something isn't going cleanly — then stop. No
narration flourishes (session timers, recap paragraphs) unless asked.
End each session on a closed status report, not an open question.

---
Reference docs (loaded only when the task needs them):
@docs/phase2-decade-spine.md · @docs/phase1-foundations.md · @docs/strategy-review-2026-09.md · @docs/trending-posts.md · @docs/architecture.md · @docs/content-build.md · @docs/writing-standard.md · @link-map.md
