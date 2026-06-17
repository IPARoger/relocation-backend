# Plate & Wheel Geometry Exploration — Phase 3.0A

Status: visual arrangement exploration (geometry only)
Type: where information physically lives around the wheel
Constraint: no implementation, no production UI, no CSS, no color, no typography,
no atmosphere, no texture, no glow. **Ignore all styling.** Focus only on
geometry, hierarchy, placement, and information grouping. No mockups, no final
decision.

Purpose: doctrine is complete; now determine *where information physically lives*
around the wheel. The wheel is the primary object. The question: how to arrange
profile authority, chart identity, location context, and metadata **without
crowding the wheel.**

Surfaces explored: Profile, Relocated Location, Comparison. (Map, City
Intelligence, Notes-page deliberately ignored.)

Vocabulary used throughout:
- **Wheel** — the chart object (primary).
- **Authority block** — profile selector, birth name, birth date, birth time,
  birth city.
- **Context block** — chart context label (Natal / Current / Relocated), city
  name, lat/lon, UTC, Tropical, Placidus.
- **Metadata** — the technical/system facts within the context block that may stay,
  collapse, or move.

Positions are described relationally (above / beside / below / corner / inline),
never in measurements.

---

## TASK 1 + TASK 2 — Ten competing arrangements per page

Each arrangement names a geometry and specifies Wheel / Authority / Context /
Metadata placement and behavior.

### PROFILE PAGE

**P1. Corner Plate.**
- *Wheel:* center, heavily dominant, owns the page's middle.
- *Authority:* compact block in upper-left corner.
- *Context:* small line under the authority corner (Natal default).
- *Metadata:* lat/lon, UTC, systems collapse into a disclosed line; only name +
  birth essentials stay visible.

**P2. Split Plate.** (see Task 3 for deep dive)
- *Wheel:* center, dominant.
- *Authority:* upper-left (name, birth triad, selector).
- *Context:* lower-left (context label, city, lat/lon, UTC, Tropical, Placidus).
- *Metadata:* identity stays upper; technical/system grouped lower; nothing
  crosses the wheel.

**P3. Banner Plate.**
- *Wheel:* center but pushed down by a full-width header band.
- *Authority:* spread across the top banner.
- *Context:* right end of the banner.
- *Metadata:* inline in banner; risk of horizontal crowding. Wheel sits lower.

**P4. Wheel Anchor.**
- *Wheel:* center and largest possible; everything else orbits at a respectful
  remove.
- *Authority:* a single quiet line above the wheel.
- *Context:* a single quiet line below the wheel.
- *Metadata:* almost all collapsed/disclosed; maximal wheel room.

**P5. Side Ledger.**
- *Wheel:* center-left, dominant but shifted to give a right column.
- *Authority:* top of the right column.
- *Context:* beneath authority in the same column.
- *Metadata:* listed in the right ledger, always visible; reference tables below.

**P6. Stacked Title.**
- *Wheel:* center, dominant.
- *Authority:* a titlepage stack directly above the wheel (name large, birth triad
  beneath).
- *Context:* a subtitle line within the same stack.
- *Metadata:* colophon line at the very bottom of the page.

**P7. Twin Corners.**
- *Wheel:* center, dominant.
- *Authority:* upper-left corner.
- *Context:* upper-right corner (balanced).
- *Metadata:* split between corners; risk of the eye ping-ponging.

**P8. Lower Context.**
- *Wheel:* center, dominant.
- *Authority:* above the wheel (compact).
- *Context:* entirely below the wheel, ahead of the tables.
- *Metadata:* with the lower context; identity up, everything else down.

**P9. Floating Authority.**
- *Wheel:* center, dominant; authority overlaps the wheel's outer margin as a
  light corner inset.
- *Authority:* floating top-left over the wheel's negative space.
- *Context:* floating bottom-left similarly.
- *Metadata:* collapsed; only essentials float. (Risk: encroaches on wheel.)

**P10. Reading Column.**
- *Wheel:* centered at the top of a single narrow reading column; dominant within
  the column's width.
- *Authority:* title above the wheel.
- *Context:* line below the wheel.
- *Metadata:* flows further down the single column as a quiet block.

---

### RELOCATED LOCATION PAGE

**R1. Location Banner / Profile Lens.**
- *Wheel:* center, dominant but below a location-subject header.
- *Authority:* profile lens as a subtitle in the header ("for {profile}") +
  selector.
- *Context:* location name leads the header; lat/lon, UTC, systems beneath.
- *Metadata:* technical collapses below; city name stays prominent.

