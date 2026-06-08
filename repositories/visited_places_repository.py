from services.supabase_client import get_supabase


def list_visited_places(profile_id: str):
    client = get_supabase()
    result = (
        client.table("visited_places")
        .select("*")
        .eq("profile_id", profile_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data


def get_visited_place(visited_place_id: str):
    client = get_supabase()
    result = (
        client.table("visited_places")
        .select("*")
        .eq("id", visited_place_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_visited_place(
    profile_id: str,
    place_id: str,
    visited_at: str = None,
    source: str = None,
    notes: str = None,
):
    client = get_supabase()

    payload = {
        "profile_id": profile_id,
        "place_id": place_id,
    }

    optional = {
        "visited_at": visited_at,
        "source": source,
        "notes": notes,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = client.table("visited_places").insert(payload).execute()
    return result.data[0] if result.data else None
