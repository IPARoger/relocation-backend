# Task 40 — Canonical Port Check

**Type:** Read-only audit  
**Date:** 2026-06-16  
**Resolves:** 8000 vs 8004 split from task 39

---

## 1. Files read

| # | File | Notes |
|---|------|-------|
| 1 | `Old File/main.py` | Only path returned by step-1 `find` (374 lines; tail inspected for bind) |

**Step-1 `find` output (maxdepth 2):**

```
./Old File/main.py
```

No `app.py`, `main.py` (root), `server.py`, `run.py`, `Procfile`, `Makefile`, or `start.sh` in repo root or `/backend`.

**Not opened (per 5-file cap / step-1 scope):** `main_centerline_FIXER.py` (production ASGI module), smoke scripts, ops docs — cited below via `rg`/`grep` only.

---

## 2. Port binding line(s) found

### `Old File/main.py` (only find result)

**No port binding line.** File ends with a `/health` route; no `uvicorn.run`, `app.run`, `if __name__`, or `PORT=` assignment.

### Production module (grep only — not opened)

`main_centerline_FIXER.py` — **no in-process bind.** No `uvicorn.run`, no `if __name__ == "__main__"` block, no `os.getenv("PORT")` / hardcoded listen port. The FastAPI `app` is exported for external ASGI servers.

**Effective bind mechanism (CLI, not in step-1 files):**

| Source | Line | Content |
|--------|------|---------|
| `docs/architecture/OPERATIONAL_SMOKE_TESTS.md` | 24 | `venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8004 --reload` |
| `scripts/smoke_map_current.py` | 14 (docstring) | `uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000` |
| `scripts/smoke_map_current.py` | 39 | `BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000")` |
| `scripts/smoke_saved_investigations.py` | 38 | `PORT = 8004` |
| `scripts/smoke_saved_investigations.py` | 135 | `"--port", str(PORT)` |

Port is chosen by whoever invokes `uvicorn`, not by application code.

---

## 3. Step-3 grep (files only)

```
./Old File/main_centerline.py
./Old File/main.py
./main_contours.py
./truth_field_regions.py
./aura_field_engine.py
./build_cities.py
./local_product_store.py
./brute_force_validator.py
./repositories/account_saved_investigations_repository.py
./repositories/account_settings_repository.py
```

(None opened beyond step-1 file.)

---

## 4. Classification

**SPLIT_PORT**

- The backend does not embed a single listen port.
- Startup paths disagree: operational doc and account/JWT smokes use **8004**; map/renderer smokes and several `BASE_URL` defaults use **8000**.
- Not **ENV_DRIVEN** at the application layer (no `PORT` read in `main_centerline_FIXER.py`). Smokes optionally override client URL via `BASE_URL`, but bind port is still hardcoded per script when they spawn uvicorn.

---

## 5. Recommended canonical port

**No application-level canonical port exists.**

For local dev normalization (implementation follow-up, not this task):

| Candidate | Rationale |
|-----------|-----------|
| **8004** | Documented in `OPERATIONAL_SMOKE_TESTS.md` as the primary `main_centerline_FIXER` server; matches four hardcoded `http://127.0.0.1:8004` lines in `map_CURRENT.html` (task 39). |
| **8000** | Default in many smoke `BASE_URL` values; ops doc still treats 8000 as a separate "legacy" aura/calculation service. |

**Recommendation:** Standardize on **8004** for `main_centerline_FIXER` and migrate smoke `BASE_URL` defaults from 8000 to 8004 (or use relative URLs / single `BASE_URL` env everywhere). Until that work lands, treat bind port as **caller-defined**.

---

## 6. Validation

**VERIFIED**

- Step-1 startup candidate located (`Old File/main.py`); production entry is `uvicorn main_centerline_FIXER:app` (outside find pattern).
- Port binding mechanism determined: **CLI `--port`**, not in-app.
- Classification assigned: **SPLIT_PORT**.
- Files opened for read: **1** (within 5-file limit).
- No application files modified.
