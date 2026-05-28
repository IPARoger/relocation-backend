#!/usr/bin/env python3
"""Validate a local product store JSON file (Phase 3.0a).

Run:
  ./venv/bin/python scripts/validate_local_product_store.py [path]

Exit 0 when valid; exit 1 with errors printed to stderr.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from local_product_store import (  # noqa: E402
    DEFAULT_STORE_PATH,
    validate_store,
)

FORBIDDEN_FIXTURE = {
    "conditions": {"geojson": {}, "kind": "saved_investigation"},
    "settings_snapshot": {"house_system": "placidus"},
}


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_STORE_PATH

    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    with open(path, "r", encoding="utf-8") as fh:
        state = json.load(fh)

    errors = validate_store(state)
    if errors:
        print(f"INVALID ({len(errors)} errors): {path}", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: {path}")
    print(f"  clients={len(state.get('clients') or [])}")
    print(f"  saved_investigations={len(state.get('saved_investigations') or [])}")
    print(f"  favorite_cities={len(state.get('favorite_cities') or [])}")

    # Self-check: forbidden-key detector must catch renderer artifacts.
    probe = {
        "_storage": "TEMPORARY_LOCAL_SCAFFOLD",
        "storage_schema_version": 2,
        "professional_account": {},
        "user_settings": {},
        "places": [],
        "birth_profiles": [],
        "clients": [{"id": "c1", "birth_profile_id": "bp1"}],
        "saved_investigations": [
            {
                "id": "inv1",
                "settings_snapshot": FORBIDDEN_FIXTURE["settings_snapshot"],
                "conditions": FORBIDDEN_FIXTURE["conditions"],
            }
        ],
        "favorite_cities": [],
        "tags": [],
        "notes": [],
    }
    probe_errors = validate_store(probe)
    if not any("forbidden key" in e for e in probe_errors):
        print("error: forbidden-key self-check failed", file=sys.stderr)
        return 1

    print("  forbidden-key self-check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
