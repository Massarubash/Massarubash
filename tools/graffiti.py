"""
graffiti.py - shared toolkit for the MASSARU profile assets.

Everything visual in this repo is generated from this file:
  * PAL          -> the colour palette
  * GLYPHS       -> a hand-made single-stroke alphabet (A-Z, 0-9, a few symbols)
  * Scene        -> wall/spray/overlay primitives that can be rendered as SVG *and* as GIF frames
  * letters_svg  -> bubble-letter lettering (outline, shadow, fill, gloss, 3D extrude) with
                    optional "painting" animation (SMIL, works inside GitHub <img> tags)
  * letters_pil  -> the same lettering drawn with Pillow, used for the painting GIF
  * ill_*        -> small illustration fragments (hand, spray can, controller, ...)
Edit colours / text / timings here or in the generate-*.py scripts, then run build-all.py.
"""
import math
import random
import re

import numpy as np
from PIL import Image, ImageDraw

# --------------------------------------------------------------------------- palette
PAL = dict(
    red='#E5192B', crimson='#7A0A1E', dark='#2A0A1A', black='#0B0A0F', graphite='#1B1820',
    magenta='#E0187F', pink='#FF5FA8', purple='#6A2BC2', violet='#3B1670', white='#F6F2EA',
    yellow='#FFD21F', blue='#2F5BFF', cyan='#2AA7FF',
)


def rgb(h, a=255):
    h = h.lstrip('#')
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(a)


# --------------------------------------------------------------------------- stroke alphabet
# Every glyph lives in a box of roughly x 0..100, y 10..110 (single stroke paths, M/L/C/Q only).
GLYPHS = {
    'A': 'M10,110 L50,12 L90,110 M27,76 L73,76',
    'B': 'M14,12 L14,110 M14,12 L55,12 C92,12 92,58 55,60 L14,60 M55,60 C98,60 98,110 55,110 L14,110',
    'C': 'M88,34 C80,5 12,5 12,60 C12,115 80,115 88,86',
    'D': 'M14,12 L14,110 L50,110 C100,110 100,12 50,12 L14,12',
    'E': 'M86,12 L14,12 L14,110 L86,110 M14,60 L70,60',
    'F': 'M86,12 L14,12 L14,110 M14,60 L70,60',
    'G': 'M88,34 C80,5 12,5 12,60 C12,115 85,115 88,80 L55,80',
    'H': 'M14,12 L14,110 M86,12 L86,110 M14,60 L86,60',
    'I': 'M30,12 L70,12 M50,12 L50,110 M30,110 L70,110',
    'J': 'M80,12 L80,80 C80,120 14,118 14,84',
    'K': 'M14,12 L14,110 M86,12 L14,66 M36,48 L88,110',
    'L': 'M14,12 L14,110 L86,110',
    'M': 'M10,110 L10,12 L50,72 L90,12 L90,110',
    'N': 'M12,110 L12,12 L88,110 L88,12',
    'O': 'M50,10 C100,10 100,110 50,110 C0,110 0,10 50,10',
    'P': 'M14,110 L14,12 L55,12 C100,12 100,66 55,66 L14,66',
    'Q': 'M50,10 C100,10 100,110 50,110 C0,110 0,10 50,10 M58,80 L92,116',
    'R': 'M14,110 L14,12 L55,12 C100,12 100,62 55,62 L14,62 M52,62 L88,110',
    'S': 'M86,30 C84,2 14,2 14,36 C14,66 86,54 86,86 C86,118 14,118 12,88',
    'T': 'M10,12 L90,12 M50,12 L50,110',
    'U': 'M12,12 L12,78 C12,120 88,120 88,78 L88,12',
    'V': 'M10,12 L50,110 L90,12',
    'W': 'M6,12 L28,110 L50,40 L72,110 L94,12',
    'X': 'M12,12 L88,110 M88,12 L12,110',
    'Y': 'M10,12 L50,60 L90,12 M50,60 L50,110',
    'Z': 'M12,12 L88,12 L12,110 L88,110',
    '0': 'M50,10 C100,10 100,110 50,110 C0,110 0,10 50,10',
    '1': 'M28,34 L52,12 L52,110',
    '2': 'M14,34 C14,2 86,2 86,36 C86,60 14,90 14,110 L88,110',
    '3': 'M14,22 C30,2 84,6 80,36 C78,56 46,58 46,58 C84,58 90,70 88,86 C84,118 30,118 12,96',
    '4': 'M70,110 L70,12 L10,80 L92,80',
    '5': 'M84,12 L24,12 L18,56 C50,40 90,56 88,84 C84,118 28,118 12,96',
    '6': 'M80,18 C40,0 10,40 12,76 C14,122 84,120 84,82 C84,48 30,46 14,76',
    '7': 'M12,12 L88,12 L40,110',
    '8': 'M50,60 C0,56 6,8 50,10 C94,8 100,56 50,60 C0,64 0,112 50,112 C100,112 100,64 50,60',
    '9': 'M20,102 C60,120 90,80 88,44 C86,-2 16,0 16,38 C16,72 70,74 86,44',
    '@': 'M70,60 C70,40 36,42 36,66 C36,90 70,86 70,60 L70,78 C70,98 94,92 92,62 C88,12 10,14 10,64 C10,112 70,116 90,92',
    '_': 'M10,114 L90,114',
    '.': 'M50,108 L50,109',
    '*': 'M50,50 L50,51',
    '-': 'M25,62 L75,62',
    '!': 'M50,12 L50,80 M50,106 L50,107',
    '?': 'M18,36 C18,4 82,4 82,36 C82,60 50,56 50,82 M50,106 L50,107',
    '/': 'M20,110 L80,12',
    '<': 'M80,14 L16,62 L80,108',
    '>': 'M20,14 L84,62 L20,108',
    '+': 'M50,30 L50,90 M20,60 L80,60',
    ',': 'M50,104 L44,118',
    ':': 'M50,40 L50,41 M50,92 L50,93',
}
GLYPHS['\u2022'] = GLYPHS['*'] = 'M50,62 L50,63'   # bullet used in taglines


