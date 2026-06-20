# MAP-MOTION-0 — Object Persistence Animation Doctrine

**Date:** 2026-06-20  
**Status:** Canonical — all map animation work is bound by this document  
**Applies to:** `map_SANDBOX_genie_v7.html`, `map_CURRENT.html`, all future map UI work

---

## 1. Core Principle

**Animation exists to teach object permanence.**

Every animated transition in this interface is a lesson about where a tool lives. When the Genie panel closes, the user must understand that the panel became the bottle — not that the panel disappeared and a bottle coincidentally appeared. When the Save pill travels to become a disk, the user must watch a single pill physically transform into a disk. There is no acceptable shortcut.

---

## 2. The Morph Rule

Controls must **transform** into their future state. They must not **disappear and reappear**.

| Pattern | Classification | Verdict |
|---------|---------------|---------|
| Object A continuously changes position, size, opacity, and shape until it becomes Object B | Morph | ✓ Required |
| Object A fades out, then Object B fades in at a different position | Substitution | ✗ Forbidden |
| Object A fades out, then Object B appears immediately at its destination | Teleport | ✗ Forbidden |
| Object A shrinks to invisible, then Object B scales in from zero | Substitution | ✗ Forbidden |
| A ghost clone flies from A to B while A and B are hidden | Morph (if clone is continuously visible) | ✓ Acceptable |
| Ghost clone fades out before reaching destination, then B appears | Substitution disguised as morph | ✗ Forbidden |

---

## 3. The Object Continuity Test

Before shipping any animation, answer:

> **"Can I track this object with my eyes from beginning to end without losing it?"**

If the answer is no, the animation fails. Losing the object means:
- It became invisible at any point before the destination was reached
- A visually distinct new object appeared before the original had fully arrived
- The object teleported (position jumped discontinuously)
- A flash or repaint artifact occurred

---

## 4. The Single-Element Rule

Morphing animations must use **one element throughout** or **one ghost-clone** that is measured, moved, and morphed as a single unit.

Forbidden patterns:
- `innerHTML` replacement mid-animation
- `display:none` on element A before element B is fully opaque
- Any forced repaint between A's departure and B's arrival
- Two separately animated elements (A fading, B appearing) even when timed to overlap

Required pattern:
```
1. Measure A's bounding box
2. Measure B's bounding box (even if B is currently hidden)
3. Animate a single element (A itself, or a clone) from A's rect to B's rect
4. Keep that element fully opaque during travel
5. Only when it has ARRIVED at B's position may it fade and B reveal itself
6. If step 5 is needed, A and B must be coincident at that moment (pixel-level overlap)
   so the crossover is invisible
```

---

## 5. The No-Switcheroo Rule

**No innerHTML switcheroo.**

Changing an element's inner content mid-animation always produces a flash (a repaint frame where neither the old nor new content is rendered correctly). This is always forbidden during an active animation.

If an element must change its inner content as part of a morph, the new content must be present from the start of the animation and cross-faded in using opacity — so that at no frame is the element without visible content.

---

## 6. Human-Scale Timing

Animations must be slow enough for a human observer to follow. The test is: if you watch the animation once at normal speed, can you describe what happened?

| Duration | Assessment |
|---------|------------|
| < 200ms | Magic. User cannot track. Forbidden for teaching animations. |
| 200–500ms | Fast. Acceptable for minor state changes (button press feedback). |
| 500ms–1.5s | Standard. Acceptable for UI mode changes. |
| 1.5s–3.0s | Slow. Required for primary teaching animations (Genie↔bottle, Save pill). |
| > 3.0s | Very slow. Reserve for identity stamp watermark (background receding). |

Easing curves must feel **physical** (cubic-bezier with gradual acceleration and deceleration), not **magical** (linear, instant, or exponential snapping).

---

## 7. Acceleration Must Feel Natural

Cheap animations accelerate unnaturally — they start fast and snap to the end, or ease to a complete stop that feels rubber-band. Every animated element must feel like it has physical weight.

Required cubic-bezier family: `.4,0,.2,1` (standard material) or `.6,0,.15,1` (deliberate, weighted) for primary morphs. Never `ease-in` alone (objects don't teleport to their destination from nowhere) and never `linear` (objects don't move mechanically).

---

## 8. Animation as Teaching

Each animation teaches one fact. Document that fact:

| Animation | Lesson |
|-----------|--------|
| Genie panel → bottle | "Your search settings live inside that square icon" |
| Bottle → Genie panel | "That square was always the search builder, compressed" |
| Save pill → disk | "Save is still here — it moved to the map canvas" |
| Disk → pill | "The disk unfolds back into the save button" |
| Back/Fwd/Pin expanded → icon | "These are still here — compressed to icons" |
| Share pill → glyph | "Share is still here — smaller" |
| Nav → hamburger | "The navigation went into the ≡ icon" |
| Hamburger → nav | "The ≡ holds all navigation" |
| Notepad expanded → stub | "Your notes are still here — small" |
| Stub → icon (explore) | "Notes follow you into explore mode" |

If the animation cannot teach its lesson because the object disappears before arriving, it fails the test.

---

## 9. Staged Repair Plan

| Slice | Scope | Status |
|-------|-------|--------|
| MAP-MOTION-1 | Genie panel ↔ bottle | In progress |
| MAP-MOTION-2 | Save Search pill ↔ disk | Planned |
| MAP-MOTION-3 | Back/Forward/Pin + Share | Planned |
| MAP-MOTION-4 | Chrome/nav ↔ hamburger | Planned |
| MAP-MOTION-5 | Notepad states + storage wiring | Planned |

Each slice is implemented and validated before the next begins.

---

## 10. Acceptance Criteria Per Slice

Every MAP-MOTION slice is complete when:

1. The animated element (or ghost clone) remains **continuously opaque** from departure to arrival
2. No alternative element appears before the traveler has arrived and become coincident
3. No console errors during the animation
4. No `display` property changes during active animation (only `opacity` and `transform`)
5. A smoke test confirms bbox continuity at start, mid-point, and end
6. A human observer watching once can answer: "Where did the tool go?"
