/* Linear Algebra lab UI. Every tool runs several methods on the same input and cross-checks them (Gauss vs Gauss-Jordan vs Cramer vs inverse vs LU ...). */
(function(){
'use strict';
var U = window.USTM, LA = window.LA, root = document.getElementById('lab');
if(!root) return;
var Q = LA.q;
function T(s){ return '$' + s + '$'; }
function D(s){ return '$$' + s + '$$'; }
function matText(M){ return M.map(function(r){ return r.map(String).join(' '); }).join('\n'); }
function vec(text){ var M = LA.parseMatrix(text); if(M.length === 1) return M[0]; if(M.every(function(r){ return r.length === 1; })) return M.map(function(r){ return r[0]; }); throw new Error('enter a vector as one row or one column'); }
function stepsHtml(steps, ncoef, start){
  var h = '<div class="steps">'; if(start) h += '<div class="st"><span class="op">start</span>' + T(LA.texMat(start, ncoef)) + '</div>';
  steps.forEach(function(s){ h += '<div class="st"><span class="op">' + T(s.op) + '</span>' + T(LA.texMat(s.M, ncoef)) + '</div>'; });
  return h + '</div>';
}
function sec(title, body, open){ return '<details class="sol"' + (open ? ' open' : '') + '><summary>' + title + '</summary>' + body + '</details>'; }
function agree(label, ok){ return '<p>' + (ok ? '✅ ' : '⚠️ ') + label + '</p>'; }
function same(a, b){ return a.length === b.length && a.every(function(x, i){ return x.eq(b[i]); }); }

var TOOLS = [];
function tool(id, title, fields, run, example){ TOOLS.push({id: id, title: title, fields: fields, run: run, example: example}); }

/* ------------------------------------------------------------------ solve Ax = b */
tool('solve', 'Solve Ax = b', [['A', 'Coefficient matrix A (rows on separate lines)', 5], ['b', 'Right-hand side b (one row or one column)', 1], ['iters', 'Jacobi / Gauss–Seidel iterations', 0, '8']], function(f){
  var A = LA.parseMatrix(f.A), b = vec(f.b), n = A[0].length, h = '';
  if(b.length !== A.length) throw new Error('b must have ' + A.length + ' entries');
  var aug = A.map(function(r, i){ return r.concat([b[i]]); });
  var gj = LA.solve(A, b);
  h += '<p><b>Augmented matrix</b> ' + T(LA.texMat(aug, n)) + '</p>';
  h += sec('Method 1 — Gauss–Jordan elimination (reduced row echelon form)', stepsHtml(gj.R.steps, n, aug) + '<p>RREF: ' + T(LA.texMat(gj.R.M, n)) + '</p>' + (gj.kind === 'none' ? '<p>A row reads $0=c\\ne0$: the system is <b>inconsistent</b>.</p>' : gj.kind === 'unique' ? '<p>Unique solution ' + T(LA.texVec(gj.sol)) + '.</p>' : '<p>Infinitely many solutions (' + gj.free.length + ' free variable' + (gj.free.length > 1 ? 's' : '') + '): ' + T(LA.paramTex(gj)) + ', ' + T(['t', 's', 'u', 'v'].slice(0, gj.free.length).join(',') + '\\in\\mathbb{R}') + '.</p>'), true);
  if(gj.kind === 'unique'){
    var g = LA.gaussBackSub(A, b), ok = [];
    h += sec('Method 2 — Gaussian elimination, then back-substitution', stepsHtml(g.steps, n, aug) + '<p>Echelon form ' + T(LA.texMat(g.echelon, n)) + '. Back-substitute from the last row up: ' + T(g.lines.join(',\\ ')) + '.</p>');
    ok.push(same(g.x, gj.sol));
    if(A.length === n){
      var cr = LA.cramer(A, b);
      h += sec('Method 3 — Cramer\'s rule', '<p>' + T('\\det A=' + cr.det.tex()) + '; replacing column ' + 'j' + ' by $b$: ' + T(cr.dets.map(function(d, j){ return '\\det A_{' + (j + 1) + '}=' + d.tex(); }).join(',\\ ')) + '. So ' + T(cr.x.map(function(x, j){ return 'x_{' + (j + 1) + '}=\\frac{' + cr.dets[j].tex() + '}{' + cr.det.tex() + '}=' + x.tex(); }).join(',\\ ')) + '.</p>');
      ok.push(same(cr.x, gj.sol));
      var iv = LA.inverse(A);
      h += sec('Method 4 — Inverse matrix: x = A⁻¹ b', '<p>' + D('A^{-1}=' + LA.texMat(iv.inv)) + D('x=A^{-1}b=' + LA.texVec(LA.mul(iv.inv, b.map(function(x){ return [x]; })).map(function(r){ return r[0]; }))) + '</p>');
      ok.push(same(LA.mul(iv.inv, b.map(function(x){ return [x]; })).map(function(r){ return r[0]; }), gj.sol));
      var lu = LA.lu(A), Pb = LA.mul(lu.P, b.map(function(x){ return [x]; })).map(function(r){ return r[0]; }), y = [], x = new Array(n);
      for(var i = 0; i < n; i++){ var s = Pb[i]; for(var j = 0; j < i; j++) s = s.sub(lu.L[i][j].mul(y[j])); y.push(s); }
      for(i = n - 1; i >= 0; i--){ s = y[i]; for(j = i + 1; j < n; j++) s = s.sub(lu.U[i][j].mul(x[j])); x[i] = s.div(lu.U[i][i]); }
      h += sec('Method 5 — LU factorisation: PA = LU, solve Ly = Pb, then Ux = y', '<p>' + D('P=' + LA.texMat(lu.P) + ',\\ L=' + LA.texMat(lu.L) + ',\\ U=' + LA.texMat(lu.U)) + '<p>Forward substitution: ' + T('y=' + LA.texVec(y)) + '; back substitution: ' + T('x=' + LA.texVec(x)) + '.</p>');
      ok.push(same(x, gj.sol));
      if(LA.diagDominant(A)){
        var N = Math.max(1, Math.min(60, parseInt(f.iters || '8', 10))), zero = A.map(function(){ return 0; });
        var jac = LA.iterate(A, b, zero, N, 'jacobi'), gs = LA.iterate(A, b, zero, N, 'gs'), ex = gj.sol.map(function(v){ return v.toNumber(); });
        var tb = '<table class="t"><tr><th>k</th><th>Jacobi x⁽ᵏ⁾</th><th>Gauss–Seidel x⁽ᵏ⁾</th></tr>';
        for(i = 0; i <= N; i++) tb += '<tr><td>' + i + '</td><td>(' + jac[i].map(function(v){ return v.toFixed(5); }).join(', ') + ')</td><td>(' + gs[i].map(function(v){ return v.toFixed(5); }).join(', ') + ')</td></tr>';
        h += sec('Method 6 — Jacobi and Gauss–Seidel iterations (A is strictly diagonally dominant, so both converge)', '<p>Jacobi: ' + T('x_i^{(k+1)}=\\frac{1}{a_{ii}}\\Big(b_i-\\sum_{j\\ne i}a_{ij}x_j^{(k)}\\Big)') + '; Gauss–Seidel uses the already updated components. Exact solution ' + T(LA.texVec(gj.sol)) + ' ≈ (' + ex.map(function(v){ return v.toFixed(5); }).join(', ') + ').</p>' + tb + '</table>');
      } else h += '<p class="muted">Jacobi / Gauss–Seidel are shown only for strictly diagonally dominant matrices (|aᵢᵢ| > Σ|aᵢⱼ|), where convergence is guaranteed. This matrix is not.</p>';
    }
    h += agree('All the methods above give the same unique solution (' + ok.length + ' cross-checks).', ok.every(Boolean));
  } else if(gj.kind === 'inf' && A.length === n) h += '<p class="muted">Cramer\'s rule, the inverse and LU solving need a unique solution (invertible square A).</p>';
  var rA = LA.rank(A), rAb = LA.rank(aug);
  h += '<p>Rank check: ' + T('\\operatorname{rank}A=' + rA + ',\\ \\operatorname{rank}[A\\mid b]=' + rAb + ',\\ n=' + n) + ' ⇒ ' + (rA < rAb ? 'inconsistent' : rA === n ? 'unique solution' : 'infinitely many solutions') + '.</p>';
  return h;
}, {A: [[1, 2, 1, 1], [0, 1, 3, 0], [2, 5, 5, 3]], b: [4, -1, 8]});

/* ------------------------------------------------------------------ parameter scan */
tool('param', 'Systems with a parameter k', [['A', 'Matrix whose entries may contain the parameter k (e.g. k-5, 2k, k^2-14)', 5], ['b', 'Right-hand side (leave empty to study only the matrix: rank / invertibility)', 1]], function(f){
  var rowsTxt = String(f.A).trim().split(/\n|;/).map(function(r){ return r.trim(); }).filter(Boolean).map(function(r){ return r.replace(/[\[\]]/g, ' ').split(/[\s,]+/).filter(Boolean); });
  var rows = rowsTxt.length, cols = rowsTxt[0].length, bt = f.b && f.b.trim() ? f.b.replace(/[\[\]]/g, ' ').split(/[\s,;\n]+/).filter(Boolean) : null;
  if(bt && bt.length !== rows) throw new Error('b must have ' + rows + ' entries');
  if(!window.math) throw new Error('math.js did not load');
  function ev(e, kv){ var val = window.math.evaluate(e.replace(/(\d)k/g, '$1*k'), {k: kv.toNumber()}); return Q(Math.round(val * 1e6) / 1e6); }
  var evalAt = function(kv){ return rowsTxt.map(function(r, i){ return r.map(function(e){ return ev(e, kv); }).concat(bt ? [ev(bt[i], kv)] : []); }); };
  var res = LA.scanParameter(evalAt, rows, cols, !!bt, 4), h = '';
  var nm = {none: 'no solution (inconsistent)', unique: 'a unique solution', inf: 'infinitely many solutions'};
  if(bt){
    h += '<p>Compare ' + T('\\operatorname{rank}A') + ' and ' + T('\\operatorname{rank}[A\\mid b]') + ' (consistent iff equal; unique iff both equal ' + T('n=' + cols) + '). Critical values come from the vanishing of minors of ' + T('A') + ' and ' + T('[A\\mid b]') + '.</p><ul>';
    res.at.forEach(function(o){ if(o.b !== res.generic) h += '<li>' + T('k=' + o.k.tex()) + ': ' + nm[o.b] + '</li>'; });
    h += '<li>every other real ' + T('k') + ': ' + nm[res.generic] + '</li></ul>';
    var none = res.critical.filter(function(k){ return res.at.find(function(o){ return o.k.eq(k); }).b === 'none'; });
    h += '<p><b>Inconsistent for</b> ' + (res.generic === 'none' ? 'every real k except ' + (res.at.filter(function(o){ return o.b !== 'none'; }).map(function(o){ return T('k=' + o.k.tex()); }).join(', ') || 'none') : none.length ? none.map(function(k){ return T('k=' + k.tex()); }).join(', ') : 'no real k') + '.</p>';
  } else {
    h += '<p>The rank drops exactly at the roots of the minors: ' + (res.critical.length ? res.critical.map(function(k){ return T('k=' + k.tex()); }).join(', ') : 'no rational value') + '. For a square matrix this is where ' + T('\\det A(k)=0') + ' (not invertible).</p>';
    res.at.forEach(function(o){ h += '<p>' + T('k=' + o.k.tex()) + ': ' + o.b + '</p>'; }); h += '<p>Generic ' + T('k') + ': ' + res.generic + '.</p>';
  }
  h += '<p class="muted">Only rational critical values are found exactly (irrational roots such as k=±√5 are reported by the determinant tool: factor the polynomial it shows).</p>';
  return h;
}, {A: [[1, 2, 1, 1], [0, 1, 3, 0], [2, 5, 5, 'k']], b: [4, -1, 8]});

/* ------------------------------------------------------------------ determinant */
tool('det', 'Determinant', [['A', 'Square matrix A', 5]], function(f){
  var A = LA.parseMatrix(f.A), n = A.length; if(A[0].length !== n) throw new Error('the matrix must be square');
  var ds = LA.detSteps(A), h = '<p><b>Result: ' + T('\\det A=' + LA.det(A).tex()) + '</b></p>';
  h += sec('Method 1 — row reduction to triangular form (swaps flip the sign; adding multiples changes nothing)', stepsHtml(ds.steps, undefined, A) + (ds.zero ? '<p>A column has no pivot ⇒ ' + T('\\det A=0') + '.</p>' : '<p>' + T('\\det A=' + (ds.sign < 0 ? '-' : '') + ds.tri.map(function(r, i){ return '(' + r[i].tex() + ')'; }).join('\\cdot') + '=' + ds.det.tex()) + '.</p>'), true);
  if(n > 1){
    var best = 0, bz = -1; A.forEach(function(r, i){ var z = r.filter(function(x){ return x.isZero(); }).length; if(z > bz){ bz = z; best = i; } });
    var ce = LA.cofactorExpansion(A, best);
    h += sec('Method 2 — cofactor expansion along row ' + (best + 1) + ' (the row with most zeros)', '<p>' + D('\\det A=\\sum_j a_{' + (best + 1) + 'j}C_{' + (best + 1) + 'j}=' + ce.terms.map(function(t, j){ return t.a.isZero() ? '0' : '(' + t.a.tex() + ')(' + t.cof.tex() + ')'; }).join('+') + '=' + ce.total.tex()) + '</p>');
    var agreeOk = ce.total.eq(ds.det);
    if(n === 3){
      var a = A, sar = a[0][0].mul(a[1][1]).mul(a[2][2]).add(a[0][1].mul(a[1][2]).mul(a[2][0])).add(a[0][2].mul(a[1][0]).mul(a[2][1])).sub(a[0][2].mul(a[1][1]).mul(a[2][0])).sub(a[0][0].mul(a[1][2]).mul(a[2][1])).sub(a[0][1].mul(a[1][0]).mul(a[2][2]));
      h += sec('Method 3 — rule of Sarrus (3×3 only)', '<p>' + T('\\det A=a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}-a_{13}a_{22}a_{31}-a_{11}a_{23}a_{32}-a_{12}a_{21}a_{33}=' + sar.tex()) + '</p>');
      agreeOk = agreeOk && sar.eq(ds.det);
    }
    h += agree('The methods agree.', agreeOk);
    var d = ds.det;
    h += '<p>Consequences: ' + T('\\det A^T=' + d.tex()) + (d.isZero() ? ', ' + T('A') + ' is <b>singular</b> (no inverse; rows dependent)' : ', ' + T('\\det A^{-1}=' + ONEdiv(d)) + ', ' + T('A') + ' is invertible') + ', ' + T('\\det(2A)=2^{' + n + '}\\det A=' + Q(2).pow(n).mul(d).tex()) + ', ' + T('\\det(A^2)=' + d.mul(d).tex()) + '.</p>';
  }
  return h;
}, {A: [[2, 0, -1, 4], [-1, 2, 0, 3], [3, 0, 1, 2], [-2, 0, 3, 1]]});
function ONEdiv(d){ return LA.ONE.div(d).tex(); }

/* ------------------------------------------------------------------ inverse */
tool('inverse', 'Inverse matrix', [['A', 'Square matrix A', 5]], function(f){
  var A = LA.parseMatrix(f.A), n = A.length; if(A[0].length !== n) throw new Error('the matrix must be square');
  var d = LA.det(A), h = '<p>' + T('\\det A=' + d.tex()) + '</p>';
  var iv = LA.inverse(A);
  if(!iv) return h + '<p class="err">A is singular: the reduction of [A | I] produces a zero row, so there is no inverse.</p>';
  h += sec('Method 1 — Gauss–Jordan on [A | I]', stepsHtml(iv.steps, n, A.map(function(r, i){ return r.concat(LA.ident(n)[i]); })) + '<p>' + D('A^{-1}=' + LA.texMat(iv.inv)) + '</p>', true);
  var adj = LA.adjugate(A), ok = LA.eqM(LA.mmap(adj, function(x){ return x.div(d); }), iv.inv);
  h += sec('Method 2 — adjugate: A⁻¹ = adj(A) / det A', '<p>' + D('\\operatorname{adj}A=' + LA.texMat(adj) + ',\\quad A^{-1}=\\frac{1}{' + d.tex() + '}\\operatorname{adj}A') + '</p>');
  if(n === 2) h += sec('Method 3 — the 2×2 formula', '<p>' + D('\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}^{-1}=\\frac{1}{ad-bc}\\begin{bmatrix}d&-b\\\\-c&a\\end{bmatrix}') + '</p>');
  h += agree('Check A·A⁻¹ = I: ' + (LA.eqM(LA.mul(A, iv.inv), LA.ident(n))) + '; the two methods agree: ' + ok + '.', ok && LA.eqM(LA.mul(A, iv.inv), LA.ident(n)));
  return h;
}, {A: [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]});

/* ------------------------------------------------------------------ rank and subspaces */
tool('rank', 'Rank, null space, column and row space', [['A', 'Matrix A', 5]], function(f){
  var A = LA.parseMatrix(f.A), R = LA.rref(A), r = R.pivots.length, n = A[0].length;
  var ns = LA.nullspace(A), cs = LA.columnSpaceBasis(A), rs = LA.rowSpaceBasis(A);
  var h = sec('Row reduction', stepsHtml(R.steps, undefined, A) + '<p>RREF ' + T(LA.texMat(R.M)) + ', pivot columns ' + R.pivots.map(function(c){ return c + 1; }).join(', ') + '.</p>', true);
  h += '<p><b>' + T('\\operatorname{rank}A=' + r + ',\\ \\operatorname{nullity}A=' + (n - r) + ',\\ n=' + n) + '</b> — rank + nullity = n ✓.</p>';
  h += '<p>Basis of the null space ' + T('\\ker A') + ': ' + (ns.length ? ns.map(function(v){ return T(LA.texVec(v)); }).join(', ') : T('\\{0\\}')) + '</p>';
  h += '<p>Basis of the column space (the pivot columns of A): ' + cs.map(function(v){ return T(LA.texVec(v)); }).join(', ') + '</p>';
  h += '<p>Basis of the row space (non-zero rows of the RREF): ' + rs.map(function(v){ return T(LA.texVec(v)); }).join(', ') + '</p>';
  h += '<p>One-to-one (as a map ' + T('x\\mapsto Ax') + '): ' + (ns.length === 0 ? 'yes' : 'no') + ' · onto ' + T('\\mathbb{R}^{' + A.length + '}') + ': ' + (r === A.length ? 'yes' : 'no') + '.</p>';
  return h;
}, {A: [[1, 3, 2, 22, 13], [1, 0, 2, -2, 1], [3, 6, 5, 42, 27]]});

/* ------------------------------------------------------------------ eigen */
tool('eigen', 'Eigenvalues, eigenvectors, diagonalization', [['A', 'Square matrix A', 5], ['k', 'Power k for A^k (optional)', 0, '5']], function(f){
  var A = LA.parseMatrix(f.A), n = A.length; if(A[0].length !== n) throw new Error('the matrix must be square');
  var E = LA.eigen(A), cp = E.charpoly, h = '';
  function polyTex(c){ var t = []; for(var i = c.length - 1; i >= 0; i--){ if(c[i].isZero()) continue; var s = c[i].sign() > 0 ? (t.length ? '+' : '') : '-', a = c[i].abs(), co = (a.isOne() && i > 0) ? '' : a.tex(); t.push(s + co + (i > 1 ? '\\lambda^{' + i + '}' : i === 1 ? '\\lambda' : '')); } return t.join('') || '0'; }
  h += '<p>Characteristic polynomial ' + T('\\det(\\lambda I-A)=' + polyTex(cp)) + '; trace ' + T('=' + A.reduce(function(s, r, i){ return s.add(r[i]); }, LA.ZERO).tex()) + ' = sum of eigenvalues, determinant ' + T('=' + LA.det(A).tex()) + ' = product (up to sign ' + T('(-1)^n') + ' in the polynomial).</p>';
  E.values.forEach(function(v){ h += '<p>' + T('\\lambda=' + v.val.tex()) + ' (algebraic multiplicity ' + v.alg + '): eigenspace basis ' + (v.vectors.map(function(x){ return T(LA.texVec(x)); }).join(', ') || '—') + ' (geometric multiplicity ' + v.geo + ')</p>'; });
  if(E.rest.length > 1){ h += '<p>The remaining factor has no rational roots; numerically: ' + E.restRoots.map(function(z){ return T((+z.re.toFixed(6)) + (z.im ? (z.im > 0 ? '+' : '-') + Math.abs(+z.im.toFixed(6)) + 'i' : '')); }).join(', ') + '.</p>'; }
  if(E.diagonalizable){
    var P = E.P, Dm = E.D, Pi = LA.inverse(P).inv;
    h += '<p><b>Diagonalizable</b> (geometric = algebraic multiplicity for every eigenvalue): ' + D('P=' + LA.texMat(P) + ',\\quad D=' + LA.texMat(Dm) + ',\\quad P^{-1}AP=D') + '</p>';
    h += agree('Check P⁻¹AP = D: ' + LA.eqM(LA.mul(LA.mul(Pi, A), P), Dm), LA.eqM(LA.mul(LA.mul(Pi, A), P), Dm));
    var kk = parseInt(f.k || '0', 10); if(kk > 0){ var Dk = LA.zeros(n, n); for(var i = 0; i < n; i++) Dk[i][i] = Dm[i][i].pow(kk); var Ak = LA.mul(LA.mul(P, Dk), Pi); h += '<p>' + D('A^{' + kk + '}=PD^{' + kk + '}P^{-1}=' + LA.texMat(Ak)) + '</p>' + agree('Matches repeated multiplication: ' + LA.eqM(Ak, LA.powerMat(A, kk)), LA.eqM(Ak, LA.powerMat(A, kk))); }
    var sym = LA.eqM(A, LA.transpose(A));
    if(sym){
      var cols = [], parts = [];
      E.values.forEach(function(v){ var g = LA.gramSchmidt(v.vectors); g.u.forEach(function(u, i){ parts.push('\\lambda=' + v.val.tex() + ':\\ \\frac{1}{' + LA.sqrtTex(g.norm2[i]) + '}' + LA.texVec(u)); }); });
      h += '<p>A is symmetric ⇒ <b>orthogonally diagonalizable</b>: normalise an orthogonal basis of each eigenspace (Gram–Schmidt inside eigenspaces; different eigenspaces are already orthogonal): ' + T(parts.join(';\\quad ')) + '. Then ' + T('P^{T}AP=D') + ' with these unit vectors as columns of ' + T('P') + '.</p>';
    }
  } else if(E.rest.length === 1){ h += '<p><b>Not diagonalizable over ℝ</b>: some eigenvalue has geometric multiplicity smaller than its algebraic multiplicity (too few independent eigenvectors).</p>'; }
  else h += '<p><b>Not diagonalizable over ℚ</b> with the exact method here (irrational or complex eigenvalues); use the numeric roots above.</p>';
  return h;
}, {A: [[-1, 4, -2], [-3, 4, 0], [-3, 1, 3]]});

/* ------------------------------------------------------------------ orthogonal tools */
tool('ortho', 'Gram–Schmidt, projections, orthogonal complement, least squares', [['V', 'Vectors u₁, u₂, … (one per line)', 4], ['u', 'Vector u to project (optional)', 1], ['pts', 'Data points for the least-squares line, e.g. -2 2; -1 1; 0 1; 1 3 (optional)', 1]], function(f){
  var V = LA.parseMatrix(f.V), n = V[0].length, h = '';
  var g = LA.gramSchmidt(V);
  h += sec('Gram–Schmidt on the vectors in the given order', '<p>' + T('u_k=v_k-\\sum_{j<k}\\frac{\\langle v_k,u_j\\rangle}{\\langle u_j,u_j\\rangle}u_j') + '</p><p>' + g.u.map(function(u, i){ return T('u_{' + (i + 1) + '}=' + LA.texVec(u) + ',\\ \\|u_{' + (i + 1) + '}\\|^2=' + g.norm2[i].tex()); }).join('<br>') + '</p><p>Orthonormal basis: ' + g.u.map(function(u, i){ return T('e_{' + (i + 1) + '}=\\frac{1}{' + LA.sqrtTex(g.norm2[i]) + '}' + LA.texVec(u)); }).join(', ') + '</p>', true);
  var comp = LA.nullspace(V), gc = comp.length ? LA.gramSchmidt(comp) : null;
  h += sec('Orthogonal complement of the span (null space of the matrix whose rows are the vectors)', '<p>Basis of ' + T('U^{\\perp}') + ' (dimension ' + comp.length + '): ' + (comp.map(function(v){ return T(LA.texVec(v)); }).join(', ') || T('\\{0\\}')) + '</p>' + (gc ? '<p>Orthonormalised: ' + gc.u.map(function(u, i){ return T('\\frac{1}{' + LA.sqrtTex(gc.norm2[i]) + '}' + LA.texVec(u)); }).join(', ') + '</p>' : ''));
  if(f.u && f.u.trim()){
    var u = vec(f.u), pU = LA.project(u, g.u, g.norm2), res = u.map(function(x, i){ return x.sub(pU[i]); });
    h += sec('Projection of u onto U = span of the vectors', '<p>' + D('\\operatorname{proj}_Uu=\\sum_k\\frac{\\langle u,u_k\\rangle}{\\langle u_k,u_k\\rangle}u_k=' + LA.texVec(pU) + ',\\qquad u-\\operatorname{proj}_Uu=\\operatorname{proj}_{U^\\perp}u=' + LA.texVec(res)) + '</p><p>Check: ' + T('u-\\operatorname{proj}_Uu') + ' is orthogonal to every vector: ' + V.every(function(v){ return LA.dot(res, v).isZero(); }) + '. Distance from ' + T('u') + ' to ' + T('U') + ': ' + T('\\sqrt{' + LA.dot(res, res).tex() + '}=' + LA.sqrtTex(LA.dot(res, res))) + '.</p>');
  }
  if(f.pts && f.pts.trim()){
    var P = LA.parseMatrix(f.pts), xs = P.map(function(r){ return r[0]; }), ys = P.map(function(r){ return r[1]; }), ls = LA.leastSquares(xs, ys, 1);
    h += sec('Least-squares line y = a + bx', '<p>Normal equations ' + T('X^{T}Xc=X^{T}y') + ': ' + D(LA.texMat(ls.normal) + 'c=' + LA.texVec(ls.rhs).replace(/^\(/, '\\begin{bmatrix}').replace(/\)$/, '\\end{bmatrix}').replace(/,\\ /g, '\\\\') + '\\ \\Rightarrow\\ (a,b)=' + LA.texVec(ls.coef) + ',\\quad y=' + ls.coef[0].tex() + (ls.coef[1].sign() >= 0 ? '+' : '') + ls.coef[1].tex() + 'x') + '</p>');
  }
  return h;
}, {V: [[1, -1, 1, 0], [-2, 2, -2, 1]], u: [1, 2, 1, 1], pts: '-2 2; -1 1; 0 1; 1 3'});

/* ------------------------------------------------------------------ linear maps in bases */
tool('bases', 'Matrix of a linear map relative to bases; coordinates; transition matrix', [['A', 'Standard matrix A of T (columns = T(e_j))', 4], ['B', 'Basis B of the domain (one basis vector per line)', 4], ['Bp', 'Basis B′ of the codomain (one vector per line; leave empty to use B)', 4], ['x', 'Vector x (optional)', 1]], function(f){
  var A = LA.parseMatrix(f.A), B = LA.transpose(LA.parseMatrix(f.B)), Bp = f.Bp && f.Bp.trim() ? LA.transpose(LA.parseMatrix(f.Bp)) : B, h = '';
  var Pi = LA.inverse(Bp); if(!Pi) throw new Error("B′ is not a basis (singular)"); if(B.length !== A[0].length) throw new Error('B must consist of vectors in the domain of T');
  var rel = LA.mul(LA.mul(Pi.inv, A), B);
  h += '<p>With ' + T('P_B') + ', ' + T('P_{B\'}') + ' having the basis vectors as columns: ' + D('[T]_{B,B\'}=P_{B\'}^{-1}\\,A\\,P_B') + D('P_B=' + LA.texMat(B) + ',\\ P_{B\'}=' + LA.texMat(Bp) + ',\\ P_{B\'}^{-1}=' + LA.texMat(Pi.inv)) + D('[T]_{B,B\'}=' + LA.texMat(rel)) + '</p>';
  if(B.length === Bp.length){ var tr = LA.mul(Pi.inv, B); h += '<p>Transition matrix from ' + T('B') + ' to ' + T('B\'') + ' (columns = coordinates of the ' + T('B') + '-vectors in ' + T('B\'') + '): ' + D('P_{B\\to B\'}=P_{B\'}^{-1}P_B=' + LA.texMat(tr)) + '</p>'; }
  if(f.x && f.x.trim()){ var x = vec(f.x).map(function(v){ return [v]; }), xB = LA.solve(B, x.map(function(r){ return r[0]; })); if(xB.kind === 'unique') h += '<p>' + T('[x]_B=' + LA.texVec(xB.sol)) + '; ' + T('T(x)=Ax=' + LA.texVec(LA.mul(A, x).map(function(r){ return r[0]; }))) + '; ' + T('[T(x)]_{B\'}=[T]_{B,B\'}[x]_B=' + LA.texVec(LA.mul(rel, xB.sol.map(function(v){ return [v]; })).map(function(r){ return r[0]; }))) + '.</p>'; }
  return h;
}, {A: [[1, -2, 1], [2, -3, 5], [3, -2, 1]], B: [[1, 2, 0], [1, 0, -1], [-2, 1, 2]], Bp: '', x: [1, 0, 0]});

/* ------------------------------------------------------------------ Jacobian (extension) */
tool('jacobian', 'Jacobian matrix (extension: Calculus II)', [['F', 'Component functions of x, y, z (one per line), e.g.  x^2*y   and   x + y^3', 3], ['vars', 'Variables', 0, 'x, y'], ['pt', 'Point (comma separated)', 0, '1, 2']], function(f){
  if(!window.math) throw new Error('math.js did not load');
  var math = window.math, fs = f.F.split(/\n|;/).map(function(s){ return s.trim(); }).filter(Boolean), vars = f.vars.split(',').map(function(s){ return s.trim(); }).filter(Boolean), pt = f.pt.split(',').map(function(s){ return parseFloat(s); });
  if(vars.length !== pt.length) throw new Error('the point needs one coordinate per variable');
  var J = fs.map(function(e){ return vars.map(function(v){ return math.simplify(math.derivative(e, v)); }); });
  var scope = {}; vars.forEach(function(v, i){ scope[v] = pt[i]; });
  var num = J.map(function(r){ return r.map(function(d){ return d.evaluate(scope); }); });
  var h = '<p>' + D('J=\\begin{bmatrix}' + J.map(function(r){ return r.map(function(d){ return d.toTex(); }).join(' & '); }).join(' \\\\ ') + '\\end{bmatrix}') + '</p>';
  h += '<p>At the point ' + T('(' + pt.join(',') + ')') + ': ' + D('J=\\begin{bmatrix}' + num.map(function(r){ return r.map(function(v){ return +v.toFixed(6); }).join(' & '); }).join(' \\\\ ') + '\\end{bmatrix}') + '</p>';
  if(num.length === num[0].length){ var dd = math.det(num); h += '<p>' + T('\\det J=' + (+dd.toFixed(6))) + ' — the local area/volume scaling factor of the map (used in change of variables, e.g. polar coordinates give ' + T('\\det J=r') + ').</p>'; }
  h += '<p class="muted">The Jacobian matrix is the matrix of the best linear approximation ' + T('F(p+h)\\approx F(p)+J(p)h') + ': it connects this course (linear transformations) with multivariable calculus.</p>';
  return h;
}, {F: 'x^2*y\nx + y^3', vars: 'x, y', pt: '1, 2'});

/* ------------------------------------------------------------------ UI */
function build(){
  root.innerHTML = '';
  var tabs = U.el('div', 'tabs'); root.appendChild(tabs);
  var box = U.el('div', 'panel'); root.appendChild(box);
  function open(id, preset){
    var t = TOOLS.filter(function(x){ return x.id === id; })[0] || TOOLS[0];
    U.$$('button', tabs).forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-id') === t.id); });
    box.innerHTML = ''; box.appendChild(U.el('h3', null, t.title));
    var inputs = {};
    t.fields.forEach(function(fd){
      var lab = U.el('label', null, fd[1]); lab.style.display = 'block'; lab.style.marginTop = '6px';
      var el = fd[2] === 0 ? U.el('input') : U.el('textarea'); if(fd[2] === 0){ el.type = 'text'; el.value = fd[3] || ''; } else { el.rows = fd[2]; }
      var src = (preset && preset[fd[0]] !== undefined) ? preset[fd[0]] : (t.example || {})[fd[0]];
      if(src !== undefined && fd[2] !== 0) el.value = Array.isArray(src) ? (Array.isArray(src[0]) ? matText(src) : src.join(' ')) : String(src);
      if(src !== undefined && fd[2] === 0 && src !== '') el.value = Array.isArray(src) ? src.join(', ') : String(src);
      inputs[fd[0]] = el; box.appendChild(lab); box.appendChild(el);
    });
    var go = U.el('button', 'btn', '▶ Compute'), ex = U.el('button', 'btn alt', 'Reset to the example'), out = U.el('div', 'out');
    box.appendChild(go); box.appendChild(ex); box.appendChild(out);
    function run(){
      var vals = {}; Object.keys(inputs).forEach(function(k){ vals[k] = inputs[k].value; });
      try{ out.innerHTML = t.run(vals); }catch(e){ out.innerHTML = '<p class="err">⚠ ' + String(e.message || e).replace(/</g, '&lt;') + '</p>'; }
      U.math(out);
    }
    go.onclick = run; ex.onclick = function(){ open(id); }; run();
    try{ history.replaceState(null, '', '#tool=' + t.id); }catch(e){}
  }
  TOOLS.forEach(function(t){ var b = U.el('button', null, t.title.split(':')[0].split(' (')[0]); b.setAttribute('data-id', t.id); b.onclick = function(){ open(t.id); }; tabs.appendChild(b); });
  var h = location.hash.slice(1), p = {}, id = 'solve';
  h.split('&').forEach(function(kv){ var i = kv.indexOf('='); if(i > 0){ var k = kv.slice(0, i), v = decodeURIComponent(kv.slice(i + 1)); if(k === 'tool') id = v; else { try{ p[k] = JSON.parse(v); }catch(e){ p[k] = v; } } } });
  open(id, Object.keys(p).length ? p : undefined);
}
build();
})();
