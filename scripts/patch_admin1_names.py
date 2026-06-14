"""
ADMIN1-FIX-3: Patch numeric GeoNames admin1 codes in Supabase places table.

Source:  admin1CodesASCII.txt (repo root)
Target:  Supabase places table, provider='geonames' rows only

Safety:
  - UUIDs never changed.
  - Only admin1 and display_name columns updated.
  - provider IS NULL / 'test' / 'smoke' rows never touched.
  - Rollback snapshot saved before any writes.
  - --dry-run prints plan without writing.
  - --rollback restores from snapshot.

Usage:
  python3 scripts/patch_admin1_names.py --dry-run
  python3 scripts/patch_admin1_names.py
  python3 scripts/patch_admin1_names.py --rollback
"""

import json, os, sys, time
from pathlib import Path
from collections import defaultdict
import requests as _requests

REPO_ROOT     = Path(__file__).resolve().parent.parent
ADMIN1_FILE   = REPO_ROOT / "admin1CodesASCII.txt"
ROLLBACK_FILE = REPO_ROOT / "scripts" / "admin1_patch_rollback_snapshot.json"
BATCH_SIZE    = 500
PAGE_SIZE     = 1000
DRY_RUN       = "--dry-run"  in sys.argv
DO_ROLLBACK   = "--rollback" in sys.argv

# Load .env.staging (canonical live DB) then fall back to .env
def _load_env():
    # Try .env.staging (live places DB) first; fall back to .env.
    # Always write unconditionally so shell-inherited values don't mask the correct project.
    loaded = False
    for fn in [REPO_ROOT / ".env.staging", REPO_ROOT / ".env"]:
        if fn.exists():
            for line in fn.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")
            loaded = True
            break  # stop after first file found
    if not loaded:
        print("WARNING: no .env.staging or .env found")
_load_env()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = (os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
                or os.environ.get("SUPABASE_ANON_KEY", ""))

# Manually reviewed override: GeoNames says "State of Berlin"; we use "Berlin".
ADMIN1_OVERRIDES = {"DE.16": "Berlin"}

DRY_RUN_PROBES = [
    ("Shanghai",  "CN", "1796236"),
    ("Mumbai",    "IN", "1275339"),
    ("Tokyo",     "JP", "1850147"),
    ("Paris",     "FR", "2988507"),
    ("Sao Paulo", "BR", "3448439"),
    ("Berlin",    "DE", "2950159"),
]

# ---------------------------------------------------------------------------
# urllib replaced by requests

def _base_headers():
    return {
        "apikey":        SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type":  "application/json",
    }

def sb_get(path, retries=5, backoff=2):
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    for attempt in range(retries):
        try:
            r = _requests.get(url, headers=_base_headers(), timeout=(10, 30))
            r.raise_for_status()
            return r.json()
        except Exception as ex:
            if attempt == retries - 1:
                raise
            wait = backoff ** attempt
            print(f"  GET retry {attempt+1}/{retries} ({ex.__class__.__name__}) — wait {wait}s")
            time.sleep(wait)

def sb_patch(path, data, retries=4, backoff=2):
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    hdrs = {**_base_headers(), "Prefer": "return=minimal"}
    for attempt in range(retries):
        try:
            r = _requests.patch(url, headers=hdrs, json=data, timeout=(10, 30))
            r.raise_for_status()
            return
        except Exception as ex:
            if attempt == retries - 1:
                raise
            wait = backoff ** attempt
            time.sleep(wait)

# ---------------------------------------------------------------------------

def load_admin1_lookup():
    if not ADMIN1_FILE.exists():
        print(f"ERROR: {ADMIN1_FILE} not found.")
        print("  Download: https://download.geonames.org/export/dump/admin1CodesASCII.txt")
        sys.exit(1)
    lookup = {}
    for line in ADMIN1_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            lookup[parts[0]] = parts[1]
    for key, name in ADMIN1_OVERRIDES.items():
        lookup[key] = name
    return lookup

def fetch_all_geonames_rows():
    rows = []
    offset = 0
    while True:
        path = (
            f"places?provider=eq.geonames"
            f"&select=id,geonames_id,canonical_name,admin1,country_code,country_name,display_name"
            f"&offset={offset}&limit={PAGE_SIZE}&order=id.asc"
        )
        batch = sb_get(path)
        rows.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        if offset % 10000 == 0:
            print(f"  Fetched {offset:,} rows...")
    return rows

def compute_update(row, lookup):
    current_a1 = row.get("admin1") or ""
    if not current_a1.lstrip("-").isnumeric():
        return None
    cc      = row.get("country_code") or ""
    key     = f"{cc}.{current_a1}"
    name    = row.get("canonical_name") or ""
    country = row.get("country_name") or ""
    resolved = lookup.get(key)
    if resolved:
        new_a1   = resolved
        parts    = [p for p in [name, resolved, country] if p]
    else:
        new_a1   = None
        parts    = [p for p in [name, country] if p]
    new_dn = ", ".join(parts)
    if new_a1 == current_a1 and new_dn == row.get("display_name", ""):
        return None
    return new_a1, new_dn

