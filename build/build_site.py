# -*- coding: utf-8 -*-
"""Assemble the static pages (milestone 1: home, chapter quizzes, exams, practice bank, sources)."""
import json, os, re, sys
from collections import Counter, defaultdict
from sitegen import *

HAVE = {"quiz", "exam", "bank", "sources", "lab"}      # pages built so far (nav shows only these)

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
}

def counts_by_ch(bank):
    c = defaultdict(Counter)
    for q in bank["items"]:
        c[q["ch"]][q["origin"]] += 1
    return c

# ------------------------------------------------------------------------------------------ pages
def home(course):
    c = COURSES[course]; meta = load_json(course + "/data/meta.json"); f = FACTS[course]
    nq = sum(meta["counts"].values())
    rows = "".join("<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>" % (a, b, esc(d)) for a, b, d in f["rows"])
    notes = "".join("<li>%s</li>" % esc(n) for n in f["notes"])
    mid = meta["sets"]["midterm"][0]
    body = """
<h1>%(name)s <span class="muted">(%(code)s)</span> — self-study and exam-training system</h1>
<p class="lead">%(tag)s Built from the course lectures, tutorial sheets, extra problems, mock tests and past finals. <b>%(nq)d</b> questions with computed answers and worked explanations.</p>
<div class="cards">
 <a class="card" href="quiz/index.html"><b>📘 Chapter quizzes</b><span>3 sets per chapter, 12 questions each, instant feedback and explanations.</span></a>
 <a class="card" href="exam/index.html"><b>⏱ Mock exams</b><span>%(midtitle)s · Speed exam: 30 questions in 20 minutes · custom exams.</span></a>
 <a class="card" href="bank/index.html"><b>🗂 Practice bank</b><span>All %(nq)d questions: filter by chapter, topic, level and source; written mode.</span></a>
 <a class="card" href="sources/index.html"><b>📚 Sources and coverage</b><span>Every document used, textbook map, errors found in the course materials.</span></a>
</div>
<h2>Your progress</h2>
<div class="panel" id="progress" data-base="data/" data-course="%(slug)s"><span class="muted">Loading…</span></div>
<h2>How to train with this site</h2>
<ol>
 <li><b>Learn a chapter</b> with your lecture slides and the textbook sections listed on the <a href="sources/index.html">Sources</a> page.</li>
 <li><b>Quiz it:</b> do the three sets of that chapter. Read every explanation, also for the questions you got right. Use "Redo only the mistakes".</li>
 <li><b>Go deeper</b> in the <a href="bank/index.html">practice bank</a>: tick <i>written mode</i> to hide the options, solve on paper, then compare with the model answer.</li>
 <li><b>Simulate the exams:</b> the mock midterm (no going back), then the 30-question / 20-minute speed exam. Aim for 40 seconds per question and review every explanation afterwards.</li>
 <li><b>Repeat the weak chapters</b> shown in the progress panel above until each is above 75%%.</li>
</ol>
<h2>About the course (%(who)s)</h2>
<div class="panel"><table class="t"><tr><th>Component</th><th>Weight</th><th>Details</th></tr>%(rows)s</table><ul>%(notes)s</ul>
<p class="muted">Information of academic year 2025–26 only; check the official GED announcements for your year.</p></div>
""" % dict(name=c["name"], code=c["code"], tag=esc(c["tagline"]), nq=nq, slug=course, who=esc(f["who"]), rows=rows, notes=notes, midtitle=esc(mid["title"].split(" · ")[0]))
    return page(course, "Home", body, 0, "home", scripts=["home.js"], have=HAVE)

def quiz_hub(course):
    meta = load_json(course + "/data/meta.json")
    rows = ""
    for ch in meta["chapters"]:
        sets = meta["sets"]["chapter"][ch["id"]]
        links = " ".join('<a class="btn small" href="run.html?set=%s">Set %s</a>' % (s["id"], s["id"][-1]) for s in sets)
        rows += "<tr><td><b>%s</b></td><td>%s<div class='muted'>%s</div></td><td>%d</td><td>%s <a class='btn small alt' href='../bank/index.html?ch=%s'>All questions</a></td></tr>" % (
            ch["id"].upper().replace("C", "Ch. "), esc(ch["title"]), esc(ch["src"]), meta["counts"][ch["id"]], links, ch["id"])
    body = """<h1>Chapter quizzes</h1>
<p class="lead">Three different sets for every chapter (12 questions each, no repeated questions between the sets). Answer, get instant feedback with a worked explanation, retry, and save your score.</p>
<div class="panel"><table class="t"><tr><th>Chapter</th><th>Topic and where it comes from</th><th>Bank size</th><th>Quizzes</th></tr>%s</table></div>
<p class="muted">Tip: do Set A cold, study the explanations, then Set B a day later and Set C a week later (spaced repetition).</p>""" % rows
    return page(course, "Chapter quizzes", body, 1, "quiz", have=HAVE)

