# -*- coding: utf-8 -*-
"""Linear Algebra gap-fill pool: questions for the concepts that the Concept finder reported as thin (linear equation, rank, adjugate, invertibility,
orthogonal matrices, matrix of a map relative to bases and similarity, Gram-Schmidt and least squares).
A separate Bank (ids of kind 'g', tag 'gap') merged after the main bank: the ids and option order of the existing questions do not move and the fixed quizzes
and mock exams keep their questions; the new ones live in the practice bank, the random quizzes and one extra set per chapter.
Every answer is computed with exact sympy arithmetic and every wrong option is verified to be wrong."""
import sympy as sp
from qlib import Bank, tex, M, vec, uniq_by_text
from la_common import *
from la_steps import mtx
from gen_la1 import mt

TAG = ("gap",)
def GAP(topic): return "Generated to fill a gap: " + topic

def mcq(B, ch, topic, level, stem, correct, wrongs, explain, origin="gen"):
    ok = B.mcq(ch, topic, level, stem, correct, wrongs, explain, GAP(topic), origin, TAG)
    assert ok, "question not added (duplicate or too few distinct distractors): " + stem[:80]
    return ok

x, y, z, s, r = sp.symbols("x y z s r")

def is_linear(e):
    return e.is_polynomial(x, y, z) and sp.Poly(sp.expand(e), x, y, z).total_degree() <= 1

# =============================================================================================== chapter 1
def linear_equations(B):
    ch, t = "c1", "Linear equations"
    good = 2 * x - 3 * y + z - 5; bad = [x * y + z - 1, x ** 2 + y + z, sp.sin(x) + y - 2]
    assert is_linear(good) and not any(is_linear(e) for e in bad)
    mcq(B, ch, t, 1, "Which of the following is a linear equation in $x,\\ y,\\ z$?", "$2x-3y+z=5$", ["$xy+z=1$", "$x^2+y+z=0$", "$\\sin x+y=2$"],
        "A linear equation has the form $a_1x_1+\\dots+a_nx_n=b$: every unknown appears to the first power, alone (no products of unknowns, no powers, no functions such as $\\sin x$). Only $2x-3y+z=5$ has that form.")
    e1 = 2 * x - y + 3 * z - 6
    assert sp.Matrix([[2, -1, 3]]).rank() == 1 and 3 - 1 == 2
    mcq(B, ch, t, 2, "How many free parameters are needed to describe all solutions of the single equation $2x-y+3z=6$ in the unknowns $x,\\ y,\\ z$?",
        "Two: the solutions form a plane in $\\mathbb R^3$", ["One: they form a line", "Three: every point of $\\mathbb R^3$ is a solution", "None: the equation has exactly one solution"],
        "One equation is one pivot: the rank is $1$, so there are $3-1=2$ free variables (for instance $y=s$, $z=t$ and $x=\\tfrac12(6+s-3t)$). The solution set is a plane.")
    eq = x + 2 * y - z - 4
    gen_ok = (4 - 2 * s + r, s, r)
    wr = [(4 + 2 * s + r, s, r), (4 - 2 * s - r, s, r), (4 - 2 * s + r, s, -r)]
    assert sp.expand(eq.subs({x: gen_ok[0], y: gen_ok[1], z: gen_ok[2]})) == 0
    assert all(sp.expand(eq.subs({x: w[0], y: w[1], z: w[2]})) != 0 for w in wr)
    mcq(B, ch, t, 2, "Which is the general solution of the single equation $x+2y-z=4$ (with $s,\\ r\\in\\mathbb R$)?", "$(4-2s+r,\\ s,\\ r)$",
        ["$(4+2s+r,\\ s,\\ r)$", "$(4-2s-r,\\ s,\\ r)$", "$(4-2s+r,\\ s,\\ -r)$"],
        "Solve for the leading unknown: $x=4-2y+z$. Put $y=s$, $z=r$: $(x,y,z)=(4-2s+r,\\ s,\\ r)$. Check: $(4-2s+r)+2s-r=4$ for every $s,r$. The other triples fail this check (a sign slip in $y$ or $z$).")
    ks = sp.symbols("kk"); sol = sp.solve(3 * 1 - 2 + 2 * ks - 7, ks)
    assert sol == [3]
    mcq(B, ch, t, 2, "For which value of $k$ is $(1,\\ 2,\\ k)$ a solution of $3x-y+2z=7$?", "$k=3$", ["$k=1$", "$k=6$", "$k=4$"],
        "Substitute: $3(1)-2+2k=7\\Rightarrow 1+2k=7\\Rightarrow k=3$. ($k=1$ comes from using $+y$; $k=4$ from forgetting to multiply $x$ by 3; $k=6$ from forgetting the factor 2 of $z$.)")
    pt = (2, -1, 3)
    eqs = {"$2x+y-z=0$": 2 * pt[0] + pt[1] - pt[2], "$x+y+z=0$": pt[0] + pt[1] + pt[2], "$x-y+z=0$": pt[0] - pt[1] + pt[2], "$3x+y-z=0$": 3 * pt[0] + pt[1] - pt[2]}
    assert [k_ for k_, v in eqs.items() if v == 0] == ["$2x+y-z=0$"]
    mcq(B, ch, t, 1, "Which equation has $(2,\\ -1,\\ 3)$ as a solution?", "$2x+y-z=0$", ["$x+y+z=0$", "$x-y+z=0$", "$3x+y-z=0$"],
        "Substitute $(x,y,z)=(2,-1,3)$: $2x+y-z=4-1-3=0$ \\checkmark. The others give $4$, $6$ and $2$.")
    for a_, b_ in [(0, 1), (1, 0)]:
        assert sp.solve(a_ * x + b_ * y - 1, [x, y], dict=True)
    assert sp.solve(0 * x + 0 * y - 1, [x, y], dict=True) == [] and sp.solve(2 * x + 3 * y - 0, [x, y], dict=True)
    mcq(B, ch, t, 3, "For which coefficients does the equation $ax+by=c$ (in the unknowns $x,\\ y$) have NO solution?", "$a=b=0$ and $c\\neq0$",
        ["$a=0$ and $b\\neq0$", "$c=0$", "$a\\neq0$ and $b\\neq0$"],
        "If $a=b=0$ the equation reads $0=c$: impossible when $c\\neq0$. If $a=0,\\ b\\neq0$ then $y=c/b$ (a line of solutions); if $c=0$ then $(0,0)$ works; if $a,b\\neq0$ the solutions form a line.")
    Asys = sp.Matrix([[2, -1], [4, -2]]); bsys = sp.Matrix([3, 6])
    assert Asys.rank() == 1 and Asys.row_join(bsys).rank() == 1
    mcq(B, ch, t, 2, "The system $2x-y=3,\\ 4x-2y=6$ has", "infinitely many solutions (both equations describe the same line)", ["exactly one solution", "no solution", "exactly two solutions"],
        "The second equation is twice the first, so after one row operation it becomes $0=0$. Rank $A=$ rank $[A|b]=1<2$ unknowns: one free variable, hence a whole line of solutions.")

