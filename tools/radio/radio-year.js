/* 1960smusic.net — Radio Dial: optional ?year= filter (Phase 2 decade
   spine, docs/phase2-decade-spine.md task 1 follow-up). Reads globals from
   radio-app.js (loadStationSongs, cache, setStatus). When a valid year is
   present, narrows each enabled station's song pool to that year in place
   by overwriting radio-app.js's shared `cache`, so Play/Skip/Select all
   stay within-year with no changes needed elsewhere. A station with zero
   songs for that year is left unfiltered rather than made unplayable. */

function rdRequestedYear(){
  var y = parseInt(new URLSearchParams(location.search).get('year'), 10);
  return (y >= 1960 && y <= 1969) ? y : null;
}

(function init(){
  var year = rdRequestedYear();
  if (!year) return;
  document.addEventListener('rd:dial-rendered', function(e){
    var genres = (e.detail && e.detail.genres) || [];
    var firstMatch = null;
    var pending = genres.map(function(g){
      return loadStationSongs(g.id).then(function(songs){
        var filtered = songs.filter(function(s){ return s.year === year; });
        if (filtered.length){
          cache[g.id] = filtered;
          if (!firstMatch) firstMatch = g.id;
        }
      });
    });
    Promise.all(pending).then(function(){
      if (!firstMatch){
        setStatus('No stations have ' + year + ' songs yet.');
        return;
      }
      var tile = document.querySelector('.rd-station[data-genre="' + firstMatch + '"]');
      if (tile){
        tile.classList.add('requested');
        tile.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  }, { once: true });
})();
