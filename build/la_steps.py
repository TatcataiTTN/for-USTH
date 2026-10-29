# -*- coding: utf-8 -*-
"""Step-by-step linear-algebra solvers that emit HTML + KaTeX (exact rational arithmetic via sympy).
Used for (a) explanations of quiz questions, (b) worked solutions of past-paper / tutorial problems.
The JavaScript lab (shared/la.js) implements the same algorithms; tests/la_cross_check.py compares them."""
import sympy as sp
from qlib import tex, vec

# ----------------------------------------------------------------------------- formatting
def mtx(Mx, ncoef=None):
    Mx = sp.Matrix(Mx)
    rows = [" & ".join(tex(Mx[i, j]) for j in range(Mx.cols)) for i in range(Mx.rows)]
    if ncoef is not None and ncoef < Mx.cols:
        spec = "c" * ncoef + "|" + "c" * (Mx.cols - ncoef)
        return r"\left[\begin{array}{%s}" % spec + r" \\ ".join(rows) + r"\end{array}\right]"
    return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"

def coef(c):
    c = sp.nsimplify(c)
    return "" if c == 1 else tex(c)

def op_scale(r, c):
    return r"R_{%d}\leftarrow %sR_{%d}" % (r + 1, coef(c), r + 1)

def op_add(i, f, r):
    f = sp.nsimplify(f)
    sign = "+" if f > 0 else "-"
    return r"R_{%d}\leftarrow R_{%d}%s%sR_{%d}" % (i + 1, i + 1, sign, coef(abs(f)), r + 1)

def op_swap(i, j):
    return r"R_{%d}\leftrightarrow R_{%d}" % (i + 1, j + 1)

def steps_html(steps, ncoef=None, start=None):
    """steps = [(op_latex, matrix)] -> HTML block (flex-wrapped chips)."""
    h = '<div class="steps">'
    if start is not None:
        h += '<div class="st"><span class="op">start</span>$%s$</div>' % mtx(start, ncoef)
    for op, Mx in steps:
        h += '<div class="st"><span class="op">$%s$</span>$%s$</div>' % (op, mtx(Mx, ncoef))
    return h + "</div>"

# ----------------------------------------------------------------------------- row reduction
def row_reduce(Mx, ncoef=None, reduced=True):
    """Gauss (reduced=False: forward elimination, no normalisation) or Gauss-Jordan (reduced=True).
    Returns (final matrix, steps, pivot columns)."""
    Mx = sp.Matrix(Mx)
    ncoef = Mx.cols if ncoef is None else ncoef
    steps, pivots, r = [], [], 0
    for c in range(ncoef):
        if r >= Mx.rows:
            break
        p = next((i for i in range(r, Mx.rows) if Mx[i, c] != 0), None)
        if p is None:
            continue
        if p != r:
            Mx.row_swap(p, r)
            steps.append((op_swap(p, r), Mx.copy()))
        if reduced and Mx[r, c] != 1:
            piv = Mx[r, c]
            Mx[r, :] = Mx[r, :] / piv
            steps.append((op_scale(r, 1 / piv), Mx.copy()))
        for i in range(Mx.rows):
            if i != r and Mx[i, c] != 0 and (reduced or i > r):
                f = Mx[i, c] / Mx[r, c]
                Mx[i, :] = Mx[i, :] - f * Mx[r, :]
                steps.append((op_add(i, -f, r), Mx.copy()))
        pivots.append(c)
        r += 1
    return Mx, steps, pivots

def solution_text(A, b, names=None):
    """Return (kind, html) describing the general solution after Gauss-Jordan."""
    A = sp.Matrix(A); b = sp.Matrix(b)
    n = A.cols
    names = names or ["x_%d" % (j + 1) for j in range(n)]
    R_, _, piv = row_reduce(A.row_join(b), n, True)
    rA = len(piv)
    if any(R_[i, :n].is_zero_matrix and R_[i, n] != 0 for i in range(R_.rows)):
        return "none", "The last non-zero row is $0=%s\\neq 0$, so the system is <b>inconsistent</b> (no solution)." % tex(
            next(R_[i, n] for i in range(R_.rows) if R_[i, :n].is_zero_matrix and R_[i, n] != 0))
    free = [j for j in range(n) if j not in piv]
    if not free:
        return "unique", "Unique solution: $%s$." % ",\\ ".join("%s=%s" % (names[j], tex(R_[i, n])) for i, j in enumerate(piv))
    params = [sp.Symbol(x) for x in ["t", "s", "u", "v"][:len(free)]]
    val = {}
    for q, j in enumerate(free):
        val[j] = params[q]
    for i, j in enumerate(piv):
        e = R_[i, n] - sum(R_[i, f] * val[f] for f in free)
        val[j] = sp.expand(e)
    lines = ",\\ ".join("%s=%s" % (names[j], tex(val[j])) for j in range(n))
    plist = ",".join(tex(p) for p in params)
    return "inf", ("Infinitely many solutions (%d free variable%s): $%s$, where $%s\\in\\mathbb{R}$."
                   % (len(free), "s" if len(free) > 1 else "", lines, plist))

