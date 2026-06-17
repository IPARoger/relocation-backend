# C4-4: GET /saved-investigations/{id} + map M1 migration

**Roadmap:** C4-4  
**Status:** VERIFIED

## 1. New route code

`main_centerline_FIXER.py` (after create handler):

```python
@app.get("/saved-investigations/{investigation_id}")
def api_get_saved_investigation(request: Request, investigation_id: str):
    jwt_token = _jwt_from_request(request)
    from repositories.account_saved_investigations_repository import (
        SavedInvestigationsError,
        get_saved_investigation_by_id,
    )

    try:
        return get_saved_investigation_by_id(jwt_token, investigation_id)
    except SavedInvestigationsError as err:
        if err.reason in ("auth_user_missing", "account_missing"):
            status = 401
        elif err.reason in ("saved_search_not_found",):
            status = 404
        else:
            status = 422
        raise HTTPException(
            status_code=status,
            detail={"error": err.reason, "message": str(err)},
        ) from err
```

Auth pattern matches create/rename/archive: `_jwt_from_request(request)` + sync repository call + `SavedInvestigationsError` → HTTP status mapping.

## 2. Repository method

Added `get_saved_investigation_by_id(jwt_token, saved_search_id)` in `repositories/account_saved_investigations_repository.py`.

Uses `get_supabase_for_user(jwt_token)`, `_resolve_account_id`, and account-scoped query on `saved_searches` with `archived_at IS NULL`. Returns: `id`, `account_id`, `profile_id`, `title`, `conditions_json`, `viewport_json`, `archived_at`.

## 3. M1 before/after

**Before** (`applySupabaseSavedInvestigationReplay` — direct Supabase SELECT):

```javascript
const accountId = window.CurrentUser && window.CurrentUser.accountId;

const { data: row, error: fetchErr } = await sbClient
    .from("saved_searches")
    .select("id, account_id, title, conditions_json, viewport_json, archived_at")
    .eq("id", explorationId)
    .is("archived_at", null)
    .maybeSingle();
// + client-side account_id ownership check
```

**After** (JWT fetch to backend-owned route):

```javascript
const { data: _sess } = await sbClient.auth.getSession();
const _token = _sess && _sess.session && _sess.session.access_token;
if (!_token) throw new Error("Session unavailable. Reload and try again.");
const _resp = await fetch(`${API_BASE}/saved-investigations/${encodeURIComponent(explorationId)}`, {
    headers: { "Authorization": "Bearer " + _token },
});
// 404 → "Saved investigation not found or archived."
const row = await _resp.json();
```

Fields consumed unchanged: `conditions_json`, `viewport_json`, `title`. Ownership enforced server-side (no client `account_id` check).

## 4. Smoke results

```
venv/bin/python scripts/smoke_saved_investigations.py  → exit 0
  PASS: fe_replay — status=Reopened: Smoke FE Replay …
  PASS: all 15 checks

venv/bin/python scripts/smoke_map_current.py  → exit 0
  overall_pass: true
```

Note: `smoke_map_current.py` requires a running server on port 8004; `smoke_saved_investigations.py` starts its own when port is free.

## 5. VERIFIED
