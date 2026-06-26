/**
 * first_profile_intake.js — first-profile / birth-record intake overlay.
 *
 * Activates when window.SupabaseStoreReady rejects with "Intake overlay required",
 * meaning the authenticated user has no profiles or birth records yet.
 *
 * Beta fields: Birth Date, Birth Time (required), Birth Place.
 * Display name is resolved silently (Google metadata or fallback).
 *
 * Write path: POST /profiles/create-with-birth
 *
 * On success: redirect to /map_CURRENT.html with app_shell handoff params.
 *
 * Exposes: window.__showFirstProfileIntake()
 */
(function () {
  "use strict";

  var INTAKE_OVERLAY_ID = "rm-first-profile-intake";
  var overlayShown = false;

  var DEFAULT_LAUNCH_CONTEXT = { mode: "first", onCreated: null };
  var launchContext = DEFAULT_LAUNCH_CONTEXT;

  function normalizeLaunchOptions(options) {
    var opts = options || {};
    var mode = opts.mode === "add" ? "add" : "first";
    var onCreated = typeof opts.onCreated === "function" ? opts.onCreated : null;
    return { mode: mode, onCreated: onCreated };
  }

  // ── Styles (instrument surface — matches auth.html / family_resemblance) ──

  var CSS = [
    "#" + INTAKE_OVERLAY_ID + " {",
    "  position:fixed; inset:0; z-index:99999;",
    "  display:flex; align-items:center; justify-content:center;",
    "  padding:32px 20px; overflow-y:auto;",
    "  font-family:\"Avenir Next\",\"Segoe UI\",-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;",
    "  font-size:15.5px; line-height:1.5; color:var(--rm-ink,#33291f);",
    "  background:",
    "    radial-gradient(58% 50% at 12% -4%, rgba(214,176,108,.16), transparent 60%),",
    "    radial-gradient(50% 44% at 98% 4%, rgba(150,178,150,.10), transparent 60%),",
    "    radial-gradient(70% 60% at 86% 96%, rgba(120,160,185,.09), transparent 62%),",
    "    var(--rm-paper,#f4ecdc);",
    "  -webkit-font-smoothing:antialiased;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .rm-intake-journey { width:100%; max-width:400px; }",
    "#" + INTAKE_OVERLAY_ID + " .rm-intake-wordmark {",
    "  font-family:\"Iowan Old Style\",\"Palatino Linotype\",Palatino,Georgia,serif;",
    "  font-size:1.35rem; font-weight:600; text-align:center; margin:0 0 8px;",
    "  color:var(--rm-ink,#33291f);",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .card {",
    "  background:var(--rm-card,#fdf8ee); border:1px solid var(--rm-line,#ddd0b8);",
    "  border-radius:12px; padding:26px 24px 24px; width:100%;",
    "  box-shadow:0 1px 2px rgba(51,41,31,.06),0 14px 32px -20px rgba(51,41,31,.16);",
    "}",
    "#" + INTAKE_OVERLAY_ID + " h2 {",
    "  font-family:\"Iowan Old Style\",\"Palatino Linotype\",Palatino,Georgia,serif;",
    "  font-size:1.35rem; font-weight:600; margin:0 0 6px; text-align:center;",
    "  color:var(--rm-ink,#33291f);",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .subtitle {",
    "  margin:0 0 22px; font-size:13px; color:var(--rm-ink-soft,#6a5f4f);",
    "  text-align:center; line-height:1.45;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .field { margin-bottom:14px; }",
    "#" + INTAKE_OVERLAY_ID + " label {",
    "  display:block; font-size:12px; font-weight:600; color:var(--rm-ink-soft,#6a5f4f);",
    "  margin-bottom:6px; letter-spacing:.01em;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " input[type=text],",
    "#" + INTAKE_OVERLAY_ID + " input[type=date],",
    "#" + INTAKE_OVERLAY_ID + " input[type=time] {",
    "  width:100%; box-sizing:border-box;",
    "  background:var(--rm-card,#fdf8ee); border:1px solid var(--rm-line,#ddd0b8);",
    "  border-radius:10px; color:var(--rm-ink,#33291f); padding:10px 12px;",
    "  font:inherit; font-size:14px; outline:none;",
    "  transition:border-color .15s, box-shadow .15s;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " input:focus {",
    "  border-color:var(--rm-accent,#5b6b63);",
    "  box-shadow:0 0 0 2px color-mix(in srgb, var(--rm-accent,#5b6b63) 14%, transparent);",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .hint {",
    "  font-size:11.5px; color:var(--rm-ink-faint,#9b9080); margin-top:5px; line-height:1.4;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .rm-sls-wrap {",
    "  display:flex; align-items:center; position:relative;",
    "  background:var(--rm-card,#fdf8ee); border:1px solid var(--rm-line,#ddd0b8);",
    "  border-radius:10px; padding:0 12px;",
    "  box-shadow:inset 0 1px 0 rgba(255,255,255,.4);",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .rm-sls-input {",
    "  flex:1; border:none; background:transparent; padding:10px 0;",
    "  font:inherit; font-size:14px; color:var(--rm-ink,#33291f); outline:none;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .rm-sls-clear {",
    "  border:none; background:transparent; color:var(--rm-ink-faint,#9b9080);",
    "  cursor:pointer; font-size:12px; padding:4px 0 4px 8px;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .rm-sls-panel {",
    "  position:absolute; left:0; right:0; top:calc(100% + 4px);",
    "  background:var(--rm-card,#fdf8ee); border:1px solid var(--rm-line,#ddd0b8);",
    "  border-radius:10px; max-height:180px; overflow-y:auto; z-index:10;",
    "  box-shadow:0 4px 16px -8px rgba(51,41,31,.2);",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .rm-sls-item {",
    "  padding:9px 14px; font-size:13.5px; cursor:pointer;",
    "  color:var(--rm-ink,#33291f); border-bottom:1px solid var(--rm-line-soft,#ece2cf);",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .rm-sls-item:hover { background:var(--rm-line-soft,#ece2cf); }",
    "#" + INTAKE_OVERLAY_ID + " .rm-sls-item:last-child { border-bottom:none; }",
    "#" + INTAKE_OVERLAY_ID + " .place-wrap { position:relative; }",
    "#" + INTAKE_OVERLAY_ID + " .searching {",
    "  font-size:11.5px; color:var(--rm-ink-faint,#9b9080); margin-top:5px;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .submit-btn {",
    "  width:100%; padding:12px 16px; border-radius:10px;",
    "  border:1px solid #465650; background:var(--rm-accent,#5b6b63);",
    "  color:var(--rm-card,#fdf8ee); font:inherit; font-size:14px; font-weight:600;",
    "  cursor:pointer; margin-top:8px; box-shadow:0 1px 2px rgba(51,41,31,.1);",
    "  transition:filter .15s, opacity .15s;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .submit-btn:hover:not(:disabled) { filter:brightness(1.03); }",
    "#" + INTAKE_OVERLAY_ID + " .submit-btn:disabled { opacity:0.5; cursor:default; }",
    "#" + INTAKE_OVERLAY_ID + " .err-msg {",
    "  margin-top:12px; padding:10px 12px; border-radius:10px;",
    "  background:#fff5f5; border:1px solid #e8c4c4; color:#7f1d1d;",
    "  font-size:13px; display:none;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .err-msg.visible { display:block; }",
    "#" + INTAKE_OVERLAY_ID + " .sr-only {",
    "  position:absolute; width:1px; height:1px; padding:0; margin:-1px;",
    "  overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0;",
    "}",
  ].join("\n");

  function injectStyles() {
    if (!document.getElementById("rm-intake-family-css")) {
      var link = document.createElement("link");
      link.id = "rm-intake-family-css";
      link.rel = "stylesheet";
      link.href = "/theme/family_resemblance.css";
      document.head.appendChild(link);
    }
    if (document.getElementById("rm-intake-styles")) return;
    var el = document.createElement("style");
    el.id = "rm-intake-styles";
    el.textContent = CSS;
    document.head.appendChild(el);
  }

  // ── State ───────────────────────────────────────────────────────────────────

  var state = {
    birthDate:    "",
    birthTime:    "",
    placeQuery:   "",
    selectedPlace: null,
    placeResults:  [],
    searching:    false,
    submitting:   false,
  };

  var searchTimer = null;

  // ── Place search ────────────────────────────────────────────────────────────

  async function searchPlaces(query) {
    if (!query || query.length < 2) {
      state.placeResults = [];
      renderResults();
      return;
    }
    state.searching = true;
    renderSearching(true);

    try {
      var searchApi = window.RMPlaceSearch;
      if (!searchApi || typeof searchApi.searchPlaces !== "function") {
        throw new Error("RMPlaceSearch unavailable");
      }
      state.placeResults = await searchApi.searchPlaces(query, 10);
    } catch (err) {
      state.placeResults = [];
      console.warn("[intake] place search error:", err.message);
    } finally {
      state.searching = false;
      renderSearching(false);
      renderResults();
    }
  }

  function renderSearching(active) {
    var el = document.getElementById("rm-intake-searching");
    if (el) el.style.display = active ? "block" : "none";
  }

  function renderResults() {
    var container = document.getElementById("rm-intake-place-results");
    if (!container) return;
    container.innerHTML = "";
    if (state.selectedPlace) {
      container.style.display = "none";
      return;
    }
    if (state.placeResults.length === 0) {
      container.style.display = "none";
      return;
    }
    container.style.display = "block";
    state.placeResults.forEach(function (place) {
      var item = document.createElement("div");
      item.className = "rm-sls-item";
      var label = place.display_name;
      item.textContent = label;
      item.addEventListener("click", function () {
        selectPlace(place, label);
      });
      container.appendChild(item);
    });
  }

  function selectPlace(place, label) {
    state.selectedPlace  = place;
    state.placeResults   = [];
    var input = document.getElementById("rm-intake-place-input");
    if (input) {
      input.value    = label || place.display_name;
      input.readOnly = true;
    }
    var container = document.getElementById("rm-intake-place-results");
    if (container) container.style.display = "none";
    var clearBtn = document.getElementById("rm-intake-place-clear");
    if (clearBtn) clearBtn.style.display = "inline";
  }

  function clearPlace() {
    state.selectedPlace = null;
    state.placeResults  = [];
    var input = document.getElementById("rm-intake-place-input");
    if (input) {
      input.value    = "";
      input.readOnly = false;
      input.focus();
    }
    var clearBtn = document.getElementById("rm-intake-place-clear");
    if (clearBtn) clearBtn.style.display = "none";
  }

  // ── Display name (silent for first-run) ─────────────────────────────────────

  function userSignedInWithGoogle(user) {
    if (!user) return false;
    var ids = user.identities || [];
    for (var i = 0; i < ids.length; i++) {
      if (ids[i].provider === "google") return true;
    }
    return !!(user.app_metadata && user.app_metadata.provider === "google");
  }

  function prefillNameFromGoogleMetadata() {
    resolveDisplayName().catch(function () { /* no session — skip prefill */ });
  }

  async function resolveDisplayName() {
    var nameInput = document.getElementById("rm-intake-name");
    var fromInput = nameInput ? String(nameInput.value || "").trim() : "";
    if (fromInput) return fromInput;

    if (typeof window.SupabaseReady === "undefined") return "My Profile";

    try {
      var client = await window.SupabaseReady;
      var result = await client.auth.getSession();
      var user = result && result.data && result.data.session && result.data.session.user;
      if (user) {
        if (userSignedInWithGoogle(user)) {
          var meta = user.user_metadata || {};
          var googleName = String(meta.full_name || meta.name || "").trim();
          if (googleName) {
            if (nameInput) nameInput.value = googleName;
            return googleName;
          }
        }
        var email = String(user.email || "").trim();
        if (email.indexOf("@") > 0) {
          var local = email.split("@")[0].replace(/[._+\-]+/g, " ").trim();
          if (local) {
            if (nameInput) nameInput.value = local;
            return local;
          }
        }
      }
    } catch (e) { /* fall through */ }

    return "My Profile";
  }

  // ── Insert logic ────────────────────────────────────────────────────────────

  async function submitIntake() {
    var errEl = document.getElementById("rm-intake-err");
    var submitBtn = document.getElementById("rm-intake-submit");

    function showError(msg) {
      if (errEl) { errEl.textContent = msg; errEl.className = "err-msg visible"; }
      if (submitBtn) submitBtn.disabled = false;
      state.submitting = false;
    }

    var displayName = await resolveDisplayName();
    var birthDate   = (document.getElementById("rm-intake-date") || {}).value || "";
    var birthTime   = (document.getElementById("rm-intake-time") || {}).value || "";

    if (!birthDate)   return showError("Birth date is required.");
    if (!birthTime)   return showError("Birth time is required.");
    if (!state.selectedPlace) return showError("Birth place is required. Search and select a city.");

    state.submitting = true;
    if (submitBtn) submitBtn.disabled = true;
    if (errEl) errEl.className = "err-msg";

    var currentUser = window.CurrentUser;
    if (!currentUser || !currentUser.accountId) {
      return showError("Session error. Please reload the page and try again.");
    }

    try {
      var client    = await window.SupabaseReady;
      var accountId = currentUser.accountId;
      var userId    = currentUser.userId;

      var sessionResult = await client.auth.getSession();
      var session = sessionResult && sessionResult.data ? sessionResult.data.session : null;
      var token = session && session.access_token;
      if (!token) return showError("Session error. Please reload the page and try again.");

      var createResp = await fetch("/profiles/create-with-birth", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token,
        },
        body: JSON.stringify({
          display_name: displayName,
          birth_date: birthDate,
          birth_time_mode: "exact",
          birth_time_start: birthTime + ":00",
          birth_place_id: state.selectedPlace.id,
          timezone_id: state.selectedPlace.timezone_id || null,
          profile_type: "human",
        }),
      });

      if (!createResp.ok) {
        var errDetail = null;
        try { errDetail = (await createResp.json()).detail; } catch (e) { /* non-JSON */ }
        var errReason = errDetail && errDetail.error;
        var errMsg = (errDetail && errDetail.message) || ("HTTP " + createResp.status);
        if (errReason === "rollback_failed" && errDetail && errDetail.profile_id) {
          console.error(
            "[intake] Compensating profile delete FAILED. Orphan profile left:",
            errDetail.profile_id, errMsg
          );
          return showError(
            "Birth record creation failed AND profile cleanup failed. " +
            "Orphan profile ID: " + errDetail.profile_id + ". " +
            "Contact support or delete the profile manually. Error: " + errMsg
          );
        }
        if (errReason === "birth_record_failed") {
          return showError(
            "Birth record creation failed (profile was cleaned up). " +
            "Please try again. Error: " + errMsg
          );
        }
        return showError("Could not create profile: " + errMsg);
      }

      var created = await createResp.json();
      var profileId = created.profile_id;

      if (launchContext.mode === "add" && typeof launchContext.onCreated === "function") {
        console.log("[intake] Profile and birth record created (add mode). Handing off to shell.");
        var onCreatedCb = launchContext.onCreated;
        var switchEl = document.getElementById("rm-intake-switch");
        var switchToNew = switchEl ? !!switchEl.checked : true;
        removeOverlay();
        onCreatedCb(profileId, { switchToNew: switchToNew });
        return;
      }

      console.log("[intake] Profile and birth record created. Redirecting to map...");
      var handoffCreatedAt = new Date().toISOString();
      window.location.href =
        '/map_CURRENT.html?skipOnboarding=1&handoff=app_shell' +
        '&handoffCreatedAt=' + encodeURIComponent(handoffCreatedAt) +
        '&chartRecordId=' + encodeURIComponent(profileId);

    } catch (err) {
      showError("Unexpected error: " + (err.message || String(err)));
    }
  }

  // ── Overlay DOM ─────────────────────────────────────────────────────────────

  function buildOverlay() {
    var overlay = document.createElement("div");
    overlay.id = INTAKE_OVERLAY_ID;

    var nameField = launchContext.mode === "add"
      ? '  <div class="field">'
        + '<label for="rm-intake-name">Display name</label>'
        + '<input type="text" id="rm-intake-name" placeholder="e.g. Anna Rivera" autocomplete="off" />'
        + '</div>'
      : '  <input type="hidden" id="rm-intake-name" value="" />';

    overlay.innerHTML = [
      '<div class="rm-intake-journey">',
      '  <p class="rm-intake-wordmark">Relocation</p>',
      '  <div class="card">',
      '    <h2>Birth information</h2>',
      '    <p class="subtitle">Exact birth time is required for relocation overlays.</p>',
      nameField,
      '    <div class="field">',
      '      <label for="rm-intake-date">Birth date</label>',
      '      <input type="date" id="rm-intake-date" />',
      '    </div>',
      '    <div class="field">',
      '      <label for="rm-intake-time">Birth time</label>',
      '      <input type="time" id="rm-intake-time" />',
      '      <p class="hint">24-hour local time at birth place.</p>',
      '    </div>',
      '    <div class="field">',
      '      <label for="rm-intake-place-input">Birth location</label>',
      '      <div class="place-wrap">',
      '        <div class="rm-sls-wrap">',
      '          <input type="text" class="rm-sls-input" id="rm-intake-place-input"',
      '                 placeholder="Search city…" autocomplete="off" />',
      '          <button type="button" class="rm-sls-clear" id="rm-intake-place-clear"',
      '                  style="display:none;">Clear</button>',
      '        </div>',
      '        <div class="rm-sls-panel" id="rm-intake-place-results" style="display:none;"></div>',
      '      </div>',
      '      <div class="searching" id="rm-intake-searching" style="display:none;">Searching…</div>',
      '      <p class="hint">Select from search results.</p>',
      '    </div>',
      (launchContext.mode === "add"
        ? '    <label class="field" style="display:flex;align-items:center;gap:8px;font-size:13px;cursor:pointer;">'
          + '<input type="checkbox" id="rm-intake-switch" checked style="width:auto;margin:0;" />'
          + 'Switch to new profile</label>'
        : ''),
      '    <button type="button" class="submit-btn" id="rm-intake-submit">Continue</button>',
      '    <div class="err-msg" id="rm-intake-err"></div>',
      '  </div>',
      '</div>',
    ].join("\n");

    return overlay;
  }

  function attachListeners(overlay) {
    var placeInput = document.getElementById("rm-intake-place-input");
    if (placeInput) {
      placeInput.addEventListener("input", function (e) {
        state.placeQuery = e.target.value;
        state.selectedPlace = null;
        clearTimeout(searchTimer);
        searchTimer = setTimeout(function () {
          searchPlaces(state.placeQuery);
        }, 300);
      });
    }

    var clearBtn = document.getElementById("rm-intake-place-clear");
    if (clearBtn) clearBtn.addEventListener("click", clearPlace);

    var submitBtn = document.getElementById("rm-intake-submit");
    if (submitBtn) submitBtn.addEventListener("click", submitIntake);
  }

  function removeOverlay() {
    var existing = document.getElementById(INTAKE_OVERLAY_ID);
    if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
    overlayShown = false;
    launchContext = DEFAULT_LAUNCH_CONTEXT;
  }

  function showOverlay(options) {
    if (overlayShown) return;
    launchContext = normalizeLaunchOptions(options);
    overlayShown = true;

    injectStyles();
    var overlay = buildOverlay();
    overlay.classList.add("rm-instrument-surface");
    document.body.appendChild(overlay);
    attachListeners(overlay);
    prefillNameFromGoogleMetadata();

    setTimeout(function () {
      var dateInput = document.getElementById("rm-intake-date");
      if (dateInput) dateInput.focus();
    }, 100);
  }

  window.__showFirstProfileIntake = showOverlay;

  if (typeof window.SupabaseStoreReady !== "undefined") {
    window.SupabaseStoreReady.catch(function (err) {
      if (err && err.message && err.message.indexOf("Intake overlay required") !== -1) {
        showOverlay();
      }
    });
  }

})();
