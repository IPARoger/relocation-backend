"""JWT-owned account settings save (backend-owned, account-safe).

Mirrors the prior browser path in app_shell.html saveAccountSettingsPatch:
shallow-merge a patch into the account-level user_settings row
(profile_id IS NULL), creating the row when none exists. Reads stay where they
are (account-store / store bridge); this module only owns the WRITE.
"""

from services.supabase_user_client import get_supabase_for_user


class SettingsError(Exception):
    """Raised when a settings operation cannot proceed."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def _resolve_account_ctx(client, jwt_token: str):
    user_resp = client.auth.get_user(jwt_token)
    user = getattr(user_resp, "user", None)
    if user is None:
        raise SettingsError("Authenticated user could not be resolved", "auth_user_missing")
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise SettingsError("No account membership for authenticated user", "account_missing")
    return account_ids[0], user.id


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
            raise SettingsError("profile not found", "profile_not_found") from exc
        raise
    if not result.data:
        raise SettingsError("profile not found", "profile_not_found")
    if result.data[0].get("archived_at") is not None:
        raise SettingsError("profile is archived", "profile_not_found")


def merge_account_settings(jwt_token: str, settings_patch: dict) -> dict:
    """Shallow-merge settings_patch into the account-level user_settings row."""
    if not isinstance(settings_patch, dict):
        raise SettingsError("settings_patch must be an object", "invalid_patch")

    client = get_supabase_for_user(jwt_token)
    account_id, account_user_id = _resolve_account_ctx(client, jwt_token)

    # Ownership validation for the account default chart record, when present.
    if "default_chart_record_id" in settings_patch:
        default_id = settings_patch.get("default_chart_record_id")
        if default_id:
            _require_owned_active_profile(client, account_id, default_id)

    existing = (
        client.table("user_settings")
        .select("id, settings_json")
        .eq("account_id", account_id)
        .is_("profile_id", "null")
        .limit(1)
        .execute()
    )
    rows = existing.data or []

    if rows:
        current = rows[0].get("settings_json") or {}
        merged = {**current, **settings_patch}
        result = (
            client.table("user_settings")
            .update({"settings_json": merged})
            .eq("id", rows[0]["id"])
            .execute()
        )
        if getattr(result, "error", None) or not result.data:
            raise SettingsError(
                f"could not update settings: {getattr(result, 'error', 'no data')}",
                "update_failed",
            )
        return {"settings_json": result.data[0].get("settings_json") or merged}

    merged = dict(settings_patch)
    payload = {
        "account_id": account_id,
        "account_user_id": account_user_id,
        "profile_id": None,
        "settings_json": merged,
    }
    result = client.table("user_settings").insert(payload).execute()
    if getattr(result, "error", None) or not result.data:
        raise SettingsError(
            f"could not create settings: {getattr(result, 'error', 'no data')}",
            "insert_failed",
        )
    return {"settings_json": result.data[0].get("settings_json") or merged}
