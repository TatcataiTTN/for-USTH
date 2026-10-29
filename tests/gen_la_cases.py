"""Generate random linear-algebra test cases with sympy (ground truth) for tests/la_cross_check.js."""
import json, random, sys, os
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "build"))
from la_common import classify_param, k, m, a

rng = random.Random(2026)
S = lambda x: "%d/%d" % (sp.Rational(x).p, sp.Rational(x).q) if sp.Rational(x).q != 1 else str(sp.Rational(x).p)
SM = lambda M: [[S(M[i, j]) for j in range(M.cols)] for i in range(M.rows)]
cases = {"rref": [], "square": [], "solve": [], "gs": [], "param": []}
def rnd(r, c, lo=-4, hi=4, dep=0.3):
    M = sp.Matrix(r, c, lambda i, j: rng.randint(lo, hi))
    if r > 1 and rng.random() < dep:
        M[r - 1, :] = M[0, :] * rng.choice([1, 2, -1]) + (M[1, :] if r > 2 else sp.zeros(1, c))
    return M
for _ in range(220):
    M = rnd(rng.randint(1, 4), rng.randint(1, 5))
    R, piv = M.rref()
    cases["rref"].append(dict(M=SM(M), rref=SM(R), pivots=list(piv), rank=M.rank(), nullity=M.cols - M.rank()))
for _ in range(220):
    n = rng.randint(1, 4)
    M = rnd(n, n, -3, 3, 0.25)
    cp = M.charpoly().all_coeffs()[::-1]
    ev = M.eigenvals()
    rational = all(e.is_Rational for e in ev)
    ev_info = None
    if rational:
        ev_info = []
        for val, mult, basis in M.eigenvects():
            ev_info.append(dict(val=S(val), alg=mult, geo=len(basis)))
    inv = None
    if M.det() != 0:
        inv = SM(M.inv())
    cases["square"].append(dict(M=SM(M), det=S(M.det()), inv=inv, charpoly=[S(c) for c in cp], eig=ev_info, diag=(M.is_diagonalizable() if rational else None)))
for _ in range(200):
    r, c = rng.choice([(3, 3), (3, 4), (4, 3), (2, 3), (3, 2), (4, 4)])
    A = rnd(r, c); b = sp.Matrix(r, 1, lambda i, j: rng.randint(-5, 5))
    if rng.random() < 0.5:
        x0 = sp.Matrix(c, 1, lambda i, j: rng.randint(-3, 3)); b = A * x0
    rA, rAb = A.rank(), A.row_join(b).rank()
    kind = "none" if rA < rAb else ("unique" if rA == c else "inf")
    sol = None
    if kind == "unique":
        sol = [S(v) for v in A.LUsolve(b)]
    cases["solve"].append(dict(A=SM(A), b=[S(v) for v in b], kind=kind, sol=sol, rank=rA, rankAb=rAb))
for _ in range(80):
    n = rng.randint(2, 4)
    while True:
        V = sp.Matrix(n, n, lambda i, j: rng.randint(-3, 3))
        if V.det() != 0: break
    cols = [V[:, j] for j in range(n)]
    us = []; ns = []
    for v in cols:
        w = v
        for u, nn in zip(us, ns): w = w - (v.dot(u) / nn) * u
        us.append(w); ns.append(w.dot(w))
    cases["gs"].append(dict(vs=[[S(x) for x in c_] for c_ in cols], norm2=[S(x) for x in ns], u=[[S(x) for x in w] for w in us]))
# parametric systems from the past papers (scanParameter must find the same critical values and behaviours)
PAR = [("2024-25-S1 Q1", sp.Matrix([[1, 2, 1, 1], [0, 1, 3, 0], [2, 5, 5, k]]), sp.Matrix([4, -1, 8]), k),
       ("2024-25-S2 Q1", sp.Matrix([[1, 0, 2, -2], [0, 2, 1, -1], [2, 0, 4, k - 5]]), sp.Matrix([1, -1, 4]), k),
       ("2023-24-S2 Q1", sp.Matrix([[1, 1, 1], [1, 2, 3], [2, k, 1]]), sp.Matrix([0, 4, 3]), k),
       ("2023-24-S1 Q1", sp.Matrix([[1, 0, -3], [3, 1, -2], [k, k, 1]]), sp.Matrix([-2, 5, 4]), k),
       ("2022-23 Q1", sp.Matrix([[1, -2, 1], [0, 2, -8], [-4, 5, k]]), sp.Matrix([0, 8, -k]), k),
       ("2019-20 Q1", sp.Matrix([[1, 1, 1], [1, 2, 4], [2, -3, -k]]), sp.Matrix([4, 12, k + 3]), k),
       ("2018-19 DEG Q1", sp.Matrix([[1, -k, 3], [2, 4, -4], [1, -2, 2]]), sp.Matrix([5, 0, 4]), k),
       ("2018-19 ABC Q1", sp.Matrix([[5, 2, 5, 1], [1, 2, 1, -3], [3, 6, k + 2, -9]]), sp.Matrix([9, -3, 6]), k),
       ("Sheet1 Ex4", sp.Matrix([[1, 2, -3], [3, -1, 5], [4, 1, k ** 2 - 14]]), sp.Matrix([4, 2, k + 2]), k),
       ("Sheet1 Ex6", sp.Matrix([[1, k, 1], [2, k - 1, 3], [k, 1, 3]]), sp.Matrix([k, 1, 2 * k - 3]), k)]
for name, A, b, sym in PAR:
    cls = classify_param(A, b, sym)
    gen = cls["generic"]
    crit = {}
    for c, v in cls.items():
        if c == "generic" or v == gen: continue
        if sp.sympify(c).is_Rational: crit[S(c)] = v
    cases["param"].append(dict(name=name, A=[[str(A[i, j]) for j in range(A.cols)] for i in range(A.rows)], b=[str(x) for x in b], crit=crit, generic=gen))
json.dump(cases, open(os.path.join(os.path.dirname(__file__), "la_cases.json"), "w"))
print({kk: len(v) for kk, v in cases.items()})
