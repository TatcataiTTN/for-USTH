# -*- coding: utf-8 -*-
"""Concept finder: one searchable page for every concept of every course (definition, key facts, how it is asked, how many bank questions cover it).
Concepts live in build/concepts/{la,cal,ph1,ph2}.py; counts and links come from the generated banks, never typed. Writes concepts/index.html and concepts/data.json."""
import json, os, sys
from sitegen import *
from concepts import la, cal, ph1, ph2

SETS = [("Calculus-1", "Calculus I", cal), ("Linear-Algebra", "Linear Algebra", la), ("Physics-1", "Physics I", ph1), ("Physics-2", "Physics II", ph2)]

def build(live):
    """live = courses whose bank pages are published (others keep their counts but get no links)."""
    out = []; report = []; errs = []; courses = {}
    for slug, label, mod in SETS:
        if not os.path.exists(os.path.join(ROOT, slug, "data", "bank.json")):
            continue
        bank = load_json(slug + "/data/bank.json")["items"]; meta = load_json(slug + "/data/meta.json")
        chtitle = {c["id"]: c["title"] for c in meta["chapters"]}
        have = {(i["ch"], i["topic"]) for i in bank}; used = set()
        for k, c in enumerate(mod.CONCEPTS):
            for t in c["topics"]:
                if (c["ch"], t) not in have:
                    errs.append("concept %s/%s refers to unknown bank topic %r in %s" % (slug, c["name"][0], t, c["ch"]))
                used.add((c["ch"], t))
            qs = [i for i in bank if i["ch"] == c["ch"] and i["topic"] in c["topics"]]
            lv = {}
            for i in qs: lv[i["level"]] = lv.get(i["level"], 0) + 1
            out.append(dict(id="%s-%d" % (slug, k + 1), course=slug, label=label, ch=c["ch"], chapter=chtitle[c["ch"]], name=c["name"], defn=c["defn"], facts=c["facts"], angles=c["angles"],
                            topics=c["topics"], kw=c["kw"], hot=c["hot"], n=len(qs), levels=lv, live=slug in live))
        courses[slug] = dict(label=label, bank=len(bank), mapped=sum(1 for i in bank if (i['ch'], i['topic']) in used))
        left = sorted(have - used)
        if left: report.append("%s: bank topics not in any concept: %s" % (slug, "; ".join("%s/%s" % x for x in left)))
    if errs: sys.exit("\n".join(errs))
    write("concepts/data.json", json.dumps(dict(concepts=out, courses=courses), ensure_ascii=False, separators=(",", ":")))
    body = """<h1>Concept finder · Tra cứu khái niệm</h1>
<p class="lead">Every concept of every course in one place: definition, key facts, the ways an exam asks about it, and how many practice questions already cover it. Use it to see what is thin and to plan new question sets. <span class="muted">Mọi khái niệm của mọi môn: định nghĩa, ý chính, các dạng đề hay gặp và số câu luyện tập đã có.</span></p>
<div id="concepts" data-src="data.json"><p class="muted">Loading…</p></div>"""
    html_ = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Concept finder · USTH B1</title>
<link rel="icon" type="image/png" href="../shared/img/favicon.png"><link rel="stylesheet" href="../shared/vendor/katex/katex.min.css"><link rel="stylesheet" href="../shared/core.css"><link rel="stylesheet" href="../shared/concepts.css">
<script>(function(){try{var t=JSON.parse(localStorage.getItem('ustm:theme')||'null');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}catch(e){}})();</script><script src="../shared/gate.js"></script></head><body>
<header class="top"><div class="wrap"><a class="brand" href="../index.html"><img src="../shared/img/usth_logo.png" alt="USTH"><span>USTH B1 · Concept finder</span></a><nav><a href="../index.html">All courses</a></nav></div></header>
<main class="wrap">%s</main>
<script src="../shared/vendor/katex/katex.min.js"></script><script src="../shared/vendor/katex/auto-render.min.js"></script><script src="../shared/core.js"></script><script src="../shared/concepts.js"></script></body></html>""" % body
    write("concepts/index.html", html_)
    return len(out), report
