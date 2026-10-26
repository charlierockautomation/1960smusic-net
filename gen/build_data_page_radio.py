# -*- coding: utf-8 -*-
"""Build /data/1960s-music-genres-by-year/ (Phase 3 data page 1).

Every figure on the page is computed here from data/radio-eligible-*.json,
so the table, chart and prose cannot drift from the data. Re-run after the
radio lists change; gen/test_data_page_radio.py checks the page against them.

Usage: python3 gen/build_data_page_radio.py
"""
import collections
import glob
import html
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SLUG = "/data/1960s-music-genres-by-year/"
OUT_DIR = os.path.join(ROOT, SLUG.strip("/"))
IMG = "1960s-music-genres-by-year-chart.png"
KW = "1960s music genres"
PUBLISHED = "2026-10-26"

# station order and display names; hub slug == genre id except 60s-rock umbrella
GENRES = [
    ("british-invasion", "British Invasion"),
    ("motown-soul", "Motown, Soul & R&B"),
    ("folk-rock", "Folk Rock"),
    ("psychedelic-rock", "Psychedelic Rock"),
    ("garage-surf-rock", "Garage & Surf Rock"),
    ("country-60s", "Country"),
    ("pop-brill-building", "Pop & Brill Building"),
    ("jazz-easy-listening", "Jazz & Easy Listening"),
]
SHORT = {"british-invasion": "British Invasion", "motown-soul": "Motown & Soul", "folk-rock": "Folk Rock",
         "psychedelic-rock": "Psychedelic", "garage-surf-rock": "Garage & Surf", "country-60s": "Country",
         "pop-brill-building": "Pop & Brill", "jazz-easy-listening": "Jazz & Easy"}
YEARS = list(range(1960, 1970))

# one plain sentence per genre, paraphrased from data/genres.json descriptions
BLURB = {
    "british-invasion": "Beat groups from the UK followed The Beatles to America after 1964, pairing jangling guitars with tight harmonies.",
    "motown-soul": "It covers Detroit's polished Motown formula and the grittier, gospel-fueled soul of the American South.",
    "folk-rock": "Acoustic protest songwriting plugged in, from Bob Dylan going electric in 1965 to The Byrds' twelve-string Rickenbacker.",
    "psychedelic-rock": "It used studio effects, modal drones and long improvisation to turn the era's mind-expanding experiments into sound.",
    "garage-surf-rock": "Teenagers playing raw rock on cheap amps and combo organs sit beside reverb-heavy surf instrumentals from Southern California.",
    "country-60s": "The decade split between the string-smoothed Nashville Sound and the twangy Bakersfield Sound of Buck Owens and Merle Haggard.",
    "pop-brill-building": "Professional songwriting teams at New York's Brill Building powered girl groups, teen idols and, late on, bubblegum pop.",
    "jazz-easy-listening": "This is sophisticated adult pop: swinging vocalists, lush film themes and bossa nova from composers like Burt Bacharach and Henry Mancini.",
}


def load():
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "radio-eligible-*.json"))):
        with open(f, encoding="utf-8") as fh:
            rows += json.load(fh)
    return rows


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))


def stats(rows):
    cell = collections.Counter((r["year"], r["genre"]) for r in rows)
    ytot = collections.Counter(r["year"] for r in rows)
    gtot = collections.Counter(r["genre"] for r in rows)
    unique = len({(norm(r["title"]), norm(r["artist"])) for r in rows})
    return cell, ytot, gtot, unique


def pct(n, d):
    return f"{round(n / d * 100)}%"


def esc(s):
    return html.escape(s, quote=False)


def make_chart(cell, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors = ["#1F4E79", "#B8312F", "#6A8E3A", "#7B3F98", "#D98E04", "#8A5A2B", "#E377A2", "#2A9D8F"]
    fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor("#F5EEDC")
    ax.set_facecolor("#F5EEDC")
    bottom = [0] * len(YEARS)
    for (gid, _), color in zip(GENRES, colors):
        vals = [cell[(y, gid)] for y in YEARS]
        ax.bar([str(y) for y in YEARS], vals, bottom=bottom, color=color, label=SHORT[gid], width=0.72)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for i, b in enumerate(bottom):
        ax.text(i, b + 1, str(b), ha="center", va="bottom", fontsize=11, color="#1A1310")
    ax.set_title("Songs on the Radio Dial by year and genre (our dataset)", fontsize=15, color="#1A1310", loc="left")
    ax.set_ylabel("Songs", color="#1A1310")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors="#1A1310")
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=10)
    fig.text(0.99, 0.01, "1960smusic.net", ha="right", fontsize=9, color="#5B4A38")
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)


