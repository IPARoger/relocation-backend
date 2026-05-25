# Aura Visual Design Brief

## Status
Draft, active design doctrine.

This document captures the current visual and conceptual direction for aura rendering in the relocation app.

It is not a final rendering specification.
It is a visual-design and product-doctrine brief to guide future mockups, experiments, and eventual implementation.

---

## Purpose of Aura

Aura is a visual intensity field around exact angular or aspect conditions.

It is **not** decorative fog.
It is **not** mystical atmosphere.
It is **not** an interpretive overlay pretending to be truth.

Its purpose is to visually show:

- where a condition becomes more exact,
- where its influence intensifies,
- and where a broader desirable region contains extra concentration or “juice.”

Example:

A user may already be viewing a broad region where **Sun in the 1st house** is true.
Within that region, an aura around **Sun conjunct Ascendant** helps show where the placement becomes especially strong.
This helps the user identify cities or sub-regions with more concentrated power inside an already desirable zone.

---

## Separate Visual Languages

The visual system currently has three separate visual languages that must be designed independently before they are combined:

- aspect-to-angle bands,
- rain discovery for user-selected polygons/regions,
- virga ghost discovery for unselected sibling regions.

These should not be combined yet.

Do not use rain or virga visuals for aspect-to-angle bands.

Do not use aspect-band visuals for polygon discovery.

Do not proceed to combined animation before each target is independently approved.

---

## Aspect-to-Angle Bands

Aspect-to-angle visuals are bounded orb/intensity bands, not diffuse aura clouds.

Aspect-to-angle bands are continuous gradient fields, not particle fields.

They must not be rendered as:

- rain,
- virga,
- probe dots,
- star dots,
- bacteria,
- scatter,
- or pixelated discovery particles.

Rain and virga are discrete-dot animation languages. Aspect-to-angle bands are smooth continuous intensity fields around exact centerlines.

The first design task is to define the band outline and boundary before color rendering. Only after the outer bounds and centerline are known should the band receive a smooth continuous color/intensity field.

Initial width tests should include primary aspect/orb caps such as:

- 10° each side,
- 8° each side,
- 6° each side,
- 3° each side.

The primary outer cap comes from the aspect/orb setting, with possible user override.

The narrow-space restraint is separate. The 30% adjacent-house/space cap is not the universal primary cap.

When an adjacent house/space is narrow, especially under about 30° or otherwise strongly unequal, cap that side so the band does not consume too much of the neighboring space. An experimental restraint may be:

- about 30% of the adjacent house/space width.

Do not treat the 30% cap as the universal primary cap. It is a restraint for narrow or unequal spaces.

Each side may be capped independently. Asymmetric left/right caps are allowed initially because they may be more truthful to the neighboring field geometry. Symmetric caps may be tested later only if truthful asymmetry proves too visually confusing.

Early experiments should avoid high-latitude and 65° complications. Solve ordinary cases first.

Centerline and edge rules:

- the centerline must not be white,
- the centerline should be the darkest or most opaque version of the selected color,
- outer edges must not fade to white,
- outer edges should fade to near-transparent versions of the selected color,
- no part of the band should turn white unless the selected color itself is white, which is not the normal case,
- the outer boundary must not look ragged, frayed, speckled, or broken,
- the outermost edge should be a continuous, uniform, extremely transparent version of the selected color,
- the next inward region should be smoothly and uniformly more visible,
- the gradient should remain smooth from edge to centerline,
- visible parallel stripe artifacts should be avoided.

Preferred construction:

1. define the outer bounds,
2. define the centerline,
3. render a smooth continuous gradient across the band.

Opacity and intensity should accelerate toward exactness. Static target tests should compare:

- linear ramps,
- logarithmic ramps,
- harmonic/overtone ramps,
- Fibonacci-like ramps.

The visual target is closer to a controlled Gaussian, logarithmic, or harmonic falloff than a feathered polygon edge or pixel field. A Gaussian-like curve may be acceptable if controlled and tuned to the desired harmonic, Fibonacci, or logarithmic acceleration.

The key requirement is continuous smooth concentration toward exactness. The opacity ramp may be mathematically generated, but the visible result should be smooth, proportional, premium, and map-readable.

Prior renders failed partly because the opaque center region was too broad and too fat. The strongest opacity should be concentrated at the exact centerline.

The adjacent band may retain a small amount of strong opacity depending on Fibonacci, harmonic, or logarithmic sequencing, but opacity should fall off quickly after the immediate center/core zone. Most of the band outside the tight center should be translucent to near-transparent.

Avoid broad "speedbump" opacity where the whole band feels similarly cloudy or heavy. The band should feel like a narrow exactness crest with smooth proportional falloff, not a wide opaque mound.

The outer edge remains a continuous, uniform, extremely faint version of the selected color, adjusting proportionally where the band narrows to accommodate small adjacent houses/spaces.

