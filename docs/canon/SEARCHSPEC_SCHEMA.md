# SearchSpec Schema

**Status:** Canonical architecture doctrine — not active Beta implementation  
**Date:** 2026-06-27  
**Mode:** Documentation only — no code, no migrations, no UI changes  
**Authority:** Subordinate to [`FOUNDATIONAL_CONSTITUTION.md`](../constitutional/FOUNDATIONAL_CONSTITUTION.md)  
**Companions:** [`AI_RUNTIME_ARCHITECTURE.md`](AI_RUNTIME_ARCHITECTURE.md) · [`INTENT_TRANSLATION_ENGINE.md`](INTENT_TRANSLATION_ENGINE.md) · [`AI_INTERACTION_SURFACES.md`](AI_INTERACTION_SURFACES.md) · [`WEB3_AI_IMPLEMENTATION_ROADMAP.md`](../roadmaps/WEB3_AI_IMPLEMENTATION_ROADMAP.md)

> **Promotion rule:** This document defines the SearchSpec contract. Nothing here becomes active until explicitly promoted into an implementation plan with scope, migration plan, validation gate, and rollback path. The Web2 instrument remains sovereign.

> **Overlay-first hard rule:** SearchSpec primary output is **overlay branches, map overlay configurations, viable geographic regions, and shareable overlay sets** — **not candidate city lists**. Users and professionals explore the map and choose places. Cities enter the system only after the user pins or selects a place, a saved comparison already contains cities, the user explicitly asks about a selected city, City Intelligence is requested for selected places, or a professional explicitly invokes a later optional city-helper mode.

---

## §0 Purpose

SearchSpec is the **overlay-first contract** between the conversation layer (Navigator or Astro Assist) and the execution layer (Engine). It serializes astrological search intent as structured map-search strategy — not as a city-query.

| Party | Role |
|-------|------|
| **Navigator** | Produces SearchSpec from consultation evidence via Intent Translation Engine |
| **Astro Assist** | Produces SearchSpec directly from professional technical criteria (same schema) |
| **Engine** | Consumes SearchSpec; returns overlay branches and geographic conditions |
| **Genie/Map Adapter** | Consumes confirmed SearchSpec; launches overlays first, then optional saved-search handoff |
| **Guardian** | Reviews user-facing explanations of SearchSpec results before display |

SearchSpec does not speak to users. Navigator and Astro Assist translate it into language. The Engine executes it. The map shows it.

---

## §1 Engine output contract

When the Engine executes a SearchSpec, it returns **per branch variant**:

| Output | Description |
|--------|-------------|
| `overlay_branches` | Named overlay branches (planet/house/angle/aspect conditions rendered as map overlays) |
| `viable_geographic_regions` | Geographic areas where branch conditions overlap — regions, not city lists |
| `map_overlay_configuration` | Parameters to render overlays on the Web2 map instrument |
| `shareable_overlay_set` | Serializable overlay configuration the professional may send to a client ("explore this highlighted region") |
| `strategy_variant_label` | Named category for the branch (e.g., "Creative Recognition path," "Mastery path") — not a raw score |
| `transparency_notes` | What was tried, substituted, or traded off |
| `partial_match_disclosure` | When exact conditions cannot be satisfied in geography |

**Cities are not default Engine output.** A `selected_place_analysis` block may appear only when `city_helper_mode` is explicitly set (§3.14) and places are already user-selected or comparison-bound.

---

## §2 SearchSpec object — top-level shape

```
SearchSpec
  spec_identity              -- §3.1
  manifest_pinning           -- §3.2
  source_context             -- §3.3
  desired_conditions         -- §3.4
  avoids_and_exclusions      -- §3.5
  soft_preferences           -- §3.6
  geographic_bounds          -- §3.7
  birth_time_uncertainty     -- §3.8
  branch_variants            -- §3.9
  tradeoff_scan              -- §3.10
  optimization_carving       -- §3.11
  recalculate_more           -- §3.12
  handoffs                   -- §3.13
  city_helper_mode           -- §3.14 (optional; explicit only)
  user_confirmation          -- §3.15
  audit_transparency         -- §3.16
```

---

## §3 Field definitions

### §3.1 Spec identity / version

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `spec_id` | string (UUID) | yes | Stable ID for this spec instance |
| `spec_version` | string (semver) | yes | Schema version (e.g., `1.0.0`) |
| `spec_schema_id` | string | yes | Canonical schema identifier (`searchspec.overlay_first.v1`) |
| `parent_spec_id` | string (UUID) | no | When this spec supersedes a prior spec (never in-place mutation) |
| `created_at` | ISO 8601 | yes | Creation timestamp |
| `updated_at` | ISO 8601 | yes | Last metadata update (body immutable after confirmation) |
| `status` | enum | yes | `draft` \| `proposed` \| `confirmed` \| `superseded` \| `archived` |

