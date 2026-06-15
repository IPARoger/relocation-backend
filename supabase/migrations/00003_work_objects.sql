-- Schema sandbox only. Not applied. No app integration.
-- Work objects: saved investigations (saved searches), saved charts, favorites, comparisons.
-- saved_charts and saved_investigations are distinct product objects.

CREATE TABLE saved_investigations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id uuid NOT NULL REFERENCES clients (id),
    birth_profile_id uuid NOT NULL REFERENCES birth_profiles (id),
    title text NOT NULL,
    conditions jsonb NOT NULL,
    viewport jsonb NOT NULL,
    settings_snapshot jsonb NOT NULL,
    settings_snapshot_version smallint NOT NULL DEFAULT 1,
    layer_display_state jsonb NOT NULL DEFAULT '{}'::jsonb,
    default_reopen_mode text NOT NULL DEFAULT 'keep_snapshot',
    source_investigation_id uuid REFERENCES saved_investigations (id),
    schema_version smallint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE saved_investigations IS
    'Saved search / saved investigation. Product synonym: saved_searches. '
    'Stores semantic inquiry intent and Layer 2 settings_snapshot at save time. '
    'Must NOT store renderer artifacts (GeoJSON, canvas, renderer_substrate, aura, virga, cache, debug).';

COMMENT ON COLUMN saved_investigations.conditions IS
    'Semantic overlay conditions only (planet_in_house, angle_in_sign, aspect_to_angle, NOT/exclusion). '
    'JSON shape versioned via schema_version and inner schema_version key. '
    'Forbidden keys include: geojson, renderer_substrate, canvas, aura_*, virga_*, cache_*, debug_*.';

COMMENT ON COLUMN saved_investigations.settings_snapshot IS
    'Layer 2 settings frozen at save time (house system, zodiac mode, orb defaults, helper layers, ontology pack). '
    'On reopen: default_reopen_mode keep_snapshot uses this; use_current reads live user_settings instead.';

COMMENT ON COLUMN saved_investigations.viewport IS
    'Display context only: center, zoom, bounds. Not a substitute for conditions.';

COMMENT ON COLUMN saved_investigations.layer_display_state IS
    'Display-only UI state: mute, solo, z-order. Does not alter Layer 1 membership.';

COMMENT ON COLUMN saved_investigations.default_reopen_mode IS
    'keep_snapshot | use_current. Enforced in 00005_indexes_constraints.sql.';

COMMENT ON COLUMN saved_investigations.updated_at IS
    'Sandbox phase: application-maintained timestamp. No database trigger is installed yet.';

CREATE TABLE saved_charts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id uuid NOT NULL REFERENCES clients (id),
    birth_profile_id uuid NOT NULL REFERENCES birth_profiles (id),
    place_id uuid NOT NULL REFERENCES places (id),
    title text,
    point_truth_cache jsonb,
    computed_at timestamptz,
    schema_version smallint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE saved_charts IS
    'Relocated chart record = birth profile + destination place. '
    'Distinct from saved_investigations (semantic map search). '
    'point_truth_cache is optional API memo only; popup/API remain authoritative. '
    'Must not store map tiles, GeoJSON, or renderer output.';

COMMENT ON COLUMN saved_charts.updated_at IS
    'Sandbox phase: application-maintained timestamp. No database trigger is installed yet.';

CREATE TABLE favorite_cities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id uuid NOT NULL REFERENCES clients (id),
    place_id uuid NOT NULL REFERENCES places (id),
    saved_investigation_id uuid REFERENCES saved_investigations (id),
    sort_order integer,
    schema_version smallint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE favorite_cities IS
    'Client-scoped place bookmark. References stable places.id, not raw search strings. '
    'Product limit: max 50 favorites per client (documented; DB enforcement deferred to a future migration).';

CREATE TABLE comparison_sets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id uuid NOT NULL REFERENCES clients (id),
    title text NOT NULL,
    saved_investigation_id uuid REFERENCES saved_investigations (id),
    birth_profile_id uuid NOT NULL REFERENCES birth_profiles (id),
    schema_version smallint NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE comparison_sets IS
    'Ordered place shortlist for comparing candidates under one birth profile. '
    'Optional link to parent saved_investigation for context.';

COMMENT ON COLUMN comparison_sets.updated_at IS
    'Sandbox phase: application-maintained timestamp. No database trigger is installed yet.';

CREATE TABLE comparison_set_places (
    comparison_set_id uuid NOT NULL REFERENCES comparison_sets (id) ON DELETE CASCADE,
    place_id uuid NOT NULL REFERENCES places (id),
    sort_order smallint NOT NULL,
    annotation text,
    PRIMARY KEY (comparison_set_id, place_id)
);

COMMENT ON TABLE comparison_set_places IS
    'Join table: ordered places within a comparison set.';
