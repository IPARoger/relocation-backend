# Visual & Semantic Style Guide (Relocation Map System)

**Status:** Planning and doctrine. This document defines **what visuals mean** and **how they should behave**. It does **not** mandate implementation order or ship dates.

**Companion docs:** `docs/overlay_and_aura_visual_strategy.md`, `docs/ux_principles_and_emotional_tone.md`, `docs/map_and_overlay_design_research.md`, `docs/brand_and_experience_foundations.md`, `docs/intentionality_and_symbolic_constraints.md` (fate/agency/tradeoffs), `docs/ai_constitution_and_review_architecture.md` (interpretive AI governance: reviewer layers, anti-patterns). Visual epistemology here pairs with those interpretive doctrines.

**Discipline:** Future rendering work should follow this guide so the product does not drift toward **debuggy/generic** UIs or **beautiful-but-unusable** spectacle.

---

## 1. Visual epistemology (truth hierarchy)

| Surface | Role | Semantic contract |
|--------|------|-------------------|
| **Right-click / point popup** | **Canonical point truth** for the queried location | Authoritative for “what is true *here*” at that click (degrees, houses, etc.). |
| **Map overlays** | **Exploratory fields** | Show *where* conditions hold as regions/lines; optimized for browse and compare, not a full chart printout. |
| **Account / chart pages** | **Full scientific dump** | Full relocated chart, aspect tables, comparisons, dense technical layout as appropriate. |
| **Cards / favorites / comparison UI (future)** | Same **information language** as popups where possible—shorthand and calm, not a second dialect. |

**Popups are appetizers, not full chart reports.** They must stay information-dense but **legible**; the heavy tables belong off-map.

**Direction:** City popup, right-click popup, favorites, and comparison snippets should **converge** on one typographic and labeling convention (headers, planet weight, house alignment).

---

## 2. House field semantics (categorical + cusp softness)

- **Planet-in-house regions are categorical fields:** inside/outside membership for the chosen house rule must stay **truthful** (already a product moral).
- **Visual breadth:** regions may read **broad and soft** at the polygon edge as long as **membership** remains correct for the engine’s definition.
- **Cusp transition (planned visual encoding):** a **~2° default** blend along house boundaries expresses **astrological cusp softness**, not epistemic uncertainty. Copy/tooltips should eventually explain this as **cusp transition**, not “we’re unsure.”
- **Texture family:** If house fields use **ultra-faint** directional texture (see §5), it must stay in the **same semantic family** as the house layer—never decorative GIS striping.

**Future `?` affordance:** Short explanation of cusp-gradient semantics (link or inline help).

---

## 3. Aspect-to-angle aura semantics (intensity, not category)

- **Centerline = exactness anchor:** mathematically exact aspect-to-angle geometry stays the spine; aura does not redefine membership.
- **Aura = energetic / angular intensification** in orb space: “closer to exact = stronger,” **not** a category bleed like house-to-house.
- **Shape language:** Gravitational, **concave**, sharpening toward the line—**avoid** Gaussian mush and “speed bump” blobs.
- **Orb policy (product parameter, not one size fits all):** defaults may vary by aspect family, e.g. **tighter** for sextiles (~4–5°), **wider** for conjunction/opposition (~5–8°), **user-adjustable** in settings later. **Popup** remains authority for exact placement/orb at a point.
- **Aura guides exploration**; it must not read as **final judgment** where the popup disagrees.

**Critical separation:** **~2° house cusp gradient** (boundary softness within the **categorical house field**) and **~5–8° (or rule-based) aspect aura** ( **angular** intensification) are **different systems**—see `docs/overlay_and_aura_visual_strategy.md` § “Separating cusp softness from aspect aura.” **Do not conflate** them visually (same ramp, same color, or same blur on both).

---

## 4. Overlay texture semantics (almost subconscious)

- Texture should be **barely consciously visible**—orientation or grain hint only.
- **Never** heavy GIS striping, hatch spam, or high-contrast patterns.
- **Planned differentiation (future):** planet-in-house could use **ultra-faint diagonal** in one direction; angle-in-sign could use the **opposite** faint diagonal; their overlap may read as a **subtle crosshatch** without overwhelming cities.
- Additional layer families (future) might use **dots or orthogonal lines** only where needed for discrimination under transparency—not for decoration.
- **Purpose:** semantic differentiation **under** transparency and overlap, not ornament.

---

