# -*- coding: utf-8 -*-
"""Calculus I chapter 1: functions, limits, continuity (Lectures 1-3, Tutorials 1-3, Computation problems 1-3, Mock Test 1)."""
import math, random
import sympy as sp
from qlib import tex, uniq_by_text, near_numbers, R, note
from cal_common import *

oo = sp.oo

def cbrt(e):
    return sp.real_root(e, 3)

# ----------------------------------------------------------------------------- helpers
def limq(B, ch, level, stem_expr, expr, var, pt, direction, expected, method, src, origin="src", extras=(), lead="Evaluate"):
    """Compute the limit with sympy, assert it equals the hand-derived value, and add the question."""
    val = sp.limit(expr, var, pt, direction) if direction else sp.limit(expr, var, pt)
    assert sp.simplify(val - expected) == 0 or val == expected, (src, stem_expr, val, expected)
    side = {"+": "^{+}", "-": "^{-}", None: ""}[direction]
    ptx = tex(pt) if pt not in (oo, -oo) else ("\\infty" if pt == oo else "-\\infty")
    stem = "%s $\\displaystyle\\lim_{%s\\to %s%s}%s$." % (lead, tex(var), ptx, side, stem_expr)
    c, wr = lim_options(val, B.rng, extras)
    B.mcq(ch, "Limits", level, stem, c, wr, method + " Result: %s." % c, src, origin)
    return val

def parity(f, var=x, pts=(0.3, 0.8, 1.7, 2.9)):
    ev = od = True
    for p in pts:
        a, b = sp.N(f.subs(var, p)), sp.N(f.subs(var, -p))
        if abs(a - b) > 1e-9: ev = False
        if abs(a + b) > 1e-9: od = False
    return "Both even and odd" if ev and od else "Even" if ev else "Odd" if od else "Neither even nor odd"

PAR_OPTS = ["Even", "Odd", "Neither even nor odd", "Both even and odd"]

