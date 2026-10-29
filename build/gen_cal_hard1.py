# -*- coding: utf-8 -*-
"""Calculus I, level-4 pool in the style of the Moodle mock midterm (MAT1.001): slots 1-11, 14, 15, 17, 18.
Each slot of the 20-question Moodle mock gets several fresh variants (new numbers or functions, same trap); every answer is computed with sympy
and re-derived by a second route (high-precision numerics, Hermite interpolation of a table, or exhaustive checks).  Slot numbers are stored in tags ("moodle-sNN")."""
import sympy as sp
from qlib import tex
from cal_common import E, lim_text, uniq_by_text

xr = sp.Symbol("x", real=True)
SRC = "Moodle-style mock midterm, question %d (our variant, new numbers)"
sin, cos, tan, exp, log, sqrt, pi, R = sp.sin, sp.cos, sp.tan, sp.exp, sp.log, sp.sqrt, sp.pi, sp.Rational

def add(B, ch, slot, level, topic, stem, correct, wrongs, explain, tags=()):
    return B.mcq(ch, topic, level, stem, correct, wrongs, explain, SRC % slot, origin="hard", tags=["moodle-s%02d" % slot] + list(tags))

def agree(a, b, what, tol=1e-5):
    fa, fb = float(sp.N(a, 30)), float(sp.N(b, 30))
    assert abs(fa - fb) <= tol * max(1.0, abs(fb)), "%s: %r vs %r" % (what, fa, fb)

def nlim(f, x0, eps=sp.Rational(1, 10**7)):
    """Second route for a finite two-sided limit: average of f(x0 - eps) and f(x0 + eps) at 60 digits."""
    return (sp.N(f.subs(xr, x0 - eps), 60) + sp.N(f.subs(xr, x0 + eps), 60)) / 2

def vals(*vs):
    """Option strings for sympy-able values, duplicates removed."""
    return uniq_by_text([E(sp.nsimplify(v)) for v in vs])

def L(v):
    return E(sp.nsimplify(v))

def dec(v, k=2):
    """Decimal option such as $1.04$."""
    return "$%s$" % ("%.*f" % (k, float(v)))

# ------------------------------------------------------------------------------------------------ slot 1: slope of a tangent (warm-up, level 2)
def s01(B):
    for f, a in ((sin(xr), pi / 4), (cos(xr), pi / 3), (tan(xr), pi / 4), (sin(2 * xr), pi / 6), (log(cos(xr)), pi / 4)):
        m = sp.simplify(sp.diff(f, xr).subs(xr, a))
        h = R(1, 10**8)
        agree(m, (f.subs(xr, a + h) - f.subs(xr, a - h)) / (2 * h), "s01 slope")
        val = sp.simplify(f.subs(xr, a))
        add(B, "c2", 1, 2, "Tangent lines", "Find the slope of the tangent line to $y=%s$ at $x=%s$." % (tex(f), tex(a)), L(m), vals(-m, 2 * m, val, m / 2, -2 * m, 1 / m),
            "$y'=%s$, and at $x=%s$ this equals %s. The common slips are a wrong sign, forgetting the chain factor, or giving the height $y(%s)=%s$ instead of the slope." % (tex(sp.diff(f, xr)), tex(a), L(m), tex(a), tex(val)))

