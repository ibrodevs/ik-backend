(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // Soft UI Dashboard uses <table class="table"> with <tbody> <tr>
    // Non-checkbox cells are rendered as <span class="fw-normal"> (not <td>)
    // Links to edit pages are <a> tags inside those spans or inside <th>/<td>
    var rows = document.querySelectorAll("table.table tbody tr, #result_list table tbody tr");

    rows.forEach(function (row) {
      // Find the first <a> with an href that leads to a change page
      var link = row.querySelector("a[href*='/change/'], th a, td a");
      if (!link) {
        // Fallback: any <a> with href in the row
        link = row.querySelector("a[href]");
      }
      if (!link || !link.href) return;

      row.style.cursor = "pointer";

      row.addEventListener("click", function (e) {
        // Don't hijack clicks on interactive elements
        var target = e.target;
        if (target.closest("input, a, button, label, .form-check")) return;

        window.location.href = link.href;
      });
    });
  });
})();
