"""generate-banners.py - gera assets/banners/*.svg e assets/headers/*.svg.

  banner-01  MASSARU (arte final estática; a animação de pintura é o GIF em assets/animations/)
  banner-02  SOBRE MIM          banner-03  HABILIDADES          banner-04  Instagram + Twitch
  art-01..03 painéis de pichação / wildstyle / tag SEM texto (arte pura de rua)
  headers    INFO PESSOAL, INTERESSES DEV e a assinatura final

Os banners 02-04, os painéis e os cabeçalhos se pintam sozinhos em loop (SMIL).
Rodar:  python3 tools/generate-banners.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from street import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BG = '#17141b'


def write(rel, svg):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote', rel, f'{len(svg) / 1024:.1f} KB')


def compose(sc, uid, T, animate, letters, extra_over='', title='', desc='', pre_letters=''):
    return compose_scene(sc, uid, T, animate, letters, extra_over, title, desc, pre_letters)


def add_drips(A, r, text, cx, y, h, fills, track, rot, ow, seed, chance=.75):
    for d in make_drips(text, cx, y, h, fills, r, track, rot, ow, chance=chance, seed=seed):
        A('over', 'drip', **{k: v for k, v in d.items() if k != 't'})


def add_spray(A, r, text, cx, y, h, color, track, rot, seed, n=220):
    A('spray', 'dots', dots=speckle(text, cx, y, h, n, 14, r, rot, track, seed), color=color, a=.8, stage=(.02, .3))


def code_marks(A, r, x, y, s, color, layer='wall', stage=None):
    """{ } and </> drawn as rough spray strokes."""
    marker(A, [(x + 12 * s, y), (x + 3 * s, y), (x + 3 * s, y + 20 * s), (x - 6 * s, y + 30 * s), (x + 3 * s, y + 40 * s), (x + 3 * s, y + 60 * s), (x + 12 * s, y + 60 * s)], color, 4, r, layer, stage)
    marker(A, [(x + 36 * s, y + 8 * s), (x + 20 * s, y + 30 * s), (x + 36 * s, y + 52 * s)], color, 4, r, layer, stage)
    marker(A, [(x + 70 * s, y + 8 * s), (x + 54 * s, y + 56 * s)], color, 4, r, layer, stage)
    marker(A, [(x + 86 * s, y + 8 * s), (x + 102 * s, y + 30 * s), (x + 86 * s, y + 52 * s)], color, 4, r, layer, stage)


# ----------------------------------------------------------------------------- banner 01
def banner01():
    sc = scene_main()
    m = MAIN
    letters = letters_svg(m['text'], m['cx'], m['y'], m['h'], STYLE_MAIN, False, rot=m['rot'], track=m['track'], seed=m['seed'])
    return compose(sc, 'b1', 14, False, letters, title='MASSARU', desc='MASSARU em graffiti de rua: letras vermelhas tortas com bloco 3D, tinta escorrendo, lambe-lambe rasgado, setas e pichação numa parede de concreto.')


# ----------------------------------------------------------------------------- banner 02 - SOBRE MIM
def banner02():
    T, r = 12, random.Random(21)
    sc = Scene(1200, 300, bg=BG)
    A = sc.add
    concrete(A, r, 1200, 300)
    A('wall', 'halo', c=(200, 150), r=360, color=PAL['purple'], a=.55)
    color_field(A, r, 620, 150, 590, 128, PAL['magenta'], .97, .1, fl=(5, -2, 10))
    color_field(A, r, 1000, 236, 250, 76, PAL['crimson'], .92, .14)
    color_field(A, r, 230, 70, 210, 60, PAL['pink'], .8, .14)
    halftone(A, 700, 212, 420, 74, 9, PAL['white'], 'left', a=.4)
    halftone(A, 300, 4, 420, 60, 9, PAL['purple'], 'down', a=.75)
    paste(A, r, 1010, 30, 150, 112, 6, accent=PAL['yellow'])
    wild_arrow(A, r, 520, 266, 340, 64, -4, PAL['blue'], PAL['violet'], fl=(-6, 3, 10))
    pixo(A, r, 900, 206, 230, 58, PAL['white'], 4, a=.85)
    tag_loop(A, r, 40, 262, 240, 22, PAL['yellow'], 4, a=.9)
    cross(A, r, 1160, 160, 10, PAL['white'], 4)
    crown(A, r, 210, 34, 40, PAL['yellow'], 4)
    A('wall', 'dots', dots=cloud(420, 90, 200, 280, r, 1.6), color=PAL['blue'], a=.8)
    A('wall', 'dots', dots=cloud(880, 150, 180, 240, r, 1.6), color=PAL['purple'], a=.8)
    text, cx = 'SOBRE MIM', 640
    h = min(fit(text, 700, 26), 150)
    y = 46
    st = dict(fill=[PAL['yellow']], fw=14, outline=PAL['blue'], ow=27, hl=None, extrude=(PAL['black'], 5, (1.4, 1.8)), rough=5)
    add_spray(A, r, text, cx, y, h, PAL['yellow'], 26, -2, 3)
    add_drips(A, r, text, cx, y, h, [PAL['yellow']], 26, -2, 27, 3)
    drip_edge(A, r, 80, 1100, 20, PAL['magenta'], 10, 'over', (.7, .9), 6, 30)
    letters = letters_svg(text, cx, y, h, st, True, T, -2, 26, 3)
    tag = plain_svg('OI, TUDO BEM? PRAZER!', 640, 238, 24, PAL['white'], 3.2, animate=True, T=T, t0=.55, t1=.9, shadow=PAL['black'])
    art = reveal(stencil_hand(30, 58, 1.4, PAL['white'], 'h2'), (0.0, .12), T)
    return compose(sc, 'b2', T, True, letters, tag + art, 'Sobre mim',
                   'SOBRE MIM em letras de rua amarelas com contorno azul sobre um fundo magenta, com uma mão em estêncil e pichações.')


# ----------------------------------------------------------------------------- banner 03 - HABILIDADES
def banner03():
    T, r = 12, random.Random(33)
    sc = Scene(1200, 300, bg=BG)
    A = sc.add
    concrete(A, r, 1200, 300)
    A('wall', 'halo', c=(300, 140), r=360, color=PAL['blue'], a=.5)
    A('wall', 'halo', c=(950, 160), r=340, color=PAL['purple'], a=.6)
    color_field(A, r, 600, 150, 590, 128, PAL['violet'], .97, .11, fl=(-5, 3, 9))
    color_field(A, r, 190, 150, 190, 110, PAL['blue'], .9, .14)
    color_field(A, r, 1040, 100, 200, 90, PAL['magenta'], .85, .14)
    for pts, c in pixels(520, 4, 14, 4, 16, [PAL['purple'], PAL['blue'], PAL['black'], PAL['violet']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.9)
    for pts, c in pixels(960, 244, 10, 3, 14, [PAL['red'], PAL['crimson'], PAL['black']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.9)
    halftone(A, 680, 210, 440, 80, 9, PAL['cyan'], 'left', a=.5)
    wild_arrow(A, r, 1196, 250, 380, 72, 184, PAL['white'], PAL['crimson'], fl=(6, -3, 10))
    wild_arrow(A, r, 10, 52, 300, 62, 6, PAL['cyan'], PAL['violet'], fl=(-5, 3, 11))
    pixo(A, r, 40, 218, 220, 56, PAL['white'], 4, a=.8)
    code_marks(A, r, 80, 100, 1.0, PAL['yellow'])
    code_marks(A, r, 1030, 196, .6, PAL['white'])
    cross(A, r, 1150, 40, 10, PAL['white'], 4)
    A('wall', 'dots', dots=cloud(320, 150, 200, 260, r, 1.6), color=PAL['cyan'], a=.75)
    A('wall', 'dots', dots=cloud(900, 120, 180, 220, r, 1.6), color=PAL['pink'], a=.75)
    text, cx = 'HABILIDADES', 620
    h = min(fit(text, 800, 26), 140)
    y = 44
    st = dict(fill=[PAL['white']], fw=14, outline=PAL['black'], ow=27, hl=PAL['cyan'], extrude=(PAL['violet'], 6, (1.5, 1.9)), rough=5)
    add_spray(A, r, text, cx, y, h, PAL['cyan'], 26, 1.5, 4)
    add_drips(A, r, text, cx, y, h, [PAL['white'], PAL['cyan']], 26, 1.5, 27, 4, .6)
    letters = letters_svg(text, cx, y, h, st, True, T, 1.5, 26, 4)
    tag = plain_svg('COM O QUE EU TRABALHO', 620, 232, 24, PAL['yellow'], 3.2, animate=True, T=T, t0=.55, t1=.9, shadow=PAL['black'])
    return compose(sc, 'b3', T, True, letters, tag, 'Habilidades',
                   'HABILIDADES em letras de rua brancas sobre campos azul e roxo, com setas wildstyle, meio-tom e marcas de código.')


# ----------------------------------------------------------------------------- banner 04 - Instagram + Twitch
IG = ('M28,0 H72 A28,28 0 0 1 100,28 V72 A28,28 0 0 1 72,100 H28 A28,28 0 0 1 0,72 V28 A28,28 0 0 1 28,0 Z '
      'M30,12 H70 A18,18 0 0 1 88,30 V70 A18,18 0 0 1 70,88 H30 A18,18 0 0 1 12,70 V30 A18,18 0 0 1 30,12 Z '
      'M24,50 A26,26 0 1 0 76,50 A26,26 0 1 0 24,50 Z M36,50 A14,14 0 1 0 64,50 A14,14 0 1 0 36,50 Z '
      'M66,28 A6,6 0 1 0 78,28 A6,6 0 1 0 66,28 Z')
TWITCH = 'M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.43l-3 3v-3H6.857V1.714h13.714Z'


def banner04():
    T, r = 12, random.Random(44)
    sc = Scene(1200, 340, bg=BG)
    A = sc.add
    concrete(A, r, 1200, 340)
    A('wall', 'halo', c=(200, 170), r=360, color=PAL['red'], a=.55)
    A('wall', 'halo', c=(900, 170), r=380, color=PAL['magenta'], a=.4)
    color_field(A, r, 700, 170, 530, 150, PAL['crimson'], .97, .1, fl=(5, 3, 10))
    color_field(A, r, 180, 170, 175, 150, PAL['magenta'], .92, .12)
    color_field(A, r, 1090, 260, 170, 80, PAL['purple'], .9, .14)
    halftone(A, 500, 270, 520, 64, 9, PAL['white'], 'left', a=.4)
    halftone(A, 460, 4, 400, 56, 9, PAL['red'], 'down', a=.8)
    wild_arrow(A, r, 1196, 60, 330, 64, 186, PAL['yellow'], PAL['crimson'], fl=(6, 3, 10))
    pixo(A, r, 940, 250, 220, 56, PAL['white'], 4, a=.85)
    tag_loop(A, r, 330, 300, 260, 22, PAL['yellow'], 4, a=.9)
    paste(A, r, 1040, 120, 120, 96, -7, accent=PAL['magenta'])
    cross(A, r, 330, 36, 10, PAL['white'], 4)
    crown(A, r, 1000, 40, 36, PAL['yellow'], 4)
    text, cx = 'ME SIGA', 700
    h, y = 112, 34
    st = dict(fill=[PAL['pink']], fw=14, outline=PAL['black'], ow=27, hl=PAL['white'], extrude=(PAL['purple'], 6, (1.5, 1.9)), rough=5)
    add_spray(A, r, text, cx, y, h, PAL['magenta'], 26, -2, 6, 180)
    add_drips(A, r, text, cx, y, h, [PAL['pink'], PAL['magenta']], 26, -2, 27, 6, .7)
    letters = letters_svg(text, cx, y, h, st, True, T, -2, 26, 6)
    l2 = plain_svg('NO INSTAGRAM E NA TWITCH', 700, 176, 30, PAL['white'], 3.6, animate=True, T=T, t0=.4, t1=.7, shadow=PAL['black'])
    l3 = plain_svg('ACOMPANHE MINHAS LIVES ESQUISITAS', 700, 226, 24, PAL['yellow'], 3.2, animate=True, T=T, t0=.55, t1=.85, shadow=PAL['black'])
    l4 = plain_svg('@MASSDVV_  \u2022  @MASSADV_', 700, 274, 22, PAL['pink'], 3.0, animate=True, T=T, t0=.62, t1=.92, shadow=PAL['black'])
    art = (reveal(stencil_svg(IG, 54, 48, 1.15, PAL['white'], 'ig', True, 5), (0.0, .12), T) +
           reveal(stencil_svg(TWITCH, 66, 188, 4.3, PAL['white'], 'tw', True, 6, 'nonzero'), (0.04, .16), T))
    return compose(sc, 'b4', T, True, letters, l2 + l3 + l4 + art, 'Instagram e Twitch',
                   'ME SIGA NO INSTAGRAM E NA TWITCH, acompanhe minhas lives esquisitas, com ícones em estêncil e os perfis @massdvv_ e @massadv_.')


# ----------------------------------------------------------------------------- text-free street panels
def art01():
    T, r = 12, random.Random(51)
    sc = Scene(1200, 240, bg=BG)
    A = sc.add
    concrete(A, r, 1200, 240)
    A('wall', 'halo', c=(400, 120), r=380, color=PAL['crimson'], a=.6)
    A('wall', 'halo', c=(900, 120), r=340, color=PAL['purple'], a=.4)
    color_field(A, r, 330, 130, 250, 80, PAL['red'], .9, .15, fl=(4, -2, 9))
    color_field(A, r, 920, 110, 220, 70, PAL['violet'], .9, .15)
    pixo(A, r, 70, 40, 330, 150, PAL['white'], 8, 'over', (.04, .4))
    pixo(A, r, 470, 52, 260, 130, PAL['yellow'], 7, 'over', (.22, .55))
    pixo(A, r, 800, 36, 340, 160, PAL['white'], 8, 'over', (.4, .75))
    tag_loop(A, r, 440, 196, 280, 26, PAL['red'], 5, 'over', (.5, .78))
    crown(A, r, 120, 34, 50, PAL['yellow'], 5, 'over', (.7, .8))
    cross(A, r, 1130, 200, 12, PAL['white'], 5, 'over', (.76, .84))
    drip_edge(A, r, 70, 1140, 205, PAL['red'], 14, 'over', (.7, .92), 8, 28)
    return compose(sc, 'a1', T, True, '', title='Pichação', desc='Painel de pichação abstrata sem texto: barras altas e inclinadas em branco, amarelo e vermelho sobre concreto.')


def art02():
    T, r = 12, random.Random(52)
    sc = Scene(1200, 240, bg='#d9d2c3')   # cream wall, like the wildstyle reference
    A = sc.add
    A('wall', 'halo', c=(300, 100), r=300, color=PAL['blue'], a=.25)
    A('wall', 'halo', c=(900, 140), r=300, color=PAL['red'], a=.22)
    halftone(A, 30, 20, 300, 80, 9, PAL['blue'], 'right', a=.4)
    shards = [([(80, 150), (230, 40), (300, 120), (200, 190)], PAL['blue']), ([(300, 120), (470, 30), (540, 110), (420, 170)], PAL['white']),
              ([(520, 160), (700, 50), (760, 140), (620, 200)], PAL['red']), ([(740, 60), (930, 30), (960, 120), (800, 150)], PAL['yellow']),
              ([(900, 170), (1060, 70), (1140, 140), (1040, 210)], PAL['purple'])]
    for i, (pts, col) in enumerate(shards):
        st = (.05 + i * .1, .2 + i * .1)
        for k in range(6, 0, -1):
            A('over', 'poly', pts=[(x + 2.2 * k, y + 2.6 * k) for x, y in jit(pts, r, 1.5, 2)] if k == 6 else [(x + 2.2 * k, y + 2.6 * k) for x, y in pts], fill=PAL['black'] if k > 4 else '#2a1a40', a=1, stage=st)
        A('over', 'poly', pts=jit(pts, r, 1.4, 2), fill=col, a=1, stroke=PAL['black'], sw=4.5, stage=st)
    wild_arrow(A, r, 40, 190, 420, 70, -18, PAL['white'], PAL['blue'], 'over', None, (.5, .6))
    wild_arrow(A, r, 1180, 60, 380, 70, 198, PAL['red'], PAL['violet'], 'over', None, (.58, .68))
    wild_arrow(A, r, 400, 214, 380, 60, -10, PAL['blue'], PAL['black'], 'over', None, (.66, .76))
    spark(A, r, 640, 30, 16, PAL['black'], 'over', (.8, .86))
    cross(A, r, 1160, 200, 11, PAL['black'], 4, 'over', (.82, .9))
    drip_edge(A, r, 100, 1100, 214, PAL['red'], 9, 'over', (.76, .94), 6, 20)
    return compose(sc, 'a2', T, True, '', title='Wildstyle', desc='Painel wildstyle sem texto: estilhaços angulares e setas entrelaçadas com bloco 3D e contorno preto em azul, branco, vermelho, amarelo e roxo.')


def art03():
    T, r = 12, random.Random(53)
    sc = Scene(1200, 240, bg=BG)
    A = sc.add
    concrete(A, r, 1200, 240)
    color_field(A, r, 600, 120, 600, 150, PAL['magenta'], 1, .08, 30, 'wall', None, 200)
    A('wall', 'halo', c=(300, 120), r=300, color=PAL['pink'], a=.5)
    halftone(A, 20, 10, 500, 70, 9, PAL['purple'], 'down', a=.6)
    halftone(A, 700, 160, 480, 70, 9, PAL['violet'], 'left', a=.6)
    A('wall', 'dots', dots=cloud(250, 140, 260, 380, r, 2.2), color=PAL['blue'], a=.9)
    A('wall', 'dots', dots=cloud(950, 80, 240, 360, r, 2.2), color=PAL['purple'], a=.9)
    for i in range(3):
        scrawl(A, r, 90 + i * 16, 52 + i * 8, 960, 120, PAL['yellow'], 9 - i * 2, 'over', (.05 + i * .13, .45 + i * .13), PAL['blue'] if i == 0 else None, 6 - i)
    spark(A, r, 1100, 40, 16, PAL['yellow'], 'over', (.8, .88))
    cross(A, r, 90, 200, 12, PAL['white'], 4, 'over', (.82, .9))
    drip_edge(A, r, 120, 1100, 190, PAL['yellow'], 14, 'over', (.68, .92), 10, 40)
    return compose(sc, 'a3', T, True, '', title='Tag', desc='Painel de tag sem texto: rabisco amarelo largo sobre um fundo magenta rosa com respingos azuis e roxos e tinta escorrendo.')


# ----------------------------------------------------------------------------- headers
def header(uid, text, st, field, accent, seed, T=10):
    r = random.Random(seed)
    sc = Scene(1200, 150, bg=BG)
    A = sc.add
    concrete(A, r, 1200, 150)
    A('wall', 'halo', c=(300, 75), r=300, color=accent, a=.45)
    color_field(A, r, 600, 76, 590, 62, field, .96, .1, 26, 'wall', None, 110)
    halftone(A, 40, 4, 300, 40, 8, accent, 'down', a=.8)
    pixo(A, r, 60, 96, 200, 40, PAL['white'], 3.5, a=.8)
    tag_loop(A, r, 930, 104, 200, 18, PAL['yellow'], 3.5, a=.9)
    cross(A, r, 1150, 40, 8, PAL['white'], 3.5)
    h = min(fit(text, 760, 26), 96)
    y = (150 - h) / 2 - 10
    add_spray(A, r, text, 600, y, h, st['fill'][0], 26, -1.5, seed, 140)
    add_drips(A, r, text, 600, y, h, st['fill'], 26, -1.5, st['ow'], seed, .6)
    letters = letters_svg(text, 600, y, h, st, True, T, -1.5, 26, seed)
    return compose(sc, 'h' + uid, T, True, letters, '', text.title(), f'Cabeçalho de seção em graffiti de rua escrevendo {text}.')


def header_signature():
    T, r = 12, random.Random(99)
    sc = Scene(1200, 240, bg=BG)
    A = sc.add
    concrete(A, r, 1200, 240)
    A('wall', 'halo', c=(600, 120), r=420, color=PAL['crimson'], a=.7)
    color_field(A, r, 600, 112, 560, 96, PAL['crimson'], .96, .1, 26, 'wall', None, 130)
    color_field(A, r, 200, 170, 200, 60, PAL['purple'], .85, .15)
    halftone(A, 700, 190, 420, 44, 8, PAL['white'], 'left', a=.4)
    wild_arrow(A, r, 20, 214, 300, 56, -6, PAL['white'], PAL['violet'])
    scrawl(A, r, 280, 38, 640, 110, PAL['white'], 8, 'over', (.05, .55), PAL['black'], 5)
    scrawl(A, r, 300, 46, 600, 96, PAL['red'], 4, 'over', (.15, .62), None, 5)
    crown(A, r, 120, 70, 60, PAL['yellow'], 5, 'over', (.6, .7))
    cross(A, r, 1100, 60, 12, PAL['white'], 4, 'over', (.7, .78))
    drip_edge(A, r, 320, 900, 150, PAL['red'], 12, 'over', (.6, .9), 10, 50)
    tag = plain_svg('SEJA CRIATIVO. SEJA INTENSO.', 600, 190, 26, PAL['yellow'], 3.6, animate=True, T=T, t0=.6, t1=.92, shadow=PAL['black'])
    return compose(sc, 'sg', T, True, '', tag, 'Assinatura', 'Assinatura de rua em rabisco branco e vermelho sobre fundo carmesim, com a frase seja criativo, seja intenso.')


if __name__ == '__main__':
    write('assets/banners/banner-01-massaru.svg', banner01())
    write('assets/banners/banner-02-about-me.svg', banner02())
    write('assets/banners/banner-03-my-skills.svg', banner03())
    write('assets/banners/banner-04-instagram.svg', banner04())
    write('assets/banners/art-01-pixo.svg', art01())
    write('assets/banners/art-02-wildstyle.svg', art02())
    write('assets/banners/art-03-tag.svg', art03())
    write('assets/headers/header-personal-info.svg', header('personal', 'INFO PESSOAL', dict(fill=[PAL['white']], fw=14, outline=PAL['black'], ow=27, hl=PAL['pink'], extrude=(PAL['magenta'], 5, (1.4, 1.8)), rough=4), PAL['crimson'], PAL['magenta'], 11))
    write('assets/headers/header-dev-interests.svg', header('interests', 'INTERESSES DEV', dict(fill=[PAL['yellow']], fw=14, outline=PAL['black'], ow=27, hl=PAL['white'], extrude=(PAL['blue'], 5, (1.4, 1.8)), rough=4), PAL['violet'], PAL['blue'], 12))
    write('assets/headers/header-signature.svg', header_signature())
