# Control & Action Doctrine Audit

Status: provisional audit (Phase 2.8E)
Type: archaeology / doctrine only — no code, prototype, component, or commit changes
Scope: actions, controls, ownership, authority, semantics

Out of scope (deferred to later phases): colors, typography, spacing, glow,
shadows, animation/hover/easing.

Builds on: Plate Doctrine (2.8C), Badge & Metadata Doctrine (2.8D).
The Action-language tension (Add/Edit/Change) opened in 2.8D §6a is carried
forward here.

Files audited:
`map_CURRENT.html`, `prototype_profile_workspace_v11.html`,
`prototype_relocated_location_v1.html`, `comparison_v2.html`–`v5.html`,
`city_profile_v1.html`–`v4.html`, `app_shell.html`.

---

## 1. Action Inventory

Every user action, its page(s), target object, trigger control, current wording,
and whether the wording is correct.

| Action | Page(s) | Target object | Trigger control | Current wording | Wording correct? |
|---|---|---|---|---|---|
| Change Profile | profile v11, relocated v1, map | profile (active lens) | `.profile-select` button / `#chartProfile` select / `#profileSelect` | name + caret (no verb); map = native select | Implicit; should read as "Change Profile" |
| Edit Profile / Birth Data | profile v11 (`.linkbtn` "Edit"), comparison v3–v5 (`.profile-btn` "Edit"), app_shell ("Edit birth data") | profile birth data | link button / button | "Edit" / "Edit birth data" | OK (modify existing) |
| Add Profile | profile v11 (`.linkbtn.plus` "+"), comparison v3–v5 (`.profile-btn` "Add") | new profile | icon/button | "+" / "Add" | Ambiguous ("+" unlabeled; "Add" lacks object) |
| Add Favorite | map popup (`.popup-action-favorite`), profile v11 (Add City → favorite), relocated v1 (`.fav-btn`) | favorite_place | button | "Favorite" / "Add to Favorites" / typeahead "Add 'X'" | Inconsistent (3 wordings for one action) |
| Remove / Archive Favorite | profile v11 (`.trash` "Remove"), map (archive API) | favorite_place | trash button | "Remove" (title); archives via API | Mislabeled: "Remove" performs Archive |
| Show favorite status | map ("Favorited ✓"), relocated v1 (`.fav-btn.on` "Favorited" + ★), profile v11 (`.star.on`) | favorite_place | button/star | "Favorited" / ★ | Status fused into action control (hybrid) |
| Open Chart | map popup ("Open chart"), app_shell ("Open full chart", "Full chart", "View chart") | relocated chart page | button | "Open chart" / "Full chart" / "View chart" | Inconsistent (Open vs View vs Full) |
| Open / Enlarge Wheel | profile v11, relocated v1 (`data-act=popout` `.popout` "⤢ Enlarge") | chart wheel modal | disc click | "⤢ Enlarge" | OK |
| Open City Intelligence | relocated v1 (`.intel-open` "Open Full City Intelligence", disabled), comparison (`.ci-open-btn`, `.cc-info` "i"), comparison v2 popup ("Open full city page →") | city intelligence page | button/link | several | Inconsistent (Open / "i" / "→") |
| Open Chart Library | map (`#libraryOpenLink`) | external library page | link | "Open Chart Library" | OK |
| Compare Cities | profile v11 (`.compare-btn` "Compare (n)"), app_shell ("Compare places", "Add to comparison") | comparison set | button | "Compare (n)" / "Add to comparison" | OK-ish; "Add to comparison" is Create |
| Save Search / View | map (`#saveCurrentViewBtn` "Save current view to library"), profile v11 (Saved Searches list) | saved search | button/list | "Save current view to library" | Verbose but OK |
| Save Notes | relocated v1, comparison v3–v5 (`.notes-save` "Save") | note record | button | "Save" | OK |
| Edit / Open Notes | profile v11 (`.notes-link` "notes" → modal), comparison v3–v5 (`.notes-toggle-btn` "✎ Notes" → disclosure), relocated v1 (inline composer) | note record | link / toggle / inline | "notes" / "✎ Notes" | Inconsistent entry pattern (3 models) |
| Hide / Restore comparison city | comparison v3–v5 (`.cc` "Hide", `.stub-restore` "Restore"), comparison v2 (`.city-ctrl` "Hide") | comparison column | button | "Hide" / "Restore" | OK (transient visibility, not archive) |
| Reorder comparison city | comparison v3–v5 (`.cc-arr` ‹ ›), comparison v2 ("Reorder" future) | comparison column order | arrow buttons | ‹ › (no label) | OK as icons; v2 stub mislabeled future |
| Replace comparison city | comparison v3–v5 (`.cc-rep` "Replace" → picker), comparison v2 ("Replace" future) | comparison column place | button → modal | "Replace" | OK (switch place in slot) |
| Add comparison city | comparison v3–v5 (`.add-city-btn` "+ Add" → picker) | new comparison place | button → modal | "+ Add" | Ambiguous (lacks object) |
| Change Currency | city_profile v2/v4 (`.curr-btn` Local/USD/Home + `.curr-home-change` "(Change)") | active currency view | pill buttons + link | "Local/USD/Home" + "(Change)" | OK (switch context) |
| Change Home Currency | city_profile v2/v4 (`.curr-home-change` → modal) | home currency setting | link → modal | "(Change)" | OK |
| Change Weather Unit | city_profile v1–v4 (`.wt-btn` F°/C°) | weather unit view | toggle buttons | "F° / C°" | OK |
| Change Citizenship | city_profile v2/v4 (`.visa-change` "Change Citizenship" → modal) | visa citizenship context | button → modal | "Change Citizenship" | OK (exemplary verb+object) |
| Change Intentions | city_profile v4 (`.intentions-change` "[Change]", disabled) | stated intentions | button | "[Change]" | OK (future) |
| Change Language detail | city_profile (lang change link) | language reference | link | "change" | Minor |
| View map / navigate sections | all (`.mainmenu a`, `.nav-links a`) | route | link | "View Map" / "Map" / "Compare" | Inconsistent ("View Map" vs "Map") |
| Back / Back to Top | city profiles (`.back-link` "← Back", `.back-to-top`) | previous route / top | link | "← Back" / "↑ Back to Top" | OK |
| Account menu | profile v11 (`.account-btn` + menu: Account/Billing/Sign out) | account | button + menu | name + ▾ | OK |
| Switch view (Natal/Current/Comparison) | profile v11 (`.chip` view pills) | active chart view | pills | "Natal / Current Location / Comparison" | OK (context switch) |
| Switch angle (ASC/DSC/MC/IC/All) | profile v11 + relocated v1 (`.apill`), comparison v3–v5 (`.angle-tab`) | A2A table angle | pills / tabs | angle names | OK; two control metaphors |
| Expand/collapse section | comparison v2–v5 (`.block-header` toggle), city profiles (`.acc-trigger`) | content section | disclosure | arrow/chevron | OK; two metaphors |
| Find regions | map (`#findBtn` "Find regions") | map search result | button | "Find regions" | OK |
| Save current view | map (`#saveCurrentViewBtn`) | library entry | button | as above | OK |
| Map condition builders | map (`#planetA`, `#houseA`, `#angleSign*`, `#overlay*`) | query parameters | native selects | n/a | OK (functional) |
| Inspect point / Open popup | map (right-click), app_shell ("Inspect point") | location popup | map gesture / button | n/a / "Inspect point" | OK |
| Export (entry/viewport/chart/comparison/PNG) | app_shell | export artifact | buttons | "Export …" | OK (scaffold) |
| Resume exploration | app_shell ("Resume → Map") | saved exploration | button | "Resume → Map" | OK (scaffold) |
| Toggle drawer (Genie) | app_shell ("Expand/Collapse") | drawer | button | "Expand drawer"/"Collapse" | OK |
| New Chart Record | app_shell ("+ New Chart Record", disabled) | chart record | button | "+ New Chart Record" | Scaffold vocabulary |

