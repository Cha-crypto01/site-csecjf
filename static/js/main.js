/* ============================================================
   CSECJF — script.js
   - Header & footer injectés automatiquement sur chaque page
   - Hero carousel (images + titres)
   - Menu mobile, scroll reveal, compteurs, scroll-top
   ============================================================ */

/* 1) CONFIGURATION */

const SITE_LOGO = "image/shared/Logo-csecjf.png";

const NAV_LINKS = [
  { href: "index.html",         label: "Accueil" },
  { href: "about.html",         label: "À Propos" },
  { href: "services.html",      label: "Services" },
  { href: "achievements.html",  label: "Réalisations" },
  { href: "blog.html",          label: "Blog" },
  { href: "contact.html",       label: "Contact" },
];

const HERO_SLIDES = [
  {
    image: "image/accueil/Centre Socio-Educatif.jpeg",
    eyebrow: "CSECJF Guinaw Rails Sud",
    title: 'Centre Socio-Éducatif et Culturel, <span class="accent">des Jeunes et Femmes</span>.',
    subtitle: "Un espace dédié à l'autonomisation, l'éducation et le développement économique local au cœur de Dakar..",
    ctaPrimary:  { label: "Consulter le BEL",   href: "services.html" },
    ctaSecondary:{ label: "Nous contacter",     href: "contact.html" },
  },
  {
    image: "image/accueil/backround.jpeg",
    eyebrow: "Guinaw Rails Sud",
    title: 'Éduquer, <span class="accent">autonomiser</span>, transformer.',
    subtitle: "Un centre socio-éducatif au service des jeunes et des femmes pour bâtir une économie locale résiliente.",
    ctaPrimary:  { label: "S'inscrire",             href: "contact.html" },
    ctaSecondary:{ label: "Découvrir nos actions",  href: "services.html" },
  },
  {
    image: "image/accueil/Salle de réunion.jpeg",
    eyebrow: "Formation & Emploi",
    title: 'Des compétences pour <span class="accent">les métiers de demain</span>.',
    subtitle: "Cursus certifiants en informatique, gestion, couture et artisanat — 80% d'insertion professionnelle.",
    ctaPrimary:  { label: "Voir les formations",   href: "services.html" },
    ctaSecondary:{ label: "Nos réalisations",      href: "achievements.html" },
  },
  
];


const AUTOPLAY_MS = 6000;

/* 2) HEADER */
function buildHeader() {
  const currentPage = (location.pathname.split('/').pop() || 'index.html').toLowerCase();

  const links = NAV_LINKS.map(l => {
    const active = (l.href.toLowerCase() === currentPage) ? ' class="active"' : '';
    return `<li><a href="${l.href}"${active}>${l.label}</a></li>`;
  }).join('');

  const header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML = `
    <div class="header-container">
      <a href="index.html" class="site-logo" aria-label="CSECJF - Accueil">
        <img src="${SITE_LOGO}" alt="CSECJF Logo" style="height: 3rem; width: auto;">
      </a>
      

      <nav aria-label="Navigation principale">
        <ul class="nav-menu" id="navMenu">${links}</ul>
      </nav>

      <button class="menu-toggle" id="menuToggle" aria-label="Ouvrir le menu" aria-expanded="false">
        <span class="material-symbols-outlined">menu</span>
      </button>
    </div>
  `;

  document.querySelectorAll('header').forEach(h => h.remove());
  document.body.insertBefore(header, document.body.firstChild);

  const toggle = header.querySelector('#menuToggle');
  const menu   = header.querySelector('#navMenu');
  
  // Menu toggle logic
  function toggleMenu() {
    const open = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.querySelector('.material-symbols-outlined').textContent = open ? 'close' : 'menu';
  }
  toggle.addEventListener('click', toggleMenu);
  
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.querySelector('.material-symbols-outlined').textContent = 'menu';
  }));

  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* 3) FOOTER */
function buildFooter() {
  document.querySelectorAll('footer').forEach(f => f.remove());

  const year = new Date().getFullYear();
  const footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.innerHTML = `
    <div class="footer-container">
      <div class="footer-section">
        <div class="footer-brand">CSECJF</div>
        <p>Dispositif de proximité à l'économie locale, au cœur de Guinaw Rails Sud.</p>
      </div>
      <div class="footer-section">
        <h4>Pages</h4>
        ${NAV_LINKS.map(l => `<a href="${l.href}">${l.label}</a>`).join('')}
      </div>
      <div class="footer-section">
        <h4>Ressources</h4>
        <a href="#">Conditions d'utilisation</a>
        <a href="#">Politique de confidentialité</a>
        <a href="#">FAQ</a>
      </div>
      <div class="footer-section">
        <h4>Contact</h4>
        <a href="mailto:contact@csecjf-dakarsud.sn">contact@csecjf-dakarsud.sn</a>
        <a href="tel:+221771396529">+221 77 139 65 29</a>
        <div class="social-row" style="margin-top:1rem;">
          <a href="#" aria-label="Facebook"><span class="material-symbols-outlined">public</span></a>
          <a href="#" aria-label="Instagram"><span class="material-symbols-outlined">photo_camera</span></a>
          <a href="#" aria-label="LinkedIn"><span class="material-symbols-outlined">work</span></a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      © ${year} CSECJF Guinaw Rails Sud. Construit avec passion pour notre communauté.
    </div>
  `;
  document.body.appendChild(footer);
}

