# -*- coding: utf-8 -*-
"""Question-bank library shared by the Calculus I and Linear Algebra generators.

Rules (see skill build-complete-self-study-system, stages 3-4):
  * every correct answer is COMPUTED (sympy / Fraction), never typed by hand;
  * distractors are realistic mistakes, not random numbers;
  * option order is shuffled with a fixed seed, then the correct position is balanced and audited.
"""
import json, math, random, re
from fractions import Fraction
import sympy as sp

# ----------------------------------------------------------------------------- LaTeX helpers
def tex(x):
    """sympy / int / Fraction / str -> LaTeX string (no dollars)."""
    if isinstance(x, str):
        return x
    if isinstance(x, Fraction):
        x = sp.Rational(x.numerator, x.denominator)
    if isinstance(x, (int,)):
        return str(x)
    out = sp.latex(x)
    for a_, b_ in (("\\operatorname{atan}", "\\arctan"), ("\\operatorname{asin}", "\\arcsin"), ("\\operatorname{acos}", "\\arccos"), ("\\log", "\\ln")):
        out = out.replace(a_, b_)
    return out

def M(x):
    """Inline math."""
    return "$" + tex(x) + "$"

def mat(m, kind="bmatrix"):
    m = sp.Matrix(m)
    rows = [" & ".join(tex(m[i, j]) for j in range(m.cols)) for i in range(m.rows)]
    return r"\begin{%s}" % kind + r" \\ ".join(rows) + r"\end{%s}" % kind

def aug(A, b):
    """Augmented matrix [A | b] as LaTeX array."""
    A = sp.Matrix(A); b = sp.Matrix(b)
    n = A.cols
    rows = [" & ".join([tex(A[i, j]) for j in range(n)] + [tex(b[i, 0])]) for i in range(A.rows)]
    return r"\left[\begin{array}{" + "c" * n + "|c}" + r" \\ ".join(rows) + r"\end{array}\right]"

def vec(v):
    """Row-style tuple (a, b, c)."""
    return "(" + ", ".join(tex(sp.nsimplify(c)) for c in v) + ")"

def colvec(v):
    return mat(sp.Matrix(list(v)))

def system_tex(A, b, names=None):
    """Aligned linear system in LaTeX."""
    A = sp.Matrix(A); b = sp.Matrix(b)
    names = names or ["x_%d" % (j + 1) for j in range(A.cols)]
    lines = []
    for i in range(A.rows):
        parts = []
        for j in range(A.cols):
            c = sp.nsimplify(A[i, j])
            if c == 0:
                continue
            if c.is_number:
                neg = bool(c < 0)
                mag = -c if neg else c
                coef = "" if mag == 1 else tex(mag)
            else:  # symbolic coefficient (parameter systems)
                neg = bool(c.could_extract_minus_sign())
                mag = -c if neg else c
                coef = "" if mag == 1 else (r"\left(%s\right)" % tex(mag) if mag.is_Add else tex(mag))
            term = coef + names[j]
            if not parts:
                parts.append(("-" if neg else "") + term)
            else:
                parts.append(f" {'-' if neg else '+'} {term}")
        lhs = "".join(parts) if parts else "0"
        lines.append(f"{lhs} = {tex(b[i, 0])}")
    return r"\begin{cases}" + r" \\ ".join(lines) + r"\end{cases}"

def R(a, b=1):
    return sp.Rational(a, b)

# ----------------------------------------------------------------------------- distractor helpers
def uniq_by_text(vals):
    seen, out = set(), []
    for v in vals:
        k = re.sub(r"\s+", "", str(v))
        if k not in seen:
            seen.add(k); out.append(v)
    return out

def near_numbers(ans, rng, extra=()):
    """Plausible numeric distractors for an exact answer (sympy Rational / int)."""
    a = sp.nsimplify(ans)
    cands = list(extra) + [-a, a + 1, a - 1, 2 * a, a + 2, a - 2, a * 3]
    if a != 0:
        cands += [1 / a]
    if a.is_Rational and a.q != 1:
        cands += [sp.Rational(a.p, 1), sp.Rational(1, a.p) if a.p != 0 else a]
    cands = [sp.nsimplify(c) for c in cands if sp.nsimplify(c) != a]
    cands = uniq_by_text([tex(c) for c in cands])
    return cands

