# -*- coding: utf-8 -*-
"""Build the JSON data of the two Physics courses: question banks, quiz sets (3 per chapter), midterm mocks, final mocks,
speed exams (30 questions / 20 minutes), written papers and source notes.   Run after (or before) build_data.py - the files are independent."""
import json, os, sys
from collections import Counter
import qlib
from build_data import build_course, write_course, sanitize_papers

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PH1_CHAPTERS = [
    ("c1", "Kinematics", "Mechanics tutorial Parts 1–2 · Lecture 1 · Halliday ch. 2 and 4"),
    ("c2", "Dynamics: Newton's laws", "Mechanics tutorial Part 3 · Lectures 2–3 · Halliday ch. 5–6"),
    ("c3", "Work, energy and momentum", "Mechanics tutorial Part 4 · Lecture 4 · Halliday ch. 7–9"),
    ("c4", "Circular motion and rotation", "Mechanics tutorial Part 5 · Lecture 5 · Halliday ch. 4, 6 and 10"),
    ("c5", "Temperature, heat and the first law", "Thermodynamics tutorial Part I · Thermodynamics Part I · Halliday ch. 18"),
    ("c6", "Kinetic theory of gases", "Thermodynamics tutorial Part II · Thermodynamics Part II · Halliday ch. 19"),
    ("c7", "Entropy and the second law", "Thermodynamics tutorial Part III · Thermodynamics Part III · Halliday ch. 20"),
]
PH2_CHAPTERS = [
    ("c1", "Coulomb's law", "Lecture Electricity C1 · Homework session 1 · Halliday ch. 21"),
    ("c2", "Electric fields", "Lecture Electricity C2 · Homework sessions 1–2 · Halliday ch. 22"),
    ("c3", "Gauss' law", "Electrostatics lecture ch. 3 · Homework session 2 · Halliday ch. 23"),
    ("c4", "Electric potential", "Electrostatics lecture ch. 4 · Homework session 3 · Halliday ch. 24"),
    ("c5", "Magnetic force", "Magnetism lecture ch. 5 · Halliday ch. 28"),
    ("c6", "Magnetic fields of currents", "Magnetism lecture ch. 6 · Halliday ch. 29"),
    ("c7", "Induction and inductance", "Magnetism lecture ch. 7 · Halliday ch. 30"),
    ("c8", "Nature and propagation of light", "Optics lecture · Tutorial chapter 33 · Young and Freedman ch. 33"),
    ("c9", "Geometric optics", "Optics lecture · Tutorial chapter 34 · Young and Freedman ch. 34"),
    ("c10", "Interference", "Optics lecture · Tutorial chapter 35 · Young and Freedman ch. 35"),
    ("c11", "Diffraction", "Optics lecture · Tutorial chapter 36 · Young and Freedman ch. 36"),
]

CALC_NOTE = "A calculator is allowed and needed for the numerical questions: give answers to the precision shown in the options (about 3 significant figures)."

def course_notes(prefixes):
    return [dict(src=a, note=b) for a, b in qlib.NOTES if a.startswith(prefixes)]

def main():
    qlib.NOTES.clear()
    import gen_ph1
    B1 = gen_ph1.build(); r1 = B1.finalize()
    print("PH1", r1)
    q1 = {"c1": 5, "c2": 5, "c3": 6, "c4": 4}
    s1 = {"c1": 4, "c2": 4, "c3": 4, "c4": 4, "c5": 4, "c6": 5, "c7": 5}
    f1 = {"c1": 3, "c2": 4, "c3": 5, "c4": 3, "c5": 8, "c6": 10, "c7": 7}
    t1 = "Fundamental Physics I Midterm (Mechanics, 20 questions, 40 min)"
    ft1 = "Fundamental Physics I Final (40 questions, 80 min)"
    sets1 = build_course("Physics-1", B1, PH1_CHAPTERS, q1, t1, 31, mid_min=40, sprint_quota=s1, final_quota=f1, final_title="Fundamental Physics I Final", final_min=80)
    meta1 = dict(midterm_quota=q1, midterm_minutes=40, midterm_title=t1, sprint_quota=s1, final_quota=f1, final_minutes=80, final_title=ft1, calc_note=CALC_NOTE)
    try:
        from ph1_papers import build_papers as ph1_papers
        pap1 = sanitize_papers(ph1_papers())
    except ImportError:
        pap1 = []
    n1 = write_course("Physics-1", B1, {"papers.json": pap1, "notes.json": course_notes(("Mechanics", "Thermodynamics", "Lecture", "Final tutorial"))}, PH1_CHAPTERS, sets1, meta1)
    print("written", n1, "Physics I questions;", len(pap1), "papers")

    try:
        import gen_ph2
    except ImportError:
        gen_ph2 = None
    if gen_ph2:
        B2 = gen_ph2.build(); r2 = B2.finalize()
        print("PH2", r2)
        q2 = {"c1": 4, "c2": 5, "c3": 4, "c4": 4, "c5": 3}
        s2 = {"c1": 2, "c2": 3, "c3": 3, "c4": 3, "c5": 3, "c6": 3, "c7": 3, "c8": 3, "c9": 3, "c10": 2, "c11": 2}
        f2 = {"c1": 2, "c2": 3, "c3": 3, "c4": 3, "c5": 4, "c6": 5, "c7": 5, "c8": 3, "c9": 5, "c10": 4, "c11": 3}
        t2 = "Fundamental Physics II Midterm (Electricity and Magnetism, 20 questions, 40 min)"
        ft2 = "Fundamental Physics II Final (40 questions, 80 min)"
        sets2 = build_course("Physics-2", B2, PH2_CHAPTERS, q2, t2, 32, mid_min=40, sprint_quota=s2, final_quota=f2, final_title="Fundamental Physics II Final", final_min=80)
        meta2 = dict(midterm_quota=q2, midterm_minutes=40, midterm_title=t2, sprint_quota=s2, final_quota=f2, final_minutes=80, final_title=ft2, calc_note=CALC_NOTE)
        try:
            from ph2_papers import build_papers as ph2_papers
            pap2 = sanitize_papers(ph2_papers())
        except ImportError:
            pap2 = []
        n2 = write_course("Physics-2", B2, {"papers.json": pap2, "notes.json": course_notes(("Homework", "Tutorial chapter", "Lecture", "Final tutorial", "Electrostatics", "Magnetism", "Optics"))}, PH2_CHAPTERS, sets2, meta2)
        print("written", n2, "Physics II questions;", len(pap2), "papers")
    for slug, sets in (("Physics-1", sets1),) + ((("Physics-2", sets2),) if gen_ph2 else ()):
        print(slug, "chapter sets:", sum(len(v) for v in sets["chapter"].values()), "midterm:", [len(s["ids"]) for s in sets["midterm"]], "sprint:", [len(s["ids"]) for s in sets["sprint"]], "final:", [len(s["ids"]) for s in sets["final"]])

if __name__ == "__main__":
    main()
