# -*- coding: utf-8 -*-
"""Assemble the Linear Algebra question bank (verified, balanced)."""
import sys, json
from qlib import Bank
import gen_la1

def build():
    B = Bank("LA", seed=20261029)
    gen_la1.ch1(B); gen_la1.ch2(B); gen_la1.ch3(B)
    import gen_la2
    gen_la2.ch4(B); gen_la2.ch5(B)
    try:
        import gen_la3
    except ImportError:
        gen_la3 = None
    if gen_la3:
        gen_la3.ch6(B); gen_la3.ch7(B)
    return B

if __name__ == "__main__":
    B = build()
    print(B.finalize())
    from collections import Counter
    print(Counter(i["ch"] for i in B.items))
