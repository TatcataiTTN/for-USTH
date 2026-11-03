"""Concept finder and question analyser: page loads, the three tabs work, the analyser matches / flags questions, teaching a keyword persists,
every concept renders without KaTeX errors, search / course / chapter filters and the brief work, links to the banks resolve, no overflow on a phone.
Usage: python3 tests/concepts_test.py [BASE_URL] [--shots]"""
import json, os, sys, time, urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import auth
args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (args[0] if args else "http://127.0.0.1:8765/").rstrip("/") + "/"
SHOTS = "--shots" in sys.argv
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tests", "screens", "concepts"); os.makedirs(OUT, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "concepts", "data.json"), encoding="utf-8"))
IN_SCOPE = [c for c in DATA["concepts"] if not c.get("out")]
LA_N = sum(1 for c in IN_SCOPE if c["course"] == "Linear-Algebra")
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
def tab(d, t): js(d, "document.querySelector('.cf-tabs [data-tab=\"%s\"]').click()" % t); time.sleep(.3)
def analyse(d, text, course="all"):
    js(d, "var q=document.getElementById('az-q');q.value=arguments[0];document.getElementById('az-course').value=arguments[1];document.getElementById('az-go').click()", text, course)
    time.sleep(.5)
    if not text: return None
    return js(d, "var b=document.querySelector('#az-out .callout');return {cls:b.className,txt:b.innerText}")
def example(d, i):
    js(d, "var s=document.getElementById('az-ex');s.value=arguments[0];s.dispatchEvent(new Event('change'))", str(i))
    time.sleep(.5)
    return js(d, "var b=document.querySelector('#az-out .callout');return {cls:b.className,txt:b.innerText,plan:document.getElementById('az-out').innerText.indexOf('Combined solution plan')>=0,q:document.getElementById('az-q').value}")

EXPECT_LABEL = ["Linear Algebra", "Linear Algebra", "Calculus I", "Calculus I", "Physics I", "Physics I", "Physics II", "Physics II"]
UNMATCHED = "What is the capital of France and who painted the Mona Lisa in the Louvre museum?"
UNKNOWN = "Zorblax quintuplet frobnication of the widget"
VI_Q = "Tìm cơ sở của không gian cột của ma trận A"

