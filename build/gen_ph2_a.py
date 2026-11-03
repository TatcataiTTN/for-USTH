# -*- coding: utf-8 -*-
"""Physics II (PHY1.002) - Electricity: chapter 1 Coulomb's law, 2 Electric fields, 3 Gauss' law, 4 Electric potential.
Sources: homework sessions 1-3 (Halliday problems), Electricity lectures C1-C2, electrostatics lecture (2025-26), midterm tutoring slides."""
import math
import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize_scalar
from phys_common import *
from phys_verify import integrate
import figs

H1 = "Homework session 1"
H2 = "Homework session 2"
H3 = "Homework session 3"
GEN = lambda s: "Generated, same style as: " + s
k = K_E
UC = 1e-6      # microcoulomb
NC = 1e-9

def force_vec(q1, p1, q2, p2):
    """Coulomb force on charge 1 (at p1) due to charge 2 (at p2) as a numpy vector."""
    d = np.array(p1, float) - np.array(p2, float)
    r = np.linalg.norm(d)
    return k * q1 * q2 / r ** 3 * d

def field_vec(qs, ps, p):
    """Net electric field at point p of point charges qs at positions ps."""
    E = np.zeros(2)
    for q, pos in zip(qs, ps):
        d = np.array(p, float) - np.array(pos, float)
        E += k * q / np.linalg.norm(d) ** 3 * d
    return E

