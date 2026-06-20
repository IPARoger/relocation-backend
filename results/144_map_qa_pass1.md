# MAP-QA-1 — First QA Pass

**Date:** 2026-06-20  
**Scope:** Explore mode · Ghost strip · Notebook placement · Onboarding spotlight targets · Animation rough edges  
**Type:** Audit only — no implementation, no commits  
**Baseline:** post MAP-UX-4 (`map_CURRENT.html`)

---

## 1. Explore Mode

### Friction

**F-1 — Left-rail controls persist in explore with no explore treatment.**  
`#rm-map-controls` (Back/Forward/Pin, top:90px left:12px) and `#rm-save-pill` (top:136px left:12px) are `position:absolute` in `#map` and have no `body.rm-explore` CSS rule. They stay visible in explore mode. No design decision documented for whether they should fade, dim, or stay — leaving an ambiguous state.

**F-2 — Nameplate has no explore-mode ghost treatment.**  
MAP-UX-2.6 added the nameplate with `position:fixed`. The sandbox applied `body.explore .identity-stamp` rules (transparent background, white halo text, meta lines collapse). None of that is present in production. In explore mode the nameplate looks identical to setup mode — it doesn't recede into the map.

**F-3 — No explicit "return to Genie" affordance label.**  
The bottle button title is `"Reopen variable builder"` (tooltip only). No visible label. A first-time user does not know the sliders icon means "go back". The breathe pulse draws attention but doesn't communicate intent.

**F-4 — Panel collapse with overflow content may crush visually.**  
`#panel { width: 0 !important; overflow: hidden }` without `white-space: nowrap` on panel children. Text in the panel will reflow and wrap as width shrinks — this reflow happens mid-animation and may look messy rather than a clean slide-off.

### Hierarchy Issues

**H-1 — Ghost strip and bottle compete for the same right-rail column.**  
Bottle: `right:18px; top:62px`. Ghost strip: `right:18px; top:46%`. When the strip has 2-4 tokens they don't overlap (strip center is ~414px from top, bottle is at 62px). But with a single long token, the strip's top edge could reach ~380px — still clear. Not a current collision, but zero margin documented.

**H-2 — Empty ghost strip shows "No variables active" text.**  
If a user clicks Search Map without setting any condition, the ghost strip container appears in explore mode with the empty-state copy. This exposes the strip container without content, which is visually weak and structurally misleading — explore mode implies active conditions exist.

---

## 2. Ghost Strip

### Friction

**F-5 — Token label uses abbreviation only (`Ma · 7`), not full label.**  
The `mini` field (abbreviated planet + house number) is what renders in the ghost strip. `Ma · 7` is legible for power users, not learners. The `label` field (`Mars – 7th House`) is computed but only used in the `title` attribute. On the strip itself, a first-time user sees `Ma · 7` with no explanation.

**F-6 — No tooltip or expansion for label.**  
The `title` attribute on the container row is not set; only the swatch and label span are present. A hover tooltip on the full row showing the expanded label would bridge the abbreviation gap without consuming space.

**F-7 — Mute/Solo/Not buttons have no persistent legend.**  
The strip shows three 30px unlabeled squares: `[✕] [M] [S]`. The instructions `title` attributes say `NOT — redact`, `Mute`, `Solo`. A first-time user encountering these three buttons after a search has no legend unless they hover each.

**F-8 — Mute/Solo/Not are visual-only (documented).**  
Toggling any button does not affect the map overlays (no `rmGenieAdapter.redrawWithFilters` integration yet). This is correctly documented as a future hook but is a significant gap: the controls appear to work (CSS class toggles, `aria-pressed` updates) but the map doesn't change. If a real user clicks "Mute", they will expect the overlay to disappear.

### Motion Issues

**M-1 — All ghost tokens fade in simultaneously (no stagger).**  
Each `.rm-gtok` has `animation: rmGhostIn .6s ease both` with no `animation-delay`. The sandbox staggered tokens with incremental delays so they cascade-slide in. Without stagger, 3-4 tokens appear as a single flash, losing the "materializing from right" cascade effect.

