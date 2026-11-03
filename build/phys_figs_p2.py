# -*- coding: utf-8 -*-
"""Physics II figures (chapters 1-11): each one computed from the law, checked a second way, saved as PNG + CSV (see phys_plots.py)."""
import numpy as np
from scipy import special
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.signal import find_peaks
from phys_plots import *

C = "Physics-2"
K_E, EPS0, MU0, E_CH, M_E, M_P, C_L = 8.99e9, 8.85e-12, 4e-7 * np.pi, 1.602e-19, 9.11e-31, 1.673e-27, 3.0e8

def efield(charges, X, Y):
    """Field (Ex, Ey) of point charges [(q, x, y)] at the points X, Y."""
    ex = np.zeros_like(X, dtype=float); ey = np.zeros_like(X, dtype=float)
    for q, x0, y0 in charges:
        dx, dy = X - x0, Y - y0; r3 = np.hypot(dx, dy) ** 3
        ex += K_E * q * dx / r3; ey += K_E * q * dy / r3
    return ex, ey

# =============================================================================================== chapter 1: Coulomb's law
@figure(C, "p2-c1-inverse-square", "c1", "Coulomb's law: force against distance",
        "$q_1=1\\,\\mu\\mathrm{C}$ and $q_2=2\\,\\mu\\mathrm{C}$. On log-log axes the force is a straight line of slope $-2$: doubling the distance divides the force by four. At $10\\,\\mathrm{cm}$ it is $1.8\\,\\mathrm{N}$.",
        r"F=k\frac{|q_1q_2|}{r^2},\qquad k=\frac1{4\pi\varepsilon_0}=8.99\times10^9\ \mathrm{N\,m^2/C^2}")
def _():
    r = np.logspace(-2, 0, 61); F = K_E * 1e-6 * 2e-6 / r ** 2
    close(np.polyfit(np.log10(r), np.log10(F), 1)[0], -2.0, rel=1e-9, what="slope -2"); close(K_E * 2e-12 / 0.1 ** 2, 1.798, rel=1e-3, what="F at 10 cm"); close(1 / (4 * np.pi * EPS0), K_E, rel=2e-3, what="k = 1/(4 pi eps0)")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.loglog(r * 100, F, color=NAVY); ax.plot([10], [1.798], "o", color=RED); ax.annotate("10 cm: 1.8 N", (13, 2.2), color=RED); panel(ax, "distance r (cm)", "force F (N)")
    fig.tight_layout()
    return dict(r_m=r, F_N=F), fig

@figure(C, "p2-c1-line-forces", "c1", "Net force on a test charge near two fixed charges",
        "$q_1=+2\\,\\mu\\mathrm{C}$ at $x=0$, $q_2=-3\\,\\mu\\mathrm{C}$ at $x=0.10\\,\\mathrm{m}$, test charge $+1\\,\\mu\\mathrm{C}$. The force is repulsive near $q_1$, attractive near $q_2$ and passes through zero once, at $x=-0.445\\,\\mathrm{m}$ (outside, on the side of the weaker charge).",
        r"F(x)=kq_3\sum_i q_i\,\frac{x-x_i}{|x-x_i|^3}")
def _():
    q1, q2, q3 = 2e-6, -3e-6, 1e-6
    def F(x): return K_E * q3 * (q1 * (x - 0.0) / np.abs(x - 0.0) ** 3 + q2 * (x - 0.10) / np.abs(x - 0.10) ** 3)
    xz = brentq(F, -0.7, -0.2); close(xz, 0.1 * np.sqrt(2) / (np.sqrt(2) - np.sqrt(3)), rel=1e-9, what="zero of the net force")
    segs = [np.linspace(-0.7, -0.004, 140), np.linspace(0.004, 0.096, 90), np.linspace(0.104, 0.5, 140)]; xs = np.concatenate(segs)
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    for sg in segs: ax.plot(sg, F(sg), color=NAVY)
    ax.axhline(0, color=GREY, lw=1); ax.plot([xz], [0], "o", color=RED); ax.annotate("F = 0 at x = %.3f m" % xz, (xz + 0.02, 0.8), color=RED)
    ax.axvline(0, color=ORANGE, ls=":"); ax.axvline(0.10, color=ORANGE, ls=":"); ax.text(-0.012, 6.9, "+2 μC", color=ORANGE, ha="right"); ax.text(0.112, 6.9, "−3 μC", color=ORANGE, ha="left"); ax.set_ylim(-8, 8)
    panel(ax, "position x of the test charge (m)", "force on it, along +x (N)")
    fig.tight_layout()
    return dict(x_m=xs, F_N=F(xs)), fig

@figure(C, "p2-c1-square", "c1", "Superposition of forces: the fourth corner of a square",
        "Charges $+2\\,\\mu\\mathrm{C}$ at three corners of a square of side $0.30\\,\\mathrm{m}$ act on a fourth $+2\\,\\mu\\mathrm{C}$: two forces of $0.40\\,\\mathrm{N}$ along the sides and one of $0.20\\,\\mathrm{N}$ along the diagonal. Resultant $0.765\\,\\mathrm{N}$ along the diagonal.",
        r"\vec F=\sum_i\vec F_i,\qquad F=\Big(\sqrt2+\tfrac12\Big)\frac{kq^2}{a^2}")
def _():
    q, a = 2e-6, 0.30; src = [(q, a, 0.0), (q, 0.0, a), (q, a, a)]; ex_, ey_ = efield(src, np.array([0.0]), np.array([0.0])); Fx, Fy = q * ex_[0], q * ey_[0]
    f0 = K_E * q * q / a ** 2; close(np.hypot(Fx, Fy), (np.sqrt(2) + 0.5) * f0, rel=1e-9, what="resultant")
    comps = []
    for qq, x, y in src:
        e1, e2 = efield([(qq, x, y)], np.array([0.0]), np.array([0.0])); comps.append((q * e1[0], q * e2[0]))
    fig, ax = plt.subplots(figsize=(5.6, 5.0)); ax.set_aspect("equal")
    for (qq, x, y) in src: ax.plot([x], [y], "o", color=NAVY, ms=11); ax.text(x + 0.012, y + 0.012, "+2 μC")
    ax.plot([0], [0], "o", color=RED, ms=11); ax.text(0.015, 0.02, "+2 μC (test)", color=RED); sc = 0.17
    for (fx, fy), col in zip(comps, (GREEN, GREEN, ORANGE)): ax.annotate("", xy=(fx * sc, fy * sc), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=2))
    ax.annotate("", xy=(Fx * sc, Fy * sc), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=3)); ax.text(Fx * sc - 0.005, Fy * sc - 0.035, "F = %.3f N" % np.hypot(Fx, Fy), color=RED, ha="center")
    ax.text(-0.205, -0.045, "0.40 N", color=GREEN); ax.text(-0.045, -0.095, "0.40 N", color=GREEN); ax.text(-0.115, -0.065, "0.20 N", color=ORANGE, fontsize=9)
    ax.set_xlim(-0.24, 0.40); ax.set_ylim(-0.24, 0.40); panel(ax, "x (m)", "y (m)")
    fig.tight_layout()
    return dict(source=np.array(["+x neighbour", "+y neighbour", "opposite corner", "resultant"]), Fx_N=np.array([c[0] for c in comps] + [Fx]), Fy_N=np.array([c[1] for c in comps] + [Fy])), fig

# =============================================================================================== chapter 2: electric fields
@figure(C, "p2-c2-dipole-lines", "c2", "Electric field lines of a dipole",
        "$\\pm1\\,\\mathrm{nC}$ at $x=\\pm1\\,\\mathrm{cm}$. Lines leave the positive charge and end on the negative one; the field is strongest between and next to the charges, and at the midpoint it equals $2kq/a^2=1.8\\times10^5\\,\\mathrm{N/C}$.",
        r"\vec E=k\sum_i q_i\frac{\vec r-\vec r_i}{|\vec r-\vec r_i|^3}")
def _():
    a, q = 0.01, 1e-9; ch = [(q, -a, 0.0), (-q, a, 0.0)]
    e0, _y = efield(ch, np.array([0.0]), np.array([0.0])); close(e0[0], 2 * K_E * q / a ** 2, rel=1e-9, what="field at the midpoint")
    g = np.linspace(-0.04, 0.04, 161); X, Y = np.meshgrid(g, g); Ex, Ey = efield(ch, X, Y); close(Ey[:, 80], 0.0, atol=1e-3 * np.abs(Ex).max(), what="Ey = 0 on the mid-plane")
    fig, ax = plt.subplots(figsize=(6.4, 5.0)); sp = np.hypot(Ex, Ey)
    ax.streamplot(X * 100, Y * 100, Ex, Ey, color=np.log10(sp), cmap="viridis", density=1.6, linewidth=1.1, arrowsize=1.1)
    ax.plot([-1], [0], "o", color=RED, ms=10); ax.plot([1], [0], "o", color=NAVY, ms=10); ax.text(-1.0, 0.45, "+", ha="center", fontsize=14, color=RED); ax.text(1.0, 0.45, "−", ha="center", fontsize=16, color=NAVY)
    ax.set_aspect("equal"); ax.set_xlim(-4, 4); ax.set_ylim(-4, 4); panel(ax, "x (cm)", "y (cm)")
    fig.tight_layout(); idx = np.s_[::8, ::8]
    return dict(x_m=X[idx].ravel(), y_m=Y[idx].ravel(), Ex_NC=Ex[idx].ravel(), Ey_NC=Ey[idx].ravel()), fig

@figure(C, "p2-c2-ring-axis", "c2", "Field on the axis of a charged ring",
        "$Q=5\\,\\mathrm{nC}$, $R=6\\,\\mathrm{cm}$: zero at the centre, a maximum at $z=R/\\sqrt2=4.24\\,\\mathrm{cm}$ and an inverse-square tail $kQ/z^2$ far away. At $z=8\\,\\mathrm{cm}$ the field is $3.6\\times10^3\\,\\mathrm{N/C}$.",
        r"E_z=\frac{kQz}{(z^2+R^2)^{3/2}},\qquad E_{\max}\ \text{at}\ z=\frac{R}{\sqrt2}")
