# -*- coding: utf-8 -*-
"""Validate a published article page against house style before it ships.

Usage: python3 gen/check_article.py <path-to-index.html> [...]
       python3 gen/check_article.py --site     (sitemap/llms.txt sync, run by
                                                gen/publish_prep.py)

Full rules: docs/writing-standard.md. Checks enforced here (2026-08-16):
  - zero em dashes (—) or en dashes used as em-dash substitutes (–)
  - at least 4 FAQ questions (no length requirement on answers)
  - table of contents present when body word count > 600
  - every <img> has descriptive alt text: non-empty, not the filename, not
    identical to its figcaption
  - at least one YouTube embed on song and artist pages
  - every embedded YouTube id has an on-record embeddable=true,
    made_for_kids=false status in gen/yt_status_cache.json
  - at least one TikTok embed on trending pages, unless the page carries a
    `<!-- TIKTOK-EXEMPT: ... -->` comment documenting why no verifiable
    TikTok source exists for that story
  - word count within range for the page type:
      artist bio: 800-1200, song story: 600-900, genre hub: 1200-1800,
      trending: 400-700
  - no banned filler phrases / AI-cliche words
  - one sentence per line: no multi-sentence paragraph without a <br> break
  - 75%+ of sentences under 20 words
  - visible byline linking to /about/charlie/ with a Published <time>
    date, and Article JSON-LD with a Person author plus datePublished and
    dateModified
  - title tag 60 characters or fewer in total (brand suffix only if it fits)
  - visible "Updated <time>" in the byline, equal to Article JSON-LD
    dateModified (and never earlier than Published)
  - song story / artist bio: Key Facts box right after the intro (before
    the featured image) with the required rows, a link to the matching
    /1960s/<year>/ page, and /best-60s-songs/ for songs on that list
  - about / contact / privacy / terms links use the canonical trailing-slash
    form, page canonical matches the page's own URL, and a page already in
    data/posts.json is present in sitemap.xml and llms.txt
  - keyword density strictly 1%-2% (outside that band is a fail either
    way), keyword present in title, meta description, first 100 words,
    at least one H2/H3, and never in two consecutive sentences. Focus
    keyword is read from the JSON-LD "about" field.

Page type is read from the "PAGE:" line in the leading HTML comment block
if present, else inferred from the path (/blog/artists/, /blog/songs/,
/blog/genres/, /blog/trending/).
"""
import json
import os
import re
import sys
import html as htmllib

SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
YT_STATUS_CACHE = os.path.join(os.path.dirname(__file__), "yt_status_cache.json")

BANNED_PHRASES = [
    "in this article",
    "in conclusion",
    "it goes without saying",
    "it is worth noting",
    "delve",
    "tapestry",
    "testament",
    "vibrant",
    "unveil",
    "groundbreaking",
    "seminal",
    "journey",
    "realm",
    "haunting",
    "sonic landscape",
]
SOFT_BANNED_MAX_ONE = [
    "stands the test of time",
]

WORD_COUNT_RANGES = {
    "artist bio": (800, 1200),
    "song story": (600, 900),
    "genre hub": (1200, 1800),
    "trending": (400, 700),
    # Sized off the 1960 page (task 2, 1349 words): chart table, key albums,
    # OTD-linked events, genre shifts and a radio CTA push it well past a
    # song story but the content list doesn't need genre-hub-length prose.
    "year page": (1100, 1800),
    # /best-60s-songs/ (Phase 2 task 12): a 100-row table with a why-it-matters
    # line per song is ~2,500 words by itself, so the range sits above the
    # prose-only types and bounds table plus surrounding prose together.
    "list page": (2800, 4200),
}

EM_DASH = "—"
EN_DASH = "–"


def detect_type(text, path):
    m = re.search(r"PAGE:\s*(.+)", text)
    if m:
        label = m.group(1).strip().lower()
        for key in WORD_COUNT_RANGES:
            if key in label:
                return key
    norm = path if path.startswith("/") else "/" + path
    if "/blog/artists/" in norm:
        return "artist bio"
    if "/blog/songs/" in norm:
        return "song story"
    if "/blog/genres/" in norm:
        return "genre hub"
    if "/blog/trending/" in norm:
        return "trending"
    if "/1960s/" in norm:
        return "year page"
    if "/best-60s-songs/" in norm:
        return "list page"
    return None


