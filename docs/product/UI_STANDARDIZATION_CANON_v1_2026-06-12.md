# UI_STANDARDIZATION_CANON_v1_2026-06-12

**Status:** Canonical, revisable operating manual for UI standardization decisions made during the beta harmonization pass (June 2026).  
**Purpose:** One central location for what is locked, what is provisional, and what remains — so future chats, designers, and implementers do not re-derive decisions from scattered studies.  
**Authority:** Subordinate to `FOUNDATIONAL_CONSTITUTION.md` and `INTERFACE_AND_DESIGN_CANON.md`. When this doc conflicts with those, the constitutional docs win.  
**Revision policy:** Update this file when a system is promoted from provisional → locked, or when a locked decision is intentionally revised. Note changes in §12 Revision Log.

**Live studies:** `validation/mockups/beta/index.html`  
**Primary table study:** `validation/mockups/beta/table_format_study.html`

---

## 0. Constitutional Anchor (unchanged)

**Reveal structure. Preserve judgment.**

Standardization exists to make the instrument feel like one family — not to decorate, gamify, or steer emotion. Color, glow, and motion must teach structure and familiarity without implying good/bad judgment.

---

## 1. Master Standardization Register

The project began with GPT’s 20-category inventory, whittled to **10 decidable structural systems**, then expanded in practice as badges, favorites, and color studies emerged.

### 1A. Core 10 (structural pass)

| # | System | Status | Notes |
|---|--------|--------|-------|
| 1 | **Title Plate** | ✅ Locked (~95%) | Zone A account owner (upper right, initials circle + menu). Zone B name plate (center-aligned text; Edit/+ as appendages). Zone C location context on relocated only. Wheel always centered. |
| 2 | **Spacing** | ◑ Applied (~80%) | Vertical rhythm on Fibonacci scale (3·5·8·13·21). Page margins and card gaps harmonized in beta prototypes. Full spacing doctrine not yet written as standalone spec. |
| 3 | **Card** | ◑ Applied (~80%) | Shared `tcard` shell: serif title, interior padding, collapse caret left of title. Table order **AiS · PiH · A2A · Notes** (Notes as different species, extra separation TBD). |
| 4 | **Border** | ✅ Locked (~90%) | **G3** mono-depth grey double line + **~4% interior signature glow** on all table cards (chart + comparison). Per-table hue whisper (AiS/PiH/A2A). Colorist intensity pass deferred. |
| 5 | **Separator** | ✅ Locked (~80%) | See §3. Row inset hairlines, section hierarchy, spacing-before-notes, earn-the-line rule. |
| 6 | **Table** | ✅ Locked (~85%) | See §4. 34-unit grid, formats, vertical rhythm, G3+glow. |
| 7 | **Button** | ◻︎ Not formalized | Roles, states, action-verb lexicon discussed in `docs/design/control_and_action_doctrine_audit.md` — not locked. |
| 8 | **Link** | ◻︎ Not formalized | Chevron policy, underline, external links — partially implemented in favorites/city rows. |
| 9 | **Hover** | ◑ Partial | Desktop rollover chevron + light row highlight in favorites. Glow carved out to color pass. |
| 10 | **Metadata** | ◑ Partial | Birth date/time/place, lat-lon, UTC, Tropical·Placidus placement rules locked on title plate; full metadata collapsibility not locked. |

### 1B. Parallel tracks (not in original 10, but required)