**Versioning rule:** Any material change after `user_confirmation.confirmed_at` is set creates a **new** `spec_id` with `parent_spec_id` pointing to the prior spec. Confirmed specs are never modified in place.

---

### §3.2 Manifest pinning

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `manifest_id` | string | yes | Layer 2 manifest pinned to this spec |
| `manifest_version` | string | yes | Manifest version at time of spec creation |
| `model_resolver_snapshot` | object | no | Optional resolver cache key for reproducibility |

Every consultation session and every Engine run must be reproducible against the same manifest. Search logic grounded in Layer 2 may use **Approved** entries only.

---

### §3.3 Source surface / context

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `produced_by` | enum | yes | `navigator` \| `astro_assist` \| `genie_refinement` \| `saved_search_reload` |
| `surface_id` | string | yes | Originating surface (`intake`, `map_pinwheel`, `genie`, `astro_assist`, etc.) |
| `consultation_id` | string | no | Active AI consultation session |
| `session_id` | string | yes | Application session |
| `profile_id` | string | yes | Active chart/profile |
| `intent_snapshot` | object | no | Frozen excerpt of Consultation Canon at spec creation |
| `viewport_context` | object | no | Map viewport when spec originated from map (`center`, `zoom`, `active_overlays`) |
| `selected_places` | array | no | User-selected or pinned places already in scope (downstream analysis only) |

---

### §3.4 Desired conditions

Primary astrological targets the Engine must satisfy as overlay branches.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `desired_conditions` | array | yes | List of condition objects |

**Condition object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `condition_id` | string | yes | Stable ID within this spec |
| `subject` | object | yes | `{ type: planet \| angle \| point, name: string }` |
| `target` | object | yes | `{ type: house \| angle \| aspect, value: string \| number, orb_deg?: number }` |
| `weight` | enum | yes | `required` \| `strong` \| `moderate` \| `weak` |
| `layer2_entry_ref` | string | no | Approved Layer 2 entry ID grounding this condition |
| `rationale` | string | no | Human-readable why (audit; not user-facing by default) |

Desired conditions compile to **map overlay strategies**, not city filters.

---

### §3.5 Avoids / exclusions / NOT conditions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hard_avoids` | array | no | Conditions that **exclude** a geographic region from a branch |
| `soft_avoids` | array | no | Conditions to minimize; disclosed in tradeoff scan |
| `not_conditions` | array | no | Explicit NOT logic (e.g., NOT Saturn in 4th) |

**Avoid object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `subject` | object | yes | Planet/angle/point |
| `target` | object | yes | House/angle/aspect |
| `reason` | string | no | Why this is excluded (transparency) |
| `severity` | enum | yes | `disqualifying` \| `strong_penalty` \| `preference_against` |

---

### §3.6 Soft preferences

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `soft_preferences` | array | no | List of preference objects |

**Preference object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | yes | Plain-language preference |
| `weight` | number | yes | Internal weight only (0.0–1.0); **never shown to users** |
| `linked_condition_id` | string | no | Optional link to a `desired_conditions` entry |

---

### §3.7 Geographic bounds

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `geographic_bounds` | object | no | Bounding object |

**Geographic bounds object:**

| Field | Type | Description |
|-------|------|-------------|
| `include_regions` | string[] | ISO region/country codes or named regions |
| `exclude_regions` | string[] | Regions to exclude |
| `max_distance_km` | object | `{ from_place_id, km }` |
| `min_distance_km` | object | `{ from_place_id, km }` |
| `bounding_box` | object | `{ north, south, east, west }` |
| `climate_filters` | object | **Schema present; execution deferred in v1** |

Geographic bounds constrain **where overlays are evaluated**, not which cities are returned.

---

### §3.8 Birth-time uncertainty / range support

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `birth_time_uncertainty` | object | yes | Uncertainty declaration |

**Birth-time uncertainty object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `certainty_level` | enum | yes | `exact` \| `range` \| `unknown` |
| `range_start` | string (time) | if range | Earliest plausible birth time |
| `range_end` | string (time) | if range | Latest plausible birth time |
| `evaluation_mode` | enum | yes | `point` \| `range_union` \| `range_intersection` |
| `disclosure_required` | boolean | yes | When true, Engine must surface uncertainty in transparency notes |

When `certainty_level` is `range` or `unknown`, overlay branches may widen or split. The Engine must disclose which house cusp ambiguity affected results.

