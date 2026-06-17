-- ================================================================
-- DRAFT MIGRATION — DO NOT APPLY
-- Account / Workspace layer + RLS skeletons
-- File:   2026_06_12_account_workspace_rls_draft.sql
-- Status: DESIGN ARTIFACT. Not validated, not applied, no data changed.
-- Pairs:  docs/architecture/ACCOUNT_WORKSPACE_RLS_PLAN_v1_2026-06-12.md
-- ----------------------------------------------------------------
-- This file ABORTS if executed. Remove the guard block (Section 0)
-- ONLY after human review + staging validation with the publishable key.
-- ================================================================

-- ================================================================
-- 0. SAFETY GUARD  (delete this block to enable the migration)
-- ================================================================
do $guard$
begin
  raise exception
    'DRAFT migration: review ACCOUNT_WORKSPACE_RLS_PLAN_v1 and validate on staging before applying. Remove Section 0 guard to proceed.';
end $guard$;

-- Sentinel reused as the legacy dev account id (greppable + reversible):
--   00000000-0000-0000-0000-000000000000

create extension if not exists "pgcrypto";

-- ================================================================
-- 1. ACCOUNTS  (the workspace / ownership boundary)
-- ================================================================
create table if not exists accounts (
  id           uuid primary key default gen_random_uuid(),
  name         text not null,
  account_type text not null default 'personal'
               check (account_type in ('personal','professional','family','organization')),
  created_by   uuid references auth.users(id) on delete set null,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  archived_at  timestamptz
);

-- ================================================================
-- 2. ACCOUNT MEMBERSHIPS  (auth.users <-> accounts, many-to-many)
-- ================================================================
create table if not exists account_memberships (
  id          uuid primary key default gen_random_uuid(),
  account_id  uuid not null references accounts(id) on delete cascade,
  user_id     uuid not null references auth.users(id) on delete cascade,
  role        text not null default 'owner'
              check (role in ('owner','admin','member','assistant','viewer')),
  invited_by  uuid references auth.users(id) on delete set null,
  accepted_at timestamptz,                 -- null = pending invitation
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  archived_at timestamptz,
  unique (account_id, user_id)
);

create index if not exists idx_memberships_user    on account_memberships(user_id);
create index if not exists idx_memberships_account on account_memberships(account_id);

-- ================================================================
-- 3. ACCESS HELPERS  (SECURITY DEFINER avoids RLS recursion on memberships)
-- ================================================================
create or replace function app_account_ids()
returns setof uuid
language sql stable security definer
set search_path = public
as $fn$
  select account_id
  from account_memberships
  where user_id = auth.uid()
    and accepted_at is not null
    and archived_at is null
$fn$;

create or replace function app_has_account_role(target_account uuid, roles text[])
returns boolean
language sql stable security definer
set search_path = public
as $fn$
  select exists (
    select 1 from account_memberships
    where user_id = auth.uid()
      and account_id = target_account
      and role = any(roles)
      and accepted_at is not null
      and archived_at is null
  )
$fn$;

-- ================================================================
-- 4. profiles.account_id  (account_user_id kept during transition — Open Q1)
-- ================================================================
alter table profiles
  add column if not exists account_id uuid references accounts(id) on delete cascade;
create index if not exists idx_profiles_account_id on profiles(account_id);
-- AFTER cutover only:  alter table profiles drop column account_user_id;

-- ================================================================
-- 5. DENORMALIZED account_id ON CHILDREN  (Open Q2 — recommended)
--    Makes every child policy:  account_id in (select app_account_ids())
-- ================================================================
alter table birth_records            add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table intention_profiles       add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table current_location_history add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table location_events          add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table favorite_places          add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table visited_places           add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table saved_searches           add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table comparison_sets          add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table comparison_set_places    add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table notes                    add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table share_links              add column if not exists account_id uuid references accounts(id) on delete cascade;
alter table user_settings            add column if not exists account_id uuid references accounts(id) on delete cascade;

