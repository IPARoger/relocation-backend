# RESULT: 63_c4_3_favorites_jwt_route

**Roadmap ID:** C4-3
**Author:** Cursor (manual copy-paste track)
**Date:** 2026-06-17 UTC

## New route — `GET /favorites`

Added to `main_centerline_FIXER.py` after `/favorites/archive`:

```python
@app.get("/favorites")
def api_list_favorites(request: Request, profile_id: str):
    jwt_token = _jwt_from_request(request)
    from repositories.account_favorites_repository import (
        FavoritesError,
        list_favorites,
    )
    try:
        items = list_favorites(jwt_token, profile_id=profile_id)
        return {"favorites": items}
    except FavoritesError as err:
        status = 404 if err.reason in ("profile_not_found", "favorite_not_found") else 422
        raise HTTPException(
            status_code=status,
            detail={"error": err.reason, "message": str(err)},
        ) from err
```

Auth pattern: `_jwt_from_request` → `list_favorites(jwt_token, profile_id)` → ownership validated via `_require_owned_active_profile` inside repository. Matches existing `/favorites/save` and `/favorites/archive` pattern exactly.

## Repository method added

`list_favorites(jwt_token, profile_id)` appended to `repositories/account_favorites_repository.py`.

Returns list of `{id, profile_id, place_id, label, rank, starred, display_name, latitude, longitude}` — joined with `places` table via Supabase `.select()` relationship.

## M3 before/after (`applyMapFavoriteButtonState`, ~line 2419)

**Before:** Direct `sbClient.from("favorite_places")` SELECT filtered by `account_id`, `profile_id`, `place_id`.

**After:** `GET /favorites?profile_id=` fetch with Bearer token, then `.some((f) => f.place_id === place.id)` client-side filter.

## M4 before/after (`loadSavedPlacesForActiveProfile`, ~line 6175)

**Before:** Two Supabase queries — `favorite_places` list + `places` join by IDs.

**After:** Single `GET /favorites?profile_id=` fetch returns favorites with `display_name, latitude, longitude` pre-joined. Two Supabase reads eliminated.

## Smoke results

| Smoke | Exit | Result |
|-------|------|--------|
| `smoke_map_current.py` | **0** | `overall_pass: true` |
| `smoke_saved_investigations.py` | **0** | `PASS: smoke_saved_investigations` |

## Status

**VERIFIED**
