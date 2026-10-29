// Slide engine: scales the 1280x720 canvas to the window, keyboard and button navigation, dots, fullscreen, #n deep links.
(function(){
 var deck=document.querySelector('.mdeck'),wrap=deck.querySelector('.mdeck-canvas-wrap'),vp=deck.querySelector('.mdeck-viewport');
 var sl=[].slice.call(vp.querySelectorAll('.mdeck-slide')),i=0,dots=deck.querySelector('.mdeck-dots'),cnt=deck.querySelector('.mdeck-count');
 sl.forEach(function(_,k){var b=document.createElement('button');b.title='Slide '+(k+1);b.onclick=function(){go(k)};dots.appendChild(b)});
 function fit(){var fs=document.fullscreenElement===deck;var w=fs?window.innerWidth:wrap.clientWidth;var h=fs?window.innerHeight-48:1e9;
  var s=Math.min(w/1280,h/720);vp.style.transform='scale('+s+')';wrap.style.height=(720*s)+'px';wrap.style.width=fs?(1280*s)+'px':'100%';wrap.style.margin=fs?'0 auto':'0';}
 function go(k){i=Math.max(0,Math.min(sl.length-1,k));sl.forEach(function(s,n){s.classList.toggle('active',n===i)});
  [].forEach.call(dots.children,function(d,n){d.classList.toggle('on',n===i)});cnt.textContent=(i+1)+' / '+sl.length;
  try{history.replaceState(null,'','#'+(i+1))}catch(e){}}
 deck.querySelector('.mdeck-prev').onclick=function(){go(i-1)};deck.querySelector('.mdeck-next').onclick=function(){go(i+1)};
 deck.querySelector('.mdeck-fs').onclick=function(){if(document.fullscreenElement){document.exitFullscreen()}else{deck.requestFullscreen&&deck.requestFullscreen()}};
 document.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){go(i+1);e.preventDefault()}else if(e.key==='ArrowLeft'||e.key==='PageUp'){go(i-1)}else if(e.key==='Home'){go(0)}else if(e.key==='End'){go(sl.length-1)}});
 window.addEventListener('resize',fit);document.addEventListener('fullscreenchange',fit);
 var h=parseInt((location.hash||'').slice(1),10);fit();go(isNaN(h)?0:h-1);
})();