Stripe and banding constraints:

- do not create quasi-parallel line artifacts around the center,
- do not color degree-by-degree or half-degree-by-half-degree if that creates visible banding,
- prefer defining the outer bounds and centerline, then rendering a continuous gradient across the whole width,
- if internal "harmonic bands" are used conceptually, they should be visually blended into a smooth field, not obvious stripes.

Label readability:

- the middle core may obscure very small labels briefly or locally,
- outside the tight core, labels and city names should remain readable through the band,
- the band should imply intensity without behaving like an opaque cloud.

Before algorithmic implementation, create static target mockups for:

- 10° each side,
- 8° each side,
- 6° each side,
- 3° each side.

These mockups should show the finished smooth band target only. Do not combine bands with rain or virga in these mockups.

This is emotional implication and visual guidance, not the official measurement layer. Exact math belongs in popup/table detail.

---

## Rain Discovery Micro-Animations

Rain is for user-selected polygon/region conditions only.

Rain begins as a dense, subtle starry field of tiny uniform dots. Dots should be:

- small,
- refined,
- uniform,
- elegant.

Rain should not produce:

- blobs,
- twinkling,
- mechanical marching-soldier grids.

The animation should eventually resolve into a full translucent polygon. It should not remain scattered dots.

By the time rain completes, there should be no feathering anywhere. The final selected region should look crisp and neat like the original polygon overlay model. Every rendered subpixel/area should resolve cleanly as inside or outside the selected polygon/region.

Rain discovery may use dots during the animation, but the final state must not remain:

- dotted,
- fuzzy,
- feathered,
- or cloudy.

The final polygon should be a complete translucent filled region with crisp boundaries and map-readable opacity.

Border clustering and interior filling are separate micro-animations.

Border clustering is the computationally hard part:

- dots/bacteria cluster around true borders,
- border evidence tightens over passes,
- the final border should feel discovered, not stamped on.

Interior filling is more passive and economical once the border is approximately known:

- once the border is roughly known, the interior fills with small grey/white stars,
- those stars gradually saturate into the selected polygon color,
- the result resolves into the final translucent polygon state.

For the first target, border crisping and interior fill should coterminate: the sharp border and complete fill arrive together.

Later tests may allow the border to finish slightly before the interior if that feels more organic.

The color transition from grey/white stars into final polygon color may begin linear, but later tests should compare logarithmic and harmonic intensification so dots feel like they "find themselves" into the final color.

The animation may originally have been intended to buy time during brute-force calculation, but visual truth should not depend on incomplete computation. It may be more truthful and simpler if rain is driven from already-computed/cached Layer 1 truth data.

---

## Multiple Selected Regions

The user may select multiple regions or conditions.

Multiple selected regions should rain/fill roughly simultaneously, with slight organic timing variation across all selected regions.

Do not let multiple regions animate in robotic lockstep.

Design progression:

1. first solve one selected region,
2. then solve two selected regions,
3. then three,
4. then four,
5. then five and more.

Overlap rules remain a separate design protocol.

Candidate overlap treatments include:

- blended child colors,
- extremely subtle texture or crosshatching.

If texture/crosshatching or blended child colors become part of the final overlap language, rain discovery must eventually resolve into that final mixed/texture state too.

Texture must remain premium, subtle, and nearly unconscious. It must never become noisy.

---

## Virga Discovery

Virga uses the same visual grammar as rain but aborts early.

Virga is for unselected sibling conditions of the first selected variable only.

Examples:

- If `Sun in 1st` is selected, virga may imply `Sun in 2nd` through `Sun in 12th`, not all other planets.
- If `ASC in Aries` is selected, virga may imply `ASC in Taurus` through `ASC in Pisces`.

Virga behavior:

- perform only a few ghost discovery passes; exact pass count remains a design variable,
- treat "2-3 passes" as only a starting intuition, not a fixed rule,
- avoid robotic lockstep across sibling virga regions,
- vary timing, clustering, and fadeout with slight organic/random variation,
- cluster close enough to imply borders and pique curiosity,
- evaporate before crisp edges form,
- evaporate before filled interiors form,
- remain maximally subtle and charming.

Initial rule: suppress virga where it intersects or materially overlaps user-selected rendered polygons.

Future rule consideration: reduce or eliminate virga when many variables are selected, because the map may already be visually busy and the user is already exploring.

Virga may be more truthful and easier to choreograph from already-computed/cached Layer 1 truth data, especially when multiple selected variables create conflicts.

---

## Core Visual Doctrine

### 1. Aura should be built from a bounded field, not stripes

Aura should **not** be rendered as many visible striations or bands such as:

- one stripe per degree,
- multiple thin stepped lines,
- or obvious contour rings.

That would feel overly mechanical, cluttered, and visually distracting.

