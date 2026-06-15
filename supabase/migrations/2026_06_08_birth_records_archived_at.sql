-- Phase 2.0B — add soft-archive column to birth_records.
-- Decision: keep the normalized birth_records schema; do NOT add
-- latitude, longitude, source_label, or birth_datetime_utc.
-- This migration adds only archived_at to support soft archive.

alter table birth_records
  add column if not exists archived_at timestamptz;
