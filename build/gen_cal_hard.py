# -*- coding: utf-8 -*-
"""Assemble the Calculus I level-4 pool (Moodle-style hard questions) as a separate Bank, so the ids and options of the existing bank stay untouched."""
from qlib import Bank, note
import gen_cal_hard1, gen_cal_hard2, gen_cal_hard3

def build():
    B = Bank("CAL", seed=20261031)
    for part in (gen_cal_hard1.build_part1, gen_cal_hard2.build_part2, gen_cal_hard3.build_part3):
        part(B)
    for mod in ("gen_cal_hard4",):                       # chapter extras (written after the slot families)
        try:
            m = __import__(mod)
        except ImportError:
            continue
        m.build_extras(B)
    return B

def lint(B):
    """Fail on text that would render wrongly: control characters (a LaTeX backslash in a non-raw string), unbalanced $ (an escaped \\$ does not count),
    empty or repeated options, or an answer index outside the options."""
    problems = []
    for q in B.items:
        for t in [q["q"], q["explain"]] + list(q["opts"]):
            if any(ord(ch) < 32 and ch != "\n" for ch in t):
                problems.append((q["id"], "control character", t[:60]))
            if t.replace("\\$", "").count("$") % 2:
                problems.append((q["id"], "unbalanced $", t[:60]))
        if len(set(q["opts"])) != 4 or any(not o.strip() for o in q["opts"]) or not 0 <= q["correct"] < 4:
            problems.append((q["id"], "bad options", ""))
    assert not problems, "hard pool lint failed: %r" % (problems[:5],)
    return len(B.items)

def merge(main, hard):
    """Finalize the hard bank on its own (balanced answer positions), give its ids the 'h' kind, and append it to the main bank."""
    report = hard.finalize()
    lint(hard)
    for it in hard.items:
        it["id"] = it["id"].replace("-q", "-h", 1)
    main.items.extend(hard.items)
    return report

if __name__ == "__main__":
    H = build()
    print(merge(Bank("CAL", seed=1), H))
    print("skipped", len(H.skipped))
