# -*- coding: utf-8 -*-
"""Physics I gap-fill pool: questions for the concepts that the Concept finder reported as thin (vectors, Hooke's law, conservative forces,
impulse, connected bodies, Carnot, displacement/velocity, motion graphs, thermal expansion, power, rotation, apparent weight).
A separate Bank (ids of kind 'g', tag 'gap') merged after the main bank, so the ids and option order of the existing questions do not move
and the fixed quizzes and mock exams keep their questions; the new ones live in the practice bank, the random quizzes and one extra set per chapter."""
import math
from phys_common import *
import figs
from qlib import Bank

TAG = ("gap",)
def GAP(topic): return "Generated to fill a gap: " + topic

def num(B, ch, topic, level, stem, ans, wrongs, unit, explain, sig=3, fig=None):
    return mcq_num(B, ch, topic, level, stem, ans, wrongs, unit, explain, GAP(topic), origin="gen", sig=sig, fig=fig, tags=TAG)

def txt(B, ch, topic, level, stem, correct, wrongs, explain, fig=None):
    return mcq_text(B, ch, topic, level, stem, correct, wrongs, explain, GAP(topic), origin="concept", fig=fig, tags=TAG)

# =============================================================================================== chapter 1
def vectors(B):
    c, t = "c1", "Vectors and components"
    A, th = 12.0, 35.0
    Ax, Ay = A * math.cos(rad(th)), A * math.sin(rad(th)); check(math.hypot(Ax, Ay), A)
    num(B, c, t, 1, "A displacement has magnitude $12.0\\,\\mathrm{m}$ and points $35^\\circ$ above the $+x$ axis. What is its $y$-component?",
        Ay, [Ax, A * math.tan(rad(th)), A / math.sin(rad(th)), A * math.sin(th)], "m",
        ex("$A_y=A\\sin\\theta=12.0\\sin35^\\circ=%s\\,\\mathrm{m}$; the cosine gives the $x$-component, $A_x=%s\\,\\mathrm{m}$." % (sci(Ay), sci(Ax)),
           "Check: $\\sqrt{A_x^2+A_y^2}=12.0\\,\\mathrm{m}$. (Calculator in radian mode would give $\\sin35=-0.43$: always check the mode.)"))
    ang = math.degrees(math.atan2(4.0, -3.0)); q4 = math.degrees(math.atan(4.0 / -3.0))
    check(ang, q4 + 180.0)
    num(B, c, t, 2, "The vector $\\vec A=-3.0\\,\\hat i+4.0\\,\\hat j$ (in metres) has magnitude $5.0\\,\\mathrm{m}$. What angle does it make with the $+x$ axis, measured counter-clockwise?",
        ang, [q4, 53.13, 36.87, 233.13], "deg",
        ex("$\\tan^{-1}(4.0/(-3.0))=-53.1^\\circ$ lies in the fourth quadrant, but $\\vec A$ points into the second quadrant (negative $x$, positive $y$).",
           "Add $180^\\circ$: $\\theta=%s^\\circ$." % sci(ang)))
    a, b = (2.0, -3.0, 1.0), (4.0, 0.0, 5.0)
    d = sum(x * y for x, y in zip(a, b)); check(d, 13.0)
    num(B, c, t, 1, "For $\\vec a=2\\hat i-3\\hat j+\\hat k$ and $\\vec b=4\\hat i+5\\hat k$, what is $\\vec a\\cdot\\vec b$?",
        d, [8.0, 14.0, 3.0, math.sqrt(14 * 41)], "",
        ex("$\\vec a\\cdot\\vec b=a_xb_x+a_yb_y+a_zb_z=(2)(4)+(-3)(0)+(1)(5)=%s$." % sci(d), "The result is a number (a scalar), not a vector."))
    cs = 24.0 / 25.0; thab = math.degrees(math.acos(cs))
    check(thab, math.degrees(math.atan2(4, 3) - math.atan2(3, 4)))
    num(B, c, t, 2, "What is the angle between $\\vec a=3\\hat i+4\\hat j$ and $\\vec b=4\\hat i+3\\hat j$?",
        thab, [math.degrees(math.asin(cs)), math.degrees(math.atan(cs)), 36.87, 53.13], "deg",
        ex("$\\cos\\theta=\\dfrac{\\vec a\\cdot\\vec b}{|\\vec a||\\vec b|}=\\dfrac{12+12}{5\\times5}=0.96\\Rightarrow\\theta=%s^\\circ$." % sci(thab),
           "Check with the directions: $53.1^\\circ-36.9^\\circ=16.3^\\circ$."))
    p = 2.0; check(2 * 3 + p * (-4) + 1 * 2, 0.0)
    num(B, c, t, 2, "For what value of $p$ are $\\vec a=2\\hat i+p\\hat j+\\hat k$ and $\\vec b=3\\hat i-4\\hat j+2\\hat k$ perpendicular?",
        p, [1.5, -2.0, 8.0, 0.5], "",
        ex("Perpendicular means $\\vec a\\cdot\\vec b=0$: $(2)(3)+(p)(-4)+(1)(2)=8-4p=0\\Rightarrow p=%s$." % sci(p),
           "Forgetting the $\\hat k$ term gives $p=1.5$; a sign slip gives $p=-2$."))
    Am, Bm = (3.0, 4.0), (-1.0, 2.0)
    S = (Am[0] + Bm[0], Am[1] + Bm[1]); mag = math.hypot(*S)
    check(mag, math.sqrt(math.hypot(*Am) ** 2 + math.hypot(*Bm) ** 2 + 2 * (Am[0] * Bm[0] + Am[1] * Bm[1])))
    num(B, c, t, 2, "Vectors $\\vec A=3\\hat i+4\\hat j$ and $\\vec B=-\\hat i+2\\hat j$. What is the magnitude of $\\vec A+\\vec B$?",
        mag, [math.hypot(*Am) + math.hypot(*Bm), math.sqrt(math.hypot(*Am) ** 2 + math.hypot(*Bm) ** 2), math.hypot(Am[0] - Bm[0], Am[1] - Bm[1]), 8.0], "",
        ex("Add component by component: $\\vec A+\\vec B=(3-1)\\hat i+(4+2)\\hat j=2\\hat i+6\\hat j$.", "$|\\vec A+\\vec B|=\\sqrt{2^2+6^2}=\\sqrt{40}=%s$. Magnitudes do NOT add: $|\\vec A|+|\\vec B|=7.24$ is only the largest possible value." % sci(mag)))
    txt(B, c, t, 1, "Which of these quantities is a scalar?", "The work $W=\\vec F\\cdot\\Delta\\vec r$", ["The momentum $m\\vec v$", "The displacement $\\Delta\\vec r$", "The acceleration $\\vec a$"],
        ex("The dot product of two vectors is a number: work (and power, energy) are scalars. Momentum, displacement and acceleration have a direction."))
    check(math.hypot(0.6, -0.8), 1.0)
    txt(B, c, t, 2, "A unit vector parallel to $\\vec v=6\\hat i-8\\hat j$ is", "$0.6\\,\\hat i-0.8\\,\\hat j$", ["$6\\,\\hat i-8\\,\\hat j$", "$\\dfrac{6\\hat i-8\\hat j}{14}$", "$0.8\\,\\hat i-0.6\\,\\hat j$"],
        ex("Divide by the MAGNITUDE $|\\vec v|=\\sqrt{6^2+8^2}=10$: $\\hat v=0.6\\hat i-0.8\\hat j$ (its length is 1).", "Dividing by $6+8=14$ or swapping the components does not give a vector of length 1 along $\\vec v$."))
    txt(B, c, t, 1, "Two non-zero vectors $\\vec A$ and $\\vec B$ satisfy $\\vec A\\cdot\\vec B=0$. The vectors are", "perpendicular to each other", ["parallel to each other", "antiparallel (opposite directions)", "equal in magnitude"],
        ex("$\\vec A\\cdot\\vec B=AB\\cos\\theta=0$ with $A,B\\neq0$ forces $\\cos\\theta=0$, so $\\theta=90^\\circ$."))
    Rx, Ry = 3.0 + 4.0 * math.cos(rad(60)), 4.0 * math.sin(rad(60)); R = math.hypot(Rx, Ry)
    check(R, math.sqrt(9 + 16 + 2 * 3 * 4 * math.cos(rad(60))))
    num(B, c, t, 3, "A hiker walks $3.0\\,\\mathrm{km}$ east and then $4.0\\,\\mathrm{km}$ in a direction $60^\\circ$ north of east. What is the magnitude of her displacement?",
        R, [7.0, 5.0, math.sqrt(9 + 16 - 2 * 3 * 4 * math.cos(rad(60)))], "km",
        ex("Components: $R_x=3.0+4.0\\cos60^\\circ=5.0\\,\\mathrm{km}$, $R_y=4.0\\sin60^\\circ=3.46\\,\\mathrm{km}$.", "$|R|=\\sqrt{5.0^2+3.46^2}=%s\\,\\mathrm{km}$. The $7.0\\,\\mathrm{km}$ is the distance walked, not the displacement." % sci(R)))

