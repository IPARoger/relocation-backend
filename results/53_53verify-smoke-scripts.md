# RESULT: 53_53verify-smoke-scripts

**Author:** Cursor (results/ lane)  
**Originating task:** tasks/53_53verify-smoke-scripts.md  
**Branch:** `cursor/verify-smoke-scripts-c417`

## Files changed

| File | Change |
|------|--------|
| `results/53_53verify-smoke-scripts.md` | Closeout report (this file) |

No application, schema, smoke-script, or dependency files were modified.

## Exact changes

- Inventoried all `scripts/smoke_*.py` files (59 total).
- Installed runtime prerequisites needed to execute smokes in this Linux sandbox (Playwright Python package, Chromium browser binaries, backend Python deps via `pip`; `python3-dev` for `pyswisseph` build).
- Executed every smoke script sequentially (`timeout 300 python3 scripts/<script>` per script).
- Re-ran a server-dependent subset with `uvicorn main_centerline_FIXER:app` listening on `127.0.0.1:8004` to isolate port/env failures from script logic.

## Validation evidence

### Pre-run inventory

```text
$ ls scripts/smoke_*.py | wc -l
59

$ python3 --version
Python 3.12.3

$ python3 -m pip show playwright | head -2
Name: playwright
Version: 1.60.0

$ ls ~/.cache/ms-playwright/
chromium-1223
chromium_headless_shell-1223
ffmpeg-1011

$ test -f .env.staging && echo present || echo absent
absent

$ readlink /workspace/venv/bin/python
python3.11 -> /opt/homebrew/opt/python@3.11/bin/python3.11  (macOS path; not executable on Linux)
```

### Batch execution command

```bash
for f in scripts/smoke_*.py; do
  timeout 300 python3 "$f" >"/tmp/smoke_runs/${f##*/}.log" 2>&1
  echo "$f exit=$?"
done
```

### Summary (initial run, no server, no Supabase env)

| Metric | Value |
|--------|-------|
| Total scripts | 59 |
| PASS (exit 0) | 22 |
| FAIL (exit non-zero) | 37 |
| Pass rate | 37.3% |

### Full results table (initial run)

| Script | Result | Seconds |
|--------|--------|---------|
| smoke_account_store_read.py | FAIL | 0 |
| smoke_app_shell_context_transport.py | FAIL | 0 |
| smoke_app_shell_map_handoff.py | FAIL | 0 |
| smoke_app_shell_store_read.py | FAIL | 0 |
| smoke_chart_record_birth_bridge.py | FAIL | 1 |
| smoke_chart_record_library_read.py | FAIL | 0 |
| smoke_comparison_sets.py | FAIL | 0 |
| smoke_current_location_backend.py | FAIL | 0 |
| smoke_current_location_frontend.py | FAIL | 0 |
| smoke_favorites.py | FAIL | 0 |
| smoke_genie_handoff_transport_v2.py | FAIL | 0 |
| smoke_genie_map_engine.py | FAIL | 0 |
| smoke_genie_product_integration_slice1.py | FAIL | 0 |
| smoke_genie_sandbox.py | FAIL | 0 |
| smoke_legacy_writes_deprecated.py | FAIL | 0 |
| smoke_library_handoff.py | FAIL | 1 |
| smoke_library_scaffold.py | FAIL | 2 |
| smoke_local_product_store.py | **PASS** | 0 |
| smoke_map_current_aura_debug.py | FAIL | 0 |
| smoke_map_current.py | FAIL | 1 |
| smoke_map_saved_investigation_note.py | FAIL | 0 |
| smoke_notes_backend.py | FAIL | 0 |
| smoke_notes_frontend.py | FAIL | 0 |
| smoke_phase2_10_observer_contract.py | **PASS** | 0 |
| smoke_phase2_11_execution_policy_contract.py | **PASS** | 0 |
| smoke_phase2_12_runtime_bridge_dev.py | **PASS** | 1 |
| smoke_phase2_13_execution_runtime_dev.py | **PASS** | 0 |
| smoke_phase2_14_fetch_bridge_dev.py | FAIL | 0 |
| smoke_phase2_15_renderer_hydration_sandbox.py | **PASS** | 1 |
| smoke_phase2_16_multi_overlay_sandbox.py | **PASS** | 0 |
| smoke_phase2_17_viewport_hydration_sandbox.py | **PASS** | 1 |
| smoke_phase2_18_progressive_refinement_sandbox.py | **PASS** | 0 |
| smoke_phase2_19_adaptive_density_sandbox.py | **PASS** | 1 |
| smoke_phase2_20_ambiguity_domain_sandbox.py | **PASS** | 0 |
| smoke_phase2_21_implication_field_sandbox.py | **PASS** | 1 |
| smoke_phase2_22_emergence_field_sandbox.py | **PASS** | 0 |
| smoke_phase2_23_cross_domain_continuity_sandbox.py | **PASS** | 0 |
| smoke_phase2_24_production_readiness_contract.py | **PASS** | 1 |
| smoke_phase2_25_production_shadow_adapter_dev.py | **PASS** | 0 |
| smoke_phase2_26_real_map_shadow_adapter.py | FAIL | 0 |
| smoke_phase2_27_real_map_shadow_self_check.py | FAIL | 0 |
| smoke_phase2_28_in_page_readiness_evaluation.py | FAIL | 0 |
| smoke_phase2_29_visible_readiness_indicator.py | FAIL | 0 |
| smoke_phase2_30_dev_overlay_container.py | FAIL | 0 |
| smoke_phase2_31_renderer_adjacent_metadata.py | FAIL | 0 |
| smoke_phase2_32_dev_renderer_integration.py | FAIL | 0 |
| smoke_phase2_33_isolated_debug_test_layer.py | FAIL | 0 |
| smoke_phase2_4_cache_contract.py | **PASS** | 0 |
| smoke_phase2_5_scheduler_contract.py | **PASS** | 0 |
| smoke_phase2_6_cache_store_contract.py | **PASS** | 0 |
| smoke_phase2_7_orchestration_contract.py | **PASS** | 0 |
| smoke_phase2_8_mock_runtime_harness.py | **PASS** | 0 |
| smoke_phase2_9_execution_bridge_contract.py | **PASS** | 0 |
| smoke_place_resolution.py | FAIL | 1 |
| smoke_profile_create.py | FAIL | 0 |
| smoke_profile_rename_archive.py | FAIL | 0 |
| smoke_saved_investigations.py | FAIL | 0 |
| smoke_settings_account.py | FAIL | 0 |
| smoke_substrate_adapter.py | FAIL | 0 |

