# -*- coding: utf-8 -*-
"""Build /data/1960s-musicians-by-song-count/ (Phase 3 data page 2).

Counts songs per credited act on the Radio Dial (data/radio-eligible-*.json).
Every figure on the page is computed here, so the table, chart and prose
cannot drift from the data. gen/test_data_page_artists.py checks the page.

Usage: python3 gen/build_data_page_artists.py
"""
import collections
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_data_page_radio as radio  # shares loader, genre names, page chrome

ROOT = radio.ROOT
SLUG = "/data/1960s-musicians-by-song-count/"
OUT_DIR = os.path.join(ROOT, SLUG.strip("/"))
IMG = "1960s-musicians-by-song-count-chart.png"
KW = "1960s musicians"
PUBLISHED = "2026-11-09"
PUBLISHED_LABEL = "November 9, 2026"
TOP_N = 20
YEARS = radio.YEARS
GENRES = radio.GENRES
GENRE_NAME = dict(GENRES)
SHORT = radio.SHORT
COLORS = dict(zip([g for g, _ in GENRES],
                  ["#1F4E79", "#B8312F", "#6A8E3A", "#7B3F98", "#D98E04", "#8A5A2B", "#E377A2", "#2A9D8F"]))

# Billing variants of the same act, merged under one name. Duets and
# "with" credits (Marvin Gaye & Tammi Terrell, The Beatles with Billy Preston)
# stay separate because they are credited as a different act.
MERGE = {
    "Little Stevie Wonder": "Stevie Wonder",
    "The Miracles": "Smokey Robinson & The Miracles",
    "The Young Rascals": "The Rascals",
    "Tommy James and the Shondells": "Tommy James & The Shondells",
    "Vince Guaraldi": "Vince Guaraldi Trio",
}
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def load():
    """Unique songs (by youtube_id) with a merged `act` field."""
    rows = radio.load()
    seen, out = set(), []
    for r in rows:
        if r["youtube_id"] in seen:
            continue
        seen.add(r["youtube_id"])
        out.append(dict(r, act=MERGE.get(r["artist"], r["artist"])))
    return rows, out


def stats(songs):
    count = collections.Counter(s["act"] for s in songs)
    order = sorted(count, key=lambda a: (-count[a], a.lower().removeprefix("the ")))
    cutoff = count[order[TOP_N - 1]]
    top = [a for a in order if count[a] >= cutoff]
    info = {}
    gidx = {g: i for i, (g, _) in enumerate(GENRES)}
    for a in top:
        mine = [s for s in songs if s["act"] == a]
        gc = collections.Counter(s["genre"] for s in mine)
        main = sorted(gc, key=lambda g: (-gc[g], gidx[g]))[0]
        ys = sorted({s["year"] for s in mine})
        info[a] = {"n": count[a], "genre": main, "genres": gc, "first": ys[0], "last": ys[-1], "years": ys}
    return count, top, cutoff, info


def bios():
    """Act name -> live bio URL, from data/artists.json where the page exists."""
    with open(os.path.join(ROOT, "data", "artists.json"), encoding="utf-8") as f:
        artists = json.load(f)
    out = {}
    for a in artists:
        slug = a.get("article_slug") or ""
        if slug and os.path.exists(os.path.join(ROOT, slug.strip("/"), "index.html")):
            out[radio.norm(a["name"])] = slug
    return out


def leaders(songs, key):
    c = collections.Counter(s["act"] for s in songs if key(s))
    m = max(c.values())
    return m, sorted(a for a, n in c.items() if n == m)


def esc(s):
    return html.escape(s, quote=False)


