#!/usr/bin/env python3
"""Smoke: CI-0 City Intelligence foundation.

Layers:
  1. Static — migration, module imports, provider contracts
  2. Unit — stub AI word counts, photo categories, location resolution
  3. HTTP — GET/POST against running server (skipped if down or no Supabase)

Run:
  ./venv/bin/python scripts/smoke_city_intelligence.py
  BASE=http://127.0.0.1:8004 ./venv/bin/python scripts/smoke_city_intelligence.py
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PORT = int(os.environ.get("PORT", "8004"))
BASE = os.environ.get("BASE", f"http://127.0.0.1:{PORT}")
_MIGRATION_CANDIDATES = (
    ROOT / "supabase" / "migrations" / "20260626154900_city_intelligence.sql",
    ROOT / "supabase" / "migrations" / "2026_06_26_city_intelligence.sql",
)
MIGRATION = next((m for m in _MIGRATION_CANDIDATES if m.exists()), _MIGRATION_CANDIDATES[-1])


def check(cond: bool, msg: str, failures: list[str]) -> None:
    if not cond:
        failures.append(msg)


def word_count(text: str) -> int:
    return len((text or "").split())


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.5):
            return True
    except OSError:
        return False


def fetch(path: str, method: str = "GET", body: dict | None = None, timeout: float = 20):
    data = json.dumps(body).encode() if body is not None else None
    headers = {}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as err:
        raw = err.read().decode()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"raw": raw}
        return err.code, payload


def smoke_static(failures: list[str]) -> int:
    checks = 0
    checks += 1
    check(MIGRATION.exists(), "migration file missing", failures)
    if MIGRATION.exists():
        sql = MIGRATION.read_text(encoding="utf-8")
        checks += 1
        check("city_intelligence" in sql and "city_id uuid primary key" in sql, "migration DDL incomplete", failures)

    try:
        from city_intelligence.providers import (
            AiSummaryProvider,
            AirportProvider,
            LocationProvider,
            PhotoProvider,
        )
        from city_intelligence.service import enqueue_background_hydration, get_or_hydrate
        from repositories import city_intelligence_repository
        checks += 1
        check(True, "", failures)
    except Exception as exc:  # noqa: BLE001
        checks += 1
        check(False, f"import failed: {exc}", failures)

    return checks


def smoke_unit(failures: list[str]) -> int:
    checks = 0
    place = {
        "id": "00000000-0000-4000-8000-000000000099",
        "display_name": "Lisbon",
        "country_name": "Portugal",
        "country_code": "PT",
        "latitude": 38.72,
        "longitude": -9.14,
        "population": 500000,
    }

    from city_intelligence.providers.ai_summary import AiSummaryProvider
    from city_intelligence.providers.photo import PhotoProvider
    from city_intelligence.providers.location import LocationProvider

    ai = AiSummaryProvider()
    summaries = ai.generate_summaries(place=place, location_context=None, airports={}, photos={})
    checks += 1
    check(set(summaries.keys()) >= {"overview", "climate", "expat"}, "AI fields incomplete", failures)
    for field, text in summaries.items():
        wc = word_count(text)
        checks += 1
        check(40 <= wc <= 120, f"AI field {field} word count {wc} outside ~50-80 band", failures)

    photos = PhotoProvider().fetch_photos(place=place, location_context=None)
    checks += 1
    check(set(photos.keys()) == {"hero", "street", "residential", "nature", "landmark"}, "photo categories wrong", failures)
    checks += 1
    check(all(str(v).startswith("http") for v in photos.values()), "photo URLs invalid", failures)

    loc = LocationProvider(nearest_place_lookup=lambda *a, **k: [])
    custom = loc.resolve(latitude=64.5, longitude=-21.9, place=None)
    checks += 1
    check(custom.get("is_custom") or custom.get("is_remote"), "custom/remote resolution failed", failures)
    checks += 1
    check(bool(custom.get("suggested_name")), "custom suggested_name missing", failures)

    known = LocationProvider(nearest_place_lookup=lambda *a, **k: []).resolve(
        latitude=38.72, longitude=-9.14, place=place
    )
    checks += 1
    check(known.get("is_known_city") is True, "known city should not get custom name", failures)

    return checks


def smoke_http(failures: list[str]) -> int:
    checks = 0
    host = BASE.split("://", 1)[-1].split(":")[0]
    if not port_open(host, PORT):
        print(f"  HTTP layer: SKIP (no server on {BASE})")
        return 0

    st, _ = fetch("/health", timeout=3)
    checks += 1
    check(st == 200, f"/health returned {st}", failures)

    # Use first place from DB if available
    place_id = None
    try:
        from repositories.places_repository import list_places
        rows = list_places(limit=1)
        if rows:
            place_id = rows[0]["id"]
    except Exception:
        place_id = None

    if not place_id:
        print("  HTTP layer: SKIP (Supabase unavailable for place lookup)")
        return checks

    st, body = fetch(f"/city-intelligence/{place_id}")
    checks += 1
    check(st == 200, f"GET /city-intelligence returned {st}: {body}", failures)
    if st == 200:
        checks += 1
        check(body.get("status") in ("ready", "custom"), "GET status not ready/custom", failures)
        checks += 1
        check(bool(body.get("overview")), "GET missing overview", failures)

    st2, body2 = fetch(f"/city-intelligence/hydrate/{place_id}", method="POST")
    checks += 1
    check(st2 == 200, f"POST hydrate returned {st2}: {body2}", failures)

    return checks


def main() -> int:
    failures: list[str] = []
    total = 0
    total += smoke_static(failures)
    total += smoke_unit(failures)
    total += smoke_http(failures)

    if failures:
        print(f"FAIL {len(failures)}/{total}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {total}/{total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
