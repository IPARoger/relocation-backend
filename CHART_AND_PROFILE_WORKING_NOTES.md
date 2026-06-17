# Chart & Profile — Working Notes + Transfer Doc

Purpose: a single low-cost handoff file so a NEW chat (e.g. the genie work) can start
without re-reading the whole project, docs, or past transcripts.

> If you are an AI reading this in a fresh chat: **Do NOT re-read `docs/`, source code,
> or prior chat history.** Read ONLY this file plus the one prototype file named below.
> That keeps cost at ~$0.50–$1/prompt instead of $2–$4.

---

## 1. Current canonical files

- **Profile page (latest):** `prototype_profile_workspace_v11.html`
- Chart wheel (latest standalone): `prototype_chart_wheel_holistic_v09.html`
- Everything is plain static HTML/CSS/vanilla JS. **No frameworks, no deps, no build.**
- Iterate by saving a new version number (v12, v13…). Do not overwrite older versions.

## 2. Emotional / design target (do not drift from this)

- Relocation astrology **instrument**, not a mystical performance.
- Calm, capable, serious, exploratory, long-lived. Beauty is quiet, discovered over time.
- Color **differentiates** more than it attracts. No purple cosmic gradients, no Harry-Potter
  parchment, no DMV/SaaS coldness. Map = optimistic/exploratory; Profile = "knuckle down,
  but still enthused." The two must feel related, not identical.
