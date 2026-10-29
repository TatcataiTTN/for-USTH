# -*- coding: utf-8 -*-
"""Calculus I chapters 5-6: techniques of integration, improper integrals, sequences and series."""
import math
import numpy as np
import sympy as sp
from qlib import tex, uniq_by_text, near_numbers, R, note
from cal_common import *
from gen_cal1 import limq

oo = sp.oo
C = sp.Symbol("C")
z_, r_, v_, s_ = sp.symbols("z r v s", positive=True)

def ant_q(B, ch, level, lbl, integrand, ans, wrongs, how, src, var=x, origin="src", topic="Techniques of integration", pts=(0.4, 0.9, 1.6, 2.3)):
    """Antiderivative question: asserts d(ans)/dvar == integrand before adding the question."""
    assert num_equal(sp.diff(ans, var), integrand, var, pts=list(pts)), (src, sp.simplify(sp.diff(ans, var) - integrand))
    mc_expr(B, ch, topic, level, "Evaluate $\\displaystyle\\int %s$." % lbl, ans, list(wrongs), how + " Check: differentiating gives the integrand. Answer: $%s+C$." % tex(ans), src, origin, var,
            wrap=lambda e: "$" + tex(e) + "+C$")

def def_q(B, ch, level, lbl, expr, lo, hi, val, extras, how, src, origin="src", var=x, topic="Definite integrals"):
    got = sp.integrate(expr, (var, lo, hi))
    if got.has(sp.Integral):      # CAS could not close the form: verify numerically instead
        assert abs(float(sp.N(sp.Integral(expr, (var, lo, hi)))) - float(sp.N(val))) < 1e-8, (src, val)
    else:
        assert sp.simplify(got - val) == 0, (src, got, val)
    hi_t = tex(hi) if hi != oo else "\\infty"
    mc_val(B, ch, topic, level, "Evaluate $\\displaystyle\\int_{%s}^{%s}%s$." % (tex(lo), hi_t, lbl), val, extras, how + " Value: $%s$." % tex(val), src, origin)

# numeric heuristics for series (used only to double-check a claimed behaviour)
def partial_sums(f, N1=10 ** 5, N2=10 ** 6, start=1):
    n1 = np.arange(start, N1 + 1, dtype=np.float64); n2 = np.arange(start, N2 + 1, dtype=np.float64)
    a1 = f(n1); a2 = f(n2)
    return float(np.nansum(a1)), float(np.nansum(a2)), a2[-1]

def series_behaves(f, expect, start=1):
    S1, S2, last = partial_sums(f, start=start)
    if expect == "conv":
        assert abs(S2 - S1) < 0.05 * max(1.0, abs(S1)), (S1, S2)
    else:
        assert abs(S2 - S1) > 0.05 * max(1.0, abs(S1)) or abs(last) > 1e-6, (S1, S2, last)

def seq_limit(an, n, expect, lbl=""):
    """Limit of a sequence: sympy first; if the CAS fails, verify numerically with 50-digit arithmetic."""
    import mpmath as mp
    try:
        val = sp.limit(an, n, oo)
        assert sp.simplify(val - expect) == 0 or val == expect, (lbl, val, expect)
        return val
    except (NotImplementedError, TypeError, ValueError):
        mp.mp.dps = 60
        f = sp.lambdify(n, an, "mpmath")
        v1, v2 = f(mp.mpf(3000)), f(mp.mpf(6000))
        if expect == oo:
            assert v2 > v1 > 10 ** 6, (lbl, v1, v2)
        else:
            assert abs(v2 - mp.mpf(float(sp.N(expect)))) < 1e-6, (lbl, v2, expect)
        return expect

