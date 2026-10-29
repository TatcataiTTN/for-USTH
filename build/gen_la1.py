# -*- coding: utf-8 -*-
"""LA chapters 1-3: systems, matrices, determinants. All answers computed with sympy."""
import itertools, random
import sympy as sp
from qlib import tex, M, mat, aug, vec, colvec, system_tex, uniq_by_text, near_numbers, R, note
from la_common import *
from la_steps import mtx, row_reduce, solution_text

def mt(Mx_):  # inline matrix math
    return "$" + mtx(Mx_) + "$"

def numopts(val, rng, extra=(), fmt=M):
    """Correct + wrong numeric options as text."""
    a_ = sp.nsimplify(val)
    wr = []
    for e in extra:
        e = sp.nsimplify(e)
        if e != a_:
            wr.append(fmt(e))
    for c in near_numbers(a_, rng):
        wr.append("$" + c + "$")
    return fmt(a_), uniq_by_text(wr)

# ============================================================================== CHAPTER 1
SYS = {
    # Exercise Sheet 1, Ex. 3
    "S1-E3.1": ([[1, 1, 2], [2, 4, -3], [3, 6, -5]], [0, 1, 0], ["x", "y", "z"]),
    "S1-E3.2": ([[2, 2, 2], [-2, 5, 2], [8, 1, 4]], [0, 1, -1], ["x", "y", "z"]),
    "S1-E3.3": ([[1, 2, 0, -1, 1], [0, 3, 1, 0, -1], [0, 0, 1, 7, 0]], [1, 2, 1], ["x", "y", "z", "t", "w"]),
    "S1-E3.4": ([[1, -2, 1, -4], [1, 3, 7, 2], [1, -12, -11, -16]], [1, 2, 5], ["x", "y", "z", "t"]),
    "S1-E3.5": ([[2, -1, 3, 4], [1, 0, -2, 7], [3, -3, 1, 5], [2, 1, 4, 4]], [9, 11, 8, 10], ["I_1", "I_2", "I_3", "I_4"]),
    "S1-E3.6": ([[2, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 2]], [0, 0, 0, 5], ["u", "v", "w", "z"]),
}

def ask_system(B, ch, A, b, names, src, level=1, origin="src", intro="", which=None):
    A = sp.Matrix(A); b = sp.Matrix(b)
    kind, sol, free = solve_sys(A, b)
    n = A.cols
    stem_sys = intro + "\n$$" + system_tex(A, b, names) + "$$"
    R_, _, piv = row_reduce(A.row_join(b), n, True)
    expl_rr = "Gauss–Jordan on the augmented matrix gives $%s$." % mtx(R_, n)
    if kind == "unique":
        j = which if which is not None else B.rng.randrange(n)
        val = sol[j]
        others = [sol[i] for i in range(n) if i != j]
        c, wr = numopts(val, B.rng, extra=others + [sum(sol)])
        B.mcq(ch, "Solving systems", level, stem_sys + "\nWhat is $%s$?" % names[j], c, wr,
              expl_rr + " Reading the last column: $%s=%s$ (unique solution: $%s$)." % (names[j], tex(val), vec(list(sol))), src, origin)
        tot = sum(sol)
        c2, wr2 = numopts(tot, B.rng, extra=[sol[0], -tot])
        B.mcq(ch, "Solving systems", level, stem_sys + "\nWhat is the value of $%s$?" % "+".join(names), c2, wr2,
              expl_rr + " The unique solution is $%s$, so $%s=%s$." % (vec(list(sol)), "+".join(names), tex(tot)), src, origin)
    elif kind == "inf":
        sol2, fr = rename_free(sol, free)
        v = particular(sol, free, B.rng)
        bad = near_vectors(v, A, b, B.rng, 5)
        if len(bad) >= 3:
            B.mcq(ch, "Solving systems", level, stem_sys + "\nWhich vector $(%s)$ is a solution?" % ",".join(names),
                  "$" + vec(v) + "$", ["$" + vec(w) + "$" for w in bad[:3]],
                  expl_rr + " There are %d free variable(s), so there are infinitely many solutions; substituting each option into the equations, only $%s$ satisfies all of them." % (len(free), vec(v)),
                  src, origin)
        nf = len(free)
        B.mcq(ch, "Solving systems", level, stem_sys + "\nHow many free parameters does the general solution have?",
              "$%d$" % nf, ["$%d$" % z for z in sorted({0, 1, 2, 3, 4} - {nf})][:3],
              expl_rr + " Free variables = unknowns − pivots = $%d-%d=%d$." % (n, len(piv), nf), src, origin)
    else:
        B.mcq(ch, "Solving systems", level, stem_sys + "\nHow many solutions does the system have?",
              "None (inconsistent)", ["Exactly one", "Exactly two", "Infinitely many"],
              expl_rr + " The row $[0\\ \\cdots\\ 0\\mid c]$ with $c\\ne0$ means $0=c$: the system is inconsistent.", src, origin)

