# RESULT: 74_h4_slice4_a2a_shell

**Roadmap ID:** H4-4
**Author:** Cursor (cloud executor)
**Commit:** `80a8701`

## Files changed
- `app_shell.html` — A2A bottled shell (`renderComparisonA2aBlockShellHtml`, angle pill strip, dual hydrate, collapse sync, beta CSS)
- `scripts/smoke_h4_slice4_a2a_shell.py` — static slice 4 smoke + regression chain

## Validation evidence
```text
$ python3 scripts/smoke_h4_slice4_a2a_shell.py
PASS 14/14
  smoke_h4_slice3_pih_shell.py: PASS (via regression chain)
  smoke_h4_slice2_ais_shell.py: PASS
  smoke_h4b_comparison_authority.py: PASS
  smoke_comparison_a2a_matrix.py: 10/10 passed

$ python3 scripts/smoke_h4_slice3_pih_shell.py
PASS 11/11

$ python3 scripts/smoke_h4b_comparison_authority.py
PASS 14/14

$ python3 scripts/smoke_comparison_a2a_matrix.py
10/10 passed
```

`data-a2a-shape="matrix"` preserved in `renderA2aComparisonHtml`; matrix data logic untouched.

## Rollback command
```bash
git reset --hard e37bf9d
```
(or `git reset --hard checkpoint/h4b_start_clean`)

## Rejected scope
Notes rail, City Intelligence, Profile carousel, relocated/frozen surfaces, backend/API/schema changes.

**VERIFIED**
