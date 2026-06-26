# Beta Master Checklist

**Canonical release tracker for Beta.**  
**Last updated:** 2026-06-27 (Settings V1 canon)
**Rule:** Every H/M/BI/M slice updates this file before closeout.

### Next Slice

**BI-0G — First save dialog token harmonization**

Scope: Mockups 06–08 (`validation/mockups/beta/first_experience/`) → harmonize first map popup + save dialog with instrument family. Auth + birth intake done in [272](../results/272_first_experience_auth_intake_implementation.md).

*BI-0C complete. Transition screen deferred (direct map redirect). Map in maintenance mode ([269](../results/269_map_surface_genie_harmonization_audit.md)).*

---

> Summaries only — detail in linked audits/canon.  
> **Built ≠ Release Ready.** Release Ready means a stranger could complete the workflow without coaching.

**Related (do not duplicate):**
- [Material System Canon](canon/MATERIAL_SYSTEM_CANON.md) · [Material delta](../results/263_material_system_delta.md)
- [Map trust audit](../results/265_map_control_overlay_trust_audit.md) · [M2 surface audit](../results/269_map_surface_genie_harmonization_audit.md) · [Map QA pass 1](../results/144_map_qa_pass1.md)
- [Settings V1 Product Spec](canon/SETTINGS_V1_PRODUCT_SPEC.md)
- [Family resemblance](../results/264_family_resemblance_final_audit.md) · [First experience archaeology](../results/270_first_experience_archaeology_audit.md) · [Settings audit](../results/262_settings_harmonization_audit.md)
- [Production acceptance](../architecture/PRODUCTION_ACCEPTANCE_CHECKLIST.md) · [Feature status board](../architecture/FEATURE_STATUS_BOARD.md) *(stale 2026-06-14 — use this doc)*

---

## Release state legend

| Column | Meaning |
|--------|---------|
| **Built** | Code exists in production path |
| **Smoke** | Automated static/runtime smoke passes |
| **PO QA** | Product owner manually validated |
| **Release Ready** | Stranger-safe without hand-holding |

| Risk | Meaning |
|------|---------|
| **P0** | Blocks any external beta |
| **P1** | Blocks public / broad beta |
| **P2** | Polish; acceptable post-beta |

| Remaining risk | Engine/data · UI/presentation · QA/acceptance |

---

## Beta Readiness (honest)

| Metric | Estimate |
|--------|----------|
| Built (code exists) | ~72% |
| Smoke-covered | ~55% |
| PO QA'd | ~40% |
| **Release Ready** | **~25%** |

**Release confidence: ~58%** — closed internal/alpha plausible; external beta blocked on intake/auth + city search + first-session map trust.

---

## Major areas — release matrix

| Area | Built | Smoke | PO QA | Release Ready | Risk left | Risk |
|------|:-----:|:-----:|:-----:|:-------------:|-----------|:----:|
| **Auth** | ✅ | ✅ | ⚪ | ⚪ | PO QA | **P0** |
| **Birth intake** | ✅ | ✅ | ⚪ | ⚪ | PO QA | **P0** |
| **Map** | ✅ | ✅ | 🟡 | ⚪ | UI · Genie harmonization · QA | **P0** |
| **Comparison V5** | ✅ | ✅ | 🟡 | 🟡 | QA | P1 |
| **Profile / Relocated** | ✅ | ✅ | 🟡 | 🟡 | Engine · QA | P1 |
| **City Intelligence** | 🟡 | ✅ | ⚪ | ⚪ | UI · QA | P1 |
| **Settings** | 🟡 | ✅ | ⚪ | ⚪ | UI · QA | P1 |
| **Notes** | ✅ | ✅ | ⚪ | ⚪ | QA | P1 |
| **Help** | 🟡 | ✅ | ⚪ | ⚪ | UI · QA | P1 |
| **Exports / OAuth** | ⚪ | ⚪ | ⚪ | ⚪ | — | P2 |

---

## Product Confidence (qualitative)

| Question | Answer today |
|----------|--------------|
| Would I trust this with a **paying** user? | **No** — intake/auth visuals and city search not release-ready |
| Would I let an **astrologer** evaluate it? | **Cautiously** — chart engine credible; first 5 minutes weak |
| Would I use it for a **real relocation/trip** exploration? | **Internal only** — map overlays need PO trust pass |
| Would I be **embarrassed by the first 5 minutes**? | **Yes** — auth + intake not harmonized with instrument family |

---

## Known Weak Spots

- Auth reskinned to instrument family (`auth.html`) — PO QA pending
- Birth intake reskinned; exact time only; name silent on first-run — PO QA pending
- Google/Apple OAuth deferred; status must stay explicit
- City/IATA alias quality (NYC, Bombay, Praha)
- Ghost NOT deferred (engine exclude not shipped)
- Notes library partial (canonical on chart surfaces only)
- Full City Intelligence page incomplete (inline only for Beta)
- Map material bridge shipped (M2-X); PO visual QA + screenshots still required
- M2 screenshot evidence incomplete — PO session required ([269](../results/269_map_surface_genie_harmonization_audit.md))
- Exports absent
- FEATURE_STATUS_BOARD stale — verify port 8004 / comparison facts before external users

