#!/usr/bin/env python3
"""Static smoke for BI-0C — auth + birth intake instrument family."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "auth.html"
INTAKE = ROOT / "first_profile_intake.js"
FAMILY = ROOT / "theme/family_resemblance.css"


def check(label: str, ok: bool, failures: list[str]) -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    if not AUTH.is_file() or not INTAKE.is_file() or not FAMILY.is_file():
        print("ABORT: missing auth.html, first_profile_intake.js, or family_resemblance.css", file=sys.stderr)
        return 1

    auth = AUTH.read_text(encoding="utf-8")
    intake = INTAKE.read_text(encoding="utf-8")

    check("auth: links family_resemblance.css", "family_resemblance.css" in auth, failures)
    check("auth: body rm-instrument-surface", 'class="rm-instrument-surface"' in auth or "rm-instrument-surface" in auth, failures)
    check("auth: sage accent (not blue SaaS primary)", "#1d4ed8" not in auth and "var(--rm-accent" in auth, failures)
    check("auth: no gray SaaS ground", "#f0f4f8" not in auth and "#f3f4f6" not in auth, failures)
    check("auth: serif wordmark", "var(--rm-serif)" in auth, failures)
    check("auth: OAuth DOM preserved", 'id="google-signup-btn"' in auth and "signInWithOAuth" in auth, failures)
    check("auth: data-view signup/login/confirm", all(v in auth for v in ('data-view="signup"', 'data-view="login"', 'data-view="confirm"')), failures)

    check("intake: instrument tokens (no purple dev overlay)", "#7b61ff" not in intake and "#1a1a2e" not in intake, failures)
    check("intake: family_resemblance.css injected", "family_resemblance.css" in intake, failures)
    check("intake: rm-sls-* place search", "rm-sls-wrap" in intake and "rm-sls-item" in intake, failures)
    check("intake: no Unknown time UI", "rm-mode-unknown" not in intake and 'data-mode="unknown"' not in intake, failures)
    check("intake: birth_time_mode always exact", 'birth_time_mode: "exact"' in intake, failures)
    check("intake: no unknown mode branch in submit", "birthTimeMode" not in intake, failures)

    # Beta first-run: hidden display name; visible label only in add-mode branch
    build = intake.split("function buildOverlay", 1)[1].split("function attachListeners", 1)[0]
    check("intake: hidden name field for first-run", 'type="hidden" id="rm-intake-name"' in build, failures)
    check(
        "intake: Display name label gated to add mode only",
        'launchContext.mode === "add"' in build and build.index('Display name') > build.index('launchContext.mode === "add"'),
        failures,
    )
    check("intake: resolveDisplayName fallback", "My Profile" in intake and "resolveDisplayName" in intake, failures)
    check("intake: RMPlaceSearch preserved", "RMPlaceSearch" in intake, failures)
    check("intake: create-with-birth endpoint", "/profiles/create-with-birth" in intake, failures)
    check("intake: direct map redirect on success", "map_CURRENT.html?skipOnboarding=1" in intake, failures)

    total = 20
    passed = total - len(failures)
    print(f"\n{passed}/{total} PASS")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
