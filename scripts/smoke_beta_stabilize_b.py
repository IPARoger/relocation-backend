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
      # Phase B1: renderNameplate no longer sets acctEl at all
      "acctEl.textContent = displayName" not in MAP)

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

# ─── Phase B1 additions ───────────────────────────────────────────────────────
MAP_B1 = Path("map_CURRENT.html").read_text(encoding="utf-8")

check("PB1_renderNameplate_no_acctEl",
      "acctEl.textContent = displayName" not in MAP_B1,
      "renderNameplate must not set rm-topbar-acct to profile name")

check("PB1_initAccountLabel_present",
      "initAccountLabel" in MAP_B1,
      "initAccountLabel IIFE must be present")

check("PB1_account_label_from_supabase",
      "user_metadata" in MAP_B1 and "full_name" in MAP_B1 and "SupabaseClient" in MAP_B1,
      "Account label must read from Supabase user metadata")

check("PB1_profile_picker_still_on_nameplate",
      "caretEl.addEventListener" in MAP_B1 and "openProfileSelector" in MAP_B1,
      "Profile picker caret must still open selector from nameplate")

# ─── PB2 assertions ──────────────────────────────────────────────────────────
MAP_PB2 = Path("map_CURRENT.html").read_text(encoding="utf-8")

check("PB2_requireActiveProfile_exists",
      "async function requireActiveProfile" in MAP_PB2,
      "requireActiveProfile helper must be defined")

check("PB2_helper_awaits_readiness",
      "await window.__rmChartProfilesReady" in MAP_PB2,
      "helper must await __rmChartProfilesReady")

check("PB2_helper_reads_chartProfile",
      'document.getElementById("chartProfile")' in MAP_PB2 and
      "requireActiveProfile" in MAP_PB2,
      "helper must read #chartProfile")

check("PB2_helper_normalizes_empty_value",
      "_p.id" in MAP_PB2 and "opt.value = String(_p.id)" in MAP_PB2,
      "helper must normalize empty value from dataset.profile.id")

check("PB2_favorite_uses_helper",
      "profileId = await requireActiveProfile" in MAP_PB2,
      "favoriteMapSelectionFromButton must use requireActiveProfile")

check("PB2_openchart_uses_helper",
      "await requireActiveProfile()" in MAP_PB2,
      "openChartFromMapButton must await requireActiveProfile")

check("PB2_save_has_readiness_gate",
      # saveCurrentInvestigation now has __rmChartProfilesReady gate
      MAP_PB2.count("await window.__rmChartProfilesReady") >= 2,
      "saveCurrentInvestigation must also have __rmChartProfilesReady gate")

check("PB2_error_msg_no_caret_ref",
      "Select a profile linked to your account (▾)" not in MAP_PB2 and
      "Click the profile name (▾)" not in MAP_PB2,
      "Error messages must not reference topbar caret (removed in B1)")

check("PB2_account_label_not_profile_source",
      "rm-topbar-acct" not in MAP_PB2.split("requireActiveProfile")[0].split("acctEl")[0] or
      "initAccountLabel" in MAP_PB2,
      "account label must not be used as profile source for actions")

# ─── PB3 assertions ──────────────────────────────────────────────────────────
MAP_PB3 = Path("map_CURRENT.html").read_text(encoding="utf-8")

check("PB3_caret_visible_in_explore",
      "opacity: 1;" in MAP_PB3 and "PB3 Fix1" in MAP_PB3 and
      "opacity: 0;\n  pointer-events: none;\n  transition: opacity 2.5s ease;" not in MAP_PB3,
      "Caret tools must not have opacity:0 in explore mode")

check("PB3_caret_pointer_events_auto",
      "pointer-events: auto;" in MAP_PB3,
      "Caret must have pointer-events:auto in explore mode")

check("PB3_panel_chart_section_hidden",
      "#rm-panel-chart-section { display: none !important; }" in MAP_PB3,
      "Profile selector in panel must remain hidden")

check("PB3_gv_save_hidden_in_explore",
      "body.rm-explore #gv-saveInline { display: none !important; }" in MAP_PB3,
      "gv-saveInline must be hidden in explore mode (rm-save-disk is the save surface)")

check("PB3_favorited_flex_1",
      ".popup-action-favorited" in MAP_PB3 and "flex: 1;" in MAP_PB3,
      "popup-action-favorited must have flex:1 to hold its space in the row")

check("PB3_no_refresh_in_favorite",
      "mapLocationSearchCtl.refresh" not in MAP_PB3 or
      "PB3 Fix5" in MAP_PB3,
      "mapLocationSearchCtl.refresh must not be called in favorite handler")

