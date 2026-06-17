#!/usr/bin/env python3
"""Copy TELEGRAM_* from .env.local into GitHub Actions secrets.

Requires GH_TOKEN or GITHUB_TOKEN with repo admin (secrets write).

Usage:
  export GH_TOKEN=ghp_...
  python scripts/sync_github_telegram_secrets.py
"""

import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    from nacl import encoding, public
except ImportError:
    sys.stderr.write("Install PyNaCl: pip install pynacl\n")
    raise SystemExit(2)

REPO = os.environ.get("GITHUB_REPOSITORY", "IPARoger/relocation-backend")


def api(token, method, path, data=None):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        raise SystemExit(f"GitHub API {exc.code}: {body[:300]}") from exc


def encrypt(pub_b64, value):
    box = public.SealedBox(public.PublicKey(pub_b64.encode(), encoding.Base64Encoder()))
    return base64.b64encode(box.encrypt(value.encode())).decode()


def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.stderr.write("Set GH_TOKEN or GITHUB_TOKEN first.\n")
        return 1

    env_path = Path(__file__).resolve().parents[1] / ".env.local"
    if not env_path.is_file():
        sys.stderr.write(f"Missing {env_path}\n")
        return 1

    values = {}
    for line in env_path.read_text().splitlines():
        if line.startswith("TELEGRAM_BOT_TOKEN=") or line.startswith("TELEGRAM_CHAT_ID="):
            k, v = line.split("=", 1)
            values[k] = v.strip().strip('"').strip("'")

    if len(values) != 2:
        sys.stderr.write("Need TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env.local\n")
        return 1

    pk = api(token, "GET", f"/repos/{REPO}/actions/secrets/public-key")
    for name, value in values.items():
        api(
            token,
            "PUT",
            f"/repos/{REPO}/actions/secrets/{name}",
            {
                "encrypted_value": encrypt(pk["key"], value),
                "key_id": pk["key_id"],
            },
        )
        print(f"synced {name}")
    print("Done. Re-run Actions → telegram-test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Also sync Gmail if present in .env.local
GMAIL_KEYS = ("GMAIL_USER", "GMAIL_APP_PASSWORD", "RELAY_NOTIFY_EMAIL")
