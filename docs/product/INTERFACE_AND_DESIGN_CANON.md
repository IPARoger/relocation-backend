# INTERFACE_AND_DESIGN_CANON.md

**Status:** Canonical onboarding and transfer manual for interface, UX, visual semantics, screen hierarchy, and design-system constraints.  
**Source archive:** `ALL_PROJECT_DOCUMENTS.txt`  
**Generation method:** three-pass local Python extraction and consolidation.  
**Matched design/interface source blocks:** 186  
**Audit hash:** `40bc474b2679ca19`

---

## 0. Unbending Product Guardrail

**Reveal structure. Preserve judgment. Cities are secondary targets.**

This sentence is the interface constitution. The product is an astrological geography instrument, not an oracle, not a dashboard, not a recommendation engine, and not a city-ranking toy. The interface must make chart conditions visible, searchable, inspectable, saveable, and comparable. It must not decide what the chart means for the user. It must not collapse symbolic tradeoffs into a hidden score. It must not auto-interpret a place as good, bad, destined, ideal, blessed, cursed, or optimized. Interpretation belongs one hundred percent to the interactive human user, whether that user is a professional astrologer, an advanced symbolic practitioner, or a lay explorer later supported by optional educational layers.

The visual system therefore has one primary ethical job: expose spatial structure without stealing judgment. Every map fill, material strip, popup, drawer control, chart detail view, favorite, comparison, saved search, export, or onboarding cue must respect this boundary. The software may show “Sun in 1st applies here,” “Venus in 7th overlaps here,” “Saturn in 4th is excluded here,” “ASC is in Libra here,” or “this angular band is closer to exactness here.” The software may not turn that into “move here,” “this is best,” “this will make you happy,” or “this is objectively superior.” Any future assistive interpretation must remain downstream, labeled, optional, and subordinate to the factual layer.

Cities are also downstream. They are human markers placed inside geographical coordinates. The computational starting point is not a city list; it is the earth as coordinate field, sampled through a chart model. City labels help people orient, shortlist, compare, and save. They do not define the geometry. A city can be clicked, searched, favorited, compared, and exported, but it remains a candidate point or named region inside a wider condition field. The viewport canvas begins with geography and chart conditions. Cities are secondary affordances for human decision-making.

---

## 1. Source Scope and Extraction Boundaries

The design canon was built from archive blocks whose headers or content matched interface-oriented keywords: `ux`, `ui`, `color`, `layout`, `font`, `typography`, `overlay`, `visual`, `design`, `workflow`, `concept`, `style`, `canvas`, `sidebar`, `drawer`, `genie`, `map`, `screen`, `brand`, `experience`, `semantic`, `journey`, `onboarding`, `interaction`, `layer`, `ontology`, `geometry`, `condition`, `popup`, `cities`, `control`, `palette`, `motion`, `animation`, `aura`, `virga`, and `rain`.

The matched source set spans these categories:

| Category | Matched blocks |
|---|---:|
| architecture_bridge | 178 |
| language_payload | 90 |
| map_workspace | 146 |
| validation_design | 89 |
| visual_semantics | 119 |
| workflow_screens | 165 |

The deeper pass preserved source block names, hashes, headings, and requirement-like lines in the audit JSON. The manual below consolidates the design and interface requirements into a single operational doctrine. It does not attempt to preserve every historical sentence verbatim. It preserves product laws, implementation boundaries, UX hierarchy, visual semantics, screen responsibilities, and future optimization inventory while excluding speculative 2.0/Web3 models from active build instructions.

### High-priority source families

The most central interface and design source families include:

- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/product_doctrine/UX_DOCTRINE_MASTER.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_DOCTRINE_MASTER.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ux/2026-05-29_application_journey_architecture_v1.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/2026-05-29_application_journey_architecture_v1.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ux/UX_CONSTITUTION.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_CONSTITUTION.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/UX_CONSTITUTION.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_CONSTITUTION.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_1_2_EXTRACTION_AUDIT.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_RENDERING_ARCHITECTURE.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/visual_design/aura_visual_design_brief.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/technical_philosophy/rendering_truth_over_cosmetics.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/overlay_and_aura_visual_strategy.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/cartographic_language_and_city_rendering.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/relocation_app_product_roadmap.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/relocation_app_product_roadmap.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/ONBOARDING_CLASSIFICATION_REPORT.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_app_shell_handoff_audit_v1_2026-05-30.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_IMPLEMENTATION_PROTOCOL.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/relocation_map_architecture.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_render_payload_v1_2026-05-30.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/client_chart_data_model_v1_2026-05-29.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/client_chart_data_model_v1_2026-05-29.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/05_archive/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ui/map_workspace_behavior_audit_v1_2026-05-30.md`

---

## 2. Interface Epistemology: What Each Surface Is Allowed To Mean

The interface has a truth hierarchy. Every UI surface must know whether it is reporting a point fact, a spatial field, a management object, or an interpretive note.

### 2.1 Point inspection is canonical local truth

The point popup, right-click inspection, city-click detail, and full relocated chart view are the authority for “what is true here.” If a user clicks a point, the system must report factual relocated chart data for that coordinate: angles, house placements, relevant angle signs, aspect-to-angle data, and other supported relocation-specific facts. This surface is allowed to be dense because it is the inspection layer. It should still be calm, legible, and typographically disciplined.

The popup must not become a mini-interpretation engine. It should avoid motivational copy, quality judgments, or synthesized winners. It may display exact degrees, houses, signs, coordinate context, and structured rows. Where possible, city popup, arbitrary point popup, favorites cards, comparison snippets, and saved-location cards should converge on a shared information language so users do not have to learn multiple dialects for the same facts.

### 2.2 Map overlays are exploratory where-fields

Overlays answer “where does this condition hold?” rather than “what should I do?” House regions are categorical membership fields. Angle-in-sign regions are categorical fields. Aspect-to-angle lines and bands are exactness/intensity fields around validated geometry. Exclusion/NOT regions are intentional deprioritization fields. Overlaps are meaningful candidate structures, not accidental clutter.

The map may be visually compelling, but it may not lie. Fills, bands, gradients, textures, opacity, child colors, and material effects must never change Layer 1 membership. Styling can reveal, clarify, prioritize, or reduce visual competition. Styling cannot invent truth, smooth away contradiction, move boundaries, blur incompatible concepts together, or hide disagreement between overlay and popup.

### 2.3 Account, chart, and comparison pages carry full records

The map is deliberately sparse compared with chart pages. The account/chart surface may carry birth chart identity, saved searches, favorite locations, saved comparisons, notes, settings, and full relocated fact tables. This is where denser technical layouts are acceptable. The map popup is an appetizer; the chart page is the full record.

Comparison views must preserve factual equality among candidate places. They may show side-by-side facts and invite human review. They must not synthesize an automatic winner by default. “Best place on Earth” is the wrong frame. Constrained comparison under explicit human intention is the product story.

---

## 3. Spatial Hierarchy and Viewport Law

The map is the primary viewport. It is not a background image behind a dashboard. It is the instrument face.

### 3.1 Geography before cities

The viewport begins with coordinates and condition space. Users may later select cities, save favorites, run comparisons, or export map states, but the system’s first computational relationship is between chart parameters and geographic coordinates. City search helps humans navigate the field. City labels help users orient under overlays. City density and label legibility are product-critical, but city names do not define the condition geometry.

### 3.2 Map real estate is sacred

A control fails if it hides coastlines, city labels, political boundaries, candidate overlap evidence, or the visual relationship between conditions. Interface chrome must serve the map and then recede. Permanent full-height panels, oversized legends, debug banners, status badges, and Photoshop-style layer panels are anti-patterns unless explicitly confined to developer/debug modes.

### 3.3 Controls are secondary but not hidden

The system must avoid two opposite failures: cluttering the map with dashboard controls, and hiding essential actions so deeply that the user feels lost. The target pattern is a map-primary workspace with compact map chrome, a collapsible Genie/drawer, a clear location search, a primary search action visible without scrolling on laptop screens, and layer controls that are available but not visually dominant.

### 3.4 Location search belongs on map chrome

Location search should not be trapped inside the condition builder. The user needs one clear way to search for a location from the map surface. The target placement is lightweight, translucent, and map-native. The city/location search is a navigational affordance; the Genie/drawer is a condition-construction affordance. Mixing them creates conceptual fatigue.

---

## 4. Map Workspace, Drawer, and Genie Doctrine

The map workspace contains three major conceptual zones: the map surface, the location/search chrome, and the condition/layer control system.

### 4.1 The Genie has two modes

Configuration Mode is the editor. It shows full variable cards, field labels, dropdown teaching copy, condition details, polarity, and any necessary experimental controls. Exploration Mode is the compact post-render mode. It uses small affordances, swatches, shorthand, layer rows, mute/solo/exclude controls, and map-surface save/pin affordances.

Reopening the Genie returns to Configuration Mode. The user re-enters the editor to inspect or change the setup, not to be trapped in shorthand-only mode. This rule protects clarity. Compact rows are for exploration; full cards are for understanding and editing.

### 4.2 Search Map emits an immutable render snapshot

Live card state is not search truth after render. When the user runs a search, the interface emits an immutable `genie_render`-style payload snapshot. Pin, Save Search, history, replay, and future export must refer to that rendered snapshot, not to whatever happens to be in the live DOM after the user edits cards again. Re-render produces a new creation timestamp and a new snapshot. Prior snapshots are not mutated.

This immutability is a design-system rule, not just a backend rule. UI labels must make it clear that the displayed map corresponds to the last rendered condition set. Dirty state must be represented if the user changes the editor after render. The user should never believe they are saving one set of conditions while the app silently saves another.

### 4.3 Modular condition cards, not fixed A/B/C rows

The target condition editor is modular. Each row is one semantic condition: planet in house, angle in sign, aspect to angle, transit-through-house if explicitly enabled later, transit-aspect-to-angle if explicitly enabled later, or the same condition expressed with `exclude` polarity. NOT is not a separate variable type. It is a polarity on a canonical condition.

The legacy A/B/C shape may remain as an adapter constraint, but the UI must not teach users that there are only three hardcoded slots or that dummy rows are meaningful. Any adapter that maps modular variables into legacy A/B/C must report degradation metadata when overflow occurs. Silent dropping of conditions is prohibited.

### 4.4 Layer controls are display controls, not astrology truth

Mute, Solo, Send to Background, Send to Foreground, and similar layer controls affect display visibility and inspection priority. They must not change Layer 1 membership, renderer substrate, canonical conditions, or saved astrological truth. Mute hides a layer visually while keeping it in the investigation. Solo isolates temporarily. Send to background lowers visual priority without implying the condition is astrologically less important. NOT/exclusion is not a display toggle only; it is a semantic condition polarity and must be treated deliberately.

### 4.5 Drawer collapse must preserve user orientation

The control drawer should collapse to a corner chip, not disappear into off-screen death. The chip should preserve active condition count and dirty-state indication. One action should restore the drawer. Collapse must not jump the map so violently that the user loses geographic context. There should be no auto-collapse timer; the user owns the chrome.

### 4.6 Missing abstractions to implement deliberately

The interface doctrine implies several state abstractions that should not be improvised ad hoc in the DOM: `LayerDisplayState` for mute/solo/z-order per condition ID, `DrawerLayoutState` for expanded/collapsed/height state, `ConditionDirtyFlag` for unsaved or stale render state, and a mobile gesture map for inspect vs pan. These are design obligations because failure here causes users to mistrust the map or lose work.

---

## 5. Visual Semantic System

The design language is restrained, semantic, and inspectable. It must not read as generic astrology SaaS, mystical rainbow dashboard, neon toy map, AI oracle theater, or debug GIS board.

### 5.1 Beauty from truthful systems

The visual system should become beautiful because the geometry, hierarchy, and semantics are truthful. Decorative fog, fake glow, ornament without a semantic job, and blurs that move membership are rejected. Premium means quiet confidence: fewer elements, each earning its pixels.

### 5.2 House field semantics

Planet-in-house overlays are categorical regions. Their inside/outside membership must remain correct for the engine’s definition. A future cusp transition may soften the display near a house boundary, but this is not uncertainty and not a different house membership. If a cusp display gradient is used, it should be explained as astrological cusp softness, often around a small default scale, and must remain distinct from aspect aura.

### 5.3 Aspect-to-angle material strips and aura semantics

Aspect-to-angle geometry has an exact centerline or exact relationship spine. Any surrounding band communicates angular intensification or orb proximity: closer to exact is stronger. The band must not redefine membership. It is not a broad claim that every part of the corridor is equal. The preferred read is restrained at the outer edge, materially visible near exactness, and strongest at the exact line.

The intensity curve should not be linear if linearity creates a muddy middle corridor. Acceptable curves include logarithmic, exponential, power-law, sigmoid, or another deliberate non-linear shape that sharpens toward exactness. The renderer’s intensity assignment should be a function of normalized distance within configured orb, not raw degrees alone. This lets the same visual logic compress under tighter orbs, high-latitude geometry, and narrow angular corridors.

### 5.4 Cusp softness and aspect aura must never be conflated

House cusp transition and aspect aura are different concepts. The first softens presentation of a categorical house boundary. The second displays angular exactness intensity around a line or relation. Reusing the same blur, ramp, color, or copy for both creates a muddy metaphor and breaks trust. Prototype them separately before combining them in one production view.

### 5.5 Overlaps are discovery objects

Overlap regions are often the answer. A user may search for “Sun in 1st and Venus in 7th but not Saturn in 4th.” The interface must allow this structure to remain visible, inspectable, and emotionally exciting without deciding for the user. Overlap zones should not disappear into alpha mud. Child-color strategies, adaptive opacity, muted layers, solo controls, and semantic color families should eventually make overlap legibility a designed system rather than an accident of stacking.

The interface may use neutral language such as “candidate overlap,” “notable overlap,” or “high-concentration zone.” It should avoid “best,” “winner,” or “top” unless the user has explicitly declared ranking criteria.

### 5.6 NOT/exclusion visual language

Exclusion regions are not positive overlays. They should not light up the allowed world or create alarmist red danger maps. The preferred treatment is a soft veil, desaturation, charcoal/redacted language, muted scrim, low-contrast pattern, or other calm deprioritization. Geography must stay readable. NOT communicates “do not prioritize here,” not “this place is bad.”

### 5.7 Color system principles

Color families should be semantic, not arbitrary rainbow astrology decoration. House conditions, angle-in-sign regions, aspect-to-angle bands, overlap child colors, and NOT/exclusion treatments require separate color families. Current proof-of-concept palettes validate math and visibility, not brand approval. Any final palette must preserve city labels, coastlines, boundaries, and accessibility, including colorblind robustness.

Strong saturation is reserved for meaning. Generic SaaS purple-teal, neon map accents, toy astrology glitter, and muddy alpha stacking are rejected. Control cards may echo overlay colors in small swatches so controls act as the legend. Full-card rainbow treatment should be avoided unless proven readable and restrained.

### 5.8 Typography and popup hierarchy

Typography should be calm, legible, and instrument-grade. Popups may be dense but must not become spreadsheets on the map. Headers may carry more weight; planet names should remain readable without shouting. House numbers should align. Redundant lines should be removed when information is already encoded in degrees. Account pages can carry denser tables; map popups should present the minimum fact set required for immediate inspection.

### 5.9 Motion and animation

Motion is allowed only when it serves orientation or truth availability. Drawer collapse and restore may be animated. Hover/focus states may be subtle. Computed-truth staging may be explored later, but motion must never pretend computation is complete before it is complete. Game-like chrome, scanning theater, radar effects, speculative emergence, timing theater, or loading animations implying false precision are rejected.

Rain/Virga discovery systems are future-facing and must not enter active instructions until truth/topology and performance are stable. If they return, they must be tied to real computed truth or clearly treated as restrained reveal pacing, not fake solver behavior.

---

## 6. Screen and Workflow Canon

### 6.1 Entry and first chart creation

The entry surface should support sign in, account creation, and learning the product purpose without exposing advanced controls. First-time users should be guided toward creating a chart record, not dropped directly into a cluttered map. Birth data intake establishes trust. It should feel calm, premium, and serious, not like a scary form or a playful astrology quiz.

For the current active build, exact birth data is assumed. Approximate birth time, confidence ranges, and conversational intake belong to later governed layers and should not pollute the base workflow.

### 6.2 Dashboard and chart record

The dashboard is not the main decision surface. It is an orientation surface for chart records, saved objects, account utilities, settings, and navigation. The chart record is the central owner of saved searches, favorite locations, notes, comparisons, and history. Favorites and saved explorations belong to one chart record. Active chart context must not change silently.

The dashboard should avoid map clutter and deep technical controls. The map is opened from the chart context or selected chart context. Settings may include orb defaults, visual settings, house system, zodiac mode, and other configuration surfaces, but advanced settings should not overwhelm initial use.

### 6.3 Map exploration workflow

The core workflow is: choose chart context, configure conditions, search the map, inspect regions, click points or cities, save candidate locations, save searches if useful, and compare selected locations. This order matters. The map finds possibilities; the human evaluates. The city is not the starting point unless the user explicitly searches for a known place.

The map must support three entry patterns: condition-first exploration, city/location search, and arbitrary point inspection. All three converge on factual chart inspection, not automatic interpretation.

### 6.4 Favorites workflow

Favorite locations are chart-bound candidate objects. They may be named cities or arbitrary saved coordinates. A saved location can open a full relocated chart, receive notes, be added to a comparison, or be exported/shared. Ranking should be handled cautiously because the product doctrine avoids implying that one place is inherently better outside stated intention. Tags may be added only if they do not create clutter or a computer-code feeling.

### 6.5 Comparison workflow

Comparison should begin with two locations for one chart before expanding. The interface should show side-by-side relocated facts: planet-in-house, aspect-to-angle, angle-in-sign, current/natal context if useful, and notes. Three to five charts may be possible later, but cognitive overload is a risk. The first implementation should prioritize clarity and parity with manual runs. The comparison must not produce a synthesized winner by default.

### 6.6 Saved searches and shared views

Saved searches persist semantic intent and render snapshot context. They should not persist renderer internals as product truth. A saved search should restore chart context, condition variables, settings snapshot, and viewport enough to replay honestly. Shared views for clients may expose selected overlays and limited controls, possibly mute/solo, but should prevent clients from accidentally changing professional-selected conditions unless explicitly allowed. Shared views must feel elegant, minimal, and free of debug clutter.

### 6.7 Notes

Notes are persistent annotations but should remain restrained. The product should not become overly clinical or word-processor-like. Notes may support professional observations, client goals, session context, or saved-location commentary, but the base interface should not over-prompt users into a rigid methodology. AI-generated summaries, if ever added, must remain optional and clearly distinguished from user-authored notes.

### 6.8 Settings

Settings must separate Layer 1 compute parameters from Layer 2 preferences. Birth data, chart inputs, house system, zodiac mode, and condition semantics affect computation. Orb defaults, minor aspect preferences, visual settings, helper layers, ontology packs, and style presets are higher-level configuration. Settings snapshots must be captured for replay honesty. Layer 2 must not secretly alter Layer 1 membership.

---

## 7. Layer Model: Geometry, Ontology, Intent, Interpretation, and Experience

The archive’s interface doctrine repeatedly implies a layered model. The exact terminology may evolve, but the interface should preserve these boundaries.

### 7.1 Layer 1 — Geometry and factual computation

Layer 1 is chart inputs, ephemeris parameters, coordinates, house system, zodiac mode, angle geometry, condition membership, and exact point truth. This layer determines what is true at a location. UI must never mutate it through styling controls.

### 7.2 Layer 2 — Ontology and settings

Layer 2 governs vocabulary, enabled condition types, orb defaults, helper categories, style tokens, and professional/literacy presets. Ontology can change how users ask questions and which symbolic frameworks are available. It cannot falsify Layer 1 membership. Snapshots preserve replay honesty.

### 7.3 Layer 3 — User intent and workflow framing

Layer 3 includes user goals, saved investigation names, comparison intention, client context, and professional workflow. This layer organizes exploration without declaring objective superiority. It lets the user ask, “Where can I find this structure?” or “Which of these places better fits my stated intention?” without allowing the system to pretend a universal ranking exists.

### 7.4 Layer 4 — Interpretation and assistive language

Layer 4 is future optional interpretation, AI assistance, symbolic explanation, tradeoff analysis, and educational guidance. It must remain subordinate to human judgment. The active interface instructions must not depend on it. No AI UI should become primary navigation structure in the non-AI professional core.

### 7.5 Layer 5 — Experience and visual atmosphere

Layer 5 is the emotional and visual envelope: calm, premium, restrained, contemplative, map-first, long-session comfortable, non-interfering. It supports imagination without competing with it. It makes room for meaning-making without manufacturing certainty. It is never allowed to override factual surfaces.

---

## 8. Validation and Drift Control for Interface Work

Design changes must be validated as rigorously as backend changes when they affect truth perception.

### 8.1 Screenshot and interaction validation

UI slices should prove drawer collapse/restore preserves condition state, mute/solo does not alter payload truth, overlap remains readable at 1280×800 with drawer collapsed, and screenshot regression fixtures remain unchanged for truth regions. City labels and clickable candidate locations must remain visible under supported overlay states.

### 8.2 Debug separation

Debug geometry, trace conditions, validation overlays, status strings, internal metrics, and sampling diagnostics must not leak onto commercial UX surfaces. Debug mode can be powerful. Production mode must be calm. If a user-facing “show me your math” mode is added later, it must be deliberately designed and not simply expose raw developer clutter.

### 8.3 Anti-drift rules

Future agents and developers must not invent visual behavior without checking this canon. Feature flags, branches, and small prototypes are preferred for new encodings. Palette changes cannot move geometry. Typography changes cannot hide required facts. Animation cannot mask unfinished computation. Custom controls cannot break accessibility. Map library changes require evidence of blocker, not taste.

---

## 9. Active Non-Goals

The active design system does not include speculative Web3 frontend models, social feeds, engagement loops, dashboard gamification, automatic city scoring, AI-driven navigation, consumer oracle flows, broad animation systems, final visual style presets, rain/virga production animation, or multi-framework ontology marketplaces. These may live in future inventory if they remain relevant, but they are excluded from current build instructions.

---

## 10. Implementation Checklist

Before any interface change lands, the implementer should verify:

1. Does the change preserve “Reveal structure. Preserve judgment”?
2. Does it keep cities secondary to geography and condition fields?
3. Does it preserve popup truth over overlay impression?
4. Does it avoid auto-interpretation or hidden scoring?
5. Does it keep map real estate primary?
6. Does it avoid debug clutter in production?
7. Does it preserve condition snapshot immutability?
8. Does it distinguish display controls from semantic truth?
9. Does it preserve Layer 1 / Layer 2 separation?
10. Does it keep typography calm and facts scannable?
11. Does it preserve city label readability?
12. Does it preserve overlap inspectability?
13. Does it keep NOT/exclusion calm and non-punitive?
14. Does it avoid conflating cusp softness with aspect aura?
15. Does it avoid hidden renderer or payload mutations?
16. Does it include a rollback path or small-scope validation step?

---

## Future Experience Excellence Inventory

This inventory tracks upcoming interface optimizations without making them active setup instructions.

### Map and control refinement

- Full Genie/drawer production component after flexible condition rows and map-native location search are stable.
- Mobile bottom-sheet or compact drawer design for condition cards and layer controls.
- Dirty-state design for rendered snapshot vs edited conditions.
- Clear Map, Save Search, Back, Forward, and Pin placement finalization.
- LayerDisplayState, DrawerLayoutState, and ConditionDirtyFlag abstractions.

### Visual semantic refinement

- Deliberate semantic color-token system for house, angle-sign, aspect, overlap, and NOT families.
- Child-color overlap system to replace accidental alpha mud.
- Colorblind validation path and dark/light basemap behavior.
- Typography scale and spacing tokens for map chrome, popups, chart pages, comparison views, and exports.
- Subtle texture experiments for layer differentiation under transparency.

### Overlay and rendering experience

- Aspect-to-angle material-strip/aura visual refinement on top of validated geometry.
- Cusp transition display prototype with explicit explanatory affordance.
- Mute/solo/background/foreground layer mixer implementation.
- NOT/exclusion visual prototype after positive overlay palette stabilizes.
- Map-context sandbox validation for label readability, pane ordering, and zoom behavior.

### Workflow and saved-object polish

- Saved Search naming flow with optional human-editable suggestions.
- Favorite location management with notes and comparison selection.
- Two-city comparison MVP with side-by-side facts and no winner.
- Shared/client view export with restricted controls and clear exploration/authority tier.
- Professional defaults preset that exposes inspectability without splitting the app prematurely.

### Onboarding and learning

- One-time right-click/point-truth onboarding veil or spotlight.
- Calm chart-entry onboarding that avoids advanced terminology overload.
- Optional “show calculation” or debug-education mode, distinct from production chrome.
- Future educational material and professional training flows, governed separately from active interface.

### Deferred experience explorations

- Rain/Virga reveal systems only after truth substrate, performance, and semantic boundaries are stable.
- Selectable visual style presets that change palette/material language but never math or certainty.
- AI-assisted interpretation surfaces that remain optional, downstream, and clearly separated from factual UI.
- Advanced ontology/plugin UX after core professional workflow is stable.


---

## Appendix A — Extracted Design Source Index

### A.1 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/AI_WORKFLOW_GOVERNANCE.md`
- Categories: workflow_screens, architecture_bridge, validation_design
- Characters: 14272; SHA-12: `570f3cca823a`
- Key headings: AI Workflow Governance Protocol; Purpose; Ghost Boss Governance Doctrine; Dangerous Temporary-Forever Compromises; Mandatory Governance Closeout; Continuity Volume Protocol; Mandatory Closeout Checklist; When To Update `DEFERRED_EXCELLENCE_REGISTRY.md`; When To Update `CURRENT_RENDERING_DOCTRINE.md`; When To Create Validation Narratives
- Requirement signals:
  - Future AI agents should ingest continuity volumes before planning or implementation when a task touches governance, renderer doctrine, deferred excellence, product direction, or multi-phase continuity. Treat the volume as archaeology eviden…
  - Do not update the doctrine for product-only scaffolding unless it changes renderer boundaries or restates renderer constraints that future agents must obey.
  - - Rejected ideas or compromises: ...

