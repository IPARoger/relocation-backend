#!/usr/bin/env python3
"""DIGNITIES-HOUSE-1 — house-correspondence PIH dignity validation."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ontology_unit_checks() -> list[tuple[str, bool, str]]:
    js_path = ROOT / "dignity_ontology.js"
    js = js_path.read_text(encoding="utf-8")
    test_js = "var window = globalThis;\n" + js + """
console.log(JSON.stringify({
  moon2: RMDignityOntology.lookupFamilyByHouse("Moon", 2),
  sun7: RMDignityOntology.lookupFamilyByHouse("Sun", 7),
  sun1: RMDignityOntology.lookupFamilyByHouse("Sun", 1),
  uranus5: RMDignityOntology.lookupFamilyByHouse("Uranus", 5),
}));
"""
    out: list[tuple[str, bool, str]] = []
    try:
        with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode="w", encoding="utf-8") as f:
            f.write(test_js)
            tmp = f.name
        raw = subprocess.check_output(["node", tmp], text=True).strip()
        data = json.loads(raw)
        out.append(("unit_moon_h2_supportive", data.get("moon2") == "supportive", str(data.get("moon2"))))
        out.append(("unit_sun_h7_challenging", data.get("sun7") == "challenging", str(data.get("sun7"))))
        out.append(("unit_sun_h1_supportive", data.get("sun1") == "supportive", str(data.get("sun1"))))
        out.append(("unit_unmapped_null", data.get("uranus5") is None, str(data.get("uranus5"))))
    except Exception as exc:
        out.append(("unit_ontology", False, str(exc)[:120]))
    finally:
        try:
            Path(tmp).unlink(missing_ok=True)
        except Exception:
            pass
    return out


def static_checks() -> list[tuple[str, bool, str]]:
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    onto = (ROOT / "dignity_ontology.js").read_text(encoding="utf-8")
    out: list[tuple[str, bool, str]] = []
    out.append(("static_lookup_by_house", "lookupFamilyByHouse" in onto, "ontology export"))
    out.append(("static_pih_uses_house_lookup",
                "lookupFamilyByHouse(planet, house)" in shell,
                "PIH house lookup"))
    out.append(("static_pih_not_sign_dignity",
                "pihDignityClass(planet, houseNum)" in shell or "pihDignityClass(planet, houseNum)" in shell.replace("houseNum", "house"),
                "house param in cell"))
    sign_in_cell = "pihSignFromPlanetInfo(info)" in shell.split("function pihHouseCellHtml")[1].split("function pihDignitiesFooterHtml")[0]
    out.append(("static_pih_cell_no_sign_lookup", not sign_in_cell, "no sign in pihHouseCellHtml"))
    out.append(("static_dignities_help",
                "rm-pih-dignities-help" in shell and "PIH_DIGNITIES_HELP_COPY" in shell,
                "? help affordance"))
    out.append(("static_help_copy_relocation",
                "signs do not change" in shell and "houses do" in shell,
                "help mentions relocation"))
    out.append(("static_no_dignity_diff",
                "dignityDiff" not in shell and "dignity_diff" not in shell,
                "no dignity diff logic"))
    chunk = shell[shell.find("PIH_DIGNITIES_HELP_COPY"):shell.find("PIH_DIGNITIES_HELP_COPY") + 600] if "PIH_DIGNITIES_HELP_COPY" in shell else ""
    out.append(("static_no_scoring_language",
                not any(w in chunk.lower() for w in ("ranking", "better", "worse", "improved", "stronger")),
                "no scoring in help block"))
    return out


def main() -> int:
    results = ontology_unit_checks() + static_checks()
    passed = 0
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
        if ok:
            passed += 1
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
