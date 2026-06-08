from datetime import datetime, timezone

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_saved_searches(profile_id: str):
    client = get_supabase()
    result = (
        client.table("saved_searches")
        .select("*")
        .eq("profile_id", profile_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data


def get_saved_search(saved_search_id: str):
    client = get_supabase()
    result = (
        client.table("saved_searches")
        .select("*")
        .eq("id", saved_search_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_saved_search(
    profile_id: str,
    title: str,
    intention_profile_id: str = None,
    search_type: str = None,
    conditions_json: dict = None,
    viewport_json: dict = None,
    settings_snapshot_json: dict = None,
    date_start: str = None,
    date_end: str = None,
):
    client = get_supabase()

    payload = {
        "profile_id": profile_id,
        "title": title,
    }

    optional = {
        "intention_profile_id": intention_profile_id,
        "search_type": search_type,
        "conditions_json": conditions_json,
        "viewport_json": viewport_json,
        "settings_snapshot_json": settings_snapshot_json,
        "date_start": date_start,
        "date_end": date_end,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = client.table("saved_searches").insert(payload).execute()
    return result.data[0] if result.data else None


def update_saved_search(
    saved_search_id: str,
    title: str = None,
    intention_profile_id: str = None,
    search_type: str = None,
    conditions_json: dict = None,
    viewport_json: dict = None,
    settings_snapshot_json: dict = None,
    date_start: str = None,
    date_end: str = None,
):
    client = get_supabase()

    payload = {"updated_at": _utc_now_iso()}

    optional = {
        "title": title,
        "intention_profile_id": intention_profile_id,
        "search_type": search_type,
        "conditions_json": conditions_json,
        "viewport_json": viewport_json,
        "settings_snapshot_json": settings_snapshot_json,
        "date_start": date_start,
        "date_end": date_end,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = (
        client.table("saved_searches")
        .update(payload)
        .eq("id", saved_search_id)
        .execute()
    )
    return result.data[0] if result.data else None


def archive_saved_search(saved_search_id: str):
    client = get_supabase()

    now = _utc_now_iso()
    payload = {
        "archived_at": now,
        "updated_at": now,
    }

    result = (
        client.table("saved_searches")
        .update(payload)
        .eq("id", saved_search_id)
        .execute()
    )
    return result.data[0] if result.data else None
