# MAP-UX-0: Production Map vs Designed Map — Source Truth Audit

**Date:** 2026-06-20
**Type:** Audit only — no implementation authorized
**Read budget:** 4 files examined + structural scan

---

## 1. Map-related HTML/JS files in repo

### Production / wired

| File | Size | Route | Status |
|------|------|-------|--------|
| `map_CURRENT.html` | 259 KB | `/map_CURRENT.html` (production route) | **Active production map** |
| `genie_SANDBOX_variable_builder.html` | 8 KB | `/genie_SANDBOX_variable_builder.html` | Dev sandbox only |

### Design prototypes (not routed to production)

| File | Size | Last modified | Nature |
|------|------|---------------|--------|
| `prototype_genie_v1.html` | 26 KB | 2026-06-17 | Early motion concept |
| `prototype_genie_v2.html` | 38 KB | 2026-06-17 | Profile caret + Back/Forward + Save Search introduced |
| `prototype_genie_v3.html` | 40 KB | 2026-06-17 | Nameplate top-left, NOT/Mute/Solo per variable |
| `map_SANDBOX_genie_v4.html` | 44 KB | 2026-06-17 | Ghost strip + profile caret |
| `map_SANDBOX_genie_v5.html` | 50 KB | 2026-06-17 | Ghost tokens grid-aligned; Save pill morphs to disk |
| `map_SANDBOX_genie_v6.html` | 57 KB | 2026-06-17 | UI harmonization; centered city search |
| `map_SANDBOX_genie_v7.html` | 57 KB | 2026-06-17 | **Identical to v6 except title line** (title-only diff confirmed) |

**Note on v6/v7:** `diff` confirms the two files differ only in the `<title>` tag and the header comment label.
The **latest design is effectively `map_SANDBOX_genie_v6`**, with v7 being a title-renamed copy.

---

## 2. Production handoff

`app_shell.html` routes map navigation exclusively through `buildMapHandoffUrl()`, which resolves to:

```
/map_CURRENT.html?chartRecordId=…&profileId=…&genieRenderRef=…&handoff=app_shell
```

No genie sandbox (`v4`–`v7`) or prototype file is routed through the production handoff. The production map is unambiguously **`map_CURRENT.html`**.

---

## 3. Feature comparison: production map vs intended UX

### User-visible feature audit

| Feature | `map_CURRENT.html` (production) | `map_SANDBOX_genie_v7.html` (latest design) |
|---------|--------------------------------|---------------------------------------------|
| **Profile selector** | `<select id="chartProfile">` — functional, plain dropdown in side panel | `<div class="plate" id="plate">` — nameplate top-left of map canvas with name, birth date, caret |
| **Profile nameplate / caret** | No — select lives in a panel section | Yes — `.plate` at `left:16px; top:188px`; caret beside name |
| **Genie variable builder** | Via `genie_variable_builder.js` + `genie_map_engine_adapter.js` — real API, wired to backend | Self-contained inline JS — **mock overlays only** (`seededZones()` + random circles) |
| **Ghost variable tokens (Mute/Solo/Not)** | Stubs only — `[data-role="ghost-tools"]` selector in walkthrough JS; **no DOM element in production** | Yes — `.ghoststrip` with per-token NOT/Mute/Solo buttons; fully interactive in prototype |
| **Map search placement** | `<div id="rm-map-loc-search-mount">` in side panel (left rail) | Centered overlay `<div class="ov citysearch">` — floating above map, dissolves in explore mode |
| **History Back/Forward (`<>`)** | Stubs only — `[data-role="history-controls"]` in walkthrough; **no DOM element** | Yes — `<button class="navbtn back">` and `<button class="navbtn fwd">` in `.mapctrls` |
| **Pin** | Stub only — `[data-role="pin-control"]` in walkthrough; **no DOM element** | Yes — `<button class="navbtn pin">` in `.mapctrls` |
| **Save Search (disk / pill)** | `<button id="saveInvestigationBtn">Save Investigation</button>` — save-to-backend form in side panel | `<button class="save-inline" id="saveInline">Save search</button>` + floating `.save-disk` — morphing pill that flies to disk |
| **Topbar / hamburger in explore mode** | None — layout is fixed left panel + map | `.topbar` dissolves in explore mode; brand + hamburger float; `body.explore #map { top:0 }` |
| **Map Notes** | `data-role="map-notes"` stub in walkthrough only; notes field in Save Investigation form (wired to `/notes/saved-investigation`) | `.sp-notes` (contenteditable) in saved-search popover — prototype only |
| **Overlay engine** | Real: `genie_map_engine_adapter.js` → `/search-regions` API | Mock: `seededZones()` draws random circles; no real search regions |
| **Auth / Supabase** | Yes — `supabase_client.js`, `auth_guard.js`, RLS-protected APIs | No — standalone file, no auth, no API calls |
| **Profile intake** | Yes — `first_profile_intake.js` | No |
| **Saved-location search** | Yes — `saved_location_search_service.js`, `saved_location_search_ui.js` | No |

