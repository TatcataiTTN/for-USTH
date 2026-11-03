# -*- coding: utf-8 -*-
"""Physics II gap-fill pool: questions for the concepts that the Concept finder reported as thin (superposition of forces and fields, dipoles and rings,
Hall effect, forces on currents, crossed fields, current loops, Gauss' law for magnetism, Biot-Savart, solenoids, RL circuits, motional emf, induced fields,
magnetic flux, reflection, Snell's law, refraction at a surface, X-ray diffraction, combined interference and diffraction).
A separate Bank (ids of kind 'g', tag 'gap') merged after the main bank: the ids and option order of the existing questions do not move and the fixed
quizzes and mock exams keep their questions; the new ones live in the practice bank, the random quizzes and one extra set per chapter."""
import math
from phys_common import *
from qlib import Bank

TAG = ("gap",)
def GAP(topic): return "Generated to fill a gap: " + topic

def num(B, ch, topic, level, stem, ans, wrongs, unit, explain, sig=3, fig=None):
    return mcq_num(B, ch, topic, level, stem, ans, wrongs, unit, explain, GAP(topic), origin="gen", sig=sig, fig=fig, tags=TAG)

def txt(B, ch, topic, level, stem, correct, wrongs, explain, fig=None):
    return mcq_text(B, ch, topic, level, stem, correct, wrongs, explain, GAP(topic), origin="concept", fig=fig, tags=TAG)

def efield(charges, pt):
    """Field (Ex, Ey) at pt from point charges [(q, (x, y))]."""
    ex_ = ey_ = 0.0
    for q, (x, y) in charges:
        dx, dy = pt[0] - x, pt[1] - y; r3 = math.hypot(dx, dy) ** 3
        ex_ += K_E * q * dx / r3; ey_ += K_E * q * dy / r3
    return ex_, ey_

# =============================================================================================== chapters 1 and 2
def electrostatics(B):
    c, t = "c1", "Superposition of forces"
    q1, q2, q3 = 2.0e-6, -3.0e-6, 1.0e-6
    F1 = K_E * q1 * q3 / 0.20 ** 2; F2 = K_E * q2 * q3 / 0.10 ** 2; net = F1 + F2
    check(abs(net), q3 * math.hypot(*efield([(q1, (0, 0)), (q2, (0.10, 0))], (0.20, 0))))
    num(B, c, t, 2, "Charges $q_1=+2.0\\,\\mu\\mathrm{C}$ at $x=0$, $q_2=-3.0\\,\\mu\\mathrm{C}$ at $x=0.10\\,\\mathrm{m}$ and $q_3=+1.0\\,\\mu\\mathrm{C}$ at $x=0.20\\,\\mathrm{m}$ lie on a line. What is the magnitude of the net force on $q_3$?",
        abs(net), [abs(F1) + abs(F2), abs(F2), abs(F1), 0.5 * (abs(F1) + abs(F2))], "N",
        ex("$q_1$ repels $q_3$ (towards $+x$): $F_1=\\dfrac{kq_1q_3}{(0.20)^2}=%s\\,\\mathrm{N}$." % sci(F1), "$q_2$ attracts $q_3$ (towards $-x$): $F_2=\\dfrac{k|q_2|q_3}{(0.10)^2}=%s\\,\\mathrm{N}$." % sci(abs(F2)),
           "The forces point in opposite directions, so they subtract: $F=%s-%s=%s\\,\\mathrm{N}$ towards $-x$ (adding the magnitudes would be the classic error)." % (sci(abs(F2)), sci(F1), sci(abs(net)))))
    q, a = 2.0e-6, 0.30; f0 = K_E * q * q / a ** 2; Fsq = f0 * (math.sqrt(2) + 0.5)
    ch3 = [(q, (a, 0.0)), (q, (0.0, a)), (q, (a, a))]; ex_, ey_ = efield(ch3, (0.0, 0.0)); check(Fsq, q * math.hypot(ex_, ey_))
    num(B, c, t, 2, "Three charges $+2.0\\,\\mu\\mathrm{C}$ sit at three corners of a square of side $0.30\\,\\mathrm{m}$. What is the magnitude of the force on a fourth charge $+2.0\\,\\mu\\mathrm{C}$ placed at the remaining corner?",
        Fsq, [f0 * math.sqrt(2), 3 * f0, f0 * (math.sqrt(2) + 1), f0 * (math.sqrt(2) + 2)], "N",
        ex("Each neighbouring charge gives $F_0=\\dfrac{kq^2}{a^2}=%s\\,\\mathrm{N}$ along a side; the two forces are perpendicular and add to $\\sqrt2F_0$ along the diagonal." % sci(f0),
           "The opposite corner is at distance $a\\sqrt2$: $\\dfrac{kq^2}{2a^2}=\\dfrac{F_0}{2}$, along the same diagonal.", "$F=\\left(\\sqrt2+\\tfrac12\\right)F_0=%s\\,\\mathrm{N}$." % sci(Fsq)))
    txt(B, c, t, 1, "The net electrostatic force on a point charge due to a group of other point charges is", "the vector sum of the Coulomb forces due to each of the other charges separately",
        ["the Coulomb force of the total charge placed at their centre", "the sum of the magnitudes of the individual forces", "the force due to the nearest charge only"],
        ex("Forces superpose as vectors (principle of superposition): each pair interacts as if the others were absent, and the results are added with their directions."))
    txt(B, c, t, 3, "Three equal positive charges $Q$ sit at the corners of an equilateral triangle. A fourth positive charge $q$ is placed at the centre of the triangle. The net force on $q$ is",
        "zero, because the three equal forces are $120^\\circ$ apart and cancel", ["directed towards one corner", "$3kQq/r^2$ directed towards the centre", "non-zero and directed along the altitude from one corner"],
        ex("By symmetry the three forces have equal magnitude and directions $120^\\circ$ apart, so their vector sum is zero (the same as three equal forces in equilibrium)."))
    qa, qb, qc = 2.0e-6, -4.0e-6, 1.0e-6
    fa = K_E * qa * qc / 0.30 ** 2; fb = K_E * abs(qb) * qc / 0.40 ** 2; Fm = math.hypot(fa, fb)
    check(Fm, qc * math.hypot(*efield([(qa, (0.30, 0.0)), (qb, (0.0, 0.40))], (0.0, 0.0))))
    num(B, c, t, 2, "A charge $+1.0\\,\\mu\\mathrm{C}$ sits at the origin. A charge $+2.0\\,\\mu\\mathrm{C}$ is at $(0.30,\\ 0)\\,\\mathrm{m}$ and a charge $-4.0\\,\\mu\\mathrm{C}$ is at $(0,\\ 0.40)\\,\\mathrm{m}$. What is the magnitude of the net force on the charge at the origin?",
        Fm, [fa + fb, abs(fb - fa), fb, fa], "N",
        ex("The $+2.0\\,\\mu\\mathrm{C}$ charge repels along $-x$: $F_x=%s\\,\\mathrm{N}$. The $-4.0\\,\\mu\\mathrm{C}$ charge attracts along $+y$: $F_y=%s\\,\\mathrm{N}$." % (sci(fa), sci(fb)),
           "The forces are perpendicular: $F=\\sqrt{F_x^2+F_y^2}=%s\\,\\mathrm{N}$ (not their sum)." % sci(Fm)))
    # ------------------------------------------------------------------ superposition of fields
    c, t = "c2", "Superposition of fields"
    L = 0.30; x = 2 * L / 3; check(4 / x ** 2, 1 / (L - x) ** 2)
    num(B, c, t, 2, "Two positive charges, $+4q$ and $+q$, are $0.30\\,\\mathrm{m}$ apart. At what distance from the $+4q$ charge, on the line between them, is the electric field zero?",
        x, [L / 2, L / 3, 4 * L / 5, L / 5], "m",
        ex("The fields cancel where $\\dfrac{k(4q)}{x^2}=\\dfrac{kq}{(L-x)^2}$, i.e. $\\dfrac2x=\\dfrac1{L-x}$.", "$x=\\dfrac{2L}{3}=%s\\,\\mathrm{m}$ - closer to the weaker charge, not at the midpoint." % sci(x)))
    Q, a = 2.0e-9, 0.10; Em = 2 * K_E * Q / a ** 2
    check(Em, math.hypot(*efield([(Q, (-a, 0.0)), (-Q, (a, 0.0))], (0.0, 0.0))))
    num(B, c, t, 2, "Charges $+2.0\\,\\mathrm{nC}$ and $-2.0\\,\\mathrm{nC}$ are $0.20\\,\\mathrm{m}$ apart. What is the magnitude of the electric field at the midpoint between them?",
        Em, [0.0, K_E * Q / a ** 2, 4 * K_E * Q / a ** 2, K_E * Q / a ** 2 * 1.5], "N/C",
        ex("At the midpoint both fields point in the SAME direction (away from $+Q$, towards $-Q$), so they add: $E=2\\dfrac{kQ}{a^2}=2\\dfrac{(8.99\\times10^9)(2.0\\times10^{-9})}{(0.10)^2}=%s\\,\\mathrm{N/C}$." % sci(Em), "The field is zero at the midpoint only for two charges of the SAME sign."))
    qq, aa, yy = 3.0e-9, 0.040, 0.030; Eb = 2 * K_E * qq * yy / (yy ** 2 + aa ** 2) ** 1.5
    check(Eb, efield([(qq, (-aa, 0.0)), (qq, (aa, 0.0))], (0.0, yy))[1])
    num(B, c, t, 3, "Two charges $+3.0\\,\\mathrm{nC}$ are fixed at $(\\pm0.040,\\ 0)\\,\\mathrm{m}$. What is the electric field at the point $(0,\\ 0.030)\\,\\mathrm{m}$?",
        Eb, [2 * K_E * qq / yy ** 2, K_E * qq * yy / (yy ** 2 + aa ** 2) ** 1.5, 2 * K_E * qq / (yy ** 2 + aa ** 2), 0.0], "N/C",
        ex("Each charge is at distance $r=\\sqrt{0.030^2+0.040^2}=0.050\\,\\mathrm{m}$. The $x$-components cancel; the $y$-components add: $E=2\\dfrac{kq}{r^2}\\cdot\\dfrac{y}{r}$.", "$E=\\dfrac{2kqy}{(y^2+a^2)^{3/2}}=%s\\,\\mathrm{N/C}$ along $+y$." % sci(Eb)))
    # ------------------------------------------------------------------ ring and disk
    t = "Charged ring and disk"
    Qr, R, z = 5.0e-9, 0.060, 0.080; Er = K_E * Qr * z / (z * z + R * R) ** 1.5
    N = 20000; Esum = sum(K_E * (Qr / N) * z / (z * z + R * R) ** 1.5 for _ in range(N)); check(Er, Esum, 1e-9)       # every element has the same distance: the axial parts add
    num(B, c, t, 2, "A ring of radius $0.060\\,\\mathrm{m}$ carries a uniform charge of $+5.0\\,\\mathrm{nC}$. What is the electric field on the axis at $0.080\\,\\mathrm{m}$ from the centre?",
        Er, [K_E * Qr / z ** 2, K_E * Qr / (z * z + R * R), K_E * Qr * z / R ** 3, 0.0], "N/C",
        ex("$E_z=\\dfrac{kQz}{(z^2+R^2)^{3/2}}=\\dfrac{(8.99\\times10^9)(5.0\\times10^{-9})(0.080)}{(0.0100)^{3/2}}=%s\\,\\mathrm{N/C}$." % sci(Er), "The point-charge value $kQ/z^2$ would ignore that each element is farther than $z$ and that only the axial component survives."))
    txt(B, c, t, 1, "The electric field at the centre of a uniformly charged ring (in the plane of the ring) is", "zero", ["$kQ/R^2$ pointing towards the ring", "$kQ/R^2$ pointing away from the centre", "$2kQ/R^2$"],
        ex("Every element of charge is cancelled by the diametrically opposite one: the field at the centre is zero (although the potential there is $kQ/R$, not zero)."))
    sg = 2.0e-6; Ed = sg / (2 * EPS0)
    num(B, c, t, 3, "A very large uniformly charged disk carries a surface charge density of $2.0\\times10^{-6}\\,\\mathrm{C/m^2}$. What is the electric field very close to the centre of the disk, with $z\\ll R$? ($\\varepsilon_0=8.85\\times10^{-12}\\,\\mathrm{C^2/N\\,m^2}$)",
        Ed, [sg / EPS0, sg / (4 * EPS0), sg * K_E], "N/C",
        ex("For $z\\ll R$ the disk looks like an infinite sheet: $E=\\dfrac{\\sigma}{2\\varepsilon_0}=\\dfrac{2.0\\times10^{-6}}{2(8.85\\times10^{-12})}=%s\\,\\mathrm{N/C}$." % sci(Ed), "$\\sigma/\\varepsilon_0$ is the field next to a CONDUCTING surface (one face only)."))
    # ------------------------------------------------------------------ dipoles
    t = "Electric dipoles"
    qd, d = 3.0e-9, 0.020; p = qd * d
    num(B, c, t, 1, "A dipole consists of charges $+3.0\\,\\mathrm{nC}$ and $-3.0\\,\\mathrm{nC}$ separated by $2.0\\,\\mathrm{cm}$. What is the magnitude of its dipole moment?",
        p, [qd / d, 2 * qd * d, qd * d * d, qd * 2], "C m",
        ex("$p=qd=(3.0\\times10^{-9})(0.020)=%s\\,\\mathrm{C\\,m}$ (convert $2.0\\,\\mathrm{cm}$ to metres; $q$ is ONE of the two charges)." % sci(p, 2)), sig=2)
    E0 = 2.0e4; th = 30.0; tau = p * E0 * math.sin(rad(th))
    num(B, c, t, 2, "A dipole of moment $6.0\\times10^{-11}\\,\\mathrm{C\\,m}$ makes an angle of $30^\\circ$ with a uniform field of $2.0\\times10^4\\,\\mathrm{N/C}$. What is the torque on it?",
        tau, [p * E0 * math.cos(rad(th)), p * E0, p * E0 * math.sin(rad(th)) / 2, p * E0 * 5], "N m",
        ex("$\\tau=pE\\sin\\theta=(6.0\\times10^{-11})(2.0\\times10^4)\\sin30^\\circ=%s\\,\\mathrm{N\\,m}$ (maximum, $pE=1.2\\times10^{-6}$, at $90^\\circ$)." % sci(tau, 2)), sig=2)
    W = 2 * p * E0
    num(B, c, t, 3, "How much work must an external agent do to turn the dipole above ($p=6.0\\times10^{-11}\\,\\mathrm{C\\,m}$, $E=2.0\\times10^4\\,\\mathrm{N/C}$) from its stable equilibrium orientation to the opposite orientation?",
        W, [p * E0, 4 * p * E0, 0.0], "J",
        ex("$U=-\\vec p\\cdot\\vec E$: $U=-pE$ at $0^\\circ$ and $+pE$ at $180^\\circ$, so $W=\\Delta U=2pE=2(6.0\\times10^{-11})(2.0\\times10^4)=%s\\,\\mathrm{J}$." % sci(W, 2)), sig=2)

