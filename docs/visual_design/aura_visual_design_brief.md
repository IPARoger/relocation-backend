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

It should feel:

- mathematically grounded,
- subtle,
- elegant,
- informative,
- and calm.

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
