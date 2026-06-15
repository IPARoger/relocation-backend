# AUDIT: 30_ACCOUNT_MANAGEMENT_CHECKPOINT_AUDIT

Task: `30_ACCOUNT_MANAGEMENT_CHECKPOINT_AUDIT`
Mode: read-only checkpoint audit; documentation output only
Result: **VERIFIED**
Commit-readiness verdict: **READY WITH CONDITIONS** (scoped commit + explicit decisions below)

## 1. What profile/account-management capabilities are now real?

- First-profile intake with honest copy (Task 20): creates a profile + birth/chart record; copy now states current location is set separately, later.
- Profile **Rename** from Profile Management cards (Task 22): RLS-scoped Supabase client write to `profiles.display_name`, trimmed, blank rejected, scoped by `id` + `account_id`.
- Profile **Archive (soft)** from Profile Management cards (Task 28, Phase B): sets `profiles.archived_at`/`updated_at`, scoped by `id` + `account_id` + `archived_at IS NULL`, with:
  - last-active-profile guard,
  - replacement-default selection (keep current default if valid, else first remaining),
  - `default_chart_record_id` repair only when the archived profile was default,
  - persisted active-profile repair only when it pointed at the archived profile,
  - reload/navigate behavior.
- Honest UI copy across shell screens (earlier honesty series carried in the same working tree): resume-context stub, export/share status, "Screen 2 — Map Launcher", Screen 4 actions, must-not lines.
- Backend (present in working tree but OUT OF PHASE, see Q3/Q6): RLS-scoped `GET /profiles` via `list_profiles_for_user` (`main_centerline_FIXER.py`, `repositories/profiles_repository.py`).

## 2. Which were live-smoked?

- **Rename** — live, reversible smoke on staging (Task 23): display_name changed and reverted; children preserved; birth record untouched.
- **Archive** — live, reversible smoke on staging (Task 29): soft-archive parent only; target removed from active list; children preserved (birth_records, favorite_places, saved_searches, comparison_sets, comparison_set_places); effective-default repaired to replacement; fully restored (archived_at -> null; created settings row deleted); independent service-role re-read confirmed original state.

Both used `.env.staging` (`rnwlrdtqhfjhpllryxiz`) and an owner-authenticated, RLS-respecting client.

Not re-smoked this phase: first-profile intake persistence (audited in Task 19; only copy changed in Task 20).

## 3. Which files changed across Tasks 20-29?

Production code:
- `app_shell.html` — rename (22), archive (28), must-not copy (23/28). NOTE: the same uncommitted working copy ALSO contains the earlier honesty-fix series (Tasks ~07-16: RESUME_CONTEXT_STUB, Screen 2 Map Launcher, screenExport, "Export / share status", "Back to shell map"). These were never committed, so they ride along in any commit of this file.
- `first_profile_intake.js` — Task 20 copy only (title, subtitle, birth-city helper text).

Docs:
- `docs/architecture/ENV_STAGING_CANON.md` — new (Task 25).
- `audits/18,19,21,24,26,27_*.md` and `results/18-30_*.md` — phase audit/result records.

Out-of-phase tracked drift (NOT in the Tasks 20-29 allowed-file set; from an earlier session):
- `main_centerline_FIXER.py` — RLS-scoped `/profiles` endpoint.
- `repositories/profiles_repository.py` — new `list_profiles_for_user`.
- `docs/product/FUTURE_FEATURES_ROADMAP.md` (+20), `docs/resolutions/MICRO_DECISION_LOG_v1_2026-06-02.md` (+53).