def build():
    rows = load()
    cell, ytot, gtot, unique = stats(rows)
    total = len(rows)
    ps = {y: cell[(y, "psychedelic-rock")] for y in YEARS}
    ps_total = gtot["psychedelic-rock"]
    ps_first = min(y for y in YEARS if ps[y])
    ps_peak = max(YEARS, key=lambda y: ps[y])
    ps_peak_share = pct(ps[ps_peak], ytot[ps_peak])
    ps_peak_of_all = pct(ps[ps_peak], ps_total)
    after = [y for y in YEARS if y > ps_peak]
    lead_g = sorted(gtot, key=lambda g: -gtot[g])
    zero_cells = sum(1 for y in YEARS for g, _ in GENRES if cell[(y, g)] == 0)
    small = [y for y in YEARS if ytot[y] < 20]
    names = dict(GENRES)
    pre = YEARS[0:YEARS.index(ps_first)]
    pre_label = f"{pre[0]} to {pre[-1]}"

    # --- table ---
    head = "".join(f'<th><a href="/blog/genres/{g}/">{esc(SHORT[g])}</a></th>' for g, _ in GENRES)
    trs = []
    for y in YEARS:
        tds = "".join(
            f'<td>{cell[(y, g)]} <span>({pct(cell[(y, g)], ytot[y])})</span></td>' if cell[(y, g)] else "<td>0</td>"
            for g, _ in GENRES)
        trs.append(f'<tr><th scope="row"><a href="/1960s/{y}/">{y}</a></th>{tds}<td>{ytot[y]}</td></tr>')
    foot = "".join(f"<td>{gtot[g]} <span>({pct(gtot[g], total)})</span></td>" for g, _ in GENRES)
    table = (
        '<div class="table-scroll">\n<table class="data-table">\n'
        "<caption>Songs on the Radio Dial by year and primary genre, with each genre's share of that year</caption>\n"
        f'<thead><tr><th scope="col">Year</th>{head}<th scope="col">All</th></tr></thead>\n<tbody>\n'
        + "\n".join(trs)
        + f'\n<tr><th scope="row">All years</th>{foot}<td>{total}</td></tr>\n</tbody>\n</table>\n</div>'
    )

    # --- genre sections ---
    gsec = []
    for g, nm in GENRES:
        ys = [y for y in YEARS if cell[(y, g)]]
        peak = max(YEARS, key=lambda y: (cell[(y, g)], -y))
        gsec.append(
            f'<h3 id="{g}"><a href="/blog/genres/{g}/">{esc(nm)}</a></h3>\n'
            f"<p>{esc(BLURB[g])}<br>\n"
            f"Our dataset holds {gtot[g]} songs here, {pct(gtot[g], total)} of the dial, from {ys[0]} to {ys[-1]} and most in {peak} ({cell[(peak, g)]}).</p>"
        )

    small_line = ""
    if small:
        small_line = (f"<br>\nYears under 20 songs ({', '.join(map(str, small))}) are a small sample, so read their shares loosely.")

    L = {}
    L["title"] = "1960s Music Genres by Year: What Our Radio Dial Holds"
    L["h1"] = "1960s Music Genres by Year: What Our Radio Dial Holds"
    L["desc"] = (f"1960s music genres by year, counted across {unique} songs on our Radio Dial. See where each genre peaks, "
                 f"when psychedelic rock appears, and how the mix shifts.")
    lead = (f"These 1960s music genres add up to {unique} songs on the 1960smusic.net <a href=\"/tools/radio/\">Radio Dial</a>, counted by year.<br>\n"
            f"Every number here comes from our dataset, a list of songs we checked and cleared for playback.<br>\n"
            f"It is not a census of the decade.")
    insight = (
        f"<p>Psychedelic rock is the sharpest shift in our dataset.<br>\n"
        f"It has no songs from {pre_label}, then {ps[ps_first]} in {ps_first}.<br>\n"
        f"{ps_peak} holds {ps[ps_peak]} of its {ps_total} songs ({ps_peak_of_all}), and psychedelic rock fills {ps_peak_share} of that year on the dial.<br>\n"
        f"By {after[-1]} it is down to {ps[after[-1]]}.</p>\n"
        f"<p>Read that as the dial, not the decade.<br>\n"
        f"Our list has more songs for the mid-1960s than for the early years, so counts rise with it.<br>\n"
        f'The <a href="/blog/genres/psychedelic-rock/">psychedelic rock guide</a> tells the story behind the numbers.</p>'
    )
    top, second = lead_g[0], lead_g[1]
    table_intro = (
        f"<p>This table counts each song once, under its primary genre.<br>\n"
        f"Each cell shows the count and that genre's share of the year.<br>\n"
        f"{esc(SHORT[top])} leads overall with {gtot[top]} songs ({pct(gtot[top], total)}), ahead of {esc(SHORT[second])} with {gtot[second]}.<br>\n"
        f"{zero_cells} of the {len(YEARS) * len(GENRES)} year and genre cells are empty, which mostly marks styles that had not yet arrived.{small_line}</p>"
    )
    method = (
        f"<p>The Radio Dial lists {total} songs across eight stations, and {unique} of them are unique.<br>\n"
        f"Wild Thing by The Troggs sits on two stations, so it is counted in both.<br>\n"
        f"Each song sits under the release year recorded in our list.</p>"
    )
    faq = [
        ("What were the main 1960s music genres?",
         "Our dataset sorts the Radio Dial into eight genres.<br>\nThey run from British Invasion and Motown to psychedelic rock and easy listening."),
        ("When does psychedelic rock appear in the Radio Dial?",
         f"Psychedelic rock first appears in {ps_first} with {ps[ps_first]} songs.<br>\nIt peaks in {ps_peak} with {ps[ps_peak]}."),
        ("Which genre has the most songs on the dial?",
         f"{esc(names[top])} has the most, with {gtot[top]} songs.<br>\n{esc(names[second])} follows with {gtot[second]}."),
        ("Do these counts show which genres were most popular?",
         "No, they show what is on our Radio Dial.<br>\nThe counts reflect how we built the list, not how popular each genre was."),
    ]
    closing = (f'Browse every genre on the <a href="/data/">data index</a> or return to the <a href="/1960s/">1960s year guides</a>.<br>\n'
               f"Listen on the <a href=\"/tools/radio/\">Radio Dial</a> to hear these 1960s music genres for yourself.")

    faq_html = "\n".join(
        f'<details{" open" if i == 0 else ""}>\n<summary>{q}</summary>\n<div class="answer"><p>{a}</p></div>\n</details>'
        for i, (q, a) in enumerate(faq))
    faq_ld = ",\n".join(
        '    {"@type": "Question", "name": %s, "acceptedAnswer": {"@type": "Answer", "text": %s}}'
        % (json.dumps(q, ensure_ascii=False), json.dumps(re.sub(r"<br>\s*", " ", html.unescape(a)), ensure_ascii=False))
        for q, a in faq)

    alt = ("Stacked bar chart of Radio Dial songs per year from 1960 to 1969, split by genre; "
           "psychedelic rock appears in 1966 and peaks in 1967.")
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RTM6T90PRM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-RTM6T90PRM');
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{L['title']}</title>
<meta name="description" content="{html.escape(L['desc'])}">
<link rel="canonical" href="https://1960smusic.net{SLUG}">
<meta property="og:type" content="article">
<meta property="og:title" content="{L['h1']}">
<meta property="og:description" content="{html.escape(L['desc'])}">
<meta property="og:url" content="https://1960smusic.net{SLUG}">
<meta property="og:image" content="https://1960smusic.net{SLUG}{IMG}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#3D2B1F">
<link rel="stylesheet" href="/styles.css">
<style>
.data-table{{min-width:0;font-size:.82rem;}}
.data-table th,.data-table td{{padding:6px 5px;}}
.data-table td span{{display:block;color:var(--ink-soft);font-size:.9em;}}
</style>
<!-- FOCUS KEYWORD: {KW} -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{L['h1']}",
  "description": {json.dumps(L['desc'], ensure_ascii=False)},
  "image": "https://1960smusic.net{SLUG}{IMG}",
  "author": {{"@type": "Person", "name": "Charlie Gillingham", "url": "https://1960smusic.net/about/charlie/"}},
  "publisher": {{
    "@type": "Organization",
    "name": "1960smusic.net",
    "logo": {{"@type": "ImageObject", "url": "https://1960smusic.net/android-chrome-512x512.png"}}
  }},
  "datePublished": "{PUBLISHED}",
  "dateModified": "{PUBLISHED}",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://1960smusic.net{SLUG}"}},
  "about": "{KW}",
  "keywords": "{KW}, 1960s music by year, Radio Dial, music genres of the 1960s"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://1960smusic.net/"}},
    {{"@type": "ListItem", "position": 2, "name": "Data", "item": "https://1960smusic.net/data/"}},
    {{"@type": "ListItem", "position": 3, "name": "1960s Music Genres by Year", "item": "https://1960smusic.net{SLUG}"}}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_ld}
  ]
}}
</script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">1960s<span>music</span>.net</a>
    <button class="nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav" type="button"><span class="bars" aria-hidden="true"></span></button>
    <nav class="site-nav" id="site-nav" aria-label="Primary">
      <a href="/">Home</a>
      <a href="/tools/radio/">Listen Now</a>
      <a href="/blog/">Blog</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
    </nav>
  </div>
