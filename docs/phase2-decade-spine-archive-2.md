# Phase 2 — Decade Spine: Archive 2

Overflow from `docs/phase2-decade-spine-archive.md` (195-line ceiling,
CLAUDE.md File Size Ceiling rule). Holds year-page build notes from 1964
onward as they rotate out of the active file.

## Task 6 detail: 1964 build notes

`/1960s/1964/` live 2026-10-06, 1686 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1964 (tracklist; one primary
source, ranks 22-25 confirmed by a second search result, Billboard's own
list returned HTTP 402) plus the full chronological 23-single
number-ones list, cross-verified against de.wikipedia. All 25 YouTube
ids resolved (2 cached, 23 via `generate.py`'s no-API scraper) and
verified embeddable, not made-for-kids, in one batched
`yt_video_status.py` call. Two ids are cached `flagged` (Dancing in the
Street, Glad All Over, non-official channels), same acceptable-if-
compliant call as earlier years. Links all 6 live hubs that overlap
1964 (british-invasion, motown-soul, garage-surf-rock, pop-brill-
building, jazz-easy-listening, folk-rock); country-60s not linked, no
verified 1964 country tie in the sourced material. Featured image is a
public-domain Library of Congress photo (Marion S. Trikosko) of the
Beatles at the Washington Coliseum, Feb 11 1964, via Wikimedia Commons.
Notable Events links OTD Sep 5, Sep 26, Sep 27. Playwright self-test
(`gen/test_playlist_player_1964.py`) PASS.

## Task 7 detail: 1965 build notes

`/1960s/1965/` live 2026-10-08, 1689 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1965 (tracklist; cross-verified
against billboardtop100of.com) plus the chronological number-ones
list (27 titles, dates/weeks cross-checked against de.wikipedia; no
total stated since en/de disagree 26 vs 27). Wooly Bully is year-end
No. 1 but peaked No. 2, used as the lead hook. All 25 YouTube ids
resolved (3 cached, 22 via scraper, This Diamond Ring on a retry) and
verified embeddable, not made-for-kids, in one batched call. Links all
7 eligible hubs. Featured image is a real CC BY 4.0 photo of the Rolling
Stones in Finland, June 25 1965 (Finnish Heritage Agency, via Wikimedia
Commons). Notable Events links OTD Sep 4, Sep 12, Oct 9. Playwright
self-test (`gen/test_playlist_player_1965.py`) PASS.

## Years 1966-1969 build notes

`/1960s/1966/` live 2026-10-08, 1694 words, check_article.py PASS.
Billboard year-end top 25 of 1966 uses Billboard's REVISED ranking
(Green Berets No. 1; billboardtop100of.com full list, Billboard's
revision confirmed by AOL and Wikipedia's Green Berets article). The
original Dec 24 1966 printed list (Wikipedia) ranks California
Dreamin' first and Green Berets tenth; the page says so in an h3.
Billboard's own page returned HTTP 402. Chronological number-ones list
(27 titles, weeks cross-checked against rogerogreen.com). All 25
YouTube ids resolved (6 cached, 19 via scraper) and verified
embeddable, not made-for-kids, in one batched call; several carry the
usual acceptable-if-compliant `yt` flag. Links 7 hubs (no country-60s,
no verified 1966 tie). Featured image: CBS publicity photo of the
Supremes on Ed Sullivan, 1966, public domain via Wikimedia Commons.
Notable Events links OTD Sep 3, 12, 21, 24, Oct 15 (Sep 10 in albums
bullet text only, no link). Playwright self-test PASS.

`/1960s/1967/` live 2026-10-08, 1554 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1967 (Wikipedia, cross-checked
against billboardtop100of.com; To Sir With Love No. 1) plus the
chronological number-ones list (19 songs; weeks derived from the
Wikipedia issue-date ranges, no independent second source found).
Peaks for non-number-ones from Wikipedia's top-ten list, Come Back
When You Grow Up confirmed No. 3 by search. All 25 YouTube ids
verified embeddable, not made-for-kids, in one batched call; two
scraper picks were live versions (Ode to Billie Joe, I Think We're
Alone Now) and were swapped for studio Topic uploads. Flagged `yt`:
I'm a Believer, Happy Together, Groovin', Incense and Peppermints.
Links 6 hubs (no country-60s, no folk-rock: no verified tie). Featured
image: public-domain Aretha Franklin photo from a July 15 1967
Atlantic trade ad in Billboard, via Wikimedia Commons. Velvet
Underground and Forever Changes dates left at month level (sources
disagree / single source). Notable Events links OTD Sep 17, 18, 23,
Oct 14. Playwright self-test (`gen/test_playlist_player_1967.py`) PASS.

`/1960s/1968/` live 2026-10-08, 1637 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1968 (Wikipedia; Hey Jude No. 1)
plus the chronological number-ones list (16 songs; weeks derived from
Wikipedia issue dates, sum to 52 and match its stated per-act totals, no
independent second source). Peaks for non-number-ones from Wikipedia's
top-ten list. All 25 YouTube ids verified embeddable, not made-for-kids,
in one batched call (8 cached, 17 via scraper, mostly official/Topic
uploads). Links 7 hubs (no garage-surf-rock: no 1968 top-25 tie). Prose
avoids "Jeannie C. Riley" because check_article.py's sentence splitter
treats the initial as a sentence end. Featured image: public-domain
Warner/Reprise Jimi Hendrix Experience promo, via Wikimedia Commons.
Notable Events links OTD Sep 7, 21, 28, Oct 12, 16. Playwright self-test
(`gen/test_playlist_player_1968.py`) PASS.

`/1960s/1969/` live 2026-10-08, 1697 words, check_article.py PASS.
Billboard Year-End Hot 100 top 25 of 1969 (Wikipedia) plus the
chronological number-ones list (17 songs; weeks sum to 52, 5th
Dimension 9 and Beatles/Zager and Evans 6 each match Wikipedia's stated
totals; no independent second source). Peaks for non-number-ones from
Wikipedia's top-ten list. All 25 YouTube ids verified embeddable, not
made-for-kids, in one batched call; seven scraper picks (fan uploads,
live/TV takes) were swapped for studio Topic/VEVO uploads. Links 7 hubs (no psychedelic-rock:
no 1969 top-25 tie); CCR tagged garage-surf-rock, Tom Jones tagged
jazz-easy-listening, both judgment calls. Featured image: CC BY-SA 4.0
Woodstock crowd photo by James M Shelley, via Wikimedia Commons (a
public-domain Sly Stone Woodstock photo was passed over: eBay/AP
provenance unclear). Notable Events links OTD Sep 13, 14, Oct 1, 4, 7, 12. Playwright
self-test (`gen/test_playlist_player_1969.py`) PASS.
