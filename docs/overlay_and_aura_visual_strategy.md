# Overlay And Aura Visual Strategy

This document is planning only. It does not specify an implementation commitment.

**Formal epistemology and tone:** see **`docs/visual_semantic_style_guide.md`** (truth hierarchy, texture semantics, popup language, implementation discipline).

## Separating cusp softness from aspect aura (do not conflate)

Two different physical/semantic ideas must stay **visually and verbally distinct**:

| System | Role | Typical scale (starting point) | Reads as |
|--------|------|---------------------------------|----------|
| **House cusp transition** | Softens **categorical** house boundary presentation | **~2°** default gradient along cusp | *Astrological cusp softness*—not “uncertainty.” |
| **Aspect-to-angle aura** | **Angular** intensification toward exact aspect | Often **~5–8°** (or **aspect-dependent**: e.g. tighter for sextile ~4–5°, wider for conj/opp ~5–8°, user-tunable later) | *Energetic strength toward exactness*—not house category bleed. |

**Implementation risk:** reusing the same blur, same ramp curve, or same color for both reads as **one muddy metaphor** and breaks visual epistemology. House fields stay **membership/categorical** (with optional **cusp display** softness); aspect auras stay **orb/intensity** around a **centerline**. Prototype and review them **in isolation** before combining in one view.

## A. Overlap Philosophy

Overlap regions are the real answer.

Users are usually searching for combinations, not isolated conditions. The map should make the places where desired conditions overlap feel discoverable, trustworthy, and exciting without obscuring the geography underneath.

Principles:

- Overlap must remain city-readable.
- Transparency is critical.
- Users need to browse candidate cities beneath overlays.
- Overlap should feel luminous and intelligently combined.
- Avoid muddy alpha stacking.
- Avoid simple opacity escalation that turns the map dark or purple.
- The overlap system should communicate "this is a stronger candidate area" without burying labels, coastlines, or city markers.

## B. Child-Color Strategy

The eventual color system should use intentional child colors for overlaps instead of relying on accidental transparency mixing.

Goals:

- Semantic blending rather than transparency dominance.
- Predictable color outcomes for common pairings.
- Overlap colors that feel brighter, cleaner, or more luminous rather than heavier.
- UI controls should reflect selected overlay colors so the controls themselves act as the legend.

Palette families:

- House regions.
- Angle-sign regions.
- Aspect overlays.
- Exclusion/NOT overlays.

Near-term prototype idea:

- Define parent colors for each condition type.
- Define child colors for known overlap pairs or categories.
- Keep fill opacity moderate and label readability protected.
- Use debug mode to inspect overlap counts before committing to final palette.

## C. NOT/Exclusion Visual Language

Exclusion regions should not behave like positive overlays.

They should feel like off-limits or disqualified areas, not lit-up candidate areas.

Visual direction:

- Subtle blackout or desaturation.
- Grey/black treatment, but not harsh opaque black.
- Preserve geography readability.
- Avoid flooding the whole inverse region with visual noise.
- Consider texture, hatching, or faint pattern for exclusions.
- Keep the treatment calm and professional.

The exclusion layer should say "do not prioritize here" without making the map hostile or unreadable.

## D. Aura Philosophy

The current aspect system is mathematically correct but visually incomplete: it draws centerlines only.

An aura should communicate intensity proximity around ASC/MC aspect lines.

### D.0 Aura is occupancy widening from exactness — never blur

Aura is **not** a post-process applied to a line. It is the same brute-force occupancy substrate as every other layer, asked the same question at a *sequence of widening orbs*. Concretely, an aura is the set of discrete bands

- *exact* (cells where `|abs_sep − aspect_target| = 0` to grid resolution)
- `|abs_sep − aspect_target| ≤ 0.5°`
- `|abs_sep − aspect_target| ≤ 1°`
- `|abs_sep − aspect_target| ≤ 2°`
- … (further bands as the product orb allows)

Each band is a **truthful geometric distance from exactness**. Rendering intensity is then a weighted composition over these bands — through **opacity, saturation, and dot density** — not a gaussian blur, not a feather filter, not a glow effect. If a renderer cannot derive its aura strictly from these bands, it is not the aura system described in this doctrine.

### D.1 Intensity must be non-linear from edge to centerline

Intensity **may not** increase linearly from the outer orb edge to the centerline. A linear ramp produces an opaque middle corridor that fogs out the map.

