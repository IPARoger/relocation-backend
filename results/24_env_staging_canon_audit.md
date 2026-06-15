# RESULT: 24_ENV_STAGING_CANON_AUDIT

Task: `24_ENV_STAGING_CANON_AUDIT`
Mode: read-only audit; documentation output only
Source evidence: `results/23_profile_rename_copy_and_live_smoke.md`
Result: **VERIFIED**

## Scope

Inspected only the requested env/runtime evidence:

- `.env.example`
- `.env`
- `.env.staging`
- `main_centerline_FIXER.py`
- `supabase_store_bridge.js`
- `first_profile_intake.js`
- `scripts/`
- `results/23_profile_rename_copy_and_live_smoke.md`

No secrets were printed or recorded. API keys and service-role keys were treated as redacted.

## Findings

### 1. Which env file does the running backend use in normal local QA?

Normal local QA currently uses `.env.staging`, because the established QA commands start uvicorn after sourcing `.env.staging`.

Evidence from `results/23_profile_rename_copy_and_live_smoke.md`:

- The active DB was identified as `.env.staging`.
- The backend uvicorn process and Playwright QA smokes were noted as sourcing `.env.staging`.
- The frontend reads Supabase config from backend endpoint `/config/supabase`, so the backend process environment controls which Supabase project app shell/map QA uses.

Important caveat: `main_centerline_FIXER.py` itself calls `load_dotenv()` in `/config/supabase`. With python-dotenv defaults, that loads `.env` when the process environment has not already been populated. It does not, by itself, select `.env.staging`.

So the practical canon is:

- Correct local QA startup: source `.env.staging` before running the backend.
- Risky startup: run backend without sourcing `.env.staging`; then `/config/supabase` can fall back to `.env`.

### 2. Which Supabase project is active for `app_shell` / map QA?

The active QA Supabase project is the `.env.staging` project:

- `.env.staging`: `rnwlrdtqhfjhpllryxiz`

This is the project used by the successful Task 23 live rename smoke. It has the expected Web2/current schema, including `profiles.account_id`, and is consistent with these runtime paths:

- `supabase_store_bridge.js` filters active tables by `account_id`.
- `first_profile_intake.js` inserts `account_id` into `profiles` and `birth_records`.
- Task 23 used an RLS-authenticated client against this project and successfully performed:
  - `profiles.update({ display_name }).eq("id", id).eq("account_id", accountId)`

### 3. Is `.env` stale, legacy, or still used anywhere?

`.env` appears stale/legacy for the current Web2 app shell/map QA path.

Evidence:

- `.env` points to Supabase project `dpmtmmryvlftfahipowa`.
- Task 23 found that project has an older `profiles` schema where `account_user_id` exists but `account_id` does not.
- That stale schema would break the current frontend/runtime contract, because current code expects `account_id`.

However, `.env` is still a possible fallback because:

- `main_centerline_FIXER.py` calls `load_dotenv()` without specifying `.env.staging`.
- `scripts/patch_admin1_names.py` explicitly tries `.env.staging` first, then falls back to `.env`.
- `.env.example` currently points at the same project ref as `.env` (`dpmtmmryvlftfahipowa`), which could mislead future setup/agents.

Conclusion: `.env` should be treated as **legacy/stale unless explicitly proven otherwise**. It is not the authoritative DB for current app shell/map QA.

### 4. Does any script or runtime path still read `.env` when it should read `.env.staging`?

Yes, there are two risk paths:

1. `main_centerline_FIXER.py`
   - `/config/supabase` imports `load_dotenv` and calls `load_dotenv()`.
   - This is safe only when `.env.staging` values have already been exported into the process environment before backend startup.
   - If not, it can read `.env`, causing the frontend to connect to the stale DB.

2. `scripts/patch_admin1_names.py`
   - Its own comments say it loads `.env.staging` first and falls back to `.env`.
   - That fallback is intentional in the script, but now risky because `.env` is stale for current QA.

Other scripts inspected mostly rely on already-exported environment variables (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`) or `BASE_URL`. `scripts/ingest_cities_to_places.py` explicitly documents `source .env.staging`.

### 5. Minimal documentation or guardrail needed

Minimum documentation:

- Add a short env canon note near setup/QA instructions stating:
  - `.env.staging` is the authoritative local QA environment for `app_shell.html` and `map_CURRENT.html`.
  - `.env` is legacy/stale and must not be used for app shell/map validation unless intentionally auditing legacy data.
  - Start backend QA with `set -a && source .env.staging && set +a`, then run uvicorn.
  - Confirm `/config/supabase` resolves to project ref `rnwlrdtqhfjhpllryxiz` before live data validation.

Minimum technical guardrail:

- Change `/config/supabase` or backend startup to fail closed if `SUPABASE_URL` resolves to known-stale project `dpmtmmryvlftfahipowa` during app shell/map QA.
- Alternatively, make `main_centerline_FIXER.py` load `.env.staging` explicitly in local QA mode, or require an explicit `REL_BACKEND_ENV=staging` / `SUPABASE_ENV=staging` before serving `/config/supabase`.
- Update `scripts/patch_admin1_names.py` to warn loudly, require a flag, or abort before falling back to `.env`.
- Update `.env.example` so it does not point at the stale project ref, or label it as placeholder-only.

## Answers

1. Running backend normal local QA: `.env.staging`, when started using the established QA command that sources `.env.staging` before uvicorn. The backend code itself can fall back to `.env` if not started that way.
2. Active Supabase project for app shell/map QA: `.env.staging` project `rnwlrdtqhfjhpllryxiz`.
3. `.env` status: stale/legacy for current Web2 QA; still physically present and still reachable through fallback paths.
4. Paths that can still read `.env`: `main_centerline_FIXER.py` via default `load_dotenv()` if staging values are not pre-exported; `scripts/patch_admin1_names.py` via explicit fallback.
5. Minimal guardrail: document `.env.staging` as canonical for local QA and add a fail-closed check/warning so agents cannot silently query `dpmtmmryvlftfahipowa` for current app shell/map validation.

## Scope verification

- No production files modified.
- No env secrets printed.
- Documentation written to `audits/24_env_staging_canon_audit.md` and `results/24_env_staging_canon_audit.md`.

VERIFIED
