# -*- coding: utf-8 -*-
"""Concept finder: one searchable page for every concept of every course (definition, key facts, how it is asked, how many bank questions cover it).
Concepts live in build/concepts/{la,cal,ph1,ph2}.py; counts and links come from the generated banks, never typed. Writes concepts/index.html and concepts/data.json."""
import json, os, subprocess, sys, tempfile
from sitegen import *
from concepts import la, cal, ph1, ph2

SETS = [("Calculus-1", "Calculus I", cal), ("Linear-Algebra", "Linear Algebra", la), ("Physics-1", "Physics I", ph1), ("Physics-2", "Physics II", ph2)]

import re
_TAGS = re.compile(r"(</?(?:i|b)>)")

def safe(s):
    """The concept texts are inserted with innerHTML: escape < > & (formulas such as $j<k$ would otherwise open a tag and swallow the text); <i> and <b> stay."""
    return "".join(p if i % 2 else p.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for i, p in enumerate(_TAGS.split(s)))

def safe_all(v):
    if isinstance(v, str): return safe(v)
    if isinstance(v, (list, tuple)): return [safe_all(x) for x in v]
    return v

def check_text(errs, cid, field, v):
    """Build-time guard: no raw markup characters left, formulas delimiters balanced."""
    if isinstance(v, (list, tuple)):
        for x in v: check_text(errs, cid, field, x)
        return
    plain = _TAGS.sub("", v)
    if re.search(r"<|>|&(?!(?:amp|lt|gt);)", plain): errs.append("%s %s: raw markup character in %r" % (cid, field, v[:60]))
    if v.replace("\\$", "").count("$") % 2: errs.append("%s %s: unbalanced $ in %r" % (cid, field, v[:60]))

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
            if re.search(r"[<>&]", " ".join(c["name"])): errs.append("concept name with markup characters: %r" % c["name"][0])
            out.append(dict(id="%s-%d" % (slug, k + 1), course=slug, label=label, ch=c["ch"], chapter=chtitle[c["ch"]], name=c["name"], defn=safe_all(c["defn"]), facts=safe_all(c["facts"]), angles=safe_all(c["angles"]),
                            steps=safe_all(c.get("steps", [])), traps=safe_all(c.get("traps", [])), related=c.get("related", []), kwv=c.get("kwv", ""), units=c.get("units", ""), out=bool(c.get("out")),
                            topics=c["topics"], kw=c["kw"], hot=c["hot"], n=len(qs), levels=lv, live=slug in live))
        courses[slug] = dict(label=label, bank=len(bank), mapped=sum(1 for i in bank if (i['ch'], i['topic']) in used))
        left = sorted(have - used)
        if left: report.append("%s: bank topics not in any concept: %s" % (slug, "; ".join("%s/%s" % x for x in left)))
    for c in out:
        for f in ("defn", "facts", "angles", "steps", "traps"): check_text(errs, c["id"], f, c[f])
    if errs: sys.exit("\n".join(errs))
    spec = [dict(id=c["id"], course=c["course"], ch=c["ch"], topics=c["topics"]) for c in out if c["topics"]]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        json.dump(spec, tf); tmp = tf.name
    try:
        mined = json.loads(subprocess.run(["node", os.path.join(ROOT, "build", "mine_keywords.js"), tmp], capture_output=True, text=True, check=True).stdout)
    finally:
        os.unlink(tmp)
    for c in out:
        c["ak"] = mined.get(c["id"], [])
    write("concepts/data.json", json.dumps(dict(concepts=out, courses=courses), ensure_ascii=False, separators=(",", ":")))
    body = """<h1>Concept finder and question analyser · Tra cứu khái niệm và phân tích đề</h1>
<p class="lead">Paste a question: the keyword system finds the concepts it needs and shows the formulas, the steps and the usual traps; a question that matches nothing is flagged as outside the catalogue. <span class="muted">Dán một câu hỏi: hệ từ khóa tìm các khái niệm cần dùng, hiện công thức, các bước và bẫy hay gặp; câu không khớp khái niệm nào được đánh dấu là ngoài phạm vi.</span></p>
<div id="concepts" data-src="data.json"><p class="muted">Loading…</p></div>"""
    html_ = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Concept finder · USTH B1</title>
<link rel="icon" type="image/png" href="../shared/img/favicon.png"><link rel="stylesheet" href="../shared/vendor/katex/katex.min.css"><link rel="stylesheet" href="../shared/core.css"><link rel="stylesheet" href="../shared/concepts.css">
<script>(function(){try{var t=JSON.parse(localStorage.getItem('ustm:theme')||'null');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}catch(e){}})();</script><script src="../shared/gate.js"></script></head><body>
<header class="top"><div class="wrap"><a class="brand" href="../index.html"><img src="../shared/img/usth_logo.png" alt="USTH"><span>USTH B1 · Concept finder</span></a><nav><a href="../index.html">All courses</a></nav></div></header>
<main class="wrap">%s</main>
<script src="../shared/vendor/katex/katex.min.js"></script><script src="../shared/vendor/katex/auto-render.min.js"></script><script src="../shared/core.js"></script><script src="../shared/analyzer-core.js"></script><script src="../shared/analyzer.js"></script><script src="../shared/concepts.js"></script></body></html>""" % body
    write("concepts/index.html", html_)
    return len(out), report


def build_course_pages(courses, hv):
    """One Question analyser page per course, locked to that course (the global page /concepts/ still covers all courses)."""
    for course in courses:
        name = COURSES[course]["name"]
        body = ('<h1>Question analyser · %s</h1>'
                '<p class="lead">Paste a question from this course: the keyword system finds the concepts it needs and shows the formulas, the steps and the usual traps; a question that matches nothing is flagged as outside the catalogue so that keywords can be added. '
                '<span class="muted">Dán một câu hỏi của môn này: hệ từ khóa tìm các khái niệm cần dùng, hiện công thức, các bước và bẫy hay gặp; câu không khớp khái niệm nào được đánh dấu là ngoài phạm vi.</span></p>'
                '<div id="concepts" data-src="../../concepts/data.json" data-course="%s" data-base="../"><p class="muted">Loading…</p></div>') % (esc(name), course)
        write(course + "/analyse/index.html", page(course, "Question analyser", body, 1, "analyse", scripts=["analyzer-core.js", "analyzer.js", "concepts.js"], css=["concepts.css"], have=hv(course),
                                                    desc="Paste a %s question: matching concepts, formulas, steps and usual traps." % name))
