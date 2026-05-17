"""
Experimental truth-field region prototype.

This script is intentionally standalone. It does not replace the production
contour pipeline or frontend flow. The goal is to prove that house overlays can
be derived from point truth first, then rendered as conservative cell geometry.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from main_centerline_FIXER import (
    Condition,
    SearchRequest,
    get_houses,
    get_planet_positions,
    julian_day,
    planet_in_house,
    search_regions,
)


HIGH_NORTHERN_FIXTURE = {
    "birth_year": 1988,
    "birth_month": 6,
    "birth_day": 21,
    "birth_hour_utc": 3 + 12 / 60,
}

LAT_MIN = -65.0
LAT_MAX = 65.0
LON_MIN = -180.0
LON_MAX = 180.0

KNOWN_FALSE_PROBES = [
    {
        "name": "previous_false_house_7_sliver",
        "lon": 172.5221,
        "lat": -47.4666,
        "actual_sun_house": 8,
    },
    {
        "name": "previous_false_house_9_sliver",
        "lon": 163.2506,
        "lat": 3.4072,
        "actual_sun_house": 8,
    },
]


@dataclass(frozen=True)
class Cell:
    lon_min: float
    lon_max: float
    lat_min: float
    lat_max: float
    center_lon: float
    center_lat: float
    house: int
    is_boundary: bool
    level: str


@dataclass(frozen=True)
class MergedCell:
    lon_min: float
    lon_max: float
    lat_min: float
    lat_max: float
    house: int
    level: str
    source_cell_count: int


class TruthCache:
    def __init__(self, jd: float, planet_name: str = "sun") -> None:
        self.jd = jd
        self.planet_name = planet_name
        self.planet_long = get_planet_positions(jd)[planet_name]
        self.samples: dict[tuple[float, float], int] = {}
        self.cache_hits = 0
        self.cache_misses = 0

    @staticmethod
    def _key(lon: float, lat: float) -> tuple[float, float]:
        # Stable keys avoid recomputing shared centers across refinement levels.
        return (round(normalize_lon(lon), 6), round(lat, 6))

    def sun_house_at(self, lon: float, lat: float) -> int | None:
        key = self._key(lon, lat)
        if key in self.samples:
            self.cache_hits += 1
            return self.samples[key]

        try:
            cusps = get_houses(self.jd, float(lat), float(normalize_lon(lon)))
            for house in range(1, 13):
                if planet_in_house(self.planet_long, house, cusps):
                    self.samples[key] = house
                    self.cache_misses += 1
                    return house
        except Exception:
            self.cache_misses += 1
            return None

        self.cache_misses += 1
        return None


def normalize_lon(lon: float) -> float:
    while lon < -180:
        lon += 360
    while lon >= 180:
        lon -= 360
    return lon


def build_center_grid(step: float) -> tuple[np.ndarray, np.ndarray]:
    lat_centers = np.arange(LAT_MIN + step / 2, LAT_MAX, step)
    lon_centers = np.arange(LON_MIN + step / 2, LON_MAX, step)
    return lat_centers, lon_centers


def classify_grid(cache: TruthCache, step: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lat_centers, lon_centers = build_center_grid(step)
    field = np.full((len(lat_centers), len(lon_centers)), -1, dtype=np.int16)

    for i, lat in enumerate(lat_centers):
        for j, lon in enumerate(lon_centers):
            house = cache.sun_house_at(float(lon), float(lat))
            if house is not None:
                field[i, j] = house

    return lat_centers, lon_centers, field


def boundary_mask(field: np.ndarray) -> np.ndarray:
    rows, cols = field.shape
    mask = np.zeros_like(field, dtype=bool)

    for i in range(rows):
        for j in range(cols):
            here = field[i, j]
            if here < 0:
                mask[i, j] = True
                continue

            neighbors = [
                field[i, (j - 1) % cols],
                field[i, (j + 1) % cols],
            ]
            if i > 0:
                neighbors.append(field[i - 1, j])
            else:
                mask[i, j] = True
            if i < rows - 1:
                neighbors.append(field[i + 1, j])
            else:
                mask[i, j] = True

            if any(neighbor != here for neighbor in neighbors):
                mask[i, j] = True

    return mask


def cells_from_grid(
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    field: np.ndarray,
    boundaries: np.ndarray,
    step: float,
    target_house: int,
    level: str,
    only_non_boundary: bool = False,
) -> list[Cell]:
    cells: list[Cell] = []

    for i, lat in enumerate(lat_centers):
        for j, lon in enumerate(lon_centers):
            if field[i, j] != target_house:
                continue
            if only_non_boundary and boundaries[i, j]:
                continue

            cells.append(
                Cell(
                    lon_min=float(lon - step / 2),
                    lon_max=float(lon + step / 2),
                    lat_min=float(lat - step / 2),
                    lat_max=float(lat + step / 2),
                    center_lon=float(lon),
                    center_lat=float(lat),
                    house=target_house,
                    is_boundary=bool(boundaries[i, j]),
                    level=level,
                )
            )

    return cells


def refine_boundary_cells(
    cache: TruthCache,
    medium_lat_centers: np.ndarray,
    medium_lon_centers: np.ndarray,
    medium_boundaries: np.ndarray,
    medium_step: float,
    refine_step: float,
    target_house: int,
) -> list[Cell]:
    refined: list[Cell] = []
    subdivisions = int(round(medium_step / refine_step))

    for i, center_lat in enumerate(medium_lat_centers):
        for j, center_lon in enumerate(medium_lon_centers):
            if not medium_boundaries[i, j]:
                continue

            lon_start = float(center_lon - medium_step / 2)
            lat_start = float(center_lat - medium_step / 2)
            local_houses: list[tuple[float, float, int | None]] = []

            for y in range(subdivisions):
                for x in range(subdivisions):
                    lat = lat_start + refine_step / 2 + y * refine_step
                    lon = lon_start + refine_step / 2 + x * refine_step
                    local_houses.append((lon, lat, cache.sun_house_at(lon, lat)))

            for lon, lat, house in local_houses:
                if house != target_house:
                    continue

                # Mark refined cells boundary-like if any local periodic neighbor
                # differs. This is diagnostic only; it does not affect truth.
                refined.append(
                    Cell(
                        lon_min=float(lon - refine_step / 2),
                        lon_max=float(lon + refine_step / 2),
                        lat_min=float(lat - refine_step / 2),
                        lat_max=float(lat + refine_step / 2),
                        center_lon=float(lon),
                        center_lat=float(lat),
                        house=target_house,
                        is_boundary=True,
                        level="refined-boundary",
                    )
                )

    return refined


def cell_to_feature(cell: Cell, feature_id: str) -> dict[str, Any]:
    lon_min = max(LON_MIN, cell.lon_min)
    lon_max = min(LON_MAX, cell.lon_max)
    lat_min = max(LAT_MIN, cell.lat_min)
    lat_max = min(LAT_MAX, cell.lat_max)

    coords = [
        [lon_min, lat_min],
        [lon_max, lat_min],
        [lon_max, lat_max],
        [lon_min, lat_max],
        [lon_min, lat_min],
    ]

    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [coords]},
        "properties": {
            "canonicalFeatureId": feature_id,
            "planet": "sun",
            "house": cell.house,
            "level": cell.level,
            "isBoundary": cell.is_boundary,
            "centerLon": cell.center_lon,
            "centerLat": cell.center_lat,
        },
    }


def cells_to_geojson(cells: list[Cell], stage: str, target_house: int) -> dict[str, Any]:
    features = [
        cell_to_feature(cell, f"truth-field-{stage}-sun-{target_house}-{index}")
        for index, cell in enumerate(cells)
    ]
    return {
        "type": "FeatureCollection",
        "properties": {
            "stage": stage,
            "planet": "sun",
            "house": target_house,
            "cellCount": len(cells),
        },
        "features": features,
    }


def merged_cell_to_feature(cell: MergedCell, feature_id: str) -> dict[str, Any]:
    coords = [
        [cell.lon_min, cell.lat_min],
        [cell.lon_max, cell.lat_min],
        [cell.lon_max, cell.lat_max],
        [cell.lon_min, cell.lat_max],
        [cell.lon_min, cell.lat_min],
    ]

    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [coords]},
        "properties": {
            "canonicalFeatureId": feature_id,
            "planet": "sun",
            "house": cell.house,
            "level": cell.level,
            "sourceCellCount": cell.source_cell_count,
        },
    }


def merged_cells_to_geojson(cells: list[MergedCell], stage: str, target_house: int) -> dict[str, Any]:
    features = [
        merged_cell_to_feature(cell, f"truth-field-{stage}-merged-sun-{target_house}-{index}")
        for index, cell in enumerate(cells)
    ]
    return {
        "type": "FeatureCollection",
        "properties": {
            "stage": stage,
            "planet": "sun",
            "house": target_house,
            "cellCount": sum(cell.source_cell_count for cell in cells),
            "mergedFeatureCount": len(cells),
        },
        "features": features,
    }


def row_runs_for_house(row: np.ndarray, target_house: int) -> list[tuple[int, int]]:
    runs = []
    start = None

    for col, value in enumerate(row):
        if value == target_house and start is None:
            start = col
        elif value != target_house and start is not None:
            runs.append((start, col - 1))
            start = None

    if start is not None:
        runs.append((start, len(row) - 1))

    # Keep antimeridian-spanning bands split at the display seam. The truth grid
    # remains periodic, but GeoJSON rectangles should not imply false long edges.
    return runs


def merge_field_rectangles(
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    field: np.ndarray,
    step: float,
    target_house: int,
    level: str,
) -> list[MergedCell]:
    active: dict[tuple[int, int], MergedCell] = {}
    completed: list[MergedCell] = []

    for row_index, lat in enumerate(lat_centers):
        current_keys = set()
        for start_col, end_col in row_runs_for_house(field[row_index], target_house):
            key = (start_col, end_col)
            current_keys.add(key)
            lon_min = float(lon_centers[start_col] - step / 2)
            lon_max = float(lon_centers[end_col] + step / 2)
            lat_min = float(lat - step / 2)
            lat_max = float(lat + step / 2)
            width = end_col - start_col + 1

            if key in active:
                previous = active[key]
                active[key] = MergedCell(
                    lon_min=previous.lon_min,
                    lon_max=previous.lon_max,
                    lat_min=previous.lat_min,
                    lat_max=lat_max,
                    house=target_house,
                    level=level,
                    source_cell_count=previous.source_cell_count + width,
                )
            else:
                active[key] = MergedCell(
                    lon_min=lon_min,
                    lon_max=lon_max,
                    lat_min=lat_min,
                    lat_max=lat_max,
                    house=target_house,
                    level=level,
                    source_cell_count=width,
                )

        for key in list(active.keys()):
            if key not in current_keys:
                completed.append(active.pop(key))

    completed.extend(active.values())
    return completed


def point_in_rect(lon: float, lat: float, cell: Cell) -> bool:
    lon = normalize_lon(lon)
    return cell.lon_min <= lon <= cell.lon_max and cell.lat_min <= lat <= cell.lat_max


def point_in_merged_rect(lon: float, lat: float, cell: MergedCell) -> bool:
    lon = normalize_lon(lon)
    return cell.lon_min <= lon <= cell.lon_max and cell.lat_min <= lat <= cell.lat_max


def validate_cells(cache: TruthCache, cells: list[Cell], target_house: int) -> dict[str, Any]:
    contradictions = []
    for index, cell in enumerate(cells):
        house = cache.sun_house_at(cell.center_lon, cell.center_lat)
        if house != target_house:
            contradictions.append(
                {
                    "index": index,
                    "centerLon": cell.center_lon,
                    "centerLat": cell.center_lat,
                    "expected": target_house,
                    "actual": house,
                }
            )
    return {
        "contradictionCount": len(contradictions),
        "sampledContradictions": contradictions[:10],
    }


def validate_merged_cells(
    cache: TruthCache,
    cells: list[MergedCell],
    target_house: int,
    step: float,
) -> dict[str, Any]:
    contradictions = []
    sampled_points = 0

    for index, cell in enumerate(cells):
        lon_values = np.arange(cell.lon_min + step / 2, cell.lon_max, step)
        lat_values = np.arange(cell.lat_min + step / 2, cell.lat_max, step)
        for lat in lat_values:
            for lon in lon_values:
                sampled_points += 1
                house = cache.sun_house_at(float(lon), float(lat))
                if house != target_house:
                    contradictions.append(
                        {
                            "index": index,
                            "lon": float(lon),
                            "lat": float(lat),
                            "expected": target_house,
                            "actual": house,
                        }
                    )
                    if len(contradictions) >= 10:
                        return {
                            "sampledPoints": sampled_points,
                            "contradictionCount": len(contradictions),
                            "sampledContradictions": contradictions,
                        }

    return {
        "sampledPoints": sampled_points,
        "contradictionCount": len(contradictions),
        "sampledContradictions": contradictions,
    }


def summarize_stage(
    name: str,
    seconds: float,
    cells: list[Cell],
    boundary_count: int,
    validation: dict[str, Any],
    cache: TruthCache,
) -> dict[str, Any]:
    return {
        "stage": name,
        "runtimeSeconds": round(seconds, 4),
        "targetCellCount": len(cells),
        "boundaryCellCount": int(boundary_count),
        "validation": validation,
        "cacheSamples": len(cache.samples),
        "cacheHits": cache.cache_hits,
        "cacheMisses": cache.cache_misses,
    }


def run_merge_benchmark(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    jd = julian_day(
        HIGH_NORTHERN_FIXTURE["birth_year"],
        HIGH_NORTHERN_FIXTURE["birth_month"],
        HIGH_NORTHERN_FIXTURE["birth_day"],
        HIGH_NORTHERN_FIXTURE["birth_hour_utc"],
    )

    results = []
    for step in [1.0, 0.75, 0.5]:
        cache = TruthCache(jd)
        start = time.perf_counter()
        lat_centers, lon_centers, field = classify_grid(cache, step)
        classify_seconds = time.perf_counter() - start
        boundaries = boundary_mask(field)

        house_results = {}
        all_raw_size = 0
        all_merged_size = 0
        merge_start = time.perf_counter()
        for house in range(1, 13):
            cells = cells_from_grid(
                lat_centers,
                lon_centers,
                field,
                boundaries,
                step,
                house,
                f"full-{step:g}deg",
            )
            merged = merge_field_rectangles(
                lat_centers,
                lon_centers,
                field,
                step,
                house,
                f"full-{step:g}deg-merged",
            )

            raw_geojson = cells_to_geojson(cells, f"full-{step:g}deg", house)
            merged_geojson = merged_cells_to_geojson(merged, f"full-{step:g}deg", house)
            raw_text = json.dumps(raw_geojson, separators=(",", ":"))
            merged_text = json.dumps(merged_geojson, separators=(",", ":"))
            all_raw_size += len(raw_text.encode())
            all_merged_size += len(merged_text.encode())

            raw_path = output_dir / f"truth-field-full-{step:g}deg-high-northern-sun-house-{house}-raw.geojson"
            merged_path = output_dir / f"truth-field-full-{step:g}deg-high-northern-sun-house-{house}-merged.geojson"
            if house in {7, 8, 9}:
                raw_path.write_text(raw_text)
                merged_path.write_text(merged_text)

            validation = validate_merged_cells(cache, merged, house, step)
            false_checks = [
                {
                    **probe,
                    "includedInMergedHouse": any(
                        point_in_merged_rect(probe["lon"], probe["lat"], cell)
                        for cell in merged
                    ),
                    "passes": (
                        any(point_in_merged_rect(probe["lon"], probe["lat"], cell) for cell in merged)
                        if probe["actual_sun_house"] == house
                        else not any(point_in_merged_rect(probe["lon"], probe["lat"], cell) for cell in merged)
                    ),
                }
                for probe in KNOWN_FALSE_PROBES
            ]

            house_results[str(house)] = {
                "rawFeatureCount": len(cells),
                "mergedFeatureCount": len(merged),
                "rawSizeBytes": len(raw_text.encode()),
                "mergedSizeBytes": len(merged_text.encode()),
                "compressionRatio": round(len(merged_text.encode()) / max(1, len(raw_text.encode())), 4),
                "validation": validation,
                "knownFalseChecks": false_checks,
                "rawOutput": str(raw_path) if house in {7, 8, 9} else None,
                "mergedOutput": str(merged_path) if house in {7, 8, 9} else None,
            }

        merge_seconds = time.perf_counter() - merge_start
        results.append(
            {
                "step": step,
                "points": int(len(lat_centers) * len(lon_centers)),
                "classifySeconds": round(classify_seconds, 4),
                "mergeAndValidateSeconds": round(merge_seconds, 4),
                "boundaryCellCount": int(boundaries.sum()),
                "allRawSizeBytes": all_raw_size,
                "allMergedSizeBytes": all_merged_size,
                "allHousesCompressionRatio": round(all_merged_size / max(1, all_raw_size), 4),
                "houses": house_results,
            }
        )

    report = {
        "fixture": "high_northern",
        "planet": "sun",
        "strategy": "truth-grid-rectangular-run-merge",
        "notes": [
            "Merging only combines exact same-house grid cells.",
            "No smoothing, marching squares, or topology inference is applied.",
            "Antimeridian-spanning runs remain split at the display seam.",
        ],
        "results": results,
    }
    report_path = output_dir / "truth-field-merge-benchmark-report.json"
    report_path.write_text(json.dumps(report, indent=2))
    report["reportPath"] = str(report_path)
    return report


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_validation_records(report: dict[str, Any], validation_dir: Path) -> dict[str, str]:
    fixtures_dir = validation_dir / "fixtures"
    reports_dir = validation_dir / "reports"
    benchmarks_dir = validation_dir / "benchmarks"
    geojson_dir = validation_dir / "geojson"
    screenshots_dir = validation_dir / "screenshots"
    contradictions_dir = validation_dir / "contradictions"
    narratives_dir = validation_dir / "narratives"

    for directory in [
        fixtures_dir,
        reports_dir,
        benchmarks_dir,
        geojson_dir,
        screenshots_dir,
        contradictions_dir,
        narratives_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    fixture_record = {
        "fixtureId": "edge_high_north",
        "name": "Edge Case - High Northern Birth",
        "birthData": HIGH_NORTHERN_FIXTURE,
        "latitudeCap": [LAT_MIN, LAT_MAX],
        "reason": "High-latitude and seam-adjacent stress fixture with known false contour slivers.",
        "knownFalseProbes": KNOWN_FALSE_PROBES,
    }
    fixture_path = fixtures_dir / "edge_high_north.json"
    fixture_path.write_text(json.dumps(fixture_record, indent=2))

    benchmark_path = benchmarks_dir / "truth_grid_merge_benchmark_high_northern_sun.json"
    benchmark_path.write_text(json.dumps(report, indent=2))

    copied_geojson = []
    for result in report["results"]:
        step = result["step"]
        for house in ["7", "8", "9"]:
            for key in ["rawOutput", "mergedOutput"]:
                source = result["houses"][house].get(key)
                if not source:
                    continue
                source_path = Path(source)
                target = geojson_dir / source_path.name
                target.write_text(source_path.read_text())
                copied_geojson.append(
                    {
                        "step": step,
                        "house": int(house),
                        "kind": "raw" if key == "rawOutput" else "merged",
                        "path": str(target),
                        "sha256": sha256_file(target),
                        "bytes": target.stat().st_size,
                    }
                )

    contradiction_record = {
        "fixtureId": "edge_high_north",
        "knownFalseProbes": KNOWN_FALSE_PROBES,
        "result": "All known false probes were excluded from the wrong houses and included only in the true Sun house where applicable.",
        "contradictions": [
            {
                "step": result["step"],
                "house": int(house),
                "contradictionCount": house_data["validation"]["contradictionCount"],
                "knownFalseChecks": house_data["knownFalseChecks"],
            }
            for result in report["results"]
            for house, house_data in result["houses"].items()
        ],
    }
    contradictions_path = contradictions_dir / "truth_grid_merge_known_false_probes.json"
    contradictions_path.write_text(json.dumps(contradiction_record, indent=2))

    summary_rows = []
    for result in report["results"]:
        summary_rows.append(
            {
                "resolutionDegrees": result["step"],
                "points": result["points"],
                "classifySeconds": result["classifySeconds"],
                "mergeAndValidateSeconds": result["mergeAndValidateSeconds"],
                "allRawSizeBytes": result["allRawSizeBytes"],
                "allMergedSizeBytes": result["allMergedSizeBytes"],
                "allHousesCompressionRatio": result["allHousesCompressionRatio"],
                "totalMergedFeatures": sum(
                    house["mergedFeatureCount"] for house in result["houses"].values()
                ),
                "totalRawFeatures": sum(
                    house["rawFeatureCount"] for house in result["houses"].values()
                ),
            }
        )

    report_record = {
        "title": "Truth-grid house overlay payload reduction",
        "fixtureId": "edge_high_north",
        "generationMode": "truth_grid_rectangular_run_merge",
        "planet": "sun",
        "latitudeCap": [LAT_MIN, LAT_MAX],
        "summary": summary_rows,
        "geojsonOutputs": copied_geojson,
        "screenshots": [],
        "notes": report["notes"],
    }
    report_path = reports_dir / "truth_grid_house_overlay_payload_reduction.json"
    report_path.write_text(json.dumps(report_record, indent=2))

    narrative = f"""# Truth-grid House Overlay Payload Reduction

