# -*- coding: utf-8 -*-
"""Assemble the static pages of all courses (home, modules, chapter quizzes, exams, practice bank, written practice, labs, sources) and the root hub."""
import json, os, re, sys
from collections import Counter, defaultdict
from sitegen import *

MATHS = ("Calculus-1", "Linear-Algebra")
PHYSICS = ("Physics-1", "Physics-2")
HAVE = {"quiz", "exam", "bank", "sources", "lab", "modules", "written"}      # sections of the finished courses
HAVE_BY_COURSE = {}                                                         # filled by main(): a new course lists only the sections that exist so far

def hv(course):
    return HAVE_BY_COURSE.get(course, HAVE)

TEXTBOOKS = {
    "Calculus-1": {
        "c1": "Thomas ch. 1 Functions (1.1–1.3) and ch. 2 Limits and Continuity (2.1–2.6) · Stewart ch. 1 (1.1–1.3) and ch. 2 (2.1–2.6)",
        "c2": "Thomas ch. 3 Derivatives (3.1–3.11) · Stewart ch. 2 (2.7–2.8) and ch. 3 Differentiation Rules (3.1–3.5, 3.9, 3.10)",
        "c3": "Thomas ch. 4 Applications of Derivatives (4.1–4.8) · Stewart ch. 4 Applications of Differentiation (4.1–4.9)",
        "c4": "Thomas ch. 5 Integrals (5.1–5.6) and ch. 6 (6.1–6.4) · Stewart ch. 5 (5.1–5.5), ch. 6 (6.1–6.3, 6.5) and ch. 8 (8.1–8.2)",
        "c5": "Thomas ch. 8 Techniques of Integration (8.1–8.5, 8.8) · Stewart ch. 7 (7.1–7.5, 7.8)",
        "c6": "Thomas ch. 10 Infinite Sequences and Series (10.1–10.10) · Stewart ch. 11 Infinite Sequences and Series (11.1–11.11)",
    },
    "Linear-Algebra": {
        "c1": "Elementary Linear Algebra (8th ed.) ch. 1 §1.1–1.3 · Strang ch. 2 §2.1–2.3 and §3.3–3.4",
        "c2": "Elementary Linear Algebra ch. 2 §2.1–2.4 · Strang §2.4–2.7",
        "c3": "Elementary Linear Algebra ch. 3 §3.1–3.4 · Strang ch. 5 §5.1–5.3",
        "c4": "Elementary Linear Algebra ch. 4 §4.1–4.7 · Strang ch. 3 §3.1–3.6",
        "c5": "Elementary Linear Algebra ch. 5 §5.1–5.4 · Strang ch. 4 §4.1–4.4",
        "c6": "Elementary Linear Algebra ch. 6 §6.1–6.4 · Strang ch. 7 §7.1–7.3",
        "c7": "Elementary Linear Algebra ch. 7 §7.1–7.3 · Strang ch. 6 §6.1–6.4",
    },
    "Physics-1": {
        "c1": "Halliday ch. 2 Motion Along a Straight Line and ch. 4 Motion in Two and Three Dimensions · Young and Freedman ch. 2–3",
        "c2": "Halliday ch. 5 Force and Motion I and ch. 6 Force and Motion II · Young and Freedman ch. 4–5",
        "c3": "Halliday ch. 7 Kinetic Energy and Work, ch. 8 Potential Energy and Conservation of Energy, ch. 9 Centre of Mass and Linear Momentum · Young and Freedman ch. 6–8",
        "c4": "Halliday §4.7 Uniform Circular Motion, §6.5, ch. 10 Rotation · Young and Freedman §3.4, §5.4 and ch. 9",
        "c5": "Halliday ch. 18 Temperature, Heat, and the First Law of Thermodynamics · Young and Freedman ch. 17 and 19",
        "c6": "Halliday ch. 19 The Kinetic Theory of Gases · Young and Freedman ch. 18",
        "c7": "Halliday ch. 20 Entropy and the Second Law of Thermodynamics · Young and Freedman ch. 20",
    },
    "Physics-2": {
        "c1": "Halliday ch. 21 Coulomb's Law · Young and Freedman ch. 21 (21.1–21.3)",
        "c2": "Halliday ch. 22 Electric Fields · Young and Freedman ch. 21 (21.4–21.7)",
        "c3": "Halliday ch. 23 Gauss' Law · Young and Freedman ch. 22",
        "c4": "Halliday ch. 24 Electric Potential · Young and Freedman ch. 23",
        "c5": "Halliday ch. 28 Magnetic Fields · Young and Freedman ch. 27",
        "c6": "Halliday ch. 29 Magnetic Fields Due to Currents · Young and Freedman ch. 28",
        "c7": "Halliday ch. 30 Induction and Inductance · Young and Freedman ch. 29–30",
        "c8": "Halliday ch. 33 (reflection, refraction, polarization) · Young and Freedman ch. 33",
        "c9": "Halliday ch. 34 Images · Young and Freedman ch. 34",
        "c10": "Halliday ch. 35 Interference · Young and Freedman ch. 35",
        "c11": "Halliday ch. 36 Diffraction · Young and Freedman ch. 36",
    },
}

