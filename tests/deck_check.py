"""Layout QA of the slide decks (1280x720 canvas): overflow, text < 20 px, KaTeX errors, how far down each slide is filled.
Usage: python3 tests/deck_check.py [BASE_URL] [--shots]"""
import sys, glob, os, time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (args[0] if args else "http://127.0.0.1:8765/").rstrip("/") + "/"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
o = Options()
for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=1320,900"): o.add_argument(a)
d = webdriver.Chrome(options=o)
JS = """
var slides=[].slice.call(document.querySelectorAll('.mdeck-slide')), out=[];
var wrap=document.querySelector('.mdeck-canvas-wrap');
slides.forEach(function(s,i){
  slides.forEach(function(t){t.classList.remove('active')}); s.classList.add('active');
  var sr=s.getBoundingClientRect(), sc=sr.width/1280, bottom=0, small=[], over=0;
  [].forEach.call(s.querySelectorAll('*'),function(e){
    if(e.closest('.logo-chip')||e.closest('.katex')&&!e.classList.contains('katex')) return;
    var r=e.getBoundingClientRect(); if(r.width===0||r.height===0) return;
    if(e.tagName==='H2'&&!s.classList.contains('cover')&&!s.classList.contains('endcard')) return;
    var b=(r.bottom-sr.top)/sc; if(b>bottom) bottom=b;
    if((r.right-sr.left)/sc>1282) over++;
    var hasText=[].some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim().length>0});
    if(hasText){var fs=parseFloat(getComputedStyle(e).fontSize)*(1); if(fs<19.5) small.push(Math.round(fs)+'px:'+e.textContent.trim().slice(0,30));}
  });
  var h2=s.querySelector('h2'); out.push({i:i,title:(h2?h2.textContent:'').slice(0,50),bottom:Math.round(bottom),small:small.slice(0,3),over:over,kerr:s.querySelectorAll('.katex-error').length,sh:s.scrollHeight});
});
return out;
"""
bad = 0; n = 0; sparse = []
for course in ("Calculus-1", "Linear-Algebra"):
    for f in sorted(glob.glob(os.path.join(ROOT, course, "modules", "m*.html"))):
        name = os.path.basename(f)
        d.get(BASE + course + "/modules/" + name); time.sleep(2.2)
        struct = d.execute_script("""var all=document.querySelectorAll('.mdeck-slide').length, top=document.querySelectorAll('.mdeck-viewport > .mdeck-slide').length;
var allowed={DIV:1,SPAN:1,P:1,UL:1,OL:1,LI:1,TABLE:1,TBODY:1,TR:1,TH:1,TD:1,B:1,I:1,STRONG:1,EM:1,BR:1,IMG:1,H2:1,A:1,SUP:1,SUB:1,CODE:1,SVG:1,PATH:1,SEMANTICS:1,ANNOTATION:1};
var bad=[];[].forEach.call(document.querySelectorAll('.mdeck-slide *'),function(e){if(e.closest('.katex')||e.closest('svg'))return;if(!allowed[e.tagName]) bad.push(e.tagName)});
return {all:all,top:top,bad:bad.slice(0,5)};""")
        n += 1
        if struct["all"] != struct["top"] or struct["bad"]:
            bad += 1; print("%s %s: broken slide structure (nested slides %d/%d, odd tags %s)" % (course, name, struct["top"], struct["all"], struct["bad"]))
        res = d.execute_script(JS)
        for r in res:
            n += 1
            probs = []
            if r["bottom"] > 716: probs.append("overflow bottom=%d" % r["bottom"])
            if r["over"]: probs.append("wider than the canvas")
            if r["small"]: probs.append("small text %s" % r["small"])
            if r["kerr"]: probs.append("KaTeX errors")
            if probs:
                bad += 1; print("%s %s slide %d '%s': %s" % (course, name, r["i"] + 1, r["title"], "; ".join(probs)))
            elif r["bottom"] < 440 and r["i"] not in (0,):
                sparse.append("%s %s slide %d '%s' bottom=%d" % (course, name, r["i"] + 1, r["title"], r["bottom"]))
d.quit()
print("%d slides checked, %d with problems, %d sparse (< 440 px filled)" % (n, bad, len(sparse)))
for s in sparse[:20]: print("  sparse:", s)
sys.exit(1 if bad else 0)