| Track | Status | Notes |
|-------|--------|-------|
| **Badge system** | ◑ Provisional | Natal / Current Location badges; de-pilled B1 direction; colorist pass deferred. |
| **Color & typeface** | ◻︎ Deferred | L2 New Pastures + B1 badges as working skin. Professional colorist pass planned. |
| **Animation & motion** | ◑ In study | See §5F. Functional, human-paced, no acceleration/overshoot/added color. Studies in `motion_lab.html`. Overlay reveal (rain/virga) deferred to clean-start. |
| **Controls & disclosure** | ✅ Locked (~85%) | See §5. Decision board answered 2026-06-12. Custom dropdown D2, collapse stub H1+, C3/S1, selective custom C4. |
| **Genie / search UI** | ◑ Partial | See §6. Two-tier cascade, overlay popover — implemented in favorites study, not site-wide. |
| **Map workspace** | ◻︎ Stale | `map_CURRENT.html` not harmonized with beta chart/comparison family. |
| **Favorites / Saved** | ◑ ~70% | Thirds layout, sort popover, genie filter — polish deferred. |
| **Settings** | ◻︎ Not started | |
| **Help handbook** | ◻︎ Not started | |
| **Teaching overlays** | ◻︎ Not started | First-time use, chart entry overlay. |
| **Notes page** | ◻︎ Not started | Combined notes filesystem + scratch pad. |
| **Auth integration** | ◻︎ Not started | Tie surfaces together with account/session. |

### 1C. Synthesis layer (do last)

**Family Resemblance System** — final pass after structural 10 + color/type + animation are settled. Confirms all pages read as one instrument.

---

## 2. Title Plate System (locked)

**Account owner (Zone A)** — upper right. Circle with initials + dropdown (Help, Profile, Log out). Independent of whose chart is displayed.

**Name plate (Zone B)** — most authoritative block on any page. Center-aligned name; Edit and + are **appendages** (do not participate in centering). Birth date and time may share one line (especially 24h). Metadata (lat/lon, UTC, Tropical·Placidus) is reference-grade; spacing tightened across pages.

**Location context (Zone C)** — relocated/current-location pages only. City name larger than person name for temporary location emphasis. **Current Location** badge on chart; **Natal** badge in comparisons and favorites. Profile page has no Zone C (natal chart).

**Wheel** — always centered at top; tables below. Zone B and C fill horizontal space beside the wheel on desktop.

---

## 3. Separator System (locked ~80%)

| Decision | Rule |
|----------|------|
| **Row separators (tables)** | **1C** inset hairline. **8px** inset standard width; **4px** when column is narrow. Last row: no bottom rule. |
| **Section separators** | **2B + 2C mix** — medium rule between major bands (wheel → tables); hairline between table cards; **extra whitespace before Notes** (species separation — amount TBD in full layout). |
| **Card separation** | **3A** gap-only between sibling cards (no shared vertical ledger). |
| **Line-weight hierarchy** | Hairline = row; medium = section; heavy reserved for comparison/double-border tables. |
| **Earn the line** | Prefer whitespace when hierarchy is already clear. Lines earn their place at row and section boundaries, not as decoration. |
| **City Intelligence** | Real divider **before** CI block (different species from tables). |
| **Texture / valence** | Pinned, not locked. `distinct_texture_study.html` — revisit with color pass. No emotional shading as default. |

**Studies:** `separator_study.html`, `separator_calibrate.html`

---

## 4. Table System (locked ~85%)

### 4A. Page order and allocation

Tables appear left-to-right: **AiS · PiH · A2A · Notes** (Notes may occupy reserve column or separate band).

**Horizontal grid — 34 units** (Fibonacci family):

| Slot | Units | Role |
|------|-------|------|
| AiS | 8 | Angle in Sign |
| PiH | 8 | Planet in House |
| A2A | 13 | Aspect to Angle (All mode needs 4 angle columns) |
| Reserve | 5 | Notes and/or implied “+ city” capacity on comparison |

Internal column subdivisions also use Fibonacci ratios (e.g. PiH **5:3:2**, AiS label + centered value field).

### 4B. Vertical rhythm

- **Row unit:** ~**21px** (Fibonacci), fixed per row — `min-height` + minimal vertical padding (3px).
- **Header gap below title:** 8px.
- **Column gap between cards:** 18px.
- **Section gap:** 21px.
- **Dynamic growth:** Adding planets/aspects adds whole row-units; sibling tables top-align. Long lists may paginate at Fibonacci caps (13, 21) with “show more.”
- **Row rhythm:** **Fixed row unit** (B2) — Sun in PiH lines up with Sun in A2A and ASC in AiS; total height floats as bodies are added.

