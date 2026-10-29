# -*- coding: utf-8 -*-
"""Shared helpers for the Linear Algebra generators (sympy-verified)."""
import itertools, random
import sympy as sp
from qlib import tex, M, mat, aug, vec, colvec, system_tex, uniq_by_text, near_numbers

k, m, a, t, s_, u_ = sp.symbols("k m a t s u")
X = sp.symbols("x1:9")

def Mx(rows):
    return sp.Matrix(rows)

def perturb(A, rng, how="entry"):
    """Return a copy of A with one entry changed by +-1 (a realistic arithmetic slip)."""
    B = sp.Matrix(A)
    for _ in range(20):
        i, j = rng.randrange(B.rows), rng.randrange(B.cols)
        d = rng.choice([-2, -1, 1, 2])
        C = B.copy(); C[i, j] = C[i, j] + d
        if C != A:
            return C
    return B

def solve_sys(A, b):
    """-> (kind, solution tuple or None, free symbols list). kind in 'unique' | 'none' | 'inf'."""
    A = sp.Matrix(A); b = sp.Matrix(b)
    n = A.cols
    xs = sp.symbols("x1:%d" % (n + 1))
    rA, rAb = A.rank(), A.row_join(b).rank()
    if rA < rAb:
        return "none", None, []
    sol = list(sp.linsolve((A, b), *xs))[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]), key=str) if sol else []
    kind = "unique" if rA == n else "inf"
    return kind, sol, free

def rename_free(sol, free):
    names = [t, s_, u_]
    sub = {f: names[i] for i, f in enumerate(free)}
    return [sp.simplify(e.subs(sub)) for e in sol], [names[i] for i in range(len(free))]

def sol_tex(sol, free):
    sol2, fr = rename_free(sol, free)
    body = vec(sol2)
    if fr:
        body += ",\\ " + ",".join(tex(f) for f in fr) + r"\in\mathbb{R}"
    return "$" + body + "$"

def particular(sol, free, rng):
    """Pick a concrete particular solution of a parametric solution."""
    vals = {f: rng.choice([-1, 0, 1, 2]) for f in free}
    return [sp.nsimplify(e.subs(vals)) for e in sol]

def satisfies(A, b, v):
    return sp.Matrix(A) * sp.Matrix(list(v)) == sp.Matrix(b)

def near_vectors(v, A, b, rng, n=6):
    """Vectors close to a true solution that FAIL the system (typical arithmetic slips)."""
    outs = []
    tries = 0
    while len(outs) < n and tries < 200:
        tries += 1
        w = list(v)
        i = rng.randrange(len(w))
        w[i] = w[i] + rng.choice([-2, -1, 1, 2])
        if rng.random() < 0.3:
            j = rng.randrange(len(w)); w[j] = -w[j]
        if not satisfies(A, b, w) and w not in outs:
            outs.append(w)
    return outs

def crit_values(A, b, sym):
    """Candidate critical parameter values: real roots of all minors of A and [A|b]."""
    A = sp.Matrix(A); b = sp.Matrix(b)
    Ab = A.row_join(b)
    cands = set()
    for Mt in (A, Ab):
        for size in range(1, min(Mt.shape) + 1):
            for rows in itertools.combinations(range(Mt.rows), size):
                for cols in itertools.combinations(range(Mt.cols), size):
                    d = sp.expand(Mt.extract(list(rows), list(cols)).det())
                    if d != 0 and d.has(sym):
                        for r in sp.solve(d, sym):
                            if r.is_real:
                                cands.add(sp.nsimplify(r))
    return sorted(cands, key=lambda z: float(z))

def classify_param(A, b, sym):
    """-> dict value->category plus 'generic'. Categories: unique | none | inf."""
    A = sp.Matrix(A); b = sp.Matrix(b)
    n = A.cols
    cands = crit_values(A, b, sym)
    def cat(v):
        Av = A.subs(sym, v); bv = b.subs(sym, v)
        rA, rAb = Av.rank(), Av.row_join(bv).rank()
        if rA < rAb: return "none"
        return "unique" if rA == n else "inf"
    out = {c: cat(c) for c in cands}
    g = 101
    while g in cands:
        g += 2
    out["generic"] = cat(g)
    return out

def value_set_text(vals, sym):
    """Text for a set of parameter values: '$k=2$', '$k\\in\\{-1,3\\}$', 'no value of $k$', 'every real $k$'."""
    st = tex(sym)
    vals = sorted(set(vals), key=lambda z: float(z))
    if not vals:
        return "no value of $%s$" % st
    if len(vals) == 1:
        return "$%s=%s$" % (st, tex(vals[0]))
    if len(vals) == 2 and vals[0] == -vals[1]:
        return "$%s=\\pm %s$" % (st, tex(vals[1]))
    return "$%s\\in\\{%s\\}$" % (st, ",".join(tex(v) for v in vals))

def set_options(correct, cands, sym, rng):
    """Correct value set + 3 distinct plausible wrong sets built from the critical values."""
    cands = list(cands)
    pool = []
    for r in range(0, min(3, len(cands)) + 1):
        for comb in itertools.combinations(cands, r):
            pool.append(tuple(comb))
    for c in cands:
        if c != 0:
            pool.append((-c,))
    ct = value_set_text(correct, sym)
    texts = uniq_by_text([value_set_text(p, sym) for p in pool])
    texts = [x for x in texts if x != ct]
    rng.shuffle(texts)
    extra = ["every real $%s$" % tex(sym)]
    texts = texts + [e for e in extra if e != ct]
    return ct, texts[:3] if len(texts) >= 3 else texts
