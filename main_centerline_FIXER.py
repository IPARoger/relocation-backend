from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

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
    return_all_houses: bool = False
    aspect_resolution: float = 0.5
    overlay_stage: str | None = None
    aspect_overlay: dict | None = None

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
            req.return_all_houses
        )
    else:
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
@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/chart-profiles")
def get_chart_profiles():
    return load_chart_profiles()