### 4C. Title treatment

- Titles **flush left** (serif).
- No redundant column headers when serif card title is present.

### 4D. Format rules

**PiH**
- Planet flush left (4px indent).
- House value centered in value column (ordinal: 1st, 2nd, 3rd…).
- Late-in-house: greyed value + `?` as exponent beside number (not far margin).
- **Show Dignities** toggle at **bottom of PiH card** (footer) — does not push rows out of sync with siblings; hides when PiH collapses.

**AiS**
- Full sign names (not abbreviations).
- Value centered on the **sign word**: degree hangs left, minutes hang right; sign names align vertically down the card.
- Angle label (ASC, DSC, MC, IC) pinned left.

**A2A**
- **All mode:** planet column + 4 angle columns (ASC, DSC, MC, IC).
- Cell format: aspect abbreviation + orb — e.g. `Tri 2°08'`, `Conj 0°41'`.
- Full words (Conjunct, Square…) available via user setting.
- Orb color: **applying** (warm) vs **separating** (cool) — functional, not valence.
- Empty cell: em-dash `—` (not star, not blank).
- Pills for angle filter on card header (same as profile/relocated/comparison).
- Single-angle mode: one value column beside planet, same cell format.

**Comparison matrix**
- Bottle **`comparison_v5_beta.html`** column layout — not the over-tight study variant.
- Header breathing room for `‹ ›`, hide, and city controls.
- Double border: **G3** + inner glow on heavy tables.

### 4E. Border and glow (light vs heavy)

| Weight | Treatment |
|--------|-----------|
| All table cards (PiH, AiS, A2A) | **G3** mono-depth grey double line + **~4% interior signature glow** (wheel-style, even throughout — not drop shadow, not TRON edge). **Locked C5:** per-table signature hue (green/blue/violet family). |
| Heavy (comparison matrix) | Same **G3 + ~4% glow** treatment as chart tables. |
| Color on border | Essentially grey with **~8% hue whisper** on outer ring, **~4%** on interior glow — life without opinion. Professional colorist pass deferred. |
| Row shading | **Lines-only** default (no zebra). Hairline row dividers only. |

**Rejected:** Neon glow, pill badges as default, vertical ledger lines on table sides, star placeholders for empty A2A, D3 left-accent-only border.

### 4F. Density

- **Lean B** (standard), **C** (compact) acceptable on narrow viewports.
- Row padding ~6px in early studies; tightened to ~21px row unit in final study.
- Comparison columns: closer than early beta, but not as tight as the failed study — match `comparison_v5_beta`.

### 4G. Deferred polish

- PiH numbers “one notch left” — fine-tune in full layout.
- Whitespace before Notes: **none extra** beyond grid gap (B3) — tables already have breathing room; Notes species separation via column gap only.
- Left label column compression in dynamic-rhythm demo — revisit in full layout.
- Astrology-harmonic proportions (vs pure Fibonacci) — future proportion pass.
- Propagation to `profile_standard.html`, `relocated_standard.html` — **done 2026-06-12** (structure + G3/glow + lines-only + collapse stub). Comparison G3 propagation pending.
- Comparison AiS uses block-centered values per city column (bottled v5_beta), not word-centered like chart pages — harmonization deferred (OQ).

**Studies:** `table_study.html`, `table_context_study.html`, `table_format_study.html`, `palette_study5.html`, `l2_refine.html`, `badge_depill.html`

---

## 5. Controls, Disclosure & Selection (locked ~85%)

Decision board answered **2026-06-12** (`open_questions_board.html`). Structural rules locked; motion timing deferred to animation pass.

### 5A. Hiding and collapse

| Target | Control | Position | Behavior |
|--------|---------|----------|----------|
| Table cards (PiH, AiS, A2A) | Caret / chevron | **Left** of card title | **H1+:** collapse to **stub only** — title words hidden; caret remains as restore affordance. Sibling cards **do not shrink** (top-aligned band). Drawer destination + motion deferred. |
| City Intelligence | Caret | **Left** of section title | Same grammar as tables |
| Notes (comparison) | Collapse + sticky FAB | FAB stops at city-bar divider; placeholder when hidden | |
| Notes (chart pages) | Pop-out + inline | Far-right column or floating | Rich text; B&W panel; mic glyph harmonized later |