# ============================================================================== CHAPTER 5
def ch5(B):
    ch = "c5"; rng = B.rng
    # ---- Tutorial 9 / Computation 9 : basic formulas, substitution
    def_q(B, ch, 2, "\\dfrac{16x}{8x^2+2}\\,dx", 16 * x / (8 * x ** 2 + 2), 0, 1, sp.log(5), [sp.log(2), sp.log(5) / 2, 2 * sp.log(5), sp.log(10)], "$u=8x^2+2$, $du=16x\\,dx$: $[\\ln u]_2^{10}=\\ln10-\\ln2=\\ln5$.", "Tutorial 9, Q1(a)", var=x)
    cot = lambda e: sp.cos(e) / sp.sin(e)
    ant_q(B, ch, 3, "\\dfrac{e^{-\\cot z}}{\\sin^2z}\\,dz", sp.exp(-cot(z_)) / sp.sin(z_) ** 2, sp.exp(-cot(z_)), [-sp.exp(-cot(z_)), sp.exp(-cot(z_)) / sp.sin(z_) ** 2, sp.exp(cot(z_)), sp.exp(-cot(z_)) * sp.cos(z_)], "$u=-\\cot z$, $du=\\csc^2z\\,dz$: $\\int e^u\\,du=e^u$.", "Tutorial 9, Q1(b)", var=z_, pts=(0.7, 1.1, 1.9))
    ant_q(B, ch, 3, "\\dfrac{d\\theta}{\\sqrt{2\\theta-\\theta^2}}", 1 / sp.sqrt(2 * th - th ** 2), sp.asin(th - 1), [sp.asin(th), sp.acos(th - 1), sp.atan(th - 1), sp.asin(th - 1) / 2], "Complete the square: $2\\theta-\\theta^2=1-(\\theta-1)^2$; with $u=\\theta-1$ the integral is $\\arcsin u$.", "Tutorial 9, Q1(c)", var=th, pts=(0.4, 0.8, 1.3, 1.7))
    ant_q(B, ch, 3, "\\dfrac{2\\,dx}{x\\sqrt{1-4\\ln^2x}}", 2 / (x * sp.sqrt(1 - 4 * sp.log(x) ** 2)), sp.asin(2 * sp.log(x)), [sp.asin(sp.log(x)), sp.acos(2 * sp.log(x)), sp.asin(2 * sp.log(x)) / 2, 2 * sp.asin(2 * sp.log(x))], "$u=2\\ln x$, $du=\\frac{2}{x}dx$: $\\int\\frac{du}{\\sqrt{1-u^2}}=\\arcsin u$.", "Tutorial 9, Q1(d)", pts=(0.8, 1.1, 1.4))
    ant_q(B, ch, 3, "e^{z+e^{z}}\\,dz", sp.exp(z_ + sp.exp(z_)), sp.exp(sp.exp(z_)), [sp.exp(z_ + sp.exp(z_)), sp.exp(sp.exp(z_)) * z_, sp.exp(z_) * sp.exp(sp.exp(z_)) / 2, sp.exp(sp.exp(z_)) / 2], "$u=e^z$, $du=e^zdz$: $e^{z+e^z}dz=e^u\\,du$, so the antiderivative is $e^{u}=e^{e^z}$.", "Tutorial 9, Q1(e)", var=z_, pts=(0.3, 0.6, 1.0))
    # ---- integration by parts
    ant_q(B, ch, 2, "(r^2+r+1)e^{r}\\,dr", (r_ ** 2 + r_ + 1) * sp.exp(r_), sp.exp(r_) * (r_ ** 2 - r_ + 2), [sp.exp(r_) * (r_ ** 2 + r_ + 1), sp.exp(r_) * (r_ ** 2 + 3 * r_ + 4), sp.exp(r_) * (r_ ** 2 - 3 * r_ + 2), sp.exp(r_) * (r_ ** 3 / 3 + r_ ** 2 / 2 + r_)], "Parts twice with $u=$ the polynomial: $e^r(P-P'+P'')$ with $P=r^2+r+1$: $e^r\\left(r^2+r+1-(2r+1)+2\\right)$.", "Tutorial 9, Q3(a)", var=r_, pts=(0.3, 0.9, 1.7))
    th_ = th
    ant_q(B, ch, 3, "e^{\\theta}\\sin\\theta\\,d\\theta", sp.exp(th_) * sp.sin(th_), sp.exp(th_) * (sp.sin(th_) - sp.cos(th_)) / 2, [sp.exp(th_) * (sp.sin(th_) + sp.cos(th_)) / 2, sp.exp(th_) * (sp.sin(th_) - sp.cos(th_)), sp.exp(th_) * sp.sin(th_) / 2, -sp.exp(th_) * sp.cos(th_)], "Parts twice returns the original integral: $I=e^\\theta(\\sin\\theta-\\cos\\theta)-I$, so $I=\\frac12e^\\theta(\\sin\\theta-\\cos\\theta)$.", "Tutorial 9, Q3(b)", var=th_, pts=(0.4, 1.0, 1.7))
    ant_q(B, ch, 2, "\\dfrac{e^{\\sqrt x}}{\\sqrt x}\\,dx", sp.exp(sp.sqrt(x)) / sp.sqrt(x), 2 * sp.exp(sp.sqrt(x)), [sp.exp(sp.sqrt(x)), sp.exp(sp.sqrt(x)) / 2, 2 * sp.exp(sp.sqrt(x)) * sp.sqrt(x), 2 * sp.exp(x)], "No parts needed: $u=\\sqrt x$, $du=\\frac{dx}{2\\sqrt x}$ gives $2\\int e^udu$.", "Tutorial 9, Q4(a)")
    val4 = sp.integrate(x ** 3 * sp.cos(2 * x), (x, 0, sp.pi / 2))
    mc_val(B, ch, "Integration by parts", 3, "$\\displaystyle\\int_0^{\\pi/2}x^3\\cos2x\\,dx=$", val4, [-val4, val4 + 1, val4 * 2, sp.Rational(3, 4) - sp.pi ** 2 / 8],
           "Integrate by parts three times (tabular method): $x^3\\cdot\\frac{\\sin2x}2+3x^2\\frac{\\cos2x}{4}-6x\\frac{\\sin2x}{8}-6\\frac{\\cos2x}{16}$ evaluated from $0$ to $\\frac\\pi2$; the value is $%s\\approx%.4f$." % (tex(sp.simplify(val4)), float(val4)), "Tutorial 9, Q4(b)", "src")
    for lbl, f_, F_, wr, how, src in [
        ("x\\cos x\\,dx", x * sp.cos(x), x * sp.sin(x) + sp.cos(x), [x * sp.sin(x) - sp.cos(x), x ** 2 * sp.sin(x) / 2, sp.sin(x) + x * sp.cos(x), -x * sp.sin(x) + sp.cos(x)], "Parts: $u=x$, $dv=\\cos x\\,dx$: $x\\sin x-\\int\\sin x\\,dx$.", "Computation problems 9, Q5"),
        ("x^2e^{x}\\,dx", x ** 2 * sp.exp(x), (x ** 2 - 2 * x + 2) * sp.exp(x), [(x ** 2 + 2 * x + 2) * sp.exp(x), (x ** 2 - 2 * x) * sp.exp(x), x ** 3 * sp.exp(x) / 3, (x ** 2 - 2 * x + 1) * sp.exp(x)], "Parts twice (or $e^x(P-P'+P'')$ with $P=x^2$).", "Computation problems 9, Q6"),
        ("e^{x}\\cos x\\,dx", sp.exp(x) * sp.cos(x), sp.exp(x) * (sp.sin(x) + sp.cos(x)) / 2, [sp.exp(x) * (sp.sin(x) - sp.cos(x)) / 2, sp.exp(x) * (sp.sin(x) + sp.cos(x)), sp.exp(x) * sp.sin(x) / 2, sp.exp(x) * sp.cos(x) / 2], "Parts twice and solve for the integral: $I=e^x(\\cos x+\\sin x)-I$.", "Computation problems 9, Q7"),
        ("\\cos^5x\\,dx", sp.cos(x) ** 5, sp.sin(x) - 2 * sp.sin(x) ** 3 / 3 + sp.sin(x) ** 5 / 5, [sp.sin(x) + 2 * sp.sin(x) ** 3 / 3 + sp.sin(x) ** 5 / 5, sp.sin(x) - sp.sin(x) ** 3 / 3 + sp.sin(x) ** 5 / 5, sp.cos(x) ** 6 / 6, sp.sin(x) - 2 * sp.sin(x) ** 3 + sp.sin(x) ** 5], "Odd power: save one $\\cos x$, write $\\cos^4x=(1-\\sin^2x)^2$, put $u=\\sin x$: $\\int(1-2u^2+u^4)du$.", "Computation problems 9, Q8"),
        ("\\tan^4x\\,dx", sp.tan(x) ** 4, sp.tan(x) ** 3 / 3 - sp.tan(x) + x, [sp.tan(x) ** 3 / 3 + sp.tan(x) + x, sp.tan(x) ** 5 / 5, sp.tan(x) ** 3 / 3 - sp.tan(x) - x, sp.sec(x) ** 4 / 4], "$\\tan^4x=\\tan^2x(\\sec^2x-1)=\\tan^2x\\sec^2x-\\sec^2x+1$.", "Computation problems 9, Q10"),
        ("\\dfrac{x^2}{x^2+1}\\,dx", x ** 2 / (x ** 2 + 1), x - sp.atan(x), [x + sp.atan(x), x ** 3 / (3 * x), sp.atan(x), x - sp.log(x ** 2 + 1)], "$\\frac{x^2}{x^2+1}=1-\\frac{1}{x^2+1}$.", "Computation problems 9, Q1"),
        ("\\dfrac{dx}{x-\\sqrt x}", 1 / (x - sp.sqrt(x)), 2 * sp.log(sp.sqrt(x) - 1), [sp.log(x - sp.sqrt(x)), 2 * sp.log(sp.sqrt(x)), sp.log(sp.sqrt(x) - 1), 2 * sp.log(sp.sqrt(x) + 1)], "$u=\\sqrt x$, $dx=2u\\,du$: $\\int\\frac{2u\\,du}{u^2-u}=2\\int\\frac{du}{u-1}=2\\ln|u-1|$ (for $x>1$).", "Computation problems 9, Q3"),
        ("\\dfrac{2^{\\ln z^3}}{16z}\\,dz", 2 ** sp.log(z_ ** 3) / (16 * z_), 2 ** sp.log(z_ ** 3) / (48 * sp.log(2)), [2 ** sp.log(z_ ** 3) / (16 * sp.log(2)), 2 ** sp.log(z_ ** 3) / 48, 2 ** sp.log(z_ ** 3) * sp.log(2) / 48, 2 ** sp.log(z_ ** 3) / (16 * z_)], "$2^{\\ln z^3}=e^{3\\ln2\\cdot\\ln z}$; with $u=\\ln z$, $du=\\frac{dz}z$: $\\frac1{16}\\int2^{3u}du=\\frac{2^{3u}}{16\\cdot3\\ln2}$.", "Computation problems 9, Q4")]:
        vv = z_ if "dz" in lbl else x
        ant_q(B, ch, 2 if "cos^5" not in lbl else 3, lbl, f_.subs(x, vv) if vv != x else f_, F_.subs(x, vv) if vv != x else F_, [w.subs(x, vv) if vv != x else w for w in wr], how, src, var=vv, pts=(1.3, 1.7, 2.4, 3.1))
    def_q(B, ch, 3, "\\dfrac{dx}{\\cos^2x\\tan x}", 1 / (sp.cos(x) ** 2 * sp.tan(x)), sp.pi / 4, sp.pi / 3, sp.log(3) / 2, [sp.log(3), sp.log(2), sp.sqrt(3) - 1, sp.log(sp.sqrt(2))], "$u=\\tan x$, $du=\\sec^2x\\,dx$: $\\int\\frac{du}{u}=\\ln u$; $\\ln\\tan\\frac\\pi3-\\ln\\tan\\frac\\pi4=\\ln\\sqrt3=\\frac12\\ln3$.", "Computation problems 9, Q2")
    def_q(B, ch, 3, "\\sqrt{1+\\cos4x}\\,dx", sp.sqrt(1 + sp.cos(4 * x)), 0, sp.pi / 4, sp.sqrt(2) / 2, [sp.sqrt(2), sp.Rational(1, 2), sp.pi / 4, sp.sqrt(2) / 4], "$1+\\cos4x=2\\cos^22x$, so $\\sqrt{\\cdot}=\\sqrt2\\cos2x$ on $[0,\\frac\\pi4]$: $\\sqrt2\\left[\\frac{\\sin2x}{2}\\right]_0^{\\pi/4}=\\frac{\\sqrt2}{2}$.", "Computation problems 9, Q9")
    ant_q(B, ch, 2, "8\\cos^3 2\\theta\\sin2\\theta\\,d\\theta", 8 * sp.cos(2 * th) ** 3 * sp.sin(2 * th), -sp.cos(2 * th) ** 4, [sp.cos(2 * th) ** 4, -sp.cos(2 * th) ** 4 / 2, sp.cos(2 * th) ** 4 / 4, -sp.sin(2 * th) ** 4], "$u=\\cos2\\theta$, $du=-2\\sin2\\theta\\,d\\theta$: $-4\\int u^3du=-u^4$.", "Tutorial 9, Q6", var=th, pts=(0.3, 0.7, 1.2))
    def_q(B, ch, 2, "\\sqrt{1-\\cos^2\\theta}\\,d\\theta", sp.sqrt(1 - sp.cos(x) ** 2), 0, sp.pi, 2, [0, sp.pi, 4, 1], "$\\sqrt{1-\\cos^2\\theta}=|\\sin\\theta|=\\sin\\theta$ on $[0,\\pi]$: $[-\\cos\\theta]_0^\\pi=2$ (a common slip is to write $\\sqrt{\\sin^2\\theta}=\\sin\\theta$ on intervals where $\\sin<0$).", "Tutorial 9, Q7")
    ant_q(B, ch, 2, "\\sec^2x\\tan^2x\\,dx", sp.sec(x) ** 2 * sp.tan(x) ** 2, sp.tan(x) ** 3 / 3, [sp.tan(x) ** 3, sp.sec(x) ** 3 / 3, sp.tan(x) ** 3 / 6, sp.sec(x) ** 2 * sp.tan(x) ** 3 / 3], "$u=\\tan x$, $du=\\sec^2x\\,dx$: $\\int u^2du$.", "Tutorial 9, Q8", pts=(0.3, 0.7, 1.1))
    ant_q(B, ch, 3, "\\cos3x\\cos4x\\,dx", sp.cos(3 * x) * sp.cos(4 * x), sp.sin(x) / 2 + sp.sin(7 * x) / 14, [sp.sin(x) / 2 - sp.sin(7 * x) / 14, sp.sin(x) + sp.sin(7 * x), sp.sin(3 * x) * sp.sin(4 * x) / 12, sp.sin(x) / 2 + sp.sin(7 * x) / 7], "Product-to-sum: $\\cos3x\\cos4x=\\frac12[\\cos x+\\cos7x]$.", "Tutorial 9, Q9", pts=(0.3, 0.7, 1.1))
    ant_q(B, ch, 3, "\\dfrac{\\sec^3x}{\\tan x}\\,dx", sp.sec(x) ** 3 / sp.tan(x), sp.sec(x) - sp.log(sp.csc(x) + sp.cot(x)), [sp.sec(x) + sp.log(sp.csc(x) + sp.cot(x)), sp.sec(x), sp.sec(x) ** 2 / 2, sp.log(sp.sec(x) + sp.tan(x))], "$\\frac{\\sec^3x}{\\tan x}=\\frac{\\sec x(1+\\tan^2x)}{\\tan x}=\\csc x+\\sec x\\tan x$; integrate each: $-\\ln|\\csc x+\\cot x|+\\sec x$.", "Tutorial 9, Q10(a)", pts=(0.3, 0.7, 1.1))
    ant_q(B, ch, 3, "x\\sin^2x\\,dx", x * sp.sin(x) ** 2, x ** 2 / 4 - x * sp.sin(2 * x) / 4 - sp.cos(2 * x) / 8, [x ** 2 / 4 + x * sp.sin(2 * x) / 4 + sp.cos(2 * x) / 8, x ** 2 / 4 - x * sp.sin(2 * x) / 2 - sp.cos(2 * x) / 4, x ** 3 * sp.sin(x) ** 3 / 9, x ** 2 / 2 - x * sp.sin(2 * x) / 4], "Half-angle: $\\sin^2x=\\frac{1-\\cos2x}{2}$, then parts on $\\int x\\cos2x$.", "Tutorial 9, Q10(b)", pts=(0.3, 0.7, 1.1))
    # ---- trigonometric substitution
    def_q(B, ch, 2, "\\dfrac{dx}{\\sqrt{9-x^2}}", 1 / sp.sqrt(9 - x ** 2), 0, sp.Rational(3, 2), sp.pi / 6, [sp.pi / 3, sp.pi / 4, sp.pi / 2, sp.pi / 12], "$x=3\\sin\\theta$: $\\int d\\theta=\\theta=\\arcsin\\frac x3$; at $x=\\frac32$: $\\arcsin\\frac12=\\frac\\pi6$.", "Tutorial 10, Q1(a)", topic="Trigonometric substitution")
    ant_q(B, ch, 3, "\\sqrt{1-9t^2}\\,dt", sp.sqrt(1 - 9 * t ** 2), (sp.asin(3 * t) + 3 * t * sp.sqrt(1 - 9 * t ** 2)) / 6, [(sp.asin(3 * t) - 3 * t * sp.sqrt(1 - 9 * t ** 2)) / 6, (sp.asin(3 * t) + 3 * t * sp.sqrt(1 - 9 * t ** 2)) / 2, (sp.asin(3 * t) + t * sp.sqrt(1 - 9 * t ** 2)) / 6, sp.asin(3 * t) / 3], "$3t=\\sin\\theta$: $\\frac13\\int\\cos^2\\theta\\,d\\theta=\\frac16(\\theta+\\sin\\theta\\cos\\theta)$.", "Tutorial 10, Q1(b)", var=t, topic="Trigonometric substitution", pts=(0.1, 0.2, 0.3))
    ant_q(B, ch, 3, "\\sqrt{\\dfrac{x+1}{1-x}}\\,dx", sp.sqrt((x + 1) / (1 - x)), sp.asin(x) - sp.sqrt(1 - x ** 2), [sp.asin(x) + sp.sqrt(1 - x ** 2), sp.acos(x) - sp.sqrt(1 - x ** 2), sp.asin(x) - sp.sqrt(1 - x ** 2) / 2, 2 * sp.sqrt((x + 1) / (1 - x))], "Multiply by $\\sqrt{x+1}/\\sqrt{x+1}$: $\\frac{x+1}{\\sqrt{1-x^2}}$; split into $\\frac{1}{\\sqrt{1-x^2}}+\\frac{x}{\\sqrt{1-x^2}}$.", "Tutorial 10, Q2(a)", topic="Trigonometric substitution", pts=(0.1, 0.3, 0.6))
    ant_q(B, ch, 3, "\\dfrac{v^2\\,dv}{(1-v^2)^{5/2}}", v_ ** 2 / (1 - v_ ** 2) ** sp.Rational(5, 2), v_ ** 3 / (3 * (1 - v_ ** 2) ** sp.Rational(3, 2)), [v_ ** 3 / (1 - v_ ** 2) ** sp.Rational(3, 2), v_ / (3 * (1 - v_ ** 2) ** sp.Rational(3, 2)), v_ ** 3 / (3 * (1 - v_ ** 2) ** sp.Rational(5, 2)), sp.tan(sp.asin(v_)) ** 2 / 2], "$v=\\sin\\theta$: $\\int\\frac{\\sin^2\\theta}{\\cos^4\\theta}d\\theta=\\int\\tan^2\\theta\\sec^2\\theta\\,d\\theta=\\frac{\\tan^3\\theta}3$, and $\\tan\\theta=\\frac{v}{\\sqrt{1-v^2}}$.", "Tutorial 10, Q2(b)", var=v_, topic="Trigonometric substitution", pts=(0.1, 0.3, 0.5))
    xI = sp.Symbol("x", real=True)
    ant_q(B, ch, 3, "x^3\\sqrt{1-x^2}\\,dx", x ** 3 * sp.sqrt(1 - x ** 2), -(1 - x ** 2) ** sp.Rational(3, 2) / 3 + (1 - x ** 2) ** sp.Rational(5, 2) / 5, [(1 - x ** 2) ** sp.Rational(3, 2) / 3 - (1 - x ** 2) ** sp.Rational(5, 2) / 5, -(1 - x ** 2) ** sp.Rational(3, 2) / 3 - (1 - x ** 2) ** sp.Rational(5, 2) / 5, -(1 - x ** 2) ** sp.Rational(3, 2) / 3 + (1 - x ** 2) ** sp.Rational(5, 2) / 10, x ** 4 * sp.sqrt(1 - x ** 2) / 4],
          "Three methods agree. $u$-substitution: $u=1-x^2$, $x^3dx=-\\frac12(1-u)\\,du$, giving $-\\frac12\\int(1-u)\\sqrt u\\,du=-\\frac13u^{3/2}+\\frac15u^{5/2}$. (Parts: $\\int x^2\\cdot x\\sqrt{1-x^2}dx$; trig sub: $x=\\sin\\theta$.)", "Tutorial 10, Q4", topic="Trigonometric substitution", pts=(0.1, 0.3, 0.6))
    ant_q(B, ch, 3, "\\dfrac{dx}{\\sqrt{4+x^2}}", 1 / sp.sqrt(4 + x ** 2), sp.log(x + sp.sqrt(4 + x ** 2)), [sp.asin(x / 2), sp.atan(x / 2) / 2, sp.log(sp.sqrt(4 + x ** 2)), sp.sqrt(4 + x ** 2)], "$x=2\\tan\\theta$: $\\int\\sec\\theta\\,d\\theta=\\ln|\\sec\\theta+\\tan\\theta|=\\ln\\left|\\frac{\\sqrt{4+x^2}+x}{2}\\right|$ (the constant $\\ln\\frac12$ is absorbed in $C$).", "Computation problems 10, Q1", topic="Trigonometric substitution")
    ant_q(B, ch, 3, "\\dfrac{dx}{\\sqrt{25x^2-4}}\\ \\ (x>\\tfrac25)", 1 / sp.sqrt(25 * x ** 2 - 4), sp.log(5 * x + sp.sqrt(25 * x ** 2 - 4)) / 5, [sp.log(5 * x + sp.sqrt(25 * x ** 2 - 4)), sp.acos(2 / (5 * x)) / 2, sp.log(5 * x + sp.sqrt(25 * x ** 2 - 4)) / 25, sp.sqrt(25 * x ** 2 - 4) / 5], "$5x=2\\sec\\theta$: $\\frac15\\int\\sec\\theta\\,d\\theta=\\frac15\\ln|\\sec\\theta+\\tan\\theta|=\\frac15\\ln\\left|\\frac{5x}{2}+\\frac{\\sqrt{25x^2-4}}{2}\\right|$.", "Computation problems 10, Q2", topic="Trigonometric substitution", pts=(0.5, 0.9, 1.5))
    # ---- partial fractions
    ap = sp.apart((t ** 2 + 8) / (t ** 2 + 5 * t + 6), t)
    B.mcq(ch, "Partial fractions", 2, "Expand $\\dfrac{t^2+8}{t^2+5t+6}$ in partial fractions.", "$" + tex(ap) + "$", ["$" + tex(w) + "$" for w in [1 + 12 / (t + 2) - 17 / (t + 3), 1 - 12 / (t + 2) - 17 / (t + 3), 12 / (t + 2) + 17 / (t + 3), 1 - 17 / (t + 2) + 12 / (t + 3)] if sp.simplify(w - ap) != 0],
          "Improper (degrees equal): divide first, $\\frac{t^2+8}{t^2+5t+6}=1+\\frac{2-5t}{(t+2)(t+3)}$, then $\\frac{2-5t}{(t+2)(t+3)}=\\frac{A}{t+2}+\\frac{B}{t+3}$ with $A=12$, $B=-17$.", "Computation problems 10, Q3", "src")
    assert sp.simplify(ap - (1 + 12 / (t + 2) - 17 / (t + 3))) == 0
    ant_q(B, ch, 3, "\\dfrac{x^2+4x+1}{(x-1)(x+1)(x+3)}\\,dx", (x ** 2 + 4 * x + 1) / ((x - 1) * (x + 1) * (x + 3)), sp.Rational(3, 4) * sp.log(x - 1) + sp.Rational(1, 2) * sp.log(x + 1) - sp.Rational(1, 4) * sp.log(x + 3),
          [sp.Rational(3, 4) * sp.log(x - 1) - sp.Rational(1, 2) * sp.log(x + 1) - sp.Rational(1, 4) * sp.log(x + 3), sp.Rational(1, 4) * sp.log(x - 1) + sp.Rational(1, 2) * sp.log(x + 1) + sp.Rational(3, 4) * sp.log(x + 3), sp.log(x - 1) + sp.log(x + 1) - sp.log(x + 3), sp.Rational(3, 4) * sp.log(x - 1) + sp.Rational(1, 2) * sp.log(x + 1) + sp.Rational(1, 4) * sp.log(x + 3)],
          "Cover-up: $A=\\frac{1+4+1}{2\\cdot4}=\\frac34$, $B=\\frac{1-4+1}{(-2)(2)}=\\frac12$, $C=\\frac{9-12+1}{(-4)(-2)}=-\\frac14$.", "Computation problems 10, Q4", topic="Partial fractions", pts=(1.4, 1.8, 2.5))
    ant_q(B, ch, 3, "\\dfrac{2x^3-2x^2+1}{x^2-x}\\,dx", (2 * x ** 3 - 2 * x ** 2 + 1) / (x ** 2 - x), x ** 2 + sp.log(x - 1) - sp.log(x), [x ** 2 - sp.log(x - 1) + sp.log(x), x ** 2 + sp.log(x - 1) + sp.log(x), x ** 2 / 2 + sp.log(x - 1) - sp.log(x), 2 * x + sp.log(x - 1) - sp.log(x)],
          "Long division: $\\frac{2x^3-2x^2+1}{x^2-x}=2x+\\frac{1}{x(x-1)}=2x+\\frac1{x-1}-\\frac1x$.", "Computation problems 10, Q5", topic="Partial fractions", pts=(1.4, 1.8, 2.5))
    ant_q(B, ch, 3, "\\dfrac{dt}{t^3+t^2-2t}", 1 / (t ** 3 + t ** 2 - 2 * t), sp.log(t - 1) / 3 - sp.log(t) / 2 + sp.log(t + 2) / 6, [sp.log(t - 1) / 3 + sp.log(t) / 2 + sp.log(t + 2) / 6, sp.log(t - 1) / 3 - sp.log(t) / 2 - sp.log(t + 2) / 6, sp.log(t - 1) - sp.log(t) + sp.log(t + 2), sp.log(t - 1) / 6 - sp.log(t) / 2 + sp.log(t + 2) / 3],
          "$t^3+t^2-2t=t(t-1)(t+2)$. Cover-up: $A_0=\\frac{1}{(-1)(2)}=-\\frac12$, $A_1=\\frac{1}{1\\cdot3}=\\frac13$, $A_{-2}=\\frac{1}{(-2)(-3)}=\\frac16$.", "Tutorial 10, Q5(a)", var=t, topic="Partial fractions", pts=(1.4, 1.8, 2.5))
    F5b = sp.atan(s_) + 1 / (s_ - 1) - 1 / (s_ - 1) ** 2
    ant_q(B, ch, 3, "\\dfrac{2s+2}{(s^2+1)(s-1)^3}\\,ds", (2 * s_ + 2) / ((s_ ** 2 + 1) * (s_ - 1) ** 3), F5b, [F5b - 2 / (s_ - 1), -F5b, sp.atan(s_) - 1 / (s_ - 1) - 1 / (s_ - 1) ** 2, sp.atan(s_) + 1 / (s_ - 1) + 1 / (s_ - 1) ** 2, sp.log(s_ ** 2 + 1) + 1 / (s_ - 1) - 1 / (s_ - 1) ** 2],
          "Partial fractions $\\frac{As+B}{s^2+1}+\\frac{C}{s-1}+\\frac{D}{(s-1)^2}+\\frac{E}{(s-1)^3}$ give $\\frac{2s+2}{(s^2+1)(s-1)^3}=\\frac{1}{s^2+1}-\\frac{1}{(s-1)^2}+\\frac{2}{(s-1)^3}$. Integrating term by term: $\\arctan s+\\frac{1}{s-1}-\\frac{1}{(s-1)^2}$.", "Tutorial 10, Q5(b)", var=s_, topic="Partial fractions", pts=(1.4, 1.9, 2.6))
    # ---- improper integrals
    mc_val(B, ch, "Improper integrals", 3, "$\\displaystyle\\int_0^{\\infty}2e^{-\\theta}\\sin\\theta\\,d\\theta=$", 1, [2, sp.Rational(1, 2), sp.oo, 0], "$\\int e^{-\\theta}\\sin\\theta\\,d\\theta=-\\frac12e^{-\\theta}(\\sin\\theta+\\cos\\theta)$; from $0$ to $\\infty$: $0-(-\\frac12)=\\frac12$, times $2$ gives $1$.", "Tutorial 10, Q7(a)", "src")
    assert sp.integrate(2 * sp.exp(-x) * sp.sin(x), (x, 0, oo)) == 1
    mc_val(B, ch, "Improper integrals", 3, "$\\displaystyle\\int_0^2\\dfrac{dx}{\\sqrt{|x-1|}}=$", 4, [2, 0, sp.oo, 8], "Singular at $x=1$: split, $\\int_0^1\\frac{dx}{\\sqrt{1-x}}+\\int_1^2\\frac{dx}{\\sqrt{x-1}}=2+2=4$ (each converges since $p=\\frac12<1$).", "Tutorial 10, Q7(b)", "src")
    assert sp.integrate(1 / sp.sqrt(sp.Abs(x - 1)), (x, 0, 1)) + sp.integrate(1 / sp.sqrt(x - 1), (x, 1, 2)) == 4
    mc_text(B, ch, "Improper integrals", 2, "$\\displaystyle\\int_0^{\\infty}\\dfrac{d\\theta}{1+e^{\\theta}}$", "converges (to $\\ln2$)", ["diverges", "converges to $1$", "converges to $\\frac12$"], "$\\frac1{1+e^\\theta}<e^{-\\theta}$ so it converges by comparison; exactly, $\\int\\frac{d\\theta}{1+e^\\theta}=\\theta-\\ln(1+e^\\theta)$ gives $\\ln2$.", "Tutorial 10, Q8(a)", "src")
    assert sp.integrate(1 / (1 + sp.exp(x)), (x, 0, oo)) == sp.log(2)
    mc_text(B, ch, "Improper integrals", 2, "$\\displaystyle\\int_{e^{e}}^{\\infty}\\ln(\\ln x)\\,dx$", "diverges", ["converges to $0$", "converges to $e$", "converges to $1$"], "For $x\\ge e^e$, $\\ln(\\ln x)\\ge1$, so the integral exceeds $\\int_{e^e}^\\infty1\\,dx=\\infty$ (direct comparison).", "Tutorial 10, Q8(b)", "src")
    mc_text(B, ch, "Improper integrals", 3, "$\\displaystyle\\int_2^{\\infty}\\dfrac{dx}{x(\\ln x)^p}$ ($p>0$) converges if and only if", "$p>1$", ["$p<1$", "$p\\ge1$", "$p>2$"], "$u=\\ln x$: $\\int_{\\ln2}^\\infty u^{-p}du$, a $p$-integral at infinity, finite iff $p>1$.", "Tutorial 11, Q6(a)", "src")
    mc_val(B, ch, "Improper integrals", 2, "$\\displaystyle\\int_0^{1}\\dfrac{dx}{\\sqrt{1-x^2}}=$", sp.pi / 2, [sp.pi, 1, sp.pi / 4, sp.oo], "$[\\arcsin x]_0^1=\\frac\\pi2$ (improper at $x=1$ but convergent).", "Computation problems 10, Q6", "src")
    mc_val(B, ch, "Improper integrals", 3, "$\\displaystyle\\int_0^{\\ln2}x^{-2}e^{-1/x}\\,dx=$", sp.exp(-1 / sp.log(2)), [sp.exp(-sp.log(2)), sp.Rational(1, 2), sp.exp(1 / sp.log(2)), 1], "$u=-\\frac1x$, $du=\\frac{dx}{x^2}$: $[e^{-1/x}]_0^{\\ln2}=e^{-1/\\ln2}-\\lim_{x\\to0^+}e^{-1/x}=e^{-1/\\ln2}$.", "Computation problems 10, Q7", "src")
    mc_val(B, ch, "Improper integrals", 2, "$\\displaystyle\\lim_{x\\to\\infty}\\int_{-x}^{x}\\sin t\\,dt=$", 0, [sp.oo, 1, 2, -1], "$\\sin t$ is odd, so $\\int_{-x}^x\\sin t\\,dt=0$ for every $x$. (Caution: this does NOT make $\\int_{-\\infty}^\\infty\\sin t\\,dt$ convergent.)", "Computation problems 10, Q8", "src")
    mc_val(B, ch, "Improper integrals", 2, "$\\displaystyle\\int_{-\\infty}^{\\infty}\\dfrac{dx}{1+x^2}=$", sp.pi, [sp.pi / 2, 2, sp.oo, 2 * sp.pi], "$[\\arctan x]_{-\\infty}^{\\infty}=\\frac\\pi2-(-\\frac\\pi2)=\\pi$.", "Computation problems 10, Q10", "src")
    L9 = sp.integrate(sp.log(1 + x), (x, 0, 1)); assert L9 == 2 * sp.log(2) - 1
    mc_val(B, ch, "Improper integrals", 3, "Evaluate $L=\\displaystyle\\lim_{n\\to\\infty}\\sum_{k=1}^{n}\\ln\\sqrt[n]{1+\\tfrac kn}$ by recognising a Riemann sum.", 2 * sp.log(2) - 1, [sp.log(2), 1, 2 * sp.log(2), sp.log(2) - 1],
           "$\\ln\\sqrt[n]{1+\\frac kn}=\\frac1n\\ln\\left(1+\\frac kn\\right)$, so $L=\\int_0^1\\ln(1+x)\\,dx=[(1+x)\\ln(1+x)-x]_0^1=2\\ln2-1$.", "Computation problems 10, Q9", "src")
    # ---- Mock Test Q3-Q4
    G13 = (sp.atan((x - 3) / 2) + 2 * (x - 3) / (x ** 2 - 6 * x + 13)) / 16
    ant_q(B, ch, 3, "\\dfrac{dx}{(x^2-6x+13)^2}", 1 / (x ** 2 - 6 * x + 13) ** 2, G13, [(sp.atan((x - 3) / 2) + 2 * (x - 3) / (x ** 2 - 6 * x + 13)) / 8, sp.atan((x - 3) / 2) / 2, -1 / (x ** 2 - 6 * x + 13), (sp.atan((x - 3) / 2) - 2 * (x - 3) / (x ** 2 - 6 * x + 13)) / 16],
          "Complete the square: $x^2-6x+13=(x-3)^2+4$. With $x-3=2\\tan\\theta$: $\\int\\frac{2\\sec^2\\theta\\,d\\theta}{16\\sec^4\\theta}=\\frac18\\int\\cos^2\\theta\\,d\\theta=\\frac1{16}(\\theta+\\sin\\theta\\cos\\theta)$, and $\\sin\\theta\\cos\\theta=\\frac{\\tan\\theta}{1+\\tan^2\\theta}=\\frac{2(x-3)}{x^2-6x+13}$.", "Mock Test 1, Q3(a)(iii)", topic="Trigonometric substitution", pts=(3.4, 4.1, 5.2))
    sa = sp.integrate(2 * sp.pi * sp.Rational(1, 3) * sp.sqrt(x) * (3 - x) * sp.sqrt(1 + sp.diff(sp.Rational(1, 3) * sp.sqrt(x) * (3 - x), x) ** 2), (x, 0, 3))
    sa = sp.simplify(sa); assert sa == 3 * sp.pi, sa
    mc_val(B, ch, "Arc length and surface area", 3, "The arc $y=\\frac13\\sqrt x\\,(3-x)$, $0\\le x\\le3$, is rotated about the $x$-axis. The surface area is", 3 * sp.pi, [2 * sp.pi, 6 * sp.pi, 9 * sp.pi / 2, sp.pi],
           "$y'=\\frac{1-x}{2\\sqrt x}$ and $1+y'^2=\\left(\\frac{1+x}{2\\sqrt x}\\right)^2$; $S=2\\pi\\int_0^3\\frac13\\sqrt x(3-x)\\frac{1+x}{2\\sqrt x}dx=\\frac\\pi3\\int_0^3(3+2x-x^2)dx=\\frac\\pi3\\cdot9=3\\pi$.", "Mock Test 1, Q3(b)(ii)", "src")
    k_ = sp.Symbol("k", positive=True)
    B.mcq(ch, "Improper integrals", 3, "For which $k$ does $\\displaystyle\\int_2^\\infty\\dfrac{dx}{x\\ln^kx}$ converge, and what is its value then?", "$k>1$; the value is $\\dfrac{(\\ln2)^{1-k}}{k-1}$", ["$k\\ge1$; the value is $\\dfrac{(\\ln2)^{1-k}}{k-1}$", "$k>1$; the value is $\\dfrac{(\\ln2)^{k-1}}{k-1}$", "$k<1$; the value is $\\dfrac{(\\ln2)^{1-k}}{1-k}$"],
          "$u=\\ln x$: $\\int_{\\ln2}^\\infty u^{-k}du=\\left[\\frac{u^{1-k}}{1-k}\\right]_{\\ln2}^\\infty$, which is finite iff $k>1$ and then equals $\\frac{(\\ln2)^{1-k}}{k-1}$. For $k=1$ it is $\\ln\\ln x\\to\\infty$.", "Mock Test 1, Q4", "src")
    B.mcq(ch, "Improper integrals", 1, "$\\displaystyle\\int_1^\\infty\\dfrac{dx}{x^p}$ converges iff", "$p>1$", ["$p\\ge1$", "$p<1$", "$p>0$"], "For $p\\ne1$, $\\left[\\frac{x^{1-p}}{1-p}\\right]_1^\\infty$ is finite only when $p>1$; for $p=1$ it is $\\ln x\\to\\infty$.", "Lecture 9–10", "concept")
    B.mcq(ch, "Improper integrals", 1, "$\\displaystyle\\int_0^1\\dfrac{dx}{x^p}$ converges iff", "$p<1$", ["$p>1$", "$p\\le1$", "$p\\ge0$"], "Near $0$ the integrand blows up unless $p<1$.", "Lecture 9–10", "concept")
    B.mcq(ch, "Improper integrals", 2, "Direct comparison: if $0\\le f\\le g$ and $\\int^\\infty g$ converges, then", "$\\int^\\infty f$ converges", ["$\\int^\\infty f$ diverges", "$\\int^\\infty f=\\int^\\infty g$", "nothing can be said"], "A smaller non-negative function cannot have a larger area; the converse comparison proves divergence.", "Lecture 10a", "concept")
    B.mcq(ch, "Techniques of integration", 1, "Integration by parts: $\\int u\\,dv=$", "$uv-\\int v\\,du$", ["$uv+\\int v\\,du$", "$u\\,dv-v\\,du$", "$\\int u\\,du\\cdot\\int dv$"], "Reverse of the product rule.", "Lecture 7–8", "concept")
    B.mcq(ch, "Trigonometric substitution", 1, "To integrate $\\sqrt{a^2-x^2}$ one uses the substitution", "$x=a\\sin\\theta$", ["$x=a\\tan\\theta$", "$x=a\\sec\\theta$", "$x=a\\cos^2\\theta$"], "Then $\\sqrt{a^2-x^2}=a\\cos\\theta$. ($\\sqrt{a^2+x^2}\\to\\tan$, $\\sqrt{x^2-a^2}\\to\\sec$.)", "Lecture 9", "concept")
    B.mcq(ch, "Partial fractions", 1, "Before decomposing $\\dfrac{P(x)}{Q(x)}$ into partial fractions one must first", "divide if $\\deg P\\ge\\deg Q$ (make the fraction proper)", ["factor $P(x)$", "differentiate $Q(x)$", "set $x=0$"], "Partial fractions apply only to proper rational functions.", "Lecture 9", "concept")

