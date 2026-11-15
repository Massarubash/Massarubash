"""build-all.py - regenerates EVERYTHING (banners, dividers, icons, animations), optimizes and verifies.
Run:  python3 tools/build-all.py        (add --no-gif to skip the slow GIF step)
"""
import os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
extra = [a for a in sys.argv[1:] if a == '--no-gif']
steps = [('generate-banners.py', []), ('generate-dividers.py', []), ('generate-icons.py', []),
         ('generate-animations.py', extra), ('optimize-assets.py', ['--skip-gif'] if extra else []), ('verify-assets.py', [])]
for name, args in steps:
    print(f'\n=== {name} ===')
    r = subprocess.run([sys.executable, os.path.join(here, name)] + args)
    if r.returncode:
        sys.exit(r.returncode)
