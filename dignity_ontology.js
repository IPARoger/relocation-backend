/**
 * dignity_ontology.js — dignity presets, custom rules, PIH house correspondence.
 */
(function () {
  "use strict";

  var REL = {
    RULERSHIP: "rulership",
    EXALTATION: "exaltation",
    DETRIMENT: "detriment",
    FALL: "fall",
  };

  var SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
  ];

  var PLANETS = [
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
    "Uranus", "Neptune", "Pluto",
  ];

  var NATURAL_HOUSE_SIGNS = SIGNS.slice();

  function cloneMap(src) {
    var out = {};
    Object.keys(src || {}).forEach(function (p) {
      out[p] = Object.assign({}, src[p]);
    });
    return out;
  }

  function mergeMaps() {
    var out = {};
    for (var i = 0; i < arguments.length; i++) {
      var m = arguments[i];
      Object.keys(m || {}).forEach(function (p) {
        if (!out[p]) out[p] = {};
        Object.assign(out[p], m[p]);
      });
    }
    return out;
  }

  var ANCIENT = {
    Sun: { Aries: REL.EXALTATION, Leo: REL.RULERSHIP, Libra: REL.FALL, Aquarius: REL.DETRIMENT },
    Moon: { Taurus: REL.EXALTATION, Cancer: REL.RULERSHIP, Scorpio: REL.FALL, Capricorn: REL.DETRIMENT },
    Mercury: { Gemini: REL.RULERSHIP, Virgo: REL.RULERSHIP, Pisces: REL.DETRIMENT, Sagittarius: REL.DETRIMENT },
    Venus: { Taurus: REL.RULERSHIP, Libra: REL.RULERSHIP, Aries: REL.DETRIMENT, Scorpio: REL.DETRIMENT, Pisces: REL.EXALTATION, Virgo: REL.FALL },
    Mars: { Aries: REL.RULERSHIP, Scorpio: REL.RULERSHIP, Libra: REL.DETRIMENT, Taurus: REL.DETRIMENT, Capricorn: REL.EXALTATION, Cancer: REL.FALL },
    Jupiter: { Sagittarius: REL.RULERSHIP, Pisces: REL.RULERSHIP, Gemini: REL.DETRIMENT, Virgo: REL.DETRIMENT, Cancer: REL.EXALTATION, Capricorn: REL.FALL },
    Saturn: { Capricorn: REL.RULERSHIP, Aquarius: REL.RULERSHIP, Cancer: REL.DETRIMENT, Leo: REL.DETRIMENT, Libra: REL.EXALTATION, Aries: REL.FALL },
  };

  var MODERN_OUTERS = {
    Uranus: { Aquarius: REL.RULERSHIP, Leo: REL.DETRIMENT },
    Neptune: { Pisces: REL.RULERSHIP, Virgo: REL.DETRIMENT },
    Pluto: { Scorpio: REL.RULERSHIP, Taurus: REL.DETRIMENT },
  };

  function buildModern() {
    var m = cloneMap(ANCIENT);
    if (m.Jupiter) delete m.Jupiter.Pisces;
    if (m.Saturn) delete m.Saturn.Aquarius;
    if (m.Mars) delete m.Mars.Scorpio;
    return mergeMaps(m, MODERN_OUTERS);
  }

  function buildHybrid() {
    return mergeMaps(ANCIENT, MODERN_OUTERS);
  }

  var PRESET_MAPS = {
    ancient: ANCIENT,
    modern: buildModern(),
    hybrid: buildHybrid(),
  };

  var activeConfig = {
    preset: "hybrid",
    customRules: [],
    colorMode: "paired",
    colors: {
      supportive: "#eef7f3",
      challenging: "#faf3e8",
      exaltation: "#e8f4ec",
      fall: "#fdf0e0",
    },
  };

  var activeByPlanet = buildHybrid();

  function normSign(sign) {
    var s = String(sign || "").trim();
    if (!s) return "";
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
  }

  function normPlanet(planet) {
    var p = String(planet || "").trim();
    if (!p) return "";
    return p.charAt(0).toUpperCase() + p.slice(1).toLowerCase();
  }

  function normRel(type) {
    var t = String(type || "").trim().toLowerCase();
    if (t === "ruler" || t === "rules") return REL.RULERSHIP;
    if (t === "detriment") return REL.DETRIMENT;
    if (t === "exaltation") return REL.EXALTATION;
    if (t === "fall") return REL.FALL;
    return t;
  }

  function rulesToMap(rules) {
    var out = {};
    (rules || []).forEach(function (r) {
      if (!r) return;
      var p = normPlanet(r.planet);
      var s = normSign(r.sign);
      var rel = normRel(r.relationship || r.type);
      if (!p || !s || !rel) return;
      if (!out[p]) out[p] = {};
      out[p][s] = rel;
    });
    return out;
  }

  function rebuildActiveMap() {
    if (activeConfig.preset === "custom") {
      activeByPlanet = rulesToMap(activeConfig.customRules);
    } else {
      activeByPlanet = cloneMap(PRESET_MAPS[activeConfig.preset] || PRESET_MAPS.hybrid);
    }
  }

  function applyCssColors() {
    if (typeof document === "undefined") return;
    var c = activeConfig.colors || {};
    var root = document.documentElement;
    root.style.setProperty("--rm-dignity-supportive", c.supportive || "#eef7f3");
    root.style.setProperty("--rm-dignity-challenging", c.challenging || "#faf3e8");
    root.style.setProperty("--rm-dignity-exaltation", c.exaltation || c.supportive || "#e8f4ec");
    root.style.setProperty("--rm-dignity-fall", c.fall || c.challenging || "#fdf0e0");
  }

  function setConfig(cfg) {
    if (!cfg || typeof cfg !== "object") return;
    if (cfg.preset) activeConfig.preset = String(cfg.preset);
    if (Array.isArray(cfg.customRules)) activeConfig.customRules = cfg.customRules.slice();
    if (cfg.colorMode) activeConfig.colorMode = cfg.colorMode === "four" ? "four" : "paired";
    if (cfg.colors && typeof cfg.colors === "object") {
      activeConfig.colors = Object.assign({}, activeConfig.colors, cfg.colors);
    }
    rebuildActiveMap();
    applyCssColors();
  }

  function parseSignFromLongitudeFormatted(fmt) {
    if (!fmt) return null;
    var m = String(fmt).match(/°\s*([A-Za-z]+)/);
    return m ? normSign(m[1]) : null;
  }

  function lookupRelationship(planet, sign) {
    var p = normPlanet(planet);
    var s = normSign(sign);
    if (!p || !s || !activeByPlanet[p]) return null;
    return activeByPlanet[p][s] || null;
  }

  function lookupFamily(planet, sign) {
    var rel = lookupRelationship(planet, sign);
    if (!rel) return null;
    if (rel === REL.RULERSHIP || rel === REL.EXALTATION) return "supportive";
    if (rel === REL.DETRIMENT || rel === REL.FALL) return "challenging";
    return null;
  }

  function lookupFamilyByHouse(planet, house) {
    var h = parseInt(house, 10);
    if (!Number.isFinite(h) || h < 1 || h > 12) return null;
    return lookupFamily(planet, NATURAL_HOUSE_SIGNS[h - 1]);
  }

  function lookupDetailByHouse(planet, house) {
    var h = parseInt(house, 10);
    if (!Number.isFinite(h) || h < 1 || h > 12) return null;
    return lookupRelationship(planet, NATURAL_HOUSE_SIGNS[h - 1]);
  }

  function rulersForSign(sign) {
    var s = normSign(sign);
    var rulers = [];
    Object.keys(activeByPlanet).forEach(function (p) {
      if (activeByPlanet[p][s] === REL.RULERSHIP) rulers.push(p);
    });
    return rulers;
  }

  function presetExample(presetId) {
    var id = presetId || activeConfig.preset;
    if (id === "ancient") return "Jupiter rules Pisces";
    if (id === "modern") return "Neptune rules Pisces";
    if (id === "hybrid") return "Jupiter + Neptune rule Pisces";
    return "Custom dignity rules";
  }

  function getConfig() {
    return {
      preset: activeConfig.preset,
      customRules: activeConfig.customRules.slice(),
      colorMode: activeConfig.colorMode,
      colors: Object.assign({}, activeConfig.colors),
    };
  }

  setConfig({ preset: "hybrid" });

  window.RMDignityOntology = {
    REL: REL,
    SIGNS: SIGNS,
    PLANETS: PLANETS,
    PRESETS: ["ancient", "modern", "hybrid", "custom"],
    setConfig: setConfig,
    getConfig: getConfig,
    presetExample: presetExample,
    rulersForSign: rulersForSign,
    lookupRelationship: lookupRelationship,
    lookupFamily: lookupFamily,
    lookupFamilyByHouse: lookupFamilyByHouse,
    lookupDetailByHouse: lookupDetailByHouse,
    parseSignFromLongitudeFormatted: parseSignFromLongitudeFormatted,
  };
})();
