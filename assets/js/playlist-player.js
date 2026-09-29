/* 1960smusic.net -- shared playlist player engine (year pages, later
   /best-60s-songs/, genre hubs, tools). Ported from the working sticky
   player at musicofthe80s.com (components/player/cassette-player.tsx +
   contexts/player-context.tsx): same lazy-create-on-first-play engine,
   same mobile-autoplay-stuck fallback, same error-skip throttle, adapted
   from React/context to plain globals for this site's no-build-step
   setup. One sticky YouTube player, lazy created on first play so no
   iframe loads before a user interaction (page speed). Dispatches
   'pp:update' on document with a full state snapshot after every change;
   pair with playlist-player-ui.js (the sticky bar) and playlist-table.js
   (per-page tracklist controls). */

var PlaylistPlayer = (function(){
  var playlist = [], currentIndex = 0, playlistId = '';
  var isPlaying = false, currentTime = 0, duration = 0;
  var player = null, apiLoading = false, pendingStart = null;
  var hasUnmuted = false;
  var errStreak = 0, lastErrTime = 0, skipTimer = null;
  var pollTimer = null, autoplayCheckTimer = null;

  function emit(){
    document.dispatchEvent(new CustomEvent('pp:update', { detail: getState() }));
  }

  function loadApi(cb){
    if (window.YT && window.YT.Player){ cb(); return; }
    pendingStart = cb;
    if (apiLoading) return;
    apiLoading = true;
    var prev = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = function(){
      if (prev) prev();
      if (pendingStart){ var fn = pendingStart; pendingStart = null; fn(); }
    };
    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    document.head.appendChild(tag);
  }

  function startPolling(){
    stopPolling();
    pollTimer = setInterval(function(){
      if (!player || !isPlaying) return;
      try { currentTime = player.getCurrentTime() || 0; duration = player.getDuration() || 0; } catch(e){}
      emit();
    }, 500);
  }
  function stopPolling(){ if (pollTimer){ clearInterval(pollTimer); pollTimer = null; } }

  function checkAutoplayStuck(){
    if (autoplayCheckTimer) clearTimeout(autoplayCheckTimer);
    autoplayCheckTimer = setTimeout(function(){
      if (!player || !isPlaying) return;
      try {
        var st = player.getPlayerState();
        var PS = window.YT.PlayerState;
        if (st === PS.CUED || st === PS.UNSTARTED){
          isPlaying = false;
          emit();
        }
      } catch(e){}
    }, 2500);
  }

  function onStateChange(e){
    var PS = window.YT.PlayerState;
    if (e.data === PS.PLAYING){
      errStreak = 0;
      isPlaying = true;
      if (!hasUnmuted){ hasUnmuted = true; try { player.unMute(); player.setVolume(100); } catch(err){} }
      startPolling();
      emit();
    } else if (e.data === PS.PAUSED){
      isPlaying = false; stopPolling(); emit();
    } else if (e.data === PS.ENDED){
      next();
    }
  }

  function onError(e){
    var song = playlist[currentIndex];
    console.warn('PlaylistPlayer: YouTube error', e.data, 'for', song && song.title, song && song.youtube_id);
    var now = Date.now();
    if (now - lastErrTime > 6000) errStreak = 0;
    lastErrTime = now;
    errStreak++;
    if (errStreak >= 4){
      console.warn('PlaylistPlayer: too many consecutive errors, stopping auto-skip.');
      isPlaying = false; emit();
      return;
    }
    if (skipTimer) clearTimeout(skipTimer);
    skipTimer = setTimeout(next, 600);
  }

  function ensurePlayer(cb){
    if (player){ cb(); return; }
    loadApi(function(){
      if (player){ cb(); return; }
      var host = document.getElementById('pp-video');
      if (!host) return;
      player = new YT.Player(host, {
        host: 'https://www.youtube-nocookie.com',
        width: '100%', height: '100%',
        playerVars: { autoplay: 1, mute: 1, controls: 1, playsinline: 1 },
        events: {
          onReady: function(){ cb(); },
          onStateChange: onStateChange,
          onError: onError
        }
      });
    });
  }

  function startCurrent(){
    var song = playlist[currentIndex];
    if (!song) return;
    currentTime = 0; duration = 0;
    ensurePlayer(function(){
      try { player.loadVideoById(song.youtube_id); checkAutoplayStuck(); } catch(e){}
    });
    emit();
  }

  function loadPlaylist(songs, startIndex, id){
    playlist = songs || [];
    if (!playlist.length) return;
    currentIndex = Math.max(0, Math.min(startIndex || 0, playlist.length - 1));
    playlistId = id || '';
    isPlaying = true;
    startCurrent();
  }

  function play(){
    if (!playlist.length) return;
    if (player){ try { player.playVideo(); } catch(e){} isPlaying = true; startPolling(); emit(); }
    else startCurrent();
  }
  function pause(){
    if (player){ try { player.pauseVideo(); } catch(e){} }
    isPlaying = false; stopPolling(); emit();
  }
  function stop(){
    if (player){ try { player.stopVideo(); } catch(e){} }
    isPlaying = false; currentTime = 0; stopPolling(); emit();
  }
  function next(){
    if (!playlist.length) return;
    currentIndex = (currentIndex + 1) % playlist.length;
    isPlaying = true;
    startCurrent();
  }
  function prev(){
    if (!playlist.length) return;
    currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
    isPlaying = true;
    startCurrent();
  }
  function seekTo(index){
    if (index < 0 || index >= playlist.length) return;
    currentIndex = index;
    isPlaying = true;
    startCurrent();
  }
  function setVolume(v){ if (player) try { player.setVolume(v); } catch(e){} }

  function isThisPlaylistActive(id){ return playlist.length > 0 && playlistId === id; }
  function getState(){
    return {
      playlist: playlist, currentIndex: currentIndex, playlistId: playlistId,
      isPlaying: isPlaying, currentTime: currentTime, duration: duration,
      song: playlist[currentIndex] || null
    };
  }

  return {
    loadPlaylist: loadPlaylist, play: play, pause: pause, stop: stop,
    next: next, prev: prev, seekTo: seekTo, setVolume: setVolume,
    isThisPlaylistActive: isThisPlaylistActive, getState: getState
  };
})();