**M-2 — Container animation overlaps token animations.**  
The ghost strip container animates with `rmGhostStripIn` (1.15s, .35s delay, blur+translate). Individual tokens animate with `rmGhostIn` (.6s, no delay). The token animation begins when the container is still blurring in — the result is animated content inside a blurring container, which can read as visual noise.

**M-3 — Ghost strip right:18px inside `#map` (flex:1) shifts during panel collapse.**  
As the panel width transitions from 300px to 0, `#map` grows 300px rightward. The ghost strip is `right:18px` within `#map`, so its viewport position shifts 300px to the right during the collapse animation. The strip animates in via `rmGhostStripIn` simultaneously with the map expanding, so the strip appears to slide from two directions at once: inward via `translateX(10px)` and rightward via `#map` width change. The final resting position is correct (right:18px from viewport right edge) but the path is noisy.

**M-4 — Panel collapse doesn't coordinate with ghost strip entrance.**  
The two animations run independently: panel width begins collapsing at 0ms; ghost strip entrance begins at 350ms delay. There is no choreography — the map grows, then the strip appears. The sandbox had a unified `body.explore` state machine where all transitions were authored together. The production version has two separate CSS authors (panel is `#panel { transition }`, strip is `@keyframes`).

---

## 3. Notebook / Map Notes

### Placement Issue

**N-1 — Notes textarea buried in collapsing panel.**  
`#saveInvestigationNote` exists as a `<textarea>` inside `#panel`. In explore mode, the panel collapses to width:0. Notes become completely inaccessible during the primary map exploration state. This means users can't write a note about what they're seeing while looking at the map — they must reopen the panel via the bottle, killing explore mode.

**N-2 — No overlay placement for notes in explore mode.**  
The onboarding step 8 references `[data-role="map-notes"]` which doesn't exist as a DOM element anywhere. This implies a future floating notes pad on the map canvas — but it's not built. Currently notes exist only as a textarea form field styled as a plain production UI input (`style="width:100%;box-sizing:border-box"`), not as a polished overlay.

**N-3 — Notes textarea has no visual hierarchy.**  
It sits between the `Find regions` button and the `Save Investigation` button with no section heading. It's the least discoverable element in the panel.

---

## 4. Onboarding Issues

**O-1 — Step 4 selector is broken (`data-role="ghost-tools"`).**  
The walkthrough framework defines step 4 as:
```js
selector: '[data-role="ghost-tools"]'
```
The actual ghost strip element has `data-role="map-ghost-strip"`. No element in production has `data-role="ghost-tools"`. Because this step is not marked `optional: true`, the framework will silently skip it (per `resolveTarget` → `showStep(idx+1)`). Step 4 will never spotlight the ghost strip.

**O-2 — Step 4 targets the wrong granularity.**  
Even if the selector were correct, spotlighting the full ghost strip container does not teach Mute/Solo/Not individually. The individual buttons (`.rm-notb`, `.rm-mb`, `.rm-sb`) are the teachable moments. The spotlight should sequence through them or at least land on a single token row, not the entire strip.

**O-3 — Step 4 requires explore mode to be active.**  
The ghost strip is `display:none` in setup mode. If the walkthrough reaches step 4 before a search has been executed, the target element is invisible and won't spot correctly even if the selector matched. The framework needs to either: (a) call `window.__rmGhostStrip.enterExplore()` before step 4, or (b) detect and skip step 4 if not in explore mode.

**O-4 — Steps 5-7 (Pin, History, Save) are all in setup-mode left-rail.**  
These selectors work correctly — `[data-role="map-pin"]`, `[data-role="history-controls"]`, `[data-role="map-save-search"]` all exist and are always visible. No issue here, documented for completeness.

**O-5 — Step 8 (Map Notes) is optional but selector is absent.**  
`[data-role="map-notes"]` does not exist in production. The step is `optional: true` so it skips gracefully. Low friction but the "Step 8 of 8" label suggests 8 steps and users get 7 — label should be `7 of 7` if step 8 is truly optional and absent.

