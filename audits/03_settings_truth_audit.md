# AUDIT: 03_SETTINGS_TRUTH_AUDIT

**Type:** Read-only product-truth audit
**Author:** Cursor (relay trial — results/ lane)
**Date:** 2026-06-15
**Depends on:** `audits/02_settings_consumption_audit.md`
**Status:** Read-only — no code/backend/schema/data changes

---

## Objective

Classify every setting from the 02 audit as MVP Product Truth, Deferred Product
Truth, Placeholder, or Abandoned. Determine owning screen, launch requirement,
and future dependency.

---

## Classification definitions

- **MVP Product Truth** — setting is live, wired, and correctly affects behavior
  today. Required and functional.
- **Deferred Product Truth** — setting is a legitimate future product requirement.
  It is real and will eventually be wired, but is intentionally not wired for
  the current phase. Not honesty-dishonest if it has no UI control; honesty-gap
  if it has a UI control implying it works.
- **Placeholder** — setting field exists to reserve schema space. No current user
  workflow depends on it. Could be wired or removed later.
- **Abandoned** — the layer this setting was designed for has been explicitly
  frozen or deferred per project governance. No near-term wiring planned.

---

## Product-truth audit by setting

---

### 1. `default_chart_record_id`

| Attribute | Value |
|---|---|
| **Classification** | **MVP Product Truth** |
| User-facing workflow | Dashboard loads with the default record. "Open Map" uses it. Nav context falls back to it. |
| Owning screen | Settings |
| Required for MVP? | **Yes** |
| Deferred? | No |
| Abandoned? | No |
| Future dependency | None — complete as-is. |

**Reasoning:** Fully wired and correctly consumed. The professional astrologer
workflow requires a stable default record so that opening the app or returning to
the dashboard is predictable. This setting is doing exactly what it should.

---

### 2. `house_system`

| Attribute | Value |
|---|---|
| **Classification** | **Deferred Product Truth (with active honesty gap)** |
| User-facing workflow | Professional astrologers use different house systems (Placidus, Whole Sign, Koch, Equal). Relocated chart facts — ASC/MC/DSC/IC and planet-in-house placements — change meaningfully with house system. |
| Owning screen | Settings (UI exists), Engine (consumption missing) |
| Required for MVP? | **No — not required if Placidus is the only supported system, provided the UI is honest about it.** |
| Deferred? | **Yes — engine wiring is deferred.** |
| Abandoned? | No — it is a legitimate future requirement. |
| Future dependency | Engine threading: `SearchRequest` field + `swe.houses` `hsys` param + `/relocated-chart` query param. Medium–large implementation. |

**Reasoning:** The setting exists because house system choice is a real,
professional-level product need. However, it is *currently dishonest*: the
Settings screen offers a dropdown and a Save button that imply the choice has
effect, but the engine hardcodes Placidus. The correct MVP resolution is one of:
(a) hide/disable the house-system selector with "Placidus only — more systems
coming" until the engine is wired, or (b) wire the engine. It must not remain
as a live dropdown that implies choice while having no effect.

**This is the only setting with an active UI honesty gap today.**

---

### 3. `zodiac_mode`

| Attribute | Value |
|---|---|
| **Classification** | **Deferred Product Truth** |
| User-facing workflow | Tropical vs sidereal zodiac changes every planet longitude; it is a fundamental astrologer preference. Western relocation astrology is almost universally tropical. Vedic/sidereal astrologers exist but are not the current target user. |
| Owning screen | Settings (no UI control exists yet) |
| Required for MVP? | **No** |
| Deferred? | **Yes** |
| Abandoned? | No |
| Future dependency | Engine support for sidereal mode (`swe.set_sid_mode` before calculations). Low immediate priority given target professional is Western. |

**Reasoning:** No UI control exists, so there is no current honesty gap. The
field is stored in the schema shape for future use. Leave as-is until explicitly
needed.

---

### 4. `orb_defaults`

| Attribute | Value |
|---|---|
| **Classification** | **Deferred Product Truth** |
| User-facing workflow | Professional astrologers customize their orbs. Tighter or looser orbs change which aspects qualify for conditions in `/search-regions`. This is a real, high-value professional customization. |
| Owning screen | Settings (no UI control exists yet) |
| Required for MVP? | **No** |
| Deferred? | **Yes** |
| Abandoned? | No |
| Future dependency | `SearchRequest` would need an `orb_overrides` field; the aspect-band logic would need to consume it. Medium implementation. |

**Reasoning:** No UI control, no honesty gap. The defaults are sensible. When
aspect-based search is the primary professional workflow, orb customization will
become high value. Deferred correctly.

---

### 5. `visible_minor_aspects`

