# RESULT: 04_sb-4-smoke-inventory

**Roadmap ID:** SB-4
**Author:** Cursor (execution half)
**Date:** 2026-06-18

## Objective

List files under `smokes/` matching `*ownership*` or `*quarantine*`.

## Summary

| Pattern | Matches |
|---------|--------:|
| `*ownership*` | 0 |
| `*quarantine*` | 0 |
| **Total** | **0** |

**Finding:** The directory `smokes/` does not exist at the repository root. No files match either glob pattern.

## Inventory

*(empty — no `smokes/` directory and no matching files)*

## Related note (out of scope)

The repo has `tests/smoke/` (singular) with four files, none of whose names contain `ownership` or `quarantine`:

- `tests/smoke/map-page-smoke.spec.js`
- `tests/smoke/mint_session.py`
- `tests/smoke/saved-investigation-smoke.spec.js`
- `tests/smoke/session.cjs`

Task scope is strictly `smokes/` per task file; `tests/smoke/` was not substituted.

## Files changed

- `relay-sandbox/results/04_sb-4-smoke-inventory.md` (this closeout only)
- No changes to source, test, or smoke scripts.

## Validation evidence

```text
$ test -d smokes && echo 'smokes exists' || echo 'smokes MISSING'
smokes MISSING

$ find smokes -type f \( -iname '*ownership*' -o -iname '*quarantine*' \) 2>/dev/null | sort
(no output — directory absent)

$ find . -type d -name 'smokes' 2>/dev/null
(no output — no smokes/ directory anywhere in repo)
```

## Rollback command

```bash
rm relay-sandbox/results/04_sb-4-smoke-inventory.md
```

## Rejected scope

- Creating or populating a `smokes/` directory (task scope: read-only inventory).
- Substituting `tests/smoke/` for `smokes/` (task path is explicit).
- Schema, database, secrets, migration, or renderer/math/overlay changes (not required; not attempted).
- Opening a PR (not requested).

## VERIFIED

Read-only inventory complete: **0** files under `smokes/` match `*ownership*` or `*quarantine*` because `smokes/` is absent from the working tree.
