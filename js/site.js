/* Sunroom Studios - fills prices/links from js/site-config.js and swaps in preview images when they exist.
   Everything works (as placeholders) with JavaScript off. No tracking, no network calls except loading your own images. */
(function () {
  var C = window.SUNROOM || { listings: {} };
  var all = function (sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); };

  function arm(a, url) {
    if (url) {
      a.href = url; a.target = "_blank"; a.rel = "noopener";
      a.classList.remove("is-pending"); a.removeAttribute("aria-disabled");
    } else {
      a.setAttribute("aria-disabled", "true");
      a.addEventListener("click", function (e) { e.preventDefault(); });
    }
  }

  all("[data-price]").forEach(function (el) {
    var l = C.listings[el.getAttribute("data-price")];
    if (l && l.price) el.textContent = "$" + l.price;
  });
  all("[data-buy]").forEach(function (a) {
    var l = C.listings[a.getAttribute("data-buy")];
    arm(a, l && l.etsy);
  });
  all('[data-link="etsy-shop"]').forEach(function (a) { arm(a, C.etsyShop); });
  all('[data-link="gumroad-word-search"]').forEach(function (a) { arm(a, C.gumroadWordSearch); });

  all("[data-img]").forEach(function (slot) {
    var img = new Image();
    img.onload = function () {
      img.alt = slot.getAttribute("data-alt") || "";
      slot.textContent = ""; slot.appendChild(img); slot.classList.add("has-img");
    };
    img.src = slot.getAttribute("data-img");
  });
})();