def rank_questions(B):
    ch, t = "c1", "Rank"
    A1 = sp.Matrix([[1, 2, 3], [2, 4, 6], [1, 0, 1]]); assert A1.rank() == 2
    mcq(B, ch, t, 1, "What is the rank of $A=%s$?" % mtx(A1), "$2$", ["$3$", "$1$", "$0$"],
        "Row 2 is twice row 1, so after $-2R_1+R_2\\to R_2$ it becomes zero. Rows 1 and 3 are not multiples of each other, so two non-zero rows remain: rank $A=2$. (Counting the non-zero rows BEFORE reducing would give $3$.)")
    A2 = sp.Matrix([[1, 2, 0, 1], [0, 1, 1, 2], [1, 3, 1, 3]]); assert A2[2, :] == A2[0, :] + A2[1, :] and A2.rank() == 2
    mcq(B, ch, t, 2, "What is the rank of $A=%s$?" % mtx(A2), "$2$", ["$3$", "$1$", "$4$"],
        "Row 3 equals row 1 plus row 2 ($R_1+R_2=(1,3,1,3)$), so $-R_1-R_2+R_3\\to R_3$ gives a zero row. Rows 1 and 2 are independent: rank $A=2$. The rank can never exceed the number of rows ($3$).")
    mcq(B, ch, t, 2, "What is the largest possible rank of a $4\\times6$ matrix?", "$4$", ["$6$", "$10$", "$24$"],
        "$\\operatorname{rank}A\\le\\min(m,n)$: at most one pivot per row and one per column, so for $4\\times6$ the rank is at most $4$.")
    mcq(B, ch, t, 2, "A system $A\\mathbf x=\\mathbf b$ in $n$ unknowns has $\\operatorname{rank}A=\\operatorname{rank}[A|\\mathbf b]=n$. Then the system has", "exactly one solution",
        ["infinitely many solutions", "no solution", "either none or infinitely many, depending on $\\mathbf b$"],
        "Equal ranks mean the system is consistent; rank $=n$ means no free variable. So the solution is unique. (Rank $A<$ rank $[A|b]$ would mean no solution; rank $<n$ means infinitely many.)")
    A3 = sp.Matrix([[1, 1, 1, 1], [0, 1, 2, 3], [1, 2, 3, 4]]); b3 = sp.Matrix([1, 2, 3])
    assert A3[2, :] == A3[0, :] + A3[1, :] and b3[2] == b3[0] + b3[1] and A3.rank() == 2 and A3.row_join(b3).rank() == 2
    mcq(B, ch, t, 3, "The system $A\\mathbf x=\\mathbf b$ with $[A\\,|\\,\\mathbf b]=%s$ is consistent. How many free parameters does its solution set have?" % mtx(A3.row_join(b3), 4), "$2$", ["$1$", "$3$", "$0$"],
        "Row 3 $=$ row 1 $+$ row 2 on both sides, so it reduces to $0=0$: rank $A=$ rank $[A|b]=2$. With $4$ unknowns, the number of free parameters is $n-\\operatorname{rank}A=4-2=2$.")
    Ak = sp.Matrix([[1, 1, 1], [1, 2, k], [1, 4, k ** 2]])
    assert sp.factor(Ak.det()) == (k - 1) * (k - 2) and Ak.subs(k, 1).rank() == 2 and Ak.subs(k, 2).rank() == 2 and Ak.subs(k, 0).rank() == 3
    ct, wr = set_options([1, 2], [1, 2], k, B.rng)
    mcq(B, ch, t, 3, "For which values of $k$ is the rank of $A=%s$ less than $3$?" % mtx(Ak), ct, wr,
        "A $3\\times3$ matrix has rank $<3$ exactly when it is singular. Here $\\det A=(k-1)(k-2)$ (Vandermonde-type), so the rank drops at $k=1$ and $k=2$; for those values the rows are dependent (rank $2$) and for every other $k$ the rank is $3$.")
    mcq(B, ch, t, 2, "For every matrix $A$, the rank of $A^T$ is", "equal to the rank of $A$ (row rank = column rank)", ["the number of rows of $A$", "always $\\operatorname{rank}A-1$", "$\\min(m,n)$"],
        "The number of independent rows equals the number of independent columns, so $\\operatorname{rank}A^T=\\operatorname{rank}A$. The rank is the number of pivots, not the size of the matrix.")
    A4 = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]]); B4 = sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    assert A4.rank() == 2 and B4.rank() == 3 and (A4 * B4).rank() == 2
    mcq(B, ch, t, 3, "$A$ and $B$ are $3\\times3$ matrices with $\\operatorname{rank}A=2$ and $B$ invertible. What is $\\operatorname{rank}(AB)$?", "$2$", ["$3$", "$1$", "$5$"],
        "Multiplying by an invertible matrix does not change the rank: $\\operatorname{rank}(AB)=\\operatorname{rank}A=2$. In general $\\operatorname{rank}(AB)\\le\\min(\\operatorname{rank}A,\\operatorname{rank}B)$, so it can never be $3$ here. Example: $A=\\operatorname{diag}(1,1,0)$ and $B=%s$ give $\\operatorname{rank}(AB)=2$." % mtx(B4))