| Attribute | Value |
|---|---|
| **Classification** | **Deferred Product Truth** |
| User-facing workflow | Minor aspects (semi-square, sesquiquadrate, quincunx, etc.) are used by many professional astrologers. Showing or hiding them in search conditions and relocated chart output is a legitimate preference. |
| Owning screen | Settings (no UI control) |
| Required for MVP? | **No** |
| Deferred? | **Yes** |
| Abandoned? | No |
| Future dependency | Genie condition builder + `/search-regions` + `/relocated-chart` would need to recognize minor aspect types. Medium implementation when minor aspects are added to the Genie. |

**Reasoning:** No UI control, no honesty gap. Placeholder correctly placed for
when minor aspects are introduced into the Genie condition builder.

---

### 6. `helper_layers`

| Attribute | Value |
|---|---|
| **Classification** | **Placeholder** |
| User-facing workflow | Unclear. Likely intended for map overlay helper layers (e.g. timezone lines, equator, ecliptic). No clear user-facing workflow documented in current codebase. |
| Owning screen | Unknown / Map (I — not confirmed in codebase) |
| Required for MVP? | **No** |
| Deferred? | Unclear |
| Abandoned? | Possibly — the field name suggests it was intended for a visual/map feature that is not referenced anywhere in the current frontend or backend. |
| Future dependency | Unknown. |

**Reasoning:** No UI, no consumption, no documented workflow. Could be repurposed
or removed. Not a honesty gap. Lowest priority of all fields.

---

### 7. `ontology_pack_id`

| Attribute | Value |
|---|---|
| **Classification** | **Abandoned (frozen per governance)** |
| User-facing workflow | Would support switching between interpretation frameworks (e.g. traditional vs modern rulerships, different dignity systems). This is an AI/interpretation layer concept. |
| Owning screen | Future AI/interpretation layer (frozen) |
| Required for MVP? | **No** |
| Deferred? | No — explicitly frozen |
| Abandoned? | **Yes — AI interpretation layers are frozen per project governance** |
| Future dependency | Layer 4/5 / AI interpretation (out of scope for Web2 phase) |

**Reasoning:** Per project governance: "AI interpretation layers are frozen. Do
not revisit unless a specific defect is demonstrated." This field was provisioned
for a future that is not in scope. It should be treated as inert and reserved,
not removed, but not wired.

---

### 8. `settings_version`

| Attribute | Value |
|---|---|
| **Classification** | **Placeholder** |
| User-facing workflow | None — this is an infrastructure field for future schema migration gating. |
| Owning screen | None (internal) |
| Required for MVP? | **No** |
| Deferred? | Yes — when `settings_json` shape changes, this enables migration. |
| Abandoned? | No |
| Future dependency | Settings migration guard when `settings_json` schema evolves. |

**Reasoning:** Correct placeholder. No user-facing role. No honesty gap.
Retain for future migration safety.

---

## Master table

| Setting | Classification | Required for MVP? | Deferred? | Abandoned? | Owning Screen | Future Dependency |
|---|---|---|---|---|---|---|
| `default_chart_record_id` | MVP Product Truth | **Yes** | No | No | Settings | None |
| `house_system` | Deferred Product Truth (**active honesty gap**) | No (if UI is honest) | **Yes** | No | Settings + Engine | Engine hsys param threading |
| `zodiac_mode` | Deferred Product Truth | No | Yes | No | Settings | Sidereal engine support |
| `orb_defaults` | Deferred Product Truth | No | Yes | No | Settings | SearchRequest orb override |
| `visible_minor_aspects` | Deferred Product Truth | No | Yes | No | Settings | Minor aspect Genie + engine |
| `helper_layers` | Placeholder | No | Unclear | Possibly | Map (unknown) | Unknown |
| `ontology_pack_id` | Abandoned (frozen) | No | No | **Yes** | AI layer (frozen) | Layer 4/5 (out of scope) |
| `settings_version` | Placeholder | No | Yes | No | Internal | Migration guard |

---

## Action implications (observations only — not authorization)

1. **`house_system` UI honesty gap is the only action-required finding.** The
   dropdown and Save button imply the setting works when it does not. Either
   the selector should be made honest ("Placidus only") or the engine should be
   wired. This does not require any new setting or schema work.

2. All other settings with no UI control are non-urgent. They carry no honesty
   gap because users cannot interact with them.

3. `helper_layers` and `ontology_pack_id` could be reviewed for cleanup at a
   future settings-rationalization pass, but pose no current risk.

---

## Explicitly NOT done (rejected scope)

- No code changes.
- No schema changes.
- No engine wiring.
- No UI changes.
- No self-selected follow-up tasks.

---

## Result

VERIFIED (read-only; no files changed)