def strip_tags(fragment):
    fragment = re.sub(r"<script.*?</script>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<style.*?</style>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return htmllib.unescape(fragment)


def body_html(text):
    """Raw .article-body HTML, tags intact, header/nav/footer chrome excluded."""
    m = re.search(r'class="article-body"[^>]*>(.*)', text, flags=re.S | re.I)
    if m:
        chunk = m.group(1)
        end = re.search(r"</article>", chunk, flags=re.I)
        if end:
            chunk = chunk[:end.start()]
        return chunk
    m2 = re.search(r"<body[^>]*>(.*)</body>", text, flags=re.S | re.I)
    return m2.group(1) if m2 else text


def body_text(text):
    body = re.sub(r"<!--.*?-->", " ", body_html(text), flags=re.S)
    # The Key Facts box is a data table, not prose: out of word count/density.
    body = re.sub(r'<aside class="key-facts".*?</aside>', " ", body, flags=re.S)
    return strip_tags(body)


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9']+", text))


def prose_lines(text):
    """One entry per intended sentence: every <p>, split on <br>, in document
    order. House style is one sentence per line/<br> segment, so this reads
    sentences directly off the markup instead of re-splitting on punctuation
    (which false-positives across headings, TOC entries, and FAQ questions
    that have no sentence-ending punctuation of their own)."""
    lines = []
    for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", body_html(text), flags=re.S | re.I):
        for seg in re.split(r"<br\s*/?>", m.group(1), flags=re.I):
            plain = strip_tags(seg).strip()
            if plain:
                lines.append(plain)
    return lines


def check_em_dashes(text, errors):
    body = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    if EM_DASH in body:
        errors.append("em dash (—) found in file")
    if EN_DASH in body:
        errors.append("en dash (–) found in file")


def check_faq(text, errors):
    answers = re.findall(r'class="answer"><p>(.*?)</p></div>', text, flags=re.S)
    faq_schema_q = 0
    for m in re.finditer(r'"@type"\s*:\s*"FAQPage".*?"mainEntity"\s*:\s*\[(.*?)\]\s*\}', text, flags=re.S):
        faq_schema_q = len(re.findall(r'"@type"\s*:\s*"Question"', m.group(1)))
    count = max(len(answers), faq_schema_q)
    if count < 4:
        errors.append(f"only {count} FAQ question(s) found, need at least 4")


def check_toc(text, errors, wc):
    if wc <= 600:
        return
    has_toc = bool(re.search(r'aria-label="Table of contents"', text, flags=re.I)) or \
        bool(re.search(r"table of contents", text, flags=re.I))
    if not has_toc:
        errors.append(f"body is {wc} words (>600) but no Table of Contents found")


def _filename_words(src):
    base = os.path.splitext(os.path.basename(src))[0]
    return re.sub(r"[-_]+", " ", base).strip().lower()


def check_images(text, errors):
    imgs = re.findall(r"<img\b[^>]*>", text, flags=re.I)
    if not imgs:
        errors.append("no <img> tag found")
        return

    captioned = {}
    for fig_m in re.finditer(r"<figure\b[^>]*>(.*?)</figure>", text, flags=re.S | re.I):
        fig = fig_m.group(1)
        img_m = re.search(r"<img\b[^>]*>", fig, flags=re.I)
        cap_m = re.search(r"<figcaption>(.*?)</figcaption>", fig, flags=re.S | re.I)
        if img_m and cap_m:
            captioned[img_m.group(0)] = strip_tags(cap_m.group(1)).strip()

    for tag in imgs:
        m = re.search(r'alt="([^"]*)"', tag, flags=re.I)
        alt = m.group(1).strip() if m else ""
        src_m = re.search(r'src="([^"]*)"', tag, flags=re.I)
        src = src_m.group(1) if src_m else ""
        short = tag[:70]
        if not alt:
            errors.append(f"<img> missing/empty alt text: {short}")
            continue
        if alt.lower() == _filename_words(src):
            errors.append(f"<img> alt text is just the filename: {short}")
            continue
        caption = captioned.get(tag)
        if caption and alt.lower() == caption.lower():
            errors.append(f"<img> alt text is identical to its caption: {short}")


def check_youtube(text, errors, page_type):
    if page_type not in ("song story", "artist bio"):
        return
    if "youtube.com/embed/" not in text and "youtube-nocookie.com/embed/" not in text:
        errors.append(f"no YouTube embed found (required on {page_type} pages)")


def check_youtube_compliance(text, errors):
    """Every embedded YouTube id must have an on-record embeddable=true,
    made_for_kids=false result in gen/yt_status_cache.json (see
    gen/yt_video_status.py) before it can ship. Covers both a static
    .../embed/<id> URL and a data-pp-yt="<id>" attribute (the shared
    playlist-player component in /assets/js/ loads ids that way, never as
    a static embed URL, since nothing loads until Play is pressed)."""
    ids = set(re.findall(r"youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{11})", text))
    ids |= set(re.findall(r'data-pp-yt="([A-Za-z0-9_-]{11})"', text))
    if not ids:
        return
    cache = json.load(open(YT_STATUS_CACHE)) if os.path.exists(YT_STATUS_CACHE) else {}
    for vid in sorted(ids):
        st = cache.get(vid)
        if not st:
            errors.append(f"YouTube id {vid} has no status on record; run "
                           f"gen/yt_video_status.py {vid} first")
        elif st.get("made_for_kids"):
            errors.append(f"YouTube id {vid} is made-for-kids, cannot be embedded")
        elif not st.get("embeddable"):
            errors.append(f"YouTube id {vid} is not embeddable per its on-record status")


def check_tiktok(text, errors, page_type):
    if page_type != "trending":
        return
    if "tiktok.com/embed.js" in text:
        return
    if re.search(r"<!--\s*TIKTOK-EXEMPT:", text):
        return
    errors.append("no TikTok embed found (required on trending pages)")


def check_word_count(wc, errors, page_type):
    if page_type not in WORD_COUNT_RANGES:
        return
    lo, hi = WORD_COUNT_RANGES[page_type]
    if not (lo <= wc <= hi):
        errors.append(f"word count {wc} outside {page_type} range {lo}-{hi}")


def check_banned_phrases(plain_text, errors):
    lowered = plain_text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            errors.append(f'banned word/phrase found: "{phrase}"')
    for phrase in SOFT_BANNED_MAX_ONE:
        n = lowered.count(phrase)
        if n > 1:
            errors.append(f'"{phrase}" used {n} times, allowed once per article')


def check_byline(text, errors):
    m = re.search(r'<p class="byline[^"]*">(.*?)</p>', text, flags=re.S | re.I)
    if not m:
        errors.append('no byline found (<p class="byline">)')
    else:
        if 'href="/about/charlie/"' not in m.group(1):
            errors.append("byline does not link to /about/charlie/")
        if not re.search(r'Published\s*<time datetime="\d{4}-\d{2}-\d{2}"', m.group(1)):
            errors.append('byline has no "Published <time datetime=...>" date')
    upd = re.search(r'Updated\s*<time datetime="(\d{4}-\d{2}-\d{2})"', m.group(1)) if m else None
    pub = re.search(r'Published\s*<time datetime="(\d{4}-\d{2}-\d{2})"', m.group(1)) if m else None
    if m and not upd:
        errors.append('byline has no visible "Updated <time datetime=...>" date')
    article = None
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S | re.I):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        if isinstance(data, dict) and data.get("@type") == "Article":
            article = data
    if article is None:
        errors.append("no Article JSON-LD found")
        return
    author = article.get("author") or {}
    if author.get("@type") != "Person" or not author.get("name"):
        errors.append("Article JSON-LD author is not a Person with a name")
    for key in ("datePublished", "dateModified"):
        if not article.get(key):
            errors.append(f"Article JSON-LD missing {key}")
    if upd and article.get("dateModified") and upd.group(1) != article["dateModified"]:
        errors.append(f'visible Updated date {upd.group(1)} does not match JSON-LD dateModified {article["dateModified"]}')
    if upd and pub and upd.group(1) < pub.group(1):
        errors.append("Updated date is earlier than Published date")
    if pub and article.get("datePublished") and pub.group(1) != article["datePublished"]:
        errors.append(f'visible Published date {pub.group(1)} does not match JSON-LD datePublished {article["datePublished"]}')


