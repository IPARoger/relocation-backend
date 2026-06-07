# Chat 02 Raw Im1. Missed or Underdeveloped Items

**Architecture pivots were underdeveloped.**  
The first extraction did not fully capture the repeated pivot pattern: fragile patching → broken interface → Git restore → stable baseline → isolated feature addition → regression → need for Cursor/VS Code. The durable lesson is that this project needs checkpoint discipline before every risky math/UI change.

**Aspect overlay strategy was too compressed.**  
The important distinction is:

- broad house-placement polygons = regional sweep
- aspect-to-angle overlays = narrower “extra juice”
- city click charts = precise local verification/details

These are three different modes and should not be forced into one UI or one geometry model.

**The debugging failure itself is institutional knowledge.**  
A major lesson is that the AI repeatedly solved the wrong layer: frontend styling when the problem was backend process state; backend code when the browser was showing the wrong file/port; fake math when the product needed validated astronomy.

**The user’s instruction style is product-critical.**  
Future AI collaborators must avoid vague “find this line” directions when many similar lines exist. Exact block replacement or full-file rewrite is preferred once code becomes unstable.

## 2. Corrections to First Extraction

**Correction: The frontend was not always “not the issue.”**  
At different moments it was the issue: wrong file being viewed, local HTML vs running server, stale browser cache, and style functions masking aspect overlays. The lesson is not “frontend is fine,” but “identify the active layer before changing code.”

**Correction: The math issue is more specific than “longitude wrong.”**  
Ecliptic longitude was incorrectly used for MC. MC angularity needs right ascension/sidereal-time logic. ASC/DSC are even more complex and should not be treated as simple ±90° longitude offsets.

**Correction: Hard rectangles are not just ugly; they are epistemically dangerous.**  
They are acceptable scaffolding only if clearly labeled temporary. Otherwise they create false confidence that the map is astrologically valid.

**Correction: Favorites were misunderstood.**  
They are not merely a sidebar list on the map. They belong to a chart/client/account data layer, with the map as an action page.

## 3. Additional Durable Insights

**CURRENTLY IMPORTANT — Stable baseline before feature work.**  
The project should always preserve a known-good working file before adding search, overlays, gradients, favorites, or chart features.

**CURRENTLY IMPORTANT — Raw JSON inspection matters.**  
Before diagnosing Leaflet rendering, inspect backend response geometry/properties. This prevents confusing style problems with data problems.

**CURRENTLY IMPORTANT — Process state is a real bug category.**  
Zombie uvicorn processes and “address already in use” caused stale behavior. Future workflow should include clear server-stop/start commands and port checks.

**CURRENTLY IMPORTANT — Full-file rewrites may be safer than patching.**  
Once indentation corruption accumulates, replacing `main.py` with a clean full version is safer than surgical TextEdit edits.

**FUTURE INVESTIGATION — Aspect search needs layered design.**  
Planet-to-angle search should start with MC only, then IC, then ASC/DSC, then aspect families. Planet-to-planet relocated aspects come later.

**FUTURE INVESTIGATION — AI should support, not dominate.**  
There should be a “dumb/non-AI” mode where the software simply shows charts, placements, overlays, and comparisons. AI interpretation is optional.

## 4. Important Repetitions / Foundational Themes

**Exactness over cleverness.**  
Repeatedly reinforced. The app should not fake geometry to look good.

**Overlap is often the answer.**  
The product’s value is not merely individual lines or regions, but meaningful overlaps and combined conditions.

**Map-first, but not map-only.**  
The map is central for discovery, but account/chart/favorites/comparisons are separate durable workflows.

**One change at a time.**  
This became the main engineering discipline after regressions.

**Validation before polish.**  
No gradient, aura, or color system matters until the math is verified.

## 5. Still Unresolved

