# -*- coding: utf-8 -*-
"""Slide-deck HTML builder in the USTH-DSES style (1280x720 canvas, scaled by shared/deck.js)."""
import html, re

esc = lambda s: html.escape(str(s), quote=False)
CHIP = '<div class="logo-chip"><img src="{r}shared/img/usth_logo.png" alt="USTH"><img src="{r}shared/img/usth_dses_logo.png" alt="DSES"></div>'

def safe_math(h):
    """A raw '<' or '>' inside $...$ (e.g. $j<k$, $|x-a|<R$) would be parsed as HTML: escape them inside every math segment."""
    return re.sub(r"(\$\$.*?\$\$|\$.*?\$)", lambda m: m.group(0).replace("<", "&lt;").replace(">", "&gt;"), h, flags=re.S)

# ---- content blocks (strings of HTML; math is written with $...$ and rendered by KaTeX)
def ul(items, ordered=False):
    t = "ol" if ordered else "ul"
    return "<%s>%s</%s>" % (t, "".join("<li>%s</li>" % i for i in items), t)

def formula(tex):
    return '<div class="formula">$$%s$$</div>' % tex

def callout(label, body, kind=""):
    return '<div class="callout %s"><div class="lbl">%s</div>%s</div>' % (kind, label, body)

def table(head, rows):
    return "<table><tr>%s</tr>%s</table>" % ("".join("<th>%s</th>" % h for h in head), "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows))

def cols(*parts):
    return '<div class="cols">%s</div>' % "".join("<div>%s</div>" % p for p in parts)

def cards(*cs):
    return '<div class="cards">%s</div>' % "".join('<div class="card"><b>%s</b><span>%s</span></div>' % c for c in cs)

def p(text):
    return "<p>%s</p>" % text

def small(text):
    return '<p class="small">%s</p>' % text

class Deck:
    def __init__(self, title, subtitle, meta, r):
        self.r = r; self.slides = []
        chip = CHIP.format(r=r)
        self.slides.append(safe_math('<div class="mdeck-slide cover">%s<h2>%s</h2><div class="cover-sub">%s</div><div class="cover-meta">%s</div></div>' % (chip, title, subtitle, meta)))

    def add(self, title, body):
        self.slides.append(safe_math('<div class="mdeck-slide">%s<h2><span>%s</span></h2>%s</div>' % (CHIP.format(r=self.r), title, body)))

    def divider(self, title, body=""):
        self.slides.append(safe_math('<div class="mdeck-slide divider"><h2>%s</h2>%s</div>' % (title, body)))

    def end(self, title, body):
        self.slides.append(safe_math('<div class="mdeck-slide endcard">%s<h2>%s</h2>%s</div>' % (CHIP.format(r=self.r), title, body)))

    def html(self):
        return ('<div class="mdeck"><div class="mdeck-canvas-wrap"><div class="mdeck-viewport">%s</div></div>'
                '<div class="mdeck-bar"><button class="mdeck-prev" type="button">◀ Previous</button><button class="mdeck-next" type="button">Next ▶</button><span class="mdeck-count"></span>'
                '<div class="mdeck-dots"></div><button class="mdeck-fs" type="button">⛶ Full screen</button></div></div>') % "".join(self.slides)