def check_title_length(text, errors):
    m = re.search(r"<title>(.*?)</title>", text, flags=re.S)
    if not m:
        errors.append("no <title> tag")
        return
    title = htmllib.unescape(m.group(1)).strip()
    if len(title) > 60:
        errors.append(f"title tag is {len(title)} chars (max 60 in total): {title!r}")


KEY_FACT_LABELS = {
    "song story": ["Released", "Label", "Written by", "Produced by"],
    "artist bio": ["Origin", "Genre", "Label", "Peak chart hits"],
}


def check_key_facts(text, errors, page_type, path):
    """Song stories and artist bios: Key Facts box after the intro, plus
    the required /1960s/<year>/ link (and /best-60s-songs/ when listed)."""
    if page_type not in KEY_FACT_LABELS:
        return
    m = re.search(r'<aside class="key-facts"[^>]*>(.*?)</aside>', text, flags=re.S)
    if not m:
        errors.append("no Key Facts box (<aside class=\"key-facts\">) after the intro")
        return
    lead = text.find('<p class="lead">')
    fig = text.find('<figure class="featured-image">')
    if not (0 <= lead < m.start() < fig):
        errors.append("Key Facts box must sit after the lead paragraph and before the featured image")
    labels = re.findall(r"<dt>(.*?)</dt>", m.group(1))
    for need in KEY_FACT_LABELS[page_type]:
        if need not in labels:
            errors.append(f'Key Facts box missing "{need}" row')
    if page_type == "song story" and not any("peak" in l.lower() for l in labels):
        errors.append('Key Facts box needs at least one chart "peak" row (US peak / UK peak)')
    for dd in re.findall(r"<dd>(.*?)</dd>", m.group(1), flags=re.S):
        if not re.sub(r"<[^>]+>", "", dd).strip():
            errors.append("Key Facts box has an empty value")
    year_links = set(re.findall(r'href="/1960s/(\d{4})/"', text))
    if not year_links:
        errors.append("no link to a /1960s/<year>/ year page")
    elif page_type == "song story":
        sub = re.search(r'"@type":\s*"MusicRecording".*?"datePublished":\s*"(\d{4})"', text, flags=re.S)
        if sub and sub.group(1) not in year_links:
            errors.append(f"song story must link to /1960s/{sub.group(1)}/ (its release year)")
    if page_type == "song story":
        slug = os.path.basename(os.path.dirname(os.path.abspath(path)))
        try:
            with open(os.path.join(SITE_ROOT, "best-60s-songs", "index.html"), encoding="utf-8") as f:
                listed = f'href="/blog/songs/{slug}/"' in f.read()
        except OSError:
            listed = False
        if listed and 'href="/best-60s-songs/"' not in text:
            errors.append("song is on /best-60s-songs/ but the page does not link to it")


