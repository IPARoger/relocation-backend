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
