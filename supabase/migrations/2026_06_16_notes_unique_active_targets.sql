-- Enforce a single active note per logical target + section.
--
-- Backend note saves (POST /notes/chart-record, POST /notes/comparison-set)
-- update the newest active row and insert only when none exists. Without these
-- partial unique indexes a race or a failed update could leave duplicate active
-- notes, and reads (account-store / store bridge) pick "the" active row, so
-- duplicates are a correctness hazard.
--
-- Legacy rows created by the browser used a NULL section_key; coalesce(...,'main')
-- unifies those with the backend default section_key='main'.
--
-- Safety: the notes table is empty in staging at authoring time (no duplicate
-- active rows), so these indexes apply cleanly.

create unique index if not exists notes_one_active_chart_record_per_profile
  on notes (account_id, profile_id, coalesce(section_key, 'main'))
  where archived_at is null
    and target_type = 'chart_record';

create unique index if not exists notes_one_active_comparison_set
  on notes (account_id, target_id, coalesce(section_key, 'main'))
  where archived_at is null
    and target_type = 'comparison_set';

-- Rollback:
--   drop index if exists notes_one_active_chart_record_per_profile;
--   drop index if exists notes_one_active_comparison_set;
