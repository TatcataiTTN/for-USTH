# -*- coding: utf-8 -*-
"""Lecture walkthrough pages: the lecturers' original slides one by one with a bilingual teaching script, a value level and exercises.
Lecture files live in build/lectures/ (cal_L01.py ...); this module checks them (every slide covered once, every image present,
every exercise check true) and writes <course>/lectures/index.html and <course>/lectures/<id>.html."""
import importlib, os, re
from PIL import Image
from sitegen import *
from lec_lib import fmt, run_check, LEVELS

# course -> (file prefix, original PDF name on the site, [(lecture id, number of slides in the original deck)])
CATALOGUE = {
    "Calculus-1": ("cal", "Calculus-I_Lecture-%s.pdf", [("L01", 47), ("L02", 51), ("L03", 46), ("L04", 44), ("L05", 54), ("L06", 44), ("L07", 46), ("L08", 67), ("L09", 46), ("L10a", 19), ("L10b", 17), ("L11", 30), ("L12", 46)]),
    "Linear-Algebra": ("la", "Linear-Algebra_Lecture-%s.pdf", [("L1", 0), ("L2", 0), ("L3", 0), ("L4", 0), ("L5", 0), ("L6", 0), ("L7", 0)]),
}

LANG_HEAD = ("<script>(function(){var d=document.documentElement;try{var l=JSON.parse(localStorage.getItem('ustm:lang')||'null');"
             "d.setAttribute('data-lang',(l==='en'||l==='vi')?l:'both')}catch(e){d.setAttribute('data-lang','both')}})();</script>")

HOWTO = ("Open a lecture, share your screen and walk down the page: every card is one slide of the lecturers' own deck, with what to say (English and Vietnamese), "
         "why the slide matters and exercises with hidden solutions. The buttons at the bottom right switch between English, Vietnamese or both.",
         "Mở một bài giảng, chia sẻ màn hình rồi đi từ trên xuống: mỗi thẻ là một slide trong bộ slide gốc của các thầy cô, kèm lời giảng (tiếng Anh và tiếng Việt), "
         "giá trị của slide và bài tập có lời giải ẩn. Các nút ở góc dưới bên phải chuyển giữa tiếng Anh, tiếng Việt hoặc cả hai.")

def bi(en, vi, sep=True):
    """Inline bilingual label; the stylesheet shows one or both parts according to <html data-lang>."""
    return '<span class="l-en">%s</span>%s<span class="l-vi">%s</span>' % (en, '<span class="l-sep"> · </span>' if sep else "", vi)

def inline(text):
    """fmt() without the paragraph wrapper, for a short answer inside a line."""
    return re.sub(r"^<p>|</p>$", "", fmt(text))

def scripts(en, vi):
    return '<div class="sc en" lang="en"><span class="lab">EN</span>%s</div><div class="sc vi" lang="vi"><span class="lab">VI</span>%s</div>' % (fmt(en), fmt(vi))

def load(pkg, lid):
    """The lecture module if its file exists, else None (a lecture without a script yet is listed as 'in preparation')."""
    if not os.path.exists(os.path.join(ROOT, "build", "lectures", "%s_%s.py" % (pkg, lid))):
        return None
    return importlib.import_module("lectures.%s_%s" % (pkg, lid))

def any_lectures(course):
    if course not in CATALOGUE:
        return False
    pkg, _, cat = CATALOGUE[course]
    return any(load(pkg, lid) for lid, _ in cat)

def check_lecture(course, lid, mod, pages, pdf):
    """Coverage, images, original PDF and exercise checks. Returns the number of checked and unchecked exercises."""
    nums = [s["n"] for s in mod.SLIDES]
    assert nums == sorted(set(nums)), "%s %s: list every slide once, in order" % (course, lid)
    missing = sorted(set(range(1, pages + 1)) - set(nums)); extra = sorted(set(nums) - set(range(1, pages + 1)))
    assert not missing and not extra, "%s %s: missing slides %s, unknown slides %s" % (course, lid, missing, extra)
    assert mod.LECTURE["pages"] == pages, "%s %s: LECTURE pages differ from the catalogue" % (course, lid)
    for n in nums:
        assert os.path.exists(os.path.join(ROOT, course, "lectures", "img", lid, "%03d.webp" % n)), "%s %s: image %d missing" % (course, lid, n)
    assert os.path.exists(os.path.join(ROOT, course, "lectures", "pdf", pdf % lid[1:])), "%s %s: original PDF missing" % (course, lid)
    done = todo = 0
    for s in mod.SLIDES:
        assert s["v"] in LEVELS and s["en"] and s["vi"] and all(s["t"]), "%s %s slide %d: incomplete" % (course, lid, s["n"])
        for k, e in enumerate(s["ex"], 1):
            if run_check(e, "%s %s slide %d exercise %d" % (course, lid, s["n"], k)):
                done += 1
            else:
                todo += 1
    return done, todo

