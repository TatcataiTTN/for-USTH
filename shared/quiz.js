/* Quiz / exam runner.
   practice mode  : every question visible, instant feedback + explanation, retry buttons (chapter quizzes)
   exam mode      : one question per screen, countdown, optional forward-only navigation (Moodle style), review at the end
   URL examples   : run.html?set=c3-B        (chapter quiz)
                    run.html?exam=midterm-A  (20 questions, 50 min, no going back)
                    run.html?exam=sprint-random (30 random questions, 20 min)
                    run.html?exam=custom&ch=c1,c2&n=15&min=20&fwd=1                                              */
(function(){
'use strict';
var U = window.USTM;
var root = document.getElementById('runner');
if(!root) return;
var base = root.getAttribute('data-base');
var course = root.getAttribute('data-course');
var LETTERS = 'ABCD';

function fail(msg){ root.innerHTML = ''; var d = U.el('div', 'callout bad'); d.appendChild(U.el('b', null, 'Could not start: ')); d.appendChild(document.createTextNode(msg)); root.appendChild(d); }

Promise.all([U.json(base + 'bank.json'), U.json(base + 'meta.json')]).then(function(res){
  var bank = res[0], meta = res[1];
  var byId = {}; bank.items.forEach(function(q){ byId[q.id] = q; });
  var cfg;
  try{ cfg = resolve(new URLSearchParams(location.search), meta, bank, byId); }catch(e){ return fail(e.message); }
  if(cfg.mode === 'exam') runExam(cfg, meta); else runPractice(cfg, meta);
}).catch(function(e){ fail(String(e.message || e)); });

/* ------------------------------------------------------------------ configuration */
function findSet(list, id){ return list.filter(function(s){ return s.id === id; })[0]; }
function drawQuota(bank, quota, rnd){
  var out = [];
  Object.keys(quota).forEach(function(ch){
    var pool = U.shuffle(bank.items.filter(function(q){ return q.ch === ch && (q.tags || []).indexOf('extension') < 0; }), rnd);
    out = out.concat(pool.slice(0, quota[ch]));
  });
  return U.shuffle(out, rnd);
}
function resolve(p, meta, bank, byId){
  var seed = parseInt(p.get('seed') || String(Date.now() % 1e9), 10);
  var rnd = U.mulberry32(seed);
  var mk = function(ids){ return ids.map(function(i){ return byId[i]; }).filter(Boolean); };
  if(p.get('set')){
    var id = p.get('set'), ch = id.split('-')[0];
    var s = findSet(meta.sets.chapter[ch] || [], id);
    if(!s) throw new Error('Unknown quiz set "' + id + '".');
    return {mode: 'practice', title: s.title, key: id, items: mk(s.ids), minutes: null};
  }
  var ex = p.get('exam');
  if(!ex) throw new Error('No quiz or exam was selected.');
  var all = meta.sets.midterm.concat(meta.sets.sprint);
  var s2 = findSet(all, ex);
  if(s2) return {mode: 'exam', title: s2.title, key: ex, items: mk(s2.ids), minutes: s2.minutes, forward: !!s2.forward_only};
  if(ex === 'sprint-random')
    return {mode: 'exam', title: 'Speed exam · random 30 questions in 20 minutes', key: ex, items: drawQuota(bank, meta.sprint_quota, rnd), minutes: 20, forward: false};
  if(ex === 'midterm-random')
    return {mode: 'exam', title: meta.midterm_title + ' · random', key: ex, items: drawQuota(bank, meta.midterm_quota, rnd), minutes: meta.midterm_minutes, forward: true};
  if(ex === 'custom'){
    var chs = (p.get('ch') || '').split(',').filter(Boolean), n = Math.max(1, Math.min(60, parseInt(p.get('n') || '15', 10)));
    var pool = U.shuffle(bank.items.filter(function(q){ return (!chs.length || chs.indexOf(q.ch) >= 0) && (q.tags || []).indexOf('extension') < 0; }), rnd).slice(0, n);
    if(!pool.length) throw new Error('No question matches this selection.');
    return {mode: 'exam', title: 'Custom exam (' + pool.length + ' questions)', key: 'custom', items: pool, minutes: Math.max(1, parseInt(p.get('min') || String(Math.ceil(pool.length * 0.67)), 10)), forward: p.get('fwd') === '1'};
  }
  throw new Error('Unknown exam "' + ex + '".');
}

/* ------------------------------------------------------------------ shared rendering */
function questionCard(q, idx, total){
  var box = U.el('div', 'qitem'); box.setAttribute('data-id', q.id);
  var head = U.el('div', 'qhead');
  head.appendChild(U.el('span', 'tag', (idx !== undefined ? 'Q' + (idx + 1) + (total ? '/' + total : '') + ' · ' : '') + q.topic));
  head.appendChild(U.el('span', 'tag lv' + q.level, 'level ' + q.level));
  box.appendChild(head);
  box.appendChild(U.el('div', 'qtxt', q.q));
  return box;
}
function optButtons(q, box, onPick){
  var btns = q.opts.map(function(o, i){
    var b = U.el('button', 'opt'); b.type = 'button';
    b.appendChild(U.el('span', 'optl', LETTERS[i] + '.')); b.appendChild(U.el('span', 'optt', o));
    b.onclick = function(){ onPick(i, b); }; box.appendChild(b); return b;
  });
  return btns;
}
function sourceLine(q){
  return U.el('div', 'qsrc', U.srcLabel(q));
}

/* ------------------------------------------------------------------ practice mode */
function runPractice(cfg, meta){
  var items = cfg.items, st = {ans: {}, done: false};
  var sk = U.key(course, 'practice:' + cfg.key);
  root.innerHTML = '';
  var bar = U.el('div', 'panel');
  var h = U.el('h2', null, cfg.title); bar.appendChild(h);
  var score = U.el('div', 'score'); bar.appendChild(score);
  var row = U.el('div', 'row');
  var bFin = U.el('button', 'btn', 'Finish and save result'); var bRe = U.el('button', 'btn alt', '↺ Restart this quiz'); var bWrong = U.el('button', 'btn alt', 'Redo only the mistakes');
  bWrong.style.display = 'none'; row.appendChild(bFin); row.appendChild(bWrong); row.appendChild(bRe); bar.appendChild(row);
  root.appendChild(bar);
  var list = U.el('div'); root.appendChild(list);
  var result = U.el('div'); root.appendChild(result);
  function refresh(){
    var a = Object.keys(st.ans).length, c = items.filter(function(q){ return st.ans[q.id] === q.correct; }).length;
    score.textContent = 'Answered ' + a + '/' + items.length + ' · correct ' + c + (a ? ' · ' + U.pct(c, a) + '%' : '');
    bWrong.style.display = (a && c < a) ? '' : 'none';
  }
  function build(subset){
    list.innerHTML = ''; result.innerHTML = '';
    subset.forEach(function(q, i){
      var box = questionCard(q, i, subset.length);
      var ex = U.el('div', 'explain');
      var btns = optButtons(q, box, function(pick, b){
        if(st.ans[q.id] !== undefined) return;
        st.ans[q.id] = pick; U.qstat(course, q.id, pick === q.correct);
        btns.forEach(function(x, k){ x.disabled = true; if(k === q.correct) x.classList.add('correct'); });
        if(pick !== q.correct) b.classList.add('wrong');
        ex.innerHTML = ''; ex.appendChild(U.el('b', null, pick === q.correct ? '✅ Correct. ' : '❌ The answer is ' + LETTERS[q.correct] + '. '));
        ex.appendChild(document.createTextNode(q.explain)); ex.classList.add('show'); U.math(ex); refresh();
      });
      box.appendChild(ex); box.appendChild(sourceLine(q));
      var retry = U.el('button', 'btn alt small', '↺ Try this question again'); retry.type = 'button';
      retry.onclick = function(){ delete st.ans[q.id]; build(subset); refresh(); };
      box.appendChild(retry); list.appendChild(box);
    });
    U.math(list); refresh();
  }
  bRe.onclick = function(){ st.ans = {}; build(items); window.scrollTo(0, 0); };
  bWrong.onclick = function(){ var w = items.filter(function(q){ return st.ans[q.id] !== undefined && st.ans[q.id] !== q.correct; }); w.forEach(function(q){ delete st.ans[q.id]; }); build(w); window.scrollTo(0, 0); };
  bFin.onclick = function(){
    var c = items.filter(function(q){ return st.ans[q.id] === q.correct; }).length;
    var wrong = items.filter(function(q){ return st.ans[q.id] !== q.correct; }).map(function(q){ return q.id; });
    U.record(course, {t: Date.now(), id: cfg.key, title: cfg.title, mode: 'practice', score: c, total: items.length, secs: 0, wrong: wrong});
    result.innerHTML = ''; var d = U.el('div', 'callout good'); d.appendChild(U.el('b', null, 'Saved. '));
    d.appendChild(document.createTextNode('Score ' + c + '/' + items.length + ' (' + U.pct(c, items.length) + '%). Unanswered questions count as wrong.')); result.appendChild(d);
    d.scrollIntoView({behavior: 'smooth', block: 'center'});
  };
  build(items);
}

/* ------------------------------------------------------------------ exam mode */
function runExam(cfg, meta){
  var items = cfg.items, n = items.length;
  var st = {i: 0, ans: new Array(n).fill(null), left: cfg.minutes * 60, t0: Date.now(), finished: false, tq: new Array(n).fill(0), tstart: Date.now()};
  var timer = null;
  root.innerHTML = '';
  var intro = U.el('div', 'panel');
  intro.appendChild(U.el('h2', null, cfg.title));
  var ul = U.el('ul');
  [n + ' multiple-choice questions · ' + cfg.minutes + ' minutes (about ' + Math.round(cfg.minutes * 60 / n) + ' s per question)',
   cfg.forward ? 'You cannot return to previous questions (like the Moodle mock): choose carefully, then press Next.' : 'You may move freely between questions and change answers before you submit.',
   'No feedback is shown until you finish; unanswered questions score 0. Calculators are not needed for these questions.'].forEach(function(t){ ul.appendChild(U.el('li', null, t)); });
  intro.appendChild(ul);
  var go = U.el('button', 'btn', '▶ Start the exam'); intro.appendChild(go); root.appendChild(intro);
  go.onclick = function(){ begin(); };

  function begin(){
    root.innerHTML = '';
    var top = U.el('div', 'exambar');
    var tl = U.el('span', 'timer'); var pg = U.el('span', 'prog'); var bfin = U.el('button', 'btn small alt', 'Finish now');
    top.appendChild(pg); top.appendChild(tl); top.appendChild(bfin); root.appendChild(top);
    var body = U.el('div'); root.appendChild(body);
    var nav = U.el('div', 'row');
    var bprev = U.el('button', 'btn alt', '◀ Previous'), bnext = U.el('button', 'btn', 'Next ▶');
    if(!cfg.forward) nav.appendChild(bprev); nav.appendChild(bnext); root.appendChild(nav);
    var pal = U.el('div', 'palette'); if(!cfg.forward) root.appendChild(pal);
    function tick(){
      st.left = Math.max(0, cfg.minutes * 60 - Math.round((Date.now() - st.t0) / 1000));
      tl.textContent = '⏱ ' + U.fmtTime(st.left); tl.className = 'timer' + (st.left < 60 ? ' low' : '');
      if(st.left <= 0) finish(true);
    }
    function show(){
      body.innerHTML = '';
      var q = items[st.i];
      var box = questionCard(q, st.i, n);
      var btns = optButtons(q, box, function(pick){
        st.ans[st.i] = pick; btns.forEach(function(x, k){ x.classList.toggle('chosen', k === pick); });
        drawPal();
      });
      if(st.ans[st.i] !== null) btns[st.ans[st.i]].classList.add('chosen');
      body.appendChild(box); U.math(box);
      pg.textContent = 'Question ' + (st.i + 1) + ' of ' + n + ' · answered ' + st.ans.filter(function(v){ return v !== null; }).length;
      bprev.disabled = st.i === 0; bnext.textContent = st.i === n - 1 ? 'Submit ✔' : 'Next ▶';
      st.tstart = Date.now(); drawPal();
    }
    function drawPal(){
      if(cfg.forward) return; pal.innerHTML = '';
      items.forEach(function(_, k){ var b = U.el('button', 'pchip' + (st.ans[k] !== null ? ' done' : '') + (k === st.i ? ' cur' : ''), String(k + 1)); b.type = 'button'; b.onclick = function(){ leave(); st.i = k; show(); }; pal.appendChild(b); });
    }
    function leave(){ st.tq[st.i] += (Date.now() - st.tstart) / 1000; }
    bprev.onclick = function(){ if(st.i > 0){ leave(); st.i--; show(); } };
    bnext.onclick = function(){
      if(st.i < n - 1){ leave(); st.i++; show(); window.scrollTo(0, 0); }
      else if(confirm(st.ans.filter(function(v){ return v === null; }).length ? 'Some questions are unanswered. Submit anyway?' : 'Submit the exam?')){ leave(); finish(false); }
    };
    bfin.onclick = function(){ if(confirm('Finish the exam now? Unanswered questions score 0.')){ leave(); finish(false); } };
    document.onkeydown = function(e){
      if(st.finished) return; var k = e.key.toLowerCase(), idx = 'abcd'.indexOf(k);
      if(idx >= 0 && k.length === 1){ var b = U.$$('.opt', body)[idx]; if(b) b.click(); }
      else if(e.key === 'ArrowRight' || e.key === 'Enter'){ bnext.click(); }
      else if(e.key === 'ArrowLeft' && !cfg.forward){ bprev.click(); }
    };
    timer = setInterval(tick, 500); tick(); show();
    function finish(auto){
      if(st.finished) return; st.finished = true; clearInterval(timer); document.onkeydown = null;
      var used = Math.min(cfg.minutes * 60, Math.round((Date.now() - st.t0) / 1000));
      results(auto, used);
    }
  }

  function results(auto, used){
    root.innerHTML = '';
    var right = 0, byCh = {}, wrong = [];
    items.forEach(function(q, k){
      var ok = st.ans[k] === q.correct; if(ok) right++; else wrong.push(q.id);
      byCh[q.ch] = byCh[q.ch] || [0, 0]; byCh[q.ch][1]++; if(ok) byCh[q.ch][0]++;
      U.qstat(course, q.id, ok);
    });
    var grade = Math.round(right / n * 100) / 10;
    U.record(course, {t: Date.now(), id: cfg.key, title: cfg.title, mode: 'exam', score: right, total: n, secs: used, wrong: wrong, byCh: byCh});
    var box = U.el('div', 'panel');
    box.appendChild(U.el('h2', null, (auto ? '⏱ Time is up — ' : '') + 'Result'));
    box.appendChild(U.el('div', 'bigscore', right + ' / ' + n + ' correct · ' + grade.toFixed(1) + ' / 10'));
    box.appendChild(U.el('p', null, 'Time used: ' + U.fmtTime(used) + ' of ' + cfg.minutes + ':00. Unanswered: ' + st.ans.filter(function(v){ return v === null; }).length + '.'));
    var tb = U.el('table', 't'); var hr = U.el('tr'); ['Chapter', 'Correct', 'Questions', '%'].forEach(function(t){ hr.appendChild(U.el('th', null, t)); }); tb.appendChild(hr);
    Object.keys(byCh).sort().forEach(function(c){ var tr = U.el('tr'); [c.toUpperCase(), byCh[c][0], byCh[c][1], U.pct(byCh[c][0], byCh[c][1]) + '%'].forEach(function(t){ tr.appendChild(U.el('td', null, String(t))); }); tb.appendChild(tr); });
    box.appendChild(tb);
    var row = U.el('div', 'row');
    var again = U.el('a', 'btn', '↺ Take it again'); again.href = location.href; var hub = U.el('a', 'btn alt', 'Back to the exam hub'); hub.href = './';
    row.appendChild(again); row.appendChild(hub); box.appendChild(row); root.appendChild(box);
    root.appendChild(U.el('h3', null, 'Review: every question with the correct answer and a worked explanation'));
    items.forEach(function(q, k){
      var c = U.el('div', 'qitem'); var ok = st.ans[k] === q.correct;
      c.appendChild(U.el('div', 'qhead')).appendChild(U.el('span', 'tag ' + (ok ? 'okt' : 'badt'), (ok ? '✅ ' : st.ans[k] === null ? '⚪ ' : '❌ ') + 'Q' + (k + 1) + ' · ' + q.topic));
      c.appendChild(U.el('div', 'qtxt', q.q));
      q.opts.forEach(function(o, i){ var b = U.el('div', 'opt static' + (i === q.correct ? ' correct' : (i === st.ans[k] ? ' wrong' : ''))); b.appendChild(U.el('span', 'optl', LETTERS[i] + '.')); b.appendChild(U.el('span', 'optt', o)); c.appendChild(b); });
      var ex = U.el('div', 'explain show'); ex.appendChild(U.el('b', null, (ok ? 'Correct. ' : st.ans[k] === null ? 'Not answered. The answer is ' + LETTERS[q.correct] + '. ' : 'Your answer ' + LETTERS[st.ans[k]] + '; the correct answer is ' + LETTERS[q.correct] + '. '))); ex.appendChild(document.createTextNode(q.explain));
      c.appendChild(ex); c.appendChild(sourceLine(q)); root.appendChild(c);
    });
    U.math(root); window.scrollTo(0, 0);
  }
}
})();
