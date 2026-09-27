/* Debug mode for the Yetim Vakfi x COP31 site.
   Usage: open any page with ?debug=1  (e.g. index.html?debug=1)
   Does NOTHING unless debug=1 is present. Shows a design-system audit panel:
   theme / nav / footer / Aya widget / meta / images / JS errors / viewport. */
(function () {
  if (!/[?&#]debug=1\b/.test(location.search + location.hash)) return;

  var errors = [];
  window.addEventListener("error", function (e) {
    errors.push((e.message || "script error") + " @" + (e.lineno || "?"));
    var el = document.getElementById("dbg-errs");
    if (el) el.textContent = errors.length + " error(s): " + errors.slice(-3).join(" | ");
  });

  function cssVar(n) {
    try { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
    catch (e) { return "?"; }
  }

  function runChecks() {
    var nav = document.querySelector("nav.aya-nav");
    var navLinks = nav ? nav.querySelectorAll("a").length : 0;
    var imgs = document.querySelectorAll("img");
    var broken = 0, i;
    for (i = 0; i < imgs.length; i++) {
      if (imgs[i].complete && imgs[i].naturalWidth === 0) broken++;
    }
    var lsKeys = "?";
    try { lsKeys = String(localStorage.length); } catch (e) { lsKeys = "blocked"; }
    var vp = document.querySelector('meta[name="viewport"]');
    return [
      ["Theme CSS", !!document.querySelector('link[href*="site-theme.css"]'), "--bg=" + (cssVar("--bg") || "(unset)")],
      ["Nav bar", !!nav && navLinks === 7, navLinks + "/7 links"],
      ["Footer", !!document.querySelector("footer.aya-foot"), "aya-foot"],
      ["Aya widget", !!document.getElementById("aya-fab"), "#aya-fab " + (document.getElementById("aya-panel") ? "+ panel" : "(no panel)")],
      ["Title", document.title.length > 0, document.title.slice(0, 40)],
      ["Viewport meta", !!vp, vp ? "ok" : "MISSING"],
      ["lang", !!document.documentElement.lang, document.documentElement.lang || "(none)"],
      ["Images", broken === 0, imgs.length + " total, " + broken + " broken"],
      ["JS errors", errors.length === 0, errors.length + " captured"],
      ["Viewport", true, window.innerWidth + "x" + window.innerHeight + " DPR=" + (window.devicePixelRatio || 1)],
      ["RTL", true, document.body.className.indexOf("rtl") >= 0 ? "rtl ON" : "ltr"],
      ["localStorage", true, lsKeys + " keys"]
    ];
  }

  function buildPanel() {
    var css = "#dbg-p{position:fixed;top:64px;right:10px;z-index:99999;width:300px;max-height:80vh;overflow:auto;background:#111827;color:#e5e7eb;font:12.5px/1.6 -apple-system,'Segoe UI',Tahoma,Arial,sans-serif;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.4);border:1px solid #374151}" +
      "#dbg-p h3{margin:0;padding:10px 12px;font-size:13px;background:#0b3d3f;border-radius:12px 12px 0 0}" +
      "#dbg-p table{width:100%;border-collapse:collapse}#dbg-p td{padding:4px 10px;border-top:1px solid #1f2937;vertical-align:top}" +
      "#dbg-p .ok{color:#34d399;font-weight:bold}#dbg-p .bad{color:#f87171;font-weight:bold}" +
      "#dbg-p .det{color:#9ca3af;font-size:11.5px;word-break:break-word}" +
      "#dbg-p .row{display:flex;gap:6px;padding:10px;border-top:1px solid #1f2937;flex-wrap:wrap}" +
      "#dbg-p button{background:#0d7377;color:#fff;border:none;border-radius:8px;padding:6px 10px;font-size:12px;font-weight:bold;cursor:pointer;font-family:inherit}" +
      "#dbg-p button.ghost{background:#374151}#dbg-p button.warn{background:#b45309}" +
      "#dbg-errs{padding:6px 10px;font-size:11.5px;color:#fbbf24;border-top:1px solid #1f2937;word-break:break-word}" +
      "body.dbg-ol *{outline:1px solid rgba(220,38,38,.55)!important}";
    var st = document.createElement("style");
    st.textContent = css;
    document.head.appendChild(st);
    var p = document.createElement("div");
    p.id = "dbg-p";
    p.innerHTML = "<h3>🐞 Debug — design audit</h3><div id=\"dbg-list\"></div><div id=\"dbg-errs\"></div>" +
      "<div class=\"row\"><button id=\"dbg-re\">Re-run</button><button id=\"dbg-ol\" class=\"warn\">Outlines</button>" +
      "<button id=\"dbg-cp\">Copy</button><button id=\"dbg-x\" class=\"ghost\">Hide</button></div>";
    document.body.appendChild(p);
    document.getElementById("dbg-re").onclick = render;
    document.getElementById("dbg-x").onclick = function () { p.style.display = "none"; };
    document.getElementById("dbg-ol").onclick = function () {
      document.body.classList.toggle("dbg-ol");
    };
    document.getElementById("dbg-cp").onclick = function () {
      var t = "DEBUG " + location.pathname + "\n" + runChecks().map(function (c) {
        return (c[1] ? "PASS " : "FAIL ") + c[0] + " :: " + c[2];
      }).join("\n");
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(t);
      } else {
        var ta = document.createElement("textarea");
        ta.value = t; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
      }
    };
  }

  function render() {
    var list = document.getElementById("dbg-list");
    if (!list) return;
    var h = "<table>";
    runChecks().forEach(function (c) {
      h += "<tr><td class=\"" + (c[1] ? "ok" : "bad") + "\">" + (c[1] ? "✅" : "❌") + "</td><td><b>" + c[0] + "</b><br><span class=\"det\">" + c[2] + "</span></td></tr>";
    });
    list.innerHTML = h + "</table>";
  }

  if (document.readyState === "complete") { buildPanel(); render(); }
  else {
    window.addEventListener("load", function () { buildPanel(); render(); });
    setTimeout(function () { if (!document.getElementById("dbg-p")) { buildPanel(); render(); } }, 4000);
  }
})();
