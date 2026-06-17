# Task 41 — Port Normalization Fix

**Type:** Implementation  
**Date:** 2026-06-16  
**Canonical port:** 8004 (per task 40)

---

## 1. Files changed

| File | Lines | Change |
|------|-------|--------|
| `map_CURRENT.html` | 980 | Added `const API_BASE = '';` |
| `map_CURRENT.html` | 1473 | `` fetch(`${API_BASE}/profiles`, ...) `` |
| `map_CURRENT.html` | 2273 | `{ apiBase: API_BASE, coordTolerance: 0.02 }` |
| `map_CURRENT.html` | 2405 | `` `${API_BASE}/places/search?q=...` `` |
| `map_CURRENT.html` | 4749 | `` fetch(`${API_BASE}/search-regions`, ...) `` |
| `scripts/smoke_map_current.py` | 39 | `BASE_URL` default `8000` → `8004` |
| `scripts/smoke_library_scaffold.py` | 31 | `BASE_URL` default `8000` → `8004` |
| `scripts/smoke_library_handoff.py` | 45 | `BASE_URL` default `8000` → `8004` |
| `.env.example` | 21–22 | Appended `# Server` / `PORT=8004` |

No other files modified.

---

## 2. Grep validation (steps 1–3)

### Step 1 — `map_CURRENT.html`

```
rg -n "8004|8000|127.0.0.1" map_CURRENT.html
```

Remaining matches are **comments** (`port 8000`, `8004 Supabase block`) and `maxSamples: 8000` — **no** `http://127.0.0.1:8004` literals remain.

```
API_BASE constant:
980:const API_BASE = '';
1473:        const profilesResponse = await fetch(`${API_BASE}/profiles`, {
2273:    }, { apiBase: API_BASE, coordTolerance: 0.02 });
2405:                `${API_BASE}/places/search?q=${encodeURIComponent(displayName)}`
4749:    const response = await fetch(`${API_BASE}/search-regions`, {
```

**PASS**

### Step 2 — `smoke_map_current.py`

```
39:BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8004").rstrip("/")
```

**PASS**

### Step 3 — `.env.example`

```
22:PORT=8004
```

**PASS**

---

## 3. Smoke result (step 4)

```bash
set -a && source .env.staging && set +a && venv/bin/python scripts/smoke_map_current.py
```

**Exit code:** 0

```json
{
  "overall_pass": true,
  "report": ".../validation/reports/map_current_smoke.json",
  "url": "http://127.0.0.1:8004/map_CURRENT.html?bust=...&skipOnboarding=1"
}
```

**PASS** — no assertion failures.

---

## 4. Validation

**VERIFIED**

- All 4 hardcoded `http://127.0.0.1:8004` URLs replaced with `API_BASE` (same-origin relative).
- Smoke `BASE_URL` defaults aligned to 8004.
- `PORT=8004` added to `.env.example`.
- `smoke_map_current.py` exits 0.
- Scope limited to authorized files; no backend changes.
- Not committed (awaiting human review).

---

## Task 41b — Commit & push

**Commit:** `e6a1948`  
**Message:** `fix: replace hardcoded :8004 URLs with API_BASE constant`

**Push:** `456ddfa..e6a1948  main -> main` (success)

**`git log origin/main..HEAD`:** empty (local in sync with remote)

**Note:** `validation/reports/map_current_smoke.json` and `validation/reports/sprint_dc_ic_validation.json` were modified by smoke run but **not** included in commit (out of scope).

**VERIFIED**
