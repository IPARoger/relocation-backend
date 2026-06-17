"""JWT-owned saved investigation create/rename/archive (backend-owned, account-safe).

Mirrors map save and app_shell rename/archive paths. Create preserves the three
JSON payloads unchanged. Rename touches title + updated_at only. Archive is
idempotent. Reads (store bridge, map replay) stay where they are.
"""

from datetime import datetime, timezone

from services.supabase_user_client import get_supabase_for_user


class SavedInvestigationsError(Exception):
    """Raised when a saved investigation operation cannot proceed."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_account_id(client, jwt_token: str) -> str:
    user_resp = client.auth.get_user(jwt_token)
    if getattr(user_resp, "user", None) is None:
        raise SavedInvestigationsError(
            "Authenticated user could not be resolved", "auth_user_missing",
        )
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise SavedInvestigationsError(
            "No account membership for authenticated user", "account_missing",
        )
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
            raise SavedInvestigationsError(
                "profile not found", "profile_not_found",
            ) from exc
        raise
    if not result.data:
        raise SavedInvestigationsError("profile not found", "profile_not_found")
    if result.data[0].get("archived_at") is not None:
        raise SavedInvestigationsError("profile not found", "profile_not_found")


def _get_owned_row(client, account_id, saved_search_id, *, active_only: bool):
    try:
        q = (
            client.table("saved_searches")
            .select("id, profile_id, title, archived_at")
            .eq("id", saved_search_id)
            .eq("account_id", account_id)
            .limit(1)
        )
        if active_only:
            q = q.is_("archived_at", "null")
        result = q.execute()
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise SavedInvestigationsError(
                "saved search not found", "saved_search_not_found",
            ) from exc
        raise
    if not result.data:
        raise SavedInvestigationsError(
            "saved search not found", "saved_search_not_found",
        )
    return result.data[0]


def create_saved_investigation(
    jwt_token: str,
    profile_id: str,
    title: str,
    conditions_json: dict = None,
    viewport_json: dict = None,
    settings_snapshot_json: dict = None,
    search_type: str = "map",
) -> dict:
    """Insert a saved investigation for an owned active profile."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    _require_owned_active_profile(client, account_id, profile_id)

    name = (title or "").strip()
    if not name:
        raise SavedInvestigationsError("title is required", "invalid_title")

    payload = {
        "account_id": account_id,
        "profile_id": profile_id,
        "title": name,
        "search_type": search_type or "map",
        "conditions_json": conditions_json if conditions_json is not None else {},
        "viewport_json": viewport_json if viewport_json is not None else {},
        "settings_snapshot_json": settings_snapshot_json if settings_snapshot_json is not None else {},
    }
    result = client.table("saved_searches").insert(payload).execute()
    if getattr(result, "error", None) or not result.data:
        raise SavedInvestigationsError(
            f"could not create saved investigation: {getattr(result, 'error', 'no data')}",
            "create_failed",
        )
    row = result.data[0]
    return {
        "id": row.get("id"),
        "profile_id": row.get("profile_id"),
        "title": row.get("title") or name,
        "status": "created",
    }


def rename_saved_investigation(
    jwt_token: str,
    saved_search_id: str,
    title: str,
    profile_id: str = None,
) -> dict:
    """Rename an active owned saved investigation."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    row = _get_owned_row(client, account_id, saved_search_id, active_only=True)
    if profile_id is not None and row.get("profile_id") != profile_id:
        raise SavedInvestigationsError(
            "saved search not found", "saved_search_not_found",
        )

    name = (title or "").strip()
    if not name:
        raise SavedInvestigationsError("title is required", "invalid_title")

    now = _utc_now_iso()
    result = (
        client.table("saved_searches")
        .update({"title": name, "updated_at": now})
        .eq("id", saved_search_id)
        .execute()
    )
    if getattr(result, "error", None) or not result.data:
        raise SavedInvestigationsError(
            f"could not rename saved investigation: {getattr(result, 'error', 'no data')}",
            "rename_failed",
        )
    out = result.data[0]
    return {
        "id": out.get("id"),
        "profile_id": out.get("profile_id"),
        "title": out.get("title") or name,
        "status": "renamed",
    }


def archive_saved_investigation(
    jwt_token: str,
    saved_search_id: str,
    profile_id: str = None,
) -> dict:
    """Archive an owned saved investigation (idempotent)."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    row = _get_owned_row(client, account_id, saved_search_id, active_only=False)
    if profile_id is not None and row.get("profile_id") != profile_id:
        raise SavedInvestigationsError(
            "saved search not found", "saved_search_not_found",
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
        client.table("saved_searches")
        .update({"archived_at": now, "updated_at": now})
        .eq("id", saved_search_id)
        .execute()
    )
    if getattr(result, "error", None) or not result.data:
        raise SavedInvestigationsError(
            f"could not archive saved investigation: {getattr(result, 'error', 'no data')}",
            "archive_failed",
        )
    out = result.data[0]
    return {
        "id": out.get("id"),
        "profile_id": out.get("profile_id"),
        "archived_at": out.get("archived_at"),
        "status": "archived",
    }

def get_saved_investigation_by_id(jwt_token: str, saved_search_id: str) -> dict:
    """Fetch an active owned saved investigation for map replay."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    try:
        result = (
            client.table("saved_searches")
            .select("id, account_id, profile_id, title, conditions_json, viewport_json, archived_at")
            .eq("id", saved_search_id)
            .eq("account_id", account_id)
            .is_("archived_at", "null")
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise SavedInvestigationsError(
                "saved search not found", "saved_search_not_found",
            ) from exc
        raise
    if not result.data:
        raise SavedInvestigationsError(
            "saved search not found", "saved_search_not_found",
        )
    return result.data[0]