# =============================================================================================== chapter 1
def ch1(B):
    c = "c1"
    # ---------------------------------------------------------------- Homework 1, problem 1: two identical conducting spheres
    F1, F2, r = 0.108, 0.0360, 0.500
    prod = -F1 * r ** 2 / k                                   # q1 q2 (attraction: opposite signs)
    s = 2 * math.sqrt(F2 * r ** 2 / k)                        # q1 + q2 (each sphere keeps half after contact), the net charge is positive
    qa, qb = sorted(np.roots([1, -s, prod]).real)             # roots of x^2 - s x + prod = 0
    x = sp.symbols("x"); sols = sorted(float(v) for v in sp.solve(x ** 2 - sp.Float(s) * x + sp.Float(prod), x))
    check(qa, sols[0]); check(qb, sols[1])
    mcq_num(B, c, "Coulomb's law", 3, "Two identical conducting spheres, fixed in place, attract each other with a force of $0.108\\,\\mathrm{N}$ when their centres are $50.0\\,\\mathrm{cm}$ apart. They are then joined by a thin wire and the wire is removed; now they repel each other with a force of $0.0360\\,\\mathrm{N}$. The initial net charge is positive. What was the negative charge on one of the spheres?",
            qa, [-qb, qa / 2, -qa, -s, qb], "C", ex("Before: $q_1q_2=-\\dfrac{Fr^2}{k}=-3.00\\times10^{-12}\\,\\mathrm{C^2}$ (opposite signs).", "After touching, identical spheres share the net charge equally: $\\left(\\dfrac{q_1+q_2}{2}\\right)^2=\\dfrac{F'r^2}{k}\\Rightarrow q_1+q_2=2.00\\times10^{-6}\\,\\mathrm{C}$ (positive).", "So $q_1,q_2$ are the roots of $x^2-2.00\\times10^{-6}x-3.00\\times10^{-12}=0$: $x=+3.00\\times10^{-6}$ and $-1.00\\times10^{-6}\\,\\mathrm{C}$."), H1 + ", Q1(a)", sig=3)
    mcq_num(B, c, "Coulomb's law", 3, "For the two identical conducting spheres of the previous problem (attraction $0.108\\,\\mathrm{N}$ at $50.0\\,\\mathrm{cm}$; after contact repulsion $0.0360\\,\\mathrm{N}$; positive net charge), what was the POSITIVE charge on the other sphere?", qb, [-qa, s, -qb, qb / 2, 4.0e-6], "C", ex("The two initial charges are the roots of $x^2-(q_1+q_2)x+q_1q_2=0$ with $q_1+q_2=2.00\\times10^{-6}$ and $q_1q_2=-3.00\\times10^{-12}$: $+3.00\\times10^{-6}\\,\\mathrm{C}$ and $-1.00\\times10^{-6}\\,\\mathrm{C}$."), H1 + ", Q1(b)", sig=3)
    # ---------------------------------------------------------------- problem 2: four particles at the corners of a square
    a = 1.0
    qq = sp.symbols("Q")
    ex_ = sp.solve(-1.0 * qq - qq ** 2 / (2 * sp.sqrt(2)), qq)             # x-balance on particle 1 for q = 1: -Q q - Q^2/(2 sqrt 2) = 0
    check(float([v for v in ex_ if abs(v) > 1e-9][0]), -2 * math.sqrt(2))
    mcq_num(B, c, "Coulomb's law", 3, "Four particles sit at the corners of a square. Particles 1 and 4 (on one diagonal) have charge $Q$; particles 2 and 3 (on the other diagonal) have charge $q$. What is $Q/q$ if the net electrostatic force on particles 1 and 4 is zero?", -2 * math.sqrt(2), [2 * math.sqrt(2), -math.sqrt(2), -1 / (2 * math.sqrt(2)), -2.0], "", ex("Force on particle 1 from its two neighbours (charge $q$, distance $a$) points along the sides: each has magnitude $\\dfrac{kQq}{a^2}$, resultant $\\sqrt2\\,\\dfrac{kQq}{a^2}$ along the diagonal.", "The opposite corner (charge $Q$, distance $a\\sqrt2$) pushes along the diagonal with $\\dfrac{kQ^2}{2a^2}$. Balance: $\\sqrt2\\,Qq=-\\dfrac{Q^2}{2}$, so $\\dfrac Qq=-2\\sqrt2=-2.83$."), H1 + ", Q2(a)", sig=3)
    mcq_pick(B, c, "Coulomb's law", 3, "In the same square (charges $Q$ on one diagonal, $q$ on the other), is there any value of $q$ (for fixed $Q$) that makes the net electrostatic force zero on ALL four particles?",
             ["No: balance on particles 1, 4 needs $Q/q=-2\\sqrt2$ but on 2, 3 it needs $Q/q=-1/(2\\sqrt2)$", "Yes: $q=-Q$", "Yes: $q=Q/\\sqrt2$", "Yes, any $q$ with opposite sign to $Q$"], 0,
             ex("For particles 2 and 3 the roles are exchanged: zero force needs $q/Q=-2\\sqrt2$, i.e. $Q/q=-1/(2\\sqrt2)=-0.354$. The two conditions $-2.83$ and $-0.354$ contradict each other, so no value of $q$ works."), H1 + ", Q2(b)", "src")
    # ---------------------------------------------------------------- problem 3: two particles in the xy plane, find the third
    q1, p1, q2, p2, q3 = 3.0 * UC, (0.035, 0.005), -4.0 * UC, (-0.020, 0.015), 4.0 * UC
    F12 = force_vec(q2, p2, q1, p1); Fm = np.linalg.norm(F12); ang = math.degrees(math.atan2(F12[1], F12[0]))
    check(Fm, k * abs(q1 * q2) / math.hypot(0.055, 0.010) ** 2)
    u = (np.array(p2) - np.array(p1)) / np.linalg.norm(np.array(p2) - np.array(p1))      # unit vector from particle 1 to particle 2
    r3 = math.sqrt(k * abs(q2 * q3) / Fm); p3 = np.array(p2) + r3 * u
    F32 = force_vec(q2, p2, q3, tuple(p3))
    check(float(np.linalg.norm(F12 + F32)) / Fm + 1.0, 1.0, 1e-9, "net force on particle 2 vanishes")
    mcq_num(B, c, "Coulomb's law", 2, "Particle 1 ($q_1=3.0\\,\\mu\\mathrm{C}$) is at $(3.5\\,\\mathrm{cm},\\,0.50\\,\\mathrm{cm})$ and particle 2 ($q_2=-4.0\\,\\mu\\mathrm{C}$) at $(-2.0\\,\\mathrm{cm},\\,1.5\\,\\mathrm{cm})$. What is the magnitude of the electrostatic force on particle 2 due to particle 1?", Fm, [Fm / 10, Fm * 10, k * abs(q1 * q2) / 0.055 ** 2, Fm / math.sqrt(2)], "N", ex("Separation: $r=\\sqrt{(5.5)^2+(1.0)^2}\\,\\mathrm{cm}=5.59\\,\\mathrm{cm}$.", "$F=\\dfrac{k|q_1q_2|}{r^2}=\\dfrac{(8.99\\times10^9)(3.0\\times10^{-6})(4.0\\times10^{-6})}{(0.0559)^2}=34.5\\,\\mathrm{N}$ (attractive)."), H1 + ", Q3(a)", sig=3)
    mcq_num(B, c, "Coulomb's law", 2, "For the same two charges (particle 2 is attracted by particle 1), what is the direction of the force on particle 2, as an angle from the $+x$ axis?", ang, [-ang, 180.0 + ang, 90.0 - ang, ang / 2], "deg", ex("The force on particle 2 points TOWARDS particle 1 (opposite charges attract): direction $(+5.5,\\,-1.0)\\,\\mathrm{cm}$.", "Angle $=\\arctan\\dfrac{-1.0}{5.5}=-10.3^\\circ$, i.e. $10.3^\\circ$ below the $+x$ axis."), H1 + ", Q3(b)", sig=3)
    mcq_text(B, c, "Coulomb's law", 3, "A third particle with $q_3=+4.0\\,\\mu\\mathrm{C}$ is to be placed so that the net force on particle 2 vanishes. Its coordinates (in cm) are",
             "$(-8.4,\\ 2.7)$", ["$(8.4,\\ -2.7)$", "$(-8.4,\\ -2.7)$", "$(0.75,\\ 1.0)$"],
             ex("Particle 3 must pull particle 2 with the same $34.5\\,\\mathrm{N}$ in the OPPOSITE direction, so it lies on the line through 1 and 2, beyond 2 (away from 1).", "Distance: $\\dfrac{k|q_2q_3|}{r_3^2}=34.5\\Rightarrow r_3=6.46\\,\\mathrm{cm}$ along the unit vector $(-5.5,\\,1.0)/5.59$.", "Position $=(-2.0,\\,1.5)+6.46(-0.984,\\,0.179)=(-8.35,\\,2.66)\\,\\mathrm{cm}$."), H1 + ", Q3(c, d)", "src")
    # ---------------------------------------------------------------- problem 4: equilibrium of three charges on a line
    L = 0.0900
    xe = brentq(lambda x: 1 / x ** 2 - 4 / (L - x) ** 2, 1e-4, L - 1e-4)
    check(xe, L / 3)
    mcq_num(B, c, "Coulomb's law", 3, "Particle 1 (charge $q$) and particle 2 (charge $4.00q$) are held $9.00\\,\\mathrm{cm}$ apart on the $x$ axis. Where on the axis (distance from particle 1, in cm) must a third particle be placed so that it feels no net force?", xe * 100, [L * 100 / 2, L * 100 * 2 / 3, L * 100 / 5, L * 100 / 4], "cm", ex("Between the two charges the forces on a test charge balance when $\\dfrac{q}{x^2}=\\dfrac{4q}{(L-x)^2}\\Rightarrow L-x=2x$.", "$x=\\dfrac L3=3.00\\,\\mathrm{cm}$ from particle 1 (closer to the smaller charge)."), H1 + ", Q4(a, b)", sig=3)
    mcq_num(B, c, "Coulomb's law", 3, "A third particle placed at $L/3$ from particle 1 (charge $q$; particle 2 has charge $4q$, $L=9.00\\,\\mathrm{cm}$ apart) must be such that ALL THREE particles stay in place when released. What is $q_3/q$?", -4 / 9, [4 / 9, -1 / 9, -4.0, -2 / 3], "", ex("Particle 1 is pushed away from particle 2 by $\\dfrac{k(q)(4q)}{L^2}$, so particle 3 must pull it back: $\\dfrac{k\\,q|q_3|}{(L/3)^2}=\\dfrac{4kq^2}{L^2}\\Rightarrow|q_3|=\\dfrac{4q}{9}$.", "$q_3$ must be negative (attractive for particle 1): $q_3/q=-\\dfrac49=-0.444$."), H1 + ", Q4(c)", sig=3)
    # ---------------------------------------------------------------- problems 6, 7
    r_ = 2.82e-10; Fn = k * E_CH ** 2 / r_ ** 2
    mcq_num(B, c, "Coulomb's law", 1, "What is the magnitude of the electrostatic force between a singly charged sodium ion (charge $+e$) and an adjacent singly charged chlorine ion ($-e$) in a salt crystal if their separation is $2.82\\times10^{-10}\\,\\mathrm{m}$?", Fn, [Fn * 2, Fn / 2, Fn * 4, Fn / 4], "N", ex("$F=\\dfrac{ke^2}{r^2}=\\dfrac{(8.99\\times10^9)(1.602\\times10^{-19})^2}{(2.82\\times10^{-10})^2}=2.90\\times10^{-9}\\,\\mathrm{N}$ (attractive)."), H1 + ", Q6", sig=3)
    ratio = k * E_CH ** 2 / (G_NEWTON * M_E ** 2)
    check(ratio, (E_CH / M_E) ** 2 * k / G_NEWTON)
    mcq_num(B, c, "Coulomb's law", 2, "An electron and a positron have charges $-e$ and $+e$ and equal masses $9.11\\times10^{-31}\\,\\mathrm{kg}$. What is the ratio of the electrical force to the gravitational force between them?", ratio, [ratio / 100, ratio * 100, ratio / 1000, ratio * 10], "", ex("Both forces fall off as $1/r^2$, so the distance cancels: $\\dfrac{F_e}{F_g}=\\dfrac{ke^2}{Gm^2}=\\dfrac{(8.99\\times10^9)(1.602\\times10^{-19})^2}{(6.674\\times10^{-11})(9.11\\times10^{-31})^2}=4.17\\times10^{42}$.", "Gravity is utterly negligible between elementary particles."), H1 + ", Q7", sig=3)
    # ---------------------------------------------------------------- generated: forces of point charges
    for q1_, q2_, r_ in [(2.0, 5.0, 0.30), (-3.0, 3.0, 0.15), (1.5, -6.0, 0.80)]:
        F = k * abs(q1_ * q2_) * UC ** 2 / r_ ** 2
        mcq_num(B, c, "Coulomb's law", 1, "Two point charges of %s μC and %s μC are %s m apart in vacuum. What is the magnitude of the force between them?" % (sci(q1_), sci(q2_), sci(r_)), F, [F * r_, F * 100, k * abs(q1_ * q2_) * UC ** 2 / r_, k * abs(q1_ * q2_) * UC / r_ ** 2], "N", ex("$F=\\dfrac{k|q_1q_2|}{r^2}=\\dfrac{(8.99\\times10^9)(%s\\times10^{-6})(%s\\times10^{-6})}{%s^2}=%s\\,\\mathrm{N}$." % (sci(abs(q1_)), sci(abs(q2_)), sci(r_), sci(F))), GEN(H1 + ", Q6"), "gen", sig=3)
    mcq_pick(B, c, "Coulomb's law", 1, "The distance between two point charges is tripled. The electrostatic force between them becomes", ["$1/9$ of its value", "$1/3$ of its value", "$3$ times its value", "$9$ times its value"], 0, ex("$F\\propto1/r^2$: $r\\to3r$ gives $F\\to F/9$."), "Lecture Electricity C1 (Coulomb's law)", "concept")
    mcq_pick(B, c, "Coulomb's law", 2, "One of two point charges is doubled and the distance between them is also doubled. The force between them becomes", ["$1/2$ of its value", "$2$ times its value", "$1/4$ of its value", "unchanged"], 0, ex("$F\\propto\\dfrac{q_1q_2}{r^2}\\to\\dfrac{2}{4}F=\\dfrac F2$."), "Lecture Electricity C1 (Coulomb's law)", "concept")
    # three collinear charges, net force on the middle one
    qs = [3.0 * UC, -2.0 * UC, 4.0 * UC]; xs = [0.0, 0.10, 0.25]
    fa = k * abs(qs[0] * qs[1]) / 0.10 ** 2; fb = k * abs(qs[1] * qs[2]) / 0.15 ** 2
    Fx = fb - fa                                              # +x: toward charge 3
    chk = sum(force_vec(qs[1], (xs[1], 0), q_, (x_, 0))[0] for q_, x_ in ((qs[0], xs[0]), (qs[2], xs[2])))
    check(Fx, chk)
    mcq_num(B, c, "Superposition of forces", 2, "Three point charges lie on the $x$ axis: $+3.0\\,\\mu\\mathrm{C}$ at $x=0$, $-2.0\\,\\mu\\mathrm{C}$ at $x=0.10\\,\\mathrm{m}$ and $+4.0\\,\\mu\\mathrm{C}$ at $x=0.25\\,\\mathrm{m}$. What is the net force on the $-2.0\\,\\mu\\mathrm{C}$ charge (positive = towards $+x$)?", Fx, [-Fx, fa + fb, fa, fb], "N", ex("From the $+3.0\\,\\mu\\mathrm{C}$ charge (attraction, towards $-x$): $F=\\dfrac{k(3.0)(2.0)\\times10^{-12}}{0.10^2}=5.39\\,\\mathrm{N}$.", "From the $+4.0\\,\\mu\\mathrm{C}$ charge (attraction, towards $+x$, $r=0.15\\,\\mathrm{m}$): $\\dfrac{k(4.0)(2.0)\\times10^{-12}}{0.15^2}=3.20\\,\\mathrm{N}$.", "Net $=-5.39+3.20=-2.19\\,\\mathrm{N}$, i.e. $2.19\\,\\mathrm{N}$ towards $-x$ (superposition: add vectors with signs)."), GEN(H1 + ", Q3"), "gen", sig=3)
    # perpendicular forces
    qa_, qb_, qc_, ra, rb = 4.0 * UC, 6.0 * UC, 3.0 * UC, 0.20, 0.30
    Fa = k * qa_ * qc_ / ra ** 2; Fb = k * qb_ * qc_ / rb ** 2; Fr = math.hypot(Fa, Fb)
    chk = np.linalg.norm(force_vec(qc_, (0, 0), qa_, (ra, 0)) + force_vec(qc_, (0, 0), qb_, (0, rb))); check(Fr, chk)
    mcq_num(B, c, "Superposition of forces", 2, "A $3.0\\,\\mu\\mathrm{C}$ charge sits at the origin. A $+4.0\\,\\mu\\mathrm{C}$ charge is on the $x$ axis at $0.20\\,\\mathrm{m}$ and a $+6.0\\,\\mu\\mathrm{C}$ charge on the $y$ axis at $0.30\\,\\mathrm{m}$. What is the magnitude of the net force on the $3.0\\,\\mu\\mathrm{C}$ charge?", Fr, [Fa + Fb, abs(Fa - Fb), Fa, math.sqrt(Fa * Fb)], "N", ex("$F_x=\\dfrac{k(3.0)(4.0)\\times10^{-12}}{0.20^2}=2.70\\,\\mathrm{N}$ (pushing towards $-x$), $F_y=\\dfrac{k(3.0)(6.0)\\times10^{-12}}{0.30^2}=1.80\\,\\mathrm{N}$ (towards $-y$).", "The forces are perpendicular: $F=\\sqrt{2.70^2+1.80^2}=3.24\\,\\mathrm{N}$ (not the sum $4.5\\,\\mathrm{N}$)."), GEN(H1 + ", Q3"), "gen", sig=3)
    # charge sharing
    for qx, qy in [(6.0, -2.0), (9.0, 3.0), (-8.0, 2.0)]:
        fin = (qx + qy) / 2
        mcq_num(B, c, "Charge and conductors", 2, "Two identical small conducting spheres carry charges %s μC and %s μC. They are touched together and separated. What is the charge on each sphere afterwards (in μC)?" % (sci(qx), sci(qy)), fin, [qx + qy, (qx - qy) / 2, qx * qy / (qx + qy), qx / 2, (qx - qy)], "\\mu C", ex("Identical conductors share the total charge equally (charge is conserved): $q=\\dfrac{q_1+q_2}{2}=\\dfrac{%s+(%s)}{2}=%s\\,\\mu\\mathrm{C}$." % (sci(qx), sci(qy), sci(fin))), GEN(H1 + ", Q1"), "gen", sig=3)
    mcq_num(B, c, "Charge and conductors", 1, "How many excess electrons are on an object carrying a charge of $-1.0\\,\\mu\\mathrm{C}$?", 1.0e-6 / E_CH, [1.0e-6 / E_CH / 1000, 1.0e-6 / (2 * E_CH), 1.0e-6 / E_CH * 2, 1.0e-6 / E_CH * 1000], "", ex("Charge is quantised, $q=ne$: $n=\\dfrac{1.0\\times10^{-6}}{1.602\\times10^{-19}}=6.2\\times10^{12}$ electrons."), "Lecture Electricity C1 (charge is quantised)", sig=2, origin="gen")
    r_h = 5.29e-11; Fh = k * E_CH ** 2 / r_h ** 2
    mcq_num(B, c, "Coulomb's law", 1, "In a hydrogen atom the electron is on average $5.29\\times10^{-11}\\,\\mathrm{m}$ from the proton. What is the electrostatic force between them?", Fh, [Fh / 100, Fh * 1e3, k * E_CH / r_h ** 2, Fh / 2], "N", ex("$F=\\dfrac{ke^2}{r^2}=\\dfrac{(8.99\\times10^9)(1.602\\times10^{-19})^2}{(5.29\\times10^{-11})^2}=8.2\\times10^{-8}\\,\\mathrm{N}$: tiny, yet it acts on a mass of only $9\\times10^{-31}\\,\\mathrm{kg}$."), GEN(H1 + ", Q6"), "gen", sig=2)
    mcq_pick(B, c, "Charge and conductors", 1, "Two metal spheres, one positively charged and one neutral, are brought into contact and separated. The neutral sphere ends up", ["positively charged (electrons moved from it to the other sphere)", "negatively charged", "neutral", "positively charged (protons moved onto it)"], 0, ex("Electrons (the mobile carriers) flow from the neutral sphere to the positive one until their potentials equalise; the neutral sphere is left with a deficit of electrons, i.e. positive. Protons do not move in a conductor."), "Lecture Electricity C1 (charge transfer)", "concept")
    mcq_pick(B, c, "Charge and conductors", 1, "A negatively charged rod is brought near, but does not touch, a neutral metal sphere on an insulating stand; the sphere is briefly grounded (touched by a finger) with the rod still in place, and then the rod is removed. The sphere is", ["positively charged", "negatively charged", "neutral", "positively charged only on its far side"], 0, ex("Charging by induction: the rod repels electrons from the sphere to the ground. Removing the ground connection first and the rod afterwards leaves the sphere with a net positive charge, spread uniformly over the surface."), "Lecture Electricity C1 (charging by induction)", "concept")
    mcq_pick(B, c, "Charge and conductors", 1, "Which statement describes the conservation of charge correctly?", ["The net charge of an isolated system never changes", "Charge can be created from energy", "Positive charge is always conserved but negative is not", "Charge is conserved only in collisions of particles"], 0, ex("Charge can be transferred, and particle-antiparticle pairs can be created with total charge zero, but the algebraic sum of the charges of an isolated system is constant."), "Lecture Electricity C1 (conservation of charge)", "concept")
    mcq_pick(B, c, "Coulomb's law", 2, "A charged particle is inside a uniformly charged thin spherical shell. The net electrostatic force on it from the shell is", ["zero", "directed towards the nearest part of the shell", "the same as if the shell's charge were at its centre", "directed away from the centre"], 0, ex("Shell theorem 2: inside a uniformly charged shell the forces from all parts cancel. Outside, the shell acts like a point charge at its centre (shell theorem 1)."), "Midterm tutoring slides (shell theories)", "concept")
    q_s, R_s, d_ = 8.0 * UC, 0.20, 0.50; qt = 1.0 * UC
    Fsh = k * q_s * qt / d_ ** 2
    mcq_num(B, c, "Coulomb's law", 2, "A thin spherical shell of radius $0.20\\,\\mathrm{m}$ carries a uniformly distributed charge of $+8.0\\,\\mu\\mathrm{C}$. What force does it exert on a point charge of $+1.0\\,\\mu\\mathrm{C}$ at $0.50\\,\\mathrm{m}$ from its centre?", Fsh, [k * q_s * qt / (d_ - R_s) ** 2, k * q_s * qt / R_s ** 2, 0.0, k * q_s * qt / (d_ + R_s) ** 2], "N", ex("Outside a uniformly charged shell the force is that of a point charge at the centre: $F=\\dfrac{k(8.0\\times10^{-6})(1.0\\times10^{-6})}{0.50^2}=0.288\\,\\mathrm{N}$ (repulsive). Do not measure the distance to the surface."), "Midterm tutoring slides (shell theories)", "gen", sig=3)

