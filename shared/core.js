/* USTM core: tiny helpers shared by every page (no dependencies besides KaTeX). */
(function(){
'use strict';
var U = window.USTM = {};

U.el = function(tag, cls, txt){ var e = document.createElement(tag); if(cls) e.className = cls; if(txt !== undefined) e.textContent = txt; return e; };
U.$ = function(sel, root){ return (root || document).querySelector(sel); };
U.$$ = function(sel, root){ return [].slice.call((root || document).querySelectorAll(sel)); };

U.json = function(url){
  return fetch(url).then(function(r){ if(!r.ok) throw new Error('HTTP ' + r.status + ' for ' + url); return r.json(); });
};

U.math = function(root){
  if(window.renderMathInElement){
    try{
      window.renderMathInElement(root || document.body, {
        delimiters: [{left:'$$', right:'$$', display:true}, {left:'$', right:'$', display:false}],
        throwOnError: false, errorColor: '#b00020'
      });
      U.glue(root || document.body);
    }catch(e){ console.error('KaTeX render error', e); }
  }
};
/* A line must not start with the comma/period that follows a formula, nor end with the bracket that precedes one:
   keep them together in a no-wrap <span class="nw"> (a word joiner is ignored by browsers next to inline-blocks). */
U.glue = function(root){
  [].forEach.call(root.querySelectorAll('.katex:not([data-glued])'), function(k){
    k.setAttribute('data-glued', '1');
    var par = k.parentNode;
    if(!par || par.className === 'katex-display') return;                      /* display math sits on its own line */
    var el = (!par.className && par.childNodes.length === 1) ? par : k;        /* auto-render wraps inline math in a plain <span> */
    var n = el.nextSibling, p = el.previousSibling, after = '', before = '';
    if(n && n.nodeType === 3){ var m = /^[,.;:!?)\]]+/.exec(n.nodeValue); if(m){ after = m[0]; n.nodeValue = n.nodeValue.slice(after.length); } }
    if(p && p.nodeType === 3){ var q = /[(\[]+$/.exec(p.nodeValue); if(q){ before = q[0]; p.nodeValue = p.nodeValue.slice(0, p.nodeValue.length - before.length); } }
    if(!after && !before) return;
    var w = document.createElement('span'); w.className = 'nw';
    el.parentNode.insertBefore(w, el);
    if(before) w.appendChild(document.createTextNode(before));
    w.appendChild(el);
    if(after) w.appendChild(document.createTextNode(after));
  });
};

/* localStorage that never throws (private windows, blocked storage) */
U.store = {
  get: function(k, d){ try{ var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); }catch(e){ return d; } },
  set: function(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); return true; }catch(e){ return false; } },
  del: function(k){ try{ localStorage.removeItem(k); }catch(e){} }
};

U.mulberry32 = function(a){
  return function(){ a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
};
U.shuffle = function(arr, rnd){
  rnd = rnd || Math.random; var a = arr.slice();
  for(var i = a.length - 1; i > 0; i--){ var j = Math.floor(rnd() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
  return a;
};
U.srcLabel = function(q){
  if(q.origin === 'src') return '📎 Source: ' + q.src;
  if(q.origin === 'gen') return '➕ ' + (/^(Generated|Extension)/.test(q.src) ? q.src : 'Generated, same style as: ' + q.src);
  return '💡 Concept check · ' + q.src;
};
U.fmtTime = function(s){ s = Math.max(0, Math.round(s)); var m = Math.floor(s / 60), r = s % 60; return m + ':' + (r < 10 ? '0' : '') + r; };
U.pct = function(a, b){ return b ? Math.round(100 * a / b) : 0; };
U.key = function(course, what){ return 'ustm:' + course + ':' + what; };

/* ---- theme + font size menu ------------------------------------------------------------ */
U.initTheme = function(){
  var t = U.store.get('ustm:theme', 'auto');
  var f = U.store.get('ustm:font', '');
  if(t === 'dark' || t === 'light') document.documentElement.setAttribute('data-theme', t);
  if(f) document.documentElement.style.fontSize = f;
  U.$$('[data-set-theme]').forEach(function(b){
    b.onclick = function(){
      var v = b.getAttribute('data-set-theme');
      if(v === 'auto') document.documentElement.removeAttribute('data-theme'); else document.documentElement.setAttribute('data-theme', v);
      U.store.set('ustm:theme', v);
    };
  });
  U.$$('[data-set-font]').forEach(function(b){
    b.onclick = function(){ var v = b.getAttribute('data-set-font'); document.documentElement.style.fontSize = v; U.store.set('ustm:font', v); };
  });
  /* the popup is anchored to the right edge of its button; on a phone the button sits at the left, so shift the popup back into the viewport */
  var det = document.querySelector('details.menu');
  if(det) det.addEventListener('toggle', function(){
    var pop = det.querySelector('.pop'); if(!pop) return;
    pop.style.left = ''; pop.style.right = '';
    if(!det.open) return;
    var r = pop.getBoundingClientRect(), vw = document.documentElement.clientWidth;
    if(r.left < 8){ pop.style.right = 'auto'; pop.style.left = '0'; r = pop.getBoundingClientRect(); if(r.right > vw - 8) pop.style.left = (vw - 8 - r.right) + 'px'; }
  });
};

/* ---- progress records (history + per-question statistics) ------------------------------- */
U.record = function(course, entry){
  var hk = U.key(course, 'history');
  var h = U.store.get(hk, []);
  h.unshift(entry);
  U.store.set(hk, h.slice(0, 200));
};
U.qstat = function(course, id, correct){
  var k = U.key(course, 'qstats');
  var s = U.store.get(k, {});
  var r = s[id] || [0, 0];
  r[0] += 1; if(correct) r[1] += 1;
  s[id] = r;
  U.store.set(k, s);
};

document.addEventListener('DOMContentLoaded', function(){ U.initTheme(); U.math(document.body); });
})();
