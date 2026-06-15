# 05 Frontend Placeholder Honesty Audit

Task: `05_FRONTEND_PLACEHOLDER_HONESTY_AUDIT`  
Mode: read-only audit; documentation output only  
Notification: `started` sent once via `scripts/relay_notify.py started`

## Scope

Authorized files read:

- `app_shell.html`
- `map_CURRENT.html`
- `account_drawer.js`
- `supabase_store_bridge.js`
- `docs/architecture/TWO_AGENT_RELAY_GOVERNANCE.md`
- `audits/01_backend_wiring_inventory.md`
- `audits/02_settings_consumption_audit.md`
- `audits/03_settings_truth_audit.md`

No app code was modified. No backend/schema/database action was performed.

## Classification Key

- **Misleading / unavailable behavior**: visible control or copy implies behavior that is absent, stale, weaker than stated, or routed to the wrong surface.
- **Acceptable honest placeholder**: visible limitation is disabled, explicitly labeled, or has an honest blocked state.
- **Move/remove/relabel later**: not an implementation instruction for this task; only a future disposition bucket.
- **Out of scope**: frozen or explicitly deferred by governance/audits.

## A. Visible Controls Still Implying Unavailable Behavior

| Priority | Surface | Evidence | Current truth | Classification |
|---|---|---|---|---|
| HIGH | `app_shell.html` saved investigation resume copy | `RESUME_CONTEXT_STUB` says `Resume passes context only; saved conditions not replayed on map (v1)`; rendered in Dashboard/Chart Record saved explorations and in-shell map route (`app_shell.html` lines 233, 1110, 1192, 1310). | Current accepted workflow is that saved investigation replay restores conditions and auto-searches on `map_CURRENT.html`. Copy is stale and understates real behavior. | Misleading / stale copy |
| HIGH | `app_shell.html` Export / Share | Export entry is reachable from Chart Record, Screen 4, and Comparison (`app_shell.html` lines 1167, 1399, 1636). Export screen builds `https://example.com...` as a readonly link (`app_shell.html` lines 1643-1658). PNG is disabled and labeled placeholder (`app_shell.html` line 1662). | PNG placeholder is honest. The example-domain link looks like a share artifact but is not a real share link. Prior backend audit also classifies export/share as placeholder (`audits/01` lines 251-268). | Misleading placeholder |
| HIGH | `app_shell.html` in-shell `#/map` route remnants | Primary nav opens real `map_CURRENT.html` (`app_shell.html` lines 1054-1062), but `screenMap()` still exists as an internal route (`app_shell.html` lines 1300-1336), including `Full chart`, `Compare places`, `Export viewport`, and disabled `Save exploration`. | Normal primary nav no longer reaches the placeholder map, but the route is still reachable via `data-nav="map"` buttons, hash URLs, and some back buttons. Its action panel can navigate without a `placeId`. | Orphaned / duplicate map path |
| MEDIUM | `app_shell.html` Screen 4 `Add to comparison` | Screen 4 shows `Add to comparison` (`app_shell.html` line 1398). Prior backend audit says it navigates to Compare but does not pre-select the current place (`audits/01` lines 173-180). | Button wording implies adding the viewed place; current behavior is navigation only. | Misleading action label |
| MEDIUM | `app_shell.html` Screen 4 `Back to map` | Screen 4 uses `data-nav="map"` for back buttons (`app_shell.html` lines 1365, 1397). | `data-nav="map"` navigates to the in-shell map route, not necessarily the production `map_CURRENT.html` handoff. | Orphaned navigation path |
| MEDIUM | `map_CURRENT.html` city search | Label says `City (placeholder list — exact name, Enter)` and placeholder says `Exact name only...` (`map_CURRENT.html` lines 755-758). Failure copy says `Not in placeholder list... Real geocoder required` (`map_CURRENT.html` lines 6078-6085). | This is honestly labeled as a placeholder list, but it remains a visible production-map limitation and city-only wording. | Honest limitation, still user-facing |
| LOW | `account_drawer.js` Help buttons | Two drawer buttons, `Learn & Tutorials` and `About Relocation Astrology`, both dispatch `ad-help` and navigate to one static help route (`account_drawer.js` lines 191-194, 311-315). | Both labels imply distinct destinations; current destination is the same static `Help & Learn` screen. | Duplicate entry point |
| LOW | `supabase_store_bridge.js` placeholder data fields | `notes: ""`, `tags: []`, `updated_at: null`, comparison set `notes: ""`, and store-level `notes: []` are assembled (`supabase_store_bridge.js` lines 245-315, 340-353). | Mostly not directly visible, but these placeholders explain why some UI notes are local/empty or not cross-device. | Future data-room placeholders |

## B. Placeholders Acceptable Because Clearly Marked

