// MemoryCare — small progressive enhancements. The page works without JS.

(function () {
  const root = document.documentElement;

  // Mobile navigation
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('site-nav');

  function setNav(open) {
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  }

  toggle.addEventListener('click', () => {
    setNav(toggle.getAttribute('aria-expanded') !== 'true');
  });

  nav.addEventListener('click', (e) => {
    if (e.target.closest('a')) setNav(false);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      setNav(false);
      toggle.focus();
    }
  });

  // Larger-text toggle, remembered per visitor
  const sizeBtn = document.querySelector('.text-size-toggle');
  const STORAGE_KEY = 'memorycare-text-large';

  function setLarge(on) {
    root.classList.toggle('text-large', on);
    sizeBtn.setAttribute('aria-pressed', String(on));
    sizeBtn.title = on ? 'Make text smaller' : 'Make text larger';
  }

  try {
    setLarge(localStorage.getItem(STORAGE_KEY) === '1');
  } catch (_) { /* storage unavailable */ }

  sizeBtn.addEventListener('click', () => {
    const on = !root.classList.contains('text-large');
    setLarge(on);
    try { localStorage.setItem(STORAGE_KEY, on ? '1' : '0'); } catch (_) {}
  });

  // Footer year
  document.getElementById('year').textContent = new Date().getFullYear();
})();
