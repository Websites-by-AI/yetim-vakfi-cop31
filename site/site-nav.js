/* Shared drawer (hamburger) menu + footer for the Yetim Vakfi x COP31 site.
   Include with: <script src="site-nav.js"></script> (before aya-widget.js)
   All 7 links collapse behind one button; drawer slides from the side. */
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
  function isRTL() {
    try {
      return document.body.classList.contains("rtl") ||
        getComputedStyle(document.body).direction === "rtl";
    } catch (e) { return false; }
  }
  var css =
    ".aya-top{position:sticky;top:0;z-index:9990;display:flex;align-items:center;gap:10px;background:#0b3d3f;color:#fff;padding:9px 12px;box-shadow:0 2px 10px rgba(0,0,0,.25);font-family:'Segoe UI',Tahoma,Arial,sans-serif}" +
    ".aya-burger{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);color:#fff;font-size:18px;line-height:1;border-radius:10px;padding:7px 12px;cursor:pointer;font-family:inherit}" +
    ".aya-title{color:#fff;text-decoration:none;font-weight:bold;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}" +
    ".aya-home{margin-inline-start:auto;color:#fff;text-decoration:none;font-size:18px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:10px;padding:4px 10px}" +
    ".aya-nav{position:fixed;top:0;bottom:0;width:min(300px,85vw);background:#0b3d3f;z-index:9995;display:flex;flex-direction:column;padding:12px;gap:6px;transition:transform .25s ease;font-family:'Segoe UI',Tahoma,Arial,sans-serif}" +
    ".aya-nav.left{left:0;transform:translateX(-105%)}" +
    ".aya-nav.right{right:0;transform:translateX(105%)}" +
    ".aya-nav.open{transform:translateX(0)}" +
    ".aya-nav a{color:#fff;text-decoration:none;font-size:15px;font-weight:bold;background:rgba(255,255,255,.08);padding:11px 14px;border-radius:10px}" +
    ".aya-nav a.on{background:#f59e0b;color:#1f2937}" +
    ".aya-x{align-self:flex-end;background:none;border:none;color:#fff;font-size:22px;cursor:pointer;padding:2px 8px;line-height:1}" +
    ".aya-veil{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:9994;display:none}" +
    ".aya-veil.show{display:block}" +
    ".aya-foot{text-align:center;font-size:12.5px;color:#6b7280;padding:18px 12px 34px;font-family:'Segoe UI',Tahoma,Arial,sans-serif;line-height:2}" +
    ".aya-foot a{color:#0d7377;text-decoration:none;font-weight:bold}";
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);

  var top = document.createElement("div");
  top.className = "aya-top";
  top.innerHTML = "<button class=\"aya-burger\" id=\"aya-burger\" aria-label=\"Menu\">☰</button>" +
    "<a class=\"aya-title\" href=\"index.html\">🧸 Yetim Vakfı × COP31</a>" +
    "<a class=\"aya-home\" href=\"index.html\" aria-label=\"Home\">🏠</a>";
  document.body.insertBefore(top, document.body.firstChild);

  var veil = document.createElement("div");
  veil.className = "aya-veil";
  veil.id = "aya-veil";
  document.body.appendChild(veil);

  var nav = document.createElement("nav");
  nav.className = "aya-nav left";
  nav.id = "aya-nav";
  var h = "<button class=\"aya-x\" id=\"aya-x\" aria-label=\"Close\">✕</button>";
  PAGES.forEach(function (p) {
    h += "<a href=\"" + p[0] + "\"" + (p[0] === here ? " class=\"on\"" : "") + ">" + p[1] + "</a>";
  });
  nav.innerHTML = h;
  document.body.appendChild(nav);

  function open() {
    nav.classList.remove("left", "right", "open");
    nav.classList.add(isRTL() ? "right" : "left");
    void nav.offsetWidth;
    nav.classList.add("open");
    veil.classList.add("show");
  }
  function close() {
    nav.classList.remove("open");
    veil.classList.remove("show");
  }
  document.getElementById("aya-burger").onclick = open;
  document.getElementById("aya-x").onclick = close;
  veil.onclick = close;
  nav.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", close); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") close();
  });

  var f = document.createElement("footer");
  f.className = "aya-foot";
  f.innerHTML = "🧸 Yetim Vakfı × COP31<br><a href=\"contact.html\">📞 Contact</a> • <a href=\"https://yetimvakfi.org.tr/en\" target=\"_blank\" rel=\"noopener\">🌐 yetimvakfi.org.tr</a> • <a href=\"index.html\">🏠 Home</a>";
  document.body.appendChild(f);
})();
