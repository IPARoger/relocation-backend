"""Shared V5 smoke guard: comparison plugin JS must parse under node --check."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V5_JS_FILES = (
    ROOT / "validation/mockups/beta/comparison_v5_route.js",
    ROOT / "validation/mockups/beta/comparison_v5_adapter.js",
)


def assert_v5_js_syntax(check) -> None:
    for path in V5_JS_FILES:
        result = subprocess.run(
            ["node", "--check", str(path)],
            capture_output=True,
            text=True,
        )
        rel = path.relative_to(ROOT)
        detail = result.stderr.strip() or result.stdout.strip()
        check(
            result.returncode == 0,
            f"node --check {rel}" + (f" — {detail}" if result.returncode != 0 else " ok"),
        )
