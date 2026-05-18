# Aspect aura defaults (approximate display)

**Status:** Frontend-only visualization when `?aspectAura` is present on `map_CURRENT.html`. **Not** astrology orbs and **not** geographic buffers in degrees.

## Authority

- **Popup** / API chart: exact longitudes and derived angles.
- **Centerline** GeoJSON from `/search-regions`: exact aspect-to-angle spine.
- **Aura**: widened, low-opacity stroke **under** the centerline; **screen-pixel weight** scales by selected aspect **preset** only.

## Default screen weights (Leaflet `weight`, approximate)

| Aspect preset   | Aura `weight` | Rationale (product tuning)        |
|-----------------|---------------|-----------------------------------|
| sextile, trine, soft | 9       | Tighter major “soft” family       |
| square          | 11            | Mid between soft and hard         |
| conjunction, opposition, hard | 14 | Wider for conj/opp-style bands |
| any             | 12            | Compromise for multi-line mode    |

**Exact lines** still use API `weight` / `opacity` (MC ~4×95% opacity; contour angles ~2×100% in current defaults).

## NOT done here

- No backend orb field or membership change.
- No latitude-aware geographic σ for aura width (future refinement).
- No replacement of popup copy or numeric orb display.
