#!/usr/bin/env python3
"""
MAP-MOTION-1 smoke test — object persistence / FLIP animation continuity.

Doctrine: every animated transition must keep the travelling element continuously
visible from departure to arrival. This script verifies the Genie<->bottle FLIP.

Checks:
  1. Pre-search: builder visible, bottle hidden.
  2. Mid-travel (~1s): builder still opaque, has non-identity transform, bottle not revealed.
  3. Post-travel (~2.2s): bottle revealed, builder flip-hidden, bottle at CSS position.
  4. Reopen (~0.7s mid): builder opaque and expanding, bottle not revealed.
  5. Post-reopen (~2.1s): builder visible, no residual styles, bottle hidden.
  6. No console errors.

Usage: python3 scripts/smoke_map_motion_object_persistence.py
"""
from __future__ import annotations
import json, sys, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SANDBOX = ROOT / "map_SANDBOX_genie_v7.html"
REPORT_DIR = ROOT / "validation" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("SKIP: pip install playwright && playwright install chromium")
    sys.exit(0)

results = []
console_errors = []

def check(name, passed, detail=""):
    sym = "v" if passed else "X"
    print(f"  {sym} [{'PASS' if passed else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    results.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})

def run():
    print(f"\nMAP-MOTION-1 Smoke  |  {SANDBOX.name}  |  {datetime.now(timezone.utc).isoformat()}\n")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.add_init_script("localStorage.setItem('rm-wt-dismissed','1');localStorage.setItem('rm-wt-step','99');")
        page.goto(SANDBOX.as_uri(), wait_until="domcontentloaded")
        time.sleep(1.5)

        # Pre-search
        print("-- Pre-search --")
        s = page.evaluate("""() => {
            var b=document.getElementById('builder'), bt=document.getElementById('bottle');
            var bs=window.getComputedStyle(b), bts=window.getComputedStyle(bt);
            var r=b.getBoundingClientRect();
            return {bOp:+bs.opacity, bW:r.width, bH:r.height, botOp:+bts.opacity};
        }""")
        check("Builder visible", s["bOp"]>0 and s["bW"]>0, f"op={s['bOp']} w={s['bW']:.0f}")
        check("Bottle hidden", s["botOp"]<0.05, f"op={s['botOp']}")

        # Trigger search via JS (bypasses dropdown UI; animation is what we test)
        print("\n-- Inject variable + search via JS --")
        try:
            page.evaluate("""() => {
                // Push one planet-house variable directly into the variables array
                if (typeof variables !== 'undefined') {
                    window.__sandbox.variables.push({id:'test1', category:'planet_house',
                        values:{planet:'Sun', house:1}, not:false});
                }
            }""")
            time.sleep(0.2)
            page.evaluate("() => window.__sandbox && window.__sandbox.doSearch()")
            t0 = time.time()
            check("Search triggered via JS", True)
        except Exception as e:
            check("Search triggered", False, str(e)); browser.close(); return

        # Mid-travel (~1s)
        print("\n-- Mid-travel (1s) --")
        time.sleep(1.0)
        m = page.evaluate("""() => {
            var b=document.getElementById('builder'), bt=document.getElementById('bottle');
            var bs=window.getComputedStyle(b), bts=window.getComputedStyle(bt);
            var tx=b.style.transform||bs.transform;
            return {bOp:+bs.opacity, tx:tx, botOp:+bts.opacity,
                    botRev:bt.classList.contains('bottle--revealed'),
                    exploreOn:document.body.classList.contains('explore')};
        }""")
        check("Explore active", m["exploreOn"])
        check("Builder opaque mid-travel (>=0.9)", m["bOp"]>=0.9, f"op={m['bOp']}")
        check("Builder has transform (travelling)", m["tx"] not in ("none","matrix(1, 0, 0, 1, 0, 0)",""), f"tx={m['tx'][:50]}")
        check("Bottle not yet revealed at 1s", not m["botRev"], f"botOp={m['botOp']}")

        # Post-travel (~2.2s)
        print("\n-- Post-travel (2.2s) --")
        time.sleep(max(0, 2.2-(time.time()-t0)))
        p = page.evaluate("""() => {
            var b=document.getElementById('builder'), bt=document.getElementById('bottle');
            var bs=window.getComputedStyle(b), bts=window.getComputedStyle(bt);
            var br=bt.getBoundingClientRect();
            return {bOp:+bs.opacity, flipHid:b.classList.contains('builder--flip-hidden'),
                    botRev:bt.classList.contains('bottle--revealed'), botOp:+bts.opacity,
                    botTop:br.top, botRight:1280-br.left-br.width,
                    bInlineTx:b.style.transform};
        }""")
        check("Builder flip-hidden after arrival", p["flipHid"], f"op={p['bOp']}")
        check("Bottle revealed after arrival", p["botRev"], f"op={p['botOp']}")
        check("Bottle at CSS position (top~62, right~18)", abs(p["botTop"]-62)<12 and abs(p["botRight"]-18)<12,
              f"top={p['botTop']:.0f} right={p['botRight']:.0f}")
        check("No residual inline transform on builder", not p["bInlineTx"], f"tx='{p['bInlineTx']}'")

        # Reopen
        print("\n-- Reopen (click bottle) --")
        try:
            page.click("#bottle"); t1=time.time(); check("Bottle clicked", True)
        except Exception as e:
            check("Bottle clicked", False, str(e)); browser.close(); return

        time.sleep(0.7)
        mr = page.evaluate("""() => {
            var b=document.getElementById('builder'), bt=document.getElementById('bottle');
            var bs=window.getComputedStyle(b), bts=window.getComputedStyle(bt);
            var animTx=window.getComputedStyle(b).transform; return {bOp:+bs.opacity, tx:animTx, botRev:bt.classList.contains('bottle--revealed')};
        }""")
        check("Builder opaque mid-reopen (>=0.9)", mr["bOp"]>=0.9, f"op={mr['bOp']}")
        check("Builder expanding (has transform)", mr["tx"] not in ("none","","matrix(1, 0, 0, 1, 0, 0)"), f"tx={mr['tx'][:50]}")
        check("Bottle not revealed mid-reopen", not mr["botRev"])

        time.sleep(max(0, 2.1-(time.time()-t1)))
        pr = page.evaluate("""() => {
            var b=document.getElementById('builder'), bt=document.getElementById('bottle');
            var bs=window.getComputedStyle(b);
            return {bOp:+bs.opacity, flipHid:b.classList.contains('builder--flip-hidden'),
                    inlineStyle:b.getAttribute('style')||'',
                    botRev:bt.classList.contains('bottle--revealed'),
                    exploreOn:document.body.classList.contains('explore')};
        }""")
        check("Builder visible post-reopen (>=0.9)", pr["bOp"]>=0.9, f"op={pr['bOp']}")
        check("No flip-hidden on builder post-reopen", not pr["flipHid"])
        check("No residual inline styles post-reopen", not pr["inlineStyle"].strip(), f"style='{pr['inlineStyle']}'")
        check("Bottle hidden post-reopen", not pr["botRev"])
        check("Explore class removed", not pr["exploreOn"])

        print("\n-- Console errors --")
        check("No JS errors", len(console_errors)==0,
              f"{len(console_errors)}: {'; '.join(console_errors[:2])}" if console_errors else "")

        browser.close()

    passed = sum(1 for r in results if r["status"]=="PASS")
    failed = sum(1 for r in results if r["status"]=="FAIL")
    print(f"\n{'='*50}")
    print(f"  RESULT: {passed}/{len(results)} passed, {failed} failed")
    print(f"{'='*50}")
    rpt = {"script":"smoke_map_motion_object_persistence","timestamp":datetime.now(timezone.utc).isoformat(),
           "summary":{"passed":passed,"failed":failed,"total":len(results)},
           "results":results,"console_errors":console_errors}
    out = REPORT_DIR/"smoke_map_motion_object_persistence.json"
    out.write_text(json.dumps(rpt, indent=2))
    print(f"  Report: {out}")
    if failed: sys.exit(1)

if __name__=="__main__":
    run()
