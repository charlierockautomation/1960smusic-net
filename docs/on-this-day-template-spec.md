# On This Day — Page Template Spec
For: 1960smusic.net /blog/on-this-day/[date-slug]/
Companion file to on-this-day-sources.md (research/sourcing rules) — this file is the structural/visual build spec.

Read on-this-day-sources.md FIRST for coverage rules, card structure, media rules, and internal-linking rules. This file is how those rules get built.

---

## URL PATTERN
`/blog/on-this-day/september-1/` (one page per calendar date, all 10 years grouped on it)

## JSON DATA FILE
`/data/on-this-day/09-01.json`

```json
{
  "date_label": "September 1",
  "date_slug": "september-1",
  "flagship": {
    "year": 1969,
    "category": "culture",
    "headline": "Woodstock's midnight deadline",
    "summary_line_1": "...",
    "summary_line_2": "...",
    "youtube_id": null,
    "image": null
  },
  "stats": [
    { "value": 27, "label": "verified events" },
    { "value": 6, "label": "chart milestones" },
    { "value": 4, "label": "watchable clips" }
  ],
  "years": [
    {
      "year": 1969,
      "events": [
        {
          "category": "concert",
          "headline": "Hendrix lights up Red Rocks",
          "summary_line_1": "The Jimi Hendrix Experience headlined the Colorado amphitheater with Vanilla Fudge and Soft Machine opening.",
          "summary_line_2": "It was one of the era's loudest and most electric outdoor bills.",
          "youtube_id": "abc123",
          "image": null,
          "internal_link": { "text": "Jimi Hendrix Experience", "url": "/blog/artists/jimi-hendrix-experience/" },
          "external_link": null
        }
      ]
    }
  ]
}
```
`category` enum: `birth | death | release | chart | concert | festival | broadcast | industry | culture`
Only ONE of `youtube_id` / `image` populated per event, video wins if both are legitimately available.

## PAGE LAYOUT (top to bottom)

1. **Hero band** — eyebrow "On this day in 1960s music", H1 = date_label, vivid year-pill nav row. Each pill is `<a href="#y{year}">`. Current/most-recent year pill visually distinct (filled, not outlined).

2. **Flagship callout** — full-width accent-colored card, the single best story of the day, larger type than regular cards, embed if `youtube_id` present.

3. **Stat strip** — 3 metric cards side by side (event count, category count, clip count — computed from the data, not hardcoded).

4. **Year sections** — for each year 1969 down to 1960 (most recent first):
   - `<section id="y{year}">` wrapper
   - Small uppercase year label divider
   - One card per event in that year, identical structure every time (category badge → headline → 2-sentence summary → optional media → inline internal/external link woven into the sentence)

5. **FAQ block** — 4-6 Q&As generated from that day's actual events, written last after cards are finalized. This is the schema-tagged AI-citation asset.

6. **Closing internal links** — "More On This Day" row linking to 2-3 adjacent/related dates once they exist (skip if this is the first page live).

## SCHEMA
- `CreativeWork` objects for each entry, wrapped in `ItemList` (not `Event`,
  GSC flags Event items missing required `location`; these are historical,
  not upcoming ticketed events, so CreativeWork avoids that check entirely)
- `FAQPage` for the FAQ block
- `BreadcrumbList` (Home > Blog > On This Day > September 1)

## STYLING NOTES
- Vivid, high-contrast category colors — this is the one place on the site allowed to be louder/more colorful than the standard article template, since the page's job is to feel like a scannable event feed, not a long-form essay
- Anchor-jump nav must have smooth scroll and account for any sticky header offset
- Cards use consistent border-radius, spacing, and badge styling across every single card, every day — the repetition is a feature, not a bug, it's what makes a 27-card page still feel organized
