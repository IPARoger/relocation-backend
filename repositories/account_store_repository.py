"""Read-only account store assembler (mirrors supabase_store_bridge.js)."""

from __future__ import annotations

from dataclasses import dataclass, field

from services.account_settings_resolver import get_effective_settings
from services.supabase_user_client import get_supabase_for_user


class AccountStoreBuildError(Exception):
    """Raised when the store cannot be assembled (matches bridge hard failures)."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


@dataclass
class AccountStoreAssemblyMeta:
    """Non-fatal assembly notes (not part of the bridge store shape)."""

    non_fatal_warnings: list[str] = field(default_factory=list)
    unavailable_fields: list[str] = field(default_factory=list)


def _to_confidence_tier(mode: str | None) -> str:
    if mode == "exact":
        return "T0"
    if mode == "approximate":
        return "T2"
    return "T3"


def _to_record_type(profile_type: str | None) -> str:
    if profile_type == "research":
        return "research"
    if profile_type == "human":
        return "self"
    return "client"


def _trim_time(pg_time: str | None) -> str | None:
    if not pg_time:
        return None
    return pg_time[:5]


def _resolve_account_context(client, jwt_token: str) -> tuple[str, str]:
    """Return (account_id, account_name) for the authenticated user."""
    user_resp = client.auth.get_user(jwt_token)
    user = getattr(user_resp, "user", None)
    if user is None:
        raise AccountStoreBuildError(
            "Authenticated user could not be resolved",
            "auth_user_missing",
        )

    account_ids = client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        raise AccountStoreBuildError(
            "No account membership found for authenticated user",
            "account_missing",
        )

    account_id = account_ids[0]
    acct_row = (
        client.table("accounts")
        .select("id, name")
        .eq("id", account_id)
        .limit(1)
        .execute()
    )
    account_name = "Personal"
    if acct_row.data:
        account_name = acct_row.data[0].get("name") or account_name

    return account_id, account_name


def build_account_store(jwt_token: str) -> dict:
    """Assemble the Store v3 shape for the caller's account (read-only)."""
    client = get_supabase_for_user(jwt_token)
    account_id, account_name = _resolve_account_context(client, jwt_token)
    meta = AccountStoreAssemblyMeta(
        unavailable_fields=[
            "chart_record_history",
            "tags",
            "notes",
        ],
    )

    profiles_result = (
        client.table("profiles")
        .select("id, display_name, profile_type")
        .eq("account_id", account_id)
        .is_("archived_at", "null")
        .order("created_at", desc=False)
        .execute()
    )
    if profiles_result.data is None and getattr(profiles_result, "error", None):
        raise AccountStoreBuildError(
            f"profiles: {profiles_result.error}",
            "profiles_query_failed",
        )
    profiles = profiles_result.data or []
    if not profiles:
        raise AccountStoreBuildError(
            "No profiles found. Intake overlay required.",
            "profiles_missing",
        )

    birth_result = (
        client.table("birth_records")
        .select(
            "id, profile_id, birth_date, birth_time_mode, birth_time_start, "
            "birth_place_id, timezone_id"
        )
        .eq("account_id", account_id)
        .order("created_at", desc=True)
        .execute()
    )
    if birth_result.data is None and getattr(birth_result, "error", None):
        raise AccountStoreBuildError(
            f"birth_records: {birth_result.error}",
            "birth_records_query_failed",
        )

    birth_by_profile_id: dict[str, dict] = {}
    for br in birth_result.data or []:
        pid = br.get("profile_id")
        if pid and pid not in birth_by_profile_id:
            birth_by_profile_id[pid] = br

    favs_result = (
        client.table("favorite_places")
        .select("id, profile_id, place_id, rank, label")
        .eq("account_id", account_id)
        .is_("archived_at", "null")
        .order("rank", desc=False)
        .execute()
    )
    if favs_result.data is None and getattr(favs_result, "error", None):
        raise AccountStoreBuildError(
            f"favorite_places: {favs_result.error}",
            "favorite_places_query_failed",
        )
    favs = favs_result.data or []

    cs_result = (
        client.table("comparison_sets")
        .select("id, profile_id")
        .eq("account_id", account_id)
        .is_("archived_at", "null")
        .execute()
    )
    if cs_result.data is None and getattr(cs_result, "error", None):
        raise AccountStoreBuildError(
            f"comparison_sets: {cs_result.error}",
            "comparison_sets_query_failed",
        )
    comp_sets = cs_result.data or []

    csp_data: list[dict] = []
    if comp_sets:
        cs_ids = [cs["id"] for cs in comp_sets]
        csp_result = (
            client.table("comparison_set_places")
            .select("comparison_set_id, place_id, sort_order")
            .in_("comparison_set_id", cs_ids)
            .order("sort_order", desc=False)
            .execute()
        )
        if csp_result.data is None and getattr(csp_result, "error", None):
            raise AccountStoreBuildError(
                f"comparison_set_places: {csp_result.error}",
                "comparison_set_places_query_failed",
            )
        csp_data = csp_result.data or []

    saved_searches: list[dict] = []
    try:
        ss_result = (
            client.table("saved_searches")
            .select(
                "id, profile_id, title, conditions_json, viewport_json, "
                "settings_snapshot_json, created_at, updated_at"
            )
            .eq("account_id", account_id)
            .is_("archived_at", "null")
            .order("updated_at", desc=True)
            .execute()
        )
        if getattr(ss_result, "error", None):
            meta.non_fatal_warnings.append(
                f"saved_searches query non-fatal: {ss_result.error}"
            )
        else:
            saved_searches = ss_result.data or []
    except Exception as exc:  # noqa: BLE001
        meta.non_fatal_warnings.append(f"saved_searches query non-fatal: {exc}")

    current_location_by_profile_id: dict[str, str] = {}
    try:
        cl_result = (
            client.table("current_location_history")
            .select("profile_id, place_id")
            .eq("account_id", account_id)
            .eq("is_current", True)
            .execute()
        )
        if getattr(cl_result, "error", None):
            meta.non_fatal_warnings.append(
                f"current_location_history query non-fatal: {cl_result.error}"
            )
        else:
            for row in cl_result.data or []:
                pid = row.get("profile_id")
                place_id = row.get("place_id")
                if pid and place_id and pid not in current_location_by_profile_id:
                    current_location_by_profile_id[pid] = place_id
    except Exception as exc:  # noqa: BLE001
        meta.non_fatal_warnings.append(
            f"current_location_history query non-fatal: {exc}"
        )

    place_id_set: set[str] = set()
    for br in birth_by_profile_id.values():
        if br.get("birth_place_id"):
            place_id_set.add(br["birth_place_id"])
    for fav in favs:
        if fav.get("place_id"):
            place_id_set.add(fav["place_id"])
    for row in csp_data:
        if row.get("place_id"):
            place_id_set.add(row["place_id"])
    for place_id in current_location_by_profile_id.values():
        if place_id:
            place_id_set.add(place_id)

    places_by_id: dict[str, dict] = {}
    if place_id_set:
        places_result = (
            client.table("places")
            .select("id, display_name, latitude, longitude")
            .in_("id", list(place_id_set))
            .execute()
        )
        if places_result.data is None and getattr(places_result, "error", None):
            raise AccountStoreBuildError(
                f"places: {places_result.error}",
                "places_query_failed",
            )
        for place in places_result.data or []:
            places_by_id[place["id"]] = place

    raw_settings = None
    settings_result = (
        client.table("user_settings")
        .select("settings_json, profile_id")
        .eq("account_id", account_id)
        .order("created_at", desc=False)
        .execute()
    )
    if not getattr(settings_result, "error", None) and settings_result.data:
        acct_row = next(
            (r for r in settings_result.data if r.get("profile_id") is None),
            None,
        )
        chosen = acct_row or settings_result.data[0]
        raw_settings = chosen.get("settings_json") or {}

    chart_record_note_by_profile_id: dict[str, str] = {}
    try:
        notes_result = (
            client.table("notes")
            .select("profile_id, body, updated_at, target_type, archived_at")
            .eq("account_id", account_id)
            .eq("target_type", "chart_record")
            .is_("archived_at", "null")
            .order("updated_at", desc=True)
            .execute()
        )
        if getattr(notes_result, "error", None):
            meta.non_fatal_warnings.append(
                f"notes chart_record query non-fatal: {notes_result.error}"
            )
        else:
            for row in notes_result.data or []:
                pid = row.get("profile_id")
                if pid and pid not in chart_record_note_by_profile_id:
                    chart_record_note_by_profile_id[pid] = row.get("body") or ""
    except Exception as exc:  # noqa: BLE001
        meta.non_fatal_warnings.append(f"notes chart_record query non-fatal: {exc}")

    comparison_set_note_by_target_id: dict[str, str] = {}
    try:
        cmp_notes_result = (
            client.table("notes")
            .select("target_id, body, updated_at, target_type, archived_at")
            .eq("account_id", account_id)
            .eq("target_type", "comparison_set")
            .is_("archived_at", "null")
            .order("updated_at", desc=True)
            .execute()
        )
        if getattr(cmp_notes_result, "error", None):
            meta.non_fatal_warnings.append(
                f"notes comparison_set query non-fatal: {cmp_notes_result.error}"
            )
        else:
            for row in cmp_notes_result.data or []:
                tid = row.get("target_id")
                if tid and tid not in comparison_set_note_by_target_id:
                    comparison_set_note_by_target_id[tid] = row.get("body") or ""
    except Exception as exc:  # noqa: BLE001
        meta.non_fatal_warnings.append(
            f"notes comparison_set query non-fatal: {exc}"
        )

    store_places = [
        {
            "id": place["id"],
            "display_name": place.get("display_name"),
            "lat": float(place["latitude"]),
            "lon": float(place["longitude"]),
            "schema_version": 1,
        }
        for place in places_by_id.values()
    ]

    store_birth_profiles = []
    for profile in profiles:
        br = birth_by_profile_id.get(profile["id"])
        if not br:
            continue
        store_birth_profiles.append(
            {
                "id": br["id"],
                "birth_date": br.get("birth_date"),
                "birth_time": _trim_time(br.get("birth_time_start"))
                if br.get("birth_time_mode") == "exact"
                else None,
                "birth_place_id": br.get("birth_place_id"),
                "timezone_id": br.get("timezone_id"),
                "confidence_tier": _to_confidence_tier(br.get("birth_time_mode")),
                "confidence_metadata": {},
                "representative_time": None,
                "schema_version": 1,
                "updated_at": None,
            }
        )

    store_clients = []
    for profile in profiles:
        br = birth_by_profile_id.get(profile["id"])
        if not br:
            continue
        store_clients.append(
            {
                "id": profile["id"],
                "display_name": profile.get("display_name"),
                "birth_profile_id": br["id"],
                "record_type": _to_record_type(profile.get("profile_type")),
                "current_location_place_id": current_location_by_profile_id.get(
                    profile["id"]
                ),
                "notes": chart_record_note_by_profile_id.get(profile["id"], ""),
                "tags": [],
                "schema_version": 1,
                "updated_at": None,
            }
        )

    if not store_clients:
        raise AccountStoreBuildError(
            "Profiles exist but no birth records found. "
            "Intake overlay must complete birth record entry.",
            "birth_records_missing",
        )

    saved_default = (raw_settings or {}).get("default_chart_record_id")
    default_is_valid = saved_default and any(
        c["id"] == saved_default for c in store_clients
    )
    default_chart_record_id = (
        saved_default if default_is_valid else store_clients[0]["id"]
    )

    effective_settings = get_effective_settings(raw_settings, None)
    store_user_settings = {
        "settings_version": effective_settings["settings_version"],
        "house_system": effective_settings["house_system"],
        "zodiac_mode": effective_settings["zodiac_mode"],
        "orb_defaults": effective_settings["major_aspect_orbs"],
        "visible_minor_aspects": effective_settings["visible_minor_aspects"],
        "out_of_sign_aspects": effective_settings["out_of_sign_aspects"],
        "visible_planets": effective_settings["visible_planets"],
        "visible_bodies": effective_settings["visible_bodies"],
        "visible_major_aspects": effective_settings["visible_major_aspects"],
        "visible_minor_aspects_list": effective_settings[
            "visible_minor_aspects_list"
        ],
        "major_aspect_orbs": effective_settings["major_aspect_orbs"],
        "minor_aspect_orbs": effective_settings["minor_aspect_orbs"],
        "house_proximity_orb_degrees": effective_settings[
            "house_proximity_orb_degrees"
        ],
        "subsequent_house_policy": effective_settings["subsequent_house_policy"],
        "aspect_to_angle_orbs": effective_settings["aspect_to_angle_orbs"],
        "helper_layers": effective_settings["helper_layers"],
        "ontology_pack_id": effective_settings["ontology_pack_id"],
        "default_chart_record_id": default_chart_record_id,
        "updated_at": None,
    }

    store_favs = [
        {
            "id": fav["id"],
            "client_id": fav.get("profile_id"),
            "place_id": fav.get("place_id"),
            "saved_investigation_id": None,
            "notes": fav.get("label") or "",
            "sort_order": fav.get("rank") if fav.get("rank") is not None else 0,
            "schema_version": 1,
        }
        for fav in favs
    ]

    csp_by_set_id: dict[str, list[str]] = {}
    for row in csp_data:
        csp_by_set_id.setdefault(row["comparison_set_id"], []).append(row["place_id"])

    store_comp_sets = [
        {
            "id": cs["id"],
            "client_id": cs.get("profile_id"),
            "place_ids": csp_by_set_id.get(cs["id"], []),
            "saved_investigation_id": None,
            "notes": comparison_set_note_by_target_id.get(cs["id"], ""),
            "schema_version": 1,
            "updated_at": None,
        }
        for cs in comp_sets
    ]

    store_saved_investigations = [
        {
            "id": ss["id"],
            "client_id": ss.get("profile_id"),
            "name": ss.get("title") or "Untitled",
            "title": ss.get("title") or "Untitled",
            "conditions": ss.get("conditions_json") or {},
            "viewport": ss.get("viewport_json") or {},
            "settings_snapshot": ss.get("settings_snapshot_json") or {},
            "updated_at": ss.get("updated_at") or ss.get("created_at"),
            "schema_version": 1,
        }
        for ss in saved_searches
    ]

    return {
        "_storage": "SUPABASE_LIVE",
        "_warning": f"Live Supabase data. account_id={account_id}",
        "storage_schema_version": 3,
        "supabase_mirror_version": 1,
        "professional_account": {
            "id": account_id,
            "display_name": account_name,
            "schema_version": 1,
            "created_at": None,
            "updated_at": None,
        },
        "user_settings": store_user_settings,
        "places": store_places,
        "birth_profiles": store_birth_profiles,
        "clients": store_clients,
        "saved_investigations": store_saved_investigations,
        "favorite_cities": store_favs,
        "comparison_sets": store_comp_sets,
        "chart_record_history": [],
        "tags": [],
        "notes": [],
    }
