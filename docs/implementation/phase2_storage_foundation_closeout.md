# Phase 2 Storage Foundation Closeout

## Status

Phase 2 storage foundation is complete and verified through:

- repository smoke tests
- API smoke tests
- Python compile checks
- Supabase health checks
- profile library aggregate endpoint smoke test
- git checkpoint and tag discipline

Latest verified storage milestone:

- `phase2_storage_foundation_verified_20260608_231059`

Latest profile-library endpoint milestone:

- `phase2_profile_library_endpoint_20260608_231718`

## Implemented storage/API surfaces

Implemented:

- profiles
- birth records
- places
- saved searches / saved investigations
- comparison sets
- comparison set places
- favorite places
- visited places
- notes
- user settings
- share links
- profile library aggregate endpoint

## Deliberate omission: saved charts

Saved charts are not implemented in Phase 2 storage foundation.

Reason:

- `saved_charts` routes are absent from `main_centerline_FIXER.py`.
- The live Supabase schema does not currently expose a `saved_charts` table.
- Earlier direct Supabase access returned `PGRST205` for `public.saved_charts`.

Therefore saved charts must not be patched as a simple endpoint task.

Saved charts require a focused schema/migration decision before repository/API implementation.

## Product interpretation

This is acceptable for the current checkpoint because:

- saved searches / investigations preserve map inquiry
- favorite places preserve candidate locations
- comparison sets preserve city/location comparison groupings
- notes preserve human/professional commentary
- share links preserve outbound curated views

Saved charts remain an important future object for:

- saving a clicked-city relocated chart
- comparing relocated chart records directly
- attaching chart-specific notes
- exporting client chart views

## Next safe stage

Do not add more backend entities blindly.

Next stage should be:

- profile/library UX architecture
- map/profile/comparison navigation doctrine
- onboarding-first-chart flow
- later saved-charts schema design if needed

