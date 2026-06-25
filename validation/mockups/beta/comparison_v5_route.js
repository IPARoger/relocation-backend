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
      <label><input type="checkbox" data-action="toggle-cmp-diffs" style="width:auto;margin:0;" /> Diffs</label>
      <label style="margin-left:12px;"><input type="checkbox" data-action="toggle-pih-dignities" data-pih-scope="compare" style="width:auto;margin:0;" /> Dignities</label>
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

    <!-- Notes rail: floating panel; RTE toolbar harmonization deferred (preferred future: controls on bottom) -->
    <aside class="comparison-notes-rail" id="cmp-notes-rail" data-cmp-mount="notes-rail" data-cmp-role="notes-rail" data-cmp-notes-layout="floating" data-cmp-notes-toolbar-position="top">
      <button type="button" id="notes-fab" title="Open notes" data-action="cmp-notes-show" data-cmp-role="notes-fab"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16v13l-4 4H4z"/><line x1="8" y1="9" x2="16" y2="9"/><line x1="8" y1="13" x2="13" y2="13"/></svg></button>
      
      <div class="general-notes-section">
        <div class="general-notes-head"><button type="button" class="gn-collapse" title="Hide notes" data-action="cmp-notes-hide" data-cmp-role="notes-collapse">▾</button><div class="general-notes-label">Notes</div></div>
        <div class="notes-toolbar">
            <button class="notes-tool" title="Bold"><b>B</b></button>
            <button class="notes-tool" title="Italic" style="font-style:italic;font-weight:400">I</button>
            <button class="notes-tool" title="Underline" style="text-decoration:underline">U</button>
            <button class="notes-tool" title="Bullet list"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><line x1="9" y1="6" x2="20" y2="6"/><line x1="9" y1="12" x2="20" y2="12"/><line x1="9" y1="18" x2="20" y2="18"/><circle cx="4.5" cy="6" r="1.3" fill="currentColor" stroke="none"/><circle cx="4.5" cy="12" r="1.3" fill="currentColor" stroke="none"/><circle cx="4.5" cy="18" r="1.3" fill="currentColor" stroke="none"/></svg></button>
          </div>
          <textarea id="rm-cmp-note" class="notes-textarea" data-cmp-mount="notes-input" data-cmp-role="notes-input" placeholder="General comparison notes&#8230;" rows="7">__CMP_NOTES__</textarea>
          <p class="note-hint">Optional &middot; same record as Profile notebook &middot; pops out for long entries</p>
          <div class="notes-actions"><button class="notes-tool mic" title="Voice note (future)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 10a7 7 0 0 0 14 0"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="8.5" y1="22" x2="15.5" y2="22"/></svg></button><button type="button" class="notes-save" data-action="save-comparison-note" data-cmp-role="notes-save">Save</button></div>
        </div>
      </div>
    </aside>
  </div>
</div>
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

  function shellFragmentHtml(notesEsc) {
    return SHELL_FRAGMENT.replace("__CMP_NOTES__", notesEsc || "");
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
    const notesEsc = escapeHtml(cs.notes || "");
    const shellFixed = shellFragmentHtml(notesEsc);
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
