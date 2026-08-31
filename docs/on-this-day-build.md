# On This Day Build Queue

Single source of truth for what On This Day date page gets built next. Read
this file at the start of every On This Day session before touching
anything else. Companion files: `docs/on-this-day-sources.md` (research and
audit rules) and `docs/on-this-day-template-spec.md` (page structure).

## How this works

1. Find the first row below with status `not started`. That is the only
   date to work on. Never start a new row while an earlier row is
   `in progress`, `audited`, or `drafted`, finish and confirm one live
   before starting the next. One date goes live per day, not a batch.
2. **Workflow starting Sept 2 (changed from the Sept 1 build): Charlie
   supplies the verified dataset for the next date directly**, instead of
   researching it from scratch. Still run it through the Part 1/3/4 checks
   in `docs/on-this-day-sources.md` (date verification, source audit,
   final output) before building, since a "verified" claim still needs a
   real Tier 1/2 citation traced and confirmed before it ships, the way
   the Sept 1 dataset review caught real date errors (Ray Conniff, Sonny &
   Cher, Bowie, Jethro Tull) even in a pre-vetted list. Get Charlie's
   explicit approval on the RECOMMENDED FINAL DATASET before writing
   anything.
3. Build `data/on-this-day/{MM-DD}.json` from the approved dataset, per the
   schema in `docs/on-this-day-template-spec.md`.
4. Build the page at `blog/on-this-day/{date-slug}/index.html` from
   `docs/on-this-day-page-template.html`, matching the CSS/markup already
   live on `blog/on-this-day/september-1/index.html`.
   - Media: every card should carry either a real image or a real video,
     never left blank unless truly nothing verifiable exists for that
     specific event (see `docs/on-this-day-sources.md` IMAGES & VIDEO
     rules). **Even on a day where real images can be found for every
     card, deliberately use video in place of an image for exactly two
     of the cards**, so the page doesn't read as all-photo. Pick the two
     events that best support a real, verifiable video. Beyond those two,
     video still takes priority over image whenever a legitimate clip
     exists for that specific event.
   - Never invent or guess a `youtube_id` or image URL. Verify each one
     (oEmbed/direct fetch for video, license check for images) before it
     goes in the JSON. If the working environment can't reach youtube.com
     to verify, say so explicitly and flag those IDs for Charlie to
     spot-check on the live page rather than silently skipping video.
5. Build locally, run a local server, and get Charlie's explicit
   go-ahead before pushing to `main`.
6. Once pushed live, in the same session update all of: this file (status
   -> `live`), `data/posts.json` (new entry, type `on-this-day`,
   **including a `seq` field set to this file's queue row number** — see
   note below, this is required, not optional), `link-map.md` (status ->
   `live`, live URL, inbound/outbound links), and regenerate `sitemap.xml`
   (`python3 gen/generate_sitemap.py`, after `posts.json` is updated). Only
   then move to the next `not started` row.

**Why `seq` matters:** the `/blog/on-this-day/` archive and the blog index
sort this type newest-first, but several date pages often get built and
published on the same real calendar day (their `posts.json` `date` field
ties). A tie broken by array order silently drifted out of true
chronological order once before. `seq` (this file's queue row number, which
is calendar-locked) is what `blog/shared.js`'s `byOtdDesc` actually sorts
on for `on-this-day` posts, so the listing always runs newest-covered-date
first regardless of publish-date collisions. Never add an `on-this-day`
entry to `posts.json` without it.

**Never use the Agent/Task tool (subagents or delegation) for any of this.**
All research, verification, and building happens directly, single-session.

Status values: `not started` -> `in progress` (research/audit underway) ->
`audited` (RECOMMENDED FINAL DATASET approved by Charlie, JSON not yet
built) -> `drafted` (JSON and page built, not yet reviewed locally) ->
`live` (pushed to main and confirmed responding 200 at its live URL).

Order is locked: September, October, November, December, January,
February, March, April, May, June, July, August (calendar order starting
from the first date built, September 1).

## Queue

Live rows moved to [`docs/on-this-day-build-archive.md`](on-this-day-build-archive.md).
Rows past this file's range live in [`docs/on-this-day-build-queued.md`](on-this-day-build-queued.md)
— once every row below is `live`, pull the next chunk from that file in
calendar order and append it here.

