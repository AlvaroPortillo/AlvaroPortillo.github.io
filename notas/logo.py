"""Genera el emblema Kingdom Hearts + World of Warcraft + Naruto.

- img/logo.svg          estático (para enlazarlo o usarlo como imagen)
- img/logo-animado.svg  animado (runas y vidriera girando, runas que laten, tomoe del sharingan girando)
- index.html            mete el animado entre <!-- logo:inicio --> y <!-- logo:fin -->

Capas, de atrás adelante:
- WoW: alas de dragón doradas (filigrana de los marcos de la interfaz) y una espada rúnica.
- KH: una llave espada, cruzada con la espada detrás del anillo.
- WoW: anillo de metal con remaches, cimera con gema y banda de piedra con runas arcanas (la piedra
  de hogar). Las runas son glifos inventados: no copian ningún alfabeto ni logotipo.
- KH + WoW: vidriera de la Estación del Despertar con los colores de la Alianza y la Horda.
- Naruto + KH: un sharingan cuya pupila es el corazón con la corona.

Uso:  python notas/logo.py
"""
import math
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent

ALIANZA = ('#2F6FE4', '#7FB2FF')   # azul y su cristal claro
HORDA = ('#B3261E', '#F0715E')     # rojo y su cristal claro
ARCANO = '#7DE8FF'
PIEDRA = '#151B2C'
PLOMO = '#0A0E1A'
ORO_CLARO = '#FFE08A'
ORO_OSCURO = '#9A6418'

# Glifos de 8 × 12 centrados en el origen (solo trazos)
RUNAS = [
    'M0 -6V6M0 -6l4 4M0 0l-4 4',
    'M-3 -6V6M3 -6V6M-3 -3 3 3',
    'M0 -6 4 0 0 6 -4 0Z',
    'M-4 -6 4 6M4 -6 -4 6M-4 0h8',
    'M0 -6V6M-4 -2 0 2 4 -2',
    'M0 6V-6M0 -1-4 -6M0 -1 4 -6',
]

HEART = 'M0 22C-6 15-26 4-26-8-26-18-18-24-10-24-4-24 0-20 0-15 0-20 4-24 10-24 18-24 26-18 26-8 26 4 6 15 0 22Z'
CORONA = 'M-10-14-12-31-5-23 0-36 5-23 12-31 10-14Z'


def pt(r, a):
    return r * math.cos(a), r * math.sin(a)


def f(x):
    return f'{x:.2f}'.rstrip('0').rstrip('.')


def sector(r1, r2, a0, a1):
    x0, y0 = pt(r1, a0); x1, y1 = pt(r2, a0); x2, y2 = pt(r2, a1); x3, y3 = pt(r1, a1)
    return (f'M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}A{r2} {r2} 0 0 1 {f(x2)} {f(y2)}'
            f'L{f(x3)} {f(y3)}A{r1} {r1} 0 0 0 {f(x0)} {f(y0)}Z')


def ala(g):
    """Ala izquierda de dragón (la derecha es su espejo): membrana con tres festones y huesos."""
    membrana = ('M-84 -34C-104 -62-134 -78-164 -74Q-146 -54-160 -28Q-138 -20-144 14'
                'Q-122 12-114 48Q-98 30-86 30Z')
    return (f'<path d="{membrana}" fill="url(#{g("oro")})" stroke="{PLOMO}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<path d="M-86 -24-160 -28M-86 -4-144 14M-86 16-114 48M-84 -34-164 -74" fill="none" '
            f'stroke="{ORO_OSCURO}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M-90 -36C-108 -60-134 -72-158 -71" fill="none" stroke="{ORO_CLARO}" stroke-width="1.6" stroke-linecap="round"/>')


def llave_espada(g):
    """Llave espada en vertical (punta arriba); se gira 45° al colocarla. La punta asoma por encima del
    anillo y la empuñadura por debajo."""
    return (
        f'<rect x="-4" y="-142" width="8" height="244" rx="2" fill="url(#{g("plata")})" stroke="{PLOMO}" stroke-width="2"/>'
        # Dientes de la llave: silueta de corona
        f'<path d="M3 -146H22V-132H16V-138H10V-125H3Z" fill="url(#{g("plata")})" stroke="{PLOMO}" stroke-width="2" stroke-linejoin="round"/>'
        # Guarda redondeada dorada y empuñadura
        f'<rect x="-4.5" y="102" width="9" height="28" rx="2" fill="#2A2F45" stroke="{PLOMO}" stroke-width="1.6"/>'
        f'<rect x="-14" y="99" width="28" height="34" rx="10" fill="none" stroke="{PLOMO}" stroke-width="8.5"/>'
        f'<rect x="-14" y="99" width="28" height="34" rx="10" fill="none" stroke="url(#{g("oro")})" stroke-width="5.5"/>'
        # Llavero
        f'<path d="M0 133V140" stroke="{PLOMO}" stroke-width="1.6"/>'
        f'<path transform="translate(0 147) scale(.28)" d="{HEART}" fill="url(#{g("plata")})" stroke="{PLOMO}" stroke-width="5"/>')


