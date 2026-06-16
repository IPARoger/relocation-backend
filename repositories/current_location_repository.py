"""Read/write current-location ownership (JWT-scoped, account-safe).

Mirrors the browser write sequence previously in current_location_editor.js:
  1. UPDATE current_location_history SET is_current=false for the profile/account
  2. INSERT a new is_current=true row

All access is scoped to the caller JWT (RLS enforced) plus explicit account
ownership checks. No RPC, no ORM abstraction.
"""

from __future__ import annotations

from datetime import datetime, timezone

from services.supabase_user_client import get_supabase_for_user


class CurrentLocationError(Exception):
    """Raised when a current-location operation cannot proceed."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_account_id(client, jwt_token: str) -> str:
    user_resp = client.auth.get_user(jwt_token)
    user = getattr(user_resp, "user", None)
    if user is None:
        raise CurrentLocationError(
            "Authenticated user could not be resolved",
            "auth_user_missing",
        )

    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise CurrentLocationError(
            "No account membership found for authenticated user",
            "account_missing",
        )
    return account_ids[0]


def _require_owned_profile(client, account_id: str, profile_id: str) -> None:
    """Ensure the profile exists and belongs to the caller's account.

    The query is RLS-scoped, so a profile from another account returns no row.
    """
    try:
        result = (
            client.table("profiles")
            .select("id, account_id")
            .eq("id", profile_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise CurrentLocationError("profile not found", "profile_not_found") from exc
        raise
    if not result.data:
        raise CurrentLocationError("profile not found", "profile_not_found")


def _require_place(client, place_id: str) -> dict:
    """Ensure the place exists; return the place payload."""
    try:
        result = (
            client.table("places")
            .select("id, display_name, latitude, longitude, timezone_id")
            .eq("id", place_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise CurrentLocationError("place not found", "place_not_found") from exc
        raise
    if not result.data:
        raise CurrentLocationError("place not found", "place_not_found")
    return result.data[0]


def _fetch_place(client, place_id: str) -> dict | None:
    if not place_id:
        return None
    result = (
        client.table("places")
        .select("id, display_name, latitude, longitude, timezone_id")
        .eq("id", place_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def _shape_response(row: dict, place: dict | None) -> dict:
    return {
        "id": row.get("id"),
        "profile_id": row.get("profile_id"),
        "account_id": row.get("account_id"),
        "place_id": row.get("place_id"),
        "selected_at": row.get("selected_at"),
        "is_current": row.get("is_current"),
        "source": row.get("source"),
        "place": place,
    }


def get_current_location(jwt_token: str, profile_id: str) -> dict:
    """Return the active current-location row (or null) for a profile.

    Shape: { "profile_id": ..., "current_location": <row|null> }
    """
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    _require_owned_profile(client, account_id, profile_id)

    result = (
        client.table("current_location_history")
        .select("id, profile_id, account_id, place_id, selected_at, is_current, source")
        .eq("account_id", account_id)
        .eq("profile_id", profile_id)
        .eq("is_current", True)
        .order("selected_at", desc=True)
        .limit(1)
        .execute()
    )

    if not result.data:
        return {"profile_id": profile_id, "current_location": None}

    row = result.data[0]
    place = _fetch_place(client, row.get("place_id"))
    return {"profile_id": profile_id, "current_location": _shape_response(row, place)}


def set_current_location(
    jwt_token: str,
    profile_id: str,
    place_id: str,
    source: str = "manual",
) -> dict:
    """Retire prior current rows and insert a new current row.

    Returns { "profile_id": ..., "current_location": <row> } including place.
    """
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    _require_owned_profile(client, account_id, profile_id)
    place = _require_place(client, place_id)

    # A. Retire existing current rows (non-fatal if none exist).
    retire = (
        client.table("current_location_history")
        .update({"is_current": False})
        .eq("account_id", account_id)
        .eq("profile_id", profile_id)
        .eq("is_current", True)
        .execute()
    )
    if getattr(retire, "error", None):
        raise CurrentLocationError(
            f"could not retire prior current rows: {retire.error}",
            "retire_failed",
        )

    # B. Insert the new current row.
    payload = {
        "account_id": account_id,
        "profile_id": profile_id,
        "place_id": place_id,
        "is_current": True,
        "source": source,
        "selected_at": _utc_now_iso(),
    }
    insert = client.table("current_location_history").insert(payload).execute()
    if getattr(insert, "error", None) or not insert.data:
        raise CurrentLocationError(
            f"could not insert current row: {getattr(insert, 'error', 'no data')}",
            "insert_failed",
        )

    row = insert.data[0]
    return {"profile_id": profile_id, "current_location": _shape_response(row, place)}
