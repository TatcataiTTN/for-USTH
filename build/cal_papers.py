# -*- coding: utf-8 -*-
"""Calculus I written papers with full worked solutions.
Paper 1 is the real Mock Test 1 (2025-26). Papers B and C are 'final-style' mock papers in the same format (5 problems, 20 marks)
built from the problem types of the tutorials. Every final answer is verified with sympy while building (an assertion stops the build)."""
import math
import mpmath as mp
import sympy as sp
from qlib import tex

x, t, a_, b_, k_ = sp.symbols("x t a b k", positive=True)
u = sp.Symbol("u", positive=True)
C = sp.Symbol("C")
oo = sp.oo

def N_(e, nd=4):
    return "%.*f" % (nd, float(sp.N(e)))

def same(e1, e2, var=x, pts=(0.7, 1.3, 2.1, 3.4)):
    for p in pts:
        v1 = complex(sp.N(sp.sympify(e1).subs(var, p), 20)); v2 = complex(sp.N(sp.sympify(e2).subs(var, p), 20))
        assert abs(v1 - v2) < 1e-9 * max(1, abs(v1)), (e1, e2, p, v1, v2)
    return True

def anti(F, f, var=x, pts=(0.7, 1.3, 2.1, 3.4)):
    """assert F' = f"""
    return same(sp.diff(F, var), f, var, pts)

xr = sp.Symbol("xr", real=True)

def parity(expr_of_xr, pts):
    """'even' / 'odd' / 'neither' decided numerically on sample points of the domain (expr uses the real symbol xr)."""
    ev = od = True
    for p_ in pts:
        a1 = complex(sp.N(expr_of_xr.subs(xr, p_), 25)); a2 = complex(sp.N(expr_of_xr.subs(xr, -p_), 25))
        if abs(a1 - a2) > 1e-12: ev = False
        if abs(a1 + a2) > 1e-12: od = False
    return "even" if ev and not od else "odd" if od and not ev else "both" if ev and od else "neither"

def numeq(a, b, tol=1e-12):
    return abs(float(sp.N(sp.sympify(a) - sp.sympify(b), 30))) < tol

def ol(*items):
    return "<ol class='stp'>%s</ol>" % "".join("<li>%s</li>" % i for i in items)

def part(text, marks, answer, solution, lab=None):
    return dict(text=text, marks=marks, answer=answer, solution=solution, lab=lab, topic=None)

def paper(id_, title, sub, minutes, problems, calc="No calculators", note=""):
    return dict(id=id_, year=title, shift=sub, date="", minutes=minutes, calc=calc, problems=problems, note=note)

