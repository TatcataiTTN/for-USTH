/* Written papers: hub + paper page.
   study mode : statement, then "Show answer" / "Show full solution" for every part, plus a link that opens the lab with the data of the part
   exam mode  : countdown (120 min), statements only (answers stay hidden), scratch notes; at the end every part is shown with its model solution
                and a self-marking selector (0 … marks, step 0.5); the total out of 20 is saved to the progress dashboard                         */
(function(){
'use strict';
var U = window.USTM;
var hub = document.getElementById('written-hub'), page = document.getElementById('written');
if(!hub && !page) return;
var host = hub || page, base = host.getAttribute('data-base'), course = host.getAttribute('data-course'), labBase = host.getAttribute('data-lab');
var TOOLMAP = {rref: 'rank'};

function total(p){ var t = 0; p.problems.forEach(function(q){ q.forEach(function(pt){ t += pt.marks; }); }); return t; }
function title(p){ return p.year + (p.shift ? ' · ' + p.shift : ''); }
function labLink(lab){
  if(!lab || !lab.tool) return null;
  var parts = ['tool=' + (TOOLMAP[lab.tool] || lab.tool)];
  Object.keys(lab).forEach(function(k){ if(k === 'tool') return; var v = lab[k]; if(v === '' || v === null) return; parts.push(k + '=' + encodeURIComponent(typeof v === 'string' ? v : JSON.stringify(v))); });
  return labBase + '#' + parts.join('&');
}
function fmt(n){ return (Math.round(n * 2) / 2).toString(); }

U.json(base + 'papers.json').then(function(papers){ hub ? renderHub(papers) : renderPaper(papers); })
  .catch(function(e){ host.textContent = 'Could not load the papers: ' + e.message; });

/* ------------------------------------------------------------------ hub */
function renderHub(papers){
  hub.innerHTML = '';
  var hist = U.store.get(U.key(course, 'history'), []);
  papers.forEach(function(p){
    var best = null;
    hist.forEach(function(h){ if(h.id === 'written:' + p.id && (best === null || h.score > best)) best = h.score; });
    var c = U.el('div', 'panel');
    c.appendChild(U.el('h3', null, title(p)));
    var info = [p.date, p.minutes + ' min', p.calc, p.problems.length + ' problems · ' + fmt(total(p)) + ' marks'].filter(Boolean).join(' · ');
    c.appendChild(U.el('p', 'muted', info));
    if(p.note) c.appendChild(U.el('p', 'muted', p.note));
    var topics = p.problems.map(function(q, i){ return 'P' + (i + 1) + ': ' + q.length + ' part' + (q.length > 1 ? 's' : ''); }).join(' · ');
    c.appendChild(U.el('p', 'small', topics));
    var row = U.el('div', 'row');
    var a1 = U.el('a', 'btn', '📖 Study with solutions'); a1.href = 'paper.html?p=' + encodeURIComponent(p.id);
    var a2 = U.el('a', 'btn alt', '⏱ Take it as an exam'); a2.href = 'paper.html?p=' + encodeURIComponent(p.id) + '&mode=exam';
    row.appendChild(a1); row.appendChild(a2);
    if(best !== null) row.appendChild(U.el('span', 'tag okt', 'best self-mark ' + fmt(best) + ' / ' + fmt(total(p))));
    c.appendChild(row); hub.appendChild(c);
  });
}

/* ------------------------------------------------------------------ paper page */
function renderPaper(papers){
  var qp = new URLSearchParams(location.search), id = qp.get('p'), mode = qp.get('mode') === 'exam' ? 'exam' : 'study';
  var P = papers.filter(function(p){ return p.id === id; })[0];
  if(!P){ page.innerHTML = ''; var d = U.el('div', 'callout bad'); d.appendChild(document.createTextNode('Unknown paper. ')); var a = U.el('a', null, 'Back to the list'); a.href = './'; d.appendChild(a); page.appendChild(d); return; }
  document.title = title(P) + ' · ' + document.title;
  if(mode === 'exam') examFlow(P); else study(P);
}

function head(P, mode){
  var h = U.el('div'); h.appendChild(U.el('h1', null, title(P)));
  h.appendChild(U.el('p', 'muted', [P.date, P.minutes + ' minutes', P.calc, fmt(total(P)) + ' marks'].filter(Boolean).join(' · ') + (P.note ? ' — ' + P.note : '')));
  var sw = U.el('p'); var other = U.el('a', 'btn small alt', mode === 'exam' ? '📖 Switch to study mode' : '⏱ Take it as an exam'); other.href = 'paper.html?p=' + encodeURIComponent(P.id) + (mode === 'exam' ? '' : '&mode=exam'); sw.appendChild(other);
  var back = U.el('a', 'btn small alt', '◀ All papers'); back.href = './'; sw.appendChild(back); h.appendChild(sw); return h;
}
function partStatement(pt, nameTxt){
  var b = U.el('div', 'part'); var tx = U.el('div', 'ptxt'); tx.textContent = nameTxt + pt.text; b.appendChild(tx);
  b.appendChild(U.el('span', 'marks', '[' + fmt(pt.marks) + ' mark' + (pt.marks === 1 ? '' : 's') + ']')); return b;
}
function names(P){ var out = []; P.problems.forEach(function(q, i){ q.forEach(function(pt, j){ out.push(q.length > 1 ? (i + 1) + '.' + (j + 1) + ' ' : (i + 1) + '. '); }); }); return out; }

function study(P){
  page.innerHTML = ''; page.appendChild(head(P, 'study'));
  var nm = names(P), k = 0;
  P.problems.forEach(function(q, i){
    var box = U.el('div', 'panel'); var sum = q.reduce(function(s, pt){ return s + pt.marks; }, 0);
    box.appendChild(U.el('h2', null, 'Problem ' + (i + 1) + ' (' + fmt(sum) + ' marks)')); box.firstChild.style.marginTop = '0';
    q.forEach(function(pt){
      var b = partStatement(pt, nm[k++]);
      var row = U.el('div', 'row');
      var ans = U.el('div', 'callout good hide'); ans.innerHTML = '<b>Answer.</b> ' + pt.answer;
      var sol = U.el('div', 'explain hide'); sol.innerHTML = pt.solution;
      var b1 = U.el('button', 'btn alt small', '✔ Show the answer'); b1.type = 'button';
      var b2 = U.el('button', 'btn alt small', '📝 Show the full solution'); b2.type = 'button';
      b1.onclick = function(){ ans.classList.toggle('hide'); b1.textContent = ans.classList.contains('hide') ? '✔ Show the answer' : 'Hide the answer'; U.math(ans); };
      b2.onclick = function(){ sol.classList.toggle('hide'); sol.classList.toggle('show'); b2.textContent = sol.classList.contains('hide') ? '📝 Show the full solution' : 'Hide the solution'; U.math(sol); };
      row.appendChild(b1); row.appendChild(b2);
      var ll = labLink(pt.lab); if(ll){ var a = U.el('a', 'btn alt small', '🧮 Check in the lab'); a.href = ll; row.appendChild(a); }
      b.appendChild(row); b.appendChild(ans); b.appendChild(sol); box.appendChild(b);
    });
    page.appendChild(box);
  });
  var tip = U.el('div', 'callout'); tip.innerHTML = '<b>How to use this page.</b> Cover the solution, solve on paper first, then open the answer and compare your <i>method</i>, not only the number. For the real exam also practise the presentation: state the method, show every row operation / substitution, and check the result.';
  page.appendChild(tip); U.math(page);
}

function examFlow(P){
  var key = U.key(course, 'notes:' + P.id), notes = U.store.get(key, {});
  var secs = P.minutes * 60, t0 = null, timer = null, finished = false;
  page.innerHTML = ''; page.appendChild(head(P, 'exam'));
  var intro = U.el('div', 'panel');
  var ul = U.el('ul'); ['Duration: ' + P.minutes + ' minutes. ' + P.calc + '. No notes, no books.', 'Work on paper, show your work with detailed calculations and arguments (as the exam instructs). The page only shows the statements; use the box under each problem for short notes if you like.',
    'When you finish (or time is up) the model solutions appear and you mark yourself part by part. Be strict: a correct number without the method earns only part of the marks.'].forEach(function(t){ ul.appendChild(U.el('li', null, t)); });
  intro.appendChild(ul); var go = U.el('button', 'btn', '▶ Start the exam'); intro.appendChild(go); page.appendChild(intro);
  go.onclick = function(){ begin(); };

  function begin(){
    page.innerHTML = ''; page.appendChild(head(P, 'exam')); t0 = Date.now();
    var bar = U.el('div', 'exambar'), tl = U.el('span', 'timer'), pg = U.el('span', 'prog', fmt(total(P)) + ' marks'), bf = U.el('button', 'btn small alt', 'Finish and mark');
    bar.appendChild(pg); bar.appendChild(tl); bar.appendChild(bf); page.appendChild(bar);
    var nm = names(P), k = 0;
    P.problems.forEach(function(q, i){
      var box = U.el('div', 'panel'); var sum = q.reduce(function(s, pt){ return s + pt.marks; }, 0);
      box.appendChild(U.el('h2', null, 'Problem ' + (i + 1) + ' (' + fmt(sum) + ' marks)')); box.firstChild.style.marginTop = '0';
      q.forEach(function(pt){ box.appendChild(partStatement(pt, nm[k++])); });
      var ta = U.el('textarea'); ta.rows = 3; ta.placeholder = 'Scratch notes for problem ' + (i + 1) + ' (optional, kept in this browser)'; ta.style.width = '100%'; ta.value = notes['p' + i] || '';
      ta.oninput = function(){ notes['p' + i] = ta.value; U.store.set(key, notes); }; box.appendChild(ta); page.appendChild(box);
    });
    U.math(page);
    function tick(){ var left = Math.max(0, secs - Math.round((Date.now() - t0) / 1000)); tl.textContent = '⏱ ' + U.fmtTime(left); tl.className = 'timer' + (left < 300 ? ' low' : ''); if(left <= 0) finish(true); }
    timer = setInterval(tick, 500); tick();
    bf.onclick = function(){ if(confirm('Finish the exam now and see the solutions?')) finish(false); };
    function finish(auto){ if(finished) return; finished = true; clearInterval(timer); mark(auto, Math.min(secs, Math.round((Date.now() - t0) / 1000))); }
  }

  function mark(auto, used){
    page.innerHTML = ''; page.appendChild(head(P, 'exam'));
    var top = U.el('div', 'panel'); top.appendChild(U.el('h2', null, (auto ? '⏱ Time is up — ' : '') + 'Self-marking'));
    top.firstChild.style.marginTop = '0';
    top.appendChild(U.el('p', null, 'Time used: ' + U.fmtTime(used) + ' of ' + P.minutes + ':00. Compare each part with the model solution and give yourself marks (0 to the maximum, steps of 0.5).'));
    var sc = U.el('div', 'bigscore', '0 / ' + fmt(total(P))); top.appendChild(sc);
    var save = U.el('button', 'btn', 'Save my result'), msg = U.el('span', 'muted'); top.appendChild(save); top.appendChild(msg); page.appendChild(top);
    var sels = [], nm = names(P), k = 0;
    function upd(){ var s = 0; sels.forEach(function(x){ s += parseFloat(x.value); }); sc.textContent = fmt(s) + ' / ' + fmt(total(P)) + '  (' + (s / total(P) * 20).toFixed(1) + ' / 20)'; return s; }
    P.problems.forEach(function(q, i){
      var box = U.el('div', 'panel'); box.appendChild(U.el('h2', null, 'Problem ' + (i + 1))); box.firstChild.style.marginTop = '0';
      q.forEach(function(pt){
        var b = partStatement(pt, nm[k++]);
        var ans = U.el('div', 'callout good'); ans.innerHTML = '<b>Answer.</b> ' + pt.answer; b.appendChild(ans);
        var d = document.createElement('details'); d.className = 'sol'; var s = document.createElement('summary'); s.textContent = 'Full solution'; d.appendChild(s); var inner = U.el('div'); inner.innerHTML = pt.solution; d.appendChild(inner); b.appendChild(d);
        var row = U.el('div', 'row'); var lab = U.el('label', null, 'My marks: '); var sel = U.el('select');
        for(var m = 0; m <= pt.marks + 1e-9; m += 0.5){ var o = U.el('option', null, fmt(m) + ' / ' + fmt(pt.marks)); o.value = String(m); sel.appendChild(o); }
        sel.onchange = upd; sels.push(sel); lab.appendChild(sel); row.appendChild(lab); var ll = labLink(pt.lab); if(ll){ var a = U.el('a', 'btn alt small', '🧮 Check in the lab'); a.href = ll; row.appendChild(a); } b.appendChild(row); box.appendChild(b);
      });
      page.appendChild(box);
    });
    upd();
    save.onclick = function(){
      var s = upd(); U.record(course, {t: Date.now(), id: 'written:' + P.id, title: 'Written · ' + title(P), mode: 'written', score: s, total: total(P), secs: used, wrong: []});
      msg.textContent = ' Saved: ' + fmt(s) + ' / ' + fmt(total(P)) + '. It will appear in the progress panel on the home page.'; save.disabled = true;
    };
    U.math(page); window.scrollTo(0, 0);
  }
}
})();
