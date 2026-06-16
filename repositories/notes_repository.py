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


# ---------------------------------------------------------------------------
# JWT-scoped note ownership (account-safe). Used by the backend-owned note
# endpoints. Unlike the legacy service-role helpers above, these enforce the
# caller account, the owning profile / comparison set, and a fixed target_type.
#
# Save semantics mirror the prior browser path: update the newest active row for
# the (account, target, section); insert one only when none exists.
# ---------------------------------------------------------------------------

from services.supabase_user_client import get_supabase_for_user


class NotesError(Exception):
    """Raised when a note operation cannot proceed."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


def _resolve_account_id(client, jwt_token: str) -> str:
    user_resp = client.auth.get_user(jwt_token)
    if getattr(user_resp, "user", None) is None:
        raise NotesError("Authenticated user could not be resolved", "auth_user_missing")
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise NotesError("No account membership for authenticated user", "account_missing")
    return account_ids[0]


def _shape_note(row: dict) -> dict:
    return {
        "id": row.get("id"),
        "account_id": row.get("account_id"),
        "profile_id": row.get("profile_id"),
        "target_type": row.get("target_type"),
        "target_id": row.get("target_id"),
        "section_key": row.get("section_key"),
        "body": row.get("body") or "",
        "updated_at": row.get("updated_at"),
        "archived_at": row.get("archived_at"),
    }


def _find_active_note(client, account_id, target_type, *, profile_id=None,
                      target_id=None, section_key="main"):
    """Newest active note for the (account, target, section), or None.

    Matches legacy rows where section_key is NULL by treating NULL as 'main'.
    """
    query = (
        client.table("notes")
        .select("id, account_id, profile_id, target_type, target_id, section_key, "
                "body, updated_at, archived_at")
        .eq("account_id", account_id)
        .eq("target_type", target_type)
        .is_("archived_at", "null")
        .order("updated_at", desc=True)
    )
    if profile_id is not None:
        query = query.eq("profile_id", profile_id)
    if target_id is not None:
        query = query.eq("target_id", target_id)
    rows = query.execute().data or []
    for row in rows:
        if (row.get("section_key") or "main") == section_key:
            return row
    return None


def _upsert_note(client, *, account_id, profile_id, target_type, target_id,
                 section_key, body):
    existing = _find_active_note(
        client, account_id, target_type,
        profile_id=profile_id if target_type == "chart_record" else None,
        target_id=target_id, section_key=section_key,
    )
    text = str(body if body is not None else "")
    if existing:
        result = (
            client.table("notes")
            .update({
                "body": text,
                "section_key": section_key,
                "updated_at": _utc_now_iso(),
            })
            .eq("id", existing["id"])
            .execute()
        )
        if getattr(result, "error", None) or not result.data:
            raise NotesError(
                f"could not update note: {getattr(result, 'error', 'no data')}",
                "update_failed",
            )
        return _shape_note(result.data[0])

    payload = {
        "account_id": account_id,
        "profile_id": profile_id,
        "target_type": target_type,
        "target_id": target_id,
        "section_key": section_key,
        "body": text,
    }
    result = client.table("notes").insert(payload).execute()
    if getattr(result, "error", None) or not result.data:
        raise NotesError(
            f"could not insert note: {getattr(result, 'error', 'no data')}",
            "insert_failed",
        )
    return _shape_note(result.data[0])


def _require_owned_profile(client, account_id, profile_id):
    try:
        result = (
            client.table("profiles")
            .select("id")
            .eq("id", profile_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise NotesError("profile not found", "profile_not_found") from exc
        raise
    if not result.data:
        raise NotesError("profile not found", "profile_not_found")


def _require_owned_comparison_set(client, account_id, comparison_set_id):
    """Return owning profile_id for the comparison set, or raise."""
    try:
        result = (
            client.table("comparison_sets")
            .select("id, profile_id")
            .eq("id", comparison_set_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise NotesError("comparison set not found", "comparison_set_not_found") from exc
        raise
    if not result.data:
        raise NotesError("comparison set not found", "comparison_set_not_found")
    return result.data[0]["profile_id"]


def set_chart_record_note(jwt_token: str, profile_id: str, body: str,
                          section_key: str = "main") -> dict:
    """Save the chart-record note for a profile (backend-owned, account-safe)."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    _require_owned_profile(client, account_id, profile_id)
    return _upsert_note(
        client,
        account_id=account_id,
        profile_id=profile_id,
        target_type="chart_record",
        target_id=None,
        section_key=section_key or "main",
        body=body,
    )


def _require_owned_saved_search(client, account_id, saved_search_id):
    """Return owning profile_id for the saved search, or raise.

    Restricts to active (non-archived) rows so notes cannot attach to a
    soft-deleted investigation.
    """
    try:
        result = (
            client.table("saved_searches")
            .select("id, profile_id")
            .eq("id", saved_search_id)
            .eq("account_id", account_id)
            .is_("archived_at", "null")
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise NotesError("saved search not found", "saved_search_not_found") from exc
        raise
    if not result.data:
        raise NotesError("saved search not found", "saved_search_not_found")
    return result.data[0]["profile_id"]


def set_saved_investigation_note(jwt_token: str, saved_search_id: str, body: str,
                                 section_key: str = "main") -> dict:
    """Save the saved-investigation note (backend-owned, account-safe)."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    owning_profile_id = _require_owned_saved_search(client, account_id, saved_search_id)
    return _upsert_note(
        client,
        account_id=account_id,
        profile_id=owning_profile_id,
        target_type="saved_investigation",
        target_id=saved_search_id,
        section_key=section_key or "main",
        body=body,
    )


def set_comparison_set_note(jwt_token: str, comparison_set_id: str, body: str,
                            section_key: str = "main") -> dict:
    """Save the comparison-set note (backend-owned, account-safe)."""
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    owning_profile_id = _require_owned_comparison_set(client, account_id, comparison_set_id)
    return _upsert_note(
        client,
        account_id=account_id,
        profile_id=owning_profile_id,
        target_type="comparison_set",
        target_id=comparison_set_id,
        section_key=section_key or "main",
        body=body,
    )
