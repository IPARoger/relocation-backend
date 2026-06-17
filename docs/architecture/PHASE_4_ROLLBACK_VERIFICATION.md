# Phase 4 Rollback Verification

**Date:** 2026-06-13  
**Status:** Rollback artifact created. Not executed.  
**Rollback file:** `supabase/migrations/2026_06_13_phase4_rollback.sql`  
**Source migration:** `supabase/migrations/2026_06_13_phase4_integrity_lock.sql`  
**Object inventory verified live against staging (`rnwlrdtqhfjhpllryxiz`).**

---

## Context

The Production Cutover Plan identified the Phase 4 rollback as a blocking prerequisite — the only phase in the P1–P6 migration sequence without a rollback artifact. This document records the dependency analysis, rollback ordering rationale, complete object inventory, and the post-rollback validation checklist required to confirm a successful reversal.

---

## 1. Dependency Analysis

Phase 4 creates objects in seven ordered steps. Each creates dependencies that constrain the rollback ordering. The dependency graph is:

```
app_set_account_from_parent()   ←── 12 triggers depend on it
        │                              (triggers must be dropped first)
        ▼
  [function drop safe]

profiles_id_account_id_uniq     ←── 10 composite FKs reference it as FK target
comparison_sets_id_account_id_uniq ←── 1 composite FK references it
        │                              (FKs must be dropped before UNIQUE constraints)
        ▼
  [UNIQUE constraint drop safe]

account_id NOT NULL on 13 cols  ←── composite FKs assumed NOT NULL columns
        │                              (NOT NULL removal should follow FK removal
        │                               for semantic correctness, not strict
        │                               dependency — Postgres allows NOT NULL
        │                               removal independent of FKs)
        ▼
  [account_id nullable again → user_settings_account_id_fkey SET NULL valid]
```

**Critical dependency chain:**
1. Triggers → Function: triggers must be dropped before the function they reference.
2. Composite FKs → UNIQUE targets: `profiles_id_account_id_uniq` and `comparison_sets_id_account_id_uniq` are FK targets for 11 composite FKs. Dropping the UNIQUE constraints while referencing FKs exist would fail with `ERROR: cannot drop constraint ... because other objects depend on it`. FKs must be dropped first.
3. NOT NULL → Restored FKs: `user_settings_account_id_fkey` (restored in R8) uses `ON DELETE SET NULL`. For SET NULL to be semantically valid, `user_settings.account_id` must be nullable. The column becomes nullable in R6 (NOT NULL drop). R8 must follow R6.

**Non-dependencies (order is flexible between these):**
- Partial unique indexes on `user_settings` (R4) can be dropped at any point after R3 with no dependency on NOT NULL or UNIQUE constraints.
- `share_links` visibility check and default (R5) have no dependency on any other rollback step.

---

## 2. Rollback Order

Eight steps, each idempotent (`IF EXISTS` guards throughout):

| Step | Action | Rationale |
|---|---|---|
| R1 | Drop 12 triggers (`trg_*_set_account`) | Triggers depend on the function; function cannot be dropped while they exist |
| R2 | Drop `app_set_account_from_parent()` | Safe only after all 12 dependent triggers are gone |
| R3 | Drop 13 composite FKs (`*_profile_account_fkey`, `*_cset_account_fkey`, `*_cascade_fkey`) | Composite FKs reference the UNIQUE constraints dropped in R7; must precede R7 |
| R4 | Drop 2 partial unique indexes (`user_settings_account_default_uniq`, `user_settings_profile_uniq`) | No FK dependency; scheduled here for logical grouping |
| R5 | Drop `share_links_visibility_check`; drop `visibility` column default | No dependency on other steps |
| R6 | Remove NOT NULL from 13 `account_id` columns | After FK removal for semantic correctness; `user_settings.account_id` must be nullable before R8 restores the SET NULL FK |
| R7 | Drop `profiles_id_account_id_uniq`; drop `comparison_sets_id_account_id_uniq` | MUST follow R3; would fail if composite FKs still referenced these |
| R8 | Restore 13 original single-column FKs | Follows R6 (account_id nullable again); re-establishes pre-Phase-4 referential integrity |

---

## 3. Objects Removed by the Rollback

### 3a. Triggers removed (12)

| Trigger name | Table |
|---|---|
| `trg_birth_records_set_account` | `birth_records` |
| `trg_intention_profiles_set_account` | `intention_profiles` |
| `trg_current_location_history_set_account` | `current_location_history` |
| `trg_location_events_set_account` | `location_events` |
| `trg_favorite_places_set_account` | `favorite_places` |
| `trg_visited_places_set_account` | `visited_places` |
| `trg_saved_searches_set_account` | `saved_searches` |
| `trg_comparison_sets_set_account` | `comparison_sets` |
| `trg_notes_set_account` | `notes` |
| `trg_share_links_set_account` | `share_links` |
| `trg_comparison_set_places_set_account` | `comparison_set_places` |
| `trg_user_settings_set_account` | `user_settings` |