**Rules:** Hide ≠ Remove. Comparison **X** remove requires confirmation popup. Hide must be reversible without hunting. Collapse exists to **reduce clutter** — do not leave unnecessary title text when hidden.

### 5B. Dropdowns and selectors

| Control | Pattern | Custom? |
|---------|---------|---------|
| Account menu (Zone A) | **D2 Soft card** — rounded, soft shadow, hover fill | ✅ Yes |
| Profile selector (name plate) | Same D2 family | ✅ Yes |
| Relocated city selector | Same D2 family + **location search** at top, badge (Current/Natal), gold **star on right when saved**, **+ Add a location** footer | ✅ Yes |
| Genie variable pickers (Map + Saved Searches) | Two-tier cascade, **no search field** — compact rows so all bodies stay visible (§6) | ✅ Yes |
| Sort (Favorites / Saved) | **S1** icon-only `⇅` → popover menu (Recent · A–Z · Distance) | Popover, not native |
| A2A angle pills | On-card pill strip | Not a dropdown — pills stay |
| Map sidebar misc. selects | Hardened native where low-risk | Selective — not full replacement |
| Settings chart-system change | **Ask each time** before applying Tropical·Placidus change (C2) | Modal/confirm, not silent |

**Active-row indicator — LOCKED: checkmark + soft tint** (consistent with favorites/compare checkboxes). Accent-line variant rejected (read too "generic cool SaaS"; new grammar not used elsewhere).

**Genie — no search field, ever.** Even long lists (13 bodies) use compact row formatting so every option is equally visible; no planet is privileged or buried, and no extra effort is required. Shrink formatting before adding chrome.

**City names in dropdowns:** abbreviate region/country to hold menu width (e.g. `Portland, OR · USA`, `Austin, TX · USA`). Full disambiguated names belong to the dedicated **city search** feature (see §10 pending).

**User intent:** Custom dropdown family for all **identity and search** selectors. Not generic 1990s or raw OS chrome. Carets are plain arrows (no circle background).

**Other dropdowns in the product (inventory):** comparison city-add picker (future), settings preference panels, help/account submenus, teaching-overlay dismiss controls. These inherit D2 when they are `<select>`-class choices; pure action menus (Help / Log out) use the same soft-card shell without pretending to be form fields.

**Studies:** `dropdown_study.html` (3 base prototypes), `dropdown_study2.html` (locked: checkmark + no-Genie-search).

### 5C. Checkboxes and selection

| Use | Pattern |
|-----|---------|
| Favorites → Compare | **C3 Whole-row select** — click row; check + tint; checkbox left of row |
| Multi-select lists | Visible checkboxes; no “compare” footer text required |
| Settings toggles | Standard toggle for Show Dignities, node display, aspect glyph vs word, etc. |

### 5D. Buttons and links (preview for #7–#8)

Action lexicon from control audit — target consistency:

- **Edit** — modify existing profile birth data.
- **Add** / **+** — new profile or new city (label the object).
- **Change** — switch active profile lens.
- **Remove** / **Archive** — favorites (settings-handled; trash icon not text).
- **Open** / chevron — navigate to chart or saved item.
- **Search** — explicit button at end of Genie cascade.

**Source:** `docs/design/control_and_action_doctrine_audit.md`

### 5E. Hover (preview for #9)

| Target | Desktop | Mobile |
|--------|---------|--------|
| Favorites city row | Light background + chevron reveal | Chevron always visible or tap row |
| Notes icon | Optional rollover reveal | Always visible |
| Table rows | Subtle (lines-only default); no dark rollover | N/A |
| Links / Open | Chevron may appear on hover | Tap |

Star icon: **only** the star changes when starred — not note color, not row color.

### 5F. Motion (in study — `motion_lab.html`)

