# Genie → App Shell Handoff Audit v1

## Status

**AUDIT ONLY** — read-only gap analysis. No redesign, no implementation.

**Partially superseded:** commit `9e448e0` added hook-only map execution (`__rmExecuteGenieRender`). Sections on **app shell handoff** and **Genie → shell transport** remain accurate. Sections claiming map has **no** Genie path are updated below.

**Date:** 2026-05-30  
**Scope:** What Genie emits today, what app shell and map expect today, and what adapter/transport is required to connect them.

**Sources read:**

- `docs/contracts/genie_render_payload_v1_2026-05-30.md`
- `docs/contracts/variable_card_language_v1_2026-05-30.md`
- `genie_SANDBOX_variable_builder.html`
- `app_shell.html`
- `map_CURRENT.html`
- `scripts/smoke_app_shell_map_handoff.py`

---

## Executive summary

Genie (sandbox) **emits a full `genie_render` payload in memory** on Search Map. App shell **transports navigation context only** via Map Handoff Contract v1 URL params.

**Three distinct states (do not conflate):**

| State | Status |
|-------|--------|
| **a) Sandbox payload exists** | ✅ `genie_render` v1 emitted in sandbox |
| **b) Map hook can execute `genie_render`** | ✅ `window.__rmExecuteGenieRender(payload)` + `genie_map_engine_adapter.js` (commit `9e448e0`); reads `variables[]` only; no auto-execute on load |
| **c) App shell handoff delivers `genie_render`** | ❌ Not implemented |

Map **default user path** still uses legacy DOM (Find regions). App shell handoff is **receive-only context** — no Genie payload.

There is **zero wired handoff** between Genie and app shell, or between shell navigation and automatic Genie search on map load. `legacyCompatibility` is emitted for diagnostics; map engine adapter **must not** use it as execution input.

**Recommended transport for Web 2.0 (unchanged):** keep **nav context in URL** (v1) and add a **payload reference + same-origin side channel** (e.g. `genieRenderRef` query param + `sessionStorage`). Do **not** put the full payload in the URL.

---

## A. Current Genie contract

### Emitter

`genie_SANDBOX_variable_builder.html` — standalone sandbox, not embedded in app shell.

### Trigger

Primary action **Search Map** (`#renderBtn`) calls `normalizePayload()` when all cards are complete. No backend call, no navigation, no `postMessage`, no `sessionStorage`.

### Payload shape (as implemented)

Aligns with Genie Render Payload Contract v1, with one sandbox extension:

```json
{
  "schema_version": 1,
  "kind": "genie_render",
  "createdAt": "<ISO-8601>",
  "chartRecordId": "sandbox-chart-record",
  "variables": [ /* Variable[] */ ],
  "layerControls": {
    "mutedVariableIds": [],
    "soloVariableId": null,
    "excludeVariableIds": []
  },
  "settingsSnapshot": {
    "transitModeEnabled": false,
    "registry": { /* category → id → enabled */ },
    "cardLanguage": { /* language registry snapshot — extension beyond bare contract */ }
  },
  "legacyCompatibility": {
    "schema_version": 1,
    "kind": "saved_investigation",
    "chart_id": "sandbox-chart-record",
    "house_conditions": [ /* max 3, slots A/B/C */ ],
    "angle_sign_conditions": [ /* max 1 */ ],
    "aspect_overlay": { /* max 1 */ } | null,
    "aspect_overlays": [ /* all include aspects — sandbox extra */ ],
    "notExclusions": [ /* polarity exclude vars */ ],
    "degradation": {
      "canonicalVariableCount": 0,
      "legacyMappedCount": 0,
      "unmappedVariableIds": [],
      "warnings": []
    }
  }
}
```

### Variable semantics (canonical)

| Concern | Behavior |
|---------|----------|
| Types | `planet_in_house`, `angle_in_sign`, `aspect_to_angle`, transit types (gated) |
| Polarity | `include` \| `exclude` (NOT is not a type) |
| Field names | Canonical `body` / `transitBody`; legacy adapter maps to `planet` |
| Labels | Registry type labels (e.g. `Planet · House`), not field sentences |
| Search truth | `complete` and `experimental` variables with `enabled: true` |
| Layer controls | Mute/solo in `layerControls` only; exclude also in `excludeVariableIds` |

### Output destinations today

