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

  // Contact form: friendly UX while submitting to Formspree,
  // and report the lead to Google Ads before the page navigates away
  const form = document.getElementById('contactForm');
  if (form) {
    let conversionSent = false;
    form.addEventListener('submit', (e) => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.dataset.original = btn.textContent;
        btn.textContent = 'Sending…';
        btn.disabled = true;
      }
      if (conversionSent || typeof gtag !== 'function') return;
      e.preventDefault();
      conversionSent = true;
      const proceed = () => form.submit();
      const fallback = setTimeout(proceed, 700);
      gtag('event', 'conversion', {
        'send_to': 'AW-18194038866/T-GhCNTM9cocENKAzOND',
        'event_callback': () => { clearTimeout(fallback); proceed(); }
      });
    });
  }
})();
