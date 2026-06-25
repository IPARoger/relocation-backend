/**
 * V5-1 shadow hydration adapter — maps live comparison data to mockup anchors.
 * Canonical path: validation/mockups/beta/comparison_v5_adapter.js
 * Consumes existing app shapes only; does not define new fetch routes or backend contracts.
 */
(function (global) {
  "use strict";

  var AIS_ANGLE_ROWS = [
    { key: "ASC", label: "ASC" },
    { key: "DSC", label: "DSC" },
    { key: "MC", label: "MC" },
    { key: "IC", label: "IC" },
  ];

  var ATA_PLANETS = [
    "Sun", "Moon", "Mercury", "Venus", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron",
  ];

  var PIH_ROWS = [
    "Sun", "Moon", "Mercury", "Venus", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron",
    "North Node", "South Node",
  ];

  var CMP_CAPACITY_RESERVED = 5;

  var CI_CATEGORY_LABELS = [
    "Regional context",
    "Safety",
    "Cost of living",
    "Professional / expat environment",
    "Climate",
    "Mobility / transit",
    "Regional character",
  ];

  var CI_PLACEHOLDER_SNIPPETS = ["—", "—", "—", "—", "—", "—", "—"];

  var COL_LABEL = 200;
  var COL_CITY = 158;
  var COL_STUB = 52;
  var COL_ADD = 72;

  var A2A_ASP_ABBR = {
    conjunction: "Conj",
    square: "Sq",
    trine: "Tri",
    opposition: "Opp",
    sextile: "Sext",
  };

  function esc(deps, s) {
    if (deps && typeof deps.escapeHtml === "function") return deps.escapeHtml(s == null ? "" : String(s));
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function ord(n) {
    var num = Number(n);
    if (!Number.isFinite(num)) return "\u2014";
    var s = num % 100;
    var t = num % 10;
    if (s >= 11 && s <= 13) return num + "th";
    return num + (t === 1 ? "st" : t === 2 ? "nd" : t === 3 ? "rd" : "th");
  }

  function mountEl(root, name) {
    return root ? root.querySelector('[data-cmp-mount="' + name + '"]') : null;
  }

  function resolveColumnOrder(ws, placeIds) {
    var ids = Array.isArray(placeIds) ? placeIds.slice() : [];
    if (!ws || !Array.isArray(ws.column_order_place_ids)) return ids;
    var order = ws.column_order_place_ids.filter(function (id) { return ids.indexOf(id) >= 0; });
    ids.forEach(function (id) {
      if (order.indexOf(id) < 0) order.push(id);
    });
    return order;
  }

  function resolveHiddenSet(ws) {
    var hidden = ws && Array.isArray(ws.hidden_place_ids) ? ws.hidden_place_ids : [];
    return new Set(hidden);
  }

  function resolveVisibleOrderedPlaceIds(ws, placeIds) {
    var ordered = resolveColumnOrder(ws, placeIds);
    var hidden = resolveHiddenSet(ws);
    return ordered.filter(function (id) { return !hidden.has(id); });
  }

  function resolveActiveAngleKey(ws) {
    var tab = (ws && ws.active_angle_tab) || "asc";
    if (tab === "all" || tab === "mc") return tab === "mc" ? "MC" : "ASC";
    return String(tab).toUpperCase();
  }

  function splitCityNameLines(name) {
    var parts = String(name || "").split(",");
    return {
      line1: (parts[0] || "").trim() || String(name || ""),
      line2: parts.slice(1).join(",").trim(),
    };
  }

  function placeCoordsDisplay(deps, placeId) {
    if (!deps || typeof deps.resolvePlaceLatLon !== "function") return "\u2014";
    var c = deps.resolvePlaceLatLon(placeId);
    if (!c || typeof deps.formatPlateLatLonDisplay !== "function") return "\u2014";
    return deps.formatPlateLatLonDisplay(c.lat, c.lon) || "\u2014";
  }

  function cityTagForPlace(ctx, placeId) {
    var deps = ctx.deps || {};
    var chartId = ctx.chartRecord && ctx.chartRecord.chartRecordId;
    if (deps.resolveBirthPlaceId && chartId && deps.resolveBirthPlaceId(chartId) === placeId) return "Natal";
    if (deps.resolveCurrentLocationPlaceId && chartId && deps.resolveCurrentLocationPlaceId(chartId) === placeId) return "Current";
    var favs = (ctx.chartRecord && ctx.chartRecord.favorites) || [];
    if (favs.some(function (f) { return f.placeId === placeId; })) return "Favorite";
    return null;
  }

  function colByPlaceId(cols, placeId) {
    return (cols || []).find(function (c) { return c.placeId === placeId; }) || null;
  }

  function canonicalFromCol(deps, col) {
    if (!col || col.error || !deps || typeof deps.getCanonicalChartFromPayload !== "function") return null;
    return deps.getCanonicalChartFromPayload(col.chart);
  }

  function buildFactTable(labels, visibleCols, getCell, colPlaceIds, rowMeta) {
    rowMeta = rowMeta || {};
    var W = COL_LABEL + visibleCols.length * COL_CITY;
    var h = '<table class="fact-table" data-cmp-v5-hydrated="true" style="width:' + W + 'px;table-layout:fixed;border-collapse:collapse">';
    h += '<colgroup><col style="width:' + COL_LABEL + 'px">';
    visibleCols.forEach(function () { h += '<col style="width:' + COL_CITY + 'px">'; });
    h += "</colgroup><tbody>";
    labels.forEach(function (label, rowIdx) {
      var rowKeys = visibleCols.map(function (col, colIdx) {
        var pid = colPlaceIds[colIdx];
        if (typeof rowMeta.rowKey === "function") return rowMeta.rowKey(pid, rowIdx, col);
        return null;
      });
      var labelOut = (typeof rowMeta.labelHtml === "function") ? rowMeta.labelHtml(label, rowIdx) : label;
      h += "<tr><td class=\"label-col\">" + labelOut + "</td>";
      visibleCols.forEach(function (col, colIdx) {
        var pid = colPlaceIds[colIdx];
        var v = getCell(pid, rowIdx, col);
        var tex = (colIdx % 2 === 0) ? " cmp-col-texture-a" : " cmp-col-texture-b";
        var diffCls = typeof rowMeta.diffTdClass === "function"
          ? (rowMeta.diffTdClass(rowKeys[colIdx], rowKeys) || "") : "";
        var extraCls = typeof rowMeta.extraTdClass === "function"
          ? (rowMeta.extraTdClass(pid, rowIdx, col) || "") : "";
        h += '<td class="val-col' + tex + diffCls + extraCls + '" data-cmp-col-index="' + colIdx + '">' + (v != null ? v : '<span class="ph">&mdash;</span>') + "</td>";
      });
      h += "</tr>";
    });
    h += "</tbody></table>";
    return h;
  }

  function mapAuthority(root, ctx) {
    var el = mountEl(root, "authority");
    if (!el || !ctx.chartRecord) return;
    var r = ctx.chartRecord;
    var deps = ctx.deps || {};
    var coordsMeta = typeof deps.profilePlateReferenceMetaLine === "function"
      ? deps.profilePlateReferenceMetaLine(r.chartRecordId)
      : "";
    var birthLine = typeof deps.formatComparisonAuthorityBirthDate === "function"
      ? deps.formatComparisonAuthorityBirthDate(r.birthDate)
      : r.birthDate;
    var glyph = typeof deps.comparisonAuthorityGlyphHtml === "function"
      ? deps.comparisonAuthorityGlyphHtml(r)
      : '<span class="glyph glyph-slot" aria-hidden="true"></span>';
    el.innerHTML =
      '<div class="zb-name"><span class="nmwrap"><span class="nm">' + esc(deps, r.displayName) + "</span>" +
      '<span class="tools">' +
      '<button type="button" class="profile-caret" title="Switch profile" tabindex="-1" aria-hidden="true">&#9662;</button>' +
      '<button type="button" class="profile-btn" title="Edit birth data" tabindex="-1" aria-hidden="true">Edit</button>' +
      '<button type="button" class="profile-btn plus" title="Add profile" tabindex="-1" aria-hidden="true">+</button>' +
      "</span></span></div>" +
      '<div class="zb-primary">' + esc(deps, birthLine) + " \u00b7 " + esc(deps, r.birthTimeDisplay) + " " + glyph + "</div>" +
      '<div class="zb-primary">' + esc(deps, r.birthCity) + "</div>" +
      (coordsMeta ? '<div class="zb-meta">' + esc(deps, coordsMeta) + "</div>" : "") +
      '<div class="zb-meta">Tropical \u00b7 Placidus</div>';
  }

  function mapCityBar(root, ctx) {
    var el = mountEl(root, "city-bar-inner");
    if (!el || !ctx.comparisonSet) return;
    var deps = ctx.deps || {};
    var placeIds = ctx.comparisonSet.placeIds || [];
    var ws = ctx.workspaceState || {};
    var order = resolveColumnOrder(ws, placeIds);
    var hidden = resolveHiddenSet(ws);
    var visible = resolveVisibleOrderedPlaceIds(ws, placeIds);
    var nameById = (deps.viewModelPlaceNameById) || {};
    var favs = (ctx.chartRecord && ctx.chartRecord.favorites) || [];

    var canAdd = order.length < CMP_CAPACITY_RESERVED;
    var W = COL_LABEL;
    order.forEach(function (pid) { W += hidden.has(pid) ? COL_STUB : COL_CITY; });
    if (canAdd) W += COL_ADD;

    var h = '<table class="city-bar-table" data-cmp-v5-hydrated="true" style="width:' + W + 'px;table-layout:fixed;border-collapse:collapse">';
    h += '<colgroup><col style="width:' + COL_LABEL + 'px">';
    order.forEach(function (pid) {
      h += '<col style="width:' + (hidden.has(pid) ? COL_STUB : COL_CITY) + 'px">';
    });
    if (canAdd) h += '<col style="width:' + COL_ADD + 'px">';
    h += '</colgroup><tbody><tr>';
    h += '<td class="bar-label"><div class="bar-authority" data-cmp-role="authority-sticky-transform" data-cmp-authority-source="rm-cmp-zone-b">';
    if (ctx.chartRecord) {
      h += '<div class="ba-name">' + esc(deps, ctx.chartRecord.displayName) + "</div>";
      h += '<div class="ba-meta">' + esc(deps, ctx.chartRecord.birthDate) + " \u00b7 " + esc(deps, ctx.chartRecord.birthTimeDisplay) + "</div>";
      h += '<div class="ba-place">' + esc(deps, (ctx.chartRecord.birthCity || "").split(",")[0].trim()) + "</div>";
    }
    h += "</div></td>";

    order.forEach(function (pid) {
      var name = typeof deps.comparisonCityDisplayName === "function"
        ? deps.comparisonCityDisplayName(pid, favs, nameById)
        : (nameById[pid] || pid);
      if (hidden.has(pid)) {
        var short = name.split(",")[0].trim().slice(0, 10) || name.slice(0, 10);
        h += '<td class="bar-stub"><button type="button" class="stub-restore" data-action="cmp-toggle-place" data-place-id="' + esc(deps, pid) + '">' + esc(deps, short) + "</button></td>";
        return;
      }
      var lines = splitCityNameLines(name);
      var tag = cityTagForPlace(ctx, pid);
      var tagHtml = tag
        ? '<div class="city-tag' + (tag === "Natal" ? " natal" : tag === "Current" ? " current" : "") + '">' + esc(deps, tag) + "</div>"
        : '<div class="city-tag-empty" aria-hidden="true"></div>';
      var vidx = visible.indexOf(pid);
      var isFirst = vidx === 0;
      var isLast = vidx === visible.length - 1;
      h += '<td class="bar-city city-card" data-cmp-role="city-card" data-place-id="' + esc(deps, pid) + '">';
      h += '<button type="button" class="city-remove" data-action="cmp-remove-place" data-place-id="' + esc(deps, pid) + '">\u00d7</button>';
      h += '<div class="city-badge-zone">' + tagHtml + "</div>";
      h += '<div class="city-name-zone"><span class="bnwrap city-name-lines">';
      h += '<span class="bname-line bname-line-primary">' + esc(deps, lines.line1) + "</span>";
      h += '<span class="bname-line bname-line-secondary">' + esc(deps, lines.line2) + "</span>";
      h += '<span class="city-name-inline-actions"><button type="button" class="city-info-inline" data-action="cmp-city-info" data-place-id="' + esc(deps, pid) + '">i</button></span>';
      h += "</span></div>";
      h += '<div class="city-coords">' + esc(deps, placeCoordsDisplay(deps, pid)) + "</div>";
      h += '<div class="city-ctrls">';
      h += '<button type="button" class="cc cc-arr" data-action="cmp-move-place" data-place-id="' + esc(deps, pid) + '" data-dir="-1"' + (isFirst ? " disabled" : "") + ">\u2039</button>";
      h += '<button type="button" class="cc" data-action="cmp-toggle-place" data-place-id="' + esc(deps, pid) + '">Hide</button>';
      h += '<button type="button" class="cc cc-rep" data-action="cmp-replace-place" data-place-id="' + esc(deps, pid) + '">Replace</button>';
      h += '<button type="button" class="cc cc-arr" data-action="cmp-move-place" data-place-id="' + esc(deps, pid) + '" data-dir="1"' + (isLast ? " disabled" : "") + ">\u203a</button>";
      h += "</div></td>";
    });

    if (canAdd) {
      h += '<td class="bar-add"><button type="button" class="add-city-btn" data-action="cmp-add-place">+\u2009Add</button></td>';
    }
    h += "</tr></tbody></table>";
    el.innerHTML = h;
  }

  function mapAisTable(root, ctx) {
    var el = mountEl(root, "ais-table");
    if (!el) return;
    var deps = ctx.deps || {};
    var placeIds = (ctx.comparisonSet && ctx.comparisonSet.placeIds) || [];
    var ws = ctx.workspaceState || {};
    var visibleIds = resolveVisibleOrderedPlaceIds(ws, placeIds);
    var visibleCols = visibleIds.map(function (pid) { return colByPlaceId(ctx.cols, pid); }).filter(Boolean);
    var labels = AIS_ANGLE_ROWS.map(function (r) { return r.label; });

    var diffsOn = !!(ws && ws.diffs_enabled);
    el.innerHTML = buildFactTable(labels, visibleCols, function (pid, rowIdx) {
      var col = colByPlaceId(ctx.cols, pid);
      var cc = canonicalFromCol(deps, col);
      var key = AIS_ANGLE_ROWS[rowIdx].key;
      var entry = cc && cc.angles ? cc.angles[key] : null;
      if (!entry || entry.longitude_deg == null) return null;
      if (typeof deps.aisFormatAngleDisplayHtml === "function") return deps.aisFormatAngleDisplayHtml(entry);
      return "\u2014";
    }, visibleIds, {
      rowKey: function (pid, rowIdx, col) {
        var cc = canonicalFromCol(deps, col);
        var key = AIS_ANGLE_ROWS[rowIdx].key;
        var entry = cc && cc.angles ? cc.angles[key] : null;
        if (deps.aisAngleDiffKey) return deps.aisAngleDiffKey(entry);
        return entry ? String(entry.longitude_deg) : "\u2014";
      },
      diffTdClass: function (cellKey, rowKeys) {
        return deps.cmpDiffTdClass ? deps.cmpDiffTdClass(cellKey, rowKeys, diffsOn) : "";
      },
    });
  }

  function mapPihTable(root, ctx) {
    var el = mountEl(root, "pih-table");
    if (!el) return;
    var deps = ctx.deps || {};
    var placeIds = (ctx.comparisonSet && ctx.comparisonSet.placeIds) || [];
    var ws = ctx.workspaceState || {};
    var visibleIds = resolveVisibleOrderedPlaceIds(ws, placeIds);
    var visibleCols = visibleIds.map(function (pid) { return colByPlaceId(ctx.cols, pid); }).filter(Boolean);
    // Mockup rhythm: fixed PIH row set (canonical planet house order + nodes).
    var labels = PIH_ROWS.slice();

    var diffsOn = !!(ws && ws.diffs_enabled);
    var dignitiesOn = !!(ws && ws.dignities_enabled);
    el.innerHTML = buildFactTable(labels, visibleCols, function (pid, rowIdx) {
      var col = colByPlaceId(ctx.cols, pid);
      if (!col || col.error) return null;
      var cc = canonicalFromCol(deps, col);
      var pn = labels[rowIdx];
      var info = (cc && cc.planets && cc.planets[pn]) || {};
      if (info.house == null) return '<span class="ph">&mdash;</span>';
      if (typeof deps.comparisonPihHouseValueHtml === "function") return deps.comparisonPihHouseValueHtml(pn, info);
      return ord(info.house);
    }, visibleIds, {
      labelHtml: function (label, rowIdx) {
        var refCol = visibleCols[0];
        var entry = {};
        if (refCol && typeof deps.planetEntryForMotionLookup === "function") {
          entry = deps.planetEntryForMotionLookup(visibleCols, label, refCol);
        } else if (refCol) {
          var cc0 = canonicalFromCol(deps, refCol);
          entry = (cc0 && cc0.planets && cc0.planets[label]) || {};
        }
        if (typeof deps.formatTablePlanetNameHtml === "function") {
          return deps.formatTablePlanetNameHtml(label, entry);
        }
        return esc(deps, label);
      },
      rowKey: function (pid, rowIdx, col) {
        var cc = canonicalFromCol(deps, col);
        var pn = labels[rowIdx];
        var info = (cc && cc.planets && cc.planets[pn]) || {};
        return deps.pihHouseDiffKey ? deps.pihHouseDiffKey(info) : String(info.house != null ? info.house : "\u2014");
      },
      diffTdClass: function (cellKey, rowKeys) {
        return deps.cmpDiffTdClass ? deps.cmpDiffTdClass(cellKey, rowKeys, diffsOn) : "";
      },
      extraTdClass: function (pid, rowIdx, col) {
        var base = " pih-house-cell";
        if (!dignitiesOn || !deps.pihDignityClass) return base;
        var cc = canonicalFromCol(deps, col);
        var pn = labels[rowIdx];
        var info = (cc && cc.planets && cc.planets[pn]) || {};
        if (info.house == null) return base;
        return base + (deps.pihDignityClass(pn, info.house) || "");
      },
    });
  }

  function buildA2aContactIndex(canonicalChart) {
    var idx = new Map();
    var raw = (canonicalChart && Array.isArray(canonicalChart.aspects_to_angles))
      ? canonicalChart.aspects_to_angles
      : [];
    raw.forEach(function (row) {
      if (!row || !row.planet || !row.angle) return;
      idx.set(String(row.planet) + "\0" + String(row.angle).toUpperCase(), row);
    });
    return idx;
  }

  function formatA2aCellHtml(deps, row) {
    if (!row || !row.aspect) return '<span class="ph">&mdash;</span>';
    var abbrMap = (deps && deps.PROFILE_A2A_ASP_ABBR) || A2A_ASP_ABBR;
    var abbr = abbrMap[String(row.aspect).toLowerCase()] || String(row.aspect);
    var motion = row.motion === "applying" ? " app" : row.motion === "separating" ? " sep" : "";
    var orb = typeof deps.formatA2aSeparationDeg === "function"
      ? deps.formatA2aSeparationDeg(row.separation_deg)
      : "\u2014";
    return '<span class="asp">' + esc(deps, abbr) + '</span> <span class="orb' + motion + '">' + esc(deps, orb) + "</span>";
  }

  function mapA2aTable(root, ctx) {
    var el = mountEl(root, "a2a-table");
    if (!el) return;
    var deps = ctx.deps || {};
    var ws = ctx.workspaceState || {};
    var angleKey = resolveActiveAngleKey(ws);
    var placeIds = (ctx.comparisonSet && ctx.comparisonSet.placeIds) || [];
    var visibleIds = resolveVisibleOrderedPlaceIds(ws, placeIds);
    var visibleCols = visibleIds.map(function (pid) { return colByPlaceId(ctx.cols, pid); }).filter(Boolean);

    var diffsOn = !!(ws && ws.diffs_enabled);
    el.innerHTML = buildFactTable(ATA_PLANETS, visibleCols, function (pid, rowIdx) {
      var col = colByPlaceId(ctx.cols, pid);
      var cc = canonicalFromCol(deps, col);
      if (!cc) return null;
      var idx = buildA2aContactIndex(cc);
      var planet = ATA_PLANETS[rowIdx];
      var hit = idx.get(planet + "\0" + angleKey) || idx.get(planet + "\0" + angleKey.toLowerCase());
      return formatA2aCellHtml(deps, hit);
    }, visibleIds, {
      rowKey: function (pid, rowIdx, col) {
        var cc = canonicalFromCol(deps, col);
        if (!cc) return "\u2014";
        var idx = buildA2aContactIndex(cc);
        var planet = ATA_PLANETS[rowIdx];
        var hit = idx.get(planet + "\0" + angleKey) || idx.get(planet + "\0" + angleKey.toLowerCase());
        return deps.a2aCellDiffKey ? deps.a2aCellDiffKey(hit) : (hit ? String(hit.aspect || "\u2014") : "\u2014");
      },
      diffTdClass: function (cellKey, rowKeys) {
        return deps.cmpDiffTdClass ? deps.cmpDiffTdClass(cellKey, rowKeys, diffsOn) : "";
      },
    });

    var pills = root.querySelector('[data-cmp-role="canonical-a2a-pills"]');
    if (pills) {
      pills.querySelectorAll("[data-angle]").forEach(function (btn) {
        btn.classList.toggle("active", btn.getAttribute("data-angle") === angleKey);
      });
    }
  }

  function mapNotes(root, ctx) {
    var el = mountEl(root, "notes-input") || (root && root.querySelector("#rm-cmp-note"));
    if (!el || !ctx.comparisonSet) return;
    el.value = ctx.comparisonSet.notes || "";
  }

  function mapCiSection(root, ctx) {
    var el = mountEl(root, "ci-cards");
    if (!el) return;
    var deps = ctx.deps || {};
    var placeIds = (ctx.comparisonSet && ctx.comparisonSet.placeIds) || [];
    var ws = ctx.workspaceState || {};
    var visibleIds = resolveVisibleOrderedPlaceIds(ws, placeIds);
    var nameById = (deps.viewModelPlaceNameById) || {};
    var favs = (ctx.chartRecord && ctx.chartRecord.favorites) || [];
    var rowsById = (deps.cityIntelligenceByPlaceId) || {};
    var placesById = (deps.placesById) || {};

    if (global.CityIntelligenceCanonical && CityIntelligenceCanonical.CANONICAL) {
      el.innerHTML = CityIntelligenceCanonical.renderComparisonInlineCardsHtml({
        placeIds: visibleIds,
        rowsById: rowsById,
        placesById: placesById,
        nameFor: function (pid) {
          var name = typeof deps.comparisonCityDisplayName === "function"
            ? deps.comparisonCityDisplayName(pid, favs, nameById)
            : (nameById[pid] || pid);
          var lines = splitCityNameLines(name);
          return lines.line1 + (lines.line2 ? ", " + lines.line2 : "");
        },
        coordsFor: function (pid) { return placeCoordsDisplay(deps, pid); },
      }, deps.escapeHtml);
      return;
    }

    var h = '<div class="ci-spacer"></div>';
    visibleIds.forEach(function (pid) {
      var name = typeof deps.comparisonCityDisplayName === "function"
        ? deps.comparisonCityDisplayName(pid, favs, nameById)
        : (nameById[pid] || pid);
      var lines = splitCityNameLines(name);
      h += '<div class="ci-card" data-place-id="' + esc(deps, pid) + '" data-cmp-role="ci-card">';
      h += '<div class="ci-name">' + esc(deps, lines.line1 + (lines.line2 ? ", " + lines.line2 : "")) + "</div>";
      h += '<div class="ci-coords">' + esc(deps, placeCoordsDisplay(deps, pid)) + "</div>";
      h += "<ul class=\"ci-list\">";
      CI_PLACEHOLDER_SNIPPETS.forEach(function (snippet, idx) {
        h += '<li data-ci-category="' + idx + '">' + esc(deps, snippet) + "</li>";
      });
      h += "</ul>";
      h += '<button type="button" class="ci-open-btn" data-action="cmp-ci-open-page" data-place-id="' + esc(deps, pid) + '">Open Full City Intelligence</button>';
      h += "</div>";
    });
    el.innerHTML = h;
  }

  function buildShadowShellHtml() {
    return (
      '<div id="rm-cmp-v5-shadow" data-cmp-v5-shadow="true" hidden aria-hidden="true" style="display:none">' +
        '<div data-cmp-mount="comparison-root" data-cmp-v5-shadow-root="true">' +
          '<div class="cmp-zone-b" data-cmp-mount="authority" data-cmp-role="authority-primary"></div>' +
          '<div data-cmp-mount="city-bar-inner"></div>' +
          '<div data-cmp-mount="ais-table"></div>' +
          '<div data-cmp-mount="pih-table"></div>' +
          '<div class="angle-tabs" data-cmp-role="canonical-a2a-pills">' +
            '<button type="button" class="angle-tab" data-angle="ASC">ASC</button>' +
            '<button type="button" class="angle-tab" data-angle="DSC">DSC</button>' +
            '<button type="button" class="angle-tab" data-angle="MC">MC</button>' +
            '<button type="button" class="angle-tab" data-angle="IC">IC</button>' +
          "</div>" +
          '<div data-cmp-mount="a2a-table"></div>' +
          '<div class="ci-section" data-cmp-mount="ci-section"><div class="ci-grid" data-cmp-mount="ci-cards"></div></div>' +
          '<textarea id="rm-cmp-note" data-cmp-mount="notes-input" data-cmp-role="notes-input"></textarea>' +
        "</div>" +
      "</div>"
    );
  }

  function hydrate(root, ctx) {
    if (!root || !ctx) return false;
    mapAuthority(root, ctx);
    mapCityBar(root, ctx);
    mapAisTable(root, ctx);
    mapPihTable(root, ctx);
    mapA2aTable(root, ctx);
    mapNotes(root, ctx);
    mapCiSection(root, ctx);
    root.setAttribute("data-cmp-v5-shadow-hydrated", "true");
    return true;
  }

  var ComparisonV5Adapter = {
    AIS_ANGLE_ROWS: AIS_ANGLE_ROWS,
    ATA_PLANETS: ATA_PLANETS,
    PIH_ROWS: PIH_ROWS,
    CMP_CAPACITY_RESERVED: CMP_CAPACITY_RESERVED,
    CI_CATEGORY_LABELS: CI_CATEGORY_LABELS,
    buildShadowShellHtml: buildShadowShellHtml,
    hydrate: hydrate,
    mapAuthority: mapAuthority,
    mapCityBar: mapCityBar,
    mapAisTable: mapAisTable,
    mapPihTable: mapPihTable,
    mapA2aTable: mapA2aTable,
    mapNotes: mapNotes,
    mapCiSection: mapCiSection,
  };

  global.ComparisonV5Adapter = ComparisonV5Adapter;
})(typeof window !== "undefined" ? window : globalThis);
