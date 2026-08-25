/* 1960smusic.net — Radio Dial: YouTube IFrame Player engine.
   Hidden audio-only player; the UI on top never shows YouTube chrome. */

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

  function create(elementId, firstVideoId){
    player = new YT.Player(elementId, {
      height: '1', width: '1',
      videoId: firstVideoId,
      playerVars: { autoplay: 1, controls: 0, disablekb: 1, fs: 0, modestbranding: 1, playsinline: 1 },
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
      var start = function(){ create(elementId, firstVideoId); };
      if (apiReady && window.YT && window.YT.Player) start();
      else pendingInit = start;
    },
    loadVideo: function(id){
      if (player && player.loadVideoById) player.loadVideoById(id);
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
