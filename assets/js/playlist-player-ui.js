/* 1960smusic.net -- sticky bar UI for PlaylistPlayer (see playlist-player.js).
   Builds the bar once, keeps it out of the way (translated off screen, not
   display:none, so #pp-video is ready to size itself) until a playlist
   loads. The video inside is always full YouTube chrome, visible and never
   covered, per the site's YouTube Embed Rule. */

(function(){
  function fmtTime(sec){
    sec = Math.max(0, Math.floor(sec || 0));
    var m = Math.floor(sec / 60), s = sec % 60;
    return m + ':' + String(s).padStart(2, '0');
  }

  var bar = document.createElement('div');
  bar.className = 'pp-bar';
  bar.setAttribute('aria-hidden', 'true');
  bar.innerHTML =
    '<div class="pp-bar-inner">' +
      '<div class="pp-bar-video"><div id="pp-video"></div></div>' +
      '<div class="pp-bar-info">' +
        '<p class="pp-bar-title" id="pp-bar-title">No track</p>' +
        '<p class="pp-bar-artist" id="pp-bar-artist"></p>' +
        '<div class="pp-bar-progress-track"><div class="pp-bar-progress-fill" id="pp-bar-fill"></div></div>' +
        '<div class="pp-bar-time"><span id="pp-bar-elapsed">0:00</span> / <span id="pp-bar-duration">0:00</span> ' +
          '<span class="pp-bar-counter" id="pp-bar-counter"></span></div>' +
      '</div>' +
      '<div class="pp-bar-transport">' +
        '<button type="button" class="pp-btn" id="pp-btn-prev" aria-label="Previous track">&#9198;</button>' +
        '<button type="button" class="pp-btn pp-btn-play" id="pp-btn-play" aria-label="Play">&#9654;</button>' +
        '<button type="button" class="pp-btn" id="pp-btn-stop" aria-label="Stop">&#9632;</button>' +
        '<button type="button" class="pp-btn" id="pp-btn-next" aria-label="Next track">&#9197;</button>' +
        '<input type="range" class="pp-vol" id="pp-vol" min="0" max="100" value="100" aria-label="Volume">' +
      '</div>' +
    '</div>';
  document.addEventListener('DOMContentLoaded', function(){ document.body.appendChild(bar); attach(); });

  function attach(){
    document.getElementById('pp-btn-prev').addEventListener('click', function(){ PlaylistPlayer.prev(); });
    document.getElementById('pp-btn-next').addEventListener('click', function(){ PlaylistPlayer.next(); });
    document.getElementById('pp-btn-stop').addEventListener('click', function(){ PlaylistPlayer.stop(); });
    document.getElementById('pp-btn-play').addEventListener('click', function(){
      var s = PlaylistPlayer.getState();
      if (s.isPlaying) PlaylistPlayer.pause(); else PlaylistPlayer.play();
    });
    document.getElementById('pp-vol').addEventListener('input', function(e){
      PlaylistPlayer.setVolume(Number(e.target.value));
    });
  }

  document.addEventListener('pp:update', function(e){
    var s = e.detail;
    var has = s.playlist && s.playlist.length > 0;
    bar.classList.toggle('pp-visible', has);
    bar.setAttribute('aria-hidden', has ? 'false' : 'true');
    if (!has) return;
    document.getElementById('pp-bar-title').textContent = s.song ? s.song.title : 'No track';
    document.getElementById('pp-bar-artist').textContent = s.song ? (s.song.artist + (s.song.year ? ' (' + s.song.year + ')' : '')) : '';
    document.getElementById('pp-bar-elapsed').textContent = fmtTime(s.currentTime);
    document.getElementById('pp-bar-duration').textContent = fmtTime(s.duration);
    document.getElementById('pp-bar-counter').textContent = (s.currentIndex + 1) + ' / ' + s.playlist.length;
    var pct = s.duration > 0 ? Math.min(100, (s.currentTime / s.duration) * 100) : 0;
    document.getElementById('pp-bar-fill').style.width = pct + '%';
    var playBtn = document.getElementById('pp-btn-play');
    playBtn.innerHTML = s.isPlaying ? '&#10074;&#10074;' : '&#9654;';
    playBtn.setAttribute('aria-label', s.isPlaying ? 'Pause' : 'Play');
  });
})();