- Correct MC longitude formula and validation.
- Correct ASC/DSC curve geometry.
- Gradient/orb falloff implementation.
- Whether Leaflet remains sufficient or Google/Mapbox/MapLibre is better.
- How to handle poles/high latitudes.
- How to handle antimeridian seams.
- City label density and international search.
- Account/dashboard UX.
- Favorites data model.
- Comparison workflow.
- AI interpretation scope.
- Typography/custom glyphs.
- Overlay color system and semantic child colors.
- NOT/exclusion overlays.

## 6. Items That Should Be Added to Permanent Project Docs

**Engineering discipline doc**

- Use Git checkpoints.
- Never mix math, frontend, cache, and server debugging.
- Prefer full-file replacement after corruption.
- Move to Cursor/VS Code.

**Validation dossier**

- astro.com comparisons.
- city popup truth checks.
- raw JSON samples.
- screenshots of regressions.
- known edge cities.

**Aspect-search design doc**

- Phase 1: planet conjunct MC.
- Phase 2: MC/IC.
- Phase 3: ASC/DSC.
- Phase 4: aspect families.
- Phase 5: planet-to-planet relocated aspects.
- Phase 6: scoring/overlap heatmaps.

**UX philosophy doc**

- restrained, premium, contemplative.
- map-readable under overlays.
- no gimmicks.
- professional workflow first.
- AI optional.

**Overlay/aura doc**

- centerline exactness.
- orb falloff.
- transparency rules.
- semantic overlap blending.
- exclusion overlays.port

Paste raw archaeology output here. Leave it unedited during intake.  

Second-Pass Audit — Relocation Astrology Platform Archaeology

## 1. Missed or Underdeveloped Items

### 1.1 The “AI workflow failure” is not incidental; it is a core project lesson

**Status: CURRENTLY IMPORTANT**

The first extraction mentioned that long chats degrade, but it did not fully capture how central this became.

This chat demonstrated that AI-assisted coding can actively damage the project when:

- the AI loses track of current code state,
- gives “find something like this” instructions,
- assumes code that no longer exists,
- gives line-level advice without current line numbers,
- proposes edits based on stale mental state,
- mixes backend geometry issues with frontend rendering issues,
- patches symptoms instead of restoring known-good architecture.

Durable lesson:

> The project needs an explicit AI collaboration protocol, not just product documentation.

Recommended permanent doc:

```text
docs/ai_workflow_protocol.md

```

Required rules:

- Never patch from memory when current code has been pasted or uploaded.
- Always distinguish “observed code” from “inferred code.”
- Use exact `FIND / REPLACE WITH`.
- Use real line numbers only when they are visible/current.
- Do not say “probably,” “something like,” or “look around” during implementation.
- When more than two speculative fixes fail, stop and perform regression analysis.
- When indentation breaks repeatedly, replace full blocks or restore from backup.
- Always preserve a known-good file before risky edits.

Why it matters:

The app’s technical risk is not only math. The development process itself can corrupt the system unless controlled.

---

### 1.2 The “user trust contract” was underdeveloped

**Status: CURRENTLY IMPORTANT**

The first extraction captured that the user wants exact commands, but not the deeper product/process implication.

The user’s frustration was not merely communication style. It revealed a trust contract:

> When the software represents invisible astrological geography, imprecision destroys trust.

This applies both to:

- the product UX,
- and the development workflow.

If the app visually shows a line, region, or overlap, it must mean something precise. If the AI says “change this,” the instruction must refer to something real and current.

Durable principle:

```text
Trust is built through inspectable precision.

```

Strategic implication:

The same philosophy should guide:

- overlays,
- popups,
- validation,
- UI labels,
- AI-generated explanations,
- developer docs,
- professional reports.

---

### 1.3 The “server restart friction” became a workflow requirement

**Status: CURRENTLY IMPORTANT**

The first extraction did not sufficiently capture that the user repeatedly needed copy-paste server commands every time.

Important durable workflow preference:

Every implementation response involving backend edits should end with:

