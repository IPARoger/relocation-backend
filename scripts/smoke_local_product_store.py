#!/usr/bin/env python3
"""Phase 3.0b — local product store smoke (file-only, no HTTP).

Proves:
  * client + birth profile + place creation
  * saved investigation with settings_snapshot round-trip
  * favorite city persistence
  * comparison set (2–5 places, one Chart Record)
  * chart record history placeholder
  * default_chart_record_id
  * atomic save/load
  * validation + forbidden-key rejection
  * one birth_profile per client enforcement
  * committed scaffold seed (3 Chart Records, shell ID parity)

Run:
  ./venv/bin/python scripts/smoke_local_product_store.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from local_product_store import (  # noqa: E402
    DEFAULT_STORE_PATH,
    add_favorite_city,
    append_chart_record_history,
    create_client,
    create_comparison_set,
    create_place,
    empty_store,
    get_default_chart_record_id,
    load,
    save,
    save_investigation,
    set_default_chart_record_id,
    validate_store,
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="smoke_product_store_") as tmp:
        store_path = Path(tmp) / "TEMPORARY_product_store.json"
        state = empty_store()

        client = create_client(
            state,
            display_name="Smoke Client",
            birth_date="1990-05-15",
            birth_time="12:00",
            timezone_id="UTC",
            birth_place={
                "display_name": "Smoke City",
                "lat": 40.0,
                "lon": -100.0,
                "external_source": "manual",
            },
            confidence_tier="T0",
            record_type="client",
            notes="client note",
            tags=["relocation"],
        )

        set_default_chart_record_id(state, client["id"])

        investigation = save_investigation(
            state,
            client_id=client["id"],
            title="Smoke investigation",
            name="Smoke investigation",
            notes="exploration note",
            conditions={
                "schema_version": 1,
                "kind": "saved_investigation",
                "house_conditions": [
                    {"slot": "A", "type": "planet_in_house", "planet": "moon", "house": 4}
                ],
                "angle_sign_conditions": [],
                "aspect_overlay": None,
            },
            viewport={
                "north": 81.0,
                "south": -72.0,
                "east": 127.0,
                "west": -127.0,
                "zoom": 2.0,
                "center_lat": 20.0,
                "center_lon": 0.0,
            },
        )

        if not isinstance(investigation.get("settings_snapshot"), dict):
            fail("settings_snapshot missing after save_investigation")
        if investigation.get("originating_chart_record_id") != client["id"]:
            fail("originating_chart_record_id must match client_id")

        birth_place_id = state["birth_profiles"][0]["birth_place_id"]
        favorite = add_favorite_city(
            state,
            client_id=client["id"],
            place_id=birth_place_id,
            notes="favorite note",
            saved_investigation_id=investigation["id"],
        )

        p2 = create_place(
            state,
            display_name="Smoke City B",
            lat=41.0,
            lon=-101.0,
        )
        create_comparison_set(
            state,
            client_id=client["id"],
            place_ids=[birth_place_id, p2["id"]],
        )

        append_chart_record_history(
            state,
            client_id=client["id"],
            event_type="map_search",
            payload={"smoke": True},
            saved_investigation_id=investigation["id"],
        )

        pre_errors = validate_store(state)
        if pre_errors:
            fail(f"pre-save validation: {pre_errors}")

        save(state, store_path)
        if not store_path.exists():
            fail("store file not written")

        reloaded = load(store_path)
        reload_errors = validate_store(reloaded)
        if reload_errors:
            fail(f"post-load validation: {reload_errors}")

        if reloaded.get("_storage") != "TEMPORARY_LOCAL_SCAFFOLD":
            fail("_storage marker missing after reload")

        if reloaded.get("storage_schema_version") != 3:
            fail("expected storage_schema_version 3 after reload")

        if get_default_chart_record_id(reloaded) != client["id"]:
            fail("default_chart_record_id not persisted")

        if len(reloaded.get("clients") or []) != 1:
            fail("expected 1 client after reload")
        if len(reloaded.get("saved_investigations") or []) != 1:
            fail("expected 1 investigation after reload")
        if len(reloaded.get("favorite_cities") or []) != 1:
            fail("expected 1 favorite after reload")
        if len(reloaded.get("comparison_sets") or []) != 1:
            fail("expected 1 comparison_set after reload")
        if len(reloaded.get("chart_record_history") or []) != 1:
            fail("expected 1 history row after reload")

        inv = reloaded["saved_investigations"][0]
        if "settings_snapshot" not in inv or not inv["settings_snapshot"]:
            fail("settings_snapshot not persisted")

        if inv["client_id"] != client["id"]:
            fail("client_id mismatch after reload")
        if favorite["id"] != reloaded["favorite_cities"][0]["id"]:
            fail("favorite id mismatch after reload")

        dup_state = json.loads(json.dumps(reloaded))
        dup_state["clients"].append(
            {
                "id": "client_dup",
                "display_name": "Dup",
                "birth_profile_id": dup_state["clients"][0]["birth_profile_id"],
                "record_type": "client",
                "notes": "",
                "tags": [],
                "schema_version": 1,
            }
        )
        dup_errors = validate_store(dup_state)
        if not any("birth_profile_id reused" in e for e in dup_errors):
            fail("expected duplicate birth_profile validation error")

        bad_state = json.loads(json.dumps(reloaded))
        bad_state["saved_investigations"][0]["conditions"]["geojson"] = {"type": "Feature"}
        bad_errors = validate_store(bad_state)
        if not any("forbidden key" in e for e in bad_errors):
            fail("expected forbidden geojson key error")

        missing_snapshot = json.loads(json.dumps(reloaded))
        del missing_snapshot["saved_investigations"][0]["settings_snapshot"]
        miss_errors = validate_store(missing_snapshot)
        if not any("settings_snapshot" in e for e in miss_errors):
            fail("expected missing settings_snapshot error")

        bad_cmp = json.loads(json.dumps(reloaded))
        bad_cmp["comparison_sets"].append(
            {
                "id": "cmp_bad",
                "client_id": client["id"],
                "place_ids": [birth_place_id],
                "schema_version": 1,
            }
        )
        cmp_errors = validate_store(bad_cmp)
        if not any("2–5 place_ids" in e for e in cmp_errors):
            fail("expected comparison set place count error")

    if not DEFAULT_STORE_PATH.exists():
        fail(f"committed scaffold missing: {DEFAULT_STORE_PATH}")

    seed = load(DEFAULT_STORE_PATH)
    seed_errors = validate_store(seed)
    if seed_errors:
        fail(f"committed scaffold invalid: {seed_errors}")

    if len(seed.get("clients") or []) != 3:
        fail("scaffold must contain 3 Chart Records")
    expected_ids = {"cr-anna-rivera", "cr-jordan-lee", "cr-research-event"}
    actual_ids = {c["id"] for c in seed["clients"]}
    if actual_ids != expected_ids:
        fail(f"scaffold Chart Record IDs mismatch: {actual_ids}")

    if get_default_chart_record_id(seed) != "cr-anna-rivera":
        fail("scaffold default_chart_record_id must be cr-anna-rivera")

    jordan_bp = next(bp for bp in seed["birth_profiles"] if bp["id"] == "bp_jordan")
    meta = jordan_bp.get("confidence_metadata") or {}
    if "9:47 AM" not in meta.get("time_range_display", ""):
        fail("Jordan confidence_metadata time_range_display missing")

    cmp_sets = seed.get("comparison_sets") or []
    if not cmp_sets:
        fail("scaffold must contain at least one comparison_set")
    if not (2 <= len(cmp_sets[0]["place_ids"]) <= 5):
        fail("scaffold comparison_set must have 2–5 places")

    print("PASS: smoke_local_product_store")
    print("  round-trip: client + investigation + favorite + comparison + history")
    print("  settings_snapshot: persisted")
    print("  default_chart_record_id: persisted")
    print("  one birth_profile per client: enforced")
    print("  forbidden keys: rejected")
    print("  committed scaffold: 3 Chart Records + shell ID parity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
