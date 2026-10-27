# DESIGN.md · Portada de Alvaro Portillo

Página principal (`https://alvaroportillo.github.io/`). Solo enlaza a dos sitios: la Guía 100 % de
Kingdom Hearts y mi GitHub. Hereda el sistema de la guía (`kh-guia-100/DESIGN.md`) y sus efectos de
portada (`#/juegos`) para que todo se sienta de la misma casa.

## Idea central
Una portada de Kingdom Hearts a pantalla completa: la **vidriera** de la Estación del Despertar gigante
detrás del **emblema** personal, bajo una aurora con los colores de los juegos y chispas de luz que suben.
Debajo, la guía: las tres colecciones de Steam como puertas sobre otra vidriera, las cifras y lo que tiene
cada juego.

El emblema KH + WoW + Naruto (`notas/logo.py` genera `img/logo.svg`, `img/logo-animado.svg` y el de
`index.html`, entre `<!-- logo:inicio -->` y `<!-- logo:fin -->`): Frostmourne y la Cadena Reino cruzadas,
anillo dorado con remaches y gema roja, banda de runas, vidriera con azul de la Alianza y rojo de la
Horda y sharingan con el corazón de KH en la pupila. Sus colores son fijos (es un logo).

## Paleta (tokens en `:root`)
| Token | Oscuro (por defecto) | Claro | Uso |
|---|---|---|---|
| `--bg` | `#070B1A` | `#EEF2FA` | Fondo |
| `--surface` | `rgba(132,160,255,.07)` | `rgba(255,255,255,.72)` | Paneles translúcidos |
| `--line` | `rgba(170,195,255,.18)` | `rgba(20,32,80,.14)` | Bordes sutiles |
| `--text` | `#ECF0FF` | `#0F1633` | Texto principal |
| `--text-2` | `#AEB9DA` | `#3D4770` | Texto secundario (AA sobre `--bg`) |
| `--gold` | `#EBC765` | `#9A6B00` | Nombre, botón principal, cifras, foco |
| `--kh`, `--kh2fm`, `--kh3`, `--ddd`, `--aqua`, `--ventus`, `--terra` | los de la guía | los de la guía | Aurora, vidrieras, chispas y el tinte de cada ficha de juego (`--tile`) |

El dorado es el único acento de interfaz; los colores de los juegos solo tiñen fondos y fichas.

## Tipografía
- **Cinzel** 900: el nombre, en oro grabado (en claro, oro oscuro sin brillo), y las cifras.
- **Cinzel** 700: títulos de sección y nombres de juego.
- **Sora** (400/600/800): todo lo demás.

## Espaciado y radios
- Escala de 4 px. Margen lateral de 16 px; ancho máximo 1180 px.
- Radios: `--r-s: 10px` · `--r-m: 18px` · `--r-l: 28px` (fichas y cifras). Botones en píldora.

## Movimiento
Todo con `transform`/`opacity` y desactivado con `prefers-reduced-motion` (y sin JS, todo se ve quieto y completo):
- Portada: la aurora deriva (26 s), la vidriera se enciende y gira (160 s, y avanza con el scroll),
  chispas en `<canvas>` (se paran si la portada no se ve), el emblema entra girando, flota y se inclina
  hacia el ratón, y un destello recorre el nombre cada 7 s.
- Colecciones y fichas: logos con relieve que se inclinan hacia el ratón y un destello que los recorre
  (`.logo3d`, igual que la guía); en las fichas, una luz del color del juego sigue al ratón.
- Cada bloque sube al entrar en pantalla, escalonado (`--k`); las cifras cuentan desde cero.
- Cursor: estela de llave espada (`cursor.js`, solo con ratón).
- Botones: brillo que los cruza y la flecha avanza (200 ms).

## Reglas
- Contraste WCAG AA, foco visible (anillo dorado), funciona a 390 px y 1280 px sin scroll lateral.
- Nada de emojis como iconos: SVG en línea.
- Tema oscuro por defecto; el botón de tema cambia a claro y se recuerda en el navegador (`portada:tema`).
