-- CI-0: City Intelligence Foundation
-- One canonical row per city (places.id). Cache for hydrated intelligence payloads.

create table if not exists city_intelligence (
  city_id uuid primary key references places(id) on delete cascade,
  status text not null default 'pending',
  overview text,
  population text,
  climate text,
  cost text,
  safety text,
  language text,
  healthcare text,
  transport text,
  visa text,
  culture text,
  expat text,
  photos_json jsonb not null default '{}'::jsonb,
  airport_json jsonb not null default '{}'::jsonb,
  ai_version text,
  generated_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_city_intelligence_status on city_intelligence(status);
create index if not exists idx_city_intelligence_generated_at on city_intelligence(generated_at desc nulls last);

comment on table city_intelligence is 'Canonical City Intelligence cache; city_id FK to places (one row per city).';
comment on column city_intelligence.status is 'pending | hydrating | ready | error | custom';
