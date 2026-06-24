#!/usr/bin/env python3
"""Static smoke: MAP-GHOST-A click propagation repair for map_CURRENT.html.

Verifies ghost strip uses L.DomEvent.disableClickPropagation so Mute/Solo/NOT
clicks do not bubble to Leaflet.

Run:
    venv/bin/python scripts/smoke_ghost_click_propagation.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "map_CURRENT.html"


def check(label: str, ok: bool) -> bool:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    return ok


def main() -> int:
    if not MAP.exists():
        print(f"ABORT: {MAP} not found", file=sys.stderr)
        return 1

    src = MAP.read_text(encoding="utf-8")
    results: list[bool] = []

    print("\nMAP-GHOST-A click propagation:")
    results.append(check(
        "#rm-ghost-strip element present",
        'id="rm-ghost-strip"' in src,
    ))
    results.append(check(
        "initGhostStrip IIFE present",
        "function initGhostStrip" in src or "initGhostStrip()" in src,
    ))
    results.append(check(
        "L.DomEvent.disableClickPropagation called on ghost strip",
        bool(re.search(
            r"disableClickPropagation\s*\(\s*ghostEl\s*\)",
            src,
        )),
    ))
    results.append(check(
        "disableClickPropagation is inside MAP-UX-4 ghost block",
        bool(re.search(
            r"MAP-UX-4[\s\S]{0,800}disableClickPropagation\s*\(\s*ghostEl\s*\)",
            src,
        )),
    ))
    results.append(check(
        "ghost strip click handler still present",
        "data-gmini" in src and "syncGhost()" in src,
    ))

    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} PASS")
    if passed < total:
        print(f"FAILED: {total - passed}", file=sys.stderr)
        return 1
    print("PASS MAP-GHOST-A static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
