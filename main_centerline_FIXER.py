from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Any, List, Literal, Union

import swisseph as swe
import os
swe.set_ephe_path(os.path.join(os.path.dirname(__file__), "ephe"))
import numpy as np
import json
import time
from pathlib import Path
from scipy.ndimage import gaussian_filter
from skimage import measure
from skimage.measure import approximate_polygon
from truth_grid_engine import (
    SIGN_NAMES,
    generate_angle_sign_features,
    generate_truth_grid_house_features,
    normalize_angle_sign_code,
)
from aura_field_engine import (
    AURA_POC_OVERLAY,
    CONVERGENCE_DELTA_THRESHOLD,
    generate_aura_field,
    generate_aura_adaptive_raster,
    generate_aura_convergence_raster,
    generate_aura_raster,
    is_aura_poc_overlay,
    signed_angle_diff as aura_signed_angle_diff,
)
from local_product_store import (
    ChartRecordBirthResolutionError,
    list_chart_record_summaries,
    load as load_product_store,
    resolve_engine_birth_params,
    summarize_chart_record,
)

app = FastAPI()
CHARTS_FILE = Path(__file__).parent / "charts" / "chart_profiles.json"
APP_DIR = Path(__file__).parent

def load_chart_profiles():
    if not CHARTS_FILE.exists():
        return []

    with open(CHARTS_FILE, "r") as f:
        return json.load(f)


@app.get("/map_CURRENT.html")
def serve_map_current():
    return FileResponse(APP_DIR / "map_CURRENT.html", media_type="text/html")


@app.get("/map_SANDBOX_truth_pixels.html")
def serve_map_sandbox_truth_pixels():
    return FileResponse(APP_DIR / "map_SANDBOX_truth_pixels.html", media_type="text/html")


@app.get("/map_SANDBOX_truth_reveal.html")
def serve_map_sandbox_truth_reveal():
    return FileResponse(APP_DIR / "map_SANDBOX_truth_reveal.html", media_type="text/html")


@app.get("/map_SANDBOX_polygon_reveal.html")
def serve_map_sandbox_polygon_reveal():
    return FileResponse(APP_DIR / "map_SANDBOX_polygon_reveal.html", media_type="text/html")


@app.get("/map_SANDBOX_screen_pixel_truth.html")
def map_sandbox_screen_pixel_truth():
    return FileResponse(
        APP_DIR / "map_SANDBOX_screen_pixel_truth.html",
        media_type="text/html",
    )


@app.get("/map_SANDBOX_brute_force.html")
def serve_map_sandbox_brute_force():
    return FileResponse(APP_DIR / "map_SANDBOX_brute_force.html", media_type="text/html")


@app.get("/map_SANDBOX_phase2_cache.html")
def serve_map_sandbox_phase2_cache():
    return FileResponse(
        APP_DIR / "map_SANDBOX_phase2_cache.html",
        media_type="text/html",
    )


@app.get("/phase2_cache_scheduler.js")
def serve_phase2_cache_scheduler():
    return FileResponse(
        APP_DIR / "phase2_cache_scheduler.js",
        media_type="application/javascript",
    )


@app.get("/substrate_adapter.js")
def serve_substrate_adapter():
    return FileResponse(
        APP_DIR / "substrate_adapter.js",
        media_type="application/javascript",
    )


@app.get("/genie_map_engine_adapter.js")
def serve_genie_map_engine_adapter():
    return FileResponse(
        APP_DIR / "genie_map_engine_adapter.js",
        media_type="application/javascript",
    )


@app.get("/genie_variable_builder.js")
def serve_genie_variable_builder():
    return FileResponse(
        APP_DIR / "genie_variable_builder.js",
        media_type="application/javascript",
    )


@app.get("/genie_variable_builder.css")
def serve_genie_variable_builder_css():
    return FileResponse(
        APP_DIR / "genie_variable_builder.css",
        media_type="text/css",
    )


@app.get("/genie_SANDBOX_variable_builder.html")
def serve_genie_sandbox_variable_builder():
    return FileResponse(
        APP_DIR / "genie_SANDBOX_variable_builder.html",
        media_type="text/html",
    )


@app.get("/map_SANDBOX_raindrop_aesthetic.html")
def serve_map_sandbox_raindrop_aesthetic():
    return FileResponse(
        APP_DIR / "map_SANDBOX_raindrop_aesthetic.html",
        media_type="text/html",
    )


@app.get("/cities.js")
def serve_cities_js():
    return FileResponse(APP_DIR / "cities.js", media_type="application/javascript")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Condition(BaseModel):
    planet: str
    house: int
    orb: float = 2.0


class AngleSignCondition(BaseModel):
    angle: str
    sign: str

class AuraFieldRequest(BaseModel):
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    aspect_overlay: dict
    resolution: float = 2.0
    max_orb: float = 6.0
    min_strength: float = 0.04
    include_debug_points: bool = False
    apply_lat_cap: bool = True


class AuraRasterRequest(BaseModel):
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    aspect_overlay: dict
    north: float
    south: float
    west: float
    east: float
    width: int
    height: int
    max_orb: float = 6.0
    apply_lat_cap: bool = True


class AuraAdaptiveRasterRequest(BaseModel):
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    aspect_overlay: dict
    north: float
    south: float
    west: float
    east: float
    paint_width: int
    paint_height: int
    max_orb: float = 6.0
    apply_lat_cap: bool = True
    initial_divisions: int = 6
    max_depth: int = 6
    gradient_tolerance: float = 0.06
    min_cell_deg: float = 0.035
    max_samples: int = 120000
    max_leaves: int = 12000
    include_debug_cells: bool = True
    include_convergence_metrics: bool = True
    include_reveal_transport: bool = False
    refinement_stage_id: str | None = None


class ClassifyPointPayload(BaseModel):
    lat: float
    lon: float


_ZODIAC_SIGNS = (
    "aries", "taurus", "gemini", "cancer",
    "leo", "virgo", "libra", "scorpio",
    "sagittarius", "capricorn", "aquarius", "pisces",
)
# Cusp INDEX (into the 0-based 12-element cusps array) for each of the
# four angles. The angles are derived from the Placidus house cusps:
# ASC = cusp of 1st, IC = cusp of 4th, DSC = cusp of 7th, MC = cusp of 10th.
_ANGLE_TO_CUSP_INDEX = {"asc": 0, "ic": 3, "dsc": 6, "mc": 9}


class PlanetInHouseCondition(BaseModel):
    """A single planet-in-house condition slot in a brute-force grid query."""

    type: Literal["planet_in_house"] = "planet_in_house"
    planet: str
    house: int


class AngleInSignCondition(BaseModel):
    """A single angle-in-sign condition slot in a brute-force grid query.

    The cell is a match iff the requested relocated angle (ASC, MC, IC,
    or DSC) currently falls within the requested zodiac sign (30°
    band). The angle is derived from the same `swe.houses` cusps the
    other condition types use; no additional astrology assumption is
    introduced.
    """

    type: Literal["angle_in_sign"] = "angle_in_sign"
    angle: Literal["asc", "mc", "ic", "dsc"]
    sign: Literal["aries", "taurus", "gemini", "cancer",
                  "leo", "virgo", "libra", "scorpio",
                  "sagittarius", "capricorn", "aquarius", "pisces"]


# Major-aspect target angles in degrees of ecliptic separation. These
# are the *exact* targets; the orb is applied per-condition at the
# call site, not here. Quintile/quincunx/etc. are intentionally
# absent — step 6 starts with the five classical major aspects only.
_ASPECT_TARGET_DEG = {
    "conjunction": 0.0,
    "sextile":     60.0,
    "square":      90.0,
    "trine":       120.0,
    "opposition":  180.0,
}


class AspectToAngleCondition(BaseModel):
    """A single aspect-to-angle condition slot in a brute-force grid query.

    The cell is a match iff a natal planet's longitude is within ``orb``
    degrees of an exact major aspect to the relocated angle (ASC, MC,
    IC, or DSC) computed at the cell. This is the classical "relocation
    centerline" condition rendered as an occupancy *band* of width
    ``2 × orb``, not as an interpolated curve.

    Per cell:
      1. compute cusps via ``swe.houses(jd, lat, lon)``
      2. angle_long = cusps[cusp_index_for(angle)]
      3. signed_sep = ((planet_long - angle_long + 180) % 360) - 180
      4. abs_sep    = abs(signed_sep)
      5. match iff abs(abs_sep - target_degrees_for(aspect)) <= orb

    The planet longitude is the natal value — tropical zodiac
    longitudes do not change with location; only houses and angles do.

    No smoothing, no interpolation, no inferred curves: the condition
    is either true at this exact cell or it is not.
    """

    type: Literal["aspect_to_angle"] = "aspect_to_angle"
    planet: str
    angle: Literal["asc", "mc", "ic", "dsc"]
    aspect: Literal["conjunction", "sextile", "square", "trine", "opposition"]
    orb: float = Field(default=1.0, gt=0.0, le=15.0)


# Discriminated union: the request schema accepts any condition shape
# and decides by the `type` field. Older clients posting
# `{planet, house}` without a `type` still work because the default on
# PlanetInHouseCondition is "planet_in_house" — a model_validator on
# the request normalises missing types before discrimination.
Condition = Annotated[
    Union[PlanetInHouseCondition, AngleInSignCondition, AspectToAngleCondition],
    Field(discriminator="type"),
]


class BruteForceGridRequest(BaseModel):
    """Brute-force deterministic grid classification request.

    For the proof test: classify EVERY point of a regular lat/lon grid that
    covers the given bounds at the requested spacing, then return only the
    coordinates that match the requested conditions. This is the
    "no laziness, no smoothing, every cell is asked" rendering target —
    not a sampling strategy.

    Multi-condition support: the request may carry up to six
    ``conditions``. Every cell is classified once via ``swe.houses`` and
    then tested against ALL conditions in that single pass; a match cell
    is returned with a bitmask telling the renderer which conditions it
    satisfied. Overlap is therefore real — it is "this exact lat/lon
    satisfies condition A and condition B simultaneously in the same
    classification" — never a client-side reconstruction.

    Mixed condition types are supported: a single request may freely
    combine ``planet_in_house`` and ``angle_in_sign`` slots. Each slot
    declares its ``type``; legacy clients omitting ``type`` get
    ``planet_in_house`` by default for back-compat.

    The legacy ``target_planet``/``target_house`` pair is still accepted
    as a one-condition shorthand for older URL parameters.

    The request is intentionally NOT optimised. We accept a grid up to
    five million cells; anything larger is rejected so the wire response
    cannot accidentally become a denial-of-service.
    """

    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    north: float
    south: float
    east: float
    west: float
    grid_deg: float
    conditions: list[Condition] | None = None
    target_planet: str | None = None
    target_house: int | None = None
    # The reference screenshots show polygons extending to the polar belt;
    # default to NOT clipping at ±65° for the proof test. Product code can
    # still pass apply_lat_cap=true if it wants the policy-clipped version.
    apply_lat_cap: bool = False
    include_non_matches: bool = False

    @model_validator(mode="before")
    @classmethod
    def _default_condition_type(cls, data):
        """Inject ``type=planet_in_house`` on any legacy condition dict
        that omits it. Discriminated-union validation runs after this,
        so older callers posting ``{planet, house}`` keep working."""
        if isinstance(data, dict):
            conds = data.get("conditions")
            if isinstance(conds, list):
                for c in conds:
                    if isinstance(c, dict) and "type" not in c:
                        if "planet" in c and "house" in c:
                            c["type"] = "planet_in_house"
                        elif "angle" in c and "sign" in c:
                            c["type"] = "angle_in_sign"
                        elif "planet" in c and "angle" in c and "aspect" in c:
                            c["type"] = "aspect_to_angle"
        return data


