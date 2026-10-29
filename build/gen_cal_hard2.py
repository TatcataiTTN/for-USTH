# -*- coding: utf-8 -*-
"""Calculus I, level-4 pool in the style of the Moodle mock midterm, part 2: slots 8, 9, 10, 11, 14, 15, 17, 18 (limits, parity, derivatives at a point)."""
import itertools
import sympy as sp
from qlib import tex
from cal_common import E, lim_text, uniq_by_text
from gen_cal_hard1 import add, agree, nlim, vals, L, xr, sin, cos, tan, exp, log, sqrt, pi, R

# ------------------------------------------------------------------------------------------------ slot 8: infinite and one-sided limits (does the limit exist?)
def s08(B):
    cases = [   # f, x0, a plausible wrong finite value
        ((xr ** 3 - 8) / (xr ** 2 - 4), -2, [3, -3]),
        ((xr ** 3 - 8) / (xr ** 2 - 4), 2, [-6, 6]),
        (1 / xr - 1 / sp.Abs(xr), 0, [0, 2]),
        ((xr ** 2 - 1) / sp.Abs(xr - 1), 1, [2, -2]),
        ((xr ** 2 + xr - 6) / (xr ** 2 - 9), -3, [0, 5]),
        (sin(xr) / sp.Abs(xr), 0, [1, -1]),
    ]
    for f, x0, fin in cases:
        left, right = sp.limit(f, xr, x0, "-"), sp.limit(f, xr, x0, "+")
        h = R(1, 10**6)
        nl, nr = sp.N(f.subs(xr, x0 - h), 30), sp.N(f.subs(xr, x0 + h), 30)       # second route: sample both sides
        if left == right and left.is_finite:
            truth = left; agree(nl, truth, "s08 left", 1e-3); agree(nr, truth, "s08 right", 1e-3)
        elif left == right:
            truth = left; assert (float(nl) > 1e3) == (left == sp.oo)
        else:
            truth = None; assert abs(float(nl) - float(nr)) > 0.5 or abs(float(nl)) > 1e3 or abs(float(nr)) > 1e3
        dne = "the limit does not exist"
        ftex = "\\left(\\frac1x-\\frac1{|x|}\\right)" if f == 1 / xr - 1 / sp.Abs(xr) else tex(f)
        stem = "Evaluate $\\displaystyle\\lim_{x\\to%s}%s$." % (tex(x0), ftex)
        if truth is None:
            add(B, "c1", 8, 4, "Limits", stem, dne, [lim_text(sp.oo), lim_text(-sp.oo)] + [lim_text(sp.nsimplify(w)) for w in fin[:1]],
                "Compute the two one-sided limits: from the left it is %s and from the right it is %s. They are different, so the limit does **not exist**. Quoting one of the one-sided values (or $\\pm\\infty$) is the trap." % (lim_text(left), lim_text(right)))
        else:
            add(B, "c1", 8, 4, "Limits", stem, lim_text(truth), [lim_text(sp.oo) if truth != sp.oo else lim_text(-sp.oo), lim_text(-sp.oo) if truth != -sp.oo else lim_text(sp.oo), dne] + [lim_text(sp.nsimplify(w)) for w in fin],
                "Factor and cancel the vanishing factor (or compare the one-sided limits): both sides give %s, so the limit is %s." % (lim_text(truth), lim_text(truth)))

# ------------------------------------------------------------------------------------------------ slot 9: limits needing two conjugates
def s09(B):
    cases = [((3 - sqrt(xr)) / (5 - sqrt(xr + 16)), 9), ((sqrt(xr) - 2) / (sqrt(xr + 5) - 3), 4), ((3 - sqrt(xr + 5)) / (2 - sqrt(xr)), 4),
             ((sqrt(2 * xr + 1) - 3) / (sqrt(xr + 5) - 3), 4), ((sqrt(xr + 7) - 4) / (sqrt(xr) - 3), 9)]
    for f, x0 in cases:
        v = sp.limit(f, xr, x0)
        agree(v, nlim(f, x0), "s09 limit", 1e-4)
        wr = [1 / v, 2 * v, v / 2, 1] + ([v + 1] if v != 1 else [])
        add(B, "c1", 9, 4, "Limits", "Find the value of $\\displaystyle\\lim_{x\\to%s}%s$." % (tex(x0), tex(f)), L(v), vals(*[w for w in wr if sp.nsimplify(w) != v][:5]),
            "Both numerator and denominator vanish at $x=%s$ ($\\frac00$). Multiply the top **and** the bottom by their conjugates: each difference of square roots becomes a multiple of $(x-%s)$, which cancels. After cancelling it, substitute $x=%s$: the limit is %s." % (tex(x0), tex(x0), tex(x0), L(v)))

