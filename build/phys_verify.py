# -*- coding: utf-8 -*-
"""Independent numerical routes used to double-check the closed-form answers of the Physics generators
(ODE integration, numerical quadrature, ray-transfer matrices). None of them shares code with the formulas it checks."""
import math
import numpy as np
from scipy.integrate import solve_ivp, quad

def projectile(v0, theta_deg, h0=0.0, g=9.8, drag=0.0, m=1.0):
    """Numerical flight to the ground y = 0 (launch from height h0). Returns dict(range, time, hmax, vx_end, vy_end, speed_end)."""
    th = math.radians(theta_deg)
    def rhs(t, s):
        x, y, vx, vy = s
        sp = math.hypot(vx, vy)
        return [vx, vy, -drag / m * sp * vx, -g - drag / m * sp * vy]
    def hit(t, s):
        return s[1]
    hit.terminal = True; hit.direction = -1
    sol = solve_ivp(rhs, [0, 1e5], [0, h0, v0 * math.cos(th), v0 * math.sin(th)], events=hit, rtol=1e-11, atol=1e-12, max_step=0.01 if v0 < 100 else 0.5, dense_output=True)
    ts = np.linspace(0, sol.t_events[0][0], 4001)
    ys = sol.sol(ts)[1]
    xe, ye, vxe, vye = sol.y_events[0][0]
    return dict(range=xe, time=sol.t_events[0][0], hmax=float(ys.max()), vx_end=vxe, vy_end=vye, speed_end=math.hypot(vxe, vye))

def vertical_throw(v0, h0=0.0, g=9.8):
    """Numerical vertical throw (up positive). Returns dict(time_to_top, hmax, time_to_ground, v_ground, distance)."""
    def rhs(t, s):
        return [s[1], -g]
    def top(t, s):
        return s[1]
    top.terminal = False; top.direction = -1
    def ground(t, s):
        return s[0]
    ground.terminal = True; ground.direction = -1
    sol = solve_ivp(rhs, [0, 1e4], [h0, v0], events=[top, ground], rtol=1e-12, atol=1e-12, max_step=0.01)
    t_top = sol.t_events[0][0] if len(sol.t_events[0]) else 0.0
    h_top = sol.y_events[0][0][0] if len(sol.t_events[0]) else h0
    t_gr = sol.t_events[1][0]; v_gr = sol.y_events[1][0][1]
    dist = (h_top - h0) + h_top if v0 > 0 else h0
    return dict(t_top=t_top, hmax=h_top, t_ground=t_gr, v_ground=v_gr, distance=dist)

def integrate(f, a, b):
    """Adaptive quadrature (scipy.quad)."""
    return quad(f, a, b, epsabs=1e-13, epsrel=1e-11, limit=200)[0]

def lens_image(f, do):
    """Thin lens by ray-transfer (ABCD) matrices: object at distance do (to the left), focal length f. Returns (di, m)."""
    # propagate do, lens, then solve for the image distance where the ray height is independent of the launch angle (B = 0)
    A1 = np.array([[1, do], [0, 1]])
    L = np.array([[1, 0], [-1 / f, 1]])
    S = L @ A1                                  # object plane -> just after the lens
    # image plane: B of (propagation di) @ S = 0 -> S[0][1] + di * S[1][1] = 0
    di = -S[0][1] / S[1][1]
    T = np.array([[1, di], [0, 1]]) @ S
    return float(di), float(T[0][0])

def mirror_image(f, do):
    """Mirror: same matrices as a lens of focal length f, images in front of the mirror are real (di > 0)."""
    return lens_image(f, do)

def refraction_surface_image(n1, n2, R, do):
    """Single spherical refracting surface (R > 0 when the centre of curvature is on the outgoing side) by ABCD matrices.
    Returns (di, m) with di measured from the vertex on the outgoing side."""
    A1 = np.array([[1, do], [0, 1]])
    P = np.array([[1, 0], [-(n2 - n1) / (n2 * R), n1 / n2]])
    S = P @ A1
    di = -S[0][1] / S[1][1]
    T = np.array([[1, di], [0, 1]]) @ S
    return float(di), float(T[0][0])


