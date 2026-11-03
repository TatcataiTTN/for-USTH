# -*- coding: utf-8 -*-
"""Concept catalogue helpers. A concept: id, course, chapter, names, definition, key facts, ways it is asked (question angles), bank topics it is covered by, keywords."""
def P(s):
    en, vi = s.split(" | ", 1)
    return [en.strip(), vi.strip()]
def C(ch, name, defn, facts, angles, topics=(), kw="", hot=False):
    return dict(ch=ch, name=P(name), defn=P(defn), facts=P(facts), angles=[P(a) for a in angles], topics=list(topics), kw=kw, hot=hot)
