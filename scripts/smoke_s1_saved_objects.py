#!/usr/bin/env python3
"""Smoke: S1 saved object management in Settings → My Data (static checks).

Verifies app_shell.html exposes canonical management sections, sort law,
favorites folder hooks, composite language, and confirmation dialog wiring.

Run:
  ./venv/bin/python scripts/smoke_s1_saved_objects.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_SHELL = ROOT / "app_shell.html"

CANONICAL_SORT_LABELS = ("A-Z", "A\u2013Z", "Recently Added", "Recently Viewed", "Distance")
FORBIDDEN_SORT = (
    "best match",
    "relevance",
    "ai sort",
    "weighted",
    "ranking",
    "smart sort",
)

REQUIRED_SECTIONS = (
    ("sec-data-profiles", "Birth Profiles"),
    ("sec-data-favorites", "Favorites"),
    ("sec-data-saved", "Saved Searches"),
    ("sec-data-comparisons", "Saved Comparisons"),
    ("sec-data-notes", "Notes"),
)

REQUIRED_HOOKS = (
    "SETTINGS_SORT_OPTIONS",
    "settingsConfirm",
    "rm-settings-confirm-dialog",
    "data-settings-fav-folders",
    "settings-fav-create-folder",
    "settings-fav-move-folder",
    "settings-profile-composite",
    "settings-obj-bulk-delete",
    "wireSettingsSavedObjects",
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not APP_SHELL.is_file():
        fail(f"missing {APP_SHELL}")

    text = APP_SHELL.read_text(encoding="utf-8")
    results: list[tuple[str, bool, str]] = []

    for sec_id, label in REQUIRED_SECTIONS:
        ok = sec_id in text and label in text
        results.append((f"section_{sec_id}", ok, label))

    for hook in REQUIRED_HOOKS:
        results.append((f"hook_{hook}", hook in text, hook))

        sort_block = re.search(r"const SETTINGS_SORT_OPTIONS = \[([\s\S]*?)\];", text)
    if not sort_block:
        fail("SETTINGS_SORT_OPTIONS block not found")
    sort_src = sort_block.group(1)
    sort_labels_ok = all(
        token in sort_src
        for token in ("recent-added", "recent-viewed", "distance", "az")
    ) and ("A\\u2013Z" in sort_src or "A-Z" in sort_src)
    results.append(("sort_labels_canonical", sort_labels_ok, "canonical sort labels"))
    sort_src = sort_src.lower()
    for bad in FORBIDDEN_SORT:
        results.append((f"no_forbidden_sort_{bad.replace(' ', '_')}", bad not in sort_src, bad))

    composite_ok = (
        "creates a" in text.lower()
        and "new" in text.lower()
        and "profile" in text.lower()
        and "never" in text.lower()
        and "source" in text.lower()
    )
    results.append(("composite_new_profile_language", composite_ok, "composite copy"))

    bulk_warn = "irreversible" in text.lower() and "settings-obj-bulk-delete" in text
    results.append(("bulk_delete_irreversible_warning", bulk_warn, "bulk delete copy"))

    confirm_dialog = "rm-settings-confirm-dialog" in text and "settingsConfirm(" in text
    results.append(("confirmation_dialog_present", confirm_dialog, "confirm dialog"))

    failed = [r for r in results if not r[1]]
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name} ({detail})")

    if failed:
        fail(f"{len(failed)} check(s) failed")
    print(f"PASS: smoke_s1_saved_objects ({len(results)} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