# ------------------------------------------------------------------------------------------------ slot 2: composite limits whose inner function vanishes to higher order
def s02(B):
    g = lambda a: sqrt(xr ** 2 + a ** 2) - a
    cases = [
        (sin(g(3)) / xr, "the inner function is $O(x^2)$, so $\\sin g\\approx g\\approx x^2/6$ and the quotient behaves like $x/6$", [R(1, 3), R(1, 6), 1, R(2, 3)]),
        (sin(g(2)) / xr ** 2, "$\\sin g\\approx g\\approx\\dfrac{x^2}{2a}$ with $a=2$, so the quotient tends to $\\frac1{4}$", [0, R(1, 2), 1, R(1, 8)]),
        ((1 - cos(g(2))) / xr ** 4, "$1-\\cos g\\approx g^2/2$ and $g\\approx x^2/4$, so the quotient tends to $\\frac12\\cdot\\frac1{16}$", [R(1, 16), R(1, 8), R(1, 4), 0]),
        (tan(sqrt(1 + 4 * xr) - 1) / xr, "$g=\\sqrt{1+4x}-1\\approx2x$ and $\\tan g\\approx g$", [1, R(1, 2), 4, 0]),
        ((exp(xr ** 2) - 1) / (1 - cos(xr)), "$e^{x^2}-1\\approx x^2$ and $1-\\cos x\\approx x^2/2$", [1, R(1, 2), 0, 4]),
    ]
    for f, why, wrongs in cases:
        v = sp.limit(f, xr, 0)
        agree(v, nlim(f, 0), "s02 limit", 1e-4)
        add(B, "c1", 2, 4, "Limits", "Evaluate $\\displaystyle\\lim_{x\\to0}%s$." % tex(f), lim_text(v), [lim_text(sp.nsimplify(w)) for w in wrongs if sp.nsimplify(w) != v] + [lim_text(sp.oo), "the limit does not exist"],
            "Replace each small piece by its leading behaviour: %s. The limit is %s. The trap is to say 'the inner function tends to 0, so the quotient tends to 1' without comparing the **orders** of numerator and denominator." % (why, lim_text(v)))

# ------------------------------------------------------------------------------------------------ slot 3: which hypothesis is needed? (concept, level 3)
def s03(B):
    qs = [
        ("c1", "Limits", "Which of the following is **not** required by the Squeeze Theorem for $f(x)\\le g(x)\\le h(x)$ near $a$?",
         "$g$ is continuous at $a$", ["$f(x)\\le g(x)\\le h(x)$ for all $x$ near $a$ (except possibly at $a$)", "$\\lim_{x\\to a}f(x)=\\lim_{x\\to a}h(x)$", "$f$ and $h$ have limits as $x\\to a$"],
         "The theorem needs the two outer functions to have the **same** limit and the inequality near $a$; it then *produces* the limit of $g$. Nothing is assumed about $g$ (not even that it is defined at $a$), and the inequality is not required at $a$ itself."),
        ("c1", "Intermediate Value Theorem", "Which hypothesis of the Intermediate Value Theorem cannot be dropped?",
         "$f$ is continuous on the closed interval $[a,b]$", ["$f$ is differentiable on $(a,b)$", "$f$ is increasing on $[a,b]$", "$f(a)$ and $f(b)$ are both positive"],
         "Differentiability and monotonicity are not needed (the IVT holds for every continuous function), and $f(a),f(b)$ must lie on **opposite sides** of the target value, not both positive. Continuity on $[a,b]$ is essential: $f(x)=1/x$ on $[-1,1]$ takes $-1$ and $1$ but never $0$."),
        ("c3", "Mean Value Theorem", "For which of these functions does Rolle's theorem **fail** on $[-1,1]$, although $f(-1)=f(1)$?",
         "$f(x)=|x|$", ["$f(x)=x^2-1$", "$f(x)=\\cos\\frac{\\pi x}{2}$", "$f(x)=x^4-x^2$"],
         "All four have $f(-1)=f(1)$ and are continuous. Only $|x|$ is not differentiable on the open interval (it has a corner at $0$), and indeed its derivative is never $0$."),
        ("c3", "Extreme values", "For which function does the Extreme Value Theorem guarantee an absolute maximum **and** minimum on the given interval?",
         "$f(x)=\\sqrt{x+1}$ on $[-1,3]$", ["$f(x)=\\dfrac1x$ on $[-1,1]$", "$f(x)=\\tan x$ on $[0,\\frac{\\pi}{2}]$", "$f(x)=\\dfrac{x}{x^2-4}$ on $[0,3]$"],
         "The theorem needs continuity on a **closed bounded** interval. $\\sqrt{x+1}$ is continuous on $[-1,3]$. The others are not continuous on their intervals: $\\frac1x$ at $0$, $\\tan x$ at $\\frac\\pi2$, $\\frac{x}{x^2-4}$ at $2$."),
        ("c3", "Extreme values", "Fermat's theorem says that if $f$ has a local extremum at an interior point $c$ and $f'(c)$ exists, then $f'(c)=0$. Which statement is true?",
         "$f(x)=x^3$ has $f'(0)=0$ but no local extremum at $0$", ["If $f'(c)=0$ then $f$ has a local extremum at $c$", "$f(x)=|x|$ has $f'(0)=0$ at its minimum", "A local extremum can only occur where $f'(c)=0$"],
         "Fermat's theorem is **one-directional**. $x^3$ shows that $f'(c)=0$ does not force an extremum, and $|x|$ has its minimum at a corner where $f'(0)$ does not exist, so extrema can also occur where the derivative is undefined."),
    ]
    cont = sp.calculus.util.continuous_domain
    assert cont(sqrt(xr + 1), xr, sp.S.Reals).contains(0) and not cont(1 / xr, xr, sp.S.Reals).contains(0) and not cont(xr / (xr ** 2 - 4), xr, sp.S.Reals).contains(2)     # the EVT claims above
    for ch, topic, stem, ok, wrong, expl in qs:
        add(B, ch, 3, 3, topic, stem, ok, wrong, expl)

