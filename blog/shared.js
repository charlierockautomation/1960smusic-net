/* 1960smusic.net — shared blog index helpers.
   Pure client-side. Reads /data/posts.json. No backend.
   Adding a new published article only ever requires one new entry in
   posts.json; the blog index and every category archive page pick it
   up automatically through this file. */

const TYPE_LABELS = {
  'genre-hub': 'Genre Hub',
  'artist-bio': 'Artist Bio',
  'song-story': 'Song Story',
  'trending': 'Trending',
  'on-this-day': 'On This Day',
};

const TYPE_SECTION_TITLES = {
  'genre-hub': 'Genre Hubs',
  'artist-bio': 'Artist Bios',
  'song-story': 'Song Stories',
  'trending': 'Trending',
  'on-this-day': 'On This Day',
};

const TYPE_ARCHIVES = {
  'genre-hub': '/blog/genres/',
  'artist-bio': '/blog/artists/',
  'song-story': '/blog/songs/',
  'trending': '/blog/trending/',
  'on-this-day': '/blog/on-this-day/',
};

const TYPE_ORDER = ['genre-hub', 'artist-bio', 'song-story', 'trending', 'on-this-day'];

let _posts = null;
async function loadPosts() {
  if (_posts) return _posts;
  const res = await fetch('/data/posts.json');
  const data = await res.json();
  _posts = data.posts || [];
  return _posts;
}

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function formatDate(iso) {
  const d = new Date(iso + 'T00:00:00Z');
  if (isNaN(d)) return iso;
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
}

function byDateDesc(a, b) {
  return a.date < b.date ? 1 : a.date > b.date ? -1 : 0;
}

/* on-this-day posts often share a publish date (several built same day),
   so byDateDesc alone can't tell them apart. `seq` is the queue row number
   from docs/on-this-day-build.md, which is strictly calendar-ordered, so it
   breaks ties correctly. Falls back to byDateDesc if seq is ever missing. */
function byOtdDesc(a, b) {
  if (typeof a.seq === 'number' && typeof b.seq === 'number') return b.seq - a.seq;
  return byDateDesc(a, b);
}

/* renders one post as a .genre-card (existing site card style, reused as-is) */
function postCardHtml(post) {
  const label = TYPE_LABELS[post.type] || post.type;
  return '<a class="genre-card" href="' + escapeHtml(post.slug) + '">' +
    '<span class="freq">' + escapeHtml(label) + ' &middot; ' + escapeHtml(formatDate(post.date)) + '</span>' +
    '<h3>' + escapeHtml(post.title) + '</h3>' +
    '<p class="sound">' + escapeHtml(post.description) + '</p>' +
  '</a>';
}

/* ---- blog index: up to `limit` most recent posts per type, all 5 sections ---- */
async function renderBlogIndex(limit) {
  const posts = await loadPosts();
  TYPE_ORDER.forEach(function (type) {
    const grid = document.getElementById('posts-' + type);
    const seeAll = document.getElementById('seeall-' + type);
    if (!grid) return;
    const ofType = posts.filter(function (p) { return p.type === type; }).sort(type === 'on-this-day' ? byOtdDesc : byDateDesc);
    if (!ofType.length) {
      grid.outerHTML = '<p class="sub">New ' + TYPE_SECTION_TITLES[type].toLowerCase() + ' coming soon.</p>';
      if (seeAll) seeAll.hidden = true;
      return;
    }
    grid.innerHTML = ofType.slice(0, limit).map(postCardHtml).join('');
    if (seeAll) seeAll.href = TYPE_ARCHIVES[type];
  });
}

/* ---- category archive page: every post of one type, newest first ---- */
async function renderArchive(type) {
  const posts = await loadPosts();
  const grid = document.getElementById('archive-grid');
  const ofType = posts.filter(function (p) { return p.type === type; }).sort(type === 'on-this-day' ? byOtdDesc : byDateDesc);
  if (!ofType.length) {
    grid.outerHTML = '<p class="sub">Nothing published in this section yet. Check back soon.</p>';
    return;
  }
  grid.innerHTML = ofType.map(postCardHtml).join('');
}