/* 4) HERO CAROUSEL */
function buildHeroCarousel() {
  const mount = document.getElementById('heroCarousel');
  if (!mount) return;

  const isHome = (location.pathname.split('/').pop() || 'index.html').toLowerCase() === 'index.html';
  mount.classList.add('hero-carousel');
  if (!isHome) mount.classList.add('is-compact');
  mount.innerHTML = `
    <div class="slides">
      ${HERO_SLIDES.map((s, i) => `
        <div class="hero-slide ${i===0?'is-active':''}" style="background-image:url('${s.image}')" data-index="${i}"></div>
      `).join('')}
    </div>
    <div class="hero-content">
      <span class="hero-eyebrow" id="heroEyebrow">${HERO_SLIDES[0].eyebrow}</span>
      <h1 class="hero-title" id="heroTitle">${HERO_SLIDES[0].title}</h1>
      <p class="hero-subtitle" id="heroSubtitle">${HERO_SLIDES[0].subtitle}</p>
      <div class="hero-cta" id="heroCta">
        <a href="${HERO_SLIDES[0].ctaPrimary.href}" class="btn btn-primary">
          ${HERO_SLIDES[0].ctaPrimary.label}
          <span class="material-symbols-outlined">arrow_forward</span>
        </a>
        <a href="${HERO_SLIDES[0].ctaSecondary.href}" class="btn btn-secondary">
          ${HERO_SLIDES[0].ctaSecondary.label}
        </a>
      </div>
    </div>
    <div class="hero-dots" id="heroDots">
      ${HERO_SLIDES.map((_, i) => `<button class="hero-dot ${i===0?'is-active':''}" data-index="${i}" aria-label="Slide ${i+1}"></button>`).join('')}
    </div>
    <div class="hero-controls">
      <button class="hero-arrow" id="heroPrev" aria-label="Précédent">
        <span class="material-symbols-outlined">arrow_back</span>
      </button>
      <button class="hero-arrow" id="heroNext" aria-label="Suivant">
        <span class="material-symbols-outlined">arrow_forward</span>
      </button>
    </div>
    <div class="hero-stats">
      <div class="stat-card">
        <div class="stat-number">9+</div>
        <div class="stat-label">Années d'impact</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">5+</div>
        <div class="stat-label">Admis par an</div>
      </div>
    </div>
  `;

  const slides  = mount.querySelectorAll('.hero-slide');
  const dots    = mount.querySelectorAll('.hero-dot');
  const eyebrow = mount.querySelector('#heroEyebrow');
  const titleEl = mount.querySelector('#heroTitle');
  const subEl   = mount.querySelector('#heroSubtitle');
  const ctaEl   = mount.querySelector('#heroCta');
  let current = 0;
  let timer;

  function show(i) {
    current = (i + HERO_SLIDES.length) % HERO_SLIDES.length;
    const s = HERO_SLIDES[current];
    slides.forEach((el, k) => el.classList.toggle('is-active', k === current));
    dots.forEach((el, k) => el.classList.toggle('is-active', k === current));

    [eyebrow, titleEl, subEl, ctaEl].forEach(el => {
      el.style.opacity = 0;
      el.style.transform = 'translateY(12px)';
    });
    setTimeout(() => {
      eyebrow.textContent = s.eyebrow;
      titleEl.innerHTML   = s.title;
      subEl.textContent   = s.subtitle;
      ctaEl.innerHTML = `
        <a href="${s.ctaPrimary.href}" class="btn btn-primary">
          ${s.ctaPrimary.label}
          <span class="material-symbols-outlined">arrow_forward</span>
        </a>
        <a href="${s.ctaSecondary.href}" class="btn btn-secondary">
          ${s.ctaSecondary.label}
        </a>`;
      [eyebrow, titleEl, subEl, ctaEl].forEach((el, idx) => {
        setTimeout(() => {
          el.style.transition = 'opacity .6s ease, transform .6s ease';
          el.style.opacity = 1;
          el.style.transform = 'translateY(0)';
        }, idx * 90);
      });
    }, 250);
  }

  const next = () => show(current + 1);
  const prev = () => show(current - 1);
  const startAutoplay = () => { clearInterval(timer); timer = setInterval(next, AUTOPLAY_MS); };
  const stopAutoplay  = () => clearInterval(timer);

  mount.querySelector('#heroNext').addEventListener('click', () => { next(); startAutoplay(); });
  mount.querySelector('#heroPrev').addEventListener('click', () => { prev(); startAutoplay(); });
  dots.forEach(d => d.addEventListener('click', () => {
    show(parseInt(d.dataset.index, 10));
    startAutoplay();
  }));
  mount.addEventListener('mouseenter', stopAutoplay);
  mount.addEventListener('mouseleave', startAutoplay);

  let startX = 0;
  mount.addEventListener('touchstart', e => startX = e.touches[0].clientX, { passive: true });
  mount.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) { dx < 0 ? next() : prev(); startAutoplay(); }
  });

  startAutoplay();
}

