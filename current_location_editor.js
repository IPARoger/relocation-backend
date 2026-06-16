/**
 * current_location_editor.js — lightweight "Set Current Location" overlay.
 *
 * Exposes:  window.__showCurrentLocationEditor(profileId)
 *
 * Requires: window.SupabaseReady, window.CurrentUser
 *
 * Write sequence (RLS-compliant, no service role):
 *   A. UPDATE current_location_history SET is_current=false
 *          WHERE profile_id=? AND account_id=? AND is_current=true
 *   B. INSERT current_location_history
 *          { profile_id, account_id, place_id, is_current:true, source:'manual' }
 *
 * After save: notify the shell (optional onSaved callback or the
 * window.__rmAppShell.applyCurrentLocationUpdate hook) for an in-place refresh.
 * Falls back to location.reload() only when no shell hook handles the update.
 */
(function () {
  "use strict";

  var EDITOR_OVERLAY_ID = "rm-current-location-editor";

  function injectStyles() {
    if (document.getElementById(EDITOR_OVERLAY_ID + "-styles")) return;
    var style = document.createElement("style");
    style.id = EDITOR_OVERLAY_ID + "-styles";
    style.textContent = [
      "#" + EDITOR_OVERLAY_ID + " {",
      "  position:fixed;inset:0;background:rgba(10,10,26,0.88);",
      "  display:flex;align-items:center;justify-content:center;",
      "  z-index:10000;font-family:inherit;",
      "}",
      "#" + EDITOR_OVERLAY_ID + " .card {",
      "  background:#13132a;border:1px solid #2e2e5e;border-radius:12px;",
      "  padding:32px 28px;max-width:420px;width:90%;color:#e0e0f0;position:relative;",
      "}",
      "#" + EDITOR_OVERLAY_ID + " h2 { margin:0 0 6px;font-size:1.2rem;color:#c8b8ff; }",
      "#" + EDITOR_OVERLAY_ID + " .subtitle { margin:0 0 24px;font-size:0.85rem;color:#8888aa; }",
      "#" + EDITOR_OVERLAY_ID + " .field { margin-bottom:16px; }",
      "#" + EDITOR_OVERLAY_ID + " label { display:block;font-size:0.78rem;color:#9090b0;margin-bottom:4px; }",
      "#" + EDITOR_OVERLAY_ID + " input[type=text] {",
      "  width:100%;box-sizing:border-box;background:#0c0c20;border:1px solid #3a3a6a;",
      "  color:#e0e0f0;padding:8px 10px;border-radius:6px;font-size:0.95rem;",
      "}",
      "#" + EDITOR_OVERLAY_ID + " input:focus { border-color:#7b61ff;outline:none; }",
      "#" + EDITOR_OVERLAY_ID + " .place-results {",
      "  background:#0c0c20;border:1px solid #3a3a6a;border-top:none;",
      "  border-radius:0 0 6px 6px;max-height:180px;overflow-y:auto;",
      "}",
      "#" + EDITOR_OVERLAY_ID + " .place-result {",
      "  padding:8px 10px;cursor:pointer;font-size:0.88rem;border-bottom:1px solid #1e1e3e;",
      "}",
      "#" + EDITOR_OVERLAY_ID + " .place-result:hover { background:#252550; }",
      "#" + EDITOR_OVERLAY_ID + " .place-result.selected { background:#1f1f48;color:#c8b8ff; }",
      "#" + EDITOR_OVERLAY_ID + " .place-wrap { position:relative; }",
      "#" + EDITOR_OVERLAY_ID + " .searching { font-size:0.78rem;color:#8080a0;margin-top:4px; }",
      "#" + EDITOR_OVERLAY_ID + " .btn-row { display:flex;gap:10px;margin-top:20px; }",
      "#" + EDITOR_OVERLAY_ID + " .submit-btn {",
      "  flex:1;background:#7b61ff;color:#fff;border:none;border-radius:6px;",
      "  padding:10px 0;font-size:0.95rem;cursor:pointer;",
      "}",
      "#" + EDITOR_OVERLAY_ID + " .submit-btn:disabled { opacity:0.4;cursor:default; }",
      "#" + EDITOR_OVERLAY_ID + " .cancel-btn {",
      "  background:#1e1e3e;color:#9090b0;border:1px solid #3a3a6a;border-radius:6px;",
      "  padding:10px 16px;font-size:0.95rem;cursor:pointer;",
      "}",
      "#" + EDITOR_OVERLAY_ID + " .err-msg { display:none;color:#ff6b6b;font-size:0.82rem;margin-top:10px; }",
      "#" + EDITOR_OVERLAY_ID + " .err-msg.visible { display:block; }",
    ].join("\n");
    document.head.appendChild(style);
  }

  var state = {
    profileId:    null,
    placeResults: [],
    selectedPlace: null,
    placeQuery:   "",
    searching:    false,
    submitting:   false,
    onSaved:      null,
  };

  var searchTimer = null;

  async function searchPlaces(query) {
    if (!query || query.length < 2) {
      state.placeResults = [];
      renderResults();
      return;
    }
    state.searching = true;
    renderSearching(true);
    try {
      var client = await window.SupabaseReady;
      var result = await client
        .from("places")
        .select("id, display_name, timezone_id, admin1, country_code")
        .ilike("display_name", query + "%")
        .order("display_name", { ascending: true })
        .limit(10);
      if (result.error) throw result.error;
      state.placeResults = result.data || [];
    } catch (err) {
      state.placeResults = [];
      console.warn("[cl-editor] place search error:", err.message);
    } finally {
      state.searching = false;
      renderSearching(false);
      renderResults();
    }
  }

  function renderSearching(active) {
    var el = document.getElementById("rm-cl-searching");
    if (el) el.style.display = active ? "block" : "none";
  }

  function renderResults() {
    var container = document.getElementById("rm-cl-place-results");
    if (!container) return;
    container.innerHTML = "";
    if (!state.placeResults.length) { container.style.display = "none"; return; }
    container.style.display = "block";
    state.placeResults.forEach(function (place) {
      var item = document.createElement("div");
      item.className = "place-result" +
        (state.selectedPlace && state.selectedPlace.id === place.id ? " selected" : "");
      // display_name already includes region + country (post ADMIN1-FIX-3),
      // so we do not re-append admin1/country_code (avoids duplicate labels).
      var label = place.display_name;
      item.textContent = label;
      item.addEventListener("click", function () { selectPlace(place, label); });
      container.appendChild(item);
    });
  }

  function selectPlace(place, label) {
    state.selectedPlace = place;
    var input = document.getElementById("rm-cl-place-input");
    if (input) input.value = label || place.display_name;
    var clearBtn = document.getElementById("rm-cl-place-clear");
    if (clearBtn) clearBtn.style.display = "inline";
    var container = document.getElementById("rm-cl-place-results");
    if (container) container.style.display = "none";
  }

  function clearPlace() {
    state.selectedPlace = null;
    state.placeResults  = [];
    var input = document.getElementById("rm-cl-place-input");
    if (input) { input.value = ""; input.focus(); }
    var clearBtn = document.getElementById("rm-cl-place-clear");
    if (clearBtn) clearBtn.style.display = "none";
    var container = document.getElementById("rm-cl-place-results");
    if (container) container.style.display = "none";
  }

  async function saveLocation() {
    var errEl     = document.getElementById("rm-cl-err");
    var submitBtn = document.getElementById("rm-cl-submit");

    function showError(msg) {
      if (errEl)     { errEl.textContent = msg; errEl.className = "err-msg visible"; }
      if (submitBtn) submitBtn.disabled = false;
      state.submitting = false;
    }

    if (!state.selectedPlace) return showError("Please search and select a city first.");

    state.submitting = true;
    if (submitBtn) submitBtn.disabled = true;
    if (errEl) errEl.className = "err-msg";

    var currentUser = window.CurrentUser;
    if (!currentUser || !currentUser.accountId) {
      return showError("Session error. Please reload and try again.");
    }

    var profileId = state.profileId;
    var accountId = currentUser.accountId;
    var placeId   = state.selectedPlace.id;

    try {
      var client = await window.SupabaseReady;

      // A. Retire existing is_current rows for this profile (non-fatal if none exist)
      var retireResult = await client
        .from("current_location_history")
        .update({ is_current: false })
        .eq("profile_id", profileId)
        .eq("account_id", accountId)
        .eq("is_current", true);

      if (retireResult.error) {
        console.warn("[cl-editor] retire rows warning (non-fatal):", retireResult.error.message);
      }

      // B. Insert new current row
      var insertResult = await client
        .from("current_location_history")
        .insert({
          profile_id:  profileId,
          account_id:  accountId,
          place_id:    placeId,
          is_current:  true,
          source:      "manual",
          selected_at: new Date().toISOString(),
        });

      if (insertResult.error) {
        return showError("Could not save location: " + insertResult.error.message);
      }

      // Close the overlay, then ask the shell to update in place. The DB write
      // above is the source of truth; the shell hook only refreshes UI state.
      removeOverlay();
      var savedPlace = {
        id:           placeId,
        display_name: state.selectedPlace.display_name,
        timezone_id:  state.selectedPlace.timezone_id || null,
        admin1:       state.selectedPlace.admin1 || null,
        country_code: state.selectedPlace.country_code || null,
      };
      var handled = false;
      if (typeof state.onSaved === "function") {
        try {
          handled = state.onSaved(profileId, savedPlace) === true;
        } catch (cbErr) {
          console.warn("[cl-editor] onSaved callback failed (non-fatal):", cbErr && cbErr.message);
        }
      }
      if (!handled && window.__rmAppShell &&
          typeof window.__rmAppShell.applyCurrentLocationUpdate === "function") {
        try {
          handled = window.__rmAppShell.applyCurrentLocationUpdate(profileId, savedPlace) === true;
        } catch (hookErr) {
          console.warn("[cl-editor] shell update hook failed (non-fatal):", hookErr && hookErr.message);
        }
      }
      if (!handled) {
        console.log("[cl-editor] Location saved. No shell hook; reloading...");
        window.location.reload();
      } else {
        console.log("[cl-editor] Location saved. Shell updated in place.");
      }

    } catch (err) {
      showError("Unexpected error: " + (err.message || String(err)));
    }
  }

  function buildOverlay() {
    var overlay = document.createElement("div");
    overlay.id = EDITOR_OVERLAY_ID;
    overlay.innerHTML = [
      '<div class="card">',
      '  <h2>Set Current Location</h2>',
      '  <p class="subtitle">Search for your current city. Used as the reference point for relocation comparisons.</p>',
      '  <div class="field">',
      '    <label for="rm-cl-place-input">City</label>',
      '    <div class="place-wrap">',
      '      <input type="text" id="rm-cl-place-input"',
      '             placeholder="Start typing a city name\u2026" autocomplete="off" />',
      '      <button type="button" id="rm-cl-place-clear"',
      '              style="display:none;position:absolute;right:8px;top:8px;',
      '                     background:none;border:none;color:#8888aa;cursor:pointer;font-size:0.8rem;"',
      '              >\u2715 clear</button>',
      '      <div class="place-results" id="rm-cl-place-results" style="display:none;"></div>',
      '    </div>',
      '    <div class="searching" id="rm-cl-searching" style="display:none;">Searching\u2026</div>',
      '  </div>',
      '  <div class="btn-row">',
      '    <button type="button" class="cancel-btn" id="rm-cl-cancel">Cancel</button>',
      '    <button type="button" class="submit-btn" id="rm-cl-submit">Save Location</button>',
      '  </div>',
      '  <div class="err-msg" id="rm-cl-err"></div>',
      '</div>',
    ].join("\n");
    return overlay;
  }

  function removeOverlay() {
    var el = document.getElementById(EDITOR_OVERLAY_ID);
    if (el) el.remove();
  }

  function attachListeners(overlay) {
    var placeInput = document.getElementById("rm-cl-place-input");
    if (placeInput) {
      placeInput.addEventListener("input", function (e) {
        state.placeQuery    = e.target.value;
        state.selectedPlace = null;
        clearTimeout(searchTimer);
        searchTimer = setTimeout(function () { searchPlaces(state.placeQuery); }, 300);
      });
    }

    var clearBtn = document.getElementById("rm-cl-place-clear");
    if (clearBtn) clearBtn.addEventListener("click", clearPlace);

    var submitBtn = document.getElementById("rm-cl-submit");
    if (submitBtn) submitBtn.addEventListener("click", saveLocation);

    var cancelBtn = document.getElementById("rm-cl-cancel");
    if (cancelBtn) cancelBtn.addEventListener("click", removeOverlay);

    // Dismiss on backdrop click
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) removeOverlay();
    });
  }

  window.__showCurrentLocationEditor = function (profileId, options) {
    if (!profileId) { console.warn("[cl-editor] No profileId provided."); return; }

    state.profileId     = profileId;
    state.placeResults  = [];
    state.selectedPlace = null;
    state.placeQuery    = "";
    state.searching     = false;
    state.submitting    = false;
    state.onSaved       = (options && typeof options.onSaved === "function") ? options.onSaved : null;

    removeOverlay();
    injectStyles();
    var overlay = buildOverlay();
    document.body.appendChild(overlay);
    attachListeners(overlay);

    setTimeout(function () {
      var input = document.getElementById("rm-cl-place-input");
      if (input) input.focus();
    }, 80);
  };

})();
