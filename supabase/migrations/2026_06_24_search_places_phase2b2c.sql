-- CITY-SEARCH-2B+2C: prefix alias index-friendly range + tier short-circuit.
-- 2B: replace LIKE n||'%' with >= n AND < upper_bound for place_aliases + places prefix tiers.
-- 2C: search_places_ranked_fast runs exact tiers first; skips prefix tiers when limit met.

create or replace function public.normalized_prefix_range_end(p_prefix text)
returns text
language sql
immutable
parallel safe
as $$
  select coalesce(p_prefix, '') || E'\uffff';
$$;

comment on function public.normalized_prefix_range_end(text) is
  'CITY-SEARCH-2B: exclusive upper bound for btree prefix range on normalized text.';

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
language plpgsql
volatile
as $function$
declare
  v_q text;
  v_n text;
  v_lim integer;
  v_have integer;
  v_upper text;
begin
  v_q := trim(coalesce(p_query, ''));
  v_n := trim(coalesce(p_norm, ''));
  v_lim := greatest(1, least(coalesce(p_limit, 20), 50));

  if v_n = '' then
    return;
  end if;

  v_upper := public.normalized_prefix_range_end(v_n);

  drop table if exists _sp_candidates;
  create temp table _sp_candidates (
    place_id uuid not null,
    matched_alias text,
    match_rank integer not null
  ) on commit drop;

  -- Tier 1: exact places (canonical, display primary)
  insert into _sp_candidates (place_id, matched_alias, match_rank)
  select p.id, null::text, 1
  from places p
  where p.normalized_canonical = v_n;

  insert into _sp_candidates (place_id, matched_alias, match_rank)
  select p.id, null::text, 1
  from places p
  where p.normalized_display_primary = v_n;

  -- Tier 2: exact alias (indexed equality)
  insert into _sp_candidates (place_id, matched_alias, match_rank)
  select pa.place_id, pa.alias, case when pa.is_preferred then 1 else 2 end
  from place_aliases pa
  where pa.normalized_alias = v_n;

  select count(distinct place_id) into v_have from _sp_candidates;

  if v_have < v_lim then
    -- Tier 3: prefix places (indexed range)
    insert into _sp_candidates (place_id, matched_alias, match_rank)
    select p.id, null::text, 3
    from places p
    where p.normalized_canonical >= v_n
      and p.normalized_canonical < v_upper;

    insert into _sp_candidates (place_id, matched_alias, match_rank)
    select p.id, null::text, 3
    from places p
    where p.normalized_display_primary >= v_n
      and p.normalized_display_primary < v_upper;

    select count(distinct place_id) into v_have from _sp_candidates;

    if v_have < v_lim then
      -- Tier 4: prefix alias (2B — indexed range, not seq scan LIKE)
      insert into _sp_candidates (place_id, matched_alias, match_rank)
      select pa.place_id, pa.alias, 4
      from place_aliases pa
      where pa.normalized_alias >= v_n
        and pa.normalized_alias < v_upper;
    end if;
  end if;

  return query
  with best as (
    select distinct on (c.place_id)
      c.place_id,
      c.matched_alias,
      c.match_rank
    from _sp_candidates c
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
  limit v_lim;
end;
$function$;

-- Legacy ranked search: 2B prefix range on alias + places branches (monolithic UNION retained).
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
      greatest(1, least(coalesce(p_limit, 20), 50)) as lim,
      public.normalized_prefix_range_end(trim(coalesce(p_norm, ''))) as n_upper
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
    where params.n <> ''
      and p.normalized_canonical >= params.n
      and p.normalized_canonical < params.n_upper

    union all

    select p.id, null::text, 3
    from places p, params
    where params.n <> ''
      and p.normalized_display_primary >= params.n
      and p.normalized_display_primary < params.n_upper

    union all

    select pa.place_id, pa.alias, 4
    from place_aliases pa, params
    where params.n <> ''
      and pa.normalized_alias >= params.n
      and pa.normalized_alias < params.n_upper

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
  'CITY-SEARCH-2B+2C: tier short-circuit exact before prefix; alias prefix uses indexed range.';
comment on function public.search_places_ranked is
  'CITY-SEARCH-2B: prefix tiers use normalized_prefix_range_end; legacy UNION for fallback path.';
