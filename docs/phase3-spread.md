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
| 2 | Monthly original-data page (`data-page` type, `/data/<topic-slug>/`) | 1/month | in progress (page 1 live; next due Nov) |
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

### 2. Monthly original-data page (page 1 live)
New page type `data-page`, one per month, built only from our own dataset and
framed as "our dataset", never as the whole 1960s. Full spec:
`docs/phase3-data-page-spec.md`. Status 2026-10-26:

- Wiring committed (20e36a0): type detection, 600-1200 words, year/genre
  link checks, sitemap carve-out for `/data/`, `posts.json` and `llms.txt`
  support, DRAFT `/data/` index, `link-map.md` row. CLAUDE.md has a pointer.
- Source list expanded (50f4c29): radio-eligible now 557 rows, every year
  43+ songs and every genre 53+. Daily pool check re-run.
- Page 1 built 2026-10-26: `/data/1960s-music-genres-by-year/` (keyword
  "1960s music genres" approved, 954 words, check_article.py PASS). Live
  2026-10-26. Rebuild with `gen/build_data_page_radio.py`,
  verify with `gen/test_data_page_radio.py`.

### Cleanup: done 2026-10-26 (a14233a)
- Checked the 1960 and 1969 candidates against Wikipedia infoboxes: all 9
  (1960) were released in 1959; Everyday People, Dizzy, Build Me Up Buttercup
  were released late 1968; One, Grazing in the Grass, Hair stay (1969);
  Proud Mary's sources disagree and it stays. Decision (Charlie): keep the
  chart-year framing, no songs removed. Every year page 1960-1969 now has a
  two-line intro note and a "Why are some songs from late <prior year>..."
  FAQ entry (visible plus FAQPage JSON-LD), with verified examples. Updated
  bumped to 2026-10-26. Examples are a shortlist, not exhaustive.

### 3. Weekly Trending
Cloud routine `trig_01GCntYZh1oWceGXGBxqYKHA`, Mondays 14:00 UTC, pushes a
`trending/YYYY-MM-DD` branch only. Charlie approves before merge. Rules in
`docs/trending-posts.md`.

### 4. Weekly refresh
One existing page a week. Updated date and `dateModified` change only for
substantive edits (CLAUDE.md "Updated Dates"). Pick the page and log it here
when work starts.
