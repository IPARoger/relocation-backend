"""
CITY-2: One-time GeoNames cities ingest into Supabase places table.

Source:  cities5000_enriched.json  (~68k rows, already on disk)
Target:  Supabase places table (live columns confirmed 2026-06-13)
Safety:  Aborts if table already has > 100 rows (prevents double-load).
         Existing 4 test rows are NOT deleted.
Rollback: DELETE FROM places WHERE provider = 'geonames';

Usage:
  cd /path/to/relocation-backend
  source .env.staging
  python3 scripts/ingest_cities_to_places.py [--dry-run] [--min-pop N] [--force]
"""

import json, os, sys, urllib.request, urllib.error, urllib.parse, time

DATASET_PATH = "cities5000_enriched.json"
BATCH_SIZE   = 500
PROVIDER     = "geonames"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = (os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
                or os.environ.get("SUPABASE_ANON_KEY", ""))

DRY_RUN = "--dry-run" in sys.argv
FORCE   = "--force"   in sys.argv
MIN_POP = 0
for i, arg in enumerate(sys.argv):
    if arg == "--min-pop" and i + 1 < len(sys.argv):
        MIN_POP = int(sys.argv[i + 1])

SAMPLE_CITIES = ["New York", "London", "Chiang Mai", "Podgorica"]


def sb_request(path, method="GET", data=None, extra_headers=None):
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
               "Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    body = json.dumps(data).encode() if data is not None else None
    req  = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/{path}",
                                  data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
        return r.status, json.loads(raw) if raw.strip() else []


def count_places():
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
               "Prefer": "count=exact", "Range": "0-0"}
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/places?select=count",
                                 headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        cr = r.headers.get("content-range", "0-0/0")
        return int(cr.split("/")[-1])


def search_sample(q):
    _, rows = sb_request(
        f"places?display_name=ilike.%25{urllib.parse.quote(q)}%25"
        f"&limit=3&order=importance_rank.desc.nullslast"
    )
    return rows


def map_row(city):
    name    = city["name"]
    admin1  = city.get("admin1") or city.get("admin1_code") or ""
    country = city.get("country") or ""
    cc      = (city.get("country_code") or "")[:2] or None

    parts   = [p for p in [name, admin1, country] if p]
    display = ", ".join(parts)
    pop     = int(city.get("pop") or 0)
    return {
        "display_name":     display,
        "canonical_name":   name,
        "latitude":         float(city["lat"]),
        "longitude":        float(city["lng"]),
        "country_code":     cc,
        "country_name":     country or None,
        "admin1":           admin1 or None,
        "timezone_id":      city.get("timezone") or None,
        "population":       pop or None,
        "geonames_id":      str(city["geoname_id"]),
        "provider":         PROVIDER,
        "provider_place_id":str(city["geoname_id"]),
        "importance_rank":  min(1.0, pop / 25_000_000.0),
    }


def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set.")
        sys.exit(1)

    print(f"Loading {DATASET_PATH} ...")
    cities = json.loads(open(DATASET_PATH).read())
    if MIN_POP > 0:
        cities = [c for c in cities if int(c.get("pop") or 0) >= MIN_POP]
    print(f"  {len(cities):,} cities (min-pop={MIN_POP})")

    if DRY_RUN:
        print("\nDRY RUN — first 5 rows:")
        for c in cities[:5]:
            print(" ", json.dumps(map_row(c)))
        sys.exit(0)

    count_before = count_places()
    print(f"\nplaces rows before: {count_before}")

    if count_before > 100 and not FORCE:
        print(f"\nABORTED: table already has {count_before} rows (guard).")
        print("  --force to skip. Rollback: DELETE FROM places WHERE provider='geonames';")
        sys.exit(1)

    rows   = [map_row(c) for c in cities]
    total  = len(rows)
    done   = 0
    errors = 0
    t0     = time.time()
    print(f"\nInserting {total:,} rows in batches of {BATCH_SIZE} ...")

    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        try:
            sb_request("places", method="POST", data=batch,
                       extra_headers={"Prefer": "resolution=ignore-duplicates,return=minimal"})
            done += len(batch)
        except urllib.error.HTTPError as e:
            print(f"  ERROR batch {i//BATCH_SIZE}: HTTP {e.code} — {e.read().decode()[:200]}")
            errors += 1
            time.sleep(1)
        except Exception as ex:
            print(f"  ERROR batch {i//BATCH_SIZE}: {ex}")
            errors += 1
            time.sleep(1)

        if (done % 10000 < BATCH_SIZE) or (i + BATCH_SIZE >= total):
            print(f"  {done:>6,}/{total:,}  ({time.time()-t0:.0f}s)  errors={errors}")

    count_after = count_places()
    print(f"\nDone.  before={count_before}  after={count_after}  "
          f"delta={count_after - count_before:,}  errors={errors}")

    print("\nSample search verification:")
    for q in SAMPLE_CITIES:
        results = search_sample(q)
        if results:
            r = results[0]
            print(f"  {q!r:15} -> {r.get('display_name')!r}  "
                  f"tz={r.get('timezone_id')}  pop={r.get('population')}")
        else:
            print(f"  {q!r:15} -> NOT FOUND")

    print("\nRollback: DELETE FROM places WHERE provider = 'geonames';")
    if errors:
        print(f"WARNING: {errors} batch(es) failed. Re-run with --force.")
    else:
        print("INGEST COMPLETE.")


if __name__ == "__main__":
    main()