### A.2 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/CURRENT_RENDERING_DOCTRINE.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 7576; SHA-12: `0b4a58929157`
- Key headings: Current Rendering Doctrine — Summary; The stack (top to bottom); Non-negotiables; Legacy `/search-regions` Truth Grid; Phase-2 cache (product substrate); Evidence bundle (read in this order); Documents marked SUPERSEDED (archaeology preserved); Warnings against backsliding; Remaining gaps (structural, not aesthetic); Recommendation

### A.3 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DEFERRED_EXCELLENCE_REGISTRY.md`
- Categories: workflow_screens, language_payload, architecture_bridge
- Characters: 30563; SHA-12: `8fdc70fc996d`
- Key headings: Deferred Excellence Registry; Purpose; Cross-Cutting Doctrine; Status Legend; 1. Renderer / Topology Improvements; 1.1 Stable component IDs across zoom/pan; 1.2 Graph / global path solver; 1.3 Canonical-default migration; 1.4 Continuous topology extraction refinement; 1.5 Subpixel/edge extraction refinement for narrow-orb ASC
- Requirement signals:
  - Rejection is not deferral — these are choices we will not casually revisit:

### A.4 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/DOCTRINE_INDEX.md`
- Categories: visual_semantics, workflow_screens, architecture_bridge
- Characters: 15975; SHA-12: `ffca0c0f93b1`
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene

### A.5 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/EXECUTIVE_TRANSFER_BRIEF_NEXT_CHAT.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 9792; SHA-12: `d91200d72161`
- Key headings: Executive Transfer Brief For Next Chat; 1. Current Project State; 2. What Is Considered Solved; 3. What Is Intentionally Deferred; 4. Current Renderer Status; 4.1 Renderer handoff state; 5. Governance Status; 6. Productization Status; 7. Immediate Next Recommended Phases; 8. Strategic Warnings
- Requirement signals:
  - Do not silently switch renderers. Do not auto-promote canonical. Do not treat visual mismatch as math failure without evidence.
  - - Rejected scope.
  - - Do not reopen renderer panic without evidence.
  - - Do not confuse representation artifacts with astrology math failures.
  - - Do not let local JSON persistence become permanent product storage by accident.

### A.6 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_1_2_EXTRACTION_AUDIT.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 31222; SHA-12: `99e7cbcf42db`
- Key headings: Phase 1.2 Extraction Audit; Concise Findings; Files Inspected; Production and backend; Sandboxes; Validation / capture scripts; Doctrine used as constraints; Current Rendering Entry Points; Production renderer; Backend endpoints
- Requirement signals:
  - must not change behavior and must not mix the legacy production overlay
  - Critical globals in this path:
  - Do not proceed to production adapter or canonical wiring in Phase 1.2.
  - - Do not run full screen-pixel adaptive captures for scheduler-only
  - should not change any of these.

