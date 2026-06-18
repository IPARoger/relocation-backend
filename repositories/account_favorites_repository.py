"""JWT-owned favorite save/archive (backend-owned, account-safe).

Mirrors the prior browser favorite paths (map insert, shell archive) but
enforces the caller account, active profile ownership, and place existence.
Save is idempotent against the favorite_places unique(profile_id, place_id)
constraint: an active row is returned as-is, an archived row is reactivated,
otherwise a new row is inserted. Reads stay where they are.
"""

from datetime import datetime, timezone

from services.supabase_user_client import get_supabase_for_user


class FavoritesError(Exception):
    """Raised when a favorite operation cannot proceed."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_account_id(client, jwt_token: str) -> str:
    user_resp = client.auth.get_user(jwt_token)
    if getattr(user_resp, "user", None) is None:
        raise FavoritesError("Authenticated user could not be resolved", "auth_user_missing")
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise FavoritesError("No account membership for authenticated user", "account_missing")
    return account_ids[0]


def _require_owned_active_profile(client, account_id, profile_id):
    try:
        result = (
            client.table("profiles")
            .select("id, archived_at")
            .eq("id", profile_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise FavoritesError("profile not found", "profile_not_found") from exc
        raise
    if not result.data:
        raise FavoritesError("profile not found", "profile_not_found")
    if result.data[0].get("archived_at") is not None:
        raise FavoritesError("profile is archived", "profile_not_found")


def _require_place(client, place_id):
    try:
        result = (
            client.table("places").select("id").eq("id", place_id).limit(1).execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise FavoritesError("place not found", "place_not_found") from exc
        raise
    if not result.data:
        raise FavoritesError("place not found", "place_not_found")


def _shape(row: dict) -> dict:
    return {
        "id": row.get("id"),
        "account_id": row.get("account_id"),
        "profile_id": row.get("profile_id"),
        "place_id": row.get("place_id"),
        "label": row.get("label"),
        "rank": row.get("rank"),
        "starred": row.get("starred"),
        "archived_at": row.get("archived_at"),
        "reactivated": row.get("_reactivated", False),
        "status": row.get("_status", "created"),
    }


def save_favorite(jwt_token: str, profile_id: str, place_id: str,
                  label: str = None, rank: int = None, starred: bool = True) -> dict:
    """Idempotent favorite save: return active, reactivate archived, or insert."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    _require_owned_active_profile(client, account_id, profile_id)
    _require_place(client, place_id)

    existing = (
        client.table("favorite_places")
        .select("id, account_id, profile_id, place_id, label, rank, starred, archived_at")
        .eq("account_id", account_id)
        .eq("profile_id", profile_id)
        .eq("place_id", place_id)
        .limit(1)
        .execute()
    ).data or []

    if existing:
        row = existing[0]
        if row.get("archived_at") is None:
            row["_status"] = "exists"
            return _shape(row)
        # Reactivate the archived favorite in place (no duplicate row).
        patch = {"archived_at": None, "updated_at": _utc_now_iso()}
        if label is not None:
            patch["label"] = label
        if rank is not None:
            patch["rank"] = rank
        if starred is not None:
            patch["starred"] = starred
        result = (
            client.table("favorite_places").update(patch).eq("id", row["id"]).execute()
        )
        if getattr(result, "error", None) or not result.data:
            raise FavoritesError(
                f"could not reactivate favorite: {getattr(result, 'error', 'no data')}",
                "reactivate_failed",
            )
        out = result.data[0]
        out["_reactivated"] = True
        out["_status"] = "reactivated"
        return _shape(out)

    payload = {
        "account_id": account_id,
        "profile_id": profile_id,
        "place_id": place_id,
    }
    if label is not None:
        payload["label"] = label
    if rank is not None:
        payload["rank"] = rank
    if starred is not None:
        payload["starred"] = starred
    result = client.table("favorite_places").insert(payload).execute()
    if getattr(result, "error", None) or not result.data:
        raise FavoritesError(
            f"could not save favorite: {getattr(result, 'error', 'no data')}",
            "insert_failed",
        )
    out = result.data[0]
    out["_status"] = "created"
    return _shape(out)


def archive_favorite(jwt_token: str, favorite_id: str, profile_id: str = None) -> dict:
    """Archive an owned favorite (account-safe). Returns the archived row."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)

    try:
        existing = (
            client.table("favorite_places")
            .select("id, account_id, profile_id, place_id, label, rank, starred, archived_at")
            .eq("id", favorite_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        ).data or []
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise FavoritesError("favorite not found", "favorite_not_found") from exc
        raise
    if not existing:
        raise FavoritesError("favorite not found", "favorite_not_found")
    row = existing[0]
    if profile_id is not None and row.get("profile_id") != profile_id:
        raise FavoritesError("favorite not found", "favorite_not_found")

    if row.get("archived_at") is not None:
        return _shape(row)

    result = (
        client.table("favorite_places")
        .update({"archived_at": _utc_now_iso(), "updated_at": _utc_now_iso()})
        .eq("id", favorite_id)
        .execute()
    )
    if getattr(result, "error", None) or not result.data:
        raise FavoritesError(
            f"could not archive favorite: {getattr(result, 'error', 'no data')}",
            "archive_failed",
        )
    return _shape(result.data[0])


def list_favorites(jwt_token: str, profile_id: str) -> list:
    """Return active favorites with joined place data for a profile."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    _require_owned_active_profile(client, account_id, profile_id)
    result = (
        client.table("favorite_places")
        .select("id, profile_id, place_id, label, rank, starred, places(id, display_name, latitude, longitude, provider, geonames_id, country_code, admin1)")
        .eq("account_id", account_id)
        .eq("profile_id", profile_id)
        .is_("archived_at", "null")
        .order("created_at", desc=True)
        .execute()
    )
    rows = result.data or []
    out = []
    for row in rows:
        place = row.get("places") or {}
        out.append({
            "id": row.get("id"),
            "profile_id": row.get("profile_id"),
            "place_id": row.get("place_id"),
            "label": row.get("label"),
            "rank": row.get("rank"),
            "starred": row.get("starred"),
            "display_name": place.get("display_name"),
            "latitude": place.get("latitude"),
            "longitude": place.get("longitude"),
            "provider": place.get("provider"),
            "geonames_id": place.get("geonames_id"),
            "country_code": place.get("country_code"),
            "admin1": place.get("admin1"),
        })
    return out