---

## 2. Action Classification

Every action mapped to one class.

### Create (creates or attaches a new object)
- Add Favorite (map popup, profile Add City, relocated Add to Favorites)
- Add Profile ("+" / "Add")
- Add Comparison City ("+ Add")
- Add to Comparison (app_shell)
- Save Search / Save current view to library
- Save Notes (first save of a note record)
- New Chart Record (app_shell, disabled)

### Modify (changes contents of an existing object)
- Edit Profile / Edit Birth Data
- Edit Notes (and re-Save)
- Change Citizenship contents (visa context edit)
- Map condition builders (edit query object)

### Switch Context (changes active selection — no object created/destroyed)
- Change Profile (profile/relocated/map)
- Switch View (Natal / Current Location / Comparison)
- Switch Angle (ASC/DSC/MC/IC/All)
- Change Currency / Change Home Currency
- Change Weather Unit
- Replace Comparison City (switch place in slot)
- Reorder Comparison City
- Hide / Restore Comparison City (visibility toggle)

### Navigate (moves the user elsewhere)
- Open Chart / View Chart / Full Chart (→ relocated chart page)
- Open / Enlarge Wheel (→ modal)
- Open City Intelligence ("i" / "Open Full City Intelligence" / "→")
- Open Chart Library
- View Map / nav links
- Back / Back to Top
- Resume → Map (app_shell)
- Inspect point → popup
- Export … (app_shell)

