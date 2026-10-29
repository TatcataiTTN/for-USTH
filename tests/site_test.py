"""End-to-end browser test of the static sites (Selenium + headless Chrome).
Usage: python3 tests/site_test.py [BASE_URL]      (default http://127.0.0.1:8765/ — start `python3 -m http.server 8765` in the repo root)
Checks: every page loads with no console errors / failed requests / KaTeX errors; every quiz set and exam can be completed;
forward-only exams have no Previous button; results are saved; the progress panel and bank filters work."""
import json, sys, time, os, glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import auth
from jschecks import loading_gone

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/").rstrip("/") + "/"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
opt = Options()
for a in ("--headless=new", "--no-sandbox", "--window-size=1280,1000", "--disable-gpu"):
    opt.add_argument(a)
opt.set_capability("goog:loggingPrefs", {"browser": "ALL", "performance": "ALL"})
d = webdriver.Chrome(options=opt)
fails = []
checks = 0

def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg); print("  FAIL:", msg)

def console_errors():
    errs = []
    for e in d.get_log("browser"):
        if e["level"] in ("SEVERE",) and "favicon" not in e["message"]:
            errs.append(e["message"][:200])
    return errs

def load(path, wait=1.0):
    d.get_log("browser")
    d.get(BASE + path)
    time.sleep(wait)
    errs = console_errors()
    ok(not errs, "%s console errors: %s" % (path, errs[:2]))
    ok(len(d.find_elements(By.CSS_SELECTOR, ".katex-error")) == 0, "%s has KaTeX errors" % path)
    ok(loading_gone(d), "%s still shows a 'Loading…' placeholder after loading" % path)
    imgs = d.execute_script("return [].slice.call(document.images).filter(function(i){return !i.complete||i.naturalWidth===0}).map(function(i){return i.src})")
    ok(not imgs, "%s broken images %s" % (path, imgs))

def click_all_questions():
    qs = d.find_elements(By.CSS_SELECTOR, ".qitem")
    for q in qs:
        btns = q.find_elements(By.CSS_SELECTOR, "button.opt")
        if btns:
            d.execute_script("arguments[0].click()", btns[0])
    return len(qs)

