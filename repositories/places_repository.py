from services.supabase_client import get_supabase


def list_places(limit: int = 50):
    client = get_supabase()
    result = (
        client.table("places")
        .select("*")
        .order("display_name", desc=False)
        .limit(limit)
        .execute()
    )
    return result.data


def get_place(place_id: str):
    client = get_supabase()
    result = (
        client.table("places")
        .select("*")
        .eq("id", place_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_place(
    display_name: str,
    latitude: float,
    longitude: float,
    provider: str = None,
    provider_place_id: str = None,
    geonames_id: str = None,
    canonical_name: str = None,
    admin1: str = None,
    admin2: str = None,
    country_code: str = None,
    country_name: str = None,
    timezone_id: str = None,
    population: int = None,
    importance_rank: float = None,
    language_code: str = None,
    alternate_names_json: dict = None,
    source_json: dict = None,
):
    client = get_supabase()

    payload = {
        "display_name": display_name,
        "latitude": latitude,
        "longitude": longitude,
    }

    optional = {
        "provider": provider,
        "provider_place_id": provider_place_id,
        "geonames_id": geonames_id,
        "canonical_name": canonical_name,
        "admin1": admin1,
        "admin2": admin2,
        "country_code": country_code,
        "country_name": country_name,
        "timezone_id": timezone_id,
        "population": population,
        "importance_rank": importance_rank,
        "language_code": language_code,
        "alternate_names_json": alternate_names_json,
        "source_json": source_json,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = client.table("places").insert(payload).execute()
    return result.data[0] if result.data else None


def search_places(query: str, limit: int = 20):
    client = get_supabase()
    pattern = f"%{query}%"
    result = (
        client.table("places")
        .select("*")
        .ilike("display_name", pattern)
        .order("importance_rank", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data

def search_places_by_geonames(geonames_id: str):
    # Return places matching geonames_id (0 or 1 row as list).
    client = get_supabase()
    gid = str(geonames_id or "").strip()
    if not gid:
        return []
    try:
        result = (
            client.table("places")
            .select("*")
            .eq("geonames_id", gid)
            .limit(1)
            .execute()
        )
    except Exception:  # noqa: BLE001
        return []
    return result.data or []