### Archive / Remove (removes or hides an object)
- Archive Favorite (currently labeled "Remove")
- Remove from list (`.trash`) — semantically Archive in profile favorites
- Hide Comparison City (transient, not destructive — borderline; classified Switch Context above, listed here for visibility)

Classification conflict flagged: **Hide** (visibility) vs **Archive** (lifecycle)
vs **Remove** (destructive) are not cleanly separated; the profile `.trash`
"Remove" actually archives.

---

## 3. Control Inventory

Every control type, pages, current variants, purpose, ownership.

| Control type | Pages | Current variants | Purpose | Ownership |
|---|---|---|---|---|
| Profile selector | profile v11 (`.profile-select`), relocated v1 (`#profileSelect`), map (`#chartProfile` native), comparison (`.profile-name` static + `.nav-account`) | serif name+caret / header button / native select / static text | switch governing profile | Profile (authority) |
| Account control | profile v11 (`.account-btn` + menu), comparison/city (`.nav-account` static text) | dropdown menu / static | account scope | Account |
| Primary buttons | all | `.btn`, `button.primary`, `#findBtn`, `#saveCurrentViewBtn`, `.fav-btn`, `.compare-btn`, `.modal-btn` | perform actions | varies by target |
| Link buttons | profile v11 (`.linkbtn`), city (`.visa-change`, `.curr-home-change`, `.lang-change`), comparison (`.notes-toggle-btn`) | text/underline links acting as buttons | lightweight actions | varies |
| Nav links | all (`.mainmenu a`, `.nav-links a`, `.back-link`, `.back-to-top`) | header nav / breadcrumb / back | navigation | route |
| View pills | profile v11 (`.view-pills .chip`) | warm pill track | switch chart view | Profile page |
| Angle pills/tabs | profile v11 + relocated v1 (`.apill`), comparison v3–v5 (`.angle-tab`) | carousel pills vs underline tabs | switch A2A angle | chart table |
| Currency/weather toggles | city profiles (`.curr-btn`, `.wt-btn`) | filled-active button groups | switch unit/context | City Intelligence |
| Dropdowns (native) | map (`#chartProfile`, `#planet*`, `#house*`, `#angle*`, `#overlay*`), app_shell (`select.inline`, house-system) | native `<select>` | choose value | query / settings |
| Selectors (custom) | profile v11 typeahead (`.suggest`), comparison picker modal | suggestion list / modal list | choose place | favorites / comparison |
| Favorite control | map popup, profile star, relocated `.fav-btn` | button label flip / star toggle / button+★ | add + reflect favorite | favorite_place (hybrid) |
| Disclosure rows | comparison v2–v5 (`.block-header`), city profiles (`.acc-trigger` / `.acc-row`) | section collapse vs accordion row | expand/collapse content | content section |
| Modal triggers | comparison (Replace/Add/info), city (citizenship/home-currency), profile (notes/wheel), map (none; Leaflet popup) | button/link → overlay | open dialog | varies |
| Notes controls | relocated v1 (inline composer), comparison v3–v5 (toggle → composer + toolbar), profile v11 (link → modal) | inline / disclosure / modal | create/edit notes | note owner entity |
| Notes toolbar | comparison v3–v5 (`.notes-tool` B/I/U/list/voice) | formatting buttons (mostly placeholder) | format note | note record |
| Column controls | comparison (`.cc` Hide, `.cc-arr` reorder, `.cc-rep` Replace, `.stub-restore`, `.add-city-btn`) | small text/icon buttons | manage comparison columns | comparison set |
| Wheel popout | profile v11 + relocated v1 (`data-act=popout`) | disc click + `.popout` hint | enlarge wheel | chart |
| Trash/remove | profile v11 (`.trash`) | ✕ icon button | remove/archive saved item | favorites/lists |
| Debug controls | map (self-check, lat-cap overlays) | internal toggles | diagnostics | internal (non-canon) |