def _():
    Q, R = 5e-9, 0.06; z = np.linspace(0, 0.30, 601); E = K_E * Q * z / (z ** 2 + R ** 2) ** 1.5
    close(z[np.argmax(E)], R / np.sqrt(2), atol=6e-4, what="maximum at R/sqrt2"); close(K_E * Q * 0.08 / (0.08 ** 2 + R ** 2) ** 1.5, 3596.0, rel=1e-3, what="E at 8 cm")
    N = 4000; th = (np.arange(N) + 0.5) * 2 * np.pi / N; xr, yr = R * np.cos(th), R * np.sin(th); dq = Q / N; zz = 0.08
    Ez = np.sum(K_E * dq * zz / (xr ** 2 + yr ** 2 + zz ** 2) ** 1.5); close(Ez, K_E * Q * zz / (zz ** 2 + R ** 2) ** 1.5, rel=1e-9, what="sum over charge elements")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(z * 100, E, color=NAVY, label="ring"); ax.plot(z[1:] * 100, K_E * Q / z[1:] ** 2, color=GREY, ls="--", label="point charge kQ/z²"); ax.set_ylim(0, 1.6e4)
    ax.plot([R / np.sqrt(2) * 100], [E.max()], "o", color=RED); ax.annotate("max at R/√2", (R / np.sqrt(2) * 100 + 1, E.max() + 500), color=RED); panel(ax, "distance z along the axis (cm)", "E (N/C)", legend=True)
    fig.tight_layout()
    return dict(z_m=z, E_NC=E), fig

@figure(C, "p2-c2-distance-laws", "c2", "How the field falls with distance for three charge distributions",
        "Point charge $E\\propto1/r^2$, long line of charge $E\\propto1/r$, large sheet $E=\\text{const}$. Log-log slopes: $-2$, $-1$ and $0$. (Each uses $1\\,\\mathrm{nC}$, $1\\,\\mathrm{nC/m}$ and $1\\,\\mathrm{nC/m^2}$.)",
        r"E_{\rm point}=\frac{kQ}{r^2},\qquad E_{\rm line}=\frac{\lambda}{2\pi\varepsilon_0r},\qquad E_{\rm sheet}=\frac{\sigma}{2\varepsilon_0}")
def _():
    r = np.logspace(-2, 0, 41); Ep = K_E * 1e-9 / r ** 2; El = 1e-9 / (2 * np.pi * EPS0 * r); Es = np.full_like(r, 1e-9 / (2 * EPS0))
    for E, s in ((Ep, -2.0), (El, -1.0), (Es, 0.0)): close(np.polyfit(np.log10(r), np.log10(E), 1)[0], s, atol=1e-9, what="log-log slope")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.loglog(r * 100, Ep, color=NAVY, label="point charge  ∝ 1/r²"); ax.loglog(r * 100, El, color=RED, label="line of charge  ∝ 1/r"); ax.loglog(r * 100, Es, color=GREEN, label="large sheet  = const")
    panel(ax, "distance r (cm)", "E (N/C)", legend=True)
    fig.tight_layout()
    return dict(r_m=r, E_point_NC=Ep, E_line_NC=El, E_sheet_NC=Es), fig

@figure(C, "p2-c2-dipole-axis", "c2", "On the axis of a dipole: exact field and the far-field law",
        "Charges $\\pm q$ separated by $2a$: the exact axial field tends to $2kp/z^3$ (inverse cube) once $z\\gg a$; the two curves differ by 2 % at $z=10a$ and by less than $1\\,\\%$ beyond $z=15a$.",
        r"E_{\rm exact}=kq\left[\frac1{(z-a)^2}-\frac1{(z+a)^2}\right]\ \longrightarrow\ \frac{2kp}{z^3},\quad p=2qa")
def _():
    a, q = 0.01, 1e-9; z = np.logspace(np.log10(1.5 * a), np.log10(100 * a), 80); p = 2 * q * a
    Ex = K_E * q * (1 / (z - a) ** 2 - 1 / (z + a) ** 2); Ea = 2 * K_E * p / z ** 3
    close(Ex[z > 15 * a] / Ea[z > 15 * a], 1.0, rel=0.01, what="far-field law within 1 % beyond 15 a"); close(Ex / Ea, 1 / (1 - (a / z) ** 2) ** 2, rel=1e-9, what="exact ratio 1/(1-a^2/z^2)^2"); close(np.polyfit(np.log10(z[z > 20 * a]), np.log10(Ex[z > 20 * a]), 1)[0], -3.0, rel=0.01, what="slope -3")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.loglog(z / a, Ex, color=NAVY, label="exact (two charges)"); ax.loglog(z / a, Ea, color=RED, ls="--", label="2kp/z³"); panel(ax, "distance z / a", "E on the axis (N/C)", legend=True)
    fig.tight_layout()
    return dict(z_over_a=z / a, E_exact_NC=Ex, E_far_field_NC=Ea), fig

# =============================================================================================== chapter 3: Gauss' law
@figure(C, "p2-c3-sphere-profile", "c3", "Field of a charged sphere: insulating ball and conducting shell",
        "Total charge $Q=10\\,\\mathrm{nC}$, radius $R=5\\,\\mathrm{cm}$. Outside, both give $kQ/r^2$. Inside the uniform ball $E=kQr/R^3$ grows linearly; inside the conductor the field is zero (all the charge sits on the surface).",
        r"\oint\vec E\cdot d\vec A=\frac{Q_{\rm enc}}{\varepsilon_0}\ \Rightarrow\ E=\frac{kQ}{r^2}\ (r>R),\quad E=\frac{kQr}{R^3}\ (r<R,\ \text{uniform ball})")
def _():
    Q, R = 10e-9, 0.05; r = np.linspace(0.001, 0.15, 300); Eb = np.where(r < R, K_E * Q * r / R ** 3, K_E * Q / r ** 2); Ec = np.where(r < R, 0.0, K_E * Q / r ** 2)
    close(K_E * Q * R / R ** 3, K_E * Q / R ** 2, what="continuity at R for the ball")
    for rr in (0.03, 0.10):                                           # Gauss' law by explicit integration of the enclosed charge
        enc = Q * min(1.0, (rr / R) ** 3); close(K_E * enc / rr ** 2, np.interp(rr, r, Eb), rel=2e-3, what="Gauss' law at r = %.2f" % rr)
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(r * 100, Eb / 1e3, color=NAVY, label="uniformly charged insulating ball"); ax.plot(r * 100, Ec / 1e3, color=RED, ls="--", label="conducting sphere / shell"); ax.axvline(R * 100, color=GREY, ls=":")
    panel(ax, "distance r from the centre (cm)", "E (kN/C)", legend=True)
    fig.tight_layout()
    return dict(r_m=r, E_insulating_NC=Eb, E_conducting_NC=Ec), fig

@figure(C, "p2-c3-flux-angle", "c3", "Electric flux through a flat surface against its orientation",
        "Uniform field $E=500\\,\\mathrm{N/C}$ and area $A=0.20\\,\\mathrm{m^2}$: $\\Phi=EA\\cos\\theta$ with $\\theta$ the angle between $\\vec E$ and the normal. Maximum $100\\,\\mathrm{N\\,m^2/C}$ face-on, zero edge-on, negative when the normal points against the field.",
        r"\Phi_E=\int\vec E\cdot d\vec A=EA\cos\theta")
def _():
    E, A = 500.0, 0.20; th = np.linspace(0, 180, 181); Phi = E * A * np.cos(np.radians(th)); close(Phi[0], 100.0, what="face-on flux"); close(Phi[90], 0.0, atol=1e-9, what="edge-on flux"); close(Phi[-1], -100.0, what="back side")
    fig, ax = plt.subplots(figsize=(7.2, 3.9)); ax.plot(th, Phi, color=NAVY); ax.axhline(0, color=GREY, lw=1); panel(ax, "angle θ between E and the normal (degrees)", "flux Φ (N m²/C)"); ax.set_xlim(0, 180); ax.set_xticks(range(0, 181, 30))
    fig.tight_layout()
    return dict(theta_deg=th, flux_Nm2C=Phi), fig

@figure(C, "p2-c3-plates", "c3", "Field of infinite charged sheets (superposition)",
        "Each sheet gives $\\sigma/2\\varepsilon_0$ pointing away from it (if positive). Opposite sheets $\\pm\\sigma$: the fields add between them ($\\sigma/\\varepsilon_0$) and cancel outside. Equal sheets: the opposite.",
        r"E_{\rm sheet}=\frac{\sigma}{2\varepsilon_0},\qquad E_{\rm between}=\frac{\sigma}{\varepsilon_0}")
def _():
    sg = 1e-6; x = np.linspace(-3, 3, 601); E1 = sg / (2 * EPS0)
    def sheet(x0, s): return np.sign(x - x0) * s / (2 * EPS0)
    opp = sheet(-1, sg) + sheet(1, -sg); same = sheet(-1, sg) + sheet(1, sg); single = sheet(0, sg)
    close(opp[np.abs(x) < 0.9], sg / EPS0, what="between opposite sheets"); close(opp[np.abs(x) > 1.1], 0.0, atol=1e-6 * E1, what="outside opposite sheets"); close(same[np.abs(x) < 0.9], 0.0, atol=1e-6 * E1, what="between like sheets")
    fig, ax = plt.subplots(figsize=(7.4, 4.0)); ax.plot(x, single / 1e3, color=GREY, label="one sheet at x = 0"); ax.plot(x, opp / 1e3, color=NAVY, label="+σ at x = −1, −σ at x = +1"); ax.plot(x, same / 1e3, color=RED, ls="--", label="+σ at x = ±1")
    ax.axvline(-1, color=ORANGE, ls=":"); ax.axvline(1, color=ORANGE, ls=":"); panel(ax, "x (m)", "Eₓ (kN/C)  for σ = 1 μC/m²", legend=True); ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    return dict(x_m=x, E_single_NC=single, E_opposite_NC=opp, E_equal_NC=same), fig

@figure(C, "p2-c3-cylinder", "c3", "Field of a long uniformly charged cylinder",
        "Charge per length $\\lambda=2\\,\\mathrm{nC/m}$, radius $R=2\\,\\mathrm{cm}$: inside $E=\\lambda r/(2\\pi\\varepsilon_0R^2)$ (linear), outside $E=\\lambda/(2\\pi\\varepsilon_0r)$ (inverse), continuous at the surface.",
        r"E\,2\pi rL=\frac{\lambda_{\rm enc}L}{\varepsilon_0}\ \Rightarrow\ E=\frac{\lambda}{2\pi\varepsilon_0r}\ (r>R)")
def _():
    lam, R = 2e-9, 0.02; r = np.linspace(0.001, 0.10, 300); E = np.where(r < R, lam * r / (2 * np.pi * EPS0 * R ** 2), lam / (2 * np.pi * EPS0 * r)); close(lam * R / (2 * np.pi * EPS0 * R ** 2), lam / (2 * np.pi * EPS0 * R), what="continuity at R")
    close(E[r > R] * r[r > R], lam / (2 * np.pi * EPS0), what="E r = const outside")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(r * 100, E, color=NAVY); ax.axvline(R * 100, color=GREY, ls=":"); panel(ax, "distance r from the axis (cm)", "E (N/C)")
    fig.tight_layout()
    return dict(r_m=r, E_NC=E), fig

