# -*- coding: utf-8 -*-
"""Page templates shared by both courses (English site; the Vietnamese site reuses them with a different string table)."""
import html, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
esc = lambda s: html.escape(str(s), quote=True)

MATH_VERIFY = "Every numerical answer is computed by program (sympy / exact rational arithmetic) and, where the course gives an answer key, compared with it; differences are listed on the"
PHYS_VERIFY = "Every numerical answer is computed by program from the physical law and re-derived by a second, independent route (another formula, energy instead of kinematics, numerical integration or simulation, ray-transfer matrices); differences from the printed answers of the course sheets are listed on the"

COURSES = {
    "Calculus-1": dict(slug="Calculus-1", code="MAT1.001", name="Calculus I", credits=4, verify=MATH_VERIFY,
                       tagline="Single-variable calculus: limits, derivatives, integrals, sequences and series.",
                       sources=[("Lectures #1–#12", "Calculus I 24-25 lecture slides (printed versions)"), ("Tutorials #1–#12", "Calculus I 24-25 tutorial sheets"),
                                ("Computation problems #1–#12", "additional training problems"), ("Mock Test 1", "Mocktest for Final Calculus I, 2025–26"),
                                ("Textbooks", "Thomas' Calculus (recommended) and Stewart's Calculus")]),
    "Linear-Algebra": dict(slug="Linear-Algebra", code="MAT1.002", name="Linear Algebra", credits=4, verify=MATH_VERIFY,
                           tagline="Systems, matrices, determinants, vector spaces, inner products, linear maps, eigenvalues.",
                           sources=[("Lectures 1–7", "MAT1.002 lecture slides"), ("Exercise Sheets 1–7", "tutorial sheets (A4, B5, B6 – LA – BI15)"),
                                    ("Final exams 2018–2025", "eight past papers (D,E,G / A,B,C,AE 2018–19, 2019–20, 2022–23, 2023–24 ×2, 2024–25 ×2)"),
                                    ("Textbooks", "Elementary Linear Algebra, 8th ed. (main book) and Strang, Introduction to Linear Algebra, 4th ed. (for review)")]),
    "Physics-1": dict(slug="Physics-1", code="PHY1.001", name="Fundamental Physics I", credits=4, verify=PHYS_VERIFY,
                      tagline="Mechanics and thermodynamics: kinematics, Newton's laws, work, energy and momentum, circular motion, heat, kinetic theory, entropy.",
                      sources=[("Lectures", "Mechanics lectures 1–5 (AY 2024–25 and 2026–27) and Thermodynamics parts I–III"), ("Tutorials", "Mechanics tutorial Parts 1–5 and Thermodynamics tutorial Parts I, II (1), II (2), III"),
                               ("Tutoring slides", "Midterm and final tutorials by the Learning Support team (scanned slides, OCR read)"), ("Textbooks", "Halliday, Resnick and Walker, Fundamentals of Physics (main book) and Young and Freedman, University Physics")]),
    "Physics-2": dict(slug="Physics-2", code="PHY1.002", name="Fundamental Physics II", credits=4, verify=PHYS_VERIFY,
                      tagline="Electricity, magnetism and optics: Coulomb's law, fields, Gauss' law, potential, magnetic force and fields, induction, light, lenses, interference, diffraction.",
                      sources=[("Lectures", "Electricity, Magnetism and Optics lecture slides (AY 2024–25 and 2025–26)"), ("Tutorials", "Homework sessions 1–3 (Halliday problems) and tutorial chapters 33–36 (Young and Freedman problems)"),
                               ("Tutoring slides", "Midterm and final tutorials and formula sheets by the Learning Support team (scanned slides, OCR read)"), ("Textbooks", "Halliday, Resnick and Walker, Fundamentals of Physics and Young and Freedman, University Physics with Modern Physics")]),
}