def espada_runica(g):
    """Espada rúnica de WoW en vertical (punta arriba), con runas que brillan en la parte de la hoja que
    asoma por encima del anillo."""
    runas = ''.join(f'<path class="e-runa" style="--i:{i}" transform="translate(0 {y}) scale(.7)" d="{RUNAS[i]}"/>'
                    for i, y in enumerate([-128, -110]))
    return (
        f'<path d="M0 -150 11 -132V90L0 98-11 90V-132Z" fill="url(#{g("acero")})" stroke="{PLOMO}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<g fill="none" stroke="{ARCANO}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" filter="url(#{g("brillo")})">{runas}</g>'
        # Guarda con cuernos, empuñadura y pomo con gema
        f'<path d="M-32 92Q-21 103-8 98H8Q21 103 32 92L25 110H-25Z" fill="#3A4458" stroke="{PLOMO}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M-25 110H25" stroke="url(#{g("oro")})" stroke-width="3"/>'
        f'<rect x="-4.5" y="110" width="9" height="22" rx="2" fill="#2A2F45" stroke="{PLOMO}" stroke-width="1.6"/>'
        f'<circle cy="138" r="7" fill="{ARCANO}" stroke="{PLOMO}" stroke-width="2"/>')


def sharingan(g):
    """Iris rojo, anillo y tres tomoe; la pupila es el corazón de KH con su corona."""
    # Tomoe: cabeza redonda y cola que sigue el anillo
    tomoe = '<circle r="4.6"/><path d="M4.4 -1.4C5 -6 2 -10 -3 -11.5C0 -8.5 .8 -6 -1.5 -4.4Z"/>'
    tres = ''.join(f'<g transform="rotate({a}) translate(0 -18.5) rotate(-90) scale(1.15)">{tomoe}</g>' for a in (60, 180, 300))
    return (
        f'<circle r="30" fill="url(#{g("iris")})" stroke="{PLOMO}" stroke-width="3"/>'
        f'<circle r="18.5" fill="none" stroke="#2A0404" stroke-width="1.8"/>'
        f'<g class="e-tomoe" fill="#140303">{tres}</g>'
        f'<g transform="translate(0 3) scale(.34)">'
        f'<path d="{HEART}" fill="#140303" stroke="#140303" stroke-width="3" stroke-linejoin="round"/>'
        f'<path d="{CORONA}" fill="url(#{g("oro")})" stroke="#140303" stroke-width="4" stroke-linejoin="round"/></g>')


