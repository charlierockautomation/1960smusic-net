# Writing Standard

Single source of truth for how every article on this site is written.
`docs/article-template.html` implements the structure; `gen/check_article.py`
enforces everything below that can be checked mechanically. Adopted
2026-08-16, revised same day, supersedes anything about article writing
said in chat before the most recent revision.

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

## Structure

- Fixed order: H1, then the intro/lead paragraph, then the featured
  image, then the Table of Contents, then the YouTube embed, then the
  rest of the body (sections, FAQ, closing paragraph).
- FAQ: 4-6 questions, no fixed word count per answer.
- FAQ questions should be real questions people actually search for
  where practical, not invented-sounding. Source them from actual web
  search per article rather than guessing at plausible phrasing.
- Article + FAQPage + BreadcrumbList JSON-LD schema text matches the
  visible page content. If body copy is edited (including density
  trims), the matching schema text gets edited too in the same pass.
- 3-5 internal links in the body, each distinct URL used once. At least
  one dofollow external link to an authoritative source (Wikipedia or
  similar) for factual grounding on named entities.
- No hallucination: an unverifiable date, quote, or stat gets left out
  of the article, not guessed at or smoothed over.

## What check_article.py can and can't enforce

Mechanically checked: word count by type, TOC presence, image + alt
text, YouTube embed on song/artist pages, banned words, one-sentence-
per-line, em dashes, unfilled template placeholders, FAQ count (not
answer length), sentence-length distribution, keyword density and its
required placements (title, meta, first 100 words, H2/H3, never
consecutive sentences).

Not mechanically checked, judgment calls made while writing: whether a
3+ item list is really a list vs. a run-on sentence, whether PAA
questions are genuinely sourced from search vs. invented, whether prose
reads "sensory and specific" vs. generic, whether schema text still
matches visible content after an edit. These stay a human/agent
discipline, not a script.