### 3b. Trigger function removed (1)

| Function | Notes |
|---|---|
| `public.app_set_account_from_parent()` | SECURITY DEFINER; fills `account_id` from parent on INSERT/UPDATE |

### 3c. Composite FKs removed (13)

| Constraint | Table | Referenced target |
|---|---|---|
| `birth_records_profile_account_fkey` | `birth_records` | `profiles(id, account_id)` |
| `intention_profiles_profile_account_fkey` | `intention_profiles` | `profiles(id, account_id)` |
| `current_location_history_profile_account_fkey` | `current_location_history` | `profiles(id, account_id)` |
| `location_events_profile_account_fkey` | `location_events` | `profiles(id, account_id)` |
| `favorite_places_profile_account_fkey` | `favorite_places` | `profiles(id, account_id)` |
| `visited_places_profile_account_fkey` | `visited_places` | `profiles(id, account_id)` |
| `saved_searches_profile_account_fkey` | `saved_searches` | `profiles(id, account_id)` |
| `comparison_sets_profile_account_fkey` | `comparison_sets` | `profiles(id, account_id)` |
| `notes_profile_account_fkey` | `notes` | `profiles(id, account_id)` |
| `share_links_profile_account_fkey` | `share_links` | `profiles(id, account_id)` |
| `comparison_set_places_cset_account_fkey` | `comparison_set_places` | `comparison_sets(id, account_id)` |
| `user_settings_profile_account_fkey` | `user_settings` | `profiles(id, account_id)` MATCH SIMPLE |
| `user_settings_account_id_cascade_fkey` | `user_settings` | `accounts(id)` ON DELETE CASCADE |

### 3d. UNIQUE constraints removed (2)

| Constraint | Table | Columns |
|---|---|---|
| `profiles_id_account_id_uniq` | `profiles` | `(id, account_id)` |
| `comparison_sets_id_account_id_uniq` | `comparison_sets` | `(id, account_id)` |

### 3e. NOT NULL constraints removed (13)

All 13 `account_id` columns revert to nullable (`is_nullable = 'YES'`):

`profiles`, `birth_records`, `intention_profiles`, `current_location_history`,
`location_events`, `favorite_places`, `visited_places`, `saved_searches`,
`comparison_sets`, `comparison_set_places`, `notes`, `share_links`, `user_settings`

### 3f. Partial unique indexes removed (2)

| Index | Table | Predicate |
|---|---|---|
| `user_settings_account_default_uniq` | `user_settings` | `WHERE profile_id IS NULL` |
| `user_settings_profile_uniq` | `user_settings` | `WHERE profile_id IS NOT NULL` |

### 3g. share_links column changes reversed

| Column | Before rollback | After rollback |
|---|---|---|
| `visibility` default | `'private'` | None |
| `share_links_visibility_check` | EXISTS — `visibility IN ('private','unlisted','public')` | DROPPED |

---

## 4. Objects Restored by the Rollback

The rollback restores 13 original single-column FKs (R8), which were dropped by Phase 4 when composite FKs were substituted. These restore pre-Phase-4 referential integrity.

| Constraint restored | Table | References | ON DELETE |
|---|---|---|---|
| `birth_records_profile_id_fkey` | `birth_records` | `profiles(id)` | CASCADE |
| `intention_profiles_profile_id_fkey` | `intention_profiles` | `profiles(id)` | CASCADE |
| `current_location_history_profile_id_fkey` | `current_location_history` | `profiles(id)` | CASCADE |
| `location_events_profile_id_fkey` | `location_events` | `profiles(id)` | CASCADE |
| `favorite_places_profile_id_fkey` | `favorite_places` | `profiles(id)` | CASCADE |
| `visited_places_profile_id_fkey` | `visited_places` | `profiles(id)` | CASCADE |
| `saved_searches_profile_id_fkey` | `saved_searches` | `profiles(id)` | CASCADE |
| `comparison_sets_profile_id_fkey` | `comparison_sets` | `profiles(id)` | CASCADE |
| `notes_profile_id_fkey` | `notes` | `profiles(id)` | CASCADE |
| `share_links_profile_id_fkey` | `share_links` | `profiles(id)` | CASCADE |
| `comparison_set_places_comparison_set_id_fkey` | `comparison_set_places` | `comparison_sets(id)` | CASCADE |
| `user_settings_profile_id_fkey` | `user_settings` | `profiles(id)` | CASCADE |
| `user_settings_account_id_fkey` | `user_settings` | `accounts(id)` | SET NULL |

