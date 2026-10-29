# -*- coding: utf-8 -*-
"""Shared helpers for the Calculus I question generators (sympy-verified)."""
import math, random, itertools
import sympy as sp
from qlib import tex, uniq_by_text, near_numbers, note

x, t, th, n_, k_ = sp.symbols("x t theta n k")

def E(e):
    """Inline math for a sympy expression / number."""
    return "$" + tex(e) + "$"

def num_equal(a, b, var=x, pts=None):
    """Numerical equality of two expressions at several safe sample points (fallback: symbolic)."""
    a, b = sp.sympify(a), sp.sympify(b)
    if a == b:
        return True
    fa = sp.lambdify(var, a, "mpmath") if a.has(var) else None
    ok = 0
    for p in (pts or [0.31, 0.77, 1.3, 1.9, 2.6, 3.4, -0.45, -1.2, -2.3]):
        try:
            va = complex(sp.N(a.subs(var, p), 20)); vb = complex(sp.N(b.subs(var, p), 20))
        except Exception:
            continue
        if any(math.isnan(z) or math.isinf(z) for z in (va.real, va.imag, vb.real, vb.imag)):
            continue
        ok += 1
        if abs(va - vb) > 1e-8 * max(1.0, abs(va)):
            return False
    if ok == 0:
        try:
            return sp.simplify(a - b) == 0
        except Exception:
            return False
    return True

def distinct_exprs(correct, wrongs, var=x):
    """Drop wrong expressions equal (numerically) to the correct one or to each other."""
    out = []
    for w in wrongs:
        w = sp.sympify(w)
        if num_equal(w, correct, var):
            continue
        if any(num_equal(w, o, var) for o in out):
            continue
        out.append(w)
    return out

def mc_expr(B, ch, topic, level, stem, correct, wrongs, explain, src, origin="src", var=x, wrap=E):
    """MCQ whose options are sympy expressions (verified pairwise different)."""
    ws = distinct_exprs(correct, wrongs, var)
    return B.mcq(ch, topic, level, stem, wrap(correct), [wrap(w) for w in ws], explain, src, origin)

def mc_val(B, ch, topic, level, stem, val, extras, explain, src, origin="src", fmt=E):
    """MCQ with an exact scalar answer; wrong options = extras first (typical mistakes), then generic near values."""
    val = sp.nsimplify(val) if not isinstance(val, sp.Basic) else val
    wr = []
    for e in extras:
        e = sp.nsimplify(e) if not isinstance(e, sp.Basic) else e
        try:
            if sp.simplify(e - val) == 0:
                continue
        except Exception:
            pass
        wr.append(fmt(e))
    if val.is_number and val.is_finite:
        for c in near_numbers(val, B.rng):
            wr.append("$" + c + "$" if fmt is E else c)
    return B.mcq(ch, topic, level, stem, fmt(val), uniq_by_text(wr), explain, src, origin)

def mc_text(B, ch, topic, level, stem, correct, wrongs, explain, src, origin="src"):
    return B.mcq(ch, topic, level, stem, correct, wrongs, explain, src, origin)

def interval_tex(s):
    return "$" + sp.latex(s) + "$"

def lim(expr, var, pt, dir=None):
    return sp.limit(expr, var, pt, dir) if dir else sp.limit(expr, var, pt)

def lim_text(v):
    """LaTeX for a limit value."""
    if v == sp.oo:
        return "$+\\infty$"
    if v == -sp.oo:
        return "$-\\infty$"
    return "$" + tex(v) + "$"

def lim_options(val, rng, extras=()):
    """Option strings for a limit value, including +/- infinity and 'does not exist' as plausible wrongs."""
    val = sp.sympify(val)
    wr = []
    for e in extras:
        wr.append(lim_text(sp.nsimplify(e)) if not isinstance(e, str) else e)
    base = [sp.oo, -sp.oo, 0, 1, -1]
    for b in base:
        if b != val:
            wr.append(lim_text(b))
    if val.is_number and val.is_finite:
        for c in near_numbers(val, rng):
            wr.append("$" + c + "$")
    wr.append("the limit does not exist")
    wr = [w for w in uniq_by_text(wr) if w != (lim_text(val))]
    return lim_text(val), wr

def order_wrongs(wrongs, correct_text, k=3, rng=None):
    wr = [w for w in uniq_by_text(wrongs) if w != correct_text]
    return wr
