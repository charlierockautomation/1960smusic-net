# Writing Standard

Single source of truth for how every article is written.
`docs/article-template.html` implements the structure; `gen/check_article.py`
enforces what can be checked mechanically. Supersedes earlier chat guidance.
Trending-only rules: `docs/trending-posts.md`. GEO/AI-citation rules
(answer the title's question in the first 60 words, question-style H2s where
natural, full entity names first, inline sources, FAQ from real
People-also-ask): full list in `docs/strategy-review-2026-09.md`.

## Keyword density

- Formula: `(exact-phrase matches in body / total body word count) x 100`.
- Target range: strictly over 1% and under 2%. Below 1% is not enough
  signal, above 2% is a stuffing flag. Both directions are enforced.
- The focus keyword must appear in: the `<title>` tag, the meta
  description, the first 100 words of body copy, at least one H2 or H3,
  and the URL slug. Exception: if the keyword is long enough (6+ words,
  typically a full song title) that adding one more occurrence for the
  H2/H3 placement would push density over 2% at the article's word
  count, that placement is skipped rather than forced. First-sentence
  and last-sentence placement stay mandatory regardless.
- Never in two consecutive sentences. Never forced or unnatural, if a
  sentence reads awkwardly with the exact phrase, use a pronoun or a
  synonym instead and let the sentence read cleanly.
- 2-3 secondary keywords (natural synonyms, related terms) carry the
  rest of the semantic weight through the body instead of repeating the
  focus keyword.
- Body word count only. Title, meta description, and JSON-LD schema
  text are expected to carry the exact phrase and don't count toward
  the body density calculation.

## Prose and readability

- One sentence per line, each wrapped in its own `<p>` tag. Never bundle
  multiple sentences into one block. Use `<br>` inside a single `<p>`
  only when grouping sentences that belong to the same thought (matches
  existing site convention already in use).
- 75%+ of sentences under 20 words.
- No em dashes anywhere in prose, commas, colons, or periods instead.
  One narrow exception: a numeric separator like "Song, #36" inside a
  bulleted list item, never in flowing prose. In practice, just avoid
  needing the exception at all.
- Banned words/phrases (AI-cliche tells): delve, tapestry, testament,
  vibrant, unveil, groundbreaking, seminal, journey, realm, haunting,
  sonic landscape. "Stands the test of time" may appear once per
  article if genuinely unavoidable, never twice.
- Any list of 3+ items is a real `<ul>`/`<ol>`, never crammed into a
  sentence with parenthetical asides.
- Long H2 sections get real H3 subheadings breaking them up, one per
  distinct idea, named for what that chunk is actually about.
- Write like you're the top expert in this field: sensory, specific,
  human. Not a generic AI rewrite of Wikipedia. Each article should be
  better, more informative, and better written than anything else
  online about the same subject, not just adequate.
- Preserve existing `<strong>` emphasis on facts/names that warrant it,
  don't strip bold when editing a sentence, don't add it gratuitously
  either.

## Content completeness (mandatory pre-writing step)

Before drafting a single word (once per article, never as a retrofit):

- Search the focus keyword and read the top 3 currently-ranking Google pages.
- Note every true, verifiable fact, angle and subtopic they cover: dates,
  names, numbers, anecdotes, context.
- Cover everything relevant they cover, no gaps; never leave out a real,
  relevant fact because the article "felt long enough".
- Beat all three: more complete, more accurate, better written. Better
  written means real flow and voice for a music fan who wants the real
  story, not more facts crammed in or writing for a search engine.
- Facts found here still go through the no-hallucination rule: verified only.

## Title, Key Facts, year links (beyond CLAUDE.md pipeline step 4)

- Title tag ≤60 chars total; add " | 1960smusic.net" only if it fits.
  Byline always shows Published and Updated (same on a new page; Updated =
  `dateModified`). When to bump Updated: CLAUDE.md "Updated Dates".
- Key Facts box (song/artist) sits straight after the intro, before the
  featured image. Song rows: Released, Label, Written by, Produced by, US/UK
  peak. Artist rows: Origin, Genre, Label, Peak chart hits. Values from
  `gen/key_facts_data.py` (verified, omit unconfirmed), then
  `gen/build_key_facts.py --write`. Box excluded from word count and density.
- Trending posts weave their year-page link into a sentence naming that
  year. Genre hubs link every key year in `gen/genre_peak_years.py` (edit
  that file if a hub's story shifts).
- `og:image` and JSON-LD `image`: self-hosted, never hotlinked.

## Structure

- Fixed order: H1, then the intro/lead paragraph, then the Key Facts box
  (song/artist only), then the featured image, then the Table of Contents, then the YouTube embed, then the
  rest of the body (sections, FAQ, closing paragraph).
- FAQ: 4-6 questions, no fixed word count per answer.
- FAQ questions should be real questions people actually search for
  where practical, not invented-sounding. Source them from actual web
  search per article rather than guessing at plausible phrasing.
- Article + FAQPage + BreadcrumbList JSON-LD schema text matches the
  visible page content. If body copy is edited (including density
  trims), the matching schema text gets edited too in the same pass.
- 3-5 internal links in the body, each distinct URL used once.
- Sources (2026-11-10): song, artist, genre and trending pages link at
  least 3 distinct authoritative external sources in the body (Wikipedia,
  Billboard, Official Charts, Rock Hall, label/artist sites; never
  YouTube/TikTok/streaming/social). Applies to new pages. Weekly refresh:
  any page refreshed must be brought up to 3 in the same pass.
  `check_article.py` enforces it once Published or Updated is 2026-11-10+.
- Meta description 120-160 characters, focus keyword included (enforced).
- No hallucination: an unverifiable date, quote, or stat gets left out
  of the article, not guessed at or smoothed over.

## What check_article.py can and can't enforce

Checked: word count, TOC, image + alt, YouTube/TikTok embeds, banned
words, one sentence per line, em dashes, placeholders, FAQ count,
sentence length, keyword density and placements, meta length, sources.
Judgment calls, not scripted: real lists vs. run-ons, PAA questions
really sourced, prose sensory vs. generic, schema text still matching
visible content after an edit.