**ON DELETE SET NULL note for `user_settings_account_id_fkey`:** Phase 4 explicitly documents this as "upgrades from SET NULL to CASCADE." The rollback restores SET NULL. This is semantically valid because `user_settings.account_id` is nullable after R6. If `account_id` were NOT NULL, SET NULL would produce a constraint violation at delete time — but after the rollback, the column is nullable again.

---

## 5. Validation Checklist

Run these queries immediately after applying the rollback to confirm all 8 steps succeeded. All expected results are exact counts or exact nullability values — no ambiguity.

### Check R1+R2: All triggers and function are gone

```sql
-- Expect: 0
SELECT count(*) AS remaining_triggers
FROM pg_trigger t
JOIN pg_class c ON c.oid = t.tgrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND t.tgname LIKE 'trg_%_set_account';
```

```sql
-- Expect: 0
SELECT count(*) AS remaining_function
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE p.proname = 'app_set_account_from_parent'
  AND n.nspname = 'public';
```

### Check R3: All 13 composite FKs are gone

```sql
-- Expect: 0 rows
SELECT table_name, constraint_name
FROM information_schema.table_constraints
WHERE table_schema = 'public'
  AND constraint_name IN (
    'birth_records_profile_account_fkey',
    'intention_profiles_profile_account_fkey',
    'current_location_history_profile_account_fkey',
    'location_events_profile_account_fkey',
    'favorite_places_profile_account_fkey',
    'visited_places_profile_account_fkey',
    'saved_searches_profile_account_fkey',
    'comparison_sets_profile_account_fkey',
    'notes_profile_account_fkey',
    'share_links_profile_account_fkey',
    'comparison_set_places_cset_account_fkey',
    'user_settings_profile_account_fkey',
    'user_settings_account_id_cascade_fkey'
  );
```

### Check R4: Partial unique indexes are gone

```sql
-- Expect: 0 rows
SELECT indexname
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'user_settings'
  AND indexname IN (
    'user_settings_account_default_uniq',
    'user_settings_profile_uniq'
  );
```

### Check R5: share_links visibility is clean

```sql
-- Expect: column_default IS NULL, no check constraint row
SELECT column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'share_links'
  AND column_name = 'visibility';

SELECT count(*) AS check_exists
FROM information_schema.table_constraints
WHERE table_schema = 'public'
  AND constraint_name = 'share_links_visibility_check';
-- Expect: 0
```

### Check R6: All 13 account_id columns are nullable

```sql
-- Expect: all 13 rows show is_nullable = 'YES'
SELECT table_name, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND column_name = 'account_id'
  AND table_name IN (
    'profiles','birth_records','intention_profiles','current_location_history',
    'location_events','favorite_places','visited_places','saved_searches',
    'comparison_sets','comparison_set_places','notes','share_links','user_settings'
  )
ORDER BY table_name;
```

### Check R7: UNIQUE targets are gone

```sql
-- Expect: 0 rows
SELECT constraint_name
FROM information_schema.table_constraints
WHERE table_schema = 'public'
  AND constraint_name IN (
    'profiles_id_account_id_uniq',
    'comparison_sets_id_account_id_uniq'
  );
```

### Check R8: All 13 original single-column FKs are present

```sql
-- Expect: 13 rows
SELECT table_name, constraint_name
FROM information_schema.table_constraints
WHERE table_schema = 'public'
  AND constraint_type = 'FOREIGN KEY'
  AND constraint_name IN (
    'birth_records_profile_id_fkey',
    'intention_profiles_profile_id_fkey',
    'current_location_history_profile_id_fkey',
    'location_events_profile_id_fkey',
    'favorite_places_profile_id_fkey',
    'visited_places_profile_id_fkey',
    'saved_searches_profile_id_fkey',
    'comparison_sets_profile_id_fkey',
    'notes_profile_id_fkey',
    'share_links_profile_id_fkey',
    'comparison_set_places_comparison_set_id_fkey',
    'user_settings_profile_id_fkey',
    'user_settings_account_id_fkey'
  )
ORDER BY table_name;
```

### Overall state summary (run last)

