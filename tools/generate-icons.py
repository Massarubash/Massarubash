"""generate-icons.py - gera assets/icons, assets/social, assets/illustrations e assets/backgrounds.
Edite TECH / LABELS / SOCIAL abaixo para mudar os textos das etiquetas e rode:  python3 tools/generate-icons.py
"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graffiti import *  # noqa

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


def interest_card(slug, label, art, accent, uid):
    r = random.Random(slug.__hash__() % 1000)
    sc = Scene(280, 230)
    A = sc.add
    A('wall', 'halo', c=(140, 100), r=170, color=PAL[accent], a=.6)
    A('wall', 'poly', pts=jit(blob(140, 104, 118, 74, 16, r), r, 2), fill=PAL['violet'] if accent != 'blue' else PAL['dark'], a=.95)
    A('wall', 'poly', pts=jit(arrow(-10, 170, 210, 60, -8), r), fill=PAL[accent], a=.85, stroke=PAL['black'], sw=3)
    A('wall', 'dots', dots=cloud(140, 110, 120, 140, r, 1.5), color=PAL['pink'], a=.7)
    for pts, c in pixels(216, 6, 4, 3, 12, [PAL[accent], PAL['black'], PAL['crimson']], r):
        A('wall', 'poly', pts=pts, fill=c, a=.9)
    p = scene_svg(sc, uid)
    txt = letters_svg(label, 140, 160, fit(label, 190, 26) if fit(label, 190, 26) < 52 else 52, dict(fill=[PAL['white']], fw=24, outline=PAL['black'], ow=42, shadow=(PAL[accent], (8, 10))), False, 14, -2, 26)
    body = p['wall'] + float_wrap(art, 0, -4, 5) + txt
    return svg_doc(280, 230, body, f'Card de interesse: {label.title()}', f'Card em graffiti: {label.lower()}.', p['defs'])


def illustrations():
    write('assets/illustrations/interest-games.svg', interest_card('games', 'JOGOS', ill_controller(60, 28, 1.1), 'magenta', 'ig1'))
    write('assets/illustrations/interest-web.svg', interest_card('web', 'WEB', ill_window(52, 22, .92), 'blue', 'ig2'))
    write('assets/illustrations/interest-art.svg', interest_card('art', 'ARTE', ill_can(100, 18, 1.1) + ill_hand(170, 40, .42, 'iah'), 'red', 'ig3'))
    write('assets/illustrations/interest-linux.svg', interest_card('linux', 'LINUX', ill_window(52, 22, .92, True), 'purple', 'ig4'))


def backgrounds():
    r = random.Random(77)
    sc = Scene(1200, 170, bg=PAL['graphite'])
    A = sc.add
    for row in range(0, 170, 22):
        off = 0 if (row // 22) % 2 == 0 else 40
        for x in range(-40 + off, 1200, 80):
            A('wall', 'poly', pts=[(x, row), (x + 78, row), (x + 78, row + 20), (x, row + 20)], fill=r.choice(['#201C26', '#1B1820', '#241F2B']), a=1)
    A('wall', 'halo', c=(300, 90), r=300, color=PAL['crimson'], a=.7)
    A('wall', 'halo', c=(900, 80), r=300, color=PAL['purple'], a=.55)
    A('wall', 'halo', c=(600, 150), r=260, color=PAL['magenta'], a=.3)
    A('wall', 'poly', pts=jit(arrow(-20, 140, 420, 90, -6), r), fill=PAL['magenta'], a=.7, stroke=PAL['black'], sw=3, fl=(-6, 2, 10))
    A('wall', 'poly', pts=jit(arrow(1220, 70, 420, 90, 186), r), fill=PAL['purple'], a=.8, stroke=PAL['black'], sw=3, fl=(6, -2, 10))
    for ln in web(0, 0, 150, 8, 82):
        A('wall', 'line', pts=ln, color=PAL['white'], w=1.4, a=.4)
    for ln in web(1200, 170, 140, 188, 262):
        A('wall', 'line', pts=ln, color=PAL['white'], w=1.4, a=.35)
    A('wall', 'poly', pts=star(150, 62, 34, 18, 9, 4), fill=PAL['yellow'], a=.9, stroke=PAL['black'], sw=3)
    A('wall', 'poly', pts=star(1060, 110, 40, 22, 10, 0), fill=PAL['yellow'], a=.85, stroke=PAL['black'], sw=3)
    A('wall', 'dots', dots=cloud(600, 90, 500, 380, r, 1.6), color=PAL['red'], a=.7)
    for x in range(40, 1180, 26):
        A('wall', 'drip', x=x + r.uniform(-6, 6), y=0, len=r.choice([6, 10, 16, 26, 40]), w=r.uniform(3.5, 6), color=PAL['red'])
    p = scene_svg(sc, 'bgw')
    tags = (plain_svg('MASSARU', 600, 58, 64, PAL['white'], 7, 'middle', 24, shadow=PAL['red']) )
    body = p['wall'] + f'<g transform="rotate(-2 600 90)" opacity=".92">{tags}</g>'
    write('assets/backgrounds/footer-wall.svg', svg_doc(1200, 170, body, 'Rodapé parede de graffiti', 'Parede de tijolos escura com spray, tinta escorrendo e a tag MASSARU.', p['defs']))


if __name__ == '__main__':
    icons(); tech(); illustrations(); backgrounds()
    print('icons, social buttons, tech stickers, illustrations and backgrounds written')