class ClassifyPointsRequest(BaseModel):
    """Per-point deterministic classification request.

    For each (lat, lon) the server returns the integer house (1..12) of EVERY
    supported planet at that relocated coordinate. The all-planets response is
    intentional: it costs essentially the same as one planet (one ``swe.houses``
    call + twelve cusp comparisons per planet) and lets the client cache the
    full chart-by-point truth on the first reveal pass. Subsequent overlay
    switches (e.g. Sun in 1st → Moon in 4th) can be served from cache without
    re-hitting the engine.

    The truth is exact at every point. Stochastic sample positions are the
    client's concern; this endpoint never invents or interpolates membership.
    """

    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    points: list[ClassifyPointPayload]
    apply_lat_cap: bool = True


class AuraConvergenceRasterRequest(BaseModel):
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    aspect_overlay: dict
    north: float
    south: float
    west: float
    east: float
    paint_width: int
    paint_height: int
    max_orb: float = 6.0
    apply_lat_cap: bool = True
    initial_divisions: int = 4
    convergence_delta_threshold: float = CONVERGENCE_DELTA_THRESHOLD
    target_pixels_above_threshold_pct: float = 0.0
    per_pass_sample_budget: int = 2000
    max_passes: int = 64
    max_samples: int = 120000
    max_leaves: int = 12000
    min_cell_deg: float = 0.035
    overshoot_guard: bool = True
    include_debug_cells: bool = True
    include_pass_history: bool = True
    include_pixel_attribution_sample: bool = False
    pixel_attribution_sample_cap: int = 4000


class SearchRequest(BaseModel):
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    house_conditions: List[Condition]
    angle_sign_conditions: List[AngleSignCondition] = Field(default_factory=list)
    resolution: float = 1.5
    generation_mode: str = "contour"
    truth_grid_resolution: float = 0.75
    truth_grid_boundary_refine: bool = True
    return_all_houses: bool = False
    aspect_resolution: float = 0.5
    overlay_stage: str | None = None
    aspect_overlay: dict | None = None

    @model_validator(mode="before")
    @classmethod
    def _default_house_condition_type(cls, data):
        """Preserve legacy /search-regions callers posting {planet, house}."""
        if isinstance(data, dict):
            conds = data.get("house_conditions")
            if isinstance(conds, list):
                for c in conds:
                    if isinstance(c, dict) and "type" not in c and "planet" in c and "house" in c:
                        c["type"] = "planet_in_house"
        return data

def julian_day(year, month, day, hour_utc):
    return swe.julday(year, month, day, hour_utc)

def get_planet_positions(jd):
    planets = {
        "sun": swe.SUN, "moon": swe.MOON, "mercury": swe.MERCURY,
        "venus": swe.VENUS, "mars": swe.MARS, "jupiter": swe.JUPITER,
        "saturn": swe.SATURN, "uranus": swe.URANUS, "neptune": swe.NEPTUNE,
        "pluto": swe.PLUTO, "chiron": swe.CHIRON
    }
    result = {}
    for name, pid in planets.items():
        result[name] = swe.calc_ut(jd, pid)[0][0] % 360
    return result

def get_houses(jd, lat, lon):
    cusps, _ = swe.houses(jd, lat, lon, b'P')
    return [c % 360 for c in cusps[:12]]

def min_degrees_to_any_cusp(planet_lon: float, cusps12: list[float]) -> float:
    """Smallest angle (0–180°) from planet longitude to any Placidus cusp."""
    p = planet_lon % 360
    best = 180.0
    for c in cusps12:
        c = c % 360
        d = abs(((p - c + 180) % 360) - 180)
        if d < best:
            best = d
    return best


def planet_in_house(planet_long, house_num, cusps):
    start = cusps[house_num - 1]
    end = cusps[house_num % 12]

    if start <= end:
        return start <= planet_long < end

    return planet_long >= start or planet_long < end


def signed_angle_diff(a, b):
    return ((a - b + 180) % 360) - 180


def format_zodiac(deg):
    deg = deg % 360

    sign_index = int(deg // 30)

    sign_deg = deg % 30

    whole_deg = int(sign_deg)

    minutes = int((sign_deg - whole_deg) * 60)

    return f"{whole_deg}° {SIGN_NAMES[sign_index].title()} {minutes:02d}'"


def zodiac_sign_name(deg):
    return SIGN_NAMES[int((deg % 360) // 30)].title()
        
@app.post("/search-regions")
def search_regions(req: SearchRequest):
    """Legacy GeoJSON overlay endpoint.

    STATUS: transitional legacy substrate. Production migration target is
    `/screen-pixel-truth` via the adapter path documented in
    docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md. Keep this endpoint available
    for rollback and validation history, but do not extend it as the
    canonical rendering substrate.
    """
    jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
    planets = get_planet_positions(jd)

    lat_grid = np.arange(-60, 86, req.resolution)
    lon_grid = np.arange(-180, 181, req.resolution)

    features = []
    aspect_features = []
    aspect_metadata = None
    angle_sign_metadata = None

    # =====================================
    # HOUSE REGION SEARCH
    # =====================================
    if req.generation_mode == "truth_grid":
        features, truth_grid_metadata = generate_truth_grid_house_features(
            jd,
            planets,
            req.house_conditions,
            req.truth_grid_resolution,
            req.return_all_houses,
            req.truth_grid_boundary_refine,
        )
    else:
        # ARCHAEOLOGY: contour mode is the rejected polygon-smoothing path.
        # It used gaussian_filter + find_contours to make regions look
        # continuous. Keep for history/rollback only; do not use for Phase-C
        # production migration. Canonical visible rendering is adaptive
        # screen-space truth via /screen-pixel-truth.
        truth_grid_metadata = None
        for idx, cond in enumerate(req.house_conditions):
            mask = np.zeros((len(lat_grid), len(lon_grid)), dtype=np.uint8)
            planet_name = cond.planet.lower()
            planet_long = planets[planet_name]
            polygon_index = 0

            for i, lat in enumerate(lat_grid):
                for j, lon in enumerate(lon_grid):
                    try:
                        cusps = get_houses(jd, lat, lon)
                        if planet_in_house(planet_long, cond.house, cusps):
                            mask[i, j] = 1
                    except:
                        pass

            smooth_mask = gaussian_filter(mask.astype(float), sigma=1.2)
            contours = measure.find_contours(smooth_mask, 0.5)

            for contour in contours:
                if len(contour) < 20:
                    continue
                contour = approximate_polygon(contour, tolerance=0.08)
                coords = []

                for point in contour:
                    lat_f = point[0]
                    lon_f = point[1]

                    if 0 <= lat_f < len(lat_grid) - 1 and 0 <= lon_f < len(lon_grid) - 1:
                        lat_i = int(lat_f)
                        lon_i = int(lon_f)
                        lat_frac = lat_f - lat_i
                        lon_frac = lon_f - lon_i
                        lat_val = lat_grid[lat_i] * (1 - lat_frac) + lat_grid[lat_i + 1] * lat_frac
                        lon_val = lon_grid[lon_i] * (1 - lon_frac) + lon_grid[lon_i + 1] * lon_frac
                        coords.append([float(lon_val), float(lat_val)])
                if len(coords) >= 3:
                    features.append({
                        "type": "Feature",
                        "geometry": {"type": "Polygon", "coordinates": [coords]},
                        "properties": {
                            "canonicalFeatureId": f"house-{idx}-{planet_name}-{cond.house}-{polygon_index}",
                            "planet": planet_name,
                            "house": cond.house,
                            "condition_index": idx,
                            "overlap_count": 1,
                            "generation_mode": "contour"
                        }
                    })
                    polygon_index += 1

    if req.angle_sign_conditions:
        angle_sign_features, angle_sign_metadata = generate_angle_sign_features(
            jd,
            req.angle_sign_conditions,
            req.truth_grid_resolution,
            condition_index_offset=len(req.house_conditions),
            boundary_refine=req.truth_grid_boundary_refine,
        )
        features.extend(angle_sign_features)

    # =====================================
    # ASPECT OVERLAY (MC meridian; ASC/DC/IC = ecliptic-longitude contours)
    # =====================================
    if req.aspect_overlay:
        aspect_started = time.perf_counter()
        selected_planet = req.aspect_overlay.get("planet", "sun").lower()
        selected_angle = normalize_angle_sign_code(str(req.aspect_overlay.get("angle", "MC")))
        if selected_angle not in ("ASC", "MC", "DC", "IC"):
            selected_angle = str(req.aspect_overlay.get("angle", "MC")).strip().upper()
        selected_aspect = req.aspect_overlay.get("aspect", "conjunction").lower()
        aspect_resolution = req.aspect_resolution if req.aspect_resolution > 0 else 0.5
        overlay_stage = req.overlay_stage or "final"

        planet_ids = {
            "sun": swe.SUN, "moon": swe.MOON, "mercury": swe.MERCURY,
            "venus": swe.VENUS, "mars": swe.MARS, "jupiter": swe.JUPITER,
            "saturn": swe.SATURN, "uranus": swe.URANUS, "neptune": swe.NEPTUNE,
            "pluto": swe.PLUTO, "chiron": swe.CHIRON
        }

        planet_id = planet_ids.get(selected_planet)

        if planet_id is not None:
            result = swe.calc_ut(jd, planet_id, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
            planet_ra_deg = result[0][0]
            planet_lon = swe.calc_ut(jd, planet_id)[0][0] % 360

            aspect_sets = {
                "conjunction": [0],
                "opposition": [180],
                "square": [90, 270],
                "trine": [120, 240],
                "sextile": [60, 300],

                "hard": [0, 90, 180, 270],

                "soft": [60, 120, 240, 300],

                "any": [0, 60, 90, 120, 180, 240, 270, 300]
            }

            aspect_colors = {
                0: "#0066ff", 180: "#ff4444", 90: "#ff9900", 270: "#ff9900",
                120: "#00cc66", 240: "#00cc66", 60: "#bb66ff", 300: "#bb66ff"
            }

            offsets = aspect_sets.get(selected_aspect, [0])
            timing = {
                "total_seconds": None,
                "asc_grid_seconds": None,
                "asc_contour_seconds": None,
                "contour_grid_seconds": None,
                "contour_trace_seconds": None,
            }

            angle_grid = None
            lat_vals = None
            lon_vals = None
            sample_count = 0
            contour_started = None

            if selected_angle in ("ASC", "DC", "IC"):
                grid_started = time.perf_counter()
                lat_vals = np.arange(-65, 66, aspect_resolution)
                lon_vals = np.arange(-180, 181, aspect_resolution)

                angle_grid = np.full(
                    (len(lat_vals), len(lon_vals)),
                    np.nan
                )

                sample_count = 0
                for i, lat in enumerate(lat_vals):
                    for j, lon in enumerate(lon_vals):
                        try:
                            _, ascmc = swe.houses(jd, lat, lon, b"P")
                            if selected_angle == "ASC":
                                angle_grid[i, j] = ascmc[0] % 360
                            elif selected_angle == "DC":
                                angle_grid[i, j] = (ascmc[0] + 180.0) % 360
                            else:
                                angle_grid[i, j] = (ascmc[1] + 180.0) % 360
                            sample_count += 1
                        except Exception:
                            pass

                grid_elapsed = round(time.perf_counter() - grid_started, 4)
                timing["contour_grid_seconds"] = grid_elapsed
                if selected_angle == "ASC":
                    timing["asc_grid_seconds"] = grid_elapsed
                contour_started = time.perf_counter()

            for offset in offsets:
                target_ra = (planet_ra_deg + offset) % 360
                target_lon = (planet_lon + offset) % 360

                # =====================================
                # MC CALCULATION (ecliptic MC meridian in geographic lon)
                # =====================================
                if selected_angle == "MC":
                    gst_deg = swe.sidtime(jd) * 15.0
                    mc_lon = target_ra - gst_deg

                    while mc_lon < -180:
                        mc_lon += 360
                    while mc_lon > 180:
                        mc_lon -= 360

                    # Main line
                    aspect_features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[mc_lon, -85], [mc_lon, 85]]
                        },
                        "properties": {
                            "planet": selected_planet,
                            "angle": "MC",
                            "aspect": selected_aspect,
                            "overlay_stage": overlay_stage,
                            "aspect_resolution": aspect_resolution,
                            "color": aspect_colors.get(offset, "#0066ff"),
                            "weight": 4,
                            "opacity": 0.95
                        }
                    })

                # =====================================
                # ASC / DC / IC — same contour machinery on ecliptic longitude field
                # =====================================
                if selected_angle in ("ASC", "DC", "IC") and angle_grid is not None:
                    diff_grid = np.full(
                        angle_grid.shape,
                        np.nan
                    )

                    for i in range(angle_grid.shape[0]):
                        for j in range(angle_grid.shape[1]):
                            ang = angle_grid[i, j]
                            if np.isnan(ang):
                                continue

                            diff = signed_angle_diff(
                                float(ang),
                                target_lon
                            )

                            if abs(diff) < 90:
                                diff_grid[i, j] = diff

                    contours = measure.find_contours(diff_grid, 0.0)

                    for contour in contours:
                        coords = []

                        for point in contour:
                            y, x = point

                            lat = np.interp(
                                y,
                                np.arange(len(lat_vals)),
                                lat_vals
                            )

                            lon = np.interp(
                                x,
                                np.arange(len(lon_vals)),
                                lon_vals
                            )

                            coords.append([
                                float(lon),
                                float(lat)
                            ])

                        if len(coords) > 5:
                            aspect_features.append({
                                "type": "Feature",
                                "geometry": {
                                    "type": "LineString",
                                    "coordinates": coords
                                },
                                "properties": {
                                    "planet": selected_planet,
                                    "angle": selected_angle,
                                    "aspect": selected_aspect,
                                    "aspect_offset": offset,
                                    "overlay_stage": overlay_stage,
                                    "aspect_resolution": aspect_resolution,
                                    "color": aspect_colors.get(offset, "#00e5ff"),
                                    "weight": 2,
                                    "opacity": 1.0
                                }
                            })

            if selected_angle in ("ASC", "DC", "IC") and contour_started is not None:
                trace_elapsed = round(time.perf_counter() - contour_started, 4)
                timing["contour_trace_seconds"] = trace_elapsed
                if selected_angle == "ASC":
                    timing["asc_contour_seconds"] = trace_elapsed

            timing["total_seconds"] = round(time.perf_counter() - aspect_started, 4)
            aspect_metadata = {
                "angle": selected_angle,
                "aspect_set": selected_aspect,
                "aspect_resolution": aspect_resolution,
                "overlay_stage": overlay_stage,
                "timing": timing,
                "feature_count": len(aspect_features),
            }
            if selected_angle in ("ASC", "DC", "IC") and lat_vals is not None:
                aspect_metadata["sample_count"] = sample_count
                aspect_metadata["grid_shape"] = [len(lat_vals), len(lon_vals)]

    response = {
        "type": "FeatureCollection",
        "features": features + aspect_features,
        "properties": {
            "generation_mode": req.generation_mode,
            "truth_grid": truth_grid_metadata,
            "angle_sign": angle_sign_metadata,
            "aspect_overlay": aspect_metadata
        }
    }
    return response