FACTS = {
    "Calculus-1": dict(
        who="Course advice sheet by Pham Minh Tri (AY 2025–26; lecturers Le Hai Khoi, Vu Tuan Anh, Nguyen Dinh Vu)",
        rows=[("Attendance", "5%", "lectures and tutorials"), ("Activity", "10%", "you must correct tutor exercises at least 6 times in the 12 tutorials to get the full 20/20 here"),
              ("Midterm", "25%", "MCQ test on Moodle (the advice sheet says 16 questions; the Moodle mock you shared has 20 random questions from chapters 1–3, 50 minutes, no going back, first attempt graded)"),
              ("Final", "60%", "written test: 5 questions of 4 points each")],
        notes=["Calculus I at USTH is single-variable calculus (calculation-oriented, not proof-oriented analysis).", "About 60–80% of the content is familiar from high school, yet the first-take failing rate was around 70% in AY 2025–26: the written test is demanding and carelessness is costly.",
               "Chapters 5 (techniques of integration, improper integrals) and especially 6 (sequences and series) are the hardest."]),
    "Linear-Algebra": dict(
        who="Course advice sheet by Nguyen Hai Long (AY 2025–26; lecturer Dao Quang Duc)",
        rows=[("Attendance", "10%", "you are barred from the final if you miss more than 30% of sessions without a valid reason"), ("Midterm", "30%", "written test or MCQ on Moodle, depending on the tutorial lecturer; up to 6 bonus points from tutorials can be added to it"),
              ("Final", "60%", "written test, 120 minutes, 5 questions with 2–3 parts each; calculators are not allowed in the midterm and final (the 2023–24 Shift 1 paper allowed them)")],
        notes=["Main textbook: Elementary Linear Algebra (8th edition) — the course content and many exercises come from it; Strang's book is better for review after you have learned the material.",
               "Vector spaces (chapter 4) is the make-or-break topic: eigenvalues, inner products and linear maps all depend on it.", "Calculations are easy but long and there is no calculator: practise exact fractions, and show every row operation."]),
    "Physics-1": dict(
        who="Course advice sheet by Pham Hieu Dung (AY 2025–26)",
        rows=[("Attendance", "10%", "lecture and tutor class; you are barred from the final if you miss more than 30% of sessions without a valid reason"),
              ("Midterm", "30%", "MCQ test on Moodle, 20 questions (the documents do not give the duration; the mocks here use 40 minutes, our assumption)"),
              ("Final", "60%", "MCQ test on Moodle, 40 questions (duration not stated; the mocks use 80 minutes, our assumption)")],
        notes=["Content: Mechanics (kinematics, Newton's laws of motion, conservation of energy and momentum, circular motion) and Thermodynamics (zeroth, first and second laws, ideal gases, kinetic theory, entropy).",
               "Bonus points are given generously in lectures and tutor classes: up to 4 points can be added directly to the final exam (the method differs per tutor lecturer).",
               "The form of the test varies from year to year (multiple choice or constructed response, or both) and a large share of the midterm and final questions come from the tutor problems, so work through them all.",
               "Thermodynamics appears a lot in the final and is harder than Mechanics; for Mechanics practise the Newton's-law and force problems."]),
    "Physics-2": dict(
        who="Course advice sheet by Bui Thien Truong, Hoang Tien Anh and Huynh Nguyen Van Anh (AY 2025–26)",
        rows=[("Attendance", "10%", "lecture and tutor class"), ("Midterm", "30%", "MCQ test on Moodle (the 2025–26 midterm tutoring covers chapters 1–6: Coulomb's law up to the magnetic fields of currents)"),
              ("Final", "60%", "MCQ test on Moodle (number of questions and duration are not stated in the documents; the mocks here use 40 questions and 80 minutes, our assumption)")],
        notes=["Three parts: Electricity (Coulomb's law, electric field, Gauss' law, electric potential), Magnetism (magnetic force, magnetic field, induction) and Optics (nature and propagation of light, geometric optics, interference, diffraction).",
               "One of the harder B1 courses because of the sheer number of formulae in every part. Electricity is easy if you follow the lectures; Magnetism needs more mathematics; Optics is the easiest but is stuffed with formulae.",
               "Bonus points: up to 6 points can be added to the midterm (any excess goes to the final).",
               "Visualise: pictures and videos help a lot with fields, forces and rays."]),
}

# strings that differ between the courses (the Maths strings are kept exactly as before)
UI = {
    "Calculus-1": dict(
        wdesc="The real Mock Test 1 plus two final-style mocks, full solutions, 120-minute exam mode with self-marking.",
        labdesc="Plots, limits, Newton, Riemann/Simpson, series, Taylor, antiderivative checker.",
        train=4, lab_title="Calculus lab", lab_scripts=["vendor/mathjs/math.min.js", "calc-lab.js"], bank_unit="questions"),
    "Linear-Algebra": dict(
        wdesc="Eight real past finals (2018–2025) with full worked solutions, exam mode with timer and self-marking.",
        labdesc="Exact multi-method solvers: Gauss, Gauss–Jordan, Cramer, inverse, LU, Jacobi, eigen tools, Jacobian.",
        train=4, lab_title="Linear Algebra lab", lab_scripts=["vendor/mathjs/math.min.js", "la.js", "la-lab.js"], bank_unit="questions"),
    "Physics-1": dict(
        wdesc="Multi-part problems from the tutorial sheets, in exam format with full worked solutions, a timer and self-marking.",
        labdesc="Interactive simulators: kinematics solver, projectile, relative velocity, forces and ramps, collisions, circular motion, calorimetry, gas processes and p–V diagrams, heat engines.",
        train=5, lab_title="Physics I lab", lab_scripts=["lab-phys.js", "lab-ph1.js"], bank_unit="questions"),
    "Physics-2": dict(
        wdesc="Multi-part problems from the homework and tutorial sheets, in exam format with full worked solutions, a timer and self-marking.",
        labdesc="Interactive simulators: point charges, fields and potential maps, Gauss' law, charged particles in fields, magnetic fields, induction, refraction, lenses and mirrors, interference and diffraction.",
        train=5, lab_title="Physics II lab", lab_scripts=["lab-phys.js", "lab-ph2.js"], bank_unit="questions"),
}

