# SUPABASE_SCHEMA_PLAN_v1

## Purpose

Define the first persistence schema before creating Supabase tables.

This is a plan only. No live database changes yet.

## Core Doctrine

One Profile = one human/client identity.

A Profile may have:
- one active natal birth record
- current location records
- favorite places
- saved searches
- saved comparisons
- local notes
- notebook aggregation
- future intention profiles
- future linked profile relationships

## Birth Time Modes

Supported schema room:

- exact
- range
- approximate
- unknown

MVP Web2 default:

exact

For exact birth time:

birth_time_start = birth_time_end

For range or approximate birth time:

birth_time_start and birth_time_end define the calculation range.

Future use:

The app may render min/max chart overlays and confidence gradients where both times agree.

Unknown birth time:

Allowed for storing profile data and possibly rendering a symbolic/noon birth wheel.

Unknown birth time must not be treated as reliable for relocation mapping.

The app should help users find birth certificates, hospital records, family records, or rectification support.

If birth-time range is too wide, relocation mapping becomes unreliable and must show a warning.

## Places / Favorites

places = canonical city/location catalog.

favorite_places = profile-saved city list referencing places.

MVP treats saved cities and favorites as the same user-facing concept.

Future room:
- categories
- rankings
- intention-specific favorites
- auto-added current locations
- professional notes

## Current Location

Profiles should support current location history.

MVP should store deliberate current-location selections/check-ins.

Do not store every GPS ping in this table.

Future travel/road-trip telemetry belongs in a separate session table.

## Intention Profiles

Not MVP, but schema should leave room.

Future intention profiles may contain their own:
- favorites
- saved searches
- saved comparisons
- notes

Therefore these tables should later support nullable intention_profile_id.

## Notes

Notes are local where written.

Notebook views aggregate notes upward.

Do not duplicate note bodies just to create master notes.

Notes may attach to:
- profile
- place
- current location
- favorite place
- saved search
- saved comparison
- comparison section
- PiH section
- AiS section
- A2A section

## Proposed MVP Tables

### profiles

Human/client identity.

Key fields:
- id
- account_user_id
- display_name
- profile_type
- created_at
- updated_at
- archived_at

### birth_records

Natal data for the profile.

Key fields:
- id
- profile_id
- birth_date
- birth_time_mode
- birth_time_start
- birth_time_end
- birth_place_id
- timezone_id
- utc_datetime_start
- utc_datetime_end
- confidence_notes
- chart_settings_json
- created_at
- updated_at

### places

Canonical place/city records.

Key fields:
- id
- provider
- provider_place_id
- geonames_id
- display_name
- canonical_name
- admin1
- admin2
- country_code
- country_name
- latitude
- longitude
- timezone_id
- population
- importance_rank
- language_code
- alternate_names_json
- source_json
- created_at
- updated_at

### current_location_events

Deliberate current-location records.

Key fields:
- id
- profile_id
- place_id
- selected_at
- is_current
- source
- notes
- created_at

### favorite_places

Saved cities/favorites for a profile.

Key fields:
- id
- profile_id
- place_id
- intention_profile_id nullable future
- label
- rank
- starred
- created_at
- updated_at
- archived_at

### saved_searches

Saved map investigations.

Key fields:
- id
- profile_id
- intention_profile_id nullable future
- title
- conditions_json
- viewport_json
- settings_snapshot_json
- created_at
- updated_at
- archived_at

### comparison_sets

Saved comparisons.

Key fields:
- id
- profile_id
- intention_profile_id nullable future
- title
- settings_snapshot_json
- created_at
- updated_at
- archived_at

### comparison_set_places

Places included in a comparison.

Key fields:
- id
- comparison_set_id
- place_id
- sort_order
- role
- created_at

### notes

Local notes with notebook aggregation.

Key fields:
- id
- profile_id
- intention_profile_id nullable future
- target_type
- target_id
- section_key
- title
- body
- created_at
- updated_at
- archived_at

### user_settings

Account-level or profile-level settings.

Key fields:
- id
- account_user_id
- profile_id nullable
- settings_json
- created_at
- updated_at

### share_links

One-click public sharing.

Key fields:
- id
- profile_id
- target_type
- target_id
- slug
- visibility
- hide_birth_data
- include_notes
- include_tables
- include_chart_wheel
- expires_at
- created_at
- revoked_at

## Explicitly Deferred

Do not build yet:
- AI interpretation tables
- ontology marketplace
- glyph marketplace
- travel telemetry
- road trip sessions
- airplane/offline sessions
- city intelligence cache tables
- export template builder
- professional billing
- composite charts

Leave room, but do not decorate empty rooms.

