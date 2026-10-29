/* Calculus I lab (math.js): plot + derivative, limit explorer, Newton / bisection, Riemann sums and quadrature, series, Taylor polynomials,
   antiderivative checker, curve-sketching helper. Numerical tools are labelled as such: they support, never replace, the exact method. */
(function(){
'use strict';
var U = window.USTM, root = document.getElementById('lab'), math = window.math;
if(!root) return;
if(!math){ root.textContent = 'math.js did not load.'; return; }
function T(s){ return '$' + s + '$'; }
function D(s){ return '$$' + s + '$$'; }
function fx(expr){ var c = math.compile(expr.replace(/\^/g, '^')); return function(x){ var v = c.evaluate({x: x}); return typeof v === 'number' ? v : (v && v.re !== undefined ? (Math.abs(v.im) < 1e-12 ? v.re : NaN) : NaN); }; }
function num(v, nd){ nd = nd || 8; if(!isFinite(v)) return String(v); var a = Math.abs(v); return (a !== 0 && (a < 1e-6 || a >= 1e9)) ? v.toExponential(5) : String(+v.toFixed(nd)); }
function parseX(s){ s = String(s).trim().toLowerCase(); if(s === 'inf' || s === '+inf' || s === 'infinity') return Infinity; if(s === '-inf') return -Infinity; return math.evaluate(s.replace(/\bpi\b/g, 'pi')); }
function derivTex(expr, k){ var e = math.parse(expr), d = e; for(var i = 0; i < (k || 1); i++) d = math.simplify(math.derivative(d, 'x')); return d; }
var TOOLS = [];
function tool(id, title, fields, run, example){ TOOLS.push({id: id, title: title, fields: fields, run: run, example: example}); }

/* ---------------------------------------------------------------- canvas plotting */
function plot(host, curves, xmin, xmax, marks){
  var cv = U.el('canvas'); cv.width = 760; cv.height = 420; host.appendChild(cv);
  var g = cv.getContext('2d'), W = cv.width, H = cv.height, N = 700, ys = [];
  curves.forEach(function(c){ c.pts = []; for(var i = 0; i <= N; i++){ var x = xmin + (xmax - xmin) * i / N, y; try{ y = c.f(x); }catch(e){ y = NaN; } c.pts.push([x, y]); if(isFinite(y)) ys.push(y); } });
  ys.sort(function(a, b){ return a - b; });
  var lo = ys.length ? ys[Math.floor(ys.length * 0.02)] : -1, hi = ys.length ? ys[Math.floor(ys.length * 0.98)] : 1; if(lo === hi){ lo -= 1; hi += 1; } var pad = (hi - lo) * 0.12; lo -= pad; hi += pad;
  var X = function(x){ return (x - xmin) / (xmax - xmin) * W; }, Y = function(y){ return H - (y - lo) / (hi - lo) * H; };
  g.fillStyle = '#fff'; g.fillRect(0, 0, W, H); g.strokeStyle = '#e3e7f1'; g.lineWidth = 1; g.fillStyle = '#566074'; g.font = '12px sans-serif';
  var sx = niceStep((xmax - xmin) / 8), sy = niceStep((hi - lo) / 6);
  for(var x = Math.ceil(xmin / sx) * sx; x <= xmax; x += sx){ g.beginPath(); g.moveTo(X(x), 0); g.lineTo(X(x), H); g.stroke(); g.fillText(num(x, 3), X(x) + 2, Math.min(H - 4, Math.max(12, Y(0) + 12))); }
  for(var y = Math.ceil(lo / sy) * sy; y <= hi; y += sy){ g.beginPath(); g.moveTo(0, Y(y)); g.lineTo(W, Y(y)); g.stroke(); g.fillText(num(y, 3), Math.min(W - 40, Math.max(2, X(0) + 3)), Y(y) - 2); }
  g.strokeStyle = '#273896'; g.lineWidth = 1.6; g.beginPath(); if(lo < 0 && hi > 0){ g.moveTo(0, Y(0)); g.lineTo(W, Y(0)); } if(xmin < 0 && xmax > 0){ g.moveTo(X(0), 0); g.lineTo(X(0), H); } g.stroke();
  curves.forEach(function(c){ g.strokeStyle = c.color; g.lineWidth = 2.2; g.beginPath(); var pen = false, prev = null; c.pts.forEach(function(p){ var yy = p[1]; if(!isFinite(yy) || yy < lo - (hi - lo) || yy > hi + (hi - lo) || (prev !== null && Math.abs(yy - prev) > (hi - lo) * 1.5)){ pen = false; prev = isFinite(yy) ? yy : null; return; } if(!pen){ g.moveTo(X(p[0]), Y(yy)); pen = true; } else g.lineTo(X(p[0]), Y(yy)); prev = yy; }); g.stroke(); });
  (marks || []).forEach(function(m){ g.fillStyle = m.color || '#ED1C24'; g.beginPath(); g.arc(X(m.x), Y(m.y), 5, 0, 7); g.fill(); if(m.label){ g.fillStyle = '#1b2433'; g.fillText(m.label, X(m.x) + 7, Y(m.y) - 7); } });
  if(marks && marks.rects){ g.fillStyle = 'rgba(39,56,150,0.18)'; g.strokeStyle = 'rgba(39,56,150,0.7)'; marks.rects.forEach(function(r){ var y0 = Y(0), y1 = Y(r.h); g.fillRect(X(r.x0), Math.min(y0, y1), X(r.x1) - X(r.x0), Math.abs(y0 - y1)); g.strokeRect(X(r.x0), Math.min(y0, y1), X(r.x1) - X(r.x0), Math.abs(y0 - y1)); }); }
  return cv;
}
function niceStep(raw){ var p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p; return (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p; }

/* ---------------------------------------------------------------- tools */
tool('plot', 'Plot and derivative', [['f', 'f(x)', 0, 'x^3 - 3*x'], ['g', 'second curve g(x) (optional)', 0, ''], ['range', 'x from, to', 0, '-3, 3'], ['x0', 'Point x₀ for the tangent line', 0, '1']], function(f, host){
  var r = f.range.split(',').map(parseX), F = fx(f.f), curves = [{f: F, color: '#273896'}], x0 = parseX(f.x0), d1 = derivTex(f.f), dF = fx(d1.toString());
  if(f.g.trim()) curves.push({f: fx(f.g), color: '#1a7f37'});
  var y0 = F(x0), m = dF(x0), tl = function(x){ return y0 + m * (x - x0); };
  curves.push({f: tl, color: '#ED1C24'}); curves.push({f: dF, color: '#e08a00'});
  var h = '<p>' + T('f(x)=' + math.parse(f.f).toTex()) + ' (blue), tangent at ' + T('x_0=' + num(x0)) + ' (red), ' + T('f\'(x)') + ' (orange)' + (f.g.trim() ? ', second curve (green)' : '') + '.</p>';
  h += D('f\'(x)=' + d1.toTex()) + D('f\'\'(x)=' + derivTex(f.f, 2).toTex());
  h += '<p>At ' + T('x_0=' + num(x0)) + ': ' + T('f(x_0)=' + num(y0)) + ', ' + T('f\'(x_0)=' + num(m)) + '. Tangent line: ' + T('y=' + num(y0) + (m >= 0 ? '+' : '-') + num(Math.abs(m)) + '(x-' + num(x0) + ')') + '. Linearization ' + T('L(x)=f(x_0)+f\'(x_0)(x-x_0)') + '.</p>';
  host.innerHTML = h; plot(host, curves, r[0], r[1], [{x: x0, y: y0, label: '(' + num(x0, 3) + ', ' + num(y0, 3) + ')'}]);
}, {});

tool('limit', 'Limit explorer (numerical)', [['f', 'f(x)', 0, 'sin(x)/x'], ['a', 'x → a  (a number, pi, inf or -inf)', 0, '0']], function(f, host){
  var F = fx(f.f), a = parseX(f.a), h = '<p class="muted">Numerical evidence only: it suggests the limit, but a proof needs algebra, the squeeze theorem or L\'Hôpital.</p>';
  var rows = '';
  if(isFinite(a)){
    for(var k = 1; k <= 9; k++){ var e = Math.pow(10, -k); rows += '<tr><td>10<sup>−' + k + '</sup></td><td>' + num(F(a - e), 10) + '</td><td>' + num(F(a + e), 10) + '</td></tr>'; }
    h += '<table class="t"><tr><th>h</th><th>f(a − h)  (from the left)</th><th>f(a + h)  (from the right)</th></tr>' + rows + '</table>';
    var L = F(a - 1e-9), R = F(a + 1e-9);
    h += '<p><b>Left</b> ≈ ' + num(L, 6) + ', <b>right</b> ≈ ' + num(R, 6) + ': ' + ((Math.abs(L) > 1e6 || Math.abs(R) > 1e6) ? 'the values blow up (infinite limit or a vertical asymptote); compare the signs of the two sides.' : Math.abs(L - R) < 1e-5 * Math.max(1, Math.abs(L)) ? 'the one-sided values agree, so the limit is probably ' + num((L + R) / 2, 6) + '.' : 'the one-sided limits differ: the limit does not exist.') + '</p>';
  } else {
    var s = a > 0 ? 1 : -1;
    for(k = 1; k <= 10; k++){ var X = s * Math.pow(10, k); rows += '<tr><td>' + (s > 0 ? '' : '−') + '10<sup>' + k + '</sup></td><td>' + num(F(X), 10) + '</td></tr>'; }
    h += '<table class="t"><tr><th>x</th><th>f(x)</th></tr>' + rows + '</table>';
  }
  host.innerHTML = h;
}, {});

tool('newton', 'Newton\'s method and bisection', [['f', 'f(x)', 0, 'x^4 + x - 3'], ['x0', 'Starting point x₀ (Newton)', 0, '1'], ['n', 'Iterations', 0, '6'], ['ab', 'Bisection interval a, b', 0, '1, 2']], function(f, host){
  var F = fx(f.f), dF = fx(derivTex(f.f).toString()), x = parseX(f.x0), n = Math.min(40, parseInt(f.n || '6', 10)), h = '<p>Newton: ' + T('x_{n+1}=x_n-\\frac{f(x_n)}{f\'(x_n)}') + ', with ' + T('f\'(x)=' + derivTex(f.f).toTex()) + '.</p>';
  var rows = '<tr><td>0</td><td>' + num(x, 12) + '</td><td>' + num(F(x), 6) + '</td><td>–</td></tr>';
  for(var i = 1; i <= n; i++){ var d = dF(x); if(d === 0){ rows += '<tr><td colspan="4">f′(x) = 0: the tangent is horizontal, Newton fails.</td></tr>'; break; } var nx = x - F(x) / d; rows += '<tr><td>' + i + '</td><td>' + num(nx, 12) + '</td><td>' + num(F(nx), 6) + '</td><td>' + num(Math.abs(nx - x), 3) + '</td></tr>'; x = nx; }
  h += '<table class="t"><tr><th>n</th><th>xₙ</th><th>f(xₙ)</th><th>|xₙ − xₙ₋₁|</th></tr>' + rows + '</table>';
  var ab = f.ab.split(',').map(parseX), a = ab[0], b = ab[1]; rows = '';
  if(F(a) * F(b) > 0) h += '<p class="err">Bisection needs f(a) and f(b) of opposite signs (IVT).</p>'; else {
    for(i = 1; i <= 12; i++){ var c = (a + b) / 2, fc = F(c); rows += '<tr><td>' + i + '</td><td>' + num(a, 8) + '</td><td>' + num(b, 8) + '</td><td>' + num(c, 8) + '</td><td>' + num(fc, 4) + '</td></tr>'; if(F(a) * fc <= 0) b = c; else a = c; }
    h += '<h3>Bisection (IVT)</h3><table class="t"><tr><th>step</th><th>a</th><th>b</th><th>midpoint</th><th>f(mid)</th></tr>' + rows + '</table>';
  }
  host.innerHTML = h;
}, {});

tool('riemann', 'Riemann sums, trapezoid and Simpson', [['f', 'f(x)', 0, 'x^2 - 1'], ['ab', 'Interval a, b', 0, '0, 2'], ['n', 'Subintervals n (even for Simpson)', 0, '4'], ['rule', 'Draw the rectangles of: left | right | mid', 0, 'mid']], function(f, host){
  var F = fx(f.f), ab = f.ab.split(',').map(parseX), a = ab[0], b = ab[1], n = Math.max(1, Math.min(2000, parseInt(f.n || '4', 10))); if(n % 2) n++;
  var dx = (b - a) / n, L = 0, Rr = 0, M = 0, Tz = 0, S = F(a) + F(b), rects = [];
  for(var i = 0; i < n; i++){ var x0 = a + i * dx, x1 = x0 + dx; L += F(x0); Rr += F(x1); M += F((x0 + x1) / 2); Tz += (F(x0) + F(x1)) / 2; S += (i % 2 ? 2 : 4) * 0 ; }
  S = F(a) + F(b); for(i = 1; i < n; i++) S += (i % 2 ? 4 : 2) * F(a + i * dx);
  L *= dx; Rr *= dx; M *= dx; Tz *= dx; S *= dx / 3;
  var big = 20000, h2 = (b - a) / big, ref = F(a) + F(b); for(i = 1; i < big; i++) ref += (i % 2 ? 4 : 2) * F(a + i * h2); ref *= h2 / 3;
  var rule = f.rule.trim().toLowerCase();
  for(i = 0; i < n; i++){ var xl = a + i * dx, xr = xl + dx; rects.push({x0: xl, x1: xr, h: F(rule === 'left' ? xl : rule === 'right' ? xr : (xl + xr) / 2)}); }
  var h = '<p>' + T('\\Delta x=\\frac{b-a}{n}=' + num(dx, 6)) + ', ' + T('n=' + n) + '. Reference value (Simpson with 20 000 steps): ' + T(num(ref, 10)) + '.</p><table class="t"><tr><th>Rule</th><th>Value</th><th>Error vs reference</th></tr>' +
    [['Left endpoints', L], ['Right endpoints', Rr], ['Midpoints', M], ['Trapezoid', Tz], ['Simpson', S]].map(function(r){ return '<tr><td>' + r[0] + '</td><td>' + num(r[1], 8) + '</td><td>' + num(r[1] - ref, 3) + '</td></tr>'; }).join('') + '</table>';
  host.innerHTML = h; var m = []; m.rects = rects; plot(host, [{f: F, color: '#273896'}], a - (b - a) * 0.05, b + (b - a) * 0.05, m);
}, {});

tool('series', 'Series: partial sums and test hints', [['a', 'General term aₙ (variable n)', 0, '1/(n^2)'], ['n0', 'First index', 0, '1'], ['N', 'Number of terms', 0, '30']], function(f, host){
  var c = math.compile(f.a), n0 = parseInt(f.n0, 10), N = Math.min(200000, parseInt(f.N, 10)), s = 0, rows = '';
  function A(n){ var v = c.evaluate({n: n}); return typeof v === 'number' ? v : NaN; }
  var marks = [1, 2, 3, 4, 5, 10, 20, 50, 100, 200, 500, 1000, 5000, 10000, 100000].filter(function(k){ return k <= N; }); if(marks.indexOf(N) < 0) marks.push(N);
  for(var n = n0, k = 1; k <= N; n++, k++){ s += A(n); if(marks.indexOf(k) >= 0) rows += '<tr><td>' + k + '</td><td>' + num(A(n), 8) + '</td><td>' + num(s, 10) + '</td></tr>'; }
  var nn = n0 + N - 1, ratio = Math.abs(A(nn + 1) / A(nn)), root_ = Math.pow(Math.abs(A(nn)), 1 / nn);
  var h = '<table class="t"><tr><th>terms</th><th>last term aₙ</th><th>partial sum Sₙ</th></tr>' + rows + '</table>';
  h += '<p>At n = ' + nn + ': ' + T('|a_{n+1}/a_n|\\approx' + num(ratio, 6)) + ', ' + T('\\sqrt[n]{|a_n|}\\approx' + num(root_, 6)) + '. ';
  var an = Math.abs(A(nn));
  if(an > 1e-3 && N >= 20) h += 'The last term is not small: by the <i>n-th term test</i> the series probably <b>diverges</b>. ';
  else if(ratio < 0.97 && root_ < 0.99) h += 'Ratio and root are clearly below 1: probably <b>converges absolutely</b> (Ratio / Root test). ';
  else if(ratio > 1.03) h += 'The ratio is above 1: probably <b>diverges</b>. ';
  else h += 'Ratio ≈ 1: the Ratio and Root tests are inconclusive; try comparison, the integral test or the alternating series test. ';
  host.innerHTML = h + '</p><p class="muted">Partial sums are numerical evidence only. Slowly diverging series (like Σ 1/n) look like they converge — always prove the verdict with a test.</p>';
}, {});

tool('taylor', 'Taylor polynomial and error', [['f', 'f(x)', 0, 'sin(x)'], ['a', 'Center a', 0, '0'], ['n', 'Degree n', 0, '5'], ['x0', 'Evaluate at x₀', 0, '0.5'], ['range', 'Plot range', 0, '-4, 4']], function(f, host){
  var a = parseX(f.a), n = Math.min(12, parseInt(f.n, 10)), x0 = parseX(f.x0), r = f.range.split(',').map(parseX), F = fx(f.f), d = math.parse(f.f), cs = [], tex = [];
  var fact = 1;
  for(var k = 0; k <= n; k++){ if(k > 0){ d = math.simplify(math.derivative(d, 'x')); fact *= k; } var val = d.evaluate({x: a}) / fact; cs.push(val); if(Math.abs(val) > 1e-12) tex.push((val < 0 ? '-' : (tex.length ? '+' : '')) + (Math.abs(Math.abs(val) - 1) < 1e-12 && k > 0 ? '' : num(Math.abs(val), 6)) + (k === 0 ? '' : '(x' + (a === 0 ? '' : (a < 0 ? '+' + num(-a) : '-' + num(a))) + ')' + (k > 1 ? '^{' + k + '}' : ''))); }
  var P = function(x){ var s = 0; for(var k2 = 0; k2 <= n; k2++) s += cs[k2] * Math.pow(x - a, k2); return s; };
  var dn1 = d, nextD = math.simplify(math.derivative(d, 'x')), g = function(x){ return nextD.evaluate({x: x}); }, mx = 0, lo = Math.min(a, x0), hi = Math.max(a, x0);
  for(var i = 0; i <= 400; i++){ var xx = lo + (hi - lo) * i / 400, vv = Math.abs(g(xx)); if(isFinite(vv)) mx = Math.max(mx, vv); }
  var bound = mx * Math.pow(Math.abs(x0 - a), n + 1) / math.factorial(n + 1);
  var h = D('P_{' + n + '}(x)=' + tex.join('')) + '<p>' + T('f(' + num(x0) + ')=' + num(F(x0), 10)) + ', ' + T('P_{' + n + '}(' + num(x0) + ')=' + num(P(x0), 10)) + ', actual error ' + T(num(Math.abs(F(x0) - P(x0)), 4)) + '. Lagrange bound ' + T('|R_n|\\le\\frac{M|x-a|^{n+1}}{(n+1)!}') + ' with ' + T('M\\approx' + num(mx, 5)) + ' (max of ' + T('|f^{(n+1)}|') + ' between ' + T('a') + ' and ' + T('x_0') + '): ' + T('\\le' + num(bound, 4)) + '.</p>';
  host.innerHTML = h; plot(host, [{f: F, color: '#273896'}, {f: P, color: '#ED1C24'}], r[0], r[1], [{x: x0, y: F(x0), label: 'x₀'}]);
}, {});

tool('check', 'Antiderivative / derivative checker', [['f', 'Integrand f(x)', 0, 'x*cos(x^2)'], ['F', 'Your antiderivative F(x) (without +C)', 0, 'sin(x^2)/2'], ['ab', 'Definite integral limits a, b (optional)', 0, '0, 1']], function(f, host){
  var F0 = fx(f.f), F1 = fx(f.F), worst = 0, bad = null, pts = [];
  for(var i = 0; i < 40; i++){ pts.push(-2.7 + 5.4 * ((i * 0.6180339887) % 1)); }
  pts.forEach(function(x){ var hh = 1e-5, d = (F1(x + hh) - F1(x - hh)) / (2 * hh), e = F0(x); if(isFinite(d) && isFinite(e)){ var err = Math.abs(d - e) / Math.max(1, Math.abs(e)); if(err > worst){ worst = err; bad = x; } } });
  var h = (worst < 1e-6 ? '<p>✅ <b>F′(x) = f(x)</b> at all 40 test points (largest relative difference ' + worst.toExponential(2) + '): your antiderivative is correct (up to the constant).</p>' : '<p class="err">❌ F′(x) ≠ f(x): at x = ' + num(bad, 4) + ' they differ (relative error ' + worst.toExponential(2) + '). Differentiate your F with the chain/product rule and compare.</p>');
  h += '<p>Exact derivative of your F: ' + T('F\'(x)=' + derivTex(f.F).toTex()) + '</p>';
  if(f.ab.trim()){ var ab = f.ab.split(',').map(parseX), a = ab[0], b = ab[1], n = 20000, hh = (b - a) / n, s = F0(a) + F0(b); for(i = 1; i < n; i++) s += (i % 2 ? 4 : 2) * F0(a + i * hh); s *= hh / 3; h += '<p>' + T('\\int_{' + num(a) + '}^{' + num(b) + '}f\\,dx') + ': Simpson ≈ ' + T(num(s, 10)) + '; ' + T('F(b)-F(a)=' + num(F1(b) - F1(a), 10)) + (Math.abs(s - (F1(b) - F1(a))) < 1e-6 ? ' ✅ (FTC part 2)' : ' ⚠ (check the limits and F)') + '.</p>'; }
  host.innerHTML = h;
}, {});

tool('sketch', 'Curve-sketching helper', [['f', 'f(x)', 0, 'x^3/3 - x^2/2 - 2*x + 1/3'], ['range', 'Search interval', 0, '-4, 4']], function(f, host){
  var F = fx(f.f), d1 = derivTex(f.f), d2 = derivTex(f.f, 2), D1 = fx(d1.toString()), D2 = fx(d2.toString()), r = f.range.split(',').map(parseX), h = '';
  function roots(g, lo, hi){ var out = [], n = 4000, prev = g(lo), px = lo; for(var i = 1; i <= n; i++){ var x = lo + (hi - lo) * i / n, v = g(x); if(v === 0){ out.push(x); } else if(isFinite(prev) && isFinite(v) && prev * v < 0 && Math.abs(prev - v) < 1e3){ var a = px, b = x; for(var k = 0; k < 60; k++){ var m = (a + b) / 2; if(g(a) * g(m) <= 0) b = m; else a = m; } out.push((a + b) / 2); } prev = v; px = x; } return out; }
  var cps = roots(D1, r[0], r[1]), ips = roots(D2, r[0], r[1]);
  h += D('f\'(x)=' + d1.toTex()) + D('f\'\'(x)=' + d2.toTex());
  h += '<table class="t"><tr><th>Critical point x</th><th>f(x)</th><th>f″(x)</th><th>Type (second derivative test)</th></tr>' + (cps.map(function(x){ var s = D2(x); return '<tr><td>' + num(x, 6) + '</td><td>' + num(F(x), 6) + '</td><td>' + num(s, 5) + '</td><td>' + (s > 1e-7 ? 'local minimum' : s < -1e-7 ? 'local maximum' : 'inconclusive (use the first derivative test)') + '</td></tr>'; }).join('') || '<tr><td colspan="4">none found in the interval</td></tr>') + '</table>';
  h += '<table class="t"><tr><th>Inflection candidate x</th><th>f(x)</th></tr>' + (ips.map(function(x){ return '<tr><td>' + num(x, 6) + '</td><td>' + num(F(x), 6) + '</td></tr>'; }).join('') || '<tr><td colspan="2">none found</td></tr>') + '</table>';
  var big = [F(1e6), F(-1e6)];
  h += '<p>Behaviour at infinity (numerical): ' + T('f(10^6)\\approx' + num(big[0], 4)) + ', ' + T('f(-10^6)\\approx' + num(big[1], 4)) + '. Sign of ' + T('f\'') + ' on the intervals between critical points tells you where ' + T('f') + ' increases or decreases.</p>';
  host.innerHTML = h; var marks = cps.map(function(x){ return {x: x, y: F(x), label: 'crit'}; }).concat(ips.map(function(x){ return {x: x, y: F(x), color: '#1a7f37', label: 'infl'}; }));
  plot(host, [{f: F, color: '#273896'}, {f: D1, color: '#e08a00'}], r[0], r[1], marks);
}, {});

/* ---------------------------------------------------------------- UI */
function build(){
  root.innerHTML = '';
  var tabs = U.el('div', 'tabs'); root.appendChild(tabs);
  var box = U.el('div', 'panel'); root.appendChild(box);
  function open(id){
    var t = TOOLS.filter(function(x){ return x.id === id; })[0] || TOOLS[0];
    U.$$('button', tabs).forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-id') === t.id); });
    box.innerHTML = ''; box.appendChild(U.el('h3', null, t.title));
    var inputs = {}; t.fields.forEach(function(fd){ var lab = U.el('label', null, fd[1]); lab.style.display = 'block'; lab.style.marginTop = '6px'; var el = U.el('input'); el.type = 'text'; el.value = fd[3]; inputs[fd[0]] = el; box.appendChild(lab); box.appendChild(el); });
    var go = U.el('button', 'btn', '▶ Compute'), out = U.el('div', 'out lab-out'); box.appendChild(go); box.appendChild(out);
    function run(){ var vals = {}; Object.keys(inputs).forEach(function(k){ vals[k] = inputs[k].value; }); try{ t.run(vals, out); }catch(e){ out.innerHTML = '<p class="err">⚠ ' + String(e.message || e).replace(/</g, '&lt;') + '</p>'; } U.math(out); }
    go.onclick = run; Object.keys(inputs).forEach(function(k){ inputs[k].onkeydown = function(e){ if(e.key === 'Enter') run(); }; }); run();
    try{ history.replaceState(null, '', '#tool=' + t.id); }catch(e){}
  }
  TOOLS.forEach(function(t){ var b = U.el('button', null, t.title.split(':')[0].split(' (')[0]); b.setAttribute('data-id', t.id); b.onclick = function(){ open(t.id); }; tabs.appendChild(b); });
  var m = /tool=([a-z]+)/.exec(location.hash); open(m ? m[1] : 'plot');
}
build();
})();
