# W2-NOTES-1: Notes Library v1

**Date:** 2026-06-16  
**Doctrine:** `results/115_w2_notes_library_doctrine_v1.md`  
**Scope:** `app_shell.html`, `scripts/smoke_notes_library.py`

## Summary

Added a profile-scoped **Notes Library** route (`#/notes-library`) with a restrained three-column layout for searching and editing contextual notes. No scratchpad, no AI, no Settings changes.

## Route

- **Path:** `#/notes-library?chartRecordId={profileId}`
- **Entry:** Chart Record → "Notes Library" button
- **Scope:** Selected profile is master; notes loaded via `GET /notes/{profile_id}`

## Layout

| Column | Content |
|--------|---------|
| Left | Seven note categories (collections) |
| Middle | Search input + filterable note list |
| Right | Editor for selected note (body + Save) |

### Collections

| Category | Status |
|----------|--------|
| Profile | Wired (`chart_record`) |
| Comparisons | Wired (`comparison_set`) |
| Saved Searches / Investigations | Wired (`saved_investigation`) |
| Saved Locations | Not wired yet |
| Relocated Charts | Not wired yet |
| City Intelligence | Not wired yet |
| Map Notes | Not wired yet |

### List item fields

- Title (derived from note title or related object)
- Note type (Profile / Comparison / Saved Search)
- Related object name
- First-line preview
- Updated time

### Search

Filters title, body, related object name, and note type (client-side).

### Save paths (existing endpoints)

- Profile → `POST /notes/chart-record`
- Comparison → `POST /notes/comparison-set`
- Investigation → `POST /notes/saved-investigation`

In-memory view model synced after save for profile and comparison notes.

## Preserved contextual notes

- Chart Record notepad (`#rm-chart-note`) unchanged
- Comparison notepad (`#rm-cmp-note`) unchanged
- Map saved-investigation note flow unchanged

## Validation (2026-06-16, port 8004)

```
PASS: smoke_notes_library.py (8 checks)
PASS: smoke_comparison_sets.py
PASS: smoke_saved_investigations.py
PASS: smoke_settings_navigation.py
```

## Out of scope

- Archive/delete from library
- Unwired categories (saved location, relocated chart, city intel, map)
- Cross-profile search
- AI summarization
- Settings / My Data placement
