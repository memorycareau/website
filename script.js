// MemoryCare — small progressive enhancements. The page works without JS.

(function () {
  const root = document.documentElement;
  root.classList.add('js');

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

  // Feature showcases: accessible tabs that swap the phone screenshot
  document.querySelectorAll('[data-tabs]').forEach((group) => {
    const tabs = Array.from(group.querySelectorAll('[role="tab"]'));

    function select(tab, focus) {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) tab.focus();
    }

    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => select(tab));
      tab.addEventListener('keydown', (e) => {
        const keys = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 };
        if (e.key in keys) {
          e.preventDefault();
          select(tabs[(i + keys[e.key] + tabs.length) % tabs.length], true);
        } else if (e.key === 'Home' || e.key === 'End') {
          e.preventDefault();
          select(tabs[e.key === 'Home' ? 0 : tabs.length - 1], true);
        }
      });
    });

    select(tabs.find((t) => t.getAttribute('aria-selected') === 'true') || tabs[0]);
  });

  // Gentle fade-in as sections scroll into view
  const revealed = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    revealed.forEach((el) => io.observe(el));
  } else {
    revealed.forEach((el) => el.classList.add('is-visible'));
  }

  // Legal pages: contents list starts collapsed on small screens
  const toc = document.querySelector('.toc-details');
  if (toc && window.matchMedia('(max-width: 959px)').matches) toc.open = false;

  // Footer year
  document.getElementById('year').textContent = new Date().getFullYear();
})();
