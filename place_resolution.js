/**
 * RMPlaceResolution — shared city/place -> place_id resolution utility.
 *
 * Single seam reused by Map (and, later, Profile Add City / Comparison) so we
 * do not maintain separate resolvers. Uses existing endpoints only:
 *   GET  /places/search?q=<displayName>
 *   POST /places
 *
 * No schema/repository/API changes. Browser global, classic script.
 */
(function () {
  "use strict";

  function resolveApiBase(options) {
    if (options && options.apiBase) return options.apiBase;
    try {
      if (typeof LIBRARY_API_BASE !== "undefined" && LIBRARY_API_BASE) {
        return LIBRARY_API_BASE;
      }
    } catch (e) { /* not defined in this scope */ }
    if (typeof window !== "undefined" && window.LIBRARY_API_BASE) {
      return window.LIBRARY_API_BASE;
    }
    return "http://127.0.0.1:8000";
  }

  function norm(value) {
    return String(value == null ? "" : value).trim().toLowerCase();
  }

  function hasCoordinates(selection) {
    return Number.isFinite(Number(selection.latitude)) &&
      Number.isFinite(Number(selection.longitude));
  }

  /**
   * Resolve an existing place (by name, plus coordinate proximity when
   * coordinates are present) or create one when coordinates exist.
   *
   * @param {{displayName:string, latitude?:number, longitude?:number,
   *          country?:string, admin?:string, origin?:string}} selection
   * @param {{apiBase?:string, coordTolerance?:number}} [options]
   * @returns {Promise<object>} place row (has .id)
   */
  async function resolvePlaceFromCitySelection(selection, options) {
    selection = selection || {};
    options = options || {};
    var base = resolveApiBase(options);
    var tolerance = (typeof options.coordTolerance === "number")
      ? options.coordTolerance
      : 0.02;

    var displayName = selection.displayName;
    if (!displayName || !String(displayName).trim()) {
      throw new Error("place_resolution: displayName required");
    }

    var coords = hasCoordinates(selection);
    var lat = Number(selection.latitude);
    var lon = Number(selection.longitude);

    // Prefer deterministic identity via GeoNames id when present. This avoids
    // creating duplicate places when display_name formats differ (e.g. map
    // passes the short city name while the canonical row is
    // "City, Region, Country"). Reads the shared places table directly
    // (RLS: authenticated select). Falls back to name + coordinate matching,
    // then to create — existing behavior is preserved when no id/client.
    var geonamesId = selection.geonamesId != null
      ? String(selection.geonamesId).trim()
      : "";
    var sbClient = (options && options.supabaseClient)
      || (typeof window !== "undefined" && (window.SupabaseClient || window._supabaseClient))
      || null;
    if (geonamesId && sbClient && typeof sbClient.from === "function") {
      try {
        var gidResult = await sbClient
          .from("places")
          .select("*")
          .eq("geonames_id", geonamesId)
          .limit(1);
        if (!gidResult.error &&
            Array.isArray(gidResult.data) &&
            gidResult.data.length &&
            gidResult.data[0].id) {
          return gidResult.data[0];
        }
      } catch (e) { /* non-fatal — fall through to name/coordinate matching */ }
    }

    var matches = [];
    try {
      var resp = await fetch(base + "/places/search?q=" + encodeURIComponent(displayName));
      if (resp.ok) matches = await resp.json();
    } catch (e) {
      matches = [];
    }
    if (!Array.isArray(matches)) matches = [];

    var existing;
    if (coords) {
      existing = matches.find(function (p) {
        return norm(p.display_name) === norm(displayName) &&
          Math.abs(Number(p.latitude) - lat) <= tolerance &&
          Math.abs(Number(p.longitude) - lon) <= tolerance;
      });
    } else {
      existing = matches.find(function (p) {
        return norm(p.display_name) === norm(displayName);
      });
    }
    if (existing) return existing;

    if (!coords) {
      throw new Error(
        "place_resolution: no coordinates and no exact match for \"" + displayName + "\""
      );
    }

    var body = {
      display_name: displayName,
      latitude: lat,
      longitude: lon,
      provider: selection.origin || "manual"
    };
    if (selection.country) body.country_name = selection.country;
    if (selection.admin) body.admin1 = selection.admin;

    var createResp = await fetch(base + "/places", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!createResp.ok) {
      throw new Error("place_resolution: place_create_failed_" + createResp.status);
    }
    return createResp.json();
  }

  window.RMPlaceResolution = {
    resolvePlaceFromCitySelection: resolvePlaceFromCitySelection
  };
})();
