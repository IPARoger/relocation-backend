/*
  Genie variable builder — extracted from genie_SANDBOX_variable_builder.html.
  Mount via RelocationGenieVariableBuilder.mount(root, options).
*/
(function (global) {
  "use strict";
  "use strict";

  /**
   * AVAILABLE OBJECTS REGISTRY (Settings-owned vocabulary)
   * -------------------------------------------------------
   * Production: Settings enables/disables catalog entries; Genie consumes registry.list().
   * Sandbox: mock catalog below + debug-panel toggles simulate Settings.
   * Genie owns variables and field bindings — not astrological doctrine.
   */
  const OBJECT_CATALOG = Object.freeze({
    bodies: [
      { id: "sun", label: "Sun", group: "luminary", defaultEnabled: true },
      { id: "moon", label: "Moon", group: "luminary", defaultEnabled: true },
      { id: "mercury", label: "Mercury", group: "personal", defaultEnabled: true },
      { id: "venus", label: "Venus", group: "personal", defaultEnabled: true },
      { id: "mars", label: "Mars", group: "personal", defaultEnabled: true },
      { id: "jupiter", label: "Jupiter", group: "social", defaultEnabled: true },
      { id: "saturn", label: "Saturn", group: "social", defaultEnabled: true },
      { id: "uranus", label: "Uranus", group: "outer", defaultEnabled: true },
      { id: "neptune", label: "Neptune", group: "outer", defaultEnabled: true },
      { id: "pluto", label: "Pluto", group: "outer", defaultEnabled: true },
      { id: "chiron", label: "Chiron", group: "asteroid", defaultEnabled: true },
      { id: "north_node", label: "North Node", group: "node", defaultEnabled: false },
      { id: "south_node", label: "South Node", group: "node", defaultEnabled: false },
      { id: "lilith", label: "Lilith", group: "point", defaultEnabled: false },
      { id: "part_of_fortune", label: "Part of Fortune", group: "point", defaultEnabled: false },
      { id: "vertex", label: "Vertex", group: "point", defaultEnabled: false },
      { id: "east_point", label: "East Point", group: "point", defaultEnabled: false },
    ],
    angles: [
      { id: "ASC", label: "Ascendant (ASC)", defaultEnabled: true },
      { id: "DSC", label: "Descendant (DSC)", defaultEnabled: true },
      { id: "MC", label: "Midheaven (MC)", defaultEnabled: true },
      { id: "IC", label: "Imum Coeli (IC)", defaultEnabled: true },
    ],
    signs: [
      { id: "aries", label: "Aries", defaultEnabled: true },
      { id: "taurus", label: "Taurus", defaultEnabled: true },
      { id: "gemini", label: "Gemini", defaultEnabled: true },
      { id: "cancer", label: "Cancer", defaultEnabled: true },
      { id: "leo", label: "Leo", defaultEnabled: true },
      { id: "virgo", label: "Virgo", defaultEnabled: true },
      { id: "libra", label: "Libra", defaultEnabled: true },
      { id: "scorpio", label: "Scorpio", defaultEnabled: true },
      { id: "sagittarius", label: "Sagittarius", defaultEnabled: true },
      { id: "capricorn", label: "Capricorn", defaultEnabled: true },
      { id: "aquarius", label: "Aquarius", defaultEnabled: true },
      { id: "pisces", label: "Pisces", defaultEnabled: true },
    ],
    houses: Array.from({ length: 12 }, (_, i) => ({
      id: String(i + 1),
      label: String(i + 1),
      defaultEnabled: true,
    })),
    aspects: [
      { id: "conjunction", label: "Conjunction", tier: "major", defaultEnabled: true },
      { id: "opposition", label: "Opposition", tier: "major", defaultEnabled: true },
      { id: "square", label: "Square", tier: "major", defaultEnabled: true },
      { id: "trine", label: "Trine", tier: "major", defaultEnabled: true },
      { id: "sextile", label: "Sextile", tier: "major", defaultEnabled: true },
      { id: "hard", label: "All Hard Aspects", tier: "group", defaultEnabled: true },
      { id: "soft", label: "All Soft Aspects", tier: "group", defaultEnabled: true },
      { id: "any", label: "All Major Aspects", tier: "group", defaultEnabled: true },
      { id: "semisextile", label: "Semi-Sextile", tier: "minor", defaultEnabled: false },
      { id: "quincunx", label: "Quincunx", tier: "minor", defaultEnabled: false },
      { id: "semisquare", label: "Semi-Square", tier: "minor", defaultEnabled: false },
      { id: "sesquiquadrate", label: "Sesquiquadrate", tier: "minor", defaultEnabled: false },
    ],
    date_presets: [
      { id: "today", label: "Today", defaultEnabled: true },
      { id: "next_30", label: "Next 30 Days", defaultEnabled: true },
      { id: "next_365", label: "Next 365 Days", defaultEnabled: true },
      { id: "custom", label: "Custom", defaultEnabled: true },
    ],
  });

  /** Genie field bindings → registry categories (not doctrine). */
  const VARIABLE_FIELD_BINDINGS = Object.freeze({
    planet_in_house: [
      { field: "body", category: "bodies", label: "Body / Point" },
      { field: "house", category: "houses", label: "House" },
    ],
    angle_in_sign: [
      { field: "angle", category: "angles", label: "Angle" },
      { field: "sign", category: "signs", label: "Sign" },
    ],
    aspect_to_angle: [
      { field: "body", category: "bodies", label: "Body / Point" },
      { field: "aspect", category: "aspects", label: "Aspect" },
      { field: "angle", category: "angles", label: "Angle" },
    ],
    transit_through_house: [
      { field: "datePreset", category: "date_presets", label: "Date range" },
      { field: "transitBody", category: "bodies", label: "Body / Point" },
      { field: "house", category: "houses", label: "House" },
    ],
    transit_aspect_to_angle: [
      { field: "datePreset", category: "date_presets", label: "Date range" },
      { field: "transitBody", category: "bodies", label: "Body / Point" },
      { field: "aspect", category: "aspects", label: "Aspect" },
      { field: "angle", category: "angles", label: "Angle" },
    ],
  });

  function createAvailableObjectsRegistry(catalog) {
    /** @type {Record<string, Record<string, boolean>>} */
    const enabled = {};
    Object.keys(catalog).forEach((category) => {
      enabled[category] = {};
      catalog[category].forEach((item) => {
        enabled[category][item.id] = item.defaultEnabled !== false;
      });
    });

    return {
      catalog,
      list(category) {
        return (catalog[category] || []).filter((item) => enabled[category]?.[item.id]);
      },
      options(category) {
        return this.list(category).map((item) => [item.id, item.label]);
      },
      firstId(category) {
        const items = this.list(category);
        return items.length ? items[0].id : "";
      },
      isEnabled(category, id) {
        if (!id) return false;
        return Boolean(enabled[category]?.[id]);
      },
      setEnabled(category, id, on) {
        if (!(catalog[category] || []).some((item) => item.id === id)) return;
        enabled[category][id] = Boolean(on);
      },
      snapshot() {
        return JSON.parse(JSON.stringify(enabled));
      },
      togglableItems() {
        const out = {};
        Object.keys(catalog).forEach((category) => {
          out[category] = catalog[category].filter((item) => item.defaultEnabled === false);
        });
        return out;
      },
    };
  }

  const objectRegistry = createAvailableObjectsRegistry(OBJECT_CATALOG);
  window.__rmAvailableObjectsRegistry = objectRegistry;

  /** Presentation language — swappable; stable type ids unchanged (variable_card_language v1). */
  const CARD_LANGUAGE_REGISTRY = Object.freeze({
    separatorToken: "·",
    primaryAction: "Search Map",
    labels: Object.freeze({
      planet_in_house: "Planet · House",
      angle_in_sign: "Angle · Sign",
      aspect_to_angle: "Aspect · Angle",
      transit_through_house: "Transit · House",
      transit_aspect_to_angle: "Transit · Aspect · Angle",
      transit_group: "Relocated Transits (Experimental)",
    }),
    controls: Object.freeze({
      excludeLabel: "Exclude",
      excludeCompactLabel: "⊘",
      muteLabel: "Mute",
      soloLabel: "Solo",
    }),
  });

  function cardLanguageSnapshot() {
    return {
      separatorToken: CARD_LANGUAGE_REGISTRY.separatorToken,
      primaryAction: CARD_LANGUAGE_REGISTRY.primaryAction,
      labels: { ...CARD_LANGUAGE_REGISTRY.labels },
      controls: { ...CARD_LANGUAGE_REGISTRY.controls },
    };
  }

  function typeLabelFor(v) {
    return v.type ? (CARD_LANGUAGE_REGISTRY.labels[v.type] || "") : "";
  }

  const MAX_VARIABLES = 12;
  const VARIABLE_TYPES = [
    { id: "planet_in_house", transit: false },
    { id: "angle_in_sign", transit: false },
    { id: "aspect_to_angle", transit: false },
    { id: "transit_through_house", transit: true },
    { id: "transit_aspect_to_angle", transit: true },
  ].map((t) => ({
    ...t,
    label: CARD_LANGUAGE_REGISTRY.labels[t.id],
  }));

  const SANDBOX_CHART_RECORD_ID = "sandbox-chart-record";
  // activeChartRecordId() reads mountOptions.chartRecordId when mounted

  const TRANSIT_INFO_TEXT =
    "Experimental relocation-transit mode. " +
    "Many astrologers read transits to the natal chart only. " +
    "Transits to relocated houses or relocated angles are offered for research and experimentation, " +
    "not as the default interpretive model.";

  let nextId = 1;
  let genieOpen = true;
  let transitEnabled = false;
  let transitModalShowEnable = false;
  let clearUndoSnapshot = null;
  let clearUndoTimer = null;
  let lastNormalizedPayload = null;
  let renderCount = 0;

  /** @type {Array<object>} */
  let variables = [createEmptyVariable()];

  function createEmptyVariable() {
    return {
      id: `var-${nextId++}`,
      type: "",
      polarity: "include",
      fields: defaultFields(""),
      layer: { mute: false, solo: false },
    };
  }

  function defaultFields(type) {
    const base = {
      datePreset: objectRegistry.firstId("date_presets"),
      startDate: "",
      endDate: "",
      body: objectRegistry.firstId("bodies"),
      transitBody: objectRegistry.firstId("bodies"),
      house: objectRegistry.firstId("houses"),
      angle: objectRegistry.firstId("angles"),
      sign: objectRegistry.firstId("signs"),
      aspect: objectRegistry.firstId("aspects"),
    };
    if (!type) {
      return {
        datePreset: "",
        startDate: "",
        endDate: "",
        body: "",
        transitBody: "",
        house: "",
        angle: "",
        sign: "",
        aspect: "",
      };
    }
    const bindings = VARIABLE_FIELD_BINDINGS[type] || [];
    const out = { ...base };
    bindings.forEach(({ field, category }) => {
      out[field] = objectRegistry.firstId(category);
    });
    return out;
  }

  function bindingFor(type, field) {
    return (VARIABLE_FIELD_BINDINGS[type] || []).find((b) => b.field === field) || null;
  }

  function sanitizeVariableFields(v) {
    if (!v.type) return;
    (VARIABLE_FIELD_BINDINGS[v.type] || []).forEach(({ field, category }) => {
      if (!objectRegistry.isEnabled(category, v.fields[field])) {
        v.fields[field] = objectRegistry.firstId(category);
      }
    });
  }

  function sanitizeAllVariables() {
    variables.forEach(sanitizeVariableFields);
  }

  function isTransitType(type) {
    return type === "transit_through_house" || type === "transit_aspect_to_angle";
  }

  function resolveVariableStatus(v) {
    if (!v.type) return "incomplete";
    if (isTransitType(v.type) && !transitEnabled) return "disabled";
    if (!isVariableComplete(v)) return "incomplete";
    if (isTransitType(v.type) && transitEnabled) return "experimental";
    return "complete";
  }

  function resolveVariableEnabled(v) {
    return !(isTransitType(v.type) && !transitEnabled);
  }

  function buildVariableLabel(v) {
    if (!isVariableComplete(v)) return "";
    return typeLabelFor(v);
  }

  function canonicalFieldsForPayload(v) {
    const f = v.fields;
    if (v.type === "planet_in_house") {
      return { body: f.body, house: parseInt(f.house, 10) };
    }
    if (v.type === "angle_in_sign") {
      return { angle: f.angle, sign: f.sign };
    }
    if (v.type === "aspect_to_angle") {
      return { body: f.body, aspect: f.aspect, angle: f.angle };
    }
    if (v.type === "transit_through_house") {
      return {
        transitBody: f.transitBody,
        house: parseInt(f.house, 10),
        datePreset: f.datePreset,
        startDate: f.startDate || null,
        endDate: f.endDate || null,
        experimental: true,
      };
    }
    if (v.type === "transit_aspect_to_angle") {
      return {
        transitBody: f.transitBody,
        aspect: f.aspect,
        angle: f.angle,
        datePreset: f.datePreset,
        startDate: f.startDate || null,
        endDate: f.endDate || null,
        experimental: true,
      };
    }
    return { ...f };
  }

  function serializePayloadVariable(v) {
    return {
      id: v.id,
      type: v.type,
      polarity: v.polarity === "exclude" ? "exclude" : "include",
      enabled: resolveVariableEnabled(v),
      status: resolveVariableStatus(v),
      label: buildVariableLabel(v),
      fields: v.type ? canonicalFieldsForPayload(v) : { ...v.fields },
    };
  }

  function legacyBodyField(v) {
    const f = v.fields;
    if (v.type === "transit_through_house" || v.type === "transit_aspect_to_angle") {
      return f.transitBody;
    }
    return f.body;
  }

  function isVariableComplete(v) {
    if (!v.type) return false;
    if (isTransitType(v.type) && !transitEnabled) return false;
    const f = v.fields;
    const bindings = VARIABLE_FIELD_BINDINGS[v.type] || [];
    for (const { field, category } of bindings) {
      if (field === "datePreset") {
        if (!f.datePreset) return false;
        if (f.datePreset === "custom" && (!f.startDate || !f.endDate)) return false;
        continue;
      }
      if (!f[field] || !objectRegistry.isEnabled(category, f[field])) return false;
    }
    return bindings.length > 0;
  }

  function allVariablesComplete() {
    return variables.length > 0 && variables.every(isVariableComplete);
  }

  function anyIncomplete() {
    return variables.some((v) => !isVariableComplete(v));
  }

  function cardColor(kind) {
    const map = {
      planet_in_house: "#eab308",
      angle_in_sign: "#db2777",
      aspect_to_angle: "#2563eb",
      transit_through_house: "#94a3b8",
      transit_aspect_to_angle: "#94a3b8",
    };
    return map[kind] || "#cbd5e1";
  }

  function legacyNotExclusion(v) {
    const f = v.fields;
    const planet = legacyBodyField(v);
    const base = { type: v.type, variableId: v.id, polarity: "exclude" };
    if (v.type === "planet_in_house") {
      return { ...base, planet, house: parseInt(f.house, 10) };
    }
    if (v.type === "angle_in_sign") {
      return { ...base, angle: f.angle, sign: f.sign };
    }
    if (v.type === "aspect_to_angle") {
      return { ...base, planet, aspect: f.aspect, angle: f.angle };
    }
    if (v.type === "transit_through_house") {
      return { ...base, planet, house: parseInt(f.house, 10) };
    }
    if (v.type === "transit_aspect_to_angle") {
      return { ...base, planet, aspect: f.aspect, angle: f.angle };
    }
    return base;
  }

  function buildLegacyDegradation(includeHouses, includeAngles, includeAspects, includeTransits, payloadVariables) {
    const unmappedVariableIds = [];
    const warnings = [];

    includeHouses.slice(3).forEach((row) => {
      unmappedVariableIds.push(row.variableId);
      warnings.push(
        `planet_in_house ${row.variableId} (${row.planet} in ${row.house}${row.house === 1 ? "st" : row.house === 2 ? "nd" : row.house === 3 ? "rd" : "th"} house) exceeds legacy A/B/C capacity`,
      );
    });

    includeAngles.slice(1).forEach((row) => {
      unmappedVariableIds.push(row.variableId);
      warnings.push(
        `angle_in_sign ${row.variableId} (${row.angle} in ${row.sign}) exceeds legacy single angle_sign_conditions slot`,
      );
    });

    includeAspects.slice(1).forEach((row) => {
      unmappedVariableIds.push(row.variableId);
      warnings.push(
        `aspect_to_angle ${row.variableId} (${row.planet} ${row.aspect} ${row.angle}) exceeds legacy single aspect_overlay slot`,
      );
    });

    includeTransits.forEach((row) => {
      unmappedVariableIds.push(row.variableId);
      warnings.push(
        `${row.type} ${row.variableId} has no legacy positive slot (transit experimental)`,
      );
    });

    const canonicalVariableCount = payloadVariables.filter(
      (v) => v.status === "complete" || v.status === "experimental",
    ).length;
    const legacyMappedCount =
      Math.min(includeHouses.length, 3) +
      Math.min(includeAngles.length, 1) +
      Math.min(includeAspects.length, 1);

    return {
      canonicalVariableCount,
      legacyMappedCount,
      unmappedVariableIds,
      warnings,
    };
  }

  function buildLegacyCompatibility(
    includeHouses,
    includeAngles,
    includeAspects,
    notExclusions,
    includeTransits,
    payloadVariables,
  ) {
    const slotLabels = ["A", "B", "C"];
    const house_conditions = includeHouses.slice(0, 3).map((row, i) => ({
      slot: slotLabels[i],
      type: row.type,
      planet: row.planet,
      house: row.house,
      variableId: row.variableId,
    }));
    const angle_sign_conditions = includeAngles.slice(0, 1).map(({ type, angle, sign, variableId }) => ({
      type,
      angle,
      sign,
      variableId,
    }));
    const aspectSlice = includeAspects.slice(0, 1);
    const aspect_overlay = aspectSlice.length === 1
      ? { type: "aspect_to_angle", ...aspectSlice[0] }
      : null;
    return {
      schema_version: 1,
      kind: "saved_investigation",
      chart_id: activeChartRecordId(),
      house_conditions,
      angle_sign_conditions,
      aspect_overlay,
      aspect_overlays: includeAspects,
      notExclusions,
      degradation: buildLegacyDegradation(
        includeHouses,
        includeAngles,
        includeAspects,
        includeTransits,
        payloadVariables,
      ),
    };
  }

  function normalizePayload() {
    const includeHouses = [];
    const includeAngles = [];
    const includeAspects = [];
    const includeTransits = [];
    const notExclusions = [];
    const layerControls = {
      mutedVariableIds: [],
      soloVariableId: null,
      excludeVariableIds: [],
    };

    variables.forEach((v) => {
      if (!isVariableComplete(v)) return;
      if (v.layer.mute) layerControls.mutedVariableIds.push(v.id);
      if (v.layer.solo) layerControls.soloVariableId = v.id;
      if (v.polarity === "exclude") {
        layerControls.excludeVariableIds.push(v.id);
        notExclusions.push(legacyNotExclusion(v));
        return;
      }

      const f = v.fields;
      const planet = legacyBodyField(v);
      if (v.type === "planet_in_house") {
        includeHouses.push({
          variableId: v.id,
          type: "planet_in_house",
          planet,
          house: parseInt(f.house, 10),
        });
      } else if (v.type === "angle_in_sign") {
        includeAngles.push({
          variableId: v.id,
          type: "angle_in_sign",
          angle: f.angle,
          sign: f.sign,
        });
      } else if (v.type === "aspect_to_angle") {
        includeAspects.push({
          variableId: v.id,
          type: "aspect_to_angle",
          planet,
          aspect: f.aspect,
          angle: f.angle,
        });
      } else if (v.type === "transit_through_house" && transitEnabled) {
        includeTransits.push({
          variableId: v.id,
          type: "transit_through_house",
          planet,
          house: parseInt(f.house, 10),
        });
      } else if (v.type === "transit_aspect_to_angle" && transitEnabled) {
        includeTransits.push({
          variableId: v.id,
          type: "transit_aspect_to_angle",
          planet,
          aspect: f.aspect,
          angle: f.angle,
        });
      }
    });

    const payloadVariables = variables.map(serializePayloadVariable);

    return {
      schema_version: 1,
      kind: "genie_render",
      createdAt: new Date().toISOString(),
      chartRecordId: activeChartRecordId(),
      variables: payloadVariables,
      layerControls,
      settingsSnapshot: {
        transitModeEnabled: transitEnabled,
        registry: objectRegistry.snapshot(),
        cardLanguage: cardLanguageSnapshot(),
      },
      legacyCompatibility: buildLegacyCompatibility(
        includeHouses,
        includeAngles,
        includeAspects,
        notExclusions,
        includeTransits,
        payloadVariables,
      ),
    };
  }

  function cloneVariable(v) {
    return {
      id: v.id,
      type: v.type,
      polarity: v.polarity === "exclude" ? "exclude" : "include",
      fields: { ...v.fields },
      layer: { ...v.layer },
      complete: isVariableComplete(v),
      transit: isTransitType(v.type),
    };
  }

  function getState() {
    return {
      genieOpen,
      transitEnabled,
      mode: document.getElementById("explorationModeToggle").checked ? "exploration" : "configuration",
      variableCount: variables.length,
      maxVariables: MAX_VARIABLES,
      allComplete: allVariablesComplete(),
      variables: variables.map(cloneVariable),
      lastNormalizedPayload,
      renderCount,
      registry: objectRegistry.snapshot(),
    };
  }

  function selectOptionsFromPairs(pairs, selected, placeholder) {
    const ph = placeholder
      ? `<option value="" disabled${selected ? "" : " selected"}>${placeholder}</option>`
      : "";
    return ph + pairs.map(([val, label]) =>
      `<option value="${val}"${val === selected ? " selected" : ""}>${label}</option>`
    ).join("");
  }

  function registryFieldSelect(type, field, value, { disabled = false } = {}) {
    const binding = bindingFor(type, field);
    if (!binding) return "";
    const pairs = objectRegistry.options(binding.category);
    const label = binding.label;
    return `
      <div class="field">
        <label>${label}</label>
        <select data-field="${field}" ${disabled ? "disabled" : ""}>
          ${selectOptionsFromPairs(pairs, value)}
        </select>
      </div>`;
  }

  function typeSelectOptions(selected) {
    let html = `<option value="" disabled${selected ? "" : " selected"}>Select type…</option>`;
    const core = VARIABLE_TYPES.filter((t) => !t.transit);
    const transit = VARIABLE_TYPES.filter((t) => t.transit);
    core.forEach((t) => {
      const isSelected = t.id === selected;
      html += `<option value="${t.id}"${isSelected ? " selected" : ""}>${t.label}</option>`;
    });
    if (transit.length) {
      html += `<optgroup label="${CARD_LANGUAGE_REGISTRY.labels.transit_group}">`;
      transit.forEach((t) => {
        const isSelected = t.id === selected;
        const disabled = !transitEnabled;
        const suffix = transitEnabled ? " (experimental)" : " (off)";
        html += `<option value="${t.id}"${isSelected ? " selected" : ""}${disabled ? " disabled class=\"transit-option-disabled\"" : ""}>${t.label}${suffix}</option>`;
      });
      html += "</optgroup>";
    }
    return html;
  }

  function openTransitModal(showEnable) {
    transitModalShowEnable = showEnable && !transitEnabled;
    document.getElementById("transitModalBody").textContent = TRANSIT_INFO_TEXT;
    document.getElementById("transitModalEnableBtn").hidden = !transitModalShowEnable;
    document.getElementById("transitModalBackdrop").hidden = false;
  }

  function closeTransitModal() {
    document.getElementById("transitModalBackdrop").hidden = true;
  }

  function enableTransitVariables() {
    transitEnabled = true;
    document.getElementById("transitEnabledToggle").checked = true;
    closeTransitModal();
    render();
  }

  function disableTransitVariables() {
    variables.forEach((v) => {
      if (isTransitType(v.type)) {
        v.type = "";
        v.fields = defaultFields("");
      }
    });
    render();
  }

  function renderDateFields(v, disabled) {
    const f = v.fields;
    const custom = f.datePreset === "custom";
    return `
      <div class="field-row">
        ${registryFieldSelect(v.type, "datePreset", f.datePreset, { disabled })}
      </div>
      <div class="field-row">
        <div class="field">
          <label>Start date</label>
          <input type="date" data-field="startDate" value="${f.startDate || ""}"
            ${disabled || !custom ? "disabled" : ""} />
        </div>
        <div class="field">
          <label>End date</label>
          <input type="date" data-field="endDate" value="${f.endDate || ""}"
            ${disabled || !custom ? "disabled" : ""} />
        </div>
      </div>`;
  }

  function renderFieldsForType(v) {
    const f = v.fields;
    const transit = isTransitType(v.type);
    const fieldsDisabled = transit && !transitEnabled;
    if (!v.type) {
      return `<p style="margin:0;font-size:12px;color:#64748b">Choose a variable type to configure fields.</p>`;
    }
    const bindings = VARIABLE_FIELD_BINDINGS[v.type] || [];
    if (!bindings.length) return "";

    if (v.type === "planet_in_house") {
      return `
        <div class="field-row">
          ${registryFieldSelect(v.type, "body", f.body, { disabled: fieldsDisabled })}
          ${registryFieldSelect(v.type, "house", f.house, { disabled: fieldsDisabled })}
        </div>`;
    }
    if (v.type === "angle_in_sign") {
      return `
        <div class="field-row">
          ${registryFieldSelect(v.type, "angle", f.angle, { disabled: fieldsDisabled })}
          ${registryFieldSelect(v.type, "sign", f.sign, { disabled: fieldsDisabled })}
        </div>`;
    }
    if (v.type === "aspect_to_angle") {
      return `
        <div class="field-row">
          ${registryFieldSelect(v.type, "body", f.body, { disabled: fieldsDisabled })}
          ${registryFieldSelect(v.type, "aspect", f.aspect, { disabled: fieldsDisabled })}
        </div>
        <div class="field-row single">
          ${registryFieldSelect(v.type, "angle", f.angle, { disabled: fieldsDisabled })}
        </div>`;
    }
    if (v.type === "transit_through_house") {
      return `
        ${renderDateFields(v, fieldsDisabled)}
        <div class="field-row">
          ${registryFieldSelect(v.type, "transitBody", f.transitBody, { disabled: fieldsDisabled })}
          ${registryFieldSelect(v.type, "house", f.house, { disabled: fieldsDisabled })}
        </div>`;
    }
    if (v.type === "transit_aspect_to_angle") {
      return `
        ${renderDateFields(v, fieldsDisabled)}
        <div class="field-row">
          ${registryFieldSelect(v.type, "transitBody", f.transitBody, { disabled: fieldsDisabled })}
          ${registryFieldSelect(v.type, "aspect", f.aspect, { disabled: fieldsDisabled })}
        </div>
        <div class="field-row single">
          ${registryFieldSelect(v.type, "angle", f.angle, { disabled: fieldsDisabled })}
        </div>`;
    }
    return "";
  }

  function renderLayerToggles(v, index) {
    const color = cardColor(v.type);
    const ctl = CARD_LANGUAGE_REGISTRY.controls;
    const muteCls = v.layer.mute ? "active-mute" : "";
    const soloCls = v.layer.solo ? "active-solo" : "";
    const notCls = v.polarity === "exclude" ? "active-not" : "";
    return `
      <div class="layer-toggles">
        <label class="${muteCls}">
          <input type="checkbox" data-layer="mute" ${v.layer.mute ? "checked" : ""} /> ${ctl.muteLabel}
        </label>
        <label class="${soloCls}">
          <input type="checkbox" data-layer="solo" ${v.layer.solo ? "checked" : ""} /> ${ctl.soloLabel}
        </label>
        <label class="${notCls}">
          <input type="checkbox" data-layer="not" ${v.polarity === "exclude" ? "checked" : ""} /> ${ctl.excludeLabel}
        </label>
      </div>
      <div class="layer-toggles-compact" title="Exploration Mode scaffold">
        <span class="layer-dot" style="background:${color}" data-title="${ctl.muteLabel}"></span>
        <span class="layer-dot" style="background:${color};opacity:0.5" data-title="${ctl.soloLabel}"></span>
        <span class="layer-dot" style="background:${color};opacity:0.25" data-title="${ctl.excludeCompactLabel} ${ctl.excludeLabel}">${ctl.excludeCompactLabel}</span>
        <span style="font-size:9px;color:#64748b">Track ${String.fromCharCode(65 + index)}</span>
      </div>`;
  }

  function renderCards() {
    const root = document.getElementById("variableCards");
    root.innerHTML = variables.map((v, i) => {
      const complete = isVariableComplete(v);
      const transit = isTransitType(v.type);
      return `
        <article class="variable-card${complete ? "" : " incomplete"}${transit && transitEnabled ? " transit-type" : ""}"
          data-id="${v.id}" data-kind="${v.type || "unset"}">
          <div class="card-top">
            <span class="card-index">Variable ${i + 1}${complete ? "" : " · incomplete"}</span>
            <span>
              ${transit ? `<button type="button" class="card-transit-info" data-card-transit-info title="About transit variables">?</button>` : ""}
              <button type="button" class="card-remove" data-remove="${v.id}"
                ${variables.length <= 1 ? "disabled" : ""} title="Remove variable">×</button>
            </span>
          </div>
          <div class="field-row single">
            <div class="field">
              <div class="type-label-row">
                <label>Type</label>
                ${(!transitEnabled || transit) ? `<button type="button" class="card-transit-info" data-type-transit-info title="About transit variables">?</button>` : ""}
              </div>
              <select data-type-select>
                ${typeSelectOptions(v.type)}
              </select>
            </div>
          </div>
          ${renderFieldsForType(v)}
          ${v.type && (!transit || transitEnabled) ? renderLayerToggles(v, i) : ""}
        </article>`;
    }).join("");

    root.querySelectorAll("[data-type-select]").forEach((el, i) => {
      const prevType = variables[i].type;
      el.addEventListener("change", () => {
        const nextType = el.value;
        if (isTransitType(nextType) && !transitEnabled) {
          el.value = prevType || "";
          openTransitModal(true);
          return;
        }
        variables[i].type = nextType;
        variables[i].fields = defaultFields(nextType);
        syncSoloExclusive(variables[i]);
        render();
      });
    });

    root.querySelectorAll("[data-card-transit-info], [data-type-transit-info]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        openTransitModal(!transitEnabled);
      });
    });

    root.querySelectorAll("[data-field]").forEach((el) => {
      el.addEventListener("change", () => {
        const card = el.closest(".variable-card");
        const v = variables.find((x) => x.id === card.dataset.id);
        if (!v) return;
        v.fields[el.dataset.field] = el.value;
        render();
      });
    });

    root.querySelectorAll("[data-layer]").forEach((el) => {
      el.addEventListener("change", () => {
        const card = el.closest(".variable-card");
        const v = variables.find((x) => x.id === card.dataset.id);
        if (!v) return;
        const key = el.dataset.layer;
        if (key === "not") {
          v.polarity = el.checked ? "exclude" : "include";
        } else {
          v.layer[key] = el.checked;
        }
        if (key === "solo" && el.checked) {
          variables.forEach((other) => {
            if (other.id !== v.id) other.layer.solo = false;
          });
        }
        render();
      });
    });

    root.querySelectorAll("[data-remove]").forEach((btn) => {
      btn.addEventListener("click", () => {
        if (variables.length <= 1) return;
        variables = variables.filter((x) => x.id !== btn.dataset.remove);
        render();
      });
    });
  }

  function syncSoloExclusive(active) {
    if (active.layer.solo) {
      variables.forEach((v) => {
        if (v.id !== active.id) v.layer.solo = false;
      });
    }
  }

  function updateCornerControl() {
    const corner = document.getElementById("genieCorner");
    if (!corner) return;
    if (genieOpen) {
      corner.innerHTML = clearUndoSnapshot
        ? `<button type="button" class="clear-map-btn undo" id="clearMapBtn">Undo Clear</button>`
        : `<button type="button" class="clear-map-btn" id="clearMapBtn">Clear Map</button>`;
      document.getElementById("clearMapBtn").addEventListener("click", onClearMap);
    } else {
      corner.innerHTML = `<button type="button" class="genie-chip" id="openGenieChip" title="Open Genie">Genie</button>`;
      document.getElementById("openGenieChip").addEventListener("click", () => {
        genieOpen = true;
        render();
      });
    }
  }

  function onClearMap() {
    if (clearUndoSnapshot) {
      variables = clearUndoSnapshot.map((v) => ({
        ...v,
        polarity: v.polarity === "exclude" ? "exclude" : "include",
        fields: { ...v.fields },
        layer: { ...v.layer },
      }));
      clearUndoSnapshot = null;
      if (clearUndoTimer) clearTimeout(clearUndoTimer);
      clearUndoTimer = null;
      document.getElementById("renderStatus").textContent = "Undo Clear restored variables.";
      render();
      return;
    }
    clearUndoSnapshot = variables.map((v) => ({
      ...v,
      polarity: v.polarity === "exclude" ? "exclude" : "include",
      fields: { ...v.fields },
      layer: { ...v.layer },
    }));
    variables = [createEmptyVariable()];
    lastNormalizedPayload = null;
    document.getElementById("renderJson").textContent = "null";
    document.getElementById("renderStatus").textContent = "Map cleared — one empty variable. Undo available briefly.";
    if (clearUndoTimer) clearTimeout(clearUndoTimer);
    clearUndoTimer = setTimeout(() => {
      clearUndoSnapshot = null;
      updateCornerControl();
    }, 8000);
    render();
  }

  function updateActions() {
    const addBtn = document.getElementById("addVariableBtn");
    const renderBtn = document.getElementById("renderBtn");
    const atMax = variables.length >= MAX_VARIABLES;
    const canAdd = allVariablesComplete() && !atMax;
    addBtn.disabled = !canAdd;
    addBtn.style.display = atMax ? "none" : "";
    renderBtn.disabled = !allVariablesComplete();
    renderBtn.textContent = CARD_LANGUAGE_REGISTRY.primaryAction;
    if (atMax) {
      addBtn.title = "Maximum 12 variables";
    } else if (anyIncomplete()) {
      addBtn.title = "Complete all variables before adding another";
    } else {
      addBtn.title = "";
    }
  }

  function updateDebug() {
    document.getElementById("debugJson").textContent = JSON.stringify(
      {
        variables: variables.map(cloneVariable),
        genieOpen,
        transitEnabled,
        renderCount,
        registry: objectRegistry.snapshot(),
      },
      null,
      2
    );
  }

  function renderRegistrySettings() {
    const root = document.getElementById("registrySettingsBody");
    if (!root || root.hidden) return;
    const togglable = objectRegistry.togglableItems();
    const categoryLabels = {
      bodies: "Bodies & points",
      aspects: "Aspects",
      angles: "Angles",
      signs: "Signs",
      houses: "Houses",
      date_presets: "Date presets",
    };
    root.innerHTML = Object.entries(togglable)
      .filter(([, items]) => items.length > 0)
      .map(([category, items]) => `
        <div class="registry-group">
          <div class="registry-group-title">${categoryLabels[category] || category}</div>
          <div class="registry-toggles">
            ${items.map((item) => {
              const on = objectRegistry.isEnabled(category, item.id);
              return `<label class="${on ? "" : "is-off"}">
                <input type="checkbox" data-registry-category="${category}" data-registry-id="${item.id}"
                  ${on ? "checked" : ""} />
                ${item.label}
              </label>`;
            }).join("")}
          </div>
        </div>`).join("");

    root.querySelectorAll("[data-registry-category]").forEach((el) => {
      el.addEventListener("change", () => {
        objectRegistry.setEnabled(el.dataset.registryCategory, el.dataset.registryId, el.checked);
        sanitizeAllVariables();
        render();
      });
    });
  }

  function updateTransitHint() {
    const hint = document.getElementById("transitTypeHint");
    hint.classList.toggle("enabled", transitEnabled);
    hint.querySelector("span").textContent = transitEnabled
      ? "Experimental transit types available in type menu"
      : "Transit through house · Transiting aspect to angle (off by default)";
  }

  function render() {
    const panel = document.getElementById("geniePanel");
    const app = document.getElementById("app");
    const exploration = document.getElementById("explorationModeToggle").checked;
    panel.classList.toggle("collapsed", !genieOpen);
    if (app) app.classList.toggle("exploration-mode", exploration);
    const saveStub = document.getElementById("saveSearchStub");
    if (saveStub) saveStub.classList.toggle("hidden", !exploration);
    document.getElementById("transitEnabledToggle").checked = transitEnabled;
    updateTransitHint();
    renderRegistrySettings();
    renderCards();
    updateCornerControl();
    updateActions();
    updateDebug();
  }

  function buildMountHtml(options) {
    const externalDebug = Boolean(options && options.externalDebug);
    const debugStubs = externalDebug
      ? ""
      : `
    <pre id="debugJson" hidden aria-hidden="true"></pre>
    <pre id="renderJson" hidden aria-hidden="true"></pre>
    <div id="registrySettingsBody" hidden aria-hidden="true"></div>`;
    return `
    <div class="genie-panel" id="geniePanel" aria-label="Genie workbench">
      <header class="genie-header">
        <div class="genie-header-row">
          <div class="chart-record-line">
            <span id="genieChartRecordName"></span>
            <button type="button" class="info" title="Chart Record info">ⓘ</button>
          </div>
          <button type="button" class="genie-collapse" id="collapseGenie" title="Collapse Genie">×</button>
        </div>
        <div class="genie-sub">Configuration Mode · modular variables</div>
        <label class="mode-toggle">
          <input type="checkbox" id="explorationModeToggle" />
          Preview Exploration Mode (compact layer toggles)
        </label>
        <div class="transit-settings">
          <label class="transit-toggle">
            <input type="checkbox" id="transitEnabledToggle" />
            <span>Enable experimental transit variables</span>
          </label>
          <button type="button" class="transit-info-btn" id="transitInfoBtn" title="About transit variables">?</button>
        </div>
        <div class="transit-type-hint" id="transitTypeHint">
          <span>Transit through house · Transiting aspect to angle</span>
          <button type="button" class="transit-info-btn" id="transitHintInfoBtn" title="About transit variables">?</button>
        </div>
      </header>
      <div class="genie-body">
        <div class="variable-cards" id="variableCards"></div>
      </div>
      <footer class="genie-footer">
        <div class="action-row">
          <button type="button" id="addVariableBtn">Add Variable</button>
          <button type="button" class="primary" id="renderBtn">Search Map</button>
        </div>
        <div class="render-status" id="renderStatus">Configure at least one complete variable, then Render.</div>
      </footer>
    </div>
    <div class="transit-modal-backdrop" id="transitModalBackdrop" hidden>
      <div class="transit-modal" role="dialog" aria-labelledby="transitModalTitle" aria-modal="true">
        <h4 id="transitModalTitle">Experimental relocation-transit mode</h4>
        <p id="transitModalBody"></p>
        <div class="transit-modal-actions">
          <button type="button" class="primary" id="transitModalEnableBtn" hidden>Enable experimental transit variables</button>
          <button type="button" id="transitModalCloseBtn">Close</button>
        </div>
      </div>
    </div>${debugStubs}
  `;
  }

  /** @type {{ onSearchMap?: (payload: object) => void, onCollapse?: () => void, chartRecordId?: string, chartRecordName?: string, externalDebug?: boolean }} */
  let mountOptions = {};

  function activeChartRecordId() {
    return mountOptions.chartRecordId || SANDBOX_CHART_RECORD_ID;
  }

  function updateChartRecordLine() {
    const el = document.getElementById("genieChartRecordName");
    if (el) el.textContent = mountOptions.chartRecordName || activeChartRecordId();
  }

  function wireMountEvents() {
    document.getElementById("addVariableBtn").addEventListener("click", () => {
      if (!allVariablesComplete() || variables.length >= MAX_VARIABLES) return;
      variables.push(createEmptyVariable());
      render();
    });

    document.getElementById("renderBtn").addEventListener("click", () => {
      if (!allVariablesComplete()) return;
      lastNormalizedPayload = normalizePayload();
      renderCount += 1;
      const renderJson = document.getElementById("renderJson");
      if (renderJson) renderJson.textContent = JSON.stringify(lastNormalizedPayload, null, 2);
      if (typeof mountOptions.onSearchMap === "function") {
        mountOptions.onSearchMap(lastNormalizedPayload);
        document.getElementById("renderStatus").textContent =
          `Search Map #${renderCount} — handoff to map.`;
        console.info("[genie-builder] Search Map handoff:", lastNormalizedPayload);
        updateDebug();
        return;
      }
      document.getElementById("renderStatus").textContent =
        `Render #${renderCount} — ${lastNormalizedPayload.variables.filter((v) => v.status === "complete" || v.status === "experimental").length} variable(s). No backend call.`;
      console.info("[genie-sandbox] normalized render payload:", lastNormalizedPayload);
      updateDebug();
    });

    document.getElementById("collapseGenie").addEventListener("click", () => {
      if (typeof mountOptions.onCollapse === "function") {
        mountOptions.onCollapse();
        return;
      }
      genieOpen = false;
      render();
    });

    document.getElementById("explorationModeToggle").addEventListener("change", render);

    document.getElementById("transitEnabledToggle").addEventListener("change", (e) => {
      transitEnabled = e.target.checked;
      if (!transitEnabled) disableTransitVariables();
      else render();
    });

    document.getElementById("transitInfoBtn").addEventListener("click", () => openTransitModal(!transitEnabled));
    document.getElementById("transitHintInfoBtn").addEventListener("click", () => openTransitModal(!transitEnabled));
    document.getElementById("transitModalCloseBtn").addEventListener("click", closeTransitModal);
    document.getElementById("transitModalEnableBtn").addEventListener("click", enableTransitVariables);
    document.getElementById("transitModalBackdrop").addEventListener("click", (e) => {
      if (e.target.id === "transitModalBackdrop") closeTransitModal();
    });
    const modalBody = document.getElementById("transitModalBody");
    if (modalBody) modalBody.textContent = TRANSIT_INFO_TEXT;
  }

  function mountGenieVariableBuilder(root, options) {
    if (!root) throw new TypeError("root element required");
    mountOptions = options || {};
    root.classList.add("genie-drawer-mount");
    root.innerHTML = buildMountHtml(mountOptions);
    updateChartRecordLine();
    wireMountEvents();
    genieOpen = true;
    render();
    return {
      getState,
      normalizePayload,
      getRegistry: () => objectRegistry,
      getCardLanguageRegistry: () => cardLanguageSnapshot(),
    };
  }

  global.RelocationGenieVariableBuilder = {
    mount: mountGenieVariableBuilder,
    getState,
    normalizePayload,
    getCardLanguageRegistry: () => cardLanguageSnapshot(),
    CARD_LANGUAGE_REGISTRY,
    MAX_VARIABLES,
    TRANSIT_INFO_TEXT,
    VARIABLE_TYPES: VARIABLE_TYPES.map((t) => ({ ...t })),
    VARIABLE_FIELD_BINDINGS,
    isTransitType,
  };

  global.__rmGenieSandbox = global.RelocationGenieVariableBuilder;
})(typeof globalThis !== "undefined" ? globalThis : window);
