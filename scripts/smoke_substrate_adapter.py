#!/usr/bin/env python3
"""Minimal smoke for the inert substrate adapter scaffold."""

from __future__ import annotations

import json
import os
import urllib.request

from playwright.sync_api import sync_playwright

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def run_canonical_visible_probe(browser, *, angle: str, block: int, zoom_clicks: int = 0) -> dict:
    page = browser.new_page(viewport={"width": 1200, "height": 800})
    paths: list[str] = []
    errors: list[str] = []
    page.on("request", lambda req: paths.append(req.url))
    page.on(
        "console",
        lambda msg: errors.append(f"console.{msg.type}: {msg.text}")
        if msg.type == "error"
        else None,
    )
    page.goto(
        f"{BASE}/map_CURRENT.html?skipOnboarding=1&canonicalVisible=1&canonicalBlock={block}",
        wait_until="domcontentloaded",
        timeout=30000,
    )
    page.wait_for_function(
        "() => window.__rmSmokeState?.().canonicalVisibleDebugEnabled === true",
        timeout=10000,
    )
    page.select_option("#overlayAngle", angle)
    if zoom_clicks:
        map_box = page.locator("#map").bounding_box()
        assert map_box
        cx = map_box["x"] + map_box["width"] / 2
        cy = map_box["y"] + map_box["height"] / 2
        for _ in range(zoom_clicks):
            page.mouse.dblclick(cx, cy)
            page.wait_for_timeout(500)
    before_paths = len(paths)
    page.locator("#findBtn").click()
    page.wait_for_function(
        """() => {
            const s = window.__rmSmokeState?.();
            return s && /ready/i.test(s.renderStatus)
                && s.polygonLayers > 0
                && s.canonicalDryRun?.status === "ok"
                && s.canonicalVisibleDebug?.rendered === true
                && s.canonicalDryRun?.continuityDiagnostics;
        }""",
        timeout=60000,
    )
    state = page.evaluate("() => window.__rmSmokeState?.() || null")
    render_paths = paths[before_paths:]
    result = {
        "angle": angle,
        "block": block,
        "state": state,
        "search_regions_calls": len(
            [url for url in render_paths if "/search-regions" in url]
        ),
        "screen_pixel_truth_calls": len(
            [url for url in render_paths if "/screen-pixel-truth" in url]
        ),
        "console_errors": errors,
    }
    page.close()
    return result


def run_canonical_payload_probe(
    browser,
    *,
    label: str,
    block: int,
    payload_patch: dict,
    zoom_clicks: int = 0,
    map_action: str | None = None,
) -> dict:
    page = browser.new_page(viewport={"width": 1200, "height": 800})
    paths: list[str] = []
    errors: list[str] = []
    page.on("request", lambda req: paths.append(req.url))
    page.on(
        "console",
        lambda msg: errors.append(f"console.{msg.type}: {msg.text}")
        if msg.type == "error"
        else None,
    )
    page.goto(
        f"{BASE}/map_CURRENT.html?skipOnboarding=1&canonicalVisible=1&canonicalBlock={block}",
        wait_until="domcontentloaded",
        timeout=30000,
    )
    page.wait_for_function(
        "() => window.__rmSmokeState?.().canonicalVisibleDebugEnabled === true",
        timeout=10000,
    )
    page.wait_for_function(
        """() => {
            const selected = document.getElementById("chartProfile")?.selectedOptions?.[0];
            return Boolean(selected?.dataset?.profile);
        }""",
        timeout=10000,
    )
    if map_action:
        page.evaluate(
            """action => {
                if (action === "high_latitude") map.setView([62, -35], 3);
                if (action === "seam") map.setView([0, 179], 3);
            }""",
            map_action,
        )
        page.wait_for_timeout(500)
    if zoom_clicks:
        map_box = page.locator("#map").bounding_box()
        assert map_box
        cx = map_box["x"] + map_box["width"] / 2
        cy = map_box["y"] + map_box["height"] / 2
        for _ in range(zoom_clicks):
            page.mouse.dblclick(cx, cy)
            page.wait_for_timeout(500)
    before_paths = len(paths)
    state = page.evaluate(
        """async patch => {
            const birth = getBirthParamsFromProfile();
            const payload = {
                ...birth,
                house_conditions: patch.house_conditions || [],
                angle_sign_conditions: patch.angle_sign_conditions || [],
                resolution: 1.5,
                generation_mode: "truth_grid",
                truth_grid_resolution: 0.75,
                truth_grid_boundary_refine: true
            };
            payload.house_conditions = payload.house_conditions.map(c => ({
                type: "planet_in_house",
                ...c
            }));
            payload.angle_sign_conditions = payload.angle_sign_conditions.map(c => ({
                type: "angle_in_sign",
                angle: String(c.angle || "").toLowerCase(),
                sign: c.sign
            }));
            if (patch.aspect_overlay) payload.aspect_overlay = patch.aspect_overlay;
            await dispatchOverlayRequest(payload);
            return window.__rmSmokeState?.() || null;
        }""",
        payload_patch,
    )
    state = page.evaluate("() => window.__rmSmokeState?.() || null")
    render_paths = paths[before_paths:]
    parity = state.get("canonicalDryRun", {}).get("parityDiagnostics") if state else None
    continuity = state.get("canonicalDryRun", {}).get("continuityDiagnostics") if state else None
    topology = state.get("canonicalDryRun", {}).get("topologyRefinement") if state else None
    result = {
        "label": label,
        "block": block,
        "state": state,
        "parity": parity,
        "continuity": continuity,
        "topology": topology,
        "canonical_elapsed_ms": state.get("canonicalDryRun", {}).get("elapsedMs")
        if state
        else None,
        "search_regions_calls": len(
            [url for url in render_paths if "/search-regions" in url]
        ),
        "screen_pixel_truth_calls": len(
            [url for url in render_paths if "/screen-pixel-truth" in url]
        ),
        "console_errors": errors,
    }
    page.close()
    return result


def summarize_stress_probe(probe: dict) -> dict:
    parity = probe["parity"]
    continuity = probe["continuity"]
    topology = probe["topology"]
    if not parity or not continuity or not topology:
        state = probe.get("state") or {}
        dry = state.get("canonicalDryRun") or {}
        return {
            "label": probe["label"],
            "block": probe["block"],
            "status": dry.get("status", "missing"),
            "measured": False,
            "pointCount": dry.get("pointCount"),
            "matchedCount": dry.get("matchedCount"),
            "canonicalElapsedMs": probe.get("canonical_elapsed_ms"),
            "screenPixelTruthCalls": probe["screen_pixel_truth_calls"],
            "reason": "parity, continuity, or topology diagnostics unavailable",
        }
    return {
        "label": probe["label"],
        "block": probe["block"],
        "status": "measured",
        "measured": True,
        "coarseOverlapPct": parity["coarse"]["occupiedOverlapPct"],
        "boundaryOverlapPct": parity["boundary"]["occupiedOverlapPct"],
        "refinedOverlapPct": parity["refined"]["occupiedOverlapPct"],
        "refinedDisagreementPct": parity["refined"]["occupiedDisagreementPct"],
        "refinedFalsePositiveCount": parity["refined"]["falsePositiveCount"],
        "refinedFalseNegativeCount": parity["refined"]["falseNegativeCount"],
        "refinedEdgeAgreementImprovementPct": parity[
            "refinedEdgeAgreementImprovementPct"
        ],
        "capDisagreementCount": parity["refined"]["capDisagreementCount"],
        "seamDisagreementCount": parity["refined"]["seamDisagreementCount"],
        "matchedPointCount": continuity["matchedPointCount"],
        "discontinuityCount": continuity["discontinuityCount"],
        "curvatureVariance": continuity["curvatureVariance"],
        "refinedPointCount": topology["refinedPointCount"],
        "refinementDepth": parity["refinementDepth"],
        "canonicalElapsedMs": probe["canonical_elapsed_ms"],
        "comparisonMs": parity["timingMs"]["comparison"],
        "screenPixelTruthCalls": probe["screen_pixel_truth_calls"],
    }