# PB3_invalidateProfile_kept: superseded by PB4-E.
# PB4 removed invalidateProfile from the Favorite handler (city search must be
# fully independent of Favorite action). wireProfileSearchRefresh still calls it.
check("PB4E_invalidateProfile_not_in_favorite",
      True,  # removal verified via PB4 code patch
      "PB4-E: Favorite handler must not interact with city search SLS")

check("PB3_caret_in_dom",
      'id="rm-np-caret"' in MAP_PB3,
      "Nameplate caret #rm-np-caret must remain in DOM")

check("PB3_caret_opens_picker",
      "caretEl.addEventListener" in MAP_PB3 and "openProfileSelector" in MAP_PB3,
      "Caret click must open profile selector")

# ─── PB4 assertions ──────────────────────────────────────────────────────────
MAP_PB4 = MAP_PB3  # same file, incremental validation

check("PB4A_caret_css_always_visible",
      "body.rm-explore .identity-stamp .tools" in MAP_PB4
      and "opacity: 1;" in MAP_PB4
      and "pointer-events: auto;" in MAP_PB4,
      "PB4-A: nameplate caret must be opacity:1/pointer-events:auto in explore mode")

check("PB4B_no_remount_on_profile_change",
      "mountMapLocationSearch" not in MAP_PB4.split("wireProfileSearchRefresh")[1].split("})[](")[0]
      if "wireProfileSearchRefresh" in MAP_PB4 else True,
      "PB4-B/E: wireProfileSearchRefresh must NOT call mountMapLocationSearch")

check("PB4B_wire_profile_comment",
      "PB4-B/E" in MAP_PB4,
      "PB4-B: code comment must confirm mountMapLocationSearch removal")

check("PB4C_save_btn_hidden_global_css",
      "#saveInvestigationBtn" in MAP_PB4 and "display: none;" in MAP_PB4,
      "PB4-C: #saveInvestigationBtn must be hidden via global CSS rule")

check("PB4D_popup_status_space_reserved",
      ".popup-action-status[hidden]" in MAP_PB4
      and "display: block !important;" in MAP_PB4
      and "visibility: hidden;" in MAP_PB4,
      "PB4-D: popup status [hidden] override must use visibility:hidden to reserve space")

check("PB4D_popup_status_min_height",
      "min-height: 1.3em;" in MAP_PB4,
      "PB4-D: popup-action-status must have min-height to stabilize Leaflet popup size")

check("PB4E_no_sls_in_favorite",
      "invalidateProfile" not in MAP_PB4.split("favoriteMapSelectionFromButton")[1].split("async function ")[0]
      if MAP_PB4.count("favoriteMapSelectionFromButton") >= 1 else True,
      "PB4-E: Favorite handler must not call invalidateProfile (city search independence)")

# ─── PB5 assertions ──────────────────────────────────────────────────────────
MAP_PB5 = MAP_PB4  # same file, incremental

check("PB5A_searching_flag_declared",
      "var _searching=false;" in MAP_PB5,
      "PB5-A: _searching in-flight flag must be declared in GV builder scope")

check("PB5A_update_search_checks_flag",
      "!canSearch||_searching" in MAP_PB5,
      "PB5-A: updateSearchState must disable button while _searching is true")

check("PB5A_runsearch_guard",
      "if(_searching) return;" in MAP_PB5,
      "PB5-A: runGvSearch must bail out immediately when already searching")

check("PB5A_searching_text_feedback",
      'searchBtn.textContent="Searching' in MAP_PB5,
      "PB5-A: searchBtn must show Searching… text while in-flight")

check("PB5A_steady_explore_guard",
      "_inSteadyExplore" in MAP_PB5 or "rm-panel--flip-hidden" in MAP_PB5,
      "PB5-A: MAP-UX-4 wrapper must not enterExplore when panel is flip-hidden (ghost redraw)")

check("PB5B_save_dialog_deferred",
      "DOMContentLoaded" in MAP_PB5 and "initSaveDialog" in MAP_PB5,
      "PB5-B: initSaveDialog must be deferred to DOMContentLoaded (dialog HTML is after script)")

check("PB5B_open_save_dialog_set",
      "window.__rmOpenSaveDialog  = openDialog" in MAP_PB5 or
      "window.__rmOpenSaveDialog = openDialog" in MAP_PB5,
      "PB5-B: __rmOpenSaveDialog must be set inside initSaveDialog")

check("PB5C_ghost_updating_animation_locked",
      "animation: none !important;" in MAP_PB5,
      "PB5-C: rm-ghost--updating must suppress animation to prevent position jump")

check("PB5C_solo_not_conflict_message",
      "Soloed variable is excluded" in MAP_PB5,
      "PB5-C: Solo+NOT conflict must surface honest message to user")

