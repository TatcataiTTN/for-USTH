# -*- coding: utf-8 -*-
"""Physics II (PHY1.002) - Magnetism: chapter 5 Magnetic force, 6 Magnetic fields of currents, 7 Induction and inductance.
Sources: magnetism lecture (2025-26, chapters 5-7), the magnetism / induction tutoring slides (Halliday problems 28-30), formula sheets."""
import math
import numpy as np
from phys_common import *
from phys_verify import lorentz_orbit, wire_field, arc_path, rl_current, integrate
import figs

LEC5 = "Magnetism lecture (2025-26), chapter 5"
LEC6 = "Magnetism lecture (2025-26), chapter 6"
LEC7 = "Magnetism lecture (2025-26), chapter 7"
TUT = "Magnetism tutoring slides"
FIN = "Final tutoring slides 2025-26 (induction)"
GEN = lambda s: "Generated, same style as: " + s

def vec3(v, unit="", sig=3):
    """(a i + b j + c k) in LaTeX with unit vectors, zero components dropped."""
    parts = []
    for x, name in zip(v, ("\\hat i", "\\hat j", "\\hat k")):
        if abs(x) < 1e-12 * max(1.0, max(abs(t) for t in v)):
            continue
        s_ = sci(abs(x), sig) + "\\," + name
        parts.append(("-" if x < 0 else ("+" if parts else "")) + s_)
    return "$(" + "".join(parts) + ")" + unit_tex(unit) + "$"

