# Phase 2 — Decade Spine: Archive

Detail write-ups rotated out of `docs/phase2-decade-spine.md` to keep it
under the 195-line ceiling (CLAUDE.md File Size Ceiling rule). Task
statuses live in the active file's table; this file only holds the
build notes for tasks whose detail no longer needs to stay in working
memory.

## Task 1 detail: Year page template + schema design

Design the shared shell for `/1960s/<year>/` before building any single
year, so all 10 stay structurally identical (matches how
`article-template.html` works for the other content types):
- Answer-first intro: year + defining fact + a number, in the first 60
  words (GEO rule 1 in the strategy review).
- Sections: US #1 hits that year (table: title, artist, chart, peak,
  weeks), key albums released, notable events (link out to the
  matching `/blog/on-this-day/<month>-<day>/` page wherever one
  exists), genre shifts that year, "Play <year>" radio filter link
  (`/tools/radio/?year=<year>`, check whether `radio-app.js` supports a
  year filter yet or whether that needs its own small task first).
- Schema: Article + ItemList (the year's #1s) + BreadcrumbList, author
  Person + datePublished/dateModified per the Phase 1 task 5/7 pattern.
- Internal links: up to the homepage and to `/best-60s-songs/` and
  `/blog/genres/60s-rock/` once those exist; across to every OTD page
  already live for that year (query `data/*.json` / OTD tracker for
  matches) and any genre hub whose era overlaps.
- Word count / density rules: use the base Structure section of
  `writing-standard.md` (no type-specific range is defined yet for
  "year page" in `check_article.py`; add one, sized after seeing how
  long a real year page runs, then keep every year page in that range).
- Facts only from `data/songs.json`/`data/artists.json` plus verified
  web search (Billboard/Official Charts year-end lists), same
  no-hallucination bar as every other page type.

Done: shell built at `docs/year-page-template.html`, same
placeholder/comment convention as `article-template.html`. Sections in
fixed order: lead, image, TOC, US #1 Hits table, Key Albums, Notable
Events, Genre Shifts, Play-on-radio CTA, FAQ, closing links. Schema:
Article (author Person, datePublished/dateModified) + ItemList (#1
hits) + BreadcrumbList (2-level, Home > Year, no mid-tier hub exists
yet) + FAQPage. `gen/check_article.py` now detects `/1960s/` paths as
type `year page`; no word-count range added yet, sizing deferred to
the first real page (task 2) per the note above.
Checked `radio-app.js` 2026-09-29: it only read a `?station=` query
param, no year filtering. Built the filter same session
(`tools/radio/radio-year.js`, wired into `tools/radio/index.html`):
on `?year=<1960-1969>` it narrows each enabled station's song pool to
that year in place (overwrites `radio-app.js`'s shared `cache`, so
Play/Skip/Select all stay within-year for free), using the `year`
field already present on every `data/radio-eligible-*.json` entry. A
genre with zero songs for that year is left unfiltered rather than
made unplayable (verified against real data: e.g. 1963 has matches in
7 of 8 genres, psychedelic-rock correctly has none since that hub
doesn't start until 1965). Logic and data shape verified via a Node
script; full browser playback not spot-checked this session.
Up-links to `/best-60s-songs/` and `/blog/genres/60s-rock/` are noted
in the template as omit-until-live (tasks 12/13), not linked yet.

Note: the BreadcrumbList this task shipped was 2-level (Home > Year,
"no mid-tier hub exists yet"). Task 16 (`/1960s/` hub) later added that
mid-tier: every year page's breadcrumb is now 3-level (Home > 1960s >
Year), see `docs/phase2-decade-spine.md` task 16 for when/why.