# =============================================================================================== chapter 2
def springs(B):
    c, t = "c2", "Hooke's law and springs"
    k, x = 250.0, 0.12; F = k * x
    num(B, c, t, 1, "A spring of constant $250\\,\\mathrm{N/m}$ is stretched $0.12\\,\\mathrm{m}$ beyond its natural length. What force does it exert?",
        F, [0.5 * k * x, 0.5 * k * x * x, k * x * x, k / x], "N",
        ex("Hooke's law: $F=kx=(250)(0.12)=%s\\,\\mathrm{N}$." % sci(F), "$\\tfrac12kx^2=1.8\\,\\mathrm{J}$ is the stored ENERGY, not a force."))
    F2, x2 = 4.0, 0.050; k2 = F2 / x2
    num(B, c, t, 1, "A force of $4.0\\,\\mathrm{N}$ stretches a spring by $5.0\\,\\mathrm{cm}$. What is the spring constant?",
        k2, [F2 / 5.0, F2 * x2, 2 * k2, F2 / x2 ** 2], "N/m",
        ex("Convert first: $5.0\\,\\mathrm{cm}=0.050\\,\\mathrm{m}$.", "$k=\\dfrac Fx=\\dfrac{4.0}{0.050}=%s\\,\\mathrm{N/m}$." % sci(k2, 2)), sig=2)
    m, xe = 0.50, 0.049; k3 = m * G / xe
    check(k3, 100.0)
    num(B, c, t, 2, "A $0.50\\,\\mathrm{kg}$ mass hangs at rest from a vertical spring and stretches it by $4.9\\,\\mathrm{cm}$ ($g=9.8\\,\\mathrm{m/s^2}$). What is the spring constant?",
        k3, [m / xe, m * G * xe, 2 * k3, m * G / 4.9], "N/m",
        ex("At equilibrium the spring force balances the weight: $kx=mg$.", "$k=\\dfrac{mg}{x}=\\dfrac{(0.50)(9.8)}{0.049}=%s\\,\\mathrm{N/m}$." % sci(k3)))
    k1_, k2_ = 200.0, 300.0
    num(B, c, t, 2, "Two springs, $k_1=200\\,\\mathrm{N/m}$ and $k_2=300\\,\\mathrm{N/m}$, are attached side by side (in parallel) between a wall and the same block. What is the equivalent spring constant?",
        k1_ + k2_, [1 / (1 / k1_ + 1 / k2_), (k1_ + k2_) / 2, k2_ - k1_], "N/m",
        ex("In parallel both springs stretch by the same amount and their forces add: $k_{eq}=k_1+k_2=%s\\,\\mathrm{N/m}$." % sci(k1_ + k2_)))
    ks = 1 / (1 / k1_ + 1 / k2_); check(ks, k1_ * k2_ / (k1_ + k2_))
    num(B, c, t, 2, "Two springs, $k_1=200\\,\\mathrm{N/m}$ and $k_2=300\\,\\mathrm{N/m}$, are joined end to end (in series) and pulled. What is the equivalent spring constant?",
        ks, [k1_ + k2_, (k1_ + k2_) / 2, math.sqrt(k1_ * k2_)], "N/m",
        ex("In series the same force acts on both and the extensions add: $\\dfrac1{k_{eq}}=\\dfrac1{k_1}+\\dfrac1{k_2}$.", "$k_{eq}=\\dfrac{k_1k_2}{k_1+k_2}=\\dfrac{200\\times300}{500}=%s\\,\\mathrm{N/m}$ - softer than either spring." % sci(ks)))
    txt(B, c, t, 3, "A spring of constant $k$ is cut into two equal halves. What is the spring constant of each half?", "$2k$", ["$k/2$", "$k$", "$4k$"],
        ex("Two identical halves joined in series must give the original spring: $\\dfrac{k'}{2}=k$, so $k'=2k$.", "A shorter piece of the same wire is stiffer: it needs twice the force for the same extension."))
    m4, k4, x4 = 0.40, 100.0, 0.10; a4 = k4 * x4 / m4
    check(a4, 25.0)
    num(B, c, t, 2, "A $0.40\\,\\mathrm{kg}$ block on a smooth horizontal table is attached to a spring ($k=100\\,\\mathrm{N/m}$) that is stretched $0.10\\,\\mathrm{m}$ and then released. What is the block's acceleration at the moment of release?",
        a4, [k4 * x4, k4 * x4 * m4, k4 / m4, k4 * x4 * x4 / (2 * m4)], "m/s^2",
        ex("The spring force is the only horizontal force: $F=kx=(100)(0.10)=10\\,\\mathrm{N}$.", "$a=\\dfrac Fm=\\dfrac{10}{0.40}=%s\\,\\mathrm{m/s^2}$ (a force is not an acceleration: divide by the mass)." % sci(a4)))
    for xs, Fs in [((2.0, 4.0, 6.0, 8.0), (1.5, 3.0, 4.5, 6.0))]:
        ratios = [f / (xx / 100) for xx, f in zip(xs, Fs)]; check(min(ratios), max(ratios))
    txt(B, c, t, 2, "A spring is stretched and the force is measured: $x=2.0,\\ 4.0,\\ 6.0,\\ 8.0\\,\\mathrm{cm}$ gives $F=1.5,\\ 3.0,\\ 4.5,\\ 6.0\\,\\mathrm{N}$. Does the spring obey Hooke's law, and what is $k$?",
        "Yes, $k=75\\,\\mathrm{N/m}$", ["Yes, $k=0.75\\,\\mathrm{N/m}$", "Yes, $k=1.5\\,\\mathrm{N/m}$", "No: $F$ is not proportional to $x$"],
        ex("$F/x$ is the same for every pair: $\\dfrac{1.5}{0.020}=\\dfrac{3.0}{0.040}=\\dots=75\\,\\mathrm{N/m}$, so $F\\propto x$ (Hooke's law).", "Use metres: with $x$ in cm the number would be $0.75\\,\\mathrm{N/cm}$, not $\\mathrm{N/m}$."))
    txt(B, c, t, 2, "Spring A has twice the spring constant of spring B. The same force pulls on each. The extension of A compared with that of B is", "half as large", ["twice as large", "the same", "four times as large"],
        ex("$x=F/k$: doubling $k$ at fixed $F$ halves the extension. A stiffer spring stretches less."))
    m5, k5 = 2.0, 400.0; keff = k5 / 2; x5 = m5 * G / keff
    check(x5, m5 * G / k5 + m5 * G / k5)
    num(B, c, t, 3, "A $2.0\\,\\mathrm{kg}$ mass hangs from two identical springs ($k=400\\,\\mathrm{N/m}$ each) joined end to end (in series), the upper one fixed to the ceiling. What is the total extension? ($g=9.8\\,\\mathrm{m/s^2}$)",
        x5, [m5 * G / k5, m5 * G / (2 * k5), 2 * m5 * G / k5 * 2, m5 * G / (k5 * 10)], "m",
        ex("Each spring carries the full weight $mg=19.6\\,\\mathrm{N}$ and stretches $\\dfrac{mg}{k}=0.049\\,\\mathrm{m}$.", "The extensions add: $x=2\\times0.049=%s\\,\\mathrm{m}$ (equivalently $k_{eq}=200\\,\\mathrm{N/m}$ and $x=mg/k_{eq}$)." % sci(x5)))

