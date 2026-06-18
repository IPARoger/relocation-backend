/**
 * place_search_client.js — shared backend place search for birth/current location UIs.
 * Routes city search through GET /places/search (alias-aware ranked search).
 */
(function () {
  "use strict";

  function apiBase() {
    if (typeof window !== "undefined" && window.API_BASE) return window.API_BASE;
    return "";
  }

  async function searchPlaces(query, limit) {
    var q = String(query || "").trim();
    if (q.length < 2) return [];
    var lim = limit || 10;
    var url =
      apiBase() +
      "/places/search?q=" +
      encodeURIComponent(q) +
      "&limit=" +
      encodeURIComponent(String(lim));
    var resp = await fetch(url);
    if (!resp.ok) {
      throw new Error("place search failed: HTTP " + resp.status);
    }
    var rows = await resp.json();
    return Array.isArray(rows) ? rows : [];
  }

  window.RMPlaceSearch = {
    searchPlaces: searchPlaces,
  };
})();
