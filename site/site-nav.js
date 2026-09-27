/* Shared top nav + footer for the Yetim Vakfi x COP31 site. Include with:
   <script src="site-nav.js"></script>  (before aya-widget.js) */
(function () {
  var PAGES = [
    ["index.html", "🏠 Home"],
    ["yetim-vakfi-fundraising-tracker.html", "💛 Tracker"],
    ["cop31-20-startups.html", "🚀 Startups"],
    ["cop31-startup-zone-rules-check.html", "✅ Rules"],
    ["yetim-vakfi-cop31-swot-report.html", "⚡ SWOT"],
    ["blog.html", "📰 Blog"],
    ["contact.html", "📞 Contact"]
  ];
  var here = (location.pathname.split("/").pop() || "index.html").split("?")[0];
  var css = ".aya-nav{position:sticky;top:0;z-index:9990;display:flex;gap:6px;flex-wrap:wrap;justify-content:center;background:#0b3d3f;padding:9px 10px;box-shadow:0 2px 10px rgba(0,0,0,.25)}" +
    ".aya-nav a{color:#fff;text-decoration:none;font-size:13px;font-weight:bold;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);padding:6px 13px;border-radius:999px;font-family:'Segoe UI',Tahoma,Arial,sans-serif;white-space:nowrap}" +
    ".aya-nav a.on{background:#f59e0b;border-color:#f59e0b;color:#1f2937}" +
    ".aya-foot{text-align:center;font-size:12.5px;color:#6b7280;padding:18px 12px 34px;font-family:'Segoe UI',Tahoma,Arial,sans-serif;line-height:2}" +
    ".aya-foot a{color:#0d7377;text-decoration:none;font-weight:bold}";
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);
  var nav = document.createElement("nav");
  nav.className = "aya-nav";
  var h = "";
  PAGES.forEach(function (p) {
    h += '<a href="' + p[0] + '"' + (p[0] === here ? ' class="on"' : "") + ">" + p[1] + "</a>";
  });
  nav.innerHTML = h;
  document.body.insertBefore(nav, document.body.firstChild);
  var f = document.createElement("footer");
  f.className = "aya-foot";
  f.innerHTML = "🧸 Yetim Vakfı × COP31<br><a href=\"contact.html\">📞 Contact</a> • <a href=\"https://yetimvakfi.org.tr/en\">🌐 yetimvakfi.org.tr</a> • <a href=\"index.html\">🏠 Home</a>";
  document.body.appendChild(f);
})();
