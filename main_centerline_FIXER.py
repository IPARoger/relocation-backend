from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

import swisseph as swe
import os
swe.set_ephe_path(os.path.join(os.path.dirname(__file__), "ephe"))
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import measure
from skimage.measure import approximate_polygon

app = FastAPI()

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

class SearchRequest(BaseModel):
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour_utc: float
    house_conditions: List[Condition]
    resolution: float = 1.5
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

def planet_in_house(planet_long, house_num, cusps):
    start = cusps[house_num - 1]
    end = cusps[house_num % 12]

    if start <= end:
        return start <= planet_long < end

    return planet_long >= start or planet_long < end


def signed_angle_diff(a, b):
    return ((a - b + 180) % 360) - 180


def format_zodiac(deg):

    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces"
    ]

    deg = deg % 360

    sign_index = int(deg // 30)

    sign_deg = deg % 30

    whole_deg = int(sign_deg)

    minutes = int((sign_deg - whole_deg) * 60)

    return f"{whole_deg}° {signs[sign_index]} {minutes:02d}'"
        
@app.post("/search-regions")
def search_regions(req: SearchRequest):
    jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
    planets = get_planet_positions(jd)

    lat_grid = np.arange(-60, 86, req.resolution)
    lon_grid = np.arange(-180, 181, req.resolution)

    features = []
    aspect_features = []

    # =====================================
    # HOUSE REGION SEARCH
    # =====================================
    for idx, cond in enumerate(req.house_conditions):
        mask = np.zeros((len(lat_grid), len(lon_grid)), dtype=np.uint8)
        planet_long = planets[cond.planet.lower()]

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
                    "properties": {"condition_index": idx, "overlap_count": 1}
                })

    # =====================================
    # ASPECT OVERLAY (MC and ASC)
    # =====================================
    if req.aspect_overlay:
        selected_planet = req.aspect_overlay.get("planet", "sun").lower()
        selected_angle = req.aspect_overlay.get("angle", "MC").upper()

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
                0: "#00e5ff", 180: "#ff4444", 90: "#ff9900", 270: "#ff9900",
                120: "#00cc66", 240: "#00cc66", 60: "#bb66ff", 300: "#bb66ff"
            }

            offsets = aspect_sets.get(req.aspect_overlay.get("aspect", "conjunction").lower(), [0])

            for offset in offsets:
                target_ra = (planet_ra_deg + offset) % 360
                target_lon = (planet_lon + offset) % 360

                print(
                    "ASPECT DEBUG",
                    req.aspect_overlay.get("aspect"),
                    "OFFSET:", offset,
                    "TARGET_LON:", target_lon
                )

                # =====================================
                # MC CALCULATION
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
                            "color": aspect_colors.get(offset, "#00e5ff"),
                            "weight": 4,
                            "opacity": 0.95
                        }
                    })

                # =====================================
                # ASC CALCULATION
                # =====================================
                if selected_angle == "ASC":
                    lat_vals = np.arange(-65, 66, 0.5)
                    lon_vals = np.arange(-180, 181, 0.5)

                    diff_grid = np.full(
                        (len(lat_vals), len(lon_vals)),
                        np.nan
                    )

                    for i, lat in enumerate(lat_vals):
                        for j, lon in enumerate(lon_vals):
                            try:
                                cusps, ascmc = swe.houses(jd, lat, lon, b'P')
                                asc = ascmc[0] % 360

                                diff = signed_angle_diff(
                                    asc,
                                    target_lon
                                )

                                if abs(diff) < 90:
                                    diff_grid[i, j] = diff

                            except Exception:
                                pass

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
                                    "angle": "ASC",
                                    "aspect_offset": offset,
                                    "color": aspect_colors.get(offset, "#00e5ff"),
                                    "weight": 2,
                                    "opacity": 1.0
                                }
                            })
                        
        return {
            "type": "FeatureCollection",
            "features": features + aspect_features
        }
@app.get("/relocated-chart")
def relocated_chart(lat: float, lon: float):

    jd = swe.julday(
        1976,
        1,
        13,
        12.78333
    )

    cusps, ascmc = swe.houses(
        jd,
        lat,
        lon,
        b'P'
    )

    asc = ascmc[0] % 360
    mc = ascmc[1] % 360
    desc = (asc + 180) % 360
    ic = (mc + 180) % 360

    return {

        "lat": lat,
        "lon": lon,

        "asc": format_zodiac(asc),
        "mc": format_zodiac(mc),
        "desc": format_zodiac(desc),
        "ic": format_zodiac(ic),

        "asc_deg": asc,
        "mc_deg": mc,
        "desc_deg": desc,
        "ic_deg": ic
    }
@app.get("/health")
def health():
    return {"status": "ok"}