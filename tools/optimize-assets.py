"""optimize-assets.py - shrinks every asset in place and prints a size report.
  * SVG : strips comments / indentation / whitespace between tags (artwork is untouched)
  * GIF : re-saves with Pillow's optimizer; uses gifsicle too when it is installed
  * Warns when a file is bigger than the budget (SVG 120 KB, GIF 2 MB, PNG 500 KB)
Run:  python3 tools/optimize-assets.py
"""
import os, re, shutil, subprocess, sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BUDGET = {'.svg': 120 * 1024, '.gif': 2 * 1024 * 1024, '.png': 500 * 1024}


def min_svg(path):
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'>\s+<', '><', s).strip() + '\n'
    open(path, 'w', encoding='utf-8').write(s)


def opt_gif(path):
    if shutil.which('gifsicle'):
        subprocess.run(['gifsicle', '-O3', '--colors', '160', path, '-o', path], check=False)
        return
    im = Image.open(path)
    frames, durs = [], []
    for i in range(im.n_frames):
        im.seek(i)
        frames.append(im.convert('RGB').quantize(colors=160, dither=Image.Dither.NONE))
        durs.append(im.info.get('duration', 80))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=True, disposal=1)


total = 0
for base, _, files in os.walk(os.path.join(ROOT, 'assets')):
    for f in sorted(files):
        p = os.path.join(base, f)
        ext = os.path.splitext(f)[1].lower()
        before = os.path.getsize(p)
        if ext == '.svg':
            min_svg(p)
        elif ext == '.gif' and '--skip-gif' not in sys.argv:
            opt_gif(p)
        after = os.path.getsize(p)
        total += after
        flag = '  <-- over budget' if after > BUDGET.get(ext, 1e12) else ''
        print(f'{os.path.relpath(p, ROOT):58s} {before / 1024:7.1f} KB -> {after / 1024:7.1f} KB{flag}')
print(f'\ntotal assets: {total / 1024 / 1024:.2f} MB')
