"""JWT-owned Quick Share create + public frozen read (QUICK-SHARE-MVP)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import uuid

from services.supabase_client import get_supabase
from services.supabase_user_client import get_supabase_for_user


class QuickShareError(Exception):
    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


DEFAULT_EXPIRY_DAYS = 30


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _resolve_account_id(client, jwt_token: str) -> str:
    user_resp = client.auth.get_user(jwt_token)
    if getattr(user_resp, "user", None) is None:
        raise QuickShareError(
            "Authenticated user could not be resolved", "auth_user_missing",
        )
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise QuickShareError(
            "No account membership for authenticated user", "account_missing",
        )
    return account_ids[0]


def _require_owned_active_profile(client, account_id: str, profile_id: str) -> None:
    try:
        result = (
            client.table("profiles")
            .select("id, display_name, archived_at")
            .eq("id", profile_id)
            .eq("account_id", account_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise QuickShareError("profile not found", "profile_not_found") from exc
        raise
    if not result.data:
        raise QuickShareError("profile not found", "profile_not_found")
    if result.data[0].get("archived_at") is not None:
        raise QuickShareError("profile not found", "profile_not_found")


def create_quick_share(
    jwt_token: str,
    *,
    profile_id: str,
    profile_display_name: str | None,
    source_surface: str,
    conditions_json: dict | None,
    viewport_json: dict | None,
    settings_snapshot_json: dict | None,
    place_id: str | None = None,
    place_label: str | None = None,
    chart_facts_json: dict | None = None,
) -> dict:
    client = get_supabase_for_user(jwt_token)
    account_id = _resolve_account_id(client, jwt_token)
    _require_owned_active_profile(client, account_id, profile_id)

    display_name = (profile_display_name or "").strip()
    if not display_name:
        prof = (
            client.table("profiles")
            .select("display_name")
            .eq("id", profile_id)
            .limit(1)
            .execute()
        )
        if prof.data:
            display_name = (prof.data[0].get("display_name") or "").strip()
    if not display_name:
        display_name = "Profile"

    surface = (source_surface or "map").strip() or "map"
    if surface not in ("map", "chart"):
        raise QuickShareError("invalid source_surface", "invalid_source_surface")

    now = _utc_now()
    expires_at = now + timedelta(days=DEFAULT_EXPIRY_DAYS)
    share_id = str(uuid.uuid4())

    payload = {
        "id": share_id,
        "account_id": account_id,
        "profile_id": profile_id,
        "profile_display_name": display_name,
        "source_surface": surface,
        "conditions_json": conditions_json if isinstance(conditions_json, dict) else {},
        "viewport_json": viewport_json if isinstance(viewport_json, dict) else {},
        "settings_snapshot_json": (
            settings_snapshot_json if isinstance(settings_snapshot_json, dict) else {}
        ),
        "place_id": place_id,
        "place_label": place_label,
        "chart_facts_json": chart_facts_json if isinstance(chart_facts_json, dict) else None,
        "expires_at": expires_at.isoformat(),
    }

    svc = get_supabase()
    result = svc.table("quick_shares").insert(payload).execute()
    if getattr(result, "error", None) or not result.data:
        raise QuickShareError(
            f"could not create quick share: {getattr(result, 'error', 'no data')}",
            "create_failed",
        )

    row = result.data[0]
    qs_id = row.get("id") or share_id
    return {
        "quick_share_id": qs_id,
        "url": f"/map_CURRENT.html?quickShare={qs_id}",
        "expires_at": row.get("expires_at") or expires_at.isoformat(),
    }


def get_quick_share_public(quick_share_id: str) -> dict:
    try:
        uuid.UUID(str(quick_share_id))
    except ValueError as exc:
        raise QuickShareError("quick share not found", "not_found") from exc

    svc = get_supabase()
    try:
        result = (
            svc.table("quick_shares")
            .select(
                "id, profile_display_name, source_surface, conditions_json, "
                "viewport_json, settings_snapshot_json, place_id, place_label, "
                "chart_facts_json, created_at, expires_at, revoked_at"
            )
            .eq("id", quick_share_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise QuickShareError("quick share not found", "not_found") from exc
        if "quick_shares" in msg and "does not exist" in msg:
            raise QuickShareError("quick share storage unavailable", "storage_unavailable") from exc
        raise

    if not result.data:
        raise QuickShareError("quick share not found", "not_found")

    row = result.data[0]
    if row.get("revoked_at"):
        raise QuickShareError("quick share not found", "not_found")

    expires_raw = row.get("expires_at")
    if expires_raw:
        expires_dt = datetime.fromisoformat(str(expires_raw).replace("Z", "+00:00"))
        if expires_dt.tzinfo is None:
            expires_dt = expires_dt.replace(tzinfo=timezone.utc)
        if expires_dt <= _utc_now():
            raise QuickShareError("quick share expired", "expired")

    conditions = row.get("conditions_json") if isinstance(row.get("conditions_json"), dict) else {}
    public_conditions = dict(conditions)
    public_conditions.pop("chart_record_id", None)

    return {
        "quick_share_id": row.get("id"),
        "brand": "Relocation Astrology",
        "kind": "quick_share_map",
        "profile_display_name": row.get("profile_display_name") or "Profile",
        "source_surface": row.get("source_surface") or "map",
        "conditions_json": public_conditions,
        "viewport_json": row.get("viewport_json") if isinstance(row.get("viewport_json"), dict) else {},
        "settings_snapshot_json": (
            row.get("settings_snapshot_json")
            if isinstance(row.get("settings_snapshot_json"), dict)
            else {}
        ),
        "place_id": row.get("place_id"),
        "place_label": row.get("place_label"),
        "chart_facts_json": row.get("chart_facts_json"),
        "created_at": row.get("created_at"),
        "expires_at": row.get("expires_at"),
        "shared_view_notice": (
            "Shared map/search snapshot — read-only. Not a formal report or export."
        ),
    }