def ch1(B):
    ch = "c1"
    # ---- identification / concepts (hand-written, answers by reasoning)
    B.mcq(ch, "Linear equations", 1, "Which of the following is a linear equation in $x_1,x_2,x_3$?",
          "$\\pi x_1-2x_2+\\tfrac13x_3=\\sqrt[3]{71}$",
          ["$x_1^{-2}+x_2+8x_3=5$", "$x_1x_2+x_3=2$", "$x_1+\\sin x_2-x_3=0$"],
          "A linear equation has the form $a_1x_1+a_2x_2+a_3x_3=b$ with constant coefficients. $\\pi$ and $\\sqrt[3]{71}$ are constants; the other options contain $x_1^{-2}$, a product $x_1x_2$ or $\\sin x_2$.",
          "Exercise Sheet 1, Ex. 1", "src")
    B.mcq(ch, "Linear equations", 1, "Which of the following is NOT a linear equation in $x,y,z$?",
          "$xy+z=1$", ["$x-3y+\\sqrt5\\,z=2$", "$\\tfrac{x}{2}+y-\\tfrac{z}{7}=0$", "$2x=y-4z+9$"],
          "Products of unknowns make an equation non-linear; the other three are of the form $ax+by+cz=d$.", "Exercise Sheet 1, Ex. 1 (style)", "gen")
    B.mcq(ch, "Solution sets", 1, "A linear system can have exactly …",
          "no solution, one solution, or infinitely many solutions",
          ["no solution, one solution, or exactly two solutions", "one solution or infinitely many solutions, never none", "any finite number of solutions"],
          "A line/plane arrangement can be empty, a single point, or contain a line/plane; two solutions would force the whole line through them, hence infinitely many.", "Lecture 1 / Larson §1.1", "concept")
    B.mcq(ch, "Solution sets", 1, "A homogeneous system $Ax=0$ is always …",
          "consistent (it has at least the trivial solution)", ["inconsistent", "uniquely solvable", "of infinitely many solutions"],
          "$x=0$ always satisfies $Ax=0$. It has only this solution iff $\\operatorname{rank}A=n$.", "Lecture 1 / Larson §1.2", "concept")
    B.mcq(ch, "Solution sets", 2, "A consistent system has 3 equations and 5 unknowns. How many solutions does it have?",
          "infinitely many", ["exactly one", "exactly three", "exactly five"],
          "Rank $\\le3<5$, so at least $5-3=2$ free variables: infinitely many solutions.", "Lecture 1 / Larson §1.2", "concept")
    B.mcq(ch, "Row operations", 1, "Which is NOT an elementary row operation?",
          "multiply a row by $0$", ["swap two rows", "multiply a row by a non-zero constant", "add a multiple of one row to another row"],
          "Multiplying by $0$ destroys information (not reversible). The other three are the elementary row operations and do not change the solution set.", "Lecture 1", "concept")
    B.mcq(ch, "Row operations", 2, "After Gauss–Jordan elimination the leading entry of each non-zero row is $1$ and …",
          "it is the only non-zero entry in its column", ["all entries to its right are $0$", "it is the only non-zero entry in its row", "the matrix is symmetric"],
          "Reduced row-echelon form: leading 1's, each the only non-zero entry in its column, with zero rows at the bottom.", "Lecture 1 / Larson §1.2", "concept")
    B.mcq(ch, "Row operations", 2, "Gaussian elimination (without the reduced step) produces a matrix in …",
          "row-echelon form, then back-substitution finishes the solution", ["reduced row-echelon form directly", "diagonal form always", "column-echelon form"],
          "Gauss: eliminate below pivots → echelon form → back-substitute. Gauss–Jordan continues eliminating above pivots to reach RREF.", "Lecture 1", "concept")
    B.mcq(ch, "Rank", 2, "A system $Ax=b$ with $A\\in\\mathbb{R}^{m\\times n}$ is consistent iff …",
          "$\\operatorname{rank}A=\\operatorname{rank}[A\\mid b]$", ["$\\operatorname{rank}A=n$", "$\\operatorname{rank}[A\\mid b]=m$", "$\\det A\\neq0$"],
          "Kronecker–Capelli / rank criterion: $b$ must lie in the column space of $A$.", "Lecture 1", "concept")
    B.mcq(ch, "Rank", 2, "A consistent system with $n$ unknowns has a unique solution iff …",
          "$\\operatorname{rank}A=n$", ["$\\operatorname{rank}A<n$", "$m=n$", "$b=0$"],
          "No free variables ⇔ every column is a pivot column ⇔ $\\operatorname{rank}A=n$.", "Lecture 1", "concept")

    # ---- augmented matrices in RREF (Sheet 1, Ex. 2)
    RREFS = [
        ("S1-E2.1", [[1, 0, 0, 5], [0, 1, 0, -2], [0, 0, 1, 4]], 3),
        ("S1-E2.2", [[1, 0, 0, 4, -1], [0, 1, 0, 2, 6], [0, 0, 1, 3, 2]], 4),
        ("S1-E2.3", [[1, 6, 0, 0, 4, -2], [0, 0, 1, 0, 3, 1], [0, 0, 0, 1, 5, 2], [0, 0, 0, 0, 0, 0]], 5),
        ("S1-E2.4", [[1, 2, 0, 3, 0, 7], [0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 1, 2]], 5),
    ]
    for tag, Mm, n in RREFS:
        Mm = sp.Matrix(Mm); A = Mm[:, :n]; b = Mm[:, n]
        kind, sol, free = solve_sys(A, b)
        nf = len(free)
        stem = "The augmented matrix of a system in $x_1,\\dots,x_%d$ is already in reduced row-echelon form:\n$$%s$$" % (n, mtx(Mm, n))
        if kind == "unique":
            B.mcq(ch, "Reading an RREF", 1, stem + "\nThe system has …", "exactly one solution: $%s$" % vec(list(sol)),
                  ["no solution", "infinitely many solutions", "exactly one solution: $%s$" % vec([-z for z in sol])],
                  "Every unknown is a pivot variable, so the last column gives the solution directly.", "Exercise Sheet 1, Ex. 2", "src")
        else:
            B.mcq(ch, "Reading an RREF", 1, stem + "\nHow many free parameters does the general solution have?", "$%d$" % nf,
                  ["$%d$" % z for z in sorted({0, 1, 2, 3} - {nf})][:3],
                  "Pivot columns: %s. The other %d unknown(s) are free." % (", ".join(str(p + 1) for p in range(n) if any(Mm[i, p] == 1 and all(Mm[r, p] == 0 for r in range(Mm.rows) if r != i) for i in range(Mm.rows)) and p not in free), nf),
                  "Exercise Sheet 1, Ex. 2", "src")
            sol2, fr = rename_free(sol, free)
            v = particular(sol, free, B.rng)
            bad = near_vectors(v, A, b, B.rng, 5)
            if len(bad) >= 3:
                B.mcq(ch, "Reading an RREF", 2, stem + "\nWhich vector is a solution of the system?", "$" + vec(v) + "$", ["$" + vec(w) + "$" for w in bad[:3]],
                      "Give values to the free variables and solve for the pivot variables; $%s$ satisfies every row." % vec(v), "Exercise Sheet 1, Ex. 2", "src")

    # ---- Exercise Sheet 1 Ex. 3 systems
    for tag, (A, b, names) in SYS.items():
        ask_system(B, ch, A, b, names, "Exercise Sheet 1, Ex. %s" % tag.split("E")[1], level=1 if len(names) == 3 else 2,
                   intro="Solve the system by Gauss–Jordan elimination.")

    # ---- Ex. 4 parameter a
    A4 = sp.Matrix([[1, 2, -3], [3, -1, 5], [4, 1, a ** 2 - 14]]); b4 = sp.Matrix([4, 2, a + 2])
    cls = classify_param(A4, b4, a)
    gen = cls["generic"]
    crit = {c: v for c, v in cls.items() if c != "generic" and v != gen}
    stem4 = "Consider $$%s$$" % system_tex(A4, b4, ["x", "y", "z"])
    for want, label in (("none", "no solution"), ("inf", "infinitely many solutions")):
        vals = [c for c in crit if crit[c] == want]
        ct, wr = set_options(vals, list(crit.keys()), a, B.rng)
        B.mcq(ch, "Systems with a parameter", 3, stem4 + "\nFor which real $a$ does the system have %s?" % label, ct, wr,
              "$\\det\\begin{bmatrix}1&2&-3\\\\3&-1&5\\\\4&1&a^2-14\\end{bmatrix}=-7(a^2-16)$, so only $a=\\pm4$ need checking. Row 3 equals row 1 + row 2 in the coefficients; the right-hand sides then agree iff $a+2=6$, i.e. $a=4$. Hence $a=4$: infinitely many solutions; $a=-4$: none; otherwise unique.",
              "Exercise Sheet 1, Ex. 4", "src")
    # ---- Ex. 5 consistency condition
    A5 = sp.Matrix([[-1, 2, -3, 1], [2, -1, 2, -3], [3, 0, 1, -5]])
    ln = A5.T.nullspace()[0]
    ln = ln * sp.ilcm(*[sp.fraction(z)[1] for z in ln])
    cond = "%s=0" % "".join(("+" if c > 0 else "-") + ("" if abs(c) == 1 else tex(abs(c))) + "b_%d" % (i + 1) for i, c in enumerate(ln) if c != 0).lstrip("+")
    alt = []
    for flip in range(3):
        l2 = list(ln); l2[flip] = -l2[flip]
        alt.append("%s=0" % "".join(("+" if c > 0 else "-") + ("" if abs(c) == 1 else tex(abs(c))) + "b_%d" % (i + 1) for i, c in enumerate(l2) if c != 0).lstrip("+"))
    B.mcq(ch, "Systems with a parameter", 3,
          "For which right-hand sides is the system consistent?\n$$%s$$" % system_tex(A5, sp.Matrix(sp.symbols("b1 b2 b3")), ["x_1", "x_2", "x_3", "x_4"]),
          "$" + cond + "$", ["$" + z + "$" for z in alt],
          "Row-reducing $[A\\mid b]$, the third row becomes $[0\\ 0\\ 0\\ 0\\mid %s]$, so consistency requires $%s$ (a vector $c$ with $c^TA=0$ gives the condition $c\\cdot b=0$)." % (tex(sum(c * sp.Symbol("b%d" % (i + 1)) for i, c in enumerate(ln))), cond),
          "Exercise Sheet 1, Ex. 5", "src")
    # ---- Ex. 6 parameter m
    A6 = sp.Matrix([[1, m, 1], [2, m - 1, 3], [m, 1, 3]]); b6 = sp.Matrix([m, 1, 2 * m - 3])
    cls = classify_param(A6, b6, m)
    gen = cls["generic"]; crit = {c: v for c, v in cls.items() if c != "generic" and v != gen}
    stem6 = "Consider $$%s$$" % system_tex(A6, b6, ["x", "y", "z"])
    for want, label in (("none", "no solution"), ("inf", "infinitely many solutions")):
        vals = [c for c in crit if crit[c] == want]
        if vals or want == "none":
            ct, wr = set_options(vals, list(crit.keys()), m, B.rng)
            B.mcq(ch, "Systems with a parameter", 3, stem6 + "\nFor which real $m$ does the system have %s?" % label, ct, wr,
                  "Compute $\\det$ of the coefficient matrix; its real roots are the only critical values. At each critical value compare $\\operatorname{rank}A$ with $\\operatorname{rank}[A\\mid b]$: " +
                  "; ".join("$m=%s$ → %s" % (tex(c), {"none": "no solution", "inf": "infinitely many", "unique": "unique"}[crit[c]]) for c in sorted(crit, key=float)) + ". Every other $m$ gives a unique solution.",
                  "Exercise Sheet 1, Ex. 6", "src")

    # ---- past-paper systems (Final exams)
    PAPERS = [
        ("Final 2024–25 Shift 1, Q1", sp.Matrix([[1, 2, 1, 1], [0, 1, 3, 0], [2, 5, 5, k]]), sp.Matrix([4, -1, 8]), k, 3, "inconsistent", ["x_1", "x_2", "x_3", "x_4"]),
        ("Final 2024–25 Shift 2, Q1", sp.Matrix([[1, 0, 2, -2], [0, 2, 1, -1], [2, 0, 4, k - 5]]), sp.Matrix([1, -1, 4]), k, 1, "consistent", ["x_1", "x_2", "x_3", "x_4"]),
        ("Final 2023–24 Shift 2, Q1", sp.Matrix([[1, 1, 1], [1, 2, 3], [2, k, 1]]), sp.Matrix([0, 4, 3]), k, -1, "inconsistent", ["x_1", "x_2", "x_3"]),
        ("Final 2023–24 Shift 1, Q1", sp.Matrix([[1, 0, -3], [3, 1, -2], [k, k, 1]]), sp.Matrix([-2, 5, 4]), k, 2, "consistent", ["x_1", "x_2", "x_3"]),
        ("Final 2022–23 Group 1, Q1", sp.Matrix([[1, -2, 1], [0, 2, -8], [-4, 5, m]]), sp.Matrix([0, 8, -m]), m, 9, "inconsistent", ["x", "y", "z"]),
        ("Final 2019–20, Q1", sp.Matrix([[1, 1, 1], [1, 2, 4], [2, -3, -m]]), sp.Matrix([4, 12, m + 3]), m, 1, "inconsistent", ["x", "y", "z"]),
        ("Final 2018–19 (D, E, G), Q1", sp.Matrix([[1, -m, 3], [2, 4, -4], [1, -2, 2]]), sp.Matrix([5, 0, 4]), m, 3, "unique", ["x", "y", "z"]),
        ("Final 2018–19 (A, B, C, AE), Q1", sp.Matrix([[5, 2, 5, 1], [1, 2, 1, -3], [3, 6, m + 2, -9]]), sp.Matrix([9, -3, 6]), m, 4, "inconsistent", ["x_1", "x_2", "x_3", "x_4"]),
    ]
    for src, Ap, bp, sym, val, want, names in PAPERS:
        Av, bv = Ap.subs(sym, val), bp.subs(sym, val)
        ask_system(B, ch, Av, bv, names, src + "(a)", level=2, intro="Exam question (parameter fixed to $%s=%s$). Solve:" % (tex(sym), tex(val)))
        cls = classify_param(Ap, bp, sym)
        gen = cls["generic"]; crit = {c: v for c, v in cls.items() if c != "generic" and v != gen}
        cat = {"inconsistent": "none", "consistent": None, "unique": "unique"}[want]
        if want == "consistent":
            vals = [c for c in crit if crit[c] == "none"]; wanted = "consistent"
        else:
            vals = [c for c in crit if crit[c] == cat]
        pool = list(crit.keys()) or [0]
        if want == "consistent":
            # consistent for all except the 'none' values -> phrase as complement question: which k make it INCONSISTENT
            ct, wr = set_options(vals, pool, sym, B.rng)
            qtxt = "inconsistent"
        elif want == "unique" and gen == "unique":
            vals = [c for c in crit if crit[c] != "unique"]
            ct, wr = set_options(vals, pool, sym, B.rng)
            qtxt = "NOT a unique solution (no solution or infinitely many)"
        else:
            ct, wr = set_options(vals, pool, sym, B.rng)
            qtxt = "no solution"
        if len(wr) >= 3:
            B.mcq(ch, "Systems with a parameter", 3,
                  "$$%s$$\nFor which values of $%s$ does the system have %s?" % (system_tex(Ap, bp, names), tex(sym), qtxt), ct, wr,
                  "Critical values of $%s$ come from the minors of $A$ and $[A\\mid b]$: %s. Compare ranks there: %s; any other value behaves like a generic one (%s)." % (
                      tex(sym), ", ".join("$%s=%s$" % (tex(sym), tex(c)) for c in sorted(crit, key=float)) or "none",
                      "; ".join("$%s=%s$ → %s" % (tex(sym), tex(c), {"none": "inconsistent", "inf": "infinitely many", "unique": "unique"}[crit[c]]) for c in sorted(crit, key=float)) or "n/a",
                      {"none": "inconsistent", "inf": "infinitely many", "unique": "unique solution"}[gen]),
                  src + "(b)", "src")

    # ---- randomised unique-solution systems and rank / free variables
    rng = B.rng
    made = 0
    while made < 8:
        while True:
            A = sp.Matrix(3, 3, lambda i, j: rng.randint(-3, 3))
            if A.det() != 0 and abs(A.det()) <= 12:
                break
        sol = sp.Matrix([rng.randint(-3, 3) for _ in range(3)])
        b = A * sol
        before = len(B.items)
        ask_system(B, ch, A, b, ["x", "y", "z"], "Generated (same style as Sheet 1, Ex. 3)", level=1, origin="gen", intro="Solve:")
        made += len(B.items) - before
    for _ in range(5):
        A = sp.Matrix(3, 4, lambda i, j: rng.randint(-2, 3))
        A[2, :] = A[0, :] * rng.choice([1, 2, -1]) + A[1, :] * rng.choice([0, 1, -2])
        r = A.rank()
        B.mcq(ch, "Rank", 2, "For the homogeneous system $Ax=0$ with $A=%s$, how many free variables are there?" % mtx(A),
              "$%d$" % (4 - r), ["$%d$" % z for z in sorted({0, 1, 2, 3, 4} - {4 - r})][:3],
              "Row 3 is a combination of rows 1 and 2 by construction; row-reducing gives $\\operatorname{rank}A=%d$. Free variables $=n-\\operatorname{rank}A=4-%d=%d$." % (r, r, 4 - r),
              "Generated (rank / nullity)", "gen")