# =============================================================================================== chapter 3
def adjugate_questions(B):
    ch, t = "c3", "Adjugate"
    A = sp.Matrix([[3, 1], [5, 2]]); adj = A.adjugate(); C = A.cofactor_matrix()
    assert adj == sp.Matrix([[2, -1], [-5, 3]]) and A * adj == A.det() * sp.eye(2) and C == adj.T
    wr = [sp.Matrix([[2, 1], [5, 3]]), sp.Matrix([[3, -1], [-5, 2]]), C]
    assert all(w != adj for w in wr)
    mcq(B, ch, t, 1, "What is $\\operatorname{adj}(A)$ for $A=%s$?" % mtx(A), mt(adj), [mt(w) for w in wr],
        "For a $2\\times2$ matrix swap the diagonal entries and change the signs of the off-diagonal entries: $\\operatorname{adj}\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}=\\begin{bmatrix}d&-b\\\\-c&a\\end{bmatrix}$. "
        "Here $\\operatorname{adj}(A)=%s$; check $A\\operatorname{adj}(A)=(\\det A)I=I$. The matrix $%s$ is the cofactor matrix: the adjugate is its TRANSPOSE." % (mtx(adj), mtx(C)))
    A3 = sp.Matrix([[1, 2, 0], [0, 1, 3], [2, 0, 1]]); e = A3.adjugate()[0, 1]
    assert e == A3.cofactor(1, 0) == -2 and A3.cofactor(0, 1) == 6 and A3.minor(1, 0) == 2
    mcq(B, ch, t, 2, "For $A=%s$, what is the $(1,2)$ entry of $\\operatorname{adj}(A)$?" % mtx(A3), "$-2$", ["$6$", "$2$", "$-6$"],
        "The adjugate is the transpose of the cofactor matrix, so $[\\operatorname{adj}A]_{12}=C_{21}=(-1)^{2+1}\\det\\begin{bmatrix}2&0\\\\0&1\\end{bmatrix}=-2$. "
        "$C_{12}=6$ is the entry of the cofactor matrix itself (transposition forgotten) and $2$ is the minor without its sign.")
    assert (A3 * A3.adjugate()) == A3.det() * sp.eye(3)
    mcq(B, ch, t, 2, "$A$ is a $3\\times3$ matrix with $\\det A=5$. Then $A\\cdot\\operatorname{adj}(A)$ equals", "$5I$", ["$5A$", "$\\tfrac15 I$", "$\\operatorname{adj}(A)/5$"],
        "The defining property of the adjugate is $A\\operatorname{adj}(A)=\\operatorname{adj}(A)A=(\\det A)\\,I$. It follows that $A^{-1}=\\dfrac{1}{\\det A}\\operatorname{adj}(A)$ when $\\det A\\neq0$.")
    A4 = sp.Matrix([[2, 1], [4, 3]]); inv = A4.inv(); assert inv == A4.adjugate() / A4.det() == sp.Matrix([[sp.Rational(3, 2), -sp.Rational(1, 2)], [-2, 1]])
    wrs = [A4.adjugate(), 2 * A4.adjugate(), sp.Matrix([[sp.Rational(3, 2), -2], [-sp.Rational(1, 2), 1]])]
    assert all(w != inv for w in wrs)
    mcq(B, ch, t, 2, "Use the adjugate to find $A^{-1}$ for $A=%s$." % mtx(A4), mt(inv), [mt(w) for w in wrs],
        "$\\det A=2(3)-1(4)=2$ and $\\operatorname{adj}(A)=%s$. So $A^{-1}=\\dfrac1{\\det A}\\operatorname{adj}(A)=\\tfrac12%s=%s$. Forgetting the factor $1/\\det A$ gives $\\operatorname{adj}(A)$ itself." % (mtx(A4.adjugate()), mtx(A4.adjugate()), mtx(inv)))
    D = sp.diag(2, 2, 1); assert D.det() == 4 and D.adjugate().det() == 16 == D.det() ** 2
    mcq(B, ch, t, 3, "$A$ is a $3\\times3$ matrix with $\\det A=4$. What is $\\det\\big(\\operatorname{adj}(A)\\big)$?", "$16$", ["$4$", "$64$", "$12$"],
        "From $A\\operatorname{adj}(A)=(\\det A)I$ take determinants: $\\det A\\cdot\\det(\\operatorname{adj}A)=(\\det A)^3$, so $\\det(\\operatorname{adj}A)=(\\det A)^{n-1}=4^2=16$. Check with $A=\\operatorname{diag}(2,2,1)$: $\\operatorname{adj}A=\\operatorname{diag}(2,2,4)$, determinant $16$.")
    Ar = sp.Matrix([[1, 2, 0], [0, 1, 3], [2, 0, 1]])
    assert (2 * Ar).adjugate() == 4 * Ar.adjugate() != 2 * Ar.adjugate() and (2 * Ar).adjugate() != 8 * Ar.adjugate()
    mcq(B, ch, t, 3, "$A$ is a $3\\times3$ matrix. Then $\\operatorname{adj}(2A)$ equals", "$4\\operatorname{adj}(A)$", ["$2\\operatorname{adj}(A)$", "$8\\operatorname{adj}(A)$", "$\\tfrac12\\operatorname{adj}(A)$"],
        "Each cofactor of $2A$ is a $2\\times2$ determinant of entries that are all doubled, so it is multiplied by $2^2=4$: $\\operatorname{adj}(kA)=k^{n-1}\\operatorname{adj}(A)$ with $n=3$. (Compare $\\det(2A)=2^3\\det A$.)")
    S = sp.Matrix([[1, 2], [2, 4]]); assert S.det() == 0 and S * S.adjugate() == sp.zeros(2)
    mcq(B, ch, t, 2, "If $A$ is a square matrix with $\\det A=0$, then $A\\cdot\\operatorname{adj}(A)$ is", "the zero matrix", ["the identity matrix", "$A$ itself", "$\\operatorname{adj}(A)$"],
        "$A\\operatorname{adj}(A)=(\\det A)I=0\\cdot I=0$. Example: $A=%s$, $\\operatorname{adj}A=%s$ and $A\\operatorname{adj}A=%s$." % (mtx(S), mtx(S.adjugate()), mtx(S * S.adjugate())))
    Dg = sp.diag(2, 3, 5); aD = Dg.adjugate(); assert aD == sp.diag(15, 10, 6)
    wrd = [Dg, sp.diag(sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 5)), sp.diag(30, 30, 30)]
    mcq(B, ch, t, 3, "What is $\\operatorname{adj}(A)$ for $A=\\operatorname{diag}(2,3,5)$?", mt(aD), [mt(w) for w in wrd],
        "For a diagonal matrix the cofactor $C_{ii}$ is the product of the OTHER diagonal entries: $3\\cdot5=15$, $2\\cdot5=10$, $2\\cdot3=6$. So $\\operatorname{adj}A=\\operatorname{diag}(15,10,6)$, and $A\\operatorname{adj}A=30I$ since $\\det A=30$. ($\\operatorname{diag}(\\tfrac12,\\tfrac13,\\tfrac15)$ is the inverse, not the adjugate.)")
    Q = sp.Matrix([[1, 3], [2, 5]]); assert Q.adjugate().adjugate() == Q
    mcq(B, ch, t, 3, "$A$ is any $2\\times2$ matrix. Then $\\operatorname{adj}\\big(\\operatorname{adj}(A)\\big)$ equals", "$A$", ["$A^{-1}$", "$\\det(A)\\,A$", "$A^{T}$"],
        "For $2\\times2$ matrices $\\operatorname{adj}$ swaps the diagonal and flips the off-diagonal signs; doing it twice returns the original matrix. (In general $\\operatorname{adj}(\\operatorname{adj}A)=(\\det A)^{n-2}A$, which is $A$ for $n=2$.)")
    t = "Invertibility"
    mcq(B, ch, t, 2, "Which condition is NOT equivalent to the invertibility of an $n\\times n$ matrix $A$?", "$A$ is symmetric", ["$\\operatorname{rank}A=n$", "$A\\mathbf x=\\mathbf 0$ has only the trivial solution", "the columns of $A$ are linearly independent"],
        "Invertible $\\iff$ rank $n$ $\\iff$ only the trivial solution of $A\\mathbf x=\\mathbf 0$ $\\iff$ independent columns. Symmetry has nothing to do with it: $%s$ is symmetric and singular." % mtx(sp.Matrix([[1, 1], [1, 1]])))
    Cands = {"$%s$" % mtx(m_): m_ for m_ in (sp.Matrix([[1, 2], [2, 4]]), sp.Matrix([[1, 2], [3, 4]]), sp.Matrix([[0, 0], [1, 2]]), sp.Matrix([[1, 1], [1, 1]]))}
    inv_ones = [k_ for k_, m_ in Cands.items() if m_.rank() == 2]; assert inv_ones == ["$%s$" % mtx(sp.Matrix([[1, 2], [3, 4]]))]
    mcq(B, ch, t, 2, "Which of these matrices is invertible?", inv_ones[0], [k_ for k_ in Cands if k_ != inv_ones[0]],
        "A $2\\times2$ matrix is invertible exactly when its determinant (equivalently the rank test) is non-zero: $\\det\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}=-2\\neq0$. The others have a row that is a multiple of another row or a zero row (determinant $0$, rank $<2$).")
    N = sp.Matrix([[0, 1], [0, 0]]); assert N * N == sp.zeros(2) and N != sp.zeros(2) and N.rank() < 2
    mcq(B, ch, t, 3, "$A$ is a non-zero square matrix with $A^2=0$. Then $A$ is", "not invertible", ["invertible, with $A^{-1}=A$", "invertible, with $A^{-1}=-A$", "invertible only if $A$ is symmetric"],
        "If $A$ were invertible, multiplying $A^2=0$ by $A^{-2}$ would give $I=0$, impossible. So $A$ is singular. Example: $A=%s$ has $A^2=0$." % mtx(N))