### A.7 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 58355; SHA-12: `c6ef18d0c316`
- Key headings: Phase-2 Cache Integration — Architecture & Implementation Planning; 0. Where this fits; 1. Grounding — what is true today, measured; 1.1 Sandbox state (measured, not asserted); 1.2 What this means; 1.3 Hard architectural finding — substrate mismatch; 2. Production Scheduler Architecture; 2.1 Single-active-job model; 2.2 Foreground vs background queues; 2.3 Cancellation / interruption behaviour
- Requirement signals:
  - doctrine forbids). It exists because rapid user actions (zoom-tap +
  - must match the cache-key inputs in §2.7 of this document. Until that
  - should be recorded in `ai_context/decisions.md` as part of step 0.

### A.8 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_IMPLEMENTATION_PROTOCOL.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 54962; SHA-12: `c32fcebbd584`
- Key headings: Phase-C Implementation Protocol; Operational constitution for landing the validated architecture without future chaos; 0. Where this fits; 1. Implementation Phase Breakdown; Phase 1.1 — Documentation alignment (no code); Phase 1.2 — Archaeology fencing (low-risk cleanup); Phase 1.3 — Scheduler extraction (no behaviour change); Phase 1.4 — Substrate adapter scaffold (legacy-only); Phase 1.5 — Canonical substrate wiring (flag-gated); Phase 1.6 — Scheduler/cache wiring on canonical (flag-gated)
- Requirement signals:
  - Doctrine regressions are real regressions. They block phase advance
  - future coding AI) participate in Phase-C work. It is **distinct from**

### A.9 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_PRODUCTION_MIGRATION_PLAN.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 64644; SHA-12: `af96b1d10c2e`
- Key headings: Phase-C Production Migration Plan; Legacy overlay pipeline → canonical screen-space adaptive substrate; 0. Where this fits; 1. Legacy vs Canonical Substrate Audit; 1.1 The legacy overlay pipeline (what is in production today); 1.2 The canonical screen-space substrate (validated, sandbox-proven); 1.3 Semantic differences; 1.4 Rendering differences (visible); 1.5 Cache compatibility implications; 1.6 Validation differences
- Requirement signals:
  - must classify both world copies independently and consistently.
  - Do not delete the endpoint code. It remains callable for offline

### A.10 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PHASE_C_RENDERING_ARCHITECTURE.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 47288; SHA-12: `3744bf667647`
- Key headings: Phase C — Rendering Substrate Architecture (Governing Laws); 0. Where this document sits; 1. Canonical Rendering Truths; 1.1 The four absolute statements; 1.2 Screen-space truth doctrine; 1.3 Adaptive refinement as production substrate; 1.4 Why visible output is canonical; 1.5 Globe truth vs screen truth; 2. Convergence Strategy; 2.1 Convergence is the contract; sample count is not
- Requirement signals:
  - must follow the same shape: name, fixture, validation pass, doctrine note.
  - - Future palette work uses **deliberate child colors** for known overlap
  - Forbidden visual states, even when the underlying occupancy is truthful:
  - should be **reclassified as superseded** with a header pointing at
  - must be made explicit:

### A.11 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/PROJECT_CONTINUITY_INDEX.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 2667; SHA-12: `303dae8aa89c`
- Key headings: Project Continuity Index; Canonical Governance Docs; Canonical Archaeology Docs; Canonical Renderer Doctrine Docs; Deferred Excellence; Validation Narratives; Continuity Volume Convention; Recommended Future-AI Ingestion Order
- Requirement signals:
  - Do not promote raw continuity claims into doctrine without cross-checking current docs and code.

### A.12 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 22169; SHA-12: `b7b7a39122bb`
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit

### A.13 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/ai_constitution_and_review_architecture.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 13119; SHA-12: `d6ae8f16c65e`
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal)

### A.14 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/client_chart_data_model_v1_2026-05-29.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 35789; SHA-12: `795365723409`
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases
- Requirement signals:
  - - forbidden renderer keys in investigation JSON.
  - Future revisions: append date to filename (`client_chart_data_model_v2_YYYY-MM-DD.md`) or bump version segment per repo doc convention.

### A.15 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/architecture/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 20953; SHA-12: `db53e1e91227`
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning

### A.16 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/aspect_aura_defaults.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 1291; SHA-12: `2e467a76fee6`
- Key headings: Aspect aura defaults (approximate display); Authority; Default screen weights (Leaflet `weight`, approximate); NOT done here

### A.17 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/brand_and_experience_foundations.md`
- Categories: visual_semantics, language_payload, architecture_bridge
- Characters: 12722; SHA-12: `d3afa8b142af`
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles
- Requirement signals:
  - - Reject **generic SaaS** purple-teal dashboards, **neon** map accents, and **toy astrology** glitter.
  - - Reject **debug clutter** as default UI; instrumentation stays in explicit debug modes.
  - - Reject **ornamental texture and gradient** unless it carries **semantic** weight (and even then, keep it **subconscious**).

### A.18 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/cartographic_language_and_city_rendering.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 18608; SHA-12: `33b4db97eb55`
- Key headings: Cartographic language and city rendering; 0. Basemap or tile strategy change ⇒ full visual identity re-test; 1. Map label language vs app language; 2. Provider evaluation (map + search); 2.1 Dimensions to score (required for any serious comparison); 2.2 Qualitative stack comparison (high level); 2.3 “Extra hour” vs “multi-day / multi-week”; 2.4 Effort bands for “whole solution” slices; 2.5 GeoNames bridge first vs “long-term now”; 3. City visibility under overlays (hard constraint)
- Requirement signals:
  - - Avoid **million-dot** clutter and **empty-ocean** deserts where possible—tune by **visible density** and QA (`geocoder_and_city_strategy.md`).

### A.19 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/README.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 2857; SHA-12: `1e003b635a0c`
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - - future excellence,
  - Do not silently merge hard constitutional doctrine with tentative future-feature planning.

### A.20 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/constitutional_ingestion_checklist.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 3060; SHA-12: `3ace0cd9a495`
- Key headings: Constitutional Ingestion Checklist; Status; Purpose; Folder Structure; Canonical Constitutional Docs; Core Constitutional Layer; Runtime / Governance Constitutional Layer; Conversational / Interpretive Constitutional Layer; Semi-Canonical / Strategic Docs; Strategic / Future Architecture Layer
- Requirement signals:
  - - doctrine evolves,
  - * future planning,
  - * doctrine may require refinement,

### A.21 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/implementation_governance_and_ai_workflow_protocol.md`
- Categories: workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 3988; SHA-12: `b127e5c52050`
- Key headings: Implementation Governance And AI Workflow Protocol; Status; Purpose; Core Principle; Architectural integrity is more important than implementation speed.; AI Workflow Principle; One Change At A Time; Rollback Discipline; Commit Discipline; Sandbox Before Production
- Requirement signals:
  - should remain independently inspectable.
  - - future extensibility,

### A.22 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer4_optimization_and_exploration_doctrine.md`
- Categories: architecture_bridge, validation_design
- Characters: 4341; SHA-12: `289b4552320f`
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both
- Requirement signals:
  - Future Layer 4 systems may eventually include:

### A.23 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layer_sovereignty_and_forbidden_crossings.md`
- Categories: architecture_bridge
- Characters: 3715; SHA-12: `76af8fdb4707`
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.
- Requirement signals:
  - - forbidden crossings,
  - must remain infrastructure only.
  - must remain grounded in:

### A.24 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/layered_symbolic_intelligence_architecture.md`
- Categories: architecture_bridge
- Characters: 4801; SHA-12: `5242de0598f3`
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.
- Requirement signals:
  - - forbidden crossings,

### A.25 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/map_first_product_doctrine_v1.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 9016; SHA-12: `a67e60eba18a`
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class
- Requirement signals:
  - Avoid drifting toward “Map → everything else.”
  - Do not force workflow around Intent Summary in Web 2.0.
  - Future relationship support uses **linked Chart Records** — not nested charts.
  - Future AI should:
  - Do not propose or implement:

### A.26 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/mvp_beta_and_future_feature_roadmap.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 4767; SHA-12: `c904d8af5d1e`
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes
- Requirement signals:
  - Future growth must preserve:

### A.27 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: map_workspace, language_payload, architecture_bridge
- Characters: 3617; SHA-12: `f6bab89d14d7`
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology
- Requirement signals:
  - Future systems may allow professionals to:
  - Future implementation should preserve:

### A.28 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/professional_mode_vs_lay_mode_strategy.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 3492; SHA-12: `c166907d611f`
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role
- Requirement signals:
  - - do not know astrological terminology,

### A.29 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/purification_audit_framework.md`
- Categories: architecture_bridge, validation_design
- Characters: 3639; SHA-12: `a43528565790`
- Key headings: Purification Audit Framework; Status; Purpose; Core Principle; Architectural purity is easier to preserve than to restore.; What A Purification Audit Is; Layer Purity Checks; Layer 1 Checks; Layer 2 Checks; Layer 3 Checks
- Requirement signals:
  - Future features must remain:

### A.30 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_and_renderer_sovereignty.md`
- Categories: visual_semantics, map_workspace, language_payload, architecture_bridge
- Characters: 3826; SHA-12: `edda50b52a22`
- Key headings: Runtime And Renderer Sovereignty; Purpose; Core Principle; Rendering must never alter truth.; Runtime Sovereignty; Renderer Sovereignty; Hydration Boundaries; Sandbox Boundaries; Observer Limitations; Renderer Substrate Integrity

### A.31 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/runtime_build_sequence_and_timeline.md`
- Categories: visual_semantics, map_workspace, language_payload, architecture_bridge
- Characters: 4934; SHA-12: `12aea4343437`
- Key headings: Runtime Build Sequence And Timeline; Status; Maintenance Notes; Purpose; Core Principle; Build irreversible foundations first.; Phase Family 1 — Truth And Runtime Foundation; Goal; Includes; Status
- Requirement signals:
  - - avoid rabbit-hole development,
  - - future expansion,
  - Future development should remain:

