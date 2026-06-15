from datetime import datetime, timezone

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def get_user_settings(account_user_id: str, profile_id: str = None):
    client = get_supabase()

    query = (
        client.table("user_settings")
        .select("*")
        .eq("account_user_id", account_user_id)
    )

    if profile_id is None:
        query = query.is_("profile_id", "null")
    else:
        query = query.eq("profile_id", profile_id)

    result = query.limit(1).execute()
    return result.data[0] if result.data else None


def create_user_settings(
    account_user_id: str,
    settings_json: dict,
    profile_id: str = None,
):
    client = get_supabase()

    payload = {
        "account_user_id": account_user_id,
        "settings_json": settings_json,
    }

    if profile_id is not None:
        payload["profile_id"] = profile_id

    result = client.table("user_settings").insert(payload).execute()
    return result.data[0] if result.data else None


def update_user_settings(
    settings_id: str,
    settings_json: dict = None,
):
    client = get_supabase()

    payload = {"updated_at": _utc_now_iso()}

    if settings_json is not None:
        payload["settings_json"] = settings_json

    result = (
        client.table("user_settings")
        .update(payload)
        .eq("id", settings_id)
        .execute()
    )
    return result.data[0] if result.data else None
