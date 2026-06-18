#!/usr/bin/env python3
"""Smoke: alias-aware place search via GET /places/search (A3 GeoNames).

Validates 29 launch-critical queries from results/88_a3_geonames_alternate_names_strategy.md.
Top result must match expected canonical_name + country_name.

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_place_alias_search.py
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "venv" / "bin" / "python"
PORT = 8004

# (query, expected canonical_name, expected country_name)
CASES = [
    ("NYC", "New York City", "United States"),
    ("New York", "New York City", "United States"),
    ("Bombay", "Mumbai", "India"),
    ("Mumbai", "Mumbai", "India"),
    ("Madras", "Chennai", "India"),
    ("Chennai", "Chennai", "India"),
    ("Calcutta", "Kolkata", "India"),
    ("Kolkata", "Kolkata", "India"),
    ("Cochin", "Kochi", "India"),
    ("Kochi", "Kochi", "India"),
    ("Praha", "Prague", "Czechia"),
    ("Prague", "Prague", "Czechia"),
    ("Köln", "Köln", "Germany"),
    ("Cologne", "Köln", "Germany"),
    ("Koeln", "Köln", "Germany"),
    ("Kiev", "Kyiv", "Ukraine"),
    ("Kyiv", "Kyiv", "Ukraine"),
    ("Peking", "Beijing", "China"),
    ("Beijing", "Beijing", "China"),
    ("Firenze", "Florence", "Italy"),
    ("Florence", "Florence", "Italy"),
    ("Roma", "Rome", "Italy"),
    ("Rome", "Rome", "Italy"),
    ("Moskva", "Moscow", "Russia"),
    ("Moscow", "Moscow", "Russia"),
    ("Lisboa", "Lisbon", "Portugal"),
    ("Lisbon", "Lisbon", "Portugal"),
    ("Wien", "Vienna", "Austria"),
    ("Vienna", "Vienna", "Austria"),
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) != 0


def wait_health(base: str, timeout_s: float = 25.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base + "/health", timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def search(base: str, q: str | None = None, geonames_id: str | None = None, limit: int = 1):
    params = []
    if q:
        params.append("q=" + urllib.parse.quote(q))
    if geonames_id:
        params.append("geonames_id=" + urllib.parse.quote(geonames_id))
    params.append(f"limit={limit}")
    url = f"{base}/places/search?{'&'.join(params)}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.load(resp)


def main() -> int:
    base = f"http://127.0.0.1:{PORT}"
    proc = None
    try:
        urllib.request.urlopen(base + "/health", timeout=2)
    except Exception:
        if not port_free(PORT):
            fail(f"port {PORT} occupied but /health unreachable")
        proc = subprocess.Popen(
            [
                str(PYTHON),
                "-m",
                "uvicorn",
                "main_centerline_FIXER:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(PORT),
            ],
            cwd=str(ROOT),
            env=dict(os.environ),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if not wait_health(base):
            proc.terminate()
            fail(f"temp server did not start on {base}")

    results = []
    try:
        for query, exp_canon, exp_country in CASES:
            try:
                rows = search(base, q=query, limit=1)
            except urllib.error.HTTPError as err:
                results.append((query, False, f"HTTP {err.code}"))
                continue
            if not rows:
                results.append((query, False, "no results"))
                continue
            top = rows[0]
            ok = top.get("canonical_name") == exp_canon and top.get("country_name") == exp_country
            if ok:
                results.append((query, True, f"{exp_canon}, {exp_country}"))
            else:
                got = f"{top.get('canonical_name')}, {top.get('country_name')}"
                results.append((query, False, f"got {got}, expected {exp_canon}, {exp_country}"))

        gid_rows = search(base, geonames_id="1275339", limit=1)
        gid_ok = bool(gid_rows) and gid_rows[0].get("canonical_name") == "Mumbai"
        results.append(("geonames_id=1275339", gid_ok, gid_rows[0].get("canonical_name") if gid_rows else "none"))

        try:
            urllib.request.urlopen(f"{base}/places/search", timeout=10)
            results.append(("missing_query_422", False, "expected 422"))
        except urllib.error.HTTPError as err:
            results.append(("missing_query_422", err.code == 422, f"status={err.code}"))

        passed = sum(1 for _, ok, _ in results if ok)
        total = len(results)
        for name, ok, detail in results:
            print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")

        print(f"\n{passed}/{total} passed")
        return 0 if passed == total else 1
    finally:
        if proc:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
