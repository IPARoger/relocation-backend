# 263 — Material System Delta (D1)

**Date:** 2026-06-26  
**Authority:** `docs/canon/MATERIAL_SYSTEM_CANON.md`  
**Scope:** Practical implementation work remaining after D1 material audit. No redesign proposals — parity and harmonization only.

---

## Summary

Beta chart surfaces (Profile, Relocated, Comparison V5, Notes) share a converging material language via `tband_foundation.css`, G3 card treatment, comparison hatch, and `notes_canonical.css`. **Map**, **Help**, and **production City Intelligence** remain outside the family. **D2** (tokens) and **Family Resemblance** final pass are the largest remaining workstreams.

---

## P0 — Structural identity gaps

| Item | Current state | Work |
|------|---------------|------|
| **Map workspace harmonization** | `map_CURRENT.html` / Genie lineage separate from beta chart family (`UI_STANDARDIZATION_CANON` §7 — stale) | Propagate stone/paper/ink, D2 dropdowns, title plate grammar, separator rules, Genie v6 choreography to production map without changing overlay math |
| **Family Resemblance final pass** | Explored in `family_resemblance_exploration_2_9a.md`; not closed | Cross-page audit: verify six rooms share DNA list in Material Canon §9; fix outliers |
| **D2 palette & material tokens** | `relocation_themes.css` has `--th-*`; no semantic `--material-*` layer | Tokenize stone/paper/glass/ink/shadow; wire Settings theme picker + all surfaces to one contract |

---

## P1 — Surface-level harmonization

| Item | Current state | Work |
|------|---------------|------|
| **Comparison G3 propagation** | Partially complete; some study variants diverge | Ensure live Comparison V5 matches `comparison_v5_beta` border/glow/hatch intensity |
| **Settings material alignment** | H6 layout polish; not full material pass | Apply paper panels, ink hierarchy, chrome recession consistently across all 7 sections |
| **Help handbook** | Not started (`UI_STANDARDIZATION_CANON` §1B) | Build on stone ground + paper handbook surfaces; same type roles as Settings |
| **City Intelligence production UI** | Canon CI-2; mockups aligned | When CI ships, use Paper reference blocks, species divider before CI, inline cell typography per canon |
| **Transported-material sign-off** | Beta-stabilized; not final aesthetic approval | Review aura/strip intensity on map against canon §2.5; no geometry changes |

---

## P2 — Chrome formalization

| Item | Current state | Work |
|------|---------------|------|
| **Button system (#7)** | Not formalized | Lock roles, states, primary/secondary/destructive per `control_and_action_doctrine_audit.md` |
| **Link system (#8)** | Partial | Chevron policy, underline rules, external link treatment site-wide |
| **Hover system (#9)** | Partial | Favorites row hover locked; extend consistently; no dark table rollovers |
| **Badge colorist pass** | De-pilled B1 direction; colors deferred | Apply status material family without emotional valence |
| **Spacing doctrine standalone** | ~80% applied; no single spec | Document Fibonacci rhythm as token doc companion to D2 |

---

## P3 — Texture & atmosphere

| Item | Current state | Work |
|------|---------------|------|
| **Material texture study → production** | `material_texture_study.html`, `distinct_texture_study.html` | Select at most one row weave for optional table separation; default remains lines-only |
| **Comparison hatch elsewhere** | Locked on comparison columns | If reused (e.g. favorites columns), same or lower intensity — never intensify |
| **Page ground atmosphere** | Warm gradients in studies | Apply stone tier consistently behind chart pages; avoid per-page bespoke backgrounds |
| **Wheel focal treatment** | Highest tier in doctrine | Audit that no card/table exceeds wheel atmosphere on chart-bearing pages |
| **Rain/virga overlay reveal** | Deferred (`UI_STANDARDIZATION_CANON` §5H) | Isolated study when scheduled; instant overlay until then |

---

## P4 — Reading comfort propagation

| Item | Current state | Work |
|------|---------------|------|
| **Notes canonical** | H7 complete | None for renderer — maintain single `NotesCanonical` |
| **Regional date/time** | localStorage wired H6-3; Profile Management list only | Propagate date format preference to other birth-date displays when safe (per H6 scope constraint) |
| **CI prose measure** | Doctrine defines length budgets | Enforce comfortable line length in Full City page when built |
| **Table fatigue** | Lines-only default locked | Resist zebra reintroduction; audit comparison marathon sessions |

---

## P5 — Map-specific (material only, no math)

| Item | Work |
|------|------|
| Genie DNA transfer | Name plate, dropdowns, chips from chart pages |
| Explore chrome dissolve | Glass floating controls; Share prominence |
| Popup typography | Match premium instrument tone per `INTERFACE_AND_DESIGN_CANON` |
| Sidebar/control density | Reduce debug-ship clutter; custom dropdown migration |
| Aura/material strip polish | Intensity from exactness fields only |

---

## Explicitly out of scope (D1)

- New color decoration or palette expansion beyond D2
- Comparison winner/loser coloring
- Notebook/skeuomorphic Notes treatments
- Animation entertainment or bounce easing
- City Intelligence user settings
- Astrology calculation or overlay semantics changes

---

## Suggested sequence

1. **D2 tokens** — unblock consistent implementation  
2. **Map harmonization pass** — largest visual outlier  
3. **Family Resemblance audit** — close cross-page gaps  
4. **Chrome formalization** (buttons, links, hover)  
5. **Help + CI** as those surfaces ship  
6. **Texture/atmosphere** propagation from studies  

---

## Revision log

| Date | Note |
|------|------|
| 2026-06-26 | D1 material delta — post canon audit |
