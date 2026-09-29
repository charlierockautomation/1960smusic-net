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

    Array.prototype.forEach.call(document.querySelectorAll('[data-pp-count][data-pp-table="' + table.id + '"]'), function(el){
      el.textContent = songs.length;
    });

    function highlight(){
      var s = PlaylistPlayer.getState();
      var activeId = PlaylistPlayer.isThisPlaylistActive(id) && s.song ? s.song.youtube_id : null;
      rows.forEach(function(tr){
        tr.classList.toggle('pp-active', !!activeId && tr.getAttribute('data-pp-yt') === activeId);
      });
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

    Array.prototype.forEach.call(document.querySelectorAll('[data-pp-playall][data-pp-table="' + table.id + '"]'), function(btn){
      btn.addEventListener('click', function(){ PlaylistPlayer.loadPlaylist(songs, 0, id); });
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-pp-shuffle][data-pp-table="' + table.id + '"]'), function(btn){
      btn.addEventListener('click', function(){ PlaylistPlayer.loadPlaylist(shuffle(songs), 0, id); });
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-pp-search][data-pp-table="' + table.id + '"]'), function(input){
      input.addEventListener('input', function(){
        var q = input.value.trim().toLowerCase();
        rows.forEach(function(tr){
          var hay = (tr.getAttribute('data-pp-title') + ' ' + tr.getAttribute('data-pp-artist')).toLowerCase();
          tr.classList.toggle('pp-hidden', q.length > 0 && hay.indexOf(q) === -1);
        });
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    Array.prototype.forEach.call(document.querySelectorAll('table[data-pp-playlist-id]'), setup);
  });
})();
