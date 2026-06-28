/**
 * PR #23 collectSettingsV3Patch() — save wiring fragment (@ 23774db)
 * Merge into your existing collectSettingsV3Patch in app_shell.html.
 * Preserves your richer UI; only replaces save/read logic for bodies + orbs.
 */
function collectSettingsV3Patch() {
  /** @type {Record<string, unknown>} */
  const patch = {};
  const eff = _sv3Eff();
  const planetIds = SV3_MAIN_PLANETS.map(([id]) => id);
  const bodyIds = ["chiron", "north_node", "south_node"];
  const advBodyIds = SV3_ADVANCED_BODIES.map(([id]) => id);
  const anyAdvOpen = !!document.querySelector("#rm-sv3-advanced-bodies[open]")
    || !!document.querySelector("#rm-sv3-advanced-orbs[open]")
    || !!document.querySelector("#rm-sv3-advanced-calc-panel[open]");
  const collectTbl = (kind, ids) => ids.filter((id) => {
    const el = document.getElementById("rm-sv3-" + kind + "tbl-" + id);
    return el ? !!el.checked : false;
  });
  const collectCht = (kind, ids) => ids.filter((id) => {
    const el = document.getElementById("rm-sv3-" + kind + "cht-" + id);
    return el ? !!el.checked : false;
  });
  if (anyAdvOpen) {
    patch.visible_planets = collectTbl("planet", planetIds);
    patch.visible_bodies = collectTbl("body", bodyIds);
  } else {
    patch.visible_planets = (eff && Array.isArray(eff.visible_planets))
      ? eff.visible_planets.slice() : planetIds.slice();
    patch.visible_bodies = (eff && Array.isArray(eff.visible_bodies))
      ? eff.visible_bodies.slice() : ["chiron"];
  }
  const majorIds = SV3_MAJOR_ASPECTS.map(([id]) => id);
  const minorIds = SV3_MINOR_ASPECTS.map(([id]) => id);
  const orbsAdvOpen = !!document.querySelector("#rm-sv3-advanced-orbs[open]");
  if (orbsAdvOpen) {
    patch.visible_major_aspects = majorIds.filter((id) => {
      const el = document.getElementById("rm-sv3-majtbl-" + id);
      return el ? !!el.checked : false;
    });
    patch.visible_minor_aspects_list = minorIds.filter((id) => {
      const el = document.getElementById("rm-sv3-mintbl-" + id);
      return el ? !!el.checked : false;
    });
  } else {
    patch.visible_major_aspects = (eff && Array.isArray(eff.visible_major_aspects))
      ? eff.visible_major_aspects.slice() : majorIds.slice();
    patch.visible_minor_aspects_list = (eff && Array.isArray(eff.visible_minor_aspects_list))
      ? eff.visible_minor_aspects_list.slice() : [];
  }
  const minorMaster = document.getElementById("rm-sv3-minor-master");
  if (minorMaster) patch.visible_minor_aspects = !!minorMaster.checked;
  const collectOrbs = (kind, ids, allowDisabled) => {
    const out = {};
    ids.forEach((id) => {
      const el = document.getElementById("rm-sv3-" + kind + "orb-" + id);
      if (!el) return;
      if (!allowDisabled && el.disabled) return;
      const n = parseFloat(el.value);
      if (!isNaN(n)) out[id] = n;
    });
    return out;
  };
  let mo = collectOrbs("maj", majorIds, orbsAdvOpen);
  if (!Object.keys(mo).length) mo = Object.assign({}, (eff && eff.major_aspect_orbs) || {});
  if (Object.keys(mo).length) patch.major_aspect_orbs = mo;
  const mno = collectOrbs("min", minorIds, orbsAdvOpen);
  if (Object.keys(mno).length) patch.minor_aspect_orbs = mno;
  const oosEl = document.getElementById("rm-sv3-oos-aspects");
  if (oosEl) patch.out_of_sign_aspects = !!oosEl.checked;
  const lateOrbEl = document.getElementById("rm-sv3-late-orb");
  if (lateOrbEl && !lateOrbEl.disabled) {
    const n = parseFloat(lateOrbEl.value);
    if (!isNaN(n)) patch.house_proximity_orb_degrees = n;
  }
  const showA2aEl = document.getElementById("rm-sv3-show-a2a");
  const lateAlertEl = document.getElementById("rm-sv3-late-alert");
  const hl = Object.assign({}, (eff && eff.helper_layers) || {});
  if (showA2aEl) hl.show_aspects_to_angles = !!showA2aEl.checked;
  if (lateAlertEl) hl.show_late_in_house_alert = !!lateAlertEl.checked;
  if (anyAdvOpen) {
    hl.chart_planets = collectCht("planet", planetIds);
    hl.chart_bodies = collectCht("body", bodyIds);
    const advBodies = {};
    const advChart = {};
    advBodyIds.forEach((id) => {
      const tbl = document.getElementById("rm-sv3-advbodytbl-" + id);
      const cht = document.getElementById("rm-sv3-advbodycht-" + id);
      if (tbl && tbl.checked) advBodies[id] = true;
      if (cht && cht.checked) advChart[id] = true;
    });
    hl.advanced_bodies = advBodies;
    hl.advanced_bodies_chart = advChart;
  }
  if (orbsAdvOpen) {
    hl.chart_major_aspects = majorIds.filter((id) => {
      const el = document.getElementById("rm-sv3-majcht-" + id);
      return el ? !!el.checked : false;
    });
    hl.chart_minor_aspects = minorIds.filter((id) => {
      const el = document.getElementById("rm-sv3-mincht-" + id);
      return el ? !!el.checked : false;
    });
  } else {
    const effHl = (eff && eff.helper_layers) || {};
    hl.chart_major_aspects = Array.isArray(effHl.chart_major_aspects)
      ? effHl.chart_major_aspects.slice() : majorIds.slice();
    hl.chart_minor_aspects = Array.isArray(effHl.chart_minor_aspects)
      ? effHl.chart_minor_aspects.slice() : [];
  }
  patch.helper_layers = hl;
  if (showA2aEl) {
    const on = !!showA2aEl.checked;
    const prev = (eff && eff.display_aspects_to_angles) || { asc: true, mc: true, dsc: false, ic: false };
    patch.display_aspects_to_angles = on
      ? { asc: prev.asc !== false, mc: prev.mc !== false, dsc: !!prev.dsc, ic: !!prev.ic }
      : { asc: false, mc: false, dsc: false, ic: false };
  }
  return patch;
}