# ============================================================================== CHAPTER 6
def ch6(B):
    ch = "c6"; rng = B.rng
    n = sp.Symbol("n", positive=True, integer=True)
    # ---- limits of sequences
    SEQ = [("\\sqrt[n]{4^{n}n}", sp.root(4 ** n * n, n), 4, "Tutorial 11, Q1(a)", "$\\sqrt[n]{4^nn}=4\\,n^{1/n}\\to4\\cdot1$ (since $n^{1/n}\\to1$)."),
           ("\\left(\\tfrac13\\right)^{n}+\\dfrac{1}{\\sqrt{2^{n}}}", sp.Rational(1, 3) ** n + 1 / sp.sqrt(2 ** n), 0, "Tutorial 11, Q1(b)", "Both terms are geometric with ratio $<1$: $\\frac13$ and $\\frac1{\\sqrt2}$; each tends to $0$."),
           ("\\dfrac{3^{n}}{n^{3}}", 3 ** n / n ** 3, oo, "Computation problems 11, Q1", "Exponentials beat polynomials: $\\frac{3^n}{n^3}\\to\\infty$ (diverges)."),
           ("\\dfrac{(10/11)^{n}}{(9/10)^{n}+(11/12)^{n}}", (sp.Rational(10, 11)) ** n / ((sp.Rational(9, 10)) ** n + (sp.Rational(11, 12)) ** n), 0, "Computation problems 11, Q2", "Divide by $(11/12)^n$: the numerator is $\\left(\\frac{120}{121}\\right)^n\\to0$ and the denominator tends to $1$; the limit is $0$."),
           ("\\dfrac{n^2+1}{2n^2-n}", (n ** 2 + 1) / (2 * n ** 2 - n), sp.Rational(1, 2), "Generated (Lecture 10b)", "Divide by $n^2$: $\\frac{1+1/n^2}{2-1/n}\\to\\frac12$."),
           ("\\left(1+\\dfrac{2}{n}\\right)^{n}", (1 + 2 / n) ** n, sp.exp(2), "Generated (Lecture 10b)", "Standard limit $\\left(1+\\frac an\\right)^n\\to e^a$ with $a=2$."),
           ("\\dfrac{\\sin n}{n}", sp.sin(n) / n, 0, "Generated (Lecture 10b)", "Squeeze: $-\\frac1n\\le\\frac{\\sin n}{n}\\le\\frac1n$."),
           ("\\dfrac{n!}{n^n}", sp.factorial(n) / n ** n, 0, "Generated (Lecture 10b)", "$\\frac{n!}{n^n}=\\frac{1}{n}\\cdot\\frac{2}{n}\\cdots\\frac{n}{n}\\le\\frac1n\\to0$ (squeeze).")]
    for lbl, an, expect, src, how in SEQ:
        val = seq_limit(an, n, expect, lbl)
        c, wr = lim_options(val, rng, extras=[1, 0, oo] if expect not in (1, 0) else [oo, 2])
        B.mcq(ch, "Limits of sequences", 2, "Find $\\displaystyle\\lim_{n\\to\\infty}a_n$ for $a_n=%s$." % lbl, c, wr, how + " Result: %s." % c, src, "src" if "Generated" not in src else "gen")
    # recursive sequences
    def rec_limit(f, a1, N=60):
        a = sp.Rational(a1)
        for _ in range(N):
            a = f(a)
        return float(a)
    r2 = rec_limit(lambda a: (a + 6) / (a + 2), -1); assert abs(r2 - 2) < 1e-9
    B.mcq(ch, "Limits of sequences", 3, "Let $a_1=-1$, $a_{n+1}=\\dfrac{a_n+6}{a_n+2}$ and assume $(a_n)$ converges. Its limit is", "$2$", ["$-3$", "$3$", "$-2$"],
          "If $a_n\\to L$ then $L=\\frac{L+6}{L+2}\\Rightarrow L^2+L-6=0\\Rightarrow L=2$ or $L=-3$. The terms $-1,5,\\frac{11}7,\\dots$ are positive from $a_2$ on, so the limit must be the positive root $2$.", "Tutorial 11, Q2", "src")
    r3 = rec_limit(lambda a: 2 + 1 / a, 2); assert abs(r3 - (1 + math.sqrt(2))) < 1e-9
    B.mcq(ch, "Limits of sequences", 3, "The sequence $2,\\ 2+\\frac12,\\ 2+\\frac{1}{2+\\frac12},\\ 2+\\frac{1}{2+\\frac{1}{2+\\frac12}},\\dots$ (so $a_{n+1}=2+\\frac1{a_n}$) converges to", "$1+\\sqrt2$", ["$2$", "$1-\\sqrt2$", "$\\frac{1+\\sqrt5}{2}$"],
          "If $a_n\\to L$: $L=2+\\frac1L\\Rightarrow L^2-2L-1=0\\Rightarrow L=1\\pm\\sqrt2$; all terms are positive, so $L=1+\\sqrt2$.", "Computation problems 11, Q3", "src")
    # ---- series sums
    S3 = sp.summation(5 / (n * (n + 1)), (n, 1, oo)); assert S3 == 5
    mc_val(B, ch, "Series sums", 2, "$\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{5}{n(n+1)}=$", 5, [sp.Rational(5, 2), 1, sp.oo, 10], "Telescoping: $\\frac5{n(n+1)}=5\\left(\\frac1n-\\frac1{n+1}\\right)$, partial sum $S_N=5\\left(1-\\frac1{N+1}\\right)\\to5$.", "Tutorial 11, Q3", "src")
    mc_val(B, ch, "Series sums", 2, "Write $0.\\overline{23}=0.232323\\ldots$ as a fraction.", sp.Rational(23, 99), [sp.Rational(23, 100), sp.Rational(23, 90), sp.Rational(2, 9), sp.Rational(23, 999)], "Geometric series: $\\frac{23}{100}\\cdot\\frac1{1-1/100}=\\frac{23}{99}$.", "Tutorial 11, Q4", "src")
    S4 = sp.summation(1 / sp.Integer(2) ** n + (-1) ** n / sp.Integer(5) ** n, (n, 0, oo)); assert S4 == sp.Rational(17, 6)
    mc_val(B, ch, "Series sums", 2, "$\\displaystyle\\sum_{n=0}^{\\infty}\\left(\\dfrac1{2^n}+\\dfrac{(-1)^n}{5^n}\\right)=$", sp.Rational(17, 6), [sp.Rational(5, 2), sp.Rational(9, 4), sp.Rational(7, 3), sp.Rational(13, 6)], "Two geometric series: $\\frac1{1-1/2}=2$ and $\\frac1{1+1/5}=\\frac56$; the sum is $2+\\frac56=\\frac{17}{6}$.", "Computation problems 11, Q4", "src")
    mc_val(B, ch, "Series sums", 2, "$\\displaystyle\\sum_{n=1}^{\\infty}\\left(\\dfrac1n-\\dfrac1{n+1}\\right)=$", 1, [sp.oo, 0, sp.Rational(1, 2), 2], "Partial sums telescope: $S_N=1-\\frac{1}{N+1}\\to1$.", "Computation problems 11, Q5", "src")
    mc_val(B, ch, "Series sums", 2, "$\\displaystyle\\sum_{n=1}^{\\infty}\\left(\\dfrac23\\right)^{n}=$", 2, [3, sp.Rational(2, 3), sp.Rational(1, 3), sp.oo], "Geometric series starting at $n=1$: $\\frac{r}{1-r}=\\frac{2/3}{1/3}=2$ (first term $a=\\frac23$).", "Computation problems 11, Q7", "src")
    assert sp.simplify(sp.summation(sp.exp(-2 * n), (n, 1, oo)) - 1 / (sp.exp(2) - 1)) == 0
    mc_val(B, ch, "Series sums", 2, "$\\displaystyle\\sum_{n=1}^{\\infty}e^{-2n}=$", 1 / (sp.exp(2) - 1), [1 / (1 - sp.exp(-2)), sp.exp(-2), 1 / (sp.exp(2) + 1), sp.exp(2) / (sp.exp(2) - 1)], "Geometric with first term $e^{-2}$ and ratio $e^{-2}$: $\\frac{e^{-2}}{1-e^{-2}}=\\frac1{e^2-1}$ (it converges, as the Integral Test also shows).", "Computation problems 11, Q6", "src")
    # ---- convergence / divergence verdicts (cross-checked numerically)
    tests = [
        ("\\displaystyle\\sum_{n=0}^{\\infty}\\cos\\dfrac{n\\pi}{2}", None, "diverges", "$a_n=\\cos\\frac{n\\pi}2$ takes the values $1,0,-1,0,\\dots$ and does not tend to $0$: the $n$-th term test shows divergence.", "Tutorial 11, Q5(a)", 2),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n^n}{n!}", None, "diverges", "$\\frac{a_{n+1}}{a_n}=\\left(1+\\frac1n\\right)^n\\to e>1$ (ratio test), so $a_n\\to\\infty$.", "Tutorial 11, Q5(b)", 2),
        ("\\displaystyle\\sum_{n=1}^{\\infty}ne^{-n^2}", lambda m: m * np.exp(-m ** 2), "converges", "Integral test: $\\int_1^\\infty xe^{-x^2}dx=\\frac1{2e}<\\infty$ ($f$ is positive and decreasing for $x\\ge1$).", "Tutorial 11, Q7(a)", 2),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{2^{\\ln n}}", lambda m: 2.0 ** (-np.log(m)), "diverges", "$2^{-\\ln n}=n^{-\\ln2}$ is a $p$-series with $p=\\ln2\\approx0.69<1$: diverges (equivalently $\\int_1^\\infty x^{-\\ln2}dx=\\infty$).", "Tutorial 11, Q7(b)", 3),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{\\cos^2n}{n^{3/2}}", lambda m: np.cos(m) ** 2 / m ** 1.5, "converges", "$0\\le\\frac{\\cos^2n}{n^{3/2}}\\le\\frac{1}{n^{3/2}}$, a convergent $p$-series ($p=\\frac32>1$): comparison test.", "Tutorial 11, Q8", 2),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{5^n}{\\sqrt{n\\,4^n}}", None, "diverges", "$a_n=\\frac{(5/2)^n}{\\sqrt n}\\to\\infty$ (exponential beats $\\sqrt n$), so the series diverges by the $n$-th term test (the Limit Comparison Test with $(5/2)^n$ also fails to give convergence).", "Tutorial 11, Q9", 3),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n!}{10^n}", None, "diverges", "Ratio test: $\\frac{a_{n+1}}{a_n}=\\frac{n+1}{10}\\to\\infty>1$.", "Tutorial 11, Q10(a)", 2),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n^n}{(2^n)^2}", None, "diverges", "Root test: $\\sqrt[n]{a_n}=\\frac{n}{4}\\to\\infty>1$.", "Tutorial 11, Q10(b)", 2),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{\\sqrt n+1}{\\sqrt{n^2+3}}", lambda m: (np.sqrt(m) + 1) / np.sqrt(m ** 2 + 3), "diverges", "Compare with $\\frac1{\\sqrt n}$: $\\frac{\\sqrt n+1}{\\sqrt{n^2+3}}\\ge\\frac{\\sqrt n}{\\sqrt{n^2+3n^2}}=\\frac{1}{2\\sqrt n}$, a divergent $p$-series ($p=\\frac12$).", "Computation problems 11, Q8", 3),
        ("\\displaystyle\\sum_{n=2}^{\\infty}\\dfrac{1}{\\sqrt n\\,\\ln n}", lambda m: 1 / (np.sqrt(m) * np.log(m)), "diverges", "For large $n$, $\\ln n<n^{1/4}$, so $\\frac{1}{\\sqrt n\\ln n}>\\frac{1}{n^{3/4}}$ (divergent $p$-series, $p=\\frac34$).", "Computation problems 11, Q9", 3),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n^{\\sqrt2}}{2^n}", lambda m: m ** 1.4142135623730951 / 2.0 ** m, "converges", "Ratio test: $\\frac{a_{n+1}}{a_n}=\\frac12\\left(1+\\frac1n\\right)^{\\sqrt2}\\to\\frac12<1$.", "Computation problems 11, Q10", 3),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{2^n}{3^n}", lambda m: (2 / 3) ** m, "converges", "Geometric series with ratio $\\frac23$, $|r|<1$.", "Computation problems 11, Q7", 1),
        ("\\displaystyle\\sum_{n=2}^{\\infty}\\dfrac{1}{n\\ln^2n}", lambda m: 1 / (m * np.log(m) ** 2), "converges", "Integral test: $\\int_2^\\infty\\frac{dx}{x\\ln^2x}=\\frac1{\\ln2}<\\infty$.", "Tutorial 11, Q6(b)", 3),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{n^{1.01}}", None, "converges", "$p$-series with $p=1.01>1$ converges (very slowly).", "Generated (Lecture 11)", 1),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{\\sqrt{n}}", lambda m: m ** -0.5, "diverges", "$p$-series with $p=\\frac12\\le1$ diverges.", "Generated (Lecture 11)", 1),
        ("\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{3n+1}{2n+5}", None, "diverges", "$a_n\\to\\frac32\\ne0$: the terms do not tend to $0$.", "Generated (Lecture 11)", 1),
    ]
    for lbl, fnum, verdict, how, src, lvl in tests:
        if fnum is not None:
            series_behaves(fnum, "conv" if verdict == "converges" else "div", start=2 if "n=2" in lbl else 1)
        ops = ["converges", "diverges"]
        correct = verdict
        wr = [o for o in ops if o != verdict] + ["converges conditionally but not absolutely" if verdict == "converges" else "converges absolutely", "the test is inconclusive; no conclusion can be drawn"]
        B.mcq(ch, "Convergence tests", lvl, "Does the series $%s$ converge or diverge?" % lbl, correct, wr, how, src, "src" if "Generated" not in src else "gen")
    # note about the printed key of Computation problems 11, Q11
    a = [sp.Integer(1)]
    for k in range(1, 60):
        a.append(a[-1] * (1 + sp.atan(k)) / k)
    ssum = sum(a)
    assert abs(float(a[-1])) < 1e-30 and float(ssum) > 0
    ratio_lim = sp.limit((1 + sp.atan(n)) / n, n, oo); assert ratio_lim == 0
    B.mcq(ch, "Convergence tests", 3, "Let $a_1=1$ and $a_{n+1}=\\dfrac{1+\\tan^{-1}n}{n}\\,a_n$ ($n\\ge1$). Does $\\sum a_n$ converge?", "converges (ratio test: $\\frac{a_{n+1}}{a_n}\\to0<1$)", ["diverges, because $\\tan^{-1}n\\to\\frac\\pi2$", "diverges, because $a_n\\ge1$", "the ratio test is inconclusive"],
          "$\\frac{a_{n+1}}{a_n}=\\frac{1+\\arctan n}{n}\\le\\frac{1+\\pi/2}{n}\\to0$. So $\\sum a_n$ converges (the partial sums stabilise: $a_2\\approx1.785$, $a_3\\approx1.88$, $a_4\\approx1.41$, $a_5\\approx0.82,\\dots$).", "Computation problems 11, Q11", "src")
    note("Computation problems 11, Q11", "The printed key says the series DIVERGES. With $a_{n+1}=\\frac{1+\\tan^{-1}n}{n}a_n$ the ratio tends to $0$, so the Ratio Test gives convergence (partial sums computed numerically stabilise). The key entry appears to be mistaken (a version with $a_{n+1}=\\frac{n}{1+\\tan^{-1}n}a_n$ would diverge).")
    # ---- alternating series (Tutorial 12 Q1-Q2)
    B.mcq(ch, "Alternating series", 2, "The series $\\displaystyle\\sum_{n=1}^\\infty(-1)^{n+1}\\left(\\dfrac{n}{10}\\right)^n$", "diverges (the terms do not tend to $0$)", ["converges by the Alternating Series Test", "converges absolutely", "converges conditionally"],
          "$\\left(\\frac n{10}\\right)^n\\to\\infty$ (it exceeds $1$ once $n>10$), so $a_n\\not\\to0$ and the series diverges; the AST needs $b_n\\to0$.", "Tutorial 12, Q1(a)", "src")
    B.mcq(ch, "Alternating series", 2, "The series $\\displaystyle\\sum_{n=1}^\\infty(-1)^{n+1}\\dfrac{3\\sqrt{n+1}}{\\sqrt n+1}$", "diverges (the terms tend to $\\pm3$, not $0$)", ["converges conditionally", "converges absolutely", "converges to $0$"],
          "$\\frac{3\\sqrt{n+1}}{\\sqrt n+1}\\to3$, so $a_n$ oscillates between about $\\pm3$: the $n$-th term test gives divergence.", "Tutorial 12, Q1(b)", "src")
    B.mcq(ch, "Alternating series", 3, "$\\displaystyle\\sum_{n=1}^\\infty\\dfrac{(-2)^{n+1}}{n+5^n}$", "converges absolutely", ["converges conditionally only", "diverges", "converges to $0$ but not absolutely"],
          "$\\left|\\frac{(-2)^{n+1}}{n+5^n}\\right|\\le2\\left(\\frac25\\right)^n$, a convergent geometric series: comparison test ⇒ absolute convergence.", "Tutorial 12, Q2(a)", "src")
    b2 = lambda m: np.log(m) / (m - np.log(m))
    mm = np.arange(5, 3000, dtype=np.float64); assert np.all(np.diff(b2(mm)) < 0)
    S_abs1, S_abs2, _ = partial_sums(b2, 10 ** 4, 10 ** 6, start=2); assert S_abs2 - S_abs1 > 1
    B.mcq(ch, "Alternating series", 3, "$\\displaystyle\\sum_{n=1}^\\infty(-1)^n\\dfrac{\\ln n}{n-\\ln n}$", "converges conditionally (not absolutely)", ["converges absolutely", "diverges", "diverges because the terms oscillate"],
          "$b_n=\\frac{\\ln n}{n-\\ln n}\\to0$ and is eventually decreasing, so the series converges by the AST. But $\\sum b_n$ diverges (compare with $\\frac{1}{n}$: $b_n\\ge\\frac1n$ for $n\\ge3$), so the convergence is conditional.", "Tutorial 12, Q2(b)", "src")
    B.mcq(ch, "Alternating series", 1, "The Alternating Series Test for $\\sum(-1)^{n}b_n$ with $b_n>0$ requires", "$b_n$ decreasing (eventually) and $b_n\\to0$", ["$b_n\\to0$ only", "$b_n$ increasing", "$\\sum b_n$ converges"], "Both conditions are needed (e.g. $b_n=\\frac{1}{n}$ for odd $n$ and $\\frac1{n^2}$ for even $n$ shows 'only $b_n\\to0$' is not enough).", "Lecture 11", "concept")
    B.mcq(ch, "Alternating series", 2, "For a convergent alternating series with decreasing $b_n\\to0$, the error after $N$ terms satisfies", "$|R_N|\\le b_{N+1}$", ["$|R_N|\\le b_N$", "$|R_N|\\ge b_{N+1}$", "$|R_N|=b_{N+1}$"], "The remainder is bounded by the first omitted term.", "Lecture 11", "concept")
    B.mcq(ch, "Convergence tests", 2, "Which test is the most direct for $\\displaystyle\\sum\\dfrac{n!}{10^n}$?", "the Ratio Test", ["the Integral Test", "the Alternating Series Test", "the Comparison Test with $\\frac{1}{n^2}$"], "Factorials versus exponentials are exactly what the Ratio Test handles.", "Lecture 11", "concept")
    B.mcq(ch, "Convergence tests", 2, "Which test is the most direct for $\\displaystyle\\sum\\dfrac{n^n}{(2^n)^2}$?", "the Root Test", ["the Alternating Series Test", "the Integral Test", "the Limit Comparison Test with $\\frac1n$"], "$n$-th powers inside: $\\sqrt[n]{a_n}$ simplifies at once.", "Lecture 11", "concept")
    B.mcq(ch, "Convergence tests", 1, "If $\\sum|a_n|$ converges then $\\sum a_n$", "converges (absolute convergence implies convergence)", ["may diverge", "converges to $0$", "converges only if $a_n>0$"], "Absolute convergence is the stronger property.", "Lecture 11", "concept")
    B.mcq(ch, "Convergence tests", 1, "If $\\displaystyle\\lim a_n\\neq0$ then $\\sum a_n$", "diverges", ["converges", "may converge or diverge", "converges conditionally"], "The $n$-th term test (divergence test). The converse is false: $\\sum\\frac1n$ diverges although $\\frac1n\\to0$.", "Lecture 11", "concept")
    # ---- power series: radius and interval
    B.mcq(ch, "Power series", 3, "$\\displaystyle\\sum_{n=1}^\\infty\\dfrac{(x-1)^n}{\\sqrt n}$ has radius $R$ and interval of convergence", "$R=1$, interval $[0,2)$", ["$R=1$, interval $(0,2)$", "$R=1$, interval $[0,2]$", "$R=2$, interval $(-1,3)$"],
          "Ratio test: $|x-1|\\lim\\sqrt{\\frac n{n+1}}=|x-1|<1$. At $x=2$: $\\sum\\frac1{\\sqrt n}$ diverges; at $x=0$: $\\sum\\frac{(-1)^n}{\\sqrt n}$ converges (AST). So $[0,2)$: absolutely for $0<x<2$, conditionally at $x=0$.", "Tutorial 12, Q3(a)", "src")
    assert sp.limit(sp.sqrt(n / (n + 1)), n, oo) == 1
    B.mcq(ch, "Power series", 3, "$\\displaystyle\\sum_{n=1}^\\infty n^nx^n$ converges", "only at $x=0$ ($R=0$)", ["for $|x|<1$", "for all real $x$", "for $|x|<\\frac1e$"],
          "Root test: $\\sqrt[n]{|n^nx^n|}=n|x|\\to\\infty$ for every $x\\ne0$.", "Tutorial 12, Q3(b)", "src")
    B.mcq(ch, "Power series", 3, "For $\\displaystyle\\sum_{n=1}^\\infty(-2)^n(n+1)(x-1)^n$ the radius of convergence is $R=$ and it converges absolutely on", "$R=\\frac12$; $\\frac12<x<\\frac32$ (and nowhere conditionally)", ["$R=2$; $-1<x<3$", "$R=\\frac12$; $\\frac12\\le x\\le\\frac32$", "$R=1$; $0<x<2$"],
          "$\\left|\\frac{a_{n+1}}{a_n}\\right|=2|x-1|\\frac{n+2}{n+1}\\to2|x-1|<1\\iff|x-1|<\\frac12$. At the ends $|x-1|=\\frac12$ the terms $(n+1)(\\pm1)^n$ do not tend to $0$: divergence.", "Computation problems 12, Q1", "src")
    B.mcq(ch, "Power series", 3, "The radius of convergence of $\\displaystyle\\sum_{n=1}^\\infty\\dfrac{n!\\,x^n}{3\\cdot6\\cdot9\\cdots(3n)}$ is", "$3$", ["$1$", "$\\frac13$", "$\\infty$"], "$\\left|\\frac{a_{n+1}}{a_n}\\right|=\\frac{(n+1)|x|}{3(n+1)}=\\frac{|x|}{3}<1\\iff|x|<3$.", "Computation problems 12, Q2", "src")
    B.mcq(ch, "Power series", 3, "$\\displaystyle\\sum_{n=1}^\\infty\\dfrac{n\\,x^n}{(n+1)(2x+1)^n}$ converges absolutely for", "$x<-1$ or $x>-\\frac13$", ["$-1<x<-\\frac13$", "$|x|<1$", "$x>-1$"],
          "$\\sqrt[n]{|a_n|}\\to\\left|\\frac{x}{2x+1}\\right|<1\\iff x^2<(2x+1)^2\\iff(3x+1)(x+1)>0$, i.e. $x<-1$ or $x>-\\frac13$ (and $x\\ne-\\frac12$).", "Computation problems 12, Q7", "src")
    B.mcq(ch, "Power series", 2, "$\\displaystyle\\sum_{n=0}^\\infty\\dfrac{x^n}{n!}$ has radius of convergence", "$\\infty$", ["$1$", "$e$", "$0$"], "$\\frac{|x|}{n+1}\\to0<1$ for every $x$.", "Lecture 12", "concept")
    B.mcq(ch, "Power series", 2, "$\\displaystyle\\sum_{n=1}^\\infty\\dfrac{x^n}{n}$ converges for", "$-1\\le x<1$", ["$-1<x<1$", "$-1\\le x\\le1$", "$|x|\\le\\frac12$"], "$R=1$; $x=1$ is the harmonic series (diverges) and $x=-1$ the alternating harmonic series (converges).", "Lecture 12", "concept")
    # ---- Taylor / Maclaurin
    B.mcq(ch, "Taylor and Maclaurin series", 3, "In the Taylor polynomial of $f(x)=\\sin x$ about $a=\\frac\\pi4$, the coefficient of $\\left(x-\\frac\\pi4\\right)^2$ is", "$-\\dfrac{\\sqrt2}{4}$", ["$-\\dfrac{\\sqrt2}{2}$", "$\\dfrac{\\sqrt2}{4}$", "$-\\dfrac{\\sqrt2}{8}$"],
          "$c_2=\\frac{f''(\\pi/4)}{2!}=\\frac{-\\sin(\\pi/4)}{2}=-\\frac{\\sqrt2}{4}$. The full cubic is $\\frac{\\sqrt2}{2}\\left[1+u-\\frac{u^2}2-\\frac{u^3}6\\right]$, $u=x-\\frac\\pi4$.", "Tutorial 12, Q4", "src")
    assert sp.simplify(sp.diff(sp.sin(x), x, 2).subs(x, sp.pi / 4) / 2 + sp.sqrt(2) / 4) == 0
    ser = sp.series(sp.exp(x) + 1 / (1 + x), x, 0, 5).removeO()
    co = [ser.coeff(x, k) for k in range(5)]
    assert co == [2, 0, sp.Rational(3, 2), sp.Rational(-5, 6), sp.Rational(25, 24)]
    B.mcq(ch, "Taylor and Maclaurin series", 2, "The Maclaurin series of $f(x)=e^x+\\dfrac{1}{1+x}$ begins", "$2+0\\cdot x+\\frac32x^2-\\frac56x^3+\\frac{25}{24}x^4+\\cdots$", ["$2+2x+\\frac12x^2+\\frac76x^3+\\cdots$", "$2+0\\cdot x+\\frac12x^2-\\frac56x^3+\\cdots$", "$1+0\\cdot x+\\frac32x^2+\\frac76x^3+\\cdots$"],
          "$e^x=\\sum\\frac{x^n}{n!}$ and $\\frac1{1+x}=\\sum(-1)^nx^n$; the coefficient of $x^n$ is $\\frac1{n!}+(-1)^n$: $2,0,\\frac32,-\\frac56,\\frac{25}{24}$.", "Tutorial 12, Q5", "src")
    pb = sp.Symbol("p", positive=True)
    B.mcq(ch, "Taylor and Maclaurin series", 3, "The Maclaurin series of $\\ln\\dfrac{1+x}{1-x}$ ($|x|<1$) is", "$2\\left(x+\\dfrac{x^3}{3}+\\dfrac{x^5}{5}+\\cdots\\right)$", ["$x+\\dfrac{x^3}{3}+\\dfrac{x^5}{5}+\\cdots$", "$2\\left(x-\\dfrac{x^3}{3}+\\dfrac{x^5}{5}-\\cdots\\right)$", "$2\\left(x+\\dfrac{x^2}{2}+\\dfrac{x^3}{3}+\\cdots\\right)$"],
          "$\\ln(1+x)=x-\\frac{x^2}2+\\frac{x^3}3-\\cdots$ and $\\ln(1-x)=-x-\\frac{x^2}2-\\frac{x^3}3-\\cdots$; subtracting, the even powers cancel and the odd ones double.", "Tutorial 12, Q8", "src")
    assert sp.series(sp.log((1 + x) / (1 - x)), x, 0, 6).removeO() == 2 * (x + x ** 3 / 3 + x ** 5 / 5)
    B.mcq(ch, "Taylor and Maclaurin series", 2, "The Maclaurin series of $5\\cos\\pi x$ is", "$\\displaystyle\\sum_{k=0}^\\infty\\dfrac{5(-1)^k(\\pi x)^{2k}}{(2k)!}$", ["$\\displaystyle\\sum_{k=0}^\\infty\\dfrac{5(-1)^k(\\pi x)^{2k+1}}{(2k+1)!}$", "$\\displaystyle\\sum_{k=0}^\\infty\\dfrac{5(\\pi x)^{2k}}{(2k)!}$", "$\\displaystyle\\sum_{k=0}^\\infty\\dfrac{(-1)^k(5\\pi x)^{2k}}{(2k)!}$"],
          "Substitute $\\pi x$ into $\\cos u=\\sum\\frac{(-1)^ku^{2k}}{(2k)!}$ and multiply by $5$.", "Computation problems 12, Q3", "src")
    B.mcq(ch, "Taylor and Maclaurin series", 3, "The Taylor series of $f(x)=2^x$ about $x=1$ is", "$\\displaystyle\\sum_{n=0}^\\infty\\dfrac{2(\\ln2)^n}{n!}(x-1)^n$", ["$\\displaystyle\\sum_{n=0}^\\infty\\dfrac{(\\ln2)^n}{n!}(x-1)^n$", "$\\displaystyle\\sum_{n=0}^\\infty\\dfrac{2^n}{n!}(x-1)^n$", "$\\displaystyle\\sum_{n=0}^\\infty\\dfrac{2\\ln2}{n!}(x-1)^n$"],
          "$f^{(n)}(x)=(\\ln2)^n2^x$, so $f^{(n)}(1)=2(\\ln2)^n$ and $c_n=\\frac{f^{(n)}(1)}{n!}$.", "Computation problems 12, Q4", "src")
    B.mcq(ch, "Taylor and Maclaurin series", 3, "Differentiating $\\frac{1}{1-x^2}=\\sum_{n\\ge0}x^{2n}$ term by term, $\\dfrac{2x}{(1-x^2)^2}=$", "$\\displaystyle\\sum_{n=1}^\\infty2n\\,x^{2n-1}$", ["$\\displaystyle\\sum_{n=1}^\\infty n\\,x^{2n-1}$", "$\\displaystyle\\sum_{n=0}^\\infty2n\\,x^{2n}$", "$\\displaystyle\\sum_{n=1}^\\infty2\\,x^{2n-1}$"],
          "$\\frac{d}{dx}\\frac{1}{1-x^2}=\\frac{2x}{(1-x^2)^2}$ and $\\frac{d}{dx}x^{2n}=2nx^{2n-1}$.", "Computation problems 12, Q5", "src")
    # Remainders and error estimates
    nmin = None
    for N in range(1, 15):
        if 0.1 ** (N + 1) / (N + 1) < 1e-8:
            nmin = N; break
    assert nmin == 7
    note("Tutorial 12, Q9", "The key gives $8$ (counting the zero constant term of $\\ln(1+x)$ as a term). With the Lagrange bound $|R_n(0.1)|\\le\\frac{0.1^{n+1}}{n+1}$ the polynomial $P_7$ already works ($1.25\\times10^{-9}<10^{-8}$), i.e. $7$ non-zero terms $x-\\frac{x^2}2+\\cdots+\\frac{x^7}7$.")
    B.mcq(ch, "Taylor and Maclaurin series", 3, "How many non-zero terms of the Maclaurin series of $\\ln(1+x)$ guarantee $\\ln1.1$ to within $10^{-8}$ (using $|R_n(x)|\\le\\frac{|x|^{n+1}}{n+1}$)?", "$7$ (up to $x^7/7$)", ["$6$", "$8$", "$5$"],
          "Need $\\frac{0.1^{n+1}}{n+1}<10^{-8}$: $n=6$ gives $\\frac{10^{-7}}{7}\\approx1.4\\times10^{-8}$ (too big), $n=7$ gives $\\frac{10^{-8}}{8}=1.25\\times10^{-9}$. (The printed key '8' counts the zero constant term as a term.)", "Tutorial 12, Q9", "src")
    err6 = sp.Rational(1, 10) * sp.Rational(1, 10) ** 4 / 24
    B.mcq(ch, "Taylor and Maclaurin series", 3, "Estimate the error when $P_3(x)=x-\\frac{x^3}{6}$ approximates $\\sin x$ at $x=0.1$ (Lagrange bound with $|f^{(4)}(c)|=|\\sin c|\\le0.1$).", "$|R_3(0.1)|\\le\\dfrac{0.1\\cdot0.1^4}{24}\\approx4.2\\times10^{-7}$", ["$|R_3(0.1)|\\le\\dfrac{0.1^4}{24}\\approx4.2\\times10^{-6}$ is the only available bound", "$|R_3(0.1)|\\le4.2\\times10^{-9}$", "$|R_3(0.1)|\\le\\dfrac{0.1^3}{6}\\approx1.7\\times10^{-4}$"],
          "$R_3(x)=\\frac{f^{(4)}(c)}{4!}x^4$ with $|f^{(4)}(c)|=|\\sin c|\\le|c|\\le0.1$: $|R_3(0.1)|\\le\\frac{0.1\\cdot10^{-4}}{24}=4.2\\times10^{-7}$ (the cruder bound with $|\\sin c|\\le1$ is $4.2\\times10^{-6}$; both are valid bounds, the first is sharper).", "Tutorial 12, Q6", "src")
    B.mcq(ch, "Taylor and Maclaurin series", 3, "To expand $f(x)=\\cos x$ for $x$ near $69$, which centre makes the Taylor series most convenient?", "$a=22\\pi\\approx69.115$ (then $\\cos x=1-\\frac{(x-22\\pi)^2}{2}+\\frac{(x-22\\pi)^4}{24}-\\cdots$)", ["$a=0$ (Maclaurin series)", "$a=69$", "$a=\\frac\\pi2$"],
          "$22\\pi$ is a multiple of $2\\pi$ very close to $69$, so $\\cos x=\\cos(x-22\\pi)$ and the powers $(x-22\\pi)^k$ are tiny: the first few terms are very accurate.", "Tutorial 12, Q10", "src")
    B.mcq(ch, "Taylor and Maclaurin series", 1, "The Taylor polynomial of degree $n$ of $f$ about $a$ is $\\sum_{k=0}^{n}$", "$\\dfrac{f^{(k)}(a)}{k!}(x-a)^k$", ["$f^{(k)}(a)\\,(x-a)^k$", "$\\dfrac{f^{(k)}(x)}{k!}(x-a)^k$", "$\\dfrac{f^{(k)}(a)}{k}(x-a)^k$"], "Coefficient $=f^{(k)}(a)/k!$.", "Lecture 12", "concept")
    B.mcq(ch, "Taylor and Maclaurin series", 1, "The Maclaurin series of $e^{x}$ is", "$\\displaystyle\\sum_{n=0}^\\infty\\dfrac{x^n}{n!}$", ["$\\displaystyle\\sum_{n=0}^\\infty x^n$", "$\\displaystyle\\sum_{n=1}^\\infty\\dfrac{x^n}{n!}$", "$\\displaystyle\\sum_{n=0}^\\infty\\dfrac{(-1)^nx^n}{n!}$"], "$f^{(n)}(0)=1$ for every $n$.", "Lecture 12", "concept")
    B.mcq(ch, "Taylor and Maclaurin series", 2, "The Maclaurin series of $\\dfrac{1}{1-x}$ is $\\sum x^n$ and converges for", "$|x|<1$", ["$|x|\\le1$", "all $x$", "$x>0$"], "A geometric series with ratio $x$.", "Lecture 12", "concept")
    B.mcq(ch, "Taylor and Maclaurin series", 2, "The Maclaurin series of $\\sin x$ contains only", "odd powers of $x$ (because $\\sin$ is an odd function)", ["even powers of $x$", "all powers of $x$", "powers $x^{3k}$"], "$\\sin x=x-\\frac{x^3}{3!}+\\frac{x^5}{5!}-\\cdots$", "Lecture 12", "concept")
    series_behaves(lambda m: 1 / m ** 2, "conv")
