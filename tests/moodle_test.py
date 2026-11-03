"""Moodle review pages (Linear Algebra, Physics I, Physics II): every page renders without KaTeX errors, nothing overflows (desktop and phone), the language switch and
the answer buttons work, the question list matches the cards, the PDFs are served.
Usage: [ONLY=Physics-1] python3 tests/moodle_test.py [BASE_URL] [--shots]"""
import os, sys, time, urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import auth

args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (args[0] if args else "http://127.0.0.1:8765/").rstrip("/") + "/"
SHOTS = "--shots" in sys.argv
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tests", "screens", "moodle"); os.makedirs(OUT, exist_ok=True)
fails = []; checks = 0
def ok(c, m):
    global checks
    checks += 1
    if not c:
        fails.append(m); print("  FAIL:", m)
def status(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
            return r.status
    except Exception as e:
        return getattr(e, "code", 0)
def driver(w, h, mobile):
    o = Options()
    for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=%d,%d" % (w, h)): o.add_argument(a)
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    d = webdriver.Chrome(options=o)
    if mobile: d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": w, "height": h, "deviceScaleFactor": 2, "mobile": True})
    auth.prime(d, BASE)
    return d
def vis(d, sel):
    return d.execute_script("var e=document.querySelector(arguments[0]);return !!e && getComputedStyle(e).display!=='none'", sel)
SETS = {"Linear-Algebra": ["ch1", "ch2", "ch3", "ch4"], "Physics-1": ["mock", "final"], "Physics-2": ["final"]}
for course, ids_ in SETS.items():
  if os.environ.get("ONLY") and course not in os.environ["ONLY"].split(","): continue
  C = course + "/moodle/"
  for mobile in (False, True):
    d = driver(390 if mobile else 1280, 800 if mobile else 900, mobile); tag = course + (" phone" if mobile else " desktop")
    try:
        d.get(BASE + C + "index.html"); time.sleep(1.2)
        ok(d.execute_script("return document.querySelectorAll('.card[href]').length") == len(ids_), tag + " index: %d set cards" % len(ids_))
        ok(d.execute_script("return document.querySelectorAll('.katex-error').length") == 0, tag + " index KaTeX errors")
        ok(d.execute_script("return document.documentElement.scrollWidth<=window.innerWidth+1"), tag + " index overflow")
        ok(d.execute_script("return [].some.call(document.querySelectorAll('nav a'),function(a){return a.textContent==='Moodle review'})"), tag + " nav has Moodle review")
        for cid in ids_:
            url = BASE + C + cid + ".html"; d.get(url); time.sleep(1.8); t = "%s %s" % (tag, cid)
            n = d.execute_script("return document.querySelectorAll('section.mq').length")
            ok(n > 0, t + ": no question cards")
            ok(d.execute_script("return document.querySelectorAll('.katex-error').length") == 0, t + ": KaTeX errors")
            ok(d.execute_script("return document.querySelectorAll('.katex').length") > 20, t + ": formulas not rendered")
            ids = d.execute_script("return [].map.call(document.querySelectorAll('.tocgrid a'),function(a){return a.getAttribute('href').slice(1)})")
            ok(len(ids) == n and all(d.execute_script("return !!document.getElementById(arguments[0])", i) for i in ids), t + ": list does not match cards")
            ok(d.execute_script("return document.documentElement.scrollWidth<=window.innerWidth+1"), t + ": page overflows")
            bad = d.execute_script("return [].filter.call(document.querySelectorAll('.mq .sc,.mqq,.mqkey'),function(e){return e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflowX==='visible'}).length")
            ok(bad == 0, t + ": %d clipped boxes" % bad)
            errs = [m for m in d.get_log("browser") if m["level"] == "SEVERE"]
            ok(not errs, t + ": console errors %s" % [m["message"][:100] for m in errs[:2]])
            d.execute_script("localStorage.removeItem('ustm:lang')"); d.get(url); time.sleep(1)
            ok(vis(d, ".sc.en") and vis(d, ".sc.vi"), t + ": both languages by default")
            d.execute_script("document.querySelector('[data-lang-set=en]').click()")
            ok(vis(d, ".sc.en") and not vis(d, ".sc.vi"), t + ": EN only")
            d.execute_script("document.querySelector('[data-lang-set=vi]').click()")
            ok(not vis(d, ".sc.en") and vis(d, ".sc.vi"), t + ": VI only")
            d.execute_script("document.querySelector('[data-lang-set=both]').click()")
            v = d.execute_script("return document.querySelectorAll('.ex details.sol').length")
            ok(v > 0 and d.execute_script("return document.querySelectorAll('.ex details.sol[open]').length") == 0, t + ": practice answers should start closed")
            d.execute_script("document.getElementById('solall').click()")
            ok(d.execute_script("return document.querySelectorAll('details.sol[open]').length==document.querySelectorAll('details.sol').length"), t + ": open-all")
            ok(status(BASE + C + "pdf/%s_Moodle-%s.pdf" % (course, cid)) == 200, t + ": PDF missing")
            if SHOTS:
                d.execute_script("var s=document.querySelectorAll('section.mq')[2];if(s)s.scrollIntoView()"); time.sleep(.6)
                d.save_screenshot(os.path.join(OUT, "%s-%s-%s.png" % (course, cid, "phone" if mobile else "desktop")))
    finally:
        d.quit()
print("\n%d checks, %d failures" % (checks, len(fails)))
sys.exit(1 if fails else 0)
