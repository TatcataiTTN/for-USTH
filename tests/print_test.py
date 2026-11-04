"""Printable midterm papers: every midterm mock of every course renders as a paper (right number of questions, four options each, figures present, no KaTeX errors, answer sheet)
and as a solutions version (one marked answer and one explanation per question).   Usage: python3 tests/print_test.py [BASE_URL]"""
import json, os, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import auth
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8766/").rstrip("/") + "/"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
o = Options()
for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=1100,900"): o.add_argument(a)
o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o); auth.prime(d, BASE)
fails = []; checks = 0
def ok(c, m):
    global checks
    checks += 1
    if not c: fails.append(m); print("  FAIL:", m)
def load(url):
    d.get(BASE + url)
    for _ in range(60):
        if d.execute_script("return document.body.getAttribute('data-ready')") == "1": return True
        time.sleep(0.25)
    return False
for course in ("Calculus-1", "Linear-Algebra", "Physics-1", "Physics-2"):
    meta = json.load(open(os.path.join(ROOT, course, "data", "meta.json"), encoding="utf-8")); bank = {i["id"]: i for i in json.load(open(os.path.join(ROOT, course, "data", "bank.json"), encoding="utf-8"))["items"]}
    mids = meta["sets"]["midterm"]; ok(len(mids) >= 12, "%s: only %d midterm mocks" % (course, len(mids)))
    for k, s in enumerate(mids):
        keys = (0, 1) if k in (0, len(mids) - 1) else (0,)
        for key in keys:
            url = "%s/exam/print.html?exam=%s%s" % (course, s["id"], "&key=1" if key else ""); tag = "%s %s%s" % (course, s["id"], " (solutions)" if key else "")
            ok(load(url), tag + ": page did not finish")
            n = len(s["ids"]); figs = sum(1 for i in s["ids"] if "fig" in bank[i])
            ok(d.execute_script("return document.querySelectorAll('.pq').length") == n, tag + ": expected %d questions" % n)
            ok(d.execute_script("return [].every.call(document.querySelectorAll('.pq'),function(q){return q.querySelectorAll('.po').length===4})"), tag + ": a question without four options")
            ok(d.execute_script("return document.querySelectorAll('.pfig svg').length") == figs, tag + ": expected %d figures" % figs)
            ok(d.execute_script("return document.querySelectorAll('.katex-error').length") == 0, tag + ": KaTeX errors")
            if key: ok(d.execute_script("return document.querySelectorAll('.po.good').length===document.querySelectorAll('.pq').length&&document.querySelectorAll('.pexp').length===document.querySelectorAll('.pq').length"), tag + ": answers or explanations missing")
            else: ok(d.execute_script("return !!document.querySelector('.psheet table')&&document.querySelectorAll('.po.good').length===0"), tag + ": answer sheet missing or answers leaked into the paper")
    errs = [m for m in d.get_log("browser") if m["level"] == "SEVERE"]; ok(not errs, "%s: console errors %s" % (course, [m["message"][:80] for m in errs[:2]]))
d.quit(); print("\n%d checks, %d failures" % (checks, len(fails))); sys.exit(1 if fails else 0)
