-- CITY-SEARCH-2A: materialized normalized search columns on places + indexes.
-- Rewrites search_places_ranked_fast / search_places_ranked branches 1,2,4,5
-- to compare indexed columns instead of per-row normalize_place_alias_text().

alter table public.places
  add column if not exists normalized_canonical text
    generated always as (public.normalize_place_alias_text(canonical_name)) stored,
  add column if not exists normalized_display_primary text
    generated always as (
      public.normalize_place_alias_text(split_part(display_name, ',', 1))
    ) stored;

comment on column public.places.normalized_canonical is
  'CITY-SEARCH-2A: normalized canonical_name for indexed exact/prefix search.';
comment on column public.places.normalized_display_primary is
  'CITY-SEARCH-2A: normalized display_name primary segment (before comma).';

create index if not exists places_normalized_canonical_idx
  on public.places (normalized_canonical);

create index if not exists places_normalized_canonical_prefix_idx
  on public.places (normalized_canonical text_pattern_ops);

create index if not exists places_normalized_display_primary_idx
  on public.places (normalized_display_primary);

create index if not exists places_normalized_display_primary_prefix_idx
  on public.places (normalized_display_primary text_pattern_ops);

create or replace function public.search_places_ranked_fast(p_query text, p_norm text, p_limit integer default 20)
returns table (
  id uuid,
  provider text,
  provider_place_id text,
  geonames_id text,
  display_name text,
  canonical_name text,
  admin1 text,
  admin2 text,
  country_code text,
  country_name text,
  latitude numeric,
  longitude numeric,
  timezone_id text,
  population integer,
  importance_rank numeric,
  language_code text,
  alternate_names_json jsonb,
  source_json jsonb,
  created_at timestamptz,
  updated_at timestamptz,
  matched_alias text,
  match_rank integer
)
language sql
stable
as $$
  with params as (
    select
      trim(coalesce(p_query, '')) as q,
      trim(coalesce(p_norm, '')) as n,
      greatest(1, least(coalesce(p_limit, 20), 50)) as lim
  ),
  candidates as (
    -- 1 exact canonical (indexed normalized_canonical)
    select p.id as place_id, null::text as matched_alias, 1 as match_rank
    from places p, params
    where params.n <> '' and p.normalized_canonical = params.n

    union all

    -- 2 exact display primary segment (indexed normalized_display_primary)
    select p.id, null::text, 1
    from places p, params
    where params.n <> '' and p.normalized_display_primary = params.n

    union all

    -- 3 exact normalized alias (unchanged — already indexed)
    select pa.place_id, pa.alias, case when pa.is_preferred then 1 else 2 end
    from place_aliases pa, params
    where params.n <> '' and pa.normalized_alias = params.n

    union all

    -- 4 prefix canonical (indexed text_pattern_ops)
    select p.id, null::text, 3
    from places p, params
    where params.n <> '' and p.normalized_canonical like params.n || '%'

    union all

    -- 5 prefix display primary segment (indexed text_pattern_ops)
    select p.id, null::text, 3
    from places p, params
    where params.n <> '' and p.normalized_display_primary like params.n || '%'

    union all

    -- 6 prefix alias (Phase 2B target — unchanged in 2A)
    select pa.place_id, pa.alias, 4
    from place_aliases pa, params
    where params.n <> '' and pa.normalized_alias like params.n || '%'
  ),
  best as (
    select distinct on (c.place_id)
      c.place_id,
      c.matched_alias,
      c.match_rank
    from candidates c
    order by c.place_id, c.match_rank asc, length(coalesce(c.matched_alias, '')) desc
  )
  select
    p.id, p.provider, p.provider_place_id, p.geonames_id, p.display_name, p.canonical_name,
    p.admin1, p.admin2, p.country_code, p.country_name, p.latitude, p.longitude,
    p.timezone_id, p.population, p.importance_rank, p.language_code,
    p.alternate_names_json, p.source_json, p.created_at, p.updated_at,
    b.matched_alias, b.match_rank
  from best b
  join places p on p.id = b.place_id
  order by b.match_rank asc, p.importance_rank desc nulls last, p.population desc nulls last, p.display_name asc
  limit (select lim from params);
$$;

create or replace function public.search_places_ranked(p_query text, p_norm text, p_limit integer default 20)
returns table (
  id uuid,
  provider text,
  provider_place_id text,
  geonames_id text,
  display_name text,
  canonical_name text,
  admin1 text,
  admin2 text,
  country_code text,
  country_name text,
  latitude numeric,
  longitude numeric,
  timezone_id text,
  population integer,
  importance_rank numeric,
  language_code text,
  alternate_names_json jsonb,
  source_json jsonb,
  created_at timestamptz,
  updated_at timestamptz,
  matched_alias text,
  match_rank integer
)
language sql
stable
as $$
  with params as (
    select
      trim(coalesce(p_query, '')) as q,
      trim(coalesce(p_norm, '')) as n,
      greatest(1, least(coalesce(p_limit, 20), 50)) as lim
  ),
  candidates as (
    select p.id as place_id, null::text as matched_alias, 1 as match_rank
    from places p, params
    where params.n <> '' and p.normalized_canonical = params.n

    union all

    select p.id, null::text, 1
    from places p, params
    where params.n <> '' and p.normalized_display_primary = params.n

    union all

    select pa.place_id, pa.alias, case when pa.is_preferred then 1 else 2 end
    from place_aliases pa, params
    where params.n <> '' and pa.normalized_alias = params.n

    union all

    select p.id, null::text, 3
    from places p, params
    where params.n <> '' and p.normalized_canonical like params.n || '%'

    union all

    select p.id, null::text, 3
    from places p, params
    where params.n <> '' and p.normalized_display_primary like params.n || '%'

    union all

    select pa.place_id, pa.alias, 4
    from place_aliases pa, params
    where params.n <> '' and pa.normalized_alias like params.n || '%'

    union all

    select p.id, null::text, 5
    from places p, params
    where params.q <> '' and p.display_name ilike '%' || params.q || '%'

    union all

    select p.id, null::text, 5
    from places p, params
    where params.q <> '' and p.canonical_name ilike '%' || params.q || '%'
  ),
  best as (
    select distinct on (c.place_id)
      c.place_id,
      c.matched_alias,
      c.match_rank
    from candidates c
    order by c.place_id, c.match_rank asc, length(coalesce(c.matched_alias, '')) desc
  )
  select
    p.id, p.provider, p.provider_place_id, p.geonames_id, p.display_name, p.canonical_name,
    p.admin1, p.admin2, p.country_code, p.country_name, p.latitude, p.longitude,
    p.timezone_id, p.population, p.importance_rank, p.language_code,
    p.alternate_names_json, p.source_json, p.created_at, p.updated_at,
    b.matched_alias, b.match_rank
  from best b
  join places p on p.id = b.place_id
  order by b.match_rank asc, p.importance_rank desc nulls last, p.population desc nulls last, p.display_name asc
  limit (select lim from params);
$$;

comment on function public.search_places_ranked_fast is
  'CITY-SEARCH-2A: exact + prefix tiers; places branches use normalized_* indexed columns.';
comment on function public.search_places_ranked is
  'CITY-SEARCH-2A: legacy monolithic ranked search; places branches use normalized_* columns.';
