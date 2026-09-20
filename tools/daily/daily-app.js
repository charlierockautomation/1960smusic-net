/* 1960smusic.net — Daily Guessing Game: level state machine, scoring,
   year-guess multiple-choice UI, hook playback. Pool loading/selection is
   in daily-pool.js, the countdown in daily-timer.js, the leaderboard in
   daily-leaderboard.js -- split to keep this file under the line ceiling. */

var MAX_LEVEL = 15;
var MAX_SCORE = MAX_LEVEL * (MAX_LEVEL + 1); // 240
var READY_TIMEOUT_MS = 9000;

var level = 1, songInLevel = 0, score = 0, usedIds = {};
var currentSong = null, currentAccepted = [], currentOptions = [];
var running = false, hasUnmuted = false, troubleRetries = 0;

function renderScorebar(){
  document.getElementById('da-scorebar').innerHTML =
    '<span>Level <strong>' + level + '</strong> of ' + MAX_LEVEL + '</span>' +
    '<span>Song <strong>' + (songInLevel + 1) + '</strong> of ' + level + '</span>' +
    '<span>Score <strong>' + score + '</strong></span>';
}

function playCurrentClip(){
  HookPlayer.play('da-audio', currentSong.youtube_id, hookStart(currentSong), {
    readyTimeoutMs: READY_TIMEOUT_MS,
    onStateChange: onPlayerStateChange,
    onReadyTimeout: onPlayerTrouble,
    onError: onPlayerTrouble
  });
}
function onPlayerStateChange(e){
  if (e.data === YT.PlayerState.PLAYING){
    troubleRetries = 0;
    if (!hasUnmuted){ hasUnmuted = true; HookPlayer.unmute(); }
    DailyTimer.resume();
  } else if (e.data === YT.PlayerState.BUFFERING){
    DailyTimer.freeze();
  }
}
function onPlayerTrouble(){
  troubleRetries++;
  if (troubleRetries > 3){
    DailyTimer.stop();
    running = false;
    document.getElementById('da-game').innerHTML =
      '<div class="result"><p class="kicker">Playback trouble</p>' +
      '<p class="desc">This round could not load a video. Try again shortly.</p>' +
      '<button class="btn" id="da-restart" type="button">Play again</button></div>';
    document.getElementById('da-restart').addEventListener('click', startRun);
    return;
  }
  usedIds[currentSong.youtube_id] = true; // don't retry the same broken id
  renderQuestion();
}

function revealText(song){
  var a = song.year_market ? (song.year + ' in the ' + song.year_market) : String(song.year);
  var b = song.year_alt_market ? (song.year_alt + ' in the ' + song.year_alt_market) : String(song.year_alt);
  return a + ' and ' + b;
}

function renderQuestion(){
  currentSong = pickTarget(usedIds);
  if (!currentSong){ endRun(false); return; }
  currentAccepted = acceptedYears(currentSong);
  var distractors = pickYearDistractors(currentAccepted, 4 - currentAccepted.length);
  currentOptions = shuffle(currentAccepted.concat(distractors));
  renderScorebar();
  var opts = currentOptions.map(function(y, i){
    return '<button class="option" data-idx="' + i + '">' + y + '</button>';
  }).join('');
  document.getElementById('da-game').innerHTML =
    '<div class="q">' +
      '<p class="prompt">What year was this released?</p>' +
      '<div class="options" id="da-options">' + opts + '</div>' +
      '<div id="da-reveal"></div>' +
    '</div>';
  document.getElementById('da-options').addEventListener('click', onAnswer);
  DailyTimer.reset(secondsForLevel(level) * 1000, onTimeout);
  playCurrentClip();
}

function disableOptions(){
  document.querySelectorAll('#da-options .option').forEach(function(b){ b.disabled = true; });
}
function showReveal(){
  if (currentAccepted.length > 1){
    document.getElementById('da-reveal').innerHTML =
      '<p class="da-reveal">Released ' + revealText(currentSong) + '. Both count.</p>';
  }
}

function onAnswer(e){
  var btn = e.target.closest('.option');
  if (!btn) return;
  DailyTimer.lock();
  HookPlayer.pause();
  disableOptions();
  var idx = parseInt(btn.getAttribute('data-idx'), 10);
  var correct = currentAccepted.indexOf(currentOptions[idx]) !== -1;
  btn.classList.add(correct ? 'correct' : 'wrong');
  showReveal();
  usedIds[currentSong.youtube_id] = true;
  setTimeout(function(){ correct ? onCorrect() : endRun(false); }, 1300);
}

function onTimeout(){
  HookPlayer.pause();
  disableOptions();
  document.querySelectorAll('#da-options .option').forEach(function(b, i){
    if (currentAccepted.indexOf(currentOptions[i]) !== -1) b.classList.add('correct');
  });
  showReveal();
  usedIds[currentSong.youtube_id] = true;
  setTimeout(function(){ endRun(false); }, 1300);
}

function onCorrect(){
  score += 1;
  songInLevel += 1;
  if (songInLevel >= level){
    score += level;
    if (level >= MAX_LEVEL){ endRun(true); return; }
    renderLevelClear();
  } else {
    renderQuestion();
  }
}

function renderLevelClear(){
  DailyTimer.stop();
  document.getElementById('da-game').innerHTML =
    '<div class="result">' +
      '<p class="kicker">Level ' + level + ' cleared</p>' +
      '<h2>+' + level + ' bonus</h2>' +
      '<p class="desc">Score so far: <strong>' + score + '</strong></p>' +
      '<button class="btn" id="da-continue" type="button">Continue to Level ' + (level + 1) + '</button>' +
    '</div>';
  document.getElementById('da-continue').addEventListener('click', function(){
    level += 1; songInLevel = 0; renderQuestion();
  });
}

function endRun(cleared){
  running = false;
  DailyTimer.stop();
  HookPlayer.stop();
  var levelReached = cleared ? MAX_LEVEL : level;
  var songsInLevel = cleared ? MAX_LEVEL : songInLevel;
  renderScorebar();
  document.getElementById('da-game').innerHTML =
    '<div class="result" id="da-gameover">' +
      '<p class="kicker">' + (cleared ? 'Perfect run!' : 'Game over') + '</p>' +
      '<h2>Final score: ' + score + '</h2>' +
      '<p class="desc">Reached level ' + levelReached + ' of ' + MAX_LEVEL + '.</p>' +
      '<div id="da-entry"></div>' +
      '<button class="btn secondary" id="da-restart" type="button">Play again</button>' +
    '</div>';
  document.getElementById('da-restart').addEventListener('click', startRun);
  checkLeaderboard(score, levelReached, songsInLevel, cleared);
}

function startRun(){
  running = true;
  level = 1; songInLevel = 0; score = 0; usedIds = {};
  hasUnmuted = false; troubleRetries = 0;
  HookPlayer.destroy();
  renderQuestion();
}

(function init(){
  document.getElementById('da-start').addEventListener('click', function(){
    document.getElementById('da-intro').hidden = true;
    document.getElementById('da-game').hidden = false;
    startRun();
  });
  loadAllSongs();
  fetchLeaderboard().then(renderLeaderboard);
})();
