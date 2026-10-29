"""Save screenshots of key pages: python3 tests/shot.py <path> <out.png> [width] [height] [click-start]"""
import sys, time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import auth
BASE="http://127.0.0.1:8765/"
o=Options()
for a in ("--headless=new","--no-sandbox","--disable-gpu"): o.add_argument(a)
w=int(sys.argv[3]) if len(sys.argv)>3 else 1280; h=int(sys.argv[4]) if len(sys.argv)>4 else 900
o.add_argument("--window-size=%d,%d"%(w,h))
d=webdriver.Chrome(options=o); auth.prime(d, BASE); d.get(BASE+sys.argv[1]); time.sleep(1.5)
if len(sys.argv)>5:
    for b in d.find_elements(By.CSS_SELECTOR,"button.btn"):
        if "Start" in b.text: d.execute_script("arguments[0].click()",b); time.sleep(0.8); break
d.save_screenshot(sys.argv[2]); d.quit(); print("saved",sys.argv[2])
