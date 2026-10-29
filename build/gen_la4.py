# -*- coding: utf-8 -*-
"""Linear Algebra extras from the exercises of 'Linear Algebra Summary (UPDATED Gen 16 edition)' and from the lecture theory
that the first generators did not cover (rows/columns of AB, sequence subspaces, similarity, orthogonal matrices, rotations and
projections, ...). Every claim is verified by computation (exact sympy arithmetic, plus explicit counterexamples).

Formatting rule used below: mtx(M) = matrix LaTeX WITHOUT dollars (use inside running text that is already in math mode);
mt(M) / mats(...) = matrix WITH dollars (use for stand-alone answer options)."""
import numpy as np
import sympy as sp
from qlib import tex, M, vec, uniq_by_text, note
from la_common import *
from la_steps import mtx
from gen_la1 import mt
from gen_la2 import V

SUM = "Linear Algebra Summary (Gen 16)"

def rand_mat(rng, r, c, lo=-3, hi=3):
    return sp.Matrix(r, c, lambda i, j: rng.randint(lo, hi))

def mats(*Ms):
    return [mt(Mi) for Mi in Ms]

# ============================================================================== CHAPTER 1
def ch1(B):
    ch = "c1"
    # --- row-operation notation: subtract R1 from R2 in ONE elementary operation
    A0 = sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    target = A0.copy(); target[1, :] = A0[1, :] - A0[0, :]
    def op_correct(Z): N = Z.copy(); N[1, :] = -Z[0, :] + Z[1, :]; return N
    def op_reversed(Z): N = Z.copy(); N[1, :] = Z[0, :] - Z[1, :]; return N
    def op_other_row(Z): N = Z.copy(); N[0, :] = Z[1, :] - Z[0, :]; return N
    def op_swap(Z): N = Z.copy(); r0, r1 = Z[0, :], Z[1, :]; N[0, :] = r1; N[1, :] = r0; return N
    assert op_correct(A0) == target and op_reversed(A0) != target and op_other_row(A0) != target and op_swap(A0) != target
    assert op_reversed(A0)[1, :] == -target[1, :]          # it is the wanted row with its sign changed: two elementary steps, not one
    B.mcq(ch, "Row operations", 1, "In the course notation, which single elementary row operation replaces $R_2$ by $R_2-R_1$?", "$-R_1+R_2\\to R_2$",
          ["$R_1-R_2\\to R_2$", "$R_2-R_1\\to R_1$", "$R_1\\leftrightarrow R_2$"],
          "The allowed forms are $R_i\\leftrightarrow R_j$, $kR_i\\to R_i$ and $kR_i+R_j\\to R_j$. To subtract a row, add $(-1)$ times it: $-R_1+R_2\\to R_2$. "
          "Writing $R_1-R_2\\to R_2$ gives the opposite row $R_1-R_2$ (it needs two steps: $-R_1+R_2\\to R_2$ and then $-R_2\\to R_2$); $R_2-R_1\\to R_1$ changes the wrong row; a swap only exchanges rows.", SUM + ", I.2 (note on row operations)", "src")
    # --- system with a parameter: x+2y-3z=4, 3x-y+5z=2, 4x+y+(a^2-14)z=a+2
    A = sp.Matrix([[1, 2, -3], [3, -1, 5], [4, 1, a ** 2 - 14]]); b = sp.Matrix([4, 2, a + 2])
    assert sp.expand(A.det() + 7 * (a ** 2 - 16)) == 0                  # det A = -7 (a - 4)(a + 4)
    cls = classify_param(A, b, a)
    assert cls[-4] == "none" and cls[4] == "inf" and cls["generic"] == "unique", cls
    assert sp.expand(A[2, 2] - (A[0, 2] + A[1, 2]) - (a ** 2 - 16)) == 0 and A[2, 0] == A[0, 0] + A[1, 0] and A[2, 1] == A[0, 1] + A[1, 1] and sp.expand(b[2] - b[0] - b[1] - (a - 4)) == 0   # row3-row1-row2 = (0,0,a^2-16 | a-4)
    system = "$\\begin{cases}x+2y-3z=4\\\\3x-y+5z=2\\\\4x+y+(a^2-14)z=a+2\\end{cases}$"
    hint = "Subtract the first two equations from the third: $(a^2-16)z=a-4$, i.e. $(a-4)(a+4)z=a-4$."
    ct, wr = set_options([-4], [-4, 4], a, B.rng)
    B.mcq(ch, "Systems with a parameter", 3, "For which values of $a$ does the system %s have NO solution?" % system, ct, wr,
          hint + " If $a=-4$ this reads $0\\cdot z=-8$: inconsistent. If $a=4$ it reads $0\\cdot z=0$ (a free variable), and if $a\\neq\\pm4$ the coefficient matrix is invertible ($\\det=-7(a^2-16)\\neq0$).", SUM + ", I.4 (system with a parameter)", "src")
    ct, wr = set_options([4], [-4, 4], a, B.rng)
    B.mcq(ch, "Systems with a parameter", 3, "For which values of $a$ does the system %s have infinitely many solutions?" % system, ct, wr,
          hint + " At $a=4$ the last equation becomes $0\\cdot z=0$, so $z$ is free and (with the first two equations) the solution set is a line.", SUM + ", I.4 (system with a parameter)", "src")
    B.mcq(ch, "Systems with a parameter", 3, "For which values of $a$ does the system %s have exactly one solution?" % system, "$a\\neq4$ and $a\\neq-4$",
          ["$a=4$ only", "$a=-4$ only", "$a=\\pm4$"],
          hint + " When $a^2-16\\neq0$ we can divide: $z=\\frac{1}{a+4}$, and the other unknowns follow from the first two equations.", SUM + ", I.4 (system with a parameter)", "src")

