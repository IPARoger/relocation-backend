# HELP-0: Help / Course / Onboarding Doctrine Map

**Date:** 2026-06-20
**Type:** Doctrine + content map — no implementation authorized
**Read budget:** results/124, results/132, results/135

---

## 1. Onboarding Genie Preload Doctrine

### Rule

The first map walkthrough **must not open on an empty map.**

Three Genie variables must be preloaded before the user sees the map for the first time. These variables are **calculated dynamically from the user's chart** — they are not hard-coded example conditions.

### Calculation goal

The system searches for a set of ≥3 variables that:

1. Produce **at least 1 overlap region** anywhere on the world map.
2. Ideally produce **2 or more overlapping regions** so the first impression immediately demonstrates why intersection matters.

An overlap region is where two or more active overlays coincide — the product's core analytical unit.

### "Buy time" window

The profile nameplate / caret teaching step (Step 1 of the walkthrough) introduces the idea of profile ownership. This step requires no map interaction and takes ~10–15 seconds of user attention.

**The system should use this window to calculate candidate preload variable sets in the background**, so by the time the user reaches the Genie step (Step 2), the map is already populated with meaningful overlapping overlays.

### Fallback

If no 2-overlap set is found within the allotted window, fall back to a 1-overlap set. If no overlap set is found at all, use the 3 highest-confidence single conditions for the chart and proceed — an empty map is never acceptable.

### Implementation note (deferred)

This calculation belongs to a future **preload service** or **Genie bootstrap path**. It is not part of ONBOARDING-2A1 (framework only) or MAP-UX-1 (nameplate only). It is scoped as a later slice, likely **ONBOARDING-2C** or **GENIE-BOOT-1**.

---

## 2. Tutorial Purpose

### What the initial map walkthrough teaches

The walkthrough is map-only. It teaches **novel interactions** a first-time user cannot infer from the map chrome:

| Step | Topic |
|------|-------|
| 1 | Profile selector / nameplate caret — profile context and ownership |
| 2 | Genie variable builder — adding conditions |
| 3 | Current-location popup (right-click / long-press) |
| 4 | Mute / Solo / Not ghost tools |
| 5 | Pin |
| 6 | History (`<>`) |
| 7 | Save Search |
| 8 | Map Notes *(optional)* |

### What the walkthrough does NOT teach

The walkthrough deliberately skips:

- The full research workflow
- Favorites
- Comparison workspace
- Settings
- Profile management
- A2A (aspect-to-angle) tables
- Dignities / PIH tables
- City Intelligence
- Astro Assist

These are taught contextually when the user reaches them, or via the longer courses described below.

---

## 3. "How to Get the Most Out of This App" — Research Workflow Course

**Audience:** Users who have completed intake and the map walkthrough and want to understand the research methodology.

**Format:** Text-based Help article (or short video). Not a modal tour.

### Outline

**A. Start with intentions**
Define what you are optimizing for in a new location: career, relationship, health, creativity, community — or some combination. These intentions shape which astrological conditions to search for.

**B. Translate intentions into astrology conditions**
Use Genie to select conditions that correspond to your intentions. Each variable is a chart condition (body, aspect, angle, sign). You do not need to cover everything — start with 2–4 meaningful conditions.

**C. Select overlays in Genie**
Each variable generates an overlay region on the map. Different conditions produce different geometry. The map shows where each condition is strong.

**D. Look for intersections of desired traits**
Overlapping regions are where multiple conditions are simultaneously strong. These are your primary candidates. The intersection is the product's core signal.

**E. Look for outer/non-overlap regions for undesired traits**
If a condition represents something you wish to minimize (Mute / Not), areas where that overlay is present but others are not become exclusion zones.

**F. Use A2A to refine within a region**
Once a promising region appears, open the Aspect-to-Angle (A2A) table to evaluate precise angular relationships at specific cities. A2A is more granular than the map overlay geometry.

**G. Open tables to evaluate tradeoffs**
Use comparison tables to assess planetary positions, house placements, and aspect patterns across candidate cities. No scoring — the tables present facts, you weigh them.

**H. Use Diffs when nearby locations are similar**
When two cities look similar on the map and tables, use the Diffs surface to isolate the specific astrological differences between them. Diffs are useful for fine-grained discrimination.

**I. Use Astro Assist as an aid, not an authority**
Astro Assist can explain conditions, summarize patterns, and surface things you might miss. It does not score or rank locations. The researcher decides.

**J. Open City Intelligence for non-astrological context**
City Intelligence surfaces practical, non-astrological data (cost of living, climate, demographics, walkability, etc.). This information complements the astrological picture — it does not replace it.

**K. Decide, save, compare, note, revise**
Save searches to return to them. Use Chart Record to compare saved states. Add Map Notes to document your thinking. Revisit as your intentions evolve.

---

## 4. Newbie AIS Course (Beginner Entry Point)

**Audience:** Users new to relocation astrology who find Genie and map overlays overwhelming.

**AIS = Astro Interpretive Summary** — the easiest, most familiar surface.

**Goal:** Let beginners start with reading about their chart at a specific city before they engage with the map. AIS is recognizable (like a natal chart reading) and requires no explanation of overlays.

### Outline

**Module 1 — What is Relocation Astrology?**
Brief conceptual frame: moving does not change your natal chart, but it changes how planets align to local angles. Different cities = different local angles = different lived experience.

No jargon yet. No math. No overlays.

**Module 2 — Your AIS: What You See**
Walk the user through the AIS output for their birth city.