# =============================================================================================== chapter 2
def ch2(B):
    c = "c2"
    # ---------------------------------------------------------------- homework 1, chapter 2
    E_A = 40.0
    mcq_num(B, c, "Electric field and field lines", 1, "In a region the electric field lines on the left have twice the separation of those on the right. If the field magnitude at A (left) is $40\\,\\mathrm{N/C}$, what is the magnitude of the force on a proton at A?", E_CH * E_A, [E_CH * E_A * 2, E_CH * E_A / 2, E_CH * E_A * 4, E_CH * E_A / 4], "N", ex("$F=eE=(1.602\\times10^{-19})(40)=6.4\\times10^{-18}\\,\\mathrm{N}$."), H1 + ", Chapter 2 Q1(a)", sig=2)
    mcq_num(B, c, "Electric field and field lines", 2, "Field lines on the left of a figure are twice as far apart as the lines on the right. If the field is $40\\,\\mathrm{N/C}$ on the left (at A), what is the field magnitude on the right (at B)?", 80.0, [20.0, 40.0, 160.0, 10.0], "N/C", ex("The density of field lines (lines per unit area) is proportional to $E$. Lines twice as close means twice the density, so $E_B=2\\times40=80\\,\\mathrm{N/C}$."), H1 + ", Chapter 2 Q1(b)", sig=2)
    mcq_pick(B, c, "Electric field and field lines", 1, "Which statement about electric field lines is correct?", ["They start on positive charges, end on negative charges, and never cross", "They start on negative charges and end on positive charges", "They can cross where the field is strongest", "They always form closed loops"], 0, ex("The field is tangent to the line and points away from positive charges; the number of lines per unit area measures $E$. A crossing would mean two field directions at one point."), "Midterm tutoring slides (mapping electric fields)", "concept")
    # ring: where is E maximum?
    R = 0.0240
    zs = minimize_scalar(lambda z: -(z / (z * z + R * R) ** 1.5), bounds=(1e-6, 0.2), method="bounded", options={"xatol": 1e-10}).x
    check(zs, R / math.sqrt(2), 1e-4)
    mcq_num(B, c, "Charged ring and disk", 3, "Charge is distributed uniformly around a ring of radius $R=2.40\\,\\mathrm{cm}$. At what distance from the ring's centre, along its axis, is the field magnitude greatest?", R / math.sqrt(2) * 100, [R * 100, R * 100 / 2, R * 100 * math.sqrt(2), 0.0], "cm", ex("$E(z)=\\dfrac{kQz}{(z^2+R^2)^{3/2}}$. Set $\\dfrac{\\mathrm{d}E}{\\mathrm{d}z}=0$: $(z^2+R^2)-3z^2=0\\Rightarrow z=\\dfrac{R}{\\sqrt2}=1.70\\,\\mathrm{cm}$.", "A numerical maximisation of $E(z)$ confirms $z=1.70\\,\\mathrm{cm}$ (zero at the centre, and decaying as $1/z^2$ far away)."), H1 + ", Chapter 2 Q4", sig=3)
    # finite rod, perpendicular bisector
    q, Lr, Rr = 7.81e-12, 0.145, 0.0600
    Er = k * q / (Rr * math.sqrt(Rr ** 2 + (Lr / 2) ** 2))
    En = integrate(lambda x: k * (q / Lr) * Rr / (Rr ** 2 + x ** 2) ** 1.5, -Lr / 2, Lr / 2)
    check(Er, En, 1e-9, "rod field by quadrature")
    mcq_num(B, c, "Charged ring and disk", 3, "A charge $q=7.81\\,\\mathrm{pC}$ is spread uniformly along a thin non-conducting rod of length $L=14.5\\,\\mathrm{cm}$. What is the magnitude of the electric field at point P, at distance $R=6.00\\,\\mathrm{cm}$ from the rod along its perpendicular bisector?", Er, [k * q / Rr ** 2, k * q / (Rr ** 2 + (Lr / 2) ** 2), 2 * Er, k * q / (Rr * Lr / 2)], "N/C", ex("Integrate over the rod (the components along the rod cancel): $E=\\dfrac{kq}{R\\sqrt{R^2+(L/2)^2}}$.", "$E=\\dfrac{(8.99\\times10^9)(7.81\\times10^{-12})}{(0.0600)\\sqrt{0.0600^2+0.0725^2}}=12.4\\,\\mathrm{N/C}$, pointing away from the rod (for positive $q$). Numerical quadrature of the exact integral agrees; treating the rod as a point charge gives $19.5\\,\\mathrm{N/C}$, too much."), H2 + ", Q5", sig=3)
    note(H2 + ", Q5", "the sheet's figure and answer key are not included in the documents; the field at P was computed from the integral (12.4 N/C for the data given) and checked by numerical integration.")
    # disk
    Rd = 0.600
    zd = Rd / math.sqrt(3)
    f = lambda z: 1 - z / math.sqrt(z * z + Rd * Rd)
    check(f(zd), 0.5, 1e-12)
    mcq_num(B, c, "Charged ring and disk", 3, "At what distance along the central perpendicular axis of a uniformly charged plastic disk of radius $0.600\\,\\mathrm{m}$ is the electric field magnitude equal to one-half the magnitude of the field at the centre of the disk's surface?", zd, [Rd / 2, Rd / math.sqrt(2), Rd * math.sqrt(3), Rd / 4], "m", ex("On the axis: $E=\\dfrac{\\sigma}{2\\varepsilon_0}\\left(1-\\dfrac{z}{\\sqrt{z^2+R^2}}\\right)$; at the surface ($z\\to0$) $E_0=\\dfrac{\\sigma}{2\\varepsilon_0}$.", "$1-\\dfrac{z}{\\sqrt{z^2+R^2}}=\\dfrac12\\Rightarrow\\dfrac{z}{\\sqrt{z^2+R^2}}=\\dfrac12\\Rightarrow3z^2=R^2$, $z=\\dfrac{R}{\\sqrt3}=0.346\\,\\mathrm{m}$."), H2 + ", Q6", sig=3)
    # Millikan oil drop
    r_d, rho, E = 1.64e-6, 851.0, 1.92e5
    m_d = rho * 4 / 3 * math.pi * r_d ** 3; q_d = m_d * G / E
    mcq_num(B, c, "Charged particle in a field", 3, "In Millikan's experiment an oil drop of radius $1.64\\,\\mu\\mathrm{m}$ and density $0.851\\,\\mathrm{g/cm^3}$ is held suspended in a DOWNWARD electric field of $1.92\\times10^{5}\\,\\mathrm{N/C}$. What is the magnitude of the charge on the drop in units of $e$?", q_d / E_CH, [q_d / E_CH * 2, q_d / E_CH / 2, q_d / E_CH * 4 / 3, 1.0], "e", ex("Mass $m=\\rho\\,\\tfrac43\\pi r^3=851\\times\\tfrac43\\pi(1.64\\times10^{-6})^3=1.57\\times10^{-14}\\,\\mathrm{kg}$.", "Equilibrium: $|q|E=mg\\Rightarrow|q|=\\dfrac{(1.57\\times10^{-14})(9.8)}{1.92\\times10^5}=8.0\\times10^{-19}\\,\\mathrm{C}=5.0\\,e$.", "The force on the drop must point UP, opposite to the field, so the charge is negative: $q=-5e$."), H2 + ", Q7", sig=2)
    # electron between plates
    E_f = 120.0; a_e = E_CH * E_f / M_E; vx, vy0, dx = 1.5e5, 3.0e3, 0.020
    t = dx / vx; vy = vy0 - a_e * t
    mcq_num(B, c, "Charged particle in a field", 2, "An electron between two charged parallel plates is in a uniform field $\\vec E=(120\\,\\mathrm{N/C})\\hat j$. What is the magnitude of its acceleration?", a_e, [E_CH * E_f / M_P, a_e * 2, a_e / 2, a_e * 1e-3], "m/s^2", ex("$a=\\dfrac{eE}{m}=\\dfrac{(1.602\\times10^{-19})(120)}{9.11\\times10^{-31}}=2.11\\times10^{13}\\,\\mathrm{m/s^2}$, directed along $-\\hat j$ (the force on an electron is opposite to $\\vec E$)."), H2 + ", Q8(a)", sig=3)
    mcq_num(B, c, "Charged particle in a field", 3, "The electron has $v_x=1.5\\times10^{5}\\,\\mathrm{m/s}$ and $v_y=3.0\\times10^{3}\\,\\mathrm{m/s}$ and accelerates at $-2.11\\times10^{13}\\,\\mathrm{m/s^2}$ along $y$. What is $v_y$ after its $x$ coordinate has changed by $2.0\\,\\mathrm{cm}$?", vy, [-vy, vy * 10, vy / 10, -vy / 2, vy0], "m/s", ex("The $x$-motion is uniform: $t=\\dfrac{0.020}{1.5\\times10^5}=1.33\\times10^{-7}\\,\\mathrm{s}$.", "$v_y=3.0\\times10^3+(-2.11\\times10^{13})(1.33\\times10^{-7})=-2.81\\times10^6\\,\\mathrm{m/s}$; $v_x$ is unchanged, so $\\vec v=(1.5\\times10^5\\hat i-2.8\\times10^6\\hat j)\\,\\mathrm{m/s}$."), H2 + ", Q8(b)", sig=3)
    p_, E_ = 3.02e-25, 46.0; th0 = math.radians(64.0)
    W = p_ * E_ * (math.cos(th0) - math.cos(th0 + math.pi))
    U = lambda th: -p_ * E_ * math.cos(th)
    check(W, U(th0 + math.pi) - U(th0))
    mcq_num(B, c, "Electric dipoles", 3, "How much work is required to turn an electric dipole through $180^\\circ$ in a uniform field of $46.0\\,\\mathrm{N/C}$ if the dipole moment is $3.02\\times10^{-25}\\,\\mathrm{C\\,m}$ and the initial angle between $\\vec p$ and $\\vec E$ is $64^\\circ$?", W, [2 * p_ * E_, p_ * E_ * math.cos(th0), 0.0, p_ * E_ * (1 - math.cos(th0))], "J", ex("$U=-pE\\cos\\theta$. Initially $\\theta=64^\\circ$, finally $244^\\circ$: $W=\\Delta U=-pE(\\cos244^\\circ-\\cos64^\\circ)=2pE\\cos64^\\circ$.", "$W=2(3.02\\times10^{-25})(46.0)\\cos64^\\circ=1.22\\times10^{-23}\\,\\mathrm{J}$ (positive work is needed: the dipole prefers $\\theta<90^\\circ$)."), H2 + ", Q9", sig=3)
    # dipole far field, bisector
    p2_, rr = 4.0e-12, 0.30
    Ed = k * p2_ / rr ** 3
    mcq_num(B, c, "Electric dipoles", 2, "An electric dipole has moment $p=4.0\\times10^{-12}\\,\\mathrm{C\\,m}$. What is the magnitude of its field on the perpendicular bisector at a distance $r=0.30\\,\\mathrm{m}\\gg d$ from its centre?", Ed, [2 * Ed, k * p2_ / rr ** 2, Ed / 2, k * p2_ / rr ** 4], "N/C", ex("Far on the bisector $E=\\dfrac{kp}{r^3}=\\dfrac{(8.99\\times10^9)(4.0\\times10^{-12})}{0.30^3}=1.33\\,\\mathrm{N/C}$, pointing OPPOSITE to $\\vec p$. (On the axis it is twice as large, $2kp/r^3$.)"), GEN(H1 + ", Chapter 2 Q3"), "gen", sig=3)
    # exact dipole vs approximation (two charges, numerically)
    q0, d0, z0 = 1.0e-9, 0.01, 0.50
    Eax = field_vec([q0, -q0], [(0, d0 / 2), (0, -d0 / 2)], (0, z0))[1]; Eap = 2 * k * q0 * d0 / z0 ** 3
    check(Eax, Eap, 2e-3)
    mcq_num(B, c, "Electric dipoles", 2, "A dipole consists of $+1.0\\,\\mathrm{nC}$ and $-1.0\\,\\mathrm{nC}$ separated by $1.0\\,\\mathrm{cm}$. What is the magnitude of the field on its axis at $0.50\\,\\mathrm{m}$ from the centre?", Eap, [Eap / 2, k * q0 / z0 ** 2, Eap * 2, k * q0 * d0 / z0 ** 2], "N/C", ex("Far on the axis $E=\\dfrac{2kp}{z^3}$ with $p=qd=1.0\\times10^{-11}\\,\\mathrm{C\\,m}$: $E=\\dfrac{2(8.99\\times10^9)(1.0\\times10^{-11})}{0.50^3}=1.44\\,\\mathrm{N/C}$.", "Adding the exact fields of the two charges gives the same value to within $0.1\\%$. A single charge would give $36\\,\\mathrm{N/C}$: the two nearly cancel."), GEN(H1 + ", Chapter 2 Q3"), "gen", sig=3)
    # point charge fields
    for qv, rv in [(2.0e-9, 0.30), (-5.0e-9, 0.10), (12.0e-9, 0.60)]:
        Ep = k * abs(qv) / rv ** 2
        mcq_num(B, c, "Electric field and field lines", 1, "What is the magnitude of the electric field %s m from a point charge of %s nC?" % (sci(rv), sci(qv * 1e9)), Ep, [Ep * rv, k * abs(qv) / rv, Ep / 2, Ep * 100], "N/C", ex("$E=\\dfrac{k|q|}{r^2}=\\dfrac{(8.99\\times10^9)(%s\\times10^{-9})}{%s^2}=%s\\,\\mathrm{N/C}$; it points %s the charge." % (sci(abs(qv * 1e9)), sci(rv), sci(Ep), "toward" if qv < 0 else "away from")), GEN(H1 + ", Chapter 2 Q2"), "gen", sig=3)
    # midpoint of two charges
    for qa_, qb_, dd in [(4.0e-9, 4.0e-9, 0.20), (6.0e-9, -2.0e-9, 0.40), (3.0e-9, 9.0e-9, 0.30)]:
        E_mid = field_vec([qa_, qb_], [(0, 0), (dd, 0)], (dd / 2, 0))[0]
        Ea = k * qa_ / (dd / 2) ** 2; Eb = k * qb_ / (dd / 2) ** 2
        check(E_mid, Ea - Eb)
        mcq_num(B, c, "Superposition of fields", 2, "Charges %s nC (at x = 0) and %s nC (at x = %s m) lie on the x axis. What is the electric field at the midpoint (positive = towards +x)?" % (sci(qa_ * 1e9), sci(qb_ * 1e9), sci(dd)), E_mid, [-E_mid, Ea + Eb, Ea, k * (qa_ + qb_) / dd ** 2], "N/C",
                ex("Both distances are %s m. Left charge: $E_a=\\dfrac{kq_a}{r^2}=%s\\,\\mathrm{N/C}$ along $+x$ if $q_a>0$." % (sci(dd / 2), sci(Ea)),
                   "Right charge: $E_b=\\dfrac{kq_b}{r^2}=%s\\,\\mathrm{N/C}$, directed along $-x$ if $q_b>0$ (away from a positive charge)." % sci(Eb),
                   "Net $E_x=E_a-E_b=%s\\,\\mathrm{N/C}$: like charges partly cancel at the midpoint, opposite charges add." % sci(E_mid)), GEN(H1 + ", Chapter 2 Q2"), "gen", sig=3)
    # motion in uniform field
    for v0, Efield, L_ in [(2.0e6, 500.0, 0.05), (1.0e7, 2000.0, 0.04)]:
        t = L_ / v0; dy = 0.5 * E_CH * Efield / M_E * t ** 2
        mcq_num(B, c, "Charged particle in a field", 3, "An electron enters the region between horizontal plates at %s m/s, parallel to them. The uniform field is %s N/C and the plates are %s m long. By how much is the electron deflected (in mm) when it leaves?" % (sci(v0), sci(Efield), sci(L_)), dy * 1e3, [dy * 2e3, dy * 1e3 / 2, E_CH * Efield / M_E * t * 1e3, dy * 1e4], "mm", ex("Time between the plates $t=\\dfrac{L}{v_0}=%s\\,\\mathrm{s}$; acceleration $a=\\dfrac{eE}{m}=%s\\,\\mathrm{m/s^2}$." % (sci(t), sci(E_CH * Efield / M_E)), "Deflection $y=\\tfrac12at^2=%s\\,\\mathrm{m}=%s\\,\\mathrm{mm}$ (a parabola, like a projectile)." % (sci(dy), sci(dy * 1e3))), GEN(H2 + ", Q8"), "gen", sig=3)
    V_acc = 1000.0; vv = math.sqrt(2 * E_CH * V_acc / M_E)
    mcq_num(B, c, "Charged particle in a field", 2, "A uniform field of $5.0\\times10^{3}\\,\\mathrm{N/C}$ acts on a proton released from rest. How long does it take the proton to reach $1.0\\times10^{5}\\,\\mathrm{m/s}$?", 1.0e5 / (E_CH * 5.0e3 / M_P), [1.0e5 / (E_CH * 5.0e3 / M_E), 2 * 1.0e5 / (E_CH * 5.0e3 / M_P), 1.0e5 / (E_CH * 5.0e3 / M_P) / 2, 4 * 1.0e5 / (E_CH * 5.0e3 / M_P)], "s", ex("$a=\\dfrac{eE}{m_p}=\\dfrac{(1.602\\times10^{-19})(5.0\\times10^3)}{1.673\\times10^{-27}}=4.8\\times10^{11}\\,\\mathrm{m/s^2}$.", "$t=\\dfrac{v}{a}=\\dfrac{1.0\\times10^5}{4.8\\times10^{11}}=2.1\\times10^{-7}\\,\\mathrm{s}$."), GEN(H2 + ", Q8"), "gen", sig=2)
    # torque on a dipole
    p_, E_, th = 2.0e-29, 3.0e4, 30.0
    tau = p_ * E_ * math.sin(math.radians(th))
    mcq_num(B, c, "Electric dipoles", 2, "A water molecule has dipole moment $6.2\\times10^{-30}\\,\\mathrm{C\\,m}$. What torque acts on it when it makes an angle of $30^\\circ$ with a uniform field of $3.0\\times10^{4}\\,\\mathrm{N/C}$?", 6.2e-30 * 3.0e4 * 0.5, [6.2e-30 * 3.0e4, 6.2e-30 * 3.0e4 * math.cos(math.radians(30)), 6.2e-30 * 3.0e4 * 2, 6.2e-30 / 3.0e4], "N m", ex("$\\tau=pE\\sin\\theta=(6.2\\times10^{-30})(3.0\\times10^4)\\sin30^\\circ=9.3\\times10^{-26}\\,\\mathrm{N\\,m}$; it tries to align $\\vec p$ with $\\vec E$."), "Lecture Electricity C2 (a dipole in an electric field)", "gen", sig=2)
    mcq_pick(B, c, "Electric dipoles", 2, "In a uniform electric field the net force on an electric dipole is", ["zero, but there is a torque unless $\\vec p\\parallel\\vec E$", "non-zero and along $\\vec p$", "zero and also zero torque", "along $\\vec E$ and equal to $pE$"], 0, ex("The two charges feel equal and opposite forces $\\pm q\\vec E$: no net force, but a torque $\\vec\\tau=\\vec p\\times\\vec E$ (zero only when $\\vec p$ and $\\vec E$ are parallel or antiparallel)."), "Lecture Electricity C2 (a dipole in an electric field)", "concept")
    mcq_pick(B, c, "Electric field and field lines", 1, "A negative test charge is placed in the field of a positive point charge. The force on the test charge points", ["towards the positive charge", "away from the positive charge", "perpendicular to the field line", "in the direction of the field"], 0, ex("The force on a negative charge is opposite to $\\vec E$; $\\vec E$ points away from the positive charge, so the force points towards it (attraction)."), "Lecture Electricity C2 (the electric field)", "concept")
    # infinite line, plane from superposition (line of charge, Halliday ch.22)
    lam, d_ = 5.0e-9, 0.20
    mcq_num(B, c, "Charged ring and disk", 2, "A very long straight wire carries a uniform linear charge density of $5.0\\,\\mathrm{nC/m}$. What is the field magnitude $0.20\\,\\mathrm{m}$ from the wire?", 2 * k * lam / d_, [k * lam / d_, k * lam / d_ ** 2, 2 * k * lam / d_ ** 2, 2 * k * lam * d_], "N/C", ex("Infinite line: $E=\\dfrac{\\lambda}{2\\pi\\varepsilon_0r}=\\dfrac{2k\\lambda}{r}=\\dfrac{2(8.99\\times10^9)(5.0\\times10^{-9})}{0.20}=450\\,\\mathrm{N/C}$, falling off as $1/r$ (not $1/r^2$). (A finite rod gives this limit when $r\\ll L$.)"), "Lecture Electricity C2 (a line of charge)", "gen", sig=3)
    Qr, zr, Rr_ = 3.0e-9, 0.10, 0.05
    Ering = k * Qr * zr / (zr ** 2 + Rr_ ** 2) ** 1.5
    Enum = integrate(lambda th: k * (Qr / (2 * math.pi)) * zr / (zr ** 2 + Rr_ ** 2) ** 1.5, 0, 2 * math.pi)
    check(Ering, Enum, 1e-9)
    mcq_num(B, c, "Charged ring and disk", 2, "A ring of radius $5.0\\,\\mathrm{cm}$ carries a uniformly distributed charge of $3.0\\,\\mathrm{nC}$. What is the electric field on the axis, $10\\,\\mathrm{cm}$ from the centre?", Ering, [k * Qr / zr ** 2, k * Qr * zr / (zr ** 2 + Rr_ ** 2), k * Qr / (zr ** 2 + Rr_ ** 2), k * Qr * zr / (zr ** 2 + Rr_ ** 2) ** 2], "N/C", ex("$E=\\dfrac{kQz}{(z^2+R^2)^{3/2}}=\\dfrac{(8.99\\times10^9)(3.0\\times10^{-9})(0.10)}{(0.010+0.0025)^{3/2}}=1.9\\times10^{3}\\,\\mathrm{N/C}$, along the axis away from the ring.", "Treating the ring as a point charge at the centre would give $2.7\\times10^3\\,\\mathrm{N/C}$ - not accurate at $z=2R$."), GEN(H1 + ", Chapter 2 Q4"), "gen", sig=2)


