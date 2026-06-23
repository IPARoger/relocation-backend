#!/usr/bin/env python3
"""Static smoke: Google OAuth v1 wiring in auth.html only.

Verifies structural evidence for Google sign-in without requiring a live server,
Supabase dashboard config, or browser OAuth flow.

Run:
    venv/bin/python scripts/smoke_google_oauth.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "auth.html"


def check(label: str, result: bool) -> bool:
    print(f"  {'PASS' if result else 'FAIL'}  {label}")
    return result


def main() -> int:
    if not AUTH.exists():
        print(f"ABORT: {AUTH} not found", file=sys.stderr)
        return 1

    html = AUTH.read_text(encoding="utf-8")
    results: list[bool] = []

    print("\nGoogle OAuth UI (auth.html):")
    results.append(check("signup Google button #google-signup-btn", 'id="google-signup-btn"' in html))
    results.append(check("login Google button #google-login-btn", 'id="google-login-btn"' in html))
    results.append(check('button label "Continue with Google"', "Continue with Google" in html))
    results.append(check("oauth divider present", 'class="oauth-divider"' in html))
    results.append(check(".btn-oauth CSS present", ".btn-oauth" in html))

    print("\nOAuth redirect and provider:")
    results.append(check("OAUTH_REDIRECT uses /auth.html", 'OAUTH_REDIRECT = window.location.origin + "/auth.html"' in html))
    results.append(check("signInWithOAuth present", "signInWithOAuth" in html))
    results.append(check('provider: "google"', 'provider: "google"' in html))
    results.append(check("redirectTo: OAUTH_REDIRECT", "redirectTo: OAUTH_REDIRECT" in html))

    print("\nCallback and error handling:")
    results.append(check("parseOAuthUrlError function", "function parseOAuthUrlError" in html))
    results.append(check("stripOAuthParams function", "function stripOAuthParams" in html))
    results.append(check("access_denied cancelled message", "Sign-in was cancelled." in html))
    results.append(check("init calls stripOAuthParams after getSession", "stripOAuthParams();" in html))
    results.append(check("history.replaceState strips query", "history.replaceState(null, \"\", window.location.pathname)" in html))

    print("\nScope guards:")
    results.append(check("no Apple provider", 'provider: "apple"' not in html))
    results.append(check("no signInWithOAuth apple", "signInWithApple" not in html))

    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} PASS")
    if passed < total:
        print(f"FAILED: {total - passed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
