# Visual Surface Critique — Phase 3.1A

Visual critique of real surfaces against the Design Philosophy Brief. Not a
redesign. No fixes implemented, no code, no styling values.

Surfaces reviewed (as built):
- `prototype_profile_workspace_v11.html`
- `prototype_relocated_location_v1.html`
- `comparison_v5.html`

Observed geometry (for grounding, not prescription):
- **Profile v11** = Side-Plate: `view-pills` → `chart-head` (plate ~240 *beside*
  560 wheel) → `ref-row` (PiH 1.05 / AiS 0.72 / A2A 1.23) → `lower` 3-col panels
  (Favorites / Comparisons / Searches). Notes exist only as "notes" links in the
  lists + modal.
- **Relocated v1** = Location-Banner: `loc-header` (big H1 subject + 5-item
  meta-block + Favorited button) *above* → `charts` (guest wheel + side plate) →
  `sys-meta` 3-col (Birth / Relocated / System) → `lower-section` (Intelligence +
  Notes composer).
- **Comparison v5** = Authority-Band: `app-nav` → `profile-block` band → sticky
  `city-bar` (2px boundary) → collapsible block sections (AiS / PiH / A2A
  fact-tables) → CI cards + section notes. No wheel (`wheel-reserved`).

===============================================================================
# TASK 1 — Works / Wrong / Unfinished (no fixes)
===============================================================================

## Profile v11
- **Works:** wheel reads as the object (good size + glow); view-pills are a clean,
  obvious context switch; the three reference tables sit in a calm row; home
  warmth feels alive without decoration.
- **Wrong:** the plate sits *left of* the wheel but is small and light, so the
  wheel drifts right-of-center inside the wide column — left whitespace imbalance;
  authority reads thin (the small plate) against the big serif name; profile
  authority is split between the topbar selector and the plate name.
- **Unfinished:** notes have no home on the chart page (only tiny "notes" links in
  the lower lists); the lower 3-col panel region feels like a different, denser
  page stapled below the chart.

## Relocated v1
- **Works:** the place is unmistakably the subject; the Notes composer is present
  and feels welcomed; favorite state is visible; sys-meta is tidily grouped.
