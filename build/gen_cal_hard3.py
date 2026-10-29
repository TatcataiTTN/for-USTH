# -*- coding: utf-8 -*-
"""Calculus I, level-4 pool in the style of the Moodle mock midterm, part 3: slots 12, 13, 16, 19, 20 (related rates, IVT in context, critical points)."""
import sympy as sp
from qlib import tex
from cal_common import E, uniq_by_text
from gen_cal_hard1 import add, agree, vals, L, xr, sin, cos, tan, exp, log, sqrt, pi, R

t = sp.Symbol("t", real=True)

def num(v, k=3):
    """Option such as $2.893\\ \\mathrm{K/min}$ with a unit."""
    return "%.*f" % (k, float(v))

def unit_opts(vs, unit, k=3):
    return uniq_by_text(["$%s\\ \\mathrm{%s}$" % (num(v, k), unit) for v in vs])

def fd(f, t0=0, h=R(1, 10**6)):
    """Central difference of an explicit function of t (second route for related rates)."""
    return (sp.N(f.subs(t, t0 + h), 40) - sp.N(f.subs(t, t0 - h), 40)) / (2 * h)

# ------------------------------------------------------------------------------------------------ slot 12: related rates from a physical law
def s12(B):
    Rg = R(821, 10000)
    for P0, rP, V0, rV, n in ((R(5), R(1, 5), 12, -R(1, 10), 8), (R(12), -R(3, 20), 6, R(1, 4), 5), (R(3), R(1, 10), 20, -R(1, 5), 4)):
        val = (rP * V0 + P0 * rV) / (n * Rg)
        T = (P0 + rP * t) * (V0 + rV * t) / (n * Rg)
        agree(val, fd(T), "s12 gas law")
        wrongs = [rP * V0 / (n * Rg), (rP * V0 - P0 * rV) / (n * Rg), (rP * V0 + P0 * rV) / Rg, -val]
        add(B, "c2", 12, 4, "Related rates", "For an ideal gas $PV=nRT$ with $R=0.0821$. At a certain instant $P=%s$ atm and is changing at $%s$ atm/min, $V=%d$ L and is changing at $%s$ L/min, with $n=%d$ mol. Find the rate of change of the temperature $T$ at that instant." % (
            num(P0, 1), num(rP, 2), V0, num(rV, 2), n), "$%s\\ \\mathrm{K/min}$" % num(val), [w for w in unit_opts(wrongs, "K/min") if w != "$%s\\ \\mathrm{K/min}$" % num(val)],
            "$T=\\dfrac{PV}{nR}$, so by the product rule $\\dfrac{dT}{dt}=\\dfrac{P'V+PV'}{nR}=\\dfrac{(%s)(%d)+(%s)(%s)}{%d(0.0821)}=%s$ K/min. The slips are keeping only one product-rule term, a sign error on the second, or forgetting $n$." % (num(rP, 2), V0, num(P0, 1), num(rV, 2), n, num(val)))
    for r1, r2, d1, d2 in ((80, 100, R(3, 10), R(1, 5)), (30, 60, R(1, 2), R(2, 5)), (20, 30, R(1, 4), R(1, 2))):
        Rt = 1 / (R(1, r1) + R(1, r2))
        val = Rt ** 2 * (R(d1) / r1 ** 2 + R(d2) / r2 ** 2)
        Rfun = 1 / (1 / (r1 + d1 * t) + 1 / (r2 + d2 * t))
        agree(val, fd(Rfun), "s12 resistors")
        wrongs = [d1 + d2, (d1 + d2) / 2, R(d1) * d2 / (d1 + d2), Rt * (R(d1) / r1 + R(d2) / r2)]
        add(B, "c2", 12, 4, "Related rates", "Two resistors $R_1=%d\\ \\Omega$ and $R_2=%d\\ \\Omega$ are connected in parallel, so $\\dfrac1R=\\dfrac1{R_1}+\\dfrac1{R_2}$. $R_1$ increases at $%s\\ \\Omega/\\mathrm{s}$ and $R_2$ at $%s\\ \\Omega/\\mathrm{s}$. How fast is $R$ changing?" % (r1, r2, num(d1, 2), num(d2, 2)),
            "$%s\\ \\Omega/\\mathrm{s}$" % num(val), [w for w in unit_opts(wrongs, "\\Omega/s") if w != "$%s\\ \\Omega/\\mathrm{s}$" % num(val)],
            "Differentiate $\\frac1R=\\frac1{R_1}+\\frac1{R_2}$: $-\\dfrac{R'}{R^2}=-\\dfrac{R_1'}{R_1^2}-\\dfrac{R_2'}{R_2^2}$, so $R'=R^2\\left(\\dfrac{R_1'}{R_1^2}+\\dfrac{R_2'}{R_2^2}\\right)$ with $R=%s$. Result: %s $\\Omega$/s. The factor $R^2$ is the one that is usually forgotten." % (num(Rt, 3), num(val)))
    # conical tank
    for rad, hgt, flow, depth in ((3, 6, 4, 2), (2, 8, 5, 4), (4, 8, 6, 3)):
        h = sp.Symbol("h", positive=True)
        V = sp.pi / 3 * (R(rad, hgt) * h) ** 2 * h
        val = flow / sp.diff(V, h).subs(h, depth)
        agree(val, sp.N(flow / (sp.pi * (R(rad, hgt) * depth) ** 2), 30), "s12 cone")
        wrongs = [flow / (sp.pi * rad ** 2), flow / sp.diff(V, h).subs(h, hgt), flow / (sp.pi * R(rad, hgt) * depth ** 2), 4 * val, val / 2, 2 * val]
        add(B, "c2", 12, 4, "Related rates", "Water is poured at $%d\\ \\mathrm{m^3/min}$ into a conical tank with its vertex down, top radius $%d$ m and height $%d$ m. How fast is the water level rising when the depth is $%d$ m?" % (flow, rad, hgt, depth),
            "$%s\\ \\mathrm{m/min}$" % num(val), [w for w in unit_opts(wrongs, "m/min") if w != "$%s\\ \\mathrm{m/min}$" % num(val)],
            "At depth $h$ the water surface has radius $r=\\dfrac{%d}{%d}h$ (similar triangles), so $V=\\frac13\\pi r^2h=\\dfrac{\\pi}{3}\\left(\\dfrac{%d}{%d}\\right)^2h^3$ and $\\dfrac{dV}{dt}=\\pi\\left(\\dfrac{%d}{%d}\\right)^2h^2\\dfrac{dh}{dt}$. At $h=%d$: $\\dfrac{dh}{dt}=%s$ m/min. The trap is to use the fixed top radius instead of $r(h)$." % (rad, hgt, rad, hgt, rad, hgt, depth, num(val)))
    # shadows: the tip moves faster than the person, the length grows slower
    for lamp, man, speed in ((5, R(9, 5), R(6, 5)), (6, 2, 1), (8, R(3, 2), R(4, 5))):
        tip = speed * lamp / (lamp - man); length = speed * man / (lamp - man)
        assert tip - length == speed
        add(B, "c2", 12, 4, "Related rates", "A person %s m tall walks away from a street lamp %s m high at %s m/s. How fast does the **tip of the shadow** move along the ground?" % (num(man, 1).rstrip("0").rstrip("."), num(lamp, 0), num(speed, 1).rstrip("0").rstrip(".")),
            "$%s\\ \\mathrm{m/s}$" % num(tip), unit_opts([length, speed, tip + length], "m/s"),
            "Similar triangles give $\\dfrac{%s}{s}=\\dfrac{%s}{s-x}$, where $x$ is the person's distance from the lamp and $s$ the distance of the shadow tip: $s=\\dfrac{%s}{%s}x$, so $s'=%s\\times%s=%s$ m/s. The **length** of the shadow grows at only %s m/s (the tip minus the person); the tip is always faster than the person." % (
                num(lamp, 0), num(man, 1), num(lamp, 0), num(lamp - man, 1), num(lamp / (lamp - man), 3), num(speed, 1), num(tip), num(length)))
        add(B, "c2", 12, 4, "Related rates", "A person %s m tall walks away from a street lamp %s m high at %s m/s. How fast is the **length of the shadow** increasing?" % (num(man, 1).rstrip("0").rstrip("."), num(lamp, 0), num(speed, 1).rstrip("0").rstrip(".")),
            "$%s\\ \\mathrm{m/s}$" % num(length), unit_opts([tip, speed, length * 2, length + speed, length / 2], "m/s"),
            "With the shadow of length $\\ell$ and distance $x$: $\\dfrac{\\ell}{%s}=\\dfrac{x+\\ell}{%s}$, so $\\ell=\\dfrac{%s}{%s}x$ and $\\ell'=%s\\times%s=%s$ m/s. Do not confuse it with the speed of the tip of the shadow (%s m/s)." % (
                num(man, 1), num(lamp, 0), num(man, 1), num(lamp - man, 1), num(man / (lamp - man), 3), num(speed, 1), num(length), num(tip)))
    # Boyle's law
    for P, V, rV in ((150, 40, -2), (80, 25, -1), (200, 50, -4)):
        val = -R(P) * rV / V
        Pf = R(P) * V / (V + rV * t)
        agree(val, fd(Pf), "s12 Boyle")
        add(B, "c2", 12, 3, "Related rates", "A gas obeys Boyle's law $PV=C$ (constant temperature). At one instant $V=%d$ L, $P=%d$ kPa and the volume is decreasing at $%d$ L/min. How fast is the pressure changing?" % (V, P, -rV),
            "$%s\\ \\mathrm{kPa/min}$" % num(val, 2), unit_opts([-val, val / 2, val * 2], "kPa/min", 2),
            "$P=C/V$, so $\\dfrac{dP}{dt}=-\\dfrac{C}{V^2}\\dfrac{dV}{dt}=-\\dfrac{P}{V}\\dfrac{dV}{dt}=-\\dfrac{%d}{%d}(%d)=%s$ kPa/min: positive, because compressing a gas raises its pressure." % (P, V, rV, num(val, 2)))

