-- Phase 5: RLS policies + share RPC.
-- Staging only. No auth wiring. No frontend.
-- Follows PHASE_5_RLS_EXECUTION_SPEC.md §1–4 exactly.
-- Role arrays used throughout:
--   WRITE_ROLES  = {owner,admin,member,assistant}
--   SHARE_ROLES  = {owner,admin,member}
--   MANAGE_ROLES = {owner,admin}
--   OWNER_ONLY   = {owner}

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 0: Enable RLS on every relevant table (idempotent)
-- ─────────────────────────────────────────────────────────────────────────────

alter table accounts                  enable row level security;
alter table account_memberships       enable row level security;
alter table profiles                  enable row level security;
alter table birth_records             enable row level security;
alter table intention_profiles        enable row level security;
alter table current_location_history  enable row level security;
alter table location_events           enable row level security;
alter table favorite_places           enable row level security;
alter table visited_places            enable row level security;
alter table saved_searches            enable row level security;
alter table comparison_sets           enable row level security;
alter table comparison_set_places     enable row level security;
alter table notes                     enable row level security;
alter table user_settings             enable row level security;
alter table share_links               enable row level security;
alter table places                    enable row level security;
-- profile_relationships: leave default-deny (no account_id; deferred per spec §8.J)

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 1: accounts
-- ─────────────────────────────────────────────────────────────────────────────

create policy "accounts_select" on accounts
  for select to authenticated
  using (id in (select app_account_ids()));

create policy "accounts_insert" on accounts
  for insert to authenticated
  with check (created_by = auth.uid());

create policy "accounts_update" on accounts
  for update to authenticated
  using  (app_has_account_role(id, array['owner','admin']))
  with check (app_has_account_role(id, array['owner','admin']));

create policy "accounts_delete" on accounts
  for delete to authenticated
  using (app_has_account_role(id, array['owner']));

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 2: account_memberships
-- Members of an account see all memberships; admin+ can manage.
-- No recursion: policies call app_account_ids()/app_has_account_role(),
-- which are SECURITY DEFINER and bypass RLS on account_memberships internally.
-- ─────────────────────────────────────────────────────────────────────────────

create policy "memberships_select" on account_memberships
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "memberships_insert" on account_memberships
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin']));

create policy "memberships_update" on account_memberships
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin']))
  with check (app_has_account_role(account_id, array['owner','admin']));

create policy "memberships_delete" on account_memberships
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin']));

-- ─────────────────────────────────────────────────────────────────────────────
-- STEPS 3–13, 15: Uniform 4-policy pattern for all profile-owned tables
-- and comparison_set_places, user_settings.
-- ─────────────────────────────────────────────────────────────────────────────

