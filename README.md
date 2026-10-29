# for-USTH — self-study and exam-training sites for USTH B1 mathematics and physics

Static sites (no backend) built from the USTH course documents of MAT1.001 *Calculus I*, MAT1.002 *Linear Algebra*, PHY1.001 *Fundamental Physics I* and PHY1.002 *Fundamental Physics II*.

* `Calculus-1/` → https://tatcataittn.github.io/for-USTH/Calculus-1/
* `Linear-Algebra/` → https://tatcataittn.github.io/for-USTH/Linear-Algebra/
* `Physics-1/` → https://tatcataittn.github.io/for-USTH/Physics-1/
* `Physics-2/` → https://tatcataittn.github.io/for-USTH/Physics-2/

Each course site has: chapter quizzes (3 sets per chapter), 3 mock midterms (20 questions, forward-only), 3 speed exams (30 questions, 20 min; the two Physics sites also have 3 mock finals of 40 questions, because their finals are multiple choice), a filterable practice bank with a source on every question, 13 / 7 study modules with USTH-DSES style slides, interactive labs (exact multi-method solvers for Linear Algebra, plots and numeric tools for Calculus), written practice (past or mock finals with full worked solutions, exam mode with timer and self-marking) and a Sources page (documents read, coverage, errors found in the course materials).

## Layout

* `shared/` — engines (quiz / exam / bank / written / labs / slides / progress), styles, vendored KaTeX and math.js (offline, no CDN at runtime)
* `build/` — Python generators: question banks (`gen_cal*.py`, `gen_la*.py` sympy-verified; `gen_ph1_*.py`, `gen_ph2_*.py` verified by a second physical route, with generated SVG figures from `figs.py`), quiz sets and papers (`build_data.py`, `build_data_phys.py`), module slides, page templates (`build_site.py`)
* `tests/` — KaTeX check of every formula, exact Linear Algebra library cross-check, Selenium end-to-end suites, slide layout check, screenshot helpers

## Sign-in screen

Every page first shows a sign-in screen in a new browser (`shared/gate.js`). After signing in it is remembered on that browser, and *Display → Sign out* brings it back.
It is a convenience gate, not real protection: the sites are static, so the check runs in the browser and the pages and data files stay reachable by their URLs.
Only a salted PBKDF2 hash is stored in the repository, never the password. Change the credentials with `python3 build/set_password.py`.

## Rebuild and test

```
cd build && python3 build_data.py && python3 build_data_phys.py && python3 build_site.py    # needs sympy, numpy, scipy, mpmath
python3 build/audit_phys.py                                       # every numeric Physics answer must appear, with the same rounding, in its worked explanation
node tests/katex_check.js && node tests/la_cross_check.js        # syntax of all math; exact LA library vs sympy
python3 -m http.server 8765 &                                     # then, with Chrome + selenium installed:
python3 tests/site_test.py; python3 tests/lab_test.py; python3 tests/written_test.py; python3 tests/deck_check.py
python3 tests/layout_check.py                                     # both courses x light/dark x phone (390 px)/desktop: overflow, contrast, menu
USTM_PASS='<password>' python3 tests/gate_test.py                 # the real sign-in form (password only from the environment)
```

The other Selenium suites sign in with the public hash stored in `shared/gate.js` (`tests/auth.py`), so they never need the password. Each script takes a base URL, so the same suites run against the deployed site.

Every answer is computed by code and checked a second way (exact arithmetic, numerical quadrature or an explicit counterexample); the build stops when a check fails.

Unofficial study material. Textbooks and lecture slides are not included; problem statements are paraphrased and cited.
