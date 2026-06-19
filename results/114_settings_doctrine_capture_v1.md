# Settings Doctrine Capture v1

**Status:** Authoritative product doctrine (capture only)  
**Date:** 2026-06-16  
**Type:** Doctrine / requirements capture — no implementation authorized by this document  
**Supersedes:** Informal placeholder copy in Settings UI; does not supersede W2-SETTINGS-1 navigation framework mechanics

---

## Purpose

Record authoritative Settings structure and content decisions for future Settings-2+ work. The current Settings implementation is acceptable as a **navigation framework only**. Most content described here is future work.

---

## Settings Structure

### Top-level sections (canonical order)

1. **Account**
2. **My Data**
3. **Astrology**
4. **Appearance**
5. **Notifications**
6. **Exports**
7. **About**
8. **User-Created Features** *(future)*

### Structural rules

- **Do not** use **Display** as a top-level category.
- **Appearance** is visual presentation.
- **Astrology** is chart logic and calculation/display defaults.
- Settings should become a **real product area**, not a dev/testing surface.

### Relation to current implementation (W2-SETTINGS-1)

Current nav uses `Display` and `Data` as interim section ids. Future work should migrate toward **Appearance** and **My Data** per this doctrine. Legacy aliases may persist during transition.

---

## Account

### Eventually contains

- Email
- Auth provider
- Subscription
- Security

### Content quality rules

- Current placeholder content is **not** product quality.
- **Remove** internal/testing language, including:
  - "Personal"
  - "Default profile map smoke"
- Copy must read as end-user account management, not QA or engineering notes.

---

## My Data

### Contains

- Profiles
- Saved Searches
- Saved Comparisons
- Archives
- History

### Actions (per entity where applicable)

- Rename
- Archive
- Delete
- Restore

### Placement rules

- **Manage Profiles belongs here** — not under Account.
- **Notes do not belong here.** Notes remain in their workflow surfaces (Chart Record, comparison workspace, etc.).

---

## Astrology

Section order (authoritative):

1. Additional Bodies
2. Aspects
3. Orbs
4. House System
5. Zodiac
6. Dignities
7. Advanced

### Core planets

- Core planets are **fixed** (not user-toggleable in this section).

### Additional Bodies

**Default on:**

- Chiron ✓

**Default off:**

- North Node □
- South Node □

**Advanced caret** (collapsed by default; expand for):

- Lilith
- Part of Fortune
- Future exotic bodies

**Remove:**

- "Future Bodies" as a labeled grouping or section title

**Remove:**

- Explanatory filler text that restates obvious UI behavior

---

## Aspects

### Major aspects

- Listed **individually** (not lumped as a single opaque control)

### Minor aspects

- Listed **individually**

### Missing aspect types (to add)

- Novile
- Septile

### Display columns (per aspect row)

Two independent toggles:

| Column | Meaning |
|--------|---------|
| □ Display on Chart | Wheel / relocated chart surfaces |
| □ Display in A2A / Search | Angle-to-angle and search-related surfaces |

---

## Orbs

### Parallel structure

Each aspect (or aspect family) supports **two** orb values where applicable:

- **Chart display orb**
- **A2A / Search orb**

### Late in House

**Toggle:** *Take late-house planets as subsequent house?*

| State | Orb control |
|-------|-------------|
| YES | Orb input **active** |
| NO | Orb input **disabled** |

**Default orb:** 2 degrees

### Out of Sign Aspects

- Single toggle (on/off)

---

## House System

- **Move above Dignities** in section order (see Astrology order above).

---

## Zodiac

- **Move above Dignities** in section order (see Astrology order above).

---

## Dignities

### Presets

- Ancient
- Modern
- Hybrid
- Custom

### Preset examples

| Preset | Example |
|--------|---------|
| Ancient | Jupiter rules Pisces |
| Modern | Neptune rules Pisces |
| Hybrid | Jupiter + Neptune co-rule Pisces |

### Custom mode

Repeatable rows:

| Field | |
|-------|---|
| Sign | |
| Planet | |
| Dignity Type | |

**Action:** Add Dignity

### Interpretive Hints

- **Beginner feature**
- **Default: OFF**

**Description (required when enabled or in help copy):**

> These are subjective interpretations intended to help decision-making and are not objective astrological facts.

---

## Appearance

### Contains (current / near-term)

**Glyph styles**, including variants for:

- Mars
- Capricorn
- Uranus
- Pluto

### Future

- Aspect band style
- Aspect band topology
- Theme options

### Scope boundary

- Regional formats, map presentation, and language may live here or in dedicated sub-panels under Appearance — but **not** under a top-level "Display" category.

---

## Notifications

### Do not include

- Comparison updates

### Future focus

- Road Trip Mode
- Airplane Mode
- Relocation change alerts

---

## Exports

### Contains

- **Branding opt-out** (Pro)
- **Templates**
- **Template Builder**

### Possible template sections

- Profiles
- Relocated Charts
- Comparison Tables
- Map Pages
- City Intelligence
- Share Links

### Export targets

- PDF
- Client package

---

## About

### Data Sources (attribution)

- Swiss Ephemeris
- GeoNames
- IANA Time Zone Database
- Leaflet / OpenStreetMap

Attribution belongs here — not repeated on map and chart surfaces.

---

## General Notes

| Topic | Doctrine |
|-------|----------|
| Current W2-SETTINGS-1 | Navigation framework only — acceptable interim |
| This document | Authoritative target for Settings-2 and later |
| Implementation | Not authorized by this capture; separate tickets required |
| Notes | Never a Settings section; never under My Data |
| Display | Retired as top-level name; use Appearance + Astrology split |
| Testing language | Must not ship in Account or any user-facing Settings copy |

---

## Acceptance (for future implementation tickets)

A future Settings pass is doctrine-aligned when:

1. Top-level nav matches **Account → My Data → Astrology → Appearance → Notifications → Exports → About** (+ future User-Created Features).
2. **Display** is not a top-level category.
3. Manage Profiles lives under **My Data** with rename/archive/delete/restore.
4. Astrology section order and Additional Bodies defaults match this document.
5. Aspects include Novile and Septile with dual display columns.
6. Orbs expose chart vs A2A/search orbs and Late-in-House behavior per doctrine.
7. House System and Zodiac appear above Dignities.
8. Dignities presets and Interpretive Hints match doctrine.
9. Notifications exclude comparison updates; future modes listed as backlog.
10. Exports structure matches branding/templates/builder doctrine.
11. Account and placeholder copy contain no internal/testing language.