# ============================================================================== CHAPTER 2
def ch2(B):
    ch = "c2"
    rng = B.rng
    # --- rows and columns of AB
    for _ in range(200):
        Am, Bm = rand_mat(rng, 3, 3), rand_mat(rng, 3, 3)
        Bc = Bm.copy(); Bc[:, 2] = Bc[:, 0]; assert (Am * Bc)[:, 0] == (Am * Bc)[:, 2]      # equal columns of B -> equal columns of AB
        Ar = Am.copy(); Ar[2, :] = Ar[0, :]; assert (Ar * Bm)[0, :] == (Ar * Bm)[2, :]      # equal rows of A -> equal rows of AB
    A1 = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 1, 1]]); B1 = sp.Matrix([[1, 2], [0, 1], [1, 2]])
    assert B1[0, :] == B1[2, :] and (A1 * B1)[0, :] != (A1 * B1)[2, :]                       # equal rows of B do NOT give equal rows of AB
    A2, B2 = sp.Matrix([[1, 1], [0, 1]]), sp.Matrix([[1, 0], [1, 1]])
    assert (A2 * B2) ** 2 != A2 ** 2 * B2 ** 2
    D1, D2 = sp.diag(1, 2), sp.diag(3, 4)
    assert (D1 * D2) ** 2 == D1 ** 2 * D2 ** 2
    cexB = "For example $A=%s$, $B=%s$ have equal rows $1$ and $3$ in $B$, but $AB=%s$ has different rows $1$ and $3$." % (mtx(A1), mtx(B1), mtx(A1 * B1))
    B.mcq(ch, "Properties", 2, "For matrices $A,B$ with $AB$ defined, which statement is TRUE in general?", "If columns $1$ and $3$ of $B$ are equal, then columns $1$ and $3$ of $AB$ are equal",
          ["If rows $1$ and $3$ of $B$ are equal, then rows $1$ and $3$ of $AB$ are equal", "$(AB)^2=A^2B^2$", "$AB=BA$ whenever both products are defined"],
          "Column $j$ of $AB$ is $A$ times column $j$ of $B$, so equal columns of $B$ give equal columns of $AB$. " + cexB, SUM + ", II (exercise 2)", "src")
    B.mcq(ch, "Properties", 2, "For matrices $A,B$ with $AB$ defined, which statement is TRUE in general?", "If rows $1$ and $3$ of $A$ are equal, then rows $1$ and $3$ of $AB$ are equal",
          ["If rows $1$ and $3$ of $B$ are equal, then rows $1$ and $3$ of $AB$ are equal", "$(A+B)^2=A^2+2AB+B^2$", "$(AB)^2=A^2B^2$"],
          "Row $i$ of $AB$ is (row $i$ of $A$)$\\cdot B$, so equal rows of $A$ give equal rows of $AB$. " + cexB + " Also $(A+B)^2=A^2+AB+BA+B^2$, which equals $A^2+2AB+B^2$ only when $AB=BA$.", SUM + ", II (exercise 2)", "src")
    B.mcq(ch, "Properties", 2, "For $n\\times n$ matrices $A,B$, the equation $(AB)^2=A^2B^2$", "holds for some pairs (for instance when $AB=BA$) but not for every pair",
          ["holds for every pair of matrices", "never holds unless $A$ or $B$ is the zero matrix", "holds exactly when $A$ and $B$ are both invertible"],
          "$(AB)^2=ABAB$ and $A^2B^2=AABB$, so they agree when $A$ and $B$ commute: for the non-zero diagonal matrices $A=\\operatorname{diag}(1,2)$, $B=\\operatorname{diag}(3,4)$ both sides are equal. "
          "Counterexample (both invertible): $A=%s$, $B=%s$ give $(AB)^2=%s\\neq A^2B^2=%s$." % (mtx(A2), mtx(B2), mtx((A2 * B2) ** 2), mtx(A2 ** 2 * B2 ** 2)), SUM + ", II (exercise 2d)", "src")
    # --- cancellation: AC = BC
    Cs = sp.Matrix([[1, 0], [0, 0]]); Ax = sp.Matrix([[1, 2], [3, 4]]); Bx = sp.Matrix([[1, 9], [3, -5]])
    assert Ax * Cs == Bx * Cs and Ax != Bx and Cs != sp.zeros(2) and Cs.det() == 0
    for _ in range(100):                                         # with an invertible C the cancellation is valid
        C = rand_mat(rng, 2, 2)
        if C.det() != 0:
            P1, P2 = rand_mat(rng, 2, 2), rand_mat(rng, 2, 2)
            assert (P1 * C == P2 * C) == (P1 == P2)
    B.mcq(ch, "Properties", 3, "Let $AC=BC$ with $C\\neq0$. Which conclusion is correct?", "if $C$ is invertible then $A=B$; if $C$ is singular, $A=B$ is not guaranteed",
          ["$A=B$ always, because $C\\neq0$", "$A\\neq B$ whenever $C$ is singular", "$A=B$ only when $C$ is singular"],
          "If $C$ is invertible, multiply on the right by $C^{-1}$. If $C$ is singular, cancellation can fail: for $C=%s$, $A=%s$, $B=%s$ we get $AC=BC=%s$ although $A\\neq B$. "
          "(But $A=B$ can still happen: it is just not forced.)" % (mtx(Cs), mtx(Ax), mtx(Bx), mtx(Ax * Cs)), SUM + ", II.2 (cancellation)", "src")
    note(SUM + ", II.2", "The notes say that for $AC=BC$ with $C\\neq0$ and $C$ not invertible, 'then $A\\neq B$'. That is too strong: when $C$ is singular, $A=B$ is simply not guaranteed (it may or may not hold).")
    # --- B = [[3,-4,1],[1,2,3],[4,-1,0]]: inverse (Gauss-Jordan) and the solution of Bx = (-1,2,7)
    Bm = sp.Matrix([[3, -4, 1], [1, 2, 3], [4, -1, 0]]); bb = sp.Matrix([-1, 2, 7])
    Binv = Bm.inv(); xs = Binv * bb
    assert Bm.det() == -48 and list(xs) == [sp.Rational(103, 48), sp.Rational(19, 12), sp.Rational(-53, 48)] and Bm * xs == bb
    assert Binv == sp.Matrix([[sp.Rational(-1, 16), sp.Rational(1, 48), sp.Rational(7, 24)], [sp.Rational(-1, 4), sp.Rational(1, 12), sp.Rational(1, 6)], [sp.Rational(3, 16), sp.Rational(13, 48), sp.Rational(-5, 24)]])
    B.mcq(ch, "Inverse (Gauss–Jordan)", 3, "For $B=%s$, solve $Bx=b$ with $b=(-1,2,7)$ (use $x=B^{-1}b$)." % mtx(Bm), V(list(xs)),
          [V(w) for w in near_vectors(list(xs), Bm, bb, rng, 6)[:3]],
          "Gauss–Jordan on $[B\\,|\\,I]$ gives $B^{-1}=%s$ ($\\det B=-48$). Then $x=B^{-1}b=\\left(\\frac{103}{48},\\frac{19}{12},-\\frac{53}{48}\\right)$. Check: $Bx=(-1,2,7)$." % mtx(Binv), SUM + ", II exercise 3", "src")
    B.mcq(ch, "Inverse (Gauss–Jordan)", 3, "What is the entry in row $2$, column $3$ of $B^{-1}$ for $B=%s$?" % mtx(Bm), "$%s$" % tex(Binv[1, 2]),
          ["$%s$" % tex(Binv[2, 1]), "$%s$" % tex(-Binv[1, 2]), "$%s$" % tex(Bm[1, 2])],
          "Reduce $[B\\,|\\,I]$ to $[I\\,|\\,B^{-1}]$: $B^{-1}=%s$. Its $(2,3)$ entry is $%s$ (the $(3,2)$ entry is $%s$)." % (mtx(Binv), tex(Binv[1, 2]), tex(Binv[2, 1])), SUM + ", II exercise 3", "src")
    # --- for which c is [[2,c,c],[c,c,c],[8,7,c]] singular?
    c = sp.Symbol("c")
    Ac = sp.Matrix([[2, c, c], [c, c, c], [8, 7, c]])
    roots = sp.solve(Ac.det(), c); assert sorted(roots) == [0, 2, 7], roots
    assert Ac.subs(c, 0).rank() < 3 and Ac.subs(c, 2)[0, :] == Ac.subs(c, 2)[1, :] and Ac.subs(c, 7)[:, 1] == Ac.subs(c, 7)[:, 2]
    B.mcq(ch, "Invertibility", 3, "For which values of $c$ is $A=%s$ NOT invertible?" % mtx(Ac), "$c\\in\\{0,2,7\\}$", ["$c\\in\\{0,2\\}$", "$c\\in\\{2,7,8\\}$", "$c\\in\\{0,7\\}$"],
          "Expanding gives $\\det A=%s$, whose roots are $c=0,2,7$. In terms of the rows and columns: $c=0$ gives a zero row (row $2$), $c=2$ gives two equal rows (rows $1,2$), $c=7$ gives two equal columns (columns $2,3$)." % tex(sp.factor(Ac.det())), SUM + ", II exercise 4", "src")

