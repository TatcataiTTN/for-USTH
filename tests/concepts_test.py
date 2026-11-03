"""Concept finder: loads, every concept renders without KaTeX errors, search / course / chapter filters and the brief work, links to the banks resolve, no overflow on a phone.
Usage: python3 tests/concepts_test.py [BASE_URL] [--shots]"""
import os, sys, time, urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import auth
args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (args[0] if args else "http://127.0.0.1:8765/").rstrip("/") + "/"
SHOTS = "--shots" in sys.argv
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tests", "screens", "concepts"); os.makedirs(OUT, exist_ok=True)
fails = []; checks = 0
def ok(c, m):
    global checks
    checks += 1
    if not c: fails.append(m); print("  FAIL:", m)
def status(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=30) as r: return r.status
    except Exception as e: return getattr(e, "code", 0)
def drv(w, h, mob):
    o = Options()
    for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=%d,%d" % (w, h)): o.add_argument(a)
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    d = webdriver.Chrome(options=o)
    if mob: d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": w, "height": h, "deviceScaleFactor": 2, "mobile": True})
    auth.prime(d, BASE); return d
js = lambda d, s, *a: d.execute_script(s, *a)
for mob in (False, True):
    d = drv(390 if mob else 1280, 800 if mob else 900, mob); t = "phone" if mob else "desktop"
    try:
        d.get(BASE + "concepts/index.html"); time.sleep(2)
        n = js(d, "return document.querySelectorAll('.cf-card').length")
        ok(n >= 60, "%s: only %d cards" % (t, n))
        ok(js(d, "return document.querySelectorAll('.katex-error').length") == 0, t + ": KaTeX errors")
        ok(js(d, "return document.querySelectorAll('.katex').length") > 50, t + ": formulas missing")
        ok(js(d, "return document.documentElement.scrollWidth<=window.innerWidth+1"), t + ": page overflows")
        js(d, "var i=document.querySelector('.cf-bar input[type=search]');i.value='span';i.dispatchEvent(new Event('input'))"); time.sleep(.4)
        titles = js(d, "return [].map.call(document.querySelectorAll('.cf-card h3'),function(h){return h.textContent})")
        ok(any("span" in x.lower() for x in titles) and 0 < len(titles) < 10, t + ": search 'span' gave %s" % titles[:3])
        js(d, "var i=document.querySelector('.cf-bar input[type=search]');i.value='không gian sinh';i.dispatchEvent(new Event('input'))"); time.sleep(.4)
        ok(js(d, "return document.querySelectorAll('.cf-card').length") >= 1, t + ": Vietnamese search finds nothing")
        js(d, "var i=document.querySelector('.cf-bar input[type=search]');i.value='';i.dispatchEvent(new Event('input'))"); time.sleep(.3)
        js(d, "var s=document.querySelectorAll('.cf-bar select')[0];s.value='Linear-Algebra';s.dispatchEvent(new Event('change'))"); time.sleep(.4)
        ok(js(d, "return document.querySelectorAll('.cf-card').length") == 26, t + ": LA filter should show 26 concepts")
        js(d, "document.querySelectorAll('.cf-bar button')[0].click()"); time.sleep(.3)
        hot = js(d, "return document.querySelectorAll('.cf-card').length")
        ok(0 < hot < 26, t + ": exam filter gave %d" % hot)
        js(d, "document.querySelector('.cf-card input[data-id]').click()"); time.sleep(.2)
        ok(js(d, "return document.querySelector('.cf-tray').classList.contains('show')"), t + ": brief tray did not open")
        href = js(d, "var a=document.querySelector('.cf-card a.tag');return a&&a.getAttribute('href')")
        ok(href and status(BASE + "concepts/" + href.split("?")[0]) == 200, t + ": bank link broken %s" % href)
        errs = [m for m in d.get_log("browser") if m["level"] == "SEVERE"]
        ok(not errs, t + ": console errors %s" % [m["message"][:100] for m in errs[:2]])
        if SHOTS: d.save_screenshot(os.path.join(OUT, "concepts-%s.png" % t))
        # bank deep link
        d.get(BASE + "Linear-Algebra/bank/index.html?ch=c3&topic=Adjugate"); time.sleep(1.5)
        ok(js(d, "return document.querySelectorAll('#bank .qcard, #bank .q').length>0 || document.body.innerText.indexOf('Adjugate')>=0"), t + ": bank deep link")
        ok(js(d, "var s=[].filter.call(document.querySelectorAll('#bank select'),function(x){return [].some.call(x.options,function(o){return o.value==='Adjugate'})})[0];return !!s&&s.value==='Adjugate'"), t + ": topic param not applied")
    finally: d.quit()
print("\n%d checks, %d failures" % (checks, len(fails))); sys.exit(1 if fails else 0)
