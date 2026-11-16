"""
street.py - street-art building blocks for the MASSARU assets (concrete walls, wheat-paste posters, pixo tags,
wildstyle arrows, overspray, halftone, tape) + the hero scene shared by the static banner and the painting GIF.
Every helper takes `A` (a Scene.add function) and a random.Random, and only creates plain scene items, so the same
artwork renders as SVG (animated) and as GIF frames.
"""
import math
import random

from graffiti import *  # noqa
from graffiti import _dist


# ----------------------------------------------------------------------------- basics
def rough(pts, r, j=1.5, step=14):
    """Subdivide + jitter a polyline so lines look hand-drawn."""
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(_dist(a, b) // step))
        for k in range(1, n + 1):
            t = k / n
            jj = j if k < n else 0
            out.append((a[0] + (b[0] - a[0]) * t + r.uniform(-jj, jj), a[1] + (b[1] - a[1]) * t + r.uniform(-jj, jj)))
    return out


def marker(A, pts, color, w, r, layer='wall', stage=None, under=PAL['black'], a=1.0, j=1.4, hi=None):
    """A marker / spray stroke: black underlay, colour body and an optional thin light edge."""
    p = rough(pts, r, j)
    if under:
        A(layer, 'line', pts=p, color=under, w=w + 5, a=.95 * a, stage=stage)
    A(layer, 'line', pts=p, color=color, w=w, a=a, stage=stage)
    if hi:
        A(layer, 'line', pts=[(x - w * .18, y - w * .22) for x, y in p], color=hi, w=max(1.5, w * .16), a=.55, stage=stage)


def overspray(A, r, pts, color, n, rad, layer='wall', a=.7, stage=None, rmax=1.8):
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)] or [(pts[0], pts[0])]
    dots = []
    for _ in range(n):
        p, q = r.choice(segs)
        t = r.random()
        dots.append((r.gauss(p[0] + (q[0] - p[0]) * t, rad), r.gauss(p[1] + (q[1] - p[1]) * t, rad), r.uniform(.5, rmax)))
    A(layer, 'dots', dots=dots, color=color, a=a, stage=stage)


