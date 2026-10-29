"""Lecture walkthrough pages: every slide image loads, the language switch and the solution buttons work, the slide list links resolve,
the original PDFs are served, nothing overflows on a phone, and no KaTeX or console errors appear.
Usage: python3 tests/lectures_test.py [BASE_URL] [--shots]   (ONLY=Calculus-1 limits the courses; --shots keeps screenshots in tests/screens/lectures/)"""
import glob, os, re, sys, time, urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import auth

args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (args[0] if args else "http://127.0.0.1:8765/").rstrip("/") + "/"
SHOTS = "--shots" in sys.argv
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tests", "screens", "lectures"); os.makedirs(OUT, exist_ok=True)

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

def driver(width, height, mobile=False):
    o = Options()
    for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=%d,%d" % (width, height)):
        o.add_argument(a)
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    d = webdriver.Chrome(options=o)
    if mobile:
        d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 2, "mobile": True})
    auth.prime(d, BASE)
    return d

def vis(d, sel):
    return d.execute_script("var e=document.querySelector(arguments[0]);return !!e && getComputedStyle(e).display!=='none'", sel)

def load(d, url):
    d.get(url); time.sleep(1.2)
    d.execute_script("document.querySelectorAll('img[loading=lazy]').forEach(function(i){i.loading='eager'})")
    for _ in range(40):                                   # wait for every slide image
        if d.execute_script("return [].every.call(document.querySelectorAll('.lpic img'),function(i){return i.complete})"):
            break
        time.sleep(0.5)

def check_page(d, course, lid, mobile):
    url = BASE + "%s/lectures/%s.html" % (course, lid); tag = "%s %s %s" % (course, lid, "phone" if mobile else "desktop")
    d.execute_script("localStorage.removeItem('ustm:lang')")
    load(d, url)
    n = d.execute_script("return document.querySelectorAll('.lslide').length")
    ok(n > 0, "%s: no slide cards" % tag)
    bad = d.execute_script("return [].filter.call(document.querySelectorAll('.lpic img'),function(i){return !(i.complete&&i.naturalWidth>0)}).map(function(i){return i.getAttribute('src')})")
    ok(not bad, "%s: images not loaded: %s" % (tag, bad[:3]))
    ok(d.execute_script("return document.querySelectorAll('.katex-error').length") == 0, "%s: KaTeX errors" % tag)
    ok(d.execute_script("return document.querySelectorAll('.katex').length") > 0, "%s: no formula rendered" % tag)
    ids = d.execute_script("return [].map.call(document.querySelectorAll('.tocgrid a'),function(a){return a.getAttribute('href').slice(1)})")
    ok(len(ids) == n and all(d.execute_script("return !!document.getElementById(arguments[0])", i) for i in ids), "%s: slide list does not match the cards" % tag)
    ok(d.execute_script("return document.documentElement.scrollWidth<=window.innerWidth+1"), "%s: horizontal overflow" % tag)
    errs = [m for m in d.get_log("browser") if m["level"] == "SEVERE"]
    ok(not errs, "%s: console errors %s" % (tag, [m["message"][:120] for m in errs[:2]]))
    # language switch: both languages by default, one at a time on request, remembered after a reload
    ok(vis(d, ".sc.en") and vis(d, ".sc.vi"), "%s: both languages should show by default" % tag)
    d.execute_script("document.querySelector('[data-lang-set=en]').click()")
    ok(vis(d, ".sc.en") and not vis(d, ".sc.vi") and not vis(d, ".l-vi"), "%s: EN only" % tag)
    d.execute_script("document.querySelector('[data-lang-set=vi]').click()")
    ok(not vis(d, ".sc.en") and vis(d, ".sc.vi") and not vis(d, ".l-en"), "%s: VI only" % tag)
    d.get(url); time.sleep(0.8)
    ok(d.execute_script("return document.documentElement.getAttribute('data-lang')") == "vi" and not vis(d, ".sc.en"), "%s: language not remembered" % tag)
    d.execute_script("document.querySelector('[data-lang-set=both]').click()")
    # solutions: closed at first, one button opens and closes them all
    total = d.execute_script("return document.querySelectorAll('details.sol').length")
    ok(d.execute_script("return document.querySelectorAll('details.sol[open]').length") == 0, "%s: solutions should start closed" % tag)
    if total:
        d.execute_script("document.getElementById('solall').click()")
        ok(d.execute_script("return document.querySelectorAll('details.sol[open]').length") == total, "%s: open-all did not open every solution" % tag)
        d.execute_script("document.getElementById('solall').click()")
        ok(d.execute_script("return document.querySelectorAll('details.sol[open]').length") == 0, "%s: second click did not close them" % tag)
    ok(status(BASE + "%s/lectures/pdf/%s" % (course, d.execute_script("return document.querySelector('a[href^=\"pdf/\"]').getAttribute('href').slice(4)"))) == 200, "%s: original PDF not served" % tag)
    if SHOTS:
        d.execute_script("document.getElementById('solall').click();document.getElementById('s%d').scrollIntoView()" % (8 if n >= 8 else 1)); time.sleep(0.8)
        d.save_screenshot(os.path.join(OUT, "%s-%s-%s.png" % (course, lid, "phone" if mobile else "desktop")))
        d.execute_script("document.getElementById('solall').click()")
    return n

for course in [c for c in ("Calculus-1", "Linear-Algebra") if not os.environ.get("ONLY") or c in os.environ["ONLY"].split(",")]:
    pages = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, course, "lectures", "L*.html")))
    if not pages:
        continue
    print("==", course, "lectures:", ", ".join(pages))
    for mobile in (False, True):
        d = driver(390 if mobile else 1280, 800 if mobile else 900, mobile)
        try:
            load(d, BASE + "%s/lectures/index.html" % course)
            links = d.execute_script("return [].map.call(document.querySelectorAll('.card[href]'),function(a){return a.getAttribute('href')})")
            ok(sorted(l[:-5] for l in links) == pages, "%s index lists %s but the pages are %s" % (course, links, pages))
            ok(d.execute_script("return document.documentElement.scrollWidth<=window.innerWidth+1"), "%s index overflows" % course)
            ok(d.execute_script("return [].some.call(document.querySelectorAll('nav a'),function(a){return a.textContent==='Lectures'})"), "%s nav has no Lectures link" % course)
            for lid in pages:
                n = check_page(d, course, lid, mobile)
                print("  ", lid, "phone" if mobile else "desktop", n, "slides")
        finally:
            d.quit()

print("\n%d checks, %d failures" % (checks, len(fails)))
sys.exit(1 if fails else 0)
