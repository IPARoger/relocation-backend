# SAVED_OBJECTS_PRODUCT_CANON.md

**Status:** Canonical saved-objects product specification.  
**Version:** V1 (2026-06-27)  
**Type:** Product canon — not an implementation spec, not a schema, not a UI redesign.  
**Authority:** Subordinate to `FOUNDATIONAL_CONSTITUTION.md`, `INTERFACE_AND_DESIGN_CANON.md`, `SETTINGS_V1_PRODUCT_SPEC.md`, and `MATERIAL_SYSTEM_CANON.md`.  
**Companion:** `docs/canon/SETTINGS_V1_PRODUCT_SPEC.md` (Settings management surfaces, sort law, composite rule)  
**Revision policy:** Durable product rules live here. Engineering may choose storage shapes; product behavior must match this canon.

**Purpose:** Single source of truth for every persistent object the user creates, saves, manages, archives, deletes, searches, shares, and exports — preventing drift between Profile, Favorites, Settings, Comparison, Notes, Export, and future Library features.

---

## 0. Enduring guidance

> **Objects never silently disappear.**

Users must always understand what happened to their work: created, renamed, archived, restored, or deleted. **Archive is preferred over delete.** **Delete is always destructive** and must warn. **Bulk delete always warns.**

**Rename never changes identity** — display title may change; stable record id does not.

**Settings manages objects. Profile consumes objects. Export is a workflow** — not a primary object home.

**Search never replaces good organization.** Folders, labels, and honest lists come first; search supplements.

**Sorting is ONLY** (per Settings V1): **A–Z · Recently Added · Recently Viewed · Distance**. No weighting, AI ranking, “best match,” or hidden scores.

---

## 1. Global lifecycle law

| Action | Product rule |
|--------|--------------|
| **Create** | Explicit user action or documented automatic create (e.g. composite → new profile). User receives confirmation when identity is new. |
| **Rename** | Changes display name/title only. Never re-keys identity or merges records. |
| **Archive** | Removes from active/default surfaces; recoverable from Settings → Archives (or equivalent). Preferred over delete. |
| **Restore** | Returns archived object to active library; prior folder/label membership restored when applicable. |
| **Delete** | Permanent removal after confirmation. Single-object warning. Never silent. |
| **Bulk delete** | Multi-select + **irreversible warning** listing count and object types. |
| **Search** | Text search across title, body, place names, tags/labels when present. Does not reorder by relevance score in V1 — results sort per §0 sort law only. |
| **Share** | Object-type-specific; see per-object tables. No share without user intent. |
| **Export** | Contextual workflow at export time; Settings may hold defaults only (future export presets). |

---

## 2. Primary homes (binding)

| Surface | Role |
|---------|------|
| **Settings → My Data** (and typed sub-lists) | **Manage** — rename, archive, restore, delete, bulk delete, folder/label assignment where supported |
| **Profile** | **Consume** — active birth profile, natal context, summary of folders/labels without clutter |
| **Comparison** | **Workflow** — open/save comparison sets; notes rail; not long-term library admin |
| **Map / popup** | **Workflow** — save investigation, favorite place; defers deep management to Settings |
| **Notes Library** | **Workflow + read** — compose and find notes; bulk admin in Settings |
| **Export flow** | **Workflow** — run export on selected object(s); templates not owned by Settings primary UI |

---

## 3. Object specifications

Each object below uses the same field order. **Icon** = default semantic icon family (glyph/asset — not emoji per Settings V1).

---

### 3.1 Birth Profiles

| Field | Rule |
|-------|------|
| **Purpose** | Canonical identity for a person’s birth data — natal chart record, default map/comparison anchor. |
| **Where it appears** | Profile (primary), Settings → My Data → Birth Profiles, map nameplate, Comparison authority plate. |
| **Created** | First-run birth intake; Settings “Add profile”; duplicate-as-new never in place. |
| **Renamed** | Settings or Profile display name edit. Identity unchanged. |
| **Archived** | Hidden from picker defaults; data retained. |
| **Restored** | Returns to profile picker and My Data active list. |
| **Deleted** | Destructive; warns that comparisons, notes links, and favorites may orphan or cascade per policy (user must see scope). |
| **Bulk delete** | Allowed with type-specific warning. |
| **Search** | Name, birth place text in Settings list. |
| **Sort** | A–Z, Recently Added, Recently Viewed; Distance N/A. |
| **Folders** | N/A for profile itself; see Favorites/labels on Profile summary. |
| **Share** | Deferred V1 — no public profile URL without explicit future share product. |
| **Export** | Profile export workflow includes wheel/tables per export template. |
| **Default icon** | Natal / person plate glyph. |
| **Relationships** | Parent of Relocated Charts; referenced by Comparisons, Notes, Saved Searches. |
| **Primary home** | **Profile** (consume) · **Settings** (manage) |

