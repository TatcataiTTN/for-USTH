# -*- coding: utf-8 -*-
"""Physics I (PHY1.001): 7 modules, one per chapter; the slides are generated from the concept catalogue (build/concepts/ph1.py)."""
from phys_modules import make
from concepts import ph1

CHAPTERS = [("c1", "Kinematics"), ("c2", "Dynamics: Newton's laws"), ("c3", "Work, energy and momentum"), ("c4", "Circular motion and rotation"),
            ("c5", "Temperature, heat and the first law"), ("c6", "Kinetic theory of gases"), ("c7", "Entropy and the second law")]
WHERE = {"c1": ("Lecture 1 · Kinematics", "Mechanics tutorial Parts 1–2"), "c2": ("Lectures 2–3 · Dynamics", "Mechanics tutorial Part 3"),
         "c3": ("Lecture 4 · Work, energy, momentum", "Mechanics tutorial Part 4"), "c4": ("Lecture 5 · Circular motion and rigid bodies", "Mechanics tutorial Part 5"),
         "c5": ("Thermodynamics Part I", "Thermodynamics tutorial Part I"), "c6": ("Thermodynamics Part II", "Thermodynamics tutorial Part II"), "c7": ("Thermodynamics Part III", "Thermodynamics tutorial Part III")}
MODULES = make(ph1.CONCEPTS, CHAPTERS, WHERE)
