"""Sign-in screen test with the real form and the real PBKDF2 check.
Usage:  USTM_PASS='<password>' [USTM_USER=<name>] python3 tests/gate_test.py [BASE_URL]
The password is read from the environment (USTM_USER defaults to TatcataiTTN); it is never stored in the repository.
Checks: the screen appears on a first visit to every kind of page and hides the content; wrong / empty / right credentials; the Enter key;
the browser-derived hash equals the one in shared/gate.js; the sign-in persists across pages; the username is case-insensitive;
'Sign out' brings the screen back; the screen itself fits and is readable on phone and desktop in light and dark theme."""
import json, os, sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import auth
from jschecks import CONTRAST_JS, THEME_JS

BASE = (next((a for a in sys.argv[1:]), "http://127.0.0.1:8765/")).rstrip("/") + "/"
USER = os.environ.get("USTM_USER", "TatcataiTTN"); PASS = os.environ.get("USTM_PASS")
if not PASS:
    sys.exit("set USTM_PASS (and optionally USTM_USER) to run the sign-in test")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tests", "screens"); os.makedirs(OUT, exist_ok=True)
paper = json.load(open(os.path.join(ROOT, "Linear-Algebra", "data", "papers.json"), encoding="utf-8"))[0]["id"]
ENTRY = ["index.html", "Calculus-1/index.html", "Linear-Algebra/quiz/index.html", "Calculus-1/modules/m01.html", "Calculus-1/bank/index.html",
         "Linear-Algebra/written/paper.html?p=%s" % paper, "Calculus-1/exam/run.html?exam=midterm-A", "Linear-Algebra/lab/index.html"]

fails = []; checks = 0
def ok(c, m):
    global checks
    checks += 1
    if not c:
        fails.append(m); print("  FAIL:", m)

def driver(w=1280, h=900, phone=False):
    o = Options()
    for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=%d,%d" % (w, h)): o.add_argument(a)
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    d = webdriver.Chrome(options=o)
    if phone:
        d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": w, "height": h, "deviceScaleFactor": 2, "mobile": True})
    return d

def gate_shown(d):
    return any(e.is_displayed() for e in d.find_elements(By.ID, "ustm-gate"))
def content_hidden(d):
    return d.execute_script("var m=document.querySelector('main'); return !m || getComputedStyle(m).display === 'none'")