# =============================================================================================== chapter 5
def ch5(B):
    c = "c5"
    # ---------------------------------------------------------------- force on an electron / proton (tutoring slides, Q1)
    v = np.array([2.0e6, 3.0e6, 0.0]); Bf = np.array([0.030, -0.15, 0.0])
    Fe = -E_CH * np.cross(v, Bf); Fp = E_CH * np.cross(v, Bf)
    check(np.linalg.norm(Fe), E_CH * abs(v[0] * Bf[1] - v[1] * Bf[0]))
    mcq_num(B, c, "Magnetic force on a charge", 2, "An electron has velocity $\\vec v=(2.0\\times10^{6}\\hat i+3.0\\times10^{6}\\hat j)\\,\\mathrm{m/s}$ in a uniform field $\\vec B=(0.030\\,\\hat i-0.15\\,\\hat j)\\,\\mathrm{T}$. What is the magnitude of the magnetic force on it?", np.linalg.norm(Fe),
            [E_CH * np.linalg.norm(v) * np.linalg.norm(Bf), E_CH * abs(v[0] * Bf[0]), E_CH * abs(v[1] * Bf[1]), np.linalg.norm(Fe) * 2], "N", ex("$\\vec F=q\\,\\vec v\\times\\vec B$ with $q=-e$. Both vectors lie in the $xy$ plane, so the cross product points along $z$: $(\\vec v\\times\\vec B)_z=v_xB_y-v_yB_x=(2.0\\times10^6)(-0.15)-(3.0\\times10^6)(0.030)=-3.9\\times10^{5}\\,\\mathrm{T\\,m/s}$.", "$|F|=e\\,(3.9\\times10^5)=6.2\\times10^{-14}\\,\\mathrm{N}$."), TUT + ", Question 1", sig=2)
    mcq_pick(B, c, "Magnetic force on a charge", 2, "For the electron of the previous problem ($\\vec v$ and $\\vec B$ both in the $xy$ plane, $(\\vec v\\times\\vec B)_z<0$), the force points along", ["$+\\hat k$ for the electron and $-\\hat k$ for a proton", "$-\\hat k$ for the electron and $+\\hat k$ for a proton", "$+\\hat k$ for both", "$\\hat i$ for the electron"], 0, ex("$\\vec v\\times\\vec B=-3.9\\times10^{5}\\,\\hat k$. For a positive charge $\\vec F\\parallel\\vec v\\times\\vec B$ (that is $-\\hat k$); for the electron the force is reversed: $+\\hat k$ (out of the plane)."), TUT + ", Question 1(b)", "src")
    q, v0, Bf0, th = E_CH, 3.0e6, 0.40, 30.0
    F = q * v0 * Bf0 * math.sin(math.radians(th))
    mcq_num(B, c, "Magnetic force on a charge", 1, "A proton moves at $3.0\\times10^{6}\\,\\mathrm{m/s}$ at $30^\\circ$ to a uniform $0.40\\,\\mathrm{T}$ magnetic field. What is the magnetic force on it?", F, [q * v0 * Bf0, q * v0 * Bf0 * math.cos(math.radians(th)), F * 2, F / 2], "N", ex("$F=qvB\\sin\\theta=(1.602\\times10^{-19})(3.0\\times10^6)(0.40)\\sin30^\\circ=9.6\\times10^{-14}\\,\\mathrm{N}$. It is perpendicular to both $\\vec v$ and $\\vec B$."), GEN(TUT + ", Question 1"), "gen", sig=2)
    # ---------------------------------------------------------------- circular motion
    K, Bc = 1000.0 * E_CH, 0.010
    ve = math.sqrt(2 * K / M_E); r = M_E * ve / (E_CH * Bc)
    orb = lorentz_orbit(-E_CH, M_E, ve, Bc)
    check(r, orb["radius"], 1e-3, "orbit radius by numerical integration of the Lorentz force")
    mcq_num(B, c, "Motion in a magnetic field", 2, "An electron with kinetic energy $1.0\\,\\mathrm{keV}$ moves perpendicular to a uniform field of $0.010\\,\\mathrm{T}$. What is the radius of its circular path?", r, [r * math.sqrt(2), r / 2, r * 2, M_E * ve ** 2 / (E_CH * Bc)], "m", ex("Speed from the energy: $v=\\sqrt{\\dfrac{2K}{m}}=\\sqrt{\\dfrac{2(1.0\\times10^3)(1.602\\times10^{-19})}{9.11\\times10^{-31}}}=1.9\\times10^{7}\\,\\mathrm{m/s}$.", "The magnetic force supplies the centripetal force: $evB=\\dfrac{mv^2}{r}\\Rightarrow r=\\dfrac{mv}{eB}=\\dfrac{(9.11\\times10^{-31})(1.88\\times10^7)}{(1.602\\times10^{-19})(0.010)}=1.1\\times10^{-2}\\,\\mathrm{m}$. A numerical integration of the Lorentz force reproduces this radius."), LEC5 + ", 5.2 (charged particle in a magnetic field)", "gen", sig=2)
    T = 2 * math.pi * M_E / (E_CH * Bc)
    check(T, orb["period"], 3e-3, "period by numerical integration")
    mcq_num(B, c, "Motion in a magnetic field", 2, "What is the period of the circular motion of that electron in the $0.010\\,\\mathrm{T}$ field?", T, [2 * math.pi * r / (ve * 2), T * 2 * math.pi, T / (2 * math.pi), T * 2], "s", ex("$T=\\dfrac{2\\pi r}{v}=\\dfrac{2\\pi m}{eB}=\\dfrac{2\\pi(9.11\\times10^{-31})}{(1.602\\times10^{-19})(0.010)}=3.6\\times10^{-9}\\,\\mathrm{s}$ - independent of the speed (so $f=\\dfrac{eB}{2\\pi m}=2.8\\times10^{8}\\,\\mathrm{Hz}$)."), LEC5 + ", 5.2 and 5.8 (cyclotron frequency)", "gen", sig=2)
    mcq_num(B, c, "Motion in a magnetic field", 2, "A proton moves in a circle in a uniform field of $1.5\\,\\mathrm{T}$. What is its cyclotron frequency?", E_CH * 1.5 / (2 * math.pi * M_P), [E_CH * 1.5 / M_P, 2 * math.pi * E_CH * 1.5 / M_P, E_CH * 1.5 / (2 * math.pi * M_E), E_CH * 1.5 / (2 * math.pi * M_P) / 2], "Hz", ex("$f=\\dfrac{qB}{2\\pi m}=\\dfrac{(1.602\\times10^{-19})(1.5)}{2\\pi(1.673\\times10^{-27})}=2.3\\times10^{7}\\,\\mathrm{Hz}$ ($23\\,\\mathrm{MHz}$), whatever the proton's speed. ($qB/m$ is the angular frequency, $2\\pi f$.)"), LEC5 + ", 5.8 (cyclotrons)", "gen", sig=2)
    mp, vp, Bp = M_P, 2.0e7, 0.50
    mcq_num(B, c, "Motion in a magnetic field", 2, "A proton travelling at $2.0\\times10^{7}\\,\\mathrm{m/s}$ enters a uniform field of $0.50\\,\\mathrm{T}$ at right angles to it. What is the radius of its path?", mp * vp / (E_CH * Bp), [E_CH * Bp / (mp * vp), mp * vp ** 2 / (E_CH * Bp), mp * vp / (2 * E_CH * Bp), M_E * vp / (E_CH * Bp)], "m", ex("$r=\\dfrac{mv}{qB}=\\dfrac{(1.673\\times10^{-27})(2.0\\times10^7)}{(1.602\\times10^{-19})(0.50)}=0.42\\,\\mathrm{m}$."), GEN(LEC5 + ", 5.2"), "gen", sig=2)
    # helix
    v0, Bh, th = 2.0e6, 1.0e-3, 30.0
    rh = M_E * v0 * math.sin(math.radians(th)) / (E_CH * Bh); pitch = v0 * math.cos(math.radians(th)) * 2 * math.pi * M_E / (E_CH * Bh)
    hel = lorentz_orbit(-E_CH, M_E, v0, Bh, th)
    check(rh, hel["radius"], 2e-3); check(pitch, hel["pitch"], 3e-3)
    mcq_num(B, c, "Motion in a magnetic field", 3, "An electron with speed $2.0\\times10^{6}\\,\\mathrm{m/s}$ enters a uniform field of $1.0\\,\\mathrm{mT}$ at $30^\\circ$ to the field. What is the radius of its helical path?", rh, [M_E * v0 / (E_CH * Bh), M_E * v0 * math.cos(math.radians(th)) / (E_CH * Bh), rh / 2, rh * 2], "m", ex("Only the component of velocity PERPENDICULAR to $\\vec B$ makes it circle: $v_\\perp=v\\sin30^\\circ=1.0\\times10^6\\,\\mathrm{m/s}$.", "$r=\\dfrac{mv_\\perp}{eB}=\\dfrac{(9.11\\times10^{-31})(1.0\\times10^6)}{(1.602\\times10^{-19})(1.0\\times10^{-3})}=5.7\\times10^{-3}\\,\\mathrm{m}$."), GEN(LEC5 + ", 5.2"), "gen", sig=2)
    mcq_num(B, c, "Motion in a magnetic field", 3, "For the same electron (speed $2.0\\times10^{6}\\,\\mathrm{m/s}$ at $30^\\circ$ to a $1.0\\,\\mathrm{mT}$ field), what is the pitch of the helix (distance advanced along $\\vec B$ per turn)?", pitch, [v0 * 2 * math.pi * M_E / (E_CH * Bh), v0 * math.sin(math.radians(th)) * 2 * math.pi * M_E / (E_CH * Bh), pitch / 2, pitch * 2], "m", ex("The period is $T=\\dfrac{2\\pi m}{eB}=3.6\\times10^{-8}\\,\\mathrm{s}$; along the field the motion is uniform at $v_\\parallel=v\\cos30^\\circ=1.73\\times10^6\\,\\mathrm{m/s}$.", "$p=v_\\parallel T=(1.73\\times10^{6})(3.57\\times10^{-8})=6.2\\times10^{-2}\\,\\mathrm{m}$."), GEN(LEC5 + ", 5.2"), "gen", sig=2)
    # selector, mass spectrometer, Thomson
    Ef, Bs = 5.0e4, 0.25
    mcq_num(B, c, "Crossed fields", 2, "Charged particles pass undeflected through crossed fields $E=5.0\\times10^{4}\\,\\mathrm{V/m}$ and $B=0.25\\,\\mathrm{T}$ (velocity selector). What is their speed?", Ef / Bs, [Ef * Bs, Bs / Ef, math.sqrt(Ef / Bs), Ef / Bs / 2], "m/s", ex("No deflection when the electric and magnetic forces cancel: $qE=qvB\\Rightarrow v=\\dfrac EB=\\dfrac{5.0\\times10^4}{0.25}=2.0\\times10^{5}\\,\\mathrm{m/s}$ (independent of the charge and the mass)."), TUT + ", Thomson apparatus (crossed fields)", "gen", sig=2)
    m_ion, Vacc, Bm = 2.0e-26, 1000.0, 0.10
    rm = math.sqrt(2 * m_ion * Vacc / E_CH) / Bm
    vv = math.sqrt(2 * E_CH * Vacc / m_ion); check(rm, m_ion * vv / (E_CH * Bm))
    mcq_num(B, c, "Crossed fields", 3, "A singly charged ion of mass $2.0\\times10^{-26}\\,\\mathrm{kg}$ is accelerated from rest through $1000\\,\\mathrm{V}$ and then enters a uniform field of $0.10\\,\\mathrm{T}$ perpendicular to its velocity (mass spectrometer). What is the radius of its path?", rm, [math.sqrt(m_ion * Vacc / E_CH) / Bm, 2 * rm, rm / 2, m_ion * Vacc / (E_CH * Bm)], "m", ex("Energy: $\\tfrac12mv^2=eV\\Rightarrow v=\\sqrt{\\dfrac{2eV}{m}}=1.26\\times10^{5}\\,\\mathrm{m/s}$.", "$r=\\dfrac{mv}{eB}=\\dfrac1B\\sqrt{\\dfrac{2mV}{e}}=\\dfrac{1}{0.10}\\sqrt{\\dfrac{2(2.0\\times10^{-26})(1000)}{1.602\\times10^{-19}}}=0.16\\,\\mathrm{m}$."), GEN(TUT + ", motion of charges in E and B"), "gen", sig=2)
    # E needed for a given acceleration (tutoring slides, Q7)
    vel = np.array([0.0, 12.0e3, 15.0e3]); acc = np.array([2.00e12, 0.0, 0.0]); Bv = np.array([400e-6, 0.0, 0.0])
    E = -(M_E / E_CH) * acc - np.cross(vel, Bv)
    wrong1 = (M_E / E_CH) * acc - np.cross(vel, Bv)
    wrong2 = -(M_E / E_CH) * acc + np.cross(vel, Bv)
    wrong3 = (M_E / E_CH) * acc + np.cross(vel, Bv)
    check(float(E[0]), -11.37, 1e-3); check(float(E[1]), -6.00, 1e-9); check(float(E[2]), 4.80, 1e-9)
    mcq_text(B, c, "Crossed fields", 3, "An electron has initial velocity $(12.0\\,\\hat j+15.0\\,\\hat k)\\,\\mathrm{km/s}$ and constant acceleration $(2.00\\times10^{12}\\,\\mathrm{m/s^2})\\hat i$ in a region of uniform fields. If $\\vec B=(400\\,\\mu\\mathrm{T})\\,\\hat i$, what is the electric field $\\vec E$?",
             vec3(E, "N/C"), [vec3(wrong1, "N/C"), vec3(wrong2, "N/C"), vec3(wrong3, "N/C")],
             ex("Newton's second law: $m\\vec a=q(\\vec E+\\vec v\\times\\vec B)$ with $q=-e$, so $\\vec E=-\\dfrac me\\vec a-\\vec v\\times\\vec B$.", "$\\vec v\\times\\vec B=(0,\\ 6.00,\\ -4.80)\\,\\mathrm{N/C}$ and $-\\dfrac{m}{e}\\vec a=-11.4\\,\\hat i\\,\\mathrm{N/C}$.", "$\\vec E=(-11.4\\,\\hat i-6.00\\,\\hat j+4.80\\,\\hat k)\\,\\mathrm{N/C}$."), TUT + ", Question 7", "src")
    # ---------------------------------------------------------------- force on a wire
    Iw, Lw, Bw = 5000.0, 100.0, 60.0e-6
    F = Iw * Lw * Bw * math.sin(math.radians(70.0))
    mcq_num(B, c, "Force on a current-carrying wire", 2, "A horizontal power line carries $5000\\,\\mathrm{A}$ from south to north. Earth's field ($60.0\\,\\mu\\mathrm{T}$) points north and is inclined $70.0^\\circ$ below the horizontal. What is the magnitude of the magnetic force on $100\\,\\mathrm{m}$ of the line?", F, [Iw * Lw * Bw, Iw * Lw * Bw * math.cos(math.radians(70.0)), F * 2, F / 2], "N", ex("$F=ILB\\sin\\theta$ with $\\theta$ the angle between the current (north) and the field: $70.0^\\circ$.", "$F=(5000)(100)(60.0\\times10^{-6})\\sin70^\\circ=28.2\\,\\mathrm{N}$ (about $0.28\\,\\mathrm{N}$ per metre)."), TUT + ", Question 2", sig=3)
    mcq_pick(B, c, "Force on a current-carrying wire", 3, "For the same line (current towards the north, Earth's field towards the north and downwards), the direction of the magnetic force is", ["west (horizontal)", "east", "straight up", "straight down"], 0, ex("$\\vec F=I\\vec L\\times\\vec B$. With north $=\\hat y$, east $=\\hat x$, up $=\\hat z$: $\\vec B\\propto(\\cos70^\\circ\\hat y-\\sin70^\\circ\\hat z)$ and $\\hat y\\times(-\\hat z)=-\\hat x$: the force points west."), TUT + ", Question 2(b)", "src")
    for I_, L_, B_, th in [(4.0, 0.50, 0.30, 90.0), (6.0, 0.80, 0.25, 30.0)]:
        F = I_ * L_ * B_ * math.sin(math.radians(th))
        mcq_num(B, c, "Force on a current-carrying wire", 1, "A %s m straight wire carrying %s A makes an angle of %s° with a uniform %s T magnetic field. What is the magnetic force on the wire?" % (sci(L_), sci(I_), sci(th), sci(B_)), F, [I_ * L_ * B_, I_ * L_ * B_ * math.cos(math.radians(th)) if th != 90.0 else I_ * B_ / L_, F * 2, F / 2], "N", ex("$F=ILB\\sin\\theta=%s\\times%s\\times%s\\times\\sin%s^\\circ=%s\\,\\mathrm{N}$." % (sci(I_), sci(L_), sci(B_), sci(th), sci(F))), GEN(TUT + ", Question 2"), "gen", sig=3)
    # ---------------------------------------------------------------- torque on a loop
    mu = 0.20 * math.pi * 0.080 ** 2
    mv = mu * np.array([0.60, -0.80, 0.0]); Bl = np.array([0.25, 0.0, 0.30])
    tau = np.cross(mv, Bl); U = -float(np.dot(mv, Bl))
    check(float(tau[0]), -9.65e-4, 2e-3); check(float(tau[1]), -7.24e-4, 2e-3); check(float(tau[2]), 8.04e-4, 2e-3)
    mcq_num(B, c, "Torque on a current loop", 3, "A circular loop of radius $8.0\\,\\mathrm{cm}$ carries a current of $0.20\\,\\mathrm{A}$. Its magnetic moment points along the unit vector $0.60\\,\\hat i-0.80\\,\\hat j$. The loop is in a uniform field $\\vec B=(0.25\\,\\hat i+0.30\\,\\hat k)\\,\\mathrm{T}$. What is the magnitude of the torque on the loop?", float(np.linalg.norm(tau)), [mu * np.linalg.norm(Bl), mu * abs(Bl[0]), float(np.linalg.norm(tau)) * 2, float(np.linalg.norm(tau)) / 2], "N m", ex("$\\mu=IA=I\\pi r^2=(0.20)\\pi(0.080)^2=4.02\\times10^{-3}\\,\\mathrm{A\\,m^2}$, so $\\vec\\mu=(2.41\\times10^{-3}\\hat i-3.22\\times10^{-3}\\hat j)\\,\\mathrm{A\\,m^2}$.", "$\\vec\\tau=\\vec\\mu\\times\\vec B=(-9.65\\times10^{-4}\\hat i-7.24\\times10^{-4}\\hat j+8.04\\times10^{-4}\\hat k)\\,\\mathrm{N\\,m}$, magnitude $1.45\\times10^{-3}\\,\\mathrm{N\\,m}$."), TUT + ", Question 3", sig=3)
    mcq_num(B, c, "Torque on a current loop", 3, "For the same loop and field ($\\vec\\mu=(2.41\\times10^{-3}\\hat i-3.22\\times10^{-3}\\hat j)\\,\\mathrm{A\\,m^2}$, $\\vec B=(0.25\\hat i+0.30\\hat k)\\,\\mathrm{T}$), what is the orientation energy $U=-\\vec\\mu\\cdot\\vec B$?", U, [-U, -mu * np.linalg.norm(Bl), float(np.linalg.norm(tau)), U * 2], "J", ex("$\\vec\\mu\\cdot\\vec B=(2.41\\times10^{-3})(0.25)+0+0=6.03\\times10^{-4}\\,\\mathrm{J/T\\cdot T}$, so $U=-6.03\\times10^{-4}\\,\\mathrm{J}$."), TUT + ", Question 3(b)", sig=3)
    N, a, b, I_, B_ = 100, 0.050, 0.080, 2.0, 0.50
    mm = N * I_ * a * b
    mcq_num(B, c, "Torque on a current loop", 2, "A rectangular coil of $100$ turns, $5.0\\,\\mathrm{cm}\\times8.0\\,\\mathrm{cm}$, carries $2.0\\,\\mathrm{A}$ in a uniform field of $0.50\\,\\mathrm{T}$ that lies IN the plane of the coil. What is the torque on it?", mm * B_, [mm * B_ / 100, 0.0, N * I_ * (a + b) * B_, mm * B_ * 2], "N m", ex("$\\mu=NIA=100(2.0)(0.050)(0.080)=0.80\\,\\mathrm{A\\,m^2}$. Field in the plane of the coil means $\\vec B\\perp\\vec\\mu$: $\\tau=\\mu B\\sin90^\\circ=(0.80)(0.50)=0.40\\,\\mathrm{N\\,m}$ (the maximum torque; zero when the coil faces the field)."), GEN(TUT + ", Question 3"), "gen", sig=2)
    # Hall effect, cyclotron
    n, I_, B_, t = 8.5e28, 10.0, 1.0, 1.0e-4
    VH = I_ * B_ / (n * E_CH * t)
    mcq_num(B, c, "Hall effect", 3, "A copper strip ($n=8.5\\times10^{28}\\,\\mathrm{m^{-3}}$) $0.10\\,\\mathrm{mm}$ thick carries $10\\,\\mathrm{A}$ in a field of $1.0\\,\\mathrm{T}$ perpendicular to its faces. What is the Hall voltage across the strip?", VH, [I_ * B_ / (n * E_CH), I_ * B_ * t / (n * E_CH), VH * 1000, VH / 10], "V", ex("$V_H=\\dfrac{IB}{ne\\,t}=\\dfrac{(10)(1.0)}{(8.5\\times10^{28})(1.602\\times10^{-19})(1.0\\times10^{-4})}=7.3\\times10^{-6}\\,\\mathrm{V}$ - only a few microvolts in a good conductor, because $n$ is so large (semiconductors have far larger Hall voltages)."), LEC5 + ", 5.7 (the Hall effect)", "gen", sig=2)
    R_c, B_c = 0.50, 1.2
    Kc = (E_CH * B_c * R_c) ** 2 / (2 * M_P)
    mcq_num(B, c, "Motion in a magnetic field", 3, "A cyclotron with a magnetic field of $1.2\\,\\mathrm{T}$ and a radius of $0.50\\,\\mathrm{m}$ accelerates protons. What is their maximum kinetic energy, in MeV?", Kc / (1e6 * E_CH), [Kc / (1e6 * E_CH) * 2, Kc / (1e6 * E_CH) / 2, (E_CH * B_c * R_c) ** 2 / (M_P * 1e6 * E_CH), Kc / (1e6 * E_CH) * 4], "MeV", ex("At the largest radius $r=R=\\dfrac{mv}{eB}\\Rightarrow v=\\dfrac{eBR}{m}$.", "$K=\\dfrac{(eBR)^2}{2m}=\\dfrac{[(1.602\\times10^{-19})(1.2)(0.50)]^2}{2(1.673\\times10^{-27})}=2.8\\times10^{-12}\\,\\mathrm{J}=17\\,\\mathrm{MeV}$."), LEC5 + ", 5.8 (cyclotrons)", "gen", sig=2)
    mcq_pick(B, c, "Magnetic force on a charge", 1, "A magnetic field does NO work on a charged particle because", ["the magnetic force is always perpendicular to the velocity", "the magnetic force is zero", "the particle's speed always increases", "the field is conservative"], 0, ex("$\\mathrm{d}W=\\vec F\\cdot\\mathrm{d}\\vec l=q(\\vec v\\times\\vec B)\\cdot\\vec v\\,\\mathrm{d}t=0$: the force changes the direction of the velocity, never its magnitude, so the kinetic energy is constant."), LEC5 + ", 5.2", "concept")
    mcq_pick(B, c, "Magnetic force on a charge", 1, "A charged particle moves parallel to a uniform magnetic field. The magnetic force on it is", ["zero", "maximal", "directed along $\\vec B$", "equal to $qvB/2$"], 0, ex("$F=qvB\\sin\\theta$ and $\\theta=0$: no force, so the particle keeps moving in a straight line."), LEC5 + ", 5.1", "concept")
    mcq_pick(B, c, "Motion in a magnetic field", 2, "Two particles of the same charge and speed enter a uniform magnetic field perpendicular to it; particle 2 has twice the mass of particle 1. The ratio of the radii $r_2/r_1$ is", ["$2$", "$1/2$", "$4$", "$1$"], 0, ex("$r=\\dfrac{mv}{qB}\\propto m$ at fixed $q$, $v$, $B$, so $\\dfrac{r_2}{r_1}=\\dfrac{2m}{m}=2$."), LEC5 + ", 5.2", "concept")
    mcq_pick(B, c, "Crossed fields", 1, "In a velocity selector with crossed $\\vec E$ and $\\vec B$, particles of which speed pass straight through?", ["$v=E/B$, whatever their charge and mass", "$v=B/E$", "all speeds, if the charge is large enough", "$v=EB$"], 0, ex("The two forces $qE$ and $qvB$ are opposite and balance only when $v=E/B$."), LEC5 + ", 5.6 (discovery of the electron)", "concept")
    I1, I2, d = 20.0, 30.0, 0.050
    Fl = MU0 * I1 * I2 / (2 * math.pi * d)
    mcq_num(B, c, "Force between parallel currents", 2, "Two long parallel wires $5.0\\,\\mathrm{cm}$ apart carry $20\\,\\mathrm{A}$ and $30\\,\\mathrm{A}$ in the same direction. What is the magnitude of the force per unit length on each wire?", Fl, [MU0 * I1 * I2 / (2 * math.pi * d ** 2), MU0 * I1 * I2 / (2 * d), Fl * 2, Fl / 2], "N/m", ex("The field of wire 1 at wire 2 is $B_1=\\dfrac{\\mu_0I_1}{2\\pi d}$; the force per length on wire 2 is $I_2B_1=\\dfrac{\\mu_0I_1I_2}{2\\pi d}=\\dfrac{(4\\pi\\times10^{-7})(20)(30)}{2\\pi(0.050)}=2.4\\times10^{-3}\\,\\mathrm{N/m}$.", "Parallel currents ATTRACT (antiparallel currents repel); the two forces are equal and opposite."), LEC5 + ", 5.5 (force between parallel currents)", "gen", sig=2)
    I_, d = 8.0, 0.10
    Fa = MU0 * I_ ** 2 / (2 * math.pi * d) * 1.5
    mcq_num(B, c, "Force between parallel currents", 3, "Three long parallel wires in a plane, $0.10\\,\\mathrm{m}$ apart (a, b, c in a row), all carry $8.0\\,\\mathrm{A}$ in the same direction. What is the net force per metre on the OUTER wire a?", Fa, [MU0 * I_ ** 2 / (2 * math.pi * d), MU0 * I_ ** 2 / (2 * math.pi * d) * 0.5, MU0 * I_ ** 2 / (2 * math.pi * d) * 2, 0.0], "N/m", ex("Wire b (distance $d$) attracts a with $\\dfrac{\\mu_0I^2}{2\\pi d}=1.28\\times10^{-4}\\,\\mathrm{N/m}$; wire c (distance $2d$) attracts it with half that. Both pull towards the other wires, so they add: $\\dfrac32\\cdot\\dfrac{\\mu_0I^2}{2\\pi d}=1.9\\times10^{-4}\\,\\mathrm{N/m}$.", "(The force on the middle wire is zero by symmetry.)"), TUT + ", parallel wires (net force on wire a)", "gen", sig=2)

