"""generate-icons.py - gera assets/icons, assets/social, assets/illustrations e assets/backgrounds.
Edite TECH / LABELS / SOCIAL abaixo para mudar os textos das etiquetas e rode:  python3 tools/generate-icons.py
"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from street import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def write(rel, svg):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(svg)


# ----------------------------------------------------------------------------- editable content
TECH = [  # (file slug, label, colour)
    ('nestjs', 'NESTJS', 'red'), ('codeigniter', 'CODEIGNITER', 'red'), ('meteor', 'METEOR', 'red'),
    ('javascript', 'JAVASCRIPT', 'yellow'), ('html5', 'HTML5', 'yellow'), ('css3', 'CSS3', 'yellow'),
    ('postgresql', 'POSTGRESQL', 'blue'),
    ('python', 'PYTHON', 'magenta'), ('cpp', 'C++', 'magenta'),
    ('unreal-engine', 'UNREAL ENGINE', 'purple'), ('blender', 'BLENDER', 'purple'), ('photoshop', 'PHOTOSHOP', 'purple'),
    ('linux', 'LINUX', 'cyan'), ('debian', 'DEBIAN', 'cyan'), ('ubuntu', 'UBUNTU', 'cyan'), ('apache', 'APACHE', 'cyan'), ('vscode', 'VS CODE', 'cyan'),
]
LABELS = [('name', 'NOME', 'yellow'), ('studying', 'ESTUDANDO', 'pink'), ('focus', 'FOCO', 'cyan'), ('activities', 'ATIVIDADES', 'yellow'),
          ('creative', 'CRIATIVO', 'pink'), ('goals', 'METAS', 'cyan'), ('learning', 'APRENDENDO', 'yellow')]
TW = 'M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.43l-3 3v-3H6.857V1.714h13.714Z'
SOCIAL = [  # (slug, label shown on the button, accent colour, glyph)
    ('instagram', '@MASSDVV_', 'magenta', 'ig'), ('twitch', '@MASSADV_', 'purple', TW),
    ('more', 'MAIS EM BREVE', 'yellow', 'plus'),
]


def glyph_group(glyph, color):
    if glyph == 'ig':
        return (f'<rect x="-30" y="-30" width="60" height="60" rx="18" fill="none" stroke="{color}" stroke-width="6"/>'
                f'<circle r="13" fill="none" stroke="{color}" stroke-width="6"/><circle cx="19" cy="-19" r="3.6" fill="{color}"/>')
    if glyph == 'plus':
        return f'<path d="M0,-24 L0,24 M-24,0 L24,0" stroke="{color}" stroke-width="9" stroke-linecap="round"/>'
    return f'<path d="{glyph}" transform="translate(-24,-24) scale(2)" fill="{color}"/>'


def icon_group(accent, glyph, size=96):
    s = size / 96
    r = random.Random(len(glyph))
    dots = ''.join(f'<circle cx="{r.gauss(48, 34):.1f}" cy="{r.gauss(48, 34):.1f}" r="{r.uniform(.6, 1.6):.1f}" fill="{PAL[accent]}" opacity=".8"/>' for _ in range(40))
    return (f'<g transform="scale({s})">{dots}'
            f'<rect x="10" y="12" width="78" height="78" rx="18" fill="{PAL[accent]}" stroke="{PAL["black"]}" stroke-width="4"/>'
            f'<rect x="6" y="6" width="78" height="78" rx="18" fill="{PAL["graphite"]}" stroke="{PAL["black"]}" stroke-width="4"/>'
            f'<rect x="12" y="12" width="66" height="66" rx="13" fill="none" stroke="{PAL[accent]}" stroke-width="3" opacity=".9"/>'
            f'<g transform="translate(45,45) scale(.56)">{glyph_group(glyph, PAL["white"])}</g></g>')


def icons():
    for slug, label, accent, glyph in SOCIAL:
        # wide button: icon + handle
        lay, wu = layout(label, 22)
        h = 26
        text_w = wu * h / 100
        W = int(100 + text_w + 34)
        body = (f'<rect x="12" y="14" width="{W - 16}" height="56" rx="16" fill="{PAL[accent]}" stroke="{PAL["black"]}" stroke-width="4"/>'
                f'<rect x="6" y="8" width="{W - 16}" height="56" rx="16" fill="{PAL["graphite"]}" stroke="{PAL["black"]}" stroke-width="4"/>'
                f'<g transform="translate(14,2) scale(.72)">{icon_group(accent, glyph)}</g>'
                + plain_svg(label, 92, 22, h, PAL['white'], 4, 'start', 22, shadow=PAL['black']) +
                f'<path d="M92,56 L{92 + text_w:.0f},56" stroke="{PAL[accent]}" stroke-width="4" stroke-linecap="round"/>')
        write(f'assets/social/button-{slug}.svg', svg_doc(W, 78, body, f'Link {slug.title()}', f'Botão em graffiti: {label}.'))


def tech():
    r = random.Random(5)
    for slug, label, col in TECH:
        lay, wu = layout(label, 22)
        h = 17
        tw = wu * h / 100
        W = int(tw + 44)
        rot = r.choice([-2, -1, 1, 2])
        body = (f'<g transform="rotate({rot} {W / 2:.0f} 26)">'
                f'<rect x="6" y="10" width="{W - 8}" height="34" rx="9" fill="{PAL[col]}" stroke="{PAL["black"]}" stroke-width="3"/>'
                f'<rect x="2" y="6" width="{W - 8}" height="34" rx="9" fill="{PAL["graphite"]}" stroke="{PAL["black"]}" stroke-width="3"/>'
                f'<rect x="6" y="10" width="{W - 16}" height="26" rx="6" fill="none" stroke="{PAL[col]}" stroke-width="1.6" opacity=".8"/>'
                + plain_svg(label, W / 2 - 2, 15, h, PAL['white'], 3.1, 'middle', 22) + '</g>')
        write(f'assets/icons/tech-{slug}.svg', svg_doc(W + 6, 52, body, label, f'Etiqueta {label}.'))
    for slug, label, col in LABELS:
        lay, wu = layout(label, 22)
        h = 20
        tw = wu * h / 100
        W = int(tw + 40)
        pts = f'8,8 {W},4 {W - 4},40 4,44'
        body = (f'<polygon points="{pts}" transform="translate(4,5)" fill="{PAL["black"]}"/>'
                f'<polygon points="{pts}" fill="{PAL[col]}" stroke="{PAL["black"]}" stroke-width="3" stroke-linejoin="round"/>'
                + plain_svg(label, W / 2, 14, h, PAL['black'], 3.6, 'middle', 22) + '')
        write(f'assets/icons/label-{slug}.svg', svg_doc(W + 8, 52, body, label.title(), f'Etiqueta {label} da seção de informações pessoais.'))


CONTROLLER = ('M20,50 C20,30 50,28 60,36 L100,36 C110,28 140,30 140,50 L148,90 C150,108 130,112 118,98 L108,84 L52,84 L42,98 '
              'C30,112 10,108 12,90 Z M40,42 H48 V50 H56 V58 H48 V66 H40 V58 H32 V50 H40 Z '
              'M106,50 A6,6 0 1 0 118,50 A6,6 0 1 0 106,50 Z M120,62 A6,6 0 1 0 132,62 A6,6 0 1 0 120,62 Z '
              'M92,62 A6,6 0 1 0 104,62 A6,6 0 1 0 92,62 Z M106,74 A6,6 0 1 0 118,74 A6,6 0 1 0 106,74 Z')


def interest_card(slug, label, accent, uid, kind):
    r = random.Random(sum(map(ord, slug)))
    sc = Scene(280, 230, bg='#17141b')
    A = sc.add
    concrete(A, r, 280, 230)
    A('wall', 'halo', c=(140, 100), r=170, color=PAL[accent], a=.55)
    color_field(A, r, 140, 100, 128, 78, PAL[accent], .95, .12, 18, 'wall', None, 70)
    halftone(A, 10, 150, 260, 60, 8, PAL['white'], 'left', a=.35)
    art = ''
    if kind == 'games':
        art = stencil_svg(CONTROLLER, 50, 30, 1.22, PAL['white'], uid, True, 2)
    elif kind == 'web':
        marker(A, [(100, 50), (60, 100), (100, 150)], PAL['white'], 9, r, 'wall', under=PAL['black'])
        marker(A, [(180, 50), (220, 100), (180, 150)], PAL['white'], 9, r, 'wall', under=PAL['black'])
        marker(A, [(158, 36), (122, 164)], PAL['yellow'], 9, r, 'wall', under=PAL['black'])
    elif kind == 'art':
        art = stencil_hand(86, 24, 1.1, PAL['white'], uid)
        pixo(A, r, 14, 120, 70, 50, PAL['yellow'], 4)
        spark(A, r, 236, 40, 14, PAL['yellow'])
    else:
        marker(A, [(70, 60), (120, 100), (70, 140)], PAL['white'], 10, r, 'wall', under=PAL['black'])
        marker(A, [(140, 150), (212, 150)], PAL['yellow'], 10, r, 'wall', under=PAL['black'])
    p = scene_svg(sc, uid)
    h = min(fit(label, 200, 26), 50)
    txt = letters_svg(label, 140, 148, h, dict(fill=[PAL['white']], fw=14, outline=PAL['black'], ow=27, extrude=(PAL[accent], 4, (1.4, 1.8)), rough=3), False, 14, -2, 26, 2)
    body = p['wall'] + art + txt
    return svg_doc(280, 230, body, f'Card de interesse: {label.title()}', f'Card de rua: {label.lower()}.', p['defs'])


def illustrations():
    write('assets/illustrations/interest-games.svg', interest_card('games', 'JOGOS', 'magenta', 'ig1', 'games'))
    write('assets/illustrations/interest-web.svg', interest_card('web', 'WEB', 'blue', 'ig2', 'web'))
    write('assets/illustrations/interest-art.svg', interest_card('art', 'ARTE', 'red', 'ig3', 'art'))
    write('assets/illustrations/interest-linux.svg', interest_card('linux', 'LINUX', 'purple', 'ig4', 'linux'))


def backgrounds():
    r = random.Random(77)
    sc = Scene(1200, 170, bg='#17141b')
    A = sc.add
    concrete(A, r, 1200, 170)
    A('wall', 'halo', c=(300, 90), r=300, color=PAL['crimson'], a=.7)
    A('wall', 'halo', c=(900, 80), r=300, color=PAL['purple'], a=.55)
    color_field(A, r, 330, 90, 300, 70, PAL['crimson'], .95, .12, 22, 'wall', (5, -2, 10), 100)
    color_field(A, r, 900, 100, 280, 64, PAL['violet'], .95, .12, 22, 'wall', (-5, 2, 10), 100)
    halftone(A, 40, 110, 360, 50, 8, PAL['white'], 'right', a=.4)
    wild_arrow(A, r, 1196, 138, 380, 46, 186, PAL['magenta'], PAL['black'], fl=(5, 0, 10))
    pixo(A, r, 30, 24, 120, 60, PAL['white'], 4, a=.85)
    pixo(A, r, 1020, 30, 120, 56, PAL['yellow'], 4, a=.9)
    tag_loop(A, r, 440, 140, 320, 20, PAL['white'], 4, a=.8)
    cross(A, r, 1150, 40, 10, PAL['white'], 4)
    for x in range(40, 1180, 26):
        A('wall', 'drip', x=x + r.uniform(-6, 6), y=0, len=r.choice([6, 10, 16, 26, 40]), w=r.uniform(3.5, 6), color=PAL['red'])
    p = scene_svg(sc, 'bgw')
    tx = 'ARTE \u2022 C\u00d3DIGO \u2022 JOGOS'
    tags = plain_svg(tx, 600, 62, min(fit(tx, 780, 24), 56), PAL['white'], 6, 'middle', 24, shadow=PAL['red'], wobble=.8)
    body = p['wall'] + f'<g transform="rotate(-2 600 90)" opacity=".95">{tags}</g>'
    write('assets/backgrounds/footer-wall.svg', svg_doc(1200, 170, body, 'Rodapé parede de graffiti', 'Parede de concreto com pichação, spray, tinta escorrendo e a tag ARTE, CÓDIGO, JOGOS.', p['defs']))


if __name__ == '__main__':
    icons(); tech(); illustrations(); backgrounds()
    print('icons, social buttons, tech stickers, illustrations and backgrounds written')