def quiz_run(course):
    body = '<h1>Quiz</h1><div id="runner" data-base="../data/" data-course="%s"><p class="muted">Loading…</p></div>' % course
    return page(course, "Quiz", body, 1, "quiz", scripts=["quiz.js"], have=HAVE)

def exam_hub(course):
    meta = load_json(course + "/data/meta.json")
    mid = meta["sets"]["midterm"]; sp = meta["sets"]["sprint"]
    mlinks = " ".join('<a class="btn" href="run.html?exam=%s">Mock %s</a>' % (s["id"], s["id"][-1]) for s in mid) + ' <a class="btn alt" href="run.html?exam=midterm-random">🎲 New random midterm</a>'
    slinks = " ".join('<a class="btn" href="run.html?exam=%s">Speed %s</a>' % (s["id"], s["id"][-1]) for s in sp) + ' <a class="btn alt" href="run.html?exam=sprint-random">🎲 New random speed exam</a>'
    chk = "".join('<label><input type="checkbox" value="%s" checked> %s</label><br>' % (c["id"], esc(c["id"].upper().replace("C", "Ch. ") + " " + c["title"])) for c in meta["chapters"])
    qc = meta["midterm_quota"]
    midnote = {"Calculus-1": "Format of the Moodle mock: <b>20 random questions from chapters 1–3, 50 minutes, you cannot return to previous questions, first attempt graded.</b> (The advice sheet for the real midterm mentions 16 questions.)",
               "Linear-Algebra": "The advice sheet says the midterm is a written test or an MCQ test on Moodle depending on the tutorial lecturer. These mocks use the same style (20 questions, 50 minutes) on chapters 1–4 — <b>the covered chapters are our assumption</b>; adjust with the custom builder below."}[course]
    body = """<h1>Mock exams</h1>
<div class="panel"><h2 style="margin-top:0">📝 Midterm mock — %(mt)s</h2><p>%(note)s Question mix: %(mix)s.</p><p>%(ml)s</p></div>
<div class="panel"><h2 style="margin-top:0">⚡ Speed exam — 30 questions in 20 minutes (40 s per question)</h2><p>Questions drawn from every chapter (about equal numbers). You may jump around; the palette shows what you have answered. Use it to train speed and accuracy: skip fast, come back later.</p><p>%(sl)s</p></div>
<div class="panel"><h2 style="margin-top:0">🛠 Build your own exam</h2>
<form id="custom"><div class="row"><div>%(chk)s</div><div><label>Questions <input type="number" id="n" value="15" min="5" max="60" style="width:5em"></label><br>
<label>Minutes <input type="number" id="min" value="10" min="1" max="120" style="width:5em"></label><br><label><input type="checkbox" id="fwd"> forward only (no going back)</label><br>
<button class="btn" type="submit" style="margin-top:8px">Start</button></div></div></form></div>
<p class="muted">Results (score, time, chapter breakdown, review of every question) are saved in this browser and feed the progress panel on the home page.</p>""" % dict(
        mt=esc(meta["midterm_title"].split(" (")[0]), note=midnote, mix=", ".join("%d from %s" % (v, k.upper().replace("C", "Ch. ")) for k, v in qc.items()), ml=mlinks, sl=slinks, chk=chk)
    inline = """<script>document.getElementById('custom').addEventListener('submit',function(e){e.preventDefault();var ch=[].slice.call(document.querySelectorAll('#custom input[type=checkbox][value]:checked')).map(function(x){return x.value}).join(',');if(!ch){alert('Select at least one chapter');return}
location.href='run.html?exam=custom&ch='+ch+'&n='+document.getElementById('n').value+'&min='+document.getElementById('min').value+'&fwd='+(document.getElementById('fwd').checked?1:0)});</script>"""
    return page(course, "Mock exams", body + inline, 1, "exam", have=HAVE)