def join(names):
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def make_chart(top, info, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor("#F5EEDC")
    ax.set_facecolor("#F5EEDC")
    names = list(reversed(top))
    vals = [info[a]["n"] for a in names]
    ax.barh(names, vals, color=[COLORS[info[a]["genre"]] for a in names], height=0.72)
    for i, v in enumerate(vals):
        ax.text(v + 0.15, i, str(v), va="center", fontsize=8.5, color="#1A1310")
    ax.tick_params(axis="y", labelsize=8.5, colors="#1A1310")
    ax.tick_params(axis="x", colors="#1A1310")
    ax.set_xlabel("Songs on the Radio Dial", color="#1A1310")
    ax.set_title("Acts with the most songs on the Radio Dial (our dataset)", fontsize=15, color="#1A1310", loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    used = [g for g, _ in GENRES if any(info[a]["genre"] == g for a in top)]
    ax.legend(handles=[Patch(color=COLORS[g], label=SHORT[g]) for g in used], loc="lower right",
              frameon=False, fontsize=9, title="Main genre", title_fontsize=9)
    fig.text(0.99, 0.01, "1960smusic.net", ha="right", fontsize=9, color="#5B4A38")
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)


def build():
    rows, songs = load()
    total = len(songs)
    count, top, cutoff, info = stats(songs)
    bio = bios()
    acts = len(count)
    singles = sum(1 for n in count.values() if n == 1)
    top_songs = sum(info[a]["n"] for a in top)
    tied = sum(1 for a in top if info[a]["n"] == cutoff)
    first, second = top[0], top[1]
    f_info = info[first]
    multi = [a for a in top if len(info[a]["genres"]) > 1]

    def act_html(a):
        u = bio.get(radio.norm(a))
        return f'<a href="{u}">{esc(a)}</a>' if u else esc(a)

    # --- table ---
    trs, rank, prev = [], 0, None
    for i, a in enumerate(top, 1):
        d = info[a]
        if d["n"] != prev:
            rank, prev = i, d["n"]
        yrs = str(d["first"]) if d["first"] == d["last"] else f"{d['first']} to {d['last']}"
        trs.append(f'<tr><td>{rank}</td><th scope="row">{act_html(a)}</th><td>{d["n"]}</td>'
                   f'<td>{esc(SHORT[d["genre"]])}</td><td>{yrs}</td></tr>')
    table = (
        '<div class="table-scroll">\n<table class="data-table">\n'
        f"<caption>Acts with the most songs on the Radio Dial: top {TOP_N} with ties, {len(top)} acts</caption>\n"
        '<thead><tr><th scope="col">Rank</th><th scope="col">Act</th><th scope="col">Songs</th>'
        '<th scope="col">Main genre</th><th scope="col">Years in our dataset</th></tr></thead>\n<tbody>\n'
        + "\n".join(trs) + "\n</tbody>\n</table>\n</div>"
    )

    # --- by year ---
    year_items = []
    for y in YEARS:
        ys = [s for s in songs if s["year"] == y]
        m, names = leaders(ys, lambda s: True)
        if len(names) <= 2:
            who = f"{esc(join(names))} with {m} songs" + (" each" if len(names) > 1 else "")
        else:
            who = f"{WORDS.get(len(names), len(names))} acts tie on {m} songs each"
        year_items.append(f'<li><a href="/1960s/{y}/">{y}</a>: {who}, out of {len(ys)} songs.</li>')
    # --- by genre ---
    genre_items = []
    for g, nm in GENRES:
        m, names = leaders(songs, lambda s, g=g: s["genre"] == g)
        gn = sum(1 for s in songs if s["genre"] == g)
        who = esc(join(names)) + (f" with {m} songs each, out of {gn}" if len(names) > 1 else f" with {m} of {gn} songs")
        genre_items.append(f'<li><a href="/blog/genres/{g}/">{esc(nm)}</a>: {who}.</li>')

    first_by_g = f_info["genres"]
    g1, g2 = sorted(first_by_g, key=lambda g: -first_by_g[g])[:2]

    L = {}
    L["title"] = "1960s Musicians With the Most Songs on Our Radio Dial"
    L["h1"] = L["title"]
    L["crumb"] = "1960s Musicians by Song Count"
    L["desc"] = (f"The 1960s musicians with the most songs among {total} on our Radio Dial. "
                 f"{first} lead with {f_info['n']}, ahead of {second} with {info[second]['n']}.")
    lead = (f"{first} lead the 1960s musicians on our <a href=\"/tools/radio/\">Radio Dial</a>, with {f_info['n']} of its {total} songs.<br>\n"
            f"{second} come second with {info[second]['n']}.<br>\n"
            f"Every number here comes from our dataset, the songs we checked and cleared for playback.<br>\n"
            f"It is not a sales chart or a census of the decade.")
    if second == "Bob Dylan":
        lead = lead.replace(f"{second} come second", f"{second} comes second")
    insight = (
        f"<p>{first} hold {f_info['n']} songs, {f_info['n'] - info[second]['n']} more than anyone else.<br>\n"
        f"They have songs in all {len(f_info['years'])} years from {f_info['first']} to {f_info['last']}.<br>\n"
        f"They also split across two stations: {first_by_g[g1]} {esc(SHORT[g1])} songs and {first_by_g[g2]} {esc(SHORT[g2])} songs.</p>\n"
        f"<p>Below the top, the 1960s musicians on our dial run wide rather than deep.<br>\n"
        f"It holds {acts} different acts, and {singles} of them ({radio.pct(singles, acts)}) have a single song.<br>\n"
        f"The {len(top)} acts in the table hold {top_songs} songs, {radio.pct(top_songs, total)} of the dial.</p>"
    )
    table_intro = (
        f"<p>This table ranks the top {TOP_N} acts by song count, with ties shown.<br>\n"
        f"{str(WORDS.get(tied, tied)).capitalize()} acts tie on {cutoff} songs, so the table runs to {len(top)}.<br>\n"
        f"Main genre is the station holding most of that act's songs.<br>\n"
        f"Names link to our artist bios where one exists.</p>"
    )
    method = (
        f"<p>The Radio Dial lists {len(rows)} songs across eight stations, and {total} are unique.<br>\n"
        f"Wild Thing by The Troggs sits on two stations, so we counted it once here.<br>\n"
        f"Songs are counted by the act credited on the record.</p>\n"
        f"<p>Name changes of the same act are merged:</p>\n<ul>\n"
        f"<li>Little Stevie Wonder counts as Stevie Wonder.</li>\n"
        f"<li>The Miracles count as Smokey Robinson &amp; The Miracles.</li>\n"
        f"<li>The Young Rascals count as The Rascals.</li>\n</ul>\n"
        f"<p>Duets and joint credits stay separate, so Marvin Gaye &amp; Tammi Terrell are not added to Marvin Gaye.<br>\n"
        f"Years in our dataset are the first and last years an act appears on the dial, not career dates.</p>"
    )
    faq = [
        ("Who were the most popular 1960s musicians?",
         f"Popularity is hard to measure, and our dataset does not try.<br>\nOn our Radio Dial, {first} have the most songs, with {f_info['n']}."),
        ("Which artist has the most songs on the Radio Dial?",
         f"{first} have {f_info['n']} songs.<br>\n{second} {'is' if second == 'Bob Dylan' else 'are'} next with {info[second]['n']}."),
        ("How many artists are on the Radio Dial?",
         f"The dial holds {acts} different acts across {total} songs.<br>\n{singles} of those acts have one song each."),
        ("Why are some big names missing from the top of the list?",
         "The dial is a list we built and cleared for playback, not every hit of the decade.<br>\nAn act with fewer cleared songs ranks lower here, whatever its fame."),
        ("How are duets and name changes counted?",
         "Name changes of one act are merged, such as Little Stevie Wonder into Stevie Wonder.<br>\nDuets count as their own credited act."),
    ]
    closing = (f'See the genre mix by year on our <a href="/data/1960s-music-genres-by-year/">genres data page</a> or the <a href="/data/">data index</a>.<br>\n'
               f"Tune in on the Radio Dial and hear these 1960s musicians for yourself.")

    faq_html = "\n".join(
        f'<details{" open" if i == 0 else ""}>\n<summary>{q}</summary>\n<div class="answer"><p>{a}</p></div>\n</details>'
        for i, (q, a) in enumerate(faq))
    faq_ld = ",\n".join(
        '    {"@type": "Question", "name": %s, "acceptedAnswer": {"@type": "Answer", "text": %s}}'
        % (json.dumps(q, ensure_ascii=False), json.dumps(re.sub(r"<br>\s*", " ", html.unescape(a)), ensure_ascii=False))
        for q, a in faq)
    alt = (f"Horizontal bar chart of the {len(top)} acts with the most Radio Dial songs, colored by main genre; "
           f"{first} lead with {f_info['n']}, then {second} with {info[second]['n']}.")

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
.data-table{{min-width:0;font-size:.85rem;}}
.data-table th,.data-table td{{padding:6px 6px;}}
.data-table tbody th{{text-align:left;font-weight:600;}}
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
  "keywords": "{KW}, 60s artists, 1960s bands, Radio Dial"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://1960smusic.net/"}},
    {{"@type": "ListItem", "position": 2, "name": "Data", "item": "https://1960smusic.net/data/"}},
    {{"@type": "ListItem", "position": 3, "name": "{L['crumb']}", "item": "https://1960smusic.net{SLUG}"}}
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
      <a href="/">Home</a> &rsaquo; <a href="/data/">Data</a> &rsaquo; <span aria-current="page">{L['crumb']}</span>
    </nav>

    <header class="article-header">
      <h1>{L['h1']}</h1>
      <p class="byline">By <a href="/about/charlie/">Charlie Gillingham</a> <span aria-hidden="true">&middot;</span> Published <time datetime="{PUBLISHED}">{PUBLISHED_LABEL}</time> <span aria-hidden="true">&middot;</span> Updated <time datetime="{PUBLISHED}">{PUBLISHED_LABEL}</time></p>
    </header>

    <div class="article-body">
      <p class="lead">{lead}</p>
      <figure class="featured-image">
        <img src="{IMG}" alt="{esc(alt)}" width="1200" height="630">
        <figcaption>Songs per act on the Radio Dial, colored by main genre. Chart built from our dataset.</figcaption>
      </figure>
      <h2 id="table-of-contents">Table of Contents</h2>
      <ul>
        <li><a href="#lead-finding">{esc(first)} lead the dial</a></li>
        <li><a href="#top-acts">The top {TOP_N} acts, with ties</a></li>
        <li><a href="#by-year">Leading acts year by year</a></li>
        <li><a href="#by-genre">Leading acts by genre</a></li>
        <li><a href="#method">How we counted</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
      <hr>
      <h2 id="lead-finding">{esc(first)} Lead With {f_info['n']} Songs</h2>
      {insight}
      <hr>
      <h2 id="top-acts">The Top 1960s Musicians on the Dial</h2>
      {table_intro}
      {table}
      <hr>
      <h2 id="by-year">Which Act Leads Each Year?</h2>
      <p>Counting all the 1960s musicians on the dial, not only the top {len(top)}, here is who leads each year.<br>
      Busy middle years have clear leaders, while the thinner early and late years end in ties.</p>
      <ul>
{chr(10).join(year_items)}
      </ul>
      <hr>
      <h2 id="by-genre">Which Act Leads Each Genre?</h2>
      <p>Each Radio Dial station has its own leader, out of that station's songs.</p>
      <ul>
{chr(10).join(genre_items)}
      </ul>
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
    make_chart(top, info, os.path.join(OUT_DIR, IMG))
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {SLUG}: {total} unique songs, {acts} acts, top {len(top)} (cutoff {cutoff}); unused bios? multi-genre {multi}")


if __name__ == "__main__":
    build()
