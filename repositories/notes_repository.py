from datetime import datetime, timezone

from services.supabase_client import get_supabase


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_notes(profile_id: str):
    client = get_supabase()
    result = (
        client.table("notes")
        .select("*")
        .eq("profile_id", profile_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data


def get_note(note_id: str):
    client = get_supabase()
    result = (
        client.table("notes")
        .select("*")
        .eq("id", note_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def create_note(
    profile_id: str,
    target_type: str,
    body: str,
    intention_profile_id: str = None,
    target_id: str = None,
    section_key: str = None,
    title: str = None,
):
    client = get_supabase()

    payload = {
        "profile_id": profile_id,
        "target_type": target_type,
        "body": body,
    }

    optional = {
        "intention_profile_id": intention_profile_id,
        "target_id": target_id,
        "section_key": section_key,
        "title": title,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = client.table("notes").insert(payload).execute()
    return result.data[0] if result.data else None


def update_note(
    note_id: str,
    target_type: str = None,
    body: str = None,
    intention_profile_id: str = None,
    target_id: str = None,
    section_key: str = None,
    title: str = None,
):
    client = get_supabase()

    payload = {"updated_at": _utc_now_iso()}

    optional = {
        "target_type": target_type,
        "body": body,
        "intention_profile_id": intention_profile_id,
        "target_id": target_id,
        "section_key": section_key,
        "title": title,
    }

    for key, value in optional.items():
        if value is not None:
            payload[key] = value

    result = (
        client.table("notes")
        .update(payload)
        .eq("id", note_id)
        .execute()
    )
    return result.data[0] if result.data else None


def archive_note(note_id: str):
    client = get_supabase()

    now = _utc_now_iso()
    payload = {
        "archived_at": now,
        "updated_at": now,
    }

    result = (
        client.table("notes")
        .update(payload)
        .eq("id", note_id)
        .execute()
    )
    return result.data[0] if result.data else None
