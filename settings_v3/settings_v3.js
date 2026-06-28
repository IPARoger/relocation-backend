/**
 * Settings V3 — richer prototype clone mounted inside app_shell.html
 * Charts section includes PR #23 fixes: Tables|Chart bodies, table orbs, advanced unlock.
 */
(function () {
  "use strict";

  const SV3_MAIN_PLANETS = [
    ["sun", "Sun"], ["moon", "Moon"], ["mercury", "Mercury"], ["venus", "Venus"],
    ["mars", "Mars"], ["jupiter", "Jupiter"], ["saturn", "Saturn"],
    ["uranus", "Uranus"], ["neptune", "Neptune"], ["pluto", "Pluto"],
  ];
  const SV3_ABOVE_FOLD_BODIES = [
    ["chiron", "Chiron", true],
    ["north_node", "North Node", false],
    ["south_node", "South Node", false],
  ];
  const SV3_ADVANCED_BODIES = [
    ["lilith", "Lilith"],
    ["true_node", "True Node"],
    ["vertex", "Vertex"],
    ["part_of_fortune", "Part of Fortune"],
  ];
  const SV3_MAJOR_ASPECTS = [
    ["conjunction", "Conjunction", 8], ["opposition", "Opposition", 8], ["square", "Square", 8],
    ["trine", "Trine", 8], ["sextile", "Sextile", 6],
  ];
  const SV3_MINOR_ASPECTS = [
    ["quincunx", "Quincunx", 3], ["semisextile", "Semi-sextile", 2], ["semisquare", "Semi-square", 2],
    ["sesquiquadrate", "Sesquiquadrate", 2], ["quintile", "Quintile", 2], ["biquintile", "Biquintile", 2],
    ["septile", "Septile", 2], ["novile", "Novile", 2],
  ];

  const DATA_KINDS = [
    ["searches", "Saved searches"],
    ["comparisons", "Saved comparisons"],
    ["favorites", "Favorites"],
    ["notes", "Notes"],
    ["history", "History"],
    ["export", "Export my data"],
  ];

  let mountedRoot = null;
  let wired = false;

  function bridge() {
    return window.__rmSettingsV3Bridge || {};
  }

  function appShell() {
    return window.__rmAppShell || {};
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;",
    }[c]));
  }

  function soonBadge() {
    return '<span class="badge b-soon">soon</span>';
  }

  function sv3Eff() {
    const RM = window.RMSettings;
    const raw = (appShell().storeRaw && appShell().storeRaw()) || {};
    return (RM && typeof RM.getEffectiveSettings === "function")
      ? RM.getEffectiveSettings(raw.user_settings || null, null)
      : null;
  }

  function sv3Helper(key, fallback) {
    const eff = sv3Eff();
    const hl = (eff && eff.helper_layers && typeof eff.helper_layers === "object") ? eff.helper_layers : {};
    return hl[key] != null ? hl[key] : fallback;
  }

  function parseSectionFromHash() {
    const raw = (location.hash || "#/settings-v3").replace(/^#/, "");
    const path = raw.split("?")[0].replace(/^\//, "");
    const parts = path.split("/").filter(Boolean);
    if (parts[0] !== "settings-v3") return "charts";
    if (parts[1] === "data") return "data";
    const id = parts[1] || "charts";
    const valid = SECTIONS.some((s) => s.id === id);
    return valid ? id : "charts";
  }

  function sectionHash(id) {
    return id === "charts" ? "#/settings-v3/charts" : `#/settings-v3/${id}`;
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

  function sv3BodiesHeadHtml() {
    return `<thead><tr><th>Name</th><th class="rm-sv3-bodies-tbl">Tables</th><th class="rm-sv3-bodies-cht">Chart</th></tr></thead>`;
  }

  function sv3BodyRow(id, label, tblOn, chtOn, kind) {
    const lockAttr = ' disabled aria-disabled="true" data-sv3-advanced-lock="1"';
    return `<tr class="is-locked">
      <td>${esc(label)}</td>
      <td class="rm-sv3-bodies-tbl"><input type="checkbox" id="rm-sv3-${kind}tbl-${id}"${tblOn ? " checked" : ""}${lockAttr} /></td>
      <td class="rm-sv3-bodies-cht"><input type="checkbox" id="rm-sv3-${kind}cht-${id}"${chtOn ? " checked" : ""}${lockAttr} /></td>
    </tr>`;
  }

  function settingsV3BodiesHtml() {
    const eff = sv3Eff();
    const planets = (eff && Array.isArray(eff.visible_planets)) ? eff.visible_planets : SV3_MAIN_PLANETS.map(([id]) => id);
    const bodies = (eff && Array.isArray(eff.visible_bodies)) ? eff.visible_bodies : [];
    const hl = (eff && eff.helper_layers) || {};
    const chartPlanets = Array.isArray(hl.chart_planets) ? hl.chart_planets : planets.slice();
    const chartBodies = Array.isArray(hl.chart_bodies) ? hl.chart_bodies : bodies.slice();
    const advBodies = (hl.advanced_bodies && typeof hl.advanced_bodies === "object") ? hl.advanced_bodies : {};
    const advChart = (hl.advanced_bodies_chart && typeof hl.advanced_bodies_chart === "object") ? hl.advanced_bodies_chart : {};
    const planetRows = SV3_MAIN_PLANETS.map(([id, label]) => {
      const tblOn = planets.indexOf(id) !== -1;
      const chtOn = chartPlanets.indexOf(id) !== -1;
      return sv3BodyRow(id, label, tblOn, chtOn, "planet");
    }).join("");
    const foldRows = SV3_ABOVE_FOLD_BODIES.map(([id, label, defaultOn]) => {
      let tblOn = defaultOn;
      if (id === "chiron") tblOn = bodies.indexOf("chiron") !== -1 || bodies.length === 0;
      if (id === "north_node") tblOn = bodies.indexOf("north_node") !== -1;
      if (id === "south_node") tblOn = bodies.indexOf("south_node") !== -1;
      const chtOn = chartBodies.indexOf(id) !== -1 || (id === "chiron" && chartBodies.length === 0 && tblOn);
      return sv3BodyRow(id, label, tblOn, chtOn, "body");
    }).join("");
    const advRows = SV3_ADVANCED_BODIES.map(([id, label]) => {
      const tblOn = !!advBodies[id];
      const chtOn = !!advChart[id];
      return sv3BodyRow(id, label, tblOn, chtOn, "advbody");
    }).join("");
    return `
      <div class="rm-sv3-card" id="rm-sv3-bodies">
        <h4>Bodies &amp; Angles</h4>
        <table class="rm-sv3-bodies-table simple">
          ${sv3BodiesHeadHtml()}
          <tbody>
            ${planetRows}
            ${foldRows}
          </tbody>
        </table>
        <details class="rm-sv3-advanced" id="rm-sv3-advanced-bodies">
          <summary>Advanced Bodies</summary>
          <table class="rm-sv3-bodies-table simple">
            ${sv3BodiesHeadHtml()}
            <tbody>${advRows}</tbody>
          </table>
        </details>
      </div>`;
  }

  function settingsV3ZodiacHouseHtml() {
    const eff = sv3Eff();
    const zodiac = (eff && eff.zodiac_mode) || "tropical";
    const house = (eff && eff.house_system) || "placidus";
    return `
      <div class="rm-sv3-card" id="rm-sv3-zodiac">
        <h4>Zodiac / House System</h4>
        <div class="rm-sv3-zodiac-row">
          <label class="block">Zodiac
            <select id="rm-sv3-zodiac-mode">
              <option value="tropical"${zodiac === "tropical" ? " selected" : ""}>Tropical</option>
              <option value="sidereal" disabled aria-disabled="true">Sidereal</option>
            </select>
          </label>
          <label class="block">House system
            <select id="rm-sv3-house-system">
              <option value="placidus"${house === "placidus" ? " selected" : ""}>Placidus</option>
              <option value="whole_sign" disabled>Whole Sign</option>
              <option value="equal" disabled>Equal</option>
              <option value="koch" disabled>Koch</option>
            </select>
          </label>
        </div>
      </div>`;
  }

  function sv3OaHeadHtml() {
    return `<thead><tr>
      <th class="rm-sv3-oa-name-h"></th>
      <th class="rm-sv3-oa-tbl rm-sv3-oa-h-tables">Tables</th>
      <th class="rm-sv3-oa-cht rm-sv3-oa-h-chart">Chart</th>
      <th class="rm-sv3-oa-orb rm-sv3-oa-h-orb">Orb</th>
    </tr></thead>`;
  }

  function sv3AspectRow(kind, id, label, orbVal, tblOn, chtOn, opts) {
    const o = opts || {};
    const isMajor = kind === "maj";
    const lockMajor = isMajor && o.lockMajor !== false;
    const lockAttr = lockMajor ? ' disabled aria-disabled="true" data-sv3-major-lock="1"' : "";
    const lockCls = lockMajor ? " is-locked" : "";
    const orbDis = (isMajor && lockMajor) || o.orbDisabled
      ? ' disabled aria-disabled="true"' + (isMajor ? ' data-sv3-major-lock="1"' : "") : "";
    return `<tr class="rm-sv3-oa-row${lockCls}" data-sv3-aspect-row="${kind}-${id}">
      <td class="rm-sv3-oa-label">${esc(label)}</td>
      <td class="rm-sv3-oa-tbl"><input type="checkbox" id="rm-sv3-${kind}tbl-${id}"${tblOn ? " checked" : ""}${lockAttr} /></td>
      <td class="rm-sv3-oa-cht"><input type="checkbox" id="rm-sv3-${kind}cht-${id}"${chtOn ? " checked" : ""}${lockAttr} /></td>
      <td class="rm-sv3-oa-orb"><input type="number" id="rm-sv3-${kind}orb-${id}" min="0" max="15" step="0.5" value="${orbVal}"${orbDis} /></td>
    </tr>`;
  }

  function settingsV3OrbsAspectsHtml() {
    const eff = sv3Eff();
    const majVis = (eff && Array.isArray(eff.visible_major_aspects)) ? eff.visible_major_aspects : [];
    const minVis = (eff && Array.isArray(eff.visible_minor_aspects_list)) ? eff.visible_minor_aspects_list : [];
    const majOrb = (eff && eff.major_aspect_orbs) || {};
    const minOrb = (eff && eff.minor_aspect_orbs) || {};
    const num = (v, d) => (v == null ? d : v);
    const hl = (eff && eff.helper_layers) || {};
    const chartMaj = Array.isArray(hl.chart_major_aspects) ? hl.chart_major_aspects : majVis;
    const chartMin = Array.isArray(hl.chart_minor_aspects) ? hl.chart_minor_aspects : minVis;
    const lateAlert = sv3Helper("show_late_in_house_alert", true) !== false;
    const lateOrb = (eff && eff.house_proximity_orb_degrees != null) ? eff.house_proximity_orb_degrees : 2;
    const oos = eff ? !!eff.out_of_sign_aspects : false;
    const showA2a = sv3Helper("show_aspects_to_angles", true) !== false;
    const majorTblOn = (id) => (majVis.length ? majVis.indexOf(id) !== -1 : true);
    const majorChtOn = (id) => (chartMaj.length ? chartMaj.indexOf(id) !== -1 : majorTblOn(id));
    const majorRows = SV3_MAJOR_ASPECTS.map(([id, label, d]) =>
      sv3AspectRow("maj", id, label, num(majOrb[id], d), majorTblOn(id), majorChtOn(id), { lockMajor: true })
    ).join("");
    const minorRows = SV3_MINOR_ASPECTS.map(([id, label, d]) =>
      sv3AspectRow("min", id, label, num(minOrb[id], d), minVis.indexOf(id) !== -1, chartMin.indexOf(id) !== -1, { lockMajor: false })
    ).join("");
    return `
      <div class="rm-sv3-card" id="rm-sv3-orbs">
        <h4>Orbs &amp; Aspects</h4>
        <div class="rm-sv3-oa">
          <table class="rm-sv3-oa-table simple">
            ${sv3OaHeadHtml()}
            <tbody>${majorRows}</tbody>
          </table>
          <details class="rm-sv3-advanced rm-sv3-oa-minor-wrap" id="rm-sv3-advanced-orbs">
            <summary>Advanced Orbs &amp; Aspects</summary>
            <table class="rm-sv3-oa-table simple">
              ${sv3OaHeadHtml()}
              <tbody>${minorRows}</tbody>
            </table>
          </details>
          <div class="rm-sv3-oa-options">
            <label class="block"><input type="checkbox" id="rm-sv3-late-alert"${lateAlert ? " checked" : ""} /> Show late-in-house planet alert</label>
            <div class="rm-sv3-advanced-only">
              <label class="block">Late-house orb adjustment
                <input type="number" id="rm-sv3-late-orb" min="0" max="10" step="0.5" value="${lateOrb}" disabled aria-disabled="true" data-sv3-advanced-lock="1" style="max-width:80px;" />
              </label>
            </div>
            <label class="block"><input type="checkbox" id="rm-sv3-oos-aspects"${oos ? " checked" : ""} /> Show out-of-sign aspects</label>
            <label class="block"><input type="checkbox" id="rm-sv3-show-a2a"${showA2a ? " checked" : ""} /> Show aspects to angles</label>
          </div>
        </div>
      </div>`;
  }

  function settingsV3AdvancedCalcHtml() {
    const eff = sv3Eff();
    const minorMaster = eff ? !!eff.visible_minor_aspects : false;
    return `
      <div class="rm-sv3-card rm-sv3-advanced-calc" id="rm-sv3-advanced-calc">
        <h4>Advanced Calculation Settings</h4>
        <details class="rm-sv3-advanced" id="rm-sv3-advanced-calc-panel">
          <summary>Advanced</summary>
          <div class="rm-sv3-calc-row">
            <span>Direction-aware subsequent house</span>
            ${soonBadge()}
          </div>
          <label class="block" style="display:flex;align-items:center;gap:8px;margin-top:8px;">
            <input type="checkbox" id="rm-sv3-minor-master"${minorMaster ? " checked" : ""} />
            Enable minor aspect calculations
          </label>
          <p class="meta" style="margin:8px 0 0;">Minor aspects and custom orbs are configured in Orbs &amp; Aspects above.</p>
        </details>
      </div>`;
  }

  function secAccount() {
    const user = window.CurrentUser || {};
    const name = user.accountName || user.email || "—";
    return `
      <section class="card" id="sec-account">
        ${head("My Account")}
        ${row("Account owner", "Name shown on charts and exports.", `<input type="text" value="${esc(name)}" disabled>`)}
        ${row("Email", "", `<input type="email" value="${esc(user.email || "—")}" disabled>`)}
        ${row("Sign-in", "", `<button class="btn" disabled>Manage sign-in</button> ${soonBadge()}`)}
        ${row("Plan", "", selDis(["Free", "Individual", "Professional"]))}
        ${row("Billing", "", `<button class="btn" disabled>Manage billing</button> ${soonBadge()}`)}
        <div class="help">Paid plans add more profiles, saved work, exports, and advanced tools.</div>
      </section>`;
  }

  function secProfiles() {
    return `
      <section class="card" id="sec-profiles">
        ${head("My Profiles")}
        <div id="settings-v3-profiles-toolbar"></div>
        <div class="profile-grid" id="pgrid" style="margin-top:12px">
          <button type="button" class="pcard newp" data-action="settings-profile-create">+ New Profile</button>
        </div>
        <div data-settings-obj-bulk="profiles" class="row nb" style="margin-top:12px;">
          <span class="meta" data-settings-obj-selected-count="profiles">0 selected</span>
          <div class="ctl">
            <button type="button" data-action="settings-obj-bulk-archive" data-settings-obj-type="profiles" disabled>Archive selected</button>
          </div>
        </div>
        <div class="help">Profiles open from the list above. Use the star on a profile card to set your account default.</div>
      </section>`;
  }

  function secCharts() {
    return `
      <section class="card" id="sec-charts">
        ${head("Charts")}
        <div class="warn"><b>Global chart preferences.</b> Changes here apply to future charts and tables.</div>
        ${settingsV3BodiesHtml()}
        ${settingsV3ZodiacHouseHtml()}
        ${settingsV3OrbsAspectsHtml()}
        ${settingsV3AdvancedCalcHtml()}
        <div class="settings-save-bar">
          <button type="button" class="btn primary" data-action="save-settings-v3">Save chart settings</button>
          <button type="button" class="btn" data-action="restore-settings-v3-defaults">Restore defaults</button>
          <span id="rm-sv3-msg" class="meta" aria-live="polite"></span>
        </div>
      </section>`;
  }

  function secMap() {
    return `
      <section class="card" id="sec-map">
        ${head("My Map")}
        ${row("Show aspect bands", "", '<span class="sw on" data-toggle2="bands"></span>')}
        ${row("Aspect band profile", "", selDis(["Balanced", "Gentle", "Mountain / steep", "Custom slope"]) + " " + soonBadge())}
        ${row("Show exact aspect lines", "", '<span class="sw" data-toggle2="centerlines"></span>')}
        ${row("Exclusion style", "How excluded areas are marked on the map.", selDis(["Charcoal redaction", "Diagonal hatch", "Redacted stripe"]))}
        ${row("Mute behavior", "", "<select><option>Hide layer</option><option>Dim layer</option></select>")}
        ${row("Solo behavior", "", "<select><option>Hide others</option><option>Dim others</option></select>")}
        <div class="help">Map overlay colors live in Appearance.</div>
      </section>`;
  }

  function secAppearance() {
    return `
      <section class="card" id="sec-appearance">
        ${head("Appearance")}
        <div class="subhead">Colors</div>
        <div class="themes" id="themePicker"></div>
        <div class="subhead">Symbols &amp; notation</div>
        ${row("Aspect notation", "", selDis(["Sun Conj Saturn", "Sun Conjunction Saturn", "Sun \u260C Saturn"]))}
        <div class="subhead">Wheel</div>
        ${row("Wheel style", "", selDis(["Default wheel"]) + " " + soonBadge())}
      </section>`;
  }

  function secLocation() {
    return `
      <section class="card" id="sec-location">
        ${head("Location")}
        ${row("Ask for current location when needed", "", '<span class="sw" data-toggle2="geo" data-soon="1"></span> ' + soonBadge())}
        ${row("Manual current-location override", "", '<input type="text" placeholder="e.g. Berlin, Germany" disabled>')}
      </section>`;
  }

  function secLanguage() {
    return `
      <section class="card" id="sec-language">
        ${head("Language &amp; Regional")}
        ${row("Interface language", "App interface language.", selDis(["English"]) + " " + soonBadge())}
        ${row("Date format", "", selDis(["13 Jan 1976", "Jan 13, 1976", "13/01/1976"]))}
        ${row("Time format", "", '<div class="seg" id="timeSeg"><button type="button" data-time="ampm" class="on">AM / PM</button><button type="button" data-time="24">24-hour</button></div>')}
      </section>`;
  }

  function secSharing() {
    return `
      <section class="card" id="sec-sharing">
        ${head("Sharing &amp; Exports")}
        ${row("Default share link", "", "<select><option>Public link</option></select>")}
        ${row("Hide birth data", "", '<span class="sw" data-toggle2="hidebirth"></span>')}
        ${row("Include notes", "", '<span class="sw" data-toggle2="incnotes"></span>')}
        ${row("Include tables", "", '<span class="sw on" data-toggle2="inctables"></span>')}
        ${row("Include chart wheel", "", '<span class="sw on" data-toggle2="incwheel"></span>')}
      </section>`;
  }

  function secData() {
    const counts = (bridge().dataHubCounts && bridge().dataHubCounts()) || {};
    const hubRows = DATA_KINDS.map(([kind, label]) => {
      const count = counts[kind] != null ? counts[kind] : "—";
      const manageBtn = kind === "export"
        ? `<button type="button" class="btn tiny" data-action="settings-v3-data-manage" data-data-kind="${kind}">Export</button>`
        : `<button type="button" class="btn tiny" data-action="settings-v3-data-manage" data-data-kind="${kind}">Manage</button>`;
      return `<div class="data-row">
        <div><div class="lab">${esc(label)}</div></div>
        <div class="ctl"><b data-v3-data-count="${kind}">${esc(String(count))}</b> ${manageBtn}</div>
      </div>`;
    }).join("");
    return `
      <section class="card" id="sec-data">
        <div id="settings-v3-data-hub">
          ${head("My Data")}
          <div class="subhead">Data management</div>
          ${hubRows}
          <div class="help">Manage saved searches, comparisons, favorites, and notes from here.</div>
        </div>
        <div id="settings-v3-data-manage" hidden>
          <div class="row nb">
            <button type="button" class="btn ghost" data-action="settings-v3-data-back">\u2190 Back to My Data</button>
          </div>
          <h3 id="settings-v3-data-manage-title" style="margin:8px 0 12px;font-size:16px;"></h3>
          <div id="settings-v3-data-manage-body"></div>
        </div>
      </section>`;
  }

  function secTechnical() {
    return `
      <section class="card" id="sec-technical">
        ${head("Technical")}
        ${row("Diagnostics &amp; developer options", "", '<button type="button" class="btn ghost tiny" data-toggle="techbox">Show \u25be</button>')}
        <div id="techbox" style="display:none">
          ${row("Debug mode", "", '<span class="sw" data-toggle2="debug"></span>')}
          ${row("Show calculation metadata", "", '<span class="sw" data-toggle2="meta"></span>')}
          ${row("Version / build", "", `<span class="meta">Settings V3 \u00b7 ${new Date().toISOString().slice(0, 10)}</span>`)}
        </div>
      </section>`;
  }

  function secPersonalization() {
    return `
      <section class="card" id="sec-personalization">
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

  function applySettingsV3AdvancedState(root) {
    const scope = root || document;
    const bodiesOpen = !!scope.querySelector("#rm-sv3-advanced-bodies[open]");
    const orbsOpen = !!scope.querySelector("#rm-sv3-advanced-orbs[open]");
    const calcOpen = !!scope.querySelector("#rm-sv3-advanced-calc-panel[open]");
    const anyOpen = bodiesOpen || orbsOpen || calcOpen;
    const sv3Root = scope.querySelector(".settings-v3-root");
    if (sv3Root) sv3Root.classList.toggle("rm-sv3-advanced-open", anyOpen);
    scope.querySelectorAll("[data-sv3-advanced-lock]").forEach((el) => {
      if (anyOpen) { el.removeAttribute("disabled"); el.removeAttribute("aria-disabled"); }
      else { el.setAttribute("disabled", "disabled"); el.setAttribute("aria-disabled", "true"); }
    });
    scope.querySelectorAll("#rm-sv3-bodies tr.is-locked").forEach((row) => {
      row.classList.toggle("is-locked", !anyOpen);
    });
    scope.querySelectorAll("[data-sv3-major-lock]").forEach((el) => {
      if (orbsOpen) { el.removeAttribute("disabled"); el.removeAttribute("aria-disabled"); }
      else { el.setAttribute("disabled", "disabled"); el.setAttribute("aria-disabled", "true"); }
    });
    scope.querySelectorAll(".rm-sv3-oa-row[data-sv3-aspect-row^='maj-']").forEach((row) => {
      row.classList.toggle("is-locked", !orbsOpen);
    });
  }

  function collectSettingsV3Patch() {
    const patch = {};
    const eff = sv3Eff();
    const planetIds = SV3_MAIN_PLANETS.map(([id]) => id);
    const bodyIds = ["chiron", "north_node", "south_node"];
    const advBodyIds = SV3_ADVANCED_BODIES.map(([id]) => id);
    const anyAdvOpen = !!document.querySelector("#rm-sv3-advanced-bodies[open]")
      || !!document.querySelector("#rm-sv3-advanced-orbs[open]")
      || !!document.querySelector("#rm-sv3-advanced-calc-panel[open]");
    const collectTbl = (kind, ids) => ids.filter((id) => {
      const el = document.getElementById("rm-sv3-" + kind + "tbl-" + id);
      return el ? !!el.checked : false;
    });
    const collectCht = (kind, ids) => ids.filter((id) => {
      const el = document.getElementById("rm-sv3-" + kind + "cht-" + id);
      return el ? !!el.checked : false;
    });
    if (anyAdvOpen) {
      patch.visible_planets = collectTbl("planet", planetIds);
      patch.visible_bodies = collectTbl("body", bodyIds);
    } else {
      patch.visible_planets = (eff && Array.isArray(eff.visible_planets))
        ? eff.visible_planets.slice() : planetIds.slice();
      patch.visible_bodies = (eff && Array.isArray(eff.visible_bodies))
        ? eff.visible_bodies.slice() : ["chiron"];
    }
    const majorIds = SV3_MAJOR_ASPECTS.map(([id]) => id);
    const minorIds = SV3_MINOR_ASPECTS.map(([id]) => id);
    const orbsAdvOpen = !!document.querySelector("#rm-sv3-advanced-orbs[open]");
    if (orbsAdvOpen) {
      patch.visible_major_aspects = majorIds.filter((id) => {
        const el = document.getElementById("rm-sv3-majtbl-" + id);
        return el ? !!el.checked : false;
      });
      patch.visible_minor_aspects_list = minorIds.filter((id) => {
        const el = document.getElementById("rm-sv3-mintbl-" + id);
        return el ? !!el.checked : false;
      });
    } else {
      patch.visible_major_aspects = (eff && Array.isArray(eff.visible_major_aspects))
        ? eff.visible_major_aspects.slice() : majorIds.slice();
      patch.visible_minor_aspects_list = (eff && Array.isArray(eff.visible_minor_aspects_list))
        ? eff.visible_minor_aspects_list.slice() : [];
    }
    const minorMaster = document.getElementById("rm-sv3-minor-master");
    if (minorMaster) patch.visible_minor_aspects = !!minorMaster.checked;
    const collectOrbs = (kind, ids, allowDisabled) => {
      const out = {};
      ids.forEach((id) => {
        const el = document.getElementById("rm-sv3-" + kind + "orb-" + id);
        if (!el) return;
        if (!allowDisabled && el.disabled) return;
        const n = parseFloat(el.value);
        if (!isNaN(n)) out[id] = n;
      });
      return out;
    };
    let mo = collectOrbs("maj", majorIds, orbsAdvOpen);
    if (!Object.keys(mo).length) mo = Object.assign({}, (eff && eff.major_aspect_orbs) || {});
    if (Object.keys(mo).length) patch.major_aspect_orbs = mo;
    const mno = collectOrbs("min", minorIds, orbsAdvOpen);
    if (Object.keys(mno).length) patch.minor_aspect_orbs = mno;
    const oosEl = document.getElementById("rm-sv3-oos-aspects");
    if (oosEl) patch.out_of_sign_aspects = !!oosEl.checked;
    const lateOrbEl = document.getElementById("rm-sv3-late-orb");
    if (lateOrbEl && !lateOrbEl.disabled) {
      const n = parseFloat(lateOrbEl.value);
      if (!isNaN(n)) patch.house_proximity_orb_degrees = n;
    }
    const showA2aEl = document.getElementById("rm-sv3-show-a2a");
    const lateAlertEl = document.getElementById("rm-sv3-late-alert");
    const hl = Object.assign({}, (eff && eff.helper_layers) || {});
    if (showA2aEl) hl.show_aspects_to_angles = !!showA2aEl.checked;
    if (lateAlertEl) hl.show_late_in_house_alert = !!lateAlertEl.checked;
    if (anyAdvOpen) {
      hl.chart_planets = collectCht("planet", planetIds);
      hl.chart_bodies = collectCht("body", bodyIds);
      const advBodies = {};
      const advChart = {};
      advBodyIds.forEach((id) => {
        const tbl = document.getElementById("rm-sv3-advbodytbl-" + id);
        const cht = document.getElementById("rm-sv3-advbodycht-" + id);
        if (tbl && tbl.checked) advBodies[id] = true;
        if (cht && cht.checked) advChart[id] = true;
      });
      hl.advanced_bodies = advBodies;
      hl.advanced_bodies_chart = advChart;
    }
    if (orbsAdvOpen) {
      hl.chart_major_aspects = majorIds.filter((id) => {
        const el = document.getElementById("rm-sv3-majcht-" + id);
        return el ? !!el.checked : false;
      });
      hl.chart_minor_aspects = minorIds.filter((id) => {
        const el = document.getElementById("rm-sv3-mincht-" + id);
        return el ? !!el.checked : false;
      });
    } else {
      const effHl = (eff && eff.helper_layers) || {};
      hl.chart_major_aspects = Array.isArray(effHl.chart_major_aspects)
        ? effHl.chart_major_aspects.slice() : majorIds.slice();
      hl.chart_minor_aspects = Array.isArray(effHl.chart_minor_aspects)
        ? effHl.chart_minor_aspects.slice() : [];
    }
    patch.helper_layers = hl;
    if (showA2aEl) {
      const on = !!showA2aEl.checked;
      const prev = (eff && eff.display_aspects_to_angles) || { asc: true, mc: true, dsc: false, ic: false };
      patch.display_aspects_to_angles = on
        ? { asc: prev.asc !== false, mc: prev.mc !== false, dsc: !!prev.dsc, ic: !!prev.ic }
        : { asc: false, mc: false, dsc: false, ic: false };
    }
    return patch;
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

  function wireChartsAdvanced(root) {
    ["rm-sv3-advanced-bodies", "rm-sv3-advanced-orbs", "rm-sv3-advanced-calc-panel"].forEach((id) => {
      const el = root.querySelector("#" + id);
      if (!el || el.__sv3AdvWired) return;
      el.__sv3AdvWired = true;
      el.addEventListener("toggle", () => applySettingsV3AdvancedState(root));
    });
    applySettingsV3AdvancedState(root);
  }

  function wireSaveHandlers(root) {
    root.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-action]");
      if (!btn || !root.contains(btn)) return;
      const action = btn.getAttribute("data-action");
      if (action === "save-settings-v3") {
        const msg = root.querySelector("#rm-sv3-msg");
        if (msg) msg.textContent = "Saving\u2026";
        const patch = collectSettingsV3Patch();
        const save = appShell().saveAccountSettingsPatch;
        if (typeof save !== "function") {
          if (msg) msg.textContent = "Save unavailable — reload and try again.";
          return;
        }
        save(patch).then(() => {
          if (msg) msg.textContent = "Saved.";
          if (typeof appShell().loadViewModelFromStore === "function") {
            return appShell().loadViewModelFromStore();
          }
        }).catch((err) => {
          if (msg) msg.textContent = err.message || String(err);
        });
      }
      if (action === "restore-settings-v3-defaults") {
        const chartsSec = root.querySelector("#sec-charts");
        if (chartsSec) {
          const inner = secCharts();
          chartsSec.outerHTML = inner;
          wireChartsAdvanced(root);
        }
        const msg = root.querySelector("#rm-sv3-msg");
        if (msg) msg.textContent = "Defaults restored (not saved yet).";
      }
    });
  }

  function wireNav(root) {
    root.querySelectorAll(".nav a[data-go]").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        const id = a.getAttribute("data-go");
        if (!id) return;
        const hash = sectionHash(id);
        if (history.replaceState) history.replaceState(null, "", hash);
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
      const show = box.style.display === "none";
      box.style.display = show ? "block" : "none";
      t.textContent = show ? "Hide \u25b4" : "Show \u25be";
    });
    root.addEventListener("click", (e) => {
      const t = e.target.closest("[data-toggle2]");
      if (!t || !root.contains(t) || t.classList.contains("locked") || t.getAttribute("data-soon")) return;
      t.classList.toggle("on");
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

    if (bridge().ensureDelegation) bridge().ensureDelegation();
    wireNav(rootEl);
    wireToggles(rootEl);
    wireChartsAdvanced(rootEl);
    wireSaveHandlers(rootEl);

    if (!wired) {
      wired = true;
      window.addEventListener("hashchange", () => {
        if (mountedRoot) onHashChange(mountedRoot);
      });
    }

    const active = parseSectionFromHash();
    setNavActive(rootEl, active);
    if (bridge().refreshProfiles) bridge().refreshProfiles();
    if (bridge().refreshDataHub) bridge().refreshDataHub();

  }

  window.SettingsV3 = {
    mount,
    collectSettingsV3Patch,
    applySettingsV3AdvancedState,
  };
})();
