/* 1960smusic.net — Radio Dial: Skip + Volume controls.
   Reads globals from radio-app.js (queue, nextTrack, RadioPlayer, esc). One
   shared volume for the whole page since only one station plays at a time. */

var RD_VOL_KEY = 'rd-volume';
var rdLastSkip = 0;

function rdLoadVolume(){
  try {
    var v = parseInt(localStorage.getItem(RD_VOL_KEY), 10);
    return (v >= 0 && v <= 100) ? v : 100;
  } catch(e){ return 100; }
}
function rdSaveVolume(v){ try { localStorage.setItem(RD_VOL_KEY, String(v)); } catch(e){} }

var rdVolume = rdLoadVolume();

function rdIOSVolumeLocked(){
  var ua = navigator.userAgent || '';
  if (/iPhone|iPad|iPod/.test(ua)) return true;
  return navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1;
}

function rdApplyVolume(){ RadioPlayer.setVolume(rdVolume); }

function rdSyncVolumeUI(){
  document.querySelectorAll('.rd-vol-slider').forEach(function(el){ el.value = rdVolume; });
}

function rdOnVolumeInput(v){
  rdVolume = v;
  rdSaveVolume(rdVolume);
  rdApplyVolume();
  rdSyncVolumeUI();
}

function rdSkipBtnHTML(id, name){
  return '<button type="button" class="rd-skip-btn" data-genre="' + esc(id) +
    '" disabled aria-label="Skip to next track on ' + esc(name) + ' station">&#9197; Skip</button>';
}
function rdVolumeHTML(name){
  if (rdIOSVolumeLocked()) return '<p class="rd-vol-hint">Use your device volume buttons.</p>';
  return '<label class="rd-vol-wrap"><span class="rd-vol-label">Vol</span>' +
    '<input type="range" class="rd-vol-slider" min="0" max="100" value="' + rdVolume +
    '" aria-label="Volume for ' + esc(name) + ' station"></label>';
}

document.addEventListener('rd:dial-rendered', function(e){
  e.detail.genres.forEach(function(g){
    var el = document.querySelector('.rd-extra-ctrls[data-genre="' + g.id + '"]');
    if (!el) return;
    el.innerHTML = '<div class="rd-ctrls-row">' + rdSkipBtnHTML(g.id, g.name) + '</div>' + rdVolumeHTML(g.name);
  });
});

document.addEventListener('rd:tiles-updated', function(e){
  document.querySelectorAll('.rd-skip-btn').forEach(function(btn){
    btn.disabled = btn.getAttribute('data-genre') !== e.detail.playingGenre;
  });
});

document.addEventListener('rd:track-started', function(){ rdApplyVolume(); });

document.getElementById('rd-dial').addEventListener('click', function(e){
  var skipBtn = e.target.closest('.rd-skip-btn');
  if (!skipBtn || skipBtn.disabled) return;
  var now = Date.now();
  if (now - rdLastSkip < 500) return;
  rdLastSkip = now;
  nextTrack();
});

document.getElementById('rd-dial').addEventListener('input', function(e){
  if (e.target.classList.contains('rd-vol-slider')) rdOnVolumeInput(parseInt(e.target.value, 10));
});