# ------------------------------------------------------------------------------------------------ slot 4: linearization (argument versus variable, over- or under-estimate)
def s04(B):
    cases = [   # f, the number to approximate (as f at sqrt(arg)), its LaTeX, decimals shown, the typical wrong values
        (exp(xr ** 2), R(1, 25), "e^{0.04}", 2, ["1.04", "1.02", "1.08"]),
        (cos(xr ** 2), R(9, 100), "\\cos(0.09)", 2, ["0.91", "0.95", "0.99"]),
        (log(1 + xr ** 2), R(1, 25), "\\ln(1.04)", 2, ["0.04", "0.02", "0.05"]),
        ((1 + xr ** 2) ** 10, R(1, 100), "(1.01)^{10}", 2, ["1.10", "1.05", "1.15"]),
    ]
    for f, arg, name, k, wrong in cases:
        assert sp.diff(f, xr).subs(xr, 0) == 0                            # the tangent at 0 is horizontal, so L is constant
        Lx = f.subs(xr, 0)
        var = sqrt(arg)
        true = sp.N(f.subs(xr, var), 8)
        add(B, "c2", 4, 4, "Linearization", "Use the linearization $L(x)$ of $f(x)=%s$ at $x=0$ to approximate $%s$." % (tex(f), name), dec(Lx, k), ["$%s$" % w for w in wrong],
            "$f(0)=%s$ and $f'(x)=%s$ vanishes at $0$, so $L(x)=%s$ is **constant**. The number $%s$ equals $f(%s)$, so the approximation is $L(%s)=%s$ (the true value is about $%.4f$): the linearization of the *composite* is not the linearization of the outer function." % (
                tex(Lx), tex(sp.diff(f, xr)), tex(Lx), name, tex(var), tex(var), tex(Lx), float(true)))
    for f, a, x1, name, kind in ((log(xr), 1, R(11, 10), "\\ln1.1", "overestimate"), (exp(xr), 0, R(1, 10), "e^{0.1}", "underestimate"), (sqrt(xr), 4, R(41, 10), "\\sqrt{4.1}", "overestimate"), (xr ** R(1, 3), 8, R(83, 10), "\\sqrt[3]{8.3}", "overestimate")):
        Lx = f.subs(xr, a) + sp.diff(f, xr).subs(xr, a) * (xr - a)
        approx = sp.N(Lx.subs(xr, x1), 10); true = sp.N(f.subs(xr, x1), 10)
        assert (approx > true) == (kind == "overestimate"), "s04 over/under"
        other = "underestimate" if kind == "overestimate" else "overestimate"
        txt = lambda v, w: "$%.4f$, an %s" % (float(v), w)
        add(B, "c2", 4, 4, "Linearization", "Use the linearization of $f(x)=%s$ at $a=%s$ to approximate $%s$. What is the approximation, and is it an overestimate or an underestimate?" % (tex(f), a, name),
            txt(approx, kind), [txt(approx, other), txt(true, kind), txt(true, other)],
            "$L(x)=%s$, so $L(%s)=%.4f$; the true value is $%.4f$. The graph of $f$ is %s on this interval, so the tangent line lies %s the curve and $L$ gives an **%s**." % (
                tex(sp.simplify(Lx)), tex(x1), float(approx), float(true), "concave down" if kind == "overestimate" else "concave up", "above" if kind == "overestimate" else "below", kind))

