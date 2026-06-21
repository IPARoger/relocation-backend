#!/usr/bin/env python3
"""Smoke: comparison set backend ownership (POST /comparison-sets/create|archive).

Backend:
  * create set + places (places need not be favorites)
  * archive + idempotent archive
  * invalid profile / place -> 404
  * cross-account -> 404
  * unauthenticated -> 401

Frontend (app_shell.html):
  * build comparison from favorites picker
  * compare screen opens with new set
  * archive from chart-record module
  * compare screen safe after archive (recovery)
  * in-memory updates, no reload, no console errors

Run:
  set -a && source .env.staging && set +a
  ./venv/bin/python scripts/smoke_comparison_sets.py
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PYTHON = ROOT / "venv" / "bin" / "python"
DEFAULT_EMAIL = "davidleongoodman@gmail.com"
PORT = 8004

# PIH-QA-FIX-1: scoped Screen 4 row extractors — never use unscoped table.simple for PIH.
PIH_ROW_EXTRACT_JS = """(planet) => {
  const root = document.getElementById('rm-screen4-facts');
  const table = root && root.querySelector('.rm-pih-table[data-pih-source="canonical_chart"]');
  if (!table) return null;
  const row = Array.from(table.querySelectorAll('tr')).find(
    (tr) => tr.cells[0] && tr.cells[0].textContent.trim() === planet
  );
  if (!row) return null;
  return Array.from(row.cells).map((td) => td.textContent.trim());
}"""

A2A_ROWS_FOR_PLANET_JS = """(planet) => {
  const root = document.getElementById('rm-screen4-facts');
  const table = root && root.querySelector('.rm-a2a-table[data-a2a-source="canonical_chart"]');
  if (!table) return [];
  return Array.from(table.querySelectorAll('tr'))
    .filter((tr) => tr.cells[0] && tr.cells[0].textContent.trim() === planet)
    .map((tr) => Array.from(tr.cells).map((td) => td.textContent.trim()));
}"""



def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def fetch(base, path, headers=None, method="GET", body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    hdrs = dict(headers or {})
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{base}{path}", headers=hdrs, method=method, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()


def state_route_present(base):
    try:
        st, _ = fetch(base, "/comparison-sets/state", method="POST",
                      body={"profile_id": "x", "comparison_set_id": "y", "settings_snapshot_json": {}}, timeout=3)
    except Exception:
        return False
    return st == 401


def route_present(base):
    try:
        st, _ = fetch(base, "/comparison-sets/create", method="POST",
                      body={"profile_id": "x", "place_ids": ["a", "b"]}, timeout=3)
    except Exception:
        return None
    return st == 401


def port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) != 0


def wait_health(base, timeout_s=25.0):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base + "/health", timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def resolve_ctx(url, anon, svc):
    from supabase import create_client
    anon_client = create_client(url, anon)
    email = os.environ.get("RM_SMOKE_EMAIL", DEFAULT_EMAIL).strip()
    admin = create_client(url, svc)
    link = admin.auth.admin.generate_link({"type": "magiclink", "email": email})
    res = anon_client.auth.verify_otp(
        {"token_hash": link.properties.hashed_token, "type": "magiclink"}
    )
    if not res.session:
        fail(f"could not authenticate {email}")
    token = res.session.access_token
    anon_client.postgrest.auth(token)
    account_ids = anon_client.rpc("app_account_ids").execute().data or []
    if not account_ids:
        fail("no account for smoke user")
    return token, account_ids[0], res


def cmp_places(admin, set_id):
    return (
        admin.table("comparison_set_places")
        .select("place_id, sort_order")
        .eq("comparison_set_id", set_id)
        .order("sort_order")
        .execute()
    ).data or []


def ensure_two_favorites(admin, account_id, profile_id, stamp):
    """Return two place_ids with active favorites for frontend picker (admin setup only)."""
    favs = (
        admin.table("favorite_places")
        .select("place_id")
        .eq("account_id", account_id)
        .eq("profile_id", profile_id)
        .is_("archived_at", "null")
        .limit(5)
        .execute()
    ).data or []
    ids = [f["place_id"] for f in favs if f.get("place_id")]
    created_place_ids = []
    while len(ids) < 2:
        pid = (
            admin.table("places").insert({
                "display_name": f"Smoke Cmp Fav {stamp}-{len(ids)}",
                "latitude": 10.0 + len(ids), "longitude": 20.0 + len(ids),
                "provider": "map_custom", "country_code": "ZZ",
            }).execute()
        ).data[0]["id"]
        created_place_ids.append(pid)
        admin.table("favorite_places").insert({
            "account_id": account_id, "profile_id": profile_id,
            "place_id": pid, "label": f"Smoke fav {len(ids)}",
        }).execute()
        ids.append(pid)
    return ids[:2], created_place_ids









def static_pih_qa_selector_checks(script_path: Path) -> list[tuple[str, bool, str]]:
    """PIH-QA-FIX-1: forbid unscoped table.simple PIH reads in smoke scripts."""
    text = script_path.read_text(encoding="utf-8")
    out: list[tuple[str, bool, str]] = []
    out.append(("static_pih_qa_scoped_extractors",
                "PIH_ROW_EXTRACT_JS" in text
                and "rm-pih-table" in text
                and 'data-pih-source="canonical_chart"' in text,
                "PIH_ROW_EXTRACT_JS scopes to rm-pih-table"))
    out.append(("static_pih_qa_a2a_scoped_extractors",
                "A2A_ROWS_FOR_PLANET_JS" in text
                and "rm-a2a-table" in text,
                "A2A_ROWS_FOR_PLANET_JS scopes to rm-a2a-table"))
    unscoped_pih = (
        "querySelectorAll('table.simple tr')" in text
        and "PIH_ROW_EXTRACT_JS" not in text.split("querySelectorAll('table.simple tr')")[0][-800:]
    )
    out.append(("static_pih_qa_no_unscoped_simple",
                "querySelectorAll('table.simple tr')" not in text
                or ("PIH_ROW_EXTRACT_JS" in text and not unscoped_pih),
                "no unscoped table.simple PIH row reads in smoke script"))
    return out


def static_pih_checks(shell_path: Path, map_path: Path) -> list[tuple[str, bool, str]]:
    """Static assertions for PHASE-2A PIH canonical migration."""
    shell = shell_path.read_text(encoding="utf-8")
    map_html = map_path.read_text(encoding="utf-8")
    start = shell.find("// PHASE-2A:")
    end = shell.find("// WHEEL-1:", start)
    block = shell[start:end] if start >= 0 and end > start else ""
    render_start = shell.find("function renderRelocatedChartHtml")
    render_end = shell.find("let _screen4Token = 0;", render_start)
    render_block = shell[render_start:render_end] if render_start >= 0 else ""
    cmp_start = shell.find("function renderComparisonTableHtml")
    cmp_end = shell.find("// Comparison workspace reading-state", cmp_start)
    cmp_block = shell[cmp_start:cmp_end] if cmp_start >= 0 else ""
    out: list[tuple[str, bool, str]] = []
    out.append(("static_pih_canonical_source",
                'data-pih-source="canonical_chart"' in render_block,
                "Screen 4 PIH table attr"))
    out.append(("static_pih_no_planet_houses_in_render",
                "planet_houses" not in block
                and "planet_houses" not in render_block
                and "planet_houses" not in cmp_block,
                "no planet_houses in PIH render paths"))
    out.append(("static_comparison_angles_from_canonical",
                "renderComparisonAngleRowsHtml" in cmp_block
                and "getCanonicalChartFromPayload" in cmp_block
                and "c.chart.asc" not in cmp_block
                and "c.chart.mc" not in cmp_block
                and "planet_houses" not in cmp_block,
                "comparison angles from canonical_chart.angles"))
    out.append(("static_pih_helpers_exported",
                "__rmGetCanonicalChartFromPayload" in shell
                and "__rmFormatCanonicalAngleDisplay" in shell,
                "helpers on window for map"))
    out.append(("static_popup_canonical_planets",
                "getCanonicalChartFromPayloadLocal" in map_html
                and "cc.planets" in map_html
                and "data.planet_houses" not in map_html[map_html.find("function buildPlanetHouseRowsFromData"):map_html.find("function mapHumanPlaceLabel")],
                "popup PIH reads canonical_chart.planets"))
    return out

def static_wheel_checks(shell_path: Path) -> list[tuple[str, bool, str]]:
    """Static assertions for WHEEL-1 / WHEEL-v2 (no Playwright required)."""
    shell = shell_path.read_text(encoding="utf-8")
    start = shell.find("// WHEEL-1")
    end = shell.find("// A2A-1:", start)
    block = shell[start:end] if start >= 0 and end > start else ""
    out: list[tuple[str, bool, str]] = []
    out.append(("static_wheel_source_attr",
                'data-wheel-source="canonical_chart"' in block,
                "data-wheel-source on wheel wrap"))
    out.append(("static_wheel_reads_cusps",
                "houses.cusps_deg" in block,
                "reads houses.cusps_deg"))
    out.append(("static_wheel_reads_angles",
                "canonicalChart.angles" in block or "canonical_chart.angles" in block,
                "reads canonical_chart.angles"))
    out.append(("static_wheel_reads_planets",
                "canonicalChart.planets" in block,
                "reads canonical_chart.planets"))
    out.append(("static_wheel_reads_p2p_spokes",
                "canonicalChart.aspects_planet_to_planet" in block,
                "P2P spokes from canonical_chart.aspects_planet_to_planet"))
    out.append(("static_wheel_reads_motion_state",
                "entry.motion_state" in block,
                "retrograde/station from canonical_chart.planets.motion_state"))
    out.append(("static_wheel_no_client_aspect_math",
                "_compute_aspects_planet_to_planet" not in block
                and "separation_deg" not in block
                and "orb_limit_deg" not in block,
                "no client P2P aspect math in wheel block"))
    out.append(("static_wheel_no_swe",
                "swe." not in block and "Swiss" not in block,
                "no client swe"))
    out.append(("static_wheel_no_legacy_geometry",
                "planet_houses" not in block
                and "asc_deg" not in block
                and "mc_deg" not in block,
                "no legacy flat keys in wheel block"))
    out.append(("static_wheel_no_p2p_table",
                "planet-to-planet table" not in shell.lower(),
                "no separate P2P table/grid"))
    out.append(("static_wheel_screen4_order",
                "return meta + wheel + ais + a2a + planets" in shell,
                "Screen 4 section order"))
    return out




def static_motion_checks(shell_path: Path) -> list[tuple[str, bool, str]]:
    """WHEEL-v2: motion markers read canonical_chart.planets only (no client speed math)."""
    shell = shell_path.read_text(encoding="utf-8", errors="replace")
    wh_start = shell.find("// WHEEL-1")
    wh_end = shell.find("// A2A-1:", wh_start)
    block = shell[wh_start:wh_end] if wh_start >= 0 and wh_end > wh_start else ""
    out: list[tuple[str, bool, str]] = []
    out.append(("static_motion_wheel_reads_motion_state",
                "entry.motion_state" in block,
                "wheel reads planet.motion_state from canonical"))
    out.append(("static_motion_no_client_speed_math",
                "speed_deg_per_day" not in block,
                "no client speed computation in wheel block"))
    out.append(("static_motion_station_markers_in_wheel",
                "station_direct" in block and "station_retrograde" in block,
                "station states rendered in wheel block"))
    return out

def static_p2p_checks(shell_path: Path) -> list[tuple[str, bool, str]]:
    """WHEEL-v2: P2P spokes from canonical only — no client aspect math or tables."""
    shell = shell_path.read_text(encoding="utf-8")
    wh_start = shell.find("function renderRelocatedWheelSvg")
    wh_end = shell.find("function renderRelocatedWheelHtml", wh_start)
    wh_block = shell[wh_start:wh_end] if wh_start >= 0 and wh_end > wh_start else ""
    out: list[tuple[str, bool, str]] = []
    out.append(("static_p2p_spokes_from_canonical",
                "canonicalChart.aspects_planet_to_planet" in wh_block,
                "wheel draws spokes from canonical_chart.aspects_planet_to_planet"))
    out.append(("static_p2p_no_client_compute",
                "_compute_aspects_planet_to_planet" not in shell
                and "separation_deg" not in wh_block
                and "orb_limit_deg" not in wh_block,
                "no client P2P aspect math in wheel block"))
    out.append(("static_no_p2p_table",
                "planet-to-planet table" not in shell.lower(),
                "no P2P table/grid in app_shell"))
    return out

def static_a2a_checks(shell_path: Path) -> list[tuple[str, bool, str]]:
    """Static assertions for A2A-1 (no Playwright required)."""
    shell = shell_path.read_text(encoding="utf-8")
    start = shell.find("// A2A-1:")
    end = shell.find("function renderRelocatedChartHtml", start)
    block = shell[start:end] if start >= 0 and end > start else ""
    out: list[tuple[str, bool, str]] = []
    out.append(("static_a2a_placeholder_removed",
                "Aspect-to-angle table content ships in a later slice" not in shell,
                "workbook placeholder removed"))
    out.append(("static_a2a_canonical_source_attr",
                'data-a2a-source="canonical_chart"' in block,
                "data-a2a-source on A2A tables"))
    out.append(("static_a2a_reads_aspects_to_angles",
                "aspects_to_angles" in block,
                "consumer reads aspects_to_angles"))
    out.append(("static_a2a_cache_workbook",
                "_comparisonColsCache" in block and "refreshA2aWorkbookSection" in shell,
                "comparison uses _comparisonColsCache"))
    out.append(("static_a2a_no_longitude_math",
                "longitude_deg" not in block and "swe." not in block,
                "no client longitude aspect math in A2A block"))
    out.append(("static_a2a_no_settings_refilter",
                "filterA2aRowsForLocalSettings" not in block
                and "aspectsToAnglesForDisplay" in block,
                "no client settings drift filter on A2A rows"))
    return out


def static_settings_final_wire_checks(shell_path: Path) -> list[tuple[str, bool, str]]:
    """SETTINGS-FINAL-WIRE-1 static honesty + rehydrate assertions."""
    shell = shell_path.read_text(encoding="utf-8")
    out: list[tuple[str, bool, str]] = []
    out.append(("static_final_wire_rehydrate",
                "rehydrateSettingsConsumers" in shell and "applyAccountSettingsPatch" in shell,
                "settings save rehydrates consumers"))
    out.append(("static_final_wire_restore",
                "restore-astrology-defaults" in shell and "buildAstrologyDefaultsRestorePatch" in shell,
                "restore defaults control"))
    oos_chunk = shell.split('id="rm-settings-oos-aspects"', 1)
    oos_enabled = len(oos_chunk) > 1 and "disabled aria-disabled" not in oos_chunk[1][:220]
    out.append(("static_final_wire_oos_live", oos_enabled, "out-of-sign is an active control"))
    out.append(("static_final_wire_subsequent_disabled",
                "rm-settings-subsequent-house-enabled" not in shell,
                "subsequent-house misleading checkbox removed"))
    out.append(("static_final_wire_orbs_copy",
                "when those renderers are live" not in shell,
                "chart display orb copy updated"))
    out.append(("static_final_wire_a2a_copy",
                "ship in a later slice" not in shell,
                "A2A angle copy updated"))
    return out



def static_diffs_mvp_checks(shell_path: Path) -> list[tuple[str, bool, str]]:
    """DIFFS-MVP-1: comparison cell-level diff mode."""
    shell = shell_path.read_text(encoding="utf-8")
    out: list[tuple[str, bool, str]] = []
    out.append(("static_diffs_toggle",
                'data-action="toggle-cmp-diffs"' in shell and "setDiffsEnabled" in shell,
                "Diffs toggle wired"))
    out.append(("static_diffs_identical_class",
                "rm-cmp-diff-identical" in shell and "cmpDiffTdClass" in shell,
                "identical cell fade class"))
    out.append(("static_diffs_pih_ais_a2a",
                "pihHouseDiffKey" in shell and "aisAngleDiffKey" in shell and "a2aCellDiffKey" in shell,
                "PIH AIS A2A diff keys"))
    out.append(("static_diffs_reference_column",
                "referencePlaceId" in shell and "resolveVisibleOrderedPlaceIds" in shell,
                "first visible column reference"))
    out.append(("static_diffs_no_p2p",
                "aspects_planet_to_planet" not in shell.split("buildComparisonDiffContext", 1)[0]
                or "p2p" not in shell[shell.find("buildComparisonDiffContext"):shell.find("buildComparisonDiffContext") + 800].lower(),
                "no P2P in diff helpers"))
    out.append(("static_diffs_no_summary_panel",
                "diff-summary" not in shell.lower() and "diffSummary" not in shell,
                "no summary panel"))
    bad = ("improved", "better", "worse", "stronger", "ranking")
    diff_chunk = shell[shell.find("DIFFS-MVP-1"):shell.find("DIFFS-MVP-1") + 4500] if "DIFFS-MVP-1" in shell else ""
    out.append(("static_diffs_no_interpretive_language",
                not any(w in diff_chunk.lower() for w in bad),
                "no ranking/interpretive copy in diff block"))
    return out


def static_dignities_house_checks(shell_path: Path, onto_path: Path) -> list[tuple[str, bool, str]]:
    """DIGNITIES-HOUSE-1 static wiring checks."""
    shell = shell_path.read_text(encoding="utf-8")
    onto = onto_path.read_text(encoding="utf-8")
    out: list[tuple[str, bool, str]] = []
    out.append(("static_dh_lookup_export", "lookupFamilyByHouse" in onto, "ontology export"))
    out.append(("static_dh_pih_house", "lookupFamilyByHouse(planet, house)" in shell, "PIH uses house"))
    cell_chunk = shell.split("function pihHouseCellHtml", 1)[1].split("function pihDignitiesFooterHtml", 1)[0]
    out.append(("static_dh_no_sign_in_cell", "pihSignFromPlanetInfo" not in cell_chunk, "no sign dignity in cell"))
    out.append(("static_dh_help", "rm-pih-dignities-help" in shell, "? help"))
    out.append(("static_dh_no_diff", "dignityDiff" not in shell, "no dignity diff"))
    return out

def wheel_v2_pih_crosscheck(page, profile_id: str, locations: list[tuple[str, dict]], expected: dict[str, int]) -> list[tuple[str, bool, str]]:
    """Playwright: Sun house from .rm-pih-table only (PIH-QA-FIX-1)."""
    out: list[tuple[str, bool, str]] = []
    for key, place in locations:
        page.evaluate(
            "(args)=>window.__rmAppShell.navigate('chart',{chartRecordId:args.pid,placeId:args.placeId})",
            {"pid": profile_id, "placeId": place["id"]},
        )
        page.wait_for_selector(
            '#rm-screen4-facts .rm-pih-table[data-pih-source="canonical_chart"]',
            timeout=120000,
        )
        page.wait_for_timeout(1500)
        row = page.evaluate(PIH_ROW_EXTRACT_JS, "Sun")
        house = row[1] if row and len(row) > 1 else None
        exp = expected.get(key)
        ok = str(house) == str(exp)
        out.append((f"fe_pih_sun_house_{key}", ok, f"displayed={house} expected={exp} row={row}"))
        a2a = page.evaluate(A2A_ROWS_FOR_PLANET_JS, "Sun")
        out.append((f"fe_pih_not_a2a_contamination_{key}",
                    not row or (len(row) == 3 and house not in ("Conjunction", "Opposition", "Square", "Trine", "Sextile")),
                    f"pih_cols={len(row) if row else 0} a2a_sun_rows={len(a2a)}"))
    return out


def resolve_wheel_v2_qa_locations(admin, account_id: str, profile_id: str) -> list[tuple[str, dict]]:
    """Kansas City (current), favorite custom, comparison city — same fixtures as WHEEL-v2 QA."""
    def place_row(pid):
        return admin.table("places").select("id,display_name,latitude,longitude").eq("id", pid).single().execute().data

    fav_rows = admin.table("favorite_places").select("place_id").eq("account_id", account_id).is_("archived_at", "null").order("rank").execute().data or []
    current_row = admin.table("current_location_history").select("place_id").eq("profile_id", profile_id).eq("is_current", True).limit(1).execute().data
    current = place_row(current_row[0]["place_id"])
    fav = place_row(next((f["place_id"] for f in fav_rows if f["place_id"] != current["id"]), fav_rows[0]["place_id"]))
    cs = admin.table("comparison_sets").select("id").eq("account_id", account_id).is_("archived_at", "null").limit(1).execute().data
    cmp_places = admin.table("comparison_set_places").select("place_id").eq("comparison_set_id", cs[0]["id"]).order("sort_order").execute().data
    cmp = place_row(next((r["place_id"] for r in cmp_places if r["place_id"] not in {current["id"], fav["id"]}), cmp_places[0]["place_id"]))
    return [
        ("current_kansas_city", current),
        ("favorite_city", fav),
        ("comparison_city", cmp),
    ]


def main() -> int:
    url = os.environ.get("SUPABASE_URL", "")
    anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not all([url, anon_key, service_key]):
        fail("Set SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY")

    from supabase import create_client
    admin = create_client(url, service_key)

    proc = None
    base = f"http://127.0.0.1:{PORT}"
    present = route_present(base)
    state_ok = state_route_present(base) if present is True else False
    need_temp = present is not True or not state_ok
    if need_temp:
        if present is False:
            fail(f"port {PORT} serving build without /comparison-sets/create")
        port = PORT if port_free(PORT) else next((p for p in (8041, 8042, 8043) if port_free(p)), None)
        if port is None:
            fail("no free port for temp server")
        base = f"http://127.0.0.1:{port}"
        proc = subprocess.Popen(
            [str(PYTHON), "-m", "uvicorn", "main_centerline_FIXER:app",
             "--host", "127.0.0.1", "--port", str(port)],
            cwd=str(ROOT), env=dict(os.environ),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if not wait_health(base):
            proc.terminate()
            fail(f"temp server did not start on {base}")

    results = []
    results.extend(static_pih_qa_selector_checks(ROOT / "scripts" / "smoke_comparison_sets.py"))
    results.extend(static_pih_checks(ROOT / "app_shell.html", ROOT / "map_CURRENT.html"))
    results.extend(static_wheel_checks(ROOT / "app_shell.html"))
    results.extend(static_p2p_checks(ROOT / "app_shell.html"))
    results.extend(static_motion_checks(ROOT / "app_shell.html"))
    results.extend(static_a2a_checks(ROOT / "app_shell.html"))
    results.extend(static_settings_final_wire_checks(ROOT / "app_shell.html"))
    results.extend(static_diffs_mvp_checks(ROOT / "app_shell.html"))
    results.extend(static_dignities_house_checks(ROOT / "app_shell.html", ROOT / "dignity_ontology.js"))

    created_set_ids = []
    created_place_ids = []
    created_fav_place_ids = []
    profile_id = None
    stamp = uuid.uuid4().hex[:8]
    try:
        jwt, account_id, sess = resolve_ctx(url, anon_key, service_key)
        headers = {"Authorization": f"Bearer {jwt}"}

        profiles = (
            admin.table("profiles").select("id, display_name")
            .eq("account_id", account_id).is_("archived_at", "null")
            .order("created_at").limit(1).execute()
        ).data or []
        if not profiles:
            fail("no active profile")
        profile_id = profiles[0]["id"]

        # Two throwaway places — NOT favorites (backend must not require favorites)
        p1 = admin.table("places").insert({
            "display_name": f"Smoke Cmp A {stamp}", "latitude": 1.1, "longitude": 2.2,
            "provider": "map_custom", "country_code": "ZZ",
        }).execute().data[0]["id"]
        p2 = admin.table("places").insert({
            "display_name": f"Smoke Cmp B {stamp}", "latitude": 3.3, "longitude": 4.4,
            "provider": "map_custom", "country_code": "ZZ",
        }).execute().data[0]["id"]
        created_place_ids.extend([p1, p2])

        # create
        st, b = fetch(base, "/comparison-sets/create", headers=headers, method="POST",
                      body={"profile_id": profile_id, "place_ids": [p1, p2],
                            "title": f"Smoke comparison {stamp}"})
        created = json.loads(b) if st == 200 else {}
        set_id = created.get("id")
        if set_id:
            created_set_ids.append(set_id)
        rows = cmp_places(admin, set_id) if set_id else []
        results.append(("be_create_200",
                        st == 200 and created.get("status") == "created"
                        and created.get("place_ids") == [p1, p2] and len(rows) == 2,
                        f"status={st} id={set_id} places={len(rows)}"))



        # workspace state save
        sample_snapshot = {
            "comparison_workspace_state": {
                "schema_version": 1,
                "collapsed_sections": {"ais": True, "pih": False, "a2a": False, "city_intelligence": False, "notes": False},
                "visible_sections": {"ais": True, "pih": True, "a2a": True, "city_intelligence": True, "notes": True},
                "active_angle_tab": "mc",
                "diffs_enabled": False,
                "dignities_enabled": False,
                "interpretive_hints_enabled": False,
                "hidden_place_ids": [],
                "column_order_place_ids": [],
            }
        }
        st, b = fetch(base, "/comparison-sets/state", headers=headers, method="POST",
                      body={"profile_id": profile_id, "comparison_set_id": set_id,
                            "settings_snapshot_json": sample_snapshot})
        db_snap = (
            admin.table("comparison_sets").select("settings_snapshot_json")
            .eq("id", set_id).single().execute()
        ).data if set_id else None
        inner = ((db_snap or {}).get("settings_snapshot_json") or {}).get("comparison_workspace_state") or {}
        results.append(("be_state_200", st == 200 and inner.get("active_angle_tab") == "mc",
                        f"status={st} tab={inner.get('active_angle_tab')}"))
        st, _ = fetch(base, "/comparison-sets/state", method="POST",
                      body={"profile_id": profile_id, "comparison_set_id": set_id,
                            "settings_snapshot_json": sample_snapshot})
        results.append(("be_state_unauth_401", st == 401, f"status={st}"))

        # archive
        st, b = fetch(base, "/comparison-sets/archive", headers=headers, method="POST",
                      body={"comparison_set_id": set_id, "profile_id": profile_id})
        archived = json.loads(b) if st == 200 else {}
        results.append(("be_archive_200",
                        st == 200 and archived.get("status") == "archived"
                        and archived.get("archived_at"),
                        f"status={st} archived={archived.get('archived_at')}"))

        # idempotent archive
        st, b = fetch(base, "/comparison-sets/archive", headers=headers, method="POST",
                      body={"comparison_set_id": set_id})
        again = json.loads(b) if st == 200 else {}
        results.append(("be_archive_idempotent",
                        st == 200 and again.get("status") == "already_archived",
                        f"status={st} stat={again.get('status')}"))

        # invalid profile
        st, _ = fetch(base, "/comparison-sets/create", headers=headers, method="POST",
                      body={"profile_id": str(uuid.uuid4()), "place_ids": [p1, p2]})
        results.append(("be_invalid_profile_404", st == 404, f"status={st}"))

        # invalid place
        st, _ = fetch(base, "/comparison-sets/create", headers=headers, method="POST",
                      body={"profile_id": profile_id, "place_ids": [p1, str(uuid.uuid4())]})
        results.append(("be_invalid_place_404", st == 404, f"status={st}"))

        # cross-account profile
        other = (
            admin.table("profiles").select("id").neq("account_id", account_id)
            .is_("archived_at", "null").limit(1).execute()
        ).data
        if other:
            st, _ = fetch(base, "/comparison-sets/archive", headers=headers, method="POST",
                          body={"comparison_set_id": set_id, "profile_id": other[0]["id"]})
            results.append(("be_cross_account_404", st == 404, f"status={st}"))
        else:
            results.append(("be_cross_account_404", True, "skipped"))

        # unauth
        st, _ = fetch(base, "/comparison-sets/create", method="POST",
                      body={"profile_id": profile_id, "place_ids": [p1, p2]})
        results.append(("be_unauth_401", st == 401, f"status={st}"))

        # ================= FRONTEND =================
        fav_place_ids, new_fav_places = ensure_two_favorites(
            admin, account_id, profile_id, stamp,
        )
        created_fav_place_ids.extend(new_fav_places)

        from playwright.sync_api import sync_playwright
        s = sess.session
        ref = urlparse(url).hostname.split(".")[0]
        storage_key = f"sb-{ref}-auth-token"
        storage_val = json.dumps({
            "access_token": s.access_token, "refresh_token": s.refresh_token,
            "expires_at": s.expires_at, "expires_in": s.expires_in,
            "token_type": s.token_type or "bearer",
            "user": json.loads(sess.user.model_dump_json()),
        })

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            console_errors = []
            load_count = {"n": 0}
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console_errors.append("pageerror: " + str(e)))
            page.on("load", lambda _f: load_count.__setitem__("n", load_count["n"] + 1))
            page.on("dialog", lambda d: d.accept())
            page.add_init_script(
                f"try{{window.localStorage.setItem({json.dumps(storage_key)},{json.dumps(storage_val)});}}catch(e){{}}"
            )

            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.CurrentUser && !!window.__rmAppShell "
                "&& typeof window.__rmAppShell.navigate === 'function'",
                timeout=30000,
            )
            page.evaluate(
                "()=>{const m=document.getElementById('guidedOnboardingModal');if(m)m.remove();}"
            )
            page.wait_for_function(
                "(pid)=>{try{const vm=window.__rmAppShell.viewModel();"
                "return !!vm && vm.chartRecords.some(r=>r.chartRecordId===pid);}catch(e){return false;}}",
                arg=profile_id, timeout=30000,
            )


            # C-UX-4: Chrome Compare → overlay workflow
            page.evaluate("() => window.__rmAppShell.closeComparisonOverlay()")
            page.click('[data-nav-route="compare"]')
            page.wait_for_function(
                "() => document.getElementById('comparisonOverlayModal')?.classList.contains('open')",
                timeout=15000,
            )
            results.append(("fe_overlay_chrome_open", True, "overlay open"))

            on_compare_route = page.evaluate(
                "() => window.__rmAppShell.navContext.route === 'compare'"
            )
            results.append(("fe_overlay_on_compare_screen", on_compare_route, f"route={on_compare_route}"))

            overlay_ph = page.evaluate(
                "() => document.querySelector('#rm-cmp-overlay-search-mount [data-rm-saved-loc-input]')?.placeholder || ''"
            )
            results.append(("fe_overlay_family_b_placeholder",
                            "favorites" in overlay_ph.lower() and "location" in overlay_ph.lower(),
                            f"placeholder={overlay_ph!r}"))

            page.click('#rm-cmp-overlay-search-mount [data-rm-saved-loc-input]')
            page.wait_for_function(
                "() => document.querySelector('#rm-cmp-overlay-search-mount [data-rm-saved-loc-panel]:not([hidden])')",
                timeout=20000,
            )
            starter_overlay = page.evaluate(
                "() => document.querySelectorAll('#rm-cmp-overlay-search-mount [data-rm-saved-loc-item]').length"
            )
            results.append(("fe_overlay_starter", starter_overlay >= 1, f"items={starter_overlay}"))

            page.fill('#rm-cmp-overlay-search-mount [data-rm-saved-loc-input]', 'Ouagadougou')
            page.wait_for_function(
                "() => [...document.querySelectorAll('#rm-cmp-overlay-search-mount [data-rm-saved-loc-item]')]"
                ".some((el) => (el.textContent || '').includes('Ouagadougou'))",
                timeout=25000,
            )
            page.click('#rm-cmp-overlay-search-mount [data-rm-saved-loc-item]')
            page.wait_for_timeout(400)

            page.evaluate(
                """(args) => {
                  window.__rmAppShell.addComparisonPick(args.id1, args.n1, { hostId: 'rm-cmp-overlay-selected', msgId: 'rm-cmp-overlay-msg' });
                  window.__rmAppShell.addComparisonPick(args.id2, args.n2, { hostId: 'rm-cmp-overlay-selected', msgId: 'rm-cmp-overlay-msg' });
                }""",
                {"id1": fav_place_ids[0], "n1": "fav-a", "id2": fav_place_ids[1], "n2": "fav-b"},
            )
            compare_enabled = page.evaluate(
                "() => !document.getElementById('rm-cmp-overlay-compare-btn')?.disabled"
            )
            results.append(("fe_overlay_compare_enabled", compare_enabled, f"enabled={compare_enabled}"))

            blocked = page.evaluate(
                """() => {
                  const app = window.__rmAppShell;
                  const host = document.getElementById('rm-cmp-overlay-selected');
                  let n = host ? host.querySelectorAll('.rm-cmp-pick').length : 0;
                  while (n < 6) {
                    const ok = app.addComparisonPick('block-test-' + n, 'Extra ' + n, {
                      hostId: 'rm-cmp-overlay-selected', msgId: 'rm-cmp-overlay-msg',
                    });
                    if (!ok) {
                      const msg = document.getElementById('rm-cmp-overlay-msg')?.textContent || '';
                      return msg.indexOf('Maximum 5') !== -1;
                    }
                    n++;
                  }
                  return false;
                }"""
            )
            results.append(("fe_overlay_max_five", blocked, f"blocked={blocked}"))

            page.click('[data-action="cmp-overlay-close"]')
            page.wait_for_function(
                "() => !document.getElementById('comparisonOverlayModal')?.classList.contains('open')",
                timeout=10000,
            )
            cancel_closed = page.evaluate(
                "() => document.getElementById('comparisonOverlayModal')?.getAttribute('aria-hidden') === 'true'"
            )
            results.append(("fe_overlay_cancel_closes", cancel_closed, f"closed={cancel_closed}"))

            page.evaluate("() => window.__rmAppShell.closeComparisonOverlay()")

            # Build comparison from compare screen
            loads_before = load_count["n"]
            page.evaluate(
                "(pid)=>{window.__rmAppShell.switchChartRecord(pid);"
                "window.__rmAppShell.navigate('compare', {chartRecordId: pid, comparisonSetId: null}, { skipComparisonOverlay: true });}",
                profile_id,
            )
            page.wait_for_selector("[data-action='compare-build']", timeout=15000)
            page.wait_for_selector("[data-rm-saved-loc-input]", timeout=15000)

            page.evaluate(
                """(args) => {
                  const vm = window.__rmAppShell.viewModel();
                  const rec = vm.chartRecords.find((r) => r.chartRecordId === args.pid);
                  args.ids.forEach((placeId) => {
                    const fav = rec && rec.favorites
                      ? rec.favorites.find((f) => f.placeId === placeId)
                      : null;
                    const name = fav ? fav.placeName : placeId;
                    window.__rmAppShell.addComparisonPick(placeId, name);
                  });
                }""",
                {"pid": profile_id, "ids": fav_place_ids[:2]},
            )
            page.wait_for_function(
                "() => document.querySelectorAll('.rm-cmp-pick:checked').length >= 2",
                timeout=10000,
            )

            # Family B: unified search input present with doctrine placeholder
            ph = page.evaluate(
                "() => document.querySelector('[data-rm-saved-loc-input]')?.placeholder || ''"
            )
            results.append(("fe_family_b_placeholder",
                            "favorites" in ph.lower() and "location" in ph.lower(),
                            f"placeholder={ph!r}"))

            page.click("[data-action='compare-build']")
            page.wait_for_function(
                "()=>window.__rmAppShell.navContext.comparisonSetId",
                timeout=20000,
            )
            fe_set_id = page.evaluate("()=>window.__rmAppShell.navContext.comparisonSetId")
            if fe_set_id:
                created_set_ids.append(fe_set_id)
            mem_has = page.evaluate(
                "(id)=>{const r=window.__rmAppShell.storeRaw();"
                "return !!(r&&r.comparison_sets&&r.comparison_sets.some(c=>c.id===id));}",
                fe_set_id,
            )
            results.append(("fe_create_compare_opens",
                            bool(fe_set_id) and mem_has,
                            f"setId={fe_set_id} mem={mem_has}"))

            # Overlay: open saved comparison restores workspace
            page.evaluate("() => window.__rmAppShell.closeComparisonOverlay()")
            page.click('[data-nav-route="compare"]')
            page.wait_for_selector(f'.rm-cmp-overlay-open[data-cmp-id="{fe_set_id}"]', timeout=15000)
            page.click(f'.rm-cmp-overlay-open[data-cmp-id="{fe_set_id}"]')
            page.wait_for_selector("#rm-cmp-workspace", timeout=15000)
            overlay_ws = page.evaluate("() => !!document.getElementById('rm-cmp-workspace')")
            results.append(("fe_overlay_open_saved", overlay_ws, f"workspace={overlay_ws}"))

            results.append(("fe_create_no_reload",
                            load_count["n"] == loads_before,
                            f"loads={load_count['n']} before={loads_before}"))


            # Family B starter + merged search
            page.evaluate(
                "(pid)=>{window.__rmAppShell.switchChartRecord(pid);"
                "window.__rmAppShell.navigate('compare',"
                "{chartRecordId: pid, comparisonSetId: null}, { skipComparisonOverlay: true });}",
                profile_id,
            )
            page.wait_for_selector("[data-rm-saved-loc-input]", timeout=15000)
            page.evaluate(
                "(pid) => { if (window.RMSavedLocationSearch) window.RMSavedLocationSearch.invalidateProfile(pid); }",
                profile_id,
            )
            page.click("[data-rm-saved-loc-input]")
            page.wait_for_function(
                "() => document.querySelector('[data-rm-saved-loc-panel]:not([hidden])')",
                timeout=20000,
            )
            page.wait_for_function(
                "() => document.querySelectorAll('[data-rm-saved-loc-item]').length >= 1",
                timeout=20000,
            )
            starter_count = page.evaluate(
                "() => document.querySelectorAll('[data-rm-saved-loc-item]').length"
            )
            results.append(("fe_family_b_starter", starter_count >= 1,
                            f"starter_items={starter_count}"))
            page.fill("[data-rm-saved-loc-input]", "London")
            page.wait_for_function(
                "() => document.querySelector('[data-rm-saved-loc-panel]:not([hidden])') && document.querySelectorAll('[data-rm-saved-loc-item]').length > 0",
                timeout=15000,
            )
            merged_count = page.evaluate(
                "() => document.querySelectorAll('[data-rm-saved-loc-item]').length"
            )
            results.append(("fe_family_b_merge_search", merged_count >= 1,
                            f"merged_items={merged_count}"))

            # Restore built comparison before workspace round-trip
            page.evaluate(
                "(args)=>{window.__rmAppShell.navigate('compare',"
                "{chartRecordId: args.pid, comparisonSetId: args.sid});}",
                {"pid": profile_id, "sid": fe_set_id},
            )

            # Workspace state round-trip (before archive)
            page.wait_for_selector("#rm-cmp-workspace", timeout=15000)
            page.click("[data-action='cmp-angle-tab'][data-angle-tab='asc']")
            page.wait_for_function(
                "()=>document.querySelector('.rm-cmp-angle-tab.active')?.getAttribute('data-angle-tab')==='asc'",
                timeout=5000,
            )
            page.click("[data-action='cmp-toggle-section'][data-cmp-section='ais']")
            page.evaluate("async ()=>{ await window.__rmAppShell.flushComparisonWorkspaceState(); }")
            page.wait_for_function(
                "()=>{const m=document.getElementById('rm-cmp-ws-msg');"
                "return m && m.textContent.indexOf('saved') !== -1;}",
                timeout=15000,
            )
            db_row_mem = (
                admin.table("comparison_sets").select("settings_snapshot_json")
                .eq("id", fe_set_id).single().execute()
            ).data
            mem_ws = ((db_row_mem or {}).get("settings_snapshot_json") or {}).get("comparison_workspace_state") or {}
            mem_tab = mem_ws.get("active_angle_tab")
            results.append(("fe_workspace_inmemory", mem_tab == "asc", f"tab={mem_tab}"))
            page.goto(base + "/app_shell.html", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => !!window.__rmAppShell && typeof window.__rmAppShell.navigate === 'function'",
                timeout=30000,
            )
            page.evaluate(
                "()=>{const m=document.getElementById('guidedOnboardingModal');if(m){m.remove();}}"
            )
            page.evaluate(
                "(args)=>{window.__rmAppShell.navigate('compare',"
                "{chartRecordId: args.pid, comparisonSetId: args.sid});}",
                {"pid": profile_id, "sid": fe_set_id},
            )
            page.wait_for_selector("#rm-cmp-workspace", timeout=15000)
            rl_tab = page.evaluate(
                "()=>document.querySelector('.rm-cmp-angle-tab.active')?.getAttribute('data-angle-tab')")
            rl_collapsed = page.evaluate(
                "()=>document.getElementById('rm-cmp-sec-ais')?.classList.contains('collapsed')")
            db_row = (
                admin.table("comparison_sets").select("settings_snapshot_json")
                .eq("id", fe_set_id).single().execute()
            ).data
            db_ws = ((db_row or {}).get("settings_snapshot_json") or {}).get("comparison_workspace_state") or {}
            results.append(("fe_workspace_reload_tab", rl_tab == "asc", f"tab={rl_tab}"))
            results.append(("fe_workspace_reload_collapsed", rl_collapsed is True, f"collapsed={rl_collapsed}"))
            results.append(("fe_workspace_db_tab", db_ws.get("active_angle_tab") == "asc",
                            f"db_tab={db_ws.get('active_angle_tab')}"))

            # Archive from chart-record module
            page.evaluate(
                "(pid)=>{window.__rmAppShell.navigate('chart-record', {chartRecordId: pid});}",
                profile_id,
            )
            page.wait_for_selector("#rm-cr-comparison-sets", timeout=15000)
            page.wait_for_function(
                "(id)=>!!document.querySelector('.rm-cr-cmp-archive[data-cmp-id=\"'+id+'\"]')",
                arg=fe_set_id, timeout=20000,
            )
            loads_before_arch = load_count["n"]
            page.click(f".rm-cr-cmp-archive[data-cmp-id='{fe_set_id}']")
            page.wait_for_function(
                "(id)=>!document.querySelector('.rm-cr-cmp-archive[data-cmp-id=\"'+id+'\"]')",
                arg=fe_set_id, timeout=15000,
            )
            mem_after = page.evaluate(
                "(id)=>{const r=window.__rmAppShell.storeRaw();"
                "return !!(r&&r.comparison_sets&&r.comparison_sets.some(c=>c.id===id));}",
                fe_set_id,
            )
            db_arch = (
                admin.table("comparison_sets").select("archived_at")
                .eq("id", fe_set_id).single().execute()
            ).data
            results.append(("fe_archive_removed",
                            mem_after is False and db_arch and db_arch.get("archived_at"),
                            f"mem={mem_after} archived={db_arch.get('archived_at') if db_arch else None}"))
            results.append(("fe_archive_no_reload",
                            load_count["n"] == loads_before_arch,
                            f"loads={load_count['n']} before={loads_before_arch}"))

            # Compare screen recovery: reopen compare — should not error with stale set
            page.evaluate(
                "(pid)=>{window.__rmAppShell.navigate('compare',"
                "{chartRecordId: pid, comparisonSetId: null, placeId: null}, { skipComparisonOverlay: true });}",
                profile_id,
            )
            page.wait_for_selector("[data-action='compare-build']", timeout=15000)
            broken = page.evaluate(
                "()=>{const cs=window.__rmAppShell.navContext.comparisonSetId;"
                "const fn=window.__rmAppShell.viewModel().comparisonSets.find("
                "c=>c.id===cs); return cs && !fn;}"
            )
            results.append(("fe_compare_recovery",
                            not broken,
                            f"stale_broken={broken}"))

            # AIS-1: workbook AIS section consumes canonical_chart.angles
            page.evaluate(
                "(args)=>{window.__rmAppShell.navigate('compare',"
                "{chartRecordId: args.pid, comparisonSetId: args.sid});}",
                {"pid": profile_id, "sid": fe_set_id},
            )
            page.wait_for_selector("#rm-cmp-sec-ais .rm-ais-table[data-ais-source='canonical_chart']", timeout=25000)
            ais_check = page.evaluate(
                """() => {
                  const body = document.getElementById('rm-cmp-sec-ais');
                  const table = body && body.querySelector('.rm-ais-table[data-ais-source="canonical_chart"]');
                  const placeholder = body && (body.textContent || '').indexOf('full section content ships in a later layout slice') >= 0;
                  const a2a = (typeof window.__rmGetA2aDisplayAngles === 'function') ? window.__rmGetA2aDisplayAngles() : {};
                  const labels = table ? Array.from(table.querySelectorAll('tr td:first-child')).map(td => td.textContent.trim()) : [];
                  const thCount = table && table.querySelector('tr') ? table.querySelector('tr').querySelectorAll('th').length : 0;
                  return {
                    placeholder,
                    hasTable: !!table,
                    labels,
                    thCount,
                    asc: labels.includes('ASC'),
                    mc: labels.includes('MC'),
                    dsc: labels.includes('DSC'),
                    ic: labels.includes('IC'),
                    a2a,
                    respects: labels.includes('ASC') === !!a2a.asc
                      && labels.includes('MC') === !!a2a.mc
                      && labels.includes('DSC') === !!a2a.dsc
                      && labels.includes('IC') === !!a2a.ic,
                  };
                }"""
            )
            results.append(("fe_ais_not_placeholder",
                            ais_check.get("hasTable") and not ais_check.get("placeholder"),
                            f"hasTable={ais_check.get('hasTable')} placeholder={ais_check.get('placeholder')}"))
            results.append(("fe_ais_default_asc_mc",
                            ais_check.get("asc") and ais_check.get("mc"),
                            f"labels={ais_check.get('labels')}"))
            results.append(("fe_ais_dsc_ic_hidden_default",
                            not ais_check.get("dsc") and not ais_check.get("ic"),
                            f"dsc={ais_check.get('dsc')} ic={ais_check.get('ic')}"))
            results.append(("fe_ais_respects_display_angles",
                            ais_check.get("respects") is True,
                            f"a2a={ais_check.get('a2a')} labels={ais_check.get('labels')}"))
            results.append(("fe_ais_canonical_source",
                            ais_check.get("hasTable") is True,
                            "data-ais-source=canonical_chart"))

            results.append(("fe_ais_comparison_columns",
                            (ais_check.get("thCount") or 0) >= 2,
                            f"thCount={ais_check.get('thCount')}"))

            # A2A-1: workbook + Screen 4 consume canonical_chart.aspects_to_angles
            page.wait_for_selector("#rm-cmp-sec-a2a", timeout=25000)
            a2a_check = page.evaluate(
                """() => {
                  const body = document.getElementById('rm-cmp-sec-a2a');
                  const table = body && body.querySelector('.rm-a2a-table[data-a2a-source="canonical_chart"]');
                  const placeholder = body && (body.textContent || '').indexOf('ships in a later slice') >= 0;
                  const emptyMsg = body && (body.textContent || '').indexOf('No enabled aspect-to-angle contacts within the current orb settings.') >= 0;
                  const thCount = table && table.querySelector('tr') ? table.querySelector('tr').querySelectorAll('th').length : 0;
                  const placeChips = document.querySelectorAll('.rm-cmp-city-chip:not(.hidden-place)').length;
                  const contactHeader = table && table.querySelector('th') ? table.querySelector('th').textContent.trim() : '';
                  return {
                    placeholder,
                    hasTable: !!table,
                    emptyMsg,
                    thCount,
                    placeChips,
                    contactHeader,
                    colsMatch: !table || (thCount === placeChips + 1),
                    rowCount: table ? table.querySelectorAll('tr').length - 1 : 0,
                  };
                }"""
            )
            results.append(("fe_a2a_not_placeholder",
                            not a2a_check.get("placeholder"),
                            f"placeholder={a2a_check.get('placeholder')}"))
            results.append(("fe_a2a_canonical_source",
                            a2a_check.get("hasTable") or a2a_check.get("emptyMsg"),
                            f"hasTable={a2a_check.get('hasTable')} empty={a2a_check.get('emptyMsg')}"))
            results.append(("fe_a2a_comparison_columns",
                            (a2a_check.get("thCount") or 0) >= 2 or a2a_check.get("emptyMsg"),
                            f"thCount={a2a_check.get('thCount')}"))
            results.append(("fe_a2a_contact_column",
                            a2a_check.get("contactHeader") == "Contact" or a2a_check.get("emptyMsg"),
                            f"contactHeader={a2a_check.get('contactHeader')}"))
            results.append(("fe_a2a_columns_match_places",
                            a2a_check.get("colsMatch") is True,
                            f"thCount={a2a_check.get('thCount')} chips={a2a_check.get('placeChips')}"))

            page.evaluate(
                "(args)=>{window.__rmAppShell.navigate('chart',"
                "{chartRecordId: args.pid, placeId: args.place});}",
                {"pid": profile_id, "place": p1},
            )
            page.wait_for_selector("#rm-screen4-facts .rm-a2a-table, #rm-screen4-facts .meta", timeout=25000)
            s4_a2a = page.evaluate(
                """() => {
                  const root = document.getElementById('rm-screen4-facts');
                  const table = root && root.querySelector('.rm-a2a-table[data-a2a-source="canonical_chart"]');
                  const emptyMsg = root && (root.textContent || '').indexOf('No enabled aspect-to-angle contacts within the current orb settings.') >= 0;
                  return { hasTable: !!table, emptyMsg };
                }"""
            )
            results.append(("fe_a2a_screen4_canonical",
                            s4_a2a.get("hasTable") or s4_a2a.get("emptyMsg"),
                            f"hasTable={s4_a2a.get('hasTable')} empty={s4_a2a.get('emptyMsg')}"))

            # PIH-QA-FIX-1: Sun house cross-check via scoped .rm-pih-table (WHEEL-v2 fixtures)
            try:
                qa_locs = resolve_wheel_v2_qa_locations(admin, account_id, profile_id)
                qa_expected = {
                    "current_kansas_city": 1,
                    "favorite_city": 12,
                    "comparison_city": 7,
                }
                results.extend(wheel_v2_pih_crosscheck(page, profile_id, qa_locs, qa_expected))
            except Exception as exc:
                results.append(("fe_pih_wheel_v2_crosscheck", False, str(exc)[:120]))

            # SETTINGS-WIRE-3: A2A display angle defaults via app shell helper
            a2a_defaults = page.evaluate(
                "() => (typeof window.__rmGetA2aDisplayAngles === 'function' ? window.__rmGetA2aDisplayAngles() : null)"
            )
            results.append(("fe_a2a_display_defaults",
                            isinstance(a2a_defaults, dict)
                            and a2a_defaults.get("asc") is True
                            and a2a_defaults.get("mc") is True
                            and a2a_defaults.get("dsc") is False
                            and a2a_defaults.get("ic") is False,
                            f"defaults={a2a_defaults}"))

            app_errors = [e for e in console_errors
                          if "Failed to load resource" not in e and "net::ERR" not in e]
            results.append(("fe_no_console_errors", len(app_errors) == 0,
                            "; ".join(app_errors[:5]) or "none"))
            browser.close()

    finally:
        for sid in set(created_set_ids):
            admin.table("comparison_set_places").delete().eq("comparison_set_id", sid).execute()
            admin.table("comparison_sets").delete().eq("id", sid).execute()
        for pid in created_fav_place_ids:
            admin.table("favorite_places").delete().eq("profile_id", profile_id).eq("place_id", pid).execute()
        for pid in created_place_ids + created_fav_place_ids:
            admin.table("places").delete().eq("id", pid).execute()
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

    failed = [n for n, ok, _ in results if not ok]
    for n, ok, d in results:
        print(f"{'PASS' if ok else 'FAIL'}: {n} — {d}")
    if failed:
        fail(f"{len(failed)} check(s) failed: {', '.join(failed)}")
    print("PASS: smoke_comparison_sets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