def gauss_jordan_html(A, b, names=None, mode="gj"):
    A = sp.Matrix(A); b = sp.Matrix(b)
    aug_m = A.row_join(b)
    R_, steps, piv = row_reduce(aug_m, A.cols, reduced=(mode == "gj"))
    kind, txt = solution_text(A, b, names)
    h = "<p>Augmented matrix, then elementary row operations:</p>"
    h += steps_html(steps, A.cols, start=aug_m)
    h += "<p>%s</p>" % txt
    return kind, h

# ----------------------------------------------------------------------------- determinant
def det_html(A):
    """Row-reduction narrative with sign tracking, plus a cofactor line for 2x2 / 3x3."""
    A = sp.Matrix(A); n = A.rows
    Mx = A.copy(); sign = 1; steps = []; factor = sp.Integer(1)
    for c in range(n):
        p = next((i for i in range(c, n) if Mx[i, c] != 0), None)
        if p is None:
            steps.append((r"\text{column %d has no pivot}\Rightarrow\det=0" % (c + 1), Mx.copy()))
            return sp.Integer(0), '<p>Reduce to a triangular form:</p>' + steps_html(steps, start=A) + "<p>A zero pivot column forces $\\det A=0$.</p>"
        if p != c:
            Mx.row_swap(p, c); sign = -sign
            steps.append((op_swap(p, c) + r"\ (\det\times(-1))", Mx.copy()))
        for i in range(c + 1, n):
            if Mx[i, c] != 0:
                f = Mx[i, c] / Mx[c, c]
                Mx[i, :] = Mx[i, :] - f * Mx[c, :]
                steps.append((op_add(i, -f, c), Mx.copy()))
    diag = [Mx[i, i] for i in range(n)]
    val = sign * sp.prod(diag)
    h = "<p>Row-reduce to triangular form (adding a multiple of a row does not change $\\det$; a swap flips the sign):</p>"
    h += steps_html(steps, start=A)
    h += "<p>$\\det A=%s%s=%s$.</p>" % ("-" if sign < 0 else "", "\\cdot".join("(%s)" % tex(d) for d in diag), tex(val))
    if n == 3:
        a_ = A
        cof = (a_[0, 0] * (a_[1, 1] * a_[2, 2] - a_[1, 2] * a_[2, 1])
               - a_[0, 1] * (a_[1, 0] * a_[2, 2] - a_[1, 2] * a_[2, 0])
               + a_[0, 2] * (a_[1, 0] * a_[2, 1] - a_[1, 1] * a_[2, 0]))
        h += ("<p>Check by cofactor expansion along row 1: $%s\\,(%s)-(%s)\\,(%s)+(%s)\\,(%s)=%s$.</p>" % (
            tex(a_[0, 0]), tex(a_[1, 1] * a_[2, 2] - a_[1, 2] * a_[2, 1]),
            tex(a_[0, 1]), tex(a_[1, 0] * a_[2, 2] - a_[1, 2] * a_[2, 0]),
            tex(a_[0, 2]), tex(a_[1, 0] * a_[2, 1] - a_[1, 1] * a_[2, 0]), tex(cof)))
        assert cof == val == A.det()
    assert val == A.det(), (val, A.det())
    return val, h

# ----------------------------------------------------------------------------- inverse
def inverse_html(A):
    A = sp.Matrix(A); n = A.rows
    aug_m = A.row_join(sp.eye(n))
    R_, steps, piv = row_reduce(aug_m, n, True)
    if R_[:, :n] != sp.eye(n):
        return None, "<p>Row reduction of $[A\\mid I]$ does not reach $[I\\mid *]$ (a zero row appears), so $A$ is <b>singular</b>: no inverse.</p>"
    inv = R_[:, n:]
    assert inv == A.inv()
    h = "<p>Gauss–Jordan on $[A\\mid I]$:</p>" + steps_html(steps, n, start=aug_m)
    h += "<p>Hence $A^{-1}=%s$.</p>" % mtx(inv)
    return inv, h

# ----------------------------------------------------------------------------- spaces
def nullspace_html(A):
    A = sp.Matrix(A)
    R_, steps, piv = row_reduce(A, A.cols, True)
    ns = A.nullspace()
    h = "<p>Row-reduce $A$ to RREF: $%s$ (pivot columns: %s).</p>" % (
        mtx(R_), ", ".join(str(p + 1) for p in piv))
    if ns:
        h += "<p>Free variables → basis of the null space: %s; nullity $=%d$.</p>" % (
            ", ".join("$%s$" % vec(v) for v in ns), len(ns))
    else:
        h += "<p>No free variables: null space $=\\{0\\}$, nullity $0$.</p>"
    return ns, h

