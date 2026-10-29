# -*- coding: utf-8 -*-
"""Calculus I chapters 3-4: applications of derivatives, antiderivatives, definite integrals and their applications."""
import math
import sympy as sp
from qlib import tex, uniq_by_text, near_numbers, R, note
from cal_common import *
from gen_cal1 import limq, d_wrongs

oo = sp.oo
tt = sp.Symbol("t", real=True)

def crit_info(f, lo=None, hi=None, var=x):
    """Critical points (where f'=0) and the sign pattern, for a polynomial/smooth f."""
    return sorted(sp.solve(sp.diff(f, var), var), key=lambda z: float(sp.N(z)))

def newton(f, x0, steps, var=x):
    xs = [sp.nsimplify(x0)]
    for _ in range(steps):
        cur = xs[-1]
        xs.append(sp.nsimplify(cur - f.subs(var, cur) / sp.diff(f, var).subs(var, cur)))
    return xs

def fl(v, nd=4):
    return "$%.*f$" % (nd, float(v))

# ============================================================================== CHAPTER 3
def ch3(B):
    ch = "c3"; rng = B.rng
    # ---- absolute extrema on closed intervals (Computation #5 Q1-Q2)
    f1 = x ** 2 - 1
    mc_val(B, ch, "Extreme values", 1, "Find the absolute maximum value of $f(x)=x^2-1$ on $[-1,2]$.", 3, [0, -1, 2, 1], "Compare $f$ at the critical point $x=0$ ($f=-1$) and the endpoints: $f(-1)=0$, $f(2)=3$. Maximum $=3$ at $x=2$.", "Computation problems 5, Q1", "src")
    mc_val(B, ch, "Extreme values", 1, "Find the absolute minimum value of $f(x)=x^2-1$ on $[-1,2]$.", -1, [0, 3, 1, -3], "$f'(x)=2x=0$ at $x=0$ with $f(0)=-1$; endpoints give $0$ and $3$. Minimum $=-1$ at $x=0$.", "Computation problems 5, Q1", "src")
    g2 = sp.sqrt(4 - x ** 2)
    mc_val(B, ch, "Extreme values", 2, "Find the absolute maximum of $g(x)=\\sqrt{4-x^2}$ on $[-2,1]$.", 2, [1, sp.sqrt(3), 0, 4], "$g'(x)=-\\frac{x}{\\sqrt{4-x^2}}=0$ at $x=0$ where $g=2$; endpoints: $g(-2)=0$, $g(1)=\\sqrt3$. Maximum $=2$.", "Computation problems 5, Q2", "src")
    B.mcq(ch, "Extreme values", 2, "Where does $g(x)=\\sqrt{4-x^2}$ attain its absolute minimum on $[-2,1]$?", "at $x=-2$ (value $0$)", ["at $x=0$", "at $x=1$", "at $x=2$"], "The values are $g(-2)=0$, $g(0)=2$, $g(1)=\\sqrt3$; the smallest is at the left endpoint.", "Computation problems 5, Q2", "src")
    B.mcq(ch, "Extreme values", 2, "$y=\\dfrac{1}{\\sqrt[3]{1-x^2}}$ on its domain has", "no absolute maximum and no absolute minimum", ["an absolute maximum $1$ at $x=0$ only", "an absolute minimum $1$ at $x=0$ only", "both an absolute maximum and minimum"],
          "Near $x=\\pm1$ the function is unbounded in both directions: $\\sqrt[3]{1-x^2}$ takes any small positive or negative values, so $y\\to\\pm\\infty$.", "Computation problems 5, Q4", "src")
    B.mcq(ch, "Extreme values", 1, "The Extreme Value Theorem guarantees an absolute max and min if $f$ is", "continuous on a closed bounded interval $[a,b]$", ["differentiable on $(a,b)$ only", "increasing on $(a,b)$", "defined on an open interval"], "Both continuity and a closed bounded interval are needed.", "Lecture 5", "concept")
    B.mcq(ch, "Extreme values", 1, "Fermat's theorem: if $f$ has a local extremum at an interior point $c$ and $f'(c)$ exists, then", "$f'(c)=0$", ["$f''(c)=0$", "$f(c)=0$", "$f'(c)>0$"], "The converse is false: $f(x)=x^3$ has $f'(0)=0$ but no extremum.", "Lecture 5", "concept")
    # ---- first derivative test
    gt = -t ** 2 - 3 * t + 3
    mc_val(B, ch, "First derivative test", 2, "$g(t)=-t^2-3t+3$ has a local maximum value of", sp.Rational(21, 4), [3, sp.Rational(9, 4), sp.Rational(-3, 2), sp.Rational(15, 4)], "$g'(t)=-2t-3=0$ at $t=-\\frac32$; $g'$ changes from $+$ to $-$, so it is a maximum: $g(-\\frac32)=-\\frac94+\\frac92+3=\\frac{21}{4}$.", "Computation problems 5, Q5", "src")
    ft = 3 * th ** 2 - 4 * th ** 3
    cps = sp.solve(sp.diff(ft, th), th); assert sorted(cps) == [0, sp.Rational(1, 2)]
    B.mcq(ch, "First derivative test", 2, "For $f(\\theta)=3\\theta^2-4\\theta^3$, which statement is true?", "local minimum $0$ at $\\theta=0$ and local maximum $\\frac14$ at $\\theta=\\frac12$",
          ["local maximum $0$ at $\\theta=0$ and local minimum $\\frac14$ at $\\theta=\\frac12$", "local minimum $0$ at $\\theta=0$ and local maximum $\\frac12$ at $\\theta=\\frac14$", "no local extrema"],
          "$f'=6\\theta-12\\theta^2=6\\theta(1-2\\theta)$. $f'<0$ for $\\theta<0$, $>0$ on $(0,\\frac12)$, $<0$ after $\\frac12$: min at $0$ ($f=0$), max at $\\frac12$ ($f=\\frac34-\\frac12=\\frac14$).", "Computation problems 5, Q6", "src")
    hx = sp.real_root(x, 3) * (x ** 2 - 4)
    B.mcq(ch, "First derivative test", 3, "$h(x)=\\sqrt[3]{x}\\,(x^2-4)$ has critical points where $h'(x)=\\frac{7x^2-4}{3x^{2/3}}$ is $0$ or undefined, namely", "$x=0$ (undefined) and $x=\\pm\\frac{2}{\\sqrt7}$; the local extrema are only at $\\pm\\frac{2}{\\sqrt7}$",
          ["$x=\\pm\\frac{2}{\\sqrt7}$ only", "$x=0$ and $x=\\pm2$", "$x=0$ is a local maximum and $x=\\pm\\frac2{\\sqrt7}$ are minima"],
          "$h=x^{7/3}-4x^{1/3}$, $h'=\\frac73x^{4/3}-\\frac43x^{-2/3}=\\frac{7x^2-4}{3x^{2/3}}$. At $x=0$, $h'$ is undefined but $h'$ does not change sign there (the factor $x^{2/3}>0$), so no extremum.", "Computation problems 5, Q7", "src")
    ftt = 12 * t - t ** 3
    B.mcq(ch, "First derivative test", 3, "For $f(t)=12t-t^3$ on $-3\\le t<\\infty$: which statement is correct?", "local max $16$ at $t=2$ (also the absolute max), local min $-16$ at $t=-2$, local max $-9$ at the endpoint $t=-3$, no absolute minimum",
          ["local max $16$ at $t=-2$ and local min $-16$ at $t=2$", "absolute minimum $-16$ at $t=-2$", "no local extrema, since $f$ is a cubic"],
          "$f'=12-3t^2=0$ at $t=\\pm2$; $f(2)=16$, $f(-2)=-16$, $f(-3)=-9$. $f$ decreases from the endpoint $-3$ to $-2$, so the endpoint is a local max; $f\\to-\\infty$ as $t\\to\\infty$, so there is no absolute minimum.", "Tutorial 5, Q8", "src")
    assert (12 * 2 - 8, 12 * -2 + 8, 12 * -3 + 27) == (16, -16, -9)
    # ---- concavity (Computation #5 Q8, Q10; Tutorial 5 Q9-Q10)
    y8 = x ** 3 / 3 - x ** 2 / 2 - 2 * x + sp.Rational(1, 3)
    assert sp.solve(sp.diff(y8, x, 2), x) == [sp.Rational(1, 2)] and sorted(sp.solve(sp.diff(y8, x), x)) == [-1, 2]
    B.mcq(ch, "Concavity and inflection", 2, "For $y=\\frac{x^3}{3}-\\frac{x^2}{2}-2x+\\frac13$, the inflection point is at", "$x=\\frac12$", ["$x=-1$", "$x=2$", "$x=0$"], "$y''=2x-1=0$ at $x=\\frac12$ and $y''$ changes sign there ($x=-1,2$ are the critical points: a local max and min).", "Computation problems 5, Q8", "src")
    B.mcq(ch, "Concavity and inflection", 2, "For the same $y=\\frac{x^3}{3}-\\frac{x^2}{2}-2x+\\frac13$: local maximum at … and local minimum at …", "local max at $x=-1$, local min at $x=2$", ["local max at $x=2$, local min at $x=-1$", "local max at $x=\\frac12$, no minimum", "local min at $x=-1$ and $x=2$"],
          "$y'=x^2-x-2=(x-2)(x+1)$; $y''(-1)=-3<0$ (max) and $y''(2)=3>0$ (min).", "Computation problems 5, Q8", "src")
    yb = x + sp.sin(2 * x)
    infl = [sp.nsimplify(z) for z in (0, sp.pi / 2, -sp.pi / 2)]
    assert all(sp.simplify(sp.diff(yb, x, 2).subs(x, z)) == 0 for z in infl)
    B.mcq(ch, "Concavity and inflection", 3, "For $y=x+\\sin2x$ on $[-\\frac{2\\pi}{3},\\frac{2\\pi}{3}]$ the inflection points are at", "$x=0$ and $x=\\pm\\frac{\\pi}{2}$", ["$x=\\pm\\frac{\\pi}{3}$ only", "$x=0$ only", "$x=\\pm\\frac{\\pi}{4}$ and $x=0$"],
          "$y''=-4\\sin2x=0\\Rightarrow2x=k\\pi\\Rightarrow x=0,\\pm\\frac\\pi2$ (the points $x=\\pm\\frac\\pi3$ are the local extrema, where $y'=1+2\\cos2x=0$).", "Computation problems 5, Q10", "src")
    yv = sp.simplify(yb.subs(x, sp.pi / 3)); yv2 = sp.simplify(yb.subs(x, -sp.pi / 3))
    d_left = sp.N(sp.diff(yb, x).subs(x, -sp.Rational(1, 2) * sp.pi)); d_mid = sp.N(sp.diff(yb, x).subs(x, 0)); d_right = sp.N(sp.diff(yb, x).subs(x, sp.Rational(1, 2) * sp.pi))
    assert d_left < 0 < d_mid and d_right < 0
    B.mcq(ch, "Concavity and inflection", 3, "For $y=x+\\sin2x$ on $[-\\frac{2\\pi}{3},\\frac{2\\pi}{3}]$, which statement about the critical points $x=\\pm\\frac\\pi3$ is right?",
          "local minimum at $x=-\\frac\\pi3$ (value $%s$) and local maximum at $x=\\frac\\pi3$ (value $%s$)" % (tex(yv2), tex(yv)),
          ["local maximum at $x=-\\frac\\pi3$ and local minimum at $x=\\frac\\pi3$", "both are local maxima", "both are local minima"],
          "$y'=1+2\\cos2x$: $y'<0$ on $(-\\frac{2\\pi}3,-\\frac\\pi3)$, $y'>0$ on $(-\\frac\\pi3,\\frac\\pi3)$, $y'<0$ on $(\\frac\\pi3,\\frac{2\\pi}3)$. So $x=-\\frac\\pi3$ is a minimum and $x=\\frac\\pi3$ a maximum, with $y(\\pm\\frac\\pi3)=\\pm(\\frac\\pi3+\\frac{\\sqrt3}2)$.", "Computation problems 5, Q10", "src")
    note("Computation problems 5, Q10", "The printed key says 'local maximum $y(-\\pi/3)=-\\pi/3-\\sqrt3/2$, local minimum $y(\\pi/3)=\\pi/3+\\sqrt3/2$'. Since $y(-\\pi/3)<y(\\pi/3)$ this is impossible for a max/min pair at those points: the sign of $y'$ shows a local MINIMUM at $-\\pi/3$ and a local MAXIMUM at $\\pi/3$. We follow the computation.")
    mc_val(B, ch, "Concavity and inflection", 3, "For $y=x^3+bx^2+cx+d$ to have a point of inflection at $x=1$, $b$ must equal", -3, [3, -1, 1, 0], "$y''=6x+2b$; $y''(1)=0\\Rightarrow b=-3$ (and $y''$ changes sign there).", "Tutorial 5, Q9", "src")
    B.mcq(ch, "Concavity and inflection", 2, "A quadratic curve $y=ax^2+bx+c$ ($a\\ne0$) has", "no inflection point ($y''=2a$ never changes sign)", ["exactly one inflection point at its vertex", "two inflection points", "an inflection point at $x=-\\frac{b}{2a}$"], "$y''=2a$ is a non-zero constant, so the concavity never changes.", "Tutorial 5, Q10", "src")
    # ---- MVT / Rolle
    B.mcq(ch, "Mean Value Theorem", 2, "Does $f(x)=\\sqrt{x(1-x)}$ satisfy the hypotheses of the MVT on $[0,1]$?", "Yes: continuous on $[0,1]$ and differentiable on $(0,1)$ (the infinite slopes at the endpoints do not matter)",
          ["No: $f$ is not differentiable at $0$ and $1$, so the MVT fails", "No: $f$ is not continuous on $[0,1]$", "Yes, because $f(0)=f(1)$ is the only requirement"],
          "The MVT needs continuity on $[a,b]$ and differentiability only on the open interval $(a,b)$.", "Tutorial 5, Q2", "src")
    mc_val(B, ch, "Mean Value Theorem", 2, "A thermometer rises from $-19$ °C to $100$ °C in $14$ s. By the MVT, at some instant the temperature was rising at … °C/s", sp.Rational(17, 2), [sp.Rational(119, 7), 7, 14, sp.Rational(81, 14)], "Average rate $=\\frac{100-(-19)}{14}=\\frac{119}{14}=8.5$ °C/s; the MVT guarantees a time with exactly this instantaneous rate.", "Tutorial 5, Q7", "src")
    for f_, a_, b_ in [(x ** 2, 1, 3), (x ** 3, 0, 2), (x ** 2 - 4 * x + 1, 0, 3)]:
        cc = [z for z in sp.solve(sp.Eq(sp.diff(f_, x), (f_.subs(x, b_) - f_.subs(x, a_)) / (b_ - a_)), x) if a_ < z < b_]
        assert len(cc) == 1
        mc_val(B, ch, "Mean Value Theorem", 2, "Find the number $c\\in(%d,%d)$ guaranteed by the MVT for $f(x)=%s$." % (a_, b_, tex(f_)), cc[0],
               [sp.Rational(a_ + b_, 2), a_, b_, sp.nsimplify(cc[0] + 1)], "Solve $f'(c)=\\frac{f(%d)-f(%d)}{%d-%d}=%s$: $c=%s$." % (b_, a_, b_, a_, tex((f_.subs(x, b_) - f_.subs(x, a_)) / (b_ - a_)), tex(cc[0])), "Generated (Lecture 5: MVT)", "gen")
    B.mcq(ch, "Mean Value Theorem", 2, "Rolle's Theorem requires $f$ continuous on $[a,b]$, differentiable on $(a,b)$ and …", "$f(a)=f(b)$", ["$f(a)=0$", "$f'(a)=f'(b)$", "$f$ increasing"], "Then $f'(c)=0$ for some $c\\in(a,b)$.", "Lecture 5", "concept")
    B.mcq(ch, "Mean Value Theorem", 3, "To show $f(x)=x^4+3x+1$ has exactly one zero in $[-2,-1]$ one uses", "the IVT ($f(-2)=11>0$, $f(-1)=-1<0$) for existence and $f'(x)=4x^3+3<0$ on $[-2,-1]$ (Rolle) for uniqueness",
          ["Rolle's theorem alone", "the IVT alone", "the Squeeze theorem"], "A sign change gives a zero; if there were two zeros, Rolle would give a zero of $f'$ between them, but $f'<0$ throughout.", "Tutorial 5, Q6(a)", "src")
    assert (-2) ** 4 + 3 * (-2) + 1 == 11 and (-1) ** 4 + 3 * (-1) + 1 == -1
    # ---- asymptotes
    fa = (2 * x ** 2 + 3) / (x - 1)
    q_, r_ = sp.div(sp.Poly(2 * x ** 2 + 3, x), sp.Poly(x - 1, x)); assert q_.as_expr() == 2 * x + 2
    B.mcq(ch, "Asymptotes", 2, "The graph of $f(x)=\\dfrac{2x^2+3}{x-1}$ has", "the vertical asymptote $x=1$ and the oblique asymptote $y=2x+2$ (no horizontal asymptote)",
          ["the vertical asymptote $x=1$ and the horizontal asymptote $y=2$", "only the oblique asymptote $y=2x$", "the vertical asymptote $x=1$ and the oblique asymptote $y=2x-2$"],
          "Long division: $\\frac{2x^2+3}{x-1}=2x+2+\\frac{5}{x-1}$. The remainder term vanishes at infinity ⇒ oblique asymptote $y=2x+2$; the denominator vanishes at $x=1$ (numerator $5\\ne0$) ⇒ vertical asymptote.", "Generated (Lecture 5: asymptotes)", "gen")
    fb = (3 * x ** 2 - 1) / (x ** 2 + 2)
    assert sp.limit(fb, x, oo) == 3
    B.mcq(ch, "Asymptotes", 1, "The horizontal asymptote of $f(x)=\\dfrac{3x^2-1}{x^2+2}$ is", "$y=3$", ["$y=0$", "$y=-\\tfrac12$", "there is none"], "Equal degrees: $\\lim_{x\\to\\pm\\infty}f=\\frac31=3$.", "Generated (Lecture 5)", "gen")
    # ---- optimization (Tutorial 6, Computation #6, Mock Test)
    mc_val(B, ch, "Optimization", 2, "Among rectangles of area $16$ in², the smallest perimeter is (in inches)", 16, [8, 32, 20, 4], "$P=2(x+\\frac{16}{x})$; $P'=0$ at $x=4$ (a square $4\\times4$): $P=16$.", "Tutorial 6, Q1", "src")
    A_ = sp.Symbol("A"); xx = sp.Symbol("x", positive=True)
    area = 2 * xx * (1 - xx); xs = sp.solve(sp.diff(area, xx), xx); assert xs == [sp.Rational(1, 2)] and area.subs(xx, sp.Rational(1, 2)) == sp.Rational(1, 2)
    mc_val(B, ch, "Optimization", 3, "A rectangle with base on the hypotenuse (length $2$) is inscribed in an isosceles right triangle. The largest possible area is", sp.Rational(1, 2), [1, sp.Rational(1, 4), sp.Rational(2, 3), 2],
           "Put the hypotenuse on $[-1,1]$ with apex $(0,1)$: a rectangle of half-width $x$ has height $1-x$, so $A=2x(1-x)$, maximal at $x=\\frac12$: $A=\\frac12$ (dimensions $1\\times\\frac12$).", "Tutorial 6, Q2", "src")
    Vb = x * (8 - 2 * x) * (15 - 2 * x); xs = [z for z in sp.solve(sp.diff(Vb, x), x) if 0 < z < 4]; assert xs == [sp.Rational(5, 3)] and Vb.subs(x, xs[0]) == sp.Rational(2450, 27)
    mc_val(B, ch, "Optimization", 3, "An open box is made from an $8\\times15$ in sheet by cutting equal corner squares and folding. The maximum volume (in³) is", sp.Rational(2450, 27), [sp.Rational(2450, 9), sp.Rational(1225, 27), 90, sp.Rational(350, 3)],
           "$V=x(8-2x)(15-2x)$, $V'=0\\Rightarrow12x^2-92x+120=0\\Rightarrow x=\\frac53$ (the other root $6>4$ is outside the domain $0<x<4$). $V(\\frac53)=\\frac53\\cdot\\frac{14}3\\cdot\\frac{35}3=\\frac{2450}{27}$.", "Tutorial 6, Q3", "src")
    B.mcq(ch, "Optimization", 2, "With $800$ m of fence for a rectangular plot bounded by a river on one side (no fence there), the largest area and dimensions are", "$80\\,000$ m² with sides $200$ m (two) and $400$ m (parallel to the river)",
          ["$160\\,000$ m² with a $400\\times400$ square", "$80\\,000$ m² with sides $400$ m (two) and $200$ m (parallel to the river)", "$40\\,000$ m² with a $200\\times200$ square"],
          "Let $x$ be each side perpendicular to the river: $A=x(800-2x)$, $A'=800-4x=0\\Rightarrow x=200$, parallel side $400$: $A=200\\cdot400=80000$.", "Tutorial 6, Q4", "src")
    asq = sp.Symbol("a", positive=True)
    costf = asq ** 2 + 2000 / asq; assert sp.solve(sp.diff(costf, asq), asq) == [10]
    B.mcq(ch, "Optimization", 3, "An open-top steel tank with a square base must hold $500$ ft³ and use the least steel. The base side and height are", "base $10$ ft, height $5$ ft", ["base $5$ ft, height $20$ ft", "base $10$ ft, height $10$ ft", "base $\\sqrt[3]{500}$ ft, height $\\sqrt[3]{500}$ ft"],
          "Base side $a$, height $h=\\frac{500}{a^2}$. Surface $S=a^2+4ah=a^2+\\frac{2000}{a}$; $S'=2a-\\frac{2000}{a^2}=0\\Rightarrow a^3=1000$, $a=10$, $h=5$.", "Tutorial 6, Q5", "src")
    arect = 2 * xx * (27 - xx ** 2); xs = sp.solve(sp.diff(arect, xx), xx); assert xs == [3] and arect.subs(xx, 3) == 108
    mc_val(B, ch, "Optimization", 3, "A rectangle has its base on the $x$-axis and upper vertices on $y=27-x^2$. The maximum area is", 108, [54, 81, 216, 162], "$A=2x(27-x^2)$, $A'=54-6x^2=0\\Rightarrow x=3$; $A=2\\cdot3\\cdot18=108$.", "Computation problems 6, Q1", "src")
    # Mock test: two towns and a station (minimise time)
    xs_ = sp.Symbol("x", positive=True)
    T = sp.sqrt(25 + xs_ ** 2) / 3 + sp.sqrt(49 + (6 - xs_) ** 2) / 6
    xopt = sp.nsolve(sp.diff(T, xs_), xs_, 2.0); assert 0 < xopt < 6
    # independent check by golden-section search
    lo, hi = 0.0, 6.0
    Tf = sp.lambdify(xs_, T)
    for _ in range(200):
        m1 = lo + (hi - lo) * 0.381966; m2 = lo + (hi - lo) * 0.618034
        if Tf(m1) < Tf(m2): hi = m2
        else: lo = m1
    assert abs((lo + hi) / 2 - float(xopt)) < 1e-6
    xo = float(xopt)
    B.mcq(ch, "Optimization", 3, "Towns $A$ and $B$ are $5$ and $7$ miles from a straight railroad; the feet of the perpendiculars $C,D$ are $6$ miles apart. A train goes $A\\to S\\to B$ with $S$ on $CD$, at $3$ mph on $AS$ and $6$ mph on $SB$. Minimising the total time, the distance $CS$ is about",
          "$%.2f$ miles" % xo, ["$%.2f$ miles" % (xo + 1.0), "$%.2f$ miles" % (xo - 1.0), "$3.00$ miles"] if abs(xo - 3.0) > 0.05 else ["$%.2f$ miles" % (xo + 1.0), "$%.2f$ miles" % (xo - 1.0), "$%.2f$ miles" % (xo + 2)],
          "With $x=CS$: $T(x)=\\frac{\\sqrt{25+x^2}}{3}+\\frac{\\sqrt{49+(6-x)^2}}{6}$. Setting $T'(x)=\\frac{x}{3\\sqrt{25+x^2}}-\\frac{6-x}{6\\sqrt{49+(6-x)^2}}=0$ and solving numerically gives $x\\approx%.3f$; $T''>0$ so it is a minimum (checked also by a golden-section search)." % xo, "Mock Test 1, Q2", "src")
    # ---- L'Hopital
    limq(B, ch, 3, "\\dfrac{2x^2-(3x+1)\\sqrt{x}+2}{x-1}", (2 * x ** 2 - (3 * x + 1) * sp.sqrt(x) + 2) / (x - 1), x, 1, None, -1, "At $x=1$ the numerator is $2-4+2=0$, so this is $\\frac00$. L'Hôpital: $\\frac{4x-3\\sqrt x-\\frac{3x+1}{2\\sqrt x}}{1}\\to4-3-2=-1$.", "Tutorial 6, Q6(a)", "src", extras=[3, 0, 1])
    limq(B, ch, 3, "\\dfrac{x(\\cos x-1)}{\\sin x-x}", x * (sp.cos(x) - 1) / (sp.sin(x) - x), x, 0, None, 3, "$\\frac00$: apply L'Hôpital repeatedly (or use $\\cos x-1\\approx-\\frac{x^2}2$, $\\sin x-x\\approx-\\frac{x^3}6$): the ratio tends to $3$.", "Tutorial 6, Q6(b)", "src", extras=[-3, 0, 1])
    limq(B, ch, 2, "\\dfrac{\\sin x-\\cos x}{x-\\pi/4}", (sp.sin(x) - sp.cos(x)) / (x - sp.pi / 4), x, sp.pi / 4, None, sp.sqrt(2), "$\\frac00$ at $x=\\frac\\pi4$; L'Hôpital: $\\frac{\\cos x+\\sin x}{1}\\to\\sqrt2$ (this is $f'(\\frac\\pi4)$ for $f=\\sin x-\\cos x$).", "Computation problems 6, Q2", "src", extras=[0, 1, sp.sqrt(2) / 2])
    cc7 = sp.limit((9 * x - 3 * sp.sin(3 * x)) / (5 * x ** 3), x, 0); assert cc7 == sp.Rational(27, 10)
    mc_val(B, ch, "L'Hôpital's rule", 3, "For which $c$ is $f(x)=\\dfrac{9x-3\\sin3x}{5x^3}$ ($x\\ne0$), $f(0)=c$, continuous at $0$?", sp.Rational(27, 10), [sp.Rational(9, 5), 3, sp.Rational(27, 5), 0], "Need $c=\\lim_{x\\to0}f$: L'Hôpital three times, $\\frac{81\\cos3x\\cdot}{\\cdots}$ — equivalently $3\\sin3x\\approx9x-\\frac{27}2x^3$, so the numerator $\\approx\\frac{27}{2}x^3$ and the limit is $\\frac{27/2}{5}=\\frac{27}{10}$.", "Tutorial 6, Q7", "src")
    limq(B, ch, 2, "x\\ln x", x * sp.log(x), x, 0, "+", 0, "Rewrite as $\\frac{\\ln x}{1/x}$ ($\\frac{-\\infty}{\\infty}$): L'Hôpital gives $\\frac{1/x}{-1/x^2}=-x\\to0$.", "Generated (Lecture 6: indeterminate forms)", "gen", extras=[-oo, 1, oo])
    limq(B, ch, 2, "\\dfrac{e^x-1-x}{x^2}", (sp.exp(x) - 1 - x) / x ** 2, x, 0, None, sp.Rational(1, 2), "$\\frac00$: apply L'Hôpital twice: $\\frac{e^x-1}{2x}\\to\\frac{e^x}{2}\\to\\frac12$.", "Generated (Lecture 6)", "gen", extras=[0, 1, oo])
    limq(B, ch, 2, "\\left(1+\\dfrac1x\\right)^{x}", (1 + 1 / x) ** x, x, oo, None, sp.E, "Form $1^\\infty$: take $\\ln$: $x\\ln(1+\\frac1x)=\\frac{\\ln(1+1/x)}{1/x}\\to1$ (L'Hôpital), so the limit is $e^1=e$.", "Generated (Lecture 6)", "gen", extras=[1, 0, oo])
    limq(B, ch, 3, "x^{1/x}", x ** (1 / x), x, oo, None, 1, "Form $\\infty^0$: $\\ln x^{1/x}=\\frac{\\ln x}{x}\\to0$ (L'Hôpital), so the limit is $e^0=1$.", "Generated (Lecture 6)", "gen", extras=[0, sp.E, oo])
    limq(B, ch, 3, "\\left(\\dfrac1{\\sin x}-\\dfrac1x\\right)", 1 / sp.sin(x) - 1 / x, x, 0, None, 0, "Form $\\infty-\\infty$: combine, $\\frac{x-\\sin x}{x\\sin x}$ is $\\frac00$; L'Hôpital twice gives $\\frac{\\sin x}{2\\cos x-x\\sin x}\\to0$.", "Generated (Lecture 6)", "gen", extras=[1, oo, sp.Rational(1, 2)])
    limq(B, ch, 2, "\\dfrac{\\ln x}{x}", sp.log(x) / x, x, oo, None, 0, "$\\frac\\infty\\infty$: L'Hôpital gives $\\frac{1/x}{1}\\to0$ (logarithms grow slower than any power).", "Generated (Lecture 6)", "gen", extras=[1, oo, sp.E])
    B.mcq(ch, "L'Hôpital's rule", 1, "Which of the following is NOT an indeterminate form?", "$\\dfrac{1}{0^+}$", ["$\\dfrac00$", "$\\infty-\\infty$", "$0\\cdot\\infty$"], "$\\frac1{0^+}=+\\infty$ is determined; the others can have any value.", "Lecture 6", "concept")
    # ---- Newton's method
    f9 = x ** 4 + x - 3
    xs = newton(f9, -1, 2); assert xs[1] == -2 and xs[2] == sp.Rational(-51, 31)
    B.mcq(ch, "Newton's method", 2, "Newton's method for $f(x)=x^4+x-3$ starting at $x_0=-1$: $x_1$ and $x_2$ are", "$x_1=-2$ and $x_2=-\\frac{51}{31}\\approx-1.645$", ["$x_1=-2$ and $x_2=-\\frac{11}{31}$", "$x_1=0$ and $x_2=-1$", "$x_1=-\\frac32$ and $x_2=-\\frac{51}{31}$"],
          "$x_{n+1}=x_n-\\frac{f(x_n)}{f'(x_n)}$, $f'=4x^3+1$. $f(-1)=-3$, $f'(-1)=-3\\Rightarrow x_1=-1-1=-2$. $f(-2)=11$, $f'(-2)=-31\\Rightarrow x_2=-2+\\frac{11}{31}=-\\frac{51}{31}$.", "Tutorial 6, Q9(a)", "src")
    xs = newton(f9, 1, 2); assert xs[1] == sp.Rational(6, 5)
    x2f = float(xs[2])
    B.mcq(ch, "Newton's method", 2, "Newton's method for $f(x)=x^4+x-3$ starting at $x_0=1$ gives $x_1=\\frac65$ and $x_2\\approx$", "$%.5f$" % x2f, ["$%.5f$" % (x2f + 0.03), "$%.5f$" % (x2f - 0.05), "$1.20000$"],
          "$f(1)=-1$, $f'(1)=5$: $x_1=1+\\frac15=1.2$. $f(1.2)=0.2736$, $f'(1.2)=7.912$: $x_2=1.2-\\frac{0.2736}{7.912}\\approx%.5f$." % x2f, "Tutorial 6, Q9(a)", "src")
    xs = newton(x ** 4 - 2, 1, 2); assert xs[1] == sp.Rational(5, 4)
    x2g = float(xs[2])
    B.mcq(ch, "Newton's method", 2, "To approximate $\\sqrt[4]{2}$ solve $x^4-2=0$ by Newton's method from $x_0=1$: $x_2\\approx$", "$%.4f$" % x2g, ["$%.4f$" % (x2g + 0.06), "$%.4f$" % (x2g - 0.06), "$1.2500$"],
          "$x_{n+1}=x_n-\\frac{x_n^4-2}{4x_n^3}$: $x_1=1+\\frac14=1.25$, $x_2=1.25-\\frac{1.25^4-2}{4\\cdot1.25^3}\\approx%.4f$ (true value $1.18921$)." % x2g, "Tutorial 6, Q9(b)", "src")
    f3 = x ** 2 + x - 1
    xs = newton(f3, -1, 2); assert xs[2] == sp.Rational(-5, 3)
    xs2 = newton(f3, 1, 2); assert xs2[2] == sp.Rational(13, 21)
    B.mcq(ch, "Newton's method", 2, "Newton's method for $x^2+x-1=0$ with $x_0=-1$ gives $x_2=$", "$-\\frac53$", ["$-2$", "$-\\frac{13}{21}$", "$-\\frac32$"], "$f'=2x+1$. $x_1=-1-\\frac{-1}{-1}=-2$; $x_2=-2-\\frac{1}{-3}=-\\frac53$.", "Computation problems 6, Q3", "src")
    B.mcq(ch, "Newton's method", 2, "Newton's method for $x^2+x-1=0$ with $x_0=1$ gives $x_2=$", "$\\frac{13}{21}$", ["$\\frac23$", "$\\frac{5}{3}$", "$\\frac{7}{3}$"], "$x_1=1-\\frac13=\\frac23$; $x_2=\\frac23-\\frac{f(2/3)}{f'(2/3)}=\\frac23-\\frac{1/9}{7/3}=\\frac23-\\frac1{21}=\\frac{13}{21}$.", "Computation problems 6, Q3", "src")
    B.mcq(ch, "Newton's method", 1, "Newton's iteration for solving $f(x)=0$ is", "$x_{n+1}=x_n-\\dfrac{f(x_n)}{f'(x_n)}$", ["$x_{n+1}=x_n-\\dfrac{f'(x_n)}{f(x_n)}$", "$x_{n+1}=x_n+\\dfrac{f(x_n)}{f'(x_n)}$", "$x_{n+1}=\\dfrac{f(x_n)}{f'(x_n)}$"], "Follow the tangent line at $x_n$ down to the $x$-axis.", "Lecture 6", "concept")
    B.mcq(ch, "Newton's method", 3, "For $f(x)=\\sqrt{|x|}\\operatorname{sgn}(x)$ (i.e. $\\sqrt x$ for $x\\ge0$, $-\\sqrt{-x}$ for $x<0$), Newton's method from $x_0=h>0$ gives $x_1=$", "$-h$ (and then $x_2=h$: the iteration oscillates)", ["$0$ (immediate convergence)", "$h/2$", "$2h$"],
          "For $x>0$: $x_1=h-\\frac{\\sqrt h}{1/(2\\sqrt h)}=h-2h=-h$; by symmetry the next step returns to $h$.", "Tutorial 6, Q10", "src")
    # ---- antiderivatives
    Ft = (tt * sp.sqrt(tt) + sp.sqrt(tt)) / tt ** 2
    ant = sp.integrate(sp.expand(Ft), tt); assert num_equal(sp.diff(ant, tt), Ft, tt, pts=[0.5, 1.5, 2.5])
    mc_expr(B, ch, "Antiderivatives", 2, "Find the most general antiderivative of $\\dfrac{t\\sqrt t+\\sqrt t}{t^2}$.", ant + sp.Symbol("C"), [-2 / sp.sqrt(tt) + sp.Symbol("C"), 2 * sp.sqrt(tt) + 2 / sp.sqrt(tt) + sp.Symbol("C"), -sp.log(tt) + 2 * sp.sqrt(tt) + sp.Symbol("C"), sp.sqrt(tt) / 2 + sp.Symbol("C")],
            "Split: $\\frac{t^{3/2}+t^{1/2}}{t^2}=t^{-1/2}+t^{-3/2}$, so $F=2t^{1/2}-2t^{-1/2}+C$. Check by differentiating.", "Tutorial 6, Q11(a)", "src", tt)
    mc_expr(B, ch, "Antiderivatives", 2, "Find the most general antiderivative of $\\dfrac{\\csc\\theta\\cot\\theta}{2}$.", -sp.csc(th) / 2 + sp.Symbol("C"), [sp.csc(th) / 2 + sp.Symbol("C"), -sp.sec(th) / 2 + sp.Symbol("C"), -sp.cot(th) / 2 + sp.Symbol("C"), sp.log(sp.sin(th)) / 2 + sp.Symbol("C")],
            "$\\frac{d}{d\\theta}\\csc\\theta=-\\csc\\theta\\cot\\theta$, so $\\int\\csc\\theta\\cot\\theta\\,d\\theta=-\\csc\\theta$ and the answer is $-\\frac12\\csc\\theta+C$.", "Tutorial 6, Q11(b)", "src", th)
    mc_expr(B, ch, "Antiderivatives", 1, "An antiderivative of $\\dfrac32\\sqrt x$ is", x ** sp.Rational(3, 2), [sp.sqrt(x), 3 * x ** sp.Rational(3, 2) / 4, 9 * x ** sp.Rational(3, 2) / 4, x ** sp.Rational(1, 2) / 2], "$\\int\\frac32x^{1/2}dx=\\frac32\\cdot\\frac{x^{3/2}}{3/2}=x^{3/2}$.", "Computation problems 6, Q5(a)", "src")
    mc_expr(B, ch, "Antiderivatives", 1, "An antiderivative of $\\dfrac{1}{2\\sqrt x}$ is", sp.sqrt(x), [x ** sp.Rational(3, 2), 1 / sp.sqrt(x), -1 / (4 * x ** sp.Rational(3, 2)), 2 * sp.sqrt(x)], "$\\frac{d}{dx}\\sqrt x=\\frac1{2\\sqrt x}$.", "Computation problems 6, Q5(b)", "src")
    mc_expr(B, ch, "Antiderivatives", 2, "An antiderivative of $-\\csc5x\\cot5x$ is", sp.csc(5 * x) / 5, [sp.csc(5 * x), -sp.csc(5 * x) / 5, 5 * sp.csc(5 * x), -sp.cot(5 * x) / 5], "$\\frac{d}{dx}\\csc5x=-5\\csc5x\\cot5x$, so $\\frac15\\csc5x$ has derivative $-\\csc5x\\cot5x$.", "Computation problems 6, Q6(b)", "src")
    mc_expr(B, ch, "Antiderivatives", 2, "$\\displaystyle\\int\\dfrac{1+\\cos4t}{2}\\,dt=$", t / 2 + sp.sin(4 * t) / 8 + sp.Symbol("C"), [t / 2 + sp.sin(4 * t) / 2 + sp.Symbol("C"), t / 2 - sp.sin(4 * t) / 8 + sp.Symbol("C"), t + sp.sin(4 * t) / 4 + sp.Symbol("C"), t / 2 + sp.sin(4 * t) / 4 + sp.Symbol("C")],
            "$\\int\\frac12dt=\\frac t2$ and $\\int\\frac{\\cos4t}{2}dt=\\frac{\\sin4t}{8}$ (divide by the inner derivative $4$).", "Computation problems 6, Q7", "src", t)
    B.mcq(ch, "Antiderivatives", 1, "If $F'(x)=f(x)$, then every antiderivative of $f$ has the form", "$F(x)+C$", ["$F(x)\\cdot C$", "$F'(x)+C$", "$F(x)+C$ only for $C=0$"], "Two antiderivatives differ by a constant (a consequence of the MVT).", "Lecture 6", "concept")


