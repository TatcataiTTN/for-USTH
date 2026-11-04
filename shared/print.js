/* Printable exam paper: ?exam=midterm-A  (questions only)   ?exam=midterm-A&key=1  (with the answers and worked explanations) */
(function(){
'use strict';
var root = document.getElementById('paper'); if(!root) return;
var qs = {}; location.search.replace(/^\?/, '').split('&').forEach(function(p){ var a = p.split('='); if(a[0]) qs[decodeURIComponent(a[0])] = decodeURIComponent(a[1] || ''); });
var base = root.getAttribute('data-base'), key = qs.key === '1', LET = ['A', 'B', 'C', 'D'];
function el(t, c, h){ var e = document.createElement(t); if(c) e.className = c; if(h != null) e.innerHTML = h; return e; }
function txt(t, c, s){ var e = el(t, c); e.textContent = s; return e; }
Promise.all([fetch(base + 'bank.json').then(function(r){ return r.json(); }), fetch(base + 'meta.json').then(function(r){ return r.json(); })]).then(function(a){
  var by = {}; a[0].items.forEach(function(i){ by[i.id] = i; });
  var sets = [].concat(a[1].sets.midterm, a[1].sets.sprint, a[1].sets.final || [], a[1].sets.replica || []);
  var set = sets.filter(function(s){ return s.id === qs.exam; })[0];
  if(!set){ root.textContent = 'Unknown exam: ' + qs.exam; return; }
  root.innerHTML = '';
  var head = el('div', 'phead');
  head.appendChild(txt('h1', '', set.title)); document.title = set.title + (key ? ' (solutions)' : '') + ' · printable';
  head.appendChild(txt('p', 'pmeta', set.ids.length + ' questions · ' + set.minutes + ' minutes' + (set.forward_only ? ' · no going back' : '') + (key ? ' · SOLUTIONS' : '')));
  if(!key) head.appendChild(txt('p', 'pname', 'Name: ______________________    Date: ____________    Score: ____ / ' + set.ids.length));
  head.appendChild(txt('p', 'pnote', 'Choose one answer for each question. Calculators are allowed where the questions need numbers (3 significant figures).'));
  root.appendChild(head);
  set.ids.forEach(function(id, n){
    var q = by[id], box = el('div', 'pq');
    box.appendChild(txt('div', 'pqh', (n + 1) + '.  ' + (key ? '[' + q.topic + ' · level ' + q.level + ']' : '')));
    box.appendChild(txt('div', 'pqt', q.q));
    if(q.fig){ var f = el('div', 'pfig', q.fig); box.appendChild(f); }
    var ol = el('div', 'popts');
    q.opts.forEach(function(o, i){ var li = txt('div', 'po' + (key && i === q.correct ? ' good' : ''), LET[i] + '.  ' + o); ol.appendChild(li); });
    box.appendChild(ol);
    if(key){ box.appendChild(txt('div', 'pans', 'Answer: ' + LET[q.correct])); box.appendChild(txt('div', 'pexp', q.explain)); }
    root.appendChild(box);
  });
  if(!key){                                                    // a compact answer sheet at the end of the paper
    var sheet = el('div', 'psheet'); sheet.appendChild(txt('h2', '', 'Answer sheet'));
    var t = el('table'); var row = '<tr>' + set.ids.map(function(_, n){ return '<th>' + (n + 1) + '</th>'; }).join('') + '</tr><tr>' + set.ids.map(function(){ return '<td>&nbsp;</td>'; }).join('') + '</tr>';
    t.innerHTML = row; sheet.appendChild(t); root.appendChild(sheet);
  }
  if(window.renderMathInElement) renderMathInElement(root, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}], throwOnError: false});
  document.body.setAttribute('data-ready', '1');
}).catch(function(e){ root.textContent = 'Could not load the exam (' + e + ').'; });
})();
