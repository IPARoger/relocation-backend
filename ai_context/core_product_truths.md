# Core Product Truths

These are durable principles that should survive individual implementation chunks, UI experiments, and future chat transitions.

## Astrology Truth

- Map overlays must agree with point-and-click astrology truth.
- Popup point-truth validation is authoritative for local membership checks.
- Canonical backend truth must not be altered to satisfy frontend display constraints.
- Frontend wrapping, clipping, or rendering should never change logical astrology membership.
- `truth_grid` is the canonical architecture direction for house overlays and other binary region searches where sampled truth is more reliable than contour topology.
- Contour output may remain as fallback, but false region membership is not acceptable.
- ASC/MC aspect centerlines should preserve astrology semantics while rendering and UX can evolve.

## Inspectability

- Features should remain traceable from backend canonical identity to frontend display representation.
- Debug modes should expose canonical IDs, display IDs, generation mode, and validation metadata where useful.
- Validation records are part of the project memory and should be preserved when they explain decisions.
- Difficult charts, seam cases, and edge cases should be treated as first-class proof points, not afterthoughts.

## Map and Overlay UX

- The map is the primary visual instrument.
- Overlap readability is essential because overlap is how candidate city regions become meaningful.
- Overlay color and transparency should keep city labels and geographic context readable.
- Naive alpha stacking should not be allowed to create misleading visual dominance.
- Aspect lines can later gain aura/intensity fields, but exact backend centerlines remain the source of truth.

## Product Experience

- The app should feel professional-grade, calm, premium, restrained, and trustworthy.
- Avoid overdesign and clever interactions that create artificial stupidity.
- Controls should serve exploration, not dominate the map.
- The professional non-AI workflow must remain fully usable.
- AI should come after a strong non-AI foundation and should support user intention rather than replace professional judgment.

## Visual / Semantic Product Identity

High-level visual epistemology—**what the UI is allowed to mean**—without locking in pixels, shaders, or layer mechanics. Details and experiments live in `docs/visual_semantic_style_guide.md` and `docs/overlay_and_aura_visual_strategy.md`.

- **Popup truth hierarchy:** Point-level popups (e.g. right-click relocated truth) are **authoritative for “here”**—membership and values at that coordinate. They are **shorthand**, not full chart reports.
- **Overlays as exploratory fields:** Map regions and lines show **where** conditions hold for browsing and comparison; they must not contradict popup truth at the same point.
- **Account / chart pages for deep analysis:** Full relocated chart, tables, and comparisons belong in **account/chart surfaces**—dense technical readouts are appropriate there, not in the map popup.
- **Map-first, contemplative atmosphere:** The map is the primary instrument; the experience should support **long, calm** exploration.
- **Restrained premium tone:** Professional and inviting without gimmicks, neon, toy astrology, or generic dashboard chrome.
- **Overlap readability as a core UX constraint:** Candidate places and labels must stay discoverable; naive opacity stacking that muddies the map is unacceptable.
- **Semantic differentiation over decorative styling:** Visual choices should encode **meaning** (condition families, overlap semantics, exclusion tone)—not ornament.
- **Anti-neon, anti-dashboard, anti-kitsch:** Avoid high-chroma accent soup, corporate SaaS sameness, and astrology “club” flash.
- **Calm analytical instrument:** The product should read as a **quiet tool for judgment**, not a performative showcase.
- **City readability priority:** Geography and city context stay legible under overlays; beauty never buys cover over basemap truthfulness.
- **Exploratory overlays vs authoritative popup:** Overlays **guide** where to look; popups **settle** local truth. Future cards (favorites, comparisons) should share this **interaction language**.

## Emotionally non-interfering design (experiential constraints)

**Not marketing**—these are **durable experience constraints** for future UX and rendering (fuller articulation: **`docs/brand_and_experience_foundations.md`**).

