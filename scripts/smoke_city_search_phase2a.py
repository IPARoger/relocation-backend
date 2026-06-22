#!/usr/bin/env python3
"""CITY-SEARCH-2A static smoke — migration + RPC branch rewrite."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIG = ROOT / "supabase/migrations/2026_06_23_search_places_phase2a.sql"
STAGED = ROOT / "supabase/migrations/2026_06_22_search_places_staged.sql"


def main() -> int:
    mig = MIG.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    checks.append(("migration_file", MIG.is_file(), str(MIG)))
    for col in ("normalized_canonical", "normalized_display_primary"):
        checks.append((f"column_{col}", col in mig, f"generated column {col}"))
    for idx in (
        "places_normalized_canonical_idx",
        "places_normalized_canonical_prefix_idx",
        "places_normalized_display_primary_idx",
        "places_normalized_display_primary_prefix_idx",
    ):
        checks.append((f"index_{idx}", idx in mig, idx))
    checks.append((
        "rpc_uses_normalized_canonical",
        "p.normalized_canonical = params.n" in mig and "normalize_place_alias_text(p.canonical_name)" not in mig.split("search_places_ranked_fast")[1],
        "fast RPC branch 1 uses column",
    ))
    checks.append((
        "rpc_uses_normalized_display",
        "p.normalized_display_primary = params.n" in mig,
        "fast RPC branch 2 uses column",
    ))
    checks.append((
        "repo_cache_bypass",
        "use_cache: bool = True" in (ROOT / "repositories/places_repository.py").read_text(),
        "search_places supports use_cache for benchmarks",
    ))

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"\n{passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
