-- Phase 4: Integrity lock.
-- Constraint ordering per spec §3:
--   1. UNIQUE(id, account_id) targets
--   2. NOT NULL on all 13 carrying tables
--   3. Composite FKs NOT VALID (drop old single-column FK, add composite)
--   4. VALIDATE each composite FK
--   5. Trigger function + BEFORE INSERT/UPDATE triggers
--   6. user_settings partial unique indexes
--   7. share_links default + check constraint

-- ──────────────────────────────────────────────────────────────────────────────
-- STEP 1: UNIQUE targets (must exist before composite FKs reference them)
-- ──────────────────────────────────────────────────────────────────────────────

alter table profiles
  add constraint profiles_id_account_id_uniq unique (id, account_id);

alter table comparison_sets
  add constraint comparison_sets_id_account_id_uniq unique (id, account_id);

-- ──────────────────────────────────────────────────────────────────────────────
-- STEP 2: NOT NULL (targets must be non-null before composite FKs assume presence)
-- ──────────────────────────────────────────────────────────────────────────────

alter table profiles                  alter column account_id set not null;
alter table comparison_sets           alter column account_id set not null;
alter table birth_records             alter column account_id set not null;
alter table intention_profiles        alter column account_id set not null;
alter table current_location_history  alter column account_id set not null;
alter table location_events           alter column account_id set not null;
alter table favorite_places           alter column account_id set not null;
alter table visited_places            alter column account_id set not null;
alter table saved_searches            alter column account_id set not null;
alter table comparison_set_places     alter column account_id set not null;
alter table notes                     alter column account_id set not null;
alter table share_links               alter column account_id set not null;
alter table user_settings             alter column account_id set not null;

-- ──────────────────────────────────────────────────────────────────────────────
-- STEP 3: Composite FKs — drop old single-column profile_id FK, add composite
-- (added NOT VALID so no full table scan; validated in step 4)
-- ──────────────────────────────────────────────────────────────────────────────

-- birth_records
alter table birth_records
  drop constraint birth_records_profile_id_fkey,
  add constraint birth_records_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- intention_profiles
alter table intention_profiles
  drop constraint intention_profiles_profile_id_fkey,
  add constraint intention_profiles_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- current_location_history
alter table current_location_history
  drop constraint current_location_history_profile_id_fkey,
  add constraint current_location_history_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- location_events
alter table location_events
  drop constraint location_events_profile_id_fkey,
  add constraint location_events_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- favorite_places
alter table favorite_places
  drop constraint favorite_places_profile_id_fkey,
  add constraint favorite_places_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- visited_places
alter table visited_places
  drop constraint visited_places_profile_id_fkey,
  add constraint visited_places_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- saved_searches
alter table saved_searches
  drop constraint saved_searches_profile_id_fkey,
  add constraint saved_searches_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- comparison_sets
alter table comparison_sets
  drop constraint comparison_sets_profile_id_fkey,
  add constraint comparison_sets_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- notes
alter table notes
  drop constraint notes_profile_id_fkey,
  add constraint notes_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- share_links
alter table share_links
  drop constraint share_links_profile_id_fkey,
  add constraint share_links_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    on update cascade on delete cascade not valid;

-- comparison_set_places → comparison_sets composite
alter table comparison_set_places
  drop constraint comparison_set_places_comparison_set_id_fkey,
  add constraint comparison_set_places_cset_account_fkey
    foreign key (comparison_set_id, account_id) references comparison_sets(id, account_id)
    on update cascade on delete cascade not valid;

-- user_settings: per-profile composite (MATCH SIMPLE → profile_id IS NULL rows not enforced)
alter table user_settings
  drop constraint user_settings_profile_id_fkey,
  add constraint user_settings_profile_account_fkey
    foreign key (profile_id, account_id) references profiles(id, account_id)
    match simple on update cascade on delete cascade not valid;

-- user_settings: account-level FK — upgrade from SET NULL to CASCADE
alter table user_settings
  drop constraint user_settings_account_id_fkey,
  add constraint user_settings_account_id_cascade_fkey
    foreign key (account_id) references accounts(id)
    on delete cascade not valid;

-- ──────────────────────────────────────────────────────────────────────────────
-- STEP 4: VALIDATE composite FKs (separate step; no exclusive lock on full scan)
-- ──────────────────────────────────────────────────────────────────────────────