# ============================================================================== CHAPTER 3
def ch3(B):
    ch = "c3"
    # --- 2022 A^3 + A^2 - A + 3I = 0  =>  A is invertible
    a1 = [z.real for z in np.roots([2022, 1, -1, 3]) if abs(z.imag) < 1e-12][0]
    assert abs(2022 * a1 ** 3 + a1 ** 2 - a1 + 3) < 1e-9 and abs(a1 * (-(2022 * a1 ** 2 + a1 - 1) / 3) - 1) < 1e-9        # 1x1 sanity check of A^{-1} = -(2022A^2+A-I)/3
    Z = sp.Symbol("Z")
    assert sp.expand(Z * (2022 * Z ** 2 + Z - 1) - (2022 * Z ** 3 + Z ** 2 - Z)) == 0
    B.mcq(ch, "Properties of det", 3, "A square matrix $A$ satisfies $2022A^3+A^2-A+3I=0$. Which argument shows that $A$ is invertible?",
          "$A\\,(2022A^2+A-I)=-3I$, so $\\det A\\cdot\\det(2022A^2+A-I)=(-3)^n\\neq0$ and therefore $\\det A\\neq0$",
          ["taking determinants term by term gives $2022\\det A^3+\\det A^2-\\det A+3=0$, which cannot hold for $\\det A=0$", "every square matrix that satisfies a polynomial equation is invertible", "the equation has the constant term $3$, which is the determinant of $A$"],
          "Move $3I$ to the right and factor $A$ out of the other three terms (all are polynomials in $A$, so they commute): $A(2022A^2+A-I)=-3I$. Taking determinants, $\\det A\\cdot\\det(2022A^2+A-I)=(-3)^n\\neq0$, so $\\det A\\neq0$. "
          "It even gives $A^{-1}=-\\frac13(2022A^2+A-I)$. The other arguments are wrong: $\\det$ is not additive, and e.g. $A=0$ satisfies $A^2=0$ but is not invertible.", SUM + ", III exercise 2", "src")
    note(SUM + ", III exercise 2", "The factorisation is printed as $A(2022A^3+A^2-A)=-3I$; it should be $A(2022A^2+A-I)=-3I$. Also $\\det(-3I)=(-3)^n$ for an $n\\times n$ matrix, not $-3$. The conclusion (A invertible) is unaffected.")
    # --- inverse by the adjoint
    A = sp.Matrix([[-3, -5, -7], [2, 4, 3], [0, 1, -1]])
    cof = A.cofactor_matrix(); adj = cof.T
    assert A.det() == -3 and cof == sp.Matrix([[-7, 2, 2], [-12, 3, 3], [13, -5, -2]]) and A.inv() == adj / A.det()
    assert A.inv() == sp.Matrix([[sp.Rational(7, 3), 4, sp.Rational(-13, 3)], [sp.Rational(-2, 3), -1, sp.Rational(5, 3)], [sp.Rational(-2, 3), -1, sp.Rational(2, 3)]])
    opts = mats(A.inv(), cof / A.det(), adj / 3, adj)
    assert len(set(opts)) == 4
    B.mcq(ch, "Adjugate", 3, "Use the adjoint (adjugate) to find $A^{-1}$ for $A=%s$ (here $\\det A=-3$)." % mtx(A), opts[0], opts[1:],
          "Cofactors: $C=%s$. The adjoint is the TRANSPOSE of the cofactor matrix, $\\operatorname{adj}A=%s$, and $A^{-1}=\\frac{1}{\\det A}\\operatorname{adj}A=-\\frac13\\operatorname{adj}A=%s$. Check: $AA^{-1}=I$. "
          "The wrong options forget the transpose, divide by $+3$ instead of $-3$, or forget to divide." % (mtx(cof), mtx(adj), mtx(A.inv())), SUM + ", III exercise 4", "src")
    B.mcq(ch, "Adjugate", 2, "For $A=%s$ the cofactor $C_{23}=(-1)^{2+3}M_{23}$ equals" % mtx(A), "$%s$" % tex(cof[1, 2]), ["$%s$" % tex(-cof[1, 2]), "$%s$" % tex(cof[2, 1]), "$%s$" % tex(cof[0, 0])],
          "Delete row $2$ and column $3$: $M_{23}=\\det\\begin{bmatrix}-3&-5\\\\0&1\\end{bmatrix}=-3$. The sign is $(-1)^{5}=-1$, so $C_{23}=3$.", SUM + ", III exercise 4", "src")

