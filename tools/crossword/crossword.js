/* 1960smusic.net — reusable crossword player.
   Generic: takes any layout JSON of the shape produced by
   gen/build_crossword_layout.js (crossword-layout-generator output):
     { rows, cols, table: [[letter|"-", ...], ...],
       result: [{ answer, clue, startx, starty, orientation }, ...] }
   Mount into an empty container element; this builds the whole UI
   (grid, clue lists, controls, status line) inside it.
   No dependencies beyond the DOM. Reused across future crossword pages. */

var CrosswordPlayer = (function () {

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function buildNumbering(table, rows, cols) {
    var numberMap = {};
    var num = 0;
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        if (table[r][c] === '-') continue;
        var leftBlocked = (c === 0) || table[r][c - 1] === '-';
        var rightOpen = (c + 1 < cols) && table[r][c + 1] !== '-';
        var topBlocked = (r === 0) || table[r - 1][c] === '-';
        var bottomOpen = (r + 1 < rows) && table[r + 1][c] !== '-';
        var isAcrossStart = leftBlocked && rightOpen;
        var isDownStart = topBlocked && bottomOpen;
        if (isAcrossStart || isDownStart) {
          num += 1;
          numberMap[r + '_' + c] = num;
        }
      }
    }
    return numberMap;
  }

  function wordCells(w) {
    // crossword-layout-generator emits 1-indexed startx/starty; convert to
    // 0-indexed to match the table array.
    var r0 = w.starty - 1, c0 = w.startx - 1;
    var cells = [];
    for (var k = 0; k < w.answer.length; k++) {
      if (w.orientation === 'across') cells.push({ r: r0, c: c0 + k });
      else cells.push({ r: r0 + k, c: c0 });
    }
    return cells;
  }

  function mount(containerId, layoutUrl) {
    var container = document.getElementById(containerId);
    if (!container) return;
    fetch(layoutUrl).then(function (r) { return r.json(); }).then(function (layout) {
      init(container, layout);
    });
  }

  function init(container, layout) {
    var rows = layout.rows, cols = layout.cols, table = layout.table;
    var words = layout.result;
    var numberMap = buildNumbering(table, rows, cols);

    words.forEach(function (w) {
      w.number = numberMap[(w.starty - 1) + '_' + (w.startx - 1)];
    });

    var wordsAt = {};
    words.forEach(function (w) {
      wordCells(w).forEach(function (cell) {
        var key = cell.r + '_' + cell.c;
        if (!wordsAt[key]) wordsAt[key] = {};
        wordsAt[key][w.orientation] = w;
      });
    });

    var userGrid = [];
    for (var r = 0; r < rows; r++) {
      userGrid.push([]);
      for (var c = 0; c < cols; c++) userGrid[r].push('');
    }

    var state = { selR: -1, selC: -1, dir: 'across', revealed: false };

    var prefix = 'cw' + Math.random().toString(36).slice(2, 8);

    container.innerHTML =
      '<div class="cw-controls">' +
        '<button class="btn secondary" type="button" id="' + prefix + '-check">Check</button>' +
        '<button class="btn secondary" type="button" id="' + prefix + '-reveal">Reveal</button>' +
      '</div>' +
      '<p class="cw-status" id="' + prefix + '-status">Click a cell or a clue to start.</p>' +
      '<div class="cw-wrap">' +
        '<div class="cw-board">' +
          '<div class="cw-grid" id="' + prefix + '-grid" style="grid-template-columns:repeat(' + cols + ',1fr)"></div>' +
          '<input class="cw-hidden-input" id="' + prefix + '-input" type="text" autocapitalize="characters" autocomplete="off" autocorrect="off" spellcheck="false">' +
        '</div>' +
        '<div class="cw-clues">' +
          '<div class="cw-clue-col"><h3>Across</h3><ul class="cw-clue-list" id="' + prefix + '-across"></ul></div>' +
          '<div class="cw-clue-col"><h3>Down</h3><ul class="cw-clue-list" id="' + prefix + '-down"></ul></div>' +
        '</div>' +
      '</div>';

    var gridEl = document.getElementById(prefix + '-grid');
    var inputEl = document.getElementById(prefix + '-input');
    var statusEl = document.getElementById(prefix + '-status');
    var acrossEl = document.getElementById(prefix + '-across');
    var downEl = document.getElementById(prefix + '-down');

    var gridHtml = '';
    for (var ry = 0; ry < rows; ry++) {
      for (var cx = 0; cx < cols; cx++) {
        if (table[ry][cx] === '-') {
          gridHtml += '<div class="cw-cell cw-block" data-r="' + ry + '" data-c="' + cx + '"></div>';
        } else {
          var n = numberMap[ry + '_' + cx];
          gridHtml += '<div class="cw-cell" data-r="' + ry + '" data-c="' + cx + '">' +
            (n ? '<span class="cw-num">' + n + '</span>' : '') +
            '<span class="cw-letter"></span></div>';
        }
      }
    }
    gridEl.innerHTML = gridHtml;

    function cellEl(r, c) {
      return gridEl.querySelector('.cw-cell[data-r="' + r + '"][data-c="' + c + '"]');
    }

    var acrossWords = words.filter(function (w) { return w.orientation === 'across'; })
      .sort(function (a, b) { return a.number - b.number; });
    var downWords = words.filter(function (w) { return w.orientation === 'down'; })
      .sort(function (a, b) { return a.number - b.number; });

    acrossEl.innerHTML = acrossWords.map(function (w) {
      return '<li data-num="' + w.number + '" data-dir="across"><span class="cw-clue-num">' + w.number + '.</span> ' + esc(w.clue) + '</li>';
    }).join('');
    downEl.innerHTML = downWords.map(function (w) {
      return '<li data-num="' + w.number + '" data-dir="down"><span class="cw-clue-num">' + w.number + '.</span> ' + esc(w.clue) + '</li>';
    }).join('');

    function wordAt(r, c, dir) {
      var entry = wordsAt[r + '_' + c];
      return entry ? entry[dir] : null;
    }

    function clearHighlights() {
      var cells = gridEl.querySelectorAll('.cw-selected, .cw-in-word');
      cells.forEach(function (el) { el.classList.remove('cw-selected', 'cw-in-word'); });
      var clues = container.querySelectorAll('.cw-clue-list li.cw-active');
      clues.forEach(function (el) { el.classList.remove('cw-active'); });
    }

    function highlight(r, c, dir) {
      clearHighlights();
      var w = wordAt(r, c, dir);
      if (w) {
        wordCells(w).forEach(function (cell) {
          var el = cellEl(cell.r, cell.c);
          if (el) el.classList.add('cw-in-word');
        });
        var list = dir === 'across' ? acrossEl : downEl;
        var li = list.querySelector('li[data-num="' + w.number + '"]');
        if (li) {
          li.classList.add('cw-active');
          li.scrollIntoView({ block: 'nearest' });
        }
      }
      var sel = cellEl(r, c);
      if (sel) sel.classList.add('cw-selected');
    }

    function selectCell(r, c, forceDir, scroll) {
      if (r < 0 || r >= rows || c < 0 || c >= cols) return;
      if (table[r][c] === '-') return;
      var entry = wordsAt[r + '_' + c] || {};
      var dir = forceDir;
      if (!dir) {
        if (state.selR === r && state.selC === c && entry.across && entry.down) {
          dir = state.dir === 'across' ? 'down' : 'across';
        } else if (entry[state.dir]) {
          dir = state.dir;
        } else {
          dir = entry.across ? 'across' : 'down';
        }
      }
      state.selR = r; state.selC = c; state.dir = dir;
      highlight(r, c, dir);
      inputEl.value = '';
      inputEl.focus();
      if (scroll) {
        var el = cellEl(r, c);
        if (el) el.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      }
    }

    function setLetter(r, c, letter) {
      userGrid[r][c] = letter;
      var el = cellEl(r, c);
      if (el) {
        var span = el.querySelector('.cw-letter');
        if (span) span.textContent = letter;
        el.classList.remove('cw-wrong', 'cw-revealed');
      }
    }

    function nextCell(r, c, dir, delta) {
      var nr = r, nc = c;
      if (dir === 'across') nc += delta; else nr += delta;
      if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) return null;
      if (table[nr][nc] === '-') return null;
      return { r: nr, c: nc };
    }

    gridEl.addEventListener('click', function (e) {
      var cell = e.target.closest('.cw-cell');
      if (!cell || cell.classList.contains('cw-block')) return;
      selectCell(parseInt(cell.getAttribute('data-r'), 10), parseInt(cell.getAttribute('data-c'), 10));
    });

    container.addEventListener('click', function (e) {
      var li = e.target.closest('.cw-clue-list li');
      if (!li) return;
      var num = parseInt(li.getAttribute('data-num'), 10);
      var dir = li.getAttribute('data-dir');
      var w = words.filter(function (x) { return x.orientation === dir && x.number === num; })[0];
      if (w) selectCell(w.starty - 1, w.startx - 1, dir, true);
    });

    inputEl.addEventListener('input', function () {
      var raw = inputEl.value;
      inputEl.value = '';
      if (!raw) return;
      var ch = raw.charAt(raw.length - 1).toUpperCase();
      if (!/[A-Z]/.test(ch)) return;
      if (state.selR < 0) return;
      setLetter(state.selR, state.selC, ch);
      var next = nextCell(state.selR, state.selC, state.dir, 1);
      if (next) selectCell(next.r, next.c, state.dir);
      checkComplete();
    });

    inputEl.addEventListener('keydown', function (e) {
      if (state.selR < 0) return;
      var r = state.selR, c = state.selC;
      if (e.key === 'Backspace') {
        e.preventDefault();
        if (userGrid[r][c]) {
          setLetter(r, c, '');
        } else {
          var prev = nextCell(r, c, state.dir, -1);
          if (prev) {
            setLetter(prev.r, prev.c, '');
            selectCell(prev.r, prev.c, state.dir);
          }
        }
      } else if (e.key === 'ArrowRight') {
        e.preventDefault(); selectCell(r, c + 1, 'across');
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault(); selectCell(r, c - 1, 'across');
      } else if (e.key === 'ArrowDown') {
        e.preventDefault(); selectCell(r + 1, c, 'down');
      } else if (e.key === 'ArrowUp') {
        e.preventDefault(); selectCell(r - 1, c, 'down');
      }
    });

    function checkComplete() {
      for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
          if (table[r][c] === '-') continue;
          if (userGrid[r][c] !== table[r][c]) return false;
        }
      }
      statusEl.textContent = 'Solved! Every answer is correct.';
      statusEl.classList.add('cw-done');
      return true;
    }

    document.getElementById(prefix + '-check').addEventListener('click', function () {
      var allFilled = true;
      for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
          if (table[r][c] === '-') continue;
          var el = cellEl(r, c);
          if (!userGrid[r][c]) { allFilled = false; continue; }
          if (userGrid[r][c] !== table[r][c]) {
            el.classList.add('cw-wrong');
          } else {
            el.classList.remove('cw-wrong');
          }
        }
      }
      if (!checkComplete()) {
        statusEl.classList.remove('cw-done');
        statusEl.textContent = allFilled ? 'Some letters are wrong, marked in red.' : 'Checked so far. Keep filling in the grid.';
      }
    });

    document.getElementById(prefix + '-reveal').addEventListener('click', function () {
      state.revealed = true;
      for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
          if (table[r][c] === '-') continue;
          setLetter(r, c, table[r][c]);
          var el = cellEl(r, c);
          if (el) el.classList.add('cw-revealed');
        }
      }
      statusEl.classList.remove('cw-done');
      statusEl.textContent = 'Revealed. Here is the completed grid.';
    });
  }

  return { mount: mount };
})();
