/* 1960smusic.net — Daily Guessing Game: per-round countdown.
   Computed from Date.now() timestamps, never decremented, so background-tab
   throttling can't stretch or shrink a round. Freezes only on BUFFERING and
   before the round's first PLAYING event; a native-controls pause keeps
   counting so pausing can never buy extra time. */

var TIMER = { START_SECONDS: 20, STEP_SECONDS: 1, MIN_SECONDS: 6 };

function secondsForLevel(lvl){
  return Math.max(TIMER.MIN_SECONDS, TIMER.START_SECONDS - (lvl - 1) * TIMER.STEP_SECONDS);
}

var DailyTimer = (function(){
  var state = null;

  function render(ms){
    var el = document.getElementById('da-timer');
    if (!el) return;
    el.hidden = false;
    var secs = Math.ceil(ms / 1000);
    el.textContent = secs + 's';
    el.classList.toggle('low', secs <= 5);
  }
  function elapsedMs(){
    var extra = state.playStartedAt != null ? Date.now() - state.playStartedAt : 0;
    return state.elapsedBeforePauseMs + extra;
  }
  function freeze(){
    if (!state) return;
    if (state.playStartedAt != null){
      state.elapsedBeforePauseMs += Date.now() - state.playStartedAt;
      state.playStartedAt = null;
    }
    if (state.tickHandle){ clearInterval(state.tickHandle); state.tickHandle = null; }
  }
  function tick(){
    if (!state || state.fired) return;
    var remaining = state.totalMs - elapsedMs();
    if (remaining <= 0){
      state.fired = true;
      render(0);
      freeze();
      if (state.onTimeout) state.onTimeout();
      return;
    }
    render(remaining);
  }

  return {
    reset: function(totalMs, onTimeout){
      DailyTimer.stop();
      state = { totalMs: totalMs, elapsedBeforePauseMs: 0, playStartedAt: null, fired: false, tickHandle: null, onTimeout: onTimeout };
      render(totalMs);
    },
    resume: function(){
      if (!state || state.fired) return;
      if (state.playStartedAt == null) state.playStartedAt = Date.now();
      if (!state.tickHandle) state.tickHandle = setInterval(tick, 200);
    },
    freeze: freeze,
    /* Locks the round's answer in: stops the clock permanently so a
       delayed timeout tick can't race a click that already landed. */
    lock: function(){ if (state) state.fired = true; freeze(); },
    stop: function(){
      if (state && state.tickHandle) clearInterval(state.tickHandle);
      state = null;
      var el = document.getElementById('da-timer');
      if (el) el.hidden = true;
    }
  };
})();
