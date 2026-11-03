/* Concept finder page: three tabs (analyse a question, browse the concepts, keyword index). */
(function(){
'use strict';
var root = document.getElementById('concepts'); if(!root) return;
var FIXED = root.getAttribute('data-course') || '', BASE = root.getAttribute('data-base') || '';
var S = {q: '', course: 'all', ch: 'all', sort: 'name', hot: false}, data = [], COURSES = {}, sel = {};
function el(t, c, h){ var e = document.createElement(t); if(c) e.className = c; if(h != null) e.innerHTML = h; return e; }
function esc(s){ return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
function norm(s){ return window.Analyzer.norm(s); }
function math(node){ if(window.renderMathInElement) renderMathInElement(node, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}], throwOnError: false}); }
function pr(a){ return a[0] === a[1] ? a[0] : a[0] + '<br><span class="vi">' + a[1] + '</span>'; }
function list(items, ordered){ var tag = ordered ? 'ol' : 'ul'; return '<' + tag + '>' + items.map(function(s){ return '<li>' + (s[0] === s[1] ? s[0] : s[0] + ' <span class="vi">· ' + s[1] + '</span>') + '</li>'; }).join('') + '</' + tag + '>'; }

/* ---------------------------------------------------------------- browse tab */
function browse(pane){
  var concepts = data.filter(function(c){ return !c.out; });
  var bar = el('div', 'cf-bar'), cov = el('div'), lst = el('div'), tray = el('div', 'cf-tray');
  var search = el('input'); search.type = 'search'; search.placeholder = 'Search a concept, formula or word (EN / VI) · Tìm khái niệm…';
  var selC = el('select'), selCh = el('select'), selSort = el('select'), bHot = el('button', null, '★ Seen in exams'); bHot.type = 'button';
  selSort.innerHTML = '<option value="name">Sort: A–Z</option><option value="gap">Sort: fewest questions first</option><option value="most">Sort: most questions first</option>';
  (FIXED ? [search, selCh, selSort, bHot] : [search, selC, selCh, selSort, bHot]).forEach(function(x){ bar.appendChild(x); });
  [bar, cov, lst, tray].forEach(function(x){ pane.appendChild(x); });
  function matches(c){
    if(S.course !== 'all' && c.course !== S.course) return false;
    if(S.ch !== 'all' && c.ch !== S.ch) return false;
    if(S.hot && !c.hot) return false;
    if(S.q){ var t = norm([c.name.join(' '), c.defn.join(' '), c.facts.join(' '), c.kw, c.kwv, c.topics.join(' '), c.chapter, c.label].join(' ')); return S.q.split(/\s+/).every(function(w){ return t.indexOf(w) >= 0; }); }
    return true;
  }
  function link(c){
    if(!c.live) return '<span class="muted">bank not published yet · chưa đăng ngân hàng câu hỏi</span>';
    return c.topics.map(function(t){ return '<a class="tag" href="' + (BASE || ('../' + c.course + '/')) + 'bank/index.html?ch=' + c.ch + '&topic=' + encodeURIComponent(t) + '">' + esc(t) + '</a>'; }).join('');
  }
  function card(c){
    var d = el('div', 'cf-card'), cls = c.n < 8 ? 'low' : (c.n < 20 ? 'mid' : 'ok');
    var lv = Object.keys(c.levels).sort().map(function(k){ return 'L' + k + ':' + c.levels[k]; }).join(' · ');
    d.innerHTML = '<label style="float:right"><input type="checkbox" data-id="' + c.id + '"' + (sel[c.id] ? ' checked' : '') + '> add to brief</label>' +
      '<h3>' + (c.hot ? '★ ' : '') + c.name[0] + ' <span class="vi">· ' + c.name[1] + '</span></h3>' +
      '<div class="meta"><span class="tag">' + esc(c.label) + '</span><span class="tag">' + esc(c.chapter) + '</span><span class="tag">questions: <b class="cf-n ' + cls + '">' + c.n + '</b>' + (lv ? ' (' + lv + ')' : '') + '</span><span class="tag">keywords: ' + (c.kw.split(',').length + (c.kwv ? c.kwv.split(',').length : 0)) + '</span></div>' +
      '<p>' + pr(c.defn) + '</p>' +
      '<p><b>Formulas · Công thức:</b> ' + pr(c.facts) + '</p>' +
      (c.steps.length ? '<details><summary><b>Steps · Các bước</b></summary>' + list(c.steps, true) + '</details>' : '') +
      (c.traps.length ? '<details><summary><b>Traps · Bẫy</b></summary>' + list(c.traps, false) + '</details>' : '') +
      '<details><summary><b>How it is asked · Cách ra đề</b></summary>' + list(c.angles, false) + '</details>' +
      '<p>' + link(c) + '</p>';
    return d;
  }
  function brief(){
    var cs = concepts.filter(function(c){ return sel[c.id]; });
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
    var rows = '', courses = [];
    concepts.forEach(function(c){ if(courses.indexOf(c.course) < 0) courses.push(c.course); });
    courses.forEach(function(k){
      var cs = concepts.filter(function(c){ return c.course === k; }), thin = cs.filter(function(c){ return c.n < 8; }).length, outn = data.filter(function(c){ return c.out && c.course === k; }).length;
      rows += '<tr><td style="text-align:left">' + esc(cs[0].label) + '</td><td>' + cs.length + '</td><td>' + COURSES[k].mapped + ' of ' + COURSES[k].bank + '</td><td>' + thin + '</td><td>' + outn + '</td></tr>';
    });
    cov.innerHTML = '<table class="cf-cov"><thead><tr><th>Course</th><th>Concepts</th><th>Bank questions covered</th><th>Concepts with &lt; 8 questions</th><th>Out-of-scope topics known</th></tr></thead><tbody>' + rows + '</tbody></table>';
  }
  function render(){
    var cs = concepts.filter(matches);
    cs.sort(function(a, b){ return S.sort === 'gap' ? a.n - b.n : (S.sort === 'most' ? b.n - a.n : (a.course + a.ch + a.name[0]).localeCompare(b.course + b.ch + b.name[0])); });
    lst.innerHTML = ''; lst.appendChild(el('p', 'muted', cs.length + ' concept' + (cs.length === 1 ? '' : 's')));
    cs.forEach(function(c){ lst.appendChild(card(c)); });
    [].forEach.call(lst.querySelectorAll('input[data-id]'), function(i){ i.onchange = function(){ sel[i.getAttribute('data-id')] = i.checked; brief(); }; });
    math(lst); bHot.className = S.hot ? 'on' : ''; brief();
  }
  function fillCh(){
    var seen = {}; selCh.innerHTML = '<option value="all">All chapters</option>';
    concepts.forEach(function(c){ if(S.course !== 'all' && c.course !== S.course) return; var k = c.course + '|' + c.ch; if(seen[k]) return; seen[k] = 1;
      var o = el('option', null, esc((S.course === 'all' ? c.label + ' · ' : '') + c.ch.toUpperCase().replace('C', 'Ch. ') + ' ' + c.chapter)); o.value = c.ch; selCh.appendChild(o); });
    S.ch = 'all';
  }
  selC.innerHTML = '<option value="all">All courses</option>';
  var seenC = {}; concepts.forEach(function(c){ if(!seenC[c.course]){ seenC[c.course] = 1; var o = el('option', null, esc(c.label)); o.value = c.course; selC.appendChild(o); } });
  search.oninput = function(){ S.q = norm(search.value).trim(); render(); };
  selC.onchange = function(){ S.course = selC.value; fillCh(); render(); };
  selCh.onchange = function(){ S.ch = selCh.value; render(); };
  selSort.onchange = function(){ S.sort = selSort.value; render(); };
  bHot.onclick = function(){ S.hot = !S.hot; render(); };
  fillCh(); coverage(); render();
}

