# -*- coding: utf-8 -*-
"""Calculus I, extra questions from the final-exam tutoring slides (scanned; read from the page images) and from
Lectures 7, 8, 10b, 11 and 12 (symmetry, mean value theorem for integrals, monotone sequences, Taylor error).
Every answer is computed with sympy; every definite integral is also checked by numerical quadrature (mpmath)."""
import math
import mpmath as mp
import numpy as np
import sympy as sp
from qlib import tex
from cal_common import *

oo = sp.oo
mp.mp.dps = 30
S1 = "Final tutorial (session 1)"
S2 = "Final tutorial (session 2)"
y = sp.Symbol("y")

def numcheck(expr, a, b, val, var=x, tol=1e-9):
    """The exact value must agree with numerical quadrature of the integrand (endpoints may be +-oo)."""
    f = sp.lambdify(var, expr, "mpmath")
    end = lambda e: mp.inf if e == oo else (-mp.inf if e == -oo else mp.mpf(str(sp.N(e, 30))))
    q = mp.quad(f, [end(a), end(b)])
    assert abs(q - mp.mpf(str(sp.N(val, 30)))) < tol, (expr, q, sp.N(val))

def two_sig(v):
    """Decimal text of v rounded to 2 significant digits (for error-bound options)."""
    return "$" + np.format_float_positional(float("%.2g" % v), trim="-") + "$"

# ============================================================================== CHAPTER 2
def ch2(B):
    ch = "c2"
    F = x ** 2 + 2 * x * y + 3 * y ** 2 - 2
    assert sp.solve(F.subs(y, 1), x) == [-1]
    yp = sp.simplify(sp.idiff(F, y, x))
    assert sp.simplify(yp + (x + y) / (x + 3 * y)) == 0
    ypp = sp.simplify(sp.diff(yp, x) + sp.diff(yp, y) * yp)           # y'' by the chain rule (y' = yp)
    v1 = sp.simplify(yp.subs({x: -1, y: 1})); v2 = sp.simplify(ypp.subs({x: -1, y: 1}))
    assert v1 == 0 and v2 == sp.Rational(-1, 2), (v1, v2)
    eq = "$x^2+2xy+3y^2=2$"
    # the four candidate derivatives must be pairwise different functions of (x, y)
    cands = [-(x + y) / (x + 3 * y), (x + y) / (x + 3 * y), -(x + 4 * y) / x, -x / (x + 3 * y)]
    assert all(sp.simplify(cands[i] - cands[j]) != 0 for i in range(4) for j in range(i))
    B.mcq(ch, "Implicit differentiation", 2, "If %s, then $\\dfrac{dy}{dx}=$" % eq, "$-\\dfrac{x+y}{x+3y}$", ["$\\dfrac{x+y}{x+3y}$", "$-\\dfrac{x+4y}{x}$", "$-\\dfrac{x}{x+3y}$"],
          "Differentiate both sides in $x$ (product rule on $2xy$, chain rule on $3y^2$): $2x+2y+2xy'+6yy'=0\\Rightarrow y'=-\\dfrac{x+y}{x+3y}$. "
          "Typical slips: a wrong sign; forgetting $y'$ in $6yy'$, which gives $-\\frac{x+4y}{x}$; forgetting the $2y$ from the product rule, which gives $-\\frac{x}{x+3y}$.", S1 + ", implicit differentiation example", "src")
    mc_val(B, ch, "Implicit differentiation", 2, "If %s, find $y'$ at the point where $y=1$ (this forces $x=-1$)." % eq, v1, [-1, 1, sp.Rational(1, 2), -sp.Rational(1, 3)],
           "$y=1$ gives $x^2+2x+3=2$, i.e. $(x+1)^2=0$, so $x=-1$. Then $y'=-\\dfrac{x+y}{x+3y}=-\\dfrac{0}{2}=0$ (a horizontal tangent).", S1 + ", implicit differentiation example", "src")
    mc_val(B, ch, "Implicit differentiation", 3, "If %s, find $y''$ at the point $(-1,1)$, where $y'=0$." % eq, v2, [sp.Rational(1, 2), -1, sp.Rational(1, 4), 0],
           "Differentiate $y'=-\\dfrac{x+y}{x+3y}$ again: $y''=-\\dfrac{(1+y')(x+3y)-(x+y)(1+3y')}{(x+3y)^2}$. At $(-1,1)$ with $y'=0$: $-\\dfrac{1\\cdot2-0\\cdot1}{2^2}=-\\dfrac12$ (concave down there).", S1 + ", implicit differentiation example", "src")
    assert sp.sqrt(25 ** 2 - 7 ** 2) == 24
    mc_val(B, ch, "Related rates", 3, "The top of a $25$-ft ladder leaning against a vertical wall slips down at $1$ ft/s. How fast (in ft/s) is the bottom of the ladder moving away from the wall at the instant it is $7$ ft from the wall?",
           sp.Rational(24, 7), [-sp.Rational(24, 7), sp.Rational(7, 24), 1, sp.Rational(25, 7)],
           "$x^2+y^2=25^2\\Rightarrow x\\,x'+y\\,y'=0$, so $x'=-\\dfrac{y}{x}\\,y'$. When $x=7$: $y=\\sqrt{625-49}=24$, and $y'=-1$ (the top moves down), hence $x'=-\\dfrac{24}{7}\\cdot(-1)=\\dfrac{24}{7}\\approx3.43$ ft/s.", S1 + ", related-rates example", "src")

