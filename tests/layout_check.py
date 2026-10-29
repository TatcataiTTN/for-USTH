"""Layout sweep: every kind of page of both courses in light and dark theme at phone and desktop width.
Fails on horizontal page overflow, KaTeX errors, console errors, a stale 'Loading…' placeholder, or text that is unreadable
(contrast ratio below 3:1 against its effective background for any visible text element).
Usage: python3 tests/layout_check.py [BASE_URL] [--shots]   (--shots keeps a screenshot of every page in tests/screens/layout/)"""
import json, os, sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import auth

args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (args[0] if args else "http://127.0.0.1:8765/").rstrip("/") + "/"
SHOTS = "--shots" in sys.argv
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tests", "screens", "layout"); os.makedirs(OUT, exist_ok=True)

import glob
PAGES = {"": ["index.html"]}
for course in [c for c in ("Calculus-1", "Linear-Algebra", "Physics-1", "Physics-2") if not os.environ.get("ONLY") or c in os.environ["ONLY"].split(",")]:
    if not os.path.exists(os.path.join(ROOT, course, "data", "meta.json")):
        continue
    meta = json.load(open(os.path.join(ROOT, course, "data", "meta.json"), encoding="utf-8"))
    bank = json.load(open(os.path.join(ROOT, course, "data", "bank.json"), encoding="utf-8"))
    papers = json.load(open(os.path.join(ROOT, course, "data", "papers.json"), encoding="utf-8"))
    mods = sorted(glob.glob(os.path.join(ROOT, course, "modules", "m*.html")))
    figs = {q["id"] for q in bank["items"] if "fig" in q}
    figset = next((st["id"] for ch in meta["sets"]["chapter"].values() for st in ch if figs & set(st["ids"])), None)
    pages = ["index.html"]
    if mods: pages += ["modules/index.html", "modules/%s" % os.path.basename(mods[0])]
    pages += ["quiz/index.html", "quiz/run.html?set=c1-A"] + (["quiz/run.html?set=%s" % figset] if figset else [])
    pages += ["exam/index.html", "exam/run.html?exam=midterm-A", "exam/run.html?exam=sprint-A"] + (["exam/run.html?exam=final-A"] if meta["sets"].get("final") else [])
    pages += ["bank/index.html"] + (["bank/index.html?ch=c1"] if figset else [])
    if papers: pages += ["written/index.html", "written/paper.html?p=%s" % papers[0]["id"], "written/paper.html?p=%s&mode=exam" % papers[0]["id"]]
    if os.path.exists(os.path.join(ROOT, course, "lab", "index.html")): pages.append("lab/index.html")
    lecs = sorted(glob.glob(os.path.join(ROOT, course, "lectures", "L*.html")))
    if lecs: pages += ["lectures/index.html"] + ["lectures/%s" % os.path.basename(p) for p in (lecs[0], lecs[-1])]
    pages.append("sources/index.html")
    PAGES[course + "/"] = pages

from jschecks import CONTRAST_JS, THEME_JS, loading_gone

fails = []; checks = 0
def ok(c, m):
    global checks
    checks += 1
    if not c:
        fails.append(m); print("  FAIL:", m)

for theme in ("light", "dark"):
    for label, (w, h) in (("phone", (390, 844)), ("desktop", (1280, 900))):
        o = Options()
        for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=%d,%d" % (w, h)): o.add_argument(a)
        o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        d = webdriver.Chrome(options=o)
        if label == "phone":      # headless Chrome cannot make a window narrower than 500 px, so emulate a real 390 px phone viewport
            d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": w, "height": h, "deviceScaleFactor": 2, "mobile": True})
        d.get(BASE + "index.html"); d.execute_script(("localStorage.clear(); " + auth.SET_JS + "; localStorage.setItem('ustm:theme', JSON.stringify(%r))") % theme)
        for prefix, pages in PAGES.items():
            for page in pages:
                path = prefix + page; tag = "[%s %s] %s" % (theme, label, path)
                d.get_log("browser"); d.get(BASE + path); time.sleep(1.1)
                if "exam/run" in page:        # start the exam so the question view is what gets checked
                    for b in d.find_elements(By.CSS_SELECTOR, "button.btn"):
                        if "Start" in b.text: d.execute_script("arguments[0].click()", b); time.sleep(0.6); break
                if "mode=exam" in page:
                    for b in d.find_elements(By.CSS_SELECTOR, "button.btn"):
                        if "Start" in b.text: d.execute_script("arguments[0].click()", b); time.sleep(0.6); break
                errs = [e["message"][:120] for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"]]
                ok(not errs, "%s console errors %s" % (tag, errs[:1]))
                ok(len(d.find_elements(By.CSS_SELECTOR, ".katex-error")) == 0, "%s KaTeX errors" % tag)
                ok(loading_gone(d), "%s stale Loading placeholder" % tag)
                sw, iw = d.execute_script("return [document.documentElement.scrollWidth, window.innerWidth]")
                ok(iw == w or label == "desktop", "%s viewport is %d px, expected %d" % (tag, iw, w))
                ok(sw <= iw + 1, "%s horizontal page overflow: scrollWidth %d > viewport %d" % (tag, sw, iw))
                if page == "index.html":      # the Display popup must open fully inside the viewport
                    sm = [e for e in d.find_elements(By.CSS_SELECTOR, "details.menu summary") if e.is_displayed()]
                    if sm:
                        d.execute_script("arguments[0].click()", sm[0]); time.sleep(0.3)
                        l, r_, vw = d.execute_script("var r=document.querySelector('details.menu .pop').getBoundingClientRect(); return [r.left, r.right, document.documentElement.clientWidth]")
                        ok(l >= 0 and r_ <= vw, "%s Display popup outside the viewport: %.0f..%.0f of %d" % (tag, l, r_, vw))
                        d.execute_script("arguments[0].click()", sm[0])
                attr, lum = d.execute_script(THEME_JS)
                ok(attr == theme and (lum > 0.6 if theme == "light" else lum < 0.15), "%s the %s theme is not in effect (data-theme=%s, background luminance %.2f)" % (tag, theme, attr, lum))
                low = d.execute_script(CONTRAST_JS)
                ok(not low, "%s low-contrast text: %s" % (tag, low))
                if SHOTS:
                    d.save_screenshot(os.path.join(OUT, "%s_%s_%s.png" % (theme, label, path.replace("/", "_").replace("?", "_").replace("=", "-").replace("&", "_"))))
        d.quit()
print("\n%d checks, %d failures" % (checks, len(fails)))
sys.exit(1 if fails else 0)
