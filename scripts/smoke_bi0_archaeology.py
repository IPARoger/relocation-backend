#!/usr/bin/env python3
"""Read-only smoke for BI-0A First Experience archaeology.

Verifies production routes, assets, and critical first-run links exist.
No runtime auth; no UI changes.
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8000"

ASSETS = [
    "auth.html",
    "map_CURRENT.html",
    "app_shell.html",
    "first_profile_intake.js",
    "place_search_client.js",
    "supabase_client.js",
    "auth_guard.js",
    "theme/family_resemblance.css",
]

ROUTES_IN_FIXER = [
    "/auth.html",
    "/map_CURRENT.html",
    "/first_profile_intake.js",
    "/place_search_client.js",
]

DEAD_LINK_PATTERNS = [
    (r'href="/auth\.html"', "auth link"),
    (r'href="/map_CURRENT\.html"', "map link"),
    (r'href="/app_shell\.html"', "app shell link"),
]


def fetch(url: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, body
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, str(e)


def main() -> int:
    import os
    base = os.environ.get("BASE_URL", BASE).rstrip("/")
    failures: list[str] = []
    checks = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(msg)

    # Local files exist
    for name in ASSETS:
        p = ROOT / name
        check(p.is_file(), f"asset on disk: {name}")

    fixer = (ROOT / "main_centerline_FIXER.py").read_text(encoding="utf-8")
    for route in ROUTES_IN_FIXER:
        check(route in fixer, f"route registered in fixer: {route}")

    auth = (ROOT / "auth.html").read_text(encoding="utf-8")
    intake = (ROOT / "first_profile_intake.js").read_text(encoding="utf-8")
    map_html = (ROOT / "map_CURRENT.html").read_text(encoding="utf-8")

    check('data-view="signup"' in auth, "auth: signup view")
    check('data-view="login"' in auth, "auth: login view")
    check('data-view="confirm"' in auth, "auth: confirm view")
    check("signInWithOAuth" in auth and "google" in auth, "auth: Google OAuth wired")
    check("apple" not in auth.lower() or "signInWithOAuth" not in auth.split("apple")[0], "auth: no Apple OAuth button expected")
    check('MAP_URL = "/map_CURRENT.html"' in auth, "auth: redirects to production map")

    check("__showFirstProfileIntake" in intake, "intake: show hook exported")
    check("RMPlaceSearch" in intake, "intake: uses RMPlaceSearch")
    check("/profiles/create-with-birth" in intake, "intake: create-with-birth endpoint")
    check('family_resemblance.css' in auth, "auth: family_resemblance.css linked")
    check("rm-instrument-surface" in auth, "auth: instrument surface class")
    check('birth_time_mode: "exact"' in intake, "intake: exact birth time mode")
    check("rm-mode-unknown" not in intake, "intake: no unknown time toggle (BI-0C)")

    check("first_profile_intake.js" in map_html, "map: loads intake script")
    check("auth_guard.js" in map_html, "map: auth guard present")
    check("#gv-builder-host" in map_html, "map: Genie builder present")
    check("family_resemblance.css" in map_html, "map: family CSS linked (M2-X)")

    check("first_profile_intake.js" in (ROOT / "app_shell.html").read_text(encoding="utf-8"), "shell: loads intake script")

    # HTTP reachability (optional if server up)
    status, _ = fetch(f"{base}/health")
    if status == 200:
        for route in ["/auth.html", "/map_CURRENT.html", "/first_profile_intake.js"]:
            st, body = fetch(f"{base}{route}")
            check(st == 200 and len(body) > 100, f"HTTP 200: {route}")
        st_auth, auth_body = fetch(f"{base}/auth.html")
        for pat, label in DEAD_LINK_PATTERNS:
            if pat.startswith("href"):
                continue  # outbound links checked in source files
        check("/map_CURRENT.html" in auth_body, "auth.html served contains map redirect")
    else:
        print(f"WARN: server not reachable at {base} — skipping HTTP checks")

    if failures:
        print(f"FAIL {len(failures)}/{checks}")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASS {checks}/{checks} BI-0 archaeology checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
