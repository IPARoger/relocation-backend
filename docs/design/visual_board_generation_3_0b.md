# Visual Board Generation — Phase 3.0B

Visual boards only. Show, don't tell. Numbers = reading/attention order.

```text
[ WHEEL ]  primary chart      AUTH  profile sel·name·b.date·b.time·b.city
( o )      mini-wheel         CTX   Natal/Current/Reloc·city·lat/lon·UTC·systems
{ meta }   lat/lon·UTC·Trop·Plac    NOTES notes region   ····· collapsed/disclosed
[PiH][AiS][A2A] tables        ==== strong boundary       CIP  city-intel preview
```

###############################################################################
# TASK 1 — PROFILE BOARDS
###############################################################################

## SPLIT PLATE — study A (auth UL / ctx LL)
```text
+-----------------------------------------------------------+
| AUTH(1) David Goodman v                                   |
| 14 Mar 1989 · 07:42                                       |
| Portland, OR                       [    WHEEL    ](3)     |
| - - - - - - -                      [          ]           |
| CTX(2) Natal                       [          ]           |
| 44.0N·122.7W                       [          ]           |
| {UTC-8·Tropical·Placidus}(4)                              |
+========================ref-row===========================+
| [  PiH (5) ] [ AiS ] [     A2A          ]                 |
+----------------------------------------------------------+
| NOTES(6) ·············· disclosed                         |
+----------------------------------------------------------+
```
hier: AUTH1 > CTX2 > WHEEL3 > meta4 > tables5 > notes6

## SPLIT PLATE — study B (auth UL / ctx LL / meta beside wheel base)
```text
+-----------------------------------------------------------+
| AUTH(1) David Goodman v                                   |
| 14 Mar 1989 · 07:42 · Portland OR  [    WHEEL    ](3)     |
| - - - -                            [          ]           |
| CTX(2) Natal · 44.0N 122.7W        [          ]           |
|                                    [__________]           |
|                                    {UTC·Trop·Plac}(4)     |
+========================ref-row===========================+
| [  PiH (5) ] [ AiS ] [     A2A          ]                 |
+----------------------------------------------------------+
```
hier: AUTH1 > CTX2 > WHEEL3 > meta4(under wheel) > tables5

## SPLIT PLATE — study C (notes fill A2A slack, single-chart)
```text
+-----------------------------------------------------------+
| AUTH(1) Name v · 14 Mar 1989·07:42·Portland OR            |
| CTX(2) Natal·44.0N122.7W·{UTC Trop Plac}(4) [ WHEEL ](3)  |
+========================ref-row===========================+
| [ PiH(5) ] [ AiS ] [ A2A ] | NOTES(6)                    |
| [        ] [     ] [     ] | (slack beside A2A,          |
| [        ] [     ] [     ] |  OUTSIDE table bounds)      |
+----------------------------------------------------------+
```
hier: AUTH1 > CTX2 > WHEEL3 > meta4 > tables5 > notes6

## LOWER CONTEXT — study D (identity caps / context floors)
```text
+-----------------------------------------------------------+
|            AUTH(1) David Goodman v                        |
|            14 Mar 1989·07:42·Portland OR                  |
|                                                           |
|                 [     WHEEL     ](2)                      |
|                 [               ]                         |
|                 [               ]                         |
|                                                           |
|     CTX(3) Natal·44.0N 122.7W·{UTC Trop Plac}(4)          |
+========================ref-row===========================+
| [  PiH (5) ] [ AiS ] [     A2A          ]                 |
+----------------------------------------------------------+
| NOTES(6)                                                  |
+----------------------------------------------------------+
```
hier: AUTH1 > WHEEL2 > CTX3 > meta4 > tables5 > notes6

## LOWER CONTEXT — study E (auth UL strip / context band under wheel)
```text
+-----------------------------------------------------------+
| AUTH(1) David Goodman v · 14 Mar 1989·07:42·Portland OR   |
|-----------------------------------------------------------|
|                 [     WHEEL     ](2)                      |
|                 [               ]                         |
|                 [               ]                         |
|===========================================================|
| CTX(3) Natal | 44.0N 122.7W | {UTC-8·Trop·Plac}(4)        |
+========================ref-row===========================+
| [  PiH (5) ] [ AiS ] [     A2A          ]                 |
+----------------------------------------------------------+
| NOTES(6)                                                  |
+----------------------------------------------------------+
```
hier: AUTH1 > WHEEL2 > CTX3 > meta4 > tables5 > notes6

