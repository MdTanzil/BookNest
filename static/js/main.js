document.addEventListener('DOMContentLoaded', function () {
  initQuantityButtons();
  initAutoDismissAlerts();
  initImageZoom();
  initConfirmActions();
  initStickyNavbar();
  initAutoSubmitFilters();
  initCartTotalUpdate();
  initWishlistToggle();
  initBackToTop();
  initStarRating();
  initSmoothScroll();
});

function initQuantityButtons() {
  var buttons = document.querySelectorAll('[data-action]');

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var action = btn.getAttribute('data-action');
      if (action !== 'inc' && action !== 'dec') return;

      var input = btn.parentElement.querySelector('[data-field="quantity"]');
      if (!input) return;

      var currentVal = parseInt(input.value, 10);
      if (isNaN(currentVal)) currentVal = 1;

      var max = parseInt(input.getAttribute('data-max'), 10);
      var min = parseInt(input.getAttribute('data-min'), 10);
      if (isNaN(min)) min = 1;

      if (action === 'inc') {
        if (isNaN(max) || currentVal < max) {
          input.value = currentVal + 1;
        }
      } else if (action === 'dec') {
        if (currentVal > min) {
          input.value = currentVal - 1;
        }
      }

      var event = new Event('change', { bubbles: true });
      input.dispatchEvent(event);
      updateCartTotal();
    });
  });

  var qtyInputs = document.querySelectorAll('[data-field="quantity"]');
  qtyInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      var val = parseInt(input.value, 10);
      var min = parseInt(input.getAttribute('data-min'), 10);
      var max = parseInt(input.getAttribute('data-max'), 10);
      if (isNaN(min)) min = 1;

      if (isNaN(val) || val < min) {
        input.value = min;
      } else if (!isNaN(max) && val > max) {
        input.value = max;
      }
      updateCartTotal();
    });
  });
}

function initAutoDismissAlerts() {
  var alerts = document.querySelectorAll('.alert[data-auto-dismiss="true"], .alert:not([data-auto-dismiss])');

  alerts.forEach(function (alert) {
    if (alert.getAttribute('data-auto-dismiss') === 'false') return;

    var closeBtn = alert.querySelector('.btn-close, [data-bs-dismiss="alert"]');
    if (!closeBtn) return;

    setTimeout(function () {
      if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
        var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      } else {
        closeBtn.click();
      }
    }, 4000);
  });
}

function initImageZoom() {
  var containers = document.querySelectorAll('.img-zoom-container');

  containers.forEach(function (container) {
    var img = container.querySelector('img');
    var lens = container.querySelector('.img-zoom-lens');
    var result = container.querySelector('.img-zoom-result');
    if (!img) return;

    if (lens || result) {
      setupZoomWithLens(container, img, lens, result);
    }
  });

  var zoomImages = document.querySelectorAll('[data-zoomable="true"]');
  zoomImages.forEach(function (img) {
    if (!img.closest('.img-zoom-container')) {
      var wrapper = document.createElement('div');
      wrapper.className = 'img-zoom-container position-relative d-inline-block';
      img.parentNode.insertBefore(wrapper, img);
      wrapper.appendChild(img);

      var lens = document.createElement('div');
      lens.className = 'img-zoom-lens';
      wrapper.appendChild(lens);

      var result = document.createElement('div');
      result.className = 'img-zoom-result';
      wrapper.appendChild(result);

      setupZoomWithLens(wrapper, img, lens, result);
    }
  });
}