def column_space_basis(A):
    A = sp.Matrix(A)
    _, piv = A.rref()
    return [A[:, j] for j in piv], piv

def gram_schmidt_html(vs, normalize=True):
    vs = [sp.Matrix(v) for v in vs]
    us = []; lines = []
    for i, v in enumerate(vs):
        w = v.copy(); terms = []
        for j, u in enumerate(us):
            c = (v.dot(u)) / (u.dot(u))
            w = w - c * u
            terms.append("(%s)\\,u_{%d}" % (tex(c), j + 1))
        w = sp.simplify(w)
        us.append(w)
        if terms:
            lines.append("u_{%d}=v_{%d}-%s=%s" % (i + 1, i + 1, "-".join(terms), vec(list(w))))
        else:
            lines.append("u_{1}=v_{1}=%s" % vec(list(w)))
    es = [sp.simplify(u / sp.sqrt(u.dot(u))) for u in us]
    h = "<p>Gram–Schmidt (orthogonal vectors first): $u_k=v_k-\\sum_{j<k}\\frac{\\langle v_k,u_j\\rangle}{\\langle u_j,u_j\\rangle}u_j$.</p><p>"
    h += "<br>".join("$%s$" % l for l in lines) + "</p>"
    if normalize:
        h += "<p>Normalise $e_k=u_k/\\|u_k\\|$: " + ", ".join("$e_{%d}=%s$" % (i + 1, vec(list(e))) for i, e in enumerate(es)) + ".</p>"
    return us, es, h

# ----------------------------------------------------------------------------- eigen
lam = sp.Symbol("lambda")

def eigen_html(A):
    A = sp.Matrix(A); n = A.rows
    cp = sp.factor((A - lam * sp.eye(n)).det())
    ev = A.eigenvects()
    h = "<p>Characteristic polynomial: $\\det(A-\\lambda I)=%s$.</p>" % tex(cp)
    P_cols = []; D_diag = []
    for val, mult, basis in sorted(ev, key=lambda e: float(sp.re(sp.N(e[0])))):
        h += "<p>$\\lambda=%s$ (algebraic multiplicity %d): eigenspace basis %s (geometric multiplicity %d).</p>" % (
            tex(val), mult, ", ".join("$%s$" % vec(list(v)) for v in basis), len(basis))
        for v in basis:
            P_cols.append(v); D_diag.append(val)
    diag = len(P_cols) == n and all(sp.im(sp.N(e[0])) == 0 for e in ev)
    P = None; D = None
    if diag:
        P = sp.Matrix.hstack(*P_cols); D = sp.diag(*D_diag)
        assert sp.simplify(P.inv() * A * P - D) == sp.zeros(n)
        h += "<p>Geometric = algebraic multiplicity for every eigenvalue ⇒ <b>diagonalizable</b>: $P=%s,\\ D=%s$, $P^{-1}AP=D$.</p>" % (mtx(P), mtx(D))
    else:
        h += "<p>Not diagonalizable over $\\mathbb{R}$: there are not $n$ independent real eigenvectors.</p>"
    return ev, P, D, h

def orth_diag(A):
    """Orthogonal diagonalisation of a symmetric matrix: (P orthogonal, D, html)."""
    A = sp.Matrix(A); n = A.rows
    assert A == A.T
    cols = []; diag = []
    h = "<p>$A$ is symmetric, so it is orthogonally diagonalizable (spectral theorem).</p>"
    cp = sp.factor((A - lam * sp.eye(n)).det())
    h += "<p>$\\det(A-\\lambda I)=%s$.</p>" % tex(cp)
    for val, mult, basis in sorted(A.eigenvects(), key=lambda e: float(sp.N(e[0]))):
        us, es, hh = gram_schmidt_html(basis)
        h += "<p>$\\lambda=%s$: basis %s. Orthonormalise inside the eigenspace → %s.</p>" % (
            tex(val), ", ".join("$%s$" % vec(list(v)) for v in basis),
            ", ".join("$%s$" % vec(list(e)) for e in es))
        cols += es; diag += [val] * len(es)
    P = sp.Matrix.hstack(*cols); D = sp.diag(*diag)
    assert sp.simplify(P.T * A * P - D) == sp.zeros(n)
    h += "<p>$P=%s,\\ D=%s$ and $P^{T}AP=D$ (eigenvectors of different eigenvalues are already orthogonal).</p>" % (mtx(sp.simplify(P)), mtx(D))
    return P, D, h
