# for-USTH — self-study and exam-training sites for USTH B1 mathematics

Static sites (no backend) built from the USTH course documents of MAT1.001 *Calculus I* and MAT1.002 *Linear Algebra*.

* `Calculus-1/` → https://tatcataittn.github.io/for-USTH/Calculus-1/
* `Linear-Algebra/` → https://tatcataittn.github.io/for-USTH/Linear-Algebra/

Each course site has: chapter quizzes (3 sets per chapter), 3 mock midterms (20 questions, 50 min, forward-only), 3 speed exams (30 questions, 20 min), a filterable practice bank with a source on every question, 13 / 7 study modules with USTH-DSES style slides, interactive labs (exact multi-method solvers for Linear Algebra, plots and numeric tools for Calculus), written practice (past or mock finals with full worked solutions, exam mode with timer and self-marking) and a Sources page (documents read, coverage, errors found in the course materials).

## Layout

* `shared/` — engines (quiz / exam / bank / written / labs / slides / progress), styles, vendored KaTeX and math.js (offline, no CDN at runtime)
* `build/` — Python generators: question banks (`gen_cal*.py`, `gen_la*.py`, sympy-verified), quiz sets and papers (`build_data.py`), module slides, page templates (`build_site.py`)
* `tests/` — KaTeX check of every formula, exact Linear Algebra library cross-check, Selenium end-to-end suites, slide layout check, screenshot helpers

## Rebuild and test

```
cd build && python3 build_data.py && python3 build_site.py        # needs sympy, numpy, mpmath
node tests/katex_check.js && node tests/la_cross_check.js        # syntax of all math; exact LA library vs sympy
python3 -m http.server 8765 &                                     # then, with Chrome + selenium installed:
python3 tests/site_test.py; python3 tests/lab_test.py; python3 tests/written_test.py; python3 tests/deck_check.py
```

Every answer is computed by code and checked a second way (exact arithmetic, numerical quadrature or an explicit counterexample); the build stops when a check fails.

Unofficial study material. Textbooks and lecture slides are not included; problem statements are paraphrased and cited.