# =============================================================================================== chapter 5
def magnetic_forces(B):
    c = "c5"
    t = "Hall effect"
    n_cu, I, Bf, th = 8.5e28, 10.0, 0.50, 0.50e-3; VH = I * Bf / (n_cu * E_CH * th)
    num(B, c, t, 2, "A copper strip ($n=8.5\\times10^{28}\\,\\mathrm{m^{-3}}$) $0.50\\,\\mathrm{mm}$ thick carries a current of $10\\,\\mathrm{A}$ in a perpendicular magnetic field of $0.50\\,\\mathrm{T}$. What is the Hall voltage across the strip?",
        VH, [I * Bf / (n_cu * E_CH * 0.50), 2 * VH, VH / 2, I * Bf * th / (n_cu * E_CH)], "V",
        ex("$V_H=\\dfrac{IB}{n\\,e\\,t}=\\dfrac{(10)(0.50)}{(8.5\\times10^{28})(1.602\\times10^{-19})(0.50\\times10^{-3})}=%s\\,\\mathrm{V}$." % sci(VH), "Thickness in metres ($0.50\\,\\mathrm{mm}=5.0\\times10^{-4}\\,\\mathrm{m}$); the Hall voltage of a good metal is tiny, which is why semiconductors are used as Hall probes."))
    I2, B2, t2, V2 = 3.0, 1.2, 0.20e-3, 3.50e-6; n2 = I2 * B2 / (E_CH * t2 * V2)
    num(B, c, t, 2, "A strip $0.20\\,\\mathrm{mm}$ thick carries $3.0\\,\\mathrm{A}$ in a field of $1.2\\,\\mathrm{T}$ and the Hall voltage is $3.50\\,\\mu\\mathrm{V}$. What is the charge-carrier density?",
        n2, [2 * n2, n2 / 2, I2 * B2 / (E_CH * 0.20 * V2)], "m^{-3}",
        ex("From $V_H=\\dfrac{IB}{net}$: $n=\\dfrac{IB}{e\\,t\\,V_H}=\\dfrac{(3.0)(1.2)}{(1.602\\times10^{-19})(0.20\\times10^{-3})(3.50\\times10^{-6})}=%s\\,\\mathrm{m^{-3}}$." % sci(n2), "Use $t$ in metres and $V_H$ in volts ($3.50\\,\\mu\\mathrm{V}=3.50\\times10^{-6}\\,\\mathrm{V}$)."))
    # direction: current to the right, B into the page, electrons: force on electron q v x B, v = -x, B = -z -> v x B = -(x)x(-z)... computed with cross product
    def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    Fe = tuple(-1 * x for x in cross((-1, 0, 0), (0, 0, -1)))          # q = -e, v = -x (electrons drift against the current), B = -z (into the page)
    check(Fe[1], 1.0)                                                  # electrons are pushed towards +y: the top edge becomes negative, the bottom edge higher in potential
    txt(B, c, t, 3, "A current flows to the right through a flat strip placed in a magnetic field pointing into the page. The charge carriers are electrons. Which edge of the strip is at the higher potential?",
        "The bottom edge", ["The top edge", "Both edges are at the same potential", "The right-hand end"],
        ex("The electrons drift to the LEFT: $\\vec v=-v\\hat x$. The field points into the page: $\\vec B=-B\\hat z$. Then $\\vec v\\times\\vec B=vB(\\hat x\\times\\hat z)=-vB\\,\\hat y$.",
           "For an electron ($q=-e$) the force $q\\vec v\\times\\vec B=+evB\\,\\hat y$ points to the TOP edge, so the electrons pile up there. The top edge becomes negative and the BOTTOM edge is at the higher potential. For positive carriers the polarity would be reversed - this is how the sign of the carriers is measured."))
    txt(B, c, t, 2, "The Hall voltage across a conducting strip of thickness $t$ carrying current $I$ in a perpendicular field $B$ is proportional to", "$\\dfrac{IB}{t}$", ["$IBt$", "$\\dfrac{I}{Bt}$", "$\\dfrac{B}{It}$"],
        ex("$V_H=\\dfrac{IB}{net}$: proportional to the current and the field, inversely proportional to the thickness (a thinner strip gives a larger voltage)."))
    VHh, Bh, w = 1.2e-6, 0.40, 0.015; vd = VHh / (Bh * w); check(E_CH * (VHh / w), E_CH * vd * Bh)
    num(B, c, t, 3, "The Hall voltage across a $1.5\\,\\mathrm{cm}$ wide strip in a $0.40\\,\\mathrm{T}$ field is $1.2\\,\\mu\\mathrm{V}$. What is the drift speed of the charge carriers?",
        vd, [VHh / Bh, VHh * w / Bh, VHh * Bh * w], "m/s",
        ex("In steady state the electric Hall force balances the magnetic force: $eE_H=ev_dB$ with $E_H=V_H/w$.", "$v_d=\\dfrac{V_H}{Bw}=\\dfrac{1.2\\times10^{-6}}{(0.40)(0.015)}=%s\\,\\mathrm{m/s}$." % sci(vd)))
    # ------------------------------------------------------------------ parallel currents
    t = "Force between parallel currents"
    Ia = Ib = 10.0; dd = 0.020; fl = MU0 * Ia * Ib / (2 * math.pi * dd)
    num(B, c, t, 1, "Two long parallel wires $2.0\\,\\mathrm{cm}$ apart each carry $10\\,\\mathrm{A}$ in the same direction. What is the force per unit length between them?",
        fl, [2 * fl, MU0 * Ia * Ib / dd, fl / 2, fl * 100], "N/m",
        ex("$\\dfrac FL=\\dfrac{\\mu_0I_1I_2}{2\\pi d}=\\dfrac{(4\\pi\\times10^{-7})(10)(10)}{2\\pi(0.020)}=%s\\,\\mathrm{N/m}$." % sci(fl), "Do not forget the $2\\pi$ in the denominator; the force is attractive for currents in the same direction."))
    txt(B, c, t, 1, "Two long parallel wires carry currents in the same direction. The wires", "attract each other", ["repel each other", "exert no force on each other", "attract only if the currents are equal"],
        ex("Each wire creates a field at the other that, with the right-hand rule, gives a force towards the other wire when the currents are parallel; opposite currents repel (Newton's third law: the two forces are equal and opposite)."))
    Fl, ds = 4.0e-4, 0.050; Iw = math.sqrt(Fl * 2 * math.pi * ds / MU0); check(Iw, 10.0)
    num(B, c, t, 2, "Two long parallel wires $5.0\\,\\mathrm{cm}$ apart carry equal currents and attract each other with a force of $4.0\\times10^{-4}\\,\\mathrm{N}$ per metre of length. What is the current in each wire?",
        Iw, [Iw ** 2, Iw / 2, Iw * 2, Iw / 10], "A", sig=2,
        explain=ex("$\\dfrac FL=\\dfrac{\\mu_0I^2}{2\\pi d}\\Rightarrow I=\\sqrt{\\dfrac{2\\pi d}{\\mu_0}\\dfrac FL}=\\sqrt{\\dfrac{2\\pi(0.050)(4.0\\times10^{-4})}{4\\pi\\times10^{-7}}}=%s\\,\\mathrm{A}$." % sci(Iw, 2)))
    txt(B, c, t, 2, "The distance between two long parallel current-carrying wires is doubled while the currents are kept fixed. The force per unit length between them", "is halved", ["is quartered", "is doubled", "does not change"],
        ex("$\\dfrac FL=\\dfrac{\\mu_0I_1I_2}{2\\pi d}\\propto\\dfrac1d$: doubling $d$ halves the force (it is NOT an inverse-square law, unlike Coulomb's force between point charges)."))
    I1, I2, dw = 5.0, 15.0, 0.30; xz = dw * I1 / (I1 + I2); check(I1 / xz, I2 / (dw - xz))
    num(B, "c6", "Magnetic field of a straight wire", 3, "Two long parallel wires $0.30\\,\\mathrm{m}$ apart carry currents of $5.0\\,\\mathrm{A}$ and $15\\,\\mathrm{A}$ in the same direction. At what distance from the $5.0\\,\\mathrm{A}$ wire, on the line between the wires, is the magnetic field zero?",
        xz, [dw / 2, dw * I2 / (I1 + I2), 0.10, dw / 4 * 0.4], "m",
        ex("Between the wires the two fields point in opposite directions and cancel when $\\dfrac{\\mu_0I_1}{2\\pi x}=\\dfrac{\\mu_0I_2}{2\\pi(d-x)}$, i.e. $\\dfrac{I_1}{x}=\\dfrac{I_2}{d-x}$.", "$x=d\\dfrac{I_1}{I_1+I_2}=0.30\\times\\dfrac{5}{20}=%s\\,\\mathrm{m}$ (closer to the smaller current)." % sci(xz)))
    # ------------------------------------------------------------------ force on a wire
    t = "Force on a current-carrying wire"
    Iw, Lw, Bw = 5.0, 0.40, 0.30
    num(B, c, t, 1, "A straight wire $0.40\\,\\mathrm{m}$ long carries $5.0\\,\\mathrm{A}$ perpendicular to a uniform magnetic field of $0.30\\,\\mathrm{T}$. What is the force on the wire?",
        Iw * Lw * Bw, [Iw * Lw * Bw / 2, Iw * Bw, Iw * Lw / Bw, Iw * Lw * Bw * 2], "N",
        ex("$F=ILB\\sin90^\\circ=(5.0)(0.40)(0.30)=%s\\,\\mathrm{N}$." % sci(Iw * Lw * Bw)))
    F30 = Iw * Lw * Bw * math.sin(rad(30))
    num(B, c, t, 2, "The same wire ($0.40\\,\\mathrm{m}$, $5.0\\,\\mathrm{A}$) makes an angle of $30^\\circ$ with the $0.30\\,\\mathrm{T}$ field. What is the force on it?",
        F30, [Iw * Lw * Bw * math.cos(rad(30)), Iw * Lw * Bw, Iw * Lw * Bw * math.tan(rad(30))], "N",
        ex("$F=ILB\\sin\\theta$ with $\\theta$ the angle between the wire (current) and $\\vec B$: $F=(5.0)(0.40)(0.30)\\sin30^\\circ=%s\\,\\mathrm{N}$." % sci(F30)))
    def cr(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    check(cr((1, 0, 0), (0, 0, 1))[1], -1.0)
    txt(B, c, t, 2, "A wire carries current to the right (along $+x$) in a uniform field pointing out of the page (along $+z$). The force on the wire points", "down the page ($-y$)", ["up the page ($+y$)", "into the page", "to the left"],
        ex("$\\vec F=I\\vec L\\times\\vec B$ with $\\vec L=\\hat x$, $\\vec B=\\hat z$: $\\hat x\\times\\hat z=-\\hat y$. Right-hand rule: fingers along the current, curl towards $\\vec B$, thumb gives the force."))
    lam, Bh = 0.020, 0.25; Ih = lam * G / Bh
    num(B, c, t, 3, "A horizontal wire of mass $0.020\\,\\mathrm{kg}$ per metre lies perpendicular to a horizontal magnetic field of $0.25\\,\\mathrm{T}$. What current makes the wire float (the magnetic force balances its weight)? ($g=9.8\\,\\mathrm{m/s^2}$)",
        Ih, [Ih / 10, Ih * 10, lam / Bh, lam * G * Bh], "A",
        ex("Balance per unit length: $IB=\\lambda g\\Rightarrow I=\\dfrac{\\lambda g}{B}=\\dfrac{(0.020)(9.8)}{0.25}=%s\\,\\mathrm{A}$." % sci(Ih)))
    # ------------------------------------------------------------------ crossed fields
    t = "Crossed fields"
    Ec, Bc = 3.0e4, 0.050; vs = Ec / Bc
    num(B, c, t, 2, "In a velocity selector the electric field is $3.0\\times10^4\\,\\mathrm{V/m}$ and the magnetic field is $0.050\\,\\mathrm{T}$. At what speed do particles pass through undeflected?",
        vs, [Ec * Bc, Ec / Bc ** 2, Ec / (2 * Bc), 2 * Ec / Bc], "m/s", sig=2,
        explain=ex("Undeflected: $qE=qvB\\Rightarrow v=\\dfrac EB=\\dfrac{3.0\\times10^4}{0.050}=%s\\,\\mathrm{m/s}$." % sci(vs, 2)))
    txt(B, c, t, 2, "A velocity selector with crossed uniform fields $E$ and $B$ lets particles through undeflected. The speed that passes depends on", "$E$ and $B$ only, not on the charge or the mass of the particle", ["the charge of the particle only", "the mass of the particle only", "the charge-to-mass ratio of the particle"],
        ex("$qE=qvB$: the charge cancels, and mass never enters the force balance. $v=E/B$ for protons, electrons or ions alike."))
    vq, Eq = 2.0e5, 1.0e4; Bq = Eq / vq
    num(B, c, t, 3, "What magnetic field must be combined with an electric field of $1.0\\times10^4\\,\\mathrm{V/m}$, perpendicular to it, so that particles of speed $2.0\\times10^5\\,\\mathrm{m/s}$ pass undeflected?",
        Bq, [vq / Eq, Bq * 10, Bq / 10, Bq * 2], "T", sig=2,
        explain=ex("$B=\\dfrac Ev=\\dfrac{1.0\\times10^4}{2.0\\times10^5}=%s\\,\\mathrm{T}$." % sci(Bq, 2)))
    # ------------------------------------------------------------------ torque on a loop
    t = "Torque on a current loop"
    N_, I_, A_, B_ = 50, 2.0, 0.10 * 0.20, 0.30; mu = N_ * I_ * A_; tl = mu * B_
    num(B, c, t, 2, "A rectangular coil of $50$ turns, $0.10\\,\\mathrm{m}\\times0.20\\,\\mathrm{m}$, carries $2.0\\,\\mathrm{A}$. What is its magnetic dipole moment?",
        mu, [mu / N_, mu * 2, N_ * I_ / A_, I_ * A_], "A m^2", sig=2,
        explain=ex("$\\mu=NIA=(50)(2.0)(0.10\\times0.20)=%s\\,\\mathrm{A\\,m^2}$ (all turns count)." % sci(mu, 2)))
    num(B, c, t, 2, "The coil above ($\\mu=2.0\\,\\mathrm{A\\,m^2}$) is in a uniform field of $0.30\\,\\mathrm{T}$ with its plane parallel to the field. What is the torque on it?",
        tl, [tl / 2, mu / B_, mu + B_], "N m", sig=2,
        explain=ex("Plane parallel to $\\vec B$ means the normal is perpendicular to $\\vec B$: $\\tau=\\mu B\\sin90^\\circ=(2.0)(0.30)=%s\\,\\mathrm{N\\,m}$ (the maximum)." % sci(tl, 2)))

# =============================================================================================== chapter 6
def magnetic_fields(B):
    c = "c6"
    t = "Gauss' law for magnetism"
    txt(B, c, t, 1, "Gauss's law for magnetism states that the net magnetic flux through any closed surface is", "zero", ["$\\mu_0$ times the current enclosed", "proportional to the magnetic 'charge' enclosed", "equal to $BA$"],
        ex("$\\oint\\vec B\\cdot d\\vec A=0$ for every closed surface: there are no isolated magnetic poles, so as many field lines leave the surface as enter it."))
    txt(B, c, t, 2, "Which statement is a direct consequence of Gauss's law for magnetism?", "Magnetic field lines have no beginning or end: they form closed loops (isolated magnetic poles do not exist)",
        ["Magnetic field lines begin on north poles and end on south poles", "A changing electric flux produces a magnetic field", "The field of a long straight wire falls off as $1/r$"],
        ex("Because $\\oint\\vec B\\cdot d\\vec A=0$, field lines cannot start or stop at a point; they close on themselves (inside a magnet they run from the south pole to the north pole)."))
    num(B, c, t, 2, "A closed spherical surface surrounds a bar magnet. The magnetic flux through the upper hemisphere is $+0.40\\,\\mathrm{Wb}$ (outward). What is the flux through the lower hemisphere?",
        -0.40, [0.40, 0.0, -0.80], "Wb",
        ex("The total flux through the closed sphere is zero: $\\Phi_{upper}+\\Phi_{lower}=0\\Rightarrow\\Phi_{lower}=-0.40\\,\\mathrm{Wb}$ (the field lines that leave through the top come back in through the bottom)."), sig=2)
    Bc, rc = 0.30, 0.020; Phi = Bc * math.pi * rc ** 2
    num(B, c, t, 3, "A closed cylinder of radius $2.0\\,\\mathrm{cm}$ has its axis along a uniform magnetic field of $0.30\\,\\mathrm{T}$. The flux through the left end cap is $-3.77\\times10^{-4}\\,\\mathrm{Wb}$ (inward) and through the curved side it is zero. What is the flux through the right end cap?",
        Phi, [-Phi, 0.0, 2 * Phi], "Wb",
        ex("The curved side is parallel to $\\vec B$ (zero flux). The total flux through a closed surface is zero, so the right end cap carries $+B\\pi r^2=(0.30)\\pi(0.020)^2=%s\\,\\mathrm{Wb}$ outward." % sci(Phi)))
    txt(B, c, t, 3, "What distinguishes Gauss's law for magnetism from Gauss's law for electricity?", "The net electric flux can be non-zero because isolated charges exist, while the net magnetic flux is always zero because isolated poles do not",
        ["The electric flux depends on the shape of the closed surface but the magnetic flux does not", "Gauss's law for magnetism holds only for uniform fields", "Only the magnetic law involves a fundamental constant ($\\mu_0$)"],
        ex("Electric flux through a closed surface equals $Q_{enc}/\\varepsilon_0$ (charge can be isolated). No magnetic monopole has ever been found, so the enclosed 'magnetic charge' is zero. Neither flux depends on the shape of the surface, only on what is enclosed."))
    # ------------------------------------------------------------------ Biot-Savart
    t = "Biot-Savart law"
    I, R = 6.0, 0.10; Bsc = MU0 * I / (4 * R)
    N = 20000; Bint = sum(MU0 / (4 * math.pi) * I * (R * math.pi / N) / R ** 2 for _ in range(N)); check(Bsc, Bint, 1e-9)
    num(B, c, t, 2, "A wire carrying $6.0\\,\\mathrm{A}$ is bent into a semicircle of radius $0.10\\,\\mathrm{m}$ (the straight leads do not contribute). What is the magnetic field at the centre of the semicircle?",
        Bsc, [MU0 * I / (2 * R), MU0 * I / (4 * math.pi * R), MU0 * I / (2 * math.pi * R)], "T",
        ex("Every element $d\\ell=R\\,d\\theta$ is perpendicular to the radius, so $dB=\\dfrac{\\mu_0}{4\\pi}\\dfrac{I\\,d\\ell}{R^2}$ and all contributions point the same way.", "Half a loop gives half the field of a full loop: $B=\\dfrac{\\mu_0I}{4R}=\\dfrac{(4\\pi\\times10^{-7})(6.0)}{4(0.10)}=%s\\,\\mathrm{T}$." % sci(Bsc)))
    I2, R2, thd = 8.0, 0.20, math.pi / 2; Barc = MU0 * I2 * thd / (4 * math.pi * R2)
    num(B, c, t, 3, "A wire carrying $8.0\\,\\mathrm{A}$ follows a $90^\\circ$ circular arc of radius $0.20\\,\\mathrm{m}$. What is the magnetic field at the centre of curvature of the arc?",
        Barc, [MU0 * I2 / (2 * R2), MU0 * I2 / (4 * R2), Barc / 2], "T",
        ex("A $90^\\circ$ arc is one quarter of a full circle: $B=\\dfrac14\\dfrac{\\mu_0I}{2R}=\\dfrac{\\mu_0I\\theta}{4\\pi R}$ with $\\theta=\\pi/2$.", "$B=\\dfrac{(4\\pi\\times10^{-7})(8.0)}{8(0.20)}=%s\\,\\mathrm{T}$." % sci(Barc)))
    txt(B, c, t, 2, "According to the Biot-Savart law, the magnetic field $d\\vec B$ at a point P due to a current element $I\\,d\\vec\\ell$ is directed", "perpendicular to both $d\\vec\\ell$ and the line joining the element to P", ["along $d\\vec\\ell$", "along the line joining the element to P", "radially outward from the wire, in the plane of the wire"],
        ex("$d\\vec B=\\dfrac{\\mu_0}{4\\pi}\\dfrac{I\\,d\\vec\\ell\\times\\hat r}{r^2}$: a cross product, so $d\\vec B$ is perpendicular to both $d\\vec\\ell$ and $\\hat r$ (right-hand rule)."))
    # ------------------------------------------------------------------ solenoids
    t = "Solenoids and toroids"
    n, Is = 2000.0, 1.5; Bs = MU0 * n * Is
    num(B, c, t, 1, "A long solenoid has $2000$ turns per metre and carries $1.5\\,\\mathrm{A}$. What is the magnetic field inside it?",
        Bs, [MU0 * 20 * Is, MU0 * n * Is / 2, 2 * Bs], "T",
        ex("$B=\\mu_0nI=(4\\pi\\times10^{-7})(2000)(1.5)=%s\\,\\mathrm{T}$ (with $n$ in turns per METRE)." % sci(Bs)))
    Ns, Ls, I3 = 500, 0.25, 2.0; B3 = MU0 * (Ns / Ls) * I3
    num(B, c, t, 2, "A solenoid of $500$ turns is $0.25\\,\\mathrm{m}$ long and carries $2.0\\,\\mathrm{A}$. What is the field at its centre (ideal solenoid)?",
        B3, [MU0 * Ns * I3, MU0 * Ns * I3 * Ls, B3 / 2], "T",
        ex("$n=\\dfrac NL=\\dfrac{500}{0.25}=2000\\,\\mathrm{m^{-1}}$, so $B=\\mu_0nI=(4\\pi\\times10^{-7})(2000)(2.0)=%s\\,\\mathrm{T}$." % sci(B3)))
    Nt, It, rt = 800, 2.0, 0.15; Bt = MU0 * Nt * It / (2 * math.pi * rt)
    num(B, c, t, 3, "A toroid with $800$ turns carries $2.0\\,\\mathrm{A}$. What is the field at a radius of $0.15\\,\\mathrm{m}$ from the centre, inside the winding?",
        Bt, [MU0 * Nt * It / (math.pi * rt), MU0 * Nt * It / rt, MU0 * Nt * It], "T",
        ex("Ampere's law around a circle of radius $r$: $B(2\\pi r)=\\mu_0NI$, so $B=\\dfrac{\\mu_0NI}{2\\pi r}=\\dfrac{(4\\pi\\times10^{-7})(800)(2.0)}{2\\pi(0.15)}=%s\\,\\mathrm{T}$." % sci(Bt)))
    txt(B, c, t, 2, "Inside a long ideal solenoid, the magnitude of the magnetic field", "is uniform and independent of the position along the axis and of the distance from it",
        ["is zero on the axis and grows towards the windings", "decreases as $1/r$ with the distance $r$ from the axis", "is the same inside and outside the solenoid"],
        ex("For an ideal (very long) solenoid $B=\\mu_0nI$ everywhere inside, parallel to the axis; outside the field is (nearly) zero."))
    # ------------------------------------------------------------------ loops
    t = "Magnetic field of a loop"
    Nl, Il, Rl = 20, 3.0, 0.050; Bl = MU0 * Nl * Il / (2 * Rl)
    num(B, c, t, 2, "A flat coil of $20$ turns and radius $0.050\\,\\mathrm{m}$ carries $3.0\\,\\mathrm{A}$. What is the magnetic field at its centre?",
        Bl, [MU0 * Nl * Il / Rl, MU0 * Il / (2 * Rl), MU0 * Nl * Il / (4 * Rl)], "T",
        ex("Each turn gives $\\dfrac{\\mu_0I}{2R}$ and the $N$ turns add: $B=\\dfrac{\\mu_0NI}{2R}=\\dfrac{(4\\pi\\times10^{-7})(20)(3.0)}{2(0.050)}=%s\\,\\mathrm{T}$." % sci(Bl)))
    I4, R4, z4 = 4.0, 0.10, 0.20; Bax = MU0 * I4 * R4 ** 2 / (2 * (R4 ** 2 + z4 ** 2) ** 1.5)
    num(B, c, t, 3, "A circular loop of radius $0.10\\,\\mathrm{m}$ carries $4.0\\,\\mathrm{A}$. What is the magnetic field on its axis at $0.20\\,\\mathrm{m}$ from the centre?",
        Bax, [MU0 * I4 / (2 * R4), MU0 * I4 * R4 ** 2 / (2 * z4 ** 3), MU0 * I4 * R4 ** 2 / (2 * (R4 ** 2 + z4 ** 2))], "T",
        ex("On the axis $B_z=\\dfrac{\\mu_0IR^2}{2(R^2+z^2)^{3/2}}=\\dfrac{(4\\pi\\times10^{-7})(4.0)(0.10)^2}{2(0.050)^{3/2}}=%s\\,\\mathrm{T}$." % sci(Bax), "The centre value $\\mu_0I/2R=2.51\\times10^{-5}\\,\\mathrm{T}$ is ten times larger: the field falls quickly along the axis."))
    txt(B, c, t, 2, "The magnetic field at the centre of a circular current loop points", "along the axis, perpendicular to the plane of the loop (right-hand rule)", ["in the plane of the loop, tangent to the wire", "radially outward in the plane of the loop", "nowhere: the field at the centre is zero"],
        ex("By the right-hand rule (curl the fingers along the current, the thumb gives $\\vec B$) the field through the centre is along the axis. Unlike the electric field of a charged ring, it is NOT zero there."))

# =============================================================================================== chapter 7
def induction(B):
    c = "c7"
    t = "RL circuits"
    L, R, eps = 0.60, 24.0, 12.0; tau = L / R; If = eps / R
    num(B, c, t, 1, "What is the time constant of an RL circuit with $L=0.50\\,\\mathrm{H}$ and $R=25\\,\\Omega$?",
        0.50 / 25.0, [0.50 * 25.0, 25.0 / 0.50, 0.50 / 50.0, 0.50 / 25.0 * 2], "s",
        ex("$\\tau=\\dfrac LR=\\dfrac{0.50\\,\\mathrm{H}}{25\\,\\Omega}=%s\\,\\mathrm{s}$ (the units $\\mathrm{H/\\Omega}$ are seconds)." % sci(0.50 / 25.0)))
    I_tau = If * (1 - math.exp(-1))
    num(B, c, t, 2, "A $12\\,\\mathrm{V}$ battery is connected at $t=0$ to a coil with $L=0.60\\,\\mathrm{H}$ in series with $R=24\\,\\Omega$. What is the current at $t=\\tau=L/R$?",
        I_tau, [If, If * math.exp(-1), If / 2, 1 - math.exp(-1)], "A",
        ex("Final current $I_f=\\dfrac{\\varepsilon}{R}=0.50\\,\\mathrm{A}$ and $\\tau=\\dfrac LR=0.025\\,\\mathrm{s}$.", "$I(\\tau)=I_f(1-e^{-1})=0.50(0.632)=%s\\,\\mathrm{A}$ (63 percent of the final value; $0.184$ would be the decaying case)." % sci(I_tau)))
    txt(B, c, t, 2, "A battery is connected to an inductor in series with a resistor and the switch is closed at $t=0$. Just after closing, the current and the voltage across the inductor are", "$I=0$ and $V_L=\\varepsilon$",
        ["$I=\\varepsilon/R$ and $V_L=0$", "$I=\\varepsilon/R$ and $V_L=\\varepsilon$", "$I=0$ and $V_L=0$"],
        ex("The inductor opposes any sudden change of current, so $I(0)=0$. With no current there is no voltage across $R$, so the inductor takes the whole emf: $V_L=L\\,dI/dt=\\varepsilon$. At the end the roles swap: $I=\\varepsilon/R$, $V_L=0$."))
    I0, tau2, I1 = 0.80, 0.050, 0.20; tt = tau2 * math.log(I0 / I1)
    num(B, c, t, 3, "The current in a decaying RL circuit is $I(t)=I_0e^{-t/\\tau}$ with $I_0=0.80\\,\\mathrm{A}$ and $\\tau=0.050\\,\\mathrm{s}$. After how long has it fallen to $0.20\\,\\mathrm{A}$?",
        tt, [4 * tau2, tau2 * math.log(2), 3 * tau2], "s",
        ex("$e^{-t/\\tau}=\\dfrac{0.20}{0.80}=\\dfrac14\\Rightarrow t=\\tau\\ln4=(0.050)(1.386)=%s\\,\\mathrm{s}$ (not $4\\tau$)." % sci(tt)))
    U = 0.5 * L * If ** 2
    num(B, c, t, 2, "The circuit of the previous problems ($\\varepsilon=12\\,\\mathrm{V}$, $R=24\\,\\Omega$, $L=0.60\\,\\mathrm{H}$) reaches its final current. How much energy is stored in the inductor?",
        U, [L * If ** 2, L * If, 0.5 * L ** 2 * If, 0.5 * If ** 2 * R], "J",
        ex("$U=\\tfrac12LI_f^2=\\tfrac12(0.60)(0.50)^2=%s\\,\\mathrm{J}$." % sci(U)))
    VL = eps * math.exp(-1)
    num(B, c, t, 3, "In the same circuit ($\\varepsilon=12\\,\\mathrm{V}$) after the battery is switched on, what is the voltage across the inductor at $t=\\tau$?",
        VL, [eps, eps * (1 - math.exp(-1)), eps / 2], "V",
        ex("$V_L=\\varepsilon-IR=\\varepsilon e^{-t/\\tau}$, so at $t=\\tau$: $V_L=12e^{-1}=%s\\,\\mathrm{V}$ ($7.58\\,\\mathrm{V}$ is the voltage across the resistor)." % sci(VL)))
    num(B, c, t, 2, "A $12\\,\\mathrm{V}$ battery is connected at $t=0$ to a coil with $L=0.60\\,\\mathrm{H}$ in series with $24\\,\\Omega$. What is the initial rate of increase of the current, $dI/dt$ at $t=0$?",
        eps / L, [eps / R, eps * L, R / L], "A/s",
        ex("At $t=0$ the current is zero, so $\\varepsilon=L\\dfrac{dI}{dt}$: $\\dfrac{dI}{dt}=\\dfrac{\\varepsilon}{L}=\\dfrac{12}{0.60}=%s\\,\\mathrm{A/s}$ (the resistor does not matter at that instant)." % sci(eps / L)))
    # ------------------------------------------------------------------ motional emf
    t = "Motional emf"
    Bm, lm, vm = 0.50, 0.40, 6.0; em = Bm * lm * vm
    num(B, c, t, 1, "A metal rod $0.40\\,\\mathrm{m}$ long moves at $6.0\\,\\mathrm{m/s}$ perpendicular to a uniform field of $0.50\\,\\mathrm{T}$ and to its own length. What emf is induced between its ends?",
        em, [em / 2, em * 2, Bm * vm / lm, Bm * lm / vm], "V",
        ex("$\\varepsilon=Blv=(0.50)(0.40)(6.0)=%s\\,\\mathrm{V}$." % sci(em)))
    Rm = 0.30; Im = em / Rm; Fm = Bm * Im * lm; Pm = Fm * vm; check(Pm, Im ** 2 * Rm)
    num(B, c, t, 2, "The rod above slides on rails that complete a circuit of total resistance $0.30\\,\\Omega$. What current flows?",
        Im, [em * Rm, Im / 2, Im * 2], "A",
        ex("$I=\\dfrac{\\varepsilon}{R}=\\dfrac{1.2}{0.30}=%s\\,\\mathrm{A}$." % sci(Im)))
    num(B, c, t, 2, "What external force is needed to keep the rod moving at constant speed ($B=0.50\\,\\mathrm{T}$, $l=0.40\\,\\mathrm{m}$, $I=4.0\\,\\mathrm{A}$)?",
        Fm, [Bm * Im / lm, Bm * lm, Fm * vm], "N",
        ex("The magnetic force on the rod is $F=IlB=(4.0)(0.40)(0.50)=%s\\,\\mathrm{N}$, opposing the motion (Lenz's law); the external force must balance it." % sci(Fm)))
    num(B, c, t, 3, "At what rate is energy dissipated in the circuit ($\\varepsilon=1.2\\,\\mathrm{V}$, $I=4.0\\,\\mathrm{A}$, $R=0.30\\,\\Omega$, rod speed $6.0\\,\\mathrm{m/s}$)?",
        Pm, [Pm / 2, 4 * Pm, Fm], "W",
        ex("$P=I^2R=(4.0)^2(0.30)=%s\\,\\mathrm{W}$, which equals the mechanical power supplied, $Fv=(0.80)(6.0)=4.8\\,\\mathrm{W}$ - energy is conserved." % sci(Pm)))
    def cr(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    check(cr((1, 0, 0), (0, 0, 1))[1], -1.0)
    txt(B, c, t, 2, "A conducting rod, lying along the $y$ axis, moves to the right (along $+x$) through a uniform magnetic field pointing out of the page ($+z$). In which direction are positive charges pushed along the rod?",
        "Towards the bottom of the page ($-y$)", ["Towards the top of the page ($+y$)", "Into the page", "To the right"],
        ex("$\\vec F=q\\vec v\\times\\vec B$ with $\\vec v=v\\hat x$ and $\\vec B=B\\hat z$: $\\hat x\\times\\hat z=-\\hat y$. The positive charges move to the bottom end, so the bottom end is at the higher potential."))
    Bw, wr, Lr = 0.20, 30.0, 0.50; er = 0.5 * Bw * wr * Lr ** 2
    num(B, c, t, 3, "A metal rod of length $0.50\\,\\mathrm{m}$ rotates about one end at $30\\,\\mathrm{rad/s}$ in a uniform field of $0.20\\,\\mathrm{T}$ perpendicular to its plane of rotation. What emf is induced between its ends?",
        er, [Bw * wr * Lr ** 2, Bw * wr * Lr, 0.5 * er], "V",
        ex("The speed grows linearly along the rod ($v=\\omega r$), so the average speed is $\\omega L/2$: $\\varepsilon=B\\dfrac{\\omega L}2L=\\tfrac12B\\omega L^2=\\tfrac12(0.20)(30)(0.50)^2=%s\\,\\mathrm{V}$." % sci(er)))
    txt(B, c, t, 2, "A rod slides at constant speed along rails closing a circuit of fixed resistance. If the speed is doubled, the external power needed to keep it moving", "is multiplied by four",
        ["is doubled", "is unchanged", "is multiplied by eight"],
        ex("$\\varepsilon\\propto v$, so $I\\propto v$; the force $F=IlB\\propto v$; the power $P=Fv\\propto v^2$ (equivalently $P=\\varepsilon^2/R$): doubling the speed quadruples the power."))
    # ------------------------------------------------------------------ induced electric fields
    t = "Induced electric fields"
    dBdt, ri = 0.020, 0.030; Ei = 0.5 * ri * dBdt
    num(B, c, t, 2, "The magnetic field in a long solenoid of radius $0.050\\,\\mathrm{m}$ changes at $0.020\\,\\mathrm{T/s}$. What is the magnitude of the induced electric field at a point $0.030\\,\\mathrm{m}$ from the axis, inside the solenoid?",
        Ei, [ri * dBdt, math.pi * ri ** 2 * dBdt, Ei / 2], "V/m",
        ex("Faraday: $E(2\\pi r)=\\pi r^2\\dfrac{dB}{dt}\\Rightarrow E=\\dfrac r2\\dfrac{dB}{dt}=\\dfrac{0.030}{2}(0.020)=%s\\,\\mathrm{V/m}$ (tangent to a circle around the axis)." % sci(Ei)))
    Rs, ro = 0.050, 0.10; Eo = Rs ** 2 / (2 * ro) * dBdt
    num(B, c, t, 3, "For the same solenoid (radius $0.050\\,\\mathrm{m}$, $dB/dt=0.020\\,\\mathrm{T/s}$), what is the induced electric field at $0.10\\,\\mathrm{m}$ from the axis, OUTSIDE the solenoid?",
        Eo, [ro / 2 * dBdt, Rs / 2 * dBdt, Eo / 2], "V/m",
        ex("Outside, only the flux inside the solenoid counts: $E(2\\pi r)=\\pi R^2\\dfrac{dB}{dt}\\Rightarrow E=\\dfrac{R^2}{2r}\\dfrac{dB}{dt}=\\dfrac{(0.050)^2}{2(0.10)}(0.020)=%s\\,\\mathrm{V/m}$." % sci(Eo), "The field is NOT zero outside even though $B=0$ there: it falls as $1/r$."))
    txt(B, c, t, 2, "A copper plate swings between the poles of a magnet. The eddy currents induced in the plate", "produce a force that opposes the motion (magnetic braking)",
        ["accelerate the plate", "have no effect on the motion", "flow in straight lines parallel to the field"],
        ex("By Lenz's law the induced currents oppose the change of flux that causes them, so the force on them opposes the motion; the mechanical energy is turned into heat in the plate."))
    txt(B, c, t, 2, "The iron core of a transformer is built from thin insulated sheets (laminations) in order to", "reduce the energy lost to eddy currents",
        ["increase the eddy currents", "reduce the magnetic field in the core", "make the core lighter only"],
        ex("Slicing the core into insulated sheets confines the eddy currents to small loops, which raises the resistance of the current paths and cuts the $I^2R$ heating."))
    rl, dBl = 0.040, 0.050; el = math.pi * rl ** 2 * dBl; check(el, 0.5 * rl * dBl * 2 * math.pi * rl)
    num(B, c, t, 3, "A circular loop of radius $0.040\\,\\mathrm{m}$ lies in a uniform field perpendicular to its plane that changes at $0.050\\,\\mathrm{T/s}$. What emf is induced around the loop?",
        el, [2 * el, el / 2, 2 * math.pi * rl * dBl], "V",
        ex("$|\\varepsilon|=\\dfrac{d\\Phi}{dt}=\\pi r^2\\dfrac{dB}{dt}=\\pi(0.040)^2(0.050)=%s\\,\\mathrm{V}$ (equivalently $E\\cdot2\\pi r$ with $E=\\tfrac r2\\dfrac{dB}{dt}$)." % sci(el)))
    # ------------------------------------------------------------------ magnetic flux
    t = "Magnetic flux"
    Bf, Af = 0.30, 0.020
    num(B, c, t, 1, "A uniform field of $0.30\\,\\mathrm{T}$ is perpendicular to a flat loop of area $0.020\\,\\mathrm{m^2}$. What is the magnetic flux through the loop?",
        Bf * Af, [Bf * Af / 2, Bf * Af * 2, Bf / Af], "Wb", sig=2,
        explain=ex("$\\Phi=BA\\cos0^\\circ=(0.30)(0.020)=%s\\,\\mathrm{Wb}$." % sci(Bf * Af, 2)))
    num(B, c, t, 2, "The plane of the same loop ($0.020\\,\\mathrm{m^2}$) makes an angle of $30^\\circ$ with the $0.30\\,\\mathrm{T}$ field. What is the flux?",
        Bf * Af * math.cos(rad(60)), [Bf * Af * math.cos(rad(30)), Bf * Af, 0.0], "Wb", sig=2,
        explain=ex("The angle in $\\Phi=BA\\cos\\theta$ is between $\\vec B$ and the NORMAL to the plane: $\\theta=90^\\circ-30^\\circ=60^\\circ$.", "$\\Phi=(0.30)(0.020)\\cos60^\\circ=%s\\,\\mathrm{Wb}$." % sci(Bf * Af * 0.5, 2)))
    Nc, Phi1 = 200, 2.0e-3
    num(B, c, t, 2, "A coil of $200$ turns has a flux of $2.0\\times10^{-3}\\,\\mathrm{Wb}$ through each turn. What is the flux linkage $N\\Phi$?",
        Nc * Phi1, [Phi1, Phi1 / Nc, Nc * Phi1 / 2], "Wb", sig=2,
        explain=ex("Faraday's law uses the flux linkage: $N\\Phi=(200)(2.0\\times10^{-3})=%s\\,\\mathrm{Wb}$." % sci(Nc * Phi1, 2)))
    txt(B, c, t, 2, "One weber is equal to", "$1\\,\\mathrm{T\\,m^2}$", ["$1\\,\\mathrm{T/m^2}$", "$1\\,\\mathrm{V/s}$", "$1\\,\\mathrm{A\\,m}$"],
        ex("$\\Phi=BA$, so $1\\,\\mathrm{Wb}=1\\,\\mathrm{T\\,m^2}$. Since $\\varepsilon=d\\Phi/dt$, it is also $1\\,\\mathrm{V\\,s}$ (volt-second), not volt per second."))
    Bk, Ak = 0.50, 0.040
    num(B, c, t, 3, "A loop of area $0.040\\,\\mathrm{m^2}$ in a $0.50\\,\\mathrm{T}$ field is rotated from a position where its normal is parallel to the field to one where the normal is perpendicular to it. What is the change in flux?",
        -Bk * Ak, [Bk * Ak, 0.0, -2 * Bk * Ak], "Wb", sig=2,
        explain=ex("Initially $\\Phi_i=BA=0.020\\,\\mathrm{Wb}$; finally $\\Phi_f=BA\\cos90^\\circ=0$.", "$\\Delta\\Phi=\\Phi_f-\\Phi_i=%s\\,\\mathrm{Wb}$ (a decrease)." % sci(-Bk * Ak, 2)))
    Bq, rq = 0.40, 0.050; Phiq = Bq * math.pi * rq ** 2
    num(B, c, t, 2, "A circular loop of radius $5.0\\,\\mathrm{cm}$ is perpendicular to a uniform field of $0.40\\,\\mathrm{T}$. What is the flux through it?",
        Phiq, [Bq * 2 * math.pi * rq * rq, Bq * math.pi * rq, Bq * rq * rq], "Wb",
        ex("$\\Phi=B\\pi r^2=(0.40)\\pi(0.050)^2=%s\\,\\mathrm{Wb}$ (area $\\pi r^2$, radius in metres)." % sci(Phiq)))

# =============================================================================================== chapters 8, 9, 11
def optics(B):
    c = "c8"
    t = "Reflection"
    num(B, c, t, 1, "A light ray strikes a plane mirror making an angle of $35^\\circ$ with the surface of the mirror. What is the angle of reflection?",
        55.0, [35.0, 70.0, 110.0, 90.0], "deg", sig=2,
        explain=ex("Angles are measured from the NORMAL: angle of incidence $=90^\\circ-35^\\circ=55^\\circ$, and the angle of reflection equals it: $55^\\circ$.", "$35^\\circ$ is the glancing angle; $110^\\circ$ is the angle between the incident and reflected rays."))
    num(B, c, t, 2, "A plane mirror is rotated by $10^\\circ$ about an axis in its surface, perpendicular to the plane of incidence, while the incident ray stays fixed. Through what angle does the reflected ray turn?",
        20.0, [10.0, 5.0, 40.0], "deg", sig=2,
        explain=ex("Rotating the mirror by $\\alpha$ rotates its normal by $\\alpha$, so both the angle of incidence and the angle of reflection change by $\\alpha$: the reflected ray turns by $2\\alpha=20^\\circ$."))
    txt(B, c, t, 2, "A ray of light is reflected successively by two plane mirrors that meet at a right angle (the ray lies in a plane perpendicular to both mirrors). The emerging ray is", "parallel to the incoming ray but travelling in the opposite direction",
        ["perpendicular to the incoming ray", "parallel to the incoming ray and in the same direction", "along the same line as the incoming ray, in the same direction"],
        ex("Each reflection reverses the component of the direction perpendicular to that mirror. Two perpendicular mirrors reverse both components, so the ray returns anti-parallel to its original direction (a corner reflector)."))
    v = 1.5
    num(B, c, t, 2, "A person walks towards a large plane mirror at $1.5\\,\\mathrm{m/s}$. At what speed does the person's image approach the person?",
        2 * v, [v, 0.0, 4 * v], "m/s",
        ex("The image is as far behind the mirror as the person is in front: if the person moves $1.5\\,\\mathrm{m/s}$ towards the mirror, the image moves $1.5\\,\\mathrm{m/s}$ towards it from behind, so they close at $2\\times1.5=%s\\,\\mathrm{m/s}$." % sci(2 * v)))
    h = 1.80
    num(B, c, t, 3, "What is the minimum height of a plane mirror hanging on a wall in which a person $1.80\\,\\mathrm{m}$ tall can see their whole body?",
        h / 2, [h, h / 4, 1.2, 1.35], "m",
        ex("For any distance from the mirror the light from the top of the head and from the feet reaches the eyes after reflecting at points that are half-way between eye level and head, and eye level and feet. The mirror needs only half the person's height: $\\tfrac12(1.80)=%s\\,\\mathrm{m}$." % sci(h / 2)))
    txt(B, c, t, 2, "A sheet of white paper scatters light in all directions even though every ray obeys the law of reflection. This is because", "the surface is rough, so the normal points in a different direction at each point",
        ["the paper absorbs the light and re-emits it", "the law of reflection does not hold for rough surfaces", "light changes its wavelength on reflection from paper"],
        ex("On a microscopic scale the paper surface is rough: neighbouring rays meet surface elements with different normals and are reflected in different directions (diffuse reflection). A mirror's polished surface has one normal over large areas (specular reflection)."))
    # ------------------------------------------------------------------ Snell
    t = "Snell's law"
    n1, n2, th1 = 1.00, 1.50, 40.0; th2 = math.degrees(math.asin(n1 * math.sin(rad(th1)) / n2))
    num(B, c, t, 2, "Light in air strikes a glass surface ($n=1.50$) at an angle of incidence of $40^\\circ$. What is the angle of refraction?",
        th2, [th1 / n2, math.degrees(math.asin(n2 * math.sin(rad(th1)))), th1 * n2], "deg",
        ex("Snell's law: $n_1\\sin\\theta_1=n_2\\sin\\theta_2$, so $\\sin\\theta_2=\\dfrac{\\sin40^\\circ}{1.50}=0.429$ and $\\theta_2=%s^\\circ$." % sci(th2), "The angles are not proportional ($40/1.50=26.7$); the ray bends towards the normal in the denser medium."))
    d_, nw = 1.20, 1.33; dap = d_ / nw
    num(B, c, t, 2, "A coin lies at the bottom of a pool of water ($n=1.33$) $1.20\\,\\mathrm{m}$ deep. Looking almost straight down, at what apparent depth does the coin appear?",
        dap, [d_ * nw, d_, d_ / 2], "m",
        ex("For near-normal viewing the apparent depth is $d'=\\dfrac{d}{n}=\\dfrac{1.20}{1.33}=%s\\,\\mathrm{m}$: the bottom seems closer to the surface." % sci(dap)))
    nw, ng, tw = 1.33, 1.50, 30.0; tg = math.degrees(math.asin(nw * math.sin(rad(tw)) / ng))
    num(B, c, t, 3, "Light in water ($n=1.33$) meets a glass surface ($n=1.50$) at an angle of incidence of $30^\\circ$. What is the angle of refraction in the glass?",
        tg, [math.degrees(math.asin(ng * math.sin(rad(tw)) / nw)), tw, math.degrees(math.asin(math.sin(rad(tw)) / ng))], "deg",
        ex("$n_1\\sin\\theta_1=n_2\\sin\\theta_2\\Rightarrow\\sin\\theta_2=\\dfrac{1.33\\sin30^\\circ}{1.50}=0.443$, $\\theta_2=%s^\\circ$ (a small bend towards the normal; the indices must be used in the right order)." % sci(tg)))
    # ------------------------------------------------------------------ light as EM wave
    t = "Light as an electromagnetic wave"
    E0 = 150.0; B0 = E0 / C_LIGHT
    num(B, c, t, 2, "The electric field amplitude of an electromagnetic wave in vacuum is $150\\,\\mathrm{V/m}$. What is the amplitude of its magnetic field?",
        B0, [B0 / 2, 2 * B0, 10 * B0, B0 / 10], "T",
        ex("In a vacuum $E=cB$ at every instant, so $B_0=\\dfrac{E_0}{c}=\\dfrac{150}{3.00\\times10^8}=%s\\,\\mathrm{T}$." % sci(B0)))
    lam = 500e-9; f = C_LIGHT / lam
    num(B, c, t, 2, "What is the frequency of green light of wavelength $500\\,\\mathrm{nm}$ in vacuum?",
        f, [2 * f, f / 2, f / 1000, 1000 * f], "Hz",
        ex("$f=\\dfrac c\\lambda=\\dfrac{3.00\\times10^8}{500\\times10^{-9}}=%s\\,\\mathrm{Hz}$ (convert nanometres to metres)." % sci(f)))
    # ------------------------------------------------------------------ chapter 9
    c, t = "c9", "Refraction at a surface"
    txt(B, c, t, 2, "A point object in air is $20\\,\\mathrm{cm}$ in front of a convex spherical glass surface ($n=1.50$, radius of curvature $10\\,\\mathrm{cm}$). Where is the image?",
        "At infinity: the rays leave the surface parallel", ["$30\\,\\mathrm{cm}$ inside the glass", "$60\\,\\mathrm{cm}$ inside the glass", "A virtual image $20\\,\\mathrm{cm}$ in front of the surface"],
        ex("$\\dfrac{n_1}{s}+\\dfrac{n_2}{s'}=\\dfrac{n_2-n_1}{R}$: $\\dfrac1{20}+\\dfrac{1.50}{s'}=\\dfrac{0.50}{10}=0.050$.", "So $\\dfrac{1.50}{s'}=0$ and $s'\\to\\infty$: the object is at the first focal point of the surface."))
    s2, R2, n1, n2 = 30.0, 10.0, 1.00, 1.50; sp = n2 / ((n2 - n1) / R2 - n1 / s2); check(n1 / s2 + n2 / sp, (n2 - n1) / R2)
    num(B, c, t, 2, "A point object in air is $30\\,\\mathrm{cm}$ from a convex spherical glass surface ($n=1.50$, $R=10\\,\\mathrm{cm}$). How far from the surface, inside the glass, is the image?",
        sp, [1 / ((n2 - n1) / R2 - 1 / s2), 45.0, 2 * sp], "cm",
        ex("$\\dfrac1{30}+\\dfrac{1.50}{s'}=\\dfrac{0.50}{10}\\Rightarrow\\dfrac{1.50}{s'}=0.0500-0.0333=0.0167$.", "$s'=%s\\,\\mathrm{cm}$ (real image, inside the glass). The thin-lens form $\\tfrac1s+\\tfrac1{s'}$ would give $60\\,\\mathrm{cm}$: forgetting $n_2$ on the image side." % sci(sp)))
    txt(B, c, t, 3, "A small fish sits at the centre of a thin spherical glass bowl of radius $15\\,\\mathrm{cm}$ filled with water ($n=1.33$). Seen from outside the bowl, the fish appears",
        "at the centre of the bowl, magnified by a factor $1.33$", ["closer to the surface, at $11\\,\\mathrm{cm}$ from the centre", "at the centre of the bowl, with its actual size", "farther from the surface, at $20\\,\\mathrm{cm}$ from the centre"],
        ex("With $s=R=15\\,\\mathrm{cm}$ and the centre of curvature on the object side ($R_s=-15\\,\\mathrm{cm}$): $\\dfrac{1.33}{15}+\\dfrac1{s'}=\\dfrac{1-1.33}{-15}=0.0220\\Rightarrow s'=-15\\,\\mathrm{cm}$: the image is at the same place (virtual).", "Magnification $m=-\\dfrac{n_1s'}{n_2s}=-\\dfrac{1.33(-15)}{1(15)}=+1.33$: the rays strike the surface along the normal, so they are not bent, but the fish looks larger."))
    # ------------------------------------------------------------------ chapter 11
    c, t = "c11", "X-ray diffraction"
    lam, d, m = 0.154e-9, 0.282e-9, 1; thx = math.degrees(math.asin(m * lam / (2 * d)))
    num(B, c, t, 2, "X-rays of wavelength $0.154\\,\\mathrm{nm}$ are reflected from crystal planes $0.282\\,\\mathrm{nm}$ apart. At what glancing angle is the first-order Bragg maximum found?",
        thx, [math.degrees(math.asin(lam / d)), 2 * thx, math.degrees(math.asin(lam / (4 * d)))], "deg",
        ex("Bragg's law $2d\\sin\\theta=m\\lambda$ with $m=1$: $\\sin\\theta=\\dfrac{0.154}{2(0.282)}=0.273$, $\\theta=%s^\\circ$." % sci(thx), "Do not drop the factor 2; the beam is deviated by $2\\theta=31.7^\\circ$ from its original direction."))
    th_, lam2 = 20.0, 0.154; dd = lam2 / (2 * math.sin(rad(th_)))
    num(B, c, t, 2, "A first-order Bragg reflection of X-rays of wavelength $0.154\\,\\mathrm{nm}$ is seen at a glancing angle of $20.0^\\circ$. What is the spacing of the crystal planes?",
        dd, [lam2 / math.sin(rad(th_)), lam2 / (2 * math.cos(rad(th_))), lam2 / 4], "nm",
        ex("$d=\\dfrac{m\\lambda}{2\\sin\\theta}=\\dfrac{0.154}{2\\sin20.0^\\circ}=%s\\,\\mathrm{nm}$." % sci(dd)))
    mmax = math.floor(2 * 0.282 / 0.154)
    num(B, c, t, 3, "X-rays of wavelength $0.154\\,\\mathrm{nm}$ reflect from planes $0.282\\,\\mathrm{nm}$ apart. What is the highest order $m$ of Bragg reflection that can be observed?",
        float(mmax), [4.0, 2.0, 1.0], "",
        ex("$\\sin\\theta\\le1\\Rightarrow m\\le\\dfrac{2d}{\\lambda}=\\dfrac{2(0.282)}{0.154}=3.66$, so the highest observable order is $m=%s$ (orders are integers)." % sci(float(mmax), 1)))
    txt(B, c, t, 1, "In Bragg's law $2d\\sin\\theta=m\\lambda$ the angle $\\theta$ is measured between the incident X-ray beam and", "the crystal planes (the glancing angle)",
        ["the normal to the crystal planes", "the scattered beam", "the surface of the sample holder"],
        ex("Bragg's $\\theta$ is the GLANCING angle with the reflecting planes (unlike optics, where angles are taken from the normal). The path difference between rays from adjacent planes is $2d\\sin\\theta$."))
    txt(B, c, t, 2, "X-rays rather than visible light are used to study the structure of crystals because", "their wavelength is comparable to the spacing of the atoms ($\\sim0.1\\,\\mathrm{nm}$)",
        ["they are more intense than visible light", "crystals do not absorb them", "they travel faster in a crystal"],
        ex("Diffraction needs a wavelength of the order of the spacing: visible light ($400$-$700\\,\\mathrm{nm}$) is thousands of times longer than the atomic spacing, so a crystal would act like a mirror for it; X-rays ($\\sim0.1\\,\\mathrm{nm}$) are diffracted."))
    t = "Combined interference and diffraction"
    a, dsl = 0.10, 0.50; nfr = 2 * int(round(dsl / a)) - 1
    num(B, c, t, 2, "A double slit has slit separation $d=0.50\\,\\mathrm{mm}$ and slit width $a=0.10\\,\\mathrm{mm}$. How many bright interference fringes lie within the central diffraction maximum?",
        float(nfr), [5.0, 10.0, 11.0], "",
        ex("The first diffraction minimum is at $a\\sin\\theta=\\lambda$ and the $m$-th fringe at $d\\sin\\theta=m\\lambda$, so they coincide when $m=d/a=5$ (that fringe is missing).", "Visible fringes: $m=-4,\\dots,+4$, i.e. $2(d/a)-1=%s$." % sci(float(nfr), 1)))
    nfr2 = 2 * int(round(0.40 / 0.10)) - 1
    num(B, c, t, 2, "A double slit has $d=0.40\\,\\mathrm{mm}$ and $a=0.10\\,\\mathrm{mm}$. How many bright fringes lie within the central diffraction peak?",
        float(nfr2), [4.0, 8.0, 9.0], "",
        ex("$d/a=4$: the fourth-order fringe falls on the first diffraction minimum and is missing, leaving $m=-3,\\dots,+3$: $2(4)-1=%s$ fringes." % sci(float(nfr2), 1)))
    txt(B, c, t, 3, "In a double-slit experiment the slit separation is $d=3a$, where $a$ is the width of each slit. Which interference orders are missing from the pattern?", "$m=\\pm3,\\ \\pm6,\\dots$",
        ["$m=\\pm1,\\ \\pm2$", "$m=\\pm2,\\ \\pm4,\\dots$", "None: every order is visible"],
        ex("An order is missing when the interference maximum $d\\sin\\theta=m\\lambda$ coincides with a diffraction minimum $a\\sin\\theta=n\\lambda$: $m=n\\dfrac da=3n$, i.e. $m=\\pm3,\\pm6,\\dots$"))
    txt(B, c, t, 2, "In the pattern of a double slit with slits of finite width, the spacing of the bright fringes is set by ____ and the overall envelope of intensity by ____.", "the slit separation $d$; the slit width $a$",
        ["the slit width $a$; the slit separation $d$", "the wavelength only; the screen distance only", "the slit separation $d$; the slit separation $d$"],
        ex("Fringe spacing $\\Delta y=\\lambda L/d$ comes from interference between the two slits; the envelope is the single-slit diffraction pattern, whose width is set by $\\lambda L/a$."))
    lam3, a3 = 600e-9, 0.10e-3; thm = math.degrees(math.asin(lam3 / a3))
    num(B, c, t, 3, "Light of wavelength $600\\,\\mathrm{nm}$ passes through a double slit with $d=0.30\\,\\mathrm{mm}$ and $a=0.10\\,\\mathrm{mm}$. At what angle is the first minimum of the diffraction envelope?",
        thm, [math.degrees(math.asin(lam3 / 0.30e-3)), 2 * thm, thm / 6], "deg",
        ex("The envelope minima are at $a\\sin\\theta=n\\lambda$: $\\sin\\theta=\\dfrac{600\\times10^{-9}}{0.10\\times10^{-3}}=6.0\\times10^{-3}$, $\\theta=%s^\\circ$ ($d$ would give the fringe spacing $0.115^\\circ$ instead)." % sci(thm)))

# =============================================================================================== assembly
def build():
    B = Bank("PH2", seed=20261105)
    for fn in (electrostatics, magnetic_forces, magnetic_fields, induction, optics):
        fn(B)
    return B

def lint(B):
    problems = []
    for q in B.items:
        for t in [q["q"], q["explain"]] + list(q["opts"]):
            if any(ord(ch) < 32 and ch != "\n" for ch in t):
                problems.append((q["id"], "control character", t[:60]))
            if t.replace("\\$", "").count("$") % 2:
                problems.append((q["id"], "unbalanced $", t[:60]))
            for seg in t.split("$")[1::2]:
                if "%" in seg.replace("\\%", ""):
                    problems.append((q["id"], "unescaped % inside math", seg[:60]))
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
    print(merge(Bank("PH2", seed=1), G_))
    print(sorted(Counter((i["ch"], i["topic"]) for i in G_.items).items()))
    print("skipped", len(G_.skipped), "fillers", len(FILLED))
    for x in G_.skipped + FILLED: print("  ", x)
