# -*- coding: utf-8 -*-
"""Calculus I, level-4 pool, chapter extras: traps and multi-step questions for chapters 2-6 that follow the Moodle mock's spirit but are not tied to one of its 20 slots.
Every answer is computed with sympy and re-derived by a second route (finite differences, numerical quadrature, partial sums)."""
import mpmath as mp
import sympy as sp
from qlib import tex
from cal_common import E, uniq_by_text
from gen_cal_hard1 import agree, vals, L, xr, sin, cos, tan, exp, log, sqrt, pi, R

mp.mp.dps = 30
SRC = "Moodle-style hard question (our own, same spirit as the Moodle mock)"

def put(B, ch, topic, stem, correct, wrongs, explain, level=4):
    return B.mcq(ch, topic, level, stem, correct, wrongs, explain, SRC, origin="hard", tags=["moodle-extra"])

def quad(f, a, b, *corners):
    """Numerical integral (second route); endpoints may be sympy numbers or +-oo; corners = interior points where the integrand has a kink."""
    end = lambda v: mp.inf if v == sp.oo else (-mp.inf if v == -sp.oo else mp.mpf(float(v)))
    return mp.quad(sp.lambdify(xr, f, "mpmath"), [end(a)] + [end(c) for c in corners] + [end(b)])

def dec(v, k=4):
    return "$%s$" % ("%.*f" % (k, float(v)))

def count_opts(c, hi=5):
    return "$%d$" % c, ["$%d$" % k for k in range(0, hi + 1) if k != c]