box-diagram (Split vs Lower):
```text
 SPLIT PLATE              LOWER CONTEXT
 +------+--------+        +-----------------+
 | AUTH | WHEEL  |        |      AUTH       |
 | CTX  | WHEEL  |        |      WHEEL      |
 +------+--------+        |      CTX        |
 | tables        |        +-----------------+
 +---------------+        | tables          |
 left-loaded             | NOTES            |
 wheel center-right      +-----------------+
                         wheel dead-center
```

###############################################################################
# TASK 2 — RELOCATED BOARDS  (location important, NOT authority)
###############################################################################

## QUIET RELOCATION — study A (Profile geometry, content swapped)
```text
+-----------------------------------------------------------+
| AUTH(1) for David Goodman v   <- SAME slot as Profile     |
| 14 Mar 1989·07:42·Portland OR      [  WHEEL  ](3)         |
| - - - -                            [ (guest) ]           |
| CTX(2) Kyoto, Japan                [        ]            |
| 35.0N·135.7E                       [        ]            |
| {UTC+9·Trop·Plac}(4)                                     |
+========================ref-row===========================+
| [ PiH(5) ] [ AiS ] [    A2A         ]                    |
+----------------------------------------------------------+
| NOTES(6) (favorite-place) ········· CIP ·····(7)         |
+----------------------------------------------------------+
```
authority via SLOT; location via content. lens stays by wheel.

## SPLIT PLATE (Relocated) — study B (subject leads size, lens keeps slot)
```text
+-----------------------------------------------------------+
| KYOTO, JAPAN (1, big)                                     |
| for David Goodman v (auth, anchor slot) [  WHEEL  ](3)   |
| - - - -                                 [ (guest) ]      |
| CTX(2) Relocated·35.0N 135.7E           [        ]       |
| {UTC+9·Trop·Plac}(4)                    [        ]       |
+========================ref-row===========================+
| [ PiH(5) ] [ AiS ] [    A2A         ]                    |
+----------------------------------------------------------+
| NOTES(6)                          CIP preview(7)         |
+----------------------------------------------------------+
```
location = size+order ; profile = proximity+anchor.

## LOWER CONTEXT (Relocated) — study C (auth above / location below wheel)
```text
+-----------------------------------------------------------+
|         AUTH(1) for David Goodman v                       |
|                                                           |
|              [     WHEEL (guest)     ](2)                 |
|              [                       ]                    |
|              [                       ]                    |
|                                                           |
| LOCATION(3) Kyoto, Japan · 35.0N 135.7E · {UTC Trop}(4)   |
+========================ref-row===========================+
| [ PiH(5) ] [ AiS ] [    A2A         ]                    |
+----------------------------------------------------------+
| NOTES(6)                          CIP preview(7)         |
+----------------------------------------------------------+
```
authority senior(above) ; location prominent(below) ; wheel safe.

## RELOCATED — study D (location header band, lens subtitle)
```text
+===========================================================+
| KYOTO, JAPAN (1)   ·subtitle· for David Goodman v (auth)  |
+-----------------------------------------------------------+
|              [     WHEEL (guest)     ](3)                 |
|              [                       ]                    |
| CTX(2) Relocated·35.0N135.7E·{UTC+9 Trop Plac}(4)        |
+========================ref-row===========================+
| [ PiH(5) ] [ AiS ] [    A2A         ]                    |
+----------------------------------------------------------+
| NOTES(6)   |   CIP preview(7)  [Open City Intelligence]  |
+----------------------------------------------------------+
```
RISK: band lowers wheel; subject may over-lead authority.