Untracked core production files (never committed, not gitignored):
- `supabase_store_bridge.js` (referenced throughout this phase's audits), `auth.html`, `auth_guard.js`, `phase2_cache_scheduler.js`.

## 4. Remaining honesty/copy issues before commit?

- Minor: the Archive confirmation says "You can restore it later from the database." There is no self-serve unarchive UI. This is technically accurate (admin/DB restore proven in Task 29) but implies a user-facing capability that does not exist. Consider softening (e.g. "Archived profiles can be restored by support.") or removing the clause. Low severity; not a blocker.
- No other misleading copy found. Rename and Archive are now real, so removing them from the must-not line was correct.

## 5. Remaining unvalidated code paths before commit?

- DOM event flow for Rename and Archive (button click -> `window.confirm`/`window.prompt` -> Supabase write -> reload/navigate) was validated at the QUERY level (smokes replicated the exact queries) plus `node --check` syntax and logic-branch presence. It was NOT exercised end-to-end in a browser (no Playwright run this phase).
- Archive `updated_at` fallback branch (retry with `{ archived_at }` only) was never triggered — the live write succeeded with `updated_at`, so the fallback path is unexercised.
- Backend RLS `/profiles` drift (`list_profiles_for_user`) is unvalidated in this phase.
- First-profile intake persistence not re-run this phase (only copy changed).

None are correctness blockers given the query-level live smokes, but they are the gaps to close next.

## 6. Exact files to INCLUDE in the checkpoint commit

Core (validated this phase — recommend commit):
- `app_shell.html`
- `first_profile_intake.js`
- `docs/architecture/ENV_STAGING_CANON.md`
- `audits/18_profile_add_rename_archive_audit.md`
- `audits/19_first_profile_intake_audit.md`
- `audits/21_profile_rename_archive_scope_plan.md`
- `audits/24_env_staging_canon_audit.md`
- `audits/26_profile_archive_backend_readiness_audit.md`
- `audits/27_profile_archive_phase_b_plan.md`
- `audits/30_account_management_checkpoint_audit.md`
- `results/18_*.md` through `results/30_*.md` (18,19,20,21,22,23,24,25,26,27,28,29,30)

Decision-required (flag to human — do NOT auto-bundle silently):
- `supabase_store_bridge.js` — untracked CORE dependency referenced by this phase. Recommend INCLUDE (the repo is currently missing a production file), but acknowledge it has never been tracked, so its full contents enter history now.
- `main_centerline_FIXER.py`, `repositories/profiles_repository.py` — coherent account-mgmt RLS backend changes but OUT OF PHASE and unvalidated here. Recommend a SEPARATE commit (e.g. "profiles: RLS-scoped /profiles listing") rather than folding into this UI checkpoint.
- `docs/product/FUTURE_FEATURES_ROADMAP.md`, `docs/resolutions/MICRO_DECISION_LOG_v1_2026-06-02.md` — include if they document this work; otherwise separate.
- `auth.html`, `auth_guard.js`, `phase2_cache_scheduler.js` — untracked production files; tracking them is a git-hygiene decision separate from this checkpoint.

## 7. Exact files to EXCLUDE from the checkpoint commit

- Secrets: `.env`, `.env.local`, `.env.staging` (already gitignored — never commit).
- All untracked binary/artifact files: `*.png`, `*.jpeg`, `*.pdf`, `*.zip`, `*.key`, `Mockups/`, `Tear Sheet*/`, `Tear Sheets*/`, `Unsplash images/`, `Color Swatches/`, `Fonts and Glyphs/`, `images/`.
- Sandbox/prototype scratch: `map_SANDBOX_*.html`, `prototype_*.html`, `Old File/`, `validation/` outputs, `validation_screenshots/`.
- Any `*.bak*` working backups.
- Terminal capture files (not in repo).

## 8. Suggested commit message

```
profiles: rename + soft archive from Profile Management; honest UI/intake copy; env-staging canon

- Profile Management: add Rename (Phase A) and soft Archive (Phase B)
  with last-profile guard, replacement-default selection, and persisted
  active-profile repair; RLS-scoped Supabase client writes (id + account_id).
- Honest copy across shell screens (resume, export/share, map launcher,
  Screen 4) and first-profile intake.
- Add docs/architecture/ENV_STAGING_CANON.md (staging is authoritative for
  app_shell/map local QA; .env is stale/legacy).
- Rename and archive live-smoked reversibly on staging; children preserved.
```

(Use a separate commit for the backend RLS `/profiles` changes if those are included.)

## 9. Next phase after commit

1. Phase C: backend ownership hardening for the `/profiles/{id}/archive` route before any frontend uses it; validate `list_profiles_for_user`.
2. Browser-level E2E (Playwright) for the Rename/Archive DOM flow (click -> confirm -> write -> reload), including the `updated_at` fallback path.
3. Product decision on unarchive: either add a restore UI or soften the "restore from the database" copy.
4. Git hygiene: track core production files (`supabase_store_bridge.js`, `auth.html`, `auth_guard.js`) and add `.gitignore` rules for artifacts/sandboxes to stop 450+ untracked files from obscuring real changes.

## Scope verification

- No production files modified.
- Read-only inspection of `app_shell.html`, `first_profile_intake.js`, `docs/architecture/ENV_STAGING_CANON.md`, and `results/`.
- Written to `audits/30_account_management_checkpoint_audit.md` and `results/30_account_management_checkpoint_audit.md`.

VERIFIED