for mob in (False, True):
    d = drv(390 if mob else 1280, 800 if mob else 900, mob); t = "phone" if mob else "desktop"
    try:
        d.get(BASE + "concepts/index.html"); time.sleep(2)
        # ---------------------------------------------------------------- tabs and layout
        tabs = js(d, "return [].map.call(document.querySelectorAll('.cf-tabs button'),function(b){return b.textContent})")
        ok(len(tabs) == 3, "%s: expected 3 tabs, got %s" % (t, tabs))
        ok(js(d, "return !!document.getElementById('az-q')"), t + ": analyser textarea missing")
        ok(js(d, "return document.querySelectorAll('.cf-pane')[0].style.display==='block'"), t + ": analyser tab is not the default")
        # ---------------------------------------------------------------- analyser: the 9 examples
        n_ex = js(d, "return document.getElementById('az-ex').options.length") - 1
        ok(n_ex == 9, "%s: expected 9 examples, got %d" % (t, n_ex))
        plans = 0
        for i in range(n_ex):
            r = example(d, i)
            if i < len(EXPECT_LABEL):
                ok("good" in r["cls"] and ("(" + EXPECT_LABEL[i] + ")") in r["txt"], "%s: example %d should match a %s concept, got %r" % (t, i, EXPECT_LABEL[i], r["txt"][:120]))
            else:
                ok("bad" in r["cls"] and "outside the taught scope" in r["txt"], "%s: example %d should be flagged out of scope, got %r" % (t, i, r["txt"][:120]))
            plans += 1 if r["plan"] else 0
            if i == 0 and SHOTS: js(d, "window.scrollTo(0,0)"); d.save_screenshot(os.path.join(OUT, "analyse-%s.png" % t))
            if i == n_ex - 1 and SHOTS: d.save_screenshot(os.path.join(OUT, "analyse-out-%s.png" % t))
        ok(plans >= 1, t + ": no example produced a combined solution plan")
        # one result in detail
        example(d, 0)
        ok(js(d, "var c=document.querySelector('#az-out .az-card');return !!c&&c.open&&!!c.querySelector('ol')&&c.innerText.indexOf('Traps')>=0&&c.innerText.indexOf('Formulas')>=0"), t + ": first card should be open with formulas, steps and traps")
        ok(js(d, "return document.querySelectorAll('#az-out .katex').length")>0, t + ": no formulas rendered in the result")
        ok(js(d, "return document.querySelectorAll('#az-out .az-question mark').length")>0, t + ": no highlighted keywords in the question")
        ok(js(d, "return document.querySelectorAll('#az-out .katex-error').length")==0, t + ": KaTeX errors in the result")
        ok(js(d, "return document.documentElement.scrollWidth<=document.documentElement.clientWidth+1"), t + ": analyser result overflows")
        ok(js(d, "return document.getElementById('az-out').innerText.indexOf('Universal frame')>=0"), t + ": universal frame missing")
        # ---------------------------------------------------------------- unmatched and Vietnamese
        r = analyse(d, UNMATCHED)
        ok("bad" in r["cls"] and "No concept matched" in r["txt"], "%s: unrelated question should be flagged, got %r" % (t, r["txt"][:100]))
        r = analyse(d, VI_Q)
        ok("good" in r["cls"] and "(Linear Algebra)" in r["txt"], "%s: Vietnamese question not matched: %r" % (t, r["txt"][:100]))
        r = analyse(d, "")
        ok(js(d, "return document.getElementById('az-out').innerText.indexOf('Paste a question')>=0"), t + ": empty input message missing")
        # ---------------------------------------------------------------- teach the system
        js(d, "localStorage.removeItem('ustm:customkw');localStorage.removeItem('ustm:outscope')")
        r = analyse(d, UNKNOWN)
        ok("bad" in r["cls"], t + ": nonsense question should be unmatched, got %r" % r["txt"][:80])
        sugg = js(d, "return [].map.call(document.querySelectorAll('#az-out .cand'),function(b){return b.textContent})")
        ok("zorblax" in sugg and "quintuplet" in sugg, "%s: keyword suggestions missing %s" % (t, sugg))
        ok(js(d, "return document.querySelector('.az-teach').open"), t + ": the teach panel should be open when nothing matched")
        js(d, "var s=document.getElementById('az-tc');for(var i=0;i<s.options.length;i++){if(/Linear combination and span/.test(s.options[i].text)&&/Linear Algebra/.test(s.options[i].text)){s.value=s.options[i].value}};document.getElementById('az-tk').value='zorblax';document.getElementById('az-add').click()")
        time.sleep(.5)
        r = js(d, "var b=document.querySelector('#az-out .callout');return {cls:b.className,txt:b.innerText}")
        ok("good" in r["cls"] and "Linear combination and span" in r["txt"], "%s: taught keyword did not take effect: %r" % (t, r["txt"][:100]))
        ok("zorblax" in (js(d, "return localStorage.getItem('ustm:customkw')") or ""), t + ": taught keyword not saved")
        d.get(BASE + "concepts/index.html"); time.sleep(2)
        r = analyse(d, UNKNOWN)
        ok("good" in r["cls"], t + ": taught keyword lost after reload")
        js(d, "document.getElementById('az-outbtn').click()"); time.sleep(.2)
        ok(UNKNOWN in (js(d, "return localStorage.getItem('ustm:outscope')") or ""), t + ": outside-the-course mark not saved")
        js(d, "document.getElementById('az-reset').click()"); time.sleep(.5)
        r = js(d, "var b=document.querySelector('#az-out .callout');return {cls:b.className,txt:b.innerText}")
        ok("bad" in r["cls"] and js(d, "return localStorage.getItem('ustm:customkw')") == "{}", t + ": 'forget my additions' did not reset")
        # ---------------------------------------------------------------- browse tab (previous checks)
        tab(d, "br")
        n = js(d, "return document.querySelectorAll('.cf-card').length")
        ok(n == len(IN_SCOPE), "%s: expected %d concept cards, got %d" % (t, len(IN_SCOPE), n))
        ok(js(d, "return document.querySelectorAll('.katex-error').length") == 0, t + ": KaTeX errors")
        ok(js(d, "return document.querySelectorAll('.katex').length") > 50, t + ": formulas missing")
        ok(js(d, "return document.documentElement.scrollWidth<=document.documentElement.clientWidth+1"), t + ": page overflows")
        ok(js(d, "var c=document.querySelectorAll('.cf-card');var s=0;[].forEach.call(c,function(x){if(x.querySelector('ol')&&x.innerText.indexOf('Traps')>=0)s++});return s")==len(IN_SCOPE), t + ": every concept card should show steps and traps")
        js(d, "var i=document.querySelector('.cf-bar input[type=search]');i.value='span';i.dispatchEvent(new Event('input'))"); time.sleep(.4)
        titles = js(d, "return [].map.call(document.querySelectorAll('.cf-card h3'),function(h){return h.textContent})")
        ok(any("span" in x.lower() for x in titles) and 0 < len(titles) < 10, t + ": search 'span' gave %s" % titles[:3])
        js(d, "var i=document.querySelector('.cf-bar input[type=search]');i.value='không gian sinh';i.dispatchEvent(new Event('input'))"); time.sleep(.4)
        ok(js(d, "return document.querySelectorAll('.cf-card').length") >= 1, t + ": Vietnamese search finds nothing")
        js(d, "var i=document.querySelector('.cf-bar input[type=search]');i.value='';i.dispatchEvent(new Event('input'))"); time.sleep(.3)
        js(d, "var s=document.querySelectorAll('.cf-bar select')[0];s.value='Linear-Algebra';s.dispatchEvent(new Event('change'))"); time.sleep(.4)
        ok(js(d, "return document.querySelectorAll('.cf-card').length") == LA_N, "%s: LA filter should show %d concepts" % (t, LA_N))
        js(d, "document.querySelectorAll('.cf-bar button')[0].click()"); time.sleep(.3)
        hot = js(d, "return document.querySelectorAll('.cf-card').length")
        ok(0 < hot < LA_N, t + ": exam filter gave %d" % hot)
        js(d, "document.querySelector('.cf-card input[data-id]').click()"); time.sleep(.2)
        ok(js(d, "return document.querySelector('.cf-tray').classList.contains('show')"), t + ": brief tray did not open")
        href = js(d, "var a=document.querySelector('.cf-card a.tag');return a&&a.getAttribute('href')")
        ok(href and status(BASE + "concepts/" + href.split("?")[0]) == 200, t + ": bank link broken %s" % href)
        if SHOTS: d.save_screenshot(os.path.join(OUT, "concepts-%s.png" % t))
        # ---------------------------------------------------------------- keyword index tab
        tab(d, "kw")
        rows = js(d, "return document.querySelectorAll('.kwrow').length")
        ok(rows >= 400, "%s: keyword index has only %d rows" % (t, rows))
        js(d, "var i=document.querySelectorAll('.cf-pane')[2].querySelector('input[type=search]');i.value='eigen';i.dispatchEvent(new Event('input'))"); time.sleep(.3)
        sub = js(d, "return [].map.call(document.querySelectorAll('.kwrow'),function(r){return r.innerText.toLowerCase()})")
        ok(0 < len(sub) < rows and all("eigen" in x for x in sub) and any("eigenvalues and eigenvectors" in x for x in sub), "%s: keyword filter 'eigen' gave %d rows" % (t, len(sub)))
        ok(js(d, "return document.documentElement.scrollWidth<=document.documentElement.clientWidth+1"), t + ": keyword index overflows")
        if SHOTS: d.save_screenshot(os.path.join(OUT, "keywords-%s.png" % t))
        # ---------------------------------------------------------------- hash deep link
        d.get("about:blank"); d.get(BASE + "concepts/index.html#kw"); time.sleep(2)
        ok(js(d, "return document.querySelectorAll('.cf-pane')[2].style.display==='block'"), t + ": #kw does not open the keyword index")
        errs = [m for m in d.get_log("browser") if m["level"] == "SEVERE"]
        ok(not errs, t + ": console errors %s" % [m["message"][:100] for m in errs[:2]])
        # bank deep link
        d.get(BASE + "Linear-Algebra/bank/index.html?ch=c3&topic=Adjugate"); time.sleep(1.5)
        ok(js(d, "return document.querySelectorAll('#bank .qcard, #bank .q').length>0 || document.body.innerText.indexOf('Adjugate')>=0"), t + ": bank deep link")
        ok(js(d, "var s=[].filter.call(document.querySelectorAll('#bank select'),function(x){return [].some.call(x.options,function(o){return o.value==='Adjugate'})})[0];return !!s&&s.value==='Adjugate'"), t + ": topic param not applied")
    finally: d.quit()
print("\n%d checks, %d failures" % (checks, len(fails))); sys.exit(1 if fails else 0)
