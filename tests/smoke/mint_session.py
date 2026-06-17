#!/usr/bin/env python3
"""Mint Supabase browser session + first active profile id for Playwright smokes."""

from __future__ import annotations

import json
import os
import sys
from urllib.parse import urlparse


def fail(msg: str) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")

    from supabase import create_client

    email = os.environ.get("RM_SMOKE_EMAIL", "davidleongoodman@gmail.com").strip()
    anon_client = create_client(url, anon_key)
    admin = create_client(url, service_key)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp(
        {"token_hash": link.properties.hashed_token, "type": "magiclink"}
    )
    if not res.session:
        fail(f"could not authenticate {email}")

    ref = urlparse(url).hostname.split(".")[0]
    s = res.session
    storage_key = f"sb-{ref}-auth-token"
    storage_val = json.dumps(
        {
            "access_token": s.access_token,
            "refresh_token": s.refresh_token,
            "expires_at": s.expires_at,
            "expires_in": s.expires_in,
            "token_type": s.token_type or "bearer",
            "user": json.loads(res.user.model_dump_json()),
        }
    )

    token = s.access_token
    anon_client.postgrest.auth(token)
    account_ids = anon_client.rpc("app_account_ids").execute().data or []
    profile_id = None
    if account_ids:
        profiles = (
            admin.table("profiles")
            .select("id")
            .eq("account_id", account_ids[0])
            .is_("archived_at", "null")
            .order("created_at")
            .limit(1)
            .execute()
        ).data or []
        if profiles:
            profile_id = profiles[0]["id"]

    print(
        json.dumps(
            {
                "access_token": token,
                "storage_key": storage_key,
                "storage_val": storage_val,
                "profile_id": profile_id,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
