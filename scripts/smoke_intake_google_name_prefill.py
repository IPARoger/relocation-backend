#!/usr/bin/env python3
"""Static smoke: Google OAuth name prefill in first_profile_intake.js.

Run:
    venv/bin/python scripts/smoke_intake_google_name_prefill.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "first_profile_intake.js"


def check(label: str, ok: bool) -> bool:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    return ok


def main() -> int:
    if not INTAKE.exists():
        print(f"ABORT: {INTAKE} not found", file=sys.stderr)
        return 1

    js = INTAKE.read_text(encoding="utf-8")
    results = [
        check("prefillNameFromGoogleMetadata defined", "function prefillNameFromGoogleMetadata" in js),
        check("called from showOverlay", "prefillNameFromGoogleMetadata();" in js),
        check("userSignedInWithGoogle gate", "function userSignedInWithGoogle" in js),
        check('checks provider === "google"', 'provider === "google"' in js),
        check("uses user_metadata.full_name", "meta.full_name" in js),
        check("fallback user_metadata.name", "meta.name" in js),
        check("only fills empty rm-intake-name", 'getElementById("rm-intake-name")' in js and "!String(nameInput.value" in js),
        check("no email prefill", "user.email" not in js or js.count("user.email") == 0),
        check("no accounts.name write", "accounts.name" not in js),
    ]
  # email might appear elsewhere - grep more carefully
    email_prefill = 'nameInput.value =' in js and 'user.email' in js
    if email_prefill:
        results.append(check("no email written to name input", False))
    else:
        results.append(check("no email written to name input", True))

    passed = sum(results)
    print(f"\n{passed}/{len(results)} PASS")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
