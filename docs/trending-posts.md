# Trending Posts (moved from CLAUDE.md 2026-10-08 to keep CLAUDE.md under the 199-line ceiling)

Rules unchanged. Structure details also live in `docs/writing-standard.md`.

`/blog/trending/` covers 1960s songs/artists resurging in modern
culture (TikTok, streaming, sync placements). Same content pipeline
as every other type above, plus:

- Word count target: 400-700 words. Trending-specific structure and
  the mandatory "why it's trending now" module are in
  `docs/writing-standard.md`.
- Live TikTok embed (blockquote + `tiktok.com/embed.js`) required,
  placed where it's contextually relevant. Confirm it actually
  renders before marking the page done, don't assume the markup is
  enough. This repo's dev sandbox cannot always reach TikTok's video
  CDN, so a local check can show a correctly-built but blank embed;
  spot-check the live URL after deploy the same way On This Day
  YouTube ids get spot-checked.
- Feature image is a real photo, never AI-generated, even when the
  viral source clip itself uses an AI-generated image. Prefer a
  freely-licensed photo of the artist (Wikimedia Commons first). If
  none exists, fall back to editorial-context single/album cover art,
  then non-person period-appropriate stock imagery, in that order.
  Note which tier was used when reporting the page as done.
- No rotation queue yet, unlike `docs/content-build.md`. Charlie
  requests each Trending post individually until one exists.
