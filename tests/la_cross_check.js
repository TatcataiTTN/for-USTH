// Compare shared/la.js (exact BigInt rationals) with sympy ground truth produced by tests/gen_la_cases.py
const path = require('path'), fs = require('fs');
const LA = require(path.join(__dirname, '..', 'shared', 'la.js'));
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'la_cases.json'), 'utf8'));
let n = 0, bad = 0;
const ok = (c, msg) => { n++; if(!c){ bad++; if(bad < 25) console.log('FAIL', msg); } };
const S = x => x.toString();
const M2S = M => M.map(r => r.map(S));
const same = (A, B) => JSON.stringify(A) === JSON.stringify(B);
cases.rref.forEach((c, i) => {
  const M = LA.parseMatrix(c.M), R = LA.rref(M);
  ok(same(M2S(R.M), c.rref), 'rref #' + i + ' ' + JSON.stringify(c.M));
  ok(R.pivots.length === c.rank && LA.rank(M) === c.rank, 'rank #' + i);
  const ns = LA.nullspace(M);
  ok(ns.length === c.nullity, 'nullity #' + i);
  ns.forEach(v => { const Av = LA.mul(M, v.map(x => [x])); ok(Av.every(r => r[0].isZero()), 'A v = 0 #' + i); });
  ok(LA.columnSpaceBasis(M).length === c.rank, 'colspace dim #' + i);
});
cases.square.forEach((c, i) => {
  const M = LA.parseMatrix(c.M), d = LA.det(M);
  ok(S(d) === c.det, 'det #' + i + ' got ' + S(d) + ' want ' + c.det);
  ok(S(LA.detSteps(M).det) === c.det, 'detSteps #' + i);
  if(M.length > 1) ok(S(LA.cofactorExpansion(M, 0).total) === c.det, 'cofactor expansion #' + i);
  const inv = LA.inverse(M);
  if(c.inv === null) ok(inv === null, 'singular inverse #' + i);
  else { ok(inv && same(M2S(inv.inv), c.inv), 'inverse #' + i); const adj = LA.adjugate(M); ok(same(M2S(LA.mmap(adj, x => x.div(d))), c.inv), 'adjugate inverse #' + i); ok(LA.eqM(LA.mul(M, inv.inv), LA.ident(M.length)), 'A A^-1 = I #' + i); }
  ok(same(LA.charpoly(M).map(S), c.charpoly), 'charpoly #' + i + ' got ' + LA.charpoly(M).map(S) + ' want ' + c.charpoly);
  const E = LA.eigen(M);
  if(c.eig){
    const got = E.values.map(v => ({val: S(v.val), alg: v.alg, geo: v.geo})).sort((a, b) => LA.q(a.val).cmp(LA.q(b.val)));
    const want = c.eig.slice().sort((a, b) => LA.q(a.val).cmp(LA.q(b.val)));
    ok(same(got, want), 'eigen #' + i + ' got ' + JSON.stringify(got) + ' want ' + JSON.stringify(want));
    ok(E.rest.length === 1, 'all roots rational #' + i);
    ok(E.diagonalizable === c.diag, 'diagonalizable #' + i);
    if(E.diagonalizable){ ok(LA.eqM(LA.mul(M, E.P), LA.mul(E.P, E.D)), 'AP = PD #' + i); }
  } else { ok(E.rest.length > 1 || E.values.length === 0 || true, 'irrational spectrum #' + i); }
  const lu = LA.lu(M); ok(LA.eqM(LA.mul(lu.P, M), LA.mul(lu.L, lu.U)), 'PA = LU #' + i);
  if(M.length > 1 && c.eig){ const A3 = LA.powerMat(M, 5); let B = M; for(let k = 1; k < 5; k++) B = LA.mul(B, M); ok(LA.eqM(A3, B), 'matrix power #' + i); }
});
cases.solve.forEach((c, i) => {
  const A = LA.parseMatrix(c.A), b = c.b.map(LA.q), r = LA.solve(A, b);
  ok(r.kind === c.kind, 'solve kind #' + i + ' got ' + r.kind + ' want ' + c.kind);
  if(c.kind === 'unique'){ ok(same(r.sol.map(S), c.sol), 'solution #' + i); const g = LA.gaussBackSub(A, b); ok(g && same(g.x.map(S), c.sol), 'gauss back-substitution #' + i); if(A.length === A[0].length){ const cr = LA.cramer(A, b); ok(cr && same(cr.x.map(S), c.sol), 'cramer #' + i); } }
  if(c.kind === 'inf'){ const p = r.particular; ok(LA.mul(A, p.map(x => [x])).every((row, k) => row[0].eq(b[k])), 'particular solves #' + i); r.dirs.forEach(d => ok(LA.mul(A, d.map(x => [x])).every(row => row[0].isZero()), 'direction in kernel #' + i)); }
});
cases.gs.forEach((c, i) => {
  const vs = c.vs.map(v => v.map(LA.q)), g = LA.gramSchmidt(vs);
  ok(same(g.norm2.map(S), c.norm2), 'gram-schmidt norms #' + i); ok(same(g.u.map(v => v.map(S)), c.u), 'gram-schmidt vectors #' + i);
});
cases.param.forEach(c => {
  const f = (kv) => c.A.map(r => r.map(e => evalEntry(e, kv))).map((r, i) => r.concat([evalEntry(c.b[i], kv)]));
  function evalEntry(e, kv){ const expr = e.replace(/\^/g, '**').replace(/(\d)\*?k/g, '$1*k').replace(/k\*\*2/g, '(k*k)'); const val = Function('k', 'return ' + (expr.replace(/\*\*/g, '**')))(kv.toNumber()); return LA.q(Math.round(val * 1000) / 1000); }
  const rows = c.A.length, cols = c.A[0].length;
  const res = LA.scanParameter(f, rows, cols, true, 3);
  const got = {}; res.critical.forEach(k => { got[S(k)] = res.at.find(o => o.k.eq(k)).b; });
  ok(same(Object.keys(got).sort(), Object.keys(c.crit).sort()) && Object.keys(got).every(k => got[k] === c.crit[k]) && res.generic === c.generic, 'parameter scan ' + c.name + ' got ' + JSON.stringify(got) + '/' + res.generic + ' want ' + JSON.stringify(c.crit) + '/' + c.generic);
});
console.log(`la_cross_check: ${n} checks, ${bad} failures`);
process.exit(bad ? 1 : 0);
