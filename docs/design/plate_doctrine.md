# Plate Doctrine

Status: provisional doctrine (Phase 2.8C)
Source: Phase 2.8B Plate Doctrine Audit
Scope: product-wide identity/context blocks ("plates")

This is a decision document, not a raw audit. Future implementation should
follow it. It deliberately does **not** decide final colors, fonts, animation,
badge styling, or metadata styling — those belong to later doctrines.

---

## 1. Definition

A **plate** is the identity/context block that tells the user **what object they
are looking at** and **through what authority/lens** they are looking at it.

A plate answers two questions at once:

- **Subject** — what is this page/region about?
- **Authority** — through whose/what lens is the subject being interpreted?

A plate is not a table, not a card grid, not a wheel. It is the orienting header
that frames everything below it.

---

## 2. Core Rule

**Subject and authority are not always the same.**

The plate must always make both legible, even when they differ.

| Surface | Subject | Authority |
|---|---|---|
| Profile page | person | profile |
| Relocated Location page | location | profile |
| Comparison page | comparison set / locations | profile + comparison set |
| Map popup | clicked point | active profile **only if** chart data is shown |
| City Intelligence | place | place / intelligence dataset |

Corollary: when the subject is *not* the profile (e.g. a location), the plate
must still surface the governing profile (e.g. "For {profile}") so the user
never loses the lens.

---

## 3. Approved Plate Families

Nine approved families. Each entry defines intended use, subject, authority,
required/optional/forbidden fields, and allowed placement zones.

### 3.1 Full Profile Plate

- **Intended use:** primary identity block on chart-bearing Profile views.
- **Subject:** person / natal chart.
- **Authority:** profile.
- **Required fields:** profile name; birth date/time; birth place; lat/lon;
  UTC/offset; zodiac (Tropical); house system (Placidus).
- **Optional fields:** edit/add profile controls; current-location addendum block.
- **Forbidden fields:** city intelligence facts; comparison facts; notes owned by
  table sections.
- **Allowed placement:** beside wheel; above wheel.

### 3.2 Compact Profile Plate

- **Intended use:** space-constrained chart context (e.g. side-by-side guest
  charts, current-location chart).
- **Subject:** current location / secondary chart.
- **Authority:** profile.
- **Required fields:** location name; coords; UTC.
- **Optional fields:** short relocation label.
- **Forbidden fields:** profile-management controls; full birth detail.
- **Allowed placement:** beside wheel; above wheel; sticky column (compact).

### 3.3 Location-Subject Plate

- **Intended use:** Relocated Location page where the place is the subject but the
  profile is the authority.
- **Subject:** relocated location.
- **Authority:** profile.
- **Required fields:** place name; profile lens ("For {profile}"); country/region;
  lat/lon; UTC; favorite state when relevant.
- **Optional fields:** favorite toggle; secondary descriptors.
- **Forbidden fields:** edit/add profile; full city intelligence body; place as the
  *sole* authority (profile lens must remain).
- **Allowed placement:** page top (above wheel).

### 3.4 Side Plate

- **Intended use:** narrow chart-adjacent identity/metadata block.
- **Subject:** the chart being shown (natal or relocated).
- **Authority:** profile.
- **Required fields:** subject place/identity; coords; profile name.
- **Optional fields:** chart label; system context (birth/relocated/system rows).
- **Forbidden fields:** city intelligence; notes editors.
- **Allowed placement:** side metadata column; beside wheel.

### 3.5 Micro Plate

- **Intended use:** map popup head and modal head — minimum viable orientation.
- **Subject:** clicked point / enlarged chart.
- **Authority:** active profile **only when** chart data is shown; otherwise point only.
- **Required fields:** point/title; lat/lon.
- **Optional fields:** admin/country; policy or provenance note; compact chart preview.
- **Forbidden fields:** full city intelligence; notes ownership; destination-level UI.
- **Allowed placement:** popup top; modal top.

### 3.6 Comparison Profile Plate

- **Intended use:** the single governing-profile band on a Comparison page.
- **Subject:** profile context for the comparison.
- **Authority:** profile.
- **Required fields:** profile name; birth date/UTC; birth place; coords;
  Tropical/Placidus.
