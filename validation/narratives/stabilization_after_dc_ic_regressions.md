# Stabilization pass after DC/IC sprint regressions

**Scope:** Corrective only: map behavior, honest UI, and misleading prototype chrome removed—not a product or Genie redesign.

## Fixed (this pass)

- **Angle labeling / order (UI):** Selects and mental model use **ASC, DSC, MC, IC** in that order. Labels show **DSC** (not “DC”). Payloads to `/search-regions` still send **DC** for the descendant where the engine expects it (normalized in `map_CURRENT.html`).
- **Compact relocated popup:** **ASC and MC only** in the angle summary; **DSC/IC omitted** from shorthand (full chart / API still has them). Default cusp **explanatory copy removed**; **near-cusp** rows use a **subtle left-edge indicator** only. Planet column **left-aligned**; house column **centered** and **closer** to the planet column.
- **Aspect aura:** **No aura** for **MC/IC** (centerlines only). For **ASC/DSC** contours (API angle **ASC** / **DC**), **`?aspectAura`** draws **offset bands** with **Gaussian-style falloff** (not a flat wide corridor), **weaker at low zoom**, **compressed toward the pole** so the glow does not overwhelm squeezed house geometry. **Exact stroke remains authoritative**; aura is explicitly illustrative.
- **Map interaction:** **`doubleClickZoom` re-enabled**; **wheel** tuned via **`zoomSnap` / `zoomDelta`**, **`wheelPxPerZoomLevel`**, **`wheelDebounceTime`**. **`maxBounds` + `maxBoundsViscosity`** restore a **finite, bounded world** with calm snap-back (tiles already `noWrap`) to reduce **grey margins** and duplicate-world panning. **Reset (○)** unchanged.
- **City search:** Inline **“N places match…” pick list removed** (no layout push). **Enter** resolves to the **highest-population match** in `cities.js`; **city marker click** opens the popup with **pan only—no auto zoom**.
- **Legends:** Panel **multicolor legend** appears only with **`?debugGeometry`**, **`?showLegend`**, or **`?traceConditions`** (dev-facing). **Geometry debug** popups still require **`?debugGeometry`**.
- **Vector joins:** Aspect / overlay **polylines** use **`lineCap: "round"`** and **`lineJoin: "round"`** where stroked.
- **docs / product honesty:** `cities.js` called out as **placeholder** in UI copy and **geocoder** docs; real ranking (Paris FR vs Paris TX, etc.) is **spec / future geocoder**, not current behavior.

## Aura doctrine (backlink)

Non-certifying visual field, tuning from **validated samples / realized geometry** (not a second truth model), falloff shape, poles, **mute/hide**, **popup + exact line always win**: **`docs/overlay_and_aura_visual_strategy.md`**, § **D** — **Doctrine: non-certifying field, samples, and adaptation**.

## Deferred / unchanged on purpose

- **No replacement geocoder** in this pass (no GeoNames import, no hosted API). Enter-only + pop-only keeps the map usable without pretending `cities.js` is globally correct.
- **House polygon “jagged” look** is not “fixed” with blur or smoothing. Institutional write-up remains **`validation/narratives/correction_ui_overlay_qa_pass.md` § “Cause of jagged / blocky polygon edges”** (grid + merge + resolution; not treated as a Leaflet defect). A **git-identified golden commit** for “acceptable” edges was not found; if a decisive checkpoint appears, restore **resolution / generation_mode / merge path** there before new visual hacks.
- **MC/IC “warmth”** without a misleading vertical wall: deferred; centerline-only until a **bell-style** treatment is acceptable for those axes too.
- **Backend astrology math:** unchanged except **frontend** angle code normalization **DSC → DC** for API compatibility.

## Follow-up (geocoder)

Integration target: **GeoNames local import** or **hosted geocoder API** with **stable ID**, **admin**, **country**, **population**, **alternate names**, **precise coordinates**; ranking must support disambiguation examples in `docs/geocoder_and_city_identity_strategy.md`. Until then, **do not certify** city search as globally intelligent.