## RELOCATED — study E (side place-ledger + CIP at ledger foot)
```text
+-----------------------------------------------------------+
| for David Goodman v (1)                                   |
|                                          PLACE(2)         |
|        [    WHEEL (guest)    ](3)        Kyoto, Japan     |
|        [                     ]           35.0N·135.7E     |
|        [                     ]           {UTC+9}(4)       |
|        [                     ]           Trop·Plac        |
|                                          ----             |
|                                          CIP(7) preview   |
+========================ref-row===========================+
| [ PiH(5) ] [ AiS ] [    A2A         ]                    |
+----------------------------------------------------------+
| NOTES(6)                                                  |
+----------------------------------------------------------+
```
location lives in right ledger; wheel shifts left (mild).

how location stays subordinate (box):
```text
 AUTHORITY = WHERE (slot near wheel) + ANCHOR (fixed position)
 LOCATION  = WHAT  (size + reading-order + headline)
 => place can be BIG and FIRST yet never own the lens
```

###############################################################################
# TASK 3 — COMPARISON BOARDS  (width / city-count / density pressure)
###############################################################################

## SINGLE AUTHORITY BAND — study A (3 cities)
```text
+===========================================================+
| PROFILE BAND(1) David Goodman v · Tropical · Placidus     |
+=========================sticky============================+
| CITY(2) | Lisbon    | Austin    | Bali     | + add       |
|         | 38.7N9.1W | 30.2N97.7W| 8.6S115E |             |
+-----------------------------------------------------------+
| Sun (3) |  H10      |  H7       |  H1      |              |
| Moon    |  H4       |  H2       |  H9      |              |
| ASC     |  Gem      |  Lib      |  Aqu     |              |
+-----------------------------------------------------------+
| NOTES(4) (comparison-entity)                              |
+-----------------------------------------------------------+
```
one authority governs all ; systems once in band.

## SINGLE AUTHORITY BAND — study B (5 cities, width pressure)
```text
+===========================================================+
| PROFILE BAND(1) David Goodman v                          |
+=========================sticky============================+
| CITY(2)| Lisbon | Austin | Bali | Porto | Nice | +      |
+-----------------------------------------------------------+
| Sun(3) |  H10   |  H7    | H1   | H10   | H8   |         |
| Moon   |  H4    |  H2    | H9   | H4    | H6   |         |
| ASC    |  Gem   |  Lib   | Aqu  | Gem   | Vir  |         |
+-----------------------------------------------------------+
| System(4): Tropical · Placidus (stated ONCE, global)      |
+-----------------------------------------------------------+
   <----------------- horizontal scroll ----------------->
```
systems pulled to footer => columns stay narrow, more cities fit.

## OBSERVATORY COMPARISON — study C (mini-wheel per city)
```text
+===========================================================+
| PROFILE BAND(1) David Goodman v · Tropical · Placidus     |
+-----------------------------------------------------------+
|   ( o )         ( o )          ( o )        (2)           |
|  Lisbon        Austin         Bali                       |
|  38.7N9.1W     30.2N97.7W     8.6S115E                   |
+=========================matrix============================+
| Sun(3) |  H10   |  H7        |  H1     |                  |
| Moon   |  H4    |  H2        |  H9     |                  |
| ASC    |  Gem   |  Lib       |  Aqu    |                  |
+-----------------------------------------------------------+
| NOTES(4)                                                  |
+-----------------------------------------------------------+
```
chart present per column (centering instinct survives).

## OBSERVATORY — study D (mini-wheels + spotlight pair, others parked)
```text
+===========================================================+
| PROFILE BAND(1) David Goodman v · Tropical · Placidus     |
+-----------------------------------------------------------+
| parked: [Bali][Porto][Nice]   (slim tabs)                |
+============== focus pair(2) ==============================+
|     ( o ) Lisbon       |     ( o ) Austin                |
|     38.7N 9.1W         |     30.2N 97.7W                 |
+=========================matrix(3)=========================+
| Sun  |  H10            |  H7                             |
| Moon |  H4             |  H2                             |
+-----------------------------------------------------------+
| NOTES(4)                                                  |
+-----------------------------------------------------------+
```
density capped at 2 wheels ; depth preserved.

