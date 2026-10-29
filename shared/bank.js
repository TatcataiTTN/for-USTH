/* Practice bank: filter by chapter / topic / level / source, search, paginate, answer with instant feedback,
   "Written mode" hides the options so you can solve on paper first and then check the model answer. */
(function(){
'use strict';
var U = window.USTM;
var root = document.getElementById('bank');
if(!root) return;
var base = root.getAttribute('data-base'), course = root.getAttribute('data-course');
var LETTERS = 'ABCD';
var S = {ch: 'all', topic: 'all', level: 'all', origin: 'all', q: '', wrong: false, written: false, page: 0, size: 12, order: null};

Promise.all([U.json(base + 'bank.json'), U.json(base + 'meta.json')]).then(function(res){ init(res[0], res[1]); })
  .catch(function(e){ root.textContent = 'Could not load the bank: ' + e.message; });

function init(bank, meta){
  var items = bank.items;
  S.order = items.map(function(_, i){ return i; });
  var chapters = meta.chapters;
  var qs = U.store.get(U.key(course, 'qstats'), {});
  var panel = U.el('div', 'panel'); root.appendChild(panel);
  var row = U.el('div', 'row filters');
  function sel(label, opts, key){
    var l = U.el('label', null, label + ' '); var s = U.el('select');
    opts.forEach(function(o){ var op = U.el('option', null, o[1]); op.value = o[0]; s.appendChild(op); });
    s.onchange = function(){ S[key] = s.value; S.page = 0; if(key === 'ch'){ fillTopics(); } render(); };
    l.appendChild(s); row.appendChild(l); return s;
  }
  var selCh = sel('Chapter', [['all', 'All chapters (' + items.length + ')']].concat(chapters.map(function(c){ return [c.id, c.id.toUpperCase().replace('C', 'Ch. ') + ' · ' + c.title + ' (' + items.filter(function(i){ return i.ch === c.id; }).length + ')']; })), 'ch');
  var selTopic = sel('Topic', [['all', 'All topics']], 'topic');
  sel('Level', [['all', 'All'], ['1', 'Basic (1)'], ['2', 'Medium (2)'], ['3', 'Hard (3)']], 'level');
  sel('Source', [['all', 'All'], ['src', 'From the course documents (' + items.filter(function(i){ return i.origin === 'src'; }).length + ')'], ['gen', 'Generated, same style (' + items.filter(function(i){ return i.origin === 'gen'; }).length + ')'], ['concept', 'Concept checks (' + items.filter(function(i){ return i.origin === 'concept'; }).length + ')']], 'origin');
  panel.appendChild(row);
  var row2 = U.el('div', 'row');
  var search = U.el('input'); search.type = 'search'; search.placeholder = 'Search text, topic or source…'; search.oninput = function(){ S.q = search.value.toLowerCase(); S.page = 0; render(); };
  var cb = U.el('label'); var c1 = U.el('input'); c1.type = 'checkbox'; c1.onchange = function(){ S.wrong = c1.checked; S.page = 0; render(); }; cb.appendChild(c1); cb.appendChild(document.createTextNode(' only questions I got wrong'));
  var cw = U.el('label'); var c2 = U.el('input'); c2.type = 'checkbox'; c2.onchange = function(){ S.written = c2.checked; render(); }; cw.appendChild(c2); cw.appendChild(document.createTextNode(' written mode (hide options)'));
  var bsh = U.el('button', 'btn alt small', '🔀 Shuffle'); bsh.onclick = function(){ S.order = U.shuffle(S.order); S.page = 0; render(); };
  var bor = U.el('button', 'btn alt small', '⟲ Original order'); bor.onclick = function(){ S.order = items.map(function(_, i){ return i; }); S.page = 0; render(); };
  row2.appendChild(search); row2.appendChild(cb); row2.appendChild(cw); row2.appendChild(bsh); row2.appendChild(bor); panel.appendChild(row2);
  var info = U.el('div', 'score'); panel.appendChild(info);
  var list = U.el('div'); root.appendChild(list);
  var nav = U.el('div', 'row'); root.appendChild(nav);
  function fillTopics(){
    var ts = {}; items.forEach(function(i){ if(S.ch === 'all' || i.ch === S.ch) ts[i.topic] = (ts[i.topic] || 0) + 1; });
    selTopic.innerHTML = ''; var o = U.el('option', null, 'All topics'); o.value = 'all'; selTopic.appendChild(o);
    Object.keys(ts).sort().forEach(function(t){ var op = U.el('option', null, t + ' (' + ts[t] + ')'); op.value = t; selTopic.appendChild(op); });
    S.topic = 'all';
  }
  fillTopics();
  var qp = new URLSearchParams(location.search);
  if(qp.get('ch')){ S.ch = qp.get('ch'); selCh.value = S.ch; fillTopics(); }
  if(qp.get('written') === '1'){ S.written = true; c2.checked = true; }
  function filtered(){
    qs = U.store.get(U.key(course, 'qstats'), {});
    return S.order.map(function(i){ return items[i]; }).filter(function(q){
      if(S.ch !== 'all' && q.ch !== S.ch) return false;
      if(S.topic !== 'all' && q.topic !== S.topic) return false;
      if(S.level !== 'all' && String(q.level) !== S.level) return false;
      if(S.origin !== 'all' && q.origin !== S.origin) return false;
      if(S.q && (q.q + ' ' + q.topic + ' ' + q.src).toLowerCase().indexOf(S.q) < 0) return false;
      if(S.wrong){ var r = qs[q.id]; if(!r || r[1] === r[0]) return false; }
      return true;
    });
  }
  function render(){
    var f = filtered(), pages = Math.max(1, Math.ceil(f.length / S.size)); if(S.page >= pages) S.page = pages - 1;
    info.textContent = f.length + ' question' + (f.length === 1 ? '' : 's') + ' · page ' + (S.page + 1) + ' of ' + pages;
    list.innerHTML = '';
    f.slice(S.page * S.size, (S.page + 1) * S.size).forEach(function(q){ list.appendChild(card(q)); });
    nav.innerHTML = '';
    var p = U.el('button', 'btn alt', '◀ Previous'), n = U.el('button', 'btn alt', 'Next ▶');
    p.disabled = S.page === 0; n.disabled = S.page >= pages - 1;
    p.onclick = function(){ S.page--; render(); window.scrollTo(0, 0); }; n.onclick = function(){ S.page++; render(); window.scrollTo(0, 0); };
    nav.appendChild(p); nav.appendChild(n); U.math(list);
  }
  function card(q){
    var box = U.el('div', 'qitem');
    var head = U.el('div', 'qhead'); head.appendChild(U.el('span', 'tag', q.id)); head.appendChild(U.el('span', 'tag', q.topic)); head.appendChild(U.el('span', 'tag lv' + q.level, 'level ' + q.level)); box.appendChild(head);
    box.appendChild(U.el('div', 'qtxt', q.q));
    var ex = U.el('div', 'explain');
    function reveal(pick){
      ex.innerHTML = '';
      if(pick !== undefined) ex.appendChild(U.el('b', null, pick === q.correct ? '✅ Correct. ' : '❌ The answer is ' + LETTERS[q.correct] + '. '));
      else ex.appendChild(U.el('b', null, 'Answer ' + LETTERS[q.correct] + ': '));
      if(S.written || pick === undefined){ ex.appendChild(U.el('span', 'optt ansline', q.opts[q.correct])); ex.appendChild(document.createElement('br')); }
      ex.appendChild(document.createTextNode(q.explain)); ex.classList.add('show'); U.math(ex);
    }
    if(S.written){
      var b = U.el('button', 'btn alt small', '👁 Show the model answer'); b.type = 'button'; b.onclick = function(){ reveal(); b.style.display = 'none'; }; box.appendChild(b);
    } else {
      var btns = q.opts.map(function(o, i){
        var bt = U.el('button', 'opt'); bt.type = 'button'; bt.appendChild(U.el('span', 'optl', LETTERS[i] + '.')); bt.appendChild(U.el('span', 'optt', o));
        bt.onclick = function(){
          if(bt.disabled) return; U.qstat(course, q.id, i === q.correct);
          btns.forEach(function(x, k){ x.disabled = true; if(k === q.correct) x.classList.add('correct'); }); if(i !== q.correct) bt.classList.add('wrong'); reveal(i);
        };
        box.appendChild(bt); return bt;
      });
    }
    box.appendChild(ex);
    box.appendChild(U.el('div', 'qsrc', U.srcLabel(q)));
    return box;
  }
  render();
}
})();