**R2. Split Plate (Relocated variant).**
- *Wheel:* center, dominant.
- *Authority:* upper-left (profile lens + selector, smaller than Profile page).
- *Context:* lower-left (Relocated label, city, lat/lon, UTC, systems).
- *Metadata:* grouped lower-left; city named without heavy badge.

**R3. Guest Corner.**
- *Wheel:* center, dominant (guest, slightly smaller).
- *Authority:* profile lens compact in upper-left corner.
- *Context:* location block in upper-right corner.
- *Metadata:* collapsed; only city + essentials visible.

**R4. Subject Title / Lens Footer.**
- *Wheel:* center, dominant.
- *Authority:* profile lens line *below* the wheel (deliberately subordinate
  position) yet always present.
- *Context:* location title *above* the wheel (subject leads).
- *Metadata:* with the lower lens line + collapsed technical.

**R5. Dual Context (Natal ghost).**
- *Wheel:* relocated center, dominant; a small natal reference at a remove.
- *Authority:* upper-left, owning both charts.
- *Context:* location block beside the relocated wheel.
- *Metadata:* minimal; comparison-of-self implied geometrically.

**R6. Lower Location.**
- *Wheel:* center, dominant.
- *Authority:* above the wheel (profile lens prominent).
- *Context:* location + metadata entirely below the wheel.
- *Metadata:* below; keeps authority above as the senior position.

**R7. Side Place Ledger.**
- *Wheel:* center-left, dominant.
- *Authority:* top of right column.
- *Context:* location facts fill the right ledger.
- *Metadata:* always-visible right column; city intel teaser at its foot.

**R8. Threshold Stack.**
- *Wheel:* center, dominant, framed as a "door."
- *Authority:* profile lens stacked above the wheel.
- *Context:* location name as the wheel's caption directly beneath.
- *Metadata:* colophon at page foot.

**R9. Balanced Twins (profile senior).**
- *Wheel:* center, dominant.
- *Authority:* upper-left, visually senior.
- *Context:* upper-right, visually junior (location).
- *Metadata:* split but weighted so authority reads first.

**R10. Quiet Relocation.**
- *Wheel:* center, dominant; geometry nearly identical to Profile's chosen plate.
- *Authority:* same position as Profile (consistency), profile lens.
- *Context:* location named in the context slot Profile uses for Natal/Current.
- *Metadata:* same grouping as Profile; only the *content* differs, not the
  geometry. (Maximal family resemblance.)

---

### COMPARISON PAGE

**C1. Sticky City Bar / Single Authority Band.**
- *Wheel:* small per-city wheels optional, or none; the matrix is the center.
- *Authority:* one profile band across the top (governs all columns).
- *Context:* city identities in a sticky bar above the matrix columns.
- *Metadata:* per-city coords/systems collapse into the city bar on disclosure.

**C2. Column Headers as Plates.**
- *Wheel:* none or tiny; matrix-centric.
- *Authority:* single profile band, page top.
- *Context:* each column topped by a compact city plate (name + coords).
- *Metadata:* minimal in header; systems shared once at the profile band.

**C3. Observatory Comparison.**
- *Wheel:* a small wheel per city above its column, kept central-per-column.
- *Authority:* single profile band above all.
- *Context:* city name caption under each mini-wheel.
- *Metadata:* collapsed; coords on disclosure.

**C4. Frozen Label Column.**
- *Wheel:* none; pure matrix.
- *Authority:* profile band top.
- *Context:* cities across the top; a frozen left label column names the rows.
- *Metadata:* in expandable sections, not column headers.

**C5. Stacked Cities (vertical).**
- *Wheel:* optional small wheel per city.
- *Authority:* profile band top.
- *Context:* each city a stacked block (not side-by-side), reducing width.
- *Metadata:* within each city block, collapsible.

**C6. Spotlight Pair.**
- *Wheel:* two wheels for the focused pair; others parked as slim tabs.
- *Authority:* profile band top.
- *Context:* full plates for the two focused cities only.
- *Metadata:* full for the pair, hidden for parked cities.

**C7. Shared-System Footer.**
- *Wheel:* none/tiny.
- *Authority:* profile band top; Tropical/Placidus stated once.
- *Context:* city names in sticky bar.
- *Metadata:* systems removed from every column and stated once globally (width
  saver).

**C8. Card Deck.**
- *Wheel:* per-card optional.
- *Authority:* profile band top.
- *Context:* each city a card flipped through; only a few visible.
- *Metadata:* on card; width controlled by showing fewer cities at once.

