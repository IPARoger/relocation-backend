"""JWT-owned profile + birth record creation (backend-owned, account-safe).

Mirrors first_profile_intake.js: insert profiles then birth_records with
compensating profile delete if the birth row fails. Places must exist;
no favorite requirement.
"""

from services.supabase_user_client import get_supabase_for_user


class ProfileCreateError(Exception):
    """Raised when profile+birth creation cannot proceed."""

    def __init__(self, message: str, reason: str, profile_id: str = None):
        super().__init__(message)
        self.reason = reason
        self.profile_id = profile_id


def _resolve_account_ctx(client, jwt_token: str):
    user_resp = client.auth.get_user(jwt_token)
    user = getattr(user_resp, "user", None)
    if user is None:
        raise ProfileCreateError(
            "Authenticated user could not be resolved", "auth_user_missing",
        )
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise ProfileCreateError(
            "No account membership for authenticated user", "account_missing",
        )
    return account_ids[0], user.id


def _require_place(client, place_id):
    try:
        result = (
            client.table("places").select("id").eq("id", place_id).limit(1).execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise ProfileCreateError("place not found", "place_not_found") from exc
        raise
    if not result.data:
        raise ProfileCreateError("place not found", "place_not_found")


def create_profile_with_birth(
    jwt_token: str,
    display_name: str,
    birth_date: str,
    birth_time_mode: str,
    birth_place_id: str,
    birth_time_start: str = None,
    timezone_id: str = None,
    profile_type: str = "human",
) -> dict:
    """Create a profile and its birth record for the caller account."""
    client = get_supabase_for_user(jwt_token)
    account_id, account_user_id = _resolve_account_ctx(client, jwt_token)

    name = (display_name or "").strip()
    if not name:
        raise ProfileCreateError("display_name is required", "invalid_display_name")
    if not birth_date:
        raise ProfileCreateError("birth_date is required", "invalid_birth_date")
    if not birth_place_id:
        raise ProfileCreateError("birth_place_id is required", "invalid_birth_place_id")

    mode = (birth_time_mode or "").strip().lower()
    if mode not in ("exact", "unknown"):
        raise ProfileCreateError(
            "birth_time_mode must be exact or unknown", "invalid_birth_time_mode",
        )
    if mode == "exact" and not birth_time_start:
        raise ProfileCreateError(
            "birth_time_start is required when birth_time_mode is exact",
            "birth_time_required",
        )

    _require_place(client, birth_place_id)

    profile_result = (
        client.table("profiles")
        .insert({
            "account_id": account_id,
            "account_user_id": account_user_id,
            "display_name": name,
            "profile_type": profile_type or "human",
        })
        .execute()
    )
    if getattr(profile_result, "error", None) or not profile_result.data:
        raise ProfileCreateError(
            f"could not create profile: {getattr(profile_result, 'error', 'no data')}",
            "profile_create_failed",
        )
    profile_row = profile_result.data[0]
    profile_id = profile_row["id"]

    birth_payload = {
        "account_id": account_id,
        "profile_id": profile_id,
        "birth_date": birth_date,
        "birth_time_mode": mode,
        "birth_place_id": birth_place_id,
        "birth_time_start": birth_time_start if mode == "exact" else None,
        "timezone_id": timezone_id,
    }
    birth_result = client.table("birth_records").insert(birth_payload).execute()
    if getattr(birth_result, "error", None) or not birth_result.data:
        birth_err = getattr(birth_result, "error", "no data")
        try:
            client.table("profiles").delete().eq("id", profile_id).execute()
        except Exception as rollback_exc:  # noqa: BLE001
            raise ProfileCreateError(
                f"birth record failed and profile rollback failed: {rollback_exc}; "
                f"orphan profile_id={profile_id}; birth error: {birth_err}",
                "rollback_failed",
                profile_id=profile_id,
            ) from rollback_exc
        raise ProfileCreateError(
            f"could not create birth record: {birth_err}",
            "birth_record_failed",
        )

    birth_row = birth_result.data[0]
    return {
        "profile_id": profile_id,
        "birth_record_id": birth_row.get("id"),
        "display_name": name,
        "birth_place_id": birth_place_id,
        "status": "created",
    }


def _utc_now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def _require_owned_active_profile(client, account_id, profile_id):
    try:
        result = (
            client.table("profiles")
            .select("id, display_name, archived_at")
            .eq("id", profile_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise ProfileCreateError("profile not found", "profile_not_found") from exc
        raise
    if not result.data:
        raise ProfileCreateError("profile not found", "profile_not_found")
    if result.data[0].get("archived_at") is not None:
        raise ProfileCreateError("profile not found", "profile_not_found")
    return result.data[0]


def _list_active_profiles(client, account_id):
    return (
        client.table("profiles")
        .select("id, display_name")
        .eq("account_id", account_id)
        .is_("archived_at", "null")
        .order("created_at", desc=False)
        .execute()
    ).data or []


def _get_account_default_profile_id(client, account_id):
    result = (
        client.table("user_settings")
        .select("settings_json")
        .eq("account_id", account_id)
        .is_("profile_id", "null")
        .limit(1)
        .execute()
    )
    if not result.data:
        return None
    return (result.data[0].get("settings_json") or {}).get("default_chart_record_id")


def _compute_replacement_profile_id(active, profile_id, current_default):
    remaining = [p for p in active if p.get("id") != profile_id]
    if not remaining:
        return None, None
    replacement_id = current_default
    if not (
        replacement_id
        and replacement_id != profile_id
        and any(p.get("id") == replacement_id for p in remaining)
    ):
        replacement_id = remaining[0]["id"]
    replacement = next((p for p in remaining if p.get("id") == replacement_id), None)
    return replacement_id, replacement


def rename_profile(jwt_token: str, profile_id: str, display_name: str) -> dict:
    """Rename an active owned profile."""
    client = get_supabase_for_user(jwt_token)
    account_id, _account_user_id = _resolve_account_ctx(client, jwt_token)
    _require_owned_active_profile(client, account_id, profile_id)

    name = (display_name or "").strip()
    if not name:
        raise ProfileCreateError("display_name is required", "invalid_display_name")

    now = _utc_now_iso()
    result = (
        client.table("profiles")
        .update({"display_name": name, "updated_at": now})
        .eq("id", profile_id)
        .eq("account_id", account_id)
        .is_("archived_at", "null")
        .execute()
    )
    if getattr(result, "error", None) or not result.data:
        raise ProfileCreateError(
            f"could not rename profile: {getattr(result, 'error', 'no data')}",
            "rename_failed",
        )
    row = result.data[0]
    return {
        "profile_id": row.get("id") or profile_id,
        "display_name": row.get("display_name") or name,
        "status": "renamed",
    }


def archive_profile(jwt_token: str, profile_id: str) -> dict:
    """Archive an owned active profile with replacement metadata."""
    client = get_supabase_for_user(jwt_token)
    account_id, _account_user_id = _resolve_account_ctx(client, jwt_token)

    try:
        existing = (
            client.table("profiles")
            .select("id, display_name, archived_at")
            .eq("id", profile_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        ).data or []
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise ProfileCreateError("profile not found", "profile_not_found") from exc
        raise
    if not existing:
        raise ProfileCreateError("profile not found", "profile_not_found")
    row = existing[0]
    if row.get("archived_at") is not None:
        return {
            "profile_id": row["id"],
            "archived_at": row.get("archived_at"),
            "status": "already_archived",
            "was_default": False,
            "replacement_profile_id": None,
            "replacement_display_name": None,
        }

    active = _list_active_profiles(client, account_id)
    if len(active) <= 1:
        raise ProfileCreateError(
            "cannot archive the only remaining profile", "only_profile_remaining",
        )
    if not any(p.get("id") == profile_id for p in active):
        raise ProfileCreateError("profile not found", "profile_not_found")

    current_default = _get_account_default_profile_id(client, account_id)
    replacement_id, replacement = _compute_replacement_profile_id(
        active, profile_id, current_default,
    )
    replacement_name = (replacement or {}).get("display_name") or "another profile"
    was_default = bool(current_default and current_default == profile_id)

    now = _utc_now_iso()
    result = (
        client.table("profiles")
        .update({"archived_at": now, "updated_at": now})
        .eq("id", profile_id)
        .eq("account_id", account_id)
        .is_("archived_at", "null")
        .execute()
    )
    if getattr(result, "error", None) or not result.data:
        raise ProfileCreateError(
            f"could not archive profile: {getattr(result, 'error', 'no data')}",
            "archive_failed",
        )
    out = result.data[0]
    return {
        "profile_id": out.get("id") or profile_id,
        "archived_at": out.get("archived_at") or now,
        "status": "archived",
        "was_default": was_default,
        "replacement_profile_id": replacement_id,
        "replacement_display_name": replacement_name,
    }
