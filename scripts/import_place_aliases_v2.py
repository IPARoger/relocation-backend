#!/usr/bin/env python3
"""Import GeoNames alternateNamesV2.txt into place_aliases.

alternateNamesV2 columns (tab-separated):
  alternateNameId, geonameid, isolanguage, alternate name,
  isPreferredName, isShortName, isColloquial, isHistoric, from, to

Download (do not commit):
  https://download.geonames.org/export/dump/alternateNamesV2.zip
  unzip -p alternateNamesV2.zip alternateNamesV2.txt > data/geonames/alternateNamesV2.txt

Usage:
  set -a && source .env.staging && set +a
  python3 scripts/import_place_aliases_v2.py --input data/geonames/alternateNamesV2.txt

Rollback:
  DELETE FROM place_aliases WHERE source = 'geonames_v2';
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.place_alias_normalize import normalize_place_alias

BATCH_SIZE = 500
SOURCE = "geonames_v2"
DEFAULT_INPUT = ROOT / "data" / "geonames" / "alternateNamesV2.txt"
DOWNLOAD_URL = "https://download.geonames.org/export/dump/alternateNamesV2.zip"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY", "")


def sb_request(path, method="GET", data=None, extra_headers=None):
    import json

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/{path}", data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
        return json.loads(raw) if raw.strip() else []


def load_places_map():
    out = {}
    offset = 0
    page = 1000
    while True:
        rows = sb_request(
            f"places?select=id,geonames_id,canonical_name&provider=eq.geonames"
            f"&order=geonames_id.asc&limit={page}&offset={offset}"
        )
        if not rows:
            break
        for row in rows:
            gid = str(row.get("geonames_id") or "").strip()
            if gid:
                out[gid] = row
        if len(rows) < page:
            break
        offset += page
    return out


def ensure_input(path: Path, download: bool) -> None:
    if path.exists():
        return
    if not download:
        raise SystemExit(
            f"ERROR: {path} not found. Download alternateNamesV2.zip from GeoNames "
            f"or pass --download to fetch automatically."
        )
    dest_dir = path.parent
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / "alternateNamesV2.zip"
    print(f"Downloading {DOWNLOAD_URL} ...")
    urllib.request.urlretrieve(DOWNLOAD_URL, zip_path)
    print(f"Extracting to {path} ...")
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open("alternateNamesV2.txt") as src, path.open("wb") as dst:
            while True:
                chunk = src.read(1024 * 1024)
                if not chunk:
                    break
                dst.write(chunk)
    print("Download complete.")


def truthy(field: str) -> bool:
    return str(field or "").strip() == "1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--download", action="store_true", help="Download alternateNamesV2.zip if missing")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-rows", type=int, default=0, help="Stop after N matching aliases (debug)")
    args = parser.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY required", file=sys.stderr)
        return 1

    input_path = Path(args.input)
    ensure_input(input_path, args.download)

    print("Loading places geonames_id map ...")
    places = load_places_map()
    print(f"  {len(places):,} geonames places")

    pending = []
    seen_keys: set[tuple[str, str]] = set()
    lines = 0

    with input_path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            lines += 1
            if lines % 2_000_000 == 0:
                print(f"  scanned {lines:,} v2 lines, queued {len(pending):,}")
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            gid = parts[1].strip()
            place = places.get(gid)
            if not place:
                continue
            alias = parts[3].strip()
            if not alias or len(alias) < 2:
                continue
            norm = normalize_place_alias(alias)
            if not norm:
                continue
            canonical_norm = normalize_place_alias(place.get("canonical_name") or "")
            if norm == canonical_norm:
                continue
            key = (place["id"], norm)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            lang = parts[2].strip() or None
            pending.append(
                {
                    "place_id": place["id"],
                    "geonames_id": gid,
                    "alias": alias,
                    "normalized_alias": norm,
                    "language_code": lang,
                    "source": SOURCE,
                    "is_preferred": truthy(parts[4]) if len(parts) > 4 else False,
                }
            )
            if args.max_rows and len(pending) >= args.max_rows:
                break

    print(f"Scanned {lines:,} lines; {len(pending):,} aliases to insert")

    if args.dry_run:
        for row in pending[:5]:
            print(" ", row)
        return 0

    done = 0
    errors = 0
    t0 = time.time()
    for i in range(0, len(pending), BATCH_SIZE):
        batch = pending[i : i + BATCH_SIZE]
        try:
            sb_request(
                "place_aliases",
                method="POST",
                data=batch,
                extra_headers={"Prefer": "resolution=ignore-duplicates,return=minimal"},
            )
            done += len(batch)
        except urllib.error.HTTPError as e:
            print(f"  ERROR batch {i // BATCH_SIZE}: HTTP {e.code} {e.read()[:200]!r}")
            errors += 1
        if done and done % 50000 < BATCH_SIZE:
            print(f"  {done:,}/{len(pending):,} ({time.time() - t0:.0f}s) errors={errors}")

    print(f"Done: inserted~{done:,} aliases, errors={errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