LEGAL_BAD = re.compile(r'href="/(about|contact|privacy-policy|terms-of-use)(\.html)?["#?]')


def check_site_links(text, path, errors):
    bad = sorted({m.group(1) for m in LEGAL_BAD.finditer(text)})
    if bad:
        errors.append("non-canonical links (need trailing slash): " + ", ".join("/" + b for b in bad))
    if "<span data-year>" not in text:
        errors.append("footer copyright year missing the dynamic <span data-year> hook")
    rel = os.path.relpath(os.path.abspath(path), SITE_ROOT).replace(os.sep, "/")
    url = "/" if rel == "index.html" else "/" + rel[: -len("index.html")] if rel.endswith("index.html") else "/" + rel
    m = re.search(r'<link rel="canonical" href="https://1960smusic\.net([^"]*)"', text)
    if m and m.group(1) != url:
        errors.append(f"canonical {m.group(1)} does not match page URL {url}")


def check_published_listing(path, errors):
    """A page already in data/posts.json is live: it must be in sitemap.xml and llms.txt."""
    rel = os.path.relpath(os.path.abspath(path), SITE_ROOT).replace(os.sep, "/")
    if not rel.endswith("index.html"):
        return
    slug = "/" + rel[: -len("index.html")]
    try:
        with open(os.path.join(SITE_ROOT, "data", "posts.json"), encoding="utf-8") as f:
            live = {p["slug"] for p in json.load(f)["posts"]}
    except (OSError, ValueError):
        return
    if slug not in live:
        return
    for name, needle in (("sitemap.xml", f"<loc>https://1960smusic.net{slug}</loc>"), ("llms.txt", f"(https://1960smusic.net{slug})")):
        try:
            with open(os.path.join(SITE_ROOT, name), encoding="utf-8") as f:
                if needle not in f.read():
                    errors.append(f"live page missing from {name}: run python3 gen/publish_prep.py")
        except OSError:
            errors.append(f"{name} not found")