- In-memory `lastNormalizedPayload`
- Debug JSON panel (`#renderJson`)
- `console.info`
- Hooks: `window.__rmGenieSandbox.normalizePayload()`, `getState()`, `getCardLanguageRegistry()`

### Not emitted / not connected

- No `renderId` / persistence key
- No handoff URL, shell navigation, or automatic map invocation from sandbox Search Map
- `chartRecordId` is a sandbox stub, not store-backed
- Sandbox does **not** call `__rmExecuteGenieRender` (map hook is separate; smoke-only / programmatic today)

---

## B. Current app shell contract

### Navigation context (in-app)

Hash route + query params via `ROUTE_CONTEXT_CONTRACT` and `NAV_CONTEXT_KEYS`:

| Key | Role |
|-----|------|
| `chartRecordId` | Required on `#/map` route |
| `placeId` | Optional (favorite / place-centered entry) |
| `explorationId` | Optional |
| `comparisonSetId` | Optional on other routes; none on map route |

Encoded in `#/{route}?{params}`; `returnTo` is pipe-delimited stack encoding.

### Map Handoff Contract v1 (shell → map)

Defined in `app_shell.html` as `MAP_HANDOFF_CONTRACT`:

| Property | Value |
|----------|-------|
| Strategy | `url-query-params` only |
| Marker | `handoff=app_shell` |
| Fields | `chartRecordId`, `placeId`, `explorationId`, `comparisonSetId`, `returnTo`, `handoffCreatedAt` |
| Also set | `skipOnboarding=1` |

`buildMapHandoffUrl(navContext)` → `/map_CURRENT.html?...`

### Genie in shell today

Screen 2 map route shows a **placeholder** genie-drawer: disabled add-condition buttons, no variable builder, no Search Map, **no payload emission**. Production map link uses context handoff v1 only.

### Shell exports

`window.__rmAppShell.buildMapHandoffUrl()`, `MAP_HANDOFF_CONTRACT`, `navContext`, store-backed chart record ids (e.g. `cr-anna-rivera`).

### Smoke coverage

`scripts/smoke_app_shell_map_handoff.py` — shell builds URL, map receives context, **no renderer/profile/viewport mutations**. **No Genie payload assertions.**

---

## C. Current map contract

### App shell handoff (receive-only)

`readAppShellHandoff()` when `handoff=app_shell`:

```javascript
{
  source: "app_shell",
  chartRecordId, placeId, explorationId,
  comparisonSetId, returnTo, handoffCreatedAt
}
```

- Rendered in dev panel `#appShellHandoff`
- Hook: `window.__rmAppShellHandoff()`
- **Explicitly does not** change chart profile, viewport, search form, or trigger Find regions

### Search / render truth (default user path)

`findRegions()` → `buildPlanFromLegacyDom()` → `executeSearchPlan()` — reads **DOM selects**:

- `planetA` / `houseA` (required for first condition)
- Optional `planetB`/`houseC`, `planetC`/`houseC`
- `getSelectedAngleSignCondition()` → one angle-in-sign
- `getSelectedAspectOverlay()` → one aspect-to-angle

Builds backend payload with `house_conditions`, `angle_sign_conditions`; **does not send `notExclusions`**.

### Saved investigation replay (library only)

`applySavedInvestigationConditions(view)` hydrates DOM from saved view `conditions[0]`:

- `house_conditions[]` with slots A/B/C
- `angle_sign_conditions[0]`
- `aspect_overlay`

**Does not apply `notExclusions`.** Used when library saved-view replay runs (`applyLibrarySavedViewReplay`), not from app shell handoff.

### `collectSavedInvestigationConditions()`

Legacy collector for library save — same A/B/C + single angle + single aspect shape; **no `notExclusions`**.

### Chart identity on map

`#chartProfile` dropdown — built-in astro profiles + library charts. IDs are **not** the same namespace as shell `chartRecordId` (store client records). App shell handoff `chartRecordId` is **not** applied to `#chartProfile`.

### Viewport

Default center/zoom on load. Library handoff can restore viewport from saved view; **app shell handoff does not** carry or apply viewport. `placeId` from shell handoff is **not** used to center the map.

### Genie execution (hook-only — commit `9e448e0`)

**Exists:** `window.__rmExecuteGenieRender(payload)` → `genie_map_engine_adapter.js` → `executeSearchPlan()`.

