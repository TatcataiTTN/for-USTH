/* Sign-in screen: shown the first time a page is opened in a browser, then remembered on that browser.
   This is a convenience gate, not real protection: the sites are static, so the check runs in the browser and the pages and data files
   stay reachable by their URLs. Only a salted PBKDF2 hash of "username + newline + password" is kept here, never the password itself.
   Change the credentials with:  python3 build/set_password.py */
(function(){
'use strict';
var CFG = {salt: '4a1d0b06219ac1554a386d330f4e3b82', iter: 200000, hash: '79999bcc2a68783cdf54341a212aca0b9ba21f902356fe26ac0a4620251b7b82'}; // GATE-CONFIG (rewritten by build/set_password.py)
var KEY = 'ustm:auth';
if(!CFG.hash) return;                       // not configured: no gate

var me = document.currentScript;            // only valid while this script runs, so read it now
var BASE = me && me.src ? me.src.replace(/gate\.js(\?.*)?$/, '') : 'shared/';
var root = document.documentElement;

/* storage that survives blocked localStorage (private windows): localStorage, then sessionStorage, then memory */
function usable(kind){ try{ var s = window[kind], t = '__ustm_probe'; s.setItem(t, '1'); s.removeItem(t); return s; }catch(e){ return null; } }
var area = usable('localStorage') || usable('sessionStorage'), memory = null;
function getToken(){ try{ return area ? area.getItem(KEY) : memory; }catch(e){ return memory; } }
function setToken(v){ memory = v; try{ if(area) area.setItem(KEY, v); }catch(e){} }
function clearToken(){ memory = null; try{ if(area) area.removeItem(KEY); }catch(e){} }

/* "Sign out" buttons (in the Display menu) work whether or not the page is locked */
document.addEventListener('click', function(e){
  if(e.target.closest && e.target.closest('[data-logout]')){ clearToken(); location.reload(); }
});

if(getToken() === CFG.hash) return;         // already signed in on this browser

function toHex(buf){ return Array.prototype.map.call(new Uint8Array(buf), function(b){ return ('0' + b.toString(16)).slice(-2); }).join(''); }
function fromHex(h){ var a = new Uint8Array(h.length / 2); for(var i = 0; i < a.length; i++) a[i] = parseInt(h.substr(2 * i, 2), 16); return a; }
/* must match derive() in build/set_password.py: PBKDF2-SHA256, 256 bits, over lower(trim(username)) + "\n" + password */
function derive(user, pass){
  var enc = new TextEncoder();
  return crypto.subtle.importKey('raw', enc.encode(user.trim().toLowerCase() + '\n' + pass), 'PBKDF2', false, ['deriveBits'])
    .then(function(k){ return crypto.subtle.deriveBits({name: 'PBKDF2', salt: fromHex(CFG.salt), iterations: CFG.iter, hash: 'SHA-256'}, k, 256); })
    .then(toHex);
}

/* lock the page right away (this script runs in <head>, before the body is painted) */
root.classList.add('ustm-locked');
var st = document.createElement('style');
st.textContent =
  'html.ustm-locked body>*:not(#ustm-gate){display:none!important}html.ustm-locked{overflow:hidden}' +
  '#ustm-gate{position:fixed;top:0;right:0;bottom:0;left:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px;overflow:auto;background:var(--bg,#f4f6fb);color:var(--fg,#1b2433)}' +
  '#ustm-gate form{width:100%;max-width:380px;box-sizing:border-box;background:var(--card,#fff);border:1px solid var(--border,#d5dae6);border-radius:14px;padding:22px 20px;box-shadow:0 12px 40px rgba(0,0,0,.18)}' +
  '#ustm-gate .g-chip{display:inline-flex;align-items:center;gap:10px;background:#fff;border:1px solid #d5dae6;border-radius:10px;padding:4px 12px}' +
  '#ustm-gate .g-chip img{height:34px;width:auto;display:block}' +
  '#ustm-gate h1{margin:12px 0 4px;font-size:1.45rem;line-height:1.2;color:inherit}' +
  '#ustm-gate p{margin:4px 0 8px;font-size:.95rem;color:var(--muted,#566074)}' +
  '#ustm-gate label{display:block;margin-top:12px;font-size:.92rem}' +
  '#ustm-gate input[type=text],#ustm-gate input[type=password]{display:block;width:100%;box-sizing:border-box;margin-top:4px;padding:10px 12px;font:inherit;font-size:16px;border:1px solid var(--border,#c9cfdd);border-radius:8px;background:var(--bg,#fff);color:var(--fg,#1b2433)}' +
  '#ustm-gate label.g-show{display:flex;align-items:center;gap:6px;margin-top:10px;color:var(--muted,#566074)}' +
  '#ustm-gate #ustm-err{min-height:1.3em;margin:10px 0 0;font-weight:600;color:var(--bad,#b3261e)}' +
  '#ustm-gate button{width:100%;margin-top:10px;padding:11px;font:inherit;font-weight:600;border:0;border-radius:8px;background:var(--navy,#273896);color:#fff;cursor:pointer}' +
  '#ustm-gate button[disabled]{opacity:.65;cursor:wait}';
(document.head || root).appendChild(st);

function build(){
  var g = document.createElement('div');
  g.id = 'ustm-gate'; g.setAttribute('role', 'dialog'); g.setAttribute('aria-modal', 'true'); g.setAttribute('aria-labelledby', 'ustm-gate-title');
  g.innerHTML =
    '<form id="ustm-gate-form" novalidate>' +
      '<span class="g-chip"><img src="' + BASE + 'img/usth_logo.png" alt="USTH"><img src="' + BASE + 'img/usth_dses_logo.png" alt="DSES"></span>' +
      '<h1 id="ustm-gate-title">Sign in</h1>' +
      '<p>USTH B1 · Maths and Physics self-study. Sign in once to open the sites on this browser.</p>' +
      '<label>Username<input id="ustm-user" name="username" type="text" autocomplete="username" autocapitalize="none" autocorrect="off" spellcheck="false"></label>' +
      '<label>Password<input id="ustm-pass" name="password" type="password" autocomplete="current-password"></label>' +
      '<label class="g-show"><input id="ustm-show" type="checkbox"> Show password</label>' +
      '<p id="ustm-err" role="alert" aria-live="assertive"></p>' +
      '<button id="ustm-go" type="submit">Sign in</button>' +
    '</form>';
  document.body.appendChild(g);
  var form = g.querySelector('form'), user = g.querySelector('#ustm-user'), pass = g.querySelector('#ustm-pass'),
      err = g.querySelector('#ustm-err'), go = g.querySelector('#ustm-go');
  g.querySelector('#ustm-show').onchange = function(){ pass.type = this.checked ? 'text' : 'password'; };
  function reset(){ go.disabled = false; go.textContent = 'Sign in'; }
  form.onsubmit = function(ev){
    ev.preventDefault(); err.textContent = '';
    if(!user.value.trim() || !pass.value){ err.textContent = 'Enter your username and password.'; (user.value.trim() ? pass : user).focus(); return; }
    if(!(window.crypto && crypto.subtle)){ err.textContent = 'This browser cannot check the password on this page (it needs a secure https connection).'; return; }
    go.disabled = true; go.textContent = 'Checking…';
    derive(user.value, pass.value).then(function(h){
      if(h === CFG.hash){
        setToken(h); root.classList.remove('ustm-locked'); g.parentNode.removeChild(g);
        document.dispatchEvent(new CustomEvent('ustm:signin'));
        return;
      }
      err.textContent = 'Wrong username or password.'; pass.value = ''; pass.focus();
      setTimeout(reset, 700);                 // a short pause after a wrong attempt
    }, function(){ err.textContent = 'Could not check the password in this browser.'; reset(); });
  };
  user.focus();
}
if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