alter table birth_records             validate constraint birth_records_profile_account_fkey;
alter table intention_profiles        validate constraint intention_profiles_profile_account_fkey;
alter table current_location_history  validate constraint current_location_history_profile_account_fkey;
alter table location_events           validate constraint location_events_profile_account_fkey;
alter table favorite_places           validate constraint favorite_places_profile_account_fkey;
alter table visited_places            validate constraint visited_places_profile_account_fkey;
alter table saved_searches            validate constraint saved_searches_profile_account_fkey;
alter table comparison_sets           validate constraint comparison_sets_profile_account_fkey;
alter table notes                     validate constraint notes_profile_account_fkey;
alter table share_links               validate constraint share_links_profile_account_fkey;
alter table comparison_set_places     validate constraint comparison_set_places_cset_account_fkey;
alter table user_settings             validate constraint user_settings_profile_account_fkey;
alter table user_settings             validate constraint user_settings_account_id_cascade_fkey;

-- ──────────────────────────────────────────────────────────────────────────────
-- STEP 5: Trigger function + BEFORE INSERT/UPDATE triggers on all children
-- ──────────────────────────────────────────────────────────────────────────────

create or replace function app_set_account_from_parent()
returns trigger
language plpgsql
security definer
set search_path = public
as $fn_account_from_parent$
begin
  if new.account_id is null then
    if tg_table_name = 'comparison_set_places' then
      new.account_id := (select account_id from comparison_sets where id = new.comparison_set_id);
    else
      -- profile_id-owned tables; account-level user_settings (profile_id IS NULL) = no-op
      if new.profile_id is not null then
        new.account_id := (select account_id from profiles where id = new.profile_id);
      end if;
    end if;
  end if;
  return new;
end;
$fn_account_from_parent$;

create trigger trg_birth_records_set_account
  before insert or update of profile_id on birth_records
  for each row execute function app_set_account_from_parent();

create trigger trg_intention_profiles_set_account
  before insert or update of profile_id on intention_profiles
  for each row execute function app_set_account_from_parent();

create trigger trg_current_location_history_set_account
  before insert or update of profile_id on current_location_history
  for each row execute function app_set_account_from_parent();

create trigger trg_location_events_set_account
  before insert or update of profile_id on location_events
  for each row execute function app_set_account_from_parent();

create trigger trg_favorite_places_set_account
  before insert or update of profile_id on favorite_places
  for each row execute function app_set_account_from_parent();

create trigger trg_visited_places_set_account
  before insert or update of profile_id on visited_places
  for each row execute function app_set_account_from_parent();

create trigger trg_saved_searches_set_account
  before insert or update of profile_id on saved_searches
  for each row execute function app_set_account_from_parent();

create trigger trg_comparison_sets_set_account
  before insert or update of profile_id on comparison_sets
  for each row execute function app_set_account_from_parent();

create trigger trg_notes_set_account
  before insert or update of profile_id on notes
  for each row execute function app_set_account_from_parent();

create trigger trg_share_links_set_account
  before insert or update of profile_id on share_links
  for each row execute function app_set_account_from_parent();

create trigger trg_comparison_set_places_set_account
  before insert or update of comparison_set_id on comparison_set_places
  for each row execute function app_set_account_from_parent();

create trigger trg_user_settings_set_account
  before insert or update of profile_id on user_settings
  for each row execute function app_set_account_from_parent();

-- ──────────────────────────────────────────────────────────────────────────────
-- STEP 6: user_settings partial unique indexes
-- ──────────────────────────────────────────────────────────────────────────────

-- One account-level user_settings per account (profile_id IS NULL)
create unique index if not exists user_settings_account_default_uniq
  on user_settings (account_id) where profile_id is null;

-- One per-profile user_settings per profile
create unique index if not exists user_settings_profile_uniq
  on user_settings (profile_id) where profile_id is not null;

-- ──────────────────────────────────────────────────────────────────────────────
-- STEP 7: share_links visibility — default 'private', add value check
-- ──────────────────────────────────────────────────────────────────────────────

alter table share_links
  alter column visibility set default 'private',
  add constraint share_links_visibility_check
    check (visibility in ('private','unlisted','public'));
