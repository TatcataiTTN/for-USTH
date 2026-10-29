# -*- coding: utf-8 -*-
"""LA chapters 4-5: vector spaces and inner product spaces. Truth of every claim is checked by computation."""
import itertools, random
import sympy as sp
from qlib import tex, M, vec, system_tex, uniq_by_text, near_numbers, R, note
from la_common import *
from la_steps import mtx
from gen_la1 import mt, numopts

def V(v):
    return "$" + vec(list(v)) + "$"

def colstr(v):
    return "$" + mtx(sp.Matrix(list(v))) + "$"

def vecs_options(correct, rng, extras=(), n=3):
    """Option strings for a vector answer; wrong ones: given extras + single-entry perturbations / sign flips."""
    c = list(correct)
    wr = []
    for e in extras:
        e = list(e)
        if e != c:
            wr.append(V(e))
    for _ in range(40):
        w = list(c)
        i = rng.randrange(len(w))
        w[i] = sp.nsimplify(w[i] + rng.choice([-2, -1, 1, 2]))
        if w != c:
            wr.append(V(w))
        w2 = [-z for z in c]
        if w2 != c:
            wr.append(V(w2))
        if len(uniq_by_text(wr)) >= n + 2:
            break
    return V(c), uniq_by_text(wr)

# ----------------------------------------------------------------------------- axiom testing
def test_space(sampler, add, smul, contains, zero, rng, trials=120):
    """Return the set of failing properties (empirical, with random integer samples; witnesses are exact)."""
    fails = set()
    if not contains(zero):
        fails.add("zero")
    scal = [-3, -2, -1, 0, 1, 2, 3]
    for _ in range(trials):
        u, v = sampler(rng), sampler(rng)
        c, d = rng.choice(scal), rng.choice(scal)
        if not contains(add(u, v)):
            fails.add("add_closure")
        if not contains(smul(c, u)):
            fails.add("smul_closure")
        if smul(1, u) != u:
            fails.add("one")
        if add(smul(c, u), smul(d, u)) != smul(c + d, u):
            fails.add("dist_scalar")
        if add(smul(c, u), smul(c, v)) != smul(c, add(u, v)):
            fails.add("dist_vector")
        if smul(c * d, u) != smul(c, smul(d, u)):
            fails.add("assoc_scalar")
    return fails

PROP_TEXT = {
    "add_closure": "the set is not closed under addition",
    "smul_closure": "the set is not closed under scalar multiplication",
    "zero": "the set contains no zero vector",
    "one": "$1\\cdot u=u$ fails",
    "dist_scalar": "$(c+d)u=cu+du$ fails",
    "dist_vector": "$c(u+v)=cu+cv$ fails",
    "assoc_scalar": "$(cd)u=c(du)$ fails",
}

def vs_cases(rng):
    """Cases from Exercise Sheet 4, Ex. 3 (a)-(h). Returns list of dicts with computed failing properties."""
    def v3(r): return sp.Matrix([r.randint(-4, 4) for _ in range(3)])
    def v2(r): return sp.Matrix([r.randint(-4, 4) for _ in range(2)])
    def m2(r): return sp.Matrix(2, 2, lambda i, j: r.randint(-3, 3))
    def p2(r): return sp.Matrix([r.randint(-3, 3), r.randint(-3, 3), r.choice([-2, -1, 1, 2, 3])])   # a0,a1,a2 with a2 != 0
    cases = []
    cases.append(dict(tag="a", desc="$\\mathbb{R}^3$ with usual addition and $c\\cdot(x,y,z)=(cx,y,z)$",
                      sampler=v3, add=lambda u, v: u + v, smul=lambda c, u: sp.Matrix([c * u[0], u[1], u[2]]),
                      contains=lambda u: True, zero=sp.zeros(3, 1)))
    cases.append(dict(tag="b", desc="$\\mathbb{R}^2$ with usual addition and $c\\cdot(x,y)=(2cx,2cy)$",
                      sampler=v2, add=lambda u, v: u + v, smul=lambda c, u: 2 * c * u, contains=lambda u: True, zero=sp.zeros(2, 1)))
    cases.append(dict(tag="c", desc="the set $\\{(x,y):x\\ge0\\}$ with the usual operations of $\\mathbb{R}^2$",
                      sampler=lambda r: sp.Matrix([r.randint(0, 5), r.randint(-4, 4)]), add=lambda u, v: u + v, smul=lambda c, u: c * u,
                      contains=lambda u: u[0] >= 0, zero=sp.zeros(2, 1)))
    cases.append(dict(tag="d", desc="the set of all $2\\times2$ matrices with matrix addition and scalar multiplication",
                      sampler=m2, add=lambda u, v: u + v, smul=lambda c, u: c * u, contains=lambda u: True, zero=sp.zeros(2, 2)))
    cases.append(dict(tag="e", desc="the set of singular $2\\times2$ matrices (usual operations)",
                      sampler=lambda r: _singular(r), add=lambda u, v: u + v, smul=lambda c, u: c * u,
                      contains=lambda u: u.det() == 0, zero=sp.zeros(2, 2)))
    cases.append(dict(tag="f", desc="the set of non-singular $2\\times2$ matrices (usual operations)",
                      sampler=lambda r: _nonsingular(r), add=lambda u, v: u + v, smul=lambda c, u: c * u,
                      contains=lambda u: u.det() != 0, zero=sp.zeros(2, 2)))
    cases.append(dict(tag="g", desc="the set of matrices $\\begin{bmatrix}a&1\\\\1&b\\end{bmatrix}$ (usual operations)",
                      sampler=lambda r: sp.Matrix([[r.randint(-3, 3), 1], [1, r.randint(-3, 3)]]), add=lambda u, v: u + v, smul=lambda c, u: c * u,
                      contains=lambda u: u[0, 1] == 1 and u[1, 0] == 1, zero=sp.zeros(2, 2)))
    cases.append(dict(tag="h", desc="the set of polynomials of degree exactly $2$ (usual operations)",
                      sampler=p2, add=lambda u, v: u + v, smul=lambda c, u: c * u,
                      contains=lambda u: u[2] != 0, zero=sp.zeros(3, 1)))
    for cs in cases:
        cs["fails"] = test_space(cs["sampler"], cs["add"], cs["smul"], cs["contains"], cs["zero"], rng)
        cs["is_vs"] = not cs["fails"]
    return cases

def _singular(r):
    while True:
        Z = sp.Matrix(2, 2, lambda i, j: r.randint(-3, 3))
        if Z.det() == 0:
            return Z

def _nonsingular(r):
    while True:
        Z = sp.Matrix(2, 2, lambda i, j: r.randint(-3, 3))
        if Z.det() != 0:
            return Z

