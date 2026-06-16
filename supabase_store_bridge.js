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
      .select("id, profile_id")
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
        notes:                     "",
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
        place_ids:             cspBySetId[cs.id] || [],
        saved_investigation_id: null,
        notes:                 "",
        schema_version:        1,
        updated_at:            null,
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
