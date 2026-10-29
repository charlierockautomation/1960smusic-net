# Singles table component (artist bios)

Playable, sortable, scrollable "Key singles and Hot 100 peaks" table. First
used on `/blog/artists/the-four-seasons/` (2026-10-29). It extends the
year-page player (`assets/js/playlist-player.js`, `-ui.js`, `playlist-table.js`,
`assets/css/playlist-player.css`); there is no second player system.

## Behavior
- Each row has a Play button. Row click also plays. YouTube loads only on first
  play; nothing but the page's own embed loads on page view.
- Playback uses the shared sticky bottom bar (visible, never covered, full
  YouTube controls). Next/Prev follow the table's current sort order.
- Sorting re-orders the real `<tr>`s. The playing song keeps playing and the
  playlist order updates (`PlaylistPlayer.reorder`).
- Box is `.pp-table-scroll` (max-height 480px, 60vh under 640px), sticky header,
  no horizontal page scroll at 320px.

## Markup (copy from `docs/article-template.html`)
- Visible caption: `<p class="pp-caption" aria-hidden="true">` ABOVE the scroll
  box. The real `<caption class="pp-sr-only">` inside the table repeats the same
  text, so the sticky header can never cover it. One sentence only (the
  one-sentence-per-line gate); put the "press Play" hint in the prose above.
- `<table id="pp-table-<slug>" class="pp-table" data-pp-playlist-id="artist-<slug>" data-pp-sortable>`.
- Header: first `<th>` holds `<span class="pp-sr-only">Play</span>`; sortable
  columns are `<th aria-sort="none"><button type="button" class="pp-sort" data-pp-sort="text|num">`.
- Row: `<tr data-pp-yt="<youtube id>" data-pp-title data-pp-artist data-pp-yr>`
  with first cell `<button type="button" class="pp-play-btn" aria-label="Play <title>">&#9654; Play</button>`.
- Numeric text needs a key: `<td data-pp-sortkey="1">No. 1</td>` so No. 1 sorts
  before No. 13. Never use a bare `data-year`/`data-title` (site.js collision).
- Page includes: `/assets/css/playlist-player.css` in `<head>`; before
  `/site.js`: `playlist-player.js`, `playlist-player-ui.js`, `playlist-table.js`.

## YouTube IDs
Official uploads first (Rhino "Official Audio", artist channel, VEVO), then
"Artist - Topic". Find with `gen/generate.py` `yt_search_ids` + `oembed`, verify
embeddable with `gen/yt_video_status.py` `check_and_record`. List every id with
its channel when presenting the page.

## Updated dates
Adding Play buttons or sorting to an existing table is plumbing: no Updated or
`dateModified` bump.

## Song-story links
When a song story is published for any song in an artist's singles table, link that table row to it in the same push.

## Mixed singles/album tables
- Album row plays the album's best-known track, and the bar shows that track's title (`data-pp-title`); put the album in the `aria-label`.
- A table never repeats a `data-pp-yt` id (highlight and seek key on it), so if the album's hit is already a row, use its next best-known track.
- `check_article.py` leaves Play/sort buttons and the `.pp-caption` duplicate out of the word count.
