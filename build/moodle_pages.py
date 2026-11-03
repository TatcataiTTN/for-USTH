# -*- coding: utf-8 -*-
"""Linear Algebra: worked solutions for the Moodle chapter quizzes and the mock midterm, with practice variants (similar, harder, different angle).
Content lives in build/moodle_la/ch1..ch4.py (bilingual); every variant carries a `chk` that is evaluated at build time, so a wrong typed answer stops the build.
Writes Linear-Algebra/moodle/index.html and Linear-Algebra/moodle/ch1..ch4.html."""
import os
from sitegen import *
from lecture_pages import LANG_HEAD, bi

LA_SETS = [("ch1", "Quiz Chapter 1", "Quiz chương 1", "Linear systems and Gaussian elimination", "Hệ phương trình tuyến tính và khử Gauss", "ch1"),
           ("ch2", "Quiz Chapter 2", "Quiz chương 2", "Matrices and inverses", "Ma trận và nghịch đảo", "ch2"),
           ("ch3", "Quiz Chapter 3", "Quiz chương 3", "Determinants", "Định thức", "ch3"),
           ("ch4", "Quiz Chapter 4", "Quiz chương 4", "Vector spaces, rank, eigenvalues", "Không gian vectơ, hạng, trị riêng", "ch4")]
LA_MOCK = ("Mock midterm", "Solved in item", [("Q1", "2.9 (Q14)"), ("Q2", "2.2"), ("Q3", "4.5"), ("Q4", "4.3 (Q9)"), ("Q5", "4.2 (Q12)"), ("Q6", "1.9 (Q15)"), ("Q7", "2.6 (figure missing)"), ("Q8", "3.4"), ("Q9", "1.1"), ("Q10", "1.2"),
        ("Q11", "4.9"), ("Q12", "1.10"), ("Q13", "2.2"), ("Q14", "4.8"), ("Q15", "3.10"), ("Q16", "4.6"), ("Q17", "2.9 (Q13)"), ("Q18", "2.7"), ("Q19", "4.2 (Q2)"), ("Q20", "4.3 (Q8)")],
          "All 20 mock questions reuse questions of the four chapter quizzes; find them here.", "20 câu mock đều lấy từ bốn quiz chương; xem tương ứng ở đây.")
LA_HOWTO = ("Every question of the four Moodle chapter quizzes and of the mock midterm, solved step by step with the rule behind each move, and followed by practice variants "
         "(★ same idea, ★★ harder, ★★★ a different angle). Open the green boxes for answers. The buttons at the bottom right switch English / Vietnamese.",
         "Mọi câu hỏi của bốn quiz chương trên Moodle và của mock midterm, giải từng bước kèm quy tắc đằng sau mỗi bước, rồi đến các câu tương tự "
         "(★ cùng ý, ★★ khó hơn, ★★★ góc nhìn khác). Bấm vào ô xanh để xem đáp án. Các nút ở góc dưới bên phải chuyển Anh / Việt.")
LA_FLAGS = [("1.4 and 2.6", "The pictures (a flow network and two grade matrices) did not load in the PDFs you shared, so these two questions are explained by method and a worked example.", "Hình (mạng dòng chảy và hai ma trận điểm) không hiện trong PDF đã gửi nên hai câu này được giải bằng phương pháp và ví dụ."),
         ("3.4", "$x=0$ also satisfies $\\det(A^2)=64$; among the options only $\\pm4$ is offered.", "$x=0$ cũng thoả $\\det(A^2)=64$; trong các đáp án chỉ có $\\pm4$."),
         ("4.9", "The keyed answer is a <i>column</i>-space basis, not a row-space basis; option (d) is also a valid column-space basis.", "Đáp án của đề là cơ sở không gian <i>cột</i>, không phải không gian hàng; đáp án (d) cũng là cơ sở hợp lệ của không gian cột."),
         ("4.3", "$P_3$ is taken as polynomials of degree $\\le3$ (dimension 4), following the key.", "$P_3$ hiểu là đa thức bậc $\\le3$ (chiều 4), theo đáp án của đề.")]

