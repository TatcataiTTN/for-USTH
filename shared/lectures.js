/* Lecture walkthrough pages: language switch (EN / EN + VI / VI), open or close every solution, solutions open when printing,
   and a slide viewer (lightbox): click a slide picture -> full-screen viewer with the previous / next slide (buttons, arrow keys, swipe). */
(function(){
'use strict';
var root = document.documentElement;

function mark(lang){
  [].forEach.call(document.querySelectorAll('[data-lang-set]'), function(b){ b.classList.toggle('on', b.getAttribute('data-lang-set') === lang); });
}
function setLang(lang){
  root.setAttribute('data-lang', lang);
  try{ localStorage.setItem('ustm:lang', JSON.stringify(lang)); }catch(e){}
  mark(lang);
}
function sols(){ return [].slice.call(document.querySelectorAll('details.sol')); }
function openAll(open){ sols().forEach(function(d){ if(open) d.setAttribute('open', ''); else d.removeAttribute('open'); }); }


/* ---- slide viewer ---- */
function initViewer(){
  var pics = [].slice.call(document.querySelectorAll('a.lpic')), N = pics.length;
  if(!N) return;
  var box = null, img, cap, cnt, prev, next, fs, open = null, cur = 0, start = 0, lastFocus = null, tx = null, ty = null;
  function el(tag, cls, label, text){ var e = document.createElement(tag); e.className = cls; if(label){ e.setAttribute('aria-label', label); e.title = label; } if(text) e.textContent = text; if(tag === 'button') e.type = 'button'; return e; }
  function build(){
    box = el('div', 'lbx'); box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Slide viewer'); box.hidden = true; box.tabIndex = -1;
    var top = el('div', 'lbx-top'); cap = el('span', 'lbx-cap'); cnt = el('span', 'lbx-cnt'); cnt.setAttribute('aria-live', 'polite');
    fs = el('button', 'lbx-btn lbx-fs', 'Full screen (F)', '⛶');
    open = el('a', 'lbx-btn lbx-new', 'Open the picture in a new tab', '↗'); open.target = '_blank'; open.rel = 'noopener';
    var x = el('button', 'lbx-btn lbx-x', 'Close (Esc)', '✕');
    top.appendChild(cap); top.appendChild(cnt); if(box.requestFullscreen || box.webkitRequestFullscreen) top.appendChild(fs); top.appendChild(open); top.appendChild(x);
    var stage = el('div', 'lbx-stage'); img = el('img', 'lbx-img'); img.alt = '';
    prev = el('button', 'lbx-nav lbx-prev', 'Previous slide (←)', '‹'); next = el('button', 'lbx-nav lbx-next', 'Next slide (→)', '›');
    stage.appendChild(prev); stage.appendChild(img); stage.appendChild(next);
    box.appendChild(top); box.appendChild(stage); document.body.appendChild(box);
    prev.addEventListener('click', function(){ go(cur - 1); }); next.addEventListener('click', function(){ go(cur + 1); }); img.addEventListener('click', function(){ go(cur + 1); });
    x.addEventListener('click', close); fs.addEventListener('click', toggleFs);
    stage.addEventListener('click', function(e){ if(e.target === stage) close(); });
    stage.addEventListener('touchstart', function(e){ var t = e.changedTouches[0]; tx = t.clientX; ty = t.clientY; }, {passive: true});
    stage.addEventListener('touchend', function(e){ if(tx === null) return; var t = e.changedTouches[0], dx = t.clientX - tx, dy = t.clientY - ty; tx = null; if(Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(dy)) go(cur + (dx < 0 ? 1 : -1)); }, {passive: true});
  }
  function load(i){ if(i >= 0 && i < N){ var im = new Image(); im.src = pics[i].getAttribute('href'); } }
  function go(i){
    if(i < 0 || i >= N) return;
    cur = i; var a = pics[i], pic = a.querySelector('img');
    img.src = a.getAttribute('href'); img.alt = pic ? pic.alt : ''; cap.textContent = pic ? pic.alt : ''; cnt.textContent = (i + 1) + ' / ' + N; open.href = a.getAttribute('href');
    prev.disabled = i === 0; next.disabled = i === N - 1; load(i + 1); load(i - 1);
  }
  function show(i){
    if(!box) build();
    lastFocus = document.activeElement; start = i; document.body.style.overflow = 'hidden'; box.hidden = false; go(i); box.focus();
  }
  function close(){
    if(!box || box.hidden) return;
    if(document.fullscreenElement && document.exitFullscreen){ try{ document.exitFullscreen(); }catch(e){} }
    box.hidden = true; document.body.style.overflow = '';
    if(cur !== start) pics[cur].scrollIntoView({block: 'center'});             // land on the slide you stopped at
    if(lastFocus && lastFocus.focus){ try{ lastFocus.focus({preventScroll: true}); }catch(e){} }
  }
  function toggleFs(){
    try{
      if(document.fullscreenElement || document.webkitFullscreenElement){ (document.exitFullscreen || document.webkitExitFullscreen).call(document); }
      else (box.requestFullscreen || box.webkitRequestFullscreen).call(box);
    }catch(e){}
  }
  pics.forEach(function(a, i){
    a.title = 'Click to view the slides full screen (← → to move)';
    a.addEventListener('click', function(e){ if(e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); show(i); });
  });
  document.addEventListener('keydown', function(e){
    if(!box || box.hidden || e.metaKey || e.ctrlKey || e.altKey) return;
    var k = e.key, used = true;
    if(k === 'ArrowRight' || k === 'PageDown' || (k === ' ' && !/^(BUTTON|A)$/.test(document.activeElement.tagName))) go(cur + 1);
    else if(k === 'ArrowLeft' || k === 'PageUp') go(cur - 1);
    else if(k === 'Home') go(0);
    else if(k === 'End') go(N - 1);
    else if(k === 'Escape') close();
    else if((k === 'f' || k === 'F') && (box.requestFullscreen || box.webkitRequestFullscreen)) toggleFs();
    else if(k === 'Tab'){                                                     // keep the focus inside the viewer
      var f = [].filter.call(box.querySelectorAll('button,a[href]'), function(b){ return !b.disabled; }), first = f[0], last = f[f.length - 1];
      if(e.shiftKey && (document.activeElement === first || document.activeElement === box)){ last.focus(); } else if(!e.shiftKey && document.activeElement === last){ first.focus(); } else used = document.activeElement !== box ? false : (first.focus(), true);
    } else used = false;
    if(used) e.preventDefault();
  });
}

document.addEventListener('DOMContentLoaded', function(){
  initViewer();
  mark(root.getAttribute('data-lang') || 'both');
  [].forEach.call(document.querySelectorAll('[data-lang-set]'), function(b){
    b.addEventListener('click', function(){ setLang(b.getAttribute('data-lang-set')); });
  });
  var all = document.getElementById('solall');
  if(all) all.addEventListener('click', function(){ openAll(sols().some(function(d){ return !d.open; })); });
});
window.addEventListener('beforeprint', function(){ openAll(true); });
})();
