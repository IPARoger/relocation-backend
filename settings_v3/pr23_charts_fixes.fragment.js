/**
 * SETTINGS V3 — PR #23 charts fixes (reference fragment)
 * Source: cursor/settings-v3-4b-charts-4b87 @ 23774db
 *
 * DO NOT load this file as a replacement for your richer Settings V3 UI.
 * Merge these behaviors into your existing settings-v3 functions in app_shell.html:
 *
 *   1. Bodies: Tables|Chart columns; Chiron + North + South Node above Advanced Bodies
 *   2. Orbs: HTML <table class="rm-sv3-oa-table"> — Name | Tables | Chart | Orb
 *   3. applySettingsV3AdvancedState: any Advanced open → unlock all body checkboxes
 *   4. collectSettingsV3Patch: tbl/cht collectors + anyAdvOpen save gate
 *
 * See results/SETTINGS_V3_PORT_GUIDE.md for grep-based merge steps on your Mac.
 */
/* eslint-disable no-unused-vars */

// ── Constants (merge into your existing SV3_* block) ─────────────────────
const SV3_ABOVE_FOLD_BODIES = [
  ["chiron", "Chiron", true],
  ["north_node", "North Node", false],
  ["south_node", "South Node", false],
];
const SV3_ADVANCED_BODIES = [
  ["lilith", "Lilith"],
  ["true_node", "True Node"],
  ["vertex", "Vertex"],
  ["part_of_fortune", "Part of Fortune"],
];

// ── Bodies row builder (Tables | Chart, locked until Advanced) ───────────
function sv3BodiesHeadHtml() {
  return `<thead><tr><th>Name</th><th class="rm-sv3-bodies-tbl">Tables</th><th class="rm-sv3-bodies-cht">Chart</th></tr></thead>`;
}

function sv3BodyRow(id, label, tblOn, chtOn, kind) {
  const lockAttr = ' disabled aria-disabled="true" data-sv3-advanced-lock="1"';
  return `<tr class="is-locked">
    <td>${escapeHtml(label)}</td>
    <td class="rm-sv3-bodies-tbl"><input type="checkbox" id="rm-sv3-${kind}tbl-${id}"${tblOn ? " checked" : ""}${lockAttr} /></td>
    <td class="rm-sv3-bodies-cht"><input type="checkbox" id="rm-sv3-${kind}cht-${id}"${chtOn ? " checked" : ""}${lockAttr} /></td>
  </tr>`;
}

// ── Orbs table header + row (NOT css grid / display:contents) ────────────
function sv3OaHeadHtml() {
  return `<thead><tr>
    <th class="rm-sv3-oa-name-h"></th>
    <th class="rm-sv3-oa-tbl rm-sv3-oa-h-tables">Tables</th>
    <th class="rm-sv3-oa-cht rm-sv3-oa-h-chart">Chart</th>
    <th class="rm-sv3-oa-orb rm-sv3-oa-h-orb">Orb</th>
  </tr></thead>`;
}

function sv3AspectRow(kind, id, label, orbVal, tblOn, chtOn, opts) {
  const o = opts || {};
  const isMajor = kind === "maj";
  const lockMajor = isMajor && o.lockMajor !== false;
  const lockAttr = lockMajor ? ' disabled aria-disabled="true" data-sv3-major-lock="1"' : "";
  const lockCls = lockMajor ? " is-locked" : "";
  const orbDis = (isMajor && lockMajor) || o.orbDisabled
    ? ' disabled aria-disabled="true"' + (isMajor ? ' data-sv3-major-lock="1"' : "") : "";
  return `<tr class="rm-sv3-oa-row${lockCls}" data-sv3-aspect-row="${kind}-${id}">
    <td class="rm-sv3-oa-label">${escapeHtml(label)}</td>
    <td class="rm-sv3-oa-tbl"><input type="checkbox" id="rm-sv3-${kind}tbl-${id}"${tblOn ? " checked" : ""}${lockAttr} /></td>
    <td class="rm-sv3-oa-cht"><input type="checkbox" id="rm-sv3-${kind}cht-${id}"${chtOn ? " checked" : ""}${lockAttr} /></td>
    <td class="rm-sv3-oa-orb"><input type="number" id="rm-sv3-${kind}orb-${id}" min="0" max="15" step="0.5" value="${orbVal}"${orbDis} /></td>
  </tr>`;
}

// ── Advanced unlock (any Advanced section → all body locks off) ──────────
function applySettingsV3AdvancedState(root) {
  const scope = root || document;
  const bodiesOpen = !!scope.querySelector("#rm-sv3-advanced-bodies[open]");
  const orbsOpen = !!scope.querySelector("#rm-sv3-advanced-orbs[open]");
  const calcOpen = !!scope.querySelector("#rm-sv3-advanced-calc-panel[open]");
  const anyOpen = bodiesOpen || orbsOpen || calcOpen;
  const sv3Root = scope.querySelector("#rm-sv3-root");
  if (sv3Root) sv3Root.classList.toggle("rm-sv3-advanced-open", anyOpen);
  scope.querySelectorAll("[data-sv3-advanced-lock]").forEach((el) => {
    if (anyOpen) { el.removeAttribute("disabled"); el.removeAttribute("aria-disabled"); }
    else { el.setAttribute("disabled", "disabled"); el.setAttribute("aria-disabled", "true"); }
  });
  scope.querySelectorAll("#rm-sv3-bodies tr.is-locked").forEach((row) => {
    row.classList.toggle("is-locked", !anyOpen);
  });
  scope.querySelectorAll("[data-sv3-major-lock]").forEach((el) => {
    if (orbsOpen) { el.removeAttribute("disabled"); el.removeAttribute("aria-disabled"); }
    else { el.setAttribute("disabled", "disabled"); el.setAttribute("aria-disabled", "true"); }
  });
  scope.querySelectorAll(".rm-sv3-oa-row[data-sv3-aspect-row^='maj-']").forEach((row) => {
    row.classList.toggle("is-locked", !orbsOpen);
  });
}

// ── Save collector (tbl/cht + anyAdvOpen) — merge into collectSettingsV3Patch
// Full implementation: see settings_v3/pr23_collect_patch.fragment.js or PR #23 app_shell.html