def counts_by_ch(bank):
    c = defaultdict(Counter)
    for q in bank["items"]:
        c[q["ch"]][q["origin"]] += 1
    return c

# ------------------------------------------------------------------------------------------ pages
def home(course, nmod):
    c = COURSES[course]; meta = load_json(course + "/data/meta.json"); f = FACTS[course]; ui = UI[course]
    nq = sum(meta["counts"].values())
    rows = "".join("<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>" % (a, b, esc(d)) for a, b, d in f["rows"])
    notes = "".join("<li>%s</li>" % esc(n) for n in f["notes"])
    mid = meta["sets"]["midterm"][0]
    fin = meta["sets"].get("final")
    if fin:
        examdesc = "Midterm mocks (%d questions) · final mocks (%d questions) · speed exam: 30 questions in 20 minutes · custom exams." % (len(mid["ids"]), len(fin[0]["ids"]))
    else:
        examdesc = "%s · Speed exam: 30 questions in 20 minutes · custom exams." % esc(mid["title"].split(" · ")[0])
    train4 = ("<li><b>Simulate the exams:</b> the mock midterm (no going back), then the 30-question / 20-minute speed exam. Aim for 40 seconds per question and review every explanation afterwards.</li>" if ui["train"] == 4 else
              "<li><b>Simulate the exams:</b> the mock midterm (no going back), the 40-question mock final, then the 30-question / 20-minute speed exam. Review every explanation afterwards, also for the questions you got right.</li>")
    have = hv(course)
    cards = []
    if "modules" in have: cards.append('<a class="card" href="modules/index.html"><b>📖 Modules (slides)</b><span>%d modules with USTH-style slide decks, worked examples and a textbook map.</span></a>' % nmod)
    cards.append('<a class="card" href="quiz/index.html"><b>📘 Chapter quizzes</b><span>3 sets per chapter, 12 questions each, instant feedback and explanations.</span></a>')
    cards.append('<a class="card" href="exam/index.html"><b>⏱ Mock exams</b><span>%s</span></a>' % examdesc)
    if "written" in have: cards.append('<a class="card" href="written/index.html"><b>✍️ Written practice</b><span>%s</span></a>' % ui["wdesc"])
    cards.append('<a class="card" href="bank/index.html"><b>🗂 Practice bank</b><span>All %d questions: filter by chapter, topic, level and source; written mode.</span></a>' % nq)
    if "lab" in have: cards.append('<a class="card" href="lab/index.html"><b>🧮 Lab</b><span>%s</span></a>' % ui["labdesc"])
    cards.append('<a class="card" href="sources/index.html"><b>📚 Sources and coverage</b><span>Every document used, textbook map, errors found in the course materials.</span></a>')
    learn = ('<li><b>Learn a module</b> with its <a href="modules/index.html">slides</a>, your lecture slides and the textbook sections listed on each module page.</li>' if "modules" in have else
             '<li><b>Learn the chapter</b> from your lecture slides and the textbook sections listed in the <a href="sources/index.html">Sources</a> page.</li>')
    body = """
<h1>%(name)s <span class="muted">(%(code)s)</span> — self-study and exam-training system</h1>
<p class="lead">%(tag)s Built from the course lectures, tutorial sheets, extra problems, mock tests and past finals. <b>%(nq)d</b> questions with computed answers and worked explanations.</p>
<div class="cards">
%(cards)s
</div>
<h2>Your progress</h2>
<div class="panel" id="progress" data-base="data/" data-course="%(slug)s"><span class="muted">Loading…</span></div>
<h2>How to train with this site</h2>
<ol>
 %(learn)s
 <li><b>Quiz it:</b> do the three sets of that chapter. Read every explanation, also for the questions you got right. Use "Redo only the mistakes".</li>
 <li><b>Go deeper</b> in the <a href="bank/index.html">practice bank</a>: tick <i>written mode</i> to hide the options, solve on paper, then compare with the model answer.</li>
 %(train4)s
 <li><b>Repeat the weak chapters</b> shown in the progress panel above until each is above 75%%.</li>
</ol>
<h2>About the course (%(who)s)</h2>
<div class="panel"><table class="t"><tr><th>Component</th><th>Weight</th><th>Details</th></tr>%(rows)s</table><ul>%(notes)s</ul>
<p class="muted">Information of academic year 2025–26 only; check the official GED announcements for your year.</p></div>
""" % dict(name=c["name"], code=c["code"], tag=esc(c["tagline"]), nq=nq, slug=course, who=esc(f["who"]), rows=rows, notes=notes, train4=train4, cards="\n".join(" " + x for x in cards), learn=learn)
    return page(course, "Home", body, 0, "home", scripts=["home.js"], have=hv(course))

