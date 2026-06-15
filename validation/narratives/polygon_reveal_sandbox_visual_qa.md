# Polygon Reveal Sandbox — Visual QA + Honest Self-Critique

> **STATUS: SUPERSEDED** (2026-05-21) — preserved as archaeology.
>
> **Why superseded:** Polygon *reveal pacing* was explored before brute-force
> screen-space truth was proven. Useful for emotional pacing lessons; not the
> production rendering substrate.
>
> **Current doctrine:** `docs/CURRENT_RENDERING_DOCTRINE.md` →
> `validation/narratives/brute_force_polygon_proof.md`

**Status:** Visual R&D evidence bundle (post–rendering language reset).
**Scope:** One polygon only — Sun in 1st house — for chart profile `baseline_validated`.
**Sandbox:** `map_SANDBOX_polygon_reveal.html` (not production, no commit, no replacement of `map_CURRENT.html`).
**Companion doctrine:** `docs/technical_philosophy/truth_field_rendering_path.md`, `docs/technical_philosophy/progressive_field_reveal.md`, `validation/narratives/truth_field_sandbox_visual_qa.md`.

This document exists so a human reviewer can answer the question the doctrine actually cares about: **does truthful, deterministic topology emergence feel right?** It is structured so the reviewer can inspect the evidence first and read the AI's interpretation second. AI claims about "feeling" are tagged so they can be discarded if they read as over-generous.

---

## 1. What this sandbox is and is not

| | |
|---|---|
| **Is** | A new sandbox for ONE polygon (Sun-in-1st) where points are revealed via stochastic exploratory probes, then progressively densified along match/non-match boundaries. |
| **Is not** | A scalar-field, aura, gradient, blur, glow, contour, quadtree-visible, or marching-squares overlay. There is no aspect line, no orb strength, no gaussian, no smoothing. |
| **Truth source** | `/classify-points` — for each (lat, lon) the engine computes `swe.houses` once and returns the integer house (1..12) of all 11 supported planets. The endpoint never invents, interpolates, deduplicates, or reorders. |
| **Pacing** | Real engine calls per phase. The only "added" cadence is per-probe CSS opacity transitions (600–700 ms) and a small inter-phase pause (120/350/900 ms by variant). |
| **Caching** | Every probe stores its full all-planets house map. Target swap (Sun-in-1st → Moon-in-4th) re-colors the existing field without a new engine call. |
| **Lat-cap honesty** | Points above ±65° (when `latCap=1`) come back with `outside_lat_cap: true` and are rendered as muted absence markers, not invented matches. |

The deliberate non-features matter as much as the features:
- no gradient fill,
- no aura halo,
- no boundary polyline drawn,
- no visible quadtree grid,
- no blur,
- no gamification of progress,
- no fake particles untied to engine probes.

---

## 2. Inspection map — direct links

Each URL is the exact form the capture harness used. They reproduce the still bundle frame-for-frame at the seed `42`.

| Pacing | Viewport | URL |
|---|---|---|
| Calm scatter | World | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=calm&viewport=world&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Cosmic bloom | World | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=bloom&viewport=world&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Eager reveal | World | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=eager&viewport=world&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Instant baseline | World | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=instant&viewport=world&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Cosmic bloom | Americas | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=bloom&viewport=americas&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Eager reveal | Eurasia (zero matches expected) | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=eager&viewport=eurasia&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Calm — halted after scatter | World | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=calm&viewport=world&stopAtPhase=0&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Calm — halted after refine 2/4 | World | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=calm&viewport=world&stopAtPhase=2&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Calm + cache swap → Moon-in-4th | World | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=calm&viewport=world&swapTo=moon:4&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |
| Lat-cap **off** | World | <http://127.0.0.1:8000/map_SANDBOX_polygon_reveal.html?pacing=eager&viewport=world&latCap=0&planet=sun&house=1&profile=baseline_validated&seed=42&auto=1> |

Server start (one-shot):

```bash
cd /Users/davegoodman/Desktop/relocation-backend
lsof -ti :8000 | xargs -r kill -9 2>/dev/null
./venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000
```

Regenerate the evidence bundle:

```bash
PLAYWRIGHT_BROWSERS_PATH=./venv/lib/python3.11/site-packages/playwright/driver/package/.local-browsers \
  ./venv/bin/python3 scripts/capture_polygon_reveal_sandbox.py
PLAYWRIGHT_BROWSERS_PATH=./venv/lib/python3.11/site-packages/playwright/driver/package/.local-browsers \
  ./venv/bin/python3 scripts/animate_polygon_reveal_sandbox.py
```

