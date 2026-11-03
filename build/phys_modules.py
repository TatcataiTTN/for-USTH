# -*- coding: utf-8 -*-
"""Physics modules (one per chapter). The slides come from the concept catalogue (definition, formulas, method, traps, how it is asked), so the
modules, the Concept finder and the question analyser always say the same thing; build_modules adds one slide per plot and the plots-and-data section."""
from deckgen import *

def plain(s):
    return s.replace("$", "")

def make(concepts, chapters, where):
    """chapters = [(id, title)], where = {id: (lecture, tutorial)}."""
    mods = []
    for i, (ch, title) in enumerate(chapters, 1):
        cs = [c for c in concepts if c["ch"] == ch and not c.get("out")]
        assert cs, "no concepts for chapter " + ch
        slides = []
        for c in cs:
            name = c["name"][0]
            asked = ("<p><b>How it is asked:</b> " + "; ".join(a[0] for a in c["angles"]) + ".</p>") if c["angles"] else ""
            slides.append((name, p(c["defn"][0]) + callout("Key formulas", c["facts"][0]) + asked))
            right = callout("Watch out", ul([t[0] for t in c["traps"]]), "warn") if c["traps"] else ""
            slides.append((name + ": method and traps", cols(callout("Method", ul([t[0] for t in c["steps"]], ordered=True)), right)))
        names = [c["name"][0] for c in cs]
        mods.append(dict(id="m%02d" % i, title=title, ch=ch, lec=where[ch][0], tut=where[ch][1],
                         summary="Concepts: " + "; ".join(plain(n) for n in names[:6]) + (" and %d more." % (len(names) - 6) if len(names) > 6 else "."),
                         objectives=["Recognise and use <b>%s</b> in exam-style questions." % n for n in names], slides=slides, tool=None,
                         topics=sorted({t for c in cs for t in c["topics"]})))
    return mods
