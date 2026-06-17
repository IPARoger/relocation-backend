# Surface Treatment Doctrine

Status: provisional doctrine (Phase 2.8, post-Hierrarchy / post-QA)
Type: doctrine extraction — assigns *treatment roles* to surfaces
Scope: depth, elevation, separation, grouping, texture, and atmosphere applied
to bounded visual regions ("surfaces").

This is a decision document, not a raw audit. It tells future implementation
**which surfaces get which kind of treatment, and why** — derived from the
Visual Language Inventory (2.8G) and bound by the Visual Hierarchy Doctrine
(2.8H). It does **not** select final colors, fonts, shadow/glow values,
spacing values, or animation timing. Those remain deferred.

Builds on and must honor: Plate Doctrine, Badge & Metadata Doctrine, Control &
Action Doctrine, Table & Information Density Doctrine, Visual Language Inventory,
Visual Hierarchy Doctrine, and the 2.8 QA Review.

Product goal: **quiet vitality** — warmth, depth, and atmosphere that support
decision-making. Treatment is functional infrastructure, not decoration.

---

## 1. Definition

A **surface** is any bounded visual region the user reads as a single thing:
the page itself, the wheel, a card, a table, a plate, a popup, a modal, a notes
panel, a scaffold box.

A **treatment** is the set of visual mechanisms that give a surface depth,
edges, grouping, texture, or atmosphere: elevation/shadow, glow, borders,
separators, row shading, gradients/texture, and spacing.

Core principle: **treatment is assigned by the surface's role in the attention
and authority hierarchy — not by aesthetic preference per page.** A surface's
treatment must encode "how much should this draw the eye" consistently across
the product.

---

## 2. Surface Tier Model

Six treatment tiers, ordered by intended visual presence. Higher tiers may carry
more atmosphere/depth; lower tiers must stay quieter.

1. **Focal object — the Wheel.** The single most-treated surface on chart pages
   (atmosphere, glow, texture, depth, internal ring hierarchy). Nothing else may
   out-treat it on a chart-bearing page.
2. **Atmospheric page ground.** The page background itself (warm gradients/paper,
   optional subtle noise). Provides life *behind* content without competing with
   it.
3. **Grouped working surfaces.** Chart reference cards, metadata/system blocks,
   city-intelligence cards — bounded groups that hold dense content. Soft
   depth/outline; clearly grouped but subordinate to the wheel.
4. **Structural surfaces.** Comparison matrices, fact tables, accordion rows,
   cost/weather tables — primarily line/shading/structure, minimal atmosphere.
5. **Transient/overlay surfaces.** Modals, map popups, drawers — focus depth and
   backdrop separation while active; not persistent atmosphere.
6. **Scaffold/quarantine surfaces.** App-shell boxes, dashed stubs, future-only
   and debug blocks — deliberately utilitarian; never promoted to product
   treatment.

Invariant: a surface's tier is stable across pages. A reference card is Tier 3
everywhere; a comparison matrix is Tier 4 everywhere.

---

## 3. Treatment-by-Tier Rules

What each tier may and may not use (mechanism roles only; no final values).

| Tier | May use | Should avoid |
|---|---|---|
| 1 Focal (Wheel) | outer glow, inner/inset boundary, radial atmosphere, paper texture, ring hierarchy, popout affordance | flat utilitarian borders; competing card chrome around it |
| 2 Page ground | warm gradients/paper, subtle noise | hard borders; strong shadows; anything that reads as a "card" |
| 3 Grouped working | soft elevation/depth, card outline, gentle top gradient, row shading, label/value alignment | glow that rivals the wheel; heavy decoration |
| 4 Structural | borders, row/column separators, alternating rows, block headers, label columns | elevation that lifts it above grouped cards; atmospheric glow |
| 5 Transient/overlay | focus depth, backdrop separation, compact containment | persistent page-level atmosphere; permanent presence |
| 6 Scaffold | flat boxes, dashed boundaries, warning/notice/debug styling | any treatment implying production canon |

