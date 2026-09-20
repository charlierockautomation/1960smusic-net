/* 1960smusic.net — Radio Dial: Select-a-track dialog.
   Lists a station's tracks (built lazily on open) via the same
   loadStationSongs()/cache and selectStation() from radio-app.js. */

var rdSelectGenre = null;
var rdSelectSongs = [];
var rdSelectInvoker = null;

function rdDialogEls(){
  return {
    dlg: document.getElementById('rd-select-dialog'),
    title: document.getElementById('rd-select-title'),
    search: document.getElementById('rd-select-search'),
    list: document.getElementById('rd-select-list')
  };
}

function rdRenderSelectList(filter){
  var els = rdDialogEls();
  var q = (filter || '').toLowerCase();
  var items = rdSelectSongs.filter(function(s){
    return !q || (s.title + ' ' + s.artist).toLowerCase().indexOf(q) !== -1;
  });
  if (!items.length){
    els.list.innerHTML = '<li class="rd-select-empty">No tracks match.</li>';
    return;
  }
  els.list.innerHTML = items.map(function(s){
    return '<li><button type="button" class="rd-select-item" data-id="' + esc(s.youtube_id) + '">' +
      esc(s.title) + ' &#8211; ' + esc(s.artist) + '</button></li>';
  }).join('');
}

function rdOpenSelectDialog(genreId, name, invoker){
  rdSelectGenre = genreId;
  rdSelectInvoker = invoker;
  var els = rdDialogEls();
  els.title.textContent = 'Select a track: ' + name;
  els.search.value = '';
  els.list.innerHTML = '<li class="rd-select-empty">Loading tracks…</li>';
  els.dlg.showModal();
  els.search.focus();
  loadStationSongs(genreId).then(function(songs){
    if (rdSelectGenre !== genreId) return;
    rdSelectSongs = songs;
    rdRenderSelectList('');
  }).catch(function(){
    els.list.innerHTML = '<li class="rd-select-empty">Could not load tracks.</li>';
  });
}

document.addEventListener('rd:dial-rendered', function(e){
  e.detail.genres.forEach(function(g){
    var el = document.querySelector('.rd-extra-select[data-genre="' + g.id + '"]');
    if (!el) return;
    el.innerHTML = '<button type="button" class="rd-select-btn" data-genre="' + esc(g.id) +
      '" data-name="' + esc(g.name) + '" aria-label="Select a track on ' + esc(g.name) + ' station">Select</button>';
  });
});

document.getElementById('rd-dial').addEventListener('click', function(e){
  var btn = e.target.closest('.rd-select-btn');
  if (!btn) return;
  rdOpenSelectDialog(btn.getAttribute('data-genre'), btn.getAttribute('data-name'), btn);
});

(function(){
  var els = rdDialogEls();
  els.search.addEventListener('input', function(){ rdRenderSelectList(els.search.value); });
  els.list.addEventListener('click', function(e){
    var item = e.target.closest('.rd-select-item');
    if (!item) return;
    var id = item.getAttribute('data-id');
    var song = rdSelectSongs.filter(function(s){ return s.youtube_id === id; })[0];
    if (!song) return;
    els.dlg.close();
    selectStation(rdSelectGenre, song);
  });
  document.getElementById('rd-select-close').addEventListener('click', function(){ els.dlg.close(); });
  els.dlg.addEventListener('close', function(){
    if (rdSelectInvoker) rdSelectInvoker.focus();
  });
})();