---

### 3.2 Composite Profiles

| Field | Rule |
|-------|------|
| **Purpose** | Chart record representing midpoints/composite of two or more **existing** birth profiles. |
| **Where it appears** | Settings → My Data; Profile picker; Comparison authority when selected. |
| **Created** | Settings or Profile management → **Create Composite** — select 2+ birth profiles → **creates NEW profile/chart record**. Never mutates source profiles. |
| **Renamed** | Same as birth profiles. |
| **Archived / Restored / Deleted** | Same lifecycle as birth profiles. |
| **Bulk delete** | Allowed with warning. |
| **Search / Sort** | Same as birth profiles. |
| **Folders** | N/A. |
| **Share / Export** | Same class as birth profiles. |
| **Default icon** | Composite / merged plate glyph (distinct from natal). |
| **Relationships** | Derived from 2+ Birth Profiles; otherwise same affordances as birth profile. |
| **Primary home** | **Settings** (create/manage) · **Profile** (consume) — **low prominence** per Settings V1. |

---

### 3.3 Relocated Charts

| Field | Rule |
|-------|------|
| **Purpose** | Astrological chart for a **place** (or saved location context) relative to a birth profile — relocation snapshot, not a new person. |
| **Where it appears** | Relocated page, map popup “view relocated chart,” Comparison column data source, Profile/Relocated history. |
| **Created** | Opening a place for a profile; saving from map popup; implicit on comparison city add (engine-backed). |
| **Renamed** | Usually inherits place display name; user may override label in Settings if stored as first-class saved row. |
| **Archived** | Removes from recent/history lists; calculation cache may remain until delete. |
| **Restored** | From Archives in Settings. |
| **Deleted** | Warns if referenced by Saved Comparison or Investigation. |
| **Bulk delete** | Allowed in Settings history lists with warning. |
| **Search** | Place name, country, profile name. |
| **Sort** | A–Z (place), Recently Added, Recently Viewed, **Distance** (when user location or reference place available). |
| **Folders** | N/A unless grouped under Saved Search parent. |
| **Share** | Future — export/share relocated table/wheel as artifact. |
| **Export** | Via export workflow on Relocated or Comparison context. |
| **Default icon** | Pin / relocated wheel glyph. |
| **Relationships** | Child of Birth Profile + Place; feeds Comparison columns, CI, Notes. |
| **Primary home** | **Workflow screen** (Relocated, popup) · **Settings** (history/manage) |

---

### 3.4 Saved Searches / Investigations

| Field | Rule |
|-------|------|
| **Purpose** | Persisted map investigation — Genie query, overlay context, optional notes, tied to places searched. |
| **Where it appears** | Map save disk dialog; Settings → Saved Searches; optional Profile summary count. |
| **Created** | Map → Save investigation (title + optional notes). |
| **Renamed** | Settings or edit dialog; identity preserved. |
| **Archived** | Removed from map quick-reopen; retained in Archives. |
| **Restored** | Reactivates in library; reopen on map from Settings. |
| **Deleted** | Destructive; warns. |
| **Bulk delete** | Supported with irreversible warning. |
| **Search** | Title, notes body, place names. |
| **Sort** | A–Z, Recently Added, Recently Viewed, Distance (to investigation primary place if geo). |
| **Folders / Labels** | Tags or folders when wired; optional on create. |
| **Share** | Future export/share of investigation summary — not V1 social share. |
| **Export** | Export workflow at save object or Comparison/Notes bundle. |
| **Default icon** | Save disk / investigation glyph. |
| **Relationships** | Links Profile, places, Notes; may reference Comparison set id. |
| **Primary home** | **Workflow** (map) · **Settings** (manage) |

---

### 3.5 Saved Comparisons

| Field | Rule |
|-------|------|
| **Purpose** | Named comparison **set** — cities/places compared against one chart record, with workspace state (hidden columns, angle tab, notes). |
| **Where it appears** | Comparison route (`#/compare`), Settings → Saved Comparisons, Profile summary. |
| **Created** | Comparison → Save (new set) or Add cities then save; URL may carry `comparisonSetId`. |
| **Renamed** | Settings; does not change set id or column place ids. |
| **Archived** | Hidden from recent/open list; restorable. |
| **Restored** | Opens in Comparison route with prior workspace. |
| **Deleted** | Warns; notes attached to set may orphan unless cascade explained. |
| **Bulk delete** | Supported with warning. |
| **Search** | Set title, city names, profile name. |
| **Sort** | A–Z, Recently Added, Recently Viewed; Distance N/A unless sorted by primary city geo. |
| **Folders / Labels** | Optional tags in Settings. |
| **Share** | Future — read-only comparison link deferred. |
| **Export** | Comparison export workflow (tables, notes slot, CI when live). |
| **Default icon** | Column / compare glyph. |
| **Relationships** | References Birth Profile, Relocated Charts per column, Notes rail content, CI blocks. |
| **Primary home** | **Workflow** (Comparison) · **Settings** (manage) |

