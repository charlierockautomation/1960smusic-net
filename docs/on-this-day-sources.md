# On This Day — Sources & Verification Protocol
For: 1960smusic.net /blog/on-this-day/
Load this file before researching or writing any On This Day post. It defines which sources to trust, in what order, and the audit process every day's dataset must pass before publishing.

---

## SOURCE TIERS

### Charlie's Seed Sources (starting set — use these first, expand as needed)
| Source | URL |
|---|---|
| Wikipedia — "1960 in music" and equivalent year pages (1961–1969) | https://en.wikipedia.org/wiki/1960_in_music |
| MusicBrainz Picard — basic variables docs (metadata/dating reference) | https://picard-docs.musicbrainz.org/en/v2.13/variables/variables_basic.html |
| Billboard Canada — Hot 100 chart | https://ca.billboard.com/charts/hot-100 |
| Grammy Awards — shows & ceremonies 1959–present | https://www.grammy.com/awards/ |
| Rock & Roll Hall of Fame — inductees by class | https://rockhall.com/inductees/classes/ |
| Official Charts — "Sixties definitive chart books" | https://www.officialcharts.com/chart-news/official-charts-announces-the-sixties-definitive-chart-books__27020/ |
| OnThisDay.com — music events calendar (day-by-day database) | https://www.onthisday.com/music/events/ |

Claude Code is approved to add further Tier 1 sources beyond this seed list as needed — quality bar below.

### Tier 1 — Primary / Authoritative (use these to CONFIRM a date)
| Category | Source | URL |
|---|---|---|
| US chart data, Hot 100 history | Billboard | https://www.billboard.com/charts/ |
| UK chart data | Official Charts Company | https://www.officialcharts.com/ |
| Canadian chart data | RPM Magazine archive (via Library and Archives Canada) | https://data2.archives.ca/e/e448/e011188230.pdf (RPM back issues, also indexed at worldradiohistory.com) |
| BBC TV/radio broadcast dates | BBC Genome Project (BBC Programme Index) | https://genome.ch.bbc.co.uk/ |
| Gold/Platinum certification dates | RIAA Gold & Platinum Database | https://www.riaa.com/gold-platinum/ |
| Grammy wins/nominations | Recording Academy / Grammy.com | https://www.grammy.com/awards |
| Rock Hall inductions, bios | Rock & Roll Hall of Fame | https://www.rockhall.com/inductees |
| Trade magazine archives (Billboard, Cash Box, Record World, RPM back issues, full scans) | World Radio History | https://worldradiohistory.com/ |
| Single/album release dates, catalog numbers | 45cat / 45worlds | https://www.45cat.com/ and https://www.45worlds.com/ |
| Discography cross-check | Discogs | https://www.discogs.com/ |
| Concert/tour dates | Setlist.fm | https://www.setlist.fm/ |
| US Copyright records (song registration dates) | US Copyright Office public catalog | https://cocatalog.loc.gov/ |
| National Recording Registry context | Library of Congress | https://www.loc.gov/programs/national-recording-preservation-board/recording-registry/ |
| Day-by-day cross-reference | OnThisDay.com | https://www.onthisday.com/music/events/ |

