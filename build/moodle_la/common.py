# -*- coding: utf-8 -*-
"""Data classes shared by the Moodle review pages (Linear Algebra, Physics I, Physics II).
Item.chk (optional) re-computes the main answer at build time; V.chk re-computes a practice variant's answer. Both must return True."""
from sympy import *
import math

class Item:
    def __init__(s, id, src, title, q, key, steps, choices=None, trap=None, note=None, variants=None, mock=None, chk=None, klabel=None):
        s.__dict__.update(locals())
def I(*a, **k): return Item(*a, **k)
class V:
    def __init__(s, lvl, qe, qv, ans, sol, chk): s.lvl, s.q, s.ans, s.sol, s.chk = lvl, (qe, qv), ans, sol, chk

def near(a, b, tol=0.006):
    """Relative closeness used by the numeric checks (answers are quoted to 2-3 significant figures)."""
    return abs(a - b) <= tol * max(1.0, abs(b))
