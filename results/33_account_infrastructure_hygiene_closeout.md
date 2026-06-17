# PHASE CLOSEOUT: Account Infrastructure Hygiene

Status: COMPLETE for frontend/runtime reproducibility.

## Summary

The account/profile frontend runtime is now reproducible from a fresh git checkout.
Previously-untracked core account files have been committed, and the application shell,
auth flow, Supabase bootstrap, and store bridge are all tracked and served by committed
backend routes.

## Checkpoint commits

- `7712df3` profiles: rename and soft archive from Profile Management
- `84bf239` accounts: track auth and Supabase store bridge
- `3522a02` accounts: track Supabase client and user profile bootstrap

## Files now tracked for account runtime

- `app_shell.html` — main account/profile shell (rename + soft archive, honest copy)
- `account_drawer.js` — account drawer, profile controls, logout
- `first_profile_intake.js` — first profile + birth record intake
- `auth.html` — login / signup / password reset page
- `auth_guard.js` — session guard + `window.logout()`
- `user_profile.js` — `window.CurrentUser` / `window.CurrentUserReady` bootstrap
- `supabase_client.js` — `window.SupabaseReady` / `window.SupabaseClient` bootstrap
- `supabase_store_bridge.js` — live Supabase store assembler (`window.SupabaseStoreReady`)

These are served by committed backend routes in `main_centerline_FIXER.py`
(`/supabase_client.js`, `/auth_guard.js`, `/user_profile.js`, `/supabase_store_bridge.js`,
`/first_profile_intake.js`, `/account_drawer.js`, `/auth.html`, `/app_shell.html`,
`/config/supabase`).

## Remaining caveats

- `main_centerline_FIXER.py` and `repositories/profiles_repository.py` still carry
  unrelated/uncommitted backend drift (RLS-scoped `/profiles` listing). This is separate
  from frontend account runtime completeness and should be committed or discarded on its own.
- `phase2_cache_scheduler.js` remains OUT of account scope (sandbox/prototype, not part of
  account infrastructure). It stays untracked for this phase.
- Large unrelated untracked workspace drift (artifacts, sandboxes, validation outputs,
  binaries, docs) remains and is not part of this phase.

## Next recommended phase

Application Shell & Drawer Architecture.

## First next task

Audit the boundaries between `app_shell.html`, `account_drawer.js`, and the Profile
Management UI before implementing anything: map responsibilities, shared globals
(`window.__rmAppShell`, `window.CurrentUser`), duplicated profile/default logic, and
navigation/handoff seams. Read-only audit first, no implementation.
