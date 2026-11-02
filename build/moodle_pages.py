# -*- coding: utf-8 -*-
"""Linear Algebra: worked solutions for the Moodle chapter quizzes and the mock midterm, with practice variants (similar, harder, different angle).
Content lives in build/moodle_la/ch1..ch4.py (bilingual); every variant carries a `chk` that is evaluated at build time, so a wrong typed answer stops the build.
Writes Linear-Algebra/moodle/index.html and Linear-Algebra/moodle/ch1..ch4.html."""
import os
from sitegen import *
from lecture_pages import LANG_HEAD, bi

CHAPTERS = [("ch1", "Quiz Chapter 1", "Quiz chương 1", "Linear systems and Gaussian elimination", "Hệ phương trình tuyến tính và khử Gauss"),
            ("ch2", "Quiz Chapter 2", "Quiz chương 2", "Matrices and inverses", "Ma trận và nghịch đảo"),
            ("ch3", "Quiz Chapter 3", "Quiz chương 3", "Determinants", "Định thức"),
            ("ch4", "Quiz Chapter 4", "Quiz chương 4", "Vector spaces, rank, eigenvalues", "Không gian vectơ, hạng, trị riêng")]
MOCK = [("1", "2.9 (Q14)"), ("2", "2.2"), ("3", "4.5"), ("4", "4.3 (Q9)"), ("5", "4.2 (Q12)"), ("6", "1.9 (Q15)"), ("7", "2.6 (figure missing)"), ("8", "3.4"), ("9", "1.1"), ("10", "1.2"),
        ("11", "4.9"), ("12", "1.10"), ("13", "2.2"), ("14", "4.8"), ("15", "3.10"), ("16", "4.6"), ("17", "2.9 (Q13)"), ("18", "2.7"), ("19", "4.2 (Q2)"), ("20", "4.3 (Q8)")]
HOWTO = ("Every question of the four Moodle chapter quizzes and of the mock midterm, solved step by step with the rule behind each move, and followed by practice variants "
         "(★ same idea, ★★ harder, ★★★ a different angle). Open the green boxes for answers. The buttons at the bottom right switch English / Vietnamese.",
         "Mọi câu hỏi của bốn quiz chương trên Moodle và của mock midterm, giải từng bước kèm quy tắc đằng sau mỗi bước, rồi đến các câu tương tự "
         "(★ cùng ý, ★★ khó hơn, ★★★ góc nhìn khác). Bấm vào ô xanh để xem đáp án. Các nút ở góc dưới bên phải chuyển Anh / Việt.")
FLAGS = [("1.4 and 2.6", "The pictures (a flow network and two grade matrices) did not load in the PDFs you shared, so these two questions are explained by method and a worked example.", "Hình (mạng dòng chảy và hai ma trận điểm) không hiện trong PDF đã gửi nên hai câu này được giải bằng phương pháp và ví dụ."),
         ("3.4", "$x=0$ also satisfies $\\det(A^2)=64$; among the options only $\\pm4$ is offered.", "$x=0$ cũng thoả $\\det(A^2)=64$; trong các đáp án chỉ có $\\pm4$."),
         ("4.9", "The keyed answer is a <i>column</i>-space basis, not a row-space basis; option (d) is also a valid column-space basis.", "Đáp án của đề là cơ sở không gian <i>cột</i>, không phải không gian hàng; đáp án (d) cũng là cơ sở hợp lệ của không gian cột."),
         ("4.3", "$P_3$ is taken as polynomials of degree $\\le3$ (dimension 4), following the key.", "$P_3$ hiểu là đa thức bậc $\\le3$ (chiều 4), theo đáp án của đề.")]

def load_items():
    import importlib
    return {c[0]: importlib.import_module("moodle_la." + c[0]).ITEMS for c in CHAPTERS}

def sc(en, vi):
    return '<div class="sc en" lang="en"><span class="lab">EN</span>%s</div><div class="sc vi" lang="vi"><span class="lab">VI</span>%s</div>' % (en, vi)

