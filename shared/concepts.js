/* Concept finder: search, filters, coverage view and a "brief" of selected concepts to plan new question sets. */
(function(){
'use strict';
var root = document.getElementById('concepts'); if(!root) return;
var COURSES = {}, S = {q: '', course: 'all', ch: 'all', sort: 'name', hot: false}, data = [], sel = {};
function el(t, c, h){ var e = document.createElement(t); if(c) e.className = c; if(h != null) e.innerHTML = h; return e; }
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }
function norm(s){ return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/đ/g,'d'); }
function text(c){ return norm([c.name.join(' '), c.defn.join(' '), c.facts.join(' '), c.kw, c.topics.join(' '), c.chapter, c.label].join(' ')); }
var shell = el('div'), bar = el('div', 'cf-bar'), cov = el('div'), list = el('div'), tray = el('div', 'cf-tray');
var search = el('input'); search.type = 'search'; search.placeholder = 'Search a concept, formula or word (EN / VI) · Tìm khái niệm…';
var selC = el('select'), selCh = el('select'), selSort = el('select'), bHot = el('button', null, '★ Seen in exams'); bHot.type = 'button';
selSort.innerHTML = '<option value="name">Sort: A–Z</option><option value="gap">Sort: fewest questions first</option><option value="most">Sort: most questions first</option>';
bar.appendChild(search); bar.appendChild(selC); bar.appendChild(selCh); bar.appendChild(selSort); bar.appendChild(bHot);
shell.appendChild(bar); shell.appendChild(cov); shell.appendChild(list); shell.appendChild(tray);
function matches(c){
  if(S.course !== 'all' && c.course !== S.course) return false;
  if(S.ch !== 'all' && c.ch !== S.ch) return false;
  if(S.hot && !c.hot) return false;
  if(S.q){ var t = text(c); return S.q.split(/\s+/).every(function(w){ return t.indexOf(w) >= 0; }); }
  return true;
}
function link(c){
  if(!c.live) return '<span class="muted">bank not published yet · chưa đăng ngân hàng câu hỏi</span>';
  return c.topics.map(function(t){ return '<a class="tag" href="../' + c.course + '/bank/index.html?ch=' + c.ch + '&topic=' + encodeURIComponent(t) + '">' + esc(t) + '</a>'; }).join('');
}
function card(c){
  var d = el('div', 'cf-card'), cls = c.n < 8 ? 'low' : (c.n < 20 ? 'mid' : 'ok');
  var lv = Object.keys(c.levels).sort().map(function(k){ return 'L' + k + ':' + c.levels[k]; }).join(' · ');
  d.innerHTML = '<label style="float:right"><input type="checkbox" data-id="' + c.id + '"' + (sel[c.id] ? ' checked' : '') + '> add to brief</label>' +
    '<h3>' + (c.hot ? '★ ' : '') + c.name[0] + ' <span class="vi">· ' + c.name[1] + '</span></h3>' +
    '<div class="meta"><span class="tag">' + esc(c.label) + '</span><span class="tag">' + esc(c.chapter) + '</span><span class="tag">questions: <b class="cf-n ' + cls + '">' + c.n + '</b>' + (lv ? ' (' + lv + ')' : '') + '</span></div>' +
    '<p>' + c.defn[0] + '<br><span class="vi">' + c.defn[1] + '</span></p>' +
    '<p><b>Key facts · Ý chính:</b> ' + c.facts[0] + '<br><span class="vi">' + c.facts[1] + '</span></p>' +
    '<p><b>How it is asked · Cách ra đề:</b></p><ul>' + c.angles.map(function(a){ return '<li>' + a[0] + ' <span class="vi">· ' + a[1] + '</span></li>'; }).join('') + '</ul>' +
    '<p>' + link(c) + '</p>';
  return d;
}
function brief(){
  var ids = Object.keys(sel).filter(function(k){ return sel[k]; });
  var cs = data.filter(function(c){ return sel[c.id]; });
  tray.className = 'cf-tray' + (cs.length ? ' show' : '');
  tray.innerHTML = '<b>' + cs.length + ' selected</b>';
  var b = el('button', null, 'Copy brief for new questions'); b.type = 'button';
  b.onclick = function(){
    var t = cs.map(function(c){ return '- ' + c.label + ' / ' + c.chapter + ': ' + c.name[0] + ' (' + c.n + ' questions now)\n' + c.angles.map(function(a){ return '    · ' + a[0]; }).join('\n'); }).join('\n');
    try{ navigator.clipboard.writeText('Concepts to build more diverse questions for:\n' + t); b.textContent = 'Copied ✓'; }catch(e){ b.textContent = 'Copy failed'; }
  };
  var c2 = el('button', null, 'Clear'); c2.type = 'button'; c2.onclick = function(){ sel = {}; render(); };
  tray.appendChild(b); tray.appendChild(c2);
}
function coverage(){
  var rows = '';
  var courses = [];
  data.forEach(function(c){ if(courses.indexOf(c.course) < 0) courses.push(c.course); });
  courses.forEach(function(k){
    var cs = data.filter(function(c){ return c.course === k; }), tot = COURSES[k].mapped + ' of ' + COURSES[k].bank;
    var thin = cs.filter(function(c){ return c.n < 8; }).length;
    rows += '<tr><td style="text-align:left">' + esc(cs[0].label) + '</td><td>' + cs.length + '</td><td>' + tot + '</td><td>' + thin + '</td></tr>';
  });
  cov.innerHTML = '<table class="cf-cov"><thead><tr><th>Course</th><th>Concepts</th><th>Bank questions covered by a concept</th><th>Concepts with &lt; 8 questions</th></tr></thead><tbody>' + rows + '</tbody></table>';
}
function render(){
  var cs = data.filter(matches);
  cs.sort(function(a, b){ return S.sort === 'gap' ? a.n - b.n : (S.sort === 'most' ? b.n - a.n : (a.course + a.ch + a.name[0]).localeCompare(b.course + b.ch + b.name[0])); });
  list.innerHTML = ''; list.appendChild(el('p', 'muted', cs.length + ' concept' + (cs.length === 1 ? '' : 's')));
  cs.forEach(function(c){ list.appendChild(card(c)); });
  [].forEach.call(list.querySelectorAll('input[data-id]'), function(i){ i.onchange = function(){ sel[i.getAttribute('data-id')] = i.checked; brief(); }; });
  if(window.renderMathInElement) renderMathInElement(list, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}], throwOnError: false});
  bHot.className = S.hot ? 'on' : ''; brief();
}
function fillCh(){
  var seen = {}; selCh.innerHTML = '<option value="all">All chapters</option>';
  data.forEach(function(c){ if(S.course !== 'all' && c.course !== S.course) return; var k = c.course + '|' + c.ch; if(seen[k]) return; seen[k] = 1;
    var o = el('option', null, esc((S.course === 'all' ? c.label + ' · ' : '') + c.ch.toUpperCase().replace('C', 'Ch. ') + ' ' + c.chapter)); o.value = c.ch; selCh.appendChild(o); });
  S.ch = 'all';
}
search.oninput = function(){ S.q = norm(search.value).trim(); render(); };
selC.onchange = function(){ S.course = selC.value; fillCh(); render(); };
selCh.onchange = function(){ S.ch = selCh.value; render(); };
selSort.onchange = function(){ S.sort = selSort.value; render(); };
bHot.onclick = function(){ S.hot = !S.hot; render(); };
fetch(root.getAttribute('data-src')).then(function(r){ return r.json(); }).then(function(d){
  COURSES = d.courses; data = d.concepts; selC.innerHTML = '<option value="all">All courses</option>';
  var seen = {}; data.forEach(function(c){ if(!seen[c.course]){ seen[c.course] = 1; var o = el('option', null, esc(c.label)); o.value = c.course; selC.appendChild(o); } });
  fillCh(); coverage(); root.innerHTML = ''; root.appendChild(shell); render();
}).catch(function(e){ root.innerHTML = '<p class="muted">Could not load the concepts (' + esc(e) + ').</p>'; });
})();
