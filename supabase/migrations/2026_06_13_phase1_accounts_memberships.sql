-- ================================================================
-- PHASE 1 — Structural tables
-- accounts, account_memberships, helper functions
-- ================================================================
-- Target:   STAGING ONLY until Phase 4.5 gate passes
-- Apply to: fresh staging Supabase project
-- Safe:     purely additive; no existing tables altered
-- Rollback: drop functions, drop account_memberships, drop accounts
-- ================================================================

-- ----------------------------------------------------------------
-- 1. accounts
-- ----------------------------------------------------------------
create table if not exists accounts (
  id           uuid        primary key default gen_random_uuid(),
  name         text        not null,
  account_type text        not null default 'personal'
                           check (account_type in (
                             'personal', 'professional', 'family', 'organization'
                           )),
  created_by   uuid        references auth.users(id) on delete set null,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  archived_at  timestamptz
);

-- ----------------------------------------------------------------
-- 2. account_memberships
-- ----------------------------------------------------------------
create table if not exists account_memberships (
  id          uuid        primary key default gen_random_uuid(),
  account_id  uuid        not null references accounts(id) on delete cascade,
  user_id     uuid        not null references auth.users(id) on delete cascade,
  role        text        not null default 'owner'
                          check (role in (
                            'owner', 'admin', 'member', 'assistant', 'viewer'
                          )),
  invited_by  uuid        references auth.users(id) on delete set null,
  accepted_at timestamptz,          -- null = invitation pending
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  archived_at timestamptz,
  unique (account_id, user_id)
);

create index if not exists idx_memberships_user
  on account_memberships (user_id);

create index if not exists idx_memberships_account
  on account_memberships (account_id);

-- ----------------------------------------------------------------
-- 3. Helper: app_account_ids()
--    Returns the set of account ids the calling auth user belongs to
--    (accepted, non-archived memberships only).
--    SECURITY DEFINER + pinned search_path prevents escalation.
-- ----------------------------------------------------------------
create or replace function app_account_ids()
returns setof uuid
language sql stable security definer
set search_path = public
as $fn_account_ids$
  select account_id
  from   account_memberships
  where  user_id     = auth.uid()
  and    accepted_at is not null
  and    archived_at is null
$fn_account_ids$;

-- ----------------------------------------------------------------
-- 4. Helper: app_has_account_role(account, roles[])
--    Returns true if the calling user holds one of the given roles
--    on the specified account.
--    Used by Phase 5 admin-level policies; defined here for review.
-- ----------------------------------------------------------------
create or replace function app_has_account_role(
  target_account uuid,
  roles          text[]
)
returns boolean
language sql stable security definer
set search_path = public
as $fn_has_role$
  select exists (
    select 1
    from   account_memberships
    where  user_id     = auth.uid()
    and    account_id  = target_account
    and    role        = any(roles)
    and    accepted_at is not null
    and    archived_at is null
  )
$fn_has_role$;

-- ================================================================
-- Phase 1 validation queries (run manually after apply)
-- ================================================================
-- 1. Tables exist:
--      select table_name from information_schema.tables
--      where table_schema = 'public'
--      and   table_name   in ('accounts', 'account_memberships');
--    Expected: 2 rows.
--
-- 2. Functions exist with SECURITY DEFINER + correct search_path:
--      select routine_name, security_type
--      from   information_schema.routines
--      where  routine_schema = 'public'
--      and    routine_name   in ('app_account_ids', 'app_has_account_role');
--    Expected: 2 rows, security_type = 'DEFINER'.
--
-- 3. All 15 existing tables unchanged (row counts match baseline):
--      Run phase0 baseline script and compare counts.
--
-- 4. Rollback (if needed — reverse order):
--      drop function if exists app_has_account_role(uuid, text[]);
--      drop function if exists app_account_ids();
--      drop table  if exists account_memberships;
--      drop table  if exists accounts;
-- ================================================================