# ============================================================================== CHAPTER 3
def ch3(B):
    ch = "c3"
    xr = sp.Symbol("xr", positive=True)
    T = sp.sqrt(xr ** 2 + 36) / 4 + (7 - xr) / 6                  # time: row P -> landing point (4 mi/h), then run to B (6 mi/h)
    crit = sp.solve(sp.diff(T, xr), xr)
    assert len(crit) == 1 and sp.simplify(crit[0] - 12 * sp.sqrt(5) / 5) == 0
    xo = 12 * sp.sqrt(5) / 5
    tmin = sp.simplify(T.subs(xr, xo)); assert sp.simplify(tmin - (sp.Rational(7, 6) + sp.sqrt(5) / 2)) == 0
    t0, t7 = T.subs(xr, 0), T.subs(xr, 7)
    assert 0 < float(xo) < 7 and float(t0) > float(tmin) and float(t7) > float(tmin) and t0 == sp.Rational(8, 3) and sp.simplify(t7 - sp.sqrt(85) / 4) == 0
    setup = "A man in a rowboat is at a point $P$, $6$ miles from the nearest point $A$ of a straight shore. He wants to reach the point $B$ on the shore, $7$ miles from $A$, in the least time. He can row at $4$ mi/h and run along the shore at $6$ mi/h."
    mc_val(B, ch, "Optimization", 3, setup + " How far from $A$ should he land?", xo, [sp.Rational(12, 5), 7, sp.Rational(7, 2), 6 / sp.sqrt(5)],
           "Landing at distance $x$ from $A$ ($0\\le x\\le7$): $t(x)=\\dfrac{\\sqrt{x^2+36}}{4}+\\dfrac{7-x}{6}$. $t'(x)=\\dfrac{x}{4\\sqrt{x^2+36}}-\\dfrac16=0\\Rightarrow3x=2\\sqrt{x^2+36}\\Rightarrow5x^2=144\\Rightarrow x=\\dfrac{12}{\\sqrt5}\\approx5.37$ miles. "
           "The end points are worse: $t(0)=\\frac32+\\frac76\\approx2.67$ h and $t(7)=\\frac{\\sqrt{85}}{4}\\approx2.31$ h, while $t(12/\\sqrt5)\\approx2.28$ h.", S1 + ", optimization problem 2", "src")
    mc_val(B, ch, "Optimization", 3, setup + " What is the least possible time (in hours)?", tmin, [sp.sqrt(85) / 4, sp.Rational(8, 3), sp.Rational(7, 6), sp.Rational(7, 6) + sp.sqrt(5)],
           "At $x=\\dfrac{12}{\\sqrt5}$: $\\dfrac{\\sqrt{144/5+36}}{4}=\\dfrac{18/\\sqrt5}{4}=\\dfrac{9}{2\\sqrt5}$ and $\\dfrac{7-12/\\sqrt5}{6}=\\dfrac76-\\dfrac{2}{\\sqrt5}$, so $t_{\\min}=\\dfrac76+\\dfrac{5}{2\\sqrt5}=\\dfrac76+\\dfrac{\\sqrt5}{2}\\approx2.285$ h. "
           "(Rowing straight to $B$ takes $\\frac{\\sqrt{85}}4\\approx2.31$ h; landing at $A$ takes $\\frac83\\approx2.67$ h.)", S1 + ", optimization problem 2", "src")

