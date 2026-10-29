# -*- coding: utf-8 -*-
"""Consistency audit of a Physics bank: the number shown in the correct option must also appear in the worked explanation
(same value at the precision of whichever is coarser), so a number typed in an explanation can never disagree with the computed answer.
Usage: python3 audit_phys.py Physics-1 [Physics-2]   (exit status 1 when something is not found)"""
import json, os, re, sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OPT = re.compile(r"^\$(-?\d+(?:\.\d+)?)(?:\\times10\^\{(-?\d+)\})?(?=\\|\s|\$|\^)")
TOKEN = re.compile(r"(-?\d+(?:\.\d+)?)(?:\s*\\times\s*10\^\{?(-?\d+)\}?)?")

def sig_digits(mant):
    d = mant.lstrip("-").replace(".", "").lstrip("0")
    if "." not in mant:
        d = d.rstrip("0")
    return max(len(d), 1)

def value(mant, ex):
    return float(mant) * 10 ** int(ex or 0)

def round_sig(v, n):
    """Half-up rounding of v to n significant figures."""
    if v == 0:
        return 0.0
    e = len(("%e" % abs(v)).split("e")[0]) and int(("%e" % abs(v)).split("e")[1])
    q = Decimal(1).scaleb(e - n + 1)
    return float(Decimal("%.12g" % v).quantize(q, rounding=ROUND_HALF_UP))

def consistent(A, nA, T, nT):
    if A == 0:
        return T == 0
    if nT <= nA:
        return abs(round_sig(A, nT) - T) <= 1e-9 * abs(T)
    return abs(round_sig(T, nA) - A) <= 1e-9 * abs(A)

def audit(course):
    b = json.load(open(os.path.join(ROOT, course, "data", "bank.json"), encoding="utf-8"))
    miss, numeric = [], 0
    for q in b["items"]:
        m = OPT.match(q["opts"][q["correct"]])
        if not m:
            continue
        numeric += 1
        A, nA = value(m.group(1), m.group(2)), sig_digits(m.group(1))
        text = q["explain"].replace("\\,", "").replace("\\ ", "")
        found = False
        for t in TOKEN.finditer(text):
            T, nT = value(t.group(1), t.group(2)), sig_digits(t.group(1))
            if nT == 1 and nA > 1 and T != A:
                continue                               # a lone digit is too weak a match
            if consistent(A, nA, T, nT):
                found = True
                break
        if not found:
            miss.append((q["id"], q["opts"][q["correct"]], q["src"]))
    return numeric, miss

if __name__ == "__main__":
    bad = 0
    for course in sys.argv[1:] or ["Physics-1", "Physics-2"]:
        if not os.path.exists(os.path.join(ROOT, course, "data", "bank.json")):
            continue
        n, miss = audit(course)
        print("%s: %d numeric answers, %d not found in their explanation" % (course, n, len(miss)))
        for i, a, s in miss:
            print("   ", i, a, "|", s)
        bad += len(miss)
    sys.exit(1 if bad else 0)
