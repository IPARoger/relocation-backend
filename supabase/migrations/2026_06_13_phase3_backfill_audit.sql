-- Phase 3: Backfill audit for clean staging.
-- This is a READ-ONLY validation script. No DML is executed.
-- On clean staging (Option A), all carrying tables have 0 rows,
-- so backfill is a confirmed no-op.

-- AUDIT 1: accounts + memberships row counts (must be 0)
select 'accounts'           as table_name, count(*) as rows from accounts
union all
select 'account_memberships',              count(*) from account_memberships;

-- AUDIT 2: Carrying table row counts + non-null account_id counts
select 'profiles'              as tbl, count(*) as total_rows, count(account_id) as assigned from profiles union all
select 'birth_records',         count(*), count(account_id) from birth_records union all
select 'intention_profiles',    count(*), count(account_id) from intention_profiles union all
select 'current_location_history', count(*), count(account_id) from current_location_history union all
select 'location_events',       count(*), count(account_id) from location_events union all
select 'favorite_places',       count(*), count(account_id) from favorite_places union all
select 'visited_places',        count(*), count(account_id) from visited_places union all
select 'saved_searches',        count(*), count(account_id) from saved_searches union all
select 'comparison_sets',       count(*), count(account_id) from comparison_sets union all
select 'comparison_set_places', count(*), count(account_id) from comparison_set_places union all
select 'notes',                 count(*), count(account_id) from notes union all
select 'share_links',           count(*), count(account_id) from share_links union all
select 'user_settings',         count(*), count(account_id) from user_settings
order by tbl;

-- AUDIT 3: Drift audit — any row where account_id is set but
-- the account_id does not exist in accounts (should be 0)
select 'profiles_drift'    as check_name, count(*) as drift_count from profiles        where account_id is not null and account_id not in (select id from accounts) union all
select 'birth_records_drift',             count(*) from birth_records                   where account_id is not null and account_id not in (select id from accounts) union all
select 'intention_profiles_drift',        count(*) from intention_profiles              where account_id is not null and account_id not in (select id from accounts) union all
select 'current_loc_hist_drift',          count(*) from current_location_history        where account_id is not null and account_id not in (select id from accounts) union all
select 'location_events_drift',           count(*) from location_events                 where account_id is not null and account_id not in (select id from accounts) union all
select 'favorite_places_drift',           count(*) from favorite_places                 where account_id is not null and account_id not in (select id from accounts) union all
select 'visited_places_drift',            count(*) from visited_places                  where account_id is not null and account_id not in (select id from accounts) union all
select 'saved_searches_drift',            count(*) from saved_searches                  where account_id is not null and account_id not in (select id from accounts) union all
select 'comparison_sets_drift',           count(*) from comparison_sets                 where account_id is not null and account_id not in (select id from accounts) union all
select 'comparison_set_places_drift',     count(*) from comparison_set_places           where account_id is not null and account_id not in (select id from accounts) union all
select 'notes_drift',                     count(*) from notes                           where account_id is not null and account_id not in (select id from accounts) union all
select 'share_links_drift',               count(*) from share_links                     where account_id is not null and account_id not in (select id from accounts) union all
select 'user_settings_drift',             count(*) from user_settings                   where account_id is not null and account_id not in (select id from accounts);

-- AUDIT 4: auth users (must be 0 — no auth users created)
select count(*) as auth_user_count from auth.users;
