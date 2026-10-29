"""Test of the Written pages (both courses).
1. static: every answer / solution fragment is well-formed HTML (balanced tags from an allowed list, no raw < or > inside formulas)
2. browser: hub, every paper in study mode (all answers + solutions revealed, no KaTeX errors) and in exam mode (start, finish, self-mark, save),
   lab links resolve and pre-fill the lab.   Usage: python3 tests/written_test.py [BASE_URL]"""
import json, os, re, sys, time
from html.parser import HTMLParser
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import auth

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/").rstrip("/") + "/"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
fails = []; checks = 0
def ok(c, m):
    global checks
    checks += 1
    if not c:
        fails.append(m); print("  FAIL:", m)

ALLOWED = {"b", "i", "ol", "ul", "li", "p", "br", "div", "span", "table", "tr", "td", "th", "sup", "sub", "code", "em", "strong", "details", "summary"}
VOID = {"br"}
class Checker(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.bad = []
    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED: self.bad.append("tag <%s>" % tag)
        if tag not in VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack or self.stack[-1] != tag: self.bad.append("unbalanced </%s> (stack %s)" % (tag, self.stack[-3:]));
        else: self.stack.pop()
MATH = re.compile(r"(\$\$.*?\$\$|\$.*?\$)", re.S)
def static_check(course):
    papers = json.load(open(os.path.join(ROOT, course, "data", "papers.json"), encoding="utf-8"))
    for p in papers:
        tot = 0
        for qi, q in enumerate(p["problems"], 1):
            for pi, pt in enumerate(q, 1):
                tot += pt["marks"]
                for fld in ("answer", "solution"):
                    h = pt[fld]; w = "%s %s Q%d.%d %s" % (course, p["id"], qi, pi, fld)
                    ok(bool(h.strip()), w + " is empty")
                    for seg in MATH.findall(h):
                        ok("<" not in seg and ">" not in seg, w + " has a raw < or > inside a formula: " + seg[:60])
                    c = Checker(); c.feed(h)
                    ok(not c.bad and not c.stack, "%s malformed HTML: %s %s" % (w, c.bad[:2], c.stack[:2]))
                ok(pt["marks"] > 0, "marks > 0")
        ok(abs(tot - 20) < 1e-9, "%s %s marks sum to %s (expected 20)" % (course, p["id"], tot))
    return papers

o = Options()
for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=1280,1000"): o.add_argument(a)
o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o)
def errs(): return [e["message"][:200] for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"]]
def load(path, wait=1.2):
    d.get_log("browser"); d.get(BASE + path); time.sleep(wait)
    ok(not errs(), "%s console errors" % path)
    ok(len(d.find_elements(By.CSS_SELECTOR, ".katex-error")) == 0, "%s KaTeX errors" % path)
    stale = [e for e in d.find_elements(By.XPATH, "//*[normalize-space(text())='Loading…']") if e.is_displayed()]
    ok(not stale, "%s still shows a 'Loading…' placeholder after loading" % path)

for course in ("Calculus-1", "Linear-Algebra"):
    print("==", course)
    papers = static_check(course)
    d.get(BASE + "index.html"); d.execute_script("localStorage.clear(); " + auth.SET_JS)
    load(course + "/written/index.html")
    cards = d.find_elements(By.CSS_SELECTOR, "#written-hub .panel")
    ok(len(cards) == len(papers), "%s hub shows %d cards, expected %d" % (course, len(cards), len(papers)))
    ok(len(d.find_elements(By.XPATH, "//a[contains(.,'Study with solutions')]")) == len(papers), "study links")
    for p in papers:
        nparts = sum(len(q) for q in p["problems"])
        # ---- study mode
        load(course + "/written/paper.html?p=" + p["id"], 1.3)
        ok(len(d.find_elements(By.CSS_SELECTOR, ".part")) == nparts, "%s study: %d parts expected" % (p["id"], nparts))
        for b in d.find_elements(By.XPATH, "//button[contains(.,'Show the answer')]"): d.execute_script("arguments[0].click()", b)
        for b in d.find_elements(By.XPATH, "//button[contains(.,'Show the full solution')]"): d.execute_script("arguments[0].click()", b)
        time.sleep(0.4)
        ok(len(d.find_elements(By.CSS_SELECTOR, ".callout.good:not(.hide)")) == nparts, "%s all answers revealed" % p["id"])
        ok(len(d.find_elements(By.CSS_SELECTOR, ".explain.show")) == nparts, "%s all solutions revealed" % p["id"])
        ok(len(d.find_elements(By.CSS_SELECTOR, ".katex-error")) == 0, "%s KaTeX errors after reveal" % p["id"])
        ok(not errs(), "%s console errors after reveal" % p["id"])
        # ---- lab links of this paper: open the first two and check that the lab got the data
        links = [a.get_attribute("href") for a in d.find_elements(By.XPATH, "//a[contains(.,'Check in the lab')]")]
        want = sum(1 for q in p["problems"] for pt in q if pt.get("lab"))
        ok(len(links) == want, "%s lab links: %d expected %d" % (p["id"], want, len(links)))
        for lk in links[:2]:
            d.get(lk); time.sleep(1.2)
            ok(not errs(), "%s lab link console errors" % p["id"])
            ok(len(d.find_elements(By.CSS_SELECTOR, ".out .err")) == 0, "%s lab link output error: %s" % (p["id"], d.find_element(By.CSS_SELECTOR, ".out").text[:80]))
            first = d.find_elements(By.CSS_SELECTOR, ".lab textarea, .lab input[type=text]")[0].get_attribute("value")
            ok(first.strip() != "", "%s lab link pre-filled the first field" % p["id"])
        # ---- exam mode
        load(course + "/written/paper.html?p=%s&mode=exam" % p["id"], 0.8)
        ok(len(d.find_elements(By.CSS_SELECTOR, ".callout.good")) == 0, "%s exam intro must not show answers" % p["id"])
        d.execute_script("arguments[0].click()", [b for b in d.find_elements(By.CSS_SELECTOR, "button.btn") if "Start" in b.text][0]); time.sleep(0.5)
        ok(len(d.find_elements(By.CSS_SELECTOR, ".timer")) == 1, "%s timer" % p["id"])
        ok(len(d.find_elements(By.CSS_SELECTOR, ".callout.good, .explain, details.sol")) == 0, "%s answers hidden during the exam" % p["id"])
        ok(len(d.find_elements(By.CSS_SELECTOR, ".part")) == nparts, "%s exam parts" % p["id"])
        d.execute_script("window.confirm=function(){return true}")
        d.execute_script("arguments[0].click()", [b for b in d.find_elements(By.CSS_SELECTOR, "button") if "Finish and mark" in b.text][0]); time.sleep(0.6)
        sels = d.find_elements(By.CSS_SELECTOR, "select")
        ok(len(sels) == nparts, "%s self-marking selects: %d expected %d" % (p["id"], len(sels), nparts))
        for s in sels:   # give maximum marks everywhere
            n = len(s.find_elements(By.TAG_NAME, "option")); d.execute_script("arguments[0].selectedIndex=%d; arguments[0].dispatchEvent(new Event('change'))" % (n - 1), s)
        txt = d.find_element(By.CSS_SELECTOR, ".bigscore").text
        ok(txt.startswith("20 / 20"), "%s total after full marks: %r" % (p["id"], txt))
        ok(len(d.find_elements(By.CSS_SELECTOR, ".katex-error")) == 0, "%s marking view KaTeX errors" % p["id"])
        d.execute_script("arguments[0].click()", [b for b in d.find_elements(By.CSS_SELECTOR, "button.btn") if "Save my result" in b.text][0]); time.sleep(0.3)
        hist = json.loads(d.execute_script("return localStorage.getItem('ustm:%s:history')" % course) or "[]")
        ok(any(h["id"] == "written:" + p["id"] and abs(h["score"] - 20) < 1e-9 for h in hist), "%s result saved in history" % p["id"])
    load(course + "/index.html", 1.5)
    ok("Written" in d.find_element(By.ID, "progress").text, "progress panel lists the written results")
d.quit()
print("\n%d checks, %d failures" % (checks, len(fails)))
sys.exit(1 if fails else 0)