def slide_card(course, lid, s):
    n = s["n"]; img = "img/%s/%03d.webp" % (lid, n)
    with Image.open(os.path.join(ROOT, course, "lectures", img)) as im:
        w, h = im.size
    en, vi = s["t"]
    out = ['<section class="lslide" id="s%d"><div class="lhead"><span class="num">Slide %d</span><h3>%s</h3><span class="lvl v%d">%s %s</span></div>' % (n, n, bi(esc(en), esc(vi)), s["v"], "★" * s["v"], bi(*LEVELS[s["v"]]))]
    out.append('<div class="lgrid"><a class="lpic" href="%s" target="_blank" rel="noopener"><img loading="lazy" decoding="async" width="%d" height="%d" src="%s" alt="%s"></a><div class="ltext">%s' % (img, w, h, img, esc("Slide %d of %s: %s" % (n, lid, en)), scripts(s["en"], s["vi"])))
    if s["why"]:
        out.append('<div class="why"><b>%s:</b>%s</div>' % (bi("Why it matters", "Giá trị"), scripts(*s["why"])))
    out.append("</div></div>")
    for k, e in enumerate(s["ex"], 1):
        ans = inline(e["a"])
        mark = '<span class="tag okt">%s</span>' % bi("✓ checked by computer algebra", "✓ đã kiểm tra bằng máy") if e["chk"] is not None else ""
        out.append('<div class="ex"><div class="exh">%s %d.%d %s</div>%s<details class="sol"><summary>%s</summary><p><b>%s:</b> %s</p>%s</details></div>' % (
            bi("Exercise", "Bài tập"), n, k, mark, scripts(e["q"], e["qv"]), bi("Answer and solution", "Đáp án và lời giải"), bi("Answer", "Đáp án"), ans, scripts(e["s"], e["sv"])))
    out.append("</section>")
    return "".join(out)

def lecture_page(course, lid, mod, pdf, prev, nxt, have):
    L = mod.LECTURE; en, vi = L["title"]
    toc = "".join('<a class="v%d" href="#s%d"><b>%d</b> %s</a>' % (s["v"], s["n"], s["n"], bi(esc(s["t"][0]), esc(s["t"][1]))) for s in mod.SLIDES)
    nex = sum(len(s["ex"]) for s in mod.SLIDES)
    links = ('<a class="btn alt" href="%s.html">◀ %s</a>' % (prev, prev) if prev else "") + ('<a class="btn alt" href="%s.html">%s ▶</a>' % (nxt, nxt) if nxt else "")
    fab = ('<div class="langfab" role="group" aria-label="Language"><button type="button" data-lang-set="en">EN</button><button type="button" data-lang-set="both">EN + VI</button>'
           '<button type="button" data-lang-set="vi">VI</button><button type="button" id="solall" title="Open / close all solutions · Mở / đóng mọi lời giải">%s</button></div>' % bi("Solutions", "Lời giải"))
    body = ('<p class="muted"><a href="index.html">%s</a> › %s</p><h1>%s</h1>%s'
            '<div class="callout"><b>%s:</b> <a href="pdf/%s">%s</a> · %d slides · %s<br><b>%s:</b> %s</div>'
            '<div class="legend"><span class="lvl v3">★★★ %s</span> <span class="lvl v2">★★ %s</span> <span class="lvl v1">★ %s</span> <span class="muted">· %d %s</span></div>'
            '<details class="toc" open><summary>%s (%d)</summary><div class="tocgrid">%s</div></details>%s<div class="row">%s</div>%s') % (
        bi("Lectures", "Bài giảng"), lid, bi(esc(en), esc(vi), False), scripts(*L["intro"]),
        bi("Original slides", "Slide gốc"), pdf % lid[1:], bi("PDF of the lecturers' deck", "file PDF của các thầy cô"), L["pages"], L["chapter"], bi("Textbook", "Giáo trình"), esc(L["books"]),
        bi("Core", "Cốt lõi"), bi("Important", "Quan trọng"), bi("Context", "Bổ trợ"), nex, "exercises attached",
        bi("Slide list", "Danh sách slide"), L["pages"], toc, "".join(slide_card(course, lid, s) for s in mod.SLIDES), links, fab)
    write("%s/lectures/%s.html" % (course, lid), page(course, "%s · %s" % (lid, en), body, 1, "lectures", scripts=["lectures.js"], css=["lectures.css"], desc="%s: %s" % (lid, en), extra_head=LANG_HEAD, have=have))

def build(course, have):
    """Write the lecture pages of a course; returns (lectures built, exercises checked, exercises without a check)."""
    pkg, pdf, cat = CATALOGUE[course]
    mods = [(lid, pages, load(pkg, lid)) for lid, pages in cat]
    ids = [lid for lid, _, mod in mods if mod]
    if not ids:
        return 0, 0, 0
    done = todo = 0; cards = ""
    for lid, pages, mod in mods:
        if not mod:
            cards += '<div class="card" style="opacity:.6"><b>%s</b><span>%s</span></div>' % (lid, bi("Script in preparation", "Đang soạn lời giảng"))
            continue
        d, t = check_lecture(course, lid, mod, pages, pdf); done += d; todo += t
        i = ids.index(lid)
        lecture_page(course, lid, mod, pdf, ids[i - 1] if i else None, ids[i + 1] if i + 1 < len(ids) else None, have)
        en, vi = mod.LECTURE["title"]
        cards += '<a class="card" href="%s.html"><b>%s · %s</b><span>%s · %d slides · %d exercises</span></a>' % (lid, lid, bi(esc(en), esc(vi), False), esc(mod.LECTURE["chapter"]), pages, sum(len(s["ex"]) for s in mod.SLIDES))
    body = '<h1>%s</h1>%s<div class="cards">%s</div>' % (bi("Lecture walkthrough", "Giảng bài theo slide gốc"), scripts(*HOWTO), cards)
    write("%s/lectures/index.html" % course, page(course, "Lectures", body, 1, "lectures", scripts=["lectures.js"], css=["lectures.css"], extra_head=LANG_HEAD, have=have))
    return len(ids), done, todo