# ------------------------------------------------------------------------------------------------ slot 10: derivative of a product at a point
def s10(B):
    cases = [(exp(xr ** 2), cos(3 * xr), 0), (xr ** 2, exp(-xr), 2), (exp(-xr), sin(2 * xr), 0), (1 + xr ** 2, exp(2 * xr), 0), (xr, exp(-xr ** 2), 1), (exp(sin(xr)), cos(xr), 0)]
    for A, Bf, a in cases:
        h = A * Bf
        v = sp.simplify(sp.diff(h, xr).subs(xr, a))
        eps = R(1, 10**8)
        agree(v, (h.subs(xr, a + eps) - h.subs(xr, a - eps)) / (2 * eps), "s10 derivative")
        Ap, Bp = sp.diff(A, xr), sp.diff(Bf, xr)
        wr = [(Ap * Bp).subs(xr, a), (Ap * Bf).subs(xr, a), (A * Bp).subs(xr, a), -v, (Ap.subs(xr, a) + Bp.subs(xr, a))]
        wr = [sp.simplify(w) for w in wr if sp.simplify(w) != v]
        add(B, "c2", 10, 3, "Differentiation rules", "Given $h(x)=%s$, find $h'(%s)$." % (tex(h), tex(a)), L(v), vals(*wr, v + 1, v - 1, 2 * v + 1, v + 2, v - 2),
            "Product rule: $h'=A'B+AB'$ with $A=%s$, $B=%s$. At $x=%s$: $A'B=%s$ and $AB'=%s$, so $h'(%s)=%s$. The usual slips are $A'B'$, a missing chain-rule factor inside the exponential or trigonometric part, and dropping one of the two terms." % (
                tex(A), tex(Bf), tex(a), tex(sp.simplify((Ap * Bf).subs(xr, a))), tex(sp.simplify((A * Bp).subs(xr, a))), tex(a), tex(v)))

# ------------------------------------------------------------------------------------------------ slot 11: what a formula really is on its domain
def s11(B):
    zero = sp.Integer(0)
    assert zero / zero is sp.nan and sp.Rational(7, 3) / sp.Rational(7, 3) == 1             # x/x: undefined at 0, equal to 1 elsewhere
    add(B, "c1", 11, 3, "Domain", "The function $f(x)=\\dfrac{x}{x}$ is ... on its domain.", "constant", ["strictly decreasing", "strictly increasing", "not monotonic"],
        "The domain is $x\\ne0$ and $f(x)=1$ there, so $f$ is constant. The missing point $0$ does not change that: simplifying does not erase the restriction, but it does not create a second value either.")
    f2 = sp.Abs(xr) / xr
    assert all(f2.subs(xr, -v) == -f2.subs(xr, v) for v in (1, 2, R(1, 3)))
    add(B, "c1", 11, 3, "Even and odd functions", "Which statement about $f(x)=\\dfrac{|x|}{x}$ is true?", "$f$ is an odd function", ["$f(x)=1$ for every $x\\ne0$", "$f$ is continuous at $0$", "$f$ is an even function"],
        "For $x>0$, $f(x)=1$; for $x<0$, $f(x)=-1$. The domain $x\\ne0$ is symmetric and $f(-x)=-f(x)$, so $f$ is odd. It takes two values, so it is not constant, and it is not even defined at $0$.")
    f3 = (xr ** 2 - 1) / (xr - 1)
    assert sp.simplify(f3 - (xr + 1)) == 0 and f3.subs(xr, 1) is sp.nan
    add(B, "c1", 11, 3, "Domain", "Which statement about $f(x)=\\dfrac{x^2-1}{x-1}$ is true?", "its graph is the line $y=x+1$ with the point $(1,2)$ removed", ["its graph is the whole line $y=x+1$", "its graph has a vertical asymptote at $x=1$", "$f(1)=2$"],
        "For $x\\ne1$ we can cancel: $f(x)=x+1$. At $x=1$ the function is **undefined**, so the line has a hole at $(1,2)$. There is no vertical asymptote, because the limit at $1$ is finite ($=2$).")
    f4 = log(xr ** 2) / log(sp.Abs(xr))
    assert all(abs(float(sp.N(f4.subs(xr, v))) - 2) < 1e-12 for v in (R(1, 2), 3, -3, -R(1, 5)))
    add(B, "c1", 11, 4, "Domain", "Which statement about $f(x)=\\dfrac{\\ln(x^2)}{\\ln|x|}$ is true?", "$f(x)=2$ for every $x$ in its domain, and $x=0,\\pm1$ are not in the domain", ["$f(x)=2$ for every real $x$", "$f(x)=|x|$ on its domain", "$f(x)=2$ only for $x>0$"],
        "$\\ln(x^2)=2\\ln|x|$ for every $x\\ne0$, so the quotient equals $2$ wherever it is defined. It is undefined at $x=0$ ($\\ln0$), and at $x=\\pm1$ the denominator $\\ln|x|$ is $0$.")
    add(B, "c1", 11, 3, "Domain", "Which statement about $f(x)=e^{\\ln x}$ is true?", "$f(x)=x$ for $x>0$, and $f$ is undefined for $x\\le0$", ["$f(x)=x$ for every real $x$", "$f(x)=|x|$ for every real $x$", "$f(x)=x$ for $x\\ge0$"],
        "$\\ln x$ exists only for $x>0$, and for those $x$ we have $e^{\\ln x}=x$. The formula $x$ alone is defined everywhere, but $e^{\\ln x}$ is not: the domain is $(0,\\infty)$ (in particular $x=0$ is excluded).")
    f6 = sin(xr) ** 2 + cos(xr) ** 2
    assert sp.simplify(f6) == 1
    add(B, "c1", 11, 3, "Trigonometry", "The function $f(x)=\\sin^2x+\\cos^2x$ is ... on its domain.", "constant, with domain $\\mathbb R$", ["not constant, because it oscillates", "constant, but only for $x\\ne\\frac{\\pi}{2}+k\\pi$", "even but not constant"],
        "$\\sin^2x+\\cos^2x=1$ for every real $x$, so $f$ is the constant function $1$ on all of $\\mathbb R$ (no point is removed). A constant function is also even, but 'constant' is the stronger statement.")