---

## 5. Summary — Priority Order

| # | Issue | Category | Severity |
|---|-------|----------|----------|
| O-1 | Step 4 selector wrong (`ghost-tools` vs `map-ghost-strip`) | Onboarding | **High** — step 4 is silently skipped |
| O-3 | Step 4 requires explore mode; framework doesn't ensure it | Onboarding | **High** — step never lands on visible target |
| F-8 | Mute/Solo/Not visual-only, map doesn't respond | Ghost strip | **High** — creates false affordance |
| M-3 | Ghost strip shifts 300px during panel collapse | Motion | Medium — noticeable during animation |
| M-1 | Tokens all fade in simultaneously (no stagger) | Motion | Medium — loses cascade effect |
| F-2 | Nameplate has no explore-mode ghost treatment | Explore mode | Medium — nameplate looks heavy over map |
| M-2 | Container blur overlaps token fade | Motion | Medium — visual noise |
| N-1 | Notes inaccessible in explore mode | Notebook | Medium — primary use case blocked |
| F-4 | Panel text reflows during width collapse | Explore mode | Medium — janky visual |
| F-1 | Left-rail controls have no explore treatment | Explore mode | Low — ambiguous but functional |
| F-7 | No legend for M/S/Not buttons | Ghost strip | Low — tooltip exists |
| F-5 | Token labels abbreviated without expansion | Ghost strip | Low — power-user legible |
| H-2 | Empty ghost strip shows "No variables" in explore | Ghost strip | Low — edge case |
| M-4 | Panel collapse and strip entrance uncoordinated | Motion | Low — feels accidental |
| F-3 | Bottle has no visible label | Explore mode | Low — breathe pulse helps |
| O-5 | Step count says "8 of 8" when step 8 skips | Onboarding | Low — cosmetic |
| N-2 | Notes overlay doesn't exist on map canvas | Notebook | Low — known deferred |

---

## Deferred / Out of Scope

- Overlay redraw with Mute/Solo/Not (needs `rmGenieAdapter.redrawWithFilters`) — documented in code
- Save disk morph animation — not yet implemented
- Nameplate explore ghost (MAP-UX-5 candidate)
- Centered city search overlay — panel search still primary

---

## 6. Animation Doctrine Audit

**Doctrine baseline:**  
Animations exist to teach object permanence. Controls should transform into their future state rather than disappear and reappear. Users must be able to mentally track an object throughout its transformation. The preferred motion language is metamorphosis, not substitution. Animations occur at human-observable speed.

**Evaluation criteria applied to every explore-mode transition:**

1. **Object permanence** — can the user track the control continuously from setup state to explore state?
2. **Teaching value** — does the animation convey where the tool went and how to retrieve it?
3. **Morph vs substitution** — does one visual state transform into the next, or does one disappear while another appears separately?
4. **Human-scale timing** — is the transition slow enough for a human to observe and comprehend?
5. **Visual hierarchy after** — does the resulting explore-mode layout correctly subordinate secondary controls and elevate the map?

---

### ADT-1 — Topbar / Main Navigation → Hamburger

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Partial | The nav clips upward (translateY + clip-path inset) toward the hamburger zone, implying directional travel. However the clip collapses symmetrically from all sides, not specifically toward the hamburger button. The connection is implied, not shown. |
| Teaching value | Partial | A careful observer can infer "the nav is inside the hamburger" from the upward movement. The hamburger appears where the nav was. A casual observer will not make this connection without the motion. |
| Morph vs substitution | Substitution | The nav collapses and disappears. The hamburger then scales in separately. They are never simultaneously opaque. No visual thread connects them. |
| Human-scale timing | Acceptable | 0.9–1.0s. Fast enough to lose the narrative for first-time users. The clip-path collapse is subtle — a slow blink misses it. |
| Visual hierarchy after | Good | Hamburger is centered (correct), clearly visible. Other nav links are gone. The map is unobstructed at the top. |

