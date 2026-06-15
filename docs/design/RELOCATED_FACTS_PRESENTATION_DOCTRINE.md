# RELOCATED FACTS PRESENTATION DOCTRINE

**Status:** Captured for future — documentation only (no code authorized)
**Type:** Design doctrine / coordination note
**Revision:** 2 — added required-consistency grammar
**Date:** 2026-06-15
**Phase:** Web2 Workflow QA

---

## 1. Purpose

Three different surfaces in the Web2 app now display the same underlying
object — **relocated chart facts** — but were wired independently during MVP
work. They are functional but visually/design-wise uncoordinated.

This note records the doctrine that these surfaces are views of *one* data
object and must eventually share a single coordinated presentation grammar.
The intent is that a future visual pass retrofits them together rather than
letting them drift further apart.

This is acceptable divergence for MVP wiring. It is documented here so it is
treated as deliberate, temporary, and coordinated later — not forgotten.

---

## 2. Surfaces included

1. **Map popup** — the compact preview shown when a city/point is opened on
   the map (`map_CURRENT.html`).
2. **Screen 4 / View Chart** — the standard relocated detail table
   (`app_shell.html`, Screen 4).
3. **Comparison page** — the multi-place comparison table
   (`app_shell.html`, Screen 5).

---

## 3. Shared underlying data object

All three surfaces present the same logical object: **relocated chart facts**
for a given birth record at a given destination location.

This object is sourced from the same backend contracts already in use:

- birth params via `/supabase/chart-records/{profile_id}/engine-birth`
- relocated facts via `/relocated-chart?lat=...&lon=...&...`

Core fields shared across surfaces:

- Angles: ASC, MC, DSC/DC, IC
- Planet-in-house rows
- Place name / coordinates context

Because the data object is the same, the labels, ordering, and formatting
should ultimately be the same too — only the *density* should differ.

---

## 4. Density ladder

The three surfaces are intentionally different densities of the same object.
The *content grammar* is shared; only the amount shown differs:

- **Map popup = brief.**
  Compact preview. A quick glance at the most important angles/placements for
  the opened point.
- **Screen 4 = complete.**
  The canonical, complete single-place relocated detail (all four angles plus
  the full planet-house list).
- **Comparison = scannable across columns.**
  The same rows as Screen 4, repeated across 2–5 places, optimized to scan a
  single fact horizontally across places.

The ladder runs: popup (brief) -> Screen 4 (complete) -> comparison (scannable
across columns). Each step must feel like the same grammar at a different
density, not three unrelated tables.

---

## 5. Required consistency

All three surfaces must agree on the following grammar. Where a surface is
briefer (popup), it shows a subset of the same rows in the same order and
format — it never renames, reorders, or reformats them.

### 5.1 Same row naming

One canonical label set is used everywhere. A row means the same thing and is
spelled the same way on every surface (e.g. "ASC", "MC", "DSC", "IC", and
"<Planet> house"). No surface invents its own synonyms or casing.

### 5.2 Same angle ordering (ASC / MC / DSC / IC)

The four angles always appear in this fixed order:

1. ASC
2. MC
3. DSC
4. IC

This ordering is identical on popup, Screen 4, and comparison. (DSC may be
labeled DSC/DC, but the label choice, once fixed, is the same everywhere.)

### 5.3 Same planet row ordering

Planet-in-house rows always appear in one fixed canonical order across all
surfaces:

Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto,
Chiron.

A briefer surface may show fewer planets, but never in a different order.

### 5.4 Same missing-value marker

A single shared marker represents an unresolved or missing fact on every
surface (the em dash "—"). Missing values are shown honestly with this marker;
no surface silently blanks, fabricates, or substitutes a different placeholder.

### 5.5 Same coordinate display doctrine

Coordinate (lat/lon) display follows one rule everywhere: coordinates are
available but secondary. They never dominate the relocated-facts grammar, are
formatted consistently (same precision/order), and appear in the same role on
each surface (place context, not a fact row).

### 5.6 Same badge doctrine (Natal / Current / Favorite)

When a place is a system or saved location, the same badge vocabulary is used
on every surface:

- **Natal Location**
- **Current Location**
- **Favorite**

Badges are visually distinct from one another and consistent across popup,
Screen 4, and comparison, per the Saved Places doctrine
(`docs/architecture/CURRENT_LOCATION_SAVED_PLACES_DOCTRINE.md`).

---

## 6. Coordination rule

**Any future change to one relocated-facts table family must check the other
two.**

If row labels, angle ordering, planet ordering, the missing-value marker,
coordinate display, or badges change on one surface, the change must be applied
to (or explicitly reconciled with) the other two. They are one family, not
three independent widgets.

---

## 7. Deferred (explicitly out of scope now)

- No CSS work now.
- No implementation of any kind.
- No renderer work.
- No chart wheel work.
- No notes work.
- No mobile design yet (mobile density per rung is deferred).

This note records intent and grammar only. Any visual/layout work requires a
separate, explicitly authorized task.

---

## Scope / Constraints

- This note records doctrine and grammar only.
- No code changes authorized by this entry.
- No schema changes authorized by this entry.
- Not part of any active implementation task.

## Acceptance / Next Step

- Awaiting explicit operator direction before any coordinated visual pass on
  the relocated-facts presentation family.