PH_HOWTO = ("Every question of the Moodle quizzes you added, solved step by step with the law behind each move, then practice variants (★ same idea, ★★ harder, ★★★ another angle). "
            "Answers are recomputed by program. Where the quiz figure did not load or the quiz has no key, the page says so. Buttons at the bottom right switch English / Vietnamese.",
            "Mọi câu hỏi của các quiz Moodle bạn đã thêm, giải từng bước kèm định luật đằng sau mỗi bước, rồi các câu tương tự (★ cùng ý, ★★ khó hơn, ★★★ góc nhìn khác). "
            "Đáp án được chương trình tính lại. Chỗ nào hình của đề không hiện hoặc đề không có đáp án, trang đều ghi rõ. Các nút ở góc dưới bên phải chuyển Anh / Việt.")
PH1_SETS = [("mock", "Mocktest Midterm", "Mock giữa kỳ", "20 questions · the quiz shows the key", "20 câu · đề có đáp án", "mock"),
            ("final", "Exercises for Final Exam", "Bài tập cuối kỳ", "40 questions · the quiz shows the key", "40 câu · đề có đáp án", "final")]
PH1_MOCK = ("Repeated questions", "Same as", [("E26 (final Q26)", "M06"), ("E36 (final Q36)", "M16"), ("E39 (final Q39)", "M03 (concept)"), ("E27 (final Q27)", "M09 (same masses, smooth vs rough)")],
            "A few exercises repeat or echo mock questions; the solution is given once and cross-referenced.", "Một vài bài tập lặp lại hoặc gần giống câu mock; lời giải ghi một lần và dẫn chiếu.")
PH1_FLAGS = [("M04, M09", "The pictures (grid paths, pulley set-up) did not load in the PDF; explained by method.", "Hình (đường đi trên lưới, ròng rọc) không hiện trong PDF; giải bằng phương pháp."),
             ("M17", "Figure axis is labelled $a$ while the text speaks of velocity; the key follows the text.", "Trục hình ghi $a$ nhưng đề nói vận tốc; đáp án theo phần chữ."),
             ("E05", "$Q=T\\Delta S=405\\ \\mathrm{K}\\times46.0=1.86\\times10^4$ J; the quiz keys $1.84\\times10^4$ J (closest option).", "$Q=T\\Delta S=405\\ \\mathrm{K}\\times46{,}0=1{,}86\\times10^4$ J; đề cho $1{,}84\\times10^4$ J (đáp án gần nhất)."),
             ("E21, E22, E27", "Answer depends on the speed of sound / sign convention / a missing figure; read the notes on each item.", "Đáp án phụ thuộc tốc độ âm / quy ước dấu / hình bị mất; đọc ghi chú ở từng mục."),
             ("E03, E09, E10, E14, E18, E25, E31, E38, E39", "Figures missing in the PDF: method and the keyed answer are given.", "Hình bị mất trong PDF: nêu phương pháp và đáp án của đề.")]
PH2_SETS = [("final", "Mocktest for Final exam", "Mock cuối kỳ", "40 questions · the quiz shows NO key (we computed every answer)", "40 câu · đề KHÔNG có đáp án (chúng tôi tính từng câu)", "final")]
PH2_MOCK = ("Questions to double-check", "Why", [("F08", "dipole midpoint: ambiguous wording"), ("F15", "straight-edge diffraction: outside the taught scope"), ("F24", "convex mirror: correct 12.0 cm is not an option"), ("F25", "ultrasound refraction: correct 46.7° is not an option")],
            "Four items are flawed; the physics and the reason are written on each page.", "Bốn câu có lỗi đề; vật lý và lý do ghi ở từng trang.")
PH2_FLAGS = [("All 40", "The quiz review printed no answer key, so every answer here is computed from the formulas and checked a second way (numerically or by a limiting case).", "Bản xem lại của quiz không in đáp án nên mọi đáp án ở đây do chúng tôi tính từ công thức và kiểm lại bằng cách thứ hai."),
             ("F11", "Radii $b,c$ and the shell charge are cut off in the PDF; taken from the source problem (Halliday).", "Bán kính $b,c$ và điện tích vỏ bị cắt trong PDF; lấy từ bài gốc (Halliday)."),
             ("F08, F15, F24, F25", "Flawed items: see the red notes on the pages.", "Các câu có lỗi: xem ghi chú trên từng trang.")]