## OBSERVATORY — study E (stacked rows, width->height, wheel per row)
```text
+===========================================================+
| PROFILE BAND(1) David Goodman v · Tropical · Placidus     |
+-----------------------------------------------------------+
| ( o ) LISBON(2) 38.7N9.1W  | Sun H10·Moon H4·ASC Gem (3) |
| ----------------------------------------------------------|
| ( o ) AUSTIN(2) 30.2N97.7W | Sun H7 ·Moon H2·ASC Lib     |
| ----------------------------------------------------------|
| ( o ) BALI(2)   8.6S115E   | Sun H1 ·Moon H9·ASC Aqu     |
+-----------------------------------------------------------+
| NOTES(4)                                                  |
+-----------------------------------------------------------+
```
no width pressure ; wheel never central (tradeoff).

density/width map:
```text
            3 cities      5 cities       8 cities
 A band  |  clean        scroll         scroll++        |
 C obs   |  clean        crowded        fails           |
 D pair  |  n/a          clean          clean           |
 E stack |  clean        clean          long-scroll     |
```

###############################################################################
# TASK 4 — NOTES INTEGRATION (placement only)
###############################################################################
```text
SIDE COMPANION            LOWER COMPANION         DRAWER
+----------+-----+        +----------------+      +----------------+
| WHEEL    |NOTE |        | WHEEL          |      | WHEEL       []<- tab
| tables   |NOTE |        | tables         |      | tables         |
+----------+-----+        +----------------+      +----------------+
                         | NOTES          |      | NOTES slides in|
                         +----------------+      +----------------+

NOTEBOOK LAUNCHER         DEDICATED ENTRY
+----------------+        +----------------+
| WHEEL          |        | WHEEL  tables  |
| tables  [Notes]| -----> |  (own notebook |
+----------------+        |   page/route)  |
  small launcher          +----------------+
```
rule (shown): notes always AFTER wheel, OUTSIDE table bounds.
```text
 OK:  below tables | beside tables(slack) | drawer | launcher | own page
 NO:  inside PiH/AiS/A2A cell  ->  implies row/section notes (forbidden)
        [ PiH | NOTE ]   <-- X never per-table
```

###############################################################################
# TASK 5 — FAILURE BOARDS (why they fail, visually)
###############################################################################

## WHEEL EXILE
```text
+-----------------------------------------------------------+
| AUTH  CTX  {meta meta meta}      [WHEEL] <- shoved corner  |
| tables tables tables tables                               |
+-----------------------------------------------------------+
  X center of gravity lost ; chart is an afterthought
```

## METADATA SPRAWL
```text
+-----------------------------------------------------------+
| {lat}{lon}{UTC}{TZ}{Trop}{Plac}{src}{elev}{datum}         |
|        [ WHEEL ] <- nibbled by a field of small facts      |
| {alt}{geoid}{house-cusp}{ayanamsa}{...}                   |
+-----------------------------------------------------------+
  X reference data given ROOM instead of sufficiency
```

## AUTHORITY DILUTION
```text
+-----------------------------------------------------------+
| Kyoto(big)         [ WHEEL ]            (no profile near)  |
| ........ for D.G. (tiny, far bottom-right corner) .......  |
+-----------------------------------------------------------+
  X lens demoted/scattered ; page stops feeling governed
```

## BANNER OVERLOAD
```text
+===========================================================+
| AUTH + CTX + {meta} + controls all in one fat top band(1) |
+===========================================================+
|              [ WHEEL ](shoved down, 2)                    |
+-----------------------------------------------------------+
  X first attention lands on band, not chart ; wheel lowered
```

## COLUMN INFLATION (comparison)
```text
+-----------------------------------------------------------+
| | Lisbon        | Austin        | Bali          |         |
| | full plate    | full plate    | full plate    |         |
| | +all metadata | +all metadata | +all metadata |         |
| | Sun H10       | Sun H7        | Sun H1        |  ...     |
+-----------------------------------------------------------+
   <======= width explodes ; comparison = endurance ======>
```

## SYMMETRY TRAP
```text
+-----------------------------------------------------------+
| AUTH(1?)            [ WHEEL ]            CTX(1?)           |
| birth triad                              city·coords      |
+-----------------------------------------------------------+
  X mirrored corners ; which is senior? eye ping-pongs <-->
```

