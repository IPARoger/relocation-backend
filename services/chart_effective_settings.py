"""Resolve effective astrology settings for Layer-1 chart compute (/relocated-chart)."""

from __future__ import annotations

from fastapi import Request

from services.account_settings_resolver import get_effective_settings


def optional_jwt_from_request(request: Request | None) -> str | None:
    if request is None:
        return None
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[len("Bearer ") :].strip()
    return token or None


def load_account_settings_json_for_jwt(jwt_token: str) -> dict | None:
    from services.supabase_user_client import get_supabase_for_user

    client = get_supabase_for_user(jwt_token)
    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        return None
    account_id = account_ids[0]
    existing = (
        client.table("user_settings")
        .select("settings_json")
        .eq("account_id", account_id)
        .is_("profile_id", "null")
        .limit(1)
        .execute()
    )
    rows = existing.data or []
    if not rows:
        return None
    settings_json = rows[0].get("settings_json")
    return settings_json if isinstance(settings_json, dict) else {}


def resolve_chart_effective_settings(
    request: Request | None,
    *,
    house_proximity_orb_query: float | None = None,
) -> dict:
    """Effective settings used for canonical_chart compute.

    Authenticated requests load account user_settings and ignore query-param
    astrology overrides. Unauthenticated requests use registry defaults with an
    optional house_proximity_orb query override (smokes / map without session).
    """
    stored: dict | None = None
    jwt = optional_jwt_from_request(request)
    if jwt:
        stored = load_account_settings_json_for_jwt(jwt)

    eff = dict(get_effective_settings(stored))

    if jwt is None and house_proximity_orb_query is not None:
        eff["house_proximity_orb_degrees"] = house_proximity_orb_query

    return eff
