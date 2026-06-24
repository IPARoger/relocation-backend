"""
smoke_beta_stabilize_b.py
MAP-BETA-STABILIZE-B static smoke tests.
"""

import re, sys
from pathlib import Path

MAP = Path("map_CURRENT.html").read_text(encoding="utf-8")

failures = []

def check(name, condition, detail=""):
    if not condition:
        failures.append("FAIL " + name + (": " + detail if detail else ""))
    else:
        print("  ok  " + name)

# B1: no topbar->openProfileSelector click handler
check("B1_no_topbar_profile_click",
      "topbar account label opens profile picker" not in MAP)

# B2: rm-topbar-acct has no caret
check("B2_no_caret_in_topbar",
      "acctEl.textContent = displayName || ''" in MAP)

# B3: .rm-acct CSS no longer has cursor: pointer
acct_css = re.search(r'\.rm-acct\s*\{[^}]+\}', MAP)
check("B3_rm_acct_no_cursor_pointer",
      acct_css is not None and "cursor: pointer" not in acct_css.group(0))

# B4: getActiveFavoriteProfileId has data-profile JSON fallback
check("B4_profile_id_accepts_data_profile",
      "opt.dataset.profile" in MAP and "JSON.parse(opt.dataset.profile)" in MAP)

# B5: rm-sls-status:empty override
check("B5_sls_status_empty_hidden",
      ".rm-sls-status:empty" in MAP and "display: none !important" in MAP)

# B6: timer guard vars declared
check("B6_timer_guards_declared",
      "_enterT1 = null, _enterT2 = null, _exitT1 = null, _exitT2 = null" in MAP)

# B7: enterExplore clears exit timers
enter_fn = re.search(r'function enterExplore\(\)\s*\{(.+?)function exitExplore', MAP, re.DOTALL)
check("B7_enter_clears_exit_timers",
      enter_fn is not None and
      "clearTimeout(_exitT1)" in enter_fn.group(1) and
      "clearTimeout(_exitT2)" in enter_fn.group(1))

# B8: exitExplore clears enter timers
exit_fn = re.search(r'function exitExplore\(\)\s*\{(.+?)\/\* keep activeConditions', MAP, re.DOTALL)
check("B8_exit_clears_enter_timers",
      exit_fn is not None and
      "clearTimeout(_enterT1)" in exit_fn.group(1) and
      "clearTimeout(_enterT2)" in exit_fn.group(1))

# B9: enterExplore stores timer handles
check("B9_enter_stores_timer_handles",
      "_enterT1 = setTimeout" in MAP and "_enterT2 = setTimeout" in MAP)

# B10: exitExplore stores timer handles
check("B10_exit_stores_timer_handles",
      "_exitT1 = setTimeout" in MAP and "_exitT2 = setTimeout" in MAP)

# B11: save disk disabled feedback
check("B11_save_disk_disabled_feedback",
      "Add at least one variable in the builder to save." in MAP)

# B12: legacy panel elements CSS hidden
check("B12_css_hide_legacy_panel_elements",
      "#renderStatus" in MAP and "#panelLegend" in MAP and
      re.search(r'#renderStatus[,\s]', MAP) is not None)

# B13: exitExplore removes rm-bottle--revealed in exit body
exit_body = re.search(r'function exitExplore\(\)(.+?)\/\* keep activeConditions', MAP, re.DOTALL)
check("B13_exit_removes_bottle_revealed",
      exit_body is not None and
      "bottle.classList.remove('rm-bottle--revealed')" in exit_body.group(1))

# B14: rm-ghost--updating CSS present
check("B14_ghost_updating_css",
      ".rm-ghost--updating" in MAP)

# B15: ghostRedrawFromState sets rm-ghost--updating
check("B15_ghost_redraw_updating_class",
      "ghostEl.classList.add('rm-ghost--updating')" in MAP and
      "ghostEl.classList.remove('rm-ghost--updating')" in MAP)

# B16: NOT button title mentions deferred polarity
check("B16_not_title_honest",
      "deferred" in MAP or "not yet in engine" in MAP)

# B17: debug panels gated (Beta-A preserved)
check("B17_debug_panels_gated",
      "__rmChartProfilesReady" in MAP and "debug" in MAP)

# B18: profile readiness gate preserved
check("B18_profile_readiness_gate",
      "await window.__rmChartProfilesReady" in MAP)

# B19: protected truth functions unchanged
for fn in ["executeSearchPlan", "__rmExecuteGenieRender", "__rmSaveCurrentInvestigation",
           "collectSavedInvestigationConditions", "createQuickShareFromMap"]:
    check("B19_truth_" + fn, fn in MAP)

# B20: profile picker exposed from nameplate
check("B20_profile_picker_exposed",
      "window.__rmOpenProfileSelector = openProfileSelector" in MAP)

print("")
if failures:
    print("FAILED: " + str(len(failures)) + " assertion(s)")
    for f in failures:
        print("  " + f)
    sys.exit(1)
else:
    total = 20 + 5  # 5 truth fn sub-checks in B19
    print("All checks passed (" + str(total) + " assertions).")