def _bez(p0, p1, p2, p3, n=16):
    pts = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


def _quad(p0, p1, p2, n=12):
    pts = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        pts.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return pts


_TOK = re.compile(r'([MLCQ])|(-?\d+\.?\d*)')


def parse_path(d):
    """Parse an absolute M/L/C/Q path into a list of polylines (sampled)."""
    toks = [(m.group(1) or float(m.group(2))) for m in _TOK.finditer(d)]
    i, cmd, pos, cur, subs = 0, None, (0, 0), None, []
    while i < len(toks):
        t = toks[i]
        if isinstance(t, str):
            cmd = t
            i += 1
            continue
        if cmd == 'M':
            pos = (toks[i], toks[i + 1]); i += 2
            cur = [pos]; subs.append(cur); cmd = 'L'
        elif cmd == 'L':
            pos = (toks[i], toks[i + 1]); i += 2
            cur.append(pos)
        elif cmd == 'C':
            p1, p2, p3 = (toks[i], toks[i + 1]), (toks[i + 2], toks[i + 3]), (toks[i + 4], toks[i + 5]); i += 6
            cur.extend(_bez(pos, p1, p2, p3)); pos = p3
        elif cmd == 'Q':
            p1, p2 = (toks[i], toks[i + 1]), (toks[i + 2], toks[i + 3]); i += 4
            cur.extend(_quad(pos, p1, p2)); pos = p2
    return subs


_gcache = {}


def _glyph(ch):
    if ch not in _gcache:
        d = GLYPHS[ch]
        subs = parse_path(d)
        xs = [p[0] for s in subs for p in s]
        _gcache[ch] = (d, subs, min(xs), max(xs))
    return _gcache[ch]


def layout(text, track=30):
    """Returns (glyph list, total width in glyph units). Each glyph: ch, d, subs, dx, x0, w."""
    x, out = 0.0, []
    for ch in text.upper():
        if ch == ' ':
            x += 44
            continue
        if ch not in GLYPHS:
            continue
        d, subs, mn, mx = _glyph(ch)
        out.append(dict(ch=ch, d=d, subs=subs, dx=x - mn, x0=x, w=mx - mn))
        x += (mx - mn) + track
    return out, x - track


def fit(text, max_w, track=30):
    """Glyph height (px) that makes `text` exactly `max_w` px wide."""
    _, wu = layout(text, track)
    return max_w / (wu / 100.0)


# --------------------------------------------------------------------------- timing
# Fractions of the animation loop. Used by both the SVG (SMIL) and the GIF renderer so the
# two always paint in the same order: spray marks -> outline -> fill -> gloss -> drips -> details.
STAGES = dict(spray=(0.0, 0.14), outline=(0.08, 0.46), fill=(0.36, 0.72), hl=(0.62, 0.76),
              extrude=(0.70, 0.80), drips=(0.72, 0.90), details=(0.80, 0.93))


def gtime(name, i, n):
    a, b = STAGES[name]
    span = b - a
    w = span * (0.5 if n > 1 else 1.0)
    t0 = a + (span - w) * (i / max(1, n - 1))
    return t0, t0 + w


def prog(t, st):
    if not st:
        return 1.0
    return max(0.0, min(1.0, (t - st[0]) / (st[1] - st[0])))


def rotate(p, cx, cy, deg):
    a = math.radians(deg)
    x, y = p[0] - cx, p[1] - cy
    return cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)


# --------------------------------------------------------------------------- geometry helpers
def jit(pts, r, j=2.0, sub=3):
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        for k in range(sub):
            t = k / sub
            out.append((a[0] + (b[0] - a[0]) * t + r.uniform(-j, j), a[1] + (b[1] - a[1]) * t + r.uniform(-j, j)))
    return out


def blob(cx, cy, rx, ry, n, r, jag=0.22):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + r.uniform(-jag, jag)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


def star(cx, cy, r1, r2, n, rot=0):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n + math.radians(rot)
        rr = r1 if i % 2 == 0 else r2
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def arrow(x, y, L, W, ang):
    loc = [(0, -W * .25), (L * .6, -W * .25), (L * .6, -W / 2), (L, 0), (L * .6, W / 2), (L * .6, W * .25), (0, W * .25)]
    return [rotate((x + px, y + py), x, y, ang) for px, py in loc]


def pixels(x, y, cols, rows, size, colors, r, dens=0.6):
    out = []
    for c in range(cols):
        for rw in range(rows):
            if r.random() < dens * (1 - rw / (rows + 1)) + 0.15:
                px, py = x + c * size, y + rw * size
                out.append(([(px, py), (px + size, py), (px + size, py + size), (px, py + size)], r.choice(colors)))
    return out


