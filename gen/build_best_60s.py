# Builds best-60s-songs/index.html from data/songs.json + curated picks/why-lines.
import json, html, os, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
E = lambda s: html.escape(s, quote=True)

songs = {s["id"]: s for s in json.load(open(f"{ROOT}/data/songs.json"))}

GENRES = {
    "british-invasion": "British Invasion",
    "motown-soul": "Motown, Soul & R&B",
    "folk-rock": "Folk Rock",
    "psychedelic-rock": "Psychedelic Rock",
    "garage-surf-rock": "Garage & Surf Rock",
    "country-60s": "Country",
    "pop-brill-building": "Pop & Brill Building",
    "jazz-easy-listening": "Jazz & Easy Listening",
}

# (song id, why-it-matters line). Order here is irrelevant; table sorts by year then this order.
PICKS = [
 ("hell-have-to-go-jim-reeves", "Jim Reeves's warm, close-miked baritone turned a country record into a crossover hit."),
 ("walk-dont-run-ventures", "The Ventures adapted a Johnny Smith jazz guitar piece and helped make the guitar instrumental a pop staple."),
 ("will-you-love-me-tomorrow-shirelles", "The first US No. 1 by an all-Black girl group, written by Gerry Goffin and Carole King."),
 ("crazy-patsy-cline", "Written by a young Willie Nelson, it became one of the definitive Nashville Sound recordings."),
 ("i-fall-to-pieces-patsy-cline", "Patsy Cline's first US country No. 1, co-written by Hank Cochran and Harlan Howard."),
 ("moon-river-henry-mancini", "Mancini's theme from Breakfast at Tiffany's won the Academy Award for Best Original Song."),
 ("please-mr-postman-marvelettes", "Motown's first No. 1 single on the US pop chart, later covered by The Beatles and The Carpenters."),
 ("big-girls-dont-cry-four-seasons", "The Four Seasons followed their breakthrough Sherry with a second US No. 1."),
 ("i-left-my-heart-in-san-francisco-tony-bennett", "It became Tony Bennett's signature song and won him two Grammy Awards in 1963."),
 ("if-i-had-a-hammer-peter-paul-and-mary", "Pete Seeger and Lee Hays wrote it, and the trio's version won two Grammy Awards."),
 ("miserlou-dick-dale", "Dick Dale adapted an Eastern Mediterranean folk melody with rapid staccato picking."),
 ("sherry-four-seasons", "The Four Seasons' first US No. 1, written by band member Bob Gaudio."),
 ("surfin-safari-beach-boys", "The Beach Boys' first national hit single, part of the early surf-music craze."),
 ("she-loves-you-beatles", "Its yeah, yeah, yeah refrain became shorthand for Beatlemania."),
 ("i-want-to-hold-your-hand-beatles", "The Beatles' first US No. 1, and the song that triggered the American British Invasion."),
 ("please-please-me-beatles", "Producer George Martin suggested speeding up what began as a slower ballad."),
 ("glad-all-over-dave-clark-five", "It knocked The Beatles' I Want to Hold Your Hand off the top of the UK chart."),
 ("be-my-baby-ronettes", "Its opening drum figure is one of pop's most imitated, a landmark of Phil Spector's Wall of Sound."),
 ("blowin-in-the-wind-bob-dylan", "It became a civil-rights anthem, though Peter, Paul and Mary's cover sold even more."),
 ("fingertips-pt-2-stevie-wonder", "This live recording made 13-year-old Stevie Wonder the youngest artist to top the US chart."),
 ("heat-wave-martha-and-the-vandellas", "An early smash for the Holland-Dozier-Holland writing team, with a driving beat that shaped Motown."),
 ("louie-louie-kingsmen", "Its slurred vocals prompted a two-year FBI obscenity investigation that found nothing."),
 ("ring-of-fire-johnny-cash", "Mariachi-style trumpets were a bold touch for a country record, and June Carter co-wrote it."),
 ("surf-city-jan-and-dean", "The first surf song to reach US No. 1, co-written by Brian Wilson."),
 ("surfin-usa-beach-boys", "The melody comes from Chuck Berry's Sweet Little Sixteen, which later earned Berry a co-writing credit."),
 ("wipe-out-surfaris", "Its cackling intro and drum solo made it a rite of passage for young drummers."),
 ("baby-love-supremes", "The Supremes' second of five straight US No. 1 hits also topped the UK chart."),
 ("where-did-our-love-go-supremes", "The Supremes' first US No. 1 single."),
 ("house-of-the-rising-sun-animals", "At full single length, it broke the era's convention of keeping songs under three minutes."),
 ("you-really-got-me-kinks", "Its distorted power chords are often cited as a blueprint for hard rock and heavy metal."),
 ("bits-and-pieces-dave-clark-five", "Its thunderous stomping beat reportedly damaged dance-hall floors."),
 ("because-dave-clark-five", "A ballad that reached the US Top 3 and showed the group's softer side."),
 ("needles-and-pins-searchers", "Its chiming twelve-string guitar sound influenced folk-rock acts like The Byrds."),
 ("do-wah-diddy-diddy-manfred-mann", "It topped the charts on both sides of the Atlantic, written by Jeff Barry and Ellie Greenwich."),
 ("downtown-petula-clark", "It made Petula Clark the first British female artist to top the US chart in the rock era."),
 ("fly-me-to-the-moon-frank-sinatra", "Quincy Jones arranged this Count Basie-backed version, later tied to the Apollo Moon missions."),
 ("dancing-in-the-street-martha-and-the-vandellas", "Marvin Gaye co-wrote it, and some later read it as an anthem of the era's social unrest."),
 ("i-cant-get-no-satisfaction-rolling-stones", "Keith Richards wrote the fuzz-guitar riff in his sleep, and it gave the Stones their first US No. 1."),
 ("for-your-love-yardbirds", "A harpsichord was unusual on a rock single, and its success reportedly prompted Eric Clapton to quit the band."),
 ("heart-full-of-soul-yardbirds", "Jeff Beck's fuzz-guitar line was originally meant to be played on a sitar."),
 ("mrs-brown-youve-got-a-lovely-daughter-hermanns-hermits", "It hit No. 1 in the US but was not at first released as a single in the UK."),
 ("im-henry-the-viii-i-am-hermanns-hermits", "A US No. 1 that adapts a British music-hall number from 1910."),
 ("my-generation-who", "Its line Hope I die before I get old became a mod-generation rallying cry."),
 ("like-a-rolling-stone-bob-dylan", "Its six-minute length broke the radio conventions of the era."),
 ("mr-tambourine-man-byrds", "The Byrds' chiming twelve-string cover of a Bob Dylan song helped launch folk rock."),
 ("the-sound-of-silence-simon-and-garfunkel", "The hit version came when a producer overdubbed electric instruments without the duo's knowledge."),
 ("my-girl-temptations", "The Temptations' first US No. 1, written by Smokey Robinson and Ronald White, with David Ruffin on lead."),
 ("stop-in-the-name-of-love-supremes", "Its stop hand gesture became part of the group's stage act."),
 ("i-got-you-i-feel-good-james-brown", "Its opening scream is among the most recognizable in soul music."),
 ("california-girls-beach-boys", "Brian Wilson said he wrote the sweeping intro after first trying LSD."),
 ("king-of-the-road-roger-miller", "It won multiple Grammy Awards in 1966, and its finger-snapping arrangement crossed over to pop."),
 ("wooly-bully-sam-the-sham-and-the-pharaohs", "Billboard named it the top record of 1965 even though it never reached No. 1."),
 ("good-vibrations-beach-boys", "Brian Wilson called it a pocket symphony assembled from many recording sessions."),
 ("paint-it-black-rolling-stones", "Brian Jones's sitar made it one of the first US No. 1 hits to feature the instrument prominently."),
 ("sunny-afternoon-kinks", "Ray Davies wrote it as a satire of the wealthy amid Britain's high taxation, and it reached UK No. 1."),
 ("over-under-sideways-down-yardbirds", "Its swirling guitar riff was influenced by Middle Eastern scales."),
 ("california-dreamin-mamas-and-the-papas", "John and Michelle Phillips wrote it while missing California from wintry New York."),
 ("eight-miles-high-byrds", "Its guitar work was influenced by John Coltrane, and it is often cited as an early psychedelic rock recording."),
 ("wild-thing-troggs", "It topped the US chart with a famously simple structure and an ocarina solo."),
 ("96-tears-question-mark-and-the-mysterians", "Its cheap combo-organ riff is a garage-rock landmark that topped the US chart."),
 ("im-a-believer-monkees", "Neil Diamond wrote it, and it became one of the biggest-selling singles of the 1960s."),
 ("last-train-to-clarksville-monkees", "The Monkees' debut single and first US No. 1."),
 ("you-keep-me-hangin-on-supremes", "Its Morse-code-like guitar intro is instantly recognizable."),
 ("reach-out-ill-be-there-four-tops", "It topped the charts in both the US and UK, with an urgent lead from Levi Stubbs."),
 ("strangers-in-the-night-frank-sinatra", "It won multiple Grammy Awards in 1967, though Sinatra reportedly disliked it."),
 ("light-my-fire-doors", "The Doors trimmed its long organ and guitar solos for the hit single, their first US No. 1."),
 ("the-end-doors", "Francis Ford Coppola used it to open and close Apocalypse Now."),
 ("strange-days-doors", "A Moog synthesizer, then a very new instrument, processes Jim Morrison's vocal."),
 ("waterloo-sunset-kinks", "Ray Davies pictures two lovers meeting by the River Thames in London."),
 ("respect-aretha-franklin", "Aretha Franklin transformed Otis Redding's original and added the spelled-out R-E-S-P-E-C-T hook."),
 ("purple-haze-jimi-hendrix-experience", "It opens with the dissonant Hendrix chord, a dominant 7#9."),
 ("white-rabbit-jefferson-airplane", "Grace Slick drew its imagery from Alice in Wonderland and built a bolero-style crescendo."),
 ("somebody-to-love-jefferson-airplane", "Darby Slick wrote it and first recorded it with his band The Great Society."),
 ("strawberry-fields-forever-beatles", "The final version splices two takes recorded in different keys and tempos."),
 ("sunshine-of-your-love-cream", "Its descending guitar riff is one of rock's most recognizable."),
 ("happy-together-turtles", "It knocked The Beatles' Penny Lane off the top of the US chart."),
 ("brown-eyed-girl-van-morrison", "Van Morrison's first solo hit remains one of the most-played songs on US radio."),
 ("daydream-believer-monkees", "John Stewart of the Kingston Trio wrote it, and it was The Monkees' last US No. 1."),
 ("lucy-in-the-sky-with-diamonds-beatles", "John Lennon said the title came from a drawing by his young son Julian."),
 ("i-heard-it-through-the-grapevine-marvin-gaye", "Gaye's version spent seven weeks at US No. 1, a year after a hit version by Gladys Knight & the Pips."),
 ("wichita-lineman-glen-campbell", "Jimmy Webb wrote it and left one line unfinished, which Campbell kept."),
 ("stand-by-your-man-tammy-wynette", "Wynette co-wrote it with producer Billy Sherrill, and it became one of the best-selling country singles by a woman."),
 ("in-a-gadda-da-vida-iron-butterfly", "The full album version runs over 17 minutes, including an extended drum solo."),
 ("do-you-know-the-way-to-san-jose-dionne-warwick", "It won Dionne Warwick her first Grammy Award."),
 ("my-way-frank-sinatra", "Paul Anka wrote the English lyric to a French melody."),
 ("okie-from-muskogee-merle-haggard", "It became an anthem amid the cultural divisions of the late 1960s."),
 ("sugar-sugar-archies", "Studio musicians performed it for the cartoon band, and it was Billboard's No. 1 single of 1969."),
 ("the-boxer-simon-and-garfunkel", "Its lie-la-lie chorus was recorded partly in an echoing elevator shaft."),
 ("the-twist-chubby-checker", "It topped the US chart in 1960 and again in 1962, and launched a national dance craze."),
 ("only-the-lonely-roy-orbison", "Roy Orbison co-wrote this operatic ballad with Joe Melson, and it reached No. 1 in the UK."),
 ("runaway-del-shannon", "Max Crook's Musitron keyboard solo helped it top the US chart in 1961."),
 ("hit-the-road-jack-ray-charles", "Percy Mayfield wrote it, and it topped the US pop chart for Ray Charles in 1961."),
 ("i-get-around-beach-boys", "The Beach Boys' first US No. 1 single."),
 ("oh-pretty-woman-roy-orbison", "Roy Orbison co-wrote it with Bill Dees, and it reached No. 1 in both the US and the UK."),
 ("when-a-man-loves-a-woman-percy-sledge", "Percy Sledge's debut hit topped both the US pop and R&B charts in 1966."),
 ("these-boots-are-made-for-walkin-nancy-sinatra", "Lee Hazlewood wrote it, and it reached No. 1 on the US chart in early 1966."),
 ("hey-jude-beatles", "It spent nine weeks at No. 1 on the Billboard Hot 100 and ran far longer than the typical single."),
 ("mrs-robinson-simon-and-garfunkel", "Featured in the film The Graduate, it won the 1969 Grammy Award for Record of the Year."),
 ("sittin-on-the-dock-of-the-bay-otis-redding", "Recorded days before Otis Redding's death, it became the first posthumous No. 1 on the US chart."),
 ("get-back-beatles", "The only Beatles single credited to another artist, keyboardist Billy Preston."),]