# ------------------------------------------------------------------------------------------------ slot 5: derivative from a table of values, checked on Hermite interpolants
def hermite(v0, d0, v1, d1):
    """Cubic H with H(0)=v0, H'(0)=d0, H(1)=v1, H'(1)=d1."""
    c, d = sp.symbols("c d")
    H = v0 + d0 * xr + c * xr ** 2 + d * xr ** 3
    sol = sp.solve([H.subs(xr, 1) - v1, sp.diff(H, xr).subs(xr, 1) - d1], [c, d])
    return H.subs(sol)

def s05(B):
    tables = [   # (f(0), f(1), f'(0), f'(1)), (g(0), g(1), g'(0), g'(1)); g(0)=1 and f(0)=1 where the question needs the argument 1
        ((1, 3, -3, R(1, 2)), (1, 5, R(1, 2), -4)),
        ((1, 4, 2, -1), (1, 2, 3, R(1, 3))),
        ((2, 1, R(3, 2), 5), (1, 2, -2, 4)),
        ((1, -1, 4, -2), (1, 3, R(1, 4), 6)),
        ((3, 1, -1, 2), (1, 2, 5, R(3, 2))),
    ]
    forms = ["f(x+g(x))", "g(f(x))", "\\dfrac{f(x)}{g(x)}", "f\\left(g(x)^2\\right)", "x\\,f\\bigl(g(x)\\bigr)"]
    for (tf, tg), name in zip(tables, forms):
        f0, f1, fp0, fp1 = tf; g0, g1, gp0, gp1 = tg
        Hf, Hg = hermite(f0, fp0, f1, fp1), hermite(g0, gp0, g1, gp1)
        if name == "f(x+g(x))":
            pt, val, wr = 0, fp1 * (1 + gp0), [fp0 * (1 + gp0), fp1, fp1 * gp0, fp1 + gp0]
            why = "the inner function is $x+g(x)=0+g(0)=1$ at $x=0$, so $\\dfrac{d}{dx}f(x+g(x))=f'(x+g(x))\\,(1+g'(x))=f'(1)\\,(1+g'(0))$"
            expr = Hf.subs(xr, xr + Hg)
        elif name == "g(f(x))":
            pt, val, wr = 0, gp1 * fp0, [gp0 * fp0, gp1, gp1 + fp0, gp1 * fp1]
            why = "$\\dfrac{d}{dx}g(f(x))=g'(f(x))\\,f'(x)$ and $f(0)=1$, so we need $g'(1)\\,f'(0)$ (the outer derivative is evaluated at the **value** of the inner function)"
            expr = Hg.subs(xr, Hf)
        elif name == "\\dfrac{f(x)}{g(x)}":
            pt, val, wr = 1, (fp1 * g1 - f1 * gp1) / g1 ** 2, [fp1 / gp1, (fp1 * g1 + f1 * gp1) / g1 ** 2, fp1 * g1 - f1 * gp1, (f1 * gp1 - fp1 * g1) / g1 ** 2]
            why = "quotient rule at $x=1$: $\\dfrac{f'g-fg'}{g^2}$"
            expr = Hf / Hg
        elif name == "f\\left(g(x)^2\\right)":
            pt, val, wr = 0, fp1 * 2 * g0 * gp0, [fp1 * gp0, fp0 * 2 * g0 * gp0, fp1 * 2 * g1 * gp1, fp1]
            why = "$g(0)=1$, so $g(0)^2=1$ and $\\dfrac{d}{dx}f(g^2)=f'(g^2)\\cdot2gg'=f'(1)\\cdot2g(0)g'(0)$"
            expr = Hf.subs(xr, Hg ** 2)
        else:
            pt, val, wr = 0, f1, [fp1 * gp0, 0, f0, f1 + fp1 * gp0]
            why = "product rule: $f(g(x))+x\\,f'(g(x))g'(x)$; at $x=0$ the second term vanishes because of the factor $x$, leaving $f(g(0))=f(1)$"
            expr = xr * Hf.subs(xr, Hg)
        val = sp.nsimplify(val)
        agree(sp.diff(expr, xr).subs(xr, pt), val, "s05 table")
        tab = "$$\\begin{array}{c|cccc} x & f(x) & g(x) & f'(x) & g'(x)\\\\ \\hline 0 & %s & %s & %s & %s\\\\ 1 & %s & %s & %s & %s \\end{array}$$" % tuple(tex(v) for v in (f0, g0, fp0, gp0, f1, g1, fp1, gp1))
        add(B, "c2", 5, 4, "Differentiation rules", "Suppose $f$, $g$ and their derivatives take the following values.%s\nFind the derivative of $%s$ at $x=%d$." % (tab, name, pt), L(val), vals(*[w for w in wr if sp.nsimplify(w) != val]),
            "Chain rule: %s. Numbers: %s. Check: replacing the table by the cubic interpolants of the same data and differentiating gives the same value." % (why, L(val)))