def web(cx, cy, R, a0, a1, spokes=6):
    angs = [a0 + (a1 - a0) * i / (spokes - 1) for i in range(spokes)]
    lines = [[(cx, cy), (cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a)))] for a in angs]
    for k in range(1, 5):
        rr = R * k / 4
        pts = []
        for i, a in enumerate(angs):
            p = (cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a)))
            if i:
                q = angs[i - 1] + (a - angs[i - 1]) / 2
                pts.append((cx + rr * .86 * math.cos(math.radians(q)), cy + rr * .86 * math.sin(math.radians(q))))
            pts.append(p)
        lines.append(pts)
    return lines


def scribble(x, y, w, h, r, n=46):
    pts = []
    for i in range(n):
        ang = i * 0.62
        pts.append((x + w * i / n + math.cos(ang) * h * .5, y + math.sin(ang) * h * .5 + r.uniform(-3, 3)))
    return pts


def zigzag(x, y, w, amp, n):
    return [(x + w * i / (n - 1), y + (amp if i % 2 else -amp)) for i in range(n)]


def cloud(cx, cy, rad, n, r, rmax=1.7):
    out = []
    for _ in range(n):
        out.append((r.gauss(cx, rad / 2.2), r.gauss(cy, rad / 2.2), r.uniform(.5, rmax)))
    return out


def swoosh(x0, x1, y, amp, n=24):
    return [(x0 + (x1 - x0) * i / (n - 1), y + math.sin(i / (n - 1) * math.pi) * -amp + (i / (n - 1)) * amp * .6) for i in range(n)]


# --------------------------------------------------------------------------- scene
class Scene:  # pass bg=False for a transparent canvas
    """wall = static backdrop (may float), spray = first marks, over = things painted last."""

    def __init__(self, w, h, bg=None):
        self.w, self.h, self.bg = w, h, (PAL['black'] if bg is None else bg)
        self.wall, self.spray, self.over = [], [], []

    def add(self, layer, t, **kw):
        it = dict(t=t, **kw)
        getattr(self, layer).append(it)
        return it