# ----------------------------------------------------------------------------- electrostatics (direct integration of Coulomb's law)
def face_flux(q, a, eps0=8.854187817e-12):
    """Electric flux of a point charge q at the centre of a cube of side a through ONE face, by numerical integration of E.dA."""
    from scipy.integrate import dblquad
    k = 1 / (4 * math.pi * eps0)
    f = lambda y, x: k * q * (a / 2) / ((a / 2) ** 2 + x * x + y * y) ** 1.5       # normal component of E on the face z = a/2
    return dblquad(f, -a / 2, a / 2, -a / 2, a / 2, epsabs=1e-12, epsrel=1e-10)[0]

def ball_field(Q, R, r, eps0=8.854187817e-12):
    """Radial field at distance r (on the axis) of a uniformly charged ball (radius R, total charge Q): Coulomb's law integrated over the volume."""
    from scipy.integrate import dblquad
    k = 1 / (4 * math.pi * eps0); rho = Q / (4 / 3 * math.pi * R ** 3)
    def f(s, z):                                              # s: cylindrical radius, z: along the axis; the field point is at z = r
        d2 = s * s + (z - r) ** 2
        return k * rho * 2 * math.pi * s * (r - z) / d2 ** 1.5
    return dblquad(f, -R, R, 0, lambda z: math.sqrt(max(R * R - z * z, 0.0)), epsabs=1e-10, epsrel=1e-7)[0]

def disk_potential(sigma, R, z, eps0=8.854187817e-12):
    """On-axis potential of a uniformly charged disk by integrating rings: V = int k dq / sqrt(s^2 + z^2)."""
    k = 1 / (4 * math.pi * eps0)
    return integrate(lambda s: k * sigma * 2 * math.pi * s / math.sqrt(s * s + z * z), 0, R)


# ----------------------------------------------------------------------------- magnetism
def lorentz_orbit(q, m, v0, B, theta_deg=90.0, periods=1.2):
    """Integrate m dv/dt = q v x B (B along z, E = 0) for a charge launched at theta from B.
    Returns dict(radius, period, pitch): radius of the projected circle (half the largest chord), time of the first return in the x-y plane
    and the advance along z in that time. Uses numerical integration only."""
    th = math.radians(theta_deg)
    v = np.array([v0 * math.sin(th), 0.0, v0 * math.cos(th)])
    wc = abs(q) * B / m
    T0 = 2 * math.pi / wc
    def rhs(t, s):
        vel = s[3:]
        a = q / m * np.cross(vel, np.array([0.0, 0.0, B]))
        return np.concatenate([vel, a])
    sol = solve_ivp(rhs, [0, periods * T0], np.concatenate([[0.0, 0.0, 0.0], v]), rtol=1e-11, atol=1e-14, dense_output=True, max_step=T0 / 400)
    ts = np.linspace(0, periods * T0, 20001)
    P = sol.sol(ts)[:3]
    # projected circle: largest chord = diameter
    xy = P[:2].T
    diam = max(np.linalg.norm(xy[i] - xy[j]) for i in range(0, len(ts), 50) for j in range(0, len(ts), 50))
    d = np.linalg.norm(xy, axis=1)
    k = np.where((ts > 0.5 * T0) & (d < diam * 1e-3 + 1e-9))[0]
    if len(k) == 0:
        k = [int(np.argmin(np.where(ts > 0.5 * T0, d, np.inf)))]
    i = int(k[0]) if len(k) else int(k)
    return dict(radius=diam / 2, period=ts[i], pitch=P[2][i])