# =============================================================================================== chapter 5
def inner_product_questions(B):
    ch, t = "c5", "Gram–Schmidt"
    v1, v2 = sp.Matrix([1, 1, 0]), sp.Matrix([1, 0, 1])
    u1 = v1; u2 = v2 - (v2.dot(u1) / u1.dot(u1)) * u1
    assert list(u2) == [sp.Rational(1, 2), -sp.Rational(1, 2), 1] and u1.dot(u2) == 0
    wr = [sp.Matrix([0, -1, 1]), sp.Matrix([sp.Rational(3, 2), sp.Rational(1, 2), 1]), sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2), 1])]
    assert all(u1.dot(w) != 0 for w in wr)
    mcq(B, ch, t, 2, "Apply Gram-Schmidt to $\\mathbf v_1=(1,1,0)$ and $\\mathbf v_2=(1,0,1)$ with $\\mathbf u_1=\\mathbf v_1$. What is $\\mathbf u_2$?", "$%s$" % vec(list(u2)), ["$%s$" % vec(list(w)) for w in wr],
        "$\\mathbf u_2=\\mathbf v_2-\\dfrac{\\mathbf v_2\\cdot\\mathbf u_1}{\\mathbf u_1\\cdot\\mathbf u_1}\\mathbf u_1=(1,0,1)-\\dfrac12(1,1,0)=(\\tfrac12,-\\tfrac12,1)$. Check: $\\mathbf u_2\\cdot\\mathbf u_1=\\tfrac12-\\tfrac12=0$. "
        "The other vectors are not orthogonal to $\\mathbf u_1$ (a wrong projection coefficient or a sign error).")
    e2 = u2 / u2.norm(); assert sp.simplify(e2.norm() - 1) == 0 and sp.simplify(e2 - sp.Matrix([1, -1, 2]) / sp.sqrt(6)) == sp.zeros(3, 1)
    wr2 = [sp.Matrix([1, -1, 2]) / sp.sqrt(3), u2, sp.Matrix([1, -1, 1]) / sp.sqrt(3)]
    assert all(sp.simplify(w.norm() - 1) != 0 for w in wr2[:2]) and sp.simplify(wr2[2].norm() - 1) == 0 and sp.simplify(wr2[2].dot(u1)) == 0 and wr2[2].cross(u2) != sp.zeros(3, 1)
    mcq(B, ch, t, 2, "After Gram-Schmidt, $\\mathbf u_2=(\\tfrac12,-\\tfrac12,1)$. Which vector is the orthonormal vector $\\mathbf e_2$ in the same direction?", "$\\dfrac1{\\sqrt6}(1,-1,2)$",
        ["$\\dfrac1{\\sqrt3}(1,-1,2)$", "$(\\tfrac12,-\\tfrac12,1)$ itself", "$\\dfrac1{\\sqrt3}(1,-1,1)$"],
        "$\\|\\mathbf u_2\\|=\\sqrt{\\tfrac14+\\tfrac14+1}=\\sqrt{3/2}$, so $\\mathbf e_2=\\dfrac{\\mathbf u_2}{\\|\\mathbf u_2\\|}=\\sqrt{\\tfrac23}(\\tfrac12,-\\tfrac12,1)=\\dfrac1{\\sqrt6}(1,-1,2)$ (length $1$). $\\mathbf u_2$ itself is orthogonal to $\\mathbf u_1$ but not a unit vector, and $(1,-1,1)/\\sqrt3$ has length $1$ but points in the wrong direction.")
    t = "Least squares"
    X = sp.Matrix([[1, 0], [1, 1], [1, 2]]); yv = sp.Matrix([1, 2, 2]); ab = (X.T * X).solve(X.T * yv)
    assert list(ab) == [sp.Rational(7, 6), sp.Rational(1, 2)]
    mcq(B, ch, t, 3, "Find the least-squares line $y=a+bx$ for the data points $(0,1),\\ (1,2),\\ (2,2)$.", "$y=\\tfrac76+\\tfrac12x$", ["$y=1+\\tfrac12x$", "$y=\\tfrac76+x$", "$y=\\tfrac53+\\tfrac12x$"],
        "Normal equations $X^TX\\begin{bmatrix}a\\\\b\\end{bmatrix}=X^T\\mathbf y$ with $X=%s$, $\\mathbf y=(1,2,2)$: $%s\\begin{bmatrix}a\\\\b\\end{bmatrix}=%s$, so $a=\\tfrac76$, $b=\\tfrac12$. "
        "The line through the first and last points ($y=1+\\tfrac12x$) fits two points exactly but is not the best fit overall." % (mtx(X), mtx(X.T * X), mtx(X.T * yv)))
    mcq(B, ch, t, 2, "The least-squares solution of an inconsistent system $A\\mathbf x=\\mathbf b$ is the solution of", "$A^TA\\,\\mathbf x=A^T\\mathbf b$", ["$AA^T\\mathbf x=\\mathbf b$", "$A^T\\mathbf x=A^T\\mathbf b$", "$A\\mathbf x=A^T\\mathbf b$"],
        "The residual $\\mathbf b-A\\mathbf x$ must be orthogonal to the column space of $A$, i.e. $A^T(\\mathbf b-A\\mathbf x)=\\mathbf 0$, which gives the normal equations $A^TA\\mathbf x=A^T\\mathbf b$.")