- Paper currently "warm sand" (`--paper:#f4ecdc`). It is **more inviting** but NOT final.
  Open task: work backward from the desired emotional state ("warm, compressed, fiery
  excitement" or similar) before locking the final color.

## 3. Chart wheel — locked structure (v09 doctrine)

- Rings (outer→in): bold outer ring → thin zodiac inner ring → sign band between them →
  planet ring → **aspect ring** (aspect lines terminate here, astro.com style) → tiny inner core.
- Sign dividers every 30°; 5° ticks (subtler, ~1/3 smaller than 10°).
- Placidus-style unequal houses; house numbers normal weight, near each house's mid-arc.
- House cusps go to the inner core but must NOT cross the sign band or pierce planets.
- Greyscale hierarchy is real (charcoal ink → mid grey cusps → light ticks).
- Subtle inner glow (gold) rising from center; confined, not a cosmic halo.
- Home chart = gold anchor; Guest/relocated chart = teal anchor (very subtle, ~80% grey mix).
- Supersample + `shape-rendering="geometricPrecision"` to avoid wobbly thin lines.
- Planet/sign glyphs are **placeholders** — real glyphs to be supplied later.
- Degrees/minutes on the wheel: parked (hero wheel currently omits them; fine for now).

## 4. Profile page — decisions locked through v11

- Header: account owner (David Goodman) dropdown top-right; main menu in header
  (View Map, Profile, Comparison, Transit Lab, Store, Help, Settings).
- View pills: **Natal · Current Location · Comparison**. Transitions slide **horizontally**
  (carousel feel), never fold/origami. Comparison's 2nd chart slides in horizontally.
- Birth/profile plate: Name (dropdown to switch profiles) + Edit + "+". Hierarchy = Name >
  date/time > place; lat/lon + UTC + Tropical/Placidus subordinated in grey.
  lat/lon on ONE line, 2 decimals. 2nd chart in comparison shows only a minimal "Current
  location" block (no duplicated birth data).
- Charts are the hero; can be enlarged via popup. Popup is **larger than the hero** and
  carries a consolidated head (name + birth date/time/place; no UTC/lat-lon).
- Reference tables:
  - **Planet in House:** 2 cols (Planet | House). House centered next to planet (not flush
    right). Numbers normal weight. Use "5" not "5th".
  - **Angle in Sign:** 2 cols (Angle | Position = "26° Cap 19'", signs abbreviated).
    Title BOLD/strong; ASC/DSC/MC/IC line labels normal weight.
  - **Aspect to Angle (A2A):** fixed planet column (incl. ASC, MC as "planets") + a single
    sliding track. Pills/columns order = **ASC · DSC · MC · IC · All**. All five frames slide
    with the SAME rhythm (one 5-frame track; no re-render jump). Single-angle values are
    centered. Empty aspects show "·". Abbreviations: Conj, Sq, Tri, Opp, Sext. One space
    between abbreviation and orb. Applying = terracotta, Separating = teal on the orb
    (subtler later). No A/S legend.
- Single-chart mode layout: PiH | Angle-in-Sign (narrow, middle) | A2A, so the row fills width.
- All boxes in a row are forced to **equal depth**.
- Dividers: a line between wheel and tables; more defined separators in saved lists.
- Lower section: Favorites (dominant) + Saved Comparisons + Saved Searches. Favorites has
  city add/autocomplete, star, hover-trash, and a Compare button that activates at 2–5 cities
  (natal + current are the first two by default). City names link to a chart popup. Saved items
  have a discreet "notes" link.

## 5. OPEN / PARKED questions (carry forward, don't lose)

- Final paper color + overall site palette (warm sand vs. cloud grey vs. greige). Decide via
  target emotion, and coordinate with the Map page palette so Profile ↔ Map feel related.
- Final glyphs (planets + signs) — user supplying.
- Inner glow vs. outer aura: subtle home/guest distinction (gold soul / cool exterior). Tune later.
- Wheel degrees/minutes rendering on the live page.
- A/S colors: may go more subtle later.
- Single-mode wheel still leaves some empty space to its right — revisit (maybe summary content
  there).
- Comparison PAGE (separate from the comparison VIEW here): planned layout is category-as-card
  with cities as columns — e.g. Planet | House(Boston) | House(Philly) | House(Bali) — with chart
  popups on hover. A2A formatting across many cities is the hard part. NOT built yet.
- Fonts: keep moving away from cold SaaS sans; serif (Iowan/Palatino) for headings is working.

## 6. Cost control protocol (IMPORTANT)

- Each new chat should be told explicitly: "Do not re-read docs or chat history; only read
  `CHART_AND_PROFILE_WORKING_NOTES.md` and `<the one file we're editing>`."
- Prefer one fresh chat per major surface (Profile / Map control panel / Comparison page /
  Settings) seeded by this doc, rather than one giant ballooning chat.
- Give batched, numbered notes (like the v11 list) instead of many small prompts.

## 7. Genie variable doctrine (for the genie / variable-builder chat)

This is the doctrine the genie (variable builder + AI search layer) must obey. It is the
same instrument feel as sections 2–4: calm, capable, exploratory. Genie must NOT become a
Photoshop panel, a layer manager, or an enterprise control wall.

**Core stance**
- The user thinks in **astrology, not UI**. The interface conforms to the user's mental
  model ("I want Sun in 1st"), never the reverse. Bad: Add Rule → Category → Subcategory →
  Operator → Condition → Advanced → Confirm. Good: "I want Sun in 1st."
- The **map is the main thing**. Variables are temporary instructions you hand to the map —
  not a form whose output area happens to be a map.
- Genie **disappears psychologically** once the search is running. Attention moves from
  "How am I configuring this?" to "What does the world look like now?" (the deepest principle).

**Primary action**
- The most important button is **Add Variable** — not Filters / Settings / Advanced /
  Layer Manager. Everything begins with Add Variable. The builder appears only when pressed,
  then retreats. Default state is small.

**Creation is sequential / progressive disclosure**
- Reveal only the *next* decision, never a wall of controls.
- Add Variable → choose category (Planet in House, Aspect to Angle, Angle in Sign,
  Planet to Planet, Transit, …) → choose the specific condition (e.g. Planet → House:
  Sun → 1st) → Add.
- **One variable at a time.** Build, Add, see it appear; build next. This rhythm matters;
  the user is not building 12 variables simultaneously.
- **Shallow depth only** (max ~2 levels: Planet in House → Sun → 1st). No nested dropdown
  mazes.
- **Wide chooser-panel dropdowns** — readable without horizontal scrolling, not a 2004
  browser select box.
- Beginners need only Planet + House. Orb / aspect family / minor aspects / custom weighting
  appear **later**, not up front.

**Variables become chips/tokens (the chips ARE the search)**
- After creation each variable is a discrete visible object:
  `[ Sun in 1st ] [ Venus in 7th ] [ NOT Saturn in 12th ] [ Jupiter trine MC ]`.
- The user thinks "I am searching for these things," not "I have settings selected."
- Dropdowns **collapse behind the chip** after creation (do not stay permanently open).
- **Order of creation is preserved** — it helps the user remember how they arrived here.
- Clicking a chip exposes **Edit / Duplicate / Remove / Mute** (Solo later). The chip is the
  control surface — not a giant settings panel.

**NOT is a variable type, created at creation time** (NOT a separate later exclusion system)
- In the creation flow: `○ Include  ● Exclude (NOT)`. `NOT Saturn in 12th` is built through
  the exact same workflow as `Sun in 1st`.
- Workflow still encourages desired-first: add desired conditions → explore → add NOT
  variables → refine → compare locations. But NOT is first-class, same builder, not a
  bolted-on filter stage.

**Mute / Solo — temporary inspection tools layered on chips**
- **Mute** = temporarily remove a variable from rendering *without deleting it* (stored,
  inactive).
- **Solo** = temporarily isolate one variable; everything else disappears temporarily
  (good for inspecting overlap / crowded searches).
- **NOT ≠ Mute ≠ Solo** and must never be conflated: NOT = search for *absence*;
  Mute = temporarily *disable*; Solo = temporarily *isolate*.

**Genie retreat / miniature state — Micro 77, variable persistence**
- When Genie collapses, variables stay visible in a **miniature strip**:
  `[ Sun in 1st ] [ Venus in 7th ] [ NOT Saturn in 12th ]`.
- Include / NOT / Mute / Solo states must stay **legible in miniature**. Lightweight controls
  (Mute, Solo, Edit, Remove) are available from the strip without reopening the full panel.
- Genie may disappear; **search intent may not.** The search stays legible after the builder
  is gone.

**Search language (future, not now)**
- Moving toward natural phrasing ("I want visibility and relationship") *alongside* technical
  ("Sun in 1st + Venus in 7th"). Support both; force neither AI nor technical language.

**Emotional sequence to design for:** Curiosity → Selection → Discovery → Refinement →
Comparison. NOT Configuration → Configuration → Configuration → Map.

## 8. Recommended genie handoff — COPY-PASTE STARTER

Start a NEW chat and paste everything between the lines below as your first message.
Replace the `<<< PASTE YOUR GENIE NOTES HERE >>>` slot with your notes.

------------------------------------------------------------------------
COST RULE: Read ONLY these two files — `CHART_AND_PROFILE_WORKING_NOTES.md`
and `prototype_profile_workspace_v11.html`. Do NOT read any other docs,
source code, or past chat history. Do not search the repo. Do not re-derive
context you don't need.

TASK: Set up the "genie" (the variable builder + AI voice/assistant layer).
Coordinate its language, tone, and behavior with the design doctrine in
sections 2–4 of `CHART_AND_PROFILE_WORKING_NOTES.md` (calm, capable,
exploratory instrument — not a mystical performance; quiet beauty; welcomes
beginners without patronizing them), AND obey the Genie variable doctrine in
section 7 (Add Variable is the primary action; sequential creation; chips are
the search; NOT is a variable type created at creation; Mute/Solo are temporary
inspection tools; the map is the main thing; Genie retreats but the search
stays legible).

Keep responses tight. Ask me before expanding scope.

GENIE SETUP NOTES:
See section 7 ("Genie variable doctrine") of
`CHART_AND_PROFILE_WORKING_NOTES.md`. Add any further specifics below.
------------------------------------------------------------------------

That chat stays cheap because the context is tiny — just these two files.

---
_Last updated for v11 of the profile prototype._
