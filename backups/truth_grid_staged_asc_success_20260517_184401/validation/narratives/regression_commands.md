# Regression Commands

Run commands from the repository root:

`/Users/davegoodman/Desktop/relocation-backend`

## Start Server

```bash
./venv/bin/python -m uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000
```

If port `8000` is already in use, stop the old server first or restart the terminal running it.

## Open Manual QA URL

```bash
open "http://127.0.0.1:8000/map_CURRENT.html?generation_mode=truth_grid&debugGeometry=1"
```

The same URL can be pasted directly into Chrome:

`http://127.0.0.1:8000/map_CURRENT.html?generation_mode=truth_grid&debugGeometry=1`

## Quick Served-route Smoke Test

```bash
./venv/bin/python - <<'PY'
from urllib import request

for url in [
    "http://127.0.0.1:8000/map_CURRENT.html?generation_mode=truth_grid&debugGeometry=1",
    "http://127.0.0.1:8000/cities.js",
    "http://127.0.0.1:8000/health",
]:
    with request.urlopen(url, timeout=10) as response:
        print(response.status, response.headers.get("content-type"), url)
PY
```

## Truth-grid API Smoke Test

```bash
./venv/bin/python - <<'PY'
import json
from urllib import request

payload = {
    "birth_year": 1988,
    "birth_month": 6,
    "birth_day": 21,
    "birth_hour_utc": 3.2,
    "house_conditions": [{"planet": "sun", "house": 7}],
    "generation_mode": "truth_grid",
    "truth_grid_resolution": 0.75,
    "resolution": 1.5
}

req = request.Request(
    "http://127.0.0.1:8000/search-regions",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with request.urlopen(req, timeout=30) as response:
    data = json.loads(response.read())

polygons = [feature for feature in data["features"] if feature["geometry"]["type"] == "Polygon"]
contradictions = sum(feature["properties"].get("validation_contradictions", 0) for feature in polygons)
print("generation_mode:", data["properties"]["generation_mode"])
print("resolution:", data["properties"]["truth_grid"]["resolution"])
print("polygon_count:", len(polygons))
print("validation_contradictions:", contradictions)
PY
```

Expected:

- `generation_mode: truth_grid`
- `resolution: 0.75`
- `polygon_count` greater than `0`
- `validation_contradictions: 0`

## Truth-field Prototype / Merge Benchmark

Still applicable for payload and merge-regression checks:

```bash
./venv/bin/python truth_field_regions.py --benchmark-merge --write-validation-records --output-dir validation_screenshots/truth-field-prototype
```

Single-house prototype run:

```bash
./venv/bin/python truth_field_regions.py --house 7 --output-dir validation_screenshots/truth-field-prototype
```

## Integration Validation Scripts

No standalone integration validation script is currently checked in. The latest browser/API validation outputs are saved as:

- `validation/reports/served_truth_grid_debug_url_check.json`
- `validation/reports/truth_grid_frontend_integration_check.json`
- `validation/reports/async_overlay_decoupling_check.json`
- `validation/reports/house_789_async_overlay_check.json`

Use the manual QA checklist plus the smoke tests above until those checks are promoted into a reusable script.