# ============================================================================== CHAPTER 4
def ch4(B):
    ch = "c4"
    rng = B.rng
    # --- subsets of R^infinity (sequences): closure checked with explicit sequences / reasoning
    N = 30
    seq = lambda f: [f(j) for j in range(1, N + 1)]
    inf_zeros = lambda s: sum(1 for z in s[:N] if z == 0) >= N // 2           # 'infinitely many zeros' for these periodic test sequences
    decreasing = lambda s: all(s[i + 1] <= s[i] for i in range(len(s) - 1))
    def geometric(s):
        if s[0] == 0:
            return all(z == 0 for z in s)
        k_ = sp.Rational(s[1], s[0]); return all(s[i + 1] == k_ * s[i] for i in range(len(s) - 1))
    def arithmetic(s):
        return all(s[i + 1] - s[i] == s[1] - s[0] for i in range(len(s) - 1))
    u, v = seq(lambda j: (j + 1) % 2), seq(lambda j: j % 2)                    # (1,0,1,0,...) and (0,1,0,1,...)
    assert inf_zeros(u) and inf_zeros(v) and not inf_zeros([p + q for p, q in zip(u, v)])
    dec = seq(lambda j: -j); assert decreasing(dec) and not decreasing([-z for z in dec])
    g1, g2 = seq(lambda j: 1), seq(lambda j: 2 ** (j - 1))
    assert geometric(g1) and geometric(g2) and not geometric([p + q for p, q in zip(g1, g2)]) and geometric([5 * z for z in g2])
    assert [p + q for p, q in zip(g1, g2)][:4] == [2, 3, 5, 9]
    ar1, ar2 = seq(lambda j: 3 + 2 * (j - 1)), seq(lambda j: -1 + 5 * (j - 1)); assert arithmetic([p + q for p, q in zip(ar1, ar2)]) and arithmetic([-4 * z for z in ar1])
    SUBS = {
        "T1": ("all sequences with $x_j=0$ from some point onward", "if $x_j=0$ for $j>p$ and $y_j=0$ for $j>q$, then $x+y$ and $cx$ vanish for $j>\\max(p,q)$"),
        "T2": ("all convergent sequences", "the sum of two convergent sequences, and a constant multiple of one, converge (limit laws)"),
        "T3": ("all arithmetic progressions ($x_{j+1}-x_j$ is the same for every $j$)", "two progressions with differences $d,d'$ add up to a progression with difference $d+d'$, and $cx$ has difference $cd$"),
        "F1": ("all sequences with infinitely many zeros, such as $(1,0,1,0,\\dots)$", "$(1,0,1,0,\\dots)+(0,1,0,1,\\dots)=(1,1,1,\\dots)$ has no zero at all, so the set is not closed under addition"),
        "F2": ("all decreasing sequences ($x_{j+1}\\le x_j$ for every $j$)", "$(-1,-2,-3,\\dots)$ is decreasing but $(-1)\\cdot(-1,-2,-3,\\dots)=(1,2,3,\\dots)$ is increasing: not closed under scalar multiplication"),
        "F3": ("all geometric progressions $(x_1,kx_1,k^2x_1,\\dots)$, allowing every $k$ and $x_1$", "$(1,1,1,\\dots)+(1,2,4,8,\\dots)=(2,3,5,9,\\dots)$ is not geometric ($\\frac32\\neq\\frac53$): not closed under addition"),
    }
    trues = ["T1", "T2", "T3"]; falses = ["F1", "F2", "F3"]
    for tk in trues:
        B.mcq(ch, "Subspaces", 2, "Which of the following subsets of $\\mathbb{R}^\\infty$ (all real sequences $x_1,x_2,\\dots$) is a subspace?", SUBS[tk][0], [SUBS[fk][0] for fk in falses],
              "Closure test, subset by subset. Subspace: %s. Not subspaces: %s." % (SUBS[tk][1], "; ".join(SUBS[fk][1] for fk in falses)), SUM + ", IV exercise 1", "src")
    for fk in falses:
        B.mcq(ch, "Subspaces", 2, "Which of the following subsets of $\\mathbb{R}^\\infty$ (all real sequences $x_1,x_2,\\dots$) is NOT a subspace?", SUBS[fk][0], [SUBS[tk][0] for tk in trues],
              "Closure test, subset by subset. Not a subspace: %s. Subspaces: %s." % (SUBS[fk][1], "; ".join(SUBS[tk][1] for tk in trues)), SUM + ", IV exercise 1", "src")
    # --- v4 = v1 - v2 + v3
    v1, v2, v3, v4 = sp.Matrix([1, 1, 0, 0]), sp.Matrix([1, 0, 1, 0]), sp.Matrix([0, 0, 1, 1]), sp.Matrix([0, 1, 0, 1])
    assert v4 == v1 - v2 + v3 and sp.Matrix.hstack(v1, v2, v3, v4).rank() == 3 and sp.Matrix.hstack(v1, v2, v3).rank() == 3
    wrongs = [v1 + v2 - v3, v1 - v2 - v3, v1 + v2 + v3]
    assert all(w != v4 for w in wrongs) and [tuple(w) for w in wrongs] == [(2, 1, 0, -1), (0, 1, -2, -1), (2, 1, 2, 1)]
    B.mcq(ch, "Span, independence, basis", 2, "The vectors $v_1=(1,1,0,0)$, $v_2=(1,0,1,0)$, $v_3=(0,0,1,1)$, $v_4=(0,1,0,1)$ are linearly dependent. Which relation shows it?", "$v_4=v_1-v_2+v_3$",
          ["$v_4=v_1+v_2-v_3$", "$v_4=v_1-v_2-v_3$", "$v_4=v_1+v_2+v_3$"],
          "Compute $v_1-v_2+v_3=(1-1+0,\\ 1-0+0,\\ 0-1+1,\\ 0-0+1)=(0,1,0,1)=v_4$, i.e. $v_1-v_2+v_3-v_4=0$ is a non-trivial relation. The other combinations give $(2,1,0,-1)$, $(0,1,-2,-1)$ and $(2,1,2,1)$. (Four vectors in $\\mathbb{R}^4$ need not be independent: here the rank is $3$.)", SUM + ", IV exercise 2", "src")
    # --- a basis of the column space from the pivot columns
    Ab = sp.Matrix([[1, 2, 0, -1], [-2, -3, 4, 5], [2, 4, 0, -2]])
    R, piv = Ab.rref(); assert piv == (0, 1) and R == sp.Matrix([[1, 0, -8, -7], [0, 1, 4, 3], [0, 0, 0, 0]])
    assert Ab.rank() == 2 and all(Ab[2, j] == 2 * Ab[0, j] for j in range(4)) and Ab[:, [0, 1]].rank() == 2          # V = {(x, y, 2x)}
    inV = lambda w: Ab.row_join(sp.Matrix(w)).rank() == 2
    assert not inV([1, 0, 0]) and inV([1, -2, 2]) and sp.Matrix([[1, -2, 2], [2, -3, 4], [0, 4, 0]]).rank() == 2 and sp.Matrix([[1, -2, 2]]).rank() == 1
    B.mcq(ch, "Span, independence, basis", 3, "Which set is a basis of $V=\\operatorname{span}\\{(1,-2,2),(2,-3,4),(0,4,0),(-1,5,-2)\\}$?", "$\\{(1,-2,2),\\ (2,-3,4)\\}$",
          ["$\\{(1,0,0),\\ (0,1,0)\\}$", "$\\{(1,-2,2),\\ (2,-3,4),\\ (0,4,0)\\}$", "$\\{(1,-2,2)\\}$"],
          "Put the vectors as the columns of $A=%s$ and row reduce: $%s$. The pivot columns are columns $1$ and $2$, so the corresponding columns of the ORIGINAL matrix $A$ form a basis and $\\dim V=2$. "
          "Wrong options: the columns of the echelon form are not in $V$ (every vector of $V$ has third coordinate equal to twice the first, which $(1,0,0)$ violates); three vectors cannot be independent in a $2$-dimensional space; one vector cannot span a plane." % (mtx(Ab), mtx(R)), SUM + ", IV exercise 3", "src")
    # --- the four fundamental subspaces of a matrix with independent columns
    for (mm, nn) in ((7, 4), (5, 3)):
        Af = sp.Matrix(mm, nn, lambda i, j: rng.randint(-3, 3))
        while Af.rank() != nn:
            Af = sp.Matrix(mm, nn, lambda i, j: rng.randint(-3, 3))
        dims = (Af.rank(), Af.T.rank(), len(Af.nullspace()), len(Af.T.nullspace()))
        assert dims == (nn, nn, 0, mm - nn)
        lab = lambda d: "$%d,\\ %d,\\ %d,\\ %d$" % d
        cand = [dims, (nn, nn, mm - nn, 0), (mm, mm, 0, nn), (nn, mm, 0, mm - nn)]
        assert len(set(cand)) == 4
        B.mcq(ch, "Null space and rank", 2, "A $%d\\times%d$ matrix $A$ has linearly independent columns. What are $\\dim \\mathrm{RS}(A),\\ \\dim \\mathrm{CS}(A),\\ \\dim N(A),\\ \\dim N(A^T)$ in this order?" % (mm, nn), lab(cand[0]), [lab(c_) for c_ in cand[1:]],
              "Independent columns give $\\operatorname{rank}A=n=%d$, so the row space and the column space both have dimension $%d$. Then $\\dim N(A)=n-\\operatorname{rank}A=0$ and $\\dim N(A^T)=m-\\operatorname{rank}A=%d-%d=%d$." % (nn, nn, mm, nn, mm - nn), SUM + ", IV exercise 5", "src")
    # --- coordinates and transition matrix
    Bb = sp.Matrix([[1, -1], [1, 1]]); xB = sp.Matrix([3, 5])
    assert list(Bb * xB) == [-2, 8] and list(3 * sp.Matrix([1, 1]) - 5 * sp.Matrix([-1, 1])) == [8, -2] and list(5 * sp.Matrix([1, 1]) + 3 * sp.Matrix([-1, 1])) == [2, 8]
    B.mcq(ch, "Coordinates and change of basis", 2, "Let $B=\\{(1,1),(-1,1)\\}$ be a basis of $\\mathbb{R}^2$ and $[x]_B=\\begin{bmatrix}3\\\\5\\end{bmatrix}$. Find the coordinates of $x$ in the standard basis.", V([-2, 8]),
          [V([8, -2]), V([2, 8]), V([3, 5])],
          "$x=3(1,1)+5(-1,1)=(3-5,\\ 3+5)=(-2,8)$, so $[x]_{\\text{standard}}=(-2,8)$. Wrong options: $(8,-2)=3(1,1)-5(-1,1)$ subtracts the second vector; $(2,8)=5(1,1)+3(-1,1)$ swaps the coefficients; $(3,5)$ just repeats $[x]_B$.", SUM + ", IV exercise 6", "src")
    b1, b2 = sp.Matrix([1, -1]), sp.Matrix([3, 1]); c1, c2 = sp.Matrix([1, 2]), sp.Matrix([-1, 0])
    Pb = sp.Matrix.hstack(b1, b2); Pc = sp.Matrix.hstack(c1, c2)
    T_BtoC = Pc.inv() * Pb                            # [v]_{B'} = (B' basis matrix)^-1 (B basis matrix) [v]_B
    assert T_BtoC == sp.Matrix([[sp.Rational(-1, 2), sp.Rational(1, 2)], [sp.Rational(-3, 2), sp.Rational(-5, 2)]])
    assert (Pb.inv() * Pc) == T_BtoC.inv()
    wrong = [T_BtoC.inv(), T_BtoC.T, -T_BtoC]
    assert len({str(w) for w in wrong + [T_BtoC]}) == 4
    B.mcq(ch, "Coordinates and change of basis", 3, "Find the transition matrix from $B=\\{(1,-1),(3,1)\\}$ to $B'=\\{(1,2),(-1,0)\\}$ (so that $[v]_{B'}=P[v]_B$).", mt(T_BtoC), mats(*wrong),
          "Row reduce $[B'\\,|\\,B]\\to[I\\,|\\,P]$, i.e. $P=(B')^{-1}B$ with the basis vectors as columns: $P=%s^{-1}%s=%s$. The matrix from $B'$ to $B$ is the inverse, $%s$." % (mtx(Pc), mtx(Pb), mtx(T_BtoC), mtx(T_BtoC.inv())), SUM + ", IV exercise 7", "src")

