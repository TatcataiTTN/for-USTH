# -*- coding: utf-8 -*-
"""Module pages: slide deck + worked examples taken from the verified bank + practice links."""
import html, json, os
from sitegen import *
from deckgen import Deck, ul, p as para

def example_cards(course, mod, bank):
    items = [q for q in bank["items"] if q["ch"] == mod["ch"] and q["topic"] in mod["topics"] and q["origin"] == "src" and not q["q"].startswith(("Which", "Is ", "Does ", "Can ", "If ", "A linear"))]
    # diversify: round-robin over topics, prefer levels 2-3
    by = {}
    for q in sorted(items, key=lambda z: (-min(z["level"], 3), z["id"])):
        by.setdefault(q["topic"], []).append(q)
    picked = []
    while len(picked) < 4 and any(by.values()):
        for t in list(by):
            if by[t] and len(picked) < 4:
                picked.append(by[t].pop(0))
    h = ""
    for i, q in enumerate(picked, 1):
        ans = q["opts"][q["correct"]]
        h += ('<div class="ex"><div class="exh">Worked example %d · %s <span class="muted">(%s)</span></div><div class="qtxt">%s</div>'
              '<details class="sol"><summary>Show the answer and the solution</summary><p><b>Answer:</b> %s</p><div class="explain show" style="display:block">%s</div></details></div>') % (
            i, html.escape(q["topic"]), html.escape(q["src"]), html.escape(q["q"]), html.escape(ans), html.escape(q["explain"]))
    return h

def build(course, mods, textbooks, tools, have):
    bank = load_json(course + "/data/bank.json"); meta = load_json(course + "/data/meta.json")
    c = COURSES[course]; chtitle = {x["id"]: x["title"] for x in meta["chapters"]}
    n_by_topic = {}
    for q in bank["items"]:
        n_by_topic[(q["ch"], q["topic"])] = n_by_topic.get((q["ch"], q["topic"]), 0) + 1
    # index page
    cards = ""
    last = None
    for m in mods:
        if m["ch"] != last:
            if last is not None: cards += "</div>"
            cards += "<h2>%s · %s</h2><div class='cards'>" % (m["ch"].upper().replace("C", "Chapter "), esc(chtitle[m["ch"]])); last = m["ch"]
        nq = sum(n_by_topic.get((m["ch"], t), 0) for t in m["topics"])
        cards += '<a class="card" href="%s.html"><b>%s · %s</b><span>%s · %s</span><span>%s</span><span><i>%d practice questions on this module\'s topics</i></span></a>' % (m["id"], m["id"].upper(), esc(m["title"]), esc(m["lec"]), esc(m["tut"]), esc(m["summary"]), nq)
    cards += "</div>"
    idx = "<h1>Modules: slides, worked examples, practice links</h1><p class='lead'>Each module has a slide deck in the USTH style (use ← → keys or the buttons; full screen with ⛶), worked examples taken from the course problems, and links to the quizzes and the lab.</p>" + cards
    write(course + "/modules/index.html", page(course, "Modules", idx, 1, "modules", have=have))
    for i, m in enumerate(mods):
        r = "../" * 2
        d = Deck(esc(m["title"]), "%s · %s %s" % (c["name"], "Module", m["id"][1:].lstrip("0") or m["id"]), "%s · %s<br>Chapter: %s<br>Books: %s" % (esc(m["lec"]), esc(m["tut"]), esc(chtitle[m["ch"]]), esc(textbooks[m["ch"]])), r)
        d.add("After this module you can", ul(m["objectives"]))
        for title, body in m["slides"]:
            d.add(title, body)
        d.end("Practice next", ul(["<b>Chapter quizzes</b> %s (3 sets)" % m["ch"].upper().replace("C", "Ch. "), "<b>Practice bank</b>, filtered to this chapter, then <i>written mode</i>", "<b>Lab</b>: %s" % esc(m["tool"][1]), "Then the mock exams (Exams page)"]))
        prev_l = '<a class="btn alt" href="%s.html">◀ %s</a>' % (mods[i - 1]["id"], esc(mods[i - 1]["title"])) if i else ""
        next_l = '<a class="btn alt" href="%s.html">%s ▶</a>' % (mods[i + 1]["id"], esc(mods[i + 1]["title"])) if i + 1 < len(mods) else ""
        qlinks = " ".join('<a class="btn small" href="../quiz/run.html?set=%s-%s">Quiz set %s</a>' % (m["ch"], s, s) for s in "ABC")
        body = ('<p class="muted"><a href="index.html">Modules</a> › %s</p><h1>%s</h1><p class="lead">%s</p>'
                '<div class="callout"><b>%s · %s · %s</b><br>Textbook sections: %s</div>%s'
                '<h2>Worked examples from the course problems</h2>%s'
                '<h2>Practice</h2><p>%s <a class="btn small alt" href="../bank/index.html?ch=%s">Practice bank (this chapter)</a> <a class="btn small alt" href="../bank/index.html?ch=%s&written=1">Written mode</a> <a class="btn small alt" href="../lab/index.html#tool=%s">Lab: %s</a></p>'
                '<div class="row">%s%s</div>') % (
            esc(m["title"]), esc(m["title"]), esc(m["summary"]), esc(m["lec"]), esc(m["tut"]), esc(chtitle[m["ch"]]), esc(textbooks[m["ch"]]), d.html(), example_cards(course, m, bank), qlinks, m["ch"], m["ch"], m["tool"][0], esc(m["tool"][1]), prev_l, next_l)
        write(course + "/modules/%s.html" % m["id"], page(course, m["title"], body, 1, "modules", scripts=["deck.js"], css=["deck.css"], have=have))