### A.32 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/constitutional/symbolic_language_style_guide.md`
- Categories: visual_semantics, language_payload
- Characters: 1703; SHA-12: `11e6dd9bdb1a`
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal

### A.33 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_app_shell_handoff_audit_v1_2026-05-30.md`
- Categories: map_workspace, language_payload, validation_design
- Characters: 16528; SHA-12: `a7754235e25c`
- Key headings: Genie → App Shell Handoff Audit v1; Status; Executive summary; A. Current Genie contract; Emitter; Trigger; Payload shape (as implemented); Variable semantics (canonical); Output destinations today; Not emitted / not connected

### A.34 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/genie_render_payload_v1_2026-05-30.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 27674; SHA-12: `7e997018eed9`
- Key headings: Genie Render Payload Contract v1; Status; Purpose; Architectural doctrine; Language stability doctrine; Principles; Therefore; Top-level payload; Field notes; Render immutability

### A.35 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/contracts/variable_card_language_v1_2026-05-30.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 15184; SHA-12: `bde701502163`
- Key headings: Variable Card Language Contract v1; Status; Purpose; Core doctrine; Canonical internal type IDs; Language registry concept; Composition rule; Registry ownership; Snapshot rule (Saved Explorations); Beta display label candidates
- Requirement signals:
  - Never persist dropdown display strings as semantic keys. Persist registry ids only.

### A.36 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/current_sidebar_ux_audit.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, validation_design
- Characters: 4992; SHA-12: `c07666b5828f`
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces

### A.37 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/local_first_data_objects_v1.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 8758; SHA-12: `90256838acac`
- Key headings: Local-First Data Objects v1; Status; Purpose; Architectural boundary; Entity glossary; ProfessionalAccount; Client; BirthProfile; RelocatedChart (future durable object); Place
- Requirement signals:
  - - must be labeled in code and docs as non-product storage
  - - future: `candidateChartDomains[]` for multi-domain cache — **schema reserved, not MVP-rendered**.

### A.38 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/data_model/supabase_schema_sandbox_plan_v1.md`
- Categories: visual_semantics, map_workspace, architecture_bridge, validation_design
- Characters: 16155; SHA-12: `8fac31540a5b`
- Key headings: Supabase Schema Sandbox Plan v1; Status; Explicit non-goals (current phase); Architectural boundary; 1. Proposed table list; 2. Columns per table; `professional_accounts`; `clients`; `birth_profiles`; `places`

### A.39 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/design/brand_visual_language_and_design_doctrine.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 7092; SHA-12: `cc31d7224c14`
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing
- Requirement signals:
  - - reject prophetic, destiny, cosmic guarantee language,
  - Must **not** change:

### A.40 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 7243; SHA-12: `f8208d0d336f`
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording
- Requirement signals:
  - - never silently treat a guess as exact.
  - - never overwrite certificate time without audit trail.

### A.41 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/future/layer5_experiential_education_through_travel_v1.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 7769; SHA-12: `9ca3e64754b9`
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only)
- Requirement signals:
  - Do not implement Layer 5 education until **all** are true:

### A.42 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_and_city_identity_strategy.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 7774; SHA-12: `1f2f2dd177f3`
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data

### A.43 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/geocoder_dataset_feasibility.md`
- Categories: visual_semantics, map_workspace, language_payload, architecture_bridge, validation_design
- Characters: 16429; SHA-12: `6ba544bcfafd`
- Key headings: Geocoder dataset feasibility (planning pass); 1. Summary recommendation; 2. Option-by-option evaluation; 2.1 GeoNames — `cities500` / `cities1000` / `allCountries`; 2.2 Natural Earth — populated places (`ne_10m_populated_places`); 2.3 Who’s On First (WOF); 2.4 Pelias / Geocode Earth (open-data stack vs hosted); 2.5 Mapbox / Google (hosted geocoding & Places); 3. Licensing notes (high level — verify before ship); 4. Rough import plan (GeoNames-first)

### A.44 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/governance/anti_cursor_bullshit_governance_rules.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 8314; SHA-12: `790aab0faf7d`
- Key headings: Anti-Cursor Bullshit Governance Rules; Status; Purpose; Non-negotiables; Before you touch code; Forbidden agent behaviors; Truth and evidence; Architecture; Documentation; Product / UX
- Requirement signals:
  - - rejected scope,
  - - forbidden shortcuts listed,

### A.45 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_memory_synthesis.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 16257; SHA-12: `04f378dc370d`
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine

### A.46 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/institutional_philosophical_synthesis.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 27007; SHA-12: `d9ca2489a35d`
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome
- Requirement signals:
  - - Avoid **good/bad placement** infantilism while still allowing **honest difficulty**: not every placement is “neutral”; moral judgment belongs in **lived ethics**, but **structural cost** is a legitimate teaching topic.

### A.47 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/intentionality_and_symbolic_constraints.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 8365; SHA-12: `d1c233003983`
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract

### A.48 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/map_and_overlay_design_research.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 5149; SHA-12: `f3943cdf7cf9`
- Key headings: Map and Overlay Design Research; 1. Leaflet vs MapLibre vs Google Maps (philosophical comparison); 2. Current Leaflet strengths (for this codebase); 3. Actual blockers to watch for (hypothesis list—not confirmed); 4. Overlay transparency strategy (research directions); 5. Semantic overlap colors; 6. Aura rendering directions (non-commitments); 7. Map-edge and world-wrap ideas; 8. Dark / light mode implications; 9. Multilingual city rendering

### A.49 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/next_implementation_sequence.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 10690; SHA-12: `ced0e563c90b`
- Key headings: Next Implementation Sequence; Priority band 1 — UX polish (minimal architecture risk); Chunk 1.1 — Sidebar density and “debug vs ship” clarity; Chunk 1.2 — Popup and typography refinement; Chunk 1.3 — Native select stability + legend clutter reduction; Priority band 2 — Validator / stress tooling; Chunk 2.1 — Fixture manifest + “run these five” script; Chunk 2.2 — Latitude / polar stress suite expansion; Chunk 2.3 — Brute-force / truth export hygiene; Priority band 3 — Account + birth-data workflows

### A.50 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/00_OPERATOR_START_HERE.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 697; SHA-12: `a0e79ddfcf29`
- Key headings: AI Onboarding Entry Point

### A.51 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/2026-05-29_application_journey_architecture_v1.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 32245; SHA-12: `8ebf2b906395`
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision
- Requirement signals:
  - - Never required to continue exploration
  - Forbidden gates: required intention fields; required tags; required AI summary; required comparison verdict before save.
  - future/             # Confidence tiers, deferred features, exploratory specs

### A.52 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/DOCTRINE_INDEX.md`
- Categories: visual_semantics, workflow_screens, architecture_bridge
- Characters: 15975; SHA-12: `ffca0c0f93b1`
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene

### A.53 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/README.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 2857; SHA-12: `1e003b635a0c`
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - - future excellence,
  - Do not silently merge hard constitutional doctrine with tentative future-feature planning.

### A.54 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_CONSTITUTION.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 34207; SHA-12: `5e220ad77dad`
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists
- Requirement signals:
  - - Do not claim full desktop parity in marketing or UX copy until inspect gesture exists.
  - - Forbidden silent chart switch; confirm when dirty draft.

### A.55 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/UX_DOCTRINE_MASTER.md`
- Categories: map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 52041; SHA-12: `85f4ed2fffef`
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application

### A.56 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/client_chart_data_model_v1_2026-05-29.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 35789; SHA-12: `795365723409`
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases
- Requirement signals:
  - - forbidden renderer keys in investigation JSON.
  - Future revisions: append date to filename (`client_chart_data_model_v2_YYYY-MM-DD.md`) or bump version segment per repo doc convention.

### A.57 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/intentionality_and_symbolic_constraints.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 8365; SHA-12: `d1c233003983`
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract

### A.58 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/map_first_product_doctrine_v1.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 9016; SHA-12: `a67e60eba18a`
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class
- Requirement signals:
  - Avoid drifting toward “Map → everything else.”
  - Do not force workflow around Intent Summary in Web 2.0.
  - Future relationship support uses **linked Chart Records** — not nested charts.
  - Future AI should:
  - Do not propose or implement:

### A.59 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/product_screen_and_transition_architecture.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 9275; SHA-12: `8187d0e4980f`
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record
- Requirement signals:
  - Never export renderer debug artifacts as product truth.
  - Do not claim mobile parity until inspect gesture exists.

### A.60 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/professional_non_ai_workflow_v1.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 9566; SHA-12: `3de8663545ba`
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth

### A.61 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_ai_product_core/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: workflow_screens, architecture_bridge
- Characters: 3360; SHA-12: `554add110fa4`
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact

### A.62 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/DOCTRINE_INDEX.md`
- Categories: visual_semantics, workflow_screens, architecture_bridge
- Characters: 15975; SHA-12: `ffca0c0f93b1`
- Key headings: Doctrine index; Philosophy, intentionality, and institutional synthesis; AI governance and interpretive systems; Meta-governance / institutional maintenance; Rendering substrate architecture; UX, experience, and product roadmap; Visual semantics, overlays, and cartography; Place search, identity, data feasibility; Validation, proof, and quality; Institutional memory, archaeology, hygiene

### A.63 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/README.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 2857; SHA-12: `1e003b635a0c`
- Key headings: Constitutional Doctrine Index; Purpose; Doctrine Categories; Canonical; Semi-Canonical; Roadmap; Exploratory; Operational Infrastructure; Core Governance; Maintenance
- Requirement signals:
  - - future excellence,
  - Do not silently merge hard constitutional doctrine with tentative future-feature planning.

