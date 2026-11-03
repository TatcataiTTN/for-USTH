# -*- coding: utf-8 -*-
"""Physics I figures (chapters 1-7): each one computed from the law, checked a second way, saved as PNG + CSV (see phys_plots.py)."""
import numpy as np
from scipy.integrate import solve_ivp
from phys_plots import *

C = "Physics-1"

# =============================================================================================== chapter 1: kinematics
@figure(C, "p1-c1-xva", "c1", "Constant acceleration: position, velocity, acceleration",
        "A body with $v_0=2\\,\\mathrm{m/s}$ and $a=1.5\\,\\mathrm{m/s^2}$. The slope of the $x$-$t$ curve is $v$, the slope of the $v$-$t$ line is $a$ and the area under the $v$-$t$ line is the displacement.",
        r"x=x_0+v_0t+\tfrac12at^2,\quad v=v_0+at")
def _():
    v0, a, x0 = 2.0, 1.5, 0.0; t = np.linspace(0, 6, 121)
    x = x0 + v0 * t + 0.5 * a * t ** 2; v = v0 + a * t; acc = np.full_like(t, a)
    close(np.gradient(x, t, edge_order=2), v, atol=1e-9, what="dx/dt = v"); close(trap(v, t), x[-1] - x0, what="area under v-t = displacement")
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=(7.2, 6.4))
    ax[0].plot(t, x, color=NAVY); panel(ax[0], "", "x (m)")
    ax[1].plot(t, v, color=RED); ax[1].fill_between(t, 0, v, color=RED, alpha=0.12); panel(ax[1], "", "v (m/s)")
    ax[1].annotate("area = x(6) − x(0) = %.0f m" % (x[-1] - x0), (3.0, 3.2), color=RED)
    ax[2].plot(t, acc, color=GREEN); ax[2].set_ylim(0, 2.2); panel(ax[2], "t (s)", "a (m/s²)")
    fig.tight_layout()
    return dict(t_s=t, x_m=x, v_ms=v, a_ms2=acc), fig

@figure(C, "p1-c1-projectile", "c1", "Projectile motion: trajectories for five launch angles",
        "Launch speed $20\\,\\mathrm{m/s}$, no air resistance. Complementary angles ($15^\\circ$ and $75^\\circ$, $30^\\circ$ and $60^\\circ$) give the same range; the maximum range is at $45^\\circ$.",
        r"R=\frac{v_0^2\sin2\theta}{g},\quad H=\frac{v_0^2\sin^2\theta}{2g}")
def _():
    v0 = 20.0; angs = [15, 30, 45, 60, 75]; s = np.linspace(0, 1, 201); data = {"fraction_of_flight": s}
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for th, col in zip(angs, PALETTE):
        r = np.radians(th); T = 2 * v0 * np.sin(r) / G; t = s * T
        x = v0 * np.cos(r) * t; y = v0 * np.sin(r) * t - 0.5 * G * t ** 2
        close(x[-1], v0 ** 2 * np.sin(2 * r) / G, rel=1e-9, what="range"); close(y.max(), v0 ** 2 * np.sin(r) ** 2 / (2 * G), rel=1e-4, what="height")
        ax.plot(x, y, color=col, label="%d°  (R = %.1f m)" % (th, x[-1])); data["x_%d_m" % th] = x; data["y_%d_m" % th] = y
    ax.set_aspect("equal"); ax.set_ylim(0, 22); panel(ax, "x (m)", "y (m)", legend=True)
    fig.tight_layout()
    return data, fig

@figure(C, "p1-c1-drag", "c1", "Free fall with and without air resistance",
        "Linear drag $F=-bv$ with terminal speed $30\\,\\mathrm{m/s}$: the speed approaches $v_t$ exponentially with time constant $\\tau=v_t/g$, while without drag it grows without limit.",
        r"v=v_t\left(1-e^{-t/\tau}\right),\quad \tau=\frac{v_t}{g},\quad v_t=\frac{mg}{b}")
def _():
    vt = 30.0; tau = vt / G; t = np.linspace(0, 12, 241)
    v_drag = vt * (1 - np.exp(-t / tau)); v_free = G * t
    sol = solve_ivp(lambda tt, y: [G - y[0] / tau], (0, 12), [0.0], t_eval=t, rtol=1e-10, atol=1e-12)
    close(sol.y[0], v_drag, rel=1e-6, atol=1e-8, what="ODE solution = analytic")
    fall = vt * t - vt * tau * (1 - np.exp(-t / tau))
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(t, v_free, color=GREY, ls="--", label="no air resistance  v = g t"); ax.plot(t, v_drag, color=NAVY, label="with drag"); ax.axhline(vt, color=RED, lw=1.2)
    ax.annotate("terminal speed 30 m/s", (6.5, vt + 1.2), color=RED); ax.set_ylim(0, 70); panel(ax, "t (s)", "v (m/s)", legend=True)
    fig.tight_layout()
    return dict(t_s=t, v_free_ms=v_free, v_drag_ms=v_drag, fallen_drag_m=fall), fig

@figure(C, "p1-c1-graphs", "c1", "Reading motion graphs: a(t), v(t) and x(t) of one trip",
        "Acceleration $+2\\,\\mathrm{m/s^2}$ for $3\\,\\mathrm{s}$, then $0$ for $3\\,\\mathrm{s}$, then $-1.5\\,\\mathrm{m/s^2}$ for $4\\,\\mathrm{s}$. The area under $a$-$t$ is the change of $v$; the area under $v$-$t$ is the change of $x$; the body stops at $t=10\\,\\mathrm{s}$ after $39\\,\\mathrm{m}$.",
        r"\Delta v=\int a\,dt,\qquad \Delta x=\int v\,dt")
def _():
    t = np.linspace(0, 10, 1001); a = np.where(t < 3, 2.0, np.where(t < 6, 0.0, -1.5))
    v = np.where(t < 3, 2.0 * t, np.where(t < 6, 6.0, 6.0 - 1.5 * (t - 6)))                                   # exact integral of the step function a(t)
    x = np.where(t < 3, t ** 2, np.where(t < 6, 9.0 + 6.0 * (t - 3), 27.0 + 6.0 * (t - 6) - 0.75 * (t - 6) ** 2))
    close(v[-1], 0.0, atol=1e-9, what="v(10) = 6 - 6 = 0"); close(x[-1], 39.0, rel=1e-12, what="x(10) = 9 + 18 + 12")
    close(cumtrap(v, t), x, atol=0.03, what="area under v-t = x")
    close(trap(a, t), v[-1], atol=0.03, what="area under a-t = v(10) - v(0)")
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=(7.2, 6.4))
    ax[0].plot(t, a, color=GREEN); ax[0].fill_between(t, 0, a, color=GREEN, alpha=0.15); panel(ax[0], "", "a (m/s²)")
    ax[1].plot(t, v, color=RED); ax[1].fill_between(t, 0, v, color=RED, alpha=0.12); panel(ax[1], "", "v (m/s)")
    ax[2].plot(t, x, color=NAVY); panel(ax[2], "t (s)", "x (m)"); ax[2].annotate("x(10 s) = 39 m", (6.2, 30), color=NAVY)
    fig.tight_layout()
    return dict(t_s=t, a_ms2=a, v_ms=v, x_m=x), fig

