from datetime import datetime, timezone

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_birth_records(profile_id: str):
    client = get_supabase()
    result = (
        client.table("birth_records")
        .select("*")
        .eq("profile_id", profile_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data


def get_birth_record(record_id: str):
    client = get_supabase()
    result = (
        client.table("birth_records")
        .select("*")
        .eq("id", record_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_birth_record(
    profile_id: str,
    birth_date: str = None,
    birth_time_mode: str = None,
    birth_time_start: str = None,
    birth_time_end: str = None,
    birth_place_id: str = None,
    timezone_id: str = None,
    utc_datetime_start: str = None,
    utc_datetime_end: str = None,
    confidence_notes: str = None,
    chart_settings_json: dict = None,
):
    client = get_supabase()
    payload = {"profile_id": profile_id}
    optional = {
        "birth_date": birth_date,
        "birth_time_mode": birth_time_mode,
        "birth_time_start": birth_time_start,
        "birth_time_end": birth_time_end,
        "birth_place_id": birth_place_id,
        "timezone_id": timezone_id,
        "utc_datetime_start": utc_datetime_start,
        "utc_datetime_end": utc_datetime_end,
        "confidence_notes": confidence_notes,
        "chart_settings_json": chart_settings_json,
    }
    for key, value in optional.items():
        if value is not None:
            payload[key] = value
    result = client.table("birth_records").insert(payload).execute()
    return result.data[0] if result.data else None


def update_birth_record(
    record_id: str,
    birth_date: str = None,
    birth_time_mode: str = None,
    birth_time_start: str = None,
    birth_time_end: str = None,
    birth_place_id: str = None,
    timezone_id: str = None,
    utc_datetime_start: str = None,
    utc_datetime_end: str = None,
    confidence_notes: str = None,
    chart_settings_json: dict = None,
):
    client = get_supabase()
    payload = {"updated_at": _utc_now_iso()}
    optional = {
        "birth_date": birth_date,
        "birth_time_mode": birth_time_mode,
        "birth_time_start": birth_time_start,
        "birth_time_end": birth_time_end,
        "birth_place_id": birth_place_id,
        "timezone_id": timezone_id,
        "utc_datetime_start": utc_datetime_start,
        "utc_datetime_end": utc_datetime_end,
        "confidence_notes": confidence_notes,
        "chart_settings_json": chart_settings_json,
    }
    for key, value in optional.items():
        if value is not None:
            payload[key] = value
    result = (
        client.table("birth_records")
        .update(payload)
        .eq("id", record_id)
        .execute()
    )
    return result.data[0] if result.data else None


def archive_birth_record(record_id: str):
    client = get_supabase()
    payload = {
        "archived_at": _utc_now_iso(),
        "updated_at": _utc_now_iso(),
    }
    result = (
        client.table("birth_records")
        .update(payload)
        .eq("id", record_id)
        .execute()
    )
    return result.data[0] if result.data else None
