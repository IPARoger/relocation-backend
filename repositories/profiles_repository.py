from services.supabase_client import get_supabase


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
