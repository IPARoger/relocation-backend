#!/usr/bin/env python3
"""Capture SETTINGS-V3-4C Orbs & Aspects grid screenshot."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "settings_v3_4c_orbs_grid_screenshot.png"
PREVIEW = ROOT / "results" / "settings_v3_4c_orbs_grid_preview.html"


def build_preview_html() -> str:
    shell = (ROOT / "app_shell.html").read_text(encoding="utf-8")
    start = shell.find("/* SETTINGS-V3")
    end = shell.find(".settings-save-bar { position: sticky", start)
    sv3_css = shell[start:end] if start >= 0 and end > start else ""
    base_css = """
  * { box-sizing: border-box; }
  body { margin: 0; padding: 24px; font-family: system-ui, sans-serif; font-size: 14px; color: #1f2937; background: #f8fafc; }
  .rm-sv3-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 14px 16px; max-width: 520px; }
  .rm-sv3-card h4 { margin: 0 0 10px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; color: #6b7280; }
  input, select { font: inherit; padding: 4px 6px; border: 1px solid #d1d5db; border-radius: 4px; }
  input:disabled { opacity: 0.55; background: #f3f4f6; }
"""
    body = """
<div class="rm-sv3-root" id="rm-sv3-root">
  <div class="rm-sv3-card"><h4>Orbs &amp; Aspects</h4>
    <div class="rm-sv3-oa"><div class="rm-sv3-oa-grid">
      <div class="rm-sv3-oa-head">
        <div class="rm-sv3-oa-h-spacer"></div>
        <div class="rm-sv3-oa-h-tables">Tables</div>
        <div class="rm-sv3-oa-h-chart">Chart</div>
        <div class="rm-sv3-oa-h-orb">Orb</div>
      </div>
      <div class="rm-sv3-oa-row is-locked">
        <div class="rm-sv3-oa-label">Conjunction</div>
        <div class="rm-sv3-oa-tbl"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-cht"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-orb"><input type="number" value="10" disabled></div>
      </div>
      <div class="rm-sv3-oa-row is-locked">
        <div class="rm-sv3-oa-label">Opposition</div>
        <div class="rm-sv3-oa-tbl"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-cht"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-orb"><input type="number" value="10" disabled></div>
      </div>
      <div class="rm-sv3-oa-row is-locked">
        <div class="rm-sv3-oa-label">Square</div>
        <div class="rm-sv3-oa-tbl"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-cht"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-orb"><input type="number" value="8" disabled></div>
      </div>
      <div class="rm-sv3-oa-row is-locked">
        <div class="rm-sv3-oa-label">Trine</div>
        <div class="rm-sv3-oa-tbl"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-cht"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-orb"><input type="number" value="8" disabled></div>
      </div>
      <div class="rm-sv3-oa-row is-locked">
        <div class="rm-sv3-oa-label">Sextile</div>
        <div class="rm-sv3-oa-tbl"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-cht"><input type="checkbox" checked disabled></div>
        <div class="rm-sv3-oa-orb"><input type="number" value="6" disabled></div>
      </div>
    </div>
    <details class="rm-sv3-advanced rm-sv3-oa-minor-wrap" style="margin-top:10px;">
      <summary>Advanced Orbs &amp; Aspects</summary>
    </details>
    </div>
  </div>
</div>"""
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{base_css}{sv3_css}</style></head><body>{body}</body></html>"


def main() -> int:
    PREVIEW.write_text(build_preview_html(), encoding="utf-8")
    cmd = [
        "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
        "--user-data-dir=/tmp/chrome-sv3-4c-cap",
        "--window-size=560,520", f"--screenshot={OUT}", f"file://{PREVIEW}",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
