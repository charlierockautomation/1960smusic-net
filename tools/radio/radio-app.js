/* 1960smusic.net — Radio Dial: station data, dial UI, queue + error handling.
   Reads /data/radio-eligible-<genre>.json only (never songs.json — kept separate). */

var GENRE_FREQ = {
  'british-invasion':'88.4','motown-soul':'90.1','folk-rock':'92.5',
  'garage-surf-rock':'94.7','psychedelic-rock':'97.3','country-60s':'99.5',
  'pop-brill-building':'101.9','jazz-easy-listening':'104.6'
};
/* All 8 stations live -- Phase 1 data verified for all 8, one-station
   checkpoint (British Invasion) confirmed working. */
var ENABLED_GENRES = {
  'british-invasion': true, 'motown-soul': true, 'folk-rock': true,
  'garage-surf-rock': true, 'psychedelic-rock': true, 'country-60s': true,
  'pop-brill-building': true, 'jazz-easy-listening': true
};
var SKIP_CODES = { 2:1, 5:1, 100:1, 101:1, 150:1 };
var DEFAULT_GENRE = 'british-invasion';

var cache = {};
var queue = [], queueIdx = 0;
var currentGenre = null, currentSong = null;
var consecutiveFails = 0;
var playingGenre = null;
var loadToken = 0;