### Summary table

| Capability | Production | Design prototype |
|-----------|-----------|-----------------|
| Real chart overlays | ✅ | ❌ (mock) |
| Auth + RLS | ✅ | ❌ |
| Intake + profile wiring | ✅ | ❌ |
| Saved search backend | ✅ | ❌ |
| Profile nameplate (top-left) | ❌ | ✅ |
| Ghost strip (Mute/Solo/Not) | ❌ (stub selector) | ✅ |
| Centered map search | ❌ | ✅ |
| History controls (`<>`) | ❌ (stub selector) | ✅ |
| Pin control | ❌ (stub selector) | ✅ |
| Save-search pill/disk | ❌ | ✅ |
| Explore-mode dissolve topbar | ❌ | ✅ |

---

## 4. Classification of the intended map

**`map_SANDBOX_genie_v7.html` (= v6) is a UX prototype-only file.**

| Criterion | Assessment |
|-----------|------------|
| Production-ready? | **No** — mock overlays, no auth, no real API calls, no Supabase integration |
| Prototype-only? | **Yes** — intended as design specification, not a production candidate |
| Partially wired? | **No** — self-contained; entirely disconnected from backend |
| Stale / unsafe to deploy? | **Unsafe to deploy directly** — would appear to work but show random fake overlays; no auth guard |

---

## 5. What `map_CURRENT.html` is missing (gap vs intended UX)

These are the controls the user reported as absent — confirmed missing from production:

1. **Profile nameplate** — top-left `.plate` with name, birth metadata, caret; production has only a `<select>` in the side panel
2. **Ghost strip (Mute/Solo/Not)** — no DOM element; only a stub selector in the walkthrough controller added in ONBOARDING-2A1
3. **History controls (`< >`)** — no DOM element in production; stub selector only
4. **Pin control** — no DOM element in production; stub selector only
5. **Centered map search** — lives in the side panel, not floating over the map
6. **Explore mode / dissolve topbar** — no mode transition in production
7. **Save Search pill/disk** — production has a form-based "Save Investigation"; no morphing pill UI

---

## 6. Recommended next slice

### Option comparison

| Option | Description | Risk | Effort |
|--------|-------------|------|--------|
| **A. Repoint production handoff** | Swap `/map_CURRENT.html` with `map_SANDBOX_genie_v7.html` | **High** — would break auth, real overlays, intake, saved search | Very low (one route change), but immediately broken |
| **B. Migrate controls into `map_CURRENT.html`** | Port the intended UX chrome (nameplate, ghost strip, history, pin, centered search, explore mode) into the production file | Medium | Medium-Large: each control must be wired to real data |
| **C. Create a new production map shell** | Build `map_PRODUCTION_v2.html` starting from `map_CURRENT.html` production logic + v7 design chrome | Medium | Large |
| **D. Keep legacy map and defer onboarding** | No UX changes; walkthrough stubs remain stubs | Low | None |

### Recommendation: **Option B — migrate controls incrementally into `map_CURRENT.html`**

Rationale:
- `map_CURRENT.html` is the only file with real overlay rendering, auth, intake, and saved-location search wired and tested
- The prototype (`v7`) is pure UI chrome — its controls can be extracted one at a time
- The walkthrough stubs already define the exact selectors each control should use (`[data-role="ghost-tools"]`, `[data-role="history-controls"]`, `[data-role="pin-control"]`)
- Each control can be added as a visible-but-non-functional stub first, then wired, without touching the rendering engine

### Suggested slice order for Option B

| Slice | Control | Work |
|-------|---------|------|
| MAP-UX-1 | Profile nameplate (`.plate` top-left; swap select → plate with caret) | Moderate — must wire to `#chartProfile` value |
| MAP-UX-2 | History controls (`<>`) | Small — state already tracked; needs DOM + wiring |
| MAP-UX-3 | Pin control | Small — state concept exists; needs DOM + persistence |
| MAP-UX-4 | Ghost strip (Mute/Solo/Not per variable) | Large — requires Genie variable state integration |
| MAP-UX-5 | Centered map search + explore mode | Moderate — CSS layout shift; search already functional |
| MAP-UX-6 | Save Search pill morphing to disk | Small UX — functional backend already exists |

---

## Explicit non-goals (this audit)

- No implementation of any listed controls
- No changes to production routes or handoff
- No migration of overlay engine from mock to real
- No commits to `map_CURRENT.html` or `app_shell.html`