---

## 4. Control vs Badge

Whether each element lets the user act (Control), only conveys state (Badge), or
does both (Hybrid — flagged).

| Element | Type | Note |
|---|---|---|
| Favorite (map / relocated / profile star) | **HYBRID** ⚠ | Single element shows favorite status AND toggles it. Should split status (Badge) from action (Control). |
| Current Location | **HYBRID** ⚠ | Profile pill = Control (switch view); comparison `.city-tag` "Current Location" = Badge (status). Same words, two types. |
| Natal | **Control** (as view pill) | Switches view; the favorites-row "Natal (Birth Chart)" text is a Badge/label. |
| Comparison (view pill) | **Control** | Switches view. |
| Shared | **Badge** | No rendered control exists; would be status only. |
| Archived | **Badge** (latent) | Logic-only; the acting control is "Remove"/`.trash`, separate from any badge. |
| Draft | **Badge** | Scaffold status only. |
| Tropical / Placidus | **Badge / Metadata** | Not actionable on chart pages; app_shell house-system `<select>` is a separate Control. |
| Confidence tier | **Badge** (warning) | Not actionable. |
| Profile selector | **Control** | Authority control. |
| Angle pills/tabs, view pills, currency/weather toggles | **Control** | Context switches. |
| "Favorited ✓" post-action label | **Badge** | Result state after the Control fired. |
| Notes toggle "✎ Notes" | **Control** | Opens composer. |
| Disclosure chevrons | **Control** | Expand/collapse. |
| City "i" / "Open Full City Intelligence" | **Control** (navigate) | Action, not a status badge. |

Hybrids to resolve: **Favorite** and **Current Location** are the two clearest
control/badge collisions.

---

## 5. Control Hierarchy

Which controls read as highest authority, and whether that is consistent.

Observed authority order on chart-bearing pages (when correct):
1. **Profile selector** (governing lens) — highest
2. **View / context switch** (Natal / Current / Relocated / Comparison)
3. **Chart-local controls** (angle pills, wheel popout)
4. **Object controls** (favorite, notes, compare)
5. **Reference/section controls** (disclosures, currency/weather toggles)
6. **Navigation/account** (nav links, account menu)

Findings:

- **Profile v11:** consistent. Profile selector sits in/above the plate; view
  pills below; chart controls inside cards; saved-item controls in lower panels.
  Authority reads correctly.
- **Relocated v1:** mostly consistent. Profile authority lives in the header
  (`#profileSelect`), favorite is a prominent page-level button beside the plate,
  notes/intel are lower. Risk: the favorite button competes visually with profile
  authority because both are top-level page controls.
