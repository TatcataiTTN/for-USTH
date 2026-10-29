# -*- coding: utf-8 -*-
"""Assemble the Calculus I question bank (verified, balanced)."""
from qlib import Bank
import gen_cal1

def build():
    B = Bank("CAL", seed=20261030)
    gen_cal1.ch1(B)
    for modname, fn in (("gen_cal1", "ch2"), ("gen_cal2", "ch3"), ("gen_cal2", "ch4"), ("gen_cal3", "ch5"), ("gen_cal3", "ch6"),
                        ("gen_cal4", "ch2"), ("gen_cal4", "ch3"), ("gen_cal4", "ch4"), ("gen_cal4", "ch5"), ("gen_cal4", "ch6")):   # gen_cal4 = tutoring-slide extras, appended last so existing ids stay stable
        try:
            mod = __import__(modname)
        except ImportError:
            continue
        if hasattr(mod, fn):
            getattr(mod, fn)(B)
    return B

if __name__ == "__main__":
    B = build()
    print(B.finalize())
    from collections import Counter
    print(sorted(Counter(i["ch"] for i in B.items).items()))
    print("skipped", len(B.skipped))
    for x in B.skipped: print("  SKIP", x)
