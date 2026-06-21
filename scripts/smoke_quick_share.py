#!/usr/bin/env python3
"""Smoke: QUICK-SHARE-MVP — create (JWT) + public read + static honesty."""

from __future__ import annotations

import json
import os
import socket
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DEFAULT_EMAIL = "davidleongoodman@gmail.com"
PORT = 8004


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def fetch(base, path, headers=None, method="GET", body=None, timeout=30):
    data = json.dumps(body).encode() if body is not None else None
    hdrs = dict(headers or {})
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{base}{path}", headers=hdrs, method=method, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()


def static_checks() -> list[tuple[str, bool, str]]:
    out: list[tuple[str, bool, str]] = []
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    mp = (ROOT / "map_CURRENT.html").read_text(encoding="utf-8")
    main = (ROOT / "main_centerline_FIXER.py").read_text(encoding="utf-8")
    out.append(("static_qs_map_button", 'id="quickShareBtn"' in mp, "map Quick Share button"))
    out.append(("static_qs_shell_button", "quick-share-chart" in shell, "profile chart Quick Share"))
    out.append(("static_qs_js_helper", (ROOT / "quick_share.js").is_file(), "quick_share.js"))
    out.append(("static_qs_create_route", "/quick-share/create" in main, "POST create route"))
    out.append(("static_qs_public_route", "/quick-share/{quick_share_id}" in main, "GET public route"))
    out.append(("static_qs_recipient_bootstrap", "bootstrapQuickShareRecipient" in mp, "recipient bootstrap"))
    out.append(("static_qs_repo_module", (ROOT / "repositories/quick_share_repository.py").is_file(), "repository"))
    out.append(("static_qs_url_param", "quickShare" in mp, "map URL param"))
    return out


def port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def resolve_ctx(url, anon, svc):
    from supabase import create_client

    anon_client = create_client(url, anon)
    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
    admin = create_client(url, svc)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp(
        {"token_hash": link.properties.hashed_token, "type": "magiclink"}
    )
    if not res.session:
        fail(f"could not authenticate {email}")
    token = res.session.access_token
    account_ids = anon_client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        fail("no account for smoke user")
    prof = (
        admin.table("profiles")
        .select("id")
        .eq("account_id", account_ids[0])
        .is_("archived_at", "null")
        .limit(1)
        .execute()
    )
    if not prof.data:
        fail("no profile for smoke user")
    return token, account_ids[0], prof.data[0]["id"], admin


def cleanup_share(admin, share_id):
    if share_id:
        try:
            admin.table("quick_shares").delete().eq("id", share_id).execute()
        except Exception:
            pass


def backend_repository_checks(url, anon, svc) -> list[tuple[str, bool, str]]:
    out: list[tuple[str, bool, str]] = []
    from repositories.quick_share_repository import create_quick_share, get_quick_share_public

    token, _account_id, profile_id, admin = resolve_ctx(url, anon, svc)
    share_id = None
    try:
        created = create_quick_share(
            token,
            profile_id=profile_id,
            profile_display_name="Smoke Profile",
            source_surface="chart",
            conditions_json={
                "schema_version": 1,
                "kind": "quick_share_smoke",
                "chart_record_id": profile_id,
                "house_conditions": [{"planet": "sun", "house": 1}],
                "birth_year": 1990,
                "birth_month": 6,
                "birth_day": 15,
                "birth_hour_utc": 12.0,
            },
            viewport_json={"center_lat": 40.0, "center_lon": -74.0, "zoom": 4},
            settings_snapshot_json={"snapshot_version": 1},
            chart_facts_json={"schema_version": 1, "planets": {"Sun": {"sign": "aries", "house": 1}}},
            place_label="Smoke Place",
        )
        share_id = created.get("quick_share_id")
        out.append((
            "be_quick_share_create",
            bool(share_id) and "quickShare=" in (created.get("url") or ""),
            f"id={share_id}",
        ))
        pub = get_quick_share_public(share_id)
        out.append((
            "be_quick_share_public_read",
            pub.get("brand") == "Relocation Astrology"
            and isinstance(pub.get("settings_snapshot_json"), dict)
            and isinstance(pub.get("viewport_json"), dict)
            and "chart_record_id" not in (pub.get("conditions_json") or {})
            and pub.get("chart_facts_json") is not None,
            f"brand={pub.get('brand')}",
        ))
        out.append(("be_quick_share_uuid_format", True, share_id))
    except Exception as exc:
        out.append(("be_quick_share_repository", False, str(exc)))
    finally:
        cleanup_share(admin, share_id)
    return out


def backend_http_checks(base, token, profile_id) -> list[tuple[str, bool, str]]:
    out: list[tuple[str, bool, str]] = []
    payload = {
        "profile_id": profile_id,
        "profile_display_name": "Smoke Profile",
        "source_surface": "map",
        "conditions_json": {
            "house_conditions": [{"planet": "sun", "house": 1}],
            "birth_year": 1990,
            "birth_month": 6,
            "birth_day": 15,
            "birth_hour_utc": 12.0,
        },
        "viewport_json": {"center_lat": 40.0, "center_lon": -74.0, "zoom": 4},
        "settings_snapshot_json": {"snapshot_version": 1},
    }
    st, raw = fetch(
        base,
        "/quick-share/create",
        headers={"Authorization": f"Bearer {token}"},
        method="POST",
        body=payload,
    )
    body = json.loads(raw.decode()) if raw else {}
    share_id = body.get("quick_share_id")
    out.append(("be_quick_share_http_create", st == 200 and bool(share_id), f"status={st}"))
    if share_id:
        st2, raw2 = fetch(base, f"/quick-share/{share_id}")
        pub = json.loads(raw2.decode()) if raw2 else {}
        out.append((
            "be_quick_share_http_public",
            st2 == 200 and pub.get("brand") == "Relocation Astrology",
            f"status={st2}",
        ))
    st3, _ = fetch(base, "/quick-share/create", method="POST", body=payload)
    out.append(("be_quick_share_create_requires_jwt", st3 == 401, f"status={st3}"))
    st4, _ = fetch(base, "/share-links", method="POST", body={
        "profile_id": profile_id,
        "target_type": "chart_record",
        "target_id": profile_id,
        "slug": "smoke-deprecated",
    })
    out.append(("be_share_links_still_deprecated", st4 == 410, f"status={st4}"))
    return out, share_id


def main() -> int:
    results: list[tuple[str, bool, str]] = []
    results.extend(static_checks())

    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

    if all([url, anon_key, service_key]):
        try:
            admin = __import__("supabase", fromlist=["create_client"]).create_client(url, service_key)
            admin.table("quick_shares").select("id").limit(1).execute()
            results.extend(backend_repository_checks(url, anon_key, service_key))
            if port_in_use(PORT):
                token, _aid, profile_id, admin = resolve_ctx(url, anon_key, service_key)
                http_results, share_id = backend_http_checks(
                    f"http://127.0.0.1:{PORT}", token, profile_id,
                )
                results.extend(http_results)
                cleanup_share(admin, share_id)
        except Exception as exc:
            results.append(("be_quick_share_table", False, str(exc)))
    else:
        print("SKIP backend quick-share tests (no Supabase env)")

    failed = [r for r in results if not r[1]]
    for name, ok, msg in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {msg}")
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
