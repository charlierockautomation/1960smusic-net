# Strategy Review — 1960smusic.net (Sep 27, 2026)

Source of truth for WHY the site is changing direction. The live, editable
version is the Claude Doc "1960smusic.net Content Strategy Review & Plan":
https://claude.ai/code/artifact/c53b1985-4346-409f-9d83-6a85189ce6ad
Task-level instructions for Claude Code live in `docs/phase1-foundations.md`.
Keep this file at or under 195 lines.

## Verdict

Do not rebuild. Writing quality, the 8 genre hubs, On This Day and the tools
are strong. The problems are structural: crawlable linking, a missing
year-by-year spine, no named author, and analytics polluted by Charlie's own
visits. Positioning: **hear the 1960s, understand them, play with them —
year by year and genre by genre.**

## Baseline data (captured Sep 27, 2026)

### Search Console
- Indexed 77 of 99 known pages (last update 9/20/26).
- 43 Google web clicks since launch; peak 8 on Sep 6.
- Recommendation flagged `/blog/on-this-day/september-3/` impressions -99%
  (normal: date pages only get searched near their date).
- Why not indexed:
  | Reason | Pages | Action |
  |---|---|---|
  | Discovered - currently not indexed | 18 | Crawl-priority problem. Fix with static HTML links (Phase 1, tasks 1-2), then request indexing |
  | Alternate page with proper canonical tag | 3 | /about, /contact, /terms-of-use → canonical .html. Working as intended |
  | Redirect error | 1 | /blog/on-this-day/september-1 (no slash), last crawled Aug 21. Loads fine now → Validate fix in GSC |
  | Crawled - currently not indexed | 0 | No quality rejections |
- The 18 "Discovered" URLs: /blog/artists/, /blog/songs/,
  /blog/artists/the-doors/, /blog/artists/the-yardbirds/,
  /blog/genres/jazz-easy-listening/, /blog/genres/pop-brill-building/,
  /blog/on-this-day/september-1/, -14/, -15/, -17/,
  /blog/songs/heart-full-of-soul-yardbirds/, i-want-to-hold-your-hand-beatles/,
  needles-and-pins-searchers/, please-please-me-beatles/,
  sunny-afternoon-kinks/, the-end-doors/, you-really-got-me-kinks/,
  /privacy-policy.html

### GA4 (Aug 30 - Sep 26, 2026)
- 97 active users, 4m 08s avg engagement, 1.8K events.
- Sources (users): direct 59, google/organic 32, chatgpt.com 3, bing 1,
  scriblihelp.com 1.
- Top pages: Blog index 111 views/12 users (mostly Charlie), Radio Dial 75/30,
  Home 61/30, Folk Rock hub 10/9, OTD Sep 19 8/4, Daily game 7/4.
- Cities: Calgary 14, Red Deer 14, Lacombe 10 (near Blackfalds = Charlie),
  Billings 6, Council Bluffs 6 (Google data center = bots).
- GA4 internal-traffic filter NOT yet active → numbers include Charlie.

### Cloudflare AI Crawl Control (7 days to Sep 27)
- Nothing blocked (all Block toggles off). 1.31k AI crawler requests, +98.9%.
- 899 allowed, 408 unsuccessful (was ~1 the week before). Cause unknown yet.
  | Crawler | Allowed | Unsuccessful |
  |---|---|---|
  | Googlebot | 291 | 17 |
  | Applebot | 118 | 8 |
  | ClaudeBot | 92 | 32 |
  | PetalBot | 83 | 0 |
  | OAI-SearchBot | 58 | 22 |
  | Amazonbot | 53 | 106 |
  | ChatGPT-User | 43 | 4 |
  | Perplexity-User | 16 | 67 |
  | CCBot | 8 | 47 |
  | Claude-SearchBot | 7 | 8 |
  | DuckAssistBot | 5 | 36 |
- Most-crawled path: /styles.css (79). Apple pulled 15.49 MB of images.

### Keyword data on file (WordStream, verified by Charlie)
- "music of the 60s" / "1960s music" / "music 60 s" cluster ~110,000
- "60s music hits" / "1960s music hits" ~33,100
- "60s songs" cluster ~22,200
- "60s rock" cluster ~9,900
- Year-page volumes (1960-1969) NOT yet verified — verify before locking.

## Confirmed technical findings (from the repo)