# =============================================================================================== chapter 6
def map_questions(B):
    ch, t = "c6", "Matrix relative to bases"
    A = sp.Matrix([[1, 1], [2, -1]]); P = sp.Matrix([[1, 1], [1, -1]]); TB = P.inv() * A * P
    assert TB == sp.Matrix([[sp.Rational(3, 2), sp.Rational(3, 2)], [sp.Rational(1, 2), -sp.Rational(3, 2)]])
    wr = [TB.T, A * P, P.inv() * A]          # P A P^-1 would equal P^-1 A P here (P^2 = 2I), so it cannot be a distractor
    assert all(w != TB for w in wr)
    mcq(B, ch, t, 3, "$T(x,y)=(x+y,\\ 2x-y)$. What is the matrix of $T$ relative to the basis $B=\\{(1,1),\\ (1,-1)\\}$ (in both domain and codomain)?", mt(TB), [mt(w) for w in wr],
        "Column $j$ of $[T]_B$ is the $B$-coordinate vector of $T(\\mathbf b_j)$. $T(1,1)=(2,1)=\\tfrac32(1,1)+\\tfrac12(1,-1)$ and $T(1,-1)=(0,3)=\\tfrac32(1,1)-\\tfrac32(1,-1)$, so $[T]_B=%s$. "
        "Equivalently $[T]_B=P^{-1}AP$ with $P=%s$. The matrix $AP=%s$ lists the images in STANDARD coordinates." % (mtx(TB), mtx(P), mtx(A * P)))
    A2 = sp.Matrix([[1, 0], [0, 0]]); PB = P.inv() * A2 * P
    assert PB == sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)], [sp.Rational(1, 2), sp.Rational(1, 2)]])
    wr2 = [A2, sp.Matrix([[1, 1], [1, 1]]), sp.Matrix([[sp.Rational(1, 2), -sp.Rational(1, 2)], [-sp.Rational(1, 2), sp.Rational(1, 2)]])]
    assert all(w != PB for w in wr2)
    mcq(B, ch, t, 3, "$T$ is the projection onto the $x$-axis, $T(x,y)=(x,0)$. What is its matrix relative to the basis $B=\\{(1,1),\\ (1,-1)\\}$?", mt(PB), [mt(w) for w in wr2],
        "$T(1,1)=(1,0)=\\tfrac12(1,1)+\\tfrac12(1,-1)$ and $T(1,-1)=(1,0)=\\tfrac12(1,1)+\\tfrac12(1,-1)$. So both columns of $[T]_B$ are $(\\tfrac12,\\tfrac12)$: $[T]_B=%s$. The standard matrix $%s$ describes the same map in different coordinates." % (mtx(PB), mtx(A2)))
    mcq(B, ch, t, 2, "The columns of the matrix $[T]_B$ of a linear map $T$ relative to a basis $B=\\{\\mathbf b_1,\\dots,\\mathbf b_n\\}$ are", "the coordinate vectors $[T(\\mathbf b_j)]_B$ of the images of the basis vectors",
        ["the vectors $T(\\mathbf b_j)$ written in the standard basis", "the coordinate vectors $[\\mathbf b_j]_B$ of the basis vectors themselves", "the images $T(\\mathbf e_j)$ of the standard basis vectors"],
        "Apply $T$ to each basis vector and express the result in the SAME basis $B$: those coordinate vectors are the columns. (The coordinate vectors of $\\mathbf b_j$ themselves are just the columns of the identity matrix.)")
    D = sp.diag(2, 3); Pm = sp.Matrix([[1, 1], [0, 1]]); Asim = Pm * D * Pm.inv()
    assert Asim == sp.Matrix([[2, 1], [0, 3]])
    wr3 = [Pm.inv() * D * Pm, D * Pm, Pm * D]
    assert all(w != Asim for w in wr3) and len({tuple(w) for w in wr3 + [Asim]}) == 4
    t = "Similar matrices"
    mcq(B, ch, t, 2, "$A=PBP^{-1}$ with $B=\\operatorname{diag}(2,3)$ and $P=%s$. What is $A$?" % mtx(Pm), mt(Asim), [mt(w) for w in wr3],
        "$A=PBP^{-1}=%s\\operatorname{diag}(2,3)%s=%s$. The ORDER matters: $P^{-1}BP=%s$ is a different matrix, and $PB$ or $BP$ alone are not similar to $B$ in general." % (mtx(Pm), mtx(Pm.inv()), mtx(Asim), mtx(Pm.inv() * D * Pm)))
    Bs = sp.Matrix([[1, 2], [0, 3]]); Ps = sp.Matrix([[1, 1], [1, 2]]); As = Ps * Bs * Ps.inv()
    assert As.eigenvals() == Bs.eigenvals() == {1: 1, 3: 1} and As.eigenvects()[0][2][0] != Bs.eigenvects()[0][2][0]
    mcq(B, ch, t, 2, "Matrices $A$ and $B$ are similar. Which statement is always true?", "They have the same eigenvalues (and the same trace, determinant and rank)",
        ["They have the same eigenvectors", "They have the same entries", "One is the transpose of the other"],
        "If $A=PBP^{-1}$ then $\\det(A-\\lambda I)=\\det(B-\\lambda I)$, so the characteristic polynomial, eigenvalues, trace, determinant and rank agree. Eigenvectors change: $\\mathbf v$ is an eigenvector of $B$ iff $P\\mathbf v$ is one of $A$.")
    mcq(B, ch, t, 2, "$A$ is similar to $B=%s$. What are the eigenvalues of $A$?" % mtx(Bs), "$1$ and $3$", ["$2$ and $3$", "$1$ and $2$", "$0$ and $4$"],
        "Similar matrices have the same eigenvalues. $B$ is upper triangular, so its eigenvalues are its diagonal entries $1$ and $3$ (the entry $2$ above the diagonal does not matter).")
    mcq(B, ch, t, 3, "A linear map $T$ has matrix $\\operatorname{diag}(2,5)$ relative to the basis $\\{\\mathbf v_1,\\mathbf v_2\\}$. Then $T(\\mathbf v_2)$ equals", "$5\\mathbf v_2$", ["$2\\mathbf v_2$", "$2\\mathbf v_1+5\\mathbf v_2$", "$5\\mathbf v_1$"],
        "The second column of $[T]_B$ is $(0,5)$: the coordinates of $T(\\mathbf v_2)$ in the basis, so $T(\\mathbf v_2)=0\\mathbf v_1+5\\mathbf v_2=5\\mathbf v_2$. The basis vectors are eigenvectors with eigenvalues $2$ and $5$.")

