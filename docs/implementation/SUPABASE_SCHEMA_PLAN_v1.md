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


## Schema Audit Addendum 001

### Birth Time Range

The schema must explicitly preserve min/max birth time.

Even if MVP defaults to exact birth time, birth_records must support:

- birth_time_mode
- birth_time_start
- birth_time_end
- utc_datetime_start
- utc_datetime_end

For exact birth time:

birth_time_start = birth_time_end

For range/approximate birth time:

birth_time_start and birth_time_end define the chart calculation boundary.

Unknown birth time may be stored, but relocation mapping must warn that useful relocation geometry requires reliable birth time.

### Intention Profiles As Sub-Profiles

Future intention profiles act like sub-profiles or sub-personalities.

Examples:
- Home
- Career
- Relationship
- Retreat
- Health
- Creative work

Favorites, saved searches, saved comparisons, notes, and future transit lab saved searches should all be able to attach either to:

- profile_id only
- profile_id + intention_profile_id

For MVP, intention_profile_id may remain null.

### Notes Scope

Notes may exist at multiple local points and aggregate upward into notebook views.

Comparison notes may include:
- PiH notes
- A2A notes
- AiS notes
- master comparison notes

Saved search notes may include:
- general saved search note
- PiH notes
- A2A notes
- AiS notes

Future Transit Lab notes should be supported by the same notes architecture.

### Future Transit Lab Saved Searches

Transit Lab is deferred, but schema should leave room for saved temporal investigations.

Future transit saved searches may require:
- profile_id
- intention_profile_id nullable
- beginning calendar date
- ending calendar date
- transit conditions
- settings snapshot
- notes

Do not build Transit Lab tables yet unless required.

### City Intelligence Cache

City Intelligence cache is deferred from MVP schema execution but must be anticipated.

Future city intelligence cache may store:
- place_id
- provider
- data_domain
- payload_json
- fetched_at
- expires_at
- source_version
- language_code

### AI Intake Cache

AI intake is deferred.

Future AI intake may be large and should not be forced into profile fields.

Future storage may require:
- profile_id
- intention_profile_id nullable
- intake_payload_json
- extracted_preferences_json
- search_guidance_json
- tradeoff_guidance_json
- substitution_guidance_json
- created_at
- updated_at

Do not build AI intake tables yet.


## Schema Audit Addendum 002

### Profile Relationships And Future Composite Charts

The schema should leave room for relationships between profiles.

Future uses:
- spouse / partner
- child
- parent
- family member
- business partner
- friend
- client group
- composite chart
- synastry chart
- shared relocation analysis

Do not build composite or synastry features for MVP.

However, avoid a schema that assumes profiles are permanently isolated.

Future table likely needed:

profile_relationships

Potential fields:
- id
- account_user_id
- profile_a_id
- profile_b_id
- relationship_type
- label
- notes
- created_at
- updated_at
- archived_at

Future composite chart records should reference existing profiles rather than duplicating human identity data.


## Schema Audit Addendum 003

### Unknown Birth Time Storage

Unknown birth time should remain storable.

Unknown birth time may support:
- basic profile creation
- symbolic/noon chart wheel
- non-relocation reference display
- guidance for finding birth records

Unknown birth time must not be treated as valid for relocation mapping, house overlays, A2A overlays, or relocated chart confidence.

MVP may use:

birth_time_mode = unknown

with birth_time_start and birth_time_end null.

### Transit Lab Saved Search Scope

Future Transit Lab saved searches are more than date ranges.

They may include:
- selected city or cities
- transit planet conditions
- planet-in-house conditions
- aspect-to-angle conditions
- orb settings
- beginning date
- ending date
- settings snapshot
- notes

For now, saved_searches may preserve this future room through:
- search_type
- conditions_json
- settings_snapshot_json
- date_start
- date_end

Do not build Transit Lab-specific tables yet.

### Notes Must Remain Structured Rows

Do not store master notes as one large editable blob.

Notes should remain separate local rows.

Notebook / Master Notes views should be generated by grouping note rows under stable system headers.

Examples:

Profile page notes:
- target_type = profile
- section_key = pih
- section_key = a2a
- section_key = ais
- section_key = general

Comparison page notes:
- target_type = comparison_set
- section_key = pih
- section_key = a2a
- section_key = ais
- section_key = general
- section_key = saved_reason

Saved search notes:
- target_type = saved_search
- section_key = pih
- section_key = a2a
- section_key = ais
- section_key = general
- section_key = saved_reason

This preserves local editing while allowing master notebook aggregation.


## Schema Audit Addendum 004

### Product Activity Events

The product should leave room to track user behavior for product improvement, caching, UX optimization, and future AI context.

Possible tracked events:
- city searched
- city selected
- city viewed
- city favorited
- city compared
- comparison opened
- saved search opened
- map zoom changed
- map viewport changed
- variable selected
- variable deselected
- overlay muted
- overlay soloed
- opacity changed
- location inspected
- share link created
- export created

Use cases:
- understand how users actually search
- improve caching priorities
- identify common region/variable sequences
- optimize UI flows
- propose future features
- improve AI context
- detect popular relocation patterns
- understand comparison behavior

Privacy doctrine:
- do not sell behavioral data to travel companies
- do not use tracking deceptively
- use activity data primarily to improve the product
- preserve user trust
- future analytics should be disclosed appropriately

Future table likely needed:

product_activity_events

Potential fields:
- id
- account_user_id
- profile_id nullable
- intention_profile_id nullable
- place_id nullable
- event_type
- event_context
- event_payload_json
- viewport_json
- conditions_json
- created_at

Do not build full analytics UI for MVP.

