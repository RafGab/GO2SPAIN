(function () {
  "use strict";

  var STORAGE_KEY = "acero-pulido-aviso-cookies";

  try {
    if (window.localStorage.getItem(STORAGE_KEY)) return;
  } catch (e) {
    // Sin acceso al almacenamiento (navegación privada, etc.): el aviso se
    // muestra en cada visita, que es el comportamiento seguro.
  }

  var style = document.createElement("style");
  // Colores: primero los de la web actual (ciruela/malva/crema) y, si la página
  // es la de privacidad (que aún usa la paleta anterior), esos como alternativa.
  style.textContent =
    ".ap-cookies { position: fixed; left: 16px; bottom: 16px; z-index: 1000000; width: 420px; max-width: calc(100vw - 32px);" +
    " box-sizing: border-box; padding: 16px 18px; border-radius: 14px; background: var(--cream, var(--paper, #faf5f3));" +
    " color: var(--ink, #2b1a20); border: 1px solid var(--line, #ead9de); box-shadow: 0 18px 40px -16px rgba(58, 29, 44, 0.4);" +
    " font: 400 13.5px/1.5 'Manrope', system-ui, -apple-system, 'Segoe UI', sans-serif; }" +
    ".ap-cookies p { margin: 0; }" +
    ".ap-cookies a { color: var(--mauve, var(--red-700, #8a4a68)); font-weight: 700; }" +
    ".ap-cookies-actions { margin-top: 12px; display: flex; justify-content: flex-end; }" +
    ".ap-cookies button { border: none; border-radius: 999px; padding: 9px 20px; cursor: pointer; font: 700 13.5px/1 inherit;" +
    " font-family: inherit; background: var(--plum, var(--red-800, #3a1d2c)); color: #fff; }" +
    ".ap-cookies button:hover { background: var(--plum-2, var(--red-700, #552a40)); }" +
    ".ap-cookies button:focus-visible, .ap-cookies a:focus-visible { outline: 2px solid var(--mauve, var(--red-700, #8a4a68)); outline-offset: 2px; }" +
    "@media (prefers-reduced-motion: no-preference) { .ap-cookies { animation: ap-cookies-in 0.3s ease-out; } }" +
    "@keyframes ap-cookies-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }" +
    "@media (max-width: 560px) { .ap-cookies { left: 12px; right: 12px; bottom: 12px; width: auto; max-width: none; } }";
  document.head.appendChild(style);

  var banner = document.createElement("div");
  banner.className = "ap-cookies";
  banner.setAttribute("role", "region");
  banner.setAttribute("aria-label", "Aviso de cookies");
  banner.innerHTML =
    "<p>Esta web <strong>no usa cookies de publicidad ni de análisis</strong>. " +
    "Solo guarda en tu navegador lo imprescindible para que el chat y este aviso funcionen. " +
    '<a href="privacidad.html#cookies">Más información</a></p>' +
    '<div class="ap-cookies-actions"><button type="button">Entendido</button></div>';

  banner.querySelector("button").addEventListener("click", function () {
    try {
      window.localStorage.setItem(STORAGE_KEY, "1");
    } catch (e) {}

    banner.remove();
    style.remove();
  });

  document.body.appendChild(banner);
})();