# ============================================================================== CHAPTER 4
def ch4(B):
    ch = "c4"
    # --- integrals of even / odd functions (Lecture 8)
    EO = [("x^3+x^2", x ** 3 + x ** 2, -2, 2, "$x^3$ is odd (integral $0$) and $x^2$ is even: $2\\int_0^2x^2\\,dx=\\frac{16}{3}$."),
          ("x^4+x", x ** 4 + x, -1, 1, "$x$ is odd (integral $0$) and $x^4$ is even: $2\\int_0^1x^4\\,dx=\\frac25$."),
          ("x^2\\sin x", x ** 2 * sp.sin(x), -sp.pi / 2, sp.pi / 2, "$x^2\\sin x$ is (even)$\\times$(odd) = odd, so the integral over the symmetric interval is $0$ with no computation."),
          ("x\\cos x+3", x * sp.cos(x) + 3, -2, 2, "$x\\cos x$ is odd (integral $0$); the constant $3$ gives $3\\cdot4=12$.")]
    for lbl, f_, a_, b_, how in EO:
        val = sp.simplify(sp.integrate(f_, (x, a_, b_))); numcheck(f_, a_, b_, val)
        mc_val(B, ch, "Definite integrals", 2, "Evaluate $\\displaystyle\\int_{%s}^{%s}\\left(%s\\right)dx$ using symmetry." % (tex(a_), tex(b_), lbl), val,
               [2 * val if val != 0 else 1, -val if val != 0 else 2, val + 1, sp.Rational(1, 2) * val if val != 0 else -1],
               how + " Value: $%s$." % tex(val), "Lecture 8, integrals of symmetric functions", "src")
    B.mcq(ch, "Definite integrals", 2, "If $f$ is even and continuous on $[-a,a]$, then $\\displaystyle\\int_{-a}^af(x)\\,dx=$", "$2\\displaystyle\\int_0^af(x)\\,dx$",
          ["$\\displaystyle\\int_0^af(x)\\,dx$", "$0$", "$-2\\displaystyle\\int_0^af(x)\\,dx$"],
          "Even means the graph is symmetric about the $y$-axis, so the left half has the same signed area as the right half. For an odd $f$ the two halves cancel and the integral is $0$.", "Lecture 8, integrals of symmetric functions", "concept")
    # --- mean value theorem for integrals (Lecture 7)
    for f_, a_, b_ in [(x ** 2, sp.Integer(0), sp.Integer(3)), (x ** 3, sp.Integer(0), sp.Integer(2)), (sp.sqrt(x), sp.Integer(0), sp.Integer(4)), (1 / x, sp.Integer(1), sp.E)]:
        integral = sp.simplify(sp.integrate(f_, (x, a_, b_)))
        avg = sp.simplify(integral / (b_ - a_))
        cs = [c_ for c_ in sp.solve(sp.Eq(f_, avg), x) if c_.is_real and a_ < c_ < b_]; assert len(cs) == 1
        c0 = cs[0]
        assert abs(float(sp.N(f_.subs(x, c0) - avg))) < 1e-12 and a_ < c0 < b_
        mc_val(B, ch, "Average value", 3, "By the Mean Value Theorem for integrals there is a number $c\\in(%s,%s)$ with $f(c)=\\dfrac{1}{b-a}\\displaystyle\\int_a^bf(x)\\,dx$. Find $c$ for $f(x)=%s$." % (tex(a_), tex(b_), tex(f_)), c0,
               [avg, (a_ + b_) / 2, integral],        # typical slips: giving the average value itself, the mid-point, or the integral
               "$\\displaystyle\\int_{%s}^{%s}%s\\,dx=%s$, so the average value is $\\dfrac{1}{%s}\\cdot%s=%s$. Solve $f(c)=%s$ in $(%s,%s)$: $c=%s$." % (tex(a_), tex(b_), tex(f_), tex(integral), tex(b_ - a_), tex(integral), tex(avg), tex(avg), tex(a_), tex(b_), tex(c0)),
               "Lecture 7, Mean Value Theorem for integrals", "src")
    B.mcq(ch, "Definite integrals", 2, "If $m\\le f(x)\\le M$ for all $x\\in[a,b]$, then $\\displaystyle\\int_a^bf(x)\\,dx$ lies between", "$m(b-a)$ and $M(b-a)$",
          ["$m$ and $M$", "$\\dfrac{m}{b-a}$ and $\\dfrac{M}{b-a}$", "$m+(b-a)$ and $M+(b-a)$"],
          "Integrate $m\\le f\\le M$ over $[a,b]$ (comparison property). Example: $e^{-1}\\le e^{-x^2}\\le1$ on $[0,1]$ gives $0.36\\le\\int_0^1e^{-x^2}dx\\le1$.", "Lecture 7, properties of the definite integral", "concept")
    # --- areas, volumes, surface (tutoring session 2)
    ar1 = sp.integrate(1 - x ** 2, (x, 0, 1)); ar2 = sp.integrate(x ** 2 + 1 - x, (x, 0, 1)); assert ar1 == sp.Rational(2, 3) and ar2 == sp.Rational(5, 6)
    numcheck(1 - x ** 2, 0, 1, ar1); numcheck(x ** 2 + 1 - x, 0, 1, ar2)
    mc_val(B, ch, "Area between curves", 1, "Find the area between the graph of $f(x)=1-x^2$ and the $x$-axis for $0\\le x\\le1$.", ar1, [sp.Rational(1, 3), 1, sp.Rational(3, 2), sp.Rational(1, 2)],
           "$f\\ge0$ on $[0,1]$, so the area is $\\int_0^1(1-x^2)\\,dx=1-\\frac13=\\frac23$.", S2 + ", area example", "src")
    mc_val(B, ch, "Area between curves", 2, "Find the area of the region between $f(x)=x^2+1$ and $g(x)=x$ for $0\\le x\\le1$.", ar2, [sp.Rational(1, 6), sp.Rational(4, 3), sp.Rational(1, 2), sp.Rational(7, 6)],
           "Since $x^2+1-x=(x-\\frac12)^2+\\frac34>0$, $f$ lies above $g$ everywhere: $\\int_0^1(x^2+1-x)\\,dx=\\frac13+1-\\frac12=\\frac56$.", S2 + ", area between two curves", "src")
    v1 = sp.pi * sp.integrate(x ** 4, (x, 0, 10)); assert v1 == 20000 * sp.pi; numcheck(sp.pi * x ** 4, 0, 10, v1)
    mc_val(B, ch, "Volumes of revolution", 2, "The graph of $f(x)=x^2$, $0\\le x\\le10$, is rotated about the $x$-axis. Find the volume of the solid.", v1, [sp.pi * 1000 / 3, 20000, 100000 * sp.pi, 5000 * sp.pi],
           "Disks of radius $f(x)$: $V=\\pi\\displaystyle\\int_0^{10}x^4\\,dx=\\pi\\cdot\\dfrac{10^5}{5}=20\\,000\\pi$.", S2 + ", volume by cross-sections", "src")
    fsh = 9 * x / sp.sqrt(x ** 3 + 9)
    vsh = 36 * sp.pi; numcheck(2 * sp.pi * x * fsh, 0, 3, vsh)
    assert sp.simplify(sp.integrate(sp.simplify(2 * sp.pi * x * fsh), (x, 0, 3)) - vsh) == 0
    mc_val(B, ch, "Volumes of revolution", 3, "The region under $y=\\dfrac{9x}{\\sqrt{x^3+9}}$ for $0\\le x\\le3$ is rotated about the $y$-axis. Find the volume of the solid (cylindrical shells).", vsh, [18 * sp.pi, 72 * sp.pi, 27 * sp.pi * sp.log(4), 12 * sp.pi],
           "$V=2\\pi\\displaystyle\\int_0^3x\\cdot\\frac{9x}{\\sqrt{x^3+9}}\\,dx=18\\pi\\int_0^3\\frac{x^2}{\\sqrt{x^3+9}}\\,dx$. With $u=x^3+9$, $du=3x^2dx$, the limits become $9$ and $36$: $18\\pi\\cdot\\frac13\\cdot2\\left[\\sqrt u\\right]_9^{36}=12\\pi(6-3)=36\\pi$. "
           "(Using disks about the $x$-axis by mistake gives $27\\pi\\ln4$.)", S2 + ", shell method example", "src")
    sf = sp.pi * (10 * sp.sqrt(10) - 1) / 27; numcheck(2 * sp.pi * x ** 3 * sp.sqrt(1 + 9 * x ** 4), 0, 1, sf)
    mc_val(B, ch, "Arc length and surface area", 3, "Find the area of the surface obtained by rotating $f(x)=x^3$, $0\\le x\\le1$, about the $x$-axis.", sf,
           [sp.pi * (10 * sp.sqrt(10) + 1) / 27, 2 * sp.pi * (10 * sp.sqrt(10) - 1) / 27, sp.pi * (10 * sp.sqrt(10) - 1) / 9, (10 * sp.sqrt(10) - 1) / 27],
           "$S=2\\pi\\displaystyle\\int_0^1x^3\\sqrt{1+9x^4}\\,dx$. Let $u=1+9x^4$, $du=36x^3dx$: $S=\\dfrac{2\\pi}{36}\\displaystyle\\int_1^{10}\\sqrt u\\,du=\\dfrac{\\pi}{18}\\cdot\\dfrac23\\left(10^{3/2}-1\\right)=\\dfrac{\\pi(10\\sqrt{10}-1)}{27}\\approx3.56$.", S2 + ", surface area example", "src")

