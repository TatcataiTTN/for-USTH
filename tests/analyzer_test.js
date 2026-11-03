// Coverage of the keyword system: every practice-bank question is analysed and the concept that owns its topic must be among the best matches.
// usage: node tests/analyzer_test.js [--verbose]    (exit code 1 when a threshold is missed)
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const A = require(path.join(root, 'shared', 'analyzer-core.js'));
const data = JSON.parse(fs.readFileSync(path.join(root, 'concepts', 'data.json'), 'utf8'));
const model = A.compile(data.concepts);
const verbose = process.argv.includes('--verbose');
let bad = 0;
const THRESH = {top1: 0.62, top3: 0.88, none: 0.04, cross: 0.04};      // minimum top-1 / top-3 hit rate within the course, maximum share of unmatched / cross-course answers
const rows = [];
for (const course of Object.keys(data.courses)) {
  const f = path.join(root, course, 'data', 'bank.json'); if (!fs.existsSync(f)) continue;
  const items = JSON.parse(fs.readFileSync(f, 'utf8')).items;
  let t1 = 0, t3 = 0, none = 0, cross = 0, outn = 0, miss = [];
  items.forEach(it => {
    const own = data.concepts.filter(c => c.course === course && c.ch === it.ch && c.topics.indexOf(it.topic) >= 0).map(c => c.id);
    const r = A.analyze(model, it.q, {course: course});
    const ids = r.results.filter(x => !x.c.out).map(x => x.c.id);
    if (r.status === 'none') none++;
    if (r.status === 'out') outn++;
    if (own.indexOf(ids[0]) >= 0) t1++;
    if (ids.slice(0, 3).some(i => own.indexOf(i) >= 0)) t3++; else if (miss.length < 400) miss.push([it.id, it.topic, it.q.slice(0, 110), ids.slice(0, 2).map(i => data.concepts.find(c => c.id === i).name[0])]);
    const g = A.analyze(model, it.q, {course: 'all'});
    if (g.results.length && g.results[0].c.course !== course && g.status !== 'none') cross++;
  });
  const n = items.length;
  rows.push([course, n, (t1 / n).toFixed(3), (t3 / n).toFixed(3), (none / n).toFixed(3), (cross / n).toFixed(3), (outn / n).toFixed(3)]);
  if (outn / n > 0.01) { bad++; console.log('FAIL: in-scope questions flagged as out of scope', course, (outn / n).toFixed(3)); }
  if (t1 / n < THRESH.top1) { bad++; console.log('FAIL top-1', course, (t1 / n).toFixed(3)); }
  if (t3 / n < THRESH.top3) { bad++; console.log('FAIL top-3', course, (t3 / n).toFixed(3)); }
  if (none / n > THRESH.none) { bad++; console.log('FAIL unmatched', course, (none / n).toFixed(3)); }
  if (cross / n > THRESH.cross) { bad++; console.log('FAIL cross-course', course, (cross / n).toFixed(3)); }
  if (verbose) { console.log('--- misses in', course); miss.slice(0, 40).forEach(m => console.log(' ', m[0], '|', m[1], '|', m[2], '=>', m[3].join(' / '))); }
}
console.log('course\tn\ttop1\ttop3\tunmatched\tcross-course\tflagged-out');
rows.forEach(r => console.log(r.join('\t')));
process.exit(bad ? 1 : 0);
