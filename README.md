# alvaroportillo.github.io

Portada con los proyectos web que voy haciendo para mis juegos. Se publica con GitHub Pages en
https://alvaroportillo.github.io/ y cada proyecto cuelga de su propio repo:

- [Guía 100 % de Kingdom Hearts](https://alvaroportillo.github.io/kh-guia-100/) ([código](https://github.com/AlvaroPortillo/kh-guia-100))
- [Project Zomboid](https://alvaroportillo.github.io/ProyectZomboid/), panel de consulta ([código](https://github.com/AlvaroPortillo/ProyectZomboid))

El emblema (Kingdom Hearts + World of Warcraft) está en `img/logo.svg` (estático) e `img/logo-animado.svg`;
se regenera con `python notas/logo.py`.

HTML y CSS sin dependencias ni compilación. Para verla en local:

```sh
python -m http.server 4260   # y abrir http://127.0.0.1:4260
```

El diseño (tokens, tipografía, vidriera) está en `DESIGN.md`, que también explica cómo añadir un proyecto.
