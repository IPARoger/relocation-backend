-- CITY-SEARCH-PERF-1: staged ranked search — fast exact/prefix tiers first;
-- ILIKE contains fallback only when fast results underfill limit.

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
    select p.id as place_id, null::text as matched_alias, 1 as match_rank
    from places p, params
    where params.n <> '' and public.normalize_place_alias_text(p.canonical_name) = params.n

    union all

    select p.id, null::text, 1
    from places p, params
    where params.n <> ''
      and public.normalize_place_alias_text(split_part(p.display_name, ',', 1)) = params.n

    union all

    select pa.place_id, pa.alias, case when pa.is_preferred then 1 else 2 end
    from place_aliases pa, params
    where params.n <> '' and pa.normalized_alias = params.n

    union all

    select p.id, null::text, 3
    from places p, params
    where params.n <> '' and public.normalize_place_alias_text(p.canonical_name) like params.n || '%'

    union all

    select p.id, null::text, 3
    from places p, params
    where params.n <> '' and public.normalize_place_alias_text(split_part(p.display_name, ',', 1)) like params.n || '%'

    union all

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

create or replace function public.search_places_ranked_fallback(
  p_query text,
  p_norm text,
  p_limit integer default 20,
  p_exclude uuid[] default '{}'::uuid[]
)
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
      greatest(0, least(coalesce(p_limit, 20), 50)) as lim
  ),
  candidates as (
    select p.id as place_id, null::text as matched_alias, 5 as match_rank
    from places p, params
    where params.q <> ''
      and p.display_name ilike '%' || params.q || '%'
      and not (p.id = any(coalesce(p_exclude, array[]::uuid[])))

    union all

    select p.id, null::text, 5
    from places p, params
    where params.q <> ''
      and p.canonical_name ilike '%' || params.q || '%'
      and not (p.id = any(coalesce(p_exclude, array[]::uuid[])))
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

grant execute on function public.search_places_ranked_fast(text, text, integer) to anon, authenticated, service_role;
grant execute on function public.search_places_ranked_fallback(text, text, integer, uuid[]) to anon, authenticated, service_role;

comment on function public.search_places_ranked_fast is
  'Stages 1–2: exact + prefix alias/canonical matches only (no ILIKE contains).';
comment on function public.search_places_ranked_fallback is
  'Stage 3: ILIKE contains fallback; skipped when fast tier already fills limit.';