def item_html(it, ch):
    o = ['<section class="lslide mq" id="q%s"><div class="lhead"><span class="num">%s</span><h3>%s</h3><span class="lvl v1">%s</span></div>' % (it.id.replace(".", "-"), it.id, bi(it.title[0], it.title[1]), esc(it.src) + ((" · Mock " + esc(it.mock)) if it.mock and "Mock" not in it.src else ""))]
    q = sc(it.q[0], it.q[1])
    if it.choices:
        q += '<ul class="mqch">' + "".join('<li><b>%s.</b> %s</li>' % ("abcd"[i], c) for i, c in enumerate(it.choices)) + "</ul>"
    o.append('<div class="mqq">%s</div>' % q)
    o.append('<div class="mqkey"><b>%s:</b> %s</div>' % (bi("Official answer (verified by us)", "Đáp án của đề (đã được kiểm tra lại)"), it.key))
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
    return course == "Linear-Algebra" and os.path.isdir(os.path.join(ROOT, "build", "moodle_la"))

def build(course, have):
    data = load_items(); total = sum(len(v) for v in data.values()); nvar = sum(len(i.variants or []) for v in data.values() for i in v)
    cards = ""
    for ci, (cid, ten, tvi, sub_en, sub_vi) in enumerate(CHAPTERS):
        items = data[cid]
        toc = "".join('<a class="v2" href="#q%s"><b>%s</b> %s</a>' % (i.id.replace(".", "-"), i.id, bi(i.title[0], i.title[1])) for i in items)
        prev = CHAPTERS[ci - 1][0] if ci else None; nxt = CHAPTERS[ci + 1][0] if ci + 1 < len(CHAPTERS) else None
        links = ('<a class="btn alt" href="%s.html">◀ %s</a>' % (prev, prev) if prev else "") + ('<a class="btn alt" href="%s.html">%s ▶</a>' % (nxt, nxt) if nxt else "")
        body = ('<p class="muted"><a href="index.html">%s</a> › %s</p><h1>%s · %s</h1><div class="callout"><b>PDF:</b> <a href="pdf/%s.pdf">%s.pdf</a> (print-ready, English + Vietnamese)</div>'
                '<details class="toc" open><summary>%s (%d)</summary><div class="tocgrid">%s</div></details>%s<div class="row">%s</div>%s') % (
            bi("Moodle review", "Ôn Moodle"), cid, bi(ten, tvi, False), bi(sub_en, sub_vi, False), "Linear-Algebra_Moodle-" + cid, "Linear-Algebra_Moodle-" + cid,
            bi("Questions", "Các câu hỏi"), len(items), toc, "".join(item_html(i, cid) for i in items), links, FAB)
        write("%s/moodle/%s.html" % (course, cid), page(course, ten, body, 1, "moodle", scripts=["lectures.js"], css=["lectures.css", "moodle.css"], desc="%s: worked solutions and practice variants" % ten, extra_head=LANG_HEAD, have=have))
        cards += '<a class="card" href="%s.html"><b>%s</b><span>%s · %d questions solved · %d practice variants</span></a>' % (cid, bi(ten, tvi, False), esc(sub_en), len(items), sum(len(i.variants or []) for i in items))
    mock = "".join("<tr><td>Q%s</td><td>%s</td></tr>" % (a, esc(b)) for a, b in MOCK)
    flags = "".join("<li><b>%s</b> — %s<br><span class='muted'>%s</span></li>" % (a, b, c) for a, b, c in FLAGS)
    body = ('<h1>%s</h1>%s<div class="cards">%s</div>'
            '<h2>%s</h2><p>%s</p><table class="tbl"><thead><tr><th>Mock midterm</th><th>%s</th></tr></thead><tbody>%s</tbody></table>'
            '<h2>%s</h2><ul>%s</ul><div class="row">%s</div>') % (
        bi("Moodle quizzes: worked solutions", "Quiz Moodle: lời giải chi tiết"), sc(*HOWTO), cards,
        bi("Mock midterm map", "Bản đồ mock midterm"), bi("All 20 mock questions reuse questions of the four chapter quizzes; find them here.", "20 câu mock đều lấy từ bốn quiz chương; xem tương ứng ở đây."), bi("Solved in item", "Lời giải ở mục"), mock,
        bi("Things to know about the quizzes", "Điều cần biết về các quiz"), flags, FAB)
    write("%s/moodle/index.html" % course, page(course, "Moodle review", body, 1, "moodle", scripts=["lectures.js"], css=["lectures.css", "moodle.css"], extra_head=LANG_HEAD, have=have))
    return total, nvar