@figure(C, "p1-c1-vectors", "c1", "Adding and subtracting vectors by components",
        "$\\vec A=(3,4)$ and $\\vec B=(-1,2)$: add or subtract component by component; the magnitude of the sum is $\\sqrt{40}=6.32$, not $|A|+|B|=7.24$.",
        r"\vec A+\vec B=(A_x+B_x,\ A_y+B_y),\quad |\vec A|=\sqrt{A_x^2+A_y^2}")
def _():
    A = np.array([3.0, 4.0]); Bv = np.array([-1.0, 2.0]); S = A + Bv; D = A - Bv
    close(np.hypot(*S), np.sqrt(40.0), what="|A+B|")
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    def arrow(p, q, col, lab, ls="-"):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2, ls=ls)); ax.text((p[0] + q[0]) / 2 + 0.1, (p[1] + q[1]) / 2 - 0.35, lab, color=col, fontsize=11)
    arrow((0, 0), A, NAVY, "A = (3, 4)"); arrow(A, A + Bv, RED, "B = (−1, 2)"); arrow((0, 0), S, GREEN, "A + B = (2, 6)")
    arrow((0, 0), Bv, RED, "", "--"); ax.plot([A[0], A[0] + Bv[0]], [A[1], A[1] + Bv[1]], alpha=0)
    ax.set_xlim(-2, 5); ax.set_ylim(-0.5, 7); ax.set_aspect("equal"); panel(ax, "x", "y")
    fig.tight_layout()
    names = np.array(["A", "B", "A+B", "A-B"]); vx = np.array([A[0], Bv[0], S[0], D[0]]); vy = np.array([A[1], Bv[1], S[1], D[1]])
    return dict(vector=names, x=vx, y=vy, magnitude=np.hypot(vx, vy), angle_deg=np.degrees(np.arctan2(vy, vx))), fig

# =============================================================================================== chapter 2: dynamics
@figure(C, "p1-c2-incline", "c2", "Acceleration down an incline against the angle",
        "$a=g(\\sin\\theta-\\mu\\cos\\theta)$ once $\\tan\\theta>\\mu$; below that angle friction holds the block. At $90^\\circ$ every curve reaches $g$ (free fall).",
        r"a=g(\sin\theta-\mu_k\cos\theta),\qquad \tan\theta_{\min}=\mu_s")
def _():
    th = np.linspace(0, 90, 181); r = np.radians(th); data = {"theta_deg": th}
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for mu, col in zip([0.0, 0.2, 0.4], [NAVY, RED, GREEN]):
        a = np.where(np.tan(r) > mu, G * (np.sin(r) - mu * np.cos(r)), 0.0)
        close(a[-1], G, rel=1e-9, what="a(90) = g")
        ax.plot(th, a, color=col, label="μ = %.1f" % mu); data["a_mu%.1f_ms2" % mu] = a
        if mu: ax.plot([np.degrees(np.arctan(mu))], [0], "o", color=col)
    panel(ax, "angle of the incline θ (degrees)", "a (m/s²)", legend=True); ax.set_xlim(0, 90)
    fig.tight_layout()
    return data, fig

@figure(C, "p1-c2-atwood", "c2", "Atwood machine: acceleration and tension against the mass ratio",
        "$m_1=1\\,\\mathrm{kg}$ and $m_2=r\\,m_1$. For $r\\to\\infty$ the acceleration approaches $g$ and the tension approaches $2m_1g$; for $r=1$ nothing moves and $T=m_1g$.",
        r"a=\frac{m_2-m_1}{m_1+m_2}\,g,\qquad T=\frac{2m_1m_2}{m_1+m_2}\,g")
def _():
    r = np.linspace(1, 10, 91); m1 = 1.0; m2 = r * m1
    a = (m2 - m1) / (m1 + m2) * G; T = 2 * m1 * m2 / (m1 + m2) * G
    close(T, m1 * (G + a), what="T = m1 (g + a)"); close(T, m2 * (G - a), what="T = m2 (g - a)")
    fig, ax = plt.subplots(1, 2, figsize=(8.0, 3.6))
    ax[0].plot(r, a, color=NAVY); ax[0].axhline(G, color=GREY, ls="--"); panel(ax[0], "mass ratio  m₂/m₁", "a (m/s²)"); ax[0].set_ylim(0, 11)
    ax[1].plot(r, T, color=RED); ax[1].axhline(2 * m1 * G, color=GREY, ls="--"); panel(ax[1], "mass ratio  m₂/m₁", "T (N)"); ax[1].set_ylim(0, 22)
    fig.tight_layout()
    return dict(mass_ratio=r, a_ms2=a, tension_N=T), fig

@figure(C, "p1-c2-friction", "c2", "Static and kinetic friction against the applied force",
        "A $10\\,\\mathrm{kg}$ crate ($\\mu_s=0.5$, $\\mu_k=0.3$): friction equals the applied force until $\\mu_smg=49\\,\\mathrm{N}$, then drops to $\\mu_kmg=29.4\\,\\mathrm{N}$ and the crate accelerates.",
        r"f_s\le\mu_sN,\qquad f_k=\mu_kN,\qquad a=\frac{F-\mu_kmg}{m}")
def _():
    m, mus, muk = 10.0, 0.5, 0.3; F = np.linspace(0, 80, 321); N = m * G
    f = np.where(F <= mus * N, F, muk * N); a = np.where(F <= mus * N, 0.0, (F - muk * N) / m)
    close(f[F <= mus * N][-1], mus * N, rel=1e-2, what="static maximum"); close(f[-1], muk * N, what="kinetic value")
    fig, ax = plt.subplots(1, 2, figsize=(8.2, 3.7))
    ax[0].plot(F, f, color=NAVY); ax[0].axhline(mus * N, color=GREY, ls=":"); ax[0].axhline(muk * N, color=GREY, ls=":"); panel(ax[0], "applied force F (N)", "friction f (N)")
    ax[0].annotate("μₛN = 49 N", (3, 51), color=GREY); ax[0].annotate("μₖN = 29.4 N", (45, 24.5), color=GREY)
    ax[1].plot(F, a, color=RED); panel(ax[1], "applied force F (N)", "a (m/s²)")
    fig.tight_layout()
    return dict(F_N=F, friction_N=f, a_ms2=a), fig