- **Wrong:** the `loc-header` banner (large H1 + 5 meta items + Favorited button)
  pushes the wheel down and makes location *out-shout* the profile lens ("For
  David Goodman" is small/subordinate) — authority weaker than subject; metadata
  is **tripled** — lat/lon/UTC appear in the loc-header meta-block, again in the
  side plate, again in sys-meta's Relocated column.
- **Unfinished:** "Open Full City Intelligence" is disabled; Notes hint says
  "Edits sync when wired"; the page reads as banner → wheel → metadata slab rather
  than a settled chart surface.

## Comparison v5
- **Works:** the single `profile-block` band gives clean, unambiguous authority;
  the sticky city bar holds column identity; collapsible sections tame density;
  fact-tables (label column + row borders) are genuinely readable.
- **Wrong:** there is **no chart anywhere** (`wheel-reserved`) — the surface loses
  the product's centering instinct entirely; section-adjacent Notes toggles make
  notes feel attached to *table sections*, brushing against the page-owned
  doctrine; city identity in the bar will fight for width as cities grow.
- **Unfinished:** reserved wheel placeholders; add-city / restore stubs; the
  matrix is strong but the page-top (nav + band + city bar) stacks three boundary
  layers before any data.

===============================================================================
# TASK 2 — Wheel dominance (actual visual balance)
===============================================================================
```text
 PAGE          WHEEL STATE            VERDICT
 Profile v11   560 single, beside     APPROPRIATELY DOMINANT, but shifted
               240 plate              right-of-center (left whitespace)
 Relocated v1  guest wheel pushed     TOO SMALL *in effect* — not by px but
               below tall banner      because banner steals the top viewport
 Comparison v5 none (reserved)        ABSENT — matrix is the center by design;
                                      no wheel to judge (continuity gap)
```
- Profile: dominance is right, *placement* is off (wheel not centered).
- Relocated: the wheel's intrinsic size is fine; the **banner robs its
  dominance** by occupying first attention.
- Comparison: no wheel — the only surface where the chart is wholly absent.

===============================================================================
# TASK 3 — Authority visibility (without careful reading)
===============================================================================
```text
                       whose chart   where am I   what page
 Profile v11    yes (plate name)   weak (pills)   yes-ish
 Relocated v1   WEAK (lens tiny)   yes (big H1)   yes (place)
 Comparison v5  yes (band)         yes (cities)   yes (band+bar)
```
- **Profile:** you can tell whose chart, but authority is *quiet* and split
  (topbar selector vs plate name); "what page / which view" leans on the pills.
- **Relocated:** the place is loud, the **profile lens is too quiet** — at a glance
  the page looks *about* Kyoto and you must read to learn it's *governed by* a
  profile. Authority under-reads relative to subject.
- **Comparison:** strongest of the three — the band answers "whose lens" and the
  city bar answers "where," immediately.

===============================================================================
# TASK 4 — Table balance (visual only, not importance)
===============================================================================
```text
 PROFILE / RELOCATED ref-row : PiH 1.05 | AiS 0.72 | A2A 1.23
   PiH   proportionally correct
   AiS   feels CRAMPED  (narrowest column, but holds short data — tolerable)
   A2A   widest, carousel — proportionally correct, owns its room
 COMPARISON fact-tables :
   label-col + city cols  proportionally correct AS the page's main surface
   (collapsible sections keep any one block from oversizing)
```
- Profile/Relocated tables are well proportioned overall; **AiS is the one that
  visually pinches** (smallest fraction), though its content is light enough to
  survive.
- Comparison tables are the dominant surface and read at the right scale; no table
  feels oversized because sections collapse.

===============================================================================
# TASK 5 — Notes integration (page-owned, not table-owned)
===============================================================================
```text
 PAGE          NOTES TODAY                       FEELS
 Profile v11   only "notes" links in lists +     FORCED / homeless on the chart
               modal                              page; no welcomed surface
 Relocated v1  composer in lower-section,         WELCOMED (best of the three);
               "same record as Favorites"         correctly favorite-place owned
 Comparison v5 toggles beside block SECTIONS      AMBIGUOUS — reads table-section
                                                  owned, brushing the doctrine
```
- **Relocated** is where notes feel naturally welcomed (a real composer, correct
  ownership language).
- **Profile** notes feel forced — present only as link-outs, no home, despite
  Profile being the intended clearinghouse.
- **Comparison** notes risk reading as *section*-owned because the toggles live
  inside block headers; visually they want to belong to the comparison, not the
  table.

===============================================================================
# TASK 6 — Ten highest-value visual improvements
   (Problem / Why it matters / Expected gain — no implementation)
===============================================================================
```text
1. PROBLEM  Profile wheel sits right-of-center beside a small left plate.
   WHY      Doctrine: wheel must read as the centered object.
   GAIN     Restores wheel centrality; removes left-whitespace imbalance.

2. PROBLEM  Relocated banner pushes the wheel out of first attention.
   WHY      Doctrine: on Relocated the wheel must be in the opening viewport.
   GAIN     Wheel regains dominance; page stops feeling like a city header.

3. PROBLEM  Relocated profile lens ("For …") under-reads vs the big place H1.
   WHY      Subject may lead, but profile must remain the visible authority.
   GAIN     Authority/subject balance; page reads as governed, not just titled.

4. PROBLEM  Relocated metadata is tripled (loc-header / side plate / sys-meta).
   WHY      Metadata sprawl crowds the wheel and dilutes the identity block.
   GAIN     One home per fact; calmer page; wheel breathes.

5. PROBLEM  Profile notes are homeless (links only) on the clearinghouse page.
   WHY      Profile is meant to be the master notebook surface.
   GAIN     Notes feel welcomed; the page fulfills its clearinghouse role.

6. PROBLEM  Comparison has no chart presence at all.
   WHY      Centering instinct / family resemblance across surfaces.
   GAIN     Comparison rejoins the organism (Observatory direction).

7. PROBLEM  Comparison notes read as table-section owned.
   WHY      Notes must feel page/entity owned, never table owned.
   GAIN     Removes the strongest doctrine-violation cue on the surface.

8. PROBLEM  Profile authority is split (topbar selector vs plate name).
   WHY      One legible authority point reads faster and unifies surfaces.
   GAIN     Quicker "whose chart"; consistency with Comparison's band.

9. PROBLEM  AiS column visually pinches in the ref-row.
   WHY      Cramped columns read as cramped even with light data.
   GAIN     Calmer table row; better proportional rhythm.

10. PROBLEM Relocated stacks banner → wheel → metadata slab → panels.
    WHY     Vertical sprawl buries the wheel and separates it from its tables.
    GAIN    Tighter chart-to-table relationship; less scrolling to the wheel.
```

===============================================================================
# TASK 7 — Things doctrine could not reveal (only visible once built)
===============================================================================
```text
- Relocated's metadata TRIPLING. On paper each block (loc-header, side plate,
  sys-meta) was justified alone; only the rendered page shows the same lat/lon/UTC
  three times. Redundancy is a build-time discovery, not a doctrine one.

- The Relocated banner DEFEATS wheel-dominance even though no rule was broken
  per-element. The banner is "allowed," the side plate is "allowed," the sys-meta
  is "allowed" — together they push the wheel down. Emergent, not specified.

- Profile's wheel is "appropriately dominant" yet still OFF-CENTER. Doctrine sized
  the wheel correctly but said nothing about the plate stealing horizontal center;
  only the eye shows the imbalance.

- Comparison feels LESS like the product than expected — not because of any rule,
  but because the total absence of a wheel removes the family's strongest visual
  signature. Doctrine treated "matrix is the center" as fine; seen, it reads as a
  different app.

- Profile notes' HOMELESSNESS only becomes obvious on the page: the doctrine
  named Profile the clearinghouse, but the built surface has nowhere for notes to
  live, exposing a gap between role and layout.

- AiS pinch: a proportion that reads fine as a fraction (0.72) but visually
  cramps — only judgeable once rendered.

- Three stacked boundary layers at Comparison's top (nav + band + city bar) create
  a "wall before data" feeling no single boundary rule predicted.
```

Visual critique only. Not a redesign. Next phase: real mockups answering these.
