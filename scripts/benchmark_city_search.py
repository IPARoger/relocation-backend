#!/usr/bin/env python3
"""Benchmark GET /places/search first-hit latency (cache-busted)."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from statistics import median

DEFAULT_QUERIES = ["London", "Paris", "Kyoto", "New York", "Ubud"]
DEFAULT_BASE = "http://127.0.0.1:8004"


def fetch_ms(base: str, q: str, limit: int = 10, bust: int | None = None) -> tuple[int, int]:
    params = {"q": q, "limit": str(limit), "nocache": "1"}
    if bust is not None:
        params["_bust"] = str(bust)
    url = f"{base.rstrip('/')}/places/search?{urllib.parse.urlencode(params)}"
    t0 = time.perf_counter()
    with urllib.request.urlopen(url, timeout=120) as resp:
        body = resp.read()
    ms = int((time.perf_counter() - t0) * 1000)
    try:
        n = len(json.loads(body))
    except json.JSONDecodeError:
        n = -1
    return ms, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--queries", nargs="*", default=DEFAULT_QUERIES)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--json-out")
    args = ap.parse_args()

    rows = []
    for q in args.queries:
        times = []
        n = 0
        for i in range(args.runs):
            ms, n = fetch_ms(args.base, q, bust=int(time.time() * 1000) + i)
            times.append(ms)
        rows.append({"query": q, "n": n, "ms": times, "median_ms": median(times)})
        print(f"{q:12} median={int(median(times)):4}ms  n={n}  runs={times}")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump({"base": args.base, "queries": rows}, f, indent=2)
        print(f"wrote {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