| Surface | Evidence | Why acceptable for now |
|---|---|---|
| Shell global banner / footer quarantine | `APPLICATION SHELL — placeholder walkthrough only. Not production UI`; `Future rooms — quarantined`; post-v1 transit/AI/Layer 4-5 copy (`app_shell.html` lines 171-187, 1862-1872). | Clear global truth and quarantine language. |
| In-shell popup modal after honesty pass | Copy says production map opens in main map tool; no fake ASC/Sun facts remain (`app_shell.html` lines 190-199). | Honest, non-fake, close-only modal. |
| Dashboard placeholder language | Dashboard says map opens via `defaultChartRecordId` only, not last-used chart (`app_shell.html` lines 1071-1121). | Limitation is explicit. |
| Chart Record notes | Textarea says `saved on this device`; handler writes only `localStorage` (`app_shell.html` lines 1158-1162, 2189-2201). | Device-local persistence is clearly stated. |
| Favorites / Saved Explorations / Comparison Sets empty states | Favorites and saved explorations tell users to open map/save; comparison sets load or show empty state (`app_shell.html` lines 1172-1207). | Honest path-forward copy. |
| Screen 4 blocked state | Missing `chartRecordId` or `placeId` shows honest blocked state (`app_shell.html` lines 1355-1365). | Does not imply unavailable chart can render. |
| Screen 4 notes / favorite | Note says `placeholder — not saved`; `Favorite this place` disabled (`app_shell.html` lines 1391-1395). | Explicitly non-saving and disabled. |
| Comparison notepad / future AI | Comparison note says `placeholder — not saved`; future AI/multi-chart is disabled (`app_shell.html` lines 1628-1632). | Honest and quarantined. |
| Settings house-system | Disabled select says `Placidus only for now`; other systems `coming soon`; save omits `house_system` (`app_shell.html` lines 1669-1694, 2204-2218). | The previous honesty gap is neutralized in current source, though prior audits still describe the old gap. |
| Settings history / location future controls | History buttons disabled as placeholders; Road Trip/GPS/Notifications/Offline controls marked `Experimental · not yet available` and `Soon` (`app_shell.html` lines 1696-1734). | Disabled and labeled. |
| Birth Data | `Birth data editing is not enabled here yet` and read-only display rows (`app_shell.html` lines 1799-1813). | Honest after `BIRTH-DATA-HONESTY-2`. |
| Map popup full chart | Map popup relocated facts are real; `Full chart coming soon` button is disabled (`map_CURRENT.html` lines 2154-2185). | No inert clickable chart path in popup. |
| Map debug/PoC legend | Aura/debug legend says debug/archaeology only and not canonical substrate (`map_CURRENT.html` lines 963-970). | Clearly debug-only. |
| Map Saved Places | Empty state says no saved places yet; dropdown is scoped to active profile and recenter-only (`map_CURRENT.html` lines 6133-6228). | Honest and real MVP behavior. |

## C. Items To Remove / Relabel / Disable / Move Later

This section records future disposition only. No implementation is authorized by this audit.

| Item | Later disposition bucket |
|---|---|
| Stale saved-investigation replay copy (`RESUME_CONTEXT_STUB`) | Relabel later: current copy contradicts accepted replay behavior. |
| Export/share screen example-domain link | Remove/disable/relabel later: avoid fake share artifact until real share/export is wired. |
| In-shell `#/map` route action panel | Remove or move later: keep production map as the only normal map surface. |
| Screen 4 `Add to comparison` | Relabel or wire later: current wording implies it adds the place. |
| Screen 4 `Back to map` using shell `map` route | Move later to production map handoff or label as shell return if retained. |
| Account drawer duplicate Help buttons | Relabel or split later: currently both lead to the same static screen. |
| Map city search placeholder list | Upgrade/relabel later: honest but visibly prototype-quality on the production map. |
| Bridge-level blank `notes` / `tags` placeholders | Leave internal until the Notes/File Cabinet doctrine is actively implemented. |

## D. High Priority Before Continuing Backend Wiring

Ranked by user-facing honesty risk, not by implementation recommendation.

1. **Stale saved-investigation replay copy** — it is directly wrong against current accepted behavior.
2. **Export/share screen fake link** — visible route implies share/export readiness and uses `example.com`.
3. **In-shell map route remnants** — primary map is fixed, but internal shell map actions remain reachable and can dead-end into missing context.
4. **Screen 4 action labels** — `Add to comparison` and `Back to map` imply stronger behavior than they perform.
5. **Map city search placeholder list** — honest but still prominent on production map; not a backend blocker unless location search UX becomes the next priority.

House-system is **not** a current high-priority honesty item in source: current Settings UI is disabled and Placidus-only. Prior audits remain historically accurate for the pre-fix state but are superseded by `04_HOUSE_SYSTEM_HONESTY` source behavior.

## E. Explicitly Out Of Scope

- No renderer, map math, overlays, truth-grid, aspect centerline, Rain/Virga, AI layers, Layer 4/5, transit, scoring, or recommendation systems.
- No backend route changes, schema changes, migrations, database writes, or Supabase mutations.
- No feature implementation from this audit.
- No notes persistence implementation.
- No export/share implementation.
- No city/geocoder replacement.
- No birth-data editing implementation.
- No comparison editing/versioning change.
- No changes to Telegram notification behavior beyond the fixed `started`/closeout labels required by this task.

## Files Written By This Task

- `audits/05_frontend_placeholder_honesty_audit.md`
- `results/05_frontend_placeholder_honesty_audit.md`

## Verification

- Read-only source/audit inspection completed across the exact authorized file list.
- No app/runtime/backend/schema/database files modified.
- `started` notification sent once.

VERIFIED
