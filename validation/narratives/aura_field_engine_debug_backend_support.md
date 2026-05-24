# Aura Field Engine Debug Backend Support

Date: 2026-05-24

## Status

`aura_field_engine.py` is debug/prototype backend support.

It is:

- backend-imported,
- not default production rendering,
- not product UI,
- not a renderer substrate flip,
- not production aura approval,
- and not an approved aura visual language.

The module exists to preserve and validate explicit aura/debug prototype paths. It must not be treated as production renderer integration.

## Backend Contact

`main_centerline_FIXER.py` imports `aura_field_engine.py`.

The imported engine supports explicit aura/debug routes:

- `POST /aura-field`
- `POST /aura-raster`
- `POST /aura-raster-adaptive`
- `POST /aura-raster-convergence`
- `GET /aura-refinement-reveal-stages`
- `GET /aspect-orb-at-point`

These routes are explicit debug/prototype surfaces. Default map behavior does not invoke them.

The default production substrate remains:

```text
legacy_search_regions
```

## Boundaries

`aura_field_engine.py` does not:

- render in the browser by itself,
- mutate DOM, map, or Leaflet layers,
- flip renderer substrate,
- hydrate production layers,
- create recommendation/scoring/final-truth surfaces,
- create product UI,
- approve aura visual language,
- or replace the default `legacy_search_regions` production path.

It computes debug/prototype aura payloads for explicit backend routes. Some payloads may include GeoJSON/debug metadata, but those outputs are not default production rendering and are not product UI.

Aura visual design remains gated by the aura visual design brief before any production aura rendering work.

## Smoke Validation

Run:

```bash
./venv/bin/python scripts/smoke_map_current_aura_debug.py
```

Pass criteria:

- aura debug smoke passes,
- default production substrate remains `legacy_search_regions`,
- aura paths require explicit debug flags,
- no runaway Leaflet aura polygon layers are created,
- console remains clean.

## Rollback Scope

Rollback is limited to:

- removing the explicit aura/debug routes if needed,
- removing the backend import if needed,
- removing `aura_field_engine.py` if needed,
- removing the aura debug smoke/report/narrative if needed.

The default `legacy_search_regions` path remains recoverable because default production rendering does not depend on aura backend routes.

## Governance Closeout

- **Accepted scope:** debug/prototype backend support for explicit aura routes.
- **Rejected scope:** default production rendering, product UI, renderer substrate flip, production aura approval, recommendation/scoring/final-truth surfaces.
- **Next allowed step:** commit only after aura debug smoke passes, with a narrow scope that excludes default production renderer files and unrelated workspace changes.
