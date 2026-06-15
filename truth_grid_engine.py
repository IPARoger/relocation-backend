from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import swisseph as swe


LATITUDE_CAP = [-65.0, 65.0]
LON_MIN = -180.0
LON_MAX = 180.0
SIGN_NAMES = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]


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


def normalize_angle_sign_code(angle: str) -> str:
    """Normalize API/UI angle labels for angle-in-sign classification."""
    a = str(angle).strip().upper()
    if a in ("DESC", "DSC", "DES", "DCS"):
        return "DC"
    return a


def zodiac_sign_index(value: int | str) -> int:
    if isinstance(value, int):
        if 0 <= value <= 11:
            return value
        if 1 <= value <= 12:
            return value - 1
    normalized = str(value).strip().lower()
    if normalized.isdigit():
        return zodiac_sign_index(int(normalized))
    if normalized in SIGN_NAMES:
        return SIGN_NAMES.index(normalized)
    raise ValueError(f"Unknown zodiac sign: {value}")


def classify_angle_signs(jd: float, angle: str, step: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    lat_centers, lon_centers = build_center_grid(step)
    field = np.full((len(lat_centers), len(lon_centers)), -1, dtype=np.int16)
    sample_count = 0
    angle_code = normalize_angle_sign_code(angle)

    for i, lat in enumerate(lat_centers):
        for j, lon in enumerate(lon_centers):
            try:
                _, ascmc = swe.houses(jd, float(lat), float(lon), b"P")
                if angle_code == "ASC":
                    angle_deg = ascmc[0] % 360
                elif angle_code == "MC":
                    angle_deg = ascmc[1] % 360
                elif angle_code == "DC":
                    angle_deg = (ascmc[0] + 180.0) % 360
                elif angle_code == "IC":
                    angle_deg = (ascmc[1] + 180.0) % 360
                else:
                    continue
                field[i, j] = int(angle_deg // 30)
                sample_count += 1
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


def merge_field_rectangles(
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    field: np.ndarray,
    step: float,
    target_value: int,
) -> list[MergedCell]:
    active: dict[tuple[int, int], MergedCell] = {}
    completed: list[MergedCell] = []

    for row_index, lat in enumerate(lat_centers):
        current_keys = set()

        for start_col, end_col in row_runs_for_house(field[row_index], target_value):
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
                    house=target_value,
                    source_cell_count=previous.source_cell_count + width,
                )
            else:
                active[key] = MergedCell(
                    lon_min=lon_min,
                    lon_max=lon_max,
                    lat_min=lat_min,
                    lat_max=lat_max,
                    house=target_value,
                    source_cell_count=width,
                )

        for key in list(active.keys()):
            if key not in current_keys:
                completed.append(active.pop(key))

    completed.extend(active.values())
    return completed


def merge_house_rectangles(
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    field: np.ndarray,
    step: float,
    target_house: int,
) -> list[MergedCell]:
    return merge_field_rectangles(lat_centers, lon_centers, field, step, target_house)


def boundary_mask(field: np.ndarray) -> np.ndarray:
    """Cells whose 4-neighbor truth differs — candidates for finer resampling."""
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
            edge = False
            if i > 0:
                neighbors.append(field[i - 1, j])
            else:
                edge = True
            if i < rows - 1:
                neighbors.append(field[i + 1, j])
            else:
                edge = True

            if edge or any(neighbor != here for neighbor in neighbors):
                mask[i, j] = True

    return mask


def _coarse_indices(
    lat: float,
    lon: float,
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    coarse_step: float,
) -> tuple[int, int]:
    ci = int(round((lat - lat_centers[0]) / coarse_step))
    cj = int(round((lon - lon_centers[0]) / coarse_step))
    ci = max(0, min(len(lat_centers) - 1, ci))
    cj = max(0, min(len(lon_centers) - 1, cj))
    return ci, cj


def refine_classification_field(
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    field: np.ndarray,
    coarse_step: float,
    refine_step: float,
    resample_fn,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    """
    Re-sample only boundary coarse cells at refine_step.
    Interior cells copy coarse truth — no falsified smoothing.
    """
    subdiv = int(round(coarse_step / refine_step))
    if subdiv < 2:
        return lat_centers, lon_centers, field, 0

    boundaries = boundary_mask(field)
    lat_min, lat_max = LATITUDE_CAP
    fine_lat = np.arange(lat_min + refine_step / 2, lat_max, refine_step)
    fine_lon = np.arange(LON_MIN + refine_step / 2, LON_MAX, refine_step)
    fine_field = np.full((len(fine_lat), len(fine_lon)), -1, dtype=np.int16)
    extra_samples = 0

    for fi, flat in enumerate(fine_lat):
        for fj, flon in enumerate(fine_lon):
            ci, cj = _coarse_indices(flat, flon, lat_centers, lon_centers, coarse_step)
            if not boundaries[ci, cj]:
                fine_field[fi, fj] = field[ci, cj]
            else:
                value = resample_fn(float(flon), float(flat))
                if value is not None:
                    fine_field[fi, fj] = value
                    extra_samples += 1

    return fine_lat, fine_lon, fine_field, extra_samples


def _house_resample_fn(jd: float, planet_long: float):
    def fn(lon: float, lat: float) -> int | None:
        try:
            cusps, _ = swe.houses(jd, lat, lon, b"P")
            cusps = [c % 360 for c in cusps[:12]]
            for house in range(1, 13):
                if planet_in_house(planet_long, house, cusps):
                    return house
        except Exception:
            return None
        return None

    return fn


def _angle_sign_resample_fn(jd: float, angle_code: str):
    def fn(lon: float, lat: float) -> int | None:
        try:
            _, ascmc = swe.houses(jd, lat, lon, b"P")
            if angle_code == "ASC":
                angle_deg = ascmc[0] % 360
            elif angle_code == "MC":
                angle_deg = ascmc[1] % 360
            elif angle_code == "DC":
                angle_deg = (ascmc[0] + 180.0) % 360
            elif angle_code == "IC":
                angle_deg = (ascmc[1] + 180.0) % 360
            else:
                return None
            return int(angle_deg // 30)
        except Exception:
            return None

    return fn


def maybe_refine_field(
    jd: float,
    lat_centers: np.ndarray,
    lon_centers: np.ndarray,
    field: np.ndarray,
    coarse_step: float,
    boundary_refine: bool,
    resample_fn,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, int, int]:
    """Returns (lat, lon, field, merge_step, base_samples, extra_samples)."""
    base_samples = int(np.count_nonzero(field >= 0))
    if not boundary_refine or coarse_step < 0.5:
        return lat_centers, lon_centers, field, coarse_step, base_samples, 0

    refine_step = coarse_step / 2.0
    fine_lat, fine_lon, fine_field, extra = refine_classification_field(
        lat_centers,
        lon_centers,
        field,
        coarse_step,
        refine_step,
        resample_fn,
    )
    return fine_lat, fine_lon, fine_field, refine_step, base_samples, extra


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


def angle_sign_cell_to_feature(
    cell: MergedCell,
    angle: str,
    sign_index: int,
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
    sign = SIGN_NAMES[sign_index]
    angle = angle.upper()

    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [coords]},
        "properties": {
            "canonicalFeatureId": f"truth-grid-angle-sign-{condition_index}-{angle.lower()}-{sign}-{feature_index}",
            "condition_type": "angle_sign",
            "angle": angle,
            "sign": sign,
            "sign_index": sign_index,
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
    boundary_refine: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    started = time.perf_counter()
    features: list[dict[str, Any]] = []
    metadata = {
        "generation_mode": "truth_grid",
        "resolution": resolution,
        "boundary_refine": boundary_refine,
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
        lat_centers, lon_centers, field, merge_step, _base, refine_samples = maybe_refine_field(
            jd,
            lat_centers,
            lon_centers,
            field,
            resolution,
            boundary_refine,
            _house_resample_fn(jd, planet_longs[planet]),
        )
        sample_count += refine_samples
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
            cells = merge_house_rectangles(lat_centers, lon_centers, field, merge_step, house)
            merged_by_house[house] = cells
            validation_by_house[house] = validate_merged_cells(
                lat_centers,
                lon_centers,
                field,
                merge_step,
                cells,
                house,
            )
        merge_seconds = time.perf_counter() - merge_start

        metadata["planets"][planet] = {
            "sample_count": sample_count,
            "merge_step": merge_step,
            "refine_samples": refine_samples,
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
                    merge_step,
                    sample_count,
                    validation_by_house[house],
                    timing,
                )
                feature["properties"]["coarse_resolution"] = resolution
                feature["properties"]["boundary_refined"] = boundary_refine and merge_step < resolution
                feature["properties"]["feature_count"] = len(cells)
                features.append(feature)

    metadata["total_seconds"] = time.perf_counter() - started
    metadata["feature_count"] = len(features)
    return features, metadata


def generate_angle_sign_features(
    jd: float,
    conditions: list[Any],
    resolution: float = 0.75,
    condition_index_offset: int = 0,
    boundary_refine: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    started = time.perf_counter()
    features: list[dict[str, Any]] = []
    metadata = {
        "generation_mode": "truth_grid",
        "resolution": resolution,
        "boundary_refine": boundary_refine,
        "latitude_cap": LATITUDE_CAP,
        "angles": {},
    }

    conditions_by_angle: dict[str, list[tuple[int, Any, int]]] = {}
    for idx, condition in enumerate(conditions):
        angle = normalize_angle_sign_code(condition.angle)
        sign_index = zodiac_sign_index(condition.sign)
        conditions_by_angle.setdefault(angle, []).append((
            condition_index_offset + idx,
            condition,
            sign_index,
        ))

    for angle, indexed_conditions in conditions_by_angle.items():
        classify_start = time.perf_counter()
        lat_centers, lon_centers, field, sample_count = classify_angle_signs(
            jd,
            angle,
            resolution,
        )
        lat_centers, lon_centers, field, merge_step, _base, refine_samples = maybe_refine_field(
            jd,
            lat_centers,
            lon_centers,
            field,
            resolution,
            boundary_refine,
            _angle_sign_resample_fn(jd, angle),
        )
        sample_count += refine_samples
        classify_seconds = time.perf_counter() - classify_start

        requested_signs = {sign_index for _, _, sign_index in indexed_conditions}
        merged_by_sign = {}
        validation_by_sign = {}
        merge_start = time.perf_counter()
        for sign_index in requested_signs:
            cells = merge_field_rectangles(lat_centers, lon_centers, field, merge_step, sign_index)
            merged_by_sign[sign_index] = cells
            validation_by_sign[sign_index] = validate_merged_cells(
                lat_centers,
                lon_centers,
                field,
                merge_step,
                cells,
                sign_index,
            )
        merge_seconds = time.perf_counter() - merge_start

        metadata["angles"][angle] = {
            "sample_count": sample_count,
            "merge_step": merge_step,
            "refine_samples": refine_samples,
            "classify_seconds": classify_seconds,
            "merge_validate_seconds": merge_seconds,
            "signs_returned": [SIGN_NAMES[index] for index in sorted(requested_signs)],
        }

        for condition_index, _condition, sign_index in indexed_conditions:
            cells = merged_by_sign[sign_index]
            timing = {
                "classify_seconds": round(classify_seconds, 4),
                "merge_validate_seconds": round(merge_seconds, 4),
            }
            for feature_index, cell in enumerate(cells):
                feature = angle_sign_cell_to_feature(
                    cell,
                    angle,
                    sign_index,
                    condition_index,
                    feature_index,
                    merge_step,
                    sample_count,
                    validation_by_sign[sign_index],
                    timing,
                )
                feature["properties"]["coarse_resolution"] = resolution
                feature["properties"]["boundary_refined"] = boundary_refine and merge_step < resolution
                feature["properties"]["feature_count"] = len(cells)
                features.append(feature)

    metadata["total_seconds"] = time.perf_counter() - started
    metadata["feature_count"] = len(features)
    return features, metadata