**C9. Twin-Column Matrix.**
- *Wheel:* none.
- *Authority:* profile band top.
- *Context:* cities paired two-at-a-time within a fixed width; cycle for more.
- *Metadata:* per pair, collapsible.

**C10. Atlas Spread.**
- *Wheel:* none/tiny.
- *Authority:* profile band top.
- *Context:* cities as atlas entries with names as headers and facts as margins.
- *Metadata:* in the margins, browsable, not all expanded.

---

## TASK 3 — Deep dive: the Split Plate

Geometry: **Authority upper-left** (name, birth date, birth time, birth city,
profile selector); **Context lower-left** (Natal/Current/Relocated label, city
name, lat/lon, UTC, Tropical, Placidus); **wheel center**, uncrossed.

**Strengths (geometric):**
- *Clean epistemic separation* — identity (who) physically held apart from context
  (what/where/system), matching the Badge & Metadata doctrine's grouping without a
  single styling decision.
- *Wheel uncrossed* — both blocks live to one side, so the wheel keeps the center
  and its quiet; nothing spans across it.
- *Stable scan path* — eye reads authority → context → wheel in a consistent
  top-to-bottom-left arc; learnable once, reusable on Relocated.
- *Vertical economy* — stacking the two blocks in one column avoids a wide banner
  and keeps the wheel from being pushed down.
- *Family resemblance* — the same two-block geometry transfers directly to the
  Relocated page (only content changes), strengthening the organism.

**Weaknesses (geometric):**
- *Left-heavy imbalance* — all information on one side can leave the opposite side
  empty and the composition lopsided, making the wheel feel off-center even when
  centered.
- *Vertical pressure* — two stacked blocks can grow tall enough to push the wheel
  down or misalign with its vertical center, especially with long names.
- *Corner competition* — two blocks in one column can read as one heavy mass that
  competes with the wheel for first attention.
- *Long-name strain* — birth city + city name + coords stacked can force wrapping
  that disturbs the block's rhythm and the wheel's alignment.
- *Context overload risk* — lower-left holds six items (label, city, lat/lon, UTC,
  Tropical, Placidus); without disclosure it can become a dense mass.

**Conclusion (no winner):** the Split Plate is *structurally sound* and a strong
family-resemblance carrier, but its risks are **balance and verticality**. It
should be tested against arrangements that distribute weight (Twin Corners) or that
move context below the wheel (Lower Context) before it is assumed to win.

---

## TASK 4 — Wheel protection audit

For each arrangement: does the wheel stay centered, get pushed down, lose
authority, or become stranded?

| Arrangement | Centered? | Pushed down? | Loses authority? | Stranded? |
|---|---|---|---|---|
| P1 Corner Plate | Yes | No | No | No |
| P2 Split Plate | Yes | Slight risk | No | Mild (left-heavy) |
| P3 Banner Plate | Lowered | **Yes** | Risk | No |
| P4 Wheel Anchor | Yes | No | No | **Risk (over-isolated)** |
| P5 Side Ledger | Shifted | No | Mild | No |
| P6 Stacked Title | Yes | Slight | No | No |
| P7 Twin Corners | Yes | No | No | No |
| P8 Lower Context | Yes | No | No | No |
| P9 Floating Authority | Yes | No | **Risk (encroachment)** | No |
| P10 Reading Column | Yes (narrow) | Slight | Mild | No |
| R1 Location Banner | Lowered | **Yes** | **Risk (location over-leads)** | No |
| R2 Split (Reloc) | Yes | Slight | No | Mild |
| R3 Guest Corner | Yes | No | No | No |
| R4 Subject Title/Lens Footer | Yes | No | Risk (lens demoted) | No |
| R5 Dual Context | Yes | No | No | Mild |
| R6 Lower Location | Yes | No | No | No |
| R7 Side Place Ledger | Shifted | No | Mild | No |
| R8 Threshold Stack | Yes | Slight | No | No |
| R9 Balanced Twins | Yes | No | No | No |
| R10 Quiet Relocation | Yes | Slight | No | Mild |
| C1–C10 (matrix-centric) | N/A (wheel small/absent) | — | Wheel not the center by design | — |

Key protections observed: corner and lower-context geometries protect the wheel
best; **banner geometries push it down**; **floating geometries risk
encroachment**; **wheel-anchor risks stranding** (the over-isolation failure from
the Spatial doctrine). On Comparison the wheel is *intentionally* not the center —
the matrix is — so wheel-protection rules transfer as "protect the matrix's
legibility" instead.