# ------------------------------------------------------------------------------------------------ slot 13: the IVT in a modelling context (which interval contains the solution?)
def s13(B):
    cases = [   # f(t), target, statement, candidate intervals (the first is the correct one)
        (500 - 20 * sqrt(t), 410, "A leaking tank holds $V(t)=500-20\\sqrt t$ litres, $t\\ge0$ minutes. In which interval is it guaranteed that the tank holds **exactly** $410$ litres at some time?", [(16, 25), (25, 36), (0, 16), (9, 16)]),
        (20 + 80 * exp(-t / 10), 50, "A cup of tea cools according to $T(t)=20+80e^{-t/10}$ degrees after $t$ minutes. In which interval is the temperature guaranteed to reach exactly $50$ degrees?", [(9, 10), (0, 5), (5, 9), (10, 15)]),
        (1000 * 2 ** (t / 3), 3000, "A population is $P(t)=1000\\cdot2^{t/3}$ after $t$ hours. In which interval is it guaranteed that the population is exactly $3000$ at some time?", [(4, 5), (0, 2), (2, 4), (5, 7)]),
        (10 - 2 * sqrt(t), 7, "The depth of water in a draining tank is $h(t)=10-2\\sqrt t$ metres, $t\\ge0$ minutes. In which interval is the depth guaranteed to be exactly $7$ metres at some time?", [(2, 3), (0, 1), (1, 2), (3, 4)]),
        (5 + 95 * exp(-t / 20), 35, "An object cools according to $T(t)=5+95e^{-t/20}$ degrees. In which interval is the temperature guaranteed to be exactly $35$ degrees at some time?", [(20, 25), (10, 15), (15, 20), (25, 30)]),
    ]
    for f, target, stem, ivs in cases:
        root = sp.nsolve(f - target, t, ivs[0][0] + 1)
        assert ivs[0][0] < root < ivs[0][1]
        brackets = [(float(f.subs(t, a)) - target) * (float(f.subs(t, b)) - target) < 0 for a, b in ivs]
        assert brackets == [True, False, False, False], "s13 brackets"
        def iv(a, b):
            return "$(%d,%d)$" % (a, b)
        add(B, "c1", 13, 4, "Intermediate Value Theorem", stem, iv(*ivs[0]), [iv(*i) for i in ivs[1:]],
            "$f$ is continuous, so the IVT applies on $[a,b]$ when the target lies **between** $f(a)$ and $f(b)$. Here $f(%d)=%.2f$ and $f(%d)=%.2f$ bracket %d, whereas the other intervals have both endpoint values on the same side of %d. (The actual time is $t\\approx%.2f$.)" % (
                ivs[0][0], float(f.subs(t, ivs[0][0])), ivs[0][1], float(f.subs(t, ivs[0][1])), target, target, float(root)))