# ----------------------------------------------------------------------------- CHAPTER 4
def ch4(B):
    ch = "c4"; rng = B.rng
    # ---- Ex. 1-2 vector arithmetic
    u, v = sp.Matrix([1, 2, 3]), sp.Matrix([-1, 3, 4])
    r1 = 3 * u - 2 * v
    c, wr = vecs_options(r1, rng, extras=[3 * u + 2 * v, 2 * u - 3 * v, u - v])
    B.mcq(ch, "Vector arithmetic", 1, "For $u=(1,2,3)$ and $v=(-1,3,4)$, compute $3u-2v$.", c, wr,
          "$3u-2v=(3,6,9)-(-2,6,8)=%s$." % vec(list(r1)), "Exercise Sheet 4, Ex. 1", "src")
    uu, vv, ww = sp.Matrix([1, -1, 2]), sp.Matrix([0, 2, 3]), sp.Matrix([0, 1, 1])
    xs = (uu - 3 * vv - 2 * ww) / 2
    assert 2 * xs - uu + 3 * vv + 2 * ww == sp.zeros(3, 1)
    c, wr = vecs_options(xs, rng, extras=[(uu + 3 * vv + 2 * ww) / 2, uu - 3 * vv - 2 * ww, (uu - 3 * vv + 2 * ww) / 2])
    B.mcq(ch, "Vector arithmetic", 2, "Solve $2x-u+3v+2w=0$ for $x$, where $u=(1,-1,2)$, $v=(0,2,3)$, $w=(0,1,1)$.", c, wr,
          "$x=\\tfrac12(u-3v-2w)=\\tfrac12(1,-1-6-2,2-9-2)=%s$." % vec(list(xs)), "Exercise Sheet 4, Ex. 2", "src")

    # ---- Ex. 3 vector-space axioms (computed)
    cases = vs_cases(rng)
    by = {c_["tag"]: c_ for c_ in cases}
    assert by["d"]["is_vs"] and not any(by[t]["is_vs"] for t in "abcefgh")
    assert by["a"]["fails"] == {"dist_scalar"} and by["c"]["fails"] == {"smul_closure"} and by["e"]["fails"] == {"add_closure"}
    assert "one" in by["b"]["fails"] and "zero" in by["f"]["fails"] and "add_closure" in by["f"]["fails"]
    non = [c_ for c_ in cases if not c_["is_vs"]]
    for _ in range(3):
        wr = rng.sample(non, 3)
        B.mcq(ch, "Vector space axioms", 2, "Which of the following (with the stated operations) is a vector space?",
              by["d"]["desc"], [w["desc"] for w in wr],
              "All $2\\times2$ matrices satisfy the ten axioms. The others fail at least one: " +
              "; ".join("%s – %s" % (w["desc"], PROP_TEXT[sorted(w["fails"])[0]]) for w in wr) + ".",
              "Exercise Sheet 4, Ex. 3", "src")
    pool_all = ["add_closure", "smul_closure", "zero", "one", "dist_scalar", "dist_vector", "assoc_scalar"]
    for tag in "abcefgh":
        cs = by[tag]
        good = [pp for pp in pool_all if pp not in cs["fails"]]
        bad = sorted(cs["fails"])
        corr = bad[0] if tag not in "b" else "one"
        wrongs = rng.sample(good, 3) if len(good) >= 3 else good
        B.mcq(ch, "Vector space axioms", 3, "Why is %s NOT a vector space? Select the property that fails." % cs["desc"],
              PROP_TEXT[corr].capitalize() if PROP_TEXT[corr][0].isalpha() else PROP_TEXT[corr],
              [PROP_TEXT[w].capitalize() if PROP_TEXT[w][0].isalpha() else PROP_TEXT[w] for w in wrongs],
              "Test the axioms on examples: %s. The other listed properties do hold for this set." % PROP_TEXT[corr], "Exercise Sheet 4, Ex. 3(%s)" % tag, "src")

    # ---- Ex. 4 subspaces of R^3 (computed closure tests)
    def r3(r): return sp.Matrix([r.randint(-4, 4) for _ in range(3)])
    SUB = [
        ("the plane $b_1=0$", lambda r: sp.Matrix([0, r.randint(-4, 4), r.randint(-4, 4)]), lambda w: w[0] == 0, "Ex. 4(a)"),
        ("the plane $b_1=1$", lambda r: sp.Matrix([1, r.randint(-4, 4), r.randint(-4, 4)]), lambda w: w[0] == 1, "Ex. 4(b)"),
        ("the vectors with $b_2b_3=0$", lambda r: (lambda a_, b_: sp.Matrix([r.randint(-4, 4), a_, 0]) if r.random() < .5 else sp.Matrix([r.randint(-4, 4), 0, b_]))(r.randint(-4, 4), r.randint(-4, 4)), lambda w: w[1] * w[2] == 0, "Ex. 4(c)"),
        ("all combinations of $(1,1,0)$ and $(2,0,1)$", lambda r: r.randint(-3, 3) * sp.Matrix([1, 1, 0]) + r.randint(-3, 3) * sp.Matrix([2, 0, 1]),
         lambda w: sp.Matrix.hstack(sp.Matrix([1, 1, 0]), sp.Matrix([2, 0, 1]), w).rank() == 2, "Ex. 4(d)"),
        ("the plane $b_3-b_2+3b_1=0$", lambda r: (lambda a_, b_: sp.Matrix([a_, b_, b_ - 3 * a_]))(r.randint(-4, 4), r.randint(-4, 4)), lambda w: w[2] - w[1] + 3 * w[0] == 0, "Ex. 4(e)"),
        ("the vectors with $b_1\\ge0$", lambda r: sp.Matrix([r.randint(0, 4), r.randint(-4, 4), r.randint(-4, 4)]), lambda w: w[0] >= 0, "(generated)"),
        ("the vectors with $b_1=b_2^2$", lambda r: (lambda t_: sp.Matrix([t_ * t_, t_, r.randint(-4, 4)]))(r.randint(-3, 3)), lambda w: w[0] == w[1] ** 2, "(generated)"),
        ("the vectors with $b_1+b_2+b_3=0$", lambda r: (lambda a_, b_: sp.Matrix([a_, b_, -a_ - b_]))(r.randint(-4, 4), r.randint(-4, 4)), lambda w: sum(w) == 0, "(generated)"),
    ]
    subinfo = []
    for desc, samp, cont, src in SUB:
        fl = test_space(samp, lambda a_, b_: a_ + b_, lambda c_, a_: c_ * a_, cont, sp.zeros(3, 1), rng)
        fl = fl & {"zero", "add_closure", "smul_closure"}
        subinfo.append((desc, not fl, fl, src))
    truth = {d: ok for d, ok, _, _ in subinfo}
    assert [ok for _, ok, _, _ in subinfo] == [True, False, False, True, True, False, False, True]
    yes = [x for x in subinfo if x[1]]; no = [x for x in subinfo if not x[1]]
    for i in range(4):
        corr = yes[i % len(yes)]
        wr = rng.sample(no, 3)
        B.mcq(ch, "Subspaces", 2, "Which of the following subsets of $\\mathbb{R}^3$ is a subspace?", corr[0], [w[0] for w in wr],
              "A subspace must contain $0$ and be closed under addition and scalar multiplication. The other options fail: " +
              "; ".join("%s → %s" % (w[0], ", ".join({"zero": "no zero vector", "add_closure": "not closed under addition", "smul_closure": "not closed under scalar multiplication"}[f] for f in sorted(w[2]))) for w in wr) + ".",
              ("Exercise Sheet 4, " + corr[3]) if corr[3].startswith("Ex.") else "Generated (Sheet 4 style)", "src" if corr[3].startswith("Ex.") else "gen")
    for i in range(4):
        corr = no[i % len(no)]
        wr = rng.sample(yes, 3)
        B.mcq(ch, "Subspaces", 2, "Which of the following subsets of $\\mathbb{R}^3$ is NOT a subspace?", corr[0], [w[0] for w in wr],
              "%s fails: %s. The other three contain $0$ and are closed under both operations." % (corr[0], ", ".join({"zero": "no zero vector", "add_closure": "not closed under addition", "smul_closure": "not closed under scalar multiplication"}[f] for f in sorted(corr[2]))),
              ("Exercise Sheet 4, " + corr[3]) if corr[3].startswith("Ex.") else "Generated (Sheet 4 style)", "src" if corr[3].startswith("Ex.") else "gen")

    # ---- Ex. 5 linear combination
    u1, u2, u3 = sp.Matrix([1, -1, 2]), sp.Matrix([2, 4, -2]), sp.Matrix([1, 2, -4]); tv = sp.Matrix([3, 0, -6])
    Pm = sp.Matrix.hstack(u1, u2, u3); co = Pm.LUsolve(tv)
    assert Pm * co == tv
    for j in range(3):
        c, wr = numopts(co[j], rng, extra=[co[(j + 1) % 3], -co[j], sum(co)])
        B.mcq(ch, "Linear combinations", 2, "Write $v=(3,0,-6)$ as $c_1u_1+c_2u_2+c_3u_3$ with $u_1=(1,-1,2)$, $u_2=(2,4,-2)$, $u_3=(1,2,-4)$. What is $c_%d$?" % (j + 1), c, wr,
              "Solve $[u_1\\ u_2\\ u_3]c=v$: $\\det[u_1\\ u_2\\ u_3]=%s\\neq0$, so the solution is unique: $c=%s$." % (tex(Pm.det()), vec(list(co))), "Exercise Sheet 4, Ex. 5", "src")

    # ---- Ex. 6-8 span / independence / basis
    def span_info(vs, dim):
        Pm_ = sp.Matrix.hstack(*[sp.Matrix(v) for v in vs]); rk = Pm_.rank(); n = len(vs)
        return rk, n, rk == n, rk == dim
    S6 = [(2, 0, -1), (2, -1, 1), (4, 2, 0)]
    rk, n, indep, spans = span_info(S6, 3)
    assert indep and spans
    B.mcq(ch, "Span, independence, basis", 2, "Is $S=\\{(2,0,-1),(2,-1,1),(4,2,0)\\}$ a basis of $\\mathbb{R}^3$?",
          "Yes: it is independent and spans $\\mathbb{R}^3$", ["No: it is linearly dependent", "No: it is independent but does not span $\\mathbb{R}^3$", "No: it spans but is dependent"],
          "$\\det\\begin{bmatrix}2&2&4\\\\0&-1&2\\\\-1&1&0\\end{bmatrix}=%s\\neq0$; three independent vectors in $\\mathbb{R}^3$ form a basis." % tex(sp.Matrix.hstack(*[sp.Matrix(z) for z in S6]).det()), "Exercise Sheet 4, Ex. 6", "src")
    # P3 basis
    S7 = [[1, -1, 0, 0], [0, 2, 3, 0], [0, 0, 1, -2], [2, 0, 0, 1]]
    d7 = sp.Matrix(S7).det()
    ans7 = ("Yes: the four coefficient vectors are independent ($\\det=%s\\neq0$)" % tex(d7)) if d7 != 0 else "No: they are dependent ($\\det=0$)"
    alt7 = ["No: they are dependent ($\\det=0$)", "No: they span only a 3-dimensional subspace", "Yes: any 4 polynomials of degree $\\le3$ form a basis"]
    if d7 == 0:
        alt7 = ["Yes: the four coefficient vectors are independent", "Yes: any 4 polynomials of degree $\\le3$ form a basis", "No: they span a 4-dimensional space but are dependent"]
    B.mcq(ch, "Span, independence, basis", 3, "Is $S=\\{1-x,\\ 2x+3x^2,\\ x^2-2x^3,\\ 2+x^3\\}$ a basis of $P_3(x)$ (polynomials of degree $\\le3$)?", ans7, alt7,
          "Write each polynomial in the basis $\\{1,x,x^2,x^3\\}$: rows $%s$. $\\dim P_3=4$, and $\\det=%s$, so %s." % (mtx(sp.Matrix(S7)), tex(d7), "they form a basis" if d7 != 0 else "they do not form a basis"), "Exercise Sheet 4, Ex. 7", "src")
    # M2x2 basis
    S8 = [[1, 0, 0, 1], [-1, 0, 1, 1], [2, 1, 1, 0], [1, 1, 0, 1]]
    d8 = sp.Matrix(S8).det()
    ans8 = "Yes: the four coordinate vectors are independent ($\\det=%s\\neq0$)" % tex(d8) if d8 != 0 else "No: they are dependent ($\\det=0$)"
    alt8 = ["No: they are dependent ($\\det=0$)", "No: they span only a 3-dimensional subspace", "Yes: any 4 matrices form a basis of $M_{2\\times2}$"] if d8 != 0 else \
        ["Yes: the four coordinate vectors are independent", "Yes: any 4 matrices form a basis of $M_{2\\times2}$", "No: they span a 4-dimensional space but are dependent"]
    B.mcq(ch, "Span, independence, basis", 3, "Is $S=\\left\\{\\begin{bmatrix}1&0\\\\0&1\\end{bmatrix},\\begin{bmatrix}-1&0\\\\1&1\\end{bmatrix},\\begin{bmatrix}2&1\\\\1&0\\end{bmatrix},\\begin{bmatrix}1&1\\\\0&1\\end{bmatrix}\\right\\}$ a basis of $M_{2\\times2}$?", ans8, alt8,
          "Identify each matrix with $(a_{11},a_{12},a_{21},a_{22})$: rows $%s$ with $\\det=%s$; $\\dim M_{2\\times2}=4$." % (mtx(sp.Matrix(S8)), tex(d8)), "Exercise Sheet 4, Ex. 8", "src")

    # ---- Ex. 9-13 null space / rank / row & column space
    NS = [("A=\\begin{bmatrix}1&2\\\\2&1\\end{bmatrix}", sp.Matrix([[1, 2], [2, 1]]), "Ex. 9(a)"), ("A=\\begin{bmatrix}1&2&3\\end{bmatrix}", sp.Matrix([[1, 2, 3]]), "Ex. 9(b)"),
          ("A=\\begin{bmatrix}1&0&-2&0\\\\4&-2&4&-2\\\\-2&0&1&3\\end{bmatrix}", sp.Matrix([[1, 0, -2, 0], [4, -2, 4, -2], [-2, 0, 1, 3]]), "Ex. 9(c)"),
          ("A=\\begin{bmatrix}1&3&2&22&13\\\\1&0&2&-2&1\\\\3&6&5&42&27\\end{bmatrix}", sp.Matrix([[1, 3, 2, 22, 13], [1, 0, 2, -2, 1], [3, 6, 5, 42, 27]]), "Ex. 12")]
    for tx, A, src in NS:
        ns = A.nullspace(); nul = len(ns)
        B.mcq(ch, "Null space and rank", 2, "What is the dimension of the solution space of $Ax=0$ for $%s$?" % tx, "$%d$" % nul, ["$%d$" % z for z in sorted({0, 1, 2, 3, 4} - {nul})][:3],
              "Row-reduce: rank $=%d$, so nullity $=n-\\operatorname{rank}=%d-%d=%d$%s." % (A.rank(), A.cols, A.rank(), nul, (" with basis " + ", ".join(V(v_) for v_ in ns)) if ns else " (only the trivial solution)"), "Exercise Sheet 4, " + src, "src")
    RK = [("\\begin{bmatrix}1&2&-1\\end{bmatrix}", sp.Matrix([[1, 2, -1]]), "Ex. 10(a)"), ("\\begin{bmatrix}1&2\\\\-4&3\\\\6&1\\end{bmatrix}", sp.Matrix([[1, 2], [-4, 3], [6, 1]]), "Ex. 10(b)"),
          ("\\begin{bmatrix}1&2&0\\\\-1&4&1\\\\0&1&3\\end{bmatrix}", sp.Matrix([[1, 2, 0], [-1, 4, 1], [0, 1, 3]]), "Ex. 10(c)")]
    for tx, A, src in RK:
        rk = A.rank()
        B.mcq(ch, "Null space and rank", 1, "Find the rank of $A=%s$." % tx, "$%d$" % rk, ["$%d$" % z for z in sorted({0, 1, 2, 3, 4} - {rk})][:3],
              "Row-reduce $A$ to echelon form; the number of non-zero rows is $%d$ (this equals $\\dim$ of the row space and of the column space)." % rk, "Exercise Sheet 4, " + src, "src")
    S11 = [(1, 2, 2), (-1, 0, 0), (1, 1, 1)]
    rk11 = sp.Matrix(S11).rank()
    B.mcq(ch, "Span, independence, basis", 2, "What is $\\dim\\operatorname{span}\\{(1,2,2),(-1,0,0),(1,1,1)\\}$?", "$%d$" % rk11, ["$%d$" % z for z in sorted({1, 2, 3, 0} - {rk11})][:3],
          "Put the vectors as rows and row-reduce: rank $=%d$. So the span has dimension %d and a basis is given by the independent rows." % (rk11, rk11), "Exercise Sheet 4, Ex. 11", "src")
    # Ex 13 nonhomogeneous
    A13 = sp.Matrix([[1, 2, 1, 1, 5], [-5, -10, 3, 3, 55], [1, 2, 2, -3, -5], [-1, -2, 1, 1, 15]]); b13 = sp.Matrix([0, -8, 14, -2])
    kind, sol, free = solve_sys(A13, b13)
    nf = len(free)
    fp = lambda k_: "Consistent, with %d free parameter%s" % (k_, "" if k_ == 1 else "s")
    correct_txt = fp(nf) if kind != "none" else "Inconsistent"
    cand = ["Inconsistent", fp(nf + 1), fp(max(nf - 1, 0)), fp(nf + 2), "Consistent, with a unique solution"]
    B.mcq(ch, "Null space and rank", 3, "Is $Ax=b$ consistent for $A=%s$, $b=%s$? If so, how many free parameters does $x=x_p+x_h$ have?" % (mtx(A13), mtx(b13)),
          correct_txt, [z for z in cand if z != correct_txt],
          "Row-reduce $[A\\mid b]$: $\\operatorname{rank}A=%d$, $\\operatorname{rank}[A\\mid b]=%d$. %s" % (A13.rank(), A13.row_join(b13).rank(), "Consistent; free variables $=5-%d=%d$, so $x=x_p+x_h$ with $x_h\\in\\ker A$ of dimension %d." % (A13.rank(), nf, nf) if kind != "none" else "The ranks differ, so there is no solution."),
          "Exercise Sheet 4, Ex. 13", "src")

    # ---- Ex. 14-17 coordinates
    xB = sp.Matrix([3, 5]); Bm = sp.Matrix.hstack(sp.Matrix([1, 1]), sp.Matrix([-1, 1])); xs = Bm * xB
    c, wr = vecs_options(xs, rng, extras=[xB, sp.Matrix([5, 3]), Bm.T * xB])
    B.mcq(ch, "Coordinates and change of basis", 2, "Let $B=\\{(1,1),(-1,1)\\}$ and $[x]_B=(3,5)^T$. What is $x$ in the standard basis?", c, wr,
          "$x=3(1,1)+5(-1,1)=%s$." % vec(list(xs)), "Exercise Sheet 4, Ex. 14", "src")
    COORD = [("$B=\\{(1,1),(0,-2)\\}$, $x=(2,-1)$", [(1, 1), (0, -2)], (2, -1), "Ex. 15(a)"),
             ("$B=\\{(1,0,0),(0,1,0),(1,1,1)\\}$, $x=(4,-2,9)$", [(1, 0, 0), (0, 1, 0), (1, 1, 1)], (4, -2, 9), "Ex. 15(b)"),
             ("$B=\\{(1,2,3),(1,2,0),(0,-6,2)\\}$, $x=(3,-3,0)$", [(1, 2, 3), (1, 2, 0), (0, -6, 2)], (3, -3, 0), "Ex. 15(c)")]
    for tx, Bv, x, src in COORD:
        Pm = sp.Matrix.hstack(*[sp.Matrix(z) for z in Bv]); co = Pm.LUsolve(sp.Matrix(x)); assert Pm * co == sp.Matrix(x)
        extras = [x, list(reversed(list(co))), list(Pm.T.LUsolve(sp.Matrix(x)))]
        c, wr = vecs_options(co, rng, extras=extras)
        B.mcq(ch, "Coordinates and change of basis", 2, "Find $[x]_B$ for %s." % tx, c, wr,
              "Solve $c_1b_1+\\dots+c_nb_n=x$, i.e. $P c=x$ with $P=%s$: $[x]_B=%s$ (check: $Pc=x$)." % (mtx(Pm), vec(list(co))), "Exercise Sheet 4, " + src, "src")
    # Ex 16
    for tx, Bv, Bpv, xB_, src in (("$B=\\{(1,1),(1,-1)\\}$, $B'=\\{(0,1),(1,2)\\}$, $[x]_B=(3,-3)^T$", [(1, 1), (1, -1)], [(0, 1), (1, 2)], (3, -3), "Ex. 16(a)"),
                                  ("$B=\\{(1,0,0),(1,1,0),(1,1,1)\\}$, $B'=\\{(0,0,1),(0,1,1),(1,1,1)\\}$, $[x]_B=(-1,2,-3)^T$", [(1, 0, 0), (1, 1, 0), (1, 1, 1)], [(0, 0, 1), (0, 1, 1), (1, 1, 1)], (-1, 2, -3), "Ex. 16(b)")):
        PB = sp.Matrix.hstack(*[sp.Matrix(z) for z in Bv]); PBp = sp.Matrix.hstack(*[sp.Matrix(z) for z in Bpv])
        xs = PB * sp.Matrix(xB_); res = PBp.LUsolve(xs); assert PBp * res == xs
        wrong_dir = (PB.LUsolve(PBp * sp.Matrix(xB_)))
        c, wr = vecs_options(res, rng, extras=[xB_, list(xs), list(wrong_dir)])
        B.mcq(ch, "Coordinates and change of basis", 3, "Find $[x]_{B'}$ given %s." % tx, c, wr,
              "First $x=P_B[x]_B=%s$ (standard coordinates), then solve $P_{B'}[x]_{B'}=x$: $[x]_{B'}=%s$." % (vec(list(xs)), vec(list(res))), "Exercise Sheet 4, " + src, "src")
    # Ex 17 transition matrices
    for tx, Bv, Bpv, src in (("$B=\\{(1,-1),(3,1)\\}$, $B'=\\{(1,2),(-1,0)\\}$", [(1, -1), (3, 1)], [(1, 2), (-1, 0)], "Ex. 17(a)"),
                             ("$B=\\{(1,1,1),(1,1,0),(1,0,0)\\}$, $B'=\\{(1,2,3),(0,1,0),(1,0,1)\\}$", [(1, 1, 1), (1, 1, 0), (1, 0, 0)], [(1, 2, 3), (0, 1, 0), (1, 0, 1)], "Ex. 17(b)")):
        PB = sp.Matrix.hstack(*[sp.Matrix(z) for z in Bv]); PBp = sp.Matrix.hstack(*[sp.Matrix(z) for z in Bpv])
        Pt = PBp.inv() * PB
        assert Pt * sp.Matrix([1] + [0] * (len(Bv) - 1)) == PBp.inv() * sp.Matrix(Bv[0])
        B.mcq(ch, "Coordinates and change of basis", 3, "Find the transition matrix from $B$ to $B'$: %s." % tx, mt(Pt),
              [mt(Pt.inv()), mt(Pt.T), mt(perturb(Pt, rng))],
              "$[x]_{B'}=P[x]_B$ with $P=P_{B'}^{-1}P_B$ (row-reduce $[B'\\mid B]\\to[I\\mid P]$): $P=%s$. (Its inverse is the transition matrix from $B'$ to $B$.)" % mtx(Pt), "Exercise Sheet 4, " + src, "src")
    B.mcq(ch, "Span, independence, basis", 2, "If $v_1,v_2,v_3$ are linearly independent, is $\\{v_1-v_2,\\ v_2-v_3,\\ v_3-v_1\\}$ independent?",
          "No: the three vectors sum to $0$, so they are dependent", ["Yes: it is again an independent set", "Yes, because it has three vectors", "It depends on the vector space $V$"],
          "$(v_1-v_2)+(v_2-v_3)+(v_3-v_1)=0$ is a non-trivial dependence relation.", "Exercise Sheet 4, Ex. 18", "src")
    # past exam bases
    for tx, S, src in (("$B=\\{(1,2,0),(1,0,-1),(-2,1,2)\\}$", [(1, 2, 0), (1, 0, -1), (-2, 1, 2)], "Final 2024–25 Shift 1, Q3(b)"),
                       ("$B=\\{(1,0,1),(1,1,1),(1,2,0)\\}$", [(1, 0, 1), (1, 1, 1), (1, 2, 0)], "Final 2018–19 (D,E,G), Q4(a)"),
                       ("$B=\\{(1,1,1),(-1,1,0),(1,2,1)\\}$", [(1, 1, 1), (-1, 1, 0), (1, 2, 1)], "Final 2019–20, Q4")):
        Pm = sp.Matrix.hstack(*[sp.Matrix(z) for z in S]); d = Pm.det(); assert d != 0
        c, wr = numopts(d, rng, extra=[-d, d + 1, 0])
        B.mcq(ch, "Span, independence, basis", 2, "Exam: to prove that %s is a basis of $\\mathbb{R}^3$ it suffices to show $\\det[v_1\\ v_2\\ v_3]\\neq0$. What is this determinant?" % tx, c, wr,
              "$\\det%s=%s\\neq0$, so the three vectors are independent and form a basis of $\\mathbb{R}^3$." % (mtx(Pm), tex(d)), src, "src")
    # conceptual
    B.mcq(ch, "Span, independence, basis", 1, "Any basis of $\\mathbb{R}^4$ has exactly …", "4 vectors", ["3 vectors", "5 vectors", "as many vectors as you like"], "The dimension of $\\mathbb{R}^n$ is $n$; every basis has $n$ vectors.", "Lecture 4", "concept")
    B.mcq(ch, "Null space and rank", 1, "For an $m\\times n$ matrix, $\\operatorname{rank}A+\\operatorname{nullity}A=$", "$n$", ["$m$", "$m+n$", "$mn$"], "Rank–nullity: columns = pivot columns + free columns.", "Lecture 4", "concept")
    B.mcq(ch, "Subspaces", 1, "$\\dim M_{2\\times2}=$", "4", ["2", "3", "6"], "Basis $E_{11},E_{12},E_{21},E_{22}$.", "Lecture 4", "concept")
    B.mcq(ch, "Subspaces", 1, "$\\dim P_n(x)$ (polynomials of degree $\\le n$) $=$", "$n+1$", ["$n$", "$n+2$", "$2n$"], "Basis $1,x,\\dots,x^n$.", "Lecture 4", "concept")
    # random rank / dimension questions
    for _ in range(6):
        A = sp.Matrix(3, 4, lambda i, j: rng.randint(-2, 3)); A[2, :] = A[0, :] + A[1, :] * rng.choice([1, -1, 2])
        rk = A.rank()
        B.mcq(ch, "Null space and rank", 2, "Let $A=%s$. What is $\\dim\\ker A$ (the nullity)?" % mtx(A), "$%d$" % (4 - rk), ["$%d$" % z for z in sorted({0, 1, 2, 3, 4} - {4 - rk})][:3],
              "Row 3 is a combination of rows 1 and 2; row-reducing gives rank $%d$. Nullity $=4-%d=%d$." % (rk, rk, 4 - rk), "Generated (rank–nullity)", "gen")
    tt = sp.Symbol("t")
    made = 0
    while made < 4:
        v1 = sp.Matrix([rng.randint(-2, 3) for _ in range(3)]); v2 = sp.Matrix([rng.randint(-2, 3) for _ in range(3)])
        v3 = sp.Matrix([rng.randint(-2, 3), tt, rng.randint(-2, 3)])
        Pm = sp.Matrix.hstack(v1, v2, v3)
        dpoly = sp.expand(Pm.det())
        if dpoly.has(tt) and sp.degree(dpoly, tt) == 1:
            root = sp.solve(dpoly, tt)[0]
            if root.q <= 3 and abs(root) <= 6:
                lc = lambda z: "$t=%s$" % tex(z)
                if B.mcq(ch, "Span, independence, basis", 3, "For which value of $t$ are the vectors $%s,\\ %s,\\ (%s,t,%s)$ linearly dependent?" % (vec(list(v1)), vec(list(v2)), tex(v3[0]), tex(v3[2])),
                         lc(root), [lc(z) for z in (-root, root + 1, root - 1, 2 * root + 3)],
                         "Three vectors in $\\mathbb{R}^3$ are dependent iff the determinant of the matrix with these columns vanishes: $\\det=%s=0$ ⇒ $t=%s$." % (tex(dpoly), tex(root)), "Generated (independence with a parameter)", "gen"):
                    made += 1

