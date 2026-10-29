# -*- coding: utf-8 -*-
"""Small SVG drawing helpers for the Physics banks, slides and papers.

The drawings are generated from the same numbers as the questions (nothing is copied from the course PDFs).
Colours come from CSS classes defined in shared/core.css (.qfig ...), so every figure follows the light / dark theme.
All text is >= 13 px in a 520-wide view box, which stays legible when the figure is scaled to a phone screen."""
import html, math

esc = lambda s: html.escape(str(s), quote=True)

def _n(x):
    return ("%.1f" % x).rstrip("0").rstrip(".")

class Fig:
    def __init__(self, w=520, h=280, label=""):
        self.w, self.h, self.label = w, h, label
        self.parts = []

    # ---- primitives
    def add(self, s):
        self.parts.append(s); return self

    def line(self, x1, y1, x2, y2, cls="ax", dash=False):
        return self.add('<line class="%s"%s x1="%s" y1="%s" x2="%s" y2="%s"/>' % (cls, ' stroke-dasharray="6 5"' if dash else "", _n(x1), _n(y1), _n(x2), _n(y2)))

    def arrow(self, x1, y1, x2, y2, cls="ar", head=10):
        """Line with a filled triangular head at (x2, y2)."""
        d = math.hypot(x2 - x1, y2 - y1) or 1.0
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        bx, by = x2 - ux * head, y2 - uy * head
        px, py = -uy * head * 0.38, ux * head * 0.38
        self.line(x1, y1, bx, by, cls)
        return self.add('<polygon class="%sh" points="%s,%s %s,%s %s,%s"/>' % (cls, _n(x2), _n(y2), _n(bx + px), _n(by + py), _n(bx - px), _n(by - py)))

    def text(self, x, y, s, anchor="middle", cls="tx", rot=None, size=None):
        tr = ' transform="rotate(%s %s %s)"' % (_n(rot), _n(x), _n(y)) if rot else ""
        st = ' style="font-size:%spx"' % size if size else ""
        return self.add('<text class="%s" x="%s" y="%s" text-anchor="%s"%s%s>%s</text>' % (cls, _n(x), _n(y), anchor, tr, st, esc(s)))

    def rect(self, x, y, w, h, cls="bx", rx=0):
        return self.add('<rect class="%s" x="%s" y="%s" width="%s" height="%s" rx="%s"/>' % (cls, _n(x), _n(y), _n(w), _n(h), rx))

    def circle(self, x, y, r, cls="dot"):
        return self.add('<circle class="%s" cx="%s" cy="%s" r="%s"/>' % (cls, _n(x), _n(y), _n(r)))

    def poly(self, pts, cls="ln", closed=False, dash=False):
        p = " ".join("%s,%s" % (_n(x), _n(y)) for x, y in pts)
        tag = "polygon" if closed else "polyline"
        return self.add('<%s class="%s"%s points="%s"/>' % (tag, cls, ' stroke-dasharray="6 5"' if dash else "", p))

    def path(self, d, cls="ln"):
        return self.add('<path class="%s" d="%s"/>' % (cls, d))

    # ---- output
    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" role="img" aria-label="%s">%s</svg>'
                % (self.w, self.h, self.w, esc(self.label), "".join(self.parts)))

    def html(self):
        return '<div class="qfig">%s</div>' % self.svg()


def _ticks(lo, hi, want=6):
    span = hi - lo
    raw = span / want
    p = 10 ** math.floor(math.log10(raw))
    m = raw / p
    step = (1 if m < 1.5 else 2 if m < 3.5 else 5 if m < 7.5 else 10) * p
    t = math.ceil(lo / step - 1e-9) * step
    out = []
    while t <= hi + 1e-9:
        out.append(round(t, 10)); t += step
    return out

def _lab(v):
    if abs(v) >= 1e4 or (v != 0 and abs(v) < 1e-2):
        return ("%.0e" % v).replace("e+0", "e").replace("e-0", "e-")
    s = ("%.4g" % v)
    return s


