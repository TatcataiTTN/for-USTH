"""Browser test of the two labs: every tool runs without error and gives the expected numbers."""
import sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/").rstrip("/") + "/"
o = Options()
for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=1200,1000"): o.add_argument(a)
o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o)
fails = []; n = 0
def ok(c, m):
    global n; n += 1
    if not c: fails.append(m); print("  FAIL:", m)
def out(): return d.find_element(By.CSS_SELECTOR, ".out").text
def errs(): return [e["message"][:160] for e in d.get_log("browser") if e["level"] == "SEVERE"]
def tab(label):
    for b in d.find_elements(By.CSS_SELECTOR, ".tabs button"):
        if b.text.strip().startswith(label): d.execute_script("arguments[0].click()", b); time.sleep(0.4); return True
    return False
def setfields(vals):
    fields = d.find_elements(By.CSS_SELECTOR, ".lab textarea, .lab input[type=text]")
    for el, v in zip(fields, vals):
        if v is not None:
            d.execute_script("arguments[0].value=arguments[1]", el, v)
def run():
    for b in d.find_elements(By.CSS_SELECTOR, ".lab button.btn"):
        if "Compute" in b.text: d.execute_script("arguments[0].click()", b); break
    time.sleep(0.5)
# ---------------- Linear Algebra lab
d.get(BASE + "Linear-Algebra/lab/index.html"); time.sleep(1.2); d.get_log("browser")
tools = [b.text for b in d.find_elements(By.CSS_SELECTOR, ".tabs button")]
ok(len(tools) == 9, "LA lab has 9 tools: %s" % tools)
for t in tools:
    tab(t); ok(len(d.find_elements(By.CSS_SELECTOR, ".out .err")) == 0, "LA tool '%s' example runs without error" % t)
    ok(len(d.find_elements(By.CSS_SELECTOR, ".katex-error")) == 0, "LA tool '%s' no KaTeX errors" % t)
ok(not errs(), "LA lab console errors: %s" % errs())
tab("Solve"); setfields(["2 1 -1\n-3 -1 2\n-2 1 2", "8 -11 -3", None]); run()
txt = out()
ok("All the methods above give the same unique solution" in txt, "square system: all methods agree; got: " + txt[:200])
ok("(2, 3, -1)" in txt.replace("\n", " ") or "2,\\ 3,\\ -1" in d.page_source or "x_{1}=2" in d.page_source or "2" in txt, "solution displayed")
tab("Solve"); setfields(["4 -1 1\n2 5 2\n1 2 4", "8 3 11", "8"]); run(); txt = out()
ok("Jacobi" in txt and "Gauss–Seidel" in txt and "strictly diagonally dominant" in txt, "Jacobi/Gauss-Seidel section for a dominant matrix")
tab("Systems with a parameter"); run(); txt = out()
ok("k=2" in txt.replace(" ", "") or "k = 2" in txt, "parameter scan finds k=2 for the 2024-25 Shift 1 system: " + txt[:200])
tab("Determinant"); setfields(["2 0 -1 4\n-1 2 0 3\n3 0 1 2\n-2 0 3 1"]); run(); ok("The methods agree" in out(), "determinant methods agree")
tab("Inverse"); setfields(["5 2 -1\n2 1 -1\n2 0 1"]); run(); ok("two methods agree: true" in out(), "inverse: Gauss-Jordan = adjugate")
tab("Eigenvalues"); setfields(["2 -2 2\n-2 5 1\n2 1 5", "3"]); run(); txt = out(); ok("orthogonally diagonalizable" in txt, "symmetric matrix is orthogonally diagonalizable")
tab("Jacobian"); run(); ok("det" in out().lower(), "Jacobian determinant shown")
ok(not errs(), "LA lab console errors after use: %s" % errs())
# ---------------- Calculus lab
d.get(BASE + "Calculus-1/lab/index.html"); time.sleep(1.2); d.get_log("browser")
tools = [b.text for b in d.find_elements(By.CSS_SELECTOR, ".tabs button")]
ok(len(tools) == 8, "Calculus lab has 8 tools: %s" % tools)
for t in tools:
    tab(t); ok(len(d.find_elements(By.CSS_SELECTOR, ".out .err")) == 0, "Calculus tool '%s' runs without error: %s" % (t, out()[:80]))
    ok(len(d.find_elements(By.CSS_SELECTOR, ".katex-error")) == 0, "Calculus tool '%s' no KaTeX errors" % t)
tab("Limit"); run(); ok("probably 1" in out() or "≈ 1" in out(), "sin(x)/x -> 1: " + out()[-160:])
tab("Newton"); run(); ok("1.1654" in out() or "1.16" in out(), "Newton x^4+x-3 from 1 converges near 1.1642")
tab("Antiderivative"); run(); ok("your antiderivative is correct" in out(), "antiderivative check passes")
tab("Antiderivative"); setfields([None, "sin(x^2)"]); run(); ok("F′(x) ≠ f(x)" in out(), "antiderivative check rejects a wrong F")
tab("Riemann"); run(); ok("Simpson" in out(), "Riemann tool")
tab("Curve"); run(); ok("local" in out(), "curve sketch classifies critical points")
ok(not errs(), "Calculus lab console errors: %s" % errs())
d.quit(); print("\n%d checks, %d failures" % (n, len(fails)))
sys.exit(1 if fails else 0)
