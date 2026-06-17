# RESULT: 54_run-quarantine-smoke-tests

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/54_54run-quarantine-smoke-tests.md  
**Date:** 2026-06-17 UTC

## Files changed

| File | Change |
|------|--------|
| `results/54_54run-quarantine-smoke-tests.md` | Closeout report (this file) |

No application, schema, backend, smoke-script, or server configuration files were modified.

## Server state (as found)

| Check | Result |
|-------|--------|
| Process on `:8004` | **Listening** — `Python` PID 45092 (`uvicorn` / `main_centerline_FIXER`) |
| Preflight at task start | `GET /health` → `200` `{"status":"ok"}` |
| Preflight after Playwright runs | `GET /health` → **timeout** (≥3s); subsequent smoke re-runs **blocked** |
| Server start/stop by this task | **None** (hard stop obeyed) |

**Finding:** The long-running process on port 8004 appears to be a **stale build** (pre-quarantine behavior). Repository code at `main_centerline_FIXER.py` defines `_quarantine_legacy_read()` returning HTTP 410 for all three legacy read paths, but the live `:8004` process returned 401/404/500/200 instead of 410.

## Invocation commands

Task 53 verified pattern (used here unchanged):

```bash
./venv/bin/python scripts/smoke_account_store_read.py
./venv/bin/python scripts/smoke_app_shell_store_read.py
```

Supplementary direct probes (read-only, no script changes):

```bash
./venv/bin/python - <<'PY'
# urllib probes against http://127.0.0.1:8004 — see raw output below
PY
```

**Environment note:** Unlike task 53 (no exported `SUPABASE_*`), this shell had `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `SUPABASE_SERVICE_ROLE_KEY` set. That caused `smoke_app_shell_store_read.py` to enter the optional Playwright branch and crash with a timeout before printing HTTP quarantine results.

## Raw output

### `smoke_account_store_read.py` (first run — server healthy)

```text
$ ./venv/bin/python scripts/smoke_account_store_read.py
PASS: health_200 — status=200
PASS: account_store_410 — {"error": "Gone", "reason": "legacy read path retired"}
PASS: account_store_auth_410 — {"error": "Gone", "reason": "legacy read path retired"}
PASS: smoke_account_store_read
exit: 0
```

**Interpretation:** Direct probe of live `:8004` immediately afterward returned `401` / `500` on `/account-store` (not 410). The smoke script's fallback logic spawns a **temporary server on `:8014`** when the live probe is not 410. The PASS above validates quarantine behavior on a **fresh temp process**, not the stale `:8004` listener.

### `smoke_account_store_read.py` (second run — server hung)

```text
$ ./venv/bin/python scripts/smoke_account_store_read.py
TimeoutError: timed out  (on GET /health against :8004)
exit: 1
```

### `smoke_app_shell_store_read.py` (both default `BASE=8000` and `BASE_URL=8004`)

```text
$ ./venv/bin/python scripts/smoke_app_shell_store_read.py
playwright._impl._errors.TimeoutError: Page.wait_for_function: Timeout 30000ms exceeded.
exit: 1

