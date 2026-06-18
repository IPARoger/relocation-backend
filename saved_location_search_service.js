/**
 * saved_location_search_service.js — Family B Saved Location Search.
 * Merges profile favorites, custom saved places (map_custom), and GET /places/search.
 */
(function () {
  "use strict";

  var SOURCE_FAVORITE = "favorite";
  var SOURCE_CUSTOM = "custom";
  var SOURCE_GEONAMES = "geonames";
  var SOURCE_TEACHING = "teaching";

  var TEACHING_LOCATIONS = [
    { display_name: "Rome, Italy", teaching_query: "Rome, Italy" },
    { display_name: "Bali, Indonesia", teaching_query: "Bali, Indonesia" },
  ];

  var RANK = {
    exact_favorite: 10,
    exact_custom: 20,
    exact_geonames: 30,
    prefix_favorite: 40,
    prefix_custom: 50,
    prefix_geonames: 60,
    contains_favorite: 70,
    contains_custom: 80,
    contains_geonames: 90,
  };

  function apiBase() {
    if (typeof window !== "undefined" && window.API_BASE) return window.API_BASE;
    return "";
  }

  function norm(s) {
    return String(s || "").trim().toLowerCase();
  }

  function displayLabel(row) {
    return String(row.label || row.display_name || row.name || "").trim();
  }

  function sourceFromProvider(provider) {
    return provider === "map_custom" ? SOURCE_CUSTOM : SOURCE_FAVORITE;
  }

  function rankTier(query, label, source) {
    var q = norm(query);
    var l = norm(label);
    if (!q || !l) return null;
    if (l === q) {
      if (source === SOURCE_FAVORITE) return RANK.exact_favorite;
      if (source === SOURCE_CUSTOM) return RANK.exact_custom;
      return RANK.exact_geonames;
    }
    if (l.indexOf(q) === 0) {
      if (source === SOURCE_FAVORITE) return RANK.prefix_favorite;
      if (source === SOURCE_CUSTOM) return RANK.prefix_custom;
      return RANK.prefix_geonames;
    }
    if (l.indexOf(q) !== -1) {
      if (source === SOURCE_FAVORITE) return RANK.contains_favorite;
      if (source === SOURCE_CUSTOM) return RANK.contains_custom;
      return RANK.contains_geonames;
    }
    return null;
  }

  function toResult(row, source) {
    var label = displayLabel(row);
    return {
      place_id: row.place_id || row.id,
      display_name: row.display_name || label,
      label: label,
      latitude: row.latitude != null ? row.latitude : row.lat,
      longitude: row.longitude != null ? row.longitude : row.lon,
      source: source,
      favorite_id: row.favorite_id || null,
      provider: row.provider || null,
      geonames_id: row.geonames_id || null,
      country_code: row.country_code || null,
      admin1: row.admin1 || null,
    };
  }

  function dedupeResults(items) {
    var seen = {};
    var out = [];
    items.forEach(function (item) {
      var key = item.place_id;
      if (!key || seen[key]) return;
      seen[key] = true;
      out.push(item);
    });
    return out;
  }

  async function authToken() {
    try {
      var client = window.SupabaseReady ? await window.SupabaseReady : null;
      if (!client) return null;
      var sessionResult = await client.auth.getSession();
      var session = sessionResult && sessionResult.data ? sessionResult.data.session : null;
      return session && session.access_token ? session.access_token : null;
    } catch (e) {
      return null;
    }
  }

  async function fetchFavorites(profileId) {
    var token = await authToken();
    if (!token || !profileId) return [];
    var resp = await fetch(
      apiBase() + "/favorites?profile_id=" + encodeURIComponent(profileId),
      { headers: { Authorization: "Bearer " + token } }
    );
    if (!resp.ok) return [];
    var data = await resp.json();
    return Array.isArray(data.favorites) ? data.favorites : [];
  }

  async function fetchPlaceMeta(placeId) {
    if (!placeId) return null;
    try {
      var resp = await fetch(apiBase() + "/place/" + encodeURIComponent(placeId));
      if (!resp.ok) return null;
      return await resp.json();
    } catch (e) {
      return null;
    }
  }

  async function enrichFavorites(favorites) {
    var out = [];
    var needsMeta = [];
    favorites.forEach(function (fav, idx) {
      if (fav.provider) return;
      needsMeta.push({ fav: fav, idx: idx });
    });
    var metas = {};
    if (needsMeta.length) {
      var fetched = await Promise.all(
        needsMeta.map(function (entry) {
          return fetchPlaceMeta(entry.fav.place_id);
        })
      );
      needsMeta.forEach(function (entry, i) {
        metas[entry.idx] = fetched[i] || {};
      });
    }
    favorites.forEach(function (fav, idx) {
      var meta = fav.provider ? fav : (metas[idx] || {});
      var source = sourceFromProvider(meta.provider);
      out.push(toResult({
        favorite_id: fav.id,
        place_id: fav.place_id,
        label: fav.label,
        display_name: fav.display_name || meta.display_name,
        latitude: fav.latitude != null ? fav.latitude : meta.latitude,
        longitude: fav.longitude != null ? fav.longitude : meta.longitude,
        provider: meta.provider || null,
        geonames_id: meta.geonames_id || null,
        country_code: meta.country_code || null,
        admin1: meta.admin1 || null,
      }, source));
    });
    return out;
  }

  function splitStarter(savedRows) {
    var favorites = [];
    var customs = [];
    savedRows.forEach(function (row) {
      if (row.source === SOURCE_CUSTOM) customs.push(row);
      else favorites.push(row);
    });
    return { favorites: favorites, customs: customs };
  }

  function rankResults(query, localRows, geonamesRows) {
    var ranked = [];
    localRows.forEach(function (row) {
      var tier = rankTier(query, row.label || row.display_name, row.source);
      if (tier != null) ranked.push({ tier: tier, item: row });
    });
    geonamesRows.forEach(function (row) {
      var item = toResult(row, SOURCE_GEONAMES);
      var tier = rankTier(query, item.display_name, SOURCE_GEONAMES);
      if (tier != null) ranked.push({ tier: tier, item: item });
    });
    ranked.sort(function (a, b) {
      if (a.tier !== b.tier) return a.tier - b.tier;
      return norm(a.item.display_name).localeCompare(norm(b.item.display_name));
    });
    return dedupeResults(ranked.map(function (r) { return r.item; }));
  }

  var profileCache = {};

  async function loadProfileSaved(profileId, options) {
    options = options || {};
    var force = !!options.forceRefresh;
    if (!force && profileCache[profileId]) {
      return profileCache[profileId];
    }
    var favorites = await fetchFavorites(profileId);
    var savedRows = await enrichFavorites(favorites);
    var starter = splitStarter(savedRows);
    var payload = {
      profileId: profileId,
      savedRows: savedRows,
      starter: starter,
      loadedAt: Date.now(),
    };
    profileCache[profileId] = payload;
    return payload;
  }

  function invalidateProfile(profileId) {
    if (profileId) delete profileCache[profileId];
    else profileCache = {};
  }

  async function searchPlaces(query, limit) {
    var searchApi = window.RMPlaceSearch;
    if (!searchApi || typeof searchApi.searchPlaces !== "function") {
      throw new Error("RMPlaceSearch unavailable");
    }
    return searchApi.searchPlaces(query, limit || 10);
  }

  async function search(profileId, query, options) {
    options = options || {};
    var q = String(query || "").trim();
    var payload = await loadProfileSaved(profileId, options);

    if (!q) {
      var locationItems = payload.starter.customs.slice();
      if (options.includeTeaching) {
        TEACHING_LOCATIONS.forEach(function (t) {
          locationItems.push({
            display_name: t.display_name,
            label: t.display_name,
            teaching_query: t.teaching_query,
            source: SOURCE_TEACHING,
          });
        });
      }
      return {
        mode: "starter",
        query: "",
        sections: [
          { id: "favorites", title: "Favorites", items: payload.starter.favorites.slice() },
          { id: "locations", title: "Locations", items: locationItems },
        ],
        items: payload.savedRows.slice(),
      };
    }

    if (q.length < 2) {
      return { mode: "typing", query: q, sections: [], items: [] };
    }

    var geonamesRows = [];
    try {
      geonamesRows = await searchPlaces(q, options.limit || 10);
    } catch (e) {
      geonamesRows = [];
    }

    var items = rankResults(q, payload.savedRows, geonamesRows);
    return {
      mode: "results",
      query: q,
      sections: [{ id: "results", title: "Results", items: items }],
      items: items,
    };
  }

  window.RMSavedLocationSearch = {
    SOURCE_FAVORITE: SOURCE_FAVORITE,
    SOURCE_CUSTOM: SOURCE_CUSTOM,
    SOURCE_GEONAMES: SOURCE_GEONAMES,
    SOURCE_TEACHING: SOURCE_TEACHING,
    TEACHING_LOCATIONS: TEACHING_LOCATIONS,
    PLACEHOLDER: "Search locations or favorites",
    loadProfileSaved: loadProfileSaved,
    invalidateProfile: invalidateProfile,
    search: search,
    rankResults: rankResults,
    dedupeResults: dedupeResults,
  };
})();