# ------------------------------------------------------------------------------------------------ slot 6: modelling with composition (order of operations)
def s06(B):
    p = sp.Symbol("p", positive=True)
    for rate, fee in ((R(15, 2), 15), (8, 12), (10, 20), (R(33, 4), 12), (6, 25)):
        t = sp.Rational(rate, 100)
        tax_then_fee, fee_then_tax = sp.expand((1 + t) * p + fee), sp.expand((1 + t) * (p + fee))
        diff = sp.simplify(fee_then_tax - tax_then_fee); assert diff == t * fee and diff > 0
        add(B, "c1", 6, 3, "Modelling with functions",
            "A customer pays the price $p$, a tax of $%s\\%%$ and a delivery fee of $%d$ dollars. The tax does not have to be charged on the delivery fee. The price after tax is $T(p)=%s\\,p$ and the price after delivery is $D(p)=p+%d$. Which way of combining them gives the lower total?" % ("%g" % float(rate), fee, "%g" % float(1 + t), fee),
            "Apply the tax to the price first, then add the fee: $D(T(p))$",
            ["Add the fee first, then apply the tax to the sum: $T(D(p))$", "Both orders cost exactly the same", "It depends on the value of $p$"],
            "$D(T(p))=%sp+%d$ but $T(D(p))=%sp+%s$. The difference is $%s\\times%d=%s$ dollars, independent of $p$, because the second order taxes the fee as well. Composition is **not commutative**." % ("%g" % float(1 + t), fee, "%g" % float(1 + t), "%g" % float((1 + t) * fee), "%g" % float(t), fee, "%g" % float(diff)))
    q = sp.Symbol("q", positive=True)
    for d, v in ((20, 10), (25, 8), (15, 20), (30, 12)):
        k = 1 - sp.Rational(d, 100)
        first, second = sp.expand(k * q - v), sp.expand(k * (q - v))      # discount then voucher, versus voucher then discount
        diff = sp.simplify(second - first); assert diff == sp.Rational(d, 100) * v
        add(B, "c1", 6, 3, "Modelling with functions", "A voucher worth $%d$ dollars and a %d%% discount can be applied in either order to a price $q$. Which order gives the lower final price?" % (v, d),
            "Discount first, then the voucher: $%s$" % tex(first), ["Voucher first, then the discount: $%s$" % tex(second), "Both orders give the same price", "It depends on the value of $q$"],
            "Discount then voucher gives $%s$; voucher then discount gives $%s$. The first is lower by $%s\\times%d=%s$ dollars: the voucher is worth its full $%d$ dollars only if it is applied **after** the discount." % (tex(first), tex(second), tex(sp.Rational(d, 100)), v, tex(sp.nsimplify(diff)), v))
    for up, down in ((25, 20), (10, 10), (50, 50), (20, 25), (30, 30)):
        net = (100 + up) * (100 - down) / sp.Integer(10**4) - 1
        pc = sp.nsimplify(net * 100)
        pct = lambda w: "$%s\\%%$" % ("%+g" % float(w)).replace("+0", "0").replace("-0", "0") if w != 0 else "$0\\%$"
        wrongs = [w for w in (up - down, -abs(up - down), pc + 5, pc - 5, (up - down) / 2) if sp.nsimplify(w) != pc]
        add(B, "c1", 6, 3, "Modelling with functions", "A price rises by %d%% and then falls by %d%%. What is the net change relative to the original price?" % (up, down), pct(pc), uniq_by_text([pct(w) for w in wrongs]),
            "The factors multiply, they do not add: $%s\\times%s=%s$, a net change of %s." % (tex(sp.Rational(100 + up, 100)), tex(sp.Rational(100 - down, 100)), tex(1 + net), pct(pc)))
    f, g = lambda s: 3 * s + 1, lambda s: s ** 2 - 2
    comp = sp.expand(f(g(xr)) - g(f(xr)))
    add(B, "c1", 6, 3, "Composition", "Let $f(x)=3x+1$ and $g(x)=x^2-2$. Simplify $(f\\circ g)(x)-(g\\circ f)(x)$.", E(comp),
        [E(sp.expand(g(f(xr)) - f(g(xr)))), E(sp.expand(3 * xr ** 2 - 5 - (3 * xr + 1) ** 2 - 2)), E(sp.expand(f(g(xr)) - g(f(xr)) + 6 * xr))],
        "$(f\\circ g)(x)=3(x^2-2)+1=3x^2-5$ and $(g\\circ f)(x)=(3x+1)^2-2=9x^2+6x-1$. Subtract: $%s$." % tex(comp))

