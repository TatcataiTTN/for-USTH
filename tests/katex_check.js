// Validate every $...$ / $$...$$ segment of both banks (stems, options, explanations) and the LA past papers with KaTeX (throwOnError).
const fs = require('fs'), path = require('path');
const katex = require(path.join(__dirname, '..', 'shared', 'vendor', 'katex', 'katex.min.js'));
function segments(s){
  const out = []; let i = 0;
  while(i < s.length){
    if(s.startsWith('$$', i)){ const j = s.indexOf('$$', i + 2); if(j < 0){ out.push({err: 'unterminated $$', text: s.slice(i, i + 40)}); break; } out.push({tex: s.slice(i + 2, j), display: true}); i = j + 2; }
    else if(s[i] === '$'){ const j = s.indexOf('$', i + 1); if(j < 0){ out.push({err: 'unterminated $', text: s.slice(i, i + 40)}); break; } out.push({tex: s.slice(i + 1, j), display: false}); i = j + 1; }
    else i++;
  }
  return out;
}
// answer / solution are inserted with innerHTML, so the browser decodes these entities before KaTeX sees the text
const dec = s => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
let bad = 0, total = 0;
function check(where, s){
  segments(String(s)).forEach(seg => {
    total++;
    if(seg.err){ bad++; console.log('BAD', where, seg.err, seg.text); return; }
    try{ katex.renderToString(seg.tex, {throwOnError: true, displayMode: seg.display}); }
    catch(e){ bad++; console.log('BAD', where, e.message.slice(0, 100), '|', seg.tex.slice(0, 70)); }
  });
}
for(const course of ['Calculus-1', 'Linear-Algebra', 'Physics-1', 'Physics-2'].filter(c => fs.existsSync(path.join(__dirname, '..', c, 'data', 'bank.json')))){
  const b = JSON.parse(fs.readFileSync(path.join(__dirname, '..', course, 'data', 'bank.json'), 'utf8'));
  b.items.forEach(q => { check(q.id + ' stem', q.q); q.opts.forEach((o, i) => check(q.id + ' opt' + i, o)); check(q.id + ' explain', q.explain);
    if(new Set(q.opts).size !== 4) { bad++; console.log('BAD duplicate options', q.id); }
    if(q.fig !== undefined && !(/^<svg[^>]*>[\s\S]*<\/svg>$/.test(q.fig) && !/<script|onload|onclick|javascript:/i.test(q.fig))) { bad++; console.log('BAD figure markup', q.id); }
    if(!(q.correct >= 0 && q.correct < 4)) { bad++; console.log('BAD correct index', q.id); } });
  const pp = path.join(__dirname, '..', course, 'data', 'papers.json');
  if(fs.existsSync(pp)){
    JSON.parse(fs.readFileSync(pp, 'utf8')).forEach(p => p.problems.forEach((q, qi) => q.forEach((pt, pi) => { const w = p.id + ' Q' + (qi + 1) + '.' + (pi + 1); check(w + ' text', pt.text); check(w + ' answer', dec(pt.answer)); check(w + ' solution', dec(pt.solution)); })));
  }
  const nn = path.join(__dirname, '..', course, 'data', 'notes.json');
  if(fs.existsSync(nn)) JSON.parse(fs.readFileSync(nn, 'utf8')).forEach(n => check('note ' + n.src, n.note));
}
console.log(`checked ${total} math segments, ${bad} problems`);
process.exit(bad ? 1 : 0);
