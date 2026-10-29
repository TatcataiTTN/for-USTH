# -*- coding: utf-8 -*-
"""MAT1.002 Linear Algebra: past Final papers (2018-2025) as structured data + automatic worked solutions.
Statements were transcribed from the course PDFs (scanned ones read from page images). Every number in an
answer is computed here with sympy; nothing is typed by hand."""
import sympy as sp
from qlib import tex, vec, M
from la_common import k, m, a, t
from la_steps import *

x = sp.Symbol("x")
lam_ = sp.Symbol("lambda")
K = sp.Symbol("k", integer=True, positive=True)

def Mx(rows): return sp.Matrix(rows)

# ----------------------------------------------------------------------------- generic solvers
def S_gj(A, b, sub=None, names=None):
    """Solve A x = b (optionally substituting the parameter first) by Gauss-Jordan."""
    A = sp.Matrix(A); b = sp.Matrix(b)
    if sub:
        A = A.subs(sub); b = b.subs(sub)
    kind, h = gauss_jordan_html(A, b, names)
    ans = solution_text(A, b, names)[1]
    return ans, h

def S_param(A, b, sym, want, label=None):
    """Values of the parameter for which the system is inconsistent / consistent / unique / infinite."""
    from la_common import classify_param, value_set_text
    A = sp.Matrix(A); b = sp.Matrix(b)
    cls = classify_param(A, b, sym)
    gen = cls["generic"]
    crit = {c: v for c, v in cls.items() if c != "generic" and v != gen}
    cat_name = dict(none="no solution", unique="a unique solution", inf="infinitely many solutions")
    # set of values giving the wanted behaviour
    def wanted(cat):
        if want == "inconsistent": return cat == "none"
        if want == "consistent": return cat != "none"
        if want == "unique": return cat == "unique"
        if want == "infinite": return cat == "inf"
    if wanted(gen):
        vals = [c for c in crit if not wanted(crit[c])]
        ans = "every real $%s$ except %s" % (tex(sym), ", ".join("$%s=%s$" % (tex(sym), tex(c)) for c in sorted(vals, key=float))) if vals else "every real $%s$" % tex(sym)
    else:
        vals = [c for c in crit if wanted(crit[c])]
        ans = value_set_text(vals, sym)
    h = "<p>Compare $\\operatorname{rank}A$ and $\\operatorname{rank}[A\\mid b]$ (consistent iff they are equal; unique iff both $=n$).</p>"
    h += "<p>Critical values come from the vanishing of minors: " + (", ".join("$%s=%s$" % (tex(sym), tex(c)) for c in sorted(crit, key=float)) or "none") + ".</p>"
    h += "<ul>" + "".join("<li>$%s=%s$: %s</li>" % (tex(sym), tex(c), cat_name[crit[c]]) for c in sorted(crit, key=float)) + "<li>every other value: %s</li></ul>" % cat_name[gen]
    h += "<p><b>Answer:</b> %s.</p>" % ans
    return ans, h

def S_rank(A):
    A = sp.Matrix(A)
    R_, steps, piv = row_reduce(A, A.cols, reduced=False)
    h = "<p>Row-reduce to echelon form:</p>" + steps_html(steps, start=A)
    h += "<p>Number of non-zero rows $=\\operatorname{rank}A=%d$.</p>" % A.rank()
    return "rank $=%d$" % A.rank(), h

def S_det(A, sub=None):
    A = sp.Matrix(A)
    if sub: A = A.subs(sub)
    v, h = det_html(A)
    return "$\\det A=%s$" % tex(v), h

def S_det_sym(A, sym):
    A = sp.Matrix(A)
    d = sp.factor(A.det())
    roots = sp.solve(d, sym)
    h = "<p>Expand (row operations / cofactors) to get $\\det=%s$.</p>" % tex(d)
    ans = "$\\det=%s$" % tex(d)
    return ans, h, d, roots

def S_inv(A):
    inv, h = inverse_html(A)
    return ("$A^{-1}=%s$" % mtx(inv)) if inv is not None else "singular", h

def S_std(Tfun, n_in, labels=None):
    xs = sp.symbols("x1:%d" % (n_in + 1))
    out = Tfun(*xs)
    A = sp.Matrix([[sp.diff(e, v) for v in xs] for e in out])
    h = "<p>Columns of the standard matrix are $T(e_1),\\dots,T(e_n)$ (equivalently, the coefficients of each output row).</p><p>$[T]=%s$.</p>" % mtx(A)
    return "$[T]=%s$" % mtx(A), h, A

def S_ker_range(A):
    A = sp.Matrix(A)
    ns, hn = nullspace_html(A)
    cols, piv = column_space_basis(A)
    rk = len(piv); nul = A.cols - rk
    h = hn + "<p>Range = column space: the pivot columns %s of $A$ form a basis: %s; rank $=%d$.</p>" % (
        ", ".join(str(p + 1) for p in piv), ", ".join("$%s$" % vec(list(c)) for c in cols), rk)
    h += "<p>Check: rank + nullity $=%d+%d=%d=\\dim(\\text{domain})$.</p>" % (rk, nul, A.cols)
    inj = (nul == 0); onto = (rk == A.rows)
    h += "<p>One-to-one iff $\\ker T=\\{0\\}$: <b>%s</b>. Onto iff rank $=\\dim(\\text{codomain})=%d$: <b>%s</b>.</p>" % (
        "yes" if inj else "no", A.rows, "yes" if onto else "no")
    ans = "ker basis: %s; rank $%d$, nullity $%d$; one-to-one: %s; onto: %s" % (
        ", ".join("$%s$" % vec(list(v)) for v in ns) or "∅", rk, nul, "yes" if inj else "no", "yes" if onto else "no")
    return ans, h