@figure(C, "p1-c2-springs", "c2", "Hooke's law: single springs, springs in parallel and in series",
        "$k_1=200\\,\\mathrm{N/m}$, $k_2=300\\,\\mathrm{N/m}$. In parallel the constants add ($500$); in series the compliances add, so the combination is softer than either spring ($120$).",
        r"F=kx,\qquad k_{\parallel}=k_1+k_2,\qquad \frac1{k_{\rm series}}=\frac1{k_1}+\frac1{k_2}")
def _():
    x = np.linspace(0, 0.10, 51); k1, k2 = 200.0, 300.0; kp = k1 + k2; ks = k1 * k2 / (k1 + k2)
    ser = {k: np.polyfit(x, k * x, 1)[0] for k in (k1, k2, kp, ks)}
    for k in ser: close(ser[k], k, rel=1e-9, what="slope = k")
    close(ks, 120.0, what="series constant")
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    for k, col, lab in ((kp, NAVY, "parallel  500 N/m"), (k2, GREEN, "spring 2  300 N/m"), (k1, ORANGE, "spring 1  200 N/m"), (ks, RED, "series  120 N/m")): ax.plot(x * 100, k * x, color=col, label=lab)
    panel(ax, "extension x (cm)", "force F (N)", legend=True)
    fig.tight_layout()
    return dict(x_m=x, F_k200_N=k1 * x, F_k300_N=k2 * x, F_parallel_N=kp * x, F_series_N=ks * x), fig

@figure(C, "p1-c2-elevator", "c2", "Apparent weight in an elevator",
        "A $60\\,\\mathrm{kg}$ passenger: $+1.5\\,\\mathrm{m/s^2}$ for $2\\,\\mathrm{s}$, cruise, then $-1.5\\,\\mathrm{m/s^2}$ for $2\\,\\mathrm{s}$. The scale reads $N=m(g+a)$: more than $mg$ while speeding up, exactly $mg$ at constant speed, less while slowing down.",
        r"N-mg=ma\ \Rightarrow\ N=m(g+a)")
def _():
    m = 60.0; t = np.linspace(0, 12, 1201); a = np.where(t < 2, 1.5, np.where(t < 10, 0.0, -1.5)); N = m * (G + a)
    v = np.where(t < 2, 1.5 * t, np.where(t < 10, 3.0, 3.0 - 1.5 * (t - 10)))                                     # exact integral of the step function a(t)
    close(v[-1], 0.0, atol=1e-9, what="the elevator ends at rest"); close(trap(a, t), 0.0, atol=0.03, what="area under a-t = 0")
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=(7.2, 6.4))
    ax[0].plot(t, a, color=GREEN); panel(ax[0], "", "a (m/s²)"); ax[1].plot(t, v, color=RED); panel(ax[1], "", "v (m/s)")
    ax[2].plot(t, N, color=NAVY); ax[2].axhline(m * G, color=GREY, ls="--"); panel(ax[2], "t (s)", "scale reading N (N)"); ax[2].annotate("mg = 588 N", (6, 595), color=GREY)
    fig.tight_layout()
    return dict(t_s=t, a_ms2=a, v_ms=v, scale_N=N), fig

# =============================================================================================== chapter 3: work, energy, momentum
@figure(C, "p1-c3-workarea", "c3", "Work as the area under the force-position graph",
        "A force that rises to $3\\,\\mathrm{N}$ over the first $2\\,\\mathrm{m}$, stays constant to $4\\,\\mathrm{m}$ and falls to zero at $6\\,\\mathrm{m}$ does $3+6+3=12\\,\\mathrm{J}$ of work. The right panel is the running total $W(x)$.",
        r"W=\int_{x_1}^{x_2}F\,dx=\Delta K")
def _():
    xs = np.linspace(0, 6, 601); F = np.interp(xs, [0, 2, 4, 6], [0, 3, 3, 0]); W = cumtrap(F, xs)
    close(W[-1], 12.0, rel=1e-6, what="total work 12 J")
    fig, ax = plt.subplots(1, 2, figsize=(8.2, 3.7))
    ax[0].plot(xs, F, color=NAVY); ax[0].fill_between(xs, 0, F, color=NAVY, alpha=0.15); panel(ax[0], "x (m)", "F (N)"); ax[0].annotate("area = 12 J", (2.2, 1.2), color=NAVY)
    ax[1].plot(xs, W, color=RED); panel(ax[1], "x (m)", "W(x) (J)")
    fig.tight_layout()
    return dict(x_m=xs, F_N=F, work_J=W), fig

@figure(C, "p1-c3-potential", "c3", "A potential-energy curve: turning points and kinetic energy",
        "For $U(x)=x^4/4-x^2$ (joules) and total energy $E=-0.6\\,\\mathrm{J}$ the particle can only be where $U\\le E$; the kinetic energy $K=E-U$ is the gap between the line and the curve. The force is minus the slope of $U$.",
        r"K=E-U(x),\qquad F=-\frac{dU}{dx}")
def _():
    x = np.linspace(-2.2, 2.2, 441); U = x ** 4 / 4 - x ** 2; E = -0.6; K = np.where(U <= E, E - U, 0.0)
    F = -(x ** 3 - 2 * x); close(F, -np.gradient(U, x, edge_order=2), atol=2e-3, what="F = -dU/dx")
    tp = np.roots([0.25, 0, -1, 0, -E])                       # turning points: U(x) = E
    tp = np.sort(tp[np.abs(tp.imag) < 1e-9].real)
    assert len(tp) == 4
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(x, U, color=NAVY, label="U(x)"); ax.axhline(E, color=RED, label="E = −0.6 J"); ax.fill_between(x, U, E, where=U <= E, color=RED, alpha=0.15, label="kinetic energy")
    ax.plot(tp, [E] * 4, "o", color=RED); ax.set_ylim(-1.3, 1.2); panel(ax, "x (m)", "energy (J)", legend=True)
    fig.tight_layout()
    return dict(x_m=x, U_J=U, K_J_for_E_minus0p6=K, F_N=F), fig

@figure(C, "p1-c3-collisions", "c3", "One-dimensional collisions against the mass ratio",
        "$m_1=1\\,\\mathrm{kg}$ at $4\\,\\mathrm{m/s}$ hits $m_2=r\\,m_1$ at rest. Elastic: $m_1$ stops at $r=1$ and bounces back for $r>1$. Perfectly inelastic: the common speed is $u/(1+r)$ and the fraction $r/(1+r)$ of the kinetic energy is lost.",
        r"v_1'=\frac{m_1-m_2}{m_1+m_2}u,\quad v_2'=\frac{2m_1}{m_1+m_2}u,\quad v'=\frac{m_1u}{m_1+m_2}")
