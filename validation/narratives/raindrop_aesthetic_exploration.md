# Raindrop / Virga Aesthetic Exploration

Sandbox only. No changes to astrology math, `map_CURRENT.html`, or the proven adaptive renderer.

## Sandbox

- URL base: `http://127.0.0.1:8000/map_SANDBOX_raindrop_aesthetic.html`
- File: `map_SANDBOX_raindrop_aesthetic.html`

Example:
```
http://127.0.0.1:8000/map_SANDBOX_raindrop_aesthetic.html?A=pih:sun:1&mode=virga&pace=5000&density=magical&auto=1
```

## Visual modes tested (5)

| mode | intent |
|------|--------|
| `blue_noise` | jittered probes; anti-grid soldiers |
| `bacteria` | organic clustering near hits |
| `virga` | faint ghost condition fades as target clarifies |
| `harmonic` | overtone-style opacity ramp + colorify |
| `fibonacci` | Fibonacci-weight opacity ramp + colorify |

## Pace variants (ms)

2000, 3000, 5000, 7000

## Density packs

sparse, readable, magical, dense

## Timing summary

| case | wall_s | samples | server_s | match_dots |
|------|-------:|--------:|---------:|-----------:|
| `blue_noise_5s_readable` | 907.94 | 150,463 | 1.02 | 40,737 |
| `bacteria_5s_readable` | 1669.77 | 151,313 | 1.16 | 40,691 |
| `virga_5s_readable` | 155.56 | 86,204 | 1.00 | 19,828 |
| `harmonic_5s_readable` | 202.99 | 77,132 | 1.19 | 19,828 |
| `fibonacci_5s_readable` | 179.28 | 77,132 | 1.26 | 19,828 |
| `bacteria_2000ms_readable` | 1487.53 | 116,515 | 1.76 | 51,616 |
| `bacteria_3000ms_readable` | 964.95 | 79,213 | 0.58 | 21,594 |
| `bacteria_7000ms_readable` | 1521.81 | 79,213 | 0.55 | 21,594 |
| `bacteria_5s_sparse` | 1025.76 | 79,534 | 0.80 | 22,211 |
| `bacteria_5s_magical` | 50.68 | 77,618 | 0.58 | 21,234 |
| `bacteria_5s_dense` | 51.55 | 77,508 | 0.56 | 21,156 |

## Perceived notes (honest, not over-polished)

### Feels magical
- **`bacteria` + `magical` density + 5s pace** — dots hunt structure; pace long enough for Phase-2 cache window without feeling stuck.
- **`virga` + `readable` + 5–7s** — ghost hint of Moon/4th (or other `?ghost=`) then Sun-in-1st colorifies; contemplative, not noisy.
- **`harmonic` at 5s** — opacity breathes toward matches; map labels stay legible if density ≤ magical.

### Feels gimmicky / risky
- **`dense` + 2s pace** — reads as muddy snow; no time for background cache; annoys.
- **`fibonacci` + `dense`** — opacity steps can feel "UI demo" unless pace ≥ 5s.
- **`sparse` + 2s** — pretty but underwhelming; feels like a loading spinner, not discovery.

### Six-condition readability
- Sandbox supports A–F slots (6 conditions). Overlap colors are averaged proof tints — **mush appears above 3 conditions** on `dense`. Recommendation: product cap **3 visible** overlays for aesthetics even if API allows 6.

## Phase-2 cache interaction

Pace is also **background-cache budget**:
- **2s**: almost no idle cache after first paint.
- **5s**: comfortable window for priorities A–C on Americas viewport (per phase2 smoke).
- **7s**: best for virga/ghost fades; may feel slow for power users.

## Render budget (backward from chosen density)

Preferred direction: **`bacteria` + `readable` + 5000ms**.

From captured `readable` runs, scale samples by density preset (`budgetScale` in sandbox):
- readable ≈ baseline samples in manifest
- magical ≈ 1.0× readable
- sparse ≈ 0.55×
- dense ≈ 1.35× (not recommended for product)

Ship budget: use measured adaptive **+20%** floor (`233,118` samples / 720×450) from targeted stress; raindrop reveal adds **wall-clock pacing only**, not extra truth samples.

## Recommendation (one direction)

**Primary:** `bacteria` clustering + incremental colorify + harmonic opacity (combine bacteria probe placement with harmonic curve, 5s default pace, `readable` density).

**Secondary palette:** keep `virga` ghost pass for first 40% of timeline only when user enables a second exploratory layer.

**Avoid:** grid-soldier reveals, `dense` packing, sub-3s pace for multi-condition stacks.

## Artifacts

- Screenshots: `validation/screenshots/raindrop_aesthetic`
- Manifest: `validation/screenshots/raindrop_aesthetic/manifest.json`
