/* 1960smusic.net -- wires a static, crawlable <table data-pp-playlist-id>
   to PlaylistPlayer (see playlist-player.js). Reads songs straight off the
   table's own <tr data-pp-yt> rows, so the HTML stays the single source of
   truth. Every attribute here is namespaced data-pp-* so it can never
   collide with a site-wide selector like site.js's [data-year] (which
   overwrites textContent for the footer's copyright year, and once wiped
   out a tracklist row that used a plain data-year attribute). Each table
   needs a matching .pp-controls block (Play All / Shuffle / search) with
   buttons/input carrying data-pp-table="<table id>". */

(function(){
  function readSongs(table){
    return Array.prototype.map.call(table.querySelectorAll('tbody tr[data-pp-yt]'), function(tr){
      return {
        youtube_id: tr.getAttribute('data-pp-yt'),
        title: tr.getAttribute('data-pp-title') || '',
        artist: tr.getAttribute('data-pp-artist') || '',
        year: tr.getAttribute('data-pp-yr') || ''
      };
    });
  }

  function shuffle(list){
    var out = list.slice();
    for (var i = out.length - 1; i > 0; i--){
      var j = Math.floor(Math.random() * (i + 1));
      var t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  function setup(table){
    var songs = readSongs(table);
    var id = table.getAttribute('data-pp-playlist-id') || table.id;
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr[data-pp-yt]'));
    var scrollBox = table.closest('.pp-table-scroll');

    Array.prototype.forEach.call(document.querySelectorAll('[data-pp-count][data-pp-table="' + table.id + '"]'), function(el){
      el.textContent = songs.length;
    });

    // Scrolls the active row into view inside scrollBox only (scrollTop math,
    // never element.scrollIntoView(), so the page itself never jumps). The
    // sticky thead always covers the top headH px of the visible box, even
    // at scrollTop 0, so scrolling up has to land headH short of the row's
    // raw offsetTop or the row ends up hidden behind the sticky header.
    function scrollActiveIntoView(tr){
      if (!scrollBox) return;
      var thead = table.querySelector('thead');
      var headH = thead ? thead.offsetHeight : 0;
      var cTop = scrollBox.scrollTop, cBottom = cTop + scrollBox.clientHeight;
      var rTop = tr.offsetTop, rBottom = rTop + tr.offsetHeight;
      if (rTop - headH < cTop) scrollBox.scrollTop = Math.max(0, rTop - headH);
      else if (rBottom > cBottom) scrollBox.scrollTop = rBottom - scrollBox.clientHeight;
    }

    function highlight(){
      var s = PlaylistPlayer.getState();
      var activeId = PlaylistPlayer.isThisPlaylistActive(id) && s.song ? s.song.youtube_id : null;
      var activeTr = null;
      rows.forEach(function(tr){
        var isActive = !!activeId && tr.getAttribute('data-pp-yt') === activeId;
        tr.classList.toggle('pp-active', isActive);
        if (isActive) activeTr = tr;
      });
      if (activeTr) scrollActiveIntoView(activeTr);
    }
    document.addEventListener('pp:update', highlight);

    function playFrom(startYtId){
      var startIndex = songs.findIndex(function(s){ return s.youtube_id === startYtId; });
      if (PlaylistPlayer.isThisPlaylistActive(id)){
        PlaylistPlayer.seekTo(startIndex);
      } else {
        PlaylistPlayer.loadPlaylist(songs, startIndex, id);
      }
    }

    table.addEventListener('click', function(e){
      if (e.target.closest('a')) return;
      var tr = e.target.closest('tr[data-pp-yt]');
      if (!tr) return;
      playFrom(tr.getAttribute('data-pp-yt'));
    });

    // Opt-in: a table with data-pp-visible-only plays only the rows the
    // search box and year/genre filters leave showing (e.g. /best-60s-songs/).
    var visibleOnly = table.hasAttribute('data-pp-visible-only');
    function playable(){
      if (!visibleOnly) return songs;
      var out = [];
      rows.forEach(function(tr, i){ if (!tr.classList.contains('pp-hidden')) out.push(songs[i]); });
      return out;
    }

    function ctl(attr){
      return document.querySelectorAll('[' + attr + '][data-pp-table="' + table.id + '"]');
    }
    Array.prototype.forEach.call(ctl('data-pp-playall'), function(btn){
      btn.addEventListener('click', function(){
        var list = playable();
        if (list.length) PlaylistPlayer.loadPlaylist(list, 0, id);
      });
    });
    Array.prototype.forEach.call(ctl('data-pp-shuffle'), function(btn){
      btn.addEventListener('click', function(){
        var list = playable();
        if (list.length) PlaylistPlayer.loadPlaylist(shuffle(list), 0, id);
      });
    });

    var searchEls = ctl('data-pp-search');
    var filterEls = ctl('data-pp-filter');
    var statusEls = ctl('data-pp-filter-status');
    function applyFilters(){
      var q = searchEls.length ? searchEls[0].value.trim().toLowerCase() : '';
      var f = {};
      Array.prototype.forEach.call(filterEls, function(sel){ f[sel.getAttribute('data-pp-filter')] = sel.value; });
      var shown = 0;
      rows.forEach(function(tr){
        var hay = (tr.getAttribute('data-pp-title') + ' ' + tr.getAttribute('data-pp-artist')).toLowerCase();
        var hide = (q.length > 0 && hay.indexOf(q) === -1) ||
          (f.year && tr.getAttribute('data-pp-yr') !== f.year) ||
          (f.genre && tr.getAttribute('data-pp-genre') !== f.genre);
        tr.classList.toggle('pp-hidden', !!hide);
        if (!hide) shown++;
      });
      Array.prototype.forEach.call(statusEls, function(el){
        el.textContent = 'Showing ' + shown + ' of ' + rows.length + ' songs';
      });
      if (scrollBox) scrollBox.scrollTop = 0;
    }
    Array.prototype.forEach.call(searchEls, function(el){ el.addEventListener('input', applyFilters); });
    Array.prototype.forEach.call(filterEls, function(el){ el.addEventListener('change', applyFilters); });
  }

  document.addEventListener('DOMContentLoaded', function(){
    Array.prototype.forEach.call(document.querySelectorAll('table[data-pp-playlist-id]'), setup);
  });
})();