# ------------------------------------------------------------------------------------------------ slot 14: continuity with parameters
def s14(B):
    a, b = sp.symbols("a b", real=True)
    items = [   # statement, the constant, wrong options (already formatted)
        ("Find the value of $a$ for which $f(x)=\\begin{cases}e^{x},&x<0\\\\ a+x,&x\\ge0\\end{cases}$ is continuous at $x=0$.", sp.solve(sp.Eq(1, a), a)[0], ["$0$", "$-1$", "any real number $a$ works", "no such $a$ exists"]),
        ("Find the value of $k$ for which $f(x)=\\begin{cases}\\dfrac{\\sin3x}{x},&x\\ne0\\\\ k,&x=0\\end{cases}$ is continuous at $x=0$.", sp.limit(sin(3 * xr) / xr, xr, 0), ["$1$", "$0$", "$\\frac13$", "no such $k$ exists"]),
        ("Find the value of $c$ for which $f(x)=\\begin{cases}\\dfrac{x^2-4}{x-2},&x\\ne2\\\\ c,&x=2\\end{cases}$ is continuous at $x=2$.", sp.limit((xr ** 2 - 4) / (xr - 2), xr, 2), ["$0$", "$2$", "$\\frac12$", "no such $c$ exists"]),
        ("Find the value of $k$ for which $f(x)=\\begin{cases}\\dfrac{1-\\cos x}{x^2},&x\\ne0\\\\ k,&x=0\\end{cases}$ is continuous at $x=0$.", sp.limit((1 - cos(xr)) / xr ** 2, xr, 0), ["$1$", "$0$", "$2$", "no such $k$ exists"]),
    ]
    for stem, val, wrong in items:
        val = sp.nsimplify(val)
        assert L(val) not in wrong
        add(B, "c1", 14, 3, "Continuity", stem, L(val), wrong,
            "Continuity at the junction needs $\\lim f(x)=f(\\text{junction})$. The limit of the formula there is %s, so the free constant must equal %s." % (L(val), L(val)))
    # two junctions: f(x)=x+1 (x<1); ax+b (1<=x<2); 3x-1 (x>=2)
    sol = sp.solve([sp.Eq(1 + 1, a * 1 + b), sp.Eq(a * 2 + b, 3 * 2 - 1)], [a, b])
    av, bv = sol[a], sol[b]
    target = av - bv
    add(B, "c1", 14, 4, "Continuity", "The function $f(x)=\\begin{cases}x+1,&x<1\\\\ ax+b,&1\\le x<2\\\\ 3x-1,&x\\ge2\\end{cases}$ is continuous everywhere. Find $a-b$.", L(target), vals(av + bv, bv - av, av * bv, 2 * av),
        "At $x=1$: $2=a+b$. At $x=2$: $2a+b=5$. Subtract: $a=3$, then $b=-1$. So $a-b=%s$ (note $a+b=2$ is only the first equation, and $ab=%s$)." % (tex(target), tex(av * bv)))