### Representative PASS output

```text
$ python3 scripts/smoke_local_product_store.py
PASS: smoke_local_product_store
  round-trip: client + investigation + favorite + comparison + history
  settings_snapshot: persisted
  default_chart_record_id: persisted
  one birth_profile per client: enforced
  forbidden keys: rejected
  committed scaffold: 3 Chart Records + shell ID parity
exit: 0

$ python3 scripts/smoke_phase2_4_cache_contract.py
  "all_pass": true
exit: 0
```

### Failure root-cause buckets (initial run)

| Category | Count | Example error |
|----------|-------|---------------|
| Missing Supabase credentials (`.env.staging` absent) | 10 | `FAIL: Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY` |
| Broken `venv/bin/python` (macOS Homebrew symlink) | 10 | `FileNotFoundError: ... '/workspace/venv/bin/python'` |
| Backend not running (`Connection refused` on default `8004`) | 9 | `urllib.error.URLError: <urlopen error [Errno 111] Connection refused>` |
| Backend expected on port `8000` (not `8004`) | 10 | `Server not reachable at http://127.0.0.1:8000/health` |
| `supabase-py` not installed / namespace shadowed by `supabase/` dir | 2 | `ImportError: cannot import name 'create_client' from 'supabase'` |

### Supplemental run with backend on port 8004

```text
$ curl -sf http://127.0.0.1:8004/health
{"status":"ok"}

$ python3 scripts/smoke_account_store_read.py
PASS: health_200 — status=200
PASS: account_store_410 — {"error": "Gone", "reason": "legacy read path retired"}
PASS: account_store_auth_410 — {"error": "Gone", "reason": "legacy read path retired"}
PASS: smoke_account_store_read
exit: 0
```

Other server-dependent scripts still failed in this supplemental run because they require port `8000`, Supabase env, or a working `venv/bin/python` to spawn their own server process.

### Scripts that passed without external server or credentials (22)

All Phase 2 contract/sandbox smokes except `smoke_phase2_14_fetch_bridge_dev.py`, plus `smoke_local_product_store.py`. These exercise in-process JS contracts via Node or file-only Python logic.

## Rollback procedure

```bash
# No application changes to revert; only this closeout file was added.
git checkout main -- results/53_53verify-smoke-scripts.md && rm -f results/53_53verify-smoke-scripts.md
```

## Rejected scope

- **Schema / backend / database / migration / renderer / math / overlay changes** — hard stops; not authorized and not required for smoke verification.
- **Credentials / secrets** — `.env.staging` is absent in this environment; Supabase-dependent smokes (10 scripts) were executed and documented as failing on missing env, but credentials were not provisioned (hard stop).
- **Fixing `venv/bin/python` symlink or smoke-script port defaults** — would modify repo or scripts; out of read-only task scope.
- **Installing `supabase-py` or resolving `supabase/` package namespace conflict** — would change environment/deps beyond read-only diagnosis; documented as blocker for 2 backend smokes.
- **Modifying smoke scripts, CI, or application code** — explicitly excluded by task scope.

## Remaining unknowns

- Whether the 37 failing scripts pass on a fully configured developer machine (Linux venv, `.env.staging`, backend on both `8000` and `8004` as needed).
- Browser smokes (`smoke_map_current.py`, profile/account smokes) were not validated end-to-end because Supabase credentials were unavailable.
- `smoke_phase2_14_fetch_bridge_dev.py` failed only on `backend_available` against port `8000`; contract logic itself was not re-tested on a live backend.

## Result

**NOT VERIFIED** — 22 of 59 smoke scripts passed (37.3%). The full suite does not pass in this environment due to missing backend server at expected ports, absent Supabase staging credentials, broken macOS-origin `venv/bin/python` symlink, and missing `supabase-py` package. End-to-end functionality is not confirmed intact.
