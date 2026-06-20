// FlowProHVAC — shared scripts
(function () {
  const menuBtn = document.querySelector('.menu-btn');
  const nav = document.querySelector('nav.primary');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      nav.classList.toggle('open');
      menuBtn.textContent = nav.classList.contains('open') ? '✕' : '☰';
    });
  }

  // Contact form: friendly UX while submitting to Formspree
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.dataset.original = btn.textContent;
        btn.textContent = 'Sending…';
        btn.disabled = true;
      }
    });
  }
})();
