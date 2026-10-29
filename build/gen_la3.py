# -*- coding: utf-8 -*-
"""LA chapters 6-7: linear transformations, eigenvalues. Every answer is computed and cross-checked."""
import random
import sympy as sp
from qlib import tex, vec, uniq_by_text, R, note
from la_common import *
from la_steps import mtx
from gen_la1 import mt, numopts
from gen_la2 import V, vecs_options

xs3 = sp.symbols("x y z w")
lam = sp.Symbol("lambda")

def T_matrix(f, n):
    """Standard matrix of f: R^n -> R^m given as python function on a sympy Matrix; asserts linearity on random samples."""
    cols = []
    for i in range(n):
        e = sp.zeros(n, 1); e[i] = 1
        cols.append(sp.Matrix(f(e)))
    A = sp.Matrix.hstack(*cols)
    rnd = random.Random(7)
    for _ in range(25):
        a_ = sp.Matrix([rnd.randint(-4, 4) for _ in range(n)]); b_ = sp.Matrix([rnd.randint(-4, 4) for _ in range(n)]); c_ = rnd.choice([-2, 3, 5])
        assert sp.Matrix(f(a_ + b_)) == sp.Matrix(f(a_)) + sp.Matrix(f(b_)) and sp.Matrix(f(c_ * a_)) == c_ * sp.Matrix(f(a_)), "not linear"
        assert sp.Matrix(f(a_)) == A * a_
    return A

def is_linear(f, n):
    rnd = random.Random(11)
    for _ in range(60):
        a_ = sp.Matrix([rnd.randint(-4, 4) for _ in range(n)]); b_ = sp.Matrix([rnd.randint(-4, 4) for _ in range(n)]); c_ = rnd.choice([-2, -1, 2, 3])
        if sp.Matrix(f(a_ + b_)) != sp.Matrix(f(a_)) + sp.Matrix(f(b_)) or sp.Matrix(f(c_ * a_)) != c_ * sp.Matrix(f(a_)):
            return False
    return True

def span_text(vs):
    return ", ".join(V(list(v_)) for v_ in vs) if vs else "$\\{0\\}$"