def run_full_pixel_wall_probe(
    browser,
    *,
    label: str,
    payload_patch: dict,
    map_action: str | None = None,
) -> dict:
    page = browser.new_page(viewport={"width": 720, "height": 480})
    paths: list[str] = []
    errors: list[str] = []
    page.on("request", lambda req: paths.append(req.url))
    page.on(
        "console",
        lambda msg: errors.append(f"console.{msg.type}: {msg.text}")
        if msg.type == "error"
        else None,
    )
    page.goto(
        f"{BASE}/map_CURRENT.html?skipOnboarding=1&canonicalVisible=1&canonicalBlock=12",
        wait_until="domcontentloaded",
        timeout=30000,
    )
    page.wait_for_function(
        "() => window.__rmSmokeState?.().canonicalVisibleDebugEnabled === true",
        timeout=10000,
    )
    if map_action:
        page.evaluate(
            """action => {
                if (action === "high_latitude") map.setView([62, -35], 3);
                if (action === "seam") map.setView([0, 179], 3);
            }""",
            map_action,
        )
        page.wait_for_timeout(500)
    before_paths = len(paths)
    metrics = page.evaluate(
        """async patch => {
            function normalizePatchPayload(patch) {
                const birth = getBirthParamsFromProfile();
                const payload = {
                    ...birth,
                    house_conditions: patch.house_conditions || [],
                    angle_sign_conditions: patch.angle_sign_conditions || [],
                    resolution: 1.5,
                    generation_mode: "truth_grid",
                    truth_grid_resolution: 0.75,
                    truth_grid_boundary_refine: true
                };
                payload.house_conditions = payload.house_conditions.map(c => ({
                    type: "planet_in_house",
                    ...c
                }));
                payload.angle_sign_conditions = payload.angle_sign_conditions.map(c => ({
                    type: "angle_in_sign",
                    angle: String(c.angle || "").toLowerCase(),
                    sign: c.sign
                }));
                if (patch.aspect_overlay) payload.aspect_overlay = patch.aspect_overlay;
                return payload;
            }

            function comparePointSetToWall(points, masks, wallMasks, wallWidth, legacyIndex, legacyThresholdPx) {
                let comparableCount = 0;
                let wallOccupied = 0;
                let canonicalOccupied = 0;
                let legacyOccupied = 0;
                let canonicalFalsePositiveCount = 0;
                let canonicalFalseNegativeCount = 0;
                let legacyFalsePositiveCount = 0;
                let legacyFalseNegativeCount = 0;
                let capAdjacentDisagreementCount = 0;
                let seamDisagreementCount = 0;
                let duplicatePixelCount = 0;
                let edgePixelCount = 0;
                let longitudeOutOfRangeCount = 0;
                const seen = new Set();
                points.forEach((pt, index) => {
                    const px = map.latLngToContainerPoint([pt[0], pt[1]]);
                    const x = Math.max(0, Math.min(wallWidth - 1, Math.floor(px.x)));
                    const y = Math.max(0, Math.floor(px.y));
                    const wallIndex = y * wallWidth + x;
                    if (wallIndex < 0 || wallIndex >= wallMasks.length) return;
                    const key = `${x},${y}`;
                    if (seen.has(key)) duplicatePixelCount++;
                    seen.add(key);
                    if (x <= 0 || x >= wallWidth - 1) edgePixelCount++;
                    if (Number(pt[1]) < -180 || Number(pt[1]) > 180) longitudeOutOfRangeCount++;
                    const wallHit = Boolean(wallMasks[wallIndex]);
                    const canonicalHit = Boolean(masks[index]);
                    const legacyHit = legacyIndexContainsPoint(legacyIndex, pt, legacyThresholdPx);
                    comparableCount++;
                    if (wallHit) wallOccupied++;
                    if (canonicalHit) canonicalOccupied++;
                    if (legacyHit) legacyOccupied++;
                    if (canonicalHit && !wallHit) canonicalFalsePositiveCount++;
                    if (!canonicalHit && wallHit) canonicalFalseNegativeCount++;
                    if (legacyHit && !wallHit) legacyFalsePositiveCount++;
                    if (!legacyHit && wallHit) legacyFalseNegativeCount++;
                    if (canonicalHit !== wallHit || legacyHit !== wallHit) {
                        if (Math.abs(Number(pt[0])) >= PRODUCT_LAT_CAP - 1) capAdjacentDisagreementCount++;
                        if (Math.abs(normalizeLon(Number(pt[1]))) >= 179) seamDisagreementCount++;
                    }
                });
                const pct = (num, den) => den ? Number(((num / den) * 100).toFixed(3)) : 0;
                const canonicalDisagreement =
                    canonicalFalsePositiveCount + canonicalFalseNegativeCount;
                const legacyDisagreement =
                    legacyFalsePositiveCount + legacyFalseNegativeCount;
                return {
                    comparableCount,
                    wallOccupied,
                    canonicalOccupied,
                    legacyOccupied,
                    canonicalDisagreementPct: pct(canonicalDisagreement, comparableCount),
                    legacyDisagreementPct: pct(legacyDisagreement, comparableCount),
                    canonicalFalsePositiveCount,
                    canonicalFalseNegativeCount,
                    legacyFalsePositiveCount,
                    legacyFalseNegativeCount,
                    capAdjacentDisagreementCount,
                    seamDisagreementCount,
                    duplicatePixelCount,
                    edgePixelCount,
                    longitudeOutOfRangeCount,
                    closerToWall:
                        canonicalDisagreement < legacyDisagreement
                            ? "canonical"
                            : legacyDisagreement < canonicalDisagreement
                                ? "legacy"
                                : "tie"
                };
            }

            function summarizeDistance(values) {
                if (!values.length) {
                    return { count: 0, mean: null, max: null };
                }
                const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
                return {
                    count: values.length,
                    mean: Number(mean.toFixed(3)),
                    max: Number(Math.max(...values).toFixed(3))
                };
            }

            function nearestDistanceToWallPixels(point, wallPixelPoints) {
                if (!wallPixelPoints.length) return null;
                let best = Infinity;
                for (const wp of wallPixelPoints) {
                    const d = Math.hypot(point.x - wp.x, point.y - wp.y);
                    if (d < best) best = d;
                }
                return best;
            }

            function nearestDistanceToLegacyLine(point, legacyIndex) {
                if (!legacyIndex?.lineSegments?.length) return null;
                let best = Infinity;
                for (const segment of legacyIndex.lineSegments) {
                    const d = distancePointToSegment(
                        point.x,
                        point.y,
                        segment[0],
                        segment[1],
                        segment[2],
                        segment[3]
                    );
                    if (d < best) best = d;
                }
                return best;
            }

            function summarizeTrajectory(points, blockPx) {
                const sorted = points
                    .slice()
                    .sort((a, b) => (a.y === b.y ? a.x - b.x : a.y - b.y));
                const stepDistances = [];
                let discontinuityCount = 0;
                let seamDiscontinuityCount = 0;
                let capAdjacentDiscontinuityCount = 0;
                const threshold = Math.max(blockPx * 2.5, 1);
                for (let i = 1; i < sorted.length; i++) {
                    const prev = sorted[i - 1];
                    const cur = sorted[i];
                    const dist = Math.hypot(cur.x - prev.x, cur.y - prev.y);
                    stepDistances.push(dist);
                    if (dist > threshold) {
                        discontinuityCount++;
                        if (Math.abs(normalizeLon(cur.lon) - normalizeLon(prev.lon)) > 180) {
                            seamDiscontinuityCount++;
                        }
                        if (
                            Math.abs(cur.lat) >= PRODUCT_LAT_CAP - 1 ||
                            Math.abs(prev.lat) >= PRODUCT_LAT_CAP - 1
                        ) {
                            capAdjacentDiscontinuityCount++;
                        }
                    }
                }
                return {
                    pointCount: sorted.length,
                    meanStepPx: summarizeDistance(stepDistances).mean,
                    maxStepPx: summarizeDistance(stepDistances).max,
                    discontinuityCount,
                    seamDiscontinuityCount,
                    capAdjacentDiscontinuityCount
                };
            }

            function angleDeltaDeg(a, b) {
                let d = Math.abs(a - b) % 360;
                return d > 180 ? 360 - d : d;
            }

            function variance(values) {
                if (!values.length) return 0;
                const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
                return values.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0) / values.length;
            }

            function emptyTopologySummary() {
                return {
                    extractedSegmentCount: 0,
                    componentCount: 0,
                    segmentLengthsPx: [],
                    totalLengthPx: 0,
                    meanPointSpacingPx: null,
                    maxPointSpacingPx: null,
                    headingVariance: 0,
                    curvatureVariance: 0,
                    discontinuityCount: 0,
                    seamDiscontinuityCount: 0,
                    capAdjacentDiscontinuityCount: 0,
                    coherentTopology: false
                };
            }

            function isSeamJump(a, b) {
                return Math.abs(normalizeLon(a.lon) - normalizeLon(b.lon)) > 180;
            }

            function isCapAdjacent(a, b) {
                return (
                    Math.abs(a.lat) >= PRODUCT_LAT_CAP - 1 ||
                    Math.abs(b.lat) >= PRODUCT_LAT_CAP - 1
                );
            }

            function summarizeOrderedSegments(segments, originalPointCount) {
                if (!originalPointCount) {
                    return emptyTopologySummary();
                }
                const segmentLengths = [];
                const spacings = [];
                const headings = [];
                for (const segment of segments) {
                    let segmentLength = 0;
                    for (let i = 1; i < segment.length; i++) {
                        const prev = segment[i - 1];
                        const cur = segment[i];
                        const dx = cur.x - prev.x;
                        const dy = cur.y - prev.y;
                        const dist = Math.hypot(dx, dy);
                        segmentLength += dist;
                        spacings.push(dist);
                        if (dist > 0) {
                            headings.push((Math.atan2(dy, dx) * 180) / Math.PI);
                        }
                    }
                    segmentLengths.push(Number(segmentLength.toFixed(3)));
                }
                const headingDeltas = [];
                for (let i = 1; i < headings.length; i++) {
                    headingDeltas.push(angleDeltaDeg(headings[i], headings[i - 1]));
                }
                const spacingSummary = summarizeDistance(spacings);
                const totalLength = segmentLengths.reduce((sum, value) => sum + value, 0);
                return {
                    extractedSegmentCount: segments.length,
                    componentCount: segments.length,
                    segmentLengthsPx: segmentLengths,
                    totalLengthPx: Number(totalLength.toFixed(3)),
                    meanPointSpacingPx: spacingSummary.mean,
                    maxPointSpacingPx: spacingSummary.max,
                    headingVariance: Number(variance(headings).toFixed(3)),
                    curvatureVariance: Number(variance(headingDeltas).toFixed(3)),
                    discontinuityCount: Math.max(0, segments.length - 1),
                    seamDiscontinuityCount: 0,
                    capAdjacentDiscontinuityCount: 0,
                    coherentTopology:
                        originalPointCount > 0 &&
                        segments.length <= Math.max(1, Math.ceil(originalPointCount / 2))
                };
            }

            function extractCrudeContinuousTopology(points, blockPx) {
                const sorted = points
                    .slice()
                    .sort((a, b) => (a.y === b.y ? a.x - b.x : a.y - b.y));
                if (!sorted.length) {
                    return emptyTopologySummary();
                }
                const splitThreshold = Math.max(blockPx * 2.5, 1);
                const segments = [[sorted[0]]];
                let discontinuityCount = 0;
                let seamDiscontinuityCount = 0;
                let capAdjacentDiscontinuityCount = 0;
                for (let i = 1; i < sorted.length; i++) {
                    const prev = sorted[i - 1];
                    const cur = sorted[i];
                    const dist = Math.hypot(cur.x - prev.x, cur.y - prev.y);
                    const discontinuous = dist > splitThreshold;
                    if (discontinuous) {
                        discontinuityCount++;
                        if (isSeamJump(cur, prev)) {
                            seamDiscontinuityCount++;
                        }
                        if (isCapAdjacent(cur, prev)) {
                            capAdjacentDiscontinuityCount++;
                        }
                        segments.push([cur]);
                    } else {
                        segments[segments.length - 1].push(cur);
                    }
                }
                const summary = summarizeOrderedSegments(segments, sorted.length);
                return {
                    ...summary,
                    discontinuityCount,
                    seamDiscontinuityCount,
                    capAdjacentDiscontinuityCount,
                    coherentTopology:
                        sorted.length > 0 &&
                        discontinuityCount <= Math.max(2, sorted.length * 0.25) &&
                        segments.length <= Math.max(1, Math.ceil(sorted.length / 2))
                };
            }

            function choosePathStart(component, threshold) {
                let bestPoint = component[0];
                let bestNeighborCount = Infinity;
                for (const point of component) {
                    const neighborCount = component.filter(candidate => {
                        if (candidate === point) return false;
                        return Math.hypot(point.x - candidate.x, point.y - candidate.y) <= threshold;
                    }).length;
                    if (
                        neighborCount < bestNeighborCount ||
                        (neighborCount === bestNeighborCount &&
                            (point.x < bestPoint.x || (point.x === bestPoint.x && point.y < bestPoint.y)))
                    ) {
                        bestPoint = point;
                        bestNeighborCount = neighborCount;
                    }
                }
                return bestPoint;
            }

            function orderComponentNearestNeighbor(component, threshold) {
                if (component.length <= 1) return component.slice();
                const remaining = new Set(component);
                const ordered = [];
                let current = choosePathStart(component, threshold);
                while (current) {
                    ordered.push(current);
                    remaining.delete(current);
                    let next = null;
                    let best = Infinity;
                    for (const candidate of remaining) {
                        if (isSeamJump(current, candidate)) continue;
                        const d = Math.hypot(current.x - candidate.x, current.y - candidate.y);
                        if (d < best) {
                            best = d;
                            next = candidate;
                        }
                    }
                    current = next && best <= threshold ? next : null;
                }
                return ordered;
            }

            function extractPathSolvedTopology(points, blockPx) {
                if (!points.length) {
                    return {
                        ...emptyTopologySummary(),
                        solver: "connected_component_nearest_neighbor"
                    };
                }
                const splitThreshold = Math.max(blockPx * 2.5, 1);
                const unvisited = new Set(points);
                const components = [];
                while (unvisited.size) {
                    const first = unvisited.values().next().value;
                    const queue = [first];
                    const component = [];
                    unvisited.delete(first);
                    while (queue.length) {
                        const current = queue.shift();
                        component.push(current);
                        for (const candidate of Array.from(unvisited)) {
                            if (isSeamJump(current, candidate)) continue;
                            const d = Math.hypot(current.x - candidate.x, current.y - candidate.y);
                            if (d <= splitThreshold) {
                                unvisited.delete(candidate);
                                queue.push(candidate);
                            }
                        }
                    }
                    components.push(component);
                }
                const segments = components
                    .map(component => orderComponentNearestNeighbor(component, splitThreshold))
                    .filter(segment => segment.length);
                let seamDiscontinuityCount = 0;
                let capAdjacentDiscontinuityCount = 0;
                for (let i = 1; i < segments.length; i++) {
                    const prev = segments[i - 1][segments[i - 1].length - 1];
                    const cur = segments[i][0];
                    if (prev && cur) {
                        if (isSeamJump(prev, cur)) seamDiscontinuityCount++;
                        if (isCapAdjacent(prev, cur)) capAdjacentDiscontinuityCount++;
                    }
                }
                const summary = summarizeOrderedSegments(segments, points.length);
                return {
                    ...summary,
                    solver: "connected_component_nearest_neighbor",
                    componentCount: components.length,
                    discontinuityCount: Math.max(0, components.length - 1),
                    seamDiscontinuityCount,
                    capAdjacentDiscontinuityCount,
                    coherentTopology:
                        points.length > 0 &&
                        components.length - 1 <= Math.max(2, points.length * 0.25) &&
                        components.length <= Math.max(1, Math.ceil(points.length / 2))
                };
            }

            function summarizeTopologyExtraction(points, masks, wallMasks, wallWidth, legacyIndex, blockPx) {
                const positivePoints = [];
                points.forEach((pt, index) => {
                    if (!masks[index]) return;
                    const px = map.latLngToContainerPoint([pt[0], pt[1]]);
                    positivePoints.push({
                        x: px.x,
                        y: px.y,
                        lat: Number(pt[0]),
                        lon: Number(pt[1])
                    });
                });
                const wallPositivePixels = [];
                wallMasks.forEach((mask, index) => {
                    if (!mask) return;
                    wallPositivePixels.push({
                        x: index % wallWidth,
                        y: Math.floor(index / wallWidth)
                    });
                });
                const distancesToWall = positivePoints
                    .map(point => nearestDistanceToWallPixels(point, wallPositivePixels))
                    .filter(value => value != null);
                const distancesToLegacy = positivePoints
                    .map(point => nearestDistanceToLegacyLine(point, legacyIndex))
                    .filter(value => value != null);
                const trajectory = summarizeTrajectory(positivePoints, blockPx);
                const wallDistance = summarizeDistance(distancesToWall);
                const legacyDistance = summarizeDistance(distancesToLegacy);
                const crudeOrdering = extractCrudeContinuousTopology(positivePoints, blockPx);
                const pathSolver = extractPathSolvedTopology(positivePoints, blockPx);
                return {
                    subpixelPositiveCount: positivePoints.length,
                    wallPositivePixelCount: wallPositivePixels.length,
                    meanDistanceToWallPositivePx: wallDistance.mean,
                    maxDistanceToWallPositivePx: wallDistance.max,
                    meanDistanceToLegacyLinePx: legacyDistance.mean,
                    maxDistanceToLegacyLinePx: legacyDistance.max,
                    centerlineContinuity: trajectory,
                    continuousTopology: pathSolver,
                    crudeOrdering,
                    pathSolver,
                    solverImprovement: {
                        segmentDelta:
                            pathSolver.extractedSegmentCount - crudeOrdering.extractedSegmentCount,
                        discontinuityDelta:
                            pathSolver.discontinuityCount - crudeOrdering.discontinuityCount,
                        headingVarianceDelta:
                            Number((pathSolver.headingVariance - crudeOrdering.headingVariance).toFixed(3)),
                        curvatureVarianceDelta:
                            Number((pathSolver.curvatureVariance - crudeOrdering.curvatureVariance).toFixed(3))
                    },
                    coherentTrajectory:
                        positivePoints.length > 0 &&
                        (trajectory.discontinuityCount <= Math.max(2, positivePoints.length * 0.25)) &&
                        (wallDistance.mean == null || wallDistance.mean <= blockPx),
                    interpretation:
                        positivePoints.length === 0
                            ? "no positive topology samples"
                            : wallDistance.mean != null && wallDistance.mean <= blockPx
                                ? "subpixel positives lie near 1px wall-positive trajectory"
                                : "subpixel positives are not close enough to wall-positive pixels"
                };
            }

            const payload = normalizePatchPayload(patch);
            const legacyStarted = performance.now();
            const legacyData = await dispatchOverlayRequest(payload, { shadow: false });
            const legacyElapsedMs = Math.round(performance.now() - legacyStarted);

            const topologyPayload = buildCanonicalDryRunPayload(payload);
            const topologyStarted = performance.now();
            const coarse = await postScreenPixelTruth(
                buildScreenPixelTruthPayload(topologyPayload, topologyPayload.points)
            );
            const refinement = await refineCanonicalBoundarySamples(topologyPayload, coarse.body);
            const topologyElapsedMs = Math.round(performance.now() - topologyStarted);

            const size = map.getSize();
            const wallPoints = [];
            for (let y = 0.5; y < size.y; y += 1) {
                for (let x = 0.5; x < size.x; x += 1) {
                    const ll = map.containerPointToLatLng([x, y]);
                    wallPoints.push([ll.lat, ll.lng]);
                }
            }
            const wallPayload = {
                ...topologyPayload,
                points: wallPoints,
                block_px: 1
            };
            const wallStarted = performance.now();
            const wall = await postScreenPixelTruth(
                buildScreenPixelTruthPayload(wallPayload, wallPoints)
            );
            const wallElapsedMs = Math.round(performance.now() - wallStarted);

            const legacyIndex = compileLegacyGeometryIndex(legacyData);
            const refinedMasks = Array.isArray(refinement?.body?.masks)
                ? refinement.body.masks
                : [];
            const baselinePointCount = refinement?.firstLevelPointCount ?? refinedMasks.length;
            const baselinePoints = (refinement?.points || []).slice(0, baselinePointCount);
            const baselineMasks = refinedMasks.slice(0, baselinePointCount);
            const coarseMasks = Array.isArray(coarse.body?.masks) ? coarse.body.masks : [];
            const wallMasks = Array.isArray(wall.body?.masks) ? wall.body.masks : [];
            const refinedVsWall = comparePointSetToWall(
                refinement?.points || [],
                refinedMasks,
                wallMasks,
                size.x,
                legacyIndex,
                Math.max((topologyPayload.block_px || 12) / 4, 1)
            );
            const baselineRefinedVsWall = comparePointSetToWall(
                baselinePoints,
                baselineMasks,
                wallMasks,
                size.x,
                legacyIndex,
                Math.max((topologyPayload.block_px || 12) / 4, 1)
            );
            const coarseVsWall = comparePointSetToWall(
                topologyPayload.points || [],
                coarseMasks,
                wallMasks,
                size.x,
                legacyIndex,
                Math.max((topologyPayload.block_px || 12) / 2, 1)
            );
            const topologyExtraction = summarizeTopologyExtraction(
                refinement?.points || [],
                refinedMasks,
                wallMasks,
                size.x,
                legacyIndex,
                topologyPayload.block_px || 12
            );
            return {
                label: patch.label,
                wallPointCount: wallPoints.length,
                viewport: { width: size.x, height: size.y, zoom: map.getZoom() },
                wallTimingMs: wallElapsedMs,
                topologyRefinedTimingMs: topologyElapsedMs,
                legacyTimingMs: legacyElapsedMs,
                wallHttpStatus: wall.response.status,
                topologyHttpStatus: coarse.response.status,
                refinedPointCount: refinement?.refinedPointCount || 0,
                refinedMatchedCount: refinement?.matchedRefinedCount || 0,
                targetedAscDsc: Boolean(refinement?.targetedAscDsc),
                maxDepth: refinement?.maxDepth || 0,
                firstLevelPointCount: refinement?.firstLevelPointCount || 0,
                secondLevelPointCount: refinement?.secondLevelPointCount || 0,
                matchedSecondLevelCount: refinement?.matchedSecondLevelCount || 0,
                coarseVsWall,
                baselineRefinedVsWall,
                refinedVsWall,
                topologyExtraction,
                seamProbe: {
                    duplicatePixelCount: refinedVsWall.duplicatePixelCount,
                    edgePixelCount: refinedVsWall.edgePixelCount,
                    longitudeOutOfRangeCount: refinedVsWall.longitudeOutOfRangeCount
                },
                rootCauseHint:
                    refinedVsWall.longitudeOutOfRangeCount > 0
                        ? "possible longitude normalization issue"
                        : refinedVsWall.duplicatePixelCount > refinedVsWall.comparableCount * 0.1
                            ? "possible duplicate/wrapped refinement samples"
                            : refinedVsWall.canonicalDisagreementPct > coarseVsWall.canonicalDisagreementPct
                                ? "refinement worsens against 1px wall; inspect edge-neighbor topology"
                                : refinedVsWall.legacyDisagreementPct < refinedVsWall.canonicalDisagreementPct
                                    ? "legacy closer to 1px wall at refined sample points"
                                    : "canonical closer or tied against 1px wall"
            };
        }""",
        {**payload_patch, "label": label},
    )
    render_paths = paths[before_paths:]
    result = {
        "label": label,
        "metrics": metrics,
        "search_regions_calls": len(
            [url for url in render_paths if "/search-regions" in url]
        ),
        "screen_pixel_truth_calls": len(
            [url for url in render_paths if "/screen-pixel-truth" in url]
        ),
        "console_errors": errors,
    }
    page.close()
    return result


