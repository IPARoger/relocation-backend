import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_profiles():
    """Service-role query — bypasses RLS. For internal/admin use only."""
    client = get_supabase()
    result = client.table("profiles").select("*").order("created_at", desc=False).execute()
    return result.data


def list_profiles_for_user(jwt_token: str):
    """RLS-scoped query using the authenticated user's JWT.

    Uses the anon key + the caller's Bearer token so the existing
    profiles_select RLS policy (account_id in app_account_ids()) filters
    results to the user's own account only.
    """
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not anon_key:
        raise RuntimeError("SUPABASE_URL or SUPABASE_ANON_KEY missing")
    client = create_client(url, anon_key)
    client.postgrest.auth(jwt_token)
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