# =============================================================================================== chapter 7
def orthogonal_questions(B):
    ch, t = "c7", "Orthogonal matrices"
    S1 = sp.Matrix([[1, 2], [2, 1]]); S2 = sp.Matrix([[1, 1], [0, -1]]); S3 = sp.Matrix([[1, 1], [0, 1]])
    for Mx_ in (S1, S2, S3):
        assert Mx_.T * Mx_ != sp.eye(2)
    assert S1 == S1.T and S2 * S2 == sp.eye(2) and S3.det() == 1
    mcq(B, ch, t, 1, "A square matrix $Q$ is orthogonal when", "$Q^TQ=I$ (its columns are orthonormal)", ["$Q^T=Q$", "$Q^2=I$", "$\\det Q=1$"],
        "Orthogonal means $Q^TQ=I$, i.e. the columns form an orthonormal set (equivalently $Q^{-1}=Q^T$). Symmetry, $Q^2=I$ and $\\det Q=1$ do not suffice: $%s$ is symmetric, $%s$ squares to $I$ and $%s$ has determinant $1$, yet none of them satisfies $Q^TQ=I$." % (mtx(S1), mtx(S2), mtx(S3)))
    R = sp.Matrix([[sp.sqrt(3) / 2, -sp.Rational(1, 2)], [sp.Rational(1, 2), sp.sqrt(3) / 2]])
    cands = [sp.Matrix([[1, 1], [-1, 1]]), sp.Matrix([[1, 2], [2, 1]]), sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5)], [sp.Rational(4, 5), sp.Rational(3, 5)]])]
    assert sp.simplify(R.T * R - sp.eye(2)) == sp.zeros(2) and all(sp.simplify(w.T * w - sp.eye(2)) != sp.zeros(2) for w in cands)
    mcq(B, ch, t, 2, "Which of these matrices is orthogonal?", mt(R), [mt(w) for w in cands],
        "Test $Q^TQ=I$: the columns must have length $1$ and be perpendicular. $%s$ is the rotation by $30^\\circ$: columns $(\\tfrac{\\sqrt3}2,\\tfrac12)$ and $(-\\tfrac12,\\tfrac{\\sqrt3}2)$ are unit vectors with dot product $0$. "
        "$\\begin{bmatrix}1&1\\\\-1&1\\end{bmatrix}$ has perpendicular columns of length $\\sqrt2$; the other two have non-perpendicular columns." % mtx(R))
    Rf = sp.diag(1, -1); assert Rf.T * Rf == sp.eye(2) and Rf.det() == -1 and R.det().simplify() == 1
    mcq(B, ch, t, 2, "If $Q$ is an orthogonal matrix, then $\\det Q$ is", "$+1$ or $-1$", ["only $+1$", "$0$ or $1$", "any real number"],
        "$\\det(Q^TQ)=(\\det Q)^2=\\det I=1$, so $\\det Q=\\pm1$. Rotations have determinant $+1$; reflections such as $\\operatorname{diag}(1,-1)$ have determinant $-1$.")
    Qr = sp.Matrix([[0, -1], [1, 0]]); vv = sp.Matrix([3, 4]); assert (Qr * vv).norm() == vv.norm() == 5
    mcq(B, ch, t, 2, "$Q=%s$ is orthogonal and $\\mathbf v=(3,4)$. What is $\\|Q\\mathbf v\\|$?" % mtx(Qr), "$5$", ["$7$", "$1$", "$25$"],
        "An orthogonal matrix preserves lengths: $\\|Q\\mathbf v\\|^2=\\mathbf v^TQ^TQ\\mathbf v=\\|\\mathbf v\\|^2$. Directly: $Q\\mathbf v=(-4,3)$ with length $\\sqrt{16+9}=5=\\|\\mathbf v\\|$.")
    S = sp.Matrix([[2, 1], [1, 2]]); ev = S.eigenvects(); vecs = [e[2][0] for e in sorted(ev, key=lambda e: e[0])]
    assert vecs[0].dot(vecs[1]) == 0
    mcq(B, ch, t, 2, "Eigenvectors of a symmetric matrix that belong to different eigenvalues are always", "orthogonal to each other", ["parallel to each other", "equal", "linearly dependent"],
        "For symmetric $A$ with $A\\mathbf u=\\lambda\\mathbf u$, $A\\mathbf w=\\mu\\mathbf w$, $\\lambda\\neq\\mu$: $\\lambda\\,\\mathbf u\\cdot\\mathbf w=A\\mathbf u\\cdot\\mathbf w=\\mathbf u\\cdot A\\mathbf w=\\mu\\,\\mathbf u\\cdot\\mathbf w$, hence $\\mathbf u\\cdot\\mathbf w=0$. Example: $%s$ has eigenvectors $(1,1)$ ($\\lambda=3$) and $(1,-1)$ ($\\lambda=1$), and their dot product is $0$." % mtx(S))
    Q = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2); Dd = sp.diag(3, 1)
    assert sp.simplify(Q.T * Q - sp.eye(2)) == sp.zeros(2) and sp.simplify(Q.T * S * Q - Dd) == sp.zeros(2)
    mcq(B, ch, t, 3, "$A=%s$ and $Q$ has the orthonormal eigenvectors $\\dfrac1{\\sqrt2}(1,1)$ and $\\dfrac1{\\sqrt2}(1,-1)$ as its first and second columns. What is $Q^TAQ$?" % mtx(S),
        mt(Dd), [mt(sp.diag(1, 3)), mt(S), mt(sp.eye(2))],
        "Orthogonal diagonalization: $Q^TAQ=D$ where the diagonal entries are the eigenvalues IN THE ORDER of the columns. $(1,1)/\\sqrt2$ belongs to $\\lambda=3$ and $(1,-1)/\\sqrt2$ to $\\lambda=1$, so $Q^TAQ=\\operatorname{diag}(3,1)$. (Swapping the columns would swap the diagonal entries.)")
    mcq(B, ch, t, 1, "If $Q$ is an orthogonal matrix, then $Q^{-1}$ equals", "$Q^T$", ["$-Q$", "$Q$", "$\\det(Q)\\,Q$"],
        "From $Q^TQ=I$ the inverse is the transpose: $Q^{-1}=Q^T$. ($Q^{-1}=Q$ holds only when also $Q^2=I$, e.g. a reflection.)")

