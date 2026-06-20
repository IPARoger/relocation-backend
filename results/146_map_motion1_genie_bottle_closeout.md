# MAP-MOTION-1 — Genie ↔ Bottle Object Persistence Closeout

**Date:** 2026-06-20  
**Scope:** `map_SANDBOX_genie_v7.html` — Genie panel ↔ bottle FLIP animation only  
**Smoke:** `scripts/smoke_map_motion_object_persistence.py` — 21/21 PASS  
**Commit:** MAP-MOTION-1

---

## What Failed Before

### Root Cause 1 — Teleport (MAP-UX-5 implementation)

The prior implementation set `transition` and the destination `transform` in the **same `cssText` assignment**:

```javascript
builder.style.cssText = 'opacity:1; transition:transform 1.85s; transform:translate(tx,ty) scale(sc)';
```

The browser processes this as a single style flush. There is no "from" state to interpolate from — the element teleports to the destination immediately. The `transition` declaration is ignored because the browser never saw the element at its starting position before the destination was declared.

### Root Cause 2 — Substitution (not morph)

The old `@keyframes bottleIn { from{ opacity:0; transform:scale(.4); } }` fired when the `explore` class was added. The bottle appeared as an independent scale-in animation rather than as the resolved destination of the builder's journey. The builder faded to invisible before arriving; the bottle then appeared separately. The user saw two events, not one.

### Root Cause 3 — display:none gap

The bottle was `display:none` by default and `display:flex` via `body.explore .bottle`. The CSS `display` change caused a repaint/reflow at the moment `explore` was added, creating a flash frame. `getBoundingClientRect()` on a `display:none` element returns zeros, so the FLIP destination measurement was unreliable.

---

## Repair Strategy

### 1. Bottle always in DOM (no display change during animation)

```css
/* OLD — display switches cause reflow/flash */
.bottle { display:none; }
body.explore .bottle { display:flex; animation:bottleIn 1.0s ease both; }

/* NEW — always display:flex (position:fixed = no layout cost); only opacity changes */
.bottle { display:flex; opacity:0; pointer-events:none; }
.bottle--revealed { opacity:1; pointer-events:auto; }
```

The bottle's `getBoundingClientRect()` is now valid at all times, even before search.

### 2. Two-rAF pattern for correct FROM/TO interpolation

```javascript
// Step 1: establish FROM state (identity transform, no transition)
builder.style.cssText = [
    'opacity:1',
    'transform:translate(0,0) scale(1)',  // explicit FROM position
    'transition:none',                    // no transition during FROM setup
    'transform-origin:center',
    'will-change:transform'
].join(';');

// Step 2: two rAFs ensure browser has flushed FROM before declaring TO
requestAnimationFrame(function() { requestAnimationFrame(function() {
    builder.style.transition = 'transform 1.9s cubic-bezier(.6,0,.15,1)';
    builder.style.transform  = 'translate('+tx+'px,'+ty+'px) scale('+sc+')';
    // builder now animates from identity → destination, opaque throughout
}); });
```

Without both `requestAnimationFrame` calls, the browser batches FROM and TO into the same rendering frame and produces a teleport.

### 3. Builder remains opaque throughout journey

The CSS rule `body.explore .builder` now sets **only `pointer-events:none`** — not `opacity:0`. The JS `opacity:1` inline style established in Step 1 is never overridden by CSS during travel. The builder is fully visible from departure to arrival.

### 4. Bottle revealed only at arrival, with pixel-level coincidence

```javascript
setTimeout(function() {
    // At this moment: builder is at bottle's center, scaled to bottle's size.
    // Adding .bottle--revealed makes bottle visible exactly where builder is.
    bottle.classList.add('bottle--revealed');  // in-place reveal, no animation

    // 120ms micro-fade of builder — invisible because bottle covers it exactly.
    builder.style.transition = 'opacity 0.12s ease';
    builder.style.opacity = '0';
}, 1950);
```

The builder and bottle are pixel-coincident at the moment of crossover. The 120ms builder fade is invisible to the user.

### 5. Reverse path (toSetup) mirrors the same logic

```javascript
// Snap builder to bottle position (no transition = instantaneous FROM)
builder.style.cssText = [
    'opacity:1',
    'transform:translate('+tx+'px,'+ty+'px) scale('+sc+')',
    'transition:none', ...
].join(';');

// Bottle fades 120ms (coincident with builder, so invisible)
bottle.classList.remove('bottle--revealed');
bottle.style.cssText = 'transition:opacity 0.12s ease; opacity:0;';

// Two rAFs: expand builder back to natural size
requestAnimationFrame(function() { requestAnimationFrame(function() {
    builder.style.transition = 'transform 1.7s cubic-bezier(.2,0,.35,1)';
    builder.style.transform  = 'none';
}); });
```

---

## Why This Is Now Object-Continuous

The smoke test confirms continuity with measured bbox values:

| Checkpoint | Builder opacity | Builder transform | Bottle |
|------------|:--------------:|:-----------------:|--------|
| Pre-search | 1.0 | none (identity) | opacity:0 |
| 1s mid-travel | **1.0** | `translate(137px, -151px) scale(0.15)` | opacity:0 (not revealed) |
| 2.2s arrival | 0 (flip-hidden) | none (inline cleared) | opacity:1 at top:62 right:18 |
| 0.7s mid-reopen | **1.0** | `matrix(0.67, 0, 0, 0.67, 52.8, -58.4)` | not revealed |
| 2.1s post-reopen | 1.0 | none (cleared) | not revealed |

The builder's opacity is 1.0 at the 1-second mid-point: it has not disappeared, it is physically travelling. The bottle is not revealed until the builder has arrived. The reverse path shows the builder expanding through an intermediate matrix — continuous, measurable, no substitution.

---

## Smoke Test Results

**File:** `scripts/smoke_map_motion_object_persistence.py`  
**Run:** 21/21 PASS — 0 failures  
**Report:** `validation/reports/smoke_map_motion_object_persistence.json`

---

## What Remains Unfixed (Planned)

| Slice | Item | Status |
|-------|------|--------|
| MAP-MOTION-2 | Save Search pill ↔ disk | Planned |
| MAP-MOTION-3 | Back/Forward/Pin + Share | Planned |
| MAP-MOTION-4 | Chrome/nav ↔ hamburger | Planned |
| MAP-MOTION-5 | Notepad states + storage wiring | Planned |

These are not regressions — they were documented as FAIL/PARTIAL in the MAP-QA-1 animation doctrine audit (section 6, results/144_map_qa_pass1.md) before MAP-MOTION-1 work began. Each will be addressed in its own slice with its own smoke test.
