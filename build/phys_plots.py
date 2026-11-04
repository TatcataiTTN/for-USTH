# -*- coding: utf-8 -*-
"""Physics figures and data files for the module pages.
Every figure is computed from the physical law (numpy / scipy), checked against an independent route (numerical integration, a second formula, an ODE solver ...),
saved as a PNG and as a CSV with the numbers behind the curves (so a student can re-plot them or fit them).
A figure function returns (data, fig): data = ordered dict column-name -> array (all columns of one figure have the same length)."""
import csv, math, os, zipfile
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import integrate

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NAVY, RED, CYAN, GREY, GREEN, ORANGE, PURPLE = "#273896", "#ED1C24", "#15AFF0", "#6b7280", "#1a7f37", "#e08a00", "#7a3fb0"
PALETTE = [NAVY, RED, CYAN, GREEN, ORANGE, PURPLE, GREY]
G = 9.8
REG = {}                                   # course -> list of figure specs

plt.rcParams.update({
    "font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11, "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 10,
    "axes.grid": True, "grid.alpha": 0.28, "axes.spines.top": False, "axes.spines.right": False, "axes.prop_cycle": matplotlib.cycler(color=PALETTE),
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "mathtext.fontset": "dejavusans", "lines.linewidth": 2.0,
})

def figure(course, fid, ch, title, caption, formula):
    """Register a figure of `course`, chapter `ch`: `title` (heading), `caption` (what to see and why), `formula` (TeX shown with it)."""
    def deco(fn):
        REG.setdefault(course, []).append(dict(id=fid, ch=ch, title=title, caption=caption, formula=formula, fn=fn))
        return fn
    return deco

def close(a, b, rel=1e-6, atol=0.0, what=""):
    if not np.allclose(a, b, rtol=rel, atol=atol):
        raise AssertionError("figure check failed%s: max |diff| = %g" % (" (" + what + ")" if what else "", float(np.max(np.abs(np.asarray(a, float) - np.asarray(b, float))))))

def trap(y, x):
    return float(integrate.trapezoid(y, x))

def cumtrap(y, x):
    return integrate.cumulative_trapezoid(y, x, initial=0.0)

def panel(ax, xlabel="", ylabel="", title=None, legend=False):
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    if title: ax.set_title(title, loc="left")
    if legend: ax.legend(frameon=False)
    return ax

def render(course, only=None):
    """Write Physics-N/modules/img/<id>.png and Physics-N/modules/data/<id>.csv (+ all-data.zip); return the list of figure records."""
    out = os.path.join(ROOT, course, "modules"); imgd = os.path.join(out, "img"); datd = os.path.join(out, "data")
    os.makedirs(imgd, exist_ok=True); os.makedirs(datd, exist_ok=True)
    recs = []
    for spec in REG.get(course, []):
        if only and spec["id"] not in only:
            continue
        data, fig = spec["fn"]()
        n = {len(np.asarray(v)) for v in data.values()}
        assert len(n) == 1, "columns of %s differ in length: %s" % (spec["id"], n)
        for k, v in data.items():
            if np.asarray(v).dtype.kind in "fc":
                assert np.all(np.isfinite(v)), "non-finite numbers in %s / %s" % (spec["id"], k)
        fig.savefig(os.path.join(imgd, spec["id"] + ".png"), dpi=110, bbox_inches="tight", pad_inches=0.12)
        plt.close(fig)
        with open(os.path.join(datd, spec["id"] + ".csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(list(data.keys()))
            cols = [np.asarray(v) for v in data.values()]
            for i in range(len(cols[0])):
                w.writerow([("%.6g" % c[i]) if c.dtype.kind == "f" else str(c[i]) for c in cols])
        recs.append(dict(id=spec["id"], ch=spec["ch"], title=spec["title"], caption=spec["caption"], formula=spec["formula"], columns=list(data.keys()), rows=int(next(iter(n))),
                         png=os.path.getsize(os.path.join(imgd, spec["id"] + ".png")), csv=os.path.getsize(os.path.join(datd, spec["id"] + ".csv"))))
    if not only:
        with zipfile.ZipFile(os.path.join(datd, "all-data.zip"), "w", zipfile.ZIP_DEFLATED) as z:
            for r in recs:
                z.writestr(zipfile.ZipInfo(r["id"] + ".csv", date_time=(2026, 11, 3, 0, 0, 0)), open(os.path.join(datd, r["id"] + ".csv"), "rb").read(), zipfile.ZIP_DEFLATED)
    return recs

def figures_of(course):
    return list(REG.get(course, []))
