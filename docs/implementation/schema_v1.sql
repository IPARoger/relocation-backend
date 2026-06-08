-- Relocation App schema_v1.sql
-- Draft only. Do not run in Supabase until reviewed.

create extension if not exists "pgcrypto";

create table if not exists profiles (
  id uuid primary key default gen_random_uuid(),
  account_user_id uuid not null,
  display_name text not null,
  profile_type text not null default 'human',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  archived_at timestamptz
);

create table if not exists places (
  id uuid primary key default gen_random_uuid(),
  provider text,
  provider_place_id text,
  geonames_id text,
  display_name text not null,
  canonical_name text,
  admin1 text,
  admin2 text,
  country_code text,
  country_name text,
  latitude numeric(10,7) not null,
  longitude numeric(10,7) not null,
  timezone_id text,
  population integer,
  importance_rank numeric,
  language_code text default 'en',
  alternate_names_json jsonb not null default '{}'::jsonb,
  source_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists birth_records (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  birth_date date,
  birth_time_mode text not null default 'exact',
  birth_time_start time,
  birth_time_end time,
  birth_place_id uuid references places(id),
  timezone_id text,
  utc_datetime_start timestamptz,
  utc_datetime_end timestamptz,
  confidence_notes text,
  chart_settings_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists current_location_history (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  place_id uuid references places(id),
  selected_at timestamptz not null default now(),
  is_current boolean not null default false,
  source text not null default 'manual',
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists location_events (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  place_id uuid references places(id),
  event_type text not null,
  event_source text not null default 'manual',
  occurred_at timestamptz not null default now(),
  latitude numeric(10,7),
  longitude numeric(10,7),
  notes text,
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists favorite_places (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  place_id uuid not null references places(id) on delete cascade,
  intention_profile_id uuid,
  label text,
  rank integer,
  starred boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  archived_at timestamptz,
  unique(profile_id, place_id)
);

create table if not exists visited_places (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  place_id uuid not null references places(id) on delete cascade,
  visited_at timestamptz,
  source text not null default 'manual',
  notes text,
  created_at timestamptz not null default now(),
  unique(profile_id, place_id)
);

create table if not exists saved_searches (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  intention_profile_id uuid,
  title text not null,
  search_type text not null default 'map',
  conditions_json jsonb not null default '{}'::jsonb,
  viewport_json jsonb not null default '{}'::jsonb,
  settings_snapshot_json jsonb not null default '{}'::jsonb,
  date_start date,
  date_end date,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  archived_at timestamptz
);

create table if not exists comparison_sets (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  intention_profile_id uuid,
  title text not null,
  settings_snapshot_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  archived_at timestamptz
);

create table if not exists comparison_set_places (
  id uuid primary key default gen_random_uuid(),
  comparison_set_id uuid not null references comparison_sets(id) on delete cascade,
  place_id uuid not null references places(id) on delete cascade,
  sort_order integer not null default 0,
  role text,
  created_at timestamptz not null default now(),
  unique(comparison_set_id, place_id)
);

create table if not exists notes (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  intention_profile_id uuid,
  target_type text not null,
  target_id uuid,
  section_key text,
  title text,
  body text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  archived_at timestamptz
);

create table if not exists user_settings (
  id uuid primary key default gen_random_uuid(),
  account_user_id uuid not null,
  profile_id uuid references profiles(id) on delete cascade,
  settings_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists share_links (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references profiles(id) on delete cascade,
  target_type text not null,
  target_id uuid not null,
  slug text not null unique,
  visibility text not null default 'public',
  hide_birth_data boolean not null default true,
  include_notes boolean not null default false,
  include_tables boolean not null default true,
  include_chart_wheel boolean not null default true,
  expires_at timestamptz,
  created_at timestamptz not null default now(),
  revoked_at timestamptz
);

-- Future-room table. Not wired in MVP.
create table if not exists profile_relationships (
  id uuid primary key default gen_random_uuid(),
  account_user_id uuid not null,
  profile_a_id uuid not null references profiles(id) on delete cascade,
  profile_b_id uuid not null references profiles(id) on delete cascade,
  relationship_type text,
  label text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  archived_at timestamptz
);

create index if not exists idx_profiles_account_user_id on profiles(account_user_id);
create index if not exists idx_birth_records_profile_id on birth_records(profile_id);
create index if not exists idx_places_country_name on places(country_name);
create index if not exists idx_places_display_name on places(display_name);
create index if not exists idx_places_timezone_id on places(timezone_id);
create index if not exists idx_current_location_profile_id on current_location_history(profile_id);
create index if not exists idx_location_events_profile_id on location_events(profile_id);
create index if not exists idx_favorite_places_profile_id on favorite_places(profile_id);
create index if not exists idx_visited_places_profile_id on visited_places(profile_id);
create index if not exists idx_saved_searches_profile_id on saved_searches(profile_id);
create index if not exists idx_comparison_sets_profile_id on comparison_sets(profile_id);
create index if not exists idx_notes_profile_id on notes(profile_id);
create index if not exists idx_notes_target on notes(target_type, target_id);
create index if not exists idx_share_links_slug on share_links(slug);