```bash
cd ~/Desktop/relocation-backend
source venv/bin/activate
uvicorn main:app --reload

```

If the server is already running:

```text
Press Control+C first, then paste the command block.

```

Why it matters:

The user is not asking for conceptual Linux guidance. They need reliable repeated operational commands during iterative debugging.

Permanent workflow doc should include:

```text
Backend restart standard command
Frontend hard refresh command
How to kill port 8000 safely
How not to type CTRL+C literally

```

---

### 1.4 Cursor paste/indentation behavior is a project risk

**Status: CURRENTLY IMPORTANT**

The first extraction mentioned Cursor, but underweighted it.

Observed issue:

Cursor/VSCode auto-indent repeatedly mangled Python blocks, especially nested loops and dictionaries.

This caused:

- syntax errors,
- accidental variable replacement,
- broken house-region logic,
- broken ASC interpolation,
- broken MC gradient loops,
- loss of working functionality.

Permanent rule:

> Avoid asking the user to manually indent large Python blocks. Provide full replacement blocks or use a formatter/Git patch.

Suggested dev practice:

- Use `python -m py_compile main.py` before restarting server.
- Use Black formatter eventually.
- Add Git before further edits.
- Use small, named functions so replacement blocks are shorter.

---

### 1.5 “DeepSeek fixed it” is an important process datum

**Status: CURRENTLY IMPORTANT**

The first extraction mentioned DeepSeek but did not preserve the strategic implication clearly enough.

A key event:

The user lost trust in the current AI thread and asked DeepSeek to repair the code. DeepSeek repaired indentation properly enough that the app worked again.

This matters because:

- cross-AI review may be valuable,
- one model can become unreliable in a long context,
- external repair can reset the codebase,
- the project should not depend on one chat’s continuity.

Strategic implication:

Create an AI reviewer workflow:

```text
GPT implementation chat
DeepSeek or second model review
local validation script
human acceptance
commit

```

---

## 2. Corrections to First Extraction

### 2.1 Correction: The “current file” was not stable at the end

**Status: CURRENTLY IMPORTANT**

The first extraction stated a “latest known backend” as if stable, but the later code paste showed corruption after attempted ASC optimization.

Specific corruptions seen:

- house-region loop accidentally changed to `asc_lon_grid`,
- `asc_lon_grid` used before it exists in the house region block,
- `lat_val` overwritten where `lon_val` should have been created,
- MC gradient tuple list pasted without its `for band_dist, opacity in`,
- ASC interpolation still partly used `lat_grid/lon_grid`,
- code had syntax errors such as `ffor`.

Correct memory:

> The user had a working DeepSeek-repaired version, then subsequent edits began corrupting it again. The safe baseline is the DeepSeek-fixed working file before later manual optimization attempts, not the final pasted corrupted code.

Permanent implication:

Before the next chat edits anything, the user should restore or identify the last working file and back it up.

Recommended first command in next implementation chat:

```bash
cd ~/Desktop/relocation-backend
cp main.py main_backup_before_next_edits.py
python -m py_compile main.py

```

---

### 2.2 Correction: ASC “double lines” were not solved by narrowing `diff`

**Status: CURRENTLY IMPORTANT**

The first extraction correctly said ASC double lines come from contour boundaries, but later guidance implied `diff <= .35` might collapse the double appearance.

More accurate statement:

`diff <= .35` may reduce band width and speed up calculations, but it does not solve the underlying contour-boundary issue. A binary mask still has edges, and contour extraction still tends to trace boundary geometry rather than a true centerline.

Correct next direction:

- skeletonization,
- medial axis,
- root-solving,
- or explicit centerline construction.

---

### 2.3 Correction: MC gradients are not true gradients yet

**Status: CURRENTLY IMPORTANT**

The first extraction described MC gradients as working, but technically they are multiple translucent `LineString`s, not a real continuous aura.

This is acceptable for prototype but should be remembered as a visual approximation.

Permanent wording:

> MC “gradient” currently means stacked translucent offset lines. Future aura rendering may need polygons, canvas blur, raster fields, SVG filters, or WebGL.

---

### 2.4 Correction: House regions were accidentally confused with ASC logic during edits

**Status: CURRENTLY IMPORTANT**

The first extraction said this happened, but not strongly enough.

This is a major architecture warning:

House-region contour extraction and ASC contour extraction look similar but must remain separate. During manual edits, ASC variables leaked into house-region code.

Examples:

- `asc_lon_grid` in house-region loop,
- `asc_lat_grid` in house-region interpolation,
- `aspect_features.append` once appeared inside house-region logic,
- house polygons temporarily became line features.

Permanent implication:

Do not optimize ASC by global search/replace for `lat_grid/lon_grid`. Edit only within the ASC function after modularization.

---

## 3. Additional Durable Insights

### 3.1 The app needs “debug mode” before more visual refinements

**Status: CURRENTLY IMPORTANT**

This was underdeveloped.

A debug mode should expose:

- number of house features,
- number of ASC contours,
- number of MC lines,
- elapsed backend calculation time,
- grid resolution used,
- aspect offsets used,
- selected planet/angle/aspect,
- whether output contains polygons or lines,
- possibly sample coordinate truth checks.

Why it matters:

The team repeatedly guessed whether the frontend, backend, cache, or geometry was responsible. Debug metadata would stop that.

Suggested API return extension:

```json
{
  "type": "FeatureCollection",
  "features": [],
  "debug": {
    "house_features": 0,
    "aspect_features": 0,
    "asc_contours": 0,
    "mc_lines": 0,
    "seconds": 0.0,
    "resolution": 1.5
  }
}

```

---

### 3.2 The app needs a known-good regression archive

**Status: CURRENTLY IMPORTANT**

The user explicitly asked to go back through the chat to identify when behavior changed. That should not require archaeology.

Create:

```text
validation/regression_cases/

```

Each case should include:

- screenshot,
- input parameters,
- expected visual behavior,
- expected backend feature count,
- expected sample city truth,
- known bugs if applicable.

Examples from this chat:

- MC conjunction should produce vertical line + aura, not curved banana.
- ASC conjunction should render curved line, not blank.
- Hard aspects should not show sextile.
- Soft aspects should include trine and sextile, not only sextile.
- Square should show both 90 and 270 offsets.
- All major aspects should include all expected offsets.
- MC polygon outline should not inherit aspect colors.
- Changing “show all aspects” should not hide real MC line functionality.

---

### 3.3 Aspect group correctness became an implicit validation category

**Status: CURRENTLY IMPORTANT**

The first extraction listed aspect sets, but did not preserve how aspect-group bugs appeared.

Observed issues:

- “All major aspects” appeared to show only sextile at one point.
- Hard aspects appeared to show sextile even though sextile should not be included.
- Soft aspects appeared to miss trine.
- Square appeared on hard aspects but perhaps not all expected components.
- Slow rendering made it hard to tell whether old layers were still displayed.

Durable implication:

Aspect-group validation must test not just geometry but semantic inclusion/exclusion.

Create tests:

```text
hard = 0, 90, 180, 270 only
soft = 60, 120, 240, 300 only
any = 0, 60, 90, 120, 180, 240, 270, 300
square = 90, 270
trine = 120, 240
sextile = 60, 300

```

Frontend must clear old layers before rendering new selections.

---

### 3.4 Layer clearing / stale overlay problem needs explicit testing

**Status: CURRENTLY IMPORTANT**

The user suspected overlays were duplicating/overlaying and old aspects kept displaying.

This may be caused by:

- frontend not clearing prior `aspectLayer`,
- backend returning duplicate features,
- slow requests finishing out of order,
- user changing controls before previous render completed,
- multiple concurrent API requests,
- Leaflet layers not removed correctly.

Permanent next-step:

Add request cancellation or response sequencing:

```text
Only render the latest request response.
Ignore older in-flight responses.
Clear aspect layer before adding new one.
Show loading state.
Disable button while request is running.

```

Why it matters:

Slow ASC makes frontend race conditions more visible.

---

### 3.5 Loading state is not just UX polish

**Status: CURRENTLY IMPORTANT**

ASC loads slowly enough that the user could not tell what was rendering for which input.

This is a functional problem.

Needed:

- spinner or “Calculating ASC…” indicator,
- disable controls during calculation,
- cancel previous request,
- timestamp/log current request,
- maybe show “ASC can take longer.”

Without this, users misinterpret stale layers as mathematical errors.

---

### 3.6 The hidden-Alaska-line incident reveals control-panel risk

**Status: CURRENTLY IMPORTANT**

The user initially thought a square line was shortened or missing, then realized part of it was hidden behind the interface.

This is important UX evidence.

Permanent rule:

> Controls must not obscure map evidence during validation or professional use.

Possible solutions:

- collapsible drawer,
- draggable panel,
- translucent panel,
- right-side drawer,
- bottom sheet,
- hide controls after search,
- map padding to account for panel.

---

### 3.7 Current latitude cap is a mathematical and UX decision

**Status: OPEN / CURRENTLY IMPORTANT**

The code uses roughly:

```python
lat_grid = np.arange(-60, 86, ...)

```

This was treated as implementation detail, but it is product-significant.

Reasons:

- Placidus houses can fail or behave strangely at high latitudes.
- Users may search Iceland, Alaska, Scandinavia, etc.
- Reykjavik/Anchorage appeared in testing.
- Polar gaps or cutoffs need explanation.

Permanent question:

Should the app:

- cap latitude,
- warn users,
- switch house systems,
- support high-latitude fallbacks,
- show “calculation unreliable above X”?

---

## 4. Important Repetitions / Foundational Themes

### 4.1 “Do not solve the wrong problem”

**Status: FOUNDATIONAL**

This repeated constantly.

Examples:

- changing frontend style when backend geometry was wrong,
- disabling MC renderer instead of fixing duplicate overlay,
- discussing rendering while server was not restarted,
- guessing code snippets that did not exist,
- treating ASC double contours as line weight issue,
- using broad `if False` to silence symptoms.

Permanent principle:

```text
Classify bug first: math, GeoJSON, frontend layer, stale server, CSS/style, or UX race.

```

---

### 4.2 “Exactness beats cleverness”

**Status: FOUNDATIONAL**

The user consistently rejected vague or clever guidance.

This should inform product design too:

- advanced features should be inspectable,
- AI interpretations should cite which placements/regions caused conclusions,
- overlays should expose exact degrees/orbs,
- professional mode should allow verification.

---

### 4.3 “The map is the model”

**Status: FOUNDATIONAL**

The map cannot be merely evocative. It is the primary interface to the calculation.

Consequences:

- city labels must be readable beneath overlays,
- overlays must correspond to truth,
- opacity must communicate intensity without hiding geography,
- overlaps must remain interpretable,
- old layers must not persist accidentally.

---

### 4.4 “Overlap is the answer”

**Status: FOUNDATIONAL**

The product’s deeper value is not individual lines but intersections:

- house + house,
- house + angle,
- angle + aspect,
- positive + negative constraints,
- city + field intensity,
- purpose + planetary pattern.

This should shape future UI:

- overlap count,
- blended regions,
- ranked candidate locations,
- “why this city” explanation.

---

### 4.5 “Professional-grade first, lay UX later”

**Status: FOUNDATIONAL / CURRENTLY IMPORTANT**

The user repeatedly values accuracy and professional trust. Lay-user UX matters, but should not come at the expense of precision.

Development sequence should be:

1. professional-grade calculations,
2. validation,
3. readable map,
4. simplified intake,
5. AI interpretation.

Not:

1. shiny AI interface,
2. vague pretty maps,
3. math later.