Instead:

- first determine the **outer bounds** of the aura,
- then render a **continuous field** inside those bounds,
- then apply a smooth intensity ramp toward the centerline.

In other words:

**define the aura region first, then fill it with a graded field.**

---

### 2. Aura width should be derived from orb, then capped

The overall width of the aura should be determined by the chosen or default orb logic.

This means the aura begins as a mathematically bounded field based on:

- aspect type,
- orb setting,
- and distance from exactness.

Typical default orb ideas discussed so far:

- conjunctions: up to about 10°
- trines and squares: about 8–10°
- sextiles: about 6°

But the raw orb width should not be allowed to dominate the map.

So aura width should then be capped by local geometry, such as:

- no more than about 30% of the relevant local house or field width,
- or another proportional cap that prevents narrow regions from being overwhelmed.

This preserves truth while protecting readability.

---

### 3. Aura should intensify toward the centerline

Each aura should have:

- a centerline of exactness,
- a bounded field around it,
- and a smooth intensification toward the centerline.

This creates the visual sense that:

- the whole aura region matters,
- but the exact line carries the most potency.

This is important because the visual message is not merely
“this condition exists here,”
but rather:

**“this condition becomes stronger as you approach exactness.”**

The user should be able to glance at the field and understand:

- the broader area of influence,
- and the most potent corridor within it.

---

### 4. Transparency is mandatory

Aura must remain visually permeable.

The map, labels, boundaries, and city context must remain readable underneath it.

Aura should never become a heavy opaque paint layer that hides:

- cities,
- coastlines,
- country context,
- or nearby overlapping conditions.

This means translucency is not optional.
Readability is a hard design requirement.

---

## Functional Product Role

Aura exists to add nuance inside already meaningful regions.

It provides a way to say:

- “this broader area is good,”
- “and this narrower part of it has extra concentration.”

This gives users a way to optimize within a positive field.

For example:

- a broad region may satisfy the desired placement,
- but cities near the aura centerline may provide slightly more strength or “extra credit.”

That is the practical value of aura.

It helps the user distinguish:

- valid space,
- stronger space,
- and strongest space,

without changing the underlying truth.

---

## Relationship to Broader Polygon Layers

Aura often sits on top of broader truth regions such as:

- planet in house,
- planet in sign,
- angle-related conditions,
- aspect-to-angle conditions.

That means the app may show:

- broad polygons,
- aura fields,
- and sometimes centerlines,
all at once.

This can become visually confusing, especially when many active layers overlap.

Therefore aura rendering must always be subordinate to overall readability.

---

## Overlap and Complexity Doctrine

### 1. Overlap is meaningful, but can become visually confusing

Sometimes aura fields may cross:

- MC-related fields crossing AC-related fields,
- overlapping angular fields,
- or multiple dense layers inside the same location.

This may not be common, but it will happen.

In these zones, raw stacking of multiple aura colors may create confusion.

---

### 2. Dense overlap may require automatic muting or simplification

When aura intersects:

- multiple polygon layers,
- multiple aura layers,
- or visually dense multi-condition zones,

the app may need to automatically reduce visual intensity.

Possible strategies:

- lower opacity,
- mute or desaturate the aura,
- reduce centerline prominence,
- compress the aura into a quieter shared visual state,
- or allow the overlap to resolve into a child color / blended state.

The goal is:

**not to let dense overlap become visual chaos.**

In especially crowded zones, the aura and even the centerline may need to diminish considerably so that the overlap becomes quieter and easier to parse.

---

### 3. Child-color logic may be useful

In overlap-heavy zones, instead of stacking bright competing colors, the system may eventually use:

- child colors,
- blended semantic colors,
- or a subdued shared color state.

This would allow the user to recognize:

- “multiple conditions are interacting here”
without forcing them to untangle loud competing layers at first glance.

This is still experimental and should be explored visually before implementation.

---

## Centerline Doctrine

The centerline is useful because it gives a visible spine of exactness.

However:

- it should not dominate the map,
- it should not become a harsh rigid engineering line unless needed,
- and in dense overlap zones it may need to fade or quiet down.

The ideal behavior is:

- centerline visible enough to orient the user,
- aura field visible enough to show potency around it,
- but both restrained enough to preserve map readability.

---

## What Aura Should Not Look Like

Aura should not look like:

- obvious contour stripes,
- heatmap sludge,
- heavy airbrushed fog,
- thick neon bands,
- opaque highlighter strokes,
- or arbitrary visual decoration disconnected from the truth model.

Human QA also rejects the current aura/progressive-reveal prototype visuals as implementation targets when they produce:

- frayed or noisy aura edges,
- insufficient opacity acceleration toward the centerline,
- too-uniform or speedbump-like aura intensity,
- mechanical, marching-soldier dot or raindrop patterns,
- dots that are too large, blobby, or visually heavy,
- grid-organized reveal patterns that feel engineered rather than organic.