###############################################################################
# TASK 6 — RAPID ELIMINATION (geometry only)
###############################################################################
```text
IMMEDIATELY STRONG
  Profile  : Lower Context (D)        wheel dead-center, symmetric
  Profile  : Split Plate (A/B)        clean epistemic split, uncrossed
  Relocated: Quiet Relocation (A)     mirrors profile, calm
  Relocated: Lower Context Reloc (C)  auth up / place down, wheel safe
  Compare  : Single Authority Band(A) clean top-down stack
  Compare  : Observatory (C)          chart survives matrix

UNCLEAR (needs the eye)
  Profile  : Split study C (notes-in-slack)   4th compartment in row?
  Relocated: Split Reloc (B)                  does place over-lead?
  Relocated: header band (D)                  wheel lowered too far?
  Compare  : Observatory pair (D)             do mini-wheels help/clutter?
  Compare  : Authority Band 5-city (B)        where does width break?

IMMEDIATELY WEAK
  Relocated: side ledger (E)          wheel shifts off-center
  Compare  : Observatory stacked (E)  wheel never central, long scroll
  + ALL failure boards (Task 5)
```

###############################################################################
# TASK 7 — VISUAL SHORTLIST
###############################################################################
```text
PROFILE — TOP 2
 1. Lower Context (D)
    wheel-protect ★★★★★  hierarchy ★★★★★  notes-room ★★★★☆
    long-names ★★★★☆     scalability ★★★★☆
 2. Split Plate (A)
    wheel-protect ★★★★☆  hierarchy ★★★★★  notes-room ★★★★☆
    long-names ★★☆☆☆ (vertical strain)  scalability ★★★★☆

RELOCATED — TOP 2
 1. Quiet Relocation (A)   == twins with Profile Lower-Context/Split
    wheel-protect ★★★★★  hierarchy ★★★★★  notes-room ★★★★☆
    long-names ★★★★☆     scalability ★★★★★ (one geometry, two pages)
 2. Lower Context Reloc (C)
    wheel-protect ★★★★★  hierarchy ★★★★☆  notes-room ★★★★☆
    long-names ★★★★☆     scalability ★★★★☆

COMPARISON — TOP 2
 1. Single Authority Band (A/B)
    wheel-protect n/a    hierarchy ★★★★★  notes-room ★★★★☆
    long-names ★★★☆☆     scalability ★★★★★ (footer-systems + scroll)
 2. Observatory (C/D)
    wheel-protect ★★★★☆  hierarchy ★★★★☆  notes-room ★★★★☆
    long-names ★★★☆☆     scalability ★★★☆☆ (mini-wheels cost width)
```
coherence thread:
```text
 Profile Lower-Context  ===  Relocated Quiet-Reloc     (shared body)
 Comparison Auth-Band    ===  Comparison Observatory     (shared head)
 -> one organism reads at a glance
```

###############################################################################
# TASK 8 — QUESTIONS ONLY THE EYE CAN ANSWER
###############################################################################
```text
1. Lower-Context vs Split Plate: which protects the wheel better WHEN
   rendered at real proportions?
2. At what city count does the Single Authority Band stop reading as
   "comparison" and start reading as "spreadsheet"?
3. Do Observatory mini-wheels clarify the matrix or clutter it?
4. Does below-wheel context (Lower Context) compete with the tables?
5. Does the home/guest difference register as KINSHIP, NOTHING, or
   DIMINISHMENT once a real guest wheel is seen?
6. Do long names actually break the Split Plate's vertical rhythm, or
   are they absorbed?
7. Does notes-in-A2A-slack read as "notes" or as "another table cell"?
8. Can location be BIG + FIRST and still feel subordinate to a small
   nearby profile lens? (only the eye decides)
9. Where exactly does metadata stop grounding the wheel and start
   crowding it?
10. Does CIP preview belong beside notes, below tables, or as a launcher?

=> These now require ACTUAL MOCKUPS. Conceptual exploration ends here.
```

Visual boards only. Next phase: real mockups, not conceptual exploration.
