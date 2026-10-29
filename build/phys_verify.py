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