---

## Beta Test Program

| Phase | Audience | Main question |
|-------|----------|---------------|
| **Internal PO QA** | Founder | Does it break? Can I complete first journey alone? |
| **Alpha** | 5–10 trusted users | Can people complete first journey without help? |
| **Closed beta** | 20–50 users | Does the experience feel worth returning to? |
| **Pro review** | 5–10 astrologers | Do astrologers trust calculations and overlays? |
| **Public beta** | Open | Would I trust this with a paying user? |

*Do not advance phase until prior phase blockers are cleared.*

---

## 1. First-Time User Journey

| Workflow | Built | Smoke | PO QA | Release Ready | Risk | Link |
|----------|:-----:|:-----:|:-----:|:-------------:|:----:|------|
| Email auth | ✅ | 🟡 | ⚪ | ⚪ | P0 | [ACCEPTANCE §1](../architecture/PRODUCTION_ACCEPTANCE_CHECKLIST.md) |
| Google/Apple OAuth | ⚪ | ⚪ | ⚪ | ⚪ | P2 | [FEATURE_STATUS_BOARD](../architecture/FEATURE_STATUS_BOARD.md) |
| First profile intake | ✅ | 🟡 | ⚪ | ⚪ | P0 | `first_profile_intake.js` |
| Chart calculation | ✅ | ✅ | 🟡 | 🟡 | P1 | — |
| City / IATA lookup | ✅ | 🟡 | ⚪ | ⚪ | P0 | [CITY_SEARCH](../architecture/CITY_SEARCH_PRODUCTION_REQUIREMENTS.md) |
| App onboarding modal | ✅ | 🟡 | ⚪ | ⚪ | P1 | [WEB2_ONBOARDING](../product/WEB2_ONBOARDING_AND_GUIDED_DISCOVERY_V2.md) |
| Map walkthrough | ✅ | 🟡 | ⚪ | ⚪ | P1 | [132](../results/132_onboarding2a_map_walkthrough_execution_plan.md) |
| First overlay search | ✅ | ✅ | 🟡 | ⚪ | P0 | [265](../results/265_map_control_overlay_trust_audit.md) |
| First save | ✅ | 🟡 | ⚪ | ⚪ | P1 | [140](../results/140_mapux3_save_search.md) |
| Favorites | ✅ | 🟡 | ⚪ | ⚪ | P1 | — |
| Comparison open | ✅ | ✅ | 🟡 | 🟡 | P1 | V5 smokes |
| CI first view | 🟡 | ✅ | ⚪ | ⚪ | P1 | H8 smoke |
| Notes compose | ✅ | ✅ | ⚪ | ⚪ | P1 | H7 smoke |
| Help open | 🟡 | ✅ | ⚪ | ⚪ | P1 | H9 smoke |

---

## 2. Core Product

| Surface | Built | Smoke | PO QA | Release Ready | Risk type | Risk |
|---------|:-----:|:-----:|:-----:|:-------------:|-----------|:----:|
| Map | ✅ | ✅ | 🟡 | ⚪ | UI · QA | P0 |
| Genie / GV search | ✅ | ✅ | 🟡 | ⚪ | QA | P1 |
| Ghost controls | 🟡 | ✅ | ⚪ | ⚪ | Engine · QA | P1 |
| Profile | ✅ | ✅ | 🟡 | 🟡 | Engine · QA | P1 |
| Relocated | ✅ | ✅ | 🟡 | 🟡 | QA | P1 |
| Comparison V5 | ✅ | ✅ | 🟡 | 🟡 | QA | P1 |
| City page | 🟡 | ✅ | ⚪ | ⚪ | UI · QA | P1 |
| Settings | 🟡 | ✅ | ⚪ | ⚪ | UI · QA | P1 |
| Notes | ✅ | ✅ | ⚪ | ⚪ | QA | P1 |
| Help | 🟡 | ✅ | ⚪ | ⚪ | UI · QA | P1 |
| History / Pin | ✅ | ✅ | ⚪ | ⚪ | QA | P1 |
| Exports | ⚪ | ⚪ | ⚪ | ⚪ | — | P2 |

---

## 3. City Intelligence

| Item | Built | Smoke | PO QA | Release Ready | Risk |
|------|:-----:|:-----:|:-----:|:-------------:|:----:|
| Inline canonical renderer | ✅ | ✅ | ⚪ | 🟡 | P1 |
| Full city page | 🟡 | ✅ | ⚪ | ⚪ | P1 |
| Backend hydration | ✅ | ✅ | ⚪ | 🟡 | P1 |
| Bulk seed | 🟡 | ⚪ | ⚪ | ⚪ | P2 |
| Photos / AI | ⚪ | ⚪ | ⚪ | ⚪ | P2 |

Canon: [CITY_INTELLIGENCE_CANON.md](canon/CITY_INTELLIGENCE_CANON.md)

---

## 4. Map (detail)

