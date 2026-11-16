"""generate-dividers.py - gera assets/dividers/*.svg (fundo transparente, legíveis no tema claro e escuro do GitHub).
Todos em estilo de rua: traço de spray, lambe-lambe rasgado, rabisco/pichação, tinta escorrendo, setas wildstyle, fita de alerta e marcas de tag.
Rodar:  python3 tools/generate-dividers.py
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from street import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def write(rel, svg):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(svg)
    print('wrote', rel, f'{len(svg) / 1024:.1f} KB')


def spray_stroke():
    T, r = 9, random.Random(5)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    pts = [(40 + i * 1120 / 40, 40 + math.sin(i * .5) * 8 + r.uniform(-2, 2)) for i in range(41)]
    marker(A, pts, PAL['red'], 12, r, 'over', (.04, .44), j=2.5, hi=PAL['pink'])
    marker(A, [(x + 6, y + 12) for x, y in pts[::2]], PAL['magenta'], 5, r, 'over', (.12, .5), under=None, j=3)
    overspray(A, r, pts, PAL['red'], 320, 11, 'over', .8, (.1, .5))
    for x in (200, 410, 560, 790, 980, 1090):
        a = .5 + r.random() * .2
        A('over', 'drip', x=x, y=50, len=r.uniform(10, 36), w=r.uniform(3.5, 6.5), color=PAL['red'], stage=(a, a + .18))
    cross(A, r, 1160, 24, 8, PAL['yellow'], 3.5, 'over', (.8, .88))
    spark(A, r, 36, 70, 9, PAL['yellow'], 'over', (.82, .9))
    return compose_scene(sc, 'd1', T, True, title='Divisor de spray', desc='Traço de spray vermelho com respingos e tinta escorrendo.')


def torn_paper():
    r = random.Random(8)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    paste(A, r, 20, 14, 1160, 62, -.6, accent=PAL['red'])
    for x in (330, 640, 950):
        A('wall', 'poly', pts=[(x, 24), (x + 90, 20), (x + 96, 66), (x + 4, 70)], fill=PAL['black'], a=.55)
    pixo(A, r, 760, 24, 260, 40, PAL['red'], 4, a=.95, under=None)
    return compose_scene(sc, 'd2', 1, False, title='Divisor de lambe-lambe', desc='Faixa de lambe-lambe rasgado com meio-tom, tinta preta e vermelha e fita.')


def scribble_loops():
    T, r = 10, random.Random(13)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    scrawl(A, r, 40, 22, 1100, 44, PAL['yellow'], 5, 'over', (.04, .6), PAL['black'], 9)
    marker(A, zigzag(120, 78, 960, 6, 30), PAL['blue'], 3.5, r, 'over', (.3, .7), under=None)
    cross(A, r, 1160, 20, 8, PAL['red'], 4, 'over', (.7, .78))
    return compose_scene(sc, 'd3', T, True, title='Divisor de rabisco', desc='Rabisco cursivo amarelo com laços e um zigue-zague azul.')


def drip_bar():
    T, r = 9, random.Random(17)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    top = [(x, 14 + r.uniform(-2.5, 2.5)) for x in range(10, 1191, 12)]
    bot = [(x, 30 + r.uniform(-2.5, 2.5)) for x in range(1190, 9, -12)]
    A('over', 'poly', pts=top + bot, fill=PAL['red'], a=1, stroke=PAL['black'], sw=3, stage=(.02, .2))
    overspray(A, r, [(10, 22), (1190, 22)], PAL['red'], 260, 10, 'over', .7, (.1, .3))
    for x in sorted(r.sample(range(40, 1170, 18), 30)):
        a = .25 + r.random() * .4
        A('over', 'drip', x=x, y=28, len=r.choice([8, 12, 18, 26, 34, 46]), w=r.uniform(3.5, 6.5), color=PAL['red'], stage=(a, a + .25))
    return compose_scene(sc, 'd4', T, True, title='Divisor de tinta escorrendo', desc='Barra de tinta vermelha com gotas escorrendo e respingos.')


def arrows():
    r = random.Random(21)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    wild_arrow(A, r, 10, 50, 520, 56, -4, PAL['white'], PAL['violet'])
    wild_arrow(A, r, 1190, 40, 520, 56, 184, PAL['red'], PAL['crimson'])
    wild_arrow(A, r, 380, 70, 440, 40, -2, PAL['magenta'], PAL['black'])
    spark(A, r, 600, 24, 11, PAL['yellow'])
    cross(A, r, 120, 16, 7, PAL['yellow'], 3.5)
    return compose_scene(sc, 'd5', 1, False, title='Divisor de setas wildstyle', desc='Setas angulares entrelaçadas com bloco 3D e contorno preto.')


def hazard_tape():
    r = random.Random(25)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    cx, cy, ang = 600, 45, -1.4
    R = lambda p: rotate(p, cx, cy, ang)
    y0, y1 = 30, 62
    A('wall', 'poly', pts=[R((-10, y0)), R((1210, y0)), R((1210, y1)), R((-10, y1))], fill=PAL['yellow'], a=1, stroke=PAL['black'], sw=3.5)
    x = -30
    while x < 1220:
        A('wall', 'poly', pts=[R((x, y0)), R((x + 24, y0)), R((x + 6, y1)), R((x - 18, y1))], fill=PAL['black'], a=1)
        x += 52
    A('wall', 'dots', dots=cloud(300, 46, 380, 160, r, 1.8), color=PAL['red'], a=.85)
    A('wall', 'dots', dots=cloud(900, 46, 380, 160, r, 1.8), color=PAL['magenta'], a=.85)
    return compose_scene(sc, 'd6', 1, False, title='Divisor de fita de alerta', desc='Fita de alerta amarela e preta com respingos vermelhos e magenta.')


def tag_marks():
    T, r = 10, random.Random(29)
    sc = Scene(1200, 90, bg=False)
    A = sc.add
    marker(A, [(60, 46), (300, 42), (560, 48)], PAL['white'], 3, r, 'over', (.02, .3), j=2)
    marker(A, [(1140, 46), (900, 50), (660, 44)], PAL['white'], 3, r, 'over', (.02, .3), j=2)
    crown(A, r, 580, 58, 40, PAL['yellow'], 4, 'over', (.3, .45))
    for i, (x, y) in enumerate([(190, 22), (330, 68), (470, 24), (730, 68), (870, 22), (1010, 66)]):
        st = (.45 + i * .05, .6 + i * .05)
        (cross if i % 2 else spark)(A, r, x, y, 9, PAL['magenta'] if i % 2 else PAL['yellow'], *(('over', st) if i % 2 == 0 else (4, 'over', st))) if False else None
        if i % 2:
            cross(A, r, x, y, 9, PAL['magenta'], 4, 'over', st)
        else:
            spark(A, r, x, y, 11, PAL['yellow'], 'over', st)
    pixo(A, r, 20, 40, 120, 40, PAL['red'], 3.5, 'over', (.5, .8))
    return compose_scene(sc, 'd7', T, True, title='Divisor de marcas de tag', desc='Linhas de giz com uma coroa amarela e pequenas marcas de rua.')


if __name__ == '__main__':
    write('assets/dividers/divider-01-spray-stroke.svg', spray_stroke())
    write('assets/dividers/divider-02-torn-paper.svg', torn_paper())
    write('assets/dividers/divider-03-scribble-loops.svg', scribble_loops())
    write('assets/dividers/divider-04-drip-bar.svg', drip_bar())
    write('assets/dividers/divider-05-shards.svg', arrows())
    write('assets/dividers/divider-06-hazard-tape.svg', hazard_tape())
    write('assets/dividers/divider-07-tag-stars.svg', tag_marks())