def quiz_hub(course):
    meta = load_json(course + "/data/meta.json")
    has_h = any(z["id"].endswith("-H") for sets in meta["sets"]["chapter"].values() for z in sets)
    hn = [len(z["ids"]) for sets in meta["sets"]["chapter"].values() for z in sets if z["id"].endswith("-H")]
    hard_note = ", plus a <b>Hard set</b> of Moodle-style level-4 questions where the chapter has enough of them (%d to %d questions)" % (min(hn), max(hn)) if has_h else ""
    rows = ""
    for ch in meta["chapters"]:
        sets = meta["sets"]["chapter"][ch["id"]]
        links = " ".join('<a class="btn %s" href="run.html?set=%s">%s</a>' % ("small alt" if s["id"].endswith("-H") else "small", s["id"], "Hard set" if s["id"].endswith("-H") else "Set %s" % s["id"][-1]) for s in sets)
        rows += "<tr><td><b>%s</b></td><td>%s<div class='muted'>%s</div></td><td>%d</td><td>%s <a class='btn small alt' href='../bank/index.html?ch=%s'>All questions</a></td></tr>" % (
            ch["id"].upper().replace("C", "Ch. "), esc(ch["title"]), esc(ch["src"]), meta["counts"][ch["id"]], links, ch["id"])
    body = """<h1>Chapter quizzes</h1>
<p class="lead">Three different sets for every chapter (12 questions each, no repeated questions between the sets)%s. Answer, get instant feedback with a worked explanation, retry, and save your score.</p>
<div class="panel"><table class="t"><tr><th>Chapter</th><th>Topic and where it comes from</th><th>Bank size</th><th>Quizzes</th></tr>%s</table></div>
<p class="muted">Tip: do Set A cold, study the explanations, then Set B a day later and Set C a week later (spaced repetition).</p>""" % (hard_note, rows)
    return page(course, "Chapter quizzes", body, 1, "quiz", have=hv(course))

def quiz_run(course):
    body = '<h1>Quiz</h1><div id="runner" data-base="../data/" data-course="%s"><p class="muted">Loading…</p></div>' % course
    return page(course, "Quiz", body, 1, "quiz", scripts=["quiz.js"], have=hv(course))

EXAM_NOTES = {
    "Calculus-1": "Format of the Moodle mock: <b>20 random questions from chapters 1–3, 50 minutes, you cannot return to previous questions, first attempt graded.</b> (The advice sheet for the real midterm mentions 16 questions.) Mocks A–E are deliberately <b>tougher than the real thing</b>: they are built from the level-4 pool (traps, hidden orders in limits, tables, word problems), so a good score here leaves a safety margin.",
    "Linear-Algebra": "The advice sheet says the midterm is a written test or an MCQ test on Moodle depending on the tutorial lecturer. These mocks use the same style (20 questions, 50 minutes) on chapters 1–4 — <b>the covered chapters are our assumption</b>; adjust with the custom builder below.",
    "Physics-1": "The advice sheet says the midterm is an <b>MCQ test on Moodle with 20 questions</b>; the midterm tutoring slides cover Mechanics (chapters 1–4). <b>The time limit is not stated in the documents</b>: these mocks use 40 minutes (2 minutes per question, our assumption) and, like the Moodle mocks, do not let you go back.",
    "Physics-2": "The advice sheet says the midterm is an <b>MCQ test on Moodle</b>; the 2025–26 midterm tutoring slides cover chapters 1–6 (Coulomb's law up to the magnetic fields of currents). <b>The number of questions and the time limit are not stated</b>: these mocks use 20 questions in 40 minutes (our assumption) and do not let you go back.",
}
FINAL_NOTES = {
    "Physics-1": "The final is an <b>MCQ test on Moodle with 40 questions</b> (the duration is not stated; 80 minutes here, our assumption). Thermodynamics appears a lot in the final, so the mix below is weighted towards chapters 5–7. You may move freely between questions.",
    "Physics-2": "The final is an <b>MCQ test on Moodle</b> (40 questions and 80 minutes are our assumption). The final tutoring slides concentrate on induction and optics, so the mix below is weighted towards chapters 5–11 with a small share of electricity. You may move freely between questions.",
}

