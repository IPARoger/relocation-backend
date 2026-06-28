# SETTINGS-V3-RESTART-3 Closeout — Charts Section

**Date:** 2026-06-29  
**Scope:** `#/settings-v3/charts` — Charts section from `prototype_settings_v2.html` with live S0 persistence  
**Legacy `#/settings`:** untouched  
**Status:** CHARTS-REPAIR-7 (PO feedback) — ready for PO QA — **not committed**

---

## Summary

Charts section in Settings V3: Bodies → Advanced Bodies → Orbs & Aspects → Advanced Orbs & Aspects → aspect toggles → Late-in-house alert → Zodiac → House System. Auto-persist on change (no Save button). My Profiles and My Data were not modified.

---

## Final behavior

### Bodies (main table)

| Row group | Default | Advanced Bodies closed | Advanced Bodies open |
|-----------|---------|------------------------|----------------------|
| Angles (ASC, MC, DSC, IC) | checked | locked | editable |
| Sun–Pluto | checked | locked | editable |
| Chiron | checked | **editable** | editable |
| North Node / South Node | unchecked | **editable** | editable |

Nodes sit above the Advanced Bodies disclosure and remain toggleable while Advanced Bodies is collapsed.

### Advanced Bodies

- Collapsed: `Show ▸`
- Expanded: `Hide ▾`
- Lilith, Vertex, Part of Fortune editable only when expanded

### Orbs & Aspects

- Column header: `Orb °` (degree sign in header only)
- Orb values: plain numbers (no trailing °)
- Major defaults: Conjunction 10, Opposition 10, Square 8, Trine 8, Sextile 6
- Minor defaults: Quincunx 3; all other minors 2
- Major aspects locked until **Advanced Orbs & Aspects** opens
- Minor aspects editable when Advanced Orbs & Aspects opens

### Aspect toggles

- **Show Out of Sign Aspects** — compact row, checkbox beside label, default OFF
- **Show Aspects to Angles** — compact row, checkbox beside label, default ON

### Other (unchanged)

- Late-in-house alert: enable checkbox + Orb ° (default 2°)
- Zodiac / House System: display-only; rule copy on change
- No Save button

---

## Persistence mapping

| V3 control | `user_settings` field | When saved |
|------------|----------------------|------------|
| Angles Tables / Chart | `helper_layers.table_angles`, `helper_layers.chart_angles` | Advanced Bodies open |
| Planets Tables / Chart | `visible_planets`, `helper_layers.chart_planets` | Advanced Bodies open |
| Chiron Tables / Chart | `visible_bodies`, `helper_layers.chart_bodies` | Advanced Bodies open |
| Node Tables | `visible_bodies` | **Always** (including Advanced Bodies closed) |
| Node Chart | `helper_layers.chart_bodies` | **Always** (including Advanced Bodies closed) |
| Lilith / Vertex / POF | `helper_layers.advanced_bodies`, `helper_layers.advanced_bodies_chart` | Advanced Bodies open |
| Major aspects / orbs | `visible_major_aspects`, `major_aspect_orbs`, `helper_layers.chart_major_aspects` | Advanced Orbs open (orbs read when unlocked) |
| Minor aspects / orbs | `visible_minor_aspects_list`, `minor_aspect_orbs`, `helper_layers.chart_minor_aspects` | Advanced Orbs open |
| Show Out of Sign Aspects | `out_of_sign_aspects` | Always |
| Show Aspects to Angles | `display_aspects_to_angles` | Always |
| Late-in-house | `house_proximity_orb_degrees` | Always |

**Not persisted:** zodiac, house system (display-only stubs).

---

## Files changed

| File | Role |
|------|------|
| `settings_v3/settings_v3.js` | Charts section markup, lock attributes, compact toggles |
| `settings_v3/settings_v3.css` | Table density, Orb ° header, compact toggle rows |
| `app_shell.html` | Hydrate/collect bridge, Advanced Bodies / Orbs lock sync |
| `results/SETTINGS_V3_RESTART_3_CLOSEOUT.md` | This document |

---

## PO QA checklist

### Route

- [ ] `#/settings-v3/charts` loads; nav highlights Charts
- [ ] No Save button

### Bodies — Advanced Bodies collapsed

- [ ] Angles + Sun–Pluto: checked, locked (grey, not clickable)
- [ ] Chiron: checked, **editable** (always clickable, Advanced Bodies open or closed)
- [ ] North Node + South Node: unchecked, **editable** (active checkbox, not grey)
- [ ] Toggle a node → reload → value retained
- [ ] Advanced Bodies button reads `Show ▸`

### Bodies — Advanced Bodies expanded

- [ ] Button reads `Hide ▾`
- [ ] All main-table rows editable: angles, Sun–Pluto, Chiron, nodes
- [ ] Lilith / Vertex / Part of Fortune editable in advanced panel
- [ ] Toggle a planet or Chiron → reload → retained

### Orbs

- [ ] Header shows `Orb °`; values are plain numbers (10, 8, 6 — no suffix)
- [ ] Major defaults: 10 / 10 / 8 / 8 / 6
- [ ] Advanced Orbs `Show ▸` / `Hide ▾`
- [ ] Minor defaults when expanded: Quincunx 3; others 2

### Aspect toggles

- [ ] Out of Sign Aspects: checkbox beside label, default OFF
- [ ] Aspects to Angles: checkbox beside label, default ON

### Regression

- [ ] `#/settings-v3` My Profiles unchanged
- [ ] `#/settings-v3/data` My Data unchanged
- [ ] Legacy `#/settings` Astrology unchanged

---

## How to test

```text
http://127.0.0.1:8000/auth.html   → sign in
http://127.0.0.1:8000/app_shell.html#/settings-v3/charts
```

Feature flag: `localStorage.relocation.flag.settingsV3 = "1"` (default on).

---


## REPAIR-7 (defaults + layout)

- Fixed empty-array bug: Mercury, IC, Sextile (and all core planets/angles/majors) default **checked** when settings lists are empty
- Checkboxes sit immediately right of label text (not far-right)
- Carets match prototype: closed Show \u25be, open Hide \u25b4
- Late-in-house: checkbox beside label; Orb ° label + plain number field grouped nearby
- Quincunx remains default unchecked

## Commit gate

Do **not** commit until PO checks all items above.