---

## 5. Still Unresolved

### 5.1 ASC centerline extraction

**Status: OPEN**

Core unresolved technical problem.

Need compare:

- skeletonize mask,
- medial axis,
- contour averaging,
- marching zero-crossings,
- analytical ASC solver,
- adaptive root tracing by latitude.

Success criteria:

- single meaningful ASC curve,
- no double boundary artifact,
- fast enough,
- stable near seams,
- visually smooth,
- validates against sample points.

---

### 5.2 ASC performance

**Status: OPEN**

Current brute-force `swe.houses` over a grid remains slow.

Possible next tests:

- coarse grid plus interpolation,
- cache repeated house calculations,
- vectorized or parallel computation,
- precomputed static grids per birth time,
- adaptive curve tracing instead of full-world raster,
- lower default resolution for preview, higher for export.

---

### 5.3 MC aura implementation

**Status: OPEN**

Current stacked lines are acceptable prototype, but not final.

Need decide:

- multi-line aura,
- filled polygon band,
- raster heatmap,
- canvas blur,
- WebGL,
- separate centerline + orb-zone.

Also need define actual orb:

- 3°?
- 5°?
- configurable?
- different for professional vs lay mode?

---

### 5.4 DC and IC

**Status: OPEN / UNDERDEVELOPED IN FIRST EXTRACTION**

The first extraction mostly discussed ASC and MC, but a full angular relocation system should support:

- ASC
- DSC/DC
- MC
- IC

Likely logic:

- DC is ASC + 180 relationship, but geographic curves may require careful handling.
- IC is MC + 180 meridian relationship.
- UX should expose all four angles eventually.

Need validation before adding.

---

### 5.5 Aspect-to-angle semantics

**Status: OPEN**

Need decide whether angular overlays mean:

- planet aspects relocated angle,
- planet RA aspect to MC,
- ecliptic longitude aspect to ASC,
- what coordinate system is astrologically correct for each.

The current code uses equatorial RA for aspects to MC. ASC uses house calculation and ASC longitude.

This needs formal documentation:

```text
docs/calculation_assumptions.md

```

---

### 5.6 House system handling

**Status: OPEN**

Current house system appears Placidus:

```python
swe.houses(jd, lat, lon, b'P')

```

Need decide:

- default house system,
- user-selectable house systems,
- polar fallback,
- professional settings.

---

### 5.7 Map provider

**Status: OPEN**

Leaflet is prototype-sufficient. Still unresolved:

- Google Maps for labels/geocoding?
- Mapbox for styling?
- MapLibre for open-source control?
- custom tiles?
- offline maps for travel mode?

---

### 5.8 City/geocoder ranking

**Status: OPEN**

Need robust city search:

- importance ranking,
- population ranking,
- country disambiguation,
- transliteration,
- alternate names,
- local scripts,
- historical names,
- airport/region relevance.

---

### 5.9 Account/intake tone

**Status: OPEN / UNDERDEVELOPED**

First extraction mentioned account UX only briefly.

Future account/intake screens will set emotional tone before map appears. They should not feel like generic forms.

Need decide:

- birth data entry style,
- privacy reassurance,
- professional/client profile mode,
- saved charts,
- purpose intake,
- “what are you seeking?” language.

---

### 5.10 Drawer/genie/sidebar behavior

**Status: OPEN / UNDERDEVELOPED**

The prompt explicitly mentions drawer/genie reasoning, but first extraction did not capture much.

Known from this chat:

- fixed controls can hide map evidence,
- map-first UX needs collapsible controls,
- long sessions require comfort,
- professional workflows need controls without clutter.

Need investigate:

- left sidebar,
- right drawer,
- floating command palette,
- “genie” assistant panel,
- bottom sheet on tablet/mobile,
- minimized map controls.

---

## 6. Items That Should Be Added to Permanent Project Docs

### 6.1 `docs/product_philosophy.md`