# ============================================================================== CHAPTER 2
def ch2(B):
    ch = "c2"
    rng = B.rng

    # ---- build-time proof-by-experiment of the theory claims used below (random integer matrices)
    def _rand(n, sym=False):
        Z = sp.Matrix(n, n, lambda i, j: rng.randint(-3, 3))
        return (Z + Z.T) if sym else Z
    ok_noncomm = False; ok_sym_ab = False; ok_sym_prod = False; ok_sym_abab = False
    for _ in range(40):
        P1, P2 = _rand(3), _rand(3)
        assert (P1 + P2) ** 2 == P1 * (P1 + P2) + P2 * (P1 + P2) == P1 ** 2 + P1 * P2 + P2 * P1 + P2 ** 2 == (P1 + P2) * (P2 + P1)
        ok_noncomm |= ((P1 + P2) ** 2 != P1 ** 2 + 2 * P1 * P2 + P2 ** 2)
        S1, S2 = _rand(3, True), _rand(3, True)
        assert (S1 * S2 * S1).T == S1 * S2 * S1 and (S1 ** 2 - S2 ** 2).T == S1 ** 2 - S2 ** 2
        ok_sym_ab |= ((S1 * S2).T != S1 * S2)
        ok_sym_prod |= (((S1 + S2) * (S1 - S2)).T != (S1 + S2) * (S1 - S2))
        ok_sym_abab |= ((S1 * S2 * S1 * S2).T != S1 * S2 * S1 * S2)
    assert ok_noncomm and ok_sym_ab and ok_sym_prod and ok_sym_abab
    # ---- sizes (Sheet 2, Ex. 1)
    dims = dict(A=(4, 5), B=(4, 5), C=(5, 2), D=(4, 2), E=(5, 5))
    def mm(l, r): return (l[0], r[1]) if l[1] == r[0] else None
    def add(l, r): return l if l == r else None
    exprs = {
        "BA": lambda: mm(dims["B"], dims["A"]),
        "AC + D": lambda: (lambda p: add(p, dims["D"]) if p else None)(mm(dims["A"], dims["C"])),
        "AE + B": lambda: (lambda p: add(p, dims["B"]) if p else None)(mm(dims["A"], dims["E"])),
        "AB + B": lambda: (lambda p: add(p, dims["B"]) if p else None)(mm(dims["A"], dims["B"])),
        "E^{T}A": lambda: mm((5, 5), dims["A"]),
        "(A^{T}+E)D": lambda: (lambda s: mm(s, dims["D"]) if s else None)(add((5, 4), dims["E"])),
        "E(AC)": lambda: (lambda p: mm(dims["E"], p) if p else None)(mm(dims["A"], dims["C"])),
        "2E(A+B)": lambda: (lambda s: mm(dims["E"], s) if s else None)(add(dims["A"], dims["B"])),
    }
    stem = "Let $A,B$ be $4\\times5$, $C$ be $5\\times2$, $D$ be $4\\times2$ and $E$ be $5\\times5$. "
    B.mcq(ch, "Sizes of products", 1, stem + "Which of the following is defined?",
          "$AC+D$ (a $4\\times2$ matrix)", ["$BA$", "$AB+B$", "$E^{T}A$"],
          "$AC$ is $(4\\times5)(5\\times2)=4\\times2$, the same size as $D$, so the sum exists. $BA$: $5\\neq4$. $AB$: $5\\neq4$. $E^TA$: $(5\\times5)(4\\times5)$ undefined.",
          "Exercise Sheet 2, Ex. 1", "src")
    B.mcq(ch, "Sizes of products", 1, stem + "What is the size of $AE+B$?",
          "$4\\times5$", ["$5\\times5$", "$4\\times4$", "it is not defined"],
          "$AE=(4\\times5)(5\\times5)=4\\times5$ and $B$ is $4\\times5$, so $AE+B$ is $4\\times5$.", "Exercise Sheet 2, Ex. 1", "src")
    B.mcq(ch, "Sizes of products", 2, stem + "Which of the following is NOT defined?",
          "$(A^{T}+E)D$", ["$AC+D$", "$AE+B$", "$BE$"],
          "$A^T$ is $5\\times4$ and $E$ is $5\\times5$: they cannot be added, so $(A^T+E)D$ is undefined. $BE=(4\\times5)(5\\times5)$ is defined.",
          "Exercise Sheet 2, Ex. 1", "src")
    # ---- numeric matrices Ex. 2
    A = sp.Matrix([[3, 0], [-1, 2], [1, 1]]); Bm = sp.Matrix([[4, -1], [0, 2]]); C = sp.Matrix([[1, 4, 2], [3, 1, 5]])
    D = sp.Matrix([[1, 5, 2], [-1, 0, 1], [3, 2, 4]]); E = sp.Matrix([[6, 1, 3], [-1, 1, 2], [4, 1, 3]])
    given = "$A=%s,\\ B=%s,\\ C=%s,\\ D=%s,\\ E=%s$" % tuple(mtx(z) for z in (A, Bm, C, D, E))
    def mq(topic, lvl, ask, res, expl, src="Exercise Sheet 2, Ex. 2", wrongs=None):
        wr = []
        if isinstance(res, sp.MatrixBase):
            for _ in range(10):
                wr.append(mt(perturb(res, rng)))
            wr.append(mt(res.T) if res.T != res else mt(-res))
            c = mt(res)
        else:
            c, wr0 = numopts(res, rng, extra=wrongs or [])
            wr = wr0
        B.mcq(ch, topic, lvl, given + "\n" + ask, c, uniq_by_text(wr), expl, src, "src")
    mq("Matrix products", 1, "Compute $AB$.", A * Bm, "$AB=(3\\times2)(2\\times2)$: each row of $A$ times $B$: $%s$." % mtx(A * Bm))
    B.mcq(ch, "Matrix products", 1, given + "\nWhich of $AB$ and $BA$ exists?", "only $AB$", ["only $BA$", "both", "neither"],
          "$A$ is $3\\times2$ and $B$ is $2\\times2$: $AB$ is $3\\times2$; $BA$ needs $2=3$, which fails.", "Exercise Sheet 2, Ex. 2", "src")
    mq("Matrix products", 2, "Compute $AC$ (a $3\\times3$ matrix).", A * C, "Row $i$ of $AC$ = (row $i$ of $A$)$\\cdot C$: $AC=%s$." % mtx(A * C))
    mq("Matrix products", 2, "Compute $CA$.", C * A, "$CA=(2\\times3)(3\\times2)$ is $2\\times2$: $CA=%s$." % mtx(C * A))
    mq("Trace", 1, "Compute $\\operatorname{Tr}(DD^{T})$.", (D * D.T).trace(), "$\\operatorname{Tr}(DD^T)=\\sum_{i,j}d_{ij}^2=%s$ (sum of squares of all entries)." % tex((D * D.T).trace()),
       wrongs=[D.trace(), (D * D).trace(), sum(D)])
    mq("Trace", 2, "Compute $\\operatorname{Tr}(3D-2E^{T})$.", (3 * D - 2 * E.T).trace(), "$\\operatorname{Tr}(3D-2E^T)=3\\operatorname{Tr}D-2\\operatorname{Tr}E=3(%s)-2(%s)=%s$." % (tex(D.trace()), tex(E.trace()), tex((3 * D - 2 * E.T).trace())),
       wrongs=[3 * D.trace() + 2 * E.trace(), D.trace() - E.trace()])
    mq("Transpose", 2, "Compute $D^{T}E^{T}-(ED)^{T}$.", sp.zeros(3, 3), "$(ED)^T=D^TE^T$, so the difference is the zero matrix.", wrongs=None)
    mq("Matrix products", 2, "Compute $(C^{T}B)A^{T}$.", (C.T * Bm) * A.T, "$C^TB$ is $3\\times2$, times $A^T$ ($2\\times3$) gives $%s$." % mtx((C.T * Bm) * A.T))
    mq("Trace", 3, "Compute $\\operatorname{Tr}\\big((C^{T}B)A^{T}\\big)$.", ((C.T * Bm) * A.T).trace(), "Add the diagonal of $(C^TB)A^T=%s$: $%s$." % (mtx((C.T * Bm) * A.T), tex(((C.T * Bm) * A.T).trace())),
       wrongs=[sum((C.T * Bm) * A.T), -((C.T * Bm) * A.T).trace()])
    # ---- Ex. 3
    A3 = sp.Matrix(2, 2, lambda i, j: (i + 1) + (j + 1)); B3 = sp.Matrix(2, 2, lambda i, j: (-1) ** ((i + 1) + (j + 1)))
    B.mcq(ch, "Matrix products", 2, "Let $a_{ij}=i+j$ and $b_{ij}=(-1)^{i+j}$ be $2\\times2$ matrices. Then $AB=%s$ and $BA$ equals …" % mtx(A3 * B3),
          mt(B3 * A3), [mt(A3 * B3), mt(perturb(B3 * A3, rng)), mt(-(B3 * A3))],
          "$A=%s$, $B=%s$: $AB=%s\\neq BA=%s$. Matrix multiplication is not commutative." % (mtx(A3), mtx(B3), mtx(A3 * B3), mtx(B3 * A3)), "Exercise Sheet 2, Ex. 3", "src")
    # ---- Ex. 4
    B.mcq(ch, "Algebra of matrices", 2, "For square matrices $A,B$ which of these is NOT guaranteed to equal $(A+B)^2$?",
          "$A^2+2AB+B^2$", ["$A(A+B)+B(A+B)$", "$A^2+AB+BA+B^2$", "$(A+B)(B+A)$"],
          "Expanding gives $A^2+AB+BA+B^2$. Since $AB\\neq BA$ in general, $A^2+2AB+B^2$ fails. ($(A+B)(B+A)$ is also $(A+B)^2$ because $A+B=B+A$.)", "Exercise Sheet 2, Ex. 4", "src")
    # ---- Ex. 7 powers
    Ap = sp.Matrix([[R(1, 2), R(1, 2)], [R(1, 2), R(1, 2)]]); Bp = sp.diag(1, -1); Cp = Ap * Bp
    assert Ap * Ap == Ap and Bp * Bp == sp.eye(2) and Cp * Cp == sp.zeros(2, 2) and Cp != sp.zeros(2, 2)
    B.mcq(ch, "Powers", 2, "For $A=%s$, what is $A^{k}$ ($k\\ge1$)?" % mtx(Ap), mt(Ap), [mt(Ap * 2), mt(sp.eye(2)), mt(sp.diag(R(1, 2), R(1, 2)))],
          "$A^2=%s=A$ (it is a projection). Hence $A^k=A$ for all $k\\ge1$." % mtx(Ap * Ap), "Exercise Sheet 2, Ex. 7", "src")
    B.mcq(ch, "Powers", 2, "For $B=%s$, what is $B^{k}$?" % mtx(Bp), "$B^k=I$ for even $k$ and $B^k=B$ for odd $k$",
          ["$B^k=B$ for all $k$", "$B^k=I$ for all $k$", "$B^k=2^{k}B$"],
          "$B^2=%s=I$, so powers alternate between $B$ (odd $k$) and $I$ (even $k$)." % mtx(Bp * Bp), "Exercise Sheet 2, Ex. 7", "src")
    B.mcq(ch, "Powers", 3, "For $C=AB$ with $A=%s$, $B=%s$, what is $C^{k}$ for $k\\ge2$?" % (mtx(Ap), mtx(Bp)),
          "$C^k=0$ (the zero matrix)", ["$C^k=C$", "$C^k=2^{k-1}C$", "$C^k=I$"],
          "$C=AB=%s$ and $C^2=%s=0$, so $C$ is nilpotent and $C^k=0$ for every $k\\ge2$. (Do not confuse it with $A$, which satisfies $A^2=A$.)" % (mtx(Cp), mtx(Cp * Cp)), "Exercise Sheet 2, Ex. 7", "src")
    # ---- inverses (Ex. 8)
    b8 = sp.Matrix([-1, 2, 7])
    INV = {
        "A_1": sp.Matrix([[1, 0, 0], [1, 1, 1], [0, 0, 1]]),
        "A_2": sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]]),
        "A_3": sp.Matrix([[1, 1, 1], [1, 2, 2], [1, 2, 3]]),
        "A_4": sp.Matrix([[0, 0, 1], [0, 1, 1], [1, 1, 1]]),
        "A_5": sp.Matrix([[sp.sqrt(2), 3 * sp.sqrt(2), 0], [-4 * sp.sqrt(2), sp.sqrt(2), 0], [0, 0, 1]]),
        "A_6": sp.Matrix([[R(1, 5), R(1, 5), R(-2, 5)], [R(1, 5), R(1, 5), R(1, 10)], [R(1, 5), R(-4, 5), R(1, 10)]]),
    }
    for name, Mt in INV.items():
        inv = sp.simplify(Mt.inv()); x = sp.simplify(inv * b8)
        B.mcq(ch, "Inverse (Gauss–Jordan)", 2, "Use Gauss–Jordan on $[A\\mid I]$ to invert $%s=%s$. What is $%s^{-1}$?" % (name, mtx(Mt), name),
              mt(inv), [mt(perturb(inv, rng)) for _ in range(6)] + [mt(Mt.T), mt(-inv)],
              "Row-reduce $[A\\mid I]\\to[I\\mid A^{-1}]$: $%s^{-1}=%s$ (check $AA^{-1}=I$)." % (name, mtx(inv)), "Exercise Sheet 2, Ex. 8", "src")
        sx = vec(list(x))
        wr = []
        for _ in range(8):
            xx = list(x); i = rng.randrange(3); xx[i] = sp.nsimplify(xx[i] + rng.choice([-1, 1, 2]))
            wr.append("$" + vec(xx) + "$")
        wr.append("$" + vec(list(Mt.T.inv() * b8)) + "$")
        B.mcq(ch, "Inverse (Gauss–Jordan)", 2, "With $%s=%s$, solve $%sx=b$ for $b=(-1,2,7)^T$ using the inverse." % (name, mtx(Mt), name),
              "$" + sx + "$", uniq_by_text(wr), "$x=%s^{-1}b=%s$." % (name, mtx(x)), "Exercise Sheet 2, Ex. 8", "src")
    # ---- Ex. 9 special inverses
    A91 = sp.Matrix([[0, 0, 0, 1], [0, 0, 2, 0], [0, 3, 0, 0], [4, 0, 0, 0]])
    B.mcq(ch, "Inverse (special forms)", 2, "For the anti-diagonal matrix $A=%s$, the inverse is …" % mtx(A91), mt(A91.inv()),
          [mt(A91.T), mt(A91 * R(1, 4)), mt(sp.diag(1, R(1, 2), R(1, 3), R(1, 4)))],
          "$A$ maps $e_1\\mapsto 4e_4,\\ e_2\\mapsto3e_3,\\ e_3\\mapsto2e_2,\\ e_4\\mapsto e_1$; invert each: $A^{-1}=%s$ (anti-diagonal with reciprocal entries)." % mtx(A91.inv()), "Exercise Sheet 2, Ex. 9", "src")
    c_ = sp.Symbol("c")
    A10 = sp.Matrix([[2, c_, c_], [c_, c_, c_], [8, 7, c_]])
    dd = sp.factor(A10.det()); roots = sp.solve(A10.det(), c_)
    wr = [("$c\\in\\{%s\\}$" % ",".join(tex(z) for z in w)) for w in ([0, 8], [2, 7], [0, 7], [-2, 8])]
    correct = "$c\\in\\{%s\\}$" % ",".join(tex(z) for z in sorted(roots, key=float))
    B.mcq(ch, "Invertibility", 3, "For which $c$ is $A=%s$ NOT invertible?" % mtx(A10), correct, [w for w in wr if w != correct][:3],
          "$\\det A=%s$, which is $0$ exactly for $c=%s$ (then two rows/columns become dependent)." % (tex(dd), ",".join(tex(z) for z in sorted(roots, key=float))), "Exercise Sheet 2, Ex. 10", "src")
    # ---- Ex. 12-14 and conceptual
    B.mcq(ch, "Properties", 2, "Which statement is true for real matrices?",
          "$A^2=0$ is possible with $A\\ne0$, but $A^TA=0$ forces $A=0$",
          ["$A^TA=0$ is possible with $A\\ne0$, but $A^2=0$ forces $A=0$", "Both $A^2=0$ and $A^TA=0$ force $A=0$", "Both are possible with $A\\ne0$"],
          "Example $A=\\begin{bmatrix}0&1\\\\0&0\\end{bmatrix}$ has $A^2=0$. But $\\operatorname{Tr}(A^TA)=\\sum a_{ij}^2=0$ forces every entry to be $0$.", "Exercise Sheet 2, Ex. 12", "src")
    B.mcq(ch, "Properties", 2, "If $A=A^T$ and $B=B^T$, which matrix is certainly symmetric?",
          "$ABA$", ["$(A+B)(A-B)$", "$AB$", "$ABAB$"],
          "$(ABA)^T=A^TB^TA^T=ABA$. In general $(A+B)(A-B)$, $AB$ and $ABAB$ are not symmetric (their transposes reverse the order).", "Exercise Sheet 2, Ex. 14", "src")
    B.mcq(ch, "Properties", 2, "If $A=A^T$ and $B=B^T$, which matrix is certainly symmetric?",
          "$A^2-B^2$", ["$(A+B)(A-B)$", "$AB$", "$ABAB$"], "$(A^2-B^2)^T=(A^T)^2-(B^T)^2=A^2-B^2$.", "Exercise Sheet 2, Ex. 14", "src")
    B.mcq(ch, "Properties", 2, "If the inverse of $A^2$ is $B$, then the inverse of $A$ is …", "$AB$", ["$BA^2$", "$B^2$", "$A^{-1}$ need not exist"],
          "$A(AB)=A^2B=I$, so $AB$ is a right inverse of the square matrix $A$; for square matrices that makes $AB=A^{-1}$. In particular $A$ is invertible whenever $A^2$ is.", "Exercise Sheet 2, Ex. 13", "src")
    B.mcq(ch, "Properties", 1, "$(AB)^{-1}=$", "$B^{-1}A^{-1}$", ["$A^{-1}B^{-1}$", "$(A^{-1}B)^{-1}$", "$A^{-1}+B^{-1}$"],
          "Check: $(AB)(B^{-1}A^{-1})=A(BB^{-1})A^{-1}=I$ — the order reverses.", "Lecture 2", "concept")
    B.mcq(ch, "Properties", 1, "$(AB)^{T}=$", "$B^{T}A^{T}$", ["$A^{T}B^{T}$", "$(A^{T}B)^T$", "$AB$"], "The transpose reverses the order of a product.", "Lecture 2", "concept")
    B.mcq(ch, "Properties", 2, "For $2\\times2$ matrices, if $AB=BA$ for EVERY $B$, then $A$ is …", "a scalar multiple of $I$",
          ["any symmetric matrix", "any diagonal matrix", "any invertible matrix"],
          "Testing with $B=E_{11}$ and $E_{12}$ gives $a=d$ and $b=c=0$.", "Exercise Sheet 2, Ex. 5", "src")
    # ---- invertibility conditions
    B.mcq(ch, "Invertibility", 1, "Which condition is NOT equivalent to '$A$ ($n\\times n$) is invertible'?", "$Ax=b$ has a solution for some $b$",
          ["$Ax=0$ has only $x=0$", "$Ax=b$ has a unique solution for every $b$", "$\\operatorname{rank}A=n$"],
          "Consistency for a single $b$ says nothing (e.g. $b=0$ always works).", "Exercise Sheet 2 (Recall)", "concept")
    # ---- random inverses & products
    for _ in range(6):
        while True:
            Ar = sp.Matrix(2, 2, lambda i, j: rng.randint(-4, 5))
            if Ar.det() not in (0,) and abs(Ar.det()) <= 6:
                break
        inv = Ar.inv()
        B.mcq(ch, "Inverse (2×2 formula)", 1, "Find $A^{-1}$ for $A=%s$." % mtx(Ar), mt(inv),
              [mt(sp.Matrix([[Ar[1, 1], Ar[0, 1]], [Ar[1, 0], Ar[0, 0]]]) / Ar.det()), mt(Ar.adjugate()), mt(perturb(inv, rng)), mt(-inv), mt(inv.T), mt(perturb(inv, rng))],
              "For $2\\times2$: $A^{-1}=\\frac{1}{ad-bc}\\begin{bmatrix}d&-b\\\\-c&a\\end{bmatrix}$ with $\\det A=%s$." % tex(Ar.det()), "Generated (2×2 inverse)", "gen")
    for _ in range(4):
        Ar = sp.Matrix(2, 3, lambda i, j: rng.randint(-3, 4)); Br = sp.Matrix(3, 2, lambda i, j: rng.randint(-3, 4))
        res = Ar * Br
        B.mcq(ch, "Matrix products", 1, "Compute $AB$ for $A=%s$, $B=%s$." % (mtx(Ar), mtx(Br)), mt(res),
              [mt(perturb(res, rng)), mt(res.T), mt(perturb(res, rng))], "Entry $(i,j)$ is (row $i$ of $A$)·(column $j$ of $B$): $AB=%s$." % mtx(res), "Generated (products)", "gen")
    # ---- exam matrices
    A2k = sp.Matrix([[4, 1, 3], [1, k, 1], [-1, 0, -1]])
    inv2 = A2k.subs(k, 2).inv()
    B.mcq(ch, "Inverse (Gauss–Jordan)", 3, "Exam: $A=%s$ with $k=2$. The entry $(A^{-1})_{23}$ is" % mtx(A2k.subs(k, 2)),
          M(inv2[1, 2]), [M(-inv2[1, 2])] + [M(sp.nsimplify(inv2[1, 2] + d)) for d in (1, -1, R(1, 2))],
          "$A^{-1}=%s$, so the $(2,3)$ entry is $%s$." % (mtx(inv2), tex(inv2[1, 2])), "Final 2024–25 Shift 1, Q2(b)", "src")
    A2s = sp.Matrix([[1, 2, 0], [1, 1, k], [1, 0, 2]])
    dv = A2s.subs(k, 3).det()
    B.mcq(ch, "Determinant rules", 3, "Exam: $A=%s$ with $k=3$. Compute $\\det(2A^2)$." % mtx(A2s.subs(k, 3)),
          M(8 * dv ** 2), [M(dv ** 2), M(2 * dv ** 2), M(8 * dv), M(64 * dv ** 2)],
          "For $n\\times n$: $\\det(cA)=c^n\\det A$ and $\\det(A^2)=(\\det A)^2$. Here $n=3$, $\\det A=%s$: $\\det(2A^2)=8(%s)^2=%s$." % (tex(dv), tex(dv), tex(8 * dv ** 2)), "Final 2024–25 Shift 2, Q2(b)", "src")
    A2c = sp.Matrix([[5, 2, -1], [2, 1, -1], [2, 0, 1]]); invc = A2c.inv()
    B.mcq(ch, "Inverse (Gauss–Jordan)", 3, "Exam: for $A=%s$, which is $A^{-1}$?" % mtx(A2c), mt(invc),
          [mt(perturb(invc, rng)), mt(perturb(invc, rng)), mt(invc.T)], "Row-reduce $[A\\mid I]$. $\\det A=%s$ and $A^{-1}=%s$." % (tex(A2c.det()), mtx(invc)), "Final 2023–24 Shift 1, Q2(b)", "src")