Rule of thumb: **atmosphere decreases as you descend the tiers; structure
increases.** Tier 1–2 carry warmth; Tier 4–6 carry structure.

---

## 4. Depth & Elevation Rules

- **The wheel carries the most depth/atmosphere** on any chart-bearing page.
- **Grouped working surfaces (cards) carry soft depth** — enough to read as a
  grouped object, never enough to rival the wheel.
- **Structural surfaces (comparison matrices, fact/accordion tables) stay
  near-flat** — depth comes from lines and structure, not elevation.
- **Overlays earn depth only while active** (modal/popup focus), then release it.
- **Metadata and plates must not out-elevate the wheel.** A plate orients with
  type and position, not with elevation that competes for the focal role.
- Elevation must **track the attention hierarchy**: heavier visual weight is only
  permitted where the Hierarchy Doctrine assigns higher attention.

Observed today and accepted as direction: chart reference cards (`.tcard`) carry
gentle depth; comparison matrices are flat. This **difference is intentional**
(grouped working surface vs structural surface) and should be preserved, not
homogenized.

---

## 5. Separator Strength Assignment

The inventory found a four-step separator scale (strong / medium / subtle /
nearly-invisible). This doctrine binds each step to a role:

- **Strong** — separates *modes or tasks*: modal/overlay backdrops, the
  chart-vs-saved-lists boundary, major city-intelligence section tops, the
  sticky comparison city-bar boundary.
- **Medium** — separates *regions within a working surface*: wheel-vs-reference
  divider, card outlines, block headers, system/metadata block edges, popup
  header line.
- **Subtle** — aids *readability inside dense data*: alternating rows, list-row
  separators, intra-card field lines, notes-toolbar edge.
- **Nearly invisible** — *implied grouping only*: spacing between text groups in
  plates, low-opacity wheel texture, fine wheel wedge fills.

Rule: **use the weakest separator that still does the job.** Do not escalate to a
border where spacing groups adequately; do not escalate to a backdrop where a
line groups adequately. Stronger separators are reserved for stronger boundaries.

---

## 6. Texture & Atmosphere Rules

- **Texture is reserved for Tier 1–2** (the wheel and the page ground) and, very
  gently, for grouped chart cards. It is what makes Profile/Relocated feel alive.
- **Structural and scaffold surfaces stay flat.** Comparison matrices, city
  detail tables, and app-shell boxes derive life from content and structure, not
  texture.
- **Atmosphere must never reduce legibility of dense data.** Where atmosphere and
  density meet (e.g. a card holding a table), structure wins inside, atmosphere
  stays at the boundary.
- Quiet-vitality test for any added texture/atmosphere: *does it increase
  confidence and orientation, or is it decorative?* If decorative, omit it.

---

## 7. Glow Rules

- **Glow is a hierarchy and warmth signal, not decoration.** Its primary home is
  the wheel.
- **Glow is reserved for the focal object and home/guest distinction.** Cards,
  tables, plates, metadata, and badges do not get focal glow; they may have soft
  depth at most.
- **No surface may carry glow that competes with the wheel** on a chart-bearing
  page.
- The **map aura/raster field is a separate system** from chart-wheel glow; this
  doctrine does not merge them, and map data-atmosphere must not be read as a
  chart wheel.

---

## 8. Grouping Rules (border vs shading vs spacing)

Choose the grouping mechanism by density, lightest-first:

1. **Spacing** — default for low-density text/identity groups (plate fields).
2. **Alternating row shading** — for dense scannable rows (chart/comparison
   tables).
3. **Borders / outlines** — for bounded working groups (cards, metadata blocks,
   sticky columns).
4. **Backdrop / containment** — for transient tasks only (modals, popups).

Rule: **escalate only when the lighter mechanism fails.** Heavy bordering of
something that spacing already groups creates visual noise and false hierarchy.

---

## 9. Home / Guest Allele Treatment

- The **home vs guest distinction is a treatment variant of the same organism,
  not a different surface.** Same structure, same mechanics; only the
  atmospheric role (warmer/home vs cooler/lighter/guest) differs.