def exam_hub(course):
    meta = load_json(course + "/data/meta.json")
    mid = meta["sets"]["midterm"]; sp = meta["sets"]["sprint"]; fin = meta["sets"].get("final")
    mlinks = " ".join('<a class="btn" href="run.html?exam=%s">Mock %s</a>' % (s["id"], s["id"][-1]) for s in mid) + ' <a class="btn alt" href="run.html?exam=midterm-random">🎲 New random midterm</a>'
    slinks = " ".join('<a class="btn" href="run.html?exam=%s">Speed %s</a>' % (s["id"], s["id"][-1]) for s in sp) + ' <a class="btn alt" href="run.html?exam=sprint-random">🎲 New random speed exam</a>'
    chk = "".join('<label><input type="checkbox" value="%s" checked> %s</label><br>' % (c["id"], esc(c["id"].upper().replace("C", "Ch. ") + " " + c["title"])) for c in meta["chapters"])
    qc = meta["midterm_quota"]
    mix = lambda q: ", ".join("%d from %s" % (v, k.upper().replace("C", "Ch. ")) for k, v in q.items())
    tough = (" Difficulty mix: about %d%% expert (level 4) and %d%% hard (level 3) questions." % tuple(round(100 * f) for _, f in meta["mid_share"][:2])) if meta.get("mid_share") else ""
    finpanel = ""
    rep = meta["sets"].get("replica")
    if rep:
        rlinks = " ".join('<a class="btn" href="run.html?exam=%s">Replica %s</a>' % (z["id"], z["id"][-1]) for z in rep)
        finpanel += ('<div class="panel"><h2 style="margin-top:0">🎯 Moodle-style replica mocks — 20 questions, 50 minutes, no going back</h2>'
                     '<p>Each replica copies the <b>blueprint of the real Moodle mock, slot by slot</b>: a tangent slope, a composite limit with a hidden-order trap, a theorem-hypotheses question, a linearization trap, a chain rule from a table, a modelling question, monotonic intervals, a one-sided limit, a limit with two conjugates, a product derivative at a point, a “function on its domain” trap, a physical-law related rate, an IVT word problem, a continuity parameter, a quotient derivative, a two-moving-objects related rate, a limits-and-inequalities statement, a parity count, an IVT sign-change interval and critical points with fractional powers. '
                     'Numbers and functions are new; every answer is computed and re-derived by a second route.</p><p>%s</p></div>' % rlinks)
    if fin:
        flinks = " ".join('<a class="btn" href="run.html?exam=%s">Final %s</a>' % (s["id"], s["id"][-1]) for s in fin) + ' <a class="btn alt" href="run.html?exam=final-random">🎲 New random final</a>'
        finpanel = """<div class="panel"><h2 style="margin-top:0">🎓 Final mock — %d questions, %d minutes</h2><p>%s Question mix: %s.</p><p>%s</p></div>""" % (len(fin[0]["ids"]), fin[0]["minutes"], FINAL_NOTES[course], mix(meta["final_quota"]), flinks)
    body = """<h1>Mock exams</h1>
<div class="panel"><h2 style="margin-top:0">📝 Midterm mock — %(mt)s</h2><p>%(note)s Question mix: %(mix)s.%(tough)s</p><p>%(ml)s</p></div>
%(finpanel)s<div class="panel"><h2 style="margin-top:0">⚡ Speed exam — 30 questions in 20 minutes (40 s per question)</h2><p>Questions drawn from every chapter (about equal numbers). You may jump around; the palette shows what you have answered. Use it to train speed and accuracy: skip fast, come back later.</p><p>%(sl)s</p></div>
<div class="panel"><h2 style="margin-top:0">🛠 Build your own exam</h2>
<form id="custom"><div class="row"><div>%(chk)s</div><div><label>Questions <input type="number" id="n" value="15" min="5" max="60" style="width:5em"></label><br>
<label>Minutes <input type="number" id="min" value="10" min="1" max="120" style="width:5em"></label><br><label><input type="checkbox" id="fwd"> forward only (no going back)</label><br>
<button class="btn" type="submit" style="margin-top:8px">Start</button></div></div></form></div>
<p class="muted">Results (score, time, chapter breakdown, review of every question) are saved in this browser and feed the progress panel on the home page.</p>""" % dict(
        mt=esc(meta["midterm_title"].split(" (")[0]), note=EXAM_NOTES[course], mix=mix(qc), tough=tough, ml=mlinks, sl=slinks, chk=chk, finpanel=finpanel)
    inline = """<script>document.getElementById('custom').addEventListener('submit',function(e){e.preventDefault();var ch=[].slice.call(document.querySelectorAll('#custom input[type=checkbox][value]:checked')).map(function(x){return x.value}).join(',');if(!ch){alert('Select at least one chapter');return}
location.href='run.html?exam=custom&ch='+ch+'&n='+document.getElementById('n').value+'&min='+document.getElementById('min').value+'&fwd='+(document.getElementById('fwd').checked?1:0)});</script>"""
    return page(course, "Mock exams", body + inline, 1, "exam", have=hv(course))

def exam_run(course):
    body = '<h1>Exam</h1><div id="runner" data-base="../data/" data-course="%s"><p class="muted">Loading…</p></div>' % course
    return page(course, "Exam", body, 1, "exam", scripts=["quiz.js"], have=hv(course))

def bank_page(course):
    meta = load_json(course + "/data/meta.json")
    body = """<h1>Practice bank</h1><p class="lead">%d questions. Each one cites its source (course document, or generated in the same style) and has a worked explanation. Tick <i>written mode</i> to hide the options and work like in the written final.</p>
<div id="bank" data-base="../data/" data-course="%s"><p class="muted">Loading…</p></div>""" % (sum(meta["counts"].values()), course)
    if course in PHYSICS:
        body = body.replace("and work like in the written final", "and solve on paper first (the exam itself is multiple choice, but the working is what you are training)")
    return page(course, "Practice bank", body, 1, "bank", scripts=["bank.js"], have=hv(course))

def load_inventory():
    inv = []
    for fn in ("_inventory.json", "_inventory_phys.json"):
        p = os.path.join(ROOT, "..", "text_raw", fn)
        if os.path.exists(p):
            inv += json.load(open(p, encoding="utf-8"))
    return inv

def doc_role(course, path):
    p = path.lower()
    if course in PHYSICS:
        if "small advice" in p: return "Course advice sheet: assessment, exam format, study tips (used on the home and exam pages)"
        if "/2. textbook" in p: return "Reference reading (chapter map below)"
        if "/4. tutorial" in p or "list of exercises" in p: return "Exercise source: the numerical problems and multiple-choice questions became questions with the sheet's own numbers; figure-only items were re-drawn with our own data"
        if "/1. tutor" in p: return "Tutoring slides / formula sheets by the Learning Support team (some scanned and OCR read): exam-style problems and the exam structure"
        if "/3. lecture" in p or "/3. lectures" in p: return "Lecture slides: chapter outline, definitions, worked examples and concept checks"
        return "Reference"
    if "/lectures/" in p: return "Lecture slides: chapter outline, concept checks"
    if "tutorials/" in p or "/tutor/" in p: return "Exercise source: every auto-checkable problem is a question; the rest is kept for the written practice"
    if "additional problems" in p: return "Exercise source (training problems)"
    if "sample tests" in p: return "Past final exam: problems solved in full on the Written page"
    if "mocktest" in p: return "Mock test source"
    if "textbooks" in p: return "Reference reading (chapter map below)"
    if "linear algebra summary" in p: return "Theory summary with worked exercises: its exercises became questions labelled 'Linear Algebra Summary (Gen 16)'; the slips found in it are listed below"
    if "final tutorial" in p or "tutor for final" in p:
        return ("Final-exam tutoring slides (scanned, OCR read): the worked examples became questions labelled 'Final tutorial (session 1/2)'" if course == "Calculus-1"
                else "Final-exam tutoring slides (scanned, OCR read): theory recap and exam-style problems, covered by the bank and the Written papers")
    if "sharing" in p: return "Sharing-session slides (scanned, OCR read)"
    return "Reference"