**Doctrine verdict:** Fails morph requirement. The hamburger appears as new rather than as the resolved destination of the nav's journey. The clip-path direction does not clearly point at the hamburger target.

---

### ADT-2 — Hamburger Button Entrance

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Weak | Scales in from 55% size (keyframe `menuHandleIn`). This is a generic "appear" — not connected to the nav that just collapsed. A user watching sees: nav compresses and vanishes → hamburger grows into view. These are two separate events. |
| Teaching value | Low | Scale-in does not communicate "the nav items are inside here." It communicates "a new button appeared." The spatial relationship to the collapsed nav is lost. |
| Morph vs substitution | Substitution | New element appearing, not a transformation of the old element. |
| Human-scale timing | Acceptable | 0.9s entrance. The pacing is fine, but the meaning is absent. |
| Visual hierarchy after | Good | Hamburger is the leftmost visible control. Its singular presence communicates that the hidden menu lives here. |

**Doctrine verdict:** Substitution, not morph. The arrival animation teaches nothing about the departed nav. A user who blinked during the nav collapse will not know the hamburger is related.

---

### ADT-3 — Share Button (Pill → Circle Glyph)

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Good | The share button stays at its position in the topright. Width and padding transition, text label collapses (max-width 0), icon remains visible and scales up. The user can watch a pill become a circle. |
| Teaching value | Good | The transition teaches: "share is still here, now compact." The label disappearing while the icon stays is pedagogically correct — the icon is the residue of the function. |
| Morph vs substitution | Morph | Single DOM element. CSS transitions change width (2.2s), padding (2.2s), text max-width (2.0s), SVG size (2.0s). No element is removed or added. |
| Human-scale timing | Good | 2.0–2.2s. Slow enough for a user to watch the text label collapse and the circle emerge. The gradual nature is legible. |
| Visual hierarchy after | Good | The compact circle is clearly distinguished (accent color, border). Correctly smaller than in setup mode. Does not compete with the map. |

**Doctrine verdict:** Passes all criteria. This is the reference implementation of the doctrine for this project — one object, continuously visible, physically changing shape at observable speed.

---

### ADT-4 — Nav Buttons (Back / Forward / Pin) → Icon-Only

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Good | Buttons remain at their position. Width narrows (2.4s), text label fades out (0.8s), icon persists throughout. The user can watch "Back" text fade while the chevron icon stays, then the box contracts around it. |
| Teaching value | Good | The label's disappearance while the icon remains teaches: "the function didn't leave, only the label did." The icon is the teaching residue — it communicates what the button does without text. |
| Morph vs substitution | Morph | Same elements, continuous visual presence. Box width and text opacity are CSS transitions, not show/hide. |
| Human-scale timing | Good | Box: 2.4s cubic-bezier. Text fade-in on return waits 1.8s for box to expand first. Labels no longer outrun the container. |
| Visual hierarchy after | Good | Icon-only buttons are clearly smaller and recede relative to the map. They remain operable but subordinate. |

**Doctrine verdict:** Passes. Strongest secondary example of the doctrine in this interface. The icon's continuous visibility provides the user a visual anchor during the text's departure.

---