def exam_run(course):
    body = '<h1>Exam</h1><div id="runner" data-base="../data/" data-course="%s"><p class="muted">Loading…</p></div>' % course
    return page(course, "Exam", body, 1, "exam", scripts=["quiz.js"], have=HAVE)

def bank_page(course):
    meta = load_json(course + "/data/meta.json")
    body = """<h1>Practice bank</h1><p class="lead">%d questions. Each one cites its source (course document, or generated in the same style) and has a worked explanation. Tick <i>written mode</i> to hide the options and work like in the written final.</p>
<div id="bank" data-base="../data/" data-course="%s"><p class="muted">Loading…</p></div>""" % (sum(meta["counts"].values()), course)
    return page(course, "Practice bank", body, 1, "bank", scripts=["bank.js"], have=HAVE)

def sources_page(course):
    meta = load_json(course + "/data/meta.json"); bank = load_json(course + "/data/bank.json")
    cc = counts_by_ch(bank)
    inv_path = os.path.join(ROOT, "..", "text_raw", "_inventory.json")
    inv = json.load(open(inv_path, encoding="utf-8")) if os.path.exists(inv_path) else []
    prefix = {"Calculus-1": "MAT1.001", "Linear-Algebra": "MAT1.002"}[course]
    def role(path):
        p = path.lower()
        if "/lectures/" in p: return "Lecture slides: chapter outline, concept checks"
        if "tutorials/" in p or "/tutor/" in p: return "Exercise source: every auto-checkable problem is a question; the rest is kept for the written practice"
        if "additional problems" in p: return "Exercise source (training problems)"
        if "sample tests" in p: return "Past final exam: problems solved in full on the Written page"
        if "mocktest" in p: return "Mock test source"
        if "textbooks" in p: return "Reference reading (chapter map below)"
        if "final tutorial" in p or "tutor for final" in p: return "Final-exam tutoring slides (scanned, OCR read)"
        if "sharing" in p: return "Sharing-session slides (scanned, OCR read)"
        return "Reference"
    rows = ""
    for r in inv:
        if r["file"].startswith(prefix):
            rows += "<tr><td>%s</td><td>%d</td><td>%s</td></tr>" % (esc(r["file"].split(" - ", 1)[1] if " - " in r["file"] else r["file"]), r["pages"], esc(role(r["file"])))
    cov = ""
    for ch in meta["chapters"]:
        k = cc[ch["id"]]
        cov += "<tr><td><b>%s</b> %s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%s</td></tr>" % (ch["id"].upper().replace("C", "Ch. "), esc(ch["title"]), sum(k.values()), k["src"], k["gen"], k["concept"], esc(TEXTBOOKS[course][ch["id"]]))
    notes = load_json(course + "/data/notes.json") if os.path.exists(os.path.join(ROOT, course, "data", "notes.json")) else []
    nhtml = "".join("<li><b>%s</b>: %s</li>" % (esc(n["src"]), esc(n["note"]).replace("$", "$")) for n in notes) or "<li>None found.</li>"
    body = """<h1>Sources, coverage and document notes</h1>
<p class="lead">What was read, how each document was used, how many questions come from each chapter, and the errors we found in the course materials.</p>
<h2>Documents read</h2><div class="panel"><table class="t"><tr><th>Document</th><th>Pages</th><th>How it is used</th></tr>%s</table>
<p class="muted">PDFs with a text layer were converted with pdftotext; scanned PDFs were OCR'd with tesseract and the formulas were checked against the page images. Where a problem statement mixed text and a figure, only the text-complete parts became questions.</p></div>
<h2>Question coverage per chapter</h2><div class="panel" style="overflow-x:auto"><table class="t"><tr><th>Chapter</th><th>Total</th><th>From course documents</th><th>Generated (same style)</th><th>Concept checks</th><th>Textbook sections</th></tr>%s</table></div>
<h2>Errors and oddities found in the course documents</h2><div class="panel"><p>Each item below was found by checking our computed answer against the printed one (or when an exercise turned out to be impossible as printed). The quiz uses the computed result.</p><ul>%s</ul></div>
<h2>How answers were verified</h2><div class="panel"><ul><li>All answers are produced by code (sympy exact arithmetic, never typed by hand) and, for source problems, compared with the printed answer key; the build stops if they disagree.</li>
<li>Distractors are realistic mistakes (sign errors, missing chain-rule factor, transposed matrices, wrong-order composition…), and every distractor is checked to be different from the correct answer.</li>
<li>Option positions are shuffled with a fixed seed and balanced (A/B/C/D each 25%%); the correct option is not systematically the longest.</li></ul></div>""" % (rows, cov, nhtml)
    return page(course, "Sources", body, 1, "sources", have=HAVE)

