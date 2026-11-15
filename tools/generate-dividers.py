"""generate-dividers.py - builds assets/dividers/*.svg (transparent backgrounds, readable on light and dark GitHub themes).
Run:  python3 tools/generate-dividers.py
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graffiti import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def write(rel, svg):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(svg)
    print('wrote', rel, f'{len(svg) / 1024:.1f} KB')


def drip_items(A, xs, y, col, st0, st1, r, wmax=7, lmax=34):
    for x in xs:
        a = st0 + (st1 - st0) * r.uniform(0, .5)
        A('over', 'drip', x=x, y=y, len=r.uniform(10, lmax), w=r.uniform(3.5, wmax), color=col, stage=(a, a + (st1 - st0) * .5))


def spray_stroke():
    T, r = 9, random.Random(5)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    pts = [(40 + i * 1120 / 70, 38 + math.sin(i * .3) * 9 + r.uniform(-1.5, 1.5)) for i in range(71)]
    A('over', 'line', pts=[(x + 3, y + 5) for x, y in pts], color=PAL['black'], w=17, a=.9, stage=(.04, .44))
    A('over', 'line', pts=pts, color=PAL['red'], w=13, a=1, stage=(.04, .44))
    A('over', 'line', pts=[(x, y - 3) for x, y in pts], color=PAL['pink'], w=3, a=.8, stage=(.08, .48))
    A('over', 'line', pts=[(x + 18, y + 14) for x, y in pts[::2]], color=PAL['blue'], w=3, a=.9, stage=(.12, .5))
    for cx in range(80, 1160, 140):
        A('over', 'dots', dots=cloud(cx, 40, 42, 26, r, 1.6), color=PAL['red'], a=.85, stage=(.1 + cx / 1200 * .35, .5))
    drip_items(A, [200, 410, 560, 790, 980, 1090], 48, PAL['red'], .5, .8, r)
    A('over', 'poly', pts=star(1160, 22, 11, 3, 4, 0), fill=PAL['yellow'], a=1, stage=(.82, .9))
    A('over', 'poly', pts=star(40, 66, 9, 2.5, 4, 0), fill=PAL['yellow'], a=1, stage=(.84, .92))
    return compose_scene(sc, 'd1', T, True, title='Divisor de spray', desc='Traço vermelho de spray com tinta escorrendo.')


def torn_paper():
    r = random.Random(8)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    def band(y0, y1, j):
        top = [(x, y0 + r.uniform(-j, j)) for x in range(0, 1201, 14)]
        bot = [(x, y1 + r.uniform(-j, j)) for x in range(1200, -1, -14)]
        return top + bot
    A('wall', 'poly', pts=band(34, 70, 5), fill=PAL['magenta'], a=1, stroke=PAL['black'], sw=3)
    A('wall', 'poly', pts=band(24, 58, 6), fill=PAL['white'], a=1, stroke=PAL['black'], sw=3)
    A('wall', 'poly', pts=band(34, 50, 4), fill=PAL['crimson'], a=.9)
    A('wall', 'line', pts=zigzag(60, 42, 300, 5, 18), color=PAL['yellow'], w=3, a=.95)
    A('wall', 'line', pts=scribble(820, 42, 300, 12, r, 40), color=PAL['black'], w=2.5, a=.9)
    A('wall', 'dots', dots=cloud(600, 52, 400, 140, r, 1.6), color=PAL['red'], a=.8)
    A('wall', 'poly', pts=star(600, 42, 14, 5, 4, 0), fill=PAL['yellow'], a=1, stroke=PAL['black'], sw=2)
    return compose_scene(sc, 'd2', 1, False, title='Divisor de papel rasgado', desc='Faixa de papel branco rasgado sobre magenta com respingos vermelhos.')


def scribble_loops():
    T, r = 10, random.Random(13)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    A('over', 'line', pts=scribble(40, 44, 1120, 52, r, 130), color=PAL['black'], w=7, a=.9, stage=(.04, .55))
    A('over', 'line', pts=scribble(40, 44, 1120, 52, r, 130), color=PAL['yellow'], w=4, a=1, stage=(.04, .55))
    A('over', 'line', pts=zigzag(120, 74, 960, 7, 40), color=PAL['blue'], w=3.5, a=.95, stage=(.2, .65))
    for i, x in enumerate((100, 330, 600, 880, 1100)):
        A('over', 'poly', pts=star(x, 18 if i % 2 else 72, 12, 3, 4, 0), fill=PAL['magenta'] if i % 2 else PAL['red'], a=1, stroke=PAL['black'], sw=2, stage=(.6 + i * .05, .8 + i * .03))
    return compose_scene(sc, 'd3', T, True, title='Divisor de rabisco', desc='Rabisco amarelo desenhado à mão com zigue-zague azul e estrelas.')


def drip_bar():
    T, r = 9, random.Random(17)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    top = [(x, 14 + r.uniform(-2.5, 2.5)) for x in range(10, 1191, 12)]
    bot = [(x, 30 + r.uniform(-2.5, 2.5)) for x in range(1190, 9, -12)]
    A('over', 'poly', pts=top + bot, fill=PAL['red'], a=1, stroke=PAL['black'], sw=3, stage=(.02, .2))
    A('over', 'line', pts=[(x, 17) for x in range(30, 1180, 12)], color=PAL['pink'], w=2.5, a=.8, stage=(.1, .3))
    xs = sorted(r.sample(range(40, 1170, 18), 30))
    for x in xs:
        a = .25 + r.random() * .4
        A('over', 'drip', x=x, y=28, len=r.choice([8, 12, 18, 26, 34, 46]), w=r.uniform(3.5, 6.5), color=PAL['red'], stage=(a, a + .25))
    A('over', 'dots', dots=cloud(600, 40, 600, 160, r, 1.5), color=PAL['crimson'], a=.7, stage=(.3, .6))
    return compose_scene(sc, 'd4', T, True, title='Divisor de tinta escorrendo', desc='Barra de tinta vermelha com gotas escorrendo.')


def shards():
    r = random.Random(21)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    A('wall', 'poly', pts=jit([(0, 70), (300, 20), (420, 76), (0, 86)], r, 1.5), fill=PAL['purple'], a=1, stroke=PAL['black'], sw=3, fl=(6, 0, 9))
    A('wall', 'poly', pts=jit(arrow(220, 56, 520, 52, -4), r), fill=PAL['magenta'], a=1, stroke=PAL['black'], sw=3, fl=(-6, 2, 8))
    A('wall', 'poly', pts=jit([(1200, 20), (860, 70), (700, 24), (1200, 6)], r, 1.5), fill=PAL['crimson'], a=1, stroke=PAL['black'], sw=3, fl=(5, 1, 10))
    A('wall', 'poly', pts=jit(arrow(1010, 36, 360, 40, 184), r), fill=PAL['red'], a=1, stroke=PAL['black'], sw=3)
    A('wall', 'line', pts=zigzag(420, 70, 360, 9, 16), color=PAL['yellow'], w=4, a=1)
    A('wall', 'poly', pts=star(600, 30, 15, 6, 6, 0), fill=PAL['yellow'], a=1, stroke=PAL['black'], sw=2.5)
    A('wall', 'poly', pts=jit(blob(120, 40, 26, 20, 12, r), r, 1), fill=PAL['blue'], a=1, stroke=PAL['black'], sw=3)
    A('wall', 'dots', dots=cloud(780, 44, 200, 110, r, 1.5), color=PAL['pink'], a=.9)
    return compose_scene(sc, 'd5', 1, False, title='Divisor de estilhaços', desc='Estilhaços de graffiti roxos, magenta e vermelhos sobrepostos.')


def hazard_tape():
    r = random.Random(25)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    cx, cy, ang = 600, 45, -1.4
    def R(p):
        return rotate(p, cx, cy, ang)
    y0, y1 = 30, 62
    A('wall', 'poly', pts=[R((-10, y0)), R((1210, y0)), R((1210, y1)), R((-10, y1))], fill=PAL['yellow'], a=1, stroke=PAL['black'], sw=3.5)
    x = -30
    while x < 1220:
        A('wall', 'poly', pts=[R((x, y0)), R((x + 24, y0)), R((x + 6, y1)), R((x - 18, y1))], fill=PAL['black'], a=1)
        x += 52
    A('wall', 'dots', dots=cloud(300, 46, 380, 160, r, 1.8), color=PAL['red'], a=.85)
    A('wall', 'dots', dots=cloud(900, 46, 380, 160, r, 1.8), color=PAL['magenta'], a=.85)
    return compose_scene(sc, 'd6', 1, False, title='Divisor de fita de alerta', desc='Fita de alerta amarela e preta com respingos vermelhos e magenta.')


def tag_stars():
    T, r = 10, random.Random(29)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    A('over', 'line', pts=[(60, 46), (540, 46)], color=PAL['black'], w=5, a=.9, stage=(.02, .3))
    A('over', 'line', pts=[(60, 46), (540, 46)], color=PAL['white'], w=2.5, a=1, stage=(.02, .3))
    A('over', 'line', pts=[(1140, 46), (660, 46)], color=PAL['black'], w=5, a=.9, stage=(.02, .3))
    A('over', 'line', pts=[(1140, 46), (660, 46)], color=PAL['white'], w=2.5, a=1, stage=(.02, .3))
    A('over', 'poly', pts=star(600, 46, 30, 12, 8, 0), fill=PAL['yellow'], a=1, stroke=PAL['black'], sw=4, stage=(.3, .5))
    for i, (x, y) in enumerate([(190, 22), (330, 70), (470, 24), (730, 70), (870, 22), (1010, 68)]):
        st = (.45 + i * .05, .6 + i * .05)
        if i % 3 == 0:
            A('over', 'poly', pts=star(x, y, 11, 3, 4, 0), fill=PAL['red'], a=1, stroke=PAL['black'], sw=2, stage=st)
        elif i % 3 == 1:
            A('over', 'line', pts=[(x - 9, y - 9), (x + 9, y + 9)], color=PAL['magenta'], w=5, a=1, stage=st)
            A('over', 'line', pts=[(x + 9, y - 9), (x - 9, y + 9)], color=PAL['magenta'], w=5, a=1, stage=st)
        else:
            A('over', 'circle', c=(x, y), r=8, fill=PAL['blue'], a=1, stroke=PAL['black'], sw=3, stage=st)
    for ln in web(30, 90, 58, -88, -2):
        A('over', 'line', pts=ln, color=PAL['white'], w=1.5, a=.8, stage=(.6, .8))
    return compose_scene(sc, 'd7', T, True, title='Divisor de estrelas', desc='Linha de giz com uma estrela amarela e pequenas marcas desenhadas à mão.')


if __name__ == '__main__':
    write('assets/dividers/divider-01-spray-stroke.svg', spray_stroke())
    write('assets/dividers/divider-02-torn-paper.svg', torn_paper())
    write('assets/dividers/divider-03-scribble-loops.svg', scribble_loops())
    write('assets/dividers/divider-04-drip-bar.svg', drip_bar())
    write('assets/dividers/divider-05-shards.svg', shards())
    write('assets/dividers/divider-06-hazard-tape.svg', hazard_tape())
    write('assets/dividers/divider-07-tag-stars.svg', tag_stars())
