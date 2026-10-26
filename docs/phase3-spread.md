# Phase 3 — Spread (Nov 9 - Dec 27, 2026)

Active work queue for Phase 3 of the Sep 2026 strategy
(`docs/strategy-review-2026-09.md`). Phase 2 (`docs/phase2-decade-spine.md`)
closed out 2026-10-11 (Gate 2 met): all 16 tasks live. On This Day keeps its
own daily track (`docs/on-this-day-build.md`). Gate: the 90-day review.

Rules that still apply: CLAUDE.md in full (No Hallucination, YouTube Embed
Rule, no subagents, Charlie approves before any push to `main`, 195-line
file ceiling, competitor research before writing). Work the first task whose
status is `not started`, except tasks 3-4, which run on their own weekly clock.

Status values: `not started` · `in progress` · `blocked (reason)` · `live`

## Tasks

| # | Task | Cadence | Status |
|---|---|---|---|
| 1 | Queue rotation: `content-build.md` rows 85+ | 3-4 pages/week | not started |
| 2 | Monthly original-data page (`data-page` type, `/data/<topic-slug>/`) | 1/month | wiring built, spec awaiting approval |
| 3 | Weekly Trending post (Monday routine) | 1/week | not started |
| 4 | Weekly refresh of one existing page | 1/week | not started |

## Task detail

### 1. Queue rotation
End condition: 3-4 queue pages live per week, Nov 9 - Dec 27 (7 weeks, so
21-28 pages). Rows are worked in number order, one at a time, per CLAUDE.md
Content Pipeline. At that pace the window reaches roughly rows 85-109 of the
35 active rows (85-119); the rest carries into the 90-day review.

Rotation check (2026-10-26, rows 85-119): follows the round-robin in
`content-build.md`. Genre order is country (85-87), pop (88-91), jazz
(92-95), british (96), psychedelic (97-100), garage (101-102), folk
(103-105), motown (106-109), country (110-113), pop (114-115), jazz
(116-119). Each pass runs british, psychedelic, garage, folk, motown,
country, pop, jazz, matching the documented cycle, and continues correctly
from the last live row (Get Ready, motown).

Flag: the Patsy Cline pieces (85, 86, 87) run back to back. So does every
other cluster (e.g. Four Seasons 88-91, Jefferson Airplane 97-100). That is
by design in the rotation rule (one full artist cluster per genre per pass,
bio first). Not reordered. Charlie decides whether to interleave genres
inside a week so a single genre doesn't fill a whole week's 3-4 pages.

Minor notes, no action taken: row 96 (Small Faces) is a lone song story with
no bio row; rows 101-102 and 114-115 are two-row clusters.

### 2. Monthly original-data page (wiring built, spec awaiting approval)
New page type `data-page`, one per month, built only from our own dataset and
framed as "our dataset", never as the whole 1960s. Spec draft:
`docs/phase3-data-page-spec.md` (written, draft). Summary:

- URL `/data/<topic-slug>/`. Wiring and a DRAFT `/data/` index are in place (uncommitted); no data page exists.
- Wiring (all in the build commit): `gen/check_article.py` (new type in
  `detect_type`, `WORD_COUNT_RANGES`, year/genre link checks), `sitemap.xml`
  via `gen/generate_sitemap.py`, `data/posts.json` entry, `link-map.md` row,
  `llms.txt` via `publish_prep.py`.
- Fields allowed: only ones present in `data/songs.json` / `artists.json` /
  `genres.json`. Nothing from outside the files, no chart data.
- First page: songs per year by genre, 1960-1969, linking every
  `/1960s/<year>/` page and every live genre hub. Source: radio-eligible
  lists (434 rows, 50+ per genre), not the 192-song `songs.json` set. See spec.

### 3. Weekly Trending
Cloud routine `trig_01GCntYZh1oWceGXGBxqYKHA`, Mondays 14:00 UTC, pushes a
`trending/YYYY-MM-DD` branch only. Charlie approves before merge. Rules in
`docs/trending-posts.md`.

### 4. Weekly refresh
One existing page a week. Updated date and `dateModified` change only for
substantive edits (CLAUDE.md "Updated Dates"). Pick the page and log it here
when work starts.