Output folder: `validation/screenshots/polygon_reveal_sandbox/`.

---

## 3. Stills bundle (10 PNGs)

All numbers below are read straight out of the engine's snapshot — no perceptual claim is implied.

| File | Probes | Matches | Non-matches | Above-cap | Engine calls | Notes |
|---|---:|---:|---:|---:|---:|---|
| `calm_final_world.png` | 526 | 232 | 284 | 10 | 5 | Calm at world, full reveal |
| `bloom_final_world.png` | 530 | 199 | 308 | 23 | 4 | Bloom at world, full reveal |
| `eager_final_world.png` | 836 | 257 | 537 | 42 | 4 | Eager at world, full reveal |
| `instant_final_world.png` | 600 | 32 | 469 | 99 | 1 | Sterile baseline — single uniform-random batch |
| `bloom_final_americas.png` | 682 | 312 | 370 | 0 | 4 | Bloom zoomed to band center |
| `eager_final_eurasia.png` | 280 | **0** | 276 | 4 | 1 | Truth at Eurasia: Sun-in-1st has no matches for this birth here. Refinement passes correctly produced zero new probes. |
| `calm_phase0_scatter_world.png` | 60 | 2 | 48 | 10 | 1 | Pure initial scatter — the "stars" state |
| `calm_phase2_refine_world.png` | 119 | 24 | 85 | 10 | 3 | Mid-refinement, polygon shape just becoming legible |
| `calm_cache_swap_to_moon4_world.png` | 526 | 10 | 506 | 10 | **5 (unchanged)** | Same probe field as `calm_final_world`, re-colored as Moon-in-4th from cache only |
| `latcap_off_world.png` | 836 | 257 | **538** | **0** | 4 | Same eager run with `latCap=0`. Capped band gets classified rather than refused; non-match count rises by exactly the number of formerly-capped probes. |

### What human QA should look for in the stills

1. `calm_phase0_scatter_world` — does the 60-probe scatter feel **star-like and exploratory**, or grid-jittered and "obvious random"?
2. `calm_phase2_refine_world` vs `calm_final_world` — is the polygon **emerging** between these two frames, or already "decided" by phase 2?
3. `instant_final_world` vs `bloom_final_world` — both have ~600 probes. Does the staged variant **read more like a polygon** than the uniform-random variant?
4. `calm_cache_swap_to_moon4_world` — does the cache flip make the philosophy concrete ("the world is already defined, you're asking it different questions"), or does the inherited Sun-in-1st boundary refinement leave a **visible scar** that the new overlay doesn't earn?
5. `eager_final_eurasia` — does the "**276 non-match dots and no matches**" picture read as honest absence, or as "broken"?
6. `latcap_off_world` vs `eager_final_world` — does the appearance of formerly-capped probes (now grey dots inside the polar belt) read as **cap policy made visible**, or as "now there are dots where there shouldn't be"?

---

## 4. Animated bundle (4 GIFs)

| File | Frames | ms/frame | What it shows |
|---|---:|---:|---|
| `calm_progression.gif` | 5 | 1400 | Scatter → refine 1 → refine 2 → refine 3 → refine 4. Probe counts: 60 → 80 → 119 → 367 → 526. |
| `bloom_progression.gif` | 4 | 1400 | Scatter → 3 refines. Probe counts: 140 → 180 → 270 → 530. |
| `eager_progression.gif` | 4 | 1400 | Scatter → 3 refines. Probe counts: 280 → 318 → 458 → 836. |
| `cache_swap_moon4.gif` | 2 | 2000 | Full calm reveal as Sun-in-1st, then the SAME probe field re-colored as Moon-in-4th from the in-page cache. Engine call count is **5 on both frames** — the swap is free. |

Per-frame stills are also written individually as `<gif_id>_frame_N.png` so a reviewer can scrub frame by frame instead of relying on GIF timing.

### What human QA should look for in the animations