def errors(d):
    return [e["message"][:140] for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"]]
def token(d):
    return d.execute_script("return localStorage.getItem('ustm:auth')")
def fill(d, user, pw):
    u, p = d.find_element(By.ID, "ustm-user"), d.find_element(By.ID, "ustm-pass")
    u.clear(); u.send_keys(user); p.clear(); p.send_keys(pw)
def wait_signed_in(d, secs=10):
    try:
        WebDriverWait(d, secs).until(lambda x: not gate_shown(x)); return True
    except Exception:
        return False
def err_text(d):
    return d.find_element(By.ID, "ustm-err").text

# ------------------------------------------------------------------ A. first visit: the screen covers every kind of page
d = driver()
for page in ENTRY:
    d.get_log("browser"); d.get(BASE + page); time.sleep(0.8)
    ok(gate_shown(d), "first visit to %s: the sign-in screen is not shown" % page)
    ok(content_hidden(d), "first visit to %s: the page content is visible behind the screen" % page)
    ok(not errors(d), "first visit to %s: console errors %s" % (page, errors(d)[:1]))
    ok(token(d) is None, "first visit to %s: a token exists before signing in" % page)

# ------------------------------------------------------------------ B. rejected attempts
d.get(BASE + "Calculus-1/index.html"); time.sleep(0.8)
d.find_element(By.ID, "ustm-go").click(); time.sleep(0.3)
ok("Enter your username and password" in err_text(d) and gate_shown(d), "empty form: expected a hint, got %r" % err_text(d))
fill(d, USER, PASS + "x"); d.find_element(By.ID, "ustm-go").click(); time.sleep(1.2)
ok("Wrong username or password" in err_text(d) and gate_shown(d) and token(d) is None, "wrong password was not rejected: %r" % err_text(d))
ok(d.find_element(By.ID, "ustm-pass").get_attribute("value") == "", "the password field is not cleared after a wrong attempt")
time.sleep(0.8)
fill(d, USER + "x", PASS); d.find_element(By.ID, "ustm-go").click(); time.sleep(1.2)
ok("Wrong username or password" in err_text(d) and gate_shown(d) and token(d) is None, "wrong username was not rejected: %r" % err_text(d))
# show-password toggle
d.find_element(By.ID, "ustm-pass").send_keys("abc"); d.find_element(By.ID, "ustm-show").click()
ok(d.find_element(By.ID, "ustm-pass").get_attribute("type") == "text", "show password did not reveal the field")
d.find_element(By.ID, "ustm-show").click()
ok(d.find_element(By.ID, "ustm-pass").get_attribute("type") == "password", "show password did not hide the field again")

# ------------------------------------------------------------------ C. right credentials with the Enter key
time.sleep(0.8)
fill(d, USER, PASS); d.find_element(By.ID, "ustm-pass").send_keys(Keys.ENTER)
ok(wait_signed_in(d), "right credentials were not accepted")
ok(not content_hidden(d), "the page stays hidden after signing in")
ok(token(d) == auth.TOKEN, "the hash derived by the browser differs from shared/gate.js (token %r)" % token(d))
ok(not errors(d), "console errors after signing in: %s" % errors(d)[:1])
# the page works after signing in without a reload (the quiz hub lists its sets)
ok(len(d.find_elements(By.CSS_SELECTOR, "main a, main .card")) > 0, "no content after signing in")

# ------------------------------------------------------------------ D. the sign-in persists across pages and reloads
for page in ["Calculus-1/index.html", "Linear-Algebra/index.html", "Calculus-1/modules/m01.html", "Linear-Algebra/written/paper.html?p=%s" % paper, "index.html"]:
    d.get(BASE + page); time.sleep(0.7)
    ok(not gate_shown(d) and not content_hidden(d), "after signing in, %s shows the sign-in screen again" % page)

# ------------------------------------------------------------------ E. sign out brings the screen back
d.get(BASE + "Calculus-1/index.html"); time.sleep(0.7)
d.execute_script("document.querySelector('details.menu summary').click()"); time.sleep(0.2)
btn = d.find_elements(By.CSS_SELECTOR, "[data-logout]")
ok(len(btn) == 1, "no 'Sign out' button in the Display menu")
if btn:
    d.execute_script("arguments[0].click()", btn[0]); time.sleep(1.0)
    ok(gate_shown(d) and token(d) is None, "'Sign out' did not bring the sign-in screen back")
d.quit()

# ------------------------------------------------------------------ F. the username is not case-sensitive
for variant in (USER.lower(), USER.upper()):
    d = driver(); d.get(BASE + "Calculus-1/index.html"); time.sleep(0.8)
    fill(d, " " + variant + " ", PASS); d.find_element(By.ID, "ustm-go").click()
    ok(wait_signed_in(d), "username %r was not accepted" % variant)
    d.quit()

# ------------------------------------------------------------------ G. the screen itself: fits and readable (light/dark x phone/desktop)
for theme in ("light", "dark"):
    for label, (w, h, phone) in (("phone", (390, 844, True)), ("desktop", (1280, 900, False))):
        d = driver(w, h, phone)
        d.get(BASE + "index.html"); d.execute_script("localStorage.setItem('ustm:theme', JSON.stringify(%r))" % theme)
        d.get(BASE + "Calculus-1/index.html"); time.sleep(0.9)
        tag = "[%s %s]" % (theme, label)
        ok(gate_shown(d), "%s sign-in screen not shown" % tag)
        l, r_, t_, b_, vw, vh = d.execute_script("var r=document.querySelector('#ustm-gate form').getBoundingClientRect(); return [r.left, r.right, r.top, r.bottom, document.documentElement.clientWidth, window.innerHeight]")
        ok(l >= 0 and r_ <= vw, "%s the form is wider than the screen: %.0f..%.0f of %d" % (tag, l, r_, vw))
        ok(b_ <= vh + 1 or h < 700, "%s the form does not fit the height: bottom %.0f of %d" % (tag, b_, vh))
        sw, iw = d.execute_script("return [document.documentElement.scrollWidth, window.innerWidth]")
        ok(sw <= iw + 1 and (not phone or iw == w), "%s horizontal overflow or wrong viewport (%d / %d)" % (tag, sw, iw))
        attr, lum = d.execute_script(THEME_JS)
        ok(attr == theme and (lum > 0.6 if theme == "light" else lum < 0.15), "%s the %s theme is not in effect (data-theme=%s, luminance %.2f)" % (tag, theme, attr, lum))
        low = d.execute_script(CONTRAST_JS)
        ok(not low, "%s low-contrast text on the sign-in screen: %s" % (tag, low))
        for sel in ("#ustm-user", "#ustm-pass", "#ustm-go"):
            r = d.execute_script("var e=document.querySelector(arguments[0]); var r=e.getBoundingClientRect(); return [r.left, r.right, r.height]", sel)
            ok(r[0] >= 0 and r[1] <= vw and r[2] >= 36, "%s %s is cut off or too small to tap: %s" % (tag, sel, r))
        d.save_screenshot(os.path.join(OUT, "gate_%s_%s.png" % (theme, label)))
        d.quit()

print("\n%d checks, %d failures" % (checks, len(fails)))
sys.exit(1 if fails else 0)