@app.post("/aura-field")
def aura_field(req: AuraFieldRequest):
    """Archaeology/debug PoC: truth-sampled scalar aura field.

    Not the canonical production rendering substrate. Retained for Phase A/B
    validation history and debug comparison only; do not use for Phase-C
    production migration.
    """
    jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
    try:
        return generate_aura_field(
            jd,
            req.aspect_overlay,
            req.resolution,
            max_orb=req.max_orb,
            min_strength=req.min_strength,
            include_debug_points=req.include_debug_points,
            apply_lat_cap=req.apply_lat_cap,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/aura-raster")
def aura_raster(req: AuraRasterRequest):
    """Archaeology/debug PoC: viewport raster aura (Sun conjunct ASC only).

    One truth sample per pixel, retained for validation history. Canonical
    production rendering is adaptive screen-space occupancy via
    /screen-pixel-truth, not this aura PoC endpoint.
    """
    if req.width * req.height > 150000:
        raise HTTPException(
            status_code=400,
            detail=f"Raster too large ({req.width}x{req.height}); max 150000 pixels",
        )
    jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
    try:
        return generate_aura_raster(
            jd,
            req.aspect_overlay,
            req.north,
            req.south,
            req.west,
            req.east,
            req.width,
            req.height,
            max_orb=req.max_orb,
            apply_lat_cap=req.apply_lat_cap,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/aura-raster-adaptive")
def aura_raster_adaptive(req: AuraAdaptiveRasterRequest):
    """Archaeology/debug PoC: adaptive truth-sampled aura raster.

    This supports historical Phase A/B validation and debug reveal checks.
    It is not the Phase-C production renderer and must not be wired into the
    production migration path as the canonical substrate.
    """
    if req.paint_width * req.paint_height > 150000:
        raise HTTPException(
            status_code=400,
            detail=f"Paint grid too large ({req.paint_width}x{req.paint_height}); max 150000 pixels",
        )
    if req.max_samples > 120000:
        raise HTTPException(status_code=400, detail="max_samples cannot exceed 120000")
    jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
    try:
        return generate_aura_adaptive_raster(
            jd,
            req.aspect_overlay,
            req.north,
            req.south,
            req.west,
            req.east,
            req.paint_width,
            req.paint_height,
            max_orb=req.max_orb,
            apply_lat_cap=req.apply_lat_cap,
            initial_divisions=req.initial_divisions,
            max_depth=req.max_depth,
            gradient_tolerance=req.gradient_tolerance,
            min_cell_deg=req.min_cell_deg,
            max_samples=req.max_samples,
            max_leaves=req.max_leaves,
            include_debug_cells=req.include_debug_cells,
            include_convergence_metrics=req.include_convergence_metrics,
            include_reveal_transport=req.include_reveal_transport,
            refinement_stage_id=req.refinement_stage_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/aura-raster-convergence")
def aura_raster_convergence(req: AuraConvergenceRasterRequest):
    """
    ARCHAEOLOGY / debug PoC — not the canonical production renderer.

    Convergence-debt-driven adaptive raster (Phase C). Refines highest-debt leaves
    first via a priority queue against a uniform reference; per-pass budgets bound
    work; an overshoot guard halts the engine if a pass increases pixel-level
    mismatch. No interpolation, no smoothing — mismatch is reported, not hidden.
    """
    if req.paint_width * req.paint_height > 150000:
        raise HTTPException(
            status_code=400,
            detail=f"Paint grid too large ({req.paint_width}x{req.paint_height}); max 150000 pixels",
        )
    if req.max_samples > 120000:
        raise HTTPException(status_code=400, detail="max_samples cannot exceed 120000")
    if req.max_passes > 256:
        raise HTTPException(status_code=400, detail="max_passes cannot exceed 256")
    jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
    try:
        return generate_aura_convergence_raster(
            jd,
            req.aspect_overlay,
            req.north,
            req.south,
            req.west,
            req.east,
            req.paint_width,
            req.paint_height,
            max_orb=req.max_orb,
            apply_lat_cap=req.apply_lat_cap,
            initial_divisions=req.initial_divisions,
            convergence_delta_threshold=req.convergence_delta_threshold,
            target_pixels_above_threshold_pct=req.target_pixels_above_threshold_pct,
            per_pass_sample_budget=req.per_pass_sample_budget,
            max_passes=req.max_passes,
            max_samples=req.max_samples,
            max_leaves=req.max_leaves,
            min_cell_deg=req.min_cell_deg,
            overshoot_guard=req.overshoot_guard,
            include_debug_cells=req.include_debug_cells,
            include_pass_history=req.include_pass_history,
            include_pixel_attribution_sample=req.include_pixel_attribution_sample,
            pixel_attribution_sample_cap=req.pixel_attribution_sample_cap,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


from aura_field_engine import PRODUCT_LAT_CAP as CLASSIFY_PRODUCT_LAT_CAP  # noqa: E402


@app.post("/classify-points")
def classify_points(req: ClassifyPointsRequest):
    """Return the deterministic planet-house mapping at every requested point.

    Truth contract:

    * For each input (lat, lon), ``swe.houses`` is computed exactly once
      (Placidus). Every planet's house is determined by ``planet_in_house``
      against the resulting cusps.
    * Points above ±``PRODUCT_LAT_CAP`` (when ``apply_lat_cap`` is true) are
      tagged ``outside_lat_cap: true`` and their ``houses`` is ``None`` — we do
      not invent classifications above the cap.
    * Any per-point ``swe`` failure surfaces as ``houses: None`` with
      ``error_reason`` so the client can render an explicit non-result rather
      than silently skip the probe.
    * The endpoint never re-orders, deduplicates, or interpolates points.
    """

    t_start = time.perf_counter()
    try:
        jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
        planet_lons = get_planet_positions(jd)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"chart_init_failed: {e}") from e

    cap = CLASSIFY_PRODUCT_LAT_CAP if req.apply_lat_cap else None
    results: list[dict[str, Any]] = []
    capped_count = 0
    error_count = 0
    success_count = 0
    for p in req.points:
        lat = float(p.lat)
        lon = float(p.lon)
        if cap is not None and abs(lat) > cap:
            results.append({
                "lat": lat,
                "lon": lon,
                "outside_lat_cap": True,
                "houses": None,
            })
            capped_count += 1
            continue
        try:
            cusps = get_houses(jd, lat, lon)
            houses: dict[str, int] = {}
            for planet_name, planet_long in planet_lons.items():
                for h in range(1, 13):
                    if planet_in_house(planet_long, h, cusps):
                        houses[planet_name] = h
                        break
            results.append({
                "lat": lat,
                "lon": lon,
                "outside_lat_cap": False,
                "houses": houses,
            })
            success_count += 1
        except Exception as exc:
            results.append({
                "lat": lat,
                "lon": lon,
                "outside_lat_cap": False,
                "houses": None,
                "error_reason": str(exc),
            })
            error_count += 1

    return {
        "points": results,
        "properties": {
            "point_count": len(req.points),
            "classified_count": success_count,
            "outside_lat_cap_count": capped_count,
            "error_count": error_count,
            "apply_lat_cap": req.apply_lat_cap,
            "lat_cap": cap,
            "compute_seconds": round(time.perf_counter() - t_start, 4),
            "planets_returned": sorted(planet_lons.keys()),
        },
    }


_CONDITION_LABELS = ["A", "B", "C", "D", "E", "F"]
_MAX_CONDITIONS = len(_CONDITION_LABELS)


@app.post("/brute-force-grid")
def brute_force_grid(req: BruteForceGridRequest):
    """Classify a deterministic lat/lon grid covering the given bounds.

    Every cell of the grid is run through ``swe.houses`` exactly once and
    tested against every requested condition. A cell that satisfies one
    or more conditions is returned as ``[lat, lon, mask]`` where ``mask``
    is a bitmask: bit ``1<<i`` set iff condition ``i`` matched. The
    response also reports a count for every mask state (and derived
    per-condition / per-pair / triple-overlap totals) so the renderer
    can paint and label overlap regions without ever recomputing
    geography on its own.
    """

    t_start = time.perf_counter()

    south, north = sorted([req.south, req.north])
    west,  east  = sorted([req.west,  req.east])
    if req.grid_deg <= 0.0:
        raise HTTPException(status_code=400, detail="grid_deg must be > 0")

    # cell counts INCLUSIVE of the upper edge
    lat_count = int(round((north - south) / req.grid_deg)) + 1
    lon_count = int(round((east  - west)  / req.grid_deg)) + 1
    total_cells = lat_count * lon_count
    MAX_CELLS = 5_000_000
    if total_cells > MAX_CELLS:
        raise HTTPException(
            status_code=400,
            detail=f"grid too large: {total_cells} cells > {MAX_CELLS} max. "
                   f"Reduce bounds or coarsen grid_deg.",
        )

    # ------------- resolve conditions list -------------
    # Prefer the explicit list. Fall back to legacy single-target fields
    # so older URL params keep working.
    raw_conditions: list[Any] = []
    if req.conditions:
        raw_conditions = list(req.conditions)
    elif req.target_planet is not None and req.target_house is not None:
        raw_conditions = [
            PlanetInHouseCondition(planet=req.target_planet, house=req.target_house)
        ]
    if not raw_conditions:
        raise HTTPException(
            status_code=400,
            detail="at least one condition is required "
                   "(conditions=[...] or target_planet/target_house)",
        )
    if len(raw_conditions) > _MAX_CONDITIONS:
        raise HTTPException(
            status_code=400,
            detail=f"too many conditions: {len(raw_conditions)} > {_MAX_CONDITIONS}",
        )

    try:
        jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
        planets = get_planet_positions(jd)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"chart_init_failed: {e}") from e

    # Compile each condition slot into a small descriptor we can dispatch
    # on cheaply inside the per-cell loop. The descriptor is a tuple
    # whose first element is the condition kind:
    #   ("pih",  house_int,  planet_long_deg,  label, planet_name)
    #   ("ais",  cusp_index, sign_index_0..11, label, angle_name, sign_name)
    #   ("a2a",  cusp_index, planet_long_deg,  target_deg, orb, label,
    #            planet_name, angle_name, aspect_name)
    cond_specs: list[tuple] = []
    conditions_report_preview: list[dict[str, Any]] = []
    for idx, cond in enumerate(raw_conditions):
        label = _CONDITION_LABELS[idx]
        if isinstance(cond, PlanetInHouseCondition):
            planet_name = cond.planet.lower()
            if planet_name not in planets:
                raise HTTPException(status_code=400,
                                    detail=f"unknown planet: {cond.planet}")
            if not (1 <= cond.house <= 12):
                raise HTTPException(
                    status_code=400,
                    detail=f"house must be 1..12 (got {cond.house} for condition {label})",
                )
            cond_specs.append(("pih", cond.house, planets[planet_name], label, planet_name))
            conditions_report_preview.append({
                "id": label,
                "type": "planet_in_house",
                "planet": planet_name,
                "house": cond.house,
            })
        elif isinstance(cond, AngleInSignCondition):
            angle_name = cond.angle.lower()
            sign_name = cond.sign.lower()
            cusp_idx = _ANGLE_TO_CUSP_INDEX[angle_name]
            sign_idx = _ZODIAC_SIGNS.index(sign_name)
            cond_specs.append(("ais", cusp_idx, sign_idx, label, angle_name, sign_name))
            conditions_report_preview.append({
                "id": label,
                "type": "angle_in_sign",
                "angle": angle_name,
                "sign": sign_name,
            })
        elif isinstance(cond, AspectToAngleCondition):
            planet_name = cond.planet.lower()
            if planet_name not in planets:
                raise HTTPException(status_code=400,
                                    detail=f"unknown planet: {cond.planet}")
            angle_name = cond.angle.lower()
            aspect_name = cond.aspect.lower()
            cusp_idx = _ANGLE_TO_CUSP_INDEX[angle_name]
            target_deg = _ASPECT_TARGET_DEG[aspect_name]
            cond_specs.append((
                "a2a", cusp_idx, planets[planet_name], target_deg, cond.orb,
                label, planet_name, angle_name, aspect_name,
            ))
            conditions_report_preview.append({
                "id": label,
                "type": "aspect_to_angle",
                "planet": planet_name,
                "angle": angle_name,
                "aspect": aspect_name,
                "orb": cond.orb,
            })
        else:  # pragma: no cover - the discriminated union prevents this
            raise HTTPException(status_code=400,
                                detail=f"unsupported condition type at slot {label}")

    n_conds = len(cond_specs)
    cap = CLASSIFY_PRODUCT_LAT_CAP if req.apply_lat_cap else None

    matches: list[list[float]] = []
    non_matches: list[list[float]] | None = [] if req.include_non_matches else None
    capped_count = 0
    error_count = 0
    classified_count = 0

    # Per-mask histogram. Index = mask value (1..(2**n_conds - 1));
    # entry 0 is "matched no conditions" and is implicit in
    # `classified_count - sum(per_mask_counts)`.
    per_mask_counts = [0] * (1 << n_conds)

    lats = [south + i * req.grid_deg for i in range(lat_count)]
    lons = [west  + j * req.grid_deg for j in range(lon_count)]

    for lat in lats:
        if lat > north + 1e-9:
            break
        if cap is not None and abs(lat) > cap:
            capped_count += lon_count
            continue
        for lon in lons:
            if lon > east + 1e-9:
                break
            try:
                cusps = get_houses(jd, lat, lon)
            except Exception:
                error_count += 1
                continue
            mask = 0
            for bit_idx, spec in enumerate(cond_specs):
                kind = spec[0]
                if kind == "pih":
                    _, house, planet_long, *_ = spec
                    if planet_in_house(planet_long, house, cusps):
                        mask |= (1 << bit_idx)
                elif kind == "ais":
                    _, cusp_idx, sign_idx, *_ = spec
                    # cusps are normalised to [0, 360). Floor-divide by 30
                    # yields the sign index 0..11; equality with the target
                    # sign index is the match condition.
                    if int(cusps[cusp_idx] // 30) == sign_idx:
                        mask |= (1 << bit_idx)
                else:  # "a2a" — aspect-to-angle centerline (truthful occupancy)
                    _, cusp_idx, planet_long, target_deg, orb, *_ = spec
                    # Signed angular separation in [-180, 180], then folded
                    # to [0, 180] so both directional matches (e.g. ±90 for
                    # square) are treated as the same aspect distance.
                    d = ((planet_long - cusps[cusp_idx] + 180.0) % 360.0) - 180.0
                    abs_sep = -d if d < 0 else d
                    delta = abs_sep - target_deg
                    if (-orb <= delta <= orb):
                        mask |= (1 << bit_idx)
            classified_count += 1
            if mask:
                per_mask_counts[mask] += 1
                matches.append([round(lat, 4), round(lon, 4), mask])
            elif non_matches is not None:
                non_matches.append([round(lat, 4), round(lon, 4)])

    compute_seconds = time.perf_counter() - t_start
    pps = classified_count / compute_seconds if compute_seconds > 0 else 0.0

    # --- Derive per-condition counts and pairwise / triple overlaps.
    # Per-condition count = sum over every mask that contains that bit.
    per_condition_counts = [0] * n_conds
    for mask_value, n in enumerate(per_mask_counts):
        if not n:
            continue
        for bit_idx in range(n_conds):
            if mask_value & (1 << bit_idx):
                per_condition_counts[bit_idx] += n

    def overlap_for(label_set: list[str]) -> int:
        """Count cells whose mask contains ALL of label_set bits set."""
        bits = 0
        for label in label_set:
            bit_idx = _CONDITION_LABELS.index(label)
            if bit_idx >= n_conds:
                return 0
            bits |= (1 << bit_idx)
        total = 0
        for mask_value, n in enumerate(per_mask_counts):
            if n and (mask_value & bits) == bits:
                total += n
        return total

    overlap_report: dict[str, int] = {"any": sum(per_mask_counts)}
    # exclusive single-condition cells: matched X and nothing else
    for bit_idx in range(n_conds):
        only_mask = 1 << bit_idx
        overlap_report[f"{_CONDITION_LABELS[bit_idx]}_only"] = per_mask_counts[only_mask]
    # pairwise overlaps (intersection — may also include the triple)
    if n_conds >= 2:
        from itertools import combinations
        for combo in combinations(range(n_conds), 2):
            labels = [_CONDITION_LABELS[i] for i in combo]
            overlap_report["_and_".join(labels)] = overlap_for(labels)
    # triple overlap
    if n_conds >= 3:
        from itertools import combinations
        for combo in combinations(range(n_conds), 3):
            labels = [_CONDITION_LABELS[i] for i in combo]
            overlap_report["_and_".join(labels)] = overlap_for(labels)

    conditions_report: list[dict[str, Any]] = []
    for bit_idx, preview in enumerate(conditions_report_preview):
        entry = dict(preview)
        entry["count"] = per_condition_counts[bit_idx]
        conditions_report.append(entry)

    response: dict[str, Any] = {
        "matches": matches,
        "properties": {
            "grid_deg": req.grid_deg,
            "lat_count": lat_count,
            "lon_count": lon_count,
            "total_grid_points": total_cells,
            "classified_count": classified_count,
            "match_count": len(matches),
            "non_match_count": classified_count - len(matches),
            "outside_lat_cap_count": capped_count,
            "error_count": error_count,
            "apply_lat_cap": req.apply_lat_cap,
            "compute_seconds": round(compute_seconds, 4),
            "points_per_second": round(pps, 0),
            "conditions": conditions_report,
            # Histogram of mask values exactly as classified. Key is the
            # mask integer encoded as a string (JSON keys must be strings).
            "per_mask_counts": {str(i): n for i, n in enumerate(per_mask_counts) if n},
            "overlap_counts": overlap_report,
            "bounds": {"north": north, "south": south, "east": east, "west": west},
        },
    }
    if non_matches is not None:
        response["non_matches"] = non_matches
    return response


# ---------------------------------------------------------------------------
# Screen-pixel-truth point classifier
# ---------------------------------------------------------------------------
# Diagnostic sibling to /brute-force-grid. Where that endpoint takes a
# regular lat/lon grid (description of the *geography* to sample),
# this one takes an explicit list of (lat, lon) points and classifies
# them one-for-one. It exists so the renderer can drive sampling from
# screen pixels (project each pixel to lat/lon on the client, post the
# list here) without inventing a parallel astrology path.
#
# Astrology math is identical: same condition compilation, same per-
# cell dispatch, same Swiss Ephemeris call. The only difference is the
# *source* of the (lat, lon) pairs — the client supplies them.

class ScreenPixelTruthRequest(BaseModel):
    """Classify an explicit list of geographic points against one or
    more conditions. Used by the screen-pixel-truth diagnostic sandbox.

    The point list is treated as opaque: there is no grid contract, no
    spacing assumption, no de-duplication. Each point is classified
    individually via ``swe.houses`` and tested against every condition;
    the response carries a mask per input point in the same order.

    Renamed away from ``ClassifyPointsRequest`` because that name is
    already taken by the per-point all-houses cache endpoint.
    """

    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    points: list[Any] = Field(
        ..., description="List of [lat, lon] pairs (degrees).",
    )
    conditions: list[Condition] | None = None
    apply_lat_cap: bool = False

    @model_validator(mode="before")
    @classmethod
    def _default_condition_type(cls, data):
        """Same legacy back-compat as BruteForceGridRequest."""
        if isinstance(data, dict):
            conds = data.get("conditions")
            if isinstance(conds, list):
                for c in conds:
                    if isinstance(c, dict) and "type" not in c:
                        if "planet" in c and "house" in c:
                            c["type"] = "planet_in_house"
                        elif "angle" in c and "sign" in c:
                            c["type"] = "angle_in_sign"
                        elif (
                            "planet" in c and "angle" in c and "aspect" in c
                        ):
                            c["type"] = "aspect_to_angle"
        return data


@app.post("/screen-pixel-truth")
def screen_pixel_truth(req: ScreenPixelTruthRequest):
    """Classify an explicit list of (lat, lon) points.

    Returns a dense ``masks`` array (one entry per input point, same
    order) so the client can paint screen pixels block-by-block without
    any index reconciliation. A mask of ``0`` means no condition
    matched at that point.
    """

    t_start = time.perf_counter()

    POINT_CAP = 2_000_000  # bumped: 1480x900 @ block_px=1 = 1.33M points
    n_points = len(req.points)
    if n_points == 0:
        raise HTTPException(status_code=400, detail="points list is empty")
    if n_points > POINT_CAP:
        raise HTTPException(
            status_code=400,
            detail=f"too many points: {n_points} > {POINT_CAP} max",
        )

    if not req.conditions:
        raise HTTPException(
            status_code=400,
            detail="at least one condition is required",
        )
    if len(req.conditions) > _MAX_CONDITIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"too many conditions: {len(req.conditions)} > "
                f"{_MAX_CONDITIONS}"
            ),
        )

    try:
        jd = julian_day(
            req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc
        )
        planets = get_planet_positions(jd)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"chart_init_failed: {e}"
        ) from e

    # Compile conditions into per-cell specs. Same shape and semantics
    # as the brute-force-grid endpoint above (kept duplicated rather
    # than extracted so /brute-force-grid stays untouched).
    cond_specs: list[tuple] = []
    conditions_report_preview: list[dict[str, Any]] = []
    for idx, cond in enumerate(req.conditions):
        label = _CONDITION_LABELS[idx]
        if isinstance(cond, PlanetInHouseCondition):
            planet_name = cond.planet.lower()
            if planet_name not in planets:
                raise HTTPException(
                    status_code=400,
                    detail=f"unknown planet: {cond.planet}",
                )
            if not (1 <= cond.house <= 12):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"house must be 1..12 (got {cond.house} "
                        f"for condition {label})"
                    ),
                )
            cond_specs.append(
                ("pih", cond.house, planets[planet_name], label, planet_name)
            )
            conditions_report_preview.append({
                "id": label,
                "type": "planet_in_house",
                "planet": planet_name,
                "house": cond.house,
            })
        elif isinstance(cond, AngleInSignCondition):
            angle_name = cond.angle.lower()
            sign_name = cond.sign.lower()
            cusp_idx = _ANGLE_TO_CUSP_INDEX[angle_name]
            sign_idx = _ZODIAC_SIGNS.index(sign_name)
            cond_specs.append(
                ("ais", cusp_idx, sign_idx, label, angle_name, sign_name)
            )
            conditions_report_preview.append({
                "id": label,
                "type": "angle_in_sign",
                "angle": angle_name,
                "sign": sign_name,
            })
        elif isinstance(cond, AspectToAngleCondition):
            planet_name = cond.planet.lower()
            if planet_name not in planets:
                raise HTTPException(
                    status_code=400,
                    detail=f"unknown planet: {cond.planet}",
                )
            angle_name = cond.angle.lower()
            aspect_name = cond.aspect.lower()
            cusp_idx = _ANGLE_TO_CUSP_INDEX[angle_name]
            target_deg = _ASPECT_TARGET_DEG[aspect_name]
            cond_specs.append((
                "a2a", cusp_idx, planets[planet_name], target_deg, cond.orb,
                label, planet_name, angle_name, aspect_name,
            ))
            conditions_report_preview.append({
                "id": label,
                "type": "aspect_to_angle",
                "planet": planet_name,
                "angle": angle_name,
                "aspect": aspect_name,
                "orb": cond.orb,
            })
        else:  # pragma: no cover
            raise HTTPException(
                status_code=400,
                detail=f"unsupported condition type at slot {label}",
            )

    n_conds = len(cond_specs)
    cap = CLASSIFY_PRODUCT_LAT_CAP if req.apply_lat_cap else None

    masks: list[int] = [0] * n_points
    per_mask_counts = [0] * (1 << n_conds)
    classified = 0
    capped = 0
    errors = 0
    matches = 0

    for i, pt in enumerate(req.points):
        if len(pt) < 2:
            errors += 1
            continue
        lat = float(pt[0]); lon = float(pt[1])
        if cap is not None and abs(lat) > cap:
            capped += 1
            continue
        try:
            cusps = get_houses(jd, lat, lon)
        except Exception:
            errors += 1
            continue
        classified += 1
        mask = 0
        for bit_idx, spec in enumerate(cond_specs):
            kind = spec[0]
            if kind == "pih":
                _, house, planet_long, *_ = spec
                if planet_in_house(planet_long, house, cusps):
                    mask |= (1 << bit_idx)
            elif kind == "ais":
                _, cusp_idx, sign_idx, *_ = spec
                if int(cusps[cusp_idx] // 30) == sign_idx:
                    mask |= (1 << bit_idx)
            else:  # "a2a"
                _, cusp_idx, planet_long, target_deg, orb, *_ = spec
                d = (
                    (planet_long - cusps[cusp_idx] + 180.0) % 360.0
                ) - 180.0
                abs_sep = -d if d < 0 else d
                delta = abs_sep - target_deg
                if -orb <= delta <= orb:
                    mask |= (1 << bit_idx)
        masks[i] = mask
        if mask:
            per_mask_counts[mask] += 1
            matches += 1

    compute_seconds = time.perf_counter() - t_start
    pps = classified / compute_seconds if compute_seconds > 0 else 0.0

    # Per-condition counts and overlap report. Same derivation as
    # /brute-force-grid so the two endpoints stay comparable.
    per_condition_counts = [0] * n_conds
    for mask_value, n in enumerate(per_mask_counts):
        if not n:
            continue
        for bit_idx in range(n_conds):
            if mask_value & (1 << bit_idx):
                per_condition_counts[bit_idx] += n

    overlap_report: dict[str, int] = {"any": matches}
    for bit_idx in range(n_conds):
        only_mask = 1 << bit_idx
        overlap_report[
            f"{_CONDITION_LABELS[bit_idx]}_only"
        ] = per_mask_counts[only_mask]

    conditions_report: list[dict[str, Any]] = []
    for bit_idx, entry in enumerate(conditions_report_preview):
        entry = dict(entry)
        entry["count"] = per_condition_counts[bit_idx]
        conditions_report.append(entry)

    return {
        "masks": masks,
        "properties": {
            "point_count": n_points,
            "classified_count": classified,
            "match_count": matches,
            "outside_lat_cap_count": capped,
            "error_count": errors,
            "apply_lat_cap": req.apply_lat_cap,
            "compute_seconds": round(compute_seconds, 4),
            "points_per_second": round(pps, 0),
            "conditions": conditions_report,
            "per_mask_counts": {
                str(i): n for i, n in enumerate(per_mask_counts) if n
            },
            "overlap_counts": overlap_report,
        },
    }


@app.get("/aura-refinement-reveal-stages")
def aura_refinement_reveal_stages():
    """Archaeology/debug PoC reveal stage manifest (Sun conjunct ASC only).

    Retained for validation history. Do not use as the production migration
    contract for screen-space overlays.
    """
    from aura_field_engine import REFINEMENT_REVEAL_STAGES, REVEAL_TRANSPORT_VERSION

    return {
        "transport_version": REVEAL_TRANSPORT_VERSION,
        "overlay_scope": "sun_conjunct_asc_poc_only",
        "stages": REFINEMENT_REVEAL_STAGES,
    }


@app.get("/aspect-orb-at-point")
def aspect_orb_at_point(
    lat: float,
    lon: float,
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour_utc: float,
    planet: str = "sun",
    aspect: str = "conjunction",
    angle: str = "ASC",
):
    """Popup-alignment helper: orb distance at one geographic point (PoC overlay)."""
    from aura_field_engine import ASPECT_OFFSETS, PLANET_IDS, _angle_longitude_at_point

    overlay = {"planet": planet, "aspect": aspect, "angle": angle}
    if not is_aura_poc_overlay(overlay):
        raise HTTPException(status_code=400, detail="PoC supports Sun conjunct ASC only")
    jd = julian_day(birth_year, birth_month, birth_day, birth_hour_utc)
    selected_angle = normalize_angle_sign_code(angle)
    planet_id = PLANET_IDS.get(planet.lower())
    if planet_id is None:
        raise HTTPException(status_code=400, detail="Unknown planet")
    ang = _angle_longitude_at_point(jd, lat, lon, selected_angle)
    if ang is None:
        raise HTTPException(status_code=400, detail="Could not evaluate angle at point")
    planet_lon = float(swe.calc_ut(jd, planet_id)[0][0] % 360)
    offsets = ASPECT_OFFSETS.get(aspect.lower(), [0])
    best_orb = 180.0
    for offset in offsets:
        target = (planet_lon + offset) % 360
        orb = abs(aura_signed_angle_diff(ang, target))
        if orb < best_orb:
            best_orb = orb
    max_orb = 6.0
    return {
        "lat": lat,
        "lon": lon,
        "orb_deg": round(best_orb, 4),
        "strength": round(max(0.0, 1.0 - best_orb / max_orb), 4),
        "max_orb": max_orb,
        "aspect_overlay": AURA_POC_OVERLAY,
    }


@app.get("/relocated-chart")
def relocated_chart(
    lat: float,
    lon: float,
    birth_year: int = 1976,
    birth_month: int = 1,
    birth_day: int = 13,
    birth_hour_utc: float = 12.78333
):
    jd = swe.julday(birth_year, birth_month, birth_day, birth_hour_utc)

    cusps_raw, ascmc = swe.houses(jd, lat, lon, b'P')

    asc = ascmc[0] % 360
    mc = ascmc[1] % 360
    desc = (asc + 180) % 360
    ic = (mc + 180) % 360
    cusps = [c % 360 for c in cusps_raw[:12]]

    planets = [
        ("Sun", swe.SUN),
        ("Moon", swe.MOON),
        ("Mercury", swe.MERCURY),
        ("Venus", swe.VENUS),
        ("Mars", swe.MARS),
        ("Jupiter", swe.JUPITER),
        ("Saturn", swe.SATURN),
        ("Uranus", swe.URANUS),
        ("Neptune", swe.NEPTUNE),
        ("Pluto", swe.PLUTO),
        ("Chiron", swe.CHIRON)
    ]

    def get_house(planet_lon, cusps):
        planet_lon = planet_lon % 360
        for i in range(12):
            start = cusps[i] % 360
            end = cusps[(i + 1) % 12] % 360
            if start <= end:
                if start <= planet_lon < end:
                    return i + 1
            else:
                if planet_lon >= start or planet_lon < end:
                    return i + 1
        return None

    planet_houses = {}

    for name, pid in planets:
        try:
            pos = swe.calc_ut(jd, pid)
            planet_lon = pos[0][0] % 360
            house_num = get_house(planet_lon, cusps)
            sep = min_degrees_to_any_cusp(planet_lon, cusps)
            planet_houses[name] = {
                "longitude": planet_lon,
                "longitude_formatted": format_zodiac(planet_lon),
                "house": house_num,
                "cusp_separation_deg": round(sep, 3),
                "near_cusp": bool(sep < 2.0),
            }
        except Exception as e:
            print(f"Error calculating {name}: {e}")
            planet_houses[name] = {
                "longitude": None,
                "longitude_formatted": "Error",
                "house": None,
                "cusp_separation_deg": None,
                "near_cusp": False,
            }

    return {
        "lat": lat,
        "lon": lon,
        "asc": format_zodiac(asc),
        "mc": format_zodiac(mc),
        "desc": format_zodiac(desc),
        "dc": format_zodiac(desc),
        "ic": format_zodiac(ic),
        "asc_sign": zodiac_sign_name(asc),
        "mc_sign": zodiac_sign_name(mc),
        "desc_sign": zodiac_sign_name(desc),
        "dc_sign": zodiac_sign_name(desc),
        "ic_sign": zodiac_sign_name(ic),
        "asc_deg": asc,
        "mc_deg": mc,
        "desc_deg": desc,
        "dc_deg": desc,
        "ic_deg": ic,
        "cusp_transition_visual_deg": 2.0,
        "planet_houses": planet_houses,
    }
@app.get("/health/supabase")
def health_supabase():
    from services.supabase_client import get_supabase

    client = get_supabase()
    result = client.table("profiles").select("id").limit(1).execute()

    return {
        "connected": True,
        "table": "profiles",
        "rows_returned": len(result.data),
    }


@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/chart-profiles")
def get_chart_profiles():
    return load_chart_profiles()


# ---------------------------------------------------------------------------
# Phase 2.0 — account + chart-library scaffold (feature-flag isolated).
# ---------------------------------------------------------------------------
#
# Scope (Phase 2.0):
#   * Local file persistence at ``library/library.json``.
#   * Reuses the existing chart profile shape (id, name, date, time, timezone,
#     place, lat, lon, notes) as the persisted unit so future canonical
#     migration / account sync stays backwards-compatible.
#   * No auth, no payments, no client sharing infrastructure.
#   * Renderer behavior, astrology math, and existing smokes are not touched.
#   * Disabled when ``RM_PHASE2_LIBRARY=0`` so smoke can confirm isolation.
#
# All endpoints under ``/library/*`` return 404 when the flag is off.
# ---------------------------------------------------------------------------

LIBRARY_DIR = APP_DIR / "library"
LIBRARY_FILE = LIBRARY_DIR / "library.json"
LIBRARY_SCHEMA_VERSION = 1


def _library_enabled() -> bool:
    return os.environ.get("RM_PHASE2_LIBRARY", "1") != "0"


def _empty_library_state() -> dict:
    return {
        "schema_version": LIBRARY_SCHEMA_VERSION,
        "charts": [],
        "views": [],
        "favorites": [],
        "active_chart_id": None,
        "settings": {
            "default_substrate": "legacy_search_regions",
            "lat_cap_label_enabled": True,
            "phase2_cache_enabled": False,
            "experimental_mode_enabled": False,
        },
    }


def load_library_state() -> dict:
    if not LIBRARY_FILE.exists():
        return _empty_library_state()
    try:
        with open(LIBRARY_FILE, "r") as fh:
            data = json.load(fh)
    except json.JSONDecodeError:
        return _empty_library_state()
    base = _empty_library_state()
    base.update({k: v for k, v in data.items() if k in base})
    base["settings"] = {**base["settings"], **(data.get("settings") or {})}
    return base


def save_library_state(state: dict) -> None:
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    state["schema_version"] = LIBRARY_SCHEMA_VERSION
    with open(LIBRARY_FILE, "w") as fh:
        json.dump(state, fh, indent=2, sort_keys=False)


class LibraryChartUpsert(BaseModel):
    id: str | None = None
    name: str
    date: str
    time: str
    timezone: str = "UTC"
    place: str = ""
    lat: float = 0.0
    lon: float = 0.0
    notes: str = ""
    favorite: bool = False


class LibraryFavoriteToggle(BaseModel):
    favorite: bool


class LibraryActiveSelection(BaseModel):
    chart_id: str | None


class LibraryViewSave(BaseModel):
    chart_id: str
    label: str = "Saved view"
    north: float
    south: float
    east: float
    west: float
    zoom: float
    center_lat: float | None = None
    center_lon: float | None = None
    conditions: list[dict[str, Any]] = Field(default_factory=list)
    notes: str = ""


class LibrarySettingsPatch(BaseModel):
    default_substrate: str | None = None
    lat_cap_label_enabled: bool | None = None
    phase2_cache_enabled: bool | None = None
    experimental_mode_enabled: bool | None = None


def _ensure_library_enabled() -> None:
    if not _library_enabled():
        raise HTTPException(status_code=404, detail="library scaffold disabled")


def _next_chart_id(state: dict, supplied: str | None) -> str:
    if supplied:
        return supplied
    existing = {c.get("id") for c in state["charts"]}
    n = len(existing) + 1
    while f"lib_chart_{n}" in existing:
        n += 1
    return f"lib_chart_{n}"


def _next_view_id(state: dict) -> str:
    existing = {v.get("id") for v in state["views"]}
    n = len(existing) + 1
    while f"lib_view_{n}" in existing:
        n += 1
    return f"lib_view_{n}"


def _build_share_url(chart_id: str) -> str:
    return f"/library.html?chart={chart_id}"


def _app_shell_enabled() -> bool:
    return os.environ.get("RM_APP_SHELL", "1") != "0"


def _local_product_store_read_enabled() -> bool:
    if _app_shell_enabled():
        return True
    return os.environ.get("RM_PHASE3_LOCAL_PRODUCT", "").strip().lower() in ("1", "true", "yes")


def _ensure_app_shell_enabled() -> None:
    if not _app_shell_enabled():
        raise HTTPException(status_code=404, detail="App shell disabled")


def _ensure_local_product_store_read_enabled() -> None:
    if not _local_product_store_read_enabled():
        raise HTTPException(status_code=404, detail="Local product store read disabled")


LOCAL_PRODUCT_STORE_SCAFFOLD = (
    APP_DIR / "scaffold" / "local_product" / "TEMPORARY_product_store.json"
)


@app.get("/app_shell.html")
def serve_app_shell_html():
    _ensure_app_shell_enabled()
    return FileResponse(APP_DIR / "app_shell.html", media_type="text/html")


@app.get("/local-product-store.json")
def serve_local_product_store_json():
    """Read-only scaffold JSON for app_shell Chart Record library (Store v3)."""
    _ensure_local_product_store_read_enabled()
    if not LOCAL_PRODUCT_STORE_SCAFFOLD.is_file():
        raise HTTPException(status_code=404, detail="Local product store scaffold not found")
    return FileResponse(LOCAL_PRODUCT_STORE_SCAFFOLD, media_type="application/json")


@app.get("/chart-records")
def list_chart_records_api():
    """Read-only Chart Record library summaries (Store v3)."""
    _ensure_local_product_store_read_enabled()
    if not LOCAL_PRODUCT_STORE_SCAFFOLD.is_file():
        raise HTTPException(status_code=404, detail="Local product store scaffold not found")
    state = load_product_store(LOCAL_PRODUCT_STORE_SCAFFOLD)
    return {"chartRecords": list_chart_record_summaries(state)}


@app.get("/chart-records/{chart_record_id}")
def get_chart_record_summary(chart_record_id: str):
    """Read-only Chart Record summary for one record."""
    _ensure_local_product_store_read_enabled()
    if not LOCAL_PRODUCT_STORE_SCAFFOLD.is_file():
        raise HTTPException(status_code=404, detail="Local product store scaffold not found")
    state = load_product_store(LOCAL_PRODUCT_STORE_SCAFFOLD)
    summary = summarize_chart_record(state, chart_record_id)
    if summary is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "chart_record_not_found", "message": f"unknown chart_record_id: {chart_record_id}"},
        )
    return summary


