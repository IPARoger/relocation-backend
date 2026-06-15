from datetime import datetime, timezone

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_favorite_places(profile_id: str):
    client = get_supabase()
    result = (
        client.table("favorite_places")
        .select("*")
        .eq("profile_id", profile_id)
        .order("rank", desc=False)
        .execute()
    )
    return result.data


def get_favorite_place(favorite_place_id: str):
    client = get_supabase()
    result = (
        client.table("favorite_places")
        .select("*")
        .eq("id", favorite_place_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_favorite_place(
    profile_id: str,
    place_id: str,
    intention_profile_id: str = None,
    label: str = None,
    rank: int = None,
    starred: bool = None,
):
    client = get_supabase()

    payload = {
        "profile_id": profile_id,
        "place_id": place_id,
    }

    optional = {
        "intention_profile_id": intention_profile_id,
        "label": label,
        "rank": rank,
        "starred": starred,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = client.table("favorite_places").insert(payload).execute()
    return result.data[0] if result.data else None


def update_favorite_place(
    favorite_place_id: str,
    intention_profile_id: str = None,
    label: str = None,
    rank: int = None,
    starred: bool = None,
):
    client = get_supabase()

    payload = {"updated_at": _utc_now_iso()}

    optional = {
        "intention_profile_id": intention_profile_id,
        "label": label,
        "rank": rank,
        "starred": starred,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = (
        client.table("favorite_places")
        .update(payload)
        .eq("id", favorite_place_id)
        .execute()
    )
    return result.data[0] if result.data else None


def archive_favorite_place(favorite_place_id: str):
    client = get_supabase()

    now = _utc_now_iso()
    payload = {
        "archived_at": now,
        "updated_at": now,
    }

    result = (
        client.table("favorite_places")
        .update(payload)
        .eq("id", favorite_place_id)
        .execute()
    )
    return result.data[0] if result.data else None