assert len(PICKS) == 100, len(PICKS)
assert len({p[0] for p in PICKS}) == 100
order = {p[0]: i for i, p in enumerate(PICKS)}
rows = sorted((songs[i] for i, _ in PICKS), key=lambda s: (s["year"], order[s["id"]]))
why = dict(PICKS)

stories = {s["id"] for s in rows if os.path.isdir(f"{ROOT}/blog/songs/{s['id']}")}
yt_cache = json.load(open(f"{ROOT}/gen/yt_status_cache.json"))
for s in rows:
    st = yt_cache[s["youtube_id"]]
    assert st["embeddable"] and not st["made_for_kids"], s["id"]

by_year = collections.Counter(s["year"] for s in rows)
by_genre = collections.Counter(s["genre_id"] for s in rows)
year_top = {}
for y in range(1960, 1970):
    c = collections.Counter(s["genre_id"] for s in rows if s["year"] == y)
    year_top[y] = c.most_common()

# ---- table rows
tr = []
for n, s in enumerate(rows, 1):
    t, a = E(s["title"]), E(s["artist_name"])
    g = s["genre_id"]
    story = (f'<a href="/blog/songs/{s["id"]}/">Read the story</a>' if s["id"] in stories else "")
    tr.append(f'''            <tr data-pp-yt="{s["youtube_id"]}" data-pp-title="{t}" data-pp-artist="{a}" data-pp-yr="{s["year"]}" data-pp-genre="{g}">
              <td><button type="button" class="pp-play-cell" aria-label="Play {t}">{n}</button></td>
              <td>{t}</td><td>{a}</td><td>{s["year"]}</td>
              <td><a href="/blog/genres/{g}/">{E(GENRES[g])}</a></td>
              <td class="pp-why">{E(why[s["id"]])}</td><td>{story}</td>
            </tr>''')