/* 5) Scroll-reveal, compteurs, scroll-top, form */
function initReveal() {
  // Select all elements with reveal class or bento cards, etc.
  const els = document.querySelectorAll('.bento-card, section, .card, .stat-card, .grid-2 > div, .grid-3 > div, .grid-4 > div, details.reveal, .reveal');
  
  // Remove duplicates
  const uniqueEls = [...new Set(els)];

  uniqueEls.forEach((el, index) => {
    // Add reveal class if not present
    if (!el.classList.contains('reveal')) {
      el.classList.add('reveal');
    }
    // Add staggered delay for grid items
    if (el.parentElement.classList.contains('grid-2') || el.parentElement.classList.contains('grid-3') || el.parentElement.classList.contains('grid-4')) {
      el.classList.add(`reveal-${(index % 4) + 1}`);
    }
  });
  
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('is-visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
  uniqueEls.forEach(el => io.observe(el));
}

function initTitleScroll() {
  const titles = document.querySelectorAll('.section-title');
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('animate-title');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.2 });
  titles.forEach(t => io.observe(t));
}

function initCounters() {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting || e.target.dataset.counted) return;
      const text = e.target.textContent.trim();
      const match = text.match(/^(\d+)/);
      if (!match) return;
      const target = parseInt(match[1], 10);
      const suffix = text.replace(match[1], '');
      e.target.dataset.counted = '1';
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 60));
      const t = setInterval(() => {
        current += step;
        if (current >= target) { e.target.textContent = target + suffix; clearInterval(t); }
        else e.target.textContent = current + suffix;
      }, 30);
    });
  }, { threshold: 0.4 });
  document.querySelectorAll('.stat-number, [data-count]').forEach(el => io.observe(el));
}

function initScrollTop() {
  const btn = document.createElement('button');
  btn.className = 'scroll-top-btn';
  btn.setAttribute('aria-label', 'Remonter en haut');
  btn.innerHTML = '<span class="material-symbols-outlined">arrow_upward</span>';
  document.body.appendChild(btn);
  window.addEventListener('scroll', () => {
    btn.style.display = window.scrollY > 400 ? 'flex' : 'none';
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

function initSmoothAnchors() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href === '#' || href.length < 2) return;
      const target = document.querySelector(href);
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior:'smooth', block:'start' }); }
    });
  });
}

function initForms() {
  document.querySelectorAll('form:not(#contact-form)').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"], .btn-primary');
      if (!btn) return;
      const original = btn.textContent;
      btn.textContent = 'Message envoyé ✓';
      btn.style.background = '#16a34a';
      form.reset();
      setTimeout(() => { btn.textContent = original; btn.style.background = ''; }, 3000);
    });
  });
}

function initMobileMenu() {
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.nav-menu');
  if (!toggle || !menu) return;
  toggle.addEventListener('click', () => {
    const open = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.querySelector('.material-symbols-outlined').textContent = open ? 'close' : 'menu';
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.querySelector('.material-symbols-outlined').textContent = 'menu';
  }));
}

function initFAQ() {
  document.querySelectorAll('details').forEach(detail => {
    detail.addEventListener('toggle', () => {
      const summary = detail.querySelector('summary');
      if (detail.open) {
        summary.style.color = 'var(--primary)';
        summary.style.fontWeight = '700';
      } else {
        summary.style.color = '';
        summary.style.fontWeight = '';
      }
    });
  });
}

function initFooterActive() {
  const currentPage = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  document.querySelectorAll('footer a, .page-sidebar a').forEach(link => {
    if (link.href.includes(currentPage)) {
      link.classList.add('active');
    }
  });
}

/* 6) Boot */
document.addEventListener('DOMContentLoaded', () => {
  buildHeader();   // header injecté automatiquement
  buildHeroCarousel();
  // buildFooter();   // footer statique utilisé dans chaque page HTML
  initReveal();
  initTitleScroll();
  initCounters();
  initScrollTop();
  initSmoothAnchors();
  initForms();
  initFAQ();
  initFooterActive();
  // UI ready
});