```sql
-- Post-rollback state should match post-Phase-2 state:
--   accounts / account_memberships: still exist (Phase 1 objects, not touched)
--   account_id columns: still exist on all 13 tables (Phase 2 objects, not touched)
--   account_id nullability: all nullable (Phase 2 state restored)
--   No composite FKs anywhere
--   No trg_*_set_account triggers anywhere
--   No app_set_account_from_parent function
--   Original single-column profile_id FKs present on all child tables
SELECT
  (SELECT count(*) FROM pg_trigger t
   JOIN pg_class c ON c.oid = t.tgrelid
   JOIN pg_namespace n ON n.oid = c.relnamespace
   WHERE n.nspname = 'public' AND t.tgname LIKE 'trg_%_set_account')
     AS phase4_triggers_remaining,     -- expect 0
  (SELECT count(*) FROM pg_proc p
   JOIN pg_namespace n ON n.oid = p.pronamespace
   WHERE p.proname = 'app_set_account_from_parent')
     AS phase4_function_remaining,     -- expect 0
  (SELECT count(*) FROM information_schema.table_constraints
   WHERE table_schema = 'public' AND constraint_name LIKE '%_profile_account_fkey')
     AS composite_profile_fks,         -- expect 0
  (SELECT count(*) FROM information_schema.columns
   WHERE table_schema = 'public' AND column_name = 'account_id'
     AND is_nullable = 'NO'
     AND table_name IN (
       'profiles','birth_records','intention_profiles','current_location_history',
       'location_events','favorite_places','visited_places','saved_searches',
       'comparison_sets','comparison_set_places','notes','share_links','user_settings'))
     AS account_id_not_null_count,     -- expect 0
  (SELECT count(*) FROM information_schema.table_constraints
   WHERE table_schema = 'public' AND constraint_name IN (
     'profiles_id_account_id_uniq','comparison_sets_id_account_id_uniq'))
     AS unique_targets_remaining,      -- expect 0
  (SELECT count(*) FROM information_schema.table_constraints
   WHERE table_schema = 'public' AND constraint_type = 'FOREIGN KEY'
     AND constraint_name LIKE '%_profile_id_fkey')
     AS original_profile_fks_present;  -- expect >= 11
```

---

## 6. ON DELETE Verification (R8)

The `ON DELETE` behavior for every FK restored in R8 has been verified against three independent evidence sources. The rollback SQL requires no changes.

### Evidence sources

**Source A — Phase 4 forward migration upgrade annotation:**
`2026_06_13_phase4_integrity_lock.sql` contains exactly one comment noting a behavioral change:
```
-- user_settings: account-level FK — upgrade from SET NULL to CASCADE
```
No equivalent annotation exists for any of the 11 child-table `*_profile_id_fkey` FKs. The migration was written to flag ON DELETE changes; the absence of any such flag for all child FKs confirms they were already `ON DELETE CASCADE` before Phase 4 replaced them.

**Source B — Original sandbox schema (`00002_core_entities.sql`, `00003_work_objects.sql`, `00004_settings_tags_notes.sql`):**
These files are explicitly marked "Schema sandbox only. Not applied." and reference different table names (`clients`, `birth_profiles`, `professional_accounts`) — they are not the source of the pre-Phase-4 FKs and cannot be used as a direct reference. However, `00003_work_objects.sql` independently shows `comparison_set_places → comparison_sets ON DELETE CASCADE`, consistent with the restored FK.

**Source C — Live staging database (`pg_constraint.confdeltype` audit, 2026-06-13):**
All 12 composite FKs Phase 4 created on child tables use `ON DELETE CASCADE`. `user_settings_account_id_cascade_fkey` uses `ON DELETE CASCADE` — confirming that was the upgrade target, and the pre-Phase-4 FK was `ON DELETE SET NULL` as annotated.

### Verification table

| Constraint restored in R8 | Original ON DELETE | Rollback ON DELETE | Match |
|---|---|---|---|
| `birth_records_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `intention_profiles_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `current_location_history_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `location_events_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `favorite_places_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `visited_places_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `saved_searches_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `comparison_sets_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `notes_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `share_links_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `comparison_set_places_comparison_set_id_fkey` | CASCADE (Source A + Source B) | CASCADE | **Y** |
| `user_settings_profile_id_fkey` | CASCADE (Source A: no upgrade note) | CASCADE | **Y** |
| `user_settings_account_id_fkey` | SET NULL (Source A: explicit upgrade annotation; Source C: cascade FK name confirms direction) | SET NULL | **Y** |

**All 13 match. No rollback SQL changes required.**

---

## 7. Production Cutover Plan Update

The Production Cutover Plan (section 5 — Rollback Points) listed Phase 4 rollback as "No automated rollback written yet — blocking prerequisite." That blocker is now resolved.

Updated rollback inventory:

| Phase | Rollback file | Status |
|---|---|---|
| Phase 6 | `2026_06_13_phase6_rollback.sql` | Exists, validated on staging |
| Phase 5 | `2026_06_13_phase5_rollback.sql` | Exists, validated on staging |
| Phase 4 | `2026_06_13_phase4_rollback.sql` | **Created 2026-06-13. Not yet executed.** |
| Phase 3 | N/A (read-only audit) | — |
| Phase 2 | No file — drop 13 columns + indexes | Straightforward; no artifact needed |
| Phase 1 | No file — drop tables + functions | Straightforward after Phase 2 rollback |

All phases now have a defined rollback path. The production cutover blocking condition is cleared.
