-- ================================================================
-- OPTION A CLEANUP — production only, run BEFORE Phase 1–4 apply
-- Removes all smoke-test owned rows; preserves global places data
-- ================================================================
-- Target:   PRODUCTION — run once, manually, before Phase 1 apply
-- Safe:     profile deletes cascade to all children via FK
-- Verify:   run validation queries below before and after
-- Rollback: none (destructive); take a manual DB backup first
-- ================================================================

-- ----------------------------------------------------------------
-- Pre-flight check (run first; confirm counts before proceeding)
-- ----------------------------------------------------------------
-- select 'profiles'          as tbl, count(*) from profiles;
-- select 'birth_records'     as tbl, count(*) from birth_records;
-- select 'favorite_places'   as tbl, count(*) from favorite_places;
-- select 'saved_searches'    as tbl, count(*) from saved_searches;
-- select 'comparison_sets'   as tbl, count(*) from comparison_sets;
-- select 'notes'             as tbl, count(*) from notes;
-- select 'share_links'       as tbl, count(*) from share_links;
-- select 'visited_places'    as tbl, count(*) from visited_places;
-- select 'user_settings'     as tbl, count(*) from user_settings;
-- select 'places'            as tbl, count(*) from places;
-- Expected from baseline: profiles=3, birth_records=3,
--   favorite_places=18, saved_searches=2, comparison_sets=2,
--   notes=2, share_links=2, visited_places=1, user_settings=2,
--   places=21.

-- ----------------------------------------------------------------
-- Step 1: delete all profiles
--   ON DELETE CASCADE propagates to:
--     birth_records, intention_profiles, current_location_history,
--     location_events, favorite_places, visited_places,
--     saved_searches, comparison_sets (-> comparison_set_places),
--     notes, share_links
-- ----------------------------------------------------------------
delete from profiles;

-- ----------------------------------------------------------------
-- Step 2: delete all user_settings
--   (not profile-owned; must be deleted separately)
-- ----------------------------------------------------------------
delete from user_settings;

-- ----------------------------------------------------------------
-- Step 3: verify places untouched
-- ----------------------------------------------------------------
-- select count(*) from places;   -- must still be 21

-- ----------------------------------------------------------------
-- Post-flight validation (run after; all must be 0 except places)
-- ----------------------------------------------------------------
-- select 'profiles'               as tbl, count(*) from profiles;
-- select 'birth_records'          as tbl, count(*) from birth_records;
-- select 'intention_profiles'     as tbl, count(*) from intention_profiles;
-- select 'current_location_history' as tbl, count(*) from current_location_history;
-- select 'location_events'        as tbl, count(*) from location_events;
-- select 'favorite_places'        as tbl, count(*) from favorite_places;
-- select 'visited_places'         as tbl, count(*) from visited_places;
-- select 'saved_searches'         as tbl, count(*) from saved_searches;
-- select 'comparison_sets'        as tbl, count(*) from comparison_sets;
-- select 'comparison_set_places'  as tbl, count(*) from comparison_set_places;
-- select 'notes'                  as tbl, count(*) from notes;
-- select 'share_links'            as tbl, count(*) from share_links;
-- select 'user_settings'          as tbl, count(*) from user_settings;
-- select 'places'                 as tbl, count(*) from places;   -- still 21