| # | Date | Page | Data file | Status |
|---|------|------|-----------|--------|
| 4 | September 4 | /blog/on-this-day/september-4/ | data/on-this-day/09-04.json | live |
| 5 | September 5 | /blog/on-this-day/september-5/ | data/on-this-day/09-05.json | live |
| 6 | September 6 | /blog/on-this-day/september-6/ | data/on-this-day/09-06.json | live |
| 7 | September 7 | /blog/on-this-day/september-7/ | data/on-this-day/09-07.json | live |
| 8 | September 8 | /blog/on-this-day/september-8/ | data/on-this-day/09-08.json | live |
| 9 | September 9 | /blog/on-this-day/september-9/ | data/on-this-day/09-09.json | live |
| 10 | September 10 | /blog/on-this-day/september-10/ | data/on-this-day/09-10.json | live |
| 11 | September 11 | /blog/on-this-day/september-11/ | data/on-this-day/09-11.json | not started |
| 12 | September 12 | /blog/on-this-day/september-12/ | data/on-this-day/09-12.json | not started |
| 13 | September 13 | /blog/on-this-day/september-13/ | data/on-this-day/09-13.json | not started |
| 14 | September 14 | /blog/on-this-day/september-14/ | data/on-this-day/09-14.json | not started |
| 15 | September 15 | /blog/on-this-day/september-15/ | data/on-this-day/09-15.json | not started |
| 16 | September 16 | /blog/on-this-day/september-16/ | data/on-this-day/09-16.json | not started |
| 17 | September 17 | /blog/on-this-day/september-17/ | data/on-this-day/09-17.json | not started |
| 18 | September 18 | /blog/on-this-day/september-18/ | data/on-this-day/09-18.json | not started |
| 19 | September 19 | /blog/on-this-day/september-19/ | data/on-this-day/09-19.json | not started |
| 20 | September 20 | /blog/on-this-day/september-20/ | data/on-this-day/09-20.json | not started |
| 21 | September 21 | /blog/on-this-day/september-21/ | data/on-this-day/09-21.json | not started |
| 22 | September 22 | /blog/on-this-day/september-22/ | data/on-this-day/09-22.json | not started |
| 23 | September 23 | /blog/on-this-day/september-23/ | data/on-this-day/09-23.json | not started |
| 24 | September 24 | /blog/on-this-day/september-24/ | data/on-this-day/09-24.json | not started |
| 25 | September 25 | /blog/on-this-day/september-25/ | data/on-this-day/09-25.json | not started |
| 26 | September 26 | /blog/on-this-day/september-26/ | data/on-this-day/09-26.json | not started |
| 27 | September 27 | /blog/on-this-day/september-27/ | data/on-this-day/09-27.json | not started |
| 28 | September 28 | /blog/on-this-day/september-28/ | data/on-this-day/09-28.json | not started |
| 29 | September 29 | /blog/on-this-day/september-29/ | data/on-this-day/09-29.json | not started |
| 30 | September 30 | /blog/on-this-day/september-30/ | data/on-this-day/09-30.json | not started |
| 31 | October 1 | /blog/on-this-day/october-1/ | data/on-this-day/10-01.json | not started |
| 32 | October 2 | /blog/on-this-day/october-2/ | data/on-this-day/10-02.json | not started |
| 33 | October 3 | /blog/on-this-day/october-3/ | data/on-this-day/10-03.json | not started |
| 34 | October 4 | /blog/on-this-day/october-4/ | data/on-this-day/10-04.json | not started |
| 35 | October 5 | /blog/on-this-day/october-5/ | data/on-this-day/10-05.json | not started |
| 36 | October 6 | /blog/on-this-day/october-6/ | data/on-this-day/10-06.json | not started |
| 37 | October 7 | /blog/on-this-day/october-7/ | data/on-this-day/10-07.json | not started |
| 38 | October 8 | /blog/on-this-day/october-8/ | data/on-this-day/10-08.json | not started |
| 39 | October 9 | /blog/on-this-day/october-9/ | data/on-this-day/10-09.json | not started |
| 40 | October 10 | /blog/on-this-day/october-10/ | data/on-this-day/10-10.json | not started |
| 41 | October 11 | /blog/on-this-day/october-11/ | data/on-this-day/10-11.json | not started |
| 42 | October 12 | /blog/on-this-day/october-12/ | data/on-this-day/10-12.json | not started |
| 43 | October 13 | /blog/on-this-day/october-13/ | data/on-this-day/10-13.json | not started |
| 44 | October 14 | /blog/on-this-day/october-14/ | data/on-this-day/10-14.json | not started |
| 45 | October 15 | /blog/on-this-day/october-15/ | data/on-this-day/10-15.json | not started |
| 46 | October 16 | /blog/on-this-day/october-16/ | data/on-this-day/10-16.json | not started |
| 47 | October 17 | /blog/on-this-day/october-17/ | data/on-this-day/10-17.json | not started |
| 48 | October 18 | /blog/on-this-day/october-18/ | data/on-this-day/10-18.json | not started |
| 49 | October 19 | /blog/on-this-day/october-19/ | data/on-this-day/10-19.json | not started |
| 50 | October 20 | /blog/on-this-day/october-20/ | data/on-this-day/10-20.json | not started |
| 51 | October 21 | /blog/on-this-day/october-21/ | data/on-this-day/10-21.json | not started |
| 52 | October 22 | /blog/on-this-day/october-22/ | data/on-this-day/10-22.json | not started |
| 53 | October 23 | /blog/on-this-day/october-23/ | data/on-this-day/10-23.json | not started |
| 54 | October 24 | /blog/on-this-day/october-24/ | data/on-this-day/10-24.json | not started |
| 55 | October 25 | /blog/on-this-day/october-25/ | data/on-this-day/10-25.json | not started |
| 56 | October 26 | /blog/on-this-day/october-26/ | data/on-this-day/10-26.json | not started |
| 57 | October 27 | /blog/on-this-day/october-27/ | data/on-this-day/10-27.json | not started |
| 58 | October 28 | /blog/on-this-day/october-28/ | data/on-this-day/10-28.json | not started |
| 59 | October 29 | /blog/on-this-day/october-29/ | data/on-this-day/10-29.json | not started |
| 60 | October 30 | /blog/on-this-day/october-30/ | data/on-this-day/10-30.json | not started |
| 61 | October 31 | /blog/on-this-day/october-31/ | data/on-this-day/10-31.json | not started |
| 62 | November 1 | /blog/on-this-day/november-1/ | data/on-this-day/11-01.json | not started |
| 63 | November 2 | /blog/on-this-day/november-2/ | data/on-this-day/11-02.json | not started |
| 64 | November 3 | /blog/on-this-day/november-3/ | data/on-this-day/11-03.json | not started |
| 65 | November 4 | /blog/on-this-day/november-4/ | data/on-this-day/11-04.json | not started |
| 66 | November 5 | /blog/on-this-day/november-5/ | data/on-this-day/11-05.json | not started |
| 67 | November 6 | /blog/on-this-day/november-6/ | data/on-this-day/11-06.json | not started |
| 68 | November 7 | /blog/on-this-day/november-7/ | data/on-this-day/11-07.json | not started |
| 69 | November 8 | /blog/on-this-day/november-8/ | data/on-this-day/11-08.json | not started |
| 70 | November 9 | /blog/on-this-day/november-9/ | data/on-this-day/11-09.json | not started |
| 71 | November 10 | /blog/on-this-day/november-10/ | data/on-this-day/11-10.json | not started |
| 72 | November 11 | /blog/on-this-day/november-11/ | data/on-this-day/11-11.json | not started |
| 73 | November 12 | /blog/on-this-day/november-12/ | data/on-this-day/11-12.json | not started |
| 74 | November 13 | /blog/on-this-day/november-13/ | data/on-this-day/11-13.json | not started |
| 75 | November 14 | /blog/on-this-day/november-14/ | data/on-this-day/11-14.json | not started |
| 76 | November 15 | /blog/on-this-day/november-15/ | data/on-this-day/11-15.json | not started |
| 77 | November 16 | /blog/on-this-day/november-16/ | data/on-this-day/11-16.json | not started |
| 78 | November 17 | /blog/on-this-day/november-17/ | data/on-this-day/11-17.json | not started |
| 79 | November 18 | /blog/on-this-day/november-18/ | data/on-this-day/11-18.json | not started |
| 80 | November 19 | /blog/on-this-day/november-19/ | data/on-this-day/11-19.json | not started |
| 81 | November 20 | /blog/on-this-day/november-20/ | data/on-this-day/11-20.json | not started |
| 82 | November 21 | /blog/on-this-day/november-21/ | data/on-this-day/11-21.json | not started |
| 83 | November 22 | /blog/on-this-day/november-22/ | data/on-this-day/11-22.json | not started |
| 84 | November 23 | /blog/on-this-day/november-23/ | data/on-this-day/11-23.json | not started |
| 85 | November 24 | /blog/on-this-day/november-24/ | data/on-this-day/11-24.json | not started |
| 86 | November 25 | /blog/on-this-day/november-25/ | data/on-this-day/11-25.json | not started |
| 87 | November 26 | /blog/on-this-day/november-26/ | data/on-this-day/11-26.json | not started |
| 88 | November 27 | /blog/on-this-day/november-27/ | data/on-this-day/11-27.json | not started |
| 89 | November 28 | /blog/on-this-day/november-28/ | data/on-this-day/11-28.json | not started |
| 90 | November 29 | /blog/on-this-day/november-29/ | data/on-this-day/11-29.json | not started |
| 91 | November 30 | /blog/on-this-day/november-30/ | data/on-this-day/11-30.json | not started |
| 92 | December 1 | /blog/on-this-day/december-1/ | data/on-this-day/12-01.json | not started |
| 93 | December 2 | /blog/on-this-day/december-2/ | data/on-this-day/12-02.json | not started |
