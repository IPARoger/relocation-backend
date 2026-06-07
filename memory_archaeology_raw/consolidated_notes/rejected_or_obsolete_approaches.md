# Rejected or Obsolete Approaches (From Archaeology)

This list preserves **why** certain paths were abandoned or flagged dangerous. Do not revive without explicit human re-approval.

---

## Geometry / seam handling

- **Seam repair by altering canonical polygon topology** (boundary-walking / forced closure along map window edges): caused **house identity leakage**, collapsed distinct houses, Southern Hemisphere artifacts—**rejected as architecture**.
- **Hard rectangular overlays presented as real** scaffolding: epistemically dangerous if mistaken for valid Placidus regions.

## Rendering / signal processing mistakes

- **Gaussian blur** (or similar) on astronomical fields used for truth extraction: can **shift** solutions and create false loops—rejected for truth; aesthetics belong in frontend-only layers.

## Aspect / line extraction misconceptions (historic debugging)

- **Contour extraction as the final word for centerlines** in some eras: produced double-line artifacts and boundary effects; archaeology pushes toward clearer centerline definitions + separate aura—exact implementation remains product-specific.

## Incorrect astronomical short-cuts (explicit catastrophic failures)

- Replacing Swiss Ephemeris computations with **hardcoded planet positions** during debugging.
- Confusing **RA** targets with **ASC ecliptic longitude** work—**rejected** as conceptual error (ASC/MC coordinate framing must match the chosen product definition).
- Accidental **Equal House** thinking when Placidus is intended.

## UX / workflow paths

- **Hover-driven** primary interactions for dense city maps: rejected as mobile-incompatible and too noisy.
- **“NOT in house” as a giant inverse paint** (whole-world exclusion visuals): rejected as unusable map semantics (may reappear as subtler constraints later).

## Institutional / AI process paths

- **Terminal heredocs** for large HTML/JS paste ops: repeatedly corrupted files; archaeology bans as operational practice.
- **Vague patch instructions** for non-coders: rejected as a repeated source of breakage—Cursor-era expectation is exact diffs or tool-applied patches.

## Overlap representation (product iteration)

- Returning many **precomputed intersection polygons** (A, B, AB, AC…) as the default UX: rejected aesthetically in some iterations in favor of natural blending—**may still be needed** for analytic modes; tension preserved.

---

## Possibly obsolete but historically explanatory

- Early “bitmask compositing everything” discussions: useful historically; may not match current truth-grid house pipeline.
- Specific “freeze at commit X” narratives from older eras: treat as **time-stamped** unless re-verified against current `main`.

---

## Not “rejected,” but **dangerous if misunderstood**

Brute-force validators: **not ‘the app’**, but also **not inherently throwaway**—archaeology argues they become permanent referee infrastructure if treated seriously.