# ----------------------------------------------------------------------------- CHAPTER 5
def ip_axioms(ip, rng, trials=120):
    """Empirically test symmetry, additivity, homogeneity and positivity of a candidate inner product on R^2."""
    fails = set()
    for _ in range(trials):
        u = sp.Matrix([rng.randint(-3, 3) for _ in range(2)]); v = sp.Matrix([rng.randint(-3, 3) for _ in range(2)]); w = sp.Matrix([rng.randint(-3, 3) for _ in range(2)])
        c = rng.choice([-2, -1, 2, 3])
        if ip(u, v) != ip(v, u): fails.add("symmetry")
        if ip(u + v, w) != ip(u, w) + ip(v, w): fails.add("additivity")
        if ip(c * u, v) != c * ip(u, v): fails.add("homogeneity")
        if ip(u, u) < 0 or (ip(u, u) == 0 and u != sp.zeros(2, 1)): fails.add("positivity")
    # positivity witnesses with all small vectors
    for a_ in range(-3, 4):
        for b_ in range(-3, 4):
            u = sp.Matrix([a_, b_])
            if ip(u, u) < 0 or (ip(u, u) == 0 and u != sp.zeros(2, 1)): fails.add("positivity")
    return fails

def ch5(B):
    ch = "c5"; rng = B.rng
    def sq(x):
        return sp.sqrt(x)
    # ---- Ex. 1-2
    u, v = sp.Matrix([1, -1, 2]), sp.Matrix([2, 3, 1])
    nu, nv, ip_, dd = sq(u.dot(u)), sq(v.dot(v)), u.dot(v), sq((u - v).dot(u - v))
    B.mcq(ch, "Norm, distance, angle", 1, "For $u=(1,-1,2)$ and $v=(2,3,1)$ with the dot product, $\\|u\\|=$", "$%s$" % tex(nu), ["$%s$" % tex(z) for z in (u.dot(u), sq(v.dot(v)), sq(u.dot(u) + 1))], "$\\|u\\|=\\sqrt{1+1+4}=%s$." % tex(nu), "Exercise Sheet 5, Ex. 1(a)", "src")
    c, wr = numopts(ip_, rng, extra=[u.dot(u), -ip_ + 2, sum(u) + sum(v)])
    B.mcq(ch, "Norm, distance, angle", 1, "For $u=(1,-1,2)$ and $v=(2,3,1)$, $\\langle u,v\\rangle=$", c, wr, "$1\\cdot2+(-1)\\cdot3+2\\cdot1=%s$." % tex(ip_), "Exercise Sheet 5, Ex. 1(c)", "src")
    B.mcq(ch, "Norm, distance, angle", 2, "For $u=(1,-1,2)$ and $v=(2,3,1)$, the distance $d(u,v)=$", "$%s$" % tex(dd), ["$%s$" % tex(z) for z in (sq((u + v).dot(u + v)), nu + nv, sq(u.dot(u) + v.dot(v)))],
          "$d(u,v)=\\|u-v\\|=\\|(-1,-4,1)\\|=\\sqrt{1+16+1}=%s$." % tex(dd), "Exercise Sheet 5, Ex. 1(d)", "src")
    W = sp.diag(1, 2, 1)
    u2, v2 = sp.Matrix([1, 1, 1]), sp.Matrix([2, 5, 2])
    ipw = (u2.T * W * v2)[0]; nuw = sq((u2.T * W * u2)[0]); nvw = sq((v2.T * W * v2)[0]); dw = sq(((u2 - v2).T * W * (u2 - v2))[0])
    c, wr = numopts(ipw, rng, extra=[u2.dot(v2), ipw + 2, (u2.T * W * u2)[0]])
    B.mcq(ch, "Norm, distance, angle", 2, "In $\\mathbb{R}^3$ with $\\langle u,v\\rangle=u_1v_1+2u_2v_2+u_3v_3$, compute $\\langle(1,1,1),(2,5,2)\\rangle$.", c, wr,
          "$1\\cdot2+2\\cdot1\\cdot5+1\\cdot2=%s$ (note the weight $2$ on the second coordinate)." % tex(ipw), "Exercise Sheet 5, Ex. 2(c)", "src")
    B.mcq(ch, "Norm, distance, angle", 2, "With the weighted product $\\langle u,v\\rangle=u_1v_1+2u_2v_2+u_3v_3$, the norm $\\|(2,5,2)\\|$ is", "$%s$" % tex(nvw), ["$%s$" % tex(z) for z in (sq(v2.dot(v2)), sq((v2.T * W * v2)[0] + 1), 3 * sq(5))],
          "$\\|v\\|^2=2^2+2\\cdot5^2+2^2=%s$, so $\\|v\\|=%s$." % (tex((v2.T * W * v2)[0]), tex(nvw)), "Exercise Sheet 5, Ex. 2(b)", "src")
    B.mcq(ch, "Norm, distance, angle", 2, "With the weighted product $\\langle u,v\\rangle=u_1v_1+2u_2v_2+u_3v_3$, the distance between $(1,1,1)$ and $(2,5,2)$ is", "$%s$" % tex(dw),
          ["$%s$" % tex(z) for z in (sq((u2 - v2).dot(u2 - v2)), sq(((u2 - v2).T * W * (u2 - v2))[0] + 1), nuw + nvw)],
          "$d^2=(1-2)^2+2(1-5)^2+(1-2)^2=%s$, so $d=%s$." % (tex(((u2 - v2).T * W * (u2 - v2))[0]), tex(dw)), "Exercise Sheet 5, Ex. 2(d)", "src")
    # ---- Ex. 3 function inner product
    xx = sp.Symbol("x")
    f, g = xx ** 2, xx ** 2 + 1
    ipfg = sp.integrate(f * g, (xx, -1, 1)); nf = sp.sqrt(sp.integrate(f * f, (xx, -1, 1))); ng = sp.sqrt(sp.integrate(g * g, (xx, -1, 1)))
    c, wr = numopts(ipfg, rng, extra=[sp.integrate(f, (xx, -1, 1)) * sp.integrate(g, (xx, -1, 1)), sp.integrate(f * g, (xx, 0, 1)), ipfg + 1])
    B.mcq(ch, "Function spaces", 2, "In $C[-1,1]$ with $\\langle f,g\\rangle=\\int_{-1}^{1}f(x)g(x)\\,dx$, compute $\\langle x^2,\\,x^2+1\\rangle$.", c, wr,
          "$\\int_{-1}^{1}(x^4+x^2)\\,dx=\\tfrac25+\\tfrac23=%s$." % tex(ipfg), "Exercise Sheet 5, Ex. 3(a)", "src")
    B.mcq(ch, "Function spaces", 3, "In $C[-1,1]$ with $\\langle f,g\\rangle=\\int_{-1}^{1}fg\\,dx$, $\\|x^2+1\\|=$", "$%s$" % tex(ng), ["$%s$" % tex(z) for z in (nf, sp.sqrt(sp.integrate(g, (xx, -1, 1))), ng ** 2)],
          "$\\|g\\|^2=\\int_{-1}^{1}(x^2+1)^2dx=\\tfrac25+\\tfrac43+2=%s$, so $\\|g\\|=%s$." % (tex(ng ** 2), tex(ng)), "Exercise Sheet 5, Ex. 3(c)", "src")
    B.mcq(ch, "Function spaces", 3, "In $C[-1,1]$ with $\\langle f,g\\rangle=\\int_{-1}^{1}fg\\,dx$, $\\|x^2\\|=$", "$%s$" % tex(nf), ["$%s$" % tex(z) for z in (ng, sp.integrate(f * f, (xx, -1, 1)), sp.sqrt(sp.integrate(f, (xx, -1, 1))))],
          "$\\|f\\|^2=\\int_{-1}^{1}x^4dx=\\tfrac25$, so $\\|f\\|=%s$." % tex(nf), "Exercise Sheet 5, Ex. 3(b)", "src")
    # ---- Ex. 4 inner product axioms (computed)
    IPS = [("$\\langle u,v\\rangle=u_1v_1+2u_2v_2$", lambda a_, b_: a_[0] * b_[0] + 2 * a_[1] * b_[1], "Ex. 4(a)"),
           ("$\\langle u,v\\rangle=u_1v_1-2u_2v_2$", lambda a_, b_: a_[0] * b_[0] - 2 * a_[1] * b_[1], "Ex. 4(b)"),
           ("$\\langle u,v\\rangle=u_1u_2+v_1v_2$", lambda a_, b_: a_[0] * a_[1] + b_[0] * b_[1], "Ex. 4(c)"),
           ("$\\langle u,v\\rangle=u_1^2v_1^2+u_2^2v_2^2$", lambda a_, b_: a_[0] ** 2 * b_[0] ** 2 + a_[1] ** 2 * b_[1] ** 2, "Ex. 4(d)"),
           ("$\\langle u,v\\rangle=3u_1v_1+u_1v_2+u_2v_1+2u_2v_2$", lambda a_, b_: 3 * a_[0] * b_[0] + a_[0] * b_[1] + a_[1] * b_[0] + 2 * a_[1] * b_[1], "(generated)"),
           ("$\\langle u,v\\rangle=u_1v_1+u_2v_2+u_1v_2+u_2v_1$", lambda a_, b_: a_[0] * b_[0] + a_[1] * b_[1] + a_[0] * b_[1] + a_[1] * b_[0], "(generated)")]
    info = []
    for desc, ipf, src in IPS:
        fl = ip_axioms(ipf, rng); info.append((desc, not fl, fl, src))
    assert [x[1] for x in info] == [True, False, False, False, True, False]
    why = {"symmetry": "it is not symmetric", "additivity": "it is not additive in the first argument", "homogeneity": "it is not homogeneous ($\\langle cu,v\\rangle\\ne c\\langle u,v\\rangle$)", "positivity": "it is not positive definite"}
    yes = [x for x in info if x[1]]; no = [x for x in info if not x[1]]
    for i in range(3):
        corr = yes[i % len(yes)]; wr = rng.sample(no, 3)
        B.mcq(ch, "Inner products", 2, "On $\\mathbb{R}^2$, which of the following defines an inner product?", corr[0], [w[0] for w in wr],
              "An inner product must be symmetric, linear and positive definite. " + " ".join("%s fails: %s." % (w[0], why[sorted(w[2])[0]]) for w in wr), "Exercise Sheet 5, " + corr[3], "src")
    for desc, ok, fl, src in info:
        holds = [k_ for k_ in why if k_ not in fl]
        if not ok and len(fl) == 1 and len(holds) == 3:
            only = sorted(fl)[0]
            B.mcq(ch, "Inner products", 3, "On $\\mathbb{R}^2$, %s is NOT an inner product. Which axiom fails?" % desc, why[only].capitalize(), [why[k_].capitalize() for k_ in holds],
                  "Test the axioms: the others hold, but %s (e.g. positivity needs $\\langle u,u\\rangle>0$ for all $u\\ne0$)." % why[only], "Exercise Sheet 5, " + src, "src")
    # ---- Ex. 5-7
    uu, vv = sp.Matrix([1, 0, -3, 0]), sp.Matrix([2, -2, 1, 1])
    cosv = sp.nsimplify(uu.dot(vv) / (sq(uu.dot(uu)) * sq(vv.dot(vv))))
    B.mcq(ch, "Norm, distance, angle", 2, "Find $\\cos\\theta$ between $u=(1,0,-3,0)$ and $v=(2,-2,1,1)$ in $\\mathbb{R}^4$.", "$%s$" % tex(cosv),
          ["$%s$" % tex(z) for z in (-cosv, sp.nsimplify(uu.dot(vv)), sp.nsimplify(uu.dot(vv) / sq(uu.dot(uu))), sp.Rational(1, 5))],
          "$\\langle u,v\\rangle=2+0-3+0=-1$, $\\|u\\|=\\sqrt{10}$, $\\|v\\|=\\sqrt{10}$, so $\\cos\\theta=-\\tfrac1{10}$ and $\\theta=\\arccos(-0.1)\\approx95.7^\\circ$.", "Exercise Sheet 5, Ex. 5", "src")
    pu, pv = sp.Matrix([1, 2]), sp.Matrix([2, 5])
    pr = (pu.dot(pv) / pv.dot(pv)) * pv
    c, wr = vecs_options(pr, rng, extras=[(pu.dot(pv) / pu.dot(pu)) * pu, (pu.dot(pv) / pv.dot(pv)) * pu, pu.dot(pv) * pv])
    B.mcq(ch, "Projections", 2, "Find $\\operatorname{proj}_{v}u$ for $u=(1,2)$, $v=(2,5)$ (Euclidean product).", c, wr,
          "$\\operatorname{proj}_vu=\\frac{\\langle u,v\\rangle}{\\langle v,v\\rangle}v=\\frac{12}{29}(2,5)=%s$." % vec(list(pr)), "Exercise Sheet 5, Ex. 6", "src")
    B.mcq(ch, "Orthogonal complements", 2, "The set of all vectors of $\\mathbb{R}^4$ orthogonal to $u=(1,-2,2,1)$ is a subspace of dimension …", "3", ["1", "2", "4"],
          "It is the null space of the $1\\times4$ matrix $u^T$: nullity $=4-1=3$.", "Exercise Sheet 5, Ex. 7", "src")
    # ---- Gram-Schmidt (Ex. 8-10)
    def gs(vs):
        us = []
        for w in vs:
            w = sp.Matrix(w)
            for q in us:
                w = w - (w.dot(q) / q.dot(q)) * q
            us.append(sp.simplify(w))
        return us, [sp.simplify(q / sq(q.dot(q))) for q in us]
    GS = [("\\{(1,1),(0,1)\\}", [(1, 1), (0, 1)], "Ex. 8"), ("\\{(1,-2,2),(2,2,1),(2,-1,-2)\\}", [(1, -2, 2), (2, 2, 1), (2, -1, -2)], "Ex. 9"),
          ("\\{(3,4,0,0),(-1,1,0,0),(2,1,0,-1),(0,1,1,0)\\}", [(3, 4, 0, 0), (-1, 1, 0, 0), (2, 1, 0, -1), (0, 1, 1, 0)], "Ex. 10")]
    for tx, bs, src in GS:
        us, es = gs(bs)
        for q in range(len(es)):
            for r_ in range(q):
                assert sp.simplify(es[q].dot(es[r_])) == 0
            assert sp.simplify(es[q].dot(es[q])) == 1
        j = len(bs) - 1
        c, wr = vecs_options(list(es[j]), rng, extras=[list(sp.Matrix(bs[j]) / sq(sp.Matrix(bs[j]).dot(sp.Matrix(bs[j])))), list(us[j]) if us[j] != es[j] else list(-es[j]), list(es[j - 1]) if j > 0 else list(-es[j])])
        B.mcq(ch, "Gram–Schmidt", 3, "Apply Gram–Schmidt (in the given order) to $B=%s$. The last vector $e_%d$ of the orthonormal basis is" % (tx, len(bs)), c, wr,
              "Orthogonalise: $u_%d=v_%d-\\sum_{j<%d}\\operatorname{proj}_{u_j}v_%d=%s$, then divide by its length $\\|u_%d\\|=%s$: $e_%d=%s$." % (
                  len(bs), len(bs), len(bs), len(bs), vec(list(us[j])), len(bs), tex(sq(us[j].dot(us[j]))), len(bs), vec(list(es[j]))), "Exercise Sheet 5, " + src, "src")
    us, es = gs([(1, 1), (0, 1)])
    c, wr = vecs_options(list(es[0]), rng, extras=[[1, 1], [sp.Rational(1, 2), sp.Rational(1, 2)], list(es[1])])
    B.mcq(ch, "Gram–Schmidt", 1, "Gram–Schmidt on $\\{(1,1),(0,1)\\}$: the first orthonormal vector $e_1$ is", c, wr, "$e_1=v_1/\\|v_1\\|=(1,1)/\\sqrt2=%s$." % vec(list(es[0])), "Exercise Sheet 5, Ex. 8", "src")
    # ---- Ex. 11-14 subspaces
    B.mcq(ch, "Orthogonal complements", 2, "For $W=\\{(x,y,z):x+y+z=0\\}\\subset\\mathbb{R}^3$, an orthonormal basis has how many vectors, and $W^\\perp=$", "2 vectors; $W^\\perp=\\operatorname{span}\\{(1,1,1)\\}$", ["3 vectors; $W^\\perp=\\{0\\}$", "2 vectors; $W^\\perp=\\operatorname{span}\\{(1,-1,0)\\}$", "1 vector; $W^\\perp=W$"],
          "$W$ is a plane (dimension 2) with normal vector $(1,1,1)$, so $W^\\perp$ is the line spanned by the normal.", "Exercise Sheet 5, Ex. 11", "src")
    A13 = sp.Matrix([[1, 2], [2, 1], [0, -1]]); wp = A13.T.nullspace()[0]; wp = wp * sp.ilcm(*[sp.fraction(z)[1] for z in wp])
    B.mcq(ch, "Orthogonal complements", 3, "Let $W$ be the span of the columns of $A=%s$. Which vector spans $W^\\perp$?" % mtx(A13), V(list(wp)),
          [V(list(z)) for z in ([wp[1], wp[0], wp[2]], [-wp[0], wp[1], wp[2]], [wp[0], wp[1], -wp[2]])] ,
          "$W^\\perp=\\ker A^T$. Solve $A^Tx=0$: $x=t%s$." % vec(list(wp)), "Exercise Sheet 5, Ex. 13", "src")
    Wb = sp.Matrix([[0, -1, 1], [0, 1, 1]]); b1_, b2_ = Wb[0, :].T, Wb[1, :].T
    assert b1_.dot(b2_) == 0
    xv = sp.Matrix([1, 0, -2]); pr = (xv.dot(b1_) / b1_.dot(b1_)) * b1_ + (xv.dot(b2_) / b2_.dot(b2_)) * b2_
    c, wr = vecs_options(list(pr), rng, extras=[list(xv - pr), list((xv.dot(b1_) / b1_.dot(b1_)) * b1_), list(xv)])
    B.mcq(ch, "Projections", 3, "Project $v=(1,0,-2)$ onto $W=\\operatorname{span}\\{(0,-1,1),(0,1,1)\\}$.", c, wr,
          "The two spanning vectors are orthogonal ($0-1+1=0$), so add the individual projections: $\\operatorname{proj}_Wv=\\frac{\\langle v,b_1\\rangle}{\\langle b_1,b_1\\rangle}b_1+\\frac{\\langle v,b_2\\rangle}{\\langle b_2,b_2\\rangle}b_2=%s$." % vec(list(pr)), "Exercise Sheet 5, Ex. 14", "src")
    # ---- Ex. 15 least squares
    pts = [(-2, 2), (-1, 1), (0, 1), (1, 3)]
    X = sp.Matrix([[1, p[0]] for p in pts]); y = sp.Matrix([p[1] for p in pts])
    beta = (X.T * X).inv() * X.T * y
    assert X.T * (y - X * beta) == sp.zeros(2, 1)
    def line_tex(a0, b0):
        return "$y=%s%s%sx$" % (tex(a0), "+" if b0 > 0 else "-", tex(abs(b0)))
    c = line_tex(beta[0], beta[1])
    wr = [line_tex(beta[0], z) for z in (-beta[1], beta[1] + sp.Rational(1, 2))] + [line_tex(z, beta[1]) for z in (beta[0] + 1, beta[0] - sp.Rational(1, 2))]
    B.mcq(ch, "Least squares", 3, "Find the least-squares line $y=a+bx$ through $(-2,2),(-1,1),(0,1),(1,3)$.", c, wr,
          "Normal equations $X^TXc=X^Ty$ with $X^TX=%s$, $X^Ty=%s$ give $(a,b)=%s$." % (mtx(X.T * X), mtx(X.T * y), vec(list(beta))), "Exercise Sheet 5, Ex. 15", "src")
    # ---- Ex. 16  (the sheet prints x=(-1,4,2), which is NOT in span(B); the intended vector is (-1,4,-2))
    Bv = [sp.Matrix([0, 2, -2]), sp.Matrix([1, 0, -2])]
    printed = sp.Matrix([-1, 4, 2]); xv = sp.Matrix([-1, 4, -2])
    Pm = sp.Matrix.hstack(*Bv)
    assert sp.Matrix.hstack(Pm, printed).rank() == 3 and sp.Matrix.hstack(Pm, xv).rank() == 2
    note("Exercise Sheet 5, Ex. 16", "As printed, $x=(-1,4,2)$ is not in the span of $B=\\{(0,2,-2),(1,0,-2)\\}$ (the third coordinate would have to be $-2$). We use $x=(-1,4,-2)$, which is in the subspace as the exercise intends.")
    co = (Pm.T * Pm).inv() * Pm.T * xv
    assert Pm * co == xv
    us, es = gs(Bv); co2 = [sp.simplify(xv.dot(e)) for e in es]
    assert sp.simplify(sum((co2[i] * es[i] for i in range(2)), sp.zeros(3, 1)) - xv) == sp.zeros(3, 1)
    c, wr = vecs_options(list(co), rng, extras=[list(reversed(list(co))), [co[0], -co[1]], list(co2)])
    B.mcq(ch, "Gram–Schmidt", 3, "$B=\\{(0,2,-2),(1,0,-2)\\}$ is a basis of a subspace containing $x=(-1,4,-2)$. The coordinates $[x]_B$ are", c, wr,
          "Solve $c_1(0,2,-2)+c_2(1,0,-2)=(-1,4,-2)$: the first coordinate gives $c_2=%s$, the second $2c_1=4$ so $c_1=%s$, and the third coordinate $-2c_1-2c_2=%s$ agrees with $x_3$." % (tex(co[1]), tex(co[0]), tex(-2 * co[0] - 2 * co[1])),
          "Exercise Sheet 5, Ex. 16(a) (x corrected, see Sources)", "src")
    c, wr = vecs_options(co2, rng, extras=[list(co), list(reversed(co2)), [co2[0], -co2[1]]])
    B.mcq(ch, "Gram–Schmidt", 3, "For the same $B$, Gram–Schmidt gives an orthonormal basis $B'=\\{e_1,e_2\\}$. The coordinates $[x]_{B'}=(\\langle x,e_1\\rangle,\\langle x,e_2\\rangle)$ of $x=(-1,4,-2)$ are", c, wr,
          "$e_1=%s$, $e_2=%s$; $[x]_{B'}=(\\langle x,e_1\\rangle,\\langle x,e_2\\rangle)=%s$." % (vec(list(es[0])), vec(list(es[1])), vec(co2)), "Exercise Sheet 5, Ex. 16(c) (x corrected, see Sources)", "src")
    # ---- past papers: complement, projection
    PP = [("Final 2024–25 Shift 1, Q4", [(1, -1, 1, 0), (-2, 2, -2, 1)], (1, 2, 1, 1)), ("Final 2023–24 Shift 2, Q4", [(1, 2, 1, 0), (0, 1, 0, 1)], (1, 1, 1, 0)),
          ("Final 2023–24 Shift 1, Q4", [(0, 1, -1, 0), (1, 1, 1, -1)], (1, 1, 1, 1))]
    for src, us_, uvec in PP:
        Um = sp.Matrix([list(z) for z in us_]); ns = Um.nullspace(); assert len(ns) == 2
        gu, ge = gs(ns); uv = sp.Matrix(uvec)
        proj = sp.simplify(sum((uv.dot(e) * e for e in ge), sp.zeros(4, 1)))
        projU = uv - proj
        assert all(sp.simplify(proj.dot(sp.Matrix(z))) == 0 for z in us_)
        B.mcq(ch, "Orthogonal complements", 2, "In $\\mathbb{R}^4$ let $U=\\operatorname{span}\\{%s,%s\\}$. What is $\\dim U^\\perp$?" % (vec(us_[0]), vec(us_[1])), "$2$", ["$1$", "$3$", "$4$"],
              "$\\dim U^\\perp=4-\\dim U=4-2=2$ ($U^\\perp=\\ker$ of the matrix whose rows are the spanning vectors).", src + "(a)", "src")
        c, wr = vecs_options(list(proj), rng, extras=[list(projU), list(-proj), list(uv)])
        B.mcq(ch, "Projections", 3, "Let $U=\\operatorname{span}\\{%s,%s\\}$ in $\\mathbb{R}^4$ and $u=%s$. The orthogonal projection of $u$ onto $U^\\perp$ is" % (vec(us_[0]), vec(us_[1]), vec(uvec)), c, wr,
              "$U^\\perp=\\ker%s$ has the orthonormal basis $e_1=%s$, $e_2=%s$ (Gram–Schmidt). Then $\\operatorname{proj}_{U^\\perp}u=\\sum\\langle u,e_i\\rangle e_i=%s$ and $u-\\operatorname{proj}_{U^\\perp}u=\\operatorname{proj}_Uu=%s$." % (
                  mtx(Um), vec(list(ge[0])), vec(list(ge[1])), vec(list(proj)), vec(list(projU))), src + "(b)", "src")
    # conceptual
    B.mcq(ch, "Inner products", 1, "Cauchy–Schwarz inequality: for all $u,v$ in an inner product space,", "$|\\langle u,v\\rangle|\\le\\|u\\|\\,\\|v\\|$", ["$|\\langle u,v\\rangle|\\ge\\|u\\|\\,\\|v\\|$", "$\\|u+v\\|=\\|u\\|+\\|v\\|$", "$\\langle u,v\\rangle\\le\\|u-v\\|$"],
          "It guarantees $|\\cos\\theta|\\le1$, so the angle formula is well defined.", "Lecture 5", "concept")
    B.mcq(ch, "Inner products", 1, "Vectors $u,v$ are orthogonal iff …", "$\\langle u,v\\rangle=0$", ["$\\|u\\|=\\|v\\|$", "$u=cv$ for some $c$", "$\\langle u,v\\rangle=1$"], "Orthogonality is defined by a zero inner product.", "Lecture 5", "concept")
    B.mcq(ch, "Orthogonal complements", 1, "For a subspace $W\\subseteq\\mathbb{R}^n$: $\\dim W+\\dim W^\\perp=$", "$n$", ["$n-1$", "$2n$", "$\\dim W^\\perp$ only"], "$\\mathbb{R}^n=W\\oplus W^\\perp$.", "Lecture 5", "concept")
    B.mcq(ch, "Projections", 1, "The orthogonal projection of $u$ onto a subspace $W$ is the vector of $W$ that …", "is closest to $u$", ["is longest", "is parallel to $u$ always", "has the same norm as $u$"], "$\\operatorname{proj}_Wu$ minimises $\\|u-w\\|$ over $w\\in W$.", "Lecture 5", "concept")
    for _ in range(4):
        a_ = sp.Matrix([rng.randint(-3, 3) for _ in range(3)]); b_ = sp.Matrix([rng.randint(-3, 3) for _ in range(3)])
        if b_.dot(b_) == 0 or a_.dot(a_) == 0 or a_.dot(b_) == 0:
            continue
        pr = (a_.dot(b_) / b_.dot(b_)) * b_
        c, wr = vecs_options(list(pr), rng, extras=[list((a_.dot(b_) / a_.dot(a_)) * a_), list(a_ - pr), list(a_.dot(b_) * b_)])
        B.mcq(ch, "Projections", 2, "Compute $\\operatorname{proj}_{v}u$ for $u=%s$, $v=%s$ (dot product)." % (vec(list(a_)), vec(list(b_))), c, wr,
              "$\\operatorname{proj}_vu=\\frac{u\\cdot v}{v\\cdot v}v=\\frac{%s}{%s}v=%s$." % (tex(a_.dot(b_)), tex(b_.dot(b_)), vec(list(pr))), "Generated (projection)", "gen")
