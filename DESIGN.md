# DESIGN.md · Portada de proyectos de Alvaro Portillo

Página principal (`https://alvaroportillo.github.io/`) que enlaza las webs de juegos que voy haciendo.
Hereda el sistema de la Guía 100 % de Kingdom Hearts (`kh-guia-100/DESIGN.md`) para que todo se
sienta de la misma casa, pero sin los logos de la guía.

## Idea central
El **emblema Kingdom Hearts + World of Warcraft + Naruto** es el elemento memorable (`notas/logo.py`
genera `img/logo.svg`, `img/logo-animado.svg` y el de la cabecera). De atrás adelante:
- Alas de dragón doradas con bisel (filigrana de los marcos de la interfaz de WoW).
- Espada rúnica de WoW con runas que brillan y llave espada de KH, cruzadas detrás del anillo.
- Puntas biseladas, anillo de metal dorado con remaches y cimera con gema roja (WoW).
- Banda de piedra con runas arcanas que laten (la piedra de hogar). Glifos inventados.
- Vidriera de la Estación del Despertar (KH) con el azul de la Alianza y el rojo de la Horda.
- Sharingan (Naruto) con tres tomoe; la pupila es el corazón con la corona de KH.

Animado: la banda gira a un lado (90 s), la vidriera al otro (140 s), las runas laten y los tomoe del
sharingan giran (9 s). Con `prefers-reduced-motion` se queda quieto. Los colores del emblema son fijos (es un logo),
no cambian con el tema. Todo lo demás es sobrio: texto alineado a la izquierda, mucho aire y una fila
ancha por proyecto con su captura.

## Paleta (tokens en `:root`)
| Token | Oscuro (por defecto) | Claro | Uso |
|---|---|---|---|
| `--bg` | `#070B1A` | `#EEF2FA` | Fondo |
| `--surface` | `rgba(132,160,255,.07)` | `rgba(255,255,255,.72)` | Paneles translúcidos |
| `--line` | `rgba(170,195,255,.18)` | `rgba(20,32,80,.14)` | Bordes sutiles |
| `--text` | `#ECF0FF` | `#0F1633` | Texto principal |
| `--text-2` | `#AEB9DA` | `#3D4770` | Texto secundario (AA sobre `--bg`) |
| `--gold` | `#EBC765` | `#9A6B00` | Nombre, foco de teclado |
| `--kh` | `#6FA8FF` | `#1F55B8` | Acento de la guía de Kingdom Hearts (azul de `--khfm`) |
| `--pz` | `#FFB547` | `#8A4D00` | Acento de Project Zomboid (ámbar `--sodium` de su panel) |

Cada proyecto define `--accent` con su color. Máximo dos acentos visibles a la vez
(`--accent` + `--gold`). Los botones llevan texto `--on-accent` (oscuro en tema oscuro, blanco en claro).

## Tipografía
- **Cinzel** 900 para el nombre, en oro grabado con bandas de metal y un leve brillo arcano (rótulos de
  WoW). En tema claro, oro oscuro sin brillo para mantener el contraste.
- **Cinzel** 700: el nombre de cada proyecto.
- **Sora** (400/600/800): todo lo demás.
- Escala 1.25 (igual que la guía). Cuerpo 1rem/1.6. Líneas ≤ 62 caracteres.

## Espaciado y radios
- Escala de 4 px: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 72 · 112. Margen lateral de 16 px en móvil.
- Radios: `--r-s: 10px` (chips) · `--r-m: 18px` (capturas) · `--r-l: 28px` (marco del proyecto).

## Movimiento
- Un único momento orquestado: el emblema animado y el texto de cabecera que sube al cargar.
- Al pasar sobre un proyecto, su marco toma el color del proyecto (200 ms, `cubic-bezier(.2,.7,.2,1)`).
- `prefers-reduced-motion`: sin giro ni transiciones.

## Reglas
- Contraste WCAG AA, foco visible (anillo dorado), funciona a 390 px y 1280 px.
- Nada de emojis como iconos: SVG en línea.
- Tema oscuro por defecto; el botón de tema cambia a claro y se recuerda en el navegador.

## Añadir un proyecto
1. Captura a 1440 × 900 (tema oscuro), convertida a WebP de 1200 × 750 en `img/<repo>.webp`.
2. Copiar un `<article class="project">` en `index.html` y darle su `--accent` en `styles.css`.