# ============================================================================== CHAPTER 1
def ch1(B):
    ch = "c1"; rng = B.rng

    # ---- parity (Mock Test 1 Q1(a); Computation #1 Q6, Q11, Q12)
    for lbl, g, expect, src in [("g(x)=\\dfrac{|x|}{x}", sp.Abs(x) / x, "Odd", "Mock Test 1, Q1(a)(i)"),
                                ("g(x)=\\dfrac{1}{\\sqrt{1-x^{2}}}", 1 / sp.sqrt(1 - x ** 2), "Even", "Mock Test 1, Q1(a)(ii)"),
                                ("g(x)=\\dfrac{x-1}{x+1}", (x - 1) / (x + 1), "Neither even nor odd", "Mock Test 1, Q1(a)(iii)"),
                                ("g(x)=1+\\sin x", 1 + sp.sin(x), "Neither even nor odd", "Mock Test 1, Q1(a)(iv)")]:
        got = parity(g); assert got == expect, (lbl, got)
        gm = sp.simplify(g.subs(x, -x))
        dom_note = {"Mock Test 1, Q1(a)(i)": " The domain $x\\ne0$ is symmetric about $0$.", "Mock Test 1, Q1(a)(ii)": " The domain $(-1,1)$ is symmetric about $0$.",
                    "Mock Test 1, Q1(a)(iii)": " Moreover the domain $x\\ne-1$ is not symmetric about $0$ ($x=1$ is allowed but $x=-1$ is not), which already rules out both symmetries.",
                    "Mock Test 1, Q1(a)(iv)": ""}[src]
        B.mcq(ch, "Even and odd functions", 1, "Is $%s$ even, odd, or neither?" % lbl, expect, [o for o in PAR_OPTS if o != expect],
              "Compute $g(-x)=%s$ and compare with $g(x)$: %s.%s" % (tex(gm), {
                  "Odd": "$g(-x)=-g(x)$, so $g$ is odd", "Even": "$g(-x)=g(x)$, so $g$ is even", "Neither even nor odd": "$g(-x)$ equals neither $g(x)$ nor $-g(x)$"}[expect], dom_note), src, "src")
    # parity algebra: f even, g odd (both defined on R)
    f1, g1 = sp.cos(x) + x ** 2, sp.sin(x) + x ** 3
    f2, g2 = x ** 4 + 1, x ** 5 - x
    PA = [("fg", lambda f, g: f * g, "Odd"), ("f/g", lambda f, g: f / g, "Odd"), ("g/f", lambda f, g: g / f, "Odd"), ("f^2", lambda f, g: f ** 2, "Even"),
          ("g^2", lambda f, g: g ** 2, "Even"), ("f\\circ g", lambda f, g: f.subs(x, g), "Even"), ("g\\circ f", lambda f, g: g.subs(x, f), "Even"),
          ("f\\circ f", lambda f, g: f.subs(x, f), "Even"), ("g\\circ g", lambda f, g: g.subs(x, g), "Odd")]
    for lbl, op, expect in PA:
        r1, r2 = parity(op(f1, g1)), parity(op(f2, g2))
        assert r1 == r2 == expect, (lbl, r1, r2, expect)
    for lbl, op, expect in PA:
        got = parity(op(f1, g1))
        reason = {"fg": "even·odd: $(fg)(-x)=f(x)\\cdot(-g(x))=-(fg)(x)$", "f/g": "$(f/g)(-x)=f(x)/(-g(x))=-(f/g)(x)$", "g/f": "$(g/f)(-x)=-g(x)/f(x)=-(g/f)(x)$",
                  "f^2": "$f(-x)^2=f(x)^2$", "g^2": "$g(-x)^2=(-g(x))^2=g(x)^2$", "f\\circ g": "$f(g(-x))=f(-g(x))=f(g(x))$ because $f$ is even",
                  "g\\circ f": "$g(f(-x))=g(f(x))$ because $f(-x)=f(x)$, so it is even", "f\\circ f": "$f(f(-x))=f(f(x))$", "g\\circ g": "$g(g(-x))=g(-g(x))=-g(g(x))$"}[lbl]
        B.mcq(ch, "Even and odd functions", 2, "Let $f$ be even and $g$ odd, both defined on all of $\\mathbb{R}$. Where defined, the function $%s$ is" % lbl, got, [o for o in PAR_OPTS if o != got],
              "%s." % reason, "Computation problems 1, Q6", "src")
    B.mcq(ch, "Even and odd functions", 2, "If $f$ is odd, is $g(x)=f(x)-2$ also odd?", "No: $g(-x)=-f(x)-2\\neq-g(x)=-f(x)+2$",
          ["Yes: subtracting a constant keeps oddness", "Yes: $g(0)=0$", "Only if $f(0)=2$"],
          "Oddness requires $g(-x)=-g(x)$. Here $g(-x)=f(-x)-2=-f(x)-2$ while $-g(x)=-f(x)+2$: they differ by $4$.", "Computation problems 1, Q11", "src")
    B.mcq(ch, "Even and odd functions", 2, "If $f$ is even, is $g(x)=f(x)-2$ even?", "Yes: $g(-x)=f(-x)-2=f(x)-2=g(x)$",
          ["No: subtracting a constant destroys evenness", "Only if $f(0)=2$", "No: $g$ becomes odd"], "A constant shift does not change the symmetry about the $y$-axis.", "Computation problems 1, Q11", "src")
    B.mcq(ch, "Even and odd functions", 2, "If a function $f$ is both even and odd, then", "$f(x)=0$ for every $x$ in its domain",
          ["$f(x)=x$", "$f(x)=1$", "such a function does not exist"], "$f(-x)=f(x)$ and $f(-x)=-f(x)$ give $f(x)=-f(x)$, hence $f(x)=0$.", "Computation problems 1, Q12", "src")

    # ---- compositions (Computation #1 Q4)
    u = lambda e: 4 * e - 5; v = lambda e: e ** 2; f = lambda e: 1 / e
    COMP = [("u(v(f(x)))", u(v(f(x)))), ("u(f(v(x)))", u(f(v(x)))), ("v(u(f(x)))", v(u(f(x)))), ("v(f(u(x)))", v(f(u(x)))), ("f(u(v(x)))", f(u(v(x)))), ("f(v(u(x)))", f(v(u(x))))]
    for lbl, val in COMP:
        wr = [w for nm, w in COMP if not num_equal(w, val)]
        wr += [u(v(x)) * f(x), v(u(x)) / x]
        mc_expr(B, ch, "Composition", 2, "With $u(x)=4x-5$, $v(x)=x^2$ and $f(x)=1/x$, compute $%s$." % lbl, sp.simplify(val), [sp.simplify(w) for w in wr],
                "Work from the inside out. $%s=%s$." % (lbl, tex(val)), "Computation problems 1, Q4", "src")
    fa = lambda e: e - 3; ga = sp.sqrt; ha = lambda e: e ** 3; ja = lambda e: 2 * e
    DEC = [("y=\\sqrt{x-3}", "g\\circ f", sp.sqrt(x - 3)), ("y=2\\sqrt{x}", "j\\circ g", 2 * sp.sqrt(x)), ("y=x^{1/4}", "g\\circ g", x ** sp.Rational(1, 4)),
           ("y=4x", "j\\circ j", 4 * x), ("y=\\sqrt{(x-3)^{3}}", "g\\circ h\\circ f", sp.sqrt((x - 3) ** 3)), ("y=(2x-6)^{3}", "h\\circ j\\circ f", (2 * x - 6) ** 3)]
    SYM = {"f": fa, "g": ga, "h": ha, "j": ja}
    def build(name):
        parts = name.replace("\\circ", " ").split()
        e = x
        for p in reversed(parts):
            e = SYM[p](e)
        return e
    allnames = ["f\\circ g", "g\\circ f", "g\\circ j", "j\\circ g", "g\\circ g", "j\\circ j", "h\\circ f", "g\\circ h\\circ f", "h\\circ g\\circ f", "h\\circ j\\circ f", "j\\circ h\\circ f", "f\\circ j\\circ h"]
    for lbl, nm, val in DEC:
        assert num_equal(build(nm), val), (nm, val)
        wr = [w for w in allnames if not num_equal(build(w), val) and w != nm]
        rng.shuffle(wr)
        B.mcq(ch, "Composition", 2, "With $f(x)=x-3$, $g(x)=\\sqrt{x}$, $h(x)=x^3$, $j(x)=2x$: which composite equals $%s$?" % lbl, "$%s$" % nm, ["$%s$" % w for w in wr[:3]],
              "Evaluate the composite from the right: $%s(x)=%s$." % (nm, tex(build(nm))), "Computation problems 1, Q5", "src")
    B.mcq(ch, "Composition", 2, "If $A(x)=1.04x$ (a 4% annual increase), the $n$-fold composition $A\\circ A\\circ\\cdots\\circ A$ is", "$1.04^{n}x$", ["$1.04\\,n\\,x$", "$(1+0.04n)x$", "$1.04x^{n}$"],
          "$A(A(x))=1.04^2x$, $A^3(x)=1.04^3x$, … so $A^{n}(x)=1.04^{n}x$ (compound interest).", "Tutorial 1, Q9", "src")
    assert sp.Rational("1.04") ** 3 == sp.Rational("1.124864")
    B.mcq(ch, "Composition", 2, "With $A(x)=1.04x$, what is $(A\\circ A\\circ A)(x)$?", "$1.124864\\,x$", ["$1.12\\,x$", "$1.0816\\,x$", "$3.12\\,x$"],
          "$A(A(A(x)))=1.04\\cdot1.04\\cdot1.04\\,x=1.04^3x=1.124864\\,x$.", "Tutorial 1, Q9", "src")

    # ---- trig (Computation #1 Q7-Q9)
    s0 = sp.Rational(3, 5)  # x in (pi/2, pi)
    cosv, tanv = -sp.sqrt(1 - s0 ** 2), -s0 / sp.sqrt(1 - s0 ** 2)
    assert cosv == sp.Rational(-4, 5) and tanv == sp.Rational(-3, 4)
    mc_val(B, ch, "Trigonometry", 1, "If $\\sin x=\\frac35$ and $x\\in(\\frac{\\pi}{2},\\pi)$, find $\\cos x$.", cosv, [sp.Rational(4, 5), sp.Rational(3, 4), -sp.Rational(3, 4)],
           "$\\cos^2x=1-\\frac9{25}=\\frac{16}{25}$; in the second quadrant cosine is negative, so $\\cos x=-\\frac45$.", "Computation problems 1, Q7", "src")
    mc_val(B, ch, "Trigonometry", 1, "If $\\sin x=\\frac35$ and $x\\in(\\frac{\\pi}{2},\\pi)$, find $\\tan x$.", tanv, [sp.Rational(3, 4), sp.Rational(4, 3), -sp.Rational(4, 3)],
           "$\\tan x=\\sin x/\\cos x=\\frac{3/5}{-4/5}=-\\frac34$.", "Computation problems 1, Q7", "src")
    c8 = sp.Rational(1, 3); s8 = -sp.sqrt(1 - c8 ** 2); t8 = s8 / c8
    mc_val(B, ch, "Trigonometry", 2, "If $\\cos x=\\frac13$ and $x\\in(-\\frac{\\pi}{2},0)$, find $\\sin x$.", s8, [sp.sqrt(8) / 3, sp.Rational(2, 3), -sp.Rational(2, 3)],
           "$\\sin^2x=1-\\frac19=\\frac89$; in the fourth quadrant sine is negative: $\\sin x=-\\frac{2\\sqrt2}{3}$.", "Computation problems 1, Q8", "src")
    mc_val(B, ch, "Trigonometry", 2, "If $\\cos x=\\frac13$ and $x\\in(-\\frac{\\pi}{2},0)$, find $\\tan x$.", t8, [2 * sp.sqrt(2), -sp.sqrt(2), sp.Rational(1, 2)],
           "$\\tan x=\\sin x/\\cos x=-\\frac{2\\sqrt2}{3}\\cdot3=-2\\sqrt2$.", "Computation problems 1, Q8", "src")
    t9 = sp.Rational(1, 2); c9 = -1 / sp.sqrt(1 + t9 ** 2); s9 = t9 * c9
    mc_val(B, ch, "Trigonometry", 2, "If $\\tan x=\\frac12$ and $x\\in(\\pi,\\frac{3\\pi}{2})$, find $\\sin x$.", s9, [1 / sp.sqrt(5), sp.Rational(1, 2), -2 / sp.sqrt(5)],
           "$\\sec^2x=1+\\tan^2x=\\frac54$, $\\cos x=-\\frac{2}{\\sqrt5}$ (third quadrant), $\\sin x=\\tan x\\cos x=-\\frac1{\\sqrt5}$.", "Computation problems 1, Q9", "src")

    # ---- domains (generated, computed with solveset)
    DOM = [("\\sqrt{x^{2}-4}", x ** 2 - 4 >= 0), ("\\ln(x^{2}-1)", x ** 2 - 1 > 0), ("\\dfrac{1}{x^{2}-x-6}", sp.Ne(x ** 2 - x - 6, 0)),
           ("\\sqrt{4-x^{2}}", 4 - x ** 2 >= 0), ("\\sqrt{x+3}\\,/\\,(x-1)", None), ("\\ln(3-x)", 3 - x > 0)]
    for lbl, cond in DOM:
        if cond is None:
            S = sp.Interval(-3, sp.oo) - {1}
        else:
            S = sp.solveset(cond, x, sp.S.Reals)
        bad = []
        if lbl.startswith("\\sqrt{x^{2}-4}"):
            bad = [sp.solveset(x ** 2 - 4 > 0, x, sp.S.Reals), sp.Interval(-2, 2), sp.Interval(2, sp.oo)]
        elif lbl.startswith("\\ln(x^{2}-1)"):
            bad = [sp.solveset(x ** 2 - 1 >= 0, x, sp.S.Reals), sp.Interval.open(-1, 1), sp.Interval.open(1, sp.oo)]
        elif lbl.startswith("\\dfrac"):
            bad = [sp.S.Reals - {3}, sp.S.Reals - {2, -3}, sp.S.Reals - {-2}]
        elif lbl.startswith("\\sqrt{4"):
            bad = [sp.Interval.open(-2, 2), sp.Interval(0, 2), sp.S.Reals - {-2, 2}]
        elif lbl.startswith("\\sqrt{x+3}"):
            bad = [sp.Interval(-3, sp.oo), sp.Interval.open(-3, sp.oo) - {1}, sp.S.Reals - {1}]
        else:
            bad = [sp.Interval(-sp.oo, 3), sp.Interval.open(3, sp.oo), sp.S.Reals]
        bad = [b for b in bad if b != S]
        B.mcq(ch, "Domain", 1, "Find the domain of $f(x)=%s$." % lbl, interval_tex(S), [interval_tex(b) for b in bad],
              {"\\sqrt{x^{2}-4}": "Need $x^2-4\\ge0$, i.e. $|x|\\ge2$.", "\\ln(x^{2}-1)": "Need $x^2-1>0$, i.e. $|x|>1$ (strict because $\\ln0$ is undefined).",
               "\\dfrac{1}{x^{2}-x-6}": "Need $x^2-x-6=(x-3)(x+2)\\ne0$, so $x\\ne3,-2$.", "\\sqrt{4-x^{2}}": "Need $4-x^2\\ge0$, i.e. $-2\\le x\\le2$.",
               "\\sqrt{x+3}\\,/\\,(x-1)": "Need $x+3\\ge0$ and $x\\ne1$.", "\\ln(3-x)": "Need $3-x>0$, i.e. $x<3$."}[lbl], "Generated (Lecture 1: domain)", "gen")

    # ---- transformations of graphs (Tutorial 1 Q7)
    TR = [("y=f(x-4)", "shift $4$ units to the right", ["shift $4$ units to the left", "shift $4$ units up", "shift $4$ units down"]),
          ("y=f(x)+3", "shift $3$ units up", ["shift $3$ units to the right", "shift $3$ units to the left", "shift $3$ units down"]),
          ("y=\\tfrac13f(x)", "compress vertically by the factor $\\tfrac13$", ["stretch vertically by the factor $3$", "compress horizontally by the factor $\\tfrac13$", "reflect in the $x$-axis"]),
          ("y=-f(x+4)", "shift $4$ units left, then reflect in the $x$-axis", ["shift $4$ units right, then reflect in the $x$-axis", "shift $4$ units left, then reflect in the $y$-axis", "shift $4$ units down"]),
          ("y=2f(x+6)", "shift $6$ units left, then stretch vertically by $2$", ["shift $6$ units right, then stretch vertically by $2$", "shift $6$ units left, then compress vertically by $2$", "shift $6$ units up, then stretch vertically by $2$"])]
    for lbl, ans, wr in TR:
        B.mcq(ch, "Transformations of graphs", 1, "The graph of $%s$ is obtained from the graph of $y=f(x)$ by" % lbl, ans, wr,
              "Changes inside the argument act horizontally and 'backwards' ($x-a$ moves right by $a$); changes outside act vertically.", "Tutorial 1, Q7", "src")

    # ---- box and cone (Tutorial 1 Q5, Q6)
    Vx = sp.expand(x * (14 - 2 * x) * (22 - 2 * x)); assert Vx == 4 * x ** 3 - 72 * x ** 2 + 308 * x
    B.mcq(ch, "Modelling with functions", 2, "A box is made from a $14\\times22$ sheet by cutting squares of side $x$ at the corners and folding up the sides. What is its volume $V(x)$ and domain?",
          "$V(x)=x(14-2x)(22-2x)=%s$, domain $0<x<7$" % tex(Vx),
          ["$V(x)=x(14-x)(22-x)$, domain $0<x<14$", "$V(x)=x(14-2x)(22-2x)$, domain $0<x<11$", "$V(x)=(14-2x)(22-2x)$, domain $0<x<7$"],
          "Base $(14-2x)\\times(22-2x)$ and height $x$. All three dimensions must be positive: $x>0$ and $x<7$ (the smaller side limits $x$).", "Tutorial 1, Q5", "src")
    rr = 4 - x / (2 * sp.pi); hh = sp.sqrt(16 - rr ** 2); Vc = sp.pi * rr ** 2 * hh / 3
    x0 = 4 * sp.pi
    assert sp.simplify(rr.subs(x, x0) - 2) == 0
    V0 = sp.simplify(Vc.subs(x, x0)); assert sp.simplify(V0 - 8 * sp.sqrt(3) * sp.pi / 3) == 0
    B.mcq(ch, "Modelling with functions", 3, "A sector with arc length $x$ is cut from a circular paper of radius $4$ and the rest is rolled into a cone. The base radius is $r(x)=$",
          "$\\dfrac{8\\pi-x}{2\\pi}$", ["$\\dfrac{x}{2\\pi}$", "$\\dfrac{8\\pi+x}{2\\pi}$", "$8\\pi-x$"],
          "The base circumference equals the remaining arc: $2\\pi r=8\\pi-x$, so $r=\\frac{8\\pi-x}{2\\pi}=4-\\frac{x}{2\\pi}$. Slant height $4$ gives $h=\\sqrt{16-r^2}$.", "Tutorial 1, Q6", "src")
    mc_val(B, ch, "Modelling with functions", 3, "For the cone of the previous problem with $x=4\\pi$, the volume $V=\\frac13\\pi r^2h$ is", V0, [sp.pi * 4 * 2 * sp.sqrt(3), 16 * sp.pi / 3, 8 * sp.pi * sp.sqrt(2) / 3],
           "$r=4-\\frac{4\\pi}{2\\pi}=2$, $h=\\sqrt{16-4}=2\\sqrt3$, $V=\\frac13\\pi\\cdot4\\cdot2\\sqrt3=\\frac{8\\sqrt3\\pi}{3}$.", "Tutorial 1, Q6", "src")

    # ---- epsilon-delta (Tutorial 2 Q1, Q5-Q7; Computation #2 Q1-Q2)
    B.mcq(ch, "Epsilon–delta", 1, "The statement $\\lim_{x\\to a}f(x)=L$ means:", "for every $\\varepsilon>0$ there is $\\delta>0$ such that $0<|x-a|<\\delta\\Rightarrow|f(x)-L|<\\varepsilon$",
          ["for every $\\delta>0$ there is $\\varepsilon>0$ such that $0<|x-a|<\\delta\\Rightarrow|f(x)-L|<\\varepsilon$", "$f(a)=L$", "for every $\\varepsilon>0$ there is $\\delta>0$ with $|x-a|<\\varepsilon\\Rightarrow|f(x)-L|<\\delta$"],
          "The order of the quantifiers matters: the target tolerance $\\varepsilon$ is given first, then $\\delta$ is chosen in response. The value $f(a)$ plays no role.", "Lecture 1", "concept")
    B.mcq(ch, "Epsilon–delta", 2, "To prove $\\lim_{x\\to4}(9-x)=5$ by the definition, given $\\varepsilon>0$ the largest suitable $\\delta$ is", "$\\delta=\\varepsilon$", ["$\\delta=\\varepsilon/2$", "$\\delta=\\min(1,\\varepsilon)$ is the only choice", "$\\delta=5\\varepsilon$"],
          "$|(9-x)-5|=|4-x|=|x-4|<\\varepsilon$ exactly when $|x-4|<\\varepsilon$, so $\\delta=\\varepsilon$ works (and any smaller $\\delta$ too).", "Computation problems 2, Q1", "src")
    B.mcq(ch, "Epsilon–delta", 2, "To prove $\\lim_{x\\to-3}\\dfrac{x^2-9}{x+3}=-6$ by the definition, for $x\\ne-3$ we have $\\left|\\dfrac{x^2-9}{x+3}-(-6)\\right|=$", "$|x+3|$, so $\\delta=\\varepsilon$ works",
          ["$|x-3|$, so $\\delta=\\varepsilon$ works", "$|x+3|^2$, so $\\delta=\\sqrt\\varepsilon$ is needed", "$6|x+3|$, so $\\delta=\\varepsilon/6$ works"],
          "For $x\\ne-3$: $\\frac{x^2-9}{x+3}=x-3$, so $|(x-3)+6|=|x+3|<\\varepsilon$ when $|x-(-3)|<\\varepsilon$.", "Computation problems 2, Q2", "src")
    for _ in range(4):
        m_ = rng.choice([2, 3, 4, 5, -2, -3]); a_ = rng.randint(-3, 4); c_ = rng.randint(-5, 5)
        eps = rng.choice([sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 2), 1])
        dlt = eps / abs(m_)
        xa = "x%+d" % (-a_) if a_ != 0 else "x"
        mc_val(B, ch, "Epsilon–delta", 2, "To prove $\\lim_{x\\to %d}(%dx%+d)=%d$ with the tolerance $\\varepsilon=%s$, the largest valid $\\delta$ is" % (a_, m_, c_, m_ * a_ + c_, tex(eps)),
               dlt, [eps, eps * abs(m_), eps / (abs(m_) + 1), 2 * dlt], "$|f(x)-L|=|%d|\\cdot|%s|<\\varepsilon\\iff|%s|<\\varepsilon/%d$, so $\\delta=\\varepsilon/|m|=%s$." % (m_, xa, xa, abs(m_), tex(dlt)), "Generated (Lecture 1: ε–δ)", "gen")
    B.mcq(ch, "Epsilon–delta", 2, "A bar is $y=10+(t-70)\\cdot10^{-4}$ cm wide at temperature $t$ °F. To keep the width within $0.0005$ cm of $10$ cm, the temperature must stay within … of $70$ °F", "$5$ °F",
          ["$0.5$ °F", "$50$ °F", "$0.0005$ °F"], "$|y-10|=10^{-4}|t-70|<0.0005\\iff|t-70|<5$.", "Tutorial 2, Q5", "src")
    d1 = min(sp.Rational(4) - sp.Rational(64, 25), sp.Rational(144, 25) - 4)
    assert d1 == sp.Rational(36, 25)
    B.mcq(ch, "Epsilon–delta", 3, "The exit rate is $y=\\sqrt{x}/2$ ft³/min for water depth $x$ ft. To keep $y$ within $0.2$ of $y_0=1$, the depth must stay within … ft of $x_0=4$",
          "$1.44$", ["$0.4$", "$1.76$", "$0.8$"], "$0.8<\\sqrt x/2<1.2\\iff2.56<x<5.76$. The nearer endpoint to $4$ is $2.56$, at distance $1.44$ (the other is $1.76$ away), so $\\delta=1.44$.", "Tutorial 2, Q6(a)", "src")
    B.mcq(ch, "Epsilon–delta", 3, "With the same exit rate $y=\\sqrt x/2$, to keep $y$ within $0.1$ of $1$ the depth must stay within … ft of $4$", "$0.76$",
          ["$1.44$", "$0.84$", "$0.2$"], "$0.9<\\sqrt x/2<1.1\\iff3.24<x<4.84$. Distances from $4$: $0.76$ and $0.84$; take the smaller, $\\delta=0.76$.", "Tutorial 2, Q6(b)", "src")
    dh = sp.Rational(10) / (36 * sp.pi)
    B.mcq(ch, "Epsilon–delta", 3, "A measuring cup has $V=36\\pi h$ (cm³, $h$ in cm). To measure $1000$ cm³ with error at most $10$ cm³, $h$ must be accurate to within about", "$%.4f$ cm" % float(dh),
          ["$%.4f$ cm" % float(sp.Rational(10) / 36), "$%.4f$ cm" % float(dh * 10), "$%.4f$ cm" % float(sp.Rational(1000) / (36 * sp.pi))],
          "$|\\Delta V|=36\\pi|\\Delta h|<10\\Rightarrow|\\Delta h|<\\frac{10}{36\\pi}\\approx0.0884$ cm.", "Tutorial 2, Q7", "src")

    # ---- limits (all verified against sympy)
    lim_f = limq
    lim_f(B, ch, 1, "\\dfrac{x^2-4}{x-2}", (x ** 2 - 4) / (x - 2), x, 2, None, 4, "Factor $x^2-4=(x-2)(x+2)$ and cancel the zero factor.", "Generated (Lecture 1–2: 0/0 limits)", "gen", extras=[0, 2, 1])
    lim_f(B, ch, 1, "\\dfrac{x^2-9}{x^2-5x+6}", (x ** 2 - 9) / (x ** 2 - 5 * x + 6), x, 3, None, 6, "Factor: $\\frac{(x-3)(x+3)}{(x-2)(x-3)}=\\frac{x+3}{x-2}\\to\\frac{6}{1}$.", "Generated (Lecture 2)", "gen", extras=[0, 3, 2])
    lim_f(B, ch, 1, "\\dfrac{3x^2-x+2}{2x^2+5}", (3 * x ** 2 - x + 2) / (2 * x ** 2 + 5), x, oo, None, sp.Rational(3, 2), "Divide numerator and denominator by $x^2$; the lower-order terms vanish.", "Generated (Lecture 2: limits at infinity)", "gen", extras=[3, 2, sp.Rational(2, 3)])
    lim_f(B, ch, 1, "\\dfrac{5x+1}{x^2+3}", (5 * x + 1) / (x ** 2 + 3), x, oo, None, 0, "The denominator has the higher degree, so the quotient tends to $0$.", "Generated (Lecture 2)", "gen", extras=[5])
    lim_f(B, ch, 2, "\\dfrac{2x^3+1}{x^3-x}", (2 * x ** 3 + 1) / (x ** 3 - x), x, -oo, None, 2, "Equal degrees: the limit is the ratio of leading coefficients, $\\frac21$, also as $x\\to-\\infty$.", "Generated (Lecture 2)", "gen", extras=[-2, 1, 0])
    lim_f(B, ch, 2, "\\left(\\sqrt{x^2+x}-x\\right)", sp.sqrt(x ** 2 + x) - x, x, oo, None, sp.Rational(1, 2), "Multiply by the conjugate: $\\frac{x}{\\sqrt{x^2+x}+x}=\\frac{1}{\\sqrt{1+1/x}+1}\\to\\frac12$.", "Generated (Lecture 2)", "gen", extras=[0, 1, oo])
    lim_f(B, ch, 2, "\\dfrac{\\sqrt{x}-2}{x-4}", (sp.sqrt(x) - 2) / (x - 4), x, 4, None, sp.Rational(1, 4), "Multiply by the conjugate $\\sqrt x+2$: $\\frac{x-4}{(x-4)(\\sqrt x+2)}=\\frac1{\\sqrt x+2}\\to\\frac14$.", "Generated (Lecture 2)", "gen", extras=[0, 4, sp.Rational(1, 2)])
    lim_f(B, ch, 1, "\\dfrac{\\sin 5x}{2x}", sp.sin(5 * x) / (2 * x), x, 0, None, sp.Rational(5, 2), "Use $\\frac{\\sin u}{u}\\to1$: $\\frac{\\sin5x}{2x}=\\frac52\\cdot\\frac{\\sin5x}{5x}\\to\\frac52$.", "Generated (Lecture 1–2: special limit)", "gen", extras=[sp.Rational(2, 5), 5, 10])
    lim_f(B, ch, 2, "\\dfrac{1-\\cos x}{x^2}", (1 - sp.cos(x)) / x ** 2, x, 0, None, sp.Rational(1, 2), "$1-\\cos x=2\\sin^2\\frac x2$, so the quotient is $\\frac12\\left(\\frac{\\sin(x/2)}{x/2}\\right)^2\\to\\frac12$.", "Generated (Lecture 2)", "gen", extras=[0, 1, 2])
    lim_f(B, ch, 1, "\\dfrac{\\tan 3x}{x}", sp.tan(3 * x) / x, x, 0, None, 3, "$\\frac{\\tan3x}{x}=3\\cdot\\frac{\\sin3x}{3x}\\cdot\\frac1{\\cos3x}\\to3$.", "Generated (Lecture 2)", "gen", extras=[1, sp.Rational(1, 3), 0])
    lim_f(B, ch, 2, "\\dfrac{\\sin^2 3x}{x^2}", sp.sin(3 * x) ** 2 / x ** 2, x, 0, None, 9, "$\\left(\\frac{\\sin3x}{x}\\right)^2=\\left(3\\cdot\\frac{\\sin3x}{3x}\\right)^2\\to9$. (This is why $c=9$ makes the function in Tutorial 4, Q5 continuous.)", "Tutorial 4, Q5", "src", extras=[3, 1, 0])
    lim_f(B, ch, 2, "x^{2}\\sin\\dfrac1x", x ** 2 * sp.sin(1 / x), x, 0, None, 0, "Squeeze theorem: $-x^2\\le x^2\\sin\\frac1x\\le x^2$ and both bounds tend to $0$.", "Tutorial 2, Q2", "src", extras=[1, oo])
    lim_f(B, ch, 1, "\\dfrac{1}{x-1}", 1 / (x - 1), x, 1, "+", oo, "The denominator tends to $0$ through positive values, so the quotient grows without bound.", "Generated (Lecture 2: infinite limits)", "gen", extras=[0, 1])
    lim_f(B, ch, 1, "\\dfrac{1}{x-1}", 1 / (x - 1), x, 1, "-", -oo, "The denominator tends to $0$ through negative values: the quotient tends to $-\\infty$.", "Generated (Lecture 2)", "gen", extras=[0, 1])
    lim_f(B, ch, 2, "\\dfrac{x-3}{x-2}", (x - 3) / (x - 2), x, 2, "+", -oo, "Numerator $\\to-1$, denominator $\\to0^+$: the quotient tends to $-\\infty$.", "Generated (Lecture 2)", "gen", extras=[0, 1])
    lim_f(B, ch, 2, "\\dfrac{x}{\\sqrt{x^2+1}}", x / sp.sqrt(x ** 2 + 1), x, -oo, None, -1, "For $x<0$, $\\sqrt{x^2}=|x|=-x$, so the quotient is $\\frac{x}{|x|\\sqrt{1+1/x^2}}\\to-1$. (Watch the sign!)", "Generated (Lecture 2: sign trap)", "gen", extras=[1, 0, oo])
    lim_f(B, ch, 2, "\\dfrac{x}{\\sqrt{x^2+1}}", x / sp.sqrt(x ** 2 + 1), x, oo, None, 1, "For $x>0$, $\\sqrt{x^2}=x$: the quotient $\\to1$.", "Generated (Lecture 2)", "gen", extras=[-1, 0, oo])
    # Computation #2 Q3 (answers (a) -inf (b) +inf (c) 0 (d) 3/2)
    g3 = x ** 2 / 2 - 1 / x
    for pt, dr, exp_, lbl in [(0, "+", -oo, "x\\to0^{+}"), (0, "-", oo, "x\\to0^{-}"), (cbrt(2), None, 0, "x\\to\\sqrt[3]{2}"), (-1, None, sp.Rational(3, 2), "x\\to-1")]:
        lim_f(B, ch, 2, "\\left(\\dfrac{x^2}{2}-\\dfrac1x\\right)", g3, x, pt, dr, exp_, "Substitute directly when the function is continuous at the point; at $0$ the term $-\\frac1x$ decides the sign of the blow-up." if pt != 0 else "As $x\\to0^{\\pm}$ the term $-\\frac1x$ dominates: it is $-\\infty$ from the right and $+\\infty$ from the left.", "Computation problems 2, Q3", "src", extras=[0, 1])
    # Computation #2 Q4 : 2 - 3/t^(1/3)
    s_ = sp.Symbol("s", positive=True)
    right = sp.limit(2 - 3 / s_ ** sp.Rational(1, 3), s_, 0, "+")           # t = s -> 0+
    left = sp.limit(2 + 3 / s_ ** sp.Rational(1, 3), s_, 0, "+")            # t = -s -> 0-
    assert right == -oo and left == oo
    B.mcq(ch, "Limits", 2, "Evaluate $\\displaystyle\\lim_{t\\to0^{+}}\\left(2-\\dfrac{3}{t^{1/3}}\\right)$.", "$-\\infty$", ["$+\\infty$", "$2$", "$0$"], "As $t\\to0^+$, $t^{1/3}\\to0^+$ so $\\frac{3}{t^{1/3}}\\to+\\infty$ and the expression tends to $-\\infty$.", "Computation problems 2, Q4(a)", "src")
    B.mcq(ch, "Limits", 2, "Evaluate $\\displaystyle\\lim_{t\\to0^{-}}\\left(2-\\dfrac{3}{t^{1/3}}\\right)$.", "$+\\infty$", ["$-\\infty$", "$2$", "the limit is $0$"], "For $t<0$, $t^{1/3}\\to0^-$ so $\\frac{3}{t^{1/3}}\\to-\\infty$ and $2-(-\\infty)=+\\infty$.", "Computation problems 2, Q4(b)", "src")
    # Mock test Q1(b)
    val = sp.limit(sp.sqrt(x + sp.sqrt(x + sp.sqrt(x))) / (sp.sqrt(x) + 1), x, oo); assert val == 1
    B.mcq(ch, "Limits", 3, "Evaluate $\\displaystyle\\lim_{x\\to\\infty}\\dfrac{\\sqrt{x+\\sqrt{x+\\sqrt{x}}}}{\\sqrt{x}+1}$.", "$1$", ["$0$", "$+\\infty$", "$\\tfrac12$"],
          "Divide by $\\sqrt x$: numerator $\\sqrt{1+\\sqrt{1/x+1/x^{3/2}}}\\to1$, denominator $1+1/\\sqrt x\\to1$.", "Mock Test 1, Q1(b)(i)", "src")
    B.mcq(ch, "Limits", 3, "Evaluate $\\displaystyle\\lim_{x\\to\\infty}\\dfrac{e^{\\sin x}}{x+1}$.", "$0$", ["$1$", "$e$", "the limit does not exist because $\\sin x$ oscillates"],
          "Squeeze: $\\frac{1}{e}\\le e^{\\sin x}\\le e$, so $0<\\frac{e^{\\sin x}}{x+1}\\le\\frac{e}{x+1}\\to0$.", "Mock Test 1, Q1(b)(ii)", "src")
    B.mcq(ch, "Limits", 2, "Let $f(x)=x^2$ for $x\\ne1$ and $f(1)=2$. Then $\\lim_{x\\to1}f(x)$ equals", "$1$", ["$2$", "$0$", "it does not exist"], "A limit ignores the value at the point: $\\lim_{x\\to1}x^2=1$ even though $f(1)=2$ (so $f$ is not continuous at $1$).", "Tutorial 2, Q1", "src")
    B.mcq(ch, "Limits", 2, "For $f(x)=x$ if $x<1$ and $f(x)=x+1$ if $x>1$, the limit $\\lim_{x\\to1}f(x)$", "does not exist (left limit $1$, right limit $2$)",
          ["equals $1$", "equals $2$", "equals $\\tfrac32$"], "A two-sided limit exists iff both one-sided limits exist and are equal. Here $1\\ne2$.", "Tutorial 2, Q3", "src")
    B.mcq(ch, "Limits", 1, "$\\displaystyle\\lim_{x\\to0}\\dfrac{|x|}{x}$", "does not exist (one-sided limits $-1$ and $1$)", ["equals $1$", "equals $-1$", "equals $0$"], "For $x>0$ the quotient is $1$; for $x<0$ it is $-1$.", "Generated (Lecture 2: one-sided limits)", "gen")
    B.mcq(ch, "Limits", 1, "The Squeeze Theorem: if $g(x)\\le f(x)\\le h(x)$ near $a$ and $\\lim g=\\lim h=L$, then", "$\\lim_{x\\to a}f(x)=L$", ["$f(a)=L$", "$f$ is continuous everywhere", "$\\lim f$ may not exist"], "$f$ is squeezed between two functions with the same limit.", "Lecture 2", "concept")

    # ---- continuity (Tutorial 2 Q8-9, Tutorial 3, Computation #2-#4)
    a_ = sp.Symbol("a")
    sol_a = sp.solve(sp.Eq(3 ** 2 - 1, 2 * a_ * 3), a_)[0]; assert sol_a == sp.Rational(4, 3)
    mc_val(B, ch, "Continuity", 2, "For which $a$ is $f(x)=x^2-1$ ($x<3$), $f(x)=2ax$ ($x\\ge3$) continuous at every $x$?", sol_a, [sp.Rational(3, 4), 8, sp.Rational(3, 2), 4], "Continuity at $3$: $\\lim_{x\\to3^-}(x^2-1)=8$ must equal $f(3)=6a$, so $a=\\frac43$.", "Tutorial 2, Q8", "src")
    bsym = sp.Symbol("b")
    bsol = sp.solve(sp.Eq(0 + bsym, 1), bsym)[0]; assert bsol == 1
    B.mcq(ch, "Continuity", 3, "Let $g(x)=x+b$ for $x<0$ and $g(x)=\\cos x$ for $x\\ge0$. Which statement is true?", "$g$ is continuous at $0$ iff $b=1$, but $g$ is not differentiable at $0$ for any $b$",
          ["$g$ is continuous and differentiable at $0$ for $b=1$", "$g$ is continuous at $0$ for every $b$", "$g$ is differentiable at $0$ for $b=0$ only"],
          "Continuity: $\\lim_{x\\to0^-}(x+b)=b$ must equal $\\cos0=1$, so $b=1$. One-sided derivatives: left $=1$, right $=-\\sin0=0$. They differ, so $g'(0)$ never exists.", "Computation problems 4, Q2", "src")
    mc_val(B, ch, "Continuity", 2, "For which $c$ is $f(x)=\\dfrac{\\sin^2 3x}{x^2}$ ($x\\ne0$), $f(0)=c$, continuous at $0$?", 9, [3, 1, 0, 6], "Need $c=\\lim_{x\\to0}\\frac{\\sin^23x}{x^2}=9$.", "Tutorial 4, Q5", "src")
    CL = [("\\dfrac{x^2-1}{x-1}", "x=1", "removable discontinuity", "the limit $\\lim_{x\\to1}(x+1)=2$ exists but $f(1)$ is undefined"),
          ("\\dfrac{|x|}{x}", "x=0", "jump discontinuity", "the one-sided limits $-1$ and $1$ exist but differ"),
          ("\\dfrac{1}{x^{2}}", "x=0", "infinite discontinuity", "$f(x)\\to+\\infty$ on both sides"),
          ("\\lfloor x\\rfloor", "x=2", "jump discontinuity", "the left limit is $1$ and the right limit is $2$")]
    names = ["removable discontinuity", "jump discontinuity", "infinite discontinuity", "continuous at that point"]
    for fx, pt, ans, why in CL:
        B.mcq(ch, "Continuity", 2, "What type of discontinuity does $f(x)=%s$ have at $%s$?" % (fx, pt), ans, [z for z in names if z != ans], "At $%s$: %s." % (pt, why), "Lecture 3 / Tutorial 3, Q3–Q4", "src" if "lfloor" in fx else "gen")
    B.mcq(ch, "Continuity", 2, "The floor function $\\lfloor x\\rfloor$ is", "continuous from the right but not from the left at every integer; discontinuous exactly at the integers",
          ["continuous everywhere", "continuous from the left but not from the right at integers", "discontinuous everywhere"],
          "For integer $n$: $\\lim_{x\\to n^+}\\lfloor x\\rfloor=n=\\lfloor n\\rfloor$ but $\\lim_{x\\to n^-}\\lfloor x\\rfloor=n-1$.", "Tutorial 3, Q3", "src")
    B.mcq(ch, "Continuity", 2, "If $h=fg$ is continuous at $0$, must $f$ and $g$ both be continuous at $0$?", "No: e.g. $f=\\operatorname{sgn}x$ is discontinuous at $0$, $g(x)=x$, yet $fg=|x|$ is continuous",
          ["Yes: a product is continuous only if both factors are", "Yes, by the Product Law for limits", "Only if $f(0)\\ne0$"], "The product law goes one way only: continuous factors ⇒ continuous product.", "Tutorial 2, Q9", "src")
    # IVT
    f_iv = x ** 3 - 15 * x + 1
    roots = sp.Poly(f_iv, x).nroots(); assert len(roots) == 3 and all(abs(sp.im(r)) < 1e-12 for r in roots)
    pool = [(a1, b1) for a1 in range(-5, 5) for b1 in range(a1 + 1, min(a1 + 4, 6))]
    yes = [(a1, b1) for a1, b1 in pool if f_iv.subs(x, a1) * f_iv.subs(x, b1) < 0]
    no = [(a1, b1) for a1, b1 in pool if f_iv.subs(x, a1) * f_iv.subs(x, b1) > 0]
    assert yes and no
    for _ in range(3):
        c1 = rng.choice(yes); w = rng.sample(no, 3)
        iv = lambda p_: "$[%d,%d]$" % p_
        B.mcq(ch, "Intermediate Value Theorem", 2, "For $f(x)=x^3-15x+1$, on which interval do the hypotheses of the IVT guarantee a root (a sign change of the continuous function $f$)?", iv(c1), [iv(z) for z in w],
              "$f$ is continuous, so a root is guaranteed on $[a,b]$ when $f(a)f(b)<0$. Here $f(%d)=%s$, $f(%d)=%s$ have opposite signs; for the other intervals the endpoint values have the same sign." % (c1[0], tex(f_iv.subs(x, c1[0])), c1[1], tex(f_iv.subs(x, c1[1]))), "Tutorial 3, Q5", "src")
    B.mcq(ch, "Intermediate Value Theorem", 2, "How many real roots does $x^3-15x+1=0$ have?", "$3$", ["$1$", "$2$", "$0$"],
          "$f(-4)=-3<0$, $f(-1)=15>0$, $f(1)=-13<0$, $f(4)=5>0$: three sign changes in $[-4,4]$ give three roots by the IVT, and a cubic has at most three.", "Tutorial 3, Q5", "src")
    fa_ = (1 - x) ** 3 - sp.sin(x)
    B.mcq(ch, "Intermediate Value Theorem", 2, "To show that $(1-x)^3=\\sin x$ has a root in $(0,1)$, set $F(x)=(1-x)^3-\\sin x$. Then", "$F(0)=1>0$ and $F(1)=-\\sin1<0$, so the IVT gives a root",
          ["$F(0)=0$, so $x=0$ is the root", "$F(0)=-1<0$ and $F(1)=\\sin1>0$, so the IVT gives a root", "$F$ is not continuous on $[0,1]$"],
          "$F$ is continuous on $[0,1]$ with $F(0)=1$ and $F(1)=-\\sin1\\approx-0.84$: opposite signs.", "Computation problems 3, Q3", "src")
    B.mcq(ch, "Intermediate Value Theorem", 2, "To show that $y=e^x$ and $y=-x$ intersect, apply the IVT to $F(x)=e^x+x$. Which values prove it?", "$F(-1)=e^{-1}-1<0$ and $F(0)=1>0$",
          ["$F(0)=1$ and $F(1)=e+1$", "$F(-1)=e^{-1}+1>0$ and $F(0)>0$", "$F(-1)=-e$ and $F(0)=-1$"], "A sign change on $[-1,0]$ gives a root of $e^x=-x$.", "Computation problems 3, Q4", "src")
    B.mcq(ch, "Intermediate Value Theorem", 1, "The IVT requires that $f$ be …", "continuous on $[a,b]$", ["differentiable on $(a,b)$ only", "increasing on $[a,b]$", "bounded on $[a,b]$ only"],
          "Continuity on the closed interval is the hypothesis; if $N$ lies between $f(a)$ and $f(b)$ then $f(c)=N$ for some $c\\in(a,b)$.", "Lecture 3", "concept")


