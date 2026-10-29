/* Progress dashboard: reads the history written by quiz.js / bank.js from localStorage (nothing leaves the browser). */
(function(){
'use strict';
var U = window.USTM;
var root = document.getElementById('progress');
if(!root) return;
var base = root.getAttribute('data-base'), course = root.getAttribute('data-course');
U.json(base + 'meta.json').then(function(meta){
  var h = U.store.get(U.key(course, 'history'), []), qs = U.store.get(U.key(course, 'qstats'), {});
  root.innerHTML = '';
  if(!h.length && !Object.keys(qs).length){
    root.appendChild(U.el('p', 'muted', 'No attempts yet. Do a chapter quiz or a mock exam — your results, weak chapters and review list will appear here (stored only in this browser).'));
    return;
  }
  var tries = 0, ok = 0; Object.keys(qs).forEach(function(k){ tries += qs[k][0]; ok += qs[k][1]; });
  var line = U.el('div', 'stats');
  [['Questions answered', tries], ['Correct', ok + ' (' + U.pct(ok, tries) + '%)'], ['Quizzes / exams finished', h.length]].forEach(function(p){ var d = U.el('div', 'stat'); d.appendChild(U.el('b', null, String(p[1]))); d.appendChild(U.el('span', null, p[0])); line.appendChild(d); });
  root.appendChild(line);
  // accuracy per chapter from per-question statistics (needs the bank for chapter ids)
  U.json(base + 'bank.json').then(function(bank){
    var by = {}; bank.items.forEach(function(q){ var r = qs[q.id]; if(r){ by[q.ch] = by[q.ch] || [0, 0, {}]; by[q.ch][0] += r[0]; by[q.ch][1] += r[1]; var t = by[q.ch][2]; t[q.topic] = t[q.topic] || [0, 0]; t[q.topic][0] += r[0]; t[q.topic][1] += r[1]; } });
    var box = U.el('div', 'bars');
    meta.chapters.forEach(function(c){
      var r = by[c.id] || [0, 0], p = U.pct(r[1], r[0]); var row = U.el('div', 'barrow');
      row.appendChild(U.el('span', 'barl', c.id.toUpperCase().replace('C', 'Ch. ') + ' ' + c.title));
      var tr = U.el('span', 'bar'); var fill = U.el('span', 'fill ' + (r[0] === 0 ? 'none' : p >= 75 ? 'hi' : p >= 50 ? 'mid' : 'lo')); fill.style.width = (r[0] ? Math.max(p, 3) : 0) + '%'; tr.appendChild(fill); row.appendChild(tr);
      row.appendChild(U.el('span', 'barv', r[0] ? p + '% (' + r[1] + '/' + r[0] + ')' : 'not started')); box.appendChild(row);
    });
    root.appendChild(U.el('h3', null, 'Accuracy by chapter')); root.appendChild(box);
    var weak = [];
    Object.keys(by).forEach(function(c){ var t = by[c][2]; Object.keys(t).forEach(function(k){ if(t[k][0] >= 3 && t[k][1] / t[k][0] < 0.6) weak.push([c, k, t[k]]); }); });
    weak.sort(function(a, b){ return a[2][1] / a[2][0] - b[2][1] / b[2][0]; });
    if(weak.length){
      root.appendChild(U.el('h3', null, 'Topics to revisit (accuracy below 60%, at least 3 attempts)'));
      var ul = U.el('ul'); weak.slice(0, 8).forEach(function(w){ ul.appendChild(U.el('li', null, w[0].toUpperCase() + ' · ' + w[1] + ' — ' + U.pct(w[2][1], w[2][0]) + '% (' + w[2][1] + '/' + w[2][0] + ')')); }); root.appendChild(ul);
    }
  });
  root.appendChild(U.el('h3', null, 'Recent results'));
  var tb = U.el('table', 't'); var hr = U.el('tr'); ['When', 'Quiz / exam', 'Score', 'Time'].forEach(function(t){ hr.appendChild(U.el('th', null, t)); }); tb.appendChild(hr);
  h.slice(0, 8).forEach(function(e){ var tr = U.el('tr'); [new Date(e.t).toLocaleString(), e.title, e.score + '/' + e.total + ' (' + U.pct(e.score, e.total) + '%)', e.secs ? U.fmtTime(e.secs) : '–'].forEach(function(t){ tr.appendChild(U.el('td', null, String(t))); }); tb.appendChild(tr); });
  root.appendChild(tb);
  var reset = U.el('button', 'btn alt small', 'Reset my progress'); reset.onclick = function(){ if(confirm('Delete all saved results for this course from this browser?')){ U.store.del(U.key(course, 'history')); U.store.del(U.key(course, 'qstats')); location.reload(); } };
  root.appendChild(reset);
}).catch(function(e){ root.textContent = 'Progress unavailable: ' + e.message; });
})();
