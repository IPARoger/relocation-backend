# RESULT: 53_verify-smoke-scripts

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/53_53verify-smoke-scripts.md

## Files changed

| File | Change |
|------|--------|
| `results/53_53verify-smoke-scripts.md` | Closeout report (this file) |

No application, schema, backend, or smoke-script source files were modified.

Diagnostic artifacts written during execution (evidence only, not product changes):

- `validation/reports/task53_smoke_run.log` — full sequential run log with per-script tails
- `/tmp/smoke_smoke_*.py.out` — per-script stdout/stderr captures (ephemeral)

## Exact changes

Read-only inventory and execution of all 60 `scripts/smoke_*.py` scripts via:

```bash
./venv/bin/python scripts/<smoke_script>.py
```

Scripts were run sequentially against the live local server at `http://127.0.0.1:8004` (health returned `{"status":"ok"}` before and after the run). Playwright/Chromium was available in the venv from task 52.

## Validation evidence

### Pre-run environment

```text
$ date -u
Wed Jun 17 16:06:29 UTC 2026

$ curl -s http://127.0.0.1:8004/health
{"status":"ok"}

$ ./venv/bin/python -c "import playwright; print('playwright import ok')"
playwright import ok

$ ls scripts/smoke_*.py | wc -l
60
```

### Execution summary

| Metric | Value |
|--------|-------|
| Total scripts | 60 |
| PASS | 29 |
| FAIL | 31 |
| Wall time | ~476s (2026-06-17T16:06:36Z → 16:14:32Z) |

```text
FINAL SUMMARY pass=29 fail=31 total=60
```

### Per-script results

| Script | Result | Exit | Duration |
|--------|--------|------|----------|
| `smoke_account_store_read.py` | PASS | 0 | 2s |
| `smoke_app_shell_context_transport.py` | FAIL | 1 | 16s |
| `smoke_app_shell_map_handoff.py` | FAIL | 1 | 16s |
| `smoke_app_shell_store_read.py` | PASS | 0 | 3s |
| `smoke_chart_record_birth_bridge.py` | FAIL | 1 | 16s |
| `smoke_chart_record_library_read.py` | FAIL | 1 | 16s |
| `smoke_comparison_sets.py` | FAIL | 1 | 0s |
| `smoke_current_location_backend.py` | FAIL | 1 | 0s |
| `smoke_current_location_frontend.py` | FAIL | 1 | 0s |
| `smoke_favorites.py` | FAIL | 1 | 0s |
| `smoke_genie_handoff_transport_v2.py` | FAIL | 1 | 16s |
| `smoke_genie_map_engine.py` | FAIL | 1 | 32s |
| `smoke_genie_product_integration_slice1.py` | FAIL | 1 | 15s |
| `smoke_genie_sandbox.py` | PASS | 0 | 2s |
| `smoke_legacy_writes_deprecated.py` | PASS | 0 | 0s |
| `smoke_library_handoff.py` | FAIL | 1 | 0s |
| `smoke_library_scaffold.py` | PASS | 0 | 5s |
| `smoke_local_product_store.py` | PASS | 0 | 0s |
| `smoke_map_current.py` | FAIL | 1 | 0s |
| `smoke_map_current_aura_debug.py` | FAIL | 1 | 3s |
| `smoke_map_saved_investigation_note.py` | FAIL | 1 | 0s |
| `smoke_notes_backend.py` | FAIL | 1 | 0s |
| `smoke_notes_frontend.py` | FAIL | 1 | 0s |
| `smoke_phase2_10_observer_contract.py` | PASS | 0 | 1s |
| `smoke_phase2_11_execution_policy_contract.py` | PASS | 0 | 0s |
| `smoke_phase2_12_runtime_bridge_dev.py` | PASS | 0 | 0s |
| `smoke_phase2_13_execution_runtime_dev.py` | PASS | 0 | 1s |
| `smoke_phase2_14_fetch_bridge_dev.py` | PASS | 0 | 1s |
| `smoke_phase2_15_renderer_hydration_sandbox.py` | PASS | 0 | 0s |
| `smoke_phase2_16_multi_overlay_sandbox.py` | PASS | 0 | 1s |
| `smoke_phase2_17_viewport_hydration_sandbox.py` | PASS | 0 | 0s |
| `smoke_phase2_18_progressive_refinement_sandbox.py` | PASS | 0 | 1s |
| `smoke_phase2_19_adaptive_density_sandbox.py` | PASS | 0 | 0s |
| `smoke_phase2_20_ambiguity_domain_sandbox.py` | PASS | 0 | 1s |
| `smoke_phase2_21_implication_field_sandbox.py` | PASS | 0 | 0s |
| `smoke_phase2_22_emergence_field_sandbox.py` | PASS | 0 | 1s |
| `smoke_phase2_23_cross_domain_continuity_sandbox.py` | PASS | 0 | 1s |
| `smoke_phase2_24_production_readiness_contract.py` | PASS | 0 | 0s |
| `smoke_phase2_25_production_shadow_adapter_dev.py` | PASS | 0 | 1s |
| `smoke_phase2_26_real_map_shadow_adapter.py` | FAIL | 1 | 33s |
| `smoke_phase2_27_real_map_shadow_self_check.py` | FAIL | 1 | 33s |
| `smoke_phase2_28_in_page_readiness_evaluation.py` | FAIL | 1 | 32s |
| `smoke_phase2_29_visible_readiness_indicator.py` | FAIL | 1 | 33s |
| `smoke_phase2_30_dev_overlay_container.py` | FAIL | 1 | 32s |
| `smoke_phase2_31_renderer_adjacent_metadata.py` | FAIL | 1 | 32s |
| `smoke_phase2_32_dev_renderer_integration.py` | FAIL | 1 | 32s |
| `smoke_phase2_33_isolated_debug_test_layer.py` | FAIL | 1 | 33s |
| `smoke_phase2_4_cache_contract.py` | PASS | 0 | 0s |
| `smoke_phase2_5_scheduler_contract.py` | PASS | 0 | 0s |
| `smoke_phase2_6_cache_store_contract.py` | PASS | 0 | 0s |
| `smoke_phase2_7_orchestration_contract.py` | PASS | 0 | 0s |
| `smoke_phase2_8_mock_runtime_harness.py` | PASS | 0 | 0s |
| `smoke_phase2_9_execution_bridge_contract.py` | PASS | 0 | 0s |
| `smoke_phase2_cache.py` | PASS | 0 | 2s |
| `smoke_place_resolution.py` | FAIL | 1 | 0s |
| `smoke_profile_create.py` | FAIL | 1 | 0s |
| `smoke_profile_rename_archive.py` | FAIL | 1 | 0s |
| `smoke_saved_investigations.py` | FAIL | 1 | 1s |
| `smoke_settings_account.py` | FAIL | 1 | 0s |
| `smoke_substrate_adapter.py` | FAIL | 1 | 61s |