# =============================================================================================== chapter 4: electric potential
@figure(C, "p2-c4-equipotentials", "c4", "Equipotentials of a dipole and the field they imply",
        "Equipotentials (colour, labelled in volts) are perpendicular to the field lines; the field points from high to low potential. Here $\\pm1\\,\\mathrm{nC}$ at $x=\\pm1\\,\\mathrm{cm}$ and the mid-plane is at $0\\,\\mathrm{V}$.",
        r"\vec E=-\nabla V,\qquad V=k\sum_i\frac{q_i}{r_i}")
def _():
    a, q = 0.01, 1e-9; g = np.linspace(-0.04, 0.04, 321); X, Y = np.meshgrid(g, g)
    r1 = np.hypot(X + a, Y); r2 = np.hypot(X - a, Y); V = K_E * q * (1 / r1 - 1 / r2); Ex, Ey = efield([(q, -a, 0.0), (-q, a, 0.0)], X, Y)
    gy, gx = np.gradient(V, g, g, edge_order=2); sel = (np.abs(X) < 0.03) & (np.abs(Y) < 0.03) & (np.hypot(X + a, Y) > 0.006) & (np.hypot(X - a, Y) > 0.006)
    close(-gx[sel], Ex[sel], rel=0.02, atol=0.003 * np.abs(Ex[sel]).max(), what="E = -dV/dx"); close(-gy[sel], Ey[sel], rel=0.02, atol=0.003 * np.abs(Ey[sel]).max(), what="E = -dV/dy")
    close(V[:, 160], 0.0, atol=1e-6 * np.abs(V).max(), what="mid-plane at 0 V")
    fig, ax = plt.subplots(figsize=(6.6, 5.2)); lv = [-1200, -800, -500, -300, -150, 0, 150, 300, 500, 800, 1200]
    cmap = plt.get_cmap("RdBu_r"); cols = [("#555555" if l == 0 else cmap(0.5 + 0.5 * np.sign(l) * (0.45 + 0.55 * abs(l) / 1200))) for l in lv]
    cs = ax.contour(X * 100, Y * 100, V, levels=lv, colors=cols, linewidths=1.7); ax.clabel(cs, fmt="%d V", fontsize=8.5)
    ax.streamplot(X * 100, Y * 100, Ex, Ey, color="#9aa0aa", density=0.9, linewidth=0.7, arrowsize=0.8); ax.plot([-1], [0], "o", color=RED); ax.plot([1], [0], "o", color=NAVY)
    ax.set_aspect("equal"); ax.set_xlim(-4, 4); ax.set_ylim(-4, 4); panel(ax, "x (cm)", "y (cm)")
    fig.tight_layout(); idx = np.s_[::16, ::16]
    return dict(x_m=X[idx].ravel(), y_m=Y[idx].ravel(), V_volt=V[idx].ravel()), fig

@figure(C, "p2-c4-sphere-potential", "c4", "Potential of a charged sphere: point charge, insulating ball, conductor",
        "$Q=10\\,\\mathrm{nC}$, $R=5\\,\\mathrm{cm}$. Outside, $V=kQ/r$ for all three. A conductor is an equipotential ($kQ/R=1800\\,\\mathrm{V}$); inside a uniform ball $V=\\frac{kQ}{2R}\\left(3-r^2/R^2\\right)$, reaching $2700\\,\\mathrm{V}$ at the centre.",
        r"V(r)=-\int_\infty^rE\,dr,\qquad V_{\rm ball}(0)=\tfrac32\,\frac{kQ}{R}")
def _():
    Q, R = 10e-9, 0.05; r = np.linspace(0.002, 0.20, 397); Vpt = K_E * Q / r
    Vb = np.where(r < R, K_E * Q / (2 * R) * (3 - r ** 2 / R ** 2), K_E * Q / r); Vc = np.where(r < R, K_E * Q / R, K_E * Q / r)
    Eb = np.where(r < R, K_E * Q * r / R ** 3, K_E * Q / r ** 2); Vnum = -cumtrap(Eb[::-1], r[::-1])[::-1] * -1                                        # V(r) = integral of E from r to the largest radius + V(rmax)
    Vnum = np.array([trap(Eb[i:], r[i:]) for i in range(len(r))]) + K_E * Q / r[-1]; close(Vnum, Vb, rel=2e-3, what="V = -integral of E dr")
    close(Vb[0], 1.5 * K_E * Q / R, rel=0.01, what="centre of the ball")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(r * 100, Vpt, color=GREY, ls=":", label="point charge kQ/r"); ax.plot(r * 100, Vb, color=NAVY, label="uniformly charged ball"); ax.plot(r * 100, Vc, color=RED, ls="--", label="conducting sphere")
    ax.axvline(R * 100, color=GREY, ls=":"); ax.set_ylim(0, 4000); panel(ax, "distance r from the centre (cm)", "V (volts)", legend=True)
    fig.tight_layout()
    return dict(r_m=r, V_point_V=Vpt, V_ball_V=Vb, V_conductor_V=Vc), fig

@figure(C, "p2-c4-ring-disk", "c4", "Potential on the axis of a ring and of a disk",
        "Both have the same total charge ($5\\,\\mathrm{nC}$) and radius ($6\\,\\mathrm{cm}$). The ring: $V=kQ/\\sqrt{z^2+R^2}$. The disk: $V=\\frac{\\sigma}{2\\varepsilon_0}\\left(\\sqrt{z^2+R^2}-z\\right)$. Far away both tend to $kQ/z$; $E_z=-dV/dz$.",
        r"V_{\rm ring}=\frac{kQ}{\sqrt{z^2+R^2}},\qquad V_{\rm disk}=\frac{\sigma}{2\varepsilon_0}\left(\sqrt{z^2+R^2}-z\right)")
def _():
    Q, R = 5e-9, 0.06; sg = Q / (np.pi * R ** 2); z = np.linspace(0, 0.30, 301); Vr = K_E * Q / np.sqrt(z ** 2 + R ** 2); Vd = sg / (2 * EPS0) * (np.sqrt(z ** 2 + R ** 2) - z)
    rr = (np.arange(4000) + 0.5) * R / 4000; Vnum = np.array([np.sum(K_E * sg * 2 * np.pi * rr * (R / 4000) / np.sqrt(rr ** 2 + zz ** 2)) for zz in z]); close(Vnum, Vd, rel=5e-4, what="disk potential by summing rings (k and 1/4 pi eps0 agree to 2e-4)")
    Ez = -np.gradient(Vr, z, edge_order=2); close(Ez[5:-5], K_E * Q * z[5:-5] / (z[5:-5] ** 2 + R ** 2) ** 1.5, rel=2e-3, atol=1.0, what="E = -dV/dz for the ring")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(z * 100, Vr, color=NAVY, label="ring"); ax.plot(z * 100, Vd, color=RED, label="disk"); ax.plot(z[5:] * 100, K_E * Q / z[5:], color=GREY, ls=":", label="point charge kQ/z"); ax.set_ylim(0, 1500)
    panel(ax, "distance z along the axis (cm)", "V (volts)", legend=True)
    fig.tight_layout()
    return dict(z_m=z, V_ring_V=Vr, V_disk_V=Vd), fig

@figure(C, "p2-c4-energy", "c4", "Electric potential energy of two point charges",
        "For $q_1q_2>0$ (repulsion) $U$ is positive and falls to zero at infinity; for $q_1q_2<0$ (attraction) it is negative: $-U$ is the energy needed to separate the pair. Here $|q_1q_2|=2\\times10^{-12}\\,\\mathrm{C^2}$.",
        r"U=k\frac{q_1q_2}{r},\qquad F=-\frac{dU}{dr}")
def _():
    r = np.linspace(0.02, 0.50, 241); Ur = K_E * 2e-12 / r; Ua = -Ur; F = -np.gradient(Ur, r, edge_order=2)
    close(F[r > 0.05], K_E * 2e-12 / r[r > 0.05] ** 2, rel=3e-3, what="F = -dU/dr (r > 5 cm, where the finite-difference step is small)"); close(Ur[r > 0.4][-1] * 0 + Ur[-1], K_E * 2e-12 / 0.5, what="value at 0.5 m")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(r * 100, Ur * 1e3, color=RED, label="like charges (repulsion)"); ax.plot(r * 100, Ua * 1e3, color=NAVY, label="opposite charges (attraction)"); ax.axhline(0, color=GREY, lw=1)
    panel(ax, "separation r (cm)", "potential energy U (mJ)", legend=True); ax.set_ylim(-1.0, 1.0)
    fig.tight_layout()
    return dict(r_m=r, U_like_J=Ur, U_unlike_J=Ua), fig

# =============================================================================================== chapter 5: magnetic force
@figure(C, "p2-c5-circles", "c5", "Charged particles in a uniform magnetic field",
        "$B=0.05\\,\\mathrm{T}$ into the page, both particles at $10^5\\,\\mathrm{m/s}$: a proton goes round a circle of radius $mv/(eB)=2.1\\,\\mathrm{cm}$; an alpha particle (twice the charge, four times the mass) a circle twice as big, in the same sense. The period $2\\pi m/(qB)$ does not depend on the speed.",
        r"r=\frac{mv}{|q|B},\qquad T=\frac{2\pi m}{|q|B},\qquad f=\frac{|q|B}{2\pi m}")
def _():
    B, v = 0.05, 1e5; m_a, q_a = 4 * M_P, 2 * E_CH; rp, ra = M_P * v / (E_CH * B), m_a * v / (q_a * B); close(ra / rp, 2.0, rel=1e-9, what="alpha radius = 2 x proton radius")
    close(2 * np.pi * rp / v, 2 * np.pi * M_P / (E_CH * B), rel=1e-9, what="period independent of speed"); close(rp, 0.0209, rel=5e-3, what="proton radius")
    s = np.linspace(0, 2 * np.pi, 361)
    xp, yp = rp * np.cos(s) , rp * np.sin(s) - rp; xa, ya = ra * np.cos(s), ra * np.sin(s) - ra               # both start at the origin moving in +x, centre below (positive charge, B into the page)
    fig, ax = plt.subplots(figsize=(6.2, 5.2)); ax.plot(xp * 100, yp * 100, color=NAVY, label="proton  r = %.1f cm" % (rp * 100)); ax.plot(xa * 100, ya * 100, color=RED, label="alpha particle  r = %.1f cm" % (ra * 100)); ax.plot([0], [0], "ko")
    gx, gy = np.meshgrid(np.arange(-4, 4.1, 2.0), np.arange(-8, 1.1, 2.0)); ax.scatter(gx.ravel(), gy.ravel(), marker="x", color="#b8bcc6", s=26, zorder=0); ax.text(0.97, 0.96, "× B into the page", transform=ax.transAxes, ha="right", va="top", color=GREY)
    ax.annotate("", xy=(1.3, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="k")); ax.set_aspect("equal"); panel(ax, "x (cm)", "y (cm)", legend=True)
    fig.tight_layout()
    return dict(x_proton_m=xp, y_proton_m=yp, x_alpha_m=xa, y_alpha_m=ya), fig