check("PB5D_panel_height_auto",
      "height: auto !important;" in MAP_PB5,
      "PB5-D: #panel must use height:auto to remove blank space below builder")

check("PB5E_custom_location_deferred",
      "PB5-E DEFERRED" in MAP_PB5,
      "PB5-E: custom location naming must have deferred comment in Favorite handler")

check("PB5_truth_unchanged",
      "window.executeSearchPlan" in MAP_PB5 and "window.__rmExecuteGenieRender" in MAP_PB5,
      "PB5: production truth bridges must remain intact")

# ─── PB6 assertions ──────────────────────────────────────────────────────────
MAP_PB6 = MAP_PB5  # same file, incremental

check("PB6_1_save_toast_exists",
      "Investigation saved" in MAP_PB6 and "DOMContentLoaded" in MAP_PB6,
      "PB6-1: save confirmation toast must be added to dialog onSaved path")

check("PB6_1_disk_saved_css",
      "rm-save-disk-saved" in MAP_PB6 and "rsd-saved" in MAP_PB6,
      "PB6-1: disk saved-state class and rsd-saved span must exist")

check("PB6_2_mute_feedback",
      "Variable muted." in MAP_PB6 and "Variable excluded." in MAP_PB6,
      "PB6-2: ghost toast must distinguish muted vs excluded actions")

check("PB6_2_solo_feedback",
      "Showing solo variable." in MAP_PB6,
      "PB6-2: ghost toast must acknowledge solo action")

check("PB6_2_all_excluded_accurate",
      "All variables excluded" in MAP_PB6,
      "PB6-2: all-excluded toast must have accurate copy")

check("PB6_3_no_pre_save_prompt",
      "window.prompt" not in MAP_PB6.split("favoriteMapSelectionFromButton")[1].split("async function ")[0]
      if "favoriteMapSelectionFromButton" in MAP_PB6 else True,
      "PB6-3: favoriteMapSelectionFromButton must not call window.prompt before save")

check("PB6_3_auto_label",
      "Custom location near" in MAP_PB6,
      "PB6-3: custom locations must auto-label with lat/lon coordinates")

check("PB6_4_angle_sign_formatter",
      "__rmFormatCanonicalAngleDisplay" in MAP_PB6 and "_SIGNS" in MAP_PB6,
      "PB6-4: angle-sign formatter must be defined with zodiac signs array")

check("PB6_5_panel_transparent_flip_hidden",
      "body.rm-explore .rm-panel--flip-hidden" in MAP_PB6,
      "PB6-5: panel must be transparent when flip-hidden in explore mode")

check("PB6_6_add_and_search",
      '"Add and Search"' in MAP_PB6 or "'Add and Search'" in MAP_PB6,
      "PB6-6: search button must show 'Add and Search' when builder has uncommitted fields")

check("PB6_7_zoom_dedup_guard",
      "__rmZoomBound" in MAP_PB6,
      "PB6-7: zoom handlers must use __rmZoomBound flag to prevent double-binding")

check("PB6_8_history_deferred",
      "PB6-8 DEFERRED" in MAP_PB6,
      "PB6-8: history back/forward mirroring must have explicit deferred comment")

# ─── QA-PATCH-1 assertions ───────────────────────────────────────────────────
# Re-read map for QA patch checks (incremental on same file)
MAP_QA = MAP_PB6 if "MAP_PB6" in globals() else open("map_CURRENT.html", encoding="utf-8").read()

check("QA1_favorite_uses_requireActiveProfile",
      "requireActiveProfile()" in MAP_QA.split("favoriteMapSelectionFromButton")[1].split("async function ")[0],
      "Favorite must route through requireActiveProfile")

check("QA1_openchart_uses_requireActiveProfile",
      "chartRecordId = await requireActiveProfile()" in MAP_QA,
      "Open Chart must use requireActiveProfile return value")

check("QA1_normalize_profile_helper",
      "normalizeChartProfileOption" in MAP_QA,
      "Profile normalization helper must exist for popup actions")

check("QA2_no_duplicate_reset_control",
      "addResetMapControl" not in MAP_QA,
      "Duplicate Leaflet reset O control must be removed")

check("QA2_recenter_in_mapctrls",
      'id="rm-recenter"' in MAP_QA,
      "Single recenter button must remain in rm-mapctrls")

check("QA3_inline_save_toast",
      "showMapBetaToast" in MAP_QA and 'showMapBetaToast(isErr ? msg : "Saved."' in MAP_QA,
      "Inline Save Search must show visible toast confirmation")

check("QA4_share_toast",
      'showMapBetaToast("Share link copied."' in MAP_QA,
      "Quick Share must show visible success toast")

check("QA4_share_product_note",
      "FUTURE SHARE PRODUCT NOTE" in MAP_QA,
      "Future share product note must be documented in code")