1. Listing pages (`blog/index.html`, `blog/*/index.html`) ship an empty
   `#archive-grid`; `blog/shared.js` fills it from `data/posts.json` at
   runtime. Non-JS crawlers see zero article links.
2. Homepage genre tiles are built in JS (`/blog/genres/' + g.slug`), so the
   only plain HTML links are Radio, Blog, About, Contact. 6 share links are `#`.
3. Homepage already has JSON-LD (Organization, WebPage, Article, FAQPage).
4. No byline, no visible dates, no author page; About names no person.
5. No `404.html` although wrangler.toml sets `not_found_handling = "404-page"`.
6. Queue row 62 "I Walk the Line" is a 1956 song (site is strictly 1960s).
7. robots.txt allows all; llms.txt exists; .assetsignore hides gen/, worker/.

## Competitive landscape (Google, Sep 2026)
- "music of the 60s": uDiscover 100 best 60s songs, Spotify/YouTube
  playlists, Paste 100 greatest, AccuRadio 60s, jeffs60s.com (memoir page).
- "1960s music" history: Wikipedia 1960s in music, Encyclopedia.com.
- "best 60s songs": uDiscover, NME, Top40Weekly (has 1960-1969 year pages).
- Gap to exploit: nobody combines playable music + dated history + tools.

## Target architecture

Two axes, genre and year. Every article links to its genre hub, its year
page and the homepage ("1960s music" anchor).

| New page | URL | Target | Notes |
|---|---|---|---|
| Year pages x10 | /1960s/1960/ … /1960s/1969/ | "1965 music", "top songs of 1965" | Answer-first intro, US #1s, key albums, events → OTD links, genre shifts, "Play 1965" radio filter |
| Best 60s songs | /best-60s-songs/ | "60s songs", "60s music hits" | 100 songs, year, genre, why-it-matters line, player, link to song story, filters |
| 60s rock umbrella | /blog/genres/60s-rock/ | "60s rock" | Links down to British Invasion, garage/surf, psychedelic hubs |
| Tool intros | each /tools/ page | "60s music trivia", "60s radio" | 200-400 words of crawlable text |
| Author page | /about/charlie/ | Charlie Gillingham | Facts supplied by Charlie only |

## GEO / AI-citation rules (apply to all new and refreshed pages)
1. Answer the title's question in the first 60 words (year + name + number).
2. Question-style H2s where natural; each section quotable on its own.
3. One fact table per article (release, label, writer, producer, US/UK peak).
4. Full entity names first, consistent spelling, linked to on-site pages.
5. Visible byline + Published/Updated dates matching schema.
6. Inline sources (Official Charts, Billboard, Rock Hall, label/artist sites).
7. FAQ written last, from real People-also-ask questions.
8. One original-data page per month built from our own dataset.

## Roadmap
| Phase | Dates | Work | Gate |
|---|---|---|---|
| 1 Foundations | Sep 28 - Oct 11 | Static listings, homepage links, byline/dates, schema, alt text, 404, GA4/Bing/Cloudflare | Every article link in view-source; bylines live |
| 2 Decade spine | Oct 12 - Nov 8 | 10 year pages, best 60s songs, 60s rock, homepage rebuild, tool intros | Year pages + list live and linked from every OTD |
| 3 Spread | Nov 9 - Dec 27 | Queue rotation 3-4/wk, 1 data page/month, Trending 1/wk, 1 refresh/wk | 90-day review |

On This Day runs throughout: 2/day through October to get 30+ days ahead of
each date, then 1/day to hold the lead.

## Metrics to review at each gate
Pages indexed (target 90%+), pages with impressions, queries count, Google
clicks trend, AI referrals in GA4 (chatgpt.com, perplexity.ai, gemini,
copilot), returning users, engagement time (after internal filter), AI
crawler unsuccessful count in Cloudflare.

## Open decisions (Charlie)
- [x] Phase 1-2 work goes ahead of the content-build.md queue (approved Sep 27)
- [ ] Cloudflare: screenshot 3xx / 4xx crawler views + Bot Fight Mode setting
- [ ] Author page facts
- [ ] Dolly Parton Trending post: retitle to her 1960s career + 301, or leave
- [ ] Row 62 "I Walk the Line" (1956): reframe or drop
- [ ] Verify year-page keyword volumes (attempted 2026-09-29 via
  DataForSEO MCP, both endpoints returned HTTP 402, no account credits;
  see `docs/phase2-decade-spine.md` open blocker)
