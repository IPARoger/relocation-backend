#!/usr/bin/env python3
"""Import GeoNames cities500.txt alternatenames column into place_aliases."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.place_alias_normalize import normalize_place_alias, split_geonames_alternates

BATCH_SIZE = 100
SOURCE = "geonames_main"
DEFAULT_INPUT = ROOT / "cities500.txt"
PLACES_CACHE = Path("/tmp/places_geonames_map.json")
EXISTING_CACHE = Path("/tmp/place_aliases_existing_keys.json")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY", "")


def sb_request(path, method="GET", data=None, extra_headers=None, retries=6):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    body = json.dumps(data).encode() if data is not None else None
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=180) as r:
                raw = r.read()
                return json.loads(raw) if raw.strip() else []
        except urllib.error.HTTPError as e:
            if method == "POST" and e.code in (409, 502, 503, 504):
                return []
            last_err = e
            if attempt + 1 < retries:
                wait = min(30, 2 ** attempt)
                print(f"  retry {attempt + 1}/{retries - 1} after HTTP {e.code} ({wait}s)", flush=True)
                time.sleep(wait)
            else:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last_err = e
            if attempt + 1 < retries:
                wait = min(30, 2 ** attempt)
                print(f"  retry {attempt + 1}/{retries - 1} after {type(e).__name__} ({wait}s)", flush=True)
                time.sleep(wait)
            else:
                raise
    raise last_err



def count_existing_aliases() -> int:
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Prefer": "count=exact",
        "Range": "0-0",
    }
    url = f"{SUPABASE_URL}/rest/v1/place_aliases?select=id&source=eq.{SOURCE}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=60) as r:
        cr = r.headers.get("Content-Range", "")
    if "/" in cr:
        return int(cr.split("/")[-1])
    return 0


def paginate(path: str, page: int = 1000):
    offset = 0
    while True:
        rows = sb_request(f"{path}&limit={page}&offset={offset}")
        if not rows:
            break
        yield from rows
        if len(rows) < page:
            break
        offset += page


def load_places_map(use_cache: bool) -> dict:
    if use_cache and PLACES_CACHE.exists():
        age = time.time() - PLACES_CACHE.stat().st_mtime
        if age < 86400:
            print(f"Loading places map from cache {PLACES_CACHE} ...", flush=True)
            return json.loads(PLACES_CACHE.read_text())
    print("Loading places geonames_id map from Supabase ...", flush=True)
    out = {}
    for row in paginate("places?select=id,geonames_id,canonical_name&provider=eq.geonames&order=geonames_id.asc"):
        gid = str(row.get("geonames_id") or "").strip()
        if gid:
            out[gid] = row
    PLACES_CACHE.write_text(json.dumps(out))
    return out


def load_existing_keys(use_cache: bool) -> set[tuple[str, str]]:
    if use_cache and EXISTING_CACHE.exists():
        cached = {tuple(x) for x in json.loads(EXISTING_CACHE.read_text())}
        db_count = count_existing_aliases()
        if len(cached) == db_count:
            print(f"Loading existing alias keys from cache {EXISTING_CACHE} ({db_count:,}) ...", flush=True)
            return cached
        print(
            f"Stale existing-keys cache ({len(cached):,} vs DB {db_count:,}); refetching ...",
            flush=True,
        )
    print("Loading existing place_aliases keys from Supabase ...", flush=True)
    keys: set[tuple[str, str]] = set()
    n = 0
    for row in paginate(
        f"place_aliases?select=place_id,normalized_alias&source=eq.{SOURCE}&order=place_id.asc"
    ):
        keys.add((row["place_id"], row["normalized_alias"]))
        n += 1
        if n % 50000 == 0:
            print(f"  loaded {n:,} existing keys", flush=True)
    EXISTING_CACHE.write_text(json.dumps([list(k) for k in keys]))
    return keys


def build_pending(places: dict, input_path: Path, existing: set[tuple[str, str]] | None) -> list[dict]:
    pending = []
    seen: set[tuple[str, str]] = set()
    lines = matched = 0
    with input_path.open(encoding="utf-8") as f:
        for line in f:
            lines += 1
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            gid = parts[0].strip()
            place = places.get(gid)
            if not place:
                continue
            matched += 1
            canonical_norm = normalize_place_alias(place.get("canonical_name") or "")
            for alias in split_geonames_alternates(parts[3]):
                norm = normalize_place_alias(alias)
                if not norm or norm == canonical_norm:
                    continue
                key = (place["id"], norm)
                if key in seen:
                    continue
                seen.add(key)
                if existing and key in existing:
                    continue
                pending.append({
                    "place_id": place["id"],
                    "geonames_id": gid,
                    "alias": alias,
                    "normalized_alias": norm,
                    "language_code": None,
                    "source": SOURCE,
                    "is_preferred": False,
                })
    print(f"Parsed {lines:,} lines; {matched:,} cities; {len(pending):,} aliases to insert", flush=True)
    return pending


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true", help="Skip aliases already in place_aliases")
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY required", file=sys.stderr)
        return 1

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: {input_path} not found", file=sys.stderr)
        return 1

    use_cache = not args.no_cache
    places = load_places_map(use_cache)
    print(f"  {len(places):,} geonames places", flush=True)

    existing = load_existing_keys(use_cache) if args.resume else None
    if existing is not None:
        print(f"  {len(existing):,} existing alias keys to skip", flush=True)

    pending = build_pending(places, input_path, existing)
    if args.dry_run:
        for row in pending[:5]:
            print(" ", row)
        return 0
    if not pending:
        print("Nothing to insert.", flush=True)
        return 0

    done = errors = 0
    t0 = time.time()
    total = len(pending)
    for i in range(0, total, BATCH_SIZE):
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
            body = e.read()[:200]
            if e.code == 409:
                done += len(batch)
            else:
                print(f"  ERROR batch {i // BATCH_SIZE}: HTTP {e.code} {body!r}", flush=True)
                errors += 1
        if done % 10000 < BATCH_SIZE or i + BATCH_SIZE >= total:
            print(f"  {done:,}/{total:,} ({time.time() - t0:.0f}s) errors={errors}", flush=True)

    if use_cache and EXISTING_CACHE.exists():
        EXISTING_CACHE.unlink(missing_ok=True)

    print(f"Done: {done:,} aliases processed, errors={errors}", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
