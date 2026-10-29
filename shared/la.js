/* Exact linear algebra in the browser (BigInt rationals): row reduction with steps, solve, determinant, inverse, rank/null/column
   spaces, characteristic polynomial, rational eigenvalues/eigenvectors, Gram-Schmidt, LU, Cramer, Jacobi / Gauss-Seidel.
   UMD module: window.LA in the browser, require() in Node (tests/la_cross_check.js compares it with sympy). */
(function(root, factory){ if(typeof module === 'object' && module.exports) module.exports = factory(); else root.LA = factory(); })(typeof self !== 'undefined' ? self : this, function(){
'use strict';

/* ---------------------------------------------------------------- rationals */
function gcd(a, b){ a = a < 0n ? -a : a; b = b < 0n ? -b : b; while(b){ var t = a % b; a = b; b = t; } return a; }
function Q(n, d){ if(!(this instanceof Q)) return new Q(n, d); n = BigInt(n); d = d === undefined ? 1n : BigInt(d); if(d === 0n) throw new Error('division by zero'); if(d < 0n){ n = -n; d = -d; } var g = gcd(n, d) || 1n; this.n = n / g; this.d = d / g; }
Q.prototype.add = function(o){ return new Q(this.n * o.d + o.n * this.d, this.d * o.d); };
Q.prototype.sub = function(o){ return new Q(this.n * o.d - o.n * this.d, this.d * o.d); };
Q.prototype.mul = function(o){ return new Q(this.n * o.n, this.d * o.d); };
Q.prototype.div = function(o){ if(o.n === 0n) throw new Error('division by zero'); return new Q(this.n * o.d, this.d * o.n); };
Q.prototype.neg = function(){ return new Q(-this.n, this.d); };
Q.prototype.isZero = function(){ return this.n === 0n; };
Q.prototype.isOne = function(){ return this.n === 1n && this.d === 1n; };
Q.prototype.cmp = function(o){ var a = this.n * o.d, b = o.n * this.d; return a < b ? -1 : a > b ? 1 : 0; };
Q.prototype.eq = function(o){ return this.n === o.n && this.d === o.d; };
Q.prototype.sign = function(){ return this.n === 0n ? 0 : this.n < 0n ? -1 : 1; };
Q.prototype.abs = function(){ return this.n < 0n ? this.neg() : this; };
Q.prototype.toNumber = function(){ return Number(this.n) / Number(this.d); };
Q.prototype.toString = function(){ return this.d === 1n ? this.n.toString() : this.n + '/' + this.d; };
Q.prototype.tex = function(){ if(this.d === 1n) return this.n.toString(); return (this.n < 0n ? '-' : '') + '\\frac{' + (this.n < 0n ? -this.n : this.n) + '}{' + this.d + '}'; };
Q.prototype.pow = function(k){ var r = new Q(1), b = this; for(var i = 0; i < k; i++) r = r.mul(b); return r; };
var ZERO = new Q(0), ONE = new Q(1);
function q(x){
  if(x instanceof Q) return x;
  if(typeof x === 'number'){ if(Number.isInteger(x)) return new Q(x); return q(String(x)); }
  var s = String(x).trim().replace(/−/g, '-');
  var m;
  if((m = /^([+-]?\d+)\s*\/\s*(\d+)$/.exec(s))) return new Q(m[1], m[2]);
  if((m = /^([+-]?)(\d*)\.(\d+)$/.exec(s))){ var den = 10n ** BigInt(m[3].length); return new Q(BigInt((m[1] === '-' ? '-' : '') + (m[2] || '0')) * den + (m[1] === '-' ? -1n : 1n) * BigInt(m[3]), den); }
  if(/^[+-]?\d+$/.test(s)) return new Q(s);
  throw new Error('cannot read "' + s + '" as a number');
}

/* ---------------------------------------------------------------- matrices */
function parseMatrix(text){
  if(Array.isArray(text)) return text.map(function(r){ return r.map(q); });
  var rows = String(text).trim().split(/\n|;/).map(function(r){ return r.trim(); }).filter(Boolean);
  var M = rows.map(function(r){ return r.replace(/[\[\]]/g, ' ').split(/[\s,]+/).filter(Boolean).map(q); });
  if(!M.length) throw new Error('empty matrix');
  var w = M[0].length; M.forEach(function(r){ if(r.length !== w) throw new Error('rows must have the same number of entries'); });
  return M;
}
function clone(M){ return M.map(function(r){ return r.slice(); }); }
function ident(n){ var I = []; for(var i = 0; i < n; i++){ I.push([]); for(var j = 0; j < n; j++) I[i].push(i === j ? ONE : ZERO); } return I; }
function zeros(r, c){ var Z = []; for(var i = 0; i < r; i++){ Z.push([]); for(var j = 0; j < c; j++) Z[i].push(ZERO); } return Z; }
function transpose(M){ return M[0].map(function(_, j){ return M.map(function(r){ return r[j]; }); }); }
function mul(A, B){
  if(A[0].length !== B.length) throw new Error('size mismatch: ' + A.length + '×' + A[0].length + ' times ' + B.length + '×' + B[0].length);
  return A.map(function(r){ return B[0].map(function(_, j){ var s = ZERO; for(var k = 0; k < r.length; k++) s = s.add(r[k].mul(B[k][j])); return s; }); });
}
function mmap(M, f){ return M.map(function(r){ return r.map(f); }); }
function eqM(A, B){ return A.length === B.length && A.every(function(r, i){ return r.every(function(x, j){ return x.eq(B[i][j]); }); }); }
function texMat(M, ncoef){
  var body = M.map(function(r){ return r.map(function(x){ return x.tex(); }).join(' & '); }).join(' \\\\ ');
  if(ncoef !== undefined && ncoef < M[0].length) return '\\left[\\begin{array}{' + 'c'.repeat(ncoef) + '|' + 'c'.repeat(M[0].length - ncoef) + '}' + body + '\\end{array}\\right]';
  return '\\begin{bmatrix}' + body + '\\end{bmatrix}';
}
function texVec(v){ return '(' + v.map(function(x){ return x.tex(); }).join(',\\ ') + ')'; }

/* ---------------------------------------------------------------- row reduction */
function coefTex(c){ return c.isOne() ? '' : c.tex(); }
function opScale(r, c){ return 'R_{' + (r + 1) + '}\\leftarrow ' + coefTex(c) + 'R_{' + (r + 1) + '}'; }
function opAdd(i, f, r){ return 'R_{' + (i + 1) + '}\\leftarrow R_{' + (i + 1) + '}' + (f.sign() > 0 ? '+' : '-') + coefTex(f.abs()) + 'R_{' + (r + 1) + '}'; }
function opSwap(i, j){ return 'R_{' + (i + 1) + '}\\leftrightarrow R_{' + (j + 1) + '}'; }
function rowReduce(M0, ncoef, reduced){
  var M = clone(M0), rows = M.length, steps = [], pivots = [], r = 0;
  ncoef = ncoef === undefined ? M[0].length : ncoef;
  for(var c = 0; c < ncoef && r < rows; c++){
    var p = -1; for(var i = r; i < rows; i++) if(!M[i][c].isZero()){ p = i; break; }
    if(p < 0) continue;
    if(p !== r){ var t = M[p]; M[p] = M[r]; M[r] = t; steps.push({op: opSwap(p, r), M: clone(M)}); }
    if(reduced && !M[r][c].isOne()){ var piv = M[r][c]; M[r] = M[r].map(function(x){ return x.div(piv); }); steps.push({op: opScale(r, ONE.div(piv)), M: clone(M)}); }
    for(i = 0; i < rows; i++){
      if(i !== r && !M[i][c].isZero() && (reduced || i > r)){
        var f = M[i][c].div(M[r][c]); M[i] = M[i].map(function(x, j){ return x.sub(f.mul(M[r][j])); });
        steps.push({op: opAdd(i, f.neg(), r), M: clone(M)});
      }
    }
    pivots.push(c); r++;
  }
  return {M: M, steps: steps, pivots: pivots};
}
function rank(M){ return rowReduce(M, M[0].length, false).pivots.length; }
function rref(M){ return rowReduce(M, M[0].length, true); }

/* ---------------------------------------------------------------- solving Ax = b */
var PARAMS = ['t', 's', 'u', 'v'];
function solve(A, b){
  var n = A[0].length, aug = A.map(function(r, i){ return r.concat([b[i]]); });
  var R = rowReduce(aug, n, true), M = R.M, piv = R.pivots;
  for(var i = 0; i < M.length; i++){
    if(M[i].slice(0, n).every(function(x){ return x.isZero(); }) && !M[i][n].isZero()) return {kind: 'none', R: R};
  }
  var free = []; for(var j = 0; j < n; j++) if(piv.indexOf(j) < 0) free.push(j);
  if(!free.length){ var sol = new Array(n); piv.forEach(function(c, i){ sol[c] = M[i][n]; }); return {kind: 'unique', sol: sol, R: R}; }
  // general solution: x = p + sum t_k d_k
  var p = new Array(n).fill(ZERO), dirs = free.map(function(){ return new Array(n).fill(ZERO); });
  free.forEach(function(f, k){ dirs[k][f] = ONE; });
  piv.forEach(function(c, i){ p[c] = M[i][n]; free.forEach(function(f, k){ dirs[k][c] = M[i][f].neg(); }); });
  return {kind: 'inf', particular: p, dirs: dirs, free: free, R: R};
}
function paramTex(res, names){
  var n = res.particular.length; names = names || Array.from({length: n}, function(_, j){ return 'x_{' + (j + 1) + '}'; });
  return res.particular.map(function(p0, j){
    var terms = []; if(!p0.isZero()) terms.push(p0.tex());
    res.dirs.forEach(function(d, k){ var c = d[j]; if(c.isZero()) return; var cs = c.isOne() ? '' : c.eq(ONE.neg()) ? '-' : c.tex(); terms.push((terms.length && c.sign() > 0 ? '+' : '') + cs + PARAMS[k]); });
    return names[j] + '=' + (terms.length ? terms.join('').replace(/\+-/g, '-') : '0');
  }).join(',\\ ');
}
function gaussBackSub(A, b){
  // Gaussian elimination to echelon form, then back-substitution (unique solution only)
  var n = A[0].length, aug = A.map(function(r, i){ return r.concat([b[i]]); }), R = rowReduce(aug, n, false), M = R.M, piv = R.pivots;
  if(piv.length < n) return null;
  for(var i = 0; i < M.length; i++) if(M[i].slice(0, n).every(function(x){ return x.isZero(); }) && !M[i][n].isZero()) return null;
  var x = new Array(n).fill(ZERO), lines = [];
  for(i = n - 1; i >= 0; i--){ var s = M[i][n]; for(var j = i + 1; j < n; j++) s = s.sub(M[i][j].mul(x[j])); x[i] = s.div(M[i][i]); lines.push('x_{' + (i + 1) + '}=' + x[i].tex()); }
  return {x: x, echelon: M, steps: R.steps, lines: lines};
}

/* ---------------------------------------------------------------- determinant, inverse, cofactors */
function det(M0){
  var M = clone(M0), n = M.length, d = ONE;
  for(var c = 0; c < n; c++){
    var p = -1; for(var i = c; i < n; i++) if(!M[i][c].isZero()){ p = i; break; }
    if(p < 0) return ZERO;
    if(p !== c){ var t = M[p]; M[p] = M[c]; M[c] = t; d = d.neg(); }
    d = d.mul(M[c][c]);
    for(i = c + 1; i < n; i++){ var f = M[i][c].div(M[c][c]); for(var j = c; j < n; j++) M[i][j] = M[i][j].sub(f.mul(M[c][j])); }
  }
  return d;
}
function detSteps(M0){
  var M = clone(M0), n = M.length, sign = 1, steps = [], diag = null;
  for(var c = 0; c < n; c++){
    var p = -1; for(var i = c; i < n; i++) if(!M[i][c].isZero()){ p = i; break; }
    if(p < 0) return {det: ZERO, steps: steps, zero: true};
    if(p !== c){ var t = M[p]; M[p] = M[c]; M[c] = t; sign = -sign; steps.push({op: opSwap(p, c) + '\\ (\\det\\times(-1))', M: clone(M)}); }
    for(i = c + 1; i < n; i++) if(!M[i][c].isZero()){ var f = M[i][c].div(M[c][c]); M[i] = M[i].map(function(x, j){ return x.sub(f.mul(M[c][j])); }); steps.push({op: opAdd(i, f.neg(), c), M: clone(M)}); }
  }
  var d = sign < 0 ? ONE.neg() : ONE; for(i = 0; i < n; i++) d = d.mul(M[i][i]);
  return {det: d, steps: steps, tri: M, sign: sign};
}
function minorM(M, i, j){ return M.filter(function(_, r){ return r !== i; }).map(function(r){ return r.filter(function(_, c){ return c !== j; }); }); }
function cofactor(M, i, j){ var d = M.length === 1 ? ONE : det(minorM(M, i, j)); return (i + j) % 2 ? d.neg() : d; }
function cofactorExpansion(M, row){
  var n = M.length, terms = [], total = ZERO;
  for(var j = 0; j < n; j++){ var c = cofactor(M, row, j); total = total.add(M[row][j].mul(c)); terms.push({a: M[row][j], cof: c}); }
  return {total: total, terms: terms};
}
function adjugate(M){ var n = M.length; return transpose(M.map(function(r, i){ return r.map(function(_, j){ return cofactor(M, i, j); }); })); }
function inverse(A){
  var n = A.length, R = rowReduce(A.map(function(r, i){ return r.concat(ident(n)[i]); }), n, true), M = R.M;
  var ok = M.every(function(r, i){ return r.slice(0, n).every(function(x, j){ return x.eq(i === j ? ONE : ZERO); }); });
  return ok ? {inv: M.map(function(r){ return r.slice(n); }), steps: R.steps} : null;
}
function cramer(A, b){
  var d = det(A); if(d.isZero()) return null;
  var xs = [], dets = [];
  for(var j = 0; j < A[0].length; j++){ var Aj = clone(A); for(var i = 0; i < A.length; i++) Aj[i][j] = b[i]; var dj = det(Aj); dets.push(dj); xs.push(dj.div(d)); }
  return {det: d, dets: dets, x: xs};
}

/* ---------------------------------------------------------------- subspaces */
function nullspace(A){
  var n = A[0].length, R = rowReduce(A, n, true), M = R.M, piv = R.pivots, out = [];
  for(var f = 0; f < n; f++){ if(piv.indexOf(f) >= 0) continue; var v = new Array(n).fill(ZERO); v[f] = ONE; piv.forEach(function(c, i){ v[c] = M[i][f].neg(); }); out.push(v); }
  return out;
}
function columnSpaceBasis(A){ var R = rowReduce(A, A[0].length, true); return R.pivots.map(function(c){ return A.map(function(r){ return r[c]; }); }); }
function rowSpaceBasis(A){ var R = rowReduce(A, A[0].length, true); return R.M.filter(function(r){ return r.some(function(x){ return !x.isZero(); }); }); }
function dot(u, v){ var s = ZERO; for(var i = 0; i < u.length; i++) s = s.add(u[i].mul(v[i])); return s; }
function gramSchmidt(vs){
  var us = [], ns = [];
  vs.forEach(function(v){ var w = v.slice(); us.forEach(function(u, k){ var c = dot(v, u).div(ns[k]); w = w.map(function(x, i){ return x.sub(c.mul(u[i])); }); }); var nn = dot(w, w); if(nn.isZero()) throw new Error('the vectors are linearly dependent'); us.push(w); ns.push(nn); });
  return {u: us, norm2: ns};
}
function sqrtTex(r){            // sqrt of a positive rational as simplified TeX
  var n = r.n, d = r.d;
  function sq(x){ var k = 1n, m = x; for(var p = 2n; p * p <= m && p < 100000n; p++){ while(m % (p * p) === 0n){ m /= p * p; k *= p; } } return [k, m]; }
  var a = sq(n), b = sq(d); // sqrt(n/d) = (a0 sqrt(a1)) / (b0 sqrt(b1)) = a0 sqrt(a1 b1) / (b0 b1)
  var num = a[1] * b[1], k = a[0], den = b[0] * b[1], g = gcd(k, den); k /= g; den /= g;
  var rad = num === 1n ? '' : '\\sqrt{' + num + '}', coef = k === 1n && rad ? '' : k.toString();
  var top = coef + rad || '1';
  return den === 1n ? top : '\\frac{' + top + '}{' + den + '}';
}
function project(u, basisOrth, norm2){ var p = new Array(u.length).fill(ZERO); basisOrth.forEach(function(b, k){ var c = dot(u, b).div(norm2[k]); p = p.map(function(x, i){ return x.add(c.mul(b[i])); }); }); return p; }
function leastSquares(xs, ys, deg){
  deg = deg === undefined ? 1 : deg; var X = xs.map(function(x){ var r = []; for(var k = 0; k <= deg; k++) r.push(x.pow(k)); return r; });
  var XT = transpose(X), N = mul(XT, X), rhs = mul(XT, ys.map(function(y){ return [y]; })).map(function(r){ return r[0]; });
  var s = solve(N, rhs); return s.kind === 'unique' ? {coef: s.sol, normal: N, rhs: rhs} : null;
}

/* ---------------------------------------------------------------- LU */
function lu(A){
  var n = A.length, L = ident(n), U = clone(A), P = ident(n), swaps = 0;
  for(var c = 0; c < n; c++){
    var p = -1; for(var i = c; i < n; i++) if(!U[i][c].isZero()){ p = i; break; }
    if(p < 0) continue;
    if(p !== c){ var t = U[p]; U[p] = U[c]; U[c] = t; t = P[p]; P[p] = P[c]; P[c] = t; for(var j = 0; j < c; j++){ t = L[p][j]; L[p][j] = L[c][j]; L[c][j] = t; } swaps++; }
    for(i = c + 1; i < n; i++){ var f = U[i][c].div(U[c][c]); L[i][c] = f; U[i] = U[i].map(function(x, j){ return x.sub(f.mul(U[c][j])); }); }
  }
  return {L: L, U: U, P: P, swaps: swaps};
}

/* ---------------------------------------------------------------- characteristic polynomial and eigenvalues */
function charpoly(A){          // det(lambda I - A) = sum c_k lambda^k, Faddeev-LeVerrier (exact)
  var n = A.length, I = ident(n), M = zeros(n, n), c = new Array(n + 1).fill(ZERO); c[n] = ONE;
  for(var k = 1; k <= n; k++){
    M = mul(A, M); for(var i = 0; i < n; i++) M[i][i] = M[i][i].add(c[n - k + 1]);
    var AM = mul(A, M), tr = ZERO; for(i = 0; i < n; i++) tr = tr.add(AM[i][i]);
    c[n - k] = tr.div(new Q(k)).neg();
  }
  return c;
}
function polyEval(c, x){ var r = ZERO; for(var i = c.length - 1; i >= 0; i--) r = r.mul(x).add(c[i]); return r; }
function polyDivLinear(c, r){   // divide by (x - r) exactly
  var n = c.length - 1, out = new Array(n); var carry = ZERO;
  for(var i = n; i >= 1; i--){ carry = c[i].add(carry.mul(r)); out[i - 1] = carry; }
  return out;
}
function divisors(x){ x = x < 0n ? -x : x; var out = []; for(var i = 1n; i * i <= x && i < 2000000n; i++){ if(x % i === 0n){ out.push(i); if(i * i !== x) out.push(x / i); } } return out; }
function ratRoots(c){
  var poly = c.slice(), roots = [];
  // clear denominators
  var L = 1n; poly.forEach(function(x){ L = L / gcd(L, x.d) * x.d; });
  var ints = poly.map(function(x){ return x.n * (L / x.d); });
  var lowIdx = 0; while(lowIdx < ints.length && ints[lowIdx] === 0n) lowIdx++;
  if(lowIdx > 0){ roots.push({r: ZERO, m: lowIdx}); poly = poly.slice(lowIdx); ints = ints.slice(lowIdx); }
  var guard = 0;
  while(poly.length > 1 && guard++ < 50){
    var a0 = ints[0], an = ints[ints.length - 1], found = null;
    var ps = divisors(a0), qs = divisors(an);
    outer: for(var i = 0; i < ps.length; i++) for(var j = 0; j < qs.length; j++) for(var sg = 0; sg < 2; sg++){
      var cand = new Q(sg ? -ps[i] : ps[i], qs[j]);
      if(polyEval(poly, cand).isZero()){ found = cand; break outer; }
    }
    if(!found) break;
    var m = 0; while(poly.length > 1 && polyEval(poly, found).isZero()){ poly = polyDivLinear(poly, found); m++; }
    roots.push({r: found, m: m});
    L = 1n; poly.forEach(function(x){ L = L / gcd(L, x.d) * x.d; }); ints = poly.map(function(x){ return x.n * (L / x.d); });
  }
  return {roots: roots.sort(function(a, b){ return a.r.cmp(b.r); }), rest: poly};
}
function numericRoots(c){        // Durand–Kerner for the remaining polynomial (floating point, complex)
  var n = c.length - 1; if(n <= 0) return [];
  var a = c.map(function(x){ return x.toNumber(); }), lead = a[n]; a = a.map(function(x){ return x / lead; });
  var z = []; for(var k = 0; k < n; k++){ var ang = 2 * Math.PI * k / n + 0.4; z.push([Math.pow(0.9, 1) * Math.cos(ang) * (1 + k * 0.1), Math.sin(ang) * (1 + k * 0.1)]); }
  function cmul(p, q2){ return [p[0] * q2[0] - p[1] * q2[1], p[0] * q2[1] + p[1] * q2[0]]; }
  function cdiv(p, q2){ var d = q2[0] * q2[0] + q2[1] * q2[1]; return [(p[0] * q2[0] + p[1] * q2[1]) / d, (p[1] * q2[0] - p[0] * q2[1]) / d]; }
  function ev(x){ var r = [a[n], 0]; for(var i = n - 1; i >= 0; i--){ r = cmul(r, x); r[0] += a[i]; } return r; }
  for(var it = 0; it < 500; it++){
    var delta = 0;
    for(var i = 0; i < n; i++){ var den = [1, 0]; for(var j = 0; j < n; j++) if(j !== i) den = cmul(den, [z[i][0] - z[j][0], z[i][1] - z[j][1]]); var dz = cdiv(ev(z[i]), den); z[i] = [z[i][0] - dz[0], z[i][1] - dz[1]]; delta = Math.max(delta, Math.abs(dz[0]) + Math.abs(dz[1])); }
    if(delta < 1e-13) break;
  }
  return z.map(function(w){ return {re: Math.abs(w[0]) < 1e-9 ? 0 : w[0], im: Math.abs(w[1]) < 1e-9 ? 0 : w[1]}; });
}
function eigen(A){
  var n = A.length, cp = charpoly(A), rr = ratRoots(cp);
  var vals = rr.roots.map(function(o){
    var N = nullspace(A.map(function(r, i){ return r.map(function(x, j){ return i === j ? x.sub(o.r) : x; }); }));
    return {val: o.r, alg: o.m, vectors: N, geo: N.length};
  });
  var diag = rr.rest.length === 1 && vals.every(function(v){ return v.geo === v.alg; });
  var P = null, D = null;
  if(diag){ var cols = []; var dg = []; vals.forEach(function(v){ v.vectors.forEach(function(x){ cols.push(x); dg.push(v.val); }); }); P = transpose(cols); D = zeros(n, n); dg.forEach(function(d, i){ D[i][i] = d; }); }
  return {charpoly: cp, values: vals, rest: rr.rest, restRoots: rr.rest.length > 1 ? numericRoots(rr.rest) : [], diagonalizable: diag, P: P, D: D};
}
function powerMat(A, k){ var R = ident(A.length), B = A; while(k > 0){ if(k & 1) R = mul(R, B); B = mul(B, B); k >>= 1; } return R; }

/* ---------------------------------------------------------------- iterative methods (floating point) */
function diagDominant(A){ return A.every(function(r, i){ var s = 0; r.forEach(function(x, j){ if(j !== i) s += Math.abs(x.toNumber()); }); return Math.abs(r[i].toNumber()) > s; }); }
function iterate(A, b, x0, N, method){
  var n = A.length, a = A.map(function(r){ return r.map(function(x){ return x.toNumber(); }); }), bb = b.map(function(x){ return x.toNumber(); }), x = x0.slice(), rows = [x.slice()];
  for(var it = 0; it < N; it++){
    var nx = x.slice();
    for(var i = 0; i < n; i++){ var s = bb[i]; for(var j = 0; j < n; j++) if(j !== i) s -= a[i][j] * (method === 'gs' ? nx[j] : x[j]); nx[i] = s / a[i][i]; }
    x = nx; rows.push(x.slice());
  }
  return rows;
}

/* ---------------------------------------------------------------- parameter scan (entries are polynomials in k) */
function combos(n, k){ var out = []; (function rec(s, acc){ if(acc.length === k){ out.push(acc.slice()); return; } for(var i = s; i < n; i++){ acc.push(i); rec(i + 1, acc); acc.pop(); } })(0, []); return out; }
function interpolate(xs, ys){   // Lagrange -> coefficient array (exact), degree < xs.length
  var n = xs.length, coef = new Array(n).fill(ZERO);
  for(var i = 0; i < n; i++){
    var num = [ONE], den = ONE;
    for(var j = 0; j < n; j++){ if(j === i) continue; var nn = new Array(num.length + 1).fill(ZERO); num.forEach(function(c, k){ nn[k + 1] = nn[k + 1].add(c); nn[k] = nn[k].sub(c.mul(xs[j])); }); num = nn; den = den.mul(xs[i].sub(xs[j])); }
    var f = ys[i].div(den); num.forEach(function(c, k){ coef[k] = coef[k].add(c.mul(f)); });
  }
  while(coef.length > 1 && coef[coef.length - 1].isZero()) coef.pop();
  return coef;
}
function scanParameter(evalAt, rows, cols, withRhs, degMax){
  // evalAt(kValue:Q) -> matrix (rows x cols [+1 if withRhs]); returns critical rational values and behaviour at each
  degMax = degMax || 4; var xs = []; for(var i = 0; i <= degMax + 2; i++) xs.push(new Q(i - 1));
  var mats = xs.map(evalAt), crit = [];
  function addRoots(poly){ if(poly.length <= 1) return; var rr = ratRoots(poly); rr.roots.forEach(function(o){ if(!crit.some(function(c){ return c.eq(o.r); })) crit.push(o.r); }); }
  var maxc = cols + (withRhs ? 1 : 0), base = mats[0];
  for(var size = 1; size <= Math.min(rows, maxc); size++){
    combos(rows, size).forEach(function(rs){ combos(maxc, size).forEach(function(cs){
      var ys = mats.map(function(M){ return det(rs.map(function(r){ return cs.map(function(c){ return M[r][c]; }); })); });
      addRoots(interpolate(xs, ys));
    }); });
  }
  crit.sort(function(a, b){ return a.cmp(b); });
  function behaviour(kv){ var M = evalAt(kv), A = M.map(function(r){ return r.slice(0, cols); }), rA = rank(A), rAb = withRhs ? rank(M) : rA; return withRhs ? (rA < rAb ? 'none' : rA === cols ? 'unique' : 'inf') : 'rank ' + rA; }
  var g = new Q(101); while(crit.some(function(c){ return c.eq(g); })) g = g.add(new Q(2));
  var gen = behaviour(g);
  return {critical: crit.filter(function(c){ return behaviour(c) !== gen; }), at: crit.map(function(c){ return {k: c, b: behaviour(c)}; }), generic: gen};
}

return {Q: Q, q: q, ZERO: ZERO, ONE: ONE, parseMatrix: parseMatrix, clone: clone, ident: ident, zeros: zeros, transpose: transpose, mul: mul, mmap: mmap, eqM: eqM, texMat: texMat, texVec: texVec,
  rowReduce: rowReduce, rank: rank, rref: rref, solve: solve, paramTex: paramTex, gaussBackSub: gaussBackSub, det: det, detSteps: detSteps, cofactor: cofactor, cofactorExpansion: cofactorExpansion,
  adjugate: adjugate, inverse: inverse, cramer: cramer, nullspace: nullspace, columnSpaceBasis: columnSpaceBasis, rowSpaceBasis: rowSpaceBasis, dot: dot, gramSchmidt: gramSchmidt, sqrtTex: sqrtTex,
  project: project, leastSquares: leastSquares, lu: lu, charpoly: charpoly, polyEval: polyEval, ratRoots: ratRoots, numericRoots: numericRoots, eigen: eigen, powerMat: powerMat,
  diagDominant: diagDominant, iterate: iterate, scanParameter: scanParameter, minorM: minorM};
});
