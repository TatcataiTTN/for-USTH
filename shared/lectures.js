/* Lecture walkthrough pages: language switch (EN / EN + VI / VI), open or close every solution, solutions open when printing. */
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

document.addEventListener('DOMContentLoaded', function(){
  mark(root.getAttribute('data-lang') || 'both');
  [].forEach.call(document.querySelectorAll('[data-lang-set]'), function(b){
    b.addEventListener('click', function(){ setLang(b.getAttribute('data-lang-set')); });
  });
  var all = document.getElementById('solall');
  if(all) all.addEventListener('click', function(){ openAll(sols().some(function(d){ return !d.open; })); });
});
window.addEventListener('beforeprint', function(){ openAll(true); });
})();
