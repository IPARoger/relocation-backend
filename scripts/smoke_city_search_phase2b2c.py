#!/usr/bin/env python3
"""CITY-SEARCH-2B+2C static smoke — prefix range + tier short-circuit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIG = ROOT / "supabase/migrations/2026_06_24_search_places_phase2b2c.sql"
MIG_2A = ROOT / "supabase/migrations/2026_06_23_search_places_phase2a.sql"


def main() -> int:
    mig = MIG.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    checks.append(("migration_file", MIG.is_file(), str(MIG)))
    checks.append(("helper_range_end", "normalized_prefix_range_end" in mig, "prefix upper bound helper"))
    checks.append(("alias_prefix_range", "pa.normalized_alias >= " in mig and "pa.normalized_alias < " in mig, "alias prefix range (2B)"))
    checks.append(("no_alias_like_prefix", "normalized_alias like" not in mig.lower(), "no LIKE prefix on aliases"))
    checks.append(("fast_plpgsql", "language plpgsql" in mig and "_sp_candidates" in mig, "fast RPC is plpgsql (2C)"))
    checks.append(("tier_short_circuit", "if v_have < v_lim then" in mig, "tier short-circuit guard"))
    checks.append(("fast_volatile", "language plpgsql\nvolatile" in mig.replace("\r\n","\n"), "fast RPC volatile for temp table"))
    checks.append(("temp_candidates", "_sp_candidates" in mig, "staged candidate table"))
    checks.append(("places_prefix_range", "normalized_canonical >= " in mig and "normalized_display_primary >= " in mig, "places prefix range"))
    checks.append(("2a_intact", MIG_2A.is_file(), "phase 2A migration present"))
    checks.append(("repo_nocache", "use_cache: bool = True" in (ROOT / "repositories/places_repository.py").read_text(), "benchmark nocache path"))

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
