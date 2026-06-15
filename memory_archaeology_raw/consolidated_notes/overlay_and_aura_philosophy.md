# Overlay and Aura Philosophy (From Archaeology)

---

## Centerline + aura model (dominant lesson)

- **Backend:** exact aspect-to-angle **centerline** (mathematical anchor).
- **Frontend:** **aura / glow / orb feel** as presentation—must not shift the anchor in ways that imply a different solution set.

**Why:** Gaussian blur and “make the line pretty” operations can translate geometry and create false loops; astronomical solving and aesthetic blur must not be conflated.

---

## Primary terrain vs intensifier (“juice”)

Repeated mental model:

- **House polygons / broad regions** = primary terrain (where a condition is true).
- **Aspect-to-angle overlays** = intensifiers: narrower, higher-energy structure inside broader regions.
- UX consequence: users may first find broad favorable geography, then locate **hotspots** within it (e.g., “Budapest vs Berlin” style arbitrage).

---

## Overlap semantics

- Overlap is often the meaningful object: combined conditions simultaneously true.
- Natural transparency blending can be visually elegant, but **must be designed** so overlaps do not become unreadable mud.
- **Child-color / semantic blending** remains debated: additive blends vs designed overlap palette vs patterns for dense stacks.

---

## Orb language

- Astrology uses **orbs**; maps compress orb into pixels—this must be explicit to avoid false certainty.
- **Late-cusp transition** concept appears repeatedly: interpretive handling of last degrees of a house (often near **2°** adjustable), visually distinct from membership lies.

---

## NOT / exclusion overlays

- Strategically important for “avoid Saturn in 12th,” etc.
- Visual grammar should not look like “positive candy color on the whole globe inverse.”
- Prefer **muted / hatched / desaturated** treatments that communicate constraint without dominating basemap readability.

---

## City readability under overlays

- If overlays hide cities, users cannot act in the real world. **Readability is sacred.**
- Marker styling patterns appear: subtle white fill + dark stroke; population/zoom-thinning strategies.

---

## Implementation notes called out in archaeology

- “Fibonacci-like” multi-stroke glow weights as a deliberate aesthetic sharp-center solution (DeepSeek extract).
- MC vs ASC glow hierarchy discussions (ASC psychologically “louder” in some design notes)—**product decision**, not a law of nature.

---

## Known unresolved visual systems

- True aura may eventually require canvas/WebGL/shaders vs stacked polylines—explicitly deferred in multiple threads.

---

## Chat 08 update: transported material strip doctrine

The renderer stabilization phase pivoted the aspect-to-angle visual model away from “aura around a spline” and toward **transported material strip** doctrine.

Durable distinction:

- **Wrong mental model:** glow, aura, gaussian blur, alpha haze, feathered polygon, emitted light, spline-distance opacity, or separate centerline stroke.
- **Accepted beta mental model:** a solid material profile transported through geometry with local `(s,u)` texture coordinates.

Core invariant:

- Each rendered sample determines local station coordinate `s`.
- Each side determines local cross-strip coordinate `u` independently.
- The renderer samples a material profile by `u`.
- The ridge is embedded inside the same material field, not drawn as a separate stroke.

The accepted architecture is validation/beta-stabilized, not final aesthetic approval. Future design work may refine palette, material language, matte/enamel feel, and style presets, but should not reopen transport architecture unless map-context validation proves structural failure.

### Psychological project-state transition

Chat 08 marks a state change from renderer existential instability to constrained iterative refinement. Future work should assume the transported-material architecture is stable enough to refine safely inside its constraints. AI should not "solve" the frozen architecture again when the remaining issue is palette, material language, overlap governance, or map-context validation.

### Proportional side-local scaling

Asymmetric bands must scale the full material hierarchy proportionally on each side. A 3-degree side is **not** a cropped 10-degree side; it is the same material logic compressed into less local width. This applies to ridge width, adjacent compression, mid-body, release timing, and edge residency.

### Overlap hot zones

Overlap regions are semantically important discovery zones, not merely clutter. Future overlap design must preserve readability while still signaling “this combination matters.” Any hotspot emphasis should remain subtle, optional or user-controlled, and avoid paternalistic ranking language.

### Layer controls and negative mode

Future overlap-heavy maps likely need mute, solo, send-to-background, send-to-foreground, and explicit negative / NOT / exclusion controls. Negative mode is for user-declared unwanted placements and should read as quiet charcoal/redacted constraint, not maximal red danger.
