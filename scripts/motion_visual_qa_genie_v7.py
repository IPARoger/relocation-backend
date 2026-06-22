#!/usr/bin/env python3
"""MOTION-QA-1 corrected — map_SANDBOX_genie_v7.html only."""
from __future__ import annotations
import asyncio, json, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = "map_SANDBOX_genie_v7.html"
ROOT_MAP = ROOT / MAP
URL = ROOT_MAP.as_uri() + f"?bust={int(time.time())}"
BASE = "file://"
SHOT_DIR = ROOT / "results" / "215_motion_visual_qa_screenshots"
DATA_PATH = ROOT / "results" / "215_motion_visual_qa_data.json"
SEED_VARS = [
    {"id":"qa1","category":"planet_house","values":{"planet":"Mars","house":7},"not":False},
    {"id":"qa2","category":"planet_house","values":{"planet":"Venus","house":10},"not":False},
    {"id":"qa3","category":"angle_sign","values":{"angle":"ASC","sign":"Leo"},"not":False},
    {"id":"qa4","category":"aspect_angle","values":{"planet":"Sun","aspect":"trine","angle":"MC"},"not":False},
]

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

async def snap(page, name):
    await page.screenshot(path=str(SHOT_DIR / name))

async def state(page):
    return await page.evaluate("""() => {
        const b=document.getElementById('builder'), bt=document.getElementById('bottle'), g=document.getElementById('ghoststrip');
        const bs=b?getComputedStyle(b):null, bts=bt?getComputedStyle(bt):null, br=b?b.getBoundingClientRect():{width:0};
        return {explore:document.body.classList.contains('explore'), builderOp:bs?+bs.opacity:-1, builderW:br.width,
          builderFlipHidden:b?b.classList.contains('builder--flip-hidden'):null,
          bottleRevealed:bt?bt.classList.contains('bottle--revealed'):null, bottleOp:bts?+bts.opacity:-1,
          ghostTokens:g?g.querySelectorAll('.gtok').length:0,
          plateText:document.getElementById('plate')?.textContent?.trim().slice(0,40)||'',
          saveDiskOp:document.getElementById('saveDisk')?+getComputedStyle(document.getElementById('saveDisk')).opacity:-1};
    }""")

async def seed_vars(page):
    await page.evaluate("""(vars)=>{window.__sandbox.variables.length=0;vars.forEach(v=>window.__sandbox.variables.push({id:v.id,category:v.category,values:v.values,not:v.not,colorIdx:0,mute:false}));if(typeof renderAll==='function')renderAll();}""", SEED_VARS)

async def do_search(page): await page.evaluate("()=>window.__sandbox.doSearch()")
async def to_setup(page): await page.evaluate("()=>window.__sandbox.toSetup()")
async def settled(page, ms=2200): await page.wait_for_timeout(ms)

async def run_sc(page, scenarios, failures, sid, name, fn):
    try:
        r = await fn(); scenarios.append({"id":sid,"name":name,"status":r.get("status","PASS"),**r})
        if r.get("status")=="FAIL": failures.append({"scenario":sid,"detail":r.get("detail","")})
    except Exception as e:
        scenarios.append({"id":sid,"name":name,"status":"ERROR","detail":str(e)}); failures.append({"scenario":sid,"detail":str(e)})

