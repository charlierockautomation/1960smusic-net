/* 1960smusic.net — shared tool helpers (Phase 1)
   Pure client-side. Reads the existing /data/*.json files. No backend. */

const DATA = { songs: null, genres: null, artists: null };

/* ---- data loading ---- */
async function loadData() {
  if (DATA.songs) return DATA;
  const [songs, genres, artists] = await Promise.all([
    fetch('/data/songs.json').then(r => r.json()),
    fetch('/data/genres.json').then(r => r.json()),
    fetch('/data/artists.json').then(r => r.json()),
  ]);
  DATA.songs = songs;
  DATA.genres = genres;
  DATA.artists = artists;
  return DATA;
}

/* ---- generic helpers ---- */
function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function randomPick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}
function genreName(id) {
  const g = (DATA.genres || []).find(x => x.id === id);
  return g ? g.name : id;
}
function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/* ---- YouTube embed (uses the verified id + recognizable hook start) ---- */
function ytEmbed(song, opts) {
  const o = opts || {};
  const start = Number.isFinite(song.youtube_clip_start_seconds) ? song.youtube_clip_start_seconds : 0;
  const src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(song.youtube_id) +
              (start > 0 ? ('?start=' + start) : '');
  return '<div class="embed">' +
    '<iframe loading="lazy" src="' + src + '" title="' + escapeHtml(song.title) + '" ' +
    'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" ' +
    'allowfullscreen></iframe></div>';
}

/* ---- a compact song "meta" line: Artist · Year · Genre ---- */
function songMeta(song) {
  return escapeHtml(song.artist_name || '') + ' &middot; ' + escapeHtml(String(song.year)) +
    ' &middot; ' + escapeHtml(genreName(song.genre_id));
}