# =============================================================================================== more chapter 1 and 2 questions
def ch1b(B):
    c = "c1"
    LEC = "Lecture Electricity C1 (Coulomb's law)"
    r_p = 4.0e-15
    Fp = k * E_CH ** 2 / r_p ** 2
    mcq_num(B, c, "Coulomb's law", 1, "How large is the electrostatic repulsion between two protons that are $4.0\\times10^{-15}\\,\\mathrm{m}$ apart inside a nucleus?", Fp, [Fp / 1000, Fp * 4, Fp / 4, Fp * 1000], "N", ex("$F=\\dfrac{ke^2}{r^2}=\\dfrac{(8.99\\times10^9)(1.602\\times10^{-19})^2}{(4.0\\times10^{-15})^2}=14\\,\\mathrm{N}$: enormous for a proton, and held in check by the strong nuclear force."), LEC + ", charge is quantised", "src", sig=2)
    mcq_num(B, c, "Charge and conductors", 2, "What is the total charge of one mole of electrons ($N_A=6.022\\times10^{23}$)?", N_A * E_CH, [N_A * E_CH * 2, N_A * E_CH / 1000, N_A * E_CH * 1000, N_A * E_CH / 2], "C", ex("$Q=N_Ae=(6.022\\times10^{23})(1.602\\times10^{-19})=9.65\\times10^{4}\\,\\mathrm{C}$ (the Faraday constant)."), LEC + ", charge is quantised", sig=3, origin="gen")
    mcq_pick(B, c, "Charge and conductors", 2, "In the nuclear decay $^{226}_{88}\\mathrm{Ra}\\to{}^{A}_{Z}\\mathrm{Rn}+{}^{4}_{2}\\mathrm{He}$, charge conservation fixes the atomic number $Z$ of the radon nucleus to be", ["$86$", "$90$", "$88$", "$84$"], 0, ex("Charge (atomic number) is conserved: $88=Z+2\\Rightarrow Z=86$ (the mass number gives $A=226-4=222$)."), LEC + ", charge is conserved", "concept")
    mcq_pick(B, c, "Charge and conductors", 1, "In the decay of a free neutron, $n\\to p+e^-+\\bar\\nu$, which fact about charge is illustrated?", ["the net charge before ($0$) equals the net charge after ($+e-e+0$)", "charge is created in the decay", "the neutron is positively charged", "electrons cannot be created"], 0, ex("Charges $0\\to(+e)+(-e)+0=0$: charged particles appear in pairs, the total stays constant."), LEC + ", charge is conserved", "concept")
    q, a_ = 3.0e-6, 0.50
    Ft = math.sqrt(3) * k * q * q / a_ ** 2
    chk = np.linalg.norm(force_vec(q, (0, 0), q, (a_, 0)) + force_vec(q, (0, 0), q, (a_ / 2, a_ * math.sqrt(3) / 2)))
    check(Ft, chk)
    mcq_num(B, c, "Superposition of forces", 2, "Three equal charges of $3.0\\,\\mu\\mathrm{C}$ sit at the corners of an equilateral triangle of side $0.50\\,\\mathrm{m}$. What is the magnitude of the net force on one of them?", Ft, [2 * k * q * q / a_ ** 2, k * q * q / a_ ** 2, k * q * q / a_ ** 2 * math.sqrt(2), Ft / 2], "N", ex("Each of the other two charges pushes with $F_0=\\dfrac{kq^2}{a^2}=0.324\\,\\mathrm{N}$, at $60^\\circ$ to each other.", "Resultant $=2F_0\\cos30^\\circ=\\sqrt3\\,F_0=0.561\\,\\mathrm{N}$ along the bisector, away from the other two."), GEN(H1 + ", Q2"), "gen", sig=3)
    q, a_ = 2.0e-6, 0.30
    Fsq = (math.sqrt(2) + 0.5) * k * q * q / a_ ** 2
    pos = [(a_, 0), (0, a_), (a_, a_)]
    chk = np.linalg.norm(sum(force_vec(q, (0, 0), q, p_) for p_ in pos))
    check(Fsq, chk)
    mcq_num(B, c, "Superposition of forces", 3, "Four equal charges of $2.0\\,\\mu\\mathrm{C}$ are at the corners of a square of side $0.30\\,\\mathrm{m}$. What is the magnitude of the net force on one charge?", Fsq, [3 * k * q * q / a_ ** 2, (2 + 0.5) * k * q * q / a_ ** 2, math.sqrt(2) * k * q * q / a_ ** 2, k * q * q / a_ ** 2], "N", ex("Let $F_0=\\dfrac{kq^2}{a^2}=0.400\\,\\mathrm{N}$. The two neighbours give $F_0$ each at $90^\\circ$: resultant $\\sqrt2F_0$ along the diagonal.", "The opposite corner (distance $a\\sqrt2$) adds $\\dfrac{F_0}{2}$ in the same direction. Net $=\\left(\\sqrt2+\\tfrac12\\right)F_0=0.765\\,\\mathrm{N}$."), GEN(H1 + ", Q2"), "gen", sig=3)
    qq_, m_ = 1.0e-6, 1.0e-3
    r_eq = qq_ * math.sqrt(k / (m_ * G))
    mcq_num(B, c, "Coulomb's law", 2, "At what separation is the electrostatic repulsion between two $1.0\\,\\mu\\mathrm{C}$ charges equal to the weight of a $1.0\\,\\mathrm{g}$ mass?", r_eq, [k * qq_ ** 2 / (m_ * G), qq_ * k / (m_ * G), r_eq / 2, r_eq * 2], "m", ex("$\\dfrac{kq^2}{r^2}=mg\\Rightarrow r=q\\sqrt{\\dfrac{k}{mg}}=10^{-6}\\sqrt{\\dfrac{8.99\\times10^9}{(10^{-3})(9.8)}}=0.96\\,\\mathrm{m}$: electrical forces on everyday objects are huge compared with gravity."), GEN(H1 + ", Q7"), "gen", sig=2)
    mcq_num(B, c, "Coulomb's law", 2, "Two charges $+9.0\\,\\mu\\mathrm{C}$ and $+4.0\\,\\mu\\mathrm{C}$ are $0.50\\,\\mathrm{m}$ apart. At what point on the line between them (distance from the larger charge) is the force on a small test charge zero?", 0.50 * 3 / 5, [0.25, 0.50 * 2 / 5, 0.50 * 9 / 13, 0.50 * 4 / 13], "m", ex("Zero force when $\\dfrac{9}{x^2}=\\dfrac{4}{(0.50-x)^2}\\Rightarrow\\dfrac{x}{0.50-x}=\\dfrac32\\Rightarrow x=0.30\\,\\mathrm{m}$ from the larger charge (nearer the smaller one)."), GEN(H1 + ", Q4"), "gen", sig=2)
    mcq_pick(B, c, "Coulomb's law", 1, "Coulomb's law $F=kq_1q_2/r^2$ applies directly to", ["point charges and, outside them, uniformly charged spheres", "any two charged objects at any separation", "moving charges only", "neutral objects"], 0, ex("It holds for point charges; by the shell theorem a uniformly charged sphere acts like a point charge at its centre for outside points. Extended objects need integration."), LEC, "concept")
    mcq_pick(B, c, "Coulomb's law", 1, "The electrostatic force between two charges acts", ["along the line joining them, with equal magnitudes on the two charges", "perpendicular to the line joining them", "only on the larger charge", "with a magnitude that depends on the direction of the line"], 0, ex("It is a central force obeying Newton's third law: equal and opposite on the two charges."), LEC, "concept")
    mcq_pick(B, c, "Charge and conductors", 1, "Rubbing a glass rod with silk makes the rod positive. This happens because", ["electrons move from the rod to the silk", "protons move from the rod to the silk", "electrons move from the silk to the rod", "charge is created on the rod"], 0, ex("Only electrons transfer between solids by friction. The rod loses electrons (net positive) and the silk gains them (net negative): the total charge stays zero."), "Lecture Electricity C1 (charge transfer)", "concept")
    mcq_pick(B, c, "Charge and conductors", 1, "A material in which charges are NOT free to move is called", ["an insulator", "a conductor", "a superconductor", "a plasma"], 0, ex("In an insulator (non-conductor) the charges stay where they are put; in a conductor they move freely."), "Midterm tutoring slides (conductors and insulators)", "concept")
    q1_, q2_, r_ = 6.0e-6, 2.0e-6, 0.40
    Fa = k * q1_ * q2_ / r_ ** 2
    mcq_num(B, c, "Coulomb's law", 2, "A $6.0\\,\\mu\\mathrm{C}$ and a $2.0\\,\\mu\\mathrm{C}$ charge are $0.40\\,\\mathrm{m}$ apart. What is the force on the $2.0\\,\\mu\\mathrm{C}$ charge?", Fa, [Fa * 3, Fa / 3, Fa * 2, Fa / 2], "N", ex("$F=\\dfrac{kq_1q_2}{r^2}=\\dfrac{(8.99\\times10^9)(6.0\\times10^{-6})(2.0\\times10^{-6})}{0.40^2}=0.674\\,\\mathrm{N}$. By Newton's third law the $6.0\\,\\mu\\mathrm{C}$ charge feels exactly the same force (the bigger charge does not feel a bigger force)."), GEN(H1 + ", Q6"), "gen", sig=3)
    mcq_num(B, c, "Coulomb's law", 2, "Two charges repel each other with a force of $0.20\\,\\mathrm{N}$ at a distance of $0.30\\,\\mathrm{m}$. What is the force at a distance of $0.10\\,\\mathrm{m}$?", 0.20 * 9, [0.20 * 3, 0.20 / 9, 0.20 * 6, 0.20 / 3], "N", ex("$F\\propto1/r^2$: the distance is divided by $3$, so the force is multiplied by $9$: $1.8\\,\\mathrm{N}$."), GEN(H1 + ", Q6"), "gen", sig=2)
    mcq_num(B, c, "Charge and conductors", 2, "Sphere A has $+8.0\\,\\mu\\mathrm{C}$ and an identical sphere B is neutral. A touches B, they are separated, then B touches a third identical neutral sphere C. What is the final charge on B (in $\\mu$C)?", 2.0, [4.0, 8.0, 1.0, 2.67], "\\mu C", ex("A and B share: $+4.0\\,\\mu\\mathrm{C}$ each. Then B and C share B's $+4.0\\,\\mu\\mathrm{C}$ equally: B ends with $+2.0\\,\\mu\\mathrm{C}$ (and C with $+2.0\\,\\mu\\mathrm{C}$, A keeps $+4.0\\,\\mu\\mathrm{C}$)."), GEN(H1 + ", Q1"), "gen", sig=2)