The accepted curves are non-linear: **logarithmic, exponential, power-law, sigmoid**, or another deliberately concave-toward-the-line shape. Whichever curve is chosen, the consequence must be:

- The **outer aura remains restrained** — translucent, breathable, map-readable for the majority of its width.
- The **strongest visual intensity is reserved for the centerline**, and optionally for the immediately neighboring near-exact band.
- The **mid-orb is not the loudest place** — the curve must accelerate *toward* the line, not bloom around it.

The forbidden visual is a "soft speed bump": a slow uniform brightening that peaks in the middle and obscures the underlying map. The required visual is a quiet field that sharpens dramatically *at* the exact line.

### D.2 The other long-standing principles still apply

- The aura should not resemble a soft speed bump.
- The aura should be subtle at the outer edge.
- Intensity should accelerate sharply toward the centerline.
- The centerline remains the strongest/darkest point.
- The ramp should be exponential or Gaussian-like, but visually concave and elegant.
- Aura should show extra juice within broader house/sign regions.
- Backend remains the source of exact centerlines.
- Frontend rendering is preferred initially so tuning is fast and visual.

**Orb targets (product-tunable; not fixed forever):**

- **Default band** often discussed in the **~5–8°** range on either side of the centerline for strong major aspects.
- **Aspect-specific defaults** may differ: e.g. **tighter** for sextiles (**~4–5°**), **wider** for conjunction/opposition (**~5–8°**), with **settings** adjusting later.
- **Popups** remain the authority for exact orb and placement at a point; aura is exploratory.

The aura should help users see "close enough to matter" without pretending every part of the band has equal strength.

**Not the same as** the **~2° house cusp transition** in § “Separating cusp softness from aspect aura”—do not use one rendering to stand in for both.

### D.3 Proportional compression

When the corridor's total spatial width shrinks — at sextiles versus conjunctions, in **compressed high-latitude houses**, at **user-reduced orbs**, in **narrow angular corridors** — the **same intensity curve must compress proportionally with it**. The *visual energy profile* (steep outer falloff, sharp peak at the line) is what is preserved; the **spatial width is what changes**.

In practice this means:

- A tight sextile band at the same default orb scaling reads with the same *character* as a default conjunction band: restrained outer, materially-visible inner, sharp centerline. It does **not** read as "weaker because the band is thinner" or "fuller because we forgot to shrink the curve."
- A polar-compressed corridor at high latitude reads the same way: the bands narrow geometrically, but the relative weight of `≤ 2°` versus `≤ 0.5°` versus exact does **not** invert or flatten.
- A user-tightened orb (e.g. someone setting orb = 0.5° instead of 2°) does not produce a clipped wedge of the wide curve — it produces the *same curve shape* scaled into the smaller corridor.

The renderer's intensity assignment must be a function of *normalized distance from exactness within the configured orb*, not raw degrees. Configured orb becomes the unit; the shape is invariant under that scaling.

### Doctrine: non-certifying field, samples, and adaptation

- **Aspect aura is a non-certifying visual field.** It does not define membership, orbs, or legal “inside/outside” for astrology logic.
- **Authority stays on the exact angular line (engine geometry) and on point truth in the popup.** Aura is illustrative intensity language only.
- **Generation and tuning should lean on validated angular samples and realized geometry** (what the backend actually produced for the contour/centerline), not on a parallel abstract model treated as a second source of astrological truth.
- **Falloff is not a flat translucent corridor** and **need not be a mathematically exact Gaussian**; curves are chosen for legibility and honest “strength near exactness” semantics.
- **Preferred read:** **steep convex acceleration** toward the centerline—**outer ~5–8°** almost invisible, **inner ~1–2°** materially visible, **exact line** strongest.
- **Brute-force / sample-driven aura** (e.g. discrete offset bands, empirically tuned ramps) is **acceptable and likely preferable**: it can stay **robust across latitudes** and edge cases where a single closed-form field would lie or overfit.
- **High latitudes / compressed houses:** aura must **adapt—compress, fade, or both**—so it **does not overwhelm** local symbolic geometry.
- **Mute / hide / solo-style controls** belong in the long-term aura strategy: dense centerlines can **temporarily obscure city and basemap detail**; users need a way to **dissect** the view without losing truth elsewhere (see also §H).
- **Popup and exact line always win** over the aura’s **impression**; if they disagree in the user’s mind, trust **popup + line**, not the glow.

