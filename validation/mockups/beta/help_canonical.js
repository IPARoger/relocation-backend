/**
 * H9 — Help handbook renderer (field guide / atlas).
 * Visual authority: validation/mockups/beta/help_handbook.html
 * Safe to import from app_shell.html only.
 */
(function (global) {
  "use strict";

  const HELP_CANONICAL = true;
  const SEARCH_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>';

  const PLATES = {
    compass: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><circle cx="32" cy="32" r="24"/><path d="M32 12v8M32 44v8M12 32h8M44 32h8"/><path d="M32 20l6 12-6 4-6-4z" fill="currentColor" fill-opacity=".12"/></svg>',
    map: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><rect x="8" y="14" width="48" height="36" rx="4"/><path d="M16 42l12-10 8 6 12-14"/><circle cx="24" cy="26" r="2.5" fill="currentColor" fill-opacity=".25"/></svg>',
    profile: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="32" cy="24" r="10"/><path d="M14 50c2-10 10-14 18-14s16 4 18 14"/></svg>',
    wheel: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="14"/><line x1="32" y1="10" x2="32" y2="54"/><line x1="10" y1="32" x2="54" y2="32"/></svg>',
    compare: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><rect x="10" y="16" width="16" height="32" rx="2"/><rect x="28" y="16" width="16" height="32" rx="2"/><rect x="46" y="16" width="8" height="32" rx="2"/></svg>',
    notes: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M16 12h32v40l-8 8H16z"/><line x1="22" y1="24" x2="42" y2="24"/><line x1="22" y1="32" x2="38" y2="32"/><line x1="22" y1="40" x2="34" y2="40"/></svg>',
    settings: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="32" cy="32" r="8"/><path d="M32 8v8M32 48v8M8 32h8M48 32h8M16 16l6 6M42 42l6 6M16 48l6-6M42 22l6-6"/></svg>',
    concepts: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M18 46V22l14-8 14 8v24"/><line x1="32" y1="14" x2="32" y2="46"/><line x1="18" y1="32" x2="46" y2="32"/></svg>',
  };

  const HANDBOOK_SECTIONS = [
    {
      id: "start",
      label: "Start Here",
      kicker: "Orientation",
      plate: "compass",
      lede: "A calm reference for how the instrument works — not a tour, not advice.",
      entries: [
        {
          id: "what-this-is",
          title: "What this product is",
          body: "<p>Relocation astrology maps chart structure onto geography. Birth data stays fixed; angles and house cusps shift as you inspect different places.</p><p>Use the handbook when you need vocabulary or workflow context. Judgment stays with you.</p>",
          links: [{ route: "chart-record", label: "Open Chart Record" }],
        },
        {
          id: "first-pass",
          title: "A first pass through the instrument",
          body: "<ul><li>Create or select a profile with birth date, time, and place.</li><li>Open the map and inspect a few cities you are curious about.</li><li>Save candidates as favorites; build a comparison when you want side-by-side tables.</li></ul>",
          links: [{ route: "map", label: "Open Map" }, { route: "profiles", label: "Manage Profiles" }],
        },
        {
          id: "replay-tour",
          title: "Replay the guided tour",
          body: "<p>The short onboarding overlay can be replayed here when you want a refresher on navigation chrome.</p>",
          action: "replay-guided-onboarding",
          actionLabel: "Replay app tour",
        },
      ],
    },
    {
      id: "map",
      label: "The Map",
      kicker: "Discovery",
      plate: "map",
      lede: "Geography first — cities are markers inside a coordinate field.",
      entries: [
        {
          id: "map-basics",
          title: "Reading the map workspace",
          body: "<ul><li>Right-click a point to open a relocated chart popup for that coordinate.</li><li>Use city search to jump to a named place; full disambiguation names appear in search results.</li><li>Find Regions highlights areas matching declared astrological conditions.</li><li>Genie layers conditions visually — membership and proximity, not rankings.</li></ul>",
          links: [{ route: "map", label: "Open Map" }],
        },
        {
          id: "map-overlays",
          title: "Overlays and inspection",
          body: "<p>Overlays encode membership and proximity only. Popups and relocated charts carry the inspectable tables — AiS, PiH, and A2A — for the point you selected.</p>",
        },
      ],
    },
    {
      id: "profiles",
      label: "Profiles",
      kicker: "Identity",
      plate: "profile",
      lede: "One Chart Record per person; profiles do not share birth data.",
      entries: [
        {
          id: "chart-record",
          title: "Chart Record page",
          body: "<p>The profile page holds natal facts, favorites, saved searches, and comparison sets for one person. Switch profiles from the title-plate caret or account drawer.</p>",
          links: [{ route: "chart-record", label: "Chart Record" }, { route: "profiles", label: "Profile Management" }],
        },
        {
          id: "birth-data",
          title: "Birth data and confidence",
          body: "<p>Date, time, and birth city anchor all calculations. Time uncertainty is stored as metadata on a single chart — not as duplicate charts.</p>",
          links: [{ route: "birth-data", label: "Birth Data route" }],
        },
      ],
    },
    {
      id: "relocated",
      label: "Relocated Charts",
      kicker: "Evaluation",
      plate: "wheel",
      lede: "Try a place on — same birth moment, new local sky.",
      entries: [
        {
          id: "relocated-page",
          title: "Relocated chart page",
          body: "<p>When you open a city from favorites or the map, the relocated page shows wheel and tables for that coordinate. Current location context appears beside the name plate.</p>",
          links: [{ route: "chart", label: "Relocated chart route" }],
        },
        {
          id: "tables",
          title: "AiS · PiH · A2A tables",
          body: "<p>Aspects in Sign centers on the sign word. Planet in House shows house placements; optional dignities footer applies traditional sign-to-house relationships. Aspects to Angles lists angle contacts within orb.</p>",
        },
      ],
    },
    {
      id: "comparison",
      label: "Comparison",
      kicker: "Discernment",
      plate: "compare",
      lede: "Side-by-side columns for weighing candidates without declaring a winner.",
      entries: [
        {
          id: "build-compare",
          title: "Building a comparison set",
          body: "<p>Add cities from favorites or search, then open the comparison workspace. Column hatch differentiates places at low intensity — not value judgment.</p>",
          links: [{ route: "compare", label: "Comparison workspace" }],
        },
        {
          id: "comparison-notes",
          title: "Notes on comparisons",
          body: "<p>General comparison notes attach to the built set. Author them from the comparison rail or Notes Library.</p>",
          links: [{ route: "notes-library", label: "Notes Library" }],
        },
      ],
    },
    {
      id: "notes",
      label: "Notes",
      kicker: "Reflection",
      plate: "notes",
      lede: "Your annotations on profiles, comparisons, and investigations.",
      entries: [
        {
          id: "notes-surfaces",
          title: "Where notes live",
          body: "<p>Profile and relocated pages carry a notes card. Comparison uses a floating rail. Notes Library searches and edits saved notes for the active profile.</p>",
          links: [{ route: "notes-library", label: "Notes Library" }],
        },
      ],
    },
    {
      id: "settings",
      label: "Settings",
      kicker: "Administration",
      plate: "settings",
      lede: "Account-wide calculation and appearance defaults.",
      entries: [
        {
          id: "settings-sections",
          title: "Settings sections",
          body: "<p>Astrology controls bodies, aspects, orbs, and dignities ontology. Appearance holds theme and regional formats. My Data links to profile management and archives.</p>",
          links: [
            { route: "settings", label: "Settings home" },
            { settingsSub: "astrology", label: "Astrology settings" },
            { settingsSub: "display", label: "Appearance settings" },
          ],
        },
      ],
    },
    {
      id: "concepts",
      label: "Concepts",
      kicker: "Reference",
      plate: "concepts",
      lede: "Vocabulary for reading tables and map overlays.",
      entries: [
        {
          id: "angles",
          title: "Angles and relocation",
          body: "<p>Ascendant, Midheaven, Descendant, and IC rotate with longitude and latitude. A planet on an angle in one city may not be on that angle elsewhere.</p>",
        },
        {
          id: "houses",
          title: "House cusps",
          body: "<p>House boundaries shift with relocation. PiH shows which house each planet occupies at the selected place.</p>",
        },
        {
          id: "feedback",
          title: "Report an issue",
          body: "<p>Found incorrect behavior or confusing copy? Email <a href=\"mailto:feedback@relocationapp.com\">feedback@relocationapp.com</a> with steps to reproduce.</p>",
        },
      ],
    },
  ];

  function esc(text, escapeHtml) {
    return escapeHtml ? escapeHtml(text) : String(text == null ? "" : text);
  }

  function sectionSearchBlob(section) {
    const parts = [section.label, section.kicker, section.lede];
    (section.entries || []).forEach((e) => {
      parts.push(e.title, e.body || "");
    });
    return parts.join(" ").toLowerCase();
  }

  function filterSections(state) {
    const q = String((state && state.searchQuery) || "").trim().toLowerCase();
    if (!q) return HANDBOOK_SECTIONS.slice();
    return HANDBOOK_SECTIONS.filter((s) => sectionSearchBlob(s).includes(q)).map((s) => {
      const entries = (s.entries || []).filter((e) => {
        const blob = (e.title + " " + (e.body || "")).toLowerCase();
        return blob.includes(q) || sectionSearchBlob(s).includes(q);
      });
      return Object.assign({}, s, { entries: entries.length ? entries : s.entries });
    });
  }

  function renderPlateHtml(plateKey) {
    const svg = PLATES[plateKey] || PLATES.compass;
    return `<div class="help-handbook-plate" aria-hidden="true">${svg}</div>`;
  }

  function renderLinksHtml(links, escapeHtml) {
    if (!links || !links.length) return "";
    const btns = links.map((lnk) => {
      if (lnk.settingsSub) {
        return `<button type="button" class="linkish" data-settings-sub="${esc(lnk.settingsSub, escapeHtml)}">${esc(lnk.label, escapeHtml)}</button>`;
      }
      if (lnk.route) {
        return `<button type="button" class="linkish" data-nav="${esc(lnk.route, escapeHtml)}">${esc(lnk.label, escapeHtml)}</button>`;
      }
      return "";
    }).join("");
    return `<div class="help-handbook-links">${btns}</div>`;
  }

  function renderEntryHtml(entry, escapeHtml, openByDefault) {
    const openAttr = openByDefault ? " open" : "";
    const action = entry.action
      ? `<button type="button" class="linkish" data-action="${esc(entry.action, escapeHtml)}">${esc(entry.actionLabel || "Open", escapeHtml)}</button>`
      : "";
    return `<details class="help-handbook-entry"${openAttr} id="help-entry-${esc(entry.id, escapeHtml)}">
      <summary>${esc(entry.title, escapeHtml)}</summary>
      <div class="help-handbook-entry-body">${entry.body || ""}${action}${renderLinksHtml(entry.links, escapeHtml)}</div>
    </details>`;
  }

  function renderSectionHtml(section, state, escapeHtml) {
    const q = String((state && state.searchQuery) || "").trim();
    const openEntries = !!q;
    const entries = (section.entries || []).map((e) => renderEntryHtml(e, escapeHtml, openEntries)).join("");
    return `<article class="help-handbook-section" id="help-section-${esc(section.id, escapeHtml)}" data-help-section="${esc(section.id, escapeHtml)}">
      <div class="help-handbook-section-head">
        ${renderPlateHtml(section.plate)}
        <div>
          <p class="help-kicker">${esc(section.kicker, escapeHtml)}</p>
          <h3>${esc(section.label, escapeHtml)}</h3>
          <p class="help-section-lede">${esc(section.lede, escapeHtml)}</p>
        </div>
      </div>
      ${entries}
    </article>`;
  }

  function renderTocHtml(state, escapeHtml) {
    const sections = filterSections(state);
    const active = (state && state.activeSectionId) || (sections[0] && sections[0].id) || "start";
    return sections.map((s) => {
      const cls = s.id === active ? " active" : "";
      return `<button type="button" class="help-toc-item${cls}" data-help-section="${esc(s.id, escapeHtml)}">${esc(s.label, escapeHtml)}</button>`;
    }).join("");
  }

  function renderSectionsHtml(state, escapeHtml) {
    const sections = filterSections(state);
    if (!sections.length) {
      return '<p class="help-handbook-empty">No handbook entries match your search.</p>';
    }
    return sections.map((s) => renderSectionHtml(s, state, escapeHtml)).join("");
  }

  function renderSearchMetaHtml(state) {
    const q = String((state && state.searchQuery) || "").trim();
    const sections = filterSections(state);
    if (!q) return "Browse by section or search terms, places, and table names.";
    const n = sections.reduce((acc, s) => acc + ((s.entries && s.entries.length) || 0), 0);
    return n ? `${sections.length} section${sections.length === 1 ? "" : "s"} · ${n} entr${n === 1 ? "y" : "ies"} match “${q}”` : `No entries match “${q}”`;
  }

  function renderPageHtml(state, escapeHtml) {
    const st = state || {};
    const q = esc(st.searchQuery || "", escapeHtml);
    return `<div class="help-handbook" data-help-framework>
      <p class="help-kicker">Handbook</p>
      <h2>Help &amp; Learn</h2>
      <p class="purpose">Field guide to the instrument — search, browse, open the surface you need.</p>
      <div class="help-handbook-layout">
        <nav class="help-handbook-toc" id="rm-help-toc" aria-label="Handbook contents">${renderTocHtml(st, escapeHtml)}</nav>
        <div class="help-handbook-main">
          <div class="help-handbook-search-wrap">
            ${SEARCH_SVG}
            <input type="search" id="rm-help-search" class="help-handbook-search" placeholder="Search handbook…" value="${q}" autocomplete="off" />
            <p class="help-handbook-search-meta" id="rm-help-search-meta" aria-live="polite">${renderSearchMetaHtml(st)}</p>
          </div>
          <div id="rm-help-sections">${renderSectionsHtml(st, escapeHtml)}</div>
          <div class="help-handbook-foot">
            <button type="button" data-nav="dashboard">Back to app</button>
            <span class="meta">Static reference · no AI advisor</span>
          </div>
        </div>
      </div>
    </div>`;
  }

  function refreshPanels(state, escapeHtml, root) {
    const host = root || document;
    const toc = host.querySelector("#rm-help-toc");
    const sections = host.querySelector("#rm-help-sections");
    const meta = host.querySelector("#rm-help-search-meta");
    const search = host.querySelector("#rm-help-search");
    if (toc) toc.innerHTML = renderTocHtml(state, escapeHtml);
    if (sections) sections.innerHTML = renderSectionsHtml(state, escapeHtml);
    if (meta) meta.textContent = renderSearchMetaHtml(state);
    if (search && search.value !== (state.searchQuery || "")) search.value = state.searchQuery || "";
  }

  global.HelpCanonical = {
    CANONICAL: HELP_CANONICAL,
    HANDBOOK_SECTIONS: HANDBOOK_SECTIONS,
    filterSections: filterSections,
    renderPageHtml: renderPageHtml,
    renderTocHtml: renderTocHtml,
    renderSectionsHtml: renderSectionsHtml,
    refreshPanels: refreshPanels,
  };
})(typeof window !== "undefined" ? window : globalThis);