# ============================================================================== CHAPTER 6
def ch6(B):
    ch = "c6"; rng = B.rng
    # ---- Ex. 1 image / preimage
    f1a = lambda v: [v[0], v[0] + 2 * v[1]]
    A1a = T_matrix(f1a, 2)
    im = sp.Matrix(f1a(sp.Matrix([2, -3])))
    c, wr = vecs_options(list(im), rng, extras=[[2, -3], [2, 4], [-2, 4]])
    B.mcq(ch, "Image and preimage", 1, "For $T(v_1,v_2)=(v_1,\\ v_1+2v_2)$, the image of $v=(2,-3)$ is", c, wr, "$T(2,-3)=(2,\\ 2+2(-3))=%s$." % vec(list(im)), "Exercise Sheet 6, Ex. 1(a)", "src")
    pre = A1a.LUsolve(sp.Matrix([4, 12])); assert A1a * pre == sp.Matrix([4, 12])
    c, wr = vecs_options(list(pre), rng, extras=[[4, 12], [4, 8], [12, 4]])
    B.mcq(ch, "Image and preimage", 2, "For $T(v_1,v_2)=(v_1,\\ v_1+2v_2)$, the preimage of $w=(4,12)$ is", c, wr, "Solve $v_1=4$, $v_1+2v_2=12$: $v_2=4$, so the preimage is $%s$ (unique since $T$ is invertible)." % vec(list(pre)), "Exercise Sheet 6, Ex. 1(a)", "src")
    f1b = lambda v: [0, v[0] + v[1], v[1] + v[2]]
    A1b = T_matrix(f1b, 3)
    im = sp.Matrix(f1b(sp.Matrix([-3, 2, 5])))
    c, wr = vecs_options(list(im), rng, extras=[[-3, 2, 5], [0, 1, 7], [0, -1, -7]])
    B.mcq(ch, "Image and preimage", 1, "For $T(v_1,v_2,v_3)=(0,\\ v_1+v_2,\\ v_2+v_3)$, the image of $v=(-3,2,5)$ is", c, wr, "$T(-3,2,5)=(0,\\ -3+2,\\ 2+5)=%s$." % vec(list(im)), "Exercise Sheet 6, Ex. 1(b)", "src")
    wv = sp.Matrix([0, 2, 5]); good = sp.Matrix([0, 2, 3]); assert A1b * good == wv
    bad = []
    for cand in ([0, 2, 5], [2, 0, 5], [1, 1, 4], [0, 3, 2], [1, 2, 3]):
        if A1b * sp.Matrix(cand) != wv: bad.append(cand)
    B.mcq(ch, "Image and preimage", 3, "For $T(v_1,v_2,v_3)=(0,\\ v_1+v_2,\\ v_2+v_3)$, which vector belongs to the preimage of $w=(0,2,5)$?", V(list(good)), [V(z) for z in bad[:3]],
          "Need $v_1+v_2=2$ and $v_2+v_3=5$: $v=(t,\\ 2-t,\\ 3+t)$ — a whole line of preimages ($T$ is not one-to-one). $t=0$ gives $(0,2,3)$.", "Exercise Sheet 6, Ex. 1(b)", "src")
    # ---- Ex. 2 linear or not
    CASES = [
        ("$T(x_1,x_2)=(x_1+2x_2,\\ -x_1-x_2)$", lambda v: [v[0] + 2 * v[1], -v[0] - v[1]], 2, "Ex. 2(a)"),
        ("$T(x_1,x_2)=(x_1+3,\\ x_2)$", lambda v: [v[0] + 3, v[1]], 2, "Ex. 2(b)"),
        ("$T(x,y)=(x+y,\\ 2y)$", lambda v: [v[0] + v[1], 2 * v[1]], 2, "Ex. 2(c)"),
        ("$T(x,y)=(|x|,\\ |y|)$", lambda v: [sp.Abs(v[0]), sp.Abs(v[1])], 2, "Ex. 2(d)"),
        ("$T(x,y,z)=(z,\\ y,\\ x)$", lambda v: [v[2], v[1], v[0]], 3, "Ex. 2(e)"),
        ("$T(x,y)=(xy,\\ x)$", lambda v: [v[0] * v[1], v[0]], 2, "(generated)"),
        ("$T(x,y)=(2x-y,\\ 0)$", lambda v: [2 * v[0] - v[1], 0], 2, "(generated)"),
        ("$T(x,y)=(x^2,\\ y)$", lambda v: [v[0] ** 2, v[1]], 2, "(generated)"),
    ]
    lin = [(d, f, n, src) for d, f, n, src in CASES if is_linear(f, n)]
    nonlin = [(d, f, n, src) for d, f, n, src in CASES if not is_linear(f, n)]
    WHY = {  # reason a map is not linear, each verified by the numeric check right below
        CASES[1][0]: ("$T(0,0)=(3,0)\\neq(0,0)$", CASES[1][1], [0, 0], None),
        CASES[3][0]: ("$T(-1,0)=(1,0)\\neq-T(1,0)=(-1,0)$", CASES[3][1], [-1, 0], None),
        CASES[5][0]: ("$T(2,2)=(4,2)\\neq2\\,T(1,1)=(2,2)$", CASES[5][1], [2, 2], [1, 1]),
        CASES[7][0]: ("$T(2,0)=(4,0)\\neq2\\,T(1,0)=(2,0)$", CASES[7][1], [2, 0], [1, 0]),
    }
    assert sp.Matrix(CASES[1][1](sp.Matrix([0, 0]))) == sp.Matrix([3, 0])
    assert sp.Matrix(CASES[3][1](sp.Matrix([-1, 0]))) == sp.Matrix([1, 0]) and sp.Matrix(CASES[3][1](sp.Matrix([1, 0]))) == sp.Matrix([1, 0])
    assert sp.Matrix(CASES[5][1](sp.Matrix([2, 2]))) == sp.Matrix([4, 2]) and 2 * sp.Matrix(CASES[5][1](sp.Matrix([1, 1]))) == sp.Matrix([2, 2])
    assert sp.Matrix(CASES[7][1](sp.Matrix([2, 0]))) == sp.Matrix([4, 0]) and 2 * sp.Matrix(CASES[7][1](sp.Matrix([1, 0]))) == sp.Matrix([2, 0])
    assert [d for d, *_ in lin] == [CASES[i][0] for i in (0, 2, 4, 6)] and len(nonlin) == 4
    for i in range(3):
        corr = lin[i]; wr = rng.sample(nonlin, 3)
        B.mcq(ch, "Linear or not", 2, "Which of the following maps is a linear transformation?", corr[0], [w[0] for w in wr],
              "A linear map satisfies $T(u+v)=T(u)+T(v)$ and $T(cu)=cT(u)$ (so $T(0)=0$). The others fail: " + "; ".join("%s: %s" % (w[0], WHY[w[0]][0]) for w in wr) + ".", "Exercise Sheet 6, " + corr[3], "src" if corr[3].startswith("Ex") else "gen")
    for i in range(3):
        corr = nonlin[i]; wr = rng.sample(lin, 3)
        B.mcq(ch, "Linear or not", 2, "Which of the following maps is NOT a linear transformation?", corr[0], [w[0] for w in wr],
              "It is not linear: %s. The other three maps are of the form $T(v)=Av$." % WHY[corr[0]][0], "Exercise Sheet 6, " + corr[3], "src" if corr[3].startswith("Ex") else "gen")
    for d, f, n, src in lin[:3]:
        A = T_matrix(f, n)
        B.mcq(ch, "Standard matrix", 1, "Find the standard matrix of %s." % d, mt(A), [mt(A.T), mt(perturb(A, rng)), mt(-A), mt(perturb(A, rng)), mt(sp.eye(A.rows))],
              "The columns are $T(e_1),\\dots,T(e_n)$: $[T]=%s$." % mtx(A), "Exercise Sheet 6, " + src, "src" if src.startswith("Ex") else "gen")
    # ---- Ex. 3
    T10 = sp.Matrix([1, 1]) / 2; T01 = sp.Matrix([1, 1]) / 1
    t13 = T10 + 3 * T01
    c, wr = vecs_options(list(t13), rng, extras=[list(T10 + T01), list(3 * sp.Matrix([1, 1]) + sp.Matrix([1, 1])), [3, 3]])
    B.mcq(ch, "Image and preimage", 2, "A linear map $T:\\mathbb{R}^2\\to\\mathbb{R}^2$ has $T(2,0)=(1,1)$ and $T(0,3)=(3,3)$. Find $T(1,3)$.", c, wr,
          "$T(1,0)=\\tfrac12T(2,0)=(\\tfrac12,\\tfrac12)$ and $T(0,1)=\\tfrac13T(0,3)=(1,1)$, so $T(1,3)=T(1,0)+3T(0,1)=%s$." % vec(list(t13)), "Exercise Sheet 6, Ex. 3", "src")
    # ---- Ex. 4-7 matrix maps
    MM = [("Ex. 4", sp.Matrix([[0, 1, 2], [-2, 0, 0]]), (6, 1, 1), (3, 5)), ("Ex. 5", sp.Matrix([[2, 1], [0, 1]]), (8, 4), (5, 2)),
          ("Ex. 6", sp.Matrix([[2, -1]]), (1, 2), (-1,)), ("Ex. 7", sp.Matrix([[1, 0], [0, -1], [1, 2]]), (1, 2), (2, -5, 12))]
    for src, A, v, w in MM:
        v = sp.Matrix(v); w = sp.Matrix(w)
        n, m_ = A.cols, A.rows
        B.mcq(ch, "Image and preimage", 1, "$T(v)=Av$ with $A=%s$. Which maps $\\mathbb{R}^n\\to\\mathbb{R}^m$ are we in?" % mtx(A), "$\\mathbb{R}^%d\\to\\mathbb{R}^%d$" % (n, m_),
              ["$\\mathbb{R}^%d\\to\\mathbb{R}^%d$" % (m_, n), "$\\mathbb{R}^%d\\to\\mathbb{R}^%d$" % (n, n), "$\\mathbb{R}^%d\\to\\mathbb{R}^%d$" % (m_, m_)] if m_ != n else ["$\\mathbb{R}^%d\\to\\mathbb{R}^%d$" % (n + 1, n), "$\\mathbb{R}^%d\\to\\mathbb{R}^%d$" % (n, n + 1), "$\\mathbb{R}^%d\\to\\mathbb{R}^%d$" % (n + 1, n + 1)],
              "$A$ is $%d\\times%d$, so $T$ takes vectors with $%d$ coordinates to vectors with $%d$ coordinates." % (m_, n, n, m_), "Exercise Sheet 6, " + src, "src")
        im = A * v
        c, wr = vecs_options(list(im), rng, extras=[list(v), list(A.T * v) if A.T.cols == len(v) else list(-im)])
        B.mcq(ch, "Image and preimage", 1, "$T(v)=Av$ with $A=%s$. Find $T(v)$ for $v=%s$." % (mtx(A), vec(list(v))), c, wr, "$T(v)=Av=%s$." % vec(list(im)), "Exercise Sheet 6, " + src, "src")
        kind, sol, free = solve_sys(A, w)
        if kind == "unique":
            pre = list(sol)
            c, wr = vecs_options(pre, rng, extras=[list(reversed(pre))])
            B.mcq(ch, "Image and preimage", 2, "$T(v)=Av$ with $A=%s$. Find the preimage of $w=%s$." % (mtx(A), vec(list(w))), c, wr, "Solve $Av=w$: the unique solution is $v=%s$." % vec(pre), "Exercise Sheet 6, " + src, "src")
        else:
            part = particular(sol, free, rng)
            bad = near_vectors(part, A, w, rng, 5)
            if len(bad) >= 3:
                B.mcq(ch, "Image and preimage", 2, "$T(v)=Av$ with $A=%s$. Which vector is a preimage of $w=%s$?" % (mtx(A), vec(list(w))), V(part), [V(z) for z in bad[:3]],
                      "Solve $Av=w$: it has %d free parameter(s), so the preimage is a whole line/plane; $%s$ is one preimage ($A\\cdot%s=w$)." % (len(free), vec(part), vec(part)), "Exercise Sheet 6, " + src, "src")
    # ---- Ex. 8-15 kernel and range
    KR = [("T(x,y,z)=(x,\\ y+2z,\\ z)", sp.Matrix([[1, 0, 0], [0, 1, 2], [0, 0, 1]]), "Ex. 8"), ("T(x,y,z)=(x+2y,\\ y+2z,\\ z+2x)", sp.Matrix([[1, 2, 0], [0, 1, 2], [2, 0, 1]]), "Ex. 9"),
          ("T(x,y)=(x+2y,\\ -2x-4y)", sp.Matrix([[1, 2], [-2, -4]]), "Ex. 10"), ("T(x,y,z,w)=(4x+5y+5z+2w,\\ -2x+2y-w,\\ 8y+4z)", sp.Matrix([[4, 5, 5, 2], [-2, 2, 0, -1], [0, 8, 4, 0]]), "Ex. 11"),
          ("T(v)=Av,\\ A=\\begin{bmatrix}2&1&3\\\\1&1&0\\\\0&1&-3\\end{bmatrix}", sp.Matrix([[2, 1, 3], [1, 1, 0], [0, 1, -3]]), "Ex. 12"),
          ("T(v)=Av,\\ A=\\begin{bmatrix}1&-1&2\\\\0&1&2\\end{bmatrix}", sp.Matrix([[1, -1, 2], [0, 1, 2]]), "Ex. 13"),
          ("T(v)=Av,\\ A=\\begin{bmatrix}1&2\\\\-1&-2\\\\1&1\\end{bmatrix}", sp.Matrix([[1, 2], [-1, -2], [1, 1]]), "Ex. 14"),
          ("T(v)=Av,\\ A=\\begin{bmatrix}1&2&-1&4\\\\3&1&2&-1\\\\-4&-3&-1&-3\\\\-1&-2&1&1\\end{bmatrix}", sp.Matrix([[1, 2, -1, 4], [3, 1, 2, -1], [-4, -3, -1, -3], [-1, -2, 1, 1]]), "Ex. 15")]
    # make sure the formula-defined maps equal their matrices
    assert T_matrix(lambda v: [v[0], v[1] + 2 * v[2], v[2]], 3) == KR[0][1]
    assert T_matrix(lambda v: [v[0] + 2 * v[1], v[1] + 2 * v[2], v[2] + 2 * v[0]], 3) == KR[1][1]
    assert T_matrix(lambda v: [v[0] + 2 * v[1], -2 * v[0] - 4 * v[1]], 2) == KR[2][1]
    assert T_matrix(lambda v: [4 * v[0] + 5 * v[1] + 5 * v[2] + 2 * v[3], -2 * v[0] + 2 * v[1] - v[3], 8 * v[1] + 4 * v[2]], 4) == KR[3][1]
    for desc, A, src in KR:
        rk = A.rank(); nul = A.cols - rk; ns = A.nullspace(); cs = A.columnspace()
        B.mcq(ch, "Kernel, range, rank–nullity", 2, "For $%s$, what are $\\operatorname{rank}T$ and $\\operatorname{nullity}T$?" % desc if desc.startswith("T(v)") else "For $%s$ (matrix $%s$), what are $\\operatorname{rank}T$ and $\\operatorname{nullity}T$?" % (desc, mtx(A)),
              "rank $%d$, nullity $%d$" % (rk, nul),
              [x_ for x_ in uniq_by_text(["rank $%d$, nullity $%d$" % (r2, A.cols - r2) for r2 in range(0, min(A.rows, A.cols) + 1)] +
                                          ["rank $%d$, nullity $%d$" % (nul, rk), "rank $%d$, nullity $%d$" % (rk, rk), "rank $%d$, nullity $%d$" % (rk + 1, nul), "rank $%d$, nullity $%d$" % (rk, nul + 1)])
               if x_ != "rank $%d$, nullity $%d$" % (rk, nul)],
              "Row-reduce $A$: rank $=%d$ (pivot columns), nullity $=n-\\operatorname{rank}=%d-%d=%d$." % (rk, A.cols, rk, nul), "Exercise Sheet 6, " + src, "src")
        if ns:
            vv = ns[0] * sp.ilcm(*[sp.fraction(z)[1] for z in ns[0]])
            bad = []
            for cand in ([1] * A.cols, [0] * (A.cols - 1) + [1], list(reversed(list(vv))), [int(z) + 1 for z in vv]):
                if A * sp.Matrix(cand) != sp.zeros(A.rows, 1) and cand not in bad:
                    bad.append(cand)
            if len(bad) >= 3:
                B.mcq(ch, "Kernel, range, rank–nullity", 2, "For $A=%s$, which vector lies in $\\ker T$?" % mtx(A), V(list(vv)), [V(z) for z in bad[:3]],
                      "Solve $Ax=0$: basis of the kernel $%s$. Check $A\\,%s=0$." % (span_text(ns), vec(list(vv))), "Exercise Sheet 6, " + src, "src")
        else:
            B.mcq(ch, "Kernel, range, rank–nullity", 2, "For $A=%s$, what is $\\ker T$?" % mtx(A), "$\\ker T=\\{0\\}$ ($T$ is one-to-one)",
                  ["$\\ker T$ is a line", "$\\ker T$ is a plane", "$\\ker T=\\mathbb{R}^%d$" % A.cols], "No free variables after row reduction (rank $=n=%d$), so only $x=0$ solves $Ax=0$." % A.cols, "Exercise Sheet 6, " + src, "src")
        inj = nul == 0; onto = rk == A.rows
        txt = lambda i_, o_: "%s, %s" % ("one-to-one" if i_ else "not one-to-one", "onto" if o_ else "not onto")
        opts = [txt(i_, o_) for i_ in (True, False) for o_ in (True, False) if (i_, o_) != (inj, onto)]
        B.mcq(ch, "One-to-one and onto", 2, "For $A=%s$, the map $T(v)=Av$ is" % mtx(A), txt(inj, onto), opts,
              "One-to-one iff $\\ker T=\\{0\\}$ (nullity $%d$); onto iff $\\operatorname{rank}=\\dim(\\text{codomain})=%d$ (rank $%d$)." % (nul, A.rows, rk), "Exercise Sheet 6, " + src, "src")
    # ---- Ex. 16-18 rank-nullity
    B.mcq(ch, "Kernel, range, rank–nullity", 1, "$T:\\mathbb{R}^5\\to\\mathbb{R}^3$ has $\\operatorname{nullity}(T)=2$. Then $\\operatorname{rank}(T)=$", "$3$", ["$2$", "$5$", "$7$"], "Rank–nullity: $\\operatorname{rank}+\\operatorname{nullity}=\\dim(\\text{domain})=5$, so $\\operatorname{rank}=3$.", "Exercise Sheet 6, Ex. 16", "src")
    B.mcq(ch, "Kernel, range, rank–nullity", 1, "$T:M_{2\\times2}\\to M_{2\\times2}$ has $\\operatorname{rank}(T)=3$. Then $\\operatorname{nullity}(T)=$", "$1$", ["$0$", "$3$", "$4$"], "$\\dim M_{2\\times2}=4$, so nullity $=4-3=1$.", "Exercise Sheet 6, Ex. 17", "src")
    B.mcq(ch, "Kernel, range, rank–nullity", 2, "$T:P_5\\to P_3$ has $\\operatorname{nullity}(T)=4$. Then $\\operatorname{rank}(T)=$", "$2$", ["$1$", "$0$", "$4$"], "$\\dim P_5=6$ (basis $1,x,\\dots,x^5$), so rank $=6-4=2$ (and $\\le\\dim P_3=4$).", "Exercise Sheet 6, Ex. 18", "src")
    # ---- Ex. 19-22 invertibility
    INV = [("T(x,y)=(2x,\\ y)", lambda v: [2 * v[0], v[1]], 2, "Ex. 19"), ("T(x,y)=(x+y,\\ 2x+2y)", lambda v: [v[0] + v[1], 2 * v[0] + 2 * v[1]], 2, "Ex. 20"),
           ("T(x,y,z)=(x,\\ x+y,\\ x+y+z)", lambda v: [v[0], v[0] + v[1], v[0] + v[1] + v[2]], 3, "Ex. 22")]
    for desc, f, n, src in INV:
        A = T_matrix(f, n)
        if A.det() != 0:
            B.mcq(ch, "Invertible maps", 2, "Is $%s$ invertible? If so, what is $A^{-1}$?" % desc, "Yes: $A^{-1}=%s$" % mtx(A.inv()),
                  ["Yes: $A^{-1}=%s$" % mtx(A.T), "Yes: $A^{-1}=%s$" % mtx(perturb(A.inv(), rng)), "No: $\\det A=0$"],
                  "$A=%s$ with $\\det A=%s\\neq0$, so $T$ is invertible and $A^{-1}=%s$ (row-reduce $[A\\mid I]$)." % (mtx(A), tex(A.det()), mtx(A.inv())), "Exercise Sheet 6, " + src, "src")
        else:
            B.mcq(ch, "Invertible maps", 2, "Is $%s$ invertible?" % desc, "No: $\\det A=0$ (the rows are dependent)", ["Yes: $A^{-1}=%s$" % mtx(sp.eye(n)), "Yes, every linear map $\\mathbb{R}^2\\to\\mathbb{R}^2$ is", "Yes: $A^{-1}=A^{T}$"],
                  "$A=%s$ has $\\det A=0$, so $T$ is not one-to-one and has no inverse." % mtx(A), "Exercise Sheet 6, " + src, "src")
    B.mcq(ch, "Invertible maps", 1, "Can $T(x,y,z)=(x+y+z,\\ z)$, a map $\\mathbb{R}^3\\to\\mathbb{R}^2$, have an inverse?", "No: a non-square matrix cannot be invertible (here $\\ker T\\neq\\{0\\}$)",
          ["Yes: $T^{-1}$ exists since $T$ is onto", "Yes: $T^{-1}=T^{T}$", "Only if $\\operatorname{rank}T=3$"], "$\\dim\\mathbb{R}^3\\neq\\dim\\mathbb{R}^2$: by rank–nullity, $\\operatorname{nullity}\\ge1$, so $T$ is not one-to-one.", "Exercise Sheet 6, Ex. 21", "src")
    # ---- Ex. 25 composition
    T1 = lambda v: [v[0], v[0] + v[1], v[1]]; T2 = lambda v: [0, v[1]]
    A1 = T_matrix(T1, 2); A2 = T_matrix(T2, 3)
    C12 = A1 * A2; C21 = A2 * A1
    assert C12.shape == (3, 3) and C21.shape == (2, 2)
    assert C12 == T_matrix(lambda v: T1(sp.Matrix(T2(sp.Matrix(v)))), 3)
    B.mcq(ch, "Composition", 3, "$T_1(x,y)=(x,\\ x+y,\\ y)$ and $T_2(x,y,z)=(0,\\ y)$. The standard matrix of $T_1\\circ T_2$ is", mt(C12), [mt(C21), mt(C12.T), mt(perturb(C12, rng)), mt(-C12)],
          "$[T_1\\circ T_2]=[T_1][T_2]=%s%s=%s$ (a $3\\times3$ matrix: $\\mathbb{R}^3\\to\\mathbb{R}^2\\to\\mathbb{R}^3$)." % (mtx(A1), mtx(A2), mtx(C12)), "Exercise Sheet 6, Ex. 25", "src")
    B.mcq(ch, "Composition", 3, "$T_1(x,y)=(x,\\ x+y,\\ y)$ and $T_2(x,y,z)=(0,\\ y)$. The standard matrix of $T_2\\circ T_1$ is", mt(C21), [mt(C12), mt(C21.T), mt(perturb(C21, rng))],
          "$[T_2\\circ T_1]=[T_2][T_1]=%s%s=%s$ (a $2\\times2$ matrix: $\\mathbb{R}^2\\to\\mathbb{R}^3\\to\\mathbb{R}^2$)." % (mtx(A2), mtx(A1), mtx(C21)), "Exercise Sheet 6, Ex. 25", "src")
    # ---- Ex. 26-27 matrices relative to bases
    A26 = T_matrix(lambda v: [-v[0], v[1], v[0] + v[1]], 2)
    PB = sp.Matrix.hstack(sp.Matrix([1, 1]), sp.Matrix([1, -1])); PBp = sp.Matrix.hstack(sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1]), sp.Matrix([1, 0, 0]))
    T_B = PBp.inv() * A26 * PB
    vB = PB.inv() * sp.Matrix([0, 1]); Tv = A26 * sp.Matrix([0, 1])
    assert PBp * (T_B * vB) == Tv
    B.mcq(ch, "Matrix relative to bases", 3, "$T(x,y)=(-x,\\ y,\\ x+y)$ with $B=\\{(1,1),(1,-1)\\}$ and $B'=\\{(0,1,0),(0,0,1),(1,0,0)\\}$. The matrix $[T]_{B,B'}$ is", mt(T_B), [mt(perturb(T_B, rng)), mt(perturb(T_B, rng)), mt(A26), mt(-T_B)],
          "$[T]_{B,B'}=P_{B'}^{-1}AP_B$ with $A=%s$, $P_B=%s$, $P_{B'}=%s$: $[T]_{B,B'}=%s$. Check on $v=(0,1)$: $[v]_B=%s$, $[Tv]_{B'}=%s$, i.e. $Tv=%s$." % (mtx(A26), mtx(PB), mtx(PBp), mtx(T_B), vec(list(vB)), vec(list(T_B * vB)), vec(list(Tv))), "Exercise Sheet 6, Ex. 26", "src")
    A27 = T_matrix(lambda v: [v[0] - 3 * v[1], v[1] - v[0]], 2); P27 = sp.Matrix.hstack(sp.Matrix([1, -1]), sp.Matrix([1, 1]))
    A27p = P27.inv() * A27 * P27
    B.mcq(ch, "Matrix relative to bases", 3, "$T(x,y)=(x-3y,\\ y-x)$ and $B'=\\{(1,-1),(1,1)\\}$. The matrix $A'$ of $T$ relative to $B'$ is", mt(A27p), [mt(A27p.T), mt(A27), mt(perturb(A27p, rng))],
          "$A'=P^{-1}AP$ with $A=%s$, $P=%s$: $A'=%s$." % (mtx(A27), mtx(P27), mtx(A27p)), "Exercise Sheet 6, Ex. 27", "src")
    # ---- past papers
    A3 = T_matrix(lambda v: [v[0] - 2 * v[1] + v[2], 2 * v[0] - 3 * v[1] + 5 * v[2], 3 * v[0] - 2 * v[1] + v[2]], 3)
    P = sp.Matrix.hstack(sp.Matrix([1, 2, 0]), sp.Matrix([1, 0, -1]), sp.Matrix([-2, 1, 2]))
    Tb = P.inv() * A3 * P
    i_, j_ = 1, 2
    c, wr = numopts(Tb[i_, j_], rng, extra=[Tb[j_, i_], -Tb[i_, j_], (P * A3 * P.inv())[i_, j_]])
    B.mcq(ch, "Matrix relative to bases", 3, "Exam: $T(x_1,x_2,x_3)=(x_1-2x_2+x_3,\\ 2x_1-3x_2+5x_3,\\ 3x_1-2x_2+x_3)$ and $B=\\{(1,2,0),(1,0,-1),(-2,1,2)\\}$. The entry in row 2, column 3 of $[T]_B=P^{-1}AP$ is", c, wr,
          "$A=%s$, $P=%s$, so $[T]_B=P^{-1}AP=%s$; its $(2,3)$ entry is $%s$." % (mtx(A3), mtx(P), mtx(Tb), tex(Tb[i_, j_])), "Final 2024–25 Shift 1, Q3(c)", "src")
    A32 = T_matrix(lambda v: [v[0] - v[1] + v[2], 6 * v[0] - 2 * v[1], 3 * v[0] - 4 * v[1] + v[2], 5 * v[1] - 4 * v[2]], 3)
    B.mcq(ch, "One-to-one and onto", 3, "Exam: $T:\\mathbb{R}^3\\to\\mathbb{R}^4$, $T(x_1,x_2,x_3)=(x_1-x_2+x_3,\\ 6x_1-2x_2,\\ 3x_1-4x_2+x_3,\\ 5x_2-4x_3)$. Is $T$ one-to-one? onto?",
          "one-to-one, not onto" if A32.rank() == 3 else "not one-to-one, not onto", ["one-to-one and onto", "not one-to-one, onto", "not one-to-one, not onto" if A32.rank() == 3 else "one-to-one, not onto"],
          "$A=%s$ has rank $%d$: nullity $3-%d=%d$, so $\\ker T$ %s; the range has dimension $%d<4$, so $T$ is not onto." % (mtx(A32), A32.rank(), A32.rank(), 3 - A32.rank(), "is $\\{0\\}$ (one-to-one)" if A32.rank() == 3 else "is non-trivial", A32.rank()), "Final 2024–25 Shift 2, Q3(c)", "src")
    A33 = T_matrix(lambda v: [3 * v[0] - 4 * v[1], 16 * v[0] - 23 * v[1], 7 * v[0] - 9 * v[1]], 2)
    B.mcq(ch, "One-to-one and onto", 3, "Exam: $T:\\mathbb{R}^2\\to\\mathbb{R}^3$, $T(x_1,x_2)=(3x_1-4x_2,\\ 16x_1-23x_2,\\ 7x_1-9x_2)$. Which statement is true?",
          "$T$ is one-to-one (kernel $\\{0\\}$) but not onto" if A33.rank() == 2 else "other", ["$T$ is onto but not one-to-one", "$T$ is both one-to-one and onto", "$T$ is neither one-to-one nor onto"],
          "$A=%s$ has rank $2$ (the two columns are independent), so $\\ker T=\\{0\\}$ and nullity $=0$; range has dimension $2<3$, so not onto." % mtx(A33), "Final 2023–24 Shift 1, Q3", "src")
    A34 = T_matrix(lambda v: [v[0] + v[1] + v[2] - v[3], 2 * v[0] + 3 * v[1] + v[2] - 2 * v[3]], 4)
    ns = A34.nullspace()
    B.mcq(ch, "Kernel, range, rank–nullity", 3, "Exam (2019–20): $T:\\mathbb{R}^4\\to\\mathbb{R}^2$, $T(x,y,z,w)=(x+y+z-w,\\ 2x+3y+z-2w)$. What is $\\dim\\ker T$?", "$%d$" % len(ns), ["$%d$" % z for z in sorted({0, 1, 2, 3, 4} - {len(ns)})][:3],
          "$[T]=%s$ has rank $2$ (onto $\\mathbb{R}^2$), so nullity $=4-2=%d$; a basis of the kernel is %s." % (mtx(A34), len(ns), span_text(ns)), "Final 2019–20, Q3(b)", "src")
    A35 = T_matrix(lambda v: [v[0] + v[1], v[1] + v[2], v[0] + v[2]], 3)
    B.mcq(ch, "Invertible maps", 3, "Exam: $T(x,y,z)=(x+y,\\ y+z,\\ x+z)$. Which is the matrix of $T^{-1}$?", mt(A35.inv()), [mt(A35), mt(A35.T), mt(perturb(A35.inv(), rng))],
          "$A=%s$, $\\det A=%s\\neq0$; row-reducing $[A\\mid I]$ gives $A^{-1}=%s$." % (mtx(A35), tex(A35.det()), mtx(A35.inv())), "Final 2023–24 Shift 2, Q3(b)", "src")
    # ---- conceptual
    B.mcq(ch, "Linear or not", 1, "If $T$ is linear then $T(0)=$", "$0$", ["$1$", "any vector", "$T$ need not map $0$ to $0$"], "$T(0)=T(0\\cdot v)=0\\cdot T(v)=0$.", "Lecture 6", "concept")
    B.mcq(ch, "Kernel, range, rank–nullity", 1, "A linear map $T$ is one-to-one iff …", "$\\ker T=\\{0\\}$", ["$\\operatorname{range}T=\\{0\\}$", "$\\operatorname{rank}T=0$", "$T$ is onto"], "If $T(u)=T(v)$ then $u-v\\in\\ker T$; injectivity ⇔ trivial kernel.", "Lecture 6", "concept")
    B.mcq(ch, "Kernel, range, rank–nullity", 2, "For $T:V\\to W$ linear with $\\dim V=n$, which identity always holds?", "$\\dim\\ker T+\\dim\\operatorname{range}T=n$", ["$\\dim\\ker T+\\dim\\operatorname{range}T=\\dim W$", "$\\dim\\ker T=\\dim\\operatorname{range}T$", "$\\dim\\operatorname{range}T=n$"], "Rank–nullity theorem.", "Lecture 6", "concept")
    B.mcq(ch, "Composition", 2, "If $T_1:\\mathbb{R}^2\\to\\mathbb{R}^3$ and $T_2:\\mathbb{R}^3\\to\\mathbb{R}^4$, the matrix of $T_2\\circ T_1$ has size", "$4\\times2$", ["$2\\times4$", "$3\\times3$", "$4\\times3$"], "$[T_2\\circ T_1]=[T_2][T_1]=(4\\times3)(3\\times2)=4\\times2$.", "Lecture 6", "concept")
    # ---- extension: Jacobian matrix (beyond MAT1.002, Calculus II) -- tagged so quiz sets can exclude it
    xx, yy = sp.symbols("x y")
    F = sp.Matrix([xx ** 2 * yy, xx + yy ** 3]); J = F.jacobian([xx, yy]); J0 = J.subs({xx: 1, yy: 2})
    B.mcq(ch, "Extension: Jacobian matrix", 3, "(Extension, not in MAT1.002.) For $F(x,y)=(x^2y,\\ x+y^3)$ the Jacobian matrix at $(1,2)$ is", mt(J0), [mt(J0.T), mt(perturb(J0, rng)), mt(-J0), mt(perturb(J0, rng)), mt(F.subs({xx: 1, yy: 2}))],
          "$J=\\begin{bmatrix}\\partial_xF_1&\\partial_yF_1\\\\\\partial_xF_2&\\partial_yF_2\\end{bmatrix}=%s$; at $(1,2)$: $%s$. It is the matrix of the best linear approximation of $F$ near the point (a linear transformation!)." % (mtx(J), mtx(J0)), "Extension (Jacobian: Calculus II)", "gen", tags=["extension"])
    rr, th = sp.symbols("r theta")
    Fp = sp.Matrix([rr * sp.cos(th), rr * sp.sin(th)]); Jp = Fp.jacobian([rr, th]); dJ = sp.simplify(Jp.det())
    B.mcq(ch, "Extension: Jacobian matrix", 3, "(Extension.) For the polar map $(r,\\theta)\\mapsto(r\\cos\\theta,\\ r\\sin\\theta)$ the Jacobian determinant is", "$r$", ["$1$", "$r^2$", "$\\cos\\theta\\sin\\theta$"],
          "$J=%s$, $\\det J=r\\cos^2\\theta+r\\sin^2\\theta=%s$ — the local area-scaling factor used in $dx\\,dy=r\\,dr\\,d\\theta$." % (mtx(Jp), tex(dJ)), "Extension (Jacobian: Calculus II)", "gen", tags=["extension"])

