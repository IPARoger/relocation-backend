/**
 * first_profile_intake.js — first-profile / birth-record intake overlay.
 *
 * Activates when window.SupabaseStoreReady rejects with "Intake overlay required",
 * meaning the authenticated user has no profiles or birth records yet.
 *
 * Shows a minimal overlay:
 *   - Display name
 *   - Birth date
 *   - Birth time mode (exact / unknown)
 *   - Birth time (shown only when mode = exact)
 *   - Birth place search (GET /places/search — alias-aware backend)
 *
 * Write path:
 *   1. INSERT INTO profiles   (account_id, account_user_id*, display_name, profile_type)
 *   2. INSERT INTO birth_records (account_id, profile_id, birth_date, birth_time_mode,
 *                                 birth_time_start, birth_place_id, timezone_id)
 *
 * * account_user_id: still NOT NULL in base schema as of Phase 4.
 *   Populated with CurrentUser.userId. Legacy column — not used for auth or identity.
 *   Will be dropped in a future migration. This is documented and intentional.
 *
 * Compensation on birth_record failure:
 *   If the birth_records INSERT fails, the just-created profile is deleted.
 *   This is a best-effort compensating DELETE (not a SQL transaction).
 *   If the compensating DELETE also fails, an error is surfaced and the orphan
 *   profile is left for manual cleanup. The user is shown a clear retry message.
 *
 * On success: redirect to /map_CURRENT.html with app_shell handoff params (skipOnboarding, handoff, handoffCreatedAt, chartRecordId=profileId).
 *
 * Exposes:
 *   window.__showFirstProfileIntake() — called by app_shell.html on INTAKE_REQUIRED
 */
