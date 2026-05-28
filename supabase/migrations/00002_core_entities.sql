-- Schema sandbox only. Not applied. No app integration.
-- Core entities: accounts, places, birth profiles, clients.
-- Create order respects FK dependencies: places -> birth_profiles -> clients.

CREATE TABLE professional_accounts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name text NOT NULL,
    email text UNIQUE,
    schema_version smallint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

COMMENT ON TABLE professional_accounts IS
    'Professional owner record. Schema sandbox only. Future auth subject; no auth dependency in this migration set.';

COMMENT ON COLUMN professional_accounts.updated_at IS
    'Sandbox phase: application-maintained timestamp. No database trigger is installed yet.';

CREATE TABLE places (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    external_source text NOT NULL,
    external_id text,
    display_name text NOT NULL,
    admin1 text,
    country_code char(2),
    country_name text,
    lat double precision NOT NULL,
    lon double precision NOT NULL,
    resolution_audit jsonb NOT NULL DEFAULT '{}'::jsonb,
    schema_version smallint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE places IS
    'Stable place identity for favorites, comparisons, and birth locations. '
    'Supports geoname/wof external IDs plus manual and map_pick entries (external_id may be NULL). '
    'Must not store renderer output or GeoJSON.';

COMMENT ON COLUMN places.external_source IS
    'One of: geoname, wof, manual, map_pick. Enforced in 00005_indexes_constraints.sql.';

COMMENT ON COLUMN places.external_id IS
    'Provider place ID when known. NULL allowed for manual/map_pick. Unique per (external_source, external_id) when NOT NULL.';

CREATE TABLE birth_profiles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    birth_date date NOT NULL,
    birth_time time,
    birth_place_id uuid NOT NULL REFERENCES places (id),
    timezone_id text NOT NULL,
    utc_offset_at_birth_minutes integer,
    confidence_tier text NOT NULL,
    confidence_metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    representative_time time,
    layer1_snapshot_hash text,
    schema_version smallint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE birth_profiles IS
    'Natal Layer 1 input domain. Must not store rendered houses, popup strings, or GeoJSON. '
    'confidence_tier T0-T4 enforced in 00005_indexes_constraints.sql.';

COMMENT ON COLUMN birth_profiles.representative_time IS
    'Explicit representative time only when confidence tier requires it. Never an implicit guess.';

COMMENT ON COLUMN birth_profiles.updated_at IS
    'Sandbox phase: application-maintained timestamp. No database trigger is installed yet.';

CREATE TABLE clients (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL REFERENCES professional_accounts (id),
    display_name text NOT NULL,
    birth_profile_id uuid NOT NULL UNIQUE REFERENCES birth_profiles (id),
    schema_version smallint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

COMMENT ON TABLE clients IS
    'One client per professional account scope. MVP: exactly one birth_profile per client (UNIQUE on birth_profile_id).';

COMMENT ON COLUMN clients.updated_at IS
    'Sandbox phase: application-maintained timestamp. No database trigger is installed yet.';