create index if not exists idx_birth_records_account_id            on birth_records(account_id);
create index if not exists idx_intention_profiles_account_id       on intention_profiles(account_id);
create index if not exists idx_current_location_account_id         on current_location_history(account_id);
create index if not exists idx_location_events_account_id          on location_events(account_id);
create index if not exists idx_favorite_places_account_id          on favorite_places(account_id);
create index if not exists idx_visited_places_account_id           on visited_places(account_id);
create index if not exists idx_saved_searches_account_id           on saved_searches(account_id);
create index if not exists idx_comparison_sets_account_id          on comparison_sets(account_id);
create index if not exists idx_comparison_set_places_account_id    on comparison_set_places(account_id);
create index if not exists idx_notes_account_id                    on notes(account_id);
create index if not exists idx_share_links_account_id              on share_links(account_id);
create index if not exists idx_user_settings_account_id            on user_settings(account_id);

-- Optional integrity guard: keep child.account_id == its profile's account_id.
-- create or replace function app_set_account_from_profile()
-- returns trigger language plpgsql as $trg$
-- begin
--   if new.account_id is null and new.profile_id is not null then
--     select account_id into new.account_id from profiles where id = new.profile_id;
--   end if;
--   return new;
-- end $trg$;
-- (attach a BEFORE INSERT/UPDATE trigger per child table if desired)

-- ================================================================
-- 6. user_settings uniqueness fix
-- ================================================================
create unique index if not exists uq_user_settings_account_default
  on user_settings(account_id) where profile_id is null;
create unique index if not exists uq_user_settings_profile
  on user_settings(account_id, profile_id) where profile_id is not null;

-- ================================================================
-- 7. share_links: default visibility -> private + value check
-- ================================================================
alter table share_links alter column visibility set default 'private';
alter table share_links
  add constraint share_links_visibility_chk
  check (visibility in ('private','unlisted','public'));
-- Existing rows keep current value; review/flip manually during backfill.

-- ================================================================
-- 8. BACKFILL  (DML — COMMENTED. Review line-by-line; run only at cutover)
-- ================================================================
-- 8a. Legacy account reusing the all-zero sentinel:
-- insert into accounts (id, name, account_type)
-- values ('00000000-0000-0000-0000-000000000000','Legacy Dev Account','personal')
-- on conflict (id) do nothing;
--
-- 8b. Point existing profiles at the legacy account:
-- update profiles set account_id = '00000000-0000-0000-0000-000000000000'
--  where account_user_id = '00000000-0000-0000-0000-000000000000' and account_id is null;
--
-- 8c. Denormalize account_id onto children from their profile (repeat per table):
-- update birth_records            c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update intention_profiles       c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update current_location_history c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update location_events          c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update favorite_places          c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update visited_places           c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update saved_searches           c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update comparison_sets          c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update notes                    c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
-- update share_links              c set account_id = p.account_id from profiles p where c.profile_id = p.id and c.account_id is null;
--
-- 8d. comparison_set_places via its set:
-- update comparison_set_places csp set account_id = cs.account_id
--   from comparison_sets cs where csp.comparison_set_id = cs.id and csp.account_id is null;
--
-- 8e. user_settings: map account_user_id -> account_id:
-- update user_settings set account_id = '00000000-0000-0000-0000-000000000000'
--  where account_user_id = '00000000-0000-0000-0000-000000000000' and account_id is null;
--
-- 8f. When the FIRST REAL user signs up (replace :new_uid):
-- insert into account_memberships (account_id, user_id, role, accepted_at)
-- values ('00000000-0000-0000-0000-000000000000', ':new_uid', 'owner', now());
--   (Alternative: create a fresh account and DELETE the smoke-test profiles instead.)
--
-- 8g. After verification, make account_id NOT NULL (per table):
-- alter table profiles      alter column account_id set not null;
-- alter table birth_records alter column account_id set not null;  -- ... etc.