# ============================================================================== CHAPTER 5
def ch5(B):
    ch = "c5"
    v = sp.sqrt(2) - 1; numcheck(x / sp.sqrt(x ** 2 + 1), 0, 1, v)
    mc_val(B, ch, "Substitution", 2, "Evaluate $\\displaystyle\\int_0^1\\dfrac{x}{\\sqrt{x^2+1}}\\,dx$.", v, [sp.sqrt(2), 1 - sp.sqrt(2) / 2, sp.Rational(1, 2), sp.sqrt(2) + 1],
           "Let $u=x^2+1$, $du=2x\\,dx$ (limits $1$ and $2$): $\\frac12\\int_1^2u^{-1/2}du=\\left[\\sqrt u\\right]_1^2=\\sqrt2-1$.", S2 + ", substitution example", "src")
    v = sp.Rational(14, 3) * sp.log(2) - sp.Rational(16, 9); numcheck((x ** 2 + 1) * sp.log(x), 1, 2, v)
    assert sp.simplify(sp.integrate((x ** 2 + 1) * sp.log(x), (x, 1, 2)) - v) == 0
    mc_val(B, ch, "Integration by parts", 3, "Evaluate $\\displaystyle\\int_1^2(x^2+1)\\ln x\\,dx$.", v,
           [sp.Rational(14, 3) * sp.log(2) + sp.Rational(16, 9), sp.Rational(8, 3) * sp.log(2) - sp.Rational(16, 9), sp.Rational(14, 3) * sp.log(2), sp.Rational(14, 3) * sp.log(2) - sp.Rational(7, 9)],
           "Parts with $u=\\ln x$, $dv=(x^2+1)dx$, $v=\\frac{x^3}{3}+x$: $\\left[\\left(\\tfrac{x^3}{3}+x\\right)\\ln x\\right]_1^2-\\displaystyle\\int_1^2\\left(\\tfrac{x^2}{3}+1\\right)dx=\\tfrac{14}{3}\\ln2-\\left[\\tfrac{x^3}{9}+x\\right]_1^2=\\tfrac{14}{3}\\ln2-\\left(\\tfrac{26}{9}-\\tfrac{10}{9}\\right)=\\tfrac{14}{3}\\ln2-\\tfrac{16}{9}$.", S2 + ", integration by parts example", "src")
    v = sp.exp(2) + 1; numcheck(x * sp.exp(x), 0, 2, v)
    mc_val(B, ch, "Integration by parts", 2, "Evaluate $\\displaystyle\\int_0^2xe^x\\,dx$.", v, [sp.exp(2) - 1, 2 * sp.exp(2), sp.exp(2), 2 * sp.exp(2) + 1],
           "Parts with $u=x$, $dv=e^xdx$: $\\left[xe^x\\right]_0^2-\\displaystyle\\int_0^2e^xdx=2e^2-(e^2-1)=e^2+1$.", S2 + ", integration by parts example", "src")
    v = sp.Rational(8, 105); numcheck(sp.sin(x) ** 2 * sp.cos(x) ** 5, 0, sp.pi / 2, v)
    mc_val(B, ch, "Techniques of integration", 3, "Evaluate $\\displaystyle\\int_0^{\\pi/2}\\sin^2x\\cos^5x\\,dx$.", v, [sp.Rational(1, 7), sp.Rational(16, 105), sp.Rational(2, 15), sp.Rational(4, 35)],
           "The power of $\\cos$ is odd: save one $\\cos x$ for $du$, $u=\\sin x$, and write $\\cos^4x=(1-u^2)^2$. $\\displaystyle\\int_0^1u^2(1-u^2)^2du=\\int_0^1(u^2-2u^4+u^6)du=\\frac13-\\frac25+\\frac17=\\frac{8}{105}$.", S2 + ", powers of sine and cosine", "src")
    v = sp.integrate(sp.sin(3 * x) * sp.cos(5 * x), (x, 0, sp.pi / 2)); numcheck(sp.sin(3 * x) * sp.cos(5 * x), 0, sp.pi / 2, v)
    p8 = sp.integrate(sp.sin(8 * x), (x, 0, sp.pi / 2)); p2 = sp.integrate(sp.sin(2 * x), (x, 0, sp.pi / 2))
    assert (p8, p2) == (0, 1) and v == sp.Rational(1, 2) * (p8 - p2) == sp.Rational(-1, 2)
    mc_val(B, ch, "Techniques of integration", 3, "Evaluate $\\displaystyle\\int_0^{\\pi/2}\\sin3x\\cos5x\\,dx$.", v, [sp.Rational(1, 2), -sp.Rational(1, 4), sp.Rational(1, 4), 0],
           "Product-to-sum: $\\sin3x\\cos5x=\\frac12\\left[\\sin8x+\\sin(-2x)\\right]=\\frac12\\left[\\sin8x-\\sin2x\\right]$. "
           "$\\int_0^{\\pi/2}\\sin8x\\,dx=\\left[-\\frac{\\cos8x}{8}\\right]_0^{\\pi/2}=0$ and $\\int_0^{\\pi/2}\\sin2x\\,dx=\\left[-\\frac{\\cos2x}{2}\\right]_0^{\\pi/2}=1$. Hence $\\frac12(0-1)=-\\frac12$.", S2 + ", trigonometric integral", "src")
    Fpf = sp.atan(2 * x) - 1 / (4 * x ** 2 + 1)
    assert sp.simplify(sp.diff(Fpf, x) - (8 * x ** 2 + 8 * x + 2) / (4 * x ** 2 + 1) ** 2) == 0
    assert sp.simplify(2 / (4 * x ** 2 + 1) + 8 * x / (4 * x ** 2 + 1) ** 2 - (8 * x ** 2 + 8 * x + 2) / (4 * x ** 2 + 1) ** 2) == 0
    mc_expr(B, ch, "Partial fractions", 3, "Evaluate $\\displaystyle\\int\\dfrac{8x^2+8x+2}{(4x^2+1)^2}\\,dx$.", Fpf,
            [sp.atan(2 * x) + 1 / (4 * x ** 2 + 1), sp.atan(2 * x) / 2 - 1 / (4 * x ** 2 + 1), 2 * sp.atan(2 * x) - 1 / (4 * x ** 2 + 1), sp.atan(2 * x) - 1 / (2 * (4 * x ** 2 + 1))],
            "The factor $4x^2+1$ is irreducible and repeated: $\\frac{8x^2+8x+2}{(4x^2+1)^2}=\\frac{Ax+B}{4x^2+1}+\\frac{Cx+D}{(4x^2+1)^2}$. Matching coefficients gives $A=0,\\ B=2,\\ C=8,\\ D=0$ (indeed $8x^2+8x+2=2(4x^2+1)+8x$). "
            "Then $\\int\\frac{2\\,dx}{4x^2+1}=\\arctan2x$ and $\\int\\frac{8x\\,dx}{(4x^2+1)^2}=-\\frac{1}{4x^2+1}$.", S2 + ", partial fractions example", "src", x, wrap=lambda e: "$" + tex(e) + "+C$")
    v = sp.log(1 + sp.sqrt(2)); numcheck(1 / sp.sqrt(9 + x ** 2), 0, 3, v)
    mc_val(B, ch, "Trigonometric substitution", 3, "Evaluate $\\displaystyle\\int_0^3\\dfrac{dx}{\\sqrt{9+x^2}}$.", v, [sp.log(2), sp.pi / 4, sp.log(3), sp.log(1 + sp.sqrt(2)) / 3],
           "Let $x=3\\tan\\theta$, $dx=3\\sec^2\\theta\\,d\\theta$, $\\sqrt{9+x^2}=3\\sec\\theta$; $\\theta$ runs from $0$ to $\\frac\\pi4$. $\\displaystyle\\int_0^{\\pi/4}\\sec\\theta\\,d\\theta=\\ln\\left|\\sec\\theta+\\tan\\theta\\right|\\Big|_0^{\\pi/4}=\\ln(\\sqrt2+1)\\approx0.881$.", S2 + ", trigonometric substitution", "src")
    # --- improper integrals
    numcheck(x * sp.exp(x), -oo, 0, -1)
    mc_val(B, ch, "Improper integrals", 3, "Evaluate $\\displaystyle\\int_{-\\infty}^0xe^x\\,dx$.", -1, [1, 0, sp.oo, -sp.exp(1)],
           "$\\int_t^0xe^xdx=\\left[xe^x-e^x\\right]_t^0=-1-te^t+e^t$. As $t\\to-\\infty$, $te^t\\to0$ and $e^t\\to0$, so the integral converges to $-1$.", S2 + ", improper integral example", "src")
    left = sp.integrate(1 / sp.sqrt(-x), (x, -1, 0)); right = sp.integrate(1 / sp.sqrt(x), (x, 0, 4)); assert (left, right) == (2, 4)
    assert abs(mp.quad(lambda s: 1 / mp.sqrt(abs(s)), [-1, 0, 4]) - 6) < 1e-6
    mc_val(B, ch, "Improper integrals", 3, "Evaluate $\\displaystyle\\int_{-1}^4\\dfrac{dx}{\\sqrt{|x|}}$ (the integrand is unbounded at $x=0$).", 6, [4, 2, sp.oo, 8],
           "Split at the singular point $0$: $\\int_{-1}^0\\frac{dx}{\\sqrt{-x}}=2$ and $\\int_0^4\\frac{dx}{\\sqrt{x}}=2\\sqrt4=4$. Both converge, so the total is $6$.", S2 + ", improper integral with a singularity", "src")
    f_cmp = lambda t: mp.sin(t) ** 2 / t ** 2
    assert abs(mp.quad(f_cmp, mp.linspace(1, 400, 400)) - mp.quad(f_cmp, mp.linspace(1, 800, 800))) < 3e-3     # the tail beyond 400 is below 1/400
    B.mcq(ch, "Improper integrals", 3, "Does $\\displaystyle\\int_1^{\\infty}\\dfrac{\\sin^2x}{x^2}\\,dx$ converge?",
          "Yes: $0\\le\\dfrac{\\sin^2x}{x^2}\\le\\dfrac1{x^2}$ and $\\displaystyle\\int_1^\\infty\\dfrac{dx}{x^2}$ converges",
          ["No: $\\sin^2x$ oscillates, so the limit defining the integral cannot exist", "No: the integrand is positive, so the area under it is infinite", "Yes: $\\sin^2x\\to0$ as $x\\to\\infty$, so the integral converges"],
          "Direct comparison: the integrand lies between $0$ and $\\frac{1}{x^2}$, and $\\int_1^\\infty x^{-2}dx=1$. The last option uses a false reason ($\\sin^2x$ does not tend to $0$, and a vanishing integrand alone would not prove convergence anyway). "
          "A positive integrand has an increasing area function, which converges when it is bounded.", S2 + ", comparison test for integrals", "src")