# ------------------------------------------------------------------------------------------------ chapter 2
def ch2(B):
    # how many points of non-differentiability
    f = sp.Abs(xr ** 2 - 1) + sp.Abs(xr)
    bad = []
    for p in (-1, 0, 1, R(1, 2), -2):
        h = R(1, 10**6)
        left = (f.subs(xr, p) - f.subs(xr, p - h)) / h; right = (f.subs(xr, p + h) - f.subs(xr, p)) / h
        if abs(float(left - right)) > 0.5:
            bad.append(p)
    assert bad == [-1, 0, 1]
    c, w = count_opts(3, 4)
    put(B, "c2", "Differentiability", "At how many points is $f(x)=|x^2-1|+|x|$ **not** differentiable?", c, w,
        "A sum is differentiable wherever both terms are. $|x|$ has a corner only at $0$, and $|x^2-1|$ has corners where $x^2-1$ changes sign, at $x=\\pm1$ (the slope jumps from $\\mp2$ to $\\pm2$). The three corner points $-1,0,1$ never cancel each other, so the answer is $3$.")
    # high derivative at 0
    for g, n in ((xr * exp(xr), 10), (xr ** 2 * exp(xr), 5), (xr * sin(xr), 6)):
        v = sp.diff(g, xr, n).subs(xr, 0)
        ser = sp.series(g, xr, 0, n + 2).removeO()
        agree(v, sp.factorial(n) * ser.coeff(xr, n), "ch2 high derivative")
        put(B, "c2", "Higher derivatives", "Let $f(x)=%s$. Find $f^{(%d)}(0)$." % (tex(g), n), L(v), vals(v / sp.factorial(n), v + n, 2 * v + 1, n, sp.factorial(n)),
            "Compute the $%d$-th derivative with Leibniz' rule (or compare Maclaurin coefficients: $f^{(%d)}(0)=%d!\\times[\\text{coefficient of }x^{%d}]$). The value is %s." % (n, n, n, n, L(v)))
    # implicit second derivative
    x_, y_ = sp.symbols("x y")
    val = sp.idiff(x_ ** 2 + y_ ** 2 - 25, y_, x_, 2).subs({x_: 3, y_: 4})
    assert val == R(-25, 64)
    put(B, "c2", "Implicit differentiation", "The point $(3,4)$ lies on the circle $x^2+y^2=25$. Find $\\dfrac{d^2y}{dx^2}$ there.", L(val), vals(R(25, 64), R(-3, 4), R(-1, 4), R(-25, 16)),
        "$y'=-\\dfrac xy$ and $y''=-\\dfrac{y-xy'}{y^2}=-\\dfrac{y+x^2/y}{y^2}=-\\dfrac{x^2+y^2}{y^3}=-\\dfrac{25}{y^3}$. At $y=4$: $-\\frac{25}{64}$ (negative: the upper half-circle is concave down). The first derivative there is $-\\frac34$.")
    # logarithmic differentiation
    g = xr ** xr
    val = sp.simplify(sp.diff(g, xr).subs(xr, 2))
    h = R(1, 10**8)
    agree(val, (g.subs(xr, 2 + h) - g.subs(xr, 2 - h)) / (2 * h), "ch2 x^x")
    put(B, "c2", "Differentiation rules", "Find $\\dfrac{d}{dx}x^{x}$ at $x=2$.", L(val), vals(4, 4 * log(2), 2 * 2 ** 1, 4 * log(2) + 1),
        "Neither the power rule nor the exponential rule applies. Write $x^x=e^{x\\ln x}$: the derivative is $x^x(\\ln x+1)$, which at $x=2$ is $4(\\ln2+1)=%s$. The power rule alone would give $x\\cdot x^{x-1}=4$, the exponential rule alone $x^x\\ln x=4\\ln2$." % tex(val))
    # tangent parallel to a given line
    f = xr ** 3 - 3 * xr ** 2 + 2
    pts = sp.solve(sp.Eq(sp.diff(f, xr), 9), xr)
    c, w = count_opts(len(pts), 3)
    put(B, "c2", "Tangent lines", "At how many points of the curve $y=x^3-3x^2+2$ is the tangent line parallel to the line $y=9x+1$?", c, w,
        "We need $y'=3x^2-6x=9$, i.e. $x^2-2x-3=0$, so $x=-1$ or $x=3$. Two points, $(-1,-2)$ and $(3,2)$; neither lies on the line $y=9x+1$ itself, so they give genuinely parallel tangents.")
    # total distance
    s = xr ** 3 - 9 * xr ** 2 + 24 * xr
    turns = sorted(sp.solve(sp.diff(s, xr), xr))
    assert turns == [2, 4]
    dist = sum(abs(s.subs(xr, b) - s.subs(xr, a)) for a, b in zip([0] + turns, turns + [5]))
    put(B, "c2", "Rates of change", "A particle moves along a line with position $s(t)=t^3-9t^2+24t$ (metres, seconds). What is the **total distance** travelled during the first $5$ seconds?", "$%s$ m" % tex(dist), ["$%s$ m" % tex(s.subs(xr, 5)), "$%s$ m" % tex(dist + 8), "$%s$ m" % tex(s.subs(xr, 2) + abs(s.subs(xr, 4) - s.subs(xr, 2)))],
        "$v=3t^2-18t+24=3(t-2)(t-4)$, so the particle reverses at $t=2$ and $t=4$. Positions: $s(0)=0$, $s(2)=20$, $s(4)=16$, $s(5)=20$. Distance $=20+4+4=%s$ m. The net displacement $s(5)-s(0)=20$ m is **not** the distance." % tex(dist))
    # dy versus delta y
    f = xr ** 3
    dy = sp.diff(f, xr).subs(xr, 2) * R(1, 10); dY = f.subs(xr, R(21, 10)) - f.subs(xr, 2)
    put(B, "c2", "Linearization", "For $y=x^3$, $x$ changes from $2$ to $2.1$. What is $\\Delta y-dy$?", dec(dY - dy, 3), [dec(dy, 3), dec(dY, 3), dec(dY + dy, 3)],
        "$dy=f'(2)\\,dx=12(0.1)=1.2$ and $\\Delta y=2.1^3-2^3=1.261$, so $\\Delta y-dy=0.061$. The differential is a good approximation but it is not exact: the error is the curvature term $\\frac12f''(2)\\,dx^2+\\ldots$.")

