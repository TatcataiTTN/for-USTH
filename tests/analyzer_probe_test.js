// Held-out test: the Moodle review questions (never used for mining) must land on the concept written down in probe_labels.json.
// usage: node tests/analyzer_probe_test.js [--verbose]
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const A = require(path.join(root, 'shared', 'analyzer-core.js'));
const data = JSON.parse(fs.readFileSync(path.join(root, 'concepts', 'data.json'), 'utf8'));
const model = A.compile(data.concepts);
const probes = JSON.parse(fs.readFileSync(path.join(__dirname, 'probe_questions.json'), 'utf8'));
const labels = JSON.parse(fs.readFileSync(path.join(__dirname, 'probe_labels.json'), 'utf8'));
const verbose = process.argv.includes('--verbose');
const T = {top3: 0.88, top3vi: 0.72};
let bad = 0;
function hit(res, subs) { return res.results.filter(r => !r.c.out).slice(0, 3).some(r => subs.some(s => r.c.name[0].toLowerCase().indexOf(s.toLowerCase()) >= 0)); }
for (const course of ['Linear-Algebra', 'Physics-1', 'Physics-2']) {
  const set = probes.filter(p => p.course === course);
  let n = 0, h = 0, hv = 0, h1 = 0, nv = 0; const miss = [];
  set.forEach(p => {
    const lab = labels[p.id]; if (!lab) { console.log('NO LABEL', p.id); bad++; return; }
    if (lab[0].indexOf('OUT:') === 0) {                      // must be flagged as outside the taught scope
      const r = A.analyze(model, p.en, {course: course});
      if (r.status !== 'out') { bad++; console.log('FAIL: not flagged outside scope:', p.id, r.status, r.results.slice(0, 2).map(x => x.c.name[0])); }
      return;
    }
    n++;
    const r = A.analyze(model, p.en, {course: course});
    if (hit(r, lab)) h++; else miss.push([p.id, lab[0], r.results.slice(0, 3).map(x => x.c.name[0].slice(0, 36)).join(' / '), r.status]);
    if (r.results.length && !r.results[0].c.out && lab.some(s => r.results[0].c.name[0].toLowerCase().indexOf(s.toLowerCase()) >= 0)) h1++;
    const rv = A.analyze(model, p.vi, {course: course}); nv++;
    if (hit(rv, lab)) hv++;
  });
  console.log(course, 'items', n, 'top1', (h1 / n).toFixed(3), 'top3', (h / n).toFixed(3), 'Vietnamese top3', (hv / nv).toFixed(3));
  if (h / n < T.top3) { bad++; console.log('FAIL top3', course); }
  if (hv / nv < T.top3vi) { bad++; console.log('FAIL Vietnamese top3', course); }
  if (verbose || miss.length) miss.forEach(m => console.log('   miss', m.join(' | ')));
}
process.exit(bad ? 1 : 0);
