# -*- coding: utf-8 -*-
"""Physics I (PHY1.001) - Mechanics: chapter 1 Kinematics and chapter 2 Dynamics.
Sources: Mechanics tutorial Part 1 (kinematics), Part 2 (free fall, projectiles, relative motion), Part 3 (dynamics), Lectures 1-3."""
import math
from phys_common import *
from phys_verify import projectile, vertical_throw
import figs

P1 = "Mechanics tutorial Part 1"
P2 = "Mechanics tutorial Part 2"
P3 = "Mechanics tutorial Part 3"
GEN = lambda s: "Generated, same style as: " + s

# =============================================================================================== chapter 1 - kinematics
def ch1(B):
    c = "c1"
    # ---------------------------------------------------------------- displacement, distance, velocity
    mcq_num(B, c, "Displacement and distance", 1, "A man walks 8 m to the east and then 6 m to the south. What is his eastward displacement?",
            8, [6, 14, 2, 10], "m", ex("The eastward displacement is the east component of the total displacement: only the 8 m walked east counts; the 6 m south has no east component.",
                                          "Eastward displacement $=8\\,\\mathrm{m}$."), P1 + ", Q1", sig=2)
    d = math.hypot(8, 6); check(d, math.sqrt(8 ** 2 + 6 ** 2))
    mcq_num(B, c, "Displacement and distance", 1, "A man walks 8 m to the east and then 6 m to the south. What is the magnitude of his total displacement from the start?",
            d, [14, 8, 6, 7], "m", ex("Displacement is the straight line from start to end: $\\sqrt{8^2+6^2}=\\sqrt{100}=10\\,\\mathrm{m}$.", "The path length (distance) is $8+6=14\\,\\mathrm{m}$, which is a different quantity."), GEN(P1 + ", Q1"), "gen", sig=2)
    ang = math.degrees(math.atan2(6, 8))
    mcq_num(B, c, "Displacement and distance", 2, "A man walks 8 m to the east and then 6 m to the south. The total displacement points south of east by an angle of",
            ang, [53.1, 45.0, 30.0, 63.4], "deg", ex("$\\tan\\theta=\\dfrac{6}{8}$, so $\\theta=\\arctan 0.75=36.9^\\circ$ south of east.", "$53.1^\\circ$ is the angle from the south direction (the complement)."),
            GEN(P1 + ", Q1"), "gen", sig=3)
    # the distance/displacement of a round trip
    mcq_text(B, c, "Displacement and distance", 1, "A runner completes exactly one lap of a 400 m track in 80 s. Her average velocity for the lap and her average speed are",
             "average velocity $0$, average speed $5\\,\\mathrm{m/s}$", ["average velocity $5\\,\\mathrm{m/s}$, average speed $5\\,\\mathrm{m/s}$", "average velocity $5\\,\\mathrm{m/s}$, average speed $0$", "average velocity $0$, average speed $0$"],
             ex("Displacement for a full lap is $0$, so average velocity $=0/80=0$.", "Distance is $400\\,\\mathrm{m}$, so average speed $=400/80=5\\,\\mathrm{m/s}$."), "Lecture 1 (position, displacement, distance)", "concept")
    mcq_pick(B, c, "Speed and velocity", 1, "For a particle accelerating along a straight line, what is the definition of its velocity?",
             ["Velocity is displacement divided by time", "Velocity is distance divided by time", "Velocity is the rate of change of displacement", "Velocity is the rate of change of distance"], 2,
             ex("Instantaneous velocity is $v=\\mathrm{d}x/\\mathrm{d}t$: the rate of change of displacement.", "'Displacement divided by time' is only the average velocity over an interval, and anything built on distance is a speed."),
             P1 + ", Q8", "src")
    mcq_pick(B, c, "Graphs of motion", 1, "Which of the following gives the acceleration of a body?",
             ["the area under its displacement-time graph", "the area under its velocity-time graph", "the gradient of its displacement-time graph", "the gradient of its velocity-time graph"], 3,
             ex("$a=\\mathrm{d}v/\\mathrm{d}t$ is the gradient (slope) of the velocity-time graph.", "The gradient of the displacement-time graph is the velocity, and the area under the velocity-time graph is the displacement."),
             P1 + ", Q9", "src")
    # ---------------------------------------------------------------- uniform acceleration (tutorial numbers)
    a, t = 5.0, 10.0
    v = a * t; check(v, math.sqrt(2 * a * (0.5 * a * t * t)))
    mcq_num(B, c, "Uniform acceleration", 1, "A car accelerates at $5\\,\\mathrm{m/s^2}$ from rest for $10\\,\\mathrm{s}$. What is its speed at the end of the $10\\,\\mathrm{s}$?",
            v, [25, 0.5, 250, 15], "m/s", ex("$v=u+at=0+5\\times10=50\\,\\mathrm{m/s}$.", "$25\\,\\mathrm{m/s}$ is the average speed and $250\\,\\mathrm{m}$ would be the distance $\\tfrac12at^2$: do not mix them up."), P1 + ", Q2", sig=2)
    u, v2, s = 10.0, 20.0, 100.0
    a = (v2 ** 2 - u ** 2) / (2 * s); check(a, (v2 - u) / (2 * s / (u + v2)))
    mcq_num(B, c, "Uniform acceleration", 2, "A racing car accelerates uniformly along a straight road. Marker posts are $100\\,\\mathrm{m}$ apart. The car passes one post at $10\\,\\mathrm{m/s}$ and the next at $20\\,\\mathrm{m/s}$. What is its acceleration?",
            a, [0.67, 2.5, 6.0, 0.1], "m/s^2", ex("No time is given, so use $v^2=u^2+2as$:", "$a=\\dfrac{v^2-u^2}{2s}=\\dfrac{400-100}{200}=1.5\\,\\mathrm{m/s^2}$.", "Check with the time: average speed $15\\,\\mathrm{m/s}$, $t=100/15=6.67\\,\\mathrm{s}$, $a=10/6.67=1.5\\,\\mathrm{m/s^2}$."), P1 + ", Q3", sig=2)
    v_imp = 9.8 * 1.0; d = 8.0e-3
    a = v_imp ** 2 / (2 * d); t_sand = 2 * d / v_imp; check(a, v_imp / t_sand)       # second route: stopping time of the average speed v/2
    mcq_num(B, c, "Free fall", 3, "A metal ball hits a sand bed one second after it is released from rest and makes an impression $8.0\\,\\mathrm{mm}$ deep. Air resistance is negligible. What is the average deceleration of the ball in the sand?",
            a, [a * 2, a / 10, a * 2 / 10, a * 4], "m/s^2", ex("Impact speed after $1\\,\\mathrm{s}$ of free fall: $v=gt=9.8\\,\\mathrm{m/s}$.", "In the sand $v^2=2ad$ with $d=8.0\\times10^{-3}\\,\\mathrm{m}$: $a=\\dfrac{9.8^2}{2\\times0.008}=6.0\\times10^3\\,\\mathrm{m/s^2}$.", "Forgetting the factor 2 gives $1.2\\times10^4$."), P1 + ", Q4", sig=2)
    u, a, t = 40.0, -5.0, 6.0
    v = u + a * t
    mcq_num(B, c, "Uniform acceleration", 1, "A car decelerates at $5\\,\\mathrm{m/s^2}$ from an initial speed of $40\\,\\mathrm{m/s}$. What is its speed after $6\\,\\mathrm{s}$?",
            v, [8, 29, 35, 70], "m/s", ex("$v=u+at=40-5\\times6=10\\,\\mathrm{m/s}$ (the car is still moving: it stops only after $8\\,\\mathrm{s}$)."), P1 + ", Q5", sig=2)
    f = 2.0 / 0.50
    mcq_num(B, c, "Speed and velocity", 1, "A car with a hole in its petrol tank loses a drop of petrol at a constant rate. The car travels at constant speed $2\\,\\mathrm{m/s}$ and the gap between two drops on the road is $50\\,\\mathrm{cm}$. What is the frequency of the drips?",
            f, [0.25, 8, 25, 1.0], "Hz", ex("Time between drops $T=\\dfrac{d}{v}=\\dfrac{0.50}{2}=0.25\\,\\mathrm{s}$, so $f=1/T=4\\,\\mathrm{Hz}$.", "Remember to convert $50\\,\\mathrm{cm}=0.50\\,\\mathrm{m}$."), P1 + ", Q7", sig=2)
    # ball thrown up, distance in 5 s (g = 10)
    v0, g_, t = 30.0, 10.0, 5.0
    t_up = v0 / g_; h = v0 ** 2 / (2 * g_); down = 0.5 * g_ * (t - t_up) ** 2
    dist = h + down; disp = v0 * t - 0.5 * g_ * t * t
    vt = vertical_throw(v0, 0.0, g_); check(vt["hmax"], h); check(h - down, disp)
    mcq_num(B, c, "Free fall", 2, "A robot shoots a ball vertically upwards at $30\\,\\mathrm{m/s}$. What distance does the ball travel in the first $5\\,\\mathrm{s}$? ($g=10\\,\\mathrm{m/s^2}$)",
            dist, [disp, h, 75, 55], "m", ex("It rises for $t=v_0/g=3\\,\\mathrm{s}$ to $h=v_0^2/2g=45\\,\\mathrm{m}$, then falls for $2\\,\\mathrm{s}$: $\\tfrac12g(2)^2=20\\,\\mathrm{m}$.", "Distance travelled $=45+20=65\\,\\mathrm{m}$; the displacement is only $45-20=25\\,\\mathrm{m}$ above the start."), P1 + ", Q14", sig=2)
    # runner: 2 m/s^2 for 4 s then constant speed, 100 m race
    a, t1, S = 2.0, 4.0, 100.0
    v1 = a * t1; s1 = 0.5 * a * t1 ** 2; t2 = (S - s1) / v1; T = t1 + t2
    check(T, t1 + (S - 0.5 * a * t1 * t1) / (a * t1))
    mcq_num(B, c, "Uniform acceleration", 2, "A runner accelerates constantly at $2\\,\\mathrm{m/s^2}$ for the first $4\\,\\mathrm{s}$ of a $100\\,\\mathrm{m}$ race and then keeps that speed to the finish. How long does the race take him?",
            T, [10.0, 12.5, 13.5, 8.0], "s", ex("Acceleration phase: $v=at=8\\,\\mathrm{m/s}$, $s_1=\\tfrac12at^2=16\\,\\mathrm{m}$.", "Constant-speed phase: $100-16=84\\,\\mathrm{m}$ at $8\\,\\mathrm{m/s}$ takes $10.5\\,\\mathrm{s}$.", "Total $=4+10.5=14.5\\,\\mathrm{s}$."), P1 + ", Q15", sig=3)
    # car from rest: 5.0 s to 20.0 m/s
    a = 20.0 / 5.0
    mcq_num(B, c, "Uniform acceleration", 1, "A car starts from rest and accelerates uniformly. After $5.0\\,\\mathrm{s}$ its speed is $20.0\\,\\mathrm{m/s}$. What is its acceleration?", a, [100, 0.25, 2, 10], "m/s^2", ex("$a=\\dfrac{\\Delta v}{\\Delta t}=\\dfrac{20.0}{5.0}=4.0\\,\\mathrm{m/s^2}$."), P1 + ", Q25(a)", sig=2)
    mcq_num(B, c, "Uniform acceleration", 1, "A car starts from rest and accelerates uniformly. After $5.0\\,\\mathrm{s}$ its speed is $20.0\\,\\mathrm{m/s}$. What is its speed after $2.0\\,\\mathrm{s}$?", 8.0, [10, 4, 16, 40], "m/s", ex("$a=4.0\\,\\mathrm{m/s^2}$, so $v=at=4.0\\times2.0=8.0\\,\\mathrm{m/s}$."), P1 + ", Q25(b)", sig=2)
    mcq_num(B, c, "Uniform acceleration", 2, "A car starts from rest and accelerates uniformly. After $5.0\\,\\mathrm{s}$ its speed is $20.0\\,\\mathrm{m/s}$. What distance does it travel in the first $2.0\\,\\mathrm{s}$?", 8.0, [16, 4, 40, 32], "m", ex("$s=\\tfrac12at^2=\\tfrac12(4.0)(2.0)^2=8.0\\,\\mathrm{m}$; as a check the average speed is $(0+8)/2=4\\,\\mathrm{m/s}$, and $4\\times2=8\\,\\mathrm{m}$."), P1 + ", Q25(c)", sig=2)
    # bus and reaction time
    mcq_num(B, c, "Uniform acceleration", 1, "A bus travels at $20\\,\\mathrm{m/s}$ when the driver sees an obstacle $120\\,\\mathrm{m}$ ahead. The reaction time is $0.6\\,\\mathrm{s}$ (the bus keeps its speed during it). How far does the bus travel during the reaction time?", 12.0, [20, 0.6, 33.3, 6.0], "m", ex("Constant speed: $s=vt=20\\times0.6=12\\,\\mathrm{m}$."), P1 + ", Q26(a)", sig=2)
    a = 20.0 ** 2 / (2 * 100.0)
    mcq_num(B, c, "Uniform acceleration", 2, "After the brakes are applied the bus travels $100\\,\\mathrm{m}$ before stopping from $20\\,\\mathrm{m/s}$. What is the magnitude of its deceleration?", a, [4.0, 0.5, 20, 1.0], "m/s^2", ex("$0=v^2-2as$, so $a=\\dfrac{v^2}{2s}=\\dfrac{400}{200}=2.0\\,\\mathrm{m/s^2}$."), P1 + ", Q26(b)", sig=2)
    mcq_text(B, c, "Uniform acceleration", 2, "The bus (speed $20\\,\\mathrm{m/s}$, reaction time $0.6\\,\\mathrm{s}$, then $100\\,\\mathrm{m}$ of braking) is $120\\,\\mathrm{m}$ from the obstacle when the driver sees it. What happens?",
             "It stops $8\\,\\mathrm{m}$ before the obstacle: total stopping distance $112\\,\\mathrm{m}$", ["It hits the obstacle: the stopping distance is $120\\,\\mathrm{m}$ or more", "It stops exactly at the obstacle", "It stops $20\\,\\mathrm{m}$ before the obstacle"],
             ex("Total distance $=12+100=112\\,\\mathrm{m}<120\\,\\mathrm{m}$, so the bus stops $8\\,\\mathrm{m}$ short.", "Forgetting the reaction distance would give $100\\,\\mathrm{m}$, i.e. $20\\,\\mathrm{m}$ spare, which is too optimistic."), P1 + ", Q26(c)", "src")
    # speed trap (Part 2 Q20)
    v1, lim, d = 110 / 3.6, 85 / 3.6, 120.0
    t = d / lim; v2 = 2 * lim - v1; a = (v1 - v2) / t
    check(a, (v1 ** 2 - v2 ** 2) / (2 * d))
    mcq_num(B, c, "Uniform acceleration", 3, "In a speed trap two pressure strips are $120\\,\\mathrm{m}$ apart on a road with a limit of $85\\,\\mathrm{km/h}$. A driver at $110\\,\\mathrm{km/h}$ on the first strip slows down at once. What constant deceleration is needed so that his average speed between the strips just equals the limit?",
            a, [a * 2, a / 2, 1.36, 4.2], "m/s^2", ex("Convert: $110\\,\\mathrm{km/h}=30.56\\,\\mathrm{m/s}$, $85\\,\\mathrm{km/h}=23.61\\,\\mathrm{m/s}$.", "Time between strips at the limit: $t=120/23.61=5.08\\,\\mathrm{s}$. For constant deceleration $\\bar v=(v_1+v_2)/2=23.61$, so $v_2=16.67\\,\\mathrm{m/s}$.", "$a=\\dfrac{v_1-v_2}{t}=\\dfrac{13.89}{5.08}=2.73\\,\\mathrm{m/s^2}$. Check: $\\dfrac{v_1^2-v_2^2}{2d}=2.73$."), P2 + ", Q20", sig=3)
    # overtaking (Part 1 Q24 idea, own numbers)
    L_l, L_c, v_rel = 17.0, 3.5, 8.0
    T = (L_l + 2 * L_c) / v_rel
    mcq_num(B, c, "Relative motion", 2, "A car of length $3.5\\,\\mathrm{m}$ overtakes a lorry of length $17.0\\,\\mathrm{m}$. The time is measured from the moment the front of the car is level with the rear of the lorry until the rear of the car is one full car length ahead of the lorry's front. The car is $8.0\\,\\mathrm{m/s}$ faster than the lorry. How long is this overtaking time $T$?",
            T, [(L_l + L_c) / v_rel, L_l / v_rel, (L_l + 3 * L_c) / v_rel, 3.0], "s", ex("Relative to the lorry the car must move forward by the lorry length plus its own length (to clear the lorry) plus one more car length: $17.0+3.5+3.5=24.0\\,\\mathrm{m}$.", "$T=\\dfrac{24.0}{8.0}=3.0\\,\\mathrm{s}$."), GEN(P1 + ", Q24"), "gen", sig=2)
    # ---------------------------------------------------------------- graph reading with generated figures
    pts = [(0, 0), (4, 8), (10, 8), (14, 0)]
    fig = figs.graph_vt(pts, label="velocity-time graph: rises from 0 to 8 m/s in 4 s, constant until 10 s, falls to 0 at 14 s").svg()
    area = 0.5 * 4 * 8 + 6 * 8 + 0.5 * 4 * 8
    check(area, sum((pts[i + 1][0] - pts[i][0]) * (pts[i + 1][1] + pts[i][1]) / 2 for i in range(3)))
    mcq_num(B, c, "Graphs of motion", 1, "The graph shows the velocity of a cyclist along a straight road. What is her displacement during the whole $14\\,\\mathrm{s}$?",
            area, [8 * 14, 48, 64, 32], "m", ex("Displacement = area under the $v$-$t$ graph = triangle $+$ rectangle $+$ triangle", "$=\\tfrac12(4)(8)+(6)(8)+\\tfrac12(4)(8)=16+48+16=80\\,\\mathrm{m}$.", "$8\\times14=112$ would ignore the speeding up and slowing down."), GEN(P1 + ", Q10 (area under a v-t graph)"), "gen", fig=fig, sig=2)
    mcq_num(B, c, "Graphs of motion", 1, "For the same graph, what is the average speed over the $14\\,\\mathrm{s}$?", area / 14, [8.0, 4.0, 5.0, 6.4], "m/s", ex("Average speed $=$ total distance / total time $=80/14=5.7\\,\\mathrm{m/s}$ (the motion never reverses, so distance $=$ displacement)."), GEN(P1 + ", Q16"), "gen", fig=fig, sig=2)
    mcq_num(B, c, "Graphs of motion", 1, "For the same graph, what is the magnitude of the acceleration during the first $4\\,\\mathrm{s}$?", 2.0, [8.0, 0.5, 4.0, 1.0], "m/s^2", ex("Acceleration = gradient of the $v$-$t$ graph $=\\dfrac{8-0}{4-0}=2.0\\,\\mathrm{m/s^2}$."), GEN(P1 + ", Q9"), "gen", fig=fig, sig=2)
    pts2 = [(0, 4), (2, 4), (6, -4), (8, -4)]
    fig2 = figs.graph_vt(pts2, label="velocity-time graph: 4 m/s until 2 s, falls linearly to -4 m/s at 6 s, then -4 m/s until 8 s").svg()
    check(0.0, 8 + 0.5 * 2 * 4 - 0.5 * 2 * 4 - 8)
    mcq_text(B, c, "Graphs of motion", 3, "The graph shows the velocity of a body along a line. Its displacement and the distance it travels in the $8\\,\\mathrm{s}$ are",
             "displacement $0$, distance $24\\,\\mathrm{m}$", ["displacement $0$, distance $0$", "displacement $24\\,\\mathrm{m}$, distance $24\\,\\mathrm{m}$", "displacement $8\\,\\mathrm{m}$, distance $16\\,\\mathrm{m}$"],
             ex("Signed areas: $0$-$2$ s: $+8$; $2$-$4$ s: $+4$; $4$-$6$ s: $-4$; $6$-$8$ s: $-8$. Net $=0$ (it ends where it started).", "Distance is the sum of the absolute values: $8+4+4+8=24\\,\\mathrm{m}$."), GEN(P1 + ", Q18 (distance vs displacement)"), "gen", fig=fig2)
    # x-t graph
    fx2 = figs.Plot((0, 10), (0, 50), "t (s)", "x (m)", label="position-time graph: 0 to 10 m in 5 s, constant until 7 s, then 50 m at 10 s")
    fx2.curve([(0, 0), (5, 10), (7, 10), (10, 50)]); fx2.drop(5, 10)
    mcq_text(B, c, "Graphs of motion", 2, "In the position-time graph, in which interval does the object move fastest, and how fast?",
             "$7$-$10\\,\\mathrm{s}$, at $13.3\\,\\mathrm{m/s}$", ["$0$-$5\\,\\mathrm{s}$, at $2.0\\,\\mathrm{m/s}$", "$5$-$7\\,\\mathrm{s}$, at $10\\,\\mathrm{m/s}$", "$7$-$10\\,\\mathrm{s}$, at $40\\,\\mathrm{m/s}$"],
             ex("Speed = gradient of the $x$-$t$ graph. $0$-$5$ s: $10/5=2.0\\,\\mathrm{m/s}$. $5$-$7$ s: horizontal line, so the object is at rest. $7$-$10$ s: $(50-10)/3=13.3\\,\\mathrm{m/s}$ - the steepest section.", "$40\\,\\mathrm{m/s}$ forgets to divide by the $3\\,\\mathrm{s}$; a horizontal line means rest, not motion."), GEN(P1 + ", Q12/Q19"), "gen", fig=fx2.svg())
    # concept: free fall with air resistance (Part 2 Q1, Q2, Q9, Q10)
    mcq_pick(B, c, "Free fall", 2, "A body falls from rest through air. Which statement about its acceleration is correct?",
             ["It stays equal to $g$ the whole time", "It decreases as the speed increases and tends to zero at the terminal velocity", "It increases because the speed increases", "It becomes negative once the body is moving fast"], 1,
             ex("Air resistance grows with speed. The net force $mg-F_{\\text{drag}}$ shrinks, so $a$ falls from $g$ towards $0$; at the terminal velocity $F_{\\text{drag}}=mg$ and $a=0$."), P2 + ", Q9", "src")
    mcq_pick(B, c, "Free fall", 2, "A speed-time graph of a falling object is a straight line through the origin with gradient $9.8\\,\\mathrm{m/s^2}$ that never levels off. Which statement describes it best?",
             ["The object drops through vacuum (free fall)", "The object drops through air and reaches terminal velocity", "The object is thrown downwards through air", "The object rises and then falls"], 0,
             ex("A straight line means constant acceleration $g$: no air resistance, i.e. free fall in vacuum. In air the graph would curve and flatten at the terminal velocity."), GEN(P2 + ", Q1-Q2"), "gen")
    # terminal velocity table (Q19)
    tt = [0, 1, 2, 3, 4, 5, 6]; vv = [0, 9.5, 15.0, 19.0, 21.5, 23.0, 23.0]
    mcq_num(B, c, "Free fall", 2, "A falling object has velocity $0,\\ 9.5,\\ 15.0,\\ 19.0,\\ 21.5,\\ 23.0,\\ 23.0\\,\\mathrm{m/s}$ at $t=0,1,\\dots,6\\,\\mathrm{s}$. What is its average acceleration between $t=1.0$ and $t=2.0\\,\\mathrm{s}$?",
            5.5, [9.5, 15.0, 7.5, 3.5], "m/s^2", ex("$\\bar a=\\dfrac{15.0-9.5}{2.0-1.0}=5.5\\,\\mathrm{m/s^2}$. It is smaller than the $9.5\\,\\mathrm{m/s^2}$ of the first second because air resistance has grown."), P2 + ", Q19", sig=2)
    mcq_num(B, c, "Free fall", 2, "For the same data, what is the terminal velocity of the object?", 23.0, [21.5, 19.0, 9.5, 15.0], "m/s", ex("The speed stops changing at $23.0\\,\\mathrm{m/s}$ (from $t=5\\,\\mathrm{s}$ on): the acceleration is $0$ and drag balances weight."), P2 + ", Q19", sig=3)
    # ---------------------------------------------------------------- free fall numbers
    g_ = 10.0
    t_all = math.sqrt(2 * 40 / g_); t_30 = math.sqrt(2 * 30 / g_); dt = t_all - t_30
    from scipy.optimize import brentq                                         # second route: root finding on y(t) = 1/2 g t^2
    check(dt, brentq(lambda t: 0.5 * g_ * t * t - 40.0, 0, 10) - brentq(lambda t: 0.5 * g_ * t * t - 30.0, 0, 10))
    mcq_num(B, c, "Free fall", 3, "A stone is released from rest at the top of a $40\\,\\mathrm{m}$ tower. Air resistance is negligible ($g=10\\,\\mathrm{m/s^2}$). How long does the stone take to fall the last $10\\,\\mathrm{m}$?",
            dt, [1.4, 2.5, 2.8, 0.71], "s", ex("Total fall time: $t=\\sqrt{2h/g}=\\sqrt{8}=2.83\\,\\mathrm{s}$.", "Time to fall the first $30\\,\\mathrm{m}$: $\\sqrt{6}=2.45\\,\\mathrm{s}$.", "Last $10\\,\\mathrm{m}$: $2.83-2.45=0.38\\,\\mathrm{s}$. (It is not $\\sqrt{2\\cdot10/10}=1.4\\,\\mathrm{s}$: that would be falling $10\\,\\mathrm{m}$ from rest.)"), P2 + ", Q3", sig=2)
    # Q16: 5.0 s fall, g = 10
    mcq_text(B, c, "Free fall", 1, "An object drops from the top of a building and takes $5.0\\,\\mathrm{s}$ to reach the ground ($g=10\\,\\mathrm{m/s^2}$). Its speeds after $1.0$, $2.0$ and $5.0\\,\\mathrm{s}$ are",
             "$10$, $20$ and $50\\,\\mathrm{m/s}$", ["$5$, $10$ and $25\\,\\mathrm{m/s}$", "$10$, $40$ and $250\\,\\mathrm{m/s}$", "$10$, $20$ and $25\\,\\mathrm{m/s}$"],
             ex("$v=gt$: $10$, $20$, $50\\,\\mathrm{m/s}$ (the speed grows linearly with time).", "$5$, $10$, $25$ would be $\\tfrac12gt$; $10,40,250$ would use $v\\propto t^2$."), P2 + ", Q16(a)", "src")
    mcq_num(B, c, "Free fall", 1, "An object drops for $5.0\\,\\mathrm{s}$ with $g=10\\,\\mathrm{m/s^2}$. What is the height of the building?", 125, [250, 50, 25, 62.5], "m", ex("$h=\\tfrac12gt^2=\\tfrac12(10)(25)=125\\,\\mathrm{m}$. Check: average speed $=\\tfrac12(0+50)=25\\,\\mathrm{m/s}$, and $25\\times5=125\\,\\mathrm{m}$."), P2 + ", Q16(c)", sig=3)
    mcq_num(B, c, "Free fall", 2, "An object drops from rest with $g=10\\,\\mathrm{m/s^2}$. How far does it fall in the NEXT second, i.e. between $t=1\\,\\mathrm{s}$ and $t=2\\,\\mathrm{s}$?", 15, [5, 10, 20, 25], "m", ex("In the first second: $\\tfrac12(10)(1)^2=5\\,\\mathrm{m}$; in the first two seconds: $\\tfrac12(10)(2)^2=20\\,\\mathrm{m}$.", "Second second: $20-5=15\\,\\mathrm{m}$ (distances in successive seconds are in the ratio $1:3:5\\ldots$)."), P2 + ", Q16(b)", sig=2)
    # Q17 bullet
    vt = vertical_throw(100.0, 0.0, 10.0)
    mcq_num(B, c, "Free fall", 1, "A bullet is fired vertically upwards at $100\\,\\mathrm{m/s}$ ($g=10\\,\\mathrm{m/s^2}$). How long does it take for its speed to fall to zero?", vt["t_top"], [20, 5, 100, 1.0], "s", ex("$v=v_0-gt=0\\Rightarrow t=\\dfrac{100}{10}=10\\,\\mathrm{s}$."), P2 + ", Q17(b)", sig=3)
    mcq_num(B, c, "Free fall", 2, "A bullet is fired vertically upwards at $100\\,\\mathrm{m/s}$ ($g=10\\,\\mathrm{m/s^2}$). What maximum height does it reach?", vt["hmax"], [1000, 250, 100, 50], "m", ex("$h=\\dfrac{v_0^2}{2g}=\\dfrac{10^4}{20}=500\\,\\mathrm{m}$. Check: average speed $50\\,\\mathrm{m/s}$ for $10\\,\\mathrm{s}$ gives $500\\,\\mathrm{m}$."), P2 + ", Q17(e)", sig=3)
    mcq_num(B, c, "Free fall", 1, "A bullet is fired vertically upwards at $100\\,\\mathrm{m/s}$. What is its average speed on the way up to the highest point?", 50, [100, 0, 25, 500], "m/s", ex("Uniform deceleration from $100$ to $0$: average speed $=\\tfrac12(100+0)=50\\,\\mathrm{m/s}$ ($=500\\,\\mathrm{m}/10\\,\\mathrm{s}$)."), P2 + ", Q17(d)", sig=2)
    mcq_pick(B, c, "Free fall", 2, "A ball is thrown vertically upwards. At the highest point of its motion, what are its velocity and its acceleration (up is positive, air resistance negligible)?",
             ["velocity $0$, acceleration $-g$", "velocity $0$, acceleration $0$", "velocity $+g$, acceleration $0$", "velocity $0$, acceleration $+g$"], 0,
             ex("At the top the velocity is momentarily zero, but gravity still acts, so $a=-g$ all the way: the acceleration is the same at every stage."), P2 + ", Q4", "src")
    # ---------------------------------------------------------------- projectile motion
    v0, th = 1.70e3, 55.0
    R = v0 ** 2 * math.sin(2 * math.radians(th)) / G; T = 2 * v0 * math.sin(math.radians(th)) / G
    sim = projectile(v0, th, 0.0, G)
    check(sim["range"], R, 1e-6, "shell range"); check(sim["time"], T, 1e-6, "shell time")
    mcq_num(B, c, "Projectile motion", 2, "A shell is fired from the ground with initial speed $1.70\\times10^{3}\\,\\mathrm{m/s}$ at $55.0^\\circ$ to the horizontal. Neglecting air resistance, what is its horizontal range?",
            R, [R / 2, v0 ** 2 * math.sin(math.radians(th)) / G, v0 ** 2 / G, v0 ** 2 * math.cos(math.radians(th)) / G], "m", ex("$R=\\dfrac{v_0^2\\sin2\\theta}{g}=\\dfrac{(1.70\\times10^{3})^2\\sin110^\\circ}{9.8}=2.77\\times10^{5}\\,\\mathrm{m}$.", "Check by integrating the equations of motion numerically: $R=2.77\\times10^5\\,\\mathrm{m}$. (Unrealistic without air resistance, but that is the model.)"), P2 + ", Q21(a)", sig=3)
    mcq_num(B, c, "Projectile motion", 2, "The same shell ($v_0=1.70\\times10^{3}\\,\\mathrm{m/s}$, $55.0^\\circ$) - for how long is it in the air?", T, [T / 2, 2 * v0 / G, 2 * v0 * math.cos(math.radians(th)) / G, R / v0], "s", ex("$T=\\dfrac{2v_0\\sin\\theta}{g}=\\dfrac{2(1700)\\sin55^\\circ}{9.8}=284\\,\\mathrm{s}$.", "Equivalent: $T=R/(v_0\\cos\\theta)=2.77\\times10^5/975=284\\,\\mathrm{s}$."), P2 + ", Q21(b)", sig=3)
    v0, th, x = 25.0, 45.0, 50.0
    y = x * math.tan(math.radians(th)) - G * x ** 2 / (2 * (v0 * math.cos(math.radians(th))) ** 2)
    tn = x / (v0 * math.cos(math.radians(th))); y2 = v0 * math.sin(math.radians(th)) * tn - 0.5 * G * tn ** 2; check(y, y2)
    mcq_num(B, c, "Projectile motion", 2, "A daredevil is shot from a cannon at $45.0^\\circ$ with initial speed $25.0\\,\\mathrm{m/s}$. A net is $50.0\\,\\mathrm{m}$ away horizontally. At what height above the cannon must the net be placed?",
            y, [x * math.tan(math.radians(th)), 17.7, 39.2, 25.0], "m", ex("Time to reach the net: $t=\\dfrac{x}{v_0\\cos\\theta}=\\dfrac{50}{17.68}=2.83\\,\\mathrm{s}$.", "Height: $y=v_0\\sin\\theta\\,t-\\tfrac12gt^2=17.68(2.83)-4.9(2.83)^2=10.8\\,\\mathrm{m}$.", "Same result from $y=x\\tan\\theta-\\dfrac{gx^2}{2v_0^2\\cos^2\\theta}=50-39.2=10.8\\,\\mathrm{m}$."), P2 + ", Q22", sig=3)
    h0, vx = 100.0, 5.0
    tf = math.sqrt(2 * h0 / G); xr = vx * tf
    sim = projectile(vx, 0.0, h0, G); check(sim["time"], tf); check(sim["range"], xr)
    mcq_num(B, c, "Projectile motion", 1, "Galileo drops one weight straight down from a $100\\,\\mathrm{m}$ tower and at the same instant throws an identical weight horizontally at $5\\,\\mathrm{m/s}$. How long after release does the horizontal one hit the ground? (Neglect air resistance.)",
            tf, [h0 / G, math.sqrt(h0 / G), 2 * tf, tf / 2], "s", ex("The vertical motion is independent of the horizontal one: both fall from rest vertically, so $t=\\sqrt{2h/g}=\\sqrt{2\\times100/9.8}=4.52\\,\\mathrm{s}$ for both. They land at the same time."), P2 + ", Q23(a, b)", sig=3)
    mcq_num(B, c, "Projectile motion", 1, "For the same throw (horizontal speed $5\\,\\mathrm{m/s}$, tower $100\\,\\mathrm{m}$), what horizontal distance does the second weight travel before landing?", xr, [vx * tf / 2, vx * 2 * tf, vx * math.sqrt(h0 / G), vx * h0 / G], "m", ex("$x=v_xt=5\\times4.52=22.6\\,\\mathrm{m}$."), P2 + ", Q23(c)", sig=3)
    v0, th, h0 = 200.0, 30.0, 50.0
    sim = projectile(v0, th, h0, G)
    tt = (v0 * math.sin(math.radians(th)) + math.sqrt((v0 * math.sin(math.radians(th))) ** 2 + 2 * G * h0)) / G
    check(sim["time"], tt, 1e-6)
    mcq_num(B, c, "Projectile motion", 3, "A cannon on a $50\\,\\mathrm{m}$ high cliff fires a ball over the edge at $200\\,\\mathrm{m/s}$ at $30^\\circ$ above the horizontal. How long is the ball in the air? (Neglect air resistance.)",
            tt, [2 * v0 * math.sin(math.radians(th)) / G, (v0 * math.sin(math.radians(th)) + math.sqrt((v0 * math.sin(math.radians(th))) ** 2 - 2 * G * h0)) / G, math.sqrt(2 * h0 / G), 25.0], "s", ex("Vertical motion (up positive): $y=h_0+v_0\\sin\\theta\\,t-\\tfrac12gt^2=0$, i.e. $50+100t-4.9t^2=0$.", "Positive root: $t=\\dfrac{100+\\sqrt{100^2+4(4.9)(50)}}{2(4.9)}=20.9\\,\\mathrm{s}$.", "$2v_0\\sin\\theta/g=20.4\\,\\mathrm{s}$ is the time for a launch from ground level: the extra $50\\,\\mathrm{m}$ of height adds time."), P2 + ", Q24", sig=3)
    mcq_pick(B, c, "Projectile motion", 2, "Two projectiles are launched from ground level with the same speed. The maximum height of projectile 1 is twice that of projectile 2. The launch angles satisfy",
             ["$\\cos\\theta_1=\\sqrt2\\cos\\theta_2$", "$\\sin\\theta_1=\\sqrt2\\sin\\theta_2$", "$\\tan\\theta_1=\\sqrt2\\tan\\theta_2$", "$\\sin\\theta_1=2\\sin\\theta_2$"], 1,
             ex("$h=\\dfrac{v_0^2\\sin^2\\theta}{2g}$, so $h_1=2h_2$ gives $\\sin^2\\theta_1=2\\sin^2\\theta_2$, i.e. $\\sin\\theta_1=\\sqrt2\\sin\\theta_2$.", "(In the printed sheet the tangent option has theta2 on both sides: a typing slip. The sine relation is the correct one.)"), P2 + ", Q12", "src")
    note(P2 + ", Q12", "option C is mistyped (it reads 'tan theta2 = sqrt2 tan theta2', theta2 on both sides); the relation that follows from h1 = 2 h2 is sin theta1 = sqrt2 sin theta2 (option B).")
    mcq_pick(B, c, "Projectile motion", 2, "A ball is projected and follows a parabolic path through its highest point T (air resistance negligible). What is true of the vertical component of its acceleration?",
             ["It is zero at T", "It is greatest at T", "It is the same at every point, $g$ downwards", "It is greatest at the launch point"], 2,
             ex("Only gravity acts, so the acceleration is $g$ downwards at every instant of the flight, including the top."), P2 + ", Q13", "src")
    mcq_pick(B, c, "Projectile motion", 2, "At the highest point of a projectile's path (air resistance negligible), which statement is true?",
             ["The horizontal acceleration is zero", "The horizontal velocity is zero", "The kinetic energy is zero", "The momentum is zero"], 0,
             ex("The horizontal velocity stays $v_0\\cos\\theta\\neq0$ all the way, so kinetic energy and momentum are not zero at the top. There is no horizontal force, so the horizontal acceleration is zero."), P2 + ", Q14", "src")
    # generated projectile family
    rows = [(20.0, 30.0), (15.0, 60.0), (30.0, 40.0), (12.0, 75.0), (25.0, 20.0)]
    for v0, th in rows:
        s = projectile(v0, th, 0.0, G)
        Rr = v0 ** 2 * math.sin(2 * math.radians(th)) / G; Hh = (v0 * math.sin(math.radians(th))) ** 2 / (2 * G)
        check(s["range"], Rr, 1e-6); check(s["hmax"], Hh, 5e-5)
        mcq_num(B, c, "Projectile motion", 2, "A ball is kicked from level ground at $%s\\,\\mathrm{m/s}$ at $%s^\\circ$ above the horizontal. What is its horizontal range? (Neglect air resistance, $g=9.8\\,\\mathrm{m/s^2}$.)" % (sci(v0, 3), sci(th, 3)),
                Rr, [2 * Rr, v0 ** 2 * math.sin(math.radians(th)) / G, v0 ** 2 * math.sin(2 * math.radians(th)) / (2 * G), v0 ** 2 / G, v0 ** 2 * math.cos(math.radians(th)) / G, v0 ** 2 * math.sin(math.radians(th)) ** 2 / G], "m",
                ex("$R=\\dfrac{v_0^2\\sin2\\theta}{g}=\\dfrac{%s^2\\sin%s^\\circ}{9.8}=%s\\,\\mathrm{m}$." % (sci(v0, 3), sci(2 * th, 3), sci(Rr, 3)), "Numerical integration of the flight gives the same range."), GEN(P2 + ", Q21"), "gen", sig=3)
        mcq_num(B, c, "Projectile motion", 2, "A ball is kicked from level ground at $%s\\,\\mathrm{m/s}$ at $%s^\\circ$ above the horizontal. What maximum height does it reach? ($g=9.8\\,\\mathrm{m/s^2}$)" % (sci(v0, 3), sci(th, 3)),
                Hh, [Hh * 2, v0 ** 2 * math.sin(math.radians(th)) / (2 * G), v0 ** 2 * math.sin(math.radians(th)) ** 2 / G, v0 ** 2 * math.cos(math.radians(th)) ** 2 / (2 * G), v0 ** 2 / (2 * G), Hh / 2], "m",
                ex("$h_{\\max}=\\dfrac{(v_0\\sin\\theta)^2}{2g}=\\dfrac{(%s\\sin%s^\\circ)^2}{19.6}=%s\\,\\mathrm{m}$." % (sci(v0, 3), sci(th, 3), sci(Hh, 3)), "Mixing up $\\sin$ and $\\cos$ or forgetting to square gives the other options."), GEN(P2 + ", Q21"), "gen", sig=3)
    mcq_pick(B, c, "Projectile motion", 1, "For a fixed launch speed on level ground and no air resistance, which launch angle gives the greatest range?",
             ["$30^\\circ$", "$45^\\circ$", "$60^\\circ$", "$90^\\circ$"], 1, ex("$R=v_0^2\\sin2\\theta/g$ is largest when $\\sin2\\theta=1$, i.e. $\\theta=45^\\circ$. Angles $\\theta$ and $90^\\circ-\\theta$ give equal ranges."), "Lecture 1 (projectile motion)", "concept")
    mcq_text(B, c, "Projectile motion", 2, "A ball is thrown horizontally at $12\\,\\mathrm{m/s}$ from the edge of a $20\\,\\mathrm{m}$ cliff. What is its speed when it hits the ground? ($g=9.8\\,\\mathrm{m/s^2}$)",
             fmt(math.hypot(12, math.sqrt(2 * 9.8 * 20)), "m/s"), [fmt(12 + math.sqrt(2 * 9.8 * 20), "m/s"), fmt(math.sqrt(2 * 9.8 * 20), "m/s"), fmt(12.0, "m/s")],
             ex("Vertical speed from energy/kinematics: $v_y=\\sqrt{2gh}=\\sqrt{2(9.8)(20)}=19.8\\,\\mathrm{m/s}$; horizontal stays $12\\,\\mathrm{m/s}$.", "Speed $=\\sqrt{12^2+19.8^2}=23.2\\,\\mathrm{m/s}$ (components add as vectors, not as numbers)."), GEN(P2 + ", Q23"), "gen")
    # ---------------------------------------------------------------- relative motion
    v_car = 50.0
    v_rain_car = v_car / math.sin(math.radians(60)); v_rain_y = v_car / math.tan(math.radians(60))
    check(v_rain_car ** 2, v_car ** 2 + v_rain_y ** 2)
    mcq_num(B, c, "Relative motion", 3, "A car travels due east at $50\\,\\mathrm{km/h}$. Rain falls vertically relative to the Earth, but the traces on the side windows make $60.0^\\circ$ with the vertical. What is the speed of the rain relative to the car?",
            v_rain_car, [v_car * math.tan(math.radians(60)), v_rain_y, v_car / math.cos(math.radians(60)), v_car], "km/h", ex("In the car's frame the rain has a horizontal component $50\\,\\mathrm{km/h}$ (westwards) and the vertical component $v_y$ of the rain relative to Earth. The streaks make $60^\\circ$ with the vertical, so $\\sin60^\\circ=\\dfrac{50}{v_{rain/car}}$.", "$v_{rain/car}=\\dfrac{50}{\\sin60^\\circ}=57.7\\,\\mathrm{km/h}$."), P2 + ", Q25(a)", sig=3)
    mcq_num(B, c, "Relative motion", 3, "A car travels due east at $50\\,\\mathrm{km/h}$. The traces of the rain on the side windows make $60.0^\\circ$ with the vertical. What is the speed of the rain relative to the Earth (it falls vertically)?",
            v_rain_y, [v_rain_car, v_car * math.tan(math.radians(60)), v_car * math.cos(math.radians(60)), v_car], "km/h", ex("Vertical component stays the same in both frames: $\\tan60^\\circ=\\dfrac{50}{v_y}\\Rightarrow v_y=\\dfrac{50}{\\tan60^\\circ}=28.9\\,\\mathrm{km/h}$ downwards."), P2 + ", Q25(b)", sig=3)
    L, t_stand = 20.0, 50.0
    v_e = L / t_stand
    check(L / (v_e + 0.5), 1 / (1 / 50.0 + 0.5 / 20.0))
    mcq_num(B, c, "Relative motion", 2, "An escalator is $20.0\\,\\mathrm{m}$ long; standing on it takes $50.0\\,\\mathrm{s}$ to ride from the bottom to the top. How long does it take a person who walks up the moving escalator at $0.500\\,\\mathrm{m/s}$ relative to the escalator?",
            L / (v_e + 0.5), [L / 0.5, 50.0 - 40.0, L / (0.5 - v_e), 25.0], "s", ex("Escalator speed: $20.0/50.0=0.400\\,\\mathrm{m/s}$. Walking in the same direction the speeds add: $0.400+0.500=0.900\\,\\mathrm{m/s}$.", "$t=20.0/0.900=22.2\\,\\mathrm{s}$."), P2 + ", Q26(a)", sig=3)
    mcq_num(B, c, "Relative motion", 3, "The same escalator ($20.0\\,\\mathrm{m}$, $0.400\\,\\mathrm{m/s}$ going up). A person walks DOWN the 'up' escalator at $0.500\\,\\mathrm{m/s}$ relative to it. How long does she take to reach the bottom?",
            L / (0.5 - v_e), [L / (0.5 + v_e), L / 0.5, 22.2, 50.0], "s", ex("Relative to the ground she moves down at $0.500-0.400=0.100\\,\\mathrm{m/s}$.", "$t=20.0/0.100=200\\,\\mathrm{s}$."), P2 + ", Q26(b)", sig=3)
    vb, vr, W = 4.0, 3.0, 100.0
    mcq_num(B, c, "Relative motion", 2, "A boat can move at $4.0\\,\\mathrm{m/s}$ relative to the water. It heads straight across a $100\\,\\mathrm{m}$ wide river whose current is $3.0\\,\\mathrm{m/s}$. How far downstream does it land?", vr * W / vb, [W, W * vb / vr, 4.0 * 25, 100.0 * 5 / 4], "m",
            ex("Crossing time $t=W/v_b=100/4.0=25\\,\\mathrm{s}$ (only the component across the river matters).", "Drift $=v_rt=3.0\\times25=75\\,\\mathrm{m}$."), GEN(P2 + ", Q25-Q26 (relative velocity)"), "gen", sig=2)
    mcq_num(B, c, "Relative motion", 2, "The same boat ($4.0\\,\\mathrm{m/s}$ relative to the water) heads straight across the $3.0\\,\\mathrm{m/s}$ current. What is its speed relative to the river bank?", math.hypot(vb, vr), [7.0, 1.0, 3.5, 4.0], "m/s", ex("The two velocity components are perpendicular: $v=\\sqrt{4.0^2+3.0^2}=5.0\\,\\mathrm{m/s}$."), GEN(P2 + ", Q25-Q26"), "gen", sig=2)
    mcq_num(B, c, "Relative motion", 1, "Two trains approach each other on parallel straight tracks at $30\\,\\mathrm{m/s}$ and $20\\,\\mathrm{m/s}$. How fast does one train appear to move relative to the other?", 50, [10, 25, 600, 36], "m/s", ex("Opposite directions: relative speed $=30+20=50\\,\\mathrm{m/s}$."), GEN(P2 + ", Q25-Q26"), "gen", sig=2)
    mcq_pick(B, c, "Relative motion", 1, "An observer in a frame A sees an object B move with velocity $\\vec v_{BA}$. In a frame C that moves with velocity $\\vec v_{AC}$ relative to C the same object has velocity",
             ["$\\vec v_{BC}=\\vec v_{BA}+\\vec v_{AC}$", "$\\vec v_{BC}=\\vec v_{BA}-\\vec v_{AC}$", "$\\vec v_{BC}=\\vec v_{AC}-\\vec v_{BA}$", "$\\vec v_{BC}=\\vec v_{BA}$"], 0,
             ex("Velocities add through the intermediate frame: $\\vec v_{BC}=\\vec v_{BA}+\\vec v_{AC}$ (Lecture: $\\vec v_{PA}=\\vec v_{PB}+\\vec v_{BA}$)."), "Lecture 1 (relative motion)", "concept")

