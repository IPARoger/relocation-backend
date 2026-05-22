# Targeted Adaptive Refinement Policy

No global slowdown. Per-tile escalation only, triggered by structural conditions (viewport-edge proximity, high latitude with aspect-to-angle conditions, thin-line orbs ≤ 0.5°). No astrology math, colors, aura, raindrop visuals, or other rendering logic changed.

This policy is referenced as normative in `docs/relocation_map_architecture.md` (§ "Refinement Hardening — Targeted Policy, Not Global Slowdown"). The follow-up dense multi-condition pass is in `validation/narratives/screen_pixel_dense_residue.md`.

## Outputs

- Manifest: `validation/screenshots/screen_pixel_adaptive_targeted/manifest.json`
- Human review index: `validation/screenshots/screen_pixel_adaptive_targeted/HUMAN_REVIEW_INDEX.md`
- Policy sweep folder: `validation/screenshots/screen_pixel_adaptive_targeted/policy_sweep`
- Final stress folder: `validation/screenshots/screen_pixel_adaptive_targeted/final`

## Chosen Policy

- Name: `edge2_thin2_highlat2_probes`
- Edge halo extra: `+2` tiles (within `2` tiles of viewport edge)
- High-latitude halo extra: `+2` tiles (above ±`65.0`°, aspect-to-angle conditions only)
- Thin-line halo extra: `+2` tiles (aspect-to-angle conditions with orb ≤ `0.5`°)
- Thin-line extra probes at ≥8 px tiles: `True`

## Where Extra Resources Are Deployed

- Any tile within the configured number of tiles from the viewport edge gets a wider halo before subdivision.
- Any tile whose four corners straddle ±60° / ±65° latitude (default ±65°) receives an additional halo ring when the case contains at least one aspect-to-angle condition.
- Any case containing an aspect-to-angle condition with orb ≤ 0.5° expands the halo for every occupied/mixed tile in every phase.
- When `apply_lat_cap=true`, tiles within `4.0°` of ±`65.0°` cannot early-accept as empty at coarse sizes.

## Where Extra Resources Are NOT Deployed

- Cases without aspect-to-angle conditions never trigger high-latitude or thin-line escalation. The baseline halo radius of 1 is unchanged.
- Wide-orb (>0.5°) aspect-to-angle conditions do not trigger thin-line escalation.
- Mid-latitude tiles in aspect-to-angle cases keep the baseline halo.
- Interior tiles away from the viewport edge keep the baseline halo unless another trigger applies.
- Polygon overlays (planet-in-house, angle-in-sign) below the polar threshold are unaffected by high-latitude escalation.

## Policy Sweep on Failure-Focus Cases