---

## TASK 5 — Profile: can Notes occupy excess A2A space without damaging hierarchy?

The A2A table can leave vertical/horizontal slack (especially in single-chart
mode). Alternatives for using it with Notes:

- **N1. Adjacent Margin.** Notes occupy the slack *beside* A2A as a margin, clearly
  downstream of the wheel and tables. *Hierarchy:* safe if notes read as peripheral.
- **N2. Below-Tables Footer.** Notes fill space *beneath* the reference row, after
  all tables. *Hierarchy:* safest; notes are last in the reading order.
- **N3. Filled Reserve.** Notes take the literal empty cell A2A doesn't use.
  *Hierarchy:* risk — if notes sit *inside* the table region they may read as
  table-level, violating the entity-notes doctrine geometrically.
- **N4. Disclosed Drawer.** Notes live collapsed in the slack, opened on invite.
  *Hierarchy:* safe; absent until wanted.
- **N5. Companion Column.** A persistent slim notes column parallel to the tables.
  *Hierarchy:* safe if it never outweighs the wheel or the tables.

Geometric rule surfaced: **Notes may use A2A's excess space only while remaining
*after* the wheel and *outside* the table's own bounds** — filling slack is fine;
occupying the table's interior is not (it would imply row/section notes). Below or
beside, never within.

---

## TASK 6 — Relocated: location important but not more authoritative than profile

Alternatives for making location prominent while keeping profile the authority,
*geometrically*:

- **L1. Subject-above / Authority-persistent.** Location leads as the page's top
  subject, but the profile lens sits in the same fixed authority slot used on the
  Profile page, so authority is *positionally* preserved even as location leads in
  reading order.
- **L2. Size-by-role.** Location named at headline prominence, profile lens smaller
  but *closer to the wheel* — proximity to the instrument encodes authority while
  size encodes subject.
- **L3. Authority-anchored, Subject-orbiting.** Profile occupies the stable anchor
  position near the wheel; location occupies a more peripheral but larger block —
  authority is central, subject is prominent.
- **L4. Sequence split.** Location first in reading sequence (subject), profile last
  but in the senior/anchor position (authority) — order ≠ authority.
- **L5. Shared slot, content swap.** Use Profile's exact geometry (Quiet
  Relocation); location simply fills the context slot. Authority stays where the
  user already learned it lives.

Geometric principle surfaced: **subject and authority can be separated by
*position vs prominence*** — let location win *size and reading-order* while profile
wins *proximity to the wheel and the stable anchor slot*. The lens never leaves the
neighborhood of the chart it governs.

---

## TASK 7 — Comparison: city identity visible without excessive horizontal width

Alternatives that keep cities identifiable while controlling width:

- **W1. Sticky compact city bar** — names + minimal coords only at the top; details
  on disclosure (width = names, not full plates).
- **W2. Vertical stacking** — cities stacked rather than side-by-side; trades width
  for height.
- **W3. Fewer-at-once** — spotlight pair / card deck shows 2–3 cities fully; cycle
  for the rest.
- **W4. Shared-system extraction** — Tropical/Placidus (identical across cities)
  stated once globally, removed from every column (real width saved).
- **W5. Frozen label column + scroll** — row labels frozen left; city columns scroll
  horizontally without the page itself widening.
- **W6. Truncate-to-disclose** — long city/admin names shown compact with full form
  on invite (geometry note only; not a truncation *rule*).
- **W7. Atlas margins** — city facts as margin notes around named entries rather
  than as ever-widening columns.

Geometric principle surfaced: **width is spent on *identity and values*, never on
repeated system metadata or fully-expanded detail** — shared facts go global,
detail goes behind disclosure, and quantity-of-cities is managed by stacking or
spotlighting rather than infinite horizontal growth.

---

## TASK 8 — Arrangements That Sound Good But Fail

Named failure geometries (generated):

- **Wheel Exile.** Wheel moved off-center to make room for information; the genetic
  center is lost and the page becomes a data panel with a chart attached. (Banner
  and aggressive Side-Ledger geometries tend here.)
- **Metadata Sprawl.** Lat/lon, UTC, systems all kept always-visible and spread
  across the plate; the wheel is nibbled by a field of small facts. (Fails the
  "reference earns sufficiency, not room" rule.)
- **Authority Dilution.** Profile authority split across multiple positions or
  demoted below location/context so the lens stops feeling governing. (R4's footer-
  lens, pushed too far; Twin geometries that balance authority into invisibility.)
