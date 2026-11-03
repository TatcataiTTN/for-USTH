/* Question analyser UI: paste a question, get the matching concepts with the formulas, the solving steps and the usual traps;
   a question that matches nothing is flagged as outside the catalogue and you can teach the system new keywords (kept in this browser, exportable). */
(function(){
'use strict';
var KW_KEY = 'ustm:customkw', OUT_KEY = 'ustm:outscope';
function el(t, c, h){ var e = document.createElement(t); if(c) e.className = c; if(h != null) e.innerHTML = h; return e; }
function esc(s){ return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
function get(k, d){ try{ var v = JSON.parse(localStorage.getItem(k) || 'null'); return v == null ? d : v; }catch(e){ return d; } }
function put(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){} }
function bi(en, vi){ return '<span class="l-en">' + en + '</span> <span class="l-sep">·</span> <span class="l-vi">' + vi + '</span>'; }
function math(node){ if(window.renderMathInElement) renderMathInElement(node, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}], throwOnError: false}); }

var EXAMPLES = [
  ['Linear-Algebra', 'Find all values of k for which the system x + y + kz = 3, x + ky + z = 2, kx + y + z = 1 is consistent.'],
  ['Linear-Algebra', 'Cho A = [[1,2,0],[0,1,3],[0,0,1]]. Tìm cơ sở của không gian hàng và không gian cột của A.'],
  ['Calculus-1', 'Find the volume of the solid obtained by rotating the region bounded by y = x^2 and y = 2x about the x-axis.'],
  ['Calculus-1', 'Water is poured at 5 m^3/min into a conical tank, vertex down. How fast is the water level rising when the depth is 4 m?'],
  ['Physics-1', 'A 2.0 kg block slides down a 30° incline with coefficient of kinetic friction 0.20 from rest. What is its speed after 3.0 m?'],
  ['Physics-1', 'Một mol khí lưỡng nguyên tử giãn đoạn nhiệt từ 5 atm xuống 1 atm, nhiệt độ ban đầu 278 K. Tính nhiệt độ cuối.'],
  ['Physics-2', 'Light of wavelength 600 nm falls on a grating with 5000 lines per cm. At what angle is the second-order maximum?'],
  ['Physics-2', 'A circular coil of 200 turns and radius 5 cm sits in a magnetic field that rises from 0 to 0.4 T in 0.1 s. Find the induced emf.'],
  ['Physics-2', 'A diffraction pattern is obtained with a straight edge; find the position of the first maximum.']
];