# =============================================================================================== chapter 3
def conservative(B):
    c, t = "c3", "Conservative forces"
    txt(B, c, t, 1, "Which of the following forces is NOT conservative?", "Kinetic friction", ["The weight $m\\vec g$ of a body near the Earth", "The force of an ideal spring", "The gravitational attraction between two planets"],
        ex("Gravity and the ideal spring do work that depends only on the end points (a potential energy exists). The work of kinetic friction depends on the length of the path and is always negative along the motion: it turns mechanical energy into heat."))
    txt(B, c, t, 1, "The work done by a conservative force on a particle that moves around any closed path and returns to its starting point is", "zero", ["always positive", "equal to the kinetic energy of the particle", "equal to the maximum potential energy along the path"],
        ex("For a conservative force $W=-\\Delta U$ and $\\Delta U=0$ when the particle returns to the same point, so $W=0$ - whatever the path."))
    m, h = 2.0, 1.5; Wg = -m * G * h
    num(B, c, t, 2, "A $2.0\\,\\mathrm{kg}$ block is raised from the floor to a shelf $1.5\\,\\mathrm{m}$ high, once by lifting it straight up and once by pushing it up a smooth ramp. What work does gravity do on the block in either case? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Wg, [-Wg, 0.0, Wg / 2, 2 * Wg], "J",
        ex("Gravity is conservative: its work depends only on the height change, $W_g=-mg\\Delta h=-(2.0)(9.8)(1.5)=%s\\,\\mathrm{J}$, the same for both paths." % sci(Wg)))
    m2, mu, L = 3.0, 0.30, 6.0; Wf = -mu * m2 * G * L
    num(B, c, t, 2, "A $3.0\\,\\mathrm{kg}$ crate is dragged over a rough floor ($\\mu_k=0.30$) from point P to point Q along a curved path $6.0\\,\\mathrm{m}$ long. P and Q are $4.0\\,\\mathrm{m}$ apart. What work does friction do? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Wf, [-mu * m2 * G * 4.0, -Wf, 0.0, Wf / 3], "J",
        ex("Friction is not conservative: its work is $-\\mu_kmg\\times(\\text{path length})=-(0.30)(3.0)(9.8)(6.0)=%s\\,\\mathrm{J}$." % sci(Wf), "Using the straight-line distance $4.0\\,\\mathrm{m}$ (giving $-35.3\\,\\mathrm{J}$) is the typical error: the path, not the displacement, counts."))
    m3, h3, Wnc = 2.0, 1.5, -12.0
    K = m3 * G * h3 + Wnc; v = math.sqrt(2 * K / m3); check(0.5 * m3 * v * v, m3 * G * h3 + Wnc)
    num(B, c, t, 2, "A $2.0\\,\\mathrm{kg}$ block slides from rest down a rough incline and drops a vertical height of $1.5\\,\\mathrm{m}$. Friction does $-12\\,\\mathrm{J}$ of work. What is its speed at the bottom? ($g=9.8\\,\\mathrm{m/s^2}$)",
        v, [math.sqrt(2 * G * h3), math.sqrt(2 * (m3 * G * h3 - Wnc) / m3), K / m3, math.sqrt(-Wnc)], "m/s",
        ex("Work-energy theorem: $\\tfrac12mv^2=mgh+W_f=29.4-12=17.4\\,\\mathrm{J}$.", "$v=\\sqrt{\\dfrac{2(17.4)}{2.0}}=%s\\,\\mathrm{m/s}$ (without friction it would be $5.42\\,\\mathrm{m/s}$)." % sci(v)))
    k4, x1, x2 = 200.0, 0.10, 0.30; Ws = 0.5 * k4 * (x1 ** 2 - x2 ** 2)
    check(Ws, -sum(k4 * (x1 + (x2 - x1) * (i + 0.5) / 2000) * (x2 - x1) / 2000 for i in range(2000)), 1e-6)
    num(B, c, t, 2, "A spring ($k=200\\,\\mathrm{N/m}$) is stretched from $x_1=0.10\\,\\mathrm{m}$ to $x_2=0.30\\,\\mathrm{m}$. How much work does the spring force do?",
        Ws, [-Ws, 0.5 * k4 * (x2 - x1) ** 2, k4 * (x2 - x1), -0.5 * k4 * (x2 - x1) ** 2], "J", sig=2,
        explain=ex("$W_{spring}=\\tfrac12k(x_1^2-x_2^2)=\\tfrac12(200)(0.10^2-0.30^2)=%s\\,\\mathrm{J}$." % sci(Ws, 2), "Negative: the spring pulls back while it is stretched. $\\tfrac12k(\\Delta x)^2$ would be wrong because the force grows with $x$."))
    U = lambda x: 3 * x * x - 2 * x
    Fx = -(U(2.001) - U(1.999)) / 0.002; check(Fx, -(6 * 2 - 2.0), 1e-6)
    num(B, c, t, 3, "A particle moves along the $x$ axis with potential energy $U(x)=3x^2-2x$ (SI units). What is the force on it at $x=2\\,\\mathrm{m}$?",
        -10.0, [10.0, -8.0, -14.0, 8.0], "N",
        ex("$F=-\\dfrac{dU}{dx}=-(6x-2)$, so at $x=2$: $F=-(12-2)=-10\\,\\mathrm{N}$ (towards $-x$).", "$U(2)=8\\,\\mathrm{J}$ is the energy, not the force; the sign comes from the minus in $F=-dU/dx$."))
    m5, mu5, d5 = 4.0, 0.25, 2.0; Wrt = -mu5 * m5 * G * 2 * d5
    num(B, c, t, 3, "A $4.0\\,\\mathrm{kg}$ block is pushed $2.0\\,\\mathrm{m}$ along a rough table ($\\mu_k=0.25$) and then pulled back to its starting point. What is the total work done by friction on the round trip? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Wrt, [0.0, Wrt / 2, -Wrt, 2 * Wrt], "J",
        ex("Friction opposes the motion on both legs, so its work is negative each time: $W=-\\mu_kmg(d+d)=-(0.25)(4.0)(9.8)(4.0)=%s\\,\\mathrm{J}$." % sci(Wrt), "For a conservative force the round trip would give zero; for friction it never does."))
    txt(B, c, t, 3, "A block slides from the same height down a smooth ramp and, in a second trial, down a rough ramp. Which statement is correct?",
        "Mechanical energy is conserved only on the smooth ramp", ["Mechanical energy is conserved on both ramps", "The kinetic energy at the bottom is the same on both ramps", "Gravity does more work on the smooth ramp"],
        ex("Gravity does the same work on both (same height drop). On the rough ramp friction removes mechanical energy, so the block arrives with less kinetic energy and $E_{mech}$ is not conserved."))
    mb, hb = 0.50, 10.0
    num(B, c, t, 1, "A $0.50\\,\\mathrm{kg}$ ball is thrown straight up from the ground, reaches a maximum height of $10\\,\\mathrm{m}$ and falls back to the ground. What is the total work done by gravity during the whole flight? ($g=9.8\\,\\mathrm{m/s^2}$)",
        0.0, [-mb * G * hb, mb * G * hb, 2 * mb * G * hb], "J",
        ex("Going up gravity does $-mgh=-49\\,\\mathrm{J}$, coming down $+mgh=+49\\,\\mathrm{J}$: the total is $0$ because gravity is conservative and the ball returns to its starting height."))

def impulse(B):
    c, t = "c3", "Impulse"
    pts = [(0, 0), (10, 600), (20, 0)]
    J = 0.5 * 20e-3 * 600.0; check(J, 6.0)
    fig = figs.graph_vt(pts, "t (ms)", "F (N)", "force-time graph of a collision: the force rises linearly from 0 to 600 N in 10 ms and falls back to 0 at 20 ms").svg()
    num(B, c, t, 2, "The graph shows the force that a bat exerts on a ball during a collision. What impulse does the ball receive?",
        J, [20e-3 * 600.0, 0.5 * 20.0 * 600.0, 0.5 * J, 0.1 * J], "N s", fig=fig,
        explain=ex("Impulse = area under the $F$-$t$ graph = $\\tfrac12(\\text{base})(\\text{height})=\\tfrac12(20\\times10^{-3}\\,\\mathrm{s})(600\\,\\mathrm{N})=%s\\,\\mathrm{N\\,s}$." % sci(J), "Convert milliseconds to seconds first; the rectangle $20\\,\\mathrm{ms}\\times600\\,\\mathrm{N}$ would double the area."))
    m, v, dt = 0.15, 30.0, 5.0e-3; Fav = m * v / dt
    num(B, c, t, 2, "A $0.15\\,\\mathrm{kg}$ ball moving at $30\\,\\mathrm{m/s}$ is brought to rest by a catcher's glove in $5.0\\,\\mathrm{ms}$. What is the average force on the ball?",
        Fav, [m * v / 5.0, 2 * Fav, m * v * v / dt, m * v * dt], "N",
        ex("$\\bar F\\,\\Delta t=\\Delta p\\Rightarrow\\bar F=\\dfrac{mv}{\\Delta t}=\\dfrac{(0.15)(30)}{5.0\\times10^{-3}}=%s\\,\\mathrm{N}$." % sci(Fav), "Use seconds ($5.0\\,\\mathrm{ms}=0.0050\\,\\mathrm{s}$); a long stopping time would make the force much smaller."))
    mb, v1, v2 = 0.50, 8.0, 6.0; Jr = mb * (v1 + v2)
    num(B, c, t, 2, "A $0.50\\,\\mathrm{kg}$ ball hits a wall at $8.0\\,\\mathrm{m/s}$ and rebounds along the same line at $6.0\\,\\mathrm{m/s}$. What is the magnitude of the impulse of the wall on the ball?",
        Jr, [mb * (v1 - v2), mb * v1, mb * v2, 2 * Jr], "N s",
        ex("Take the rebound direction as positive: $J=\\Delta p=m[v_2-(-v_1)]=0.50(6.0+8.0)=%s\\,\\mathrm{N\\,s}$. The velocity reverses, so the speeds ADD." % sci(Jr)))
    txt(B, c, t, 2, "Why does bending the knees when landing from a jump reduce the force on the legs?", "It lengthens the stopping time, so the same change of momentum needs a smaller average force",
        ["It reduces the change of momentum of the body", "It reduces the weight of the body", "It makes the impulse on the body larger"],
        ex("The change of momentum is fixed by the landing speed. $\\bar F=\\Delta p/\\Delta t$: a longer $\\Delta t$ gives a smaller $\\bar F$ (the same reason air bags and crumple zones work)."))
    Fc, mc, tc = 12.0, 3.0, 2.5; vc = Fc * tc / mc
    num(B, c, t, 2, "A constant net force of $12\\,\\mathrm{N}$ acts for $2.5\\,\\mathrm{s}$ on a $3.0\\,\\mathrm{kg}$ cart that starts from rest. What is the final speed?",
        vc, [Fc * tc, Fc / mc, Fc * tc * mc, vc / 2], "m/s",
        ex("$J=F\\Delta t=\\Delta p=mv\\Rightarrow v=\\dfrac{F\\Delta t}{m}=\\dfrac{(12)(2.5)}{3.0}=%s\\,\\mathrm{m/s}$." % sci(vc), "Without dividing by the mass you would get the impulse ($30\\,\\mathrm{N\\,s}$), not the speed."))
    N = 4000; Jint = sum(8.0 * (3.0 * (i + 0.5) / N) * (3.0 / N) for i in range(N)); check(Jint, 4.0 * 3.0 ** 2, 1e-6)
    num(B, c, t, 3, "A force $F(t)=8.0\\,t$ (in newtons, $t$ in seconds) acts on a $2.0\\,\\mathrm{kg}$ body that starts from rest, from $t=0$ to $t=3.0\\,\\mathrm{s}$. What is the body's momentum at $t=3.0\\,\\mathrm{s}$?",
        36.0, [72.0, 24.0, 18.0, 12.0], "kg m/s",
        ex("$p=\\int_0^{3}F\\,dt=\\int_0^{3}8.0\\,t\\,dt=4.0\\,t^2\\Big|_0^3=%s\\,\\mathrm{kg\\,m/s}$." % sci(Jint), "Using the final force times the time ($24\\times3=72$) overestimates because the force grows from 0; $18\\,\\mathrm{m/s}$ is the speed ($p/m$), not the momentum."))
    mA, mB = 4.0, 1.0; ratio = math.sqrt(mA / mB); check(ratio, math.sqrt(2 * mA * 100.0) / math.sqrt(2 * mB * 100.0))
    num(B, c, t, 3, "Two carts have the same kinetic energy. Cart A has four times the mass of cart B. What is the ratio $p_A/p_B$ of their momenta?",
        ratio, [4.0, 0.5, 1.0, 16.0], "",
        ex("$K=\\dfrac{p^2}{2m}\\Rightarrow p=\\sqrt{2mK}$, so $\\dfrac{p_A}{p_B}=\\sqrt{\\dfrac{m_A}{m_B}}=\\sqrt4=%s$." % sci(ratio), "Equal kinetic energy does not mean equal momentum: the heavier cart has more momentum but moves more slowly."))

