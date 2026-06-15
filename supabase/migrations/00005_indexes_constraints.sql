-- Schema sandbox only. Not applied. No app integration.
-- Secondary indexes, unique constraints, and CHECK constraints.

-- ---------------------------------------------------------------------------
-- places
-- ---------------------------------------------------------------------------

ALTER TABLE places
    ADD CONSTRAINT places_external_source_check
    CHECK (external_source IN ('geoname', 'wof', 'manual', 'map_pick'));

CREATE UNIQUE INDEX places_external_source_id_unique_idx
    ON places (external_source, external_id)
    WHERE external_id IS NOT NULL;

CREATE INDEX places_display_name_idx ON places (display_name);
CREATE INDEX places_country_code_idx ON places (country_code);

-- ---------------------------------------------------------------------------
-- birth_profiles
-- ---------------------------------------------------------------------------

ALTER TABLE birth_profiles
    ADD CONSTRAINT birth_profiles_confidence_tier_check
    CHECK (confidence_tier IN ('T0', 'T1', 'T2', 'T3', 'T4'));

CREATE INDEX birth_profiles_birth_place_id_idx ON birth_profiles (birth_place_id);

-- ---------------------------------------------------------------------------
-- clients
-- ---------------------------------------------------------------------------

CREATE INDEX clients_account_id_idx ON clients (account_id);
CREATE INDEX clients_birth_profile_id_idx ON clients (birth_profile_id);

-- ---------------------------------------------------------------------------
-- saved_investigations
-- ---------------------------------------------------------------------------

ALTER TABLE saved_investigations
    ADD CONSTRAINT saved_investigations_default_reopen_mode_check
    CHECK (default_reopen_mode IN ('keep_snapshot', 'use_current'));

ALTER TABLE saved_investigations
    ADD CONSTRAINT saved_investigations_conditions_is_object_check
    CHECK (jsonb_typeof(conditions) = 'object');

ALTER TABLE saved_investigations
    ADD CONSTRAINT saved_investigations_settings_snapshot_is_object_check
    CHECK (jsonb_typeof(settings_snapshot) = 'object');

ALTER TABLE saved_investigations
    ADD CONSTRAINT saved_investigations_viewport_is_object_check
    CHECK (jsonb_typeof(viewport) = 'object');

CREATE INDEX saved_investigations_client_id_idx ON saved_investigations (client_id);
CREATE INDEX saved_investigations_birth_profile_id_idx ON saved_investigations (birth_profile_id);
CREATE INDEX saved_investigations_source_investigation_id_idx ON saved_investigations (source_investigation_id);
CREATE INDEX saved_investigations_created_at_idx ON saved_investigations (created_at DESC);

-- ---------------------------------------------------------------------------
-- saved_charts (distinct from saved_investigations)
-- ---------------------------------------------------------------------------

CREATE UNIQUE INDEX saved_charts_client_place_unique_idx
    ON saved_charts (client_id, place_id);

CREATE INDEX saved_charts_client_id_idx ON saved_charts (client_id);
CREATE INDEX saved_charts_place_id_idx ON saved_charts (place_id);
CREATE INDEX saved_charts_birth_profile_id_idx ON saved_charts (birth_profile_id);

-- ---------------------------------------------------------------------------
-- favorite_cities
-- ---------------------------------------------------------------------------

CREATE UNIQUE INDEX favorite_cities_client_place_unique_idx
    ON favorite_cities (client_id, place_id);

CREATE INDEX favorite_cities_client_id_idx ON favorite_cities (client_id);
CREATE INDEX favorite_cities_place_id_idx ON favorite_cities (place_id);
CREATE INDEX favorite_cities_saved_investigation_id_idx ON favorite_cities (saved_investigation_id);

-- Product limit: max 50 favorites per client — documented on table; enforcement deferred.
-- Future migration example:
-- CREATE OR REPLACE FUNCTION check_favorite_cities_limit() ...

-- ---------------------------------------------------------------------------
-- comparison_sets
-- ---------------------------------------------------------------------------

CREATE INDEX comparison_sets_client_id_idx ON comparison_sets (client_id);
CREATE INDEX comparison_sets_saved_investigation_id_idx ON comparison_sets (saved_investigation_id);
CREATE INDEX comparison_sets_birth_profile_id_idx ON comparison_sets (birth_profile_id);

-- ---------------------------------------------------------------------------
-- comparison_set_places
-- ---------------------------------------------------------------------------

CREATE INDEX comparison_set_places_place_id_idx ON comparison_set_places (place_id);
CREATE INDEX comparison_set_places_sort_order_idx ON comparison_set_places (comparison_set_id, sort_order);

-- ---------------------------------------------------------------------------
-- tags
-- ---------------------------------------------------------------------------

CREATE UNIQUE INDEX tags_account_name_lower_unique_idx
    ON tags (account_id, lower(name));

CREATE INDEX tags_account_id_idx ON tags (account_id);

-- ---------------------------------------------------------------------------
-- entity_tags (polymorphic)
-- ---------------------------------------------------------------------------

ALTER TABLE entity_tags
    ADD CONSTRAINT entity_tags_entity_type_check
    CHECK (entity_type IN ('client', 'saved_investigation', 'saved_chart', 'comparison_set'));

CREATE INDEX entity_tags_entity_lookup_idx ON entity_tags (entity_type, entity_id);

-- ---------------------------------------------------------------------------
-- notes (polymorphic)
-- ---------------------------------------------------------------------------

ALTER TABLE notes
    ADD CONSTRAINT notes_entity_type_check
    CHECK (entity_type IN ('client', 'saved_investigation', 'saved_chart', 'comparison_set', 'birth_profile'));

CREATE INDEX notes_account_id_idx ON notes (account_id);
CREATE INDEX notes_entity_lookup_idx ON notes (entity_type, entity_id);

-- ---------------------------------------------------------------------------
-- professional_accounts
-- ---------------------------------------------------------------------------

CREATE INDEX professional_accounts_active_idx ON professional_accounts (id)
    WHERE deleted_at IS NULL;
