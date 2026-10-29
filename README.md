# for-USTH — self-study and exam-training sites for USTH B1 mathematics

Static sites (no backend) built from the USTH course documents of MAT1.001 *Calculus I* and MAT1.002 *Linear Algebra*.

* `Calculus-1/` → https://tatcataittn.github.io/for-USTH/Calculus-1/
* `Linear-Algebra/` → https://tatcataittn.github.io/for-USTH/Linear-Algebra/
* `shared/` — engines (quiz / exam / bank / progress), styles, vendored KaTeX and math.js (offline, no CDN at runtime)
* `build/` — Python generators: question banks (sympy-verified), quiz sets, past-paper solutions, page templates
* `tests/` — KaTeX syntax check of the whole bank, browser end-to-end test (Selenium)

Rebuild: `cd build && python3 build_data.py && python3 build_site.py` (needs `sympy`, `numpy`).
Test: `node tests/katex_check.js`; serve with `python3 -m http.server 8765` and run `python3 tests/site_test.py`.

Unofficial study material. Textbooks and lecture slides are not included; problem statements are paraphrased and cited.