# ------------------------------------------------------------------------------------------------ slot 15: derivative of a quotient at a point
def paren(v):
    """A number for use in a product: negative values in brackets."""
    return "(%s)" % tex(v) if v < 0 else tex(v)

def s15(B):
    cases = [(1 + 2 * xr + xr * exp(xr), 1 - xr + xr ** 2 * exp(xr)), (exp(xr) + xr, 1 + sin(xr) + xr ** 2), (2 + xr * cos(xr), 1 + xr * exp(2 * xr)),
             (3 + sin(2 * xr), 2 + exp(-xr)), (1 + xr ** 2 + xr * exp(xr), 2 - xr * exp(xr))]
    for N, D in cases:
        Q = N / D
        v = sp.simplify(sp.diff(Q, xr).subs(xr, 0))
        eps = R(1, 10**8)
        agree(v, (Q.subs(xr, eps) - Q.subs(xr, -eps)) / (2 * eps), "s15 derivative")
        n0, d0, np0, dp0 = N.subs(xr, 0), D.subs(xr, 0), sp.diff(N, xr).subs(xr, 0), sp.diff(D, xr).subs(xr, 0)
        wr = [np0 / dp0 if dp0 != 0 else 0, (np0 * d0 + n0 * dp0) / d0 ** 2, np0 * d0 - n0 * dp0, (n0 * dp0 - np0 * d0) / d0 ** 2]
        wr = [sp.nsimplify(w) for w in wr if sp.nsimplify(w) != v]
        add(B, "c2", 15, 4, "Differentiation rules", "Compute $Q'(0)$ where $Q(x)=%s$." % tex(Q), L(v), vals(*wr, v + 1, v - 1, v + 2, v - 2),
            "Quotient rule at $x=0$ with $N(0)=%s$, $D(0)=%s$, $N'(0)=%s$, $D'(0)=%s$ (each from the product rule on the $x\\,e^{\\cdots}$ terms): $Q'(0)=\\dfrac{N'D-ND'}{D^2}=\\dfrac{%s\\cdot%s-%s\\cdot%s}{%s}=%s$." % (
                tex(n0), tex(d0), tex(np0), tex(dp0), paren(np0), paren(d0), paren(n0), paren(dp0), tex(d0 ** 2), tex(v)))

# ------------------------------------------------------------------------------------------------ slot 17: statements about limits and inequalities
def s17(B):
    qs = [
        ("Suppose $\\lim_{x\\to a}f(x)=A$ and $\\lim_{x\\to a}g(x)=B$, and $f(x)<g(x)$ for all $x\\ne a$ near $a$ (a **strict** inequality). Which conclusion must hold?", "$A\\le B$", ["$A<B$", "$A=B$", "$A\\ge B$"],
         "Limits preserve non-strict inequalities only: $f(x)=0<x^2=g(x)$ for $x\\ne0$, yet both limits at $0$ equal $0$. So $A\\le B$, not $A<B$."),
        ("If $\\lim_{x\\to a}f(x)$ exists and $\\lim_{x\\to a}g(x)$ does **not** exist, what can we say about $\\lim_{x\\to a}\\bigl(f(x)+g(x)\\bigr)$?", "it does not exist", ["it exists and equals $\\lim f$", "it exists but its value cannot be found", "it may or may not exist"],
         "If $f+g$ had a limit, then $g=(f+g)-f$ would have one too (difference of two convergent functions), a contradiction. So the sum has no limit."),
        ("If $\\lim_{x\\to a}f(x)g(x)=0$, which statement is true?", "nothing can be concluded about $\\lim f$ or $\\lim g$ separately", ["$\\lim_{x\\to a}f(x)=0$ or $\\lim_{x\\to a}g(x)=0$", "$f(a)=0$ or $g(a)=0$", "both limits exist"],
         "Take $f(x)=x$ and $g(x)=\\sin\\frac1x$ at $a=0$: the product tends to $0$ (squeeze) but $g$ has no limit. Or $f(x)=\\frac1x$, $g(x)=x^2$: the product $x\\to0$ although $f$ has no finite limit. The product rule works only in the **forward** direction: from the factors to the product."),
        ("If $|f(x)|\\le|x|$ for all $x$ near $0$, what is $\\lim_{x\\to0}f(x)$?", "$0$", ["$1$", "it does not exist", "it cannot be determined"],
         "$-|x|\\le f(x)\\le|x|$ and both bounds tend to $0$, so the Squeeze Theorem gives $\\lim f=0$. Nothing else about $f$ is needed (it may oscillate)."),
        ("Which of these statements about limits is **false**?", "if $f(a)=L$ then $\\lim_{x\\to a}f(x)=L$", ["a limit can exist even if $f(a)$ is undefined", "if $\\lim_{x\\to a}f(x)=L$ then $f(x)$ is as close to $L$ as we wish for $x\\ne a$ close to $a$", "if both limits exist, the limit of a sum is the sum of the limits"],
         "The value $f(a)$ says nothing about the limit: $f(x)=x^2$ for $x\\ne0$, $f(0)=1$ has $f(0)=1$ but $\\lim_{x\\to0}f=0$. (This is exactly the difference between a limit and continuity.)"),
    ]
    for stem, ok, wrong, expl in qs:
        add(B, "c1", 17, 3, "Limits", stem, ok, wrong, expl)