## E. Map Readability Is Sacred

The Earth layer beneath the overlays is not a backdrop the map is allowed to consume. Cities, coastlines, labels, and political geography **must remain visible** under every overlay state the product can produce — including dense triple-overlaps, narrow aura corridors, and fully-wide-orb aspect bands.

This is a **hard constraint**, not a polish-pass preference. A candidate rendering that "looks more astrological" by burying the map fails this constraint and is rejected on doctrine, regardless of how beautiful or technically elegant the post-process is.

### What the system *is allowed* to do

- Carry a strong, even **near-opaque, exact centerline**.
- Carry one **materially-visible near-exact band** immediately adjacent to that centerline.
- Use color to declare overlap semantics (parent and child colors).
- Use opacity, saturation, and dot density as the *legitimate* knobs for aura intensity (§D.0).

### What the system is *not allowed* to do

- Produce giant opaque washes.
- Produce muddy overlap or atmospheric soup.
- Produce over-dense middle bands.
- Make city labels illegible at the relevant zoom.
- Make coastlines or country boundaries disappear under aura or fill.
- Turn dense city areas into visual soup.

### Requirements (operationalized)

- City labels remain readable.
- Candidate cities remain clickable/discoverable.
- Coastlines remain understandable.
- Country boundaries and major geography do not disappear.
- Overlays do not create large muddy regions.
- Dense city areas do not become visual soup.

The visual system should *reward* exploration. Users should want to keep looking at the map; the experience must remain contemplative and premium. If a candidate aura curve, palette, or composite cannot satisfy both "centerline reads as strongest" and "labels remain legible behind it", the candidate is wrong and must be retuned — not shipped behind a settings toggle.

## F. Open Technical Questions

Frontend rendering approaches to investigate:

- Canvas layer for aura fields.
- SVG paths with multiple strokes and opacity falloff.
- CSS/SVG blur, if controllable enough.
- Precomputed parallel stroke bands.
- Additive or screen-like blend modes.
- Gaussian/exponential opacity ramp.
- WebGL only if Canvas/SVG cannot perform adequately.

Questions:

- Can Leaflet Canvas handle multiple aura bands smoothly?
- Are blend modes consistent enough across browsers?
- How many simultaneous overlays can render before interaction feels sluggish?
- Should aura rendering use viewport clipping?
- Should aura be hidden or simplified at low zoom?
- How should aura interact with overlap colors?
- How should NOT/exclusion overlays visually combine with aura?

Recommendation before implementation:

1. Prototype one centerline aura style with Canvas/SVG.
2. Test with ASC all-major plus house/sign regions.
3. Tune for city readability first, beauty second, and mathematical explanation third.
4. Only then generalize to all aspect overlays.

## G. Color, texture, opacity, and “mute” (near-term semantics)

**Color families** today are **functional, not cosmological**: house conditions A/B/C use a fixed triad; angle-in-sign uses **purple** as a separate categorical family; aspect overlay uses **teal** for polylines. That reads as **arbitrary but learnable** until a deliberate child-overlap palette exists (see §B).

**Triple overlap** (two house fills + purple angle-in-sign, often plus teal lines) is **legitimately hard to read**: alpha stacking can look “too perfect” (clean Venn-like seams) when the underlying geometry is **merged rectangles on a grid**—those edges are **piecewise axis-aligned**, not organic boundaries. The brain may infer a single synthetic region instead of three simultaneous truths.

**Purple dilution**: when purple is alpha-blended with warm house hues, it **loses instant “angle-sign” legibility**. Mitigations to consider later (prototype-only): slightly **lower** house fill opacity when angle-sign is active; **outline-only** or **inner stroke** for angle-sign; or **muted / solo** toggles (§H).

**Texture / pattern** is **not** a casual add-on: hatch direction or grain must not be mistaken for uncertainty bands. If explored, keep it **extremely subtle**, **feature-flagged**, and **validated** against cusp/orb semantics in `docs/visual_semantic_style_guide.md`.

**Cosmetic smoothing** of polygon boundaries (blur, heavy simplification, antialiasing tricks that widen/narrow the true set) must **not** substitute for **finer truth_grid resolution** or a smoother **geometric representation** that is still **set-equivalent** to the sampled field.

