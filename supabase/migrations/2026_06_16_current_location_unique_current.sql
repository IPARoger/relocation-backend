-- Enforce a single active current-location row per (account_id, profile_id).
--
-- Background: current-location writes flip prior rows to is_current=false and
-- insert a new is_current=true row. Without this constraint, a failed retire or
-- a race could leave multiple current rows. The bridge/account-store reads pick
-- "the" current row, so duplicates are a correctness hazard.
--
-- Partial unique index: only is_current=true rows participate, so historical
-- (is_current=false) rows remain unconstrained.

create unique index if not exists current_location_one_current_per_profile
  on current_location_history (account_id, profile_id)
  where is_current = true;

-- Supporting lookup index for the active-row read path.
create index if not exists idx_current_location_current_lookup
  on current_location_history (account_id, profile_id, selected_at desc)
  where is_current = true;

-- Rollback:
--   drop index if exists current_location_one_current_per_profile;
--   drop index if exists idx_current_location_current_lookup;