COURSE_SETS = {
    "Linear-Algebra": dict(pkg="moodle_la", sets=LA_SETS, mock=LA_MOCK, flags=LA_FLAGS, howto=LA_HOWTO, title=("Moodle quizzes: worked solutions", "Quiz Moodle: lời giải chi tiết"), flagtitle=("Things to know about the quizzes", "Điều cần biết về các quiz")),
    "Physics-1": dict(pkg="moodle_ph1", sets=PH1_SETS, mock=PH1_MOCK, flags=PH1_FLAGS, howto=PH_HOWTO, title=("Moodle mock tests: worked solutions", "Mock Moodle: lời giải chi tiết"), flagtitle=("Things to know about these quizzes", "Điều cần biết về các quiz này")),
    "Physics-2": dict(pkg="moodle_ph2", sets=PH2_SETS, mock=PH2_MOCK, flags=PH2_FLAGS, howto=PH_HOWTO, title=("Moodle mock final: worked solutions", "Mock cuối kỳ Moodle: lời giải chi tiết"), flagtitle=("Things to know about this quiz", "Điều cần biết về quiz này")),
}

def load_items(course):
    import importlib
    cfg = COURSE_SETS[course]
    return {c[0]: importlib.import_module(cfg["pkg"] + "." + c[5]).ITEMS for c in cfg["sets"]}

def sc(en, vi):
    return '<div class="sc en" lang="en"><span class="lab">EN</span>%s</div><div class="sc vi" lang="vi"><span class="lab">VI</span>%s</div>' % (en, vi)

def item_html(it, ch):
    o = ['<section class="lslide mq" id="q%s"><div class="lhead"><span class="num">%s</span><h3>%s</h3><span class="lvl v1">%s</span></div>' % (it.id.replace(".", "-"), it.id, bi(it.title[0], it.title[1]), esc(it.src) + ((" · Mock " + esc(it.mock)) if it.mock and "Mock" not in it.src else ""))]
    q = sc(it.q[0], it.q[1])
    if it.choices:
        q += '<ul class="mqch">' + "".join('<li><b>%s.</b> %s</li>' % ("abcd"[i], c) for i, c in enumerate(it.choices)) + "</ul>"
    o.append('<div class="mqq">%s</div>' % q)
    if it.chk is not None:
        assert it.chk(), "main answer check failed: %s" % it.id
    o.append('<div class="mqkey"><b>%s:</b> %s</div>' % (bi(*(it.klabel or ("Official answer (verified by us)", "Đáp án của đề (đã được kiểm tra lại)"))), it.key))
    steps = "".join(sc("<b>%s %d.</b> %s" % ("Step", n, e), "<b>%s %d.</b> %s" % ("Bước", n, v)) for n, (e, v) in enumerate(it.steps, 1))
    o.append('<details class="sol" open><summary>%s</summary>%s</details>' % (bi("Worked solution", "Lời giải chi tiết"), steps))
    if it.trap:
        o.append('<div class="why"><b>%s</b>%s</div>' % (bi("Traps", "Bẫy"), sc(*it.trap)))
    if it.note:
        o.append('<div class="why mqnote"><b>%s</b>%s</div>' % (bi("Note", "Lưu ý"), sc(*it.note)))
    for n, v in enumerate(it.variants or [], 1):
        assert v.chk(), "variant check failed: %s #%d" % (it.id, n)
        ans = v.ans() if callable(v.ans) else v.ans; sol = v.sol() if callable(v.sol) else v.sol
        o.append('<div class="ex"><div class="exh">%s %s.%d <span class="lvl v2">%s</span> <span class="tag okt">%s</span></div>%s<details class="sol"><summary>%s</summary><p><b>%s:</b> %s</p>%s</details></div>' % (
            bi("Practice", "Luyện tập"), it.id, n, v.lvl, bi("✓ answer checked by computer algebra", "✓ đáp án đã kiểm tra bằng máy"), sc(*v.q), bi("Answer and solution", "Đáp án và lời giải"), bi("Answer", "Đáp án"), ans, sc(*sol)))
    o.append("</section>")
    return "".join(o)