def _ps(pts):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def _pd(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def fade_wrap(el, st, T, animate):
    if not (animate and st):
        return el
    t0, t1 = st
    return (f'<g><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{t0:.3f};{t1:.3f};1" '
            f'dur="{T}s" repeatCount="indefinite"/>{el}</g>')


def dash_anim(t0, t1, T):
    return (f'<animate attributeName="stroke-dashoffset" values="1.1;1.1;0;0" '
            f'keyTimes="0;{t0:.3f};{t1:.3f};1" dur="{T}s" repeatCount="indefinite"/>')


def item_svg(it, uid, k, animate, T):
    t, a, st = it['t'], it.get('a', 1), it.get('stage')
    defs = ''
    if t == 'poly':
        sk = ''
        if it.get('stroke'):
            sk = f' stroke="{it["stroke"]}" stroke-width="{it.get("sw", 3)}" stroke-linejoin="round"'
        el = f'<polygon points="{_ps(it["pts"])}" fill="{it["fill"]}" fill-opacity="{a}"{sk}/>'
        el = fade_wrap(el, st, T, animate)
    elif t == 'circle':
        cx, cy = it['c']
        sk = f' stroke="{it["stroke"]}" stroke-width="{it.get("sw", 3)}"' if it.get('stroke') else ''
        el = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{it["r"]:.1f}" fill="{it["fill"]}" fill-opacity="{a}"{sk}/>'
        el = fade_wrap(el, st, T, animate)
    elif t == 'halo':
        cx, cy = it['c']
        gid = f'h{uid}{k}'
        defs = (f'<radialGradient id="{gid}"><stop offset="0" stop-color="{it["color"]}" stop-opacity="{a}"/>'
                f'<stop offset="1" stop-color="{it["color"]}" stop-opacity="0"/></radialGradient>')
        el = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{it["r"]:.1f}" fill="url(#{gid})"/>'
    elif t == 'line':
        base = (f'<path d="{_pd(it["pts"])}" fill="none" stroke="{it["color"]}" stroke-width="{it["w"]}" '
                f'stroke-opacity="{a}" stroke-linecap="round" stroke-linejoin="round"')
        if animate and st:
            el = base + f' pathLength="1" stroke-dasharray="1 2" stroke-dashoffset="0">{dash_anim(st[0], st[1], T)}</path>'
        else:
            el = base + '/>'
    elif t == 'dots':
        c = ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>' for x, y, r in it['dots'])
        el = fade_wrap(f'<g fill="{it["color"]}" fill-opacity="{a}">{c}</g>', st, T, animate)
    elif t == 'drip':
        x, y, L, w = it['x'], it['y'], it['len'], it['w']
        col = it['color']
        if animate and st:
            kt = f'0;{st[0]:.3f};{st[1]:.3f};1'
            el = (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round">'
                  f'<animate attributeName="y2" values="{y:.1f};{y:.1f};{y + L:.1f};{y + L:.1f}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></line>'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{w * .85:.1f}" fill="{col}">'
                  f'<animate attributeName="cy" values="{y:.1f};{y:.1f};{y + L:.1f};{y + L:.1f}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></circle>')
        else:
            el = (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y + L:.1f}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round"/>'
                  f'<circle cx="{x:.1f}" cy="{y + L:.1f}" r="{w * .85:.1f}" fill="{col}"/>')
    else:
        raise ValueError(t)
    fl = it.get('fl')
    if animate and fl:
        el = (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{fl[0]} {fl[1]};0 0" '
              f'dur="{fl[2]}s" repeatCount="indefinite"/>{el}</g>')
    return defs, el


def grain_svg(w, h, uid, op=0.12):
    return (f'<filter id="g{uid}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" '
            f'numOctaves="2" seed="4"/><feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 -1.6 1.0"/></filter>'
            f'<rect width="{w}" height="{h}" filter="url(#g{uid})" opacity="{op}"/>')


def scene_svg(sc, uid, animate=False, T=14):
    defs, parts = [], {}
    k = 0
    for layer in ('wall', 'spray', 'over'):
        buf = []
        for it in getattr(sc, layer):
            d, el = item_svg(it, uid, k, animate, T)
            k += 1
            if d:
                defs.append(d)
            buf.append(el)
        parts[layer] = ''.join(buf)
    if sc.bg:
        g = grain_svg(sc.w, sc.h, uid)
        f_start = g.index('<rect')
        defs.append(g[:f_start])
        parts['wall'] = f'<rect width="{sc.w}" height="{sc.h}" fill="{sc.bg}"/>' + parts['wall'] + g[f_start:]
    parts['defs'] = ''.join(defs)
    return parts


def svg_doc(w, h, body, title, desc, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'<title>{title}</title><desc>{desc}</desc><defs>{defs}</defs>{body}</svg>\n')


def global_fade(inner, T, animate):
    if not animate:
        return inner
    return (f'<g><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.95;0.99;1" dur="{T}s" '
            f'repeatCount="indefinite"/>{inner}</g>')


# --------------------------------------------------------------------------- lettering (SVG)
def _glyph_el(g, width, col, st, T, animate):
    base = (f'<path d="{g["d"]}" transform="translate({g["dx"]:.1f},0)" fill="none" stroke="{col}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" pathLength="1"')
    if animate:
        return base + f' stroke-dasharray="1 2" stroke-dashoffset="0">{dash_anim(st[0], st[1], T)}</path>'
    return base + '/>'


def letters_svg(text, cx, y, h, st, animate=False, T=14, rot=0, track=30):
    """Bubble lettering. st keys: fill(list), fw, outline(color), ow, shadow(color,off), hl(color), extrude(color,n,(dx,dy))."""
    s = h / 100.0
    lay, wu = layout(text, track)
    W = wu * s
    x0, cy, n = cx - W / 2, y + h / 2, len(lay)
    o = [f'<g transform="rotate({rot:.2f} {cx:.1f} {cy:.1f})">',
         f'<g transform="translate({x0:.1f},{y - 10 * s:.1f}) scale({s:.4f})">']

    def layer(stage, width, colfn, off=(0, 0), op=1.0):
        o.append(f'<g transform="translate({off[0]},{off[1]})" opacity="{op}">')
        for i, g in enumerate(lay):
            o.append(_glyph_el(g, width, colfn(i), gtime(stage, i, n), T, animate))
        o.append('</g>')

    ex = st.get('extrude')
    if ex:
        col, steps, (dx, dy) = ex
        buf = []
        for k in range(steps, 0, -1):
            buf.append(f'<g transform="translate({dx * k:.2f},{dy * k:.2f})">' +
                       ''.join(_glyph_el(g, st['ow'], col, None, T, False) for g in lay) + '</g>')
        o.append(fade_wrap(''.join(buf), STAGES['extrude'], T, animate))
    if st.get('shadow'):
        c, off = st['shadow']
        layer('outline', st['ow'] + 6, lambda i: c, off)
    layer('outline', st['ow'], lambda i: st['outline'])
    layer('fill', st['fw'], lambda i: st['fill'][i % len(st['fill'])])
    if st.get('hl'):
        layer('hl', max(4, st['fw'] * .22), lambda i: st['hl'], (-st['fw'] * .18, -st['fw'] * .22), 0.7)
    o.append('</g></g>')
    return ''.join(o)


def plain_svg(text, x, y, h, color, sw, anchor='middle', track=22, animate=False, T=12, t0=0.1, t1=0.6, shadow=None):
    s = h / 100.0
    lay, wu = layout(text, track)
    W = wu * s
    x0 = x - W / 2 if anchor == 'middle' else (x if anchor == 'start' else x - W)
    n = len(lay)
    o = [f'<g transform="translate({x0:.1f},{y - 10 * s:.1f}) scale({s:.4f})">']

    def win(i):
        span = t1 - t0
        w = span * (0.5 if n > 1 else 1)
        a = t0 + (span - w) * (i / max(1, n - 1))
        return a, a + w

    if shadow:
        o.append('<g transform="translate(4,5)">' + ''.join(_glyph_el(g, sw / s, shadow, win(i), T, animate) for i, g in enumerate(lay)) + '</g>')
    o.append(''.join(_glyph_el(g, sw / s, color, win(i), T, animate) for i, g in enumerate(lay)))
    o.append('</g>')
    return ''.join(o)


# --------------------------------------------------------------------------- drips
DRIP_POS = {'U': [.3, .65], 'S': [.35, .6], 'O': [.4, .6], 'C': [.4], 'G': [.45], 'J': [.35], 'T': [.5], 'I': [.5],
            'Y': [.5], 'E': [.2, .8], 'L': [.2, .7], 'Z': [.2, .8], 'B': [.3], 'D': [.3], 'P': [.15], 'F': [.15],
            'R': [.12, .9], 'K': [.12, .9], 'A': [.1, .9], 'M': [.1, .9], 'N': [.12, .88], 'H': [.12, .88],
            'W': [.15, .5, .85], 'V': [.5], 'X': [.1, .9], 'Q': [.4, .9]}


def make_drips(text, cx, y, h, fills, r, track=30, rot=0, ow=37, stage=(0.72, 0.90), chance=0.8):
    s = h / 100.0
    lay, wu = layout(text, track)
    W = wu * s
    x0, cy = cx - W / 2, y + h / 2
    out = []
    for i, g in enumerate(lay):
        col = fills[i % len(fills)]
        for f in DRIP_POS.get(g['ch'], [.5]):
            if r.random() > chance:
                continue
            gx = x0 + (g['x0'] + g['w'] * f) * s
            gy = y + h + ow * s * 0.42
            px, py = rotate((gx, gy), cx, cy, rot)
            L = r.uniform(.22, .75) * h
            wd = r.uniform(4, 8) * (h / 130.0)
            a = stage[0] + (stage[1] - stage[0]) * r.uniform(0, .45)
            out.append(dict(t='drip', x=px, y=py, len=L, w=wd, color=col, stage=(a, min(stage[1], a + (stage[1] - stage[0]) * .55))))
    return out


# --------------------------------------------------------------------------- PIL renderers
def _dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def _partial(dr, polys, f, wpx, col, SS):
    segs = [(p[i], p[i + 1]) for p in polys for i in range(len(p) - 1)]
    total = sum(_dist(a, b) for a, b in segs)
    if total == 0 or f <= 0:
        return
    target, acc, r = total * f, 0.0, wpx * SS / 2
    for a, b in segs:
        if acc >= target:
            break
        L = _dist(a, b)
        k = 1.0 if L == 0 else min(1.0, (target - acc) / L)
        e = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        dr.line([(a[0] * SS, a[1] * SS), (e[0] * SS, e[1] * SS)], fill=col, width=max(1, int(wpx * SS)))
        for p in (a, e):
            dr.ellipse([p[0] * SS - r, p[1] * SS - r, p[0] * SS + r, p[1] * SS + r], fill=col)
        acc += L


def letters_pil(img, text, cx, y, h, st, t, rot=0, track=30, SS=2):
    s = h / 100.0
    lay, wu = layout(text, track)
    W = wu * s
    x0, cy, n = cx - W / 2, y + h / 2, len(lay)
    glyphs = []
    for g in lay:
        glyphs.append([[rotate(((px + g['dx']) * s + x0, (py - 10) * s + y), cx, cy, rot) for px, py in sub] for sub in g['subs']])

    def shift(polys, off):
        o = rotate((off[0] * s, off[1] * s), 0, 0, rot)
        return [[(p[0] + o[0], p[1] + o[1]) for p in poly] for poly in polys]

    def layer(dr, stage, width, colfn, off=(0, 0)):
        for i, polys in enumerate(glyphs):
            f = prog(t, gtime(stage, i, n))
            if f > 0:
                _partial(dr, shift(polys, off), f, width * s, colfn(i), SS)

    dr = ImageDraw.Draw(img)
    if st.get('shadow'):
        c, off = st['shadow']
        layer(dr, 'outline', st['ow'] + 6, lambda i: rgb(c), off)
    layer(dr, 'outline', st['ow'], lambda i: rgb(st['outline']))
    layer(dr, 'fill', st['fw'], lambda i: rgb(st['fill'][i % len(st['fill'])]))
    if st.get('hl'):
        ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d2 = ImageDraw.Draw(ov)
        layer(d2, 'hl', max(4, st['fw'] * .22), lambda i: rgb(st['hl'], 178), (-st['fw'] * .18, -st['fw'] * .22))
        img.alpha_composite(ov)


def _overlay(img):
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    return ov, ImageDraw.Draw(ov)


def pil_item(img, it, t, SS):
    ty, a, st = it['t'], it.get('a', 1), it.get('stage')
    p = prog(t, st) if st else 1.0
    if p <= 0:
        return
    W, H = img.size
    if ty == 'halo':
        cx, cy = it['c']
        r = int(it['r'] * SS)
        grad = Image.radial_gradient('L').resize((2 * r, 2 * r))
        mask = grad.point(lambda v: int(max(0, 255 - v) * a * p))
        solid = Image.new('RGBA', (2 * r, 2 * r), rgb(it['color']))
        solid.putalpha(mask)
        ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ov.paste(solid, (int(cx * SS) - r, int(cy * SS) - r))
        img.alpha_composite(ov)
        return
    ov, dr = _overlay(img)
    if ty == 'poly':
        pts = [(x * SS, y * SS) for x, y in it['pts']]
        dr.polygon(pts, fill=rgb(it['fill'], 255 * a * p))
        if it.get('stroke'):
            dr.line(pts + [pts[0]], fill=rgb(it['stroke'], 255 * p), width=max(1, int(it.get('sw', 3) * SS)), joint='curve')
    elif ty == 'circle':
        cx, cy = it['c']
        r = it['r'] * SS
        dr.ellipse([cx * SS - r, cy * SS - r, cx * SS + r, cy * SS + r], fill=rgb(it['fill'], 255 * a * p),
                   outline=rgb(it['stroke'], 255 * p) if it.get('stroke') else None, width=int(it.get('sw', 3) * SS))
    elif ty == 'line':
        _partial(dr, [it['pts']], p, it['w'], rgb(it['color'], 255 * a), SS)
    elif ty == 'dots':
        for x, y, r in it['dots']:
            dr.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=rgb(it['color'], 255 * a * p))
    elif ty == 'drip':
        e = p * p * (3 - 2 * p)
        x, y, L, w = it['x'], it['y'], it['len'] * e, it['w']
        col = rgb(it['color'])
        dr.line([(x * SS, y * SS), (x * SS, (y + L) * SS)], fill=col, width=int(w * SS))
        r = w * .85 * SS
        dr.ellipse([x * SS - r, (y + L) * SS - r, x * SS + r, (y + L) * SS + r], fill=col)
    img.alpha_composite(ov)