| Property | Value |
|----------|-------|
| Input | Full `genie_render` object (caller-supplied) |
| Adapter reads | `variables[]` **only** — not `legacyCompatibility` |
| Auto-execute on load | **No** |
| App shell handoff trigger | **No** — no `genieRenderRef` reader |
| DOM hydration | **No** — does not write A/B/C controls |
| Dev panel | `#genieRenderStatus` after explicit hook call |
| Smoke | `scripts/smoke_genie_map_engine.py` |

**Does not exist:** handoff-delivered payload, shell-embedded Genie Search Map, or map load auto-search from Genie.

### Genie handoff consumption

**None via URL/handoff.** No `genieRenderRef`, no `sessionStorage` reader on map load, no `legacyCompatibility` execution path.

---

## D. Mismatches

| # | Genie / contract | App shell | Map | Severity |
|---|------------------|-----------|-----|----------|
| 1 | Emits full `genie_render` | Transports no render payload | Hook executes payload when called; handoff delivers no payload | **Blocking** — no product handoff |
| 2 | Sandbox standalone HTML | Genie drawer is UI stub | N/A | **Blocking** — not co-located |
| 3 | `chartRecordId` from active record | Store ids (`cr-anna-rivera`) | `#chartProfile` profile/library ids; hook ignores payload `chartRecordId` | **High** — no mapping |
| 4 | `legacyCompatibility` with degradation | Not transported | Map engine adapter ignores for execution; legacy DOM path ignores degradation | **Medium** — only if legacy DOM path used |
| 5 | `notExclusions[]` in payload | N/A | Engine adapter defers exclude; findRegions never sends exclusions | **High** — exclude not in engine v1 |
| 6 | `variables[]` canonical truth | N/A | Hook path supports unlimited houses; legacy DOM still A/B/C capped | **Medium** — split by path |
| 7 | `layerControls` mute/solo | N/A | No replay UI for handoff or hook path | **Low** for Web 2.0 search slice |
| 8 | `settingsSnapshot.registry` | N/A | Map uses static profile + select options on legacy path | **Medium** — registry honesty not replayed |
| 9 | Search Map → render | Shell link says “Open production map” with context only | Hook requires explicit call; no auto-search from Genie | **Blocking** — no product wiring |
| 10 | `placeId` optional context | Handoff includes `placeId` | Not applied to map center | **Medium** — favorite entry incomplete |
| 11 | `aspect_overlays` (all) in sandbox legacy bundle | N/A | Engine adapter: first aspect only; rest degraded | **Low** — by design in v1 |
| ~~12~~ | ~~Contract doc: sandbox pre-v1~~ | — | — | **Closed** — sandbox emits v1 |

---

## E. Required adapter

Three layers are required for **product handoff**. Layer **E3 execute** partially exists as hook-only path (commit `9e448e0`).

### E1. Genie → shell capture

**Role:** On Search Map, freeze `normalizePayload()` and pass to shell transport.

**Inputs:** Live Genie editor state, active `chartRecordId` from shell `navContext` (replace sandbox stub).

**Outputs:** Full `genie_render` object + ephemeral `renderRef` (uuid or timestamp id).

**Not required:** Reshape canonical payload; Genie already builds `legacyCompatibility`.

### E2. Shell → map transport

**Role:** Combine existing nav context handoff with render payload delivery.

**Recommended pattern:**

| Channel | Carries |
|---------|---------|
| URL query (extend v1) | Existing context fields + `genieRenderRef` (+ optional `handoff=app_shell` marker) |
| Same-origin side channel | Full `genie_render` JSON at `sessionStorage['rm_genie_render:' + renderRef]` |

**Avoid:** Full payload in URL (size, encoding, degradation visibility).

**Defer:** Viewport in handoff unless explicitly scoped (library path already owns viewport separately).

### E3. Map receive → apply → search

**Hook-only execute (done — commit `9e448e0`):**

- `__rmExecuteGenieRender(payload)` validates and runs via `genie_map_engine_adapter.js`
- Reads `variables[]` only; honest degradation for exclude, transit, overflow aspects
- Proven by `smoke_genie_map_engine.py` (including wire-level four-house proof)
- **Not** triggered by handoff or map load

**Still required for product handoff:**

- Read `genieRenderRef`, load payload from side channel
- Expose `window.__rmGenieRenderHandoff()` / dev panel (optional; hook summary exists today)
- Optional auto-execute on load (behind explicit flag; conflicts with receive-only v1 smoke until extended)