def lab_page(course):
    if course == "Linear-Algebra":
        intro = """<h1>Linear Algebra lab</h1><p class="lead">Exact arithmetic (fractions, no rounding) with every step shown. Each tool solves the same problem by <b>several methods</b> — Gauss and Gauss–Jordan elimination, Cramer's rule, the inverse matrix, LU factorisation, Jacobi and Gauss–Seidel iteration; row reduction, cofactor expansion and Sarrus for determinants; Gauss–Jordan and adjugate for inverses — and checks that they agree.
There is also a scanner for systems with a parameter <i>k</i> (like question 1(b) and 2(a) of the finals), eigen-tools, orthogonal tools, matrices relative to bases and a Jacobian-matrix tool (an extension beyond MAT1.002: the Jacobian is the matrix of the linear map that best approximates a function near a point).</p>
<p class="muted">Enter matrices with one row per line and entries separated by spaces (fractions like 3/4 are fine). The lab is a checking aid: in the exam there is no calculator, so always practise the hand computation first.</p><div id="lab" class="lab"></div>"""
        scripts = ["vendor/mathjs/math.min.js", "la.js", "la-lab.js"]
    else:
        intro = """<h1>Calculus lab</h1><p class="lead">Numerical and graphical tools to check your hand work: plot a function with its derivative and tangent line, explore limits, run Newton's method and bisection, compare Riemann sums with the trapezoid and Simpson rules, watch partial sums of a series, build Taylor polynomials with the error bound, test an antiderivative by differentiating it, and get the critical points and inflection points of a curve.</p>
<p class="muted">Write functions like in a calculator: <code>x^3 - 3*x</code>, <code>sin(x)/x</code>, <code>exp(-x^2)</code>, <code>sqrt(x)</code>, <code>log(x)</code> (natural log), <code>pi</code>. Numerical output is evidence, not proof: the exam asks for exact answers and justification.</p><div id="lab" class="lab"></div>"""
        scripts = ["vendor/mathjs/math.min.js", "calc-lab.js"]
    return page(course, "Labs", intro, 1, "lab", scripts=scripts, have=HAVE)

# ------------------------------------------------------------------------------------------ root landing page
def root_index():
    html_ = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>USTH B1 — Maths self-study</title>
<link rel="stylesheet" href="shared/core.css"></head><body><header class="top"><div class="wrap"><a class="brand" href="index.html"><img src="shared/img/usth_logo.png" alt="USTH"><span>USTH B1 · Maths self-study</span></a></div></header>
<main class="wrap"><h1>USTH B1 Mathematics: self-study and exam-training sites</h1>
<p class="lead">Unofficial study systems built from the course documents: quizzes per chapter, mock midterms, a 30-questions-in-20-minutes speed exam, a verified practice bank and interactive tools.</p>
<div class="cards"><a class="card" href="Calculus-1/index.html"><b>Calculus I · MAT1.001</b><span>Limits, derivatives, integrals, sequences and series. 6 chapters, 386 questions.</span></a>
<a class="card" href="Linear-Algebra/index.html"><b>Linear Algebra · MAT1.002</b><span>Systems, matrices, determinants, vector spaces, inner products, linear maps, eigenvalues. 7 chapters, 398 questions.</span></a></div>
<p class="muted">The Vietnamese versions will be added as separate sites. Everything runs in your browser; progress stays on your device.</p></main></body></html>"""
    write("index.html", html_)

def main():
    for course in COURSES:
        write(course + "/index.html", home(course))
        write(course + "/quiz/index.html", quiz_hub(course)); write(course + "/quiz/run.html", quiz_run(course))
        write(course + "/exam/index.html", exam_hub(course)); write(course + "/exam/run.html", exam_run(course))
        write(course + "/bank/index.html", bank_page(course))
        write(course + "/sources/index.html", sources_page(course))
        write(course + "/lab/index.html", lab_page(course))
    root_index()
    print("pages written")

if __name__ == "__main__":
    main()