- **Optional fields:** edit/add controls; current-location column.
- **Forbidden fields:** place as authority; per-table notes ownership.
- **Allowed placement:** page top (below nav).

### 3.7 Comparison City Plate

- **Intended use:** repeated per-place identity in a comparison column.
- **Subject:** comparison place/column.
- **Authority:** comparison set + profile.
- **Required fields:** city/place name; country/admin; coords.
- **Optional fields:** current-location tag; column controls (hide/reorder/replace).
- **Forbidden fields:** profile birth data; profile switching.
- **Allowed placement:** sticky column (city bar).

### 3.8 City Intelligence Hero Plate

- **Intended use:** full city intelligence page identity.
- **Subject:** place.
- **Authority:** place / intelligence dataset.
- **Required fields:** city/place name; orientation or KPI snapshot.
- **Optional fields:** photos; population/cost/climate KPIs.
- **Forbidden fields:** profile-specific chart claims; astrology authority.
- **Allowed placement:** page top (hero).

### 3.9 Context / Scaffold Plate

- **Intended use:** architecture/walkthrough scaffolding only (e.g. app_shell).
- **Subject:** route/module or chart-record context.
- **Authority:** scaffold (chart record / route).
- **Required fields:** screen/route name; active record/place context.
- **Optional fields:** debug IDs; resumed exploration context.
- **Forbidden fields:** treatment as production visual canon.
- **Allowed placement:** scaffold screens only — not a product plate.

---

## 4. Placement Principles

Defines where each family is **allowed** to live. This is not a final layout
decision; it is a constraint on legal placements.

| Placement zone | Allowed plate families |
|---|---|
| Above wheel | Full Profile, Compact Profile, Location-Subject |
| Beside wheel | Full Profile, Compact Profile, Side |
| Page top | Location-Subject, Comparison Profile, City Intelligence Hero |
| Sticky column | Comparison City, Compact Profile (compact) |
| Popup top | Micro |
| Modal top | Micro |
| Side metadata column | Side |

Principle: a chart-bearing page must show its governing plate **without scrolling
the wheel out of view**. The plate orients; the wheel is the promise.

---

## 5. Profile Authority Rule

**Profile remains the highest authority for all chart-bearing pages.**

If the active profile changes, the chart-bearing page **must re-render**: wheel,
houses, interpretations, favorite state, and notes context all follow the profile.

This applies to:

- Map
- Profile
- Relocated Location
- Comparison

The page subject may be a location or a comparison set, but the lens is always the
profile. Profile-selection must therefore remain available on these surfaces using
consistent profile-authority language.

---

## 6. Notes Ownership Rule (provisional)

**Notes attach to entities, not table sections.**

Allowed note owners:

- profile
- favorite location
- comparison
- saved search
- future map research session

Forbidden note owners:

- PiH table
- AiS table
- A2A table
- individual table rows
- individual cards

The Profile page should eventually act as the **master notebook / clearinghouse**,
offering filtered access to all notes across owners. A favorite place owns its
notes; multiple surfaces (Profile favorites, Relocated Location) may view/edit the
same underlying note record.

This is preserved here as doctrine; it is not solved in this document.

---

## 7. Explicit Non-Goals

This doctrine does **not** decide:

- final colors
- final fonts
- final animation timing
- final badge styles
- final metadata styles

Those belong to later doctrines and must not be inferred from this document.

---

## 8. Implementation Implications

Immediate, practical implications for future work:

- Unify profile-authority display across Map / Profile / Relocated / Comparison
  later (currently: native select, serif plate selector, header button, static text).
- Treat the Relocated Location page as **location-subject / profile-authority**.
- Keep the map popup as a **Micro Plate**, never a full destination page.
- Treat `city_profile_v4.html` as the likely **City Intelligence Hero Plate**
  candidate.
- Consolidate Comparison around the **v5** pattern (`profile-block` +
  `city-nameplate`) later.
- Keep `app_shell.html` plates **scaffold-only**; do not promote its "Chart Record"
  language or styling into product canon.