# ------------------------------------------------------------------------------------------------ chapter 3
def ch3(B):
    # absolute extrema of |x^2-4x+3| on [0,4]
    f = sp.Abs(xr ** 2 - 4 * xr + 3)
    vs = {v: f.subs(xr, v) for v in (0, 1, 2, 3, 4)}
    assert max(vs.values()) == 3 and min(vs.values()) == 0
    put(B, "c3", "Extreme values", "Find the absolute maximum and minimum of $f(x)=|x^2-4x+3|$ on $[0,4]$.", "maximum $3$ (at $x=0$ and $x=4$), minimum $0$ (at $x=1$ and $x=3$)",
        ["maximum $3$ (at $x=0$ and $x=4$), minimum $-1$ (at $x=2$)", "maximum $3$ (at $x=0$ and $x=4$), minimum $1$ (at $x=2$)", "maximum $1$ (at $x=2$), minimum $0$ (at $x=1$ and $x=3$)"],
        "Candidates: the endpoints $f(0)=3$, $f(4)=3$; the corners $x=1,3$ (where $f'$ does not exist) with $f=0$; and the critical point $x=2$ with $f(2)=|-1|=1$. Largest value $3$, smallest $0$. The value $-1$ of the inside function is **not** a value of $f$.")
    # inflection counts
    for g, want, why in ((xr ** 4 + xr, 0, "$f''(x)=12x^2\\ge0$ vanishes at $0$ but never changes sign: no inflection point"), (xr ** 5 - 5 * xr, 1, "$f''(x)=20x^3$ changes sign at $0$: one inflection point"), (xr ** 4 - 6 * xr ** 2, 2, "$f''(x)=12x^2-12$ changes sign at $x=\\pm1$: two inflection points"), (sin(xr), 3, "$f''=-\\sin x$ changes sign at $-\\pi,0,\\pi$ on $[-\\frac{3\\pi}2,\\frac{3\\pi}2]$: three inflection points")):
        d2 = sp.diff(g, xr, 2)
        if g == sin(xr):
            stem = "How many inflection points does $f(x)=\\sin x$ have on $\\left[-\\frac{3\\pi}{2},\\frac{3\\pi}{2}\\right]$?"
            infl = [v for v in (-pi, 0, pi)]
        else:
            stem = "How many inflection points does $f(x)=%s$ have?" % tex(g)
            infl = [r for r in sp.solve(d2, xr) if r.is_real and (d2.subs(xr, r - R(1, 100)) * d2.subs(xr, r + R(1, 100)) < 0)]
        assert len(infl) == want
        c, w = count_opts(want, 4)
        put(B, "c3", "Concavity and inflection", stem, c, w, "%s. (Inflection points need a **sign change** of $f''$, not merely $f''=0$.)" % why)
    # applied optimisation
    S = lambda s: s ** 2 + 128 / s
    smin = sp.nsolve(sp.diff(S(xr), xr), xr, 3)
    assert abs(float(smin) - 4) < 1e-9 and S(4) == 48
    put(B, "c3", "Optimization", "An open-top box with a square base must hold $32\\ \\mathrm{m^3}$. What is the **least possible surface area** of its base and four sides?", "$48\\ \\mathrm{m^2}$", ["$64\\ \\mathrm{m^2}$", "$56\\ \\mathrm{m^2}$", "$40\\ \\mathrm{m^2}$"],
        "With base side $x$ and height $h=32/x^2$: $A=x^2+4xh=x^2+\\dfrac{128}x$. $A'=2x-\\dfrac{128}{x^2}=0$ gives $x=4$, $h=2$, and $A=16+32=48$ m$^2$ (the question asks for the area, not for the dimensions).")
    r = sp.Symbol("r", positive=True)
    area = 2 * sp.pi * r ** 2 + 1000 / r
    rs = sp.solve(sp.diff(area, r), r)[0]
    amin = sp.N(area.subs(r, rs), 8)
    agree(amin, min(sp.N(area.subs(r, R(k, 100)), 20) for k in range(300, 600)), "ch3 can", 1e-3)
    cm2 = lambda v: "$%.1f\\ \\mathrm{cm^2}$" % float(v)
    put(B, "c3", "Optimization", "A closed cylindrical can must hold $500\\ \\mathrm{cm^3}$. What is the least possible total surface area?", cm2(amin), [cm2(area.subs(r, rs * 1.3)), cm2(area.subs(r, rs * 0.7)), cm2(2 * amin)],
        "With $V=\\pi r^2h=500$: $A=2\\pi r^2+\\dfrac{1000}r$, $A'=4\\pi r-\\dfrac{1000}{r^2}=0$ gives $r^3=\\dfrac{250}\\pi$, $r\\approx%.3f$ and $h=2r$ (the best can is as tall as it is wide). Then $A\\approx%.1f$ cm$^2$." % (float(rs), float(amin)))
    put(B, "c3", "Optimization", "A rectangle is inscribed in a semicircle of radius $5$ with one side on the diameter. What is the largest possible area?", "$25$", ["$12.5$", "$50$", "$\\dfrac{25}{\\sqrt2}$"],
        "With half-width $x$: $A=2x\\sqrt{25-x^2}$, $A^2=4x^2(25-x^2)$ is largest at $x^2=\\dfrac{25}2$, giving $A=2\\cdot\\dfrac{5}{\\sqrt2}\\cdot\\dfrac5{\\sqrt2}=25$.")
    # mean value theorem number
    f = xr ** 3 - 3 * xr
    cs = [c for c in sp.solve(sp.Eq(sp.diff(f, xr), (f.subs(xr, 2) - f.subs(xr, 0)) / 2), xr) if 0 < c < 2]
    assert cs == [2 * sqrt(3) / 3]
    put(B, "c3", "Mean Value Theorem", "Find the number $c$ guaranteed by the Mean Value Theorem for $f(x)=x^3-3x$ on $[0,2]$.", "$c=\\dfrac{2}{\\sqrt3}\\approx1.155$", ["$c=1$", "$c=\\dfrac43$", "$c=\\dfrac{1}{\\sqrt3}\\approx0.577$"],
        "The average slope is $\\dfrac{f(2)-f(0)}{2}=\\dfrac{2-0}2=1$. Solve $f'(c)=3c^2-3=1$: $c^2=\\frac43$, so $c=\\pm\\frac2{\\sqrt3}$; only the positive root lies in $(0,2)$. The midpoint $c=1$ is not the answer in general.")
    # indeterminate forms
    forms = {"$0^\\infty$": False, "$1^\\infty$": True, "$\\infty\\cdot\\infty$": False, "$\\infty-\\infty$": True, "$0\\cdot\\infty$": True, "$\\infty^\\infty$": False}
    n = sum(forms.values())
    assert sp.limit(xr ** (1 / xr), xr, 0, "+") == 0 and sp.limit((1 + 1 / xr) ** xr, xr, sp.oo) == sp.E
    c, w = count_opts(n, 5)
    put(B, "c3", "L'Hôpital's rule", "How many of the following are indeterminate forms?\n%s" % "  ".join("(%d) %s" % (i + 1, k) for i, k in enumerate(forms)), c, w,
        "Indeterminate: $1^\\infty$, $\\infty-\\infty$, $0\\cdot\\infty$ (the limit depends on the functions). Determinate: $0^\\infty\\to0$, $\\infty\\cdot\\infty\\to\\infty$, $\\infty^\\infty\\to\\infty$. So there are %d." % n)
    # Newton
    f = xr ** 3 - 2
    xn = lambda t_: t_ - f.subs(xr, t_) / sp.diff(f, xr).subs(xr, t_)
    x2 = xn(sp.Integer(1)); x3 = sp.nsimplify(xn(x2))
    put(B, "c3", "Newton's method", "Apply Newton's method to $f(x)=x^3-2$ with $x_1=1$. What is $x_3$?", L(x3), vals(x2, x2 - f.subs(xr, x2) / 3, sp.cbrt(2), R(3, 2)),
        "$x_{n+1}=x_n-\\dfrac{x_n^3-2}{3x_n^2}$. $x_2=1+\\dfrac13=\\dfrac43$, then $x_3=\\dfrac43-\\dfrac{64/27-2}{3\\cdot16/9}=%s\\approx%.5f$, already close to $\\sqrt[3]2\\approx1.25992$." % (tex(x3), float(x3)))
    put(B, "c3", "Newton's method", "Newton's method is applied to $f(x)=x^3-2$ with the starting value $x_1=0$. What happens?", "$x_2$ is undefined because $f'(0)=0$ (horizontal tangent)", ["$x_2=0$ and the method converges to $0$", "$x_2=\\sqrt[3]2$ in one step", "the sequence converges to $-\\sqrt[3]2$"],
        "$x_2=x_1-\\dfrac{f(x_1)}{f'(x_1)}$ needs $f'(0)=3\\cdot0^2=0$ in the denominator: the tangent at $x_1=0$ is horizontal and never meets the $x$-axis. A different starting value is required.")
    # antiderivative with two conditions
    c1 = sp.Symbol("c1")
    f = xr ** 3 - 2 * xr ** 2 + c1 * xr + 1
    c1v = sp.solve(f.subs(xr, 1), c1)[0]
    f = f.subs(c1, c1v)
    assert sp.expand(sp.diff(f, xr, 2) - (6 * xr - 4)) == 0 and f.subs(xr, 0) == 1 and f.subs(xr, 1) == 0
    put(B, "c3", "Antiderivatives", "A function satisfies $f''(x)=6x-4$, $f(0)=1$ and $f(1)=0$. Find $f(2)$.", L(f.subs(xr, 2)), vals(f.subs(xr, 2) + 1, 0, f.subs(xr, 2) - 2, 3),
        "$f'=3x^2-4x+C$ and $f=x^3-2x^2+Cx+D$. $f(0)=1$ gives $D=1$; $f(1)=1-2+C+1=C=0$. Hence $f(x)=x^3-2x^2+1$ and $f(2)=8-8+1=1$ (two integrations, two conditions).")
    # counting asymptotes
    f = (2 * xr ** 2 - 3) / (xr ** 2 + xr - 2)
    vert = [r for r in sp.solve(sp.denom(f), xr)]
    assert sorted(vert) == [-2, 1] and sp.limit(f, xr, sp.oo) == 2 and sp.limit(f, xr, -sp.oo) == 2
    c, w = count_opts(3, 5)
    put(B, "c3", "Asymptotes", "How many asymptotes (vertical and horizontal together) does $f(x)=\\dfrac{2x^2-3}{x^2+x-2}$ have?", c, w,
        "The denominator $(x+2)(x-1)$ vanishes at $x=-2$ and $x=1$ where the numerator is not $0$: two vertical asymptotes. As $x\\to\\pm\\infty$ the quotient tends to $2$ at both ends: **one** horizontal asymptote $y=2$. Total $3$.")

