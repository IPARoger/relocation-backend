# Validation and Proof Strategy (From Archaeology)

---

## External truth sources

- **[astro.com](https://www.astro.com) as practical gold standard** for relocated comparisons during early engine validation (multiple cities across hemispheres).
- Importance of **high-latitude** cases (Reykjavik/Anchorage/Fairbanks narratives) because Placidus sensitivity exposes both math and UX honesty.

---

## Internal truth instruments

### Point oracle: `/relocated-chart` + map click

Archaeology frames this as a pivot:

- **City search navigates**; it is not always rigorous validation because geocoding ambiguity exists.
- **Right-click / coordinate pick** is the strongest internal comparator to external charts when coordinates are aligned.

### Brute-force / truth-map exports

- Separate dense sampling exports to compare production lines/regions against **independent raster truth**.
- Methodological rule: validate an aspect artifact with the **same aspect’s truth map**.

---

## Hierarchies of validation (explicit ordering appears)

Common ordering in archaeology:

1. Confirm relocated chart point truth vs astro.com on ordinary cases.
2. Validate aspect **semantic sets** (hard/soft/major lists) independent of geometry.
3. Validate overlays vs point probes (especially at boundaries).
4. Build/stress edge-case chart library (polar, dateline, cusp-heavy, midnight, fast Moon, etc.).
5. Automate regression comparisons where possible (still aspirational in many notes).

---

## Proof-of-work archive ethos

Screenshots alone drift; archaeology repeatedly asks for **structured dossiers**:

- city/coordinates, expected angles, observed angles, orb, pass/fail, file/app version, notes on acceptable deviation due to click precision.

---

## Failure modes that masquerade as math bugs

- Stale layers, race conditions, out-of-order async responses, wrong file open, server not restarted, duplicated event handlers.
- **Loading state** is functional: slow ASC made stale overlays look like “wrong astrology.”

---

## AI validation pitfalls (process)

- Automated small screenshots missed topology issues humans saw.
- Confidence from “clean curves” was repeatedly **wrong**.

---

## Status reminder

Archaeology describes many **past** validation crises; current repo may have resolved several. Treat these as **why our methodology exists**, not as guaranteed current bug lists—re-validate against `ai_context/current_state.md`.

---

## Chat 08 update: renderer beta validation ladder

The transported-material renderer work established a validation ladder that should be preserved:

1. **Geometry-free material control:** prove the strip profile as a solid RGB/material field before geometry.
2. **Texture-coordinate transport:** prove local `(s,u)` transport on straight and curved strips.
3. **Asymmetry proof:** fixed and dynamic left/right side widths, each normalized independently.
4. **Extreme asymmetry stress:** near-collapse cases such as right side `1`, `0.5`, and `0.25` units; distinguish pixel collapse from transport failure.
5. **Multicolor validation:** prove the same transport/hierarchy logic survives restrained palettes.
6. **Map-like overlap sandbox:** test labels, coastline, pane ordering, stacking, centerline survival, and mute/solo need before production integration.

The key proof doctrine is **validation-only before production**. Static boards and sandbox artifacts can stabilize architecture without implying final aesthetic approval or production readiness.

Renderer architecture should only reopen if a map-context validation proves structural failure, such as centerline drift, broken side-local scaling, unacceptable label/readability collapse, or pane-order impossibility.