function setupZoomWithLens(container, img, lens, result) {
  var zoomLevel = 2.5;

  function getCursorPos(e) {
    var rect = img.getBoundingClientRect();
    var x = e.clientX - rect.left;
    var y = e.clientY - rect.top;

    var scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    x = e.pageX - (rect.left + scrollLeft) + scrollLeft;
    y = e.pageY - (rect.top + scrollTop) + scrollTop;

    return { x: x, y: y };
  }

  function moveLens(e) {
    e.preventDefault();
    if (!img.offsetWidth || !img.offsetHeight) return;

    var pos = getCursorPos(e);
    var lensWidth = lens ? lens.offsetWidth : 100;
    var lensHeight = lens ? lens.offsetHeight : 100;

    var x = pos.x - lensWidth / 2;
    var y = pos.y - lensHeight / 2;

    if (x > img.width - lensWidth) x = img.width - lensWidth;
    if (x < 0) x = 0;
    if (y > img.height - lensHeight) y = img.height - lensHeight;
    if (y < 0) y = 0;

    if (lens) {
      lens.style.left = x + 'px';
      lens.style.top = y + 'px';
    }

    if (result) {
      var cx = result.offsetWidth / (lensWidth || 100);
      var cy = result.offsetHeight / (lensHeight || 100);

      result.style.backgroundImage = "url('" + img.src + "')";
      result.style.backgroundSize = (img.width * cx) + 'px ' + (img.height * cy) + 'px';
      result.style.backgroundPosition = '-' + (x * cx) + 'px -' + (y * cy) + 'px';
    }
  }

  img.addEventListener('mousemove', moveLens);
  if (lens) lens.addEventListener('mousemove', moveLens);

  img.addEventListener('mouseenter', function () {
    if (lens) lens.style.opacity = '1';
    if (result) {
      result.style.opacity = '1';
      result.style.visibility = 'visible';
    }
  });

  container.addEventListener('mouseleave', function () {
    if (lens) lens.style.opacity = '0';
    if (result) {
      result.style.opacity = '0';
      result.style.visibility = 'hidden';
    }
  });
}

function initConfirmActions() {
  var confirmElements = document.querySelectorAll('[data-confirm]');

  confirmElements.forEach(function (el) {
    el.addEventListener('click', function (e) {
      var message = el.getAttribute('data-confirm') || 'Are you sure?';
      if (!confirm(message)) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
    });
  });
}

function initStickyNavbar() {
  var navbar = document.querySelector('.navbar');
  if (!navbar) return;

  function handleScroll() {
    if (window.scrollY > 20) {
      navbar.classList.add('shadow');
    } else {
      navbar.classList.remove('shadow');
    }
  }

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

function initAutoSubmitFilters() {
  var filters = document.querySelectorAll('.auto-submit-filter');

  filters.forEach(function (filter) {
    var eventName = filter.tagName === 'SELECT' ? 'change' : 'change';
    filter.addEventListener(eventName, function () {
      var form = filter.closest('form');
      if (form) {
        clearTimeout(window._filterSubmitTimeout);
        window._filterSubmitTimeout = setTimeout(function () {
          form.submit();
        }, 300);
      }
    });
  });
}

function initCartTotalUpdate() {
  updateCartTotal();

  var cartQtyInputs = document.querySelectorAll('.cart-table [data-field="quantity"], .cart-items [data-field="quantity"]');
  cartQtyInputs.forEach(function (input) {
    input.addEventListener('input', updateCartTotal);
    input.addEventListener('change', updateCartTotal);
  });
}

function updateCartTotal() {
  var rows = document.querySelectorAll('.cart-item-row, [data-cart-item]');
  if (rows.length === 0) return;

  var subtotal = 0;

  rows.forEach(function (row) {
    var qtyInput = row.querySelector('[data-field="quantity"]');
    var priceEl = row.querySelector('[data-price]');
    var subtotalEl = row.querySelector('[data-item-subtotal]');

    var qty = qtyInput ? parseInt(qtyInput.value, 10) : 1;
    if (isNaN(qty)) qty = 1;

    var price = 0;
    if (priceEl) {
      price = parseFloat(priceEl.getAttribute('data-price'));
      if (isNaN(price)) {
        var priceText = priceEl.textContent.replace(/[^0-9.]/g, '');
        price = parseFloat(priceText);
      }
    }

    if (isNaN(price)) price = 0;

    var itemTotal = qty * price;

    if (subtotalEl) {
      subtotalEl.textContent = formatCurrency(itemTotal);
    }

    subtotal += itemTotal;
  });

  var subtotalDisplay = document.querySelector('[data-cart-subtotal]');
  var totalDisplay = document.querySelector('[data-cart-total]');

  if (subtotalDisplay) {
    subtotalDisplay.textContent = formatCurrency(subtotal);
  }

  if (totalDisplay) {
    var shippingEl = document.querySelector('[data-shipping-cost]');
    var taxEl = document.querySelector('[data-tax-amount]');
    var discountEl = document.querySelector('[data-discount-amount]');

    var shipping = shippingEl ? parseFloat(shippingEl.getAttribute('data-shipping-cost')) || 0 : 0;
    var tax = taxEl ? parseFloat(taxEl.getAttribute('data-tax-amount')) || 0 : 0;
    var discount = discountEl ? parseFloat(discountEl.getAttribute('data-discount-amount')) || 0 : 0;

    if (taxEl && !taxEl.getAttribute('data-tax-amount')) {
      var taxRate = parseFloat(taxEl.getAttribute('data-tax-rate')) || 0;
      tax = subtotal * (taxRate / 100);
      taxEl.textContent = formatCurrency(tax);
    }

    var total = subtotal + shipping + tax - discount;
    totalDisplay.textContent = formatCurrency(total);
  }
}

function formatCurrency(amount) {
  var currency = document.body.getAttribute('data-currency') || '$';
  return currency + amount.toFixed(2);
}

function initWishlistToggle() {
  var wishlistBtns = document.querySelectorAll('[data-wishlist-toggle]');

  wishlistBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();

      var icon = btn.querySelector('i');
      if (icon) {
        if (icon.classList.contains('far')) {
          icon.classList.remove('far');
          icon.classList.add('fas');
          btn.classList.add('active');
        } else if (icon.classList.contains('fas')) {
          icon.classList.remove('fas');
          icon.classList.add('far');
          btn.classList.remove('active');
        }
      }

      var bookId = btn.getAttribute('data-wishlist-toggle') || btn.getAttribute('data-book-id');
      if (bookId) {
        var event = new CustomEvent('wishlistToggle', {
          detail: { bookId: bookId, action: btn.classList.contains('active') ? 'add' : 'remove' }
        });
        document.dispatchEvent(event);
      }
    });
  });
}