/* ---------------------------------------------------------------- keyword index tab */
function kwindex(pane){
  var bar = el('div', 'cf-bar'), lst = el('div');
  var search = el('input'); search.type = 'search'; search.placeholder = 'Filter keywords · Lọc từ khóa…';
  var selC = el('select'); selC.innerHTML = '<option value="all">All courses</option>';
  var seen = {}; data.forEach(function(c){ if(!seen[c.course]){ seen[c.course] = 1; var o = el('option', null, esc(c.label)); o.value = c.course; selC.appendChild(o); } });
  bar.appendChild(search); if(!FIXED) bar.appendChild(selC); pane.appendChild(bar); pane.appendChild(el('p', 'muted', 'Every hand-written keyword of the system and the concepts it leads to. A question whose words are not here (nor mined from the banks) will not match. · Mọi từ khóa viết tay của hệ thống và các khái niệm chúng dẫn tới.')); pane.appendChild(lst);
  var idx = {};
  data.forEach(function(c){
    (c.kw + ',' + (c.kwv || '') + ',' + (c.units || '').replace(/\s*\|\s*/g, ',')).split(/[,;]/).forEach(function(k){
      k = k.trim().replace(/\*\d+(\.\d+)?$/, '').trim(); if(!k || /^~/.test(k) || /^zz/.test(k)) return;
      (idx[k.toLowerCase()] = idx[k.toLowerCase()] || []).push(c);
    });
  });
  var keys = Object.keys(idx).sort(function(a, b){ return norm(a).localeCompare(norm(b)); });
  function render(){
    var q = norm(search.value).trim(), course = selC.value, h = '', n = 0, last = '';
    keys.forEach(function(k){
      var cs = idx[k].filter(function(c){ return course === 'all' || c.course === course; });
      if(!cs.length || (q && norm(k).indexOf(q) < 0)) return;
      var L = norm(k).charAt(0).toUpperCase(); if(L !== last){ h += '<h3 class="kwl">' + esc(L) + '</h3>'; last = L; }
      h += '<div class="kwrow"><b>' + esc(k) + '</b> → ' + cs.map(function(c){ return '<span class="tag' + (c.out ? ' out' : '') + '">' + esc(c.label + ' · ' + c.name[0]) + '</span>'; }).join('') + '</div>'; n++;
    });
    lst.innerHTML = '<p class="muted">' + n + ' keywords</p>' + h;
  }
  search.oninput = render; selC.onchange = render; render();
}

