/**
 * Settings V3 — fresh prototype shell (prototype_settings_v2.html visual authority).
 * My Profiles and My Data hub wired via __rmSettingsV3Bridge; other sections are visual stubs.
 */
(function () {
  "use strict";


  let mountedRoot = null;

  function bridge() {
    return window.__rmSettingsV3Bridge || {};
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;",
    }[c]));
  }

  function soon() {
    return '<span class="badge b-soon">soon</span>';
  }

  function head(title, badge) {
    return `<div class="sec-head"><h2>${esc(title)}</h2>${badge || ""}</div>`;
  }

  function row(lab, desc, ctl) {
    return `<div class="row"><div><div class="lab">${lab}</div>${desc ? `<div class="desc">${desc}</div>` : ""}</div><div class="ctl">${ctl}</div></div>`;
  }

  function selDis(opts) {
    return `<select disabled>${opts.map((o) => `<option>${esc(o)}</option>`).join("")}</select>`;
  }

  function clItem(name, opts) {
    opts = opts || {};
    const cls = "cl-item" + (opts.locked ? " locked" : "");
    const attrs = 'type="checkbox"' + (opts.on ? " checked" : "") + (opts.locked || opts.required ? " disabled" : "");
    const tag = opts.tag ? `<span class="tag">${opts.tag}</span>` : "";
    return `<label class="${cls}"><input ${attrs}><span>${esc(name)}</span>${tag}</label>`;
  }

  function secAccount() {
    const user = window.CurrentUser || {};
    const name = user.accountName || user.email || "David Goodman";
    const email = user.email || "you@example.com";
    return `<section class="card" id="sec-account">
      ${head("My Account")}
      ${row("Account owner", "Name shown on charts and exports.", `<input type="text" value="${esc(name)}" disabled>`)}
      ${row("Email", "", `<input type="email" value="${esc(email)}" disabled>`)}
      ${row("Sign-in", "", `<button class="btn" disabled>Manage sign-in</button> ${soon()}`)}
      ${row("Plan", "", selDis(["Free", "Individual", "Professional"]))}
      ${row("Billing", "", `<button class="btn" disabled>Manage billing</button> ${soon()}`)}
      <div class="help">Paid plans add more profiles, saved work, exports, and advanced tools.</div>
    </section>`;
  }

  function secProfiles() {
    return `<section class="card" id="sec-profiles" data-settings-saved-type="profiles">
      ${head("My Profiles")}
      <div id="settings-v3-profiles-toolbar"></div>
      <div class="profile-grid" id="pgrid" style="margin-top:12px">
        <button type="button" class="pcard newp" data-action="settings-profile-create">+ New Profile</button>
      </div>
      <div class="settings-data-bulk" data-settings-obj-bulk="profiles">
        <span class="meta" data-settings-obj-selected-count="profiles">0 selected</span>
        <button type="button" data-action="settings-obj-bulk-archive" data-settings-obj-type="profiles" disabled>Archive selected</button>
      </div>
      <div class="help">Selecting a profile will open its profile page. Profiles will later gain Intention spaces that group their saved searches and work.</div>
    </section>`;
  }

  const CHART_ANGLES = [
    ["asc", "ASC"], ["mc", "MC"], ["dsc", "DSC"], ["ic", "IC"],
  ];
  const CHART_PLANETS = [
    ["sun", "Sun"], ["moon", "Moon"], ["mercury", "Mercury"], ["venus", "Venus"],
    ["mars", "Mars"], ["jupiter", "Jupiter"], ["saturn", "Saturn"],
    ["uranus", "Uranus"], ["neptune", "Neptune"], ["pluto", "Pluto"],
  ];
  const CHART_NODES = [
    ["north_node", "North Node"], ["south_node", "South Node"],
  ];
  const CHART_ADV_BODIES = [
    ["lilith", "Lilith"], ["vertex", "Vertex"], ["part_of_fortune", "Part of Fortune"],
  ];
  const CHART_MAJOR_ASPECTS = [
    ["conjunction", "Conjunction", 10],
    ["opposition", "Opposition", 10],
    ["square", "Square", 8],
    ["trine", "Trine", 8],
    ["sextile", "Sextile", 6],
  ];
  const CHART_MINOR_ASPECTS = [
    ["quincunx", "Quincunx", 3], ["semisextile", "Semi-sextile", 2], ["semisquare", "Semi-square", 2],
    ["sesquiquadrate", "Sesquiquadrate", 2], ["quintile", "Quintile", 2], ["biquintile", "Biquintile", 2],
  ];

  function chartsBodiesHeadHtml() {
    return `<thead><tr><th class="sv3-charts-grid-name"></th><th class="sv3-charts-grid-col">Chart</th><th class="sv3-charts-grid-col">Tables</th></tr></thead>`;
  }

  function chartsBodyRow(kind, id, label, tblOn, chtOn, opts) {
    opts = opts || {};
    const lockCls = opts.lockRow ? " sv3-charts-row-locked" : "";
    const phCls = opts.placeholder ? " sv3-charts-placeholder-row" : "";
    let dis = "";
    if (opts.permanentDisabled) dis = " disabled";
    else if (opts.coreLock) dis = ' disabled data-sv3-core-lock="1"';
    else if (opts.chironLock) dis = ' disabled data-sv3-chiron-lock="1"';
    else if (opts.advLock) dis = ' disabled data-sv3-adv-lock="1"';
    else if (opts.lockInputs) dis = " disabled";
    return `<tr class="sv3-charts-grid-row${lockCls}${phCls}" data-sv3-body-row="${esc(kind)}-${esc(id)}">
      <td class="sv3-charts-grid-name">${esc(label)}${opts.placeholder ? '<span class="meta sv3-charts-soon"> · not in engine yet</span>' : ""}</td>
      <td class="sv3-charts-grid-col"><input type="checkbox" id="sv3-charts-${esc(kind)}-cht-${esc(id)}"${chtOn ? " checked" : ""}${dis} /></td>
      <td class="sv3-charts-grid-col"><input type="checkbox" id="sv3-charts-${esc(kind)}-tbl-${esc(id)}"${tblOn ? " checked" : ""}${dis} /></td>
    </tr>`;
  }

  function chartsAspectHeadHtml() {
    return `<thead><tr><th class="sv3-charts-oa-name sv3-charts-oa-name-h">Aspect</th><th class="sv3-charts-grid-col">Chart</th><th class="sv3-charts-grid-col">Tables</th><th class="sv3-charts-oa-orb">Orb °</th></tr></thead>`;
  }

  function chartsOrbInput(kind, id, label, orbDefault, lockAttr) {
    return `<input type="number" id="sv3-charts-${esc(kind)}-orb-${esc(id)}" class="sv3-orb-input" min="0" max="15" step="0.5" value="${orbDefault}" aria-label="${esc(label)} orb degrees"${lockAttr || ""} />`;
  }

  function chartsAspectRow(kind, id, label, orbDefault, tblOn, chtOn, opts) {
    opts = opts || {};
    const lockCls = (opts.majorLock || opts.minorLock) ? " sv3-charts-row-locked" : "";
    let lockAttr = "";
    if (opts.majorLock) lockAttr = ' disabled data-sv3-major-lock="1"';
    else if (opts.minorLock) lockAttr = ' disabled data-sv3-minor-lock="1"';
    return `<tr class="sv3-charts-oa-row${lockCls}" data-sv3-aspect-row="${esc(kind)}-${esc(id)}">
      <td class="sv3-charts-oa-name">${esc(label)}</td>
      <td class="sv3-charts-grid-col"><input type="checkbox" id="sv3-charts-${esc(kind)}-cht-${esc(id)}"${chtOn ? " checked" : ""}${lockAttr} /></td>
      <td class="sv3-charts-grid-col"><input type="checkbox" id="sv3-charts-${esc(kind)}-tbl-${esc(id)}"${tblOn ? " checked" : ""}${lockAttr} /></td>
      <td class="sv3-charts-oa-orb">${chartsOrbInput(kind, id, label, orbDefault, lockAttr)}</td>
    </tr>`;
  }

  function secCharts() {
    const angleRows = CHART_ANGLES.map(([id, label]) =>
      chartsBodyRow("angle", id, label, true, true, { coreLock: true, lockRow: true })
    ).join("");
    const planetRows = CHART_PLANETS.map(([id, label]) =>
      chartsBodyRow("planet", id, label, true, true, { coreLock: true, lockRow: true })
    ).join("");
    const chironRow = chartsBodyRow("body", "chiron", "Chiron", true, true);
    const nodeRows = CHART_NODES.map(([id, label]) =>
      chartsBodyRow("body", id, label, false, false, { permanentDisabled: true, placeholder: true })
    ).join("");
    const advBodyRows = CHART_ADV_BODIES.map(([id, label]) =>
      chartsBodyRow("advbody", id, label, false, false, { advLock: true, permanentDisabled: true, placeholder: true })
    ).join("");
    const majorAspectRows = CHART_MAJOR_ASPECTS.map(([id, label, def]) =>
      chartsAspectRow("maj", id, label, def, true, true, { majorLock: true })
    ).join("");
    const minorAspectRows = CHART_MINOR_ASPECTS.map(([id, label, def]) =>
      chartsAspectRow("min", id, label, def, false, false, { minorLock: true })
    ).join("");

    return `<section class="card" id="sec-charts" data-settings-v3-section="charts">
      ${head("Charts")}
      <div class="subhead">Bodies</div>
      <div class="desc">Defaults are set for you. Open Advanced Bodies to change optional points. North/South Node, Lilith, Vertex, and Part of Fortune are placeholders — the engine does not calculate them yet.</div>
      <table class="sv3-charts-grid" id="sv3-charts-bodies">
        ${chartsBodiesHeadHtml()}
        <tbody>${angleRows}${planetRows}${chironRow}${nodeRows}</tbody>
      </table>
      <div class="sv3-charts-disclosure-row"><div class="lab">Advanced Bodies</div><button type="button" class="btn ghost tiny" data-toggle="sv3-charts-advbodies" data-unlock-adv="1">Show ▾</button></div>
      <div id="sv3-charts-advbodies" class="sv3-charts-adv-panel" hidden>
        <table class="sv3-charts-grid">
          ${chartsBodiesHeadHtml()}
          <tbody>${advBodyRows}</tbody>
        </table>
      </div>
      <div class="subhead">Orbs &amp; Aspects</div>
      <div class="desc">Major aspects shown on chart wheels and aspect tables.</div>
      <table class="sv3-charts-oa-grid" id="sv3-charts-orbs-aspects">
        ${chartsAspectHeadHtml()}
        <tbody>${majorAspectRows}</tbody>
      </table>
      <div class="sv3-charts-disclosure-row"><div class="lab">Advanced Orbs &amp; Aspects</div><button type="button" class="btn ghost tiny" data-toggle="sv3-charts-advorbs" data-unlock-orbs="1">Show ▾</button></div>
      <div id="sv3-charts-advorbs" class="sv3-charts-adv-panel" hidden>
        <table class="sv3-charts-oa-grid">
          ${chartsAspectHeadHtml()}
          <tbody>${minorAspectRows}</tbody>
        </table>
      </div>
      <div class="sv3-charts-option-row"><label class="sv3-charts-inline-check"><span>Show Out of Sign Aspects</span><input type="checkbox" id="sv3-charts-out-of-sign" /></label></div>
      <div class="sv3-charts-option-row"><label class="sv3-charts-inline-check"><span>Show Aspects to Angles</span><input type="checkbox" id="sv3-charts-aspects-to-angles" checked /></label></div>
      <div class="sv3-charts-option-row sv3-charts-late-line"><label class="sv3-charts-inline-check"><span>Flag late in house planets</span><input type="checkbox" id="sv3-charts-late-alert" checked aria-label="Flag late in house planets" /></label><div class="sv3-charts-late-orb-stack"><span class="sv3-orb-label">Orb °</span><input type="number" id="sv3-charts-late-orb" class="sv3-orb-input" min="0" max="10" step="0.5" value="2" aria-label="Late-in-house alert orb degrees" /></div></div>
      <div class="subhead">Zodiac</div>
      ${row("Zodiac", "", `<select id="sv3-charts-zodiac"><option value="tropical" selected>Tropical</option><option value="sidereal" disabled>Sidereal (advanced)</option><option value="vedic" disabled>Vedic (advanced)</option></select>`)}
      <div class="subhead">House System</div>
      ${row("House system", "", `<select id="sv3-charts-house"><option value="placidus" selected>Placidus</option><option value="whole_sign" disabled>Whole Sign</option><option value="equal" disabled>Equal</option><option value="koch" disabled>Koch</option></select>`)}
      <div class="warn sv3-charts-calc-rule" id="sv3-charts-calc-rule" hidden>Future charts use the new setting. Existing chart records are duplicated with the new calculation settings.</div>
    </section>`;
  }

  function secMap() {
    return `<section class="card" id="sec-map">
      ${head("My Map", soon())}
      ${row("Show aspect bands", "", '<span class="sw on locked"></span>')}
      ${row("Aspect band profile", "", selDis(["Balanced", "Gentle", "Mountain / steep", "Custom slope"]) + " " + soon())}
      ${row("Show exact aspect lines", "", '<span class="sw locked"></span>')}
      ${row("Exclusion style", "How excluded areas are marked on the map.", selDis(["Charcoal redaction", "Diagonal hatch", "Redacted stripe"]) + " " + soon())}
      ${row("Mute behavior", "", selDis(["Hide layer", "Dim layer"]))}
      ${row("Solo behavior", "", selDis(["Hide others", "Dim others"]))}
      ${row("City labels", "", selDis(["Clickable labels", "Labels only", "Minimal labels", "Dense labels"]))}
      ${row("Color-blind-safe palette", "", '<span class="sw locked"></span> ' + soon())}
      <div class="help">Map overlay colors live in Appearance \u2192 Colors.</div>
      <div class="row"><div></div><div class="ctl"><button class="btn" disabled>Restore map defaults</button></div></div>
    </section>`;
  }

  function secAppearance() {
    return `<section class="card" id="sec-appearance">
      ${head("Appearance", soon())}
      <div class="subhead">Colors</div>
      <div class="themes">
        <div class="theme-card on"><div class="tname">Spring</div></div>
        <div class="theme-card"><div class="tname">Summer</div></div>
        <div class="theme-card"><div class="tname">Autumn</div></div>
        <div class="theme-card"><div class="tname">Winter</div></div>
      </div>
      <div class="ovpreview"></div>
      ${row("Map overlay opacity", "", '<input type="range" min="14" max="78" value="42" disabled> <button class="btn tiny" disabled>Reset</button>')}
      ${row("Overlay color system", "", selDis(["Relocation Default", "Traditional / sign-inspired", "Soft", "High contrast"]) + " " + soon())}
      <div class="subhead">Symbols &amp; notation</div>
      ${row("Glyph family", "", selDis(["Default"]) + " " + soon())}
      ${row("Capricorn glyph", "", selDis(["US \u2651", "Euro \u2651\ufe0e"]))}
      ${row("Aspect notation", "", selDis(["Sun Conj Saturn", "Sun Conjunction Saturn", "\u2609 \u260C \u2644"]))}
      <div class="row nb"><div class="lab">Preview</div><div class="ctl"><span class="sample">Sun Conj Saturn</span></div></div>
      <div class="row"><div></div><div class="ctl"><button class="btn" disabled>Restore visual defaults</button></div></div>
    </section>`;
  }

  function secLocation() {
    return `<section class="card" id="sec-location">
      ${head("Location", soon())}
      <div class="subhead">Current location</div>
      ${row("Ask for current location when needed", "", '<span class="sw locked"></span> ' + soon())}
      ${row("Manual current-location override", "", '<input type="text" placeholder="e.g. Berlin, Germany" disabled>')}
      <div class="subhead">Travel / Road Trip Mode ${soon()}</div>
      ${row("Continuous route tracking", "", '<span class="sw locked"></span>')}
      ${row("Notifications", "", '<span class="sw locked"></span>')}
      ${row("Airplane Mode Live", "", '<span class="sw locked"></span> ' + soon())}
    </section>`;
  }

  function secLanguage() {
    return `<section class="card" id="sec-language">
      ${head("Language &amp; Regional", soon())}
      ${row("Interface language", "App interface language.", selDis(["English"]) + " " + soon())}
      ${row("AI language", "Follows the interface language by default.", selDis(["Match interface"]) + " " + soon())}
      ${row("Map / city-label language", "Map labels and city search, where supported.", selDis(["App language", "Local language", "English"]) + " " + soon())}
      ${row("Date format", "", selDis(["13 Jan 1976", "Jan 13, 1976", "13/01/1976", "01/13/1976", "1976-01-13"]))}
      ${row("Time format", "", '<div class="seg"><button class="on" disabled>AM / PM</button><button disabled>24-hour</button></div>')}
    </section>`;
  }

  function secSharing() {
    return `<section class="card" id="sec-sharing">
      ${head("Sharing &amp; Exports", soon())}
      <div class="subhead">Sharing</div>
      ${row("Default share link", "", selDis(["Public link", "Private link \u2014 Pro"]))}
      ${row("Hide birth data", "", '<span class="sw locked"></span>')}
      ${row("Include notes", "", '<span class="sw locked"></span>')}
      ${row("Include tables", "", '<span class="sw on locked"></span>')}
      ${row("Include chart wheel", "", '<span class="sw on locked"></span>')}
      <div class="subhead">Reports &amp; exports</div>
      ${row("Hide branding", "Available on Professional plans.", '<span class="sw locked"></span> <span class="badge b-pro">pro</span>')}
      ${row("Export defaults", "", '<button class="btn" disabled>Configure</button> ' + soon())}
      ${row("Report templates", "Choose from previews on a dedicated screen.", '<button class="btn" disabled>Browse templates</button> ' + soon())}
    </section>`;
  }

  function dataHubCounts() {
    if (typeof bridge().dataHubCounts === "function") return bridge().dataHubCounts();
    return { searches: 0, comparisons: 0, favorites: 0, notes: 0, history: 0 };
  }

  function dataHubRow(label, kind, btnLabel) {
    const counts = dataHubCounts();
    const n = counts[kind] != null ? counts[kind] : 0;
    return row(
      label,
      "",
      `<b data-v3-data-count="${kind}">${n}</b> `
        + `<button type="button" class="btn tiny" data-action="settings-v3-data-manage" data-data-kind="${kind}">${esc(btnLabel)}</button>`
    );
  }

  function secData() {
    return `<section class="card" id="sec-data">
      <div id="settings-v3-data-hub">
        ${head("My Data")}
        <div class="subhead">Data management</div>
        ${dataHubRow("Saved searches", "searches", "Manage")}
        ${dataHubRow("Saved comparisons", "comparisons", "Manage")}
        ${dataHubRow("Favorites", "favorites", "Manage")}
        ${dataHubRow("Notes", "notes", "Manage")}
        ${dataHubRow("History", "history", "View")}
        ${row("Export my data", "", selDis(["Everything"]) + ' <button type="button" class="btn" disabled>Export</button>')}
        <div class="help">Export contents (wheels, tables, notes, saved work, profiles, settings) will be customizable.</div>
        <div class="subhead">AI &amp; privacy</div>
        ${row("Allow anonymized usage to improve AI assistance", "You can change this anytime.", '<span class="sw on locked"></span> ' + soon())}
        <div class="subhead">Delete data</div>
        ${row("Delete history", "", '<button type="button" class="btn danger" disabled>Delete</button>')}
        ${row("Delete all saved searches", "", '<button type="button" class="btn danger" disabled>Delete</button>')}
        ${row("Delete all comparisons", "", '<button type="button" class="btn danger" disabled>Delete</button>')}
        ${row("Delete all favorites", "", '<button type="button" class="btn danger" disabled>Delete</button>')}
        ${row("Delete all profiles", "Permanently deletes all profiles and their saved work.", '<button type="button" class="btn danger" disabled>Delete all profiles</button>')}
        <div class="subhead">Account deletion</div>
        ${row("Delete account", "", '<button type="button" class="btn danger" disabled>Delete account</button> ' + soon())}
      </div>
      <div id="settings-v3-data-manage" hidden>
        <div class="settings-v3-data-manage-head">
          <button type="button" class="btn ghost tiny" data-action="settings-v3-data-back">\u2190 Back</button>
          <h3 id="settings-v3-data-manage-title"></h3>
        </div>
        <div id="settings-v3-data-manage-body"></div>
      </div>
    </section>`;
  }

  function secTechnical() {
    return `<section class="card" id="sec-technical">
      ${head("Technical")}
      <div class="row"><div style="flex:1"><div class="lab">Diagnostics &amp; developer options</div></div>
        <div class="ctl"><button class="btn ghost tiny" data-toggle="techbox">Show \u25be</button></div></div>
      <div id="techbox" style="display:none">
        ${row("Debug mode", "", '<span class="sw locked"></span> ' + soon())}
        ${row("Show calculation metadata", "", '<span class="sw locked"></span> ' + soon())}
        ${row("Version / build", "", `<span class="meta">Settings V3 \u00b7 ${new Date().toISOString().slice(0, 10)}</span>`)}
      </div>
    </section>`;
  }

  function secPersonalization() {
    return `<section class="card" id="sec-personalization">
      ${head("Personalization", '<span class="badge b-soon">future</span>')}
      <div class="sec-sub">Creator tools we\u2019re exploring for later.</div>
      <ul class="future-list">
        <li>Design your own glyphs and use them privately in your account.</li>
        <li>Share or license glyph packs in the store (with approval).</li>
        <li>Build your own definitions library and interpretation cookbook.</li>
      </ul>
    </section>`;
  }

  const SECTIONS = [
    { id: "account", t: "My Account", build: secAccount },
    { id: "profiles", t: "My Profiles", build: secProfiles },
    { id: "charts", t: "Charts", build: secCharts },
    { id: "map", t: "My Map", build: secMap },
    { id: "appearance", t: "Appearance", build: secAppearance },
    { id: "location", t: "Location", build: secLocation },
    { id: "language", t: "Language & Regional", build: secLanguage },
    { id: "sharing", t: "Sharing & Exports", build: secSharing },
    { id: "data", t: "My Data", build: secData },
    { id: "technical", t: "Technical", build: secTechnical },
    { id: "personalization", t: "Personalization", build: secPersonalization },
  ];

  function parseSectionFromHash() {
    const raw = (location.hash || "#/settings-v3").replace(/^#/, "");
    const path = raw.split("?")[0].replace(/^\//, "");
    const parts = path.split("/").filter(Boolean);
    if (parts[0] !== "settings-v3") return "profiles";
    const id = parts[1] || "profiles";
    if (id === "data") return "data";
    return SECTIONS.some((s) => s.id === id) ? id : "profiles";
  }

  function sectionHash(id) {
    if (id === "profiles") return "#/settings-v3";
    if (id === "data") return "#/settings-v3/data";
    return `#/settings-v3/${id}`;
  }

  function setNavActive(root, id) {
    root.querySelectorAll(".nav a[data-go]").forEach((a) => {
      a.classList.toggle("on", a.getAttribute("data-go") === id);
    });
  }

  function scrollToSection(id) {
    const el = document.getElementById("sec-" + id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function wireNav(root) {
    root.querySelectorAll(".nav a[data-go]").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        const id = a.getAttribute("data-go");
        if (!id) return;
        if (history.replaceState) history.replaceState(null, "", sectionHash(id));
        setNavActive(root, id);
        scrollToSection(id);
      });
    });
  }

  function wireToggles(root) {
    root.addEventListener("click", (e) => {
      const t = e.target.closest("[data-toggle]");
      if (!t || !root.contains(t)) return;
      const box = root.querySelector("#" + t.getAttribute("data-toggle"));
      if (!box) return;
      const show = box.hidden;
      box.hidden = !show;
      t.textContent = show ? "Hide \u25b4" : "Show \u25be";
      if (t.getAttribute("data-unlock-adv") && typeof bridge().syncAdvancedBodiesLock === "function") {
        bridge().syncAdvancedBodiesLock(show);
      }
      if (t.getAttribute("data-unlock-orbs") && typeof bridge().syncAdvancedOrbsLock === "function") {
        bridge().syncAdvancedOrbsLock(show);
      }
    });
  }

  function onHashChange(root) {
    const id = parseSectionFromHash();
    setNavActive(root, id);
    scrollToSection(id);
  }

  function mount(rootEl) {
    if (!rootEl) return;
    mountedRoot = rootEl;
    const nav = rootEl.querySelector("#settings-v3-nav");
    const col = rootEl.querySelector("#settings-v3-col");
    if (!nav || !col) return;

    nav.innerHTML = SECTIONS.map((s) =>
      `<a href="${sectionHash(s.id)}" data-go="${s.id}">${esc(s.t)}</a>`
    ).join("");
    col.innerHTML = SECTIONS.map((s) => s.build()).join("");

    wireNav(rootEl);
    wireToggles(rootEl);

    if (!rootEl.dataset.hashWired) {
      rootEl.dataset.hashWired = "1";
      window.addEventListener("hashchange", () => {
        if (mountedRoot) onHashChange(mountedRoot);
      });
    }

    const active = parseSectionFromHash();
    setNavActive(rootEl, active);

    if (typeof bridge().ensureDelegation === "function") bridge().ensureDelegation();
    if (typeof bridge().refreshProfiles === "function") bridge().refreshProfiles();
    if (typeof bridge().refreshDataHub === "function") bridge().refreshDataHub();
    if (typeof bridge().wireData === "function") bridge().wireData(rootEl);
    if (typeof bridge().wireCharts === "function") bridge().wireCharts(rootEl);
    if (typeof bridge().refreshCharts === "function") bridge().refreshCharts();
  }

  window.SettingsV3 = { mount };
})();
