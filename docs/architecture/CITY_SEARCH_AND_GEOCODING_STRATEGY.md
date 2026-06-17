# City Search & Geocoding Strategy

**Status:** Canon (revisable)  
**Date:** 2026-06-12  
**Related:** `WEB2_BACKEND_DECISIONS_FOR_REVIEW_v1_2026-06-12.md`, `WEB2_BACKEND_EXEC_SUMMARY.md`

---

## 1. Problem statement

Relocation decisions happen at **named places**. The product must:

1. Let users **search and disambiguate** cities (Portland, OR vs Portland, ME vs Portland, UK).
2. Store **canonical place records** (coordinates, country, region, timezone) permanently — birth cities, favorites, comparisons.
3. Show a **readable map** with labels that can respect **language** (e.g. München vs Munich).
4. Convert **birth date + local time + place** to **UTC** using **historical** timezone/DST rules — not today's rules.

These are **four separate systems**. Confusing them leads to wrong provider choices (especially around **storage rights**).

---

## 2. The four layers

| Layer | What it does | Provider | Cost | Status |
|-------|----------------|----------|------|--------|
| **A. Canonical dataset** | Offline city list with country, region code, timezone, population | **GeoNames** (`cities500.txt`) | Free | ✅ **Fixed** — `build_cities.py` now emits enriched JSON/JS |
| **B. Live autocomplete** | Type-ahead search, ranking, disambiguation UI | **Geoapify** (recommended) or Radar | Paid subscription | 🔲 Not wired yet |
| **C. Map tiles + label language** | The map picture and the words on it | **MapTiler** + **MapLibre** (recommended) | Paid subscription | 🔲 Sandbox still uses raw OSM |
| **D. Historical timezone** | Birth-time → UTC with correct DST for that date | **timezonefinder** + **IANA zoneinfo** (offline) | Free | 🔲 Named in `.env`, not integrated |

---

## 3. Layer A — Canonical dataset (done)

### What changed (2026-06-12)

`build_cities.py` was re-written. It previously dropped country/region/timezone from GeoNames. It now emits:

**Per city:**
- `geoname_id`, `name`, `lat`, `lng`, `pop`
- `country_code`, `country` (English name)
- `admin1_code`, `admin1` (region — full name when `admin1CodesASCII.txt` is present)
- `timezone` (IANA id, e.g. `America/Chicago`)

**Outputs:**
- `cities5000_enriched.json` — canonical compact JSON
- `cities.js` — browser bundle (`const citiesData = [...]`)

**Run:**
```bash
python3 build_cities.py                  # all rows in cities500.txt
python3 build_cities.py --min-pop 5000   # cities ≥ 5,000 pop (~68k rows)
```

### Optional GeoNames reference files (free download)

Place these in the repo root to enrich region **names** (not just codes):