### Tier 2 — Strong Secondary (use to CORROBORATE, not as sole source for a big claim)
- Official artist/estate archives and fan-maintained day-by-day logs with cited primary sources (e.g. The Beatles Bible, JoniMitchell.com archive, artist-specific sessionographies like Rick Coleman's Fats Domino work)
- AllMusic (https://www.allmusic.com/) — bios, discography dates
- Songfacts (https://www.songfacts.com/) — corroboration only, not sole source
- Contemporary newspaper archives (Google News Archive, Newspapers.com) where accessible

### Tier 3 — Backup Only, Never Sole Source for a Significant Claim
- Wikipedia — fine for a quick lead or to locate the real source, never cited alone as the sole proof of an exact date on a page meant to be a permanent, cited article
- General fan wikis, Last.fm artist wiki, Playback.fm-style birthday aggregators

**Rule: any event in the final published dataset needs at least one Tier 1 or well-sourced Tier 2 citation. Wikipedia-only events go to NEEDS VERIFICATION, not the confirmed list.**

---

## THE AUDIT PROCESS (run for every single day, before publish)

### Part 1 — Date Verification
For every candidate event, check whether the source confirms the event happened ON that specific date, and flag if:
- Only the month or year is confirmed (not the day)
- A chart *issue* date is being used as if it were the actual event date
- A recording date is being confused with a release date
- A broadcast/air date is being confused with a taping date
- Sources conflict on the date

Anything failing this check moves to **NEEDS VERIFICATION** — never gets silently upgraded to confirmed.

### Part 2 — Missing Event Search
Actively search (don't just accept what a first pass turned up) across: major rock, British Invasion, Motown, soul/R&B, folk, country, jazz, blues, surf, psychedelic, and major labels — for recording sessions, releases, concerts, TV/radio appearances, chart milestones, births, deaths, band formations/breakups/lineup changes, and industry news on that date.

### Part 3 — Source Audit
For every event kept, check whether a Tier 1 source exists even if the first pass only turned up Tier 3. Upgrade the citation whenever possible.

### Part 4 — Final Output (four sections, every day)
1. **CONFIRMED** — exact date adequately supported by Tier 1/strong Tier 2
2. **ADDITIONAL EVENTS FOUND** — new finds from the Part 2 search
3. **NEEDS VERIFICATION** — kept in a holding file, not published, until a stronger source resolves them
4. **RECOMMENDED FINAL DATASET** — the actual list that goes into that day's JSON/article

---

## COVERAGE RULE
Every verified event for that calendar date across all 10 years (1960-1969) goes on the page. No curating down to "highlights only" — if it passed the verification audit as CONFIRMED, it's published. Group cards by year, most recent year first, so the page opens on the freshest/most-recognizable material.

## CARD STRUCTURE — identical shape for every single event, no exceptions
1. Category badge (birth / death / release / chart / concert / festival / broadcast / industry / culture) — color-coded, consistent color per category site-wide
2. Bold headline, sentence case, always phrased as [Subject] + [punchy verb] + [what happened] — e.g. "Tommy Roe hits No. 1 with Sheila", "Aunt Molly Jackson dies at 80" — never a flat label like "Chart Milestone: Sheila"
3. Exactly 2 sentences of summary: sentence 1 = what happened (concrete, specific), sentence 2 = why it matters (the hook/stakes). Same two-sentence rhythm on every card, every day, no exceptions.
4. Optional media slot (see below) — video takes priority over image when both could apply to the same event
5. Inline external link only where it fits naturally in the sentence (no separate sources line — see Publishing Rule above)

## IMAGES & VIDEO
- **Video first choice:** embed a YouTube video for any event tied to a specific recording, performance, or TV appearance where one exists (the song itself, a TV clip, a Shindig!/Ready Steady Go! segment, an official archival clip). This is the strongest media type for this content — free, legal, and it's what makes the page watchable.
- **Album/single cover art:** usable in an editorial/commentary context (same convention already used on ClassicRockArtists.com) for release-type events.
- **Artist photos:** only pull from Wikimedia Commons or another confirmed public-domain/CC-licensed source — do not pull arbitrary artist photos from a general image search, most 1960s press photography is still under copyright.
- **No media exists for this event type:** that's fine — chart milestones, copyright registrations, lineup/industry news events often won't have a natural image or video. Don't force one. Let the typography and category badge carry the card.

## PAGE STRUCTURE — final
- **Year nav:** the 1960-1969 pill row at the top of the page is real in-page anchor links (`<a href="#y1960">`), each jumping straight to that year's group of cards further down. Every year gets a `<section id="yNNNN">` wrapper even if it only has one event.
- **Media density:** scale image/video count to what Google considers appropriate for the page's actual length — a 27-event day (like Sept 1) supports significantly more embedded media than a 3-event day. Don't pad a short day with filler images just to hit a quota, and don't starve a long day of visuals either. Standard image SEO practice per image used: descriptive alt text, compressed/appropriately-sized files, no unlicensed stock filler.
- **Color:** vivid, high-contrast category colors and accents — this page should visually pop, not read as a muted/corporate layout. Category badges, the flagship callout, and section dividers are where the color does the most work.
- **Internal linking:** link every event mention that has a matching live page elsewhere on the site — artist bios, song stories, genre hubs. Link the artist/song name itself inline in the summary sentence, not a separate "related" list. If no matching page exists yet, no link — don't force one.

## PUBLISHING RULE
No dedicated "Sources" or "Citations" section anywhere on the page. Instead, work real external links naturally into the body copy of each event card wherever it reads naturally (e.g. "...reached No. 1 on the [Official Charts](https://...)"). This still gives the E-E-A-T and AI-citability benefit without a footnote-style sources block. Not every event needs an outbound link — only where it fits the sentence naturally; don't force one into every card.

## FILE LOCATION
Keep this file at the repo root or in /docs/ (e.g. `docs/on-this-day-sources.md`) and reference it from CLAUDE.md's On This Day section so every session loads it automatically before starting a new day's research.
