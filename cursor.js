// Estela de llave espada que sigue al ratón.
// Solo con ratón (pointer: fine) y si el usuario no ha pedido reducir el movimiento.
// El bucle de animación se detiene cuando no queda nada que dibujar.

const VIDA_ESTELA = 260; // ms que tarda en desvanecerse un punto de la estela
const VIDA_CHISPA = 520;

export function iniciarEstela() {
  const finoMQ = matchMedia('(pointer: fine)');
  const quietoMQ = matchMedia('(prefers-reduced-motion: reduce)');
  if (!finoMQ.matches || quietoMQ.matches) return;

  const canvas = document.createElement('canvas');
  canvas.className = 'estela';
  canvas.setAttribute('aria-hidden', 'true');
  document.body.append(canvas);
  const ctx = canvas.getContext('2d');

  let dpr = 1;
  function ajustar() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = innerWidth * dpr;
    canvas.height = innerHeight * dpr;
  }
  ajustar();
  addEventListener('resize', ajustar);

  const puntos = [];
  const chispas = [];
  let cabeza = null; // posición suavizada de la llave espada
  let angulo = -Math.PI / 4;
  let raton = null;
  let animando = false;
  let colores = leerColores();

  function leerColores() {
    const cs = getComputedStyle(document.documentElement);
    return { oro: cs.getPropertyValue('--gold').trim() || '#EBC765', acento: cs.getPropertyValue('--aqua').trim() || '#63C9FF' };
  }
  new MutationObserver(() => { colores = leerColores(); })
    .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse') return;
    const ahora = performance.now();
    raton = { x: e.clientX, y: e.clientY };
    puntos.push({ ...raton, t: ahora });
    if (Math.random() < 0.35) {
      chispas.push({
        x: e.clientX + (Math.random() - 0.5) * 10,
        y: e.clientY + (Math.random() - 0.5) * 10,
        vx: (Math.random() - 0.5) * 0.04,
        vy: 0.02 + Math.random() * 0.03,
        r: 1.5 + Math.random() * 2,
        t: ahora,
      });
    }
    if (!animando) { animando = true; requestAnimationFrame(dibujar); }
  }, { passive: true });

  document.documentElement.addEventListener('pointerleave', () => { raton = null; });

  function estrella(x, y, r, alpha) {
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    for (let i = 0; i < 8; i++) {
      const rr = i % 2 ? r * 0.35 : r;
      const a = (i / 8) * Math.PI * 2;
      ctx.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr);
    }
    ctx.closePath();
    ctx.fill();
  }

  // Llave espada simplificada: dientes en la punta, hoja, guarda y empuñadura.
  function llave(x, y, ang) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(ang);
    ctx.globalAlpha = 1;
    ctx.fillStyle = colores.oro;
    ctx.strokeStyle = 'rgba(5,8,22,.85)';
    ctx.lineWidth = 1.2;
    // dientes (en el extremo que toca el cursor)
    ctx.beginPath();
    ctx.rect(-1, -5.5, 3, 11);
    ctx.rect(2, -5.5, 4, 3);
    ctx.rect(2, 1.5, 3, 3);
    ctx.fill(); ctx.stroke();
    // hoja
    ctx.fillRect(2, -1.2, 16, 2.4);
    ctx.strokeRect(2, -1.2, 16, 2.4);
    // guarda en forma de corona
    ctx.beginPath();
    ctx.moveTo(18, -6); ctx.lineTo(21, -3); ctx.lineTo(18, 0); ctx.lineTo(21, 3); ctx.lineTo(18, 6);
    ctx.lineTo(23, 6); ctx.lineTo(23, -6); ctx.closePath();
    ctx.fill(); ctx.stroke();
    // empuñadura
    ctx.fillStyle = colores.acento;
    ctx.fillRect(23, -1.6, 6, 3.2);
    ctx.strokeRect(23, -1.6, 6, 3.2);
    ctx.restore();
  }

  function dibujar() {
    const ahora = performance.now();
    while (puntos.length && ahora - puntos[0].t > VIDA_ESTELA) puntos.shift();
    while (chispas.length && ahora - chispas[0].t > VIDA_CHISPA) chispas.shift();

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, innerWidth, innerHeight);

    // Estela: segmentos que adelgazan y se apagan con la edad.
    ctx.lineCap = 'round';
    ctx.strokeStyle = colores.oro;
    ctx.shadowColor = colores.oro;
    ctx.shadowBlur = 8;
    for (let i = 1; i < puntos.length; i++) {
      const vida = 1 - (ahora - puntos[i].t) / VIDA_ESTELA;
      ctx.globalAlpha = Math.max(vida, 0) * 0.7;
      ctx.lineWidth = 1 + vida * 3;
      ctx.beginPath();
      ctx.moveTo(puntos[i - 1].x, puntos[i - 1].y);
      ctx.lineTo(puntos[i].x, puntos[i].y);
      ctx.stroke();
    }

    ctx.fillStyle = colores.oro;
    for (const c of chispas) {
      const edad = ahora - c.t;
      estrella(c.x + c.vx * edad, c.y + c.vy * edad, c.r, Math.max(1 - edad / VIDA_CHISPA, 0));
    }
    ctx.shadowBlur = 0;

    // La llave espada sigue al cursor con un poco de retraso y se orienta hacia él.
    if (raton) {
      if (!cabeza) cabeza = { x: raton.x + 18, y: raton.y + 18 };
      const objetivo = { x: raton.x + 14, y: raton.y + 16 };
      const dx = objetivo.x - cabeza.x;
      const dy = objetivo.y - cabeza.y;
      cabeza.x += dx * 0.35;
      cabeza.y += dy * 0.35;
      if (Math.hypot(dx, dy) > 0.6) {
        // Giro por el camino más corto para que no dé vueltas completas.
        const delta = Math.atan2(Math.sin(Math.atan2(-dy, -dx) - angulo), Math.cos(Math.atan2(-dy, -dx) - angulo));
        angulo += delta * 0.15;
      }
      llave(cabeza.x, cabeza.y, angulo);
    }

    const quieto = raton && cabeza && Math.hypot(raton.x + 14 - cabeza.x, raton.y + 16 - cabeza.y) < 0.5;
    if (puntos.length || chispas.length || (raton && !quieto)) requestAnimationFrame(dibujar);
    else animando = false;
  }
}