# ============================================================================== CHAPTER 5
def ch5(B):
    ch = "c5"
    rng = B.rng
    # <u,v> = u1v1 - 2u2v2 + u3v3 is not an inner product on R^3
    ip = lambda u, w: u[0] * w[0] - 2 * u[1] * w[1] + u[2] * w[2]
    for _ in range(200):
        u, w, z = [[rng.randint(-5, 5) for _ in range(3)] for _ in range(3)]; c = rng.randint(-4, 4)
        assert ip(u, w) == ip(w, u) and ip(u, [p + q for p, q in zip(w, z)]) == ip(u, w) + ip(u, z) and ip(u, [c * p for p in w]) == c * ip(u, w)
    assert ip([0, 1, 0], [0, 1, 0]) == -2
    B.mcq(ch, "Inner products", 2, "Why is $\\langle u,v\\rangle=u_1v_1-2u_2v_2+u_3v_3$ NOT an inner product on $\\mathbb{R}^3$?", "$\\langle u,u\\rangle$ can be negative, e.g. $\\langle(0,1,0),(0,1,0)\\rangle=-2$",
          ["it is not symmetric: $\\langle u,v\\rangle\\neq\\langle v,u\\rangle$", "it is not additive in the second argument", "it is not homogeneous: $\\langle u,cv\\rangle\\neq c\\langle u,v\\rangle$"],
          "Symmetry, additivity and homogeneity all hold (each term is a product of coordinates, symmetric in $u,v$). The positivity axiom $\\langle u,u\\rangle\\ge0$ fails because of the negative coefficient $-2$. "
          "In general $\\sum c_iu_iv_i$ is an inner product exactly when every $c_i>0$.", SUM + ", V.2 (inner product examples)", "src")
    # inner product on M_{2x2}: <A,B> = sum of products of entries
    Am, Bm = sp.Matrix([[1, 2], [0, -1]]), sp.Matrix([[3, -1], [2, 4]])
    ipm = lambda P, Q: sum(P[i, j] * Q[i, j] for i in range(2) for j in range(2))
    assert ipm(Am, Bm) == -3 and (Am.T * Bm).trace() == -3 and (Am * Bm).trace() == 3
    B.mcq(ch, "Inner products", 2, "On $M_{2\\times2}$ use $\\langle A,B\\rangle=a_{11}b_{11}+a_{12}b_{12}+a_{21}b_{21}+a_{22}b_{22}$. For $A=%s$ and $B=%s$, $\\langle A,B\\rangle=$" % (mtx(Am), mtx(Bm)), "$-3$", ["$3$", "$-6$", "$7$"],
          "Multiply entry by entry and add: $1\\cdot3+2\\cdot(-1)+0\\cdot2+(-1)\\cdot4=3-2+0-4=-3$ (this equals $\\operatorname{tr}(A^TB)$). Note that $\\operatorname{tr}(AB)=3$ is a different number.", SUM + ", V.2 (inner product on $M_{2,2}$)", "src")
    A3, B3 = sp.Matrix([[1, 1], [0, 0]]), sp.Matrix([[1, -1], [2, 5]])
    assert ipm(A3, B3) == 0 and A3 * B3 != sp.zeros(2) and ipm(A3, A3) != ipm(B3, B3)
    B.mcq(ch, "Inner products", 2, "With the entrywise inner product on $M_{2\\times2}$, are $A=%s$ and $B=%s$ orthogonal?" % (mtx(A3), mtx(B3)), "Yes: $\\langle A,B\\rangle=1\\cdot1+1\\cdot(-1)+0\\cdot2+0\\cdot5=0$",
          ["No: $AB\\neq0$, so they are not orthogonal", "No: $\\langle A,B\\rangle=1\\cdot1+1\\cdot1+0\\cdot2+0\\cdot5=2$", "No: they have different norms, so they are not orthogonal"],
          "Orthogonal means $\\langle A,B\\rangle=0$ for the chosen inner product. Here the sum is $1-1+0+0=0$. The matrix product $AB$ plays no role, and orthogonal vectors may have different lengths.", SUM + ", V.2 (inner product on $M_{2,2}$)", "src")
    # orthogonal sets are independent; n orthogonal nonzero vectors in an n-dimensional space form a basis
    S = sp.Matrix([[1, 1, 0], [1, -1, 0], [0, 0, 2]]).T
    G = S.T * S
    assert G.is_diagonal() and all(G[i, i] != 0 for i in range(3)) and S.rank() == 3
    B.mcq(ch, "Gram–Schmidt", 2, "Is $S=\\{(1,1,0),(1,-1,0),(0,0,2)\\}$ a basis of $\\mathbb{R}^3$?", "Yes: it is a set of $3$ non-zero, mutually orthogonal vectors in a $3$-dimensional space",
          ["No: a basis must contain the standard basis vectors", "No: the vectors have different lengths, so they are not independent", "Only if the three vectors are also unit vectors"],
          "The dot products are $(1,1,0)\\cdot(1,-1,0)=0$, $(1,1,0)\\cdot(0,0,2)=0$, $(1,-1,0)\\cdot(0,0,2)=0$. Non-zero orthogonal vectors are independent, and $n$ independent vectors in an $n$-dimensional space form a basis. (Unit length is needed only for an ORTHONORMAL basis.)", SUM + ", V.3 (orthogonal sets are independent)", "src")

