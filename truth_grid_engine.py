from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import swisseph as swe


LATITUDE_CAP = [-65.0, 65.0]
LON_MIN = -180.0
LON_MAX = 180.0


@dataclass(frozen=True)
class MergedCell:
    lon_min: float
    lon_max: float
    lat_min: float
    lat_max: float
    house: int
    source_cell_count: int


def planet_in_house(planet_long: float, house_num: int, cusps: list[float]) -> bool:
    start = cusps[house_num - 1]
    end = cusps[house_num % 12]

    if start <= end:
        return start <= planet_long < end

    return planet_long >= start or planet_long < end


def build_center_grid(step: float) -> tuple[np.ndarray, np.ndarray]:
    lat_min, lat_max = LATITUDE_CAP
    lat_centers = np.arange(lat_min + step / 2, lat_max, step)
    lon_centers = np.arange(LON_MIN + step / 2, LON_MAX, step)
    return lat_centers, lon_centers


def classify_planet_houses(jd: float, planet_long: float, step: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    lat_centers, lon_centers = build_center_grid(step)
    field = np.full((len(lat_centers), len(lon_centers)), -1, dtype=np.int16)
    sample_count = 0

    for i, lat in enumerate(lat_centers):
        for j, lon in enumerate(lon_centers):
            try:
                cusps, _ = swe.houses(jd, float(lat), float(lon), b"P")
                cusps = [c % 360 for c in cusps[:12]]
                sample_count += 1

                for house in range(1, 13):
                    if planet_in_house(planet_long, house, cusps):
                        field[i, j] = house
                        break
            except Exception:
                pass

    return lat_centers, lon_centers, field, sample_count


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

    # Keep display rectangles split at the antimeridian. The truth field is
    # periodic, but GeoJSON rectangles should not imply false seam-spanning edges.
    return runs


def merge_house_rectangles(
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    field: np.ndarray,
    step: float,
    target_house: int,
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
                    source_cell_count=previous.source_cell_count + width,
                )
            else:
                active[key] = MergedCell(
                    lon_min=lon_min,
                    lon_max=lon_max,
                    lat_min=lat_min,
                    lat_max=lat_max,
                    house=target_house,
                    source_cell_count=width,
                )

        for key in list(active.keys()):
            if key not in current_keys:
                completed.append(active.pop(key))

    completed.extend(active.values())
    return completed


def validate_merged_cells(
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    field: np.ndarray,
    step: float,
    cells: list[MergedCell],
    target_house: int,
) -> int:
    contradictions = 0

    for cell in cells:
        lon_values = np.arange(cell.lon_min + step / 2, cell.lon_max, step)
        lat_values = np.arange(cell.lat_min + step / 2, cell.lat_max, step)

        for lat in lat_values:
            for lon in lon_values:
                i = int(round((lat - lat_centers[0]) / step))
                j = int(round((lon - lon_centers[0]) / step))
                if not (0 <= i < len(lat_centers) and 0 <= j < len(lon_centers)):
                    continue
                if field[i, j] != target_house:
                    contradictions += 1

    return contradictions


def cell_to_feature(
    cell: MergedCell,
    planet: str,
    condition_index: int,
    feature_index: int,
    resolution: float,
    sample_count: int,
    validation_contradictions: int,
    timing: dict[str, float],
) -> dict[str, Any]:
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
            "canonicalFeatureId": f"truth-grid-house-{condition_index}-{planet}-{cell.house}-{feature_index}",
            "planet": planet,
            "house": cell.house,
            "condition_index": condition_index,
            "overlap_count": 1,
            "generation_mode": "truth_grid",
            "resolution": resolution,
            "latitude_cap": LATITUDE_CAP,
            "sample_count": sample_count,
            "feature_count": None,
            "validation_contradictions": validation_contradictions,
            "source_cell_count": cell.source_cell_count,
            "timing": timing,
        },
    }


def generate_truth_grid_house_features(
    jd: float,
    planet_longs: dict[str, float],
    conditions: list[Any],
    resolution: float = 0.75,
    return_all_houses: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    started = time.perf_counter()
    features: list[dict[str, Any]] = []
    metadata = {
        "generation_mode": "truth_grid",
        "resolution": resolution,
        "latitude_cap": LATITUDE_CAP,
        "planets": {},
    }

    conditions_by_planet: dict[str, list[tuple[int, Any]]] = {}
    for idx, condition in enumerate(conditions):
        planet = condition.planet.lower()
        conditions_by_planet.setdefault(planet, []).append((idx, condition))

    for planet, indexed_conditions in conditions_by_planet.items():
        classify_start = time.perf_counter()
        lat_centers, lon_centers, field, sample_count = classify_planet_houses(
            jd,
            planet_longs[planet],
            resolution,
        )
        classify_seconds = time.perf_counter() - classify_start

        # Compute all houses per planet so follow-up house selections can reuse
        # the same truth field. Return only requested houses unless explicitly
        # asked for all houses.
        cached_houses = set(range(1, 13))
        output_houses = cached_houses if return_all_houses else {
            condition.house for _, condition in indexed_conditions
        }

        merged_by_house = {}
        validation_by_house = {}
        merge_start = time.perf_counter()
        for house in cached_houses:
            cells = merge_house_rectangles(lat_centers, lon_centers, field, resolution, house)
            merged_by_house[house] = cells
            validation_by_house[house] = validate_merged_cells(
                lat_centers,
                lon_centers,
                field,
                resolution,
                cells,
                house,
            )
        merge_seconds = time.perf_counter() - merge_start

        metadata["planets"][planet] = {
            "sample_count": sample_count,
            "classify_seconds": classify_seconds,
            "merge_validate_seconds": merge_seconds,
            "houses_cached": sorted(cached_houses),
            "houses_returned": sorted(output_houses),
        }

        output_condition_pairs = (
            [(indexed_conditions[0][0], house) for house in sorted(cached_houses)]
            if return_all_houses
            else [(condition_index, condition.house) for condition_index, condition in indexed_conditions]
        )

        for condition_index, house in output_condition_pairs:
            cells = merged_by_house[house]
            timing = {
                "classify_seconds": round(classify_seconds, 4),
                "merge_validate_seconds": round(merge_seconds, 4),
            }
            for feature_index, cell in enumerate(cells):
                feature = cell_to_feature(
                    cell,
                    planet,
                    condition_index,
                    feature_index,
                    resolution,
                    sample_count,
                    validation_by_house[house],
                    timing,
                )
                feature["properties"]["feature_count"] = len(cells)
                features.append(feature)

    metadata["total_seconds"] = time.perf_counter() - started
    metadata["feature_count"] = len(features)
    return features, metadata