def connected(B):
    c, t = "c2", "Pulleys and connected bodies"
    m1, m2 = 2.0, 3.0; a = (m2 - m1) * G / (m1 + m2); T = 2 * m1 * m2 * G / (m1 + m2)
    check(T, m1 * (G + a)); check(T, m2 * (G - a))
    num(B, c, t, 2, "An ideal Atwood machine has masses $2.0\\,\\mathrm{kg}$ and $3.0\\,\\mathrm{kg}$ on a light string over a frictionless pulley. What is the magnitude of the acceleration? ($g=9.8\\,\\mathrm{m/s^2}$)",
        a, [G, m2 * G / (m1 + m2), (m2 - m1) * G / m2, a / 2], "m/s^2",
        ex("Newton's second law for each mass: $m_2g-T=m_2a$ and $T-m_1g=m_1a$.", "Adding: $a=\\dfrac{(m_2-m_1)g}{m_1+m_2}=\\dfrac{(1.0)(9.8)}{5.0}=%s\\,\\mathrm{m/s^2}$." % sci(a)))
    num(B, c, t, 2, "For the same Atwood machine ($2.0\\,\\mathrm{kg}$ and $3.0\\,\\mathrm{kg}$), what is the tension in the string? ($g=9.8\\,\\mathrm{m/s^2}$)",
        T, [m2 * G, m1 * G, (m1 + m2) * G / 2, T / 2], "N",
        ex("From the lighter mass: $T=m_1(g+a)=2.0(9.8+1.96)=%s\\,\\mathrm{N}$ (check with the heavier mass: $T=m_2(g-a)=3.0(9.8-1.96)$)." % sci(T), "The tension lies between the two weights ($19.6\\,\\mathrm{N}$ and $29.4\\,\\mathrm{N}$)."))
    M, mh = 4.0, 1.0; ah = mh * G / (M + mh); Th = M * ah; check(Th, mh * (G - ah))
    num(B, c, t, 2, "A $4.0\\,\\mathrm{kg}$ block on a frictionless table is joined by a light string over a pulley to a hanging $1.0\\,\\mathrm{kg}$ mass. What is the acceleration of the blocks? ($g=9.8\\,\\mathrm{m/s^2}$)",
        ah, [G, mh * G / M, M * G / (M + mh), ah / 2], "m/s^2",
        ex("Only the hanging weight drives the motion but BOTH masses accelerate: $m_hg=(M+m_h)a$.", "$a=\\dfrac{(1.0)(9.8)}{5.0}=%s\\,\\mathrm{m/s^2}$." % sci(ah)))
    num(B, c, t, 2, "In the previous set-up (a $4.0\\,\\mathrm{kg}$ block on a frictionless table, a hanging $1.0\\,\\mathrm{kg}$ mass), what is the tension in the string? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Th, [mh * G, ah, M * G, 0.6 * Th], "N",
        ex("The tension is the only horizontal force on the table block: $T=Ma=(4.0)(1.96)=%s\\,\\mathrm{N}$." % sci(Th), "It is smaller than the hanging weight $m_hg=9.8\\,\\mathrm{N}$ because the hanging mass is accelerating downwards."))
    mu = 0.20; af = (mh * G - mu * M * G) / (M + mh); Tf = M * (af + mu * G)
    check(mh * G - Tf, mh * af)
    num(B, c, t, 3, "The $4.0\\,\\mathrm{kg}$ block of the previous problem now slides on a table with kinetic friction coefficient $\\mu_k=0.20$ (hanging mass $1.0\\,\\mathrm{kg}$). What is the acceleration? ($g=9.8\\,\\mathrm{m/s^2}$)",
        af, [ah, (mh * G + mu * M * G) / (M + mh), 0.0, (mh * G - mu * M * G) / M], "m/s^2",
        ex("Table block: $T-\\mu_kMg=Ma$. Hanging block: $m_hg-T=m_ha$.", "Adding: $a=\\dfrac{m_hg-\\mu_kMg}{M+m_h}=\\dfrac{9.8-7.84}{5.0}=%s\\,\\mathrm{m/s^2}$. Friction acts only on the block that touches the table." % sci(af)))
    Fp, ma, mb = 10.0, 2.0, 3.0; ac = Fp / (ma + mb); Nc = mb * ac
    num(B, c, t, 3, "Blocks of $2.0\\,\\mathrm{kg}$ and $3.0\\,\\mathrm{kg}$ touch each other on a smooth floor. A horizontal force of $10\\,\\mathrm{N}$ pushes the $2.0\\,\\mathrm{kg}$ block towards the $3.0\\,\\mathrm{kg}$ block. What force does the $2.0\\,\\mathrm{kg}$ block exert on the $3.0\\,\\mathrm{kg}$ block?",
        Nc, [Fp, ma * ac, Fp / 2, ac], "N",
        ex("Both blocks move together: $a=\\dfrac{F}{m_a+m_b}=\\dfrac{10}{5.0}=2.0\\,\\mathrm{m/s^2}$.", "The $3.0\\,\\mathrm{kg}$ block is accelerated only by the contact force: $N=m_ba=(3.0)(2.0)=%s\\,\\mathrm{N}$ (the other $4.0\\,\\mathrm{N}$ accelerates the $2.0\\,\\mathrm{kg}$ block)." % sci(Nc)))
    mi, mhg, th = 3.0, 2.0, 30.0; ai = (mhg * G - mi * G * math.sin(rad(th))) / (mi + mhg); Ti = mhg * (G - ai)
    check(Ti - mi * G * math.sin(rad(th)), mi * ai)
    num(B, c, t, 3, "A $3.0\\,\\mathrm{kg}$ block on a smooth $30^\\circ$ incline is joined by a string over a pulley at the top to a hanging $2.0\\,\\mathrm{kg}$ mass. What is the acceleration of the system? ($g=9.8\\,\\mathrm{m/s^2}$)",
        ai, [mhg * G / (mi + mhg), (mhg * G + mi * G * math.sin(rad(th))) / (mi + mhg), (mhg * G - mi * G * math.sin(rad(th))) / mhg, (mhg * G - mi * G * math.sin(rad(th))) / mi], "m/s^2",
        ex("Only the component of the block's weight along the incline matters: $m_1g\\sin30^\\circ=14.7\\,\\mathrm{N}$.", "$a=\\dfrac{m_2g-m_1g\\sin\\theta}{m_1+m_2}=\\dfrac{19.6-14.7}{5.0}=%s\\,\\mathrm{m/s^2}$ (the hanging mass descends)." % sci(ai)))
    txt(B, c, t, 2, "In an ideal Atwood machine with unequal masses, the tension in the string is",
        "greater than the weight of the lighter mass and less than the weight of the heavier mass", ["equal to the weight of the heavier mass", "equal to the weight of the lighter mass", "equal to the sum of the two weights"],
        ex("The lighter mass accelerates upwards, so $T>m_1g$; the heavier mass accelerates downwards, so $T<m_2g$. Neither mass is in equilibrium, so the tension equals neither weight."))
    mA, mB, d = 5.0, 3.0, 2.0; aA = (mA - mB) * G / (mA + mB); vA = math.sqrt(2 * aA * d)
    check(0.5 * (mA + mB) * vA ** 2, (mA - mB) * G * d)
    num(B, c, t, 3, "The masses $5.0\\,\\mathrm{kg}$ and $3.0\\,\\mathrm{kg}$ hang from the ends of a rope over a frictionless pulley and are released from rest. What is their speed after the heavier mass has fallen $2.0\\,\\mathrm{m}$? ($g=9.8\\,\\mathrm{m/s^2}$)",
        vA, [math.sqrt(2 * G * d), math.sqrt(2 * (mA - mB) * G * d / mA), math.sqrt(aA * d), math.sqrt(2 * mA * G * d / (mA + mB))], "m/s",
        ex("Energy: the system loses $(m_A-m_B)gd=39.2\\,\\mathrm{J}$ of potential energy, shared as kinetic energy of BOTH masses: $\\tfrac12(m_A+m_B)v^2=39.2$.", "$v=\\sqrt{\\dfrac{2(39.2)}{8.0}}=%s\\,\\mathrm{m/s}$ (same result from $a=2.45\\,\\mathrm{m/s^2}$ and $v^2=2ad$)." % sci(vA)))

