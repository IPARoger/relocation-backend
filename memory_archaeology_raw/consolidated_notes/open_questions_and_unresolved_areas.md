# Open Questions and Unresolved Areas (From Archaeology)

These are **not** a bug list. They are **institutional uncertainties** that multiple chats circled without final product canon.

---

## Geometry and calculation semantics

- Formal spec for **MC** presentation: relocated ecliptic MC vs culmination/RA line products—must be explicit in user-facing language and internal tests.
- Full **DC/IC** surface area: ASC+180 heuristics vs distinct professional semantics; staged rollout vs early completeness.
- **Polar / high-latitude policy:** reconcile archaeology’s mixed numbers (±60, ±65, grids -60..86) into a user-understandable policy + advanced override stance.
- **House systems beyond Placidus** and polar fallbacks—when, how, and with what disclosures.

---

## Rendering architecture

- Long-term **display adapter** strategy: world copies, fragment IDs, picking behavior, performance budgets.
- Aspect **aura implementation**: stacked strokes vs raster/canvas/WebGL; ensuring aura does not imply false membership.

---

## Validation systems

- Automating regression: what becomes CI vs quarterly manual QA vs “validation dossier only.”
- Formal **aspect-group** tests as semantic entitlements (hard/soft/major) independent of geometry engine.

---

## UX systems

- Replace fixed panel with **drawer / collapsible rail** without losing obvious restore affordances.
- Mobile equivalents for **right-click truth** interactions.
- Onboarding for professional gestures without patronizing lay mode.
- Mobile layer-control pattern for mute, solo, send-to-background, send-to-foreground, and negative / NOT mode without creating Photoshop-style panel complexity.
- Whether overlap hot zones should ever be highlighted by default, or only through explicit user-controlled modes.

---

## Data + search

- Final geocoder/data strategy for global professional use.
- Ranking function for city search that combines population, fame, administrative importance, and user intent.

---

## Product scope and ethics

- How public positioning should read: astrology-forward vs broader decision-intelligence framing.
- NOT/exclusion overlays: semantics + minimal frightening UX + interpretive responsibility.
- How to communicate “notable overlap” or “high-concentration zone” without paternalistic ranking or implying the app knows the user's best life choice.

---

## Renderer beta stabilization questions (Chat 08)

- Does the transported-material renderer survive real Leaflet map context with labels, zoom, pane ordering, and production density?
- Which overlap failures are mechanical readability problems versus aesthetic/palette problems?
- What child-color or muted compositing system best preserves semantic overlap hot zones?
- How should dense centerlines behave in already-overlapped polygon regions?
- What should a future design AI refine: material language, palette, style presets, or surface coherence, without reopening transport architecture?
- When should rain/virga work begin relative to final map-context validation?

---

## Operational workflow

- Canonical filenames/modules and archival discipline (still cited as recurring failure mode).
- Rules for committing **proof artifacts** vs **machine junk** (tmp browser profiles, etc.).

---

## Weak archaeology coverage (second pass, 2026-05)

- `chat_07_*` is **useful as a topic index and audit prompt**, not as a complete substitute for substantive extracts (`chat_02`, `chat_06`, etc.).
- `current_chat_*` remains **intake-empty on disk** — if the user has new prose only locally, paste into that file or a numbered chat extract before the next consolidation pass.

---

## Human review gate

Any item above that touches **clinical certainty**, **medical/legal relocation claims**, or **public marketing language** should be reviewed by the human founder before becoming “official doctrine.”