# ------------------------------------------------------------------------------------------------ slot 18: parity of combinations of an even f and an odd g
PARITY_ITEMS = {   # name -> (LaTeX, parity: +1 even, -1 odd, 0 neither, rule applied to f even / g odd), numeric test function
    "fg": ("f(x)g(x)", -1, lambda f, g: f * g), "f/g": ("\\dfrac{f(x)}{g(x)}", -1, lambda f, g: f / g), "g/f": ("\\dfrac{g(x)}{f(x)}", -1, lambda f, g: g / f),
    "f2": ("f(x)^2", 1, lambda f, g: f * f), "g2": ("g(x)^2", 1, lambda f, g: g * g), "g3": ("g(x)^3", -1, lambda f, g: g ** 3),
    "fog": ("f(g(x))", 1, None), "gof": ("g(f(x))", 1, None), "gog": ("g(g(x))", -1, None), "fof": ("f(f(x))", 1, None), "f+g": ("f(x)+g(x)", 0, lambda f, g: f + g), "ffg": ("f(x)^2g(x)", -1, lambda f, g: f * f * g),
}

def parity_of(fn):
    """+1 / -1 / 0 numerically over several points."""
    pts = [R(7, 10), R(13, 10), R(5, 2), R(1, 3)]
    even = all(abs(float(fn(v) - fn(-v))) < 1e-9 for v in pts)
    odd = all(abs(float(fn(v) + fn(-v))) < 1e-9 for v in pts)
    return 1 if even and not odd else (-1 if odd and not even else 0)

def s18(B):
    fs = [lambda s: s ** 2, lambda s: sp.cos(s), lambda s: s ** 4 + 1]
    gs = [lambda s: s, lambda s: s ** 3, lambda s: sp.sin(s), lambda s: s / (1 + s ** 2)]
    ask = [("odd", -1, ["fg", "f+g", "gof", "g2"]), ("even", 1, ["f2", "fog", "gog", "f/g"]), ("odd", -1, ["g3", "g/f", "fof", "f+g"]), ("even", 1, ["fog", "gof", "fg", "g2"]), ("odd", -1, ["ffg", "gog", "fog", "f/g"])]
    for word, want, names in ask:
        count = 0
        for nm in names:
            tex_, par, op = PARITY_ITEMS[nm]
            for f, g in itertools.product(fs, gs):                     # second route: every concrete pair (f even, g odd) obeys the rule
                fn = (lambda v, f=f, g=g, nm=nm: {"fog": f(g(v)), "gof": g(f(v)), "gog": g(g(v)), "fof": f(f(v))}[nm]) if op is None else (lambda v, f=f, g=g, op=op: op(f(v), g(v)))
                assert parity_of(lambda v: sp.N(fn(v), 30)) == par, "parity %s" % nm
            count += (par == want)
        items = "\n".join("%d. $%s$" % (i + 1, PARITY_ITEMS[n][0]) for i, n in enumerate(names))
        opts = ["$%d$" % c for c in range(0, 5)]
        correct = "$%d$" % count
        add(B, "c1", 18, 4, "Even and odd functions", "Assume $f$ is an even function and $g$ is an odd function, both defined on $\\mathbb R$ (quotients are considered where they are defined). How many of these functions are %s?\n%s" % (word, items), correct, [o for o in opts if o != correct],
            "Rules: even$\\times$even and odd$\\times$odd are even; even$\\times$odd is odd; a quotient follows the same rule; $f(g(x))$ is even when $g$ is odd and $f$ is even; $g(f(x))$ is even because $f(-x)=f(x)$; $g(g(x))$ is odd; $f+g$ is neither in general. The count of %s functions is %d." % (word, count))

def build_part2(B):
    for fn in (s08, s09, s10, s11, s14, s15, s17, s18):
        fn(B)
