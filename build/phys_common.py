# -*- coding: utf-8 -*-
"""Shared helpers for the Physics I / Physics II question generators.

Rules (same as the Maths banks):
  * every correct answer is COMPUTED from the physical law (never typed), and each generator re-derives it a second way
    (another formula, energy instead of kinematics, numerical integration or simulation, ray-transfer matrices ...) via check();
  * distractors are the realistic mistakes students make (forgotten factor, wrong trig function, unit slip, sign, missing mass ...);
  * numbers are shown with a fixed number of significant figures and every option of a question is distinct after rounding.
"""
import math, re
from qlib import Bank, note, uniq_by_text

# ----------------------------------------------------------------------------- constants (values used in the course documents)
G = 9.8                # m/s^2 unless a problem says g = 10
K_E = 8.99e9           # N m^2 / C^2   (1 / 4 pi eps0)
EPS0 = 8.85e-12        # C^2 / (N m^2)
E_CH = 1.602e-19       # C
M_E = 9.11e-31         # kg
M_P = 1.673e-27        # kg
MU0 = 4e-7 * math.pi   # T m / A
C_LIGHT = 3.00e8       # m/s
R_GAS = 8.314          # J / (mol K)
K_B = 1.38e-23         # J / K
N_A = 6.022e23         # 1 / mol
ATM = 1.013e5          # Pa
G_NEWTON = 6.674e-11

# ----------------------------------------------------------------------------- number formatting
def _half_up(a, ndigits):
    """Round the positive number a to ndigits decimals, halves going up (41.65 -> 41.7), without binary-float surprises."""
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-ndigits)
    return float(Decimal("%.12g" % float(a)).quantize(q, rounding=ROUND_HALF_UP))      # 12 digits first: 11.549999999999999 is really 11.55

def sig_round(x, sig=3):
    """Round to `sig` significant figures (returns a float)."""
    if x == 0 or not math.isfinite(x):
        return x
    ex = math.floor(math.log10(abs(x)))
    return math.copysign(_half_up(abs(x), sig - 1 - ex), x)

def sci(x, sig=3):
    """LaTeX number with `sig` significant figures: plain for 1e-3 <= |x| < 1e4, otherwise a x 10^n."""
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    a = abs(x)
    ex = int(math.floor(math.log10(a)))
    m = _half_up(a / 10 ** ex, sig - 1)
    if m >= 10:
        m /= 10; ex += 1
    if -3 <= ex <= 3:
        n = sig - 1 - ex
        v = _half_up(a, n)
        s = ("%.*f" % (max(n, 0), v))
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return sign + s
    ms = ("%.*f" % (sig - 1, m)).rstrip("0").rstrip(".")
    return sign + (ms + r"\times10^{%d}" % ex)

def unit_tex(u):
    if not u:
        return ""
    if u == "deg":
        return r"^\circ"
    if u == "%":
        return r"\%"
    return r"\,\mathrm{%s}" % u.replace(" ", r"\,")

def fmt(x, unit="", sig=3):
    """$12.5\\,\\mathrm{m/s}$"""
    return "$" + sci(x, sig) + unit_tex(unit) + "$"

def ftxt(x, unit="", sig=3):
    """Same as fmt but without dollars (for use inside running $...$ text)."""
    return sci(x, sig) + unit_tex(unit)

def vec2(x, y, unit="", sig=3):
    return "$(" + sci(x, sig) + ",\\ " + sci(y, sig) + ")" + unit_tex(unit) + "$"

# ----------------------------------------------------------------------------- verification
class CheckError(AssertionError):
    pass

def check(a, b, rel=1e-6, what=""):
    """Two independent computations of the same quantity must agree."""
    if not math.isclose(a, b, rel_tol=rel, abs_tol=1e-12 * max(1.0, abs(a), abs(b))):
        raise CheckError("verification failed%s: %r != %r" % (" (" + what + ")" if what else "", a, b))
    return a

# ----------------------------------------------------------------------------- multiple choice builders
FILLED = []     # questions whose own distractor list was too short and needed generic fillers
def _distinct_numbers(ans, wrongs, unit, sig, min_gap=0.012):
    """Wrong values that differ from the answer and from each other at the displayed precision and by min_gap (relative)."""
    shown = {sci(ans, sig)}
    out = []
    for w in wrongs:
        if isinstance(w, tuple):
            w = w[0]
        if w is None or not math.isfinite(w):
            continue
        s = sci(w, sig)
        if s in shown:
            continue
        ref = max(abs(ans), abs(w), 1e-300)
        if abs(w - ans) / ref < min_gap:
            continue
        if ans != 0 and w != 0 and not (1e-7 <= abs(w / ans) <= 1e7):      # absurd options (10^11 kg of ice) are not realistic mistakes: skip them
            continue
        if any(abs(w - o) / max(abs(o), abs(w), 1e-300) < min_gap for o in out):
            continue
        shown.add(s); out.append(w)
    return out

def mcq_num(B, ch, topic, level, stem, ans, wrongs, unit, explain, src, origin="src", sig=3, fig=None, tags=(), fillers=True):
    """Numeric multiple choice. `wrongs` = realistic mistakes (floats); generic fillers (x2, /2, x10 ...) only top up when fewer than three."""
    ws = _distinct_numbers(ans, wrongs, unit, sig)
    if fillers and len(ws) < 3:
        FILLED.append((src, stem[:80].replace("\n", " ")))          # reported by the build so weak distractor lists get fixed
        extra = [ans * 2, ans / 2, ans * 10, ans / 10, ans * 1.5, ans / 1.5, -ans, ans * 4, ans / 4]
        ws = ws + _distinct_numbers(ans, [e for e in extra if e not in ws], unit, sig)[: 3 - len(ws)]
        ws = _distinct_numbers(ans, ws, unit, sig)
    return B.mcq(ch, topic, level, stem, fmt(ans, unit, sig), [fmt(w, unit, sig) for w in ws], explain, src, origin, tags, fig)

def mcq_text(B, ch, topic, level, stem, correct, wrongs, explain, src, origin="src", fig=None, tags=()):
    """Options are ready-made strings (concepts, directions, expressions)."""
    return B.mcq(ch, topic, level, stem, correct, uniq_by_text(list(wrongs)), explain, src, origin, tags, fig)

def concept(B, ch, topic, level, stem, correct, wrongs, explain, src, fig=None):
    return mcq_text(B, ch, topic, level, stem, correct, wrongs, explain, src, origin="concept", fig=fig)

def mcq_pick(B, ch, topic, level, stem, options, answer_index, explain, src, origin="concept", fig=None):
    """Convenience: a list of four option strings and the index of the right one."""
    correct = options[answer_index]
    wrongs = [o for i, o in enumerate(options) if i != answer_index]
    return mcq_text(B, ch, topic, level, stem, correct, wrongs, explain, src, origin, fig)

# ----------------------------------------------------------------------------- small physics helpers
def deg(x):
    return math.degrees(x)

def rad(x):
    return math.radians(x)

def steps(*lines):
    """Explanation text: numbered lines."""
    return "\n".join("%d) %s" % (i + 1, l) for i, l in enumerate(lines))

def ex(*lines):
    """Explanation text: plain lines."""
    return "\n".join(lines)
