# -*- coding: utf-8 -*-
"""Validate a published article page against house style before it ships.

Usage: python3 gen/check_article.py <path-to-index.html> [...]

Checks enforced (per team spec, 2026-08-14):
  - zero em dashes (—) or en dashes used as em-dash substitutes (–)
  - at least 4 FAQ questions (<dt> or FAQPage schema mainEntity)
  - table of contents present when body word count > 600
  - at least one <img> with non-empty alt text
  - at least one YouTube embed on song and artist pages
  - word count within range for the page type:
      artist bio: 800-1200, song story: 600-900, genre hub: 1200-1800
  - no banned filler phrases
  - one sentence per line: no multi-sentence paragraph without a <br> break

Page type is read from the "PAGE:" line in the leading HTML comment block
if present, else inferred from the path (/blog/artists/, /blog/songs/,
/blog/genres/).
"""
import re
import sys
import html as htmllib

BANNED_PHRASES = [
    "in this article",
    "in conclusion",
    "it goes without saying",
    "it is worth noting",
]

WORD_COUNT_RANGES = {
    "artist bio": (800, 1200),
    "song story": (600, 900),
    "genre hub": (1200, 1800),
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
    return None


def strip_tags(fragment):
    fragment = re.sub(r"<script.*?</script>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<style.*?</style>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return htmllib.unescape(fragment)


def body_text(text):
    # word count / banned-phrase checks apply to the article copy itself,
    # not header/nav/footer chrome, so prefer .article-body when present
    m = re.search(r'class="article-body"[^>]*>(.*)', text, flags=re.S | re.I)
    if m:
        # cut off at the closing </article> so trailing nav/footer isn't counted
        chunk = m.group(1)
        end = re.search(r"</article>", chunk, flags=re.I)
        if end:
            chunk = chunk[:end.start()]
        body = chunk
    else:
        m2 = re.search(r"<body[^>]*>(.*)</body>", text, flags=re.S | re.I)
        body = m2.group(1) if m2 else text
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    return strip_tags(body)


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9']+", text))


def check_em_dashes(text, errors):
    body = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    if EM_DASH in body:
        errors.append("em dash (—) found in file")
    if EN_DASH in body:
        errors.append("en dash (–) found in file")


def check_faq(text, errors):
    dt_count = len(re.findall(r"<dt\b", text, flags=re.I))
    faq_schema_q = 0
    for m in re.finditer(r'"@type"\s*:\s*"FAQPage".*?"mainEntity"\s*:\s*\[(.*?)\]\s*\}', text, flags=re.S):
        faq_schema_q = len(re.findall(r'"@type"\s*:\s*"Question"', m.group(1)))
    count = max(dt_count, faq_schema_q)
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
            errors.append(f'banned phrase found: "{phrase}"')


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


def check_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    page_type = detect_type(text, path)
    plain = body_text(text)
    wc = word_count(plain)

    errors = []
    check_em_dashes(text, errors)
    check_faq(text, errors)
    check_toc(text, errors, wc)
    check_images(text, errors)
    check_youtube(text, errors, page_type)
    check_word_count(wc, errors, page_type)
    check_banned_phrases(plain, errors)
    check_one_sentence_per_line(text, errors)
    check_template_placeholders(text, errors)

    return page_type, wc, errors


def main(argv):
    if not argv:
        print("usage: python3 gen/check_article.py <path-to-index.html> [...]")
        return 2
    failed = False
    for path in argv:
        page_type, wc, errors = check_file(path)
        print(f"{path}  [{page_type or 'unknown type'}, {wc} words]")
        if errors:
            failed = True
            for e in errors:
                print(f"  FAIL: {e}")
        else:
            print("  PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
