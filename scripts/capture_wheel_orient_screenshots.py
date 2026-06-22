#!/usr/bin/env python3
"""Capture before/after wheel orientation screenshots (WHEEL-ORIENT-1)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
OUT = ROOT / "results" / "198_wheel_orient_screenshots"


def fetch_canonical() -> dict:
    from fastapi.testclient import TestClient
    import main_centerline_FIXER as m

    client = TestClient(m.app)
    params = dict(
        lat=55.7558,
        lon=37.6173,
        birth_year=1976,
        birth_month=1,
        birth_day=13,
        birth_hour_utc=12.0,
        place_name="Moscow, Russia",
    )
    r = client.get("/relocated-chart", params=params)
    r.raise_for_status()
    data = r.json()
    return data.get("canonical_chart") or data


def render_wheel_svg(canonical: dict) -> str:
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    start = shell.find("// WHEEL-1 / WHEEL-v2:")
    end = shell.find("function renderRelocatedWheelHtml", start)
    block = shell[start:end]
    js = (
        "function escapeHtml(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }\n"
        "function getVisibleBodyNamesSet() { return new Set(['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron']); }\n"
        + block
        + "\nconst canonical = "
        + json.dumps(canonical)
        + ";\nprocess.stdout.write(renderRelocatedWheelSvg(canonical));\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as jf:
        jf.write(js)
        js_path = Path(jf.name)
    try:
        proc = subprocess.run(["node", str(js_path)], capture_output=True, text=True, cwd=str(ROOT))
    finally:
        js_path.unlink(missing_ok=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return proc.stdout


def screenshot_svg(svg: str, out_path: Path) -> None:
    html = (
        "<!DOCTYPE html><html><head><style>"
        "body { margin: 24px; background: #f5f5f0; }"
        ".rm-wheel-disc { display: inline-block; border-radius: 50%; box-shadow: 0 0 34px 2px rgba(184,154,85,.2); }"
        ".rm-wheel-wrap { max-width: 420px; }"
        "</style></head><body>"
        f'<div class="rm-wheel-wrap"><div class="rm-wheel-disc">{svg}</div></div>'
        "</body></html>"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        html_path = Path(f.name)
    svg_path = out_path.with_suffix(".svg")
    svg_path.write_text(svg, encoding="utf-8")
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": 520, "height": 520})
            page.set_content(html, wait_until="domcontentloaded")
            page.screenshot(path=str(out_path), full_page=True)
            browser.close()
    finally:
        html_path.unlink(missing_ok=True)


def main() -> int:
    label = sys.argv[1] if len(sys.argv) > 1 else "after"
    OUT.mkdir(parents=True, exist_ok=True)
    canonical = fetch_canonical()
    svg = render_wheel_svg(canonical)
    out = OUT / f"{label}_moscow_wheel.png"
    screenshot_svg(svg, out)
    meta_path = OUT / "manifest.json"
    meta = []
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError:
            meta = []
    meta = [m for m in meta if m.get("label") != label]
    meta.append({
        "label": label,
        "place": "Moscow, Russia",
        "asc_lon": canonical.get("angles", {}).get("ASC", {}).get("longitude_deg"),
        "screenshot": str(out.relative_to(ROOT)),
    })
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
