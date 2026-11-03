# -*- coding: utf-8 -*-
"""Physics II (PHY1.002): 11 modules, one per chapter; the slides are generated from the concept catalogue (build/concepts/ph2.py)."""
from phys_modules import make
from concepts import ph2

CHAPTERS = [("c1", "Coulomb's law"), ("c2", "Electric fields"), ("c3", "Gauss' law"), ("c4", "Electric potential"), ("c5", "Magnetic force"), ("c6", "Magnetic fields of currents"),
            ("c7", "Induction and inductance"), ("c8", "Nature and propagation of light"), ("c9", "Geometric optics"), ("c10", "Interference"), ("c11", "Diffraction")]
WHERE = {"c1": ("Lecture Electricity C1", "Homework session 1"), "c2": ("Lecture Electricity C2", "Homework sessions 1–2"), "c3": ("Electrostatics lecture ch. 3", "Homework session 2"),
         "c4": ("Electrostatics lecture ch. 4", "Homework session 3"), "c5": ("Magnetism lecture ch. 5", "Halliday ch. 28 problems"), "c6": ("Magnetism lecture ch. 6", "Halliday ch. 29 problems"),
         "c7": ("Magnetism lecture ch. 7", "Halliday ch. 30 problems"), "c8": ("Optics lecture", "Tutorial chapter 33"), "c9": ("Optics lecture", "Tutorial chapter 34"),
         "c10": ("Optics lecture", "Tutorial chapter 35"), "c11": ("Optics lecture", "Tutorial chapter 36")}
MODULES = make(ph2.CONCEPTS, CHAPTERS, WHERE)