@figure(C, "p2-c5-helix", "c5", "Helical motion: velocity components along and across the field",
        "An electron with $v_\\perp=3\\times10^6\\,\\mathrm{m/s}$ and $v_\\parallel=1\\times10^6\\,\\mathrm{m/s}$ in $B=2\\,\\mathrm{mT}$: a circle of radius $r=mv_\\perp/(eB)$ in the plane perpendicular to $\\vec B$ combined with uniform motion along $\\vec B$; the pitch is $p=v_\\parallel T$.",
        r"r=\frac{mv_\perp}{eB},\qquad p=v_\parallel T=\frac{2\pi mv_\parallel}{eB}")
def _():
    B, vp, vl = 2e-3, 3e6, 1e6; r = M_E * vp / (E_CH * B); T = 2 * np.pi * M_E / (E_CH * B); pitch = vl * T; t = np.linspace(0, 3 * T, 601); w = 2 * np.pi / T
    x, y, z = r * np.cos(w * t), r * np.sin(w * t), vl * t; close(z[200] - z[0], pitch, rel=1e-9, what="pitch"); close(np.hypot(x, y), r, rel=1e-9, what="constant radius")
    fig = plt.figure(figsize=(6.6, 5.0)); ax = fig.add_subplot(111, projection="3d"); ax.plot(x * 1e3, y * 1e3, z * 1e3, color=NAVY, lw=1.8)
    ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)"); ax.text2D(0.01, 0.52, "z, along B (mm)", transform=ax.transAxes, rotation=90, va="center"); ax.set_title("r = %.1f mm,  pitch = %.1f mm" % (r * 1e3, pitch * 1e3), fontsize=10); ax.view_init(elev=18, azim=-55)
    fig.subplots_adjust(left=0.02, right=0.86, bottom=0.04, top=0.95)
    return dict(t_s=t, x_m=x, y_m=y, z_m=z), fig

@figure(C, "p2-c5-hall", "c5", "Hall voltage against the magnetic field",
        "A strip $0.5\\,\\mathrm{mm}$ thick carrying $10\\,\\mathrm{A}$: $V_H=IB/(net)$ is linear in $B$, and tiny for a metal (copper) but thousands of times larger for a semiconductor with few carriers; that is why Hall probes use semiconductors.",
        r"V_H=\frac{IB}{n\,e\,t}")
def _():
    I, t = 10.0, 0.5e-3; B = np.linspace(0, 1.0, 41); ncu, nsi = 8.5e28, 1.0e22; Vcu = I * B / (ncu * E_CH * t); Vsi = I * B / (nsi * E_CH * t)
    close(Vcu[20] , 7.34e-7, rel=1e-2, what="copper at 0.5 T"); close(np.polyfit(B, Vsi, 1)[0], I / (nsi * E_CH * t), rel=1e-9, what="slope")
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8)); ax[0].plot(B, Vcu * 1e6, color=NAVY); panel(ax[0], "B (T)", "V_H (μV)", "copper  (n = 8.5×10²⁸ m⁻³)"); ax[1].plot(B, Vsi, color=RED); panel(ax[1], "B (T)", "V_H (V)", "semiconductor  (n = 10²² m⁻³)")
    fig.tight_layout()
    return dict(B_T=B, V_Hall_copper_V=Vcu, V_Hall_semiconductor_V=Vsi), fig

@figure(C, "p2-c5-loop-torque", "c5", "Torque and potential energy of a current loop in a field",
        "A coil with $\\mu=NIA=2\\,\\mathrm{A\\,m^2}$ in $B=0.30\\,\\mathrm{T}$: the torque $\\tau=\\mu B\\sin\\phi$ is largest ($0.6\\,\\mathrm{N\\,m}$) when the plane is parallel to $\\vec B$; the potential energy $U=-\\mu B\\cos\\phi$ is lowest when $\\vec\\mu\\parallel\\vec B$ (the torque is the slope of $U$, $\\tau=dU/d\\phi$).",
        r"\vec\tau=\vec\mu\times\vec B,\qquad U=-\vec\mu\cdot\vec B,\qquad \mu=NIA")
def _():
    mu, B = 2.0, 0.30; phi = np.linspace(0, 180, 181); r = np.radians(phi); tau = mu * B * np.sin(r); U = -mu * B * np.cos(r)
    close(tau, np.gradient(U, r, edge_order=2), atol=1e-4, what="torque magnitude = dU/dphi (central difference, 1 degree step)"); close(tau.max(), 0.6, rel=1e-9, what="maximum torque")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(phi, tau, color=NAVY, label="torque τ (N m)"); ax.plot(phi, U, color=RED, label="potential energy U (J)"); ax.axhline(0, color=GREY, lw=1)
    ax.set_xticks(range(0, 181, 30)); panel(ax, "angle φ between μ and B (degrees)", "", legend=True)
    fig.tight_layout()
    return dict(phi_deg=phi, torque_Nm=tau, U_J=U), fig

# =============================================================================================== chapter 6: magnetic fields of currents
@figure(C, "p2-c6-wire", "c6", "Magnetic field inside and outside a long straight wire",
        "$I=10\\,\\mathrm{A}$ spread uniformly over a wire of radius $2\\,\\mathrm{mm}$: inside $B=\\mu_0Ir/(2\\pi R^2)$ rises linearly, outside $B=\\mu_0I/(2\\pi r)$ falls as $1/r$; the peak $1\\,\\mathrm{mT}$ is at the surface.",
        r"\oint\vec B\cdot d\vec\ell=\mu_0I_{\rm enc}\ \Rightarrow\ B=\frac{\mu_0I}{2\pi r}\ (r>R)")
def _():
    I, R = 10.0, 2e-3; r = np.linspace(1e-4, 0.01, 400); B = np.where(r < R, MU0 * I * r / (2 * np.pi * R ** 2), MU0 * I / (2 * np.pi * r)); close(MU0 * I / (2 * np.pi * R), 1.0e-3, rel=1e-9, what="1 mT at the surface")
    close(B * 2 * np.pi * r, MU0 * I * np.minimum(1.0, (r / R) ** 2), rel=1e-9, what="Ampere's law")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(r * 1e3, B * 1e3, color=NAVY); ax.axvline(R * 1e3, color=GREY, ls=":"); ax.annotate("wire surface", (R * 1e3 + 0.1, 0.12), color=GREY); panel(ax, "distance r from the axis (mm)", "B (mT)")
    fig.tight_layout()
    return dict(r_m=r, B_T=B), fig

@figure(C, "p2-c6-helmholtz", "c6", "A single loop against a Helmholtz pair",
        "Two identical loops of radius $R$ a distance $R$ apart give an almost uniform field near the centre: the first and second derivatives of $B$ vanish there, so the variation within $\\pm0.2R$ is under $0.5\\,\\%$ (a single loop varies by about $10\\,\\%$).",
        r"B_{\rm loop}(z)=\frac{\mu_0IR^2}{2(R^2+z^2)^{3/2}},\qquad B_{\rm pair}=B_{\rm loop}(z-\tfrac R2)+B_{\rm loop}(z+\tfrac R2)")
def _():
    R, I = 0.10, 1.0; z = np.linspace(-0.25, 0.25, 501); L = lambda zz: MU0 * I * R ** 2 / (2 * (R ** 2 + zz ** 2) ** 1.5); single = L(z); pair = L(z - R / 2) + L(z + R / 2)
    c = len(z) // 2; d2 = (pair[c + 1] - 2 * pair[c] + pair[c - 1]) / (z[1] - z[0]) ** 2; close(d2, 0.0, atol=2e-3 * abs(pair[c]) / R ** 2, what="B'' = 0 at the centre of the pair")
    within = np.abs(z) <= 0.2 * R; assert (pair[within].max() - pair[within].min()) / pair[c] < 0.005 and (single[within].max() - single[within].min()) / single[c] > 0.05
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(z / R, single * 1e6, color=NAVY, label="single loop"); ax.plot(z / R, pair * 1e6, color=RED, label="Helmholtz pair (separation R)"); panel(ax, "position z along the axis (in units of R)", "B (μT)  for I = 1 A, R = 10 cm", legend=True)
    fig.tight_layout()
    return dict(z_over_R=z / R, B_single_T=single, B_pair_T=pair), fig

@figure(C, "p2-c6-solenoid", "c6", "Field on the axis of a finite solenoid",
        "$n=2000$ turns per metre, $I=1.5\\,\\mathrm{A}$, length $0.30\\,\\mathrm{m}$, radius $2\\,\\mathrm{cm}$. In the middle $B\\approx\\mu_0nI=3.77\\,\\mathrm{mT}$ (the ideal value); at each end it falls to about half of that.",
        r"B=\frac{\mu_0nI}{2}\left(\cos\theta_1-\cos\theta_2\right),\qquad B_{\rm ideal}=\mu_0nI")
def _():
    n, I, L, R = 2000.0, 1.5, 0.30, 0.02; z = np.linspace(-0.30, 0.30, 601); Bid = MU0 * n * I
    B = Bid / 2 * ((z + L / 2) / np.hypot(z + L / 2, R) - (z - L / 2) / np.hypot(z - L / 2, R))
    N = 3000; zs = (np.arange(N) + 0.5) * L / N - L / 2; Bnum = np.array([np.sum(MU0 * (n * L / N) * I * R ** 2 / (2 * (R ** 2 + (zz - zs) ** 2) ** 1.5)) for zz in z]); close(Bnum, B, rel=1e-4, what="sum over turns")
    close(B[300] / Bid, 1.0, atol=0.01, what="centre = ideal"); close(B[np.argmin(np.abs(z - L / 2))] / Bid, 0.5, atol=0.01, what="end = half")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(z * 100, B * 1e3, color=NAVY, label="finite solenoid"); ax.axhline(Bid * 1e3, color=GREY, ls="--", label="ideal μ₀nI"); ax.axvspan(-15, 15, color=ORANGE, alpha=0.08)
    panel(ax, "position z along the axis (cm)", "B (mT)", legend=True); ax.set_ylim(0, 4.4)
    fig.tight_layout()
    return dict(z_m=z, B_T=B), fig