-- STEP 3: profiles
create policy "profiles_select" on profiles
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "profiles_insert" on profiles
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "profiles_update" on profiles
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "profiles_delete" on profiles
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 4: birth_records
create policy "birth_records_select" on birth_records
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "birth_records_insert" on birth_records
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "birth_records_update" on birth_records
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "birth_records_delete" on birth_records
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 5: intention_profiles
create policy "intention_profiles_select" on intention_profiles
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "intention_profiles_insert" on intention_profiles
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "intention_profiles_update" on intention_profiles
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "intention_profiles_delete" on intention_profiles
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 6: current_location_history
create policy "current_location_history_select" on current_location_history
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "current_location_history_insert" on current_location_history
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "current_location_history_update" on current_location_history
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "current_location_history_delete" on current_location_history
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 7: location_events
create policy "location_events_select" on location_events
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "location_events_insert" on location_events
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "location_events_update" on location_events
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "location_events_delete" on location_events
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 8: favorite_places
create policy "favorite_places_select" on favorite_places
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "favorite_places_insert" on favorite_places
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "favorite_places_update" on favorite_places
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "favorite_places_delete" on favorite_places
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 9: visited_places
create policy "visited_places_select" on visited_places
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "visited_places_insert" on visited_places
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "visited_places_update" on visited_places
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "visited_places_delete" on visited_places
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 10: saved_searches
create policy "saved_searches_select" on saved_searches
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "saved_searches_insert" on saved_searches
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "saved_searches_update" on saved_searches
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "saved_searches_delete" on saved_searches
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 11: comparison_sets (profile-owned AND FK target for comparison_set_places)
create policy "comparison_sets_select" on comparison_sets
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "comparison_sets_insert" on comparison_sets
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "comparison_sets_update" on comparison_sets
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "comparison_sets_delete" on comparison_sets
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 12: comparison_set_places
create policy "comparison_set_places_select" on comparison_set_places
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "comparison_set_places_insert" on comparison_set_places
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "comparison_set_places_update" on comparison_set_places
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "comparison_set_places_delete" on comparison_set_places
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 13: notes
create policy "notes_select" on notes
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "notes_insert" on notes
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "notes_update" on notes
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "notes_delete" on notes
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 14: user_settings (account-level + per-profile; both keyed on account_id)
create policy "user_settings_select" on user_settings
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "user_settings_insert" on user_settings
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "user_settings_update" on user_settings
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member','assistant']))
  with check (app_has_account_role(account_id, array['owner','admin','member','assistant']));

create policy "user_settings_delete" on user_settings
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member','assistant']));

-- STEP 15: share_links management (assistant excluded from sharing per spec)
-- Public reads go through the get_shared_chart RPC only — no anon policy here.
create policy "share_links_select" on share_links
  for select to authenticated
  using (account_id in (select app_account_ids()));

create policy "share_links_insert" on share_links
  for insert to authenticated
  with check (app_has_account_role(account_id, array['owner','admin','member']));

create policy "share_links_update" on share_links
  for update to authenticated
  using  (app_has_account_role(account_id, array['owner','admin','member']))
  with check (app_has_account_role(account_id, array['owner','admin','member']));

create policy "share_links_delete" on share_links
  for delete to authenticated
  using (app_has_account_role(account_id, array['owner','admin','member']));

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 15b: get_shared_chart RPC — the ONLY anonymous read path for share data
-- ─────────────────────────────────────────────────────────────────────────────

create or replace function get_shared_chart(p_slug text)
returns json
language plpgsql
security definer
set search_path = public
as $fn_shared_chart$
declare
  v_link share_links%rowtype;
begin
  -- Find the link
  select * into v_link from share_links where slug = p_slug;
  if not found then return null; end if;

  -- Gate 1: Not private
  if v_link.visibility = 'private' then return null; end if;

  -- Gate 2: Not revoked
  if v_link.revoked_at is not null then return null; end if;

  -- Gate 3: Not expired
  if v_link.expires_at is not null and v_link.expires_at <= now() then return null; end if;

  -- Return whitelisted, flag-aware payload (no SELECT * — spec §4)
  return json_build_object(
    'share_link_id',       v_link.id,
    'profile_id',          v_link.profile_id,
    'target_type',         v_link.target_type,
    'target_id',           v_link.target_id,
    'visibility',          v_link.visibility,
    'include_tables',      v_link.include_tables,
    'include_chart_wheel', v_link.include_chart_wheel,
    'include_notes',       v_link.include_notes,
    'birth_data_visible',  (not v_link.hide_birth_data)
  );
end;
$fn_shared_chart$;

grant execute on function get_shared_chart(text) to anon, authenticated;

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 16: places — authenticated read; no writes via publishable key
-- Anon read deferred (spec §5, §8.I)
-- ─────────────────────────────────────────────────────────────────────────────

create policy "places_select" on places
  for select to authenticated
  using (true);

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 17: profile_relationships — no policy (default-deny; deferred per §8.J)
-- ─────────────────────────────────────────────────────────────────────────────
-- (intentional no-op)
