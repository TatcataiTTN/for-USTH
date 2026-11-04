# -*- coding: utf-8 -*-
"""Module pages: slide deck + worked examples taken from the verified bank + practice links."""
import html, json, os, zipfile
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

def fig_slide(f):
    """A slide that shows one figure with its caption and formula (the CSV link is on the page below the deck)."""
    return '<div class="figslide"><img src="img/%s.png" alt="%s"><p class="figcap">%s</p><div class="formula">$$%s$$</div></div>' % (f["id"], html.escape(f["title"]), f["caption"], f["formula"])

def fig_gallery(figs, mid):
    """The figures of a module with the numbers behind them (CSV) and a zip of all of them."""
    if not figs: return ""
    h = ('<h2>Plots and data files</h2><p class="muted">%d plots, each computed from the physical law and checked a second way (numerical integration, an ODE solver, a second formula); the CSV beside each plot holds the numbers behind it, so you can re-plot or fit them. '
         '<a class="btn small alt" href="data/%s-data.zip">Download all %d CSV files of this module (zip)</a></p><div class="figgrid">') % (len(figs), mid, len(figs))
    for f in figs:
        h += ('<figure class="fig" id="%s"><a href="img/%s.png"><img src="img/%s.png" alt="%s"></a><figcaption><b>%s</b><br>%s<br><span class="muted">%d rows · columns: %s</span> '
              '<a class="btn small" href="data/%s.csv" download>CSV</a></figcaption></figure>') % (f["id"], f["id"], f["id"], html.escape(f["title"]), html.escape(f["title"]), f["caption"], f["rows"], html.escape(", ".join(f["columns"])), f["id"])
    return h + "</div>"

def build(course, mods, textbooks, tools, have):
    bank = load_json(course + "/data/bank.json"); meta = load_json(course + "/data/meta.json")
    figs_all = []
    if os.path.exists(os.path.join(ROOT, course, "modules", "figures.json")):
        figs_all = load_json(course + "/modules/figures.json")
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
        cards += '<a class="card" href="%s.html"><b>%s · %s</b><span>%s · %s</span><span>%s</span><span><i>%d practice questions on this module\'s topics%s</i></span></a>' % (m["id"], m["id"].upper(), esc(m["title"]), esc(m["lec"]), esc(m["tut"]), esc(m["summary"]), nq, (" · %d plots with CSV data" % sum(1 for f in figs_all if f["ch"] == m["ch"])) if figs_all else "")
    cards += "</div>"
    idx = "<h1>Modules: slides, worked examples, practice links</h1><p class='lead'>Each module has a slide deck in the USTH style (use ← → keys or the buttons; full screen with ⛶), worked examples taken from the course problems, and links to the quizzes%s.</p>" % (" and the lab" if any(m.get("tool") for m in mods) else "") + (("<p>Every Physics module also has plots computed from the physical law with the numbers behind them (CSV): <a href='data/all-data.zip'>download all %d data files (zip)</a>.</p>" % len(figs_all)) if figs_all else "") + cards
    write(course + "/modules/index.html", page(course, "Modules", idx, 1, "modules", have=have))
    for i, m in enumerate(mods):
        r = "../" * 2
        d = Deck(esc(m["title"]), "%s · %s %s" % (c["name"], "Module", m["id"][1:].lstrip("0") or m["id"]), "%s · %s<br>Chapter: %s<br>Books: %s" % (esc(m["lec"]), esc(m["tut"]), esc(chtitle[m["ch"]]), esc(textbooks[m["ch"]])), r)
        d.add("After this module you can", ul(m["objectives"]))
        for title, body in m["slides"]:
            d.add(title, body)
        figs = [f for f in figs_all if f["ch"] == m["ch"]]
        for f in figs:
            d.add(f["title"], fig_slide(f))
        has_gap = any(z["id"] == m["ch"] + "-G" for z in meta["sets"]["chapter"].get(m["ch"], []))
        d.end("Practice next", ul(["<b>Chapter quizzes</b> %s (3 sets%s)" % (m["ch"].upper().replace("C", "Ch. "), ", plus a gap-fill set" if has_gap else ""), "<b>Practice bank</b>, filtered to this chapter, then <i>written mode</i>"]
                                  + (["<b>Lab</b>: %s" % esc(m["tool"][1])] if m.get("tool") else []) + (["<b>Question analyser</b>: paste a question to see the concepts, formulas and traps"] if "analyse" in have else []) + ["Then the mock exams (Exams page)"]))
        prev_l = '<a class="btn alt" href="%s.html">◀ %s</a>' % (mods[i - 1]["id"], esc(mods[i - 1]["title"])) if i else ""
        next_l = '<a class="btn alt" href="%s.html">%s ▶</a>' % (mods[i + 1]["id"], esc(mods[i + 1]["title"])) if i + 1 < len(mods) else ""
        qlinks = " ".join('<a class="btn small" href="../quiz/run.html?set=%s-%s">Quiz set %s</a>' % (m["ch"], s, s) for s in "ABC") + (' <a class="btn small alt" href="../quiz/run.html?set=%s-G">Gap-fill set</a>' % m["ch"] if has_gap else "")
        body = ('<p class="muted"><a href="index.html">Modules</a> › %s</p><h1>%s</h1><p class="lead">%s</p>'
                '<div class="callout"><b>%s · %s · %s</b><br>Textbook sections: %s</div>%s'
                '%s'
                '<h2>Worked examples from the course problems</h2>%s'
                '<h2>Practice</h2><p>%s <a class="btn small alt" href="../bank/index.html?ch=%s">Practice bank (this chapter)</a> <a class="btn small alt" href="../bank/index.html?ch=%s&written=1">Written mode</a> %s%s</p>'
                '<div class="row">%s%s</div>') % (
            esc(m["title"]), esc(m["title"]), esc(m["summary"]), esc(m["lec"]), esc(m["tut"]), esc(chtitle[m["ch"]]), esc(textbooks[m["ch"]]), d.html(), fig_gallery(figs, m["id"]), example_cards(course, m, bank), qlinks, m["ch"], m["ch"], ('<a class="btn small alt" href="../lab/index.html#tool=%s">Lab: %s</a>' % (m["tool"][0], esc(m["tool"][1]))) if m.get("tool") else "", (' <a class="btn small alt" href="../analyse/index.html">Question analyser</a>' if "analyse" in have else ""), prev_l, next_l)
        write(course + "/modules/%s.html" % m["id"], page(course, m["title"], body, 1, "modules", scripts=["deck.js"], css=["deck.css"], have=have))
        if figs:
            with zipfile.ZipFile(os.path.join(ROOT, course, "modules", "data", "%s-data.zip" % m["id"]), "w", zipfile.ZIP_DEFLATED) as z:
                for f in figs: z.writestr(zipfile.ZipInfo(f["id"] + ".csv", date_time=(2026, 11, 3, 0, 0, 0)), open(os.path.join(ROOT, course, "modules", "data", f["id"] + ".csv"), "rb").read(), zipfile.ZIP_DEFLATED)
