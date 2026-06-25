#!/usr/bin/env python3
"""Hydrate a small smoke set of City Intelligence rows (10 cities).

Does not run the full 500-1000 city production seed. Use after migration apply.

Usage:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/seed_city_intelligence_smoke.py
  ./venv/bin/python scripts/seed_city_intelligence_smoke.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SMOKE_CITIES = [
    ("New York", "US", None),
    ("London", "GB", None),
    ("Paris", "FR", None),
    ("Tokyo", "JP", None),
    ("Singapore", "SG", None),
    ("Sydney", "AU", None),
    ("Cape Town", "ZA", None),
    ("Buenos Aires", "AR", None),
    (
        "Reykjavik",
        "IS",
        {
            "geoname_id": "3413829",
            "name": "Reykjavík",
            "lat": 64.13548,
            "lng": -21.89541,
            "pop": 118918,
            "country_code": "IS",
            "country": "Iceland",
            "admin1": "Capital Region",
            "timezone": "Atlantic/Reykjavik",
        },
    ),
    ("Denver", "US", None),
]

RESULTS_FILE = ROOT / "scripts" / ".ci_smoke_seed_results.json"


def _sb():
    import os
    from supabase import create_client

    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])


def resolve_place(sb, name: str, country_code: str, geonames_row: dict | None) -> dict | None:
    rows = (
        sb.table("places")
        .select("id,display_name,country_code")
        .ilike("display_name", f"{name}%")
        .eq("country_code", country_code)
        .limit(5)
        .execute()
        .data
    )
    if rows:
        return rows[0]
    if not geonames_row:
        return None
    from repositories.places_repository import create_place

    created = create_place(
        display_name=geonames_row["name"],
        latitude=float(geonames_row["lat"]),
        longitude=float(geonames_row["lng"]),
        provider="geonames",
        provider_place_id=str(geonames_row["geoname_id"]),
        geonames_id=str(geonames_row["geoname_id"]),
        canonical_name=geonames_row["name"],
        admin1=geonames_row.get("admin1"),
        country_code=geonames_row.get("country_code"),
        country_name=geonames_row.get("country"),
        timezone_id=geonames_row.get("timezone"),
        population=int(geonames_row.get("pop") or 0),
        source_json={"seed": "ci_smoke", "geoname_id": geonames_row["geoname_id"]},
    )
    return {"id": created["id"], "display_name": created["display_name"], "country_code": country_code}


def summarize_row(city: str, place: dict, row: dict) -> dict:
    photos = row.get("photos_json") or {}
    airports = row.get("airport_json") or {}
    fields = [
        "overview", "population", "climate", "cost", "safety", "language",
        "healthcare", "transport", "visa", "culture", "expat",
    ]
    return {
        "city": city,
        "place_id": place["id"],
        "display_name": place.get("display_name"),
        "status": row.get("status"),
        "ai_version": row.get("ai_version"),
        "generated_at": row.get("generated_at"),
        "updated_at": row.get("updated_at"),
        "overview_words": len((row.get("overview") or "").split()),
        "summary_fields": sum(1 for k in fields if (row.get(k) or "").strip()),
        "photo_keys": sorted(photos.keys()),
        "airport_keys": sorted(airports.keys()) if isinstance(airports, dict) else [],
        "airport_has_data": bool(airports),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed CI smoke cities (10)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sb = _sb()
    from city_intelligence.hydration import hydrate_city

    results: list[dict] = []
    for name, cc, geonames_row in SMOKE_CITIES:
        place = resolve_place(sb, name, cc, geonames_row)
        if not place:
            results.append({"city": name, "error": "place_not_found"})
            print(f"FAIL {name}: place_not_found")
            continue
        if args.dry_run:
            results.append({"city": name, "place_id": place["id"], "dry_run": True})
            print(f"DRY {name} -> {place['id']}")
            continue
        row = hydrate_city(place["id"], force=True)
        results.append(summarize_row(name, place, row))
        print(f"OK {name} -> {place['id'][:8]} status={row.get('status')}")

    RESULTS_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")
    ok = sum(1 for r in results if "error" not in r)
    fail = sum(1 for r in results if "error" in r)
    print(f"DONE ok={ok} fail={fail} results={RESULTS_FILE}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
