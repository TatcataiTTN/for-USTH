"""Physics plots and data files: every figure of the module pages exists as a PNG (right size, not blank) and as a CSV (header, rectangular, finite numbers), the zip files contain every CSV,
every module page links its figures and CSV files, and the links resolve on the server.
Usage: python3 tests/figures_test.py [BASE_URL]      (BASE_URL defaults to http://127.0.0.1:8766/; use the production address after a push)"""
import csv, io, json, math, os, re, sys, urllib.request, zipfile
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8766/").rstrip("/") + "/"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
fails = []; checks = 0
def ok(c, m):
    global checks
    checks += 1
    if not c: fails.append(m); print("  FAIL:", m)
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u), timeout=60) as r: return r.status, r.read()
    except Exception as e: return getattr(e, "code", 0), b""
def png_size(b):
    return (int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")) if b[:8] == b"\x89PNG\r\n\x1a\n" else (0, 0)
for course, nfig_min in (("Physics-1", 30), ("Physics-2", 40)):
    print("==", course)
    figs = json.load(open(os.path.join(ROOT, course, "modules", "figures.json"), encoding="utf-8"))
    ok(len(figs) >= nfig_min, "%s: only %d figures" % (course, len(figs)))
    ok(len({f["id"] for f in figs}) == len(figs), course + ": duplicate figure ids")
    chs = {f["ch"] for f in figs}; meta = json.load(open(os.path.join(ROOT, course, "data", "meta.json"), encoding="utf-8"))
    ok(chs == {c["id"] for c in meta["chapters"]}, "%s: chapters without a figure: %s" % (course, {c["id"] for c in meta["chapters"]} - chs))
    for f in figs:
        base = course + "/modules/"
        st, png = get(BASE + base + "img/%s.png" % f["id"]); w, h = png_size(png)
        ok(st == 200 and 400 <= w <= 1400 and 200 <= h <= 1000 and len(png) > 8000, "%s: bad PNG %s (%s, %dx%d, %d bytes)" % (course, f["id"], st, w, h, len(png)))
        st, raw = get(BASE + base + "data/%s.csv" % f["id"]); rows = list(csv.reader(io.StringIO(raw.decode("utf-8")))) if st == 200 else []
        ok(st == 200 and len(rows) >= 4, "%s: bad CSV %s" % (course, f["id"]))
        if len(rows) >= 4:
            head = rows[0]; ok(head == f["columns"] and len(rows) - 1 == f["rows"], "%s: CSV header/rows of %s do not match figures.json" % (course, f["id"]))
            ok(all(len(r) == len(head) for r in rows), "%s: CSV %s is not rectangular" % (course, f["id"]))
            for j, name in enumerate(head):
                vals = [r[j] for r in rows[1:]]
                try: nums = [float(v) for v in vals]
                except ValueError: nums = None
                if nums is not None: ok(all(math.isfinite(x) for x in nums), "%s: non-finite number in %s / %s" % (course, f["id"], name))
                else: ok(len(set(vals)) >= 2, "%s: text column %s of %s has no variety" % (course, name, f["id"]))
    st, z = get(BASE + course + "/modules/data/all-data.zip"); names = set(zipfile.ZipFile(io.BytesIO(z)).namelist()) if st == 200 else set()
    ok(names == {f["id"] + ".csv" for f in figs}, "%s: all-data.zip does not hold every CSV (%d of %d)" % (course, len(names), len(figs)))
    mods = sorted(m for m in os.listdir(os.path.join(ROOT, course, "modules")) if re.match(r"m\d\d\.html$", m)); ok(len(mods) == len(meta["chapters"]), "%s: expected %d module pages, found %d" % (course, len(meta["chapters"]), len(mods)))
    for m in mods:
        st, page = get(BASE + course + "/modules/" + m); page = page.decode("utf-8"); mid = m[:-5]
        ch_figs = [f for f in figs if f["ch"] == "c" + str(int(mid[1:]))]
        ok(st == 200 and len(ch_figs) >= 3, "%s %s: page %s, %d figures for the chapter" % (course, m, st, len(ch_figs)))
        for f in ch_figs:
            ok(('img/%s.png' % f["id"]) in page and ('data/%s.csv' % f["id"]) in page, "%s %s: figure %s is not linked" % (course, m, f["id"]))
        st, z = get(BASE + course + "/modules/data/%s-data.zip" % mid); zn = set(zipfile.ZipFile(io.BytesIO(z)).namelist()) if st == 200 else set()
        ok(zn == {f["id"] + ".csv" for f in ch_figs}, "%s %s: module zip holds %d files, expected %d" % (course, m, len(zn), len(ch_figs)))
print("\n%d checks, %d failures" % (checks, len(fails))); sys.exit(1 if fails else 0)
