# ROADMAP QUEUE — 5-Chat Architecture Track (binding)

Planner: propose the **first incomplete item** below. One objective per task.
Put `**Roadmap ID:** C?_?` in every task header. Reference closeout in results/.

**Product features** (port 8000, city search, Notes UI, etc.) are **after Chat 5** — do not plan them until this queue is done.

---

## Chat 1 — Backend Ownership Migration ✅ COMPLETE

JWT write routes live. Browser → JWT → Repository → RLS.

Done: profiles CRUD/archive, favorites, comparison sets, saved investigations, places resolve-or-create, GET /profiles hardening, POST /places → 410.

**No new Chat 1 tasks** unless regression found.

---

## Chat 2 — Legacy Route Retirement (CURRENT)

**Goal:** 410-quarantine remaining legacy **service-role write** routes the production UI no longer uses.

**Already done (do not repeat):**
- POST /places → 410 (Chat 1)
- GET /account-store, GET /profile-library → 410 (task 46)
- GET /local-product-store.json → 410 (task 49)
- Quarantine smokes updated (tasks 50–55)

| ID | Size | Item | Done when |
|----|------|------|-----------|
| C2-1 | M | **Audit** remaining legacy write routes — grep callers, list safe-to-quarantine vs active | closeout C2-1 |
| C2-2 | M | 410 quarantine **profiles** legacy writes: POST /profiles, PATCH /profiles/{id}, POST /profiles/{id}/archive | closeout C2-2 |
| C2-3 | M | 410 quarantine **saved-searches** legacy writes: POST /saved-searches, PATCH /saved-search/{id}, POST …/archive | closeout C2-3 |
| C2-4 | M | 410 quarantine **comparison-sets** legacy writes (POST/PATCH/archive paths superseded by JWT routes) | closeout C2-4 |
| C2-5 | M | 410 quarantine **favorite-places** legacy writes: POST /favorite-places, PATCH, archive | closeout C2-5 |
| C2-6 | M | 410 quarantine **notes** legacy writes: POST /notes, PATCH /note/{id} (if superseded) | closeout C2-6 |
| C2-7 | S | Update smokes to expect 410 on newly quarantined **write** routes; verify ownership smokes still pass | closeout C2-7 |

---

## Chat 3 — Read Path Consolidation Audit

| ID | Size | Item | Done when |
|----|------|------|-----------|
| C3-1 | L | Audit all read paths: account-store, supabase_store_bridge, direct Supabase, profile-library, saved-search reads | closeout C3-1 |
| C3-2 | M | Deliverable: read-path architecture plan (canonical read source, what retires) | closeout C3-2 |

**Audit only — no implementation.**

---

## Chat 4 — Read Path Simplification

Execute Chat 3 plan. Examples: JWT GET saved investigation, account-store improvements, retire profile-library reads, bridge simplification.

| ID | Size | Item | Done when |
|----|------|------|-----------|
| C4-1 | L | First implementation slice from C3-2 plan (planner picks one slice only) | closeout C4-1 |
| C4-2+ | L | Further slices — one per task until plan complete | closeout C4-N |

---

## Chat 5 — Dead Code Retirement & Cleanup

| ID | Size | Item | Done when |
|----|------|------|-----------|
| C5-1 | L | Audit: dead repositories, routes, smokes, bridge code, compatibility layers | closeout C5-1 |
| C5-2+ | M | Remove dead code per audit — one slice per task, reversible commits | closeout C5-N |

---

## After Chat 5 → Product track

Settings completion, saved comparisons UX, Help/onboarding, exports, city search, port 8000 migration — see `docs/architecture/ROADMAP_AND_SEQUENCE.md`.

---

## Planner rules

1. Chat 2 before Chat 3. Chat 3 before Chat 4. No skipping.
2. One route family per task (C2-2 … C2-6) — do not bundle.
3. Always grep production UI + ownership smokes before quarantining.
4. If active caller found → PAUSE, cite route.
5. Size S → Haiku; M/L → Sonnet (via RELAY_AUTO_MODEL).