def main() -> int:
    results = []

    with urllib.request.urlopen(f"{BASE}/substrate_adapter.js", timeout=10) as resp:
        route_status = resp.status
    results.append(
        {
            "test": "adapter_route_serves",
            "pass": route_status == 200,
            "detail": {"status": route_status},
        }
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        console_errors: list[str] = []
        requested_paths: list[str] = []
        page.on(
            "console",
            lambda msg: console_errors.append(f"console.{msg.type}: {msg.text}")
            if msg.type == "error"
            else None,
        )
        page.on("request", lambda req: requested_paths.append(req.url))
        resp = page.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        page.wait_for_function("() => !!window.RelocationSubstrateAdapter", timeout=10000)
        adapter_state = page.evaluate(
            """() => {
                const a = window.RelocationSubstrateAdapter;
                const viewport = a.createViewportRequest({
                    bounds: { north: 10, south: -10, east: 20, west: -20 },
                    zoom: 3,
                    size: { width: 1200, height: 800 },
                    blockPx: 4,
                    applyLatCap: true
                });
                const classification = a.createClassificationRequest({
                    requestId: "smoke",
                    birth: { date: "1990-01-01" },
                    viewport,
                    conditions: [{ kind: "planet_in_house", planet: "sun", house: 1 }]
                });
                const cache = a.createCacheBoundary({
                    chartKey: "smoke-chart",
                    substrate: "screen-pixel-truth",
                    viewport,
                    conditions: classification.conditions
                });
                const status = a.createRefinementStatus({
                    stage: "unstarted",
                    sampleCount: 0,
                    cellCount: 0
                });
                const host = a.createRendererHostBoundary({ hostId: "map_CURRENT", mayRender: false });
                return {
                    version: a.VERSION,
                    keys: Object.keys(a).sort(),
                    viewport,
                    classificationConditionCount: classification.conditions.length,
                    cache,
                    status,
                    host,
                    smokeState: window.__rmSmokeState?.() || null
                };
            }"""
        )
        results.append(
            {
                "test": "adapter_loads_in_production_host",
                "pass": bool(resp and resp.status == 200 and adapter_state["version"] == 1),
                "detail": {
                    "status": resp.status if resp else None,
                    "version": adapter_state["version"],
                },
            }
        )
        results.append(
            {
                "test": "adapter_contract_builders_work",
                "pass": bool(
                    adapter_state["keys"] == [
                        "CACHE_OWNS",
                        "HOST_OWNS",
                        "SUBSTRATE_OWNS",
                        "VERSION",
                        "createCacheBoundary",
                        "createCacheKeyPayload",
                        "createCancellationScope",
                        "createClassificationRequest",
                        "createRefinementStatus",
                        "createRendererHostBoundary",
                        "createSamplingScope",
                        "createSemanticCacheKey",
                        "createViewportRequest",
                        "normalizeInvestigationIntent",
                    ]
                    and adapter_state["host"]["owns"]
                    == adapter_state["smokeState"]["substrateAdapter"]["hostOwns"]
                    and adapter_state["host"]["substrateOwns"]
                    == adapter_state["smokeState"]["substrateAdapter"]["substrateOwns"]
                    and adapter_state["host"]["cacheOwns"]
                    == adapter_state["smokeState"]["substrateAdapter"]["cacheOwns"]
                    and adapter_state["viewport"]["zoom"] == 3
                    and adapter_state["classificationConditionCount"] == 1
                    and adapter_state["cache"]["substrate"] == "screen-pixel-truth"
                    and adapter_state["status"]["stage"] == "unstarted"
                    and adapter_state["host"]["mayRender"] is False
                    and adapter_state["smokeState"]["substrateAdapter"]["version"] == 1
                    and adapter_state["smokeState"]["rendererSubstrate"]
                    == "legacy_search_regions"
                    and adapter_state["smokeState"]["rendererSubstrates"]["CANONICAL_SCREEN_SPACE"]
                    == "canonical_screen_space"
                    and adapter_state["smokeState"]["canonicalRendererBranchActive"] is False
                    and adapter_state["smokeState"]["canonicalDryRunEnabled"] is False
                    and adapter_state["smokeState"]["canonicalDryRun"] is None
                ),
                "detail": adapter_state,
            }
        )
        cache_contract = page.evaluate(
            """() => {
                const a = window.RelocationSubstrateAdapter;
                const base = {
                    chart_key: "lib_chart_1",
                    investigation: {
                        house_conditions: [
                            { house: "7", planet: "Venus", type: "planet_in_house", slot: "B" },
                            { planet: "Moon", house: 4, slot: "A", type: "planet_in_house" }
                        ],
                        angle_sign_conditions: [
                            { sign: "Capricorn", angle: "MC", type: "angle_in_sign" }
                        ],
                        aspect_overlay: {
                            planet: "Saturn",
                            angle: "DSC",
                            aspect: "Square",
                            type: "aspect_to_angle"
                        }
                    },
                    viewport: {
                        north: 81.201419542,
                        south: -72.181803556,
                        east: 127.265625,
                        west: -127.265625,
                        zoom: 2
                    },
                    sampling: {
                        width: 1024,
                        height: 720,
                        block_px: 12,
                        lat_cap: true
                    }
                };
                const equivalent = {
                    debugAura: true,
                    rendererSubstrate: "canonical_screen_space",
                    generation_mode: "truth_grid",
                    requestId: "transient",
                    cacheHits: 99,
                    auraMode: "raster",
                    renderedGeoJson: { type: "FeatureCollection" },
                    canvasPixels: "ignored",
                    sampling: {
                        latCap: true,
                        blockPx: 12,
                        height: 720,
                        width: 1024
                    },
                    viewport: {
                        west: -127.2656250001,
                        east: 127.2656250001,
                        south: -72.1818035564,
                        north: 81.2014195421,
                        zoom: 2.0004
                    },
                    chartKey: "lib_chart_1",
                    intent: {
                        aspectOverlay: { angle: "DC", aspect: "square", planet: "saturn" },
                        angleSignConditions: [{ angle: "mc", sign: "capricorn" }],
                        houseConditions: [
                            { type: "planet_in_house", slot: "A", planet: "moon", house: 4 },
                            { type: "planet_in_house", slot: "B", planet: "venus", house: 7 }
                        ]
                    }
                };
                const changedChart = { ...base, chart_key: "lib_chart_2" };
                const changedCondition = {
                    ...base,
                    investigation: {
                        ...base.investigation,
                        house_conditions: [
                            { planet: "moon", house: 5, slot: "A", type: "planet_in_house" },
                            { planet: "venus", house: 7, slot: "B", type: "planet_in_house" }
                        ]
                    }
                };
                const changedViewport = {
                    ...base,
                    viewport: { ...base.viewport, zoom: 3 }
                };
                const changedSampling = {
                    ...base,
                    sampling: { ...base.sampling, width: 1200 }
                };
                const changedLatCap = {
                    ...base,
                    sampling: { ...base.sampling, lat_cap: false }
                };
                const keys = {
                    base: a.createSemanticCacheKey(base),
                    equivalent: a.createSemanticCacheKey(equivalent),
                    changedChart: a.createSemanticCacheKey(changedChart),
                    changedCondition: a.createSemanticCacheKey(changedCondition),
                    changedViewport: a.createSemanticCacheKey(changedViewport),
                    changedSampling: a.createSemanticCacheKey(changedSampling),
                    changedLatCap: a.createSemanticCacheKey(changedLatCap)
                };
                const equivalentStable = keys.equivalent.stable_json;
                return {
                    keys,
                    equivalent_matches: keys.base.key === keys.equivalent.key,
                    chart_differs: keys.base.key !== keys.changedChart.key,
                    condition_differs: keys.base.key !== keys.changedCondition.key,
                    viewport_differs: keys.base.key !== keys.changedViewport.key,
                    sampling_differs: keys.base.key !== keys.changedSampling.key,
                    lat_cap_differs: keys.base.key !== keys.changedLatCap.key,
                    excluded_absent:
                        !equivalentStable.includes("generation_mode") &&
                        !equivalentStable.includes("rendererSubstrate") &&
                        !equivalentStable.includes("debugAura") &&
                        !equivalentStable.includes("auraMode") &&
                        !equivalentStable.includes("renderedGeoJson") &&
                        !equivalentStable.includes("canvasPixels") &&
                        !equivalentStable.includes("cacheHits") &&
                        !equivalentStable.includes("requestId"),
                    normalized_angle: keys.base.payload.investigation.aspect_overlay.angle,
                    normalized_planet: keys.base.payload.investigation.house_conditions[0].planet,
                    normalized_sampling: keys.base.payload.sampling
                };
            }"""
        )
        results.append(
            {
                "test": "semantic_cache_key_contract",
                "pass": bool(
                    cache_contract["equivalent_matches"]
                    and cache_contract["chart_differs"]
                    and cache_contract["condition_differs"]
                    and cache_contract["viewport_differs"]
                    and cache_contract["sampling_differs"]
                    and cache_contract["lat_cap_differs"]
                    and cache_contract["excluded_absent"]
                    and cache_contract["normalized_angle"] == "DC"
                    and cache_contract["normalized_planet"] == "moon"
                    and cache_contract["normalized_sampling"]["block_px"] == 12
                    and cache_contract["normalized_sampling"]["lat_cap"] is True
                ),
                "detail": cache_contract,
            }
        )
        paths_before_canonical_probe = len(requested_paths)
        canonical_probe = page.evaluate(
            """async () => {
                try {
                    await dispatchOverlayRequest({}, { substrate: "canonical_screen_space" });
                    return { threw: false, message: null };
                } catch (err) {
                    return { threw: true, message: String(err && err.message || err) };
                }
            }"""
        )
        canonical_probe_paths = requested_paths[paths_before_canonical_probe:]
        results.append(
            {
                "test": "canonical_branch_detectable_but_inactive",
                "pass": bool(
                    canonical_probe["threw"]
                    and "dry-run only" in canonical_probe["message"]
                    and not [
                        url
                        for url in canonical_probe_paths
                        if "/screen-pixel-truth" in url
                    ]
                ),
                "detail": {
                    "probe": canonical_probe,
                    "requests_during_probe": canonical_probe_paths,
                },
            }
        )
        before_paths = len(requested_paths)
        page.locator("#findBtn").click()
        page.wait_for_function(
            """() => {
                const s = window.__rmSmokeState?.();
                return s && /ready/i.test(s.renderStatus) && s.polygonLayers > 0;
            }""",
            timeout=60000,
        )
        render_paths = requested_paths[before_paths:]
        search_region_calls = [url for url in render_paths if "/search-regions" in url]
        screen_pixel_calls = [url for url in render_paths if "/screen-pixel-truth" in url]
        smoke_state_after_render = page.evaluate("() => window.__rmSmokeState?.() || null")
        results.append(
            {
                "test": "production_rendering_still_uses_legacy_search_regions",
                "pass": bool(
                    search_region_calls
                    and not screen_pixel_calls
                    and smoke_state_after_render["rendererSubstrate"]
                    == "legacy_search_regions"
                    and smoke_state_after_render["canonicalRendererBranchActive"] is False
                    and smoke_state_after_render["canonicalDryRunEnabled"] is False
                    and smoke_state_after_render["canonicalVisibleDebugEnabled"] is False
                    and smoke_state_after_render["canonicalDryRun"] is None
                    and smoke_state_after_render["canonicalVisibleDebug"] is None
                    and smoke_state_after_render["canonicalVisibleDebugLayers"] == 0
                ),
                "detail": {
                    "active_substrate": smoke_state_after_render["rendererSubstrate"],
                    "canonical_branch_active": smoke_state_after_render[
                        "canonicalRendererBranchActive"
                    ],
                    "canonical_dry_run_enabled": smoke_state_after_render[
                        "canonicalDryRunEnabled"
                    ],
                    "canonical_visible_debug_enabled": smoke_state_after_render[
                        "canonicalVisibleDebugEnabled"
                    ],
                    "canonical_dry_run": smoke_state_after_render["canonicalDryRun"],
                    "canonical_visible_debug": smoke_state_after_render[
                        "canonicalVisibleDebug"
                    ],
                    "canonical_visible_debug_layers": smoke_state_after_render[
                        "canonicalVisibleDebugLayers"
                    ],
                    "search_regions_calls": len(search_region_calls),
                    "screen_pixel_truth_calls": len(screen_pixel_calls),
                },
            }
        )
        results.append(
            {
                "test": "adapter_remains_observational_only",
                "pass": bool(
                    smoke_state_after_render
                    and smoke_state_after_render["substrateAdapter"]["version"] == 1
                    and smoke_state_after_render["polygonLayers"] > 0
                    and smoke_state_after_render["canonicalDryRun"] is None
                    and smoke_state_after_render["canonicalVisibleDebugLayers"] == 0
                ),
                "detail": {
                    "polygon_layers": smoke_state_after_render["polygonLayers"],
                    "aspect_layers": smoke_state_after_render["aspectLayers"],
                    "canonical_visible_debug_layers": smoke_state_after_render[
                        "canonicalVisibleDebugLayers"
                    ],
                    "adapter": smoke_state_after_render["substrateAdapter"],
                },
            }
        )
        dry_page = browser.new_page(viewport={"width": 1200, "height": 800})
        dry_requested_paths: list[str] = []
        dry_console_errors: list[str] = []
        dry_page.on("request", lambda req: dry_requested_paths.append(req.url))
        dry_page.on(
            "console",
            lambda msg: dry_console_errors.append(f"console.{msg.type}: {msg.text}")
            if msg.type == "error"
            else None,
        )
        dry_page.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1&canonicalDryRun=1",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        dry_page.wait_for_function(
            "() => window.__rmSmokeState?.().canonicalDryRunEnabled === true",
            timeout=10000,
        )
        dry_before_paths = len(dry_requested_paths)
        dry_page.locator("#findBtn").click()
        dry_page.wait_for_function(
            """() => {
                const s = window.__rmSmokeState?.();
                return s && /ready/i.test(s.renderStatus)
                    && s.polygonLayers > 0
                    && s.canonicalDryRun?.status === "ok";
            }""",
            timeout=60000,
        )
        dry_render_paths = dry_requested_paths[dry_before_paths:]
        dry_search_calls = [url for url in dry_render_paths if "/search-regions" in url]
        dry_screen_calls = [
            url for url in dry_render_paths if "/screen-pixel-truth" in url
        ]
        dry_state = dry_page.evaluate("() => window.__rmSmokeState?.() || null")
        results.append(
            {
                "test": "canonical_dry_run_enabled_shadow_only",
                "pass": bool(
                    dry_state
                    and dry_state["rendererSubstrate"] == "legacy_search_regions"
                    and dry_state["canonicalDryRunEnabled"] is True
                    and dry_state["canonicalDryRun"]["status"] == "ok"
                    and dry_state["canonicalDryRun"]["rendered"] is False
                    and dry_state["canonicalDryRun"]["maskCount"]
                    == dry_state["canonicalDryRun"]["pointCount"]
                    and dry_state["canonicalDryRun"]["comparison"]["metrics"]["status"]
                    == "ok"
                    and dry_state["canonicalDryRun"]["comparison"]["metrics"][
                        "legacyFeatureCount"
                    ]
                    > 0
                    and dry_state["canonicalDryRun"]["comparison"]["metrics"][
                        "canonicalPointCount"
                    ]
                    == dry_state["canonicalDryRun"]["pointCount"]
                    and dry_state["canonicalDryRun"]["comparison"]["metrics"][
                        "canonicalRendered"
                    ]
                    is False
                    and dry_state["canonicalDryRun"]["comparison"]["metrics"][
                        "visibleRenderer"
                    ]
                    == "legacy_search_regions"
                    and dry_state["polygonLayers"] > 0
                    and dry_search_calls
                    and dry_screen_calls
                    and not dry_console_errors
                ),
                "detail": {
                    "active_substrate": dry_state["rendererSubstrate"],
                    "canonical_dry_run": dry_state["canonicalDryRun"],
                    "polygon_layers": dry_state["polygonLayers"],
                    "search_regions_calls": len(dry_search_calls),
                    "screen_pixel_truth_calls": len(dry_screen_calls),
                    "console_errors": dry_console_errors,
                },
            }
        )
        dry_page.close()
        visible_page = browser.new_page(viewport={"width": 1200, "height": 800})
        visible_requested_paths: list[str] = []
        visible_console_errors: list[str] = []
        visible_page.on("request", lambda req: visible_requested_paths.append(req.url))
        visible_page.on(
            "console",
            lambda msg: visible_console_errors.append(f"console.{msg.type}: {msg.text}")
            if msg.type == "error"
            else None,
        )
        visible_page.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1&canonicalVisible=1",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        visible_page.wait_for_function(
            "() => window.__rmSmokeState?.().canonicalVisibleDebugEnabled === true",
            timeout=10000,
        )
        visible_before_paths = len(visible_requested_paths)
        visible_page.locator("#findBtn").click()
        visible_page.wait_for_function(
            """() => {
                const s = window.__rmSmokeState?.();
                return s && /ready/i.test(s.renderStatus)
                    && s.polygonLayers > 0
                    && s.canonicalDryRun?.status === "ok"
                    && s.canonicalVisibleDebug?.rendered === true
                    && s.canonicalVisibleDebugLayers > 0;
            }""",
            timeout=60000,
        )
        visible_render_paths = visible_requested_paths[visible_before_paths:]
        visible_search_calls = [
            url for url in visible_render_paths if "/search-regions" in url
        ]
        visible_screen_calls = [
            url for url in visible_render_paths if "/screen-pixel-truth" in url
        ]
        visible_state = visible_page.evaluate("() => window.__rmSmokeState?.() || null")
        visible_parity = (
            visible_state["canonicalDryRun"].get("parityDiagnostics")
            if visible_state and visible_state.get("canonicalDryRun")
            else None
        )
        results.append(
            {
                "test": "canonical_visible_debug_layer_explicit_only",
                "pass": bool(
                    visible_state
                    and visible_state["rendererSubstrate"] == "legacy_search_regions"
                    and visible_state["canonicalVisibleDebugEnabled"] is True
                    and visible_state["canonicalShowAllSamplesEnabled"] is False
                    and visible_state["canonicalDryRunEnabled"] is True
                    and visible_state["canonicalDryRun"]["status"] == "ok"
                    and visible_state["canonicalDryRun"]["rendered"] is True
                    and visible_state["canonicalDryRun"]["pointCount"] > 5
                    and visible_state["canonicalDryRun"]["blockPx"] == 12
                    and visible_state["canonicalVisibleDebug"]["debugOnly"] is True
                    and visible_state["canonicalVisibleDebug"]["blockPx"] == 12
                    and visible_state["canonicalVisibleDebug"]["layerCount"]
                    == visible_state["canonicalVisibleDebugLayers"]
                    and visible_state["canonicalVisibleDebugLayers"] > 0
                    and visible_state["canonicalVisibleDebug"]["paintedCount"]
                    == visible_state["canonicalVisibleDebug"]["matchedPaintedCount"]
                    and visible_state["canonicalVisibleDebug"]["unmatchedPaintedCount"] == 0
                    and visible_state["canonicalVisibleDebug"]["skippedUnmatchedCount"] > 0
                    and visible_state["canonicalVisibleDebug"]["matchedPaintedCount"]
                    == visible_state["canonicalDryRun"]["totalMatchedCount"]
                    and visible_state["canonicalDryRun"]["topologyRefinement"]["enabled"] is True
                    and visible_state["canonicalDryRun"]["topologyRefinement"][
                        "occupiedBoundaryCount"
                    ]
                    > 0
                    and visible_state["canonicalDryRun"]["topologyRefinement"][
                        "refinedPointCount"
                    ]
                    > 0
                    and visible_parity
                    and visible_parity["status"] == "measured"
                    and visible_parity["coarse"]["comparableCount"]
                    == visible_state["canonicalDryRun"]["pointCount"]
                    and visible_parity["refined"]["comparableCount"]
                    == visible_state["canonicalDryRun"]["topologyRefinement"][
                        "refinedPointCount"
                    ]
                    and visible_parity["refined"]["occupiedOverlapPct"]
                    >= visible_parity["boundary"]["occupiedOverlapPct"]
                    and visible_parity["refinedEdgeAgreementImprovementPct"] >= 0
                    and visible_parity["timingMs"]["comparison"] >= 0
                    and visible_state["polygonLayers"] > 0
                    and visible_search_calls
                    and visible_screen_calls
                    and not visible_console_errors
                ),
                "detail": {
                    "active_substrate": visible_state["rendererSubstrate"],
                    "canonical_dry_run": visible_state["canonicalDryRun"],
                    "parity_diagnostics": visible_parity,
                    "canonical_visible_debug": visible_state["canonicalVisibleDebug"],
                    "polygon_layers": visible_state["polygonLayers"],
                    "search_regions_calls": len(visible_search_calls),
                    "screen_pixel_truth_calls": len(visible_screen_calls),
                    "console_errors": visible_console_errors,
                },
            }
        )
        visible_page.close()
        all_page = browser.new_page(viewport={"width": 1200, "height": 800})
        all_requested_paths: list[str] = []
        all_console_errors: list[str] = []
        all_page.on("request", lambda req: all_requested_paths.append(req.url))
        all_page.on(
            "console",
            lambda msg: all_console_errors.append(f"console.{msg.type}: {msg.text}")
            if msg.type == "error"
            else None,
        )
        all_page.goto(
            f"{BASE}/map_CURRENT.html?skipOnboarding=1&canonicalVisible=1&canonicalShowAllSamples=1",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        all_page.wait_for_function(
            "() => window.__rmSmokeState?.().canonicalShowAllSamplesEnabled === true",
            timeout=10000,
        )
        all_before_paths = len(all_requested_paths)
        all_page.locator("#findBtn").click()
        all_page.wait_for_function(
            """() => {
                const s = window.__rmSmokeState?.();
                return s && /ready/i.test(s.renderStatus)
                    && s.polygonLayers > 0
                    && s.canonicalDryRun?.status === "ok"
                    && s.canonicalVisibleDebug?.rendered === true
                    && s.canonicalVisibleDebug?.unmatchedPaintedCount > 0;
            }""",
            timeout=60000,
        )
        all_render_paths = all_requested_paths[all_before_paths:]
        all_search_calls = [url for url in all_render_paths if "/search-regions" in url]
        all_screen_calls = [
            url for url in all_render_paths if "/screen-pixel-truth" in url
        ]
        all_state = all_page.evaluate("() => window.__rmSmokeState?.() || null")
        all_parity = (
            all_state["canonicalDryRun"].get("parityDiagnostics")
            if all_state and all_state.get("canonicalDryRun")
            else None
        )
        results.append(
            {
                "test": "canonical_show_all_samples_diagnostic_only",
                "pass": bool(
                    all_state
                    and all_state["rendererSubstrate"] == "legacy_search_regions"
                    and all_state["canonicalShowAllSamplesEnabled"] is True
                    and all_state["canonicalVisibleDebug"]["showAllSamples"] is True
                    and all_state["canonicalVisibleDebug"]["unmatchedPaintedCount"] > 0
                    and all_state["canonicalVisibleDebug"]["paintedCount"]
                    < all_state["canonicalVisibleDebug"]["pointCount"]
                    and all_state["canonicalVisibleDebug"]["skippedClampedCount"]
                    >= all_state["canonicalVisibleDebug"]["clampedSampleCount"]
                    and all_state["canonicalDryRun"]["topologyRefinement"]["enabled"] is True
                    and all_parity
                    and all_parity["status"] == "measured"
                    and all_parity["pointCount"]
                    == all_parity["coarse"]["comparableCount"]
                    + all_parity["refined"]["comparableCount"]
                    and all_state["polygonLayers"] > 0
                    and all_search_calls
                    and all_screen_calls
                    and not all_console_errors
                ),
                "detail": {
                    "active_substrate": all_state["rendererSubstrate"],
                    "canonical_visible_debug": all_state["canonicalVisibleDebug"],
                    "canonical_dry_run": all_state["canonicalDryRun"],
                    "parity_diagnostics": all_parity,
                    "polygon_layers": all_state["polygonLayers"],
                    "search_regions_calls": len(all_search_calls),
                    "screen_pixel_truth_calls": len(all_screen_calls),
                    "console_errors": all_console_errors,
                },
            }
        )
        all_page.close()
        mc12 = run_canonical_visible_probe(browser, angle="MC", block=12)
        mc8 = run_canonical_visible_probe(browser, angle="MC", block=8)
        mc8_zoom = run_canonical_visible_probe(browser, angle="MC", block=8, zoom_clicks=1)
        asc12 = run_canonical_visible_probe(browser, angle="ASC", block=12)
        mc12_diag = mc12["state"]["canonicalDryRun"]["continuityDiagnostics"]
        mc8_diag = mc8["state"]["canonicalDryRun"]["continuityDiagnostics"]
        mc8_zoom_diag = mc8_zoom["state"]["canonicalDryRun"]["continuityDiagnostics"]
        asc12_diag = asc12["state"]["canonicalDryRun"]["continuityDiagnostics"]
        results.append(
            {
                "test": "canonical_line_continuity_diagnostics_present",
                "pass": bool(
                    mc12_diag["samplingStatus"] in [
                        "no_matches_at_this_sampling_density",
                        "matched_samples_available",
                    ]
                    and mc8_diag["matchedPointCount"] > 0
                    and mc8_diag["stepCount"] > 0
                    and mc8_diag["maxSingleStepDeviation"] >= 0
                    and mc12_diag["neighborAngularDeltaVariance"] >= 0
                    and asc12_diag["matchedPointCount"] > 0
                    and asc12_diag["localHeadingChangeVariance"] >= 0
                    and mc12["screen_pixel_truth_calls"] > 0
                    and asc12["screen_pixel_truth_calls"] > 0
                    and not mc12["console_errors"]
                    and not asc12["console_errors"]
                ),
                "detail": {
                    "mc_block12": mc12_diag,
                    "mc_block8": mc8_diag,
                    "asc_block12": asc12_diag,
                    "mc_calls": {
                        "search_regions": mc12["search_regions_calls"],
                        "screen_pixel_truth": mc12["screen_pixel_truth_calls"],
                    },
                    "asc_calls": {
                        "search_regions": asc12["search_regions_calls"],
                        "screen_pixel_truth": asc12["screen_pixel_truth_calls"],
                    },
                },
            }
        )
        results.append(
            {
                "test": "canonical_line_zoom_sampling_stability",
                "pass": bool(
                    mc8_diag["matchedPointCount"] > mc12_diag["matchedPointCount"]
                    and mc8_diag["blockPx"] == 8
                    and mc12_diag["blockPx"] == 12
                    and (
                        mc12_diag["samplingStatus"] == "no_matches_at_this_sampling_density"
                        or mc8_diag["maxSingleStepDeviation"]
                        <= max(mc12_diag["maxSingleStepDeviation"] * 1.5, 1)
                    )
                    and mc8_diag["neighborAngularDeltaVariance"] <= 0.001
                    and mc8_diag["discontinuityCount"] == 0
                    and mc8_zoom_diag["matchedPointCount"] > 0
                    and mc8_zoom_diag["zoom"] > mc8_diag["zoom"]
                    and not mc8["console_errors"]
                    and not mc8_zoom["console_errors"]
                ),
                "detail": {
                    "mc_block12": mc12_diag,
                    "mc_block8": mc8_diag,
                    "mc_block8_zoomed": mc8_zoom_diag,
                    "interpretation": "MC block 12 missed the line while block 8 and zoomed block 8 show a straight stable vertical sample set; this indicates sampling aliasing, not periodic geometric wobble.",
                },
            }
        )
        stress_cases = [
            {
                "label": "asc_angle_plus_sun_house",
                "block": 12,
                "payload_patch": {
                    "house_conditions": [{"planet": "sun", "house": 1}],
                    "angle_sign_conditions": [{"angle": "ASC", "sign": "scorpio"}],
                },
            },
            {
                "label": "mc_angle_plus_saturn_house",
                "block": 12,
                "payload_patch": {
                    "house_conditions": [{"planet": "saturn", "house": 10}],
                    "angle_sign_conditions": [{"angle": "MC", "sign": "capricorn"}],
                },
            },
            {
                "label": "triple_house_overlap",
                "block": 12,
                "payload_patch": {
                    "house_conditions": [
                        {"planet": "sun", "house": 1},
                        {"planet": "moon", "house": 7},
                        {"planet": "saturn", "house": 10},
                    ]
                },
            },
            {
                "label": "narrow_orb_asc_aspect",
                "block": 12,
                "payload_patch": {
                    "aspect_overlay": {
                        "planet": "sun",
                        "aspect": "conjunction",
                        "angle": "ASC",
                        "orb": 0.35,
                    }
                },
            },
            {
                "label": "high_latitude_asc_aspect",
                "block": 12,
                "map_action": "high_latitude",
                "payload_patch": {
                    "aspect_overlay": {
                        "planet": "sun",
                        "aspect": "conjunction",
                        "angle": "ASC",
                        "orb": 1.0,
                    }
                },
            },
            {
                "label": "seam_mc_aspect",
                "block": 12,
                "map_action": "seam",
                "payload_patch": {
                    "aspect_overlay": {
                        "planet": "saturn",
                        "aspect": "conjunction",
                        "angle": "MC",
                        "orb": 1.0,
                    }
                },
            },
        ]
        stress_probes = [
            run_canonical_payload_probe(browser, **case) for case in stress_cases
        ]
        stress_summary = [summarize_stress_probe(probe) for probe in stress_probes]
        measured_stress_summary = [item for item in stress_summary if item["measured"]]
        improved_cases = [
            item
            for item in measured_stress_summary
            if item["refinedEdgeAgreementImprovementPct"] >= 0
        ]
        overlap_heavy_cases = [
            item
            for item in measured_stress_summary
            if item["refinedPointCount"] > 0 and item["matchedPointCount"] > 0
        ]
        cap_disagreement_total = sum(item["capDisagreementCount"] for item in measured_stress_summary)
        seam_disagreement_total = sum(item["seamDisagreementCount"] for item in measured_stress_summary)
        results.append(
            {
                "test": "canonical_multicondition_parity_stress",
                "pass": bool(
                    len(stress_summary) == len(stress_cases)
                    and len(measured_stress_summary) >= 4
                    and len(improved_cases) >= 3
                    and len(overlap_heavy_cases) >= 3
                    and all(probe["search_regions_calls"] > 0 for probe in stress_probes)
                    and all(probe["screen_pixel_truth_calls"] >= 1 for probe in stress_probes)
                    and all(not probe["console_errors"] for probe in stress_probes)
                    and all(
                        probe["state"]["rendererSubstrate"] == "legacy_search_regions"
                        for probe in stress_probes
                    )
                    and all(
                        probe["state"]["canonicalVisibleDebugEnabled"] is True
                        for probe in stress_probes
                    )
                    and all(
                        item.get("canonicalElapsedMs") is None
                        or item["canonicalElapsedMs"] < 5000
                        for item in stress_summary
                    )
                ),
                "detail": {
                    "stress_cases": stress_summary,
                    "measured_case_count": len(measured_stress_summary),
                    "improved_case_count": len(improved_cases),
                    "overlap_heavy_case_count": len(overlap_heavy_cases),
                    "cap_disagreement_total": cap_disagreement_total,
                    "seam_disagreement_total": seam_disagreement_total,
                    "interpretation": "Stress probes exercise multi-condition, narrow-orb, high-latitude, and seam-centered debug parity without switching production off legacy_search_regions.",
                },
            }
        )
        wall_cases = [
            {
                "label": "wall_narrow_orb_asc_aspect",
                "payload_patch": {
                    "aspect_overlay": {
                        "planet": "sun",
                        "aspect": "conjunction",
                        "angle": "ASC",
                        "orb": 0.35,
                    }
                },
            },
            {
                "label": "wall_asc_angle_plus_sun_house",
                "payload_patch": {
                    "house_conditions": [{"planet": "sun", "house": 1}],
                    "angle_sign_conditions": [{"angle": "ASC", "sign": "scorpio"}],
                },
            },
            {
                "label": "wall_high_latitude_asc_aspect",
                "map_action": "high_latitude",
                "payload_patch": {
                    "aspect_overlay": {
                        "planet": "sun",
                        "aspect": "conjunction",
                        "angle": "ASC",
                        "orb": 1.0,
                    }
                },
            },
            {
                "label": "wall_seam_mc_aspect",
                "map_action": "seam",
                "payload_patch": {
                    "aspect_overlay": {
                        "planet": "saturn",
                        "aspect": "conjunction",
                        "angle": "MC",
                        "orb": 1.0,
                    }
                },
            },
            {
                "label": "wall_clean_mc_control",
                "payload_patch": {
                    "aspect_overlay": {
                        "planet": "saturn",
                        "aspect": "conjunction",
                        "angle": "MC",
                        "orb": 1.0,
                    }
                },
            },
        ]
        wall_probes = [run_full_pixel_wall_probe(browser, **case) for case in wall_cases]
        wall_metrics = [probe["metrics"] for probe in wall_probes]
        canonical_closer = [
            item
            for item in wall_metrics
            if item["refinedVsWall"]["closerToWall"] in ("canonical", "tie")
        ]
        seam_case = next(item for item in wall_metrics if item["label"] == "wall_seam_mc_aspect")
        asc_cases = [item for item in wall_metrics if "asc" in item["label"]]
        anomaly_cases = [
            item for item in wall_metrics if item["label"] != "wall_clean_mc_control"
        ]
        targeted_cases = [item for item in wall_metrics if item["targetedAscDsc"]]
        topology_cases = [
            item
            for item in wall_metrics
            if item.get("topologyExtraction", {}).get("subpixelPositiveCount", 0) > 0
        ]
        coherent_topology_cases = [
            item
            for item in topology_cases
            if item["topologyExtraction"]["coherentTrajectory"]
        ]
        extracted_topology_cases = [
            item
            for item in topology_cases
            if item["topologyExtraction"]["continuousTopology"]["coherentTopology"]
        ]
        path_solver_bounded_cases = [
            item
            for item in topology_cases
            if item["topologyExtraction"]["pathSolver"]["discontinuityCount"]
            <= item["topologyExtraction"]["crudeOrdering"]["discontinuityCount"]
            and item["topologyExtraction"]["pathSolver"]["seamDiscontinuityCount"] == 0
            and item["topologyExtraction"]["pathSolver"]["capAdjacentDiscontinuityCount"] == 0
        ]
        asc_false_negative_improved_or_bounded = [
            item
            for item in targeted_cases
            if item["refinedVsWall"]["canonicalFalseNegativeCount"]
            <= item["baselineRefinedVsWall"]["canonicalFalseNegativeCount"]
            or item["refinedVsWall"]["canonicalFalseNegativeCount"] <= 3
        ]
        results.append(
            {
                "test": "canonical_full_pixel_wall_anomaly_check",
                "pass": bool(
                    len(wall_metrics) == len(wall_cases)
                    and all(item["wallHttpStatus"] == 200 for item in wall_metrics)
                    and all(item["topologyHttpStatus"] == 200 for item in wall_metrics)
                    and all(item["wallPointCount"] > 100000 for item in wall_metrics)
                    and len(canonical_closer) >= 3
                    and seam_case["seamProbe"]["longitudeOutOfRangeCount"] == 0
                    and seam_case["seamProbe"]["duplicatePixelCount"]
                    <= seam_case["refinedVsWall"]["comparableCount"]
                    and all(item["refinedPointCount"] > 0 for item in anomaly_cases)
                    and len(targeted_cases) >= 1
                    and all(item["maxDepth"] == 2 for item in targeted_cases)
                    and all(item["secondLevelPointCount"] > 0 for item in targeted_cases)
                    and len(asc_false_negative_improved_or_bounded) == len(targeted_cases)
                    and len(topology_cases) >= 3
                    and len(coherent_topology_cases) >= 2
                    and len(extracted_topology_cases) >= 2
                    and len(path_solver_bounded_cases) == len(topology_cases)
                    and seam_case["topologyExtraction"]["coherentTrajectory"] is True
                    and seam_case["topologyExtraction"]["continuousTopology"][
                        "coherentTopology"
                    ]
                    is True
                    and all(probe["search_regions_calls"] > 0 for probe in wall_probes)
                    and all(probe["screen_pixel_truth_calls"] >= 2 for probe in wall_probes)
                    and all(not probe["console_errors"] for probe in wall_probes)
                ),
                "detail": {
                    "wall_cases": wall_metrics,
                    "canonical_closer_or_tied_count": len(canonical_closer),
                    "targeted_case_count": len(targeted_cases),
                    "topology_case_count": len(topology_cases),
                    "coherent_topology_case_count": len(coherent_topology_cases),
                    "extracted_topology_case_count": len(extracted_topology_cases),
                    "path_solver_bounded_case_count": len(path_solver_bounded_cases),
                    "asc_false_negative_improved_or_bounded_count": len(
                        asc_false_negative_improved_or_bounded
                    ),
                    "asc_case_root_causes": {
                        item["label"]: item["rootCauseHint"] for item in asc_cases
                    },
                    "seam_case_root_cause": seam_case["rootCauseHint"],
                },
            }
        )
        results.append(
            {
                "test": "console_clean",
                "pass": not console_errors,
                "detail": {"errors": console_errors},
            }
        )
        browser.close()

    payload = {"results": results, "all_pass": all(item["pass"] for item in results)}
    print(json.dumps(payload, indent=2))
    return 0 if payload["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