def weight(B):
    c, t = "c2", "Applications of Newton's laws"
    m = 60.0; a = 2.0
    num(B, c, t, 1, "A $60\\,\\mathrm{kg}$ person stands on a bathroom scale in an elevator that accelerates upward at $2.0\\,\\mathrm{m/s^2}$. What does the scale read? ($g=9.8\\,\\mathrm{m/s^2}$)",
        m * (G + a), [m * (G - a), m * G, m * a, m * (G + a) * 2], "N",
        ex("Newton's second law (up positive): $N-mg=ma\\Rightarrow N=m(g+a)=60(9.8+2.0)=%s\\,\\mathrm{N}$." % sci(m * (G + a)), "The scale reads the normal force, which is larger than the weight $mg=588\\,\\mathrm{N}$: you feel heavier."))
    num(B, c, t, 1, "The same $60\\,\\mathrm{kg}$ person is in an elevator that accelerates DOWNWARD at $2.0\\,\\mathrm{m/s^2}$. What does the scale read? ($g=9.8\\,\\mathrm{m/s^2}$)",
        m * (G - a), [m * (G + a), m * G, m * a, m * (G - a) / 2], "N",
        ex("$mg-N=ma\\Rightarrow N=m(g-a)=60(9.8-2.0)=%s\\,\\mathrm{N}$: the apparent weight is smaller than $mg$." % sci(m * (G - a))))
    txt(B, c, t, 2, "A person stands on a scale inside an elevator whose cable has snapped, so that it falls freely. The scale reads", "zero", ["the person's normal weight $mg$", "less than $mg$ but not zero", "twice the person's weight"],
        ex("In free fall $a=g$ downwards, so $N=m(g-a)=0$: the person is 'weightless' (the gravitational force is still $mg$, but nothing pushes back)."))
    mb, th = 5.0, 30.0; Nn = mb * G * math.cos(rad(th)); check(math.hypot(Nn, mb * G * math.sin(rad(th))), mb * G)
    num(B, c, t, 2, "A $5.0\\,\\mathrm{kg}$ block rests on a $30^\\circ$ incline. What is the normal force exerted by the incline? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Nn, [mb * G * math.sin(rad(th)), mb * G, mb * G * math.tan(rad(th)), mb * G * math.cos(rad(th)) / 2], "N",
        ex("Perpendicular to the incline there is no acceleration: $N=mg\\cos\\theta=(5.0)(9.8)\\cos30^\\circ=%s\\,\\mathrm{N}$." % sci(Nn), "$mg\\sin\\theta=24.5\\,\\mathrm{N}$ is the component ALONG the incline."))
    mk, T, ang = 2.0, 20.0, 30.0; Nr = mk * G - T * math.sin(rad(ang))
    num(B, c, t, 2, "A $2.0\\,\\mathrm{kg}$ book lies on a table and is pulled by a rope with tension $20\\,\\mathrm{N}$ directed $30^\\circ$ above the horizontal. What is the normal force from the table? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Nr, [mk * G, mk * G + T * math.sin(rad(ang)), mk * G - T * math.cos(rad(ang)), mk * G - T], "N",
        ex("Vertical forces balance: $N+T\\sin30^\\circ=mg\\Rightarrow N=19.6-20\\sin30^\\circ=19.6-10=%s\\,\\mathrm{N}$." % sci(Nr), "The upward part of the pull partly supports the book, so the table pushes less than $mg$."))
    mc, ac = 800.0, 1.5; Tc = mc * (G - ac)
    num(B, c, t, 3, "An $800\\,\\mathrm{kg}$ elevator is moving UP but slowing down at $1.5\\,\\mathrm{m/s^2}$. What is the tension in the cable? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Tc, [mc * (G + ac), mc * G, mc * ac, mc * (G - ac) * 2], "N",
        ex("Slowing down while moving up means the acceleration points DOWN: $a=-1.5\\,\\mathrm{m/s^2}$.", "$T-mg=ma\\Rightarrow T=m(g-1.5)=800(9.8-1.5)=%s\\,\\mathrm{N}$ (less than the weight $7840\\,\\mathrm{N}$)." % sci(Tc)))
    gm = 1.6
    txt(B, c, t, 1, "An astronaut has a mass of $75\\,\\mathrm{kg}$ on Earth. On the Moon ($g_M=1.6\\,\\mathrm{m/s^2}$) her mass and weight are",
        "$75\\,\\mathrm{kg}$ and $120\\,\\mathrm{N}$", ["$12\\,\\mathrm{kg}$ and $120\\,\\mathrm{N}$", "$75\\,\\mathrm{kg}$ and $735\\,\\mathrm{N}$", "$12\\,\\mathrm{kg}$ and $19\\,\\mathrm{N}$"],
        ex("Mass is a property of the body and does not change. Weight $=mg_M=(75)(1.6)=%s\\,\\mathrm{N}$ (on Earth it would be $735\\,\\mathrm{N}$)." % sci(75 * gm)))

# =============================================================================================== chapter 1 (definitions, graphs)
def kin_defs(B):
    c = "c1"
    t = "Speed and velocity"
    txt(B, c, "Displacement and distance", 1, "A runner completes exactly one lap of a $400\\,\\mathrm{m}$ circular track in $80\\,\\mathrm{s}$. The magnitude of her average velocity for the lap is",
        "$0\\,\\mathrm{m/s}$", ["$5.0\\,\\mathrm{m/s}$", "$2.5\\,\\mathrm{m/s}$", "$80\\,\\mathrm{m/s}$"],
        ex("Average velocity $=\\dfrac{\\text{displacement}}{\\text{time}}$ and she ends where she started: displacement $0$, so $\\bar v=0$.", "The AVERAGE SPEED is $\\dfrac{400\\,\\mathrm{m}}{80\\,\\mathrm{s}}=5.0\\,\\mathrm{m/s}$: distance, not displacement."))
    dsp = math.hypot(3.0, 4.0)
    num(B, c, "Displacement and distance", 1, "A hiker walks $3.0\\,\\mathrm{km}$ east and then $4.0\\,\\mathrm{km}$ north. What is the magnitude of her displacement?",
        dsp, [7.0, 1.0, 12.0, 3.5], "km",
        ex("The legs are perpendicular: $|\\Delta\\vec r|=\\sqrt{3.0^2+4.0^2}=%s\\,\\mathrm{km}$." % sci(dsp, 2), "The distance walked is $7.0\\,\\mathrm{km}$: distance adds, displacement is the straight line from start to finish."), sig=2)
    num(B, c, t, 1, "The hiker above ($3.0\\,\\mathrm{km}$ east, then $4.0\\,\\mathrm{km}$ north) takes $1.0\\,\\mathrm{h}$ in total. What is her average velocity, in magnitude?",
        dsp / 1.0, [7.0, 3.5, 1.4, 12.0], "km/h",
        ex("$|\\bar{\\vec v}|=\\dfrac{|\\Delta\\vec r|}{\\Delta t}=\\dfrac{5.0\\,\\mathrm{km}}{1.0\\,\\mathrm{h}}=%s\\,\\mathrm{km/h}$ (her average SPEED is $7.0\\,\\mathrm{km/h}$)." % sci(dsp, 2)), sig=2)
    d1 = 120.0; tt = 60.0 / 60.0 + 60.0 / 40.0; vavg = d1 / tt
    check(vavg, 2 * 60.0 * 40.0 / (60.0 + 40.0))
    num(B, c, t, 2, "A car covers the first half of a $120\\,\\mathrm{km}$ trip at $60\\,\\mathrm{km/h}$ and the second half at $40\\,\\mathrm{km/h}$. What is its average speed for the whole trip?",
        vavg, [50.0, math.sqrt(60.0 * 40.0), 100.0, 24.0], "km/h", sig=3,
        explain=ex("Average speed $=\\dfrac{\\text{total distance}}{\\text{total time}}$: $t_1=\\dfrac{60}{60}=1.0\\,\\mathrm{h}$, $t_2=\\dfrac{60}{40}=1.5\\,\\mathrm{h}$.", "$\\bar v=\\dfrac{120}{2.5}=%s\\,\\mathrm{km/h}$, not the arithmetic mean $50\\,\\mathrm{km/h}$ (the car spends MORE time at the lower speed)." % sci(vavg)))
    xt = lambda s: 2 * s ** 3 - 3 * s ** 2 + 4
    v2 = (xt(2.0 + 1e-6) - xt(2.0 - 1e-6)) / 2e-6; check(v2, 12.0, 1e-6)
    num(B, c, t, 2, "The position of a particle is $x(t)=2t^3-3t^2+4$ (SI units). What is its instantaneous velocity at $t=2.0\\,\\mathrm{s}$?",
        12.0, [(xt(2.0) - xt(0.0)) / 2.0, xt(2.0), 12 * 2.0 - 6.0, 24.0], "m/s",
        ex("$v=\\dfrac{dx}{dt}=6t^2-6t$, so $v(2)=24-12=%s\\,\\mathrm{m/s}$." % sci(v2, 3), "$\\dfrac{x(2)-x(0)}{2}=2.0\\,\\mathrm{m/s}$ is the AVERAGE velocity over $0$ to $2\\,\\mathrm{s}$; $12t-6=18$ is the acceleration."))
    txt(B, c, "Displacement and distance", 1, "A particle moves along the $x$ axis from $x=+5\\,\\mathrm{m}$ to $x=-3\\,\\mathrm{m}$. Its displacement and the distance travelled are",
        "$\\Delta x=-8\\,\\mathrm{m}$ and distance $8\\,\\mathrm{m}$", ["$\\Delta x=+8\\,\\mathrm{m}$ and distance $8\\,\\mathrm{m}$", "$\\Delta x=-8\\,\\mathrm{m}$ and distance $-8\\,\\mathrm{m}$", "$\\Delta x=+2\\,\\mathrm{m}$ and distance $8\\,\\mathrm{m}$"],
        ex("$\\Delta x=x_f-x_i=-3-5=-8\\,\\mathrm{m}$ (a signed quantity: towards $-x$). The distance is the length of the path, always positive: $8\\,\\mathrm{m}$."))
    txt(B, c, t, 2, "A ball is thrown straight up and returns to the thrower's hand $4.0\\,\\mathrm{s}$ later. Its average velocity during these $4.0\\,\\mathrm{s}$ is",
        "zero", ["$9.8\\,\\mathrm{m/s}$ upward", "$9.8\\,\\mathrm{m/s}$ downward", "$19.6\\,\\mathrm{m/s}$ upward"],
        ex("The displacement over the whole flight is zero (back at the hand), so the average velocity is zero even though the ball moved. Its average SPEED is $\\dfrac{39.2\\,\\mathrm{m}}{4.0\\,\\mathrm{s}}=9.8\\,\\mathrm{m/s}$."))
    dtot = 2 * 6.0; tt2 = (20 + 30) / 60.0; vr = dtot / tt2
    num(B, c, t, 2, "A student cycles $6.0\\,\\mathrm{km}$ to school in $20\\,\\mathrm{min}$ and returns along the same road in $30\\,\\mathrm{min}$. What is her average speed for the round trip?",
        vr, [(18.0 + 12.0) / 2, 18.0, 12.0, 6.0], "km/h",
        ex("Total distance $=12\\,\\mathrm{km}$, total time $=50\\,\\mathrm{min}=\\dfrac56\\,\\mathrm{h}$.", "$\\bar v=\\dfrac{12}{5/6}=%s\\,\\mathrm{km/h}$ (the mean of $18$ and $12$, which is $15\\,\\mathrm{km/h}$, is wrong: the legs take different times)." % sci(vr)))