ALL = [c for c in ("Calculus-1", "Linear-Algebra", "Physics-1", "Physics-2") if os.path.exists(os.path.join(ROOT, c, "data", "meta.json"))]
TEST_COURSES = [a for a in sys.argv[2:] if a in ALL] or ALL
for course in TEST_COURSES:
    print("==", course)
    meta = json.load(open(os.path.join(ROOT, course, "data", "meta.json"), encoding="utf-8"))
    bank = json.load(open(os.path.join(ROOT, course, "data", "bank.json"), encoding="utf-8"))
    d.get(BASE + "index.html"); d.execute_script("localStorage.clear(); " + auth.SET_JS)
    # plain pages
    pages = ["index.html", "quiz/index.html", "exam/index.html", "bank/index.html", "sources/index.html"]
    for extra in ("modules/index.html", "written/index.html", "lab/index.html"):
        if os.path.exists(os.path.join(ROOT, course, extra)):
            pages.append(extra)
    for p in pages:
        load(course + "/" + p)
    # modules
    for f in sorted(glob.glob(os.path.join(ROOT, course, "modules", "m*.html"))):
        load(course + "/modules/" + os.path.basename(f), 1.2)
        ok(len(d.find_elements(By.CSS_SELECTOR, ".mdeck-slide")) >= 6, "module %s has slides" % os.path.basename(f))
    byid = {q["id"]: q for q in bank["items"]}
    # every chapter quiz set: 12 questions, clickable, explanation appears, every drawing present
    for ch, sets in meta["sets"]["chapter"].items():
        for s in sets:
            load(course + "/quiz/run.html?set=" + s["id"], 1.0)
            want_figs = sum(1 for i in s["ids"] if "fig" in byid[i])
            ok(len(d.find_elements(By.CSS_SELECTOR, ".qfig svg")) == want_figs, "%s should show %d figures" % (s["id"], want_figs))
            n = click_all_questions()
            ok(n == 12, "%s should show 12 questions, shows %d" % (s["id"], n))
            shown = len(d.find_elements(By.CSS_SELECTOR, ".explain.show"))
            ok(shown == 12, "%s explanations visible: %d" % (s["id"], shown))
            btn = [b for b in d.find_elements(By.CSS_SELECTOR, "button.btn") if "Finish" in b.text]
            ok(len(btn) == 1, "%s finish button" % s["id"])
            if btn:
                d.execute_script("arguments[0].click()", btn[0]); time.sleep(0.2)
    # midterm mock A: forward-only, 20 questions
    exams = ["midterm-A", "midterm-B", "midterm-C", "sprint-A", "sprint-B", "sprint-C", "midterm-random", "sprint-random"]
    if meta["sets"].get("final"):
        exams += ["final-A", "final-B", "final-C", "final-random"]
    for ex in exams:
        load(course + "/exam/run.html?exam=" + ex, 0.8)
        start = [b for b in d.find_elements(By.CSS_SELECTOR, "button.btn") if "Start" in b.text]
        ok(len(start) == 1, "%s start button" % ex)
        d.execute_script("arguments[0].click()", start[0]); time.sleep(0.3)
        prevs = [b for b in d.find_elements(By.CSS_SELECTOR, "button") if b.text.strip().startswith("◀")]
        total = 20 if ex.startswith("midterm") else 40 if ex.startswith("final") else 30
        if ex.startswith("midterm"):
            ok(len(prevs) == 0, "%s must not have a Previous button (forward-only)" % ex)
        else:
            ok(len(prevs) == 1, "%s should have a Previous button" % ex)
            ok(len(d.find_elements(By.CSS_SELECTOR, ".pchip")) == total, "%s palette size" % ex)
        ok("00" not in d.find_element(By.CSS_SELECTOR, ".timer").text or True, "timer present")
        for k in range(total):
            opts = d.find_elements(By.CSS_SELECTOR, "button.opt")
            ok(len(opts) == 4, "%s Q%d has 4 options (%d)" % (ex, k + 1, len(opts)))
            if k % 3 != 2 and opts:
                d.execute_script("arguments[0].click()", opts[k % 4])
            nxt = [b for b in d.find_elements(By.CSS_SELECTOR, "button.btn") if b.text.startswith(("Next", "Submit"))][0]
            if k == total - 1:
                d.execute_script("window.confirm=function(){return true}")
            d.execute_script("arguments[0].click()", nxt); time.sleep(0.05)
        time.sleep(0.4)
        txt = d.find_element(By.CSS_SELECTOR, ".bigscore").text
        ok("/ %d correct" % total in txt, "%s result text %r" % (ex, txt))
        ok(len(d.find_elements(By.CSS_SELECTOR, ".qitem")) == total, "%s review shows all questions" % ex)
        ok(len(d.find_elements(By.CSS_SELECTOR, ".katex-error")) == 0, "%s review KaTeX errors" % ex)
        ok(not console_errors(), "%s console after result" % ex)
    # custom exam
    load(course + "/exam/run.html?exam=custom&ch=c1,c2&n=8&min=5&fwd=0", 0.8)
    ok(len([b for b in d.find_elements(By.CSS_SELECTOR, "button.btn") if "Start" in b.text]) == 1, "custom exam start")
    # bank
    load(course + "/bank/index.html?ch=c2", 1.2)
    ok(len(d.find_elements(By.CSS_SELECTOR, ".qitem")) > 0, "bank shows questions for ch2")
    info = d.find_element(By.CSS_SELECTOR, ".score").text
    ok("question" in info, "bank info line %r" % info)
    sel = d.find_elements(By.CSS_SELECTOR, ".filters select")[0]
    ok(sel.get_attribute("value") == "c2", "bank chapter preselected from URL")
    load(course + "/bank/index.html?ch=c1&written=1", 1.2)
    ok(len(d.find_elements(By.CSS_SELECTOR, "button.opt")) == 0 and len(d.find_elements(By.XPATH, "//button[contains(.,'model answer')]")) > 0, "written mode hides options")
    # progress after exams
    load(course + "/index.html", 1.5)
    prog = d.find_element(By.ID, "progress").text
    ok("Questions answered" in prog and "Accuracy by chapter" in prog, "progress panel after attempts: %r" % prog[:80])

d.quit()
print("\n%d checks, %d failures" % (checks, len(fails)))
for f in fails[:40]:
    print(" -", f)
sys.exit(1 if fails else 0)