1. In `calm_progression.gif`, between frame 0 and frame 1, does the refinement **cluster around the matches** or appear scattered? (The latter would mean boundary refinement isn't actually firing.)
2. In `eager_progression.gif`, frame 3 vs frame 4 — does the polygon **stop changing shape**? If yes, the engine has reached the visible truth before the variant's last pass.
3. In `cache_swap_moon4.gif`, between the two frames, do the **dot positions stay fixed** while only the colors change? (Positions must be identical — they ARE the same probes.)
4. In each progression GIF, is the inter-phase pause **enough** for the eye to register the previous state, or too short / too long?

---

## 5. Doctrine compliance check

| Rule | Status | Evidence |
|---|---|---|
| Every visible dot derives from a real `/classify-points` answer | ✅ | `__sandboxSnapshots` arrays show one classification per drawn probe; no probe is added except via `spawnProbe` then `classifyOne(result)`. |
| No blur, glow, scalar field, gradient, halo, contour smoothing | ✅ | Search the HTML for `blur`, `gaussian`, `gradient` — none present. Probes are SVG `<circle>` with CSS `fill-opacity` transitions only. |
| Pacing is intentional but truthful | ✅ | Each phase makes a real engine call; between-pass pause is the only "pacing" knob. Classify call counts match phase counts (1 + n_passes). Instant variant proves staging adds nothing to truth, only to perception. |
| Cache demonstrates "the world is already defined" | ✅ | `cache_swap_moon4.gif` shows classify-call count unchanged across the target swap (`classify_calls_unchanged_across_swap: true` in `animations_manifest.json`). |
| Lat-cap honesty | ✅ | `calm_final_world` shows 10 muted capped dots above ±65°; `latcap_off_world` shows 0 capped probes (formerly-capped probes are now real non-matches). The visible delta is exactly the cap policy. |
| No invented intermediate states | ✅ | Phases are real engine call boundaries. `stopAtPhase=N` halts the loop after phase N; the still at that boundary is what the engine actually returned. |

---

## 6. Honest self-critique

The biggest risk in this kind of work is that the AI describes its own output as "magical" because it built it. I am being deliberately skeptical here.

### 6.1 What seems to work

- **The cache swap is the strongest moment.** The same dots, two different geographies, zero new engine calls. It makes the philosophy ("the world is already defined; we're asking different questions") **literal** rather than rhetorical.
- **`calm_phase0` does read as star-like.** 60 sparse dots, two of them already gold, the rest grey-white. The eye reads it as "scattered probes, two hits." This is the closest the sandbox gets to "stars in the sky."
- **The polygon clearly emerges between phases 0 and 4 of the calm variant.** Probe count rises from 60 to 526; the gold cluster goes from two outliers to a coherent vertical band stretching from the Beaufort Sea down past the Galápagos. No polygon is ever drawn — the shape **is** the dots.
- **The lat-cap A/B is honest and intelligible** — formerly-capped dots become real classifications in `latcap_off_world` without any other visual change. The cap is visibly a *policy*, not a *limit of truth*.

### 6.2 What still looks artificial

- **Refinement is visibly algorithmic in the GIFs.** Each refine pass clearly adds dots *along the existing match boundary*. The user asked for "not visibly algorithmic"; we're not quite there. The midpoint-jitter scatter softens it but doesn't hide it. *Possible next move:* make refinement spawn probes in a **shell** around each match (Poisson-disk-ish) rather than at match/non-match midpoints, so the eye doesn't trace the algorithm.
- **The cache-swap frame has a "ghost cluster."** Because the probe field was densified for Sun-in-1st, the central-Pacific area is dense in probes (now all grey because they're not Moon-in-4th matches). The Moon-in-4th gold dots are sparse and don't enjoy the boundary refinement they would have gotten if Moon-in-4th had been the original target. This is *honest* (the cache is honest about which target was discovered first) but emotionally it weakens the "geography has already been revealed" message — a reviewer might read it as "the swap didn't really save us anything." *Possible next move:* either (a) refine boundaries for *all* targets opportunistically during idle, or (b) accept that the first reveal earns the most boundary refinement and document this.

### 6.3 What feels too abrupt

- **The "instant" baseline.** 600 random probes, 32 matches, polygon barely legible. The user predicted this would feel emotionally sterile, and it does. Useful only as a reference point that proves staging adds value beyond truth.
- **Eager pacing (120 ms between passes).** Still slow enough that you see the staging, but only barely. At the edge of "snap" rather than "discovery."

### 6.4 What feels too noisy

- **Non-match dots at 0.42 opacity** are now visible enough that the world view of bloom/eager has a noticeable grey background scatter. This was a deliberate response to an earlier draft where non-matches were invisible (0.20), which made the scatter unreadable. The current setting is a tradeoff: more legibility, slightly busier image. The slider could go either way.
- **The metrics panel** is essential for QA but reads as "instrument." Fine in this sandbox, but a default product mode would hide it.

### 6.5 What feels too computational

- **The top banner** (`scatter · sun in 1st · 60 probes (2 match)`) is currently always visible during runs. It is informative but it *is* "loading theater" — exactly what the user said the reveal should not be. *Possible next move:* hide the banner by default; expose only via `?showStatus=1`.
- **The variant-pacing dropdown in the panel** trains the reviewer to think of this as a "demo of pacing options" rather than as a single deliberate reveal. For productisation this UI would shrink to nothing.

### 6.6 Where the AI may be over-generous

I claim above that the cache swap is the "strongest moment." A skeptical reading: the cache swap is only strong **if the reviewer cares that the engine call count stayed at 5.** A casual viewer of the GIF without the metric overlay might just see "Sun dots disappeared, fewer Moon dots appeared in different places" and not perceive any cache magic at all. The strength of the moment requires the metrics caption. That's an *epistemic* strength, not a *visual* one. We should not over-credit visuals for something that needs a caption to land.

Similarly, I claim phase 0 "reads as star-like." But at the 1024×768 PNG resolution the 60 dots are objectively small grey points on a dark map. Whether that reads as "stars" or as "barely there" is taste-dependent. A reviewer who expected a cosmological feel might find the result subtler than they hoped — closer to "you can see we sampled here, if you squint" than to "the night sky."

### 6.7 Pacing variant judgment

If forced to pick one to take forward:

- **Calm** is the closest to the user's stated tone ("almost accidental, understated, inevitable"). Long inter-phase dwell creates space. Trade-off: 4–5 second total reveal may feel long in product.
- **Bloom** is the most defensible default. Quick enough to not feel like "loading theater," slow enough that the polygon's emergence is visible. The geometry of the polygon is also more legible at 530 probes than at 60.
- **Eager** is the closest to "production feel" but the user explicitly warned against optimizing too early. Worth keeping as a calibration point, not a default.
- **Instant** is the negative control. Keep it as proof that staging matters.

### 6.8 Open questions for the next pass (not actioned here)

1. Should refinement spawn probes in a **shell** around each match instead of at boundary midpoints? Tested intuition: yes, would feel less algorithmic. Untested.
2. Should the cache pre-warm **other** classifications during initial scatter — i.e., classify each probe's all-11-planet house map (already returned) and store, but ALSO spawn boundary probes for the user's "likely next" target? This is closer to the user's "while showing Sun in 1st, opportunistically compute neighbors" prompt. Currently the cache covers *coloring*, not *boundary refinement*, for non-active targets.
3. Should non-match probes **fade out over time** once they've been used to establish a boundary? Doctrinally this is fine (no truth is being hidden, just visibility), but it crosses into "cosmetic" territory that the doctrine explicitly suspects.
4. Should we cap probe count per phase by **viewport** rather than absolute count? At Eurasia zoom the eager variant returned zero matches and stopped — fine, but at world zoom the same variant generated 836 probes which is denser than necessary.

---

## 7. Files in this evidence bundle

```
validation/screenshots/polygon_reveal_sandbox/
├── manifest.json                              ← stills capture manifest
├── animations_manifest.json                   ← GIF capture manifest
├── calm_final_world.png
├── bloom_final_world.png
├── eager_final_world.png
├── instant_final_world.png
├── bloom_final_americas.png
├── eager_final_eurasia.png
├── calm_phase0_scatter_world.png
├── calm_phase2_refine_world.png
├── calm_cache_swap_to_moon4_world.png
├── latcap_off_world.png
├── calm_progression.gif        (+ 5 frame PNGs)
├── bloom_progression.gif       (+ 4 frame PNGs)
├── eager_progression.gif       (+ 4 frame PNGs)
└── cache_swap_moon4.gif        (+ 2 frame PNGs)
```

Source files touched (no production paths altered):

```
main_centerline_FIXER.py                       (added /classify-points + sandbox route)
map_SANDBOX_polygon_reveal.html                (new)
scripts/capture_polygon_reveal_sandbox.py      (new)
scripts/animate_polygon_reveal_sandbox.py      (new)
validation/narratives/polygon_reveal_sandbox_visual_qa.md  (this file)
```

No commits, no replacement of `map_CURRENT.html`, no change to existing rendering paths.