def nav_items(c):
    return [("Home", "index.html", "home"), ("Lectures", "lectures/index.html", "lectures"), ("Modules", "modules/index.html", "modules"), ("Chapter quizzes", "quiz/index.html", "quiz"), ("Exams", "exam/index.html", "exam"),
            ("Practice bank", "bank/index.html", "bank"), ("Written", "written/index.html", "written"), ("Labs", "lab/index.html", "lab"), ("Sources", "sources/index.html", "sources")]

def head_scripts(r, scripts):
    base = ['vendor/katex/katex.min.js', 'vendor/katex/auto-render.min.js', 'core.js']
    return "".join('<script src="%sshared/%s"></script>' % (r, s) for s in base + list(scripts))

def page(course, title, body, depth, active="", scripts=(), css=(), desc="", lang="en", extra_head="", have=None):
    """depth = directory depth of the page below the course root (0 for Calculus-1/index.html)."""
    c = COURSES[course]
    r = "../" * (depth + 1)           # to the repository root (where shared/ lives)
    up = "../" * depth                # to the course root
    items = [(l, p, k) for l, p, k in nav_items(c) if (have is None or k in have or k == "home")]
    nav = "".join('<a href="%s%s"%s>%s</a>' % (up, p, ' class="on"' if k == active else "", l) for l, p, k in items)
    links = "".join('<link rel="stylesheet" href="%sshared/%s">' % (r, s) for s in ["vendor/katex/katex.min.css", "core.css"] + list(css))
    src_html = "".join("<li><b>%s</b> — %s</li>" % (esc(a), esc(b)) for a, b in c["sources"])
    return """<!doctype html>
<html lang="%(lang)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s · %(name)s %(code)s · USTH</title><meta name="description" content="%(desc)s">
<link rel="icon" type="image/png" href="%(r)sshared/img/favicon.png"><link rel="apple-touch-icon" href="%(r)sshared/img/apple-touch-icon.png">
<script>(function(){try{var t=JSON.parse(localStorage.getItem('ustm:theme')||'null');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);var f=JSON.parse(localStorage.getItem('ustm:font')||'null');if(f)document.documentElement.style.fontSize=f}catch(e){}})();</script>
%(links)s%(extra)s<script src="%(r)sshared/gate.js"></script></head><body>
<header class="top"><div class="wrap"><a class="brand" href="%(up)sindex.html"><img src="%(r)sshared/img/usth_logo.png" alt="USTH"><span>%(name)s · %(code)s</span></a>
<nav>%(nav)s<a href="%(r)sindex.html">All courses</a>
<details class="menu"><summary>🎨 Display</summary><div class="pop"><button data-set-theme="auto">Auto</button><button data-set-theme="light">Light</button><button data-set-theme="dark">Dark</button><button data-set-font="14px">Small text</button><button data-set-font="16px">Normal text</button><button data-set-font="19px">Large text</button><button data-logout>Sign out</button></div></details></nav></div></header>
<main class="wrap">%(body)s</main>
<footer class="foot"><div class="wrap"><div class="footlogos"><span class="chip"><img src="%(r)sshared/img/usth_logo.png" alt="USTH – University of Science and Technology of Hanoi"><img src="%(r)sshared/img/usth_dses_logo.png" alt="DSES"></span><span>University of Science and Technology of Hanoi · B1 · %(name)s (%(code)s)</span></div><p><b>Unofficial self-study material</b> prepared from the USTH %(name)s course documents (not endorsed by USTH). Problem statements are paraphrased with their source cited on every question; solutions, explanations and checks are our own. %(verify)s <a href="%(up)ssources/index.html">Sources</a> page. Progress is stored only in your browser.</p>
<details><summary>Source documents used</summary><ul class="sources">%(src)s</ul></details></div></footer>
%(scripts)s</body></html>""" % dict(lang=lang, title=esc(title), name=c["name"], code=c["code"], desc=esc(desc or c["tagline"]), links=links, extra=extra_head, up=up, r=r, nav=nav, body=body,
                                     src=src_html, scripts=head_scripts(r, scripts), verify=c['verify'])

def write(relpath, content):
    p = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def load_json(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)
