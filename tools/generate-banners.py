"""generate-banners.py - gera assets/banners/*.svg e assets/headers/*.svg.

O banner 01 é a arte final estática (a animação de pintura fica em assets/animations/massaru-painting.gif).
Os banners 02-04 e os cabeçalhos são SVGs animados (SMIL) que se pintam sozinhos em loop.
Rodar:  python3 tools/generate-banners.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graffiti import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def write(rel, svg):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote', rel, f'{len(svg) / 1024:.1f} KB')


def compose(sc, uid, T, animate, letters, extra_over='', title='', desc='', pre_letters=''):
    """wall -> (fade group: spray, illustrations, letters, over, extras)"""
    p = scene_svg(sc, uid, animate, T)
    inner = pre_letters + p['spray'] + letters + p['over'] + extra_over
    body = p['wall'] + global_fade(inner, T, animate)
    return svg_doc(sc.w, sc.h, body, title, desc, p['defs'])


# ----------------------------------------------------------------------------- banner 01
def banner01():
    sc = scene_main()
    m = MAIN
    letters = letters_svg(m['text'], m['cx'], m['y'], m['h'], STYLE_MAIN, False, rot=m['rot'], track=m['track'])
    return compose(sc, 'b1', 14, False, letters, title='MASSARU', desc='Graffiti vermelho em letras bolha escrevendo MASSARU numa parede escura, com spray, tinta escorrendo, setas e estrelas.')


# ----------------------------------------------------------------------------- banner 02 - ABOUT ME
def banner02():
    T, r = 12, random.Random(21)
    sc = Scene(1200, 300)
    A = sc.add
    A('wall', 'halo', c=(260, 150), r=320, color=PAL['magenta'], a=.5)
    A('wall', 'halo', c=(980, 190), r=300, color=PAL['purple'], a=.5)
    A('wall', 'halo', c=(620, 150), r=330, color=PAL['crimson'], a=.7)
    A('wall', 'poly', pts=jit(blob(600, 130, 520, 110, 24, r), r, 2.5), fill=PAL['crimson'], a=.95, fl=(5, -3, 9))
    A('wall', 'poly', pts=jit(arrow(-30, 215, 560, 170, -6), r), fill=PAL['magenta'], a=.9, stroke=PAL['black'], sw=4, fl=(-7, 4, 10))
    A('wall', 'poly', pts=jit([(880, 300), (1200, 40), (1200, 300)], r, 2), fill=PAL['purple'], a=.95, stroke=PAL['black'], sw=4, fl=(6, 3, 11))
    A('wall', 'poly', pts=jit(star(1010, 70, 58, 30, 9, 3), r, 1.5), fill=PAL['yellow'], a=.95, stroke=PAL['black'], sw=4, fl=(0, 6, 7))
    for pts, c in pixels(10, 232, 9, 4, 14, [PAL['blue'], PAL['violet'], PAL['black']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.95)
    for ln in web(1200, 0, 170, 98, 172):
        A('wall', 'line', pts=ln, color=PAL['white'], w=1.5, a=.45)
    A('wall', 'line', pts=scribble(300, 24, 330, 32, r), color=PAL['yellow'], w=4, a=.9)
    A('wall', 'line', pts=zigzag(900, 262, 140, 12, 8), color=PAL['blue'], w=6, a=.95)
    A('wall', 'dots', dots=cloud(230, 130, 120, 220, r), color=PAL['pink'], a=.7)
    A('wall', 'dots', dots=cloud(1000, 230, 110, 200, r), color=PAL['red'], a=.8)
    text, cx, y = 'SOBRE MIM', 600, 62
    h = fit(text, 720, 30)
    st = dict(fill=[PAL['yellow']], fw=26, outline=PAL['black'], ow=45, hl=PAL['white'], extrude=(PAL['violet'], 9, (2.4, 3.0)))
    lay, wu = layout(text, 30)
    x0 = cx - wu * (h / 100) / 2
    for i, g in enumerate(lay):
        gx = x0 + (g['x0'] + g['w'] / 2) * h / 100
        A('spray', 'dots', dots=cloud(gx, y + h / 2, 60, 45, r, 1.4), color=PAL['white'], a=.8, stage=(.02 + i * .012, .12))
    A('over', 'line', pts=swoosh(260, 940, 196, 22), color=PAL['blue'], w=9, a=1, stage=STAGES['details'])
    for d in make_drips(text, cx, y, h, st['fill'], r, 30, 0, 45, chance=.75):
        A('over', 'drip', **{k: v for k, v in d.items() if k != 't'})
    letters = letters_svg(text, cx, y, h, st, True, T, 0, 30)
    tag = plain_svg('OI, TUDO BEM? PRAZER!', 600, 252, 20, PAL['white'], 3.2, animate=True, T=T, t0=.55, t1=.9, shadow=PAL['crimson'])
    art = (reveal(float_wrap(ill_hand(40, 62, 1.45, 'a'), 0, -5, 6), (0.0, .1), T) +
           reveal(float_wrap(ill_can(1068, 52, 1.7), 0, 5, 7), (0.02, .12), T) +
           reveal(ill_burst(160, 56, .55), (.82, .9), T))
    return compose(sc, 'b2', T, True, letters, tag + art, 'Sobre mim',
                   'Letras de graffiti amarelas escrevendo SOBRE MIM, com uma mão pintada a spray e uma lata de tinta.')


# ----------------------------------------------------------------------------- banner 03 - MY SKILLS
def banner03():
    T, r = 12, random.Random(33)
    sc = Scene(1200, 300)
    A = sc.add
    A('wall', 'halo', c=(300, 140), r=330, color=PAL['blue'], a=.5)
    A('wall', 'halo', c=(900, 160), r=320, color=PAL['purple'], a=.6)
    A('wall', 'halo', c=(600, 290), r=300, color=PAL['magenta'], a=.35)
    A('wall', 'poly', pts=jit(blob(600, 140, 520, 118, 22, r), r, 2.5), fill=PAL['violet'], a=.95, fl=(-5, 3, 9))
    A('wall', 'poly', pts=jit(arrow(1220, 232, 600, 150, 184), r), fill=PAL['blue'], a=.88, stroke=PAL['black'], sw=4, fl=(8, -4, 10))
    A('wall', 'poly', pts=jit(arrow(-20, 60, 480, 120, 8), r), fill=PAL['magenta'], a=.75, stroke=PAL['black'], sw=4, fl=(-6, 5, 12))
    for pts, c in pixels(520, 6, 14, 4, 16, [PAL['purple'], PAL['blue'], PAL['black'], PAL['violet']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.9)
    for pts, c in pixels(980, 240, 10, 3, 14, [PAL['red'], PAL['crimson'], PAL['black']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.9)
    A('wall', 'poly', pts=jit(star(600, 276, 40, 22, 8, 0), r, 1.2), fill=PAL['yellow'], a=.9, stroke=PAL['black'], sw=4)
    A('wall', 'line', pts=scribble(420, 266, 360, 26, r), color=PAL['white'], w=3, a=.7)
    A('wall', 'line', pts=zigzag(220, 26, 140, 12, 8), color=PAL['yellow'], w=6, a=.95)
    A('wall', 'dots', dots=cloud(330, 150, 120, 220, r), color=PAL['cyan'], a=.7)
    A('wall', 'dots', dots=cloud(880, 120, 110, 200, r), color=PAL['pink'], a=.75)
    text, cx, y = 'HABILIDADES', 600, 54
    h = fit(text, 700, 30)
    st = dict(fill=[PAL['white']], fw=26, outline=PAL['black'], ow=45, shadow=(PAL['purple'], (10, 12)), hl=PAL['cyan'])
    lay, wu = layout(text, 30)
    x0 = cx - wu * (h / 100) / 2
    for i, g in enumerate(lay):
        gx = x0 + (g['x0'] + g['w'] / 2) * h / 100
        A('spray', 'dots', dots=cloud(gx, y + h / 2, 60, 45, r, 1.4), color=PAL['cyan'], a=.8, stage=(.02 + i * .012, .12))
    for d in make_drips(text, cx, y, h, [PAL['white'], PAL['cyan']], r, 30, 0, 45, chance=.7):
        A('over', 'drip', **{k: v for k, v in d.items() if k != 't'})
    letters = letters_svg(text, cx, y, h, st, True, T, 0, 30)
    tag = plain_svg('COM O QUE EU TRABALHO', 600, 238, 22, PAL['yellow'], 3.4, animate=True, T=T, t0=.55, t1=.9, shadow=PAL['black'])
    brackets = letters_svg('</>', 118, 84, 78, dict(fill=[PAL['yellow']], fw=19, outline=PAL['black'], ow=34, shadow=(PAL['crimson'], (7, 9))), True, T, -6, 24)
    art = (reveal(float_wrap(ill_window(1000, 52, 1.05), 0, -5, 7), (0.02, .12), T) +
           reveal(float_wrap(ill_controller(60, 164, .95), 0, 5, 6), (0.04, .14), T) +
           reveal(float_wrap(ill_window(1040, 190, .42, True), 0, 4, 8), (0.06, .16), T))
    return compose(sc, 'b3', T, True, letters, tag + brackets + art, 'Habilidades',
                   'Letras de graffiti brancas escrevendo HABILIDADES, com uma janela de código, um controle de videogame e colchetes de código.')


# ----------------------------------------------------------------------------- banner 04 - INSTAGRAM
def banner04():
    T, r = 12, random.Random(44)
    sc = Scene(1200, 300)
    A = sc.add
    A('wall', 'halo', c=(200, 150), r=320, color=PAL['red'], a=.6)
    A('wall', 'halo', c=(800, 150), r=360, color=PAL['magenta'], a=.5)
    A('wall', 'halo', c=(1100, 250), r=260, color=PAL['purple'], a=.55)
    A('wall', 'poly', pts=jit(blob(660, 150, 520, 125, 24, r), r, 2.5), fill=PAL['dark'], a=.95, fl=(5, 3, 9))
    A('wall', 'poly', pts=jit(arrow(1230, 70, 560, 140, 186), r), fill=PAL['purple'], a=.9, stroke=PAL['black'], sw=4, fl=(7, 4, 10))
    A('wall', 'poly', pts=jit(arrow(-30, 258, 520, 130, -8), r), fill=PAL['red'], a=.88, stroke=PAL['black'], sw=4, fl=(-7, -4, 11))
    A('wall', 'poly', pts=jit(star(380, 40, 44, 24, 9, 3), r, 1.4), fill=PAL['yellow'], a=.95, stroke=PAL['black'], sw=4, fl=(0, 5, 6))
    for pts, c in pixels(1030, 8, 9, 5, 15, [PAL['magenta'], PAL['crimson'], PAL['black']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.95)
    for ln in web(0, 300, 160, -82, -8):
        A('wall', 'line', pts=ln, color=PAL['white'], w=1.5, a=.4)
    A('wall', 'line', pts=scribble(980, 252, 190, 26, r, 34), color=PAL['yellow'], w=3, a=.9)
    A('wall', 'dots', dots=cloud(670, 150, 150, 260, r), color=PAL['pink'], a=.7)
    text, cx, y = 'INSTAGRAM', 700, 78
    h = fit(text, 640, 30)
    st = dict(fill=[PAL['magenta']], fw=26, outline=PAL['black'], ow=45, shadow=(PAL['purple'], (10, 12)), hl=PAL['yellow'])
    lay, wu = layout(text, 30)
    x0 = cx - wu * (h / 100) / 2
    for i, g in enumerate(lay):
        gx = x0 + (g['x0'] + g['w'] / 2) * h / 100
        A('spray', 'dots', dots=cloud(gx, y + h / 2, 60, 45, r, 1.4), color=PAL['yellow'], a=.8, stage=(.02 + i * .012, .12))
    for d in make_drips(text, cx, y, h, [PAL['magenta'], PAL['pink']], r, 30, 0, 45, chance=.7):
        A('over', 'drip', **{k: v for k, v in d.items() if k != 't'})
    letters = letters_svg(text, cx, y, h, st, True, T, -2, 30)
    follow = plain_svg('ME SIGA NO', 700, 40, 20, PAL['yellow'], 3.2, animate=True, T=T, t0=.1, t1=.4, shadow=PAL['black'])
    handle = plain_svg('@MASSDVV_', 700, 244, 34, PAL['white'], 4.4, animate=True, T=T, t0=.55, t1=.9, shadow=PAL['crimson'])
    art = (reveal(float_wrap(ill_ig(70, 60, 1.75, 'igg'), 0, -6, 6), (0.0, .12), T) +
           reveal(float_wrap(ill_heart(1040, 150, .9), 0, 5, 5), (.8, .9), T) +
           reveal(ill_burst(1120, 70, .42, PAL['yellow']), (.82, .9), T))
    flash = ''.join(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PAL["yellow"]}" stroke-width="5" stroke-linecap="round"/>'
                    for x1, y1, x2, y2 in [(270, 40, 292, 22), (286, 68, 314, 62), (246, 22, 252, 0)])
    return compose(sc, 'b4', T, True, letters, follow + handle + art + reveal(flash, (.85, .92), T), 'Instagram @massdvv_',
                   'Letras de graffiti magenta escrevendo INSTAGRAM, com um ícone estilo Instagram e o perfil @massdvv_.')


# ----------------------------------------------------------------------------- headers
def header(name, text, st, bg, T=10, h_px=150, extra=''):
    r = random.Random(sum(map(ord, name)))
    sc = Scene(1200, h_px)
    A = sc.add
    for it in bg(r):
        A('wall', **it)
    h = min(fit(text, 760, 30), 92)
    cx, y = 600, (h_px - h) / 2 - 8
    lay, wu = layout(text, 30)
    x0 = cx - wu * (h / 100) / 2
    for i, g in enumerate(lay):
        gx = x0 + (g['x0'] + g['w'] / 2) * h / 100
        A('spray', 'dots', dots=cloud(gx, y + h / 2, 50, 30, r, 1.3), color=PAL['white'], a=.8, stage=(.02 + i * .01, .12))
    for d in make_drips(text, cx, y, h, st['fill'], r, 30, 0, st['ow'], chance=.6):
        A('over', 'drip', **{k: v for k, v in d.items() if k != 't'})
    letters = letters_svg(text, cx, y, h, st, True, T, -1.5, 30)
    return compose(sc, 'h' + name[:6], T, True, letters, extra, text.title(), f'Cabeçalho de seção em graffiti escrevendo {text}.')


def bg_personal(r):
    out = [dict(t='halo', c=(300, 75), r=300, color=PAL['magenta'], a=.5), dict(t='halo', c=(950, 80), r=280, color=PAL['purple'], a=.5),
           dict(t='poly', pts=jit(blob(600, 75, 540, 62, 22, r), r, 2), fill=PAL['crimson'], a=.9, fl=(5, -2, 8)),
           dict(t='poly', pts=jit(arrow(-20, 118, 330, 90, -5), r), fill=PAL['magenta'], a=.85, stroke=PAL['black'], sw=3),
           dict(t='poly', pts=jit(arrow(1220, 40, 330, 80, 185), r), fill=PAL['purple'], a=.9, stroke=PAL['black'], sw=3),
           dict(t='line', pts=scribble(60, 24, 180, 22, r, 30), color=PAL['yellow'], w=3, a=.9),
           dict(t='dots', dots=cloud(1000, 110, 100, 150, r), color=PAL['pink'], a=.7)]
    out += [dict(t='line', pts=ln, color=PAL['white'], w=1.4, a=.4) for ln in web(1200, 0, 130, 98, 172)]
    return out


def bg_interests(r):
    out = [dict(t='halo', c=(900, 75), r=300, color=PAL['blue'], a=.4), dict(t='halo', c=(250, 80), r=280, color=PAL['red'], a=.5),
           dict(t='poly', pts=jit(blob(600, 75, 540, 62, 22, r), r, 2), fill=PAL['violet'], a=.92, fl=(-5, 2, 8)),
           dict(t='poly', pts=jit(star(110, 70, 50, 27, 9, 4), r, 1.4), fill=PAL['yellow'], a=.95, stroke=PAL['black'], sw=3, fl=(0, 5, 6)),
           dict(t='poly', pts=jit(arrow(1230, 112, 320, 86, 186), r), fill=PAL['magenta'], a=.85, stroke=PAL['black'], sw=3),
           dict(t='line', pts=zigzag(980, 24, 150, 10, 8), color=PAL['yellow'], w=5, a=.95),
           dict(t='dots', dots=cloud(300, 70, 110, 160, r), color=PAL['pink'], a=.7)]
    for pts, c in pixels(1020, 100, 9, 3, 14, [PAL['blue'], PAL['purple'], PAL['black']], r):
        out.append(dict(t='poly', pts=pts, fill=c, a=.9))
    return out


def header_signature():
    T, r = 12, random.Random(99)
    sc = Scene(1200, 250)
    A = sc.add
    A('wall', 'halo', c=(600, 125), r=420, color=PAL['crimson'], a=.8)
    A('wall', 'halo', c=(160, 200), r=260, color=PAL['purple'], a=.5)
    A('wall', 'halo', c=(1060, 60), r=240, color=PAL['blue'], a=.3)
    A('wall', 'poly', pts=jit(blob(600, 120, 540, 96, 24, r), r, 2.5), fill=PAL['dark'], a=.95, fl=(5, -3, 9))
    A('wall', 'poly', pts=jit(arrow(-30, 190, 440, 120, -7), r), fill=PAL['magenta'], a=.85, stroke=PAL['black'], sw=4)
    A('wall', 'poly', pts=jit(arrow(1230, 60, 440, 110, 187), r), fill=PAL['purple'], a=.9, stroke=PAL['black'], sw=4)
    A('wall', 'poly', pts=jit(star(120, 60, 52, 28, 9, 4), r, 1.5), fill=PAL['yellow'], a=.95, stroke=PAL['black'], sw=4, fl=(0, 6, 6))
    A('wall', 'poly', pts=jit(star(1090, 190, 60, 32, 10, 0), r, 1.5), fill=PAL['yellow'], a=.9, stroke=PAL['black'], sw=4, fl=(0, -6, 7))
    for ln in web(0, 0, 150, 8, 82):
        A('wall', 'line', pts=ln, color=PAL['white'], w=1.4, a=.4)
    A('wall', 'dots', dots=cloud(600, 120, 220, 300, r), color=PAL['red'], a=.6)
    text, cx, y = 'MASSARU', 600, 38
    h = fit(text, 620, 24)
    st = dict(fill=[PAL['red'], PAL['red'], PAL['magenta'], PAL['magenta'], PAL['red'], PAL['red'], PAL['red']], fw=25, outline=PAL['black'], ow=44, shadow=(PAL['crimson'], (9, 11)), hl=PAL['white'])
    for d in make_drips(text, cx, y, h, st['fill'], r, 24, 2, 44, chance=.8):
        A('over', 'drip', **{k: v for k, v in d.items() if k != 't'})
    letters = letters_svg(text, cx, y, h, st, True, T, 2, 24)
    tag = plain_svg('SEJA CRIATIVO. SEJA INTENSO.', 600, 214, 22, PAL['yellow'], 3.4, animate=True, T=T, t0=.6, t1=.92, shadow=PAL['black'])
    return compose(sc, 'sg', T, True, letters, tag, 'Assinatura', 'Assinatura MASSARU em letras bolha vermelhas com a frase seja criativo, seja intenso.')


if __name__ == '__main__':
    write('assets/banners/banner-01-massaru.svg', banner01())
    write('assets/banners/banner-02-about-me.svg', banner02())
    write('assets/banners/banner-03-my-skills.svg', banner03())
    write('assets/banners/banner-04-instagram.svg', banner04())
    write('assets/headers/header-personal-info.svg', header('personal', 'INFO PESSOAL', dict(fill=[PAL['white']], fw=26, outline=PAL['black'], ow=45, shadow=(PAL['magenta'], (9, 11)), hl=PAL['pink']), bg_personal))
    write('assets/headers/header-dev-interests.svg', header('interests', 'INTERESSES DEV', dict(fill=[PAL['yellow']], fw=26, outline=PAL['black'], ow=45, shadow=(PAL['blue'], (9, 11)), hl=PAL['white']), bg_interests))
    write('assets/headers/header-signature.svg', header_signature())