def ch2b(B):
    c = "c2"
    LEC = "Lecture Electricity C2 (electric fields)"
    # zero-field point between two like charges
    xz = 0.30 * 2 / 3
    mcq_num(B, c, "Superposition of fields", 2, "Charges $+4.0\\,\\mathrm{nC}$ and $+1.0\\,\\mathrm{nC}$ are $0.30\\,\\mathrm{m}$ apart. At what distance from the $+4.0\\,\\mathrm{nC}$ charge, between them, is the electric field zero?", xz, [0.15, 0.30 / 3, 0.30 * 4 / 5, 0.30 / 5], "m", ex("The fields oppose between like charges; zero when $\\dfrac{4}{x^2}=\\dfrac{1}{(0.30-x)^2}\\Rightarrow0.30-x=\\dfrac x2\\Rightarrow x=0.20\\,\\mathrm{m}$ (closer to the smaller charge)."), GEN(H1 + ", Chapter 2 Q2"), "gen", sig=2)
    # square with +q,+q top, -q,-q bottom: field at the centre
    q, a_ = 3.0e-9, 0.20
    qs = [q, q, -q, -q]; ps = [(-a_ / 2, a_ / 2), (a_ / 2, a_ / 2), (-a_ / 2, -a_ / 2), (a_ / 2, -a_ / 2)]
    Esq = np.linalg.norm(field_vec(qs, ps, (0, 0)))
    check(Esq, 4 * math.sqrt(2) * k * q / a_ ** 2)
    mcq_num(B, c, "Superposition of fields", 3, "Charges $+3.0\\,\\mathrm{nC}$ sit at the two TOP corners and $-3.0\\,\\mathrm{nC}$ at the two BOTTOM corners of a square of side $0.20\\,\\mathrm{m}$. What is the field magnitude at the centre of the square?", Esq, [0.0, 2 * math.sqrt(2) * k * q / a_ ** 2, 4 * k * q / a_ ** 2, 2 * k * q / a_ ** 2], "N/C", ex("Each corner is at $\\dfrac{a}{\\sqrt2}$ from the centre: each field has magnitude $\\dfrac{kq}{a^2/2}=\\dfrac{2kq}{a^2}=1.35\\times10^3\\,\\mathrm{N/C}$.", "The horizontal components cancel in pairs; the four vertical components (down, from each charge) add: $E=4\\cdot\\dfrac{2kq}{a^2}\\cos45^\\circ=\\dfrac{4\\sqrt2\\,kq}{a^2}=3.8\\times10^3\\,\\mathrm{N/C}$ pointing from the positive towards the negative charges."), GEN(H1 + ", Chapter 2 Q2"), "gen", sig=2)
    mm, EE, th = 2.0e-3, 1.5e3, 20.0
    qb = mm * G * math.tan(math.radians(th)) / EE
    mcq_num(B, c, "Charged particle in a field", 3, "A $2.0\\,\\mathrm{g}$ charged ball hangs from a light thread in a uniform horizontal field of $1.5\\times10^{3}\\,\\mathrm{N/C}$ and rests with the thread at $20^\\circ$ to the vertical. What is its charge?", qb, [mm * G * math.sin(math.radians(th)) / EE, mm * G / EE, mm * G / (EE * math.tan(math.radians(th))), qb * 2], "C", ex("Equilibrium: $T\\cos\\theta=mg$ and $T\\sin\\theta=qE$, so $q=\\dfrac{mg\\tan\\theta}{E}=\\dfrac{(2.0\\times10^{-3})(9.8)\\tan20^\\circ}{1.5\\times10^3}=4.8\\times10^{-6}\\,\\mathrm{C}$."), GEN(H2 + ", Q7"), "gen", sig=2)
    Qr, Lr, dr = 4.0e-9, 0.20, 0.10
    Ex = k * Qr / (dr * (dr + Lr))
    En = integrate(lambda x: k * (Qr / Lr) / x ** 2, dr, dr + Lr)
    check(Ex, En, 1e-9)
    mcq_num(B, c, "Charged ring and disk", 3, "A thin rod of length $0.20\\,\\mathrm{m}$ carries a uniformly distributed charge of $4.0\\,\\mathrm{nC}$. What is the field magnitude on the line of the rod, at a point $0.10\\,\\mathrm{m}$ beyond one end?", Ex, [k * Qr / dr ** 2, k * Qr / (dr + Lr) ** 2, k * Qr / (dr + Lr / 2) ** 2, Ex * 2], "N/C", ex("Integrate $\\mathrm{d}E=\\dfrac{k\\lambda\\,\\mathrm{d}x}{x^2}$ from $x=d$ to $d+L$: $E=k\\lambda\\left(\\dfrac1d-\\dfrac1{d+L}\\right)=\\dfrac{kQ}{d(d+L)}=\\dfrac{(8.99\\times10^9)(4.0\\times10^{-9})}{(0.10)(0.30)}=1.2\\times10^{3}\\,\\mathrm{N/C}$.", "Using a point charge at the centre ($k Q/(d+L/2)^2=2.2\\times10^3\\,\\mathrm{N/C}$) is not valid so close to the rod."), GEN(H1 + ", Chapter 2 Q4"), "gen", sig=2)
    mcq_pick(B, c, "Electric field and field lines", 1, "The electric field of a point charge at twice the distance is", ["$1/4$ as strong", "$1/2$ as strong", "twice as strong", "unchanged"], 0, ex("$E=\\dfrac{kq}{r^2}$."), LEC, "concept")
    mcq_pick(B, c, "Electric field and field lines", 1, "The field of a very long uniformly charged wire at twice the distance is", ["$1/2$ as strong", "$1/4$ as strong", "twice as strong", "unchanged"], 0, ex("An infinite line gives $E=\\dfrac{\\lambda}{2\\pi\\varepsilon_0r}\\propto\\dfrac1r$."), LEC + " (a line of charge)", "concept")
    mcq_pick(B, c, "Electric field and field lines", 2, "Which equation gives the force on a charge $q$ placed in an electric field $\\vec E$?", ["$\\vec F=q\\vec E$ (along $\\vec E$ for $q>0$, opposite for $q<0$)", "$\\vec F=\\vec E/q$", "$\\vec F=qE^2$", "$\\vec F=q/\\vec E$"], 0, ex("The field is defined as force per unit positive test charge, $\\vec E=\\vec F/q_0$."), LEC + " (the electric field)", "concept")
    mcq_num(B, c, "Charged particle in a field", 2, "How many times larger is the acceleration of an electron than that of a proton in the same electric field?", M_P / M_E, [math.sqrt(M_P / M_E), 1.0, M_E / M_P, (M_P / M_E) ** 2], "", ex("Same force magnitude $eE$; $a=\\dfrac{eE}{m}$, so $\\dfrac{a_e}{a_p}=\\dfrac{m_p}{m_e}=\\dfrac{1.673\\times10^{-27}}{9.11\\times10^{-31}}=1.84\\times10^{3}$ (in opposite directions)."), GEN(H2 + ", Q8"), "gen", sig=3)
    E0, d_ = 2.0e3, 0.05
    t = math.sqrt(2 * d_ * M_P / (E_CH * E0))
    mcq_num(B, c, "Charged particle in a field", 3, "A proton starts from rest at one plate of a parallel-plate capacitor with uniform field $2.0\\times10^{3}\\,\\mathrm{N/C}$. How long does it take to cross a gap of $5.0\\,\\mathrm{cm}$?", t, [math.sqrt(2 * d_ * M_E / (E_CH * E0)), d_ / math.sqrt(E_CH * E0 / M_P), t / 2, 2 * t], "s", ex("$a=\\dfrac{eE}{m_p}=1.9\\times10^{11}\\,\\mathrm{m/s^2}$.", "$d=\\tfrac12at^2\\Rightarrow t=\\sqrt{\\dfrac{2d}{a}}=\\sqrt{\\dfrac{2(0.050)}{1.9\\times10^{11}}}=7.2\\times10^{-7}\\,\\mathrm{s}$."), GEN(H2 + ", Q8"), "gen", sig=2)
    p_, E_ = 5.0e-30, 4.0e4
    Udip = -p_ * E_ * math.cos(math.radians(60.0))
    mcq_num(B, c, "Electric dipoles", 2, "A dipole of moment $5.0\\times10^{-30}\\,\\mathrm{C\\,m}$ makes an angle of $60^\\circ$ with a uniform field of $4.0\\times10^{4}\\,\\mathrm{N/C}$. What is its potential energy ($U=-\\vec p\\cdot\\vec E$)?", Udip, [-Udip, -p_ * E_, p_ * E_ * math.sin(math.radians(60.0)), 0.0], "J", ex("$U=-pE\\cos\\theta=-(5.0\\times10^{-30})(4.0\\times10^4)\\cos60^\\circ=-1.0\\times10^{-25}\\,\\mathrm{J}$. Negative: the dipole is below its maximum energy ($+pE$ at $180^\\circ$), minimum $-pE$ at $0^\\circ$."), GEN(H2 + ", Q9"), "gen", sig=2)
    mcq_pick(B, c, "Electric field and field lines", 1, "At the centre of a uniformly charged ring the electric field is", ["zero (the contributions of opposite elements cancel)", "$kQ/R^2$", "$kQ/R$", "infinite"], 0, ex("For every element there is an opposite one producing an equal and opposite field at the centre."), LEC + " (a charged ring)", "concept")
    mcq_pick(B, c, "Electric field and field lines", 2, "A positive point charge is released from rest in a non-uniform electric field. It", ["moves along the field line only if the line is straight", "always moves along the field line it started on", "moves perpendicular to the field line", "stays at rest"], 0, ex("The initial acceleration is along $\\vec E$, but later the velocity is no longer along the (curved) line: the path follows a field line only when the line is straight."), LEC + " (a point charge in an electric field)", "concept")
    E_, d_, v0 = 2.0e3, 0.04, 3.0e6
    t = d_ / v0; vy = E_CH * E_ / M_E * t
    ang = math.degrees(math.atan2(vy, v0))
    mcq_num(B, c, "Charged particle in a field", 3, "An electron moving horizontally at $3.0\\times10^{6}\\,\\mathrm{m/s}$ enters a region of vertical field $2.0\\times10^{3}\\,\\mathrm{N/C}$ that is $4.0\\,\\mathrm{cm}$ long. At what angle to its original direction does it leave?", ang, [math.degrees(math.atan2(0.5 * vy, v0)), ang * 2, 90.0 - ang, math.degrees(math.atan2(2 * vy, v0))], "deg", ex("Time in the field $t=\\dfrac{L}{v_0}=1.33\\times10^{-8}\\,\\mathrm{s}$; $a=\\dfrac{eE}{m}=3.5\\times10^{14}\\,\\mathrm{m/s^2}$.", "$v_y=at=4.7\\times10^{6}\\,\\mathrm{m/s}$ and $\\tan\\theta=\\dfrac{v_y}{v_0}=1.56\\Rightarrow\\theta=57^\\circ$."), GEN(H2 + ", Q8"), "gen", sig=2)