function initBackToTop() {
  var btn = document.querySelector('.back-to-top');

  if (!btn) {
    btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'back-to-top';
    btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    btn.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(btn);
  }

  function toggleVisibility() {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }

  window.addEventListener('scroll', toggleVisibility, { passive: true });
  toggleVisibility();

  btn.addEventListener('click', function () {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

function initStarRating() {
  var ratingInputs = document.querySelectorAll('.star-rating-input');

  ratingInputs.forEach(function (container) {
    var stars = container.querySelectorAll('i');
    var hiddenInput = container.querySelector('input[type="hidden"]');

    stars.forEach(function (star, index) {
      star.addEventListener('click', function () {
        var value = stars.length - index;

        stars.forEach(function (s, i) {
          if (i >= index) {
            s.classList.add('active');
          } else {
            s.classList.remove('active');
          }
        });

        if (hiddenInput) {
          hiddenInput.value = value;
          var event = new Event('change', { bubbles: true });
          hiddenInput.dispatchEvent(event);
        }

        var ratingEvent = new CustomEvent('ratingSelected', {
          detail: { value: value, element: container }
        });
        document.dispatchEvent(ratingEvent);
      });

      star.addEventListener('mouseenter', function () {
        stars.forEach(function (s, i) {
          if (i >= index) {
            s.style.color = '#FFB800';
            s.style.transform = 'scale(1.1)';
          } else {
            s.style.color = '#E0D3C8';
            s.style.transform = 'scale(1)';
          }
        });
      });
    });

    container.addEventListener('mouseleave', function () {
      stars.forEach(function (star, i) {
        if (star.classList.contains('active')) {
          star.style.color = '#FFB800';
          star.style.transform = 'scale(1.1)';
        } else {
          star.style.color = '#E0D3C8';
          star.style.transform = 'scale(1)';
        }
      });
    });

    if (hiddenInput && hiddenInput.value) {
      var val = parseInt(hiddenInput.value, 10);
      if (val > 0 && val <= stars.length) {
        stars[stars.length - val].click();
      }
    }
  });
}

function initSmoothScroll() {
  var links = document.querySelectorAll('a[href^="#"]');

  links.forEach(function (link) {
    link.addEventListener('click', function (e) {
      var href = link.getAttribute('href');
      if (!href || href === '#' || href.length < 2) return;

      var targetId = href.substring(1);
      var target = document.getElementById(targetId);
      if (!target) return;

      var navbarHeight = 0;
      var navbar = document.querySelector('.navbar.fixed-top, .navbar.sticky-top');
      if (navbar) {
        navbarHeight = navbar.offsetHeight;
      }

      e.preventDefault();

      var targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 10;

      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });

      if (history.pushState) {
        history.pushState(null, null, href);
      }
    });
  });
}