DOC_PREFIX = {"Calculus-1": "MAT1.001", "Linear-Algebra": "MAT1.002", "Physics-1": "PHY1.001", "Physics-2": "PHY1.002"}

def sources_page(course):
    meta = load_json(course + "/data/meta.json"); bank = load_json(course + "/data/bank.json")
    cc = counts_by_ch(bank)
    inv = load_inventory()
    prefix = DOC_PREFIX[course]
    rows = ""
    for r in inv:
        if r["file"].startswith(prefix) and "error" not in r:
            rows += "<tr><td>%s</td><td>%d</td><td>%s</td></tr>" % (esc(r["file"].split("/", 1)[1] if "/" in r["file"] else r["file"]), r["pages"], esc(doc_role(course, r["file"])))
    cov = ""
    has_hard = any(q["origin"] == "hard" for q in bank["items"])
    for ch in meta["chapters"]:
        k = cc[ch["id"]]
        cov += "<tr><td><b>%s</b> %s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td>%s<td>%s</td></tr>" % (ch["id"].upper().replace("C", "Ch. "), esc(ch["title"]), sum(k.values()), k["src"], k["gen"], k["concept"], ("<td>%d</td>" % k["hard"]) if has_hard else "", esc(TEXTBOOKS[course][ch["id"]]))
    notes = load_json(course + "/data/notes.json") if os.path.exists(os.path.join(ROOT, course, "data", "notes.json")) else []
    nhtml = "".join("<li><b>%s</b>: %s</li>" % (esc(n["src"]), esc(n["note"]).replace("$", "$")) for n in notes) or "<li>None found.</li>"
    if course in PHYSICS:
        how = """<h2>How answers were verified</h2><div class="panel"><ul><li>Every correct answer is produced by code from the physical law (never typed by hand) and re-derived by a second, independent route before the question is kept: another formula (energy instead of kinematics, momentum instead of forces), root finding, numerical integration, a numerical simulation of the motion, or ray-transfer matrices. The build stops when the two routes disagree.</li>
<li>For problems taken from the course sheets the numbers of the sheet are used. Where the printed statement depends on a figure we could not reproduce, the setting was redrawn with our own data and the question is labelled <i>generated, same style</i>.</li>
<li>Distractors are the realistic mistakes (forgotten factor 2, sin and cos swapped, centimetres not converted, Celsius used instead of kelvin, wrong sign of the work, mass forgotten ...); every option of a question differs from the others at the displayed precision.</li>
<li>Option positions are shuffled with a fixed seed and balanced (A/B/C/D each 25%); the correct option is not systematically the longest.</li></ul></div>"""
    else:
        how = """<h2>How answers were verified</h2><div class="panel"><ul><li>All answers are produced by code (sympy exact arithmetic, never typed by hand) and, for source problems, compared with the printed answer key; the build stops if they disagree.</li>
<li>Distractors are realistic mistakes (sign errors, missing chain-rule factor, transposed matrices, wrong-order composition…), and every distractor is checked to be different from the correct answer.</li>
<li>Option positions are shuffled with a fixed seed and balanced (A/B/C/D each 25%); the correct option is not systematically the longest.</li></ul></div>"""
    if has_hard:
        how = how.replace("</ul></div>", "<li><b>Moodle-style hard pool (level 4).</b> Built from the 20 blueprint slots of the real Moodle mock midterm (traps, composite limits, tables, modelling, IVT word problems, related rates) with new numbers; each answer is re-derived by a second route (60-digit numerical limits, cubic Hermite interpolation of the tables, finite differences of explicit functions, numerical quadrature or partial sums).</li></ul></div>", 1)
    extra_scan = ("PDFs with a text layer were converted with pdftotext; scanned PDFs were OCR'd with tesseract and the formulas were checked against the page images. Where a problem statement mixed text and a figure, only the text-complete parts became questions."
                  if course in MATHS else
                  "PDFs with a text layer were converted with pdftotext, Word and PowerPoint files with python-docx / python-pptx; scanned slides and handwritten notes were OCR'd with tesseract and read against the page images. The textbooks are listed for reference only and are not part of the site.")
    body = """<h1>Sources, coverage and document notes</h1>
<p class="lead">What was read, how each document was used, how many questions come from each chapter, and the errors we found in the course materials.</p>
<h2>Documents read</h2><div class="panel"><table class="t"><tr><th>Document</th><th>Pages</th><th>How it is used</th></tr>%s</table>
<p class="muted">%s</p></div>
<h2>Question coverage per chapter</h2><div class="panel" style="overflow-x:auto"><table class="t"><tr><th>Chapter</th><th>Total</th><th>From course documents</th><th>Generated (same style)</th><th>Concept checks</th>%s<th>Textbook sections</th></tr>%s</table></div>
<h2>Errors and oddities found in the course documents</h2><div class="panel"><p>Each item below was found by checking our computed answer against the printed one (or when an exercise turned out to be impossible as printed). The quiz uses the computed result.</p><ul>%s</ul></div>
%s""" % (rows, extra_scan, "<th>Moodle-style hard (level 4)</th>" if has_hard else "", cov, nhtml, how)
    return page(course, "Sources", body, 1, "sources", have=hv(course))