# =============================================================================================== chapter 6
def ch6(B):
    c = "c6"
    mcq_num(B, c, "Magnetic field of a straight wire", 1, "What is the magnetic field $0.10\\,\\mathrm{m}$ from a long straight wire carrying $5.0\\,\\mathrm{A}$?", MU0 * 5.0 / (2 * math.pi * 0.10), [MU0 * 5.0 / (2 * 0.10), MU0 * 5.0 / (2 * math.pi * 0.10 ** 2), MU0 * 5.0 * 0.10 / (2 * math.pi), MU0 * 5.0 / (4 * math.pi * 0.10)], "T", ex("$B=\\dfrac{\\mu_0I}{2\\pi r}=\\dfrac{(4\\pi\\times10^{-7})(5.0)}{2\\pi(0.10)}=1.0\\times10^{-5}\\,\\mathrm{T}$; the field lines are circles around the wire (right-hand rule)."), GEN(TUT + ", Example 6.2.1"), "gen", sig=2)
    r = MU0 * 1.0 / (2 * math.pi * 4.0e-6)
    mcq_num(B, c, "Magnetic field of a straight wire", 2, "At what distance from a long straight wire carrying $1.0\\,\\mathrm{A}$ is the magnetic field $4.0\\,\\mu\\mathrm{T}$?", r, [MU0 * 1.0 / (4.0e-6), 2 * math.pi * 4.0e-6 / (MU0 * 1.0), r / 2, r * 2], "m", ex("$r=\\dfrac{\\mu_0I}{2\\pi B}=\\dfrac{(4\\pi\\times10^{-7})(1.0)}{2\\pi(4.0\\times10^{-6})}=0.050\\,\\mathrm{m}$."), TUT + ", Example 6.2.1", sig=2)
    N, R_, I_ = 100, 0.60, 5.0
    Bc = N * MU0 * I_ / (2 * R_)
    chk = N * wire_field(arc_path(R_, 2 * math.pi), I_, (0, 0, 0))[2]
    check(Bc, chk, 1e-3, "loop centre field by Biot-Savart summation")
    mcq_num(B, c, "Magnetic field of a loop", 2, "A coil has $100$ circular turns of radius $0.60\\,\\mathrm{m}$, each carrying $5.0\\,\\mathrm{A}$. What is the magnetic field at its centre?", Bc, [MU0 * I_ / (2 * R_), N * MU0 * I_ / (4 * math.pi * R_), N * MU0 * I_ / (2 * R_ ** 2), Bc * 2], "T", ex("One loop gives $B=\\dfrac{\\mu_0I}{2R}$ at the centre; $N$ turns multiply it: $B=\\dfrac{N\\mu_0I}{2R}=\\dfrac{100(4\\pi\\times10^{-7})(5.0)}{2(0.60)}=5.2\\times10^{-4}\\,\\mathrm{T}$. A numerical Biot-Savart summation around the loop gives the same value."), TUT + ", Example 6.2.2", "src", sig=2)
    z = 0.80
    Bz = N * MU0 * I_ * R_ ** 2 / (2 * (R_ ** 2 + z ** 2) ** 1.5)
    chk = N * wire_field(arc_path(R_, 2 * math.pi), I_, (0, 0, z))[2]
    check(Bz, chk, 1e-3)
    mcq_num(B, c, "Magnetic field of a loop", 3, "For the same coil ($100$ turns, $R=0.60\\,\\mathrm{m}$, $5.0\\,\\mathrm{A}$), what is the field on the axis $0.80\\,\\mathrm{m}$ from the centre?", Bz, [N * MU0 * I_ / (2 * z), Bc, N * MU0 * I_ * R_ ** 2 / (2 * z ** 3), N * MU0 * I_ * R_ / (2 * (R_ ** 2 + z ** 2))], "T", ex("On the axis: $B=\\dfrac{N\\mu_0IR^2}{2(R^2+z^2)^{3/2}}=\\dfrac{100(4\\pi\\times10^{-7})(5.0)(0.36)}{2(0.36+0.64)^{3/2}}=1.1\\times10^{-4}\\,\\mathrm{T}$.", "Check by summing Biot-Savart contributions numerically: same value. At $z\\gg R$ this tends to the dipole form $\\dfrac{N\\mu_0IR^2}{2z^3}$."), TUT + ", Example 6.2.2(b)", "src", sig=2)
    R_a, I_a, phi = 0.20, 3.0, math.pi / 2
    Ba = MU0 * I_a * phi / (4 * math.pi * R_a)
    chk = wire_field(arc_path(R_a, phi), I_a, (0, 0, 0))[2]
    check(Ba, chk, 1e-4)
    mcq_num(B, c, "Biot-Savart law", 2, "A wire carrying $3.0\\,\\mathrm{A}$ is bent into a quarter circle of radius $0.20\\,\\mathrm{m}$ (the straight leads point towards the centre and contribute nothing). What is the field at the centre of the arc?", Ba, [MU0 * I_a / (2 * R_a), MU0 * I_a * phi / (2 * math.pi * R_a), Ba * 2, MU0 * I_a * phi / (4 * math.pi * R_a ** 2)], "T", ex("An arc of angle $\\varphi$ gives the fraction $\\dfrac{\\varphi}{2\\pi}$ of a full loop: $B=\\dfrac{\\mu_0I\\varphi}{4\\pi R}=\\dfrac{(4\\pi\\times10^{-7})(3.0)(\\pi/2)}{4\\pi(0.20)}=2.4\\times10^{-6}\\,\\mathrm{T}$ (verified by direct numerical summation)."), TUT + ", magnetic field from an arc of current", "src", sig=2)
    Lw, aw, Iw = 0.40, 0.05, 6.0
    sin_t = (Lw / 2) / math.hypot(aw, Lw / 2)
    Bs = MU0 * Iw / (4 * math.pi * aw) * 2 * sin_t
    chk = wire_field([(-Lw / 2, 0, 0), (Lw / 2, 0, 0)], Iw, (0, aw, 0))[2]
    check(abs(Bs), abs(chk), 1e-3)
    mcq_num(B, c, "Biot-Savart law", 3, "A straight wire segment of length $0.40\\,\\mathrm{m}$ carries $6.0\\,\\mathrm{A}$. What is the field at a point $5.0\\,\\mathrm{cm}$ from it on its perpendicular bisector?", Bs, [MU0 * Iw / (2 * math.pi * aw), MU0 * Iw / (4 * math.pi * aw), Bs * 2, Bs / 4], "T", ex("Biot-Savart for a finite segment: $B=\\dfrac{\\mu_0I}{4\\pi a}(\\sin\\theta_1+\\sin\\theta_2)$ with $\\sin\\theta=\\dfrac{L/2}{\\sqrt{a^2+(L/2)^2}}=0.97$ at each end.", "$B=\\dfrac{(4\\pi\\times10^{-7})(6.0)}{4\\pi(0.050)}(2)(0.970)=2.3\\times10^{-5}\\,\\mathrm{T}$, only 3% below the infinite-wire value $2.4\\times10^{-5}\\,\\mathrm{T}$."), GEN(TUT + ", Biot-Savart law"), "gen", sig=2)
    I_, d = 10.0, 0.20
    Bm_opp = 2 * MU0 * I_ / (2 * math.pi * d / 2)
    mcq_num(B, c, "Magnetic field of a straight wire", 3, "Two long parallel wires $0.20\\,\\mathrm{m}$ apart carry $10\\,\\mathrm{A}$ in OPPOSITE directions. What is the magnetic field midway between them?", Bm_opp, [0.0, Bm_opp / 2, Bm_opp * 2, MU0 * I_ / (2 * math.pi * d)], "T", ex("Each wire gives $\\dfrac{\\mu_0I}{2\\pi(d/2)}=2.0\\times10^{-5}\\,\\mathrm{T}$ at the midpoint. For opposite currents the two fields point the SAME way between the wires and add: $4.0\\times10^{-5}\\,\\mathrm{T}$ (for parallel currents they would cancel to zero)."), GEN(TUT + ", Biot-Savart law"), "gen", sig=2)
    mcq_pick(B, c, "Magnetic field of a straight wire", 1, "Two long parallel wires carry equal currents in the SAME direction. The magnetic field midway between them is", ["zero", "twice that of one wire", "equal to that of one wire", "infinite"], 0, ex("At the midpoint the fields of the two wires have equal magnitude and opposite directions."), GEN(TUT + ", Biot-Savart law"), "concept")
    mcq_pick(B, c, "Magnetic field of a straight wire", 1, "The magnetic field lines around a long straight current-carrying wire are", ["circles centred on the wire, in the sense given by the right-hand rule", "straight lines parallel to the wire", "straight lines radiating from the wire", "closed lines only inside the wire"], 0, ex("Thumb along the current, fingers curl in the direction of $\\vec B$."), TUT + ", Biot-Savart law", "concept")
    mcq_pick(B, c, "Gauss' law for magnetism", 1, "Gauss' law for magnetism, $\\oint\\vec B\\cdot\\mathrm{d}\\vec A=0$, states that", ["there are no magnetic monopoles: field lines are closed loops", "the magnetic flux through a closed surface equals $\\mu_0I$", "the magnetic field is uniform", "magnetic charge is conserved"], 0, ex("Every field line that enters a closed surface also leaves it, because magnetic poles come in N-S pairs."), LEC6 + ", 6.2", "concept")
    # Ampere's law
    i_ = 4.50e-3
    Ienc = (1 + 3) - (4 + 6)
    circ = MU0 * Ienc * i_
    mcq_num(B, c, "Ampere's law", 3, "Eight long wires cross the page perpendicularly; wire $k$ ($k=1,\\dots,8$) carries a current $k\\,i$ with $i=4.50\\,\\mathrm{mA}$: out of the page for odd $k$ and into the page for even $k$. A counter-clockwise closed path encloses wires $1,3,4$ and $6$ only. What is $\\oint\\vec B\\cdot\\mathrm{d}\\vec s$ along it?", circ, [-circ, MU0 * (1 + 3 + 4 + 6) * i_, MU0 * (1 + 3 - 4 - 6) * i_ / 4, 0.0], "T m", ex("Right-hand rule: for a counter-clockwise path, currents OUT of the page count positive and currents into the page negative.", "$I_{\\text{enc}}=(1+3-4-6)\\,i=-6i=-27.0\\,\\mathrm{mA}$.", "$\\oint\\vec B\\cdot\\mathrm{d}\\vec s=\\mu_0I_{\\text{enc}}=(4\\pi\\times10^{-7})(-0.0270)=-3.4\\times10^{-8}\\,\\mathrm{T\\,m}$."), GEN(TUT + ", Question 6 (eight wires)"), "gen", sig=2)
    mcq_num(B, c, "Ampere's law", 2, "A closed loop encloses three long wires carrying $2.0\\,\\mathrm{A}$, $3.0\\,\\mathrm{A}$ (both out of the page) and $1.5\\,\\mathrm{A}$ (into the page), and a fourth wire of $4.0\\,\\mathrm{A}$ lies outside the loop. What is $\\oint\\vec B\\cdot\\mathrm{d}\\vec s$ (counter-clockwise)?", MU0 * 3.5, [MU0 * 7.5, MU0 * 6.5, MU0 * 9.5, MU0 * 0.5], "T m", ex("Only enclosed currents count, with signs: $I_{\\text{enc}}=2.0+3.0-1.5=3.5\\,\\mathrm{A}$ (the outside wire contributes to $\\vec B$ on the path but not to the integral).", "$\\oint\\vec B\\cdot\\mathrm{d}\\vec s=\\mu_0(3.5)=4.4\\times10^{-6}\\,\\mathrm{T\\,m}$."), GEN(TUT + ", Ampere's law"), "gen", sig=2)
    L_s, N_s, I_s = 0.150, 600, 8.00
    Bsol = MU0 * N_s / L_s * I_s
    mcq_num(B, c, "Solenoids and toroids", 2, "A $15.0\\,\\mathrm{cm}$ long solenoid of radius $0.750\\,\\mathrm{cm}$ is closely wound with $600$ turns and carries $8.00\\,\\mathrm{A}$. What is the magnetic field near its centre?", Bsol, [MU0 * N_s * I_s, MU0 * N_s / (2 * math.pi * L_s) * I_s, MU0 * N_s / L_s * I_s / 2, MU0 * N_s * I_s / (L_s * 0.0075)], "T", ex("$B=\\mu_0nI$ with $n=\\dfrac NL=\\dfrac{600}{0.150}=4000\\,\\mathrm{turns/m}$: $B=(4\\pi\\times10^{-7})(4000)(8.00)=4.02\\times10^{-2}\\,\\mathrm{T}$ (the radius does not matter for a long solenoid)."), TUT + ", Young and Freedman 28.42", "src", sig=3)
    Nt, It, rt = 500, 2.0, 0.15
    Btor = MU0 * Nt * It / (2 * math.pi * rt)
    mcq_num(B, c, "Solenoids and toroids", 2, "A toroid with $500$ turns carrying $2.0\\,\\mathrm{A}$ has its field measured at radius $15\\,\\mathrm{cm}$ inside the core. What is the field?", Btor, [MU0 * Nt * It, MU0 * Nt * It / (4 * math.pi * rt), Btor * 2, MU0 * Nt * It / rt], "T", ex("Ampère's law on a circle of radius $r$: $B(2\\pi r)=\\mu_0NI\\Rightarrow B=\\dfrac{\\mu_0NI}{2\\pi r}=\\dfrac{(4\\pi\\times10^{-7})(500)(2.0)}{2\\pi(0.15)}=1.3\\times10^{-3}\\,\\mathrm{T}$ (falls as $1/r$ across the core; zero outside it)."), GEN(LEC6 + ", 6.3 solenoids and toroid"), "gen", sig=2)
    Rw, Iw = 2.0e-3, 8.0
    for rr in (1.0e-3, 4.0e-3):
        Bw = MU0 * Iw * rr / (2 * math.pi * Rw ** 2) if rr < Rw else MU0 * Iw / (2 * math.pi * rr)
        mcq_num(B, c, "Ampere's law", 3, "A long straight wire of radius $2.0\\,\\mathrm{mm}$ carries $8.0\\,\\mathrm{A}$ uniformly over its cross-section. What is the magnetic field at a distance of %s mm from the axis?" % sci(rr * 1000), Bw, [MU0 * Iw / (2 * math.pi * rr) if rr < Rw else MU0 * Iw * rr / (2 * math.pi * Rw ** 2), Bw * 2, Bw / 2, MU0 * Iw / (2 * math.pi * Rw)], "T", ex(("Inside the wire the enclosed current is $I\\dfrac{r^2}{R^2}$: $B=\\dfrac{\\mu_0Ir}{2\\pi R^2}=\\dfrac{(4\\pi\\times10^{-7})(8.0)(1.0\\times10^{-3})}{2\\pi(2.0\\times10^{-3})^2}=4.0\\times10^{-4}\\,\\mathrm{T}$ (it grows linearly with $r$)." if rr < Rw else "Outside the wire the whole current is enclosed: $B=\\dfrac{\\mu_0I}{2\\pi r}=\\dfrac{(4\\pi\\times10^{-7})(8.0)}{2\\pi(4.0\\times10^{-3})}=4.0\\times10^{-4}\\,\\mathrm{T}$ (falls as $1/r$). The two formulas agree at the surface.")), GEN(LEC6 + ", 6.2 Ampere's law"), "gen", sig=2)
    mcq_pick(B, c, "Solenoids and toroids", 1, "The magnetic field inside a long ideal solenoid is", ["uniform, parallel to the axis, and zero outside", "zero inside and uniform outside", "proportional to the distance from the axis", "radial"], 0, ex("$B=\\mu_0nI$ along the axis everywhere inside; the outside field of an ideal long solenoid is negligible."), LEC6 + ", 6.3", "concept")
    mcq_pick(B, c, "Ampere's law", 2, "To find the magnetic field of a long solenoid with Ampère's law, the best amperian loop is", ["a rectangle with one long side inside the solenoid, parallel to its axis", "a circle around the solenoid's axis", "a sphere", "a square entirely outside"], 0, ex("Along the long inside side $B$ is uniform and parallel to the path; the short sides are perpendicular to $\\vec B$ (no contribution) and the outside side has $B\\approx0$: $BL=\\mu_0nLI$."), LEC6 + ", 6.2", "concept")
    mcq_pick(B, c, "Biot-Savart law", 1, "The Biot-Savart law gives the magnetic field of a current element $I\\,\\mathrm{d}\\vec s$ as", ["$\\mathrm{d}\\vec B=\\dfrac{\\mu_0}{4\\pi}\\dfrac{I\\,\\mathrm{d}\\vec s\\times\\hat r}{r^2}$", "$\\mathrm{d}\\vec B=\\dfrac{\\mu_0}{4\\pi}\\dfrac{I\\,\\mathrm{d}\\vec s\\cdot\\hat r}{r^2}$", "$\\mathrm{d}\\vec B=\\dfrac{\\mu_0I}{4\\pi r}\\mathrm{d}\\vec s$", "$\\mathrm{d}\\vec B=\\mu_0I\\,\\hat r/r^2$"], 0, ex("It is the magnetic analogue of Coulomb's law, but with a CROSS product: $\\mathrm{d}\\vec B$ is perpendicular to both the current element and $\\hat r$."), LEC6 + ", 6.1", "concept")

