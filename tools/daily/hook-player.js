/* 1960smusic.net — Daily Guessing Game: hidden audio-only YouTube hook player.
   Separate from Radio Dial's RadioPlayer (different needs: seek to a start
   point, play a fixed-length clip, then pause -- never a continuous queue).
   All clip timing lives in one place (armClip) so there is never more than
   one pending pause-timer: a stray timer from a previous song firing mid
   playback of the next song was exactly the level-2-audio-cuts-out bug. */

var HookPlayer = (function(){
  var player = null;
  var apiReady = false;
  var pendingInit = null;
  var readyTimer = null;
  var clipTimer = null;

  window.onYouTubeIframeAPIReady = function(){
    apiReady = true;
    if (pendingInit) { var fn = pendingInit; pendingInit = null; fn(); }
  };

  function clearReadyTimer(){
    if (readyTimer) { clearTimeout(readyTimer); readyTimer = null; }
  }
  function clearClipTimer(){
    if (clipTimer) { clearTimeout(clipTimer); clipTimer = null; }
  }
  function armClip(durationMs, onClipEnd){
    clearClipTimer();
    clipTimer = setTimeout(function(){
      clipTimer = null;
      if (player && player.pauseVideo) { try { player.pauseVideo(); } catch(e){} }
      if (onClipEnd) onClipEnd();
    }, durationMs);
  }

  function create(elementId, firstVideoId, startSeconds, durationMs, onClipEnd, opts){
    player = new YT.Player(elementId, {
      height: '1', width: '1',
      videoId: firstVideoId,
      playerVars: {
        autoplay: 1, controls: 0, disablekb: 1, fs: 0, modestbranding: 1,
        playsinline: 1, start: startSeconds || 0
      },
      events: {
        onReady: function(e){
          clearReadyTimer();
          armClip(durationMs, onClipEnd);
          if (opts.onReady) opts.onReady(e);
        },
        onStateChange: function(e){ if (opts.onStateChange) opts.onStateChange(e); },
        onError: function(e){ if (opts.onError) opts.onError(e); }
      }
    });
  }

  return {
    /* Plays id from startSeconds for durationMs, then pauses and calls onClipEnd.
       Creates the hidden player on first call; reuses it (loadVideoById) after. */
    play: function(elementId, id, startSeconds, durationMs, onClipEnd, opts){
      opts = opts || {};
      if (player && player.loadVideoById){
        player.loadVideoById({ videoId: id, startSeconds: startSeconds || 0 });
        armClip(durationMs, onClipEnd);
        return;
      }
      clearReadyTimer();
      readyTimer = setTimeout(function(){
        if (opts.onReadyTimeout) opts.onReadyTimeout();
      }, opts.readyTimeoutMs || 9000);
      var start = function(){ create(elementId, id, startSeconds, durationMs, onClipEnd, opts); };
      if (apiReady && window.YT && window.YT.Player) start();
      else pendingInit = start;
    },
    pause: function(){
      if (player && player.pauseVideo) { try { player.pauseVideo(); } catch(e){} }
    },
    stop: function(){
      clearClipTimer();
      if (player && player.stopVideo) player.stopVideo();
    },
    destroy: function(){
      clearReadyTimer();
      clearClipTimer();
      pendingInit = null;
      if (player && player.destroy) { try { player.destroy(); } catch(e){} }
      player = null;
    },
    isActive: function(){ return !!player; }
  };
})();