async def main():
    from playwright.async_api import async_playwright
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    for p in SHOT_DIR.glob('*.png'): p.unlink()
    scenarios, failures, stress_log, console_errors = [], [], [], []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width":1440,"height":900})
        page.on("console", lambda m: console_errors.append(m.text) if m.type=="error" else None)
        await page.add_init_script("localStorage.setItem('rm-wt-dismissed','1');localStorage.setItem('rm-wt-step','99');")
        await page.goto(URL, wait_until="domcontentloaded"); await page.wait_for_timeout(1500); await seed_vars(page)

        async def s1():
            await snap(page,"01_search_before_enter.png"); await do_search(page)
            await page.wait_for_timeout(200); await snap(page,"01_mid_flip_200ms.png")
            await page.wait_for_timeout(600); await snap(page,"01_mid_flip_800ms.png"); await settled(page,1400)
            s=await state(page); await snap(page,"01_explore_settled.png")
            ok=s["explore"] and s["bottleRevealed"] and s["builderFlipHidden"]
            return {"status":"PASS" if ok else "FAIL","detail":s}
        await run_sc(page,scenarios,failures,"1","Panel → Bottle FLIP",s1)

        async def s2():
            await to_setup(page); await page.wait_for_timeout(200); await snap(page,"02_reverse_mid_200ms.png")
            await page.wait_for_timeout(600); await snap(page,"02_reverse_mid_800ms.png"); await settled(page,1200)
            s=await state(page); await snap(page,"02_search_restored.png")
            ok=(not s["explore"]) and (not s["bottleRevealed"]) and s["builderOp"]>=0.9
            return {"status":"PASS" if ok else "FAIL","detail":s}
        await run_sc(page,scenarios,failures,"2","Bottle → Panel reverse FLIP",s2)

        async def s3():
            await do_search(page); await page.wait_for_timeout(900); await snap(page,"03_ghost_mid_enter.png")
            await settled(page,1300); s=await state(page); await snap(page,"03_ghost_settled.png")
            await page.click("#ghoststrip .gtok .mb"); await page.wait_for_timeout(300)
            muted=await page.evaluate("()=>document.querySelector('#ghoststrip .gtok.muted')!==null")
            await snap(page,"03_ghost_mute_toggled.png")
            return {"status":"PASS" if s["ghostTokens"]>=4 and muted else "FAIL","detail":{"tokens":s["ghostTokens"],"muted":muted}}
        await run_sc(page,scenarios,failures,"3","Ghost strip transitions",s3)

        async def s4():
            await to_setup(page); await settled(page); await snap(page,"04_pill_search_idle.png")
            await do_search(page); await page.wait_for_timeout(400); await snap(page,"04_pill_saving.png")
            morph=await page.evaluate("()=>!!document.querySelector('body > div[style*=fixed]') || document.getElementById('saveInline').style.visibility==='hidden'")
            await page.wait_for_timeout(2600); s=await state(page); await snap(page,"04_pill_during_explore.png"); await snap(page,"04_pill_saved.png")
            disk_bug=s["saveDiskOp"]<0.05
            return {"status":"PASS" if s["explore"] and morph else "FAIL","detail":{**s,"morph_seen":morph,"disk_opacity_stuck_zero":disk_bug}}
        await run_sc(page,scenarios,failures,"4","Save pill/disk transitions",s4)

        async def s5():
            await to_setup(page); await settled(page); await snap(page,"05_nameplate_search.png")
            await do_search(page); await settled(page)
            plate=await page.evaluate("()=>({visible:!!document.getElementById('plate'),text:document.getElementById('plate').textContent.trim()})")
            await snap(page,"05_nameplate_explore.png")
            return {"status":"PASS" if plate["visible"] and "David Goodman" in plate["text"] else "FAIL","detail":plate}
        await run_sc(page,scenarios,failures,"5","Nameplate behavior",s5)

        async def s6():
            await to_setup(page); await settled(page); await snap(page,"06_search_start.png")
            await do_search(page); await page.wait_for_timeout(1000); await snap(page,"06_mid_transition.png")
            await settled(page,1200); s=await state(page); await snap(page,"06_explore_end.png")
            return {"status":"PASS" if s["explore"] else "FAIL","detail":s}
        await run_sc(page,scenarios,failures,"6","Search → Explore",s6)

        async def s7():
            await to_setup(page); await page.wait_for_timeout(400); await snap(page,"07_mid_exit.png")
            await settled(page,1500); s=await state(page); await snap(page,"07_search_restored.png")
            ok=(not s["explore"]) and s["builderOp"]>=0.9 and not s["builderFlipHidden"]
            return {"status":"PASS" if ok else "FAIL","detail":s}
        await run_sc(page,scenarios,failures,"7","Explore → Search",s7)

        async def s8():
            await page.goto(URL, wait_until="domcontentloaded"); await page.wait_for_timeout(1500); await seed_vars(page)
            stuck=0
            for i in range(25):
                await do_search(page); await settled(page,2200); await to_setup(page); await settled(page,2200)
                s=await state(page); bad=(not s["explore"]) and (s["builderFlipHidden"] or s["builderOp"]<0.5)
                if bad: stuck+=1
                stress_log.append({"cycle":i+1,"stuck":bad,**s})
            await snap(page,"08_after_25_cycles.png")
            return {"status":"PASS" if stuck==0 else "FAIL","detail":f"{stuck}/25 stuck","stuck_count":stuck}
        await run_sc(page,scenarios,failures,"8","Repeated open/close (25×)",s8)

        async def s9():
            await do_search(page); await settled(page)
            for _ in range(12):
                try: await page.click("#bottle", timeout=500)
                except Exception: pass
                await page.wait_for_timeout(80)
            await settled(page,2500); s=await state(page); await snap(page,"09_after_rapid_clicks.png")
            bad=s["builderFlipHidden"] and not s["explore"]
            return {"status":"PASS" if not bad else "FAIL","detail":s}
        await run_sc(page,scenarios,failures,"9","Rapid bottle clicks",s9)

        async def s10():
            await page.set_viewport_size({"width":390,"height":844}); await seed_vars(page); await page.wait_for_timeout(400)
            await snap(page,"10_mobile_search.png"); await do_search(page); await page.wait_for_timeout(800)
            await snap(page,"10_mobile_mid_flip.png"); await settled(page,1400); await snap(page,"10_mobile_explore.png")
            await to_setup(page); await settled(page); s=await state(page); await snap(page,"10_mobile_search_restored.png")
            await page.set_viewport_size({"width":1440,"height":900})
            return {"status":"PASS" if s["builderOp"]>=0.9 and not s["explore"] else "FAIL","detail":s}
        await run_sc(page,scenarios,failures,"10","Mobile viewport (390×844)",s10)

        async def s11():
            await seed_vars(page); await do_search(page); await page.wait_for_timeout(500)
            await snap(page,"11_pre_resize_mid_flip.png"); await page.set_viewport_size({"width":1200,"height":700})
            await page.wait_for_timeout(300); await snap(page,"11_during_resize.png"); await settled(page,2000)
            s=await state(page); await snap(page,"11_after_resize_settled.png"); await page.set_viewport_size({"width":1440,"height":900})
            return {"status":"PASS" if s["explore"] and s["bottleRevealed"] else "FAIL","detail":s}
        await run_sc(page,scenarios,failures,"11","Resize mid-transition",s11)
        await browser.close()

    fail_count=sum(1 for s in scenarios if s["status"]!="PASS")
    recommendation="READY FOR HUMAN QA" if fail_count==0 else ("NOT READY FOR HUMAN QA" if fail_count>2 else "CONDITIONAL — fix noted failures then human QA")
    data={"meta":{"audit":"MOTION-QA-1-CORRECTED","corrects":"Prior report audited map_CURRENT.html; canonical target is map_SANDBOX_genie_v7.html","url":URL,"file_url":f"file://{ROOT/MAP}","base":BASE,"timestamp":utc_now(),"desktop_viewport":{"width":1440,"height":900},"mobile_viewport":{"width":390,"height":844},"auth":"none (sandbox embedded PROFILE)","screenshot_count":len(list(SHOT_DIR.glob('*.png')))},"scenarios":scenarios,"failures":failures,"stress_cycle_log":stress_log,"console_errors":console_errors,"wrong_map_note":{"incorrect_prior_target":"map_CURRENT.html","correct_target":MAP},"recommendation":recommendation}
    DATA_PATH.write_text(json.dumps(data,indent=2))
    print(json.dumps({"recommendation":recommendation,"failures":fail_count,"pass":len(scenarios)-fail_count},indent=2))

if __name__=="__main__": asyncio.run(main())
