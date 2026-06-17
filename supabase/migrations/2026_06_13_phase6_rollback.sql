-- Phase 6 rollback.
-- Removes the signup bootstrap trigger and function.
-- Does NOT remove any accounts or memberships that were already created.
-- Safe to apply at any time; existing user data is unaffected.

drop trigger if exists on_auth_user_created on auth.users;
drop function if exists public.handle_new_user();

-- To verify rollback:
--   select count(*) from pg_trigger where tgname = 'on_auth_user_created';   -- expect 0
--   select count(*) from pg_proc p join pg_namespace n on n.oid = p.pronamespace
--     where p.proname = 'handle_new_user' and n.nspname = 'public';           -- expect 0