# ============================================================================== CHAPTER 6
def ch6(B):
    ch = "c6"
    S = sp.summation(2 * sp.Integer(3) ** (n_ + 1) / sp.Integer(5) ** n_, (n_, 0, oo)); assert S == 15
    mc_val(B, ch, "Series sums", 2, "Show that $\\displaystyle\\sum_{n=0}^\\infty\\dfrac{2\\cdot3^{n+1}}{5^n}$ converges and find its sum.", S, [sp.Rational(6, 5), 10, sp.Rational(15, 2), 30],
           "Geometric series: $\\frac{2\\cdot3^{n+1}}{5^n}=6\\left(\\frac35\\right)^n$ with first term $6$ and ratio $r=\\frac35$, $|r|<1$. The sum is $\\dfrac{6}{1-\\frac35}=15$.", S2 + ", geometric series", "src")
    S = sp.summation(n_ / sp.Integer(2) ** n_, (n_, 1, oo)); assert S == 2
    mc_val(B, ch, "Series sums", 3, "Differentiating $\\dfrac{1}{1-x}=\\sum_{n\\ge0}x^n$ gives $\\dfrac{1}{(1-x)^2}=\\sum_{n\\ge1}nx^{n-1}$ for $|x|<1$. Use this to find $\\displaystyle\\sum_{n=1}^\\infty\\dfrac{n}{2^n}$.", S, [1, 4, sp.Rational(1, 2), sp.Rational(3, 2)],
           "Multiply by $x$: $\\sum_{n\\ge1}nx^n=\\dfrac{x}{(1-x)^2}$. At $x=\\frac12$: $\\dfrac{1/2}{(1/2)^2}=2$. (Forgetting the factor $x$ gives $\\sum nx^{n-1}=4$.)", S2 + ", differentiating a geometric series", "src")
    an = lambda m: (10 * m * m - 3 * m - 1) / (m ** 4 + m * m + 1)
    assert all(an(m) > 0 and an(m) <= 10 / m ** 2 for m in range(1, 5000))
    B.mcq(ch, "Convergence tests", 2, "Which argument shows that $\\displaystyle\\sum_{n=1}^\\infty\\dfrac{10n^2-3n-1}{n^4+n^2+1}$ converges?",
          "$0<\\dfrac{10n^2-3n-1}{n^4+n^2+1}\\le\\dfrac{10}{n^2}$, and $\\sum\\dfrac{10}{n^2}$ converges",
          ["$\\dfrac{10n^2-3n-1}{n^4+n^2+1}\\ge\\dfrac{1}{n^2}$, and $\\sum\\dfrac1{n^2}$ converges", "its terms tend to $0$, and every series whose terms tend to $0$ converges", "the ratio $a_{n+1}/a_n$ tends to $1$, so the Ratio Test proves convergence"],
          "The numerator is positive and at most $10n^2$, the denominator is at least $n^4$, so the Direct Comparison Test with the $p$-series ($p=2$) applies. Being larger than a convergent series proves nothing; $a_n\\to0$ is only necessary; a ratio limit equal to $1$ is inconclusive.", S2 + ", direct comparison example", "src")
    bn = lambda m: m * (1 - math.exp(-m)) / (m ** 3 + 3)
    assert all(0 <= bn(m) <= 1 / m ** 2 for m in range(5, 3000))
    B.mcq(ch, "Convergence tests", 3, "Does $\\displaystyle\\sum_{n=5}^\\infty\\dfrac{n\\left(1-e^{-n}\\right)}{n^3+3}$ converge? Choose the valid justification.",
          "Yes: $0\\le\\dfrac{n(1-e^{-n})}{n^3+3}\\le\\dfrac{1}{n^2}$, and $\\sum\\dfrac1{n^2}$ converges",
          ["No: the terms behave like $\\dfrac1n$ because $1-e^{-n}\\to1$, so it diverges like the harmonic series", "No: the terms do not tend to $0$, so the series diverges", "Yes: the Ratio Test gives a limit smaller than $1$, so it converges"],
          "$n(1-e^{-n})<n$ and $n^3+3>n^3$, hence the term is below $\\frac{n}{n^3}=\\frac1{n^2}$ (the terms behave like $\\frac{1}{n^2}$, not $\\frac1n$, and they do tend to $0$). The Ratio Test cannot be used here: the ratio tends to $1$.", S2 + ", comparison test", "src")
    B.mcq(ch, "Power series", 2, "Find the radius and the interval of convergence of $\\displaystyle\\sum_{n=1}^\\infty n(x-2)^n$.", "$R=1$, interval $(1,3)$",
          ["$R=1$, interval $[1,3]$", "$R=1$, interval $[1,3)$", "$R=2$, interval $(0,4)$"],
          "Ratio Test: $\\dfrac{(n+1)|x-2|^{n+1}}{n|x-2|^{n}}\\to|x-2|$, so the series converges for $|x-2|<1$, i.e. $R=1$ and $1<x<3$. At $x=1$ the series is $\\sum n(-1)^n$ and at $x=3$ it is $\\sum n$: the terms do not tend to $0$, so both end points diverge.", S2 + ", interval of convergence", "src")
    lnser = sp.series(sp.log(1 + x), x, 0, 6).removeO()
    assert sp.expand(lnser - (x - x ** 2 / 2 + x ** 3 / 3 - x ** 4 / 4 + x ** 5 / 5)) == 0
    B.mcq(ch, "Taylor and Maclaurin series", 3, "Integrating $\\dfrac1{1+x}=\\sum_{n\\ge0}(-1)^nx^n$ term by term from $0$ to $x$ gives the series of $\\ln(1+x)$, which is",
          "$\\displaystyle\\sum_{n=1}^\\infty\\dfrac{(-1)^{n+1}x^n}{n}=x-\\dfrac{x^2}{2}+\\dfrac{x^3}{3}-\\cdots$",
          ["$\\displaystyle\\sum_{n=1}^\\infty\\dfrac{(-1)^{n}x^n}{n}=-x+\\dfrac{x^2}{2}-\\cdots$", "$\\displaystyle\\sum_{n=0}^\\infty(-1)^{n}x^{n+1}=x-x^2+x^3-\\cdots$", "$\\displaystyle\\sum_{n=1}^\\infty\\dfrac{x^n}{n!}=x+\\dfrac{x^2}{2}+\\dfrac{x^3}{6}+\\cdots$"],
          "$\\int_0^x(-1)^nt^n\\,dt=\\dfrac{(-1)^nx^{n+1}}{n+1}$; re-indexing $n+1\\to n$ gives $\\sum_{n\\ge1}\\frac{(-1)^{n-1}x^n}{n}$, valid for $-1<x\\le1$ (at $x=1$: $\\ln2=1-\\frac12+\\frac13-\\cdots$).", S2 + ", integrating a power series", "src")
    # --- Taylor remainder (Lecture 12)
    T4 = sum(sp.Rational(1, 2) ** k / sp.factorial(k) for k in range(5)); assert abs(float(T4) - 1.6484375) < 1e-12
    true_err = math.exp(0.5) - float(T4)
    b_ok = 2 * 0.5 ** 5 / math.factorial(5)
    assert 0 < true_err < b_ok < 5.3e-4
    B.mcq(ch, "Taylor and Maclaurin series", 3, "Taylor's inequality for $T_4(x)=1+x+\\frac{x^2}{2!}+\\frac{x^3}{3!}+\\frac{x^4}{4!}$ of $e^x$, with $M=2$ (because $e^c<2$ for $c\\le0.5$), gives $|R_4(0.5)|\\le$",
          two_sig(b_ok), [two_sig(0.5 ** 5 / math.factorial(5)), two_sig(2 * 0.5 ** 5 / math.factorial(4)), two_sig(2 * 0.5 ** 4 / math.factorial(4))],
          "$|R_4(x)|\\le\\dfrac{M|x|^5}{5!}=\\dfrac{2\\cdot0.5^5}{120}\\approx0.00052$. (Without $M$ you would get $0.00026$; using $4!$ instead of $5!$ gives $0.0026$; using the degree $4$ instead of $n+1=5$ gives $0.0052$.) "
          "The actual error is $e^{0.5}-1.6484375\\approx0.00028$, below the bound.", "Lecture 12, Taylor's inequality", "src")
    nmin = next(m for m in range(1, 30) if 3 / math.factorial(m + 1) < 1e-5)
    assert nmin == 8 and 3 / math.factorial(8) > 1e-5 > 3 / math.factorial(9)
    B.mcq(ch, "Taylor and Maclaurin series", 3, "For $e$, Taylor's inequality gives $|R_n(1)|\\le\\dfrac{3}{(n+1)!}$ (because $e^c<e<3$ for $0<c<1$). What is the smallest $n$ for which this bound guarantees $|R_n(1)|<10^{-5}$?",
          "$n=%d$" % nmin, ["$n=%d$" % (nmin - 1), "$n=%d$" % (nmin + 1), "$n=%d$" % (nmin + 2)],
          "$\\frac{3}{8!}\\approx7.4\\times10^{-5}$ is still larger than $10^{-5}$ (so the bound does not yet guarantee it for $n=7$), while $\\frac{3}{9!}\\approx8.3\\times10^{-6}<10^{-5}$ with $n+1=9$, i.e. $n=8$.", "Lecture 12, Taylor's inequality", "src")
    # --- sequences (Lectures 10b and 11)
    B.mcq(ch, "Limits of sequences", 2, "A sequence that is both bounded and monotone (increasing or decreasing)",
          "converges (Monotone Convergence Theorem)", ["converges only when it is decreasing", "converges only when it is constant from some term on", "converges to its first term"],
          "A bounded increasing sequence converges to its supremum, and a bounded decreasing one to its infimum. Example: $a_1=\\sqrt2$, $a_{n+1}=\\sqrt{2+a_n}$ is increasing and bounded by $2$, so it converges, and $L=\\sqrt{2+L}$ gives $L=2$.", "Lecture 11, monotone and bounded sequences", "concept")
    B.mcq(ch, "Limits of sequences", 2, "If $a_n\\to L$, then every subsequence of $(a_n)$", "also converges to $L$",
          ["converges to $a_1$, the first term", "is bounded but need not converge", "may converge to a different limit $L'$"],
          "Consequently, two subsequences with different limits prove divergence: $(-1)^n$ has the subsequences $1,1,1,\\dots$ and $-1,-1,-1,\\dots$.", "Lecture 10b, subsequences", "concept")
    B.mcq(ch, "Limits of sequences", 2, "To compute $\\displaystyle\\lim_{n\\to\\infty}\\dfrac{\\ln n}{n}$ with L'Hôpital's rule one first replaces $n$ by a real variable $x$, because",
          "if $f(x)\\to L$ as $x\\to\\infty$ and $a_n=f(n)$, then $a_n\\to L$", ["a sequence is a differentiable function of $n$", "L'Hôpital's rule applies directly to every sequence", "$\\ln n$ is a polynomial in $n$"],
          "$\\lim_{x\\to\\infty}\\frac{\\ln x}{x}=\\lim_{x\\to\\infty}\\frac{1/x}{1}=0$, hence $\\frac{\\ln n}{n}\\to0$. The converse is false: $\\sin(\\pi n)=0\\to0$ but $\\lim_{x\\to\\infty}\\sin(\\pi x)$ does not exist.", "Lecture 11, sequences and functions", "concept")
    B.mcq(ch, "Limits of sequences", 2, "If $f$ is continuous and $a_n\\to L$ (with $a_n$ and $L$ in the domain of $f$), then $\\displaystyle\\lim_{n\\to\\infty}f(a_n)=$", "$f(L)$", ["$L$", "$f'(L)$", "$f(a_1)$"],
          "A continuous function commutes with limits. Examples: $\\cos\\frac1n\\to\\cos0=1$ and $e^{1/n}\\to e^0=1$.", "Lecture 10b, limit laws for sequences", "concept")
