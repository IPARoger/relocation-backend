#!/usr/bin/env python3
"""Smoke: H8-1 — City Intelligence UI hydration (cache + all surfaces)."""
from __future__ import annotations

import json
import os
import re
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
SHELL = ROOT / "app_shell.html"
CI_JS = ROOT / "validation" / "mockups" / "beta" / "city_intelligence_canonical.js"
CI_CSS = ROOT / "validation" / "mockups" / "beta" / "city_intelligence_canonical.css"
V5_ADAPTER = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_adapter.js"
V5_ROUTE = ROOT / "validation" / "mockups" / "beta" / "comparison_v5_route.js"


def check(cond: bool, msg: str, failures: list[str]) -> None:
    if not cond:
        failures.append(msg)


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.5):
            return True
    except OSError:
        return False


def fetch(path: str, method: str = "GET", timeout: float = 20, *, as_text: bool = False):
    req = urllib.request.Request(f"{BASE}{path}", method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            if as_text:
                return resp.status, raw
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, {"raw": raw}
    except urllib.error.HTTPError as err:
        raw = err.read().decode()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"raw": raw}
        return err.code, payload


def smoke_static(failures: list[str]) -> int:
    checks = 0
    shell = SHELL.read_text(encoding="utf-8")
    ci_js = CI_JS.read_text(encoding="utf-8")
    adapter = V5_ADAPTER.read_text(encoding="utf-8")
    route = V5_ROUTE.read_text(encoding="utf-8")

    for path, label in [
        (CI_JS, "city_intelligence_canonical.js"),
        (CI_CSS, "city_intelligence_canonical.css"),
    ]:
        checks += 1
        check(path.exists(), f"{label} present", failures)

    checks += 1
    check("global.CityIntelligenceCanonical" in ci_js, "CityIntelligenceCanonical export", failures)
    checks += 1
    check("CI_CANONICAL" in ci_js, "CANONICAL flag in module", failures)
    checks += 1
    check("renderRelocatedBlockHtml" in ci_js, "relocated renderer", failures)
    checks += 1
    check("renderComparisonInlineCardsHtml" in ci_js, "comparison inline renderer", failures)
    checks += 1
    check("renderComparisonModalBodyHtml" in ci_js, "comparison popup renderer", failures)
    checks += 1
    check("renderFullPageHtml" in ci_js, "full page renderer", failures)
    checks += 1
    check("isRemoteLocation" in ci_js, "remote doctrine helper", failures)

    checks += 1
    check("city_intelligence_canonical.js" in shell, "app_shell loads CI module", failures)
    checks += 1
    check("city_intelligence_canonical.css" in shell, "app_shell loads CI css", failures)
    checks += 1
    check("function ciCanonicalReady()" in shell, "ciCanonicalReady helper", failures)
    checks += 1
    check("fetchCityIntelligence" in shell, "fetchCityIntelligence wired", failures)
    checks += 1
    check("CityIntelligenceCanonical.renderRelocatedBlockHtml" in shell, "relocated delegates to module", failures)
    checks += 1
    check("hydrateComparisonCityIntelligence" in shell, "comparison CI hydration", failures)
    checks += 1
    check("hydrateCityIntelligencePage" in shell, "full page hydration", failures)
    checks += 1
    check('city: screenCity' in shell, "city route screen", failures)
    checks += 1
    check("openCityIntelligenceModal" in shell, "comparison popup open", failures)

    checks += 1
    check("CityIntelligenceCanonical.renderComparisonInlineCardsHtml" in adapter, "adapter uses shared inline renderer", failures)
    checks += 1
    check("__CI_MODAL__" in route, "v5 route CI modal placeholder", failures)
    checks += 1
    check("renderComparisonModalShellHtml" in route, "v5 route modal from module", failures)

    checks += 1
    check('action === "cmp-ci-open-page"' in shell, "open full page action wired", failures)

  # No duplicate inline CI grid outside module
    inline_ci = len(re.findall(r'class="ci-list"', shell))
    checks += 1
    check(inline_ci == 0, f"shell should not inline ci-list markup (found {inline_ci})", failures)

    return checks


def smoke_unit(failures: list[str]) -> int:
    checks = 0
    from city_intelligence.providers.location import LocationProvider

    def _mock_nearest(lat, lon, limit=8):
        return [{
            "id": "mock-village",
            "display_name": "Reykjavik",
            "country_name": "Iceland",
            "country_code": "IS",
            "latitude": 64.15,
            "longitude": -21.95,
            "population": 130000,
        }]

    loc = LocationProvider(nearest_place_lookup=_mock_nearest)
    remote = loc.resolve(latitude=64.5, longitude=-21.9, place=None)
    checks += 1
    check(remote.get("is_remote") or remote.get("is_custom"), "remote location resolution", failures)
    checks += 1
    check(bool(remote.get("nearest_village") or remote.get("regional_context")), "nearest settlement for remote", failures)

    place = {
        "id": "00000000-0000-4000-8000-000000000099",
        "display_name": "Lisbon",
        "country_name": "Portugal",
        "latitude": 38.72,
        "longitude": -9.14,
        "population": 500000,
    }
    known = LocationProvider(nearest_place_lookup=lambda *a, **k: []).resolve(
        latitude=38.72, longitude=-9.14, place=place
    )
    checks += 1
    check(known.get("is_known_city") is True, "known city not renamed", failures)
    checks += 1
    check(known.get("display_name") == "Lisbon", "known city keeps display_name", failures)

    from city_intelligence.providers.photo import PhotoProvider

    photos = PhotoProvider().fetch_photos(place=place, location_context=None)
    checks += 1
    check(set(photos.keys()) == {"hero", "street", "residential", "nature", "landmark"}, "five photo categories", failures)

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

    st_js, body_js = fetch("/validation/mockups/beta/city_intelligence_canonical.js", timeout=5, as_text=True)
    checks += 1
    check(st_js == 200 and "CityIntelligenceCanonical" in (body_js or ""), f"CI canonical js route returned {st_js}", failures)

    place_id = None
    try:
        from repositories.places_repository import list_places
        rows = list_places(limit=5)
        if rows:
            place_id = rows[0]["id"]
    except Exception:
        place_id = None

    if not place_id:
        print("  HTTP layer: SKIP (Supabase unavailable for place lookup)")
        return checks

    st_ci, body = fetch(f"/city-intelligence/{place_id}")
    checks += 1
    check(st_ci == 200, f"GET /city-intelligence returned {st_ci}", failures)
    if st_ci == 200:
        checks += 1
        check(body.get("status") in ("ready", "custom"), "cache status ready/custom", failures)
        checks += 1
        check(bool(body.get("overview")), "cached overview present", failures)
        photos = body.get("photos_json") or {}
        checks += 1
        check(set(photos.keys()) >= {"hero", "street"}, "cached photos present", failures)

    return checks


def main() -> int:
    failures: list[str] = []
    total = 0
    total += smoke_static(failures)
    total += smoke_unit(failures)
    total += smoke_http(failures)

    ci0 = ROOT / "scripts" / "smoke_city_intelligence.py"
    if ci0.exists():
        proc = subprocess.run([sys.executable, str(ci0)], capture_output=True, text=True)
        out = (proc.stdout or "") + (proc.stderr or "")
        line = out.strip().splitlines()[-1] if out.strip() else ""
        if proc.returncode != 0:
            failures.append(f"smoke_city_intelligence.py: {line or proc.returncode}")
        else:
            print(f"  smoke_city_intelligence.py: {line}")

    if failures:
        print(f"FAIL {len(failures)}/{total}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {total}/{total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