- **Conditions for imagination:** The UI should not **compete** with the user’s inner exploration; it **holds space** for projection onto cities and possibilities.
- **Warm, contemplative safety:** Aim for a **breathable, calm, trustworthy** atmosphere—supporting **long exploratory sessions** without fatigue or emotional noise from the chrome.
- **Excitement from exploration, not UI theatrics:** Avoid neon, dopamine mechanics, and performative delight **as substitutes** for meaningful map work.
- **Symbolic / pre-verbal legibility:** Overlays, softness, restraint, aura, gradients—when used—belong to a **quiet visual language** aligned with honest epistemology (see Visual / Semantic Product Identity).
- **Fantasy with epistemic honesty:** Support imaginative use while **popup truth hierarchy** and membership honesty stay non-negotiable.
- **Beauty from truthful systems:** Prefer emergence from **correct, intelligible** interaction systems over **decorative** styling.
- **Principle continuity:** Preserves **anti-overdesign**, **anti-neon / anti-SaaS / anti-kitsch**, **aesthetics serving truthfulness**, **map-first** contemplation, and **instrument—not dashboard**.

## Interpretive language and emotional transparency (doctrine)

**Not polish for mechanical copy**—**durable doctrine** for how **language** (including future **AI** and **education**) may carry **astrological** meaning while the **UI stays non-interfering**. Full articulation: **`docs/brand_and_experience_foundations.md`**.

- **Chrome calm, astrology vivid when warranted:** The **interface** remains **non-coercive** and restrained; **depth and charge** in **content** come from **symbolism** when it **earns** evocation—not from hype or product voice stealing focus from the chart.
- **No competition with interpretation:** Product language and assists must **support** user and chart **interpretation**, not **supplant** or **oversteer** it.
- **Honest register:** Evocative language is allowed **when grounded** in what the chart can support; reject **manipulative certainty**, **destiny theater**, and **cosmic clickbait**.
- **Openness:** Preserve **imagination, symbolic richness, projection**—avoid forensic closure where astrology calls for **living** meaning.
- **Multiple affects, quiet shell:** Content may span many emotional registers; the **UI** stays **quiet** so those registers **read as chart-true**, not **UI-manufactured**.
- **Continuity:** Holds **emotionally non-interfering design**, **epistemic honesty**, **instrument not dashboard**, **anti-overdesign**, and **symbolic** map language as **non-contradictory** partners to interpretive depth.

## Interpretive integrity and archetypal honesty (doctrine)

**Consolidated relocation / intentionality frame:** **`docs/intentionality_and_symbolic_constraints.md`** (fate-within-agency, tradeoff intelligence, AI governance).

**Durable doctrine** for how **language and AI** handle **meaning** without distorting **symbolic structure**. Full articulation: **`docs/brand_and_experience_foundations.md`**.

- **Difficulty stays real:** Help users **integrate and strategize** around hard placements; do not **erase** or **relabel** them for comfort. Archetypes keep their **structural** identities; tradeoffs stay **visible**.
- **Tradeoff intelligence:** Relocation work is **honest comparison** of configurations—not claiming every option is equally easy.
- **Illuminate, don’t rewrite:** Content may explore **possibilities inside** the chart; it must not **pretend** the chart said something else. **Positive framing ≠ distortion.**
- **Recognition, realism, nuance:** Prefer readings that support **maturity** and **openness** without **fatalism** or **hype**; **astrology first, narrative second** (user supplies life detail and agency).
- **Continuity:** Aligns with **interpretive openness**, **anti-hype**, **epistemic honesty**, **non-interfering** UI, and **instrument not dashboard**.

## Development Discipline

- Prefer small reversible changes with clear validation.

## Where the nuanced history lives

Institutional memory synthesis from multi-chat archaeology (including pivots, rejections, and repeated anti-patterns) is captured in:

- `memory_archaeology_raw/consolidated_notes/` (themed synthesis)
- `memory_archaeology_raw/pending_imports/` (raw extracts; authoritative for quoted rationale)
- `docs/institutional_memory_synthesis.md` (bridge document with status labels)
- **`docs/ai_constitution_and_review_architecture.md`** — layered governance, reviewer duties, anti-pattern inventory (interpretive systems).
- `docs/visual_semantic_style_guide.md` (visual epistemology and overlay semantics)
- `docs/brand_and_experience_foundations.md` (tone and experience foundations—not a brand book)
- Avoid large rewrites when the current milestone is working.
- Keep production app behavior separate from local infrastructure experiments.
- Keep secrets, local scratch, and browser temp artifacts out of git.
- Preserve useful archaeology, but curate it into durable memory before relying on it.