def scene_pil(sc, SS=2):
    img = Image.new('RGBA', (sc.w * SS, sc.h * SS), rgb(sc.bg))
    for it in sc.wall:
        pil_item(img, it, 1.0, SS)
    return img


# --------------------------------------------------------------------------- main banner scene (shared by SVG + GIF)
MAIN = dict(text='MASSARU', cx=600, y=112, h=128, rot=-3, track=28)
STYLE_MAIN = dict(fill=[PAL['red'], PAL['red'], PAL['magenta'], PAL['magenta'], PAL['red'], PAL['red'], PAL['red']],
                  fw=27, outline=PAL['black'], ow=46, shadow=(PAL['crimson'], (11, 13)), hl=PAL['white'])


def scene_main():
    r = random.Random(7)
    sc = Scene(1200, 420)
    A = sc.add
    A('wall', 'halo', c=(600, 210), r=440, color=PAL['crimson'], a=.8)
    A('wall', 'halo', c=(110, 390), r=300, color=PAL['purple'], a=.55)
    A('wall', 'halo', c=(1110, 50), r=270, color=PAL['blue'], a=.3)
    A('wall', 'poly', pts=jit(blob(590, 205, 545, 150, 26, r), r, 2.5), fill=PAL['crimson'], a=.95, fl=(6, -3, 9))
    A('wall', 'poly', pts=jit(arrow(20, 330, 570, 175, -10), r), fill=PAL['magenta'], a=.92, stroke=PAL['black'], sw=4, fl=(-8, 4, 11))
    A('wall', 'poly', pts=jit(arrow(1195, 112, 540, 150, 188), r), fill=PAL['purple'], a=.95, stroke=PAL['black'], sw=4, fl=(8, 5, 10))
    A('wall', 'poly', pts=jit(blob(560, 232, 440, 105, 24, r, .18), r, 2), fill=PAL['red'], a=.35)
    for pts, c in pixels(905, 10, 11, 6, 17, [PAL['red'], PAL['crimson'], PAL['black'], PAL['magenta']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.95)
    for pts, c in pixels(14, 300, 8, 5, 15, [PAL['purple'], PAL['violet'], PAL['black']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.9)
    for ln in web(0, 0, 215, 8, 82):
        A('wall', 'line', pts=ln, color=PAL['white'], w=1.6, a=.5)
    for ln in web(1200, 420, 190, 188, 262):
        A('wall', 'line', pts=ln, color=PAL['white'], w=1.5, a=.4)
    A('wall', 'poly', pts=jit(star(120, 88, 66, 36, 9, 8), r, 1.5), fill=PAL['yellow'], a=.96, stroke=PAL['black'], sw=4, fl=(0, 7, 6))
    A('wall', 'poly', pts=jit(star(1092, 338, 84, 46, 11, 0), r, 1.5), fill=PAL['yellow'], a=.9, stroke=PAL['black'], sw=4, fl=(0, -8, 7))
    A('wall', 'circle', c=(1068, 86), r=50, fill=PAL['blue'], a=.9, stroke=PAL['white'], sw=4, fl=(-5, 6, 8))
    A('wall', 'line', pts=scribble(330, 44, 370, 40, r), color=PAL['yellow'], w=4, a=.95)
    A('wall', 'line', pts=scribble(690, 372, 330, 30, r), color=PAL['white'], w=3, a=.85)
    A('wall', 'line', pts=zigzag(46, 176, 110, 16, 7), color=PAL['blue'], w=7, a=.95)
    A('wall', 'line', pts=zigzag(1030, 252, 120, 14, 7), color=PAL['yellow'], w=6, a=.9)
    A('wall', 'dots', dots=cloud(270, 312, 130, 260, r), color=PAL['magenta'], a=.85)
    A('wall', 'dots', dots=cloud(900, 300, 120, 220, r), color=PAL['red'], a=.85)
    A('wall', 'dots', dots=cloud(640, 60, 100, 120, r), color=PAL['pink'], a=.7)
    # first marks of spray (painted first)
    s = MAIN['h'] / 100
    lay, wu = layout(MAIN['text'], MAIN['track'])
    x0 = MAIN['cx'] - wu * s / 2
    for i, g in enumerate(lay):
        gx = x0 + (g['x0'] + g['w'] / 2) * s
        A('spray', 'line', pts=[(gx - 18, MAIN['y'] - 18), (gx + 18, MAIN['y'] - 18)], color=PAL['yellow'], w=4, a=.95, stage=(0.0 + i * .012, 0.05 + i * .012))
        A('spray', 'line', pts=[(gx, MAIN['y'] - 26), (gx, MAIN['y'] - 10)], color=PAL['yellow'], w=4, a=.95, stage=(0.0 + i * .012, 0.05 + i * .012))
        A('spray', 'dots', dots=cloud(gx, MAIN['y'] + MAIN['h'] / 2, 70, 55, r, 1.4), color=PAL['white'], a=.8, stage=(0.02 + i * .012, 0.12))
    # details (painted last)
    A('over', 'line', pts=swoosh(250, 950, 300, 34), color=PAL['blue'], w=11, a=1, stage=STAGES['details'])
    A('over', 'line', pts=swoosh(240, 940, 294, 34), color=PAL['yellow'], w=7, a=1, stage=STAGES['details'])
    for cx, cy, rr in [(196, 148, 17), (1010, 150, 14), (990, 288, 12), (170, 290, 10)]:
        A('over', 'poly', pts=star(cx, cy, rr, rr * .28, 4, 0), fill=PAL['yellow'], a=1, stage=(0.82, 0.92))
    A('over', 'line', pts=scribble(880, 340, 160, 26, r, 30), color=PAL['white'], w=3, a=.9, stage=(0.86, 0.96))
    for d in make_drips(MAIN['text'], MAIN['cx'], MAIN['y'], MAIN['h'], STYLE_MAIN['fill'], r, MAIN['track'], MAIN['rot'], STYLE_MAIN['ow']):
        A('over', 'drip', **{k: v for k, v in d.items() if k != 't'})
    return sc


# --------------------------------------------------------------------------- illustration fragments (SVG only)
HAND = [(32, 118), (24, 96), (14, 74), (6, 62), (5, 52), (11, 47), (19, 52), (27, 64), (31, 66), (28, 34), (27, 16), (32, 10),
        (38, 16), (40, 40), (42, 44), (43, 10), (44, 2), (50, 0), (55, 4), (55, 40), (58, 44), (60, 14), (62, 8), (68, 8),
        (71, 16), (70, 44), (72, 48), (76, 30), (81, 26), (87, 30), (86, 54), (84, 74), (80, 96), (76, 118)]


def ill_hand(x, y, s, uid='h'):
    pts = _ps(HAND)
    r = random.Random(3)
    sp = ''.join(f'<circle cx="{r.gauss(48, 50):.1f}" cy="{r.gauss(60, 56):.1f}" r="{r.uniform(.6, 1.8):.1f}" fill="{PAL["purple"]}"/>' for _ in range(90))
    return (f'<g transform="translate({x},{y}) scale({s})"><defs><filter id="bl{uid}" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="9"/></filter></defs>'
            f'<polygon points="{pts}" fill="{PAL["magenta"]}" stroke="{PAL["magenta"]}" stroke-width="30" stroke-linejoin="round" filter="url(#bl{uid})" opacity=".95"/>{sp}'
            f'<polygon points="{pts}" transform="translate(4,5)" fill="{PAL["black"]}" opacity=".55" stroke="{PAL["black"]}" stroke-width="5" stroke-linejoin="round"/>'
            f'<polygon points="{pts}" fill="{PAL["white"]}" stroke="{PAL["blue"]}" stroke-width="5" stroke-linejoin="round"/></g>')


def ill_can(x, y, s):
    r = random.Random(11)
    sp = ''.join(f'<circle cx="{r.gauss(-20, 18):.1f}" cy="{r.gauss(8, 12):.1f}" r="{r.uniform(.7, 2.2):.1f}" fill="{PAL["yellow"]}"/>' for _ in range(40))
    return (f'<g transform="translate({x},{y}) scale({s})">{sp}'
            f'<rect x="12" y="34" width="46" height="78" rx="8" fill="{PAL["purple"]}" stroke="{PAL["black"]}" stroke-width="4"/>'
            f'<rect x="12" y="54" width="46" height="24" fill="{PAL["yellow"]}" stroke="{PAL["black"]}" stroke-width="4"/>'
            f'<path d="M17,34 L22,18 L48,18 L53,34 Z" fill="#CFCFD8" stroke="{PAL["black"]}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="29" y="6" width="12" height="14" rx="3" fill="{PAL["red"]}" stroke="{PAL["black"]}" stroke-width="4"/>'
            f'<path d="M20,44 L20,104" stroke="{PAL["white"]}" stroke-width="4" stroke-linecap="round" opacity=".6"/></g>')


def ill_controller(x, y, s):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M20,50 C20,30 50,28 60,36 L100,36 C110,28 140,30 140,50 L148,90 C150,108 130,112 118,98 L108,84 L52,84 L42,98 C30,112 10,108 12,90 Z" '
            f'transform="translate(5,6)" fill="{PAL["black"]}" opacity=".6"/>'
            f'<path d="M20,50 C20,30 50,28 60,36 L100,36 C110,28 140,30 140,50 L148,90 C150,108 130,112 118,98 L108,84 L52,84 L42,98 C30,112 10,108 12,90 Z" '
            f'fill="{PAL["magenta"]}" stroke="{PAL["black"]}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M44,50 L44,72 M33,61 L55,61" stroke="{PAL["white"]}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="112" cy="50" r="7" fill="{PAL["yellow"]}" stroke="{PAL["black"]}" stroke-width="3"/>'
            f'<circle cx="126" cy="62" r="7" fill="{PAL["blue"]}" stroke="{PAL["black"]}" stroke-width="3"/>'
            f'<circle cx="98" cy="62" r="7" fill="{PAL["red"]}" stroke="{PAL["black"]}" stroke-width="3"/>'
            f'<circle cx="112" cy="74" r="7" fill="{PAL["white"]}" stroke="{PAL["black"]}" stroke-width="3"/></g>')


def ill_window(x, y, s, prompt=False):
    body = ''
    if prompt:
        body = (f'<path d="M22,50 L38,62 L22,74" fill="none" stroke="{PAL["yellow"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M48,76 L82,76" stroke="{PAL["white"]}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M22,100 L120,100 M22,118 L90,118" stroke="{PAL["cyan"]}" stroke-width="5" stroke-linecap="round" opacity=".8"/>')
    else:
        body = (f'<path d="M22,52 L96,52" stroke="{PAL["magenta"]}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M36,70 L130,70" stroke="{PAL["yellow"]}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M36,88 L84,88" stroke="{PAL["white"]}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M22,106 L150,106" stroke="{PAL["cyan"]}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M36,124 L108,124" stroke="{PAL["red"]}" stroke-width="6" stroke-linecap="round"/>')
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="5" y="6" width="186" height="140" rx="12" fill="{PAL["black"]}" opacity=".6"/>'
            f'<rect x="0" y="0" width="186" height="140" rx="12" fill="{PAL["graphite"]}" stroke="{PAL["white"]}" stroke-width="4"/>'
            f'<path d="M0,26 L186,26" stroke="{PAL["white"]}" stroke-width="4"/>'
            f'<circle cx="16" cy="13" r="5" fill="{PAL["red"]}"/><circle cx="32" cy="13" r="5" fill="{PAL["yellow"]}"/><circle cx="48" cy="13" r="5" fill="{PAL["blue"]}"/>{body}</g>')


