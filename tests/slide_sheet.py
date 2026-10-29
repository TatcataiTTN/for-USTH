"""Contact sheet of slides: python3 tests/slide_sheet.py out.png course/module:1,3,5 course/module:2,4 ... (1-based slide numbers).
Each slide is captured at the full 1280x720 canvas by forcing a 1400px window and scaling to 640x360 for the sheet."""
import sys, time, io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageDraw
BASE = "http://127.0.0.1:8765/"
o = Options()
for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=1500,1200"): o.add_argument(a)
d = webdriver.Chrome(options=o)
shots = []
for spec in sys.argv[2:]:
    path, nums = spec.split(":")
    d.get(BASE + path.split("/")[0] + "/modules/" + path.split("/")[1] + ".html"); time.sleep(2.2)
    d.execute_script("document.querySelector('.mdeck').style.maxWidth='1300px'; window.dispatchEvent(new Event('resize'));"); time.sleep(0.4)
    for n in nums.split(","):
        d.execute_script("var s=[].slice.call(document.querySelectorAll('.mdeck-slide'));s.forEach(function(t,i){t.classList.toggle('active',i==arguments[0])})", int(n) - 1) if False else None
        d.execute_script("location.hash='#%d'; window.dispatchEvent(new Event('hashchange'));" % int(n))
        d.execute_script("var s=[].slice.call(document.querySelectorAll('.mdeck-slide'));s.forEach(function(t,i){t.classList.toggle('active',i===%d)});document.querySelector('.mdeck-count').textContent='%d / '+s.length;" % (int(n) - 1, int(n)))
        time.sleep(0.25)
        el = d.find_element(By.CSS_SELECTOR, ".mdeck-canvas-wrap")
        im = Image.open(io.BytesIO(el.screenshot_as_png)).convert("RGB").resize((640, 360), Image.LANCZOS)
        ImageDraw.Draw(im).text((8, 346), "%s #%s" % (path, n), fill=(120, 120, 120))
        shots.append(im)
d.quit()
cols = 2; rows = (len(shots) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 644, rows * 364), (255, 255, 255))
for i, im in enumerate(shots):
    sheet.paste(im, ((i % cols) * 644, (i // cols) * 364))
sheet.save(sys.argv[1]); print("saved", sys.argv[1], sheet.size)
