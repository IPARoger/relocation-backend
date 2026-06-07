# Foundational Product Truths (From Archaeology)

**Scope:** Cross-chat themes that appeared repeatedly or were corrected forcefully by the user.  
**Status labels:** *Durable principle* = should guide decisions for years. *Product stance* = strategic positioning. *Process principle* = how the team builds.

---

## Trust and truth

- **Durable principle — Inspectable precision:** If the map shows a region, line, or overlap, it must mean something **precise** in the relocated chart model. “Plausible geometry” is not validation. Trust is built through reproducible checks, not visual confidence.
- **Durable principle — The map is the primary model (not an illustration):** Users explore **geography as astrology**. The map is not decoration around a chart calculator; it is the main instrument.
- **Product stance — Not generic astrocartography:** The ambition is a **multi-condition, overlap-aware relocation exploration tool** reframing the category toward *relocation astrology* and *intent-driven comparisons*, not only angle lines on a globe.
- **Durable principle — Professional rigor before lay simplification:** Build a **neutral, powerful professional engine first**; simplify for lay users only after the foundation is trustworthy.

---

## Overlap and decision-making

- **Durable principle — Overlap is often the answer:** The deepest product value is where conditions coincide—house + house, house + angle sign, angle + aspect corridor, multi-condition intersection. Overlap is a **semantic object**, not a rendering accident.
- **Durable principle — Tradeoffs are inherent:** “Best place on Earth” is usually the wrong framing. The tool should help users clarify priorities and compare **constrained** options (e.g. three company cities), not imply one universal optimum.

---

## Precision vs cosmetics (non-negotiable vs acceptable)

- **Durable principle — Binary regions must be honest:** House membership and angle-sign membership are effectively **in/out** for users. False membership is unacceptable even in MVP.
- **Durable principle — Cosmetic roughness can be acceptable:** Seam cosmetics, visible discontinuities, and imperfect basemap styling can be acceptable **if canonical membership remains correct** and inspectable.
- **Durable principle — Aspect intensity is continuous:** Exact aspect-to-angle **centerlines** are mathematical anchors; **auras/orbs** express continuous strength and can be softer—*but must not lie about exactness at the core*.

---

## Separation of concerns (recurring architectural moral)

- **Durable principle — Canonical truth vs display adaptation:** Backend owns **membership and identity**; display owns **wrap, clip, world copies, and Leaflet-safe fragments**. Never “fix” seams by corrupting canonical topology.
- **Durable principle — Math vs rendering diagnosis:** Errors must be classified: astrology math vs GeoJSON vs map interaction vs stale server vs wrong file vs race conditions vs **AI instruction ambiguity**. Mixing categories wastes weeks.

---

## Human + AI collaboration stance

- **Process principle — AI assists; humans validate:** Especially for map truth, AI can speed implementation but cannot become the authority that overrides chart checks.
- **Process principle — Surgical vs strategic modes:** During debugging, the user repeatedly needed **ordered surgical steps**, not architectural musings. Mismatch of mode caused major failures.

---

## Emotional tone and moat

- **Product stance — Calm, premium restraint:** “Inevitable, not clever.” Long-session comfort matters. Avoid gimmicks, neon toy UX, and astrology hype.
- **Product stance — Joy and word-of-mouth:** Deliberate exploration (“shopping the map”) is part of the value—**but only if the map is trustworthy**.
- **Continuity note (archaeology):** Technical choices that reduce **false certainty** and **opaque blocking** (e.g. staged rendering, inspectable truth, honest membership) align with the same emotional contract—users should trust the instrument over multiple long sessions, not chase a flashy map that lies or “freezes” until magic finishes.

---

## Repetition as signal

Across chats, the same phrases recur: **exactness over cleverness**, **validation before polish**, **one change at a time**, **do not solve the wrong layer**, **Map-first not form-first**. Treat these as institutional values, not slogans.