# ------------------------------------------------------------------------------------------------ slot 16: related rates with two moving objects
def s16(B):
    # police car 0.5 km north moving south at 80 km/h, speeding car 1.2 km east, the distance grows at 40 km/h
    x0, y0, vy, sp_ = R(6, 5), R(1, 2), -80, 40
    s0 = sqrt(x0 ** 2 + y0 ** 2)
    val = (s0 * sp_ - y0 * vy) / x0
    X = x0 + val * t; Y = y0 + vy * t
    agree(sp.diff(sqrt(X ** 2 + Y ** 2), t).subs(t, 0), sp_, "s16 police")
    add(B, "c2", 16, 4, "Related rates", "A police car is $0.5$ km north of an intersection and moves south at $80$ km/h. A speeding car is $1.2$ km east of the same intersection and moves east. The distance between the cars is increasing at $40$ km/h. How fast is the eastbound car moving?",
        "$%s\\ \\mathrm{km/h}$" % num(val, 1), unit_opts([(s0 * sp_ + y0 * vy) / x0, sp_, (s0 * sp_) / x0, 120], "km/h", 1),
        "$s^2=x^2+y^2$ gives $s\\,s'=x\\,x'+y\\,y'$. With $s=1.3$, $y'=-80$ (the police car **approaches** the intersection): $1.3\\cdot40=1.2\\,x'+0.5(-80)$, so $x'=\\dfrac{52+40}{1.2}=%s$ km/h. A sign error on $y'$ gives the wrong value." % num(val, 1))
    # ladder: 13 m, top sliding down at 2 m/s, foot 5 m from the wall
    val = -12 * R(-2) / 5
    add(B, "c2", 16, 4, "Related rates", "A $13$ m ladder leans against a vertical wall. The top slides down the wall at $2$ m/s. How fast is the foot of the ladder moving away from the wall when the foot is $5$ m from the wall?",
        "$4.8\\ \\mathrm{m/s}$", unit_opts([2, 2.4, 0.8], "m/s", 1),
        "$x^2+y^2=169$ gives $x\\,x'+y\\,y'=0$. At $x=5$ we have $y=12$, so $x'=-\\dfrac{y\\,y'}{x}=-\\dfrac{12(-2)}{5}=4.8$ m/s (the foot is faster than the top because it is close to the wall).")
    # two boats leaving the same dock
    val = sp.Integer(50)
    add(B, "c2", 16, 4, "Related rates", "Two boats leave a dock at the same time: one goes north at $30$ km/h and the other east at $40$ km/h. How fast is the distance between them increasing $2$ hours later?",
        "$50\\ \\mathrm{km/h}$", unit_opts([70, 35, 100], "km/h", 0),
        "After $t$ hours $x=40t$, $y=30t$, $s=50t$, so $s'=50$ km/h at every moment (also by $s\\,s'=xx'+yy'$: $\\dfrac{80\\cdot40+60\\cdot30}{100}=50$). Adding the speeds ($70$) is the classic mistake.")
    # aircraft over a radar station
    val = R(8) * 400 / 10
    add(B, "c2", 16, 4, "Related rates", "A plane flies horizontally at an altitude of $6$ km at $400$ km/h and passes directly above a radar station. How fast is the distance from the station to the plane increasing when the plane is $8$ km (horizontally) past the station?",
        "$320\\ \\mathrm{km/h}$", unit_opts([400, 240, 500], "km/h", 0),
        "$s^2=x^2+6^2$ gives $s\\,s'=x\\,x'$. At $x=8$: $s=10$, so $s'=\\dfrac{8\\cdot400}{10}=320$ km/h. It is **less** than $400$ because part of the plane's motion is perpendicular to the line of sight.")
    # balloon rising
    add(B, "c2", 16, 4, "Related rates", "A balloon rises vertically at $3$ m/s from a point $40$ m from an observer on the ground. How fast is the distance between the observer and the balloon increasing when the balloon is $30$ m high?",
        "$1.8\\ \\mathrm{m/s}$", unit_opts([3, 2.4, 1.2], "m/s", 1),
        "$s^2=40^2+y^2$ gives $s\\,s'=y\\,y'$. At $y=30$: $s=50$, so $s'=\\dfrac{30\\cdot3}{50}=1.8$ m/s.")