table_rows = "\n".join(tr)

# ---- schema ItemList
items = ",\n".join(
    f'    {{"@type": "ListItem", "position": {n}, "item": {{"@type": "MusicRecording", "name": {json.dumps(s["title"])}, "byArtist": {{"@type": "MusicGroup", "name": {json.dumps(s["artist_name"])}}}, "datePublished": "{s["year"]}"}}}}'
    for n, s in enumerate(rows, 1))

# ---- by-year table
yrow = []
for y in range(1960, 1970):
    gid, cnt = year_top[y][0]
    yrow.append(f'            <tr><td>{y}</td><td>{by_year[y]}</td><td>{E(GENRES[gid])} ({cnt})</td><td><a href="/1960s/{y}/">{y} music guide</a></td></tr>')
year_rows = "\n".join(yrow)
top_year = max(by_year.items(), key=lambda kv: kv[1])
top_years = [y for y, c in by_year.items() if c == top_year[1]]

EXAMPLES = {
    "british-invasion": "She Loves You and Paint It Black",
    "motown-soul": "My Girl and Respect",
    "folk-rock": "Mr. Tambourine Man and The Sound of Silence",
    "psychedelic-rock": "Purple Haze and White Rabbit",
    "garage-surf-rock": "Wipe Out and Wild Thing",
    "country-60s": "Ring of Fire and Wichita Lineman",
    "pop-brill-building": "Be My Baby and I'm a Believer",
    "jazz-easy-listening": "Moon River and Fly Me to the Moon",
}
for g, ex in EXAMPLES.items():  # examples must really be in the genre
    for t in ex.replace("'", "'").split(" and "):
        assert any(s["genre_id"] == g and s["title"].startswith(t.rstrip(".")) for s in rows), (g, t)