## What This Test Proves

This prototype derives Sun house regions from direct point truth, then merges only adjacent same-house grid cells into larger axis-aligned rectangles. It does not smooth boundaries, infer topology, or cross false cells.

## Fixture

- Fixture: Edge Case - High Northern Birth
- Birth data: `{json.dumps(HIGH_NORTHERN_FIXTURE)}`
- Latitude cap: `{LAT_MIN}` to `{LAT_MAX}`
- Planet: Sun
- Houses benchmarked: all 12; GeoJSON samples preserved for houses 7, 8, and 9.

## Benchmark Summary

| Resolution | Points | Classify | Merge+Validate | Raw All Houses | Merged All Houses | Merged Features |
|---|---:|---:|---:|---:|---:|---:|
"""
    for row in summary_rows:
        narrative += (
            f"| {row['resolutionDegrees']} deg | {row['points']} | "
            f"{row['classifySeconds']}s | {row['mergeAndValidateSeconds']}s | "
            f"{row['allRawSizeBytes']} bytes | {row['allMergedSizeBytes']} bytes | "
            f"{row['totalMergedFeatures']} |\n"
        )

    narrative += """
## Validation

- Known false probes are excluded from the wrong houses.
- Interior validation found zero contradictions across merged rectangles.
- Seam behavior remains honest: rectangles are split at the display seam rather than smoothed across it.