---

### §3.9 Branch variants

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `branch_variants` | array | yes | At least one variant (even in draft) |
| `request_alternatives` | boolean | no | When true, Engine returns multiple named variants |

**Branch variant object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `variant_id` | string | yes | Stable ID (e.g., `branch_a`, `branch_b`) |
| `variant_label` | string | yes | User-facing name (e.g., "Ideal path," "A2A workaround") |
| `variant_description` | string | no | Short explanation of this branch's strategy |
| `condition_set` | string[] | yes | List of `condition_id` values active in this branch |
| `substitutions_applied` | array | no | What was substituted vs. ideal conditions |
| `is_partial_match` | boolean | no | True when geography cannot satisfy all required conditions |
| `overlay_style` | object | no | Map rendering hints (colors, opacity, layer grouping) |

**Proposed limit:** Up to 4 named variants per Engine run when `request_alternatives` is true.

---

### §3.10 Tradeoff scan fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tradeoff_scan` | object | no | Tradeoff analysis block |

**Tradeoff scan object:**

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | When true, Engine produces per-branch tradeoff summaries |
| `branches` | array | Per-variant `{ variant_id, gains[], gives_up[], tension_notes[] }` |
| `cross_branch_tensions` | array | Tensions between variants |
| `user_intention_alignment` | object | Optional mapping to Consultation Canon intention fields |

Tradeoff scan supports narrative explanation. It does not produce city rankings.

---

### §3.11 Optimization / carving fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `optimization_carving` | object | no | Explicit optimization state |

**Optimization carving object:**

| Field | Type | Description |
|-------|------|-------------|
| `carve_from_variant_id` | string | Which branch is being refined |
| `tightened_conditions` | array | Conditions added or strengthened |
| `relaxed_conditions` | array | Conditions loosened (must be disclosed) |
| `carve_rationale` | string | Why this carve was applied |
| `iteration` | number | Carve pass number |
| `user_requested` | boolean | True only when user or professional explicitly asked to carve |

Every carve creates audit entries. Optimization that changes confirmed specs requires a new `spec_id`.

---

### §3.12 Recalculate more

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `recalculate_more` | object | no | Recalculation request |

**Recalculate more object:**

| Field | Type | Description |
|-------|------|-------------|
| `requested` | boolean | User or professional asked for more variants |
| `exclude_variant_ids` | string[] | Variants already shown |
| `focus_hint` | string | Optional steer |
| `max_additional_variants` | number | Cap on new branches (proposed default: 2) |

Recalculate more produces a **new spec** or appends to a draft spec only. It never silently replaces a confirmed spec.

---

### §3.13 Handoffs — Genie / map / saved search

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `handoffs` | object | no | Handoff configuration |

**Handoffs object:**

| Field | Type | Description |
|-------|------|-------------|
| `map_overlay_launch` | object | **Primary default handoff** |
| `genie_launch` | object | Optional Genie session pre-population |
| `saved_search_handoff` | object | Optional saved search creation |

**`map_overlay_launch`:**

| Field | Type | Description |
|-------|------|-------------|
| `trigger` | enum | `on_confirm` \| `on_user_request` \| `manual` |
| `overlay_params` | object | Layer IDs, opacity, branch variant to render |
| `fit_bounds` | boolean | Whether map should zoom to viable region |
| `shareable` | boolean | Whether overlay set can be exported/shared (Astro Assist) |

**`genie_launch`:**

| Field | Type | Description |
|-------|------|-------------|
| `trigger` | enum | `on_confirm` \| `on_user_request` |
| `context_summary` | string | User-readable summary (not raw SearchSpec JSON) |
| `refine_from_variant_id` | string | Which branch Genie opens on |

**`saved_search_handoff`:**

| Field | Type | Description |
|-------|------|-------------|
| `trigger` | enum | `on_user_request` only — never automatic |
| `name_suggestion` | string | Proposed saved search name |
| `description_suggestion` | string | Proposed description |
| `persist_overlay_state` | boolean | Whether saved search stores overlay configuration |

**Handoff order (mandatory):** map overlay launch → Genie launch (if requested) → saved search creation (if user confirms).

---

### §3.14 City helper mode (optional — explicit only)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `city_helper_mode` | object | no | Only when explicitly invoked |

**City helper mode object:**

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Must be `true` and explicitly set |
| `invoked_by` | enum | `professional` \| `user` |
| `scope` | enum | `within_confirmed_region` \| `within_selected_places` |
| `place_ids` | string[] | User-selected places or comparison cities already in scope |
| `purpose` | string | e.g., "name major cities in highlighted region for client handoff" |

