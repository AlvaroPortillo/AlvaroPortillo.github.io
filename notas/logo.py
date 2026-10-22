"""Genera el emblema Kingdom Hearts + World of Warcraft + Naruto.

- img/logo.svg          estático (para enlazarlo o usarlo como imagen)
- img/logo-animado.svg  animado (runas y vidriera girando, runas que laten, tomoe del sharingan girando)
- index.html            mete el animado entre <!-- logo:inicio --> y <!-- logo:fin -->

Capas, de atrás adelante:
- Colgando del anillo, abiertas en V: la llave espada (KH) y la espada de Arthas al estilo Frostmourne
  (WoW): hoja dentada con runas, guarda con cuernos y calavera de ojos azules.
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


def llave_espada(g):
    """Cadena Reino en vertical (punta arriba). Origen en el centro del emblema: la punta y los dientes
    asoman por encima del anillo y la guarda en cesta, el puño y el llavero por debajo."""
    return (
        # Varilla plateada con remate redondo en la punta
        f'<rect x="-5.5" y="-156" width="11" height="262" rx="5.5" fill="url(#{g("plata")})" stroke="{PLOMO}" stroke-width="2.4"/>'
        # Dientes: corona de tres puntas mirando hacia fuera
        f'<path d="M5 -160H20L34 -168 28 -152 40 -144 28 -136 34 -120 20 -128H5Z" '
        f'fill="url(#{g("plata")})" stroke="{PLOMO}" stroke-width="2.4" stroke-linejoin="round"/>'
        # Puño negro y guarda dorada en cesta, que envuelve la mano
        f'<rect x="-5" y="108" width="10" height="30" rx="3" fill="#1C2033" stroke="{PLOMO}" stroke-width="1.8"/>'
        f'<path d="M-6 104C-24 104-26 112-26 122-26 134-20 142-8 142H8C20 142 26 134 26 122 26 112 24 104 6 104" '
        f'fill="none" stroke="{PLOMO}" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M-6 104C-24 104-26 112-26 122-26 134-20 142-8 142H8C20 142 26 134 26 122 26 112 24 104 6 104" '
        f'fill="none" stroke="url(#{g("oro")})" stroke-width="6.5" stroke-linecap="round"/>'
        f'<rect x="-9" y="99" width="18" height="8" rx="3" fill="url(#{g("oro")})" stroke="{PLOMO}" stroke-width="2"/>'
        # Llavero con cabeza de Mickey (tres círculos)
        f'<path d="M0 142V154" stroke="#C9D3E6" stroke-width="2" stroke-dasharray="2.5 1.5"/>'
        f'<g fill="url(#{g("plata")})" stroke="{PLOMO}" stroke-width="1.8">'
        f'<circle cy="162" r="6.5"/><circle cx="-6.5" cy="155" r="4"/><circle cx="6.5" cy="155" r="4"/></g>')


def espada_arthas(g):
    """Frostmourne en vertical (punta arriba). Origen en el centro del emblema: la punta asoma por
    encima del anillo y la guarda (calavera con cuernos), el puño y el pomo por debajo."""
    # Hoja ancha con el filo dentado en sierra: se estrecha hacia la punta
    derecha = []
    for y in range(-142, 96, 20):
        w = 7 + (y + 160) / 256 * 10
        derecha += [(w + 3, y), (w - 2, y + 8)]
    pts = [(0, -170)] + derecha + [(15, 100)]
    pts += [(-x, y) for x, y in reversed(pts[1:])]
    hoja = 'M' + ' '.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z'
    runas = ''.join(f'<path class="e-runa" style="--i:{i}" transform="translate(0 {y}) scale(.6)" d="{RUNAS[i % len(RUNAS)]}"/>'
                    for i, y in enumerate([-140, -120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80]))
    cuerno = 'M9 110C24 114 40 108 46 88 49 78 46 68 40 62 41 78 34 94 10 100Z'
    return (
        f'<path d="{hoja}" fill="url(#{g("acero")})" stroke="{PLOMO}" stroke-width="2.2" stroke-linejoin="round"/>'
        # Canaladura central oscura con las runas
        f'<rect x="-4.5" y="-150" width="9" height="244" rx="4.5" fill="#26324E" fill-opacity=".85"/>'
        f'<g fill="none" stroke="{ARCANO}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" filter="url(#{g("brillo")})">{runas}</g>'
        # Cuernos de la guarda, curvados hacia la hoja
        f'<g fill="url(#{g("acero")})" stroke="{PLOMO}" stroke-width="2.2" stroke-linejoin="round">'
        f'<path d="{cuerno}"/><path transform="scale(-1 1)" d="{cuerno}"/></g>'
        # Calavera con ojos azules
        f'<path d="M0 94C-12 94-15 101-15 108-15 114-11 117-9 118V125H9V118C11 117 15 114 15 108 15 101 12 94 0 94Z" '
        f'fill="#DDE2EC" stroke="{PLOMO}" stroke-width="2" stroke-linejoin="round"/>'
        f'<g fill="{ARCANO}" stroke="{PLOMO}" stroke-width="1.2" filter="url(#{g("brillo")})">'
        f'<path d="M-9 106-2 107-3 112-8 111Z"/><path d="M9 106 2 107 3 112 8 111Z"/></g>'
        f'<path d="M-4 125V120M0 125V120M4 125V120" stroke="{PLOMO}" stroke-width="1.2"/>'
        # Puño forrado y pomo con pinchos
        f'<rect x="-5" y="125" width="10" height="28" rx="2" fill="#2A2F45" stroke="{PLOMO}" stroke-width="1.8"/>'
        f'<path d="M-5 131 5 135M-5 138 5 142M-5 145 5 149" stroke="#5E6886" stroke-width="1.5"/>'
        f'<path d="M0 152 6 157 13 156 8 162 10 169 3 166 0 173-3 166-10 169-8 162-13 156-6 157Z" '
        f'fill="url(#{g("acero")})" stroke="{PLOMO}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<circle cy="162" r="3.2" fill="{ARCANO}" stroke="{PLOMO}" stroke-width="1"/>')


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

    # Armas cruzadas detrás del anillo: Frostmourne con la punta arriba a la izquierda y la Cadena Reino
    # arriba a la derecha; sus guardas asoman abajo
    partes.append(f'<g transform="rotate(-45) scale(1.1)">{espada_arthas(g)}</g>')
    partes.append(f'<g transform="rotate(45) scale(1.1)">{llave_espada(g)}</g>')

    # Puntas biseladas arriba (bajo la cimera) y abajo
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
    return (f'<svg class="emblema" xmlns="http://www.w3.org/2000/svg" viewBox="-174 -174 348 348" role="img" '
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
