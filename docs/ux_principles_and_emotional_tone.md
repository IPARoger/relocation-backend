# UX Principles and Emotional Tone

A concise distillation of how the product should **feel** and **behave**. Complements `docs/relocation_app_product_roadmap.md` (strategy) and `docs/overlay_and_aura_visual_strategy.md` (visual planning).

---

## 1. Core temperament

| Principle | Meaning |
|-----------|---------|
| **Elegance** | Fewer controls, clearer hierarchy; every element earns its pixels. |
| **Inevitability** | Interactions feel obvious after one use—not because they’re novel, but because they fit the mental model. |
| **Restraint** | Premium is **quiet**; confidence without shouting. No astrology hype aesthetic. |
| **Anti-gimmick** | Reject “clever” animations, mystery meat icons, and puzzle UI. |
| **Anti-overdesign** | No speculative chrome before map truth and readability are solid. |

---

## 2. Map-first atmosphere

- The **map is the instrument**, not a illustration behind forms.
- **Contemplative** pacing: users may spend long sessions panning and comparing—comfort matters more than initial “wow.”
- **Professional trustworthiness:** numbers, regions, and overlaps must **mean** something inspectable; visual polish never substitutes for false certainty.

---

## 3. Delight without spectacle

- **Subtle delight:** smooth staging (e.g. progressive overlays), thoughtful typography, readable defaults.
- **Invisible power:** advanced checks (popups, edge QA) exist without cluttering the default surface.
- **Clarity over spectacle:** if a visual effect obscures city names or coastlines, it fails—**no matter how beautiful**.

---

## 4. Overlap readability philosophy

- **Overlap is often the answer:** multi-condition intersections are the decision object, not accidents of alpha stacking.
- **City readability priority:** candidate places must remain discoverable **under** overlays (see roadmap §4).
- **Semantic overlap colors:** prefer designed **child colors** over muddy accidental blends (`overlay_and_aura_visual_strategy.md`).
- **NOT / exclusion:** visually distinct, calm, “off-limits” language—never a glowing inverse continent.

---

## 5. Typography and color tone

- **Typography:** calm, legible, slightly restrained; popups and labels should feel **instrument-grade**, not marketing banner.
- **Color:** grayscale-friendly structure; overlays use controlled families; reserve strong saturation for **meaning**, not decoration.
- **Long-term:** theme-aware palettes (light/dark basemaps) without losing semantic distinction—especially for colorblind-safe planning.

---

## 6. Layout cautions: drawer / genie / chrome

- Full **drawer or genie** redesigns are **deferred** until a design system exists (`decisions.md`)—they are high **UX and architecture** risk.
- Until then: **compress** the prototype sidebar; prove information hierarchy before relocating it into animated shells.
- Any collapsible UI must preserve **obvious restore** affordances (users must not lose the map’s context or their controls).

---

## 7. Mobile and tablet

- **Honest positioning:** desktop-first professional instrument for near-term MVP.
- **Tablet:** prioritize pan/zoom + readable typography; avoid cramming full sidebar—**progressive disclosure** or bottom sheet patterns *later*, with the same map-first rule.
- **Right-click / inspect truth:** mobile needs an **equivalent gesture** eventually (`open_questions.md`)—plan before parity claims.

---

## 8. When to stop designing

Stop and ship incremental UX when:

- Map **truth** regressions would dominate any visual win.
- A redesign **orphans** validation habits (screenshots, popups, fixture workflows).
- The team is **debating aesthetics** while **overlap readability** or **city labels** still fail in realistic regions.

**Rule:** **Validation before polish**; **one change at a time** for risky rendering paths.

---

## 9. Where philosophy is already strong in the repo

- Explicit **non-AI professional core** and **map-as-model** stance (`core_product_truths.md`, roadmap).
- **Overlap as semantic object** and child-color direction (`overlay_and_aura_visual_strategy.md`).
- **Centerline vs aura separation**—do not blur truth for prettiness.

---

## 10. Where philosophy could still drift

- **Custom controls** replacing native selects without a11y and proven necessity.
- **Heavy animation** or **game-like** map chrome creeping in during fatigue.
- **Positioning language** (“decision intelligence”) leaking into UI copy before ethics/marketing review.
- **Migration churn** (map libraries) driven by FOMO instead of evidenced blockers—see `docs/map_and_overlay_design_research.md`.

---

## Related docs

- `docs/relocation_app_product_roadmap.md`
- `docs/overlay_and_aura_visual_strategy.md`
- `docs/next_implementation_sequence.md`
- `docs/map_and_overlay_design_research.md`
- `memory_archaeology_raw/consolidated_notes/ux_and_design_language.md`
- `ai_context/core_product_truths.md`
