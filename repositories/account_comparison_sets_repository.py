"""JWT-owned comparison set create/archive (backend-owned, account-safe).

Places must exist but need not be favorites — the compare UI may still source
from favorites only. Create inserts comparison_sets + comparison_set_places
(sort_order 1..n) and rolls back the set row if place rows fail.
"""

from datetime import datetime, timezone

from services.supabase_user_client import get_supabase_for_user


class ComparisonSetsError(Exception):
    """Raised when a comparison set operation cannot proceed."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_account_id(client, jwt_token: str) -> str:
    user_resp = client.auth.get_user(jwt_token)
    if getattr(user_resp, "user", None) is None:
        raise ComparisonSetsError(
            "Authenticated user could not be resolved", "auth_user_missing",
        )
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise ComparisonSetsError(
            "No account membership for authenticated user", "account_missing",
        )
    return account_ids[0]


def _require_owned_active_profile(client, account_id, profile_id):
    try:
        result = (
            client.table("profiles")
            .select("id, archived_at, display_name")
            .eq("id", profile_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise ComparisonSetsError("profile not found", "profile_not_found") from exc
        raise
    if not result.data:
        raise ComparisonSetsError("profile not found", "profile_not_found")
    if result.data[0].get("archived_at") is not None:
        raise ComparisonSetsError("profile is archived", "profile_not_found")
    return result.data[0]


def _require_place(client, place_id):
    try:
        result = (
            client.table("places").select("id").eq("id", place_id).limit(1).execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise ComparisonSetsError("place not found", "place_not_found") from exc
        raise
    if not result.data:
        raise ComparisonSetsError("place not found", "place_not_found")


def _validate_place_ids(place_ids) -> list[str]:
    if not isinstance(place_ids, list):
        raise ComparisonSetsError("place_ids must be a list", "invalid_place_ids")
    ids = [str(pid) for pid in place_ids]
    if len(ids) < 2 or len(ids) > 5:
        raise ComparisonSetsError(
            "place_ids must contain between 2 and 5 items", "invalid_place_count",
        )
    if len(set(ids)) != len(ids):
        raise ComparisonSetsError("place_ids must be distinct", "duplicate_place_ids")
    return ids


def create_comparison_set(
    jwt_token: str,
    profile_id: str,
    place_ids: list,
    title: str = None,
) -> dict:
    """Insert a comparison set and its places (account-safe, place-existence only)."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    profile = _require_owned_active_profile(client, account_id, profile_id)
    ordered_place_ids = _validate_place_ids(place_ids)
    for pid in ordered_place_ids:
        _require_place(client, pid)

    resolved_title = title
    if not resolved_title:
        display = profile.get("display_name") or "Chart Record"
        resolved_title = f"Comparison · {display} · {len(ordered_place_ids)} places"

    set_payload = {
        "account_id": account_id,
        "profile_id": profile_id,
        "title": resolved_title,
    }
    set_result = client.table("comparison_sets").insert(set_payload).execute()
    if getattr(set_result, "error", None) or not set_result.data:
        raise ComparisonSetsError(
            f"could not create comparison set: {getattr(set_result, 'error', 'no data')}",
            "create_failed",
        )
    set_row = set_result.data[0]
    set_id = set_row["id"]

    place_rows = [
        {
            "comparison_set_id": set_id,
            "place_id": pid,
            "sort_order": idx,
        }
        for idx, pid in enumerate(ordered_place_ids, start=1)
    ]
    places_result = client.table("comparison_set_places").insert(place_rows).execute()
    if getattr(places_result, "error", None) or not places_result.data:
        # Best-effort rollback so no orphan set remains.
        try:
            client.table("comparison_sets").delete().eq("id", set_id).execute()
        except Exception:  # noqa: BLE001
            pass
        raise ComparisonSetsError(
            f"could not create comparison set places: {getattr(places_result, 'error', 'no data')}",
            "places_insert_failed",
        )

    return {
        "id": set_id,
        "profile_id": profile_id,
        "place_ids": ordered_place_ids,
        "title": set_row.get("title") or resolved_title,
        "status": "created",
    }


def archive_comparison_set(
    jwt_token: str,
    comparison_set_id: str,
    profile_id: str = None,
) -> dict:
    """Archive an owned comparison set (account-safe). Idempotent."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)

    try:
        existing = (
            client.table("comparison_sets")
            .select("id, profile_id, archived_at")
            .eq("id", comparison_set_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        ).data or []
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise ComparisonSetsError(
                "comparison set not found", "comparison_set_not_found",
            ) from exc
        raise
    if not existing:
        raise ComparisonSetsError(
            "comparison set not found", "comparison_set_not_found",
        )
    row = existing[0]
    if profile_id is not None and row.get("profile_id") != profile_id:
        raise ComparisonSetsError(
            "comparison set not found", "comparison_set_not_found",
        )

    if row.get("archived_at") is not None:
        return {
            "id": row["id"],
            "profile_id": row.get("profile_id"),
            "archived_at": row.get("archived_at"),
            "status": "already_archived",
        }

    now = _utc_now_iso()
    result = (
        client.table("comparison_sets")
        .update({"archived_at": now, "updated_at": now})
        .eq("id", comparison_set_id)
        .execute()
    )
    if getattr(result, "error", None) or not result.data:
        raise ComparisonSetsError(
            f"could not archive comparison set: {getattr(result, 'error', 'no data')}",
            "archive_failed",
        )
    out = result.data[0]
    return {
        "id": out.get("id"),
        "profile_id": out.get("profile_id"),
        "archived_at": out.get("archived_at"),
        "status": "archived",
    }

def update_comparison_set_state(
    jwt_token: str,
    profile_id: str,
    comparison_set_id: str,
    settings_snapshot_json: dict,
) -> dict:
    """Update comparison workspace reading state (settings_snapshot_json only)."""
    if not isinstance(settings_snapshot_json, dict):
        raise ComparisonSetsError(
            "settings_snapshot_json must be an object", "invalid_snapshot",
        )
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    _require_owned_active_profile(client, account_id, profile_id)

    try:
        existing = (
            client.table("comparison_sets")
            .select("id, profile_id, archived_at")
            .eq("id", comparison_set_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        ).data or []
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise ComparisonSetsError(
                "comparison set not found", "comparison_set_not_found",
            ) from exc
        raise
    if not existing:
        raise ComparisonSetsError(
            "comparison set not found", "comparison_set_not_found",
        )
    row = existing[0]
    if row.get("profile_id") != profile_id:
        raise ComparisonSetsError(
            "comparison set not found", "comparison_set_not_found",
        )
    if row.get("archived_at") is not None:
        raise ComparisonSetsError(
            "comparison set is archived", "comparison_set_not_found",
        )

    now = _utc_now_iso()
    result = (
        client.table("comparison_sets")
        .update({"settings_snapshot_json": settings_snapshot_json, "updated_at": now})
        .eq("id", comparison_set_id)
        .execute()
    )
    if getattr(result, "error", None) or not result.data:
        raise ComparisonSetsError(
            f"could not update comparison set state: {getattr(result, 'error', 'no data')}",
            "state_update_failed",
        )
    out = result.data[0]
    return {
        "id": out.get("id"),
        "profile_id": out.get("profile_id"),
        "settings_snapshot_json": out.get("settings_snapshot_json") or {},
        "updated_at": out.get("updated_at"),
        "status": "updated",
    }