# ------------------------------------------------------------------------------------------------ slot 7: where is a function decreasing (closed intervals)
def closed_pieces(sol):
    """The monotone pieces of a solved inequality with their endpoints included (a function is monotone on the closed interval)."""
    parts = sol.args if isinstance(sol, sp.Union) else [sol]
    return sp.Union(*[sp.Interval(i.start, i.end) for i in parts])

def set_tex(s):
    return "$%s$" % sp.latex(s)

def s07(B):
    I, U, oo = sp.Interval, sp.Union, sp.oo
    cases = [   # f, kind, the wrong sets
        (xr ** 3 - 6 * xr ** 2 + 9 * xr, "decreasing", [I(0, 2), I(3, oo), I(-3, -1)]),
        (xr ** 3 - 3 * xr ** 2 - 9 * xr + 5, "decreasing", [I(-3, 1), I(3, oo), I(-oo, -1)]),
        (2 * xr ** 3 - 9 * xr ** 2 + 12 * xr, "increasing", [I(1, 2), I(-oo, 2), I(0, oo)]),
        (xr ** 4 - 8 * xr ** 2, "decreasing", [U(I(-2, 0), I(2, oo)), I(-2, 2), I(-oo, 0)]),
        (xr * exp(-xr), "decreasing", [I(-oo, 1), I(0, oo), I(-1, 1)]),
        (xr / (xr ** 2 + 1), "decreasing", [I(-1, 1), I(-oo, 0), I(0, oo)]),
    ]
    for f, kind, wrongs in cases:
        fp = sp.diff(f, xr)
        sol = sp.solveset(fp < 0 if kind == "decreasing" else fp > 0, xr, sp.S.Reals)
        good = closed_pieces(sol)
        h = R(1, 10**6)                                                        # second route: finite differences on a grid of points
        for k in range(-60, 61):
            v = sp.Rational(k, 8)
            slope = (f.subs(xr, v + h) - f.subs(xr, v - h)) / (2 * h)
            if good.contains(v) and not sp.simplify(sol.contains(v)):
                continue                                                       # an endpoint: slope is 0 there
            assert (float(slope) < 0 if kind == "decreasing" else float(slope) > 0) == bool(sol.contains(v)), "s07 sign %s %s" % (f, v)
        assert all(w != good for w in wrongs)
        add(B, "c3", 7, 3, "First derivative test", "Find the interval(s) where $f(x)=%s$ is %s." % (tex(f), kind), set_tex(good), [set_tex(w) for w in wrongs],
            "$f'(x)=%s$, which is %s exactly on the open set %s. The function is %s on the **closed** intervals (endpoints included, because continuity lets the monotonic test extend to them). The other options mix an increasing and a decreasing part or miss a sign change." % (
                tex(sp.factor(fp)), "negative" if kind == "decreasing" else "positive", set_tex(sol), kind))

def build_part1(B):
    for fn in (s01, s02, s03, s04, s05, s06, s07):
        fn(B)