**First principle:** animation is functional, never entertainment. It exists only to prevent confusion when something appears, disappears, or changes — so the user sees *that* it happened and *where* it went. If a motion does not answer "where / what changed," remove it.

**Pacing rules (locked direction):**
- **Human-paced**, real-time — not slick, not "blitzkrieg." **Default ~0.75× speed** as the comfortable baseline (chart-page motions).
- **Genie is teaching-paced** — slower and deliberately **not synchronized.** Each beat runs at its own "right" pace for its complexity so the user learns where controls go and how they transform. Many passes needed to see all beats; that is intentional.
- **No acceleration** (ease-in) and **no overshoot/bounce.** Gentle decelerate (ease-out, `cubic-bezier(.25,.1,.25,1)`) or near-linear only.
- **Subtract color, never add it** for motion states (chart-page). Genie may grey/fade but does not add decorative color.
- **One consistent direction** within a family; get out of the way as soon as possible.

| Motion | Behavior |
|--------|----------|
| **Table hide** | The **whole card retracts into a small square around the arrow** — same grammar as the Genie bottle. Square (rounded, soft shadow) is the sole restore handle. **Arrow direction: right when open/expanded, down when hidden/contracted. It never points up.** **No chip, no "AA"/words, no bounce.** |
| **Note pop-out** | **Continuous geometry morph** — the editor **grows as one unbroken motion out of the "Notes" button's footprint** (scale anchored at the button center, content rides along — **no fade-in break, no scale-and-swap**). Closes by shrinking back into the button. Large mini-word-processor (≈ **1/3–1/2 of the screen** in app); **mic (canonical stroke glyph) + keyboard toggle bottom-right** of the input. Last 10% polish deferred. (Small-panel + slide-drawer + content-fade variants rejected.) |
| **Carousel (A2A angle / mobile columns)** | **Horizontal page-turn slide** (locked). Uniform pace, next from right / prev from left, ~0.75×. No scale, no zip. |
| **Map Genie choreography** | See **§5G** below. Current study file: `map_SANDBOX_genie_v6.html` (`body.explore` state). `map_SANDBOX_genie_v5.html` preserved for archaeology. |
| **Overlay reveal (rain / virga)** | **Deferred — clean start.** See **§5H** for intent. Overlays may **appear instantly** for now. |

### 5G. Map Genie choreography (`body.explore` — teaching motion)

**Purpose:** teach the controls — where they are, how they transform, how to use them. Not synchronized swimmers; each animation at its own pace.

**On Search Map invoke (beats are staggered, not locked together):**

| # | Element | Behavior |
|---|---------|----------|
| 1 | **Chrome / nav** | **Setup:** full white topbar. **Explore:** bar dissolves transparent for max map — only logo + hamburger (left) and Share + owner (right) float. Menu links slide into hamburger; reopen from hamburger. **Share always prominent** — setup = icon + "Share" label; explore = bold square glyph button. |
| 2 | **Back / Forward / Pin** | Text labels recede into **icon buttons** (`‹` `›` pin SVG). **Do not grey out** — remain active. |
| 3 | **City search** | **Top-left near map controls** (not centered). **Greys out** (≈50% opacity) but **stays visible and typable**. Magnifying glyph stays bright ("light on"); hover/focus relights on desktop. **Fades back in** when Genie returns. |
| 4 | **Name plate** | **Top-left authority** (same corner grammar as profile pages), offset clear of the `+ − ○` and `‹ › Pin` controls. **Does not move or shrink.** Explore: **no plate box** — the **letters themselves are outlined** (dark glyph + white halo) so the name stays readable over any map color; lat/lon/tools **fade al niente**. Profile-selector caret same size as chart pages (12px). **Fades back in** when Genie returns. |
| 5 | **Variable builder** | Shrinks into the **bottle** square (controls/sliders glyph + badge count). |
| 6 | **Ghost controls** | Fade in like ghosts in the right place on a subtle profile-DNA card (border + inner glow). Labels readable; instructional not decorative. |
| 7 | **Save search** | In-builder **small button** (not underlined link) → **disk glyph** on map (graphic-to-graphic). CSS transition both ways; full ghost-flight JS choreography still pending. |
| — | **Clear** | Says **"Clear"** (not trash icon). Only way to wipe variables; reopening Genie **preserves** last settings. |
| — | **Add & Search** | Label changes to "＋ Add & Search" when row complete; **no color flip** (stays blue). |
| — | **Bottle** | No breathing/pulse animation — if she animates properly, you know where she went. **No count badge** — the ghost controls already enumerate the active variables. |
| — | **Tempo contrast** | At least one beat runs **deliberately slow** to lag behind the others (currently **Back/Forward/Pin**, ~2.4s) — breaks the "synchronized robots" feel, reads more organic. |
| — | **Depth slider** | Dim by default (~38% opacity); lights up on rollover. |
| 8 | **Depth slider** | Appears on right rail. |
| 9 | **Map overlay** | Appears (instant for now). Pan/zoom to result region. |
| 10 | **Active filter chips** | Populate on map / in builder as variables resolve. |