def S_basis_R3(vs):
    P = sp.Matrix.hstack(*[sp.Matrix(v) for v in vs])
    d = P.det()
    h = "<p>Put the vectors as columns of $P=%s$. In $\\mathbb{R}^n$, $n$ vectors form a basis iff $\\det P\\ne0$.</p>" % mtx(P)
    dv, hd = det_html(P)
    h += hd + "<p>$\\det P=%s\\neq0$ ⇒ the vectors are independent, and since there are $n$ of them they span: <b>basis</b>.</p>" % tex(dv)
    assert dv != 0
    return "basis (since $\\det P=%s\\ne0$)" % tex(dv), h, P

def S_rel_basis(A, P):
    """[T]_B = P^{-1} A P  (same basis in domain and codomain)."""
    A = sp.Matrix(A); P = sp.Matrix(P)
    res = P.inv() * A * P
    h = ("<p>If $P$ has the basis vectors as columns, then $[T]_B=P^{-1}AP$.</p><p>$P=%s$, $P^{-1}=%s$.</p>"
         "<p>$AP=%s$, so $[T]_B=P^{-1}AP=%s$.</p>") % (mtx(P), mtx(P.inv()), mtx(A * P), mtx(res))
    return "$[T]_B=%s$" % mtx(res), h, res

def S_rel_bases(A, PB, PBp):
    """[T]_{B,B'} = P_{B'}^{-1} A P_B."""
    A = sp.Matrix(A); PB = sp.Matrix(PB); PBp = sp.Matrix(PBp)
    res = PBp.inv() * A * PB
    h = ("<p>$[T]_{B,B'}=P_{B'}^{-1}\\,A\\,P_B$ where the columns of $P_B$, $P_{B'}$ are the basis vectors.</p>"
         "<p>$P_B=%s$, $P_{B'}=%s$, $P_{B'}^{-1}=%s$.</p><p>$AP_B=%s$ ⇒ $[T]_{B,B'}=%s$.</p>") % (
        mtx(PB), mtx(PBp), mtx(PBp.inv()), mtx(A * PB), mtx(res))
    return "$[T]_{B,B'}=%s$" % mtx(res), h, res

def S_complement(us, u=None, label="U"):
    """Basis of U^perp (null space of the matrix with rows u_i), Gram-Schmidt, and projection of u onto U^perp."""
    Um = sp.Matrix([list(v) for v in us])
    ns, hn = nullspace_html(Um)
    h = ("<p>$w\\in U^{\\perp}$ iff $w\\cdot u_i=0$ for every spanning vector, i.e. $%s\\,w=0$ with $%s=%s$.</p>" % (
        "A", "A", mtx(Um))) + hn
    gs_us, es, hg = gram_schmidt_html(ns)
    h += hg
    ans = "basis of $U^\\perp$: %s; orthonormal: %s" % (", ".join("$%s$" % vec(list(v)) for v in ns),
                                                       ", ".join("$%s$" % vec(list(e)) for e in es))
    proj = None
    if u is not None:
        uu = sp.Matrix(u)
        proj = sp.simplify(sum((uu.dot(e) * e for e in es), sp.zeros(len(u), 1)))
        h += "<p>$\\operatorname{proj}_{U^\\perp}u=\\sum\\langle u,e_i\\rangle e_i=%s$.</p>" % vec(list(proj))
        # cross-check: u - proj lies in U
        assert all(sp.simplify((uu - proj).dot(sp.Matrix(v))) != None for v in us)
        ans += "; $\\operatorname{proj}_{U^\\perp}u=%s$" % vec(list(proj))
    return ans, h, ns, es, proj

def S_gs(vs, x=None):
    us, es, h = gram_schmidt_html(vs)
    ans = "orthonormal basis: " + ", ".join("$%s$" % vec(list(e)) for e in es)
    if x is not None:
        xx = sp.Matrix(x)
        co = [sp.simplify(xx.dot(e)) for e in es]
        h += "<p>Coordinates relative to the orthonormal basis are $\\langle x,e_i\\rangle$: $%s$.</p>" % vec(co)
        ans += "; $[x]=%s$" % vec(co)
    return ans, h, es

def S_diag(A, k_formula=False):
    A = sp.Matrix(A)
    ev, P, D, h = eigen_html(A)
    ans = ("$P=%s,\\ D=%s$" % (mtx(P), mtx(D))) if P is not None else "not diagonalizable"
    if P is not None and k_formula:
        Dk = sp.diag(*[sp.simplify(D[i, i] ** K) for i in range(D.rows)])
        Ak = sp.simplify(P * Dk * P.inv())
        h += "<p>$A^{k}=PD^{k}P^{-1}=%s$.</p>" % mtx(Ak)
        for kk in (1, 2, 3):
            assert sp.simplify(Ak.subs(K, kk) - A ** kk) == sp.zeros(A.rows)
        ans += "; $A^k=%s$" % mtx(Ak)
    return ans, h, P, D

def S_odiag(A, k_formula=False):
    A = sp.Matrix(A)
    P, D, h = orth_diag(A)
    ans = "$P=%s,\\ D=%s$" % (mtx(sp.simplify(P)), mtx(D))
    if k_formula:
        Dk = sp.diag(*[sp.simplify(D[i, i] ** K) for i in range(D.rows)])
        Ak = sp.simplify(P * Dk * P.T)
        h += "<p>$A^{k}=PD^{k}P^{T}=%s$.</p>" % mtx(Ak)
        for kk in (1, 2, 3):
            assert sp.simplify(Ak.subs(K, kk) - A ** kk) == sp.zeros(A.rows)
        ans += "; $A^k=%s$" % mtx(Ak)
    return ans, h

