# -*- coding: utf-8 -*-
"""Data classes for the Linear Algebra Moodle-quiz review pages. Variants carry a `chk` callable that must return True at build time."""
from sympy import *

class Item:
    def __init__(s, id, src, title, q, key, steps, choices=None, trap=None, note=None, variants=None, mock=None):
        s.__dict__.update(locals())
def I(*a, **k): return Item(*a, **k)
class V:
    def __init__(s, lvl, qe, qv, ans, sol, chk): s.lvl, s.q, s.ans, s.sol, s.chk = lvl, (qe, qv), ans, sol, chk
