"""generate-animations.py - gera assets/animations/*.
  * massaru-painting.gif : the MASSARU graffiti painted frame by frame (Pillow)  -> README hero
  * tagline.svg          : animated tagline, lettering draws itself and loops
  * drip-loop.svg        : endless paint drips
  * spray-reveal.svg     : a spray can sweeps across the page painting a streak
Run:  python3 tools/generate-animations.py   (add --no-gif to skip the slow GIF)
"""
import os, random, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graffiti import *  # noqa
from graffiti import _pd
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'assets', 'animations')
os.makedirs(OUT, exist_ok=True)

GIF_SIZE = (960, 336)       # final pixel size of the GIF
GIF_FRAMES = 46             # painting frames (the last frame is held)


def make_gif():
    SS = 2
    sc = scene_main()
    base = scene_pil(sc, SS)
    m = MAIN
    frames = []
    for k in range(GIF_FRAMES):
        t = k / (GIF_FRAMES - 1) * 0.95
        img = base.copy()
        for it in sc.spray:
            pil_item(img, it, t, SS)
        letters_pil(img, m['text'], m['cx'], m['y'], m['h'], STYLE_MAIN, t, m['rot'], m['track'], SS)
        for it in sc.over:
            pil_item(img, it, t, SS)
        frames.append(img.convert('RGB').resize(GIF_SIZE, Image.LANCZOS))
    pal = frames[-1].quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    dur = [450] + [85] * (len(q) - 2) + [4200]
    path = os.path.join(OUT, 'massaru-painting.gif')
    q[0].save(path, save_all=True, append_images=q[1:], duration=dur, loop=0, optimize=True, disposal=1)
    print('wrote assets/animations/massaru-painting.gif', f'{os.path.getsize(path) / 1024:.0f} KB')


def write(name, svg):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(svg)
    print('wrote assets/animations/' + name, f'{len(svg) / 1024:.1f} KB')


def tagline():
    T, r = 9, random.Random(61)
    text = 'DEV \u2022 ARTISTA \u2022 PROGRAMADOR DE JOGOS \u2022 CRIADOR'
    h = min(fit(text, 900, 24), 30)
    sc = Scene(1200, 96, bg=False)
    A = sc.add
    strip = jit([(60, 22), (1140, 14), (1150, 78), (50, 84)], r, 3, 6)
    A('wall', 'poly', pts=[(x + 5, y + 6) for x, y in strip], fill=PAL['crimson'], a=1)
    A('wall', 'poly', pts=strip, fill=PAL['black'], a=1, stroke=PAL['red'], sw=3)
    A('over', 'line', pts=swoosh(250, 950, 74, 6), color=PAL['red'], w=4, a=1, stage=(.7, .88))
    A('over', 'poly', pts=star(88, 48, 14, 4, 4, 0), fill=PAL['yellow'], a=1, stage=(.76, .86))
    A('over', 'poly', pts=star(1112, 48, 14, 4, 4, 0), fill=PAL['yellow'], a=1, stage=(.78, .88))
    A('over', 'dots', dots=cloud(600, 48, 800, 120, r, 1.4), color=PAL['magenta'], a=.7, stage=(.05, .5))
    txt = plain_svg(text, 600, 48 - h * .5, h, PAL['yellow'], max(3.2, h * .13), 'middle', 24, True, T, .08, .68, shadow=PAL['red'])
    write('tagline.svg', compose_scene(sc, 'tg', T, True, txt, title='Tagline', desc='Dev, artista, programador de jogos e criador, pintado numa faixa preta.'))


def drip_loop():
    r = random.Random(71)
    W, H = 1200, 120
    parts = [f'<path d="M0,0 L{W},0 L{W},12 ' + ' '.join(f'L{x},{12 + r.uniform(-3, 4):.1f}' for x in range(W, -1, -24)) + ' Z" fill="#E5192B" stroke="#0B0A0F" stroke-width="3"/>']
    cols = [PAL['red'], PAL['magenta'], PAL['purple'], PAL['crimson']]
    for i in range(34):
        x = 20 + i * 34 + r.uniform(-8, 8)
        L = r.uniform(24, 100)
        dur = r.uniform(4, 8)
        begin = -r.uniform(0, dur)
        col = r.choice(cols)
        w = r.uniform(4, 8)
        a = (f'<animate attributeName="{{}}" values="{{}}" keyTimes="0;.55;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>')
        parts.append(
            f'<line x1="{x:.1f}" y1="10" x2="{x:.1f}" y2="{10 + L:.1f}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round">'
            + a.format('y2', f'10;{10 + L:.1f};{10 + L:.1f}') + '</line>'
            + f'<circle cx="{x:.1f}" cy="{10 + L:.1f}" r="{w * .85:.1f}" fill="{col}">' + a.format('cy', f'10;{10 + L:.1f};{10 + L:.1f}')
            + a.format('opacity', '0;1;1').replace('keyTimes=".55"', 'keyTimes=".55"') + '</circle>')
    return svg_doc(W, H, ''.join(parts), 'Tinta escorrendo', 'Gotas de tinta vermelha, magenta e roxa escorrendo em loop.')


def spray_reveal():
    T, r = 8, random.Random(81)
    pts = [(60 + i * 1080 / 80, 56 + math.sin(i * .22) * 12) for i in range(81)]
    d = _pd(pts)
    ln = lambda col, w, off=(0, 0): (f'<path d="{_pd([(x + off[0], y + off[1]) for x, y in pts])}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
                                      f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1 2" stroke-dashoffset="0">'
                                      f'<animate attributeName="stroke-dashoffset" values="1.1;1.1;0;0" keyTimes="0;.04;.62;1" dur="{T}s" repeatCount="indefinite"/></path>')
    dots = ''.join(f'<circle cx="{x + r.gauss(0, 16):.1f}" cy="{y + r.gauss(2, 14):.1f}" r="{r.uniform(.6, 1.7):.1f}">'
                   f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{0.04 + .58 * i / 80:.3f};{0.07 + .58 * i / 80:.3f};1" dur="{T}s" repeatCount="indefinite"/></circle>'
                   for i, (x, y) in enumerate(pts) for _ in range(2))
    can = (f'<g><animateMotion path="M0,0 L1080,0" dur="{T}s" keyPoints="0;0;1;1" keyTimes="0;.04;.62;1" calcMode="linear" repeatCount="indefinite"/>'
           + ill_can(42, 8, .62) + '</g>')
    can = f'<g><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.62;.7;1" dur="{T}s" repeatCount="indefinite"/>{can}</g>'
    body = (f'<g opacity="1"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.93;.99;1" dur="{T}s" repeatCount="indefinite"/>'
            + ln(PAL['black'], 20, (3, 5)) + ln(PAL['magenta'], 15) + ln(PAL['pink'], 3.5, (0, -3)) + f'<g fill="{PAL["red"]}">{dots}</g>' + can + '</g>')
    return svg_doc(1200, 110, body, 'Spray pintando', 'Uma lata de spray percorre a tela pintando um traço magenta.')


if __name__ == '__main__':
    tagline()
    write('drip-loop.svg', drip_loop())
    write('spray-reveal.svg', spray_reveal())
    if '--no-gif' not in sys.argv:
        make_gif()