### A.64 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_CONSTITUTION.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 34207; SHA-12: `5e220ad77dad`
- Key headings: UX Constitution; Document status; 1. Product Philosophy; Principle; Why it exists; Required behaviors; Forbidden behaviors; 2. Map-First Doctrine; Principle; Why it exists
- Requirement signals:
  - - Do not claim full desktop parity in marketing or UX copy until inspect gesture exists.
  - - Forbidden silent chart switch; confirm when dirty draft.

### A.65 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/UX_DOCTRINE_MASTER.md`
- Categories: map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 52041; SHA-12: `85f4ed2fffef`
- Key headings: UX Doctrine Master; Document status; Part 1 — UX Doctrine; UX-D-001 — Product identity: relocation discovery instrument; UX-D-002 — Center of gravity: Map → Analysis → Administration; UX-D-003 — Map First ≠ Map Only; Map and Chart Page are co-stars; UX-D-004 — Primary application surfaces; UX-D-005 — Chart Record utility route is not a SaaS Dashboard; UX-D-006 — Preferred landing: Map-first; UX-D-007 — The Map is not a feature; the Map is the application

### A.66 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/constitutional_summary.md`
- Categories: workflow_screens, architecture_bridge
- Characters: 4609; SHA-12: `8238f401edb1`
- Key headings: Constitutional Summary; Purpose; Layer Architecture; Layer 1 - Truth; Layer 2 - Symbolic Ontology; Layer 3 - Intentional Interpretation; Layer 4 - Exploratory Optimization; Forbidden Crossings; Epistemic Doctrine; Runtime And Renderer Sovereignty

### A.67 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/epistemic_integrity_and_symbolic_humility.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 3739; SHA-12: `242cc62cfae5`
- Key headings: Epistemic Integrity And Symbolic Humility; Status; Purpose; Core Principle; Honest uncertainty is superior to symbolic overreach.; Symbolic Humility; Important Principle; Not every life event maps cleanly to astrology.; Forbidden Behavior; Examples Of Bad Behavior

### A.68 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/intentionality_and_symbolic_constraints.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 8365; SHA-12: `d1c233003983`
- Key headings: Intentionality and symbolic constraints; 1. Fate exists (structural realism); 2. Agency exists within constraints (relocation reframed); 3. Tradeoff intelligence (optimization, not fantasy); 4. Honest asymmetry (no flattering erasure); 5. Dynamic participation (between fatalism and naive free will); 6. AI interpretation implications (governance); 7. Product positioning implications (sober, not cynical); 8. Relationship to the broader product (intentionality as engine); Review contract

### A.69 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layer_sovereignty_and_forbidden_crossings.md`
- Categories: workflow_screens, architecture_bridge
- Characters: 3715; SHA-12: `76af8fdb4707`
- Key headings: Layer Sovereignty And Forbidden Crossings; Status; Purpose; Core Principle; Every layer owns a different category of intelligence.; Constitutional Rule; Lower layers are sovereign over higher layers.; Layer Ownership Summary; Forbidden Crossing #1; Layer 2 may NOT alter Layer 1 truth.
- Requirement signals:
  - - forbidden crossings,
  - must remain infrastructure only.
  - must remain grounded in:

### A.70 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/layered_symbolic_intelligence_architecture.md`
- Categories: workflow_screens, architecture_bridge
- Characters: 4801; SHA-12: `5242de0598f3`
- Key headings: Layered Symbolic Intelligence Architecture; Status; Purpose; Core Principle; Lower layers may inform higher layers.; Higher layers may NEVER rewrite lower layers.; The Four Primary Layers; Layer 1 — Truth Layer; Purpose; WHAT IS.
- Requirement signals:
  - - forbidden crossings,

### A.71 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/map_first_product_doctrine_v1.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 9016; SHA-12: `a67e60eba18a`
- Key headings: Map-First Product Doctrine v1; Status; Core product identity; Critical correction: Map First ≠ Map Only; Primary application surfaces; Chart Record utility route (not a SaaS Dashboard); Map doctrine; Chart Page doctrine; Canonical module order; Current Location is first-class
- Requirement signals:
  - Avoid drifting toward “Map → everything else.”
  - Do not force workflow around Intent Summary in Web 2.0.
  - Future relationship support uses **linked Chart Records** — not nested charts.
  - Future AI should:
  - Do not propose or implement:

### A.72 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/01_core_authority/truth_vs_astrological_fact_vs_interpretation.md`
- Categories: workflow_screens, architecture_bridge
- Characters: 3360; SHA-12: `554add110fa4`
- Key headings: Truth vs Astrological Fact vs Interpretation; Purpose; Layer Distinction; Truth; Astrological Fact; Interpretation; Truth; Examples Of Truth; Astrological Fact; Examples Of Astrological Fact

### A.73 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/2026-05-29_application_journey_architecture_v1.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 32245; SHA-12: `8ebf2b906395`
- Key headings: Application Journey Architecture v1; Status; Purpose; Co-primary surfaces: Map and Chart Page; Discovery → Analysis loop; Core UX Principles; 1. Exploration Momentum Doctrine; 2. Interface Recedes Doctrine; 3. User Sovereignty Doctrine; 4. Discovery → Refinement → Evaluation → Decision
- Requirement signals:
  - - Never required to continue exploration
  - Forbidden gates: required intention fields; required tags; required AI summary; required comparison verdict before save.
  - future/             # Confidence tiers, deferred features, exploratory specs

### A.74 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/PLAIN_LANGUAGE_PRODUCT_EXPLANATION_v1_2026-06-01.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 6093; SHA-12: `0c7a9042f0a5`
- Key headings: Plain Language Product Explanation; What Problem Does The Product Solve?; Why Relocation Astrology Is Geographic; Why The Map Is The Primary Discovery Instrument; What Overlays Represent; Why Cities Are Not The Primary Object Of Analysis; Natal Chart; Current Location Chart; Candidate Location Chart; Favorites

### A.75 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_constitution_and_review_architecture.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 13121; SHA-12: `96b9567947d8`
- Key headings: AI constitution and review architecture; 1. Purpose of AI governance; 2. Core risk: interpretive drift; 3. Constitutional model (three layers); 4. Anti-pattern inventory; 5. Reviewer-agent responsibilities; 6. Symbolic restraint doctrine; 7. Relationship to UX philosophy; 8. Long-term implementation ideas (non-binding); 9. Positioning implications (internal)

### A.76 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ai_interpretation_truthfulness_doctrine_v1_2026-05-30.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 22169; SHA-12: `b7b7a39122bb`
- Key headings: AI Interpretation Truthfulness Doctrine v1; Status; Purpose; Why this doctrine matters; Core doctrine; Macro → micro interpretation rule; Direction of travel; Metaphor (teaching copy); Descriptive but not mute; Allowed — plausible fit

### A.77 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/birth_time_uncertainty_and_confidence_doctrine.md`
- Categories: map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 7243; SHA-12: `f8208d0d336f`
- Key headings: Birth Time Uncertainty and Confidence Doctrine; Status; Purpose; Core principle; Confidence tiers; User-facing copy principles; Do; Do not; Engine behavior matrix (MVP boundaries); Data recording
- Requirement signals:
  - - never silently treat a guess as exact.
  - - never overwrite certificate time without audit trail.

### A.78 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_and_experience_foundations.md`
- Categories: visual_semantics, workflow_screens, language_payload, architecture_bridge
- Characters: 12722; SHA-12: `d3afa8b142af`
- Key headings: Brand and Experience Foundations; Emotionally non-interfering design; Interpretive language and emotional transparency; Interpretive integrity and archetypal honesty; Emotional tone; Restraint philosophy; Contemplative interaction goals; Analytical / professional atmosphere; Visual honesty; Anti-overdesign principles
- Requirement signals:
  - - Reject **generic SaaS** purple-teal dashboards, **neon** map accents, and **toy astrology** glitter.
  - - Reject **debug clutter** as default UI; instrumentation stays in explicit debug modes.
  - - Reject **ornamental texture and gradient** unless it carries **semantic** weight (and even then, keep it **subconscious**).

### A.79 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/brand_visual_language_and_design_doctrine.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 7092; SHA-12: `cc31d7224c14`
- Key headings: Brand, Visual Language, and Design Doctrine; Status; Purpose; Brand posture (non-marketing); Visual epistemology (truth hierarchy); Color language; Principles; Layer families (target); Rejected aesthetics; Typography and spacing
- Requirement signals:
  - - reject prophetic, destiny, cosmic guarantee language,
  - Must **not** change:

### A.80 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/client_chart_data_model_v1_2026-05-29.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 35789; SHA-12: `795365723409`
- Key headings: Client / Chart Data Model v1; Status; Purpose; Continuity hierarchy; Core architectural boundary; Terminology; Terminology crosswalk (storage vs product language); 1. Chart Record / client model; Current scope (hard decision); Alternate charts and special cases
- Requirement signals:
  - - forbidden renderer keys in investigation JSON.
  - Future revisions: append date to filename (`client_chart_data_model_v2_YYYY-MM-DD.md`) or bump version segment per repo doc convention.

### A.81 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/conversational_discovery_and_intentionality.md`
- Categories: visual_semantics, workflow_screens, language_payload, architecture_bridge
- Characters: 4218; SHA-12: `c7b5d8b9fc8e`
- Key headings: Conversational Discovery And Intentionality; Status; Purpose; Core Principle; User intentionality is sovereign.; Intentionality Discovery; Examples; Archetypal Exploration; Example Exploratory Style; Intentionality Strength