@figure(C, "p2-c6-parallel-wires", "c6", "Force between parallel currents",
        "$F/L=\\mu_0I_1I_2/(2\\pi d)$: inversely proportional to the separation (slope $-1$ on log-log axes) and proportional to the product of the currents; $1.0\\times10^{-3}\\,\\mathrm{N/m}$ for $10\\,\\mathrm{A}$ and $10\\,\\mathrm{A}$ at $2\\,\\mathrm{cm}$. Parallel currents attract.",
        r"\frac FL=\frac{\mu_0I_1I_2}{2\pi d}")
def _():
    d = np.logspace(-2, 0, 41); f1 = MU0 * 10 * 10 / (2 * np.pi * d); f2 = MU0 * 10 * 30 / (2 * np.pi * d); close(np.polyfit(np.log10(d), np.log10(f1), 1)[0], -1.0, atol=1e-9, what="slope -1"); close(MU0 * 100 / (2 * np.pi * 0.02), 1.0e-3, rel=1e-9, what="1 mN/m")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.loglog(d * 100, f1, color=NAVY, label="10 A and 10 A"); ax.loglog(d * 100, f2, color=RED, label="10 A and 30 A"); ax.plot([2], [1.0e-3], "o", color=GREEN); ax.annotate("2 cm: 1.0 mN/m", (2.4, 1.25e-3), color=GREEN)
    panel(ax, "separation d (cm)", "force per unit length F/L (N/m)", legend=True)
    fig.tight_layout()
    return dict(d_m=d, F_per_L_10A_10A_Nm=f1, F_per_L_10A_30A_Nm=f2), fig

# =============================================================================================== chapter 7: induction and inductance
@figure(C, "p2-c7-faraday", "c7", "Faraday's law: flux and induced emf",
        "A coil of $N=200$ turns in a field whose flux through one turn is $\\Phi=\\Phi_0\\sin\\omega t$ ($\\Phi_0=2\\,\\mathrm{mWb}$, $f=50\\,\\mathrm{Hz}$). The emf $-N\\,d\\Phi/dt$ is a cosine: largest when the flux is zero and zero when the flux is at its peak; its amplitude is $N\\omega\\Phi_0=126\\,\\mathrm{V}$.",
        r"\varepsilon=-N\frac{d\Phi}{dt}")
def _():
    N, P0, f = 200, 2e-3, 50.0; w = 2 * np.pi * f; t = np.linspace(0, 0.04, 801); Phi = P0 * np.sin(w * t); emf = -N * P0 * w * np.cos(w * t)
    close(emf, -N * np.gradient(Phi, t, edge_order=2), rel=1e-3, atol=0.5, what="emf = -N dPhi/dt"); close(np.abs(emf).max(), N * w * P0, rel=1e-6, what="amplitude")
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(7.2, 5.4)); ax[0].plot(t * 1e3, Phi * 1e3, color=NAVY); panel(ax[0], "", "flux through one turn (mWb)")
    ax[1].plot(t * 1e3, emf, color=RED); ax[1].axhline(0, color=GREY, lw=1); panel(ax[1], "t (ms)", "induced emf (V)")
    fig.tight_layout()
    return dict(t_s=t, flux_Wb=Phi, emf_V=emf), fig

@figure(C, "p2-c7-rl", "c7", "Growth and decay of the current in an RL circuit",
        "$\\varepsilon=12\\,\\mathrm{V}$, $R=24\\,\\Omega$, $L=0.60\\,\\mathrm{H}$: $\\tau=L/R=25\\,\\mathrm{ms}$. The current reaches $63\\,\\%$ of $\\varepsilon/R=0.5\\,\\mathrm{A}$ at $t=\\tau$ and is $37\\,\\%$ of its initial value one time constant after the battery is removed. The stored energy is $\\tfrac12LI^2$.",
        r"I=\frac{\varepsilon}{R}\left(1-e^{-t/\tau}\right),\qquad I=I_0e^{-t/\tau},\qquad \tau=\frac LR")
def _():
    eps, R, L = 12.0, 24.0, 0.60; tau = L / R; t = np.linspace(0, 0.15, 301); Ig = eps / R * (1 - np.exp(-t / tau)); Id = eps / R * np.exp(-t / tau)
    sol = solve_ivp(lambda tt, y: [(eps - R * y[0]) / L], (0, 0.15), [0.0], t_eval=t, rtol=1e-10, atol=1e-12); close(sol.y[0], Ig, rel=1e-6, atol=1e-8, what="ODE = analytic growth")
    close(np.interp(tau, t, Ig), 0.5 * (1 - np.exp(-1)), rel=1e-3, what="I(tau) = 0.316 A"); U = 0.5 * L * Ig ** 2; close(U[-1], 0.5 * L * (eps / R) ** 2, rel=2e-2, what="energy at the end")
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8)); ax[0].plot(t * 1e3, Ig, color=NAVY, label="growth"); ax[0].plot(t * 1e3, Id, color=RED, label="decay"); ax[0].axvline(tau * 1e3, color=GREY, ls=":"); ax[0].annotate("τ = 25 ms", (tau * 1e3 + 3, 0.05), color=GREY); panel(ax[0], "t (ms)", "I (A)", legend=True)
    ax[1].plot(t * 1e3, U * 1e3, color=GREEN); panel(ax[1], "t (ms)", "energy stored ½LI² (mJ)")
    fig.tight_layout()
    return dict(t_s=t, I_growth_A=Ig, I_decay_A=Id, U_growth_J=U), fig

@figure(C, "p2-c7-braking", "c7", "Motional emf: a sliding rod is braked by its own induced current",
        "A rod ($m=0.10\\,\\mathrm{kg}$, $l=0.40\\,\\mathrm{m}$) slides on rails closed through $R=0.30\\,\\Omega$ in $B=0.50\\,\\mathrm{T}$ with initial speed $6\\,\\mathrm{m/s}$. The magnetic force $B^2l^2v/R$ opposes the motion: $v=v_0e^{-t/\\tau}$ with $\\tau=mR/(B^2l^2)=0.75\\,\\mathrm{s}$; all the initial kinetic energy ends as heat in $R$.",
        r"\varepsilon=Blv,\quad m\frac{dv}{dt}=-\frac{B^2l^2}{R}v,\quad \tau=\frac{mR}{B^2l^2}")
def _():
    m, l, B, R, v0 = 0.10, 0.40, 0.50, 0.30, 6.0; tau = m * R / (B * l) ** 2; t = np.linspace(0, 4, 801); v = v0 * np.exp(-t / tau)
    sol = solve_ivp(lambda tt, y: [-(B * l) ** 2 / (m * R) * y[0]], (0, 4), [v0], t_eval=t, rtol=1e-10, atol=1e-12); close(sol.y[0], v, rel=1e-6, atol=1e-8, what="ODE = analytic")
    I = B * l * v / R; Pq = I ** 2 * R; heat = trap(Pq, t); close(heat, 0.5 * m * v0 ** 2, rel=2e-3, what="heat dissipated = initial kinetic energy"); close(tau, 0.75, rel=1e-9, what="time constant")
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8)); ax[0].plot(t, v, color=NAVY); ax[0].axvline(tau, color=GREY, ls=":"); ax[0].annotate("τ = 0.75 s", (tau + 0.1, 4.5), color=GREY); panel(ax[0], "t (s)", "rod speed v (m/s)")
    ax[1].plot(t, I, color=RED); panel(ax[1], "t (s)", "induced current I (A)")
    fig.tight_layout()
    return dict(t_s=t, v_ms=v, I_A=I, power_W=Pq), fig

@figure(C, "p2-c7-inductor-energy", "c7", "Energy stored in an inductor",
        "$U=\\tfrac12LI^2$ grows with the square of the current and in proportion to the inductance. The same coil that stores $0.075\\,\\mathrm{J}$ at $0.5\\,\\mathrm{A}$ ($L=0.6\\,\\mathrm{H}$) stores four times as much at $1\\,\\mathrm{A}$.",
        r"U=\tfrac12LI^2=\int_0^I Li\,di")
def _():
    I = np.linspace(0, 2, 81); data = {"I_A": I}; fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for L, col in ((0.2, GREEN), (0.6, NAVY), (1.2, RED)):
        U = 0.5 * L * I ** 2; close(U, [trap(L * I[:i + 1], I[:i + 1]) for i in range(len(I))], rel=1e-9, atol=1e-12, what="U = integral of L i di"); ax.plot(I, U, color=col, label="L = %.1f H" % L); data["U_L%.1fH_J" % L] = U
    close(0.5 * 0.6 * 0.5 ** 2, 0.075, what="0.075 J"); ax.plot([0.5], [0.075], "ko"); panel(ax, "current I (A)", "stored energy U (J)", legend=True)
    fig.tight_layout()
    return data, fig

@figure(C, "p2-c7-induced-e", "c7", "Induced electric field of a changing solenoid field",
        "$R=5\\,\\mathrm{cm}$, $dB/dt=0.020\\,\\mathrm{T/s}$: inside the solenoid $E=\\tfrac r2\\,dB/dt$ grows linearly ($3.0\\times10^{-4}\\,\\mathrm{V/m}$ at $3\\,\\mathrm{cm}$); outside it falls as $R^2/(2r)\\,dB/dt$ ($2.5\\times10^{-4}\\,\\mathrm{V/m}$ at $10\\,\\mathrm{cm}$), although $B=0$ there.",
        r"E\,(2\pi r)=\pi r_{\rm eff}^2\,\frac{dB}{dt}")
def _():
    R, dB = 0.05, 0.020; r = np.linspace(0.001, 0.15, 300); E = np.where(r < R, r / 2 * dB, R ** 2 / (2 * r) * dB)
    close(np.interp(0.03, r, E), 3.0e-4, rel=2e-3, what="E at 3 cm"); close(np.interp(0.10, r, E), 2.5e-4, rel=2e-3, what="E at 10 cm"); close(E * 2 * np.pi * r, np.pi * np.minimum(r, R) ** 2 * dB, rel=1e-9, what="Faraday's law around the circle")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(r * 100, E * 1e4, color=NAVY); ax.axvline(R * 100, color=GREY, ls=":"); ax.annotate("solenoid radius", (R * 100 + 0.4, 0.4), color=GREY); panel(ax, "distance r from the axis (cm)", "induced E (10⁻⁴ V/m)")
    fig.tight_layout()
    return dict(r_m=r, E_Vm=E), fig

# =============================================================================================== chapter 8: nature and propagation of light
@figure(C, "p2-c8-em-wave", "c8", "A plane electromagnetic wave",
        "$\\vec E$ and $\\vec B$ are perpendicular to each other and to the direction of travel, and they are in phase; their amplitudes are tied by $E_0=cB_0$. With $E_0=150\\,\\mathrm{V/m}$ the magnetic amplitude is $5.0\\times10^{-7}\\,\\mathrm{T}$.",
        r"E=cB,\qquad c=\frac1{\sqrt{\mu_0\varepsilon_0}},\qquad v=f\lambda")
