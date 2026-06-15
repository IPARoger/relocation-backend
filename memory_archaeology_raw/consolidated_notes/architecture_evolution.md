# Architecture Evolution (From Archaeology)

This section tracks **how the system was understood to work over time**, including pivots and corrections. It deliberately preserves **tensions** where archaeology disagrees with current code reality—those belong in open questions, not silent deletion.

---

## Phase A — Contour / bitmask era (early breakthrough framing)

**What archaeology claims happened**

- House regions were understood as: **grid sampling → binary mask per condition → contour extraction → GeoJSON → frontend opacity blending**.
- Frontend **natural transparency** was often preferred over precomputed “overlap polygons” for A/B/C because hard overlap patches looked worse than blended overlays.
- DeepSeek-era notes include ** bitmask debug counts** (`np.unique`) as a paradigm: absence of a pure “C only” region may be **geometry**, not “broken logic.”

**Why it mattered**

- Shifted debugging from “eyeball the map” toward **classification truth** on a grid.

**Tension / evolution**

- Contour extraction introduced **topology artifacts** (double lines, seams, merges). Later work treated contours as risky for *centerline truth* in some contexts.

---

## Phase B — “Brute-force truth maps” as an independent arbiter

**What archaeology claims happened**

- A separate dense validator exports GeoJSON truth (e.g. aspect families) for comparison in `geojson.io` against app lines.
- Major methodological breakthrough: **separate astrology correctness from renderer/contour correctness**.
- Validator philosophy moved from razor-thin zero-crossings toward **orb-corridor truth** (`abs(shortest_angle_difference) <= orb`) as closer to astrological practice.

**Why it mattered**

- Turned “looks wrong” into **comparable evidence**.

**Artifacts called out in archaeology**

- `all_aspects_truth.geojson`, `brute_force_validator.py`, warnings about validating **square Alaska** with **square truth**, not trine truth.

---

## Phase C — Angular overlays: centerline vs aura separation

**What archaeology claims happened**

- Painful iterations around ASC/MC aspect lines led to a durable principle: **backend emits exact centerlines**; **frontend renders aura/glow** for orb feel.
- Rejected: Gaussian blur / orb-fields computed as “ astronomy,” when blur **moves** perceived lines and creates false connections.
- Progressive rendering appears repeatedly: coarse → fine, “like a loading image.” **Implemented later in product** for staged ASC (per current codebase milestone).

**Why it mattered**

- Prevented “make it pretty” from silently becoming “make it false.”

---

## Phase D — Truth-grid / sampling pivot for house regions (product milestone)

**What archaeology + current repo state align on**

- For **binary house membership**, a **truth-sampling / truth-grid** approach became the canonical direction to avoid seam/topology lying—while keeping contour mode as fallback.

**Why it mattered**

- Preserves **membership semantics** when contour closure and dateline wrapping are painful.

---

## Phase E — Canonical vs display geometry (seam and dateline)

**What archaeology claims happened**

- A **failed seam-aware closure** attempt corrupted topology (houses collapsing, wrong identities), proving that **closing polygons along map window edges** is the wrong layer.
- Preferred direction: keep canonical features, adapt for display (fragments, world copies), **preserve feature identity**.

**Why it mattered**

- Codified a strict architectural boundary: **never buy cosmetic continuity with semantic lies**.

---

## Recurring engineering hazards (institutional warnings)

- **Multiple “main” files / wrong module running:** `main_centerline_FIXER.py` vs `main.py`, plus HTML variants—many regressions were “wrong runtime,” not math.
- **Indentation / herodoc / giant paste corruption:** long threads identify paste workflows as a **systemic risk**.
- **Cross-contamination between engines:** ASC grid variables accidentally used in house loops—**modular boundaries** are not optional nice-to-haves.

---

## Contradictions / evolution the team must not flatten

| Topic | Archaeology contains… | Current handling |
|------|------------------------|------------------|
| Latitude caps | ASC ±60 vs houses ±65 vs grid -60..86 vs marketing framing “inhabited Earth” | Must be documented as **product policy**, not assumed |
| MC geometry language | Some threads emphasize RA/sidereal framing; others insist relocated chart ecliptic MC for product semantics | Needs a single `docs/calculation_assumptions.md` source of truth |
| Validator role | Sometimes “temporary tool,” sometimes “permanent referee” | Decide explicitly: **tooling vs CI vs regression artifact** |

---

## Weak / incomplete archaeology inputs

- `chat_07_additional_archaeology_and_overflow.md` is mostly a **stress-fixture combined extraction/audit prompt** and rename instructions—it **indexes** topics (truth_grid, staged ASC, reviewer, memory architecture) more than it **records** full thread prose. Treat as procedural metadata + checklist, not a second full dump of `chat_02`/`chat_06`.
- `current_chat_truth_grid_memory_and_infrastructure.md` (re-checked 2026-05) is still an **empty intake placeholder** in this repo; **lack of paste there does not by itself mean a knowledge gap** if consolidation drew from numbered chats.
- DeepSeek extracts include **specific commit hashes** and monetization tiers that may be **historical** or speculative—treat as **signals**, not current repo law without verification.
