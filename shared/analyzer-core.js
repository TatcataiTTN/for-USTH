/* Question analyser core (browser + Node). Matches the words of a pasted question against the keyword system of every concept
   and returns the best concepts with the evidence (matched keywords), or flags the question as outside the catalogue.
   Keyword sources per concept: kw (hand written, English), kwv (hand written, Vietnamese), units (unit / symbol hints), ak (mined from the practice banks, weighted),
   plus the concept name. Idf makes shared words (force, energy, matrix ...) count less than specific ones (eigenvalue, Snell, Gauss ...). */
(function(root, factory){
  if(typeof module === 'object' && module.exports) module.exports = factory();
  else root.Analyzer = factory();
})(typeof self !== 'undefined' ? self : this, function(){
'use strict';

var SYM = [
  /* notation that carries meaning on its own: turn it into marker words (zz...) the concept keywords can name */
  [/\\(?:d|t)?frac\s*\{\s*d\s*(?:\^\{?\d\}?)?\s*[a-zA-Z]\s*\}\s*\{\s*d\s*[a-zA-Z]\s*(?:\^\{?\d\}?)?\s*\}|\\(?:d|t)?frac\s*\{\s*d\s*\}\s*\{\s*d\s*[a-zA-Z]\s*\}|[a-zA-Z]\^\{?\(\d+\)\}?|\b[a-zA-Z]'{1,2}(?!s\b|t\b|ll\b|re\b)/g, ' zzderiv derivative '],
  [/\\partial|∂/g, ' zzpartial partial '],
  [/\b[a-zA-Z]\s*\(\s*[a-zA-Z]\s*\(|(?:^|[^\^\\])\\circ(?![\w}])(?!\s*\})/g, ' zzcompose composition '],
  [/\[\s*(?:\\mathbf\s*\{?)?[a-zA-Z](?:\})?\s*\]_\{?[A-Za-z]/g, ' zzcoord coordinates '],
  [/\bT\s*\(\s*[a-z0-9_ ,]+\)\s*=\s*\(|\[\s*T\s*\]_/g, ' zzmap linear transformation '],
  [/\\dim\b/g, ' zzdim dimension '], [/\\ker\b/g, ' kernel '], [/\\langle/g, ' zzinner inner product '],
  [/\\operatorname\s*\{\s*(?:tr|trace)\s*\}|\\mathrm\s*\{\s*tr\s*\}|\\operatorname\s*\{\s*adj\s*\}|\\mathrm\s*\{\s*adj\s*\}/g, function(m){ return /adj/.test(m) ? ' adjugate ' : ' trace '; }],
  [/\\overline\s*\{/g, ' repeating decimal series zzrepeat '],
  [/\^\s*\{?\s*T\s*\}?/g, ' transpose '], [/[A-Za-z\)]\^\s*\{\s*-1\s*\}/g, ' inverse '],
  [/\(\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?(?:\s*,\s*-?\d+(?:\.\d+)?)*\s*\)/g, ' zztuple '],
  [/\\(?:d|t)?frac|⁄/g, ' fraction '], [/\\oint|∮/g, ' closed integral oint '], [/\\int|∫/g, ' integral '], [/\\sum|∑/g, ' sum series '], [/\\lim/g, ' limit '],
  [/\\det\b/g, ' determinant '], [/\\operatorname\{rank\}|\\mathrm\{rank\}/g, ' rank '], [/\\infty|∞/g, ' infinity '], [/\\sqrt|√/g, ' sqrt '], [/\\mathcal\s*\{?e\}?|ℰ/gi, ' emf '],
  [/\\mu_?0|μ0|μ₀/g, ' mu0 '], [/\\varepsilon_?0|ε0|ε₀|\\epsilon_?0/g, ' epsilon0 '], [/\\mu|μ/g, ' mu '], [/\\lambda|λ/g, ' lambda '], [/\\theta|θ/g, ' theta '], [/\\varphi|\\phi|φ|Φ|\\Phi/g, ' phi '],
  [/\\omega|ω/g, ' omega '], [/\\alpha|α/g, ' alpha '], [/\\beta|β/g, ' beta '], [/\\gamma|γ/g, ' gamma '], [/\\delta|\\Delta|Δ|δ/g, ' delta '], [/\\pi|π/g, ' pi '], [/\\sigma|σ/g, ' sigma '], [/\\rho|ρ/g, ' rho '], [/\\tau|τ/g, ' tau '],
  [/\\ln\b/g, ' ln log '], [/\\log\b/g, ' log '], [/\\sin\b/g, ' sin '], [/\\cos\b/g, ' cos '], [/\\tan\b/g, ' tan '], [/\\exp\b/g, ' exp '], [/\\nabla|∇/g, ' gradient '], [/\\partial|∂/g, ' partial '],
  [/\\vec\{?([a-z])\}?/gi, ' vector $1 '], [/\\cdot|·|×|\\times|\\cross/g, ' times '], [/\\leq?|≤|\\geq?|≥|<|>/g, ' inequality '], [/°|\^\s*\{?\s*\\circ\s*\}?/g, ' degree '], [/\\mathrm\{([^}]*)\}|\\text\{([^}]*)\}/g, ' $1$2 '],
  [/\\begin\{vmatrix\}/g, ' determinant matrix '],
  [/\\begin\{[pbvVB]?matrix\}|\\begin\{array\}|\\begin\{cases\}/g, ' matrix '], [/\\[a-zA-Z]+/g, ' ']
];

function strip(s){ return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D'); }

function norm(text){
  var s = String(text);
  SYM.forEach(function(p){ s = s.replace(p[0], p[1]); });
  s = strip(s).toLowerCase();
  s = s.replace(/[$_{}\\]/g, ' ').replace(/\^/g, '^');
  return s;
}

function stem(w){
  if(w.length <= 3) return w;
  if(/ies$/.test(w) && w.length > 4) return w.slice(0, -3) + 'y';
  if(/(?:ss|us|is|ous)$/.test(w)) return w;
  if(/(?:ches|shes|xes|zes|sses)$/.test(w)) return w.slice(0, -2);
  if(/s$/.test(w) && w.length > 3) w = w.slice(0, -1);
  if(/ing$/.test(w) && w.length > 5) w = w.slice(0, -3);
  else if(/ed$/.test(w) && w.length > 4) w = w.slice(0, -2);
  return w;
}

function tokens(text){
  return norm(text).split(/[^a-z0-9\/\^\.]+/).map(function(t){ return t.replace(/^\.+|\.+$/g, ''); }).filter(Boolean).map(stem);
}

var STOP = {};
('the a an of to in on at by for with from and or is are was were be been it its this that these those as if then than so such into over under between '
 + 'what which who whom how when where why find calculate compute determine give gives given value values following select one answer correct question '
 + 've cua la va cac mot nhung co khong duoc cho tim tinh hay chon dap an cau hoi sau day').split(' ').forEach(function(w){ STOP[w] = 1; });

function phraseTokens(p){ return tokens(p); }

/* spec: "span*3, linear combination, ~regex" -> [{t:[tokens], w:weight, raw:'...', re:RegExp|null}] */
function parseSpec(spec){
  var out = [];
  String(spec || '').split(/[,;\n]/).forEach(function(item){
    item = item.trim(); if(!item) return;
    var w = null, m = item.match(/\*(\d+(?:\.\d+)?)\s*$/);
    if(m){ w = parseFloat(m[1]); item = item.slice(0, m.index).trim(); }
    var re = null;
    if(item.charAt(0) === '~'){ try{ re = new RegExp(item.slice(1), 'i'); }catch(e){ return; } out.push({t: [], w: w == null ? 3 : w, raw: item, re: re}); return; }
    var t = phraseTokens(item).filter(function(x){ return x; });
    if(!t.length || t.every(function(x){ return x.length < 2; })) return;                 // single letters (x, T, K ...) are symbols of every course: never keywords
    if(w == null) w = t.length >= 2 ? 3 : (t[0].length >= 6 ? 2 : 1);
    out.push({t: t, w: w, raw: item, re: null});
  });
  return out;
}

function compile(concepts, custom){
  custom = custom || {};
  var df = {};
  var cs = concepts.map(function(c){
    var kws = []
      .concat(parseSpec(c.kw), parseSpec(c.kwv), parseSpec((c.units || '').replace(/\s*\|\s*/g, ',')), parseSpec((custom[c.id] || []).map(function(x){ return x + '*3'; }).join(',')));
    var nameKws = [];
    (c.name || []).forEach(function(n){ n.split(/\s*[,;\/]\s*/).forEach(function(part){ var t = phraseTokens(part); if(t.length) nameKws.push({t: t, w: t.length >= 2 ? 3 : 2, raw: part, re: null, name: true}); }); });
    kws = kws.concat(nameKws);
    var auto = (c.ak || []).map(function(a){ var t = String(a[0]).split(' ').filter(Boolean); return t.length ? {t: t, w: a[1], raw: a[0], re: null, auto: true} : null; }).filter(Boolean);   // mined terms are already stems
    var all = kws.concat(auto);
    var seen = {};
    all.forEach(function(k){ var key = k.re ? k.raw : k.t.join(' '); if(!seen[key]){ seen[key] = 1; df[key] = (df[key] || 0) + 1; } k.key = key; });
    return {c: c, kws: all};
  });
  var N = cs.length;
  cs.forEach(function(e){ e.kws.forEach(function(k){ k.idf = Math.log(1 + N / (df[k.key] || 1)); }); });
  return {list: cs, N: N};
}

function findSeq(tk, seq, from){
  var n = seq.length;
  for(var i = from || 0; i + n <= tk.length; i++){
    var ok = true;
    for(var j = 0; j < n; j++){ if(tk[i + j] !== seq[j]){ ok = false; break; } }
    if(ok) return i;
  }
  return -1;
}

/* opts: {course:'Linear-Algebra'|'all', top:6, min:3} */
function analyze(model, text, opts){
  opts = opts || {};
  var tk = tokens(text), nt = norm(text), res = [];
  var wordsOnly = tk.filter(function(t){ return !STOP[t]; });
  model.list.forEach(function(e){
    if(opts.course && opts.course !== 'all' && e.c.course !== opts.course) return;
    var score = 0, hits = [];
    e.kws.forEach(function(k){
      var hit = false;
      if(k.re) hit = k.re.test(nt);
      else if(k.t.length === 1 && STOP[k.t[0]]) hit = false;
      else hit = findSeq(tk, k.t) >= 0;
      if(hit){ var s = k.w * k.idf * (k.auto ? 1 : 1.6) * (e.c.out ? 1.6 : 1); score += s; hits.push({raw: k.raw, w: s, auto: !!k.auto, name: !!k.name}); }
    });
    if(score > 0) res.push({c: e.c, score: score, hits: hits.sort(function(a, b){ return b.w - a.w; })});
  });
  res.sort(function(a, b){ return b.score - a.score; });
  if(!(opts.course && opts.course !== 'all')){          // course vote: the course whose concepts collect the most evidence leads; the others are damped
    var sums = {}, cnt = {};
    res.forEach(function(r){ var k = r.c.course; cnt[k] = cnt[k] || 0; if(cnt[k] < 3){ sums[k] = (sums[k] || 0) + r.score; cnt[k]++; } });
    var mx = Math.max.apply(null, Object.keys(sums).map(function(k){ return sums[k]; }).concat([1e-9]));
    res.forEach(function(r){ r.score *= 0.55 + 0.45 * Math.pow(sums[r.c.course] / mx, 1.5); });
    res.sort(function(a, b){ return b.score - a.score; });
  }
  var best = res.length ? res[0].score : 0, minScore = opts.min == null ? 4.0 : opts.min;
  var top = res.slice(0, opts.top || 6);
  var inScope = top.filter(function(r){ return !r.c.out; });
  var outTop = top.filter(function(r){ return r.c.out && r.score >= minScore; });
  var status = 'ok';
  if(!res.length || best < minScore) status = 'none';
  else if(outTop.length && outTop[0].score >= (inScope.length ? inScope[0].score * 0.5 : 0)) status = 'out';      // a specific out-of-scope phrase is among the best matches: warn
  return {status: status, results: top, best: best, tokens: wordsOnly};
}

/* kind of question (for the generic advice) */
var KINDS = [
  [/\b(which of the following|which statement|which one|which is|chon|phat bieu nao)/i, 'mcq-pick', 'Pick the true / false statement: test each option against the definition; one counter-example kills an option.', 'Chọn phát biểu đúng/sai: thử từng đáp án với định nghĩa; một phản ví dụ là loại được.'],
  [/\b(how many|count|number of|bao nhieu|dem)/i, 'count', 'Counting: list the cases systematically (by parameter, by interval) and check the endpoints.', 'Đếm: liệt kê các trường hợp có hệ thống (theo tham số, theo khoảng) và kiểm tra các đầu mút.'],
  [/\b(for which|find all|all values|determine (?:all )?(?:the )?values|with parameter|tham so)/i, 'param', 'Parameter question: isolate the quantity that depends on the parameter, find the critical values, then test each region and each critical value separately.', 'Câu có tham số: cô lập đại lượng phụ thuộc tham số, tìm giá trị tới hạn, rồi xét từng khoảng và từng giá trị tới hạn.'],
  [/\b(show that|prove|chung minh)/i, 'proof', 'Proof: write the definition of each object, start from the left side, and use only allowed properties; state the final line explicitly.', 'Chứng minh: viết định nghĩa của từng đối tượng, đi từ vế trái, chỉ dùng tính chất được phép; nêu rõ dòng kết luận.'],
  [/\b(sketch|graph|diagram|figure|plot|ve do thi|hinh)/i, 'figure', 'Graph / figure: read slopes, areas and intercepts; label the axes and units before you compute.', 'Đồ thị / hình: đọc độ dốc, diện tích và giao điểm; ghi rõ trục và đơn vị trước khi tính.'],
  [/\b(estimate|approximately|about|xap xi|uoc luong)/i, 'estimate', 'Estimate: keep 2–3 significant figures; check the order of magnitude.', 'Ước lượng: giữ 2–3 chữ số có nghĩa; kiểm tra bậc độ lớn.']
];
function kinds(text){
  var t = strip(text), out = [];
  KINDS.forEach(function(k){ if(k[0].test(t)) out.push({id: k[1], en: k[2], vi: k[3]}); });
  return out;
}

/* distinctive words of a question that no concept uses yet (shown as one-click suggestions in "Teach the system"); real words, not stems */
function candidates(model, text, n){
  var known = {};
  model.list.forEach(function(e){ e.kws.forEach(function(k){ k.t.forEach(function(t){ known[t] = 1; }); }); });
  var raw = String(text).replace(/\\[a-zA-Z]+/g, ' ').match(/[A-Za-z\u00C0-\u1EF9][A-Za-z\u00C0-\u1EF9'-]*[A-Za-z\u00C0-\u1EF9]/g) || [];
  var seen = {}, fresh = [], rest = [];
  raw.forEach(function(w){
    var lw = w.toLowerCase(), s = stem(strip(lw));
    if(s.length < 4 || STOP[s] || seen[s]) return;
    seen[s] = 1; (known[s] ? rest : fresh).push(lw);
  });
  var byLen = function(a, b){ return b.length - a.length; };
  return fresh.sort(byLen).concat(rest.sort(byLen)).slice(0, n || 8);
}

return {compile: compile, analyze: analyze, tokens: tokens, norm: norm, stem: stem, kinds: kinds, candidates: candidates, parseSpec: parseSpec};
});