### Failure root-cause buckets (31 failures)

**A. Missing Supabase env in shell (14 scripts)** — scripts exit immediately with:

```text
FAIL: Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
```

Affected: `smoke_comparison_sets.py`, `smoke_current_location_backend.py`, `smoke_current_location_frontend.py`, `smoke_favorites.py`, `smoke_library_handoff.py`, `smoke_map_current.py`, `smoke_map_saved_investigation_note.py`, `smoke_notes_backend.py`, `smoke_notes_frontend.py`, `smoke_place_resolution.py`, `smoke_profile_create.py`, `smoke_profile_rename_archive.py`, `smoke_saved_investigations.py`, `smoke_settings_account.py`.

Note: `.env` exists locally with `SUPABASE_URL=...` but was not sourced/exported into the runner shell (hard-stop: no credential injection in this task).

**B. Playwright `wait_for_function` timeout (16 scripts)** — page readiness hooks never satisfied within 15–60s:

```text
playwright._impl._errors.TimeoutError: Page.wait_for_function: Timeout 15000ms exceeded.
```

Representative scripts: `smoke_app_shell_context_transport.py`, `smoke_app_shell_map_handoff.py`, `smoke_chart_record_birth_bridge.py`, `smoke_chart_record_library_read.py`, `smoke_genie_handoff_transport_v2.py`, `smoke_genie_map_engine.py`, `smoke_genie_product_integration_slice1.py`, `smoke_phase2_26_real_map_shadow_adapter.py` through `smoke_phase2_33_isolated_debug_test_layer.py`, `smoke_substrate_adapter.py`.

**C. Playwright runtime TypeError (1 script)** — `smoke_map_current_aura_debug.py`:

```text
playwright._impl._errors.Error: Page.wait_for_function: TypeError: Cannot read properties of null (reading 'disabled')
```

### Sample passing output

```text
$ ./venv/bin/python scripts/smoke_account_store_read.py
PASS: health_200 — status=200
PASS: account_store_410 — {"error": "Gone", "reason": "legacy read path retired"}
PASS: account_store_auth_410 — {"error": "Gone", "reason": "legacy read path retired"}
PASS: smoke_account_store_read
exit: 0
```

```text
$ ./venv/bin/python scripts/smoke_phase2_cache.py
PASS: phase2_cache_smoke
exit: 0
```

### Post-run environment

```text
$ curl -s http://127.0.0.1:8004/health
{"status":"ok"}
```

Full per-script tails: `validation/reports/task53_smoke_run.log`

## Rollback procedure

```bash
# No product changes to revert.
rm -f validation/reports/task53_smoke_run.log validation/reports/task53_smoke_run.json
rm -f /tmp/smoke_smoke_*.py.out
```

## Rejected scope

Per task hard stops, the following were **not** attempted:

- **Credentials / secrets** — did not source `.env` or export `SUPABASE_*` keys into the runner environment.
- **Backend / schema / database writes** — no server config, migrations, or data mutations.
- **Renderer / math / overlay fixes** — Playwright timeout and aura-debug TypeError failures were diagnosed only, not patched.
- **Smoke-script or application code changes** — task authorized read-only inventory only.

## Remaining unknowns

- Whether the 16 Playwright-timeout failures would pass with Supabase env exported (some spawn servers and load authenticated pages).
- Whether `smoke_map_current_aura_debug.py` failure is env-related or a genuine UI/DOM regression.
- Whether a documented smoke-runner wrapper (env load + server preflight) exists elsewhere in the repo; none was found under `scripts/run*`.

## Result

**NOT VERIFIED** — 29/60 smoke scripts passed; 31/60 failed. End-to-end functionality is **not** fully intact under the current local execution environment (missing exported Supabase env; multiple Playwright readiness timeouts).
