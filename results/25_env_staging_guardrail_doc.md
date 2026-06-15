# RESULT: 25_ENV_STAGING_GUARDRAIL_DOC

Task: `25_ENV_STAGING_GUARDRAIL_DOC`
Mode: documentation only
Allowed file: `docs/architecture/ENV_STAGING_CANON.md` (created)
Source evidence: `audits/24_env_staging_canon_audit.md`, `results/24_env_staging_canon_audit.md`
Result: **VERIFIED**

## What was written

Created `docs/architecture/ENV_STAGING_CANON.md`, a short env canon note for future agents.

## Required content check

1. `.env.staging` stated authoritative for app_shell/map local QA — yes (TL;DR + Rule).
2. Active project ref `rnwlrdtqhfjhpllryxiz` stated — yes.
3. `.env` project ref `dpmtmmryvlftfahipowa` stated stale/legacy for current Web2 QA — yes.
4. Exact startup command included — yes: `set -a && source .env.staging && set +a`.
5. Warning that `main_centerline_FIXER.py` `load_dotenv()` can fall back to `.env` if staging
   is not sourced first — yes (Why this matters / known footgun).
6. Rule: do not run app_shell/map data validation against `.env` unless explicitly auditing
   legacy data — yes (Rule).
7. No secrets printed — yes (only project refs and a startup command; no keys/tokens).

## Scope verification

- No production code modified.
- Only the allowed doc `docs/architecture/ENV_STAGING_CANON.md` and this result file were written.
- No env secrets printed.

VERIFIED
