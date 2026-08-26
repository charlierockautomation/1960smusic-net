// One-time script: reads data/crosswords/60s-music-crossword-source.json,
// runs crossword-layout-generator, writes data/crosswords/60s-music-crossword.json.
// Run with: node gen/build_crossword_layout.js
const fs = require('fs');
const path = require('path');
const CrosswordLayout = require('crossword-layout-generator');

const srcPath = path.join(__dirname, '..', 'data', 'crosswords', '60s-music-crossword-source.json');
const outPath = path.join(__dirname, '..', 'data', 'crosswords', '60s-music-crossword.json');

const source = JSON.parse(fs.readFileSync(srcPath, 'utf8'));
const inputWords = source.map(({ answer, clue }) => ({ answer, clue }));

const layout = CrosswordLayout.generateLayout(inputWords);

const placed = layout.result.filter(w => w.orientation !== 'none');
const dropped = layout.result.filter(w => w.orientation === 'none');

console.log('Input words:', inputWords.length);
console.log('Placed:', placed.length);
console.log('Dropped:', dropped.length);
if (dropped.length) {
  console.log('Dropped answers:', dropped.map(w => w.answer).join(', '));
}
console.log('Grid size:', layout.rows + ' x ' + layout.cols);

fs.writeFileSync(outPath, JSON.stringify(layout, null, 2));
console.log('Wrote', outPath);
