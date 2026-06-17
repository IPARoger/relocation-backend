# Staging Setup Instructions

**Status:** Phase 0 — staging project setup (no Supabase CLI installed; using separate project method).
**Date:** 2026-06-13

---

## Step 1 — Create a new staging Supabase project (2 min, dashboard only)

1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
2. Click **New project**
3. Name it clearly — e.g. `relocation-staging` — so it is never confused with production (`dpmtmmryvlftfahipowa`)
4. Choose the **same region** as production (reduces latency surprises)
5. Choose the **free tier** unless you expect large data volumes in testing
6. Save the project URL, anon key, and service-role key — they go in `.env.staging` (see Step 2)

---

## Step 2 — Create `.env.staging`

Copy `.env` to `.env.staging` and replace the three Supabase values with staging credentials. Leave all other keys unchanged.

```
SUPABASE_URL=https://<staging-project-ref>.supabase.co
SUPABASE_ANON_KEY=sb_publishable_…
SUPABASE_SERVICE_ROLE_KEY=sb_secret_…
```

**Never commit `.env.staging` to git.**

---

## Step 3 — Apply base schema to staging

In the Supabase dashboard for the staging project, open **SQL Editor** and run these two files in order:

1. `supabase/migrations/2026_06_08_schema_v1.sql`
2. `supabase/migrations/2026_06_08_birth_records_archived_at.sql`

No data seeding needed — Option A means we start clean.

**Verify:** `select table_name from information_schema.tables where table_schema = 'public' order by table_name;`
Expected: 15 tables matching the production baseline.

---

## Step 4 — Apply Phase 1

In the SQL Editor, run:

```
supabase/migrations/2026_06_13_phase1_accounts_memberships.sql
```

**Verify (paste into SQL Editor):**

```sql
-- Tables exist
select table_name
from   information_schema.tables
where  table_schema = 'public'
and    table_name   in ('accounts', 'account_memberships');
-- Expected: 2 rows

-- Functions exist with SECURITY DEFINER
select routine_name, security_type
from   information_schema.routines
where  routine_schema = 'public'
and    routine_name   in ('app_account_ids', 'app_has_account_role');
-- Expected: 2 rows, security_type = 'DEFINER'

-- Existing tables untouched (all counts 0 — fresh project has no data)
select 'profiles'        as t, count(*) from profiles
union all
select 'places',                count(*) from places
union all
select 'birth_records',         count(*) from birth_records
union all
select 'favorite_places',       count(*) from favorite_places
union all
select 'accounts',              count(*) from accounts
union all
select 'account_memberships',   count(*) from account_memberships;
-- Expected: profiles=0, places=0, birth_records=0,
--           favorite_places=0, accounts=0, account_memberships=0
```

---

## Step 5 — Confirm staging is isolated from production

- Production URL: `https://dpmtmmryvlftfahipowa.supabase.co`
- Staging URL must be different (different project ref in the URL)
- Run the verification query above using the **staging** service-role key only
- Never run Phase 1–4 SQL against the production URL until Phase 4.5 gate is fully green

---

## Phase 0 complete when

- [ ] Staging project created
- [ ] Base schema applied (15 tables, 0 rows)
- [ ] Phase 1 applied and verified (17 tables, functions with SECURITY DEFINER)
- [ ] `.env.staging` created and separated from `.env`
- [ ] Production URL confirmed untouched

Proceed to Phase 2 (adding nullable `account_id` columns) once all boxes are checked.
