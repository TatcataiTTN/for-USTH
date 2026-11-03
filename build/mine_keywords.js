// Mines distinctive terms of every concept from the practice-bank question stems (same tokeniser as the browser analyser).
// usage: node build/mine_keywords.js <concepts-topics.json>   -> prints {conceptId: [[stemmedTerm, weight], ...]}
const fs = require('fs'), path = require('path');
const A = require(path.join(__dirname, '..', 'shared', 'analyzer-core.js'));
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));          // [{id, course, ch, topics:[...]}]
const STOPX = new Set('the of to in on at by for with from and or is are was were be been it its this that these those as if then than so such into over under between what which who how when where why find calculate compute determine give gives given value values following select one answer correct question'.split(' '));
const courses = [...new Set(spec.map(c => c.course))];
const items = [];
for (const course of courses) {
  const f = path.join(__dirname, '..', course, 'data', 'bank.json');
  if (!fs.existsSync(f)) continue;
  JSON.parse(fs.readFileSync(f, 'utf8')).items.forEach(i => items.push({course, ch: i.ch, topic: i.topic, q: i.q}));
}
function terms(q) {
  const tk = A.tokens(q).filter(t => t.length >= 3 && !/^\d/.test(t) && !STOPX.has(t));
  const set = new Set(tk);
  const all = A.tokens(q);
  for (let i = 0; i + 1 < all.length; i++) {
    const a = all[i], b = all[i + 1];
    if (a.length >= 3 && b.length >= 3 && !/^\d/.test(a) && !/^\d/.test(b) && !STOPX.has(a) && !STOPX.has(b)) set.add(a + ' ' + b);
  }
  return set;
}
const docs = items.map(i => ({course: i.course, ch: i.ch, topic: i.topic, t: terms(i.q)}));
const df = {};
docs.forEach(d => d.t.forEach(t => { df[t] = (df[t] || 0) + 1; }));
const N = docs.length, out = {};
spec.forEach(c => {
  const D = docs.filter(d => d.course === c.course && d.ch === c.ch && c.topics.indexOf(d.topic) >= 0);
  if (D.length < 3) { out[c.id] = []; return; }
  const cnt = {};
  D.forEach(d => d.t.forEach(t => { cnt[t] = (cnt[t] || 0) + 1; }));
  const sc = [];
  Object.keys(cnt).forEach(t => {
    const frac = cnt[t] / D.length;
    if (cnt[t] >= 2 && frac >= 0.04) sc.push([t, frac * Math.log(N / df[t])]);
  });
  sc.sort((a, b) => b[1] - a[1]);
  const uni = sc.filter(x => x[0].indexOf(' ') < 0).slice(0, 22), bi = sc.filter(x => x[0].indexOf(' ') >= 0).slice(0, 10);
  const pick = uni.concat(bi), mx = Math.max.apply(null, pick.map(x => x[1]).concat([1e-9]));
  out[c.id] = pick.map(x => [x[0], Math.round((0.5 + 1.2 * x[1] / mx) * 100) / 100]);
});
process.stdout.write(JSON.stringify(out));
