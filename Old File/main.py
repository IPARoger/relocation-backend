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
                "conjunction": [0], "opposition": [180], "square": [90, 270],
                "trine": [120, 240], "sextile": [60, 300],
                "hard": [0, 90, 180, 270], "soft": [60, 120, 240, 300],
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

                    # Gradient bands
                    for band_dist, opacity, weight in [
                        (1, 0.22, 8),
                        (2, 0.16, 7),
                        (3, 0.11, 6),
                        (4, 0.07, 5),
                        (5, 0.045, 4),
                        (6, 0.025, 3)
                    ]:

                        for direction in [-1, 1]:

                            band_lon = mc_lon + (band_dist * direction)

                            while band_lon > 180:
                                band_lon -= 360

                            while band_lon < -180:
                                band_lon += 360

                            aspect_features.append({
                                "type": "Feature",
                                "geometry": {
                                    "type": "LineString",
                                    "coordinates": [[band_lon, -85], [band_lon, 85]]
                                },
                                "properties": {
                                    "planet": selected_planet,
                                    "angle": "MC",
                                    "color": aspect_colors.get(offset, "#00e5ff"),
                                    "weight": weight,
                                    "opacity": opacity
                                }
                            })

                if selected_angle == "ASC":

                    all_roots = []

                    for lon in np.arange(-180, 181, 1.5):

                        lon_roots = []

                        prev_diff = None
                        prev_lat = None

                        for lat in np.arange(-70, 71, 0.6):

                            try:
                                houses = swe.houses(jd, lat, lon, b'P')
                                asc = houses[1][0] % 360

                                diff = ((asc - target_lon + 180) % 360) - 180

                                if prev_diff is not None:

                                    # reject wraparound discontinuities
                                    if (
                                        diff * prev_diff < 0
                                        and abs(lat - prev_lat) < 10
                                    ):

                                        t = abs(prev_diff) / (abs(prev_diff) + abs(diff))
                                        crossing_lat = prev_lat + t * (lat - prev_lat)

                                        lon_roots.append(crossing_lat)                                
                                prev_diff = diff
                                prev_lat = lat

                            except:
                                pass

                        all_roots.append({
                            "lon": lon,
                            "roots": lon_roots
                        })

                    # BUILD CONTINUOUS BRANCHES
                    branches = []

                    MAX_LAT_JUMP = 12  # degrees

                    for row in all_roots:

                        lon = row["lon"]
                        roots = row["roots"]

                        used = set()

                        # Try to extend existing branches
                        for branch in branches:

                            last_lon, last_lat = branch[-1]

                            lon_gap = abs(lon - last_lon)

                            if lon_gap > 5:
                                continue

                            best_root = None
                            best_dist = 999

                            for i, lat in enumerate(roots):

                                if i in used:
                                    continue

                                from math import cos, radians, sqrt

                                dx = (lon - last_lon) * cos(radians(lat))
                                dy = lat - last_lat

                                dist = sqrt(dx * dx + dy * dy)

                                # penalize sudden direction reversals
                                if len(branch) >= 2:
                                    prev_lat = branch[-2][1]
                                    trend = last_lat - prev_lat
                                    candidate_trend = lat - last_lat

                                    if trend * candidate_trend < 0:
                                        dist += 200
                                if dist < best_dist:
                                    best_dist = dist
                                    best_root = (i, lat)

                            if (
                                best_root and (
                                    best_dist < MAX_LAT_JUMP or
                                    abs(lat) > 55
                                )
                            ):
                                i, lat = best_root

                                branch.append([float(lon), float(lat)])

                                used.add(i)

                        # Create new branches for unmatched roots
                        for i, lat in enumerate(roots):

                            if i not in used:

                                branches.append([
                                    [float(lon), float(lat)]
                                ])

                    # DRAW BRANCHES
                    aspect_name = req.aspect_overlay.get("aspect", "").lower()

                    if aspect_name in ["conjunction", "opposition"]:
                        MAX_BRANCHES = 1
                    else:
                        MAX_BRANCHES = 2
                    MIN_BRANCH_POINTS = 2

                    branches = [
                        b for b in branches
                        if len(b) >= MIN_BRANCH_POINTS
                    ]
                    branches.sort(key=len, reverse=True)
                    branches = branches[:MAX_BRANCHES]
                                        
                    for coords in branches:

                        aspect_features.append({
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",
                                "coordinates": coords
                            },
                            "properties": {
                                "planet": selected_planet,
                                "angle": "ASC",
                                "color": aspect_colors.get(offset, "#00e5ff"),
                                "weight": 4,
                                "opacity": 0.9
                            }
                        })
                            
                    

            return {
                "type": "FeatureCollection",
                "features": features + aspect_features
            }
@app.get("/health")
def health():
    return {"status": "ok"}