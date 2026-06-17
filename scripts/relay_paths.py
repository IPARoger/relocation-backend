"""Relay path resolution — supports sandbox via RELAY_HOME env."""
from __future__ import annotations

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _path(env_key: str, default: Path) -> Path:
    raw = os.environ.get(env_key, "").strip()
    if not raw:
        return default
    p = Path(raw)
    return p if p.is_absolute() else REPO / p


RELAY_HOME = _path("RELAY_HOME", REPO / "relay")
TASKS_DIR = _path("RELAY_TASKS_DIR", REPO / "tasks")
RESULTS_DIR = _path("RELAY_RESULTS_DIR", REPO / "results")
HANDOFFS_DIR = _path("RELAY_HANDOFFS_DIR", RELAY_HOME / "handoffs")
GOVERNANCE_DIR = _path("RELAY_GOVERNANCE_DIR", RELAY_HOME / "governance")
ROADMAP_QUEUE = _path("RELAY_ROADMAP_QUEUE", RELAY_HOME / "ROADMAP_QUEUE.md")
TEMPLATE = TASKS_DIR / "TEMPLATE.md"
