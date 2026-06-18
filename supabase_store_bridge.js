/**
 * supabase_store_bridge.js — Supabase-backed product store assembler.
 *
 * Queries the authenticated user's Supabase data and assembles a conforming
 * store object that can be passed directly into adaptStoreToView() in
 * app_shell.html without any modification to that function.
 *
 * Exposes:
 *   window.SupabaseStore        — assembled store object (once ready)
 *   window.SupabaseStoreReady   — Promise<store> resolving when assembled;
 *                                 rejects if no profiles/birth records exist
 *                                 (intake overlay required)
 *
 * Requirements (must load before this script):
 *   supabase_client.js   → window.SupabaseReady
 *   auth_guard.js        → session confirmed
 *   user_profile.js      → window.CurrentUserReady
 *
 * This script is READ-ONLY. Zero database writes.
 * Does not modify adaptStoreToView(), render(), or any app_shell logic.
 * Does not replace /local-product-store.json — it is an alternative input.
 */
(function () {
  "use strict";

  // ── Helpers ───────────────────────────────────────────────────────────────

  /** exact→T0, approximate→T2, unknown/other→T3 */
  function toConfidenceTier(mode) {
    if (mode === "exact")       return "T0";
    if (mode === "approximate") return "T2";
    return "T3";
  }

  /** human→self (v1 single-user), research→research, else→client */
  function toRecordType(profile_type) {
    if (profile_type === "research") return "research";
    if (profile_type === "human")    return "self";
    return "client";
  }

  /** Postgres TIME arrives as "HH:MM:SS"; store expects "HH:MM" */
  function trimTime(pgTime) {
    if (!pgTime) return null;
    return pgTime.slice(0, 5);
  }

  // ── Effective settings + snapshot infrastructure (Settings Phase 1) ─────
  //
  // Single canonical resolver for Layer 2 settings and the canonical snapshot
  // shape used by saved investigations / comparisons. This is settings LOADING
  // infrastructure only: it does not switch house systems, zodiac modes, or
  // ontology packs, and it does not touch calculations. It only resolves and
  // shapes values that already exist.

  // Hardcoded Layer 2 defaults. The seam for future ontology-pack defaults sits
  // BETWEEN these hardcoded defaults and stored user settings (see precedence in
  // getEffectiveSettings). Do not add renderer/debug/UI/cache keys here.
  var RM_SETTINGS_DEFAULTS = {
    settings_version:      1,
    house_system:          "placidus",
    zodiac_mode:           "tropical",
    orb_defaults:          { conjunction: 8, square: 8, opposition: 8, trine: 8, sextile: 6 },
    visible_minor_aspects: false,
    out_of_sign_aspects:   false,
    visible_planets:       ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"],
    visible_bodies:        ["chiron"],
    visible_major_aspects: ["conjunction", "opposition", "square", "trine", "sextile"],
    visible_minor_aspects_list: [],
    major_aspect_orbs:     { conjunction: 8, opposition: 8, square: 8, trine: 8, sextile: 6 },
    minor_aspect_orbs:     { quincunx: 3, semisextile: 2, semisquare: 2, sesquiquadrate: 2, quintile: 2, biquintile: 2 },
    house_proximity_orb_degrees: 2,
    subsequent_house_policy:     "display_only",
    aspect_to_angle_orbs:  { conjunction: 8, opposition: 8, square: 8, trine: 8, sextile: 6 },
    helper_layers:         {},
    ontology_pack_id:      null,
  };

  var RM_SETTINGS_SNAPSHOT_VERSION = 1;

  // Resolve effective Layer 2 settings.
  // Precedence: stored user settings → ontology-pack defaults → hardcoded defaults.
  // `ontologyDefaults` is accepted now to reserve the future layering seam;
  // callers may pass null until ontology packs exist.
  function getEffectiveSettings(storedUserSettings, ontologyDefaults) {
    var stored = (storedUserSettings && typeof storedUserSettings === "object") ? storedUserSettings : {};
    var onto   = (ontologyDefaults && typeof ontologyDefaults === "object") ? ontologyDefaults : {};
    function pick(key) {
      return stored[key] || onto[key] || RM_SETTINGS_DEFAULTS[key];
    }
    // Major aspect orbs: major_aspect_orbs is canonical; orb_defaults is the
    // legacy key. Prefer stored major_aspect_orbs, fall back to stored
    // orb_defaults, then ontology, then hardcoded defaults. orb_defaults is
    // returned as a mirror of the resolved canonical value (never diverges).
    var effectiveMajorOrbs =
      stored.major_aspect_orbs || stored.orb_defaults ||
      onto.major_aspect_orbs   || onto.orb_defaults   ||
      RM_SETTINGS_DEFAULTS.major_aspect_orbs;
    return {
      settings_version:      pick("settings_version"),
      house_system:          pick("house_system"),
      zodiac_mode:           pick("zodiac_mode"),
      orb_defaults:          effectiveMajorOrbs,
      visible_minor_aspects: pick("visible_minor_aspects"),
      out_of_sign_aspects:   pick("out_of_sign_aspects"),
      visible_planets:       pick("visible_planets"),
      visible_bodies:        pick("visible_bodies"),
      visible_major_aspects: pick("visible_major_aspects"),
      visible_minor_aspects_list: pick("visible_minor_aspects_list"),
      major_aspect_orbs:     effectiveMajorOrbs,
      minor_aspect_orbs:     pick("minor_aspect_orbs"),
      house_proximity_orb_degrees:
        (stored.house_proximity_orb_degrees != null) ? stored.house_proximity_orb_degrees
        : (onto.house_proximity_orb_degrees != null) ? onto.house_proximity_orb_degrees
        : RM_SETTINGS_DEFAULTS.house_proximity_orb_degrees,
      subsequent_house_policy: pick("subsequent_house_policy"),
      aspect_to_angle_orbs:  pick("aspect_to_angle_orbs"),
      helper_layers:         pick("helper_layers"),
      ontology_pack_id:      pick("ontology_pack_id"),
    };
  }

  // Canonical Layer 2 settings snapshot for saved investigations / comparisons.
  // Truth- and interpretation-relevant settings only. Renderer, debug, UI, and
  // cache state are excluded by construction (they are simply never copied in).
  function buildSettingsSnapshot(effective) {
    var eff = (effective && typeof effective === "object")
      ? effective
      : getEffectiveSettings(null, null);
    return {
      snapshot_version:      RM_SETTINGS_SNAPSHOT_VERSION,
      settings_version:      eff.settings_version      || RM_SETTINGS_DEFAULTS.settings_version,
      house_system:          eff.house_system          || RM_SETTINGS_DEFAULTS.house_system,
      zodiac_mode:           eff.zodiac_mode           || RM_SETTINGS_DEFAULTS.zodiac_mode,
      orb_defaults:          eff.major_aspect_orbs     || eff.orb_defaults || RM_SETTINGS_DEFAULTS.major_aspect_orbs,  // legacy mirror of major_aspect_orbs
      visible_minor_aspects: eff.visible_minor_aspects || RM_SETTINGS_DEFAULTS.visible_minor_aspects,
      out_of_sign_aspects:   eff.out_of_sign_aspects   || RM_SETTINGS_DEFAULTS.out_of_sign_aspects,
      visible_planets:       eff.visible_planets       || RM_SETTINGS_DEFAULTS.visible_planets,
      visible_bodies:        eff.visible_bodies        || RM_SETTINGS_DEFAULTS.visible_bodies,
      visible_major_aspects: eff.visible_major_aspects || RM_SETTINGS_DEFAULTS.visible_major_aspects,
      visible_minor_aspects_list: eff.visible_minor_aspects_list || RM_SETTINGS_DEFAULTS.visible_minor_aspects_list,
      major_aspect_orbs:     eff.major_aspect_orbs     || RM_SETTINGS_DEFAULTS.major_aspect_orbs,
      minor_aspect_orbs:     eff.minor_aspect_orbs     || RM_SETTINGS_DEFAULTS.minor_aspect_orbs,
      house_proximity_orb_degrees: (eff.house_proximity_orb_degrees != null) ? eff.house_proximity_orb_degrees : RM_SETTINGS_DEFAULTS.house_proximity_orb_degrees,
      subsequent_house_policy: eff.subsequent_house_policy || RM_SETTINGS_DEFAULTS.subsequent_house_policy,
      aspect_to_angle_orbs:  eff.aspect_to_angle_orbs  || RM_SETTINGS_DEFAULTS.aspect_to_angle_orbs,
      ontology_pack_id:      eff.ontology_pack_id != null ? eff.ontology_pack_id : RM_SETTINGS_DEFAULTS.ontology_pack_id,
    };
  }

  // Synchronous export — available as soon as this script loads, independent of
  // the async store build below.
  window.RMSettings = {
    DEFAULTS:             RM_SETTINGS_DEFAULTS,
    SNAPSHOT_VERSION:     RM_SETTINGS_SNAPSHOT_VERSION,
    getEffectiveSettings: getEffectiveSettings,
    buildSettingsSnapshot: buildSettingsSnapshot,
  };

  // ── Main builder ──────────────────────────────────────────────────────────

  async function buildSupabaseStore() {

    // 1. Resolve identity
    var currentUser = await window.CurrentUserReady;
    if (!currentUser || !currentUser.accountId) {
      throw new Error(
        "[supabase_store_bridge] CurrentUser missing. " +
        "Ensure user_profile.js resolved before this script."
      );
    }
    var accountId = currentUser.accountId;
    var client    = await window.SupabaseReady;

    // 2. profiles
    var profilesResult = await client
      .from("profiles")
      .select("id, display_name, profile_type")
      .eq("account_id", accountId)
      .is("archived_at", null)
      .order("created_at", { ascending: true });

    if (profilesResult.error) {
      throw new Error("[supabase_store_bridge] profiles: " + profilesResult.error.message);
    }
    var profiles = profilesResult.data || [];

    if (profiles.length === 0) {
      throw new Error(
        "[supabase_store_bridge] No profiles found. Intake overlay required."
      );
    }

    // 3. birth_records — newest first; keep one per profile_id
    var birthResult = await client
      .from("birth_records")
      .select("id, profile_id, birth_date, birth_time_mode, birth_time_start, birth_place_id, timezone_id")
      .eq("account_id", accountId)
      .order("created_at", { ascending: false });

    if (birthResult.error) {
      throw new Error("[supabase_store_bridge] birth_records: " + birthResult.error.message);
    }

    var birthByProfileId = {};
    (birthResult.data || []).forEach(function (br) {
      if (!birthByProfileId[br.profile_id]) birthByProfileId[br.profile_id] = br;
    });

    // 4. favorite_places
    var favsResult = await client
      .from("favorite_places")
      .select("id, profile_id, place_id, rank, label")
      .eq("account_id", accountId)
      .is("archived_at", null)
      .order("rank", { ascending: true });

    if (favsResult.error) {
      throw new Error("[supabase_store_bridge] favorite_places: " + favsResult.error.message);
    }
    var favs = favsResult.data || [];

    // 5. comparison_sets
    var csResult = await client
      .from("comparison_sets")
      .select("id, profile_id, title, settings_snapshot_json, created_at, updated_at")
      .eq("account_id", accountId)
      .is("archived_at", null);

    if (csResult.error) {
      throw new Error("[supabase_store_bridge] comparison_sets: " + csResult.error.message);
    }
    var compSets = csResult.data || [];

    // 6. comparison_set_places
    var cspData = [];
    if (compSets.length > 0) {
      var csIds = compSets.map(function (cs) { return cs.id; });
      var cspResult = await client
        .from("comparison_set_places")
        .select("comparison_set_id, place_id, sort_order")
        .in("comparison_set_id", csIds)
        .order("sort_order", { ascending: true });

      if (cspResult.error) {
        throw new Error("[supabase_store_bridge] comparison_set_places: " + cspResult.error.message);
      }
      cspData = cspResult.data || [];
    }

    // 5b. saved_searches → store.saved_investigations (read-only list, non-fatal)
    var savedSearches = [];
    try {
      var ssResult = await client
        .from("saved_searches")
        .select("id, profile_id, title, conditions_json, viewport_json, settings_snapshot_json, created_at, updated_at")
        .eq("account_id", accountId)
        .is("archived_at", null)
        .order("updated_at", { ascending: false });
      if (!ssResult.error) {
        savedSearches = ssResult.data || [];
      } else {
        console.warn("[supabase_store_bridge] saved_searches query non-fatal:", ssResult.error.message);
      }
    } catch (e) {
      console.warn("[supabase_store_bridge] saved_searches query non-fatal:", e);
    }

    // 7. current_location_history — most recent is_current=true row per profile
    var currentLocationByProfileId = {};
    try {
      var clResult = await client
        .from("current_location_history")
        .select("profile_id, place_id")
        .eq("account_id", accountId)
        .eq("is_current", true);
      if (!clResult.error) {
        (clResult.data || []).forEach(function (row) {
          if (row.place_id && !currentLocationByProfileId[row.profile_id]) {
            currentLocationByProfileId[row.profile_id] = row.place_id;
          }
        });
      }
    } catch (e) {
      console.warn("[supabase_store_bridge] current_location_history query failed (non-fatal):", e);
    }

    // 8. Collect all unique place IDs
    var placeIdSet = {};
    Object.values(birthByProfileId).forEach(function (br) {
      if (br.birth_place_id) placeIdSet[br.birth_place_id] = true;
    });
    favs.forEach(function (f)    { if (f.place_id)  placeIdSet[f.place_id]  = true; });
    cspData.forEach(function (r) { if (r.place_id)  placeIdSet[r.place_id]  = true; });
    Object.values(currentLocationByProfileId).forEach(function (pid) {
      if (pid) placeIdSet[pid] = true;
    });
    var placeIds = Object.keys(placeIdSet);

    // 9. places (no account filter — authenticated read, places are shared)
    var placesById = {};
    if (placeIds.length > 0) {
      var placesResult = await client
        .from("places")
        .select("id, display_name, latitude, longitude")
        .in("id", placeIds);

      if (placesResult.error) {
        throw new Error("[supabase_store_bridge] places: " + placesResult.error.message);
      }
      (placesResult.data || []).forEach(function (p) { placesById[p.id] = p; });
    }

    // 10. user_settings — prefer account-level row (profile_id IS NULL)
    var rawSettings = null;
    var settingsResult = await client
      .from("user_settings")
      .select("settings_json, profile_id")
      .eq("account_id", accountId)
      .order("created_at", { ascending: true });

    if (!settingsResult.error && settingsResult.data && settingsResult.data.length > 0) {
      var acctRow = settingsResult.data.find(function (r) { return r.profile_id === null; });
      rawSettings = ((acctRow || settingsResult.data[0]).settings_json) || {};
    }

    // 11. notes — chart-record-level notes (target_type='chart_record'); newest
    // non-archived row per profile. Non-fatal: notes are convenience data and
    // must never block store assembly. localStorage remains the device fallback.
    var chartRecordNoteByProfileId = {};
    try {
      var notesResult = await client
        .from("notes")
        .select("profile_id, body, updated_at, target_type, archived_at")
        .eq("account_id", accountId)
        .eq("target_type", "chart_record")
        .is("archived_at", null)
        .order("updated_at", { ascending: false });
      if (!notesResult.error) {
        (notesResult.data || []).forEach(function (row) {
          if (row.profile_id && !(row.profile_id in chartRecordNoteByProfileId)) {
            chartRecordNoteByProfileId[row.profile_id] = row.body || "";
          }
        });
      } else {
        console.warn("[supabase_store_bridge] notes query non-fatal:", notesResult.error.message);
      }
    } catch (e) {
      console.warn("[supabase_store_bridge] notes query non-fatal:", e);
    }

    // 11b. notes — comparison-set notes (target_type='comparison_set'); newest
    // non-archived row per comparison set (keyed by target_id). Non-fatal.
    var comparisonSetNoteByTargetId = {};
    try {
      var cmpNotesResult = await client
        .from("notes")
        .select("target_id, body, updated_at, target_type, archived_at")
        .eq("account_id", accountId)
        .eq("target_type", "comparison_set")
        .is("archived_at", null)
        .order("updated_at", { ascending: false });
      if (!cmpNotesResult.error) {
        (cmpNotesResult.data || []).forEach(function (row) {
          if (row.target_id && !(row.target_id in comparisonSetNoteByTargetId)) {
            comparisonSetNoteByTargetId[row.target_id] = row.body || "";
          }
        });
      } else {
        console.warn("[supabase_store_bridge] comparison_set notes query non-fatal:", cmpNotesResult.error.message);
      }
    } catch (e) {
      console.warn("[supabase_store_bridge] comparison_set notes query non-fatal:", e);
    }

    // ── Assemble conforming store shape ───────────────────────────────────

    var storePlaces = Object.values(placesById).map(function (p) {
      return {
        id:             p.id,
        display_name:   p.display_name,
        lat:            parseFloat(p.latitude),
        lon:            parseFloat(p.longitude),
        schema_version: 1,
      };
    });

    var storeBirthProfiles = [];
    profiles.forEach(function (profile) {
      var br = birthByProfileId[profile.id];
      if (!br) return;
      storeBirthProfiles.push({
        id:                  br.id,
        birth_date:          br.birth_date,
        birth_time:          br.birth_time_mode === "exact" ? trimTime(br.birth_time_start) : null,
        birth_place_id:      br.birth_place_id || null,
        timezone_id:         br.timezone_id    || null,
        confidence_tier:     toConfidenceTier(br.birth_time_mode),
        confidence_metadata: {},
        representative_time: null,
        schema_version:      1,
        updated_at:          null,
      });
    });

    var storeClients = [];
    profiles.forEach(function (profile) {
      if (!birthByProfileId[profile.id]) return;
      storeClients.push({
        id:                        profile.id,
        display_name:              profile.display_name,
        birth_profile_id:          birthByProfileId[profile.id].id,
        record_type:               toRecordType(profile.profile_type),
        current_location_place_id: currentLocationByProfileId[profile.id] || null,
        notes:                     chartRecordNoteByProfileId[profile.id] || "",
        tags:                      [],
        schema_version:            1,
        updated_at:                null,
      });
    });

    if (storeClients.length === 0) {
      throw new Error(
        "[supabase_store_bridge] Profiles exist but no birth records found. " +
        "Intake overlay must complete birth record entry."
      );
    }

    var savedDefault   = rawSettings && rawSettings.default_chart_record_id;
    var defaultIsValid = savedDefault &&
      storeClients.some(function (c) { return c.id === savedDefault; });
    var defaultChartRecordId = defaultIsValid ? savedDefault : storeClients[0].id;

    // Resolve Layer 2 settings through the canonical helper (ontology seam = null
    // for now). default_chart_record_id is resolved/validated separately above.
    var effectiveSettings = getEffectiveSettings(rawSettings, null);
    var storeUserSettings = {
      settings_version:        effectiveSettings.settings_version,
      house_system:            effectiveSettings.house_system,
      zodiac_mode:             effectiveSettings.zodiac_mode,
      orb_defaults:            effectiveSettings.major_aspect_orbs,  // legacy mirror of major_aspect_orbs
      visible_minor_aspects:   effectiveSettings.visible_minor_aspects,
      out_of_sign_aspects:     effectiveSettings.out_of_sign_aspects,
      visible_planets:         effectiveSettings.visible_planets,
      visible_bodies:          effectiveSettings.visible_bodies,
      visible_major_aspects:   effectiveSettings.visible_major_aspects,
      visible_minor_aspects_list: effectiveSettings.visible_minor_aspects_list,
      major_aspect_orbs:       effectiveSettings.major_aspect_orbs,
      minor_aspect_orbs:       effectiveSettings.minor_aspect_orbs,
      house_proximity_orb_degrees: effectiveSettings.house_proximity_orb_degrees,
      subsequent_house_policy: effectiveSettings.subsequent_house_policy,
      aspect_to_angle_orbs:    effectiveSettings.aspect_to_angle_orbs,
      helper_layers:           effectiveSettings.helper_layers,
      ontology_pack_id:        effectiveSettings.ontology_pack_id,
      default_chart_record_id: defaultChartRecordId,
      updated_at:              null,
    };

    var storeFavs = favs.map(function (f) {
      return {
        id:                    f.id,
        client_id:             f.profile_id,
        place_id:              f.place_id,
        saved_investigation_id: null,
        notes:                 f.label || "",
        sort_order:            f.rank != null ? f.rank : 0,
        schema_version:        1,
      };
    });

    var cspBySetId = {};
    cspData.forEach(function (r) {
      if (!cspBySetId[r.comparison_set_id]) cspBySetId[r.comparison_set_id] = [];
      cspBySetId[r.comparison_set_id].push(r.place_id);
    });

    var storeCompSets = compSets.map(function (cs) {
      return {
        id:                    cs.id,
        client_id:             cs.profile_id,
        profile_id:            cs.profile_id,
        title:                 cs.title || "",
        place_ids:             cspBySetId[cs.id] || [],
        settings_snapshot_json: cs.settings_snapshot_json || {},
        saved_investigation_id: null,
        notes:                 comparisonSetNoteByTargetId[cs.id] || "",
        schema_version:        1,
        created_at:            cs.created_at || null,
        updated_at:            cs.updated_at  || null,
      };
    });

    var storeSavedInvestigations = savedSearches.map(function (ss) {
      return {
        id:                ss.id,
        client_id:         ss.profile_id,
        name:              ss.title || "Untitled",
        title:             ss.title || "Untitled",
        conditions:        ss.conditions_json        || {},
        viewport:          ss.viewport_json          || {},
        settings_snapshot: ss.settings_snapshot_json || {},
        updated_at:        ss.updated_at             || ss.created_at || null,
        schema_version:    1,
      };
    });

    var store = {
      _storage:               "SUPABASE_LIVE",
      _warning:               "Live Supabase data. account_id=" + accountId,
      storage_schema_version: 3,
      supabase_mirror_version: 1,
      professional_account: {
        id:             accountId,
        display_name:   currentUser.accountName || "Personal",
        schema_version: 1,
        created_at:     null,
        updated_at:     null,
      },
      user_settings:        storeUserSettings,
      places:               storePlaces,
      birth_profiles:       storeBirthProfiles,
      clients:              storeClients,
      saved_investigations: storeSavedInvestigations,
      favorite_cities:      storeFavs,
      comparison_sets:      storeCompSets,
      chart_record_history: [],
      tags:                 [],
      notes:                [],
    };

    console.log("[supabase_store_bridge] Store assembled:", {
      profiles:            storeClients.length,
      birthProfiles:       storeBirthProfiles.length,
      places:              storePlaces.length,
      favs:                storeFavs.length,
      comparisonSets:      storeCompSets.length,
      savedInvestigations: storeSavedInvestigations.length,
      default:             defaultChartRecordId,
    });

    return store;
  }

  // ── Single-profile re-fetch ────────────────────────────────────────────────
  //
  // Re-fetches one profile + its newest birth_record + the associated birth
  // place (if not already present) and merges them into window.SupabaseStore
  // in place. Exposed as window.refreshProfile for use by app_shell.html after
  // profile creation, avoiding a full page reload.
  //
  // Invariants preserved:
  //   - Only adds; never removes or reorders existing entries.
  //   - No-ops on duplicate ids (idempotent on repeated calls).
  //   - Does not touch any other SupabaseStore key.
  //   - Does not alter the init flow or SupabaseStore shape.

  async function refreshProfile(profileId) {
    if (!profileId) throw new Error("[refreshProfile] profileId is required.");
    var store = window.SupabaseStore;
    if (!store) throw new Error("[refreshProfile] SupabaseStore not loaded.");

    var currentUser = await window.CurrentUserReady;
    if (!currentUser || !currentUser.accountId) {
      throw new Error("[refreshProfile] CurrentUser missing.");
    }
    var accountId = currentUser.accountId;
    var client    = await window.SupabaseReady;

    // Fetch profile row
    var profResult = await client
      .from("profiles")
      .select("id, display_name, profile_type")
      .eq("id", profileId)
      .eq("account_id", accountId)
      .single();
    if (profResult.error) throw profResult.error;
    var profile = profResult.data;

    // Fetch newest birth_record for this profile
    var brResult = await client
      .from("birth_records")
      .select("id, profile_id, birth_date, birth_time_mode, birth_time_start, birth_place_id, timezone_id")
      .eq("profile_id", profileId)
      .eq("account_id", accountId)
      .order("created_at", { ascending: false })
      .limit(1);
    if (brResult.error) throw brResult.error;
    var br = brResult.data && brResult.data[0];
    if (!br) throw new Error("[refreshProfile] No birth record found for profile " + profileId + ".");

    // Fetch birth place if not already in store
    store.places = store.places || [];
    if (br.birth_place_id && !store.places.some(function (p) { return p.id === br.birth_place_id; })) {
      var plResult = await client
        .from("places")
        .select("id, display_name, latitude, longitude")
        .eq("id", br.birth_place_id)
        .single();
      if (!plResult.error && plResult.data) {
        store.places.push({
          id:             plResult.data.id,
          display_name:   plResult.data.display_name,
          lat:            parseFloat(plResult.data.latitude),
          lon:            parseFloat(plResult.data.longitude),
          schema_version: 1,
        });
      }
    }

    // Merge birth_profile (idempotent)
    store.birth_profiles = store.birth_profiles || [];
    if (!store.birth_profiles.some(function (b) { return b.id === br.id; })) {
      store.birth_profiles.push({
        id:                  br.id,
        birth_date:          br.birth_date,
        birth_time:          br.birth_time_mode === "exact" ? trimTime(br.birth_time_start) : null,
        birth_place_id:      br.birth_place_id || null,
        timezone_id:         br.timezone_id    || null,
        confidence_tier:     toConfidenceTier(br.birth_time_mode),
        confidence_metadata: {},
        representative_time: null,
        schema_version:      1,
        updated_at:          null,
      });
    }

    // Merge client (idempotent)
    store.clients = store.clients || [];
    if (!store.clients.some(function (c) { return c.id === profileId; })) {
      store.clients.push({
        id:                        profile.id,
        display_name:              profile.display_name,
        birth_profile_id:          br.id,
        record_type:               toRecordType(profile.profile_type),
        current_location_place_id: null,
        notes:                     "",
        tags:                      [],
        schema_version:            1,
        updated_at:                null,
      });
    }
  }

  window.refreshProfile = refreshProfile;

  // ── Initialize ────────────────────────────────────────────────────────────

  var storeReady = buildSupabaseStore()
    .then(function (store) {
      window.SupabaseStore = store;
      return store;
    })
    .catch(function (err) {
      console.warn(
        "[supabase_store_bridge] Build failed " +
        "(app_shell will fall back to local store):", err.message
      );
      window.SupabaseStore = null;
      throw err;
    });

  window.SupabaseStoreReady = storeReady;

})();
