/**
 * human_place_label.js — shared user-visible place labels (W2-LABEL-1).
 * Known cities: City, Admin, Country (or City, Country).
 * Custom map points: user label, else coordinates.
 */
(function () {
  "use strict";

  var GENERIC_PLACE_NAMES = {
    "custom location": true,
    "saved place": true,
    "location": true,
    "unnamed location": true,
  };

  var COUNTRY_CODE_NAMES = {
    US: "United States",
    GB: "United Kingdom",
    UK: "United Kingdom",
    FR: "France",
    DE: "Germany",
    IT: "Italy",
    ES: "Spain",
    CA: "Canada",
    AU: "Australia",
    IN: "India",
    PK: "Pakistan",
    RU: "Russia",
    CN: "China",
    JP: "Japan",
    BR: "Brazil",
    MX: "Mexico",
  };

  function norm(s) {
    return String(s || "").trim().toLowerCase();
  }

  function isUuid(s) {
    return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(String(s || "").trim());
  }

  function isGenericLabel(s) {
    return GENERIC_PLACE_NAMES[norm(s)] === true;
  }

  function coordLabel(lat, lon) {
    var la = Number(lat);
    var lo = Number(lon);
    if (!Number.isFinite(la) || !Number.isFinite(lo)) return "Saved location";
    return "Saved location near " + la.toFixed(2) + ", " + lo.toFixed(2);
  }

  function isCustomPlace(place) {
    var provider = place.provider || place.origin || "";
    if (provider === "map_custom") return true;
    if (place.source === "custom") return true;
    return false;
  }

  function resolveCountryName(place) {
    if (place.country_name) return String(place.country_name).trim();
    if (place.country) return String(place.country).trim();
    var code = place.country_code ? String(place.country_code).trim().toUpperCase() : "";
    if (code && COUNTRY_CODE_NAMES[code]) return COUNTRY_CODE_NAMES[code];
    return code || "";
  }

  function resolveAdminName(place) {
    var a = place.admin1 || place.admin_name || place.admin || place.state;
    return a ? String(a).trim() : "";
  }

  function extractCityName(place) {
    if (place.canonical_name) return String(place.canonical_name).trim();
    if (place.name && !isUuid(place.name)) return String(place.name).trim();
    var dn = String(place.display_name || "").trim();
    if (!dn || isUuid(dn)) return "";
    return dn.split(",")[0].trim() || dn;
  }

  function labelAlreadyContains(label, token) {
    if (!label || !token) return false;
    var tok = norm(token);
    return label.split(",").some(function (part) {
      return norm(part) === tok;
    });
  }

  function displayNameIsDisambiguated(displayName, country, admin) {
    var parts = displayName.split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    if (parts.length < 2) return false;
    if (parts.length >= 3) return true;
    if (country && labelAlreadyContains(displayName, country)) return true;
    if (admin && labelAlreadyContains(displayName, admin)) return true;
    return parts.length >= 2;
  }

  /**
   * @param {object|string|null} placeOrFavorite place row, favorite row, search item, or legacy id string
   * @returns {string}
   */
  function humanPlaceLabel(placeOrFavorite) {
    if (placeOrFavorite == null) return "Saved place";

    if (typeof placeOrFavorite === "string") {
      var s = String(placeOrFavorite).trim();
      if (!s || isUuid(s)) return "Saved place";
      return s;
    }

    var place = placeOrFavorite;
    var lat = place.latitude != null ? place.latitude : place.lat;
    var lon = place.longitude != null ? place.longitude : place.lon;
    var userLabel = String(place.label || place.notes || place.placeName || "").trim();

    if (isCustomPlace(place)) {
      if (userLabel && !isGenericLabel(userLabel)) return userLabel;
      return coordLabel(lat, lon);
    }

    var displayName = String(place.display_name || "").trim();
    if (displayName && isUuid(displayName)) displayName = "";

    var city = extractCityName(place);
    var admin = resolveAdminName(place);
    var country = resolveCountryName(place);

    if (admin && norm(admin) === norm(city)) admin = "";

    if (displayName && displayNameIsDisambiguated(displayName, country, admin)) {
      return displayName;
    }

    var parts = [];
    if (city) parts.push(city);
    if (admin && !labelAlreadyContains(parts.join(", "), admin)) parts.push(admin);
    if (country && !labelAlreadyContains(parts.join(", "), country)) parts.push(country);

    if (parts.length) return parts.join(", ");

    if (displayName) return displayName;
    if (userLabel && !isGenericLabel(userLabel)) return userLabel;
    return "Saved place";
  }

  window.RMHumanPlaceLabel = { humanPlaceLabel: humanPlaceLabel };
})();
