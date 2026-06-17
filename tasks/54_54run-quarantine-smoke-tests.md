# Task 54 — Run Quarantine Route Smoke Tests

## Objective
Execute the quarantine-route smoke tests (written in task 50, with Playwright + Chromium installed in tasks 51–52, and scripts verified in task 53) to produce a PASS/FAIL verdict with artifact evidence for each quarantined dead read route.

---

## Scope
Run the existing smoke test scripts against the quarantined routes. Collect output. Classify each route as CONFIRMED DEAD (returning 404/410/error as expected) or UNEXPECTED LIVE (needs investigation). No code changes to application logic.

---

## Files to Read
- `relay/tasks/50_smoke_quarantine_routes.md` — the smoke test plan and scripts written in task 50
- `relay/tasks/53_53verify-smoke-scripts.md` — closeout from script verification task; confirms what scripts exist and where
- `relay/tasks/46_quarantine_dead_read_routes.md` — the original quarantine task; defines which routes were quarantined and expected behavior
- Any smoke script files referenced in task 53 (e.g. `scripts/smoke_quarantine_routes.py`, `tests/smoke/` or equivalent path confirmed in task 53 closeout)

---

## Files Expected to Change
- `relay/results/54_run-quarantine-smoke-tests.md` — new result artifact (create this)
- No application source files should change

---

## Required Behavior

1. **Read task 53 closeout first** to confirm the exact script path(s) and invocation command(s) verified as working.

2. **Run the quarantine smoke script(s)** exactly as verified in task 53. Do not modify the scripts before running.

3. **Capture full stdout/stderr output** for each script invocation.

4. **For each quarantined route tested**, record:
   - Route path and HTTP method
   - Expected behavior (e.g. 404, connection refused, redirect to auth)
   - Actual HTTP status or error received
   - PASS or FAIL verdict

5. **Produce a summary table** in the result artifact:

   | Route | Expected | Actual | Verdict |
   |---|---|---|---|
   | ... | ... | ... | PASS/FAIL |

6. **Overall verdict**: ALL PASS, PARTIAL (n of m passed), or BLOCKED (scripts could not run).

---

## Hard Stops
- Do NOT modify any application route handlers, middleware, or server files
- Do NOT modify the smoke scripts themselves (run them as-is)
- Do NOT start or stop the backend server as a side effect — note server state as found
- Do NOT touch any database, schema, secrets, or `.env` files
- If the server is not running and scripts require it, record BLOCKED with reason — do not attempt to start it as part of this task

---

## Validation Plan
The result artifact `54_run-quarantine-smoke-tests.md` must contain:
- Exact invocation command(s) used
- Raw output (or representative excerpt if very long)
- Per-route verdict table
- Overall verdict (ALL PASS / PARTIAL / BLOCKED)
- Any unexpected findings noted explicitly

---

## Rollback Plan
This task makes no application changes. There is nothing to roll back. If scripts fail to run, the result artifact records BLOCKED and the next task addresses the specific blocker.

---

## Closeout Contract
The task is VERIFIED when:
- `relay/results/54_run-quarantine-smoke-tests.md` exists
- It contains the per-route verdict table with at least one row per quarantined route
- Overall verdict is stated explicitly
- If any route is FAIL or BLOCKED, findings are described with enough detail for the next task to act on them
