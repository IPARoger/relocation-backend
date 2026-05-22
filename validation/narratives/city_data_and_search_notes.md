# City data and search (current limitations)

**Product doctrine / roadmap:** `docs/geocoder_and_city_identity_strategy.md` · **Basemap language & city rendering:** `docs/cartographic_language_and_city_rendering.md`

## Current structure (`cities.js`)

Each record is a flat object with **four fields**:

- `name` — string (city or locality name)
- `lat`, `lng` — numbers (WGS84)
- `pop` — number (used for zoom-based visibility thresholds)

There is **no** `country`, `state`, `admin1`, `geonameid`, or alternate names array in this file.

## Country display

- **UI:** City-driven popups (search Enter and marker click) show a short note that the city list has no country field, instead of inventing a country.
- **Right-click / custom locations** do not show that note (not from `cities.js`).

## What would be needed later (not implemented in this pass)

| Goal | Requirement |
|------|-------------|
| Reliable country line | Add `country` (and ideally `country_code`) to the dataset or resolve via geocoder |
| City / state / country disambiguation | Unique IDs, admin hierarchy, or structured labels (e.g. `"Springfield, IL, US"`) |
| Predictive autocomplete | Prefix index or search API; current UI is substring `includes` on full client list |
| Importance-based ranking | `pop` is already present; could combine with capital flags, wiki importance, etc. |

## Geocoder

A full geocoder or Places API is **not** wired here. Enriching `cities.js` or switching to an external search service would be a larger change and should stay out of this functional-correction pass unless the data model is extended deliberately.

**Next milestone (recommended):** replace or **augment** `cities.js` with records that include at minimum **`country`**, **`admin1` (state/region)** when applicable, **stable id**, and **alternate names** (or a server-side search index) so popups can show place hierarchy without guessing and search can disambiguate “Paris” / “Portland” / “Springfield.”