def emblema(animado, pre):
    """pre: prefijo de ids para que no choquen si hay varios en la misma página."""
    g = lambda n: f'{pre}{n}'
    partes = []

    # Alas (detrás de todo) y armas cruzadas detrás del anillo
    partes.append(f'<g class="e-alas">{ala(g)}<g transform="scale(-1 1)">{ala(g)}</g></g>')
    partes.append(f'<g transform="rotate(-45)">{espada_runica(g)}</g>')
    partes.append(f'<g transform="rotate(45)">{llave_espada(g)}</g>')

    # Puntas biseladas arriba y abajo
    puntas = ''.join(
        f'<g transform="rotate({a})"><path d="M0 -122 -16 -88 0 -94Z" fill="{ORO_CLARO}"/>'
        f'<path d="M0 -122 16 -88 0 -94Z" fill="{ORO_OSCURO}"/></g>' for a in (0, 180))
    partes.append(f'<g stroke="{PLOMO}" stroke-width="2.4" stroke-linejoin="round">{puntas}</g>')

    # Anillo de metal con remaches
    partes.append(f'<circle r="96" fill="url(#{g("oro")})" stroke="{PLOMO}" stroke-width="3"/>')
    remaches = ''.join(
        f'<circle cx="{f(pt(93, i * math.tau / 8 + math.pi / 8)[0])}" cy="{f(pt(93, i * math.tau / 8 + math.pi / 8)[1])}" r="2.6"/>'
        for i in range(8))
    partes.append(f'<g fill="#FFF3C4" stroke="{PLOMO}" stroke-width="1.2">{remaches}</g>')

    # Banda de piedra con runas
    runas = ''.join(
        f'<path class="e-runa" style="--i:{i}" transform="rotate({i * 30 + 15}) translate(0 -80.5)" d="{RUNAS[i % len(RUNAS)]}"/>'
        for i in range(12))
    partes.append(
        f'<g class="e-banda"><circle r="89" fill="{PIEDRA}" stroke="{PLOMO}" stroke-width="2"/>'
        f'<g fill="none" stroke="{ARCANO}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" filter="url(#{g("brillo")})">{runas}</g></g>')
    partes.append(f'<circle r="72" fill="none" stroke="url(#{g("oro")})" stroke-width="4"/>')

    # Cimera con gema sobre el anillo
    partes.append(f'<path d="M0 -113 8 -101 0 -89-8 -101Z" fill="url(#{g("gema")})" stroke="{PLOMO}" stroke-width="2.2" stroke-linejoin="round"/>')

    # Vidriera: Alianza y Horda alternas, con medallones de KH
    porciones = 12
    segs = []
    for i in range(porciones):
        a0 = i / porciones * math.tau - math.pi / 2
        a1 = (i + 1) / porciones * math.tau - math.pi / 2
        fondo, claro = ALIANZA if i % 2 == 0 else HORDA
        color = claro if i % 4 in (0, 1) else fondo
        segs.append(f'<path d="{sector(30, 70, a0, a1)}" fill="{color}" fill-opacity="{[0.95, 0.75, 0.85][i % 3]}"/>')
    medallas = ''.join(
        f'<circle cx="{f(pt(51, i * math.tau / 6 - math.pi / 2 + math.tau / 24)[0])}" '
        f'cy="{f(pt(51, i * math.tau / 6 - math.pi / 2 + math.tau / 24)[1])}" r="9.5"/>'
        for i in range(6))
    partes.append(
        f'<g class="e-vidriera"><g stroke="{PLOMO}" stroke-width="2.2" stroke-linejoin="round">{"".join(segs)}</g>'
        f'<g fill="#D9E4FA" stroke="{PLOMO}" stroke-width="2.2">{medallas}</g></g>')

    # Sharingan con el corazón como pupila
    partes.append(sharingan(g))

    defs = f'''<defs>
    <linearGradient id="{g("oro")}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFF1A8"/><stop offset=".35" stop-color="#E8B84A"/><stop offset=".55" stop-color="#8A5A12"/>
      <stop offset=".8" stop-color="#F5CF6A"/><stop offset="1" stop-color="#6E4510"/>
    </linearGradient>
    <linearGradient id="{g("plata")}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#B9C6DE"/><stop offset="1" stop-color="#5E6B88"/>
    </linearGradient>
    <linearGradient id="{g("acero")}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#DCE6F8"/><stop offset=".5" stop-color="#8496BC"/><stop offset="1" stop-color="#3F4C6E"/>
    </linearGradient>
    <radialGradient id="{g("iris")}" r=".62">
      <stop offset="0" stop-color="#FF5A48"/><stop offset=".7" stop-color="#D0141A"/><stop offset="1" stop-color="#7A0A0E"/>
    </radialGradient>
    <linearGradient id="{g("gema")}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF9C8A"/><stop offset=".5" stop-color="#D0141A"/><stop offset="1" stop-color="#5E0508"/>
    </linearGradient>
    <filter id="{g("brillo")}" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>'''

    estilo = ''
    if animado:
        estilo = '''<style>
    .e-banda { animation: e-giro 90s linear infinite reverse; transform-origin: 0 0; }
    .e-vidriera { animation: e-giro 140s linear infinite; transform-origin: 0 0; }
    .e-tomoe { animation: e-giro 9s linear infinite; transform-origin: 0 0; }
    .e-runa { animation: e-late 3.2s ease-in-out infinite; animation-delay: calc(var(--i) * -0.27s); }
    @keyframes e-giro { to { transform: rotate(360deg); } }
    @keyframes e-late { 0%, 100% { opacity: .5; } 50% { opacity: 1; } }
    @media (prefers-reduced-motion: reduce) { .e-banda, .e-vidriera, .e-tomoe, .e-runa { animation: none; } }
  </style>'''

    cuerpo = '\n  '.join(partes)
    return (f'<svg class="emblema" xmlns="http://www.w3.org/2000/svg" viewBox="-172 -152 344 304" role="img" '
            f'aria-label="Emblema con elementos de Kingdom Hearts, World of Warcraft y Naruto">\n'
            f'  {defs}\n  {estilo}\n  {cuerpo}\n</svg>\n')


def main():
    img = RAIZ / 'img'
    img.mkdir(exist_ok=True)
    (img / 'logo.svg').write_text(emblema(False, 'l'), encoding='utf-8')
    (img / 'logo-animado.svg').write_text(emblema(True, 'a'), encoding='utf-8')

    index = RAIZ / 'index.html'
    html = index.read_text(encoding='utf-8')
    nuevo, n = re.subn(r'(<!-- logo:inicio -->).*?(<!-- logo:fin -->)',
                       lambda m: f'{m.group(1)}\n{emblema(True, "h")}    {m.group(2)}', html, flags=re.S)
    if n != 1:
        raise SystemExit('No encuentro <!-- logo:inicio --> y <!-- logo:fin --> en index.html')
    index.write_text(nuevo, encoding='utf-8')
    print('Emblema generado: img/logo.svg, img/logo-animado.svg e index.html')


if __name__ == '__main__':
    main()