def _():
    u = 4.0; r = np.linspace(0.1, 10, 100); m1 = 1.0; m2 = r
    v1 = (m1 - m2) / (m1 + m2) * u; v2 = 2 * m1 / (m1 + m2) * u; vc = m1 * u / (m1 + m2)
    close(m1 * v1 + m2 * v2, m1 * u, what="momentum"); close(0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2, 0.5 * m1 * u ** 2, what="kinetic energy (elastic)")
    lost = 1 - (0.5 * (m1 + m2) * vc ** 2) / (0.5 * m1 * u ** 2); close(lost, m2 / (m1 + m2), what="energy lost")
    fig, ax = plt.subplots(1, 2, figsize=(8.2, 3.7))
    ax[0].plot(r, v1, color=NAVY, label="elastic: m₁"); ax[0].plot(r, v2, color=RED, label="elastic: m₂"); ax[0].plot(r, vc, color=GREEN, label="inelastic (both)"); ax[0].axhline(0, color=GREY, lw=1)
    panel(ax[0], "mass ratio  m₂/m₁", "final velocity (m/s)", legend=True); ax[1].plot(r, lost * 100, color=ORANGE); panel(ax[1], "mass ratio  m₂/m₁", "kinetic energy lost (%)")
    fig.tight_layout()
    return dict(mass_ratio=r, v1_elastic_ms=v1, v2_elastic_ms=v2, v_inelastic_ms=vc, energy_lost_fraction=lost), fig

@figure(C, "p1-c3-impulse", "c3", "Impulse of a collision force",
        "A half-sine force pulse of peak $600\\,\\mathrm{N}$ lasting $10\\,\\mathrm{ms}$ gives an impulse $2F_0T/\\pi=3.82\\,\\mathrm{N\\,s}$; on a $0.15\\,\\mathrm{kg}$ ball that is a velocity change of $25.5\\,\\mathrm{m/s}$.",
        r"J=\int F\,dt=\Delta p=m\,\Delta v")
def _():
    F0, T, m = 600.0, 10e-3, 0.15; t = np.linspace(0, T, 501); F = F0 * np.sin(np.pi * t / T); J = cumtrap(F, t)
    close(J[-1], 2 * F0 * T / np.pi, rel=1e-5, what="impulse = 2 F0 T / pi")
    fig, ax = plt.subplots(1, 2, figsize=(8.2, 3.7))
    ax[0].plot(t * 1e3, F, color=NAVY); ax[0].fill_between(t * 1e3, 0, F, color=NAVY, alpha=0.15); panel(ax[0], "t (ms)", "F (N)")
    ax[1].plot(t * 1e3, J / m, color=RED); panel(ax[1], "t (ms)", "velocity change  Δv = J/m  (m/s)")
    fig.tight_layout()
    return dict(t_ms=t * 1e3, F_N=F, impulse_Ns=J, delta_v_ms=J / m), fig

@figure(C, "p1-c3-power", "c3", "Power needed by a car against its speed",
        "Resistance $F=200+0.4v^2$ (newtons). The power needed, $P=Fv$, grows like $v^3$ at high speed; with a $60\\,\\mathrm{kW}$ engine the top speed is where the curve crosses $60\\,\\mathrm{kW}$.",
        r"P=Fv=(f_0+cv^2)\,v")
def _():
    v = np.linspace(0, 45, 451); f0, c = 200.0, 0.4; Fr = f0 + c * v ** 2; P = Fr * v / 1e3
    from scipy.optimize import brentq
    vtop = brentq(lambda s: (f0 + c * s * s) * s - 60e3, 1, 80); close((f0 + c * vtop ** 2) * vtop, 60e3, rel=1e-9, what="top speed root")
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(v, P, color=NAVY, label="power needed  P = F v"); ax.axhline(60, color=RED, label="engine 60 kW"); ax.plot([vtop], [60], "o", color=RED)
    ax.annotate("top speed %.1f m/s (%.0f km/h)" % (vtop, vtop * 3.6), (vtop - 21, 66), color=RED); ax.set_ylim(0, 100); panel(ax, "speed v (m/s)", "power (kW)", legend=True)
    fig.tight_layout()
    return dict(v_ms=v, resistance_N=Fr, power_kW=P), fig

# =============================================================================================== chapter 4: circular motion and rotation
@figure(C, "p1-c4-centripetal", "c4", "Centripetal force against speed and radius",
        "A $1000\\,\\mathrm{kg}$ car on a circular path: $F=mv^2/r$ grows with the square of the speed and falls with the radius. Friction (or banking) must supply it, which is why sharp bends are taken slowly.",
        r"a_c=\frac{v^2}{r},\qquad F_c=\frac{mv^2}{r}")
def _():
    m = 1000.0; v = np.linspace(0, 30, 61); data = {"v_ms": v}
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for r, col in zip((25, 50, 100, 200), PALETTE):
        F = m * v ** 2 / r; close(F[1:] * r / v[1:] ** 2, m, what="F r / v^2 = m"); ax.plot(v, F / 1e3, color=col, label="r = %d m" % r); data["F_r%d_kN" % r] = F / 1e3
    panel(ax, "speed v (m/s)", "centripetal force (kN)", legend=True)
    fig.tight_layout()
    return data, fig

@figure(C, "p1-c4-banked", "c4", "Ideal speed on a banked curve",
        "On a frictionless banked bend the normal force alone supplies the centripetal force: $\\tan\\theta=v^2/(rg)$. The ideal speed grows with the bank angle and with the radius.",
        r"N\cos\theta=mg,\quad N\sin\theta=\frac{mv^2}{r}\ \Rightarrow\ v=\sqrt{rg\tan\theta}")
def _():
    th = np.linspace(1, 45, 89); rad = np.radians(th); data = {"theta_deg": th}
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for R, col in zip((50, 100, 200), (NAVY, RED, GREEN)):
        v = np.sqrt(R * G * np.tan(rad)); close(v ** 2 / (R * G), np.tan(rad), what="force balance tan(theta) = v^2 / (r g)")
        ax.plot(th, v * 3.6, color=col, label="R = %d m" % R); data["v_R%d_kmh" % R] = v * 3.6
    panel(ax, "bank angle θ (degrees)", "ideal speed (km/h)", legend=True)
    fig.tight_layout()
    return data, fig

@figure(C, "p1-c4-rotkin", "c4", "Rotation with constant angular acceleration",
        "$\\alpha=2\\,\\mathrm{rad/s^2}$, $\\omega_0=1\\,\\mathrm{rad/s}$, point at $r=0.30\\,\\mathrm{m}$. The tangential speed $v=\\omega r$ grows linearly; the centripetal acceleration $\\omega^2r$ grows quadratically; the tangential acceleration $\\alpha r$ is constant.",
        r"\theta=\omega_0t+\tfrac12\alpha t^2,\quad \omega=\omega_0+\alpha t,\quad v=\omega r,\quad a_c=\omega^2r")