- Guest/relocated surfaces read as **junior context**: slightly lighter depth,
  cooler/lighter atmosphere, modestly reduced wheel scale — never a second design
  language.
- Final color/value of the home/guest distinction is **deferred**; this doctrine
  only fixes that the distinction is *atmospheric-role*, applied consistently to
  wheel and chart cards, and subordinate to wheel centrality.

---

## 10. Surface-Treatment Invariants

Binding regardless of later color/value choices:

- **Wheel centrality:** the wheel is the most-treated surface on chart pages;
  nothing out-treats it there.
- **Treatment tracks hierarchy:** visual weight is granted only where the
  Hierarchy Doctrine grants attention.
- **Metadata/plates never out-elevate the wheel.**
- **Notes surfaces are Tier 3 at most** and never carry focal treatment; notes
  remain a supporting layer (per Plate + Hierarchy doctrines).
- **Scaffold stays quarantined:** app-shell/debug/future treatments never leak
  into product canon.
- **Tier stability:** a given organism keeps its tier across all pages.
- **Lightest-effective rule:** weakest separator/grouping that works; least
  atmosphere that achieves quiet vitality.

---

## 11. Explicit Non-Goals

This doctrine does **not** decide:

- final colors or color roles' values
- final fonts or type scale
- final shadow, glow, or elevation values
- final spacing values
- final animation/timing/hover behavior
- final home/guest color language

Those belong to later phases and must not be inferred from this document.

---

## 12. Open Questions (carried forward)

From the Visual Language Inventory and Hierarchy QA; not resolved here.

- **Glow vs shadow:** when hierarchy should come from atmospheric glow vs plain
  elevation (beyond "wheel = glow").
- **Texture vs flat:** which Tier 3 surfaces (city intelligence, relocated
  panels) need texture to avoid sterility.
- **Border vs spacing thresholds:** density level at which grouping must escalate.
- **Dense vs airy:** how much air dense working tables can take without
  under-informing.
- **Atmosphere vs distraction:** the ceiling on wheel/card/page atmosphere.
- **Chart-card vs comparison-matrix divergence:** confirmed intentional here, but
  the exact treatment gap is unspecified.
- **Map warmth:** how much product atmosphere enters map controls/popups vs
  staying utilitarian.
- **Modal convergence:** whether chart/comparison/city/scaffold modals share one
  focus-treatment language.
- **Selected/active/disabled state treatment:** no cross-surface language yet.
- **Scaffold/future styling:** keep quarantined or define a real future-state
  treatment.
- **Aura vs chart glow relationship:** still unresolved.

---

## 13. Highest-Value Treatment Targets (sequence)

Order in which surface treatments should be standardized, all honoring Section 10.

1. **Wheel treatment system** (Tier 1) — glow, texture, inset, ring hierarchy,
   home/guest/relocated/modal variants, popout affordance.
2. **Chart reference card system** (Tier 3) — soft depth, outline, heading
   separator, row shading for PiH/AiS/A2A.
3. **Separator strength scale** — bind strong/medium/subtle/nearly-invisible to
   roles product-wide (Section 5).
4. **Comparison matrix structural system** (Tier 4) — row/column separation,
   block headers, sticky city-bar boundary, kept flat by design.
5. **Metadata/system block grouping** (Tier 3/4) — meta-block / sys-meta /
   plate-adjacent dense metadata.
6. **Overlay treatment language** (Tier 5) — converge modal/popup/drawer focus
   depth and backdrop.
7. **Page-ground atmosphere** (Tier 2) — warmth/texture baseline for chart pages.
8. **City-intelligence grouping** (Tier 3/4) — snapshot grid, accordions,
   cost/weather tables, CI cards.
9. **Selected/active/disabled state treatment** — pills, tabs, toggles, buttons.
10. **Scaffold/future/debug quarantine** — keep Tier 6 visually separate.

Treatment roles first; final colors, type, and values later.
