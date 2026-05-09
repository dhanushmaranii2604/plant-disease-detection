/* main.js — Plant Disease Detection */
document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss flash alerts after 5s ──────────────────
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity .5s';
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 500);
    }, 5000);
  });

  // ── Active nav link ──────────────────────────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === path) link.classList.add('active');
  });

  // ── Navbar scroll effect ─────────────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('shadow-lg', window.scrollY > 40);
    });
  }

  // ── Loading spinner on form submit ───────────────────────
  const predictForm = document.getElementById('predictForm');
  if (predictForm) {
    predictForm.addEventListener('submit', function () {
      const btn = document.getElementById('submitBtn');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analysing...';
      }
    });
  }

});