- **Banner Overload.** A full-width header carrying authority + context + metadata
  pushes the wheel down and crowds the top; first attention lands on a dense band,
  not the chart.
- **Corner Cram.** Two heavy blocks jammed into one corner read as a single mass
  competing with the wheel (Split Plate's worst case if undisciplined).
- **Floating Encroachment.** "Space-saving" floating blocks overlap the wheel's
  margin and steal its quiet (P9 pushed too far).
- **Wheel Marooned.** Over-isolating the wheel for reverence until it floats
  disconnected from the tables that depend on it (P4 pushed too far) — the
  stranding failure.
- **Column Inflation.** Comparison columns carrying full plates + full metadata
  each, widening the page until comparison becomes endurance.
- **Symmetry Trap.** Forcing authority and context into mirrored corners for visual
  balance, making the eye ping-pong and obscuring which block is senior.
- **Context Avalanche.** Lower-context geometry that dumps all six context+metadata
  items below the wheel with no disclosure, burying the tables under facts.

Common geometric root: **every failure either crosses/crowds/displaces the wheel,
or flattens the authority→context→metadata hierarchy into an undifferentiated
mass.** Good geometry protects the center and preserves the descending order.

---

## TASK 9 — The five most promising candidates (not winners)

1. **Split Plate (P2 / R2)** — strong epistemic separation, wheel uncrossed,
   transfers Profile→Relocated cleanly. *Promising because* it carries family
   resemblance and the identity/context grouping for free; *to test:* balance and
   verticality.
2. **Lower Context (P8 / R6)** — identity above, context+metadata below, wheel
   firmly centered and undisturbed. *Promising because* it protects the wheel best
   and keeps a clean reading descent; *to test:* whether below-wheel context
   competes with the tables.
3. **Quiet Relocation (R10)** — Relocated reuses Profile's exact geometry, only
   content differs. *Promising because* it is the maximal family-resemblance move
   and honors subject/authority by position; *to test:* whether location feels
   prominent enough.
4. **Single Authority Band + Sticky City Bar (C1)** — one profile band governs;
   compact city identities; systems stated once. *Promising because* it solves
   Comparison width and authority cleanly; *to test:* how many cities before the bar
   strains.
5. **Observatory Comparison (C3)** — small per-city wheels keep the chart present in
   comparison while a shared profile band governs. *Promising because* it preserves
   the centering instinct even on the matrix surface; *to test:* whether mini-wheels
   help or clutter.

These five cohere with each other (Profile and Relocated can share the Split or
Lower-Context geometry; Comparison can use C1 or C3 atop the same authority logic)
and with the doctrines — but they are candidates to *see*, not decisions.

---

## TASK 10 — What We Learned (geometry only)

- **The wheel is protected by corner and below-wheel geometries, threatened by
  banners, floats, and over-isolation.** The safest place for information is *to one
  side of* or *below* the wheel, never spanning across it and never so far that the
  wheel is marooned.
- **Authority, context, and metadata form a descending order that geometry must
  preserve.** Failures happen when that order flattens into one mass. Identity wants
  to sit high/close; context below/beside; metadata collapses or moves.
- **Subject and authority can be separated geometrically by *prominence vs
  position*.** Location can lead in size and reading order while profile holds the
  anchor slot near the wheel — so a page can be *about* a place yet *governed* by a
  profile without contradiction.
- **The same two-block geometry can serve Profile and Relocated**, which is itself a
  structural family-resemblance win; the Relocated page may differ only in content,
  not arrangement.
- **Comparison is a different geometric problem:** the matrix, not the wheel, is the
  center, so the rules transfer as *protect the matrix's legibility and control
  width* — achieved by a single governing authority band, compact city identities,
  global (not repeated) system metadata, and disclosure/stacking instead of
  horizontal growth.
- **Width on Comparison and verticality on Profile/Relocated are the two scarce
  resources** geometry must budget; long names and full metadata are the main
  threats to both, and disclosure is the main relief.
- **Metadata is the most movable layer** — almost every successful arrangement keeps
  identity visible and lets technical/system metadata collapse, move below, or go
  global. Metadata flexibility is what buys the wheel its room.

Open for the visual boards (geometry questions only the eye can answer): how tall
the Split Plate's two blocks actually grow; whether below-wheel context competes
with tables; whether mini-wheels in Comparison clarify or clutter; how many cities
a sticky bar holds before straining; whether location can feel prominent in a
shared Profile geometry.

Exploration only. No mockups, CSS, implementation, or final decision.