### ADT-5 — Genie Builder Panel → Bottle

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Incomplete | The builder scales to 6% from its top-right corner (the bottle's approximate position) over 1.8s. However, opacity fades to 0 with a 1.2s delay — meaning the builder becomes invisible before its scale journey completes. The user sees the builder shrink, then disappear, then the bottle appear. There is a gap between disappearance and bottle arrival where neither is opaque. |
| Teaching value | Weak | A user who watches carefully can observe the directional travel (toward the bottle position). But because the builder fades before it reaches the bottle, the visual chain is broken. The bottle then scales in separately. The user cannot conclude: "the builder became the bottle." |
| Morph vs substitution | Near-morph, effectively substitution | The directional scale toward the bottle is correct metamorphosis intent. But the opacity fade before arrival converts it to substitution in practice. The two elements (builder fading, bottle appearing) never occupy the same visual space simultaneously in their opaque states. |
| Human-scale timing | Acceptable | 1.8s scale — human-observable. But the 1.2s opacity delay means the visible phase is truncated. The user has ~1.2s to observe the scaling before the builder fades. |
| Visual hierarchy after | Good | Bottle is the sole right-rail element in explore mode. Clearly prominent. Breathe pulse draws attention appropriately. |

**Doctrine verdict:** Intent is correct — transform-origin aligned with bottle position is the right approach. Fails because opacity zeroes out before the journey completes, converting metamorphosis to substitution. The builder must remain visible until it reaches the bottle's position, then the bottle can replace it.

---

### ADT-6 — Bottle Button Entrance

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Incomplete | Scales from 40% (`bottleIn` keyframe). Does not connect to the builder it represents. Appears as a new element, not as the resolved destination of the builder's compression. |
| Teaching value | Low | The user sees a new square appear. Without ADT-5 completing its journey visibly, there is nothing to connect this arrival to the builder's departure. The breathe pulse communicates importance, not origin. |
| Morph vs substitution | Substitution | New element appearing independently. |
| Human-scale timing | Acceptable | 1.0s. |
| Visual hierarchy after | Good | Sole right-rail control. Clear. |

**Doctrine verdict:** Fails morph requirement. The bottle entrance animation must read as the completion of the builder's compression, not as a new element's appearance. This requires ADT-5 to resolve before or as the bottle becomes opaque.

---

### ADT-7 — Save Search Pill → Disk (flySave)

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Strong | A ghost clone of the pill travels from its builder position to the disk's fixed position over 1600ms. The ghost carries both pill content and disk SVG, cross-fading between them during flight. The user watches a single object travel and transform simultaneously. |
| Teaching value | High | The animation teaches three facts: (a) the save button did not disappear, (b) it moved to a fixed map position, (c) it changed shape to a disk/save glyph. All three lessons are delivered by the same motion without commentary. |
| Morph vs substitution | Morph | Single ghost DOM element transforms shape, content, and position simultaneously. Cross-fade eliminates the moment of substitution. The pill-shaped ghost becomes disk-shaped through continuous visual transition. |
| Human-scale timing | Good | 1600ms. The flight is slow enough to observe the shape-change mid-journey. |
| Visual hierarchy after | Good | Disk appears bottom-right, independent of the builder rail. Its position communicates permanence — it's a map-canvas element now, not a panel element. |

**Doctrine verdict:** Passes all criteria. Currently the most complete implementation of the doctrine in the project. The cross-fade morph during flight is the correct pattern for all state transitions in this interface.

---

### ADT-8 — Nameplate Identity Stamp → Watermark

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Good | The nameplate stays at its fixed position throughout. It does not move or hide. Its visual weight reduces: fill goes transparent, outline stroke appears, meta lines fade, primary text dims to ~20% opacity. The user can watch the same element becoming a watermark. |
| Teaching value | Partial | The transition correctly communicates: "the identity information is still here, receding behind the map." What it does not teach is what would restore it. There is no reverse affordance visible in explore mode — the watermark does not hint at clickability to return to setup mode. |
| Morph vs substitution | Morph | Same element, continuous presence, CSS property transitions: text-fill-color (3.5s), text-stroke (3.5s), opacity (2.8–3.0s), max-height of meta lines (3.8s). |
| Human-scale timing | Good | 3.5s primary, 2.8s meta — the slowest transitions in the interface. Correct: the nameplate should feel like the last thing to change, not the first. |
| Visual hierarchy after | Good | Watermark is visually lowest priority. Map content is fully readable through it. The outline-only treatment is sufficiently recessive. |

**Doctrine verdict:** Passes morph and timing criteria. Teaching value is partial because the watermark provides no affordance to return to setup mode. The user learns the nameplate receded; they do not learn how to bring it back.

---

### ADT-9 — Ghost Strip Materialization

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Not applicable | The ghost strip is a new element appearing in explore mode — it has no setup-mode counterpart. It represents information previously housed inside the builder panel, now extracted and displayed on the map canvas. |
| Teaching value | Partial | The strip materializes from the right (same side as the builder). This spatial relationship implies "this came from the builder." However, there is no visual continuity between the builder's chips and the ghost tokens — they are styled differently and the connection is conceptual, not visual. |
| Morph vs substitution | Appearance, not morph | A new element entering the canvas is inherently not a transformation. The slide-in from right is the best available motion for a genuinely new element. |
| Human-scale timing | Partial | Container: 1.15s (now 1.4s with delay). Tokens: 0.6s with no stagger — all tokens appear simultaneously, which is faster than human reading pace for 3-4 items. Token stagger would be more legible. |
| Visual hierarchy after | Acceptable | Strip sits at mid-right. Does not overlap bottle (top-right) or disk (bottom-right) under normal conditions. Three distinct right-rail elements (bottle, strip, disk) require clear vertical separation which is present but undocumented. |

**Doctrine verdict:** New element, not a transformed one — the doctrine's morph standard does not directly apply. The weakest element is token stagger: simultaneous appearance of 3–4 tokens reads as a flash, not as a materialization sequence. Strip-to-chips visual continuity (color, shape, abbreviation) needs strengthening so the user understands this represents their builder conditions.

---

### ADT-10 — City Search Bar (Persistent Through Transition)

| Criterion | Rating | Finding |
|-----------|--------|---------|
| Object permanence | Strong | The search bar does not change state during the explore transition. It was visible in setup mode and remains visible and interactive in explore mode. |
| Teaching value | N/A | No transformation occurs. The bar's persistent presence correctly communicates that search is always available. |
| Morph vs substitution | N/A | |
| Human-scale timing | N/A | |
| Visual hierarchy after | Good | With the builder gone, the search bar gains relative prominence. It is now the primary interactive element on the map canvas, which is correct. |

**Doctrine verdict:** Passes by design. Persistence is the correct behavior here — no teaching needed for an element that never leaves.

---

### Doctrine Audit Summary

| Transition | Object Permanence | Teaching Value | Morph vs Sub | Timing | Hierarchy | Verdict |
|------------|:-----------------:|:--------------:|:------------:|:------:|:---------:|---------|
| ADT-1 Topbar → hamburger | Partial | Partial | **Substitution** | Acceptable | Good | Fails |
| ADT-2 Hamburger entrance | Weak | Low | **Substitution** | Acceptable | Good | Fails |
| ADT-3 Share pill → glyph | Good | Good | **Morph** | Good | Good | **Passes** |
| ADT-4 Nav buttons → icon | Good | Good | **Morph** | Good | Good | **Passes** |
| ADT-5 Builder → bottle | Incomplete | Weak | Near-morph→sub | Acceptable | Good | Fails |
| ADT-6 Bottle entrance | Incomplete | Low | **Substitution** | Acceptable | Good | Fails |
| ADT-7 Save pill → disk | Strong | High | **Morph** | Good | Good | **Passes** |
| ADT-8 Nameplate → watermark | Good | Partial | **Morph** | Good | Good | **Passes** |
| ADT-9 Ghost strip entry | N/A | Partial | N/A (new) | Partial | Acceptable | Partial |
| ADT-10 Search bar (persists) | Strong | N/A | N/A | N/A | Good | **Passes** |

---

### Critical Gap — The Builder/Bottle Chain

The single largest doctrine failure is the **ADT-5 → ADT-6 pair**: the builder fades to invisible before reaching the bottle position, then the bottle appears as a new element. This breaks the most important metamorphosis in the interface — the moment where the user's primary tool compresses into its resting state.

The doctrine-correct sequence would be:

1. Builder scales down toward bottle position, **remaining opaque throughout the compression**
2. Builder reaches the bottle's bounding box at near-zero scale
3. At that moment — and only at that moment — the bottle becomes visible, inheriting the builder's position and expanding to its full size (not shrinking in from 40%, but revealed in place)
4. The user perceives a single object that compressed and then resolved

Until this chain is unbroken, the builder and bottle read as two separate elements on alternating schedules, not as one object in two states.