</header>

<main>
  <article class="wrap article">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> &rsaquo; <a href="/data/">Data</a> &rsaquo; <span aria-current="page">1960s Music Genres by Year</span>
    </nav>

    <header class="article-header">
      <h1>{L['h1']}</h1>
      <p class="byline">By <a href="/about/charlie/">Charlie Gillingham</a> <span aria-hidden="true">&middot;</span> Published <time datetime="{PUBLISHED}">October 26, 2026</time> <span aria-hidden="true">&middot;</span> Updated <time datetime="{PUBLISHED}">October 26, 2026</time></p>
    </header>

    <div class="article-body">
      <p class="lead">{lead}</p>
      <figure class="featured-image">
        <img src="{IMG}" alt="{alt}" width="1200" height="630">
        <figcaption>Songs on the Radio Dial per year, stacked by primary genre. Chart built from our dataset.</figcaption>
      </figure>
      <h2 id="table-of-contents">Table of Contents</h2>
      <ul>
        <li><a href="#psychedelic">The psychedelic rock shift</a></li>
        <li><a href="#by-year">1960s music genres by year</a></li>
        <li><a href="#genres">The eight genres</a></li>
        <li><a href="#method">How we counted</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
      <hr>
      <h2 id="psychedelic">Psychedelic Rock Arrives in {ps_first}</h2>
      {insight}
      <hr>
      <h2 id="by-year">1960s Music Genres by Year</h2>
      {table_intro}
      {table}
      <hr>
      <h2 id="genres">What Each Genre Means</h2>
{chr(10).join(gsec)}
      <hr>
      <h2 id="method">How We Counted</h2>
      {method}
      <hr>
      <h2 id="faq">FAQ</h2>
{faq_html}
      <hr>
      <p>{closing}</p>
    </div>
  </article>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div>&copy; <span data-year>2026</span> 1960smusic.net</div>
    <nav aria-label="Footer">
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy-policy/">Privacy Policy</a>
      <a href="/terms-of-use/">Terms of Use</a>
    </nav>
  </div>
</footer>

<script src="/site.js" defer></script>
</body>
</html>
"""
    os.makedirs(OUT_DIR, exist_ok=True)
    make_chart(cell, os.path.join(OUT_DIR, IMG))
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {SLUG}: {total} rows, {unique} unique, small-sample years: {small or 'none'}")


if __name__ == "__main__":
    build()