# ============================================================================== CHAPTER 6
def ch6(B):
    ch = "c6"
    rng = B.rng
    e1, e2 = sp.Matrix([1, 0]), sp.Matrix([0, 1])
    rot90 = sp.Matrix.hstack(sp.Matrix([-e1[1], e1[0]]), sp.Matrix([-e2[1], e2[0]]))        # T(x, y) = (-y, x)
    assert rot90 == sp.Matrix([[0, -1], [1, 0]]) and rot90.T * rot90 == sp.eye(2) and rot90.det() == 1
    cw = rot90.T; refl = sp.Matrix([[0, 1], [1, 0]]); rot180 = -sp.eye(2)
    B.mcq(ch, "Standard matrix", 2, "The linear transformation of $\\mathbb{R}^2$ that rotates every vector counterclockwise by $90^\\circ$ has standard matrix", mt(rot90), mats(cw, refl, rot180),
          "The columns of the standard matrix are the images of $e_1=(1,0)$ and $e_2=(0,1)$: $T(e_1)=(0,1)$ and $T(e_2)=(-1,0)$, so $A=%s$, i.e. $T(x,y)=(-y,x)$. The clockwise rotation is its transpose; $%s$ is the reflection in the line $y=x$; $-I$ is the rotation by $180^\\circ$." % (mtx(rot90), mtx(refl)), "Lecture 6 (rotations)", "src")
    Pxy = sp.Matrix([[1, 1], [1, 1]]) / 2
    assert Pxy * Pxy == Pxy and Pxy.T == Pxy and Pxy * sp.Matrix([1, 1]) == sp.Matrix([1, 1]) and Pxy * sp.Matrix([1, -1]) == sp.zeros(2, 1) and Pxy * e1 == sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    projx = sp.Matrix([[1, 0], [0, 0]])
    B.mcq(ch, "Standard matrix", 3, "The orthogonal projection of $\\mathbb{R}^2$ onto the line $y=x$ is a linear map. Its standard matrix is", mt(Pxy), mats(sp.Matrix([[1, 1], [1, 1]]), projx, refl),
          "Project the standard basis vectors: $\\operatorname{proj}_{(1,1)}(1,0)=\\frac{(1,0)\\cdot(1,1)}{(1,1)\\cdot(1,1)}(1,1)=(\\frac12,\\frac12)$, and likewise for $(0,1)$. So $A=\\frac12\\begin{bmatrix}1&1\\\\1&1\\end{bmatrix}$. "
          "Check: $A^2=A$, $A(1,1)=(1,1)$ and $A(1,-1)=0$. Without the factor $\\frac12$ the matrix would send $(1,1)$ to $(2,2)$; $%s$ projects onto the $x$-axis." % mtx(projx), "Lecture 6 (projections)", "src")
    A1, A2 = rot90, projx                                   # T1 = rotation by 90 degrees, T2 = projection onto the x-axis
    comp = A2 * A1; other = A1 * A2
    assert comp == sp.Matrix([[0, -1], [0, 0]]) and other == sp.Matrix([[0, 0], [1, 0]]) and comp != other and len({str(m_) for m_ in (comp, other, A1 + A2, A1)}) == 4
    B.mcq(ch, "Composition", 2, "$T_1$ rotates $\\mathbb{R}^2$ by $90^\\circ$ counterclockwise and $T_2$ projects onto the $x$-axis. The standard matrix of $T_2\\circ T_1$ (first $T_1$, then $T_2$) is", mt(comp), mats(other, A1 + A2, A1),
          "$T_2\\circ T_1$ has matrix $A_2A_1$ (the map applied FIRST is on the right): $%s%s=%s$. Check on $e_1$: $T_1(e_1)=(0,1)$, then $T_2(0,1)=(0,0)$, and the first column of $A_2A_1$ is $(0,0)$. The product $A_1A_2=%s$ is the matrix of $T_1\\circ T_2$, which is different." % (mtx(A2), mtx(A1), mtx(comp), mtx(other)), SUM + ", VI.4 (composition is not commutative)", "src")
    for _ in range(200):                                    # square case: injective <=> surjective
        Ar = rand_mat(rng, 3, 3, -1, 1)
        assert (len(Ar.nullspace()) == 0) == (Ar.rank() == 3)
    B.mcq(ch, "One-to-one and onto", 2, "Let $T:V\\to W$ be linear with $\\dim V=\\dim W=n$. Then", "$T$ is one-to-one if and only if $T$ is onto",
          ["$T$ is always one-to-one but need not be onto", "$T$ is always onto but need not be one-to-one", "$T$ can be one-to-one only if $\\ker T=V$"],
          "By rank–nullity $\\operatorname{rank}T+\\operatorname{nullity}T=n$. One-to-one means nullity $0$, i.e. rank $n=\\dim W$, which is exactly onto. Example: $T(v)=Av$ with a $3\\times3$ matrix and $\\det A\\neq0$ is both. "
          "(This fails when the dimensions differ: $T(x,y)=(x,y,0)$ is one-to-one but not onto $\\mathbb{R}^3$.)", SUM + ", VI.3 (one-to-one versus onto)", "src")
    # similar matrices
    A = sp.Matrix([[2, -12], [1, -5]]); P = sp.Matrix([[1, 1], [0, 1]]); Ap = P.inv() * A * P
    assert Ap == sp.Matrix([[1, -6], [1, -4]])
    assert sorted(A.eigenvals()) == sorted(Ap.eigenvals()) == [-2, -1] and A.det() == Ap.det() == 2 and A.trace() == Ap.trace() == -3 and A.rank() == Ap.rank() == 2
    v_A = sp.Matrix([4, 1]); assert A * v_A == -v_A and Ap * v_A == sp.Matrix([-2, 0]) and P.inv() * v_A == sp.Matrix([3, 1]) and Ap * (P.inv() * v_A) == -(P.inv() * v_A)
    B.mcq(ch, "Similar matrices", 3, "$A'=P^{-1}AP$ for an invertible $P$ (similar matrices). Which of the following is NOT, in general, the same for $A$ and $A'$?", "the eigenvectors",
          ["the eigenvalues", "the determinant", "the trace"],
          "Similar matrices represent the same linear map in different bases, so eigenvalues, determinant, trace and rank are unchanged. Eigenvectors are coordinate vectors, so they change to $P^{-1}v$: if $Av=\\lambda v$ then $A'(P^{-1}v)=\\lambda(P^{-1}v)$. "
          "Example: $A=%s$, $P=%s$ give $A'=%s$; both have eigenvalues $-1,-2$, $\\det=2$ and trace $-3$, but $A(4,1)=-(4,1)$ while $A'(4,1)=(-2,0)$: the eigenvector of $A'$ is $P^{-1}(4,1)=(3,1)$." % (mtx(A), mtx(P), mtx(Ap)), SUM + ", VI.6 (similar matrices)", "src")
    note(SUM + ", IV.5", "The notes say 'S1 ⊆ S2: if S2 is linearly independent then S2 is linearly independent'. The second implication should read: if S2 is linearly independent then S1 (the subset) is linearly independent.")