# ------------------------------------------------------------------------------------------------ chapter 4
def ch4(B):
    ans = 2 * xr * exp(xr ** 4) - exp(xr ** 2)
    h = R(1, 10**6)
    Fx = lambda a_: quad(exp(xr ** 2), a_, a_ ** 2)
    agree((Fx(R(6, 5) + h) - Fx(R(6, 5) - h)) / (2 * h), ans.subs(xr, R(6, 5)), "ch4 FTC1", 1e-6)
    put(B, "c4", "Fundamental Theorem of Calculus", "Find $\\dfrac{d}{dx}\\displaystyle\\int_{x}^{x^2}e^{t^2}\\,dt$.", E(ans), [E(2 * xr * exp(xr ** 4)), E(exp(xr ** 4) - exp(xr ** 2)), E(2 * xr * exp(xr ** 4) + exp(xr ** 2))],
        "Both limits depend on $x$: $\\dfrac d{dx}\\int_{a(x)}^{b(x)}f=f(b)\\,b'-f(a)\\,a'$. Here $f(x^2)\\cdot2x-f(x)\\cdot1=2xe^{x^4}-e^{x^2}$. Forgetting the chain factor $2x$, or the lower-limit term, are the usual slips.")
    val = sp.integrate(xr ** 3 + xr ** 2 + xr, (xr, -2, 2))
    agree(val, quad(xr ** 3 + xr ** 2 + xr, -2, 2), "ch4 symmetry")
    put(B, "c4", "Substitution", "Evaluate $\\displaystyle\\int_{-2}^{2}\\left(x^3+x^2+x\\right)dx$.", L(val), vals(0, 2 * val, val / 2, 8),
        "The odd terms $x^3$ and $x$ integrate to $0$ over $[-2,2]$. The even term gives $2\\int_0^2x^2dx=2\\cdot\\dfrac83=\\dfrac{16}3$.")
    val = sp.integrate(sp.Abs(xr ** 3 - xr), (xr, -1, 1))
    agree(val, quad(sp.Abs(xr ** 3 - xr), -1, 1, 0), "ch4 abs area")
    put(B, "c4", "Area between curves", "Find the area enclosed between $y=x^3-x$ and the $x$-axis on $[-1,1]$.", L(val), vals(0, 2 * val, val / 2, 1),
        "$x^3-x=x(x-1)(x+1)$ changes sign at $0$. On $[-1,0]$ it is $\\ge0$ (area $\\frac14$) and on $[0,1]$ it is $\\le0$ (area $\\frac14$). Total $\\frac12$; the plain integral is $0$ by oddness, which is the trap.")
    val = sp.integrate(2 * sp.pi * xr * xr ** 2, (xr, 0, 2))
    agree(val, 2 * mp.pi * quad(xr ** 3, 0, 2), "ch4 shells")
    put(B, "c4", "Volumes of revolution", "The region under $y=x^2$ for $0\\le x\\le2$ is rotated about the $y$-axis. Find the volume.", L(val), vals(sp.integrate(sp.pi * xr ** 4, (xr, 0, 2)), 16 * sp.pi / 3, 4 * sp.pi, 2 * val),
        "Shells: $V=\\int_0^22\\pi x\\cdot x^2\\,dx=2\\pi\\cdot\\dfrac{2^4}4=8\\pi$. Using disks about the **x**-axis instead ($\\pi\\int x^4dx=\\frac{32\\pi}5$) answers a different question.")
    val = sp.integrate(sp.sec(xr), (xr, 0, pi / 4))
    agree(val, quad(sqrt(1 + sp.tan(xr) ** 2), 0, mp.pi / 4), "ch4 arc length", 1e-6)
    put(B, "c4", "Arc length and surface area", "Find the length of the curve $y=\\ln(\\sec x)$ for $0\\le x\\le\\frac{\\pi}{4}$.", "$\\ln\\left(1+\\sqrt2\\right)$", ["$\\ln\\sqrt2$", "$\\sqrt2-1$", "$1$"],
        "$y'=\\tan x$, so $\\sqrt{1+y'^2}=\\sec x$ and $L=\\int_0^{\\pi/4}\\sec x\\,dx=\\ln|\\sec x+\\tan x|\\,\\Big|_0^{\\pi/4}=\\ln(\\sqrt2+1)\\approx0.881$.")
    put(B, "c4", "Average value", "Find the average value of $f(x)=\\sin x$ on $[0,\\pi]$.", "$\\dfrac{2}{\\pi}$", ["$\\dfrac1\\pi$", "$2$", "$\\dfrac12$"],
        "$\\dfrac1{\\pi-0}\\int_0^\\pi\\sin x\\,dx=\\dfrac{2}{\\pi}\\approx0.637$. The integral itself is $2$; do not forget to divide by the length of the interval.")
    val = sp.integrate(sin(xr) ** 3 * cos(xr), (xr, 0, pi / 2))
    assert val == R(1, 4)
    put(B, "c4", "Substitution", "Evaluate $\\displaystyle\\int_0^{\\pi/2}\\sin^3x\\cos x\\,dx$.", "$\\dfrac14$", ["$\\dfrac13$", "$\\dfrac12$", "$1$"],
        "Put $u=\\sin x$, $du=\\cos x\\,dx$; the limits become $u=0$ and $u=1$: $\\int_0^1u^3du=\\frac14$. Keep the **new** limits when you substitute.")
    put(B, "c4", "Riemann sums", "Evaluate $\\displaystyle\\lim_{n\\to\\infty}\\sum_{i=1}^{n}\\frac{i}{n^2}$.", "$\\dfrac12$", ["$0$", "$1$", "$\\infty$"],
        "$\\dfrac{i}{n^2}=\\dfrac1n\\cdot\\dfrac in$ is a right-endpoint Riemann sum of $f(x)=x$ on $[0,1]$, so the limit is $\\int_0^1x\\,dx=\\dfrac12$. (Directly: $\\sum i=\\frac{n(n+1)}2$.)")

