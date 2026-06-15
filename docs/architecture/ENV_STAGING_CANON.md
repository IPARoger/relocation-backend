# Environment Canon — Local QA (app_shell / map)

Status: authoritative for current Web2 QA
Scope: which environment file and Supabase project to use when validating
`app_shell.html` and `map_CURRENT.html` locally.

## TL;DR

- Use `.env.staging`. It is authoritative for app_shell / map local QA.
- Active Supabase project ref: `rnwlrdtqhfjhpllryxiz`.
- Do NOT use `.env` for current Web2 QA. Its project ref `dpmtmmryvlftfahipowa`
  is stale/legacy and has an older schema (e.g. `profiles` without `account_id`),
  which causes false alarms.

## Startup command (always source staging first)

```
set -a && source .env.staging && set +a
```

Then start the backend (uvicorn) and run app_shell / map QA. Optionally confirm
`/config/supabase` resolves to project ref `rnwlrdtqhfjhpllryxiz` before any live
data validation.

## Why this matters / known footgun

`main_centerline_FIXER.py` calls `load_dotenv()`. With python-dotenv defaults this
can fall back to `.env` if `.env.staging` was not sourced into the process
environment first. If that happens, the frontend (which fetches config from the
backend `/config/supabase`) will silently connect to the stale legacy project.

Always source `.env.staging` before launching the backend so the staging values
are already exported and take precedence.

## Rule

Do not run app_shell / map data validation against `.env` unless you are
explicitly auditing legacy data in project `dpmtmmryvlftfahipowa`. For all current
Web2 QA, `.env.staging` (`rnwlrdtqhfjhpllryxiz`) is the only authoritative source.

## References

- `audits/24_env_staging_canon_audit.md`
- `results/24_env_staging_canon_audit.md`