def _():
    E0 = 150.0; B0 = E0 / C_L; lam = 1.0; k = 2 * np.pi / lam; x = np.linspace(0, 2 * lam, 401); E = E0 * np.sin(k * x); Bz = B0 * np.sin(k * x)
    close(1 / np.sqrt(MU0 * EPS0), C_L, rel=2e-3, what="c = 1/sqrt(mu0 eps0)"); close(E[Bz != 0] / Bz[Bz != 0], C_L, rel=1e-9, what="E/B = c")
    fig, ax = plt.subplots(figsize=(7.4, 4.0)); ax.plot(x, E, color=NAVY, label="E (V/m), along y"); ax.set_xlabel("x / λ"); ax.set_ylabel("E (V/m)", color=NAVY); ax2 = ax.twinx(); ax2.plot(x, Bz * 1e7, color=RED, ls="--", label="B (10⁻⁷ T), along z"); ax2.set_ylabel("B (10⁻⁷ T)", color=RED); ax2.grid(False); ax2.spines["right"].set_visible(True)
    ax.set_title("travelling along +x", loc="left"); fig.tight_layout()
    return dict(x_over_lambda=x / lam, E_Vm=E, B_T=Bz), fig

@figure(C, "p2-c8-snell", "c8", "Refraction and total internal reflection",
        "Air to glass ($n=1.5$): the ray bends towards the normal; $40^\\circ$ becomes $25.4^\\circ$. Glass to air: the ray bends away, and beyond the critical angle $\\theta_c=\\sin^{-1}(1/1.5)=41.8^\\circ$ there is no refracted ray (total internal reflection).",
        r"n_1\sin\theta_1=n_2\sin\theta_2,\qquad \sin\theta_c=\frac{n_2}{n_1}")
def _():
    th = np.linspace(0, 89.9, 400); r = np.radians(th); a2g = np.degrees(np.arcsin(np.sin(r) / 1.5)); sg = 1.5 * np.sin(r); g2a = np.where(sg <= 1, np.degrees(np.arcsin(np.minimum(sg, 1.0))), np.nan)
    tc = np.degrees(np.arcsin(1 / 1.5)); close(tc, 41.81, rel=1e-3, what="critical angle"); close(np.interp(40, th, a2g), 25.37, rel=2e-3, what="40 degrees in air -> glass")
    ok = ~np.isnan(g2a); close(1.5 * np.sin(r[ok]), np.sin(np.radians(g2a[ok])), rel=1e-9, what="Snell's law glass to air")
    fig, ax = plt.subplots(figsize=(7.2, 4.1)); ax.plot(th, a2g, color=NAVY, label="air → glass  (n = 1.5)"); ax.plot(th[ok], g2a[ok], color=RED, label="glass → air"); ax.plot(th, th, color=GREY, ls=":", lw=1)
    ax.axvspan(tc, 90, color=RED, alpha=0.08); ax.annotate("total internal reflection\n(θ > θc = 41.8°)", (50, 12), color=RED); ax.set_xlim(0, 90); ax.set_ylim(0, 92); panel(ax, "angle of incidence (degrees)", "angle of refraction (degrees)", legend=True)
    fig.tight_layout()
    return dict(incidence_deg=th, refraction_air_to_glass_deg=a2g, refraction_glass_to_air_deg=np.where(ok, g2a, 90.0)), fig

@figure(C, "p2-c8-malus", "c8", "Polarizers: Malus's law and the middle polarizer",
        "Left: unpolarized light through one polarizer gives $I_0/2$; a second polarizer at angle $\\theta$ gives $\\tfrac12I_0\\cos^2\\theta$. Right: crossed polarizers pass nothing, but a third one at $45^\\circ$ between them restores $I_0/8$: $I=\\tfrac18I_0\\sin^22\\theta$.",
        r"I=I_0\cos^2\theta,\qquad I_{\rm 3\ polarizers}=\tfrac12I_0\cos^2\theta\,\cos^2(90^\circ-\theta)")
def _():
    th = np.linspace(0, 180, 361); r = np.radians(th); two = 0.5 * np.cos(r) ** 2; three = 0.5 * np.cos(r) ** 2 * np.cos(np.pi / 2 - r) ** 2
    close(three, np.sin(2 * r) ** 2 / 8, atol=1e-12, what="1/8 sin^2(2 theta)"); close(three.max(), 0.125, rel=1e-9, what="maximum I0/8 at 45 degrees"); close(th[np.argmax(three[:181])], 45.0, atol=0.5, what="maximum at 45 degrees")
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8)); ax[0].plot(th, two, color=NAVY); ax[0].set_xticks(range(0, 181, 45)); panel(ax[0], "angle θ of the second polarizer (deg)", "I / I₀ (unpolarized input)")
    ax[1].plot(th, three, color=RED); ax[1].set_xticks(range(0, 181, 45)); panel(ax[1], "angle θ of the middle polarizer (deg)", "I / I₀  after three polarizers (0°, θ, 90°)")
    fig.tight_layout()
    return dict(theta_deg=th, I_two_polarizers=two, I_three_polarizers=three), fig

@figure(C, "p2-c8-dispersion", "c8", "Dispersion: refractive index and prism deviation against wavelength",
        "Glass bends short wavelengths more than long ones (Cauchy fit $n=A+B/\\lambda^2$ for crown glass). For a $60^\\circ$ prism the minimum deviation is $\\delta=2\\sin^{-1}(n\\sin30^\\circ)-60^\\circ$: about $39.4^\\circ$ for violet and $37.8^\\circ$ for red.",
        r"n(\lambda)=A+\frac{B}{\lambda^2},\qquad \delta_{\min}=2\sin^{-1}\!\Big(n\sin\tfrac{\alpha}{2}\Big)-\alpha")
def _():
    lam = np.linspace(400, 700, 61); A, Bc = 1.5046, 0.0042; n = A + Bc / (lam / 1000) ** 2; al = np.radians(60); d = np.degrees(2 * np.arcsin(n * np.sin(al / 2)) - al)
    close(n[np.argmin(np.abs(lam - 590))], 1.5168, atol=1.5e-3, what="n of crown glass near the sodium line"); assert np.all(np.diff(n) < 0) and np.all(np.diff(d) < 0)
    # entering ray at the minimum-deviation geometry: symmetric passage, angle inside = alpha/2, so Snell's law at the first face recovers n
    th_in = np.arcsin(n * np.sin(al / 2)); close(np.sin(th_in) / np.sin(al / 2), n, rel=1e-12, what="Snell's law at the first face")
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8)); ax[0].plot(lam, n, color=NAVY); panel(ax[0], "wavelength (nm)", "refractive index n"); ax[1].plot(lam, d, color=RED); panel(ax[1], "wavelength (nm)", "minimum deviation of a 60° prism (deg)")
    fig.tight_layout()
    return dict(wavelength_nm=lam, n=n, deviation_deg=d), fig

# =============================================================================================== chapter 9: geometric optics
@figure(C, "p2-c9-thin-lens", "c9", "Thin lens: image distance and magnification against object distance",
        "$f=10\\,\\mathrm{cm}$ converging lens. Object beyond $f$: a real inverted image ($s'>0$, $m<0$), at infinity when $s\\to f^+$ and at $2f$ when $s=2f$ (then $m=-1$). Object inside $f$: a virtual, upright, enlarged image ($s'<0$, $m>1$).",
        r"\frac1s+\frac1{s'}=\frac1f,\qquad m=-\frac{s'}{s}")
def _():
    f = 10.0; s1 = np.linspace(10.5, 60, 200); s2 = np.linspace(0.5, 9.5, 100); s = np.concatenate([s2, s1]); sp = s * f / (s - f); m = -sp / s
    close(1 / s + 1 / sp, 1 / f, rel=1e-12, what="lens equation"); close(sp[np.argmin(np.abs(s - 20))], 20.0, atol=0.2, what="s = 2f -> s' = 2f"); close(m[np.argmin(np.abs(s - 20))], -1.0, atol=0.02, what="m = -1 at 2f")
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax[0].plot(s2, s2 * f / (s2 - f), color=RED, label="virtual (s < f)"); ax[0].plot(s1, s1 * f / (s1 - f), color=NAVY, label="real (s > f)"); ax[0].axvline(f, color=GREY, ls=":"); ax[0].axhline(0, color=GREY, lw=1); ax[0].set_ylim(-30, 120); panel(ax[0], "object distance s (cm)", "image distance s' (cm)", legend=True)
    ax[1].plot(s2, -(s2 * f / (s2 - f)) / s2, color=RED); ax[1].plot(s1, -(s1 * f / (s1 - f)) / s1, color=NAVY); ax[1].axvline(f, color=GREY, ls=":"); ax[1].axhline(0, color=GREY, lw=1); ax[1].set_ylim(-6, 12); panel(ax[1], "object distance s (cm)", "magnification m")
    fig.tight_layout()
    return dict(s_cm=s, s_image_cm=sp, magnification=m), fig

@figure(C, "p2-c9-ray-diagram", "c9", "Ray diagram of a converging lens",
        "Object $3\\,\\mathrm{cm}$ high, $25\\,\\mathrm{cm}$ from a lens with $f=10\\,\\mathrm{cm}$. The three principal rays (parallel → through the far focus; through the centre → straight; through the near focus → parallel) meet at $s'=16.7\\,\\mathrm{cm}$ giving an inverted image $m=-0.67$ ($2\\,\\mathrm{cm}$ high).",
        r"s'=\frac{sf}{s-f}=16.7\ \mathrm{cm},\qquad m=-\frac{s'}{s}=-0.667")