# ------------------------------------------------------------------------------------------------ slot 19: the IVT sign-change test
def s19(B):
    cases = [   # f, candidate intervals (correct first)
        (xr ** 3 + xr - 5, [(1, 2), (2, 3), (-1, 0), (0, 1)]),
        (cos(xr) - xr ** 2, [(0, 1), (1, 2), (2, 3), (R(-1, 2), R(1, 2))]),
        (log(xr) + xr - 3, [(2, 3), (1, 2), (3, 4), (R(1, 2), 1)]),
        (xr * exp(xr) - 2, [(0, 1), (1, 2), (-2, -1), (-1, 0)]),
        (xr ** 5 + xr - 1, [(0, 1), (1, 2), (-1, 0), (-2, -1)]),
    ]
    for f, ivs in cases:
        sign = [float(f.subs(xr, a)) * float(f.subs(xr, b)) < 0 for a, b in ivs]
        assert sign == [True, False, False, False], "s19 sign %s" % f
        for a, b in ivs[1:]:                                             # no root at all in the wrong intervals (no ambiguity)
            samples = [float(f.subs(xr, a + (b - a) * R(k, 40))) for k in range(0, 41)]
            assert min(samples) > 0 or max(samples) < 0, "s19 root in a wrong interval %s" % f
        iv = lambda a, b: "$(%s,%s)$" % (tex(sp.nsimplify(a)), tex(sp.nsimplify(b)))
        add(B, "c1", 19, 4, "Intermediate Value Theorem", "Which interval is guaranteed by the Intermediate Value Theorem to contain a solution of $%s=0$?" % tex(f), iv(*ivs[0]), [iv(*i) for i in ivs[1:]],
            "$f(x)=%s$ is continuous where it is defined. The IVT needs a sign change: $f(%s)=%.3f$ and $f(%s)=%.3f$ have opposite signs, while the other intervals have both endpoint values of the same sign." % (tex(f), tex(sp.nsimplify(ivs[0][0])), float(f.subs(xr, ivs[0][0])), tex(sp.nsimplify(ivs[0][1])), float(f.subs(xr, ivs[0][1]))))

