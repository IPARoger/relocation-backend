from datetime import datetime, timezone

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_profiles():
    client = get_supabase()
    result = client.table("profiles").select("*").order("created_at", desc=False).execute()
    return result.data


def get_profile(profile_id: str):
    client = get_supabase()
    result = client.table("profiles").select("*").eq("id", profile_id).limit(1).execute()
    return result.data[0] if result.data else None


def create_profile(display_name: str, account_user_id: str, profile_type: str = "human"):
    client = get_supabase()
    payload = {
        "display_name": display_name,
        "account_user_id": account_user_id,
        "profile_type": profile_type,
    }
    result = client.table("profiles").insert(payload).execute()
    return result.data[0] if result.data else None


def update_profile(profile_id: str, display_name: str = None, profile_type: str = None):
    client = get_supabase()
    payload = {"updated_at": _utc_now_iso()}
    if display_name is not None:
        payload["display_name"] = display_name
    if profile_type is not None:
        payload["profile_type"] = profile_type
    result = client.table("profiles").update(payload).eq("id", profile_id).execute()
    return result.data[0] if result.data else None


def archive_profile(profile_id: str):
    client = get_supabase()
    payload = {
        "archived_at": _utc_now_iso(),
        "updated_at": _utc_now_iso(),
    }
    result = client.table("profiles").update(payload).eq("id", profile_id).execute()
    return result.data[0] if result.data else None
