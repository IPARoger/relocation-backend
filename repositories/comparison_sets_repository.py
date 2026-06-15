from datetime import datetime, timezone

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_comparison_sets(profile_id: str):
    client = get_supabase()
    result = (
        client.table("comparison_sets")
        .select("*")
        .eq("profile_id", profile_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data


def get_comparison_set(comparison_set_id: str):
    client = get_supabase()
    result = (
        client.table("comparison_sets")
        .select("*")
        .eq("id", comparison_set_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_comparison_set(
    profile_id: str,
    title: str,
    intention_profile_id: str = None,
    settings_snapshot_json: dict = None,
):
    client = get_supabase()

    payload = {
        "profile_id": profile_id,
        "title": title,
    }

    optional = {
        "intention_profile_id": intention_profile_id,
        "settings_snapshot_json": settings_snapshot_json,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = client.table("comparison_sets").insert(payload).execute()
    return result.data[0] if result.data else None


def update_comparison_set(
    comparison_set_id: str,
    title: str = None,
    intention_profile_id: str = None,
    settings_snapshot_json: dict = None,
):
    client = get_supabase()

    payload = {"updated_at": _utc_now_iso()}

    optional = {
        "title": title,
        "intention_profile_id": intention_profile_id,
        "settings_snapshot_json": settings_snapshot_json,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = (
        client.table("comparison_sets")
        .update(payload)
        .eq("id", comparison_set_id)
        .execute()
    )
    return result.data[0] if result.data else None


def archive_comparison_set(comparison_set_id: str):
    client = get_supabase()

    now = _utc_now_iso()
    payload = {
        "archived_at": now,
        "updated_at": now,
    }

    result = (
        client.table("comparison_sets")
        .update(payload)
        .eq("id", comparison_set_id)
        .execute()
    )
    return result.data[0] if result.data else None


def list_comparison_set_places(comparison_set_id: str):
    client = get_supabase()
    result = (
        client.table("comparison_set_places")
        .select("*")
        .eq("comparison_set_id", comparison_set_id)
        .order("sort_order", desc=False)
        .execute()
    )
    return result.data


def add_place_to_comparison_set(
    comparison_set_id: str,
    place_id: str,
    sort_order: int = 0,
    role: str = None,
):
    client = get_supabase()

    payload = {
        "comparison_set_id": comparison_set_id,
        "place_id": place_id,
        "sort_order": sort_order,
    }

    if role is not None:
        payload["role"] = role

    result = client.table("comparison_set_places").insert(payload).execute()
    return result.data[0] if result.data else None


def remove_place_from_comparison_set(comparison_set_id: str, place_id: str):
    client = get_supabase()
    result = (
        client.table("comparison_set_places")
        .delete()
        .eq("comparison_set_id", comparison_set_id)
        .eq("place_id", place_id)
        .execute()
    )
    return result.data