def build_papers():
    P = []

    # ================================================================= Mock Test 1 (real)
    # ---- Problem 1
    assert parity(sp.Abs(xr) / xr, (0.5, 2.0, 3.7)) == "odd" and parity(1 / sp.sqrt(1 - xr ** 2), (0.2, 0.5, 0.9)) == "even"
    assert parity((xr - 1) / (xr + 1), (0.5, 2.0, 3.0)) == "neither" and parity(1 + sp.sin(xr), (0.5, 1.0, 2.0)) == "neither"
    p1a = part("Determine whether each function is odd, even or neither: (i) $g(x)=\\dfrac{|x|}{x}$, (ii) $g(x)=\\dfrac{1}{\\sqrt{1-x^2}}$, (iii) $g(x)=\\dfrac{x-1}{x+1}$, (iv) $g(x)=1+\\sin x$.", 2,
               "(i) odd; (ii) even; (iii) neither; (iv) neither.",
               ol("First check that the domain is symmetric about $0$, then compare $g(-x)$ with $g(x)$.",
                  "(i) Domain $x\\ne0$ (symmetric). $g(-x)=\\dfrac{|-x|}{-x}=-\\dfrac{|x|}{x}=-g(x)$ ⇒ <b>odd</b> (it is the sign function).",
                  "(ii) Domain $(-1,1)$ (symmetric). $g(-x)=\\dfrac1{\\sqrt{1-(-x)^2}}=g(x)$ ⇒ <b>even</b>.",
                  "(iii) Domain $x\\ne-1$: the point $1$ is in the domain but $-1$ is not, so the domain is not symmetric ⇒ <b>neither</b>. (Also $g(-x)=\\frac{x+1}{x-1}=\\frac1{g(x)}$, which is neither $g(x)$ nor $-g(x)$.)",
                  "(iv) $g(-x)=1-\\sin x$. It is not $g(x)$ (differs when $\\sin x\\ne0$) and not $-g(x)$ (e.g. $g(0)=1\\ne0$) ⇒ <b>neither</b>."))
    lim1 = sp.limit(sp.sqrt(x + sp.sqrt(x + sp.sqrt(x))) / (sp.sqrt(x) + 1), x, oo); assert lim1 == 1
    p1b = part("Find the limits: (i) $\\displaystyle\\lim_{x\\to\\infty}\\dfrac{\\sqrt{x+\\sqrt{x+\\sqrt x}}}{\\sqrt x+1}$, (ii) $\\displaystyle\\lim_{x\\to\\infty}\\dfrac{e^{\\sin x}}{x+1}$.", 2,
               "(i) $1$; (ii) $0$.",
               ol("(i) Divide numerator and denominator by $\\sqrt x$: the numerator becomes $\\sqrt{1+\\dfrac{\\sqrt{x+\\sqrt x}}{x}}=\\sqrt{1+\\sqrt{\\dfrac1x+\\dfrac1{x^{3/2}}}}\\to\\sqrt{1+0}=1$ and the denominator becomes $1+\\dfrac1{\\sqrt x}\\to1$. The limit is $\\dfrac11=\\mathbf 1$.",
                  "(ii) $\\sin x$ oscillates, so use the squeeze theorem: $e^{-1}\\le e^{\\sin x}\\le e$. For $x>0$: $0<\\dfrac{e^{\\sin x}}{x+1}\\le\\dfrac{e}{x+1}\\to0$. Hence the limit is $\\mathbf 0$ (the limit of the quotient exists even though $e^{\\sin x}$ has no limit)."),
               lab=dict(tool="limit", f="sqrt(x+sqrt(x+sqrt(x)))/(sqrt(x)+1)", a="inf"))
    # ---- Problem 2
    X = sp.Symbol("x", positive=True)
    T = sp.sqrt(25 + X ** 2) / 3 + sp.sqrt(49 + (6 - X) ** 2) / 6
    Tp = sp.diff(T, X)
    xs = float(sp.nsolve(Tp, X, 2.0))
    quart = sp.expand(4 * X ** 2 * (49 + (6 - X) ** 2) - (6 - X) ** 2 * (25 + X ** 2))
    assert sp.simplify(quart - (3 * X ** 4 - 36 * X ** 3 + 279 * X ** 2 + 300 * X - 900)) == 0
    assert abs(float(quart.subs(X, xs))) < 1e-6 and 0 < xs < 6
    T0, T6, Ts = float(T.subs(X, 0)), float(T.subs(X, 6)), float(T.subs(X, xs))
    assert Ts < T0 and Ts < T6 and float(sp.diff(T, X, 2).subs(X, xs)) > 0
    p2 = part("Towns A and B lie on the same side of a straight railroad: A is $5$ miles from it, B is $7$ miles from it, and the feet C and D of the perpendiculars are $6$ miles apart. A train goes from A to a station S (to be built on the line between C and D) at $3$ mph, then from S to B at $6$ mph. Find the position of S that minimises the total travel time.", 4,
              "$CS\\approx %s$ miles from C (total time $\\approx%s$ h)." % (N_(xs, 3), N_(Ts, 3)),
              ol("Let $x=CS\\in[0,6]$. Then $AS=\\sqrt{25+x^2}$ and $SB=\\sqrt{49+(6-x)^2}$, so $T(x)=\\dfrac{\\sqrt{25+x^2}}{3}+\\dfrac{\\sqrt{49+(6-x)^2}}{6}$ (time $=$ distance / speed).",
                 "$T'(x)=\\dfrac{x}{3\\sqrt{25+x^2}}-\\dfrac{6-x}{6\\sqrt{49+(6-x)^2}}$. Critical point: $T'=0\\iff2x\\sqrt{49+(6-x)^2}=(6-x)\\sqrt{25+x^2}$.",
                 "Square (both sides are positive for $0<x<6$): $4x^2\\big(49+(6-x)^2\\big)=(6-x)^2(25+x^2)$, which simplifies to the quartic $3x^4-36x^3+279x^2+300x-900=0$.",
                 "No closed form: solve numerically. On $[0,6]$ there is exactly one root, $x\\approx%s$ (e.g. bisection: the quartic is $-900<0$ at $0$ and positive at $6$)." % N_(xs, 3),
                 "Why it is the minimum: $T''(x)>0$ ($T$ is a sum of convex functions), or compare the values: $T(0)\\approx%s$, $T(%s)\\approx%s$, $T(6)\\approx%s$ hours. Endpoints are worse." % (N_(T0, 3), N_(xs, 3), N_(Ts, 3), N_(T6, 3)),
                 "<b>Answer:</b> the station should be about $%s$ miles from C (and $%s$ miles from D)." % (N_(xs, 2), N_(6 - xs, 2))))
    # ---- Problem 3
    F1 = sp.Rational(4, 3) * sp.sqrt(sp.sqrt(x) + 1) * (sp.sqrt(x) - 2)
    anti(F1, 1 / sp.sqrt(sp.sqrt(x) + 1))
    p3a1 = part("Find the antiderivative: (i) $\\displaystyle\\int\\dfrac{dx}{\\sqrt{\\sqrt x+1}}$.", 0.5,
                "$\\dfrac43\\sqrt{\\sqrt x+1}\\,(\\sqrt x-2)+C$.",
                ol("Let $t=\\sqrt x$, $x=t^2$, $dx=2t\\,dt$: $\\displaystyle\\int\\frac{2t\\,dt}{\\sqrt{t+1}}$.", "Let $w=t+1$: $\\displaystyle2\\int\\frac{w-1}{\\sqrt w}dw=2\\int\\left(w^{1/2}-w^{-1/2}\\right)dw=\\tfrac43w^{3/2}-4w^{1/2}$.",
                   "Back-substitute $w=\\sqrt x+1$: $\\tfrac43(\\sqrt x+1)^{3/2}-4(\\sqrt x+1)^{1/2}=\\tfrac43\\sqrt{\\sqrt x+1}\\,\\big(\\sqrt x+1-3\\big)=\\tfrac43\\sqrt{\\sqrt x+1}\\,(\\sqrt x-2)$.", "Check: differentiate and simplify to get back $\\dfrac1{\\sqrt{\\sqrt x+1}}$."),
                lab=dict(tool="check", f="1/sqrt(sqrt(x)+1)", F="4/3*sqrt(sqrt(x)+1)*(sqrt(x)-2)", ab=""))
    f2 = (2 * x ** 2 + 2 * x + 13) / ((x - 2) * (x ** 2 + 1) ** 2)
    ap = sp.apart(f2, x)
    F2 = sp.integrate(ap, x)
    anti(F2, f2)
    # decomposition coefficients (A/(x-2) + (Bx+C)/(x^2+1) + (Dx+E)/(x^2+1)^2)
    A_, B_, C_, D_, E_ = sp.symbols("A B C D E")
    eq = sp.expand(A_ * (x ** 2 + 1) ** 2 + (B_ * x + C_) * (x - 2) * (x ** 2 + 1) + (D_ * x + E_) * (x - 2) - (2 * x ** 2 + 2 * x + 13))
    sol = sp.solve(sp.Poly(eq, x).all_coeffs(), [A_, B_, C_, D_, E_], dict=True)[0]
    dec = "\\frac{%s}{x-2}+\\frac{%s}{x^2+1}+\\frac{%s}{(x^2+1)^2}" % (tex(sol[A_]), tex(sol[B_] * x + sol[C_]), tex(sol[D_] * x + sol[E_]))
    assert same(sol[A_] / (x - 2) + (sol[B_] * x + sol[C_]) / (x ** 2 + 1) + (sol[D_] * x + sol[E_]) / (x ** 2 + 1) ** 2, f2)
    p3a2 = part("(ii) $\\displaystyle\\int\\dfrac{2x^2+2x+13}{(x-2)(x^2+1)^2}\\,dx$.", 1, "$%s+C$" % tex(F2),
                ol("Partial fractions: $\\dfrac{2x^2+2x+13}{(x-2)(x^2+1)^2}=\\dfrac{A}{x-2}+\\dfrac{Bx+C}{x^2+1}+\\dfrac{Dx+E}{(x^2+1)^2}$ (the repeated irreducible quadratic needs two terms).",
                   "Cover-up at $x=2$: $A=\\dfrac{2\\cdot4+4+13}{(4+1)^2}=\\dfrac{25}{25}=1$. Matching the remaining coefficients (or comparing values) gives $%s$." % dec,
                   "Integrate term by term: $\\int\\frac{dx}{x-2}=\\ln|x-2|$; $\\int\\frac{x\\,dx}{x^2+1}=\\frac12\\ln(x^2+1)$; $\\int\\frac{dx}{x^2+1}=\\arctan x$; $\\int\\frac{dx}{(x^2+1)^2}=\\frac12\\left(\\arctan x+\\frac{x}{x^2+1}\\right)$ and $\\int\\frac{x\\,dx}{(x^2+1)^2}=-\\frac1{2(x^2+1)}$.",
                   "Result: $%s+C$ (verified by differentiating)." % tex(F2)),
                lab=dict(tool="check", f="(2*x^2+2*x+13)/((x-2)*(x^2+1)^2)", F=str(F2).replace("**", "^"), ab=""))
    F3 = (sp.atan((x - 3) / 2) + 2 * (x - 3) / (x ** 2 - 6 * x + 13)) / 16
    anti(F3, 1 / (x ** 2 - 6 * x + 13) ** 2)
    p3a3 = part("(iii) $\\displaystyle\\int\\dfrac{dx}{(x^2-6x+13)^2}$.", 0.5, "$\\dfrac1{16}\\left[\\arctan\\dfrac{x-3}{2}+\\dfrac{2(x-3)}{x^2-6x+13}\\right]+C$.",
                ol("Complete the square: $x^2-6x+13=(x-3)^2+4$.", "Let $x-3=2\\tan\\theta$, $dx=2\\sec^2\\theta\\,d\\theta$: $\\displaystyle\\int\\frac{2\\sec^2\\theta\\,d\\theta}{16\\sec^4\\theta}=\\frac18\\int\\cos^2\\theta\\,d\\theta=\\frac1{16}(\\theta+\\sin\\theta\\cos\\theta)$.",
                   "Back-substitute: $\\theta=\\arctan\\frac{x-3}{2}$ and $\\sin\\theta\\cos\\theta=\\dfrac{\\tan\\theta}{1+\\tan^2\\theta}=\\dfrac{(x-3)/2}{1+(x-3)^2/4}=\\dfrac{2(x-3)}{x^2-6x+13}$."),
                lab=dict(tool="check", f="1/(x^2-6*x+13)^2", F="(atan((x-3)/2)+2*(x-3)/(x^2-6*x+13))/16", ab=""))
    ya, yb = sp.symbols("a b", positive=True)
    yv = yb * (x / ya) ** 2 - ya ** 2 / (8 * yb) * sp.log(x / ya)
    yp = sp.diff(yv, x)
    root = 2 * yb * x / ya ** 2 + ya ** 2 / (8 * yb * x)
    assert sp.simplify(1 + yp ** 2 - root ** 2) == 0
    Larc = sp.simplify(sp.integrate(root, (x, ya, 3 * ya)))
    assert sp.simplify(Larc - (8 * yb + ya ** 2 / (8 * yb) * sp.log(3))) == 0
    p3b1 = part("(b)(i) Find the arc length of $\\dfrac yb=\\left(\\dfrac xa\\right)^2-\\dfrac18\\dfrac{a^2}{b^2}\\ln\\dfrac xa$ for $a\\le x\\le3a$, with $a,b>0$.", 1, "$L=8b+\\dfrac{a^2}{8b}\\ln3$.",
                 ol("$y=\\dfrac{b}{a^2}x^2-\\dfrac{a^2}{8b}\\ln\\dfrac xa$, so $y'=\\dfrac{2b}{a^2}x-\\dfrac{a^2}{8b\\,x}$.",
                    "$1+y'^2=1+\\dfrac{4b^2x^2}{a^4}-\\dfrac12+\\dfrac{a^4}{64b^2x^2}=\\dfrac{4b^2x^2}{a^4}+\\dfrac12+\\dfrac{a^4}{64b^2x^2}=\\left(\\dfrac{2b}{a^2}x+\\dfrac{a^2}{8b\\,x}\\right)^2$ — a perfect square (the cross term $2\\cdot\\frac{2bx}{a^2}\\cdot\\frac{a^2}{8bx}=\\frac12$).",
                    "$L=\\displaystyle\\int_a^{3a}\\left(\\frac{2b}{a^2}x+\\frac{a^2}{8b\\,x}\\right)dx=\\left[\\frac{b}{a^2}x^2+\\frac{a^2}{8b}\\ln x\\right]_a^{3a}=\\frac{b}{a^2}(9a^2-a^2)+\\frac{a^2}{8b}\\ln3=8b+\\frac{a^2}{8b}\\ln3$."))
    yy = sp.Rational(1, 3) * sp.sqrt(x) * (3 - x)
    Ssurf = sp.simplify(sp.integrate(sp.simplify(2 * sp.pi * yy * sp.sqrt(1 + sp.diff(yy, x) ** 2)), (x, 0, 3)))
    assert Ssurf == 3 * sp.pi
    p3b2 = part("(b)(ii) Find the surface area generated by rotating the arc $y=\\tfrac13\\sqrt x\\,(3-x)$, $0\\le x\\le3$, about the $x$-axis.", 1, "$S=3\\pi$.",
                ol("$y'=\\dfrac13\\left(\\dfrac{3-x}{2\\sqrt x}-\\sqrt x\\right)=\\dfrac{1-x}{2\\sqrt x}$.", "$1+y'^2=1+\\dfrac{(1-x)^2}{4x}=\\dfrac{(1+x)^2}{4x}$, so $\\sqrt{1+y'^2}=\\dfrac{1+x}{2\\sqrt x}$.",
                   "$S=2\\pi\\displaystyle\\int_0^3y\\sqrt{1+y'^2}\\,dx=2\\pi\\int_0^3\\frac13\\sqrt x(3-x)\\frac{1+x}{2\\sqrt x}dx=\\frac\\pi3\\int_0^3(3-x)(1+x)\\,dx=\\frac\\pi3\\int_0^3(3+2x-x^2)\\,dx=\\frac\\pi3\\cdot9=3\\pi$."))
    # ---- Problem 4
    kk = sp.Symbol("k", positive=True)
    val4 = sp.integrate(1 / (x * sp.log(x) ** 2), (x, 2, oo))
    assert numeq(val4, 1 / sp.log(2))
    p4 = part("Determine whether $\\displaystyle\\int_2^{\\infty}\\dfrac{dx}{x\\ln^kx}$ converges or diverges (the answer depends on $k$). If it converges, find its value.", 4,
              "Converges iff $k>1$, and then the value is $\\dfrac{(\\ln2)^{1-k}}{k-1}$.",
              ol("Substitute $u=\\ln x$, $du=\\dfrac{dx}x$; the limits become $\\ln2$ and $\\infty$: $\\displaystyle\\int_{\\ln2}^{\\infty}u^{-k}\\,du$.",
                 "<b>Case $k=1$:</b> $\\int\\frac{du}{u}=\\ln u\\to\\infty$: diverges.", "<b>Case $k\\ne1$:</b> $\\displaystyle\\int_{\\ln2}^{R}u^{-k}du=\\frac{R^{1-k}-(\\ln2)^{1-k}}{1-k}$.",
                 "If $k>1$, $R^{1-k}\\to0$, so the integral equals $\\dfrac{-(\\ln2)^{1-k}}{1-k}=\\dfrac{(\\ln2)^{1-k}}{k-1}$ (converges). If $k<1$, $R^{1-k}\\to\\infty$: diverges.",
                 "Check with $k=2$: $\\dfrac{(\\ln 2)^{-1}}{1}=\\dfrac1{\\ln2}\\approx1.4427$."))
    # ---- Problem 5
    n = sp.Symbol("n", positive=True, integer=True)
    ratio5 = sp.limit(sp.simplify(sp.simplify(sp.factorial(n + 1) ** 3 / sp.factorial(3 * n + 3)) / (sp.factorial(n) ** 3 / sp.factorial(3 * n))), n, oo)
    assert ratio5 == sp.Rational(1, 27)
    p5a = part("(a) Find the radius of convergence of $\\displaystyle\\sum_{n=1}^\\infty\\dfrac{(n!)^3}{(3n)!}x^n$.", 2, "$R=27$.",
               ol("Ratio test with $a_n=\\dfrac{(n!)^3}{(3n)!}$: $\\dfrac{a_{n+1}}{a_n}=\\dfrac{(n+1)^3}{(3n+3)(3n+2)(3n+1)}$ (because $(3n+3)!=(3n)!\\,(3n+1)(3n+2)(3n+3)$).",
                  "Divide by $n^3$: $\\dfrac{(1+1/n)^3}{(3+3/n)(3+2/n)(3+1/n)}\\to\\dfrac{1}{27}$.", "The series converges for $|x|\\cdot\\frac1{27}<1$, so $R=27$."))
    S5b = sp.summation((-1) ** (n + 1) / sp.sqrt(n), (n, 1, oo))
    assert S5b.is_real is not False
    p5b = part("(b) Find the radius and the interval of convergence of $\\displaystyle\\sum_{n=1}^\\infty\\dfrac{(-1)^{n+1}x^n}{\\sqrt n\\,2^n}$.", 2, "$R=2$; interval of convergence $(-2,\\,2]$.",
               ol("Ratio test: $\\left|\\dfrac{a_{n+1}}{a_n}\\right|=\\dfrac{|x|}{2}\\sqrt{\\dfrac n{n+1}}\\to\\dfrac{|x|}2<1\\iff|x|<2$, so $R=2$.",
                  "<b>Endpoint $x=2$:</b> $\\sum\\dfrac{(-1)^{n+1}}{\\sqrt n}$ — alternating, $\\frac1{\\sqrt n}\\downarrow0$: converges (conditionally; $\\sum\\frac1{\\sqrt n}$ diverges).",
                  "<b>Endpoint $x=-2$:</b> $(-1)^{n+1}\\dfrac{(-2)^n}{\\sqrt n2^n}=-\\dfrac1{\\sqrt n}$: $-\\sum\\frac1{\\sqrt n}$ diverges ($p=\\frac12\\le1$).", "Interval of convergence: $(-2,\\,2]$."),
               lab=dict(tool="series", a="(-1)^(n+1)/sqrt(n)", n0="1", N="60"))
    P.append(paper("mock-1", "Mock Test 1", "Final Calculus I · Academic year 2025–26 (real mock test)", 120,
                   [[p1a, p1b], [p2], [p3a1, p3a2, p3a3, p3b1, p3b2], [p4], [p5a, p5b]], note="Marks per part are our estimate (the real final has 5 questions of 4 points each). Duration assumed: 120 minutes."))

    # ================================================================= Mock B (final-style)
    assert parity(xr * sp.sin(xr), (0.5, 1.0, 2.0)) == "even" and parity(sp.log((1 - xr) / (1 + xr)), (0.2, 0.5, 0.9)) == "odd"
    assert parity(xr ** 2 + xr, (0.5, 1.0, 2.0)) == "neither" and parity(xr / sp.sqrt(1 + xr ** 2), (0.5, 1.0, 2.0)) == "odd"
    pB1a = part("Even, odd or neither? (i) $f(x)=x\\sin x$, (ii) $g(x)=\\ln\\dfrac{1-x}{1+x}$ on $(-1,1)$, (iii) $h(x)=x^2+x$, (iv) $k(x)=\\dfrac{x}{\\sqrt{1+x^2}}$.", 2, "(i) even; (ii) odd; (iii) neither; (iv) odd.",
                ol("(i) $(-x)\\sin(-x)=(-x)(-\\sin x)=x\\sin x$: odd × odd = <b>even</b>.", "(ii) $g(-x)=\\ln\\dfrac{1+x}{1-x}=-\\ln\\dfrac{1-x}{1+x}=-g(x)$: <b>odd</b> (domain $(-1,1)$ is symmetric).",
                   "(iii) $h(-x)=x^2-x$: not $h(x)$ and not $-h(x)$: <b>neither</b>.", "(iv) $k(-x)=\\dfrac{-x}{\\sqrt{1+x^2}}=-k(x)$: <b>odd</b>."))
    l1 = sp.limit((sp.tan(2 * x) - sp.sin(2 * x)) / x ** 3, x, 0); l2 = sp.limit(sp.sqrt(x ** 2 + 3 * x) - x, x, oo)
    assert l1 == 4 and l2 == sp.Rational(3, 2)
    pB1b = part("Find the limits: (i) $\\displaystyle\\lim_{x\\to0}\\dfrac{\\tan2x-\\sin2x}{x^3}$, (ii) $\\displaystyle\\lim_{x\\to\\infty}\\left(\\sqrt{x^2+3x}-x\\right)$.", 2, "(i) $4$; (ii) $\\dfrac32$.",
                ol("(i) $\\tan u-\\sin u=\\sin u\\,\\dfrac{1-\\cos u}{\\cos u}$. With $u=2x$ the quotient equals $\\dfrac{\\sin2x}{x}\\cdot\\dfrac{1-\\cos2x}{x^2}\\cdot\\dfrac1{\\cos2x}$. Now $\\dfrac{\\sin2x}{x}\\to2$, $\\dfrac{1-\\cos2x}{x^2}=4\\cdot\\dfrac{1-\\cos2x}{(2x)^2}\\to4\\cdot\\dfrac12=2$ and $\\dfrac1{\\cos2x}\\to1$, so the limit is $2\\cdot2\\cdot1=4$.",
                   "(ii) Multiply by the conjugate: $\\dfrac{3x}{\\sqrt{x^2+3x}+x}=\\dfrac3{\\sqrt{1+3/x}+1}\\to\\dfrac32$."),
                lab=dict(tool="limit", f="(tan(2*x)-sin(2*x))/x^3", a="0"))
    dist2 = xr ** 4 - 2 * xr ** 2 + sp.Rational(9, 4)
    assert sp.simplify(xr ** 2 + (xr ** 2 - sp.Rational(3, 2)) ** 2 - dist2) == 0 and sorted(sp.solve(sp.diff(dist2, xr), xr)) == [-1, 0, 1]
    assert dist2.subs(xr, 1) == sp.Rational(5, 4) and dist2.subs(xr, 0) == sp.Rational(9, 4)
    assert sp.diff(dist2, xr, 2).subs(xr, 0) == -4 and sp.diff(dist2, xr, 2).subs(xr, 1) == 8
    pB2 = part("Find the points of the parabola $y=x^2$ that are closest to the point $\\left(0,\\tfrac32\\right)$ and the minimal distance.", 4, "The points $(\\pm1,1)$; minimal distance $\\dfrac{\\sqrt5}{2}$.",
               ol("A point of the parabola is $(x,x^2)$. Minimise the <i>square</i> of the distance (same minimiser, no square root): $D(x)=x^2+\\left(x^2-\\tfrac32\\right)^2=x^4-2x^2+\\tfrac94$.",
                  "$D'(x)=4x^3-4x=4x(x-1)(x+1)=0\\Rightarrow x=0,\\pm1$.", "$D(0)=\\frac94$, $D(\\pm1)=1-2+\\frac94=\\frac54$. As $x\\to\\pm\\infty$, $D\\to\\infty$, so the absolute minimum is $\\frac54$ at $x=\\pm1$ ($x=0$ is a local <i>maximum</i>: $D''(0)=-4<0$, $D''(\\pm1)=8>0$).",
                  "<b>Answer:</b> closest points $(1,1)$ and $(-1,1)$, distance $\\sqrt{5/4}=\\dfrac{\\sqrt5}2\\approx1.118$."))
    FB1 = -sp.exp(-x) * (x ** 2 + 2 * x + 2); anti(FB1, x ** 2 * sp.exp(-x))
    pB3a1 = part("Evaluate (i) $\\displaystyle\\int x^2e^{-x}\\,dx$.", 1, "$-e^{-x}(x^2+2x+2)+C$.",
                 ol("Parts with $u=x^2$, $dv=e^{-x}dx$: $-x^2e^{-x}+\\int2x\\,e^{-x}dx$.", "Parts again with $u=2x$: $\\int2xe^{-x}dx=-2xe^{-x}+\\int2e^{-x}dx=-2xe^{-x}-2e^{-x}$.", "Total: $-e^{-x}\\left(x^2+2x+2\\right)+C$ (check by differentiating)."),
                 lab=dict(tool="check", f="x^2*exp(-x)", F="-exp(-x)*(x^2+2*x+2)", ab=""))
    FB2 = 2 * sp.log(x - 1) - sp.log(x + 1); anti(FB2, (x + 3) / (x ** 2 - 1), pts=(1.7, 2.3, 3.1))
    pB3a2 = part("(ii) $\\displaystyle\\int\\dfrac{x+3}{x^2-1}\\,dx$.", 1, "$2\\ln|x-1|-\\ln|x+1|+C$.",
                 ol("$\\dfrac{x+3}{(x-1)(x+1)}=\\dfrac A{x-1}+\\dfrac B{x+1}$. Cover-up: $A=\\dfrac{1+3}{1+1}=2$, $B=\\dfrac{-1+3}{-1-1}=-1$.", "Integrate: $2\\ln|x-1|-\\ln|x+1|+C$."))
    volx = sp.integrate(sp.pi * (x - x ** 4), (x, 0, 1)); voly = sp.integrate(2 * sp.pi * x * (sp.sqrt(x) - x ** 2), (x, 0, 1))
    assert volx == voly == 3 * sp.pi / 10
    pB3b = part("The region in the first quadrant between $y=x^2$ and $y=\\sqrt x$ is revolved (a) about the $x$-axis, (b) about the $y$-axis. Find both volumes.", 2, "Both volumes equal $\\dfrac{3\\pi}{10}$.",
                ol("The curves meet where $x^2=\\sqrt x\\iff x=0,1$; on $(0,1)$, $\\sqrt x\\ge x^2$.", "(a) Washers about the $x$-axis: outer radius $\\sqrt x$, inner radius $x^2$: $V=\\pi\\displaystyle\\int_0^1(x-x^4)\\,dx=\\pi\\left(\\tfrac12-\\tfrac15\\right)=\\tfrac{3\\pi}{10}$.",
                   "(b) Shells about the $y$-axis: radius $x$, height $\\sqrt x-x^2$: $V=2\\pi\\displaystyle\\int_0^1x(\\sqrt x-x^2)\\,dx=2\\pi\\left(\\tfrac25-\\tfrac14\\right)=\\tfrac{3\\pi}{10}$.", "They are equal because the region is symmetric about the line $y=x$ (swapping $x$ and $y$ swaps the two axes): a good consistency check."))
    iB1 = sp.integrate(1 / (x ** 2 + x), (x, 1, oo)); assert numeq(iB1, sp.log(2))
    pB4a = part("Evaluate $\\displaystyle\\int_1^\\infty\\dfrac{dx}{x^2+x}$.", 2, "$\\ln2$.",
                ol("$\\dfrac1{x(x+1)}=\\dfrac1x-\\dfrac1{x+1}$.", "$\\displaystyle\\int_1^R\\left(\\frac1x-\\frac1{x+1}\\right)dx=\\ln\\frac{x}{x+1}\\Big|_1^R=\\ln\\frac R{R+1}-\\ln\\frac12\\to0+\\ln2$.", "The integral converges to $\\ln 2$."))
    cmp_ok = all(((p_ + 1) / math.sqrt(p_ ** 5 + 2)) <= 2 * p_ ** -1.5 + 1e-12 for p_ in [1, 1.5, 2, 5, 10, 100])
    assert cmp_ok
    pB4b = part("Does $\\displaystyle\\int_1^\\infty\\dfrac{x+1}{\\sqrt{x^5+2}}\\,dx$ converge? Justify.", 2, "It converges.",
                ol("For $x\\ge1$: $x+1\\le2x$ and $\\sqrt{x^5+2}\\ge\\sqrt{x^5}=x^{5/2}$.", "So $0<\\dfrac{x+1}{\\sqrt{x^5+2}}\\le\\dfrac{2x}{x^{5/2}}=\\dfrac2{x^{3/2}}$.", "$\\int_1^\\infty\\frac{dx}{x^{3/2}}$ converges ($p=\\frac32>1$), so by the direct comparison test the given integral converges."))
    pB5a = part("Find the radius and the interval of convergence of $\\displaystyle\\sum_{n=1}^\\infty\\dfrac{(x+2)^n}{n\\,3^n}$.", 2, "$R=3$; interval $[-5,\\,1)$.",
                ol("Ratio test: $\\dfrac{|x+2|}{3}\\cdot\\dfrac{n}{n+1}\\to\\dfrac{|x+2|}3<1\\iff|x+2|<3$: $R=3$, centre $-2$, open interval $(-5,1)$.", "<b>$x=1$:</b> $\\sum\\frac{3^n}{n3^n}=\\sum\\frac1n$ diverges.", "<b>$x=-5$:</b> $\\sum\\frac{(-3)^n}{n3^n}=\\sum\\frac{(-1)^n}{n}$ converges (alternating harmonic).", "Interval of convergence $[-5,\\,1)$."))
    ser = sp.series(x * sp.exp(x ** 2), x, 0, 9).removeO()
    assert [ser.coeff(x, i) for i in (1, 3, 5, 7)] == [1, 1, sp.Rational(1, 2), sp.Rational(1, 6)]
    f7 = sp.diff(x * sp.exp(x ** 2), x, 7).subs(x, 0); assert f7 == 840
    pB5b = part("Find the Maclaurin series of $f(x)=xe^{x^2}$ up to the term in $x^7$ and deduce $f^{(7)}(0)$.", 2, "$x+x^3+\\dfrac{x^5}{2}+\\dfrac{x^7}{6}+\\cdots$; $f^{(7)}(0)=840$.",
                ol("Substitute $x^2$ into $e^u=\\sum\\frac{u^n}{n!}$: $e^{x^2}=1+x^2+\\frac{x^4}{2}+\\frac{x^6}{6}+\\cdots$.", "Multiply by $x$: $xe^{x^2}=\\sum_{n\\ge0}\\dfrac{x^{2n+1}}{n!}=x+x^3+\\dfrac{x^5}2+\\dfrac{x^7}6+\\cdots$.", "The coefficient of $x^7$ is $\\frac{f^{(7)}(0)}{7!}=\\frac16$, so $f^{(7)}(0)=\\frac{5040}{6}=840$."),
                lab=dict(tool="taylor", f="x*exp(x^2)", a="0", n="7", x0="0.5", range="-2, 2"))
    P.append(paper("mock-B", "Final-style mock B", "Calculus I · same format as the final (5 questions, 20 marks)", 120,
                   [[pB1a, pB1b], [pB2], [pB3a1, pB3a2, pB3b], [pB4a, pB4b], [pB5a, pB5b]], note="Written by us in the style of the course problems; not an official paper."))

    # ================================================================= Mock C (final-style)
    pC1a = part("(i) Prove by the $\\varepsilon$–$\\delta$ definition that $\\displaystyle\\lim_{x\\to2}(3x-1)=5$. (ii) Evaluate $\\displaystyle\\lim_{x\\to1}\\dfrac{x^3-1}{x^2-1}$.", 2, "(i) $\\delta=\\varepsilon/3$ works; (ii) $\\dfrac32$.",
                ol("(i) Given $\\varepsilon>0$ let $\\delta=\\dfrac\\varepsilon3$. If $0<|x-2|<\\delta$ then $|(3x-1)-5|=3|x-2|<3\\delta=\\varepsilon$. ∎", "(ii) $\\dfrac{x^3-1}{x^2-1}=\\dfrac{(x-1)(x^2+x+1)}{(x-1)(x+1)}=\\dfrac{x^2+x+1}{x+1}\\to\\dfrac32$ (cancel the zero factor $x-1\\neq0$)."))
    aa, bb = sp.symbols("a b")
    solc = sp.solve([sp.Eq(aa + 1, 1 + bb), sp.Eq(4 + bb, 6 - aa)], [aa, bb], dict=True)[0]; assert solc == {aa: 1, bb: 1}
    pC1b = part("Find $a,b$ so that $f(x)=\\begin{cases}ax+1,&x<1\\\\x^2+b,&1\\le x<2\\\\3x-a,&x\\ge2\\end{cases}$ is continuous at every $x$.", 2, "$a=1$, $b=1$.",
                ol("Each piece is a polynomial, so only the junctions $x=1$ and $x=2$ matter.", "At $x=1$: left limit $a+1$, value and right limit $1+b$: $a+1=1+b\\Rightarrow b=a$.", "At $x=2$: left limit $4+b$, value $6-a$: $4+b=6-a\\Rightarrow a+b=2$.",
                   "With $b=a$: $2a=2$, so $a=1$, $b=1$. Check: $f$ takes the values $2$ at $x=1$ and $5$ at $x=2$ from both sides."))
    Rr, hh = sp.symbols("R h", positive=True)
    Vh = sp.pi * (Rr ** 2 - hh ** 2 / 4) * hh
    hs = sp.solve(sp.diff(Vh, hh), hh)[0]; assert sp.simplify(hs - 2 * Rr / sp.sqrt(3)) == 0
    Vmax = sp.simplify(Vh.subs(hh, hs)); assert sp.simplify(Vmax - 4 * sp.pi * Rr ** 3 / (3 * sp.sqrt(3))) == 0
    pC2 = part("A right circular cylinder is inscribed in a sphere of radius $R$. Find the dimensions of the cylinder of largest volume and that volume.", 4, "$h=\\dfrac{2R}{\\sqrt3}$, $r=R\\sqrt{\\tfrac23}$, $V_{\\max}=\\dfrac{4\\pi R^3}{3\\sqrt3}$.",
               ol("Let the cylinder have height $h$ and radius $r$; its axis passes through the centre, so $r^2+\\left(\\frac h2\\right)^2=R^2$ (Pythagoras).", "$V=\\pi r^2h=\\pi\\left(R^2-\\dfrac{h^2}4\\right)h=\\pi\\left(R^2h-\\dfrac{h^3}{4}\\right)$, domain $0<h<2R$.",
                  "$V'(h)=\\pi\\left(R^2-\\dfrac34h^2\\right)=0\\Rightarrow h=\\dfrac{2R}{\\sqrt3}$. $V''=-\\frac{3\\pi}2h<0$, and $V\\to0$ at both ends, so this is the maximum.",
                  "Then $r^2=R^2-\\frac{h^2}4=R^2-\\frac{R^2}3=\\frac{2R^2}3$, $r=R\\sqrt{2/3}$, and $V=\\pi\\cdot\\frac{2R^2}3\\cdot\\frac{2R}{\\sqrt3}=\\dfrac{4\\pi R^3}{3\\sqrt3}\\approx0.7698\\,R^3$."))
    iC1 = sp.integrate(sp.sin(x) ** 2 * sp.cos(x) ** 2, (x, 0, sp.pi / 2)); assert iC1 == sp.pi / 16
    pC3a1 = part("Evaluate (i) $\\displaystyle\\int_0^{\\pi/2}\\sin^2x\\cos^2x\\,dx$.", 1, "$\\dfrac\\pi{16}$.",
                 ol("$\\sin x\\cos x=\\frac12\\sin2x$, so $\\sin^2x\\cos^2x=\\frac14\\sin^22x=\\frac18(1-\\cos4x)$.", "$\\displaystyle\\int_0^{\\pi/2}\\frac18(1-\\cos4x)\\,dx=\\frac18\\left[x-\\frac{\\sin4x}{4}\\right]_0^{\\pi/2}=\\frac18\\cdot\\frac\\pi2=\\frac\\pi{16}$."))
    FC2 = -sp.sqrt(4 - x ** 2) / (4 * x); anti(FC2, 1 / (x ** 2 * sp.sqrt(4 - x ** 2)), pts=(0.4, 0.9, 1.4, 1.8))
    pC3a2 = part("(ii) $\\displaystyle\\int\\dfrac{dx}{x^2\\sqrt{4-x^2}}$ for $0<x<2$.", 1, "$-\\dfrac{\\sqrt{4-x^2}}{4x}+C$.",
                 ol("Trigonometric substitution $x=2\\sin\\theta$, $dx=2\\cos\\theta\\,d\\theta$, $\\sqrt{4-x^2}=2\\cos\\theta$.", "$\\displaystyle\\int\\frac{2\\cos\\theta\\,d\\theta}{4\\sin^2\\theta\\cdot2\\cos\\theta}=\\frac14\\int\\csc^2\\theta\\,d\\theta=-\\frac14\\cot\\theta$.", "From the right triangle ($\\sin\\theta=\\frac x2$): $\\cot\\theta=\\dfrac{\\sqrt{4-x^2}}{x}$. Hence $-\\dfrac{\\sqrt{4-x^2}}{4x}+C$."),
                 lab=dict(tool="check", f="1/(x^2*sqrt(4-x^2))", F="-sqrt(4-x^2)/(4*x)", ab=""))
    lnc = sp.integrate(sp.sec(x), (x, 0, sp.pi / 4)); assert numeq(lnc, sp.log(1 + sp.sqrt(2)))
    assert sp.simplify(1 + sp.diff(sp.log(sp.cos(x)), x) ** 2 - sp.sec(x) ** 2) == 0
    pC3b = part("Find the length of the curve $y=\\ln(\\cos x)$ for $0\\le x\\le\\dfrac\\pi4$.", 2, "$L=\\ln\\left(1+\\sqrt2\\right)\\approx0.8814$.",
                ol("$y'=-\\tan x$, so $1+y'^2=1+\\tan^2x=\\sec^2x$ and $\\sqrt{1+y'^2}=\\sec x$ (positive on $[0,\\frac\\pi4]$).", "$L=\\displaystyle\\int_0^{\\pi/4}\\sec x\\,dx=\\ln|\\sec x+\\tan x|\\Big|_0^{\\pi/4}=\\ln(\\sqrt2+1)-\\ln1=\\ln(1+\\sqrt2)\\approx0.8814$."))
    pp = sp.Symbol("p", real=True)
    vC = sp.integrate(x ** 2 * sp.log(x), (x, 0, 1)); assert vC == sp.Rational(-1, 9)
    pC4a = part("For which $p$ does $\\displaystyle\\int_0^1x^{p}\\ln x\\,dx$ converge? Find its value.", 2, "Converges iff $p>-1$; value $-\\dfrac1{(p+1)^2}$.",
                ol("By parts ($u=\\ln x$, $dv=x^pdx$, $p\\ne-1$): $\\displaystyle\\int x^p\\ln x\\,dx=\\frac{x^{p+1}}{p+1}\\ln x-\\frac{x^{p+1}}{(p+1)^2}$.", "As $x\\to0^+$: if $p+1>0$, $x^{p+1}\\ln x\\to0$ and $x^{p+1}\\to0$; the value at $x=1$ is $-\\frac{1}{(p+1)^2}$. So the integral equals $-\\dfrac1{(p+1)^2}$.",
                   "If $p+1<0$ the term $\\frac{x^{p+1}}{p+1}\\ln x$ blows up (the integrand is not integrable at $0$); if $p=-1$: $\\int\\frac{\\ln x}{x}=\\frac{\\ln^2x}{2}\\to\\infty$. Both diverge.", "Check: $p=2$ gives $-\\frac19$, which matches $\\int_0^1x^2\\ln x\\,dx=-\\frac19$."))
    iC4 = sp.integrate(1 / (x ** 2 + 2 * x + 5), (x, -oo, oo)); assert numeq(iC4, sp.pi / 2)
    pC4b = part("Evaluate $\\displaystyle\\int_{-\\infty}^{\\infty}\\dfrac{dx}{x^2+2x+5}$.", 2, "$\\dfrac\\pi2$.",
                ol("Complete the square: $x^2+2x+5=(x+1)^2+4$.", "$\\displaystyle\\int\\frac{dx}{(x+1)^2+4}=\\frac12\\arctan\\frac{x+1}{2}$.", "Both ends converge: $\\frac12\\left[\\frac\\pi2-\\left(-\\frac\\pi2\\right)\\right]=\\frac\\pi2$."))
    nn = np_ = None
    asum = lambda m: (-1) ** m * m / (m ** 2 + 1)
    abs_diverge = sp.limit(sp.Symbol("n", positive=True) * (sp.Symbol("n", positive=True) / (sp.Symbol("n", positive=True) ** 2 + 1)), sp.Symbol("n", positive=True), oo) == 1
    assert abs_diverge
    bn = lambda m: m / (m ** 2 + 1)
    assert all(bn(m + 1) < bn(m) for m in range(2, 2000))
    pC5a = part("Does $\\displaystyle\\sum_{n=1}^\\infty\\dfrac{(-1)^nn}{n^2+1}$ converge absolutely, converge conditionally, or diverge?", 2, "It converges conditionally (not absolutely).",
                ol("<b>Absolute convergence?</b> $\\sum\\dfrac{n}{n^2+1}$: limit comparison with $\\sum\\frac1n$: $\\dfrac{n/(n^2+1)}{1/n}=\\dfrac{n^2}{n^2+1}\\to1$, and $\\sum\\frac1n$ diverges, so $\\sum|a_n|$ diverges.",
                   "<b>Convergence?</b> $b_n=\\dfrac n{n^2+1}\\to0$ and $b_{n+1}<b_n$ for $n\\ge2$ ($b_n'=\\frac{1-x^2}{(x^2+1)^2}<0$ for $x>1$), so the Alternating Series Test shows that $\\sum(-1)^nb_n$ converges.", "Hence conditional convergence."))
    P3 = 0.1 - 0.1 ** 2 / 2 + 0.1 ** 3 / 3; err = abs(math.log(1.1) - P3); assert err < 2.5e-5
    pC5b = part("Find the Taylor polynomial of degree $3$ of $f(x)=\\ln x$ about $a=1$, use it to approximate $\\ln1.1$, and bound the error.", 2, "$P_3(x)=(x-1)-\\dfrac{(x-1)^2}{2}+\\dfrac{(x-1)^3}{3}$; $\\ln1.1\\approx0.09533$; $|R_3|\\le2.5\\times10^{-5}$.",
                ol("$f'=\\frac1x$, $f''=-\\frac1{x^2}$, $f'''=\\frac2{x^3}$: at $1$: $f=0$, $f'=1$, $f''=-1$, $f'''=2$. So $P_3(x)=(x-1)-\\dfrac{(x-1)^2}{2}+\\dfrac{2}{3!}(x-1)^3=(x-1)-\\dfrac{(x-1)^2}2+\\dfrac{(x-1)^3}3$.",
                   "$P_3(1.1)=0.1-0.005+0.000333\\ldots\\approx0.095333$.", "Lagrange: $f^{(4)}(x)=-\\dfrac6{x^4}$, so for $c\\in[1,1.1]$: $|f^{(4)}(c)|\\le6$ and $|R_3(1.1)|\\le\\dfrac{6}{4!}\\,(0.1)^4=\\dfrac{(0.1)^4}{4}=2.5\\times10^{-5}$.",
                   "Check: $\\ln1.1=0.0953102\\ldots$, actual error $\\approx2.3\\times10^{-5}\\le2.5\\times10^{-5}$ ✓."),
                lab=dict(tool="taylor", f="log(x)", a="1", n="3", x0="1.1", range="0.2, 2"))
    P.append(paper("mock-C", "Final-style mock C", "Calculus I · same format as the final (5 questions, 20 marks)", 120,
                   [[pC1a, pC1b], [pC2], [pC3a1, pC3a2, pC3b], [pC4a, pC4b], [pC5a, pC5b]], note="Written by us in the style of the course problems; not an official paper."))
    return P

if __name__ == "__main__":
    ps = build_papers()
    for p in ps:
        tot = sum(pt["marks"] for q in p["problems"] for pt in q)
        print(p["id"], len(p["problems"]), "problems", sum(len(q) for q in p["problems"]), "parts", tot, "marks")