var shell = el('div'), tabs = el('div', 'cf-tabs'), panes = {};
[['az', '🔎 Analyse a question · Phân tích đề'], ['br', '📚 Browse concepts · Duyệt khái niệm'], ['kw', '🔤 Keyword index · Chỉ mục từ khóa']].forEach(function(t, i){
  var b = el('button', i === 0 ? 'on' : '', t[1]); b.type = 'button'; b.setAttribute('data-tab', t[0]); tabs.appendChild(b);
  panes[t[0]] = el('div', 'cf-pane'); panes[t[0]].style.display = i === 0 ? 'block' : 'none';
});
shell.appendChild(tabs); Object.keys(panes).forEach(function(k){ shell.appendChild(panes[k]); });
tabs.addEventListener('click', function(e){
  var t = e.target.getAttribute && e.target.getAttribute('data-tab'); if(!t) return;
  [].forEach.call(tabs.children, function(b){ b.className = b.getAttribute('data-tab') === t ? 'on' : ''; });
  Object.keys(panes).forEach(function(k){ panes[k].style.display = k === t ? 'block' : 'none'; });
  try{ history.replaceState(null, '', '#' + t); }catch(err){}
});
fetch(root.getAttribute('data-src')).then(function(r){ return r.json(); }).then(function(d){
  COURSES = d.courses; data = FIXED ? d.concepts.filter(function(c){ return c.course === FIXED; }) : d.concepts; root.innerHTML = ''; root.appendChild(shell);
  window.CFAnalyze.init(panes.az, d, d.concepts, {course: FIXED, base: BASE}); browse(panes.br); kwindex(panes.kw);
  var h = (location.hash || '').slice(1); if(panes[h]){ tabs.querySelector('[data-tab=' + h + ']').click(); }
}).catch(function(e){ root.innerHTML = '<p class="muted">Could not load the concepts (' + esc(e) + ').</p>'; });
})();