# ------------------------------------------------------------------------------------------------ slot 20: critical points of x^p (c - x)
def s20(B):
    xp = sp.Symbol("x", positive=True)
    cases = [   # exponent p (denominator odd: f is defined for negative x as well), c, reasoning
        (R(4, 3), 3, "$f'(x)=\\frac43x^{1/3}(3-x)-x^{4/3}=x^{1/3}\\left(4-\\frac73x\\right)$ is defined everywhere and vanishes at $x=0$ and $x=\\frac{12}7$."),
        (R(2, 3), 5, "$f'(x)=\\frac23x^{-1/3}(5-x)-x^{2/3}=x^{-1/3}\\left(\\frac{10}3-\\frac53x\\right)$ vanishes at $x=2$ and is **undefined** at $x=0$ (where $f$ is defined), so both are critical."),
        (R(5, 3), 4, "$f'(x)=\\frac53x^{2/3}(4-x)-x^{5/3}=x^{2/3}\\left(\\frac{20}3-\\frac83x\\right)$ vanishes at $x=0$ and $x=\\frac52$."),
        (R(1, 3), 8, "$f'(x)=\\frac13x^{-2/3}(8-x)-x^{1/3}=x^{-2/3}\\left(\\frac83-\\frac43x\\right)$ vanishes at $x=2$ and is undefined at $x=0$."),
    ]
    for p_, c, why in cases:
        fp = sp.diff(xp ** p_ * (c - xp), xp)                        # for x>0; the odd-root extension to x<0 has the same formula
        roots = [r for r in sp.solve(fp, xp) if r.is_positive]
        assert roots == [p_ * c / (p_ + 1)], "s20 root"
        at0 = sp.limit(fp, xp, 0, "+")
        assert (at0 == sp.oo) == (p_ < 1) and (at0 == 0) == (p_ > 1), "s20 behaviour at 0"
        h = R(1, 10**6); z = roots[0]
        f = lambda v: v ** p_ * (c - v)
        agree((f(z + h) - f(z - h)) / (2 * h), 0, "s20 flat at the root", 1e-6)
        z2 = tex(z)
        correct = "$x=0$ and $x=%s$" % z2
        add(B, "c3", 20, 4, "Extreme values", "Find the critical points of $f(x)=%s\\,(%d-x)$." % ("\\sqrt[%d]{x}" % p_.q if p_.p == 1 else "\\sqrt[%d]{x^{%d}}" % (p_.q, p_.p), c), correct, ["$x=%s$ only" % z2, "$x=0$ only", "$x=%s$ and $x=%d$" % (z2, c)],
            "%s A critical point is an interior point where $f'=0$ **or** $f'$ does not exist. Dropping the point where $f'$ is undefined, or the point where it vanishes through a factor $x^k$, is the usual mistake." % why)
    # domain [0, oo): the endpoint x=0 is not an interior point
    fp = sp.diff(xp ** R(3, 2) * (5 - xp), xp)
    assert sorted(sp.solve(fp, xp)) == [0, 3] if sp.solve(fp, xp)[0] == 0 else sorted(sp.solve(fp, xp)) == [3]
    add(B, "c3", 20, 4, "Extreme values", "Find the critical points of $f(x)=x^{3/2}(5-x)$ (its domain is $[0,\\infty)$).", "$x=3$ only", ["$x=0$ and $x=3$", "$x=0$ only", "$x=0$, $x=3$ and $x=5$"],
        "$f'(x)=\\frac32x^{1/2}(5-x)-x^{3/2}=x^{1/2}\\left(\\frac{15}2-\\frac52x\\right)$ vanishes at $x=0$ and $x=3$. But $x=0$ is an **endpoint** of the domain, not an interior point, so it is not a critical point (it is only a candidate for the absolute extrema). The only critical point is $x=3$.")

def build_part3(B):
    for fn in (s12, s13, s16, s19, s20):
        fn(B)
