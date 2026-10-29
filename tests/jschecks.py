"""JavaScript probes shared by the browser tests."""

# relative luminance / contrast helper executed in the page: walks visible text nodes and returns the worst offenders
CONTRAST_JS = """
function parse(c){var m=c.match(/rgba?\\(([^)]+)\\)/); if(!m) return null; var p=m[1].split(',').map(parseFloat); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1};}
function lum(c){function f(v){v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4);} return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b);}
function bgOf(el){var bg={r:255,g:255,b:255}; var chain=[]; for(var e=el;e;e=e.parentElement){chain.push(e);}
  for(var i=chain.length-1;i>=0;i--){var c=parse(getComputedStyle(chain[i]).backgroundColor); if(c&&c.a>0){ bg={r:c.r*c.a+bg.r*(1-c.a), g:c.g*c.a+bg.g*(1-c.a), b:c.b*c.a+bg.b*(1-c.a)}; } } return bg;}
var bad=[]; var seen=new Set();
var w=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
while(w.nextNode()){var n=w.currentNode; if(!n.nodeValue.trim()) continue; var el=n.parentElement; if(!el||seen.has(el)) continue; seen.add(el);
  var cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity)===0) continue;
  var r=el.getBoundingClientRect(); if(r.width===0||r.height===0) continue;
  if(el.closest('.katex-mathml, script, style, .hide, [hidden], .sr-only')) continue;
  var fg=parse(cs.color); if(!fg) continue; var bg=bgOf(el);
  var fgb={r:fg.r*fg.a+bg.r*(1-fg.a), g:fg.g*fg.a+bg.g*(1-fg.a), b:fg.b*fg.a+bg.b*(1-fg.a)};
  var L1=lum(fgb), L2=lum(bg), ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
  if(ratio<3){bad.push(ratio.toFixed(2)+' '+(el.className||el.tagName)+' "'+n.nodeValue.trim().slice(0,40)+'"');}
}
return bad.slice(0,6);
"""

# [data-theme attribute, luminance of the page background]: lets a test assert that the requested theme is really applied
THEME_JS = """
var a = document.documentElement.getAttribute('data-theme');
var c = getComputedStyle(document.body).backgroundColor.match(/[\\d.]+/g).map(parseFloat);
function f(v){ v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
return [a, 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])];
"""