It should feel:

- mathematically grounded,
- subtle,
- elegant,
- informative,
- and calm.

If raindrop or progressive reveal language is used, it should feel:

- subtle,
- small,
- refined,
- elegant,
- organic,
- and non-mechanical.

The current aura/progressive reveal output is not an approved implementation target.

---

## Approved Target Direction

Aura should be a bounded orb/intensity field, not a decorative texture or mechanical reveal pattern.

The approved target direction is:

- define the bounded aura region from orb/intensity logic,
- ramp opacity and intensity nonlinearly toward exactness and the centerline,
- make the centerline feel meaningfully intensified without making the map unreadable,
- keep edges soft, clean, and map-readable rather than noisy or frayed,
- keep any raindrop/progressive reveal treatment organic and refined rather than grid-like or mechanical,
- create one approved static aura target/mockup before further aura or renderer implementation.

---

## Current Design Priority

Before heavy production implementation,
we should first establish an approved visual concept.

That means:

1. create mockups,
2. create experiments with overlap cases,
3. test translucency against actual map readability,
4. test centerline prominence,
5. test child-color / muted-overlap possibilities,
6. and only then finalize implementation direction.

In other words:

**the visual concept should be approved before the full aura rendering system is deeply built out.**

---

## Correct Design and Build Order

The correct order is:

1. approve static aspect-to-angle band targets,
2. approve rain start frame and final polygon frame,
3. design rain in-between micro-animation stages,
4. handle rain with multiple selected regions,
5. design virga as aborted rain,
6. only then consider combining visual languages.

Do not combine visual languages prematurely.

Do not animate until the static aspect-band target and the rain start/final frames are approved. Animations should be derived backward from approved beginning and end states.

Do not keep experimenting with combined animations before the separate visual targets are approved.

---

## Recommended Mockup Set

Future visual exploration should include at least:

### Mockup A — Single clean aura
A single aura field inside a broad placement polygon, showing:
- broad region,
- centerline,
- smooth ramp toward exactness,
- and good map readability.

### Mockup B — Strong region with extra juice
A positive broad region such as Sun in the 1st house with a clear intensification corridor showing added potency.

### Mockup C — Two aura crossings
An example where two aura fields cross, testing:
- color interaction,
- centerline interaction,
- and whether the crossing is intelligible.

### Mockup D — Dense overlap zone
A deliberately complicated zone showing:
- multiple polygon layers,
- multiple aura layers,
- and a muted or child-color resolution strategy.

### Mockup E — Auto-muted dense state
A version where the system automatically quiets the aura in a visually dense zone.

### Mockup F — Solo / mute interaction view
A UI-state mockup showing how the same area looks when the user:
- solos a layer,
- mutes a layer,
- or reduces clutter manually.

---

## Product and UX Notes

Aura should support, not replace, exploratory map use.

The user workflow remains:

1. search broad desirable conditions,
2. inspect overlapping regions,
3. use aura to identify extra-strength corridors,
4. click cities for detailed truth inspection,
5. and compare specific locations more closely.

Aura is therefore a refinement aid, not the core truth layer.

---

## Governance Note

Aura must remain consistent with the deeper architecture:

- Layer 1: computes the objective truth geometry and exactness relationships.
- Layer 2: defines orb doctrine and interpretive defaults.
- Layer 3+: may decide which aura fields matter for a given search or user intention.

The renderer displays aura,
but aura must never smuggle interpretation into the truth layer.

---

## Current Open Questions

These are not yet resolved:

1. What exact intensity ramp looks best visually?
2. How strong should the centerline be relative to the field?
3. What opacity range preserves map readability best?
4. What child-color or overlap strategy is most legible?
5. When should auto-muting trigger?
6. Should aura become centerline-only in some high-density cases?
7. What visual relationship should aura have to NOT/exclusion overlays?
8. How should aura behave on mobile or small screens?

---

## Immediate Recommendation

Do not overbuild production aura rendering yet.

Next steps should be:

1. approve this doctrine,
2. create static visual mockups,
3. test overlap and readability concepts,
4. choose a preferred visual language,
5. then translate that into renderer rules.

The concept is clear.
The final look is not yet approved.

That approval should come before deeper implementation.

---

## Broader Visual System Context

This brief may later become part of a larger visual system covering:

- brand colors,
- typography,
- spacing,
- map base style,
- city labels,
- polygon overlay colors,
- overlap colors and textures,
- aspect bands,
- rain,
- virga,
- popup visual language,
- 2° house cusp gradient,
- greyscale popup notation for late-house planets,
- chart drawing style,
- professional/client export style,
- internal debug/diagnostic surfaces.

Internal debug/diagnostic surfaces are explicitly not commercial UI.