def _():
    t = np.linspace(0, 6, 121); w0, al, r = 1.0, 2.0, 0.30
    th = w0 * t + 0.5 * al * t ** 2; w = w0 + al * t; vt = w * r; ac = w ** 2 * r; at = np.full_like(t, al * r)
    close(np.gradient(th, t, edge_order=2), w, atol=1e-9, what="omega = d theta / dt"); close(ac, vt ** 2 / r, what="a_c = v^2 / r")
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8))
    ax[0].plot(t, th, color=NAVY, label="θ (rad)"); ax[0].plot(t, w, color=RED, label="ω (rad/s)"); panel(ax[0], "t (s)", "", legend=True)
    ax[1].plot(t, vt, color=GREEN, label="v = ωr (m/s)"); ax[1].plot(t, ac, color=ORANGE, label="a_c = ω²r (m/s²)"); ax[1].plot(t, at, color=GREY, label="a_t = αr (m/s²)"); panel(ax[1], "t (s)", "", legend=True)
    fig.tight_layout()
    return dict(t_s=t, theta_rad=th, omega_rads=w, v_tangential_ms=vt, a_centripetal_ms2=ac, a_tangential_ms2=at), fig

@figure(C, "p1-c4-inertia", "c4", "Moment of inertia and the rolling race",
        "$I=\\beta MR^2$ with $\\beta=1$ (hoop), $\\tfrac23$ (hollow sphere), $\\tfrac12$ (cylinder), $\\tfrac25$ (solid sphere). Rolling down a $30^\\circ$ incline, $a=g\\sin\\theta/(1+\\beta)$: the smaller $\\beta$, the faster; a frictionless sliding block beats them all.",
        r"a=\frac{g\sin\theta}{1+I/(MR^2)},\qquad K=\tfrac12Mv^2\,(1+\beta)")
def _():
    names = ["hoop", "hollow sphere", "solid cylinder", "solid sphere"]; beta = [1.0, 2 / 3, 0.5, 0.4]; th = np.radians(30); t = np.linspace(0, 2, 81)
    acc = {n: G * np.sin(th) / (1 + b) for n, b in zip(names, beta)}; acc["sliding block"] = G * np.sin(th)
    for n, b in list(zip(names, beta)) + [("sliding block", 0.0)]:
        d = 0.5 * acc[n] * 2.0 ** 2; v = acc[n] * 2.0; close(0.5 * (1 + b) * v ** 2, G * np.sin(th) * d, what="energy conservation for " + n)
    assert acc["sliding block"] > acc["solid sphere"] > acc["solid cylinder"] > acc["hollow sphere"] > acc["hoop"]
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.9), gridspec_kw=dict(width_ratios=[1, 1.25]))
    ax[0].barh(names, beta, color=[NAVY, PURPLE, GREEN, RED]); ax[0].invert_yaxis(); panel(ax[0], "β = I/(MR²)", ""); ax[0].grid(axis="y", alpha=0)
    data = {"t_s": t}
    for (n, a), col in zip(acc.items(), [NAVY, PURPLE, GREEN, RED, GREY]):
        x = 0.5 * a * t ** 2; ax[1].plot(t, x, color=col, label="%s (a = %.2f)" % (n, a)); data["x_%s_m" % n.replace(" ", "_")] = x
    panel(ax[1], "t (s)", "distance along the incline (m)", legend=True); ax[1].legend(frameon=False, fontsize=8.5)
    fig.tight_layout()
    return data, fig

@figure(C, "p1-c4-skater", "c4", "Conservation of angular momentum: the spinning skater",
        "With no external torque $L=I\\omega$ stays constant ($8\\,\\mathrm{kg\\,m^2/s}$). Pulling the arms in lowers $I$ from $4$ to $1\\,\\mathrm{kg\\,m^2}$: $\\omega$ rises from $2$ to $8\\,\\mathrm{rad/s}$ and the kinetic energy from $8$ to $32\\,\\mathrm{J}$ (the skater does the work).",
        r"L=I\omega=\text{const},\qquad K=\frac{L^2}{2I}")
def _():
    I = np.linspace(4.0, 1.0, 61); L = 8.0; w = L / I; K = L ** 2 / (2 * I)
    close(I * w, L, what="L constant"); close(K, 0.5 * I * w ** 2, what="K = I w^2 / 2"); close([K[0], K[-1]], [8.0, 32.0], what="kinetic energies")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.plot(I, w, color=NAVY, label="ω (rad/s)"); ax.set_xlabel("moment of inertia I (kg m²)"); ax.set_ylabel("ω (rad/s)", color=NAVY)
    ax2 = ax.twinx(); ax2.plot(I, K, color=RED, label="K (J)"); ax2.set_ylabel("kinetic energy K (J)", color=RED); ax2.grid(False); ax2.spines["right"].set_visible(True)
    ax.invert_xaxis(); fig.tight_layout()
    return dict(I_kgm2=I, omega_rads=w, K_J=K), fig

# =============================================================================================== chapter 5: temperature, heat, first law
@figure(C, "p1-c5-heating", "c5", "Heating curve of 1 kg of water from ice at −20 °C to steam at 120 °C",
        "Slopes are set by the specific heats (ice $2090$, water $4186$, steam $2010\\,\\mathrm{J/kg\\,K}$); the plateaus are the latent heats of fusion ($334\\,\\mathrm{kJ}$) and vaporisation ($2256\\,\\mathrm{kJ}$). Total heat: $3090.6\\,\\mathrm{kJ}$.",
        r"Q=mc\,\Delta T\ \ (\text{no phase change}),\qquad Q=mL\ \ (\text{phase change})")
def _():
    m = 1.0; Q = [m * 2090 * 20, m * 334e3, m * 4186 * 100, m * 2256e3, m * 2010 * 20]; qs = np.concatenate([[0], np.cumsum(Q)]); Ts = [-20, 0, 0, 100, 100, 120]
    close(qs[-1] / 1e3, 3090.6, rel=1e-9, what="total heat")
    q = np.linspace(0, qs[-1], 361); T = np.interp(q, qs, Ts)
    fig, ax = plt.subplots(figsize=(7.4, 4.1)); ax.plot(q / 1e3, T, color=NAVY)
    for (x, y, lab) in ((70, -15, "ice"), (90, 8, "melting"), (620, 40, "water"), (1500, 105, "boiling")):
        ax.annotate(lab, (x, y), color=RED, fontsize=10)
    ax.annotate("steam", xy=(3075, 112), xytext=(2600, 118), color=RED, fontsize=10, arrowprops=dict(arrowstyle="->", color=RED))
    panel(ax, "heat added Q (kJ)", "temperature (°C)"); ax.set_ylim(-30, 135)
    fig.tight_layout()
    return dict(Q_kJ=q / 1e3, T_C=T), fig

