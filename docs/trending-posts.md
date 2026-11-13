# Trending Posts (moved from CLAUDE.md 2026-10-08; trending section of
# writing-standard.md merged in 2026-11-13)

`/blog/trending/` covers 1960s songs/artists resurging in modern culture
(TikTok, streaming, sync placements). Same pipeline and base writing standard
as every other type, plus the rules below.

## Shape
- 400-700 words (`check_article.py` enforces for the `trending` type).
- Fixed order as the base Structure, with the YouTube-embed slot replaced:
  H1, intro/lead, featured image, TOC, then body sections. One of them is
  the mandatory "why it's trending now" module, placed where contextually
  relevant (not forced right after the TOC). It explains the actual
  resurgence (TikTok clip, sync placement, streaming spike) and embeds it
  live where possible.
- If the source clip is tagged as AI-generated media (a stylized image, not
  archival footage), say so in the module, factually, in one or two
  sentences, not as a disclaimer that undercuts the post.

## TikTok embed
- Live TikTok embed required, placed where contextually relevant: TikTok's
  oEmbed markup, `blockquote class="tiktok-embed"` with `data-video-id`,
  plus `<script async src="https://www.tiktok.com/embed.js">`.
- Confirm it renders (screenshot a local preview) before calling the page
  done; markup alone is not enough. The dev sandbox cannot always reach
  TikTok's video CDN, so a local check can show a correctly built but blank
  embed; spot-check the live URL after deploy, as On This Day YouTube ids are.
- Exception: if the peg genuinely has no TikTok source (verified by search
  every time, never assumed), use YouTube embed(s) for the module and mark
  the page `<!-- TIKTOK-EXEMPT: <one-line reason> -->` near the top so
  `check_article.py` skips the TikTok check. A real exception, not a shortcut.

## Feature image
Real photo, never AI-generated, even when the viral clip uses an AI image.
Order: freely licensed photo of the artist (Wikimedia Commons first) >
editorial-context single/album cover art (as `docs/on-this-day-sources.md`
uses for release events) > non-person period-appropriate stock imagery.
Note which tier was used when reporting the page as done.

## Schema and links
- Article + FAQPage + BreadcrumbList always; add MusicRecording
  (song-focused) or MusicGroup (artist-focused). Add VideoObject for an
  embedded clip only when name, description, thumbnail and embed URL are
  confirmed; never a guessed `uploadDate`; omit unverifiable fields.
- Base 3-5 body links rule, but never force a link to an unrelated hub or
  bio. If nothing in `link-map.md` legitimately connects, link general site
  pages (homepage, `/blog/trending/`, a relevant tool) instead.
- At least one `/1960s/<year>/` link, woven into a sentence naming that year.

## Weekly cadence (set 2026-10-22, supersedes per-post requests)
Cloud routine `trig_01GCntYZh1oWceGXGBxqYKHA` ("1960smusic.net weekly
Trending draft"), Mondays 14:00 UTC: researches a resurging 1960s peg, builds
the page, passes `check_article.py` + `publish_prep.py`, pushes only a
`trending/YYYY-MM-DD` branch. Charlie approves before anything merges to
`main`; post-push steps (verify_live, IndexNow, link-map) follow the normal
pipeline. Manage at https://claude.ai/code/routines. No rotation queue file.
