/**
 * H8-1 — shared City Intelligence renderer (Relocated, Comparison, Full page).
 * Visual authority: city_profile_v4.html, comparison_v5_beta.html, relocated_standard.html
 * Safe to import from app_shell.html, comparison_v5_route.js, comparison_v5_adapter.js only.
 */
(function (global) {
  "use strict";

  const CI_CANONICAL = true;

  const CI_CATEGORY_LABELS = [
    "Regional context",
    "Safety",
    "Cost of living",
    "Professional / expat environment",
    "Climate",
    "Mobility / transit",
    "Regional character",
  ];

  const PHOTO_LABELS = {
    hero: "Cityscape",
    street: "Street Life",
    residential: "Residential",
    nature: "Nature",
    landmark: "Infrastructure",
  };

  const PHOTO_ORDER = ["hero", "street", "residential", "nature", "landmark"];

  function esc(text, escapeHtml) {
    return escapeHtml ? escapeHtml(text) : String(text == null ? "" : text);
  }

  function truncateWords(text, maxWords) {
    if (!text) return "\u2014";
    const words = String(text).trim().split(/\s+/).filter(Boolean);
    if (!words.length) return "\u2014";
    if (words.length <= maxWords) return words.join(" ");
    return words.slice(0, maxWords).join(" ") + "\u2026";
  }

  function firstPhrase(text, maxWords) {
    if (!text) return "\u2014";
    const chunk = String(text).split(/[.;]/)[0] || String(text);
    return truncateWords(chunk, maxWords);
  }

  function formatPopulation(place, row) {
    const pop = place && place.population;
    if (pop != null && Number.isFinite(Number(pop))) {
      const n = Number(pop);
      if (n >= 1_000_000) return "~" + (n / 1_000_000).toFixed(2).replace(/\.?0+$/, "") + "M";
      if (n >= 1_000) return "~" + Math.round(n / 1000) + "k";
      return String(n);
    }
    return firstPhrase(row && row.population, 6);
  }

  function locationContextFromRow(row) {
    const airports = (row && row.airport_json) || {};
    return airports.location_context || {};
  }

  function isRemoteLocation(row, place) {
    if (!row) return false;
    if (row.status === "custom") return true;
    const ctx = locationContextFromRow(row);
    return !!(ctx.is_remote || ctx.is_custom);
  }

  function placeDisplayName(place, row) {
    if (place && (place.display_name || place.canonical_name)) {
      return place.display_name || place.canonical_name;
    }
    const ctx = locationContextFromRow(row);
    return ctx.display_name || ctx.suggested_name || "Selected location";
  }

  function countryLabel(place, row) {
    if (place && place.country_name) return place.country_name;
    const ctx = locationContextFromRow(row);
    return ctx.country_name || "\u2014";
  }

  function coordsLabel(lat, lon, formatCoords) {
    if (typeof formatCoords === "function") return formatCoords(lat, lon);
    if (lat == null || lon == null || !Number.isFinite(Number(lat)) || !Number.isFinite(Number(lon))) {
      return "\u2014";
    }
    const la = Number(lat);
    const lo = Number(lon);
    const ns = la >= 0 ? "N" : "S";
    const ew = lo >= 0 ? "E" : "W";
    return Math.abs(la).toFixed(2) + "\u00b0 " + ns + ", " + Math.abs(lo).toFixed(2) + "\u00b0 " + ew;
  }

  function airportInline(row) {
    const airports = (row && row.airport_json) || {};
    const primary = airports.primary || {};
    const nearest = airports.nearest || {};
    if (primary.iata) return String(primary.iata);
    if (primary.name) return firstPhrase(primary.name, 4);
    if (nearest.name) return firstPhrase(nearest.name, 5);
    if (nearest.iata) return String(nearest.iata);
    return "\u2014";
  }

  function airportExpanded(row) {
    const airports = (row && row.airport_json) || {};
    const primary = airports.primary || {};
    const nearest = airports.nearest || {};
    const parts = [];
    if (primary.name) {
      let line = primary.name;
      if (primary.iata) line += " (" + primary.iata + ")";
      if (primary.distance_km != null) line += ", " + primary.distance_km + " km";
      parts.push(line);
    }
    if (nearest && nearest.name) {
      let line = nearest.name;
      if (nearest.distance_km != null) line += ", " + nearest.distance_km + " km";
      parts.push(line);
    }
    return parts.length ? parts.join("; ") : "\u2014";
  }

  function nearestSettlement(row) {
    const ctx = locationContextFromRow(row);
    return ctx.nearest_village || ctx.regional_context || "\u2014";
  }

  function regionalNoteHtml(isRemote, escapeHtml) {
    if (!isRemote) return "";
    return '<p class="ci-regional-note">' + esc("Regional context based on nearest settled community.", escapeHtml) + "</p>";
  }

  function inlineSnippetsFromRow(row, place) {
    const r = row || {};
    const country = countryLabel(place, r);
    const regional = country ? truncateWords(country + " context", 4) : firstPhrase(r.overview, 4);
    return [
      regional,
      firstPhrase(r.safety, 3),
      firstPhrase(r.cost, 4),
      firstPhrase(r.expat, 5),
      firstPhrase(r.climate, 3),
      firstPhrase(r.transport, 5),
      firstPhrase(r.culture, 5),
    ];
  }

  function modalSnippetsFromRow(row, place) {
    const base = inlineSnippetsFromRow(row, place);
    return CI_CATEGORY_LABELS.map(function (label, idx) {
      const val = base[idx] || "\u2014";
      return { label: label, value: val };
    });
  }

  function cityPageUrl(placeId) {
    return placeId ? "#/city?placeId=" + encodeURIComponent(placeId) : "#";
  }

  function renderIntelRowHtml(label, value, escapeHtml, opts) {
    const cfg = opts || {};
    const stub = !value || value === "\u2014";
    const valClass = stub && cfg.stubClass ? ' class="' + esc(cfg.stubClass, escapeHtml) + '"' : "";
    return '<div class="ir"><span class="il">' + esc(label, escapeHtml) + "</span>"
      + "<span class=\"iv\"" + valClass + ">" + esc(value || "\u2014", escapeHtml) + "</span></div>";
  }

  function renderRelocatedBlockHtml(config, escapeHtml) {
    const cfg = config || {};
    const row = cfg.row;
    const place = cfg.place || null;
    const lat = cfg.lat != null ? cfg.lat : (place && place.latitude);
    const lon = cfg.lon != null ? cfg.lon : (place && place.longitude);
    const remote = isRemoteLocation(row, place);
    const link = cityPageUrl(cfg.placeId);
    const rows = [];

    if (remote) {
      rows.push(renderIntelRowHtml("Summary", firstPhrase(row && row.overview, 12), escapeHtml));
      rows.push(renderIntelRowHtml("Country", countryLabel(place, row), escapeHtml));
      rows.push(renderIntelRowHtml("Coordinates", coordsLabel(lat, lon, cfg.formatCoords), escapeHtml));
      rows.push(renderIntelRowHtml("Nearest airport", airportInline(row), escapeHtml));
      rows.push(renderIntelRowHtml("Nearest settlement", nearestSettlement(row), escapeHtml));
    } else if (row) {
      rows.push(renderIntelRowHtml("Stability", firstPhrase(row.overview, 2), escapeHtml));
      rows.push(renderIntelRowHtml("Safety", firstPhrase(row.safety, 3), escapeHtml));
      rows.push(renderIntelRowHtml("Cost of Living", firstPhrase(row.cost, 3), escapeHtml));
      rows.push(renderIntelRowHtml("Expat Environment", firstPhrase(row.expat, 5), escapeHtml));
      rows.push(renderIntelRowHtml("Climate", firstPhrase(row.climate, 3), escapeHtml));
      rows.push(renderIntelRowHtml("Mobility", firstPhrase(row.transport, 4), escapeHtml));
      rows.push(renderIntelRowHtml("Population", formatPopulation(place, row), escapeHtml));
      rows.push(renderIntelRowHtml("Character", firstPhrase(row.culture, 5), escapeHtml));
    } else {
      ["Stability", "Safety", "Cost of Living", "Expat Environment", "Climate", "Mobility", "Population", "Character"].forEach(function (label) {
        rows.push(renderIntelRowHtml(label, "\u2014", escapeHtml, { stubClass: "intel-stub" }));
      });
    }

    const linkAttrs = cfg.placeId && row
      ? ' href="' + esc(link, escapeHtml) + '"'
      : ' href="#" aria-disabled="true" tabindex="-1" onclick="return false;"';

    return "<h4>Location Intelligence</h4>"
      + regionalNoteHtml(remote && row, escapeHtml)
      + '<div class="intel-rows">' + rows.join("") + "</div>"
      + '<a class="intel-link"' + linkAttrs + ">Open Full City Intelligence \u203a</a>";
  }

  function renderComparisonInlineCardsHtml(config, escapeHtml) {
    const cfg = config || {};
    const placeIds = cfg.placeIds || [];
    const rowsById = cfg.rowsById || {};
    const placesById = cfg.placesById || {};
    const nameFor = cfg.nameFor || function (pid) { return pid; };
    const coordsFor = cfg.coordsFor || function () { return "\u2014"; };
    let h = '<div class="ci-spacer"></div>';
    placeIds.forEach(function (pid) {
      const row = rowsById[pid];
      const place = placesById[pid] || null;
      const snippets = row ? inlineSnippetsFromRow(row, place) : CI_CATEGORY_LABELS.map(function () { return "\u2014"; });
      const name = nameFor(pid, place);
      h += '<div class="ci-card" data-place-id="' + esc(pid, escapeHtml) + '" data-cmp-role="ci-card">';
      h += '<div class="ci-name">' + esc(name, escapeHtml) + "</div>";
      h += '<div class="ci-coords">' + esc(coordsFor(pid, place), escapeHtml) + "</div>";
      h += '<ul class="ci-list">';
      snippets.forEach(function (snippet, idx) {
        h += '<li data-ci-category="' + idx + '">' + esc(snippet, escapeHtml) + "</li>";
      });
      h += "</ul>";
      h += '<button type="button" class="ci-open-btn" data-action="cmp-ci-open-page" data-place-id="' + esc(pid, escapeHtml) + '">Open Full City Intelligence</button>';
      h += "</div>";
    });
    return h;
  }

  function renderComparisonModalBodyHtml(config, escapeHtml) {
    const cfg = config || {};
    const row = cfg.row;
    const place = cfg.place || null;
    const items = row ? modalSnippetsFromRow(row, place) : CI_CATEGORY_LABELS.map(function (label) {
      return { label: label, value: "\u2014" };
    });
    return items.map(function (item, idx) {
      return '<li data-ci-category="' + idx + '"><b>' + esc(item.label + ": ", escapeHtml) + "</b>" + esc(item.value, escapeHtml) + "</li>";
    }).join("");
  }

  function renderAccordionRowHtml(label, shortVal, bodyHtml, escapeHtml) {
    return '<div class="acc-row">'
      + '<button class="acc-trigger" type="button"><span class="acc-label">' + esc(label, escapeHtml) + '</span>'
      + '<span class="acc-short">' + esc(shortVal || "\u2014", escapeHtml) + '</span><span class="acc-chevron">&#9656;</span></button>'
      + '<div class="acc-panel"><div class="acc-panel-inner">' + (bodyHtml || "") + "</div></div></div>";
  }

  function proseHtml(text, escapeHtml) {
    if (!text) return '<p class="meta">\u2014</p>';
    return "<p>" + esc(text, escapeHtml) + "</p>";
  }

  function renderPhotosStripHtml(row, escapeHtml) {
    const photos = (row && row.photos_json) || {};
    const blocks = PHOTO_ORDER.map(function (key) {
      const url = photos[key];
      const label = PHOTO_LABELS[key] || key;
      if (!url) return "";
      const style = ' style="background-image:url(' + esc(url, escapeHtml) + ');background-size:cover;background-position:center"';
      return '<div class="photo-block"' + style + '><span class="photo-label">' + esc(label, escapeHtml) + "</span></div>";
    }).filter(Boolean);
    if (!blocks.length) return "";
    return '<section class="photos" aria-label="Daily life imagery"><div class="photos-strip">' + blocks.join("") + "</div></section>";
  }

  function renderFullPageHtml(config, escapeHtml) {
    const cfg = config || {};
    const row = cfg.row;
    const place = cfg.place || null;
    const lat = cfg.lat != null ? cfg.lat : (place && place.latitude);
    const lon = cfg.lon != null ? cfg.lon : (place && place.longitude);
    const remote = isRemoteLocation(row, place);
    const title = placeDisplayName(place, row);
    const country = countryLabel(place, row);
    const heading = country && title.indexOf(country) < 0 ? title + ", " + country : title;

    const snapCost = firstPhrase(row && row.cost, 4);
    const snapSafety = firstPhrase(row && row.safety, 2);
    const snapStability = firstPhrase(row && row.overview, 1);
    const snapExpat = firstPhrase(row && row.expat, 1);
    const snapInfra = firstPhrase(row && row.transport, 2);
    const snapWeather = firstPhrase(row && row.climate, 2);
    const snapPop = formatPopulation(place, row);

    const remoteBlock = remote
      ? '<div class="remote-block ci-remote-facts" style="display:block">'
        + '<p class="summary-text">' + esc("Custom location — civic facts below describe the nearest settled community.", escapeHtml) + "</p>"
        + '<div class="intel-rows">'
        + renderIntelRowHtml("Country", country, escapeHtml)
        + renderIntelRowHtml("Coordinates", coordsLabel(lat, lon, cfg.formatCoords), escapeHtml)
        + renderIntelRowHtml("Nearest settlement", nearestSettlement(row), escapeHtml)
        + renderIntelRowHtml("Nearest airport", airportExpanded(row), escapeHtml)
        + "</div></div>"
      : "";

    const overviewRows = [
      renderAccordionRowHtml("Population", snapPop, proseHtml(row && row.population, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Cost", snapCost, proseHtml(row && row.cost, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Safety", snapSafety, proseHtml(row && row.safety, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Stability & Freedom", snapStability, proseHtml(row && row.overview, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Expat Community", snapExpat, proseHtml(row && row.expat, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Infrastructure", snapInfra, proseHtml(row && row.transport, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Language", firstPhrase(row && row.language, 3), proseHtml(row && row.language, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Weather", snapWeather, proseHtml(row && row.climate, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Healthcare", firstPhrase(row && row.healthcare, 3), proseHtml(row && row.healthcare, escapeHtml), escapeHtml),
    ].join("");

    const infraRows = [
      renderAccordionRowHtml("Transportation", firstPhrase(row && row.transport, 4), proseHtml(row && row.transport, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Internet & Mobile", firstPhrase(row && row.language, 3), proseHtml(row && row.language, escapeHtml), escapeHtml),
      renderAccordionRowHtml("International Airports", airportInline(row), "<p>" + esc(airportExpanded(row), escapeHtml) + "</p>", escapeHtml),
      renderAccordionRowHtml("Visa Information", "See below", proseHtml(row && row.visa, escapeHtml), escapeHtml),
      renderAccordionRowHtml("Taxes", "Residency-based", '<p class="meta">General residency thresholds apply at national level.</p>', escapeHtml),
    ].join("");

    const cultureRows = renderAccordionRowHtml("Culture", firstPhrase(row && row.culture, 3), proseHtml(row && row.culture, escapeHtml), escapeHtml);

    const closing = '<section class="section ci-closing"><p class="summary-text">'
      + esc("Figures summarize publicly available context for relocation planning. Verify visas, costs, and residency rules with official sources before committing.", escapeHtml)
      + "</p></section>";

    return '<div class="ci-page rm-ci-page" id="rm-ci-top" data-ci-place-id="' + esc(cfg.placeId || "", escapeHtml) + '">'
      + '<a class="back-link" href="#" data-action="ci-back">&#8592; Back</a>'
      + '<header class="hero">'
      + '<h1 class="city-title">' + esc(heading, escapeHtml) + "</h1>"
      + regionalNoteHtml(remote, escapeHtml)
      + '<div class="snapshot"><div class="snap-row snap-row-1">'
      + '<div class="snap-cell"><div class="snap-label">Monthly Cost</div><div class="snap-value">' + esc(snapCost, escapeHtml) + "</div></div>"
      + '<div class="snap-cell"><div class="snap-label">Safety</div><div class="snap-value">' + esc(snapSafety, escapeHtml) + "</div></div>"
      + '<div class="snap-cell"><div class="snap-label">Stability</div><div class="snap-value">' + esc(snapStability, escapeHtml) + "</div></div>"
      + '<div class="snap-cell"><div class="snap-label">Expat Community</div><div class="snap-value">' + esc(snapExpat, escapeHtml) + "</div></div>"
      + "</div><div class=\"snap-row snap-row-2\">"
      + '<div class="snap-cell"><div class="snap-label">Infrastructure</div><div class="snap-value">' + esc(snapInfra, escapeHtml) + "</div></div>"
      + '<div class="snap-cell"><div class="snap-label">Weather</div><div class="snap-value">' + esc(snapWeather, escapeHtml) + "</div></div>"
      + '<div class="snap-cell snap-cell-pop"><div class="snap-label">Population</div><div class="snap-value">' + esc(snapPop, escapeHtml) + "</div></div>"
      + "</div></div></header>"
      + remoteBlock
      + renderPhotosStripHtml(row, escapeHtml)
      + '<section class="section" id="overview"><h2 class="section-title">Overview</h2>'
      + '<p class="summary-text">' + esc(firstPhrase(row && row.overview, 25), escapeHtml) + "</p>"
      + '<div class="accordions">' + overviewRows + "</div></section>"
      + '<section class="section" id="infrastructure"><h2 class="section-title">Infrastructure &amp; Logistics</h2><div class="accordions">' + infraRows + "</div></section>"
      + '<section class="visa-block" id="visa"><h2 class="visa-heading">Visa Information</h2>'
      + '<p class="visa-summary">' + esc(firstPhrase(row && row.visa, 20), escapeHtml) + "</p></section>"
      + '<section class="section" id="culture"><h2 class="section-title">Culture</h2><div class="accordions">' + cultureRows + "</div></section>"
      + closing
      + '<a class="back-to-top" href="#rm-ci-top">&uarr; Back to Top</a></div>';
  }

  function renderComparisonModalShellHtml() {
    return '<div class="modal-overlay" id="modal-cityinfo" data-cmp-mount="city-info-modal" data-modal="cityinfo" data-action="cmp-modal-backdrop">'
      + '<div class="modal-box"><div class="modal-title" id="modal-ci-title"></div>'
      + '<ul class="ci-modal-list" id="modal-ci-list"></ul>'
      + '<div class="modal-actions"><button type="button" class="modal-btn" data-action="cmp-modal-close" data-modal="cityinfo">Close</button></div>'
      + "</div></div>";
  }

  global.CityIntelligenceCanonical = {
    CANONICAL: CI_CANONICAL,
    CI_CATEGORY_LABELS: CI_CATEGORY_LABELS,
    PHOTO_LABELS: PHOTO_LABELS,
    truncateWords: truncateWords,
    firstPhrase: firstPhrase,
    inlineSnippetsFromRow: inlineSnippetsFromRow,
    modalSnippetsFromRow: modalSnippetsFromRow,
    isRemoteLocation: isRemoteLocation,
    placeDisplayName: placeDisplayName,
    countryLabel: countryLabel,
    coordsLabel: coordsLabel,
    airportInline: airportInline,
    nearestSettlement: nearestSettlement,
    cityPageUrl: cityPageUrl,
    renderRelocatedBlockHtml: renderRelocatedBlockHtml,
    renderComparisonInlineCardsHtml: renderComparisonInlineCardsHtml,
    renderComparisonModalBodyHtml: renderComparisonModalBodyHtml,
    renderComparisonModalShellHtml: renderComparisonModalShellHtml,
    renderFullPageHtml: renderFullPageHtml,
  };
})(typeof window !== "undefined" ? window : globalThis);
