#!/usr/bin/env python3
"""S3 — Dignity settings smoke (static)."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    onto = (ROOT / "dignity_ontology.js").read_text(encoding="utf-8")
    defs = json.loads((ROOT / "settings/astrology_settings_defaults.json").read_text())
    checks = []

    def ok(name, cond):
        checks.append((name, cond))

    ok("presets in ontology", all(p in onto for p in ["ancient", "modern", "hybrid", "custom"]))
    ok("setConfig api", "setConfig" in onto and "lookupDetailByHouse" in onto)
    ok("preset examples", "Jupiter rules Pisces" in shell and "Neptune rules Pisces" in shell)
    ok("custom editor", "rm-dignity-custom-body" in shell and "dignity-add-rule" in shell)
    ok("four types only", all(t in shell for t in ["Ruler", "Detriment", "Exaltation", "Fall"]))
    ok("no triplicity", "triplicity" not in shell.lower().split("dignitiesdisplayhtml")[1][:2000] if "dignitiesdisplayhtml" in shell.lower() else True)
    ok("color paired mode", "rm-dignity-color-mode" in shell and "four" in shell)
    ok("save dignity_preset", "dignity_preset" in shell and "dignity_custom_rules" in shell)
    ok("apply on rehydrate", "applyDignitySettingsFromEff" in shell)
    ok("pih four color classes", "dignity-exaltation" in shell and "dignity-fall" in shell)
    ok("defaults hybrid", defs.get("dignity_preset") == "hybrid")
    ok("defaults colors", "supportive" in defs.get("dignity_colors", {}))
    ok("no soon badge on dignity preset", "Ontology preset" not in shell or "settingsSoonBadge()" not in shell.split("function dignitiesDisplayHtml")[1][:800])

    failed = [n for n,p in checks if not p]
    for n,p in checks:
        print(f"  {'PASS' if p else 'FAIL'} {n}")
    print(f"\n{'PASS' if not failed else 'FAIL'} {len(checks)-len(failed)}/{len(checks)} S3 dignity checks")
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())
