(function () {
  "use strict";
  var cfg = window.SITE_CONFIG || {};

  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    initReviewsWidget();
    initChatWidget();
    initFaqSchema();
    initScrollReveal();
    var yearEl = document.getElementById("year");
    if (yearEl) yearEl.textContent = new Date().getFullYear();
  });

  // Fades/slides elements marked [data-reveal] into view as the user
  // scrolls. Falls back to showing everything immediately if the browser
  // doesn't support IntersectionObserver.
  function initScrollReveal() {
    var items = document.querySelectorAll("[data-reveal]");
    if (!items.length) return;
    if (!("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("in-view"); });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el) { observer.observe(el); });
  }

  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".main-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      var expanded = nav.classList.contains("open");
      toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("open"); });
    });
  }

  // Loads the free Elfsight "Google Reviews" widget once ELFSIGHT_WIDGET_ID
  // is set in assets/js/config.js. Until then the CSS empty-state message
  // shows and the static testimonials below act as the fallback.
  function initReviewsWidget() {
    var mount = document.getElementById("google-reviews-widget");
    if (!mount) return;
    if (!cfg.elfsightWidgetId) return;

    if (!document.querySelector('script[src*="elfsight-platform"]')) {
      var platform = document.createElement("script");
      platform.src = "https://static.elfsight.com/platform/platform.js";
      platform.async = true;
      document.body.appendChild(platform);
    }
    var widget = document.createElement("div");
    widget.className = "elfsight-app-" + cfg.elfsightWidgetId;
    widget.setAttribute("data-elfsight-app-lazy", "");
    mount.appendChild(widget);
  }

  // Loads the free Tawk.to live chat widget once TAWKTO_PROPERTY_ID and
  // TAWKTO_WIDGET_ID are set in assets/js/config.js.
  function initChatWidget() {
    if (!cfg.tawkToPropertyId || !cfg.tawkToWidgetId) return;
    if (window.Tawk_API) return;
    window.Tawk_API = window.Tawk_API || {};
    window.Tawk_LoadStart = new Date();
    var s1 = document.createElement("script");
    s1.async = true;
    s1.src = "https://embed.tawk.to/" + cfg.tawkToPropertyId + "/" + cfg.tawkToWidgetId;
    s1.charset = "UTF-8";
    s1.setAttribute("crossorigin", "*");
    document.body.appendChild(s1);
  }

  // Injects FAQPage JSON-LD from the on-page <details> FAQ items so the
  // structured data always matches the visible copy (no drift to maintain).
  function initFaqSchema() {
    var items = document.querySelectorAll("[data-faq-item]");
    if (!items.length) return;
    var entities = [];
    items.forEach(function (item) {
      var q = item.querySelector("summary");
      var a = item.querySelector("[data-faq-answer]");
      if (!q || !a) return;
      entities.push({
        "@type": "Question",
        "name": q.textContent.trim(),
        "acceptedAnswer": { "@type": "Answer", "text": a.textContent.trim() }
      });
    });
    if (!entities.length) return;
    var script = document.createElement("script");
    script.type = "application/ld+json";
    script.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": entities
    });
    document.head.appendChild(script);
  }
})();