# ============================================================================== CHAPTER 7
def ch7(B):
    ch = "c7"
    rng = B.rng
    A = sp.Matrix([[2, -12], [1, -5]])
    assert sorted(A.eigenvals()) == [-2, -1]
    lam = sp.Symbol("x")
    assert sp.expand(A.charpoly(lam).as_expr() - (lam + 1) * (lam + 2)) == 0
    assert A * sp.Matrix([4, 1]) == -sp.Matrix([4, 1]) and A * sp.Matrix([3, 1]) == -2 * sp.Matrix([3, 1])
    cand = [(-1, -2), (1, 2), (2, -5), (-3, 2)]
    lab = lambda p: "$\\lambda=%d$ and $\\lambda=%d$" % p
    assert sorted(cand[0]) == sorted(A.eigenvals()) and all(sorted(c_) != sorted(A.eigenvals()) for c_ in cand[1:])
    B.mcq(ch, "Eigenvalues", 2, "Find the eigenvalues of $A=%s$." % mtx(A), lab(cand[0]), [lab(c_) for c_ in cand[1:]],
          "$\\det(\\lambda I-A)=(\\lambda-2)(\\lambda+5)+12=\\lambda^2+3\\lambda+2=(\\lambda+1)(\\lambda+2)$, so $\\lambda=-1,-2$. Common slips: the signs of the roots ($1,2$), the diagonal entries ($2,-5$), and trace and determinant mixed up ($-3,2$).", SUM + ", III.5 exercise 3 (eigenvalues)", "src")
    others = [(4, 1), (-3, 1), (1, 3)]
    assert all(A * sp.Matrix(list(o)) != -2 * sp.Matrix(list(o)) for o in others)
    B.mcq(ch, "Eigenvectors", 2, "For $A=%s$, an eigenvector belonging to the eigenvalue $\\lambda=-2$ is" % mtx(A), V((3, 1)), [V(o) for o in others],
          "Solve $(\\lambda I-A)x=0$ with $\\lambda=-2$: $\\begin{bmatrix}-4&12\\\\-1&3\\end{bmatrix}x=0\\Rightarrow x_1=3x_2$, so $x=t(3,1)$. Check: $A(3,1)=(6-12,\\ 3-5)=(-6,-2)=-2(3,1)$. The vector $(4,1)$ belongs to $\\lambda=-1$.", SUM + ", III.5 exercise 3 (eigenvectors)", "src")
    others1 = [(3, 1), (1, 4), (-4, 1)]
    assert all(A * sp.Matrix(list(o)) != -sp.Matrix(list(o)) for o in others1)
    B.mcq(ch, "Eigenvectors", 2, "For $A=%s$, an eigenvector belonging to the eigenvalue $\\lambda=-1$ is" % mtx(A), V((4, 1)), [V(o) for o in others1],
          "$(\\lambda I-A)x=0$ with $\\lambda=-1$: $\\begin{bmatrix}-3&12\\\\-1&4\\end{bmatrix}x=0\\Rightarrow x_1=4x_2$, so $x=t(4,1)$. Check: $A(4,1)=(8-12,\\ 4-5)=(-4,-1)=-(4,1)$.", SUM + ", III.5 exercise 3 (eigenvectors)", "src")
    # distinct eigenvalues -> diagonalizable (sufficient, not necessary)
    A3 = sp.Matrix([[1, 1, 0], [0, 2, 1], [0, 0, 3]]); assert len(A3.eigenvals()) == 3 and A3.is_diagonalizable()
    I3 = sp.eye(3); assert I3.is_diagonalizable() and len(I3.eigenvals()) == 1
    J = sp.Matrix([[1, 1], [0, 1]]); assert not J.is_diagonalizable() and len(J.eigenvals()) == 1
    B.mcq(ch, "Diagonalization", 2, "An $n\\times n$ matrix has $n$ distinct eigenvalues. What follows?", "it is diagonalizable; the converse is false (e.g. $I_3$ is diagonalizable with the single eigenvalue $1$)",
          ["it may fail to be diagonalizable, as $\\begin{bmatrix}1&1\\\\0&1\\end{bmatrix}$ does", "it is diagonalizable only if it is symmetric", "it is diagonalizable if and only if its eigenvalues are distinct"],
          "Eigenvectors of distinct eigenvalues are linearly independent, so $n$ distinct eigenvalues give $n$ independent eigenvectors: a sufficient condition. It is not necessary: $I_3$ has one repeated eigenvalue but is diagonalizable, whereas $\\begin{bmatrix}1&1\\\\0&1\\end{bmatrix}$ (repeated eigenvalue, only one eigenvector direction) is not.", SUM + ", VII.2 (sufficient condition)", "src")
    # symmetric matrices
    for _ in range(300):
        S = np.array([[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)], dtype=float); S = S + S.T
        w, Vv = np.linalg.eig(S)
        if abs(np.linalg.det(Vv)) < 1e-9:       # repeated eigenvalue with numerically parallel eigenvectors: skip the numeric test (theory still guarantees diagonalizability)
            continue
        assert np.allclose(w.imag, 0)                                                        # real eigenvalues
        if min(abs(w[i] - w[j]) for i in range(3) for j in range(i)) > 1e-6:                 # distinct eigenvalues -> orthogonal eigenvectors
            assert np.allclose(Vv.T @ Vv, np.eye(3), atol=1e-8)
    Zs = sp.Matrix([[0, 1], [1, 0]]); assert any(l_ < 0 for l_ in Zs.eigenvals()) and Zs == Zs.T
    B.mcq(ch, "Diagonalization", 2, "Which statement about a real symmetric matrix $A$ is TRUE?", "eigenvectors belonging to different eigenvalues are orthogonal",
          ["some eigenvalues may be complex numbers", "all eigenvalues are positive", "it may fail to be diagonalizable"],
          "For a real symmetric matrix: all eigenvalues are real, $A$ is (orthogonally) diagonalizable, and eigenvectors of distinct eigenvalues are orthogonal. Eigenvalues need not be positive: $\\begin{bmatrix}0&1\\\\1&0\\end{bmatrix}$ has eigenvalues $1$ and $-1$.", SUM + ", VII.3 (symmetric matrices)", "src")
    # which matrix is orthogonal?
    Q = sp.Matrix([[3, -4], [4, 3]]) / 5
    assert Q.T * Q == sp.eye(2) and Q.det() == 1
    others = [sp.Matrix([[1, 1], [1, -1]]), sp.Matrix([[3, 4], [4, 3]]) / 5, sp.Matrix([[1, 0], [1, 1]])]
    assert all(o.T * o != sp.eye(2) for o in others) and others[0].T * others[0] == 2 * sp.eye(2)
    B.mcq(ch, "Orthogonal matrices", 2, "Which of these matrices is orthogonal (i.e. $P^{-1}=P^T$)?", mt(Q), mats(*others),
          "A matrix is orthogonal exactly when its columns are orthonormal. For $%s$ both columns have length $\\sqrt{(9+16)/25}=1$ and their dot product is $\\frac{1}{25}(3\\cdot(-4)+4\\cdot3)=0$. "
          "$%s$ has orthogonal but non-unit columns ($P^TP=2I$); $%s$ has unit but non-orthogonal columns; the last one has neither." % (mtx(Q), mtx(others[0]), mtx(others[1])), SUM + ", VII.3 (orthogonal matrices)", "src")
