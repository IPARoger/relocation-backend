from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

import swisseph as swe
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import measure
from skimage.measure import approximate_polygon

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# DATA MODELS
# =====================================

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
    resolution: float = 0.5

# =====================================
# ASTRO HELPERS
# =====================================

def julian_day(year, month, day, hour_utc):
    return swe.julday(year, month, day, hour_utc)

def get_planet_positions(jd):

    planets = {
        "sun": swe.SUN,
        "moon": swe.MOON,
        "mercury": swe.MERCURY,
        "venus": swe.VENUS,
        "mars": swe.MARS,
        "jupiter": swe.JUPITER,
        "saturn": swe.SATURN,
        "uranus": swe.URANUS,
        "neptune": swe.NEPTUNE,
        "pluto": swe.PLUTO
    }

    result = {}

    for name, pid in planets.items():
        result[name] = swe.calc_ut(jd, pid)[0][0] % 360

    return result

def get_houses(jd, lat, lon):

    cusps, _ = swe.houses(
        jd,
        lat,
        lon,
        b'P'
    )

    return [c % 360 for c in cusps[:12]]

def planet_in_house(planet_long, house_num, cusps):

    start = cusps[house_num - 1]
    end = cusps[house_num % 12]

    if start <= end:
        return start <= planet_long < end

    return planet_long >= start or planet_long < end

# =====================================
# API
# =====================================

@app.post("/search-regions")
def search_regions(req: SearchRequest):

    jd = julian_day(
        req.birth_year,
        req.birth_month,
        req.birth_day,
        req.birth_hour_utc
    )

    planets = get_planet_positions(jd)

    # Expanded north latitude fixes top clipping
    lat_grid = np.arange(
        -60,
        86,
        req.resolution
    )

    lon_grid = np.arange(
        -180,
        181,
        req.resolution
    )

    features = []

    for idx, cond in enumerate(req.house_conditions):

        mask = np.zeros(
            (
                len(lat_grid),
                len(lon_grid)
            ),
            dtype=np.uint8
        )

        planet_long = planets[
            cond.planet.lower()
        ]

        # =====================================
        # BUILD MASK
        # =====================================

        for i, lat in enumerate(lat_grid):

            for j, lon in enumerate(lon_grid):

                try:

                    cusps = get_houses(
                        jd,
                        lat,
                        lon
                    )

                    if planet_in_house(
                        planet_long,
                        cond.house,
                        cusps
                    ):

                        mask[i, j] = 1

                except:
                    pass

        # =====================================
        # SMOOTH MASK
        # =====================================

        smooth_mask = gaussian_filter(
            mask.astype(float),
            sigma=1.2
        )

        # =====================================
        # FIND CONTOURS
        # =====================================

        contours = measure.find_contours(
            smooth_mask,
            0.35
        )

        # =====================================
        # PROCESS CONTOURS
        # =====================================

        for contour in contours:

            if len(contour) < 20:
                continue

            contour = approximate_polygon(
                contour,
                tolerance=0.08
            )

            coords = []

            for point in contour:

                lat_f = point[0]
                lon_f = point[1]

                if (
                    0 <= lat_f < len(lat_grid) - 1
                    and
                    0 <= lon_f < len(lon_grid) - 1
                ):

                    lat_i = int(lat_f)
                    lon_i = int(lon_f)

                    lat_frac = lat_f - lat_i
                    lon_frac = lon_f - lon_i

                    lat = (
                        lat_grid[lat_i] * (1 - lat_frac)
                        +
                        lat_grid[lat_i + 1] * lat_frac
                    )

                    lon = (
                        lon_grid[lon_i] * (1 - lon_frac)
                        +
                        lon_grid[lon_i + 1] * lon_frac
                    )

                    coords.append([
                        float(lon),
                        float(lat)
                    ])

            if len(coords) >= 3:

                features.append({

                    "type": "Feature",

                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coords]
                    },

                    "properties": {
                        "condition_index": idx,
                        "overlap_count": 1
                    }

                })

    return {
        "type": "FeatureCollection",
        "features": features
    }

# =====================================
# HEALTH
# =====================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }