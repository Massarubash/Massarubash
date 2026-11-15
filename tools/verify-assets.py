"""verify-assets.py - checks README.md against the repo.
  * every local image / link in README.md exists (HTML <img src>, <a href>, markdown ![](...))
  * every SVG is well-formed XML, every GIF opens
  * reports assets that README.md never uses (commented-out placeholders count as "optional")
  * guards against forbidden identities (FLOWER, GennisCode, Guris da T.I)
Exit code 1 on any hard error.   Run:  python3 tools/verify-assets.py
"""
import os, re, sys
import xml.dom.minidom as minidom
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
readme = open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
live = re.sub(r'<!--.*?-->', '', readme, flags=re.S)
commented = ''.join(re.findall(r'<!--.*?-->', readme, flags=re.S))
errors, refs = [], set()

for m in re.finditer(r'''(?:src|srcset|href)=["']([^"']+)["']|!\[[^\]]*\]\(([^)\s]+)\)|\]\(([^)\s]+)\)''', live):
    ref = next(g for g in m.groups() if g)
    if re.match(r'^(https?:|mailto:|#)', ref):
        continue
    refs.add(ref)
    if not os.path.exists(os.path.join(ROOT, ref)):
        errors.append(f'missing file referenced in README: {ref}')

assets = []
for base, _, files in os.walk(os.path.join(ROOT, 'assets')):
    for f in files:
        p = os.path.join(base, f)
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        assets.append(rel)
        try:
            if f.endswith('.svg'):
                minidom.parse(p)
            elif f.endswith(('.gif', '.png')):
                Image.open(p).verify()
        except Exception as e:  # noqa
            errors.append(f'broken asset {rel}: {e}')

unused = [a for a in assets if a not in refs]
optional = [a for a in unused if a in commented]
truly_unused = [a for a in unused if a not in commented]
for bad in ('FLOWER', 'GennisCode', 'Guris da T.I'):
    if bad.lower() in readme.lower():
        errors.append(f'forbidden identity found in README: {bad}')
for ref in refs:
    if ref.startswith('/') or ':' in ref[:3]:
        errors.append(f'absolute path in README: {ref}')

print(f'README references {len(refs)} local files, {len(assets)} assets on disk')
print(f'optional (commented-out placeholders): {len(optional)}')
for a in truly_unused:
    print('  unused asset:', a)
for e in errors:
    print('ERROR:', e)
print('OK - every referenced resource exists' if not errors else f'{len(errors)} problem(s) found')
sys.exit(1 if errors else 0)
