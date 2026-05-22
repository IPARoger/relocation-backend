# Canonical Visible Defect Diagnosis

Date: 2026-05-22

## Scope

Phase 1.10.1 diagnoses defects observed in the debug-only `?canonicalVisible=1` layer. It does not advance to Phase 1.11, does not make canonical rendering default, and does not change astrology math, cache behavior, aura, aesthetics, or animation.

## Root Cause

The visible canonical debug canvas was painting every sampled viewport block. Matched blocks and unmatched blocks used different translucent colors, but the unmatched blocks still formed a continuous screen grid. At coarse viewport density this could read as:

- broad horizontal/global belts,
- large rectangular chunks,
- false regions near the ±65° product cap,
- or apparent canonical/legacy disagreement.

This was a debug rendering artifact, not proven backend truth failure. The canonical response already marked matches with masks; the painter was treating non-matches as visually meaningful.

## What Was Fixed

Default `?canonicalVisible=1` now paints only matched/occupied blocks. Unmatched blocks are skipped by default.

An explicit diagnostic flag was added:

```text
canonicalShowAllSamples=1
```

Only this flag paints unmatched samples, and even then samples outside the ±65° product cap are skipped so cap rows cannot appear as meaningful global belts.

## Metrics Added

The smoke/debug state now records:

- matched block count,
- unmatched block count,
- visible matched block count,
- visible unmatched block count,
- skipped unmatched block count,
- samples outside/clamped by the ±65° cap,
- skipped cap-row count,
- condition type being rendered,
- block size,
- point count,
- legacy feature count,
- canonical elapsed time.

## Debug Artifact Vs Possible Truth Issue

The broad pale grid and cap bands were debug artifacts from painting non-matches. The remaining matched blocks are actual canonical positive masks for the sampled condition and are therefore more meaningful for visual inspection.

Still unproven:

- whether matched canonical blocks align acceptably with legacy line/polygon geometry,
- whether ASC/aspect line continuity is stable across zooms and pans,
- whether boundary wobble is acceptable,
- whether full-density or adaptive canonical rendering behaves the same way.

## Phase 1.11 Readiness

Phase 1.11 is allowed only as a comparison/parity phase, not as default migration. The canonical visible layer is now trustworthy enough for matched-block inspection, but it is still debug-only and coarse.

## Rollback

Rollback removes `canonicalShowAllSamples`, matched-only paint gating, cap-row skip metrics, the added smoke assertions, and this narrative. The legacy production renderer remains untouched.
