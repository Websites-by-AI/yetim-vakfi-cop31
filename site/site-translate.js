/* Shared Google-Translate widget: ONE translator UI on every page.
   Floating globe button (bottom-left); dropdown with languages.
   Loads translate.google.com lazily on first click. Hides itself offline. */
(function () {
  var BTN_ID = "aya-tr-btn", PANEL_ID = "aya-tr-panel", GADGET_ID = "google_translate_element";
  if (document.getElementById(BTN_ID)) return;
  var css = "#aya-tr-btn{position:fixed;left:12px;bottom:76px;z-index:9996;width:46px;height:46px;border-radius:50%;background:#fff;border:2px solid #0d7377;font-size:20px;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.2);font-family:inherit}" +
    "#aya-tr-panel{position:fixed;left:12px;bottom:130px;z-index:9996;background:#fff;border:2px solid #0d7377;border-radius:12px;padding:10px 12px;box-shadow:0 10px 26px rgba(0,0,0,.25);display:none;max-width:230px}" +
    "#aya-tr-panel.show{display:block}" +
    "#aya-tr-panel .goog-te-gadget{font-size:12px!important}" +
    "#aya-tr-panel .goog-te-gadget .goog-te-combo{padding:4px;font-size:13px;max-width:200px}";
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);
  var btn = document.createElement("button");
  btn.id = BTN_ID;
  btn.title = "Translate / Cevir / ترجمه";
  btn.textContent = "🌐";
  var panel = document.createElement("div");
  panel.id = PANEL_ID;
  panel.innerHTML = '<div id="' + GADGET_ID + '"></div>';
  document.body.appendChild(btn);
  document.body.appendChild(panel);
  var loaded = false;
  window.googleTranslateElementInit = function () {
    try {
      var pl = (document.documentElement.lang || "auto").split("-")[0];
      new google.translate.TranslateElement({
        pageLanguage: pl,
        includedLanguages: "en,tr,fa,ar,de,fr,ru,es",
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
      }, GADGET_ID);
    } catch (e) { btn.style.display = "none"; }
  };
  btn.onclick = function () {
    if (!loaded) {
      loaded = true;
      var s = document.createElement("script");
      s.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
      s.onerror = function () { btn.style.display = "none"; };
      document.head.appendChild(s);
      setTimeout(function () {
        if (!panel.querySelector("select")) btn.style.display = "none";
      }, 8000);
    }
    panel.classList.toggle("show");
  };
})();