def do_rollback():
    if not ROLLBACK_FILE.exists():
        print(f"ERROR: Snapshot not found: {ROLLBACK_FILE}"); sys.exit(1)
    snapshot = json.loads(ROLLBACK_FILE.read_text())
    print(f"Rolling back {len(snapshot):,} rows...")
    if DRY_RUN:
        for r in snapshot[:3]:
            print(f"  would restore {r['id']}: {r['old_admin1']!r} / {r['old_display_name']!r}")
        print("DRY RUN — no writes."); return
    done = errors = 0
    for i in range(0, len(snapshot), BATCH_SIZE):
        batch = snapshot[i:i+BATCH_SIZE]
        for r in batch:
            try:
                sb_patch(f"places?id=eq.{r['id']}",
                         {"admin1": r["old_admin1"], "display_name": r["old_display_name"]})
                done += 1
            except Exception as ex:
                print(f"  ERROR {r['id']}: {ex}"); errors += 1
        time.sleep(0.05)
    print(f"Rollback done. Restored={done:,}  Errors={errors}")

def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set."); sys.exit(1)
    if DO_ROLLBACK:
        do_rollback(); return

    lookup = load_admin1_lookup()
    print(f"Loaded {len(lookup):,} admin1 mappings ({len(ADMIN1_OVERRIDES)} override(s))")

    print(f"\nFetching all places WHERE provider='geonames'...")
    rows = fetch_all_geonames_rows()
    print(f"  {len(rows):,} rows fetched")

    plan = []
    skipped = 0
    for row in rows:
        result = compute_update(row, lookup)
        if result is None:
            skipped += 1; continue
        new_a1, new_dn = result
        plan.append({"id": row["id"], "new_admin1": new_a1, "new_display": new_dn,
                     "old_admin1": row.get("admin1"), "old_display": row.get("display_name")})

    resolvable   = sum(1 for p in plan if p["new_admin1"] is not None)
    unresolvable = sum(1 for p in plan if p["new_admin1"] is None)

    print(f"\nUpdate plan:")
    print(f"  Already named (skip):  {skipped:,}")
    print(f"  Resolvable updates:    {resolvable:,}")
    print(f"  Unresolvable (-> null):{unresolvable:,}")
    print(f"  Total to update:       {len(plan):,}")

    probe_gids = {gid for _, _, gid in DRY_RUN_PROBES}
    probe_map  = {row["geonames_id"]: row for row in rows if row.get("geonames_id") in probe_gids}
    print(f"\nSample cities:")
    for label, cc, gid in DRY_RUN_PROBES:
        row = probe_map.get(gid)
        if not row:
            print(f"  {label}: NOT FOUND"); continue
        result = compute_update(row, lookup)
        old_dn = row.get("display_name","?")
        new_dn = result[1] if result else old_dn
        mark = "CHANGED" if old_dn != new_dn else "SAME"
        print(f"  [{mark}] {label}")
        print(f"    OLD: {old_dn!r}")
        print(f"    NEW: {new_dn!r}")

    if DRY_RUN:
        print("\nDRY RUN complete — no writes made."); return

    # Save rollback snapshot
    snapshot = [{"id": p["id"], "old_admin1": p["old_admin1"],
                 "old_display_name": p["old_display"]} for p in plan]
    ROLLBACK_FILE.write_text(json.dumps(snapshot, indent=2))
    print(f"\nRollback snapshot saved: {ROLLBACK_FILE} ({len(snapshot):,} rows)")

    # Batched updates — group rows sharing same (new_admin1, new_display) within each batch
    print(f"\nApplying updates (batch size {BATCH_SIZE})...")
    done = errors = 0
    t0 = time.time()

    for i in range(0, len(plan), BATCH_SIZE):
        batch = plan[i:i+BATCH_SIZE]
        by_value = defaultdict(list)
        for p in batch:
            by_value[(p["new_admin1"], p["new_display"])].append(p["id"])

        for (new_a1, new_dn), id_list in by_value.items():
            id_csv = ",".join(id_list)
            try:
                sb_patch(f"places?id=in.({id_csv})",
                         {"admin1": new_a1, "display_name": new_dn})
                done += len(id_list)
            except Exception as ex:
                print(f"  ERROR ids={id_csv[:60]}: {ex}")
                errors += len(id_list)

        if (done + errors) % 5000 < BATCH_SIZE or i + BATCH_SIZE >= len(plan):
            print(f"  {done+errors:>7,}/{len(plan):,}  updated={done:,}  errors={errors}  ({time.time()-t0:.0f}s)")
        time.sleep(0.02)

    print(f"\nDone. Updated={done:,}  Errors={errors}  Time={time.time()-t0:.0f}s")
    if errors:
        print(f"WARNING: {errors} rows failed. Re-run to retry (snapshot preserved).")
    else:
        print("All rows updated successfully.")

if __name__ == "__main__":
    main()
