# Phase 1 — Foundations (Sep 28 - Oct 11, 2026)

Active work queue for Phase 1 of the Sep 2026 strategy
(`docs/strategy-review-2026-09.md`). Approved by Charlie Sep 27, 2026:
**Phase 1 tasks run BEFORE new `docs/content-build.md` rows.** The On This
Day daily minimum (1/day, target 2/day through October) continues in
parallel on its own track.

Rules that still apply: CLAUDE.md in full (No Hallucination, YouTube Embed
Rule, no subagents, multiple tasks per session allowed if each is closed
out cleanly before the next starts, Charlie approves before any push to
`main`, 195-line file ceiling). Work the first task whose status is
`not started`. Update its status here in the same session it goes live.

Status values: `not started` · `in progress` · `blocked (reason)` · `live`

## Tasks

| # | Task | Status |
|---|---|---|
| 1 | Static HTML listing pages | live |
| 2 | Homepage: crawlable links to hubs, tools, latest OTD; real share links | live |
| 3 | URL + response audit (redirects, trailing slash, .html vs extensionless) | live |
| 4 | 404.html page | live |
| 5 | Byline, Published/Updated dates, author schema on every article | live |
| 6 | Author page /about/charlie/ + About rewrite | live |
| 7 | Schema audit per page type | live |
| 8 | Image alt-text rule in check_article.py + backfill | live |
| 9 | Trending clean-up (Dolly Parton retitle + 301, "1960s rock legends") | in progress |
| 10 | IndexNow ping on deploy | blocked (Charlie adds site to Bing first) |

## Task detail

Tasks 1-7 are all `live`; their write-ups moved to
[`docs/phase1-foundations-archive.md`](phase1-foundations-archive.md) to
keep this file under the line ceiling.

### 8. Alt text
Done: `check_article.py` now fails per-image (not just "at least one alt
present") when an `<img>`'s alt is empty, matches its filename, or is
identical to its figcaption. Ran against every live artist/song/genre/
trending page: zero gaps found, so no backfill edits were needed.

### 9. Trending clean-up
Charlie's decision (2026-09-28): retitle around her 1960s career, confirmed.
- Done: new page at `/blog/trending/dolly-parton-dumb-blonde/`. Facts
  verified via web search: "Dumb Blonde" (Curly Putman, Monument Records,
  1966 release) was her first Billboard Hot Country Songs entry, No. 64 on
  Jan 21 1967, peaked No. 24 on Mar 18 1967, on her 1967 debut album
  `Hello, I'm Dolly`; she replaced Norma Jean on The Porter Wagoner Show
  after Norma Jean left in Aug 1967, first TV appearance Sep 5 1967, 218
  episodes over 7 years. "Why it's trending now" module uses her real,
  sourced Aug 2026 post-death streaming surge (Billboard/Variety: catalog
  +1,143% US week-over-week, world's most-streamed artist Aug 26 with 79.7M
  global streams) plus the same TikTok tribute embed already confirmed
  rendering on the old live page (reused rather than sourcing a new one:
  this environment's network egress blocks tiktok.com outright, so a new
  clip's metadata/render couldn't be verified per writing-standard.md).
  check_article.py PASSes (686 words, density, keyword placement, sentence
  rules all clean). `_redirects` now 301s the old URL to the new one.
  posts.json, link-map.md, sitemap.xml, llms.txt, and both blog listing
  pages regenerated. Old `/blog/trending/dolly-parton-dead/` directory
  removed. Confirmed the death itself is real (NPR/CNN/Wikipedia, Aug 25
  2026) before touching any of this, since the page makes that claim.
  Merged to `main` 2026-09-28 with Charlie's go-ahead. Charlie confirmed
  both URLs live in production: new page returns 200, old
  `/blog/trending/dolly-parton-dead/` 301s to it.
- Still open: the "1960s rock legends" half of this row hasn't been
  looked at yet.

### 10. IndexNow (blocked)
After Charlie imports the site into Bing Webmaster Tools: generate an
IndexNow key file at the root and ping changed URLs after each deploy.

## Charlie's own Phase 1 tasks (dashboard work, not Claude Code)
- GA4 internal-traffic filter (steps in the Claude Doc, fix 7)
- Bing Webmaster Tools: import from GSC
- GSC: Redirect error → Validate fix; after tasks 1-2 go live, URL
  Inspection → Request indexing for /blog/ and the 5 category pages
- Cloudflare: screenshot AI Crawl Control → Metrics 3xx and 4xx views, and
  Security → Settings → Bot Fight Mode
- Author page facts; Dolly Parton decision; row 62 decision

## Gate 1 (target Oct 11)
Every listing page and the homepage pass the view-source link test, bylines
and dates are live on every article, 404 page live. Then Phase 2
(year pages, best 60s songs, 60s rock, homepage rebuild) gets its own file.