def graphs(B):
    c, t = "c1", "Graphs of motion"
    pts = [(0, 0), (4, 8), (10, 8), (12, 0)]
    area = 0.5 * 4 * 8 + 6 * 8 + 0.5 * 2 * 8; check(area, 0.5 * (12 + 6) * 8)
    fig = figs.graph_vt(pts, "t (s)", "v (m/s)", "velocity-time graph: rises linearly from 0 to 8 m/s in 4 s, stays at 8 m/s until 10 s, then falls to 0 at 12 s").svg()
    num(B, c, t, 2, "The velocity-time graph of a particle moving along a straight line is shown. How far does it travel between $t=0$ and $t=12\\,\\mathrm{s}$?",
        area, [12 * 8.0, 48.0, 36.0, 8.0], "m", fig=fig,
        explain=ex("Displacement = area under the $v$-$t$ graph: a trapezoid with parallel sides $12\\,\\mathrm{s}$ and $6\\,\\mathrm{s}$ and height $8\\,\\mathrm{m/s}$.", "Area $=\\tfrac12(12+6)(8)=%s\\,\\mathrm{m}$ (triangle $16$ + rectangle $48$ + triangle $8$)." % sci(area)))
    pts2 = [(0, 0), (2, 6), (5, 6), (8, 0)]
    slope = (0 - 6.0) / (8 - 5.0)
    fig2 = figs.graph_vt(pts2, "t (s)", "x (m)", "position-time graph: x rises from 0 to 6 m in 2 s, stays at 6 m until 5 s, then falls back to 0 at 8 s").svg()
    num(B, c, t, 2, "The position-time graph of a particle is shown. What is its velocity at $t=6.5\\,\\mathrm{s}$?",
        slope, [-slope, 0.0, 3.0, -6.0], "m/s", fig=fig2,
        explain=ex("Velocity = slope of the $x$-$t$ graph. Between $5\\,\\mathrm{s}$ and $8\\,\\mathrm{s}$ the line goes from $6\\,\\mathrm{m}$ to $0$: slope $=\\dfrac{0-6}{8-5}=%s\\,\\mathrm{m/s}$." % sci(slope), "The sign is negative: the particle is moving back towards the origin."))
    pts3 = [(0, 2), (3, 2), (3, -1), (5, -1)]
    dv = 2 * 3 + (-1) * 2
    fig3 = figs.graph_vt(pts3, "t (s)", "a (m/s^2)", "acceleration-time graph: a = +2 m/s^2 from 0 to 3 s, then a = -1 m/s^2 from 3 to 5 s").svg()
    num(B, c, t, 3, "A particle starts from rest. Its acceleration-time graph is shown. What is its speed at $t=5\\,\\mathrm{s}$?",
        dv, [6.0, 2.0, 2.5, -1.0], "m/s", fig=fig3,
        explain=ex("Change of velocity = area under the $a$-$t$ graph: $(2)(3)+(-1)(2)=6-2=%s\\,\\mathrm{m/s}$." % sci(dv), "Starting from rest, the velocity at $5\\,\\mathrm{s}$ equals this change."))
    txt(B, c, t, 1, "On a velocity-time graph, the slope of the curve at a given instant represents", "the acceleration at that instant", ["the displacement up to that instant", "the speed at that instant", "the distance travelled up to that instant"],
        ex("Slope of $v(t)$ is $dv/dt=a$. The AREA under the graph gives the displacement."))
    pts4 = [(0, 0), (2, 6), (4, 0), (6, -6), (8, 0)]
    up, down = 0.5 * 4 * 6, -0.5 * 4 * 6
    fig4 = figs.graph_vt(pts4, "t (s)", "v (m/s)", "velocity-time graph: up to 6 m/s at 2 s, back to 0 at 4 s, down to -6 m/s at 6 s, back to 0 at 8 s").svg()
    num(B, c, t, 3, "A particle moves along a line with the velocity-time graph shown. What is its displacement between $t=0$ and $t=8\\,\\mathrm{s}$?",
        up + down, [24.0, 12.0, -12.0, 48.0], "m", fig=fig4,
        explain=ex("Areas above the axis count positive, below negative: $+12\\,\\mathrm{m}$ (0 to 4 s) and $-12\\,\\mathrm{m}$ (4 to 8 s).", "Displacement $=12-12=%s\\,\\mathrm{m}$: the particle ends where it started." % sci(up + down)))
    num(B, c, t, 3, "For the same graph (velocity up to $+6\\,\\mathrm{m/s}$ and back to zero by $4\\,\\mathrm{s}$, then down to $-6\\,\\mathrm{m/s}$ and back to zero by $8\\,\\mathrm{s}$), what total distance does the particle travel between $t=0$ and $t=8\\,\\mathrm{s}$?",
        up - down, [0.0, 12.0, 48.0, 36.0], "m", fig=fig4,
        explain=ex("Distance counts all areas as positive: $|{+12}|+|{-12}|=%s\\,\\mathrm{m}$." % sci(up - down), "Displacement ($0$) and distance ($24\\,\\mathrm{m}$) differ whenever the velocity changes sign."))

# =============================================================================================== chapter 5, 7 (heat)
def thermal(B):
    c, t = "c5", "Thermal expansion"
    al, L, dT = 12e-6, 30.0, 40.0; dL = al * L * dT
    num(B, c, t, 1, "A steel rail $30.0\\,\\mathrm{m}$ long ($\\alpha=12\\times10^{-6}\\,\\mathrm{K^{-1}}$) is heated by $40\\,\\mathrm{K}$. By how much does its length increase?",
        dL, [al * dT, 2 * dL, dL * 1000, al * L], "m",
        ex("$\\Delta L=\\alpha L\\,\\Delta T=(12\\times10^{-6})(30.0)(40)=%s\\,\\mathrm{m}$ ($14.4\\,\\mathrm{mm}$)." % sci(dL), "Keep the units of $L$: the result is in metres when $L$ is in metres."))
    A0, a2, dT2 = 2.00, 23e-6, 100.0; dA = 2 * a2 * A0 * dT2
    check(dA, A0 * ((1 + a2 * dT2) ** 2 - 1), 5e-3)          # first-order formula against the exact square: they differ at second order (about 0.1 %)
    num(B, c, t, 2, "A circular hole of area $2.00\\,\\mathrm{cm^2}$ is cut in an aluminium plate ($\\alpha=23\\times10^{-6}\\,\\mathrm{K^{-1}}$). The plate is heated by $100\\,\\mathrm{K}$. By how much does the area of the hole increase?",
        dA, [a2 * A0 * dT2, 3 * a2 * A0 * dT2, 100 * dA, dA / 2 * 0.5], "cm^2", sig=2,
        explain=ex("A hole expands exactly as if it were made of the plate material, and an area grows twice as fast as a length: $\\Delta A=2\\alpha A_0\\Delta T$.", "$\\Delta A=2(23\\times10^{-6})(2.00)(100)=%s\\,\\mathrm{cm^2}$." % sci(dA, 2)))
    txt(B, c, t, 2, "A glass flask is filled to the brim with ethanol and heated. Ethanol spills over because", "the volume expansion coefficient of ethanol is much larger than that of glass",
        ["the glass contracts when heated", "the mass of the ethanol increases", "the pressure inside the flask decreases"],
        ex("Both the liquid and the flask expand; the liquid expands far more ($\\beta_{ethanol}\\approx1.1\\times10^{-3}\\,\\mathrm{K^{-1}}$ against about $2.7\\times10^{-5}\\,\\mathrm{K^{-1}}$ for glass), so the excess volume overflows."))
    txt(B, c, t, 2, "A strip of brass ($\\alpha=19\\times10^{-6}\\,\\mathrm{K^{-1}}$) is bonded to a strip of steel ($\\alpha=12\\times10^{-6}\\,\\mathrm{K^{-1}}$) and heated. The strip bends so that",
        "the brass is on the outside (convex side) of the curve", ["the steel is on the outside (convex side) of the curve", "the strip stays straight", "the brass is on the inside (concave side) of the curve"],
        ex("Brass expands more, so it becomes the longer strip; the longer strip must lie on the outside of the curve. On cooling the bending reverses. This is how a bimetallic thermostat works."))
    dLt, Lc, ac = 1.0e-3, 2.000, 17e-6; dTc = dLt / (ac * Lc)
    num(B, c, t, 2, "By how many kelvin must a $2.000\\,\\mathrm{m}$ copper rod ($\\alpha=17\\times10^{-6}\\,\\mathrm{K^{-1}}$) be heated to lengthen by $1.0\\,\\mathrm{mm}$?",
        dTc, [dTc * 2, dTc / 2, dTc * 1000, dLt / ac], "K",
        ex("$\\Delta T=\\dfrac{\\Delta L}{\\alpha L}=\\dfrac{1.0\\times10^{-3}}{(17\\times10^{-6})(2.000)}=%s\\,\\mathrm{K}$." % sci(dTc), "Use the same unit for $\\Delta L$ and $L$ (both in metres)."))
    txt(B, c, t, 2, "A flat metal plate has a circular hole in it. When the plate is heated uniformly, the diameter of the hole",
        "increases, by the same fractional amount as any other length of the plate", ["decreases, because the metal expands into the hole", "stays the same", "increases, but by less than the outer dimensions of the plate"],
        ex("Thermal expansion scales every length of the body, including the empty space inside it, exactly as if the hole were made of the same metal (like enlarging a photograph).", "The hole therefore grows: $\\Delta d=\\alpha d\\,\\Delta T$, and its area grows by $2\\alpha A\\,\\Delta T$."))