LAB_INTRO = {
    "Calculus-1": """<h1>Calculus lab</h1><p class="lead">Numerical and graphical tools to check your hand work: plot a function with its derivative and tangent line, explore limits, run Newton's method and bisection, compare Riemann sums with the trapezoid and Simpson rules, watch partial sums of a series, build Taylor polynomials with the error bound, test an antiderivative by differentiating it, and get the critical points and inflection points of a curve.</p>
<p class="muted">Write functions like in a calculator: <code>x^3 - 3*x</code>, <code>sin(x)/x</code>, <code>exp(-x^2)</code>, <code>sqrt(x)</code>, <code>log(x)</code> (natural log), <code>pi</code>. Numerical output is evidence, not proof: the exam asks for exact answers and justification.</p><div id="lab" class="lab"></div>""",
    "Linear-Algebra": """<h1>Linear Algebra lab</h1><p class="lead">Exact arithmetic (fractions, no rounding) with every step shown. Each tool solves the same problem by <b>several methods</b> — Gauss and Gauss–Jordan elimination, Cramer's rule, the inverse matrix, LU factorisation, Jacobi and Gauss–Seidel iteration; row reduction, cofactor expansion and Sarrus for determinants; Gauss–Jordan and adjugate for inverses — and checks that they agree.
There is also a scanner for systems with a parameter <i>k</i> (like question 1(b) and 2(a) of the finals), eigen-tools, orthogonal tools, matrices relative to bases and a Jacobian-matrix tool (an extension beyond MAT1.002: the Jacobian is the matrix of the linear map that best approximates a function near a point).</p>
<p class="muted">Enter matrices with one row per line and entries separated by spaces (fractions like 3/4 are fine). The lab is a checking aid: in the exam there is no calculator, so always practise the hand computation first.</p><div id="lab" class="lab"></div>""",
    "Physics-1": """<h1>Physics I lab</h1><p class="lead">Interactive simulators and calculators to see what the formulas say. Change a number and the answer, the formulas used and the picture update: solve any uniform-acceleration problem from three known quantities, fly a projectile, add velocities in moving frames, push blocks on ramps and over pulleys, collide carts, spin objects in circles, mix hot and cold water, take an ideal gas around a cycle on a <i>p</i>–<i>V</i> diagram, and compare engines and refrigerators.</p>
<p class="muted">Every tool shows the equations it uses with your numbers substituted. Use it to check a hand calculation, not to replace it: the exams are multiple choice but the reasoning is what is being tested. SI units unless a field says otherwise; <i>g</i> = 9.8 m/s² by default.</p><div id="lab" class="lab"></div>""",
    "Physics-2": """<h1>Physics II lab</h1><p class="lead">Interactive simulators and calculators for electricity, magnetism and optics: place point charges and read the force, field and potential at any point (with an equipotential map), see Gauss' law for spheres, cylinders and sheets, follow a charged particle through electric and magnetic fields, get the magnetic field of wires, loops and solenoids, simulate Faraday's law, RL and LC circuits, trace rays through a surface, a lens or a mirror, and plot double-slit, single-slit and grating patterns.</p>
<p class="muted">Every tool shows the equations it uses with your numbers substituted. Use it to check a hand calculation, not to replace it. SI units unless a field says otherwise.</p><div id="lab" class="lab"></div>""",
}

def lab_page(course):
    return page(course, "Labs", LAB_INTRO[course], 1, "lab", scripts=UI[course]["lab_scripts"], have=hv(course))

WRITTEN_INTRO = {
    "Calculus-1": """<h1>Written practice: the real mock test and two final-style mocks</h1><p class="lead">The final is a <b>written test of 5 questions worth 4 points each</b>. <b>Mock Test 1</b> is the real mock paper of 2025–26 from the course materials; <b>mock B</b> and <b>mock C</b> follow the same format and were written for this site from the problem types of the tutorials. Every part has the answer and a full worked solution (final answers are verified by computer algebra); some parts link to the lab.</p>""",
    "Linear-Algebra": """<h1>Written practice: eight past finals with full solutions</h1><p class="lead">The final is a <b>written test of 5 questions, each with 2–3 parts, 120 minutes</b>, usually without a calculator. These are the real papers of 2018–2025 (both groups of 2018–19 and both shifts of 2023–24 and 2024–25). Every part has the answer and a complete worked solution, computed in exact arithmetic with every row operation shown; some parts link to the lab where you can check the same data by several methods.</p>""",
    "Physics-1": """<h1>Written practice: multi-part problems with full solutions</h1><p class="lead">The documents say the form of the test varies from year to year (multiple choice, constructed response, or both), and the tutorial sheets are made of multi-part problems. These papers collect the classic tutorial problems of each part as <b>written problems with their full worked solutions</b>: take a paper as an exam (timer, statements only), then mark yourself part by part. The numbers are those of the tutorial sheets where the statement is text-complete, and every result is verified by a second method.</p>""",
    "Physics-2": """<h1>Written practice: multi-part problems with full solutions</h1><p class="lead">The tutorial sessions are made of multi-part problems from the Halliday and Young &amp; Freedman problem lists. These papers collect the classic problems of each part as <b>written problems with their full worked solutions</b>: take a paper as an exam (timer, statements only), then mark yourself part by part. The numbers are those of the homework sheets where the statement is text-complete, and every result is verified by a second method.</p>""",
}

def written_hub(course):
    body = WRITTEN_INTRO[course] + """<div class="callout"><b>Workflow.</b> 1) Take a paper as an <i>exam</i> (timer, statements only). 2) Mark yourself part by part against the model solutions. 3) Redo the parts you lost marks on in <i>study</i> mode, then drill the topic in the quizzes. Results are saved in this browser.</div><div id="written-hub" data-base="../data/" data-course="%s" data-lab="../lab/index.html"><p class="muted">Loading…</p></div>""" % course
    return page(course, "Written practice", body, 1, "written", scripts=["written.js"], have=hv(course))

def written_paper(course):
    body = '<div id="written" data-base="../data/" data-course="%s" data-lab="../lab/index.html"><p class="muted">Loading…</p></div>' % course
    return page(course, "Written paper", body, 1, "written", scripts=["written.js"], have=hv(course))