def wire_field(path, I, point, mu0=4e-7 * math.pi):
    """Biot-Savart field (3-vector) at `point` of a current I along a polyline `path` (list of 3D points), by summing short segments."""
    P = np.array(point, float); B = np.zeros(3)
    pts = np.array(path, float)
    for a, b in zip(pts[:-1], pts[1:]):
        n = 400
        for t in range(n):
            p0 = a + (b - a) * (t + 0.5) / n
            dl = (b - a) / n
            r = P - p0
            B += mu0 / (4 * math.pi) * I * np.cross(dl, r) / np.linalg.norm(r) ** 3
    return B

def arc_path(R, phi, n=400, z=0.0):
    """Points of a circular arc of radius R and angle phi (radians) centred on the origin in the xy plane, counter-clockwise from +x."""
    return [(R * math.cos(phi * i / n), R * math.sin(phi * i / n), z) for i in range(n + 1)]

def rl_current(emf, R, L, t, I0=0.0):
    """Numerical solution of L dI/dt + R I = emf at time t."""
    sol = solve_ivp(lambda tt, I: [(emf - R * I[0]) / L], [0, t], [I0], rtol=1e-12, atol=1e-14)
    return float(sol.y[0][-1])


# ----------------------------------------------------------------------------- optics
def fermat_refraction(n1, n2, theta1_deg, h1=1.0, h2=1.0):
    """Refracted angle (degrees from the normal) found by minimising the travel time between two fixed points on either side of a plane
    interface (Fermat's principle) - independent of Snell's law. The first point is h1 above the interface and the ray leaves it at theta1."""
    from scipy.optimize import minimize_scalar
    th1 = math.radians(theta1_deg)
    x_end = h1 * math.tan(th1)                                       # where the incident ray hits the interface
    X = x_end + h2 * 0.9                                             # an arbitrary target below the interface; the optimum for this target is found
    f = lambda x: n1 * math.hypot(x, h1) + n2 * math.hypot(X - x, h2)
    x_opt = minimize_scalar(f, bounds=(0, X), method="bounded", options={"xatol": 1e-12}).x
    # for the optimal path: incident angle from x_opt, refracted angle from the second leg; return both
    inc = math.degrees(math.atan2(x_opt, h1)); ref = math.degrees(math.atan2(X - x_opt, h2))
    return inc, ref

def refraction_by_fermat(n1, n2, inc_deg):
    """Refracted angle for a given incident angle by Fermat minimisation: choose the target so that the incident leg has the wanted angle."""
    from scipy.optimize import brentq
    # scan the target position X until the incident angle of the optimal path equals inc_deg
    g = lambda X: _inc_ref(n1, n2, X)[0] - inc_deg
    X = brentq(g, 1e-6, 50.0)
    return _inc_ref(n1, n2, X)[1]

def _inc_ref(n1, n2, X, h1=1.0, h2=1.0):
    from scipy.optimize import minimize_scalar
    f = lambda x: n1 * math.hypot(x, h1) + n2 * math.hypot(X - x, h2)
    x = minimize_scalar(f, bounds=(0, X), method="bounded", options={"xatol": 1e-13}).x
    return math.degrees(math.atan2(x, h1)), math.degrees(math.atan2(X - x, h2))

def slit_intensity(a, lam, theta, n=4001):
    """Single-slit Fraunhofer intensity relative to the centre, by integrating the wavelets across the slit (no sinc formula used)."""
    k = 2 * math.pi / lam
    ys = np.linspace(-a / 2, a / 2, n)
    amp = (getattr(np, "trapezoid", None) or np.trapz)(np.exp(1j * k * ys * math.sin(theta)), ys)
    return float(abs(amp) ** 2 / a ** 2)

def two_slit_intensity(d, lam, theta):
    """Two narrow slits: intensity relative to the maximum, from the phasor sum of the two waves."""
    phi = 2 * math.pi * d * math.sin(theta) / lam
    return float(abs(1 + np.exp(1j * phi)) ** 2 / 4)