---

### 3.6 Favorites

| Field | Rule |
|-------|------|
| **Purpose** | User-curated **places** (and optionally profiles) for fast return — geographic intent, not full investigations. |
| **Where it appears** | Map favorites UI, Profile favorites summary, Settings → Favorites. |
| **Created** | Map popup Favorite; city bar favorite tag; explicit add in Settings. |
| **Renamed** | Display label for favorite entry; place id unchanged. |
| **Archived** | Removes from map quick list; kept in Archives. |
| **Restored** | Returns to favorites folders. |
| **Deleted** | Removes favorite link; does not delete place from globe. |
| **Bulk delete** | Supported with warning. |
| **Search** | Place name, folder name, label text. |
| **Sort** | A–Z, Recently Added, Recently Viewed, **Distance**. |
| **Folders / Labels** | **Required product capability** — favorites support folders/labels; managed in Settings; Profile shows compact folder summary only. |
| **Share** | Export place list future; no V1 public favorite list. |
| **Export** | Optional favorites export via export workflow. |
| **Default icon** | Star / bookmark place glyph. |
| **Relationships** | Links Place; may appear in Comparison city bar badges (Natal/Current/Favorite). |
| **Primary home** | **Settings** (manage folders) · **Profile** (summary) · **Map popup** (create) |

---

### 3.7 Notes

| Field | Rule |
|-------|------|
| **Purpose** | User-authored text bound to chart context — profile, comparison set, place, or investigation species per Notes canon. |
| **Where it appears** | Profile t-band, Comparison notes rail, Notes Library, Settings → Notes. |
| **Created** | Type in composer → Save; auto-draft behavior must not silently discard on navigation without honest save state. |
| **Renamed** | Title field in Notes Library / Settings. |
| **Archived** | Hidden from active notebooks; restorable. |
| **Restored** | Returns to library and linked surfaces. |
| **Deleted** | Destructive; warns. |
| **Bulk delete** | Supported with warning in Settings. |
| **Search** | Title, body, linked place/comparison/profile metadata. |
| **Sort** | A–Z (title), Recently Added, Recently Viewed; Distance N/A unless sorted by linked place. |
| **Folders / Labels** | Collections in Notes Library; align with Folders/Labels canon (§3.10). |
| **Share** | Export includes notes when template allows; no anonymous paste link V1. |
| **Export** | Bundled in Comparison/Profile export workflows. |
| **Default icon** | Notebook / pen glyph. |
| **Relationships** | Attached to Profile, Comparison set, Saved Search, or place context. |
| **Primary home** | **Workflow** (inline composers) · **Notes Library** · **Settings** (bulk admin) |

---

### 3.8 Future Export Presets

| Field | Rule |
|-------|------|
| **Purpose** | Saved **defaults** for export formatting (sections included, redaction, paper layout) — not the export act itself. |
| **Where it appears** | Export workflow picker; Settings → defaults subsection only when wired. |
| **Created** | Save current export options as preset inside export flow. |
| **Renamed / Archived / Restored / Deleted** | Settings management when feature ships. |
| **Bulk delete** | Rare; supported with warning. |
| **Search / Sort** | A–Z, Recently Added, Recently Viewed. |
| **Folders** | N/A. |
| **Share** | N/A — presets are personal. |
| **Export** | Presets configure export; they are not exported as primary objects. |
| **Default icon** | Export / template glyph. |
| **Relationships** | Referenced by export workflow only. |
| **Primary home** | **Export workflow** (create/use) · **Settings** (defaults storage) — **future** |

---

### 3.9 Future Report Templates

| Field | Rule |
|-------|------|
| **Purpose** | Structured multi-section reports (wheel + tables + CI + notes) for professional deliverables. |
| **Where it appears** | Export / Report workflow — **not** Settings primary nav. |
| **Created** | Report builder at export time; save as template for reuse. |
| **Lifecycle** | Same global law when implemented. |
| **Search / Sort** | A–Z, Recently Added, Recently Viewed. |
| **Share** | Future controlled share of generated report artifact. |
| **Export** | **Is** the export product. |
| **Default icon** | Report / document glyph. |
| **Relationships** | Composes Birth Profile, Comparison, Notes, CI snapshots. |
| **Primary home** | **Export workflow** — **future** |