# ----------------------------------------------------------------------------- source-document notes
NOTES = []   # (source, note) pairs shown on the Sources page: typos / impossible exercises found while checking

def note(src, text):
    if (src, text) not in NOTES:
        NOTES.append((src, text))

# ----------------------------------------------------------------------------- the bank
class Bank:
    def __init__(self, course, seed):
        self.course = course
        self.rng = random.Random(seed)
        self.items = []
        self.essays = []
        self._keys = set()
        self._count = {}
        self.skipped = []   # (src, stem) of questions dropped for lack of distinct distractors

    def _id(self, kind, ch):
        k = (kind, ch)
        self._count[k] = self._count.get(k, 0) + 1
        return f"{self.course}-{ch}-{kind}{self._count[k]:03d}"

    def mcq(self, ch, topic, level, stem, correct, wrongs, explain, src, origin="src", tags=(), fig=None):
        """Add one multiple-choice question. Returns True if added (False if duplicate / not enough distractors).
        fig = optional inline SVG (our own generated drawing, shown between the statement and the options)."""
        correct = str(correct)
        norm = lambda s: re.sub(r"\s+", "", str(s))
        seen = {norm(correct)}
        wr = []
        for w in wrongs:
            if norm(w) not in seen:
                seen.add(norm(w)); wr.append(str(w))
        if len(wr) < 3:
            self.skipped.append((src, stem[:90].replace("\n", " ")))
            return False
        wr = wr[:3]
        key = norm(stem) + "|" + norm(correct)
        if key in self._keys:
            return False
        self._keys.add(key)
        opts = [correct] + wr
        order = list(range(4)); self.rng.shuffle(order)
        opts = [opts[i] for i in order]
        item = dict(
            id=self._id("q", ch), ch=ch, topic=topic, level=level, q=stem, opts=opts,
            correct=opts.index(correct), explain=explain, src=src, origin=origin, tags=list(tags))
        if fig:
            item["fig"] = fig
        self.items.append(item)
        return True

    def tf(self, ch, topic, level, stem, truth, explain, src, origin="concept"):
        """True/False question encoded as 4-option MCQ with fixed wording (keeps one engine)."""
        return self.mcq(ch, topic, level, stem,
                        "True" if truth else "False",
                        ["False" if truth else "True", "Only if the matrices are square", "Cannot be determined"],
                        explain, src, origin)

    def essay(self, ch, topic, level, q, sol, src, origin="src", hint=None, lab=None, answer=None):
        self.essays.append(dict(id=self._id("w", ch), ch=ch, topic=topic, level=level, q=q, sol=sol,
                                src=src, origin=origin, hint=hint, lab=lab, answer=answer))

    # ------------------------------------------------------------------ balancing + audit
    def finalize(self):
        n = len(self.items)
        targets = [i % 4 for i in range(n)]
        self.rng.shuffle(targets)
        for it, t in zip(self.items, targets):
            c = it["correct"]
            if c != t:
                it["opts"][c], it["opts"][t] = it["opts"][t], it["opts"][c]
                it["correct"] = t
        return self.audit()

    def audit(self):
        n = len(self.items)
        pos = [0] * 4
        longest = 0; testable = 0
        for it in self.items:
            pos[it["correct"]] += 1
            lens = [len(o) for o in it["opts"]]
            if len(set(lens)) > 1:
                testable += 1
                if lens[it["correct"]] == max(lens) and lens.count(max(lens)) == 1:
                    longest += 1
        exp = n / 4
        chi = sum((p - exp) ** 2 / exp for p in pos)
        return dict(n=n, essays=len(self.essays), positions=pos, chi2=round(chi, 2),
                    strictly_longest_correct=f"{longest}/{testable} = {100 * longest / max(testable, 1):.1f}% (random ~25%)")

    def dump(self, path):
        data = dict(course=self.course, items=self.items, essays=self.essays)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        return len(self.items), len(self.essays)