## H. Layer mute / “audio mixer” model (future control)

Future layer UI should treat each semantic layer like **tracks in a mixer**:

- **Mute** or **hide** individual house conditions (A/B/C), angle-in-sign, or aspect overlay **without** forcing users into a single-variable mode.
- **Solo** (temporary) is optional: isolate one condition to inspect boundaries, then restore others.
- Goal: make **complex overlaps inspectable** without nannying users away from multi-variable search—the map should support **dissection**, not prohibition.

This is **documentation-only** here; implementation can follow a small toggle strip or a drawer, once overlay identity is stable in the renderer.

## I. First-run onboarding: map veil / spotlight (future)

The inline “Using the map” card is **intentionally minimal** today. A stronger first-run pattern would:

- **Dim** the basemap slightly (e.g. semi-transparent scrim) while preserving geographic context.
- **Spotlight** or center the instructional copy on **right-click for point-truth** (relocated chart popup).
- **“Got it”** dismisses the veil and restores full contrast; persist dismissal in **session** or **local** storage.

**QA / repeat visits:** URL flags (`skipOnboarding`, `debugGeometry`, `traceConditions`, `showLegend`) skip the onboarding toast so manual passes are not blocked.

No commitment to build the veil in this iteration; keep behavior documented for product polish.

## J. Current palette is proof-of-concept only

The colors currently in use across the brute-force sandbox and `map_CURRENT.html` (yellow / blue / rose for the A/B/C house family, purple for angle-in-sign, teal for aspect overlay, deep slate for triple-overlap) are **proof-of-concept colors, not the final visual language**.

### What the current palette validates

- **Overlap semantics** — distinct colors per condition make the overlap math visible and testable.
- **Occupancy logic** — yellow vs. blue vs. green vs. slate makes truthful per-cell membership obvious in screenshots and in validation reports.
- **Blending mechanics** — translucent stacking proves that brute-force overlap is mathematically real, not a render-time gimmick.

These are *engineering* validations. They prove the substrate is correct. They do **not** prove the colors themselves are the right product expression.

### What the current palette does **not** decide

The current colors do not commit the product to any of:

- **Base color system** (which families exist, what each means symbolically and emotionally).
- **Overlap child colors** (the deliberate, named hues for two- and three-way overlaps, replacing accidental alpha blends).
- **Translucency hierarchy** (per-layer opacity governance so the map does not turn into atmospheric soup).
- **Accessibility** (color-blind robustness, contrast against basemap variants, contrast against labels).
- **Dark-map and light-map behavior** (each color must hold up against both basemap polarities).
- **Emotional tone** (contemplative vs. clinical vs. energetic — currently undecided, deliberately).
- **Perceptual harmony** (whether the palette reads as one designed system rather than a debug rainbow).
- **Label readability** under every overlay state.
- **Contemplative UX** (the experience the user has when sitting with the map for minutes, not seconds).

### Future selectable visual style presets

Future visual style presets may let users or professionals choose the emotional material language of overlays without changing the underlying truth geometry. Possible preset families:

- **Buck Rogers / technical** — instrument-like, diagnostic, precise.
- **Crunchy organic** — earthier, less clinical, still disciplined.
- **Premium lifestyle** — restrained, elegant, design-forward.
- **Gentle new age** — optional and cautious; never allowed to become mystical fog, spiritual cliché, or glow theatre.

All presets must share the same truthful transport geometry, side-local normalization, proportional compression, and popup truth. Styles may vary palette, material finish, contrast, and emotional tone; they may not vary the math truth or imply different astrological certainty.

The current transported-material renderer is a **beta placeholder**, not final aesthetic approval. Later design AI or specialist review should refine the premium material language on top of the stabilized renderer doctrine, not redesign the transport math to chase a style.

### Future color pass

A dedicated **graphics / design specialist pass** is reserved for these decisions, once the substrate (brute-force occupancy, multi-condition, aura, transit, NOT-overlays) is stable enough that the specialist is designing on top of *fixed* semantics. Before that pass, the current palette is locked as "good enough to inspect the math, not good enough to ship as the brand."

The ordering is intentional: **truthful geometry first, beautiful restrained visual language second.** A design pass before the substrate is settled would force the specialist to keep redesigning around moving math; doing it after means the specialist is free to focus entirely on color, tone, hierarchy, and emotional restraint.

