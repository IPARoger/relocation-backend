-- Schema sandbox only. Not applied. No app integration.
-- Account settings (Layer 2), tags, polymorphic entity_tags and notes.

CREATE TABLE user_settings (
    account_id uuid PRIMARY KEY REFERENCES professional_accounts (id),
    settings jsonb NOT NULL,
    settings_version smallint NOT NULL DEFAULT 1,
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE user_settings IS
    'Account-level Layer 2 defaults (orbs, house system display prefs, helper layers, ontology pack). '
    'One row per professional_account. Changing settings does not retroactively rewrite saved_investigations.settings_snapshot.';

COMMENT ON COLUMN user_settings.settings IS
    'Layer 2 JSON only. Must not contain renderer_substrate, cache, or debug keys as product truth.';

COMMENT ON COLUMN user_settings.updated_at IS
    'Sandbox phase: application-maintained timestamp. No database trigger is installed yet.';

CREATE TABLE tags (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL REFERENCES professional_accounts (id),
    name text NOT NULL,
    color_key text,
    created_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE tags IS
    'Account-scoped tag definitions. Unique per account on lower(name) enforced in 00005.';

CREATE TABLE entity_tags (
    tag_id uuid NOT NULL REFERENCES tags (id) ON DELETE CASCADE,
    entity_type text NOT NULL,
    entity_id uuid NOT NULL,
    PRIMARY KEY (tag_id, entity_type, entity_id)
);

COMMENT ON TABLE entity_tags IS
    'Polymorphic tag assignments. entity_type enforced in 00005: client, saved_investigation, saved_chart, comparison_set. '
    'Referential integrity to target rows is application-enforced until auth/RLS slice.';

CREATE TABLE notes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL REFERENCES professional_accounts (id),
    entity_type text NOT NULL,
    entity_id uuid NOT NULL,
    body text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE notes IS
    'Polymorphic professional notes. entity_type enforced in 00005: client, saved_investigation, saved_chart, comparison_set, birth_profile. '
    'Referential integrity to target rows is application-enforced until auth/RLS slice.';

COMMENT ON COLUMN notes.updated_at IS
    'Sandbox phase: application-maintained timestamp. No database trigger is installed yet.';