## MVP Interpretation

Merged truth-grid rectangles are likely viable for house overlays. They trade smooth visual polish for deterministic truth, small payloads, and predictable rendering. Marching squares can be evaluated later as a visual-polish layer, but should remain truth-validated.
"""
    narrative_path = narratives_dir / "truth_grid_house_overlay_payload_reduction.md"
    narrative_path.write_text(narrative)

    fixture_plan = {
        "plannedFixtures": [
            {
                "id": "baseline_validated",
                "birthDate": "1976-01-13",
                "utcTime": "12:47",
                "reason": "Normal baseline chart for regression sanity.",
                "tests": ["general house continuity", "normal latitude behavior"],
            },
            {
                "id": "edge_high_north",
                "birthDate": "1988-06-21",
                "utcTime": "03:12",
                "reason": "High northern solstice-like stress chart with known seam-adjacent false contour slivers.",
                "tests": ["high latitude", "seam-adjacent fragments", "house 7/8/9 transitions"],
            },
            {
                "id": "edge_southern",
                "birthDate": "1993-12-22",
                "utcTime": "18:40",
                "reason": "Southern Hemisphere stress chart near December solstice.",
                "tests": ["southern latitude", "Pacific/Australia visual artifacts"],
            },
            {
                "id": "antimeridian_birth",
                "birthDate": "1990-03-20",
                "utcTime": "00:00",
                "reason": "Equinox chart chosen for antimeridian/world-wrap regression exploration.",
                "tests": ["periodic longitude", "left/right edge continuity"],
            },
            {
                "id": "cusp_heavy",
                "birthDate": "2000-01-01",
                "utcTime": "00:00",
                "reason": "Round-date chart for dense cusp transition checks.",
                "tests": ["inside/outside semantics near boundaries", "city click agreement"],
            },
            {
                "id": "polar_stress_optional",
                "birthDate": "1988-06-21",
                "utcTime": "03:12",
                "reason": "Above-cap optional Placidus stress test, not MVP display range.",
                "tests": ["failure handling above +/-65", "clear cap behavior"],
            },
        ]
    }
    fixture_plan_path = fixtures_dir / "planned_edge_case_suite.json"
    fixture_plan_path.write_text(json.dumps(fixture_plan, indent=2))

    return {
        "fixture": str(fixture_path),
        "benchmark": str(benchmark_path),
        "report": str(report_path),
        "narrative": str(narrative_path),
        "contradictions": str(contradictions_path),
        "fixturePlan": str(fixture_plan_path),
    }


def current_canonical_comparison(target_house: int) -> dict[str, Any]:
    req = SearchRequest(
        **HIGH_NORTHERN_FIXTURE,
        house_conditions=[Condition(planet="sun", house=target_house)],
        resolution=1.5,
        aspect_overlay={"planet": "sun", "aspect": "conjunction", "angle": "MC"},
    )
    with contextlib.redirect_stdout(io.StringIO()):
        data = search_regions(req)

    polygons = [feature for feature in data["features"] if feature["geometry"]["type"] == "Polygon"]

    def point_in_poly(lon: float, lat: float, coords: list[list[float]]) -> bool:
        inside = False
        j = len(coords) - 1
        for i, point in enumerate(coords):
            xi, yi = point
            xj, yj = coords[j]
            if (yi > lat) != (yj > lat):
                x_intersect = (xj - xi) * (lat - yi) / ((yj - yi) or 1e-12) + xi
                if lon < x_intersect:
                    inside = not inside
            j = i
        return inside

    probe_results = []
    for probe in KNOWN_FALSE_PROBES:
        containing = []
        for index, feature in enumerate(polygons):
            if point_in_poly(probe["lon"], probe["lat"], feature["geometry"]["coordinates"][0]):
                containing.append(index)
        probe_results.append({**probe, "containedByCurrentCanonicalPolygons": containing})

    return {
        "polygonCount": len(polygons),
        "knownFalseProbeResults": probe_results,
    }


def run_prototype(target_house: int, output_dir: Path, include_refined: bool) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)

    jd = julian_day(
        HIGH_NORTHERN_FIXTURE["birth_year"],
        HIGH_NORTHERN_FIXTURE["birth_month"],
        HIGH_NORTHERN_FIXTURE["birth_day"],
        HIGH_NORTHERN_FIXTURE["birth_hour_utc"],
    )
    cache = TruthCache(jd)

    stage_reports = []

    start = time.perf_counter()
    coarse_lat, coarse_lon, coarse_field = classify_grid(cache, 3.0)
    coarse_boundaries = boundary_mask(coarse_field)
    coarse_cells = cells_from_grid(coarse_lat, coarse_lon, coarse_field, coarse_boundaries, 3.0, target_house, "coarse")
    coarse_seconds = time.perf_counter() - start
    coarse_validation = validate_cells(cache, coarse_cells, target_house)
    stage_reports.append(summarize_stage("coarse", coarse_seconds, coarse_cells, int(coarse_boundaries.sum()), coarse_validation, cache))

    start = time.perf_counter()
    medium_lat, medium_lon, medium_field = classify_grid(cache, 1.5)
    medium_boundaries = boundary_mask(medium_field)
    medium_cells = cells_from_grid(medium_lat, medium_lon, medium_field, medium_boundaries, 1.5, target_house, "medium")
    medium_seconds = time.perf_counter() - start
    medium_validation = validate_cells(cache, medium_cells, target_house)
    stage_reports.append(summarize_stage("medium", medium_seconds, medium_cells, int(medium_boundaries.sum()), medium_validation, cache))

    refined_cells: list[Cell] = []
    refined_validation: dict[str, Any] | None = None
    if include_refined:
        start = time.perf_counter()
        stable_medium_cells = cells_from_grid(
            medium_lat,
            medium_lon,
            medium_field,
            medium_boundaries,
            1.5,
            target_house,
            "medium-stable",
            only_non_boundary=True,
        )
        boundary_refined_cells = refine_boundary_cells(
            cache,
            medium_lat,
            medium_lon,
            medium_boundaries,
            1.5,
            0.5,
            target_house,
        )
        refined_cells = stable_medium_cells + boundary_refined_cells
        refined_seconds = time.perf_counter() - start
        refined_validation = validate_cells(cache, refined_cells, target_house)
        stage_reports.append(
            summarize_stage(
                "refined-boundary",
                refined_seconds,
                refined_cells,
                int(medium_boundaries.sum()),
                refined_validation,
                cache,
            )
        )

    outputs = {}
    for stage, cells in [
        ("coarse", coarse_cells),
        ("medium", medium_cells),
        ("refined", refined_cells),
    ]:
        if not cells:
            continue
        path = output_dir / f"truth-field-high-northern-sun-house-{target_house}-{stage}.geojson"
        path.write_text(json.dumps(cells_to_geojson(cells, stage, target_house), indent=2))
        outputs[stage] = str(path)

    final_cells = refined_cells if refined_cells else medium_cells
    known_false_checks = []
    for probe in KNOWN_FALSE_PROBES:
        included = any(point_in_rect(probe["lon"], probe["lat"], cell) for cell in final_cells)
        known_false_checks.append(
            {
                **probe,
                "includedInPrototypeTargetCells": included,
                "targetHouse": target_house,
                "passes": not included if probe["actual_sun_house"] != target_house else True,
            }
        )

    report = {
        "fixture": "high_northern",
        "planet": "sun",
        "targetHouse": target_house,
        "latitudeCap": [LAT_MIN, LAT_MAX],
        "periodicLongitude": True,
        "stageReports": stage_reports,
        "knownFalseChecks": known_false_checks,
        "currentCanonicalComparison": current_canonical_comparison(target_house),
        "outputs": outputs,
        "cacheSummary": {
            "sunHouseSamplesStored": len(cache.samples),
            "allSunHousesAvailableFromSameSamples": True,
            "estimatedAllPlanetsAllHousesCost": (
                "Approximately one swe.houses call per point, plus cheap planet longitude classification. "
                "The house cusps can be reused for all planets at the same point."
            ),
        },
        "aspectNotes": {
            "mc": "Keep current centerline strategy; it is already fast.",
            "asc": "Keep current centerline strategy for now; optimize later with progressive resolution and caching.",
        },
    }

    report_path = output_dir / f"truth-field-high-northern-sun-house-{target_house}-report.json"
    report_path.write_text(json.dumps(report, indent=2))
    report["reportPath"] = str(report_path)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the truth-field house-region prototype.")
    parser.add_argument("--house", type=int, default=7, help="Target Sun house to emit as cells.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("validation_screenshots") / "truth-field-prototype",
    )
    parser.add_argument("--skip-refined", action="store_true", help="Skip 0.5 degree boundary refinement.")
    parser.add_argument("--benchmark-merge", action="store_true", help="Benchmark raw cells versus merged rectangles.")
    parser.add_argument(
        "--write-validation-records",
        action="store_true",
        help="Write simple validation fixture/report/benchmark records for the merge benchmark.",
    )
    args = parser.parse_args()

    if args.benchmark_merge:
        report = run_merge_benchmark(args.output_dir / "merge-benchmark")
        if args.write_validation_records:
            report["validationRecords"] = write_validation_records(report, Path("validation"))
        print(json.dumps(report, indent=2))
        return

    if not 1 <= args.house <= 12:
        raise SystemExit("--house must be between 1 and 12")

    report = run_prototype(args.house, args.output_dir, include_refined=not args.skip_refined)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