@figure(C, "p1-c5-expansion", "c5", "Thermal expansion of 1 m rods",
        "$\\Delta L=\\alpha L\\,\\Delta T$: for the same temperature rise aluminium ($23\\times10^{-6}\\,\\mathrm{K^{-1}}$) grows almost twice as much as steel ($12\\times10^{-6}$), copper ($17\\times10^{-6}$) and Pyrex glass ($3.2\\times10^{-6}$) far less.",
        r"\Delta L=\alpha L\,\Delta T,\qquad \Delta A\approx2\alpha A\,\Delta T,\qquad \Delta V\approx3\alpha V\,\Delta T")
def _():
    dT = np.linspace(0, 100, 51); mats = {"aluminium": 23e-6, "copper": 17e-6, "steel": 12e-6, "Pyrex glass": 3.2e-6}; data = {"dT_K": dT}
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for (n, al), col in zip(mats.items(), (RED, ORANGE, NAVY, GREEN)):
        dL = al * 1.0 * dT * 1e3; ax.plot(dT, dL, color=col, label="%s  α = %.1e /K" % (n, al)); data["dL_%s_mm" % n.replace(" ", "_")] = dL
    close(data["dL_aluminium_mm"][-1] / data["dL_steel_mm"][-1], 23 / 12, what="ratio of expansions")
    panel(ax, "temperature rise ΔT (K)", "length increase ΔL (mm)", legend=True)
    fig.tight_layout()
    return data, fig

@figure(C, "p1-c5-mixing", "c5", "Calorimetry: final temperature of a mixture",
        "Hot liquid at $80^\\circ\\mathrm{C}$ poured into cold water at $20^\\circ\\mathrm{C}$. With the same specific heat the temperature is a mass-weighted average; oil ($c=2000\\,\\mathrm{J/kg\\,K}$) gives up less heat per kilogram, so the mixture stays cooler.",
        r"m_hc_h(T_h-T_f)=m_cc_c(T_f-T_c)\ \Rightarrow\ T_f=\frac{m_hc_hT_h+m_cc_cT_c}{m_hc_h+m_cc_c}")
def _():
    x = np.linspace(0, 1, 101); Th, Tc = 80.0, 20.0; cw, co = 4186.0, 2000.0
    Tw = (x * cw * Th + (1 - x) * cw * Tc) / (x * cw + (1 - x) * cw); To = (x * co * Th + (1 - x) * cw * Tc) / (x * co + (1 - x) * cw)
    close(Tw, Tc + (Th - Tc) * x, what="equal specific heats"); close(x * co * (Th - To), (1 - x) * cw * (To - Tc), atol=1e-6, what="heat lost = heat gained")
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(x * 100, Tw, color=NAVY, label="hot water into cold water"); ax.plot(x * 100, To, color=RED, label="hot oil into cold water"); panel(ax, "hot liquid, % of the total mass", "final temperature (°C)", legend=True)
    fig.tight_layout()
    return dict(hot_mass_fraction=x, T_final_water_C=Tw, T_final_oil_C=To), fig

@figure(C, "p1-c5-pvpaths", "c5", "Work on a p-V diagram: isothermal and isobaric expansion",
        "$0.10\\,\\mathrm{mol}$ of ideal gas at $300\\,\\mathrm{K}$ expands from $2\\,\\mathrm{L}$ to $6\\,\\mathrm{L}$. The work is the area under the path: $nRT\\ln3=274\\,\\mathrm{J}$ along the isotherm, $p_1\\Delta V=499\\,\\mathrm{J}$ at constant pressure.",
        r"W=\int p\,dV,\qquad W_{\rm iso}=nRT\ln\frac{V_2}{V_1},\qquad W_{\rm isobar}=p\,\Delta V")
def _():
    n, R, T = 0.10, 8.314, 300.0; V1, V2 = 2.0e-3, 6.0e-3; V = np.linspace(V1, V2, 201); p1 = n * R * T / V1
    p_iso = n * R * T / V; p_bar = np.full_like(V, p1)
    Wi, Wb = trap(p_iso, V), trap(p_bar, V); close(Wi, n * R * T * np.log(V2 / V1), rel=1e-4, what="isothermal work"); close(Wb, p1 * (V2 - V1), what="isobaric work")
    fig, ax = plt.subplots(figsize=(7.2, 4.1)); ax.plot(V * 1e3, p_bar / 1e3, color=RED, label="isobaric: W = %.0f J" % Wb); ax.fill_between(V * 1e3, 0, p_bar / 1e3, color=RED, alpha=0.08)
    ax.plot(V * 1e3, p_iso / 1e3, color=NAVY, label="isothermal: W = %.0f J" % Wi); ax.fill_between(V * 1e3, 0, p_iso / 1e3, color=NAVY, alpha=0.15)
    panel(ax, "V (L)", "p (kPa)", legend=True); ax.set_ylim(0, 150)
    fig.tight_layout()
    return dict(V_m3=V, p_isothermal_Pa=p_iso, p_isobaric_Pa=p_bar), fig

# =============================================================================================== chapter 6: kinetic theory
@figure(C, "p1-c6-maxwell", "c6", "Maxwell speed distribution of nitrogen",
        "$N_2$ ($M=28\\,\\mathrm{g/mol}$) at $300\\,\\mathrm{K}$ and $600\\,\\mathrm{K}$. The most probable speed is below the mean, which is below the rms speed: $v_p<v_{\\rm avg}<v_{\\rm rms}$. Raising $T$ shifts and flattens the curve; the area stays $1$.",
        r"f(v)=4\pi\left(\frac{M}{2\pi RT}\right)^{3/2}v^2e^{-Mv^2/2RT},\quad v_p=\sqrt{\tfrac{2RT}{M}},\ v_{\rm avg}=\sqrt{\tfrac{8RT}{\pi M}},\ v_{\rm rms}=\sqrt{\tfrac{3RT}{M}}")
def _():
    R, M = 8.314, 0.028; v = np.linspace(0, 2000, 2001); data = {"v_ms": v}
    f = lambda T: 4 * np.pi * (M / (2 * np.pi * R * T)) ** 1.5 * v ** 2 * np.exp(-M * v ** 2 / (2 * R * T))
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    for T, col in ((300, NAVY), (600, RED)):
        fv = f(T); close(trap(fv, v), 1.0, rel=1e-3, what="normalisation")
        vp, va, vr = np.sqrt(2 * R * T / M), np.sqrt(8 * R * T / (np.pi * M)), np.sqrt(3 * R * T / M)
        close(trap(v * fv, v), va, rel=2e-3, what="mean speed"); close(np.sqrt(trap(v ** 2 * fv, v)), vr, rel=2e-3, what="rms speed")
        ax.plot(v, fv * 1e3, color=col, label="T = %d K" % T); data["f_%dK_per_ms" % T] = fv
        if T == 300:
            for val, lab, ls in ((vp, "v_p", ":"), (va, "v_avg", "--"), (vr, "v_rms", "-.")): ax.axvline(val, color=GREY, ls=ls, lw=1.2, label="%s = %.0f m/s (300 K)" % (lab, val))
    panel(ax, "speed v (m/s)", "probability density f(v)  (10⁻³ per m/s)", legend=True); ax.set_xlim(0, 1800); ax.set_ylim(0, 2.1)
    fig.tight_layout()
    return data, fig

