# -*- coding: utf-8 -*-
"""Set the credentials of the sign-in screen (shared/gate.js).

Usage:  python3 build/set_password.py                                   (asks for the username and the password)
        USTM_USER=name USTM_PASS=secret python3 build/set_password.py   (non-interactive)

Only a salted PBKDF2-SHA256 hash is written to gate.js; the password itself is never stored. Remember that the gate is a
convenience screen on a static site, not real protection (see the note at the top of gate.js)."""
import getpass, hashlib, os, re, sys

ITER = 200_000
GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared", "gate.js")

def derive(user, password, salt, iterations=ITER):
    """Must match derive() in gate.js: PBKDF2-SHA256, 256 bits, over lower(trim(user)) + newline + password."""
    return hashlib.pbkdf2_hmac("sha256", (user.strip().lower() + "\n" + password).encode("utf-8"), salt, iterations, dklen=32)

def main():
    user = os.environ.get("USTM_USER") or input("Username: ")
    password = os.environ.get("USTM_PASS") or getpass.getpass("Password: ")
    if not user.strip() or not password:
        sys.exit("username and password must not be empty")
    salt = os.urandom(16)
    cfg = "var CFG = {salt: '%s', iter: %d, hash: '%s'}; // GATE-CONFIG (rewritten by build/set_password.py)" % (salt.hex(), ITER, derive(user, password, salt).hex())
    src = open(GATE, encoding="utf-8").read()
    new, n = re.subn(r"var CFG = \{.*?\}; // GATE-CONFIG[^\n]*", lambda m: cfg, src)
    if n != 1:
        sys.exit("the GATE-CONFIG line was not found in shared/gate.js")
    with open(GATE, "w", encoding="utf-8") as f:
        f.write(new)
    print("shared/gate.js updated for user %r" % user.strip().lower())

if __name__ == "__main__":
    main()
