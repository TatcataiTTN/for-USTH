"""Dump a bank to a readable text file for human review: python3 review.py LA|CAL"""
import sys, json
sys.path.insert(0, '.')
which = sys.argv[1]
if which == "LA":
    import gen_la as g
else:
    import gen_cal as g
B = g.build(); B.finalize()
with open(f"review/{which.lower()}_review.txt", "w", encoding="utf-8") as f:
    for it in B.items:
        f.write(f"[{it['id']}] L{it['level']} {it['topic']} | {it['src']} ({it['origin']})\n")
        f.write("Q: " + it['q'].replace("\n", "\n   ") + "\n")
        for i, o in enumerate(it['opts']):
            f.write(f"  {'*' if i == it['correct'] else ' '}{'ABCD'[i]}. {o}\n")
        f.write("  EXPL: " + it['explain'] + "\n\n")
print(len(B.items), "items written")
