/* 1960smusic.net — Daily Guessing Game: song pool loading + selection.
   Split out of daily-app.js to keep it under the house line-count ceiling. */

var GENRES = [
  'british-invasion', 'motown-soul', 'folk-rock', 'garage-surf-rock',
  'psychedelic-rock', 'country-60s', 'pop-brill-building', 'jazz-easy-listening'
];
var DEFAULT_HOOK_START = 15;
var ALL_SONGS = [];

function hookStart(song){
  return Number.isFinite(song.hook_start_seconds) ? song.hook_start_seconds : DEFAULT_HOOK_START;
}

function acceptedYears(song){
  var years = [song.year];
  if (Number.isFinite(song.year_alt)) years.push(song.year_alt);
  return years;
}

function loadExclusions(){
  return Promise.all([
    fetch('/data/daily-excluded-ids.json').then(function(r){ return r.json(); }).catch(function(){ return {}; }),
    fetch('/data/daily-manual-exclude.json').then(function(r){ return r.json(); }).catch(function(){ return {}; })
  ]).then(function(pair){ return Object.assign({}, pair[0], pair[1]); });
}

function loadAllSongs(){
  return Promise.all([
    Promise.all(GENRES.map(function(g){
      return fetch('/data/radio-eligible-' + g + '.json').then(function(r){ return r.json(); });
    })),
    loadExclusions()
  ]).then(function(res){
    var songs = [].concat.apply([], res[0]);
    var excluded = res[1];
    ALL_SONGS = songs.filter(function(s){ return !excluded[s.youtube_id]; });
  });
}

function pickTarget(usedIds){
  var pool = ALL_SONGS.filter(function(s){ return !usedIds[s.youtube_id]; });
  return randomPick(pool);
}

/* Distractor years: closest-to-correct 6 candidates, shuffled, take n --
   plausible without being predictable. */
function pickYearDistractors(accepted, n){
  var pool = [];
  for (var y = 1960; y <= 1969; y++){ if (accepted.indexOf(y) === -1) pool.push(y); }
  var primary = accepted[0];
  pool.sort(function(a, b){ return Math.abs(a - primary) - Math.abs(b - primary); });
  return shuffle(pool.slice(0, Math.max(n * 2, 6))).slice(0, n);
}
