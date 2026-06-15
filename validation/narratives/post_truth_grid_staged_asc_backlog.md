# Post Truth-grid + Staged ASC Backlog

Milestone confirmed:

- Truth-grid house overlays work and remain opt-in.
- Seam behavior appears stable for High Northern and Southern edge cases.
- Validation contradictions are `0` in saved reports.
- House polygons render quickly before overlays.
- ASC all-major uses staged/shared-grid rendering and is fast enough for manual QA.
- MC overlays remain fast.
- Professional astrologer core workflow is now viable for broader QA.

## Recommended Implementation Order

1. Immediate small UX fixes.
2. Broader fixture and regression hardening.
3. Angle-in-Sign search milestone.
4. Professional interface organization.
5. Birth data workflow.
6. Map/library reassessment after MVP blockers are clearer.

## P0 - Immediate Small UX Fixes

### Dropdown Selection Bug

- Priority: P0
- Risk: Medium
- Files likely affected: `map_CURRENT.html`
- Manual QA required: Yes
- Goal: Fix behavior where opening/selecting dropdowns appears to advance to the next item unexpectedly.
- Notes: Reproduce first before editing. Check whether this is native select focus behavior, accidental keyboard handling, duplicate event listeners, or browser-specific behavior.

### Normal-user Status Indicator

- Priority: P0
- Risk: Low
- Files likely affected: `map_CURRENT.html`
- Manual QA required: Yes
- Goal: Add non-debug status text for normal users:
  - `House regions ready`
  - `Calculating overlay`
  - `Overlay ready`
- Notes: Keep debug badge available only for `debugGeometry=1`; normal status should be visible without debug mode.

### Popup Behavior Regression Pass

- Priority: P0
- Risk: Low
- Files likely affected: `map_CURRENT.html`
- Manual QA required: Yes
- Goal: Confirm popups still clear on repeated searches and auto-reposition into view near map edges.
- Notes: Popup right-edge bounce was previously good; left-edge clipping should be retested.

## P1 - City And Map UX

### Improve City Locator/Search UX

- Priority: P1
- Risk: Medium
- Files likely affected: `map_CURRENT.html`, `cities.js`, possible city data generation scripts
- Manual QA required: Yes
- Goal: Make city search more forgiving and useful: clearer no-result state, result selection, better zoom behavior, and less manual typing friction.

### Add Country Names To Displayed Locations

- Priority: P1
- Risk: Low
- Files likely affected: `map_CURRENT.html`, `cities.js`, `build_cities.py`, `process_cities.py`
- Manual QA required: Yes
- Goal: Ensure displayed city labels/results include country names consistently.

### Improve City Density Per Square Inch

- Priority: P1
- Risk: Medium
- Files likely affected: `map_CURRENT.html`, `cities.js`, city data build scripts
- Manual QA required: Yes
- Goal: Tune visible city density by screen/map density, not only population threshold.
- Notes: This can remain Leaflet-based for now. Reassess only if density/performance becomes a concrete blocker.

## P1 - Testing And Validation

### Expand Edge-case Fixture Suite

- Priority: P1
- Risk: Low
- Files likely affected: `charts/chart_profiles.json`, `validation/fixtures/`, `validation/narratives/`
- Manual QA required: Yes
- Goal: Add representative stress fixtures from `validation/fixtures/truth_grid_fixture_plan.json`.
- Fixtures to prioritize:
  - solstice/equinox
  - high northern
  - high southern
  - antimeridian
  - cusp-heavy
  - optional above `+/-65` latitude stress

### Promote Browser/API Checks Into Scripts

- Priority: P1
- Risk: Medium
- Files likely affected: new validation script under `validation/` or `scripts/`, possibly `validation/reports/`
- Manual QA required: No for script creation, Yes for visual confirmation
- Goal: Convert recent ad hoc browser/API validations into repeatable commands.
- Notes: Keep output in `validation/reports/` for proof-of-work dossier.

### Reassess Latitude Cap

- Priority: P2
- Risk: High
- Files likely affected: `truth_grid_engine.py`, `truth_field_regions.py`, `main_centerline_FIXER.py`, validation fixtures/reports
- Manual QA required: Yes
- Goal: Determine whether the `+/-65` truth-grid cap is still necessary now that classification is robust.
- Notes: This touches Placidus edge behavior and should not be mixed with UX work.

## P2 - Angle-in-Sign Search

### ASC/MC In Sign Search

- Priority: P2
- Risk: Medium-High
- Files likely affected: `main_centerline_FIXER.py`, `truth_grid_engine.py` or new field module, `map_CURRENT.html`, validation fixtures/reports
- Manual QA required: Yes
- Goal: Search for:
  - ASC in Aries/Taurus/etc.
  - MC in Aries/Taurus/etc.
  - IC/DSC later if useful
- Recommended approach: Use the same truth-grid/brute-force sampling model where appropriate. Cache ASC/MC degree/sign fields from sampling rather than inventing a separate display-only method.
- UX note: Integrate without crowding the map; likely use an advanced/search panel section.

## P2 - Professional Interface Strategy

### Advanced Controls Organization

- Priority: P2
- Risk: Medium
- Files likely affected: `map_CURRENT.html`, possible future frontend module split
- Manual QA required: Yes
- Goal: Keep maximum real estate for the map while supporting professional controls.
- Include:
  - advanced settings section
  - aspect preferences
  - orb preferences
  - latitude cap override for professionals
  - house system settings later
  - save/share/export workflow later
- Notes: Avoid redesigning everything at once. First preserve current working map and progressively organize controls.

## P3 - Birth Data Workflow

### Proper Birth Data Entry

- Priority: P3
- Risk: High
- Files likely affected: `map_CURRENT.html`, backend request models/endpoints, possible timezone/geocoding modules
- Manual QA required: Yes
- Goal: Add real user birth data entry:
  - date
  - time
  - birthplace
  - historical timezone handling
  - daylight saving correctness
  - uncertain birth time protocols
  - rectification/uncertainty warnings
- Notes: Historical timezone correctness is a product-critical domain issue and should use a trusted library/source rather than ad hoc offsets.

### AI Guide Intake

- Priority: P3
- Risk: Medium
- Files likely affected: future UI/backend modules
- Manual QA required: Yes
- Goal: Let an AI guide collect birth/search intent while background computation warms caches.
- Notes: This should not block the non-AI professional workflow.

## P3 - Map/Library Strategy

### Mapping Stack Reassessment

- Priority: P3
- Risk: Medium
- Files likely affected: frontend only if migration is later chosen
- Manual QA required: Yes
- Recommendation: Do not migrate yet. Leaflet appears viable for MVP now that truth-grid separates truth from display artifacts.
- Reassess later against concrete blockers:
  - city density
  - interaction polish
  - vector rendering performance
  - layer count
  - export/share needs
- Options to evaluate later:
  - Leaflet
  - MapLibre
  - Mapbox
  - Google Maps

## Known Current Caveats

- `truth_grid` is still opt-in and should not become default until broader QA passes.
- Coarse/medium ASC overlays are preview geometry and can shift before final.
- Polar/above-cap behavior remains intentionally out of MVP scope.
- Validation reports exist, but some checks are not yet promoted into reusable scripts.
- Untracked browser temp profiles may exist locally and should not be committed.

