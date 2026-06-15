/* ============================================================
   relocation_theme.js  —  theme apply / persist / read
   ------------------------------------------------------------
   - Applies the stored theme to <html data-theme> immediately.
   - Persists the choice in localStorage (key: relocation.theme).
   - Cross-tab/page sync via the 'storage' event, so changing the
     theme in Settings re-themes an already-open Map prototype.
   - Exposes window.RelocationTheme for prototypes to read the
     active 12 overlay colors + NOT color.
   ============================================================ */
(function () {
  "use strict";
  var KEY = "relocation.theme";
  var THEMES = ["spring", "summer", "autumn", "winter"];
  var LABELS = { spring:"Spring — Possibility", summer:"Summer — Expansion", autumn:"Autumn — Study", winter:"Winter — Threshold" };

  function get() {
    try { var t = localStorage.getItem(KEY); return THEMES.indexOf(t) >= 0 ? t : "spring"; }
    catch (e) { return "spring"; }
  }
  function apply(t) {
    if (THEMES.indexOf(t) < 0) t = "spring";
    document.documentElement.setAttribute("data-theme", t);
  }
  function emit(t) {
    try { window.dispatchEvent(new CustomEvent("relocation:theme", { detail: t })); } catch (e) {}
  }
  function set(t) {
    if (THEMES.indexOf(t) < 0) return;
    try { localStorage.setItem(KEY, t); } catch (e) {}
    apply(t); emit(t);
  }
  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  function overlays() {
    var a = [];
    for (var i = 1; i <= 12; i++) a.push(cssVar("--th-ov-" + i));
    return a;
  }
  function not() { return cssVar("--th-not"); }

  // apply as early as possible (script is in <head>)
  apply(get());

  // keep other open pages in sync
  window.addEventListener("storage", function (e) {
    if (e.key === KEY && e.newValue) { apply(e.newValue); emit(e.newValue); }
  });

  window.RelocationTheme = {
    THEMES: THEMES, LABELS: LABELS,
    get: get, set: set, apply: apply, overlays: overlays, not: not
  };
})();