# =============================================================================================== chapter 2 - dynamics
def ch2(B):
    c = "c2"
    # ---------------------------------------------------------------- conceptual Newton's laws (Part 3 Q1-Q7)
    mcq_pick(B, c, "Newton's laws", 1, "Which of the following is NOT one of Newton's laws of motion?",
             ["The total momentum of a system of interacting bodies remains constant provided no external force acts", "The rate of change of momentum of a body is proportional to the net force and takes place in the direction of the force", "If body A exerts a force on body B, then B exerts an equal and opposite force on A", "A body continues at rest or in uniform motion in a straight line unless acted on by an external force"], 0,
             ex("Options 2, 3, 4 are the second, third and first laws. Conservation of momentum is a consequence of the second and third laws, not one of the three laws."), P3 + ", Q1", "src")
    mcq_pick(B, c, "Newton's laws", 1, "A body is falling freely under gravity. What is its rate of change of momentum equal to?", ["impulse", "kinetic energy", "power", "its weight"], 3,
             ex("$\\dfrac{\\mathrm{d}p}{\\mathrm{d}t}=F_{\\text{net}}$, and the only force is the weight $mg$."), P3 + ", Q3", "src")
    mcq_pick(B, c, "Newton's laws", 2, "The graph of the force $F$ exerted on a body against time $t$ is given. The area under the graph represents the change of which quantity of the body?", ["acceleration", "kinetic energy", "momentum", "potential energy"], 2,
             ex("Impulse $=\\int F\\,\\mathrm{d}t=\\Delta p$: the area under a force-time graph is the change in momentum."), P3 + ", Q4", "src")
    mcq_pick(B, c, "Newton's laws", 1, "A box is pushed across a horizontal floor at constant speed. If the push is stopped, the box will", ["stop immediately", "continue at constant speed", "start slowing down", "move at constant speed for a while and then slow down"], 2,
             ex("Friction was balancing the push. When the push is removed the net force is the friction alone, opposite to the motion, so the box decelerates at once ($a=\\mu g$)."), P3 + ", Q6", "src")
    mcq_pick(B, c, "Newton's laws", 1, "A box is pushed along a rough surface with constant acceleration. If the push is suddenly stopped, the box will", ["slow down and finally stop", "stop immediately", "continue at constant speed", "accelerate at a slower rate"], 0,
             ex("Only friction (opposite to the velocity) acts now: the box decelerates until it stops. It cannot stop instantly because velocity cannot change discontinuously without an impulsive force."), P3 + ", Q7", "src")
    mcq_pick(B, c, "Newton's laws", 2, "A passenger in a car is thrown forward when the car brakes sharply. Which law explains this best?", ["Newton's first law (inertia)", "Newton's second law with a constant force", "Newton's third law only", "The law of universal gravitation"], 0,
             ex("The passenger's body tends to keep its original velocity (inertia) while the car slows down beneath it: first law."), "Lecture 2 (Newton's first law, seat belts)", "concept")
    mcq_pick(B, c, "Newton's laws", 2, "A book rests on a table. The weight of the book and the normal force of the table on the book are equal and opposite. Are they an action-reaction pair (Newton's third law)?",
             ["No: they act on the same body and are different kinds of force", "Yes: they are equal and opposite", "Yes, because the book is at rest", "No, because the normal force is larger"], 0,
             ex("Third-law pairs act on DIFFERENT bodies and are of the same type. The reaction to the weight (Earth pulls the book) is the book pulling the Earth; the reaction to the normal force is the book pushing on the table."), "Lecture 2 (Newton's third law)", "concept")
    # ---------------------------------------------------------------- tractor, blocks, connected bodies
    mcq_num(B, c, "Newton's laws", 2, "A tractor of mass $1000\\,\\mathrm{kg}$ tows a trailer of mass $1000\\,\\mathrm{kg}$. The total resistance to motion is a constant $4000\\,\\mathrm{N}$ and one quarter of it acts on the trailer. They move at a constant speed of $6\\,\\mathrm{m/s}$. What force does the tow-bar exert on the tractor?",
            1000, [0, 3000, 4000, 2000], "N", ex("Constant speed $\\Rightarrow$ zero net force on each body. The trailer feels a resistance of $4000/4=1000\\,\\mathrm{N}$ forwards-opposing, so the tow-bar must pull it with $1000\\,\\mathrm{N}$; by the third law the bar pulls back on the tractor with $1000\\,\\mathrm{N}$."), P3 + ", Q2", sig=3)
    a = (6 - 4) / 2.0
    mcq_num(B, c, "Newton's second law", 1, "A box of mass $2\\,\\mathrm{kg}$ moves at a constant $3\\,\\mathrm{m/s}$ when pushed horizontally with a $4\\,\\mathrm{N}$ force on a rough surface. What is its acceleration when the push is increased to $6\\,\\mathrm{N}$?", a, [0, 2, 3, 4], "m/s^2", ex("At constant speed friction equals the push: $f=4\\,\\mathrm{N}$.", "Now $a=\\dfrac{F-f}{m}=\\dfrac{6-4}{2}=1\\,\\mathrm{m/s^2}$."), P3 + ", Q5", sig=2)
    F, m = 30.0, 3.0
    T1, T2 = F * 2 / 3, F / 3
    check(T1, 20.0); check(T2, 10.0)
    mcq_text(B, c, "Newton's second law", 2, "Three identical blocks P, Q and R are joined in a line by light strings on a smooth surface and a force of $30\\,\\mathrm{N}$ pulls P at the front. What are the tensions $T_1$ (between P and Q) and $T_2$ (between Q and R)?",
             "$T_1=20\\,\\mathrm{N}$, $T_2=10\\,\\mathrm{N}$", ["$T_1=15\\,\\mathrm{N}$, $T_2=25\\,\\mathrm{N}$", "$T_1=30\\,\\mathrm{N}$, $T_2=30\\,\\mathrm{N}$", "$T_1=10\\,\\mathrm{N}$, $T_2=20\\,\\mathrm{N}$"],
             ex("Whole system: $a=30/(3m)=10/m$.", "$T_2$ must accelerate only R: $T_2=m a=10\\,\\mathrm{N}$.", "$T_1$ accelerates Q and R: $T_1=2ma=20\\,\\mathrm{N}$. The tension decreases away from the pulled end."), GEN(P3 + ", Q8"), "gen")
    mcq_pick(B, c, "Newton's second law", 2, "Two blocks X and Y of masses $m$ and $3m$ touch each other on a smooth horizontal surface. A force $F$ pushes X, which pushes Y. What is the magnitude of the force X exerts on Y?",
             ["$F/4$", "$F/3$", "$F/2$", "$3F/4$"], 3, ex("Common acceleration $a=F/(4m)$. Y feels only the contact force: $N=3m\\,a=\\dfrac{3F}{4}$."), P3 + ", Q9", "src")
    a = 10 * 10 / 50.0; a2 = (10 * 10 - 20) / 50.0
    mcq_num(B, c, "Newton's second law", 2, "A $40\\,\\mathrm{kg}$ mass sits on a rough bench; a $10\\,\\mathrm{kg}$ mass hangs from it over a light pulley. A friction force of $20\\,\\mathrm{N}$ opposes the motion of the $40\\,\\mathrm{kg}$ mass. What is the speed of the $10\\,\\mathrm{kg}$ mass $2\\,\\mathrm{s}$ after the system is released? ($g=10\\,\\mathrm{m/s^2}$)",
            2 * a2, [2 * a, 0, 20, 2 * (100 - 20) / 10.0], "m/s", ex("Net driving force $=m_2g-f=100-20=80\\,\\mathrm{N}$ on a total mass $50\\,\\mathrm{kg}$: $a=1.6\\,\\mathrm{m/s^2}$.", "$v=at=1.6\\times2=3.2\\,\\mathrm{m/s}$."), P3 + ", Q10", sig=2)
    mcq_num(B, c, "Newton's second law", 2, "A $40\\,\\mathrm{kg}$ mass on a smooth table is joined by a light string over a pulley to a hanging $10\\,\\mathrm{kg}$ mass. What is the speed of the hanging mass $2\\,\\mathrm{s}$ after release from rest? ($g=10\\,\\mathrm{m/s^2}$)",
            2 * a, [2 * a2, 5.0, 20.0, 1.0], "m/s", ex("$a=\\dfrac{m_2g}{m_1+m_2}=\\dfrac{100}{50}=2\\,\\mathrm{m/s^2}$; $v=at=4\\,\\mathrm{m/s}$."), P3 + ", Q11", sig=2)
    # lifts
    mcq_num(B, c, "Applications of Newton's laws", 2, "A lift of mass $500\\,\\mathrm{kg}$ moves downwards with a constant acceleration of $2\\,\\mathrm{m/s^2}$ ($g=10\\,\\mathrm{N/kg}$). What is the tension in the cable?", 500 * (10 - 2), [500 * (10 + 2), 5000, 2500, 500 * 2], "N", ex("Down is positive: $mg-T=ma\\Rightarrow T=m(g-a)=500(10-2)=4000\\,\\mathrm{N}$."), P3 + ", Q12", sig=3)
    mcq_num(B, c, "Applications of Newton's laws", 2, "A man of mass $50\\,\\mathrm{kg}$ stands on a weighing scale in a lift that is descending with a constant DECELERATION of $1.0\\,\\mathrm{m/s^2}$ ($g=10\\,\\mathrm{N/kg}$). What does the scale read?", 50 * 11, [450, 500, 60, 400], "N", ex("Descending and slowing down means the acceleration is UPWARDS ($1.0\\,\\mathrm{m/s^2}$): $N-mg=ma\\Rightarrow N=m(g+a)=50(11)=550\\,\\mathrm{N}$."), P3 + ", Q13", sig=3)
    mcq_num(B, c, "Applications of Newton's laws", 2, "A man of mass $50\\,\\mathrm{kg}$ stands on a weighing scale in a lift that is descending with a constant ACCELERATION of $1.0\\,\\mathrm{m/s^2}$ ($g=10\\,\\mathrm{N/kg}$). What does the scale read?", 50 * 9, [550, 500, 60, 400], "N", ex("Accelerating downwards: $mg-N=ma\\Rightarrow N=m(g-a)=50(9)=450\\,\\mathrm{N}$. He feels lighter."), P3 + ", Q14", sig=3)
    # towed car (Q16)
    m, v, Fav = 1000.0, 0.8, 4000.0
    dp = m * v; s_car = 0.5 * m * v * v / Fav; t = dp / Fav; s_tow = v * t; stretch = s_tow - s_car; Lmin = stretch / 0.04
    check(s_car, v * t / 2)
    mcq_num(B, c, "Newton's second law", 2, "A $1000\\,\\mathrm{kg}$ car is towed from rest until it reaches the towing vehicle's constant speed $0.8\\,\\mathrm{m/s}$. What is the change of momentum of the towed car?", dp, [dp / 2, 4000.0, 0.8, 1600.0], "kg m/s", ex("$\\Delta p=m\\Delta v=1000\\times0.8=800\\,\\mathrm{kg\\,m/s}$."), P3 + ", Q16(a)", sig=3)
    mcq_num(B, c, "Newton's second law", 3, "A $1000\\,\\mathrm{kg}$ car is towed from rest to $0.8\\,\\mathrm{m/s}$ by a rope with average tension $4000\\,\\mathrm{N}$. How far does the towed car travel while it speeds up?", s_car, [s_tow, 0.16, 0.8, 0.32], "m", ex("Work-energy: $Fs=\\tfrac12mv^2\\Rightarrow s=\\dfrac{\\tfrac12(1000)(0.8)^2}{4000}=0.080\\,\\mathrm{m}$.", "Check with impulse: $t=\\Delta p/F=0.20\\,\\mathrm{s}$, $s=\\bar vt=0.4\\times0.2=0.080\\,\\mathrm{m}$."), P3 + ", Q16(b)", sig=2)
    mcq_num(B, c, "Newton's second law", 3, "In the same tow, the towing vehicle moves at a steady $0.8\\,\\mathrm{m/s}$ for the $0.20\\,\\mathrm{s}$ it takes the car to reach that speed. What is the minimum unstretched length of the rope if its breaking strain is $0.04$ (strain $=$ extension / original length)?", Lmin, [stretch, 0.16 / 0.04, 0.04, 8.0], "m", ex("Towing vehicle: $0.8\\times0.20=0.16\\,\\mathrm{m}$; towed car: $0.08\\,\\mathrm{m}$. The rope must stretch by $0.16-0.08=0.08\\,\\mathrm{m}$.", "Strain $\\le0.04\\Rightarrow L\\ge0.08/0.04=2.0\\,\\mathrm{m}$."), P3 + ", Q16(d)", sig=2)
    # incline problems
    m, th = 8.5, 30.0
    T = m * G * math.sin(math.radians(th)); N = m * G * math.cos(math.radians(th)); a = G * math.sin(math.radians(th))
    mcq_num(B, c, "Inclined plane", 2, "A block of mass $8.5\\,\\mathrm{kg}$ is held on a frictionless $30^\\circ$ incline by a cord parallel to the slope. What is the tension in the cord?", T, [N, m * G, m * G * math.tan(math.radians(th)), T * 2], "N", ex("Along the slope the cord balances the weight component: $T=mg\\sin\\theta=8.5(9.8)\\sin30^\\circ=41.7\\,\\mathrm{N}$."), P3 + ", Q18(a)", sig=3)
    mcq_num(B, c, "Inclined plane", 2, "A block of mass $8.5\\,\\mathrm{kg}$ rests on a frictionless $30^\\circ$ incline. What is the normal force on it?", N, [T, m * G, m * G / math.cos(math.radians(th)), N / 2], "N", ex("Perpendicular to the slope: $N=mg\\cos\\theta=8.5(9.8)\\cos30^\\circ=72.1\\,\\mathrm{N}$ (less than the weight $83.3\\,\\mathrm{N}$)."), P3 + ", Q18(b)", sig=3)
    mcq_num(B, c, "Inclined plane", 2, "The cord holding the $8.5\\,\\mathrm{kg}$ block on the frictionless $30^\\circ$ incline is cut. What is the magnitude of the block's acceleration?", a, [G * math.cos(math.radians(th)), G, T, G / 3], "m/s^2", ex("$a=g\\sin\\theta=9.8\\sin30^\\circ=4.9\\,\\mathrm{m/s^2}$, independent of the mass."), P3 + ", Q18(c)", sig=3)
    v0, th = 3.50, 32.0
    a = G * math.sin(math.radians(th)); d = v0 ** 2 / (2 * a); tm = v0 / a
    check(d, 0.5 * v0 * tm)
    mcq_num(B, c, "Inclined plane", 2, "A block is projected up a frictionless $32.0^\\circ$ incline with initial speed $3.50\\,\\mathrm{m/s}$. How far up the plane does it go?", d, [v0 ** 2 / (2 * G), d * 2, v0 ** 2 / (2 * G * math.cos(math.radians(th))), 0.674], "m", ex("Deceleration along the slope: $a=g\\sin\\theta=5.19\\,\\mathrm{m/s^2}$.", "$d=\\dfrac{v_0^2}{2a}=\\dfrac{12.25}{10.39}=1.18\\,\\mathrm{m}$."), P3 + ", Q19(a)", sig=3)
    mcq_num(B, c, "Inclined plane", 2, "A block is projected up a frictionless $32.0^\\circ$ incline at $3.50\\,\\mathrm{m/s}$. How long does it take to reach its highest point?", tm, [d, 2 * tm, v0 / G, 1.18], "s", ex("$t=\\dfrac{v_0}{g\\sin\\theta}=\\dfrac{3.50}{5.19}=0.674\\,\\mathrm{s}$."), P3 + ", Q19(b)", sig=3)
    mcq_text(B, c, "Inclined plane", 1, "A block is projected up a frictionless incline at $3.50\\,\\mathrm{m/s}$. What is its speed when it returns to the bottom of the incline?", fmt(3.5, "m/s"), [fmt(7.0, "m/s"), fmt(0.0, "m/s"), fmt(1.75, "m/s")], ex("Without friction mechanical energy is conserved: it returns to the same height with the same speed, $3.50\\,\\mathrm{m/s}$ (now directed down the slope)."), P3 + ", Q19(c)", "src")
    m1, m2, th = 3.70, 2.30, 30.0
    a = (m2 * G - m1 * G * math.sin(math.radians(th))) / (m1 + m2); Tn = m2 * (G - a)
    check(Tn, m1 * (a + G * math.sin(math.radians(th))))
    mcq_num(B, c, "Pulleys and connected bodies", 3, "A block $m_1=3.70\\,\\mathrm{kg}$ on a frictionless $30.0^\\circ$ incline is connected by a cord over a frictionless pulley to a hanging block $m_2=2.30\\,\\mathrm{kg}$. What is the magnitude of the acceleration of the blocks?", a,
            [(m2 - m1) * G / (m1 + m2), (m1 * G - m2 * G) / (m1 + m2), m2 * G / (m1 + m2), 1.5], "m/s^2", ex("Take down the slope and down for the hanging block as positive. Driving force: $m_2g-m_1g\\sin\\theta=22.54-18.13=4.41\\,\\mathrm{N}$.", "$a=\\dfrac{4.41}{6.00}=0.735\\,\\mathrm{m/s^2}$; the hanging block accelerates DOWNWARDS (it wins)."), P3 + ", Q20(a, b)", sig=3)
    mcq_num(B, c, "Pulleys and connected bodies", 3, "For the same arrangement ($m_1=3.70\\,\\mathrm{kg}$ on a $30.0^\\circ$ frictionless slope, $m_2=2.30\\,\\mathrm{kg}$ hanging; $a=0.735\\,\\mathrm{m/s^2}$), what is the tension in the cord?", Tn, [m2 * G, m2 * (G + a), m1 * G * math.sin(math.radians(th)), 31.4], "N", ex("Hanging block: $m_2g-T=m_2a\\Rightarrow T=m_2(g-a)=2.30(9.8-0.735)=20.8\\,\\mathrm{N}$.", "Check with the block on the slope: $T-m_1g\\sin\\theta=m_1a\\Rightarrow T=18.13+2.72=20.8\\,\\mathrm{N}$."), P3 + ", Q20(c)", sig=3)
    # force and masses (Q21)
    a1, a2_ = 12.0, 3.30
    m_ratio = a1 / a2_
    am = a1 / (m_ratio - 1); ap = a1 / (m_ratio + 1)
    check(am, 1 / (1 / a2_ - 1 / a1)); check(ap, 1 / (1 / a2_ + 1 / a1))
    mcq_num(B, c, "Newton's second law", 3, "A certain force gives an object of mass $m_1$ an acceleration of $12.0\\,\\mathrm{m/s^2}$ and an object of mass $m_2$ an acceleration of $3.30\\,\\mathrm{m/s^2}$. What acceleration would the force give to an object of mass $m_2-m_1$?",
            am, [a1 - a2_, a1 + a2_, ap, 3.0], "m/s^2", ex("$F=m_1a_1=m_2a_2\\Rightarrow m_2=3.64\\,m_1$. Then $m_2-m_1=2.64\\,m_1$ and $a=\\dfrac{F}{2.64m_1}=\\dfrac{12.0}{2.64}=4.55\\,\\mathrm{m/s^2}$.", "Use $1/a=m/F$: $\\dfrac1a=\\dfrac1{3.30}-\\dfrac1{12.0}$, so $a=4.55\\,\\mathrm{m/s^2}$."), P3 + ", Q21(a)", sig=3)
    mcq_num(B, c, "Newton's second law", 3, "With the same force (it gives $m_1$ an acceleration of $12.0\\,\\mathrm{m/s^2}$ and $m_2$ an acceleration of $3.30\\,\\mathrm{m/s^2}$), what acceleration does it give to an object of mass $m_2+m_1$?", ap, [am, a1 + a2_, (a1 + a2_) / 2, 2.0], "m/s^2", ex("$\\dfrac1a=\\dfrac1{3.30}+\\dfrac1{12.0}=0.386\\Rightarrow a=2.59\\,\\mathrm{m/s^2}$."), P3 + ", Q21(b)", sig=3)
    # hockey puck (Q23) and friction on a plane (Q24)
    u, v, t = 12.0, 6.0, 5.0
    a = (v - u) / t; mu = -a / G; d = (u + v) / 2 * t
    mcq_num(B, c, "Friction", 2, "A hockey puck is hit on a frozen lake and starts at $12\\,\\mathrm{m/s}$. Exactly $5.0\\,\\mathrm{s}$ later its speed is $6.0\\,\\mathrm{m/s}$. What is the coefficient of kinetic friction between the puck and the ice?", mu, [mu * 2, a, 0.0122, mu * 5], "", ex("Deceleration $=\\dfrac{12-6}{5}=1.2\\,\\mathrm{m/s^2}$. The only horizontal force is friction: $\\mu mg=ma\\Rightarrow\\mu=\\dfrac{a}{g}=\\dfrac{1.2}{9.8}=0.122$."), P3 + ", Q23(b)", sig=3)
    mcq_num(B, c, "Friction", 2, "A hockey puck slows from $12\\,\\mathrm{m/s}$ to $6.0\\,\\mathrm{m/s}$ in $5.0\\,\\mathrm{s}$ on ice. How far does it travel in that time?", d, [12.0 * 5, 6.0 * 5, 30.0 * 5, 18.0 * 5 / 2], "m", ex("Average speed $=\\dfrac{12+6}{2}=9\\,\\mathrm{m/s}$, so $d=9.0\\times5.0=45\\,\\mathrm{m}$."), P3 + ", Q23(c)", sig=3)
    m, th, s, t = 3.00, 30.0, 2.00, 1.50
    a = 2 * s / t ** 2; mu = (G * math.sin(math.radians(th)) - a) / (G * math.cos(math.radians(th))); f = mu * m * G * math.cos(math.radians(th)); vf = math.sqrt(2 * a * s)
    check(m * G * math.sin(math.radians(th)) - f, m * a)
    mcq_num(B, c, "Friction", 3, "A $3.00\\,\\mathrm{kg}$ block slides from rest down a $30.0^\\circ$ incline, moving $2.00\\,\\mathrm{m}$ in $1.50\\,\\mathrm{s}$. What is its acceleration?", a, [G * math.sin(math.radians(th)), 2 * a, s / t ** 2, a / 2], "m/s^2", ex("From rest $s=\\tfrac12at^2\\Rightarrow a=\\dfrac{2s}{t^2}=\\dfrac{4.00}{2.25}=1.78\\,\\mathrm{m/s^2}$."), P3 + ", Q24(a)", sig=3)
    mcq_num(B, c, "Friction", 3, "A $3.00\\,\\mathrm{kg}$ block slides down a $30.0^\\circ$ incline with an acceleration of $1.78\\,\\mathrm{m/s^2}$. What is the coefficient of kinetic friction?", mu, [math.tan(math.radians(th)), a / G, 1 - a / G, mu / 2], "", ex("Along the slope: $mg\\sin\\theta-\\mu mg\\cos\\theta=ma\\Rightarrow\\mu=\\dfrac{g\\sin\\theta-a}{g\\cos\\theta}=\\dfrac{4.9-1.78}{8.49}=0.368$."), P3 + ", Q24(b)", sig=3)
    mcq_num(B, c, "Friction", 3, "A $3.00\\,\\mathrm{kg}$ block slides down a $30.0^\\circ$ incline with $\\mu_k=0.368$. What is the magnitude of the friction force on it?", f, [m * G * math.sin(math.radians(th)), mu * m * G, mu * m * G * math.sin(math.radians(th)), f * 2], "N", ex("$f=\\mu_kN=\\mu_k\\,mg\\cos\\theta=0.368(3.00)(9.8)\\cos30^\\circ=9.37\\,\\mathrm{N}$."), P3 + ", Q24(c)", sig=3)
    mcq_num(B, c, "Friction", 2, "A $3.00\\,\\mathrm{kg}$ block starts from rest and accelerates down a $30.0^\\circ$ incline at $1.78\\,\\mathrm{m/s^2}$. What is its speed after sliding $2.00\\,\\mathrm{m}$?", vf, [2 * 1.78 * 2.0, 4.0 * 1.5, 1.78 * 1.5 * 2, vf * 2], "m/s", ex("$v^2=2as=2(1.78)(2.00)\\Rightarrow v=2.67\\,\\mathrm{m/s}$ (or $v=at=1.78\\times1.50=2.67\\,\\mathrm{m/s}$)."), P3 + ", Q24(d)", sig=3)
    # Q25 blocks A, B, C
    WA, WB, mus, muk = 44.0, 22.0, 0.2, 0.15
    WC = WB / mus - WA; ak = (WB - muk * WA) / ((WA + WB) / G)
    mcq_num(B, c, "Friction", 3, "Blocks A and B weigh $44\\,\\mathrm{N}$ and $22\\,\\mathrm{N}$. A lies on a table and is tied over a frictionless pulley to the hanging block B. Block C rests on A. What is the minimum weight of C that keeps A from sliding if $\\mu_s=0.2$ between A and the table?", WC, [WB / mus, WB / mus - WB, WB - WA * mus, 110.0 - 44.0 - 22.0], "N", ex("Static friction must balance the tension $T=W_B=22\\,\\mathrm{N}$: $\\mu_s(W_A+W_C)\\ge22\\Rightarrow W_A+W_C\\ge110\\,\\mathrm{N}$.", "$W_C\\ge110-44=66\\,\\mathrm{N}$."), P3 + ", Q25(a)", sig=3)
    mcq_num(B, c, "Friction", 3, "Blocks A (weight $44\\,\\mathrm{N}$, on a table with $\\mu_k=0.15$) and B (weight $22\\,\\mathrm{N}$, hanging) are joined over a frictionless pulley. Block C is lifted off A. What is the acceleration of A?", ak, [WB / ((WA + WB) / G), (WB - muk * WA) / (WA / G), G * muk, (WB - muk * WB) / ((WA + WB) / G)], "m/s^2", ex("Driving force $W_B-\\mu_kW_A=22-6.6=15.4\\,\\mathrm{N}$ on the total mass $(44+22)/9.8=6.73\\,\\mathrm{kg}$.", "$a=\\dfrac{15.4}{6.73}=2.29\\,\\mathrm{m/s^2}$."), P3 + ", Q25(b)", sig=3)
    # ---------------------------------------------------------------- generated dynamics families
    for m, F, mu in [(5.0, 30.0, 0.20), (12.0, 80.0, 0.30), (2.5, 15.0, 0.10), (20.0, 100.0, 0.25)]:
        f = mu * m * G; a = (F - f) / m
        mcq_num(B, c, "Friction", 2, "A $%s\\,\\mathrm{kg}$ crate is pulled along a horizontal floor by a horizontal force of $%s\\,\\mathrm{N}$. The coefficient of kinetic friction is %s. What is the acceleration of the crate?" % (sci(m), sci(F), sci(mu)),
                a, [F / m, (F + f) / m, (F - mu * m) / m, a * 2], "m/s^2", ex("Friction $f=\\mu mg=%s(%s)(9.8)=%s\\,\\mathrm{N}$." % (sci(mu), sci(m), sci(f)), "$a=\\dfrac{F-f}{m}=\\dfrac{%s-%s}{%s}=%s\\,\\mathrm{m/s^2}$." % (sci(F), sci(f), sci(m), sci(a))), GEN(P3 + ", Q23-Q25"), "gen", sig=3)
    for m, th, mu in [(6.0, 25.0, 0.15), (10.0, 40.0, 0.30), (4.0, 20.0, 0.10)]:
        a = G * (math.sin(math.radians(th)) - mu * math.cos(math.radians(th)))
        mcq_num(B, c, "Inclined plane", 3, "A %s kg block slides down a rough %s° incline (coefficient of kinetic friction %s). What is its acceleration?" % (sci(m), sci(th), sci(mu)),
                a, [G * math.sin(math.radians(th)), G * (math.sin(math.radians(th)) + mu * math.cos(math.radians(th))), G * (math.cos(math.radians(th)) - mu * math.sin(math.radians(th))), G * mu * math.cos(math.radians(th))], "m/s^2",
                ex("Along the slope: $a=g(\\sin\\theta-\\mu\\cos\\theta)=9.8(\\sin%s^\\circ-%s\\cos%s^\\circ)=%s\\,\\mathrm{m/s^2}$." % (sci(th), sci(mu), sci(th), sci(a)), "The mass cancels, and the normal force is $mg\\cos\\theta$ (not $mg$)."), GEN(P3 + ", Q24"), "gen", sig=3)
    # Atwood machine
    for m1, m2 in [(3.0, 5.0), (2.0, 7.0), (4.0, 4.5)]:
        a = abs(m2 - m1) * G / (m1 + m2); T = 2 * m1 * m2 * G / (m1 + m2)
        check(T, m1 * (G + a))
        mcq_num(B, c, "Pulleys and connected bodies", 2, "Two masses $%s\\,\\mathrm{kg}$ and $%s\\,\\mathrm{kg}$ hang from a light string over a frictionless pulley (Atwood machine). What is the tension in the string?" % (sci(m1), sci(m2)),
                T, [(m1 + m2) * G / 2, m1 * G, m2 * G, abs(m2 - m1) * G], "N", ex("$a=\\dfrac{m_2-m_1}{m_1+m_2}g=%s\\,\\mathrm{m/s^2}$." % sci(a), "Lighter mass: $T-m_1g=m_1a\\Rightarrow T=m_1(g+a)=%s\\,\\mathrm{N}$ (equal to $\\dfrac{2m_1m_2g}{m_1+m_2}$)." % sci(T)), GEN(P3 + ", Q10-Q11 (connected masses)"), "gen", sig=3)
    for m, a in [(70.0, 1.5), (55.0, 0.8)]:
        mcq_num(B, c, "Applications of Newton's laws", 2, "A %s kg person stands on a scale in a lift that accelerates UPWARDS at %s m/s². What does the scale read (in newtons)?" % (sci(m), sci(a)), m * (G + a), [m * G, m * (G - a), m * a, m * G + a], "N",
                ex("$N-mg=ma\\Rightarrow N=m(g+a)=%s(9.8+%s)=%s\\,\\mathrm{N}$." % (sci(m), sci(a), sci(m * (G + a)))), GEN(P3 + ", Q12-Q14"), "gen", sig=3)
    # weight vs mass, normal force
    mcq_pick(B, c, "Newton's laws", 1, "What is the difference between mass and weight?", ["Mass is the amount of matter and does not depend on location; weight $=mg$ is a force that depends on $g$", "Mass is a force; weight is the amount of matter", "They are the same quantity measured in different units", "Mass depends on location; weight does not"], 0,
             ex("Mass (kg) is an intrinsic property; weight (N) is the gravitational force $W=mg$, which would be about six times smaller on the Moon."), "Lecture 2 (mass and weight)", "concept")
    mcq_pick(B, c, "Applications of Newton's laws", 2, "A $10\\,\\mathrm{kg}$ block rests on a horizontal table and a hand pushes it vertically DOWN with $20\\,\\mathrm{N}$. The normal force from the table is", ["$98\\,\\mathrm{N}$", "$118\\,\\mathrm{N}$", "$78\\,\\mathrm{N}$", "$20\\,\\mathrm{N}$"], 1,
             ex("Vertical equilibrium: $N=mg+F=98+20=118\\,\\mathrm{N}$. The normal force adjusts to whatever is needed; it is not always equal to the weight."), "Lecture 3 (applying Newton's laws, free-body diagram)", "concept")
    mcq_pick(B, c, "Friction", 1, "Which statement about the maximum static friction $f_{s,\\max}$ and kinetic friction $f_k$ between the same two surfaces is correct?", ["Usually $f_{s,\\max}>f_k$ because $\\mu_s>\\mu_k$", "$f_k>f_{s,\\max}$ always", "Both depend on the contact area", "Both are independent of the normal force"], 0,
             ex("$f_{s,\\max}=\\mu_sN$ and $f_k=\\mu_kN$ with $\\mu_s\\ge\\mu_k$ in general; both are proportional to the normal force and (in this model) independent of the contact area."), "Lecture 2 (friction)", "concept")
    mcq_pick(B, c, "Applications of Newton's laws", 1, "A free-body diagram of a block sliding down a rough incline must show", ["weight, normal force and friction (up the slope)", "weight, normal force and a 'force of motion' down the slope", "only the weight", "weight, normal force, and friction pointing down the slope"], 0,
             ex("Include only real forces: gravity, the contact normal force and kinetic friction opposing the sliding. There is no separate 'force of motion'."), "Lecture 3 (free-body diagram)", "concept")
    mcq_text(B, c, "Newton's laws", 2, "A force of $12\\,\\mathrm{N}$ and a force of $5\\,\\mathrm{N}$ act on a body at right angles to each other. The magnitude of the resultant is", fmt(13.0, "N", 3), [fmt(17.0, "N", 3), fmt(7.0, "N", 3), fmt(8.5, "N", 3)], ex("Perpendicular forces: $F=\\sqrt{12^2+5^2}=13\\,\\mathrm{N}$ (not $12+5$)."), "Lecture 2 (superposition of forces)", "concept")
    mcq_num(B, c, "Newton's second law", 1, "A net force of $24\\,\\mathrm{N}$ acts on a $6.0\\,\\mathrm{kg}$ body initially at rest. What is its speed after $3.0\\,\\mathrm{s}$?", 12, [4, 72, 8, 24], "m/s", ex("$a=F/m=4.0\\,\\mathrm{m/s^2}$; $v=at=12\\,\\mathrm{m/s}$."), GEN(P3 + ", Q5"), "gen", sig=2)
    mcq_num(B, c, "Newton's second law", 2, "A $2.0\\,\\mathrm{kg}$ object feels forces $\\vec F_1=(6,\\,-2)\\,\\mathrm{N}$ and $\\vec F_2=(-2,\\,8)\\,\\mathrm{N}$. What is the magnitude of its acceleration?", math.hypot(4, 6) / 2, [math.hypot(8, 10) / 2, (4 + 6) / 2, math.hypot(4, 6), 4.0], "m/s^2", ex("Net force $=(4,\\,6)\\,\\mathrm{N}$, $|F|=\\sqrt{52}=7.21\\,\\mathrm{N}$.", "$a=7.21/2.0=3.61\\,\\mathrm{m/s^2}$."), GEN(P3 + ", Q17"), "gen", sig=3)