$ BASE_URL=http://127.0.0.1:8004 ./venv/bin/python scripts/smoke_app_shell_store_read.py
playwright._impl._errors.TimeoutError: Page.wait_for_function: Timeout 30000ms exceeded.
exit: 1
```

Script crashed in the Playwright `shell_loads_store_view_model` branch before emitting per-check PASS/FAIL lines. HTTP quarantine assertions for `/local-product-store.json` were not reached in output.

### Direct probes — live server `:8004` (task start, server responsive)

```text
GET /account-store                           -> status=401  body={"detail": "Missing or malformed Authorization header"}
GET /account-store  (Authorization: Bearer)  -> status=500  body=Internal Server Error
GET /local-product-store.json                -> status=200  body={"_storage": "TEMPORARY_LOCAL_SCAFFOLD", ... full scaffold JSON ...}
GET /profile-library/cr-anna-rivera          -> status=404  body={"detail": "profile not found"}
GET /profile-library/smoke-test-id           -> status=404  body={"detail": "profile not found"}
```

Expected quarantine body (all three routes in current repo code):

```json
{"error": "Gone", "reason": "legacy read path retired"}
```

## Per-route verdict table

Quarantined legacy **read** routes per tasks 46/50 (expected HTTP **410 Gone** with quarantine JSON body):

| Route | Method | Expected | Actual (live `:8004`) | Classification | Verdict |
|-------|--------|----------|------------------------|----------------|---------|
| `/account-store` | GET | 410 Gone | 401 `Missing or malformed Authorization header` | UNEXPECTED LIVE (auth-gated legacy handler, not quarantined) | **FAIL** |
| `/account-store` | GET + `Authorization: Bearer smoke-token` | 410 Gone | 500 Internal Server Error | UNEXPECTED LIVE | **FAIL** |
| `/profile-library/{profile_id}` | GET | 410 Gone | 404 `{"detail":"profile not found"}` | UNEXPECTED LIVE (route still resolves profiles) | **FAIL** |
| `/local-product-store.json` | GET | 410 Gone (task 50 smoke expectation; repo code quarantined) | 200 + full `TEMPORARY_LOCAL_SCAFFOLD` JSON | UNEXPECTED LIVE | **FAIL** |

**Smoke-script cross-check**

| Script | Exit | Quarantine route evidence |
|--------|------|---------------------------|
| `smoke_account_store_read.py` | 0 (1st) / 1 (2nd) | PASS only via **temp `:8014` fallback**, not live `:8004` |
| `smoke_app_shell_store_read.py` | 1 | **BLOCKED** — Playwright timeout before HTTP quarantine output |

## Overall verdict

**PARTIAL (0 of 4 live-route checks passed)**

- **0/4** quarantined read routes on the **live `:8004` server** returned the expected 410 Gone quarantine response.
- **1/2** quarantine smoke scripts reported exit 0, but that pass does **not** confirm live-server quarantine (temp-server fallback on `:8014`).
- **1/2** quarantine smoke scripts were **BLOCKED** on re-run / in this environment (server hang; Playwright timeout with Supabase creds exported).

## Unexpected findings (action items for next task)

1. **Restart required:** The `:8004` process is serving pre-quarantine behavior. Restart with current `main_centerline_FIXER.py` so `/account-store`, `/profile-library/*`, and `/local-product-store.json` return 410 as coded.
2. **Misleading smoke pass:** `smoke_account_store_read.py` exit 0 against stale live servers silently validates a temp `:8014` instance — live quarantine can appear green while production listener is stale.
3. **Playwright branch fragility:** With `SUPABASE_*` exported, `smoke_app_shell_store_read.py` aborts on Playwright timeout before HTTP quarantine checks print; consider running without Supabase creds for route-only smokes (task 53 pattern) or hardening script error handling (out of scope here).
4. **Server degradation:** After Playwright load against `:8004`, `/health` stopped responding within 3s; further smokes were blocked without restarting the server (intentionally not done in this task).

## Validation evidence

| Evidence | Location |
|----------|----------|
| Quarantine routes in repo | `main_centerline_FIXER.py` — `_quarantine_legacy_read()`, handlers at ~2061, ~3053, ~3062 |
| Task 46 partial quarantine closeout | `results/46_quarantine_dead_read_routes.md` |
| Task 50 smoke expectation updates | `results/50_smoke_quarantine_routes.md` |
| Task 53 invocation pattern | `results/53_53verify-smoke-scripts.md` |
| Timestamps | Task start `2026-06-17T16:18:33Z`; server hung observed ~16:19 UTC |

## Rollback command

```bash
# No product changes to revert.
rm -f results/54_54run-quarantine-smoke-tests.md
```

## Rejected scope

Per task hard stops, the following were **not** attempted:

- Starting, stopping, or restarting the `:8004` backend server
- Modifying route handlers, middleware, or smoke scripts
- Sourcing `.env` / injecting credentials beyond what was already exported in the shell
- Database, schema, migration, or secrets changes
- Renderer / math / overlay fixes for Playwright timeouts

## Result

**VERIFIED** — closeout artifact exists with per-route verdict table, invocation commands, raw output, overall verdict (**PARTIAL**), and actionable findings for stale-server restart and smoke-script environment caveats.