**On dismiss:** same beats reverse, each at its own pace, back to resting map.

**DNA transfer:** Genie is the map page's chance to harmonize with the rest of the site. Name plate, city search, custom dropdowns, outlines/micro-colors, buttons, selected-variable chips/badges should translate from the chart/profile pages rather than feeling like a separate product. If selected variables sit at the top, use chart-page badge/chip DNA or another already-taught formatting grammar.

**Propagation:** v5 preserved for archaeology. **v6** is the active review surface (2026-06-12 pass 2): symmetric chrome slide-out, max-map (map fills behind dissolved bar), profile-grammar plate below controls with readable ghost outline, centered city search at ~62% blur, custom checkmark dropdowns, Share label morph (no display:none), Save FLIP travel button→disk, Genie stays visible longer into bottle, styled 2/3-width action buttons, pin fade on close, bolder zoom glyphs, ghost/slider hover-to-brighten.

### 5H. Overlay reveal — rain / virga (deferred, intent locked)

- **First render only:** "rain" effect — buys time for caching while dramatizing the honest discovery process (refining the chart to reveal hidden truth). Factually how charts render, slightly dramatized. **Amuse-bouche** to ready the user for map search — delightful, missable when gone, not constant entertainment.
- **Subsequent renders:** gentler animation — possibly overlays **rising from the earth** rather than descending from heavens. TBD in isolated study.
- **For now:** overlays appear instantly. Rain/virga study deferred to clean start (prior Cursor attempts failed).

---

## 6. Genie & Search UI (to formalize)

Genie is the variable-composition search interface (Map + Saved Searches filter).

### 6A. Language

