-- Enforce a single active note per saved investigation + section.
--
-- The backend note save (POST /notes/saved-investigation) updates the newest
-- active row and inserts only when none exists. Without this partial unique
-- index a race or a failed update could leave duplicate active notes, and reads
-- pick "the" active row, so duplicates are a correctness hazard.
--
-- Mirrors the comparison_set index in 2026_06_16_notes_unique_active_targets.sql
-- (keyed on target_id, since saved_investigation notes carry the saved_searches
-- id in notes.target_id). coalesce(section_key,'main') unifies any legacy NULL
-- section_key rows with the backend default section_key='main'.
--
-- Safety: preflight at authoring time found 0 active saved_investigation notes
-- in staging (no duplicate active rows), so this index applies cleanly.

create unique index if not exists notes_one_active_saved_investigation
  on notes (account_id, target_id, coalesce(section_key, 'main'))
  where archived_at is null
    and target_type = 'saved_investigation';

-- Rollback:
--   drop index if exists notes_one_active_saved_investigation;