@figure(C, "p1-c6-isotherms", "c6", "Isotherms and an adiabat of an ideal gas",
        "One mole of a monatomic gas ($\\gamma=5/3$). Along an isotherm $pV$ is constant; along an adiabat $pV^\\gamma$ is constant, so the adiabat is steeper: at the crossing point its slope is $\\gamma$ times the slope of the isotherm.",
        r"pV=nRT,\qquad pV^{\gamma}=\text{const},\qquad \gamma=\frac{C_p}{C_V}")
def _():
    n, R, g = 1.0, 8.314, 5 / 3; V = np.linspace(0.012, 0.060, 97); data = {"V_m3": V}
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    for T, col in ((300, NAVY), (400, RED), (500, GREEN)):
        p = n * R * T / V; close(p * V, n * R * T, what="pV = nRT"); ax.plot(V * 1e3, p / 1e3, color=col, label="isotherm %d K" % T); data["p_%dK_Pa" % T] = p
    VA = 0.020; TA = 400.0; pA = n * R * TA / VA; padi = pA * (VA / V) ** g; close(padi * V ** g, pA * VA ** g, what="p V^gamma")
    h = 1e-7; sl_ad = (pA * (VA / (VA + h)) ** g - pA * (VA / (VA - h)) ** g) / (2 * h); sl_is = -pA / VA; close(sl_ad / sl_is, g, rel=1e-6, what="adiabat slope = gamma x isotherm slope")
    ax.plot(V * 1e3, padi / 1e3, color=ORANGE, ls="--", lw=2.4, label="adiabat through A"); ax.plot([VA * 1e3], [pA / 1e3], "ko"); ax.annotate("A", (VA * 1e3 + 0.6, pA / 1e3 + 6))
    data["p_adiabat_Pa"] = padi; panel(ax, "V (L)", "p (kPa)", legend=True); ax.set_ylim(0, 360)
    fig.tight_layout()
    return data, fig

@figure(C, "p1-c6-heatcap", "c6", "Molar heat capacities and the number of degrees of freedom",
        "$C_V=\\tfrac f2R$ and $C_p=C_V+R$: monatomic gases ($f=3$) have $\\gamma=5/3$, diatomic gases at room temperature ($f=5$) $\\gamma=7/5$, polyatomic gases ($f=6$) $\\gamma=4/3$.",
        r"C_V=\frac f2R,\qquad C_p=C_V+R,\qquad \gamma=\frac{C_p}{C_V}=1+\frac2f")
def _():
    kinds = np.array(["monatomic (He)", "diatomic (N2)", "polyatomic (CH4)"]); f = np.array([3.0, 5.0, 6.0]); cv = f / 2; cp = cv + 1; gam = cp / cv
    close(cp - cv, 1.0, what="Cp - Cv = R"); close(gam, 1 + 2 / f, what="gamma = 1 + 2/f")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); xs = np.arange(3); wdt = 0.36
    ax.bar(xs - wdt / 2, cv, wdt, color=NAVY, label="C_V / R"); ax.bar(xs + wdt / 2, cp, wdt, color=RED, label="C_p / R")
    for i in range(3): ax.text(xs[i], cp[i] + 0.15, "γ = %.2f" % gam[i], ha="center", color=GREY)
    ax.set_xticks(xs); ax.set_xticklabels(kinds); ax.set_ylim(0, 5.2); panel(ax, "", "C / R", legend=True); ax.grid(axis="x", alpha=0)
    fig.tight_layout()
    return dict(gas=kinds, degrees_of_freedom=f, Cv_over_R=cv, Cp_over_R=cp, gamma=gam), fig

@figure(C, "p1-c6-mfp", "c6", "Mean free path of nitrogen against pressure",
        "$\\lambda=kT/(\\sqrt2\\,\\pi d^2p)$ with $d=3.7\\times10^{-10}\\,\\mathrm{m}$ at $300\\,\\mathrm{K}$: inversely proportional to the pressure (slope $-1$ on log-log axes), about $67\\,\\mathrm{nm}$ at one atmosphere and millimetres in a rough vacuum.",
        r"\lambda=\frac{1}{\sqrt2\,\pi d^2\,N/V}=\frac{kT}{\sqrt2\,\pi d^2p}")
def _():
    k, T, d = 1.381e-23, 300.0, 3.7e-10; p = np.logspace(-3, 5, 81); lam = k * T / (np.sqrt(2) * np.pi * d ** 2 * p)
    slope = np.polyfit(np.log10(p), np.log10(lam), 1)[0]; close(slope, -1.0, rel=1e-9, what="slope -1"); lam_atm = k * T / (np.sqrt(2) * np.pi * d ** 2 * 101325.0); close(lam_atm, 6.7e-8, rel=0.02, what="1 atm value")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.loglog(p, lam, color=NAVY); ax.plot([101325.0], [lam_atm], "o", color=RED); ax.annotate("1 atm: %.0f nm" % (lam_atm * 1e9), (101325.0 / 40, lam_atm * 3), color=RED)
    panel(ax, "pressure p (Pa)", "mean free path λ (m)")
    fig.tight_layout()
    return dict(p_Pa=p, mean_free_path_m=lam), fig

# =============================================================================================== chapter 7: entropy and the second law
@figure(C, "p1-c7-carnot-eff", "c7", "Efficiency of a Carnot engine",
        "$\\eta=1-T_c/T_h$ depends only on the two reservoir temperatures: it falls linearly with $T_c/T_h$, and for $T_c=300\\,\\mathrm{K}$ it rises with $T_h$ but can never reach $1$. For $500\\,\\mathrm{K}$ and $300\\,\\mathrm{K}$ it is $40\\,\\%$.",
        r"\eta_C=1-\frac{T_c}{T_h}=\frac{W}{Q_h}")
def _():
    r = np.linspace(0, 1, 101); Th = np.linspace(300, 1500, 121); eta_r = 1 - r; eta_T = 1 - 300.0 / Th
    close(1 - 300.0 / 500.0, 0.4, what="40 %"); assert np.all(eta_T < 1)
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8))
    ax[0].plot(r, eta_r * 100, color=NAVY); panel(ax[0], "T_c / T_h", "efficiency (%)"); ax[1].plot(Th, eta_T * 100, color=RED); ax[1].plot([500], [40], "ko"); ax[1].annotate("500 K → 40 %", (520, 36), color=RED); panel(ax[1], "T_h (K)  with T_c = 300 K", "efficiency (%)")
    fig.tight_layout()
    return dict(Th_K=Th, Tc_over_Th=300.0 / Th, efficiency=eta_T), fig

