import swisseph as swe
import numpy as np
import os
import json
from skimage import measure

swe.set_ephe_path(os.path.join(os.path.dirname(__file__), "ephe"))

# ==========================================
# CONFIG
# ==========================================

YEAR = 1990
MONTH = 1
DAY = 1
HOUR = 12.0

PLANET = swe.SUN

ASPECTS = {
    "trine": [120, 240]
}

ASPECT_COLORS = {
    "conjunction": "#ff0000",
    "opposition": "#ff8800",
    "square": "#ffff00",
    "trine": "#00ff00",
    "sextile": "#00ffff"
}

ORB = 1.0

LAT_STEP = 0.5
LON_STEP = 0.5

OUTPUT = "all_aspects_truth.geojson"

# ==========================================
# BIRTH CHART
# ==========================================

jd = swe.julday(YEAR, MONTH, DAY, HOUR)

planet_lon = swe.calc_ut(jd, PLANET)[0][0] % 360

# ==========================================
# GRID
# ==========================================

lat_grid = np.arange(-60, 61, LAT_STEP)
lon_grid = np.arange(-180, 181, LON_STEP)

features = []

# ==========================================
# BUILD TRUE MASKS
# ==========================================

for aspect_name, offsets in ASPECTS.items():

    color = ASPECT_COLORS[aspect_name]

    for offset in offsets:

        target = (planet_lon + offset) % 360

        print(f"building {aspect_name} {offset}")

        mask = np.full(
            (len(lat_grid), len(lon_grid)),
            999.0
        )

        # BUILD ERROR FIELD

        for i, lat in enumerate(lat_grid):

            print(f"lat {lat}")

            for j, lon in enumerate(lon_grid):

                try:

                    houses = swe.houses(
                        jd,
                        lat,
                        lon,
                        b'P'
                    )

                    asc = houses[1][0] % 360

                    diff = abs(
                        ((asc - target + 180) % 360) - 180
                    )
                    if diff > 30:
                        diff = 999

                    mask[i, j] = diff

                except:
                    pass

        print("extracting contours...")

        # WRAP LONGITUDE SEAM

        extended_mask = np.concatenate(
            [mask[:, -20:], mask, mask[:, :20]],
            axis=1
        )

        # EXTRACT CONTOURS

        contours = measure.find_contours(
            extended_mask,
            ORB
        )

        # CONVERT TO GEOJSON

        for contour in contours:

            coords = []

            for point in contour:

                row = point[0]
                col = point[1]

                lat = np.interp(
                    row,
                    np.arange(len(lat_grid)),
                    lat_grid
                )

                wrapped_col = col - 20

                lon = np.interp(
                    wrapped_col,
                    np.arange(len(lon_grid)),
                    lon_grid
                )

                lon = ((lon + 180) % 360) - 180

                coords.append([
                    float(lon),
                    float(lat)
                ])

            if len(coords) > 10:

                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords
                    },
                    "properties": {
                        "aspect": aspect_name,
                        "color": color,
                        "offset": offset
                    }
                })

# ==========================================
# EXPORT
# ==========================================

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open(OUTPUT, "w") as f:
    json.dump(geojson, f)

print(f"saved {OUTPUT}")