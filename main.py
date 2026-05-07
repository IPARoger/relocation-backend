from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple, Set
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
    resolution: float = 0.5

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

def evaluate_point(jd, lat, lon, conditions, planets):
    try:
        cusps = get_houses(jd, lat, lon)
        for cond in conditions:
            planet_long = planets[cond.planet.lower()]
            if planet_in_house(planet_long, cond.house, cusps):
                return 1
    except:
        pass
    return 0

@app.post("/search-regions")
def search_regions(req: SearchRequest):
    jd = julian_day(req.birth_year, req.birth_month, req.birth_day, req.birth_hour_utc)
    planets = get_planet_positions(jd)
    conditions = req.house_conditions

    coarse_lat = np.arange(-60, 76, 5)
    coarse_lon = np.arange(-180, 181, 5)
    
    coarse_mask = np.zeros((len(coarse_lat), len(coarse_lon)), dtype=np.uint8)
    
    for i, lat in enumerate(coarse_lat):
        for j, lon in enumerate(coarse_lon):
            coarse_mask[i, j] = evaluate_point(jd, lat, lon, conditions, planets)
    
    edge_cells = set()
    for i in range(len(coarse_lat)):
        for j in range(len(coarse_lon)):
            val = coarse_mask[i, j]
            for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < len(coarse_lat) and 0 <= nj < len(coarse_lon):
                    if coarse_mask[ni, nj] != val:
                        edge_cells.add((i, j))
                        edge_cells.add((ni, nj))
                        break
    
    if not edge_cells:
        return {"type": "FeatureCollection", "features": []}
    
    min_lat_i = min(i for i, _ in edge_cells)
    max_lat_i = max(i for i, _ in edge_cells)
    min_lon_j = min(j for _, j in edge_cells)
    max_lon_j = max(j for _, j in edge_cells)
    
    lat_start = coarse_lat[min_lat_i]
    lat_end = coarse_lat[max_lat_i] + 5
    lon_start = coarse_lon[min_lon_j]
    lon_end = coarse_lon[max_lon_j] + 5
    
    fine_lat = np.arange(lat_start, lat_end, req.resolution)
    fine_lon = np.arange(lon_start, lon_end, req.resolution)
    
    fine_mask = np.zeros((len(fine_lat), len(fine_lon)), dtype=np.uint8)
    
    for i, lat in enumerate(fine_lat):
        for j, lon in enumerate(fine_lon):
            fine_mask[i, j] = evaluate_point(jd, lat, lon, conditions, planets)
    
    features = []
    
    if np.any(fine_mask):
        contours = measure.find_contours(fine_mask, 0.5)
        
        for contour in contours:
            coords = []
            for point in contour:
                lat_f = point[0]
                lon_f = point[1]
                if 0 <= lat_f < len(fine_lat)-1 and 0 <= lon_f < len(fine_lon)-1:
                    lat_i = int(lat_f)
                    lon_i = int(lon_f)
                    lat_frac = lat_f - lat_i
                    lon_frac = lon_f - lon_i
                    lat = fine_lat[lat_i] * (1 - lat_frac) + fine_lat[lat_i + 1] * lat_frac
                    lon = fine_lon[lon_i] * (1 - lon_frac) + fine_lon[lon_i + 1] * lon_frac
                    coords.append([float(lon), float(lat)])
            if len(coords) >= 3:
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [coords]},
                    "properties": {"condition_index": 0, "overlap_count": 1}
                })
    
    return {"type": "FeatureCollection", "features": features}

@app.get("/health")
def health():
    return {"status": "ok"}