function init(root, data, concepts){
  var A = window.Analyzer;
  var custom = get(KW_KEY, {}), outs = get(OUT_KEY, []);
  var model = A.compile(concepts, custom);
  var byId = {}; concepts.forEach(function(c){ byId[c.id] = c; });
  var box = el('div', 'az');
  box.innerHTML =
    '<div class="az-top"><textarea id="az-q" rows="5" placeholder="Paste any question here (English or Vietnamese, LaTeX is fine) · Dán câu hỏi vào đây (tiếng Anh hoặc tiếng Việt, có LaTeX cũng được)"></textarea>' +
    '<div class="az-bar"><select id="az-course"><option value="all">All courses · mọi môn</option></select>' +
    '<button type="button" id="az-go" class="on">Analyse · Phân tích</button><button type="button" id="az-clear">Clear · Xóa</button>' +
    '<select id="az-ex"><option value="">Examples · Ví dụ…</option></select></div></div><div id="az-out"></div>';
  root.appendChild(box);
  var labels = {};
  concepts.forEach(function(c){ labels[c.course] = c.label; });
  Object.keys(labels).forEach(function(k){ var o = el('option', null, esc(labels[k])); o.value = k; box.querySelector('#az-course').appendChild(o); });
  EXAMPLES.forEach(function(e, i){ var o = el('option', null, esc(labels[e[0]] + ': ' + e[1].slice(0, 60) + '…')); o.value = i; box.querySelector('#az-ex').appendChild(o); });
  var q = box.querySelector('#az-q'), courseSel = box.querySelector('#az-course'), out = box.querySelector('#az-out');

  function highlight(text, hits){
    var words = {};
    hits.forEach(function(h){ if(h.auto || /^~/.test(h.raw)) return; h.raw.split(/\s+/).forEach(function(w){ var s = A.stem(A.norm(w).trim()); if(s.length > 2) words[s] = 1; }); });
    return text.split(/([A-Za-zÀ-ỹ0-9']+)/).map(function(w, i){
      if(i % 2 === 0) return esc(w);
      var s = A.stem(A.norm(w).trim()); return words[s] ? '<mark>' + esc(w) + '</mark>' : esc(w);
    }).join('');
  }
  function list(items, ordered){ var tag = ordered ? 'ol' : 'ul'; return '<' + tag + '>' + items.map(function(s){ return '<li>' + s[0] + '<br><span class="vi">' + s[1] + '</span></li>'; }).join('') + '</' + tag + '>'; }

  function card(r, top, best, open){
    var c = r.c, pct = Math.max(4, Math.round(100 * r.score / best));
    var chips = r.hits.filter(function(h){ return !h.auto; }).slice(0, 8).map(function(h){ return '<span class="tag">' + esc(h.raw.replace(/^~/, '')) + '</span>'; }).join('') +
                r.hits.filter(function(h){ return h.auto; }).slice(0, 4).map(function(h){ return '<span class="tag auto" title="learned from the practice bank">' + esc(h.raw) + '</span>'; }).join('');
    var link = c.live && c.topics.length ? c.topics.slice(0, 3).map(function(t){ return '<a class="tag" href="../' + c.course + '/bank/index.html?ch=' + c.ch + '&topic=' + encodeURIComponent(t) + '">' + esc(t) + '</a>'; }).join('') : (c.topics.length ? '<span class="muted">bank not published</span>' : '');
    var rel = (c.related || []).map(function(id){ return byId[id] ? byId[id].name[0] : null; }).filter(Boolean).join(' · ');
    var d = el('details', 'az-card' + (c.out ? ' outc' : ''));
    if(open) d.open = true;
    d.innerHTML = '<summary><b>' + (c.hot ? '★ ' : '') + c.name[0] + '</b> <span class="vi">· ' + c.name[1] + '</span> <span class="tag">' + esc(c.label) + ' · ' + esc(c.ch.toUpperCase().replace('C', 'Ch. ')) + '</span>' +
      '<span class="bar"><i style="width:' + pct + '%"></i></span></summary>' +
      '<div class="az-body"><p class="muted">Matched · Khớp: ' + chips + '</p>' +
      '<p>' + c.defn[0] + '<br><span class="vi">' + c.defn[1] + '</span></p>' +
      (c.out ? '' :
        '<h4>Formulas · Công thức</h4><p>' + c.facts[0] + '<br><span class="vi">' + c.facts[1] + '</span></p>' +
        (c.steps.length ? '<h4>Steps · Các bước</h4>' + list(c.steps, true) : '') +
        (c.traps.length ? '<h4>Traps · Bẫy hay gặp</h4>' + list(c.traps, false) : '') +
        (c.angles.length ? '<h4>How it is asked · Cách ra đề</h4>' + list(c.angles, false) : '') +
        '<p class="muted">Practice · Luyện tập (' + c.n + '): ' + link + (rel ? ' &nbsp; Related · Liên quan: ' + esc(rel) : '') + '</p>') + '</div>';
    return d;
  }

  function teach(text, res){
    var best = res.results.length ? res.results[0].c : concepts[0];
    var cands = A.candidates(model, text, 8);
    var t = el('details', 'az-teach'); t.open = res.status !== 'ok';
    var opts = concepts.filter(function(c){ return !c.out && (courseSel.value === 'all' || c.course === courseSel.value); }).map(function(c){ return '<option value="' + c.id + '"' + (c.id === best.id ? ' selected' : '') + '>' + esc(c.label + ' · ' + c.name[0].replace(/\$/g, '')) + '</option>'; }).join('');
    t.innerHTML = '<summary><b>' + bi('Teach the system', 'Dạy cho hệ thống') + '</b></summary><div class="az-body">' +
      '<p class="muted">Pick the concept this question belongs to and the word(s) that should lead to it. Kept only in this browser; use Export to send them to be merged for everyone. · Chọn khái niệm của câu này và từ khóa dẫn tới nó. Chỉ lưu trên trình duyệt này; dùng Export để gửi lại và gộp cho mọi người.</p>' +
      '<div class="az-bar"><select id="az-tc">' + opts + '</select><input id="az-tk" type="text" placeholder="keyword, another keyword · từ khóa" value="' + esc(cands.slice(0, 3).join(', ')) + '"><button type="button" id="az-add" class="on">Add · Thêm</button></div>' +
      '<p>' + cands.map(function(w){ return '<button type="button" class="tag cand" data-w="' + esc(w) + '">' + esc(w) + '</button>'; }).join('') + '</p>' +
      '<div class="az-bar"><button type="button" id="az-outbtn">Mark this question as outside the course · Đánh dấu ngoài phạm vi</button></div>' +
      '<div id="az-mine"></div></div>';
    var mine = t.querySelector('#az-mine');
    function renderMine(){
      var keys = Object.keys(custom), n = 0;
      var h = keys.map(function(id){ if(!byId[id]) return ''; n += custom[id].length; return '<li><b>' + esc(byId[id].name[0]) + '</b>: ' + esc(custom[id].join(', ')) + '</li>'; }).join('');
      var oh = outs.map(function(o){ return '<li>' + esc(o.slice(0, 90)) + '…</li>'; }).join('');
      mine.innerHTML = '<h4>My additions · Phần tôi đã thêm (' + n + ')</h4><ul>' + (h || '<li class="muted">none yet</li>') + '</ul>' +
        (outs.length ? '<h4>Marked outside the course · Đã đánh dấu ngoài phạm vi (' + outs.length + ')</h4><ul>' + oh + '</ul>' : '') +
        '<div class="az-bar"><button type="button" id="az-exp">Copy export · Sao chép để gửi</button><button type="button" id="az-reset">Forget my additions · Xóa phần đã thêm</button></div>';
      mine.querySelector('#az-exp').onclick = function(){
        var payload = JSON.stringify({keywords: Object.keys(custom).map(function(id){ return {course: byId[id].course, concept: byId[id].name[0], keywords: custom[id]}; }), outOfScope: outs}, null, 1);
        try{ navigator.clipboard.writeText(payload); this.textContent = 'Copied ✓'; }catch(e){ window.prompt('Copy:', payload); }
      };
      mine.querySelector('#az-reset').onclick = function(){ custom = {}; outs = []; put(KW_KEY, custom); put(OUT_KEY, outs); model = A.compile(concepts, custom); run(); };
    }
    t.querySelector('#az-add').onclick = function(){
      var id = t.querySelector('#az-tc').value, ks = t.querySelector('#az-tk').value.split(',').map(function(x){ return x.trim(); }).filter(Boolean);
      if(!ks.length) return;
      custom[id] = (custom[id] || []).concat(ks.filter(function(k){ return (custom[id] || []).indexOf(k) < 0; }));
      put(KW_KEY, custom); model = A.compile(concepts, custom); run(true);
    };
    t.querySelector('#az-outbtn').onclick = function(){ if(outs.indexOf(text) < 0){ outs.push(text); put(OUT_KEY, outs); } renderMine(); };
    [].forEach.call(t.querySelectorAll('.cand'), function(b){ b.onclick = function(){ var i = t.querySelector('#az-tk'); i.value = (i.value ? i.value + ', ' : '') + b.getAttribute('data-w'); }; });
    renderMine();
    return t;
  }

  function run(keepTeach){
    var text = q.value.trim();
    out.innerHTML = '';
    if(!text){ out.appendChild(el('p', 'muted', 'Paste a question above. · Dán một câu hỏi ở trên.')); return; }
    var res = A.analyze(model, text, {course: courseSel.value, top: 6});
    var kinds = A.kinds(text);
    var banner = el('div', 'callout ' + (res.status === 'ok' ? 'good' : 'bad'));
    if(res.status === 'ok') banner.innerHTML = '<b>' + bi('Matched the catalogue', 'Khớp với hệ khái niệm') + '</b> — best: <b>' + res.results[0].c.name[0] + '</b> (' + esc(res.results[0].c.label) + ')';
    else if(res.status === 'out') banner.innerHTML = '<b>⚠ ' + bi('Probably outside the taught scope', 'Có thể nằm ngoài phạm vi môn học') + '</b> — it looks like <b>' + res.results.filter(function(r){ return r.c.out; })[0].c.name[0] + '</b>: ' + res.results.filter(function(r){ return r.c.out; })[0].c.defn[0] + ' <br><span class="vi">' + res.results.filter(function(r){ return r.c.out; })[0].c.defn[1] + '</span>';
    else banner.innerHTML = '<b>⚠ ' + bi('No concept matched: outside the catalogue', 'Không khớp khái niệm nào: ngoài hệ khái niệm') + '</b> — either the question is outside the course or the keyword system lacks its words. Use “Teach the system” below.';
    out.appendChild(banner);
    var qb = el('div', 'az-question'); qb.innerHTML = highlight(text, res.results.reduce(function(a, r){ return a.concat(r.hits); }, []));
    out.appendChild(qb);
    if(kinds.length){ var kd = el('div', 'callout'); kd.innerHTML = '<b>' + bi('Type of question', 'Dạng câu hỏi') + '</b>' + kinds.map(function(k){ return '<br>• ' + k.en + '<br><span class="vi">&nbsp;&nbsp;' + k.vi + '</span>'; }).join(''); out.appendChild(kd); }
    if(res.results.length && res.status !== 'none'){
      var best = res.results[0].score, strong = res.results.filter(function(r){ return !r.c.out && r.score >= 0.55 * best; });
      res.results.forEach(function(r, i){ out.appendChild(card(r, i, best, i === 0)); });
      if(strong.length >= 2){
        var plan = el('details', 'az-card'); plan.open = true;
        plan.innerHTML = '<summary><b>' + bi('Combined solution plan', 'Kế hoạch giải kết hợp') + '</b> <span class="muted">— this question seems to mix ' + strong.length + ' concepts</span></summary><div class="az-body">' +
          strong.map(function(r, i){ return '<h4>' + (i + 1) + '. ' + r.c.name[0] + '</h4>' + (r.c.steps.length ? list(r.c.steps, true) : ''); }).join('') + '</div>';
        out.appendChild(plan);
      }
    }
    var gen = el('details', 'az-card');
    gen.innerHTML = '<summary><b>' + bi('Universal frame for any new-looking question', 'Khung chung cho mọi câu hỏi lạ') + '</b></summary><div class="az-body"><ol>' +
      ['<b>Target</b>: what exactly is asked (quantity, unit, sign)? | <b>Cần tìm</b>: chính xác đại lượng nào (đơn vị, dấu)?',
       '<b>Given</b>: list the data with units; convert to SI. | <b>Cho</b>: liệt kê dữ kiện kèm đơn vị; đổi sang SI.',
       '<b>Principle</b>: pick the concept(s) above; write the law symbolically. | <b>Nguyên lý</b>: chọn khái niệm ở trên; viết định luật bằng ký hiệu.',
       '<b>Isolate</b> the unknown before substituting numbers. | <b>Cô lập</b> ẩn trước khi thay số.',
       '<b>Compute</b> with units; keep 3 significant figures. | <b>Tính</b> kèm đơn vị; giữ 3 chữ số có nghĩa.',
       '<b>Check</b>: units, size, limiting case, a second route. | <b>Kiểm tra</b>: đơn vị, độ lớn, trường hợp giới hạn, cách làm thứ hai.'].map(function(s){ var p = s.split(' | '); return '<li>' + p[0] + '<br><span class="vi">' + p[1] + '</span></li>'; }).join('') + '</ol></div>';
    out.appendChild(gen);
    var t = teach(text, res); out.appendChild(t);
    math(out);
  }

  box.querySelector('#az-go').onclick = function(){ run(); };
  box.querySelector('#az-clear').onclick = function(){ q.value = ''; run(); };
  box.querySelector('#az-ex').onchange = function(){ var i = this.value; if(i === '') return; q.value = EXAMPLES[i][1]; courseSel.value = EXAMPLES[i][0]; run(); this.value = ''; };
  q.addEventListener('keydown', function(e){ if((e.ctrlKey || e.metaKey) && e.key === 'Enter') run(); });
  courseSel.onchange = function(){ if(q.value.trim()) run(); };
  run();
}
window.CFAnalyze = {init: init};
})();
