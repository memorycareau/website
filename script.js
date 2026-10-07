// MemoryCare: small enhancements. Every page works without JavaScript.

(function () {
  const root = document.documentElement;

  // Entrance motion: headings rise word by word, rules draw in, screenshots
  // lift into place. Skipped entirely for prefers-reduced-motion.
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduceMotion && 'IntersectionObserver' in window) {
    root.classList.add('motion');

    // Wrap each word of plain-text headings. Screen readers get the whole
    // heading from aria-label; the word spans are hidden from them.
    document.querySelectorAll('.opening h1, .section-head h2, .limits h2, .download h2, .page-head h1')
      .forEach((heading) => {
        if (heading.children.length) return;
        const text = heading.textContent.trim();
        heading.setAttribute('aria-label', text);
        heading.textContent = '';
        text.split(/\s+/).forEach((word, i, words) => {
          const outer = document.createElement('span');
          const inner = document.createElement('span');
          outer.className = 'word';
          outer.setAttribute('aria-hidden', 'true');
          inner.textContent = word;
          inner.style.setProperty('--i', i);
          outer.appendChild(inner);
          heading.appendChild(outer);
          if (i < words.length - 1) heading.appendChild(document.createTextNode(' '));
        });
        heading.classList.add('split');
      });

    // Stagger siblings in grids and lists
    document.querySelectorAll('.screens, .opening-phones, .qa-grid, .limits-list, .games-list')
      .forEach((group) => {
        Array.from(group.children).forEach((child, i) => child.style.setProperty('--i', i));
      });

    const targets = document.querySelectorAll(
      '.split, .section, .screen, .opening-phones figure, .games-media, .qa, .limits-list li, .games-list'
    );
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach((el) => observer.observe(el));
  }

  // Mobile menu
  const menuButton = document.querySelector('.menu-button');
  const nav = document.getElementById('site-nav');

  function setMenu(open) {
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.textContent = open ? 'Close' : 'Menu';
    nav.classList.toggle('is-open', open);
  }

  menuButton.addEventListener('click', () => {
    setMenu(menuButton.getAttribute('aria-expanded') !== 'true');
  });

  nav.addEventListener('click', (e) => {
    if (e.target.closest('a')) setMenu(false);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      setMenu(false);
      menuButton.focus();
    }
  });

  // Larger text, remembered per visitor
  const sizeButton = document.querySelector('.text-size');
  const STORAGE_KEY = 'memorycare-text-large';

  function setLarge(on) {
    root.classList.toggle('text-large', on);
    sizeButton.setAttribute('aria-pressed', String(on));
  }

  try {
    setLarge(localStorage.getItem(STORAGE_KEY) === '1');
  } catch (_) { /* storage unavailable */ }

  sizeButton.addEventListener('click', () => {
    const on = !root.classList.contains('text-large');
    setLarge(on);
    try { localStorage.setItem(STORAGE_KEY, on ? '1' : '0'); } catch (_) {}
  });

  // Legal pages: contents list starts closed on small screens
  const toc = document.querySelector('.toc-details');
  if (toc && window.matchMedia('(max-width: 59.99rem)').matches) toc.open = false;

  // Footer year
  document.getElementById('year').textContent = new Date().getFullYear();
})();
