-- QUICK-SHARE-MVP: ephemeral frozen map-first share links (separate from share_links / Export).

create table if not exists quick_shares (
  id uuid primary key default gen_random_uuid(),
  account_id uuid not null,
  profile_id uuid not null references profiles (id) on delete cascade,
  profile_display_name text not null default '',
  source_surface text not null default 'map',
  conditions_json jsonb not null default '{}'::jsonb,
  viewport_json jsonb not null default '{}'::jsonb,
  settings_snapshot_json jsonb not null default '{}'::jsonb,
  place_id uuid,
  place_label text,
  chart_facts_json jsonb,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null,
  revoked_at timestamptz
);

comment on table quick_shares is
  'Frozen Quick Share snapshots. Public read by unguessable id. Not Export artifacts.';

create index if not exists idx_quick_shares_account_id on quick_shares (account_id);
create index if not exists idx_quick_shares_expires_at on quick_shares (expires_at);
