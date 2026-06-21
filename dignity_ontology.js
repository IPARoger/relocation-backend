/**
 * dignity_ontology.js — Layer-2 dignity lookup (DIGNITIES-1, DIGNITIES-HOUSE-1).
 * Sign essential dignity + house correspondence via natural zodiac.
 */
(function () {
  "use strict";

  var REL = {
    RULERSHIP: "rulership",
    EXALTATION: "exaltation",
    DETRIMENT: "detriment",
    FALL: "fall",
  };

  var BY_PLANET = {
    Sun: {
      Aries: REL.EXALTATION,
      Leo: REL.RULERSHIP,
      Libra: REL.FALL,
      Aquarius: REL.DETRIMENT,
    },
    Moon: {
      Taurus: REL.EXALTATION,
      Cancer: REL.RULERSHIP,
      Scorpio: REL.FALL,
      Capricorn: REL.DETRIMENT,
    },
    Mercury: {
      Gemini: REL.RULERSHIP,
      Virgo: REL.RULERSHIP,
      Pisces: REL.DETRIMENT,
      Sagittarius: REL.DETRIMENT,
    },
    Venus: {
      Taurus: REL.RULERSHIP,
      Libra: REL.RULERSHIP,
      Aries: REL.DETRIMENT,
      Scorpio: REL.DETRIMENT,
      Pisces: REL.EXALTATION,
      Virgo: REL.FALL,
    },
    Mars: {
      Aries: REL.RULERSHIP,
      Scorpio: REL.RULERSHIP,
      Libra: REL.DETRIMENT,
      Taurus: REL.DETRIMENT,
      Capricorn: REL.EXALTATION,
      Cancer: REL.FALL,
    },
    Jupiter: {
      Sagittarius: REL.RULERSHIP,
      Pisces: REL.RULERSHIP,
      Gemini: REL.DETRIMENT,
      Virgo: REL.DETRIMENT,
      Cancer: REL.EXALTATION,
      Capricorn: REL.FALL,
    },
    Saturn: {
      Capricorn: REL.RULERSHIP,
      Aquarius: REL.RULERSHIP,
      Cancer: REL.DETRIMENT,
      Leo: REL.DETRIMENT,
      Libra: REL.EXALTATION,
      Aries: REL.FALL,
    },
  };

  function normSign(sign) {
    var s = String(sign || "").trim();
    if (!s) return "";
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
  }

  function parseSignFromLongitudeFormatted(fmt) {
    if (!fmt) return null;
    var m = String(fmt).match(/°\s*([A-Za-z]+)/);
    return m ? normSign(m[1]) : null;
  }

  function lookupRelationship(planet, sign) {
    var p = String(planet || "").trim();
    var s = normSign(sign);
    if (!p || !s || !BY_PLANET[p]) return null;
    return BY_PLANET[p][s] || null;
  }

  function lookupFamily(planet, sign) {
    var rel = lookupRelationship(planet, sign);
    if (!rel) return null;
    if (rel === REL.RULERSHIP || rel === REL.EXALTATION) return "supportive";
    if (rel === REL.DETRIMENT || rel === REL.FALL) return "challenging";
    return null;
  }

  // Natural zodiac: house N corresponds to sign N (Aries = 1st house, …).
  var NATURAL_HOUSE_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
  ];

  function lookupFamilyByHouse(planet, house) {
    var h = parseInt(house, 10);
    if (!Number.isFinite(h) || h < 1 || h > 12) return null;
    var sign = NATURAL_HOUSE_SIGNS[h - 1];
    return lookupFamily(planet, sign);
  }

  window.RMDignityOntology = {
    lookupRelationship: lookupRelationship,
    lookupFamily: lookupFamily,
    lookupFamilyByHouse: lookupFamilyByHouse,
    parseSignFromLongitudeFormatted: parseSignFromLongitudeFormatted,
  };
})();