| Item | Built | Smoke | PO QA | Release Ready | Risk |
|------|:-----:|:-----:|:-----:|:-------------:|:----:|
| M1-A control truth | ✅ | ✅ | 🟡 | 🟡 | P1 |
| M1-B overlay instrumentation | ✅ | ✅ | ⚪ | 🟡 | P1 |
| M1-C popup + cities | ✅ | ✅ | ⚪ | 🟡 | P1 |
| M1-D chrome / history | ✅ | ✅ | ⚪ | 🟡 | P1 |
| M2 surface + Genie harmonization audit | ✅ | ✅ | ⚪ | ⚪ | P1 |
| Overlay engine (`truth_grid`) | ✅ | ✅ | 🟡 | 🟡 | P0 |
| M1-E cache | ⚪ | ⚪ | ⚪ | ⚪ | P2 |
| Material harmonization (Genie/panel) | 🟡 | ✅ | ⚪ | ⚪ | P1 |

[265 audit](../results/265_map_control_overlay_trust_audit.md)

---

## 5. Visual Polish (Beta-only)

| Item | Built | Release Ready | Risk |
|------|:-----:|:-------------:|:----:|
| Chart family (H10) | ✅ | 🟡 | P1 |
| Map material | ⚪ | ⚪ | P2 |
| D2 tokens | ⚪ | ⚪ | P2 |
| Rain / virga | ⚪ | ⚪ | P2 |

*Cosmetic only — does not outrank P0 intake/auth/map trust.*

---

## 6. QA Required (PO)

Same as Release Ready gaps — smoke is not sufficient:

- Auth + birth intake (BI-0 target)
- City search acceptance §7.2
- M2 map surface + Genie harmonization ([269](../results/269_map_surface_genie_harmonization_audit.md))
- Map post-M1 (ghost, save, history, overlays)
- Comparison marathon session
- Settings astrology → engine propagation
- Help handbook usability
- CI inline truth check
- Cross-room family resemblance walk
- Operational smoke suite on port 8004

---

## 7. Deferred After Beta

OAuth · Exports · saved-investigations library UI · M1-E cache · pin→comparison · ghost NOT engine · map material pass · D2 tokens · CI full page · help illustrations · rain/virga · AI advisor / Web3 · personalization settings

---

## 8. Release Blockers (tiered)

### P0 — blocks any external beta

| Blocker | Owner action |
|---------|--------------|
| **Auth + first profile intake** beautiful and reliable | BI-0 audit → implement |
| **Birth intake produces correct chart** | PO test + engine spot-check |
| **Map overlay demo** reliable for first-session trust | PO map pass post-M1 |
| **City search / IATA acceptance** | Run [ACCEPTANCE §7.2](../architecture/PRODUCTION_ACCEPTANCE_CHECKLIST.md) |
| **Multi-user data safety** | Verify `/profiles` RLS in staging |

### P1 — blocks public / broad beta

| Blocker | Owner action |
|---------|--------------|
| Settings PO QA | H6 acceptance |
| Notes PO QA | H7 + library scope |
| CI full-page scope clarity | Document inline-only Beta |
| Map post-M1 PO QA | Screenshot + walkthrough |
| Help handbook usability | H9 PO pass |
| Stale docs risk | Re-verify comparison facts + port 8004 |

### P2 — post-beta acceptable

| Item | Notes |
|------|-------|
| Exports | Placeholder |
| OAuth (if still deferred) | Document absence |
| Rain / virga | Material canon |
| Full palette / D2 tokens | After D1 |
| Map material harmonization | Family outlier |

---

## 9. Completion Log

*Append only. Newest first.*

```
✓ BI-0C Auth + birth intake implementation ([272](../results/272_bi0c_first_experience_implementation.md))
✓ BI-0B First experience mockups ([271](../results/271_first_experience_mockups.md))
✓ BI-0A First experience archaeology (read-only)
✓ M2-X Map visual harmonization (family bridge)
✓ M2 Map surface + Genie harmonization audit (read-first)
✓ B0-A Beta release tracker refinement      (B0-A)
✓ B0 Beta master checklist                (B0)
✓ M1-D Map explore chrome, pin, history   (aa915c1)
✓ M1-C Popup overlay discovery + cities   (cf2df64)
✓ M1-B Overlay trust instrumentation      (0841f5a)
✓ M1-A Map control truth                  (47ca21b)
✓ H10 Family resemblance                  (c563b6e)
✓ H9 Help handbook                        (50e92e4)
✓ H8 City Intelligence hydration          (3224855)
✓ D1 Material system canon                (5643242)
✓ H7 Notes canonicalization               (0da1b1a)
✓ H6 Settings harmonization               (625e23b–c932f68)
✓ Comparison V5 final punch list          (1c429e4)
```

---

## Maintenance rule

1. **One tracker** — this file only. No parallel checklists.
2. **Every H/M/BI/M slice** updates Built/Smoke/PO QA/Release Ready, risk tier, §8 if needed, and appends §9 **before closeout**.
3. **Release Ready** only when a stranger could use it unaided.
4. **Link, don't duplicate** — `results/`, `docs/canon/`, smoke script names.
5. **Five-minute read** — if a section grows, summarize and link out.