When `city_helper_mode.enabled` is false or absent, the Engine **must not** return city lists.

---

### §3.15 User confirmation state

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_confirmation` | object | no | Absent until confirmed |

**User confirmation object:**

| Field | Type | Description |
|-------|------|-------------|
| `confirmed_at` | ISO 8601 | When confirmation occurred |
| `confirmed_by` | enum | `user` \| `professional` |
| `approved_variant_id` | string | Which `branch_variants[].variant_id` was selected |
| `confirmation_method` | enum | `explicit_button` \| `verbal_ack_in_session` \| `professional_override` |
| `summary_acknowledged` | string | Last summary the confirmer agreed was accurate |

After `confirmed_at` is set: `status` becomes `confirmed`, spec body is **immutable**, further changes require new `spec_id`.

---

### §3.16 Audit / transparency notes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audit_transparency` | object | yes | Transparency block |

**Audit transparency object:**

| Field | Type | Description |
|-------|------|-------------|
| `what_tried` | string[] | Conditions or strategies attempted |
| `what_worked` | string[] | What satisfied the spec |
| `what_substituted` | array | `{ from, to, reason }` substitution log |
| `tradeoff_introduced` | string[] | Tradeoffs explicitly introduced |
| `partial_matches` | array | Regions/branches with subset satisfaction |
| `birth_time_impact` | string | How uncertainty affected results |
| `engine_run_id` | string | Engine execution ID for replay |
| `guardian_review_ids` | string[] | Guardian decisions on related user-facing output |

---

## §4 Astro Assist — same schema, different entry path

Astro Assist uses the **identical SearchSpec schema**. The difference is how the spec is produced:

| Dimension | Navigator | Astro Assist |
|-----------|-----------|--------------|
| Entry path | Built through consultation and Intent Translation Engine | Produced directly from professional technical criteria |
| `produced_by` | `navigator` | `astro_assist` |
| Clarification loop | Progressive, educational | Minimal; professional supplies explicit conditions |
| Default output | Overlay strategies for map exploration | Shareable overlay map configurations for client handoff |
| City lists | Never default | Only when `city_helper_mode` explicitly enabled |

**Professional workflow:**

1. Professional sets `desired_conditions` and `geographic_bounds` directly.
2. Engine returns overlay branches and `shareable_overlay_set`.
3. Professional sends overlay map to client: "Choose locations in this highlighted region."
4. Client pins/selects places on the map.
5. City Intelligence runs **downstream** on selected places only.

---

## §5 Explicit prohibitions

| Prohibited | Reason |
|------------|--------|
| **City ranking** | Hidden ranking; FOUNDATIONAL_CONSTITUTION.md §0.1 |
| **City lists as default output** | Overlay-first doctrine |
| **Raw scores shown to users** | Users see named strategy categories only |
| **Hidden optimization** | All carving in `optimization_carving` and `audit_transparency` |
| **Modifying confirmed specs in place** | Immutability after `user_confirmation.confirmed_at` |
| **Treating SearchSpec as a city-query mechanism** | Primary output is map overlay configuration |
| **Auto-selecting `approved_variant_id`** | User or professional must confirm |
| **Executing `climate_filters` in v1** | Schema present; execution deferred |
| **Using Draft Layer 2 entries** | Production requires Approved entries only |
| **Bypassing Guardian for result explanation** | All user-facing output reviewed before display |

---

## §6 Lifecycle

```
draft → proposed → confirmed → map_overlay_launch (primary)
                      │
                      └── new spec (parent_spec_id) on material change → prior: superseded
```

**City Intelligence** attaches only after `selected_places` exist — from map pins, comparison, or explicit `city_helper_mode`.

---

## §7 Relationship to other canons

| Document | Relationship |
|----------|--------------|
| INTENT_TRANSLATION_ENGINE.md | Produces SearchSpec fields from translation pipeline (§13 defers to this document) |
| AI_RUNTIME_ARCHITECTURE.md §2.6 | Runtime summary; this document is the authoritative schema |
| WEB3_AI_IMPLEMENTATION_ROADMAP.md Track 4 | Implementation track |
| AI_INTERACTION_SURFACES.md | Surfaces pass `source_context`; handoffs respect overlay-first order |

---

## §8 Open questions (deferred)

| Question | Status |
|----------|--------|
| JSON Schema artifact (`searchspec.overlay_first.v1.json`) | Deferred to Track 4 implementation |
| Maximum branch variants per run | Proposed: 4 |
| `climate_filters` execution | Deferred |

---

*Planning complete. Documentation only. No code changes. No database migrations. No production AI active.*