- Planets in houses (simplified: what energy is active in what area of life)
- Key aspects (angular relationships — approached descriptively)
- No emphasis on orbs, no raw math

**Module 3 — Try a New City**
Prompt the user to enter a city they are curious about. Show side-by-side AIS or a Diffs summary. Ask: does anything shift in a direction you want?

**Module 4 — Comparison Tables (intro)**
Now introduce the comparison table view. Show that the numbers they've been reading in AIS have underlying positions. Let them see a few rows.

Reinforce: no scores, no "best." These are positions, not rankings.

**Module 5 — What is a Strong Placement?**
Optional: introduce signs, angles (ASC/MC/DSC/IC), and aspects in plain language. Reference the Methodology section for users who want depth.

**Module 6 — When You're Ready: The Map**
After AIS and table familiarity, invite the user to try the map. At this point, Genie variables are less abstract because the user already knows what conditions they are interested in from the AIS/table work.

---

## 5. Help / Methodology Section Structure

Proposed top-level navigation for the Help surface:

```
Help
├── Getting Started
│   ├── Setting up your profile
│   ├── Your first map search
│   └── What the overlays mean
├── Map Walkthrough (replay trigger)
├── How to Use This App
│   └── Research Workflow (§3 above)
├── New to Relocation Astrology
│   └── AIS Beginner Course (§4 above)
├── Methodology & Doctrine
│   ├── No scoring / no "best city"
│   ├── Layer 1 vs Layer 2
│   ├── Geometry vs interpretation
│   ├── Dignities as optional metadata
│   ├── Retrograde, house-edge, A/S philosophy
│   └── AI assistance philosophy
├── Settings & Display Choices
│   ├── Orb configuration
│   ├── House systems
│   └── Appearance
├── Notes Library
│   └── How to use Map Notes and Chart Record
└── Troubleshooting
    ├── Map not loading
    ├── Profile / chart issues
    └── Contact / feedback
```

---

## 6. Methodology / Doctrine Explanation Pages

Each page is a short, plain-language explanation (300–600 words). These are referenced from the Methodology section in Help and from tooltips/info icons in the Settings and display surfaces.

### Topics

**a. No scoring / no "best city" ranking**
Why the app presents facts rather than scores. What would be wrong with a ranked output. How the researcher's intentions and values determine what "best" means — something the system cannot know.

**b. Layer 1 vs Layer 2**
Layer 1 = geometric chart facts (positions, angles, aspects, directions). Layer 2 = interpretive ontology (traditional rulerships, dignities, exaltations, interpretive hints). The app separates these. Layer 1 is non-negotiable. Layer 2 is optional metadata.

**c. Geometry vs interpretation**
The map shows geometry — where conditions are strong based on angular relationships to the horizon and meridian. The interpretation of what that means for a specific person is the researcher's domain.

**d. Dignities as optional PIH metadata**
Essential dignities (domicile, exaltation, detriment, fall) are Layer 2. They are available as optional display metadata in the PIH table, not as a scoring layer. Why: traditional dignity systems encode one ontological perspective; the app must remain neutral across traditions.

**e. Retrograde / house-edge / applying-separating philosophy**
Why retrograde is a Layer-1 fact (not interpretive). Why house-edge logic must be direction-aware. Why applying/separating is shown as blue/red without intensity gradients. Reference: `docs/doctrine/ASTROLOGY_CALCULATION_DOCTRINE.md`.

**f. Why A/S is blue/red only — no intensity gradient**
Blue = applying, red = separating. Intensity gradients would imply scoring. The app shows the direction of motion as a fact; the researcher decides what weight to assign it.

**g. Why station edge cases are conservative**
If a planet is near a house boundary but approaching station, the app does not project whether it crosses the boundary. It shows current motion. Conservative default prevents false precision.

**h. Why City Intelligence is non-astrological**
City Intelligence provides practical context (cost of living, climate, etc.) without mixing it into the astrological analysis. The two layers inform each other but do not score against each other.

**i. Why AI assistance should explain, not decide**
Astro Assist summarizes and explains. It surfaces things you might miss. It does not produce rankings, recommendations, or scores. The researcher holds the judgment function.

---

## 7. Acceptance Criteria for Future Implementation

| Criterion | Note |
|-----------|------|
| Preloaded Genie variables use chart-specific logic, not hard-coded examples | Required for walkthrough |
| Preload calculation runs during the nameplate/caret teaching step | Buy-time window |
| Initial walkthrough is ≤8 steps | Short; no scope creep |
| Feature teaching (walkthrough) is separate from research methodology (course) | Help structure enforces this |
| Methodology doctrine pages are discoverable from Settings info icons | Not buried in Help |
| No "best city" language ever appears in the product | Hard constraint |
| Help does not become a full modal tour | Single-surface replay only |
| AIS course is accessible without completing map walkthrough | Independent entry point |

---

## Related files

| File | Role |
|------|------|
| `results/124_onboarding_map_walkthrough_doctrine_correction.md` | Canonical walkthrough doctrine |
| `results/132_onboarding2a_map_walkthrough_execution_plan.md` | Implementation plan for ONBOARDING-2A |
| `results/135_map_ux_source_truth_audit.md` | Map UX source truth |
| `docs/doctrine/RELOCATION_METHODOLOGY_DOCTRINE.md` | Full product philosophy (PHILOSOPHY-0) |
| `docs/doctrine/ASTROLOGY_CALCULATION_DOCTRINE.md` | Layer-1 calculation facts doctrine |
