# Context Budget (reference, read on demand; moved from CLAUDE.md 2026-11-13)

The guard rule itself stays in CLAUDE.md "Context Budget". This file holds the
reference: which docs auto-load, which are read on demand and when, and the
audit history. Update it whenever an `@` import is added or removed.

## Auto-loaded (via `@` in CLAUDE.md), 2026-11-13

| File | Chars |
|---|---|
| ~/.claude/CLAUDE.md (global) | 7,714 |
| CLAUDE.md | 9,484 |
| docs/content-build.md | 7,388 |
| docs/architecture.md | 7,225 |
| docs/writing-standard.md | 6,643 |
| docs/trending-posts.md | 3,281 |
| docs/singles-table.md | 2,999 |
| docs/genre-hub-linking.md | 1,418 |

Measure: `wc -m ~/.claude/CLAUDE.md CLAUDE.md docs/{content-build,architecture,writing-standard,trending-posts,singles-table,genre-hub-linking}.md`

## Read on demand only (never import)

| File | Read when |
|---|---|
| `link-map.md` | Before adding or editing internal links; post-push (pipeline step 6), add the page's row. At 195 lines rotate oldest rows to `link-map-archive.md`. |
| `docs/strategy-review-2026-09.md` | Planning work: why the site changed course, roadmap, baseline metrics, full GEO/AI-citation rules. |
| `docs/phase1-foundations.md` | Closed Phase 1 history; Charlie's own open dashboard tasks (GA4 internal filter). |
| `docs/phase2-decade-spine.md` | Before editing a year page or the `/1960s/` hub (year-page tracker discipline). |
| `docs/phase3-data-page-spec.md` | Before building a data page (spec rule, keyword method, next page due). |
| `docs/context-budget.md` | This file: before adding or removing an `@` import. |
| `docs/content-build-archive.md` | Live queue rows, weekly refresh log (add new refresh rows there), done follow-ups. |
| `docs/on-this-day-build.md` | On This Day work (its header gives the workflow). |

## Audit history

2026-11-13: startup warning, 13 auto-loaded files = 152.2k chars (limit 150k):
link-map.md 64.6k, content-build.md 15.3k, writing-standard.md 10.9k,
CLAUDE.md 10.4k, global CLAUDE.md 8.3k, phase2 8.1k, phase3 spec 7.6k,
strategy review 7.5k, architecture 7.2k, phase1 5.9k, singles-table 3.0k,
trending-posts 1.9k, genre-hub-linking 1.4k. Cut to 47.6k (commit 28ab917),
then the global file's duplicate workspaces block removed (8,257 → 7,714).