genre_li = "\n".join(
    f'        <li><a href="/blog/genres/{g}/">{E(GENRES[g])}</a>: {by_genre[g]} songs, including {E(EXAMPLES[g])}.</li>'
    for g in sorted(GENRES, key=lambda g: -by_genre[g]))

year_opts = "\n".join(f'          <option value="{y}">{y}</option>' for y in range(1960, 1970))
genre_opts = "\n".join(f'          <option value="{g}">{E(GENRES[g])}</option>' for g in GENRES)

top_genre_id, top_genre_n = by_genre.most_common(1)[0]
story_count = len(stories)

TITLE = "Best 60s Songs: 100 Playable Hits From 1960 to 1969"
DESC = "The best 60s songs: 100 playable hits from 1960 to 1969 across Motown, British Invasion, folk rock, surf and country, each with a why-it-matters line."
FAQ = [
 ("What are the best 60s songs?",
  [f"The best 60s songs on this page are 100 hits from 1960 to 1969, from She Loves You to Sugar, Sugar.",
   "They are listed by year, not ranked, and each one plays on the page."]),
 ("How many songs are on this list of 60s hits?",
  [f"There are 100 songs, with at least three from every year of the decade.",
   f"{story_count} of them link to a full song story on this site."]),
 ("Which year has the most songs on the list?",
  [f"{' and '.join(str(y) for y in top_years)} lead with {top_year[1]} songs each." if len(top_years) > 1 else f"{top_years[0]} leads with {top_year[1]} songs.",
   "Years such as 1960, 1961 and 1969 have fewer entries because the site's catalogue is thinner there."]),
 ("What genres do the best 60s songs cover?",
  ["The list spans eight genres: British Invasion, Motown and soul, folk rock, psychedelic rock, garage and surf rock, country, pop and Brill Building, and jazz and easy listening.",
   "Each genre links to its own hub page."]),
 ("Can I listen to these 60s songs on this page?",
  ["Yes, press play on any row, or use Play All to run the whole list.",
   "The year and genre filters let you play only the songs you choose."]),
]

