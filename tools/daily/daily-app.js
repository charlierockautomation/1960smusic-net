/* 1960smusic.net — Daily Guessing Game: level state machine, scoring,
   multiple-choice UI, hook playback, leaderboard.
   Reuses the Radio Dial's radio-eligible-<genre>.json pools (never a
   separate dataset) plus an optional hook_start_seconds field per song. */

var GENRES = [
  'british-invasion', 'motown-soul', 'folk-rock', 'garage-surf-rock',
  'psychedelic-rock', 'country-60s', 'pop-brill-building', 'jazz-easy-listening'
];
var MAX_LEVEL = 15;
var CLIP_MS = 6000;
var DEFAULT_HOOK_START = 15;
var MAX_SCORE = MAX_LEVEL * (MAX_LEVEL + 1); // 240

var ALL_SONGS = [];
var level = 1, songInLevel = 0, score = 0, usedIds = {};
var currentSong = null, currentOptions = [];
var running = false;

function esc(s){ return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }

function hookStart(song){
  return Number.isFinite(song.hook_start_seconds) ? song.hook_start_seconds : DEFAULT_HOOK_START;
}

function loadAllSongs(){
  return Promise.all(GENRES.map(function(g){
    return fetch('/data/radio-eligible-' + g + '.json').then(function(r){ return r.json(); });
  })).then(function(lists){
    ALL_SONGS = [].concat.apply([], lists);
  });
}

function pickTarget(){
  var pool = ALL_SONGS.filter(function(s){ return !usedIds[s.youtube_id]; });
  return randomPick(pool);
}

function pickDistractors(correct, n){
  var pool = ALL_SONGS.filter(function(s){
    return s.genre === correct.genre && s.youtube_id !== correct.youtube_id && s.title !== correct.title;
  });
  pool = shuffle(pool);
  var out = [], seenTitles = {};
  for (var i = 0; i < pool.length && out.length < n; i++){
    if (seenTitles[pool[i].title]) continue;
    seenTitles[pool[i].title] = true;
    out.push(pool[i]);
  }
  if (out.length < n){
    var fallback = shuffle(ALL_SONGS.filter(function(s){ return s.youtube_id !== correct.youtube_id; }));
    for (var j = 0; j < fallback.length && out.length < n; j++) out.push(fallback[j]);
  }
  return out;
}

function renderScorebar(){
  document.getElementById('da-scorebar').innerHTML =
    '<span>Level <strong>' + level + '</strong> of ' + MAX_LEVEL + '</span>' +
    '<span>Song <strong>' + (songInLevel + 1) + '</strong> of ' + level + '</span>' +
    '<span>Score <strong>' + score + '</strong></span>';
}

function playCurrentClip(){
  var start = hookStart(currentSong);
  var btn = document.getElementById('da-play');
  btn.disabled = true;
  btn.textContent = 'Playing…';
  HookPlayer.play('da-audio', currentSong.youtube_id, start, CLIP_MS, onClipDone, {
    readyTimeoutMs: 9000,
    onReadyTimeout: function(){ btn.disabled = false; btn.textContent = '▶ Play Hook'; }
  });
}
function onClipDone(){
  var btn = document.getElementById('da-play');
  if (btn){ btn.disabled = false; btn.textContent = '▶ Replay Hook'; }
}

function renderQuestion(){
  currentSong = pickTarget();
  currentOptions = shuffle(pickDistractors(currentSong, 3).concat([currentSong]));
  renderScorebar();
  var opts = currentOptions.map(function(s, i){
    return '<button class="option" data-idx="' + i + '">' +
      '<span class="da-title">' + esc(s.title) + '</span>' +
      '<span class="da-artist">' + esc(s.artist) + '</span></button>';
  }).join('');
  document.getElementById('da-game').innerHTML =
    '<div class="q">' +
      '<p class="prompt">Name this song.</p>' +
      '<button class="btn" id="da-play" type="button">&#9654; Play Hook</button>' +
      '<div class="options" id="da-options">' + opts + '</div>' +
    '</div>';
  document.getElementById('da-play').addEventListener('click', playCurrentClip);
  document.getElementById('da-options').addEventListener('click', onAnswer);
}

function onAnswer(e){
  var btn = e.target.closest('.option');
  if (!btn) return;
  document.querySelectorAll('#da-options .option').forEach(function(b){ b.disabled = true; });
  var picked = currentOptions[parseInt(btn.getAttribute('data-idx'), 10)];
  var correct = picked.youtube_id === currentSong.youtube_id;
  btn.classList.add(correct ? 'correct' : 'wrong');
  usedIds[currentSong.youtube_id] = true;
  setTimeout(function(){ correct ? onCorrect() : endRun(false); }, 1100);
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

/* ---- leaderboard ---- */
function fetchLeaderboard(){
  return fetch('/api/leaderboard').then(function(r){ return r.json(); }).catch(function(){ return []; });
}
function renderLeaderboard(list){
  var el = document.getElementById('da-leaderboard');
  if (!el) return;
  if (!list.length){ el.innerHTML = '<p class="desc">No scores yet today. Be the first.</p>'; return; }
  el.innerHTML = '<ol class="da-lb-list">' + list.map(function(e){
    return '<li><span class="da-lb-name">' + esc(e.name) + '</span>' +
      '<span class="da-lb-score">' + e.score + '</span>' +
      '<span class="da-lb-level">Lv ' + e.level_reached + '</span></li>';
  }).join('') + '</ol>';
}
function checkLeaderboard(finalScore, levelReached, songsInLevel, cleared){
  fetchLeaderboard().then(function(list){
    renderLeaderboard(list);
    var qualifies = list.length < 5 || finalScore > list[list.length - 1].score;
    if (qualifies && finalScore > 0) renderEntryForm(finalScore, levelReached, songsInLevel, cleared);
  });
}
function renderEntryForm(finalScore, levelReached, songsInLevel, cleared){
  var wrap = document.getElementById('da-entry');
  wrap.innerHTML =
    '<p class="feedback">Top 5 score! Enter a name for the leaderboard.</p>' +
    '<form id="da-lb-form" class="da-lb-form">' +
      '<input type="text" id="da-lb-name" maxlength="20" placeholder="Your name" required>' +
      '<button class="btn" type="submit">Submit</button>' +
    '</form>' +
    '<p class="feedback" id="da-lb-msg"></p>';
  document.getElementById('da-lb-form').addEventListener('submit', function(e){
    e.preventDefault();
    var name = document.getElementById('da-lb-name').value.trim();
    if (!name) return;
    submitScore(name, finalScore, levelReached, songsInLevel, cleared);
  });
}
function submitScore(name, finalScore, levelReached, songsInLevel, cleared){
  var msg = document.getElementById('da-lb-msg');
  msg.textContent = 'Submitting…';
  fetch('/api/leaderboard', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: name, score: finalScore, level_reached: levelReached,
      songs_correct_in_level: songsInLevel, full_clear: !!cleared
    })
  }).then(function(r){ return r.json().then(function(body){ return { ok: r.ok, body: body }; }); })
    .then(function(res){
      if (res.ok){
        renderLeaderboard(res.body.leaderboard);
        document.getElementById('da-entry').innerHTML = '<p class="feedback">Added to the leaderboard.</p>';
      } else {
        msg.textContent = res.body.error || 'Could not submit score.';
      }
    }).catch(function(){ msg.textContent = 'Could not submit score. Try again later.'; });
}

function startRun(){
  running = true;
  level = 1; songInLevel = 0; score = 0; usedIds = {};
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
