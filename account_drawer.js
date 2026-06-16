/**
 * account_drawer.js — persistent Account Drawer for app_shell.html.
 *
 * Exposes: window.__showAccountDrawer()
 *
 * Reads:   window.CurrentUser        (user_profile.js)
 *          window.__rmAppShell       (app_shell.html inline script)
 * Calls:   window.__showFirstProfileIntake()      (first_profile_intake.js)
 *          window.__showCurrentLocationEditor()   (current_location_editor.js)
 *          window.logout()                        (auth_guard.js)
 *          window.__rmAppShell.saveAccountSettingsPatch()
 *          window.__rmAppShell.savePersistedChartRecord()
 */
(function () {
  "use strict";

  var DRAWER_ID = "rm-account-drawer";
  var SCRIM_ID  = "rm-account-drawer-scrim";

  function injectStyles() {
    if (document.getElementById(DRAWER_ID + "-styles")) return;
    var s = document.createElement("style");
    s.id = DRAWER_ID + "-styles";
    s.textContent = [
      "#" + SCRIM_ID + " {",
      "  display:none;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:9000;",
      "}",
      "#" + SCRIM_ID + ".open { display:block; }",
      "#" + DRAWER_ID + " {",
      "  position:fixed;top:0;right:0;height:100vh;width:300px;",
      "  background:#fff;border-left:1px solid #e2e8f0;",
      "  z-index:9001;overflow-y:auto;",
      "  transform:translateX(100%);transition:transform .22s ease;",
      "  display:flex;flex-direction:column;font-family:inherit;font-size:14px;color:#1e293b;",
      "}",
      "#" + DRAWER_ID + ".open { transform:translateX(0); }",
      "#" + DRAWER_ID + " .ad-header {",
      "  display:flex;align-items:center;justify-content:space-between;",
      "  padding:14px 16px;border-bottom:1px solid #e2e8f0;",
      "}",
      "#" + DRAWER_ID + " .ad-header h2 { margin:0;font-size:15px;font-weight:600; }",
      "#" + DRAWER_ID + " .ad-close {",
      "  background:none;border:none;cursor:pointer;font-size:18px;color:#64748b;padding:4px;",
      "}",
      "#" + DRAWER_ID + " .ad-section { padding:14px 16px;border-bottom:1px solid #f1f5f9; }",
      "#" + DRAWER_ID + " .ad-section-label {",
      "  font-size:11px;text-transform:uppercase;letter-spacing:.05em;",
      "  color:#94a3b8;margin-bottom:8px;",
      "}",
      "#" + DRAWER_ID + " .ad-field { margin-bottom:6px;font-size:13px; }",
      "#" + DRAWER_ID + " .ad-field span.label { color:#64748b;font-size:11px;margin-right:6px; }",
      "#" + DRAWER_ID + " .ad-profile-row {",
      "  display:flex;align-items:center;justify-content:space-between;",
      "  padding:6px 0;font-size:13px;border-bottom:1px solid #f8fafc;",
      "}",
      "#" + DRAWER_ID + " .ad-profile-row:last-child { border-bottom:none; }",
      "#" + DRAWER_ID + " .ad-active-dot {",
      "  width:7px;height:7px;border-radius:50%;background:#7c3aed;",
      "  display:inline-block;margin-right:6px;flex-shrink:0;",
      "}",
      "#" + DRAWER_ID + " .ad-city { font-size:11px;color:#94a3b8;margin-left:4px; }",
      "#" + DRAWER_ID + " .ad-star {",
      "  background:none;border:none;cursor:pointer;font-size:15px;",
      "  color:#cbd5e1;padding:2px 4px;line-height:1;flex-shrink:0;",
      "  transition:color .15s;",
      "}",
      "#" + DRAWER_ID + " .ad-star:hover { color:#f59e0b; }",
      "#" + DRAWER_ID + " .ad-star.is-default {",
      "  color:#f59e0b;cursor:default;",
      "}",
      "#" + DRAWER_ID + " .ad-row-actions {",
      "  display:flex;align-items:center;gap:6px;flex-shrink:0;",
      "}",
      "#ad-default-msg {",
      "  font-size:11px;min-height:14px;margin-top:6px;color:#64748b;",
      "}",
      "#ad-default-msg.is-error { color:#b91c1c; }",
      "#" + DRAWER_ID + " .ad-btn {",
      "  display:block;width:100%;text-align:left;background:none;border:1px solid #e2e8f0;",
      "  border-radius:6px;padding:8px 12px;cursor:pointer;font-size:13px;color:#1e293b;",
      "  margin-bottom:6px;",
      "}",
      "#" + DRAWER_ID + " .ad-btn:hover { background:#f8fafc; }",
      "#" + DRAWER_ID + " .ad-btn.primary {",
      "  background:#7c3aed;color:#fff;border-color:#7c3aed;",
      "}",
      "#" + DRAWER_ID + " .ad-btn.primary:hover { background:#6d28d9; }",
      "#" + DRAWER_ID + " .ad-help-row { font-size:13px;color:#475569;padding:5px 0;cursor:default; }",
      "#" + DRAWER_ID + " .ad-logout-section { margin-top:auto;padding:14px 16px; }",
      "#rm-acct-drawer-btn {",
      "  margin-left:8px;background:none;border:1px solid #cbd5e1;border-radius:6px;",
      "  padding:4px 10px;font-size:12px;cursor:pointer;color:#1e293b;white-space:nowrap;",
      "}",
      "#rm-acct-drawer-btn:hover { background:#f1f5f9; }",
    ].join("\n");
    document.head.appendChild(s);
  }

  function getActiveProfileId() {
    try {
      var shell = window.__rmAppShell;
      return shell && shell.navContext && shell.navContext.chartRecordId;
    } catch (e) { return null; }
  }

  function buildDrawerHtml() {
    var user = window.CurrentUser || {};
    var accountName = user.accountName || "Account";
    var accountType = user.accountType || "\u2014";
    var role        = user.role        || "\u2014";

    var profilesHtml = "";
    var activeId  = getActiveProfileId();
    var defaultId = null;
    var activeRecord = null;
    try {
      var shell = window.__rmAppShell;
      var records = (shell && typeof shell.getProfiles === "function") ? shell.getProfiles() : [];
      defaultId   = (shell && typeof shell.getAccountDefaultChartRecordId === "function") ? shell.getAccountDefaultChartRecordId() : null;
      activeRecord = records.find(function (r) { return r.chartRecordId === activeId; }) || records[0] || null;
      if (records.length) {
        profilesHtml = records.map(function (r) {
          var isActive   = r.chartRecordId === activeId;
          var isDefault  = r.chartRecordId === defaultId;
          var dot = isActive
            ? '<span class="ad-active-dot" title="Active"></span>'
            : '<span style="display:inline-block;width:7px;margin-right:6px;"></span>';
          var city = r.currentCity && r.currentCity !== "\u2014"
            ? '<span class="ad-city">' + r.currentCity + '</span>' : "";
          var locBtn = isActive
            ? '<button type="button" class="ad-btn" style="width:auto;padding:3px 8px;font-size:11px;margin:0;" data-action="ad-set-location">Set Location</button>'
            : "";
          var starTitle = isDefault ? "Default profile" : "Set as default profile";
          var starClass = "ad-star" + (isDefault ? " is-default" : "");
          var starBtn = '<button type="button" class="' + starClass + '"'
            + ' data-action="ad-set-default"'
            + ' data-chart-record="' + r.chartRecordId + '"'
            + ' title="' + starTitle + '"'
            + ' aria-label="' + (isDefault ? "Default profile" : "Set " + r.displayName + " as default") + '"'
            + ' aria-pressed="' + (isDefault ? "true" : "false") + '"'
            + '>' + (isDefault ? "\u2605" : "\u2606") + '</button>';
          return '<div class="ad-profile-row">'
            + '<span>' + dot + r.displayName + city + '</span>'
            + '<div class="ad-row-actions">' + starBtn + locBtn + '</div>'
            + '</div>';
        }).join("");
      } else {
        profilesHtml = '<p style="font-size:12px;color:#94a3b8;margin:0;">No profiles loaded.</p>';
      }
    } catch (e) {
      profilesHtml = '<p style="font-size:12px;color:#94a3b8;margin:0;">Could not load profiles.</p>';
    }

    var activeProfileName = activeRecord ? activeRecord.displayName : "\u2014";
    var activeCity = activeRecord
      ? (activeRecord.currentCity && activeRecord.currentCity !== "\u2014" ? activeRecord.currentCity : "Not set")
      : "\u2014";
    var profileCount = 0;
    try {
      var vm2 = window.__rmAppShell && window.__rmAppShell.viewModel();
      profileCount = (vm2 && vm2.chartRecords && vm2.chartRecords.length) || 0;
    } catch (e) {}

    return [
      '<div class="ad-header">',
      '  <h2>Account</h2>',
      '  <button class="ad-close" id="rm-ad-close" aria-label="Close">\u00d7</button>',
      '</div>',

      '<div class="ad-section">',
      '  <div class="ad-section-label">A \u2014 Account</div>',
      '  <div class="ad-field"><span class="label">Name</span>' + accountName + '</div>',
      '  <div class="ad-field"><span class="label">Type</span>' + accountType + '</div>',
      '  <div class="ad-field"><span class="label">Role</span>' + role + '</div>',
      '  <div class="ad-field"><span class="label">Active profile</span>' + activeProfileName + '</div>',
      '  <div class="ad-field"><span class="label">Current location</span>' + activeCity + '</div>',
      '</div>',

      '<div class="ad-section">',
      '  <div class="ad-section-label">B \u2014 Profiles (' + profileCount + ')</div>',
      profilesHtml,
      '  <div id="ad-default-msg" aria-live="polite"></div>',
      '  <button type="button" class="ad-btn" style="margin-top:10px;" data-action="ad-add-profile">+ Add Profile</button>',
      '</div>',

      '<div class="ad-section">',
      '  <div class="ad-section-label">C \u2014 Preferences</div>',
      '  <button type="button" class="ad-btn" data-action="ad-settings">Settings \u2192</button>',
      '</div>',

      '<div class="ad-section">',
      '  <div class="ad-section-label">D \u2014 Help</div>',
      '  <button type="button" class="ad-btn" data-action="ad-help">Learn &amp; Tutorials</button>',
      '  <button type="button" class="ad-btn" data-action="ad-help">About Relocation Astrology</button>',
      '  <a href="mailto:feedback@relocationapp.com" style="display:block;font-size:13px;color:#7c3aed;padding:5px 0;">Feedback \u2197</a>',
      '</div>',

      '<div class="ad-logout-section">',
      '  <button type="button" class="ad-btn primary" data-action="ad-logout">Log out</button>',
      '</div>',
    ].join("\n");
  }

  /* Re-renders star buttons in an already-open drawer without rebuilding everything. */
  function refreshProfilesSection(drawer, newDefaultId) {
    try {
      var vm = window.__rmAppShell && window.__rmAppShell.viewModel();
      var records = (vm && vm.chartRecords) || [];
      var rows = drawer.querySelectorAll(".ad-profile-row");
      records.forEach(function (r, i) {
        var row = rows[i];
        if (!row) return;
        var isDefault = r.chartRecordId === newDefaultId;
        var starBtn = row.querySelector(".ad-star");
        if (!starBtn) return;
        starBtn.textContent = isDefault ? "\u2605" : "\u2606";
        starBtn.className   = "ad-star" + (isDefault ? " is-default" : "");
        starBtn.title       = isDefault ? "Default profile" : "Set as default profile";
        starBtn.setAttribute("aria-label", isDefault ? "Default profile" : "Set " + r.displayName + " as default");
        starBtn.setAttribute("aria-pressed", isDefault ? "true" : "false");
      });
    } catch (e) { /* non-fatal — drawer rebuilds on next open */ }
  }

  function open() {
    var scrim  = document.getElementById(SCRIM_ID);
    var drawer = document.getElementById(DRAWER_ID);
    if (!scrim || !drawer) return;
    drawer.innerHTML = buildDrawerHtml();
    scrim.classList.add("open");
    drawer.classList.add("open");
    attachDrawerListeners(drawer);
  }

  function close() {
    var scrim  = document.getElementById(SCRIM_ID);
    var drawer = document.getElementById(DRAWER_ID);
    if (scrim)  scrim.classList.remove("open");
    if (drawer) drawer.classList.remove("open");
  }

  function attachDrawerListeners(drawer) {
    document.getElementById("rm-ad-close").addEventListener("click", close);

    drawer.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-action]");
      if (!btn) return;
      var action = btn.getAttribute("data-action");

      if (action === "ad-set-default") {
        var newDefaultId = btn.getAttribute("data-chart-record");
        if (!newDefaultId) return;

        var shell = window.__rmAppShell;
        var msgEl = document.getElementById("ad-default-msg");
        if (!shell || typeof shell.setAccountDefaultChartRecord !== "function") {
          if (msgEl) { msgEl.textContent = "Error: helper not available."; msgEl.className = "is-error"; }
          return;
        }

        var prevDefaultId = typeof shell.getAccountDefaultChartRecordId === "function"
          ? shell.getAccountDefaultChartRecordId() : null;
        if (prevDefaultId === newDefaultId) return;

        // Optimistic star repaint only; the shell owns the canonical default value.
        refreshProfilesSection(drawer, newDefaultId);
        if (msgEl) { msgEl.textContent = "Saving\u2026"; msgEl.className = ""; }

        shell.setAccountDefaultChartRecord(newDefaultId)
          .then(function () {
            if (msgEl) {
              msgEl.textContent = "\u2713 Default updated.";
              msgEl.className = "";
              setTimeout(function () { if (msgEl) msgEl.textContent = ""; }, 2500);
            }
          })
          .catch(function (err) {
            refreshProfilesSection(drawer, prevDefaultId);
            if (msgEl) {
              msgEl.textContent = "Error: " + (err && err.message ? err.message : String(err));
              msgEl.className = "is-error";
            }
          });
        return;
      }

      if (action === "ad-add-profile") {
        close();
        if (typeof window.__showFirstProfileIntake === "function") {
          var shellApi = window.__rmAppShell;
          var onCreated = shellApi && typeof shellApi.handleProfileCreated === "function"
            ? shellApi.handleProfileCreated : null;
          window.__showFirstProfileIntake({ mode: "add", onCreated: onCreated });
        }
      }
      if (action === "ad-set-location") {
        var profileId = getActiveProfileId();
        close();
        if (profileId && typeof window.__showCurrentLocationEditor === "function") {
          window.__showCurrentLocationEditor(profileId);
        }
      }
      if (action === "ad-settings") {
        close();
        if (window.__rmAppShell && typeof window.__rmAppShell.navigate === "function") {
          window.__rmAppShell.navigate("settings");
        }
      }
      if (action === "ad-help") {
        close();
        if (window.__rmAppShell && typeof window.__rmAppShell.navigate === "function") {
          window.__rmAppShell.navigate("help");
        }
      }
      if (action === "ad-logout") {
        if (typeof window.logout === "function") {
          window.logout();
        }
      }
    });
  }

  function ensureDom() {
    if (document.getElementById(DRAWER_ID)) return;
    var scrim = document.createElement("div");
    scrim.id = SCRIM_ID;
    scrim.addEventListener("click", close);
    document.body.appendChild(scrim);

    var drawer = document.createElement("div");
    drawer.id = DRAWER_ID;
    drawer.setAttribute("role", "dialog");
    drawer.setAttribute("aria-label", "Account");
    document.body.appendChild(drawer);
  }

  window.__showAccountDrawer = function () {
    injectStyles();
    ensureDom();
    open();
  };

})();