page = f'''<!DOCTYPE html>
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
<title>{E(TITLE)}</title>
<meta name="description" content="{E(DESC)}">
<link rel="canonical" href="https://1960smusic.net/best-60s-songs/">
<meta property="og:type" content="article">
<meta property="og:title" content="{E(TITLE)}">
<meta property="og:description" content="{E(DESC)}">
<meta property="og:url" content="https://1960smusic.net/best-60s-songs/">
<meta property="og:image" content="https://1960smusic.net/1960s/1964/beatles-1964.jpg">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#3D2B1F">
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/assets/css/playlist-player.css">
<!-- FOCUS KEYWORD: best 60s songs -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {json.dumps(TITLE)},
  "description": {json.dumps(DESC)},
  "image": "https://1960smusic.net/1960s/1964/beatles-1964.jpg",
  "author": {{"@type": "Person", "name": "Charlie Gillingham", "url": "https://1960smusic.net/about/charlie/"}},
  "publisher": {{
    "@type": "Organization",
    "name": "1960smusic.net",
    "logo": {{"@type": "ImageObject", "url": "https://1960smusic.net/android-chrome-512x512.png"}}
  }},
  "datePublished": "2026-10-08",
  "dateModified": "2026-10-08",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://1960smusic.net/best-60s-songs/"}},
  "about": {{"@type": "Thing", "@id": "https://1960smusic.net/best-60s-songs/#subject", "name": "Best 60s songs"}},
  "keywords": "best 60s songs, 60s songs, 60s music hits, 1960s songs"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "@id": "https://1960smusic.net/best-60s-songs/#tracklist",
  "name": "Best 60s songs, 100 playable hits from 1960 to 1969",
  "itemListElement": [
{items}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://1960smusic.net/"}},
    {{"@type": "ListItem", "position": 2, "name": "Best 60s Songs", "item": "https://1960smusic.net/best-60s-songs/"}}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{(","+chr(10)).join('    {"@type": "Question", "name": '+json.dumps(q)+', "acceptedAnswer": {"@type": "Answer", "text": '+json.dumps(" ".join(a))+'}}' for q,a in FAQ)}
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
      <a href="/">Home</a> &rsaquo; <span aria-current="page">Best 60s Songs</span>
    </nav>

    <header class="article-header">
      <h1>{E(TITLE)}</h1>
      <p class="byline">By <a href="/about/charlie/">Charlie Gillingham</a> <span aria-hidden="true">&middot;</span> Published <time datetime="2026-10-08">October 8, 2026</time> <span aria-hidden="true">&middot;</span> Updated <time datetime="2026-10-08">October 8, 2026</time></p>
    </header>

    <div class="article-body">
      <p class="lead">The best 60s songs span Beatlemania, Motown, surf, folk rock and psychedelia, and 100 of them play right here.<br>
      Press play on any row, or filter by year or genre and play only what you see.<br>
      Every song carries a one-line reason it matters, and some link to a full story.</p>

      <h2 id="listen">Listen to the Best 60s Songs</h2>
      <p>These <span data-pp-count data-pp-table="pp-table-best">100</span> hits run in order from 1960 to 1969.<br>
      Search by title or artist, pick a year or genre, or use Play All to run what is showing.</p>
      <div class="pp-controls">
        <button type="button" class="pp-playall" data-pp-playall data-pp-table="pp-table-best">Play All</button>
        <button type="button" class="pp-shuffle" data-pp-shuffle data-pp-table="pp-table-best">Shuffle</button>
        <input type="search" class="pp-search" data-pp-search data-pp-table="pp-table-best" placeholder="Search title or artist" aria-label="Search the 60s songs list">
        <select class="pp-filter" data-pp-filter="year" data-pp-table="pp-table-best" aria-label="Filter by year">
          <option value="">All years</option>
{year_opts}
        </select>
        <select class="pp-filter" data-pp-filter="genre" data-pp-table="pp-table-best" aria-label="Filter by genre">
          <option value="">All genres</option>
{genre_opts}
        </select>
      </div>
      <p class="pp-filter-status" data-pp-filter-status data-pp-table="pp-table-best" aria-live="polite">Showing 100 of 100 songs</p>
      <div class="table-scroll pp-table-scroll">
        <table id="pp-table-best" class="pp-table" data-pp-playlist-id="best-60s-songs" data-pp-visible-only>
          <caption>Best 60s songs, 100 hits from 1960 to 1969 with a why-it-matters line</caption>
          <thead>
            <tr><th>#</th><th>Title</th><th>Artist</th><th>Year</th><th>Genre</th><th>Why it matters</th><th>Story</th></tr>
          </thead>
          <tbody>
{table_rows}
          </tbody>
        </table>
        <div class="pp-table-fade" aria-hidden="true"></div>
      </div>

      <figure class="featured-image">
        <img src="/1960s/1964/beatles-1964.jpg" alt="The Beatles performing on stage at the Washington Coliseum in February 1964, during their first American tour" width="1000" height="655">
        <figcaption>The Beatles at the Washington Coliseum, February 11, 1964. Photo: Marion S. Trikosko, Library of Congress. Public domain, via <a href="https://commons.wikimedia.org/wiki/File:Beatles_Washington_Coliseum.jpg" target="_blank" rel="noopener">Wikimedia Commons</a>.</figcaption>
      </figure>

      <h2 id="table-of-contents">Table of Contents</h2>
      <ul>
        <li><a href="#listen">Listen to the Best 60s Songs</a></li>
        <li><a href="#how-we-picked">How We Picked These 60s Songs</a></li>
        <li><a href="#by-year">Best 60s Songs by Year</a></li>
        <li><a href="#by-genre">Best 60s Songs by Genre</a></li>
        <li><a href="#sound">What Set 60s Songs Apart</a></li>
        <li><a href="#play-along">Play Along With 60s Music</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>

      <hr>

      <h2 id="how-we-picked">How We Picked These 60s Songs</h2>
      <p>This list is not a ranking.<br>
      The 100 songs come from this site's own catalogue of {len(songs)} songs, chosen so every year from 1960 to 1969 and all eight genre hubs appear.<br>
      The thinnest years carry fewer entries because the catalogue is lighter there: 1960 has {by_year[1960]} songs, 1961 has {by_year[1961]} and 1969 has {by_year[1969]}.<br>
      Each song plays from a YouTube upload checked as embeddable and not made for kids.<br>
      Each why-it-matters line draws on the song's entry in the catalogue.<br>
      {story_count} songs link to a full story with the history behind the record.</p>

      <hr>

      <h2 id="by-year">Best 60s Songs by Year</h2>
      <p>The list leans toward the middle of the decade.<br>
      {' and '.join(str(y) for y in top_years)} {'lead' if len(top_years) > 1 else 'leads'} with {top_year[1]} songs {'each' if len(top_years) > 1 else ''}, and each year links to its own guide with the Billboard number ones.</p>
      <div class="table-scroll">
        <table>
          <caption>Songs per year on the best 60s songs list</caption>
          <thead>
            <tr><th>Year</th><th>Songs</th><th>Top genre (songs)</th><th>Year guide</th></tr>
          </thead>
          <tbody>
{year_rows}
          </tbody>
        </table>
      </div>

      <hr>

      <h2 id="by-genre">Best 60s Songs by Genre</h2>
      <p>{GENRES[top_genre_id]} is the biggest genre here, with {top_genre_n} songs.<br>
      Every genre links to a hub with the artists and stories behind it.</p>
      <ul>
{genre_li}
      </ul>

      <hr>

      <h2 id="sound">What Set 60s Songs Apart</h2>
      <h3>Records Grew Longer and Stranger</h3>
      <p>The Animals' <a href="/blog/songs/house-of-the-rising-sun-animals/">House of the Rising Sun</a> broke the habit of keeping singles under three minutes.<br>
      Bob Dylan's Like a Rolling Stone ran six minutes, and the album cut of In-A-Gadda-Da-Vida passes 17.<br>
      The Beach Boys built <a href="/blog/songs/good-vibrations-beach-boys/">Good Vibrations</a> from many recording sessions.</p>
      <h3>New Sounds Entered Pop</h3>
      <p>Brian Jones played sitar on <a href="/blog/songs/paint-it-black-rolling-stones/">Paint It Black</a>.<br>
      The Yardbirds put a harpsichord on a rock single in For Your Love.<br>
      The Doors used a Moog synthesizer on Strange Days, when the instrument was still new.</p>
      <h3>Songs Carried the Moment</h3>
      <p>Dylan's Blowin' in the Wind became a civil-rights anthem.<br>
      Aretha Franklin's Respect added the spelled-out hook that Otis Redding's original lacked.<br>
      Merle Haggard's Okie from Muskogee became an anthem amid the cultural divisions of the late decade.</p>

      <hr>

      <h2 id="play-along">Play Along With 60s Music</h2>
      <p>The <a href="/tools/radio/">Radio Dial</a> tunes eight genre stations with songs from across the decade.<br>
      Test what you know with the <a href="/tools/trivia/">60s music trivia</a> or the <a href="/tools/daily/">daily guessing game</a>.<br>
      For the chart story behind each season, start at the <a href="/1960s/">1960s year-by-year hub</a>.</p>

      <hr>

      <h2 id="faq">FAQ</h2>

{chr(10).join(f"""      <details{' open' if i == 0 else ''}>
        <summary>{E(q)}</summary>
        <div class="answer">{''.join('<p>'+E(x)+'</p>' for x in a)}</div>
      </details>""" for i, (q, a) in enumerate(FAQ))}

      <hr>

      <p>The best 60s songs still sound alive because each one marks a turn in how pop was made.<br>
      Pick a year from the hub above and keep listening.<br>
      Come back to the <a href="/">1960smusic.net homepage</a> for more stories from the decade.</p>
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

<script src="/assets/js/playlist-player.js"></script>
<script src="/assets/js/playlist-player-ui.js"></script>
<script src="/assets/js/playlist-table.js"></script>
<script src="/site.js" defer></script>
</body>
</html>
'''
assert min(by_year.values()) >= 3
open(f"{ROOT}/best-60s-songs/index.html", "w").write(page)
print("ok", len(rows), "stories", story_count, dict(by_year), by_genre.most_common())
