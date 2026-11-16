"""preview-assets.py - renders SVGs to PNG with headless Chromium (needs: pip install playwright).
Animated SVGs are frozen at a given time (fraction of the loop, default 0.93 = fully painted).
Usage: python3 tools/preview-assets.py out_dir file.svg[@fraction] ...
"""
import os, re, sys
from playwright.sync_api import sync_playwright

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for arg in sys.argv[2:]:
        path, _, frac = arg.partition('@')
        frac = float(frac or 0.93)
        svg = open(path, encoding='utf-8').read()
        w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
        dur = re.search(r'keyTimes="0;0.95;0.99;1" dur="([\d.]+)s"', svg) or re.search(r'dur="([\d.]+)s"', svg)
        T = float(dur.group(1)) if dur else 1
        pg = b.new_page(viewport={'width': int(w), 'height': int(h)})
        pg.goto('file://' + os.path.abspath(path))
        pg.evaluate(f'()=>{{const s=document.documentElement;s.pauseAnimations();s.setCurrentTime({frac * T});}}')
        pg.wait_for_timeout(150)
        name = os.path.splitext(os.path.basename(path))[0] + (f'_{int(frac * 100)}' if '@' in arg else '') + '.png'
        pg.screenshot(path=os.path.join(out, name))
        print('shot', name)
    b.close()