def carnot(B):
    c, t = "c7", "Carnot engine"
    Th, Tc = 500.0, 300.0; eta = 1 - Tc / Th
    num(B, c, t, 1, "A Carnot engine operates between reservoirs at $500\\,\\mathrm{K}$ and $300\\,\\mathrm{K}$. What is its efficiency?",
        eta * 100, [Tc / Th * 100, (Th - Tc) / Tc * 100, (Th - Tc) / (Th + Tc) * 100, 80.0], "%", sig=3,
        explain=ex("$\\eta_C=1-\\dfrac{T_c}{T_h}=1-\\dfrac{300}{500}=0.40=%s\\%%$." % sci(eta * 100), "Temperatures must be in kelvin; $\\dfrac{T_h-T_c}{T_c}=67\\%$ would exceed what the formula allows for an engine (and is the refrigerator-type ratio)."))
    ThC, TcC = 227.0, 27.0; e2 = 1 - (TcC + 273.15) / (ThC + 273.15)
    num(B, c, t, 2, "A Carnot engine works between $227^\\circ\\mathrm{C}$ and $27^\\circ\\mathrm{C}$. What is its efficiency?",
        e2 * 100, [(1 - TcC / ThC) * 100, TcC / ThC * 100, (ThC - TcC) / (ThC + TcC) * 100, (TcC + 273.15) / (ThC + 273.15) * 100], "%", sig=3,
        explain=ex("Convert to kelvin: $T_h=500\\,\\mathrm{K}$, $T_c=300\\,\\mathrm{K}$.", "$\\eta=1-\\dfrac{300}{500}=%s\\%%$. With Celsius numbers the formula would give $88.1\\%%$, which is wrong." % sci(e2 * 100)))
    Qh = 1500.0; W = eta * Qh; Qc = Qh - W; check(Qc, Qh * Tc / Th)
    num(B, c, t, 2, "A Carnot engine between $500\\,\\mathrm{K}$ and $300\\,\\mathrm{K}$ absorbs $1500\\,\\mathrm{J}$ from the hot reservoir in each cycle. How much heat does it reject to the cold reservoir per cycle?",
        Qc, [W, Qh, Qh * Th / Tc, Qh * eta / 2], "J",
        ex("For a Carnot cycle $\\dfrac{Q_c}{Q_h}=\\dfrac{T_c}{T_h}$, so $Q_c=1500\\times\\dfrac{300}{500}=%s\\,\\mathrm{J}$." % sci(Qc), "Check by energy: $W=Q_h-Q_c=600\\,\\mathrm{J}$ and $\\eta=W/Q_h=0.40$ agrees with $1-T_c/T_h$."))
    Th2, Tc2 = 400.0, 300.0
    eA = 1 - Tc2 / (Th2 + 50); eB = 1 - (Tc2 - 50) / Th2
    txt(B, c, t, 3, "A Carnot engine works between $T_h=400\\,\\mathrm{K}$ and $T_c=300\\,\\mathrm{K}$. Which change improves the efficiency more: (A) raising $T_h$ by $50\\,\\mathrm{K}$, or (B) lowering $T_c$ by $50\\,\\mathrm{K}$?",
        "(B): the efficiency becomes $%s\\%%$ instead of $%s\\%%$" % (sci(eB * 100, 3), sci(eA * 100, 3)),
        ["(A): the efficiency becomes $%s\\%%$ instead of $%s\\%%$" % (sci(eA * 100, 3), sci(eB * 100, 3)), "Both give the same efficiency", "Neither changes the efficiency, only the work per cycle"],
        ex("Initially $\\eta=1-300/400=25\\%$.", "(A): $1-\\dfrac{300}{450}=%s\\%%$. (B): $1-\\dfrac{250}{400}=%s\\%%$." % (sci(eA * 100, 3), sci(eB * 100, 3)), "The same temperature difference helps more when it is taken off the cold side, because $T_c/T_h$ falls faster."))
    txt(B, c, t, 2, "An inventor claims an engine working between $400\\,\\mathrm{K}$ and $250\\,\\mathrm{K}$ with an efficiency of $45\\%$. The claim is",
        "impossible, because the Carnot limit is $37.5\\%$", ["possible, because the Carnot limit is $62.5\\%$", "possible if friction is removed completely", "impossible, because every engine has efficiency below $25\\%$"],
        ex("The maximum efficiency is the Carnot value $1-\\dfrac{250}{400}=0.375$. No engine between these reservoirs can exceed $37.5\\%$; $62.5\\%$ is $T_c/T_h$, the ratio that is often confused with it."))
    Kr = 250.0 / (300.0 - 250.0); check(Kr, 5.0)
    num(B, c, t, 3, "A Carnot refrigerator keeps its inside at $250\\,\\mathrm{K}$ in a room at $300\\,\\mathrm{K}$. What is its coefficient of performance?",
        Kr, [300.0 / 50.0, 50.0 / 250.0, 300.0 / 250.0, 50.0 / 300.0], "",
        ex("$K_C=\\dfrac{T_c}{T_h-T_c}=\\dfrac{250}{300-250}=%s$." % sci(Kr), "$\\dfrac{T_h}{T_h-T_c}=6$ is the coefficient of performance of a HEAT PUMP; $\\dfrac{T_h-T_c}{T_h}$ is the efficiency of an engine."))
    txt(B, c, t, 2, "A Carnot cycle consists of", "two isothermal and two adiabatic processes", ["two isothermal and two isobaric processes", "two isobaric and two isochoric processes", "two adiabatic and two isochoric processes"],
        ex("Isothermal expansion at $T_h$ (heat absorbed), adiabatic expansion down to $T_c$, isothermal compression at $T_c$ (heat rejected), adiabatic compression back to $T_h$. Heat is exchanged only along the isotherms."))
    txt(B, c, t, 3, "For one complete cycle of a Carnot engine, the total entropy change of the engine together with both reservoirs is", "zero", ["positive", "negative", "equal to $W/T_h$"],
        ex("The cycle is reversible: $\\Delta S_{gas}=0$ over a cycle and the reservoirs change by $-\\dfrac{Q_h}{T_h}+\\dfrac{Q_c}{T_c}=0$ because $\\dfrac{Q_c}{Q_h}=\\dfrac{T_c}{T_h}$. A real (irreversible) engine would give $\\Delta S>0$."))

# =============================================================================================== chapter 3, 4
def power(B):
    c, t = "c3", "Power"
    F, v = 800.0, 25.0; P = F * v
    num(B, c, t, 1, "A car moves at a constant $25\\,\\mathrm{m/s}$ against a total resistive force of $800\\,\\mathrm{N}$. What power must the engine deliver to the wheels?",
        P, [F / v, 0.5 * F * v, F * v * 10, F], "W", sig=2,
        explain=ex("At constant speed the driving force equals the resistance: $P=Fv=(800)(25)=%s\\,\\mathrm{W}$ ($20\\,\\mathrm{kW}$)." % sci(P, 2)))
    m, h, tt = 1200.0, 20.0, 16.0; Pl = m * G * h / tt
    num(B, c, t, 2, "A motor lifts a $1200\\,\\mathrm{kg}$ elevator car $20\\,\\mathrm{m}$ at constant speed in $16\\,\\mathrm{s}$. What is the minimum power output of the motor? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Pl, [m * G * tt / h, m * h / tt, m * G * h, m * G / tt], "W",
        ex("At constant speed the lifting force is the weight: $P=\\dfrac{W}{t}=\\dfrac{mgh}{t}=\\dfrac{(1200)(9.8)(20)}{16}=%s\\,\\mathrm{W}$." % sci(Pl)))
    eff = 0.75; Pin = Pl / eff
    num(B, c, t, 2, "The elevator motor of the previous problem delivers $1.47\\times10^4\\,\\mathrm{W}$ of useful power and has an efficiency of $75\\%$. What electrical power does it draw?",
        Pin, [Pl * eff, Pl, Pl * 2, Pl / eff / 2], "W",
        ex("$\\eta=\\dfrac{P_{out}}{P_{in}}\\Rightarrow P_{in}=\\dfrac{P_{out}}{\\eta}=\\dfrac{1.47\\times10^4}{0.75}=%s\\,\\mathrm{W}$ (the input is larger than the output)." % sci(Pin)))
    Eb = 100.0 * 10 * 3600.0
    num(B, c, t, 1, "A $100\\,\\mathrm{W}$ light bulb is switched on for $10$ hours. How much energy does it use?",
        Eb, [100.0 * 10, 100.0 * 10 * 60, 100.0 * 10 * 3.6, 3.6e3], "J", sig=2,
        explain=ex("$E=Pt=(100\\,\\mathrm{W})(10\\times3600\\,\\mathrm{s})=%s\\,\\mathrm{J}$ ($=1\\,\\mathrm{kWh}$)." % sci(Eb, 2), "Use seconds: $1\\,\\mathrm{h}=3600\\,\\mathrm{s}$."))
    mc, Fc = 2.0, 6.0; ac = Fc / mc; vc = ac * 4.0; Pinst = Fc * vc; Pavg = 0.5 * Pinst
    num(B, c, t, 2, "A constant force of $6.0\\,\\mathrm{N}$ accelerates a $2.0\\,\\mathrm{kg}$ object from rest. What power does the force deliver at $t=4.0\\,\\mathrm{s}$?",
        Pinst, [Pavg, Fc * 4.0, 2 * Pinst, Pinst / 4], "W", sig=2,
        explain=ex("$a=F/m=3.0\\,\\mathrm{m/s^2}$, so $v(4)=12\\,\\mathrm{m/s}$.", "Instantaneous power $P=Fv=(6.0)(12)=%s\\,\\mathrm{W}$. The AVERAGE power over the four seconds is only half of that ($36\\,\\mathrm{W}$)." % sci(Pinst, 2)))
    mcy, s, vcy = 75.0, 0.05, 6.0; Pcy = mcy * G * s * vcy
    num(B, c, t, 2, "A cyclist and bicycle (total mass $75\\,\\mathrm{kg}$) climb a slope with $\\sin\\theta=0.050$ at a constant $6.0\\,\\mathrm{m/s}$. Neglecting friction and air resistance, what power does the cyclist supply? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Pcy, [mcy * G * vcy, mcy * G * s, mcy * G * s * vcy * 10, Pcy / 2], "W",
        ex("The force along the slope balances $mg\\sin\\theta=(75)(9.8)(0.050)=36.75\\,\\mathrm{N}$.", "$P=Fv=(36.75)(6.0)=%s\\,\\mathrm{W}$." % sci(Pcy)))
    Ein, Wout = 500.0, 150.0
    num(B, c, t, 1, "A machine takes in $500\\,\\mathrm{J}$ of energy and does $150\\,\\mathrm{J}$ of useful work. What is its efficiency?",
        Wout / Ein * 100, [70.0, 33.3, 3.33, 350.0], "%", sig=3,
        explain=ex("$\\eta=\\dfrac{E_{useful}}{E_{in}}=\\dfrac{150}{500}=%s\\%%$; the other $350\\,\\mathrm{J}$ is wasted as heat." % sci(Wout / Ein * 100)))