**Legacy DOM apply (superseded as architecture — do not build):**

~~Project `legacyCompatibility` onto DOM~~ — canonical path is `variables[]` → map engine adapter. Legacy DOM remains compatibility-only for manual Find regions.

**Still open:**

1. Map `chartRecordId` → `#chartProfile` option (requires id mapping — **undefined today**).
2. Surface degradation in product UI (dev panel exists for hook path).
3. **Separate engine contract** for exclude polarity — adapter defers honestly today.
4. Handoff transport (E1 + E2) — still blocking product path.

### Transport decision (question 5)

| Option | Verdict |
|--------|---------|
| Full `genie_render` in URL | **Reject** — too large, fragile |
| Payload reference only | **Insufficient alone** — map needs context ids + payload body |
| Payload + viewport | **Defer** — not part of Genie Search Map; conflicts with receive-only v1 smoke |
| **Nav context (URL) + full payload (side channel via ref)** | **Recommend** — preserves v1 smoke semantics, carries canonical truth |

---

## F. Recommended integration sequence

Minimal, incremental — no production map rewrite in step 1.

### Step 0 — Document (this audit)

Gap analysis only. ✅

### Step 1 — Genie Handoff Contract v2 (doc)

Extend Map Handoff v1 with `genieRenderRef`, side-channel storage rules, TTL, failure modes (ref missing → map shows warning, no silent search).

### Step 2 — Shell wiring (sandbox-in-drawer or linked sandbox)

- Embed/port `genie_SANDBOX_variable_builder.html` into shell map screen genie-drawer
- Bind `chartRecordId` from `navContext`
- On Search Map: write side channel + open/build handoff URL with `genieRenderRef`

### Step 3 — Map engine hook (canonical execute) ✅

**Done (commit `9e448e0`):** `genie_map_engine_adapter.js`, `__rmExecuteGenieRender`, `smoke_genie_map_engine.py`.

### Step 4 — Handoff receive + optional auto-execute

- Read `genieRenderRef` from URL + side channel on map load
- Extend `smoke_app_shell_map_handoff.py` when scoped
- Auto-execute behind explicit flag

### Step 5 — chartRecordId ↔ chartProfile bridge

- Store or mapping layer so handoff record selects correct map profile

### Step 6 — Exclude / transit engine semantics

- Out of Web 2.0 minimum; adapter defers honestly today

### Minimum Web 2.0 integration slice (next)

**Steps 1–2 + 4** (Step 3 done):

1. Contract doc for ref + side channel  
2. Shell captures Genie render and builds extended handoff URL  
3. ~~Map engine hook~~ ✅ (commit `9e448e0`)  
4. Map reads handoff ref and executes (or receive-only first)

Product path proves **Genie → shell → map transport**. Canonical execute path already exists via hook.

---

## G. Explicitly out of scope

- Redesigning Genie UX, app shell routes, or map workspace layout
- Full canonical renderer consuming unlimited `variables[]`
- `notExclusions` engine semantics on map
- Viewport / pin / save / history persistence
- Store v3, Supabase, backend classify API changes
- AI interpretation or natural-language Genie
- Transit search on production map
- Replacing Map Handoff v1 context fields
- ~~Modifying `map_CURRENT.html` or `app_shell.html` as part of this audit~~ — map modified post-audit (commit `9e448e0`); shell unchanged
- Committing or implementing adapter code (audit deliverable is this document only)

---

## Cross-reference

| Artifact | Handoff role today |
|----------|-------------------|
| `genie_render_payload_v1` | Defines emit shape; handoff transport explicitly out of scope there |
| `variable_card_language_v1` | UI copy only; `settingsSnapshot.cardLanguage` snapshot in sandbox |
| `genie_map_engine_adapter.js` | Map execute adapter; `variables[]` only (commit `9e448e0`) |
| `MAP_HANDOFF_CONTRACT` v1 | Nav context URL only |
| `smoke_app_shell_map_handoff.py` | Proves context receive-only; template for Genie handoff smoke |
| `smoke_genie_sandbox.py` | Proves sandbox payload; no shell/map leg |
| `smoke_genie_map_engine.py` | Proves hook-only map execute; no handoff leg |

---

*End of audit — ~4 pages.*
