# -*- coding: utf-8 -*-
"""Key years each genre hub must link to (/1960s/<year>/), enforced by
gen/check_seo.py.

Set by Charlie 2026-10-08. Edit a list if a hub's story shifts; check_article.py FAILs a hub that
is missing from this dict or does not link every year listed here.
"""

PEAK_YEARS = {
    "60s-rock": [1964, 1965, 1967],
    "british-invasion": [1964, 1965],
    "country-60s": [1961, 1963, 1965],
    "folk-rock": [1965, 1966],
    "garage-surf-rock": [1963, 1965, 1966],
    "jazz-easy-listening": [1962, 1964],
    "motown-soul": [1964, 1965, 1966],
    "pop-brill-building": [1962, 1963, 1964],
    "psychedelic-rock": [1966, 1967, 1968],
}