def rotation(B):
    c, t = "c4", "Rotation of rigid bodies"
    r, Fw, th = 0.30, 40.0, 30.0; tau = r * Fw * math.sin(rad(th))
    num(B, c, t, 2, "A $40\\,\\mathrm{N}$ force is applied to a wrench at a point $0.30\\,\\mathrm{m}$ from the bolt, at an angle of $30^\\circ$ to the wrench. What is the torque about the bolt?",
        tau, [r * Fw, r * Fw * math.cos(rad(th)), Fw * math.sin(rad(th)), r * Fw * 10], "N m",
        ex("$\\tau=rF\\sin\\theta=(0.30)(40)\\sin30^\\circ=%s\\,\\mathrm{N\\,m}$ ($\\theta$ is the angle between $\\vec r$ and $\\vec F$; only the perpendicular part of the force turns the wrench)." % sci(tau)))
    I, ts = 0.50, 3.0; alpha = ts / I
    num(B, c, t, 2, "A wheel of moment of inertia $0.50\\,\\mathrm{kg\\,m^2}$ is acted on by a net torque of $3.0\\,\\mathrm{N\\,m}$. What is its angular acceleration?",
        alpha, [ts * I, I / ts, ts + I, ts / I / 2], "rad/s^2",
        ex("Rotational form of Newton's second law: $\\tau=I\\alpha\\Rightarrow\\alpha=\\dfrac{\\tau}{I}=\\dfrac{3.0}{0.50}=%s\\,\\mathrm{rad/s^2}$." % sci(alpha)))
    M, R, w = 2.0, 0.20, 30.0; Id = 0.5 * M * R * R; K = 0.5 * Id * w * w; check(K, 0.5 * M * (w * R) ** 2 / 2)
    num(B, c, t, 2, "A uniform solid disk ($I=\\tfrac12MR^2$) of mass $2.0\\,\\mathrm{kg}$ and radius $0.20\\,\\mathrm{m}$ spins about its axis at $30\\,\\mathrm{rad/s}$. What is its rotational kinetic energy?",
        K, [0.5 * M * R * R * w * w * 2, 0.5 * Id * w, 0.5 * M * (w * R) ** 2 * 2, K / 2], "J",
        ex("$I=\\tfrac12MR^2=\\tfrac12(2.0)(0.20)^2=0.040\\,\\mathrm{kg\\,m^2}$.", "$K=\\tfrac12I\\omega^2=\\tfrac12(0.040)(30)^2=%s\\,\\mathrm{J}$." % sci(K)))
    Mc, vc = 4.0, 2.0; Kt = 0.75 * Mc * vc * vc
    check(Kt, 0.5 * Mc * vc ** 2 + 0.5 * (0.5 * Mc) * vc ** 2)          # translation + rotation, omega = v/R
    num(B, c, t, 3, "A solid cylinder ($I=\\tfrac12MR^2$) of mass $4.0\\,\\mathrm{kg}$ rolls without slipping on a horizontal floor with its centre moving at $2.0\\,\\mathrm{m/s}$. What is its total kinetic energy?",
        Kt, [0.5 * Mc * vc * vc, 0.25 * Mc * vc * vc, Mc * vc * vc, 0.5 * Mc * vc * vc * 0.75], "J",
        ex("Rolling without slipping: $\\omega=v/R$. $K=\\tfrac12Mv^2+\\tfrac12I\\omega^2=\\tfrac12Mv^2+\\tfrac14Mv^2=\\tfrac34Mv^2$.", "$K=\\tfrac34(4.0)(2.0)^2=%s\\,\\mathrm{J}$. Translation alone ($8.0\\,\\mathrm{J}$) forgets the rotational part." % sci(Kt)))
    I1, I2, w1 = 4.0, 1.6, 2.0; w2 = I1 * w1 / I2
    num(B, c, t, 3, "A skater spins at $2.0\\,\\mathrm{rev/s}$ with her arms outstretched ($I=4.0\\,\\mathrm{kg\\,m^2}$). She pulls her arms in and her moment of inertia drops to $1.6\\,\\mathrm{kg\\,m^2}$. What is her new rate of rotation?",
        w2, [I2 * w1 / I1, w1 * (I1 / I2) ** 2, w1 + (I1 - I2), w1], "rev/s",
        ex("No external torque, so angular momentum is conserved: $I_1\\omega_1=I_2\\omega_2$.", "$\\omega_2=\\dfrac{I_1}{I_2}\\omega_1=\\dfrac{4.0}{1.6}(2.0)=%s\\,\\mathrm{rev/s}$ (her kinetic energy increases: she does work pulling her arms in)." % sci(w2)))
    m1, x1, m2 = 20.0, 1.5, 30.0; x2 = m1 * x1 / m2
    num(B, c, t, 1, "A $20\\,\\mathrm{kg}$ child sits $1.5\\,\\mathrm{m}$ from the pivot of a light seesaw. Where must a $30\\,\\mathrm{kg}$ child sit on the other side to balance it?",
        x2, [m2 * x1 / m1, x1, 0.5, 3.0], "m",
        ex("Torques about the pivot balance: $m_1gx_1=m_2gx_2\\Rightarrow x_2=\\dfrac{m_1}{m_2}x_1=\\dfrac{20}{30}(1.5)=%s\\,\\mathrm{m}$." % sci(x2), "The heavier child sits closer to the pivot."))
    txt(B, c, t, 3, "A solid sphere, a solid cylinder and a thin hoop, all of the same mass and radius, are released from rest at the top of an incline and roll without slipping. Which one reaches the bottom first?",
        "The solid sphere", ["The solid cylinder", "The thin hoop", "They arrive together"],
        ex("$a=\\dfrac{g\\sin\\theta}{1+I/(MR^2)}$ and $I/(MR^2)$ is $\\tfrac25$ (sphere), $\\tfrac12$ (cylinder), $1$ (hoop). The smallest ratio gives the largest acceleration: the sphere wins, the hoop is last. The mass and the radius do not matter."))
    mp, L0 = 2.0, 1.0; Ic = 2 * mp * (L0 / 2) ** 2
    num(B, c, t, 2, "Two $2.0\\,\\mathrm{kg}$ point masses are fixed at the ends of a light rod of length $1.0\\,\\mathrm{m}$. What is the moment of inertia of the system about an axis through the centre of the rod, perpendicular to it?",
        Ic, [2 * mp * L0 ** 2, mp * (L0 / 2) ** 2, 2 * mp * (L0 / 2), 4 * Ic], "kg m^2",
        ex("$I=\\sum m_ir_i^2=2(2.0)(0.50)^2=%s\\,\\mathrm{kg\\,m^2}$." % sci(Ic), "About one end the answer would be $(2.0)(1.0)^2=2.0\\,\\mathrm{kg\\,m^2}$: $I$ depends on the axis."))

# =============================================================================================== assembly
def build():
    B = Bank("PH1", seed=20261104)
    for fn in (vectors, springs, conservative, impulse, connected, weight, kin_defs, graphs, thermal, carnot, power, rotation):
        fn(B)
    return B

def lint(B):
    """Same guard as the other pools: control characters, unbalanced $, repeated or empty options."""
    problems = []
    for q in B.items:
        for t in [q["q"], q["explain"]] + list(q["opts"]):
            if any(ord(ch) < 32 and ch != "\n" for ch in t):
                problems.append((q["id"], "control character", t[:60]))
            if t.replace("\\$", "").count("$") % 2:
                problems.append((q["id"], "unbalanced $", t[:60]))
        if len(set(q["opts"])) != 4 or any(not o.strip() for o in q["opts"]) or not 0 <= q["correct"] < 4:
            problems.append((q["id"], "bad options", ""))
    assert not problems, "gap pool lint failed: %r" % (problems[:5],)
    return len(B.items)

def merge(main, gap):
    """Finalize the gap bank on its own (balanced answer positions), give its ids the 'g' kind and append it to the main bank."""
    report = gap.finalize()
    lint(gap)
    for it in gap.items:
        it["id"] = it["id"].replace("-q", "-g", 1)
    main.items.extend(gap.items)
    return report

if __name__ == "__main__":
    from collections import Counter
    G_ = build()
    print(merge(Bank("PH1", seed=1), G_))
    print(sorted(Counter((i["ch"], i["topic"]) for i in G_.items).items()))
    print("skipped", len(G_.skipped), "fillers", len(FILLED))
    for x in G_.skipped + FILLED: print("  ", x)