(function () {
  "use strict";

  var INTAKE_OVERLAY_ID = "rm-first-profile-intake";
  var overlayShown = false;

  // Launch context (Phase 1 plumbing). Captured when the overlay is shown so
  // later phases can branch first-run vs. future Add Profile behavior. Default
  // mode "first" preserves existing first-run onboarding behavior exactly.
  var DEFAULT_LAUNCH_CONTEXT = { mode: "first", onCreated: null };
  var launchContext = DEFAULT_LAUNCH_CONTEXT;

  function normalizeLaunchOptions(options) {
    var opts = options || {};
    var mode = opts.mode === "add" ? "add" : "first";
    var onCreated = typeof opts.onCreated === "function" ? opts.onCreated : null;
    return { mode: mode, onCreated: onCreated };
  }

  // ── Styles ─────────────────────────────────────────────────────────────────

  var CSS = [
    "#" + INTAKE_OVERLAY_ID + " {",
    "  position:fixed; inset:0; z-index:99999;",
    "  background:rgba(10,10,20,0.82); backdrop-filter:blur(4px);",
    "  display:flex; align-items:center; justify-content:center;",
    "  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .card {",
    "  background:#1a1a2e; border:1px solid #2d2d4e; border-radius:12px;",
    "  padding:32px; width:100%; max-width:420px; color:#e0e0f0;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " h2 {",
    "  margin:0 0 6px; font-size:1.3rem; font-weight:600; color:#c8b8ff;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .subtitle {",
    "  margin:0 0 24px; font-size:0.85rem; color:#8080a0;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .field { margin-bottom:16px; }",
    "#" + INTAKE_OVERLAY_ID + " label {",
    "  display:block; font-size:0.78rem; color:#8888aa; margin-bottom:5px;",
    "  text-transform:uppercase; letter-spacing:0.05em;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " input[type=text],",
    "#" + INTAKE_OVERLAY_ID + " input[type=date],",
    "#" + INTAKE_OVERLAY_ID + " input[type=time] {",
    "  width:100%; box-sizing:border-box;",
    "  background:#0f0f1e; border:1px solid #3a3a5e; border-radius:7px;",
    "  color:#e0e0f0; padding:10px 12px; font-size:0.95rem;",
    "  outline:none; transition:border-color 0.2s;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " input:focus { border-color:#7b61ff; }",
    "#" + INTAKE_OVERLAY_ID + " .mode-row {",
    "  display:flex; gap:10px; margin-bottom:4px;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .mode-btn {",
    "  flex:1; padding:8px; border-radius:7px; border:1px solid #3a3a5e;",
    "  background:#0f0f1e; color:#9090b8; font-size:0.85rem; cursor:pointer;",
    "  transition:all 0.15s;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .mode-btn.active {",
    "  background:#2a1f5e; border-color:#7b61ff; color:#c8b8ff;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .place-results {",
    "  position:absolute; width:100%; background:#1a1a2e;",
    "  border:1px solid #3a3a5e; border-top:none; border-radius:0 0 7px 7px;",
    "  max-height:180px; overflow-y:auto; z-index:10;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .place-result {",
    "  padding:9px 12px; font-size:0.9rem; cursor:pointer; color:#c0c0e0;",
    "  border-bottom:1px solid #252540;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .place-result:hover { background:#252550; }",
    "#" + INTAKE_OVERLAY_ID + " .place-result.selected { background:#1f1f48; color:#c8b8ff; }",
    "#" + INTAKE_OVERLAY_ID + " .place-wrap { position:relative; }",
    "#" + INTAKE_OVERLAY_ID + " .searching { font-size:0.78rem; color:#8080a0; margin-top:4px; }",
    "#" + INTAKE_OVERLAY_ID + " .submit-btn {",
    "  width:100%; padding:12px; border-radius:8px; border:none;",
    "  background:#7b61ff; color:#fff; font-size:1rem; font-weight:600;",
    "  cursor:pointer; margin-top:8px; transition:opacity 0.2s;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .submit-btn:disabled { opacity:0.4; cursor:default; }",
    "#" + INTAKE_OVERLAY_ID + " .err-msg {",
    "  margin-top:12px; padding:10px 12px; border-radius:7px;",
    "  background:#2a0a0a; border:1px solid #7a2020; color:#f08080;",
    "  font-size:0.85rem; display:none;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .err-msg.visible { display:block; }",
  ].join("\n");

  function injectStyles() {
    var el = document.createElement("style");
    el.textContent = CSS;
    document.head.appendChild(el);
  }

  // ── State ───────────────────────────────────────────────────────────────────

  var state = {
    displayName:  "",
    birthDate:    "",
    birthTimeMode: "exact",
    birthTime:    "",
    placeQuery:   "",
    selectedPlace: null,   // { id, display_name, timezone_id }
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
      item.className = "place-result";
      // display_name already includes region + country (post ADMIN1-FIX-3),
      // so we do not re-append admin1/country_code (avoids duplicate labels).
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

  // ── Insert logic ────────────────────────────────────────────────────────────

  async function submitIntake() {
    var errEl = document.getElementById("rm-intake-err");
    var submitBtn = document.getElementById("rm-intake-submit");

    function showError(msg) {
      if (errEl) { errEl.textContent = msg; errEl.className = "err-msg visible"; }
      if (submitBtn) submitBtn.disabled = false;
      state.submitting = false;
    }

    // Validate
    var displayName = (document.getElementById("rm-intake-name") || {}).value || "";
    var birthDate   = (document.getElementById("rm-intake-date") || {}).value || "";
    var birthTime   = state.birthTimeMode === "exact"
      ? (document.getElementById("rm-intake-time") || {}).value || ""
      : null;

    displayName = displayName.trim();

    if (!displayName) return showError("Display name is required.");
    if (!birthDate)   return showError("Birth date is required.");
    if (state.birthTimeMode === "exact" && !birthTime) {
      return showError("Birth time is required when mode is Exact. Switch to Unknown if time is not known.");
    }
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

      // Backend owns the write (POST /profiles/create-with-birth); supply JWT.
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
          birth_time_mode: state.birthTimeMode,
          birth_time_start: state.birthTimeMode === "exact" ? birthTime + ":00" : null,
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

      // ── Success ─────────────────────────────────────────────────────────
      // Future Add Profile (mode "add"): hand the new profile back to the shell
      // and do NOT redirect. Requires a valid onCreated callback; otherwise we
      // fall back to the original first-run redirect for safety.
      if (launchContext.mode === "add" && typeof launchContext.onCreated === "function") {
        console.log("[intake] Profile and birth record created (add mode). Handing off to shell.");
        var onCreatedCb = launchContext.onCreated;
        var switchEl = document.getElementById("rm-intake-switch");
        var switchToNew = switchEl ? !!switchEl.checked : true;
        removeOverlay();
        onCreatedCb(profileId, { switchToNew: switchToNew });
        return;
      }

      // First-run onboarding (default mode "first"): continue into the map flow.
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

    overlay.innerHTML = [
      '<div class="card">',
      '  <h2>Create profile and chart record</h2>',
      '  <p class="subtitle">Enter birth details to create a profile and its chart record. Current location is set separately, later.</p>',

      '  <div class="field">',
      '    <label for="rm-intake-name">Display name</label>',
      '    <input type="text" id="rm-intake-name" placeholder="e.g. Anna Rivera" autocomplete="off" />',
      '  </div>',

      '  <div class="field">',
      '    <label for="rm-intake-date">Birth date</label>',
      '    <input type="date" id="rm-intake-date" />',
      '  </div>',

      '  <div class="field">',
      '    <label>Birth time</label>',
      '    <div class="mode-row">',
      '      <button type="button" class="mode-btn active" id="rm-mode-exact" data-mode="exact">Exact</button>',
      '      <button type="button" class="mode-btn" id="rm-mode-unknown" data-mode="unknown">Unknown</button>',
      '    </div>',
      '  </div>',

      '  <div class="field" id="rm-time-field">',
      '    <label for="rm-intake-time">Time</label>',
      '    <input type="time" id="rm-intake-time" />',
      '  </div>',

      '  <div class="field">',
      '    <label for="rm-intake-place-input">Birth city</label>',
      '    <div class="place-wrap">',
      '      <input type="text" id="rm-intake-place-input"',
      '             placeholder="Start typing a city name…" autocomplete="off" />',
      '      <button type="button" id="rm-intake-place-clear"',
      '              style="display:none;position:absolute;right:8px;top:8px;',
      '                     background:none;border:none;color:#8888aa;cursor:pointer;font-size:0.8rem;"',
      '              >✕ clear</button>',
      '      <div class="place-results" id="rm-intake-place-results" style="display:none;"></div>',
      '    </div>',
      '    <div class="searching" id="rm-intake-searching" style="display:none;">Searching…</div>',
      '    <p class="meta" style="font-size:11px;color:#8888aa;margin:4px 0 0;">Select a birth city from the available list.</p>',
      '  </div>',

      (launchContext.mode === "add"
        ? '  <label class="field" style="display:flex;align-items:center;gap:8px;font-size:13px;cursor:pointer;">'
          + '<input type="checkbox" id="rm-intake-switch" checked style="width:auto;margin:0;" />'
          + 'Switch to new profile</label>'
        : ''),
      '  <button type="button" class="submit-btn" id="rm-intake-submit">',
      '    Create my chart',
      '  </button>',
      '  <div class="err-msg" id="rm-intake-err"></div>',
      '</div>',
    ].join("\n");

    return overlay;
  }

  function attachListeners(overlay) {
    // Mode toggle
    overlay.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-mode]");
      if (!btn) return;
      state.birthTimeMode = btn.getAttribute("data-mode");
      overlay.querySelectorAll(".mode-btn").forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });
      var timeField = document.getElementById("rm-time-field");
      if (timeField) timeField.style.display = state.birthTimeMode === "exact" ? "block" : "none";
    });

    // Place search (debounced 300ms)
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

    // Place clear button
    var clearBtn = document.getElementById("rm-intake-place-clear");
    if (clearBtn) clearBtn.addEventListener("click", clearPlace);

    // Submit
    var submitBtn = document.getElementById("rm-intake-submit");
    if (submitBtn) submitBtn.addEventListener("click", submitIntake);
  }

  // ── Remove overlay ──────────────────────────────────────────────────────────

  // Removes the overlay from the DOM and resets state so a later launch (e.g.
  // first-run) starts clean. Used by the add-mode success handoff.
  function removeOverlay() {
    var existing = document.getElementById(INTAKE_OVERLAY_ID);
    if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
    overlayShown = false;
    launchContext = DEFAULT_LAUNCH_CONTEXT;
  }

  // ── Google OAuth name prefill (intake only) ─────────────────────────────────

  function userSignedInWithGoogle(user) {
    if (!user) return false;
    var ids = user.identities || [];
    for (var i = 0; i < ids.length; i++) {
      if (ids[i].provider === "google") return true;
    }
    return !!(user.app_metadata && user.app_metadata.provider === "google");
  }

  function prefillNameFromGoogleMetadata() {
    if (typeof window.SupabaseReady === "undefined") return;
    window.SupabaseReady.then(function (client) {
      return client.auth.getSession();
    }).then(function (result) {
      var session = result && result.data && result.data.session;
      var user = session && session.user;
      if (!user || !userSignedInWithGoogle(user)) return;
      var meta = user.user_metadata || {};
      var name = String(meta.full_name || meta.name || "").trim();
      if (!name) return;
      var nameInput = document.getElementById("rm-intake-name");
      if (nameInput && !String(nameInput.value || "").trim()) {
        nameInput.value = name;
      }
    }).catch(function () { /* no session — skip prefill */ });
  }

  // ── Show overlay ────────────────────────────────────────────────────────────

  function showOverlay(options) {
    if (overlayShown) return;
    launchContext = normalizeLaunchOptions(options);
    overlayShown = true;

    injectStyles();
    var overlay = buildOverlay();
    document.body.appendChild(overlay);
    attachListeners(overlay);
    prefillNameFromGoogleMetadata();

    // Focus name field
    setTimeout(function () {
      var nameInput = document.getElementById("rm-intake-name");
      if (nameInput) nameInput.focus();
    }, 100);
  }

  // ── Activation ──────────────────────────────────────────────────────────────

  /**
   * Called by app_shell.html when INTAKE_REQUIRED is detected (no args =>
   * first-run onboarding), and by shell Add Profile entry points.
   * @param {{mode?: "first"|"add", onCreated?: Function}} [options]
   */
  window.__showFirstProfileIntake = showOverlay;

  /**
   * Also self-activate: listen to SupabaseStoreReady independently.
   * Handles the case where the overlay needs to appear even if app_shell
   * is not yet initialized.
   */
  if (typeof window.SupabaseStoreReady !== "undefined") {
    window.SupabaseStoreReady.catch(function (err) {
      if (err && err.message && err.message.indexOf("Intake overlay required") !== -1) {
        showOverlay();
      }
    });
  }

})();
