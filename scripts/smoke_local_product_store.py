#!/usr/bin/env python3
"""Phase 3.0a — local product store smoke (file-only, no HTTP).

Proves:
  * client + birth profile + place creation
  * saved investigation with settings_snapshot round-trip
  * favorite city persistence
  * atomic save/load
  * validation + forbidden-key rejection
  * one birth_profile per client enforcement

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
    add_favorite_city,
    create_client,
    empty_store,
    load,
    save,
    save_investigation,
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
            notes="client note",
            tags=["relocation"],
        )

        investigation = save_investigation(
            state,
            client_id=client["id"],
            title="Smoke investigation",
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

        birth_place_id = state["birth_profiles"][0]["birth_place_id"]
        favorite = add_favorite_city(
            state,
            client_id=client["id"],
            place_id=birth_place_id,
            notes="favorite note",
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

        if len(reloaded.get("clients") or []) != 1:
            fail("expected 1 client after reload")
        if len(reloaded.get("saved_investigations") or []) != 1:
            fail("expected 1 investigation after reload")
        if len(reloaded.get("favorite_cities") or []) != 1:
            fail("expected 1 favorite after reload")

        inv = reloaded["saved_investigations"][0]
        if "settings_snapshot" not in inv or not inv["settings_snapshot"]:
            fail("settings_snapshot not persisted")

        if inv["client_id"] != client["id"]:
            fail("client_id mismatch after reload")
        if favorite["id"] != reloaded["favorite_cities"][0]["id"]:
            fail("favorite id mismatch after reload")

        # Duplicate birth_profile across clients must fail validation.
        dup_state = json.loads(json.dumps(reloaded))
        dup_state["clients"].append(
            {
                "id": "client_dup",
                "display_name": "Dup",
                "birth_profile_id": dup_state["clients"][0]["birth_profile_id"],
                "notes": "",
                "tags": [],
                "schema_version": 1,
            }
        )
        dup_errors = validate_store(dup_state)
        if not any("birth_profile_id reused" in e for e in dup_errors):
            fail("expected duplicate birth_profile validation error")

        # Forbidden renderer key must fail validation.
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

    print("PASS: smoke_local_product_store")
    print("  round-trip: client + investigation + favorite")
    print("  settings_snapshot: persisted")
    print("  one birth_profile per client: enforced")
    print("  forbidden keys: rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
