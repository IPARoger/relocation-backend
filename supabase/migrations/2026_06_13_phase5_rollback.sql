-- Phase 5 ROLLBACK — reverse of 2026_06_13_phase5_rls_policies.sql
-- Execution order: outermost dependents first, backbone last.
-- CRITICAL: do NOT disable RLS — dropping policies returns to default-deny (safe).
-- Disabling RLS would OPEN the table. Drop policies; keep RLS enabled.

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. Drop the share RPC (public read path closes first)
-- ─────────────────────────────────────────────────────────────────────────────
revoke execute on function get_shared_chart(text) from anon, authenticated;
drop function if exists get_shared_chart(text);

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. Drop places policy
-- ─────────────────────────────────────────────────────────────────────────────
drop policy if exists "places_select" on places;

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. Drop share_links policies (owned-table surface)
-- ─────────────────────────────────────────────────────────────────────────────
drop policy if exists "share_links_select" on share_links;
drop policy if exists "share_links_insert" on share_links;
drop policy if exists "share_links_update" on share_links;
drop policy if exists "share_links_delete" on share_links;

-- ─────────────────────────────────────────────────────────────────────────────
-- 4. Drop user_settings policies
-- ─────────────────────────────────────────────────────────────────────────────
drop policy if exists "user_settings_select" on user_settings;
drop policy if exists "user_settings_insert" on user_settings;
drop policy if exists "user_settings_update" on user_settings;
drop policy if exists "user_settings_delete" on user_settings;

-- ─────────────────────────────────────────────────────────────────────────────
-- 5. Drop comparison_set_places policies
-- ─────────────────────────────────────────────────────────────────────────────
drop policy if exists "comparison_set_places_select" on comparison_set_places;
drop policy if exists "comparison_set_places_insert" on comparison_set_places;
drop policy if exists "comparison_set_places_update" on comparison_set_places;
drop policy if exists "comparison_set_places_delete" on comparison_set_places;

-- ─────────────────────────────────────────────────────────────────────────────
-- 6. Drop remaining profile-owned tables (notes → comparison_sets → ... → profiles)
-- ─────────────────────────────────────────────────────────────────────────────
drop policy if exists "notes_select"    on notes;
drop policy if exists "notes_insert"    on notes;
drop policy if exists "notes_update"    on notes;
drop policy if exists "notes_delete"    on notes;

drop policy if exists "comparison_sets_select"  on comparison_sets;
drop policy if exists "comparison_sets_insert"  on comparison_sets;
drop policy if exists "comparison_sets_update"  on comparison_sets;
drop policy if exists "comparison_sets_delete"  on comparison_sets;

drop policy if exists "saved_searches_select"   on saved_searches;
drop policy if exists "saved_searches_insert"   on saved_searches;
drop policy if exists "saved_searches_update"   on saved_searches;
drop policy if exists "saved_searches_delete"   on saved_searches;

drop policy if exists "visited_places_select"   on visited_places;
drop policy if exists "visited_places_insert"   on visited_places;
drop policy if exists "visited_places_update"   on visited_places;
drop policy if exists "visited_places_delete"   on visited_places;

drop policy if exists "favorite_places_select"  on favorite_places;
drop policy if exists "favorite_places_insert"  on favorite_places;
drop policy if exists "favorite_places_update"  on favorite_places;
drop policy if exists "favorite_places_delete"  on favorite_places;

drop policy if exists "location_events_select"  on location_events;
drop policy if exists "location_events_insert"  on location_events;
drop policy if exists "location_events_update"  on location_events;
drop policy if exists "location_events_delete"  on location_events;

drop policy if exists "current_location_history_select" on current_location_history;
drop policy if exists "current_location_history_insert" on current_location_history;
drop policy if exists "current_location_history_update" on current_location_history;
drop policy if exists "current_location_history_delete" on current_location_history;

drop policy if exists "intention_profiles_select" on intention_profiles;
drop policy if exists "intention_profiles_insert" on intention_profiles;
drop policy if exists "intention_profiles_update" on intention_profiles;
drop policy if exists "intention_profiles_delete" on intention_profiles;

drop policy if exists "birth_records_select"  on birth_records;
drop policy if exists "birth_records_insert"  on birth_records;
drop policy if exists "birth_records_update"  on birth_records;
drop policy if exists "birth_records_delete"  on birth_records;

drop policy if exists "profiles_select" on profiles;
drop policy if exists "profiles_insert" on profiles;
drop policy if exists "profiles_update" on profiles;
drop policy if exists "profiles_delete" on profiles;

-- ─────────────────────────────────────────────────────────────────────────────
-- 7. Drop backbone last (memberships before accounts)
-- ─────────────────────────────────────────────────────────────────────────────
drop policy if exists "memberships_select" on account_memberships;
drop policy if exists "memberships_insert" on account_memberships;
drop policy if exists "memberships_update" on account_memberships;
drop policy if exists "memberships_delete" on account_memberships;

drop policy if exists "accounts_select" on accounts;
drop policy if exists "accounts_insert" on accounts;
drop policy if exists "accounts_update" on accounts;
drop policy if exists "accounts_delete" on accounts;

-- ─────────────────────────────────────────────────────────────────────────────
-- 8. RLS remains ENABLED on all tables (do NOT disable — would open them)
-- End state = Phase 4 close: RLS on, zero policies, publishable key → 0 rows.
-- ─────────────────────────────────────────────────────────────────────────────
