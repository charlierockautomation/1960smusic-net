/* 1960smusic.net — Radio Dial: YouTube IFrame Player engine.
   Player is the radio's visible "screen" (see #rd-audio in radio.css) --
   always on-page, always full YouTube chrome, never hidden or covered. */

var RadioPlayer = (function(){
  var player = null;
  var apiReady = false;
  var pendingInit = null;
  var readyTimer = null;
  var hooks = {};

  window.onYouTubeIframeAPIReady = function(){
    apiReady = true;
    if (pendingInit) { var fn = pendingInit; pendingInit = null; fn(); }
  };

  function clearReadyTimer(){
    if (readyTimer) { clearTimeout(readyTimer); readyTimer = null; }
  }

  function create(elementId, firstVideoId, autoplay){
    player = new YT.Player(elementId, {
      height: '270', width: '480',
      videoId: firstVideoId,
      playerVars: autoplay
        ? { autoplay: 1, mute: 1, controls: 1, playsinline: 1 }
        : { autoplay: 0, controls: 1, playsinline: 1 },
      events: {
        onReady: function(e){ clearReadyTimer(); if (hooks.onReady) hooks.onReady(e); },
        onStateChange: function(e){ if (hooks.onStateChange) hooks.onStateChange(e); },
        onError: function(e){ if (hooks.onError) hooks.onError(e); }
      }
    });
  }

  return {
    init: function(elementId, firstVideoId, opts){
      hooks = opts || {};
      clearReadyTimer();
      readyTimer = setTimeout(function(){
        if (hooks.onReadyTimeout) hooks.onReadyTimeout();
      }, opts.readyTimeoutMs || 9000);
      var start = function(){ create(elementId, firstVideoId, true); };
      if (apiReady && window.YT && window.YT.Player) start();
      else pendingInit = start;
    },
    preload: function(elementId, firstVideoId){
      if (player) return;
      var start = function(){ create(elementId, firstVideoId, false); };
      if (apiReady && window.YT && window.YT.Player) start();
      else pendingInit = start;
    },
    loadVideo: function(id){
      if (player && player.loadVideoById) player.loadVideoById(id);
    },
    unmute: function(vol){
      if (player && player.unMute) { player.unMute(); player.setVolume(vol == null ? 100 : vol); }
    },
    setVolume: function(vol){
      if (player && player.setVolume) player.setVolume(vol);
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
