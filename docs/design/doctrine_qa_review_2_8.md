# Doctrine QA Review — Plate / Badge & Metadata / Visual Hierarchy

Status: QA checkpoint (Phase 2.8, post-Hierarchy)
Type: review only — no code, prototypes, colors, fonts, or redesign
Purpose: lock what is decided, record what was rejected, and carry forward what
is still open — before the Surface Treatment Doctrine begins.

Documents reviewed:
- `docs/design/plate_doctrine.md` (2.8C)
- `docs/design/badge_and_metadata_doctrine_audit.md` (2.8D + correction pass)
- `docs/design/visual_hierarchy_doctrine_audit.md` (2.8H)

Legend:
- **Confirmed** — stable; treat as binding doctrine going forward.
- **Rejected** — considered and explicitly walked back; do not reintroduce.
- **Open** — unresolved tension; carried forward, not decided here.

---

## A. Plate Doctrine

### Confirmed
- A plate is the identity/context block answering **subject** and **authority**.
- **Subject and authority can differ** and both must always be legible.
- When subject is not the profile, the plate must still surface the governing
  profile ("For {profile}").
- **Profile is the highest authority** on all chart-bearing pages; if the active
  profile changes, the page **must re-render** (wheel, houses, interpretations,
  favorite state, notes context).
- Nine approved plate families (Full Profile, Compact Profile, Location-Subject,
  Side, Micro, Comparison Profile, Comparison City, City Intelligence Hero,
  Context/Scaffold).
- Relocated Location page = **location-subject / profile-authority**.
- Map popup = **Micro plate**, never a full destination.
- A chart-bearing page must show its governing plate **without scrolling the
  wheel out of view** ("the plate orients; the wheel is the promise").
- **Notes attach to entities, not table sections** (allowed: profile, favorite
  location, comparison, saved search, future map session).
- Profile page = eventual **master notebook / clearinghouse**.
- Pattern anchors: `city_profile_v4` = City Intelligence Hero candidate;
  consolidate Comparison around **v5**; `app_shell` plates are scaffold-only.

### Rejected
- Place as the **sole** authority on the Relocated page (profile lens must remain).
- Per-table / per-row / per-card note ownership (PiH/AiS/A2A notes, row notes).
- Promoting `app_shell` "Chart Record" language/styling into product canon.

### Open
- Exact compact/expanded field sets per family at small sizes.
- Where the governing profile renders on each surface (selector vs static text).

---

## B. Badge & Metadata Doctrine

### Confirmed
- **Birth Time is Tier 1 identity/chart data**, never grouped with Lat/Lon, UTC,
  or source/provenance.
- Tier 1 identity block = **Profile Name + Birth Date + Birth Time + Birth Place**.
- **Tropical and Placidus are metadata, not badges.**
- Lat/Lon and UTC are **supporting technical metadata**.
- User-facing badges should stay limited (lean: **Natal** and **Current
  Location**); other states are context/status, handled lightly.
- Favorite is a **mixed Action + Status** control (separation deferred, see Open).
- **Provenance, dataset notes, and diagnostics belong in tooltips/footnotes**,
  never as primary badges.
- Lat-cap ON/OFF debug overlay is **never** product canon.
- Placement tendencies: identity/subject go **up/beside** the wheel; system +
  provenance go **below or into tooltips**; livability facts go into
  **tables/intelligence**.
- Authority hierarchy (chart pages): Profile/Native > Wheel > Context > Metadata,
  and **no audited chart page lets metadata outrank the wheel or profile**.
- Action language (Add / Edit / Change …) standardization is a **required future
  doctrine**; provisional split: Add = create/attach, Edit = modify contents,
  Change = switch a selected setting/context/value.

### Rejected
- **"Relocated Location" as a required, primary, user-facing badge** (correction
  pass): internal doctrine language only; relocated places are identified by
  place name + favorite state + chart context.
- Grouping Birth Time visually with Lat/Lon / UTC / source.
- Treating Tropical/Placidus as badges/context labels.
- Using **Add / Edit / Change interchangeably**.
- Storing a **state in the country field** ("Texas, USA" in the country slot).

