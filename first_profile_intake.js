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
    var mode = opts.mode === "add" ? "add" : (opts.mode === "rename" ? "rename" : (opts.mode === "edit" ? "edit" : "first"));
    return {
      mode: mode,
      onCreated: typeof opts.onCreated === "function" ? opts.onCreated : null,
      onRenamed: typeof opts.onRenamed === "function" ? opts.onRenamed : null,
      onUpdated: typeof opts.onUpdated === "function" ? opts.onUpdated : null,
      profileId: opts.profileId || null,
      displayName: opts.displayName || "",
    };
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
    "#" + INTAKE_OVERLAY_ID + " .card { position:relative; }",
    "#" + INTAKE_OVERLAY_ID + " .rm-intake-close {",
    "  position:absolute; top:12px; right:12px; width:32px; height:32px;",
    "  border:none; background:transparent; color:var(--rm-ink-soft,#6a5f4f);",
    "  font-size:22px; line-height:1; cursor:pointer; border-radius:8px;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .rm-intake-close:hover { background:var(--rm-line-soft,#ece2cf); }",
    "#" + INTAKE_OVERLAY_ID + " .name-row { display:flex; gap:12px; }",
    "#" + INTAKE_OVERLAY_ID + " .name-row .name-col { flex:1; min-width:0; }",
    "#" + INTAKE_OVERLAY_ID + " .rm-intake-actions {",
    "  display:flex; gap:10px; margin-top:8px;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .cancel-btn {",
    "  flex:1; padding:12px 16px; border-radius:10px;",
    "  border:1px solid var(--rm-line,#ddd0b8); background:var(--rm-card,#fdf8ee);",
    "  color:var(--rm-ink,#33291f); font:inherit; font-size:14px; font-weight:600; cursor:pointer;",
    "}",
    "#" + INTAKE_OVERLAY_ID + " .submit-btn { flex:1; margin-top:0; }",
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
    lastPlaceResults: [],
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
      state.lastPlaceResults = state.placeResults.slice();
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
    var placeInput = document.getElementById("rm-intake-place-input");
    if (state.selectedPlace && placeInput && placeInput.readOnly) {
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
    state.placeQuery = "";
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
    if (launchContext.mode !== "first") return;
    resolveDisplayName().catch(function () { /* no session — skip prefill */ });
  }

  function splitDisplayName(full) {
    var parts = String(full || "").trim().split(/\s+/).filter(Boolean);
    if (!parts.length) return { first: "", last: "" };
    if (parts.length === 1) return { first: parts[0], last: "" };
    return { first: parts[0], last: parts.slice(1).join(" ") };
  }

  function readIntakeDisplayName() {
    var firstEl = document.getElementById("rm-intake-first");
    var lastEl = document.getElementById("rm-intake-last");
    var first = firstEl ? String(firstEl.value || "").trim() : "";
    var last = lastEl ? String(lastEl.value || "").trim() : "";
    var combined = (first + " " + last).trim();
    return combined || "";
  }

  function applyNameFields(first, last) {
    var firstEl = document.getElementById("rm-intake-first");
    var lastEl = document.getElementById("rm-intake-last");
    if (firstEl) firstEl.value = first || "";
    if (lastEl) lastEl.value = last || "";
  }

  async function resolveDisplayName() {
    var fromInput = readIntakeDisplayName();
    if (fromInput) return fromInput;

    if (launchContext.mode !== "first") return "";

    if (typeof window.SupabaseReady === "undefined") return "My Profile";

    try {
      var client = await window.SupabaseReady;
      var result = await client.auth.getSession();
      var user = result && result.data && result.data.session && result.data.session.user;
      if (user && userSignedInWithGoogle(user)) {
        var meta = user.user_metadata || {};
        var given = String(meta.given_name || "").trim();
        var family = String(meta.family_name || "").trim();
        if (given || family) {
          applyNameFields(given, family);
          return (given + " " + family).trim();
        }
        var googleName = String(meta.full_name || meta.name || "").trim();
        if (googleName) {
          var split = splitDisplayName(googleName);
          applyNameFields(split.first, split.last);
          return googleName;
        }
      }
    } catch (e) { /* fall through */ }

    return "My Profile";
  }

  // ── Insert logic ────────────────────────────────────────────────────────────


  function resetIntakeFormState() {
    state.birthDate = "";
    state.birthTime = "";
    state.placeQuery = "";
    state.selectedPlace = null;
    state.placeResults = [];
    state.lastPlaceResults = [];
    state.searching = false;
    state.submitting = false;
  }

  function intakeApiErrorMessage(detail, fallback) {
    if (!detail) return fallback;
    if (typeof detail === "string") return detail;
    if (detail.message) return String(detail.message);
    if (detail.error) return String(detail.error);
    return fallback;
  }

  function normalizeBirthTimeStartForApi(timeVal) {
    var t = String(timeVal || "").trim();
    if (!t) return "";
    if (/^\d{1,2}:\d{2}:\d{2}$/.test(t)) return t;
    if (/^\d{1,2}:\d{2}$/.test(t)) return t + ":00";
    var parsed = parseTimeForInput(t);
    return parsed ? parsed + ":00" : "";
  }

  function matchPlaceResultByLabel(label) {
    var q = String(label || "").trim();
    if (!q) return null;
    var pools = [state.placeResults || [], state.lastPlaceResults || []];
    for (var pi = 0; pi < pools.length; pi++) {
      var list = pools[pi];
      for (var i = 0; i < list.length; i++) {
        if (String(list[i].display_name || "").trim() === q) return list[i];
      }
    }
    return null;
  }

  async function resolveBirthPlaceForSubmit(token) {
    var inputEl = document.getElementById("rm-intake-place-input");
    var inputLabel = inputEl ? String(inputEl.value || "").trim() : "";
    if (!inputLabel) return null;

    var place = state.selectedPlace;
    if (place && place.id) {
      var placeLabel = String(place.display_name || "").trim();
      if (!placeLabel || placeLabel === inputLabel || (inputEl && inputEl.readOnly)) {
        return { id: place.id, timezone_id: place.timezone_id || null };
      }
    }

    var matched = matchPlaceResultByLabel(inputLabel);
    if (matched && matched.id) {
      state.selectedPlace = matched;
      return { id: matched.id, timezone_id: matched.timezone_id || null };
    }

    if (!window.RMPlaceResolution ||
        typeof window.RMPlaceResolution.resolvePlaceFromCitySelection !== "function") {
      return (place && place.id)
        ? { id: place.id, timezone_id: place.timezone_id || null }
        : null;
    }

    var src = matched || place || {};
    var resolved = await window.RMPlaceResolution.resolvePlaceFromCitySelection({
      displayName: inputLabel,
      geonamesId: src.geonames_id || null,
      latitude: src.latitude,
      longitude: src.longitude,
      country: src.country_name || src.country_code || null,
      admin: src.admin1 || null,
      origin: "birth_intake",
    }, { accessToken: token });
    state.selectedPlace = resolved;
    return { id: resolved.id, timezone_id: resolved.timezone_id || null };
  }

  async function submitIntake() {
    var errEl = document.getElementById("rm-intake-err");
    var submitBtn = document.getElementById("rm-intake-submit");

    function showError(msg) {
      if (errEl) { errEl.textContent = msg; errEl.className = "err-msg visible"; }
      if (submitBtn) submitBtn.disabled = false;
      state.submitting = false;
    }


    if (launchContext.mode === "edit") {
      var editName = readIntakeDisplayName();
      if (!editName) return showError("First or last name is required.");
      var editDate = (document.getElementById("rm-intake-date") || {}).value || "";
      var editTime = (document.getElementById("rm-intake-time") || {}).value || "";
      if (!editDate) return showError("Birth date is required.");
      if (!editTime) return showError("Birth time is required.");
      if (!launchContext.profileId) return showError("Profile unavailable. Reload and try again.");
      state.submitting = true;
      if (submitBtn) submitBtn.disabled = true;
      if (errEl) errEl.className = "err-msg";
      try {
        var clientE = await window.SupabaseReady;
        var sessE = (await clientE.auth.getSession()).data.session;
        var tokenE = sessE && sessE.access_token;
        if (!tokenE) return showError("Session error. Please reload and try again.");
        var editPlace = await resolveBirthPlaceForSubmit(tokenE);
        if (!editPlace || !editPlace.id) {
          return showError("Birth place is required. Search and select a city.");
        }
        var editResp = await fetch("/profiles/update-with-birth", {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": "Bearer " + tokenE },
          body: JSON.stringify({
            profile_id: launchContext.profileId,
            display_name: editName,
            birth_date: editDate,
            birth_time_mode: "exact",
            birth_time_start: normalizeBirthTimeStartForApi(editTime),
            birth_place_id: editPlace.id,
            timezone_id: editPlace.timezone_id || null,
          }),
        });
        if (!editResp.ok) {
          var ed = null;
          try { ed = (await editResp.json()).detail; } catch (e) {}
          return showError(intakeApiErrorMessage(ed, "Update failed."));
        }
        var onUpdated = launchContext.onUpdated;
        removeOverlay();
        if (typeof onUpdated === "function") await onUpdated(editName);
        return;
      } catch (err) {
        return showError("Unexpected error: " + (err.message || String(err)));
      }
    }

    if (launchContext.mode === "rename") {
      var renameName = readIntakeDisplayName();
      if (!renameName) return showError("Enter a first or last name.");
      state.submitting = true;
      if (submitBtn) submitBtn.disabled = true;
      if (errEl) errEl.className = "err-msg";
      try {
        var clientR = await window.SupabaseReady;
        var sessR = (await clientR.auth.getSession()).data.session;
        var tokenR = sessR && sessR.access_token;
        if (!tokenR) return showError("Session error. Please reload and try again.");
        var renameResp = await fetch("/profiles/rename", {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": "Bearer " + tokenR },
          body: JSON.stringify({ profile_id: launchContext.profileId, display_name: renameName }),
        });
        if (!renameResp.ok) {
          var rd = null;
          try { rd = (await renameResp.json()).detail; } catch (e) {}
          return showError((rd && rd.message) || "Rename failed.");
        }
        var onRenamed = launchContext.onRenamed;
        removeOverlay();
        if (typeof onRenamed === "function") onRenamed(renameName);
        return;
      } catch (err) {
        return showError("Unexpected error: " + (err.message || String(err)));
      }
    }

    var displayName = await resolveDisplayName();
    if (launchContext.mode === "add") {
      displayName = readIntakeDisplayName();
      if (!displayName) return showError("First or last name is required.");
    }
    var birthDate   = (document.getElementById("rm-intake-date") || {}).value || "";
    var birthTime   = (document.getElementById("rm-intake-time") || {}).value || "";

    if (!birthDate)   return showError("Birth date is required.");
    if (!birthTime)   return showError("Birth time is required.");
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

      var createPlace = await resolveBirthPlaceForSubmit(token);
      if (!createPlace || !createPlace.id) {
        return showError("Birth place is required. Search and select a city.");
      }

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
          birth_time_start: normalizeBirthTimeStartForApi(birthTime),
          birth_place_id: createPlace.id,
          timezone_id: createPlace.timezone_id || null,
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
    var isRename = launchContext.mode === "rename";
    var isAdd = launchContext.mode === "add";
    var isEdit = launchContext.mode === "edit";
    var showNames = isAdd || isRename || isEdit;

    var nameField = showNames
      ? '  <div class="field name-row">'
        + '<div class="name-col"><label for="rm-intake-first">First name</label>'
        + '<input type="text" id="rm-intake-first" placeholder="First name" autocomplete="given-name" /></div>'
        + '<div class="name-col"><label for="rm-intake-last">Last name</label>'
        + '<input type="text" id="rm-intake-last" placeholder="Last name" autocomplete="family-name" /></div>'
        + '</div>'
      : '  <input type="hidden" id="rm-intake-first" value="" /><input type="hidden" id="rm-intake-last" value="" />';

    var title = isRename ? "Rename profile" : (isEdit ? "Edit profile" : "Birth information");
    var subtitle = isRename
      ? "Update the first and last name shown for this profile."
      : (isEdit
        ? "Update birth date, time, and place for this profile."
        : "Exact birth time is required for relocation overlays.");

    var birthBlock = isRename ? "" : [
      '    <div class="field">',
      '      <label for="rm-intake-date">Birth date</label>',
      '      <input type="date" id="rm-intake-date" />',
      '    </div>',
      '    <div class="field">',
      '      <label for="rm-intake-time">Birth time</label>',
      '      <input type="time" id="rm-intake-time" />',
      '      <p class="hint">Local time at birth place.</p>',
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
    ].join("\n");

    overlay.innerHTML = [
      '<div class="rm-intake-journey">',
      '  <p class="rm-intake-wordmark">Relocation</p>',
      '  <div class="card">',
      (showNames ? '    <button type="button" class="rm-intake-close" id="rm-intake-close" aria-label="Close">&times;</button>' : ''),
      '    <h2>' + title + '</h2>',
      '    <p class="subtitle">' + subtitle + '</p>',
      nameField,
      birthBlock,
      (launchContext.mode === "add"
        ? '    <label class="field" style="display:flex;align-items:center;gap:8px;font-size:13px;cursor:pointer;">'
          + '<input type="checkbox" id="rm-intake-switch" checked style="width:auto;margin:0;" />'
          + 'Switch to new profile</label>'
        : ''),
      (showNames
        ? '    <div class="rm-intake-actions">'
          + '<button type="button" class="cancel-btn" id="rm-intake-cancel">Cancel</button>'
          + '<button type="button" class="submit-btn" id="rm-intake-submit">' + (isRename ? 'Save' : (isEdit ? 'Save' : 'Continue')) + '</button>'
          + '</div>'
        : '    <button type="button" class="submit-btn" id="rm-intake-submit">Continue</button>'),
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

    var cancelBtn = document.getElementById("rm-intake-cancel");
    if (cancelBtn) cancelBtn.addEventListener("click", removeOverlay);

    var closeBtn = document.getElementById("rm-intake-close");
    if (closeBtn) closeBtn.addEventListener("click", removeOverlay);

    if (launchContext.mode === "rename") {
      var split = splitDisplayName(launchContext.displayName || "");
      applyNameFields(split.first, split.last);
      var firstInput = document.getElementById("rm-intake-first");
      if (firstInput) firstInput.focus();
    }
  }

  function removeOverlay() {
    var existing = document.getElementById(INTAKE_OVERLAY_ID);
    if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
    overlayShown = false;
    launchContext = DEFAULT_LAUNCH_CONTEXT;
  }


  function parseTimeForInput(timeVal) {
    if (!timeVal) return "";
    var s = String(timeVal).trim();
    var m24 = s.match(/^(\d{1,2}):(\d{2})(?::\d{2})?$/);
    if (m24) {
      var hh = m24[1];
      var mm = m24[2];
      return (hh.length < 2 ? "0" : "") + hh + ":" + mm;
    }
    var m12 = s.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i);
    if (m12) {
      var h = parseInt(m12[1], 10);
      var min = m12[2];
      var ap = m12[3].toUpperCase();
      if (ap === "PM" && h < 12) h += 12;
      if (ap === "AM" && h === 12) h = 0;
      return (h < 10 ? "0" : "") + h + ":" + min;
    }
    var loose = s.match(/(\d{1,2}):(\d{2})/);
    if (loose) {
      var h2 = loose[1];
      var m2 = loose[2];
      return (h2.length < 2 ? "0" : "") + h2 + ":" + m2;
    }
    return "";
  }

  function lookupIntakePlace(placeId, vm, raw) {
    if (!placeId) return null;
    if (vm && vm.placesById && vm.placesById[placeId]) return vm.placesById[placeId];
    var list = (raw && raw.places) || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === placeId) return list[i];
    }
    return null;
  }

  function prefillEditProfile(profileId) {
    if (!profileId || !window.__rmAppShell) return;
    var vm = window.__rmAppShell.viewModel && window.__rmAppShell.viewModel();
    var raw = window.__rmAppShell.storeRaw && window.__rmAppShell.storeRaw();
    if (!vm || !raw) return;
    var rec = (vm.chartRecords || []).find(function (r) { return r.chartRecordId === profileId; });
    var client = (raw.clients || []).find(function (c) { return c.id === profileId; });
    var bp = client && client.birth_profile_id
      ? (raw.birth_profiles || []).find(function (b) { return b.id === client.birth_profile_id; })
      : null;
    if (!rec && !client) return;

    var displayName = (rec && rec.displayName) || (client && client.display_name) || "";
    var split = splitDisplayName(displayName);
    applyNameFields(split.first, split.last);

    var birthDate = (bp && bp.birth_date) || (rec && rec.birthDate) || "";
    if (birthDate) {
      var dateEl = document.getElementById("rm-intake-date");
      if (dateEl) dateEl.value = String(birthDate).slice(0, 10);
    }

    var timeSource = (bp && bp.birth_time) || (rec && rec.birthTime) || (rec && rec.birthTimeDisplay) || "";
    var timeInput = parseTimeForInput(timeSource);
    if (timeInput) {
      var timeEl = document.getElementById("rm-intake-time");
      if (timeEl) timeEl.value = timeInput;
    }

    var placeId = (bp && bp.birth_place_id) || null;
    var place = lookupIntakePlace(placeId, vm, raw);
    var label = (place && (place.display_name || place.name || place.label))
      || (rec && rec.birthCity)
      || "";
    if (placeId && label) {
      var stub = place || {
        id: placeId,
        display_name: label,
        timezone_id: (bp && bp.timezone_id) || null,
      };
      selectPlace(stub, label);
    }
  }

  function showOverlay(options) {
    if (overlayShown) return;
    launchContext = normalizeLaunchOptions(options);
    resetIntakeFormState();
    overlayShown = true;

    injectStyles();
    var overlay = buildOverlay();
    overlay.classList.add("rm-instrument-surface");
    document.body.appendChild(overlay);
    attachListeners(overlay);
    prefillNameFromGoogleMetadata();
    if (launchContext.mode === "edit" && launchContext.profileId) {
      prefillEditProfile(launchContext.profileId);
    }

    setTimeout(function () {
      if (launchContext.mode === "rename") return;
      if (launchContext.mode === "edit") {
        var firstInput = document.getElementById("rm-intake-first");
        if (firstInput) { firstInput.focus(); return; }
      }
      if (launchContext.mode === "add") {
        var firstInput = document.getElementById("rm-intake-first");
        if (firstInput) { firstInput.focus(); return; }
      }
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