# ============================================================================== CHAPTER 3
def ch3(B):
    ch = "c3"
    rng = B.rng
    MATS = {
        "S3-E1": sp.Matrix([[1, 4, -2], [0, -3, 1], [1, 1, -1]]),
        "S3-E2": sp.Matrix([[2, 0, -1, 4], [-1, 2, 0, 3], [3, 0, 1, 2], [-2, 0, 3, 1]]),
        "S3-E3": sp.Matrix([[-4, 1, 2, 3], [1, -2, 1, 2], [2, -1, 3, 4], [1, 2, 2, -1]]),
        "S3-E4": sp.Matrix([[-1, 1, -1, 0, 0], [0, 1, -1, 0, 1], [1, 0, 1, -1, 0], [0, -1, 0, 1, -1], [0, 1, 1, -1, 1]]),
    }
    for tag, Mt in MATS.items():
        d = Mt.det()
        c, wrt = numopts(d, rng, extra=[-d, perturb(Mt, rng).det(), perturb(Mt, rng).det()])
        B.mcq(ch, "Computing determinants", 1 if Mt.rows == 3 else 2 if Mt.rows == 4 else 3,
              "Find $\\det A$ for $A=%s$." % mtx(Mt), c, wrt,
              "Row-reduce (or expand along the row/column with most zeros). Result: $\\det A=%s$." % tex(d), "Exercise Sheet 3, Ex. %s" % tag[-1], "src")
    A5 = sp.Matrix([[1, 0, -4], [0, 3, 2], [-2, 7, 6]]); d5 = A5.det()
    st = "Let $A=%s$ with $\\det A=%s$. " % (mtx(A5), tex(d5))
    items = [("$|A^{T}|$", d5, [-d5, d5 ** 2, 1 / d5]), ("$|A^{3}|$", d5 ** 3, [3 * d5, -d5 ** 3, d5 ** 2]),
             ("$|A^{T}A|$", d5 ** 2, [d5, -d5 ** 2, 2 * d5]), ("$|A^{-1}|$", 1 / d5, [-1 / d5, d5, -d5]),
             ("$|5A|$", 125 * d5, [5 * d5, 25 * d5, 15 * d5])]
    for lbl, val, ex in items:
        c, wr = numopts(val, rng, extra=ex)
        B.mcq(ch, "Properties of det", 2, st + "Compute %s." % lbl, c, wr,
              "Use $\\det A^T=\\det A$, $\\det(AB)=\\det A\\det B$, $\\det A^{-1}=1/\\det A$ and $\\det(cA)=c^n\\det A$ ($n=3$): %s $=%s$." % (lbl, tex(val)), "Exercise Sheet 3, Ex. 5", "src")
    # Cramer
    CR = [("S3-E6", sp.Matrix([[1, 2], [-1, 1]]), sp.Matrix([5, 1]), ["x_1", "x_2"]),
          ("S3-E7", sp.Matrix([[2, 1, 2], [-1, 2, -3], [3, 2, -1]]), sp.Matrix([6, 0, 6]), ["x_1", "x_2", "x_3"])]
    for tag, A, b, names in CR:
        sol = A.LUsolve(b); d = A.det()
        for j in range(A.cols):
            Aj = A.copy(); Aj[:, j] = b
            c, wr = numopts(sol[j], rng, extra=[Aj.det(), d, sol[(j + 1) % A.cols]])
            B.mcq(ch, "Cramer's rule", 2, "Use Cramer's rule to find $%s$:\n$$%s$$" % (names[j], system_tex(A, b, names)), c, wr,
                  "$\\det A=%s$ and replacing column %d by $b$ gives $\\det A_%d=%s$, so $%s=\\det A_%d/\\det A=%s$." % (tex(d), j + 1, j + 1, tex(Aj.det()), names[j], j + 1, tex(sol[j])),
                  "Exercise Sheet 3, Ex. %s" % tag[-1], "src")
    # unique solution check (Ex 8, 9) – coefficient determinants
    U = [("S3-E8", sp.Matrix([[-1, 1, 2], [2, 3, 1], [5, 4, 2]]), "$-x+y+2z=1,\\ 2x+3y+z=-2,\\ 5x+4y+2z=4$"),
         ("S3-E9", sp.Matrix([[1, 2, 6], [2, 5, 15], [3, 1, 3]]), "$x_1+2x_2+6x_3=1,\\ 2x_1+5x_2+15x_3=4,\\ 3x_1+x_2+3x_3=-6$")]
    note("Exercise Sheet 3, Ex. 8", "The third equation is printed as $5x+4y+2x=4$; read as $5x+4y+2z=4$ (typo).")
    for tag, A, txt in U:
        d = A.det()
        verdict = lambda v: "unique solution" if v != 0 else "no unique solution"
        other = [v for v in (d + 1, d - 1, d + 2, -d) if v != d]
        B.mcq(ch, "Cramer's rule", 2, "For the system %s, compute $\\det$ of the coefficient matrix and decide how many solutions it has." % txt,
              "$\\det=%s$: %s" % (tex(d), verdict(d)),
              ["$\\det=%s$: %s" % (tex(d), "no unique solution" if d != 0 else "unique solution")] + ["$\\det=%s$: %s" % (tex(v), verdict(v)) for v in other],
              "The system has exactly one solution iff $\\det A\\neq0$ (Cramer). Here $\\det A=%s$." % tex(d), "Exercise Sheet 3, Ex. %s" % tag[-1], "src")
    # adjugate / inverse
    for tag, A in (("10", sp.Matrix([[1, 2, 3], [0, 1, -1], [2, 2, 2]])), ("11", sp.Matrix([[0, 1, 1], [1, 2, 3], [-1, -1, -2]]))):
        adj = A.adjugate(); d = A.det(); i, j = rng.randrange(3), rng.randrange(3)
        c, wr = numopts(adj[i, j], rng, extra=[adj[j, i], -adj[i, j], d])
        B.mcq(ch, "Adjugate", 3, "For $A=%s$, the entry in row $%d$, column $%d$ of $\\operatorname{adj}(A)$ is" % (mtx(A), i + 1, j + 1), c, wr,
              "$\\operatorname{adj}A$ is the transpose of the cofactor matrix: $\\operatorname{adj}A=%s$, and $\\det A=%s$." % (mtx(adj), tex(d)),
              "Exercise Sheet 3, Ex. %s" % tag, "src")
        if d == 0:
            note("Exercise Sheet 3, Ex. 11", "As printed, the matrix $%s$ has $\\det A=0$, so the inverse requested in the exercise does not exist (probably a typo in the sheet). We keep the exercise as a singular-matrix question: $A\\,\\operatorname{adj}A=(\\det A)I=0$." % mtx(A))
            B.mcq(ch, "Adjugate", 3, "For $A=%s$, which statement is correct?" % mtx(A),
                  "$A$ is singular ($\\det A=0$), so $A^{-1}$ does not exist", ["$A^{-1}=\\operatorname{adj}(A)$", "$A^{-1}=-\\operatorname{adj}(A)$", "$A^{-1}=\\operatorname{adj}(A)^{T}$"],
                  "$\\det A=%s=0$. The formula $A^{-1}=\\operatorname{adj}A/\\det A$ needs $\\det A\\neq0$; here $A\\operatorname{adj}A=0$." % tex(d), "Exercise Sheet 3, Ex. 11", "src")
            continue
        B.mcq(ch, "Adjugate", 3, "For $A=%s$ ($\\det A=%s$), find $A^{-1}$ via the adjugate." % (mtx(A), tex(d)), mt(A.inv()),
              [mt(adj), mt(perturb(A.inv(), rng)), mt(adj.T / d)], "$A^{-1}=\\frac1{\\det A}\\operatorname{adj}A=%s$." % mtx(A.inv()), "Exercise Sheet 3, Ex. %s" % tag, "src")
    # rules
    B.mcq(ch, "Properties of det", 1, "Swapping two rows of a matrix changes its determinant by …", "a factor $-1$", ["no change", "a factor $2$", "a factor $\\tfrac12$"],
          "A row swap multiplies $\\det$ by $-1$; adding a multiple of a row leaves it unchanged; scaling a row by $c$ multiplies it by $c$.", "Lecture 3", "concept")
    B.mcq(ch, "Properties of det", 1, "If $A$ is $4\\times4$, then $\\det(3A)=$", "$81\\det A$", ["$3\\det A$", "$12\\det A$", "$27\\det A$"], "$\\det(cA)=c^n\\det A$ with $n=4$: $3^4=81$.", "Lecture 3", "concept")
    B.mcq(ch, "Properties of det", 1, "The determinant of a triangular matrix is …", "the product of its diagonal entries", ["the sum of its diagonal entries", "always $0$", "the product of all entries"],
          "Expanding along the first column repeatedly gives the product of the diagonal.", "Lecture 3", "concept")
    B.mcq(ch, "Properties of det", 2, "A square matrix with two equal rows has determinant …", "$0$", ["$1$", "$-1$", "it depends on the other rows"],
          "Swapping the equal rows leaves $A$ unchanged but flips the sign: $\\det A=-\\det A$, so $\\det A=0$.", "Lecture 3", "concept")
    B.mcq(ch, "Properties of det", 2, "If $\\det A=5$ for a $3\\times3$ matrix, what is $\\det(\\operatorname{adj}A)$?", "$25$", ["$5$", "$125$", "$1/5$"],
          "$\\det(\\operatorname{adj}A)=(\\det A)^{n-1}=5^2=25$.", "Lecture 3", "concept")
    # past paper determinants
    Ak = sp.Matrix([[2, k, 2, 4], [k, 0, -2, -2], [1, 1, 1, 1], [1, 0, 0, -4]])
    d = sp.factor(Ak.det()); dv = Ak.subs(k, -1).det()
    c, wr = numopts(dv, rng, extra=[-dv, perturb(Ak.subs(k, -1), rng).det(), perturb(Ak.subs(k, -1), rng).det()])
    B.mcq(ch, "Computing determinants", 3, "Exam: $A=%s$. For $k=-1$, $\\det A=$" % mtx(Ak), c, wr,
          "Add multiples of row 3 (which has all ones) to clear the first column, then expand. $\\det A(k)=%s$ and $\\det A(-1)=%s$." % (tex(d), tex(dv)), "Final 2023–24 Shift 2, Q2(a)", "src")
    roots = sp.solve(Ak.det(), k)
    ct, wr = set_options(sorted(roots, key=float), list(roots) + [0, 1, -2], k, rng)
    B.mcq(ch, "Invertibility", 3, "Exam: for $A=%s$, for which $k$ is $A$ NOT invertible?" % mtx(Ak), ct, wr,
          "$A$ is singular iff $\\det A(k)=0$. With $\\det A(k)=%s$ this gives $k=%s$." % (tex(d), ",".join(tex(z) for z in sorted(roots, key=float))), "Final 2023–24 Shift 2, Q2(b)", "src")
    A22 = sp.Matrix([[1, 1, 1, 1], [0, 1, -2, 0], [2, 1, 0, -3], [-1, -1, 0, k]])
    dv = A22.subs(k, 2).det(); d22 = sp.factor(A22.det())
    c, wr = numopts(dv, rng, extra=[-dv, perturb(A22.subs(k, 2), rng).det(), 2 * dv])
    B.mcq(ch, "Computing determinants", 3, "Exam: $A=%s$. For $k=2$, $\\det A=$" % mtx(A22), c, wr,
          "$\\det A(k)=%s$; at $k=2$ this is $%s$. (Invertible iff $k\\ne%s$.)" % (tex(d22), tex(dv), tex(sp.solve(A22.det(), k)[0])), "Final 2022–23 Group 1, Q2(a)", "src")
    xx = sp.Symbol("x")
    Bx = sp.Matrix([[xx, 1, 1], [1, xx, 1], [1, 1, xx]])
    B.mcq(ch, "Computing determinants", 3, "Exam: $\\det\\begin{bmatrix}x&1&1\\\\1&x&1\\\\1&1&x\\end{bmatrix}=$", "$%s$" % tex(sp.factor(Bx.det())),
          ["$%s$" % tex(z) for z in (xx ** 3 - 1, (xx - 1) * (xx + 2) ** 2, xx ** 3 + 2 * xx - 3 * xx ** 2 + 1)],
          "Add rows 2 and 3 to row 1 → factor $(x+2)$; subtracting then leaves $(x-1)^2$: $\\det=(x-1)^2(x+2)=x^3-3x+2$.", "Final 2018–19 (D,E,G), Q2(b)", "src")
    ab = sp.Symbol("a")
    Bb = sp.Matrix([[1, ab, 1], [2, 1, ab], [3, 2, 1]])
    B.mcq(ch, "Computing determinants", 3, "Exam: $\\det\\begin{bmatrix}1&a&1\\\\2&1&a\\\\3&2&1\\end{bmatrix}=$", "$%s$" % tex(sp.expand(Bb.det())),
          ["$%s$" % tex(z) for z in (3 * ab ** 2 + 4 * ab + 2, -3 * ab ** 2 - 4 * ab + 2, 3 * ab ** 2 - 4 * ab - 2)],
          "Expand along row 1: $1(1-2a)-a(2-3a)+1(4-3)=3a^2-4a+2$.", "Final 2018–19 (A,B,C,AE), Q2(b)", "src")
    # random determinants
    for n in (2, 3, 3, 3, 4):
        while True:
            A = sp.Matrix(n, n, lambda i, j: rng.randint(-3, 3))
            if abs(A.det()) <= 40 and sum(1 for z in A if z != 0) >= n * n - 1:
                break
        d = A.det()
        c, wr = numopts(d, rng, extra=[-d, perturb(A, rng).det(), perturb(A, rng).det()])
        B.mcq(ch, "Computing determinants", 1 if n < 3 else 2, "Compute $\\det A$ for $A=%s$." % mtx(A), c, wr,
              "Use row operations to reach a triangular form (track swaps) or cofactor expansion: $\\det A=%s$." % tex(d), "Generated (determinants)", "gen")
    for _ in range(3):
        while True:
            A = sp.Matrix(3, 3, lambda i, j: rng.randint(-2, 3))
            if A.det() != 0:
                break
        b = sp.Matrix([rng.randint(-3, 3) for _ in range(3)])
        sol = A.LUsolve(b); j = rng.randrange(3)
        Aj = A.copy(); Aj[:, j] = b
        c, wr = numopts(sol[j], rng, extra=[Aj.det(), A.det()])
        B.mcq(ch, "Cramer's rule", 2, "Cramer's rule for $x_%d$ in $Ax=b$ with $A=%s$, $b=%s$:" % (j + 1, mtx(A), mtx(b)), c, wr,
              "$x_%d=\\det A_%d/\\det A=%s/%s=%s$." % (j + 1, j + 1, tex(Aj.det()), tex(A.det()), tex(sol[j])), "Generated (Cramer)", "gen")
