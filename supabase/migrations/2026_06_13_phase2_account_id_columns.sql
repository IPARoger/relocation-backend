-- Phase 2: Add nullable account_id to all 13 carrying tables.
-- NO NOT NULL, NO composite FKs, NO triggers, NO RLS.
-- Safe to run on a live schema; all operations are additive only.

alter table profiles
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table birth_records
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table intention_profiles
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table current_location_history
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table location_events
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table favorite_places
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table visited_places
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table saved_searches
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table comparison_sets
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table comparison_set_places
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table notes
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table share_links
  add column if not exists account_id uuid references accounts(id) on delete set null;

alter table user_settings
  add column if not exists account_id uuid references accounts(id) on delete set null;

-- Indexes for future RLS performance (one per table)
create index if not exists idx_profiles_account_id             on profiles             (account_id);
create index if not exists idx_birth_records_account_id        on birth_records        (account_id);
create index if not exists idx_intention_profiles_account_id   on intention_profiles   (account_id);
create index if not exists idx_current_location_history_acct   on current_location_history (account_id);
create index if not exists idx_location_events_account_id      on location_events      (account_id);
create index if not exists idx_favorite_places_account_id      on favorite_places      (account_id);
create index if not exists idx_visited_places_account_id       on visited_places       (account_id);
create index if not exists idx_saved_searches_account_id       on saved_searches       (account_id);
create index if not exists idx_comparison_sets_account_id      on comparison_sets      (account_id);
create index if not exists idx_comparison_set_places_acct      on comparison_set_places (account_id);
create index if not exists idx_notes_account_id                on notes                (account_id);
create index if not exists idx_share_links_account_id          on share_links          (account_id);
create index if not exists idx_user_settings_account_id        on user_settings        (account_id);