| File | Source | What it adds |
|------|--------|----------------|
| `countryInfo.txt` | [geonames.org/datasets/countryInfo.txt](https://download.geonames.org/export/dump/countryInfo.txt) | Overrides built-in country names |
| `admin1CodesASCII.txt` | [geonames.org/datasets/admin1CodesASCII.txt](https://download.geonames.org/export/dump/admin1CodesASCII.txt) | `OR` → `Oregon`, `14` → `Lisboa` |
| `alternateNamesV2.txt` | [geonames.org/datasets/alternateNamesV2.zip](https://download.geonames.org/export/dump/alternateNamesV2.zip) | Multilingual + historical names (Bombay/Mumbai) — future ingest |

### Display format (UI canon)

Abbreviate in compact UI; full names in disambiguation:

- Compact: `Portland, OR · USA`
- Disambiguation list: `Portland, Oregon, United States`
- Birth chart plate: full place string per existing UI canon

### Alignment with `places` table

`repositories/places_repository.create_place()` already accepts: `display_name`, `latitude`, `longitude`, `country_code`, `country_name`, `admin1`, `admin2`, `timezone_id`, `geonames_id`, `provider`, `provider_place_id`. Layer A + B should populate these fields when a user picks a city.

---

## 4. Layer B — Live autocomplete (subscription)

### Hard requirement: storage rights

We **permanently store** user birth cities, favorites, and search results. Many providers forbid this.

| Provider | Autocomplete | Store results? | Multilingual | Country/region | Notes |
|----------|--------------|--------------|--------------|----------------|-------|
| **Geoapify** ✅ | Good (OSM) | **Yes** | Yes | Yes | Already in `.env`; predictable pricing |
| **Radar** | Good | **Yes** | Yes | Yes | Cheaper per-request; Google-like API |
| Mapbox | Best UX | Only **Permanent** tier (costly) | Yes | Yes | Great if map is also Mapbox |
| Google Places | Best coverage | **No** permanent storage | Yes | Yes | **Disqualified** for birth-city storage |

### Recommended: Geoapify

- Already configured: `GEOAPIFY_API_KEY` in `.env.example`
- [Geoapify Geocoding API](https://www.geoapify.com/geocoding-api/)
- [Geoapify Autocomplete API](https://www.geoapify.com/address-autocomplete/)
- [Pricing](https://www.geoapify.com/pricing/)
- Storage-friendly license vs Google

### Integration pattern

1. User types in city search → call Geoapify Autocomplete (debounced).
2. User selects a result → **persist** to `places` table via Supabase (geoname_id or provider_place_id + full fields).
3. Offline/fallback: search local `cities5000_enriched.json` when API unavailable (optional).

### Runner-up: Radar

- [Radar Geocoding](https://radar.com/product/geocoding-api)
- [Pricing](https://radar.com/pricing) — 100k free/mo, $0.50/1k after
- Good if Geoapify limits are hit

---

## 5. Layer C — Map tiles + label language

**This is not city search.** It is the **map imagery** and the **text printed on the map**.

### Founder requirement: one native language per map view

The map must render **all labels in the user's chosen language** — a whole-map setting, e.g. everything in English *or* everything in Japanese. We explicitly do **not** want raw OSM behavior, which prints each place in its local script (Tokyo in Japanese, القاهرة in Arabic, Paris in French) all on the same map. A single `language` parameter on a vector-tile style delivers this; raster OSM cannot.

Raw OpenStreetMap raster tiles (current sandbox) cannot switch label language cleanly. For localized labels:

| Piece | Role | Link |
|-------|------|------|
| **MapLibre GL JS** | Open-source map renderer (no vendor lock-in) | [maplibre.org](https://maplibre.org/) |
| **MapTiler** | Vector tiles + `language` parameter for labels | [maptiler.com](https://www.maptiler.com/) |
| Mapbox GL | Alternative renderer + tiles (stronger ecosystem, more lock-in) | [mapbox.com](https://www.mapbox.com/) |

### Recommended: MapTiler + MapLibre

- [MapTiler Cloud](https://cloud.maptiler.com/) — sign up, get API key
- [MapTiler pricing](https://www.maptiler.com/cloud/pricing/)
- [MapLibre language example](https://maplibre.org/maplibre-gl-js/docs/examples/language-switch/) — exactly the "set whole map to one language" pattern
- Keeps map display independent from Geoapify search data
- Mapbox also satisfies the single-language requirement; choose based on pricing/ecosystem (reviewer question)

---

## 5b. Layer E — Dynamic text translation (DeepL)

Map labels (Layer C) and app/AI text are **different problems**. The tile provider handles map labels; **DeepL** handles everything else that is generated or written text:

- **AI interpretations / overlay copy** — translate generated narrative into the user's language.
- **UI strings** — can be pre-translated and stored, or translated on demand.
- **Notes (optional)** — user notes could be machine-translated for cross-language review.

| Piece | Role | Link |
|-------|------|------|
| **DeepL API** | High-quality machine translation for dynamic text | [deepl.com/pro-api](https://www.deepl.com/pro-api) |

**Pattern (reviewer question — pick one):**
- **Pre-translate & store** static/UI strings (cheaper at runtime, more storage).
- **Translate on demand + cache** AI/overlay text in a `translations` cache table keyed by source hash + target lang (best for dynamic content).

DeepL must run **server-side** (Supabase Edge Function or backend) so the API key is never exposed.

---

## 6. Layer D — Historical timezone

Geocoders return **today's** timezone for a coordinate. Birth charts need the rules **in effect on the birth date** (DST changes, pre-1970 zones, etc.).

### Recommended stack (already named in `.env.example`)

| Piece | Role | Link |
|-------|------|------|
| **timezonefinder** | lat/lon → IANA timezone id | [PyPI](https://pypi.org/project/timezonefinder/) |
| **zoneinfo** (Python 3.9+) | IANA rules + historical DST | [docs](https://docs.python.org/3/library/zoneinfo.html) |
| **pytz** (fallback) | Older historical edge cases | [PyPI](https://pypi.org/project/pytz/) |

### Where this runs

- **Must be server-side or trusted library** — not a subscription API.
- Input: `(lat, lon, local_datetime)` from the user's chosen place + birth time.
- Output: UTC instant + offset metadata for the chart engine.
- Layer A's `timezone` field is the starting IANA id; historical conversion is Layer D's job.

---

## 7. Shopping list (accounts to create)

Use this checklist. Founder action required for billing/signup on paid services.

### Free — do now

| # | Item | Action | Link |
|---|------|--------|------|
| 1 | GeoNames reference files | Download `admin1CodesASCII.txt` (+ optional `countryInfo.txt`) into repo root; re-run `build_cities.py` | [GeoNames export](https://download.geonames.org/export/dump/) |
| 2 | Supabase project | Confirm project is live; copy **anon key** + **service role key** into `.env` | [Supabase dashboard](https://supabase.com/dashboard) |
| 3 | MapLibre | No account needed (open source) | [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/) |

### Paid subscriptions — recommended stack

| # | Service | Purpose | Sign up | Pricing |
|---|---------|---------|---------|---------|
| 4 | **Geoapify** | City autocomplete + geocoding (storage allowed) | [geoapify.com](https://www.geoapify.com/) | [Pricing](https://www.geoapify.com/pricing/) |
| 5 | **MapTiler** | Map tiles + single-language labels | [cloud.maptiler.com](https://cloud.maptiler.com/) | [Pricing](https://www.maptiler.com/cloud/pricing/) |
| 6 | **DeepL** | Translate AI/UI/overlay/notes text | [deepl.com/pro-api](https://www.deepl.com/pro-api) | [Pricing](https://www.deepl.com/pro/change-plan) |
| 7 | **Supabase** (if exceeding free tier) | Database + auth hosting | [supabase.com/pricing](https://supabase.com/pricing) | Free tier generous for dev |

### Auth provider consoles (founder must register apps)

| # | Provider | Purpose | Console |
|---|----------|---------|---------|
| 7 | **Google Cloud** | "Sign in with Google" | [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials → OAuth 2.0 |
| 8 | **Apple Developer** | "Sign in with Apple" (requires paid Apple Developer account, ~$99/yr) | [developer.apple.com](https://developer.apple.com/account/) |
| 9 | **Supabase Auth** | Wire OAuth providers | [Supabase Auth docs](https://supabase.com/docs/guides/auth/social-login) |

**Not available:** Instagram login (Meta retired third-party Instagram OAuth). Use **Facebook** if a Meta login is desired: [Meta for Developers](https://developers.facebook.com/).

### Optional / later

| # | Service | When | Link |
|---|---------|------|------|
| 10 | Radar | If Geoapify limits hit | [radar.com](https://radar.com/) |
| 11 | Vercel or Netlify | Frontend hosting when leaving pure local HTML | [vercel.com](https://vercel.com/) / [netlify.com](https://www.netlify.com/) |
| 12 | Stripe | Payments (post-Web2 v1) | [stripe.com](https://stripe.com/) |

### Keys to collect (`.env`)

```env
# Already in .env.example — fill in real values:
SUPABASE_URL=
SUPABASE_ANON_KEY=          # browser-safe (with RLS)
SUPABASE_SERVICE_ROLE_KEY=  # server only — NEVER in browser

GEOAPIFY_API_KEY=           # Layer B autocomplete

# Add when ready:
MAPTILER_API_KEY=           # Layer C map tiles (single-language labels)
DEEPL_API_KEY=              # Layer E text translation (server-side only)
```

---

## 8. Build order (within Web2 plan)

1. ✅ Layer A — enriched GeoNames dataset (`build_cities.py`)
2. 🔲 Download `admin1CodesASCII.txt` → re-run → full region names
3. 🔲 Layer B — wire Geoapify autocomplete into city search UI; persist to `places`
4. 🔲 Layer D — historical timezone conversion for birth-time entry
5. 🔲 Layer C — swap sandbox OSM tiles for MapTiler + MapLibre with language param
6. 🔲 Map density rules (zoom thresholds, label collision) — separate pass

---

## 9. Revision log

| Date | Change |
|------|--------|
| 2026-06-12 | v1 — Four-layer model; GeoNames fix; Geoapify + MapTiler + offline tz recommended; shopping list; storage-rights constraint documented |
| 2026-06-12 | v1.1 — Added founder multilingual direction: single-native-language map labels (Layer C) + Layer E DeepL for dynamic text; verified live Supabase schema (`places` has `language_code` + `alternate_names_json`) |
| 2026-06-16 | Addendum — "Location Search" terminology; two-bar map model (Search Favorites / Search All Locations); one shared Location Search architecture (see §10) |

---

## 10. Addendum — Location Search doctrine (Favorites vs All Locations)

**Date:** 2026-06-16
**Type:** Doctrine addendum (documentation only — no implementation authorized by this entry)

### 10.1 Terminology

Use the term **"Location Search,"** not "City Search." A user's relocation
targets include cities, towns, named non-city places, and arbitrary map-click /
wilderness / custom coordinate points — not only cities.

### 10.2 Two stacked search bars on the map

The map should eventually present **two stacked search bars**:

1. **Search Favorites**
2. **Search All Locations**

These are distinct surfaces with distinct sources, not one search box.

### 10.3 Search Favorites — scope

Search Favorites searches the user's saved set for the active chart/profile:

- favorited cities
- favorited named locations
- arbitrary map-click / wilderness / custom coordinate favorites
- saved locations attached to the active chart/profile

### 10.4 Search All Locations — scope

Search All Locations searches the global location database and (future)
providers:

- global location database results
- cities
- towns
- future geocoder / location-provider results
- aliases, abbreviations, alternate spellings, historical spellings, and
  disambiguation (per the production requirements in
  `CITY_SEARCH_PRODUCTION_REQUIREMENTS.md`)

### 10.5 Important distinction — Favorites are not only custom places

Favorites are **not** only custom/random/wilderness points. Favorites also
include **normal cities the user intentionally saved**. A city appearing in the
global database does not exclude it from Favorites; the two surfaces overlap by
design.

### 10.6 Product reason for Search Favorites

Search Favorites is the **only reliable way** for users to reopen arbitrary
saved map locations that **do not exist in a standard location database**
(map-click points, wilderness coordinates, custom places). Without it, those
saved places are unreachable by name. This is why Favorites needs its own search
surface rather than relying on All Locations alone.

### 10.7 Interaction direction

Clicking either search bar opens a **dropdown / autocomplete panel**. Location
Search should **not** become a full-screen search system by default.

### 10.8 Architecture direction — one shared Location Search

This should eventually become **one shared Location Search architecture** reused
by:

- map search
- birth location search
- current location search
- comparison / favorite selection
- future location pickers

The shared system separates concerns: a search layer that returns ranked
candidates (favorites, recents, saved, and global results), and a resolution
layer that maps a chosen candidate to a canonical `places` row. Today these are
partly duplicated across the map, the current-location editor, and the birth
intake; convergence onto one architecture is the target.

This addendum records doctrine and direction only. No code, schema, or UI change
is authorized by this entry.