# ============================================================================== CHAPTER 7
def eig_multiset(A):
    ev = A.eigenvals()
    out = []
    for val, mult in sorted(ev.items(), key=lambda kv: float(sp.N(kv[0]))):
        out += [val] * mult
    return out

def eig_text(vals):
    return "$\\{" + ", ".join(tex(v_) for v_ in vals) + "\\}$"

def eig_options(vals, rng):
    """Correct multiset text + wrong ones from single changes."""
    corr = eig_text(vals)
    cands = [[-v_ for v_ in vals], [v_ + 1 for v_ in vals]]
    for i in range(len(vals)):
        w = list(vals); w[i] = w[i] + rng.choice([-2, -1, 1, 2]); cands.append(w)
        w2 = list(vals); w2[i] = -w2[i]; cands.append(w2)
    wr = uniq_by_text([eig_text(sorted(c_, key=lambda z: float(sp.N(z)))) for c_ in cands if sorted(c_, key=lambda z: float(sp.N(z))) != sorted(vals, key=lambda z: float(sp.N(z)))])
    return corr, wr

def ch7(B):
    ch = "c7"; rng = B.rng
    MATS = {
        "S7-E1": sp.Matrix([[2, 1], [5, -2]]), "S7-E2": sp.Matrix([[1, 0, 4], [0, 1, -2], [1, 0, -2]]),
        "S7-E3": sp.Matrix([[2, -1, 1], [-2, 3, -2], [-1, 1, 0]]), "S7-E4": sp.Matrix([[-2, -1, 3], [0, 1, 2], [0, 0, 1]]),
        "S7-E5": sp.Matrix([[-1, 1, 0], [0, 3, 0], [4, -2, 5]]), "S7-E6": sp.Matrix([[1, 3], [-1, 5]]),
        "S3-E12": sp.Matrix([[-3, 10], [5, 2]]), "S7-E8": sp.Matrix([[1, 3], [2, 0]]), "S7-E9": sp.Matrix([[3, 4], [4, -3]]), "S7-E10": sp.Matrix([[1, 2, 0], [2, 1, 0], [0, 0, 5]]),
        "F24S1": sp.Matrix([[-1, 4, -2], [-3, 4, 0], [-3, 1, 3]]), "F24S2": sp.Matrix([[2, -2, 2], [-2, 5, 1], [2, 1, 5]]),
        "F23S2": sp.Matrix([[3, -1, 1], [1, 1, 1], [1, -1, 3]]), "F23S1": sp.Matrix([[-1, 2, 0], [2, -4, 0], [0, 0, -5]]),
        "F22": sp.Matrix([[2, 0, -2], [0, 3, 0], [0, 0, 3]]), "F19": sp.Matrix([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]),
        "F18a": sp.Matrix([[1, 1, 0], [1, 2, 1], [0, -1, 1]]), "F18b": sp.Matrix([[1, -1, 0], [-1, 2, 1], [0, 1, 1]]),
    }
    SRC = {"S7-E1": "Exercise Sheet 7, Ex. 1", "S7-E2": "Exercise Sheet 7, Ex. 2", "S7-E3": "Exercise Sheet 7, Ex. 3", "S7-E4": "Exercise Sheet 7, Ex. 4", "S7-E5": "Exercise Sheet 7, Ex. 5",
           "S7-E6": "Exercise Sheet 7, Ex. 6", "S3-E12": "Exercise Sheet 3, Ex. 12", "S7-E8": "Exercise Sheet 7, Ex. 8", "S7-E9": "Exercise Sheet 7, Ex. 9", "S7-E10": "Exercise Sheet 7, Ex. 10",
           "F24S1": "Final 2024–25 Shift 1, Q5(a)", "F24S2": "Final 2024–25 Shift 2, Q5(a)", "F23S2": "Final 2023–24 Shift 2, Q5(a)", "F23S1": "Final 2023–24 Shift 1, Q5(a)",
           "F22": "Final 2022–23 Group 1, Q5", "F19": "Final 2019–20, Q5", "F18a": "Final 2018–19 (D,E,G), Q5", "F18b": "Final 2018–19 (A,B,C,AE), Q5"}
    info = {}
    for key, A in MATS.items():
        n = A.rows
        ev = eig_multiset(A)
        assert all(sp.im(sp.N(e_)) == 0 for e_ in ev), key
        P_cols = []
        eigs = A.eigenvects()
        geo = {val: len(basis) for val, mult, basis in eigs}
        alg = {val: mult for val, mult, basis in eigs}
        diag = all(geo[v_] == alg[v_] for v_ in geo)
        info[key] = (A, ev, eigs, geo, alg, diag, A == A.T)
        # verify A v = lambda v for every returned eigenvector
        for val, mult, basis in eigs:
            for b_ in basis:
                assert sp.simplify(A * b_ - val * b_) == sp.zeros(n, 1)
        if diag:
            P = sp.Matrix.hstack(*[b_ for val, mult, basis in eigs for b_ in basis]); D = sp.diag(*[val for val, mult, basis in eigs for b_ in basis])
            assert sp.simplify(P.inv() * A * P - D) == sp.zeros(n)
        # trace / det relations
        assert sum(ev) == A.trace() and sp.prod(ev) == A.det()
    for key, (A, ev, eigs, geo, alg, diag, sym) in info.items():
        src = SRC[key]; n = A.rows
        cp = sp.factor((A - lam * sp.eye(n)).det())
        c, wr = eig_options(ev, rng)
        B.mcq(ch, "Eigenvalues", 1 if n == 2 else 2, "Find all eigenvalues of $A=%s$ (listed with multiplicity)." % mtx(A), c, wr,
              "$\\det(A-\\lambda I)=%s$; its roots are the eigenvalues %s. (Check: trace $=%s=\\sum\\lambda$, $\\det A=%s=\\prod\\lambda$.)" % (tex(cp), eig_text(ev), tex(A.trace()), tex(A.det())), src, "src")
        if key in ("S7-E1", "S7-E8", "S7-E9", "S3-E12", "S7-E6", "S7-E3", "F24S1", "F23S2"):
            val = sorted(geo.keys(), key=lambda z: float(sp.N(z)))[-1]
            basis = [b_ for v_, m_, bs in eigs if v_ == val for b_ in bs]
            vv = basis[0] * sp.ilcm(*[sp.fraction(z)[1] for z in basis[0]])
            bad = []
            for cand in (list(reversed(list(vv))), [int(z) + 1 for z in vv], [-int(z) if i == 0 else int(z) for i, z in enumerate(vv)], [1] * n):
                cm = sp.Matrix(cand)
                if sp.simplify(A * cm - val * cm) != sp.zeros(n, 1) and cand not in bad:
                    bad.append(cand)
            if len(bad) >= 3:
                B.mcq(ch, "Eigenvectors", 2, "For $A=%s$, which vector is an eigenvector for $\\lambda=%s$?" % (mtx(A), tex(val)), V(list(vv)), [V(z) for z in bad[:3]],
                      "Solve $(A-%sI)x=0$. Then $Ax=\\lambda x$: $A%s=%s=%s\\cdot%s$." % (tex(val), vec(list(vv)), vec(list(A * vv)), tex(val), vec(list(vv))), src, "src")
        # diagonalizable?
        if n >= 2:
            ans = "Yes, diagonalizable" if diag else "No, not diagonalizable"
            why_ = ("each eigenvalue has geometric multiplicity = algebraic multiplicity: " + ", ".join("$\\lambda=%s$: %d = %d" % (tex(v_), geo[v_], alg[v_]) for v_ in sorted(geo, key=lambda z: float(sp.N(z))))) if diag else \
                   ("for $\\lambda=%s$ the eigenspace has dimension %d < multiplicity %d" % tuple([tex([v_ for v_ in geo if geo[v_] < alg[v_]][0]), geo[[v_ for v_ in geo if geo[v_] < alg[v_]][0]], alg[[v_ for v_ in geo if geo[v_] < alg[v_]][0]]]))
            yes_txt = "Yes: $A$ has $n$ independent eigenvectors"
            no_txt = "No: some eigenvalue has too few independent eigenvectors (geometric < algebraic multiplicity)"
            correct_txt = yes_txt if diag else no_txt
            wrong_txts = ["No: $A$ is not symmetric", "No: some eigenvalue is not real", "No: $A$ is not invertible"] if diag else \
                         ["Yes: all eigenvalues are real, which is enough", "Yes: $\\det A\\neq0$ is enough", "Yes: every square matrix is diagonalizable"]
            B.mcq(ch, "Diagonalization", 2, "Is $A=%s$ diagonalizable over $\\mathbb{R}$?" % mtx(A), correct_txt, wrong_txts,
                  "Eigenvalues %s; %s. $A$ is diagonalizable iff there are $n$ independent eigenvectors, i.e. geometric = algebraic multiplicity for every eigenvalue." % (eig_text(ev), why_), src, "src")
        # eigenspace dimension
        multi = [v_ for v_ in geo if alg[v_] >= 2]
        if multi:
            v_ = multi[0]
            B.mcq(ch, "Eigenvalues", 3, "For $A=%s$, the eigenvalue $\\lambda=%s$ has algebraic multiplicity %d. What is the dimension of its eigenspace?" % (mtx(A), tex(v_), alg[v_]), "$%d$" % geo[v_],
                  ["$%d$" % z for z in sorted({0, 1, 2, 3} - {geo[v_]})][:3],
                  "$\\dim\\ker(A-%sI)=n-\\operatorname{rank}(A-%sI)=%d-%d=%d$." % (tex(v_), tex(v_), n, (A - v_ * sp.eye(n)).rank(), geo[v_]), src, "src")
        if sym:
            B.mcq(ch, "Diagonalization", 2, "Can $A=%s$ be diagonalized by an orthogonal matrix $P$ (so $P^TAP=D$)?" % mtx(A), "Yes: $A$ is symmetric (spectral theorem)",
                  ["No: orthogonal diagonalization needs distinct eigenvalues", "No: orthogonal diagonalization needs all eigenvalues positive", "No: orthogonal diagonalization needs $\\det A=1$"],
                  "A real matrix is orthogonally diagonalizable iff it is symmetric. $A=A^T$ here; eigenspaces of different eigenvalues are orthogonal and repeated eigenvalues still give $n$ independent eigenvectors.", src, "src")
    # ---- powers A^n (Sheet 7 Ex. 8) and diagonal entries
    n_ = sp.Symbol("n", integer=True, positive=True)
    A8 = MATS["S7-E8"]
    P8 = sp.Matrix.hstack(*[b_ for v_, m_, bs in A8.eigenvects() for b_ in bs]); D8 = sp.diag(*[v_ for v_, m_, bs in A8.eigenvects() for b_ in bs])
    An = sp.simplify(P8 * sp.diag(*[D8[i, i] ** n_ for i in range(2)]) * P8.inv())
    for kk in (1, 2, 3, 5):
        assert sp.simplify(An.subs(n_, kk) - A8 ** kk) == sp.zeros(2)
    ent = sp.simplify(An[0, 0])
    A5pow = A8 ** 5
    c, wr = numopts(A5pow[0, 0], rng, extra=[A8[0, 0] ** 5, sp.simplify(D8[0, 0] ** 5 + D8[1, 1] ** 5), (A8 ** 4)[0, 0]])
    B.mcq(ch, "Powers via diagonalization", 3, "For $A=%s$ (eigenvalues $3$ and $-2$), the $(1,1)$ entry of $A^5$ is" % mtx(A8), c, wr,
          "$A=PDP^{-1}$ gives $A^n=PD^nP^{-1}$; here $(A^n)_{11}=%s$. For $n=5$: $A^5=%s$, so the entry is $%s$." % (tex(ent), mtx(A5pow), tex(A5pow[0, 0])), "Exercise Sheet 7, Ex. 8", "src")
    # (A^n)_11 = a*3^n + b*(-2)^n with (a,b) computed from the diagonalization
    a_c = sp.simplify(ent.coeff(3 ** n_)); b_c = sp.simplify(ent.coeff((-2) ** n_))
    assert sp.simplify(a_c * 3 ** n_ + b_c * (-2) ** n_ - ent) == 0
    form = lambda a0, b0: "$%s$" % tex(sp.simplify(a0 * 3 ** n_ + b0 * (-2) ** n_))
    wrong_pairs = [(b_c, a_c), (1, 1), (a_c, -b_c), (b_c, b_c), (a_c, a_c)]
    B.mcq(ch, "Powers via diagonalization", 3, "For $A=%s$, which formula gives $(A^{n})_{11}$?" % mtx(A8), form(a_c, b_c),
          [form(x0, y0) for x0, y0 in wrong_pairs if (x0, y0) != (a_c, b_c)],
          "Diagonalise: $A^n=PD^nP^{-1}$ with eigenvalues $3,-2$; the $(1,1)$ entry is $%s$ (check $n=1$: $%s$, $n=2$: $%s$)." % (tex(ent), tex(ent.subs(n_, 1)), tex(ent.subs(n_, 2))), "Exercise Sheet 7, Ex. 8", "src")
    # ---- A^k for past-paper matrices
    kk = sp.Symbol("k", integer=True, positive=True)
    for key, nm in (("F23S2", "2023–24 Shift 2"), ("F22", "2022–23 Group 1"), ("F19", "2019–20")):
        A, ev, eigs, geo, alg, diag, sym = info[key]
        P = sp.Matrix.hstack(*[b_ for v_, m_, bs in eigs for b_ in bs]); D = sp.diag(*[v_ for v_, m_, bs in eigs for b_ in bs])
        Ak = sp.simplify(P * sp.diag(*[D[i, i] ** kk for i in range(A.rows)]) * P.inv())
        for t_ in (1, 2, 3):
            assert sp.simplify(Ak.subs(kk, t_) - A ** t_) == sp.zeros(A.rows)
        ij = (0, A.cols - 1)
        A3 = A ** 3
        c, wr = numopts(A3[ij[0], ij[1]], rng, extra=[(A ** 2)[ij], A[ij] ** 3, (A ** 4)[ij]])
        B.mcq(ch, "Powers via diagonalization", 3, "Exam: $A=%s$. The entry in row 1, column %d of $A^3$ is" % (mtx(A), A.cols), c, wr,
              "$A$ is diagonalizable ($P^{-1}AP=D$), so $A^k=PD^kP^{-1}=%s$; for $k=3$: $A^3=%s$ and the entry is $%s$." % (mtx(Ak), mtx(A3), tex(A3[ij])), SRC[key] + "(b)", "src")
    # ---- proofs / concepts
    B.mcq(ch, "Eigenvalues", 2, "If $A^2=2A$ and $\\lambda$ is an eigenvalue of $A$, then $\\lambda$ must be", "$0$ or $2$", ["$1$ or $2$", "$0$ or $1$", "any real number"], "From $Av=\\lambda v$: $A^2v=\\lambda^2v$ and $2Av=2\\lambda v$, so $\\lambda^2=2\\lambda$, i.e. $\\lambda\\in\\{0,2\\}$.", "Final 2023–24 Shift 1, Q5(b)", "src")
    B.mcq(ch, "Eigenvalues", 2, "If $A$ is invertible and $\\lambda=a\\ne0$ is an eigenvalue of $A$, then an eigenvalue of $A^{-1}$ is", "$1/a$", ["$-a$", "$a^2$", "$a$"], "$Av=av$ ⇒ $v=aA^{-1}v$ ⇒ $A^{-1}v=\\tfrac1av$ (same eigenvector).", "Final 2024–25 Shift 1, Q5(b)", "src")
    B.mcq(ch, "Eigenvalues", 1, "For an $n\\times n$ matrix, the sum of the eigenvalues (with multiplicity) equals", "the trace of $A$", ["the determinant of $A$", "the rank of $A$", "$n$"], "The coefficient of $\\lambda^{n-1}$ in the characteristic polynomial is $-\\operatorname{tr}A$.", "Lecture 7", "concept")
    B.mcq(ch, "Eigenvalues", 1, "For an $n\\times n$ matrix, the product of the eigenvalues (with multiplicity) equals", "the determinant of $A$", ["the trace of $A$", "$0$", "$1$"], "Set $\\lambda=0$ in $\\det(A-\\lambda I)=\\prod(\\lambda_i-\\lambda)$.", "Lecture 7", "concept")
    B.mcq(ch, "Diagonalization", 2, "Eigenvectors belonging to DISTINCT eigenvalues are always", "linearly independent", ["orthogonal (for every matrix)", "equal", "parallel"], "Distinct eigenvalues give independent eigenvectors; they are orthogonal only for symmetric matrices.", "Lecture 7", "concept")
    B.mcq(ch, "Eigenvalues", 2, "A square matrix $A$ is invertible iff", "$0$ is not an eigenvalue of $A$", ["$1$ is an eigenvalue of $A$", "all eigenvalues are positive", "$A$ is symmetric"], "$0$ is an eigenvalue iff $\\det A=0$.", "Lecture 7", "concept")
    # ---- random 2x2 with integer eigenvalues
    made = 0
    while made < 5:
        l1, l2 = rng.sample(range(-4, 6), 2)
        while True:
            Pm = sp.Matrix(2, 2, lambda i, j: rng.randint(-2, 3))
            if Pm.det() in (1, -1):
                break
        A = Pm * sp.diag(l1, l2) * Pm.inv()
        ev = eig_multiset(A)
        c, wr = eig_options(ev, rng)
        if B.mcq(ch, "Eigenvalues", 1, "Find the eigenvalues of $A=%s$." % mtx(A), c, wr,
                 "$\\det(A-\\lambda I)=\\lambda^2-(%s)\\lambda+(%s)=%s$, so the eigenvalues are %s." % (tex(A.trace()), tex(A.det()), tex(sp.factor(sp.expand((A - lam * sp.eye(2)).det()))), eig_text(ev)), "Generated (2×2 eigenvalues)", "gen"):
            made += 1