## 5. NOT / exclusion overlays

- **NOT must not “light up” the whole allowed world** with a positive, saturated overlay.
- Prefer **soft veil:** desaturation, muted grey/black scrim, low-contrast treatment; geography stays **readable**.
- **Tone:** “Off limits / deprioritize,” **not** punitive blackout or alarm red.
- Texture on exclusions, if any, comes **later** and stays calm—see `overlay_and_aura_visual_strategy.md` § NOT.

---

## 6. Color philosophy

- **Avoid:** arbitrary rainbow assignments, **neon**, **muddy opacity stacking**, **generic SaaS** purple-teal dashboards.
- **Prefer:** calm, restrained, emotionally intelligent palettes; overlap **readability** beats color “purity.”
- **Planet colors (future):** may align with traditional associations but **softened** for basemap contrast and accessibility.
- **Control / card tinting:** may echo **output colors** only when **readability and elegance** hold (current prep tints in `map_CURRENT.html` are examples of “direction,” not final law).
- **Overlaps:** **Child-color / semantic overlap** behavior—**not** naive alpha mud (see overlay doc §B).

---

## 7. Popup visual language

- **Headers:** may be **bold**; **planet names** stay **regular** weight.
- **House numbers:** aligned and scannable (e.g. centered under a **House** column header).
- **Density:** high information, low noise—no redundant **ASC Sign** / **MC Sign** lines when sign is already in the **ASC/MC degree** string.
- **Future subtle encodings (optional):** house column might hint **house identity**, **cusp softness**, or **near-cusp** greyscale—**very subtle** only.

---

## 8. Interface tone

- **Quiet analytical instrument.**
- **Contemplative, map-first.**
- **Premium restraint**—elegant, not precious; beautiful, not distracting.
- **Reject:** over-clever UI, debug clutter, generic dashboard chrome, **clubby** maps, **toy astrology** neon, **corporate SaaS** sameness.

---

## 9. Map and control relationship

- The **map is the main experience**; controls **support** exploration then **recede**.
- **Search / location** may move **onto the map body** (centered, lightweight)—sidebar is not the long-term home for global place entry.
- **Reset map** behaves as a **map-native** affordance (e.g. near zoom controls), not a sidebar oddity.
- **Onboarding** for right-click truth: **one-time**, map-centered overlay—not permanent sidebar copy.

---

## 10. Account / chart page relationship

- **Map popups = shorthand.**
- **Account / chart pages = full data** and the place to set **emotional tone** for “serious tool”: restrained, inevitable, professional, calm.
- **Comparison views** may be **densely tabular** where the map stays sparse.

---

## 11. Implementation discipline

- **Do not** let agents invent visual behavior without matching this epistemology.
- Prefer **feature flags**, branches, or small throwaway prototypes for new encodings.
- **Preserve math and contracts** while tuning visuals; regress with point popups and validators.
- **City readability** is a **hard constraint**—if a visual encoding kills cities, it fails.
- **Explicit stop points:** e.g. “ship cusp gradient prototype only on one house mode + one fixture before globalizing.”

---

## Unresolved design questions (explicit)

- Exact **cusp gradient** math vs display (2° default): implementation in **truth_grid** vs **purely painterly** edge—needs ADR when built.
- **Per-aspect orb** table vs continuous slider UX.
- **Texture** on house vs angle-sign: performance and export (SVG vs canvas) when multiple layers stack.
- **Popup convergence** timetable: city vs relocated vs future favorite card parity.
- **Colorblind** validation paths for child-color overlaps and NOT layers.
- **Overlap legibility pass (deferred):** current purple-heavy stacks and fixed opacities are interim. Future work needs a deliberate **color-theory / adaptive-opacity** pass (child colors, subtle texture/hatching, layer mute rules)—possibly assisted by design exploration—not naive alpha stacking. See `validation/narratives/map_current_qa_cleanup_pass.md`.

---

## What should **not** be implemented yet (from this guide alone)

- Final **texture** passes on production tiles without prototypes.
- **NOT** layer semantics before positive overlap palette is stable.
- **Account/chart** visual system beyond placeholder—this doc sets **intent**, not screen specs.
- **Automatic** Cursor-driven “beauty refactors” without checklist against §1–3 and city readability tests.

---

## Revision

Update this document when **palette**, **orb policy**, or **truth hierarchy** decisions change; cross-link `ai_context/decisions.md` when a choice becomes formal.
