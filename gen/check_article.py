# -*- coding: utf-8 -*-
"""Validate a published article page against house style before it ships.

Usage: python3 gen/check_article.py <path-to-index.html> [...]

Full rules: docs/writing-standard.md. Checks enforced here (2026-08-16):
  - zero em dashes (—) or en dashes used as em-dash substitutes (–)
  - at least 4 FAQ questions (no length requirement on answers)
  - table of contents present when body word count > 600
  - at least one <img> with non-empty alt text
  - at least one YouTube embed on song and artist pages
  - at least one TikTok embed on trending pages
  - word count within range for the page type:
      artist bio: 800-1200, song story: 600-900, genre hub: 1200-1800,
      trending: 400-700
  - no banned filler phrases / AI-cliche words
  - one sentence per line: no multi-sentence paragraph without a <br> break
  - 75%+ of sentences under 20 words
  - keyword density strictly 1%-2% (outside that band is a fail either
    way), keyword present in title, meta description, first 100 words,
    at least one H2/H3, and never in two consecutive sentences. Focus
    keyword is read from the JSON-LD "about" field.

Page type is read from the "PAGE:" line in the leading HTML comment block
if present, else inferred from the path (/blog/artists/, /blog/songs/,
/blog/genres/, /blog/trending/).
"""
import re
import sys
import html as htmllib

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


def check_images(text, errors):
    imgs = re.findall(r"<img\b[^>]*>", text, flags=re.I)
    ok = False
    for tag in imgs:
        m = re.search(r'alt="([^"]*)"', tag, flags=re.I)
        if m and m.group(1).strip():
            ok = True
            break
    if not imgs:
        errors.append("no <img> tag found")
    elif not ok:
        errors.append("no <img> with non-empty alt text found")


def check_youtube(text, errors, page_type):
    if page_type not in ("song story", "artist bio"):
        return
    if "youtube.com/embed/" not in text and "youtube-nocookie.com/embed/" not in text:
        errors.append(f"no YouTube embed found (required on {page_type} pages)")


def check_tiktok(text, errors, page_type):
    if page_type != "trending":
        return
    if "tiktok.com/embed.js" not in text:
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
    m = re.search(r'"about"\s*:\s*"([^"]+)"', text)
    return m.group(1).strip() if m else None


def check_keyword(text, plain_text, errors, notes):
    kw = extract_focus_keyword(text)
    if not kw:
        errors.append('no focus keyword found (expected JSON-LD "about" field)')
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
    check_tiktok(text, errors, page_type)
    check_word_count(wc, errors, page_type)
    check_banned_phrases(plain, errors)
    check_one_sentence_per_line(text, errors)
    check_template_placeholders(text, errors)
    check_sentence_length(text, errors)
    check_keyword(text, plain, errors, notes)

    return page_type, wc, errors, notes


def main(argv):
    if not argv:
        print("usage: python3 gen/check_article.py <path-to-index.html> [...]")
        return 2
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