# =============================================================================================== assembly
def build():
    B = Bank("LA", seed=20261106)
    for fn in (linear_equations, rank_questions, adjugate_questions, inner_product_questions, map_questions, orthogonal_questions):
        fn(B)
    return B

def lint(B):
    problems = []
    for q in B.items:
        for t_ in [q["q"], q["explain"]] + list(q["opts"]):
            if any(ord(ch) < 32 and ch != "\n" for ch in t_):
                problems.append((q["id"], "control character", t_[:60]))
            if t_.replace("\\$", "").count("$") % 2:
                problems.append((q["id"], "unbalanced $", t_[:60]))
        if len(set(q["opts"])) != 4 or any(not o.strip() for o in q["opts"]) or not 0 <= q["correct"] < 4:
            problems.append((q["id"], "bad options", ""))
    assert not problems, "LA gap pool lint failed: %r" % (problems[:5],)
    return len(B.items)

def merge(main, gap):
    """Finalize the gap bank on its own (balanced answer positions), give its ids the 'g' kind and append it to the main bank."""
    report = gap.finalize()
    lint(gap)
    for it in gap.items:
        it["id"] = it["id"].replace("-q", "-g", 1)
    main.items.extend(gap.items)
    return report

if __name__ == "__main__":
    from collections import Counter
    G_ = build()
    print(merge(Bank("LA", seed=1), G_))
    print(sorted(Counter((i["ch"], i["topic"]) for i in G_.items).items()))
    print("skipped", len(G_.skipped))
    for x in G_.skipped: print("  ", x)