@app.get("/chart-records/{chart_record_id}/engine-birth")
def get_chart_record_engine_birth(chart_record_id: str):
    """Resolve Store v3 Chart Record natal inputs to engine birth parameters."""
    _ensure_local_product_store_read_enabled()
    if not LOCAL_PRODUCT_STORE_SCAFFOLD.is_file():
        raise HTTPException(status_code=404, detail="Local product store scaffold not found")
    try:
        state = load_product_store(LOCAL_PRODUCT_STORE_SCAFFOLD)
        return resolve_engine_birth_params(state, chart_record_id)
    except ChartRecordBirthResolutionError as err:
        status = 404 if err.reason == "chart_record_not_found" else 422
        raise HTTPException(
            status_code=status,
            detail={"error": err.reason, "message": err.message},
        ) from err


@app.get("/library.html")
def serve_library_html():
    _ensure_library_enabled()
    return FileResponse(APP_DIR / "library.html", media_type="text/html")


@app.get("/library/state")
def get_library_state():
    _ensure_library_enabled()
    return load_library_state()


@app.post("/library/charts")
def create_or_update_library_chart(chart: LibraryChartUpsert):
    _ensure_library_enabled()
    state = load_library_state()
    chart_id = _next_chart_id(state, chart.id)
    record = {
        "id": chart_id,
        "name": chart.name,
        "date": chart.date,
        "time": chart.time,
        "timezone": chart.timezone,
        "place": chart.place,
        "lat": chart.lat,
        "lon": chart.lon,
        "notes": chart.notes,
        "favorite": chart.favorite,
        "share_url": _build_share_url(chart_id),
    }
    found = False
    for idx, existing in enumerate(state["charts"]):
        if existing.get("id") == chart_id:
            state["charts"][idx] = {**existing, **record}
            found = True
            break
    if not found:
        state["charts"].append(record)
        if chart.favorite and chart_id not in state["favorites"]:
            state["favorites"].append(chart_id)
    save_library_state(state)
    return record


