# alvaroportillo.github.io

Portada personal, centrada en la [Guía 100 % de Kingdom Hearts](https://alvaroportillo.github.io/kh-guia-100/)
([código](https://github.com/AlvaroPortillo/kh-guia-100)). Se publica con GitHub Pages en https://alvaroportillo.github.io/.

El emblema (Kingdom Hearts + World of Warcraft + Naruto) está en `img/logo.svg` (estático) e `img/logo-animado.svg`;
se regenera con `python notas/logo.py`, que también lo mete en `index.html`.

HTML, CSS y JS con módulos ES, sin dependencias ni compilación. Por los módulos, en local hay que servirla
(abrir `index.html` como archivo no carga los efectos):

```sh
python -m http.server 4260   # y abrir http://127.0.0.1:4260
```

- `main.js`: tema, chispas de la portada, inclinación hacia el ratón, entradas al hacer scroll y contadores.
- `cursor.js`: estela de llave espada, copia de `kh-guia-100/src/cursor.js`.
- `img/logos/`: logos de las colecciones y de los juegos, copiados de `kh-guia-100/assets/img/logos/`.

El diseño (tokens, tipografía, efectos) está en `DESIGN.md`.
