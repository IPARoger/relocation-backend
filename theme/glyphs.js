/**
 * GLYPH-WIRING-1 — central AstroDotBasic glyph resolver (temporary production standard).
 * Character map per AstroDotBasic.ttf specimen (A–U planets, a–l signs, m–y aspects). Export: window.__rmGlyphs
 */
(function () {
  "use strict";

  const FONT_FAMILY = "AstroDotBasic";

  const SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
  ];

  const PLANET_FONT = {
    Sun: "A", Moon: "B", Mercury: "C", Venus: "D", Mars: "E",
    Jupiter: "F", Saturn: "G", Uranus: "H", Neptune: "I", Pluto: "J",
    Chiron: "U",
    "North Node": "L", "South Node": "M",
  };

  const SIGN_FONT = {
    Aries: "a", Taurus: "b", Gemini: "c", Cancer: "d", Leo: "e", Virgo: "f",
    Libra: "g", Scorpio: "h", Sagittarius: "i", Capricorn: "j", Aquarius: "k", Pisces: "l",
  };

  const ASPECT_FONT = {
    conjunction: "m", conjunct: "m",
    opposition: "n",
    square: "o",
    trine: "p",
    sextile: "q",
    semisextile: "r",
    quincunx: "s", inconjunct: "s",
    semisquare: "t",
    sesquiquadrate: "u",
    biquintile: "v",
    quintile: "w",
    parallel: "x",
    contraparallel: "y",
  };

  const ANGLE_FONT = { ASC: "P", MC: "Q" };

  const NODE_FONT = {
    "North Node": "L", "South Node": "M",
    north_node: "L", south_node: "M",
    "north node": "L", "south node": "M",
  };

  const UNICODE = {
    planets: {
      Sun: "\u2609", Moon: "\u263d", Mercury: "\u263f", Venus: "\u2640", Mars: "\u2642",
      Jupiter: "\u2643", Saturn: "\u2644", Uranus: "\u2645", Neptune: "\u2646", Pluto: "\u2647",
      Chiron: "\u26b7",
    },
    signs: {
      Aries: "\u2648", Taurus: "\u2649", Gemini: "\u264a", Cancer: "\u264b", Leo: "\u264c", Virgo: "\u264d",
      Libra: "\u264e", Scorpio: "\u264f", Sagittarius: "\u2650", Capricorn: "\u2651", Aquarius: "\u2652", Pisces: "\u2653",
    },
    aspects: {
      conjunct: "\u260c", conjunction: "\u260c",
      opposition: "\u260d",
      square: "\u25a1",
      trine: "\u25b3",
      sextile: "\u26b9",
      semisextile: "\u26ba",
      quincunx: "\u26bb", inconjunct: "\u26bb",
      semisquare: "\u2220",
      sesquiquadrate: "\u26bc",
      biquintile: "\u25c7",
      quintile: "\u25c6",
    },
    angles: { ASC: "ASC", MC: "MC", IC: "IC", DSC: "DSC" },
    nodes: { "North Node": "\u260a", "South Node": "\u260b", north_node: "\u260a", south_node: "\u260b" },
  };

  function normalizeKind(kind) {
    return String(kind || "").toLowerCase().trim();
  }

  function titleCaseSign(raw) {
    const s = String(raw || "").trim().toLowerCase();
    if (!s) return "";
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  function titleCasePlanet(raw) {
    const s = String(raw || "").trim();
    if (!s) return "";
    if (s === "Sun" || s === "Moon") return s;
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
  }

  function normalizeAspectId(raw) {
    return String(raw || "").trim().toLowerCase();
  }

  function normalizeId(kind, id) {
    const k = normalizeKind(kind);
    const raw = id;
    if (raw == null || raw === "") return "";
    if (k === "sign") return titleCaseSign(raw);
    if (k === "planet") return titleCasePlanet(raw);
    if (k === "aspect") return normalizeAspectId(raw);
    if (k === "angle") return String(raw).trim().toUpperCase();
    if (k === "node") return String(raw).trim();
    return String(raw).trim();
  }

  function resolveGlyph(kind, id) {
    const k = normalizeKind(kind);
    const nid = normalizeId(k, id);
    const label = nid || String(id || "");
    let char = "";
    let useFont = false;
    let fallback = label;

    if (k === "planet") {
      const fontChar = PLANET_FONT[nid];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = UNICODE.planets[nid] || nid;
      } else {
        fallback = UNICODE.planets[nid] || nid.slice(0, 2);
        char = fallback;
      }
    } else if (k === "sign") {
      const fontChar = SIGN_FONT[nid];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = UNICODE.signs[nid] || nid;
      } else {
        fallback = UNICODE.signs[nid] || nid;
        char = fallback;
      }
    } else if (k === "aspect") {
      const fontChar = ASPECT_FONT[nid];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = UNICODE.aspects[nid] || label;
      } else {
        fallback = UNICODE.aspects[nid] || label;
        char = fallback;
      }
    } else if (k === "angle") {
      const fontChar = ANGLE_FONT[nid];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = UNICODE.angles[nid] || nid;
      } else {
        fallback = UNICODE.angles[nid] || nid;
        char = fallback;
      }
    } else if (k === "node") {
      const fontChar = NODE_FONT[nid] || NODE_FONT[String(nid).toLowerCase()];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = UNICODE.nodes[nid] || label;
      } else {
        fallback = UNICODE.nodes[nid] || label;
        char = fallback;
      }
    } else {
      char = label;
      fallback = label;
    }

    return { char, useFont, fallback, label };
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function escapeSvgText(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;");
  }

  function formatGlyphHtml(kind, id, opts) {
    const options = opts || {};
    const g = resolveGlyph(kind, id);
    const classes = ["rm-glyph", "rm-glyph-" + normalizeKind(kind)];
    if (options.className) classes.push(options.className);
    classes.push(g.useFont ? "rm-glyph-font" : "rm-glyph-fallback");
    const title = options.title != null ? options.title : g.label;
    const aria = options.ariaLabel != null ? options.ariaLabel : g.label;
    const display = g.useFont ? g.char : (g.fallback || g.char);
    return `<span class="${classes.join(" ")}" role="img" aria-label="${escapeHtml(aria)}" title="${escapeHtml(title)}">${escapeHtml(display)}</span>`;
  }

  function formatGlyphSvgText(kind, id) {
    const g = resolveGlyph(kind, id);
    const ch = g.useFont ? g.char : (g.fallback || g.char);
    return escapeSvgText(ch);
  }

  function svgFontFamilyAttr(g) {
    return g && g.useFont ? ` font-family="${FONT_FAMILY}, Symbola, sans-serif" class="rm-wheel-glyph-font"` : "";
  }

  window.__rmGlyphs = {
    FONT_FAMILY,
    SIGN_NAMES,
    PLANET_FONT,
    SIGN_FONT,
    ASPECT_FONT,
    ANGLE_FONT,
    NODE_FONT,
    resolveGlyph,
    formatGlyphHtml,
    formatGlyphSvgText,
    svgFontFamilyAttr,
    escapeHtml,
  };
})();
