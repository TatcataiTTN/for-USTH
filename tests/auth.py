"""Sign-in helper for the Selenium tests. The sites show a sign-in screen until localStorage['ustm:auth'] holds the hash stored in
shared/gate.js. That hash is public (it is in the page source), so the tests do not need the password; only tests/gate_test.py
exercises the real sign-in form and reads the password from the USTM_PASS environment variable."""
import os, re

_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared", "gate.js")
TOKEN = re.search(r"hash: '([0-9a-f]{64})'", open(_GATE, encoding="utf-8").read()).group(1)
SET_JS = "localStorage.setItem('ustm:auth', '%s')" % TOKEN

def prime(driver, base):
    """A fresh browser profile is signed out: open the home page once and store the token for this origin."""
    driver.get(base.rstrip("/") + "/index.html")
    driver.execute_script(SET_JS)