function esc(s){ return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
function fetchJSON(path){ return fetch(path).then(function(r){ if(!r.ok) throw new Error(path+' '+r.status); return r.json(); }); }
function setStatus(t){ document.getElementById('rd-status').textContent = t; }

function loadStationSongs(genreId){
  if (cache[genreId]) return Promise.resolve(cache[genreId]);
  return fetchJSON('/data/radio-eligible-' + genreId + '.json').then(function(list){
    cache[genreId] = list; return list;
  });
}

function buildQueue(songs){ queue = shuffle(songs); queueIdx = 0; }

function renderNowPlaying(song, loading){
  document.getElementById('rd-nowplaying').hidden = false;
  document.getElementById('rd-title').textContent = song.title;
  document.getElementById('rd-artist').textContent = song.artist;
  var g = STATIONS_BY_ID[currentGenre];
  document.getElementById('rd-genre').textContent = (g ? g.name + ' · ' + g.freq + ' FM' : '');
  setStatus(loading ? 'Tuning in…' : '');
}

function nextTrack(){
  if (!queue.length) return;
  if (queueIdx >= queue.length) buildQueue(cache[currentGenre]);
  var song = queue[queueIdx++];
  currentSong = song;
  renderNowPlaying(song, true);
  RadioPlayer.loadVideo(song.youtube_id);
}

function hideTrouble(){ document.getElementById('rd-trouble').hidden = true; }
function showTrouble(){ document.getElementById('rd-trouble').hidden = false; setStatus(''); }
function hideDiagnostic(){ document.getElementById('rd-diagnostic').hidden = true; }
function showDiagnostic(){ document.getElementById('rd-diagnostic').hidden = false; setStatus(''); }

function onPlayerReady(){ /* first track autoplays via playerVars.autoplay */ }
function onPlayerStateChange(e){
  if (e.data === YT.PlayerState.PLAYING){ consecutiveFails = 0; setStatus(''); }
  else if (e.data === YT.PlayerState.ENDED){ nextTrack(); }
}
function onPlayerError(e){
  if (typeof gtag === 'function' && currentSong){
    gtag('event', 'radio_track_error', { genre: currentGenre, video_id: currentSong.youtube_id, error_code: e.data });
  }
  if (!SKIP_CODES[e.data]) return;
  consecutiveFails++;
  if (consecutiveFails >= 3){ showTrouble(); return; }
  nextTrack();
}
function onReadyTimeout(){ showDiagnostic(); }

function updateTiles(){
  document.querySelectorAll('.rd-station').forEach(function(tile){
    var id = tile.getAttribute('data-genre');
    var isPlaying = id === playingGenre;
    tile.classList.toggle('active', isPlaying);
    var playBtn = tile.querySelector('.rd-play-btn');
    var stopBtn = tile.querySelector('.rd-stop-btn');
    if (playBtn) playBtn.disabled = isPlaying;
    if (stopBtn) stopBtn.disabled = !isPlaying;
  });
}

function selectStation(genreId){
  if (!ENABLED_GENRES[genreId]) return;
  hideTrouble(); hideDiagnostic();
  consecutiveFails = 0;
  playingGenre = genreId;
  updateTiles();
  var token = ++loadToken;
  document.getElementById('rd-tunein-wrap').hidden = true;
  setStatus('Tuning in…');
  loadStationSongs(genreId).then(function(songs){
    if (token !== loadToken) return;
    currentGenre = genreId;
    buildQueue(songs);
    var song = queue[queueIdx++];
    currentSong = song;
    renderNowPlaying(song, true);
    if (!RadioPlayer.isActive()){
      RadioPlayer.init('rd-audio', song.youtube_id, {
        readyTimeoutMs: 9000, onReady: onPlayerReady,
        onStateChange: onPlayerStateChange, onError: onPlayerError, onReadyTimeout: onReadyTimeout
      });
    } else {
      RadioPlayer.loadVideo(song.youtube_id);
    }
  }).catch(function(){
    if (token !== loadToken) return;
    setStatus('Could not load this station. Try another.');
  });
}

function stopStation(){
  loadToken++;
  RadioPlayer.stop();
  playingGenre = null;
  consecutiveFails = 0;
  hideTrouble(); hideDiagnostic();
  setStatus('Stopped.');
  updateTiles();
}

function retryInit(){
  RadioPlayer.destroy();
  hideDiagnostic();
  selectStation(currentGenre || DEFAULT_GENRE);
}

var STATIONS_BY_ID = {};
function renderDial(genres){
  var ordered = genres.slice().sort(function(a,b){
    return parseFloat(GENRE_FREQ[a.id]||'999') - parseFloat(GENRE_FREQ[b.id]||'999');
  });
  ordered.forEach(function(g){ STATIONS_BY_ID[g.id] = { name: g.name, freq: GENRE_FREQ[g.id] || '' }; });
  document.getElementById('rd-dial').innerHTML = ordered.map(function(g){
    var enabled = !!ENABLED_GENRES[g.id];
    var freq = GENRE_FREQ[g.id] || '';
    return '<div class="rd-station' + (enabled ? '' : ' soon') + '" data-genre="' + esc(g.id) + '">' +
      '<span class="freq">' + esc(freq) + '</span><span class="name">' + esc(g.name) + '</span>' +
      (enabled ?
        '<div class="rd-ctrls">' +
          '<button type="button" class="rd-play-btn" data-genre="' + esc(g.id) + '">&#9654; Play</button>' +
          '<button type="button" class="rd-stop-btn" data-genre="' + esc(g.id) + '" disabled>&#9632; Stop</button>' +
        '</div>' :
        '<span class="soon-tag">Tuning in soon</span>') +
    '</div>';
  }).join('');
  document.getElementById('rd-dial').addEventListener('click', function(e){
    var playBtn = e.target.closest('.rd-play-btn');
    var stopBtn = e.target.closest('.rd-stop-btn');
    if (playBtn && !playBtn.disabled) selectStation(playBtn.getAttribute('data-genre'));
    else if (stopBtn && !stopBtn.disabled) stopStation();
  });
}

function requestedGenre(){
  var id = new URLSearchParams(location.search).get('station');
  return (id && ENABLED_GENRES[id]) ? id : null;
}

(function init(){
  var requested = requestedGenre();
  fetchJSON('/data/genres.json').then(function(genres){
    renderDial(genres);
    if (requested){
      var tile = document.querySelector('.rd-station[data-genre="' + requested + '"]');
      if (tile){
        tile.classList.add('requested');
        tile.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  }).catch(function(){
    document.getElementById('rd-dial').innerHTML = '<p>Stations unavailable.</p>';
  });
  document.getElementById('rd-tunein').addEventListener('click', function(){ selectStation(requestedGenre() || DEFAULT_GENRE); });
  document.getElementById('rd-try-again').addEventListener('click', retryInit);
})();
