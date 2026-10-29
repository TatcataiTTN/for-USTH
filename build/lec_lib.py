# -*- coding: utf-8 -*-
"""Lecture walkthrough: constructors for the script files (S slide, E exercise), text formatting and the exercise checker.
Each lecture file lists, for every slide of the lecturers' original deck, a bilingual (English / Vietnamese) teaching script,
a value level, an optional "why it matters" note and exercises whose answers are checked by sympy when the pages are built."""
import html, re

LEVELS = {3: ("Core", "Cốt lõi"), 2: ("Important", "Quan trọng"), 1: ("Context", "Bổ trợ")}

def S(n, title, en, vi, v=2, why=None, ex=()):
    """Slide n (PDF page) of the original deck: title (EN, VI), script in English and Vietnamese, value level 3/2/1, why (EN, VI), exercises."""
    return dict(n=n, t=tuple(title), en=en.strip(), vi=vi.strip(), v=v, why=tuple(why) if why else None, ex=list(ex))

def E(q, qv, ans, sol, solv, chk=None):
    """Exercise: statement (EN, VI), answer in LaTeX, solution (EN, VI) and chk = sympy expression(s) that must evaluate to True (None = conceptual, no check)."""
    return dict(q=q.strip(), qv=qv.strip(), a=ans.strip(), s=sol.strip(), sv=solv.strip(), chk=chk)

# ---------------------------------------------------------------- text
_MATH = re.compile(r"\$\$.*?\$\$|\$.*?\$", re.S)

def fmt(text):
    """Blank line = new paragraph; a line starting with '- ' is a list item; **bold**, *italic*; $...$ and $$...$$ are kept for KaTeX."""
    keep = []
    def hold(m):
        keep.append(m.group(0)); return "\x00%d\x00" % (len(keep) - 1)
    t = html.escape(_MATH.sub(hold, text), quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    out = []
    for block in re.split(r"\n\s*\n", t.strip()):
        lines = block.split("\n")
        if all(l.lstrip().startswith("- ") for l in lines):
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % l.lstrip()[2:] for l in lines))
        else:
            head = [l for l in lines if not l.lstrip().startswith("- ")]
            items = [l.lstrip()[2:] for l in lines if l.lstrip().startswith("- ")]
            out.append("<p>%s</p>" % "<br>".join(head) if head else "")
            if items:
                out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % i for i in items))
    h = "".join(out)
    return re.sub("\x00(\\d+)\x00", lambda m: html.escape(keep[int(m.group(1))], quote=False), h)

# ---------------------------------------------------------------- exercise checks
def _namespace():
    ns = {}
    exec("from sympy import *\nfrom sympy.calculus.util import continuous_domain, function_range, periodicity\nfrom sympy.calculus.singularities import is_strictly_increasing, is_strictly_decreasing, is_increasing, is_decreasing, singularities", ns)
    exec("x, y, z, t, u, v, w, a, b, c, d, h, k, m, n, p, r, s = symbols('x y z t u v w a b c d h k m n p r s', real=True)\nj, i_ = symbols('j i_', integer=True)\neps, delta = symbols('eps delta', positive=True)", ns)
    exec("def close(p, q, tol=1e-6):\n    return abs(N(p) - N(q)) < tol\n"
         "def nlim(f, a, side=0, eps=1e-7):\n    g = lambdify(x, f, 'mpmath')\n    return g(a + side * eps) if side else (g(a - eps) + g(a + eps)) / 2\n", ns)
    return ns

_NS = None

def run_check(e, where):
    """Evaluate the exercise's check expressions; any falsy result stops the build (the answer printed must be the computed one)."""
    global _NS
    if e["chk"] is None:
        return False
    _NS = _NS or _namespace()
    for expr in ([e["chk"]] if isinstance(e["chk"], str) else e["chk"]):
        try:
            ok = bool(eval(expr, _NS))
        except Exception as err:
            raise AssertionError("%s: check raised %r in %s\n  exercise: %s" % (where, err, expr, e["q"][:90]))
        if not ok:
            raise AssertionError("%s: check FAILED: %s\n  exercise: %s" % (where, expr, e["q"][:90]))
    return True