- **Map:** **inconsistent.** The profile (`#chartProfile`) is a small native
  select buried in a side panel, while popup actions ("Open chart", "Favorite")
  are the salient controls at point of contact. The highest-authority control is
  the least prominent.
- **Comparison v2–v5:** profile authority is weak (static name + Edit/Add chips),
  while column controls (Hide/Reorder/Replace/Add) dominate. Authority sits with
  the comparison set in practice, not the profile. v5 is the cleanest but still
  subordinates the profile.
- **City profiles:** no profile authority (place-authoritative pages). Internal
  hierarchy (currency/weather/citizenship switches, accordions) is consistent
  within v4; v1–v3 drift slightly.
- **app_shell:** uses "Chart Record" as the authority control instead of Profile;
  parallel concept, divergent vocabulary; scaffold-only.

Cross-page inconsistency: the **same authority (profile)** is presented four
different ways (serif button, header button, native select, static text), so its
hierarchical rank is not legible across surfaces.

---

## 6. Open Questions

Documented tensions; not resolved here.

- **Add vs Edit vs Change** — carried from 2.8D §6a. "Add" (create) appears as "+",
  "Add", "Add to Favorites"; "Change" appears as caret-only profile switch and as
  "(Change)"/"Change Citizenship". Final verb→action mapping unresolved.
- **Favorite: action vs status** — one hybrid control does both. Split into a
  status Badge + an action Control, or keep fused?
- **Open vs View vs Full (chart)** — "Open chart" / "View chart" / "Full chart"
  for the same navigation. One canonical verb needed.
- **Open City Intelligence wording** — "i" vs "Open Full City Intelligence" vs
  "→"; which is canonical?
- **Remove vs Archive vs Hide** — profile "Remove" archives; comparison "Hide" is
  transient; no destructive "Remove" exists. Three lifecycles, loose labels.
- **Link vs button** — many actions use text/underline links (`.linkbtn`,
  `.visa-change`, `.curr-home-change`, `.notes-link`) while equivalents elsewhere
  are buttons. When is each appropriate?
- **Dropdown vs disclosure** — profile switching uses a button/native select;
  sections use disclosures/accordions; angle switching uses pills vs tabs. Which
  metaphor owns which job?
- **Notes entry points** — three models (inline composer, disclosure toggle,
  link→modal). Single canonical entry pattern unresolved (and must respect 2.8D
  notes-ownership doctrine: notes attach to entities, not table sections).
- **Profile switching behavior** — selector presentation differs four ways; also
  unresolved: does switching profile re-render in place (per Plate Doctrine §5)
  and how is that signaled by the control?
- **"Add" object naming** — "+", "Add", "+ Add" frequently omit the object; should
  every create action name its object (Add Favorite, Add City, Add Profile)?
- **Nav label consistency** — "View Map" vs "Map", "Comparison" vs "Compare".
- **Angle control metaphor** — pills (profile/relocated) vs underline tabs
  (comparison) for the identical action.
- **app_shell vocabulary** — "Chart Record"/"New Chart Record" vs product
  "Profile"; reconcile or keep scaffold-only.

---

## Summary of highest-value control/action corrections

1. Resolve the **Favorite hybrid** (status Badge vs action Control).
2. Resolve the **Current Location hybrid** (view-switch Control vs status Badge,
   same words).
3. Unify **profile selector** presentation so its authority rank is legible on
   Map / Profile / Relocated / Comparison (and strengthen it on Map).
4. Canonicalize navigation verbs: **Open vs View vs Full** chart; City
   Intelligence entry wording.
5. Separate **Remove / Archive / Hide** semantics.
6. Apply the 2.8D **Add/Edit/Change** distinction to every control label, and
   require create actions to name their object.
7. Pick canonical metaphors for **angle switching** (pills vs tabs) and **notes
   entry** (inline vs disclosure vs modal).