- Variable types: Planet in House, Aspect to Angle, Angle in Sign, etc.
- Wording uses **·** or **/** between words (not “in” / “to”) where appropriate.
- User-expandable variable list via Settings (nodes, parts of fortune, custom orbs, etc.).

### 6B. Interaction model (locked in favorites study, propagate site-wide)

1. **First tier:** variable type selector.
2. **Second tier:** sub-fields appear based on first selection (cascade).
3. **Layout:** two rows stacked (not side-by-side) when space is tight.
4. **Popover:** second tier opens in **overlay popover** — must **not** push list content down.
5. **Search button** at end of filled cascade.
6. **Saved search default name:** auto from criteria (e.g. “Sun in 1st, Venus in 2nd, No Saturn in 1st”).

### 6C. Animation

Genie open/close, fade, and map fly-to are **motion-layer** concerns — governed by animation doctrine, not this doc. Structural contract: cascade logic and overlay behavior are independent of easing choices.

**Study:** `favorites_section.html` (genie popover in Saved Searches column)

---

## 7. Map Workspace (backlog)

The map has **not** been harmonized with the beta chart/comparison visual family. Active prototype: `map_CURRENT.html`.

### Known map debts

- Sidebar/control model still single-column prototype.
- Native dropdown bugs — click-through guard added; custom dropdown TBD.
- Popup aesthetics and favorite action wording inconsistent.
- Overlap color semantics and “candidate cart” not finalized.
- Rain/Virga discovery aesthetic deferred (`MICRO_INTERACTIONS` doctrine).
- Phase-C cache not wired to production map.
- Genie drawer not updated to match beta title plate / spacing / separator rules.

### Map harmonization pass (when scheduled)

1. Apply title plate + spacing + separator rules to map chrome.
2. Unify popup actions with button/link lexicon.
3. Custom dropdown for profile and Genie tiers.
4. Reconcile sidebar density with table density (lean B).
5. Revisit overlap colors after colorist pass.

---

## 8. Product Completion Roadmap (post-standardization)

After structural systems (#1–#10), color/typeface, and animation:

| Phase | Deliverable | Notes |
|-------|-------------|-------|
| **A. Propagation** | Apply locked table/separator/card rules to all beta pages | Chart, relocated, comparison, favorites |
| **B. Controls canon** | Formalize §5 into `#7 Button`, `#8 Link`, `#9 Hover` | Include custom dropdown component spec |
| **C. Color & type** | Professional colorist + L2/B1 refinement | Badges, glow, aspect colors, backgrounds |
| **D. Animation** | Human-scale hide/reveal, drawer direction, Genie motion | One direction family; no blitzkrieg |
| **E. Map pass** | Harmonize `map_CURRENT.html` with beta family | Genie + sidebar + popup |
| **F. Settings** | Chart display toggles, variable list, dignities, nodes, formatting prefs | Rules for retroactive vs future chart changes TBD |
| **G. Help handbook** | Professional + lay documentation | Linked from account menu |
| **H. Teaching overlays** | First-time use, chart entry overlay, feature discovery | Kindle-style restraint; dismissible |
| **I. Notes page** | Combined notes filesystem + full-screen scratch pad | Profile, comparison, and search notes — not profile-notes only |
| **J. Auth & integration** | Session, account, profile ownership, sync | Tie all surfaces together |
| **K. Family resemblance** | Final synthesis QA across all pages | Last |

---

## 9. Study File Index

| File | Purpose |
|------|---------|
| `validation/mockups/beta/index.html` | Entry point |
| `validation/mockups/beta/profile_standard.html` | Profile chart page |
| `validation/mockups/beta/relocated_standard.html` | Relocated chart page |
| `validation/mockups/beta/comparison_v5_beta.html` | Comparison (bottle layout) |
| `validation/mockups/beta/favorites_section.html` | Favorites / Saved functional prototype |
| `validation/mockups/beta/separator_study.html` | Separator options |
| `validation/mockups/beta/separator_calibrate.html` | Inset calibration |
| `validation/mockups/beta/table_format_study.html` | **Current table canon study** |
| `validation/mockups/beta/palette_study5.html` | L1–L4 live-with candidates |
| `validation/mockups/beta/badge_depill.html` | Badge shape direction |
| `validation/mockups/beta/distinct_texture_study.html` | Row texture (pinned) |
| `validation/mockups/beta/planet_gender_color_study.html` | Deliberate bias variant (optional) |
| `validation/mockups/beta/open_questions_board.html` | Controls/table/policy decision board (answered 2026-06-12) |
| `map_SANDBOX_genie_v5.html` | Genie v5 archaeology checkpoint |
| `map_SANDBOX_genie_v6.html` | **Current Genie harmonization / teaching-motion study** |

---

## 10. Open Questions (remaining)

| # | Question | Status |
|---|----------|--------|
| ~~1~~ | Fixed row unit vs 13-slot block | ✅ **Fixed row unit** (B2) |
| ~~2~~ | A2A 13 vs 11 units | ✅ **Keep 13** for Fibonacci alignment (B1); may revisit |
| ~~3~~ | Whitespace before Notes | ✅ **None extra** — grid gap only (B3) |
| ~~4~~ | Custom dropdown scope | ✅ **Selective custom** (C4) — Genie, saved search, profile select, relocated city; account menu too |
| ~~5~~ | Nodes in default tables | ✅ **Off in tables for now** — chart wheel only; settings later (C1) |
| ~~6~~ | Trop·Plac settings change | ✅ **Ask each time** (C2) — too big to apply silently |
| ~~7~~ | Comparison name-plate scroll | ✅ **Yes** — plate descends into city-bar gap; may shrink in corner during animation (C3) |
| ~~8~~ | Border/glow hue | ✅ **Per-table signature** at ~4% interior + G3 grey depth (C5) |

**Still open (non-board):** table-hide chip label (`AA` vs glyph); animation timing pass (map Genie + carousel + note); D2 component build; comparison G3 propagation; professional colorist intensity pass; nodes on wheel default vs settings-only.

**Pending features to build & test soon (data/backend, flagged by user):**
1. **City search with full disambiguation** — full-length place names (city, region, country) shown to disambiguate; abbreviation only inside compact dropdowns. Needs install/test soon.
2. **Timezone history** — historical timezone/DST resolution for accurate birth-time→UTC. Pairs with the city-search build.

---

## 11. Related Documents

| Document | Relationship |
|----------|--------------|
| `docs/product/INTERFACE_AND_DESIGN_CANON.md` | Parent design constitution |
| `docs/bootstrap/PROJECT_BOOTSTRAP_CANON_v1_2026-06-02.md` | Onboarding; should reference this file |
| `docs/design/control_and_action_doctrine_audit.md` | Button/action archaeology |
| `docs/design/plate_doctrine.md` | Title plate archaeology |
| `docs/MICRO_INTERACTIONS_AND_EMOTIONAL_MOVEMENT_DOCTRINE.md` | Motion philosophy |
| `docs/product/FUTURE_FEATURES_ROADMAP.md` | Long-horizon features |
| `ai_context/current_state.md` | Engineering snapshot |

---

## 12. Revision Log

| Date | Change |
|------|--------|
| 2026-06-12 | v1 created. Locked separator (~80%) and table (~85%) systems. Documented 34-unit grid, formats, G3+inner glow, controls/genie/map/roadmap backlog. |
| 2026-06-12 | Ratified in `table_format_study.html`: table order **AiS · PiH · A2A**; titles **flush left**; AiS centered on the **sign word**; heavy-table border **G3 (mono-depth grey) + inner glow ~4%** (G1 rejected as too much border, neon/edge "TRON" rejected); vertical **row unit ~21px (Fib)**; double-border red rejected (grey + 5–15% hue only). OQ#1 (fixed row unit vs 13-slot block) and OQ#2 (A2A 13 vs 11) remain open pending the full-page layout. |
| 2026-06-12 | **Propagation pass.** Fixed a JS syntax error (unescaped quotes in the Dignities-toggle `onchange`) that was blanking the wheel + tables on `profile_standard.html` and `relocated_standard.html`. Applied to both chart pages: clean **8fr·8fr·13fr·5fr** grid and **AiS word-centering** (deg left / sign centered / min right). Comparison verified rendering in bottled v5_beta state. Color-layer items (inner glow, G3, white skin) intentionally not applied yet. |
| 2026-06-12 | **Decision board locked.** D2 · H1+ (stub-only collapse) · C3 · S1 · B1(13) · B2(fixed) · B3(none) · C1(nodes off tables) · C2(ask) · C3(scroll yes) · C4(selective custom) · C5(G3+4% sig glow). Applied G3+glow + collapse stub + lines-only + dignities footer to chart pages. Controls §5 promoted to ~85% locked. |
| 2026-06-12 | **Dropdown + motion direction.** Active indicator **checkmark** (accent-line rejected). Genie **no search** ever — compact rows keep all bodies visible. City names abbreviate in dropdowns; full names → dedicated city-search (pending). Motion §5F added: functional/human-paced, no acceleration/overshoot, subtract color; table-hide chip drifts into caret (label `AA`/glyph TBD, no "A2A"); note pop-out = mini word processor; carousel = one calm uniform slide; rain/virga overlay deferred clean-start. Flagged pending features: city-search disambiguation + timezone history. |

---

*End of UI_STANDARDIZATION_CANON_v1_2026-06-12*
