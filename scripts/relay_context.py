#!/usr/bin/env python3
"""Assemble discipline + closeout context for relay planning (the Claude brain step).

Governance: every *.md in relay/governance/ (move or symlink your binding docs there).
Closeouts: latest results/ files — replaces pasting Cursor output back into Claude.

Writes relay/handoffs/latest_context.md so nothing is hidden.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GOVERNANCE_DIR = REPO / "relay" / "governance"

PER_FILE_LIMIT = int(os.environ.get("RELAY_GOVERNANCE_FILE_LIMIT", "12000"))
LATEST_CLOSEOUT_LIMIT = int(os.environ.get("RELAY_LATEST_CLOSEOUT_LIMIT", "15000"))
OLDER_CLOSEOUT_LIMIT = int(os.environ.get("RELAY_OLDER_CLOSEOUT_LIMIT", "4000"))
RESULTS_KEEP = int(os.environ.get("RELAY_CLOSEOUTS_KEEP", "5"))
MAX_PACK_CHARS = int(os.environ.get("RELAY_CONTEXT_MAX_CHARS", "120000"))


def _read(path: Path, limit: int) -> str:
    if not path.is_file():
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return ""
    if len(text) > limit:
        return text[:limit] + f"\n\n[truncated at {limit} chars]\n"
    return text


def governance_files() -> list[Path]:
    if not GOVERNANCE_DIR.is_dir():
        return []
    files = [
        p
        for p in sorted(GOVERNANCE_DIR.glob("*.md"))
        if p.name.upper() != "README.MD"
    ]
    return files


def _numbered_results() -> list[tuple[int, Path]]:
    out: list[tuple[int, Path]] = []
    for f in (REPO / "results").glob("[0-9][0-9]_*.md"):
        m = re.match(r"(\d+)_", f.name)
        if m:
            out.append((int(m.group(1)), f))
    return sorted(out, key=lambda x: x[0])


def latest_closeout_path() -> Path | None:
    numbered = _numbered_results()
    return numbered[-1][1] if numbered else None


def build_context_pack() -> str:
    parts = [
        "=== RELAY CONTEXT PACK (planner API — replaces paste into Claude) ===",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "=== GOVERNANCE (relay/governance/*.md) ===",
    ]

    gov = governance_files()
    if not gov:
        parts.append(
            "(empty — add .md files to relay/governance/, or symlink existing canon docs)"
        )
    for path in gov:
        body = _read(path.resolve(), PER_FILE_LIMIT)
        if body:
            try:
                rel = path.resolve().relative_to(REPO)
            except ValueError:
                rel = path.name
            parts += [f"--- {rel} ---", body, ""]

    results = _numbered_results()
    if results:
        parts.append("=== CLOSEOUTS FROM CURSOR (you used to paste these into Claude) ===")
        kept = results[-RESULTS_KEEP:]
        for i, (n, f) in enumerate(kept):
            is_latest = i == len(kept) - 1
            limit = LATEST_CLOSEOUT_LIMIT if is_latest else OLDER_CLOSEOUT_LIMIT
            label = "LATEST — read carefully" if is_latest else "older"
            parts += [
                f"--- results/{f.name} ({label}) ---",
                _read(f, limit),
                "",
            ]

    tasks = sorted((REPO / "tasks").glob("[0-9][0-9]_*.md"))
    if tasks:
        parts.append("=== TASK INDEX ===")
        parts.append("\n".join(f.name for f in tasks[-20:]))

    pack = "\n".join(parts).strip() + "\n"
    if len(pack) > MAX_PACK_CHARS:
        pack = pack[:MAX_PACK_CHARS] + "\n\n[pack truncated at RELAY_CONTEXT_MAX_CHARS]\n"
    return pack


def write_context_snapshot() -> Path:
    pack = build_context_pack()
    out = REPO / "relay" / "handoffs" / "latest_context.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(pack, encoding="utf-8")
    return out


def write_closeout_handoff(closeout_path: Path | None = None) -> Path | None:
    """Log the closeout the brain will see on the next plan (paste-back step)."""
    path = closeout_path or latest_closeout_path()
    if not path or not path.is_file():
        return None
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = REPO / "relay" / "handoffs" / f"{ts}_closeout_for_brain.md"
    body = _read(path, LATEST_CLOSEOUT_LIMIT)
    text = (
        "# Closeout ingested for next Claude/GPT plan\n\n"
        "This replaces pasting Cursor output back into Claude by hand.\n"
        "On the next `relay_robot.py` plan step, this file is included in the context pack.\n\n"
        f"## Source: {path.relative_to(REPO)}\n\n"
        f"{body}\n"
    )
    out.write_text(text, encoding="utf-8")
    return out


if __name__ == "__main__":
    p = write_context_snapshot()
    print(f"Wrote {p.relative_to(REPO)} ({p.stat().st_size} bytes, {len(governance_files())} governance files)")
