"""Screenshot of the practice-bank cards that match a search text: python3 tests/shot_bank.py <course> "<search>" <out.png> [width] [height] [scroll-to-text]"""
import sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import auth
BASE = "http://127.0.0.1:8765/"
course, text, out = sys.argv[1], sys.argv[2], sys.argv[3]
w = int(sys.argv[4]) if len(sys.argv) > 4 else 1280; h = int(sys.argv[5]) if len(sys.argv) > 5 else 1000
o = Options()
for a in ("--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=%d,%d" % (w, h)): o.add_argument(a)
d = webdriver.Chrome(options=o)
auth.prime(d, BASE)
d.get(BASE + course + "/bank/index.html"); time.sleep(1.5)
box = [i for i in d.find_elements(By.CSS_SELECTOR, "input[type=text], input[type=search]") if i.is_displayed()][0]
box.send_keys(text); time.sleep(1.0)
if len(sys.argv) > 6:
    el = d.find_element(By.XPATH, "//*[contains(text(), %r)]" % sys.argv[6])
    d.execute_script("arguments[0].scrollIntoView({block:'start'})", el); time.sleep(0.4)
d.save_screenshot(out); print("saved", out, "| katex errors:", len(d.find_elements(By.CSS_SELECTOR, ".katex-error")))
d.quit()
