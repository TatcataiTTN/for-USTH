# -*- coding: utf-8 -*-
"""Assemble the Physics I (PHY1.001) question bank: 7 chapters (verified, balanced)."""
from qlib import Bank
import gen_ph1_a, gen_ph1_b, gen_ph1_c

def build():
    B = Bank("PH1", seed=20261101)
    for fn in (gen_ph1_a.ch1, gen_ph1_a.ch2, gen_ph1_b.ch3, gen_ph1_b.ch4, gen_ph1_c.ch5, gen_ph1_c.ch5b, gen_ph1_c.ch6, gen_ph1_c.ch6b, gen_ph1_c.ch7):
        fn(B)
    return B

if __name__ == "__main__":
    import phys_common
    B = build()
    print(B.finalize())
    from collections import Counter
    print(sorted(Counter(i["ch"] for i in B.items).items()))
    print("skipped", len(B.skipped), "fillers", len(phys_common.FILLED))
    for x in B.skipped + phys_common.FILLED: print("  ", x)
