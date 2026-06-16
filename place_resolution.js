/**
 * RMPlaceResolution — shared city/place -> place_id resolution utility.
 *
 * Single seam reused by Map (and, later, Profile Add City / Comparison) so we
 * do not maintain separate resolvers. Writes are backend-owned:
 *   POST /places/resolve-or-create  (JWT required)
 *
 * Browser global, classic script.
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
    return "";
  }

  function hasCoordinates(selection) {
    return Number.isFinite(Number(selection.latitude)) &&
      Number.isFinite(Number(selection.longitude));
  }

  async function resolveAccessToken(options) {
    var sbClient = (options && options.supabaseClient)
      || (typeof window !== "undefined" && (window.SupabaseClient || window._supabaseClient))
      || null;
    if (!sbClient || typeof sbClient.auth !== "object") {
      throw new Error("place_resolution: session unavailable");
    }
    var sessionResult = await sbClient.auth.getSession();
    var session = sessionResult && sessionResult.data ? sessionResult.data.session : null;
    var token = session && session.access_token;
    if (!token) {
      throw new Error("place_resolution: session unavailable");
    }
    return token;
  }

  /**
   * Resolve an existing place (by GeoNames id, name, and coordinate proximity)
   * or create one when coordinates exist. Backend owns the write path.
   *
   * @param {{displayName:string, latitude?:number, longitude?:number,
   *          country?:string, admin?:string, origin?:string,
   *          geonamesId?:string|null}} selection
   * @param {{apiBase?:string, coordTolerance?:number, supabaseClient?:object,
   *          accessToken?:string}} [options]
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

    var token = options.accessToken;
    if (!token) {
      token = await resolveAccessToken(options);
    }

    var body = {
      display_name: String(displayName).trim(),
      origin: selection.origin || "manual",
      coord_tolerance: tolerance,
    };
    if (hasCoordinates(selection)) {
      body.latitude = Number(selection.latitude);
      body.longitude = Number(selection.longitude);
    }
    if (selection.country) body.country = selection.country;
    if (selection.admin) body.admin = selection.admin;
    if (selection.geonamesId != null && String(selection.geonamesId).trim()) {
      body.geonames_id = String(selection.geonamesId).trim();
    }

    var path = "/places/resolve-or-create";
    var url = base ? (base.replace(/\/$/, "") + path) : path;
    var resp = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
      },
      body: JSON.stringify(body),
    });
    if (!resp.ok) {
      throw new Error("place_resolution: place_resolve_failed_" + resp.status);
    }
    return resp.json();
  }

  window.RMPlaceResolution = {
    resolvePlaceFromCitySelection: resolvePlaceFromCitySelection
  };
})();