# ============================================================================== CHAPTER 2: derivatives
def d_wrongs(f, var=x):
    """Typical wrong derivatives of f (missing chain factor, sign, product-rule slip, ...)."""
    D = sp.diff(f, var)
    W = [-D]
    if f.is_Pow and f.exp.is_number and f.base.has(var) and f.exp != -1:
        W.append(f.exp * f.base ** (f.exp - 1))                      # forgot the inner derivative
        W.append(f.exp * f.base ** f.exp * sp.diff(f.base, var))      # forgot to lower the exponent
    if f.func in (sp.sin, sp.cos, sp.tan, sp.exp, sp.log) and f.args[0] != var:
        a0 = f.args[0]
        naive = {sp.sin: sp.cos(a0), sp.cos: -sp.sin(a0), sp.tan: 1 / sp.cos(a0) ** 2, sp.exp: sp.exp(a0), sp.log: 1 / a0}[f.func]
        W.append(naive)
        W.append(sp.diff(a0, var) * (-naive if f.func is not sp.exp else naive * a0))
    if f.is_Mul:
        facs = [q for q in f.args if q.has(var)]
        num, den = sp.fraction(sp.together(f))
        if den.has(var):
            W.append((sp.diff(num, var) * den + num * sp.diff(den, var)) / den ** 2)   # sign slip in the quotient rule
            W.append(sp.diff(num, var) / sp.diff(den, var))
        elif len(facs) == 2:
            u_, v_ = facs
            c_ = f / (u_ * v_)
            W.append(c_ * sp.diff(u_, var) * sp.diff(v_, var))                  # product rule: u'v'
    if f.is_Add:
        dts = [sp.diff(t_, var) for t_ in f.args]
        for i in range(len(dts)):
            W.append(sum(dts) - 2 * dts[i])        # one term gets the wrong sign
            W.append(sum(dts) - dts[i])            # one term is dropped
    W.append(D + 1)
    return W