### A.82 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/core_product_truths.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 9535; SHA-12: `9d9048f7cab4`
- Key headings: Core Product Truths; Astrology Truth; Inspectability; Map and Overlay UX; Product Experience; Visual / Semantic Product Identity; Emotionally non-interfering design (experiential constraints); Interpretive language and emotional transparency (doctrine); Interpretive integrity and archetypal honesty (doctrine); Development Discipline
- Requirement signals:
  - - Avoid overdesign and clever interactions that create artificial stupidity.
  - - Avoid large rewrites when the current milestone is working.

### A.83 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/geocoder_and_city_identity_strategy.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 7774; SHA-12: `1f2f2dd177f3`
- Key headings: Geocoder and city identity strategy; 1. Doctrine: city search is core systems engineering; 2. Required interaction model (target); 3. Ranking hierarchy (target function); Disambiguation examples (intent); 4. Data and identity requirements; 5. Offline / cache (later); 6. Map engine and provider tension; 7. Professional astrology workflows; 8. Blocked by current prototype data

### A.84 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/map_drawer_and_layer_control_doctrine.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 7226; SHA-12: `181a6ad8f6bd`
- Key headings: Map Drawer and Layer Control Doctrine; Status; Purpose; Control hierarchy (map screen); Drawer architecture (target); Zones; Genie-into-corner collapse; Deferral (current phase); Condition editor doctrine; Target model
- Requirement signals:
  - - avoid Photoshop panel chaos.
  - - never expose full stack at once,

### A.85 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/product_screen_and_transition_architecture.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 9275; SHA-12: `8187d0e4980f`
- Key headings: Product Screen and Transition Architecture; Status; Purpose; Information architecture (top level); Screen catalog; S0 — Chart Record utility (not SaaS home); S1 — Chart Page (analysis hub); S2 — Map exploration (co-primary; preferred landing); S3 — Comparison workspace; S4 — Full chart / relocated record
- Requirement signals:
  - Never export renderer debug artifacts as product truth.
  - Do not claim mobile parity until inspect gesture exists.

### A.86 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_mode_vs_lay_mode_strategy.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 3492; SHA-12: `c166907d611f`
- Key headings: Professional Mode vs Lay Mode Strategy; Status; Maintenance Notes; Purpose; Core Principle; The platform should remain professionally trustworthy while still accessible to non-professionals.; Professional Mode; Purpose; Professional Characteristics; Professional AI Role
- Requirement signals:
  - - do not know astrological terminology,

### A.87 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_non_ai_workflow_v1.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 9566; SHA-12: `3de8663545ba`
- Key headings: Professional Non-AI Workflow v1; Status; Purpose; Core workflow principle; Actor model; Primary workflow loop; Step 1 — Establish Chart Record context; Step 2 — Declare investigation conditions; Step 3 — Search and read overlap; Step 4 — Inspect point truth

### A.88 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_trust_and_ai_behavior_doctrine.md`
- Categories: workflow_screens, architecture_bridge
- Characters: 4267; SHA-12: `0c22e1113b72`
- Key headings: Professional Trust And AI Behavior Doctrine; Purpose; Core Principle; Honest uncertainty is superior to fabricated certainty.; AI Must Prefer Truth Over Comfort; Bounded Confidence; The AI Must Tolerate Uncertainty; Collaborative Discovery; Symbolic Humility; No Fake Omniscience

### A.89 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/professional_workflow_and_explanatory_language.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 11541; SHA-12: `1814ff883a7c`
- Key headings: Professional Workflow And Explanatory Language; Status; Purpose; Professional Map Workflow; Desired Placement Search; Exclude / NOT Variables; Solo And Mute Controls; Inspection Workflow; Helper Layers; Intention Remains Primary
- Requirement signals:
  - - future help text,

### A.90 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/symbolic_language_style_guide.md`
- Categories: visual_semantics, workflow_screens, language_payload, architecture_bridge
- Characters: 1703; SHA-12: `11e6dd9bdb1a`
- Key headings: Symbolic Language Style Guide; Purpose; Core Principle; Preferred Style; Avoid; Good Examples; Bad Examples; Archetypal Precision; Symbolic Humility; Constitutional Goal

### A.91 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/ux_principles_and_emotional_tone.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 4906; SHA-12: `3924025d2ba8`
- Key headings: UX Principles and Emotional Tone; 1. Core temperament; 2. Map-first atmosphere; 3. Delight without spectacle; 4. Overlap readability philosophy; 5. Typography and color tone; 6. Layout cautions: drawer / genie / chrome; 7. Mobile and tablet; 8. When to stop designing; 9. Where philosophy is already strong in the repo

### A.92 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/02_product_understanding/visual_semantic_style_guide.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 9451; SHA-12: `93105f1b5ba9`
- Key headings: Visual & Semantic Style Guide (Relocation Map System); 1. Visual epistemology (truth hierarchy); 2. House field semantics (categorical + cusp softness); 3. Aspect-to-angle aura semantics (intensity, not category); 4. Overlay texture semantics (almost subconscious); 5. NOT / exclusion overlays; 6. Color philosophy; 7. Popup visual language; 8. Interface tone; 9. Map and control relationship

### A.93 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ai_conversational_modes.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 2887; SHA-12: `b796e2065486`
- Key headings: AI Conversational Modes; Status; Purpose; Core Principle; Example User Modes; Executive Mode; Explorer Mode; Professional Mode; Distressed User Mode; Mode Safety
- Requirement signals:
  - Future implementation should preserve:

### A.94 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/archaeology_and_synthesis_workflow.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 9005; SHA-12: `d3add7674811`
- Key headings: Archaeology and synthesis workflow; 1. Pipeline overview; 2. When to create an archaeology pass; 3. When to create or update synthesis docs; 4. Durable truths vs transient implementation; 5. How to avoid flattening nuance during synthesis; 6. Preserving contradictory but valuable tensions; 7. Doctrine canonicalization; 8. Open tension preservation; 9. Institutional memory updating (rhythm)

### A.95 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/decision_and_uncertainty_framework.md`
- Categories: visual_semantics, workflow_screens, architecture_bridge
- Characters: 9068; SHA-12: `4b8f251dada4`
- Key headings: Decision and uncertainty framework; 1. Bounded uncertainty; 2. Heuristic vs exact truth; 3. Symbolic plausibility vs fake precision; 4. Exploratory guidance vs deterministic recommendation; 5. Preserving ambiguity intentionally; 6. Reversible decisions; 7. Experimentation doctrine; 8. User-facing confidence vs backend uncertainty; 9. “Good enough for exploration” vs “authoritative truth”
- Requirement signals:
  - Avoid **confidence cosplay**: precise typography on unverified city matches; “AI certainty” voice on interpretive guesses.

### A.96 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/doctrine_review_cycle.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 9902; SHA-12: `00598386986c`
- Key headings: Doctrine review cycle; 1. What this cycle protects; 2. Slow docs policy; 3. Implementation vs philosophy separation; 4. Tension-preservation doctrine; 5. Rationale preservation rules (“why”, not just “what”); 6. Review cadences (suggested, not ceremonial); 6.1 Doctrine coherence review; 6.2 AI drift audit; 6.3 UX coherence review
- Requirement signals:
  - - Open questions file cleared because “we should look decisive.”

### A.97 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/future_excellence_vs_future_feature_excellence.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 3941; SHA-12: `46cc032cf2b8`
- Key headings: Future Excellence vs Future Feature Excellence; Status; Maintenance Notes; Purpose; Core Principle; Infrastructure excellence and feature excellence must remain distinct.; Future Excellence; HOW the system is built.; Examples Of Future Excellence; Future Feature Excellence
- Requirement signals:
  - - future-oriented planning,
  - Future Excellence refers to:
  - Future Feature Excellence refers to:
  - must survive every expansion.

### A.98 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer4_optimization_and_exploration_doctrine.md`
- Categories: workflow_screens, architecture_bridge, validation_design
- Characters: 4341; SHA-12: `289b4552320f`
- Key headings: Layer 4 Optimization And Exploration Doctrine; Status; Maintenance Notes; Purpose; WHAT ELSE MAY BE POSSIBLE.; Core Principle; Layer 4 is subordinate to intentionality.; Subtractive Before Additive; Examples; Strong Relocations Often Do Both
- Requirement signals:
  - Future Layer 4 systems may eventually include:

### A.99 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/layer5_experiential_education_through_travel_v1.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 7769; SHA-12: `9ca3e64754b9`
- Key headings: Layer 5 — Experiential Education Through Travel; Status; Purpose; Core Educational Philosophy; Primary stance; What Layer 5 Is; What Layer 5 Is Not; Potential Future Curricula; Personalization Doctrine (Future); Relationship to AI (Post-AI Only)
- Requirement signals:
  - Do not implement Layer 5 education until **all** are true:

### A.100 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/local_archive_policy.md`
- Categories: map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 1554; SHA-12: `5f3f7178bbfa`
- Key headings: Local Archive Policy; Archive/Junk Drawer Candidates; Do Not Commit; Rule Of Thumb
- Requirement signals:
  - Do not commit disposable local/browser/system artifacts:
  - Do not commit artifacts just because they were generated while testing.

### A.101 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/memory_workflow.md`
- Categories: map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 6877; SHA-12: `0a90f034aa1f`
- Key headings: Memory Maintenance Workflow; Purpose; Sources; Mining Old Chats; Processing Extraction Docs; Consolidating Raw Archaeology (optional phase); Updating Durable Memory; Memory Types; Raw Extraction; Durable Memory
- Requirement signals:
  - Do not preserve every tactical debugging detail. Keep raw quotes only when wording matters or when they explain a decision that might otherwise be misunderstood.
  - - Future map library migration.
  - - Do not let every interesting sentence become durable memory.
  - - Do not mix current facts with future hopes.
  - - Do not mix rejected approaches with recommended architecture.