-- ================================================================
-- 9. RLS SKELETONS  (COMMENTED — enable only after backfill verified)
--    Pattern: every owned table => account_id in (select app_account_ids())
-- ================================================================
-- ---- 9.1 accounts -------------------------------------------------
-- alter table accounts enable row level security;
-- create policy accounts_select on accounts for select
--   using (id in (select app_account_ids()));
-- create policy accounts_update on accounts for update
--   using (app_has_account_role(id, array['owner','admin']))
--   with check (app_has_account_role(id, array['owner','admin']));
-- create policy accounts_delete on accounts for delete
--   using (app_has_account_role(id, array['owner']));
-- -- INSERT: typically via SECURITY DEFINER signup RPC that also creates the owner membership.
--
-- ---- 9.2 account_memberships -------------------------------------
-- alter table account_memberships enable row level security;
-- create policy memberships_select on account_memberships for select
--   using (user_id = auth.uid() or account_id in (select app_account_ids()));
-- create policy memberships_write on account_memberships for all
--   using (app_has_account_role(account_id, array['owner','admin']))
--   with check (app_has_account_role(account_id, array['owner','admin']));
--
-- ---- 9.3 profiles + all denormalized children -------------------
-- alter table profiles enable row level security;
-- create policy profiles_all on profiles for all
--   using (account_id in (select app_account_ids()))
--   with check (account_id in (select app_account_ids()));
-- -- Repeat the SAME for each child (birth_records, intention_profiles,
-- -- current_location_history, location_events, favorite_places, visited_places,
-- -- saved_searches, comparison_sets, comparison_set_places, notes, user_settings):
-- -- alter table <child> enable row level security;
-- -- create policy <child>_all on <child> for all
-- --   using (account_id in (select app_account_ids()))
-- --   with check (account_id in (select app_account_ids()));
--
-- ---- 9.4 places (global reference) -------------------------------
-- alter table places enable row level security;
-- create policy places_read on places for select to authenticated using (true);
-- -- Open Q5: add `to anon` if logged-out share pages must render a map.
-- -- Writes: no policy => only service_role (admin ingest) can write.
--
-- ---- 9.5 share_links: owner CRUD + anon public read by slug -------
-- alter table share_links enable row level security;
-- create policy share_links_owner on share_links for all
--   using (account_id in (select app_account_ids()))
--   with check (account_id in (select app_account_ids()));
-- create policy share_links_public_read on share_links for select to anon
--   using (visibility in ('public','unlisted')
--          and revoked_at is null
--          and (expires_at is null or expires_at > now()));
-- -- IMPORTANT: this exposes the share_links ROW only. The shared TARGET
-- -- (birth_records / comparison_sets) must be served by a SECURITY DEFINER
-- -- RPC / Edge Function that validates the slug and applies hide_birth_data
-- -- and include_* flags. Do NOT add anon read policies to data tables. (Open Q4)

-- ================================================================
-- 10. ROLLBACK (reverse order; run only to undo an applied version)
-- ================================================================
-- drop policy if exists share_links_public_read on share_links;
-- drop policy if exists share_links_owner on share_links;
-- ... drop remaining policies ...
-- alter table share_links disable row level security;  -- (repeat per enabled table)
-- drop index if exists uq_user_settings_account_default;
-- drop index if exists uq_user_settings_profile;
-- alter table share_links drop constraint if exists share_links_visibility_chk;
-- alter table share_links alter column visibility set default 'public';
-- alter table <each table> drop column if exists account_id;
-- drop function if exists app_has_account_role(uuid, text[]);
-- drop function if exists app_account_ids();
-- drop table if exists account_memberships;
-- drop table if exists accounts;
-- -- Backfill undo: update <tables> set account_id = null where account_id = '00000000-...';

-- ================================================================
-- END DRAFT — nothing above runs while Section 0 guard is present.
-- ================================================================