@figure(C, "p1-c7-carnot-cycle", "c7", "The Carnot cycle on a p-V diagram",
        "One mole of a monatomic gas between $500\\,\\mathrm{K}$ and $300\\,\\mathrm{K}$: isothermal expansion A→B (heat $Q_h$ in), adiabatic expansion B→C, isothermal compression C→D (heat $Q_c$ out), adiabatic compression D→A. The enclosed area is the work, and $W/Q_h=1-T_c/T_h=0.40$.",
        r"Q_h=nRT_h\ln\frac{V_B}{V_A},\quad Q_c=nRT_c\ln\frac{V_C}{V_D},\quad W=Q_h-Q_c")
def _():
    n, R, g, Th, Tc = 1.0, 8.314, 5 / 3, 500.0, 300.0; VA, VB = 0.010, 0.020; k = 1 / (g - 1); VC, VD = VB * (Th / Tc) ** k, VA * (Th / Tc) ** k
    pA = n * R * Th / VA; pB = n * R * Th / VB; pC = n * R * Tc / VC; pD = n * R * Tc / VD
    close(pB * VB ** g, pC * VC ** g, what="adiabat B-C"); close(pD * VD ** g, pA * VA ** g, what="adiabat D-A closes the cycle")
    s = np.linspace(0, 1, 101); V_AB = VA + (VB - VA) * s; V_BC = VB + (VC - VB) * s; V_CD = VC + (VD - VC) * s; V_DA = VD + (VA - VD) * s
    p_AB = n * R * Th / V_AB; p_BC = pB * (VB / V_BC) ** g; p_CD = n * R * Tc / V_CD; p_DA = pD * (VD / V_DA) ** g
    W = trap(p_AB, V_AB) + trap(p_BC, V_BC) + trap(p_CD, V_CD) + trap(p_DA, V_DA)
    Qh = n * R * Th * np.log(VB / VA); Qc = n * R * Tc * np.log(VC / VD); close(W, Qh - Qc, rel=1e-4, what="W = Qh - Qc"); close(W / Qh, 1 - Tc / Th, rel=1e-4, what="efficiency")
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for V, p, col, lab in ((V_AB, p_AB, RED, "A→B isotherm 500 K"), (V_BC, p_BC, ORANGE, "B→C adiabat"), (V_CD, p_CD, NAVY, "C→D isotherm 300 K"), (V_DA, p_DA, CYAN, "D→A adiabat")): ax.plot(V * 1e3, p / 1e3, color=col, label=lab)
    for (V, p, lab, dx, dy) in ((VA, pA, "A", -1.0, 18), (VB, pB, "B", 0.6, 10), (VC, pC, "C", 0.6, 8), (VD, pD, "D", -1.6, -22)): ax.plot([V * 1e3], [p / 1e3], "ko"); ax.annotate(lab, (V * 1e3 + dx, p / 1e3 + dy))
    ax.text(26, 360, "Q_h = %.0f J\nQ_c = %.0f J\nW = %.0f J\nη = %.2f" % (Qh, Qc, W, W / Qh), fontsize=10); panel(ax, "V (L)", "p (kPa)", legend=True); ax.legend(frameon=False, fontsize=9, loc="upper right")
    fig.tight_layout()
    return dict(V_AB_m3=V_AB, p_AB_Pa=p_AB, V_BC_m3=V_BC, p_BC_Pa=p_BC, V_CD_m3=V_CD, p_CD_Pa=p_CD, V_DA_m3=V_DA, p_DA_Pa=p_DA), fig

@figure(C, "p1-c7-entropy", "c7", "Entropy change when water is heated",
        "Heating $1\\,\\mathrm{kg}$ of water from $280$ to $360\\,\\mathrm{K}$: $\\Delta S=mc\\ln(T_2/T_1)=1052\\,\\mathrm{J/K}$. On the $T$-$S$ diagram the area under the curve is the heat absorbed, $mc\\,\\Delta T=335\\,\\mathrm{kJ}$.",
        r"\Delta S=\int\frac{dQ}{T}=mc\ln\frac{T_2}{T_1},\qquad Q=\int T\,dS")
def _():
    m, c = 1.0, 4186.0; T = np.linspace(280, 360, 161); S = m * c * np.log(T / T[0]); dS = trap(m * c / T, T)
    close(dS, m * c * np.log(360 / 280), rel=1e-6, what="Delta S"); close(trap(T, S), m * c * 80.0, rel=1e-4, what="area under the T-S curve = Q")
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.8))
    ax[0].plot(T, S, color=NAVY); panel(ax[0], "T (K)", "S − S(280 K)  (J/K)"); ax[0].annotate("ΔS = %.0f J/K" % dS, (292, 900), color=NAVY)
    ax[1].plot(S, T, color=RED); ax[1].fill_betweenx(T, 0, S, color=RED, alpha=0.12); panel(ax[1], "S − S(280 K)  (J/K)", "T (K)"); ax[1].annotate("area = Q = 335 kJ", (130, 305), color=RED)
    fig.tight_layout()
    return dict(T_K=T, S_JK=S), fig

@figure(C, "p1-c7-cop", "c7", "Refrigerator and heat-pump coefficients of performance",
        "For a Carnot refrigerator $K=T_c/(T_h-T_c)$ and for a heat pump $K=T_h/(T_h-T_c)=K_{\\rm fridge}+1$ (room at $T_h=300\\,\\mathrm{K}$). Both blow up as $T_c\\to T_h$: moving heat across a small temperature difference is cheap.",
        r"K_{\rm fridge}=\frac{Q_c}{W}=\frac{T_c}{T_h-T_c},\qquad K_{\rm pump}=\frac{Q_h}{W}=\frac{T_h}{T_h-T_c}")
def _():
    Th = 300.0; Tc = np.linspace(200, 295, 96); Kf = Tc / (Th - Tc); Kh = Th / (Th - Tc); close(Kh, Kf + 1, what="K_pump = K_fridge + 1")
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); ax.semilogy(Tc, Kf, color=NAVY, label="refrigerator  T_c/(T_h−T_c)"); ax.semilogy(Tc, Kh, color=RED, label="heat pump  T_h/(T_h−T_c)")
    ax.axvline(250, color=GREY, ls=":"); ax.annotate("T_c = 250 K: K = 5", (252, 1.6), color=GREY); panel(ax, "cold-side temperature T_c (K), with T_h = 300 K", "coefficient of performance K", legend=True)
    fig.tight_layout()
    return dict(Tc_K=Tc, K_refrigerator=Kf, K_heat_pump=Kh), fig