@app.delete("/library/charts/{chart_id}")
def delete_library_chart(chart_id: str):
    _ensure_library_enabled()
    state = load_library_state()
    state["charts"] = [c for c in state["charts"] if c.get("id") != chart_id]
    state["favorites"] = [f for f in state["favorites"] if f != chart_id]
    state["views"] = [v for v in state["views"] if v.get("chart_id") != chart_id]
    if state.get("active_chart_id") == chart_id:
        state["active_chart_id"] = None
    save_library_state(state)
    return {"deleted": chart_id}


@app.post("/library/charts/{chart_id}/favorite")
def toggle_library_chart_favorite(chart_id: str, body: LibraryFavoriteToggle):
    _ensure_library_enabled()
    state = load_library_state()
    target = None
    for chart in state["charts"]:
        if chart.get("id") == chart_id:
            chart["favorite"] = bool(body.favorite)
            target = chart
            break
    if target is None:
        raise HTTPException(status_code=404, detail="chart not found")
    if body.favorite:
        if chart_id not in state["favorites"]:
            state["favorites"].append(chart_id)
    else:
        state["favorites"] = [f for f in state["favorites"] if f != chart_id]
    save_library_state(state)
    return target


@app.post("/library/active")
def set_library_active(body: LibraryActiveSelection):
    _ensure_library_enabled()
    state = load_library_state()
    if body.chart_id is not None:
        known = {c.get("id") for c in state["charts"]}
        if body.chart_id not in known:
            raise HTTPException(status_code=404, detail="chart not found")
    state["active_chart_id"] = body.chart_id
    save_library_state(state)
    return {"active_chart_id": state["active_chart_id"]}


