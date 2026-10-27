// Portada de proyectos: tema y efectos. Sin JS o con movimiento reducido todo se ve quieto y completo.
import { iniciarEstela } from './cursor.js';

const raiz = document.documentElement;
const quietoMQ = matchMedia('(prefers-reduced-motion: reduce)');

// Botón de tema: oscuro por defecto, el claro se recuerda en este navegador.
const boton = document.querySelector('[data-theme-toggle]');
const pintaTema = () => {
  const claro = raiz.dataset.theme === 'light';
  boton.setAttribute('aria-label', claro ? 'Cambiar a tema oscuro' : 'Cambiar a tema claro');
};
boton.addEventListener('click', () => {
  const t = raiz.dataset.theme === 'light' ? 'dark' : 'light';
  raiz.dataset.theme = t;
  try { localStorage.setItem('portada:tema', t); } catch {}
  pintaTema();
});
pintaTema();

if (!quietoMQ.matches) {
  raiz.classList.add('js-anim');
  entradas();
  contadores();
  giroConScroll();
  chispas();
  iniciarEstela();
}
document.addEventListener('pointermove', inclinar, { passive: true });

// Cada bloque sube al entrar en pantalla, escalonado por --k. Se mide en cada scroll (y no con
// IntersectionObserver, que con scroll rápido se saltaba bloques); también enciende lo que ya quedó por encima.
function entradas() {
  let pendientes = [...document.querySelectorAll('.reveal')];
  let programado = false;
  const revisar = () => {
    programado = false;
    const limite = innerHeight - 40;
    pendientes = pendientes.filter((el) => {
      if (el.getBoundingClientRect().top < limite) { el.classList.add('is-in'); return false; }
      return true;
    });
    if (!pendientes.length) removeEventListener('scroll', alScroll);
  };
  const alScroll = () => { if (!programado) { programado = true; requestAnimationFrame(revisar); } };
  addEventListener('scroll', alScroll, { passive: true });
  addEventListener('resize', alScroll);
  revisar();
}

// Las cifras cuentan desde cero la primera vez que se ven.
function contadores() {
  const els = [...document.querySelectorAll('[data-cuenta]')];
  if (!('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver((entradas) => entradas.forEach((e) => {
    if (!e.isIntersecting) return;
    io.unobserve(e.target);
    const fin = Number(e.target.dataset.cuenta);
    const t0 = performance.now();
    const paso = (ahora) => {
      const p = Math.min((ahora - t0) / 1400, 1);
      e.target.textContent = Math.round(fin * (1 - (1 - p) ** 3));
      if (p < 1) requestAnimationFrame(paso);
    };
    requestAnimationFrame(paso);
  }), { threshold: 0.6 });
  els.forEach((el) => io.observe(el));
}

// Las vidrieras giran un poco más al hacer scroll.
function giroConScroll() {
  let pendiente = false;
  const aplicar = () => { raiz.style.setProperty('--giro', `${(scrollY * 0.06).toFixed(2)}deg`); pendiente = false; };
  addEventListener('scroll', () => { if (!pendiente) { pendiente = true; requestAnimationFrame(aplicar); } }, { passive: true });
}

// Inclinación hacia el ratón ([data-tilt]) y luz que sigue al ratón dentro de cada ficha de juego.
let tiltActual = null;
function inclinar(e) {
  if (e.pointerType !== 'mouse' || quietoMQ.matches) return;
  const host = e.target.closest?.('[data-tilt]');
  if (tiltActual && tiltActual !== host) {
    tiltActual.style.removeProperty('--rx'); tiltActual.style.removeProperty('--ry'); tiltActual.classList.remove('is-tilt');
  }
  tiltActual = host;
  if (!host) return;
  const r = host.getBoundingClientRect();
  const x = (e.clientX - r.left) / r.width - 0.5;
  const y = (e.clientY - r.top) / r.height - 0.5;
  host.style.setProperty('--ry', `${(x * 14).toFixed(2)}deg`);
  host.style.setProperty('--rx', `${(-y * 10).toFixed(2)}deg`);
  host.style.setProperty('--mx', `${e.clientX - r.left}px`);
  host.style.setProperty('--my', `${e.clientY - r.top}px`);
  host.classList.add('is-tilt');
}

// Chispas de luz que suben por la portada (estrellas de cuatro puntas con los colores de los juegos).
// Se para cuando la portada no se ve o la pestaña está oculta.
function chispas() {
  const canvas = document.querySelector('.chispas');
  const hero = document.querySelector('.hero');
  if (!canvas || !hero) return;
  const ctx = canvas.getContext('2d');
  let w = 0, h = 0, dpr = 1, visible = true, animando = false, colores = [];
  const lista = [];

  const leerColores = () => {
    const cs = getComputedStyle(raiz);
    colores = ['--gold', '--kh', '--aqua', '--kh3', '--ddd', '--gold'].map((v) => cs.getPropertyValue(v).trim());
  };
  new MutationObserver(leerColores).observe(raiz, { attributes: true, attributeFilter: ['data-theme'] });
  leerColores();

  const nueva = (inicio) => ({
    x: Math.random() * w,
    y: inicio ? Math.random() * h : h + 10,
    r: 1.2 + Math.random() * 2.6,
    v: 0.15 + Math.random() * 0.45,
    deriva: (Math.random() - 0.5) * 0.25,
    fase: Math.random() * Math.PI * 2,
    color: colores[Math.floor(Math.random() * colores.length)],
  });
  const ajustar = () => {
    dpr = Math.min(devicePixelRatio || 1, 2);
    w = hero.clientWidth; h = hero.clientHeight;
    canvas.width = w * dpr; canvas.height = h * dpr;
    const n = Math.round(Math.min(70, w / 18));
    while (lista.length < n) lista.push(nueva(true));
    lista.length = n;
  };
  ajustar();
  addEventListener('resize', ajustar);

  const estrella = (x, y, r) => {
    ctx.beginPath();
    for (let i = 0; i < 8; i++) {
      const rr = i % 2 ? r * 0.3 : r;
      const a = (i / 8) * Math.PI * 2;
      ctx.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr);
    }
    ctx.closePath();
    ctx.fill();
  };
  const dibujar = (t) => {
    if (!visible || document.hidden) { animando = false; return; }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    for (const c of lista) {
      c.y -= c.v; c.x += c.deriva;
      if (c.y < -10) Object.assign(c, nueva(false));
      const brillo = 0.35 + 0.65 * Math.abs(Math.sin(t / 900 + c.fase));
      ctx.globalAlpha = brillo * Math.min(1, c.y / (h * 0.25));
      ctx.fillStyle = c.color;
      ctx.shadowColor = c.color;
      ctx.shadowBlur = c.r * 4;
      estrella(c.x, c.y, c.r * (0.8 + brillo * 0.5));
    }
    requestAnimationFrame(dibujar);
  };
  const arrancar = () => { if (!animando && visible && !document.hidden) { animando = true; requestAnimationFrame(dibujar); } };
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; arrancar(); }).observe(hero);
  document.addEventListener('visibilitychange', arrancar);
  arrancar();
}