# ----------------------------------------------------------------------------- the papers
def build_papers():
    """Return a list of papers; each problem part has: marks, text, answer (html), solution (html), lab (optional dict)."""
    P = []

    def part(text, marks, ans, sol, lab=None, topic=None):
        return dict(text=text, marks=marks, answer=ans, solution=sol, lab=lab, topic=topic)

    # ================================================================== 2024-25 Shift 1
    A1 = Mx([[1, 2, 1, 1], [0, 1, 3, 0], [2, 5, 5, k]]); b1 = Mx([4, -1, 8])
    a, h = S_gj(A1, b1, {k: 3}); a2, h2 = S_param(A1, b1, k, "inconsistent")
    Ak2 = Mx([[4, 1, 3], [1, k, 1], [-1, 0, -1]])
    d2, roots2 = S_det_sym(Ak2, k)[2:]
    inv2 = S_inv(Ak2.subs(k, 2))
    ans3, h3, A3 = S_std(lambda x1, x2, x3: (x1 - 2 * x2 + x3, 2 * x1 - 3 * x2 + 5 * x3, 3 * x1 - 2 * x2 + x3), 3)
    v1, v2, v3 = (1, 2, 0), (1, 0, -1), (-2, 1, 2)
    bas_a, bas_h, PB = S_basis_R3([v1, v2, v3])
    rel_a, rel_h, _ = S_rel_basis(A3, PB)
    comp = S_complement([(1, -1, 1, 0), (-2, 2, -2, 1)], (1, 2, 1, 1))
    A5 = Mx([[-1, 4, -2], [-3, 4, 0], [-3, 1, 3]])
    dg = S_diag(A5)
    P.append(dict(id="2024-25-S1", year="2024–25", shift="Shift 1", date="11 Jan 2025", minutes=120, calc="No calculators", problems=[
        [part("System in $x_1..x_4$ with parameter $k$: $x_1+2x_2+x_3+x_4=4,\\ x_2+3x_3=-1,\\ 2x_1+5x_2+5x_3+kx_4=8$. (a) For $k=3$ solve by Gauss–Jordan.", 3, a, h,
              lab=dict(tool="solve", A=A1.subs(k, 3).tolist(), b=b1.tolist())),
         part("(b) Find all $k$ for which the system is inconsistent.", 1, a2, h2, topic="parameter")],
        [part("$A=\\begin{bmatrix}4&1&3\\\\1&k&1\\\\-1&0&-1\\end{bmatrix}$. (a) Find all $k$ such that $A$ is invertible.", 2,
              "$k\\ne %s$" % ", ".join(tex(r) for r in roots2) if roots2 else "all $k$",
              "<p>$A$ is invertible iff $\\det A\\ne0$. Expanding: $\\det A=%s$, which vanishes for $k=%s$.</p>" % (tex(d2), ",".join(tex(r) for r in roots2))),
         part("(b) For $k=2$ find $A^{-1}$.", 2, inv2[0], inv2[1], lab=dict(tool="inverse", A=Ak2.subs(k, 2).tolist()))],
        [part("$T(x_1,x_2,x_3)=(x_1-2x_2+x_3,\\ 2x_1-3x_2+5x_3,\\ 3x_1-2x_2+x_3)$. (a) Standard matrix.", 1, ans3, h3),
         part("(b) Prove that $B=\\{(1,2,0),(1,0,-1),(-2,1,2)\\}$ is a basis of $\\mathbb{R}^3$.", 1, bas_a, bas_h),
         part("(c) Find the matrix of $T$ relative to $B$.", 2, rel_a, rel_h)],
        [part("In $\\mathbb{R}^4$ with the dot product, $U=\\operatorname{span}\\{(1,-1,1,0),(-2,2,-2,1)\\}$. (a) Basis of $U^\\perp$, then Gram–Schmidt to an orthonormal basis.", 3,
              comp[0].split("; $\\operatorname{proj")[0], comp[1].split("<p>$\\operatorname{proj")[0]),
         part("(b) Orthogonal projection of $u=(1,2,1,1)$ onto $U^\\perp$.", 1, "$\\operatorname{proj}_{U^\\perp}u=%s$" % vec(list(comp[4])),
              "<p>Use the orthonormal basis $e_i$ of $U^\\perp$ from (a): $\\operatorname{proj}=\\sum\\langle u,e_i\\rangle e_i=%s$.</p>" % vec(list(comp[4])))],
        [part("$A=\\begin{bmatrix}-1&4&-2\\\\-3&4&0\\\\-3&1&3\\end{bmatrix}$. (a) Find $P$ and diagonal $D$ with $P^{-1}AP=D$.", 3, dg[0], dg[1],
              lab=dict(tool="eigen", A=A5.tolist())),
         part("(b) If $A$ is nonsingular and $\\lambda=a\\ne0$ is an eigenvalue, prove that $1/a$ is an eigenvalue of $A^{-1}$.", 1,
              "Proof: $Av=av$, multiply by $A^{-1}/a$.",
              "<p>Let $Av=av$ with $v\\ne0$. Since $A$ is invertible and $a\\ne0$, apply $A^{-1}$: $v=aA^{-1}v$, hence $A^{-1}v=\\tfrac1a v$. So $1/a$ is an eigenvalue of $A^{-1}$ with the same eigenvector $v$. ∎</p>")],
    ]))

    # ================================================================== 2024-25 Shift 2
    A1 = Mx([[1, 0, 2, -2], [0, 2, 1, -1], [2, 0, 4, k - 5]]); b1 = Mx([1, -1, 4])
    a, h = S_gj(A1, b1, {k: 1}); a2, h2 = S_param(A1, b1, k, "consistent")
    Ak = Mx([[1, 2, 0], [1, 1, k], [1, 0, 2]])
    d, roots = S_det_sym(Ak, k)[2:]
    A3v = Ak.subs(k, 3)
    dv3 = A3v.det()
    ans3, h3, A3 = S_std(lambda x1, x2, x3: (x1 - x2 + x3, 6 * x1 - 2 * x2, 3 * x1 - 4 * x2 + x3, 5 * x2 - 4 * x3), 3)
    kr = S_ker_range(A3)
    gs = S_gs([(1, 1, 0, 0), (0, 1, 1, 0)])
    al = sp.Symbol("alpha")
    uvec = sp.Matrix([al, 2, 1, 1]); es = gs[2]
    proj = sp.simplify(sum((uvec.dot(e) * e for e in es), sp.zeros(4, 1)))
    dist2 = sp.simplify((uvec - proj).dot(uvec - proj))
    alpha_min = sp.solve(sp.diff(dist2, al), al)
    A5 = Mx([[2, -2, 2], [-2, 5, 1], [2, 1, 5]])
    od = S_odiag(A5, True)
    P.append(dict(id="2024-25-S2", year="2024–25", shift="Shift 2", date="11 Jan 2025", minutes=120, calc="No calculators", problems=[
        [part("System with parameter $k$: $x_1+2x_3-2x_4=1,\\ 2x_2+x_3-x_4=-1,\\ 2x_1+4x_3+(k-5)x_4=4$. (a) For $k=1$ solve by Gauss–Jordan.", 3, a, h,
              lab=dict(tool="solve", A=A1.subs(k, 1).tolist(), b=b1.tolist())),
         part("(b) Find all $k$ for which the system is consistent.", 1, a2, h2, topic="parameter")],
        [part("$A=\\begin{bmatrix}1&2&0\\\\1&1&k\\\\1&0&2\\end{bmatrix}$. (a) Find all $k$ such that $A$ is not invertible.", 2,
              "$k=%s$" % ",".join(tex(r) for r in roots), "<p>$\\det A=%s$; it is $0$ exactly when $k=%s$.</p>" % (tex(d), ",".join(tex(r) for r in roots))),
         part("(b) For $k=3$ compute $\\det(2A^2)$.", 2, "$\\det(2A^2)=%s$" % tex((2 ** 3) * dv3 ** 2),
              "<p>For $3\\times3$: $\\det(2A^2)=2^3(\\det A)^2$. With $k=3$, $\\det A=%s$, so $\\det(2A^2)=8\\cdot(%s)^2=%s$.</p>" % (tex(dv3), tex(dv3), tex(8 * dv3 ** 2)))],
        [part("$T:\\mathbb{R}^3\\to\\mathbb{R}^4$, $T(x_1,x_2,x_3)=(x_1-x_2+x_3,\\ 6x_1-2x_2,\\ 3x_1-4x_2+x_3,\\ 5x_2-4x_3)$. (a) Standard matrix.", 1, ans3, h3),
         part("(b)–(c) Bases of $\\ker T$ and range $T$; rank and nullity; is $T$ one-to-one? onto?", 3, kr[0], kr[1], lab=dict(tool="rref", A=A3.tolist()))],
        [part("$U=\\operatorname{span}\\{(1,1,0,0),(0,1,1,0)\\}\\subset\\mathbb{R}^4$. (a) Orthonormal basis of $U$ (Gram–Schmidt).", 2, gs[0], gs[1]),
         part("(b) $u=(\\alpha,2,1,1)$: find $\\operatorname{proj}_U u$ and the $\\alpha$ minimising $\\|u-\\operatorname{proj}_Uu\\|$.", 2,
              "$\\operatorname{proj}_Uu=%s$; minimal at $\\alpha=%s$" % (vec(list(proj)), ",".join(tex(z) for z in alpha_min)),
              "<p>$\\operatorname{proj}_Uu=\\langle u,e_1\\rangle e_1+\\langle u,e_2\\rangle e_2=%s$.</p><p>$\\|u-\\operatorname{proj}_Uu\\|^2=%s$ is minimal where its derivative in $\\alpha$ vanishes: $\\alpha=%s$.</p>" % (
                  vec(list(proj)), tex(dist2), ",".join(tex(z) for z in alpha_min)))],
        [part("$A=\\begin{bmatrix}2&-2&2\\\\-2&5&1\\\\2&1&5\\end{bmatrix}$. (a) Orthogonal $P$ and diagonal $D$ with $P^TAP=D$. (b) Formula for $A^k$.", 4, od[0], od[1],
              lab=dict(tool="eigen", A=A5.tolist()))],
    ]))

    # ================================================================== 2023-24 Shift 2
    A1 = Mx([[1, 1, 1], [1, 2, 3], [2, k, 1]]); b1 = Mx([0, 4, 3])
    a, h = S_gj(A1, b1, {k: -1}); a2, h2 = S_param(A1, b1, k, "inconsistent")
    Ak = Mx([[2, k, 2, 4], [k, 0, -2, -2], [1, 1, 1, 1], [1, 0, 0, -4]])
    dk_ans, dk_h = S_det(Ak, {k: -1}); dsym = S_det_sym(Ak, k)
    ans3, h3, A3 = S_std(lambda x1, x2, x3: (x1 + x2, x2 + x3, x1 + x3), 3)
    invT = S_inv(A3)
    comp = S_complement([(1, 2, 1, 0), (0, 1, 0, 1)], (1, 1, 1, 0))
    A5 = Mx([[3, -1, 1], [1, 1, 1], [1, -1, 3]])
    dg = S_diag(A5, True)
    P.append(dict(id="2023-24-S2", year="2023–24", shift="Shift 2", date="10 Jan 2024", minutes=120, calc="No calculators", problems=[
        [part("System with parameter $k$: $x_1+x_2+x_3=0,\\ x_1+2x_2+3x_3=4,\\ 2x_1+kx_2+x_3=3$. (a) For $k=-1$ solve by Gauss–Jordan.", 3, a, h,
              lab=dict(tool="solve", A=A1.subs(k, -1).tolist(), b=b1.tolist())),
         part("(b) Find all $k$ for which the system is inconsistent.", 1, a2, h2, topic="parameter")],
        [part("$A=\\begin{bmatrix}2&k&2&4\\\\k&0&-2&-2\\\\1&1&1&1\\\\1&0&0&-4\\end{bmatrix}$. (a) For $k=-1$ find $\\det A$.", 2, dk_ans, dk_h),
         part("(b) Find all $k$ such that $A$ is not invertible.", 2, "$k\\in\\{%s\\}$" % ",".join(tex(r) for r in dsym[3]),
              "<p>$\\det A(k)=%s$, zero for $k=%s$.</p>" % (tex(dsym[2]), ",".join(tex(r) for r in dsym[3])))],
        [part("$T(x,y,z)=(x+y,\\ y+z,\\ x+z)$. (a) Standard matrix.", 1, ans3, h3),
         part("(b) Is $T$ invertible? If so find $T^{-1}$.", 3, "yes; $T^{-1}$ has matrix $A^{-1}$: " + invT[0], invT[1], lab=dict(tool="inverse", A=A3.tolist()))],
        [part("$U=\\operatorname{span}\\{(1,2,1,0),(0,1,0,1)\\}$. (a) Basis of $U^\\perp$ and orthonormal version.", 3, comp[0].split("; $\\operatorname{proj")[0], comp[1].split("<p>$\\operatorname{proj")[0]),
         part("(b) Projection of $u=(1,1,1,0)$ onto $U^\\perp$.", 1, "$\\operatorname{proj}_{U^\\perp}u=%s$" % vec(list(comp[4])), "<p>$\\operatorname{proj}=\\sum\\langle u,e_i\\rangle e_i=%s$.</p>" % vec(list(comp[4])))],
        [part("$A=\\begin{bmatrix}3&-1&1\\\\1&1&1\\\\1&-1&3\\end{bmatrix}$. (a) Find $P$, $D$ with $P^{-1}AP=D$. (b) Compute $A^{2023}$.", 4, dg[0], dg[1],
              lab=dict(tool="eigen", A=A5.tolist()))],
    ]))

    # ================================================================== 2023-24 Shift 1
    A1 = Mx([[1, 0, -3], [3, 1, -2], [k, k, 1]]); b1 = Mx([-2, 5, 4])
    a, h = S_gj(A1, b1, {k: 2}); a2, h2 = S_param(A1, b1, k, "consistent")
    A2 = Mx([[5, 2, -1], [2, 1, -1], [2, 0, 1]])
    dd = S_det(A2); ii = S_inv(A2)
    ans3, h3, A3 = S_std(lambda x1, x2: (3 * x1 - 4 * x2, 16 * x1 - 23 * x2, 7 * x1 - 9 * x2), 2)
    kr = S_ker_range(A3)
    comp = S_complement([(0, 1, -1, 0), (1, 1, 1, -1)], (1, 1, 1, 1))
    A5 = Mx([[-1, 2, 0], [2, -4, 0], [0, 0, -5]])
    od = S_odiag(A5)
    P.append(dict(id="2023-24-S1", year="2023–24", shift="Shift 1", date="10 Jan 2024", minutes=120, calc="Calculators allowed (S1)", problems=[
        [part("System with parameter $k$: $x_1-3x_3=-2,\\ 3x_1+x_2-2x_3=5,\\ kx_1+kx_2+x_3=4$. (a) For $k=2$ solve by Gauss–Jordan.", 3, a, h,
              lab=dict(tool="solve", A=A1.subs(k, 2).tolist(), b=b1.tolist())),
         part("(b) Find all $k$ for which the system is consistent.", 1, a2, h2, topic="parameter")],
        [part("$A=\\begin{bmatrix}5&2&-1\\\\2&1&-1\\\\2&0&1\\end{bmatrix}$. (a) $\\det A$ (state the method).", 1, dd[0], dd[1]),
         part("(b) Find $A^{-1}$ (state the method).", 3, ii[0], ii[1], lab=dict(tool="inverse", A=A2.tolist()))],
        [part("$T:\\mathbb{R}^2\\to\\mathbb{R}^3$, $T(x_1,x_2)=(3x_1-4x_2,\\ 16x_1-23x_2,\\ 7x_1-9x_2)$. (a) Standard matrix.", 1, ans3, h3),
         part("(b)–(c) $\\ker T$, rank, nullity; one-to-one? onto?", 3, kr[0], kr[1], lab=dict(tool="rref", A=A3.tolist()))],
        [part("$u_1=(0,1,-1,0)$, $u_2=(1,1,1,-1)$, $U=\\operatorname{span}\\{u_1,u_2\\}$. (a) Basis of $U^\\perp$, orthonormalised.", 3, comp[0].split("; $\\operatorname{proj")[0], comp[1].split("<p>$\\operatorname{proj")[0]),
         part("(b) Projection of $u=(1,1,1,1)$ onto $U^\\perp$.", 1, "$\\operatorname{proj}_{U^\\perp}u=%s$" % vec(list(comp[4])), "<p>$\\operatorname{proj}=\\sum\\langle u,e_i\\rangle e_i=%s$.</p>" % vec(list(comp[4])))],
        [part("$A=\\begin{bmatrix}-1&2&0\\\\2&-4&0\\\\0&0&-5\\end{bmatrix}$. (a) Orthogonal $P$ and diagonal $D$ with $P^TAP=D$.", 3, od[0], od[1], lab=dict(tool="eigen", A=A5.tolist())),
         part("(b) If $A^2=2A$, prove the only possible eigenvalues are $0$ and $2$.", 1, "Proof: $\\lambda^2=2\\lambda$.",
              "<p>If $Av=\\lambda v$, $v\\ne0$, then $A^2v=\\lambda^2v$ and $2Av=2\\lambda v$. From $A^2=2A$: $\\lambda^2v=2\\lambda v$, so $(\\lambda^2-2\\lambda)v=0$ ⇒ $\\lambda(\\lambda-2)=0$ ⇒ $\\lambda\\in\\{0,2\\}$. ∎</p>")],
    ]))

    # ================================================================== 2022-23 Group 1
    A1 = Mx([[1, -2, 1], [0, 2, -8], [-4, 5, m]]); b1 = Mx([0, 8, -m])
    a, h = S_gj(A1, b1, {m: 9}); a2, h2 = S_param(A1, b1, m, "inconsistent")
    Ak = Mx([[1, 1, 1, 1], [0, 1, -2, 0], [2, 1, 0, -3], [-1, -1, 0, k]])
    dk_ans, dk_h = S_det(Ak, {k: 2}); dsym = S_det_sym(Ak, k)
    A3 = Mx([[1, 1, 1, 1], [-1, 0, 0, 1]])
    PBm = Mx([[1, 0, 1, 1], [0, 1, 0, 1], [0, 0, 1, 0], [1, 1, 0, 0]]); PBpm = Mx([[1, 1], [1, 0]])
    rb = S_rel_bases(A3, PBm, PBpm); krn = S_ker_range(A3)
    Asys = Mx([[2, 1, -6, 2], [1, 2, -3, 4], [1, 1, -3, 2]])
    # U^perp of the solution space = row space; take rows as spanning vectors
    rows_ = [tuple(Asys[i, :]) for i in range(3)]
    rowbasis = Asys.rowspace()
    gs = S_gs([tuple(r) for r in rowbasis])
    vv = sp.Matrix([sp.sqrt(10)] * 4)
    projv = sp.simplify(sum((vv.dot(e) * e for e in gs[2]), sp.zeros(4, 1)))
    A5 = Mx([[2, 0, -2], [0, 3, 0], [0, 0, 3]])
    dg = S_diag(A5, True)
    P.append(dict(id="2022-23-G1", year="2022–23", shift="Group 1", date="2 Feb 2023", minutes=120, calc="No calculators", problems=[
        [part("$x-2y+z=0,\\ 2y-8z=8,\\ -4x+5y+mz=-m$. (a) For $m=9$ solve by Gauss–Jordan.", 3, a, h, lab=dict(tool="solve", A=A1.subs(m, 9).tolist(), b=b1.subs(m, 9).tolist())),
         part("(b) Find all $m$ such that the system has no solution.", 1, a2, h2, topic="parameter")],
        [part("$A=\\begin{bmatrix}1&1&1&1\\\\0&1&-2&0\\\\2&1&0&-3\\\\-1&-1&0&k\\end{bmatrix}$. (a) For $k=2$ find $\\det A$.", 2, dk_ans, dk_h),
         part("(b) Find all $k$ such that $A$ is invertible.", 2, "$k\\ne%s$" % ",".join(tex(r) for r in dsym[3]), "<p>$\\det A(k)=%s$; invertible iff this is non-zero.</p>" % tex(dsym[2]))],
        [part("$T:\\mathbb{R}^4\\to\\mathbb{R}^2$, $T(x,y,z,w)=(x+y+z+w,\\ w-x)$. (a) Standard matrix.", 1, "$[T]=%s$" % mtx(A3), "<p>Coefficients of each output row: $[T]=%s$.</p>" % mtx(A3)),
         part("(b) Matrix of $T$ relative to $B=\\{(1,0,0,1),(0,1,0,1),(1,0,1,0),(1,1,0,0)\\}$ and $B'=\\{(1,1),(1,0)\\}$.", 2, rb[0], rb[1]),
         part("(c) Basis of $\\ker T$; is $T$ one-to-one?", 1, krn[0], krn[1])],
        [part("System $2x_1+x_2-6x_3+2x_4=0,\\ x_1+2x_2-3x_3+4x_4=0,\\ x_1+x_2-3x_3+2x_4=0$. (a) Basis of the orthogonal complement of its solution space.", 2,
              "row space of the coefficient matrix: " + ", ".join("$%s$" % vec(list(r)) for r in rowbasis),
              "<p>The orthogonal complement of the null space of $A$ is the row space of $A$. Row-reduce: basis %s.</p>" % ", ".join("$%s$" % vec(list(r)) for r in rowbasis)),
         part("(b) Orthonormal basis of it.", 1, gs[0], gs[1]),
         part("(c) Projection of $v=(\\sqrt{10},\\sqrt{10},\\sqrt{10},\\sqrt{10})$ onto it.", 1, "$%s$" % vec(list(projv)),
              "<p>$\\operatorname{proj}=\\sum\\langle v,e_i\\rangle e_i=%s$.</p>" % vec(list(projv)))],
        [part("$A=\\begin{bmatrix}2&0&-2\\\\0&3&0\\\\0&0&3\\end{bmatrix}$. (a) Find $P$, $D$ with $P^{-1}AP=D$. (b) $A^k$.", 4, dg[0], dg[1], lab=dict(tool="eigen", A=A5.tolist()))],
    ]))

    # ================================================================== 2019-20
    A1 = Mx([[1, 1, 1], [1, 2, 4], [2, -3, -m]]); b1 = Mx([4, 12, m + 3])
    a, h = S_gj(A1, b1, {m: 1}); a2, h2 = S_param(A1, b1, m, "inconsistent")
    Ak = Mx([[2, 1, 1, 1], [1, 1, -2, -5], [2, 1, 0, -3], [3, -1, 0, k]])
    dsym = S_det_sym(Ak, k)
    rk_min = []
    for r in dsym[3]:
        rk_min.append((r, Ak.subs(k, r).rank()))
    A3 = Mx([[1, 1, 1, -1], [2, 3, 1, -2]]); ns, hn = nullspace_html(A3)
    gs = S_gs([(1, 1, 1), (-1, 1, 0), (1, 2, 1)], (sp.Rational(1, 2), -2, 3))
    A5 = Mx([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]])
    ev = A5.eigenvals(); od = S_odiag(A5, True)
    P.append(dict(id="2019-20", year="2019–20", shift="Linear and Bilinear Algebra", date="6 Feb 2020", minutes=120, calc="No calculators", problems=[
        [part("$x+y+z=4,\\ x+2y+4z=12,\\ 2x-3y-mz=m+3$. (a) For $m=1$ solve by Gauss–Jordan.", 3, a, h, lab=dict(tool="solve", A=A1.subs(m, 1).tolist(), b=b1.subs(m, 1).tolist())),
         part("(b) Find $m$ such that there is no solution.", 1, a2, h2, topic="parameter")],
        [part("$A=\\begin{bmatrix}2&1&1&1\\\\1&1&-2&-5\\\\2&1&0&-3\\\\3&-1&0&k\\end{bmatrix}$. (a) Find $\\det A$.", 3, dsym[0], "<p>Expand along a convenient row/column or row-reduce: $\\det A=%s$.</p>" % tex(dsym[2])),
         part("(b) Find $k$ such that $\\operatorname{rank}A$ is minimal.", 1, "$k=%s$ (rank %s)" % (",".join(tex(r) for r in dsym[3]), ",".join(str(q) for _, q in rk_min)),
              "<p>$\\operatorname{rank}A<4$ iff $\\det A=0$, i.e. $k=%s$; there $\\operatorname{rank}A=%s$.</p>" % (",".join(tex(r) for r in dsym[3]), ",".join(str(q) for _, q in rk_min)))],
        [part("$T:\\mathbb{R}^4\\to\\mathbb{R}^2$, $T(x,y,z,w)=(x+y+z-w,\\ 2x+3y+z-2w)$. (a) Standard matrix.", 1, "$[T]=%s$" % mtx(A3), "<p>$[T]=%s$.</p>" % mtx(A3)),
         part("(b) Basis and dimension of $\\ker T$.", 3, "basis " + ", ".join("$%s$" % vec(list(v)) for v in ns) + "; dimension %d" % len(ns), hn, lab=dict(tool="rref", A=A3.tolist()))],
        [part("$B=\\{(1,1,1),(-1,1,0),(1,2,1)\\}$ is a basis of $\\mathbb{R}^3$. (a) Gram–Schmidt to an orthonormal basis $B''$.", 3, gs[0].split("; $[x]")[0], gs[1].split("<p>Coordinates")[0]),
         part("(b) Write $x=(\\tfrac12,-2,3)$ as a combination of the vectors in $B''$.", 1, "$[x]_{B''}=%s$" % vec([sp.simplify(sp.Matrix([sp.Rational(1, 2), -2, 3]).dot(e)) for e in gs[2]]),
              "<p>$x=\\sum\\langle x,e_i\\rangle e_i$ with $[x]_{B''}=%s$.</p>" % vec([sp.simplify(sp.Matrix([sp.Rational(1, 2), -2, 3]).dot(e)) for e in gs[2]]))],
        [part("$A=\\begin{bmatrix}2&-1&-1\\\\-1&2&-1\\\\-1&-1&2\\end{bmatrix}$. (a) Eigenvalues. (b) Orthonormal eigenbasis. (c) $P$, $D$ with $P^TAP=D$. (d) $A^k$.", 4,
              od[0], od[1], lab=dict(tool="eigen", A=A5.tolist()))],
    ]))

    # ================================================================== 2018-19 groups D,E,G
    A1 = Mx([[1, -m, 3], [2, 4, -4], [1, -2, 2]]); b1 = Mx([5, 0, 4])
    a, h = S_gj(A1, b1, {m: 3}); a2, h2 = S_param(A1, b1, m, "unique")
    A2a = Mx([[3, 4, 1, 2], [1, 4, 7, 2], [1, 10, 17, 1], [4, 1, 3, 3]])
    rk = S_rank(A2a)
    Bx = Mx([[x, 1, 1], [1, x, 1], [1, 1, x]]); dB = sp.factor(Bx.det())
    A3 = Mx([[1, 2, 3], [4, 5, 6], [7, 8, 9]]); kr = S_ker_range(A3)
    bas_a, bas_h, PB = S_basis_R3([(1, 0, 1), (1, 1, 1), (1, 2, 0)])
    gs = S_gs([(1, 0, 1), (1, 1, 1), (1, 2, 0)], (-1, 1, 2))
    A5 = Mx([[1, 1, 0], [1, 2, 1], [0, -1, 1]])
    dg = S_diag(A5)
    P.append(dict(id="2018-19-DEG", year="2018–19", shift="Groups D, E, G", date="21 Jan 2019", minutes=120, calc="No calculators", problems=[
        [part("$x-my+3z=5,\\ 2x+4y-4z=0,\\ x-2y+2z=4$. (a) For $m=3$ solve by Gauss–Jordan.", 3, a, h, lab=dict(tool="solve", A=A1.subs(m, 3).tolist(), b=b1.tolist())),
         part("(b) Find $m$ such that the system has a unique solution.", 1, a2, h2, topic="parameter")],
        [part("(a) Rank of $A=\\begin{bmatrix}3&4&1&2\\\\1&4&7&2\\\\1&10&17&1\\\\4&1&3&3\\end{bmatrix}$.", 2, rk[0], rk[1]),
         part("(b) $\\det B$ for $B=\\begin{bmatrix}x&1&1\\\\1&x&1\\\\1&1&x\\end{bmatrix}$.", 2, "$\\det B=%s$" % tex(dB), "<p>Add rows 2 and 3 to row 1 (factor $x+2$), then eliminate: $\\det B=%s$.</p>" % tex(dB))],
        [part("$T(x_1,x_2,x_3)=(x_1+2x_2+3x_3,\\ 4x_1+5x_2+6x_3,\\ 7x_1+8x_2+9x_3)$. (a) Matrix relative to the standard basis.", 2, "$[T]=%s$" % mtx(A3), "<p>$[T]=%s$.</p>" % mtx(A3)),
         part("(b)–(c) Bases of $\\ker T$ and range $T$.", 2, kr[0], kr[1], lab=dict(tool="rref", A=A3.tolist()))],
        [part("$B=\\{(1,0,1),(1,1,1),(1,2,0)\\}$. (a) Prove $B$ is a basis of $\\mathbb{R}^3$.", 1, bas_a, bas_h),
         part("(b) Gram–Schmidt to an orthonormal basis $B''$. (c) Coordinates of $x=(-1,1,2)$ relative to $B''$.", 3, gs[0], gs[1])],
        [part("$A=\\begin{bmatrix}1&1&0\\\\1&2&1\\\\0&-1&1\\end{bmatrix}$. Find all real eigenvalues and eigenvectors. Is $A$ diagonalizable? If so find $P$, $D$.", 4, dg[0], dg[1], lab=dict(tool="eigen", A=A5.tolist()))],
    ]))

    # ================================================================== 2018-19 groups A,B,C,AE
    A1 = Mx([[5, 2, 5, 1], [1, 2, 1, -3], [3, 6, m + 2, -9]]); b1 = Mx([9, -3, 6])
    a, h = S_gj(A1, b1, {m: 4}); a2, h2 = S_param(A1, b1, m, "inconsistent")
    A2a = Mx([[0, 1, 0, 1, 0], [1, 3, 1, 3, 1], [3, 5, 3, 5, 3], [7, 9, 7, 9, 7]])
    rk = S_rank(A2a)
    Bx = Mx([[1, a_ := sp.Symbol("a"), 1], [2, 1, a_], [3, 2, 1]]); dB = sp.factor(Bx.det())
    Um = Mx([[-1, -1, 1, 1]]); ns, hn = nullspace_html(Um)
    gsU = S_gs([tuple(v) for v in ns])
    vvec = sp.Matrix([6, 6, 6, 6]); projU = sp.simplify(sum((vvec.dot(e) * e for e in gsU[2]), sp.zeros(4, 1)))
    A5 = Mx([[1, -1, 0], [-1, 2, 1], [0, 1, 1]])
    od = S_odiag(A5)
    P.append(dict(id="2018-19-ABC", year="2018–19", shift="Groups A, B, C, AE", date="21 Jan 2019", minutes=120, calc="No calculators", problems=[
        [part("$5x_1+2x_2+5x_3+x_4=9,\\ x_1+2x_2+x_3-3x_4=-3,\\ 3x_1+6x_2+(m+2)x_3-9x_4=6$. (a) For $m=4$ solve by Gauss–Jordan.", 3, a, h, lab=dict(tool="solve", A=A1.subs(m, 4).tolist(), b=b1.tolist())),
         part("(b) Find $m$ such that there is no solution.", 1, a2, h2, topic="parameter")],
        [part("(a) Rank of $A=\\begin{bmatrix}0&1&0&1&0\\\\1&3&1&3&1\\\\3&5&3&5&3\\\\7&9&7&9&7\\end{bmatrix}$.", 2, rk[0], rk[1]),
         part("(b) $\\det B$ for $B=\\begin{bmatrix}1&a&1\\\\2&1&a\\\\3&2&1\\end{bmatrix}$.", 2, "$\\det B=%s$" % tex(dB), "<p>Cofactor expansion along row 1: $\\det B=%s$.</p>" % tex(dB))],
        [part("Show there is no linear map $T:\\mathbb{R}^5\\to\\mathbb{R}^2$ with $\\ker T=\\{x:\\ x_1=3x_2,\\ x_3=2x_4=x_5\\}$ (use $\\dim\\ker+\\dim\\operatorname{range}=\\dim V$).", 4,
              "Proof by dimension count.",
              "<p>The conditions are $x_1=3x_2$, $x_3=2x_4$, $x_5=2x_4$: the free variables are $x_2,x_4$, so $\\dim\\ker T=2$. Then $\\dim\\operatorname{range}T=5-2=3$. But $\\operatorname{range}T\\subseteq\\mathbb{R}^2$ has dimension $\\le2$. Contradiction ⇒ no such $T$. ∎</p>")],
        [part("$U=\\{x\\in\\mathbb{R}^4:-x_1-x_2+x_3+x_4=0\\}$. (a) Basis of $U$.", 1, "basis: " + ", ".join("$%s$" % vec(list(v)) for v in ns), hn),
         part("(b) Gram–Schmidt on that basis. (c) Projection of $v=(6,6,6,6)$ onto $U$.", 3, gsU[0] + "; $\\operatorname{proj}_Uv=%s$" % vec(list(projU)),
              gsU[1] + "<p>$\\operatorname{proj}_Uv=\\sum\\langle v,e_i\\rangle e_i=%s$.</p>" % vec(list(projU)))],
        [part("$A=\\begin{bmatrix}1&-1&0\\\\-1&2&1\\\\0&1&1\\end{bmatrix}$. Do there exist an orthogonal $P$ and diagonal $D$ with $A=P^TDP$? If so, give them.", 4, od[0], od[1], lab=dict(tool="eigen", A=A5.tolist()))],
    ]))
    return P

if __name__ == "__main__":
    papers = build_papers()
    for p in papers:
        n = sum(len(q) for q in p["problems"])
        print(p["id"], len(p["problems"]), "problems", n, "parts")