class Plot(Fig):
    """Axes with data coordinates; `margins` = (left, right, bottom, top) in px."""
    def __init__(self, xlim, ylim, xlabel="", ylabel="", w=520, h=300, margins=(62, 18, 46, 18), xticks=None, yticks=None, grid=True, label=""):
        super().__init__(w, h, label)
        self.xlim, self.ylim = xlim, ylim
        self.ml, self.mr, self.mb, self.mt = margins
        xt = xticks if xticks is not None else _ticks(*xlim)
        yt = yticks if yticks is not None else _ticks(*ylim)
        if grid:
            for t in xt:
                self.line(self.X(t), self.mt, self.X(t), h - self.mb, "gr")
            for t in yt:
                self.line(self.ml, self.Y(t), w - self.mr, self.Y(t), "gr")
        # axes (through zero if inside the window)
        x0 = self.X(0) if xlim[0] <= 0 <= xlim[1] else self.ml
        y0 = self.Y(0) if ylim[0] <= 0 <= ylim[1] else h - self.mb
        self.line(self.ml, y0, w - self.mr, y0, "ax"); self.line(x0, h - self.mb, x0, self.mt, "ax")
        for t in xt:
            self.line(self.X(t), y0 - 3, self.X(t), y0 + 3, "ax")
            if abs(t) > 1e-12 or not (ylim[0] <= 0 <= ylim[1]):
                self.text(self.X(t), h - self.mb + 18, _lab(t), cls="tk")
        for t in yt:
            self.line(x0 - 3, self.Y(t), x0 + 3, self.Y(t), "ax")
            self.text(self.ml - 7, self.Y(t) + 5, _lab(t), anchor="end", cls="tk")
        if xlabel:
            self.text((self.ml + w - self.mr) / 2, h - 6, xlabel, cls="tx")
        if ylabel:
            self.text(15, (self.mt + h - self.mb) / 2, ylabel, cls="tx", rot=-90)

    def X(self, x):
        return self.ml + (x - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * (self.w - self.ml - self.mr)

    def Y(self, y):
        return self.h - self.mb - (y - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * (self.h - self.mb - self.mt)

    def curve(self, pts, cls="ln", dash=False):
        return self.poly([(self.X(x), self.Y(y)) for x, y in pts], cls, dash=dash)

    def func(self, f, x0, x1, n=160, cls="ln", dash=False):
        return self.curve([(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], cls, dash)

    def mark(self, x, y, label="", dx=8, dy=-8, anchor="start", cls="dot"):
        self.circle(self.X(x), self.Y(y), 4.5, cls)
        if label:
            self.text(self.X(x) + dx, self.Y(y) + dy, label, anchor=anchor)
        return self

    def hline(self, y, cls="gd"):
        return self.line(self.ml, self.Y(y), self.w - self.mr, self.Y(y), cls, dash=True)

    def vline(self, x, cls="gd"):
        return self.line(self.X(x), self.mt, self.X(x), self.h - self.mb, cls, dash=True)

    def drop(self, x, y, cls="gd"):
        """Dashed guides from a point to both axes."""
        self.line(self.X(x), self.Y(y), self.X(x), self.h - self.mb, cls, dash=True)
        self.line(self.X(x), self.Y(y), self.ml, self.Y(y), cls, dash=True)
        return self


# ----------------------------------------------------------------------------- ready-made kinematics graphs
def graph_vt(points, xlabel="t (s)", ylabel="v (m/s)", label="velocity-time graph", ylim=None, xlim=None, marks=True):
    """Piecewise-linear velocity-time graph through `points` = [(t, v), ...]."""
    ts = [p[0] for p in points]; vs = [p[1] for p in points]
    lo, hi = min(vs + [0]), max(vs + [0])
    pad = (hi - lo) * 0.12 or 1
    yl = ylim or (lo - (pad if lo < 0 else 0), hi + pad)
    xl = xlim or (min(ts + [0]), max(ts) * 1.05)
    P = Plot(xl, yl, xlabel, ylabel, label=label)
    P.curve(points, "ln")
    if marks:
        for t, v in points:
            P.circle(P.X(t), P.Y(v), 3.5, "dot")
    return P

def graph_poly(points, xlabel, ylabel, label, **kw):
    return graph_vt(points, xlabel, ylabel, label, **kw)


# ----------------------------------------------------------------------------- p-V diagrams
def pv_curve(kind, V1, V2, p1, gamma=1.4, n=40):
    """Points (V, p) of an ideal-gas process from (V1, p1) to V2: isothermal, adiabatic, isobaric, linear."""
    out = []
    for i in range(n + 1):
        V = V1 + (V2 - V1) * i / n
        if kind == "isothermal":
            p = p1 * V1 / V
        elif kind == "adiabatic":
            p = p1 * (V1 / V) ** gamma
        else:
            p = p1
        out.append((V, p))
    return out

def graph_pv(paths, vlim, plim, labels=None, xlabel="V", ylabel="p", label="p-V diagram", arrows=True, ticks=None):
    """paths = list of lists of (V, p) points (consecutive paths share end points); labels = [(V, p, 'a', dx, dy), ...]."""
    P = Plot(vlim, plim, xlabel, ylabel, label=label, xticks=ticks[0] if ticks else None, yticks=ticks[1] if ticks else None)
    for pts in paths:
        P.curve(pts, "ln")
        if arrows and len(pts) >= 2:
            k = len(pts) // 2
            x0, y0 = P.X(pts[max(k - 1, 0)][0]), P.Y(pts[max(k - 1, 0)][1])
            x1, y1 = P.X(pts[min(k + 1, len(pts) - 1)][0]), P.Y(pts[min(k + 1, len(pts) - 1)][1])
            if math.hypot(x1 - x0, y1 - y0) > 1:
                P.arrow(x0, y0, x1, y1, "ar", head=12)
    for lab in labels or []:
        V, p, s = lab[0], lab[1], lab[2]
        dx, dy = (lab[3], lab[4]) if len(lab) > 4 else (9, -9)
        P.mark(V, p, s, dx, dy)
    return P
