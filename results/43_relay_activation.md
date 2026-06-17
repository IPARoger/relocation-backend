# Task 43 — Relay Activation (dry_run)

**Date:** 2026-06-17  
**Scope:** `.github/workflows/relay.yml` branch ref fix only. No product code changes.

---

## 1. relay.yml before/after diff

```diff
--- a/.github/workflows/relay.yml
+++ b/.github/workflows/relay.yml
@@ -26,7 +26,7 @@ jobs:
       - name: Checkout relay branch
         uses: actions/checkout@v4
         with:
-          ref: checkpoint/pre-phase-2-3
+          ref: main
```

No other lines changed.

---

## 2. dry_run value confirmed

- `workflow_dispatch` input `dry_run` **default: `true`** (unchanged)
- Dry-run path runs when `inputs.dry_run == true` (unchanged)
- Live path steps still gated on `inputs.dry_run == false` (unchanged)

---

## 3. Secret references

| Secret | Status |
|--------|--------|
| `${{ secrets.TELEGRAM_BOT_TOKEN }}` | **Present** (low-balance warn, Cursor low-balance warn, approval notify steps) |
| `${{ secrets.TELEGRAM_CHAT_ID }}` | **Present** (same steps) |

Also referenced for live path (unchanged): `OPENAI_API_KEY`, `OPENAI_MODEL`, `CURSOR_API_KEY`, `CURSOR_MODEL`.

---

## 4. relay_notify.py labels (first 30 lines)

Five fixed event keys:

1. `started`
2. `complete`
3. `approval`
4. `verified`
5. `not-verified`

Accepts `--dry-run` flag (prints without sending). Workflow also invokes `low-balance` in live steps (outside the five-label docblock in usage section).

---

## 5. Notes (unchanged by this task)

These still reference `checkpoint/pre-phase-2-3` and were **not** modified per task scope (checkout ref only):

- `git push origin HEAD:checkpoint/pre-phase-2-3`
- `RELAY_BRANCH: checkpoint/pre-phase-2-3`

Follow-up may be needed before live relay commits/pushes to `main`.

---

## **VERIFIED**
