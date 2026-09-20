/* 1960smusic.net — Daily Guessing Game: Workers KV top-5 leaderboard.
   Split out of daily-app.js to keep it under the house line-count ceiling. */

function esc(s){ return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }

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