def ill_ig(x, y, s, uid='ig'):
    return (f'<g transform="translate({x},{y}) scale({s})"><defs><linearGradient id="{uid}" x1="0" y1="1" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{PAL["yellow"]}"/><stop offset=".45" stop-color="{PAL["red"]}"/>'
            f'<stop offset=".75" stop-color="{PAL["magenta"]}"/><stop offset="1" stop-color="{PAL["purple"]}"/></linearGradient></defs>'
            f'<rect x="6" y="8" width="100" height="100" rx="30" fill="{PAL["black"]}" opacity=".6"/>'
            f'<rect x="0" y="0" width="100" height="100" rx="30" fill="url(#{uid})" stroke="{PAL["black"]}" stroke-width="6"/>'
            f'<rect x="14" y="14" width="72" height="72" rx="22" fill="none" stroke="{PAL["white"]}" stroke-width="7"/>'
            f'<circle cx="50" cy="50" r="17" fill="none" stroke="{PAL["white"]}" stroke-width="7"/>'
            f'<circle cx="71" cy="29" r="5" fill="{PAL["white"]}"/></g>')


def ill_heart(x, y, s, color=None):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M50,88 C-10,40 20,0 50,32 C80,0 110,40 50,88 Z" transform="translate(4,5)" fill="{PAL["black"]}" opacity=".6"/>'
            f'<path d="M50,88 C-10,40 20,0 50,32 C80,0 110,40 50,88 Z" fill="{color or PAL["red"]}" stroke="{PAL["black"]}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M24,30 C30,18 40,18 44,28" fill="none" stroke="{PAL["white"]}" stroke-width="5" stroke-linecap="round" opacity=".8"/></g>')


def ill_burst(x, y, s, color=None):
    pts = _ps(star(0, 0, 60, 36, 10, 5))
    return (f'<g transform="translate({x},{y}) scale({s})"><polygon points="{pts}" transform="translate(4,5)" fill="{PAL["black"]}" opacity=".6"/>'
            f'<polygon points="{pts}" fill="{color or PAL["yellow"]}" stroke="{PAL["black"]}" stroke-width="5" stroke-linejoin="round"/></g>')


def reveal(frag, st, T, animate=True):
    return fade_wrap(frag, st, T, animate)


def float_wrap(frag, dx, dy, dur):
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};0 0" dur="{dur}s" '
            f'repeatCount="indefinite"/>{frag}</g>')


def compose_scene(sc, uid, T, animate, letters='', extra_over='', title='', desc='', pre_letters=''):
    """wall -> (fade group: spray, pre_letters, letters, over, extras)"""
    p = scene_svg(sc, uid, animate, T)
    inner = pre_letters + p['spray'] + letters + p['over'] + extra_over
    return svg_doc(sc.w, sc.h, p['wall'] + global_fade(inner, T, animate), title, desc, p['defs'])