---

### 3.10 Folders / Labels

| Field | Rule |
|-------|------|
| **Purpose** | Organizational metadata grouping Favorites, Notes, and applicable saved lists — **not** a separate astrological object. |
| **Where it appears** | Settings management UI; compact chips on Profile; folder pickers in Favorites/Notes. |
| **Created** | User creates folder/label in Settings or inline “add to folder” on save. |
| **Renamed** | Folder/label display name only; membership ids stable. |
| **Archived** | Archive folder → archives contained items or unwraps per explicit UX copy (must not silent-delete children). |
| **Restored** | Restores folder and membership. |
| **Deleted** | Warns: items become uncategorized, not deleted, unless user chooses “delete all contents.” |
| **Bulk delete** | Folder bulk remove with warning. |
| **Search** | Folder name; filter lists by folder. |
| **Sort** | A–Z for folder names; contents use object sort law. |
| **Share / Export** | N/A as first-class share unit. |
| **Default icon** | Folder / tag glyph. |
| **Relationships** | Many-to-many on Favorites, Notes, optionally Saved Searches/Comparisons. |
| **Primary home** | **Settings** (define) · **Profile** (glance) |

---

### 3.11 Tags (future)

| Field | Rule |
|-------|------|
| **Purpose** | Lightweight cross-cutting labels (e.g. `client`, `trip-2026`) — simpler than folders, combinable. |
| **Where it appears** | Settings; filter chips in Library views — **future**. |
| **Lifecycle** | Same global law; rename tag renames display string for all members. |
| **Search** | Tag text is primary filter. |
| **Sort** | A–Z on tag name; object lists use §0 sort law. |
| **Folders** | Tags complement folders; do not require nested hierarchy V1. |
| **Primary home** | **Settings** — **future** |

---

## 4. Cross-object consistency matrix

| Object | Settings manage | Profile consume | Workflow create | Popup / context menu |
|--------|:---------------:|:-----------------:|:---------------:|:--------------------:|
| Birth Profile | ✓ | ✓ | Intake | — |
| Composite Profile | ✓ | ✓ | Settings/Profile | — |
| Relocated Chart | ✓ | summary | Relocated / map | popup |
| Saved Search | ✓ | count | map save | — |
| Saved Comparison | ✓ | summary | Comparison | — |
| Favorite | ✓ | summary | map popup | favorite |
| Note | ✓ | inline | composers | — |
| Export Preset | defaults | — | export | — |
| Report Template | — | — | export | — |
| Folder/Label | ✓ | chips | inline pick | — |
| Tag | ✓ future | — | future | — |

---

## 5. Anti-patterns (binding)

- Silently removing objects from UI without archive/delete confirmation.
- Renaming that re-keys database ids or merges two users’ records.
- Composite creation that overwrites a source birth profile.
- AI-sorted or relevance-ranked library views.
- Settings pages that host export wizards as primary UI.
- Decorative archive/delete icons with no effect.
- Profile page becoming a full DAM (digital asset manager) — use Settings for bulk ops.
- Emoji as object icons.

---

## 6. Relationship to Settings V1

`SETTINGS_V1_PRODUCT_SPEC.md` §10 requires management surfaces for Saved Searches, Saved Comparisons, Favorites, Notes, and Birth Profiles with rename, archive, tag/folder, delete, and bulk delete. **This canon defines per-object behavior; Settings V1 defines Settings-shell obligations.** On conflict, both must be satisfied; escalate to INTERFACE_AND_DESIGN_CANON for product arbitration.

---

## 7. Acceptance checklist — Saved Objects V1

- [ ] Every object type in §3 has a documented create path and primary home.
- [ ] No object silently disappears from user view.
- [ ] Archive preferred; delete always warns; bulk delete always warns.
- [ ] Rename never changes stable identity.
- [ ] Composite profiles always create **new** records.
- [ ] Favorites support folders/labels; Profile shows summary only.
- [ ] Settings hosts management; Profile hosts consumption; Export stays workflow-first.
- [ ] All sortable lists use only: A–Z, Recently Added, Recently Viewed, Distance.
- [ ] No AI ranking, weighting, or “best match” sort.
- [ ] Search supplements folders/labels; does not replace organization.
- [ ] Export presets and report templates deferred to export workflow per §3.8–3.9.
- [ ] Tags documented as future; folders/labels active for Favorites and Notes.
- [ ] Cross-object matrix (§4) reflected in PO QA before external beta.

---

*End of Saved Objects Product Canon.*
