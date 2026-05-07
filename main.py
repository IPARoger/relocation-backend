from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple, Set, Dict
import swisseph as swe
import numpy as np
from skimage import measure

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

def julian_day(year, month, day, hour_utc):
    return swe.julday(year, month, day, hour_utc)

def get_planet_positions(jd):
    planets = {
        "sun": swe.SUN, "moon": swe.MOON, "mercury": swe.MERCURY,
        "venus": swe.VENUS, "mars": swe.MARS, "jupiter": swe.JUPITER,
        "saturn": swe.SATURN, "uranus": swe.URANUS,
        "neptune": swe.NEPTUNE, "pluto": swe.PLUTO
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

def get_condition_mask(jd, lat_grid, lon_grid, conditions, planets):
    """Return mask where each cell is a bitmask of which conditions are true"""
    mask = np.zeros((len(lat_grid), len(lon_grid)), dtype=np.uint8)
    
    for i, lat in enumerate(lat_grid):
        for j, lon in enumerate(lon_grid):
            try:
                cusps = get_houses(jd, lat, lon)
                bits = 0
                for idx, cond in enumerate(conditions):
                    planet_long = planets[cond.planet.lower()]
                    if planet_in_house(planet_long, cond.house, cusps):
                        bits |= (1 << idx)
                mask[i, j] = bits
            except:
                pass
    return mask

@app.post("/search-regions")
def search_regions(req: SearchRequest):
    jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
    planets = get_planet_positions(jd)
    conditions = req.house_conditions
    
    lat_grid = np.arange(-60, 76, 0.5)
    lon_grid = np.arange(-180, 181, 0.5)
    
    mask = get_condition_mask(jd, lat_grid, lon_grid, conditions, planets)
    
    features = []
    
    # Define colors for each combination (bitmask 1-7)
    # 1 (001) = A only, 2 (010) = B only, 4 (100) = C only
    # 3 (011) = A+B, 5 (101) = A+C, 6 (110) = B+C, 7 (111) = A+B+C
    color_map = {
        1: "#f1c40f",  # A only - yellow
        2: "#ff4d6d",  # B only - pink
        4: "#3b82f6",  # C only - blue
        3: "#ff9900",  # A+B - orange
        5: "#44cc66",  # A+C - green
        6: "#aa66ff",  # B+C - purple
        7: "#ffffff"   # A+B+C - white
    }
    
    for bit_val in color_map.keys():
        bit_mask = (mask == bit_val).astype(np.uint8)
        if np.any(bit_mask):
            contours = measure.find_contours(bit_mask, 0.5)
            for contour in contours:
                coords = []
                for point in contour:
                    lat_f = point[0]
                    lon_f = point[1]
                    if 0 <= lat_f < len(lat_grid)-1 and 0 <= lon_f < len(lon_grid)-1:
                        lat_i = int(lat_f)
                        lon_i = int(lon_f)
                        lat_frac = lat_f - lat_i
                        lon_frac = lon_f - lon_i
                        lat = lat_grid[lat_i] * (1 - lat_frac) + lat_grid[lat_i + 1] * lat_frac
                        lon = lon_grid[lon_i] * (1 - lon_frac) + lon_grid[lon_i + 1] * lon_frac
                        coords.append([float(lon), float(lat)])
                if len(coords) >= 3:
                    features.append({
                        "type": "Feature",
                        "geometry": {"type": "Polygon", "coordinates": [coords]},
                        "properties": {
                            "condition_index": bit_val,
                            "overlap_count": bin(bit_val).count("1"),
                            "color": color_map[bit_val]
                        }
                    })
    
    return {"type": "FeatureCollection", "features": features}

@app.get("/health")
def health():
    return {"status": "ok"}
