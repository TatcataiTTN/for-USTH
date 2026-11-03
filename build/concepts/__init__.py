# -*- coding: utf-8 -*-
"""Concept catalogue helpers.
C(...)  : the first-generation entry (definition, facts, ways it is asked).
K(...)  : full entry (adds steps, traps, Vietnamese keywords, units, related concepts, out-of-scope flag).
augment(): adds steps / traps / keywords to a first-generation entry by its English name."""
def P(s):
    en, vi = s.split(" | ", 1)
    return [en.strip(), vi.strip()]

def C(ch, name, defn, facts, angles, topics=(), kw="", hot=False):
    return dict(ch=ch, name=P(name), defn=P(defn), facts=P(facts), angles=[P(a) for a in angles], topics=list(topics), kw=kw, kwv="", units="", steps=[], traps=[], related=[], hot=hot, out=False)

def K(ch, name, defn, facts, steps, traps, angles=(), topics=(), kw="", kwv="", units="", related=(), hot=False, out=False):
    return dict(ch=ch, name=P(name), defn=P(defn), facts=P(facts), steps=[P(x) for x in steps], traps=[P(x) for x in traps], angles=[P(a) for a in angles],
                topics=list(topics), kw=kw, kwv=kwv, units=units, related=list(related), hot=hot, out=out)

def O(ch, name, why, kw, kwv=""):
    """A topic that is NOT in the taught scope but often looks like it is: the analyser flags it instead of forcing a match."""
    return K(ch, name, why, "not part of the course | không thuộc chương trình", [], [], [], [], kw, kwv, out=True)

def augment(concepts, aug):
    byname = {c["name"][0]: c for c in concepts}
    for name, extra in aug.items():
        if name not in byname:
            raise SystemExit("augment: unknown concept %r" % name)
        c = byname[name]
        for k, v in extra.items():
            if k in ("steps", "traps"):
                c[k] = [P(x) for x in v]
            elif k == "kw" and c.get("kw"):
                c["kw"] = c["kw"] + ", " + v
            else:
                c[k] = v
    return concepts

def add_traps(concepts, extra):
    """Append extra "EN | VI" trap lines (for example exam tips taken from a source document) to existing concepts, found by their English name."""
    byname = {c["name"][0]: c for c in concepts}
    for name, items in extra.items():
        if name not in byname:
            raise SystemExit("add_traps: unknown concept %r" % name)
        byname[name]["traps"] += [P(x) for x in items]
    return concepts
