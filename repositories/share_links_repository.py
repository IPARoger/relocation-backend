from datetime import datetime, timezone

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_share_links(profile_id: str):
    client = get_supabase()
    result = (
        client.table("share_links")
        .select("*")
        .eq("profile_id", profile_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data


def get_share_link(share_link_id: str):
    client = get_supabase()
    result = (
        client.table("share_links")
        .select("*")
        .eq("id", share_link_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_share_link(
    profile_id: str,
    target_type: str,
    target_id: str,
    slug: str,
    visibility: str = None,
    hide_birth_data: bool = None,
    include_notes: bool = None,
    include_tables: bool = None,
    include_chart_wheel: bool = None,
    expires_at: str = None,
):
    client = get_supabase()

    payload = {
        "profile_id": profile_id,
        "target_type": target_type,
        "target_id": target_id,
        "slug": slug,
    }

    optional = {
        "visibility": visibility,
        "hide_birth_data": hide_birth_data,
        "include_notes": include_notes,
        "include_tables": include_tables,
        "include_chart_wheel": include_chart_wheel,
        "expires_at": expires_at,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = client.table("share_links").insert(payload).execute()
    return result.data[0] if result.data else None


def revoke_share_link(share_link_id: str):
    client = get_supabase()

    payload = {
        "revoked_at": _utc_now_iso(),
    }

    result = (
        client.table("share_links")
        .update(payload)
        .eq("id", share_link_id)
        .execute()
    )
    return result.data[0] if result.data else None
