/* ============================================================
   main.js — Sachin Pathare Portfolio
   ============================================================ */

// ---- Navbar: add shadow on scroll ----
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 20);
});

// ---- Mobile hamburger ----
const hamburger = document.getElementById('hamburger');
const navLinks  = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  navLinks.classList.toggle('open');
});

// Close menu when a link is clicked
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navLinks.classList.remove('open');
  });
});

// ---- Intersection Observer: reveal animations ----
const observerOptions = {
  threshold: 0.12,
  rootMargin: '0px 0px -40px 0px'
};

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      // Stagger children of grids
      const delay = entry.target.dataset.delay || 0;
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, delay);
      revealObserver.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe timeline items with staggered delay
document.querySelectorAll('.timeline-item').forEach((el, i) => {
  el.dataset.delay = i * 80;
  revealObserver.observe(el);
});

// Observe skill categories with stagger
document.querySelectorAll('.skill-category').forEach((el, i) => {
  el.dataset.delay = i * 70;
  revealObserver.observe(el);
});

// Observe cert cards with stagger
document.querySelectorAll('.cert-card').forEach((el, i) => {
  el.dataset.delay = i * 100;
  revealObserver.observe(el);
});

// Observe generic data-animate elements
document.querySelectorAll('[data-animate]').forEach((el, i) => {
  el.dataset.delay = el.dataset.delay || i * 60;
  revealObserver.observe(el);
});

// ---- Active nav link highlight on scroll ----
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      navAnchors.forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === `#${id}`);
      });
    }
  });
}, { threshold: 0.4 });

sections.forEach(s => sectionObserver.observe(s));

// ---- Typed text effect in hero title ----
const heroTitle = document.querySelector('.hero-title');
if (heroTitle) {
  const phrases = ['Senior SDET', 'Automation Architect', 'Quality Engineer', 'Test Strategist'];
  let phraseIdx = 0;
  let charIdx = 0;
  let deleting = false;
  let pauseTicks = 0;

  function type() {
    const current = phrases[phraseIdx];
    if (!deleting) {
      heroTitle.textContent = current.slice(0, ++charIdx);
      if (charIdx === current.length) { deleting = true; pauseTicks = 28; }
    } else {
      if (pauseTicks > 0) { pauseTicks--; }
      else {
        heroTitle.textContent = current.slice(0, --charIdx);
        if (charIdx === 0) {
          deleting = false;
          phraseIdx = (phraseIdx + 1) % phrases.length;
        }
      }
    }
    setTimeout(type, deleting && pauseTicks === 0 ? 60 : 110);
  }
  // Small delay before starting
  setTimeout(type, 1200);
}