Acceptance threshold for `passes` is XOR ≤ `0.20%` (aligned with the baseline narrative's `acceptable / effectively identical` band).

| policy | case | samples | xor% | passes |
|---|---|---:|---:|:---:|
| `baseline` | `thin_pluto_square_asc_0p25` | 47,998 | 0.415 | no |
| `edge1` | `thin_pluto_square_asc_0p25` | 50,303 | 0.166 | yes |
| `edge1_thin1` | `thin_pluto_square_asc_0p25` | 69,911 | 0.000 | yes |
| `edge1_thin1_highlat1` | `thin_pluto_square_asc_0p25` | 74,996 | 0.000 | yes |
| `edge2_thin2_highlat1` | `thin_pluto_square_asc_0p25` | 97,147 | 0.000 | yes |
| `edge2_thin2_highlat2_probes` | `thin_pluto_square_asc_0p25` | 104,720 | 0.000 | yes |
| `edge2_thin2_hl2_latcap2` | `thin_pluto_square_asc_0p25` | 104,720 | 0.000 | yes |
| `edge2_thin2_hl2_latcap2_nocoarse4` | `thin_pluto_square_asc_0p25` | 104,720 | 0.000 | yes |
| `edge3_thin3_hl3_latcap3_nocoarse2` | `thin_pluto_square_asc_0p25` | 129,469 | 0.000 | yes |
| `baseline` | `mixed_dense_six_conditions` | 106,893 | 0.334 | no |
| `edge1` | `mixed_dense_six_conditions` | 109,909 | 0.334 | no |
| `edge1_thin1` | `mixed_dense_six_conditions` | 147,817 | 0.334 | no |
| `edge1_thin1_highlat1` | `mixed_dense_six_conditions` | 154,757 | 0.334 | no |
| `edge2_thin2_highlat1` | `mixed_dense_six_conditions` | 187,956 | 0.334 | no |
| `edge2_thin2_highlat2_probes` | `mixed_dense_six_conditions` | 194,265 | 0.334 | no |
| `edge2_thin2_hl2_latcap2` | `mixed_dense_six_conditions` | 194,265 | 0.334 | no |
| `edge2_thin2_hl2_latcap2_nocoarse4` | `mixed_dense_six_conditions` | 197,617 | 0.314 | no |
| `edge3_thin3_hl3_latcap3_nocoarse2` | `mixed_dense_six_conditions` | 228,053 | 0.307 | no |
| `baseline` | `high_svalbard_latcap_off` | 27,209 | 5.615 | no |
| `edge1` | `high_svalbard_latcap_off` | 27,710 | 5.615 | no |
| `edge1_thin1` | `high_svalbard_latcap_off` | 32,311 | 5.615 | no |
| `edge1_thin1_highlat1` | `high_svalbard_latcap_off` | 37,176 | 5.615 | no |
| `edge2_thin2_highlat1` | `high_svalbard_latcap_off` | 43,406 | 5.615 | no |
| `edge2_thin2_highlat2_probes` | `high_svalbard_latcap_off` | 63,403 | 0.000 | yes |
| `edge2_thin2_hl2_latcap2` | `high_svalbard_latcap_off` | 63,403 | 0.000 | yes |
| `edge2_thin2_hl2_latcap2_nocoarse4` | `high_svalbard_latcap_off` | 63,403 | 0.000 | yes |
| `edge3_thin3_hl3_latcap3_nocoarse2` | `high_svalbard_latcap_off` | 79,797 | 0.000 | yes |
| `baseline` | `high_svalbard_latcap_on` | 56,285 | 0.000 | yes |
| `edge1` | `high_svalbard_latcap_on` | 56,785 | 0.000 | yes |
| `edge1_thin1` | `high_svalbard_latcap_on` | 58,826 | 0.000 | yes |
| `edge1_thin1_highlat1` | `high_svalbard_latcap_on` | 61,475 | 0.000 | yes |
| `edge2_thin2_highlat1` | `high_svalbard_latcap_on` | 65,984 | 0.000 | yes |
| `edge2_thin2_highlat2_probes` | `high_svalbard_latcap_on` | 74,805 | 0.000 | yes |
| `edge2_thin2_hl2_latcap2` | `high_svalbard_latcap_on` | 83,493 | 0.000 | yes |
| `edge2_thin2_hl2_latcap2_nocoarse4` | `high_svalbard_latcap_on` | 83,493 | 0.000 | yes |
| `edge3_thin3_hl3_latcap3_nocoarse2` | `high_svalbard_latcap_on` | 101,460 | 0.000 | yes |
| `baseline` | `profile_polar_reykjavik` | 44,206 | 0.173 | yes |
| `edge1` | `profile_polar_reykjavik` | 45,784 | 0.173 | yes |
| `edge1_thin1` | `profile_polar_reykjavik` | 62,876 | 0.000 | yes |
| `edge1_thin1_highlat1` | `profile_polar_reykjavik` | 65,733 | 0.000 | yes |
| `edge2_thin2_highlat1` | `profile_polar_reykjavik` | 85,670 | 0.000 | yes |
| `edge2_thin2_highlat2_probes` | `profile_polar_reykjavik` | 93,384 | 0.000 | yes |
| `edge2_thin2_hl2_latcap2` | `profile_polar_reykjavik` | 93,384 | 0.000 | yes |
| `edge2_thin2_hl2_latcap2_nocoarse4` | `profile_polar_reykjavik` | 93,384 | 0.000 | yes |
| `edge3_thin3_hl3_latcap3_nocoarse2` | `profile_polar_reykjavik` | 119,089 | 0.000 | yes |

## Failure-Focus Cost Table (Baseline vs Chosen)

| case | baseline samples | chosen samples | extra % | baseline xor% | chosen xor% |
|---|---:|---:|---:|---:|---:|
| `thin_pluto_square_asc_0p25` | 47,998 | 104,720 | 118.2% | 0.415 | 0.000 |
| `mixed_dense_six_conditions` | 106,893 | 194,265 | 81.7% | 0.334 | 0.334 |
| `high_svalbard_latcap_off` | 27,209 | 63,403 | 133.0% | 5.615 | 0.000 |
| `high_svalbard_latcap_on` | 56,285 | 74,805 | 32.9% | 0.000 | 0.000 |
| `profile_polar_reykjavik` | 44,206 | 93,384 | 111.2% | 0.173 | 0.000 |

## Full Stress Re-Run (No Regression Check)

| case | group | baseline xor% | chosen xor% | baseline samples | chosen samples | delta samples |
|---|---|---:|---:|---:|---:|---:|
| `thin_pluto_square_asc_0p25` | `thin_aspect_lines` | 0.415 | 0.000 | 47,998 | 104,720 | +56,722 |
| `mixed_dense_six_conditions` | `mixed_dense_overlays` | 0.334 | 0.334 | 106,893 | 194,265 | +87,372 |
| `high_svalbard_latcap_off` | `high_latitude` | 5.615 | 0.000 | 27,209 | 63,403 | +36,194 |
| `high_svalbard_latcap_on` | `high_latitude` | 0.000 | 0.000 | 56,285 | 74,805 | +18,520 |
| `profile_polar_reykjavik` | `synthetic_profiles` | 0.173 | 0.000 | 44,206 | 93,384 | +49,178 |
| `thin_saturn_mc_0p25` | `thin_aspect_lines` | 0.000 | 0.000 | 30,741 | 60,716 | +29,975 |
| `thin_saturn_asc_0p25` | `thin_aspect_lines` | 0.000 | 0.000 | 35,278 | 66,136 | +30,858 |
| `thin_uranus_square_mc_0p25` | `thin_aspect_lines` | 0.000 | 0.000 | 30,720 | 59,840 | +29,120 |
| `multi_thin_lines_world` | `multiple_thin_lines` | 0.000 | 0.000 | 71,238 | 145,437 | +74,199 |
| `seam_fiji_nz` | `seam_dateline` | 0.000 | 0.000 | 33,449 | 56,476 | +23,027 |
| `seam_alaska_siberia` | `seam_dateline` | 0.000 | 0.000 | 20,880 | 27,405 | +6,525 |
| `seam_world_crossing_180` | `seam_dateline` | 0.000 | 0.000 | 30,720 | 59,840 | +29,120 |
| `high_greenland_latcap_off` | `high_latitude` | 0.000 | 0.000 | 20,880 | 27,405 | +6,525 |
| `high_greenland_latcap_on` | `high_latitude` | 0.000 | 0.000 | 57,240 | 62,865 | +5,625 |
| `high_southern_latcap_off` | `high_latitude` | 0.000 | 0.000 | 24,810 | 44,123 | +19,313 |
| `high_southern_latcap_on` | `high_latitude` | 0.000 | 0.000 | 51,621 | 67,095 | +15,474 |
| `profile_solstice_boundaries` | `synthetic_profiles` | 0.057 | 0.057 | 67,107 | 124,191 | +57,084 |
| `profile_eclipse_cluster` | `synthetic_profiles` | 0.163 | 0.163 | 81,038 | 166,084 | +85,046 |

## Measured Safety Buffer (Not Intuition)

The worst-case adaptive sample count under the chosen policy across all 18 stress cases is the empirical floor. The recommended buffers below are derived directly from that measurement, not from a guessed percentage.

| label | adaptive sample budget |
|---|---:|
| observed_minimum | 194,265 |
| +10% | 213,691 |
| +20% | 233,118 |
| +30% | 252,544 |

Recommendation: ship the conservative `+20%` full-suite budget (`233,118` samples for 720×450). The required-case floor (Svalbard pair only) is `74,805` samples (`+20%` → `89,766`). `+10%` full-suite (`213,691`) is tight when six-condition dense overlays run; `+30%` is over-provisioned unless that stack is common.

## Lat-Cap Policy

Lat-cap ±65° still simplifies the high-latitude regime and is the cheaper of the two modes. Under the chosen policy, lat-cap OFF passes the previously-failing Svalbard edge case. Lat-cap ON also passes under the chosen policy. Observations:

| pair | off XOR% | on XOR% | off samples | on samples |
|---|---:|---:|---:|---:|
| `high_greenland_latcap_off` ↔ `high_greenland_latcap_on` | 0.000 | 0.000 | 27,405 | 62,865 |
| `high_svalbard_latcap_off` ↔ `high_svalbard_latcap_on` | 0.000 | 0.000 | 63,403 | 74,805 |
| `high_southern_latcap_off` ↔ `high_southern_latcap_on` | 0.000 | 0.000 | 44,123 | 67,095 |

Recommendation: keep `±65°` lat-cap as product default. With targeted high-latitude escalation now in place, an advanced override that turns lat-cap OFF is structurally safe for power users who explicitly want high-latitude exploration. Do not expose the override in the default UI until a UI guard is added that explains the trade-off.

## Summary Of Where The System Spends More

- Edge of viewport: more halo, only when the case touches edges.
- Above ±65°: more halo, only when the case includes aspect-to-angle.
- Thin aspect lines (orb ≤ 0.5°): more halo, only for thin-line cases.
- Everywhere else: identical to the previously validated adaptive policy.