def check_site():
    """sitemap.xml must match what generate_sitemap.py would write (same URLs
    and lastmod); llms.txt must match generate_llms_txt.py output."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import generate_sitemap
    errors = []
    want = generate_sitemap.build_urls()
    with open(os.path.join(SITE_ROOT, "sitemap.xml"), encoding="utf-8") as f:
        have = {m[0]: m[1] for m in re.findall(r"<loc>https://1960smusic\.net([^<]*)</loc>\s*<lastmod>([^<]*)</lastmod>", f.read())}
    for loc in sorted(set(want) - set(have)):
        errors.append(f"sitemap.xml missing {loc}")
    for loc in sorted(set(have) - set(want)):
        errors.append(f"sitemap.xml lists {loc} but no live page found")
    for loc in sorted(set(want) & set(have)):
        if want[loc][0] != have[loc]:
            errors.append(f"sitemap.xml lastmod for {loc} is {have[loc]}, page says {want[loc][0]}")
    import generate_llms_txt as g
    sections = []
    for name, post_type in g.SECTIONS:
        sections.append((name, g.live_tools() if post_type is None else g.posts_by_type(post_type)))
    expected = g.render(g.cap_sections(sections), None)
    with open(os.path.join(SITE_ROOT, "llms.txt"), encoding="utf-8") as f:
        if f.read() != expected:
            errors.append("llms.txt is stale: run python3 gen/generate_llms_txt.py")
    return errors


SUBJECT_TYPES = {"artist bio": ("MusicGroup", "Person"), "song story": ("MusicRecording",)}


def check_schema_subject(text, errors, page_type):
    """Artist bios and song stories: Article.about must reference the page's
    MusicGroup/Person or MusicRecording block by @id, not a keyword string."""
    allowed = SUBJECT_TYPES.get(page_type)
    if not allowed:
        return
    nodes = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S | re.I):
        try:
            nodes.append(json.loads(block))
        except ValueError:
            errors.append("JSON-LD block does not parse")
    article = next((n for n in nodes if isinstance(n, dict) and n.get("@type") == "Article"), None)
    about = (article or {}).get("about")
    if not isinstance(about, dict) or about.get("@type") not in allowed or not about.get("@id"):
        errors.append("Article JSON-LD about must be {@type: %s, @id: ...}" % " or ".join(allowed))
        return
    if not any(isinstance(n, dict) and n.get("@id") == about["@id"] and n.get("@type") in allowed for n in nodes):
        errors.append("Article JSON-LD about @id matches no %s block on the page" % "/".join(allowed))


def check_template_placeholders(text, errors):
    leftover = sorted(set(re.findall(r"\{\{[A-Z0-9_.|-]+\}\}", text)))
    if leftover:
        shown = ", ".join(leftover[:8]) + (", ..." if len(leftover) > 8 else "")
        errors.append(f"{len(leftover)} unfilled article-template.html placeholder(s) left in file: {shown}")


ABBREVIATIONS = ["Mr", "Mrs", "Ms", "Dr", "St", "Sgt", "Capt", "Rev", "Jr", "Sr", "vs", "etc"]


def _strip_abbreviation_periods(plain):
    for abbr in ABBREVIATIONS:
        plain = re.sub(r"\b" + abbr + r"\.", abbr, plain)
    return plain


def check_one_sentence_per_line(text, errors):
    for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", text, flags=re.S | re.I):
        inner = m.group(1)
        segments = re.split(r"<br\s*/?>", inner, flags=re.I)
        for seg in segments:
            plain = strip_tags(seg).strip()
            if not plain:
                continue
            plain_checked = _strip_abbreviation_periods(plain)
            # sentence boundary = terminator + space + capital letter, not inside a tag
            boundaries = re.findall(r'[.!?]"?\s+[A-Z]', plain_checked)
            if len(boundaries) >= 1:
                snippet = plain[:70].strip()
                errors.append(f"multiple sentences without a line break: \"{snippet}...\"")


def check_sentence_length(text, errors):
    sents = prose_lines(text)
    if not sents:
        return
    lengths = [len(re.findall(r"[A-Za-z0-9']+", s)) for s in sents]
    under20 = sum(1 for n in lengths if n < 20)
    pct = under20 / len(lengths) * 100
    if pct < 75:
        errors.append(f"only {pct:.0f}% of sentences are under 20 words, need 75%+")


def extract_focus_keyword(text):
    # artist bios, song stories and trending carry it in a comment, since their
    # JSON-LD "about" is a structured entity; other types still use "about"
    m = re.search(r"^\s*(?:<!--)?\s*FOCUS KEYWORD:\s*(.+?)\s*(?:-->)?\s*$", text, flags=re.M) or re.search(r'"about"\s*:\s*"([^"]+)"', text)
    return m.group(1).strip() if m else None


def check_keyword(text, plain_text, errors, notes):
    kw = extract_focus_keyword(text)
    if not kw:
        errors.append('no focus keyword found (expected <!-- FOCUS KEYWORD: ... --> or JSON-LD "about")')
        return

    wc = word_count(plain_text)
    kw_words = len(kw.split())
    occ = len(re.findall(re.escape(kw), plain_text, re.I))
    density = (occ * kw_words / wc * 100) if wc else 0

    if density > 2:
        errors.append(f'keyword density {density:.2f}% for "{kw}" (over 2% is a stuffing flag)')
    elif density < 1:
        errors.append(f'keyword density {density:.2f}% for "{kw}" (under 1% is not enough signal)')

    title_m = re.search(r"<title>(.*?)</title>", text, flags=re.S | re.I)
    title = htmllib.unescape(title_m.group(1)) if title_m else ""
    if kw.lower() not in title.lower():
        errors.append(f'focus keyword "{kw}" not found in <title>')

    desc_m = re.search(r'name="description"\s+content="([^"]*)"', text, flags=re.I)
    desc = htmllib.unescape(desc_m.group(1)) if desc_m else ""
    if kw.lower() not in desc.lower():
        errors.append(f'focus keyword "{kw}" not found in meta description')

    # slice on the original text (punctuation intact) so keywords containing
    # punctuation (parentheses, hyphens, ampersands) can still match; a
    # token-stripped rebuild would silently lose that punctuation
    word_ends = [m.end() for m in re.finditer(r"[A-Za-z0-9']+", plain_text)][:100]
    first_100 = plain_text[:word_ends[-1]] if word_ends else ""
    if kw.lower() not in first_100.lower():
        errors.append(f'focus keyword "{kw}" not found in first 100 words of body')

    heading_text = " ".join(re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body_html(text), flags=re.S | re.I))
    heading_text = strip_tags(heading_text)
    if kw.lower() not in heading_text.lower():
        # long keywords (6+ words) can make "one more occurrence" mathematically
        # exceed the 2% density cap on its own; when that's the case, this
        # placement requirement is infeasible rather than skipped, so don't fail it
        would_be_density = ((occ + 1) * kw_words / wc * 100) if wc else 0
        if would_be_density <= 2:
            errors.append(f'focus keyword "{kw}" not found in any H2/H3')
        else:
            notes.append(f'focus keyword "{kw}" ({kw_words} words) not in any H2/H3, but adding one would '
                          f'push density to {would_be_density:.2f}% (over the 2% cap) at {wc} words, so this is skipped')

    sents = prose_lines(text)
    has_kw = [bool(re.search(re.escape(kw), s, re.I)) for s in sents]
    for i in range(len(has_kw) - 1):
        if has_kw[i] and has_kw[i + 1]:
            errors.append(f'focus keyword "{kw}" appears in two consecutive sentences (around: "{sents[i][:60]}...")')
            break


def check_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    page_type = detect_type(text, path)
    plain = body_text(text)
    wc = word_count(plain)

    errors = []
    notes = []
    check_em_dashes(text, errors)
    check_faq(text, errors)
    check_toc(text, errors, wc)
    check_images(text, errors)
    check_youtube(text, errors, page_type)
    check_youtube_compliance(text, errors)
    check_tiktok(text, errors, page_type)
    check_word_count(wc, errors, page_type)
    check_banned_phrases(plain, errors)
    check_one_sentence_per_line(text, errors)
    check_template_placeholders(text, errors)
    check_byline(text, errors)
    check_title_length(text, errors)
    check_key_facts(text, errors, page_type, path)
    check_site_links(text, path, errors)
    check_published_listing(path, errors)
    check_schema_subject(text, errors, page_type)
    check_sentence_length(text, errors)
    check_keyword(text, plain, errors, notes)

    return page_type, wc, errors, notes


def main(argv):
    if not argv:
        print("usage: python3 gen/check_article.py <path-to-index.html> [...] | --site")
        return 2
    if argv == ["--site"]:
        errs = check_site()
        for e in errs:
            print(f"  FAIL: {e}")
        print("site check: " + ("FAIL" if errs else "PASS (sitemap.xml and llms.txt in sync)"))
        return 1 if errs else 0
    failed = False
    for path in argv:
        page_type, wc, errors, notes = check_file(path)
        print(f"{path}  [{page_type or 'unknown type'}, {wc} words]")
        for n in notes:
            print(f"  NOTE: {n}")
        if errors:
            failed = True
            for e in errors:
                print(f"  FAIL: {e}")
        else:
            print("  PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
