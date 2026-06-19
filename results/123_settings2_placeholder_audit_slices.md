# SETTINGS-2: W2-SETTINGS-1 Placeholder Audit + Implementation Slices

**Date:** 2026-06-19  
**Type:** Audit + slices only — no implementation authorized  
**Sources:** `results/114_settings_doctrine_capture_v1.md`, `results/110_w2_settings_navigation_framework.md`, `app_shell.html` (SETTINGS_* renderers)

---

## Structural drift (framework vs doctrine 114)

| Topic | W2-SETTINGS-1 (current) | Doctrine 114 (target) | Slice |
|-------|-------------------------|----------------------|-------|
| Section id `display` | Top-level **Display** | **Appearance** (+ map/regional sub-panels) | SETTINGS-2A |
| Section id `data` | Top-level **Data** | **My Data** | SETTINGS-2A |
| Section order | Account, Astrology, Display, Notifications, Exports, Data, About | Account, **My Data**, Astrology, Appearance, Notifications, Exports, About, User-Created Features (future) | SETTINGS-2A |
| Manage Profiles | Under Account settings | **My Data** | SETTINGS-2B |
| Notes in Data panel | Personalization bullet mentions definitions | Notes **not** in My Data | SETTINGS-2B |

SETTINGS-2A is rename + route alias only (preserve `display`/`data` legacy hashes).

---

## Section-by-section placeholder audit

### Account

| Control | Current | Doctrine | Gap |
|---------|---------|----------|-----|
| Account name / role | Disabled inputs, drawer deferral | Email, auth provider, subscription, security | SETTINGS-3A Account identity |
| Default profile | **Live** (`rm-settings-default-cr`) | Belongs in My Data per 114 | Move in SETTINGS-2B |
| Copy | “Billing… coming soon” | Remove QA/internal tone | SETTINGS-3A copy pass |
| Testing language | None visible | Remove “smoke” etc. | ✅ |

### My Data (currently `data`)

| Stub | Current | Doctrine | Slice |
|------|---------|----------|-------|
| Saved searches | Stub | Saved Searches + rename/archive/delete | SETTINGS-4A (link to investigations module) |
| Favorites bulk | Stub | In My Data | SETTINGS-4B |
| Export my data | Stub | Account data export | SETTINGS-4C |
| History clear buttons | Disabled placeholders | History with restore | SETTINGS-4D |
| Technical / Debug | Duplicated under Data | Not in doctrine top-level — dev-only or About | SETTINGS-2C relocate |
| Personalization | Stub list | User-Created Features (future section) | SETTINGS-5+ |
| Manage Profiles button | Lives in Account | **Must live here** | SETTINGS-2B |

### Astrology (partially live)

| Area | Current | Doctrine | Slice |
|------|---------|----------|-------|
| Core planets | Live toggles | Fixed (not user-toggleable) | SETTINGS-3B — lock core bodies |
| Additional bodies | Live | Chiron on; nodes off; Advanced caret for Lilith/PoF | SETTINGS-3C bodies IA |
| Aspects | Live registry | Individual major + minor; add Novile, Septile; two columns (Chart vs A2A) | SETTINGS-3D aspects grid |
| Orbs | Live per-aspect | Chart orb + A2A orb columns; Late in House toggle; Out of Sign | SETTINGS-3E orbs |
| House system | Disabled Placidus | Move **above** Dignities | SETTINGS-2D reorder |
| Zodiac | Read-only Tropical | Move **above** Dignities | SETTINGS-2D reorder |
| Dignities preset | Disabled shell | Ancient/Modern/Hybrid/Custom + rows | SETTINGS-3F — **feeds `dignity_ontology.js` later** |
| Interpretive hints | Disabled preview | Beginner, default OFF, disclaimer copy | SETTINGS-3G (separate from PIH dignities display) |
| Chart appearance | Stub | Glyph styles under Appearance per 114 | SETTINGS-3H split |

### Appearance (currently under `display`)

| Stub | Doctrine | Slice |
|------|----------|-------|
| Color themes, glyph family, wheel, glyph variants | Appearance core | SETTINGS-3H |
| Language / regional | Appearance or sub-panel | SETTINGS-3I |
| Map aspect bands, city labels | Map presentation under Appearance / Map sub-panel | SETTINGS-3J |

### Notifications

| Stub | Doctrine | Gap |
|------|----------|-----|
| Comparison reminders | **Do not include** comparison updates | Remove stub in SETTINGS-2E |
| Email digests, product updates | Future: Road Trip, Airplane, relocation alerts | SETTINGS-4E |

### Exports

| Stub | Doctrine | Slice |
|------|----------|-------|
| Share link / PNG PDF | Branding opt-out (Pro), Templates, Template Builder | SETTINGS-4F |

### About

| Current | Doctrine | Slice |
|---------|----------|-------|
| Attribution live | Keep | ✅ maintain |

---

## Implementation slices (recommended)

| ID | Title | Scope | Depends |
|----|-------|-------|---------|
| **SETTINGS-2A** | Canonical section rename | `SETTINGS_SECTIONS` labels/ids: Appearance, My Data; reorder nav; legacy aliases | — |
| **SETTINGS-2B** | My Data owns profiles | Move default profile + Manage Profiles from Account; remove Notes mentions | 2A |
| **SETTINGS-2C** | Dev stubs quarantine | Move Debug/Cache to technical drawer or remove from user Data | 2A |
| **SETTINGS-2D** | Astrology section order | House System + Zodiac above Dignities in renderer | — |
| **SETTINGS-2E** | Notifications stub honesty | Remove comparison reminders; align copy to doctrine | — |
| **SETTINGS-3A** | Account copy + identity shell | Real labels; no internal language; subscription placeholder structure | 2A |
| **SETTINGS-3B** | Core planets locked | UI shows core list as fixed; additional bodies only toggleable | — |
| **SETTINGS-3C** | Additional bodies IA | Default states + Advanced caret | 3B |
| **SETTINGS-3D** | Aspect grid v2 | Per-aspect rows; Chart vs A2A columns; Novile/Septile | aspect registry |
| **SETTINGS-3E** | Dual orb columns + Late in House | Persisted keys in `user_settings` | 3D |
| **SETTINGS-3F** | Dignity presets editor | Wire preset → `dignity_ontology.js` data source | DIGNITIES-1 display ✅ |
| **SETTINGS-3G** | Interpretive hints toggle | Default OFF + disclaimer; workspace key exists | comparison WS |
| **SETTINGS-3H–J** | Appearance + map presentation | Themes, glyphs, map stubs → real controls | 2A |
| **SETTINGS-4A–F** | My Data + Exports modules | Deep links to investigations, favorites, export jobs | 2B |

---

## Persistence boundary (unchanged from W2-SETTINGS-1)

- **Live today:** Account default profile, Astrology bodies/aspects/orbs (existing save path)
- **New keys:** require `user_settings` schema design before SETTINGS-3D+ — do not stub-save

---

## Smokes per slice

| Slice | Smoke |
|-------|-------|
| 2A–2E | `smoke_settings_navigation.py` (update labels/order assertions) |
| 2B+ | `smoke_settings_account.py` (default profile still saves) |
| 3D+ | New `smoke_settings_astrology_persistence.py` (future) |

---

## Explicit non-goals (SETTINGS-2 capture)

- Implementing notification delivery, export engine, or theme engine
- Moving Notes Library into Settings
- PIH dignities display (completed in DIGNITIES-1 — separate from dignity **presets** here)
