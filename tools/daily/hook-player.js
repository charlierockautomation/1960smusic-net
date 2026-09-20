/* 1960smusic.net — Daily Guessing Game: YouTube IFrame Player engine.
   Player is the game's visible "screen" (see #da-audio in daily.css) --
   always on-page, always full YouTube chrome, never hidden or covered.
   Round length is governed by daily-app.js's countdown, not a forced
   clip cutoff, so this module is just play/pause/stop/destroy. */

var HookPlayer = (function(){
  var player = null;
  var apiReady = false;
  var pendingInit = null;
  var readyTimer = null;

  window.onYouTubeIframeAPIReady = function(){
    apiReady = true;
    if (pendingInit) { var fn = pendingInit; pendingInit = null; fn(); }
  };

  function clearReadyTimer(){
    if (readyTimer) { clearTimeout(readyTimer); readyTimer = null; }
  }

  function create(elementId, firstVideoId, startSeconds, opts){
    player = new YT.Player(elementId, {
      height: '270', width: '480',
      videoId: firstVideoId,
      playerVars: { autoplay: 1, mute: 1, controls: 1, playsinline: 1, start: startSeconds || 0 },
      events: {
        onReady: function(e){ clearReadyTimer(); if (opts.onReady) opts.onReady(e); },
        onStateChange: function(e){ if (opts.onStateChange) opts.onStateChange(e); },
        onError: function(e){ if (opts.onError) opts.onError(e); }
      }
    });
  }

  return {
    /* Plays id from startSeconds. Creates the visible player on first call;
       reuses it (loadVideoById) after, same pattern RadioPlayer already
       uses for continuous auto-advance. */
    play: function(elementId, id, startSeconds, opts){
      opts = opts || {};
      if (player && player.loadVideoById){
        player.loadVideoById({ videoId: id, startSeconds: startSeconds || 0 });
        return;
      }
      clearReadyTimer();
      readyTimer = setTimeout(function(){
        if (opts.onReadyTimeout) opts.onReadyTimeout();
      }, opts.readyTimeoutMs || 9000);
      var start = function(){ create(elementId, id, startSeconds, opts); };
      if (apiReady && window.YT && window.YT.Player) start();
      else pendingInit = start;
    },
    unmute: function(vol){
      if (player && player.unMute) { player.unMute(); player.setVolume(vol == null ? 100 : vol); }
    },
    pause: function(){
      if (player && player.pauseVideo) { try { player.pauseVideo(); } catch(e){} }
    },
    stop: function(){
      if (player && player.stopVideo) player.stopVideo();
    },
    destroy: function(){
      clearReadyTimer();
      pendingInit = null;
      if (player && player.destroy) { try { player.destroy(); } catch(e){} }
      player = null;
    },
    isActive: function(){ return !!player; }
  };
})();