FAB = ('<div class="langfab" role="group" aria-label="Language"><button type="button" data-lang-set="en">EN</button><button type="button" data-lang-set="both">EN + VI</button>'
       '<button type="button" data-lang-set="vi">VI</button><button type="button" id="solall" title="Open / close all solutions · Mở / đóng mọi lời giải">%s</button></div>' % bi("Solutions", "Lời giải"))

def any_pages(course):
    return course in COURSE_SETS and os.path.isdir(os.path.join(ROOT, "build", COURSE_SETS[course]["pkg"]))

def build(course, have):
    cfg = COURSE_SETS[course]; SETS = cfg["sets"]
    data = load_items(course); total = sum(len(v) for v in data.values()); nvar = sum(len(i.variants or []) for v in data.values() for i in v)
    cards = ""
    for ci, (cid, ten, tvi, sub_en, sub_vi, _mod) in enumerate(SETS):
        items = data[cid]
        toc = "".join('<a class="v2" href="#q%s"><b>%s</b> %s</a>' % (i.id.replace(".", "-"), i.id, bi(i.title[0], i.title[1])) for i in items)
        prev = SETS[ci - 1][0] if ci else None; nxt = SETS[ci + 1][0] if ci + 1 < len(SETS) else None
        links = ('<a class="btn alt" href="%s.html">◀ %s</a>' % (prev, prev) if prev else "") + ('<a class="btn alt" href="%s.html">%s ▶</a>' % (nxt, nxt) if nxt else "")
        pdfname = "%s_Moodle-%s" % (course, cid)
        body = ('<p class="muted"><a href="index.html">%s</a> › %s</p><h1>%s · %s</h1><div class="callout"><b>PDF:</b> <a href="pdf/%s.pdf">%s.pdf</a> (print-ready, English + Vietnamese)</div>'
                '<details class="toc" open><summary>%s (%d)</summary><div class="tocgrid">%s</div></details>%s<div class="row">%s</div>%s') % (
            bi("Moodle review", "Ôn Moodle"), cid, bi(ten, tvi, False), bi(sub_en, sub_vi, False), pdfname, pdfname,
            bi("Questions", "Các câu hỏi"), len(items), toc, "".join(item_html(i, cid) for i in items), links, FAB)
        write("%s/moodle/%s.html" % (course, cid), page(course, ten, body, 1, "moodle", scripts=["lectures.js"], css=["lectures.css", "moodle.css"], desc="%s: worked solutions and practice variants" % ten, extra_head=LANG_HEAD, have=have))
        cards += '<a class="card" href="%s.html"><b>%s</b><span>%s · %d questions solved · %d practice variants</span></a>' % (cid, bi(ten, tvi, False), esc(sub_en), len(items), sum(len(i.variants or []) for i in items))
    mt, mh, mrows, men, mvi = cfg["mock"]
    mock = "".join("<tr><td>%s</td><td>%s</td></tr>" % (esc(a), esc(b)) for a, b in mrows)
    flags = "".join("<li><b>%s</b> — %s<br><span class='muted'>%s</span></li>" % (a, b, c) for a, b, c in cfg["flags"])
    body = ('<h1>%s</h1>%s<div class="cards">%s</div>'
            '<h2>%s</h2><p>%s</p><table class="tbl"><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>'
            '<h2>%s</h2><ul>%s</ul><div class="row">%s</div>') % (
        bi(*cfg["title"]), sc(*cfg["howto"]), cards,
        bi(mt, mt), bi(men, mvi), mt, mh, mock,
        bi(*cfg["flagtitle"]), flags, FAB)
    write("%s/moodle/index.html" % course, page(course, "Moodle review", body, 1, "moodle", scripts=["lectures.js"], css=["lectures.css", "moodle.css"], extra_head=LANG_HEAD, have=have))
    return total, nvar
