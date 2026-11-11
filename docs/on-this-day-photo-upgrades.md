# On This Day Photo Upgrades

Companion to `docs/on-this-day-build.md` (standing rule there). Pages whose
share image is still the generated date card (`og-card.png`, made by
`gen/build_share_cards.py`), oldest date first. Each On This Day session
upgrades the top `pending` row to a real photo, then deletes the row in the
same push it goes live. A date with no confirmable photo is marked
`card stays: <one-line reason>` and is skipped on later sessions.

Photo order: (a) a self-hosted image already on the page (or already
self-hosted elsewhere on the site with a confirmed free licence), then
(b) a freely licensed photo, Wikimedia Commons first, downloaded into the
page's `img/` folder. Never hotlink. Show it on the page (with credit and
licence in the caption), point `og:image` and the Article JSON-LD image at
it, set the JSON `image` field, delete `og-card.png`. Plumbing only: no
Updated/dateModified bump. `check_article.py` enforces the image rule.

Upgraded so far: September 5 (2026-11-10, The Animals 1964, public domain);
September 6 (2026-11-10, Jimi Hendrix Experience 1968 Reprise photo, public domain,
reused from the Hendrix bio);
September 7 (2026-11-11, Aretha Franklin 1967 Atlantic trade-ad photo, CC0, reused from
`/1960s/1967/`);
September 10 (2026-11-11, The Beatles 1963 Dezo Hoffmann/Capitol publicity photo, public
domain in the US, reused from October 3).

| # | Page | Status |
|---|------|--------|
| 13 | /blog/on-this-day/september-13/ | pending |
| 14 | /blog/on-this-day/september-14/ | pending |
| 15 | /blog/on-this-day/september-15/ | pending |
| 16 | /blog/on-this-day/september-16/ | pending |
| 20 | /blog/on-this-day/september-20/ | pending |
| 21 | /blog/on-this-day/september-21/ | pending |
| 22 | /blog/on-this-day/september-22/ | pending |
| 23 | /blog/on-this-day/september-23/ | pending |
| 24 | /blog/on-this-day/september-24/ | pending |
| 25 | /blog/on-this-day/september-25/ | pending |
| 26 | /blog/on-this-day/september-26/ | pending |
| 27 | /blog/on-this-day/september-27/ | pending |
| 34 | /blog/on-this-day/october-4/ | pending |
| 35 | /blog/on-this-day/october-5/ | pending |
| 36 | /blog/on-this-day/october-6/ | pending |
| 37 | /blog/on-this-day/october-7/ | pending |
| 38 | /blog/on-this-day/october-8/ | pending |
| 39 | /blog/on-this-day/october-9/ | pending |
| 40 | /blog/on-this-day/october-10/ | pending |
| 41 | /blog/on-this-day/october-11/ | pending |
| 42 | /blog/on-this-day/october-12/ | pending |
| 43 | /blog/on-this-day/october-13/ | pending |
| 44 | /blog/on-this-day/october-14/ | pending |
| 45 | /blog/on-this-day/october-15/ | pending |
| 46 | /blog/on-this-day/october-16/ | pending |
| 47 | /blog/on-this-day/october-17/ | pending |
| 48 | /blog/on-this-day/october-18/ | pending |
| 49 | /blog/on-this-day/october-19/ | pending |
| 50 | /blog/on-this-day/october-20/ | pending |
| 51 | /blog/on-this-day/october-21/ | pending |
| 52 | /blog/on-this-day/october-22/ | pending |
| 53 | /blog/on-this-day/october-23/ | pending |
| 54 | /blog/on-this-day/october-24/ | pending |
| 55 | /blog/on-this-day/october-25/ | pending |
| 56 | /blog/on-this-day/october-26/ | pending |
| 57 | /blog/on-this-day/october-27/ | pending |
| 58 | /blog/on-this-day/october-28/ | pending |
| 59 | /blog/on-this-day/october-29/ | pending |
| 60 | /blog/on-this-day/october-30/ | pending |
| 61 | /blog/on-this-day/october-31/ | pending |
| 62 | /blog/on-this-day/november-1/ | pending |
| 63 | /blog/on-this-day/november-2/ | pending |
| 64 | /blog/on-this-day/november-3/ | pending |
| 65 | /blog/on-this-day/november-4/ | pending |
| 66 | /blog/on-this-day/november-5/ | pending |
| 67 | /blog/on-this-day/november-6/ | pending |
| 68 | /blog/on-this-day/november-7/ | pending |
| 69 | /blog/on-this-day/november-8/ | pending |
| 70 | /blog/on-this-day/november-9/ | pending |
| 71 | /blog/on-this-day/november-10/ | pending |
| 72 | /blog/on-this-day/november-11/ | pending |
| 73 | /blog/on-this-day/november-12/ | pending |
| 74 | /blog/on-this-day/november-13/ | pending |
| 75 | /blog/on-this-day/november-14/ | pending |
| 76 | /blog/on-this-day/november-15/ | pending |
| 77 | /blog/on-this-day/november-16/ | pending |
| 78 | /blog/on-this-day/november-17/ | pending |
| 79 | /blog/on-this-day/november-18/ | pending |
| 80 | /blog/on-this-day/november-19/ | pending |
| 81 | /blog/on-this-day/november-20/ | pending |
| 82 | /blog/on-this-day/november-21/ | pending |
| 83 | /blog/on-this-day/november-22/ | pending |
| 84 | /blog/on-this-day/november-23/ | pending |
| 85 | /blog/on-this-day/november-24/ | pending |
| 86 | /blog/on-this-day/november-25/ | pending |
| 87 | /blog/on-this-day/november-26/ | pending |
| 88 | /blog/on-this-day/november-27/ | pending |
| 89 | /blog/on-this-day/november-28/ | pending |
| 90 | /blog/on-this-day/november-29/ | pending |
| 91 | /blog/on-this-day/november-30/ | pending |
| 92 | /blog/on-this-day/december-1/ | pending |
| 93 | /blog/on-this-day/december-2/ | pending |
| 94 | /blog/on-this-day/december-3/ | pending |
| 95 | /blog/on-this-day/december-4/ | pending |
| 96 | /blog/on-this-day/december-5/ | pending |
| 97 | /blog/on-this-day/december-6/ | pending |
| 98 | /blog/on-this-day/december-7/ | pending |
| 99 | /blog/on-this-day/december-8/ | pending |
| 100 | /blog/on-this-day/december-9/ | pending |
| 101 | /blog/on-this-day/december-10/ | pending |
| 102 | /blog/on-this-day/december-11/ | pending |
| 103 | /blog/on-this-day/december-12/ | pending |
| 104 | /blog/on-this-day/december-13/ | pending |
| 105 | /blog/on-this-day/december-14/ | pending |