def _():
    f, s, h = 10.0, 25.0, 3.0; sp = s * f / (s - f); m = -sp / s; hi = m * h; close(sp, 16.6667, rel=1e-4, what="image distance")
    # three principal rays: intersections computed from the ray geometry, not from the lens equation
    O = np.array([-s, h]); r1 = (np.array([0.0, h]), np.array([f, 0.0]))       # parallel ray hits the lens at height h, then goes through the far focus (f, 0)
    def line(P, Q): d = Q - P; return P, d / np.linalg.norm(d)
    P1, d1 = line(*r1); P2, d2 = line(O, np.array([0.0, 0.0]))                   # ray through the centre
    A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]]); tt = np.linalg.solve(A, P2 - P1); X = P1 + tt[0] * d1
    close(X, [sp, hi], rel=1e-9, atol=1e-9, what="rays meet at the image point from the lens equation")
    fig, ax = plt.subplots(figsize=(8.0, 3.9)); ax.axhline(0, color=GREY, lw=1); ax.plot([0, 0], [-4.5, 4.5], color=NAVY, lw=3); ax.annotate("", xy=(-s, h), xytext=(-s, 0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.5))
    ax.annotate("", xy=(sp, hi), xytext=(sp, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5))
    ax.plot([-s, 0, sp], [h, h, hi], color=ORANGE); ax.plot([-s, 0, sp], [h, 0, hi], color=PURPLE)                  # parallel ray and the ray through the centre
    sl = (0 - h) / (-f - (-s)); yl = h + sl * (0 - (-s)); ax.plot([-s, 0, sp + 5], [h, yl, yl], color=CYAN)
    ax.plot([-f, f], [0, 0], "k|", ms=12); ax.text(-f, -0.7, "F", ha="center"); ax.text(f, -0.7, "F", ha="center"); ax.set_xlim(-30, 25); ax.set_ylim(-5, 5); ax.set_aspect("equal"); panel(ax, "distance along the axis (cm)", "height (cm)")
    fig.tight_layout()
    return dict(quantity=np.array(["object distance s (cm)", "image distance s' (cm)", "magnification m", "object height (cm)", "image height (cm)"]), value=np.array([s, sp, m, h, hi])), fig

@figure(C, "p2-c9-mirror", "c9", "Spherical mirrors: image distance against object distance",
        "A concave mirror with $f=15\\,\\mathrm{cm}$ forms real images beyond $f$ (inverted) and virtual ones inside $f$; a convex mirror ($f=-15\\,\\mathrm{cm}$) always gives a virtual, upright, reduced image between the mirror and its focus.",
        r"\frac1s+\frac1{s'}=\frac1f=\frac2R,\qquad m=-\frac{s'}{s}")
def _():
    s = np.linspace(2, 80, 157); f1, f2 = 15.0, -15.0; ok1 = np.abs(s - f1) > 0.6; s1 = s[ok1]; sp1 = s1 * f1 / (s1 - f1); sp2 = s * f2 / (s - f2)
    close(1 / s1 + 1 / sp1, 1 / f1, rel=1e-12, what="mirror equation (concave)"); close(1 / s + 1 / sp2, 1 / f2, rel=1e-12, what="mirror equation (convex)"); assert np.all(sp2 < 0) and np.all(sp2 > f2) and np.all(-sp2 / s < 1)
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); lo = s1 < f1
    ax.plot(s1[lo], sp1[lo], color=RED, label="concave, object inside f (virtual)"); ax.plot(s1[~lo], sp1[~lo], color=NAVY, label="concave, object beyond f (real)"); ax.plot(s, sp2, color=GREEN, label="convex (virtual)")
    ax.axhline(0, color=GREY, lw=1); ax.axvline(15, color=GREY, ls=":"); ax.set_ylim(-40, 120); panel(ax, "object distance s (cm)", "image distance s' (cm)", legend=True)
    fig.tight_layout()
    return dict(s_cm=s, s_image_convex_cm=sp2, s_image_concave_cm=np.where(ok1, s * f1 / np.where(ok1, s - f1, 1.0), 0.0)), fig

@figure(C, "p2-c9-lensmaker", "c9", "Lensmaker's equation: focal length of a biconvex lens",
        "For a thin lens in air $1/f=(n-1)(1/R_1-1/R_2)$. Left: a symmetric biconvex lens with $n=1.5$ has $f=R$. Right: for $R_1=-R_2=20\\,\\mathrm{cm}$ a higher refractive index gives a shorter focal length.",
        r"\frac1f=(n-1)\left(\frac1{R_1}-\frac1{R_2}\right)")
def _():
    R = np.linspace(5, 40, 71); n = 1.5; f1 = 1 / ((n - 1) * (1 / R - 1 / (-R))); close(f1, R, rel=1e-12, what="f = R for n = 1.5")
    nn = np.linspace(1.3, 2.0, 71); f2 = 1 / ((nn - 1) * (2 / 20.0)); close(f2[np.argmin(np.abs(nn - 1.5))], 20.0, rel=1e-3, what="n = 1.5, R = 20 cm -> f = 20 cm")
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8)); ax[0].plot(R, f1, color=NAVY); panel(ax[0], "radius of curvature R (cm), n = 1.5", "focal length f (cm)"); ax[1].plot(nn, f2, color=RED); panel(ax[1], "refractive index n, R = 20 cm", "focal length f (cm)")
    fig.tight_layout()
    return dict(R_cm=R, f_cm_n1p5=f1), fig

# =============================================================================================== chapter 10: interference
@figure(C, "p2-c10-double-slit", "c10", "Double-slit interference pattern",
        "$d=0.20\\,\\mathrm{mm}$, $\\lambda=600\\,\\mathrm{nm}$, screen at $2.0\\,\\mathrm{m}$: bright fringes where $d\\sin\\theta=m\\lambda$, spaced by $\\Delta y=\\lambda L/d=6.0\\,\\mathrm{mm}$; between them the intensity falls to zero (ideal slits of negligible width).",
        r"I=I_0\cos^2\!\left(\frac{\pi d\sin\theta}{\lambda}\right),\qquad \Delta y=\frac{\lambda L}{d}")
def _():
    d, lam, L = 0.20e-3, 600e-9, 2.0; y = np.linspace(-0.033, 0.033, 3301); I = np.cos(np.pi * d * np.sin(np.arctan(y / L)) / lam) ** 2
    pk, _p = find_peaks(I, height=0.99); sp = np.diff(y[pk]); close(sp.mean(), lam * L / d, rel=2e-3, what="fringe spacing lambda L / d"); assert len(pk) == 11
    fig, ax = plt.subplots(figsize=(7.4, 3.9)); ax.plot(y * 1e3, I, color=NAVY); ax.fill_between(y * 1e3, 0, I, color=NAVY, alpha=0.12); ax.annotate("", xy=(6, 1.08), xytext=(0, 1.08), arrowprops=dict(arrowstyle="<->", color=RED)); ax.text(1.0, 1.12, "Δy = 6.0 mm", color=RED)
    ax.set_ylim(0, 1.25); panel(ax, "position y on the screen (mm)", "I / I₀")
    fig.tight_layout()
    return dict(y_m=y, intensity_rel=I), fig

@figure(C, "p2-c10-colours", "c10", "Fringe spacing depends on the wavelength",
        "The same double slit ($d=0.20\\,\\mathrm{mm}$, $L=2.0\\,\\mathrm{m}$) with red ($650\\,\\mathrm{nm}$), green ($530\\,\\mathrm{nm}$) and blue ($450\\,\\mathrm{nm}$) light: $\\Delta y=\\lambda L/d$, so red fringes are the widest and all colours coincide at the central maximum (white light gives a white centre and coloured edges).",
        r"y_m=\frac{m\lambda L}{d}")
def _():
    d, L = 0.20e-3, 2.0; y = np.linspace(-0.012, 0.012, 2401); data = {"y_m": y}; fig, ax = plt.subplots(figsize=(7.4, 4.0))
    for lam, col, nm in ((650e-9, RED, "red 650 nm"), (530e-9, GREEN, "green 530 nm"), (450e-9, NAVY, "blue 450 nm")):
        I = np.cos(np.pi * d * np.sin(np.arctan(y / L)) / lam) ** 2; pk, _p = find_peaks(I, height=0.99); close(np.diff(y[pk]).mean(), lam * L / d, rel=2e-3, what="spacing for " + nm); ax.plot(y * 1e3, I, color=col, label="%s  (Δy = %.1f mm)" % (nm, lam * L / d * 1e3)); data["I_%dnm" % round(lam * 1e9)] = I
    panel(ax, "position y on the screen (mm)", "I / I₀", legend=True); ax.set_ylim(0, 1.35); ax.legend(frameon=False, ncol=1, fontsize=9, loc="upper right")
    fig.tight_layout()
    return data, fig

@figure(C, "p2-c10-thin-film", "c10", "Anti-reflection coating: reflectance against film thickness",
        "A MgF$_2$ film ($n=1.38$) on glass ($n=1.50$) in air, light of $550\\,\\mathrm{nm}$. Both reflections invert the wave, so the two beams cancel (as far as their different amplitudes allow) when $2nt=(m+\\tfrac12)\\lambda$: the first minimum is at $t=\\lambda/4n=99.6\\,\\mathrm{nm}$, where the reflectance falls from $4\\,\\%$ (bare glass) to $1.4\\,\\%$.",
        r"2nt=\left(m+\tfrac12\right)\lambda\ \ (\text{minimum}),\qquad R=r_1^2+r_2^2+2r_1r_2\cos\delta,\ \ \delta=\frac{4\pi nt}{\lambda}")
def _():
    lam, nf, ng = 550.0, 1.38, 1.50; t = np.linspace(0, 400, 801); r1 = (1 - nf) / (1 + nf); r2 = (nf - ng) / (nf + ng); dlt = 4 * np.pi * nf * t / lam; R = r1 ** 2 + r2 ** 2 + 2 * r1 * r2 * np.cos(dlt)
    close(R[0], ((1 - ng) / (1 + ng)) ** 2, rel=2e-2, what="t = 0 is bare glass (4 %; the two-beam sum gives 4.06 %)"); close(t[np.argmin(R[:300])], lam / (4 * nf), atol=0.6, what="first minimum at lambda/(4 n)"); close(R.min(), (abs(r1) - abs(r2)) ** 2, rel=1e-4, what="minimum reflectance (grid step 0.5 nm)")
    fig, ax = plt.subplots(figsize=(7.4, 4.0)); ax.plot(t, R * 100, color=NAVY); ax.axhline(4.0, color=GREY, ls="--"); ax.annotate("bare glass 4 %", (250, 4.1), color=GREY); ax.plot([lam / (4 * nf)], [R.min() * 100], "o", color=RED); ax.annotate("t = 99.6 nm,  R = %.1f %%" % (R.min() * 100), (110, 0.7), color=RED)
    ax.set_ylim(0, 4.8); panel(ax, "film thickness t (nm)", "reflectance R (%)")
    fig.tight_layout()
    return dict(t_nm=t, reflectance_percent=R * 100), fig

@figure(C, "p2-c10-superposition", "c10", "Superposition of two waves: the phase difference decides the amplitude",
        "Two waves of amplitude $A$ with phase difference $\\varphi$ add to a wave of amplitude $2A|\\cos(\\varphi/2)|$: $2A$ when in phase, $\\sqrt2A$ for $\\varphi=90^\\circ$, zero when they are opposite ($\\varphi=180^\\circ$).",
        r"A\sin(kx)+A\sin(kx+\varphi)=2A\cos\tfrac\varphi2\,\sin\!\Big(kx+\tfrac\varphi2\Big)")