@app.post("/library/views")
def save_library_view(body: LibraryViewSave):
    _ensure_library_enabled()
    state = load_library_state()
    known = {c.get("id") for c in state["charts"]}
    if body.chart_id not in known:
        raise HTTPException(status_code=404, detail="chart not found")
    view_id = _next_view_id(state)
    record = {
        "id": view_id,
        "chart_id": body.chart_id,
        "label": body.label,
        "viewport": {
            "north": body.north,
            "south": body.south,
            "east": body.east,
            "west": body.west,
            "zoom": body.zoom,
            "center_lat": body.center_lat,
            "center_lon": body.center_lon,
        },
        "conditions": body.conditions,
        "notes": body.notes,
    }
    state["views"].append(record)
    save_library_state(state)
    return record


@app.delete("/library/views/{view_id}")
def delete_library_view(view_id: str):
    _ensure_library_enabled()
    state = load_library_state()
    state["views"] = [v for v in state["views"] if v.get("id") != view_id]
    save_library_state(state)
    return {"deleted": view_id}


@app.put("/library/settings")
def patch_library_settings(body: LibrarySettingsPatch):
    _ensure_library_enabled()
    state = load_library_state()
    incoming = {k: v for k, v in body.model_dump().items() if v is not None}
    state["settings"] = {**state["settings"], **incoming}
    save_library_state(state)
    return state["settings"]

