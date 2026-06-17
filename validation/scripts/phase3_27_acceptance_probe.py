#!/usr/bin/env python3
"""Phase 3.27 true-discovery acceptance probe.

This script is an acceptance-test harness, not an animation implementation.
It is intentionally hostile to Phase 3.26-style overclaiming.

Default intent:
  - Run static audits against a sandbox HTML file.
  - Require dynamic migration proof for acceptance.
  - Exit non-zero on failed acceptance criteria.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


FORBIDDEN_TARGET_PATTERNS = [
    r"\bseamTarget\b",
    r"\bboundaryTarget\b",
    r"\bsettlementTarget\b",
    r"\bfinalTarget\b",
    r"\btargetPolygon\b",
    r"\bboundarySamples\b",
    r"\bseamSamples\b",
    r"\bpolygonTarget\b",
    r"\btargetFromPolygon\b",
    r"\bbuildBoundarySamples\b",
    r"\bdrawBoundaryLayer\b",
    r"\bsampleBoundary\b",
    r"\btraceBoundary\b",
]

TIME_SCRIPT_PATTERNS = [
    r"final\s*:\s*smoothstep\s*\([^)]*progress",
    r"finalAlpha\s*=.*(?:progress|elapsed|DURATION|t\b)",
    r"\bcompression\s*=\s*smoothstep\s*\([^)]*progress",
    r"\bcooling\s*=\s*smoothstep\s*\([^)]*(?:progress|state\.progress)",
    r"state\.progress\s*>\s*0\.\d+",
    r"\bprogress\s*>\s*0\.\d+",
    r"const\s+PHASES\s*=\s*\[",
    r"\{\s*t\s*:\s*0\.\d+\s*,\s*name\s*:",
]

HARDCODED_PROOF_PATTERNS = [
    r"hasDirectBoundaryTargets\s*:\s*false",
    r"usesTruthOracleOnly\s*:\s*true",
]

REPORT_FORBIDDEN_SUCCESS_TERMS = [
    "emergent",
    "emerges",
    "solver-caused",
    "field-discovered",
    "truth oracle only",
    "truth-oracle only",
    "no direct boundary targets",
    "full-field migration",
    "compression from uncertainty",
    "virga from abandonment",
    "final after stabilization",
    "visible particles are solver particles",
]

SUCCESS_CLAIM_TEST_REQUIREMENTS = {
    "emergent": ["froth_causality_test", "time_script_audit"],
    "emerges": ["froth_causality_test", "time_script_audit"],
    "truth oracle only": ["geometry_use_audit"],
    "truth-oracle only": ["geometry_use_audit"],
    "no direct boundary targets": ["boundary_target_audit", "geometry_use_audit"],
    "virga": ["virga_causality_test"],
    "compression": ["time_script_audit"],
    "final": ["final_renderer_test"],
}


@dataclass
class TestResult:
    name: str
    mode: str = "static"
    passed: bool = True
    evidence: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.passed = False
        self.failures.append(message)

    def note(self, message: str) -> None:
        self.evidence.append(message)


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def matching_lines(text: str, pattern: str, flags: int = 0) -> list[str]:
    hits = []
    for match in re.finditer(pattern, text, flags):
        line_no = line_for_offset(text, match.start())
        line = text.splitlines()[line_no - 1].strip()
        hits.append(f"L{line_no}: {line}")
    return hits


def function_body(text: str, function_name: str) -> str:
    start = re.search(rf"function\s+{re.escape(function_name)}\s*\([^)]*\)\s*\{{", text)
    if not start:
        return ""
    index = start.end()
    depth = 1
    while index < len(text) and depth:
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        index += 1
    return text[start.start() : index]


def passive_sky_detection(text: str) -> TestResult:
    result = TestResult("passive_sky_detection")
    background = function_body(text, "drawBackground")
    if not background:
        result.note("No drawBackground() function found.")
        return result

    star_like_lines = []
    for line_no, line in enumerate(background.splitlines(), start=1):
        stripped = line.strip()
        if "drawCell(" in stripped or ".arc(" in stripped or "ctx.arc(" in stripped:
            star_like_lines.append(f"drawBackground L{line_no}: {stripped}")
            continue
        if "fillRect(" in stripped:
            is_full_canvas_fill = bool(re.search(r"fillRect\s*\(\s*0\s*,\s*0\s*,\s*W\s*,\s*H\s*\)", stripped))
            if not is_full_canvas_fill:
                star_like_lines.append(f"drawBackground L{line_no}: {stripped}")

    if star_like_lines:
        result.fail("Passive renderer drawBackground() contains passive star/dot rendering.")
        result.evidence.extend(star_like_lines)
    else:
        result.note("No passive star/dot primitive found inside drawBackground(); full-canvas background fills are ignored.")

    return result


def geometry_use_audit(text: str) -> TestResult:
    result = TestResult("geometry_use_audit", mode="static_and_instrumentation_required")
    if "polygonGeometryUseCounts" not in text:
        result.fail(
            "Missing required geometry-use instrumentation: polygonGeometryUseCounts."
        )
        return result

    for field in ["truthOracleCalls", "particleTargetUses", "renderUses", "finalRenderUses"]:
        if field not in text:
            result.fail(f"polygonGeometryUseCounts missing field: {field}")

    for field in ["particleTargetUses", "renderUses", "finalRenderUses"]:
        nonzero_pattern = rf"{field}\s*:\s*(?!0\b)([1-9]\d*|[A-Za-z_$])"
        hits = matching_lines(text, nonzero_pattern)
        if hits:
            result.fail(f"Geometry use count must be zero for {field}.")
            result.evidence.extend(hits)

    if result.passed:
        result.note("polygonGeometryUseCounts exists and forbidden use counters are statically zero.")
    return result


def boundary_target_audit(text: str) -> TestResult:
    result = TestResult("boundary_target_audit")
    for pattern in FORBIDDEN_TARGET_PATTERNS:
        hits = matching_lines(text, pattern)
        if hits:
            result.fail(f"Forbidden target pattern matched: {pattern}")
            result.evidence.extend(hits)

    for pattern in HARDCODED_PROOF_PATTERNS:
        hits = matching_lines(text, pattern)
        if hits:
            result.fail(f"Hardcoded proof boolean is not acceptance evidence: {pattern}")
            result.evidence.extend(hits)

    if result.passed:
        result.note("No forbidden target names or hardcoded target-proof booleans found.")
    return result


def time_script_audit(text: str) -> TestResult:
    result = TestResult("time_script_audit")
    for pattern in TIME_SCRIPT_PATTERNS:
        hits = matching_lines(text, pattern)
        if hits:
            result.fail(f"Time/progress-script pattern matched: {pattern}")
            result.evidence.extend(hits)

    if result.passed:
        result.note("No configured time-script patterns found.")
    return result


def froth_causality_test(text: str) -> TestResult:
    result = TestResult("froth_causality_test")
    required_terms = [
        "localParticleDensity",
        "baselineParticleDensity",
        "densityMultiplier",
        "localVelocityVariance",
        "recentSampleRate",
        "frontierPressure",
        "neighborDisagreement",
        "unresolvedDuration",
    ]
    missing = [term for term in required_terms if term not in text]
    if missing:
        result.fail("Missing explicit froth causality metrics: " + ", ".join(missing))
    if re.search(r"state\.progress\s*>\s*0\.55", text):
        result.fail("Froth-like size change is gated by state.progress > 0.55.")
        result.evidence.extend(matching_lines(text, r"state\.progress\s*>\s*0\.55"))
    if result.passed:
        result.note("Froth metrics present and no configured progress gate found.")
    return result


def virga_causality_test(text: str) -> TestResult:
    result = TestResult("virga_causality_test")
    required_terms = ["abandoned", "abandonedStep", "abandonmentReason"]
    missing = [term for term in required_terms if term not in text]
    if missing:
        result.fail("Missing explicit virga abandonment state: " + ", ".join(missing))

    cooling_hits = matching_lines(
        text,
        r"\bcooling\s*=\s*smoothstep\s*\([^)]*(?:progress|state\.progress)",
    )
    if cooling_hits:
        result.fail("Virga/cooling appears driven by progress/time.")
        result.evidence.extend(cooling_hits)

    if result.passed:
        result.note("Explicit abandonment state found and no configured progress cooling found.")
    return result


def final_renderer_test(text: str) -> TestResult:
    result = TestResult("final_renderer_test")
    draw_final = function_body(text, "drawFinal")
    state_at = function_body(text, "stateAt")

    if "fillRect(" in draw_final:
        result.fail("drawFinal() uses fillRect(), indicating raw grid-brick final rendering.")
        result.evidence.extend(matching_lines(draw_final, r"fillRect\s*\("))

    if re.search(r"final\s*:\s*smoothstep\s*\([^)]*progress", state_at):
        result.fail("Final reveal alpha is derived from progress/time.")
        result.evidence.extend(matching_lines(state_at, r"final\s*:\s*smoothstep\s*\([^)]*progress"))

    if not draw_final:
        result.fail("No drawFinal() function found for final renderer audit.")

    if result.passed:
        result.note("Final renderer does not match configured raw-brick/time-gate failures.")
    return result


def report_truthfulness_test(report_text: str | None, completed_results: list[TestResult]) -> TestResult:
    result = TestResult("report_truthfulness_test")
    if report_text is None:
        result.fail("No report provided; truthfulness cannot be audited.")
        return result

    lower = report_text.lower()
    passed_test_names = {test.name for test in completed_results if test.passed}

    for term, required_tests in SUCCESS_CLAIM_TEST_REQUIREMENTS.items():
        index = lower.find(term)
        if index == -1:
            continue
        window = lower[max(0, index - 500) : index + 900]
        cited_tests = [test_name for test_name in required_tests if test_name.lower() in window]
        passing_citations = [test_name for test_name in cited_tests if test_name in passed_test_names]
        if not cited_tests:
            result.fail(
                f"Report claim '{term}' does not cite required named test(s): {', '.join(required_tests)}"
            )
        elif not passing_citations:
            result.fail(
                f"Report claim '{term}' cites no passing required test output. Required: {', '.join(required_tests)}"
            )

    if "hasdirectboundarytargets: false" in lower or "usestruthoracleonly: true" in lower:
        result.fail("Report cites hardcoded debug booleans as acceptance evidence.")

    if "no prohibited matches were found" in lower and "grep" in lower:
        result.fail("Report treats grep-style absence as success evidence without mechanism proof.")

    if result.passed:
        result.note("No configured report truthfulness failures found.")
    return result


def full_field_migration_static_test(text: str) -> TestResult:
    result = TestResult("full_field_migration_test")
    required_particle_state = ["id", "x0", "y0", "x", "y", "visible", "origin", "targetReason"]
    missing = []
    particle_push_blocks = re.findall(r"probes\.push\s*\(\s*\{(?P<body>.*?)\}\s*\)", text, re.S)
    if not particle_push_blocks:
        result.fail("No probe/particle construction blocks found.")
        return result

    joined = "\n".join(particle_push_blocks)
    for term in required_particle_state:
        if not re.search(rf"\b{re.escape(term)}\s*:", joined):
            missing.append(term)

    if missing:
        result.fail(
            "Particle state lacks fields required for dynamic migration proof: " + ", ".join(missing)
        )

    if result.passed:
        result.note("Particle state exposes required dynamic migration provenance fields.")
    return result


def run_dynamic_migration_check(url: str | None) -> TestResult:
    result = TestResult("dynamic_full_field_migration_test", mode="dynamic_required")
    if not url:
        result.fail(
            "Dynamic migration proof was not run because --url was not provided. No future implementation can be accepted without dynamic migration proof."
        )
        return result

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover - environment dependent
        result.fail(f"Playwright unavailable for dynamic migration check: {exc}")
        return result

    js = r"""
    () => {
      if (typeof buildInitialProbes !== "function") {
        return { ok: false, error: "buildInitialProbes() not exposed" };
      }
      if (typeof simulate !== "function" || !window.model || !model.ring) {
        return { ok: false, error: "simulate() or model.ring unavailable" };
      }
      const initial = buildInitialProbes();
      const midSim = simulate(0.5, model.ring);
      const mid = midSim.probes;
      const cellWidth = typeof CELL_W === "number" ? CELL_W : 1;
      const cellHeight = typeof CELL_H === "number" ? CELL_H : cellWidth;
      const byId = new Map();
      const required = ["id", "x0", "y0", "x", "y", "visible", "origin", "targetReason"];
      for (const p of initial) {
        const missing = required.filter((key) => p[key] === undefined);
        if (missing.length) {
          return { ok: false, error: "particles lack required provenance fields: " + missing.join(", ") };
        }
        byId.set(p.id, p);
      }
      const macroCols = 8;
      const macroRows = 5;
      const occupied = new Set();
      for (const p of initial) {
        if (!p.visible) continue;
        const col = Math.max(0, Math.min(macroCols - 1, Math.floor(p.x0 / (W / macroCols))));
        const row = Math.max(0, Math.min(macroRows - 1, Math.floor(p.y0 / (H / macroRows))));
        occupied.add(col + ":" + row);
      }
      const distances = [];
      let moved = 0, compared = 0;
      for (const p of mid) {
        if (!byId.has(p.id)) continue;
        const start = byId.get(p.id);
        compared++;
        const d = Math.hypot(p.x - start.x0, p.y - start.y0);
        distances.push(d);
        if (d > 3 * cellWidth) moved++;
      }
      distances.sort((a, b) => a - b);
      const meanDistanceMoved = distances.length ? distances.reduce((a, b) => a + b, 0) / distances.length : 0;
      const medianDistanceMoved = distances.length ? distances[Math.floor(distances.length / 2)] : 0;
      let frontierAttractionAlignmentScore = null;
      if (midSim.grid && midSim.grid.frontier) {
        frontierAttractionAlignmentScore = "requires vector-to-frontier implementation";
      }
      const boundaryTargetAlignmentScore = window.boundarySamples ? "requires boundary sample comparison" : null;
      return {
        ok: true,
        initialCount: initial.length,
        initialMacroCellCoverage: occupied.size / (macroCols * macroRows),
        compared,
        moved,
        percentMoved: compared ? moved / compared : 0,
        meanDistanceMoved,
        medianDistanceMoved,
        frontierAttractionAlignmentScore,
        boundaryTargetAlignmentScore,
        threshold: 0.40
      };
    }
    """

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.wait_for_function(
                "() => window.__phase326State || window.__phase327State || window.model",
                timeout=60000,
            )
            data: dict[str, Any] = page.evaluate(js)
            browser.close()
    except Exception as exc:  # pragma: no cover - environment dependent
        result.fail(f"Dynamic migration check failed to execute: {exc}")
        return result

    result.note(json.dumps(data, sort_keys=True))
    if not data.get("ok"):
        result.fail(str(data.get("error", "dynamic migration check returned ok=false")))
    elif data.get("percentMoved", 0) < data.get("threshold", 0.40):
        result.fail("Fewer than 40% of initial particles moved more than 3 cell widths.")
    elif data.get("initialMacroCellCoverage", 0) < 0.70:
        result.fail("Initial macro-cell coverage is below 70%.")
    elif not isinstance(data.get("frontierAttractionAlignmentScore"), (int, float)):
        result.fail("frontierAttractionAlignmentScore was not computed numerically.")

    return result


def final_renderer_mode_test(text: str) -> TestResult:
    result = TestResult("final_renderer_mode_test", mode="static_and_instrumentation_required")
    mode_hits = matching_lines(text, r"finalRendererMode\s*:\s*['\"](?:debugGrid|resolvedContour)['\"]")
    if not mode_hits:
        result.fail('Missing required finalRendererMode declaration: "debugGrid" or "resolvedContour".')
        return result

    resolved_hits = matching_lines(text, r"finalRendererMode\s*:\s*['\"]resolvedContour['\"]")
    if not resolved_hits:
        result.fail('Acceptance finalRendererMode must be "resolvedContour" or equivalent non-brick renderer.')
        result.evidence.extend(mode_hits)
    else:
        result.note("finalRendererMode declares resolvedContour.")
    return result


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Phase 3.27 acceptance probe")
    parser.add_argument("--sandbox", required=True, help="Sandbox HTML file to audit")
    parser.add_argument("--report", help="Report markdown file to audit")
    parser.add_argument("--url", help="Browser URL for mandatory dynamic migration proof")
    args = parser.parse_args(argv)

    sandbox = Path(args.sandbox)
    if not sandbox.exists():
        print(json.dumps({"passed": False, "error": f"Missing sandbox: {sandbox}"}, indent=2))
        return 2

    report_text = None
    report_path = None
    if args.report:
        report_path = Path(args.report)
        if not report_path.exists():
            print(json.dumps({"passed": False, "error": f"Missing report: {report_path}"}, indent=2))
            return 2
        report_text = read_text(report_path)

    text = read_text(sandbox)

    results = [
        passive_sky_detection(text),
        full_field_migration_static_test(text),
        boundary_target_audit(text),
        geometry_use_audit(text),
        time_script_audit(text),
        froth_causality_test(text),
        virga_causality_test(text),
        final_renderer_test(text),
        final_renderer_mode_test(text),
    ]
    results.append(run_dynamic_migration_check(args.url))
    results.append(report_truthfulness_test(report_text, results))

    passed = all(result.passed for result in results)
    payload = {
        "sandbox": str(sandbox),
        "report": str(report_path) if report_path else None,
        "url": args.url,
        "passed": passed,
        "tests": [
            {
                "name": result.name,
                "mode": result.mode,
                "passed": result.passed,
                "evidence": result.evidence,
                "failures": result.failures,
            }
            for result in results
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
