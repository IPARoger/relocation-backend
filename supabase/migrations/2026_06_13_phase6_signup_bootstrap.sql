-- Phase 6: Signup bootstrap.
-- Creates handle_new_user() SECURITY DEFINER + AFTER INSERT trigger on auth.users.
-- Every new auth user automatically receives one personal account
-- and one owner membership (accepted_at = now()) before any RLS
-- policies are consulted, because the function runs as its definer
-- (postgres) and bypasses RLS entirely.

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. Bootstrap function
-- ─────────────────────────────────────────────────────────────────────────────

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $fn_handle_new_user$
declare
  v_account_id uuid;
begin
  -- Create a personal account owned by the new auth user
  insert into public.accounts (name, account_type, created_by)
  values ('Personal', 'personal', new.id)
  returning id into v_account_id;

  -- Create owner membership, auto-accepted (accepted_at required by app_account_ids())
  insert into public.account_memberships (account_id, user_id, role, accepted_at)
  values (v_account_id, new.id, 'owner', now());

  return new;
end;
$fn_handle_new_user$;

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. Trigger on auth.users AFTER INSERT
-- ─────────────────────────────────────────────────────────────────────────────

drop trigger if exists on_auth_user_created on auth.users;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ─────────────────────────────────────────────────────────────────────────────
-- Rollback (if needed):
--   drop trigger if exists on_auth_user_created on auth.users;
--   drop function if exists public.handle_new_user();
-- ─────────────────────────────────────────────────────────────────────────────