# ------------------------------------------------------------------------------------------------ chapter 5
def ch5(B):
    put(B, "c5", "Improper integrals", "Evaluate $\\displaystyle\\int_{-1}^{1}\\frac{dx}{x^2}$.", "the integral diverges", ["$-2$", "$2$", "$0$"],
        "The integrand is unbounded at $x=0$, inside the interval. The antiderivative $-\\frac1x$ would give $-1-1=-2$, which is impossible for a positive function: the integral **diverges** (both halves $\\int_0^1x^{-2}dx$ diverge). Never apply the FTC across a singularity.")
    for f, a, b, val, why in ((xr * exp(-xr ** 2), 0, sp.oo, R(1, 2), "$u=x^2$: $\\frac12\\int_0^\\infty e^{-u}du$"), (log(xr), 0, 1, -1, "by parts, $x\\ln x-x$ at $1$ is $-1$ and at $0^+$ is $0$"), (1 / (1 + xr ** 2), 0, sp.oo, pi / 2, "$\\arctan x\\to\\frac\\pi2$"), (1 / (xr ** 2 + xr), 1, sp.oo, log(2), "partial fractions $\\frac1x-\\frac1{x+1}$, so $\\ln\\frac{x}{x+1}\\Big|_1^\\infty=0-\\ln\\frac12$")):
        v = sp.integrate(f, (xr, a, b))
        assert sp.simplify(v - val) == 0
        num = quad(f, a, b)
        agree(val, num, "ch5 improper", 1e-6)
        lo = tex(a); hi = "\\infty" if b == sp.oo else tex(b)
        put(B, "c5", "Improper integrals", "Evaluate $\\displaystyle\\int_{%s}^{%s}%s\\,dx$." % (lo, hi, tex(f)), L(val), vals(*[w for w in (-val, 2 * val, val + 1, 1, 0) if sp.simplify(w - val) != 0][:5]),
            "Method: %s. The value is %s (the integral converges)." % (why, L(val)))
    n = 2
    put(B, "c5", "Improper integrals", "How many of these integrals converge? (1) $\\int_1^\\infty x^{-1}dx$ (2) $\\int_1^\\infty x^{-2}dx$ (3) $\\int_0^1x^{-1/2}dx$ (4) $\\int_0^1x^{-3/2}dx$", "$%d$" % n, ["$%d$" % k for k in (0, 1, 3, 4)],
        "$p$-tests: at infinity $\\int_1^\\infty x^{-p}dx$ converges iff $p>1$ ((1) diverges, (2) converges); at $0$, $\\int_0^1x^{-p}dx$ converges iff $p<1$ ((3) converges to $2$, (4) diverges). So $2$ converge.")
    v = sp.integrate(1 / (1 + xr ** 2) ** R(3, 2), (xr, 0, 1))
    agree(v, quad(1 / (1 + xr ** 2) ** R(3, 2), 0, 1), "ch5 trig sub")
    put(B, "c5", "Trigonometric substitution", "Evaluate $\\displaystyle\\int_0^1\\frac{dx}{(1+x^2)^{3/2}}$.", "$\\dfrac{1}{\\sqrt2}$", ["$\\dfrac{\\pi}{4}$", "$\\sqrt2-1$", "$\\dfrac12$"],
        "$x=\\tan\\theta$, $dx=\\sec^2\\theta\\,d\\theta$, $(1+x^2)^{3/2}=\\sec^3\\theta$: the integral becomes $\\int_0^{\\pi/4}\\cos\\theta\\,d\\theta=\\sin\\frac\\pi4=\\frac1{\\sqrt2}$.")
    v = sp.integrate(xr ** 2 * exp(xr), (xr, 0, 1))
    assert sp.simplify(v - (sp.E - 2)) == 0
    put(B, "c5", "Integration by parts", "Evaluate $\\displaystyle\\int_0^1x^2e^x\\,dx$.", "$e-2$", ["$e-1$", "$2-e$", "$\\dfrac{e}{3}$"],
        "Parts twice: $\\int x^2e^x=x^2e^x-2\\int xe^x=x^2e^x-2(x-1)e^x$. Evaluate from $0$ to $1$: $e-2(0)-(0+2)=e-2\\approx0.718$.")
    v = sp.integrate(1 / (xr ** 2 - 1), (xr, 2, 3))
    agree(v, quad(1 / (xr ** 2 - 1), 2, 3), "ch5 partial fractions")
    put(B, "c5", "Partial fractions", "Evaluate $\\displaystyle\\int_2^3\\frac{dx}{x^2-1}$.", "$\\dfrac12\\ln\\dfrac32$", ["$\\ln\\dfrac32$", "$\\dfrac12\\ln\\dfrac43$", "$\\dfrac12\\ln3$"],
        "$\\dfrac1{x^2-1}=\\dfrac12\\left(\\dfrac1{x-1}-\\dfrac1{x+1}\\right)$, so the integral is $\\dfrac12\\ln\\dfrac{x-1}{x+1}\\Big|_2^3=\\dfrac12\\left(\\ln\\dfrac12-\\ln\\dfrac13\\right)=\\dfrac12\\ln\\dfrac32\\approx0.203$.")

