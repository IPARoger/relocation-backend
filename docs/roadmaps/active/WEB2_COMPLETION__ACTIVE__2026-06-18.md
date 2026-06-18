# Web2 Completion Roadmap

**Roadmap ID:** WEB2_COMPLETION  
**Status:** ACTIVE  
**Date:** 2026-06-18  
**Authority:** This is the current post–Chat-5 product roadmap. Supersedes ad-hoc product planning prior to architecture track closure.

**Checkpoint:** `a814c68` (Chat 5 governance sync)  
**References:** `relay/ROADMAP_QUEUE.md`, `docs/architecture/ROADMAP_AND_SEQUENCE.md`, `results/82_chat5_closure_audit.md`

---

## 1. Current Status

| Area | State |
|------|-------|
| Architecture chats 1–5 | **COMPLETE** — backend ownership, legacy write retirement, read-path consolidation, dead-code cleanup |
| Cleanup track | **CLOSED** — no remaining required cleanup slices |
| Product track | **CURRENT** — this roadmap |
| Auth, profiles, map handoff, Find Regions | Working, smoke-tested |
| Settings save/load | Working; `house_system` stored but not fully wired to engine |
| Notes | localStorage only — not persistent across devices |
| Help / onboarding | Minimal placeholder content |
| Port 8000 (Angular overlays, relocated chart popup) | Not migrated — deferred |
| Exports, share, diffs, dignities | Not implemented |

**Direction:** Complete honest Web2 product surfaces before Web3 discovery or interpretive expansion.

---

## 2. Completed Infrastructure Work

### Chat 1 — Backend Ownership Migration
- JWT write routes live: profiles, favorites, comparison sets, saved investigations, places resolve-or-create
- GET `/profiles` hardened; POST `/places` → 410
- Browser → JWT → Repository → RLS

### Chat 2 — Legacy Route Retirement
- 25/25 legacy service-role write routes return 410
- Verified: `smoke_legacy_writes_deprecated.py`

### Chat 3 — Read Path Consolidation Audit
- Read-path inventory and architecture plan (`results/59_*`, `results/60_*`)

### Chat 4 — Read Path Simplification
- No direct Supabase reads remain in `app_shell.html` or `map_CURRENT.html`
- Favorites, saved investigations, comparison sets, profile refresh routed through backend/bridge
- Dead GET routes quarantined (410)

### Production safety (pre–Chat track, retained)
- Email/password auth, account bootstrap, app_shell → map handoff contract
- Birth data resolution, GeoNames places table (~68k cities)
- Account drawer, settings persistence, favorites write path

---

## 3. Completed Cleanup Work

### Chat 5 — Dead Code Retirement & Cleanup (CLOSED)
| Slice | Outcome |
|-------|---------|
| C5-1 | Dead-code audit |
| C5-2a | Removed 6 confirmed-dead backend stubs |
| C5-4 / C5-4a | Legacy map audit; quarantined dead renderer stub |
| C5-5 | Removed `orb_defaults` mirror write from `app_shell.html` |
| C5-6 | Removed unused back-compat `state` proxy |

**Blocked (do not retry without new spec):** C5-2 (`_deprecated_legacy_write` shims), C5-3 (live bridge helpers).

**Closure:** `results/82_chat5_closure_audit.md`, governance sync `results/83_*`.

---

## 4. Remaining Web2 Work

### Priority 1 — Core shell completeness

| Item | Scope | Notes |
|------|-------|-------|
| **Settings UX** | Wire `house_system` to chart engine; honest settings feedback | Settings save works; functional effect incomplete |
| **Notes UX** | Migrate from localStorage to Supabase `notes` table via backend | Trust failure on device switch until done |
| **Help System** | Replace static placeholder with final copy and navigation | Currently minimal |
| **Onboarding Overlays** | Guided discovery walkthrough, dismissal, visual design | Modal exists; content and design incomplete |

### Priority 2 — User workflows