def dq(B, ch, level, lbl, f, src, origin="src", var=x, expect=None, how="", name="f", wrap=E):
    """Question: derivative of f. If `expect` is given (answer key of the course), assert agreement."""
    D = sp.simplify(sp.diff(f, var))
    if expect is not None:
        assert num_equal(D, expect, var), (src, D, expect)
    mc_expr(B, ch, "Differentiation rules", level, "Find $%s'$ for $%s=%s$." % (name, name, lbl) if name != "r" else "Find $\\dfrac{dr}{d\\theta}$ for $r=%s$." % lbl, D,
            [sp.simplify(w) for w in d_wrongs(f, var)], ("%s " % how if how else "") + "$%s'=%s$." % (name, tex(D)) if name != "r" else ("%s " % how if how else "") + "$\\dfrac{dr}{d\\theta}=%s$." % tex(D), src, origin, var)
    return D

def ch2(B):
    ch = "c2"; rng = B.rng
    s_, tt, z_ = sp.symbols("s t z", positive=True)
    # ---- Computation #3 Q7 with answer keys
    dq(B, ch, 3, "\\dfrac{\\sqrt s-1}{\\sqrt s+1}", (sp.sqrt(s_) - 1) / (sp.sqrt(s_) + 1), "Computation problems 3, Q7(1)", var=s_, name="f",
       expect=1 / (sp.sqrt(s_) * (sp.sqrt(s_) + 1) ** 2), how="Quotient rule: $\\frac{(\\sqrt s+1)\\frac1{2\\sqrt s}-(\\sqrt s-1)\\frac1{2\\sqrt s}}{(\\sqrt s+1)^2}$.")
    dq(B, ch, 3, "\\dfrac{1}{(x^2-1)(x^2+x+1)}", 1 / ((x ** 2 - 1) * (x ** 2 + x + 1)), "Computation problems 3, Q7(2)", name="y",
       expect=-(4 * x ** 3 + 3 * x ** 2 - 1) / ((x ** 2 - 1) ** 2 * (x ** 2 + x + 1) ** 2), how="Write $y=P^{-1}$ with $P=(x^2-1)(x^2+x+1)=x^4+x^3-x-1$; then $y'=-P'/P^2$.")
    dq(B, ch, 2, "(t^2+1)\\left(t+5+\\dfrac1t\\right)", (tt ** 2 + 1) * (tt + 5 + 1 / tt), "Computation problems 3, Q7(3)", var=tt, name="g",
       expect=3 * tt ** 2 + 10 * tt + 2 - 1 / tt ** 2, how="Expand first: $g=t^3+5t^2+2t+5+t^{-1}$.")
    # ---- Computation #3 Q8: second derivatives
    r_ = 1 / (3 * s_ ** 2) - 5 / (2 * s_)
    r1, r2 = sp.simplify(sp.diff(r_, s_)), sp.simplify(sp.diff(r_, s_, 2))
    assert num_equal(r1, -2 / (3 * s_ ** 3) + 5 / (2 * s_ ** 2), s_) and num_equal(r2, 2 / s_ ** 4 - 5 / s_ ** 3, s_)
    mc_expr(B, ch, "Higher derivatives", 2, "Find $\\dfrac{d^2r}{ds^2}$ for $r=\\dfrac{1}{3s^2}-\\dfrac{5}{2s}$.", r2,
            [-2 / (3 * s_ ** 3) + 5 / (2 * s_ ** 2), 2 / s_ ** 4 + 5 / s_ ** 3, -2 / s_ ** 4 + 5 / s_ ** 3, 6 / s_ ** 4 - 10 / s_ ** 3],
            "$r=\\frac13s^{-2}-\\frac52s^{-1}$, $r'=-\\frac23s^{-3}+\\frac52s^{-2}$, $r''=2s^{-4}-5s^{-3}$.", "Computation problems 3, Q8(1)", "src", s_)
    w_ = (1 + 3 * z_) / (3 * z_) * (3 - z_)
    w1 = sp.simplify(sp.diff(w_, z_)); w2 = sp.simplify(sp.diff(w_, z_, 2))
    mc_expr(B, ch, "Higher derivatives", 2, "Find $\\dfrac{dw}{dz}$ for $w=\\left(\\dfrac{1+3z}{3z}\\right)(3-z)$.", w1,
            [sp.simplify(-w1), sp.diff((1 + 3 * z_) / (3 * z_), z_) * sp.diff(3 - z_, z_), w1 + 1, sp.simplify(sp.diff((1 + 3 * z_) / (3 * z_), z_) * (3 - z_) - (1 + 3 * z_) / (3 * z_))],
            "Simplify first: $w=\\frac{(1+3z)(3-z)}{3z}=\\frac{3+8z-3z^2}{3z}=\\frac1z+\\frac83-z$, so $w'=%s$." % tex(w1), "Computation problems 3, Q8(2)", "src", z_)
    mc_expr(B, ch, "Higher derivatives", 2, "Find $\\dfrac{d^2w}{dz^2}$ for $w=\\left(\\dfrac{1+3z}{3z}\\right)(3-z)$.", w2,
            [-w2, sp.simplify(sp.diff(w_, z_)), 1 / z_ ** 3, -1 / z_ ** 3], "$w=\\frac1z+\\frac83-z$, $w'=-\\frac1{z^2}-1$, $w''=\\frac{2}{z^3}$.", "Computation problems 3, Q8(2)", "src", z_)
    # ---- Computation #4 Q1, Q3, Q4, Q5
    dq(B, ch, 2, "4-\\theta^{2}\\sin\\theta", 4 - th ** 2 * sp.sin(th), "Computation problems 4, Q1(a)", var=th, name="r", how="Product rule on $\\theta^2\\sin\\theta$.")
    dq(B, ch, 3, "\\sec\\theta\\csc\\theta", sp.sec(th) * sp.csc(th), "Computation problems 4, Q1(b)", var=th, name="r", how="Product rule with $(\\sec\\theta)'=\\sec\\theta\\tan\\theta$ and $(\\csc\\theta)'=-\\csc\\theta\\cot\\theta$.")
    dq(B, ch, 2, "\\dfrac{\\sin\\theta+\\cos\\theta}{\\cos\\theta}", (sp.sin(th) + sp.cos(th)) / sp.cos(th), "Computation problems 4, Q1(c)", var=th, name="r", expect=1 / sp.cos(th) ** 2, how="Simplify first: $r=\\tan\\theta+1$.")
    dq(B, ch, 1, "\\sqrt{3-t}", sp.sqrt(3 - t), "Computation problems 4, Q3(a)", var=t, name="p", expect=-1 / (2 * sp.sqrt(3 - t)), how="Chain rule: $\\frac{1}{2\\sqrt{3-t}}\\cdot(-1)$.")
    dq(B, ch, 3, "x^{2}\\sin^{4}x+x\\cos^{-2}x", x ** 2 * sp.sin(x) ** 4 + x * sp.cos(x) ** -2, "Computation problems 4, Q3(b)", name="y", how="Product and chain rules on each term.")
    dq(B, ch, 3, "\\left(\\dfrac{\\sin\\theta}{1+\\cos\\theta}\\right)^{2}", (sp.sin(th) / (1 + sp.cos(th))) ** 2, "Computation problems 4, Q3(c)", var=th, name="f", how="Chain rule outside, quotient rule inside (note $\\frac{\\sin\\theta}{1+\\cos\\theta}=\\tan\\frac\\theta2$).")
    dq(B, ch, 3, "\\sin\\!\\left(\\dfrac{t}{\\sqrt{t+1}}\\right)", sp.sin(t / sp.sqrt(t + 1)), "Computation problems 4, Q3(d)", var=t, name="q", how="Chain rule: $\\cos(\\cdot)\\cdot\\frac{d}{dt}\\frac{t}{\\sqrt{t+1}}$ with $\\frac{d}{dt}\\frac{t}{\\sqrt{t+1}}=\\frac{t+2}{2(t+1)^{3/2}}$.")
    dq(B, ch, 3, "\\left(1+\\tan^{4}\\tfrac{t}{12}\\right)^{3}", (1 + sp.tan(t / 12) ** 4) ** 3, "Computation problems 4, Q4", var=t, name="y", how="Three nested layers: cube, fourth power of $\\tan$, argument $t/12$.")
    y2 = sp.simplify(sp.diff((1 + 1 / x) ** 3, x, 2))
    mc_expr(B, ch, "Higher derivatives", 3, "Find $y''$ for $y=\\left(1+\\dfrac1x\\right)^3$.", y2, [sp.simplify(sp.diff((1 + 1 / x) ** 3, x)), -y2, sp.simplify(6 * (1 + 1 / x) / x ** 4), sp.simplify(6 * (1 + 1 / x) ** 2 / x ** 3)],
            "$y'=3(1+x^{-1})^2(-x^{-2})$, then differentiate again with the product rule: $y''=%s$." % tex(y2), "Computation problems 4, Q5", "src")
    # ---- derivative definition, tangent lines (generated)
    for f_, a_, name in [(x ** 2, 3, "x^2"), (sp.sqrt(x), 4, "\\sqrt{x}"), (1 / x, 2, "\\dfrac1x"), (x ** 3 - 2 * x, 1, "x^3-2x")]:
        val = sp.limit((f_.subs(x, a_ + sp.Symbol("h")) - f_.subs(x, a_)) / sp.Symbol("h"), sp.Symbol("h"), 0); assert val == sp.diff(f_, x).subs(x, a_)
        mc_val(B, ch, "Definition of the derivative", 1, "Use $f'(a)=\\lim_{h\\to0}\\frac{f(a+h)-f(a)}{h}$ to compute $f'(%d)$ for $f(x)=%s$." % (a_, name), val,
               [-val, f_.subs(x, a_), 2 * val, val + 1], "$f'(%d)=%s$ (the limit of the difference quotient equals $\\frac{d}{dx}%s$ at $%d$)." % (a_, tex(val), name, a_), "Lecture 3 (definition of the derivative)", "gen")
    for f_, a_, name in [(x ** 3, 1, "x^3"), (sp.sqrt(x), 4, "\\sqrt{x}"), (sp.exp(2 * x), 0, "e^{2x}"), (x ** 2 + 3 * x, 2, "x^2+3x")]:
        m_ = sp.diff(f_, x).subs(x, a_); y0 = f_.subs(x, a_); L = sp.expand(m_ * (x - a_) + y0)
        wr = [sp.expand(y0 * (x - a_) + m_), sp.expand(m_ * (x - a_) - y0), sp.expand(-m_ * (x - a_) + y0), sp.expand(m_ * x + y0)]
        mc_expr(B, ch, "Tangent lines", 2, "Find the tangent line to $y=%s$ at $x=%d$." % (name, a_), L, [sp.Eq(sp.Symbol("y"), w) for w in []] or wr,
                "Slope $f'(%d)=%s$, point $(%d,%s)$: $y=%s(x-%d)+%s$, i.e. $y=%s$." % (a_, tex(m_), a_, tex(y0), tex(m_), a_, tex(y0), tex(L)), "Generated (Lecture 3: tangent line)", "gen", x, wrap=lambda e: "$y=" + tex(e) + "$")
    # ---- differentiability
    DIF = [("|x|", sp.Abs(x), "corner"), ("x^{1/3}", sp.real_root(x, 3), "vertical tangent"), ("x^{2/3}", sp.real_root(x, 3) ** 2, "cusp"), ("x^2", x ** 2, "smooth")]
    for lbl, f_, kind in DIF:
        if kind != "smooth":
            B.mcq(ch, "Differentiability", 2, "Which of the following is NOT differentiable at $x=0$?", "$%s$" % lbl,
                  ["$%s$" % l2 for l2, _, k2 in DIF if l2 != lbl][:3], "At $0$ the graph of $%s$ has a %s, so the difference quotient has no finite two-sided limit. The others are differentiable at $0$ ($x^2$ is smooth; check the remaining ones: only corners, cusps and vertical tangents fail)." % (lbl, kind) if False else
                  "$%s$ has a %s at $0$: the difference quotient $\\frac{f(h)-f(0)}{h}$ has no finite limit." % (lbl, kind), "Tutorial 3, Q10–Q12", "src") if False else None
    B.mcq(ch, "Differentiability", 2, "Which function is continuous but NOT differentiable at $x=0$?", "$f(x)=|x|$", ["$f(x)=x^2$", "$f(x)=x^3$", "$f(x)=\\dfrac{|x|}{x}$ (with $f(0)=0$)"],
          "$|x|$ is continuous, but the one-sided derivatives are $-1$ and $1$ (a corner). $\\frac{|x|}{x}$ is not even continuous at $0$.", "Tutorial 3, Q10–Q12", "src")
    B.mcq(ch, "Differentiability", 1, "If $f$ is differentiable at $a$, then", "$f$ is continuous at $a$", ["$f'$ is continuous at $a$", "$f(a)=0$", "$f''(a)$ exists"],
          "Differentiable ⇒ continuous (the converse is false, e.g. $|x|$ at $0$).", "Lecture 3", "concept")
    B.mcq(ch, "Differentiability", 2, "Which of these is NOT a way for $f$ to fail to be differentiable at $a$?", "$f$ has a horizontal tangent at $a$", ["$f$ has a corner at $a$", "$f$ has a vertical tangent at $a$", "$f$ is discontinuous at $a$"],
          "A horizontal tangent means $f'(a)=0$: perfectly differentiable.", "Lecture 3", "concept")
    B.mcq(ch, "Differentiability", 3, "If $|f(x)|\\le x^2$ on $[-1,1]$, then $f'(0)$", "exists and equals $0$", ["does not exist", "equals $1$", "may or may not exist"],
          "$|f(0)|\\le0$ so $f(0)=0$, and $\\left|\\frac{f(h)-f(0)}{h}\\right|\\le|h|\\to0$ (squeeze): $f'(0)=0$.", "Computation problems 3, Q9(a)", "src")
    B.mcq(ch, "Differentiability", 3, "For $f(x)=x^2\\sin\\frac1x$ ($x\\ne0$), $f(0)=0$, what is $f'(0)$?", "$0$", ["$1$", "it does not exist because $\\sin\\frac1x$ oscillates", "$\\infty$"],
          "$\\frac{f(h)-0}{h}=h\\sin\\frac1h$ and $|h\\sin\\frac1h|\\le|h|\\to0$: $f'(0)=0$.", "Computation problems 3, Q9(b)", "src")
    B.mcq(ch, "Differentiability", 3, "For $h(x)=x^2\\sin\\frac1x$, $h(0)=0$: is $h'$ continuous at $0$? And for $k(x)=xh(x)$?", "No for $h'$; yes for $k'$",
          ["Yes for $h'$; no for $k'$", "Yes for both", "No for both"],
          "$h'(x)=2x\\sin\\frac1x-\\cos\\frac1x$ for $x\\ne0$ has no limit at $0$ although $h'(0)=0$. For $k=x^3\\sin\\frac1x$: $k'(x)=3x^2\\sin\\frac1x-x\\cos\\frac1x\\to0=k'(0)$.", "Computation problems 4, Q13", "src")
    asym, bsym = sp.symbols("a b")
    sol = sp.solve([sp.Eq(-asym + bsym, -asym - 1 + 2 * bsym), sp.Eq(asym, 3 * asym + 1)], [asym, bsym], dict=True)[0]
    assert sol[asym] == sp.Rational(-1, 2) and sol[bsym] == 1
    B.mcq(ch, "Differentiability", 3, "For which $a,b$ is $g(x)=ax+b$ ($x\\le-1$), $g(x)=ax^3+x+2b$ ($x>-1$) differentiable for all $x$?", "$a=-\\tfrac12,\\ b=1$",
          ["$a=\\tfrac12,\\ b=1$", "$a=-\\tfrac12,\\ b=-1$", "$a=-1,\\ b=\\tfrac12$"],
          "Continuity at $-1$: $-a+b=-a-1+2b\\Rightarrow b=1$. Equal derivatives at $-1$: $a=3a(-1)^2+1\\Rightarrow-2a=1\\Rightarrow a=-\\frac12$.", "Computation problems 3, Q10", "src")
    # ---- implicit differentiation
    yv = sp.Function("y")
    def idiff_at(eq, pt, order):
        yy = sp.Symbol("yy")
        d1 = sp.idiff(eq, yy, x)
        if order == 1:
            return sp.simplify(d1.subs({x: pt[0], yy: pt[1]}))
        d2 = sp.diff(d1, x) + sp.diff(d1, yy) * d1
        return sp.simplify(d2.subs({x: pt[0], yy: pt[1]}))
    yy = sp.Symbol("yy")
    v1 = idiff_at(x ** 3 + yy ** 3 - 16, (2, 2), 2)
    assert v1 == -2, v1
    mc_val(B, ch, "Implicit differentiation", 3, "If $x^3+y^3=16$, find $\\dfrac{d^2y}{dx^2}$ at $(2,2)$.", v1, [2, -1, sp.Rational(-1, 2), -4], "$y'=-\\frac{x^2}{y^2}$; differentiating again, $y''=-\\frac{2xy^2-2x^2yy'}{y^4}$. At $(2,2)$: $y'=-1$ and $y''=-\\frac{16+16\\cdot(-1)\\cdot(-1)\\cdot(-1)\\cdot0}{16}$ → evaluate with the formula to get $%s$." % tex(v1) if False else
           "$y'=-\\frac{x^2}{y^2}$, which equals $-1$ at $(2,2)$. Then $y''=-\\frac{2xy^2-2x^2yy'}{y^4}=-\\frac{2\\cdot2\\cdot4-2\\cdot4\\cdot2\\cdot(-1)}{16}=-\\frac{16+16}{16}=%s$." % tex(v1), "Tutorial 4, Q6(a)", "src")
    v2 = idiff_at(x * yy + yy ** 2 - 1, (0, -1), 2)
    mc_val(B, ch, "Implicit differentiation", 3, "If $xy+y^2=1$, find $\\dfrac{d^2y}{dx^2}$ at $(0,-1)$.", v2, [-v2, 0, 2, sp.Rational(1, 2)],
           "Differentiate: $y+xy'+2yy'=0\\Rightarrow y'=-\\frac{y}{x+2y}$, which is $-\\frac12$ at $(0,-1)$. Differentiating again and substituting gives $y''=%s$." % tex(v2), "Tutorial 4, Q6(b)", "src")
    for eq, lbl, src in [(x ** 2 * yy + x * yy ** 2 - 6, "x^2y+xy^2=6", "Computation problems 4, Q6(a)"), (x + sp.tan(x * yy), "x+\\tan(xy)=0", "Computation problems 4, Q6(c)")]:
        d1 = sp.simplify(sp.idiff(eq, yy, x)); Y = sp.Symbol("y")
        d1y = d1.subs(yy, Y)
        wrongs = [sp.simplify(-d1y), sp.simplify(d1y + 1), sp.simplify(sp.diff(eq, x).subs(yy, Y)), sp.simplify(-sp.diff(eq, Y) / sp.diff(eq, x).subs(yy, Y)) if False else sp.simplify(sp.diff(eq.subs(yy, Y), Y) / sp.diff(eq.subs(yy, Y), x))]
        mc_expr(B, ch, "Implicit differentiation", 3, "Use implicit differentiation to find $\\dfrac{dy}{dx}$ for $%s$." % lbl, d1y, wrongs,
                "Differentiate both sides w.r.t. $x$ treating $y=y(x)$, then solve for $y'=-\\frac{F_x}{F_y}$: $\\frac{dy}{dx}=%s$." % tex(d1y), src, "src", Y)
    # ---- kinematics (Tutorial 4 Q2-Q4)
    s_t = tt ** 3 - 6 * tt ** 2 + 9 * tt; v_t = sp.diff(s_t, tt); a_t = sp.diff(s_t, tt, 2)
    assert sp.solve(v_t, tt) == [1, 3] and a_t.subs(tt, 1) == -6 and a_t.subs(tt, 3) == 6 and sp.solve(a_t, tt) == [2] and v_t.subs(tt, 2) == -3
    dist = abs(s_t.subs(tt, 1) - s_t.subs(tt, 0)) + abs(s_t.subs(tt, 2) - s_t.subs(tt, 1)); assert dist == 6
    mc_text(B, ch, "Rates of change", 2, "A body has position $s=t^3-6t^2+9t$. Its acceleration at the times when the velocity is zero is", "$-6$ at $t=1$ and $6$ at $t=3$", ["$6$ at $t=1$ and $-6$ at $t=3$", "$0$ at both times", "$-3$ at $t=1$ and $3$ at $t=3$"],
            "$v=3t^2-12t+9=3(t-1)(t-3)$ vanishes at $t=1,3$; $a=6t-12$ gives $a(1)=-6$ and $a(3)=6$.", "Tutorial 4, Q2(a)", "src")
    mc_val(B, ch, "Rates of change", 2, "For $s=t^3-6t^2+9t$, the body's speed at the moment its acceleration is zero is", 3, [-3, 0, 9, 12], "$a=6t-12=0$ at $t=2$; $v(2)=12-24+9=-3$, so the speed is $|v|=3$.", "Tutorial 4, Q2(b)", "src")
    mc_val(B, ch, "Rates of change", 3, "For $s=t^3-6t^2+9t$, the total distance travelled from $t=0$ to $t=2$ is", 6, [2, 4, 8, 10], "The body moves forward until $t=1$ ($s$ goes $0\\to4$) then back ($4\\to2$): $4+2=6$ (the displacement is only $2$).", "Tutorial 4, Q2(c)", "src")
    mc_val(B, ch, "Rates of change", 2, "A bacterium population is $b=10^6+10^4t-10^3t^2$ ($t$ in hours). The growth rate at $t=10$ h is", -10 ** 4, [10 ** 4, 0, -10 ** 3, -2 * 10 ** 4], "$b'(t)=10^4-2\\cdot10^3t$, so $b'(10)=10^4-2\\cdot10^4=-10^4$ per hour (the population is shrinking).", "Tutorial 4, Q3", "src")
    mc_val(B, ch, "Rates of change", 2, "For the same population, the growth rate at $t=5$ h is", 0, [10 ** 4, -10 ** 4, 5 * 10 ** 3, 10 ** 5], "$b'(5)=10^4-10^4=0$: the population has reached its maximum.", "Tutorial 4, Q3", "src")
    Dt = sp.Rational(10, 9) * tt ** 2; v_ = sp.diff(Dt, tt); tt0 = sp.solve(sp.Eq(v_, sp.Rational(500, 9)), tt)[0]; dist = Dt.subs(tt, tt0)
    assert tt0 == 25 and dist == sp.Rational(6250, 9)
    mc_val(B, ch, "Rates of change", 3, "An aircraft's distance along the runway is $D=\\frac{10}{9}t^2$ m ($t$ in s). It takes off at $200$ km/h $=\\frac{500}{9}$ m/s. After how many seconds?", 25, [50, 100, 20, 12.5], "$v=D'=\\frac{20}{9}t=\\frac{500}{9}\\Rightarrow t=25$ s (distance $\\frac{10}{9}\\cdot625\\approx694.4$ m).", "Tutorial 4, Q4", "src")
    # ---- related rates
    mc_val(B, ch, "Related rates", 3, "In $V=IR$, $V$ increases at $1$ V/s and $I$ decreases at $\\frac13$ A/s. When $V=12$ V and $I=2$ A, $\\dfrac{dR}{dt}=$ (ohms/s)", sp.Rational(3, 2), [-sp.Rational(3, 2), 3, sp.Rational(1, 2), -3],
           "$R=V/I$; $R'=\\frac{V'I-VI'}{I^2}=\\frac{1\\cdot2-12\\cdot(-\\frac13)}{4}=\\frac{6}{4}=\\frac32>0$: $R$ is increasing.", "Tutorial 4, Q7(d)", "src")
    ll, ww = 12, 5; dl, dw = -2, 2
    mc_val(B, ch, "Related rates", 3, "A rectangle's length decreases at $2$ cm/s and its width increases at $2$ cm/s. At $l=12$, $w=5$ the area changes at … cm²/s", ll * dw + ww * dl, [-14, 34, 0, 24], "$A=lw$: $A'=l'w+lw'=(-2)(5)+(12)(2)=14$ (increasing).", "Tutorial 4, Q9(a)", "src")
    mc_val(B, ch, "Related rates", 3, "For the same rectangle, the diagonal $d=\\sqrt{l^2+w^2}$ changes at … cm/s", sp.Rational(-14, 13), [sp.Rational(14, 13), 0, -14, sp.Rational(-14, 5)],
           "$d=13$ and $d'=\\frac{ll'+ww'}{d}=\\frac{12(-2)+5(2)}{13}=-\\frac{14}{13}$: the diagonal is decreasing while the area increases and the perimeter stays constant.", "Tutorial 4, Q9(c)", "src")
    B.mcq(ch, "Related rates", 2, "For the same rectangle ($l'=-2$, $w'=2$), the perimeter $P=2(l+w)$ is", "constant ($P'=0$)", ["increasing", "decreasing", "increasing at $4$ cm/s"], "$P'=2(l'+w')=2(-2+2)=0$.", "Tutorial 4, Q9(b)", "src")
    # ---- linearization and differentials
    B.mcq(ch, "Linearization", 2, "The linearization of $f(x)=\\sin x$ at $a=\\pi$ is", "$L(x)=\\pi-x$", ["$L(x)=x$", "$L(x)=x-\\pi$", "$L(x)=-x$"], "$f(\\pi)=0$, $f'(\\pi)=\\cos\\pi=-1$: $L(x)=0-1\\cdot(x-\\pi)=\\pi-x$.", "Tutorial 4, Q10(b)", "src")
    B.mcq(ch, "Linearization", 1, "The linearization of $f(x)=\\sin x$ at $a=0$ is", "$L(x)=x$", ["$L(x)=1$", "$L(x)=\\cos x$", "$L(x)=x+1$"], "$f(0)=0$, $f'(0)=1$: $L(x)=x$.", "Tutorial 4, Q10(a)", "src")
    mc_val(B, ch, "Linearization", 3, "The radius of a circle grows from $2.00$ m to $2.02$ m. The estimated change in area $dA$ (in m²) is", sp.Rational(8, 100) * sp.pi, [sp.Rational(4, 100) * sp.pi, sp.Rational(2, 100) * sp.pi, sp.Rational(16, 100) * sp.pi],
           "$dA=2\\pi r\\,dr=2\\pi(2)(0.02)=0.08\\pi\\approx0.251$ m². Relative to $A=4\\pi$ this is $2\\%$.", "Tutorial 4, Q11", "src")
    B.mcq(ch, "Linearization", 2, "Use $(1+x)^k\\approx1+kx$ to estimate $(1.0002)^{50}$.", "$1.01$", ["$1.0002$", "$1.10$", "$1.001$"], "$k=50$, $x=0.0002$: $1+50\\cdot0.0002=1.01$.", "Computation problems 4, Q11(a)", "src")
    B.mcq(ch, "Linearization", 2, "Use $(1+x)^k\\approx1+kx$ to estimate $\\sqrt[3]{1.009}$.", "$1.003$", ["$1.009$", "$1.03$", "$1.0003$"], "$k=\\frac13$, $x=0.009$: $1+\\frac13\\cdot0.009=1.003$.", "Computation problems 4, Q11(b)", "src")
    mc_val(B, ch, "Linearization", 3, "Estimate (using $dV=2\\pi rh\\,dr$) the volume in cubic inches of a cylindrical shell of height $30$, radius $6$ and thickness $0.5$.", 180 * sp.pi, [90 * sp.pi, 360 * sp.pi, 1080 * sp.pi, 36 * sp.pi],
           "$V=\\pi r^2h$, $dV=2\\pi rh\\,dr=2\\pi(6)(30)(0.5)=180\\pi\\approx565.5$ in³.", "Computation problems 4, Q12", "src")
    # ---- osculating circle (Tutorial 4 Q12) verified by solving
    h_, k0, a0 = sp.symbols("h k a", real=True)
    circ = (x - h_) ** 2 + (sp.Symbol("yy") - k0) ** 2 - a0 ** 2
    # parabola y=x^2+1 at (1,2): y'=2, y''=2
    eqs = [circ.subs({x: 1, sp.Symbol("yy"): 2}),
           (sp.diff(circ, x) + sp.diff(circ, sp.Symbol("yy")) * 2).subs({x: 1, sp.Symbol("yy"): 2}),
           (sp.diff(circ, x, 2) + 2 * sp.diff(circ, x, sp.Symbol("yy")) * 2 + sp.diff(circ, sp.Symbol("yy"), 2) * 4 + sp.diff(circ, sp.Symbol("yy")) * 2).subs({x: 1, sp.Symbol("yy"): 2})]
    solc = [s__ for s__ in sp.solve(eqs, [h_, k0, a0], dict=True) if s__[a0] > 0]
    assert solc and solc[0][h_] == -4 and solc[0][k0] == sp.Rational(9, 2) and sp.simplify(solc[0][a0] - 5 * sp.sqrt(5) / 2) == 0, solc
    B.mcq(ch, "Linearization", 3, "The circle $(x-h)^2+(y-k)^2=a^2$ is tangent to $y=x^2+1$ at $(1,2)$ and has the same second derivative there. Then $(h,k,a)=$", "$\\left(-4,\\tfrac92,\\tfrac{5\\sqrt5}{2}\\right)$",
          ["$\\left(4,\\tfrac92,\\tfrac{5\\sqrt5}{2}\\right)$", "$\\left(-4,-\\tfrac92,\\tfrac{5\\sqrt5}{2}\\right)$", "$\\left(-4,\\tfrac92,\\tfrac52\\right)$"],
          "Impose three conditions at $(1,2)$: the point lies on the circle, the slopes agree ($y'=2$), and the second derivatives agree ($y''=2$). Solving the three equations gives $h=-4$, $k=\\frac92$, $a=\\frac{5\\sqrt5}{2}$.", "Tutorial 4, Q12", "src")