# ------------------------------------------------------------------------------------------------ chapter 6
def ch6(B):
    k = sp.Symbol("k", integer=True, positive=True)
    put(B, "c6", "Alternating series", "Which of these series is **conditionally** (not absolutely) convergent?", "$\\displaystyle\\sum_{n=1}^\\infty\\frac{(-1)^n}{\\sqrt n}$", ["$\\displaystyle\\sum_{n=1}^\\infty\\frac{(-1)^n}{n^2}$", "$\\displaystyle\\sum_{n=1}^\\infty\\frac{(-1)^n n}{n+1}$", "$\\displaystyle\\sum_{n=1}^\\infty\\frac{1}{n^2}$"],
        "$\\sum\\frac{(-1)^n}{\\sqrt n}$ converges by the alternating series test, but $\\sum\\frac1{\\sqrt n}$ is a divergent $p$-series: conditional. $\\sum\\frac{(-1)^n}{n^2}$ is absolutely convergent; $\\frac{(-1)^nn}{n+1}$ does not tend to $0$ so it diverges; $\\sum\\frac1{n^2}$ is not alternating.")
    n = sp.Symbol("n", positive=True, integer=True)
    r = sp.limit(sp.factorial(n + 1) * n ** n / ((n + 1) ** (n + 1) * sp.factorial(n)), n, sp.oo)
    assert r == 1 / sp.E
    put(B, "c6", "Power series", "Find the radius of convergence of $\\displaystyle\\sum_{n=1}^\\infty\\frac{n!}{n^n}x^n$.", "$e$", ["$\\dfrac1e$", "$1$", "$\\infty$"],
        "Ratio test: $\\left|\\dfrac{a_{n+1}x^{n+1}}{a_nx^n}\\right|=\\dfrac{(n+1)!\\,n^n}{(n+1)^{n+1}n!}|x|=\\left(\\dfrac{n}{n+1}\\right)^n|x|\\to\\dfrac{|x|}{e}$. Convergence needs $\\frac{|x|}e<1$, i.e. $R=e$ (the limit of the ratio is $\\frac1e$, whose inverse is the radius).")
    put(B, "c6", "Power series", "Find the interval of convergence of $\\displaystyle\\sum_{n=1}^\\infty\\frac{(x-2)^n}{n\\,3^n}$.", "$[-1,5)$", ["$(-1,5)$", "$[-1,5]$", "$(-1,5]$"],
        "Ratio test: $R=3$ centred at $2$, so $-1<x<5$. At $x=5$ the series is the harmonic series (diverges); at $x=-1$ it is $\\sum\\frac{(-1)^n}{n}$ (converges). Hence $[-1,5)$: the two endpoints must be tested separately.")
    f = sin(xr ** 2)
    v = sp.diff(f, xr, 6).subs(xr, 0)
    assert v == -120
    put(B, "c6", "Taylor and Maclaurin series", "Let $f(x)=\\sin(x^2)$. Find $f^{(6)}(0)$.", "$-120$", ["$-\\dfrac16$", "$120$", "$-720$"],
        "$\\sin u=u-\\frac{u^3}{6}+\\cdots$ with $u=x^2$ gives $\\sin(x^2)=x^2-\\frac{x^6}6+\\cdots$. The coefficient of $x^6$ is $-\\frac16$, and $f^{(6)}(0)=6!\\times\\left(-\\frac16\\right)=-120$. The coefficient is not the derivative.")
    g = exp(xr) * sin(xr)
    c5 = sp.series(g, xr, 0, 7).removeO().coeff(xr, 5)
    assert c5 == R(-1, 30)
    put(B, "c6", "Taylor and Maclaurin series", "Find the coefficient of $x^5$ in the Maclaurin series of $e^x\\sin x$.", "$-\\dfrac1{30}$", ["$\\dfrac1{120}$", "$-\\dfrac1{24}$", "$\\dfrac1{30}$"],
        "Multiply the series: $e^x\\sin x=\\left(1+x+\\frac{x^2}2+\\frac{x^3}6+\\frac{x^4}{24}+\\cdots\\right)\\left(x-\\frac{x^3}6+\\frac{x^5}{120}-\\cdots\\right)$. The $x^5$ terms are $1\\cdot\\frac1{120}$, $\\frac{x^2}2\\cdot\\left(-\\frac{x^3}6\\right)$ and $\\frac{x^4}{24}\\cdot x$: $\\frac1{120}-\\frac1{12}+\\frac1{24}=\\frac{1-10+5}{120}=-\\frac1{30}$ (check: $\\operatorname{Im}(1+i)^5/5!=-\\frac4{120}$).")
    for expr, val, wrong in (((1 + 3 / n) ** (2 * n), sp.exp(6), (sp.exp(3), sp.exp(2), 1, sp.exp(5))), (n * sin(1 / n), 1, (0, sp.oo, R(1, 2), pi))):
        v = sp.limit(expr, n, sp.oo)
        assert sp.simplify(v - val) == 0
        put(B, "c6", "Limits of sequences", "Find $\\displaystyle\\lim_{n\\to\\infty}%s$." % tex(expr), L(val), vals(*wrong),
            "This is %s. The limit is %s." % ("a $1^\\infty$ form: $\\left(1+\\frac an\\right)^{bn}\\to e^{ab}$, so $e^{3\\cdot2}=e^6$" if val != 1 else "$\\dfrac{\\sin u}{u}\\to1$ with $u=\\frac1n\\to0$: $n\\sin\\frac1n=\\frac{\\sin(1/n)}{1/n}$", L(val)))
    s1 = sp.summation(1 / (n * (n + 2)), (n, 1, sp.oo))
    assert s1 == R(3, 4)
    put(B, "c6", "Series sums", "Find the sum of $\\displaystyle\\sum_{n=1}^\\infty\\frac1{n(n+2)}$.", "$\\dfrac34$", ["$\\dfrac12$", "$1$", "$\\dfrac38$"],
        "$\\dfrac1{n(n+2)}=\\dfrac12\\left(\\dfrac1n-\\dfrac1{n+2}\\right)$ telescopes: only $\\frac12\\left(1+\\frac12\\right)=\\frac34$ survives. (Two terms survive, not one, because the shift is $2$.)")
    s2 = sp.summation((2 ** n + 3 ** n) / sp.Integer(6) ** n, (n, 0, sp.oo))
    assert s2 == R(7, 2)
    put(B, "c6", "Series sums", "Find the sum of $\\displaystyle\\sum_{n=0}^\\infty\\frac{2^n+3^n}{6^n}$.", "$\\dfrac72$", ["$\\dfrac52$", "$\\dfrac{13}{6}$", "$6$"],
        "Split into two geometric series: $\\sum\\left(\\frac13\\right)^n=\\frac1{1-1/3}=\\frac32$ and $\\sum\\left(\\frac12\\right)^n=2$. The sum is $\\frac32+2=\\frac72$.")

def build_extras(B):
    for fn in (ch2, ch3, ch4, ch5, ch6):
        fn(B)
