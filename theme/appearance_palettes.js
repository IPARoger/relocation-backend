/* appearance_palettes.js — curated visual palettes (Settings S4).
   Overlay, aspect, dignity, chart, and inner-glow families share the optimistic-primary
   visual language. Pinwheel / Search Map chips use overlay order (not Google rainbow). */
(function () {
  "use strict";

  var SPRING_OVERLAY = [
    "#6E93AE", "#88A97F", "#A8B99D", "#8EB6B0", "#5E8F95", "#D0A66B",
    "#D89B74", "#B76D5D", "#C98792", "#9A93B7", "#7C8A96", "#6675A8"
  ];
  var SUMMER_OVERLAY = [
    "#4F83B5", "#5FA7A5", "#6FAE84", "#A7BE65", "#D3B15F", "#D89B52",
    "#D67A65", "#B95F52", "#D38DA0", "#9686C8", "#718AA2", "#556A94"
  ];
  var WINTER_OVERLAY = [
    "#5A7EA4", "#6D91A5", "#7FA6A2", "#7F9A81", "#B9A271", "#B97D67",
    "#B06D62", "#B78B9B", "#9B92B4", "#8278A4", "#7E8B95", "#596B8F"
  ];

  var PALETTES = {
    overlay: {
      "optimistic-primary": {
        label: "Optimistic Primary",
        desc: "Spring doctrine — travel, hope, and possibility",
        colors: SPRING_OVERLAY,
        not: "#2C3338"
      },
      "summer-expansion": {
        label: "Summer Expansion",
        desc: "Energetic exploration and active movement",
        colors: SUMMER_OVERLAY,
        not: "#2A2F38"
      },
      "winter-clarity": {
        label: "Winter Clarity",
        desc: "Cool focus for comparison and study",
        colors: WINTER_OVERLAY,
        not: "#272D34"
      }
    },
    aspect: {
      "optimistic-primary": {
        label: "Optimistic Primary",
        desc: "Green harmonious · red challenging · blue motion",
        harmonious: "#46a862",
        challenging: "#e85c4f",
        minor: "#4084d6",
        applying: "#e85c4f",
        separating: "#4084d6"
      },
      "spring-harmony": {
        label: "Spring Harmony",
        desc: "Doctrine accents — juniper, terracotta, horizon",
        harmonious: "#88A97F",
        challenging: "#B76D5D",
        minor: "#5E8F95",
        applying: "#D0A66B",
        separating: "#6E93AE"
      }
    },
    dignity: {
      "optimistic-soft": {
        label: "Optimistic Soft",
        desc: "Readable PIH washes — supportive and challenging families",
        supportive: "#e8f5ec",
        challenging: "#fdf0e8",
        exaltation: "#ddf3e4",
        fall: "#fce8d8"
      },
      "spring-mist": {
        label: "Spring Mist",
        desc: "Calm paper tints aligned to Spring doctrine",
        supportive: "#eef7f3",
        challenging: "#faf3e8",
        exaltation: "#e8f4ec",
        fall: "#fdf0e0"
      }
    },
    chart: {
      "optimistic-primary": {
        label: "Optimistic Primary",
        desc: "Core ink wheel with doctrine accents",
        ink: "#252A2E",
        cusp: "#7C8A96",
        divider: "#9AA3AD",
        tick5: "#DDE3DD",
        innerSoft: "#8A9198",
        base: "#F4F5F1",
        band: "#E7ECE7",
        glowColor: "#88A97F",
        glowAlpha: 0.07,
        glowReach: 0.20,
        paperOpacity: 0.04,
        p2pHarmonious: "#46a862",
        p2pChallenging: "#e85c4f",
        p2pMinor: "#4084d6"
      },
      "warm-stone": {
        label: "Warm Stone",
        desc: "Beta warm-grey wheel (legacy)",
        ink: "#2b2926",
        cusp: "#8a857a",
        divider: "#9b968b",
        tick5: "#c4bfb2",
        innerSoft: "#9a9485",
        base: "#eae8e3",
        band: "#f1ece0",
        glowColor: "#b89a55",
        glowAlpha: 0.16,
        glowReach: 0.20,
        paperOpacity: 0.05,
        p2pHarmonious: "#2563eb",
        p2pChallenging: "#dc2626",
        p2pMinor: "#16a34a"
      }
    },
    inner_glow: {
      "micro-green": {
        label: "Micro Green",
        desc: "Relocation promise — subtle radial wash",
        glowColor: "#46a35e",
        glowAlpha: 0.07,
        glowReach: 0.20
      },
      "micro-blue": {
        label: "Micro Blue",
        desc: "Current-location emphasis",
        glowColor: "#3a82d6",
        glowAlpha: 0.07,
        glowReach: 0.20
      },
      "micro-warm": {
        label: "Micro Warm",
        desc: "Brass horizon warmth",
        glowColor: "#D0A66B",
        glowAlpha: 0.08,
        glowReach: 0.18
      }
    }
  };

  var DEFAULTS = {
    overlay_palette: "optimistic-primary",
    aspect_palette: "optimistic-primary",
    dignity_palette: "optimistic-soft",
    chart_palette: "optimistic-primary",
    inner_glow_palette: "micro-green"
  };

  function pickId(eff, key) {
    var e = eff || {};
    var val = e[key];
    return (val && typeof val === "string") ? val : DEFAULTS[key];
  }

  function resolvePaletteIds(eff) {
    return {
      overlay: pickId(eff, "overlay_palette"),
      aspect: pickId(eff, "aspect_palette"),
      dignity: pickId(eff, "dignity_palette"),
      chart: pickId(eff, "chart_palette"),
      inner_glow: pickId(eff, "inner_glow_palette")
    };
  }

  function bucket(cat, id) {
    var map = PALETTES[cat] || {};
    var defKey = DEFAULTS[cat + "_palette"];
    return map[id] || map[defKey] || map[Object.keys(map)[0]];
  }

  function getResolved(eff) {
    var ids = resolvePaletteIds(eff);
    var overlay = bucket("overlay", ids.overlay);
    var aspect = bucket("aspect", ids.aspect);
    var dignity = bucket("dignity", ids.dignity);
    var chartBase = bucket("chart", ids.chart);
    var inner = bucket("inner_glow", ids.inner_glow);
    var chart = {};
    var k;
    for (k in chartBase) { if (Object.prototype.hasOwnProperty.call(chartBase, k)) chart[k] = chartBase[k]; }
    chart.glowColor = inner.glowColor;
    chart.glowAlpha = inner.glowAlpha;
    chart.glowReach = inner.glowReach;
    return {
      ids: ids,
      overlay: overlay,
      aspect: aspect,
      dignity: dignity,
      chart: chart,
      pinwheel: overlay.colors || SPRING_OVERLAY,
      not: overlay.not || "#2C3338"
    };
  }

  function dignityColorsFromResolved(resolved) {
    var d = resolved.dignity;
    return {
      supportive: d.supportive,
      challenging: d.challenging,
      exaltation: d.exaltation,
      fall: d.fall
    };
  }

  function applyCssVariables(eff) {
    var r = getResolved(eff);
    var root = document.documentElement;
    var i;
    for (i = 0; i < r.pinwheel.length; i++) {
      root.style.setProperty("--th-ov-" + (i + 1), r.pinwheel[i]);
      root.style.setProperty("--rm-ov-" + (i + 1), r.pinwheel[i]);
    }
    root.style.setProperty("--th-not", r.not);
    root.style.setProperty("--rm-not", r.not);
    root.style.setProperty("--rm-aspect-harmonious", r.aspect.harmonious);
    root.style.setProperty("--rm-aspect-challenging", r.aspect.challenging);
    root.style.setProperty("--rm-aspect-minor", r.aspect.minor);
    root.style.setProperty("--rm-aspect-applying", r.aspect.applying);
    root.style.setProperty("--rm-aspect-separating", r.aspect.separating);
    root.style.setProperty("--rm-dignity-supportive", r.dignity.supportive);
    root.style.setProperty("--rm-dignity-challenging", r.dignity.challenging);
    root.style.setProperty("--rm-dignity-exaltation", r.dignity.exaltation);
    root.style.setProperty("--rm-dignity-fall", r.dignity.fall);
    root.style.setProperty("--rm-wheel-ink", r.chart.ink);
    root.style.setProperty("--rm-wheel-cusp", r.chart.cusp);
    root.style.setProperty("--rm-wheel-divider", r.chart.divider);
    root.style.setProperty("--rm-wheel-tick5", r.chart.tick5);
    root.style.setProperty("--rm-wheel-inner-soft", r.chart.innerSoft);
    root.style.setProperty("--rm-wheel-base", r.chart.base);
    root.style.setProperty("--rm-wheel-band", r.chart.band);
    root.style.setProperty("--rm-wheel-glow-color", r.chart.glowColor);
    root.style.setProperty("--rm-wheel-glow-alpha", String(r.chart.glowAlpha));
    root.style.setProperty("--rm-wheel-glow-reach", String(r.chart.glowReach));
    root.style.setProperty("--rm-wheel-p2p-harmonious", r.chart.p2pHarmonious);
    root.style.setProperty("--rm-wheel-p2p-challenging", r.chart.p2pChallenging);
    root.style.setProperty("--rm-wheel-p2p-minor", r.chart.p2pMinor);
    return r;
  }

  window.RMAppearancePalettes = {
    PALETTES: PALETTES,
    DEFAULTS: DEFAULTS,
    getResolved: getResolved,
    resolvePaletteIds: resolvePaletteIds,
    dignityColorsFromResolved: dignityColorsFromResolved,
    applyCssVariables: applyCssVariables,
    pinwheelColors: function (eff) { return getResolved(eff).pinwheel; },
    overlayColors: function (eff) { return getResolved(eff).pinwheel; },
    notColor: function (eff) { return getResolved(eff).not; }
  };
})();
