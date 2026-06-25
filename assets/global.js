/* Shak Distributors — minimal theme JS */
(function () {
  'use strict';

  // Mobile nav toggle
  var toggle = document.querySelector('[data-menu-toggle]');
  var nav = document.querySelector('[data-menu]');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') nav.classList.remove('is-open');
    });
  }

  // Live cart count via AJAX add-to-cart (progressive enhancement)
  var countEl = document.querySelector('[data-cart-count]');
  function refreshCount() {
    fetch('/cart.js', { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (c) { if (countEl) countEl.textContent = c.item_count; })
      .catch(function () {});
  }

  document.querySelectorAll('form[action$="/cart/add"], .product-form').forEach(function (form) {
    if (!form.querySelector('[name="add"]')) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('[name="add"]');
      var original = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Adding…'; }
      fetch('/cart/add.js', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      })
        .then(function (r) { return r.json(); })
        .then(function () {
          refreshCount();
          if (btn) { btn.textContent = 'Added ✓'; setTimeout(function () { btn.textContent = original; btn.disabled = false; }, 1400); }
        })
        .catch(function () {
          if (btn) { btn.textContent = original; btn.disabled = false; }
          form.submit();
        });
    });
  });
})();