### Open
- "Current Location" vs "Relocated" vocabulary (one term needed).
- Favorite: status vs action separation.
- Date / time / Lat-Lon / UTC / country / state canonical formats.
- State/country abbreviation vs full name; long-name handling.
- UTC vs local time presentation; named time-zone (JST) shown or tooltip-only.
- Tropical/Placidus placement (sub-line vs sys rows vs system band — three today).
- Lat/Lon precision (2 vs 4 decimals; hemispheric vs signed).
- Metadata density on mobile.
- Confidence / Archived / Shared / Draft badge treatment when surfaced.
- Provenance final home (tooltip vs footnote vs City Intelligence section).
- `app_shell` "Chart Record"/record-type vocabulary reconciliation.

---

## C. Visual Hierarchy Doctrine

### Confirmed
- **Wheel centrality:** the wheel is the central object on all chart-bearing
  pages and must not be displaced by plates or metadata.
- Authority stack: **Profile/owner > active chart (wheel) > location/context >
  reference tables > metadata > provenance/system**.
- Always visible on chart pages: **profile authority (or selector), the wheel,
  and the current context label.**
- May collapse: detailed metadata, city detail, comparison sections, notes
  composers.
- **Table working-rank:** primary = A2A + comparison matrices; secondary = PiH +
  mini city intelligence; reference-only = AiS + popup preview + scaffold.
- Rank reflects **time-on-surface for analysis**, not visual size.
- Notes are a **supporting layer** that never outranks the wheel or working
  tables; Profile sits atop the notes hierarchy as clearinghouse.
- City Intelligence is the deliberate **place-authoritative exception** (no
  wheel; profile does not govern it; must never imply chart authority).
- Map popup is **preview-rank**; the full wheel/chart is **destination-rank**.

### Rejected
- Allowing metadata, badges, notes, or provenance to visually dominate the wheel.
- Treating the densest table (A2A All mode) as an automatic default focus
  (kept opt-in, see Open).

### Open
- Subject-vs-authority **visual balance** when they differ (location plate read
  first vs wheel centrality on Relocated).
- **Profile authority weight on Map** (selector currently least prominent yet
  highest authority).
- Comparison **authority vs subject** weight (profile band light vs matrices heavy).
- Notes **visibility** per page without competing with wheel/tables.
- Comparison **density** ceiling (columns/sections before overload).
- Metadata **visibility vs collapse** thresholds.
- **Long-name handling** in plates and sticky columns.
- **Profile-switching visibility** (how visible the action and its re-render are).
- A2A All-mode default vs opt-in.

---

## D. Cross-Doctrine Consistency Check

- **No contradictions found** among the three documents. They form a consistent
  spine: Plate (what/whose) -> Badge & Metadata (which atoms, what tier, where) ->
  Hierarchy (where attention goes).
- **Reinforced across all three:** profile authority supremacy; wheel centrality;
  notes-belong-to-entities; metadata never outranks the wheel; map popup is a
  micro/preview, not a destination; comparison consolidates on v5; city profile
  is place-authoritative and chart-free.
- **Recurring unresolved theme (highest carry-forward priority):**
  **subject-vs-authority weighting** and **profile-authority visibility on Map
  and Comparison** appear as Open in both the Badge/Metadata and Hierarchy
  reviews. These should be first to resolve once styling work can encode weight.
- **Vocabulary debt:** "Current Location" vs "Relocated", and Add/Edit/Change,
  remain open in two documents and gate consistent labeling.

---

## E. QA Verdict

- Plate, Badge & Metadata, and Visual Hierarchy doctrines are **internally
  consistent and mutually reinforcing**; confirmed items above are safe to treat
  as binding.
- Rejected items must **not** be reintroduced by later phases.
- Open items are **not blockers** for Surface Treatment Doctrine, which concerns
  *how surfaces are treated* (depth/separation/atmosphere by role) rather than
  *what attention or authority means* — but Surface Treatment must honor every
  Confirmed item, especially **wheel centrality** and **authority order**.

Proceeding to Surface Treatment Doctrine.