# =============================================================================================== chapter 7
def ch7(B):
    c = "c7"
    Bf, a, b, th = 0.40, 0.20, 0.30, 60.0
    Phi = Bf * a * b * math.cos(math.radians(th))
    mcq_num(B, c, "Magnetic flux", 1, "A rectangular loop of $0.20\\,\\mathrm{m}\\times0.30\\,\\mathrm{m}$ is in a uniform field of $0.40\\,\\mathrm{T}$. The angle between the field and the loop's normal is $60^\\circ$. What is the magnetic flux through the loop?", Phi, [Bf * a * b * math.sin(math.radians(th)), Bf * a * b, Bf * (a + b) * math.cos(math.radians(th)), Phi * 2], "Wb", ex("$\\Phi_B=BA\\cos\\theta=(0.40)(0.060)\\cos60^\\circ=1.2\\times10^{-2}\\,\\mathrm{Wb}$ ($1\\,\\mathrm{Wb}=1\\,\\mathrm{T\\,m^2}$), with $\\theta$ measured from the normal."), GEN(FIN + ", magnetic flux"), "gen", sig=2)
    N, A, dB, dt = 200, 0.05, 1.5, 3.0
    emf = N * A * dB / dt
    mcq_num(B, c, "Faraday's law", 1, "A flat coil with $200$ turns and area $0.05\\,\\mathrm{m^2}$ is in a uniform field perpendicular to its plane. The field changes from $0$ to $1.5\\,\\mathrm{T}$ in $3.0\\,\\mathrm{s}$. What is the induced emf?", emf, [A * dB / dt, N * dB / dt, N * A * dB * dt, emf * 2], "V", ex("Faraday: $|\\varepsilon|=N\\left|\\dfrac{\\Delta\\Phi}{\\Delta t}\\right|=NA\\dfrac{\\Delta B}{\\Delta t}=(200)(0.05)\\dfrac{1.5}{3.0}=5.0\\,\\mathrm{V}$."), FIN + ", Faraday's law of induction", sig=2, origin="src")
    A_in, rate = 2.00, 0.870
    ind = A_in * rate; net = 20.0 + ind
    mcq_num(B, c, "Faraday's law", 3, "A square loop of side $2.00\\,\\mathrm{m}$ has half of its area in a uniform field perpendicular to it. The loop contains an ideal battery of emf $20.0\\,\\mathrm{V}$. The field varies as $B=0.0420-0.870\\,t$ (T, s). If the induced emf has the same sense as the battery's, what is the net emf in the circuit?", net, [20.0 - ind, ind, 20.0 + 2 * ind, 20.0 + 4.0 * rate], "V", ex("Flux through the loop: $\\Phi=B\\cdot\\dfrac{A_{\\text{loop}}}{2}=B(2.00\\,\\mathrm{m^2})$, so $|\\varepsilon_{\\text{ind}}|=2.00\\left|\\dfrac{\\mathrm{d}B}{\\mathrm{d}t}\\right|=2.00(0.870)=1.74\\,\\mathrm{V}$ (the field decreases, so the induced current tries to maintain the flux).", "Net emf $=20.0+1.74=21.7\\,\\mathrm{V}$ (it would be $18.3\\,\\mathrm{V}$ if the induced emf opposed the battery)."), FIN + ", Faraday's law of induction", "src", sig=3)
    Bm, Lm, vm = 0.50, 0.40, 5.0
    em = Bm * Lm * vm
    mcq_num(B, c, "Motional emf", 2, "A conducting rod of length $0.40\\,\\mathrm{m}$ slides at $5.0\\,\\mathrm{m/s}$ perpendicular to a uniform $0.50\\,\\mathrm{T}$ field, along rails joined by a $2.0\\,\\Omega$ resistor. What force must be applied to keep the speed constant?", Bm * (em / 2.0) * Lm, [em, em / 2.0, Bm * em * Lm, Bm * Lm * vm * vm], "N", ex("Motional emf $\\varepsilon=BLv=(0.50)(0.40)(5.0)=1.0\\,\\mathrm{V}$; current $I=\\dfrac{\\varepsilon}{R}=0.50\\,\\mathrm{A}$.", "Magnetic braking force $F=ILB=(0.50)(0.40)(0.50)=0.10\\,\\mathrm{N}$ - the applied force must match it, and supplies the power $Fv=\\varepsilon I=0.50\\,\\mathrm{W}$ dissipated in the resistor."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    Nc, Ac, Bc2, fc = 100, 0.020, 0.20, 50.0
    wc = 2 * math.pi * fc
    emax = Nc * Bc2 * Ac * wc
    t_ = np.linspace(0, 1 / fc, 20001)
    flux = Nc * Bc2 * Ac * np.cos(wc * t_)
    num_peak = float(np.max(np.abs(np.gradient(flux, t_))))
    check(emax, num_peak, 2e-3, "peak emf by differentiating the flux numerically")
    mcq_num(B, c, "Faraday's law", 3, "A coil of $100$ turns and area $0.020\\,\\mathrm{m^2}$ rotates at $50\\,\\mathrm{Hz}$ in a uniform $0.20\\,\\mathrm{T}$ field. What is the peak emf?", emax, [Nc * Bc2 * Ac * fc, emax / (2 * math.pi), emax * 2, Nc * Bc2 * Ac], "V", ex("$\\Phi=NBA\\cos\\omega t\\Rightarrow\\varepsilon=-\\dfrac{\\mathrm{d}\\Phi}{\\mathrm{d}t}=NBA\\omega\\sin\\omega t$, peak $NBA\\omega=100(0.20)(0.020)(2\\pi\\cdot50)=1.3\\times10^{2}\\,\\mathrm{V}$. (Using $f$ instead of $\\omega=2\\pi f$ is a common slip.)"), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    mcq_pick(B, c, "Lenz's law", 2, "The north pole of a bar magnet is pushed TOWARDS a conducting loop (loop plane perpendicular to the magnet's axis). The induced current in the loop produces a magnetic field that", ["opposes the approaching pole (repels it)", "attracts the approaching pole", "has no effect on the magnet", "points in the same direction as the magnet's field at the loop"], 0, ex("Lenz's law: the induced effect opposes the CHANGE (increasing flux of the north pole's field). The loop behaves as a north pole facing the magnet, repelling it; energy for the induced current comes from the work done pushing the magnet."), LEC7 + ", 7.2 (Lenz's law)", "concept")
    mcq_pick(B, c, "Lenz's law", 2, "A uniform field points INTO the page and its magnitude is decreasing. The induced current in a circular loop in the plane of the page is", ["clockwise", "counter-clockwise", "zero", "alternating"], 0, ex("The inward flux decreases, so the induced current produces an inward field of its own to oppose the decrease: by the right-hand rule a CLOCKWISE current gives a field into the page inside the loop."), FIN + ", Lenz's law", "src")
    mcq_pick(B, c, "Faraday's law", 1, "Which change induces an emf in a closed loop?", ["any change of the magnetic flux through it: the field, the area or the orientation", "only a changing field strength", "only a moving loop", "a steady current in the loop"], 0, ex("$\\Phi=BA\\cos\\theta$ can change through $B$, $A$ or $\\theta$; only $\\mathrm{d}\\Phi/\\mathrm{d}t\\neq0$ gives an emf."), LEC7 + ", 7.2", "concept")
    r_, dBdt, R = 0.04, 0.10, 0.10
    Ein = r_ / 2 * dBdt
    mcq_num(B, c, "Induced electric fields", 3, "A uniform field inside a long solenoid of radius $0.10\\,\\mathrm{m}$ changes at $0.10\\,\\mathrm{T/s}$. What is the magnitude of the induced electric field at $0.04\\,\\mathrm{m}$ from the axis (inside)?", Ein, [R ** 2 / (2 * r_) * dBdt, r_ * dBdt, Ein * 2, Ein / 2], "V/m", ex("$\\oint\\vec E\\cdot\\mathrm{d}\\vec s=-\\dfrac{\\mathrm{d}\\Phi}{\\mathrm{d}t}$: $E(2\\pi r)=\\pi r^2\\left|\\dfrac{\\mathrm{d}B}{\\mathrm{d}t}\\right|\\Rightarrow E=\\dfrac r2\\left|\\dfrac{\\mathrm{d}B}{\\mathrm{d}t}\\right|=\\dfrac{0.04}{2}(0.10)=2.0\\times10^{-3}\\,\\mathrm{V/m}$ (circular field lines)."), GEN(FIN + ", induced electric field"), "gen", sig=2)
    Rr = R
    Eout = Rr ** 2 / (2 * 0.20) * dBdt
    mcq_num(B, c, "Induced electric fields", 3, "For the same solenoid (radius $0.10\\,\\mathrm{m}$, $\\mathrm{d}B/\\mathrm{d}t=0.10\\,\\mathrm{T/s}$), what is the induced field magnitude $0.20\\,\\mathrm{m}$ from the axis (OUTSIDE the solenoid)?", Eout, [0.20 / 2 * dBdt, Eout * 2, Eout / 2, 0.0], "V/m", ex("Outside, the flux is confined to $\\pi R^2$: $E(2\\pi r)=\\pi R^2\\left|\\dfrac{\\mathrm{d}B}{\\mathrm{d}t}\\right|\\Rightarrow E=\\dfrac{R^2}{2r}\\left|\\dfrac{\\mathrm{d}B}{\\mathrm{d}t}\\right|=\\dfrac{0.010}{0.40}(0.10)=2.5\\times10^{-3}\\,\\mathrm{V/m}$: the field is NOT zero outside, although $B$ is."), GEN(FIN + ", induced electric field"), "gen", sig=2)
    N_, A_, l_ = 1000, 4.0e-4, 0.25
    L = MU0 * N_ ** 2 * A_ / l_
    mcq_num(B, c, "Inductance", 2, "What is the inductance of an air-filled solenoid with $1000$ turns, cross-section $4.0\\,\\mathrm{cm^2}$ and length $0.25\\,\\mathrm{m}$?", L, [MU0 * N_ * A_ / l_, MU0 * N_ ** 2 * A_ * l_, MU0 * N_ ** 2 * l_ / A_, L * 2], "H", ex("$L=\\dfrac{N\\Phi_B}{I}=\\mu_0n^2Al=\\dfrac{\\mu_0N^2A}{\\ell}=\\dfrac{(4\\pi\\times10^{-7})(10^6)(4.0\\times10^{-4})}{0.25}=2.0\\times10^{-3}\\,\\mathrm{H}$."), LEC7 + ", 7.5 (inductor and inductance)", "gen", sig=2)
    Li, dI = 2.0e-3, 50.0
    mcq_num(B, c, "Inductance", 1, "The current through a $2.0\\,\\mathrm{mH}$ inductor changes at $50\\,\\mathrm{A/s}$. What is the magnitude of the self-induced emf?", Li * dI, [dI / Li, Li / dI, Li * dI * 2, Li * dI / 2], "V", ex("$|\\varepsilon_L|=L\\left|\\dfrac{\\mathrm{d}I}{\\mathrm{d}t}\\right|=(2.0\\times10^{-3})(50)=0.10\\,\\mathrm{V}$, opposing the change of current (Lenz)."), LEC7 + ", 7.6 (self-induction)", "gen", sig=2)
    Lh, Ia = 2.0, 3.0
    mcq_num(B, c, "Inductance", 2, "How much energy is stored in the magnetic field of a $2.0\\,\\mathrm{H}$ inductor carrying $3.0\\,\\mathrm{A}$?", 0.5 * Lh * Ia ** 2, [Lh * Ia ** 2, 0.5 * Lh * Ia, Lh * Ia, 0.5 * Lh ** 2 * Ia], "J", ex("$U_B=\\tfrac12LI^2=\\tfrac12(2.0)(3.0)^2=9.0\\,\\mathrm{J}$."), LEC7 + ", 7.5", "gen", sig=2)
    Bu = 0.50
    mcq_num(B, c, "Inductance", 2, "What is the energy density of a $0.50\\,\\mathrm{T}$ magnetic field in vacuum?", Bu ** 2 / (2 * MU0), [Bu ** 2 / MU0, Bu ** 2 / (4 * MU0), Bu ** 2 / (2 * MU0) * 10, Bu ** 2 / (2 * MU0) / 10], "J/m^3", ex("$u_B=\\dfrac{B^2}{2\\mu_0}=\\dfrac{(0.50)^2}{2(4\\pi\\times10^{-7})}=9.9\\times10^{4}\\,\\mathrm{J/m^3}$."), LEC7 + ", 7.5", "gen", sig=2)
    Mi, dI1 = 5.0e-3, 100.0
    mcq_num(B, c, "Inductance", 2, "Two coils have mutual inductance $5.0\\,\\mathrm{mH}$. The current in coil 1 changes at $100\\,\\mathrm{A/s}$. What emf is induced in coil 2?", Mi * dI1, [Mi / dI1, Mi * dI1 * 2, dI1 / Mi, Mi * dI1 / 2], "V", ex("$|\\varepsilon_2|=M\\left|\\dfrac{\\mathrm{d}I_1}{\\mathrm{d}t}\\right|=(5.0\\times10^{-3})(100)=0.50\\,\\mathrm{V}$."), LEC7 + ", 7.6 (mutual induction)", "gen", sig=2)
    emf_, R_, L_ = 12.0, 4.0, 0.20
    tau = L_ / R_
    I_t = emf_ / R_ * (1 - math.exp(-1.0))
    check(I_t, rl_current(emf_, R_, L_, tau), 1e-9, "RL current by integrating the circuit equation")
    mcq_num(B, c, "RL circuits", 3, "A $12\\,\\mathrm{V}$ battery is connected at $t=0$ to a $4.0\\,\\Omega$ resistor in series with a $0.20\\,\\mathrm{H}$ inductor. What is the current after one time constant ($t=L/R$)?", I_t, [12.0 / 4.0, 12.0 / 4.0 * math.exp(-1.0), 12.0 / 4.0 * 0.5, 12.0 / 4.0 * (1 - math.exp(-2.0))], "A", ex("$I(t)=\\dfrac{\\varepsilon}{R}\\left(1-e^{-t/\\tau}\\right)$ with $\\tau=\\dfrac LR=0.050\\,\\mathrm{s}$ and $\\dfrac\\varepsilon R=3.0\\,\\mathrm{A}$.", "At $t=\\tau$: $I=3.0(1-e^{-1})=1.9\\,\\mathrm{A}$, i.e. $63\\%$ of the final value (numerical integration of $L\\,\\mathrm{d}I/\\mathrm{d}t+RI=\\varepsilon$ agrees)."), "Magnetism lecture (2025-26): beyond the chapter 7 outline (RL circuit)", "gen", sig=2, tags=("extension",))
    mcq_pick(B, c, "Inductance", 1, "An inductor opposes", ["a change in the current through it", "the current itself", "a constant current", "the voltage of the battery"], 0, ex("$\\varepsilon_L=-L\\dfrac{\\mathrm{d}I}{\\mathrm{d}t}$ acts against the CHANGE; a steady current in an ideal inductor produces no emf."), LEC7 + ", 7.5-7.6", "concept")
    mcq_pick(B, c, "Faraday's law", 2, "The SI unit of magnetic flux, the weber, is equal to", ["$1\\,\\mathrm{T\\,m^2}$", "$1\\,\\mathrm{T/m^2}$", "$1\\,\\mathrm{V\\,s^2}$", "$1\\,\\mathrm{A\\,m}$"], 0, ex("$\\Phi_B=BA$, so $1\\,\\mathrm{Wb}=1\\,\\mathrm{T\\,m^2}=1\\,\\mathrm{V\\,s}$ (since $\\varepsilon=\\mathrm{d}\\Phi/\\mathrm{d}t$)."), LEC7 + ", 7.1 (magnetic flux)", "concept")


# =============================================================================================== more chapter 5, 6, 7 questions
AX = {(1, 0, 0): "+x", (-1, 0, 0): "-x", (0, 1, 0): "+y", (0, -1, 0): "-y", (0, 0, 1): "+z", (0, 0, -1): "-z"}

def axis_name(v):
    return AX[tuple(int(round(t)) for t in v)]

def ch5b(B):
    c = "c5"
    # ---------------------------------------------------------------- right-hand rule, computed with cross products
    unit = {"+x": (1, 0, 0), "+y": (0, 1, 0), "+z": (0, 0, 1)}
    cases = [("proton", 1, "+x", "+y"), ("electron", -1, "+x", "+y"), ("proton", 1, "+y", "+z"), ("electron", -1, "+z", "+x"), ("proton", 1, "+z", "+y"), ("electron", -1, "+y", "+x")]
    for name, sgn, vd, bd in cases:
        F = sgn * np.cross(unit[vd], unit[bd])
        cp = np.cross(unit[vd], unit[bd])
        right = axis_name(F)
        wrongs = [axis_name(-F), axis_name(unit[vd]), axis_name(unit[bd])]
        correct = "the %s direction" % right
        mcq_text(B, c, "Magnetic force on a charge", 2, "A %s moves along the %s axis in a uniform magnetic field along the %s axis. In which direction is the magnetic force on it?" % (name, vd, bd), correct, ["the %s direction" % w for w in wrongs],
                 ex("$\\vec F=q\\,\\vec v\\times\\vec B$. For the unit vectors, $\\vec v\\times\\vec B$ points along %s." % axis_name(cp), "The charge is %s, so the force points along %s." % ("positive: the same direction" if sgn > 0 else "negative: the opposite direction", right)), GEN(LEC5 + ", 5.1-5.2 (right-hand rule)"), "gen")
    # ---------------------------------------------------------------- ratios
    mcq_pick(B, c, "Motion in a magnetic field", 2, "A proton and a deuteron (charge $e$, mass $2m_p$) enter a uniform magnetic field with the same speed, perpendicular to it. The ratio $r_d/r_p$ of their radii is", ["$2$", "$1/2$", "$\\sqrt2$", "$1$"], 0, ex("$r=\\dfrac{mv}{qB}$: same $q$, $v$, $B$, so $r\\propto m$ and $r_d/r_p=2$."), GEN(LEC5 + ", 5.2"), "gen")
    mcq_pick(B, c, "Motion in a magnetic field", 3, "A proton and an alpha particle (charge $2e$, mass $4m_p$) have the SAME kinetic energy and enter a uniform field perpendicular to it. The ratio $r_\\alpha/r_p$ is", ["$1$", "$2$", "$1/2$", "$\\sqrt2$"], 0, ex("$r=\\dfrac{mv}{qB}=\\dfrac{\\sqrt{2mK}}{qB}$. With equal $K$: $\\dfrac{r_\\alpha}{r_p}=\\dfrac{\\sqrt{m_\\alpha}}{\\sqrt{m_p}}\\dfrac{q_p}{q_\\alpha}=\\sqrt4\\cdot\\dfrac12=1$: the two follow the same circle."), GEN(LEC5 + ", 5.2"), "gen")
    K = 10.0e3 * E_CH
    Bp = 0.50
    rp = math.sqrt(2 * M_P * K) / (E_CH * Bp)
    mcq_num(B, c, "Motion in a magnetic field", 2, "A $10\\,\\mathrm{keV}$ proton moves perpendicular to a uniform $0.50\\,\\mathrm{T}$ field. What is the radius of its orbit?", rp, [math.sqrt(2 * M_P * K) / (E_CH * Bp) * math.sqrt(2), rp / 2, rp * 2, M_P * K / (E_CH * Bp)], "m", ex("$p=\\sqrt{2m_pK}=\\sqrt{2(1.673\\times10^{-27})(1.602\\times10^{-15})}=2.3\\times10^{-21}\\,\\mathrm{kg\\,m/s}$.", "$r=\\dfrac{p}{eB}=\\dfrac{2.3\\times10^{-21}}{(1.602\\times10^{-19})(0.50)}=2.9\\times10^{-2}\\,\\mathrm{m}$."), GEN(LEC5 + ", 5.2"), "gen", sig=2)
    Bh = 0.80
    th = math.pi * M_P / (E_CH * Bh)
    mcq_num(B, c, "Motion in a magnetic field", 2, "How long does a proton take to complete HALF a circle in a uniform $0.80\\,\\mathrm{T}$ field?", th, [2 * th, th / 2, 2 * math.pi * M_P / (E_CH * Bh) * 2 * math.pi, M_P / (E_CH * Bh)], "s", ex("The period is $T=\\dfrac{2\\pi m}{eB}$, so half a circle takes $\\dfrac T2=\\dfrac{\\pi m}{eB}=\\dfrac{\\pi(1.673\\times10^{-27})}{(1.602\\times10^{-19})(0.80)}=4.1\\times10^{-8}\\,\\mathrm{s}$, whatever the speed."), GEN(LEC5 + ", 5.8"), "gen", sig=2)
    # isotopes in a mass spectrometer
    r1 = 1.00; r2 = r1 * math.sqrt(238.0 / 235.0)
    sep = 2 * (r2 - r1)
    mcq_num(B, c, "Crossed fields", 3, "Singly charged ions of $^{235}$U and $^{238}$U enter the same magnetic field perpendicular to it with the same kinetic energy. The $^{235}$U ions follow a semicircle of radius $1.00\\,\\mathrm{m}$. How far apart do the two beams land on the detector (the difference of the diameters)?", sep * 100, [(r2 - r1) * 100, sep * 100 * 2, sep * 100 * 10, sep * 100 / 4], "cm", ex("$r=\\dfrac{\\sqrt{2mK}}{qB}\\propto\\sqrt m$: $r_{238}=1.00\\sqrt{\\dfrac{238}{235}}=1.0063\\,\\mathrm{m}$.", "The landing points are one DIAMETER from the entrance: $2(1.0063-1.00)=0.0127\\,\\mathrm{m}=1.3\\,\\mathrm{cm}$."), GEN(LEC5 + ", 5.6 (mass-to-charge ratio)"), "gen", sig=2)
    # wire shapes
    R_, I_, B_ = 0.10, 3.0, 0.40
    F = I_ * 2 * R_ * B_
    mcq_num(B, c, "Force on a current-carrying wire", 3, "A wire carrying $3.0\\,\\mathrm{A}$ is bent into a semicircle of radius $0.10\\,\\mathrm{m}$ lying in a plane perpendicular to a uniform $0.40\\,\\mathrm{T}$ field. What is the net magnetic force on the semicircle?", F, [I_ * math.pi * R_ * B_, 0.0, I_ * R_ * B_, F * 2], "N", ex("The net force on a curved wire equals the force on a straight wire joining its ends: $F=I\\,(2R)\\,B=(3.0)(0.20)(0.40)=0.24\\,\\mathrm{N}$. The arc length $\\pi R$ is NOT the effective length."), GEN(TUT + ", Question 2"), "gen", sig=2)
    mcq_pick(B, c, "Torque on a current loop", 2, "The net magnetic force on a closed current loop in a UNIFORM magnetic field is", ["zero (but there may be a torque)", "$NIAB$", "$IB\\ell$ for each side added together", "perpendicular to the plane of the loop"], 0, ex("The forces on opposite sides are equal and opposite, so the net force vanishes: $\\oint I\\,\\mathrm{d}\\vec l\\times\\vec B=I\\left(\\oint\\mathrm{d}\\vec l\\right)\\times\\vec B=0$. The forces can still form a couple (torque $\\vec\\mu\\times\\vec B$)."), LEC5 + ", 5.4 (torque on a current loop)", "concept")
    mu_, B_ = 0.80, 0.50
    mcq_num(B, c, "Torque on a current loop", 2, "A coil with magnetic moment $0.80\\,\\mathrm{A\\,m^2}$ makes an angle of $30^\\circ$ with a $0.50\\,\\mathrm{T}$ field. What is the magnitude of the torque?", mu_ * B_ * math.sin(math.radians(30)), [mu_ * B_ * math.cos(math.radians(30)), mu_ * B_, mu_ * B_ * 2, mu_ * B_ * math.sin(math.radians(30)) / 2], "N m", ex("$\\tau=\\mu B\\sin\\theta=(0.80)(0.50)\\sin30^\\circ=0.20\\,\\mathrm{N\\,m}$ (with $\\theta$ the angle between $\\vec\\mu$ and $\\vec B$)."), GEN(LEC5 + ", 5.4"), "gen", sig=2)
    mcq_num(B, c, "Torque on a current loop", 3, "A coil with magnetic moment $0.80\\,\\mathrm{A\\,m^2}$ is in a $0.50\\,\\mathrm{T}$ field. How much work is needed to turn it from parallel to $\\vec B$ (stable) to antiparallel (unstable)?", 2 * mu_ * B_, [mu_ * B_, 0.0, 4 * mu_ * B_, mu_ * B_ / 2], "J", ex("$U=-\\vec\\mu\\cdot\\vec B$: $U_{\\parallel}=-\\mu B$ and $U_{\\text{anti}}=+\\mu B$, so $W=\\Delta U=2\\mu B=2(0.80)(0.50)=0.80\\,\\mathrm{J}$."), GEN(LEC5 + ", 5.4"), "gen", sig=2)
    v_, r_ = 2.19e6, 5.29e-11
    mub = E_CH * v_ * r_ / 2
    mcq_num(B, c, "Torque on a current loop", 3, "In the Bohr model the electron circles the proton at $2.19\\times10^{6}\\,\\mathrm{m/s}$ in an orbit of radius $5.29\\times10^{-11}\\,\\mathrm{m}$. What is the orbital magnetic dipole moment?", mub, [E_CH * v_ * r_, mub / 2, mub * 4, mub / 4], "A m^2", ex("Orbiting charge is a current $I=\\dfrac{e}{T}=\\dfrac{ev}{2\\pi r}$; $\\mu=IA=\\dfrac{ev}{2\\pi r}\\pi r^2=\\dfrac{evr}{2}=\\dfrac{(1.602\\times10^{-19})(2.19\\times10^6)(5.29\\times10^{-11})}{2}=9.3\\times10^{-24}\\,\\mathrm{A\\,m^2}$ (the Bohr magneton)."), GEN(LEC5 + ", 5.4"), "gen", sig=2)
    # Hall: carrier density from the Hall voltage
    I_, B_, t, VH = 3.0, 1.5, 2.0e-4, 2.0e-5
    n = I_ * B_ / (E_CH * t * VH)
    mcq_num(B, c, "Hall effect", 3, "A metal strip $0.20\\,\\mathrm{mm}$ thick carries $3.0\\,\\mathrm{A}$ in a perpendicular field of $1.5\\,\\mathrm{T}$ and shows a Hall voltage of $20\\,\\mu\\mathrm{V}$. What is the density of charge carriers?", n, [I_ * B_ * t / (E_CH * VH), I_ * B_ / (E_CH * VH), n / 1000, n * 1000], "m^{-3}", ex("$V_H=\\dfrac{IB}{net}\\Rightarrow n=\\dfrac{IB}{etV_H}=\\dfrac{(3.0)(1.5)}{(1.602\\times10^{-19})(2.0\\times10^{-4})(2.0\\times10^{-5})}=7.0\\times10^{27}\\,\\mathrm{m^{-3}}$."), GEN(LEC5 + ", 5.7"), "gen", sig=2)
    mcq_pick(B, c, "Hall effect", 2, "The sign of the Hall voltage across a conducting strip tells us", ["whether the charge carriers are positive or negative", "the strip's resistance", "the strength of the current only", "the direction of the electric field in the strip"], 0, ex("Moving positive or negative carriers are pushed to the same side by the magnetic force but produce opposite polarity of the transverse voltage: the Hall effect identified electrons as the carriers in most metals."), LEC5 + ", 5.7", "concept")
    V_, Bt = 2000.0, 1.0e-3
    vt = math.sqrt(2 * E_CH * V_ / M_E); rt = M_E * vt / (E_CH * Bt)
    em = 2 * V_ / (Bt ** 2 * rt ** 2)
    check(em, E_CH / M_E, 1e-6)
    mcq_num(B, c, "Crossed fields", 3, "Electrons accelerated from rest through $2000\\,\\mathrm{V}$ move in a circle of radius $0.151\\,\\mathrm{m}$ in a field of $1.0\\,\\mathrm{mT}$. What value of $e/m$ follows from these three numbers?", em, [V_ / (Bt ** 2 * rt ** 2), 2 * V_ / (Bt * rt), em / 2, em * 2], "C/kg", ex("$eV=\\tfrac12mv^2$ and $r=\\dfrac{mv}{eB}$: eliminate $v$ to get $\\dfrac em=\\dfrac{2V}{B^2r^2}=\\dfrac{2(2000)}{(1.0\\times10^{-3})^2(0.151)^2}=1.75\\times10^{11}\\,\\mathrm{C/kg}$ (accepted value $1.76\\times10^{11}$) - Thomson's method."), LEC5 + ", 5.6 (discovery of the electron)", "gen", sig=3)
    mcq_pick(B, c, "Force between parallel currents", 1, "Two long parallel wires carry currents in OPPOSITE directions. The force between them is", ["repulsive", "attractive", "zero", "a torque but no force"], 0, ex("Parallel currents attract, antiparallel currents repel."), LEC5 + ", 5.5", "concept")
    mcq_num(B, c, "Force between parallel currents", 1, "Two long parallel wires $1.0\\,\\mathrm{m}$ apart each carry $1.0\\,\\mathrm{A}$. What is the force per metre between them? (This defined the ampere.)", MU0 * 1.0 * 1.0 / (2 * math.pi * 1.0), [MU0 * 1.0, MU0 / (2 * math.pi * 1.0 ** 2) * 2, MU0 / (4 * math.pi), 1.0], "N/m", ex("$\\dfrac FL=\\dfrac{\\mu_0I_1I_2}{2\\pi d}=\\dfrac{(4\\pi\\times10^{-7})(1)(1)}{2\\pi(1)}=2\\times10^{-7}\\,\\mathrm{N/m}$."), LEC5 + ", 5.5", "gen", sig=2)

def ch6b(B):
    c = "c6"
    unit = {"+x": (1, 0, 0), "+y": (0, 1, 0), "+z": (0, 0, 1), "-x": (-1, 0, 0), "-y": (0, -1, 0), "-z": (0, 0, -1)}
    # direction of B around a wire: I-hat x r-hat (Biot-Savart)
    for cur, pt in [("+z", "+x"), ("+z", "+y"), ("+x", "+z"), ("-z", "+x"), ("+y", "-z"), ("+x", "-y")]:
        Bd = np.cross(unit[cur], unit[pt])
        right = axis_name(Bd)
        wrongs = [axis_name(-Bd), axis_name(unit[cur]), axis_name(unit[pt])]
        mcq_text(B, c, "Magnetic field of a straight wire", 2, "A long straight wire along the %s axis carries current in the %s direction. In which direction is its magnetic field at a point on the %s axis?" % (cur[1], cur, pt), "the %s direction" % right, ["the %s direction" % w for w in wrongs],
                 ex("Biot-Savart: $\\mathrm{d}\\vec B\\propto\\mathrm{d}\\vec s\\times\\hat r$ with $\\mathrm{d}\\vec s$ along %s and $\\hat r$ (from the wire to the point) along %s." % (cur, pt), "The cross product points along %s (right-hand rule: thumb along the current, fingers curl with the field)." % right), GEN(LEC6 + ", 6.1"), "gen")
    a_, I_ = 0.20, 4.0
    Bsq = 2 * math.sqrt(2) * MU0 * I_ / (math.pi * a_)
    h = a_ / 2
    sq = [(h, -h, 0), (h, h, 0), (-h, h, 0), (-h, -h, 0), (h, -h, 0)]
    chk = wire_field(sq, I_, (0, 0, 0))[2]
    check(Bsq, abs(chk), 1e-3, "square loop centre by Biot-Savart summation")
    mcq_num(B, c, "Magnetic field of a loop", 3, "A square loop of side $0.20\\,\\mathrm{m}$ carries $4.0\\,\\mathrm{A}$. What is the magnetic field at its centre?", Bsq, [4 * MU0 * I_ / (2 * math.pi * a_), MU0 * I_ / (2 * (a_ / 2)), Bsq / 2, Bsq * 2], "T", ex("Each side is a finite wire seen from the perpendicular distance $a/2$ under $\\pm45^\\circ$: $B_{\\text{side}}=\\dfrac{\\mu_0I}{4\\pi(a/2)}(2\\sin45^\\circ)$, and the four sides add: $B=\\dfrac{2\\sqrt2\\mu_0I}{\\pi a}=\\dfrac{2\\sqrt2(4\\pi\\times10^{-7})(4.0)}{\\pi(0.20)}=2.3\\times10^{-5}\\,\\mathrm{T}$. A numerical sum confirms it."), GEN(TUT + ", Biot-Savart law"), "gen", sig=2)
    R_, I_ = 0.10, 2.0
    Bh = 2 * MU0 * I_ * R_ ** 2 / (2 * (R_ ** 2 + (R_ / 2) ** 2) ** 1.5)
    chk = wire_field(arc_path(R_, 2 * math.pi, z=-R_ / 2), I_, (0, 0, 0))[2] + wire_field(arc_path(R_, 2 * math.pi, z=R_ / 2), I_, (0, 0, 0))[2]
    check(Bh, chk, 1e-3, "two coaxial loops by Biot-Savart summation")
    mcq_num(B, c, "Magnetic field of a loop", 3, "Two identical coaxial circular loops of radius $0.10\\,\\mathrm{m}$, a distance $0.10\\,\\mathrm{m}$ apart (Helmholtz arrangement), each carry $2.0\\,\\mathrm{A}$ in the same sense. What is the field at the point on the axis midway between them?", Bh, [2 * MU0 * I_ / (2 * R_), MU0 * I_ / (2 * R_), 2 * MU0 * I_ * R_ ** 2 / (2 * (R_ / 2) ** 3), Bh * 2], "T", ex("Each loop is $z=R/2=0.050\\,\\mathrm{m}$ from the midpoint: $B_1=\\dfrac{\\mu_0IR^2}{2(R^2+z^2)^{3/2}}=\\dfrac{(4\\pi\\times10^{-7})(2.0)(0.010)}{2(0.0125)^{3/2}}=9.0\\times10^{-6}\\,\\mathrm{T}$.", "Both point the same way: $B=2B_1=1.8\\times10^{-5}\\,\\mathrm{T}$ (and the field is remarkably uniform near the midpoint)."), GEN(LEC6 + ", 6.1"), "gen", sig=2)
    a2, y2, I2 = 0.05, 0.12, 10.0
    B2 = MU0 * I2 * y2 / (math.pi * (a2 ** 2 + y2 ** 2))
    pos1, pos2 = np.array([-a2, 0.0]), np.array([a2, 0.0]); P = np.array([0.0, y2])
    def bfield(p_w, I, P):
        d = P - p_w; r2 = d @ d
        return MU0 * I / (2 * math.pi * r2) * np.array([-d[1], d[0]])      # B = mu0 I / (2 pi r) in the direction z-hat x r-hat
    Bn = np.linalg.norm(bfield(pos1, I2, P) + bfield(pos2, I2, P))
    check(B2, Bn, 1e-9)
    mcq_num(B, c, "Magnetic field of a straight wire", 3, "Two long parallel wires, $10\\,\\mathrm{cm}$ apart ($\\pm5.0\\,\\mathrm{cm}$ from the origin), carry $10\\,\\mathrm{A}$ in the same direction. What is the field magnitude at the point $12\\,\\mathrm{cm}$ from the midpoint on the perpendicular bisector?", B2, [2 * MU0 * I2 / (2 * math.pi * math.hypot(a2, y2)), 0.0, MU0 * I2 / (2 * math.pi * y2), MU0 * I2 * a2 / (math.pi * (a2 ** 2 + y2 ** 2))], "T", ex("Each wire is $\\sqrt{0.05^2+0.12^2}=0.13\\,\\mathrm{m}$ from the point: $B_1=\\dfrac{\\mu_0I}{2\\pi r}=1.5\\times10^{-5}\\,\\mathrm{T}$, perpendicular to the line from the wire.", "The components along the bisector cancel (the wires are symmetric); the components parallel to the line joining the wires add: $B=2B_1\\dfrac{y}{r}=2(1.5\\times10^{-5})\\dfrac{0.12}{0.13}=2.8\\times10^{-5}\\,\\mathrm{T}$ (equivalently $\\dfrac{\\mu_0Iy}{\\pi(a^2+y^2)}$)."), GEN(TUT + ", Biot-Savart law"), "gen", sig=2)
    I0, rr = 100.0, 0.40
    mcq_num(B, c, "Magnetic field of a straight wire", 2, "How far from a long straight wire carrying $100\\,\\mathrm{A}$ is the field equal to Earth's field, $5.0\\times10^{-5}\\,\\mathrm{T}$?", MU0 * I0 / (2 * math.pi * 5.0e-5), [MU0 * I0 / (5.0e-5), 2 * math.pi * 5.0e-5 / (MU0 * I0), MU0 * I0 / (2 * math.pi * 5.0e-5) / 2, MU0 * I0 / (2 * math.pi * 5.0e-5 ** 2)], "m", ex("$r=\\dfrac{\\mu_0I}{2\\pi B}=\\dfrac{(4\\pi\\times10^{-7})(100)}{2\\pi(5.0\\times10^{-5})}=0.40\\,\\mathrm{m}$."), GEN(TUT + ", Example 6.2.1"), "gen", sig=2)
    Bw = 3.0e-5; rw = 0.05
    Iw = 2 * math.pi * rw * Bw / MU0
    mcq_num(B, c, "Magnetic field of a straight wire", 2, "The magnetic field $5.0\\,\\mathrm{cm}$ from a long straight wire is $3.0\\times10^{-5}\\,\\mathrm{T}$. What current does it carry?", Iw, [Iw * 2, Iw / 2, 2 * math.pi * rw * Bw * MU0, Bw * rw / MU0], "A", ex("$I=\\dfrac{2\\pi rB}{\\mu_0}=\\dfrac{2\\pi(0.050)(3.0\\times10^{-5})}{4\\pi\\times10^{-7}}=7.5\\,\\mathrm{A}$."), GEN(TUT + ", Example 6.2.1"), "gen", sig=2)
    I_c, ra, rb = 5.0, 0.002, 0.006
    mcq_num(B, c, "Ampere's law", 3, "A coaxial cable has an inner conductor carrying $5.0\\,\\mathrm{A}$ and an outer sleeve carrying $5.0\\,\\mathrm{A}$ in the opposite direction. What is the field at $r=2.0\\,\\mathrm{cm}$, outside the cable?", 0.0, [MU0 * I_c / (2 * math.pi * 0.02), MU0 * I_c / (2 * math.pi * 0.02) * 2, MU0 * I_c / (math.pi * 0.02), MU0 * I_c / (2 * math.pi * 0.02) / 2], "T", ex("An amperian circle outside the cable encloses $+5.0\\,\\mathrm{A}-5.0\\,\\mathrm{A}=0$, so $B=0$: a coaxial cable does not radiate a magnetic field (inside, between the conductors, $B=\\dfrac{\\mu_0I}{2\\pi r}$)."), GEN(LEC6 + ", 6.2 Ampere's law"), "gen", sig=2)
    N_, I_s, B_t = 800, 5.0, 0.020
    L_s = MU0 * N_ * I_s / B_t
    mcq_num(B, c, "Solenoids and toroids", 2, "How long must a solenoid with $800$ turns and a current of $5.0\\,\\mathrm{A}$ be to have an interior field of $20\\,\\mathrm{mT}$?", L_s, [B_t * N_ * I_s / MU0, MU0 * N_ * I_s * B_t, L_s / 2, L_s * 2], "m", ex("$B=\\mu_0\\dfrac NLI\\Rightarrow L=\\dfrac{\\mu_0NI}{B}=\\dfrac{(4\\pi\\times10^{-7})(800)(5.0)}{0.020}=0.25\\,\\mathrm{m}$."), GEN(LEC6 + ", 6.3"), "gen", sig=2)
    n_, I_ = 2000.0, 3.0
    mcq_num(B, c, "Solenoids and toroids", 1, "A long solenoid has $2000$ turns per metre and carries $3.0\\,\\mathrm{A}$. What is the field inside it?", MU0 * n_ * I_, [MU0 * n_ * I_ / 2, MU0 * I_ / n_, MU0 * n_ * I_ * 2 * math.pi, MU0 * n_], "T", ex("$B=\\mu_0nI=(4\\pi\\times10^{-7})(2000)(3.0)=7.5\\times10^{-3}\\,\\mathrm{T}$."), GEN(LEC6 + ", 6.3"), "gen", sig=2)
    mcq_num(B, c, "Magnetic field of a loop", 2, "A single circular loop of radius $5.0\\,\\mathrm{cm}$ must produce a field of $1.0\\,\\mathrm{mT}$ at its centre. What current is needed?", 2 * 0.05 * 1.0e-3 / MU0, [0.05 * 1.0e-3 / MU0, 2 * math.pi * 0.05 * 1.0e-3 / MU0, 4 * 0.05 * 1.0e-3 / MU0, 2 * 0.05 * 1.0e-3 / MU0 / 2], "A", ex("$B=\\dfrac{\\mu_0I}{2R}\\Rightarrow I=\\dfrac{2RB}{\\mu_0}=\\dfrac{2(0.050)(1.0\\times10^{-3})}{4\\pi\\times10^{-7}}=80\\,\\mathrm{A}$."), GEN(TUT + ", Example 6.2.2"), "gen", sig=2)
    R_s = 0.10
    mcq_num(B, c, "Biot-Savart law", 3, "A wire carrying $5.0\\,\\mathrm{A}$ forms a SEMICIRCLE of radius $0.10\\,\\mathrm{m}$ closed by long straight leads that run radially in line with the centre. What is the field at the centre?", MU0 * 5.0 / (4 * R_s), [MU0 * 5.0 / (2 * R_s), MU0 * 5.0 / (8 * R_s), MU0 * 5.0 / (4 * math.pi * R_s), 0.0], "T", ex("The leads point along the line through the centre ($\\mathrm{d}\\vec s\\parallel\\hat r$), so $\\mathrm{d}\\vec s\\times\\hat r=0$: they contribute nothing. The semicircle gives half a loop: $B=\\dfrac{\\mu_0I}{4R}=\\dfrac{(4\\pi\\times10^{-7})(5.0)}{4(0.10)}=1.6\\times10^{-5}\\,\\mathrm{T}$."), GEN(TUT + ", magnetic field from an arc of current"), "gen", sig=2)
    mcq_pick(B, c, "Biot-Savart law", 2, "The magnetic constant $\\mu_0$ has the value", ["$4\\pi\\times10^{-7}\\,\\mathrm{T\\,m/A}$", "$8.99\\times10^{9}\\,\\mathrm{T\\,m/A}$", "$8.85\\times10^{-12}\\,\\mathrm{T\\,m/A}$", "$4\\pi\\times10^{7}\\,\\mathrm{T\\,m/A}$"], 0, ex("$\\mu_0=4\\pi\\times10^{-7}\\,\\mathrm{T\\,m/A}$ (permeability of free space); $8.85\\times10^{-12}$ is the permittivity $\\varepsilon_0$."), LEC6 + ", 6.1", "concept")
    mcq_pick(B, c, "Ampere's law", 1, "Ampère's law $\\oint\\vec B\\cdot\\mathrm{d}\\vec s=\\mu_0I_{\\text{enc}}$ is most useful for finding $B$ when the current distribution has", ["symmetry (long wire, solenoid, toroid, sheet)", "any shape", "no symmetry", "a changing current only"], 0, ex("As with Gauss' law, symmetry lets $B$ be pulled out of the line integral, so that $B\\,(\\text{path length})=\\mu_0I_{\\text{enc}}$."), LEC6 + ", 6.2", "concept")

def ch7b(B):
    c = "c7"
    # Lenz's rule, computed from epsilon = -dPhi/dt with Phi positive for a field out of the page
    for fieldsgn, trend in [("out of", "increasing"), ("out of", "decreasing"), ("into", "increasing"), ("into", "decreasing")]:
        dB = +1.0 if trend == "increasing" else -1.0
        dphidt = dB if fieldsgn == "out of" else -dB                                       # d(Phi_out)/dt: |B| changes by dB, Phi_out = +|B| A (out of the page) or -|B| A (into it)
        emf = -dphidt                                                                       # emf > 0: counter-clockwise current (normal out of the page)
        right = "counter-clockwise" if emf > 0 else "clockwise"
        wrong = "clockwise" if emf > 0 else "counter-clockwise"
        mcq_text(B, c, "Lenz's law", 2, "A uniform magnetic field %s the page through a circular loop in the plane of the page is %s in magnitude. What is the direction of the induced current?" % (fieldsgn, trend), "%s" % right, [wrong, "zero (the field is uniform)", "it alternates"],
                 ex("Lenz's law: the induced current opposes the CHANGE of flux. The flux %s is %s, so the induced field must %s." % (fieldsgn, trend, ("point out of the page (it adds to a decreasing outward flux)" if (fieldsgn == "out of" and trend == "decreasing") or (fieldsgn == "into" and trend == "increasing") else "point into the page (it opposes an increasing outward flux)" if fieldsgn == "out of" else "point into the page (it adds to a decreasing inward flux)")), "By the right-hand rule the loop current that gives that field is %s." % right), GEN(FIN + ", Lenz's law"), "gen")
    # B(t) polynomial with sympy
    import sympy as sp
    t = sp.symbols("t")
    Bt = 0.50 * t ** 2; A_, N_ = 0.04, 50
    eps = sp.diff(N_ * A_ * Bt, t).subs(t, 2.0)
    mcq_num(B, c, "Faraday's law", 2, "A coil of $50$ turns and area $0.040\\,\\mathrm{m^2}$ is perpendicular to a field that varies as $B=0.50\\,t^2$ (tesla, with $t$ in seconds). What is the induced emf at $t=2.0\\,\\mathrm{s}$?", float(eps), [N_ * A_ * 0.50 * 2.0 ** 2, N_ * A_ * 0.50 * 2.0 / 2, A_ * 0.50 * 2 * 2.0, float(eps) * 2], "V", ex("$\\Phi=NBA=50(0.040)(0.50\\,t^2)=1.0\\,t^2$ (Wb), so $|\\varepsilon|=\\dfrac{\\mathrm{d}\\Phi}{\\mathrm{d}t}=2.0\\,t=4.0\\,\\mathrm{V}$ at $t=2.0\\,\\mathrm{s}$ (not $\\Phi/t$: the emf is the RATE of change)."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    Bw, span, vplane = 5.0e-5, 40.0, 250.0
    mcq_num(B, c, "Motional emf", 2, "An aircraft with a $40\\,\\mathrm{m}$ wingspan flies horizontally at $250\\,\\mathrm{m/s}$ through the vertical component of Earth's field, $5.0\\times10^{-5}\\,\\mathrm{T}$. What emf appears between the wingtips?", Bw * span * vplane, [Bw * span, Bw * vplane, Bw * span * vplane * 2, Bw * span / vplane], "V", ex("The wing is a rod of length $L=40\\,\\mathrm{m}$ moving across the field: $\\varepsilon=BLv=(5.0\\times10^{-5})(40)(250)=0.50\\,\\mathrm{V}$ (not measurable with a voltmeter attached to the wingtips: it is just the other half of a circuit moving in the same field)."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    Bc, r0, vr = 0.40, 0.10, 0.002
    ec = Bc * 2 * math.pi * r0 * vr
    mcq_num(B, c, "Faraday's law", 3, "A circular loop in a uniform $0.40\\,\\mathrm{T}$ field (perpendicular to it) expands so that its radius grows at $2.0\\,\\mathrm{mm/s}$. What is the induced emf when $r=0.10\\,\\mathrm{m}$?", ec, [Bc * math.pi * r0 ** 2 * vr, Bc * 2 * math.pi * r0, ec * 2, Bc * r0 * vr], "V", ex("$\\Phi=B\\pi r^2\\Rightarrow\\varepsilon=B\\dfrac{\\mathrm{d}(\\pi r^2)}{\\mathrm{d}t}=2\\pi rB\\dfrac{\\mathrm{d}r}{\\mathrm{d}t}=2\\pi(0.10)(0.40)(0.0020)=5.0\\times10^{-4}\\,\\mathrm{V}$."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    eps_, R_ = 0.10, 0.50
    mcq_num(B, c, "Faraday's law", 1, "A loop of resistance $0.50\\,\\Omega$ has an induced emf of $0.10\\,\\mathrm{V}$. What current flows?", eps_ / R_, [eps_ * R_, R_ / eps_, eps_ / R_ / 2, eps_ / R_ * 2], "A", ex("$I=\\dfrac{\\varepsilon}{R}=\\dfrac{0.10}{0.50}=0.20\\,\\mathrm{A}$."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    N_, I_, Phi_ = 200, 2.0, 5.0e-4
    L = N_ * Phi_ / I_
    mcq_num(B, c, "Inductance", 2, "A coil of $200$ turns carries $2.0\\,\\mathrm{A}$, producing a flux of $5.0\\times10^{-4}\\,\\mathrm{Wb}$ through each turn. What is its inductance?", L, [Phi_ / I_, N_ * Phi_ * I_, N_ * I_ / Phi_, L * 2], "H", ex("$L=\\dfrac{N\\Phi_B}{I}=\\dfrac{(200)(5.0\\times10^{-4})}{2.0}=0.050\\,\\mathrm{H}$ (the flux LINKAGE $N\\Phi_B$, not the flux of one turn)."), LEC7 + ", 7.5", "gen", sig=2)
    emf_, dI = 0.30, 15.0
    mcq_num(B, c, "Inductance", 1, "An inductor shows a self-induced emf of $0.30\\,\\mathrm{V}$ when the current changes at $15\\,\\mathrm{A/s}$. What is its inductance?", emf_ / dI, [emf_ * dI, dI / emf_, emf_ / dI * 2, emf_ / dI / 2], "H", ex("$L=\\dfrac{|\\varepsilon_L|}{|\\mathrm{d}I/\\mathrm{d}t|}=\\dfrac{0.30}{15}=0.020\\,\\mathrm{H}$."), LEC7 + ", 7.6", "gen", sig=2)
    n_, I_, A_ = 5000.0, 2.0, 3.0e-4
    Phi = MU0 * n_ * I_ * A_
    mcq_num(B, c, "Magnetic flux", 2, "A long solenoid has $5000$ turns per metre and carries $2.0\\,\\mathrm{A}$. What is the flux through one turn of cross-section $3.0\\,\\mathrm{cm^2}$?", Phi, [MU0 * n_ * I_, MU0 * n_ * I_ / A_, Phi * 2, Phi / 2], "Wb", ex("$B=\\mu_0nI=(4\\pi\\times10^{-7})(5000)(2.0)=1.26\\times10^{-2}\\,\\mathrm{T}$.", "$\\Phi_B=BA=(1.26\\times10^{-2})(3.0\\times10^{-4})=3.8\\times10^{-6}\\,\\mathrm{Wb}$."), LEC7 + ", 7.1", "gen", sig=2)
    Lq, Iq = 0.50, 4.0
    mcq_num(B, c, "Inductance", 2, "How much energy is stored in a $0.50\\,\\mathrm{H}$ coil carrying $4.0\\,\\mathrm{A}$?", 0.5 * Lq * Iq ** 2, [Lq * Iq ** 2, 0.5 * Lq * Iq, Lq * Iq, 0.5 * Lq ** 2 * Iq], "J", ex("$U=\\tfrac12LI^2=\\tfrac12(0.50)(4.0)^2=4.0\\,\\mathrm{J}$."), LEC7 + ", 7.5", "gen", sig=2)
    mcq_pick(B, c, "Motional emf", 2, "A metal rod moves through a uniform magnetic field with its velocity parallel to the field lines. The motional emf along the rod is", ["zero", "$BLv$", "$BLv/2$", "$B/(Lv)$"], 0, ex("$\\varepsilon=\\oint(\\vec v\\times\\vec B)\\cdot\\mathrm{d}\\vec l=0$ when $\\vec v\\parallel\\vec B$: the magnetic force on the charges vanishes."), LEC7 + ", 7.2", "concept")
    mcq_pick(B, c, "Lenz's law", 2, "Lenz's law is a statement of conservation of", ["energy", "charge", "momentum only", "mass"], 0, ex("If the induced current aided the change that causes it, the effect would feed itself and energy would be created from nothing; the opposition means mechanical work must be done to induce the current."), LEC7 + ", 7.2", "concept")
    mcq_pick(B, c, "Induced electric fields", 2, "An electric field induced by a changing magnetic field has field lines that", ["form closed loops (it is not conservative)", "start on positive charges and end on negative charges", "are always straight", "are always parallel to $\\vec B$"], 0, ex("Faraday's law: $\\oint\\vec E\\cdot\\mathrm{d}\\vec s=-\\dfrac{\\mathrm{d}\\Phi_B}{\\mathrm{d}t}\\neq0$, so $\\vec E$ circulates: the induced field is non-conservative and potential is not defined for it."), LEC7 + ", 7.4", "concept")
    mcq_pick(B, c, "Faraday's law", 2, "A coil is rotated at constant angular speed in a uniform magnetic field. The induced emf is", ["sinusoidal in time", "constant", "zero", "proportional to $t^2$"], 0, ex("$\\Phi=NBA\\cos\\omega t$, so $\\varepsilon=NBA\\omega\\sin\\omega t$ - the principle of the AC generator."), LEC7 + ", 7.2", "concept")
    tau, R_, L_ = 0.050, 4.0, 0.20
    mcq_num(B, c, "RL circuits", 3, "An RL circuit has $R=4.0\\,\\Omega$ and $L=0.20\\,\\mathrm{H}$. What is its time constant?", L_ / R_, [R_ * L_, R_ / L_, L_ * R_ ** 2, L_ / R_ * 2], "s", ex("$\\tau=\\dfrac LR=\\dfrac{0.20}{4.0}=0.050\\,\\mathrm{s}$: after $\\tau$ the current has reached $63\\%$ of its final value."), "Magnetism lecture (2025-26): beyond the chapter 7 outline (RL circuit)", "gen", sig=2, tags=("extension",))


def ch6c(B):
    c = "c6"
    I_, R_ = 2.0, 0.05
    zc = 0.50
    Bex = MU0 * I_ * R_ ** 2 / (2 * (R_ ** 2 + zc ** 2) ** 1.5)
    chk = wire_field(arc_path(R_, 2 * math.pi), I_, (0, 0, zc))[2]
    check(Bex, chk, 1e-3)
    mcq_num(B, c, "Magnetic field of a loop", 2, "A circular loop of radius $5.0\\,\\mathrm{cm}$ carries $2.0\\,\\mathrm{A}$. What is the field on its axis $0.50\\,\\mathrm{m}$ from the centre?", Bex, [MU0 * I_ / (2 * R_), MU0 * I_ * R_ ** 2 / (2 * zc ** 2), MU0 * I_ / (2 * zc), Bex * 2], "T", ex("$B=\\dfrac{\\mu_0IR^2}{2(R^2+z^2)^{3/2}}=\\dfrac{(4\\pi\\times10^{-7})(2.0)(0.0025)}{2(0.2525)^{3/2}}=2.5\\times10^{-8}\\,\\mathrm{T}$; far away it behaves like a dipole, $\\dfrac{\\mu_0\\mu}{2\\pi z^3}$, falling as $1/z^3$. Numerical summation of the Biot-Savart law agrees."), GEN(LEC6 + ", 6.1"), "gen", sig=2)
    sgn = wire_field(arc_path(0.1, 2 * math.pi), 1.0, (0, 0, 0))[2]
    mcq_pick(B, c, "Magnetic field of a loop", 2, "A circular loop in the $xy$ plane carries a current that is COUNTER-CLOCKWISE when viewed from $+z$. The magnetic field at the centre of the loop points", ["along $+z$ (towards the viewer)", "along $-z$ (away from the viewer)", "in the plane of the loop, tangent to it", "radially outward"], 0 if sgn > 0 else 1, ex("Right-hand rule for a loop: curl the fingers along the current (counter-clockwise from above); the thumb points along $\\vec B$ at the centre: towards the viewer, $+z$. A numerical Biot-Savart sum confirms the sign."), LEC6 + ", 6.1 (right-hand rule)", "concept")
    q, v_, r_ = E_CH, 3.0e6, 1.0e-9
    Bq = 1e-7 * q * v_ / r_ ** 2
    mcq_num(B, c, "Biot-Savart law", 3, "A proton moves at $3.0\\times10^{6}\\,\\mathrm{m/s}$. What is the magnitude of the magnetic field it produces at a point $1.0\\,\\mathrm{nm}$ away, perpendicular to its velocity?", Bq, [1e-7 * q * v_ / r_, 1e-7 * q * v_ ** 2 / r_ ** 2, Bq * 2, Bq / 10], "T", ex("A moving point charge: $B=\\dfrac{\\mu_0}{4\\pi}\\dfrac{qv\\sin\\theta}{r^2}=(10^{-7})\\dfrac{(1.602\\times10^{-19})(3.0\\times10^6)}{(1.0\\times10^{-9})^2}=4.8\\times10^{-2}\\,\\mathrm{T}$."), GEN(LEC6 + ", 6.1"), "gen", sig=2)
    mcq_pick(B, c, "Ampere's law", 2, "A long hollow cylindrical conductor carries a current uniformly over its surface. The magnetic field INSIDE the hollow region is", ["zero", "$\\mu_0I/(2\\pi r)$", "uniform and non-zero", "proportional to $r$"], 0, ex("An amperian circle inside the hollow encloses no current, so $B(2\\pi r)=0\\Rightarrow B=0$ (outside, $B=\\mu_0I/2\\pi r$)."), LEC6 + ", 6.2", "concept")
    I1 = 6.0; r1 = 0.03
    mcq_num(B, c, "Magnetic field of a straight wire", 2, "Two long straight wires cross at right angles without touching (like the $x$ and $y$ axes) and carry $6.0\\,\\mathrm{A}$ each. At the point $(3.0\\,\\mathrm{cm},\\,3.0\\,\\mathrm{cm})$ the two fields are perpendicular to the plane of the wires. If they point in the SAME direction there, what is the total field?", 2 * MU0 * I1 / (2 * math.pi * r1), [MU0 * I1 / (2 * math.pi * r1), 0.0, 2 * MU0 * I1 / (2 * math.pi * r1) * math.sqrt(2) / 2, 4 * MU0 * I1 / (2 * math.pi * r1)], "T", ex("Each wire is $3.0\\,\\mathrm{cm}$ from the point: $B_1=\\dfrac{\\mu_0I}{2\\pi r}=4.0\\times10^{-5}\\,\\mathrm{T}$. Parallel fields add arithmetically: $B=2B_1=8.0\\times10^{-5}\\,\\mathrm{T}$ (if they pointed in opposite directions: zero)."), GEN(TUT + ", Biot-Savart law"), "gen", sig=2)
    mcq_pick(B, c, "Solenoids and toroids", 2, "The current in a long solenoid is doubled while the number of turns per metre is halved. The magnetic field inside it", ["is unchanged", "is doubled", "is halved", "is quadrupled"], 0, ex("$B=\\mu_0nI$: $(n/2)(2I)=nI$."), GEN(LEC6 + ", 6.3"), "gen")
    mcq_pick(B, c, "Magnetic field of a straight wire", 2, "How does the field of a long straight wire change if the distance from it is doubled and the current is also doubled?", ["it is unchanged", "it doubles", "it is halved", "it quadruples"], 0, ex("$B=\\dfrac{\\mu_0I}{2\\pi r}$: $(2I)/(2r)=I/r$."), GEN(TUT + ", Biot-Savart law"), "gen")

def ch7c(B):
    c = "c7"
    B_, r_, th = 0.60, 0.05, 30.0
    Phi = B_ * math.pi * r_ ** 2 * math.cos(math.radians(th))
    mcq_num(B, c, "Magnetic flux", 2, "A circular loop of radius $5.0\\,\\mathrm{cm}$ is in a uniform $0.60\\,\\mathrm{T}$ field. The loop's normal makes an angle of $30^\\circ$ with the field. What is the flux through the loop?", Phi, [B_ * math.pi * r_ ** 2 * math.sin(math.radians(th)), B_ * math.pi * r_ ** 2, B_ * 2 * math.pi * r_ * math.cos(math.radians(th)), Phi * 2], "Wb", ex("$\\Phi_B=B\\,\\pi r^2\\cos\\theta=(0.60)\\pi(0.050)^2\\cos30^\\circ=4.1\\times10^{-3}\\,\\mathrm{Wb}$."), GEN(LEC7 + ", 7.1"), "gen", sig=2)
    mcq_pick(B, c, "Magnetic flux", 1, "The flux of a uniform field through a loop is zero when", ["the plane of the loop is parallel to the field", "the plane of the loop is perpendicular to the field", "the field is strong", "the loop is large"], 0, ex("$\\Phi=BA\\cos\\theta$ is zero for $\\theta=90^\\circ$, i.e. when the normal is perpendicular to $\\vec B$ (the loop edge-on to the field lines)."), LEC7 + ", 7.1", "concept")
    N_, dPhi, dt = 50, 0.040, 0.020
    mcq_num(B, c, "Faraday's law", 2, "The magnetic flux through each turn of a $50$-turn coil falls uniformly from $0.040\\,\\mathrm{Wb}$ to zero in $0.020\\,\\mathrm{s}$. What is the induced emf?", N_ * dPhi / dt, [dPhi / dt, N_ * dPhi * dt, N_ * dPhi, N_ * dPhi / dt / 2], "V", ex("$|\\varepsilon|=N\\left|\\dfrac{\\Delta\\Phi}{\\Delta t}\\right|=50\\times\\dfrac{0.040}{0.020}=100\\,\\mathrm{V}$."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    A_, dBdt, R_ = 0.01, 0.50, 0.10
    mcq_num(B, c, "Faraday's law", 2, "A single loop of area $0.010\\,\\mathrm{m^2}$ and resistance $0.10\\,\\Omega$ is perpendicular to a field changing at $0.50\\,\\mathrm{T/s}$. What current is induced?", A_ * dBdt / R_, [A_ * dBdt * R_, A_ * dBdt, dBdt / R_, A_ * dBdt / R_ * 2], "A", ex("$\\varepsilon=A\\left|\\dfrac{\\mathrm{d}B}{\\mathrm{d}t}\\right|=(0.010)(0.50)=5.0\\times10^{-3}\\,\\mathrm{V}$; $I=\\dfrac{\\varepsilon}{R}=\\dfrac{5.0\\times10^{-3}}{0.10}=0.050\\,\\mathrm{A}$."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    N1, N2, A_, l_ = 1000, 50, 2.0e-4, 0.20
    M = MU0 * N1 * N2 * A_ / l_
    mcq_num(B, c, "Inductance", 3, "A coil of $50$ turns is wound tightly around the middle of a long solenoid ($1000$ turns, length $0.20\\,\\mathrm{m}$, cross-section $2.0\\,\\mathrm{cm^2}$). What is their mutual inductance?", M, [MU0 * N1 * A_ / l_, MU0 * N1 ** 2 * A_ / l_, MU0 * N1 * N2 * A_ * l_, M * 2], "H", ex("A current $I_1$ in the solenoid gives $B=\\mu_0\\dfrac{N_1}{\\ell}I_1$ and a flux $BA$ through each turn of the small coil: $M=\\dfrac{N_2\\Phi_{21}}{I_1}=\\dfrac{\\mu_0N_1N_2A}{\\ell}=\\dfrac{(4\\pi\\times10^{-7})(1000)(50)(2.0\\times10^{-4})}{0.20}=6.3\\times10^{-5}\\,\\mathrm{H}$."), GEN(LEC7 + ", 7.6"), "gen", sig=2)
    mcq_pick(B, c, "Inductance", 1, "The henry (H) is equal to", ["$1\\,\\mathrm{V\\,s/A}=1\\,\\mathrm{Wb/A}$", "$1\\,\\mathrm{V/A}$", "$1\\,\\mathrm{A\\,s/V}$", "$1\\,\\mathrm{T/A}$"], 0, ex("$L=\\dfrac{N\\Phi_B}{I}$ gives Wb/A, and $\\varepsilon=L\\dfrac{\\mathrm{d}I}{\\mathrm{d}t}$ gives V s/A."), LEC7 + ", 7.5", "concept")
    mcq_pick(B, c, "Lenz's law", 2, "A magnet falls through a long vertical copper tube and takes much longer than a non-magnetic object. The explanation is", ["eddy currents induced in the tube oppose the magnet's motion", "the tube is magnetised permanently", "air resistance is greater inside a tube", "the magnet is attracted to the copper"], 0, ex("Lenz's law: the changing flux induces currents in the tube whose fields oppose the magnet's motion (a magnetic braking force). Copper is not magnetic and the magnet is not attracted to it."), LEC7 + ", 7.2 (Lenz's law)", "concept")
    mcq_pick(B, c, "Inductance", 2, "In a circuit carrying a STEADY direct current, an ideal inductor behaves like", ["a plain wire (no voltage across it)", "an open circuit", "a resistor $\\omega L$", "a source of emf $L\\,I$"], 0, ex("$\\varepsilon_L=-L\\dfrac{\\mathrm{d}I}{\\mathrm{d}t}=0$ for constant $I$; the inductor only resists CHANGES of current (it stores the energy $\\tfrac12LI^2$)."), LEC7 + ", 7.5-7.6", "concept")
    B_s, A_s, w = 0.30, 0.040, 120.0
    emax = B_s * A_s * w
    mcq_num(B, c, "Faraday's law", 2, "A single square loop of side $0.20\\,\\mathrm{m}$ rotates at $120\\,\\mathrm{rad/s}$ about a diameter in a $0.30\\,\\mathrm{T}$ field. What is the peak emf?", emax, [B_s * A_s, B_s * A_s * w / (2 * math.pi), B_s * 0.20 * w, emax * 2], "V", ex("$\\varepsilon_{\\max}=NBA\\omega=1(0.30)(0.040)(120)=1.4\\,\\mathrm{V}$."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
    mcq_num(B, c, "Faraday's law", 2, "A conducting rod $0.60\\,\\mathrm{m}$ long moves at $3.0\\,\\mathrm{m/s}$ perpendicular to a $0.25\\,\\mathrm{T}$ field. What is the emf between its ends?", 0.25 * 0.60 * 3.0, [0.25 * 3.0, 0.25 * 0.60, 0.25 * 0.60 * 3.0 ** 2, 0.25 * 0.60 * 3.0 / 2], "V", ex("$\\varepsilon=BLv=(0.25)(0.60)(3.0)=0.45\\,\\mathrm{V}$."), GEN(FIN + ", Faraday's law"), "gen", sig=2)