def halftone(A, x, y, w, h, step, color, direction='right', layer='wall', a=.9, stage=None):
    dots = []
    cols, rows = int(w // step), int(h // step)
    for i in range(cols):
        for k in range(rows):
            f = {'right': 1 - i / cols, 'left': i / cols, 'down': 1 - k / rows, 'up': k / rows}[direction]
            rad = step * .5 * f
            if rad > .5:
                ox = step / 2 if k % 2 else 0
                dots.append((x + i * step + ox, y + k * step, rad))
    A(layer, 'dots', dots=dots, color=color, a=a, stage=stage)


def concrete(A, r, w, h):
    """Slab seams, stains and scuffs for the wall."""
    for x in (w * .31, w * .68):
        A('wall', 'line', pts=[(x + r.uniform(-4, 4), 0), (x + r.uniform(-4, 4), h)], color='#000000', w=2, a=.4)
    A('wall', 'line', pts=[(0, h * .64), (w, h * .64 + r.uniform(-6, 6))], color='#000000', w=2, a=.32)
    for _ in range(6):
        A('wall', 'halo', c=(r.uniform(0, w), r.uniform(0, h)), r=r.uniform(90, 210), color='#000000', a=.35)
    A('wall', 'dots', dots=[(r.uniform(0, w), r.uniform(0, h), r.uniform(.5, 1.4)) for _ in range(140)], color='#8a8494', a=.35)


def color_field(A, r, cx, cy, rx, ry, color, a=.95, jag=.12, n=26, layer='wall', fl=None, spray=130, stage=None):
    pts = jit(blob(cx, cy, rx, ry, n, r, jag), r, 2.2, 2)
    A(layer, 'poly', pts=pts, fill=color, a=a, fl=fl, stage=stage)
    if spray:
        overspray(A, r, pts + [pts[0]], color, spray, 9, layer, .55, stage)
    return pts


def tape(A, r, x, y, w, h, ang, layer='wall'):
    pts = [rotate(p, x + w / 2, y + h / 2, ang) for p in [(x, y), (x + w, y + r.uniform(-2, 2)), (x + w, y + h), (x, y + h + r.uniform(-2, 2))]]
    A(layer, 'poly', pts=pts, fill='#E9DFAE', a=.72)


def paste(A, r, x, y, w, h, ang, ink=PAL['black'], paper='#E8E0CF', accent=PAL['red'], layer='wall'):
    """Torn wheat-paste poster with halftone print, ink blocks and tape."""
    c = (x + w / 2, y + h / 2)
    top = [(x + w * i / 12 + r.uniform(-4, 4), y + r.uniform(-5, 5)) for i in range(13)]
    right = [(x + w + r.uniform(-4, 4), y + h * i / 6 + r.uniform(-3, 3)) for i in range(1, 6)]
    bot = [(x + w * i / 12 + r.uniform(-4, 4), y + h + r.uniform(-6, 6)) for i in range(12, -1, -1)]
    left = [(x + r.uniform(-4, 4), y + h * i / 6 + r.uniform(-3, 3)) for i in range(5, 0, -1)]
    pts = [rotate(p, c[0], c[1], ang) for p in top + right + bot + left]
    A(layer, 'poly', pts=[(px + 4, py + 5) for px, py in pts], fill='#000000', a=.35)
    A(layer, 'poly', pts=pts, fill=paper, a=.97, stroke=PAL['black'], sw=1.6)
    blk = [rotate(p, c[0], c[1], ang) for p in jit([(x + w * .08, y + h * .14), (x + w * .62, y + h * .1), (x + w * .6, y + h * .5), (x + w * .1, y + h * .55)], r, 2.5, 4)]
    A(layer, 'poly', pts=blk, fill=ink, a=.88)
    blk2 = [rotate(p, c[0], c[1], ang) for p in jit([(x + w * .55, y + h * .55), (x + w * .94, y + h * .5), (x + w * .92, y + h * .92), (x + w * .52, y + h * .9)], r, 2.5, 4)]
    A(layer, 'poly', pts=blk2, fill=accent, a=.9)
    halftone(A, x + w * .08, y + h * .6, w * .44, h * .32, 6, ink, 'right', layer, .85)
    tape(A, r, x - 10, y - 6, 46, 14, ang - 28, layer)
    tape(A, r, x + w - 36, y + h - 10, 46, 14, ang - 24, layer)


def wild_arrow(A, r, x, y, L, W, ang, color, ext=PAL['violet'], layer='wall', fl=None, stage=None):
    """Angular wildstyle arrow with a notched tail, 3D block and black outline."""
    loc = [(0, -W * .2), (L * .62, -W * .2), (L * .52, -W * .5), (L, 0), (L * .52, W * .5), (L * .62, W * .2), (0, W * .2), (L * .1, 0)]
    pts = jit([rotate((x + px, y + py), x, y, ang) for px, py in loc], r, 1.3, 2)
    for k in range(7, 0, -1):
        A(layer, 'poly', pts=[(px + 1.7 * k, py + 2.1 * k) for px, py in pts], fill=ext, a=1, stroke=PAL['black'] if k == 7 else None, sw=3, stage=stage)
    A(layer, 'poly', pts=pts, fill=color, a=1, stroke=PAL['black'], sw=4.5, fl=fl, stage=stage)
    a0 = rotate((x + L * .12, y - W * .08), x, y, ang)
    a1 = rotate((x + L * .6, y - W * .1), x, y, ang)
    A(layer, 'line', pts=[a0, a1], color=PAL['white'], w=2.4, a=.55, stage=stage)


def drip_edge(A, r, x0, x1, y, color, n, layer='over', stage=(.5, .85), lmin=8, lmax=60):
    for x in sorted(r.uniform(x0, x1) for _ in range(n)):
        a = stage[0] + (stage[1] - stage[0]) * r.uniform(0, .5)
        A(layer, 'drip', x=x, y=y, len=r.uniform(lmin, lmax), w=r.uniform(3, 6.5), color=color, stage=(a, a + (stage[1] - stage[0]) * .5))


# ----------------------------------------------------------------------------- abstract tags (no readable text)
def pixo(A, r, x, y, w, h, color, lw=6, layer='wall', stage=None, a=.95, under=PAL['black']):
    """Tall, angular pixo-style marks: leaning bars, hooks, ligatures and a rough underline."""
    n = max(3, int(w / (h * .26)))
    xs = sorted(x + w * (i + r.uniform(-.2, .2)) / n for i in range(n))
    strokes = []
    for i, xx in enumerate(xs):
        hh = h * r.uniform(.62, 1)
        top = y + h - hh
        tilt = r.uniform(-.1, .22) * hh
        bar = [(xx, y + h), (xx + tilt, top)]
        if r.random() < .6:
            bar.append((xx + tilt + r.uniform(8, 24), top + r.uniform(2, 12)))
        strokes.append(bar)
        if i and r.random() < .75:
            yy = y + h - r.uniform(.2, .8) * h
            strokes.append([(xs[i - 1] + r.uniform(-4, 4), yy), (xx + r.uniform(-2, 8), yy + r.uniform(-16, 16))])
    strokes.append([(x - 10, y + h + 6), (x + w * .5, y + h + r.uniform(-4, 8)), (x + w + 16, y + h - r.uniform(2, 16))])
    m = len(strokes)
    for i, s in enumerate(strokes):
        st = None
        if stage:
            d = (stage[1] - stage[0]) / m
            st = (stage[0] + d * i, min(stage[1], stage[0] + d * (i + 1.4)))
        marker(A, s, color, lw, r, layer, st, under, a)


def tag_loop(A, r, x, y, w, h, color, lw=5, layer='wall', stage=None, a=.95, under=PAL['black']):
    """An unreadable hand-style signature: angular zigzags, a loop or two and a long flick."""
    n = r.randint(7, 10)
    pts = []
    for i in range(n):
        px = x + w * i / (n - 1) + r.uniform(-.05, .05) * w
        py = y + h * (0.5 + (0.5 if i % 2 else -0.5) * r.uniform(.4, 1))
        pts.append((px, py))
        if r.random() < .25:
            cx, cy, rad = px, py, h * r.uniform(.12, .22)
            pts += [(cx + rad * math.cos(t), cy + rad * math.sin(t)) for t in [k * .9 for k in range(8)]]
    pts.append((x + w + w * .12, y + h * r.uniform(-.1, .2)))
    marker(A, pts, color, lw, r, layer, stage, under, a, j=2)
    marker(A, [(x + w * .05, y + h * 1.12), (x + w * .5, y + h * 1.0), (x + w * 1.05, y + h * 1.1)], color, lw * .8, r, layer, stage, under, a)


def scrawl(A, r, x, y, w, h, color, lw=6, layer='wall', stage=None, under=PAL['black'], loops=6, a=.95):
    """A fast cursive-style scrawl made of looping strokes (unreadable signature)."""
    per = 22
    n = loops * per
    amp = h / 2
    pts = []
    for i in range(n + 1):
        t = i / per * 2 * math.pi
        b = amp * (0.75 + 0.45 * math.sin(i * .09 + 1.3)) * (1 + r.uniform(-.1, .1))
        pts.append((x + w * i / n - b * .85 * math.sin(t) + r.uniform(-2, 2), y + amp - b * math.cos(t) * 1.1 + r.uniform(-2, 2)))
    pts.append((x + w + w * .06, y + amp * .2))
    marker(A, pts, color, lw, r, layer, stage, under, a, j=.6)


def crown(A, r, x, y, s, color, lw=4, layer='wall', stage=None):
    p = [(x, y), (x + s * .15, y - s * .7), (x + s * .4, y - s * .22), (x + s * .6, y - s * .88), (x + s * .8, y - s * .22), (x + s * 1.05, y - s * .72), (x + s * 1.2, y), (x, y)]
    marker(A, p, color, lw, r, layer, stage)


def cross(A, r, x, y, s, color, lw=4, layer='wall', stage=None):
    marker(A, [(x - s, y - s), (x + s, y + s * 1.05)], color, lw, r, layer, stage, under=None)
    marker(A, [(x + s, y - s), (x - s * .9, y + s)], color, lw, r, layer, stage, under=None)


def spark(A, r, x, y, s, color, layer='wall', stage=None):
    """A crude 4-ray spray spark (no outlined cartoon star)."""
    for ang in (0, 90, 45, 135):
        p = rotate((x - s, y), x, y, ang)
        q = rotate((x + s, y), x, y, ang)
        A(layer, 'line', pts=[p, q], color=color, w=2.6 if ang in (0, 90) else 1.6, a=.95, stage=stage)


# ----------------------------------------------------------------------------- stencil / SVG fragments
def stencil_svg(d, x, y, s, color, uid, spray=True, seed=1, fill_rule='evenodd'):
    """A flat stencil shape with rough edges and overspray (SVG fragment)."""
    r = random.Random(seed)
    dots = ''.join(f'<circle cx="{r.gauss(50, 46):.1f}" cy="{r.gauss(50, 46):.1f}" r="{r.uniform(.5, 1.7):.1f}"/>' for _ in range(70)) if spray else ''
    return (rough_filter(f'st{uid}', 4, '0.05 0.07', seed) + f'<g transform="translate({x},{y}) scale({s})">'
            f'<g fill="{color}" fill-opacity=".7">{dots}</g>'
            f'<path d="{d}" fill="{color}" fill-rule="{fill_rule}" filter="url(#st{uid})"/></g>')


def stencil_hand(x, y, s, color, uid):
    d = 'M' + ' L'.join(f'{px},{py}' for px, py in HAND) + ' Z'
    return stencil_svg(d, x, y, s, color, uid, True, 4)


# ----------------------------------------------------------------------------- hero scene
MAIN = dict(text='MASSARU', cx=606, y=66, h=172, rot=-2.5, track=26, seed=5)
STYLE_MAIN = dict(fill=[PAL['red'], PAL['red'], PAL['magenta'], PAL['magenta'], PAL['red'], PAL['red'], PAL['red']],
                  fw=14, outline=PAL['black'], ow=27, hl=PAL['white'], extrude=(PAL['crimson'], 7, (1.5, 2.0)), rough=5)


def scene_main():
    r = random.Random(7)
    sc = Scene(1200, 420, bg='#17141b')
    A = sc.add
    concrete(A, r, 1200, 420)
    A('wall', 'halo', c=(300, 210), r=420, color=PAL['purple'], a=.45)
    A('wall', 'halo', c=(900, 200), r=420, color=PAL['crimson'], a=.7)
    # torn poster + sprayed colour fields
    paste(A, r, 36, 30, 250, 170, -5, accent=PAL['magenta'])
    color_field(A, r, 560, 228, 520, 138, PAL['crimson'], .96, fl=(5, -2, 9))
    color_field(A, r, 250, 300, 250, 90, PAL['magenta'], .9, .16, fl=(-6, 3, 10))
    color_field(A, r, 1020, 118, 190, 90, PAL['blue'], .88, .16, fl=(5, 4, 8))
    halftone(A, 820, 330, 330, 80, 9, PAL['white'], 'left', a=.55)
    halftone(A, 560, 8, 300, 70, 9, PAL['red'], 'down', a=.8)
    # arrows and tags behind the lettering
    wild_arrow(A, r, 20, 352, 470, 120, -8, PAL['white'], PAL['violet'], fl=(-6, 3, 11))
    wild_arrow(A, r, 1196, 70, 400, 96, 190, PAL['yellow'], PAL['crimson'], fl=(6, 4, 10))
    pixo(A, r, 330, 6, 220, 66, PAL['white'], 4, a=.7)
    pixo(A, r, 880, 330, 250, 70, PAL['yellow'], 5, a=.9)
    tag_loop(A, r, 40, 372, 260, 30, PAL['white'], 3.5, a=.75)
    crown(A, r, 700, 40, 46, PAL['yellow'], 4)
    cross(A, r, 1140, 250, 12, PAL['white'], 4)
    cross(A, r, 76, 244, 10, PAL['yellow'], 3.5)
    tape(A, r, 1040, 8, 70, 18, 22)
    A('wall', 'dots', dots=cloud(250, 320, 150, 240, r, 1.6), color=PAL['pink'], a=.7)
    A('wall', 'dots', dots=cloud(960, 300, 140, 200, r, 1.6), color=PAL['red'], a=.8)
    # first marks (chalk-like ticks + overspray) painted before the letters
    m = MAIN
    s = m['h'] / 100
    lay, wu = layout(m['text'], m['track'], m['seed'])
    x0 = m['cx'] - wu * s / 2
    for i, g in enumerate(lay):
        gx = x0 + (g['x0'] + g['w'] / 2) * s
        st = (0.0 + i * .012, 0.05 + i * .012)
        A('spray', 'line', pts=[(gx - 16, m['y'] - 14), (gx + 16, m['y'] - 20)], color=PAL['yellow'], w=3.5, a=.95, stage=st)
        A('spray', 'dots', dots=cloud(gx, m['y'] + m['h'] / 2, 80, 60, r, 1.5), color=PAL['white'], a=.75, stage=(0.02 + i * .012, 0.12))
    A('spray', 'dots', dots=speckle(m['text'], m['cx'], m['y'], m['h'], 260, 16, r, m['rot'], m['track'], m['seed']), color=PAL['red'], a=.75, stage=(.2, .5))
    # details painted last
    for pts, col, w in [([(210, 322), (500, 312), (860, 326)], PAL['white'], 7), ([(236, 334), (520, 326), (900, 338)], PAL['red'], 5)]:
        marker(A, pts, col, w, r, 'over', STAGES['details'], under=None, a=.95, j=2.2)
    spark(A, r, 176, 150, 14, PAL['yellow'], 'over', (0.82, 0.92))
    spark(A, r, 1062, 142, 12, PAL['white'], 'over', (0.84, 0.93))
    for d in make_drips(m['text'], m['cx'], m['y'], m['h'], STYLE_MAIN['fill'], r, m['track'], m['rot'], STYLE_MAIN['ow'], seed=m['seed']):
        A('over', 'drip', **{k: v for k, v in d.items() if k != 't'})
    drip_edge(A, r, 300, 880, 360, PAL['red'], 7, 'over', (.7, .9), 6, 34)
    return sc