Add:

- The app is a planetary spatial intelligence system, not a generic astrocartography clone.
- The map is the model.
- Overlap is the answer.
- Precision and beauty must reinforce each other.
- Avoid gimmicky AI astrology.
- Build professional trust first; simplify later.
- Emotional tone: contemplative, premium, restrained, inevitable.

---

### 6.2 `docs/calculation_assumptions.md`

Add:

- Swiss Ephemeris is source of calculation.
- Current house system is Placidus unless changed.
- MC uses RA/sidereal-time longitude method.
- ASC currently uses brute-force relocated house calculation.
- ASC contour method currently produces boundary artifacts.
- Latitude caps and polar behavior unresolved.
- Aspect coordinate-system assumptions need formal review.

---

### 6.3 `docs/architecture.md`

Add:

- Separate MC and ASC engines.
- Separate house-region engine from angular overlays.
- Avoid cross-contamination of `lat_grid/lon_grid` and `asc_lat_grid/asc_lon_grid`.
- Modularization target:

```text
astro/houses.py
astro/regions.py
astro/mc.py
astro/asc.py
astro/aspects.py
astro/geojson.py

```

---

### 6.4 `docs/validation_strategy.md`

Add:

- Astro.com comparison archive.
- Popup truth validation.
- Regression screenshots.
- Aspect-set inclusion tests.
- Feature-count debug tests.
- Dateline and polar tests.
- False positive/false negative point testing.
- GeoJSON export independent of frontend.
- Proof-of-work archive for every major calculation claim.

---

### 6.5 `docs/ai_workflow_protocol.md`

Add:

- Always backup before editing.
- Use exact `FIND / REPLACE WITH`.
- No vague code references.
- Include restart commands every backend-edit response.
- Stop after two failed patches and perform regression analysis.
- Prefer full block replacement over manual indentation.
- Use `python -m py_compile main.py`.
- Commit working states.

---

### 6.6 `docs/ux_principles.md`

Add:

- Map-first layout.
- Controls must not hide important geography.
- Long-session comfort matters.
- City labels must remain readable under overlays.
- Loading states are functional requirements.
- Old layer clearing must be obvious.
- Professional mode vs lay mode.
- Drawer/sidebar behavior unresolved.

---

### 6.7 `docs/overlay_aura_system.md`

Add:

- Centerline + aura model.
- MC stacked-line aura is temporary.
- ASC contour double-lines are boundary artifacts.
- True aura may need raster/canvas/WebGL.
- Overlap blending and child colors.
- NOT/exclusion overlays.
- Transparency must preserve city readability.

---

### 6.8 `docs/future_features.md`

Add near-term:

- Fix ASC centerline.
- Add debug metrics.
- Add request cancellation/loading state.
- Stabilize code with Git.
- Modularize backend.
- Validate aspect groups.

Add medium-term:

- city search,
- city scoring,
- professional reports,
- saved charts,
- purpose presets,
- layer manager,
- DC/IC.

Add far-future:

- GPS travel mode,
- offline route mode,
- transits to relocated houses,
- professional astrologer dashboard,
- education/certification ecosystem,
- AI-assisted client interpretation.

---

# Final Audit Conclusion

The first extraction captured the broad project direction, but underdeveloped several durable lessons:

- the AI workflow failure itself is a core architectural/process risk;
- the ASC double-line issue is a boundary-vs-centerline mathematical problem, not merely an orb setting;
- frontend stale-layer/loading behavior may be masquerading as geometry bugs;
- city/map readability and control placement are foundational, not polish;
- the project needs permanent docs for calculation assumptions, validation, AI workflow, overlay theory, and UX philosophy;
- current “working state” must be treated carefully because later edits corrupted the once-working DeepSeek repair.

The most important permanent lesson from this chat:

> The product must make invisible astrological geography feel precise, beautiful, and trustworthy — and the development process must be equally precise, or the tool will lose integrity before it matures.

