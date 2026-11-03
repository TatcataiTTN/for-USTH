"""Full-page screenshots of the concept finder / analyser: python3 tests/shot_concepts.py [BASE_URL]  (writes tests/screens/concepts/full-*.png)"""
import base64, os, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import auth
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8766/").rstrip("/") + "/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens", "concepts"); os.makedirs(OUT, exist_ok=True)
js = lambda d, s, *a: d.execute_script(s, *a)
def drv(w, h, mob, dark):
    o = Options()
    for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=%d,%d" % (w, h)): o.add_argument(a)
    d = webdriver.Chrome(options=o)
    if mob: d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": w, "height": h, "deviceScaleFactor": 1.5, "mobile": True})
    d.execute_cdp_cmd("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-color-scheme", "value": "dark" if dark else "light"}]})
    auth.prime(d, BASE); return d
def full(d, name):
    h = js(d, "return Math.max(document.documentElement.scrollHeight,document.body.scrollHeight)")
    w = js(d, "return window.innerWidth")
    r = d.execute_cdp_cmd("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True, "clip": {"x": 0, "y": 0, "width": w, "height": min(h, 6000), "scale": 1}})
    open(os.path.join(OUT, name), "wb").write(base64.b64decode(r["data"])); print("saved", name, w, h)
def example(d, i):
    js(d, "var s=document.getElementById('az-ex');s.value=arguments[0];s.dispatchEvent(new Event('change'))", str(i)); time.sleep(.8)
for mob, dark in ((False, False), (True, True)):
    t = ("phone" if mob else "desktop") + ("-dark" if dark else "-light")
    d = drv(390 if mob else 1280, 800 if mob else 900, mob, dark)
    try:
        d.get(BASE + "concepts/index.html"); time.sleep(2)
        example(d, 0); full(d, "full-analyse-%s.png" % t)
        example(d, 8); full(d, "full-out-%s.png" % t)
        js(d, "var q=document.getElementById('az-q');q.value='Zorblax quintuplet frobnication of the widget';document.getElementById('az-go').click()"); time.sleep(.6); full(d, "full-none-%s.png" % t)
        js(d, "document.querySelector('.cf-tabs [data-tab=br]').click()"); time.sleep(.5); full(d, "full-browse-%s.png" % t)
    finally: d.quit()
