/**
 * GLYPH-WIRING-1 + S5 glyph library — AstroDotBasic resolver with variant registry.
 * Export: window.__rmGlyphs
 */
(function () {
  "use strict";

  const FONT_FAMILY = "AstroDotBasic";
  const ALT_FONT_FAMILIES = { AstroDotBasic: "AstroDotBasic", AstroZLzx: "AstroZLzx" };

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

  const GLYPH_ENTITY_KEYS = {
    Mars: "mars", Uranus: "uranus", Pluto: "pluto", Capricorn: "capricorn",
  };

  const DEFAULT_GLYPH_SELECTIONS = {
    mars: "standard", uranus: "herschel", pluto: "monogram", capricorn: "us_loop",
  };

  let GLYPH_REGISTRY = null;
  let activeGlyphSelections = Object.assign({}, DEFAULT_GLYPH_SELECTIONS);

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

  function setGlyphRegistry(registry) {
    GLYPH_REGISTRY = registry && typeof registry === "object" ? registry : null;
  }

  function setGlyphSelections(selections) {
    activeGlyphSelections = Object.assign({}, DEFAULT_GLYPH_SELECTIONS);
    if (!selections || typeof selections !== "object") return;
    Object.keys(DEFAULT_GLYPH_SELECTIONS).forEach((key) => {
      if (selections[key]) activeGlyphSelections[key] = String(selections[key]);
    });
  }

  function getGlyphSelections() {
    return Object.assign({}, activeGlyphSelections);
  }

  function registryEntityFor(kind, nid) {
    if (!GLYPH_REGISTRY || !GLYPH_REGISTRY.entities) return null;
    const entityKey = GLYPH_ENTITY_KEYS[nid];
    if (!entityKey) return null;
    const entity = GLYPH_REGISTRY.entities[entityKey];
    if (!entity || entity.kind !== normalizeKind(kind)) return null;
    return { entityKey, entity };
  }

  function resolveVariantAsset(entityKey, entity) {
    const variantId = activeGlyphSelections[entityKey] || entity.default_variant;
    const variants = entity.variants || {};
    const variant = variants[variantId] || variants[entity.default_variant];
    if (!variant) return null;
    return { variantId, variant };
  }

  function resolveFromRegistry(kind, nid) {
    const hit = registryEntityFor(kind, nid);
    if (!hit) return null;
    const picked = resolveVariantAsset(hit.entityKey, hit.entity);
    if (!picked) return null;
    const v = picked.variant;
    if (v.asset_status === "stub") {
      return {
        char: "",
        useFont: false,
        isStub: true,
        stubUrl: v.stub_svg || "",
        stubLabel: v.stub_label || "stub",
        fallback: v.stub_label || "stub",
        label: hit.entity.label,
        variantId: picked.variantId,
        fontFamily: null,
        transform: null,
      };
    }
    const fam = ALT_FONT_FAMILIES[v.font_family] || FONT_FAMILY;
    return {
      char: v.char || "",
      useFont: true,
      isStub: false,
      fallback: v.char || nid,
      label: hit.entity.label,
      variantId: picked.variantId,
      fontFamily: fam,
      transform: v.transform || null,
    };
  }

  function resolveGlyph(kind, id) {
    const k = normalizeKind(kind);
    const nid = normalizeId(k, id);
    const label = nid || String(id || "");

    const reg = resolveFromRegistry(k, nid);
    if (reg) return reg;

    let char = "";
    let useFont = false;
    let fallback = label;

    if (k === "planet") {
      const fontChar = PLANET_FONT[nid];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = fontChar;
      } else {
        fallback = nid.slice(0, 2);
        char = fallback;
      }
    } else if (k === "sign") {
      const fontChar = SIGN_FONT[nid];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = fontChar;
      } else {
        fallback = nid;
        char = fallback;
      }
    } else if (k === "aspect") {
      const fontChar = ASPECT_FONT[nid];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = fontChar;
      } else {
        fallback = label;
        char = fallback;
      }
    } else if (k === "angle") {
      const fontChar = ANGLE_FONT[nid];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = nid;
      } else {
        fallback = nid;
        char = fallback;
      }
    } else if (k === "node") {
      const fontChar = NODE_FONT[nid] || NODE_FONT[String(nid).toLowerCase()];
      if (fontChar) {
        char = fontChar;
        useFont = true;
        fallback = fontChar;
      } else {
        fallback = label;
        char = fallback;
      }
    } else {
      char = label;
      fallback = label;
    }

    return {
      char, useFont, fallback, label,
      isStub: false, stubUrl: "", stubLabel: "", variantId: null,
      fontFamily: useFont ? FONT_FAMILY : null, transform: null,
    };
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

  function glyphStyleAttr(g) {
    if (!g || !g.transform) return "";
    return ` style="display:inline-block;transform:${g.transform};transform-origin:center center;"`;
  }

  function formatGlyphHtml(kind, id, opts) {
    const options = opts || {};
    const g = resolveGlyph(kind, id);
    const classes = ["rm-glyph", "rm-glyph-" + normalizeKind(kind)];
    if (options.className) classes.push(options.className);
    if (g.isStub) classes.push("rm-glyph-stub");
    else classes.push(g.useFont ? "rm-glyph-font" : "rm-glyph-fallback");
    const title = options.title != null ? options.title : g.label;
    const aria = options.ariaLabel != null ? options.ariaLabel : g.label;
    if (g.isStub && g.stubUrl) {
      return `<span class="${classes.join(" ")}" role="img" aria-label="${escapeHtml(aria)}" title="${escapeHtml(title)}"><img class="rm-glyph-stub-img" src="${escapeHtml(g.stubUrl)}" alt="${escapeHtml(g.stubLabel || "stub")}" width="1.05em" height="1.05em"${glyphStyleAttr(g)} /></span>`;
    }
    const fam = g.fontFamily || FONT_FAMILY;
    if (fam === FONT_FAMILY) classes.push("rm-glyph-font");
    else classes.push("rm-glyph-font", "rm-glyph-font-" + fam.toLowerCase());
    const display = g.useFont ? g.char : (g.fallback || g.char);
    return `<span class="${classes.join(" ")}" role="img" aria-label="${escapeHtml(aria)}" title="${escapeHtml(title)}"${glyphStyleAttr(g)}>${escapeHtml(display)}</span>`;
  }

  function formatGlyphSvgText(kind, id) {
    const g = resolveGlyph(kind, id);
    if (g.isStub) return "";
    const ch = g.useFont ? g.char : (g.fallback || g.char);
    return escapeSvgText(ch);
  }

  function formatGlyphSvgFragment(kind, id, x, y, fontSize, fill) {
    const g = resolveGlyph(kind, id);
    const fs = fontSize || 14;
    const col = fill || "#111";
    if (g.isStub && g.stubUrl) {
      const sz = fs * 1.1;
      return `<image x="${(x - sz / 2).toFixed(1)}" y="${(y - sz / 2).toFixed(1)}" width="${sz.toFixed(1)}" height="${sz.toFixed(1)}" href="${escapeHtml(g.stubUrl)}" class="rm-glyph-stub-img"><title>${escapeHtml(g.label)}</title></image>`;
    }
    const fam = g.fontFamily || FONT_FAMILY;
    const fontAttr = g.useFont ? ` font-family="${fam}, Symbola, sans-serif" class="rm-wheel-glyph-font"` : "";
    const transformAttr = g.transform ? ` transform="rotate(180 ${x} ${y})"` : "";
    const ch = g.useFont ? g.char : (g.fallback || g.char);
    return `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" text-anchor="middle" font-size="${fs.toFixed(1)}" fill="${col}"${fontAttr}${transformAttr}>${escapeSvgText(ch)}</text>`;
  }

  function svgFontFamilyAttr(g) {
    if (!g || !g.useFont) return "";
    const fam = g.fontFamily || FONT_FAMILY;
    return ` font-family="${fam}, Symbola, sans-serif" class="rm-wheel-glyph-font"`;
  }

  function listGlyphEntities() {
    if (!GLYPH_REGISTRY || !GLYPH_REGISTRY.entities) return [];
    return Object.entries(GLYPH_REGISTRY.entities).map(([key, entity]) => ({
      key,
      kind: entity.kind,
      entityId: entity.entity_id,
      label: entity.label,
      defaultVariant: entity.default_variant,
      variants: Object.entries(entity.variants || {}).map(([id, v]) => ({
        id,
        label: v.label,
        assetStatus: v.asset_status,
      })),
    }));
  }

  window.__rmGlyphs = {
    FONT_FAMILY,
    ALT_FONT_FAMILIES,
    SIGN_NAMES,
    PLANET_FONT,
    SIGN_FONT,
    ASPECT_FONT,
    ANGLE_FONT,
    NODE_FONT,
    DEFAULT_GLYPH_SELECTIONS,
    setGlyphRegistry,
    setGlyphSelections,
    getGlyphSelections,
    resolveGlyph,
    formatGlyphHtml,
    formatGlyphSvgText,
    formatGlyphSvgFragment,
    svgFontFamilyAttr,
    listGlyphEntities,
    escapeHtml,
  };
})();