# ------------------------------------------------------------------------------------------ root landing page
def root_index():
    avail = available_courses()
    nq = {c: sum(load_json(c + "/data/meta.json")["counts"].values()) for c in avail}     # read from the generated data, never typed
    nch = {c: len(load_json(c + "/data/meta.json")["chapters"]) for c in avail}
    desc = {"Calculus-1": ("Calculus I · MAT1.001", "Limits, derivatives, integrals, sequences and series."),
            "Linear-Algebra": ("Linear Algebra · MAT1.002", "Systems, matrices, determinants, vector spaces, inner products, linear maps, eigenvalues."),
            "Physics-1": ("Fundamental Physics I · PHY1.001", "Kinematics, Newton's laws, energy and momentum, circular motion, heat, kinetic theory, entropy."),
            "Physics-2": ("Fundamental Physics II · PHY1.002", "Coulomb's law, electric fields, Gauss' law, potential, magnetic force and fields, induction, light, lenses, interference, diffraction.")}
    def cards(group):
        return "".join('<a class="card" href="%s/index.html"><b>%s</b><span>%s %d chapters, %d questions.</span></a>' % (c, desc[c][0], desc[c][1], nch[c], nq[c]) for c in group if c in avail)
    phys = cards(PHYSICS)
    physblock = ("<h2>Physics</h2>\n<div class=\"cards\">%s</div>\n" % phys) if phys else ""
    html_ = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>USTH B1 — Maths and Physics self-study</title>
<link rel="icon" type="image/png" href="shared/img/favicon.png"><link rel="apple-touch-icon" href="shared/img/apple-touch-icon.png"><link rel="stylesheet" href="shared/core.css"><script>(function(){try{var t=JSON.parse(localStorage.getItem('ustm:theme')||'null');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}catch(e){}})();</script><script src="shared/gate.js"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="index.html"><img src="shared/img/usth_logo.png" alt="USTH"><span>USTH B1 · Maths and Physics self-study</span></a></div></header>
<main class="wrap"><div class="hero"><span class="chip big"><img src="shared/img/usth_logo.png" alt="USTH – University of Science and Technology of Hanoi"><img src="shared/img/usth_dses_logo.png" alt="DSES"></span><span class="muted">University of Science and Technology of Hanoi · Department of Mathematics &amp; ICT · B1 year</span></div>
<h1>USTH B1 Mathematics and Physics: self-study and exam-training sites</h1>
<p class="lead">Unofficial study systems built from the course documents: quizzes per chapter, mock midterms and finals, a 30-questions-in-20-minutes speed exam, a verified practice bank, slides and interactive tools.</p>
<h2>Mathematics</h2>
<div class="cards">%s</div>
%s<p class="muted">The Vietnamese versions will be added as separate sites. Everything runs in your browser; progress stays on your device.</p></main></body></html>""" % (cards(MATHS), physblock)
    write("index.html", html_)

def available_courses():
    """Courses with data; USTM_COURSES=Calculus-1,Linear-Algebra limits a build to some of them (a course not ready to publish stays out of the hub)."""
    only = os.environ.get("USTM_COURSES")
    return [c for c in COURSES if os.path.exists(os.path.join(ROOT, c, "data", "meta.json")) and (not only or c in only.split(","))]

def main():
    import build_modules, modules_cal, modules_la, lecture_pages
    mods = {"Calculus-1": modules_cal.MODULES, "Linear-Algebra": modules_la.MODULES}
    for name, key in (("modules_ph1", "Physics-1"), ("modules_ph2", "Physics-2")):
        try:
            mods[key] = __import__(name).MODULES
        except ImportError:
            mods[key] = []
    courses = available_courses()
    for course in courses:
        h = {"quiz", "exam", "bank", "sources"}
        if mods.get(course): h.add("modules")
        if lecture_pages.any_lectures(course): h.add("lectures")
        if all(os.path.exists(os.path.join(ROOT, "shared", sc)) for sc in UI[course]["lab_scripts"]): h.add("lab")
        pp = os.path.join(ROOT, course, "data", "papers.json")
        if os.path.exists(pp) and json.load(open(pp, encoding="utf-8")): h.add("written")
        HAVE_BY_COURSE[course] = h
    if os.environ.get("USTM_ONLY") == "lectures":                # quick loop while authoring lecture scripts: rebuild only the lecture pages
        for course in courses:
            if "lectures" in hv(course):
                print(course, "lectures: %d built, %d exercises checked, %d conceptual" % lecture_pages.build(course, hv(course)))
        return
    for course in courses:
        if mods.get(course):
            build_modules.build(course, mods[course], TEXTBOOKS[course], None, hv(course))
    for course in courses:
        h = hv(course)
        write(course + "/index.html", home(course, len(mods.get(course) or [])))
        write(course + "/quiz/index.html", quiz_hub(course)); write(course + "/quiz/run.html", quiz_run(course))
        write(course + "/exam/index.html", exam_hub(course)); write(course + "/exam/run.html", exam_run(course))
        write(course + "/bank/index.html", bank_page(course))
        write(course + "/sources/index.html", sources_page(course))
        if "lab" in h: write(course + "/lab/index.html", lab_page(course))
        if "lectures" in h: print(course, "lectures: %d built, %d exercises checked, %d conceptual" % lecture_pages.build(course, h))
        if "written" in h: write(course + "/written/index.html", written_hub(course)); write(course + "/written/paper.html", written_paper(course))
    root_index()
    print("pages written for", ", ".join(courses), "| sections:", {c: sorted(HAVE_BY_COURSE[c]) for c in courses if c in PHYSICS})

if __name__ == "__main__":
    main()
