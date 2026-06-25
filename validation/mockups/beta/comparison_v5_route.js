/**
 * V5 comparison route plugin — comparison-only ownership boundary.
 * Requires comparison_v5_adapter.js (ComparisonV5Adapter).
 * Safe to delete: other app routes must not reference this module.
 */
(function (global) {
  "use strict";

  const RM_COMPARE_V5_CANONICAL = true;

  const SHELL_FRAGMENT = `<div id="rm-cmp-v5-root" class="rm-cmp-v5-root" data-cmp-role="comparison-root" data-cmp-mount="comparison-root">
<div class="profile-block comp-profile" data-cmp-role="authority">
  <div class="cmp-zone-b" id="rm-cmp-zone-b" data-cmp-mount="authority" data-cmp-role="authority-primary"></div>
</div>

<div class="page">
  <div class="comp-header" aria-hidden="true"></div>
  <p class="mobile-hint">Scroll right to see all cities.</p>

  <div class="city-bar-wrap" id="rm-cmp-city-bar" data-cmp-mount="city-bar">
    <div id="city-bar-inner" data-cmp-mount="city-bar-inner"></div>
  </div>

  <div class="comparison-body-grid">
    <main class="comparison-main">

  <!-- Angle in Sign -->
  <div class="block" data-section="ais" data-cmp-role="ais-block">
    <div class="block-header">
      <div class="block-header-left" data-action="cmp-toggle-block" data-section="ais" role="button" tabindex="0">
        <span class="block-arrow" id="arrow-ais">&#9660;</span>
        <span class="block-title">Angle in Sign</span>
      </div>
    </div>
    <div class="block-body" id="body-ais" data-cmp-mount="ais-body">
      <div class="fact-table-wrap"><div id="table-ais" data-cmp-mount="ais-table"></div></div>
    </div>
  </div>

  <!-- Planet in House -->
  <div class="block" data-section="pih" data-cmp-role="pih-block">
    <div class="block-header">
      <div class="block-header-left" data-action="cmp-toggle-block" data-section="pih" role="button" tabindex="0">
        <span class="block-arrow" id="arrow-pih">&#9660;</span>
        <span class="block-title">Planet in House</span>
      </div>
    </div>
    <div class="block-body" id="body-pih" data-cmp-mount="pih-body">
      <div class="fact-table-wrap"><div id="table-pih" data-cmp-mount="pih-table"></div></div>
    </div>
    <div class="pih-footer" data-cmp-mount="pih-footer" data-cmp-role="pih-footer">
      <label title="Fade duplicate values within each row across visible cities"><input type="checkbox" data-action="toggle-cmp-diffs" style="width:auto;margin:0;" /> Diffs</label>
      <label style="margin-left:12px;" title="Tint house cells using traditional sign–house correspondence (requires dignity data)"><input type="checkbox" data-action="toggle-pih-dignities" data-pih-scope="compare" style="width:auto;margin:0;" /> Dignities</label>
    </div>
  </div>

  <!-- Aspect to Angle -->
  <div class="block" data-section="a2a" data-cmp-role="a2a-block">
    <div class="block-header">
      <div class="block-header-left" data-action="cmp-toggle-block" data-section="a2a" data-cmp-toggle-id="ata" role="button" tabindex="0">
        <span class="block-arrow" id="arrow-ata">&#9660;</span>
        <span class="block-title">Aspect to Angle</span>
        <span class="angle-sep">&middot;</span>
        <!-- Canonical A2A pill style (preferred); candidate to propagate to Profile/Relocated later -->
        <div class="angle-tabs" data-cmp-role="canonical-a2a-pills">
          <button type="button" class="angle-tab active" data-action="cmp-angle-tab" data-angle-tab="asc" data-angle="ASC">ASC</button>
          <button type="button" class="angle-tab" data-action="cmp-angle-tab" data-angle-tab="dsc" data-angle="DSC">DSC</button>
          <button type="button" class="angle-tab" data-action="cmp-angle-tab" data-angle-tab="mc" data-angle="MC">MC</button>
          <button type="button" class="angle-tab" data-action="cmp-angle-tab" data-angle-tab="ic" data-angle="IC">IC</button>
        </div>
      </div>
    </div>
    <div class="block-body" id="body-ata" data-cmp-mount="a2a-body">
      <div class="fact-table-wrap"><div id="table-ata" data-cmp-mount="a2a-table"></div></div>
    </div>
  </div>

  <p class="wheel-note" aria-hidden="true" hidden></p>

  <!-- City Intelligence (below A2A): column-aligned CI grid; 7 categories from City page; compact snippets; (i) modal shows labeled version -->
  <div class="ci-section" data-section="city_intelligence" data-cmp-mount="ci-section">
    <div class="ci-section-head"><button type="button" class="ci-collapse" title="Hide City Intelligence" data-action="cmp-toggle-ci-section" data-section="city_intelligence">▾</button><div class="ci-section-title">City Intelligence</div></div>
    <div class="ci-grid" id="ci-cards" data-cmp-mount="ci-cards"></div>
  </div>
    </main>

    <!-- H7-1: Notes rail hydrated from NotesCanonical shared renderer -->
    __NOTES_RAIL__
  </div>
</div>
__CI_MODAL__
</div>`;

  function formatComparisonAuthorityBirthDate(isoDate) {
    if (!isoDate) return "";
    const parts = String(isoDate).split("-");
    if (parts.length === 3) {
      const d = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
      if (!Number.isNaN(d.getTime())) {
        return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
      }
    }
    return String(isoDate);
  }

  function comparisonAuthorityGlyphHtml(_chartRecord) {
    return '<span class="glyph glyph-slot" aria-hidden="true"></span>';
  }

  function shellFragmentHtml(notesRaw, escapeHtml) {
    const rail = (global.NotesCanonical && NotesCanonical.CANONICAL)
      ? NotesCanonical.renderRailHtml({ notes: notesRaw || "" }, escapeHtml)
      : "";
    const modal = (global.CityIntelligenceCanonical && CityIntelligenceCanonical.CANONICAL)
      ? CityIntelligenceCanonical.renderComparisonModalShellHtml()
      : "";
    return SHELL_FRAGMENT.replace("__NOTES_RAIL__", rail).replace("__CI_MODAL__", modal);
  }

  function isCanonicalComparisonSet(cs, comparisonSetId, ws) {
    return !!(RM_COMPARE_V5_CANONICAL && cs && comparisonSetId && ws && Array.isArray(cs.placeIds) && cs.placeIds.length >= 2);
  }

  function shouldRenderCanonicalShell(cs, comparisonSetId, ws) {
    return isCanonicalComparisonSet(cs, comparisonSetId, ws);
  }

  function renderShellHtml(origin, cs, ws, helpers) {
    if (!origin || !cs || !ws || !helpers) return "";
    const escapeHtml = helpers.escapeHtml;
    const resolveColumnOrderPlaceIds = helpers.resolveColumnOrderPlaceIds;
    const orderedIds = resolveColumnOrderPlaceIds(ws, cs.placeIds).slice(0, 5);
    const chartRecordId = escapeHtml(origin.chartRecordId);
    const placeIdsAttr = escapeHtml(orderedIds.join(","));
    const shellFixed = shellFragmentHtml(cs.notes || "", escapeHtml);
    return `
    <div class="rm-cmp-v5-canonical-wrap" data-cmp-v5-canonical="true">
      ${shellFixed}
      <div id="rm-cmp-v5-hydration-bridge" hidden aria-hidden="true" data-cmp-v5-hydration-only="true">
        <div id="rm-screen5-columns"
             data-chart-record="${chartRecordId}"
             data-place-ids="${placeIdsAttr}"></div>
      </div>
    </div>`;
  }

  function syncRouteChrome(opts) {
    const route = opts.route;
    const comparisonSetId = opts.comparisonSetId;
    const escapeHtml = opts.escapeHtml;
    const accountInitials = opts.accountInitials;
    const nav = document.getElementById("rm-cmp-v5-nav");
    const header = document.querySelector("header.app-header");
    const on = !!(opts.canonicalActive);
    if (on) {
      document.body.classList.add("rm-compare-v5-canonical");
    } else {
      document.body.classList.remove("rm-compare-v5-canonical");
    }
    if (header) {
      header.hidden = on;
      header.setAttribute("aria-hidden", on ? "true" : "false");
    }
    if (!nav) return;
    nav.hidden = !on;
    nav.setAttribute("aria-hidden", on ? "false" : "true");
    if (!on) return;
    const initials = accountInitials();
    nav.innerHTML = `
    <button type="button" class="nav-logo" data-action="cmp-v5-nav-dashboard">Relocation</button>
    <ul class="nav-links">
      <li><button type="button" class="nav-link" data-action="cmp-v5-nav-map">Map</button></li>
      <li><button type="button" class="nav-link" data-action="cmp-v5-nav-charts">Charts</button></li>
      <li><button type="button" class="nav-link active" aria-current="page">Compare</button></li>
      <li><button type="button" class="nav-link" data-action="cmp-v5-nav-settings">Settings</button></li>
    </ul>
    <button type="button" class="nav-account" data-action="open-account-drawer">${escapeHtml(initials)} &#9662;</button>`;
  }

  function ensureShadowMount() {
    let outer = document.getElementById("rm-cmp-v5-shadow");
    if (!outer && global.ComparisonV5Adapter) {
      const holder = document.createElement("div");
      holder.innerHTML = global.ComparisonV5Adapter.buildShadowShellHtml();
      outer = holder.firstElementChild;
      if (outer) document.body.appendChild(outer);
    }
    return outer ? outer.querySelector('[data-cmp-v5-shadow-root="true"]') : null;
  }

  function withAdapterDeps(ctx) {
    if (!ctx) return null;
    return {
      chartRecord: ctx.chartRecord,
      comparisonSet: ctx.comparisonSet,
      cols: ctx.cols,
      workspaceState: ctx.workspaceState,
      deps: Object.assign({}, ctx.deps, {
        formatComparisonAuthorityBirthDate,
        comparisonAuthorityGlyphHtml,
      }),
    };
  }

  function hydrateCanonical(ctx) {
    if (!RM_COMPARE_V5_CANONICAL) return false;
    if (!global.ComparisonV5Adapter || !ctx) return false;
    if (!Array.isArray(ctx.cols) || !ctx.cols.length) return false;
    const root = document.getElementById("rm-cmp-v5-root");
    if (!root) return;
    global.ComparisonV5Adapter.hydrate(root, withAdapterDeps(ctx));
    return true;
  }

  function hydrateShadow(ctx) {
    if (RM_COMPARE_V5_CANONICAL && document.getElementById("rm-cmp-v5-root")) return;
    if (!global.ComparisonV5Adapter || !ctx || !ctx.cols) return;
    const shadowRoot = ensureShadowMount();
    if (!shadowRoot) return;
    global.ComparisonV5Adapter.hydrate(shadowRoot, withAdapterDeps(ctx));
  }

  function wireComparisonV5CanonicalActions(scope, hooks) {
    var root = (scope && scope.querySelector) ? scope.querySelector("#rm-cmp-v5-root") : document.getElementById("rm-cmp-v5-root");
    if (!root || root.dataset.cmpV5ActionsWired === "1") return;
    root.dataset.cmpV5ActionsWired = "1";
    root.addEventListener("click", function (e) {
      var el = e.target.closest("[data-action]");
      if (!el || !root.contains(el)) return;
      var action = el.getAttribute("data-action");
      if (hooks && typeof hooks.onAction === "function") hooks.onAction(action, el, e);
    });
  }

  global.ComparisonV5Route = {
    CANONICAL: RM_COMPARE_V5_CANONICAL,
    isCanonicalComparisonSet,
    shouldRenderCanonicalShell,
    renderShellHtml,
    syncRouteChrome,
    hydrateCanonical,
    hydrateShadow,
    wireComparisonV5CanonicalActions,
    formatComparisonAuthorityBirthDate,
    comparisonAuthorityGlyphHtml,
  };
})(typeof window !== "undefined" ? window : globalThis);
