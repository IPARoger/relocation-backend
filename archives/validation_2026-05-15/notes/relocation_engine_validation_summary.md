# Relocation Engine Validation Summary — 2026-05-15

Core relocation engine validated against astro.com using point-click popup validator.

Validated cities:

| City | Result |
|---|---|
| Osaka | PASS |
| Atlanta | PASS |
| Cape Town | PASS |
| Singapore | PASS |
| Anchorage | PASS |
| Buenos Aires | PASS |
| Reykjavik | PASS |

Conclusion:

The relocation engine itself is effectively validated for ASC, MC, DESC, and IC.

Remaining validation work is now focused on visualization fidelity:

- contour line validation
- anti-meridian continuity
- aspect overlay validation
- polygon/orb topology
- interpolation behavior
- UI refinement

Important product decisions:

- Default latitude guardrail should likely cap normal users around ±65°.
- Advanced/research mode can later unlock extreme latitude behavior with warning.
- Fairbanks is current preferred symbolic northern-boundary city.
- Popup should expand to include full planet-house matrix.
- Cusp-zone UX should show planets late in a house as transitional toward the next house.
- City search needs autocomplete with disambiguation.
- Map dots should eventually be replaced or supplemented with clickable city names / cleaner density management.