# ============================================================================== CHAPTER 4
def ch4(B):
    ch = "c4"; rng = B.rng
    xx = x
    # ---- Riemann sums
    f = x ** 2 - 1
    def riemann(f, a, b, n, mode):
        dx = sp.Rational(b - a, n)
        pts = {"L": [a + i * dx for i in range(n)], "R": [a + (i + 1) * dx for i in range(n)], "M": [a + (i + sp.Rational(1, 2)) * dx for i in range(n)]}[mode]
        return sum(f.subs(x, p) for p in pts) * dx
    L4, R4, M4 = riemann(f, 0, 2, 4, "L"), riemann(f, 0, 2, 4, "R"), riemann(f, 0, 2, 4, "M")
    assert (L4, R4, M4) == (sp.Rational(-1, 4), sp.Rational(7, 4), sp.Rational(5, 8)) and sp.integrate(f, (x, 0, 2)) == sp.Rational(2, 3)
    for mode, nm, val, others in [("L", "left-endpoint", L4, [R4, M4]), ("R", "right-endpoint", R4, [L4, M4]), ("M", "midpoint", M4, [L4, R4])]:
        mc_val(B, ch, "Riemann sums", 2, "For $f(x)=x^2-1$ on $[0,2]$ with $4$ equal subintervals, the %s Riemann sum is" % nm, val, others + [sp.Rational(2, 3)],
               "$\\Delta x=\\frac12$; sample points %s. The sum is $\\Delta x\\sum f(c_k)=%s$ (the exact integral is $\\frac23$)." % ({"L": "$0,\\frac12,1,\\frac32$", "R": "$\\frac12,1,\\frac32,2$", "M": "$\\frac14,\\frac34,\\frac54,\\frac74$"}[mode], tex(val)), "Tutorial 7, Q1", "src")
    nn = sp.Symbol("n", positive=True, integer=True); kk = sp.Symbol("k", integer=True)
    rs = sp.simplify(sp.summation((3 * kk / nn) ** 2 + 1, (kk, 1, nn)) * 3 / nn)
    assert sp.limit(rs, nn, oo) == 12
    B.mcq(ch, "Riemann sums", 3, "For $f(x)=x^2+1$ on $[0,3]$, the right-endpoint Riemann sum with $n$ subintervals tends, as $n\\to\\infty$, to", "$12$", ["$9$", "$10$", "$\\infty$"],
          "$\\Delta x=\\frac3n$, $c_k=\\frac{3k}{n}$: $\\sum_{k=1}^n\\left(\\frac{9k^2}{n^2}+1\\right)\\frac3n=\\frac{27}{n^3}\\cdot\\frac{n(n+1)(2n+1)}{6}+3\\to9+3=12$ (equal to $\\int_0^3(x^2+1)dx=12$).", "Tutorial 7, Q2", "src")
    # ---- average value
    for lbl, f_, a_, b_, expect, src in [("(x-1)^2", (x - 1) ** 2, 0, 3, 1, "Tutorial 7, Q3(a)"), ("|x|-1", sp.Abs(x) - 1, -1, 1, sp.Rational(-1, 2), "Tutorial 7, Q3(b)(i)"), ("|x|-1", sp.Abs(x) - 1, 1, 3, 1, "Tutorial 7, Q3(b)(ii)"),
                                         ("|x|-1", sp.Abs(x) - 1, -1, 3, sp.Rational(1, 4), "Tutorial 7, Q3(b)(iii)"), ("-3x^2-1", -3 * x ** 2 - 1, 0, 1, -2, "Computation problems 7, Q1")]:
        avg = sp.integrate(f_, (x, a_, b_)) / (b_ - a_); assert avg == expect, (lbl, avg)
        tot = sp.integrate(f_, (x, a_, b_))
        mc_val(B, ch, "Average value", 2, "Find the average value of $f(x)=%s$ over $[%d,%d]$." % (lbl, a_, b_), avg, [tot, -avg, avg + 1, tot / 2], "$\\frac1{b-a}\\int_a^bf=\\frac1{%d}\\cdot(%s)=%s$." % (b_ - a_, tex(tot), tex(avg)), src, "src")
    # ---- definite integrals / FTC
    mc_val(B, ch, "Definite integrals", 1, "$\\displaystyle\\int_{-1}^{1}(x^2-2x+3)\\,dx=$", sp.Rational(20, 3), [sp.Rational(10, 3), 6, sp.Rational(14, 3), sp.Rational(26, 3)], "Odd part $-2x$ integrates to $0$ on a symmetric interval; $\\int_{-1}^1(x^2+3)dx=\\frac23+6=\\frac{20}3$.", "Tutorial 7, Q4(a)", "src")
    mc_val(B, ch, "Definite integrals", 1, "$\\displaystyle\\int_0^{\\pi}(1+\\cos x)\\,dx=$", sp.pi, [2, sp.pi + 2, 1, 2 * sp.pi], "$[x+\\sin x]_0^\\pi=\\pi+0=\\pi$.", "Tutorial 7, Q4(b)", "src")
    mc_val(B, ch, "Substitution", 2, "$\\displaystyle\\int_0^{\\sqrt{\\pi/2}}x\\cos(x^2)\\,dx=$", sp.Rational(1, 2), [1, sp.sqrt(2) / 4, 0, sp.Rational(1, 4)], "$u=x^2$, $du=2x\\,dx$: $\\frac12\\int_0^{\\pi/2}\\cos u\\,du=\\frac12$.", "Tutorial 7, Q5(a) (upper limit read as $\\sqrt{\\pi/2}$)", "src")
    mc_val(B, ch, "Substitution", 2, "$\\displaystyle\\int_2^5\\dfrac{x\\,dx}{\\sqrt{1+x^2}}=$", sp.sqrt(26) - sp.sqrt(5), [sp.sqrt(26) + sp.sqrt(5), sp.sqrt(26) - 5, 3, 2 * (sp.sqrt(26) - sp.sqrt(5))], "$\\frac{d}{dx}\\sqrt{1+x^2}=\\frac{x}{\\sqrt{1+x^2}}$, so the value is $\\sqrt{26}-\\sqrt5$.", "Tutorial 7, Q5(b)", "src")
    tq = sp.Symbol("t", positive=True)
    dA = sp.diff(sp.integrate(x ** 4 + 3 / x ** 3, (x, 1, sp.sqrt(tq))), tq)
    dB = (tq ** 2 + 3 * tq ** sp.Rational(-3, 2)) / (2 * sp.sqrt(tq))
    assert num_equal(dA, dB, tq, pts=[0.7, 1.3, 2.2])
    mc_expr(B, ch, "Fundamental Theorem of Calculus", 3, "Find $\\dfrac{d}{dt}\\displaystyle\\int_1^{\\sqrt t}\\left(x^4+\\dfrac{3}{x^3}\\right)dx$.", sp.simplify(dB),
            [sp.simplify(tq ** 2 + 3 * tq ** sp.Rational(-3, 2)), sp.simplify(-dB), sp.simplify(sp.sqrt(tq) ** 4 + 3 / sp.sqrt(tq) ** 3 + 0), sp.simplify(tq ** 2 / 2)],
            "FTC-1 with the chain rule: $\\frac{d}{dt}\\int_1^{u(t)}g=g(u)\\,u'$ with $u=\\sqrt t$, $u'=\\frac1{2\\sqrt t}$, $g(u)=u^4+3u^{-3}$: $\\left(t^2+3t^{-3/2}\\right)\\frac{1}{2\\sqrt t}=\\frac{t^{3/2}}{2}+\\frac{3}{2t^2}$.", "Tutorial 7, Q6", "src", tq)
    for lbl, expr, expect, src in [("\\displaystyle\\int_a^x(t^3+1)\\,dt", x ** 3 + 1, x ** 3 + 1, "Computation problems 7, Q5(a)"), ("\\displaystyle\\int_x^5 3t\\sin t\\,dt", -3 * x * sp.sin(x), -3 * x * sp.sin(x), "Computation problems 7, Q5(b)"),
                                   ("\\displaystyle\\int_1^{x^2}\\cos t\\,dt", 2 * x * sp.cos(x ** 2), 2 * x * sp.cos(x ** 2), "Computation problems 7, Q6(a)"), ("\\displaystyle\\int_{1+3x^2}^{4}\\dfrac{dt}{2+t}", -2 * x / (1 + x ** 2), -2 * x / (1 + x ** 2), "Computation problems 7, Q6(b)")]:
        mc_expr(B, ch, "Fundamental Theorem of Calculus", 2, "If $y=%s$, then $\\dfrac{dy}{dx}=$" % lbl, expect,
                [-expect, expect * x, sp.sin(x) if lbl.find("\\sin") > -1 else expect + 1, sp.simplify(expect.subs(x, x ** 2)) if expect.has(x) else expect * 2], "FTC part 1 with the chain rule (swap the limits for a minus sign): $y'=%s$." % tex(expect), src, "src")
    for (stem, val, ex) in [("$\\displaystyle\\int_2^2g$ ", 0, "An integral over a degenerate interval is $0$."), ("$\\displaystyle\\int_5^1g$ given $\\displaystyle\\int_1^5g=8$", -8, "Reversing the limits flips the sign."),
                            ("$\\displaystyle\\int_1^23f$ given $\\displaystyle\\int_1^2f=-4$", -12, "Constants factor out: $3\\cdot(-4)$."), ("$\\displaystyle\\int_2^5f$ given $\\displaystyle\\int_1^2f=-4$ and $\\displaystyle\\int_1^5f=6$", 10, "$\\int_2^5=\\int_1^5-\\int_1^2=6-(-4)$."),
                            ("$\\displaystyle\\int_1^5(f-g)$ given $\\displaystyle\\int_1^5f=6$ and $\\displaystyle\\int_1^5g=8$", -2, "Linearity: $6-8$.")]:
        mc_val(B, ch, "Definite integrals", 1, "Evaluate " + stem + ".", val, [-val if val else 1, val + 2, val - 2, 2 * val if val else -1], ex, "Computation problems 7, Q2–Q4", "src")
    # ---- substitution (indefinite)
    C = sp.Symbol("C")
    SUB = [("\\displaystyle\\int(x^3+x)^5(3x^2+1)\\,dx", (x ** 3 + x) ** 6 / 6, "$u=x^3+x$, $du=(3x^2+1)dx$.", "Computation problems 7, Q7(a)", [(x ** 3 + x) ** 6, (x ** 3 + x) ** 6 / 3, (x ** 3 + x) ** 5 / 5, (x ** 3 + x) ** 6 * (3 * x ** 2 + 1) / 6]),
           ("\\displaystyle\\int\\sqrt{2x+1}\\,dx", (2 * x + 1) ** sp.Rational(3, 2) / 3, "$u=2x+1$, $du=2\\,dx$: $\\frac12\\cdot\\frac{u^{3/2}}{3/2}$.", "Computation problems 7, Q7(b)", [(2 * x + 1) ** sp.Rational(3, 2) * 2 / 3, (2 * x + 1) ** sp.Rational(3, 2) / 2, (2 * x + 1) ** sp.Rational(3, 2), (2 * x + 1) ** sp.Rational(1, 2) / 2]),
           ("\\displaystyle\\int\\cos(7x+3)\\,dx", sp.sin(7 * x + 3) / 7, "$u=7x+3$, $du=7\\,dx$.", "Computation problems 7, Q8(b)", [sp.sin(7 * x + 3), 7 * sp.sin(7 * x + 3), -sp.sin(7 * x + 3) / 7, sp.cos(7 * x + 3) / 7]),
           ("\\displaystyle\\int x^2\\cos(x^3)\\,dx", sp.sin(x ** 3) / 3, "$u=x^3$, $du=3x^2dx$.", "Computation problems 7, Q9(a)", [sp.sin(x ** 3), 3 * sp.sin(x ** 3), -sp.sin(x ** 3) / 3, x ** 3 * sp.sin(x ** 3) / 3]),
           ("\\displaystyle\\int x\\sqrt{2x+1}\\,dx", (2 * x + 1) ** sp.Rational(5, 2) / 10 - (2 * x + 1) ** sp.Rational(3, 2) / 6, "$u=2x+1$, $x=\\frac{u-1}2$: $\\frac14\\int(u^{3/2}-u^{1/2})du$.", "Computation problems 7, Q9(b)",
            [(2 * x + 1) ** sp.Rational(5, 2) / 5 - (2 * x + 1) ** sp.Rational(3, 2) / 3, (2 * x + 1) ** sp.Rational(5, 2) / 10 + (2 * x + 1) ** sp.Rational(3, 2) / 6, x * (2 * x + 1) ** sp.Rational(3, 2) / 3, (2 * x + 1) ** sp.Rational(5, 2) / 5]),
           ("\\displaystyle\\int\\sin^2x\\,dx", x / 2 - sp.sin(2 * x) / 4, "$\\sin^2x=\\frac{1-\\cos2x}2$.", "Computation problems 7, Q10(a)", [x / 2 + sp.sin(2 * x) / 4, sp.sin(x) ** 3 / 3, x / 2 - sp.sin(2 * x) / 2, -sp.sin(x) * sp.cos(x) / 2 - x / 2]),
           ("\\displaystyle\\int\\dfrac{(1+\\sqrt x)^{1/3}}{\\sqrt x}\\,dx", sp.Rational(3, 2) * (1 + sp.sqrt(x)) ** sp.Rational(4, 3), "$u=1+\\sqrt x$, $du=\\frac{dx}{2\\sqrt x}$: $2\\int u^{1/3}du=\\frac32u^{4/3}$.", "Tutorial 7, Q7(a)", [(1 + sp.sqrt(x)) ** sp.Rational(4, 3) * 3 / 4, 3 * (1 + sp.sqrt(x)) ** sp.Rational(4, 3), sp.Rational(3, 2) * (1 + sp.sqrt(x)) ** sp.Rational(2, 3), (1 + sp.sqrt(x)) ** sp.Rational(4, 3)])]
    INTEGRAND = {"Computation problems 7, Q7(a)": (x ** 3 + x) ** 5 * (3 * x ** 2 + 1), "Computation problems 7, Q7(b)": sp.sqrt(2 * x + 1), "Computation problems 7, Q8(b)": sp.cos(7 * x + 3),
                 "Computation problems 7, Q9(a)": x ** 2 * sp.cos(x ** 3), "Computation problems 7, Q9(b)": x * sp.sqrt(2 * x + 1), "Computation problems 7, Q10(a)": sp.sin(x) ** 2,
                 "Tutorial 7, Q7(a)": (1 + sp.sqrt(x)) ** sp.Rational(1, 3) / sp.sqrt(x)}
    for lbl, ans, how, src, wrongs in SUB:
        assert num_equal(sp.diff(ans, x), INTEGRAND[src], x, pts=[0.4, 0.9, 1.6, 2.3]), (src, sp.diff(ans, x))
        mc_expr(B, ch, "Substitution", 2, "Evaluate $%s$." % lbl, ans + C, [w + C for w in wrongs], how + " Result: $%s+C$." % tex(ans), src, "src", x)
    assert num_equal(sp.diff(-6 * sp.sqrt(1 - x ** 3), x), 9 * x ** 2 / sp.sqrt(1 - x ** 3), x, pts=[0.3, 0.6, 0.8])
    mc_expr(B, ch, "Substitution", 2, "$\\displaystyle\\int\\dfrac{9r^2\\,dr}{\\sqrt{1-r^3}}=$", -6 * sp.sqrt(1 - x ** 3) + C, [-3 * sp.sqrt(1 - x ** 3) + C, 6 * sp.sqrt(1 - x ** 3) + C, -12 * sp.sqrt(1 - x ** 3) + C, 9 * sp.sqrt(1 - x ** 3) + C],
            "$u=1-r^3$, $du=-3r^2dr$: $-3\\int u^{-1/2}du=-6\\sqrt u$ (variable written as $x$ here).", "Tutorial 7, Q7(b)", "src", x)
    # ---- areas between curves
    mc_val(B, ch, "Area between curves", 2, "Find the area enclosed by $x=2y^2$, $x=0$ and $y=3$.", 18, [9, 36, 54, 6], "Integrate in $y$: $\\int_0^3 2y^2dy=\\frac{2}{3}\\cdot27=18$.", "Tutorial 7, Q8(a)", "src")
    yy = sp.Symbol("y")
    ar_b = sp.integrate((yy + 2) / 4 - yy ** 2 / 4, (yy, -1, 2))
    assert ar_b == sp.Rational(9, 8)
    mc_val(B, ch, "Area between curves", 3, "Find the area enclosed by $y^2=4x$ and $y=4x-2$.", ar_b, [sp.Rational(9, 4), sp.Rational(9, 16), sp.Rational(27, 8), sp.Rational(3, 2)],
           "Intersections: $y^2=4x$ and $y=4x-2\\Rightarrow x=\\frac{y+2}4$, so $y^2=y+2$, $y=-1,2$. Integrate in $y$: $\\int_{-1}^{2}\\left(\\frac{y+2}{4}-\\frac{y^2}{4}\\right)dy=\\frac98$.", "Tutorial 7, Q8(b)", "src")
    ar_c = sp.integrate(x - sp.sin(x), (x, 0, sp.pi / 4)); assert sp.simplify(ar_c - (sp.pi ** 2 / 32 + sp.sqrt(2) / 2 - 1)) == 0
    mc_val(B, ch, "Area between curves", 3, "Find the area between $y=x$ and $y=\\sin x$ for $0\\le x\\le\\frac\\pi4$.", ar_c, [sp.pi ** 2 / 32 - sp.sqrt(2) / 2 + 1, sp.pi ** 2 / 32, sp.pi ** 2 / 32 + sp.sqrt(2) / 2, sp.Rational(1, 2)],
           "For $0\\le x\\le\\frac\\pi4$, $x\\ge\\sin x$: $\\int_0^{\\pi/4}(x-\\sin x)dx=\\left[\\frac{x^2}2+\\cos x\\right]_0^{\\pi/4}=\\frac{\\pi^2}{32}+\\frac{\\sqrt2}{2}-1\\approx%.4f$." % float(ar_c), "Tutorial 7, Q8(c)", "src")
    # ---- volumes
    v1 = sp.integrate(sp.pi * ((2 - x ** 2 - x ** 2) / 2) ** 2, (x, -1, 1)); assert v1 == 16 * sp.pi / 15
    mc_val(B, ch, "Volumes by cross-sections", 3, "A solid lies between $x=-1$ and $x=1$; its cross-sections perpendicular to the $x$-axis are disks with diameter from $y=x^2$ to $y=2-x^2$. Its volume is", v1, [8 * sp.pi / 15, 32 * sp.pi / 15, 4 * sp.pi / 3, 16 / 15],
           "Diameter $d=2-2x^2$, radius $1-x^2$: $V=\\pi\\int_{-1}^1(1-x^2)^2dx=\\pi\\left(2-\\frac43+\\frac25\\right)=\\frac{16\\pi}{15}$.", "Tutorial 8, Q1", "src")
    s_ = 2 * sp.sqrt(sp.sin(x))
    vt = sp.integrate(sp.sqrt(3) / 4 * s_ ** 2, (x, 0, sp.pi)); vs = sp.integrate(s_ ** 2, (x, 0, sp.pi)); assert sp.simplify(vt - 2 * sp.sqrt(3)) == 0 and vs == 8
    mc_val(B, ch, "Volumes by cross-sections", 3, "The base of a solid is the region under $y=2\\sqrt{\\sin x}$, $0\\le x\\le\\pi$; cross-sections perpendicular to the $x$-axis are equilateral triangles with a side on the base. Volume:", 2 * sp.sqrt(3), [8, 4 * sp.sqrt(3), sp.sqrt(3), 2 * sp.sqrt(3) * sp.pi],
           "Side $s=2\\sqrt{\\sin x}$, area $\\frac{\\sqrt3}4s^2=\\sqrt3\\sin x$; $V=\\sqrt3\\int_0^\\pi\\sin x\\,dx=2\\sqrt3$.", "Tutorial 8, Q2(a)", "src")
    mc_val(B, ch, "Volumes by cross-sections", 3, "Same base, but the cross-sections are squares with a side on the base. Volume:", 8, [2 * sp.sqrt(3), 4, 16, 8 * sp.pi], "Area $s^2=4\\sin x$; $V=4\\int_0^\\pi\\sin x\\,dx=8$.", "Tutorial 8, Q2(b)", "src")
    reg = lambda f_, g_, lo_, hi_: (f_, g_, lo_, hi_)
    # triangle 2y = x+4, y = x, x = 0  (vertices (0,0), (0,2), (4,4))
    up, lowf = (x + 4) / 2, x
    va = sp.integrate(sp.pi * (up ** 2 - lowf ** 2), (x, 0, 4)); vb = sp.integrate(2 * sp.pi * x * (up - lowf), (x, 0, 4)); vc = sp.integrate(2 * sp.pi * (4 - x) * (up - lowf), (x, 0, 4))
    vd = sp.integrate(sp.pi * ((8 - lowf) ** 2 - (8 - up) ** 2), (x, 0, 4))
    assert (va, vb, vc, vd) == (16 * sp.pi, 32 * sp.pi / 3, 64 * sp.pi / 3, 48 * sp.pi)
    # Pappus check: area 4, centroid at x = 4/3 -> distance 8/3 from x = 4
    assert 2 * sp.pi * sp.Rational(8, 3) * 4 == vc
    note("Tutorial 8, Q6(c)", "The printed key shows $\\frac{512\\pi}{3}$ for revolving the triangle $2y=x+4$, $y=x$, $x=0$ about $x=4$ (shell method). Direct integration $2\\pi\\int_0^4(4-x)\\frac{4-x}{2}dx=\\frac{64\\pi}{3}$, and Pappus' theorem (area $4$, centroid distance $\\frac83$) gives the same $\\frac{64\\pi}{3}$; the key entry appears to be mistaken.")
    TRI = "the triangle bounded by $2y=x+4$, $y=x$ and $x=0$"
    mc_val(B, ch, "Volumes of revolution", 3, "Revolve %s about the $x$-axis (washer method). Volume:" % TRI, va, [8 * sp.pi, 32 * sp.pi / 3, 48 * sp.pi, 64 * sp.pi / 3], "$V=\\pi\\int_0^4\\left[\\left(\\frac{x+4}{2}\\right)^2-x^2\\right]dx=\\pi\\int_0^4\\left(4+2x-\\frac34x^2\\right)dx=16\\pi$.", "Tutorial 8, Q6(a)", "src")
    mc_val(B, ch, "Volumes of revolution", 3, "Revolve %s about the $y$-axis (shell method). Volume:" % TRI, vb, [16 * sp.pi, 64 * sp.pi / 3, 16 * sp.pi / 3, 48 * sp.pi], "$V=2\\pi\\int_0^4x\\left(\\frac{x+4}{2}-x\\right)dx=\\pi\\int_0^4(4x-x^2)dx=\\frac{32\\pi}{3}$.", "Tutorial 8, Q6(b)", "src")
    mc_val(B, ch, "Volumes of revolution", 3, "Revolve %s about the line $x=4$ (shell method). Volume:" % TRI, vc, [32 * sp.pi / 3, 512 * sp.pi / 3, 16 * sp.pi, 128 * sp.pi / 3], "Radius $4-x$, height $\\frac{x+4}2-x=\\frac{4-x}{2}$: $V=\\pi\\int_0^4(4-x)^2dx=\\frac{64\\pi}{3}$ (see the note on the Sources page about the printed key).", "Tutorial 8, Q6(c)", "src")
    mc_val(B, ch, "Volumes of revolution", 3, "Revolve %s about the line $y=8$ (washer method). Volume:" % TRI, vd, [16 * sp.pi, 32 * sp.pi, 64 * sp.pi, 96 * sp.pi], "Outer radius $8-x$, inner radius $8-\\frac{x+4}2$: $V=\\pi\\int_0^4\\left[(8-x)^2-\\left(\\frac{12-x}{2}\\right)^2\\right]dx=48\\pi$.", "Tutorial 8, Q6(d)", "src")
    v_c1 = sp.integrate(sp.pi * ((4 - x ** 2) ** 2 - (2 - x) ** 2), (x, -1, 2)); assert v_c1 == 108 * sp.pi / 5
    mc_val(B, ch, "Volumes of revolution", 3, "Revolve the region between $y=4-x^2$ and $y=2-x$ about the $x$-axis. Volume:", v_c1, [54 * sp.pi / 5, 216 * sp.pi / 5, 27 * sp.pi / 5, 36 * sp.pi],
           "They meet where $4-x^2=2-x$: $x=-1,2$. Washers: $\\pi\\int_{-1}^2\\left[(4-x^2)^2-(2-x)^2\\right]dx=\\frac{108\\pi}{5}$.", "Computation problems 8, Q1", "src")
    v_c2 = sp.integrate(2 * sp.pi * (x + 1) * x ** 2, (x, 0, 1)); assert v_c2 == 7 * sp.pi / 6
    mc_val(B, ch, "Volumes of revolution", 3, "The region in the first quadrant under $y=x^2$ and left of $x=1$ is revolved about the line $x=-1$. Volume:", v_c2, [sp.pi / 2, 5 * sp.pi / 6, 2 * sp.pi / 3, 7 * sp.pi / 3],
           "Shells of radius $x+1$ and height $x^2$: $V=2\\pi\\int_0^1(x+1)x^2dx=2\\pi\\left(\\frac14+\\frac13\\right)=\\frac{7\\pi}6$.", "Computation problems 8, Q2", "src")
    # ---- arc length / surface area
    Lc = sp.integrate(x ** 2 + 1 / (4 * x ** 2), (x, 1, 3)); assert Lc == sp.Rational(53, 6)
    assert sp.simplify(1 + sp.diff(x ** 3 / 3 + 1 / (4 * x), x) ** 2 - (x ** 2 + 1 / (4 * x ** 2)) ** 2) == 0
    mc_val(B, ch, "Arc length and surface area", 3, "Find the length of $y=\\dfrac{x^3}{3}+\\dfrac{1}{4x}$ for $1\\le x\\le3$.", sp.Rational(53, 6), [sp.Rational(26, 3), sp.Rational(53, 3), sp.Rational(27, 4), sp.Rational(107, 12)],
           "$y'=x^2-\\frac1{4x^2}$ and $1+y'^2=\\left(x^2+\\frac1{4x^2}\\right)^2$, so $L=\\int_1^3\\left(x^2+\\frac1{4x^2}\\right)dx=\\left[\\frac{x^3}{3}-\\frac1{4x}\\right]_1^3=\\frac{53}6$.", "Tutorial 8, Q7", "src")
    ast = sp.integrate(8 * sp.sqrt(1 + sp.diff((1 - x ** sp.Rational(2, 3)) ** sp.Rational(3, 2), x) ** 2), (x, sp.sqrt(2) / 4, 1))
    assert abs(float(sp.N(ast)) - 6) < 1e-6
    mc_val(B, ch, "Arc length and surface area", 3, "The astroid $x^{2/3}+y^{2/3}=1$ has total length", 6, [4, 3, 2 * sp.pi, 8], "By symmetry $L=8\\int_{\\sqrt2/4}^1\\sqrt{1+y'^2}\\,dx$ with $y=(1-x^{2/3})^{3/2}$ (and $\\sqrt{1+y'^2}=x^{-1/3}$): the integral evaluates to $6$.", "Tutorial 8, Q8", "src")
    sa = sp.integrate(2 * sp.sqrt(x) * sp.sqrt(1 + 1 / x), (x, 0, 3)); assert sa == sp.Rational(28, 3)
    mc_val(B, ch, "Arc length and surface area", 3, "Perpendicular segments of length $h=y$ are erected at the points of $y=2\\sqrt x$, $0\\le x\\le3$. The area of the surface so formed ($\\int y\\,ds$) is", sp.Rational(28, 3), [sp.Rational(14, 3), 28, sp.Rational(56, 3), sp.Rational(16, 3)],
           "$ds=\\sqrt{1+\\frac1x}\\,dx$, $y=2\\sqrt x$: $\\int_0^32\\sqrt x\\sqrt{1+\\frac1x}\\,dx=2\\int_0^3\\sqrt{x+1}\\,dx=\\frac43\\left(4^{3/2}-1\\right)=\\frac{28}{3}$.", "Tutorial 8, Q9", "src")
    ac = sp.integrate(sp.Symbol("k") * sp.Symbol("a") * th * sp.Symbol("a"), (th, 0, 2 * sp.pi))
    assert sp.simplify(ac - 2 * sp.pi ** 2 * sp.Symbol("k") * sp.Symbol("a") ** 2) == 0
    B.mcq(ch, "Arc length and surface area", 3, "On a circle of radius $a$, vertical segments of length $ks$ are drawn at arc length $s$ from $(a,0)$ once around. The area of the surface is", "$2\\pi^2ka^2$", ["$\\pi ka^2$", "$4\\pi^2ka^2$", "$2\\pi ka^2$"],
          "$s=a\\theta$, $ds=a\\,d\\theta$: area $=\\int_0^{2\\pi}k(a\\theta)(a\\,d\\theta)=ka^2\\cdot\\frac{(2\\pi)^2}{2}=2\\pi^2ka^2$.", "Tutorial 8, Q10", "src")
    L3 = sp.N(sp.Integral(sp.sqrt(1 + (x + 1) ** 2), (x, -1, 3)))
    B.mcq(ch, "Arc length and surface area", 3, "Length of the curve $y^2+2y=2x+1$ from $(-1,-1)$ to $(7,3)$ (set up with $x=\\frac{y^2+2y-1}{2}$): $L=\\int_{-1}^{3}\\sqrt{1+(y+1)^2}\\,dy\\approx$", "$%.2f$" % float(L3), ["$%.2f$" % (float(L3) - 1), "$%.2f$" % (float(L3) + 1.5), "$8.00$"],
          "$\\frac{dx}{dy}=y+1$, so $L=\\int_{-1}^3\\sqrt{1+(y+1)^2}\\,dy\\approx%.3f$ (numerical integration; the printed key says $\\approx9.29$)." % float(L3), "Computation problems 8, Q3", "src")
    assert abs(float(L3) - 9.29) < 0.01
    ln4 = sp.integrate(sp.sec(x), (x, 0, sp.pi / 6)); assert sp.simplify(ln4 - sp.log(sp.sqrt(3))) == 0 or abs(float(sp.N(ln4)) - 0.549) < 1e-3
    B.mcq(ch, "Arc length and surface area", 3, "Length of $y=\\int_0^x\\tan t\\,dt$ for $0\\le x\\le\\frac\\pi6$:", "$\\ln\\sqrt3\\approx0.549$", ["$\\ln\\sqrt2\\approx0.347$", "$\\frac{\\pi}{6}\\approx0.524$", "$\\ln3\\approx1.099$"],
          "$y'=\\tan x$, so $\\sqrt{1+y'^2}=\\sec x$ and $L=\\int_0^{\\pi/6}\\sec x\\,dx=\\ln|\\sec x+\\tan x|\\,\\Big|_0^{\\pi/6}=\\ln\\left(\\frac{2}{\\sqrt3}+\\frac1{\\sqrt3}\\right)=\\ln\\sqrt3$.", "Computation problems 8, Q4", "src")
    B.mcq(ch, "Volumes of revolution", 1, "The disk method for revolving $y=f(x)\\ge0$, $a\\le x\\le b$, about the $x$-axis gives $V=$", "$\\pi\\int_a^b f(x)^2\\,dx$", ["$\\pi\\int_a^b f(x)\\,dx$", "$2\\pi\\int_a^b xf(x)\\,dx$", "$\\int_a^b\\pi f(x)\\,dx$"], "A thin slab is a disk of radius $f(x)$.", "Lecture 8", "concept")
    B.mcq(ch, "Volumes of revolution", 1, "The shell method for revolving $y=f(x)\\ge0$, $a\\le x\\le b$ (with $a\\ge0$), about the $y$-axis gives $V=$", "$2\\pi\\int_a^b xf(x)\\,dx$", ["$\\pi\\int_a^b xf(x)\\,dx$", "$2\\pi\\int_a^b f(x)^2dx$", "$\\pi\\int_a^b x^2f(x)\\,dx$"], "A shell has radius $x$, height $f(x)$, thickness $dx$.", "Lecture 8", "concept")
    B.mcq(ch, "Arc length and surface area", 1, "The length of the graph of $y=f(x)$ on $[a,b]$ is", "$\\int_a^b\\sqrt{1+f'(x)^2}\\,dx$", ["$\\int_a^b\\left(1+f'(x)^2\\right)dx$", "$\\int_a^b\\sqrt{1+f(x)^2}\\,dx$", "$\\int_a^b|f'(x)|\\,dx$"], "Pythagoras on $ds^2=dx^2+dy^2$.", "Lecture 8", "concept")
    B.mcq(ch, "Fundamental Theorem of Calculus", 1, "FTC part 2: if $F'=f$ on $[a,b]$ then $\\int_a^bf(x)\\,dx=$", "$F(b)-F(a)$", ["$F(a)-F(b)$", "$F'(b)-F'(a)$", "$F(b)+F(a)$"], "Evaluate any antiderivative at the endpoints.", "Lecture 7", "concept")
