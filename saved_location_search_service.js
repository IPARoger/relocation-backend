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

  var GENERIC_PLACE_NAMES = {
    "custom location": true,
    "saved place": true,
    "location": true,
    "unnamed location": true,
  };

  var US_STATE_BY_NAME = {};
  var US_STATE_NAMES = {};
  (function initUsStates() {
    var pairs = [
      ["AL", "Alabama"], ["AK", "Alaska"], ["AZ", "Arizona"], ["AR", "Arkansas"],
      ["CA", "California"], ["CO", "Colorado"], ["CT", "Connecticut"], ["DE", "Delaware"],
      ["FL", "Florida"], ["GA", "Georgia"], ["HI", "Hawaii"], ["ID", "Idaho"],
      ["IL", "Illinois"], ["IN", "Indiana"], ["IA", "Iowa"], ["KS", "Kansas"],
      ["KY", "Kentucky"], ["LA", "Louisiana"], ["ME", "Maine"], ["MD", "Maryland"],
      ["MA", "Massachusetts"], ["MI", "Michigan"], ["MN", "Minnesota"], ["MS", "Mississippi"],
      ["MO", "Missouri"], ["MT", "Montana"], ["NE", "Nebraska"], ["NV", "Nevada"],
      ["NH", "New Hampshire"], ["NJ", "New Jersey"], ["NM", "New Mexico"], ["NY", "New York"],
      ["NC", "North Carolina"], ["ND", "North Dakota"], ["OH", "Ohio"], ["OK", "Oklahoma"],
      ["OR", "Oregon"], ["PA", "Pennsylvania"], ["RI", "Rhode Island"], ["SC", "South Carolina"],
      ["SD", "South Dakota"], ["TN", "Tennessee"], ["TX", "Texas"], ["UT", "Utah"],
      ["VT", "Vermont"], ["VA", "Virginia"], ["WA", "Washington"], ["WV", "West Virginia"],
      ["WI", "Wisconsin"], ["WY", "Wyoming"], ["DC", "District of Columbia"],
    ];
    pairs.forEach(function (p) {
      US_STATE_BY_NAME[norm(p[1])] = p[0];
      US_STATE_NAMES[p[0]] = p[1];
    });
  })();

  var QUERY_CACHE_TTL_MS = 45000;
  var QUERY_CACHE_MAX = 48;
  var queryCache = {};

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

  function isGenericPlaceName(name) {
    return GENERIC_PLACE_NAMES[norm(name)] === true;
  }

  function coordLabel(lat, lon) {
    var la = Number(lat);
    var lo = Number(lon);
    if (!Number.isFinite(la) || !Number.isFinite(lo)) return "Saved location";
    return "Saved location near " + la.toFixed(2) + ", " + lo.toFixed(2);
  }

  function formatPlaceDisplayName(row, source) {
    if (window.RMHumanPlaceLabel && window.RMHumanPlaceLabel.humanPlaceLabel) {
      var payload = Object.assign({}, row, { source: source });
      if (source === SOURCE_CUSTOM) payload.provider = payload.provider || "map_custom";
      return window.RMHumanPlaceLabel.humanPlaceLabel(payload);
    }
    var label = displayLabel(row);
    var dn = String(row.display_name || label || "").trim();
    if (source !== SOURCE_CUSTOM && source !== SOURCE_FAVORITE) return dn || label;
    if (label && !isGenericPlaceName(label)) return label;
    if (dn && !isGenericPlaceName(dn)) return dn;
    return coordLabel(
      row.latitude != null ? row.latitude : row.lat,
      row.longitude != null ? row.longitude : row.lon
    );
  }

  function resolveStateToken(token) {
    var t = String(token || "").trim();
    if (!t) return null;
    var upper = t.toUpperCase();
    if (upper.length === 2 && US_STATE_NAMES[upper]) return upper;
    return US_STATE_BY_NAME[norm(t)] || null;
  }

  function parseCityStateQuery(query) {
    var raw = String(query || "").trim();
    if (!raw) return { city: "", state: null };
    var commaParts = raw.split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    if (commaParts.length >= 2) {
      var state = resolveStateToken(commaParts[commaParts.length - 1]);
      if (state) {
        return { city: commaParts.slice(0, -1).join(", "), state: state };
      }
    }
    var words = raw.split(/\s+/).filter(Boolean);
    if (words.length >= 2) {
      var last = words[words.length - 1];
      var abbr = resolveStateToken(last);
      if (abbr) {
        return { city: words.slice(0, -1).join(" "), state: abbr };
      }
    }
    return { city: raw, state: null };
  }

  function admin1Matches(item, stateAbbr) {
    if (!stateAbbr || !item) return false;
    var a1 = String(item.admin1 || "").trim();
    if (!a1) return false;
    var upper = a1.toUpperCase();
    if (upper === stateAbbr) return true;
    return norm(a1) === norm(US_STATE_NAMES[stateAbbr] || "");
  }

  function itemCityName(item) {
    return norm(String(item.display_name || item.label || "").split(",")[0] || "");
  }

  function rankTier(query, item, source) {
    var parsed = parseCityStateQuery(query);
    var q = norm(query);
    var label = norm(item.display_name || item.label || "");
    if (!q || !label) return null;

    if (parsed.state && parsed.city) {
      var qCity = norm(parsed.city);
      var iCity = itemCityName(item);
      if (iCity !== qCity && iCity.indexOf(qCity) !== 0) return null;
      if (!admin1Matches(item, parsed.state)) return null;
      if (iCity === qCity) {
        if (source === SOURCE_FAVORITE) return RANK.exact_favorite;
        if (source === SOURCE_CUSTOM) return RANK.exact_custom;
        return RANK.exact_geonames;
      }
      if (source === SOURCE_FAVORITE) return RANK.prefix_favorite;
      if (source === SOURCE_CUSTOM) return RANK.prefix_custom;
      return RANK.prefix_geonames;
    }

    if (label === q) {
      if (source === SOURCE_FAVORITE) return RANK.exact_favorite;
      if (source === SOURCE_CUSTOM) return RANK.exact_custom;
      return RANK.exact_geonames;
    }
    if (label.indexOf(q) === 0) {
      if (source === SOURCE_FAVORITE) return RANK.prefix_favorite;
      if (source === SOURCE_CUSTOM) return RANK.prefix_custom;
      return RANK.prefix_geonames;
    }
    if (label.indexOf(q) !== -1) {
      if (source === SOURCE_FAVORITE) return RANK.contains_favorite;
      if (source === SOURCE_CUSTOM) return RANK.contains_custom;
      return RANK.contains_geonames;
    }
    return null;
  }

  function toResult(row, source) {
    var display = formatPlaceDisplayName(row, source);
    return {
      place_id: row.place_id || row.id,
      display_name: display,
      label: displayLabel(row) || display,
      latitude: row.latitude != null ? row.latitude : row.lat,
      longitude: row.longitude != null ? row.longitude : row.lon,
      source: source,
      favorite_id: row.favorite_id || null,
      provider: row.provider || null,
      geonames_id: row.geonames_id || null,
      country_code: row.country_code || null,
      admin1: row.admin1 || null,
      population: row.population != null ? row.population : null,
      importance_rank: row.importance_rank != null ? row.importance_rank : null,
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
        population: meta.population,
        importance_rank: meta.importance_rank,
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

  function importanceScore(item) {
    var pop = item.population != null ? Number(item.population) : NaN;
    if (Number.isFinite(pop) && pop > 0) return pop;
    var rank = item.importance_rank != null ? Number(item.importance_rank) : NaN;
    if (Number.isFinite(rank) && rank > 0) return rank;
    return 0;
  }

  function localityBoost(query, item) {
    var parsed = parseCityStateQuery(query);
    var label = norm(item.display_name || item.label || "");
    if (!label) return 0;
    var city = label.split(",")[0].trim();
    var boost = 0;

    if (parsed.state && parsed.city) {
      if (itemCityName(item) === norm(parsed.city) && admin1Matches(item, parsed.state)) {
        boost += 50000000;
      }
      return boost;
    }

    var q = norm(query);
    if (city === q) boost += 10000000;
    else if (city.indexOf(q) === 0) boost += 1000000;

    if (item.country_code === "FR" && (city === "paris" || q === "paris")) boost += 500000;
    if (item.country_code === "GB" && (city === "london" || q === "london")) boost += 500000;
    return boost;
  }

  function rankResults(query, localRows, geonamesRows) {
    var ranked = [];
    localRows.forEach(function (row) {
      var tier = rankTier(query, row, row.source);
      if (tier != null) ranked.push({ tier: tier, item: row });
    });
    geonamesRows.forEach(function (row) {
      var item = toResult(row, SOURCE_GEONAMES);
      var tier = rankTier(query, item, SOURCE_GEONAMES);
      if (tier != null) ranked.push({ tier: tier, item: item });
    });
    ranked.sort(function (a, b) {
      if (a.tier !== b.tier) return a.tier - b.tier;
      var boostA = localityBoost(query, a.item) + importanceScore(a.item);
      var boostB = localityBoost(query, b.item) + importanceScore(b.item);
      if (boostB !== boostA) return boostB - boostA;
      return norm(a.item.display_name).localeCompare(norm(b.item.display_name));
    });
    return dedupeResults(ranked.map(function (r) { return r.item; }));
  }

  var profileCache = {};

  function queryCacheKey(profileId, q) {
    return String(profileId || "") + "\0" + norm(q);
  }

  function getCachedQuery(profileId, q) {
    var key = queryCacheKey(profileId, q);
    var entry = queryCache[key];
    if (!entry) return null;
    if (Date.now() - entry.at > QUERY_CACHE_TTL_MS) {
      delete queryCache[key];
      return null;
    }
    return entry.payload;
  }

  function setCachedQuery(profileId, q, payload) {
    var key = queryCacheKey(profileId, q);
    queryCache[key] = { at: Date.now(), payload: payload };
    var keys = Object.keys(queryCache);
    if (keys.length > QUERY_CACHE_MAX) {
      keys.sort(function (a, b) { return queryCache[a].at - queryCache[b].at; });
      var drop = keys.length - QUERY_CACHE_MAX;
      for (var i = 0; i < drop; i++) delete queryCache[keys[i]];
    }
  }

  function clearQueryCache(profileId) {
    if (!profileId) {
      queryCache = {};
      return;
    }
    var prefix = String(profileId) + "\0";
    Object.keys(queryCache).forEach(function (key) {
      if (key.indexOf(prefix) === 0) delete queryCache[key];
    });
  }

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
    if (profileId) {
      delete profileCache[profileId];
      clearQueryCache(profileId);
    } else {
      profileCache = {};
      queryCache = {};
    }
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

    var cached = options.skipCache ? null : getCachedQuery(profileId, q);
    if (cached) return cached;

    var geonamesRows = [];
    try {
      geonamesRows = await searchPlaces(q, options.limit || 12);
    } catch (e) {
      geonamesRows = [];
    }

    var items = rankResults(q, payload.savedRows, geonamesRows);
    var result = {
      mode: "results",
      query: q,
      sections: [{ id: "results", title: "Results", items: items }],
      items: items,
    };
    setCachedQuery(profileId, q, result);
    return result;
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
    parseCityStateQuery: parseCityStateQuery,
  };
})();