def _():
    x = np.linspace(0, 2 * np.pi, 400); data = {"kx_rad": x}; fig, ax = plt.subplots(3, 1, sharex=True, figsize=(7.2, 6.0))
    for a_, ph, col in zip(ax, (0.0, np.pi / 2, np.pi), (NAVY, ORANGE, RED)):
        y1 = np.sin(x); y2 = np.sin(x + ph); s = y1 + y2; close(s, 2 * np.cos(ph / 2) * np.sin(x + ph / 2), atol=1e-12, what="sum identity"); close(np.abs(s).max(), 2 * abs(np.cos(ph / 2)), atol=1e-3, what="amplitude")
        a_.plot(x, y1, color=GREY, lw=1.2); a_.plot(x, y2, color=GREY, lw=1.2, ls="--"); a_.plot(x, s, color=col, lw=2.2); a_.set_ylim(-2.3, 2.3); panel(a_, "", "φ = %d°" % round(np.degrees(ph))); data["sum_phi%d" % round(np.degrees(ph))] = s
    ax[2].set_xlabel("kx (rad)"); fig.tight_layout()
    return data, fig

# =============================================================================================== chapter 11: diffraction
@figure(C, "p2-c11-single-slit", "c11", "Single-slit diffraction",
        "$I=I_0\\,[\\sin\\beta/\\beta]^2$ with $\\beta=\\pi a\\sin\\theta/\\lambda$; minima at $a\\sin\\theta=m\\lambda$ ($m=\\pm1,\\pm2,\\dots$). A narrower slit gives a wider central maximum, whose full width is $2\\lambda/a$ in $\\sin\\theta$; the side maxima are only $4.7\\,\\%$ and $1.65\\,\\%$ of the central one.",
        r"I=I_0\left(\frac{\sin\beta}{\beta}\right)^2,\quad \beta=\frac{\pi a\sin\theta}{\lambda},\quad a\sin\theta=m\lambda\ (\text{minima})")
def _():
    s = np.linspace(-0.6, 0.6, 3001); data = {"sin_theta": s}; fig, ax = plt.subplots(figsize=(7.4, 4.0))
    for a_over_l, col in ((2, RED), (5, NAVY), (10, GREEN)):
        beta = np.pi * a_over_l * s; I = np.sinc(beta / np.pi) ** 2; ax.plot(s, I, color=col, label="a = %d λ" % a_over_l); data["I_a%dlambda" % a_over_l] = I
        z = np.array([m / a_over_l for m in (1, 2) if m / a_over_l < 0.6]); close(np.interp(z, s[s >= 0], I[s >= 0]), 0.0, atol=2e-3, what="zeros at sin(theta) = m lambda / a")
    b = np.linspace(0.01, 12, 200001); sc = np.sinc(b / np.pi) ** 2; pk, _p = find_peaks(sc); close(sc[pk[:2]], [0.04719, 0.01648], rel=2e-3, what="side maxima 4.7 % and 1.65 %")
    panel(ax, "sin θ", "I / I₀", legend=True)
    fig.tight_layout()
    return data, fig

@figure(C, "p2-c11-double-finite", "c11", "Double slit with slits of finite width: interference × diffraction",
        "$d=3a$: the narrow interference fringes ($\\cos^2$) sit under the single-slit envelope ($\\mathrm{sinc}^2$). The orders $m=\\pm3,\\pm6,\\dots$ fall exactly on the zeros of the envelope and are missing; 5 fringes fit in the central maximum.",
        r"I=I_0\cos^2\!\Big(\frac{\pi d\sin\theta}{\lambda}\Big)\left(\frac{\sin\beta}{\beta}\right)^2,\qquad \text{missing orders } m=n\frac da")
def _():
    a_l, d_l = 1.0, 3.0; s = np.linspace(-1.5, 1.5, 12001); env = np.sinc(a_l * s) ** 2; I = np.cos(np.pi * d_l * s) ** 2 * env
    for m in (-3, 3):
        close(I[np.argmin(np.abs(s - m / d_l))], 0.0, atol=1e-6, what="order %d is missing" % m)
    close(I[np.argmin(np.abs(s - 1 / d_l))], np.sinc(1 / 3.0) ** 2, rel=1e-3, what="order 1 follows the envelope")
    pk, _p = find_peaks(I, height=0.02); central = pk[np.abs(s[pk]) < 1.0 / a_l]; assert len(central) == 5, len(central)          # visible fringes (>2 % of I0) inside the central diffraction maximum
    fig, ax = plt.subplots(figsize=(7.4, 4.0)); ax.plot(s, I, color=NAVY, label="interference × diffraction"); ax.plot(s, env, color=RED, ls="--", label="single-slit envelope")
    for m in (-3, 3): ax.plot([m / d_l], [0], "o", mfc="white", mec=RED, ms=8, zorder=5); ax.annotate("order %+d\nmissing" % m, (m / d_l, 0.16), color=RED, fontsize=9, ha="center")
    panel(ax, "a sin θ / λ", "I / I₀", legend=True)
    fig.tight_layout()
    return dict(a_sin_theta_over_lambda=s, I_rel=I, envelope=env), fig

@figure(C, "p2-c11-grating", "c11", "Diffraction gratings: more slits, sharper maxima",
        "Intensity for $N=2$, $5$ and $20$ slits of the same spacing $d$. The principal maxima ($d\\sin\\theta=m\\lambda$) stay where they are but their width shrinks as $1/N$, and $N-2$ weak secondary maxima appear between them.",
        r"I=I_0\left[\frac{\sin(N\varphi)}{N\sin\varphi}\right]^2,\qquad \varphi=\frac{\pi d\sin\theta}{\lambda}")
def _():
    x = np.linspace(-1.5, 1.5, 6001); data = {"d_sin_theta_over_lambda": x}; fig, ax = plt.subplots(3, 1, sharex=True, figsize=(7.4, 6.0))
    for a_, N, col in zip(ax, (2, 5, 20), (NAVY, RED, GREEN)):
        ph = np.pi * x; den = np.sin(ph); den = np.where(np.abs(den) < 1e-9, 1e-9, den); I = (np.sin(N * ph) / (N * den)) ** 2; I[np.abs(np.sin(ph)) < 1e-9] = 1.0
        mid = (x > 0.02) & (x < 0.98); pk, _p = find_peaks(I[mid], height=1e-4)
        if N > 2: close(len(pk), N - 2, atol=0, what="N - 2 secondary maxima between principal maxima")
        for m in (-1, 0, 1): close(I[np.argmin(np.abs(x - m))], 1.0, atol=1e-3, what="principal maximum at integer order")
        a_.plot(x, I, color=col); a_.set_ylim(0, 1.1); panel(a_, "", "N = %d" % N); data["I_N%d" % N] = I
    ax[2].set_xlabel("d sin θ / λ"); fig.tight_layout()
    return data, fig

@figure(C, "p2-c11-airy", "c11", "Circular aperture: the Airy pattern and the Rayleigh criterion",
        "$I=I_0\\,[2J_1(x)/x]^2$ with $x=\\pi D\\sin\\theta/\\lambda$; the first dark ring is at $x=3.832$, i.e. $\\sin\\theta=1.22\\lambda/D$. Two equal incoherent sources that far apart are just resolved: the dip between their peaks is about $26\\,\\%$.",
        r"I=I_0\left[\frac{2J_1(x)}{x}\right]^2,\qquad \theta_{\min}\approx1.22\frac{\lambda}{D}")
def _():
    x = np.linspace(-12, 12, 4801); xs = np.where(np.abs(x) < 1e-12, 1e-12, x); I = (2 * special.j1(xs) / xs) ** 2; z1 = special.jn_zeros(1, 1)[0]; close(z1, 3.8317, rel=1e-4, what="first zero of J1"); close(z1 / np.pi, 1.2197, rel=1e-3, what="1.22")
    off = z1; I2 = (2 * special.j1(np.where(np.abs(x - off) < 1e-12, 1e-12, x - off)) / np.where(np.abs(x - off) < 1e-12, 1e-12, x - off)) ** 2; tot = I + I2
    mid = tot[np.argmin(np.abs(x - off / 2))]; close(mid, 0.735, atol=0.01, what="Rayleigh dip: the midpoint intensity is 73.5 % of the peaks")
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.9)); ax[0].plot(x, I, color=NAVY); ax[0].plot([z1, -z1], [0, 0], "o", color=RED); ax[0].annotate("x = 3.83\n(1.22 λ/D)", (3.9, 0.12), color=RED); panel(ax[0], "x = π D sin θ / λ", "I / I₀")
    ax[1].plot(x, I, color=GREY, lw=1); ax[1].plot(x, I2, color=GREY, lw=1); ax[1].plot(x, tot, color=RED); ax[1].set_xlim(-6, 10); panel(ax[1], "x  (two sources 3.83 apart)", "I / I₀"); ax[1].annotate("dip ≈ 26 %", (off / 2 - 1.3, mid - 0.2), color=RED)
    fig.tight_layout()
    return dict(x=x, I_single=I, I_two_sources=tot), fig

@figure(C, "p2-c11-bragg", "c11", "Bragg reflection of X-rays",
        "Crystal planes $0.282\\,\\mathrm{nm}$ apart: constructive reflection when $2d\\sin\\theta=m\\lambda$. For $\\lambda=0.154\\,\\mathrm{nm}$ the first order is at $15.8^\\circ$; shorter wavelengths give smaller angles and higher orders appear when $\\lambda\\le2d/m$.",
        r"2d\sin\theta=m\lambda,\qquad m_{\max}=\left\lfloor\frac{2d}{\lambda}\right\rfloor")
def _():
    d = 0.282; lam = np.linspace(0.05, 0.18, 131); data = {"wavelength_nm": lam}; fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for m, col in ((1, NAVY), (2, RED), (3, GREEN)):
        s = m * lam / (2 * d); assert np.all(s <= 1); th = np.degrees(np.arcsin(s)); close(2 * d * np.sin(np.radians(th)), m * lam, rel=1e-12, what="Bragg condition"); ax.plot(lam, th, color=col, label="m = %d" % m); data["theta_m%d_deg" % m] = th
    t1 = np.degrees(np.arcsin(0.154 / (2 * d))); close(t1, 15.85, rel=2e-3, what="15.8 degrees"); ax.plot([0.154], [t1], "ko"); ax.annotate("0.154 nm: 15.8°", (0.158, t1 - 5), fontsize=9); close(np.floor(2 * d / 0.154), 3.0, what="highest order 3")
    panel(ax, "X-ray wavelength (nm)", "glancing angle θ (degrees)", legend=True)
    fig.tight_layout()
    return data, fig
