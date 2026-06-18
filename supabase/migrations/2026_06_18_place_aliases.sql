-- A3: GeoNames alternate names — alias storage + ranked search RPC.

create table if not exists place_aliases (
  id uuid primary key default gen_random_uuid(),
  place_id uuid not null references places(id) on delete cascade,
  geonames_id text not null,
  alias text not null,
  normalized_alias text not null,
  language_code text,
  source text not null,
  is_preferred boolean not null default false,
  created_at timestamptz not null default now(),
  constraint place_aliases_source_check check (
    source in ('geonames_main', 'geonames_v2', 'override')
  )
);

create unique index if not exists place_aliases_place_norm_source_uidx
  on place_aliases (place_id, normalized_alias, source);

create index if not exists place_aliases_normalized_alias_idx
  on place_aliases (normalized_alias);

create index if not exists place_aliases_normalized_alias_prefix_idx
  on place_aliases (normalized_alias text_pattern_ops);

create index if not exists place_aliases_geonames_id_idx
  on place_aliases (geonames_id);

create index if not exists place_aliases_place_id_idx
  on place_aliases (place_id);

-- Launch-critical overrides (geonames_id → alias) for gaps and ranking hints.
insert into place_aliases (place_id, geonames_id, alias, normalized_alias, language_code, source, is_preferred)
select p.id, p.geonames_id, v.alias, v.norm, v.lang, 'override', true
from places p
join (values
  ('5128581', 'NYC', 'nyc', 'en'),
  ('5128581', 'New York', 'new york', 'en'),
  ('1275339', 'Bombay', 'bombay', 'en'),
  ('1264527', 'Madras', 'madras', 'en'),
  ('1275004', 'Calcutta', 'calcutta', 'en'),
  ('1273874', 'Cochin', 'cochin', 'en'),
  ('3067696', 'Praha', 'praha', 'cs'),
  ('2886242', 'Cologne', 'cologne', 'en'),
  ('2886242', 'Koeln', 'koeln', 'de'),
  ('703448', 'Kiev', 'kiev', 'en'),
  ('1816670', 'Peking', 'peking', 'en'),
  ('3176959', 'Firenze', 'firenze', 'it'),
  ('3169070', 'Roma', 'roma', 'it'),
  ('524901', 'Moskva', 'moskva', 'ru'),
  ('2267057', 'Lisboa', 'lisboa', 'pt'),
  ('2761369', 'Wien', 'wien', 'de')
) as v(gid, alias, norm, lang) on p.geonames_id = v.gid
on conflict (place_id, normalized_alias, source) do nothing;


create extension if not exists unaccent;

create or replace function public.normalize_place_alias_text(t text)
returns text
language sql
immutable
parallel safe
as $$
  select lower(trim(regexp_replace(unaccent(coalesce(t, '')), '\s+', ' ', 'g')));
$$;

-- Ranked place search: exact canonical → exact alias → prefix canonical/display → prefix alias → ILIKE fallback.
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
    -- 1 exact canonical
    select p.id as place_id, null::text as matched_alias, 1 as match_rank
    from places p, params
    where params.n <> '' and public.normalize_place_alias_text(p.canonical_name) = params.n

    union all

    -- 2 exact display_name primary segment (before first comma)
    select p.id, null::text, 1
    from places p, params
    where params.n <> ''
      and public.normalize_place_alias_text(split_part(p.display_name, ',', 1)) = params.n

    union all

    -- 3 exact normalized alias (preferred overrides tie with exact canonical; population breaks ties)
    select pa.place_id, pa.alias, case when pa.is_preferred then 1 else 2 end
    from place_aliases pa, params
    where params.n <> '' and pa.normalized_alias = params.n

    union all

    -- 4 prefix canonical
    select p.id, null::text, 3
    from places p, params
    where params.n <> '' and public.normalize_place_alias_text(p.canonical_name) like params.n || '%'

    union all

    -- 5 prefix display primary segment
    select p.id, null::text, 3
    from places p, params
    where params.n <> '' and public.normalize_place_alias_text(split_part(p.display_name, ',', 1)) like params.n || '%'

    union all

    -- 6 prefix alias
    select pa.place_id, pa.alias, 4
    from place_aliases pa, params
    where params.n <> '' and pa.normalized_alias like params.n || '%'

    union all

    -- 7 ILIKE fallback on display_name (legacy behavior)
    select p.id, null::text, 5
    from places p, params
    where params.q <> '' and p.display_name ilike '%' || params.q || '%'

    union all

    -- 8 ILIKE fallback on canonical_name
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

grant execute on function public.search_places_ranked(text, text, integer) to anon, authenticated, service_role;

comment on table place_aliases is
  'Searchable place aliases from GeoNames alternatenames / alternateNamesV2 and app overrides.';
comment on function public.search_places_ranked is
  'Ranked city search for birth records: canonical, alias, prefix, then ILIKE fallback.';
