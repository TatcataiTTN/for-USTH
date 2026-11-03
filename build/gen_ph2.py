# -*- coding: utf-8 -*-
"""Assemble the Physics II (PHY1.002) question bank: 11 chapters (verified, balanced)."""
from qlib import Bank
import gen_ph2_a, gen_ph2_b, gen_ph2_c, gen_ph2_d

def build():
    B = Bank("PH2", seed=20261102)
    for fn in (gen_ph2_a.ch1, gen_ph2_a.ch1b, gen_ph2_a.ch2, gen_ph2_a.ch2b, gen_ph2_b.ch3, gen_ph2_b.ch3b, gen_ph2_b.ch4, gen_ph2_b.ch4b,
               gen_ph2_c.ch5, gen_ph2_c.ch5b, gen_ph2_c.ch6, gen_ph2_c.ch6b, gen_ph2_c.ch6c, gen_ph2_c.ch7, gen_ph2_c.ch7b, gen_ph2_c.ch7c,
               gen_ph2_d.ch8, gen_ph2_d.ch8b, gen_ph2_d.ch9, gen_ph2_d.ch9b, gen_ph2_d.ch10, gen_ph2_d.ch10b, gen_ph2_d.ch10c, gen_ph2_d.ch11, gen_ph2_d.ch11b):
        fn(B)
    return B

if __name__ == "__main__":
    import phys_common
    from collections import Counter
    B = build()
    phys_common.lint_bank(B)
    print(B.finalize())
    ne = Counter(i["ch"] for i in B.items if "extension" not in i.get("tags", []))
    print(sorted(Counter(i["ch"] for i in B.items).items(), key=lambda kv: int(kv[0][1:])), "| non-extension:", sorted(ne.items(), key=lambda kv: int(kv[0][1:])))
    print("skipped", len(B.skipped), "fillers", len(phys_common.FILLED))
    for x in B.skipped + phys_common.FILLED: print("  ", x)