| Item | Scope | Notes |
|------|-------|-------|
| **Comparison Intake UX** | Real comparison facts; intake flow polish | Comparison screen uses mocked placeholder text |
| **Map Intake UX** | First-profile and return-user intake refinement | Handoff works; UX pass needed |
| **Export System** | Chart/data export paths | Not implemented |
| **Share System** | Share links, revocation, recipient experience | Backend scaffold exists; product incomplete |

### Priority 3 — Advanced surfaces (post-core)

| Item | Scope | Notes |
|------|-------|-------|
| **Diffs UI** | Comparison diffs after real comparison facts exist | Blocked on comparison data |
| **Dignities Layer** | Dignity overlay on map/chart surfaces | Not implemented |
| **Optional Interpretive Layer** | Interpretive content layer — **default OFF** | Future-facing; must not ship enabled by default |

### Priority 4 — Launch readiness

| Item | Scope | Notes |
|------|-------|-------|
| **Relocated Chart Page audit/wiring audit** | Port 8000 dependency; popup relocated chart | Requires port 8000 migration decision |
| **City Search and Language QA** | Alias coverage ("NYC", "Bombay", "Praha"); language QA | Prefix-only canonical English today |
| **Zodiac/House-System validation audit** | End-to-end validation of zodiac and house-system settings | Settings stored; engine wiring incomplete |
| **Final visual pass** | UI standardization per design canon | See `docs/product/UI_STANDARDIZATION_CANON_*` |
| **Final wiring QA** | Production acceptance checklist, smoke gate expansion | See `docs/architecture/PRODUCTION_ACCEPTANCE_CHECKLIST.md` |

### Production safety (retained from Track 0)

These remain prerequisites before external users:

- `/profiles` user scoping (multi-tenant leak risk if unfixed)
- `handle_new_user()` trigger verified in every Supabase environment

---

## 5. Deferred Web3 Work

Do not start until Web2 completion priorities 1–2 are honest and smoke-verified.

| Item | Rationale |
|------|-----------|
| Web3 discovery flows | Product identity expansion — out of Web2 completion scope |
| Angular aura overlays (port 8000) | Infrastructure migration; separate from shell UX |
| Google / Apple auth | Identity expansion — after core shell trustworthy |
| Email template styling | Polish — after functional completeness |
| Interpretive layer (enabled) | Default OFF; explicit founder decision required |
| Genie as production render driver | Infrastructure exists; not production path |

Draft exploratory roadmaps belong in `docs/roadmaps/superseded/` or `archive/` with `DRAFT` status until promoted to ACTIVE.

---

## 6. Launch Readiness Checklist

Use before declaring Web2 launch-ready. Each item requires smoke or manual QA evidence in `results/`.

### Infrastructure gates (done)
- [x] JWT ownership write paths live
- [x] Legacy service-role writes return 410 (25/25)
- [x] No direct Supabase reads in production shell HTML
- [x] App shell → map handoff contract verified
- [x] Cleanup track closed with closure audit

### Product gates (open)
- [ ] Settings changes produce visible chart/map effect (`house_system`)
- [ ] Notes persist across devices (Supabase-backed)
- [ ] Help content final (not placeholder)
- [ ] Onboarding walkthrough complete
- [ ] Favorites list display and soft-delete in UI
- [ ] Comparison intake uses real data
- [ ] Export and share flows end-to-end
- [ ] City search alias coverage meets production requirements
- [ ] `/profiles` scoped per authenticated account
- [ ] `handle_new_user()` confirmed in all environments
- [ ] Production acceptance checklist signed off
- [ ] Recovery smokes green on staging

### Explicit non-goals for Web2 launch
- Port 8000 full migration (unless promoted into scope)
- Dignities layer enabled in production
- Interpretive layer enabled by default
- Web3 discovery features

---

## Revision history

| Version | Date | Change |
|---------|------|--------|
| 2026-06-18 | 2026-06-18 | Initial ACTIVE roadmap post–Chat 5 closure |