# ---------------------------------------------------------------------------
# Phase 2.0A — Profiles API (Supabase-backed repository passthrough).
# ---------------------------------------------------------------------------


class ProfileCreate(BaseModel):
    display_name: str
    account_user_id: str
    profile_type: str = "human"


class ProfileUpdate(BaseModel):
    display_name: str | None = None
    profile_type: str | None = None


@app.get("/profiles")
def api_list_profiles():
    from repositories.profiles_repository import list_profiles

    return list_profiles()


@app.get("/profiles/{profile_id}")
def api_get_profile(profile_id: str):
    from repositories.profiles_repository import get_profile

    profile = get_profile(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not found")
    return profile


@app.post("/profiles")
def api_create_profile(body: ProfileCreate):
    from repositories.profiles_repository import create_profile

    return create_profile(
        display_name=body.display_name,
        account_user_id=body.account_user_id,
        profile_type=body.profile_type,
    )


@app.patch("/profiles/{profile_id}")
def api_update_profile(profile_id: str, body: ProfileUpdate):
    from repositories.profiles_repository import get_profile, update_profile

    if get_profile(profile_id) is None:
        raise HTTPException(status_code=404, detail="profile not found")
    return update_profile(
        profile_id,
        display_name=body.display_name,
        profile_type=body.profile_type,
    )


@app.post("/profiles/{profile_id}/archive")
def api_archive_profile(profile_id: str):
    from repositories.profiles_repository import archive_profile, get_profile

    if get_profile(profile_id) is None:
        raise HTTPException(status_code=404, detail="profile not found")
    return archive_profile(profile_id)


# ---------------------------------------------------------------------------
# Phase 2.0B — Birth Records API (Supabase-backed repository passthrough).
# ---------------------------------------------------------------------------


class BirthRecordCreate(BaseModel):
    profile_id: str
    birth_date: str | None = None
    birth_time_mode: str | None = None
    birth_time_start: str | None = None
    birth_time_end: str | None = None
    birth_place_id: str | None = None
    timezone_id: str | None = None
    utc_datetime_start: str | None = None
    utc_datetime_end: str | None = None
    confidence_notes: str | None = None
    chart_settings_json: dict | None = None


class BirthRecordUpdate(BaseModel):
    birth_date: str | None = None
    birth_time_mode: str | None = None
    birth_time_start: str | None = None
    birth_time_end: str | None = None
    birth_place_id: str | None = None
    timezone_id: str | None = None
    utc_datetime_start: str | None = None
    utc_datetime_end: str | None = None
    confidence_notes: str | None = None
    chart_settings_json: dict | None = None


@app.get("/birth-records/{profile_id}")
def api_list_birth_records(profile_id: str):
    from repositories.birth_records_repository import list_birth_records

    return list_birth_records(profile_id)


@app.get("/birth-record/{record_id}")
def api_get_birth_record(record_id: str):
    from repositories.birth_records_repository import get_birth_record

    record = get_birth_record(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="birth record not found")
    return record


@app.post("/birth-records")
def api_create_birth_record(body: BirthRecordCreate):
    from repositories.birth_records_repository import create_birth_record

    return create_birth_record(
        profile_id=body.profile_id,
        birth_date=body.birth_date,
        birth_time_mode=body.birth_time_mode,
        birth_time_start=body.birth_time_start,
        birth_time_end=body.birth_time_end,
        birth_place_id=body.birth_place_id,
        timezone_id=body.timezone_id,
        utc_datetime_start=body.utc_datetime_start,
        utc_datetime_end=body.utc_datetime_end,
        confidence_notes=body.confidence_notes,
        chart_settings_json=body.chart_settings_json,
    )


@app.patch("/birth-record/{record_id}")
def api_update_birth_record(record_id: str, body: BirthRecordUpdate):
    from repositories.birth_records_repository import (
        get_birth_record,
        update_birth_record,
    )

    if get_birth_record(record_id) is None:
        raise HTTPException(status_code=404, detail="birth record not found")
    return update_birth_record(
        record_id,
        birth_date=body.birth_date,
        birth_time_mode=body.birth_time_mode,
        birth_time_start=body.birth_time_start,
        birth_time_end=body.birth_time_end,
        birth_place_id=body.birth_place_id,
        timezone_id=body.timezone_id,
        utc_datetime_start=body.utc_datetime_start,
        utc_datetime_end=body.utc_datetime_end,
        confidence_notes=body.confidence_notes,
        chart_settings_json=body.chart_settings_json,
    )


@app.post("/birth-record/{record_id}/archive")
def api_archive_birth_record(record_id: str):
    from repositories.birth_records_repository import (
        archive_birth_record,
        get_birth_record,
    )

    if get_birth_record(record_id) is None:
        raise HTTPException(status_code=404, detail="birth record not found")
    return archive_birth_record(record_id)


# ---------------------------------------------------------------------------
# Phase 2.0C — Places API (Supabase-backed repository passthrough).
# ---------------------------------------------------------------------------


class PlaceCreate(BaseModel):
    display_name: str
    latitude: float
    longitude: float
    provider: str | None = None
    provider_place_id: str | None = None
    geonames_id: str | None = None
    canonical_name: str | None = None
    admin1: str | None = None
    admin2: str | None = None
    country_code: str | None = None
    country_name: str | None = None
    timezone_id: str | None = None
    population: int | None = None
    importance_rank: float | None = None
    language_code: str | None = None
    alternate_names_json: dict | None = None
    source_json: dict | None = None


@app.get("/places")
def api_list_places(limit: int = 50):
    from repositories.places_repository import list_places

    return list_places(limit)


@app.get("/places/search")
def api_search_places(q: str, limit: int = 20):
    from repositories.places_repository import search_places

    return search_places(q, limit)


@app.get("/place/{place_id}")
def api_get_place(place_id: str):
    from repositories.places_repository import get_place

    try:
        place = get_place(place_id)
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise HTTPException(status_code=404, detail="place not found") from e
        raise
    if place is None:
        raise HTTPException(status_code=404, detail="place not found")
    return place


@app.post("/places")
def api_create_place(body: PlaceCreate):
    from repositories.places_repository import create_place

    return create_place(
        display_name=body.display_name,
        latitude=body.latitude,
        longitude=body.longitude,
        provider=body.provider,
        provider_place_id=body.provider_place_id,
        geonames_id=body.geonames_id,
        canonical_name=body.canonical_name,
        admin1=body.admin1,
        admin2=body.admin2,
        country_code=body.country_code,
        country_name=body.country_name,
        timezone_id=body.timezone_id,
        population=body.population,
        importance_rank=body.importance_rank,
        language_code=body.language_code,
        alternate_names_json=body.alternate_names_json,
        source_json=body.source_json,
    )


# ---------------------------------------------------------------------------
# Phase 2.0D — Saved Searches API (Supabase-backed repository passthrough).
# ---------------------------------------------------------------------------


class SavedSearchCreate(BaseModel):
    profile_id: str
    title: str
    intention_profile_id: str | None = None
    search_type: str | None = None
    conditions_json: dict | None = None
    viewport_json: dict | None = None
    settings_snapshot_json: dict | None = None
    date_start: str | None = None
    date_end: str | None = None


class SavedSearchUpdate(BaseModel):
    title: str | None = None
    intention_profile_id: str | None = None
    search_type: str | None = None
    conditions_json: dict | None = None
    viewport_json: dict | None = None
    settings_snapshot_json: dict | None = None
    date_start: str | None = None
    date_end: str | None = None


@app.get("/saved-searches/{profile_id}")
def api_list_saved_searches(profile_id: str):
    from repositories.saved_searches_repository import list_saved_searches

    return list_saved_searches(profile_id)


@app.get("/saved-search/{saved_search_id}")
def api_get_saved_search(saved_search_id: str):
    from repositories.saved_searches_repository import get_saved_search

    try:
        saved_search = get_saved_search(saved_search_id)
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise HTTPException(status_code=404, detail="saved search not found") from e
        raise
    if saved_search is None:
        raise HTTPException(status_code=404, detail="saved search not found")
    return saved_search


@app.post("/saved-searches")
def api_create_saved_search(body: SavedSearchCreate):
    from repositories.saved_searches_repository import create_saved_search

    return create_saved_search(
        profile_id=body.profile_id,
        title=body.title,
        intention_profile_id=body.intention_profile_id,
        search_type=body.search_type,
        conditions_json=body.conditions_json,
        viewport_json=body.viewport_json,
        settings_snapshot_json=body.settings_snapshot_json,
        date_start=body.date_start,
        date_end=body.date_end,
    )


@app.patch("/saved-search/{saved_search_id}")
def api_update_saved_search(saved_search_id: str, body: SavedSearchUpdate):
    from repositories.saved_searches_repository import (
        get_saved_search,
        update_saved_search,
    )

    try:
        existing = get_saved_search(saved_search_id)
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise HTTPException(status_code=404, detail="saved search not found") from e
        raise
    if existing is None:
        raise HTTPException(status_code=404, detail="saved search not found")
    return update_saved_search(
        saved_search_id,
        title=body.title,
        intention_profile_id=body.intention_profile_id,
        search_type=body.search_type,
        conditions_json=body.conditions_json,
        viewport_json=body.viewport_json,
        settings_snapshot_json=body.settings_snapshot_json,
        date_start=body.date_start,
        date_end=body.date_end,
    )


@app.post("/saved-search/{saved_search_id}/archive")
def api_archive_saved_search(saved_search_id: str):
    from repositories.saved_searches_repository import (
        archive_saved_search,
        get_saved_search,
    )

    try:
        existing = get_saved_search(saved_search_id)
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise HTTPException(status_code=404, detail="saved search not found") from e
        raise
    if existing is None:
        raise HTTPException(status_code=404, detail="saved search not found")
    return archive_saved_search(saved_search_id)


# ---------------------------------------------------------------------------
# Phase 2.0E — Comparison Sets API (Supabase-backed repository passthrough).
# ---------------------------------------------------------------------------


def _comparison_set_or_404(comparison_set_id: str):
    from repositories.comparison_sets_repository import get_comparison_set

    try:
        existing = get_comparison_set(comparison_set_id)
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise HTTPException(status_code=404, detail="comparison set not found") from e
        raise
    if existing is None:
        raise HTTPException(status_code=404, detail="comparison set not found")
    return existing


class ComparisonSetCreate(BaseModel):
    profile_id: str
    title: str
    intention_profile_id: str | None = None
    settings_snapshot_json: dict | None = None


class ComparisonSetUpdate(BaseModel):
    title: str | None = None
    intention_profile_id: str | None = None
    settings_snapshot_json: dict | None = None


class ComparisonSetPlaceAdd(BaseModel):
    place_id: str
    sort_order: int = 0
    role: str | None = None


@app.get("/comparison-sets/{profile_id}")
def api_list_comparison_sets(profile_id: str):
    from repositories.comparison_sets_repository import list_comparison_sets

    return list_comparison_sets(profile_id)


@app.get("/comparison-set/{comparison_set_id}")
def api_get_comparison_set(comparison_set_id: str):
    return _comparison_set_or_404(comparison_set_id)


@app.post("/comparison-sets")
def api_create_comparison_set(body: ComparisonSetCreate):
    from repositories.comparison_sets_repository import create_comparison_set

    return create_comparison_set(
        profile_id=body.profile_id,
        title=body.title,
        intention_profile_id=body.intention_profile_id,
        settings_snapshot_json=body.settings_snapshot_json,
    )


@app.patch("/comparison-set/{comparison_set_id}")
def api_update_comparison_set(comparison_set_id: str, body: ComparisonSetUpdate):
    from repositories.comparison_sets_repository import update_comparison_set

    _comparison_set_or_404(comparison_set_id)
    return update_comparison_set(
        comparison_set_id,
        title=body.title,
        intention_profile_id=body.intention_profile_id,
        settings_snapshot_json=body.settings_snapshot_json,
    )


@app.post("/comparison-set/{comparison_set_id}/archive")
def api_archive_comparison_set(comparison_set_id: str):
    from repositories.comparison_sets_repository import archive_comparison_set

    _comparison_set_or_404(comparison_set_id)
    return archive_comparison_set(comparison_set_id)


@app.get("/comparison-set/{comparison_set_id}/places")
def api_list_comparison_set_places(comparison_set_id: str):
    from repositories.comparison_sets_repository import list_comparison_set_places

    _comparison_set_or_404(comparison_set_id)
    return list_comparison_set_places(comparison_set_id)


@app.post("/comparison-set/{comparison_set_id}/places")
def api_add_place_to_comparison_set(comparison_set_id: str, body: ComparisonSetPlaceAdd):
    from repositories.comparison_sets_repository import add_place_to_comparison_set

    _comparison_set_or_404(comparison_set_id)
    return add_place_to_comparison_set(
        comparison_set_id=comparison_set_id,
        place_id=body.place_id,
        sort_order=body.sort_order,
        role=body.role,
    )


@app.delete("/comparison-set/{comparison_set_id}/places/{place_id}")
def api_remove_place_from_comparison_set(comparison_set_id: str, place_id: str):
    from repositories.comparison_sets_repository import remove_place_from_comparison_set

    _comparison_set_or_404(comparison_set_id)
    return remove_place_from_comparison_set(comparison_set_id, place_id)


# ---------------------------------------------------------------------------
# Phase 2.0F — Favorite Places API (Supabase-backed repository passthrough).
# ---------------------------------------------------------------------------


def _favorite_place_or_404(favorite_place_id: str):
    from repositories.favorite_places_repository import get_favorite_place

    try:
        existing = get_favorite_place(favorite_place_id)
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise HTTPException(status_code=404, detail="favorite place not found") from e
        raise
    if existing is None:
        raise HTTPException(status_code=404, detail="favorite place not found")
    return existing


class FavoritePlaceCreate(BaseModel):
    profile_id: str
    place_id: str
    intention_profile_id: str | None = None
    label: str | None = None
    rank: int | None = None
    starred: bool | None = None


class FavoritePlaceUpdate(BaseModel):
    intention_profile_id: str | None = None
    label: str | None = None
    rank: int | None = None
    starred: bool | None = None


@app.get("/favorite-places/{profile_id}")
def api_list_favorite_places(profile_id: str):
    from repositories.favorite_places_repository import list_favorite_places

    return list_favorite_places(profile_id)


@app.get("/favorite-place/{favorite_place_id}")
def api_get_favorite_place(favorite_place_id: str):
    return _favorite_place_or_404(favorite_place_id)


@app.post("/favorite-places")
def api_create_favorite_place(body: FavoritePlaceCreate):
    from repositories.favorite_places_repository import create_favorite_place

    return create_favorite_place(
        profile_id=body.profile_id,
        place_id=body.place_id,
        intention_profile_id=body.intention_profile_id,
        label=body.label,
        rank=body.rank,
        starred=body.starred,
    )


@app.patch("/favorite-place/{favorite_place_id}")
def api_update_favorite_place(favorite_place_id: str, body: FavoritePlaceUpdate):
    from repositories.favorite_places_repository import update_favorite_place

    _favorite_place_or_404(favorite_place_id)
    return update_favorite_place(
        favorite_place_id,
        intention_profile_id=body.intention_profile_id,
        label=body.label,
        rank=body.rank,
        starred=body.starred,
    )


@app.post("/favorite-place/{favorite_place_id}/archive")
def api_archive_favorite_place(favorite_place_id: str):
    from repositories.favorite_places_repository import archive_favorite_place

    _favorite_place_or_404(favorite_place_id)
    return archive_favorite_place(favorite_place_id)


# ---------------------------------------------------------------------------
# Phase 2.0G — Visited Places API (Supabase-backed repository passthrough).
# Note: no update/archive endpoints — schema has no updated_at/archived_at.
# ---------------------------------------------------------------------------


class VisitedPlaceCreate(BaseModel):
    profile_id: str
    place_id: str
    visited_at: str | None = None
    source: str | None = None
    notes: str | None = None


@app.get("/visited-places/{profile_id}")
def api_list_visited_places(profile_id: str):
    from repositories.visited_places_repository import list_visited_places

    return list_visited_places(profile_id)


@app.get("/visited-place/{visited_place_id}")
def api_get_visited_place(visited_place_id: str):
    from repositories.visited_places_repository import get_visited_place

    try:
        visited_place = get_visited_place(visited_place_id)
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "22P02" in msg or "invalid input syntax for type uuid" in msg:
            raise HTTPException(status_code=404, detail="visited place not found") from e
        raise
    if visited_place is None:
        raise HTTPException(status_code=404, detail="visited place not found")
    return visited_place


@app.post("/visited-places")
def api_create_visited_place(body: VisitedPlaceCreate):
    from repositories.visited_places_repository import create_visited_place

    return create_visited_place(
        profile_id=body.profile_id,
        place_id=body.place_id,
        visited_at=body.visited_at,
        source=body.source,
        notes=body.notes,
    )
