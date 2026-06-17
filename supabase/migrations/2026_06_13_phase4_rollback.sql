-- Phase 4 rollback.
-- Exact reversal of 2026_06_13_phase4_integrity_lock.sql.
-- All object names verified live against staging (2026-06-13).
--
-- PRE-CONDITIONS (both must be true before applying):
--   1. Phase 5 rollback has already been applied
--      (2026_06_13_phase5_rollback.sql). Phase 5 RLS policies reference the
--      constraint structure built in Phase 4. Apply rollbacks in reverse phase
--      order: P6 → P5 → P4 → P2 → P1.
--   2. All carrying tables have zero rows, OR you accept that removing NOT NULL
--      and composite FKs leaves existing rows with unvalidated account_id
--      relationships. On clean staging / post-Option-A production this is safe.
--
-- This rollback is constraint-only. It does not DELETE or UPDATE any data.
--
-- Rollback order (dependency-safe):
--   R1. Drop 12 BEFORE triggers            (depend on trigger function)
--   R2. Drop trigger function              (safe after all triggers gone)
--   R3. Drop 13 composite FKs             (must precede R7: reference UNIQUE targets)
--   R4. Drop 2 partial unique indexes     (no FK dependency)
--   R5. Remove share_links visibility     (check constraint + column default)
--   R6. Remove NOT NULL from 13 columns   (after FKs removed)
--   R7. Drop 2 UNIQUE(id, account_id)     (MUST follow R3)
--   R8. Restore 13 original single-column FKs

-- ─────────────────────────────────────────────────────────────────────────────
-- R1: Drop 12 BEFORE INSERT/UPDATE triggers
-- ─────────────────────────────────────────────────────────────────────────────

drop trigger if exists trg_birth_records_set_account             on birth_records;
drop trigger if exists trg_intention_profiles_set_account        on intention_profiles;
drop trigger if exists trg_current_location_history_set_account  on current_location_history;
drop trigger if exists trg_location_events_set_account           on location_events;
drop trigger if exists trg_favorite_places_set_account           on favorite_places;
drop trigger if exists trg_visited_places_set_account            on visited_places;
drop trigger if exists trg_saved_searches_set_account            on saved_searches;
drop trigger if exists trg_comparison_sets_set_account           on comparison_sets;
drop trigger if exists trg_notes_set_account                     on notes;
drop trigger if exists trg_share_links_set_account               on share_links;
drop trigger if exists trg_comparison_set_places_set_account     on comparison_set_places;
drop trigger if exists trg_user_settings_set_account             on user_settings;

-- ─────────────────────────────────────────────────────────────────────────────
-- R2: Drop trigger function
-- ─────────────────────────────────────────────────────────────────────────────

drop function if exists public.app_set_account_from_parent();

-- ─────────────────────────────────────────────────────────────────────────────
-- R3: Drop 13 composite FKs
-- ─────────────────────────────────────────────────────────────────────────────

alter table birth_records             drop constraint if exists birth_records_profile_account_fkey;
alter table intention_profiles        drop constraint if exists intention_profiles_profile_account_fkey;
alter table current_location_history  drop constraint if exists current_location_history_profile_account_fkey;
alter table location_events           drop constraint if exists location_events_profile_account_fkey;
alter table favorite_places           drop constraint if exists favorite_places_profile_account_fkey;
alter table visited_places            drop constraint if exists visited_places_profile_account_fkey;
alter table saved_searches            drop constraint if exists saved_searches_profile_account_fkey;
alter table comparison_sets           drop constraint if exists comparison_sets_profile_account_fkey;
alter table notes                     drop constraint if exists notes_profile_account_fkey;
alter table share_links               drop constraint if exists share_links_profile_account_fkey;
alter table comparison_set_places     drop constraint if exists comparison_set_places_cset_account_fkey;
alter table user_settings             drop constraint if exists user_settings_profile_account_fkey;
alter table user_settings             drop constraint if exists user_settings_account_id_cascade_fkey;

-- ─────────────────────────────────────────────────────────────────────────────
-- R4: Drop 2 partial unique indexes on user_settings
-- ─────────────────────────────────────────────────────────────────────────────

drop index if exists public.user_settings_account_default_uniq;
drop index if exists public.user_settings_profile_uniq;

-- ─────────────────────────────────────────────────────────────────────────────
-- R5: Remove share_links visibility changes
-- ─────────────────────────────────────────────────────────────────────────────

alter table share_links
  drop constraint if exists share_links_visibility_check,
  alter column visibility drop default;

-- ─────────────────────────────────────────────────────────────────────────────
-- R6: Remove NOT NULL from all 13 account_id columns
-- ─────────────────────────────────────────────────────────────────────────────

alter table profiles                  alter column account_id drop not null;
alter table comparison_sets           alter column account_id drop not null;
alter table birth_records             alter column account_id drop not null;
alter table intention_profiles        alter column account_id drop not null;
alter table current_location_history  alter column account_id drop not null;
alter table location_events           alter column account_id drop not null;
alter table favorite_places           alter column account_id drop not null;
alter table visited_places            alter column account_id drop not null;
alter table saved_searches            alter column account_id drop not null;
alter table comparison_set_places     alter column account_id drop not null;
alter table notes                     alter column account_id drop not null;
alter table share_links               alter column account_id drop not null;
alter table user_settings             alter column account_id drop not null;

-- ─────────────────────────────────────────────────────────────────────────────
-- R7: Drop UNIQUE(id, account_id) on profiles and comparison_sets
--     MUST follow R3 — these were the FK targets for composite FKs.
-- ─────────────────────────────────────────────────────────────────────────────

alter table profiles         drop constraint if exists profiles_id_account_id_uniq;
alter table comparison_sets  drop constraint if exists comparison_sets_id_account_id_uniq;

-- ─────────────────────────────────────────────────────────────────────────────
-- R8: Restore 13 original single-column FKs
--
--     ON DELETE behavior per Phase 4 commentary and standard schema convention:
--       - 10 profile-owned child tables: ON DELETE CASCADE
--       - comparison_set_places -> comparison_sets: ON DELETE CASCADE
--       - user_settings -> profiles: ON DELETE CASCADE
--       - user_settings -> accounts: ON DELETE SET NULL
--         (Phase 4 explicitly "upgrades from SET NULL to CASCADE"; restoring)
-- ─────────────────────────────────────────────────────────────────────────────

alter table birth_records
  add constraint birth_records_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table intention_profiles
  add constraint intention_profiles_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table current_location_history
  add constraint current_location_history_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table location_events
  add constraint location_events_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table favorite_places
  add constraint favorite_places_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table visited_places
  add constraint visited_places_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table saved_searches
  add constraint saved_searches_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table comparison_sets
  add constraint comparison_sets_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table notes
  add constraint notes_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table share_links
  add constraint share_links_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

alter table comparison_set_places
  add constraint comparison_set_places_comparison_set_id_fkey
    foreign key (comparison_set_id) references comparison_sets(id)
    on delete cascade;

alter table user_settings
  add constraint user_settings_profile_id_fkey
    foreign key (profile_id) references profiles(id)
    on delete cascade;

-- account_id is nullable after R6, making ON DELETE SET NULL valid again
alter table user_settings
  add constraint user_settings_account_id_fkey
    foreign key (account_id) references accounts(id)
    on delete set null;