### A.102 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/mvp_beta_and_future_feature_roadmap.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 4767; SHA-12: `c904d8af5d1e`
- Key headings: MVP, Beta, And Future Feature Roadmap; Status; Maintenance Notes; Purpose; Core Principle; Stable foundations accelerate future development.; Development Phases; Stage 1 — Truth Foundation; Goal; Includes
- Requirement signals:
  - Future growth must preserve:

### A.103 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/ontology_plugin_and_symbolic_framework_architecture.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 3617; SHA-12: `f6bab89d14d7`
- Key headings: Ontology Plugin And Symbolic Framework Architecture; Status; Purpose; Core Principle; Symbolic systems may vary.; Examples Of Future Ontology Systems; Plugin Scope; Plugins Must Never; Plugin Architecture Goal; Default Ontology
- Requirement signals:
  - Future systems may allow professionals to:
  - Future implementation should preserve:

### A.104 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_continuity_workflow.md`
- Categories: workflow_screens, architecture_bridge
- Characters: 5184; SHA-12: `8a80bdfb8e6e`
- Key headings: Project Continuity Workflow; 1. Goals; 2. Memory lanes (what goes where); 3. Archaeology intake workflow; 4. Consolidation workflow (when to run); 5. Reviewer workflow; 6. Proposed updates workflow; 7. Raw archaeology vs durable truths; 8. How future chats should initialize; 9. How to continue safely after context loss
- Requirement signals:
  - - Never **delete** old contradictory raw text—pivots are historical evidence.

### A.105 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/project_memory_taxonomy.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 5641; SHA-12: `e630f6401456`
- Key headings: Project Memory Taxonomy; Architecture; UX Philosophy; Visual doctrine vs rendering experiments vs temporary UX; Implementation State; Future Features; Rejected Approaches; Validation Methodology; Edge Cases; Unresolved Questions
- Requirement signals:
  - - Avoid over-clever UI.
  - Rejected approaches should include the reason, not just the verdict.
  - - Should native selects remain or be replaced selectively?
  - - Future professional assistant mode.

### A.106 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_extended_context/relocation_strategy_framework.md`
- Categories: map_workspace, workflow_screens, architecture_bridge
- Characters: 2978; SHA-12: `5542c6b3c8b9`
- Key headings: Relocation Strategy Framework; Status; Purpose; Core Principle; Subtractive relocation comes before additive optimization.; Subtractive Relocation; Additive Relocation; Strong Relocations Often Do Both; Tradeoff Reality; Archetypes Are Contextual
- Requirement signals:
  - Future implementation should preserve:

### A.107 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ai_and_professional_workflow_strategy.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 4077; SHA-12: `093c412a15e4`
- Key headings: AI and Professional Workflow Strategy (From Archaeology); Institutional memory vs chat memory (anti–vibe-chaos); AI reviewer infrastructure (evolution); Non-negotiable product stance; AI collaboration failures as institutional risk; Second-opinion models; Practitioner assist vision (future); Consumer / intake AI (later); Strategic business hypotheses (treat as archaeology, not commitments); Tension to preserve

### A.108 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/current_sidebar_ux_audit.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, validation_design
- Characters: 4992; SHA-12: `c07666b5828f`
- Key headings: Current Sidebar / Map UX Audit; Implemented refinements (summary); 1. Wasted space (historical); 2. Unnecessary repetition; 3. Controls obscuring map usage; 4. Visual hierarchy; 5. Scrolling friction; 6. Mobile / tablet; 7. Readability; 8. Debug surfaces

### A.109 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/foundational_product_truths.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 4380; SHA-12: `9c5286269c09`
- Key headings: Foundational Product Truths (From Archaeology); Trust and truth; Overlap and decision-making; Precision vs cosmetics (non-negotiable vs acceptable); Separation of concerns (recurring architectural moral); Human + AI collaboration stance; Emotional tone and moat; Repetition as signal

### A.110 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/geocoder_and_city_strategy.md`
- Categories: visual_semantics, map_workspace, workflow_screens, validation_design
- Characters: 1799; SHA-12: `098e8b02e313`
- Key headings: Geocoder and City Strategy (From Archaeology); Why cities are core (not decoration); Readability and density; Search and disambiguation; Internationalization; Provider strategy tension (open); Dataset anecdotes (process lessons); UX details that affect trust

### A.111 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_memory_synthesis.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 16257; SHA-12: `04f378dc370d`
- Key headings: Institutional Memory Synthesis (Archaeology → Durable Docs); Chronology and authority; Project memory vs chat memory; 1. Core product identity; 2. Architecture themes; Canonical vs display geometry; Truth-grid vs contours; Centerline + aura separation; Independent brute-force validation exports; 3. Validation doctrine

### A.112 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/institutional_philosophical_synthesis.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 27007; SHA-12: `d9ca2489a35d`
- Key headings: Institutional Philosophical & Architectural Synthesis; 1. Core philosophy; 2. Symbolic / intellectual framework; 2.1 Symbolic realism (not mythic inflation); 2.2 Truth hierarchy (epistemology of surfaces); 2.3 Distinct metaphors (anti-conflation discipline); 2.4 Dynamic participation (between fatalism and naive will); 3. AI behavioral doctrine; 4. UX and pacing philosophy; 4.1 Emotionally non-interfering chrome
- Requirement signals:
  - - Avoid **good/bad placement** infantilism while still allowing **honest difficulty**: not every placement is “neutral”; moral judgment belongs in **lived ethics**, but **structural cost** is a legitimate teaching topic.

### A.113 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/map_workspace_behavior_audit_v1_2026-05-30.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 15325; SHA-12: `7567f30ce7ff`
- Key headings: Map Workspace Behavior Audit v1; Status; Purpose; Language and ID doctrine (applies to all sections); 1. Behavior already decided; Genie modes; Reasons to reopen Genie (decided intents); Search and render; Variable model; Legacy adapter (handoff to production map path)

### A.114 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/open_questions_and_unresolved_areas.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 3871; SHA-12: `c86a26458dc6`
- Key headings: Open Questions and Unresolved Areas (From Archaeology); Geometry and calculation semantics; Rendering architecture; Validation systems; UX systems; Data + search; Product scope and ethics; Renderer beta stabilization questions (Chat 08); Operational workflow; Weak archaeology coverage (second pass, 2026-05)

### A.115 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/product_brief.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 3080; SHA-12: `ba708a2f1745`
- Key headings: Product Brief; Product; Current Core Capabilities; Product Philosophy; Overlay Truth Standard; Current Architecture Direction; Validation Corpus; Institutional memory (archaeology)
- Requirement signals:
  - - Avoid "too clever" UI that creates artificial stupidity.
  - - Avoid map-library migration until there is evidence the remaining issues are Leaflet-specific.

### A.116 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/rejected_or_obsolete_approaches.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge
- Characters: 2949; SHA-12: `9bccda948bdc`
- Key headings: Rejected or Obsolete Approaches (From Archaeology); Geometry / seam handling; Rendering / signal processing mistakes; Aspect / line extraction misconceptions (historic debugging); Incorrect astronomical short-cuts (explicit catastrophic failures); UX / workflow paths; Institutional / AI process paths; Overlap representation (product iteration); Possibly obsolete but historically explanatory; Not “rejected,” but **dangerous if misunderstood**

### A.117 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/relocation_app_product_roadmap.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 27057; SHA-12: `24ab9bae5cb8`
- Key headings: Relocation App Product Roadmap; 1. Current Stable Milestone; 2. Product Philosophy; 3. Core Search Types; 4. Overlay/Color System Roadmap; 5. Aspect Aura Roadmap; 6. UX/Layout Roadmap; 7. City Search / Geocoder Roadmap; 8. Birth Data / Accounts / Professional Mode Roadmap; Saved Object Taxonomy
- Requirement signals:
  - - Avoid self-indulgent bells and whistles.
  - - Avoid "too clever" UI that creates artificial stupidity.
  - Future search types:
  - - Avoid naive alpha stacking when it makes purple or dark colors dominate.
  - - Should not light up the whole inverse region.

### A.118 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/travel_and_future_modes.md`
- Categories: visual_semantics, map_workspace, workflow_screens, architecture_bridge, validation_design
- Characters: 1279; SHA-12: `c351ba13dcef`
- Key headings: Travel and Future Modes (From Archaeology); Road-trip / GPS mode; Offline / airplane scenarios; Transit overlays and relocated houses (debated); Positioning consequence; Dependencies called out

### A.119 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/ux_and_design_language.md`
- Categories: visual_semantics, map_workspace, workflow_screens, language_payload, architecture_bridge, validation_design
- Characters: 3849; SHA-12: `ac5f86eb3a13`
- Key headings: UX and Design Language (From Archaeology); Map-first and spatial reading; Trust UX vs explanation UX; Typography and popups (professional validation patterns); Interaction pitfalls called out repeatedly; Emotional tone; Product positioning language (from archaeology); Tensions to preserve (not resolve here); Chat 08 update: style presets and mobile layer control
- Requirement signals:
  - Future visual style presets may be desirable, but they must remain downstream from truth geometry. Candidate families include:

### A.120 `/Users/davegoodman/Desktop/relocation-backend-docs-backup/onboarding/03_historical_context/web2_account_chart_workflow_architecture_review_v1_2026-05-29.md`
- Categories: map_workspace, workflow_screens, language_payload, architecture_bridge
- Characters: 20953; SHA-12: `db53e1e91227`
- Key headings: Web 2.0 Account / Chart Workflow Architecture — Review Proposal; Status; Executive summary; 1. Proposed navigation hierarchy; A. Navigation tree; Navigation principles; Recommended route IDs (conceptual); 2. User journey diagrams; B. Map entry paths (exact); C. Leaving map and returning



---

## Appendix B — Audit Statement

Programmatic pass selected 186 UI/UX/design/interface-related source blocks from 196 total archive blocks. The audit JSON stores selected file names, hashes, headings, requirement signals, category counts, and source matching metadata. Final generated word count before this statement: 12666 words.
